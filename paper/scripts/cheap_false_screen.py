#!/usr/bin/env python3
"""Cheap pure-Python FALSE-side pre-filter, reusing the production solver's
own fast stages (no Lean judge, no subprocess) to stratify order-5 candidate
pairs the way the (competition-provided) hard1/2/3 sets are believed to have
been curated: throw away what a fixed portfolio already resolves, keep only
the resistant tail for the expensive ATP pass.

Reuses `scripts/my_solver_merged/solver.py`'s stages 1/1.3/1.5 verbatim:
  - search_counterexample(max_n=3)               -- exhaustive Fin<=3
  - search_counterexample_extended(sizes 4-7)    -- structured Fin4-7
  - af_find(max_n=40)                            -- symbolic affine mod n<=40
These are the pure-search halves of the real stages (the judge-submission
wrapper is skipped entirely -- we only want existence, not a verified cert).

Usage:
  python cheap_false_screen.py order5_pool_v2.jsonl --out survivors.jsonl \
      --screened-out screened_out.jsonl [--offset 0] [--limit 400]
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "scripts", "my_solver_merged"))
import solver  # noqa: E402


def screen_one(eq1, eq2):
    """Return the family name that resolved it FALSE, or None if it survives."""
    n, t = solver.search_counterexample(eq1, eq2, max_n=3)
    if n is not None:
        return f"exhaustive Fin<=3 (n={n})"
    n, t = solver.search_counterexample_extended(eq1, eq2, sizes=(4, 5, 6, 7))
    if n is not None:
        return f"structured Fin4-7 (n={n})"
    try:
        out = solver.af_find(eq1, eq2, max_n=40)
    except Exception as e:  # noqa: BLE001
        out = None
    if out:
        n, t = out
        return f"affine mod<=40 (n={n})"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", required=True, help="pairs that survive (candidates)")
    ap.add_argument("--screened-out", default=None, help="pairs resolved by the cheap filter")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0, help="0 = to end")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.jsonl, encoding="utf-8") if l.strip()]
    end = len(rows) if not args.limit else min(len(rows), args.offset + args.limit)
    chunk = rows[args.offset:end]

    survivors, screened = [], []
    t0 = time.time()
    for r in chunk:
        fam = screen_one(r["equation1"], r["equation2"])
        if fam is None:
            survivors.append(r)
        else:
            r2 = dict(r)
            r2["cheap_screen_family"] = fam
            screened.append(r2)
    dt = time.time() - t0

    mode = "a" if args.offset > 0 else "w"
    with open(args.out, mode, encoding="utf-8") as f:
        for r in survivors:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if args.screened_out:
        with open(args.screened_out, mode, encoding="utf-8") as f:
            for r in screened:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[{args.offset}:{end}] {len(chunk)} pairs in {dt:.1f}s "
          f"({dt/max(1,len(chunk))*1000:.1f}ms/pair) -> "
          f"{len(survivors)} survive, {len(screened)} screened out",
          file=sys.stderr)


if __name__ == "__main__":
    main()
