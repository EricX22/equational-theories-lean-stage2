#!/usr/bin/env python3
"""Recompute the deterministic-baseline column, offline.

The baseline (translation-invariant / greedy / open_to_us) is pure Python — no
Vampire — so it can be re-derived at any time without touching the proof statuses.
That matters because `order6_grade.grade` hardcoded the variables x,y,z and threw
KeyError('w') on every 4-variable law; `prove_status.py` caught it and wrote
`baseline="error:'w'"`, silently blanking the column for ~4k laws (including 63
AUSTIN_PROVEN ones that could not then be counted as benchmark gold).

Rather than re-run the provers, rescore here and let `status_report.py --baselines`
override the broken column.

  python paper/scripts/rescore_baselines.py --in 'paper/results/*_status_*.jsonl' \
      --out paper/results/baselines.jsonl [--all] [--shard 0/16]

--all rescores every law; the default only fixes rows whose baseline is missing or
errored, which is much faster and is all that is needed.
"""
import argparse, glob, json, os, sys, time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--shard", default=None)
    a = ap.parse_args()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et
    import order6_grade

    laws, seen = [], set()
    for pat in a.inp:
        for f in sorted(glob.glob(pat)):
            for line in open(f):
                if not line.strip():
                    continue
                r = json.loads(line)
                law = r["law"]
                if law in seen:
                    continue
                bl = str(r.get("baseline", ""))
                if a.all or not bl or bl.startswith("error"):
                    seen.add(law); laws.append(law)

    if a.shard:
        i, m = (int(x) for x in a.shard.split("/"))
        laws = [L for k, L in enumerate(laws) if k % m == i]
    print(f"rescoring {len(laws)} laws", flush=True)

    t0 = time.time()
    with open(a.out, "a") as f:
        for j, law in enumerate(laws, 1):
            try:
                _, bl = order6_grade.grade(et, law)
            except Exception as e:
                bl = f"error:{e}"
            f.write(json.dumps({"law": law, "baseline": bl}, ensure_ascii=False) + "\n")
            f.flush()
            if j % 200 == 0:
                rate = j / max(time.time() - t0, 1e-9)
                print(f"  {j}/{len(laws)}  {rate:.1f} laws/s", flush=True)
    print(f"DONE -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
