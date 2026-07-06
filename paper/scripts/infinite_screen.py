#!/usr/bin/env python3
"""Infinite-model candidate screen: find pairs whose countermodel must be INFINITE
and that deterministic infinite search cannot construct -- the only clean LLM
targets, because finite solvers (SAT/mf2/fmb) structurally cannot touch them.

The finite capability band taught us the lesson the hard way: 64/74 fell to the
finite finder and the other 10 were finder-budget gaps at Fin8-9, not frontier.
There is no LLM necessity in the finite regime. The infinite regime is different:
SAT and Vampire-fmb only build FINITE domains, so a pair with no finite model but
an infinite one (e.g. a ZZ[alpha] construction) is beyond every finite tool by
construction -- and beyond the deterministic infinite finder too, unless it is a
plain idempotent-linear model.

A genuine target survives a STACK of subtractions (each drop is honest and
cheap-first):

  1. FINITE_MODEL          finite finder (mf2/SAT/affine) finds one   -> drop
  2. THEOREM               Vampire saturation proves EQ1->EQ2          -> drop
                           (no countermodel exists at all)
  3. FINITE_MODEL_LARGE    Vampire fmb finds one climbing to size K    -> drop
  4. INFINITE_DETERMINISTIC  al_ (ZZ[alpha], idempotent slice) finds   -> drop
                             an infinite linear model (solved, no LLM)
  5. INFINITE_CANDIDATE    survives all of the above                   -> LLM TARGET

Only tier 5 goes to the o3 algebraic-linear / structured proposer. An LLM solve
of a tier-5 pair (Lean-verified) cannot be reproduced by any finite tool or by
the deterministic infinite finder -- that is the necessity claim.

CAVEATS (state them in the paper, do not hide them):
  * "not a theorem at budget T" is not a proof of non-theoremhood; a longer prove
    budget can still promote a candidate to THEOREM. Use a generous --prove-timeout.
  * "no finite model up to fmb size K" is evidence, not proof, that the model must
    be infinite. The real certificate is the LLM's Lean-verified infinite model;
    the screen only decides where to spend. A provable "no finite model" upgrade
    (EQ1 forces cancellativity => finite models satisfy EQ2) is a future lever.

Usage:
  # screen the current open tier
  python paper/scripts/infinite_screen.py \
      --harvest paper/results/bench_big_shard_*.jsonl --tier HARD_NONLINEAR \
      --solver-dir scripts/my_solver_merged --vampire paper/bin/vampire \
      --fin-budget 60 --prove-timeout 300 --fmb-timeout 300 --al-deg-max 12 \
      --out-report paper/results/infinite_screen.jsonl \
      --out-targets paper/problems/infinite_targets.json
  # or an explicit {id:[eq1,eq2]} set via --pairs
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baseline      # noqa: E402  finite stages + al_ stage + solver loader
import etp_terms     # noqa: E402  TPTP encoders


# ---- input loading -------------------------------------------------------
def load_targets(args):
    if args.pairs:
        obj = json.load(open(args.pairs))
        return [(pid, e[0], e[1]) for pid, e in obj.items()]
    paths = []
    for g in args.harvest:
        paths.extend(sorted(glob.glob(g)))
    seen, out = set(), []
    for p in paths:
        for line in open(p):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if args.tier and r.get("tier") != args.tier:
                continue
            pid = r["id"]
            if pid in seen:
                continue
            seen.add(pid)
            out.append((pid, r.get("equation1") or r.get("eq1"),
                        r.get("equation2") or r.get("eq2")))
    return out


# ---- Vampire helpers (same invocation as true_side_sweep) ----------------
def _vampire(body, cmd, timeout):
    with tempfile.TemporaryDirectory() as wd:
        path = os.path.join(wd, "prob.p")
        open(path, "w").write(body)
        try:
            p = subprocess.run(cmd(path), capture_output=True, text=True,
                               timeout=timeout + 5)
            return p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            return "TIMEOUT"


def vampire_theorem(eq1, eq2, timeout, vbin):
    s = _vampire(etp_terms.tptp_true(eq1, eq2),
                 lambda f: [vbin, "--mode", "casc", "-t", f"{timeout}s", f], timeout)
    return ("SZS status Theorem" in s or "SZS status Unsatisfiable" in s
            or "Refutation found" in s)


def vampire_fmb(eq1, eq2, timeout, vbin):
    s = _vampire(etp_terms.tptp_false(eq1, eq2),
                 lambda f: [vbin, "-sa", "fmb", "-t", f"{timeout}s", f], timeout)
    return ("SZS status Satisfiable" in s or "SZS status CounterSatisfiable" in s
            or "Exiting with 1 model" in s or "Finite Model Found" in s)


# ---- the escalating screen ----------------------------------------------
def screen_pair(solver, fin_args, pid, eq1, eq2, args):
    t0 = time.time()
    rec = {"id": pid, "eq1": eq1, "eq2": eq2}

    # 1) cheap finite finder (its FAILURE is the infinite signal)
    for name, fn in baseline.STAGES:
        if name == "al":          # al_ is the deterministic INFINITE finder; handle at step 4
            continue
        try:
            if fn(solver, eq1, eq2, fin_args):
                rec.update(tier="FINITE_MODEL", by=name, secs=round(time.time()-t0, 1))
                return rec
        except Exception:
            pass

    # 2) theorem? (no countermodel exists at all)
    if args.prove_timeout > 0 and vampire_theorem(eq1, eq2, args.prove_timeout, args.vampire):
        rec.update(tier="THEOREM", secs=round(time.time()-t0, 1))
        return rec

    # 3) finite model at larger size via Vampire fmb
    if args.fmb_timeout > 0 and vampire_fmb(eq1, eq2, args.fmb_timeout, args.vampire):
        rec.update(tier="FINITE_MODEL_LARGE", secs=round(time.time()-t0, 1))
        return rec

    # 4) deterministic infinite (idempotent-linear ZZ[alpha]) -- solved, but NOT the LLM
    try:
        if baseline.stage_al(solver, eq1, eq2, fin_args):
            rec.update(tier="INFINITE_DETERMINISTIC", secs=round(time.time()-t0, 1))
            return rec
    except Exception:
        pass

    # 5) survives everything -> the clean LLM target
    rec.update(tier="INFINITE_CANDIDATE", secs=round(time.time()-t0, 1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--harvest", nargs="+", help="harvest shard(s); globs ok")
    src.add_argument("--pairs", help="explicit {id:[eq1,eq2]} json")
    ap.add_argument("--tier", default="HARD_NONLINEAR",
                    help="harvest tier to pull when using --harvest")
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--out-report", required=True)
    ap.add_argument("--out-targets", required=True,
                    help="{id:[eq1,eq2]} of INFINITE_CANDIDATE pairs (the LLM set)")
    # budgets
    ap.add_argument("--fin-budget", type=float, default=60.0,
                    help="per-stage budget for the finite finder subtraction")
    ap.add_argument("--af-max-n", type=int, default=25)
    ap.add_argument("--sat-sizes", default="5,6,7,8")
    ap.add_argument("--al-deg-max", type=int, default=12)
    ap.add_argument("--prove-timeout", type=int, default=300)
    ap.add_argument("--fmb-timeout", type=int, default=300)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    fin_args = SimpleNamespace(
        af_max_n=args.af_max_n, af_decide_cost=5_000_000,
        mf2_budget=args.fin_budget, sat_sizes=args.sat_sizes,
        sat_budget=args.fin_budget, al_deg_max=args.al_deg_max, skip=set())

    solver = baseline.load_solver(args.solver_dir)
    targets = load_targets(args)
    if args.limit:
        targets = targets[:args.limit]

    rows, tally, llm_targets = [], {}, {}
    print(f"screening {len(targets)} pairs for infinite-model candidates")
    print(f"{'pair':<20} {'tier':<24} secs")
    print("-" * 56)
    for pid, eq1, eq2 in targets:
        rec = screen_pair(solver, fin_args, pid, eq1, eq2, args)
        rows.append(rec)
        tally[rec["tier"]] = tally.get(rec["tier"], 0) + 1
        if rec["tier"] == "INFINITE_CANDIDATE":
            llm_targets[pid] = [eq1, eq2]
        print(f"{pid:<20} {rec['tier']:<24} {rec.get('secs')}")
        with open(args.out_report, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(args.out_targets, "w") as f:
            json.dump(llm_targets, f, indent=2, ensure_ascii=False)
    print("-" * 56)
    for k in ("FINITE_MODEL", "THEOREM", "FINITE_MODEL_LARGE",
              "INFINITE_DETERMINISTIC", "INFINITE_CANDIDATE"):
        print(f"  {k:<24} {tally.get(k, 0)}")
    print(f"\nINFINITE_CANDIDATE (LLM target set) = {len(llm_targets)} -> {args.out_targets}")
    print(f"report -> {args.out_report}")


if __name__ == "__main__":
    main()
