# PAPER_PLAN — benchmark design

Supersedes the pivot plan in `attic/`. Read `HANDOFF.md` for state, `HISTORY.md` for
the wrong turns. This file answers one question: **what must an instance do, and what
must we build, for the measurement to mean what the abstract will say it means.**

Written 2026-07-09.

---

## 0. Freshness check (done, 2026-07-09)

Before investing in Phase B. Our `reference/equational_theories` snapshot is at
upstream `d612bc0`, **2026-06-14** (Kothari, #1448). The *live* blueprint at
`teorth.github.io/.../order-5-austin-laws.html` still reports:

- 106 laws with only trivial finite models; **10 Austin (Table 20.1)**; **96 unknown
  (Table 20.2)**; 24 unknown-finite (Table 20.3).
- **12857 and 33436 are both in Table 20.2**, the open set. Confirmed against the
  rendered table, not our snapshot.
- 22818 is in Table 20.1 — so its absence from `o5_status` is our shard bug, not an
  upstream change.

JRS (arXiv:2602.16324) study ETP proper, order ≤ 4. No order-5 saturation campaign is
published. Berlioz–Melliès (arXiv:2601.20759) embed ETP theories in a latent space —
statistical, not constructive, and not a competitor for this task.

**Not verified:** `vlad902/equational_theories@order5`, the branch the blueprint says
holds the working results, could not be fetched. Check it by hand before publishing
any claim about 12857/33436. The Zulip thread linked from the chapter is the other
place a closure would surface first.

Conclusion: the headline is live. Re-run this check immediately before submission.

---

## 1. What an instance must do

Five properties. Each is a filter with a mechanical test; an instance that fails any
of them is not shipped.

**(1) Answerable, provably, before it ships.** The dichotomy — either `L ⊨ x = y`, or
`L` has a nontrivial model and every such model is infinite — holds only once "no
nontrivial finite model" is a *theorem* about `L`. The (i)-certificate is therefore
the **admission ticket**, not a result. No certificate, no instance. Otherwise we
score models on questions that may have no answer.

**(2) Method-bound, not compute-bound.** A compute-bound instance yields to a bigger
timeout. A method-bound one does not, because the answer is not in the method's search
space: finite model search on an Austin law is *provably* empty, and completion may
diverge. This is measurable, not assertable — run the portfolio at
`30 / 60 / 120 / 300 / 600 s` and record resolution per law.

> **Tier definition (the one that type-checks).** A *law* is resolved or not; flatness
> is a property of the *corpus*. So: hard tier = **unresolved at `B_max` under every
> portfolio configuration**. Separately publish the corpus-level budget curve, to argue
> that `B_max` lies past the knee. Do not write "flat in log-budget" of a single law.

**(3) The answer is an object, not a bit.** A yes/no answer gives a coin 50%. The
submission is a model or a rewrite system, and the verifier checks it. This is what
makes the task construction rather than classification.

**(4) Non-retrievable.** Order ≤ 4 is public in full. Order 5's 106 are a published
table. Ship order ≥ 6, generated post-cutoff, seeds and dates recorded. Note that
**our own publication contaminates the tier the day it ships** — see §5E.

**(5) Synthesis-loaded: near the literature, not beyond it.** A law whose model needs
a structure nobody has conceived measures nothing — everyone scores zero. The
instances with signal are those where a *published* construction, generalised or
composed, works, but no single one supplies it off the shelf. Selection should
therefore prefer laws at **small distance** from the covered families, not maximal
distance. Measuring that distance requires the construction suite of §5B½ to exist.

## 2. What looks relevant and is not

- **Solvability.** An instance nobody solves discriminates nothing. An instance
  provably unsolvable is a bug: everything Lean-checkable is findable by proof
  enumeration. Hardness is relative to methods — normal, and sufficient. Corollary:
  the hard tier *needs* instances the best model solves, or we report 0 vs 0.
- **Undecidability of the family.** Buys "for any solver, some instance defeats it."
  Buys nothing about a finite release, which is always exhaustible.
- **Corpus size.** 9,725 is a count of law strings. Classes are the unit. And *rate*
  matters more than size: a generator with nonzero hard-rate is durable at any rate.
- **The novelty of our (i)-prover.** It is a specialisation of Infinox's method
  (Claessen & Lillieström, JAR 2011): enumerate candidate functions with a property,
  ATP as sub-procedure — i.e. our surjectivity encoding. Our `x = C[S(x)]` observation
  (left inverse is syntactic, so injectivity needs neither search nor an ATP call) is a
  real optimisation on this fragment and *not a contribution until measured against
  Infinox*. If Infinox dominates it, the benchmark is unchanged. Admission machinery.
- **Beating the SOTA prover.** The portfolio is a measuring stick. A stronger baseline
  yields a smaller, more defensible tier. **Keeping the baseline weak to inflate the
  tier is this project's main integrity risk**, and it has a twin: keeping the
  *construction* suite weak. See §5B½.
- **Whether the model "understands."** The certificate is the claim.

## 3. The asymmetry to state up front

`TRIVIAL`, `HAS_FINITE_MODEL`, `AUSTIN_PROVEN` are machine-checked facts. Hard-tier
membership — "no completion prover terminated" — is an **absence**. There is no
certificate for it and in general there cannot be. The one set the paper is built on
is the only set defined by effort rather than by proof.

That sentence goes in the paper, not in a footnote. It is precisely *why* the baseline
portfolio must be strong, named, versioned and published, and why durability rests on
shipping the generator rather than on any impossibility claim.

## 4. Two baselines, both of which must be strong

| | measures | current state |
|---|---|---|
| **prover portfolio** | can existence be decided by automation? | one prover, one ordering — indefensible |
| **construction suite** | can a model be *built* by a known recipe? | two builders — indefensible |

The second is the one we have been ignoring. `order6_grade.py` implements
translation-invariant and greedy. **Neither is prior art — both are ours.** So
`BENCHMARK GOLD: 4` currently means "our two builders failed," which is the same class
of claim as "Vampire didn't finish in 20s." An LLM win against that shows the model
beat our code, not the literature.

Before any LLM number means what the abstract will say: implement every construction
family in the literature (Kisielewicz; ETP's chapter 7 — translation-invariant,
greedy, Asterix/Obelix/Dupont, the ad hoc models; linear ℤ[α]; quotients). Expect the
honest cost: **a stronger construction suite shrinks the hard tier.** Do it anyway.

## 5. Phases and gates

### A — Admission
Install Infinox. Benchmark against our (i)-prover on the order-5 corpus; keep the
union, cite the loser. Point the union at the **1,726 `OPEN` laws where `x` recurs in
the RHS** and the 42 `SATISFIABLE_ONLY` (which need only (i)). Every promotion is a
free instance.

> Measured 2026-07-09 on the local corpus: `x` occurs more than once in the RHS for
> **98.2%** of `OPEN` vs **85.1%** of `NO_FINITE_MODEL`. The root-straddle special case
> is 16.1% of `OPEN` vs 0.8% of `NO_FINITE_MODEL` — a ~20× enrichment, so the mechanism
> is right, but it covers only 282 of 1,757 laws. The general blocker is that no single
> subterm carries `x` uniquely, so the syntactic left inverse does not exist and
> injectivity must be proved by search.
>
> **1,726 is an upper bound, and probably a loose one.** A law lands in `OPEN` for two
> different reasons: (a) no tier-1 witness exists, so injectivity needs a real proof —
> this is the Infinox-shaped case; or (b) a witness exists but Vampire could not close
> the query in budget — this needs *compute*, not Infinox. The `x`-recurrence statistic
> does not separate them. Split the class before quoting a yield.

**Gate:** every shipped law carries an (i)-certificate.

### B — Verification

> **Pilot 2026-07-09, and the correction that followed.**
> `bin/vampire -sa otter --show_active on`. Both laws **saturate** (9.4 s, ~8 s) under a
> complete strategy ⇒ a nontrivial model exists. `Definitions and Model Updates` is
> **empty** — no `f₀, f₁` — so the signature-reduct trap does not bite; the only added
> symbols are `sK0, sK1` from the nontriviality axiom.
>
> The active set is **not a plain TRS**: 12857 has 70 of 357 equations with a variable on
> each side absent from the other (33436: 69/351; control 4916: 0/3; unchanged under
> `-to lpo`). **We first read this as a wall. It is not one.** JRS's pre-orderedness
> requirement is on their *printer*, not on the construction. Their Def. 1 rewrites when
> the **ground instance** decreases, `t[σ(l)] → t[σ(r)]` whenever `σ(l) ≻ σ(r)`, and
> unbound variables on the far side "can be mapped to any ground term such that
> `σ(l) ≻ σ(r)`, in practice the smallest constant."
>
> So every equation is usable, in whichever direction decreases the instance.
> Termination is free (`≻` well-founded on ground terms); ground confluence is inherited
> from saturation under unfailing completion. **The models for 12857 and 33436 are
> computable today.** `scripts/ordered_model.py` implements Defs 1–2; measured:
>
> | law | equations | law holds on ground instances | `x = y` refuted |
> |---|---|---|---|
> | 4916 | 3 | 27/27 (rules fired in 27) | yes |
> | 12857 | 357 | 27/27 (rules fired in 27) | yes |
> | 33436 | 351 | 27/27 | yes |
>
> Non-vacuity is checked, not assumed (`HISTORY.md` records us confirming a rule that
> never fired). `x = y` refuted ⇒ the model is nontrivial ⇒ the law is Austin.
>
> **The ordering trap.** Ground confluence transfers only with respect to *the ordering
> the prover saturated under*. Evaluating a KBO saturation with LPO gives normal forms
> that need not be canonical. Certs now carry `% saturated-with:` and `ordered_model.py`
> refuses to evaluate on a mismatch. The table above is KBO-on-KBO.
>
> **What is actually missing** is only an off-the-shelf *certifier*: CSI/TTT2 check plain
> TRSs. And since `answer_spec.py` makes **Lean the arbiter**, CeTA was never on the
> critical path. Hence the sharpened contribution: formalise **ordered rewriting with
> unorientable equations** — JRS's open 43, our ~36% — not the pre-ordered case that
> already has certificates. B¾'s census is now an *argument for* the contribution rather
> than a wall in front of it, and Twee is demoted to a baseline component (§5C).

Pilot **12857 and 33436** end to end before anything scales:
`--show_active on` → orient → CSI → TTT2 → CeTA → **check the two constants normalise
apart** (nontriviality is a separate check; confluence + termination give you *a*
model, not a nontrivial one).

Two traps:
- **Signature.** JRS note Vampire introduces definitions `f₀, f₁, …` to saturate, which
  "cannot easily be read off the saturated set, but are not necessary to define the
  model." The extracted system lives over the *extended* signature. The magma we claim
  is the **reduct to the original operation**. Get this wrong and CSI happily certifies
  a rewrite system for a structure that is not the one in the paper.
- **Completeness.** Verify the saturation came from a complete strategy before trusting
  it. We have this check; keep it.

Then the contribution: **generic Lean formalisation** — Herbrand domain, normalisation
function, well-foundedness of the ordering, confluence ⇒ model. JRS lay out these four
steps and decline them ("quite involved"). ETP is a Lean project. This turns *any*
CeTA-certified system, theirs or ours, into a Lean theorem, and it does not depend on
any of the three gates below.

**Gate:** two laws certified end to end before scaling.

### B¾ — Orientability census (run 2026-07-09), and what it says about the corpus

How many of the 247 `AUSTIN_PROVEN` saturate into a *rewrite system*, i.e. into
something CSI/TTT2/CeTA can certify? Sampled with `bin/vampire -sa otter
--show_active on` at 6–8 s:

| population | n | clean (0 unorientable) | dirty |
|---|---|---|---|
| harvested order-6+ (one-op extensions) | 20 | **20** | 0 |
| order-5 (ETP Tables 1–2) | 11 | 7 | **4** |

The harvested laws are not merely clean — their active sets are **1 to 5 clauses**, and
the modal case is a single clause: the law itself, with **zero critical pairs**. Nothing
to complete, confluence immediate, model free.

The order-5 laws split. 15535 (175 clauses, 52 unorientable) and 30591 (181 / 52) are as
pathological as 12857 (358 / 70) and 33436 (352 / 69). Note the two dirtiest — our
headline laws — did not saturate inside **this census's 6–7 s** budget and are recorded
as `null` here; §B saturated them at 9.4 s and ~8 s with a 35 s budget. No contradiction,
but it means **the dirty fraction is undercounted, not over**.

Also: every law in this table is `AUSTIN_PROVEN`, i.e. its saturation *closed* under a
complete strategy, so `L ∧ sK0 ≠ sK1` is consistent. **A dirty law cannot secretly be
`TRIVIAL`** — a trivial law makes that set inconsistent and can never saturate. The
"dirty ⇒ near-trivial ⇒ contaminated tier" worry therefore cannot apply to 12857, 33436,
15535, 30591. It applies to the laws that *never saturated*: `NO_FINITE_MODEL`. Those are
the hard tier, dirtiness is unmeasurable for them, and the retry's conversion rate is
exactly the measurement of whether they skew trivial.

**SELECTION BIAS — read this before using the table above.** `AUSTIN_PROVEN` means
*saturation finished inside the classifier's budget* (20 s harvest, 120 s curated). A
law whose completion is long and dirty does not get that label; it lands in
`NO_FINITE_MODEL` or `OPEN`. So the harvested population is **selected for clean, fast
saturation**, and "20/20 clean" partly measures the classifier, not the generator.
Follow-up run the same day:

- 4 randomly chosen `NO_FINITE_MODEL` laws: **none** saturate at 18 s. The hard tier
  really is where the slow/dirty completions must be, if they exist.
- One-op extensions of **clean** seed 4916: of 6 sampled, one saturates dirty (95
  clauses, 1 unorientable), one clean, 4 unresolved at 6 s. **Dirtiness is generated,
  not merely inherited from ETP's order-5 laws.** That is the good news for renewability.
- One-op extensions of **dirty** seed 15535: 4 of 6 are provably TRIVIAL at 5 s — the
  trivial-strip lesson from `HISTORY.md`, again.

So the honest version of the census: among laws that saturate *quickly*, dirty is rare.
The fraction of dirty laws among those that saturate **given a real budget** is the
number that matters and is **not yet measured** — it needs the retry-length runs on the
cluster. Do not conclude "the generator only produces the floor" from the table above;
conclude that the classifier's budget hides the interesting cases inside
`NO_FINITE_MODEL`.

Three consequences, and the first one is uncomfortable:

1. **The fallback paper's N is large but cheap.** ~200 certified infinite models sounds
   good until you see that most are zero-critical-pair laws whose model was never in
   doubt. The certifications worth having are exactly the ones we cannot currently do.
   Size the fallback by *dirty* laws certified, not by laws certified.
2. **The generator does produce dirty laws — at an unknown rate.** One-op extension
   inherits the no-finite-model argument, and the *labelled* Austin population is almost
   all zero-critical-pair. But a 6-law sample of 4916's extensions already contains a
   95-clause dirty saturation, so dirtiness is generated. The renewability question is
   therefore quantitative — *what fraction of extensions, given a real budget, saturate
   dirty?* — and it is answerable only with the cluster's long runs.
3. **Evidence for the §5D collapse worry.** 9,725 laws descend from 130 seeds, and their
   saturations look like the seeds'. Structural near-duplication at the level of the
   completion behaviour is what equivalence-class collapse looks like from the outside.

The ~86% prior from JRS (261/304, order ≤ 4, arbitrary `L → E`) does not transfer. On
the population that actually matters — real order-5 laws — it is **~64% clean, 36%
dirty**, and worse at the top.

### B½ — The construction suite
§4. Implement the published families faithfully. Rename `order6_grade.py`.

### C — The prover baseline
E, Twee, Vampire (ground joinability), × KBO weightings × LPO precedences × the budget
ladder. Docker image, exact flags, version number. Hard tier = unresolved at `B_max`
under all configurations, **stated as relative to portfolio v1.0**.

Timeouts as they actually stand today (a referee will check this sentence):
`TMO_FAST=20` applies **only** to the `r1`/`r2` harvest; `o5_status` and `tgt_status`
ran at `TMO_SLOW=120`; the retry runs at `TMO_HARD=300`. The tier is indefensible
because of prover-and-ordering monoculture, **not** because of budget.

**Gate:** the 20s → 300s conversion rate. **RUN 2026-07-09, retry complete
(`scripts/retry_curve.py`).** 294 laws re-classified at 300 s/prover after 20 s:

```
conversion rate                    11/294 = 3.7%
of 216 NO_FINITE_MODEL laws:
    -> TRIVIAL     4  (1.9%)   hard-tier contamination, removed
    -> AUSTIN      0  (0.0%)   hard-tier under-budgeting
unconverted: median 606 s, max 3014 s — they burn the budget, they are not "almost done"
```

**Zero saturations closed at 15× the budget.** The four trivial conversions all landed
by 160 s, well inside the cap: past the knee for *that* direction. So the gate passes —
the hard tier is not merely under-budgeted — with one caveat that must be printed in the
paper: this is **one prover and one term ordering**. "Method-bound" here means bound
relative to `vampire -sa otter` under KBO. That is exactly what the portfolio exists to
upgrade, and it is why the tier must be re-derived against v1.0 before the number ships.

The 1.9% trivial rate is the **hard-tier contamination estimate**, and it is a real
number to quote: the two-sided task (§2) is what makes those laws harmless rather than
unanswerable.

**And a claim of mine this refutes.** I argued the retry "pays twice" — that laws
converting to `AUSTIN_PROVEN` would gain saturations, hence models, hence the cheap
prover-free separations of §5D. Zero converted. The hard tier gains **no models**, so
model-based separation stays unavailable there, and its equivalence census remains
prover-only, one-directional, and expensive. Do not budget for it as if it were cheap.

### D — The unit of counting (run this **before** C)
Not cheap as stated: 3,428 laws is ~5.9M pairs, ~12M prover calls; at 1 s/call on 32
cores that is days.

> **Result, 2026-07-10 — `AUSTIN_PROVEN` collapses by a quarter.** 250-law sample on the
> cluster: **250 laws → ≤188 classes**, 213 proved equivalences. And 188 is an *upper
> bound* (we can only over-split), so the true collapse is ≥25%.
>
> A 48-law pilot the day before gave 48 → 44 (8%) and I read it as "no collapse". That
> was a sampling artifact: the pilot drew 11 order-5 seeds (pairwise inequivalent by
> ETP's own check) plus 39 harvested laws scattered across many seeds, so it contained
> almost no *siblings*. The 250-law draw is dense in siblings — many extensions of the
> same seed — and siblings are exactly what merge. **Collapse scales with sibling
> density, so extrapolating 25% to the full 9,725-law corpus is optimistic, not
> conservative.**
>
> Structure of the merges: mostly a seed and its extensions, all in one class — e.g.
> 22455 `x = (y ◇ (x◇x)) ◇ ((y◇z) ◇ y)` heads a large family, and **33436 itself is
> equivalent to one of its own extensions**. Many merges replace a once-occurring
> variable by a term containing a fresh one (`y ◇ z` ⇝ `y ◇ (z ◇ w)`), which is a
> *syntactic* pattern worth using as a free pre-filter before any prover call.
>
> Consequences: the abstract quotes **classes**, never laws. `seed_dedupe.py` must run at
> generation time — it would have stopped most of these entering the corpus. And the
> fallback paper's N is ~0.75× nominal at best.
>
> Method: cross-evaluating each law in every other law's model (`scripts/equiv_sample.py`,
> prover-free) certified **1,123 of 1,128** pairs inequivalent on the pilot; only the
> survivors cost a prover call. Separations are sound; merges are prover-proved.
>
> But look at *what* merged: every one of the 5 is a **seed ↔ its own one-op extension**,
> e.g. `x = (((y◇y)◇y)◇x)◇(y◇z)` (28770) ≡ `x = ((((y◇y)◇y)◇x)◇(y◇(z◇y)))`. One-op
> extension sometimes produces a law that is *logically equivalent* to its seed. The
> generator must dedupe extensions against their seed, and the corpus count must be
> stated after that dedupe.
>
> Method note: separations are **sound** (a failing ground instance is a counterexample);
> merges were only candidates until the prover proved both directions. We therefore never
> wrongly merge, and 44 is an **upper bound** at an 8 s budget. Sanity: every model
> satisfies its own law (48/48), and no cell hit the step cap.
>
> **This does not settle the hard tier.** `NO_FINITE_MODEL` laws have no saturation,
> hence no model, hence no cheap separations — run `equiv_sample.py --no-models` there
> and pay the prover for every pair. That is still the gate.

**SAMPLE FIRST. The fingerprint is a premature optimisation.** You do not need all 3,428
laws to answer "does the hard tier collapse." Take **250 at random** and run *incremental
union-find against class representatives*: for each new law, try to prove it equivalent
to each existing representative (two calls per pair). Cost is `O(n·k)`, and it
self-terminates — 250 laws giving 240 classes means no collapse, stop; 250 giving 30
means the paper changes, and you knew by lunchtime. A few thousand prover calls, not 12
million. Do this **before** §5C.

Only then, if a full census is wanted:

1. **Fingerprint.** For each law, which of a fixed probe set of ~100 equations does it
   entail (1 s each)? ~343k calls, one pass.
2. **Pairwise only within matching buckets.** Then union-find.

`scripts/fingerprint.py` implements step 1–2. **Its coordinates are Y-only, so it can
only ever over-split** — two equivalent laws land in different buckets whenever one
entailment missed the budget — and over-splitting inflates the class count, the direction
that corrects against us later. With `ordered_model.py` in hand, the probe vector gains
sound **N** coordinates on the hard tier (normalise the probe in the law's own model),
and the fingerprint becomes correct rather than merely fast. Until then it is a
scheduling heuristic, not a measurement. Two further findings from building it:

**The cheap exact invariants are empirically dead.** Sampled finite magmas and affine-ℤ
magmas are exact equivalence invariants and cost no prover time — and measured over 247
`AUSTIN_PROVEN` + 400 `NO_FINITE_MODEL` + 400 `HAS_FINITE_MODEL` laws they are
**all-zero for every law**: one bucket, zero separation. A sampled structure satisfying
a specific 4-variable order-5+ law is astronomically unlikely, and Austin laws have no
nontrivial finite models at all. Sampled-structure fingerprints do not work here. Do
not rebuild them.

**Refutation is the bottleneck, and it is the same bottleneck as §B.** A probe
coordinate can read Y (prover proved `L ⊨ p`) but never a certified N unless we hold a
model of `L` in which `p` fails. On the hard tier every model of `L` is infinite, so the
only such object is the saturation-derived rewrite system — and reading distinct normal
forms as distinct elements is valid exactly when that system is **convergent**, which is
what CSI/TTT2/CeTA certify. So **the equivalence-class count and the countermodel
certification are the same problem.** Without N, buckets can only split classes, and the
class count stays an upper bound that shrinks with compute.

Demonstrated on 4916 (3 oriented rules, 0 unorientable): normalising with fresh
constants refutes `x = y`, `x ◇ y = y ◇ x`, `x ◇ x = x`, associativity and left
projection, and correctly does *not* refute `x = x`. That first refutation is the Austin
property of 4916, prover-free and hand-checkable — modulo convergence. On 12857/33436
the channel is unavailable (287/70 and 282/69 oriented/unorientable).

**Action item for `prove_status.py`:** it never persists finite models — `witness` holds
the (i)-prover's injective subterm, not a magma. Persisting the FMB model for
`HAS_FINITE_MODEL` laws buys the N-channel for free on the easy tiers, where no
certification is needed.

**Direction of error.** Equivalence is semi-decidable in the positive direction only:
if `L ≡ L'` we eventually prove it; if they are inequivalent we may never know. So
unproved equivalences leave classes **split**, and the class count is an **upper
bound** that shrinks with compute. That is the wrong direction for a number in an
abstract — we would be over-claiming corpus size, and the error corrects against us
later. Report it as an upper bound, with the budget attached, and say so in the paper.

**Gate:** if the hard tier collapses to a few dozen classes, this is not a smaller
paper — it is a different one. See §6.

### E — Generator as artifact
Publish `order6_targeted.py` + seeds + dates + the cheap screen. **Dedupe extensions
against their seed at generation time** (`scripts/seed_dedupe.py`): measured on the 48
one-op extensions of 28770, **3 are logically equivalent to the seed** (6.3%), and the
seed's own saturation model separated 40 of the other 45 prover-free. The three dropped
all replace a once-occurring variable with a term containing a fresh one. Left in, this
inflates the corpus systematically and scales with the harvest.

The durability number is **not** "fraction of one-op extensions surviving portfolio
v1.0" — survivors may be duplicates. It is:

> **equivalence classes per thousand extensions surviving portfolio v1.0**

which composes D with E and is the only version of the rate that means what we want.
Rolling held-out mint, dated after evaluated models' cutoffs; scores reported on the
fresh mint.

### F — The eval

> **VERIFICATION IS CLOSED (2026-07-10).** `answer_spec.py --selftest --lean-dir .`
> passes on the cluster: Lean compiles the reference proof against the *generated*
> statement, the shadow/`sorry`/`axiom`/`native_decide` gates reject, and the axiom
> footprint is inside `{propext, Quot.sound, Classical.choice}`. The judge is real, and
> minimum-acceptable item 1 is done. What remains is *coverage* — how many model shapes
> a submitter can push through Lean — which is what §5B's formalisation widens.

**Tool access is pre-registered, or the measurement is void.** If the model may call
Twee or Vampire, then on a hard-tier law it can run the portfolio at 10× our budget and
win. That is a verified solve that measures nothing — the same instance falling to the
same method with more compute.

| resource | allowed? |
|---|---|
| construction suite (§B½) | **yes** |
| Lean / CeTA / CSI / TTT2 as *checkers* | **yes** |
| saturation provers (Vampire, E, Twee) | **no** |
| self-verification loop against the checkers | **yes**, report compute |

**And the flip side:** after any LLM solve, re-run the portfolio at 10× on that law. If
it falls, say so. That is the honest analogue of what happened to the finite band
(`attic/finite_regime/`), and a reviewer will ask.

**Answer-channel parity.** The baseline and the model must emit the *same* certificate,
or "portfolio scores 0" is a category error rather than a zero. The greedy builder
emits a domain-verified partial magma — it cannot certify a solve on the two-sided
task, so it cannot score. Every baseline component either outputs a Lean model, a
CeTA-certified rewrite system, or a proof of `L ⊨ x = y`, **or it is excluded from
scoring and reported as a heuristic**.

Report both cells: `M \ N` (model solves, portfolio doesn't) and `N \ M`. If the model
only wins where the portfolio wins, there is no synthesis, and that is a finding.
Pre-register the metric before the first LLM call so the tier cannot be tuned to
flatter the result.

## 6. Three gates can each end the benchmark framing

- **D collapse** — 3,428 → forty classes.
- **C's budget curve** — the frontier was under-budgeted.
- **Property (5)'s wall** — the hard tier is hard because it is *far* from every known
  family, so nothing scores.

That is good design: each gate is a cheap experiment that can kill an expensive build.
It also means **P(all three pass) is not high**, and both cheap diagnostics (D, and the
budget curve from C's gate) are available this week.

**If (5) walls:** minting instances one generalisation-step outside our suite changes
the claim from "beyond all known automated methods" to "one step beyond the suite we
wrote" — interpolation over our own recipe, not synthesis. Weaker, still publishable.
**Pre-register it as a fallback now**, so it is not discovered as a rationalisation
after the wall shows up.

**The fallback paper**, which depends on none of the three:

> A generic Lean formalisation of saturation-derived infinite models — Herbrand domain,
> normalisation, well-foundedness, confluence ⇒ model — turning CeTA-certified rewrite
> systems into Lean theorems, plus N closed cases from ETP's open Table 2.

It is real, it is the thing JRS explicitly left on the table, ETP is a Lean project,
and it is Phase B, which we were going to build anyway. Decide now that this is the
floor, and the benchmark is upside.
