#!/usr/bin/env python3
"""Select laws out of prove_status.py output, by proved status.

Two uses in the overnight loop:

  seeds    — laws worth EXTENDING to generate the next order. The right seeds are
             the ones with a *proved* absence of finite models (AUSTIN_PROVEN or
             NO_FINITE_MODEL): the no-finite-model mechanism is largely inherited
             by one-op extensions, so extending them lands in the Austin band far
             more often than random sampling does.

  unsettled — laws still lacking a theorem either way (NO_FINITE_MODEL,
             SATISFIABLE_ONLY, OPEN). These get a second pass at a long timeout.

  python paper/scripts/seeds_from_status.py --in 'paper/results/*_status_*.jsonl' \
      --status AUSTIN_PROVEN NO_FINITE_MODEL --out paper/results/seeds_r2.jsonl
"""
import argparse, glob, json

UNSETTLED = ["NO_FINITE_MODEL", "SATISFIABLE_ONLY", "OPEN"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--status", nargs="+", default=["AUSTIN_PROVEN", "NO_FINITE_MODEL"])
    ap.add_argument("--unsettled", action="store_true", help="shorthand for the open statuses")
    ap.add_argument("--max", type=int, default=0, help="cap the number emitted (0 = all)")
    a = ap.parse_args()

    want = set(UNSETTLED if a.unsettled else a.status)
    seen, out = set(), []
    for pat in a.inp:
        for path in sorted(glob.glob(pat)):
            for line in open(path):
                if not line.strip():
                    continue
                r = json.loads(line)
                if r.get("status") in want and r["law"] not in seen:
                    seen.add(r["law"]); out.append(r["law"])
    if a.max:
        out = out[:a.max]
    with open(a.out, "w") as f:
        for law in out:
            f.write(json.dumps({"law": law}, ensure_ascii=False) + "\n")
    print(f"{len(out)} laws with status in {sorted(want)} -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
