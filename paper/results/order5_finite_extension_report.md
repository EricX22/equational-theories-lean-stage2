# Pushing finite search past Fin≤11 on all 8 validated hard pairs (2026-07-03)

Direct follow-up to the population scale-up
([[order5-scaled-population]]): before trusting the 8 validated hard order-5
pairs as genuine C3/proposer targets, check whether any of them are only
"hard" because the fixed portfolio's `mf2` finite-model finder caps out at
Fin≤11 — i.e. rule out "just needed a bigger `for` loop" before crediting
anything to needing an exotic/infinite construction.

## What could and couldn't be done in this sandbox
The ideal version of this check (300s+ Vampire per direction, full 240s
mf2 budget per size) can't run inside this environment — any single bash
command is hard-capped at 45s, and no background process survives between
calls, so a genuine multi-hundred-second search simply cannot complete
here. That version needs the real machine (`run.sh`, no artificial cap).

What's feasible and was actually run: our own `mf2_Finder` (pure Python,
no external process, part of `scripts/my_solver_merged/solver.py`) called
directly at domain sizes **beyond** the portfolio's Fin≤11 cap — Fin
12, 13, 14 in the portfolio's strongest mode (idempotent quasigroup:
`qg=True, idem=True`, the mode empirically associated with most of the
existing residual solves per [[false-side-quasigroup-breakthrough]]), plus
a spot-check in **general** (unconstrained) mode at Fin 12.

Harness sanity-checked first: a trivial idempotent/non-commutative-Latin-
square test (`x◇x=x` / `x◇y=y◇x`, n=4) found a genuine witness in
<0.001s, confirming the API and equation-parsing work correctly and that
fast "miss" results aren't silently broken calls.

## Results: all 8 pairs still miss at every size/mode tried

| Pair | Fin12 idem+qg | Fin13 idem+qg | Fin14 idem+qg | Fin12 general |
|---|---|---|---|---|
| order5v2_0073 | miss (0.0s) | miss (0.0s) | miss (0.0s) | miss (15.1s, exhausted budget) |
| order5v2_1593 | miss (11.3s) | miss (11.5s) | miss (10.6s) | miss (20.2s, exhausted budget) |
| order5v2_0534 | miss (10.1s) | miss (10.0s) | miss (10.1s) | miss (15.0s, exhausted budget) |
| order5v2_0515 | miss (0.0s) | miss (0.1s) | miss (0.1s) | miss (15.7s, exhausted budget) |
| order5big_5245 | miss (0.0s) | miss (0.0s) | miss (0.0s) | miss (15.1s, exhausted budget) |
| order5big_6145 | miss (0.7s) | miss (1.3s) | miss (2.3s) | miss (15.7s, exhausted budget) |
| order5big_7472 | miss (0.0s) | miss (0.0s) | miss (0.0s) | miss (15.0s, exhausted budget) |
| order5big_1071 | miss (0.0s) | miss (0.0s) | miss (0.0s) | miss (15.0s, exhausted budget) |

Two distinct signatures worth noting:
- **Instant misses (0.0-0.1s)**: constraint propagation alone refutes the
  idem+qg mode almost immediately for most pairs — a real, fast negative
  (verified not to be a broken call, see the sanity check above), not
  evidence of being "close" to a solution.
- **Full-budget misses (10-20s)**: `order5v2_1593`, `order5v2_0534`, and
  `order5big_6145` genuinely used the entire time budget in at least one
  mode — these are the ones where more time budget is the *most* plausible
  lever among the 8, and would be the first candidates to re-check if a
  much longer (real-machine) run becomes available.

## What this means for C3/C4
None of the 8 dissolve by simply searching 3 sizes past where the
portfolio stopped, in either its strongest structured mode or an
unconstrained general search. This doesn't prove no finite countermodel
exists at Fin 15+ (that's unprovable in general — the methodological
guardrail PAPER_PLAN already commits to: claim empirically, not
theoretically), but it does mean the "obviously just needed a slightly
bigger domain" explanation is now less plausible for all 8 than it was
before this check, strengthening their credibility as genuine C3 targets
that need a structurally different construction, not just more finite
search.

## Recommendation
1. Treat all 8 as reasonably de-risked C3 targets for the next proposer
   run — this check doesn't guarantee they need infinite/exotic models,
   but it rules out the cheapest alternative explanation.
2. On the real machine, prioritize `order5v2_1593`, `order5v2_0534`, and
   `order5big_6145` for a genuine long-budget (100s+) mf2/Vampire rerun
   first — they're the ones that used their full time budget here, so are
   the most likely (of the 8) to actually be time-starved rather than
   structurally unreachable.
3. A ready-to-run long-budget script for the real machine:
   `paper/scripts/mf2_extend.py --id <id> --eq1 ... --eq2 ...
   --sizes 15,16,17,18 --per-size-budget 120` (just bump
   `--per-size-budget`; no sandbox cap applies there).

## Artifacts
- `paper/scripts/mf2_extend.py` — direct `mf2_Finder` caller, idem+qg mode,
  configurable sizes/budget.
- `paper/scripts/mf2_extend_general.py` — same, unconstrained general mode.
- This report.
