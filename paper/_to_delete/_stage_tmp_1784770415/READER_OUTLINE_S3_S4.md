# Reader-state outline — §3 Methodology & §4 Experiments

Written 2026-07-19. Companion to `PAPER_HANDOFF.md` / `TASK_AND_JUDGING.md` /
`CLAIMS_LEDGER.md`. Every paragraph is specified by the reader's **In** state (what they
believe/expect walking in), the **Move** (what the paragraph does), and the **Out** state
(what they must believe walking out). Guardrails cite the claims ledger. Figure/table
anchors are placed where the reader needs them, not where the floats are convenient.

Ordering follows the 2026-07-18 decision: **§3.1 task → §3.2 corpus → §3.3 verification.**
Rationale from the reader's side: after the task is posed, the next question a reviewer
actually asks is "do 10,000 such laws really exist, and are they distinct?" — existence
before grading. Verification then closes §3 so the section ends on "and all of this is
checkable by machine," which is the note §4 opens on.

---

## The one-sentence story of each section

- **§3:** *This task is well-posed (certified dichotomy), the instances are real,
  distinct, and endlessly mintable (extension engine + funnel), and every answer is graded
  by a machine certificate matched to its side (Lean / ATP).*
- **§4:** *Automation solves a floor and then stops — the residual is bound by method, not
  budget; current LLMs [don't move it / climb only the easiest rungs under support]; yet
  the pipeline settles a case the literature left open, so the frontier is real, answerable,
  and worth climbing.*

The two stories interlock: §3 proves every instance HAS an answer; §4 shows nobody can
FIND most of them. That gap — determinate but unreached — is the benchmark's value
proposition, and every paragraph below either builds it or defends it.

---

## §3 The Austin-Law Proof-Synthesis Benchmark

Reader walking in from §1–§2: believes infinite construction is the shared frontier of
reasoning models and provers; has met "Austin law" informally; knows saturation, ETP,
Infinox, JRS from Related Work. Their standing skepticisms, each answered by one
subsection: (a) "is this an open-problems wall dressed as a benchmark?" → §3.1;
(b) "are the 10k instances real, distinct, novel?" → §3.2; (c) "can you really grade an
infinite object, and can the grader be gamed?" → §3.3.

### §3.1 Problem Formulation
*(anchor: the two-sided task schematic — law → construct-model / prove-trivial → verified)*

- **¶1 — definitions.**
  In: intro-level, informal grasp of magma/law/trivial.
  Move: fix the formal vocabulary once — magma, carrier, law $x = T$, order, satisfies,
  trivial magma; the question "does $L$ entail $x=y$ or admit a nontrivial model?"
  Out: reader can parse every later formula; no new claims made. Keep tight (Eric's
  define-then-explain voice); this paragraph earns nothing except precision.

- **¶2 — admissibility.**
  In: reader knows some laws have no nontrivial finite model, but not how WE know.
  Move: define admissible = carries a machine-checked proof of no-nontrivial-finite-model;
  sketch the (i)-argument (subterm containing every $x$ → injectivity → finite surjectivity
  → collapse); state sound-but-incomplete, uncertifiable candidates discarded; credit
  Infinox as the general method.
  Out: reader believes NO finite-model law can be in the corpus — admission requires a
  proof, not a failed search. This is the load-bearing trust anchor for everything after.
  Guardrail: it's a ticket of admission, not a contribution claim [THM].

- **¶3 — dichotomy and well-posedness.**
  In: reader accepts the certificate; may still file the task as "open problems."
  Move: the dichotomy — admissible $L$ is trivial XOR Austin (nontrivial ⇒ infinite);
  determinacy comes from excluded middle, admissibility only removes the third case.
  Out: reader believes every instance has exactly one right answer; "unanswerable
  instance" is off the table. The benchmark is a set of questions, not a wall.
  Guardrail: do NOT say admissibility "makes" the answer determinate [AVOID].

- **¶4 — the asymmetry (what the benchmark measures).**
  In: reader accepts well-posedness; doesn't yet see why one side is special.
  Move: trivial side is a first-order consequence — complete search confirms it whenever
  true; Austin side has no such guarantee — a failed derivation is not a model;
  undecidability cited softly as background only. Climax: resolving the Austin side means
  INVENTING a structure tailored to the law.
  Out: reader can state the thesis themselves: deduction is search, construction is
  synthesis, and this benchmark isolates the synthesis. This paragraph is the §3 payoff;
  everything before it was setup.
  Guardrail: undecidability is never load-bearing [BG]; no "no general method exists"
  claim [AVOID] — per-law tailoring is an Experiments finding, not a definition.

### §3.2 Corpus Construction
*(anchors: methodology fig (a) extension engine; fig (b) Sankey funnel; density figure;
distinctness/classes table)*

- **¶1 — generation by extension.** *(fig a)*
  In: reader believes the task is well-posed for A law; asks "where do thousands come
  from?"
  Move: extend a seed Austin law by one operation ($v \to v \diamond w$); inheritance of
  the no-finite-model mechanism explains the yield; random sampling stated dead in one
  sentence (rarity + redundancy). Note the re-seeding loop: confirmed Austins seed the
  next order.
  Out: reader understands the corpus is manufactured, not curated — and that the same
  machine keeps running (plants renewability for ¶4).

- **¶2 — the funnel.** *(fig b — narrate the paragraph DOWN the figure)*
  In: reader knows candidates exist; asks "how do you keep junk out?"
  Move: screens cheap-to-expensive: fast triviality strip → admissibility certificate →
  full-portfolio classification into Trivial 3,080 / Austin 262 / hard tier 4,141, with
  discards peeling off (finite-model 1,042, uncertified 1,906 + 43) from the 10,474 pool.
  Present classification as ONE step ("classified by the full portfolio") — the hard tier
  is the residual of the full portfolio, not of one prover.
  Out: reader can reproduce the funnel from the figure and trusts each number has a
  certificate or an explicit "discarded" label. Numbers marked provisional until the
  sweep completes.
  Guardrail: hard tier defined against the FULL portfolio (sweep found Twee-only models;
  the old "Vampire residual" framing is dead).

- **¶3 — distinctness.**
  In: reader's next objection: "extensions of few seeds = near-duplicates."
  Move: equivalence census on the 262 proven-Austin laws — model-based separation decides
  33,936 pairs prover-free, 255 proven equivalent, 0 undecided → ≤195 classes (~26%
  collapse); we report classes, not laws. Optional one-two sentences: cross-class model
  transfer is 0.25%, so classes are construction-distinct, not just logically distinct.
  Out: reader believes the corpus size is honestly counted and the redundancy objection is
  pre-empted with a complete, checkable census.

- **¶4 — renewability and contamination.** *(density figure)*
  In: reader believes the current corpus is real; asks "does the well run dry, and why is
  'contamination-free' more than a slogan?"
  Move: Austin DENSITY per 1k screened rises with order (20.5 / 24.4 / 25.4 at orders
  6/7/8); new-class yield persists (flat, ~16–19/1k — say "persists," never "rises");
  order ≥6 laws did not exist before generation, seeds and dates recorded → evaluation can
  always outrun any training cutoff.
  Out: reader believes renewal is measured, not asserted — and that contamination-freedom
  follows from the generator, not from secrecy.
  Guardrail: exclude order 5 from the curve (ETP-given, not our draw); density not raw
  counts (raw order-8 dip is a screening-volume artifact).

### §3.3 Answer Verification
*(anchor: optional judge schematic / worked-certificate listing)*

- **¶1 — the principle: a certificate for each side.**
  In: reader believes the corpus; final skepticism: "grade an INFINITE object? by machine?"
  Move: a solved instance is a verified fact, no human in the loop; the two sides need
  different machinery, so the judge is two-channel: TRIVIAL = a Lean proof, kernel-checked;
  AUSTIN = the solver submits a MODEL as a finite presentation $E$, certified by an
  automated prover. State the trust base plainly: Lean kernel on one side, ATP saturation
  (cross-checkable by a second prover) on the other — the same trust base the corpus
  labels already rest on.
  Out: reader has the map of the two channels and doesn't feel a bait-and-switch when the
  Austin channel turns out not to be Lean.
  Guardrail: this is the multi-channel pivot — never say "checked by Lean" of the
  construction side (current §3.2 tex text violates this; rewrite).

- **¶2 — the trivial channel.**
  In: reader wants to see one channel concretely.
  Move: generated `TrivialGoal` (state it); header/body/footer sandwich forces the exact
  statement; textual gate + closed axiom allowlist; accepted ⇒ correct by construction.
  Out: reader believes the deductive side is airtight and gameproof — framed as a sound
  autochecker, not anti-cheating theater.

- **¶3 — the construction channel.**
  In: reader now expects the Austin analogue and suspects it's the hard part.
  Move: solver proposes a presentation $E$ (equations over $\diamond$ — not the law
  itself); two prover queries: (A) $E \vdash L$ (refutation proof — the strong certificate)
  and (B) $E \cup \{a \neq b\}$ saturates (nontrivial model of $E$ exists,
  completeness-guarded). Both pass ⇒ a nontrivial model of $L$ exists ⇒ Austin. Then the
  self-policing: $E = \{L\}$ gains nothing (B becomes the bare saturation that diverges);
  a collapsing $E$ passes (A) but fails (B).
  Out: reader believes the construction channel is sound AND ungameable, and — key —
  that submitting $E$ still requires the solver to have *found the model*; the harness
  only checks it.

- **¶4 — scope, honestly (why not Lean everywhere).**
  In: reader may ask "why not one arbiter?" — the answer must feel principled, not
  apologetic.
  Move: two facts close the question. Descent theorem: no Austin model is an arithmetic
  formula (poly/affine over $\mathbb{Z}, \mathbb{Z}^k, \mathbb{Z}/n$ descends mod 2 to a
  finite nontrivial model — contradiction), so the "easy" Lean-checkable family is
  provably empty — which is also provable backing for the creativity claim: the answer
  can't be a memorized formula. And Lean-certifying rewrite-system models needs ground
  confluence of ordered rewriting — reduced to one open lemma, the companion paper.
  Out: reader sees the two-channel design as forced by theorems, not convenience; and
  takes away the bonus: Austin answers are provably non-formulaic.
  Guardrail: descent is a theorem [THM] — state it as one; companion paper framed as
  future work, not a gap in soundness.

---

## §4 Experiments

Reader walking in: sold on the design; now wants evidence. Their questions, in order:
"how strong is the automated baseline?" (§4.1), "is the hard tier really method-bound?"
(§4.2), "what about LLMs — isn't that the point?" (§4.3), "is any of this climbable, or
is it a wall?" (§4.4). §4.2 is the core result; §4.3 and §4.4 are the two halves of the
'not a wall' defense.

### §4.1 Baseline Portfolio (setup)

- **¶1 — the portfolio.**
  In: reader needs to trust that "automation fails" means strong automation.
  Move: 8 configurations — Vampire ×5 (proof + saturation, KBO/LPO), E ×2, Twee (unfailing
  completion, purpose-built for unit equations) — over the 30–600s ladder; two paradigms
  (superposition, completion) because the two task sides need different machinery;
  resolved = any config returns a verdict, direction-aware (a proving-mode saturation is
  never read as a model).
  Out: reader accepts "the strongest automated provers we assemble" as a fair baseline.
  Guardrail: exactly that phrase — never "no automated method" [AVOID].

- **¶2 — reproducibility + the principled exclusion.**
  In: reader wonders about Mace4/Paradox.
  Move: pinned versions/flags/container, SZS verdicts, selftest-gated runs; finite-model
  finders excluded because admissibility PROVES they cannot succeed — the exclusion is a
  theorem, not a choice.
  Out: reader can rerun the baseline and cannot accuse the portfolio of a strawman.

### §4.2 The Method-Bound Frontier (the core result)
*(anchors: budget-ladder table; corpus/composition table if not already in §3.2)*

- **¶1 — what the full sweep resolves (the floor, and the shed contamination).**
  In: reader expects "portfolio solves some, fails on the rest."
  Move: saturation constructs the 262 Austin models in median 0.1s — automation DOES
  construct, when completion terminates; the full-portfolio sweep over the residual sheds
  a small contamination in BOTH directions (a few late trivials; a few completion-only
  models, [FILL exact counts when sweep completes]). The hard tier is what remains after
  all of it.
  Out: reader trusts the tier's definition because we visibly subtracted everything
  automation could do — including the models that would otherwise be a reviewer's gotcha.
  Guardrail: "automation cannot construct" is FALSE [EMP]; the honest claim is the
  residual. Wait for the sweep before freezing numbers.

- **¶2 — the flat curve (method-bound, not compute-bound).**
  In: reader's default explanation is "just needs more time."
  Move: the budget ladder — resolutions at the shortest budget, none after, out to 20×
  per config (3/120 at 30s, 0 at 60–600s); retry corroboration (3.7% convert at 300s, 0 →
  Austin); bimodality (models arrive in ~0.1s or never).
  Out: reader believes compute is not the bottleneck — the STABILITY of the residual under
  more budget and more provers is the finding.
  Guardrail: phrase as stability under added compute/methods, NOT "the portfolio's
  residual resists the portfolio" (circular).

- **¶3 — not one prover's blind spot.**
  In: last automated escape hatch: "maybe Vampire-shaped, not hard."
  Move: two distinct paradigms; Twee solves in seconds instances that run Vampire to
  hundreds of clauses, yet [FILL: on the hard tier Twee adds only the N sweep models /
  nothing beyond]; failure is shared across paradigms.
  Out: reader concludes the difficulty is a property of the laws, not of a tool. §4.2
  closes with the gap §3 promised: determinate answers nobody can reach.

### §4.3 LLM Baseline
*(two branches; the protocol paragraph is identical in both)*

- **¶1 — protocol (fairness first).**
  In: reader arrives asking "did you give LLMs a real chance?"
  Move: pre-registered setting — every model gets the same inputs (law + generated goal +
  scaffold), the judge as a verification oracle with a fixed self-verify budget; the
  support ladder (naked → skeleton → autoformalizer → revealed waypoints) so failure is
  attributable: construction vs. formalization vs. derivation; tool access fixed
  (checkers yes, saturation provers no — else the model just reruns §4.1 at 10×);
  instances stratified by proof length (the trivial side has a measured 2→97-waypoint
  gradient). Rate-limited calls excluded from denominators.
  Out: reader accepts any number that follows as fair — the ladder converts even a zero
  into information.

- **¶2 — results. BRANCH A (some easy-tier solves — hoped):**
  Move: solves appear on the easiest trivial instances and rise with support [and
  reasoning effort]; zero at every rung on the hard tier; report solves-by-rung and
  cost.
  Out: reader sees a climbable gradient INSIDE the benchmark: today's models enter at the
  bottom rung, the frontier stays untouched — the benchmark meaningfully separates
  present from future capability. (Any solve gets the 10× portfolio recheck, reported.)

- **¶2′ — results. BRANCH B (zero everywhere — current data):**
  Move: N laws × M models × all rungs → 0 verified solves; failure-mode breakdown:
  invalid derivation steps even with waypoints revealed (derivation-bound), output
  starvation, granularity mismatch — measured on instances whose full proofs are 2
  lemmas long.
  Out: reader reads the zero as a real capability gap, not a harness artifact — the
  well-posedness certificates (§3.1) and the 2-waypoint floor make "the task is
  impossible/unfair" unavailable. Framed to reinforce §4.2: the same laws resist search
  AND today's models.
  Guardrail: never report the retired L2-affine 0/60 as an LLM number; exclude 429 rows.

### §4.4 Case Study: an Order-5 Law Left Open by ETP
*(anchor: worked-example listing — the law, its presentation E / saturated model)*

- **¶1 — the case and its provenance.**
  In: after two zero-heavy sections the reader needs proof the pipeline produces
  mathematics, not just filters.
  Move: an order-5 law and its dual (12857/33436 — ONE case up to duality), listed by ETP
  among laws with only trivial finite models but unresolved infinite-model existence;
  confirmed Austin by two independent routes (Vampire ordered saturation + Twee), model
  non-vacuous (27/27 rules fire, $x=y$ refuted).
  Out: reader believes the benchmark's machinery settles literature-open questions —
  the instances are real mathematics.
  Guardrail: resolved by the AUTOMATED pipeline — not hard-tier, not beating the
  baseline, and "an order-5 case and its dual," never "two problems" [CAVEAT].

- **¶2 — what the example teaches (and its limit).**
  In: reader wants to know what an Austin answer looks like concretely.
  Move: walk the model at arm's length — the saturated presentation as a term-model
  recipe; note it is NOT a plain rewrite system (unorientable equations), which is
  exactly why ordered rewriting and the confluence lemma matter (callback to §3.3¶4, the
  companion paper).
  Out: reader leaves §4 with a concrete mental image of a solution, a felt sense of why
  these are hard, and the arc closed: well-posed (§3) → unreached (§4.2–4.3) → reachable
  (§4.4).

---

## Cross-cutting checks before drafting

1. §3.2/§3.3 of the CURRENT TEX still say Lean checks both sides — must be rewritten to
   the multi-channel design before any of §3 is polished.
2. Intro ¶8 "constructs no model at all" contradicts the sweep — soften to "resolves only
   a small fraction of the construction side" when §4.2 is drafted.
3. All hard-tier counts (4,141; sweep contamination; Twee-only models) are provisional
   until `baseline_full.jsonl` finishes — draft with [FILL] markers, freeze once.
4. Table anchors: corpus composition (funnel numbers), budget ladder, distinctness/classes,
   [LLM ladder]; figures: task schematic, methodology (a)+(b), density, worked example.
5. Every paragraph above ends on its Out state — if a drafted paragraph's last sentence
   doesn't land the Out, cut or move the trailing material.
