# Session log — 2026-07-04

LLM-assisted countermodel construction for open order-5 equational implications.
This log records everything built and found in this session, the current state
of the paper, and the open levers.

---

## 1. Headline outcomes

- **Verification is clean and independent.** Certificates are checked by plain
  Lean (`lean_oracle.py`, `#print axioms` allowlist) and/or the competition
  judge — no pre-existing labels needed.
- **A previously-open pair was solved and formally verified** (`order5v2_1593`),
  but it also falls to a strengthened deterministic search, so it is a
  *verification/search* contribution, not an LLM-necessity one.
- **The hard survivors are provably outside the entire linear-model family**
  (finite affine AND infinite algebraic-linear), via a constraint derivation —
  a near-proof, not a search cutoff.
- **A neurosymbolic constructor works**: the LLM names a non-linear *family*, a
  deterministic engine exhausts its parameter space, Lean verifies the result.
- **LLM capability is demonstrated but not necessity.** On a controlled
  known-solvable set the LLM constructed a verified non-linear countermodel
  (`order5big_0584`); on the genuinely-open set it solved 0/24.
- **A characterized benchmark is being harvested in the background** from a
  3,179-pair pool (deterministic, resumable, shardable).

---

## 2. Artifacts built (all in `paper/scripts/`, certs in `paper/certs/`)

| File | Purpose |
|------|---------|
| `lean_oracle.py` | Plain-Lean verification oracle: bans `native_decide`/`sorry`/`axiom`, runs `lake env lean`, requires `#print axioms` ⊆ {propext, Quot.sound, Classical.choice}. The paper's principled verifier. |
| `baseline.py` | Strengthened deterministic FALSE-side baseline (affine `af_find`, `mf2` finder, SAT, algebraic-linear `al_`), tunable bounds, LLM off. Defines the frontier. |
| `linear_triage.py` | Derives EQ1's linear-coefficient constraints (`al_constraints`) and decides whether ANY linear op refutes the pair. Classifies LINEAR vs NON-LINEAR-REQUIRED. |
| `true_side_sweep.py` | Vampire prove (EQ1→EQ2 theorem?) + fmb (finite model?) at long budget; classifies THEOREM / COUNTERMODEL / OPEN. |
| `structured_search.py` | Symbolic half of the neurosymbolic loop: exhaustively searches an LLM-named non-linear ansatz `op(x,y,n,P)` over int/permutation params, sound self-verify, returns a specific failure diagnosis. |
| `harvest.py` | Resumable, shardable background characterizer over the cheap-screened pool → benchmark rows tiered LINEAR / SOLVED_FMB / THEOREM / HARD_NONLINEAR. |
| `extract_targets.py` | Pulls proposer-ready `{id:[eq1,eq2]}` sets from harvest output by tier (capability set = `SOLVED_FMB & not linear_refutable`; open set = `HARD_NONLINEAR`). |
| `proposer_o3.py` (extended) | o3 proposer. Modes: `finite`, `algebraic_linear` (infinite ℤ[α]), `structured_finite`. Linear-gate injects the constraint analysis; failure-witness feedback; robust JSON parse; token/cost logging; `--force-infinite`, `--struct-budget`. |
| `certs/Order5v2_1593.lean` | Symbolic ZMod-17 certificate for `1593` (see below). |

---

## 3. Results in detail

### 3.1 Verification & the 1593 solve
o3 proposed the affine model `x◇y = 8x + 7y (mod 17)` for `order5v2_1593`. The
explicit-table encoding timed out the judge (17⁵ `decideFin` > 120s). Rebuilt as
a **symbolic** certificate: EQ1 as a universal integer identity plus one modulus
fact (`linear_combination`), EQ2 refuted by a single witness — no enumeration.
Verified by `lean_oracle.py`: **PASS, 14.7s, axioms {propext, Quot.sound,
Classical.choice}, no sorry/native_decide** (an earlier `decide` version passed
at 161s, above the judge's 120s cap — which is exactly why the judge had
rejected a correct model).

**Caveat:** the strengthened affine search (`baseline.py` with the n-cap raised)
finds `1593` (and `6145`) on its own at Fin17. So `1593` is a worked example of
the verification win, **not** evidence the LLM does something search can't.

### 3.2 Strengthened baseline (on `pairs8`)
With mf2 240s, SAT to Fin8, affine to n≈21, algebraic-linear to degree 12: the
baseline solves **2/8** — exactly the two with linear counterexamples
(`1593`=8x+7y, `6145`=9x+2y, both mod 17). The other six survive everything
deterministic.

### 3.3 Provable non-linearity (linear triage)
`al_constraints` derives, from EQ1, the exact conditions a linear op
`a·x+b·y(+c)` must satisfy. Result across the 8: the 2 solved pairs have linear
refutations; **all 6 survivors have NO linear counterexample** — for `0073` the
only linear EQ1-model is right-projection (too strong); for the other five no
linear op satisfies EQ1 at all. Because infinite algebraic-linear models are the
same linear family, this rules out infinite-linear too. This is a near-*proof*
(structural), not a search cutoff — the strongest characterization we have.

### 3.4 TRUE-side sweep (survivors, 600s/direction)
All 6 survivors returned **OPEN**: not theorems, and Vampire's fmb found no
finite model. Genuinely hard both ways at 15× the original screen budget.

### 3.5 Neurosymbolic structured-ansatz constructor
Motivation: linear models are deterministically *derivable* (so no LLM needed);
non-linear models are not derivable and the raw table space is un-brute-able
(Fin>8). The LLM's unique job is naming the *structured family*; the solver
exhausts the small parameter space and Lean-verifies. Split matches the observed
failure mode (o3 is bad at full tables, better at naming structure).

### 3.6 Capability result (controlled set)
Test set = `SOLVED_FMB & not linear_refutable` (a non-linear countermodel
provably exists because Vampire fmb found one, but linear search missed it),
extracted by `extract_targets.py`. Breadth sweep, 6 pairs, 2 rounds:
**1 solve — `order5big_0584`**.
- Model (from the accepted table): `op(i,j) = 2·(j mod 2) + (i div 2)` on Fin 4.
- Genuinely non-linear; EQ1 holds ∀, EQ2 fails; judge **accepted**;
  independently re-verified.
- Interpretation: **capability confirmed** — the LLM constructs verified
  non-linear countermodels. `0584` is also fmb-solvable, so this isolates
  capability, it is not a necessity claim.

### 3.7 Necessity result (open set)
Test set = `HARD_NONLINEAR` (24 open pairs). Breadth sweep, 2 rounds, $6.45:
**0 solves.** Dominant failure: `NO parameter made EQ1 hold`. o3's proposed
families were overwhelmingly *affine-with-a-twist* (`permuted_affine_*`,
`quadratic_affine_mod_*`, `perm_shift`), which cannot thread the rigid EQ1
constraints. The one earlier win (`0584`) came from a structurally-novel family
(bit-decomposition), so **structural diversity is the lever and o3 does not
supply it unprompted.** Partial existence confound: these pairs also resisted
Vampire fmb, so many may have no small model.

### 3.8 Background benchmark harvest
Pool `order5_big_survivors.jsonl` = 3,179 cheap-screened pairs (unlabeled). The
cheap FALSE-only screen let many **theorems** through (first 5 sampled pairs
were all THEOREM at 4s). `harvest.py` tiers each pair and streams; the
`HARD_NONLINEAR` yield is ≈1.5% (≈48 from this pool), matching prior estimates.

---

## 4. Key numbers

| Metric | Value |
|--------|-------|
| `pairs8` solved by strengthened deterministic baseline | 2 / 8 (both linear) |
| Survivors provably outside the linear family | 6 / 6 |
| Survivors OPEN at Vampire 600s both directions | 6 / 6 |
| LLM capability set (known non-linear solvable) | **1 / 6 solved** (`0584`) |
| LLM necessity set (open `HARD_NONLINEAR`) | **0 / 24 solved** |
| `1593` symbolic cert (plain Lean) | PASS, 14.7s, clean axioms |
| Harvest pool size | 3,179 (many theorems; ~1.5% hard-nonlinear) |

---

## 5. Paper skeleton (honest framing)

Not "LLMs crack open problems" — the evidence doesn't support it. The defensible
paper is **resource + characterization + capability study**:

1. **Benchmark.** A contamination-free (self-generated, post-dating training),
   self-verified (Lean, no labels needed), deterministically-characterized set
   of open order-5 equational implications, tiered by solvability.
2. **Deterministic characterization.** Linear-model triage that *proves* pairs
   lie outside whole model families; a strengthened baseline; a stratification
   of what each method solves. This is the rigorous core.
3. **Neurosymbolic constructor + honest evaluation.** LLM-named ansatz +
   exhaustive symbolic search + Lean cert. Demonstrated capability (`0584`,
   worked example), cleanly isolated from existence; honest necessity-negative
   (0/24 open), with the narrow-vocabulary diagnosis.

Reviewer-facing strengths: contamination-free, ungameable verification;
difficulty defined *relative* to stated budgets with a robustness check (hard at
40s stays hard at 600s); non-linearity argued by structural proof, not cutoff.

---

## 6. Open levers / next steps

- **Structural-diversity prompt (bounded bet):** steer o3 off permuted-affine
  toward categorically different non-linear families (bit/coordinate
  decomposition, idempotent quasigroups, quandle/conjugation, piecewise) + a
  feedback line calling out affine-adjacent repeats. One re-sweep; may not move
  it (existence confound + possibly limited vocabulary).
- **Plain-Lean stamp for structured wins:** wire `0584`'s cert through
  `lean_oracle.py` (currently only the competition judge).
- **Scale the benchmark:** more sampled pools through `harvest.py` (deterministic,
  parallel) to grow the characterized set.
- **Consolidate toward the capability+benchmark paper** rather than chasing
  necessity, per the don't-tunnel principle.

---

## 7. Reproduction (cluster; Vampire at `paper/bin/vampire` or on PATH)

```bash
# verify the 1593 symbolic certificate
python paper/scripts/lean_oracle.py paper/certs/Order5v2_1593.lean

# strengthened deterministic baseline
python paper/scripts/baseline.py --pairs paper/problems/pairs8.json \
  --solver-dir scripts/my_solver_merged --out paper/results/baseline_pairs8.jsonl \
  --mf2-budget 240 --sat-sizes 5,6,7,8 --sat-budget 300 --al-deg-max 12

# linear-model triage (proves non-linearity)
python paper/scripts/linear_triage.py --pairs paper/problems/survivors6.json \
  --solver-dir scripts/my_solver_merged --maxn 19

# TRUE-side existence check
python paper/scripts/true_side_sweep.py --pairs paper/problems/survivors6.json \
  --prove-timeout 600 --fmb-timeout 600 --vampire paper/bin/vampire \
  --out paper/results/true_side_survivors.jsonl

# background benchmark harvest (shard 8 ways)
for i in $(seq 0 7); do nohup python paper/scripts/harvest.py \
  --pool paper/problems/order5_big_survivors.jsonl --solver-dir scripts/my_solver_merged \
  --out paper/results/bench_shard_$i.jsonl --prove-timeout 60 --fmb-timeout 60 \
  --vampire paper/bin/vampire --shard $i/8 > paper/results/harvest_$i.log 2>&1 & done

# capability test: extract known-solvable non-linear, run structured proposer
python paper/scripts/extract_targets.py --harvest paper/results/bench_shard_*.jsonl \
  --tier SOLVED_FMB --require-nonlinear --shuffle --limit 20 --out paper/problems/cap_test.json
python paper/scripts/proposer_o3.py --pairs paper/problems/cap_test.json \
  --reasoning-effort high --rounds 2 --solver-dir scripts/my_solver_merged \
  --judge-dir judge/ --cert-dir paper/certs --struct-budget 200000 \
  --out paper/results/proposer_cap_test.jsonl
```

*(Sandbox note: the workspace mount intermittently serves stale/truncated copies
of freshly-edited files; always parse-check on the cluster before a run:
`python -c "import ast; ast.parse(open('paper/scripts/proposer_o3.py').read())"`.)*
