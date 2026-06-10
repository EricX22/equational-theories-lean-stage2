# Equational Theories Solver — State of the Union

_Last updated: 2026-06-10. Single-file solver at `scripts/my_solver/solver.py` (~3,010 lines, self-contained, pure Python, no network/z3 in the shipped path)._

## 0. 2026-06-10 session — false-side breakthrough (needs judge re-measurement)

Two new deterministic false-side stages were added and validated in Python replay
(table verification is judge-equivalent for false certs):

- **Stage 1.3 — symbolic affine models (`af_` namespace).** op = (a·x+b·y+c) mod n,
  with Eq1/Eq2 checked symbolically per (n,a,b) and c SOLVED (the constant term is
  linear in c). Reaches any modulus in microseconds — e.g. `hard2_0051` falls to
  Z13 with op=7x+7y, `hard2_0096` to Z9 op=6x+y+1, `hard1_0017` to Z7 op=2x+6y.
  The ETP paper's "linear models" family, done as algebra instead of search.
- **Stage 2.9 first pass — domain-propagation finder portfolio (`mf2_` namespace).**
  SEM/Mace4-style: bitmask domains per cell, set-valued bottom-up evaluation of Eq1
  ground instances (union over arg combos — sound over-approximation), unit
  assign/prune, MRV branching, least-number symmetry breaking via the
  designated-elements rule, and **quasigroup/Latin modes** (alldifferent row/col
  pruning, optional idempotent diagonal). Weighted (mode,size) schedule up to Fin 9,
  60s budget. KEY EMPIRICAL FINDING: nearly all hard2/hard1 residual counterexamples
  are (idempotent) quasigroups — with alldiff+idem the search needs only ~6-15 NODES
  even at Fin 8, where the old finders never reached past Fin 7.

**Replay results on the known false residuals** (Python-verified, real judge pending):

| Benchmark | Before | After | Notes |
|---|---|---|---|
| hard2 finder-miss set (34 IDs incl. `hard2_0002`) | 0/34 | **30/34** | 28 via mf2 portfolio (2 Fin4, 16 Fin5, 1 Fin6, 1 Fin7, 6 Fin8 + 2 recovered), 2 via affine (Z13, Z9) |
| hard1 cascade residual (6 IDs) | 0/6 | **5/6** | 4 via mf2 (Fin 7-8), 1 via affine (Z7) |

Expected coverage if judge confirms: hard2 79.5% → ~91%, hard1 78.3% → ~85.5%.
Remaining genuinely-hard false core (5 IDs): `hard2_0027/0093/0124/0125`,
`hard1_0009` — z3-sat at Fin 6 (or unknown ≤7) but non-Latin, non-affine; these
need conflict learning (real CDCL) or much larger budgets.

Also added: model-finder candidates are now self-verified in Python before being
sent to the judge (drops any buggy table before it costs a judge call).

**TODO next session:** re-run hard1/hard2/normal/hard3 under the real judge to
confirm; consider per-problem time scaling (solo budget allows far more than 60s);
the 5-ID hard core wants nogood learning.

## 1. Snapshot

| Problem set | Solved | Wrong | Solver version measured |
|---|---|---|---|
| normal (1000) | **97.2%** (972) | 0 | current engine |
| hard1 (69) | **78.3%** (54) | 0 | current engine |
| hard2 (200) | **79.5%** (159) | 0 | current engine |
| hard3 (400) | **89.8%** (359) | 0 | current engine |

**Zero wrong answers anywhere** — structural, not luck: every accepted output is checked by the Lean judge (proofs type-checked, counterexample tables run through `decideFin!`). The only failure mode is *missing* (gave up / certificate rejected), never *wrong*. The real metric is coverage.

> All four sets have now been measured on the current engine. The WalkSAT pass added +3 on normal (96.9%→97.2%, all false-side); hard1/hard2/hard3 were unchanged — their remaining false cases are the genuinely-hard Fin 6+ kind that WalkSAT also misses.

## 2. What's implemented — the stage pipeline

The solver tries cheap/deterministic stages first and only reaches the LLM as a last resort. Stages added this session are marked **[new]**.

**False side (find a finite magma satisfying Eq1, violating Eq2 → table judged by `decideFin!`):**
- Exhaustive Fin 2-3 enumeration
- Named witness tables (projections, constants, cyclic, Z4, …)
- One/two-cell perturbations of structured tables
- Structured Fin 4-7 families
- **[new] Stage 2.9 — backtracking finite-model finder**: unit-propagates Eq1 over the partial op-table, branches on undetermined cells (reliable for Fin 4); then a **WalkSAT / min-conflicts local search** for the harder Fin 5-7 models the DFS can't find. Placed *after* the true-proof stages so true cases mostly resolve first.
- **[new] Stage 2.9c — Eq2-directed finder + duality**: third pass inside `try_model_finder`. Forces the Eq2 violation up front (posts `eval(Eq2.lhs)=u` as a ground constraint for each Eq2 assignment/target), then completes Eq1 by unit-propagation DFS under the **least-number heuristic** (introduce value k+1 only after k appears — cuts carrier-relabeling duplicates). Each size is also tried on the **dual** (operands swapped) and transposed back. **Real-judge result: no net improvement on hard2** — the +5 it found in a standalone finder-only replay (`hard2_0016/0181/0192` Fin 6, `hard2_0068/0092` Fin 5) were already solved upstream by the named/structured/perturbed stages, so end-to-end coverage is unchanged. Kept in the pipeline (0 wrong, low cost) but it is not the lever for hard2's residual. `hard2_0002` (z3-only Fin 5) still resists.

**True side (prove Eq1 ⇒ Eq2 in Lean):**
- Direct `h` instantiation; two-step `h` chain
- Bounded equality graph (Eq2.lhs → Eq2.rhs); singleton equality graph
- Generic tactic battery (rw/simp/…)
- Trivial + structural singleton templates
- **[new] Stage 2.7 — singleton completion (Phase 1)**: proof-carrying ordered Knuth-Bendix completion. When Eq1 forces `∀ p q, p = q`, derives it mechanically and emits a `kc_ptype`-checked Lean proof.
- **[new] Stage 2.8 — non-singleton completion (Phase 2)**: same engine pointed at proving `goal_lhs = goal_rhs` directly (normalize both sides to a common form).

**LLM:**
- Singleton strategist path: kept.
- **[new]** Non-singleton proof fallback: **gated off** (`ENABLE_NS_LLM_FALLBACK = False`). It returned unusable output, solved ~0, and cost 20-340s/case (one case burned 337s). Reversible via the flag.

**Infrastructure:**
- **[new]** `runner.py` hardened: tolerates a corrupt/empty results file at startup and writes results atomically (an interrupted run previously zeroed the file and crashed the next run).

## 3. Per-set residual, broken down true vs false

| Set | Unsolved | gold-TRUE | gold-FALSE | Dominant gap |
|---|---|---|---|---|
| normal | 28 | 24 | 4 | true (hard non-singleton) |
| hard1 | 15 | 6 | 9 | mixed |
| hard2 | 41 | 15 | 26 | false (hard Fin 6+/awkward) |
| hard3 | 41 | 39 | 2 | true (hard non-singleton) |

The residual composition flips by set: the hard-TRUE frontier dominates normal and especially hard3; the hard-FALSE cases dominate hard2.

## 4. What we're missing, by type

**TRUE residual — hard non-singleton implications.**
Eq2 genuinely follows from Eq1 but *without* a singleton collapse, and ordered completion *saturates* (reaches a complete system) without the goal's two sides joining. Confirmed not false (z3 finds no counterexample up to Fin 6-7) and not budget-limited (saturation point is identical at cap 22 vs 34). Many are "variable-shuffling" laws (e.g. `x◇y = (z◇z)◇(x◇x)`, where the two sides don't share variables) that LPO can't orient. Solving these needs a *change of search direction*, not more compute — i.e. goal-directed search or LLM waypoints (Phase 4/5).

**FALSE residual — counterexamples beyond the finder's reach.**
The DFS finder gets Fin 4 reliably; WalkSAT recovered most Fin 5. What remains needs Fin 6+ or awkward Fin-5 landscapes where even local search struggles (e.g. hard2_0002 has a z3-confirmed Fin-5 model that neither DFS nor WalkSAT finds). z3 finds these easily, but z3 can't ship (pure-Python constraint), so matching it would mean reimplementing a real CSP/SAT solver in Python. The Eq2-directed + duality finder (Stage 2.9c) was tried against exactly this residual and added **0 net solves on hard2** under the real judge — directed enumeration with the least-number heuristic is not enough; the genuine residual (incl. hard2_0002) appears to need conflict-driven propagation (CDCL-style learning), not smarter brute enumeration.

## 5. What we tried

**Shipped (all judge-validated, 0 wrong):**
- Phase 1 singleton completion → normal 93.8% → integrated; validated 20/20 on sample_20.
- Phase 2 non-singleton completion → normal to 96.9% (+26 direct solves).
- LLM curb (4→1 attempts) then fast-fail (→0) → cut LLM time ~80%, killed 100-340s waits.
- Backtracking model finder → hard1 50.7%→78.3% (+19).
- WalkSAT local-search pass → hard2 70.5%→79.5% (model finder 33→51, +18 false solves).
- runner.py robustness fixes.
- Eq2-directed finder + duality (Stage 2.9c) → +5 in a finder-only standalone replay, but **0 net on the full hard2 pipeline under the real judge** (those 5 were already solved upstream). Shipped anyway (0 wrong, cheap), but hard2's false residual needs a stronger lever, not this.

**Investigated, not shipped:**
- **Phase 4 goal-directed search** (for the true residual). Decision-only search finds paths for ~part of the residual, but the *proof-carrying* version is low-yield in tractable form: a valid Lean proof needs the search to reach `goal_rhs` *exactly* (the decision prototype counted alpha-equivalent matches, which overcounted ~6/10), and the higher-coverage "fresh variable" config hits the documented rename cycle (a lemma var binding to a term containing itself). The safe config produced one verified-valid proof (hard3_0376) but missed most of the sampled residual. This is the genuine research frontier.
- **z3 / SMT** — used only as a dev-time oracle (sizing counterexamples, confirming true/false). Cannot ship.

## 6. What's next (options, roughly by value-to-effort)

1. **Re-run normal/hard1/hard3 on the current engine** — cheap; gets honest updated baselines with WalkSAT + fast-fail (should lift the false residual on those sets).
2. **Push the model finder further** — Fin 7-8, smarter cell/value ordering (MRV), targeted Eq2-violation. Helps the hard2-style false residual; diminishing returns on the most awkward cases.
3. **Phase 4 done properly** — per-step fresh namespacing for the fresh config, then measure real yield. Highest potential on the true residual (hard3's 39, normal's 24) but uncertain payoff and real effort — the research frontier.
4. **Earlier "likely-false" gate** — skip the generic-tactic battery + completion on cases that look false, not just the LLM. Pure speed; the fast-fail already handled the worst (the LLM call).

## 7. Properties worth remembering

- **Correctness is outsourced to Lean.** Search can be as heuristic/stochastic as we like with zero risk of a wrong answer — the downside of a bad heuristic is only wasted time.
- **Single self-contained `solver.py`, pure Python.** No network, no z3/SMT, no sibling imports. The folder must contain only `solver.py` for deployment.
- **Everything deterministic-first.** The LLM is now essentially unused; the competitive edge is the in-process completion + model-finding engine.
