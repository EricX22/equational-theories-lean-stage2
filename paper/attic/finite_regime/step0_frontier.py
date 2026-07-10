#!/usr/bin/env python3
"""Step 0: define the capability-set A/B frontier (deterministic, no LLM/API).

The capability band is every pair the harvest tiered SOLVED_FMB and NOT
linear_refutable: a NON-linear finite countermodel provably exists (Vampire fmb
found one) and no linear op refutes the pair. But some of those the unconstrained
finder already cracks on its own -- those are useless as an LLM/finisher test,
because there is no headroom to show the LLM added anything.

This script partitions the band at a FIXED budget B:

  * solved by the unconstrained finder at B   -> NOT an A/B target (drop)
  * missed by the unconstrained finder at B   -> the A/B TARGET SET

The miss-set is simultaneously (a) the proposer target file and (b) the honest
denominator for the capability solve-rate. Critically, the control arm here uses
baseline.py's EXACT stage code and the SAME budget B, so a later "constrained
search solved it, unconstrained at B did not" claim is a clean comparison rather
than an apples-to-oranges one. Record B; it IS the experiment.

Usage:
  python paper/scripts/step0_frontier.py \
      --harvest paper/results/bench_shard_*.jsonl \
      --solver-dir scripts/my_solver_merged \
      --mf2-budget 240 --sat-sizes 5,6,7,8 --sat-budget 300 \
      --af-max-n 25 --al-deg-max 12 \
      --out-targets paper/problems/cap_frontier_misses.json \
      --out-report  paper/results/cap_frontier.jsonl
"""
from __future__ import annotations
import argparse
import glob
import json
import sys
import time
from types import SimpleNamespace

# Reuse the unconstrained finder verbatim so the A/B control == the baseline.
import baseline  # noqa: E402  (same scripts/ dir; run from repo root or add to path)


def load_capability_band(harvest_globs, limit, shuffle):
    """Rows tiered SOLVED_FMB and not linear_refutable = the capability band."""
    paths = []
    for g in harvest_globs:
        paths.extend(sorted(glob.glob(g)))
    seen, band = set(), []
    for p in paths:
        with open(p) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                if r.get("tier") != "SOLVED_FMB" or r.get("linear_refutable"):
                    continue
                pid = r["id"]
                if pid in seen:
                    continue
                seen.add(pid)
                band.append(r)
    if shuffle:
        import random
        random.Random(shuffle).shuffle(band)
    if limit:
        band = band[:limit]
    return band


def eq_pair(row):
    # harvest rows use equation1/equation2; be tolerant of eq1/eq2 too.
    e1 = row.get("equation1") or row.get("eq1")
    e2 = row.get("equation2") or row.get("eq2")
    return e1, e2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--harvest", nargs="+", required=True,
                    help="harvest jsonl shard(s); globs allowed")
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--out-targets", required=True,
                    help="proposer-ready {id:[eq1,eq2]} of the UNCONSTRAINED MISSES")
    ap.add_argument("--out-report", required=True,
                    help="jsonl: per-pair solved_by/stages at budget B")
    # --- budget B (identical bounds must be reused for the A/B control arm) ---
    ap.add_argument("--af-max-n", type=int, default=25)
    ap.add_argument("--af-decide-cost", type=int, default=5_000_000)
    ap.add_argument("--mf2-budget", type=float, default=240.0)
    ap.add_argument("--sat-sizes", default="5,6,7,8")
    ap.add_argument("--sat-budget", type=float, default=300.0)
    ap.add_argument("--al-deg-max", type=int, default=12)
    ap.add_argument("--skip", default="")
    ap.add_argument("--limit", type=int, default=0,
                    help="cap the band size (0 = all)")
    ap.add_argument("--shuffle", type=int, default=0,
                    help="RNG seed to shuffle before --limit (0 = no shuffle)")
    args = ap.parse_args()

    # Budget B, frozen into a namespace baseline.run_pair understands verbatim.
    B = SimpleNamespace(
        af_max_n=args.af_max_n,
        af_decide_cost=args.af_decide_cost,
        mf2_budget=args.mf2_budget,
        sat_sizes=args.sat_sizes,
        sat_budget=args.sat_budget,
        al_deg_max=args.al_deg_max,
        skip={s.strip() for s in args.skip.split(",") if s.strip()},
    )
    budget_desc = {
        "af_max_n": B.af_max_n, "af_decide_cost": B.af_decide_cost,
        "mf2_budget": B.mf2_budget, "sat_sizes": B.sat_sizes,
        "sat_budget": B.sat_budget, "al_deg_max": B.al_deg_max,
        "skipped_stages": sorted(B.skip),
    }

    solver = baseline.load_solver(args.solver_dir)
    band = load_capability_band(args.harvest, args.limit, args.shuffle)
    if not band:
        sys.exit("no SOLVED_FMB & non-linear rows found in harvest input")

    rows, misses = [], {}
    n_solved = 0
    print(f"capability band: {len(band)} pairs (SOLVED_FMB & not linear_refutable)")
    print(f"budget B: {json.dumps(budget_desc)}")
    print(f"{'pair':<20} {'unconstrained':<14} {'found by'}")
    print("-" * 60)
    t_start = time.time()
    for row in band:
        pid = row["id"]
        e1, e2 = eq_pair(row)
        r = baseline.run_pair(solver, pid, e1, e2, B)
        r["budget"] = budget_desc
        rows.append(r)
        found = [f"{k}({v.get('size','')})" for k, v in r["stages"].items()
                 if v.get("status") == "FOUND"]
        if r["solved_by"]:
            n_solved += 1
            verdict = "in reach"
        else:
            verdict = "MISS -> A/B"
            misses[pid] = [e1, e2]
        print(f"{pid:<20} {verdict:<14} {', '.join(found) or '--'}")

    with open(args.out_report, "w") as f:
        # first line is a header row capturing budget B and the denominator
        f.write(json.dumps({
            "_meta": True, "budget": budget_desc,
            "band_total": len(band), "unconstrained_solved": n_solved,
            "ab_target_count": len(misses),
            "elapsed_s": round(time.time() - t_start, 1),
        }) + "\n")
        for r in rows:
            f.write(json.dumps(r) + "\n")
    with open(args.out_targets, "w") as f:
        json.dump(misses, f, indent=2, ensure_ascii=False)

    print("-" * 60)
    print(f"unconstrained finder at B solved {n_solved}/{len(band)} of the band")
    print(f"A/B target set (unconstrained MISSES) = {len(misses)} pairs")
    print(f"  -> proposer targets:  {args.out_targets}")
    print(f"  -> per-pair report:   {args.out_report}")
    print("These misses are the denominator for the capability solve-rate AND the "
          "only pairs where an LLM/finisher solve proves it beat unconstrained "
          "search at this exact budget.")


if __name__ == "__main__":
    main()
