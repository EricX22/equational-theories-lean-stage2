#!/usr/bin/env python3
"""Sample candidate implication pairs from the order-5 ETP equation set.

`reference/equational_theories/data/eq_size5.txt` extends the published
order-<=4 `equations.txt` (4694 laws) with all equations up to term-size 5
(62576 laws total; verified byte-identical prefix). Lines 4695+ are laws that
do not appear anywhere in the published, Lean-formalized ETP order-<=4 graph
-- i.e. genuinely open pairs (per PAPER_PLAN.md, step 1: "order-5 yield
probe").

A sampled pair (eq1_id, eq2_id) is kept only if at least one id is >4694, so
every row involves at least one law outside the resolved graph. Output rows
match the existing hard1/2/3.jsonl schema so build_tptp.py / run_baselines.py
work unmodified. `answer` is null: these implications are, by construction,
unresolved.

Usage:
  python sample_order5.py --n 250 --seed 20260701 \
      --out paper/problems/order5_probe.jsonl
"""
from __future__ import annotations
import argparse
import json
import os
import random

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "reference", "equational_theories", "data")
ORDER4_N = 4694  # len(equations.txt); verified prefix of eq_size5.txt


def load_eqs(path):
    with open(path, encoding="utf-8") as fh:
        return [l.rstrip("\n") for l in fh if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=250, help="number of pairs to sample")
    ap.add_argument("--seed", type=int, default=20260701)
    ap.add_argument("--eq-file", default=os.path.join(DATA, "eq_size5.txt"))
    ap.add_argument("--out", default="paper/problems/order5_probe.jsonl")
    ap.add_argument("--id-prefix", default="order5")
    args = ap.parse_args()

    eqs = load_eqs(args.eq_file)
    total = len(eqs)
    assert total > ORDER4_N, f"expected >{ORDER4_N} lines, got {total}"

    rng = random.Random(args.seed)
    seen = set()
    rows = []
    attempts = 0
    while len(rows) < args.n and attempts < args.n * 200:
        attempts += 1
        i = rng.randint(1, total)      # 1-indexed law id
        j = rng.randint(1, total)
        if i == j:
            continue
        if i <= ORDER4_N and j <= ORDER4_N:
            continue                    # both order-<=4: already-resolved pair
        key = (min(i, j), max(i, j))
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "id": f"{args.id_prefix}_{len(rows) + 1:04d}",
            "eq1_id": i,
            "eq2_id": j,
            "equation1": eqs[i - 1],
            "equation2": eqs[j - 1],
            "answer": None,
            "order5": True,
            "eq1_order5": i > ORDER4_N,
            "eq2_order5": j > ORDER4_N,
        })

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"sampled {len(rows)} pairs (attempts={attempts}, total_laws={total}, "
          f"order4_boundary={ORDER4_N}) -> {args.out}")


if __name__ == "__main__":
    main()
