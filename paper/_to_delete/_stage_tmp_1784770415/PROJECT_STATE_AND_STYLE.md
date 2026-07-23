# ALPS / AAAI-27 — Project State and Writing Style Guide

**This document is canonical as of 2026-07-23.** It supersedes the state sections of
`PAPER_HANDOFF.md` / `HANDOFF.md` and all earlier style notes. Session memory points here.
Update this file when state changes; keep memory entries as pointers plus hard rules only.

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

### The rules (sentence level — new)

1. **Findings are measurements, not verdicts.** Lead with the number, follow with the
   interpretation. Never the reverse, and never interpretation alone.
2. **No sentence fragments.** Every sentence has a subject and a finite verb. No
   sentences that exist for rhythm ("It does not.").
3. **No colon-punchlines or dash-reveals.** Colons introduce lists, definitions, or
   restatements — not quips. Em-dashes are for parentheticals only, at most one pair per
   paragraph.
4. **At most one rhetorical antithesis in the entire paper.** "Bound by method, not
   budget" currently appears in the intro, experiments, and a caption. Pick one home
   (recommend: experiments, where the evidence is) and rewrite the others plainly.
5. **No aphorisms or equative punchlines** ("The frontier is a property of the laws, not
   of a tool"; "not a baseline; it is a shrug"). State the observation and its support.
6. **No personification.** Laws do not "resist everything we run" (→ "remain unresolved
   under every configuration"); pipelines are not "pointed at the literature"; failures
   do not "sharpen." Standard logic usage ("the law entails," "the set is satisfiable")
   is fine.
7. **Intensifiers require numbers or deletion:** exceedingly, remarkably, striking,
   precisely, exactly, genuinely, deliberately, almost nothing, nearly instantly.
8. **Size adjectives require numbers:** "a large and growing set" → "4,030 laws."
9. **Verbs of record, not drama:** "buys nothing" → "yields no additional resolutions";
   "erases/vaporizes" → "deletes/rewrites"; "cracks/attacks" → "resolves/attempts".
10. **No rhetorical questions.** None currently in the draft; keep it that way.
11. **Captions follow the same rules.** A caption states what the figure shows and what
    it establishes, in full sentences, without punchlines.
12. **Terminology is fixed and reused:** the two prover queries are "checks (a) and (b)"
    (never "horns"); "presentation E"; "admissible"; "hard tier"; "resolved". Introduce a
    term once, then use it unchanged.

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

- BAD: "The pipeline, pointed at the literature, returns a new fact — but the portfolio
  reaches it, so the case marks the floor's edge, not the frontier."
  GOOD: "The resolved tier therefore already contains a previously open case. Because the
  portfolio resolves it, it belongs to the automated floor rather than to the hard tier."

- BAD (cleft): "It is that combination, a frontier problem that is nonetheless checkable
  and endless in supply, that makes them something a benchmark can be built upon."
  GOOD: "Austin laws therefore support a benchmark: each instance has a determinate
  answer, answers are machine-checkable, and fresh instances can be generated without
  limit."

- BAD: "These problems are exceedingly difficult, but that is the intent."
  GOOD: "These problems are difficult by design."

### Known offenders in the current draft (de-punch pass, in order of appearance)

- Intro: "Proven correct is not the same as new." (fragment-adjacent opener; acceptable
  to keep if Eric wants one deliberate short sentence in the paper — flag, don't silently
  keep); "exceedingly difficult"; "compute, not creativity" (antithesis #2);
  "bound by method, not computational budget" (antithesis #1, intro copy).
- §4.1: "two populations with almost nothing between them"; "It does not (Table…)";
  "not a threshold we chose"; "The floor is not without content"; "the pipeline, pointed
  at the literature"; "floor's edge, not the frontier"; "not one prover's blind spot";
  "A law yields in fractions of a second or resists everything we run"; "frontier is a
  property of the laws, not of a tool".
- §4.2: "the way it stays there is the finding"; "yields to nothing we run"; "the
  asymmetry of the task thus reappears one level up" (content is good; phrase plainly);
  "Instance selection is the step we control most carefully" (fine).
- Captions: failed-submission caption "the rule that erases the law's clutter also erases
  the witness" → state plainly ("the same rewrite that deletes the law's middle term also
  derives a = b"); "strong enough to entail L, too strong to keep two elements apart" →
  one instance of this phrasing may stay as the named tension, but only once in the
  paper.
- Abstract: final sentence colon-punchline → restate as a plain sentence.

---

## Part II — Project state (2026-07-23)

### Venue, identity, canonical sources

- AAAI-27 main track. Registration title + abstract drafted 2026-07-21 (abstract ~240
  words in chat; trim order if needed: ETP clause → examples list → merge confound
  sentences). Title: "ALPS: Measuring Invention in Language Models with Machine-Verified
  Mathematical Construction" (keep "invention" — it is defended; keep "machine-verified").
- Keyword plan: primary ML: Evaluation, Benchmarking, Datasets & Analysis; secondary
  APP: AI for Science; optionally NLP: (Large) Language Models. Avoid KRR primary.
- Canonical tex: `AnonymousSubmission2027.tex` at repo root (synced with Overleaf; repo
  copy may lag — Overleaf is source of truth). `paper/latex/main.tex` is an obsolete
  skeleton.

### Thesis and framing (settled)

- The paper measures **invention**, operationally defined (judged on the answer): novel
  to every model, beyond every known procedure, proven correct. Math is the apparatus,
  not the subject. Three properties = three confound removals (verifiable → no judging;
  renewable → no contamination; constructive → no procedure). The full confound triple
  appears ONCE in full (properties-¶ closer); compact forms elsewhere.
- Invention defense (intro ¶7): operational definition with named alternative ("not
  whether anything resembling human creativity occurred inside the model"), adaptation
  example, procedure defined as "applies identically to every problem, leaves nothing to
  decide." Discussion must still add the scope concession (artifact, not process) and the
  falsifiability/renewability note (if tailoring is ever automated, those laws stop
  counting; the generator mints past them).

### Section status

- Intro: complete (reframed capability-first; invention defense installed).
- Related Works: complete.
- Method: complete incl. breadcrumbs; construction-channel clarity rewrite DRAFTED in
  chat (semantic reading of E, the syllogism, "the prover never reasons about infinity")
  — Eric to merge; negative-controls sentence pending (verify which controls the current
  gate actually runs before claiming them).
- Experiments §4.1: rewritten 2026-07-23 against `tab:frontier` with PROVISIONAL numbers
  (see below). §4.2: rewrite pending — must incorporate stochasticity (repro run),
  weak-model construction results, launch-condition closing paragraph, cost sentence,
  seed-distinctness pointer, unpublished-instances sentence.
- Discussion: TODO. Anchors: invention scope concession; falsifiability + renewability;
  ground confluence = companion-work boundary; hard-tier interior un-censused;
  middle rungs (chain-length ladder) as designed future work; what methods the benchmark
  motivates (the entail-without-collapse tension).
- Conclusion: TODO. Abstract: drafted, not yet pasted into the tex.
- NOTE: all prose drafted before 2026-07-23 (including §4.1 rewrite and all figure
  captions) predates the style correction and needs the de-punch pass.

### Floats (final plan)

Intro: `fig_intro_mirror` (v4: generic header, satisfy-spine, no chips) +
`tab_gap`/properties (v3: no citations in float; adjacent prose carries all family
cites — that contract is LOAD-BEARING). Method: funnel `fig_methodology_filters`,
extension `fig_methodology_extension`. Verification: `fig_toy_certificate` (toy law
x = x◇(y◇y), E = {u◇v=u}; openly non-admissible, teaches admissibility by contrast).
Experiments: `tab_frontier` (replaces tab:curve — DELETE tab:curve and its \input),
`tab_llm` (dashes → 0s; repro footnote), `fig_failed_submission` (o4-mini verbatim,
checks not horns, derivations inline). Appendix: `fig_worked_instance`
(law 0f43eb94ffca end-to-end; verify hand-translated infix equations against the .sat).
Budget pressure valves: extension figure → prose; toy + failed → one two-panel float.

### Provisional numbers (swap when the frozen sweep finishes)

Extrapolated from the 43%-complete sweep (44 trivial + 4 completion-only at that point).
Tagged %PROV in `tab_frontier.tex`; appear in prose ONLY in §4.1 ¶2 and ¶4:
trivial 102 · completion-only models 9 · resolved 111 · hard tier 4,030 (97.3%) ·
ladder cumulative 105/109/110/111/111 · "six more laws" (600s vs 30s delta).

### Experiments data state (results/ paths)

- Certified-easy 63 (o3 full support): 9 kernel-verified solves (single run).
- REPRO RUN (`llm_autoform_o3_repro.jsonl`, identical settings): reproduces 1 of the 9,
  solves 1 new of 5 additional → solve events are stochastic; report as pass@1 with
  per-law solve probability; 10 distinct laws verified across runs. CONSEQUENCE: the
  no-waypoints ablation (4/9) is within run noise of full support (1/9 on rerun) — the
  support-dial claim is DOWNGRADED to suggestive. Clean signals: effort-low = 0 in every
  run; GPT-4.1 = 0 and o4-mini = 0 at every setting; construction = 0 everywhere.
- Construction hard-25: o3 0/25 (23 entail-but-collapse, 2 consistent-but-weak; E's NOT
  persisted by old runner). o4-mini 0/25 (`llm_construct_o4mini_hard25.jsonl`: 10 fail
  both checks, 11 entail-collapse, 4 weak). GPT-4.1 0/25 (3 both / 9 weak / 9
  entail-collapse). These tallies are Claude's classification of each record's FINAL
  attempt — re-derive with own script before publication.
- Pending/optional: vendor diversity (Gemini free tier on cert-63) or delete "rather
  than vendor" from the draft; ~$5-8 of the $20 budget remains after the above runs.
- Worked instances: `paper/certs/saturation/*.sat` = 305 files = 262 AUSTIN_PROVEN + 43
  SATISFIABLE-ONLY REJECTS. Always check `no_finite_model: true` in
  `results/final_status.jsonl` before using one as an exhibit (0a724d3b3544 is a reject;
  0f43eb94ffca, 0553134a10b3, 04ed20a636d7, 149c4489ac1c are safe).

### Reviewer feedback tracker

- Prof round 1 ("why is this a benchmark") → resolved by the capability-first reframe.
- Round 2, point 1 (invention too broad) → resolved (operational definition ¶).
- Point 2 (discovery connection too generic) → resolved (mirror v4 + toy + failed +
  worked-instance figures).
- Point 4 (construction verification unclear) → drafted (channel rewrite, to merge).
- Point 5 (more models/analysis) → partially resolved (weak-model runs, repro); vendor
  diversity open.
- Point 3 (hard-tier meaningfulness / human validation) → OPEN. Planned answer:
  provenance, not surveys — the hard tier contained ETP's open problems, and the pipeline
  settled one (12857/33436); two sentences in Discussion.

### Mechanical sweep (do once, at the end)

Em-dashes: " - " → "---" (intro ¶2, ¶7; method admissibility ¶, presentation ¶,
recursive ¶; contribution bullet 3). Bullet 3: "proof\citep" missing space. Equation (1)
needs terminal period. "proved/proven" → pick one. Line ~320 placeholder cites →
`mccune2003mace4`, `claessen2003new`. "A law counts as resolves" → "resolved".
Verify labels: fig:introduction ↔ Figures/fig_intro_mirror; tab:properties ↔ tab_gap.
references.bib verification pass. Confirm no ETP-public seed laws in cert-63 / hard-25
(needed for the unpublished-instances claim).
