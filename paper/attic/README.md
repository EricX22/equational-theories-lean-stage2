# attic/

Nothing here is on a live code path. Kept for provenance and for the two pieces
worth stealing back.

- `finite_regime/` — the pre-pivot solver: completion engine, CDCL finite-model
  finder, affine/quasigroup families, LLM waypoint proposer. Abandoned because the
  finite regime has **zero LLM-necessity** (an unconstrained model finder solves the
  whole capability band). Worth stealing back: `proposer_o3.py` — the OpenRouter call
  and self-verify loop, which the construction task will need.
- `order6_pipeline/` — generate → strip-trivial → fmb-confirm → grade. Superseded by
  `scripts/overnight.sh` + `scripts/prove_status.py`, which prove statuses instead of
  sieving candidates. `order6_strip_trivial.py` documents the trivial-strip filter,
  whose *absence* once made order-6 look barren.
- `logs/` — the four raw session logs, condensed into `../HISTORY.md`.
- `PAPER_PLAN.md`, `EXPERIMENT_SPEC.md`, `PROPOSER_LOOP_SPEC.md`,
  `STEELMAN_PORTFOLIO.md`, `ORDER5_HARNESS_FEASIBILITY.md` — plans written before
  the sieve-to-prover shift. Superseded by `../HANDOFF.md`.
