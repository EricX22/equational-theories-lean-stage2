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
  generator/           corpus extension + screening scripts
  judge/               the two-channel judge and its validation harness
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
with the bundled Vampire binary at `judge/vampire` (v5.0.1, BSD 3-clause;
see `judge/VAMPIRE_LICENCE`).

Environment used for all reported runs: 2× AMD EPYC 7313 (32 cores), 503 GB
RAM, Ubuntu 22.04.5. Provers: Vampire 5.0.1, Twee 2.6.1, E 3.3.5. LLM calls
went through a single API gateway with provider-default sampling; the APIs
expose no seed parameter, so run-to-run variation is measured (reproduction
run) rather than controlled. Result files record every attempt verbatim.

## Claims → artifacts

Every number in the paper traces to a file in this package. Result files are
JSONL, one record per law per run.

| Paper claim | Artifact | Check |
|---|---|---|
| Screening funnel (Table 3) and 4,141-law residual | `corpus/` law sets, `generator/` scripts | counts per file |
| Sweep resolves 114 = 110 trivial + 4 models; hard tier 4,027 (97.2%) | `baseline/baseline_full_final.jsonl` | count RESOLVED records by verdict |
| Budget ladder 91/8/5/4/6 by rung (Table 4) | same file | group resolved laws by first-resolving budget |
| Per-configuration table (Appendix A3) | same file | group by (config, budget) |
| o3 trivial: 4/63 (6.3% pass@1) without waypoints, 9/63 (14%) with | `llm_runs/llm_autoform_o3_nohints63.jsonl` (first 63 records = first pass), `llm_runs/llm_autoform_o3_cert63.jsonl` (first 63 = first pass) | count `solved` in first pass |
| Second passes add 2 (no waypoints) / 0 (waypoints); 13 distinct laws solved across all runs | remaining records of the two files above + repro file | union of solved laws |
| o4-mini 0/63; GPT-4.1 both conditions | `llm_runs/llm_autoform_o4mini_cert63.jsonl`, `llm_runs/llm_autoform_gpt41_*63.jsonl` | count `solved` |
| Reproduction: 1/9 solved laws reproduce, 1/5 matched unsolved newly solve | `llm_runs/llm_autoform_o3_repro.jsonl` | compare against first-pass solved set |
| Hard-25 trivial channel: 0/25 (two-sidedness control) | `llm_runs/llm_autoform_o3_hard25.jsonl` | count `solved` |
| Hard-25 construction: 0/25 for all three LLMs | `llm_runs/llm_construct_{o3,o4mini,gpt41}_hard25.jsonl` | count `solved` (deduplicate to last record per law) |
| Failure taxonomy 23/2/0, 11/4/10, 10/11/4 (Appendix A4) | same three files | classify final-round attempt by checks (a)/(b) |
| Worked example 12857/33436: 27/27 ground instances, distinct normal forms | `judge/ordered_model.py` + `corpus/certs/` | rerun the script on the certificate |
| Renewability per order (Appendix A5) | `corpus/` per-order screening outputs | counts |
| Token/cost table (Appendix A8) | all `llm_runs/*.jsonl` | sum token fields per file |

## Withheld material

Two deliberate omissions, both stated in the paper:

1. **Reference solutions for the 63 certified-easy laws are withheld** to keep
   the trivial channel usable for future evaluation. `corpus/cert63_laws.jsonl`
   lists the laws; the harvested reference chains do not ship. Note that the
   raw result files necessarily contain the chains the evaluated LLMs
   themselves produced on solved laws — the experimental record is verbatim.
2. **No Equational Theories Project data files are redistributed** (their
   repository's single-file redistribution rule). Laws are referenced by ETP
   number only; every corpus file shipped here is output of our own extension
   and screening pipeline.

## Anonymization

Local filesystem paths, usernames, repository URLs, and API keys have been
stripped. Scripts take all paths as arguments; no absolute path in this
package is load-bearing.
