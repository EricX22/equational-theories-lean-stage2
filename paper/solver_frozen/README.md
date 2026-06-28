# Frozen paper baseline (git-ref freeze)

The paper measures against a **frozen** version of the competition solver
(`scripts/my_solver_merged/solver.py`) so results stay reproducible while the
competition solver keeps changing.

## How the freeze works
The baseline is pinned as a **git ref**, not a copied file. `run_ours.py`
materializes it at run time:

```
git show <FREEZE_REF>:scripts/my_solver_merged/solver.py
```

- `FREEZE_REF` default: **`ef84234`** (`ef842345e2676f5a29eea5c6e607facf3397bb9c`,
  frozen 2026-06-28, commit "freeze: paper baseline solver" — 4561 lines, includes
  the working-tree edits that were uncommitted at first freeze). Override with
  `run_ours.py --solver-ref <sha>`.
- `solver.py` in this directory is a **placeholder that raises** — do not import it.

## Why a git ref instead of a copied file
The Cowork dev sandbox truncates the ~175 KB `solver.py` over the mount: a
straight `cp` produced a file cut off mid-statement at line 4530. The git object
store is not truncated (`git show` returns the complete, compiling file), so a
ref freeze is the reliable mechanism here.

## Note
**Re-freeze deliberately.** The baseline is now a clean committed ref
(`ef84234`, no uncommitted working-tree drift). Bump `FREEZE_REF` in
`run_ours.py` only when you intend to move the baseline, and record the new SHA
+ date above.
