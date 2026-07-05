#!/usr/bin/env python3
"""Extract proposer-ready target sets from harvest output, filtered by tier.

Two main uses:
  * CAPABILITY test (isolate LLM ability from existence): known non-linear
    solvable pairs -- a finite model provably exists but linear search missed it.
        --tier SOLVED_FMB --require-nonlinear
    If the LLM's structured mode rediscovers these, its construction ability is
    real; if it can't even match unstructured search, that's a clean ceiling.
  * ASPIRATIONAL open targets (breadth net for a novel success):
        --tier HARD_NONLINEAR

Emits a JSON dict {id: [eq1, eq2]} -- the same shape proposer_o3.py --pairs
accepts. Use --limit / --shuffle for a breadth sample across many candidates
(the LLM side rewards one novel success, so wide-and-shallow beats deep).

Reads one or more harvest JSONL files (pass shards with multiple --harvest).
"""
from __future__ import annotations
import argparse
import json
import random


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--harvest", nargs="+", required=True,
                    help="one or more harvest output JSONL files (shards ok)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tier", default=None,
                    help="keep only this tier (e.g. SOLVED_FMB, HARD_NONLINEAR)")
    ap.add_argument("--require-nonlinear", action="store_true",
                    help="keep only pairs with NO linear refutation (linear_refutable == false)")
    ap.add_argument("--limit", type=int, default=0, help="cap the number of pairs (0 = all)")
    ap.add_argument("--shuffle", action="store_true",
                    help="shuffle before applying --limit (breadth sample)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    rows = []
    seen = set()
    for path in args.harvest:
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r["id"] in seen:
                continue
            if args.tier and r.get("tier") != args.tier:
                continue
            if args.require_nonlinear and r.get("linear_refutable"):
                continue
            seen.add(r["id"])
            rows.append(r)

    if args.shuffle:
        random.Random(args.seed).shuffle(rows)
    if args.limit:
        rows = rows[:args.limit]

    out = {r["id"]: [r["equation1"], r["equation2"]] for r in rows}
    with open(args.out, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    tiers = {}
    for r in rows:
        tiers[r.get("tier")] = tiers.get(r.get("tier"), 0) + 1
    print(f"wrote {len(out)} pairs -> {args.out}  (tiers: {tiers})")


if __name__ == "__main__":
    main()
