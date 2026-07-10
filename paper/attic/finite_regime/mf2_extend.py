#!/usr/bin/env python3
"""Push the mf2 backtracking finder past the portfolio's Fin<=11 cap, on
the validated hard order-5 pairs, to check whether any of them just needed
a slightly bigger finite domain (idem+qg mode, matching the known
residual-family pattern) before crediting them as needing something exotic."""
import argparse, json, sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "scripts", "my_solver_merged"))
from solver import mf2_Finder  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True)
ap.add_argument("--eq1", required=True)
ap.add_argument("--eq2", required=True)
ap.add_argument("--sizes", default="12,13,14")
ap.add_argument("--per-size-budget", type=float, default=10.0)
args = ap.parse_args()

for n in [int(x) for x in args.sizes.split(",")]:
    t0 = time.time()
    try:
        f = mf2_Finder(args.eq1, args.eq2, n)
        table = f.solve(deadline=time.time() + args.per_size_budget, qg=True, idem=True)
    except Exception as e:
        print(f"{args.id} n={n}: ERROR {e!r}", file=sys.stderr)
        continue
    dt = time.time() - t0
    if table is not None:
        print(f"{args.id} n={n}: FOUND counterexample! ({dt:.1f}s) table={table}")
    else:
        print(f"{args.id} n={n}: miss ({dt:.1f}s)")
