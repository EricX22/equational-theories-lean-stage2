# PAPER HANDOFF — Austin-law benchmark (AAAI-27)

Consolidated state for continuing the paper. Companions: `PAPER_PLAN.md` (design +
reasoning), `OUTLINE.md` (section-by-section skeleton), `HANDOFF.md`/`HISTORY.md`
(experimental history), `figures_tables.tex` (T1/T2/F1 drafts). This file is the single
place to resume from.

Written end of the 2026-07 writing session.

---

## 0. One-paragraph thesis

The Equational Theories Project (ETP) is verifiable but **uniform** — one strategy (ATP
proof search + finite model builder) resolves ~22M implications, so it measures
execution, not construction. We isolate **Austin laws** (infinite models, no nontrivial
finite one; order ≥5, where finite search is empty by theorem), extend past the order ETP
enumerated, and pose a **two-sided, machine-checkable task**: given an admissible law $L$
(certified to have no nontrivial finite model), either construct a nontrivial model with a
Lean proof it satisfies $L$, or prove $L \models x=y$ (trivial). It is an **AAAI-27
main-track benchmark paper.**

The four selling points, threaded through the paper as **V / N / C / M**:
- **V — Verifiable:** answers are Lean proofs, kernel-checked; no human in the loop.
- **N — Non-vacuous:** every instance is certified answerable (the dichotomy), so it is a
  set of well-posed questions, not an open-problems list or a wall.
- **C — Contamination-free & renewable:** a public generator mints fresh order-≥6
  instances that did not exist before, unseen by any model's training.
- **M — Method-bound:** difficulty is the deductive-vs-constructive asymmetry — trivial is
  found by search (r.e.), Austin must be *constructed* — not a matter of compute.

**Do NOT claim full undecidability as load-bearing.** The asymmetry ("failure to prove
trivial is not a model") carries the argument; undecidability of equational entailment is
cited only as background (`baaderNipkow1998`), softened ("in general," "can be expected").

---

## 1. Paper structure and the claim each section makes

Standard-AAAI titles; the benchmark design lives as subsections of §3 (the "Method"
slot). Section numbers are AAAI-unnumbered; cross-ref numbered floats/theorems with plain
`\ref`, sections by name (no `hyperref`/`cleveref` — forbidden).

**1. Introduction** — ETP is uniform → measures execution not construction; Austin laws
are where the uniform strategy is provably inapplicable; the four features V/N/C/M; the
formal hook (deductive vs constructive). Contributions: (i) two-sided task + certified
answerability; (ii) order-≥6 corpus + public generator; (iii) Lean judge; (iv) strong
baseline defining the hard tier, shown method-bound; (v) two ETP-open order-5 cases closed.
*Write last.*

**2. Related Work** — AI-for-science/reasoning benchmarks (stress the contamination
problem our generator sidesteps); ETP (source of the term "Austin law," blueprint §5/§20,
Kisielewicz); Lean/ITP; ATP + completion + SZS; **JRS (Janota–Rawson–Schulz,
arXiv:2602.16324)** — the closest prior work, position honestly: they do saturation-as-
model for order ≤4 arbitrary targets; we fix the target to Eq2, restrict to certified-
no-finite-model laws, go past order 5, and make it an AI-for-science *benchmark*; Infinox
(our admissibility prover is a specialisation).

**3. The [NAME] Benchmark** (Method):
- **3.1 Problem Formulation** — DRAFTED (see §2 below). Claims: the task is well-defined
  (magma/law/order/carrier/trivial), admissible = certified no-finite-model, the
  dichotomy (trivial XOR Austin), non-vacuity (every instance answerable — from excluded
  middle, *not* from our filter), the deductive/constructive asymmetry, the capability
  isolated (synthesis tailored to the law).
- **3.2 Answer Verification** — DRAFTED. Claims: a submission is a Lean proof of a
  generated goal (`AustinGoal`/`TrivialGoal`); nontriviality + admissibility ⇒ the model
  is infinite, so `AustinGoal` establishes $L$ is Austin without a finiteness proof; the
  checker is sound (fixed statement, kernel-checked, standard axioms) so accepted answers
  are genuine — details deferred to repo/appendix.
- **3.3 Corpus Construction** — NOT drafted. Claims: generation by one-op extension
  (~500× yield); admissibility filter; **≥26% class collapse (262→≤195), quote classes
  not laws**; `seed_dedupe` at generation; contamination-free (order ≥6, seeds+dates);
  durability = classes per thousand surviving extensions.

**4. Experiments**
- **4.1 Baseline Portfolio** — 8 configs (Vampire 5.0.1 ×5, E ×2, Twee 2.6.1), ladder
  30/60/120/300/600s, SZS verdicts, pinned, selftest-gated. Both proof-search and
  saturation because the two task directions need different machinery.
- **4.2 Method-Bounded Frontier** (core result) — flat curve (3/120 at 30s, 0 higher);
  **0 new AUSTIN, 11 TRIVIAL** (contamination shed); retry corroboration (3.7%, 0/216→
  AUSTIN); **no Twee-only model** → tier is method-bound, not Vampire-bound (the reshaping
  alternative is tested and ruled out).
- **4.3 LLM Baseline** — fair-effort, modest; ~0 on hard tier (reinforces difficulty). Use
  the **scaffolded "same jumping point" setting**: give every model the law + generated
  goal + a content-free proof skeleton with model-shaped holes + the judge as a
  verification oracle (self-verify loop, pre-registered). Isolates the creative leap from
  Lean-wrangling; fair because identical start.
- **4.4 Case Study & Climbable Gradient** — (a) 12857/33436 closed two ways (pipeline
  works end-to-end on literature-open problems) — **position carefully: NOT hard-tier, the
  portfolio resolves them; do not frame as beating the baseline;** (b) a few **hard-tier
  laws solved by hand** (algebraic models the portfolio misses, Lean-verified) — the
  evidence the frontier is *climbable*, highest-leverage main-track item. Also: the o3
  mod-17 affine model (n=17 outside the automated search's n≤13 cap) is a ready LLM
  capability demo *if* the instance is contamination-clean.

**5. Discussion & Limitations** — undecidability deliberately not claimed; hard-tier
collapse unmeasured (prover-only census there — no saturations); **ground confluence
open** → saturation-model answers not yet Lean-certifiable (algebraic ones are), companion
paper; 120-law curve is a rate, membership list needs the full sweep; (i)-prover vs
Infinox not yet benchmarked.

**6. Conclusion** — the four features cashed; the open challenge (construct where deductive
search cannot) on a renewable, contamination-free, verified family.

---

## 2. Drafted text (as of session end)

**§3.1 Problem Formulation** — 4 paragraphs, final:
1. magma/carrier/law/order/satisfies/trivial + the question (entails $x=y$ vs nontrivial
   model). Laws are $L: x=T$, $T$ of order ≥5.
2. finite vs infinite; finite found by search (no creative construction) → excluded;
   admissible = machine-checked no-nontrivial-finite-model; dichotomy (trivial XOR Austin,
   infinite); Austin laws named `\citep{kisielewicz1988}`. **Non-vacuity sentence:** "Every
   law either entails $x=y$ or it does not... admissibility guarantees only that the two
   possibilities are exactly the trivial and the Austin case... difficulty lies in finding
   the answer, not in whether one exists." (Definiteness from excluded middle, NOT our
   filter — this framing matters, see §7.)
3. the asymmetry (deductive/constructive); trivial = first-order consequence, proof search
   confirms if true; Austin = no such guarantee, absence of a derivation is not a model,
   entailment undecidable in general `\citep{baaderNipkow1998}` so no uniform procedure
   expected; construction ("not selected from a catalogue but invented"); climax: "the
   synthesis of a new mathematical structure, tailored to the individual law, that
   deductive search does not supply."

**§3.2 Answer Verification** — final:
1. lead-in + submission: "Given an admissible law $L$, a solver must produce an answer...
   that a machine can check. This answer — a *submission* — takes one of two forms: a model
   ... or a proof that $L$ entails $x=y$. Both checked automatically by Lean; accepted only
   when the check succeeds; a verified fact not a predicted label; no human in the loop."
2. generated goals: `AustinGoal` (∃ carrier, op, two distinct elements, Law) and
   `TrivialGoal` (∀ ... Law ⇒ all equal). Nontriviality clause; **soundness bridge**: "may
   look too weak... but admissibility excludes every nontrivial finite model, so any magma
   satisfying Law with two distinct elements is necessarily infinite, and a proof of
   `AustinGoal` establishes that $L$ is an Austin law." Requiring only nontriviality keeps
   it tractable (no infinitude proof in Lean).
- Soundness/anti-gaming paragraph: **dropped** (repo material — not running a competition).
- Optional format-agnostic line (judge accepts any model form) — include only to preempt
  "designed around your own methods."

**Figures/tables** (`paper/latex/figures_tables.tex`): T1 corpus composition, T2 baseline
curve, F1 pipeline schematic (TikZ). **T3 comparison table** (vs other AI-for-science
benchmarks on V/N/C/answerable/construction) and **L1 worked-example listing** (mod-17
model, doubles as LLM demo) still to build — T3 is high-leverage.

---

## 3. Frozen empirical numbers (with sources)

| result | number | source |
|---|---|---|
| corpus, by law (2026-07-09) | 9,725: 2895 trivial / 990 finite / 247 Austin / 3798 no-finite-model / 42 sat-only / 1753 open | HANDOFF.md §4 — **RECOUNT from final_status.jsonl before submission; reconcile 247 vs 262** |
| class collapse | 262 Austin-proven → ≤195 classes (≥26%) | `results/classes.json`, `equiv_sample.py` |
| baseline curve | 120 laws, 8 configs; 3/120 at 30s, 0 at 60/120/300/600 | `results/baseline_v1.jsonl` (portfolio d4ee2fb7) |
| baseline verdicts | 0 AUSTIN, 11 TRIVIAL; one law completion-only | same |
| retry conversion | 294 laws @300s: 3.7%; 0/216 → AUSTIN, 4 → TRIVIAL | `retry_curve.py` |
| 12857 / 33436 | Austin, two methods (Vampire sat + Twee); models 27/27, non-vacuous; NOT plain TRSs (70/69 unorientable) | `ordered_model.py`, Twee `--tstp` |
| Lean model file | 0 errors, 2 sorries (`exists_nf`, `ground_confluent`) | `lean/OrderedModel.lean` |
| judge | selftest passes end-to-end incl. reference answer compiles | `answer_spec.py --selftest --lean-dir .` |

---

## 4. Code / project organization

Root: `AnonymousSubmission2027.tex` (AAAI-27 kit, the live paper), `references.bib`
(**all entries flagged VERIFY**), `eprover/` (gitignored, source build).

`paper/`
- `PAPER_PLAN.md` OUTLINE.md HANDOFF.md HISTORY.md **PAPER_HANDOFF.md** (this) RUNBOOK.md
- `bin/vampire` (5.0.1, bundled)
- `lean/OrderedModel.lean` — the companion contribution; 3/4 steps proved, one real sorry
- `latex/` — `figures_tables.tex`, older `main.tex` skeleton, `draft_*.md`
- `certs/` — saturation certs (`% saturated-with:` header for ordering guard), `ordered/`
- `results/` — `final_status.jsonl`, `classes.json`, `baseline_v1.jsonl`, `retry_curve.json`,
  `.done/` markers, `run_all.log`
- `scripts/` — see below

**Scripts built this session (the paper's engine):**
- `ordered_model.py` — JRS Def 1-2: saturated set → model by *ordered* rewriting (handles
  unorientable equations). `--ordering kbo|lpo` with a mismatch guard (refuses if cert's
  `% saturated-with:` ordering ≠ eval ordering). `verify_law` (non-vacuity checked),
  `refutes`, `nontrivial`. Selftest.
- `answer_spec.py` — the judge. Generates `Law/AustinGoal/TrivialGoal`; header-body-footer
  sandwich; textual gate + axiom allowlist; `--selftest [--lean-dir .]`.
- `baseline_probe.py` — portfolio (8 configs), budget ladder, SZS-status verdicts,
  `--n` sampling (curve is a rate!), selftest. **Direction-aware: `triv` configs never emit
  AUSTIN** (a proving-mode saturation is untrusted).
- `equiv_sample.py` — equivalence census; model-based prover-free separation (1123/1128 on
  the pilot), only survivors go to the prover. `--no-models` for the hard tier.
- `seed_dedupe.py` — drop one-op extensions equivalent to their seed (6.3% on 28770).
- `retry_curve.py` — reads the 20s→300s conversion off retry vs pre-retry.
- `fingerprint.py` — deferred equivalence-fingerprint tool (exact invariants empirically
  dead on this corpus; only the prover-probe + model-refute channels have signal).
- `run_all.sh` — overnight orchestrator: gates (answer_spec, twee_strings), retry_curve,
  equiv_sample (BEFORE baseline — cheap-first), baseline, lean_model. SIG-keyed markers,
  truncates `baseline_v1.jsonl` once, `runnable()` prover check, `ALLOW_PROVISIONAL` guard.
- `progress_runall.sh` — read-only monitor (census, curve, by-config, TWEE-ONLY check,
  staleness — idle-aware).

**Pre-existing (Phase-0/harvest era):** `prove_status.py` (the 3 provers + certs),
`status_report.py`, `order6_targeted.py` (generator), `order6_grade.py` (the two *ours*
construction builders — NOT prior art; rename), `overnight.sh` (harvest loop),
`progress.sh` (monitors overnight.sh, NOT run_all), `etp_terms.py` (term parsing/emitters),
`lean_oracle.py` (algebraic-model verifier), `rescore_baselines.py`, `confluence_cert.py`.

`reference/equational_theories/` — checked-out ETP (snapshot `d612bc0`, 2026-06-14).
`attic/finite_regime/` — dead Phase-0 solver (incl. `proposer_o3.py`, the OpenRouter loop).

---

## 5. Standard workflow (how code gets made and validated here)

1. **Write to the local folder** with Write/Edit (`C:\Users\ericx\Projects\...`). This is
   the git working copy; the sandbox mounts it read-mostly.
2. **Every script has a `--selftest`** with known answers (e.g. 4916 saturates to AUSTIN, a
   known-trivial law proves TRIVIAL, an Austin law is NOT provable trivial). `run_all.sh`
   refuses to run without `SELFTEST OK`. Add one to any new script.
3. **Validate logic standalone in `/tmp`**, because the sandbox mount truncates files
   (~7–13KB, mid-line). Copy the pure logic into a `/tmp/*.py`, feed synthetic inputs
   covering the tricky cases, run. Never trust `bash -n` / `python -c` on the mounted file
   if it's large — check the real file with the Read tool instead.
4. **Run with** `PYTHONDONTWRITEBYTECODE=1 python3 -B` (stale pyc bit us).
5. **Ship to the cluster (groupml01)** via `git add -A && commit && push`, then `git pull`
   there. After pulling, *verify the sync landed* (`grep` for a known new string) — a pull
   that brings "1 file, 16 lines" means earlier commits didn't push.
6. **Long runs:** `setsid ... </dev/null &` + `disown` (plain `nohup &` dies on session
   close). Verify liveness in 90s (file exists + shards running) rather than waiting for the
   hourly heartbeat.
7. **Monitor** read-only with `progress_runall.sh` or `run_all.sh --status`.

---

## 6. Traps (all cost real time this session)

- **Mount truncation** — files >~7–13KB show cut off mid-line in bash; the disk file is
  fine. Verify with Read, validate logic in `/tmp`.
- **Stale mount** — the sandbox view of `results/` can lag the cluster by hours; a "result"
  that looks stale/old may just be an unsynced mount. Read cluster state from the cluster.
- **Append contamination** — `baseline_probe.py` appends; multiple runs mixed data (120s
  ballooned to 142 vs 117). `run_all.sh` now truncates once per run.
- **Heartbeat holds stdout** — a background child inheriting stdout keeps `| tee` open
  forever. Heartbeat writes to the log file only, started with stdout closed.
- **Bare `wait` deadlock** — `wait` with no args also waits for the heartbeat child (never
  exits). Collect shard PIDs, `wait "${pids[@]}"`.
- **Stale `.done` markers** — portfolio-dependent stages are SIG-keyed
  (`vampire|eprover|twee|budgets` hash) so adding Twee re-runs the selftest.
- **Twee** — ships as a `.tar.gz` (not a bare binary; `curl -o twee` gives you the gzip →
  "Exec format error"). Needs `--tstp` for SZS output; else only prose
  (`RESULT: CounterSatisfiable`). `runnable()` guards against a non-executable "prover."
- **Direction-aware verdict** — a `triv` config that saturates instead of proving must NOT
  be read as AUSTIN (proving-mode saturation is incomplete/untrusted).
- **Budget arithmetic** — hard-tier laws never resolve, so every law walks the whole
  ladder: 8 configs × 1110s = 8880 core-s/law. The curve is a *rate* → sample (`BASELINE_N`
  default 300); don't sweep all 3,428 for the curve (~7 days).

---

## 7. Writing process notes

- **Voice:** Eric's KDD paper (`Concept-Residual...`, in uploads). Declarative;
  define-then-explain ("A *X* is a..."); concrete grounding/examples; measured;
  **prose-forward, minimal lists, few theorem environments**; introduces notation but wraps
  it in words. Match this.
- **Cadence:** one paragraph at a time — draft, Eric edits, iterate. Give the LaTeX, then a
  short note on the 1–2 load-bearing choices, then offer the next paragraph. Don't over-
  explain.
- **Framing correctness that recurs:** (a) definiteness of an answer comes from excluded
  middle, NOT from admissibility (admissibility only rules out the finite-nontrivial third
  case); (b) "no general method" is FALSE — greedy/translation-invariant/affine/saturation
  are general; per-law tailoring is the honest claim, and the "needs bespoke construction"
  point is an *Experiments* finding (the residual resists all general builders), not a
  definitional claim; (c) don't frame verification as anti-cheating/competition — it's a
  sound autochecker.
- **LaTeX constraints (AAAI-27 kit):** forbidden — `hyperref`, `nameref`, `cleveref`,
  `geometry`, `float`, etc. Added OK: `amsmath/amssymb/amsthm`, `booktabs`, `tikz`
  (+`arrows.meta,positioning`). Sections unnumbered (`secnumdepth 0`); ref numbered floats/
  theorems with `\ref`, sections by name. `references.bib` at root; every entry VERIFY.

---

## 8. Open decisions / next steps (priority order)

1. ~~**Name the benchmark**~~ — DONE 2026-07-13: **ALPS — Austin Law Proof-Synthesis**.
   Thread through §3 title and every "our benchmark"/[NAME] placeholder.
2. **Draft §3.3 Corpus Construction**, then §4 Experiments, §2 Related Work, §1+abstract
   last. §5/§6 short.
3. **Hand-solve 2–3 hard-tier laws** (algebraic models, Lean-verified) — the climbable-
   gradient evidence; highest-leverage for main track. Try algebraic first (checkable now,
   dodges `ground_confluent`).
4. **LLM baseline** — pick model(s), the scaffolded setting, fresh solvable instance for the
   capability demo (check o3-1593 contamination status or regenerate).
5. **Build T3 (comparison table)** and **L1 (worked-example listing)**.
6. **Recount corpus numbers**; reconcile 247 vs 262 Austin; verify all citations
   (Kisielewicz, Austin, JRS arXiv, Infinox pages).
7. **Full hard-tier sweep** (membership list) — long run, after ladder/portfolio frozen.
8. Later / companion paper: prove `ground_confluent` in `OrderedModel.lean`.
