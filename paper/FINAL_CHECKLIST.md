# ALPS / AAAI-27 — Final Checklist (canonical as of 2026-07-27 evening)

Supersedes REFRAME_SWEEP.md (fully applied) and the state sections of
PROJECT_STATE_AND_STYLE.md. Paper is CONTENT-COMPLETE: all sections drafted in the
final register (intro, related works, method, experiments, discussion, conclusion),
sweep finished, all numbers final. What remains is mechanical + packaging.

**DEADLINES: full paper 2026-07-28 11:59pm UTC-12 (tomorrow). Supplementary + code
2026-07-31 11:59pm UTC-12.**

---

## A. Final numbers (sweep merged & verified 2026-07-27: 4,141 laws, 0 dup rows)

Resolved **114 = 110 trivial + 4 models** (2.8% of residual). Ladder (models/trivial/
unresolved-after): 30s 4/87/4,050 · 60s 0/8/4,042 · 120s 0/5/4,037 · 300s 0/4/4,033 ·
600s 0/6/**4,027**. Hard tier **4,027 (97.2%)**. Abstract/intro pair: **2.2%** (30s
rung, 91/4,141) + **0.6%** added (23 laws, all trivial). Identities to spot-check after
edits: 91+8+5+4+6=114; 4,141−114=4,027; 2.2+0.6≈2.8.

### The ten number swaps (find → replace)
1. Abstract: 2.5% → 2.2% ; adds 0.1% → adds 0.6%
2. Intro validation ¶: same pair as abstract, verbatim
3. §4.1: "further 90 laws (2.2% of the residual): 86 triviality proofs" → "further 114
   laws (2.8% of the residual): 110 triviality proofs"
4. §4.1: "remaining 4,051 laws" → "remaining 4,027 laws"
5. §4.1: "of the 90 residual laws ... 73 resolve at the 30-second" → "of the 114 ... 91
   resolve at the 30-second"
6. §4.1: "resolves only 17 more" → "resolves only 23 more" (still "each one a
   triviality proof" — verified true)
7. Table 4 rows: 4/87/4,050 · 0/8/4,042 · 0/5/4,037 · 0/4/4,033 · 0/6/4,027
8. Table 4 caption: "4051 laws (97.1%)" → "4,027 laws (97.2%)"
9. §4.2: "25 of the 4,051" → "25 of the 4,027" (hard-25 sample verified still
   unresolved in final sweep — sentence stays exact)
10. Conclusion: "adds 17 triviality proofs" → "adds 23 triviality proofs" (its 2.2%
    stays — now denotes the 30s rung, matching the abstract)

DO NOT touch Table 3 (screening funnel): 10,474/1,085/9,389/1,906/7,483/3,080/195/4,141
are screening-stage numbers. Rename its residual row "**Unresolved by screening**" and
keep the caption clause handing the residual to §4.1 (stage distinction, not staleness).

## B. Mechanical sweeps (one pass each, then recompile)

1. **model → LLM/solver** where it means the AI system. EXCEPTIONS (math sense, keep):
   "no new models", "completion-only models", "All four models the sweep recovers",
   every "model of a law / nontrivial model / finite model". Table 5 header "Model" →
   "LLM". Do by eyeball, not regex.
2. **Spaced hyphens " - " → "---"**: intro ¶1 (world - formalizing), walk-through ¶
   (executed - specification ... verification -), contributions bullet (channels - a
   Lean proof ... -), generation ¶ (recursive - laws ... n+1 -). Grep " - " for stragglers.
3. **"(Figure 2)" → "(Table 2)"** in walk-through ¶ (mirror is a table now; label kept).
4. **Equation \eqref vs bare \eqref** — one convention (paper is on "Equation \eqref").
5. **certified/verified adjective** — one choice for solve-adjective ("verified"
   recommended; "certificate/certify" reserved for the artifact/judge act).
6. Table 1 caption: drop "effectively" if still present; caption family-cites already
   cut (families cited in §2 text).
7. Final grep for "??" in the compiled PDF (broken refs) and for "%PROV"/"TODO"/"VERIFY"
   comments left in the tex.

## C. Verify-before-submit

- **Appendix worked example exists** — §4.1 promises "the full worked example is in the
  appendix" (12857/33436, 27 equations). If the appendix moved to supplementary, change
  the sentence to "in the supplementary material."
- Bib: runco2012standard, solar2006combinatorial, solar2013program, alur2013syntax,
  garg2014ice, hubert2026olympiad all present (confirmed in v9 refs); re-check after
  final compile that none went unused/undefined.
- Vendor clause: confirm no "rather than vendor" survives anywhere (believed cut →
  Gemini run moot; remaining OpenRouter credits are free budget).
- OpenReview: title registered; **abstract field must be updated to match the final
  PDF abstract (2.2/0.6 numbers)** if the form allows edits until the paper deadline.
  Keywords per plan: primary ML: Evaluation/Benchmarking/Datasets & Analysis;
  secondary APP: AI for Science; optional NLP: (L)LMs.
- Links block in main.tex stays commented (anonymous submission; code goes via
  supplementary upload, not links).
- Final full-paper adversarial read on the last compile (numbers cross-check, refs,
  fixed-term consistency, style) — hand the PDF to the assistant session.

## D. Supplementary materials plan (due 2026-07-31 AoE)

Package = ONE zip + optional appendix PDF, anonymized. Suggested layout:

```
supplementary/
  README.md                  <- map of contents, judge quickstart, claims->artifact table
  appendix.pdf               <- worked example 12857/33436 (27-eq presentation, both
                                routes, non-orientability note) + protocol prompts +
                                per-config sweep table if cut from main
  corpus/                    <- released law sets: admissible pool w/ tiers, 195-class
                                map, cert-63 LAWS (NOT their chains), hard-25 sample
  generator/                 <- extension + screening scripts (prove_status, filters)
  judge/                     <- answer_spec.py (Lean side), llm_construct.py (ATP side),
                                --selftest instructions, Vampire build/version notes
  baseline/                  <- baseline_probe.py, resume_sweep.sh, merged
                                baseline_full.jsonl (25 MB — check size limit; else
                                per-budget summary + regeneration instructions)
  llm_runs/                  <- run harnesses + result jsonls (autoform cert63/nohints63/
                                repro/low, construct hard25 x3, hard25 trivial), prompts
```

Rules discovered earlier, DO NOT VIOLATE:
- **No ETP data files** (single-file redistribution rule — etp-repo-findings memory).
  Reference ETP by law numbers only; the corpus we ship is our own extension output.
- **Cert-63 solutions stay withheld** (paper says so): ship the law list, not
  easy_chain_harvest chains. State the withholding in README.
- **Anonymize**: strip /u/jrg4wx paths, EricX22 URLs, author names from headers, git
  metadata (export files, don't zip the .git), OpenRouter keys from any log.
- Vampire binary: confirm license permits redistribution (v5.0.1); otherwise ship
  version + download pointer instead of the binary.
- Check AAAI-27 supplementary size limit + whether the reproducibility checklist is
  required this year (template has ReproducibilityChecklist.tex commented).

Build order (fits before 07-31): 1) appendix.pdf from existing worked-example material;
2) code dirs by copying the frozen scripts (they are already self-contained); 3) scrub
pass (grep for jrg4wx, EricX22, sk-or-, home paths); 4) README with claims→artifact map
(each paper number → file that reproduces it); 5) zip, size check, upload.

## E. Post-submission (before 07-31, low priority)

- Camera-ready debts if accepted: de-anonymize, links block, real author block.
- Leftover OpenRouter credits: optional Gemini repro-14 for rebuttal ammunition.
- Rebuttal kit already banked: CEGIS argument (in paper §5 now), hard-tier provenance
  (ETP case in §4.1), taxonomy re-derivation scripts.
