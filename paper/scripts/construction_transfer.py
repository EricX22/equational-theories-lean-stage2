#!/usr/bin/env python3
"""construction_transfer.py — does each Austin law need its OWN construction, or do the
models transfer? Direct evidence on the "novel construction vs. seed-adaptation" worry.

Every AUSTIN_PROVEN law already has a model: its saturated set (in certs/saturation/).
Define the transfer matrix

    T[i][j] = does law_j hold in law_i's model M_i ?        (True / False / None)

computed with equiv_sample.holds_in — pure-Python ground rewriting, NO prover. Reading it:

  * M_i satisfies MANY laws            -> one construction covers them        -> ADAPTATION
  * each M_i satisfies ~only its own   -> constructions are specific          -> DIVERSITY
  * CROSS-LOGICAL-CLASS transfer is the sharp number: if M_i satisfies a law_j that is
    logically INEQUIVALENT to law_i, then a solver handed M_i already solves j, so the
    >=195 logical classes OVERSTATE the number of distinct constructions (the reviewer's
    #1/#5). If cross-class transfer is ~0, logical distinctness and construction
    distinctness coincide, and the diversity claim stands.

Note the asymmetry: T is directional. `T[i][j] and T[j][i]` (mutual) is the
model-satisfaction predicate equiv_sample uses as its equivalence CANDIDATE filter, so
"construction classes" (mutual union-find) should track the logical classes; the
interesting leakage is the ONE-directional, cross-class entries.

USAGE
  # smoke test on a handful:
  python3 paper/scripts/construction_transfer.py --in paper/results/final_status.jsonl \
      --sat-dir paper/certs/saturation --classes paper/results/classes_full.json \
      --n 15 --out /tmp/transfer_smoke.json
  # full 262:
  python3 paper/scripts/construction_transfer.py --in paper/results/final_status.jsonl \
      --sat-dir paper/certs/saturation --classes paper/results/classes_full.json \
      --n 0 --out paper/results/transfer.json
"""
from __future__ import annotations
import argparse, glob, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ordered_model as om        # noqa: E402
import equiv_sample as es         # noqa: E402  (holds_in: eqs, small, law, cap)


def load_models(inp: str, sat_dir: str, n: int, seed: int):
    seen: dict[str, str] = {}
    for fn in glob.glob(inp):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("status") == "AUSTIN_PROVEN":
                seen.setdefault(r["law"], r.get("cert"))
    items = sorted(seen.items())
    if n and n < len(items):
        import random
        random.Random(seed).shuffle(items)
        items = sorted(items[:n])
    laws, models, missing = [], {}, 0
    for law, cert in items:
        p = os.path.join(sat_dir, f"{cert}.sat") if cert else None
        if p and os.path.exists(p):
            eqs, _ = om.load(p)
            models[len(laws)] = (eqs, om.smallest_const(eqs))
            laws.append(law)
        else:
            missing += 1
    return laws, models, missing


def class_of(laws: list[str], classes_json: str) -> list[int]:
    idx = {lw: i for i, lw in enumerate(laws)}
    parent = list(range(len(laws)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    if classes_json and os.path.exists(classes_json):
        for a, b in json.load(open(classes_json)).get("merged", []):
            if a in idx and b in idx:
                x, y = find(idx[a]), find(idx[b])
                if x != y:
                    parent[x] = y
    return [find(i) for i in range(len(laws))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--sat-dir", default="paper/certs/saturation")
    ap.add_argument("--classes", default="paper/results/classes_full.json")
    ap.add_argument("--n", type=int, default=0, help="sample N Austin laws (0 = all)")
    ap.add_argument("--seed", type=int, default=2)
    ap.add_argument("--cap", type=int, default=3000, help="rewrite step cap per ground check")
    ap.add_argument("--out")
    a = ap.parse_args()

    laws, models, missing = load_models(a.inp, a.sat_dir, a.n, a.seed)
    N = len(laws)
    if N == 0:
        print("no models loaded — check --sat-dir and the cert hashes", file=sys.stderr)
        sys.exit(1)
    cls = class_of(laws, a.classes)
    n_logical = len(set(cls))
    print(f"{N} Austin laws with models ({missing} skipped: no cert file); "
          f"{n_logical} logical classes", file=sys.stderr)

    # T[i][j]: does law_j hold in M_i?  (True / False / None=step-capped)
    T = [[None] * N for _ in range(N)]
    for i in range(N):
        eqs, small = models[i]
        for j in range(N):
            T[i][j] = es.holds_in(eqs, small, laws[j], a.cap)
        if (i + 1) % 20 == 0:
            print(f"  ...{i+1}/{N} models", file=sys.stderr)

    coverage = [sum(1 for j in range(N) if T[i][j] is True) for i in range(N)]  # incl self
    self_fail = [i for i in range(N) if T[i][i] is not True]      # sanity: should be empty
    undecided = sum(1 for i in range(N) for j in range(N) if T[i][j] is None)

    cross_dir = sum(1 for i in range(N) for j in range(N)
                    if i != j and T[i][j] is True and cls[i] != cls[j])
    mutual = sum(1 for i in range(N) for j in range(i + 1, N)
                 if T[i][j] is True and T[j][i] is True)

    # "construction classes": mutual-transfer union-find, compare to logical classes.
    parent = list(range(N))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i in range(N):
        for j in range(i + 1, N):
            if T[i][j] is True and T[j][i] is True:
                x, y = find(i), find(j)
                if x != y:
                    parent[x] = y
    n_constr = len({find(i) for i in range(N)})

    summary = {
        "n_laws": N, "models_missing": missing,
        "logical_classes": n_logical, "construction_classes": n_constr,
        "coverage_min": min(coverage), "coverage_median": statistics.median(coverage),
        "coverage_mean": round(statistics.mean(coverage), 3), "coverage_max": max(coverage),
        "cross_class_directional_transfers": cross_dir,
        "cross_class_transfer_rate": round(cross_dir / (N * (N - 1)), 5) if N > 1 else 0,
        "mutual_transfer_pairs": mutual, "undecided_cells": undecided,
        "self_consistency_failures": self_fail,
        "cap": a.cap,
    }
    print("\n=== construction-transfer summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("\nINTERPRETATION:")
    print(f"  logical classes {n_logical} vs construction classes {n_constr}: "
          f"{'coincide (diversity real)' if n_constr >= 0.95 * n_logical else 'construction fewer (some shared)'}")
    print(f"  cross-class one-directional transfers: {cross_dir} "
          f"({summary['cross_class_transfer_rate']*100:.2f}% of ordered pairs) — "
          f"{'low => models do NOT solve logically-distinct laws' if summary['cross_class_transfer_rate'] < 0.02 else 'non-trivial => some construction sharing across classes'}")
    if self_fail:
        print(f"  WARNING: {len(self_fail)} laws do not hold in their own model — "
              f"check the sat certs for indices {self_fail[:10]}")

    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1)
        print(f"\nwrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
