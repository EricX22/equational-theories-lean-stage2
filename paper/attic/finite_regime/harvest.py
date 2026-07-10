#!/usr/bin/env python3
"""Resumable background benchmark harvester / characterizer for order-5 pairs.

Reads a cheap-screened pool (JSONL with id, equation1, equation2) and, for each
pair not already characterized, runs a deterministic battery and STREAMS a
packaged benchmark row. Designed to run unattended (nohup) and in parallel
(--shard). Resumable: on restart it skips ids already present in --out.

Battery (cheap first, expensive last, everything short-circuits):
  1. linear analysis (ms): does a LINEAR op a*x+b*y+c refute the pair? Also
     derive EQ1's coefficient constraints. A refuting linear model -> tier LINEAR.
  2. vampire fmb: finite countermodel at --fmb-timeout?          -> tier SOLVED_FMB.
  3. vampire prove: EQ1 -> EQ2 a theorem at --prove-timeout?     -> tier THEOREM.
  4. otherwise                                                    -> tier HARD_NONLINEAR
     (open; no linear refutation up to --maxn; resisted Vampire both ways).

Tiers:
  LINEAR          deterministically solved by a linear model (the easy solved tier)
  SOLVED_FMB      deterministically solved by Vampire's finite-model builder
  THEOREM         EQ1 -> EQ2 provable; NOT a countermodel target (drop)
  HARD_NONLINEAR  genuinely open, provably outside the linear family: the target tier
  (a pair with no linear refutation but that Vampire also can't touch and that
   still has some linear EQ1-model is tagged HARD_NONLINEAR too; see fields.)

Usage:
  python paper/scripts/harvest.py --pool paper/problems/order5_big_survivors.jsonl \
      --solver-dir scripts/my_solver_merged --out paper/results/benchmark_characterized.jsonl \
      --prove-timeout 60 --fmb-timeout 60 --vampire paper/bin/vampire
  # parallel workers: add --shard 0/8 ... --shard 7/8 with distinct --out files
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time


def load_solver(d):
    sys.path.insert(0, d)
    import solver
    solver.trace = lambda *a, **k: None
    return solver


def render_cons(cons):
    out = []
    for poly in cons:
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
        out.append((" + ".join(terms).replace("+ -", "- ") or "0") + " = 0")
    return out


def linear_analysis(solver, eq1, eq2, maxn):
    """Return (constraints_text, eq1_has_linear_model, refuting_example|None)."""
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
    return render_cons(cons), eq1_ok, example


def _vampire(body, cmd_builder, timeout):
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "prob.p")
        open(p, "w").write(body)
        try:
            r = subprocess.run(cmd_builder(p), capture_output=True, text=True, timeout=timeout + 5)
            return r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return "TIMEOUT"


def vprove(etp, eq1, eq2, t, vbin):
    s = _vampire(etp.tptp_true(eq1, eq2),
                 lambda f: [vbin, "--mode", "casc", "-t", f"{t}s", f], t)
    return ("SZS status Theorem" in s or "SZS status Unsatisfiable" in s
            or "Refutation found" in s)


def vfmb(etp, eq1, eq2, t, vbin):
    s = _vampire(etp.tptp_false(eq1, eq2),
                 lambda f: [vbin, "-sa", "fmb", "-t", f"{t}s", f], t)
    return ("SZS status Satisfiable" in s or "SZS status CounterSatisfiable" in s
            or "Exiting with 1 model" in s or "interpretation(" in s)


def characterize(solver, etp, r, args):
    eq1, eq2 = r["equation1"], r["equation2"]
    cons, eq1_ok, example = linear_analysis(solver, eq1, eq2, args.maxn)
    thm = fmb = None
    if example is not None:
        tier = "LINEAR"
    else:
        fmb = vfmb(etp, eq1, eq2, args.fmb_timeout, args.vampire) if args.fmb_timeout > 0 else False
        if fmb:
            tier = "SOLVED_FMB"
        else:
            thm = vprove(etp, eq1, eq2, args.prove_timeout, args.vampire) if args.prove_timeout > 0 else False
            tier = "THEOREM" if thm else "HARD_NONLINEAR"
    return dict(id=r["id"], equation1=eq1, equation2=eq2, tier=tier,
                linear_refutable=example is not None, linear_example=example,
                eq1_has_linear_model=eq1_ok, eq1_constraints=cons,
                linear_checked_maxn=args.maxn, vampire_fmb=fmb, vampire_theorem=thm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True)
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prove-timeout", type=int, default=60, help="0 skips the prove pass")
    ap.add_argument("--fmb-timeout", type=int, default=60, help="0 skips the fmb pass")
    ap.add_argument("--maxn", type=int, default=13, help="max modulus for the linear search")
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--shard", default="0/1", help="i/n: process pairs whose index %% n == i")
    ap.add_argument("--limit", type=int, default=0, help="stop after this many new rows (0 = all)")
    args = ap.parse_args()

    i_shard, n_shard = (int(x) for x in args.shard.split("/"))
    solver = load_solver(args.solver_dir)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms

    done = set()
    if os.path.exists(args.out):
        for line in open(args.out):
            try:
                done.add(json.loads(line)["id"])
            except Exception:
                pass

    rows = [json.loads(l) for l in open(args.pool) if l.strip()]
    counts = {}
    processed = 0
    with open(args.out, "a") as f:
        for idx, r in enumerate(rows):
            if idx % n_shard != i_shard:
                continue
            if r["id"] in done:
                continue
            t0 = time.time()
            row = characterize(solver, etp_terms, r, args)
            f.write(json.dumps(row) + "\n")
            f.flush()
            counts[row["tier"]] = counts.get(row["tier"], 0) + 1
            processed += 1
            print(f"[{processed}] {row['id']}: {row['tier']} ({round(time.time()-t0,1)}s)  "
                  f"running={counts}", file=sys.stderr)
            if args.limit and processed >= args.limit:
                break
    print(f"done: {processed} new rows -> {args.out}; tiers={counts}")


if __name__ == "__main__":
    main()
