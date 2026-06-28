"""NOT THE SOLVER. Placeholder only.

The paper baseline is frozen as a git ref, not a file copy, because the Cowork
dev sandbox truncates the ~175 KB solver.py over the mount (a copied file came
out cut mid-statement at line 4530). The git object store is intact, so the
frozen baseline is materialized at run time via:

    git show <FREEZE_REF>:scripts/my_solver_merged/solver.py

See README.md in this directory for the pinned ref. run_ours.py does this
automatically; do not import this placeholder.
"""
raise RuntimeError(
    "paper/solver_frozen/solver.py is a placeholder. The baseline is a git ref "
    "(see paper/solver_frozen/README.md); run_ours.py materializes it from git."
)
