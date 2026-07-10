# Paper Plan — LLM-guided construction of verifiable countermodels

Status: active plan as of 2026-06-30. Supersedes the TRUE-side "uniquely-solved
vs virtual-best-solver" framing in `EXPERIMENT_SPEC.md` (kept for the baseline
matrix machinery, but its thesis is dead — see "Why this plan" below).

## Thesis (one line)
Language models are useful in formal math as **constructors of verifiable
countermodels** in open-ended algebraic search spaces — proposing candidate
*worlds* where an implication fails (finite magmas, modular/affine models,
algebraic extensions, companion-matrix / ℤ-module constructions, quasigroups,
twisting semigroups, …) — while a symbolic verifier + Lean eliminate every
hallucinated result. The LLM never writes the proof; it proposes the structure,
and correctness comes entirely from checking.

## Why this plan (the reasoning, so we don't relitigate it)
- **The TRUE side is owned by ATPs.** Vampire proves our "hard" TRUE residual
  pairwise in milliseconds — 18/18 of `true_misses_18` and 6/6 of
  `dev_true_easy`, most < 0.1s (see `paper/results/baselines_*`). Our solver's
  "true misses" are misses relative to *our* narrowing engine, not to the field.
  So there is no TRUE-side "uniquely solved" story, and the LLM-waypoint work is
  not the paper's center (the "LLM proposes, verifier checks" philosophy carries
  over to the false side).
- **ETP order-≤4 is resolved and contaminated.** Our `hard1/2/3` use law IDs
  ≤4694 — the published ETP order-≤4 laws. The whole 22M-edge graph is resolved
  and Lean-formalized (Tao et al., 2025), and the project *already automated
  infinite-model construction* via greedy table-filling. Results only on this
  data are engineering evidence, not novelty.
- **Prior art is close but not on top of us.** FunSearch/AlphaEvolve own the
  "LLM proposes construction + evaluator checks" *paradigm*; "Learning to
  Disprove" (2026) does general Lean-verified counterexample generation (olympiad
  / formal-math statements), *not* infinite/algebraic model construction; the ETP
  greedy method automated much infinite construction *on order-≤4 magmas*. The
  surviving gap is narrow and specific: **agentic navigation of an open algebraic
  construction space, with Lean-verifiable certificates, on problems outside the
  resolved graph.**

## Differentiator vs prior work
- **vs direct LLM proof generation (DSP-style and successors):** we do not trust
  model-written proofs. The LLM only proposes structures; Lean/model-checking is
  the sole source of correctness.
- **vs ATPs / completion (Twee-style):** great for *true* implications and
  symbolic saturation; *false* ones need a *witness object*, and the hard ones
  need choosing the right model family, not saturating equations.
- **vs finite model finders (Mace4, Vampire `-sa fmb`):** finite search refutes
  many false implications but is structurally blind to witnesses that are large,
  structured, algebraic, or infinite.
- **vs FunSearch/AlphaEvolve:** the loop is not new. What we add is a
  *formal-math* instance where the evaluator is a Lean-verifiable certificate
  (not a score) and the target is constructive disproof over algebraic theories.

## The four claims (each an experiment)
**C1 — The benchmark is genuinely open.** Build an order-5+ (or otherwise
held-out) candidate set outside the resolved order-≤4 graph. Filter: drop
trivial/small-finite-refutable pairs and ATP-proved trues; what remains is the
hard construction set. Report: sampled / filtered-trivial / ATP-true / entering
hard set / verified countermodels found.

**C2 — The fixed portfolio is strong (steelman).** Assemble the strongest
*reasonable* fixed portfolio: exhaustive Fin 2–3, structured finite tables,
affine/modular models, SAT/domain-propagation finite search, quasigroup/Latin/
idempotent modes, algebraic-linear ℤ-module/companion-matrix, and (for evaluation
only) Vampire/Mace finite model finding. Publish its exact search-space spec
(families × parameter ranges). Report: solved per rung, residual, cost,
certificate validity. Defines the hard residual.

**C3 — The proposer adds coverage beyond the portfolio.** Arms: fixed portfolio
only; direct LLM proof/witness; LLM selects a family from the fixed list; LLM
proposes *parameterized construction hypotheses* + verifier loop; (if available)
an oracle/human-designed upper bound. The decisive comparison is **proposer vs
strong fixed portfolio**, and the LLM only gets credit when the witness is
Lean-verified *and* not already found by the portfolio. Report: additional
verified countermodels, judge/Lean acceptance, failed-proposal types, attempts/
cost per solve.

**C4 — The wins are structurally diverse / out-of-portfolio.** Tag every
proposer-only solve by construction class *and* by "was this parameterization
class in the steelman portfolio's spec, yes/no." The money number is the count
and spread of the **no**s. Diversity across families the portfolio already had is
weak; a scatter of out-of-span encoding classes is the paper.

### Target main table
| Method | Verified solves | Portfolio-residual solves | Distinct out-of-span classes | Wrong/unverified |
|---|---|---|---|---|
| Small finite search | high (easy) | 0 | 1 | 0 |
| Strong fixed portfolio | higher | 0 (baseline) | several | 0 |
| Direct LLM proof/witness | low | low | unclear | many rejected |
| LLM proposer + verifier | highest | +N (meaningful) | diverse | 0 accepted wrong |

## Methodological guardrails (hard-won)
- **Claim empirically, not theoretically.** Not "no finite portfolio is
  complete" (unprovable, invites a proof demand) but "under realistic compute a
  *strong* portfolio leaves a meaningful residual the proposer solves."
- **Commit to coverage, not efficiency.** If the LLM only picks faster among
  families the portfolio already has, that's a speed claim that evaporates with
  more baseline compute. Design so the proposer can go *outside* the portfolio's
  enumerated classes, and measure how often its wins do.
- **"Out-of-portfolio" = not enumerated by the fixed search**, not "alien math."
  A specific algebraic-extension / companion-matrix encoding the fixed sweep
  doesn't parameterize counts, even if it's "linear in spirit." Make this
  auditable via the published portfolio spec.
- **Budget-relative boundary → scaling check.** State the portfolio's enumeration
  budget; show out-of-span wins survive a substantially larger budget (bigger n,
  wider coefficient sweep). Kills "you under-budgeted the baseline."
- **Steelman the portfolio** — strongest reasonable sweep, or beating it proves
  nothing (weak-baseline trap; same lesson as the ATP baselines).
- **Unlabeled order-5 → fuzzy denominator.** After filtering ATP-proved trues,
  the residual is {false} ∪ {trues ATPs missed}, indistinguishable on a failed
  construction. Lead with the **absolute** count + diversity of verified
  constructions; treat the residual as an upper bound, not a clean success rate.
- **The construction side is self-certifying.** A Lean-checked magma satisfying
  eq1 and violating eq2 *is* the disproof — no pre-existing label needed. This is
  what lets us leave the labeled ETP graph for open order-5 problems.
- **Contamination.** Order-5 mitigates it (outside the resolved corpus). Preempt
  the softer objection — o3's *ability to propose the right family* is partly
  ETP-derived — by stating plainly that using learned mathematical intuition to
  propose is the point; the problems and witnesses are new.

## Sequencing (de-risk before building)
0. **Population scale-up (2026-07-03).** Repeated the stratified screen on
   a 10x bigger draw (8,050 of 20,000 sampled pairs) and a fresh 300-pair
   Vampire subsample: cheap-filter survivor rate held steady (39.49% vs
   40.75%), and the confirmed-hard rate held steady too (5/300 = 1.67% vs
   4/300 = 1.33%) — 4 of those 5 are genuinely new hard pairs, bringing the
   total validated hard-pair pool to **8** (double the prior 4). Extrapolating
   the ~1.5% average rate to the full 3,179-survivor pool from this one
   draw alone predicts ~48 more confirmed-hard pairs sitting there
   unvalidated — this is not a thin population, every scale-up so far finds
   proportionally *more*, not fewer. See
   `paper/results/order5_scaled_population_report.md`.
1. **Order-5 yield probe (cheap, do first). DONE 2026-07-01 — GATE PASSES.**
   Sampled 250 uniform-random order-5 pairs (outside the resolved order-≤4
   graph); ran Vampire (casc + fmb) both sides. 1/250 (0.4%) stayed genuinely
   unresolved at 40s both directions — >100x the order-≤4 hard-set's curated
   rate (~0.003% of all ordered pairs). See `paper/results/order5_probe_report.md`.
   **Follow-up (also done):** a stratified rerun that pre-filters candidates
   with the real portfolio's cheap deterministic FALSE stages before spending
   Vampire compute raised this to 4/300 (1.33%), a ~3.3x density improvement —
   see `paper/results/order5_stratified_rerun_report.md`.
2. **Residual-by-family analysis. DONE 2026-07-01.** Tagged every FALSE-side
   solve in the existing merged results by witness family; confirmed a real,
   moderately diverse above-floor construction population (9.1% of all
   order-≤4 problems), concentrated in the curated hard1/hard2 sets (37-41%)
   vs uniform sampling (0.9%) — this is *why* step 1's stratified rerun beat
   uniform sampling. See `paper/results/residual_family_analysis.md`.
3. **Build the order-5 Lean harness, the steelman portfolio spec, and the
   proposer loop; run C1–C4. Substantially done 2026-07-01:**
   - **Steelman portfolio spec (C2):** written as `paper/STEELMAN_PORTFOLIO.md`
     — all 9 deterministic FALSE-side families already exist in
     `scripts/my_solver_merged/solver.py` with exact parameter ranges
     documented; all 7 categories this plan names are covered.
   - **Order-5 Lean harness:** turned out to need *no new infrastructure*.
     `judge/verify.py` is equation-text-driven, not tied to the 4694
     registered order-≤4 law IDs, and none of the judge/submission Lean
     sources import Mathlib. Verified end-to-end (7/7 real order-5 pairs
     accepted by the actual judge, both verdicts) in
     `paper/ORDER5_HARNESS_FEASIBILITY.md`. This resolves the "heavy infra"
     risk below.
   - **Proposer loop (C3/C4):** design + a real validated case study in
     `paper/PROPOSER_LOOP_SPEC.md`. Four order-5 pairs are now confirmed
     resistant to *all 9* portfolio families (not just the cheap 3-family
     screen from step 1) plus TRUE-side deterministic stages plus Vampire at
     40s — genuine, ready-to-use C3 targets. A manual (human-stand-in)
     proposer attempt on two out-of-portfolio families (cyclic-group twists,
     dihedral groups) was negative on all four — logged as real
     failed-proposal data, not yet a positive result.
   - **Real o3 proposer run: DONE 2026-07-01, extended 2026-07-03 (live
     data across all 8 validated pairs, negative so far).** Wired
     `openai/o3` via OpenRouter (`paper/scripts/proposer_o3.py`) and ran it
     on the original 4 targets (6 attempts), then extended to the 4 new
     pairs from the population scale-up (4 more attempts): **10 real
     attempts total, ~$0.16 cost, ~16,800 reasoning tokens, all
     `self_verify_failed`, 0 reached the judge.** Proposals were genuinely
     distinct across all 10 (quadratic-twist modular, quaternion
     conjugation rack, upper-triangular affine, coordinate-swap semidirect
     square, quadratic-bilinear mod-n, high-degree modular polynomial,
     quadratic-right mod-n, parity-switch left permutation, GF(3)²
     quadratic-twist, quadratic-left affine mod-n) and mostly bug-free —
     confirms the full C3 pipeline (prompt → parse → materialize →
     self-verify → judge) works end-to-end for real, but no positive
     result yet. This sandbox's 45s command cap forced `reasoning: low`
     throughout; a `reasoning: high` rerun with more rounds on the real
     machine (via `run.sh`, no time cap) is the natural next step. See
     `paper/results/proposer_o3_first_run.md` and
     `paper/results/proposer_o3_extended_run.md`.
   - **Also done 2026-07-03:** pushed the fixed portfolio's `mf2` finder
     past its Fin≤11 cap to Fin 12-14 on all 8 pairs (idem+qg + general
     modes) — all 8 still miss, ruling out "just needed a bigger domain"
     as the cheap explanation before crediting these to the proposer. See
     `paper/results/order5_finite_extension_report.md`.
   - **Not yet done:** a `reasoning: high` rerun off-sandbox; running
     C1–C4 as a full study once a positive proposer result exists.

## Case studies (planned)
1. Structured finite countermodel where naive finite search fails but SAT/
   domain-propagation finds the table.
2. **hard2_0051-style algebraic-linear witness** (ℤ[α] ≅ ℤ⁴ companion matrix) —
   the boundary case: "linear in spirit" yet unreachable by any finite ℤ/n-affine
   sweep. Must explain crisply *why* (infinite carrier, algebraic-integer
   eigenvalue) so the boundary reads as forced by the math, not gerrymandered.
3. A structurally different order-5+ witness found only by proposer-guided search.

## Abstract-level claim (target)
On a new set of order-5 equational-theory problems, our LLM-guided constructor
finds Lean-verified countermodels beyond a strong fixed portfolio, with gains
spread across multiple construction families — evidence that language models can
contribute to formal discovery as hypothesis generators while formal verification
eliminates hallucinated results.

## Risks / kill criteria
- **Thin/absent order-5 construction population** (C1 fails) → no AI paper here;
  fall back to a systems/benchmark paper on formally-verified equational solving.
  **Status: did not fire.** See sequencing step 1 — gate passed, and the
  stratified rerun shows the population is findable more efficiently than
  uniform sampling suggested.
- **Proposer wins are all one obvious missing family** (C4 fails) → efficiency
  story only; weaker; consider whether the framing survives. **Status: open**
  — a real o3 proposer ran 6 attempts on the four validated targets
  (2026-07-01, low reasoning effort, sandbox-capped) and found zero
  self-verified wins, so C4 remains unevaluated. Not yet a bad sign (this
  was a low-effort, few-round, sandbox-limited run) — needs the
  high-effort/more-rounds rerun in `paper/PROPOSER_LOOP_SPEC.md` §9 before
  this risk can be judged either way.
- ~~**Lean harness for arbitrary order-5 laws is heavy infra** — budget it; the
  ETP generated defs/checkers were built for the 4694 order-≤4 laws.~~
  **Resolved 2026-07-01, false alarm:** the judge needs no new infra at all —
  see `paper/ORDER5_HARNESS_FEASIBILITY.md`.

## What already exists (assets)
- Merged solver ~99.04% (1653/1669) on public sets, zero wrong; false-side stages
  include affine, SAT/domain-propagation, quasigroup/Latin, and algebraic-linear
  infinite-model construction (`scripts/my_solver_merged/solver.py`).
- Frozen baseline pinned (`ef84234`); paper harness (`run_ours.py`,
  `run_baselines.py`, `build_matrix.py`, `analyze.py`); o3 config
  (`config.paper.json`); Vampire installed on the cluster (`setup_atps.sh`).
- **Order-5 track (added 2026-07-01):** `paper/STEELMAN_PORTFOLIO.md` (C2
  spec), `paper/ORDER5_HARNESS_FEASIBILITY.md` (harness validation),
  `paper/PROPOSER_LOOP_SPEC.md` (C3/C4 design + 8 validated hard targets);
  scripts `sample_order5.py`, `cheap_false_screen.py`,
  `order5_harness_smoketest.py`, `single_side_vampire.py` (runs one Vampire
  direction at a time — needed once timeout×2-sides exceeds the sandbox cap);
  data `problems/order5_probe.jsonl`, `problems/order5_pool_v2.jsonl`
  (2,000 pairs), `problems/order5_stratified.jsonl`,
  `problems/order5_pool_big.jsonl` (20,000 pairs, 8,050 screened),
  `problems/order5_big_survivors.jsonl` (3,179), `order5_big_subsample300.jsonl`;
  results `results/order5_probe_report.md`,
  `results/order5_stratified_rerun_report.md`, `results/residual_family_analysis.md`,
  `results/order5_scaled_population_report.md` (population scale-up,
  8 validated hard pairs total, ~48 more predicted in the survivor pool alone).
- **Real o3 proposer (added 2026-07-01):** `paper/scripts/proposer_o3.py`
  (live OpenRouter call + self-verify + judge loop); results
  `paper/results/proposer_o3_first_run.md`,
  `paper/results/proposer_o3_log.jsonl` (6 real attempts, $0.12, all
  self-verify-failed — first live C3 data, negative so far).
