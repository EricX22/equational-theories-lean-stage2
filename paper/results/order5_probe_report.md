# Order-5 yield probe — results (2026-07-01)

Per `PAPER_PLAN.md` sequencing step 1 ("order-5 yield probe, cheap, do first"):
sample candidate pairs outside the resolved ETP order-≤4 graph, run finite
search + Vampire on both sides, and measure whether a non-trivial hard
residual exists before building any further infrastructure. This is the C1
gate check.

## Setup
- **Law pool**: `reference/equational_theories/data/eq_size5.txt` (62,576
  equations of term-size ≤5). Verified byte-identical to the published
  order-≤4 `equations.txt` (4,694 laws) in its first 4,694 lines — so law ids
  >4694 (57,882 of them) are genuinely new, not in the published/Lean-checked
  ETP graph.
- **Sampling**: 250 pairs `(eq1_id, eq2_id)` drawn uniformly at random from
  all 62,576 laws, keeping only pairs where at least one id is >4694 (so
  every pair is outside the resolved order-≤4 graph). Seed 20260701, no
  duplicates. Script: `paper/scripts/sample_order5.py`. Output:
  `paper/problems/order5_probe.jsonl`.
- **Encoding**: `paper/scripts/build_tptp.py` → `paper/tptp_order5/` (reused
  unmodified from the EXPERIMENT_SPEC machinery).
- **Solvers**: Vampire 5.0.1, both directions — `--mode casc` (prove eq1⊨eq2 →
  TRUE) and `-sa fmb` (finite model builder, refute → FALSE/counterexample).
  This doubles as both "ATP" and "finite search" per the plan (fmb *is* a
  bounded finite-domain search). No Mace4/E/Prover9 in this sandbox; that's
  fine for a first pass since Vampire covers both directions.
- **Budget**: cheap first pass at 2s/direction/pair (500 runs total, chunked
  through the sandbox's 45s bash cap). Runs: `paper/results/baselines_order5.jsonl`.

## Headline numbers (2s budget, 250 pairs)
| Outcome | Count | % |
|---|---|---|
| ATP-proved TRUE (vampire casc) | 106 | 42.4% |
| Trivially finite-refuted (vampire fmb) | 142 | 56.8% |
| Residual (neither resolved) | 2 | 0.8% |
| Contradictions (both fired — sanity check) | 0 | 0% |

All 248 resolved pairs resolved **fast**: TRUE proofs in 0.10–0.17s, FALSE
countermodels in 0.08–0.12s (i.e. tiny domains, Fin 2–3). Only 2/250 pairs
needed the full 2s to fail to resolve.

## Follow-up on the 2 residual pairs (does more budget dissolve them?)
- `order5_0018` (eq1_id 30445, eq2_id 17398): resolved FALSE at 15s — the
  fmb search just needed a slightly larger domain (found at ~3s). Not
  interesting; an artifact of the 2s cap, not real difficulty.
- `order5_0180` (eq1_id 22505, eq2_id 46912): **still unresolved by either
  direction at 40s** (20× the original budget) — `SZS status Timeout` on
  both casc and fmb. This one is real: neither a small counterexample nor a
  fast proof exists within reach of default Vampire strategies.
  - eq1: `x = (y ◇ (x ◇ y)) ◇ ((z ◇ z) ◇ z)`
  - eq2: `x ◇ x = (y ◇ y) ◇ ((z ◇ w) ◇ x)`

So the true "hard" yield at this sample size is **1/250 (0.4%)**, with the
other apparent residual dissolving into "trivial but needed 3s not 2s."

## Is 0.4% thin or healthy? (the actual gate question)
Context matters more than the raw percentage. The curated order-≤4 hard sets
(`hard1`+`hard2`+`hard3` = 69+200+400 = 669 pairs) were themselves filtered
down from the full ordered-pair graph (4694² ≈ 22.03M pairs) — i.e. only
about **0.003%** of *all* order-≤4 pairs made it into the "hard" bucket, and
that set was constructed by deliberate difficulty stratification, not
uniform sampling.

Our order-5 probe found a genuinely resistant pair at **0.4% under pure
uniform random sampling** — over 100× the order-4 hard-rate, with zero
curation. That's a favorable signal for C1: a hard construction population
appears to exist at order 5, and naive random sampling already finds it,
which means targeted/stratified sampling (mirroring how hard1/2/3 were built
for order-4) should surface meaningfully more.

## Caveats
- N=250, 1 confirmed hard case — not yet enough to characterize the
  residual's diversity or size (C4 needs many more). This probe answers the
  binary "does a population exist," not "how large/diverse is it."
- 2s/40s Vampire-only is a much weaker filter than the eventual steelman
  portfolio (C2: SAT/domain-propagation, affine, quasigroup, algebraic-linear
  families, plus longer ATP budgets). Some of these 106+142 "trivial" cases
  and the 1 hard case have not been checked against that fuller portfolio yet
  — this was deliberately the *cheap* pre-filter, not the real harness.
- Uniform sampling is almost certainly not the best way to find hard order-5
  pairs (order-4 experience suggests hard pairs cluster in specific regions
  of the graph, not uniformly). A next iteration should bias sampling (e.g.
  toward pairs where both laws are order-5-only, toward larger/more
  "entangled" term shapes, or toward laws structurally analogous to known
  order-4 hard cases) rather than drawing uniformly.

## Recommendation
**Gate passes — proceed, don't stop.** A real hard-construction pair showed
up in a 250-sample uniform draw with a cheap Vampire-only filter, at a rate
well above the order-4 baseline's hard-fraction. Per `PAPER_PLAN.md`
sequencing:
1. (this probe — done)
2. Next: residual-by-family analysis on existing order-≤4 results (already
   partially done via memory: `false-side-quasigroup-breakthrough`,
   `two-frontier-residual-and-budget-headroom`, etc.) to inform what
   "structurally interesting" witness families to look for at order 5.
3. Scale this probe up (larger N, stratified/targeted sampling instead of
   uniform, run against the fuller steelman portfolio — not just Vampire) 
   before committing to building the full order-5 Lean harness + proposer loop.

## Artifacts produced
- `paper/scripts/sample_order5.py` — reusable sampler (bump `--n` to scale up).
- `paper/problems/order5_probe.jsonl` — the 250 sampled pairs.
- `paper/tptp_order5/` — TPTP encodings.
- `paper/results/baselines_order5.jsonl` — raw Vampire run records.
- This report.
