# Residual-by-family analysis (PAPER_PLAN step 2)

Per `PAPER_PLAN.md` sequencing step 2: "tag every solve above the
finite-search rung by witness family + in/out-of-span, with a diversity
lens. Sizes the construction population and its scatter." This uses results
we already have (no new runs) to characterize what a steelman portfolio for
order-5 needs to cover.

## Data
`pipeline/results/merged_{hard1,hard2,hard3,normal}.json` — 1,667 rows total,
1,652 solved (99.1%) by the merged solver, each tagged with `solved_by` (the
stage that produced the accepted certificate) and `verdict`. Cross-referenced
against `scripts/my_solver_merged/solver.py` (the current, authoritative
stage list — some stages postdate this run; see caveats).

**Caveat on staleness**: `merged_hard1.json`/`merged_normal.json` are from
2026-06-20, `merged_hard2/3.json` from 2026-06-28. The `algebraic-linear
infinite model` stage (ℤ[α] companion-matrix, [[infinite-model-capability]])
and later SAT-finder/maxRecDepth fixes postdate parts of this snapshot — it
shows 0 solves for that stage here even though it's confirmed to solve
hard2_0051 via a standalone spike. Treat family *shapes* as reliable, exact
counts as a lower bound pending a fresh full re-run.

## The current deterministic FALSE-side portfolio (the C2 steelman draft)
In execution order, each gated on the previous stages failing:

| # | Family (`solved_by` label) | Method | Parameter range |
|---|---|---|---|
| 1 | exhaustive Fin 2-3 counterexample search | brute-force all magmas | Fin ≤3 (floor) |
| 2 | named witness tables | curated known counterexample magmas | lookup, no sweep |
| 3 | affine model search | symbolic a·x+b·y+c mod n | modulus up to n=40 |
| 4 | perturbed witness tables | single-cell perturbation of named tables | Fin {2,3,4} |
| 5 | structured Fin 4-7 counterexample search | heuristic structured families | Fin {4,5,6,7} |
| 6 | fast false-model probe | backtracking, quick pass | Fin {4,5}, 1.8s/size |
| 7 | backtracking model finder ("mf2") | 3-pass portfolio: backtrack+unit-prop, WalkSAT local search, Eq2-directed DFS+duality | Fin 4-7, 240s budget |
| 8 | SAT false-model finder | complete CDCL | Fin {5,6,7}, 120s budget |
| 9 | algebraic-linear infinite model | ℤ[α]≅ℤᵈ companion-matrix (infinite carrier) | degree-≥2 algebraic coefficients, no finite bound |

This is already a 9-family, deliberately layered portfolio spanning brute
force → curated/structured → symbolic algebraic → complete search →
infinite algebraic models. It is the direct basis for the "exact
search-space spec (families × parameter ranges)" C2 asks to publish.

## Empirical scatter (what actually fired, this snapshot)
FALSE-side solves only (848 of 1,652; the other 804 are TRUE-side proof
stages, now largely ATP-owned and not the paper's focus):

| Family | Count | % of FALSE solves |
|---|---|---|
| exhaustive Fin 2-3 (floor) | 697 | 82.2% |
| affine model search | 71 | 8.4% |
| backtracking model finder | 39 | 4.6% |
| fast false-model probe | 36 | 4.2% |
| SAT false-model finder | 3 | 0.4% |
| named witness tables | 2 | 0.2% |
| algebraic-linear infinite model | 0* | 0%* (*undercounted, see caveat) |

**Above-floor construction population**: 151/848 (17.8% of all FALSE solves,
9.1% of *all* 1,667 problems) needed something beyond brute-force Fin ≤3.
Of those 151: affine (47.0%), backtracking (25.8%), fast-probe (23.8%), SAT
(2.0%), named-witness (1.3%) — dominated by the top 2 families (72.8%
combined) but with a real tail of qualitatively different methods (symbolic
algebra, complete SAT search, curated tables). Moderate, not flat, diversity.

## Where the construction population concentrates
| Set | Rows | Above-floor FALSE solves | Rate |
|---|---|---|---|
| hard1 | 69 | 28 (affine 7, probe 9, backtrack 11, SAT 1) | 40.6% |
| hard2 | 200 | 75 (affine 39, probe 21, backtrack 13, SAT 2) | 37.5% |
| hard3 | 398 | 37 (affine 18, probe 6, backtrack 13, named 2) | 9.3% |
| normal | 1000 | 9 (affine 7, backtrack 2) | 0.9% |

hard1/hard2 (curated as "FALSE-heavy" / "mixed, algebraic-linear core") carry
almost all the interesting construction cases; `normal` (uncurated) is
overwhelmingly trivial. **This is the key actionable signal for order-5
sampling**: the order-≤4 hard sets got their yield from deliberate
difficulty stratification, not uniform sampling — exactly why the order-5
probe's uniform draw found only 1/250 hard cases ([[order5-yield-probe]]).
Mimicking whatever criteria produced hard1/hard2 (rather than sampling
eq_size5.txt uniformly) should raise the order-5 hard-yield well above 0.4%.

## Residual (unsolved in this snapshot)
15/1,667 (0.9%): hard2 × 6 (incl. hard2_0027, hard2_0051), hard3 × 7, normal
× 2. Per memory, most have since closed: hard2_0051 via the algebraic-linear
ℤ-module stage ([[infinite-model-capability]]), several more via the SAT
finder + maxRecDepth fix ([[sat-finder-closes-false-core]],
[[maxrecdepth-was-the-false-bottleneck]]). hard2_0027 remains the one case
still believed genuinely intractable (per [[etp-repo-findings]], its
transitive structure has no low-degree finite or affine witness).

## Takeaways for order-5 harness design
1. The steelman portfolio isn't hypothetical — it already exists as 9
   working families with concrete parameter ranges (table above); order-5
   work should extend these ranges rather than invent new ones from scratch.
2. Even within the resolved order-4 graph, ~9% of *all* problems (not just
   the curated hard set) needed above-floor construction — a real,
   moderately diverse population, not a fluke.
3. Sampling strategy matters far more than raw N: hard1/hard2's curation
   produced 37-41% above-floor rates vs `normal`'s 0.9% — the order-5 probe
   should copy that stratification logic instead of uniform sampling.
4. algebraic-linear (infinite ℤ-module) is the one family with zero
   confirmed hits in bulk runs but a known real solve (hard2_0051) — worth a
   fresh full re-run to get an honest count before finalizing the C2 spec.
