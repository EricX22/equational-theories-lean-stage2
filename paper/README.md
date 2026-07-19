# paper/ — Austin-law benchmark

> **Judging pivot (2026-07-17):** answers are "machine-checked" but NOT Lean-only. TRIVIAL side =
> Lean proof; AUSTIN/construction side = solver proposes a presentation `E`, **Vampire** certifies.
> Canonical definition + current state: `TASK_AND_JUDGING.md` (then `PAPER_HANDOFF.md`).

A graded, machine-checked corpus of **Austin laws**: magma laws `x = T` with no
nontrivial finite model but an infinite one. They are the exact locus of
undecidability for equational implication into `Eq2` (`x = y`), and the only class
whose difficulty does not expire with faster hardware.

**Start here: [`HANDOFF.md`](HANDOFF.md).** Thesis, the three provers, current
numbers, the one open question that blocks the paper, known bugs, and what to do
next in priority order.

- [`HISTORY.md`](HISTORY.md) — condensed session log, including the wrong turns.
  Several are still traps; read it before re-deriving one.
- `scripts/` — the live pipeline. `overnight.sh` runs the whole loop;
  `progress.sh` inspects a running job without touching it.
- `problems/order5_seeds.jsonl` — the 130 order-5 laws from ETP Tables 1–3.
- `results/` — shard outputs. `final_status.jsonl` is the corpus, `gold.jsonl` the
  benchmark instances. `results/archive/` is pre-pivot.
- `certs/saturation/` — existence certificates. **Stale**: written before the
  `--show_active on` fix, so they hold a subset of the saturated set, not the set.
- `attic/` — pre-pivot code, superseded pipelines, superseded plans, raw logs.

Quick start:

```bash
nohup bash paper/scripts/overnight.sh > /dev/null 2>&1 &
bash paper/scripts/progress.sh
python3 paper/scripts/prove_status.py --selftest paper/bin/vampire   # must print SELFTEST OK
```
