# Solved-by-Matrix Experiment Spec (AAAI paper)

Goal: produce the central result of the paper — a per-problem matrix showing
that our neuro-symbolic system (LLM proposes waypoints, bounded narrowing
verifies, Lean checks) solves equational-implication instances that **no
classical autosolver in the portfolio closes**, and that those instances are
precisely the *direction-bound* residual.

Headline claim to support: *"Of the N instances unsolved by the virtual best
solver of {Vampire, E, Prover9, Mace4} and by our own LLM-off pipeline, the
LLM-augmented system closes M, each with a machine-checked Lean proof."*

---

## 1. Problem set (which ETP subset)

Pivot off the competition harness and onto the **original ETP implication
graph**, but evaluate on a principled, reproducible residual rather than the
full ~22M ordered pairs (4694 laws²), almost all of which are trivial.

Three tiers, all already present in `examples/problems/`:

| Set            | Count | Character                                   |
|----------------|-------|---------------------------------------------|
| `hard1.jsonl`  | 69    | FALSE-heavy (counterexample / model side)   |
| `hard2.jsonl`  | 200   | mixed; algebraic-linear FALSE core lives here |
| `hard3.jsonl`  | 400   | TRUE-heavy, direction-bound (the LLM target) |
| `true_misses_18.jsonl` | 18 | TRUE residual our no-LLM pipeline still fails |

Each row already carries everything the encoder needs:
`{id, eq1_id, eq2_id, equation1, equation2, answer}` with terms written over a
single binary op `◇` and variables `x,y,z`.

Reproducibility / citability: map every `eq1_id`/`eq2_id` back to the canonical
numbering in `reference/equational_theories/data/equations.txt` so the subset is
defined against the published ETP artifact, not our internal files. Document the
filter that produced hard1/2/3 (difficulty stratification over the ETP graph)
so a reviewer can regenerate it.

### Contamination control (do this from day one — it is the paper's biggest review risk)
The ETP Lean proofs and `equations.txt` are public and almost certainly in the
LLM's training data (`reference/equational_theories/` is literally that repo).
Mitigations, in order of strength:
1. **Held-out laws**: evaluate (also) on freshly generated law pairs not present
   in the public ETP merge, so the model cannot have memorized a chain.
2. **Recall probe**: ask the LLM for the implication/proof *without* the
   verifier; measure how often it reproduces a known ETP chain verbatim. Report
   this as the contamination baseline.
3. **Reasoning vs retrieval**: show waypoint chains the verifier accepts that do
   **not** match any chain in the ETP commentary/blueprint.

---

## 2. TPTP encoding for the ATP baselines

One small encoder, `scripts/paper/build_tptp.py`, turns each jsonl row into ATP
input. The term grammar is trivial (fully-parenthesized binary `◇`, vars
`x/y/z`), so a recursive-descent parser → `f(.,.)` suffices.

Mapping: `◇` → function symbol `f/2`; `x,y,z` → TPTP variables `X,Y,Z`; an
equation `lhs = rhs` → universally quantified equality over its free vars.

**TRUE direction (prove the implication)** — emit `<id>_true.p`:
```
fof(hyp,  axiom,      ![X,Y,Z]: ( eq1_lhs = eq1_rhs )).
fof(goal, conjecture, ![X,Y,Z]: ( eq2_lhs = eq2_rhs )).
```
Run Vampire / E / Prover9. SZS `Theorem`/`Unsatisfiable` ⇒ proved TRUE.

**FALSE direction (find a counterexample magma)** — emit `<id>_false.p`:
```
fof(hyp, axiom,            ![X,Y,Z]: ( eq1_lhs = eq1_rhs )).
fof(neg, negated_conjecture, ?[A,B,C]: ( eq2_lhs != eq2_rhs )).  % eq2 fails somewhere
```
Run Mace4 and Vampire `--mode fmb` (finite model builder). SZS `Satisfiable` /
a returned model ⇒ FALSE, and the model *is* the counterexample table.

Fairness rules (a weak baseline sinks the paper):
- Latest stable versions; record version strings in the output.
- Same wall-clock budget per problem as our solver (3600 s — generous to the ATPs).
- Sane default + one tuned config each (e.g. Vampire `--mode casc`, E `--auto`,
  Mace4 domain sweep to size matching our finder, ~Fin 2–11).
- Log the exact command line per run.

---

## 3. Attribution logging (already 80% there)

Our proxy records `solved_by`, `used_llm`, `llm_calls`, `judge_calls` per row
(`pipeline/proxy.py:1118`, surfaced by `scripts/llm_report.py`). LLM stages are
tagged `LLM waypoint narrowing`, `LLM direct proof`, `LLM strategist singleton
graph`, `LLM fallback`. To make attribution trustworthy for the matrix:

- **Two runs of our system**: `ENABLE_LLM=False` and `ENABLE_LLM=True`. The
  solved-set diff is, by construction, the LLM's marginal contribution (see the
  comment at `solver.py:101`).
- **Every claimed solve must pass the Lean judge.** Persist the accepted cert +
  judge verdict per row so "solved" means "machine-checked," not "solver said so."
  This is the soundness guarantee that differentiates us from LLM-writes-proofs work.
- For LLM-solved rows, dump the **waypoint chain** (proposed bridge terms + the
  per-hop narrowing certificate) for the case-study section.

---

## 4. Scripts to build (new dir `scripts/paper/`)

1. `build_tptp.py` — jsonl → `{id}_true.p` / `{id}_false.p`.
2. `run_baselines.py` — invoke vampire / eprover / prover9 / mace4 with timeout,
   parse SZS status, write `baselines.jsonl` (id, tool, side, status, time, cmd).
3. `run_ours.py` — run `my_solver_merged/solver.py` twice (LLM off/on) over each
   set; we already emit the rich result JSON.
4. `build_matrix.py` — join all of the above into `solved_by_matrix.csv`:
   `id, eq1_id, eq2_id, gold, vampire, E, prover9, mace4, classical_vbs,
    ours_nollm, ours_llm, ours_solved_by, ours_used_llm, judge_ok,
    time_vampire,…,time_ours`.
5. `analyze.py` — compute the tables/figures in §5; emit the uniquely-solved set
   and dump its waypoint chains.

`classical_vbs` = OR over the four classical tools. **Uniquely-solved-by-us** =
`ours_llm ∧ ¬classical_vbs ∧ ¬ours_nollm ∧ judge_ok`. That column is the result.

---

## 5. Tables & figures for the paper

- **Table 1 — coverage** by method on hard1/hard2/hard3 + aggregate.
- **Table 2 — uniquely solved vs classical VBS** (the money table): count and
  list of instances closed only by the LLM-augmented system.
- **Table 3 — ablation**: ENABLE_LLM off vs on; `solved_by` stage distribution;
  judge validity rate (should be 100%); LLM call/judge-call counts.
- **Figure — two frontiers**: FALSE residual shrinks with compute (time/Fin
  sweep) while TRUE residual is flat in compute but moves with LLM waypoints —
  the empirical core of the "direction-bound vs compute-bound" thesis.
- **Case studies (2–3)**: full LLM waypoint chains for uniquely-solved TRUE
  instances, each with its verified per-hop narrowing certificate.

Target: even M ≈ 10–20 uniquely-solved, characterizable instances is a result,
provided each survives the VBS bar and the contamination control.

---

## 6. Sequencing (gating before any of this is worth running)

1. Improve the waypoint stage until it produces real, judge-verified solves on
   the TRUE residual (currently `judge_calls`/bridges ≈ 0 — no result yet).
2. Stand up `build_tptp.py` + `run_baselines.py`; get the classical VBS column.
3. Run the matrix; inspect the uniquely-solved set.
4. Build the contamination control; confirm the unique solves aren't recall.

Step 1 is the gate — everything downstream is moot until M is real and nonzero.
