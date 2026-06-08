# Evidence-Sequenced Strategy for the Equational Theories Solver

_Last updated: 2026-06-08_

## Purpose

This document records the current strategy for the SAIR Equational Theories Stage 2 solver after reading:

1. **The Equational Theories Project (ETP)** paper, which explains how the original magma-law implication graph was solved at scale.
2. **Twee: An Equational Theorem Prover**, which gives the right model for a true-proof engine based on completion, critical pairs, normalization, scoring, redundancy, and proof objects.
3. **Draft, Sketch, and Prove (DSP)**, which gives a good division of labor for LLMs: the model proposes structure, while an automated prover fills and verifies the details.

The strategy has been revised around the main empirical lesson from our current solver work:

> The realized gains so far are deterministic. The LLM-guided completion idea is promising, but it is still an experimental hypothesis that should be tested only on the residual non-singleton true cases after the deterministic floor is built.

The solver strategy should therefore be:

```text
First build and measure the deterministic completion floor.
Then isolate the leftover non-singleton true cases.
Then test whether LLM guidance uniquely solves any of that residual.
```

The intended long-term architecture remains:

```text
Finite models refute.
Completion proves.
LLM proposes where to search.
Lean verifies.
```

But the implementation order should not front-load the LLM.

---

## 1. Competition setting

Each problem asks whether one magma law implies another:

```text
Eq1 => Eq2
```

A magma is a carrier set with one binary operation `◇`. A law is an identity over variables and `◇`, for example:

```text
x ◇ y = y ◇ x
x = y ◇ (z ◇ x)
(x ◇ y) ◇ z = x ◇ (y ◇ z)
```

The solver must return one of two certificates:

```text
TRUE  -> Lean proof that every magma satisfying Eq1 satisfies Eq2.
FALSE -> finite magma table satisfying Eq1 and violating Eq2.
```

The final certificate is judged by Lean. This is why search can be heuristic, but accepted output must be machine-checkable.

---

## 2. Revised strategic split: true cases are not one class

The previous strategy blurred two different true subclasses:

```text
A. Singleton true cases
B. Non-singleton true cases
```

This distinction matters because the required machinery is very different.

### 2.1 Singleton true cases: nearly free, deterministic, ship first

A singleton-forcing law collapses every element of every satisfying magma to the same value. Once we derive:

```lean
key : ∀ (p q : G), p = q
```

any Eq2 follows immediately:

```lean
exact key goal_lhs goal_rhs
```

Empirically, this class is much easier than the general true problem. Our current proof-carrying completion prototype, described as `docs/completion_engine_reference.py`, reportedly clears the singleton portion of `sample_20` by using only 1-3 self-overlap iterations. It does not need goal direction, scoring coefficients, LLM waypoints, or sophisticated redundancy.

Status note:

```text
Project-local status: proof-carrying completion engine cleared 10/20 sample_20 end-to-end in Python.
Remaining validation risk: the generated proof traces still need to be checked against the real Lean judge/toolchain in the competition environment.
```

This means the singleton plan is:

```text
1. Keep the deterministic singleton engine simple.
2. Integrate it into solver.py.
3. Validate emitted Lean on the real judge.
4. Do not spend LLM or advanced completion effort here unless regression tests expose a gap.
```

### 2.2 Non-singleton true cases: actual research problem

Non-singleton true cases are the hard true class. Here Eq1 does not collapse all elements, so the proof must show that Eq2’s LHS and RHS normalize to a common form, or otherwise derive a specific equality path between them.

This is where the Twee-inspired machinery earns its keep:

```text
- R/Q completion loop
- critical pair generation
- goal-directed scoring
- Eq2 subterm bias
- redundancy control
- LLM-guided seed terms or waypoints
```

The key open question is:

```text
Can LLM guidance solve non-singleton true cases that deterministic completion-lite misses within budget?
```

This is not yet proven. It should be measured early.

---

## 3. What each source contributes

### 3.1 ETP: deterministic search and verified artifacts are the foundation

The ETP paper is the closest source to the competition setting: it studied implications between magma laws, formalized proofs/refutations in Lean, and exploited deterministic and ATP-style tools at scale.

Relevant lessons:

```text
- Finite counterexamples are extremely important for false implications.
- Syntactic methods, duality, and transitivity reduce direct proof burden.
- ATP-style automation was more useful than direct public-LLM proof generation.
- Lean verification is the final trust layer.
```

The ETP paper specifically notes that simple rewriting rules for laws of the form `x ≃ f(y,z,...)` identify singleton-equivalent laws, and that duality significantly reduces the number of implications needing direct proof. It also reports that only 10,657 positive implications needed direct proof after using preorder and duality structure.

For false cases, ETP found that small finite magmas and structured model families were central. It also reports that every order-≤4 law is either equivalent to the singleton law or has a non-trivial finite model, with almost all non-singleton laws having a model of size 2-5 and one exceptional pair needing size 7.

Implication for our solver:

```text
Build a strong pure-Python finite refuter and a deterministic singleton prover before investing in LLM-guided true search.
```

### 3.2 Twee: completion is the right model for non-singleton true proofs

Twee implements an unfailing Knuth-Bendix completion loop. Its state consists of:

```text
R = active rewrite rules / unorientable equations
Q = passive candidate critical pairs, initially containing axioms
J = ground-joinable equations used for subsumption
Goal = kept normalized with respect to R
```

The main loop is:

```text
1. Pop the lowest-scoring candidate from Q.
2. Normalize it using R.
3. If it is trivial/redundant, discard it or record redundancy.
4. Otherwise orient/add it to R.
5. Generate critical pairs between the new rule and R.
6. Normalize the goal.
7. If the goal becomes t = t, theorem proved.
```

Twee also stores proof objects for active rules. It only trusts low-level proof steps such as reflexivity, symmetry, transitivity, congruence, and applying an axiom/lemma. This is exactly the style we need: the search engine can derive equations, but every accepted rule must carry enough proof information to later render Lean.

Implication for our solver:

```text
The non-singleton true engine should be a proof-carrying completion-lite engine, not an LLM proof generator.
```

### 3.3 DSP: the LLM should sketch, not prove

DSP’s pipeline is:

```text
informal proof draft -> formal sketch -> automated prover fills gaps
```

The useful analogy for our task is:

```text
LLM rewrite strategy -> deterministic completion search -> Lean certificate
```

DSP supports the idea that LLMs can provide structure while a formal prover supplies correctness. Its ablation study also warns against removing the automated prover: the prover is doing essential work.

Implication for our solver:

```text
LLM output should only affect candidate generation, search priority, and waypoints.
It should not be accepted directly as a proof.
```

---

## 4. Current project status

### 4.1 Existing solver.py baseline

The current solver already has a useful deterministic base:

```text
False side:
  - exhaustive Fin 2-3 search
  - named fixed tables
  - one-cell perturbations around structured tables
  - structured Fin 4-7 table families

True side:
  - direct h instantiation
  - two-step h chain
  - bounded equality graph from Eq2.lhs to Eq2.rhs
  - singleton equality graph from p to q
  - generic tactics where safe
  - trivial singleton template
  - structural singleton templates

LLM:
  - still mostly proof-generation oriented
  - hard singleton fallback currently low-yield/skipped in some versions
```

Known existing design issue:

```text
The old LLM path asks for Lean proof bodies. That is unreliable and should not be the primary path.
```

### 4.2 Completion engine reference status

Project-local report:

```text
File: docs/completion_engine_reference.py
Status: proof-carrying completion engine with H/SYM/TRANS/CL/CR traces and a Python ptype checker.
Observed result: cleared 10/20 sample_20 instantly, corresponding to singleton-collapse cases.
```

Caveat:

```text
I do not have this file in the current active sandbox, so this document records the described status rather than independently inspecting the file. The remaining risk is Lean-side validation of emitted certificates in the real judge environment.
```

This changes the milestone plan: the proof-traced normalizer is no longer a greenfield task. It should be treated as built, tested in Python, and awaiting Lean integration/validation.

---

## 5. Engine A: pure-Python finite refuter

Purpose:

```text
Find a finite magma satisfying Eq1 and violating Eq2.
```

Output:

```text
Lean false certificate: Fin n table + decideFin!
```

Planned search families:

```text
1. Exhaustive Fin 2-3 enumeration.
2. Named tables: projections, constants, XOR, cyclic, min/max, etc.
3. Structured Fin 4-7 tables.
4. Linear modular magmas: x ◇ y = a*x + b*y mod p.
5. Affine modular magmas: x ◇ y = a*x + b*y + c mod p.
6. Very small low-degree modular magmas.
7. One-cell/two-cell perturbations around structured bases.
8. Later: greedy partial-table construction.
```

Important implementation constraint:

```text
The in-solver refuter must stay pure Python.
Do not rely on z3, SMT solvers, network access, or external dependencies.
```

SMT/Z3 can be used for dev-time exploration, but the submitted `solver.py` must hand-roll enumeration/search and emit a table that the Lean judge checks.

---

## 6. Engine B1: deterministic singleton prover

Purpose:

```text
Prove Eq1 forces singleton, then finish Eq2 by applying ∀ p q, p = q.
```

Current evidence says this class is cheap and should be shipped before adding LLM complexity.

Expected method:

```text
1. Build a generic p, q target.
2. Use Eq1 self-overlaps and simple proof-carrying completion.
3. Derive key : ∀ p q, p = q.
4. Apply key to Eq2.lhs and Eq2.rhs.
```

Why goal direction is usually unnecessary here:

```text
Once key is proved, Eq2 no longer matters.
The target is always p = q.
Therefore Eq2 waypoints and goal-subterm scoring are irrelevant.
```

Implementation priority:

```text
P0: integrate the existing completion_engine_reference.py singleton engine into solver.py.
P0: validate generated Lean against the real judge.
P1: add regression tests for sample_20 singleton cases.
P2: only then generalize or optimize.
```

---

## 7. Engine B2: deterministic non-singleton completion-lite

Purpose:

```text
Prove Eq2 from Eq1 without singleton collapse.
```

This is the actual true-side research problem.

The engine should implement the minimal useful subset of Twee:

```text
R = active accepted rules with proof traces
Q = priority queue of candidate equations
J = optional redundancy-pattern cache
Goal = Eq2.lhs = Eq2.rhs, repeatedly normalized
```

### 7.1 Completion-lite loop

```text
initialize:
  Q = [Eq1]
  R = []
  goal = parsed Eq2

loop:
  candidate = pop_best(Q)
  candidate = normalize_equation(candidate, R)

  if candidate is trivial:
      discard
  elif candidate is duplicate / too large / too deep:
      discard
  else:
      rule = orient_or_keep(candidate)
      add rule to R with proof trace

      normalize goal_lhs and goal_rhs using R
      if normal forms match:
          render Lean proof and submit

      generate critical pairs between rule and existing R
      score and push useful ones into Q
```

### 7.2 Milestone sequencing for B2

These should be run before any LLM strategist work:

```text
M1. Integrate proof-traced normalization from completion_engine_reference.py.
M2. Validate emitted Lean for singleton cases on real judge.
M3. Add self-overlap generation for general Eq1.
M4. Add rule-rule overlap generation.
M5. Run deterministic ablation on true problems.
```

Only after M5 should we decide whether LLM guidance is worth implementing.

### 7.3 Search control and redundancy

For non-singleton true cases, scoring and redundancy matter because Q can explode. Twee reports that the passive set is quadratic in active rules and can contain millions of critical pairs, so even completion-lite needs caps.

Start with cheap controls:

```text
- max term size
- max derivation depth
- max active rules
- max Q size
- exact duplicate keys
- ordinary joinability
- timeout-aware early stop
```

Delay expensive redundancy features:

```text
Later 1: subsumption-lite J cache
Later 2: connectedness-lite for small terms
Later 3: ground-joinability-lite for variable-order cases
```

Do not implement full ground joinability until deterministic B2 results show Q explosion is the bottleneck.

---

## 8. Engine C: LLM strategist as a tested hypothesis

Previous framing made LLM-guided search sound like the core competitive edge. Revised framing:

```text
The competitive edge is a strong in-process completion engine.
LLM guidance is a hypothesis for the leftover non-singleton true residual.
```

The LLM should be wired in only after we can measure a residual where it might help.

### 8.1 Where the LLM could help

Two plausible roles remain:

```text
1. Initial Q guidance:
   Suggest seed terms, substitutions into Eq1, and promising self-overlaps.

2. Eq2 direction:
   Suggest waypoints, priority terms, and whether to bias toward goal_lhs, goal_rhs, or a shared normal form.
```

The LLM output should be strict JSON hints, for example:

```json
{
  "classification": "true_non_singleton | true_singleton | false_likely | unknown",
  "strategy": "completion | equality_graph | singleton_path | refuter_bias | dual_first",
  "seed_terms": ["x", "y", "x ◇ y", "y ◇ x"],
  "candidate_substitutions": [
    {"x": "x ◇ y", "y": "z"}
  ],
  "waypoints": [
    ["goal_lhs", "x ◇ (y ◇ z)"],
    ["x ◇ (y ◇ z)", "goal_rhs"]
  ],
  "priority_terms": ["x ◇ y", "y ◇ z"],
  "try_dual": true,
  "max_term_size_hint": 11
}
```

### 8.2 What the solver may do with LLM output

Allowed:

```text
- parse seed terms
- reject invalid terms
- add valid terms to candidate universe
- seed Q with valid Eq1 instantiations
- apply scoring bonuses to candidates touching waypoints/priority terms
- run dual mode if cheap
```

Not allowed:

```text
- trust the classification as final verdict
- accept raw Lean from the LLM
- accept unverified equality claims
- rely on LLM-suggested counterexample validity
```

### 8.3 Early ablation gate

Before building Engine C fully, run:

```text
A. Existing solver only.
B. Existing solver + deterministic singleton completion.
C. Existing solver + deterministic singleton completion + non-singleton completion-lite.
```

Then classify residual failures. Engine C is worth implementing only if:

```text
1. There is a sizable true non-singleton residual.
2. Failures look like search-direction problems rather than proof-rendering bugs.
3. Candidate traces show the right term families are absent or delayed.
```

If the residual is mostly false cases or Lean-rendering failures, LLM guidance is the wrong investment.

---

## 9. Implementation gotchas already discovered

These should be treated as hard implementation requirements.

### 9.1 Rename rules apart before matching

In rewriting, the rule and target term share a variable namespace unless we deliberately separate them. If we match without renaming the rule variables apart, a rule variable can bind to a term containing itself, causing recursive substitutions and eventually a `RecursionError` or worse.

Required rule:

```text
Before matching rule.lhs against a target subterm, alpha-rename every rule variable to a fresh namespace.
```

Example namespace scheme:

```text
rule variable x -> __r17_x
rule variable y -> __r17_y
```

Then matching can safely bind `__r17_x` to a target term containing ordinary `x`.

### 9.2 Do not dereference identity substitutions when computing proof types

Computing a proof type with an identity substitution can loop under recursive dereferencing. For proof bookkeeping, use a plain simultaneous substitution that does not chase identity mappings forever.

Required rule:

```text
For proof type computation, use non-deref simultaneous substitution.
Reserve deref/chasing substitution for actual matching/unification, with occurs checks or acyclic substitution invariants.
```

### 9.3 Lean judge validation is a separate risk

Python proof typing can validate internal consistency, but it does not guarantee Lean accepts the rendered proof.

Required rule:

```text
Every new proof-rendering path must be validated against the real Lean judge before being considered solved.
```

This is especially important for the already-working singleton completion engine.

---

## 10. Evaluation plan: run the ablation early

The ablation plan should be an early decision instrument, not an end-of-project evaluation.

### 10.1 Main comparisons

```text
A. Existing solver baseline.
B. Baseline + integrated singleton completion engine.
C. B + deterministic non-singleton completion-lite.
D. C + simple Eq2 goal bias, no LLM.
E. D + LLM initial-Q seed terms.
F. E + LLM waypoints / Eq2 direction.
```

The key decision is between C/D and E/F:

```text
Does LLM guidance uniquely solve non-singleton true cases that deterministic completion-lite misses under the same budget?
```

### 10.2 Metrics

```text
Overall:
  - solved count
  - true solved count
  - false solved count
  - time per solved problem
  - timeout count

Singleton true:
  - number routed to singleton engine
  - number proved by singleton engine
  - Lean judge acceptance rate
  - self-overlap iterations used

Non-singleton true:
  - number attempted
  - number solved by direct h/two-step/equality graph
  - number solved by deterministic completion-lite
  - number solved only with Eq2 goal bias
  - number solved only with LLM hints
  - accepted rule count at success
  - peak Q size

LLM usefulness:
  - parse rate of LLM terms
  - valid substitution rate
  - hints used in successful proof traces
  - unique solves attributable to LLM
  - wasted calls on false/easy-singleton cases
```

---

## 11. Building a labeled non-singleton true evaluation set

This is the key dataset needed to decide whether Engine C is worth building.

### 11.1 Best source: public problem files with labels

Use the public problem files bundled with the competition repo:

```text
examples/problems/sample_20.json
examples/problems/sample_200.json
examples/problems/normal.jsonl
examples/problems/hard1.jsonl
examples/problems/hard2.jsonl
examples/problems/hard3.jsonl
```

They include `answer` labels in the public practice sets.

### 11.2 Derive buckets

For every problem:

```text
if answer == false:
    bucket = FALSE
else:
    if singleton_detector(eq1) == true:
        bucket = TRUE_SINGLETON_CANDIDATE
    else:
        bucket = TRUE_NON_SINGLETON_CANDIDATE
```

Then refine by actual solver behavior:

```text
TRUE_SINGLETON_SOLVED:
  answer=true and singleton engine proves it

TRUE_SINGLETON_UNSOLVED:
  answer=true and singleton detector says singleton but singleton engine fails

TRUE_NON_SINGLETON_SOLVED_BY_BASELINE:
  answer=true, non-singleton candidate, solved by direct h/two-step/equality graph

TRUE_NON_SINGLETON_RESIDUAL:
  answer=true, non-singleton candidate, not solved by baseline or singleton engine
```

The last bucket is the target population for LLM-guided completion.

### 11.3 Singleton detector caution

A small-model singleton detector must be conservative.

Bad criterion:

```text
Eq1 has no satisfying Fin 2/3 model with at least two output values.
```

Why bad:

```text
A constant operation on Fin 2 still has a two-element carrier, so it is non-singleton even if the operation output is constant.
```

Correct conservative criterion:

```text
If any satisfying model exists on Fin 2 or Fin 3, classify as non-singleton candidate.
Only classify as singleton-like when no satisfying nontrivial carrier model is found in the searched sizes.
```

For order-≤4 laws, ETP gives some support for finite-model based singleton detection: every law among the 4694 order-≤4 laws is either singleton-equivalent or has a non-trivial finite model, usually of size ≤5 with one size-7 exception. However, Stage 2 also includes order-5 laws, so this should remain a heuristic/routing signal, not a proof.

### 11.4 Minimum useful benchmark

Before implementing LLM strategist, create:

```text
non_singleton_true_eval.jsonl
```

Each row:

```json
{
  "id": "normal_...",
  "eq1_id": 123,
  "eq2_id": 456,
  "equation1": "...",
  "equation2": "...",
  "answer": true,
  "singleton_model_search": "found_nontrivial_model | no_model_found",
  "baseline_status": "unsolved | solved_direct | solved_graph | solved_singleton",
  "notes": "optional"
}
```

Start with `sample_200` and `normal`; then add hard sets.

---

## 12. Revised implementation order

### Phase 0: preserve existing deterministic solver

```text
- Keep false search.
- Keep direct h / two-step h / bounded graph.
- Keep existing singleton templates.
```

### Phase 1: integrate deterministic singleton completion

```text
- Port completion_engine_reference.py into solver.py or a copy-pasteable section.
- Ensure no external dependencies.
- Validate Python ptype checker.
- Validate emitted Lean on real judge.
- Add regression cases from sample_20.
```

### Phase 2: build/evaluate non-singleton completion floor

```text
- Reuse proof-traced normalizer.
- Add general self-overlaps.
- Add rule-rule overlaps.
- Add basic scoring and caps.
- Do not add LLM yet.
```

### Phase 3: build labeled non-singleton true residual

```text
- Run Phase 2 on public labeled sets.
- Extract TRUE_NON_SINGLETON_RESIDUAL.
- Inspect failure traces.
```

### Phase 4: add simple deterministic goal bias

```text
- Eq2 subterm bonuses.
- Waypoints derived deterministically from goal subterms.
- Dual mode if cheap.
```

### Phase 5: only then add LLM strategist

```text
- Strict JSON only.
- Seed terms and candidate substitutions.
- Eq2 waypoints.
- No raw Lean.
- No trusted verdicts.
```

### Phase 6: redundancy upgrades if search explosion is the bottleneck

```text
- J/subsumption-lite.
- connectedness-lite.
- ground-joinability-lite.
```

---

## 13. Success criteria

The revised strategy succeeds if:

```text
1. Singleton true cases are solved deterministically and accepted by Lean.
2. False-side reliability does not regress.
3. Non-singleton true residual is measured explicitly.
4. LLM guidance is adopted only if it gives unique solves on that residual.
```

The key research question is not:

```text
Can an LLM prove these equations?
```

It is:

```text
Can an LLM improve search control for non-singleton true completion problems beyond a strong deterministic baseline?
```

---

## 14. Source notes

### 14.1 Equational Theories Project

Used for:

```text
- Lean-verified implication/refutation graph
- importance of finite counterexamples
- linear/affine model families
- singleton-equivalent law structure
- duality
- caution that direct public-LLM proof generation was not the main winning tool
```

### 14.2 Twee

Used for:

```text
- R/Q/J completion architecture
- critical-pair generation
- normalization of the goal
- candidate scoring
- passive-set explosion risk
- proof objects for active rules
- redundancy hierarchy: joinability, ground joinability, connectedness, J/subsumption
- goal transformation / goal direction
```

### 14.3 Draft, Sketch, and Prove

Used for:

```text
- LLM as structure/sketch generator
- automated prover fills gaps
- formal verifier checks final proof
- ablation evidence that automated prover completion is essential
```

---

## 15. One-line summary

```text
Ship the deterministic singleton completion engine first; measure the non-singleton true residual; then test LLM-guided Q seeding and Eq2 waypoints only if that residual is large and search-shaped.
```
