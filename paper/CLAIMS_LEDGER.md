# Claims ledger — what we can say, and how strongly

Every load-bearing claim in the paper, tagged by status so the wording stays honest.
Status key: **[THM]** proven/theorem · **[EMP]** measured, scoped to what we tested ·
**[BG]** background citation, not load-bearing · **[AVOID]** an overclaim to not make.

## Per-instance guarantees (proven, per admitted law)
- **[THM] No nontrivial finite model.** Each admitted law carries the (i)-certificate:
  a subterm containing every x makes x↦T injective ⇒ on a finite carrier surjective ⇒
  forces x=y. Sound but INCOMPLETE — laws it can't certify are discarded, not admitted.
  (Specialisation of Infinox.) Scope: only certified laws are in the corpus.
- **[THM] Dichotomy.** An admitted law is trivial XOR has an infinite nontrivial model.
  DETERMINACY comes from excluded middle, NOT from the filter. (Do not say admissibility
  "makes" the answer determinate — it only rules out the finite-nontrivial case.)
- **[THM] Accepted answers are correct.** Lean kernel-checks a proof of a fixed generated
  goal, axiom footprint ⊆ {propext, Quot.sound, Classical.choice}. Sound autochecker.

## General consequences (proven)
- **[THM] No Austin solution is an arithmetic formula (descent).** If `op` is polynomial/
  affine over ℤ (or ℤ^k, or ℤ/n), the law holds as an identity that survives reduction
  mod 2 ⇒ a nontrivial FINITE model ⇒ contradicts admissibility. So an Austin model cannot
  be a memorized/pattern-matched formula — provable backing for the creativity claim. Also
  ⇒ the affine autoformalizer is empty for Austin (its 0/60 is an artifact, NOT an LLM
  number); and 1593/hard2_0051 (ZMod/ℤ-module) are NOT Austin. See TASK_AND_JUDGING.md.
- **[THM] Finite-model finders provably fail.** Mace4/Paradox cannot succeed on admitted
  laws (no finite model exists). This is WHY excluding them is principled, not a gap.
- **[THM] Trivial side is semi-decidable.** L ⊨ x=y is a first-order consequence; a
  complete proof search confirms it whenever it holds.
- **[BG] Equational entailment is undecidable in general** (Baader–Nipkow 1998). Background
  only, softened ("in general", "can be expected"). Does NOT prove any specific law is
  unsolvable, and is NOT load-bearing — the deductive-vs-constructive asymmetry carries it.

## Empirical results (measured; scope = the methods/budgets we ran)
- **[EMP] The hard tier resists the portfolio.** The 8-config portfolio (Vampire 5.0.1 ×5,
  E ×2, Twee 2.6.1) at up to 600s leaves the hard-tier residual unresolved. Say "the
  strongest automated provers we assemble," NOT "no automated method."
- **[EMP] Method-bound, not compute-bound.** Flat budget curve (3/120 at 30s, 0 higher) +
  bimodality (Austin models saturate in a median 0.1s or diverge) + retry (3.7% convert,
  all trivial contamination, 0 new models). Scoped to the tested methods.
- **[EMP] Automated construction succeeds for SOME.** Saturation built 262 Austin models
  during construction; the full sweep finds additional Twee-only Austin models. So "automation
  cannot construct" is FALSE — it's the hard-tier RESIDUAL that resists. (See sweep.)
- **[EMP] Construction diversity.** 262 Austin laws → 195 classes, decided completely (0
  inconclusive: 33,936 separated + 255 proven-equivalent). Cross-class model transfer 0.25%;
  mutual transfer = 255 = exactly the equivalence pairs. Classes are construction-distinct.
- **[EMP] Renewability.** New Austin classes per order: 11 / 24 / 93 / 67 (cum. 195), still
  growing. CAVEAT: raw counts confound difficulty with how much we generated; normalise to a
  rate (classes per thousand extensions) before quoting.

## Case study 12857 / 33436
- **[THM/VERIFIED] Genuinely open in ETP.** Both are in Table 2 of the ETP order-5 chapter
  (`reference/equational_theories/blueprint/src/chapter/order_5.tex`, line ~85), a table of
  order-5 laws ETP proved have *only trivial finite models* but for which the *existence of
  an infinite model was left unresolved*. So "open" = ETP's finite-model methods couldn't
  decide Austin-vs-trivial — exactly the question ALPS answers. NOT in the implication
  `unknowns_*` lists or `Austin_implications.txt` (their openness is single-law infinite-model
  existence, not an implication), which is consistent.
- **[CAVEAT] They are DUALS of each other** (paired in that table; mirror forms). Resolving
  one resolves the other, so it is ONE open case up to duality. Say "an order-5 law and its
  dual," NOT "two independent problems."
- **[EMP] Confirmed Austin two ways** (Twee CounterSatisfiable + Vampire saturation
  Satisfiable); models non-vacuous (27/27 rules fire, x=y refuted).
- **Attribution:** resolved by AUTOMATED saturation-as-model in our pipeline — answers ETP's
  open infinite-model question; a pipeline demo, NOT a claim to beat the baseline and NOT
  hard-tier.
- **Lean cert of these particular rewrite-models is PENDING** ground confluence (companion
  paper); algebraic models (affine, etc.) are Lean-checkable today.

## Judging (multi-channel, 2026-07-17)
- **Verification is not Lean-only.** TRIVIAL side = Lean proof (kernel + axiom allowlist).
  AUSTIN side = solver proposes a presentation `E`; Vampire certifies `E ⊢ law` + `E ∪ {a≠b}`
  saturates. A certificate from any trusted checker (Lean/Vampire/Twee) counts. Say "machine
  certificate," not "Lean proof," when speaking of the construction side. Canonical:
  TASK_AND_JUDGING.md.
- **[EMP-scope] No verified LLM solve exists yet.** All recorded "solves" were the automated
  engine (used_llm=False), trivial side, old implication format. Do NOT claim an LLM
  construction result until llm_trivial.py / llm_construct.py produce one on the real machine.

## Overclaims to AVOID
- **[AVOID]** "no automated method solves the hard tier" → "the strongest automated provers
  we test do not," or split it: finite search provably can't (THM) + completion/saturation
  empirically stall (EMP).
- **[AVOID]** "beyond automated reach" as absolute → "beyond the reach of the automated
  methods we assemble" / "method-bound relative to current provers."
- **[AVOID]** "zero models on the hard tier" → the sweep builds a few (Twee-only); say
  "constructs solutions for only a small fraction of the construction side."
- **[AVOID]** "no general construction method exists" → FALSE (greedy/affine/saturation are
  general); the honest claim is per-law tailoring, and it's an Experiments finding.
- **[AVOID]** answer definiteness "from admissibility" → it's from excluded middle.
- **[AVOID]** undecidability as the reason the task is hard → background only.

## Wording that is safe
- "certified to have a solution the portfolio never constructs" (EMP, scoped) ✓
- "no finite-model search can find a solution" (THM) ✓
- "difficulty is bound by method, not budget" (EMP, backed by the flat curve + bimodality) ✓
- "every instance has a determinate answer" (THM, from the dichotomy) ✓
