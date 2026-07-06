# Session log — 2026-07-06

The session that found the paper's real thesis: **Austin laws/pairs** — a named,
ETP-studied family of implications that hold in every finite magma but fail in an
infinite one — as a verifiable, genuinely-open, LLM-worthy benchmark. Records the
full arc from "the finite regime has no LLM story" to a validated difficulty
filter, a concrete order-5 hard core, and an 80%-stood-up pairs pipeline.

---

## 1. Arc in one paragraph

Started by confirming the finite regime is a dead end for LLM necessity (finite
solvers own it). Pivoted to infinite-required countermodels; built `al_general`, a
*complete* Gröbner decision for the commutative-linear family (closed a ~44%
false-candidate leak). Tried constructing infinite witnesses from scratch — dead
end (non-linearity and rich identity theory are in opposition). Discovered ETP has
already named and partially studied exactly this family (**Austin laws**), leaving
a precise gap at order 5: **96 open laws** with no nontrivial finite model whose
infinite-model status ETP never attempted. Read ETP's construction toolkit
(translation-invariant magmas + greedy algorithm). Built and validated an
automated **difficulty filter** (greedy magma builder) that cleanly separates easy
(auto-constructible) from hard Austin laws — proven by 4916/41082, which have
models yet defeat it. Isolated the order-5 hard core (**10 laws, ~6 modulo
duality**), robust across two builders of different strength. Then generalized the
builder to **pairs** and concept-validated it against 820 ground-truth Austin
pairs; it works but needs hardening before scaling.

---

## 2. The pivot chain (why we are where we are)

- **Finite regime: no LLM necessity.** Capability band 74; unconstrained finder
  solves 64/74; the 10 misses were fmb-confirmed Fin8–9 (finder-budget gaps, not
  frontier); the one LLM "win" (0584) is mf2-solvable. Zero LLM-necessity.
- **Infinite regime is the only niche** where finite solvers (SAT/mf2/fmb)
  structurally can't compete.
- **`al_general` (built this session):** a linear model x*y=a*x+b*y over a
  commutative ring is decided *completely* by ideal membership — a counterexample
  exists iff some EQ2 constraint ∉ ideal(EQ1 constraints), via a Gröbner basis. No
  caps. On 300 pairs it reclaimed 131 that the old idempotent-only stage leaked as
  false candidates. This is the honest linear subtraction.
- **Construction-from-scratch: dead end.** Non-linear arithmetic magmas are
  identity-poor (x+y²+1 satisfies *zero* identities; the richest, 2max−min, only
  idempotent+commutative — too weak for a finite/infinite gap). Same root cause
  that makes search hard.

---

## 3. The find: Austin laws (ETP)

An **Austin law** = a single law with infinite models but no nontrivial finite
model (equivalent to Eq2 finitely, not infinitely). Austin laws have order ≥5
(none below, proven). ETP order-5 classification of 57,882 laws:

| | |
|---|---|
| trivial-only | 19,392 |
| have finite models | 38,360 |
| **only trivial finite models** | **106** |
| — confirmed Austin (Table 1) | **10** (models proven + Lean-formalized) |
| — **open** (Table 2): no finite model, infinite status UNKNOWN, unattempted | **96** |
| finite status unknown (Table 3) | 24 |

The **96 open laws are the gift**: ETP already proved the hard half ("no finite
model"); the open task is exactly the creative, verifiable infinite construction.
The general case is **Austin pairs** (EQ1⊨EQ2 finite-only, EQ2≠trivial): ETP lists
**820** at order ≤4 (`data/Austin_implications.txt`), so the pair-space is far
richer than single laws.

---

## 4. The construction toolkit (ETP `infinite_magma_constructions.tex`)

- **Translation-invariant magmas:** carrier = abelian group, `a◇b = b + f(b−a)`.
  Any law collapses to a **univariate functional equation in f**; solve f on ℤ by a
  **greedy algorithm** (extend a finite partial solution to cover each new point
  using fresh "novel" elements). Reduction is mechanical (we automated it); the
  creative part is the per-law partial-solution invariant + extensibility proof.
- Linear f gives finite models (Lefschetz) → excluded for Austin; needs non-linear
  f. Not all Austin laws are translation-invariant (Kisielewicz's used case-defined
  magmas on ℕ via powers of primes — we reproduced 28770's model and verified it).

---

## 5. The difficulty filter (built + validated this session)

**Greedy magma builder.** Build a magma satisfying a law by processing triples over
a growing carrier; undefined subproducts get fresh novels; the top is forced to the
target. "Survives" = model built = **EASY**; "contradicts" = **beyond this builder**.

Validation that it *discriminates* (not vacuous):
- Contradicts immediately on a provably-trivial law (no model exists).
- On the **10 known Austin laws**: survives 8, contradicts 2 (**4916, 41082** — a
  dual pair, models PROVEN by ETP) ⇒ **hard Austin laws exist and are delineable**.

**Strengthened builder** (naive + per-triple backtracking that searches operand
*reuse* to route around collisions, not just spawn novels). Impl gotchas: force the
top product to the target (not chosen from candidates); search only operands;
commit per-triple via generator abandonment. Validated: same 8/2 on known Austin.

**Decisive result — order-5 hard core is robust.** On the 96 open laws, both the
naive and strengthened builders (both orientations) return the **same 10 hard
laws**: `[7587, 9663, 10222, 12073, 12883, 22619, 33020, 35836, 36487, 38316]`.
Reclaimed 0, added 0. Vampire proves none of the 10 trivial ⇒ all are **hard-Austin
candidates**. Modulo duality (4 dual-pairs + 2 singletons) ≈ **6 independent hard
problems**. The 86 survivors are likely *easy* Austin laws — confirming them
mechanically resolves ~86 open ETP problems (a second contribution).

**Honest caveats:** "survives" is a reliable EASY signal; "contradicts" is an upper
bound on truly-hard (an even stronger method — the real ETP greedy-with-invariant,
or a translation-invariant-f solver — could reclaim a few). "Hard for our builder"
is not yet "proven Austin" — confirming requires actually constructing the models.

---

## 6. Pairs pipeline (80% stood up)

- **Candidate generation: done.** `infinite_screen` finds Austin-pair candidates
  (no finite countermodel + not a theorem + not linear, via `al_general`) — exactly
  what our original harvest was sampling.
- **Splitter (pair-builder): built + concept-validated, needs hardening.**
  Generalized the builder to satisfy EQ1 everywhere and violate EQ2 somewhere. On
  25 known Austin pairs it constructed genuine countermodels for **7** — the
  concept works. But 16 came back EQ1_FAIL (builder too weak, since these provably
  have models). Two fixes needed: (a) **symmetric** EQ1-satisfaction (both sides,
  not eval-left-force-right), (b) **n-variable** support (currently hardcoded for
  3 vars / triples; many laws use 4). Same hardening the single-law builder needed.
- **Validation harness ready:** the 820 ground-truth Austin pairs — a competent
  pair-builder should reconstruct a large fraction; whatever it can't (that has a
  model) are the hard-pair analogues of 4916/41082.

---

## 7. The paper thesis (now concrete and defensible)

A **graded, verifiable benchmark of open magma-construction problems** — Austin
laws/pairs — where automated methods (finite search, Vampire, al_general, greedy
builders) resolve the easy tier, and a hard residual requires per-instance creative
infinite construction that no single fixed procedure captures. Two tiers:

1. **Automated tier** — resolve the easy majority (e.g. the 86), extending ETP.
2. **Hard tier** — the residual (order-5: the 10; plus pairs/order-6 volume),
   where we test LLMs against expert-level construction, with Lean-verifiable
   answers on genuinely open problems.

Not "only an LLM can do it" (any found construction is deterministically
replayable) — it's competition-math-with-a-checker: solutions are verifiable, but
*finding* them per-instance is the test, and no single procedure sweeps the set.

---

## 8. Artifacts (paper/scripts/)

`al_general.py` (complete commutative-linear decision, wired as infinite_screen
tier-4), `infinite_screen.py` (4-way subtraction screen, --pool/--shard),
`fmb_probe.py`, `step0_frontier.py`, `families.py`. The greedy builders + pair
builder are prototyped inline (to be consolidated into a `constructor.py` module).
`order5_pool_infinite.jsonl` = 60k fresh pairs (seed 20260706).

Key reference data now in play: `reference/equational_theories/blueprint/src/chapter/
{infinite_models,order_5,infinite_magma_constructions,hard}.tex` and
`data/{Austin_implications.txt (820 pairs), equations.txt, eq_size5.txt}`.

---

## 9. Next steps

1. **Harden the pair-builder** (symmetric EQ1 + n-variable), validate it
   reconstructs most of the 820 known Austin pairs. ← immediate next
2. **Scale to volume:** point screen + hardened builder at order-5 pairs; the
   builder-hard residual (that isn't linear/finite/theorem) = the pair benchmark.
3. Consolidate the greedy builders into a real `constructor.py`; add a translation-
   invariant-f solver as a stronger baseline tier.
4. Confirm the 86 order-5 survivors are Austin (extract/verify models) — the
   automated-tier contribution.
5. Lean-verify one hard-tier construction end to end (worked anchor).
6. Only then: LLM eval on the hard tier, with deterministic baselines reported
   alongside (fair comparison on open problems).

---

## 10. Caveats carried forward

- Sandbox mount intermittently serves truncated copies of freshly-edited files;
  parse-check on the cluster before runs. sympy required wherever `infinite_screen`
  runs (tier-4 silently leaks without it).
- Builder "hard" = beyond *our* automation, an upper bound on truly-hard until a
  stronger baseline (or an actual construction) confirms each case.
- Budget/orientation matter: classify EASY if greedy survives in *either*
  orientation; HARD only if both contradict.
