# AAAI-27 Reproducibility Checklist — drafted answers

**Due with the paper, not with the supplementary.** AAAI-27's submission instructions
require the checklist from the Author Kit, uploaded in its own field on the form at
paper-submission time.

**Source caveat:** AAAI has not posted a separate AAAI-27 checklist page; the questions
below are AAAI-26's, which have been stable across AAAI-24/25/26. Diff them against
`ReproducibilityChecklist.tex` in your Author Kit before filling — if AAAI-27 added an
item, it will be in the .tex and not here.

**Two items need action, not just an answer.** They are flagged ACTION below.

---

## 1. General

| # | Question | Answer | Basis |
|---|---|---|---|
| 1.1 | Conceptual outline and/or pseudocode of AI methods introduced | **yes** | §3.2 gives the extension rule and the screening pipeline; §3.3 gives both judge channels; Table 3 is the funnel; Figure 1 works both checks on two laws. |
| 1.2 | Delineates opinion/hypothesis/speculation from objective facts | **yes** | §5 is explicitly conditional ("If these weaknesses generalize"); empirical claims are scoped to configurations tested throughout. |
| 1.3 | Pedagogical references for less-familiar readers | **yes** | Birkhoff 1935, Burris & Sankappanavar 1981, Baader & Nipkow 1998, Kisielewicz 1997 for the algebra; Bachmair & Ganzinger 1994 and Knuth–Bendix 1970 for the proving. |

## 2. Theoretical contributions — **yes**, this paper makes them

| # | Question | Answer | Basis |
|---|---|---|---|
| 2.1 | Assumptions and restrictions stated clearly and formally | **yes** | Admissibility is defined before use (§3.1); the dichotomy is Equation (1); the surjectivity premise is Equation (2). |
| 2.2 | Novel claims stated formally | **yes** | Equations (1), (2), (3), (6). |
| 2.3 | Proofs of all novel claims included | **yes** | The general argument (injective ⇒ surjective on a finite carrier ⇒ forces x=y) is §3.2; every per-instance claim carries a machine-checked refutation proof, shipped in the supplementary. *"partial" is also defensible if you read §3.2's argument as a sketch — your call, but "yes" is supportable given the certificates ship.* |
| 2.4 | Proof sketches or intuitions for complex results | **yes** | §3.2's paragraph on why finiteness is not first-order expressible, and §3.3's composition of checks (a) and (b). |
| 2.5 | Citations to theoretical tools used | **yes** | Superposition, Knuth–Bendix completion, Infinox, Twee all cited at point of use. |
| 2.6 | Theoretical claims demonstrated empirically to hold | **yes** | The admissibility prover runs on all 10,474 candidates (Table 3); 262 exhibited models confirm the Austin branch. |
| 2.7 | Experimental code used to eliminate/disprove claims included | **yes** | Screening and admissibility code ships in `generator/`. |

## 3. Datasets — **yes**, this paper relies on one

| # | Question | Answer | Basis |
|---|---|---|---|
| 3.1 | Motivation for the selected datasets | **yes** | §3.2 argues extension over random sampling (admissible laws too rare to sample). |
| 3.2 | Novel datasets included in a data appendix | **yes** | `corpus/` in the supplementary zip: admissible pool with tiers, 195-class map, cert-63 law list, hard-25 sample. Note in the README that the cert-63 *solutions* are withheld by design, as the paper states. |
| 3.3 | Novel datasets publicly available upon publication | **yes** | Same. |
| 3.4 | Datasets from existing literature carry citations | **yes** | ETP (Bolan et al. 2025) is cited wherever order-5 seeds and law numbering are used. |
| 3.5 | Datasets from existing literature are publicly available | **yes** | ETP is public. We reference it by law number and redistribute none of its files. |
| 3.6 | Non-public datasets described in detail | **NA** | Everything used is either public or released here. |

## 4. Computational experiments — **yes**

| # | Question | Answer | Basis |
|---|---|---|---|
| 4.1 | Number and range of values tried per hyper-parameter | **yes** | Budgets 30/60/120/300/600 s across 8 prover configurations (§4.1); LLM side is reasoning effort {medium, low}, waypoints {on, off}, 3 feedback rounds (§4.2, Table 5). |
| 4.2 | Pre-processing code included | **yes** | Screening and dedup scripts ship in `generator/`. |
| 4.3 | All source code for conducting and analyzing experiments included | **yes** | `judge/`, `baseline/`, `llm_runs/` in the zip. |
| 4.4 | Source code publicly available upon publication | **yes** | |
| 4.5 | New-method code has comments detailing the implementation | **ACTION — answer "partial" unless you know otherwise** | I have not read the scripts for comment density. "partial" is the safe, honest answer; upgrade to "yes" only if `prove_status.py`, `answer_spec.py`, and `llm_construct.py` carry real implementation comments. |
| 4.6 | Method for setting seeds described, if randomness is involved | **yes** | §4.2 states that each run samples a fresh reasoning trace and that counts are pass@1 rather than a fixed solved set, and reports an independent repro run. `config.paper.json` records `use_seed: false`, temperature 1.0 — the API exposes no usable seed for these models, and the paper handles it by reporting repeated independent runs instead. |
| 4.7 | Specifies the computing infrastructure used | **ACTION — currently "no"** | There is no hardware statement anywhere in the paper (grepped: no CPU, core, memory, or worker count). One sentence in the supplementary appendix fixes it — "Prover runs were executed on ⟨CPU⟩ with ⟨N⟩ parallel workers; LLM runs called ⟨o3 / o4-mini / GPT-4.1⟩ through the OpenRouter API." Send me the spec and I'll write it in. |
| 4.8 | Formally describes evaluation metrics | **yes** | A law is *resolved* when a configuration returns a certificate (§4.1); a *verified solve* is a judge-accepted submission (§3.3); pass@1 is defined where used (§4.2). |
| 4.9 | States the number of runs used for each reported result | **yes** | §4.2 is explicit: single-run pass@1, plus one independent reproduction run, with the union across runs reported. |
| 4.10 | Analysis goes beyond single-dimensional summaries | **yes** | Budget ladder (Table 4), per-check failure taxonomy (too strong / too weak / both), single-check clearance rates, per-LLM failure profiles. |
| 4.11 | Significance judged with appropriate statistical tests | **partial** | No formal test is run. §4.2 explicitly declines to claim the waypoint effect, calling the six-vs-nine difference indistinguishable from run noise and treating it as suggestive. *"no" is also defensible; "partial" reflects that the paper judged the comparison and refused the claim rather than ignoring it.* |
| 4.12 | Lists all final hyper-parameters per model/algorithm | **yes** | Provided the shipped config matches — see the flag below. |

---

## Two flags before you submit this

**`config.paper.json` disagrees with the paper.** It records `reasoning_effort: "high"`,
while §4.2 reports medium (and low for the ablation). If that file ships in the
supplementary as the record of final hyper-parameters, item 4.12 becomes wrong. Either
confirm the runs actually used the effort the harness passed rather than this config's
default, or ship a corrected config alongside the run scripts.

**`paper/latex/main.tex` in the repo is stale.** It still contains the pre-07-28 §4.2 and
Discussion — the cut summary sentence, "ALPS isolates the one step…", the old Conclusion
with the semicolon fragment. Overleaf remains canonical; don't build the supplementary
claims→artifact map from the repo copy. (It is clean of `%PROV`, `TODO`, `VERIFY`, and
`??`, so that grep is done.)
