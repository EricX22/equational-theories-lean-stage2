# ALPS / AAAI-27 — Project State and Writing Style Guide

**This document is canonical as of 2026-07-24.** It supersedes the state sections of
`PAPER_HANDOFF.md` / `HANDOFF.md` and all earlier style notes. Session memory points here.
Update this file when state changes; keep memory entries as pointers plus hard rules only.

**Source-of-truth warning:** Overleaf is canonical for the tex. The repo copy of
`AnonymousSubmission2027.tex` was last synced 2026-07-20 and does NOT contain the
valid-creativity reframe. Re-download from Overleaf before any session that needs to read
current text.

---

## Part I — Writing style (REVISED 2026-07-23; supersedes all prior style guidance)

### The correction

The paper's prose had drifted toward a punchy, rhetorical register: sentence fragments
for emphasis, colon-punchlines, aphorisms, antithesis pairs ("method, not budget"),
personified artifacts, and sentences that exist for rhythm rather than content. **This is
now considered wrong for this paper.** The target register is technical, professional,
and direct. The results are interesting on their own; prose that performs undermines
credibility. This applies to body text, captions, and the abstract.

### What stays (structural principles — unchanged)

- **Reader-state discipline.** Before drafting a paragraph, state where the reader is and
  what the paragraph must move them to believe. Structure follows from that.
- **Show, don't tell.** Evidence before interpretation. No grandiose significance
  sentences; the reader infers importance from what is demonstrated.
- **Plant/payoff callbacks** at the structural level (e.g., Erdős stated thinly in ¶1,
  revealed as an infinite construction in the convergence paragraph). One plant, one
  payoff.
- **No overclaiming.** Scope every claim: "at any budget we test," "no method we run,"
  never unqualified "non-derivable" (Lean proofs are r.e.). Two-sided task facts stay
  exact.
- **Active voice, prose-forward, minimal lists.** Direct does not mean passive or
  nominalization-heavy. "We sweep the portfolio over the residual" is the right shape.

### The rules (sentence level)

1. **Findings are measurements, not verdicts.** Lead with the number, follow with the
   interpretation. Never the reverse, and never interpretation alone.
2. **No sentence fragments.** Every sentence has a subject and a finite verb. No
   sentences that exist for rhythm ("It does not.").
3. **No colon-punchlines or dash-reveals.** Colons introduce lists, definitions, or
   restatements — not quips. Em-dashes are for parentheticals only, at most one pair per
   paragraph.
4. **At most one rhetorical antithesis in the entire paper.** Current allocation: the
   abstract holds it ("the obstacle is not compute, but the absence of any method that
   produces the tailored structure each law requires"). All body copies stay plain
   ("limited by the methods available rather than by the compute allotted").
5. **No aphorisms or equative punchlines** ("The frontier is a property of the laws, not
   of a tool"). State the observation and its support.
6. **No personification.** Laws do not "resist everything we run" (→ "remain unresolved
   under every configuration"). Standard logic usage ("the law entails," "the set is
   satisfiable") is fine.
7. **Intensifiers require numbers or deletion:** exceedingly, remarkably, striking,
   precisely, exactly, genuinely, deliberately, almost nothing, nearly instantly.
8. **Size adjectives require numbers:** "a large and growing set" → "4,030 laws."
9. **Verbs of record, not drama:** "buys nothing" → "yields no additional resolutions";
   "erases/vaporizes" → "deletes/rewrites"; "cracks/attacks" → "resolves/attempts".
10. **No rhetorical questions.**
11. **Captions follow the same rules.** A caption states what the figure shows and what
    it establishes, in full sentences, without punchlines.
12. **Terminology is fixed and reused:** "valid creativity" (the defined term — see Part
    II); the two prover queries are "checks (a) and (b)" (never "horns"); "presentation
    E"; "admissible"; "hard tier"; "resolved". Introduce a term once, then use it
    unchanged. Plain-verb uses of "invent/construct" are fine; "invention" as a DEFINED
    TERM is retired (replaced by valid creativity).

### Examples (bad → good), drawn from the actual draft

- BAD: "If difficulty were graded by compute, added budget would buy resolutions along
  that gradient. It does not (Table 2)."
  GOOD: "Added budget does not increase the resolution rate (Table 2): 105 of the 111
  resolutions occur at the 30-second rung, and none occur after 300 seconds."

- BAD: "the boundary is not a threshold we chose: it is a gap in the distribution."
  GOOD: "The two populations are separated by a gap in the resolution-time distribution;
  the tier boundary is not a chosen threshold."

- BAD: "The construction side stays at zero, and the way it stays there is the finding."
  GOOD: "No construction attempt certifies. The failures follow a consistent pattern: in
  23 of 25 attempts, the proposed presentation entails the law but is inconsistent with
  a ≠ b."

- BAD: "The frontier is a property of the laws, not of a tool."
  GOOD: "Both paradigms leave the same laws unresolved, so the difficulty is not specific
  to either search strategy."

- BAD (cleft): "It is that combination, a frontier problem that is nonetheless checkable
  and endless in supply, that makes them something a benchmark can be built upon."
  GOOD: "Austin laws therefore support a benchmark: each instance has a determinate
  answer, answers are machine-checkable, and fresh instances can be generated without
  limit."

- BAD: "These problems are exceedingly difficult, but that is the intent."
  GOOD: "These problems are difficult by design."

### De-punch pass status

Intro: largely rewritten 2026-07-24 in the reframe (verify remaining: "compute, not
creativity" in ¶1/¶2 region; walk-through and validation ¶ rewrites delivered 07-24 in
chat, plain register). Experiments §4.1: chat rewrite of 07-23 predates the correction
except ¶4 (redone as calibration sample); redo ¶1/¶2/¶5 phrasing when merging
("It does not", "not a threshold we chose", "floor's edge", "blind spot", "property of
the laws"). §4.2: rewrite pending, write directly in new register. Captions: failed-
submission and tab_frontier captions carry old-register lines ("bound by method, not
budget"; "the rule that erases..."), fix when placing. Abstract: rewritten 07-23/24 in
new register (done, pending term sync of "innovative").

---

## Part II — Project state (2026-07-24)

### Venue, identity, canonical sources

- AAAI-27 main track. Title registered (update pending term decision — see below).
  Abstract near-final (07-24 chat version; needs "innovative" → valid-creativity sync).
- Keyword plan: primary ML: Evaluation, Benchmarking, Datasets & Analysis; secondary
  APP: AI for Science; optionally NLP: (Large) Language Models. Avoid KRR primary.
- Canonical tex: Overleaf. Repo `AnonymousSubmission2027.tex` stale (2026-07-20).

### Thesis and framing (settled 2026-07-24)

- **Defined term: VALID CREATIVITY** — a solution event with two certifiable conditions:
  (1) the problem admits no solution by memory or by routine (necessity, a property of
  the PROBLEM — never phrase as "creativity occurred/was necessary inside the solver");
  (2) the answer is soundly justified (machine-verified). "Invention" as a defined term
  is retired; the operational stance (judged on the answer; adaptation-of-a-known-
  construction counts; "known procedure" = applies identically to every problem, leaves
  nothing to decide) carries over to the new term. Eric cut the explicit
  "inside the model" disclaimer sentences — necessity phrased problem-side does that
  work implicitly. Never say "non-derivable" unqualified.
- Anchor opportunity (recommended, not yet placed): the two conditions are the
  certifiable version of the standard definition of creativity (originality +
  effectiveness; Runco & Jaeger 2012; Boden novelty+value) — one clause + citation in ¶1.
- Three properties = what makes the two conditions certifiable: verifiable → soundness;
  renewable + constructive → necessity. Full confound triple appears once in full
  (properties ¶ closer).
- **Term-sync sweep still open:** title ("Measuring Invention..." → decide: keep
  "invention" OUT; option "ALPS: Measuring Valid Creativity in Language Models with
  Machine-Verified Mathematical Construction"); tab_gap caption ("measuring invention
  requires all three" → valid creativity); abstract ("verified answers must be
  innovative"); method breadcrumbs ("no invention is credited twice" → "no solution...";
  "only by inventing a model" → "only by constructing a model"); Related-Works closer.
  Plain-verb "invent" may stay.

### Intro structure (as reframed by Eric, 2026-07-24)

¶1 opener: LLMs in scientific work → Erdős → defines VALID CREATIVITY (two conditions).
¶2 properties-as-requirements + confounds + family walk + Table~tab:properties (former
block F moved up; table cite contract: all family exemplars cited in this ¶).
¶3 formal math as the setting + magma/law/trivial/Austin definitions.
¶4 ALPS task definition (two-sided, certificate, generator).
¶5 convergence (Erdős payoff + JRS).
¶6 walk-through: concrete discovery episode (reviewer's phrase "proposing a new
mathematical structure under constraints and verifying its global properties"),
figure ref, valid-creativity conditions decided by the answer, adaptation example
(rewrite delivered 2026-07-24 in chat).
¶7 validation + contributions (rewrite delivered 2026-07-24: 2.5%/0.1%/4,141 %PROV).

### Section status

- Intro: reframed by Eric around valid creativity; ¶6/¶7 rewrites delivered in chat.
- Related Works: complete (needs term-sync of closer).
- Method: complete incl. breadcrumbs; construction-channel clarity rewrite DRAFTED in
  chat (semantic E, syllogism, "the prover never reasons about infinity") — to merge;
  negative-controls sentence pending (verify actual gate contents first).
- Experiments §4.1: content rewrite done 07-23 (needs de-punch on merge; ¶4 already in
  new register). §4.2: pending — stochasticity/pass@1, weak-model comparison,
  launch-condition closer, cost sentence, seed-distinctness pointer, unpublished-
  instances sentence.
- Discussion: TODO. Anchors: valid-creativity scope concession (certifies the artifact/
  task conditions, not cognition); falsifiability + renewability (if tailoring is ever
  automated, those laws stop counting; generator mints past them); ground confluence =
  companion-work boundary; hard-tier interior un-censused; chain-length ladder as
  designed future rung; what methods the benchmark motivates (satisfy-the-law-without-
  collapse tension); hard-tier meaningfulness via provenance (contained ETP open
  problems; settled 12857/33436).
- Conclusion: TODO. Abstract: 07-24 version done pending term sync.

### Floats (final plan)

Intro: `fig_intro_mirror` (v4) + `tab_gap` (v3; caption term-sync pending).
Method: `fig_methodology_filters`, `fig_methodology_extension`.
Verification: `fig_toy_certificate` (toy x = x◇(y◇y), E={u◇v=u}, openly non-admissible).
Experiments: `tab_frontier` (replaces tab:curve — DELETE tab:curve), `tab_llm`
(dashes → 0s; repro footnote), `fig_failed_submission` (o4-mini verbatim, checks not
horns, derivations inline; caption de-punch pending).
Appendix: `fig_worked_instance` (law 0f43eb94ffca; verify hand-translated equations).
Pressure valves: extension figure → prose; toy + failed → one two-panel float.

### Provisional numbers registry (%PROV — swap when the frozen sweep finishes)

Extrapolated from the 43%-complete sweep (44 trivial + 4 completion-only at that point):
trivial 102 · completion-only models 9 · resolved 111 · hard tier 4,030 (97.3%) ·
ladder cumulative 105/109/110/111/111 · 30s rung = 2.5% · added-by-600s = 0.1% ("six
more laws"). APPEAR IN: `tab_frontier.tex` (%PROV tags) · §4.1 ¶2 and ¶4 · abstract
(2.5%, 0.1%, 4,141) · intro validation ¶ (2.5%, 0.1%, 4,141). Keep the abstract/intro
pair matched to the BUDGET split (30s rung vs added later), not the trivial/model split.

### Experiments data state (results/ paths)

- Certified-easy 63 (o3 full support): 9 kernel-verified solves (single run).
- REPRO RUN (`llm_autoform_o3_repro.jsonl`, identical settings): reproduces 1 of 9,
  solves 1 new of 5 → solve events stochastic; report pass@1 + per-law solve
  probability; 10 distinct laws verified across runs. Support-dial ablation (no-hints
  4/9) is within run noise of full support (1/9 rerun) → DOWNGRADED to suggestive.
  Clean signals: effort-low = 0 every run; GPT-4.1 = 0, o4-mini = 0 at every setting;
  construction = 0 everywhere.
- Construction hard-25: o3 0/25 (23 entail-but-collapse, 2 consistent-but-weak; E's not
  persisted). o4-mini 0/25 (10 both-fail / 11 entail-collapse / 4 weak). GPT-4.1 0/25
  (3 / 9 entail-collapse / 9 weak). Tallies are Claude's final-attempt classification —
  re-derive before publication.
- Pending/optional: vendor diversity (Gemini free tier on cert-63) or delete the
  "rather than vendor" clause; ~$5-8 of budget remains.
- Worked instances: `paper/certs/saturation/*.sat` = 305 = 262 AUSTIN_PROVEN + 43
  SATISFIABLE-ONLY REJECTS. Check `no_finite_model: true` in `results/final_status.jsonl`
  before exhibiting (0a724d3b3544 is a reject; 0f43eb94ffca, 0553134a10b3, 04ed20a636d7,
  149c4489ac1c are safe).

### Reviewer feedback tracker

- Prof round 1 ("why is this a benchmark") → resolved (capability-first reframe, now
  valid-creativity frame).
- Round 2 point 1 (term too broad) → resolved (valid creativity, two certifiable
  conditions, problem-side necessity).
- Point 2 (discovery connection too generic) → resolved (concrete-episode walk-through ¶
  using reviewer's own phrase + mirror/toy/failed/worked figures).
- Point 4 (construction verification unclear) → drafted (channel rewrite, to merge).
- Point 5 (more models/analysis) → partially resolved (weak-model runs, repro); vendor
  diversity open.
- Point 3 (hard-tier meaningfulness) → OPEN; planned answer = provenance (Discussion,
  two sentences).

### Mechanical sweep (do once, at the end)

Em-dashes " - " → "---" wherever remaining. Bullet 3 "proof\citep" space (fixed?).
Equation (1) terminal period. "proved/proven" consistency. Line ~320 placeholder cites →
`mccune2003mace4`, `claessen2003new`. "counts as resolves" → "resolved". Verify labels
fig:introduction / tab:properties against Figures/ filenames. references.bib pass.
Confirm no ETP-public seed laws in cert-63 / hard-25. Term-sync sweep (see above).
Typo watch: "produces new instance without limit" (abstract) → "instances".
