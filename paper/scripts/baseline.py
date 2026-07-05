#!/usr/bin/env python3
"""Strengthened finite-search baseline (NO LLM) for the order-5 hard set.

Purpose: make the "tractable finite-model frontier" a concrete, runnable object.
We run every DETERMINISTIC false-side finder in the solver -- with the LLM
disabled and with deliberately *raised* bounds -- and report, per pair, whether
the finite baseline finds a self-verified counterexample, which stage found it,
the model size, and the wall time.

Whatever this baseline MISSES is, by definition, beyond the finite frontier we
ran -- that is the target set to hand the LLM proposer, and every LLM solve of
such a pair is past the frontier by construction. Re-running with raised bounds
(especially --af-max-n / --af-decide-cost) is ALSO the honest re-test of whether
a stronger affine search finds order5v2_1593 (n=17) on its own, without the LLM.

Stages (all pure-Python search; each candidate is self-verified here in Python):
  affine  af_find              general  a*x + b*y + c (mod n),  n <= --af-max-n
  mf2     mf2_find_portfolio   domain-propagation finder (quasigroup/Latin/general)
  sat     sat_find_model       complete CDCL search over --sat-sizes
  al      al_find_linear_model infinite algebraic-linear ZZ[alpha] model, deg <= --al-deg-max

We do NOT run Lean/judge verification here: finite tables are known to verify
under the judge (with maxRecDepth), and the al_ cert self-verifies in exact ZZ.
This script maps the frontier; certification is a separate, known-good step.
Vampire is treated as an external baseline component (run via your own setup);
pass --note-vampire to record a column for it in the report.

Usage:
  python paper/scripts/baseline.py --pairs paper/problems/pairs8.json \
      --solver-dir scripts/my_solver_merged --out paper/results/baseline_pairs8.jsonl
"""
from __future__ import annotations
import argparse
import json
import sys
import time


def load_solver(solver_dir):
    sys.path.insert(0, solver_dir)
    import solver
    # Deterministic-only: make sure no LLM stage can fire, and silence tracing.
    solver.ENABLE_LLM = False
    solver.trace = lambda *a, **k: None
    return solver


def self_verify_table(solver, eq1, eq2, n, table):
    """True iff (n, table) satisfies EQ1 for all and fails EQ2 for some."""
    v1, l1, r1 = solver.parse_equation(eq1)
    v2, l2, r2 = solver.parse_equation(eq2)
    op = lambda a, b, t=table: t[a][b]
    return (solver.equation_holds(v1, l1, r1, n, op)
            and not solver.equation_holds(v2, l2, r2, n, op))


def stage_affine(solver, eq1, eq2, args):
    out = solver.af_find(eq1, eq2, max_decide_cost=args.af_decide_cost,
                         max_n=args.af_max_n)
    if not out:
        return None
    n, table = out
    if self_verify_table(solver, eq1, eq2, n, table):
        return {"size": f"Fin{n}", "detail": f"affine mod {n}"}
    return None


def stage_mf2(solver, eq1, eq2, args):
    out = solver.mf2_find_portfolio(eq1, eq2, args.mf2_budget)
    if not out:
        return None
    n, table = out
    if self_verify_table(solver, eq1, eq2, n, table):
        return {"size": f"Fin{n}", "detail": "domain-propagation finder"}
    return None


def stage_sat(solver, eq1, eq2, args):
    sizes = [int(s) for s in args.sat_sizes.split(",") if s.strip()]
    per = args.sat_budget / max(1, len(sizes))
    for n in sizes:
        try:
            tbl = solver.sat_find_model(eq1, eq2, n, time.time() + per)
        except Exception:
            tbl = None
        if tbl is not None and self_verify_table(solver, eq1, eq2, n, tbl):
            return {"size": f"Fin{n}", "detail": "CDCL SAT model"}
    return None


def stage_al(solver, eq1, eq2, args):
    # Returns a self-verified Lean cert string (exact-ZZ basis check) or None.
    cert = solver.al_find_linear_model(eq1, eq2, deg_min=2, deg_max=args.al_deg_max)
    if cert:
        return {"size": "infinite", "detail": "algebraic-linear ZZ[alpha]"}
    return None


STAGES = [
    ("affine", stage_affine),
    ("mf2", stage_mf2),
    ("sat", stage_sat),
    ("al", stage_al),
]


def run_pair(solver, pid, eq1, eq2, args):
    result = {"id": pid, "eq1": eq1, "eq2": eq2, "solved_by": None, "stages": {}}
    for name, fn in STAGES:
        if name in args.skip:
            result["stages"][name] = {"status": "skipped"}
            continue
        t0 = time.time()
        try:
            hit = fn(solver, eq1, eq2, args)
        except Exception as e:
            result["stages"][name] = {"status": "error", "error": repr(e),
                                      "secs": round(time.time() - t0, 2)}
            continue
        secs = round(time.time() - t0, 2)
        if hit:
            result["stages"][name] = {"status": "FOUND", "secs": secs, **hit}
            if result["solved_by"] is None:
                result["solved_by"] = name
        else:
            result["stages"][name] = {"status": "miss", "secs": secs}
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--out", required=True)
    # Strengthened bounds (raise these to push the frontier out).
    ap.add_argument("--af-max-n", type=int, default=25,
                    help="affine: max modulus to search")
    ap.add_argument("--af-decide-cost", type=int, default=5_000_000,
                    help="affine: max n^(#vars) (symbolic cert decouples this from verify cost)")
    ap.add_argument("--mf2-budget", type=float, default=120.0,
                    help="mf2 finder time budget (s)")
    ap.add_argument("--sat-sizes", default="5,6,7,8",
                    help="comma-separated Fin sizes for the SAT finder")
    ap.add_argument("--sat-budget", type=float, default=120.0,
                    help="total SAT finder budget (s)")
    ap.add_argument("--al-deg-max", type=int, default=8,
                    help="algebraic-linear: max polynomial degree")
    ap.add_argument("--skip", default="",
                    help="comma-separated stage names to skip (affine,mf2,sat,al)")
    args = ap.parse_args()
    args.skip = {s.strip() for s in args.skip.split(",") if s.strip()}

    solver = load_solver(args.solver_dir)
    pairs = json.load(open(args.pairs))

    rows = []
    n_solved = 0
    print(f"{'pair':<18} {'solved_by':<10} {'stages that FOUND'}")
    print("-" * 64)
    for pid, (eq1, eq2) in pairs.items():
        r = run_pair(solver, pid, eq1, eq2, args)
        rows.append(r)
        found = [f"{k}({v.get('size','')})" for k, v in r["stages"].items()
                 if v.get("status") == "FOUND"]
        if r["solved_by"]:
            n_solved += 1
        print(f"{pid:<18} {str(r['solved_by']):<10} {', '.join(found) or '-- (beyond frontier)'}")

    with open(args.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("-" * 64)
    print(f"finite baseline solved {n_solved}/{len(rows)}; "
          f"{len(rows) - n_solved} beyond the frontier -> LLM target set")
    print(f"wrote {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
