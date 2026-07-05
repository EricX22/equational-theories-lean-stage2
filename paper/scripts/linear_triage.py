#!/usr/bin/env python3
"""Deterministic linear-model triage for a set of equational pairs.

For each pair, derive (from EQ1) the exact coefficient constraints a LINEAR
operation x*y = a*x + b*y (+c) must satisfy (via the solver's al_constraints),
then decide whether ANY linear op both satisfies EQ1 and refutes EQ2. Because
the infinite algebraic-linear (ZZ[alpha]) family is the SAME linear family, a
"no" here means no linear counterexample exists at all -- finite OR infinite --
so the pair requires a NON-LINEAR construction (the genuine LLM target).

This is both a paper artifact (a near-proof that the hard survivors sit outside
the entire linear-model family) and the analysis the proposer's linear-gate
injects. Pure Python, no Lean.

Usage:
  python paper/scripts/linear_triage.py --pairs paper/problems/survivors6.json \
      --solver-dir scripts/my_solver_merged [--maxn 19]
"""
from __future__ import annotations
import argparse
import json
import sys


def render_poly(poly):
    terms = []
    for (i, j), c in sorted(poly.items(), key=lambda kv: (-(kv[0][0] + kv[0][1]), -kv[0][0])):
        c = int(c) if c == int(c) else c
        mon = ""
        if i:
            mon += "a" if i == 1 else f"a^{i}"
        if j:
            mon += ("*" if mon else "") + ("b" if j == 1 else f"b^{j}")
        if not mon:
            terms.append(str(c))
            continue
        terms.append(mon if c == 1 else ("-" + mon if c == -1 else f"{c}*{mon}"))
    return (" + ".join(terms).replace("+ -", "- ") or "0") + " = 0"


def triage(solver, eq1, eq2, maxn):
    try:
        L1, R1 = solver.al_parse_equation(eq1)
        cons = solver.al_constraints(L1, R1)
    except Exception:
        cons = []
    v1, l1, r1 = solver.parse_equation(eq1)
    v2, l2, r2 = solver.parse_equation(eq2)
    eq1_ok = False
    example = None
    for n in range(2, maxn + 1):
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    tbl = [[(a * i + b * j + c) % n for j in range(n)] for i in range(n)]
                    op = lambda x, y, t=tbl: t[x][y]
                    if solver.equation_holds(v1, l1, r1, n, op):
                        eq1_ok = True
                        if not solver.equation_holds(v2, l2, r2, n, op):
                            example = (n, a, b, c)
                            break
                if example:
                    break
            if example:
                break
        if example:
            break
    if example:
        verdict = "LINEAR COUNTEREXAMPLE EXISTS"
    elif eq1_ok:
        verdict = "NON-LINEAR REQUIRED (linear EQ1-models all too strong)"
    else:
        verdict = "NON-LINEAR REQUIRED (no linear op satisfies EQ1)"
    return verdict, cons, example


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--maxn", type=int, default=19)
    args = ap.parse_args()

    sys.path.insert(0, args.solver_dir)
    import solver
    solver.trace = lambda *a, **k: None

    pairs = json.load(open(args.pairs))
    n_nonlinear = 0
    for pid, (eq1, eq2) in pairs.items():
        verdict, cons, example = triage(solver, eq1, eq2, args.maxn)
        if "NON-LINEAR" in verdict:
            n_nonlinear += 1
        print(f"{pid}: {verdict}")
        if cons:
            print("    EQ1 linear constraints: " + "; ".join(render_poly(c) for c in cons))
        if example:
            n, a, b, c = example
            print(f"    linear counterexample: op(x,y)=({a}x+{b}y+{c}) mod {n}")
    print("-" * 60)
    print(f"{n_nonlinear}/{len(pairs)} pairs require a NON-LINEAR construction "
          f"(no linear counterexample, finite or infinite)")


if __name__ == "__main__":
    main()
