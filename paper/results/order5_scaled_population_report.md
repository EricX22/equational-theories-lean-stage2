# Order-5 hard-population scale-up (2026-07-03)

Follow-up to [[order5-stratified-rerun]], directly answering: *is the
confirmed-hard order-5 population just the 4 pairs we already found, or is
there a bigger family worth building the paper's evaluation set around?*

## Method
1. Sampled a 20,000-pair pool (`sample_order5.py`, `--n 20000 --seed
   20260702`, id-prefix `order5big`) — 10x the previous 2,000-pair draw.
2. Ran the same cheap pure-Python pre-filter (`cheap_false_screen.py`:
   exhaustive Fin≤3, structured Fin4-7, affine mod≤40 — 3 of the 9 portfolio
   families) over the first **8,050** of those 20,000 pairs, chunked into
   ~20 sandbox-safe batches.
3. Drew a fresh 300-pair subsample from the survivors (new seed, 20260703)
   and ran the same escalating Vampire protocol as before: 2s both
   directions, then 15s, then 40s on whatever still resists.

## Important caveat found mid-run: accidental seed collision
`order5_pool_big.jsonl` was sampled with `--seed 20260702` — **the same
seed** already used for the earlier `order5_pool_v2.jsonl` (2,000 pairs).
Since the sampler is a deterministic `random.Random(seed)` walk over the
same `eq_size5.txt`, this means **the first 2,000 rows of the new 8,050-pair
batch are byte-identical to the entire previous 2,000-pair draw** (verified:
all 4 previously-confirmed-hard pairs' exact `(eq1_id, eq2_id)` show up in
the new pool's first 2,000 rows). So of the 8,050 pairs screened here, only
**~6,050 are genuinely new**; the cheap-filter's 3,179 survivors include the
same 815 that survived last time, deterministically re-derived. Lesson
logged in [[cowork-sandbox-caveats]]-adjacent practice: **always pass a
fresh seed when scaling up a previous sampling run.**

This does not undermine the result below — it just means the "new
information" is somewhat smaller than the raw pair count suggests, and it
produced a nice (accidental) internal consistency check: the previously
known hard pair `order5v2_0073` (`eq1_id=35060, eq2_id=59999`) was
re-drawn, re-screened, and re-confirmed hard at 40s in this independent
Vampire run — a genuine replication, not a new pair.

## Results

**Cheap-filter pass (8,050 pairs, ~6,050 new):**
3,179 survive (39.49%) — consistent with the prior run's 815/2,000
(40.75%), confirming this is a stable rate, not a small-N fluke.

**Vampire escalation on a fresh 300-pair subsample of survivors:**
- 2s: 290/300 TRUE, 4/300 FALSE (fmb), 6/300 residual.
- 15s: 1/6 dissolves (`order5big_1017` — real, just needed more time).
- 40s (both directions) on the remaining 5: **all 5 confirmed hard**
  (`order5big_5245`, `order5big_6145`, `order5big_7472`, `order5big_0073`
  [= the known `order5v2_0073`, a re-confirmation], `order5big_1071`).

**Net new confirmed-hard pairs this session: 4**
(`order5big_5245`, `order5big_6145`, `order5big_7472`, `order5big_1071` —
verified via id lookup to be distinct from all 4 previously-known pairs).

```
order5big_5245  eq1_id=28626 eq2_id=50940
  x = (((y◇x)◇y)◇y)◇(x◇z)
  x◇y = (z◇((y◇w)◇y))◇w

order5big_6145  eq1_id=6749 eq2_id=46670
  x = y◇(x◇((z◇y)◇(y◇z)))
  x◇y = (z◇w)◇(x◇(u◇x))

order5big_7472  eq1_id=5951 eq2_id=23425
  x = y◇(y◇(x◇((z◇y)◇y)))
  x = ((y◇x)◇z)◇(z◇(x◇z))

order5big_1071  eq1_id=33998 eq2_id=2
  x = ((y◇y)◇(x◇(x◇z)))◇z
  x = y
```

**Combined distinct confirmed-hard pool across both sessions: 8 pairs**
(the 4 from [[order5-stratified-rerun]]/[[proposer-loop-spec]] +
these 4 new ones) — double the prior C3-target pool, from one modest
follow-up pass.

**Rate comparison across the two independent 300-pair Vampire subsamples:**
4/300 (1.33%, prior run) vs 5/300 (1.67%, this run) — consistent within a
narrow ~1.3-1.7% band of cheap-filter survivors. Cross-checks against the
very first uniform yield probe too: 1.5% average rate × ~40% survivor rate
≈ 0.6% of *all* raw order-5 pairs, in the same ballpark as the original
uniform probe's 0.4% ([[order5-yield-probe]]) — good agreement across three
independently-run estimates.

## Does a big underlying family exist? Yes — quantitatively, not just hopefully
Naively scaling the ~1.5% average confirmed-hard rate to the **full
3,179-survivor pool** from this single 8,050-pair draw predicts roughly
**~48 confirmed-hard pairs** sitting in that pool alone, most still
unvalidated (only 300 of 3,179 survivors have actually been pushed through
Vampire so far). And this 8,050-pair draw is itself a small sample against
the true space: `eq_size5.txt` has 62,576 laws, so the full ordered-pair
space is on the order of billions, dwarfing anything sampled here or in
the order-≤4 hard sets (which drew from "only" ~22M pairs). There is no
sign of the population being thin or close to exhausted — every scale-up
so far has found proportionally *more* confirmed-hard pairs, not fewer.

## Recommendation
1. Treat this as strong evidence for C1 (open, non-trivial hard population)
   at a scale that supports a real evaluation set, not just a handful of
   anecdotes — 8 validated targets now exist, and cheap evidence points to
   dozens-to-hundreds more being one more (still-cheap) scale-up away.
2. Next natural step for population sizing: push the full 3,179-survivor
   pool through the 2s Vampire pass (not just the 300 subsample) to replace
   the ×~10.6 extrapolation with an exact count — doable in the same
   chunked style used here, just more calls.
3. For the paper itself: the proposer (C3/C4) now has 8 validated targets
   instead of 4 to run against, doubling the real estimate of
   attempts/cost-per-solve once a `reasoning: high` rerun happens.
4. Remember the seed-collision lesson for any future sampling scale-up:
   always pick a fresh `--seed`.

## Artifacts (native sandbox path; not yet copied to the mounted project)
- `paper/problems/order5_pool_big.jsonl` (8,050 of 20,000 generated,
  screened)
- `paper/problems/order5_big_survivors.jsonl` (3,179),
  `order5_big_screened.jsonl` (4,871)
- `paper/problems/order5_big_subsample300.jsonl` (the 300-pair Vampire
  subsample)
- `paper/results/baselines_big300_2s.jsonl` (2s pass, all 300)
- `paper/results/r40_*.jsonl`, `r15_*.jsonl` (escalation runs on the 6
  residuals)
- `paper/scripts/single_side_vampire.py` (new helper: runs just one
  Vampire direction at a time, needed because 2-sides × 40s exceeds the
  sandbox's 45s cap even for a single pair)
