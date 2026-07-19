# OUTLINE — the benchmark paper (writing skeleton)

> **STALE framing (2026-07-17 pivot):** "Lean as the single arbiter / an answer is a Lean proof"
> throughout this file is superseded. Judging is now MULTI-CHANNEL — TRIVIAL side = Lean proof,
> AUSTIN/construction side = solver proposes a presentation `E` and **Vampire** certifies it (no
> Lean construction path exists yet; no Austin model is arithmetic — descent theorem). Canonical:
> `TASK_AND_JUDGING.md`. Read section content for structure, not for the judging specifics.

Section titles in standard-AAAI shape (Intro / Related / Method / Experiments /
Discussion / Conclusion). The benchmark design lives as subsections of the "Method"
section (§3), which is the slot a standard reader parses as the contribution. Each bullet
is a point to hit; the description says what it must land. `[NAME]` = the benchmark's
name if we give it one.

**The four selling points, referenced throughout:** (V) verifiable — machine-checked
Lean judge; (N) non-vacuous — every instance certified answerable; (C) contamination-free
& renewable — a public generator mints fresh, previously-nonexistent instances; (M)
method-bound — difficulty is the deductive-vs-constructive asymmetry, not compute.

---

## 1. Introduction
- **The motivating gap.** ETP is verifiable but *uniform*: one strategy (ATP proof search
  + finite model builder) resolves 22M implications, so it measures execution, not
  construction. A benchmark a single method scores ~100% on cannot measure synthesis.
- **The move.** Isolate the sub-family where that strategy is *provably* inapplicable —
  Austin laws (infinite models, no nontrivial finite one; order ≥5, finite search empty by
  theorem) — extend past the order ETP enumerated, and pose a two-sided task.
- **The four features, stated plainly** (V/N/C/M above). These are the differentiators
  vs. other AI-for-science benchmarks; the body cashes each one.
- **The formal hook.** Trivial is deductive (search finds it); Austin requires
  construction (build the object, search may never find it). That asymmetry is what an
  AI-for-science benchmark should test.
- **Contributions list.** (i) the two-sided task + certified answerability; (ii) an
  order-≥6 corpus with a public generator; (iii) a machine-checked Lean judge; (iv) a
  strong automated baseline the hard tier is defined against, shown method-bound; (v) two
  order-5 ETP-open cases confirmed Austin. Future work: the infinite-model formalisation.

## 2. Related Work
- **AI-for-science / reasoning benchmarks.** Position against math + science benchmarks,
  especially the verifiable-reward line; emphasise the *contamination* problem (static
  sets leak into training) that our generator sidesteps. This is where (C) earns its keep.
- **The Equational Theories Project.** Order ≤4 fully enumerated; order-5 chapter (106
  trivial-finite-model laws, 10 Austin, 96 open). The blueprint defines "Austin law"
  (§5/§20) — cite it as the source of the term.
- **Lean & interactive theorem proving.** Why Lean is the arbiter; ETP is itself a Lean
  project, so the format is native.
- **Automated theorem proving & completion.** Superposition, Knuth-Bendix / unfailing
  completion, the SZS ontology — the machinery the baseline is built from.
- **JRS (Janota–Rawson–Schulz), the closest prior work.** State plainly what it does
  (saturation as an explicit, certifiable model) and how ours *differs*: we fix the target
  to Eq2, restrict to certified-no-finite-model laws, go past order 5, and turn the
  construction into an AI-for-science *benchmark* rather than a prover case study. Honest
  debt, clearly bounded — this paragraph is where a reviewer checks we know the field.
- **Infinox.** Our admissibility prover is a specialisation of its finite-unsatisfiability
  method; credit it.

## 3. The [NAME] Benchmark   ← the "Method" section

### 3.1 Problem Formulation
- **Definitions.** Magmas, an equational law $x = T$, the fixed target $\mathrm{Eq}2:x=y$,
  and $L \models x=y$ meaning every model is trivial. Keep it tight; these open the section.
- **Admissibility certificate.** Each instance carries a machine-checked proof of *no
  nontrivial finite model* (the (i)-prover; Infinox specialisation). This is the admission
  ticket, not a result — it is what makes the task well-posed.
- **The dichotomy.** For admissible $L$, exactly one of trivial ($L\models x=y$) or Austin
  (nontrivial, necessarily infinite model). One-line proof from admissibility +
  completeness.
- **The asymmetry (M) and non-vacuity (N).** Trivial is r.e. (deductive, search-complete);
  Austin is co-r.e. (constructive, no complete method). Neither *negative* inference is
  available — this is why the hard tier resists search. And the certificate + dichotomy
  make every instance provably answerable: not a wall, not an open-problems list.
- **The two-sided task.** Exhibit a Lean-verified model, or prove $L\models x=y$. State
  that solvability is *not* a design criterion; hardness is relative to a named baseline.

### 3.2 Answer Verification  (feature V)
- **Lean as the single arbiter.** An answer is a Lean proof of a generated goal; accepted
  iff the kernel accepts it and its axiom footprint is within a fixed allowlist.
  Format-agnostic: nothing about the model's *shape* enters the judge.
- **The generated goals.** `AustinGoal` / `TrivialGoal`; the nontriviality clause forces
  two distinct elements while keeping the statement finiteness-free.
- **The sandwich + the safeguards.** Header/body/footer forces `solution` to the exact
  generated type; textual gate (sorry/admit/native_decide/axiom/metaprogramming/
  redefinition) + the closed axiom allowlist. Name the shadowing attack as the thing the
  design defeats — good for a figure.
- **What's checkable today.** Algebraic models via the oracle (the mod-17 example);
  saturation/rewrite models need ground confluence of ordered rewriting, reduced to a
  single open lemma — framed as the companion paper, explicitly *not* required for the
  judge to be sound.

### 3.3 Corpus Construction  (features C, and the honest counting)
- **Generation.** Extend a known Austin law by one operation (~500× yield vs random), a
  cheap n≤3 screen, then the classifier. The admissibility filter runs before anything
  expensive.
- **Distinctness — quote classes, not laws.** ≥26% equivalence collapse (262 → ≤195) by
  prover-free model-based separation (1123/1128 pairs); all observed merges are
  seed↔its-own-extension → dedupe at generation. Upper bound, shrinks with compute.
- **Contamination-free (C), with renewability as the mechanism.** Order ≤4 is public and
  order-5 is a published table, so we ship order ≥6: instances that did not exist before
  we generated them, hence unseen by any model's training. The generator is the artifact;
  seeds and dates are recorded. Durability rate = *classes per thousand surviving
  extensions*, not raw survivors.

## 4. Experiments

### 4.1 Baseline Portfolio (setup)
- **The portfolio.** 8 configs — Vampire 5.0.1 (5 modes, KBO/LPO, proof + saturation), E
  (proof + saturation), Twee 2.6.1 (unfailing completion) — over the ladder
  30/60/120/300/600 s. Why both proof-search and saturation: the two task directions are
  found by different machinery.
- **Reproducibility.** Pinned versions/flags in a container, SZS-status verdicts, a
  known-answer self-test gates every run.

### 4.2 The Method-Bounded Frontier (the core result)
- **The flat curve.** 3/120 resolve at 30 s, 0 at every higher budget (Table). 20× the
  compute buys nothing → the tier is bound by method, not time. Report the curve, not a
  single timeout, so the judgment is checkable.
- **Zero new models.** 0 Austin, 11 trivial — every resolution is *contamination* the
  portfolio sheds, made harmless by the two-sided task. The construction side is untouched.
- **Corroboration.** The 20s→300s retry: 3.7% convert, 0/216 → Austin.
- **Not one prover's blind spot.** Twee completes 12857 (357 clauses for Vampire) in
  seconds yet resolves no tier law the others miss — the "Vampire-bound not method-bound"
  alternative is tested and ruled out.

### 4.3 An LLM Baseline
- **A fair-effort, non-exhaustive LLM attempt** on a sample of the hard tier via the
  two-sided task, answers driven through the judge. Expectation: ~0 verified models — which
  *reinforces* the difficulty claim and lets the paper honestly say "and current LLMs."
  Keep it modest and clearly scoped; it is a baseline, not the headline.

### 4.4 Case Study and a Climbable Gradient
- **Two ETP-open cases closed.** 12857, 33436 confirmed Austin two independent ways
  (Vampire saturation + Twee), models computable and non-vacuous. **Position carefully:**
  these are *not* hard-tier (the portfolio resolves them) — their job is to show the
  construction+verification pipeline works end-to-end on literature-open problems, and that
  neither is a plain TRS (motivating the companion formalisation). Do *not* frame as
  beating the baseline.
- **A few hard-tier laws solved by hand.** Algebraic models we find that the portfolio
  does not, Lean-verified. This is the evidence the frontier is *climbable* — footholds a
  human finds and automated search misses — which turns "everything scores zero" into "here
  is the gap the benchmark measures." Highest-leverage item for the main-track case.

## 5. Discussion and Limitations
- **Undecidability deliberately not claimed.** The deductive/constructive asymmetry
  suffices; durability rests on the generator, not on an undecidability theorem we do not
  prove.
- **Hard-tier collapse unmeasured.** No saturations there → the equivalence census is
  prover-only and expensive; reported for `AUSTIN_PROVEN` only.
- **Ground confluence open.** Saturation-derived models not yet Lean-certifiable (algebraic
  ones are); this is the companion paper, and it is why 12857/33436 are shown via the
  computable model rather than a Lean certificate.
- **Sample vs. membership list.** The 120-law curve is sound for a rate; the definitive
  hard-tier list needs the full sweep.
- **(i)-prover vs Infinox** not yet benchmarked head-to-head.

## 6. Conclusion
- Recap the four features, cashed. Restate the open challenge the benchmark poses:
  *construct where deductive search cannot*, on a renewable, contamination-free,
  machine-verified family. Invite the community to climb it.

---

## Decisions still open
- **Name the benchmark?** §3's title and every "our benchmark" read better with one.
- **LLM baseline scope** — which model(s), how many laws, how many attempts. Keep modest.
- **How many hand-solved hard-tier laws** for §4.4 — two or three is enough; depends on
  what's gettable.
