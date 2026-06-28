#!/usr/bin/env python3
"""Encode ETP implication problems into TPTP for the classical ATP baselines.

For each row {eq1, eq2} over a single binary op (magma), emit two files:
  {id}_true.p   -- prove   eq1 |= eq2   (Vampire / E / Prover9)
  {id}_false.p  -- refute  eq1 |= eq2   (Mace4 / Vampire --mode fmb)

No dependency on the competition solver. See etp_terms.py for the encoders.

Usage:
  python build_tptp.py paper/problems/hard3.jsonl --out paper/tptp
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from etp_terms import tptp_true, tptp_false  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", default="paper/tptp")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    index, n = [], 0
    with open(args.jsonl, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            pid, eq1, eq2 = row["id"], row["equation1"], row["equation2"]
            try:
                tp_true, tp_false = tptp_true(eq1, eq2), tptp_false(eq1, eq2)
            except ValueError as e:
                print(f"  SKIP {pid}: {e}", file=sys.stderr)
                continue
            hdr = f"% {pid}  eq1={row['eq1_id']} eq2={row['eq2_id']}  gold={row['answer']}\n"
            with open(os.path.join(args.out, f"{pid}_true.p"), "w") as f:
                f.write(hdr + "% TRUE-direction: prove eq1 |= eq2\n" + tp_true)
            with open(os.path.join(args.out, f"{pid}_false.p"), "w") as f:
                f.write(hdr + "% FALSE-direction: find counterexample magma\n" + tp_false)
            index.append({"id": pid, "eq1_id": row["eq1_id"],
                          "eq2_id": row["eq2_id"], "gold": row["answer"]})
            n += 1
    with open(os.path.join(args.out, "index.jsonl"), "w") as f:
        for r in index:
            f.write(json.dumps(r) + "\n")
    print(f"wrote {n} problems x2 files -> {args.out}")


if __name__ == "__main__":
    main()
