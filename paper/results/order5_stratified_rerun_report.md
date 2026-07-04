# Order-5 stratified rerun (2026-07-01, follow-up to the uniform probe)

Follow-up to [[order5-yield-probe]] and [[residual-family-analysis]]. That
analysis showed the order-≤4 hard sets (hard1/hard2) get their high
above-floor rate (37-41%) from curation, not uniform sampling (`normal`:
0.9%) — and that this gap explains why the first order-5 probe's uniform
draw found only 1/250 (0.4%) genuinely hard pairs. This run tests whether
*mimicking that curation logic* — pre-filtering out whatever the fixed
portfolio already resolves before spending ATP compute — raises the yield.

## Method
1. **Bigger pool**: 2,000 fresh order-5 candidate pairs (same sampler,
   `paper/scripts/sample_order5.py`, new seed), same rule as before (≥1 law
   id >4694).
2. **Cheap portfolio pre-filter** (new: `paper/scripts/cheap_false_screen.py`)
   — reuses the *actual production solver's* pure-Python FALSE-side stages
   directly from `scripts/my_solver_merged/solver.py` (no Lean judge, no
   subprocess): exhaustive Fin≤3, structured Fin4-7, symbolic affine mod≤40.
   These are stages 1/3/5 of the real 9-family portfolio catalogued in
   [[residual-family-analysis]]. Cost: ~80ms/pair, pure Python.
   Result: **815/2,000 (40.75%) survive** — the cheap filter alone screened
   out 59.25% of the pool for free, before any ATP call.
3. **Subsample 300** of the 815 survivors (seed-fixed) for the expensive
   Vampire pass, keeping this run the same scale as the original probe.
4. **Same Vampire protocol as before**: 2s casc + 2s fmb, then extend to 15s
   then 40s on whatever survives, to separate "genuinely hard" from
   "just needed more time."

## Result: yield roughly 3x the uniform baseline
At 2s: 285/300 (95.0%) ATP-proved TRUE, 7/300 (2.3%) fmb-refuted, 8/300
(2.7%) residual. (The 95% TRUE rate — far above the uniform sample's 42.4%
— is because this filter only removes FALSE-resolvable cases, so survivors
skew heavily TRUE; a future pass should add a symmetric cheap TRUE-side
filter too.)

Pushing the 8 residuals to 15s, then 40s both directions:
- **4/8 confirmed hard** — unresolved by Vampire in *either* direction even
  at 40s: `order5v2_0073`, `order5v2_1593`, `order5v2_0534`, `order5v2_0515`.
- 4/8 dissolved (resolved somewhere in the 6-40s window — real but not
  "hard" by the 40s bar used in the first probe).

**4/300 = 1.33% confirmed-hard, vs 1/250 = 0.4% in the uniform probe — a
~3.3x density improvement**, at the same total sample size and using the
exact same 40s confirmation bar.

## The 4 confirmed-hard pairs
```
order5v2_0073  eq1_id=35060 eq2_id=59999
  x = ((y◇z)◇((x◇z)◇z))◇x
  (x◇x)◇y = (x◇x)◇(x◇y)

order5v2_1593  eq1_id=27288 eq2_id=6742
  x = ((y◇z)◇(z◇x))◇(z◇y)
  x = y◇(x◇((z◇x)◇(w◇u)))

order5v2_0534  eq1_id=13849 eq2_id=7647
  x = y◇((y◇((x◇z)◇z))◇z)
  x = y◇(x◇((z◇(z◇z))◇z))

order5v2_0515  eq1_id=21866 eq2_id=53697
  x = (y◇(z◇x))◇(x◇(x◇w))
  x◇y = (((z◇w)◇y)◇y)◇x
```
All resist a 40s Vampire budget in both the prove and finite-model-build
directions — real candidates for the case-study material PAPER_PLAN asks for.

## Why this matters
The absolute yield increase (1→4 confirmed-hard cases at the same N=300)
plus the free 59% pre-filter rate together mean: for the same amount of
*expensive* ATP compute, stratified sampling surfaces proportionally more
hard cases than uniform sampling, and does so using only the deterministic
portfolio stages that already exist — no new infrastructure. Naively scaling
this to the full 815-survivor pool (not just the 300 subsample) would extrapolate
to roughly 11 confirmed-hard cases from this single 2,000-pair draw.

## Recommendation
This validates the harder claim underlying C1/C2: a real, non-trivial
order-5 hard-construction population exists, it is *findable more
efficiently* than uniform sampling suggests, and the existing deterministic
portfolio (already characterized in [[residual-family-analysis]]) is the
right free first filter to apply before spending ATP/LLM budget. Next
useful refinements, in priority order:
1. Add a symmetric cheap **TRUE-side** filter (quick template proof search)
   so survivors aren't overwhelmingly TRUE-skewed — should recover more
   confirmed-hard FALSE cases per unit compute.
2. Run the full 815-survivor pool (not just 300) through Vampire to get an
   exact count instead of an extrapolation.
3. Bring in the remaining 6 deterministic FALSE families (named/perturbed
   witness tables, backtracking mf2, SAT finder, algebraic-linear ℤ-module)
   as additional pre-filter stages — the current filter only used 3 of 9.

## Artifacts
- `paper/scripts/cheap_false_screen.py` — reusable cheap pre-filter.
- `paper/problems/order5_pool_v2.jsonl` (2,000), `order5_survivors.jsonl`
  (815), `order5_screened_out.jsonl` (1,185), `order5_stratified.jsonl`
  (300 subsample used for the Vampire pass).
- `paper/results/baselines_order5_stratified.jsonl`.
- This report.
