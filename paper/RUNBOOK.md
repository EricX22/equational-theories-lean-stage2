# RUNBOOK — what to run on the cluster, in order

**All of it, automatically:**

```bash
nohup bash paper/scripts/run_all.sh > /dev/null 2>&1 &
tail -f paper/results/run_all.log         # hourly heartbeat: stage, rows, load
bash paper/scripts/run_all.sh --status    # read-only, safe any time
```

It waits for any live `overnight.sh` stage, skips stages already done (markers in
`results/.done` — delete one to force a redo), and stops at the two gates below if they
fail. Smoke-test into a scratch dir first, same convention as `overnight.sh`:
`R=/tmp/rt IN=/tmp/rt/tiny.jsonl SHARDS=1 BUDGETS=1 bash paper/scripts/run_all.sh`.

The sections below explain *why* each stage is there and in that order.

Nothing here collides with `overnight.sh`'s `wait_for` (its `pgrep` patterns are
stage-specific: `prove_status.py .*retry_status_` etc.). The only cost of running
alongside a live pipeline is CPU. Do not launch a second `prove_status.py` writing to a
matching `--out` prefix.

---

## 0. Two commands that can invalidate work in progress. Run them first.

**(a) Does the answer format actually work?** This compiles the reference proof through
Lean. If it fails, item 1 of minimum-acceptable is not closed.

```bash
python3 paper/scripts/answer_spec.py --selftest --lean-dir .
```

Expected: seven textual gates OK, then `reference answer compiles OK`.
The textual gates are tested; the Lean round-trip has **never run**.

**(b) Twee's actual output.** `baseline_probe.py::_verdict` matches strings I guessed
(`"Ran out of critical pairs"`, `"The conjecture is true"`). If they are wrong, Twee
resolves nothing, silently, and the hard tier looks robust — a failure in the
comfortable direction.

```bash
twee /tmp/4916.p            # law 4916 + (u != v); read the output with your eyes
```

Then fix `_verdict` before trusting a single number from the Twee column.

---

## 1. Install the portfolio — **no root, no cabal**

`cabal install twee` needs `apt install cabal-install`, i.e. an administrator. Don't.
Twee publishes a **prebuilt Linux amd64 binary** with each release, and E builds from
source into your home directory.

```bash
mkdir -p ~/bin && export PATH=$HOME/bin:$PATH   # add to ~/.bashrc

# Twee — latest release is 2.6.1 (the CASC-30 version, Jan 2026).
#   https://github.com/nick8325/twee/releases/tag/2.6.1   <- grab the Linux amd64 asset
#   (repo archived May 2026; upstream moved to Codeberg)
mv twee-* ~/bin/twee && chmod +x ~/bin/twee

# E — source build, installs wherever you point it, no root
git clone https://github.com/eprover/eprover && cd eprover
./configure --bindir=$HOME/bin && make && make install

# Infinox — Haskell, needs GHC. DEFER: it is the admission ticket (PAPER_PLAN §5A),
# not a baseline resolver, so it blocks nothing here. If you do want it without root,
# install GHC via ghcup, which installs entirely under $HOME.

# JRS-modified Vampire/E, which print the rewrite system on saturation:
#   arXiv:2602.16324 §5 and people.ciirc.cvut.cz/~janotmik/stamp
#   NOT required — ordered_model.py already reads a stock Vampire saturation.
```

Sanity: `twee --version && eprover --version`, then re-run `run_all.sh`. The baseline
stage unblocks itself automatically once both are on `PATH`.

CSI / TTT2 / CeTA are **optional**: they certify plain TRSs, and ~36% of our order-5
saturations are not plain TRSs. `answer_spec.py` makes Lean the arbiter, so CeTA was
never on the critical path. Install them only to cross-check the clean cases.

---

## 2. The baseline (this is the gate for the hard tier)

```bash
python3 paper/scripts/baseline_probe.py --selftest --vampire paper/bin/vampire \
    --eprover $(which eprover) --twee $(which twee)
# then, sharded:
python3 paper/scripts/baseline_probe.py \
    --in paper/results/final_status.jsonl --status NO_FINITE_MODEL \
    --vampire paper/bin/vampire --eprover $(which eprover) --twee $(which twee) \
    --budgets 30,60,120,300,600 --shard $i/32 \
    --out paper/results/baseline_v1.jsonl --certs paper/certs/baseline
python3 paper/scripts/baseline_probe.py --curve paper/results/baseline_v1.jsonl
```

It refuses to start without `SELFTEST OK`, and it warns when a prover is missing —
a hard-tier claim from an incomplete portfolio is provisional.

**Prediction, recorded so it can be wrong:** Twee moves the number more than any
ordering change. Vampire under KBO and LPO produced identically-shaped saturations
(359/70 vs 358/70 on 12857), so ordering is not the live axis; unfailing completion is
built for this fragment and handles unorientable equations by construction.

---

## 3. Already answered — do not redo

```bash
python3 paper/scripts/retry_curve.py --results paper/results
```

Retry completed 2026-07-09 15:48. 294 laws at 300 s/prover: conversion **3.7%**;
of 216 `NO_FINITE_MODEL`, **4 → TRIVIAL** (1.9%, contamination) and **0 → AUSTIN**.
Zero saturations closed at 15× the budget. Unconverted laws burn the full budget
(median 606 s). The budget gate passes, *relative to one prover and one ordering*.

---

## 4. Corpus hygiene

```bash
# dedupe extensions against their seed (3/48 of 28770's extensions ARE the seed)
python3 paper/scripts/seed_dedupe.py --seed-law '<seed>' --seed-cert <seed>.sat \
    --extensions exts.jsonl --vampire paper/bin/vampire --out kept.jsonl

# equivalence classes, model-based separation (AUSTIN_PROVEN only — the hard tier has
# no saturations, hence no models, hence no cheap separations)
python3 paper/scripts/equiv_sample.py --in 'paper/results/final_status.jsonl' \
    --status AUSTIN_PROVEN --n 250 --vampire paper/bin/vampire \
    --sat-timeout 20 --prove-timeout 30 --out paper/results/classes.json
```

Housekeeping still open: rescore baselines (`rescore_baselines.py`); re-run the order-5
pass (law 22818 missing, 127 rows for 128 laws); regenerate saturation certs with
`--show_active on` **and** the `% saturated-with:` header that `ordered_model.py`
requires; split `OPEN` into "no tier-1 witness" (Infinox-shaped) vs "witness but no
proof" (compute-shaped) before quoting the 1,726 yield.

---

## 5. The contribution

```bash
lake env lean paper/lean/OrderedModel.lean     # never compiled; expect elaboration fixes
```

Three of the four steps are proved there. The remaining `sorry` is `ground_confluent`,
and that is the paper.
