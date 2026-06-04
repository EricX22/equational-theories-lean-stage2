# Solver Implementation Handoff

This note summarizes the current `solver.py` structure so future patches can target specific functions without rereading the whole file.

## Big-picture architecture

The solver is a Solo-track SAIR Stage 2 solver. It reads one problem JSON from stdin, communicates with the proxy using JSON messages, and either asks the judge to verify a Lean certificate or asks the LLM for a response.

Current control flow in `main()`:

1. Normalize `*` to `◇`.
2. Try false certificates:
   - exhaustive finite magma search on `Fin 2`–`Fin 3`;
   - named fixed witness tables;
   - one-cell perturbations around structured tables;
   - structured table families on `Fin 4`–`Fin 7`.
3. Try true certificates:
   - direct `h` instantiation by syntactic unification;
   - two-step `h` transitivity chain;
   - singleton small-model hint;
   - bounded equality graph from goal LHS to goal RHS;
   - singleton equality graph from `p` to `q`;
   - generic Lean tactics unless Eq1 has a bare variable side;
   - trivial singleton template;
   - structural singleton templates.
4. Current behavior: if `singleton=True` and all deterministic stages fail, it stops before LLM fallback. Non-singleton cases may still use the LLM fallback.

## Protocol and logging functions

### `read_message() -> dict`
Reads one JSON line from stdin. Used for startup problem and proxy replies.

### `send_message(msg: dict) -> None`
Writes one JSON line to stdout and flushes. Used for judge/LLM calls.

### `call_judge(verdict: str, code: str) -> dict`
Sends `{"call": "judge", "verdict": verdict, "code": code}` and returns the proxy response. A status of `accepted` means the runner records the answer automatically.

### `call_llm(context: dict) -> dict`
Sends `{"call": "llm", "context": context}`. The proxy fills the module-level `PROMPT` template.

### `trace(msg: str) -> None`
Prints diagnostics to stderr. This is safe because stdout must remain JSON-protocol-only.

## Basic equation parsing and finite evaluation

### `parse_equation(text: str) -> (list[str], lhs_fn, rhs_fn)`
Parses an equation string into:

- `variables`: variables in first-appearance order;
- `lhs_fn(env)`, `rhs_fn(env)`: evaluators over an environment containing variable values and `env["op"]`.

This parser is for finite table evaluation, not symbolic proof search.

### `equation_holds(variables, lhs_fn, rhs_fn, n: int, op) -> bool`
Checks whether an equation holds for all assignments of its variables over `Fin n` under operation `op`.

### `search_counterexample(eq1_text, eq2_text, max_n=3) -> (n, table) | (None, None)`
Exhaustively enumerates all `n^(n^2)` binary operation tables for `n = 2..max_n`. Returns the first table where Eq1 holds universally and Eq2 fails.

Use this for small complete finite-model search only. `Fin 4` full enumeration is too large.

## False-side structured witness search

### `_structured_tables(n: int) -> Iterator[list[list[int]]]`
Generates structured operation tables on `Fin n`, including:

- constants;
- left/right projections;
- cyclic addition/subtraction;
- min/max;
- multiplication mod `n`;
- simple linear forms;
- XOR for power-of-two sizes;
- constant-with-diagonal;
- identity-in-slot-0.

These are candidate false witnesses; the judge still verifies any returned table.

### `search_named_witnesses(eq1_text, eq2_text) -> (name, n, table) | (None, None, None)`
Checks a short hand-coded dictionary of known finite magmas such as LP, RP, XOR2, Z3, MAX/MIN, etc. Returns a named witness if Eq1 holds and Eq2 fails.

Patch point: add new high-yield named tables here.

### `search_counterexample_extended(eq1_text, eq2_text, sizes=(4,5,6,7)) -> (n, table) | (None, None)`
Runs Eq1/Eq2 evaluation over `_structured_tables(n)` for larger finite sets. This is cheap compared with exhaustive Fin 4+.

### `_perturb_table_one_cell(table) -> Iterator[table]`
Generates all operation tables that differ from `table` in exactly one cell.

### `search_perturbed_witnesses(eq1_text, eq2_text, sizes=(2,3,4), max_bases_per_n=24) -> (n, table) | (None, None)`
Uses `_structured_tables` as base tables, perturbs one cell, and checks whether any neighbor is a false witness. This is the first step toward constraint-guided false-model search.

Patch point: can generalize to two-cell perturbations, but be careful about blowup.

## Symbolic term representation

Symbolic terms are represented as tuples:

- variable: `("var", "x")`
- product: `("op", left_tree, right_tree)`

### `parse_to_tree(text: str) -> tree`
Parses a term expression into the tree representation.

### `unify(template: tree, target: tree, sigma: dict) -> dict | None`
First-order syntactic matching from template variables to target trees. Used to instantiate `h` when the goal is a substitution instance of Eq1.

Important: this is matching/unification over the equation variables, not algebraic equality modulo laws.

### `tree_to_str(tree) -> str`
Renders a tree as over-parenthesized Lean syntax using `◇`.

### `tree_size(tree) -> int`
Counts nodes in a term tree.

### `subterms(tree) -> list[tree]`
Returns the tree and all recursive subterms.

### `apply_subst_tree(tree, subst) -> tree`
Applies a tree-valued substitution to variables in a term.

### `ordered_unique(seq, max_items=None) -> list`
Deduplicates hashable items while preserving order.

## Equality-graph true proof search

The equality graph represents terms as nodes. Each edge is one instantiated use of `h` or `(h ...).symm`.

### `generate_candidate_terms(var_names, seed_terms=(), max_depth=2, max_terms=36, max_size=9) -> list[tree]`
Builds a bounded term universe from variables and seed terms. Terms are sorted/pruned by size.

Patch point: for hard singleton cases, this is where LLM strategist seed terms should be injected.

### `_bounded_arg_pool(candidates, arity, max_arg_combos=20000) -> list[tree]`
Shrinks the candidate pool until `len(pool)^arity` is within the max instantiation budget.

### `_build_h_edge_graph(h_vars, h_lhs, h_rhs, candidates, max_arg_combos=20000) -> dict`
Instantiates Eq1 over candidate terms and adds both directions as graph edges:

- `lhs -> rhs` justified by `h args`
- `rhs -> lhs` justified by `(h args).symm`

Returns adjacency mapping: `term -> [(next_term, proof_string), ...]`.

### `_find_path(adj, start, target, max_depth=4) -> list[(src, dst, proof)] | None`
Breadth-first search for a bounded equality path.

### `calc_from_path(path) -> str`
Converts a verified term path into Lean `calc` syntax.

### `try_bounded_equality_graph(problem, eq1_text, eq2_text, max_path_depth=4) -> bool`
Attempts to prove Eq2 directly by searching an equality path from goal LHS to goal RHS. If found, generates Lean mechanically and calls the judge.

### `try_singleton_equality_graph(problem, eq1_text, eq2_text, max_path_depth=5) -> bool`
Attempts to prove `∀ p q, p = q` by searching an equality path from symbolic `p` to symbolic `q`. If found, wraps it as:

```lean
intro <goal vars>
have key : ∀ (p q : G), p = q := by
  intro p q
  calc ...
exact key <goal_lhs> <goal_rhs>
```

Patch point: this is the natural place to add LLM-strategist seed terms and target equalities.

## Direct true-proof search

### `try_direct_h_application(problem, eq1_text, eq2_text) -> bool`
Checks whether Eq2 is directly an instance of Eq1 or its symmetric orientation. If so, emits:

```lean
intro <goal vars>
exact h <args>
```

or `.symm` variant and calls the judge.

### `try_two_step_h_chain(problem, eq1_text, eq2_text, max_judge_calls=6) -> bool`
Searches for a two-edge transitivity proof:

```lean
exact (h args1).trans (h args2)
```

with orientation variants. It unifies the first step with goal LHS, computes an intermediate term, and unifies the second step with goal RHS.

### `try_generic_tactics(problem, eq1_text, eq2_text, max_judge_calls=8) -> bool`
Tries generic Lean tactics such as `rw [h]`, `simp only [h]`, and same-argument `exact h ...` calls.

Current `main()` skips this when Eq1 has a bare-variable side because `rw [h]` often fails with metavariable-pattern errors.

## Singleton detection and templates

### `has_bare_side(eq_text: str) -> bool`
Checks whether either side of an equation is a single bare variable. Used to skip generic rewrite tactics.

### `forces_singleton(eq1_text) -> bool`
Current intent: small-model hint for whether Eq1 likely forces singleton behavior. It is used only for routing.

Important known issue: in some versions, this function checks whether a satisfying table has at least two distinct output values. That is too permissive: a constant operation on `Fin 2` is still a non-singleton magma because the carrier has two elements. The conservative version should return `False` as soon as any satisfying model on `Fin 2` or `Fin 3` exists.

### `try_trivial_singleton(eq1_text, eq2_text) -> str | None`
If Eq1 has shape `x = RHS` where `x` does not occur in `RHS`, creates a one-line singleton proof:

```lean
have key : ∀ (a b : G), a = b := fun a b => ...
exact key <goal_lhs> <goal_rhs>
```

Returns proof body string or `None`.

### `_canonical_rename(text) -> (canon_text, mapping)`
Renames variables by first appearance to canonical names: first variable `x`, then `a`, `b`, `c`, ... Used to key structural templates by shape rather than by problem ID.

### `try_structural_singleton_pattern(problem, eq1_text, eq2_text) -> bool`
Matches canonical Eq1 shapes and emits verified hand-written singleton proofs. Currently includes at least:

- `x = (a ◇ x) ◇ b`
- `x = a ◇ (x ◇ ((b ◇ c) ◇ c))`

Patch point: add new hard-singleton shapes here once a proof is verified. This is currently the highest-yield place for sample-20 true hard cases.

## Lean code generation

### `make_false_code(n: int, table: list[list[int]]) -> str`
Builds a false certificate using `Fin n`, `finOpTable`, and `decideFin!`.

### `make_true_code(proof_body: str) -> str`
Wraps a proof body as:

```lean
import JudgeProblem

def submission : Goal := by
  intro G _ h
  <proof_body>
```

Proof bodies should only introduce goal variables and solve `EquationRHS G`.

## LLM parsing and filters

### `extract_json(text: str) -> dict | None`
Removes `<think>` blocks and code fences, then parses JSON.

### `clean_proof(p: str) -> str`
Normalizes LLM proof text:

- replaces `*` with `◇`;
- strips import lines;
- strips theorem/def wrappers;
- strips leading `by`.

### `goal_vars(eq_text)` / `_goal_vars(eq_text)`
Both return variables in first-appearance order. There is duplicated functionality.

### `intro_arity_ok(proof, eq2_text) -> bool`
There are duplicate definitions in the current file. The later definition overrides the earlier one in Python. The earlier version rejects accidentally introducing `h`; the later version may not. Patch should remove the duplicate or make the later version stricter.

## Current known issues / patch priorities

1. **`forces_singleton` should be conservative.** Return `False` on any satisfying `Fin 2`/`Fin 3` model, regardless of table output diversity.
2. **Duplicate `intro_arity_ok`.** The later definition overrides the earlier stricter one. Remove the duplicate or keep one strict version.
3. **Timing constants.** Current file has `BUDGET_SECONDS = 110` and `MIN_SECONDS_FOR_LLM = 8`; this is inconsistent with Solo's 3600s startup budget. Prefer reading `startup["budget"]["timeout_seconds"]` in `main()`.
4. **LLM hard-singleton fallback is currently skipped.** That is reasonable given bad proof generation, but the next direction is an LLM strategist that returns seed terms/target equalities, not Lean code.
5. **`PROMPT` is still proof-generation oriented.** For the strategist architecture, add a mode that asks for JSON search hints instead of final Lean.
6. **Graph search is shallow and seed-limited.** To improve true hard cases, feed candidate terms from templates, observed subterms, or LLM strategist output into `try_singleton_equality_graph`.

## Proposed next patch: LLM strategist instead of Lean writer

Target architecture for hard singleton cases:

1. Deterministic stages fail.
2. If `singleton=True`, call LLM with `mode="lemma_strategy"`.
3. LLM returns JSON only:

```json
{
  "mode": "lemma_strategy",
  "skeleton": "singleton_path",
  "seed_terms": ["p", "q", "p ◇ q", "q ◇ p"],
  "target_equalities": [["p", "q"]]
}
```

4. Parse seed terms with `parse_to_tree`.
5. Add them to `generate_candidate_terms` seed terms.
6. Run `_build_h_edge_graph` and `_find_path`.
7. Generate Lean mechanically with `calc_from_path`.

This keeps the LLM out of exact Lean proof authoring, where it has been unreliable.
