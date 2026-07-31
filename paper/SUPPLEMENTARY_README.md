# ALPS — Supplementary Material

Code, corpus and certificates for *ALPS: Measuring Valid Creativity in Large
Language Models with Mathematical Construction*.

Everything here is our own output. See **What is not included** below for two
deliberate omissions.

---

## Layout

```
supplementary/
  README.md
  corpus/      the released law sets and derived corpus statistics
  generator/   extension engine, screening pipeline, admissibility prover, dedup
  judge/       both verification channels, plus the ordered-model checker
  baseline/    the automated portfolio sweep and its full result set
  llm_runs/    the evaluation harnesses and every result file reported
  certs/       prover certificates for the worked example of Appendix A
```

Python 3.10+ and the standard library are sufficient for every script here
except those that invoke a prover; those take the binary's path as an argument.

---

## Quickstart: check that the judge is sound before trusting anything else

Both channels ship their control suites. Neither needs the corpus.

```bash
python3 judge/answer_spec.py --selftest
python3 judge/llm_construct.py --selftest --vampire /path/to/vampire
```

The first exercises seven ways a submission could avoid proving anything — a
`sorry`, a declared axiom, two forms of namespace shadowing, redefining the law
predicate as `True`, `native_decide`, and a misnamed theorem — and confirms each
is rejected before Lean is invoked. It also confirms a reference answer passes
and compiles within the axiom allowlist `{propext, Quot.sound,
Classical.choice}`.

The second runs the three construction controls: the law itself certifies, the
left projection `x ◇ y = x` fails check (a) as too weak, and `x = y` fails
check (b) as too strong.

---

## Claims → artifact

Each number in the paper and the file that reproduces it.

| Paper location | Claim | Artifact |
|---|---|---|
| Table 3 | 10,474 candidates; 1,085 removed by the finite-model filter; 1,906 by the admissibility prover | `corpus/final_status.jsonl` (`status` field) |
| Table 3 | admissible pool 7,483 = 3,080 trivial + 262 Austin + 4,141 residual | `corpus/final_status.jsonl` |
| §3.2 | 262 Austin laws collapse to 195 classes; 34,191 pairs, 255 proved equivalent, 0 undecided | `corpus/classes_full.json` |
| §4.1, Table 4 | 114 laws resolved by the sweep (110 trivial, 4 models); ladder 91/8/5/4/6; hard tier 4,027 | `baseline/baseline_full.jsonl` |
| §4.1 | per-configuration resolution counts | `baseline/baseline_full.jsonl` (`config` field) |
| §4.1, Appendix A | laws 12857 and 33436 resolved by two independent methods | `certs/`, `judge/ordered_model.py` |
| §4.2 | the 63-law certified-easy set | `corpus/cert63_laws.jsonl` |
| §4.2 | the 25-law hard-tier sample | `corpus/hard25_sample.jsonl` |
| §4.2, Table 5 | verified LLM solves per model and configuration | `llm_runs/llm_autoform_*.jsonl` (`solved` field) |
| §4.2 | construction attempts, 0/25 for every model | `llm_runs/llm_construct_*_hard25.jsonl` |
| §4.2, Appendix D | failure classification: too strong / too weak / both | `llm_runs/llm_failure_breakdown.py` over the above |
| §4.2 | median ≈50,000 completion tokens per solved law | `llm_runs/*.jsonl` (`usage` field) |
| Appendix E | admissible-law yield by order | `corpus/final_status.jsonl` (order = count of ◇) |
| Appendix G | 195 construction classes coincide with 195 logical classes; cross-class transfer 0.25% | `corpus/transfer.json`, `generator/construction_transfer.py` |

Reproducing the sweep in full is expensive: nothing resolves on the hard tier,
so every law walks the whole budget ladder. `baseline/baseline_probe.py` prints
a worst-case core-second estimate on startup, and `--n` samples a subset, which
measures the resolution rate as well as the full run does.

```bash
python3 baseline/baseline_probe.py --in corpus/final_status.jsonl \
    --status NO_FINITE_MODEL --out /tmp/sweep.jsonl \
    --budgets 30 --n 200 --shard 0/1 \
    --vampire /path/to/vampire --eprover /path/to/eprover --twee /path/to/twee
```

---

## What is not included

**Solutions to the certified-easy set.** The paper states that these are
withheld, so that the 63-law set remains usable as an evaluation set rather than
a worked example. `corpus/cert63_laws.jsonl` gives the laws. The verified chains
are not released: the `last` field, which holds a submitted chain, has been
removed from every solved row in `llm_runs/`. It is retained on rejected rows,
since the failure analysis depends on it and a rejected chain is not a solution.

**Equational Theories Project data.** No ETP file is redistributed. Laws that
originate in ETP's enumeration are referenced by ETP number only; the corpus
released here is the output of our own extension procedure. ETP is available
from its own repository.

---

## Provers

The portfolio is eight configurations over three provers. Binaries are not
redistributed; the versions used were:

| Prover | Version |
|---|---|
| Vampire | 5.0.1 (release build, commit `1b13eaf`) |
| E | 3.3.5 |
| Twee | 2.6.1 |

The Vampire version and build commit are also recorded in the header of each
certificate under `certs/`, so a reproduction can confirm it is comparing like
with like.

Prover runs for the paper were executed on a dual-socket AMD EPYC 7313 (2 × 16
cores, SMT disabled, 32 physical cores) with 503 GB of RAM under Ubuntu
22.04.5 LTS, sharded 32 ways.

---

## Language-model runs

Runs were made through the OpenRouter API. Reasoning effort is medium except
where a filename or the paper marks it low; GPT-4.1 has no effort setting. Solve
events are stochastic — a repeat run under identical settings reproduced one of
nine solves — so single-run counts in the paper are reported as pass@1 samples
rather than as a fixed solved set. `llm_autoform_o3_repro.jsonl` is that repeat
run.

No API key is included. The harnesses read one from the environment.
