# Session log — 2026-07-09

The sieve becomes a prover. Two changes: (1) every law now gets a *proved status*
instead of a search-failure label; (2) the rung ladder is demoted from the
benchmark's spine to a side attribute.

---

## 1. Why Austin laws and not "hard true implications"

`L |= E` is semi-decidable — Birkhoff completeness means equational proof search
finds the proof if one exists. "A finite countermodel exists" is *also*
semi-decidable — enumerate finite magmas. So:

- every TRUE instance is settled by enough compute;
- every FALSE-with-a-finite-countermodel instance is settled by enough compute.

If those were the only two cases, equational implication would be decidable (run
both procedures in parallel). It is not decidable. Therefore the undecidability
lives *entirely* in the third case: **false, with no finite countermodel**. For
the target `E = (x=y)` that class is exactly the **Austin laws**.

Consequence for benchmark design: a benchmark of true implications, or of
finite-countermodel implications, measures search efficiency against a complete
procedure, and its difficulty evaporates as hardware improves. There is always a
"long enough." For Austin laws there is no long enough — both complete
semi-procedures diverge. They are the only class whose difficulty is method-bound
rather than compute-bound. (Careful phrasing: no *individual* law is undecidable;
what is undecidable is the uniform problem, and this is the subfamily where no
uniform procedure terminates.)

This is also why our own finite-regime result was a dead end rather than a
failure: fmb solved essentially the whole finite band, exactly as the theory
predicts it eventually must.

Caveat that keeps us honest: existence of a nontrivial model is *sometimes*
mechanically provable (saturation, below). So the benchmark task must be stated
as **"produce an explicit, Lean-verifiable infinite magma"**, not "does a
nontrivial model exist". Existence is sometimes mechanical; construction isn't.

---

## 2. `prove_status.py` — the three provers

Replaces "no small model + Vampire didn't prove x=y" (two failures-to-find) with
theorems. Each law `x = T` lands in exactly one bucket:

| status | meaning | proved? |
|---|---|---|
| `TRIVIAL` | `L |= x=y` | yes — implication TRUE |
| `HAS_FINITE_MODEL` | fmb exhibits a nontrivial finite model | yes — FALSE, finite |
| `AUSTIN_PROVEN` | (i) ∧ (iii) | yes — FALSE, infinite |
| `NO_FINITE_MODEL` | (i) proved, existence open | no |
| `SATISFIABLE_ONLY` | (iii) proved, (i) open | no |
| `OPEN` | nothing proved | no |

**(i) No nontrivial finite model — pigeonhole, mechanized.** Pick a subterm `S`
of `T` containing `x`. If `x ↦ S(x)` is injective then in a *finite* model it is
surjective (pigeonhole). Surjectivity is an ordinary first-order sentence, so it
can be handed to Vampire as an axiom — that is how we say "finite" to a prover
that cannot express finiteness. If Vampire proves `x=y` from `L + surj(S)`, then
every finite model of `L` is trivial. Machine-checked, in seconds.

Injectivity comes two ways:

- **tier 1 (free, syntactic):** if `S` contains *every* occurrence of `x`, then
  `T = C[S]` with `C` x-free, and the law `x = C[S(x)]` *is* a left inverse.
  Injectivity needs no proof. Candidates = subterms on the root→LCA path of the
  x-occurrences, innermost first.
- **tier 2 (proved):** any other `x`-containing subterm, with Vampire asked to
  prove `S(x₁)=S(x₂) → x₁=x₂` first.

Soundness: `surj(S)` is asserted only inside the finite-model argument. The
conclusion is "every finite model of L is trivial", never `L |= x=y`.

**(iii) Existence — saturation.** `vampire -sa otter` on `L + ∃u,v. u≠v`. A
complete saturation that terminates without a refutation proves the theory
consistent, hence (Gödel) that a nontrivial model exists. Vampire prints
`SZS status Satisfiable` *only* when completeness was preserved — otherwise it
says "Refutation not found, incomplete strategy" — so the status line is itself
the completeness certificate; we assert both conditions. The saturated clause set
is dumped to `paper/certs/saturation/<sha>.sat` as an archivable, finitely
checkable witness. (Earlier `--mode casc_sat` is an *invalid Vampire mode* and
was silently producing fake timeouts.)

Negative controls pass: `x = x◇(x◇x)` and `x = (x◇y)◇x` (both hold in the
2-element left-projection magma) yield no (i)-witness.

---

## 3. Results so far

**10/10 ETP-confirmed order-5 Austin laws:** claim (i) machine-proved in seconds
(4916, 15535, 17522, 20034, 22455, 41082, 30591, 28770, 25964, 22818). ETP proved
these by hand, per law, in Lean. Example witness for 28770: `surj` on
`((y◇y)◇y)◇x`.

**The 18 order-5 "Rung-4" frontier laws**, at a *3-second* timeout per prover
(16 classified in the sandbox; nothing tuned):

```
   2  AUSTIN_PROVEN     no finite model + a nontrivial model exists => infinite
  10  NO_FINITE_MODEL   (i) is a theorem; existence still open
   4  OPEN              neither
```

The 2 proven Austin are 4916 and 41082 — proved end-to-end by machine, with no
construction and no hand-proof. Both are ETP Table-1 laws with published
constructions, so they are *calibration*, not frontier.

The 4 `OPEN` laws are exactly those whose x-occurrences straddle the root, so the
free (tier-1) witness degenerates to `S = T` and tier-2 needs a real injectivity
proof it did not find in 3s. Longer timeouts are the first thing to try.

Nothing in the corpus turned out `TRIVIAL`, which retroactively validates the
`order6_strip_trivial.py` stage.

---

## 4. Rungs, demoted

The rung ladder conflated two different things:

- **status** — a fact about the law (theorem or open question);
- **baseline** — a fact about *us* (which of our published constructions works).

"Rung 4" meant "beyond our suite", which is not a claim about difficulty and was
being read as one. Worse, 4916/41082 sat in Rung 4 while having published ETP
constructions. So `prove_status.py` records the two axes separately and
`status_report.py` reports them separately.

The benchmark's best instances are the intersection:

> **`AUSTIN_PROVEN` ∧ `baseline = open_to_us` ∧ no published construction.**

A model *provably exists*, is *provably infinite*, and nothing anyone has
published writes it down. Existence is settled mechanically; construction is the
task. That is the cleanest possible framing of the LLM's job, and it removes the
risk of asking a model to construct an object that may not exist.

---

## 5. Scripts

| File | Role |
|---|---|
| `prove_status.py` | trivial-prover + (i)-prover (pigeonhole/surjectivity) + saturation existence; emits status, witness, cert, baseline. `--selftest <vampire>` runs the known-answer controls. |
| `seeds_from_status.py` | pick laws by proved status: seeds for the next order, or the unsettled set for a long retry |
| `status_report.py` | merged status x baseline summary (strongest verdict per law); writes `final_status.jsonl` + `gold.jsonl` |
| `overnight.sh` | the whole loop: classify -> harvest -> classify the new laws -> retry -> report |

Two engineering notes that cost real time:

- **A truncated Python file still compiles.** The sandbox mount silently truncated
  `prove_status.py` mid-file; it lost only its `if __name__ == "__main__"` block, so
  `py_compile` passed and the script exited 0 having done nothing. Parse checks are
  not enough. `prove_status.py --selftest` runs the provers on laws with known
  answers (two negative controls + law 4916) and `overnight.sh` refuses to start
  without it.
- **`prove_status.py` appends, never truncates.** Shards read each other's outputs
  via `--skip` to resume; a shard opening its own output with `"w"` would drop laws
  a sibling had just skipped. `status_report.py` dedupes, keeping the strongest
  verdict per law.

Ordering inside `classify()`: trivial -> (i)-prover -> **fmb only if (i) failed** ->
saturation. Once (i) is a theorem there provably is no finite model, so running a
finite model builder on it is pure waste. That reorder is most of the speedup on a
big pool.

## 6. Reproduction (cluster)

```bash
nohup bash paper/scripts/overnight.sh > /dev/null 2>&1 &
tail -f paper/results/overnight.log
```

Stages: preflight+selftest -> classify order-5 -> classify existing order-6 ->
`ROUNDS` x (extend the proved-Austin laws by one op, cheap-screen, classify the new
laws) -> long retry on everything unsettled -> merged report. Every stage is
wall-clocked and every law is flushed as it is decided, so a stage that runs out of
time still contributes what it proved; re-running resumes via `--skip`.

Knobs: `SHARDS TMO_FAST TMO_SLOW TMO_HARD ROUNDS SEED_CAP S1_MAX..S4_MAX`, and
`R=/tmp/rt` to smoke-test into a scratch results dir.

Outputs: `paper/results/final_status.jsonl` (the corpus), `paper/results/gold.jsonl`
(proved Austin + no construction from our suite), `paper/certs/saturation/*.sat`
(the saturated clause set behind every existence proof).

## 7. Next

1. Full corpus pass (128 order-5 + the targeted order-6 candidates) at 60–120s.
   Report the trichotomy; that number replaces every rung count in the paper.
2. Longer/tier-2 push on the 4 `OPEN` laws.
3. Grow `AUSTIN_PROVEN ∧ open_to_us` — that's the gold set, and targeted
   generation off the Austin seeds is the volume engine for it.
4. Formalize the pigeonhole lemma (finite + injective ⇒ surjective) once in Lean,
   so the (i)-proofs can be replayed as Lean theorems rather than trusted TPTP.
