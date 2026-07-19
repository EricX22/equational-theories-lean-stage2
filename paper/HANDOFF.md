# HANDOFF — Austin-law benchmark

> **Read `PAPER_HANDOFF.md` first — it is the current resume file; this one is older (2026-07-09).**
> **Judging pivot (2026-07-17):** the construction side is NOT Lean-verified — no Lean path exists
> (confluence `sorry`) and no Austin model is arithmetic (descent theorem). It is certified by
> **Vampire** (solver proposes a presentation `E`; `E⊢law` + `E∪{a≠b}` saturates). Trivial side is
> Lean. Canonical: `TASK_AND_JUDGING.md`.

Everything a new reader (or a future us) needs: the thesis, what is *proved* vs
merely *observed*, the code that is live, the numbers as of 2026-07-09, the open
question that blocks the paper, and what to do next in priority order.

Companion docs: `PAPER_PLAN.md` (benchmark design: what an instance must do, the
phases and their gates, the fallback paper). `HISTORY.md` (how we got here, including
the wrong turns — several are still traps). Superseded plans and pre-pivot code are in
`attic/`.

**Read this first.** `TRIVIAL`, `HAS_FINITE_MODEL` and `AUSTIN_PROVEN` are
machine-checked facts. **Hard-tier membership is not.** "No completion prover
terminated" is an *absence*: there is no certificate for it and in general there cannot
be one. The one set the paper is built on is the only set defined by effort rather than
by proof. That is why the baseline portfolio must be strong, named, versioned and
published — and why durability rests on shipping the *generator*, not on any
impossibility claim. Undecidability buys nothing here: a finite release is always
exhaustible.

---

## 1. What we are building, and the three criteria

This is an **AI-for-science benchmark**. The thing being tested is whether a model
can take everything known about a problem and *construct something new* — not whether
it can execute a known procedure faster.

Mathematics is the right domain because answers are verifiable. The Equational
Theories Project is *nearly* the right dataset and isn't, for a reason worth stating
precisely: it is not that ETP's problems are decidable (each individual instance
trivially is). It is that **one method solves essentially all of them.** ATP proof
search plus a finite model builder resolves 22 million implications. No synthesis is
required anywhere. A benchmark on which a single uniform strategy scores ~100% cannot
measure construction.

**Austin laws** — laws with infinite models but no nontrivial finite one — are where
that uniform strategy runs out. Finite model search is *provably* empty there, so
one of the two standard tools is not merely slow, it is inapplicable by theorem. The
family exists only at order ≥ 5.

The benchmark must clear three bars. Solvability is not one of them.

### (a) Verifiable

Every answer is machine-checked. Two channels, both real:

- a **concrete algebraic model** (ℤ, ℤ[α], a tree, a quotient) with a Lean proof —
  our existing harness (`scripts/lean_oracle.py`);
- a **term model**: a rewrite system, with confluence checked by CSI, termination by
  TTT2, and both certificates verified by CeTA/IsaFoR. This is the JRS pipeline (§3).

This bar is *not* free, contrary to first impressions. Verifying an **infinite**
model in Lean is genuinely open work — JRS lay out the four steps (Herbrand domain,
normalisation function, well-foundedness of the ordering, confluence) and call it
"quite involved". They do not do it. ETP is a Lean project. This gap is ours.

### (b) Durability (the benchmark must not be exhausted)

Careful with the word "saturation" — it means two different things in this project.
In ATP terminology a prover *saturates* when its clause set closes. In benchmark
terminology a benchmark *saturates* when models max it out. Below, always "durable".

Undecidability alone does **not** buy durability. A benchmark release is a finite set
of instances, and a finite set can always be solved. What undecidability buys is
this: no fixed algorithm decides the whole family, so for **any** solver there exist
instances it fails on. Combine that with an **infinite, public generator** and you
get the real guarantee:

> We can always mint fresh instances that lie outside any fixed method's reach, and
> we publish the generator, not merely the instances.

So durability is a property of the *pipeline*, not of the problem. Concretely: an
instance is hard **relative to a named, published baseline portfolio**. When the
portfolio improves, we re-filter and re-generate. That is honest, it is what every
durable benchmark actually does, and it does not require us to claim that anything is
impossible.

### (c) Contamination-free

ETP enumerated order ≤ 4 (4,694 equations, all 22M implications, results public). Its
order-5 chapter is a table of 57,882 laws, of which 106 admit only trivial finite
models. Order 6 and 7 have never been enumerated by anyone. Our generator produces
them, and the specific laws we ship did not exist before we made them. Seeds are
recorded so any instance can be reproduced and dated.

---

## 2. The task, stated so that every instance is answerable

Earlier framings had a hazard: if we hand a model a law and ask for a countermodel,
and the law turns out to be trivial, the model can never succeed and we score it as a
miss. That hazard is removable, because of a dichotomy we can prove.

For a law `L` with a machine-checked proof that **no nontrivial finite model exists**,
exactly one of these holds:

1. `L ⊨ x = y` — the law is trivial, the implication into `Eq2` is TRUE; or
2. `L` has a nontrivial model, and every such model is infinite — `L` is Austin.

So the benchmark task is **two-sided**:

> Given `L`, either exhibit a nontrivial model (Lean-verified, or a CeTA-certified
> rewrite system), **or** prove `L ⊨ x = y`.

Exactly one answer exists and no instance is unanswerable. A solve in either direction
is a genuine mathematical fact, not a benchmark point. This also removes the
contamination of the hard tier by trivial-but-hard-to-prove laws, which was otherwise
unfixable.

**The two sides are not equally checkable, and saying they are erases our contribution.**

| side | status |
|---|---|
| `L ⊨ x = y` | checkable **today** (ATP proof, Lean-replayable) |
| nontrivial model, concrete algebraic | checkable today for the families we can express (`scripts/lean_oracle.py`) |
| nontrivial model, term/saturation-derived | **not yet checkable in Lean** |

The last row is the four-step construction JRS lay out — Herbrand domain,
normalisation function, well-foundedness of the ordering, confluence — and explicitly
decline, calling it "quite involved." ETP is a Lean project. That gap is the clearest
unclaimed contribution we have. It is *work in the plan*, not a premise of the task
statement. Until it exists, the term-model channel terminates at CeTA, not at Lean.

Note also that confluence + termination give you *a* model, not a *nontrivial* one.
Nontriviality is a separate check: the two constants of the negated conclusion must
normalise apart.

The deterministic baseline resolves the easy tier and, by construction, scores ~0 on
the hard one. That is the measurement.

## 3. Prior art, and the toolchain we should be using

> Janota, Rawson, Schulz. **"Case Study: Saturations as Explicit Models in Equational
> Theories."** arXiv:2602.16324, Feb 2026. <https://arxiv.org/abs/2602.16324>
> (Rawson is a Vampire developer; Schulz wrote E.)

Read it. It costs us one claim and hands us a toolchain.

**What it says.** In the unit equational fragment a saturated clause set *is* a
ground-convergent rewrite system; the Herbrand universe modulo normalisation is an
explicit, possibly infinite model, and ground equations are decided by normalising.
So **where a completion-based prover saturates, the countermodel is not merely proved
to exist — it is extractable and certifiable.** They modified Vampire and E to emit
it. On the ETP: 817 non-theorems found only by saturation, 304 after a longer FMB
run; **196 of those marked finitely unsatisfiable by Infinox**; **261 of the 304
certified confluent + terminating by CSI and TTT2, verified by CeTA/IsaFoR** — 261
fully verified countermodels. The remaining 43 have unoriented equations: model
exists, automated checking not yet known.

**What it costs us.** "Existence is mechanical, construction isn't" is dead as a
headline. Every law where saturation terminates — all 247 of our `AUSTIN_PROVEN` —
has a certifiable construction. Those are the benchmark's **floor**, not its prize.
And our (i)-prover is a specialisation of Infinox's method: Infinox "enumerates
candidate functions with particular properties, using an ATP as a sub-procedure",
which is exactly our surjectivity encoding. Our tier-1 observation — that a law
`x = C[S(x)]` supplies the left inverse *syntactically*, so injectivity needs no
search and no ATP call — is a real specialisation and probably much faster on this
fragment, but it is an optimisation of a known method. Measure it against Infinox;
don't announce it.

**What it gives us.** This is the part worth being pleased about. We have been
hand-rolling tools that exist and are better:

| tool | what it does | use |
|---|---|---|
| **Infinox** (Claessen & Lillieström, JAR 2011) | proves finite unsatisfiability | the (i) filter — probably faster and stronger than ours; benchmark against it |
| **Twee** | unfailing completion, purpose-built for UEQ | the strong baseline; likely saturates far more than `vampire -sa otter` |
| **E**, **Vampire** (ground joinability on) | saturation | the rest of the baseline portfolio |
| **JRS-modified Vampire / E** | emits the rewrite system on saturation | free certified models for the floor tier |
| **CSI** | confluence checking | verification channel for term models |
| **TTT2** | termination checking | verification channel |
| **CeTA / IsaFoR** | certified checking of CSI/TTT2 certificates | trust anchor |
| **TSTP model format** (recently extended) | standard output for finite and infinite models | our answer format |
| their table: `people.ciirc.cvut.cz/~janotmik/stamp` | the 304 / 196 breakdown | cross-check |

**Scope, which is what saves the project.** JRS study ETP proper: operation applied
at most 4 times. **Austin laws require order ≥ 5 by definition.** Their 304
saturation-only cases and our order-5/6/7 population are disjoint. They also study
arbitrary `L → E`; we fix `E = Eq2`, which is what makes "no finite model" a property
of `L` alone and makes the finite-model search provably empty rather than merely
unsuccessful.

**The methodological correction that follows.** Our hard tier is defined by
`vampire -sa otter` alone. Be precise about the budget, because a referee will check
the sentence: `TMO_FAST=20` applies **only** to the `r1`/`r2` harvest laws; `o5_status`
and `tgt_status` ran at `TMO_SLOW=120`; the retry runs at `TMO_HARD=300`. The tier is
indefensible because of **prover-and-ordering monoculture**, not because of budget. A
law that diverges under one term ordering may complete under another, so the baseline
must portfolio over **provers × orderings × budget**: E, Twee, Vampire with ground
joinability, across KBO weightings and LPO precedences, at a real timeout.

State tier membership so that it type-checks: a *law* is resolved or not; flatness is a
corpus-level property. **Hard tier = unresolved at `B_max` under every configuration**,
with the budget curve published separately to argue `B_max` lies past the knee. Do not
write "flat in log-budget" of a single law.

**The construction baseline is the twin of this problem, and it is worse.** See §6.

## 4. Where the numbers stand (2026-07-09, mid-run)

Full corpus, before the long retry, deduped by law:

```
9725 laws
   2895  TRIVIAL            implication TRUE (proved)
    990  HAS_FINITE_MODEL   FALSE, finite (proved)
    247  AUSTIN_PROVEN      FALSE, infinite (proved)
   3798  NO_FINITE_MODEL    (i) proved, existence open
     42  SATISFIABLE_ONLY   model exists, finiteness open
   1753  OPEN               nothing proved

settled (theorem):  4132 / 9725
```

Up to variable renaming **and duality**: `AUSTIN_PROVEN` 247 → **219**;
`NO_FINITE_MODEL` 3798 → **3428**.

**Do not quote these as final.** Four things move them:

1. The retry (300s/prover) converts some `NO_FINITE_MODEL` → `TRIVIAL` and some →
   `AUSTIN_PROVEN`. Both directions come out of the same bucket. The conversion rate
   is the single most important unmeasured number: it tells you whether the frontier
   is real or merely under-budgeted.
2. **Distinctness is not established.** All 9,725 laws descend from 130 seeds by
   one-operation extension, so equivalence classes may be far coarser than duality
   classes. ETP was explicit about this for their 10 (*"Vampire's decision procedure
   also establishes that all 10 Austin laws are inequivalent to each other"*). We
   have not done the pairwise mutual-implication check. **The number that belongs in
   an abstract is equivalence classes, not laws.**
3. The harvest keeps generating (round `r3` seeds off `r2`).
4. The baseline column is broken for 4,062 laws (see §6), which is why
   `BENCHMARK GOLD` currently under-reports.

### The possible headline result — unverified

Eleven `AUSTIN_PROVEN` laws are order-5. Nine are ETP's Table 1. The other two are

```
x = y ◇ ((x ◇ (y ◇ (z ◇ z))) ◇ y)        (12857)
x = (y ◇ (((z ◇ z) ◇ y) ◇ x)) ◇ y        (33436)
```

both of which sit in ETP's **Table 20.2**, captioned *"Trivial finite models, unknown
infinite models"* — the 96 laws where *"no effort was made to build infinite models."*
Confirmed 2026-07-09 against the **live** blueprint, not our snapshot (which is at
upstream `d612bc0`, 2026-06-14): still 10 Austin / 96 unknown, both laws still open.
JRS study order ≤ 4 only. **Unchecked:** `vlad902/equational_theories@order5`, the
working branch the chapter links, and the Zulip thread — a closure would surface there
first. Re-run this check before submission.

If this survives scrutiny it is a stronger claim than any corpus size: **two open
cases closed.** It has not survived scrutiny yet. Neither law is in the
zero-critical-pair class, so their Austin status currently rests on trusting Vampire —
but the fix is no longer "trust harder," it is a recipe: dump the saturated set with
`--show_active on`, orient it, run CSI and TTT2, check the certificates with CeTA, take
the reduct to the original signature, and confirm the two constants normalise apart.
This is also the cleanest end-to-end test of the verification channel, which is why it
comes before any further corpus generation.

Also: 22818 **is** in ETP's Table 20.1, so its absence from `o5_status` (127 rows for
128 laws) is our shard bug, not an upstream change.

Also: ETP's 22818 is **absent** from `o5_status` (127 rows for 128 laws — one shard
didn't emit it). The order-5 pass needs a re-run before any table is published.

---

## 5. Live code

| file | role |
|---|---|
| `scripts/prove_status.py` | the three provers; emits status + witness + cert + baseline. `--selftest <vampire>` runs known-answer controls |
| `scripts/status_report.py` | merges shard outputs (strongest verdict per law), status × baseline, writes `final_status.jsonl` + `gold.jsonl` |
| `scripts/seeds_from_status.py` | select laws by proved status: seeds for the next order, or the unsettled set |
| `scripts/order6_targeted.py` | targeted generation: extend a law by one operation, cheap `n≤3` screen |
| `scripts/order6_grade.py` | the deterministic construction baselines (translation-invariant, greedy). **Misnamed** — it is no longer a grader; rename once no job is running |
| `scripts/rescore_baselines.py` | recompute the baseline column offline (no ATP) |
| `scripts/confluence_cert.py` | ATP-free nontriviality proof via critical pairs. **Currently checks the wrong rule set** — see §3 |
| `scripts/etp_terms.py` | term parsing, TPTP/LADR emitters |
| `scripts/overnight.sh` | the whole loop: classify → harvest → classify → retry → report |
| `scripts/progress.sh` | read-only snapshot of a running job |
| `scripts/lean_oracle.py`, `scripts/setup_atps.sh` | Lean verification; prover install |

`problems/order5_seeds.jsonl` — the 130 order-5 laws from ETP Tables 1–3, committed
so nothing depends on the reference-repo path.

`attic/finite_regime/` — the pre-pivot solver work (22 files), including
`proposer_o3.py`, which is the reference implementation of the OpenRouter call and
self-verify loop worth reusing for the construction task.
`attic/order6_pipeline/` — superseded by `overnight.sh`.
`results/archive/` — pre-pivot result files.

### Reproduction

```bash
nohup bash paper/scripts/overnight.sh > /dev/null 2>&1 &
tail -f paper/results/overnight.log
bash paper/scripts/progress.sh                       # read-only, safe on a live run

python3 paper/scripts/rescore_baselines.py --in 'paper/results/*_status_*.jsonl' \
    --out paper/results/baselines.jsonl
python3 paper/scripts/status_report.py 'paper/results/*_status_*.jsonl' \
    --baselines paper/results/baselines.jsonl \
    --merge-out paper/results/final_status.jsonl --gold-out paper/results/gold.jsonl
```

Knobs: `SHARDS TMO_FAST TMO_SLOW TMO_HARD ROUNDS SEED_CAP S1_MAX..S4_MAX`, and
`R=/tmp/rt` to smoke-test into a scratch results dir.

---

## 6. Known bugs and traps

- **`order6_grade.grade` hard-coded the variables `x,y,z`** and raised
  `KeyError('w')` on every 4-variable law — i.e. on most one-op extensions.
  `prove_status.py` caught it and wrote `baseline="error:'w'"`, silently blanking the
  column for ~4,062 laws including 63 `AUSTIN_PROVEN` ones. Fixed; rescore offline
  with `rescore_baselines.py` rather than re-running the provers. `status_report.py`
  now prints a `WARNING` if any broken baselines remain.
- **`.sat` certificates are incomplete** for everything written before the
  `--show_active on` fix. Regenerate.
- **`--mode casc_sat` is not a valid Vampire mode.** It produced silent fake
  timeouts on every saturation test for a while. Use `-sa otter`.
- **A truncated Python file still compiles** (loses only its `__main__` block, exits
  0 doing nothing). `overnight.sh` will not start without `SELFTEST OK`. If a script
  fails to parse on the cluster, the mount truncated it — re-sync, don't debug.
- **Retry stage is inefficient.** For a `NO_FINITE_MODEL` law it re-runs the
  (i)-prover (already a theorem) and burns 300s on the trivial-prover *then* 300s on
  saturation, sequentially. Those two are mutually exclusive; run them in parallel
  and take whichever returns first. ~3× throughput.
- **`overnight.sh`'s `pgrep` patterns are stage-specific**, not "any prover":
  `prove_status.py .*retry_status_`, `prove_status.py .*${OUT}_`,
  `order6_targeted.py .*r${r}_pool_`. So a manual job that runs `vampire` directly, or
  imports `prove_status` as a module (`equiv_sample.py`, `baseline_probe.py`,
  `ordered_model.py`), does **not** collide with `wait_for`. The real cost of running
  alongside is CPU contention. Do not launch a second `prove_status.py` writing to a
  matching `--out` prefix.
- Order-5 fmb-confirm is essentially free-passing (these laws are pre-established
  no-finite-model), so `--fmb-timeout 0` there. Order-6 needs the real check.
- **`BENCHMARK GOLD` does not mean what it says.** `order6_grade.py` implements
  translation-invariant and greedy. **Neither is prior art — both are ours.** So "gold"
  means *our two builders failed*, which is the same class of claim as "Vampire didn't
  finish in 20s." Until the construction suite faithfully implements the published
  families (Kisielewicz; ETP ch. 7 — translation-invariant, greedy, Asterix/Obelix,
  Dupont, the ad hoc models; linear ℤ[α]; quotients), an LLM win shows the model beat
  *our code*, not the literature. Doing this right will **shrink** the hard tier.
- **The extracted model lives over an extended signature.** JRS note Vampire introduces
  definitions `f₀, f₁, …` to saturate, which "cannot easily be read off the saturated
  set, but are not necessary to define the model." The magma we claim is the **reduct to
  the original operation**. Get this wrong and CSI will happily certify a rewrite system
  for a structure that is not the one in the paper. Also verify the saturation came from
  a **complete strategy** before trusting it.
- **Equivalence is semi-decidable in the positive direction only.** Unproved
  equivalences leave classes *split*, so any class count is an **upper bound** that
  shrinks with compute — the wrong direction of error for a number in an abstract.
  Report it as an upper bound with the budget attached.
- **Pairwise mutual implication is not an afternoon.** 3,428 laws ≈ 5.9M pairs ≈ 12M
  prover calls. Fingerprint each law against a fixed ~100-equation probe set first
  (~343k calls), then go pairwise only within matching buckets.

---

## 7. What to do next, in order

**STATUS as of 2026-07-10 — most of the diagnostics below are DONE. Details in
`PAPER_PLAN.md` §5; live cluster run monitored by `scripts/progress_runall.sh`.**

| item | state |
|---|---|
| Verification / answer format | **DONE.** `answer_spec.py --selftest --lean-dir .` passes: Lean checks the reference proof, axiom footprint enforced. Minimum-acceptable item 1 closed. |
| 12857 / 33436 Austin | **CONFIRMED, two ways.** Vampire saturation + Twee unfailing completion both return `CounterSatisfiable`. Models computable via `ordered_model.py` (27/27, non-vacuous). Neither is a plain TRS — even Twee's *reduced* system has unorientable/extra-variable rules → the ordered-rewriting Lean formalisation is the contribution, not optional. |
| Equivalence collapse | **MEASURED, ≥26%.** 262-law `AUSTIN_PROVEN` census → ≤195 classes (`classes.json`). Abstract quotes classes, never laws. Hard-tier collapse still needs `equiv_sample.py --no-models` (no saturations there). |
| 20s→300s retry curve | **DONE.** 3.7% convert, 0/216 → AUSTIN. §5C. |
| Portfolio v1.0 baseline | **RUNNING (fill-in pending).** 8 configs × ladder on 120 `NO_FINITE_MODEL` laws. Curve flat, 0 new AUSTIN, ~3% TRIVIAL contamination, **no Twee-only model** (reshaping ruled out). `PAPER_PLAN.md` §5C has the write-up with `<FILL>` stubs — drop in final N, 30s rate, TRIVIAL count when the run marks `done`. |
| Lean `ground_confluent` | **OPEN — this is the paper.** `OrderedModel.lean` elaborates with 3/4 steps proved; the one real `sorry` is ground confluence of ordered rewriting on a saturated set. JRS leave it open; ETP is a Lean project. |
| Generator seed-dedupe | built (`seed_dedupe.py`); wire into `order6_targeted.py` at generation. |
| Full hard-tier sweep | not started — every `NO_FINITE_MODEL` law × portfolio v1.0; survivors = the published tier. Long run, do after ladder/portfolio frozen. |
| (i)-prover vs Infinox | not started (admission ticket, §5A). |

Below is the original ordering, kept for the reasoning. Nothing here depends on proving
anything is impossible.

**Durability — build the real baseline (this is the gate).**

1. **Install the portfolio.** E, Twee, Vampire with ground joinability, Infinox, CSI,
   TTT2, CeTA. Get the JRS-modified Vampire/E that emit rewrite systems.
2. **Re-define the hard tier** as: survives every prover × ordering × real budget.
   Run it over the 3,428 `NO_FINITE_MODEL` laws. The survivors are the benchmark's
   hard tier and the number is the headline. If it is small, generate more — the
   pipeline is designed for that, and a small *rate* is fine as long as it is nonzero.
3. **Benchmark our (i)-prover against Infinox** on the order-5 corpus. Keep whichever
   proves more; cite the other.

**Verifiability — close the Lean gap (this is the clearest open contribution).**

4. Formalise once, generically: Herbrand domain, normalisation, well-foundedness,
   confluence ⇒ model. That turns every CeTA-certified rewrite system — theirs and
   ours — into a Lean theorem. JRS explicitly leave this open and ETP is a Lean
   project.
5. Wire both answer channels into the judge: concrete algebraic model → Lean; term
   model → CSI/TTT2/CeTA. Emit TSTP model format.

**Contamination — make the generator the artifact.**

6. Publish `order6_targeted.py` + seeds + dates, not just a static instance list.
   Ship a held-out set generated after the evaluated models' cutoffs.
7. **Equivalence classes, not laws.** Pairwise mutual implication over the corpus,
   union-find. ETP pre-empted exactly this criticism for their 10; the number in the
   abstract must be classes.

**Then the eval.**

8. Two-sided task (§2), hard tier, LLM vs. the full deterministic portfolio. Reuse
   `attic/finite_regime/proposer_o3.py` for the API and self-verify loop. Test one
   law × one round before any sweep.

   **Pre-register tool access or the measurement is void.** If the model may call
   Vampire/E/Twee, it can run the portfolio at 10× our budget on a hard-tier law and
   "solve" it — same instance, same method, more compute. Construction suite: yes.
   Lean/CeTA/CSI/TTT2 as *checkers*: yes. Saturation provers: **no**. Self-verify loop:
   yes, report compute.

   **After any LLM solve, re-run the portfolio at 10× on that law.** If it falls, say
   so. That is what happened to the finite band (`attic/finite_regime/`) and a reviewer
   will ask.

   **Answer-channel parity.** Baseline and model must emit the same certificate, or
   "portfolio scores 0" is a category error, not a zero. The greedy builder emits a
   domain-verified partial magma and cannot certify a solve on the two-sided task — so
   it cannot score. Every baseline component either emits a Lean model, a CeTA-certified
   rewrite system, or a proof of `L ⊨ x = y`, or it is excluded from scoring and
   reported as a heuristic.

**Housekeeping** (cheap, do while the above runs): rescore baselines; re-run the
order-5 pass (22818 missing); regenerate saturation certs with `--show_active on`;
measure the retry conversion rate at 300s.

## 8. Framing for the writeup

> ETP is verifiable but uniform: one strategy (ATP + finite model builder) resolves
> 22 million implications, so it measures execution, not construction. We isolate the
> sub-family where that strategy is *provably* inapplicable — laws with no nontrivial
> finite model — extend it past the order ETP enumerated, and pose a two-sided,
> machine-checkable task: construct a countermodel, or prove the law trivial. Against
> the strongest published automated portfolio (completion across provers and
> orderings, plus certified model extraction), the hard tier is resolved N times by
> the portfolio and M times by the model. The generator is public, so the benchmark
> is renewable rather than a fixed set to be exhausted.

Claims **not** to make: that we invented the existence argument (ETP used saturation);
that saturation-only countermodels are inaccessible (JRS extract and certify them);
that proving "no finite model" is new (Infinox); that any instance is unsolvable in
principle (anything Lean-checkable is findable by proof enumeration — hardness here
is relative to methods, and that is normal and sufficient); that `AUSTIN_PROVEN` laws
are open problems (they are the floor).

Prior art to cite: JRS (arXiv:2602.16324); Infinox (Claessen & Lillieström, JAR
47:111–132, 2011); Bachmair–Ganzinger; Lynch; Peltier; unfailing completion
(Bachmair–Dershowitz–Plaisted); CSI, TTT2, CeTA/IsaFoR; ETP (Bolan et al.); Janota,
Vampire on ETP (arXiv:2508.15856); Austin (1983); Kisielewicz.
