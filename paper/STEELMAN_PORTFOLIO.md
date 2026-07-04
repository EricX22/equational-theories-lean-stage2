# C2 — Steelman Fixed Portfolio Spec

Status: draft v1, 2026-07-01. Written per `PAPER_PLAN.md` claim **C2**: "Assemble
the strongest reasonable fixed portfolio... Publish its exact search-space spec
(families × parameter ranges)... Defines the hard residual." This document is
the citable spec; `paper/results/residual_family_analysis.md` has the
empirical yield numbers this spec explains.

This portfolio already exists as working code
(`scripts/my_solver_merged/solver.py`) — built for the competition, not for
this paper — so C2 is descriptive, not aspirational: every family below has
been run on thousands of order-≤4 problems. The task here is to state its
exact boundaries precisely enough that a reviewer can (a) regenerate it, and
(b) judge whether an order-5 win is really outside it.

## Scope
This spec covers the **FALSE-side (construction) portfolio** — proposing a
countermodel that satisfies eq1 and violates eq2. Per `PAPER_PLAN.md`'s
"why this plan," the TRUE side (proving eq1⊨eq2) is ATP-owned: Vampire
closes our hard TRUE residual in milliseconds, so it is not part of this
paper's steelman construction and is listed only as the classical-VBS
comparison row (family 10, "for evaluation only," per C2's own wording).

## Soundness invariant (applies to every family below)
Every family below **self-verifies in exact/rational arithmetic before ever
calling the Lean judge** (evaluate eq1 holds + eq2 fails on the candidate
table/model in Python, using the same `equation_holds` check the judge would
run) and the judge itself re-checks via `decideFin!` or exact `omega`/`decide`
on the emitted Lean term. A wrong candidate can be silently dropped; it can
never be silently accepted. This is what licenses treating "solved" as
"Lean-verified," not "solver claims," per the paper's central soundness
argument.

## The portfolio (execution order = gating order)
Stages run in this order; each is only attempted if every earlier stage
failed to close the problem (a short-circuit pipeline, not a race — so
"solved_by" attribution reflects the *first* stage that works, not
necessarily the *cheapest possible* one for that instance).

### 1. Exhaustive Fin ≤3 counterexample search
Brute-force enumeration of literally every magma table on 2 and 3 elements
(`n^(n·n)` = 512 tables at n=2, ~387M at n=3 — tractable because Python
short-circuits on the first hit and most FALSE cases have small witnesses).
**Domain**: Fin {2, 3}. **Cost**: sub-second to a few seconds.
**Entry point**: `search_counterexample(eq1, eq2, max_n=3)`.

### 2. Named witness tables
Lookup against 16 curated small magmas known to break common law shapes:
`LP2/RP2/XOR2` (Fin 2), `LC3/RC3/Z3/MAX3/MIN3/FLIP3/CONST3_{0,1}` (Fin 3),
`XOR4/Z4/LP4/RP4/MAX4/MIN4` (Fin 4). **Domain**: fixed set, no sweep.
**Cost**: microseconds. **Entry point**: `search_named_witnesses`.

### 3. Affine model search
Symbolic search over `op(x,y) = a·x + b·y + c (mod n)`. For each modulus and
each `(a, b)`, solves for the set of valid `c` **algebraically** (not by
brute force over c) by propagating eq1's constraint on the coefficients, so
the sweep is `O(n²)` per modulus, not `O(n³)`. **Domain**: modulus
`n ∈ [2, 40]`, capped so `n^k ≤ 400,000` (k = max free variables in either
equation, keeping the judge's `decideFin!` fast on the emitted cert).
**Cost**: milliseconds-to-seconds. **Entry point**: `af_find` /
`try_affine_model`.

### 4. Perturbed witness tables
Takes the structured-table families from stage 5 (below) and flips a single
cell, catching counterexamples one edit away from a "nice" table.
**Domain**: Fin {2, 3, 4}. **Entry point**: `search_perturbed_witnesses`.

### 5. Structured Fin 4–7 counterexample search
~30 parameterized table families per size (constant, left/right projection,
cyclic add/sub with offset, lattice max/min, multiplication mod n, linear
`a·i+b·j mod n` for small `(a,b)`, XOR at powers of 2, constant-with-diagonal,
identity-in-slot-0) — covers most "nice" algebraic shapes without the cost of
full enumeration. **Domain**: Fin {4, 5, 6, 7}. **Entry point**:
`search_counterexample_extended` / `_structured_tables`.

### 6. Fast false-model probe
A quick backtracking pass, cheaper than the full portfolio below, to catch
easy Fin 4–5 misses before the expensive stages run. **Domain**: Fin {4, 5},
1.8s/size. **Entry point**: `mf_find_false_model`.

### 7. Backtracking model finder ("mf2") — includes quasigroup/Latin/idempotent modes
The largest family: a domain-propagation (SEM/Mace4-style) backtracking
search with per-cell bitmask domains, unit propagation, MRV branching, and
least-number symmetry breaking. Six **modes**, each a different constraint
restriction on the search space, run on a **weighted schedule** (budget
allocated proportional to a per-cell weight, cheap/likely cells first):

| Mode | Meaning | Fin sizes scheduled | Per-cell weight |
|---|---|---|---|
| `idem` | idempotent (diagonal fixed: `x◇x=x`) + Latin rows & cols | 4,5,6,7,8,9,10,11 | 0.3–3.0 |
| `qg` (quasigroup) | Latin square: all-different in every row AND column | 4,5,6,7,8,9,10,11 | 0.3–3.0 |
| `rows` | row-Latin only (all-different per row) | 4,5,6,7,8,9 | 0.3–2.0 |
| `cols` | column-Latin only | 4,5,6,7,8,9 | 0.3–2.0 |
| `directed` | goal-directed: enumerate Eq2's variable assignments first, search a model refuting that specific instance | 4,5,6,7 | 0.8–3.0 |
| `general` | no structural constraint (hardest, run last) | 4,5,6,7,8 | 0.8–3.0 |

Empirically (`solver.py` comment, [[false-side-quasigroup-breakthrough]]),
most of the hard1/hard2 residual counterexamples **are** idempotent
quasigroups, which is why `idem`/`qg` are scheduled first and reach Fin 8-9
in a handful of search nodes. Two additional complementary passes run only
if the weighted schedule above fails: WalkSAT local search (Fin {5,6,7},
2.0s/size, `mf_walk_find_model`) and Eq2-directed DFS + duality (Fin
{4,5,6,7}, 2.0s/size, `mf_directed_find_model`). **Total budget**: 240s
(`MF2_PORTFOLIO_BUDGET`), i.e. ≤6.7% of the 3600s per-problem wall clock.
**Entry point**: `mf2_find_portfolio` / `try_model_finder`.

### 8. SAT false-model finder
Complete CDCL-style search (encodes the magma-table + eq1/eq2 constraints as
a SAT instance, pure Python, no external solver) — the completeness
backstop for whatever the heuristic mf2 schedule misses. Gated to
non-singleton cases (a singleton hint means the pair is TRUE, so no
counterexample exists) and skips encodings too large for pure Python
(`n³ · n^vars > 4,000,000`). **Domain**: Fin {5, 6, 7}. **Budget**: 120s
(`SAT_FINDER_BUDGET`). **Entry point**: `sat_find_model` / `try_sat_finder`.

### 9. Algebraic-linear infinite model
Last-resort stage for cases with **no finite counterexample at all**: finds
a linear witness `x◇y = a·x + b·y` (with the idempotent ansatz `b = 1-a`)
where `a` is an algebraic number — root of an integer polynomial of degree
2–8 (`al_find_linear_model(deg_min=2, deg_max=8)`). Encodes the number ring
`ℤ[α]` as the free ℤ-module `ℤ^d` via the companion matrix of that
polynomial, checked exactly in integer arithmetic on a spanning set (proves
the identity for *all* inputs, not by sampling). Solves `hard2_0051`, the
first known FALSE case with zero finite witness
([[infinite-model-capability]]). **Domain**: infinite carrier, no size
bound; polynomial degree ∈ [2, 8]. **Entry point**:
`al_find_linear_model` / `try_algebraic_linear_model`.

### 10. Classical ATP finite-model finding (evaluation only, not part of the fixed portfolio)
Per C2's own wording — "(for evaluation only) Vampire/Mace finite model
finding" — Vampire `-sa fmb` and Mace4 are run as an **independent classical
baseline** for comparison, not as a portfolio stage the solver depends on.
This is the tool used in [[order5-yield-probe]] and
[[order5-stratified-rerun]] as the coarse ATP-side filter. Not gated into
the solve pipeline above; reported separately as the "classical VBS" column.

## Empirical solve share (from `residual_family_analysis.md`, 1,667 order-≤4 problems)
| Family | Empirical FALSE solves | % of FALSE solves |
|---|---|---|
| 1. Exhaustive Fin≤3 (floor) | 697 | 82.2% |
| 3. Affine model search | 71 | 8.4% |
| 7. Backtracking model finder (mf2) | 39 | 4.6% |
| 6. Fast false-model probe | 36 | 4.2% |
| 8. SAT false-model finder | 3 | 0.4% |
| 2. Named witness tables | 2 | 0.2% |
| 4. Perturbed witness tables | 0* | — |
| 5. Structured Fin4-7 | 0* | — |
| 9. Algebraic-linear infinite model | 0* | — |

*Zero in this snapshot is a measurement artifact, not zero capability — the
merged-run JSON predates full integration of some stages (families 4/5 solve
rows may be folded into family 1's count if a structured/perturbed hit
happened to also be inside a Fin≤3 table; family 9 has one confirmed manual
solve, `hard2_0051`, not yet reflected in a fresh full re-run). Flagged in
[[residual-family-analysis]] as an open follow-up: **re-run the full merged
solver once, fresh, before finalizing these percentages for publication.**

## Mapping to PAPER_PLAN's C2 checklist
| PAPER_PLAN category | Covered by |
|---|---|
| exhaustive Fin 2–3 | Family 1 |
| structured finite tables | Families 4, 5 |
| affine/modular models | Family 3 |
| SAT/domain-propagation finite search | Families 7, 8 |
| quasigroup/Latin/idempotent modes | Family 7's `idem`/`qg`/`rows`/`cols` modes |
| algebraic-linear ℤ-module/companion-matrix | Family 9 |
| Vampire/Mace finite model finding (eval only) | Family 10 |

All seven categories PAPER_PLAN names are present. Nothing is missing from
the checklist; the open work is tightening the empirical counts (see above)
and widening parameter ranges for order-5 (see below), not adding new
family types.

## Known gaps / likely needed extensions for order-5
1. **Parameter ranges are order-≤4-tuned, not validated at order-5.** Affine
   modulus cap (40), mf2's Fin cap (11), SAT's Fin cap (7), and the
   algebraic-linear degree cap (8) were sized against what order-≤4 problems
   needed. Order-5 laws are structurally richer (more variables per side is
   possible, deeper nesting) and may need larger witnesses; this should be
   measured, not assumed — a natural next experiment once the order-5
   harness exists.
2. **The cheap pre-filter used in [[order5-stratified-rerun]] only used
   families 1, 3, 5** (pure-Python, no judge). Families 2, 4, 6, 7, 8, 9 are
   also import-safe pure-Python and could extend that filter for a sharper
   stratified sample next time.
3. **No cheap TRUE-side filter exists yet** — the stratified rerun's 95%
   TRUE-skew in survivors is a direct consequence; a fast template-based
   proof search (mirroring families 1-9's cheap/pure-Python nature) would
   symmetrize the pre-filter.

## Cost accounting (for the eventual "cost" column in C2's target table)
- Families 1, 2, 4, 5: sub-second, pure Python, no configurable budget.
- Family 3 (affine): sub-second to a few seconds depending on modulus cap.
- Family 6 (fast probe): 1.8s × 2 sizes ≈ 3.6s fixed.
- Family 7 (mf2): 240s budget (`MF2_PORTFOLIO_BUDGET`), ≈6.7% of the 3600s
  per-problem wall clock.
- Family 8 (SAT): 120s budget (`SAT_FINDER_BUDGET`), ≈3.3% of wall clock.
- Family 9 (algebraic-linear): sub-second (deterministic polynomial-gcd
  computation, no search).
- Family 10 (Vampire/Mace, eval only): whatever budget the baseline run
  uses — 3600s in the full EXPERIMENT_SPEC baselines, 2-40s in the cheap
  order-5 probes (deliberately much smaller, since those were yield probes
  not final baselines).

Total deterministic-portfolio worst-case cost per problem (families 1-9, if
every stage runs to its full budget without an early accept): roughly
240 + 120 + a few seconds ≈ 365s, well under the 3600s cap, leaving headroom
for the LLM proposer stage this paper is ultimately measuring against.
