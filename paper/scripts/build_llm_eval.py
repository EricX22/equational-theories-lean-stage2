#!/usr/bin/env python3
"""build_llm_eval.py — curate the LLM evaluation sets from final_status.jsonl.

DESIGN. LLMs are evaluated on the SOLVABLE tier (laws with a known answer), where a
partial solve rate gives a discriminating gradient; the hard tier would floor everyone at
zero and is offered only as an optional frontier set. To stay contamination-free the eval
draws from the freshest orders and the answers are never published --- grading is done by
Lean, which verifies a submission intrinsically, so the gold label is only for our own
bookkeeping and fairness analysis.

Emits (default to paper/results/eval/):
  eval_solvable.jsonl   balanced Austin + trivial, the ranking set  (law, gold, order)
  eval_frontier.jsonl   a sample of the hard tier, optional bonus   (law, order)

USAGE
  python3 paper/scripts/build_llm_eval.py --in paper/results/final_status.jsonl \
      --orders 7 8 --n-austin 60 --n-trivial 60 --n-frontier 40 --out-dir paper/results/eval
"""
from __future__ import annotations
import argparse, glob, json, os, random


def order(law: str) -> int:
    return law.count("◇")  # count of the magma operation symbol


def load(inp: str):
    by_status = {"AUSTIN_PROVEN": [], "TRIVIAL": [], "NO_FINITE_MODEL": []}
    for fn in glob.glob(inp):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            s = r.get("status")
            if s in by_status:
                by_status[s].append(r)
    return by_status


def pick(rows, orders, n, rng):
    pool = [r for r in rows if order(r["law"]) in orders]
    rng.shuffle(pool)
    return pool[:n] if n and n < len(pool) else pool


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--orders", type=int, nargs="+", default=[7, 8])
    ap.add_argument("--n-austin", type=int, default=60)
    ap.add_argument("--n-trivial", type=int, default=60)
    ap.add_argument("--n-frontier", type=int, default=40)
    ap.add_argument("--seed", type=int, default=20260715)
    ap.add_argument("--out-dir", default="paper/results/eval")
    a = ap.parse_args()

    rng = random.Random(a.seed)
    by = load(a.inp)
    orders = set(a.orders)
    os.makedirs(a.out_dir, exist_ok=True)

    austin = pick(by["AUSTIN_PROVEN"], orders, a.n_austin, rng)
    trivial = pick(by["TRIVIAL"], orders, a.n_trivial, rng)
    frontier = pick(by["NO_FINITE_MODEL"], orders, a.n_frontier, rng)

    solvable = ([{"law": r["law"], "gold": "austin", "order": order(r["law"]),
                  "cert": r.get("cert")} for r in austin]
                + [{"law": r["law"], "gold": "trivial", "order": order(r["law"])}
                   for r in trivial])
    rng.shuffle(solvable)

    sp = os.path.join(a.out_dir, "eval_solvable.jsonl")
    fp = os.path.join(a.out_dir, "eval_frontier.jsonl")
    with open(sp, "w", encoding="utf-8") as fh:
        for r in solvable:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(fp, "w", encoding="utf-8") as fh:
        for r in frontier:
            fh.write(json.dumps({"law": r["law"], "order": order(r["law"])},
                                ensure_ascii=False) + "\n")

    print(f"solvable set: {len(solvable)} laws "
          f"({len(austin)} austin + {len(trivial)} trivial), orders {sorted(orders)}")
    print(f"  -> {sp}")
    print(f"frontier set: {len(frontier)} hard-tier laws  -> {fp}")
    avail = {k: len([r for r in v if order(r['law']) in orders]) for k, v in by.items()}
    print(f"available in orders {sorted(orders)}: "
          f"austin {avail['AUSTIN_PROVEN']}, trivial {avail['TRIVIAL']}, "
          f"hard {avail['NO_FINITE_MODEL']}")


if __name__ == "__main__":
    main()
