#!/usr/bin/env python3
"""Summarize the solved-by matrix into the paper's tables.

Produces:
  - coverage by method (overall + by gold side -> the two-frontier view)
  - classical VBS coverage
  - the uniquely-solved-by-LLM set (the headline result), written to JSONL
  - LLM stage distribution over our solves

Usage:
  python analyze.py paper/results/solved_by_matrix_hard3.csv \
      [--unique-out paper/results/uniquely_solved_hard3.jsonl]
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter

METHODS = ["vampire", "eprover", "prover9", "mace4", "classical_vbs",
           "ours_nollm", "ours_llm"]


def solved(row, method):
    if method in ("classical_vbs", "ours_nollm", "ours_llm"):
        return row[method] == "1"
    return row[method] == row["gold"]  # per-tool verdict matches gold


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix")
    ap.add_argument("--unique-out", default=None)
    args = ap.parse_args()

    with open(args.matrix, newline="") as fh:
        rows = list(csv.DictReader(fh))
    n = len(rows)
    sides = {"true": [r for r in rows if r["gold"] == "true"],
             "false": [r for r in rows if r["gold"] == "false"]}

    def cov(subset, method):
        return sum(1 for r in subset if solved(r, method))

    print(f"\n=== Coverage (n={n}: {len(sides['true'])} true / {len(sides['false'])} false) ===")
    print(f"{'method':<16}{'all':>8}{'TRUE side':>12}{'FALSE side':>12}")
    for m in METHODS:
        print(f"{m:<16}{cov(rows,m):>8}{cov(sides['true'],m):>12}{cov(sides['false'],m):>12}")

    # the headline set
    uniq = [r for r in rows if r["uniquely_solved_by_llm"] == "1"]
    print(f"\n=== Uniquely solved by LLM (vs classical VBS + our no-LLM): {len(uniq)} ===")
    for r in uniq[:50]:
        print(f"  {r['id']}  eq1={r['eq1_id']} eq2={r['eq2_id']} gold={r['gold']} "
              f"stage={r['ours_solved_by']}")

    # stage distribution over our LLM-run solves
    stages = Counter(r["ours_solved_by"] for r in rows if r["ours_llm"] == "1" and r["ours_solved_by"])
    if stages:
        print("\n=== solved_by stage distribution (ours, LLM run) ===")
        for stage, c in stages.most_common():
            print(f"  {c:>4}  {stage}")

    # sanity: judge validity over claimed solves
    claimed = [r for r in rows if r["ours_llm"] == "1"]
    bad = [r for r in claimed if r["judge_ok"] != "1"]
    print(f"\n=== Soundness: {len(claimed)} ours-LLM solves, judge_ok on {len(claimed)-len(bad)} "
          f"({'CLEAN' if not bad else str(len(bad))+' UNVERIFIED!'}) ===")

    if args.unique_out and uniq:
        with open(args.unique_out, "w") as fh:
            for r in uniq:
                fh.write(json.dumps(r) + "\n")
        print(f"\nwrote {len(uniq)} uniquely-solved rows -> {args.unique_out}")


if __name__ == "__main__":
    main()
