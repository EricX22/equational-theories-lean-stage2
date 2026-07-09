# Session log — 2026-07-08

Building the benchmark: a graded, Lean-verifiable corpus of **Austin laws**
(magma laws with no nontrivial finite model but an infinite one), with a
deterministic construction baseline that grades each law by difficulty "rung."
This log covers the thesis, the pipeline, the scripts, the key findings, and the
first concrete result: the order-5 corpus fully graded.

---

## 1. Headline

- **The benchmark is real and populated.** The order-5 Austin corpus (130 laws
  from ETP's order_5.tex) grades to **110 Rung-2 + 18 Rung-4 + 0 Rung-1**
  (2 unaccounted), all confirmed no-finite-model. That alone exceeds the "~50
  problems" bar, with an **18-law hard frontier** (bigger than the ~10 we feared).
- **Random order-6 is a dead end; targeted generation is the volume engine.**
  Random 30k pool → 6 Austin, 0 Rung-4. Extending known Austin laws by one
  operation hits the Austin band ~500× more often, and extending the Rung-4 seeds
  is how we grow the hard tier.
- **The thesis needs no "only-LLM" claim.** It's a verifiable, contamination-free,
  graded benchmark of open construction problems — deterministic baseline as the
  difficulty ladder, LLMs measured against it. Distinct from order-≤4 (saturated
  by one ATP) because no single method solves all Austin laws.

---

## 2. Thesis (settled)

Equational-implication is undecidable in general. ETP resolved the order-≤4 graph;
finite cases fell to ATPs, and the rare infinite countermodels were hand-built —
that creative sub-task is the interesting part, and it was small, closed, and never
framed as a benchmark. We isolate it: **construct an infinite model for a law that
provably has no finite one (an Austin law)**, characterize the family, grade it by
a published construction suite, and extend it into the open order-5+ region. The
family is plausibly undecidable → no single method ever saturates it (durability).
Contribution = the benchmark + method + measurement, not resolving specific laws.

Grading = a **ladder of construction methods**, each law scored by the lowest rung
that solves it, relative to a *published, fixed* suite (reproducible):

- **Rung 1** translation-invariant model `a◇b = b + f(b−a)` (verified f).
- **Rung 2** greedy magma builder, verified on its full constructed domain.
- **Rung 4** resists 1 and 2 → open-to-us (the hard frontier). (Rung 3 = bespoke
  case-defined; not automated, so it folds into "open-to-us" for now.)

Include the easy rungs too — a benchmark is a graded *range*, not an unsolvable
residual; even Rung-2 laws are real work for a model to construct.

---

## 3. The pipeline (cheap → expensive; verified at each honest step)

```
generate  ->  cheap n<=3 screen  ->  TRIVIAL-STRIP  ->  fmb-CONFIRM  ->  GRADE
(random or   (drop small models)   (Vampire proves    (long fmb; drop    (TI=R1,
 targeted)                          x=y => trivial,     if a finite        greedy
                                    NOT Austin)         model appears)     =R2,
                                                                           else R4)
```

Order matters: the **trivial-strip must come before fmb** — a random order-6
`x=T` law (4 vars) is over-constrained, so ~99% have "no finite model" only
*because they are trivial* (entail x=y), which is NOT Austin. Stripping them via a
fast `L ⊨ x=y` proof (seconds) removes the majority before paying fmb. This bug —
fmb-confirming a trivial-dominated pile — is what made order-6 first look like a
dead end (10,832 candidates → 656 non-trivial → 6 Austin).

---

## 4. Scripts (paper/scripts/)

| File | Role |
|------|------|
| `order6_search.py` | generate order-6 `x=T` laws + cheap n≤3 screen + fmb; `--pool/--shard`; solver stage optional (near-useless at order-6). |
| `order6_strip_trivial.py` | fast Vampire `L⊨x=y` prove → drop trivial (the missing Austin filter). |
| `order6_grade.py` | confirm Austin (long fmb) + grade rung (TI → verified greedy → open). |
| `order6_targeted.py` | **targeted generation**: extend known Austin laws by one op; default seeds = `paper/problems/order5_seeds.jsonl` (committed, 130 laws). Recursively re-seedable for order 7+. |
| `order6_finish.sh` / `order6_targeted_finish.sh` | unattended watchers chaining strip→grade (and generate→strip→grade). |
| `al_general.py` | complete commutative-linear (Gröbner) subtraction; note linear ⇒ finite ⇒ not Austin, so it's a screen not a rung. |

TI solver + verified greedy builder live inside `order6_grade.py`. `order5_seeds.jsonl`
(the 130 order-5 laws) is committed so nothing depends on the reference-repo path.

---

## 5. Key findings this session

- **Random order-6 yield (30k pool):** 10,832 no-60s-model → 656 non-trivial
  (strip) → **6 Austin, all Rung 2, 0 Rung 4**. Genuine Austin ≈ 0.02% of pool;
  ~250k needed for 50, and ~0 Rung-4. Abandoned.
- **Trivial-strip is the missing filter:** 8/8 sampled random cheap-survivors were
  trivial; strip removes ~94% cheaply.
- **Targeted generation ≈ 500× yield:** one-op extensions of Austin laws are
  ~15% non-trivial-no-small-model vs random 0.02%. 130 seeds → ~4,300 extensions,
  77% pass the cheap screen. This is the volume engine and the Rung-4 source.
- **Translation-invariant is empty for these laws:** 0/10 known order-5 Austin laws
  (and 0 of the graded corpus) are TI-realizable — they need bespoke constructions.
  So Rung 1 = 0; TI is a valid *floor method* that this corpus sits above. (A
  populated Rung-1 floor, if wanted, must come from Austin pairs or a TI-targeted
  search.)
- **Order-5 corpus graded:** 130 laws, 0 trivial, 0 with a finite model →
  **{Rung 2: 110, Rung 4: 18}** (2 unaccounted). The 18 Rung-4 laws are the hard
  frontier (mix of ETP-confirmed Austin like 4916/41082 and open Table-2/3
  candidates).

---

## 6. Benchmark shape (current)

- **Body (Rung 2):** ~110 order-5 + targeted-order-6 additions — greedy-verifiable
  Austin construction problems.
- **Frontier (Rung 4):** ~18 order-5 + targeted-order-6 Rung-4 extensions — resist
  the published construction suite.
- **Verifiable:** every "solve" is a Lean-checkable model (or, for the baseline's
  Rung-2, a domain-verified partial construction).
- **Contamination-free / open:** order-5 Table-2/3 are unresolved by ETP; order-6
  targeted laws are novel (self-generated, post-training).

---

## 7. Caveats to carry into the writeup

- **"Rung 4" = beyond OUR suite**, not a universal claim — reproducible relative to
  the published methods. Some Rung-4 laws are confirmed Austin (Table 1), others are
  open candidates (Table 2/3).
- **"Non-trivial" = Vampire didn't prove x=y in the budget** — a few Rung-4 laws
  could be trivial-hard-to-prove; run a longer trivial-prove on the ~18 to firm up.
- **Greedy Rung-2 = domain-verified, not infinite-proven** — a valid partial magma
  on a large domain; the infinite step is the un-automatable frontier (on-thesis).
- **fmb-confirm at order-5 is essentially free-passing** (these are pre-established
  no-finite-model), so a short fmb timeout is fine there; order-6 needs the real
  confirm.
- Sandbox mount intermittently truncates freshly-edited scripts — parse-check on the
  cluster before every launch. sympy required for `al_general`.

---

## 8. Running / next

- **Running:** targeted order-6 pipeline (`order6_targeted_finish.sh`) —
  generate → strip → grade off the 130 order-5 seeds; expect a Rung-2 body plus
  Rung-4 extensions. Its final rung line lands in `order6_targeted_finish.log`.
- **Next:**
  1. Combine `o5_graded_*` + `tgt_graded_*` → the full graded corpus.
  2. Firm up the ~18 (order-5) + order-6 Rung-4 laws: longer trivial-prove +
     confirm which are ETP-confirmed Austin vs open.
  3. Recursively re-seed `order6_targeted.py --seeds-in tgt_graded` for order-7 to
     grow volume + frontier.
  4. LLM eval on the graded corpus (report highest rung reached), with the
     deterministic suite as the baseline.
- **Process hygiene:** the watchers detect stages via `pgrep -f order6_grade.py` /
  `order6_strip_trivial.py`, so don't run a manual strip/grade concurrently with a
  watcher — sequence them.

---

## 9. Reproduction (cluster)

```bash
# order-5 grade (the committed seeds; sharded, short fmb since pre-confirmed no-model)
python -u paper/scripts/order6_strip_trivial.py --in paper/problems/order5_seeds.jsonl \
  --vampire paper/bin/vampire --prove-timeout 10 --out paper/results/o5_austin.jsonl
for i in $(seq 0 7); do nohup python -u paper/scripts/order6_grade.py \
  --in paper/results/o5_austin.jsonl --vampire paper/bin/vampire \
  --fmb-timeout 20 --shard $i/8 --out paper/results/o5_graded_$i.jsonl & done

# targeted order-6 (volume engine), fully automated
nohup bash paper/scripts/order6_targeted_finish.sh > /dev/null 2>&1 &

# rung counts
cat paper/results/o5_graded_*.jsonl paper/results/tgt_graded_*.jsonl \
  | python3 -c "import sys,json,collections;print(dict(sorted(collections.Counter(json.loads(l)['rung'] for l in sys.stdin).items())))"
```
