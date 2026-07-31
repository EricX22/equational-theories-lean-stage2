# ALPS — Supplementary Material

Supplementary material for "ALPS: Measuring Valid Creativity in Large Language
Models with Mathematical Construction" (AAAI-27 submission). This package
contains the appendix, the corpus artifacts, the complete judging and
evaluation code, and the raw result files behind every number reported in the
paper.

## Layout

```
supplementary/
  README.md            this file
  appendix.pdf         technical appendix (worked example, protocol + prompts,
                       per-configuration baseline, failure analysis, corpus
                       yield, judge validation, diversity, infrastructure/cost)
  corpus/              released law sets (see Withheld material below)
  certs/               prover certificates for the worked example (A1)
  generator/           corpus extension + screening scripts
  judge/               the two-channel judge, its validation harness, and the
                       Vampire 5.0.1 binary (BSD 3-clause; VAMPIRE_LICENCE)
  baseline/            automated-portfolio sweep code + merged results
  llm_runs/            LLM evaluation harnesses + raw result files
```

## Judge quickstart

The trivial-channel judge (Lean side) self-tests without any LLM access:

```
python3 judge/answer_spec.py --selftest --lean-dir <lean project root>
```

Expected output: seven textual-gate checks OK, then the reference answer
compiling through Lean. The construction-channel judge validation (positive
and negative controls of Appendix A6) runs through `judge/llm_construct.py`
with the bundled Vampire binary at `judge/vampire`.

Environment used for all reported runs: 2× AMD EPYC 7313 (32 cores), 503 GB
RAM, Ubuntu 22.04.5. Provers: Vampire 5.0.1, Twee 2.6.1, E 3.3.5. LLM calls
went through a single API gateway with provider-default sampling; the APIs
expose no seed parameter, so run-to-run variation is measured (reproduction
run) rather than controlled. Result files record every attempt; see Withheld
material for the one field stripped from solved rows.

## Claims → artifacts

Every number in the paper traces to a file in this package. Result files are
JSONL, one record per law per pass, appended in run order.

| Paper claim | Artifact | Check |
|---|---|---|
| Screening funnel (Table 3), 10,474 generated laws and their statuses | `corpus/final_status.jsonl`, `generator/` scripts | count rows per status |
| 195 logical classes among the 262 bare-certified laws | `corpus/classes_full.json` | count classes |
| Diversity / transfer numbers (Appendix A7) | `corpus/transfer.json` | read fields |
| Sweep resolves 114 = 110 trivial + 4 models; hard tier 4,027 (97.2%) | `baseline/baseline_full_final.jsonl` | count RESOLVED records by verdict |
| Budget ladder 91/8/5/4/6 by rung (Table 4); per-configuration table (A3) | same file | group resolved laws by budget / (config, budget) |
| o3 trivial: solutions with and without waypoints; multi-pass structure per A8 | `llm_runs/llm_autoform_o3_cert63.jsonl` (first 63 records = first pass), `llm_runs/llm_autoform_o3_nohints63.jsonl` (first 63 = first pass) | count `solved` per pass |
| o4-mini 0/63; GPT-4.1 0 in every run | `llm_runs/llm_autoform_o4mini_cert63.jsonl`, `llm_runs/llm_autoform_gpt41_cert63.jsonl`, `llm_runs/llm_autoform_gpt41_nohints63.jsonl`, `llm_runs/llm_autoform_cert63.jsonl` (early 95-law run), `llm_runs/llm_autoform_gpt41.jsonl` (pilot) | count `solved` |
| o3 low effort solves zero | `llm_runs/llm_autoform_o3_low.jsonl` | count `solved` |
| Reproduction: 1/9 solved laws reproduce, 1/5 matched unsolved newly solve | `llm_runs/llm_autoform_o3_repro.jsonl` | compare against first-pass solved set |
| Hard-25 trivial channel: 0/25 (two-sidedness control) | `llm_runs/llm_autoform_o3_hard25.jsonl` | count `solved` |
| Hard-25 construction: 0/25 for all three LLMs; failure taxonomy (A4) | `llm_runs/llm_construct_{o3,o4mini,gpt41}_hard25.jsonl` | classify final-round attempt by checks (a)/(b), last record per law |
| Worked example 12857/33436 (A1): both certificates, 27/27 ground instances | `certs/` + `judge/ordered_model.py`, `judge/confluence_cert.py` | rerun the checker on the certificates |
| Judge validation controls (A6) | `corpus/gold.jsonl`, `judge/answer_spec.py --selftest` | run the selftest |
| Token/cost table (A8) | all `llm_runs/*.jsonl` | sum `usage` fields per file |

## Withheld material

Two deliberate omissions, both stated in the paper:

1. **Solutions to the 63 certified-easy laws are withheld** to keep the
   trivial channel usable for future evaluation. `corpus/cert63_laws.jsonl`
   lists the laws; the harvested reference chains do not ship, and the
   submitted chain (`last` field) is stripped from every SOLVED row of the
   certified-easy result files, since a verified chain is itself a solution.
   Failed submissions are retained in full — the failure analysis depends on
   them, and a rejected chain is not a solution. Every count reported in the
   paper (solves per pass, rounds, token totals) is reproducible from the
   retained fields.
2. **No Equational Theories Project data files are redistributed** (their
   repository's single-file redistribution rule). Laws are referenced by ETP
   number only; every corpus file shipped here is output of our own extension
   and screening pipeline.

## Anonymization

Local filesystem paths, usernames, repository URLs, and API keys have been
stripped; the packaging script fails closed on any surviving credential or
identifying pattern. Scripts take all paths as arguments; no absolute path in
this package is load-bearing.
