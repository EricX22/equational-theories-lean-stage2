#!/usr/bin/env python3
import argparse, sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "scripts", "my_solver_merged"))
from solver import mf2_Finder  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True)
ap.add_argument("--eq1", required=True)
ap.add_argument("--eq2", required=True)
ap.add_argument("--n", type=int, default=12)
ap.add_argument("--budget", type=float, default=15.0)
args = ap.parse_args()

t0 = time.time()
f = mf2_Finder(args.eq1, args.eq2, args.n)
table = f.solve(deadline=time.time() + args.budget)  # general mode: no qg/idem
dt = time.time() - t0
print(f"{args.id} n={args.n} GENERAL: {'FOUND' if table else 'miss'} ({dt:.1f}s)")
