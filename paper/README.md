# paper/ — research track (isolated from the competition solver)

This tree is the **paper** workstream. It is deliberately walled off from the
competition submission so the two can evolve independently.

## The wall (why this is safe)
- The competition submission is whatever directory `scripts/submit.py
  --submission <dir>` is pointed at (the solver folder). It never touches
  `paper/`, so nothing here can affect a submission.
- `solver_frozen/solver.py` is a **frozen copy** of
  `scripts/my_solver_merged/solver.py` at a known git SHA (see
  `solver_frozen/PROVENANCE.txt`). The paper measures against this snapshot so
  results stay reproducible while the competition solver keeps changing.
  Re-freeze only deliberately, and bump the provenance file when you do.
- Code in `paper/scripts/` imports **nothing** from the competition solver.

## Layout
```
paper/
  EXPERIMENT_SPEC.md       full experiment design (solved-by matrix, baselines)
  solver_frozen/           README.md (git-ref freeze) + placeholder solver.py
  problems/                hard1/2/3 + true_misses_18 (copied from examples/)
  scripts/
    etp_terms.py           shared term parser + TPTP/LADR emitters
    build_tptp.py          jsonl -> TPTP .p files (Vampire/E)
    run_baselines.py       drive Vampire/E/Prover9/Mace4 -> baselines_<set>.jsonl
    run_ours.py            frozen solver, ENABLE_LLM off/on -> ours_<mode>_<set>.json
    build_matrix.py        join everything -> solved_by_matrix_<set>.csv
    analyze.py             coverage, VBS, uniquely-solved set, two-frontier view
  tptp/                    generated {id}_true.p / {id}_false.p (+ index.jsonl)
  results/                 baseline + ours runs, solved_by_matrix.csv
```

## The frozen baseline (git ref, not a file copy)
The paper baseline is pinned as git ref **`ef84234`** (clean commit, 4561 lines);
`run_ours.py` materializes it via `git show`. A copied file is unreliable here
because the Cowork sandbox truncates the ~175 KB solver over the mount. See
`solver_frozen/README.md`.

## Pipeline (all scripts built & dry-tested)
```
# 1. encode for ATPs
python paper/scripts/build_tptp.py   paper/problems/hard3.jsonl --out paper/tptp
# 2. classical baselines (needs vampire/eprover/prover9/mace4 on PATH)
python paper/scripts/run_baselines.py paper/problems/hard3.jsonl \
       --out paper/results/baselines_hard3.jsonl --timeout 60
# 3. our frozen solver, LLM off and on (needs the Lean judge env)
python paper/scripts/run_ours.py     paper/problems/hard3.jsonl --runs both \
       --solver-ref ef84234 --out-dir paper/results
# 4. join into the matrix
python paper/scripts/build_matrix.py --problems paper/problems/hard3.jsonl \
       --baselines  paper/results/baselines_hard3.jsonl \
       --ours-nollm paper/results/ours_nollm_hard3.json \
       --ours-llm   paper/results/ours_llm_hard3.json \
       --out        paper/results/solved_by_matrix_hard3.csv
# 5. tables + headline uniquely-solved set
python paper/scripts/analyze.py paper/results/solved_by_matrix_hard3.csv \
       --unique-out paper/results/uniquely_solved_hard3.jsonl
```
Headline: `uniquely_solved_by_llm = ours_llm ∧ ours_used_llm ∧ judge_ok ∧
¬classical_vbs ∧ ¬ours_nollm`.

Status: encoder, parsers, matrix join, and analysis are unit/mock-verified.
`run_baselines.py` needs the ATP binaries and `run_ours.py` needs the Lean judge
— both run in the real environment, not the dev sandbox.

## LLM model (paper A/B)
The competition runs `gpt-oss-120b`; diagnosis showed the waypoint stage's
bottleneck is **proposal quality** (~97% of proposed chains failed verification,
only 2/400 reached the judge), so the paper swaps in a stronger model.

`run_ours.py` defaults to **`paper/config.paper.json`**, which routes the LLM
stages to **`openai/o3`** (high reasoning effort) via OpenRouter — keeping the
competition `pipeline/config.json` untouched. Set the key first:
```
export OPENROUTER_API_KEY=sk-or-...
```
Swap `llm.model` to `openai/o4-mini` / `openai/o3-mini-high` or lower
`reasoning_effort` to control cost.

Plan: controlled A/B — run the frozen solver design unchanged with o3 to measure
the model effect, *then* loosen the waypoint granularity contract (coarse
waypoints + verifier-fills-gaps) and measure that increment separately.

**Residual-only o3 (cost):** `--runs both` first runs the deterministic no-LLM
baseline (no o3 cost), then seeds the o3 run from it so the harness skips the
~96% already solved and o3 only touches the residual (~26 on hard3). This is
sound because the solver runs its deterministic stages before the LLM gate, so
anything the no-LLM run solved is solved identically with `used_llm=False`.
Crucially the baseline must come from the frozen `ef84234`, NOT the older
`pipeline/results/*` runs (those predate deterministic-side gains and would
misattribute them to the LLM). `--no-residual-seed` forces the full set through
the o3 path.

## Still to do
- A/B the o3 swap on hard3, then the granularity redesign (the gate).
- Contamination control: held-out laws + recall probe (per EXPERIMENT_SPEC §1).
