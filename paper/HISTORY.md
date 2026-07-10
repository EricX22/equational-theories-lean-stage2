# History — condensed session log

Four session logs (2026-07-04, 07-06, 07-08, 07-09) compressed to what a reader
needs. Originals live in `attic/logs/` for provenance. Read `HANDOFF.md` first;
this file only explains *how we got here*, including the wrong turns, because
several of them are still traps.

---

## Phase 0 — the competition solver (pre-pivot)

The repo began as an ETP-style solver for order-<=4 equational implications:
completion engine, SAT/CDCL finite-model finder, affine and quasigroup families,
LLM "waypoint" proposer. It works. Everything from that era now sits in
`attic/finite_regime/`.

The finding that ended the phase: **the finite regime has zero LLM-necessity.**
An unconstrained model finder solves 64/74 of the capability band, and the 10
misses are Fin8-9 budget gaps confirmed by an fmb probe, not a frontier. The one
apparent LLM win (0584) is solvable by the plain finder. There was no story.

## Phase 1 — the pivot to infinite countermodels (07-06)

If finite countermodels are found by search, the only place a model can add value
is where **no finite countermodel exists**. That is the Austin family: laws with
infinite models but no nontrivial finite one. They exist only at order >= 5.

Reference point: the Equational Theories Project (ETP) classified order-5 laws
(`reference/.../order_5.tex`). Of 57,882 laws, 106 admit only trivial finite
models; **10 are confirmed Austin** (their Table 1), 96 remain open (Table 2),
24 unknown (Table 3).

## Phase 2 — build a corpus (07-08)

Generate order-6+ Austin candidates and grade them by which deterministic
construction builds a model. Two lessons, both expensive:

- **Random order-6 sampling is a dead end.** 30k pool -> 6 Austin laws, none hard.
- **The trivial-strip is the missing filter.** A random `x = T` law with 4
  variables is over-constrained: ~99% have "no finite model" only because they are
  *trivial* (they entail `x=y`), which is not Austin. Stripping those with a fast
  `L |= x=y` proof must happen **before** any expensive model search. Failing to do
  this made order-6 look barren.
- **Targeted generation is the volume engine** (~500x yield): extend a known
  Austin law by one operation. The no-finite-model mechanism is largely inherited.

Graded the 130-law order-5 corpus into a "rung" ladder (translation-invariant /
greedy builder / open-to-us). 110 / 18 / 0.

## Phase 3 — the sieve proves nothing (07-09)

A critique landed and it was right. "No small model found" + "Vampire didn't prove
`x=y` in the budget" are two *failures to find*. Stacking them is not a theorem.
The whole corpus was a candidate selector wearing a proof's clothes.

Three fixes, in order of importance:

1. **The (i)-prover.** Claim (i) = "every finite model of `L` is trivial" is now
   machine-proved per law, in seconds, by a pigeonhole argument mechanized as a
   first-order query. See `HANDOFF.md` §"The three provers".
2. **Saturation as a baseline.** `vampire -sa otter` decides *existence* of a
   nontrivial model outright for some laws. It was missing from the portfolio, and
   it is exactly what ETP used to establish their Table 1. (The mode we had been
   using, `--mode casc_sat`, is not a valid Vampire mode and was silently
   producing fake timeouts.)
3. **Rungs demoted.** The ladder conflated *status* (a fact about the law) with
   *baseline* (a fact about our construction suite). They are now separate columns.

## The wrong turns, preserved deliberately

These cost hours and would cost them again.

- **"Let logic tell you the survivors must be infinite."** Both premises were
  failures-to-find. Wrong.
- **"ETP proved their 10 Austin laws by hand in Lean."** They did not. From
  `order_5.tex`: *"Vampire's decision procedure finished without finding an
  implication to Equation 2 for 10 equations ... Hence, they must be Austin laws"*
  and, of the open 96, *"No effort was made to build infinite models."* Only 28770
  has a published construction (Kisielewicz). ETP's Table 1 **is** the saturation
  argument.
- **"Saturation terminating means the model is free."** Read `x = T` as the rule
  `T -> x`; termination is free (the RHS is a variable), so only confluence can
  fail. I claimed saturation certifies confluence of that one rule. It does not:
  law 4916's rule has two non-joinable critical pairs, and the witness is
  hand-checkable (see `HANDOFF.md`).
- **"...so the model is NOT extractable."** Also wrong, and for a subtler reason:
  Vampire *did* derive both critical pairs by superposition and closed with a
  **four-rule completed system**. Saturation here is Knuth-Bendix completion
  succeeding. The confluence check was pointed at the wrong rule set. This is
  currently **unresolved** and is the top item in `HANDOFF.md`.
- **A vacuous empirical test.** "Random ground terms normalize consistently, so the
  rule is well-behaved" -- random terms contain no redex at all (the pattern is 6
  symbols deep), so every check passed vacuously. Critical pairs are the
  non-vacuous version. Sample where the rule *fires*.

## Infrastructure lessons

- **A truncated Python file still compiles.** The sandbox mount silently truncated
  `prove_status.py` mid-file; it lost only its `if __name__ == "__main__"` block,
  so `py_compile` passed and the script exited 0 having done nothing. Parse checks
  are not enough -- `prove_status.py --selftest <vampire>` runs the provers against
  known answers, and `overnight.sh` refuses to start without `SELFTEST OK`.
- **Shards must append, never truncate.** They read each other's output via
  `--skip` to resume; opening your own output with `"w"` silently drops laws a
  sibling already skipped.
- **Check the reject logs before assuming you are search-bound.** The single
  biggest false-side win of the whole project was one missing
  `set_option maxRecDepth` in the Lean emitter, which had been causing the judge to
  reject ~28 counterexamples we had already found.
