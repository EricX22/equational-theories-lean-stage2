# C3/C4 — LLM Proposer Loop: design + a real validated case study

Status: draft v1, 2026-07-01. Written per `PAPER_PLAN.md` claims **C3**
("the proposer adds coverage beyond the portfolio") and **C4** ("the wins
are structurally diverse / out-of-portfolio"). Builds on
`STEELMAN_PORTFOLIO.md` (the fixed portfolio the proposer must beat) and
`ORDER5_HARNESS_FEASIBILITY.md` (the judge mechanism, confirmed working).

## 1. The credit rule (restated precisely)
A proposer solve counts only if **both**:
1. The candidate witness is **Lean-verified** (judge `status: accepted`,
   with `pipeline/proxy.py::DEFAULT_PROOF_POLICY` attached — see
   `ORDER5_HARNESS_FEASIBILITY.md` for why that field is required).
2. It is **not already reachable by the fixed portfolio** — i.e. all 9
   families in `STEELMAN_PORTFOLIO.md`, run at their full production
   budgets (mf2: 240s, SAT: 120s), plus the deterministic TRUE-side stages
   (direct-h, two-step-h, narrowing, completion), plus a generous ATP pass
   (Vampire, both directions), all fail on that pair first.

Every proposer target must be run through *all* of the above before the LLM
ever sees it — the case study below does exactly this, and it is more
thorough than the stratified rerun's screen (which only used 3 of 9
families as a cheap pre-filter, by design — that was for yield estimation,
not for crediting a solve).

## 2. Prompt contract: propose a hypothesis, not a witness
The proposer must **not** be asked to output a table or a full construction
directly — that collapses into "LLM guesses a witness," which is (a) hard
for an LLM to get exactly right on the first token-by-token attempt, and
(b) unfalsifiable as a distinct contribution (a lucky correct table looks
identical whether reasoned or memorized). Instead:

**Input**: eq1, eq2 (equation text), plus a compact description of what the
fixed portfolio already tried and failed at (families + ranges, so the
model doesn't waste a turn re-proposing "try Fin 6" or "try affine mod 20").

**Output** (one of):
- a **construction family name** in free text (e.g. "twisted dihedral
  group," "wreath product of Z/2 and Z/n," "near-ring with zero-symmetric
  multiplication," "tropical (min,+) semiring restricted to a sub-lattice")
- **concrete parameters** to try within that family (group order range,
  which specific twist/automorphism, etc.)
- a **short justification** tied to the equation's shape (e.g. "eq1 forces
  a self-referential left-identity pattern; try a group with a
  fixed-point-free automorphism, since conjugation-based twists are
  fixed-point-heavy and likely to fail" — this is exactly the kind of
  reasoning that failed for me manually below, which is useful negative
  signal to hand back to the model on the next round).

**A separate materializer step** (deterministic Python, not the LLM) turns
the named family + params into an actual candidate table/model, exactly the
way `af_find` turns "affine, modulus n" into a concrete table today. New
families need a new light-weight materializer function each — this is the
main new *code* surface C3 needs, and it is small per family (see §4).

## 3. Verifier loop (mirrors the existing self-verification pattern)
Every family in `STEELMAN_PORTFOLIO.md` self-verifies in Python before ever
calling the judge (checks `equation_holds(eq1)` and `not equation_holds(eq2)`
on the concrete candidate). The proposer loop must do the same:
1. Materialize candidate from the LLM's (family, params).
2. Self-verify in Python (or exact arithmetic, for infinite models).
3. Only if self-verification passes, emit a Lean cert (`make_false_code` for
   finite tables, or an `al_`-style companion-matrix cert for infinite
   algebraic models) and call `verify_answer` with `DEFAULT_PROOF_POLICY`.
4. Log the outcome regardless of accept/reject — **failed proposals are
   data**, not noise. Track a `failure_type` per attempt: `self_verify_failed`
   (materializer produced a candidate that doesn't actually satisfy eq1/¬eq2
   — this is the "no accepted-wrong" invariant: it must never reach the
   judge), `judge_rejected` (self-verified but Lean disagrees — should not
   happen if the materializer is honest, and would itself be a solver bug
   worth investigating), `no_candidate` (LLM's proposed family/params
   produced nothing to test, e.g. asked for a family with no materializer
   yet).

## 4. C4 attribution: in-span vs out-of-span
Tag every proposer accept with:
- **family_name** (free text from the LLM's proposal)
- **in_span**: does this family+parameter-range appear in
  `STEELMAN_PORTFOLIO.md`'s published spec? Concretely: is it a modulus
  ≤40 affine model, a Fin≤11 table (any of the mf2 modes), a Fin≤7 SAT
  model, or a degree≤8 algebraic-linear model? If yes → **in-span, budget
  question only** (per the "budget-relative boundary" guardrail — flag as
  "portfolio would've found this with more budget," not a coverage win).
  If no (a genuinely different encoding: group-based twists, wreath/
  semidirect products, non-linear infinite models, or a finite witness
  bigger than Fin 11) → **out-of-span**, the actual C4 money count.
- **scaling check**: for anything borderline (e.g. Fin 12-15, a family that
  merely extends an existing range), rerun the portfolio's *existing*
  family at a substantially larger budget/range first — if it now finds
  the same witness, downgrade to in-span. This directly implements
  PAPER_PLAN's "kills 'you under-budgeted the baseline'" guardrail.

## 5. Real validated case study (2026-07-01)
Four order-5 pairs from `paper/problems/order5_stratified.jsonl` were
already known to resist Vampire at 40s both directions
([[order5-stratified-rerun]]). Before treating them as legitimate C3
targets, I ran **every remaining portfolio family** (the stratified rerun's
cheap screen only used 3 of 9) against all four:

| Family | order5v2_0073 | order5v2_1593 | order5v2_0534 | order5v2_0515 |
|---|---|---|---|---|
| Named witness tables | miss | miss | miss | miss |
| Perturbed witness tables (Fin 2-4) | miss | miss | miss | miss |
| Fast false-model probe (Fin 4-5) | miss | miss | miss | miss |
| Algebraic-linear (degree 2-8) | miss | miss | miss | miss |
| mf2 backtracking incl. qg/idem/Latin (Fin≤11, 20-40s) | miss (schedule exhausted at 28s of a 40s budget — not time-starved) | miss (20s) | miss (20s) | miss (20s) |
| SAT finder (Fin 5-6, 8-15s) | miss | miss | miss | miss |
| Direct-h / two-step-h / narrowing-quick (TRUE side) | miss | miss | miss | miss |
| Completion singleton/non-singleton (TRUE side) | miss / miss | miss / miss | miss / miss | miss / miss |
| Vampire casc + fmb, 40s (from the stratified rerun) | miss | miss | miss | miss |

All four survive the *entire* current portfolio plus a real ATP pass.
**Caveat**: mf2/SAT were run at reduced budgets (20-40s / 8-15s vs the
production 240s / 120s) due to this session's time constraints — for
`order5v2_0073` the mf2 schedule provably *exhausted itself* before its
time budget ran out (28.3s of a 40s allowance), meaning more time would not
help *that* family; the other three pairs were not pushed to that same
exhaustion check and should be before final publication.

The four pairs (equations in `[[order5-stratified-rerun]]`'s memory note)
are genuine, ready-to-use C3 targets.

## 6. My own manual proposer attempts (honest negative log)
Time-boxed, by hand (standing in for the LLM this session, since no
OpenRouter/o3 key is available in this sandbox): tried two out-of-portfolio
families on all four pairs.

- **Cyclic-group twists** (`Z/n` with add, subtract, reversed-subtract,
  negate-both, left-inverse-add, right-inverse-add, additive-with-constant,
  a toy conjugation-style twist), `n = 2..12`: **no hits**. In hindsight
  this family is arguably still "affine-adjacent" (linear mod n) — a real
  proposer should be pushed toward genuinely non-linear families, and a
  reviewer would likely flag this attempt as in-span-ish anyway.
- **Dihedral groups D_2..D_6** (both multiplication orders): **no hits**.
  This is a legitimately non-linear, non-affine, non-portfolio family
  (group-Cayley-table-based, order 4-12), so a negative result here is
  real signal, not a scoping error.

**Failure-type tag for both**: `self_verify_failed` at the materializer
stage — the candidates were valid magmas but didn't satisfy eq1/¬eq2 for
any tested instance, so nothing ever reached the judge (the "0 accepted
wrong" invariant held throughout, as designed).

**What this suggests for the next attempt**: eq1 in all four pairs has the
shape "x = ⟨term mentioning x, y, z, ...⟩," i.e. a self-referential
left-identity-like constraint. Neither cyclic twists nor small dihedral
groups satisfy this pattern for any tested order — worth trying **larger
non-abelian groups** (order >12, past what mf2's qg/idem modes reached in
reduced budget), or genuinely different structures: **near-rings**,
**loops that are not groups** (non-associative but with two-sided
inverses — the "twisting semigroup" idea from `PAPER_PLAN.md`'s own
example list is underexplored here), or accepting these may need an
**infinite model past degree-8 algebraic** (a higher-degree or
transcendental construction, extending family 9's range — which would
itself be a "scaling check" case, not a new family).

## 7. What's genuinely new work vs reused
**Reused unmodified**: `judge/verify.py`, `DEFAULT_PROOF_POLICY`,
`make_false_code`, the self-verification pattern, all 9 portfolio families
(used here as the *screen*, not touched).
**New for C3**: the prompt contract (§2), the materializer-per-family
pattern (§3) — only the two families I hand-tested (cyclic twists,
dihedral) have materializers right now; each new proposed family needs
~20-40 lines like `af_find`'s, not a new subsystem. The credit/attribution
logic (§4) is new but small (a lookup against the published spec + the
scaling-check re-run).

## 8. Real o3 run (2026-07-01) — first live data

Wired the actual `openai/o3` call via OpenRouter per the §2 contract
(`paper/scripts/proposer_o3.py`) and ran it on all four validated targets.
**Result: 6 real attempts (4 pairs × round 1, 2 pairs × round 2 with
feedback), all `self_verify_failed`, $0.1234 total, 12,480 reasoning
tokens, 0 reached the judge.** Full table and analysis in
`paper/results/proposer_o3_first_run.md`; raw log in
`paper/results/proposer_o3_log.jsonl`.

Proposals were genuinely distinct from both the portfolio and my earlier
manual attempts — quadratic-twist modular, quaternion conjugation rack,
upper-triangular affine, coordinate-swap semidirect square,
quadratic-bilinear mod-n, high-degree modular polynomial — and 5/6 were
clean, bug-free code on the first shot (the quaternion one hit a real
`IndexError`, not a math dead end). This confirms the pipeline works
end-to-end for real, with no positive result yet.

**Sandbox constraint**: `reasoning: high` exceeds this environment's 45s
command cap and is silently killed (no background-process workaround
available here); had to run at `reasoning: low` throughout, which still
reasons genuinely (1.5-3k tokens/call) but is plausibly underpowered for
these four pairs specifically.

**Extended 2026-07-03** to the 4 new pairs from the population scale-up
(`paper/results/order5_scaled_population_report.md`): 4 more real
`reasoning: low` attempts, all self-verify-failed, ~$0.04 more
(4,352 reasoning tokens) — proposals (quadratic-right mod-n, parity-switch
left permutation, GF(3)² quadratic-twist, quadratic-left affine mod-n) were
all fresh and distinct from every prior attempt. **Running total: 10 real
o3 attempts across all 8 validated hard pairs, ~$0.16, 0 solves.** See
`paper/results/proposer_o3_extended_run.md`.

## 9. Immediate next steps
1. ~~Wire an actual LLM call~~ **DONE — see §8.** Next: rerun at
   `reasoning: high` on the real machine via `run.sh` (not sandbox-capped).
2. ~~Push mf2 past Fin≤11~~ **DONE 2026-07-03** on all 8 validated hard
   pairs (the original 4 plus 4 new ones from the population scale-up,
   see `paper/results/order5_scaled_population_report.md`): Fin 12-14 in
   idem+qg mode, plus a Fin12 general-mode check. All 8 still miss — rules
   out "just needed a bigger domain" as the cheap explanation. 3 pairs
   (`order5v2_1593`, `order5v2_0534`, `order5big_6145`) genuinely used
   their full time budget and are the best candidates for a real
   long-budget (100s+) rerun on the actual machine (sandbox caps any
   single command at 45s, so this couldn't be pushed further here). See
   `paper/results/order5_finite_extension_report.md`.
3. Build 2-3 more materializers for the families the negative log suggests
   (near-rings, non-associative loops, larger non-abelian groups) — these
   are the natural next things to hand the real proposer, or to try by hand
   again with more time.
4. Fix the quaternion-conjugation-rack materializer's `IndexError` (n=8)
   and retry — it failed on implementation, not the underlying math idea.
5. Increase `--rounds` per pair (only 1-2 rounds fit in this session's
   sandbox time budget) now that the full loop is proven to work.
