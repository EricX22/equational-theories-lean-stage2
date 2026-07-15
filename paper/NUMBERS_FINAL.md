# Finalized numbers (2026-07-14)

Recounted from the frozen data so the paper's figures stop being placeholders.
Sources: `results/final_status.jsonl` (10,474 records), `results/baseline_v1.jsonl`,
`results/retry_curve.json`, `results/classes_full.json`, `certs/`.

## Corpus composition (tab:corpus) — from final_status.jsonl
Status map: AUSTIN_PROVEN 262, NO_FINITE_MODEL 4141, TRIVIAL 3080,
HAS_FINITE_MODEL 1042, SATISFIABLE_ONLY 43, OPEN 1906.

Admitted (certified no nontrivial finite model):
- Austin, model exhibited: **262**
- Admissible, unresolved (hard tier): **4,141**
- Trivial (L ⊨ x=y): **3,080**

Discarded / uncertified:
- Has a nontrivial finite model: **1,042**
- Nontrivial model, admissibility uncertified (SATISFIABLE_ONLY): **43**
- Not certified admissible (OPEN): **1,906**

Total candidates: **10,474**

Superseded placeholders: 247→262, 3,798/3,400→4,141, 2,895→3,080, 990→1,042,
1,795→1,906, 9,725→10,474.

## Class collapse (tab:classes) — from classes_full.json
- Laws compared: **262**
- Confirmed-equivalent pairs: **255**
- Net class merges: **67**
- Distinct classes (upper bound): **≤195**
- Collapse: **≈26%**
- The 1,123/1,128 figure is the 48-law PILOT only — keep it labeled as an
  illustration, not a 262-law statistic.

## Baseline budget-ladder (tab:curve) — from baseline_v1.jsonl
- Sample: exactly **120 laws** at the 30s rung.
- Resolved: **3 distinct laws, all TRIVIAL, all at 30s**; 0 additional at any higher
  budget; **0 nontrivial models** at any budget. (The "10–11 TRIVIAL records" were one
  law proved by several configs — do NOT report as 11 laws.)

## Retry corroboration — from retry_curve.json
- matched 294, conversions 11 (**3.7%**), nfm 216, to_trivial 4, to_austin **0**,
  unconverted median 606.3s. (Prose figures already correct.)

## Two closed order-five cases (12857, 33436) — from certs/
- Twee: both **SZS CounterSatisfiable** (`certs/twee/{12857,33436}.out`).
- Vampire ordered saturation: **SZS Satisfiable** (`certs/ordered/12857.kbo.sat`),
  saturated set ≈361 formula lines. The prose "357 clauses" is in range but should be
  pinned to Vampire's own statistics line before submission.
- Model non-vacuous: 27/27 rules fire, x=y refuted (reproduce via
  `scripts/ordered_model.py`; `verify_law` flags VACUOUS if any rule never fires).

## Citations
- Kisielewicz "Austin identities": Algebra Universalis **38(3):324–328, 1997**
  (DOI 10.1007/s000120050057). FIX placeholder year 1988 → **1997**.
- Original term: A. K. Austin, "Finite models for laws in two variables," Proc. AMS, **1966**.
- (Distinct) Kisielewicz, "Varieties of algebras with no nontrivial finite members,"
  Lisbon conf., 1988 — only if that specific claim is cited.
- JRS: `arXiv:2602.16324`, Janota–Rawson–Schulz, **2026** — confirmed.
- Infinox (Claessen & Lillieström) — confirm exact year/venue when building the bib.

## Pending edits in AnonymousSubmission2027.tex (main file, left untouched)
- ~L361: "eleven laws are proved to satisfy L ⊨ x=y" → **"three laws"**.
- ~L379: "roughly 3,400 no-finite-model laws" → **"roughly 4,100"** (4,141 exact).
- tab:curve 120s-row denominator reads 0/117; raw data has 142 laws at 120s.
  Numerator is 0 either way, so immaterial, but clean up if you want consistency.

## Yield table (tab:yield / C3) — decision needed, no clean rate
- Random order-≥6 sampling is a dead end: ~30k pool → 6 Austin, none hard (≈0.02%).
- Extension is the "~500× volume engine" per HISTORY/notes, but RUNBOOK flags a caveat
  about filtering compute-shaped proofs "before quoting the 1,726 yield," so the exact
  extension rate is not a settled figure.
- Recommendation: drop C3 and state the point in one prose sentence, OR settle the
  extension denominator first.

## Still needs the real machine (not runnable in the sandbox)
- Hand-solve 2–3 hard-tier laws (Lean-verified algebraic models) — climbable-gradient evidence.
- LLM baseline run (per LLM_EXPERIMENT_PLAN.md).
- Full hard-tier sweep for the definitive membership list.
