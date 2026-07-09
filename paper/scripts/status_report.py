#!/usr/bin/env python3
"""Summarize prove_status.py output: what is a theorem, what is still open.

  python paper/scripts/status_report.py 'paper/results/*_status_*.jsonl' \
      [--merge-out final_status.jsonl] [--gold-out gold.jsonl]

A law can appear in several status files (a fast pass, then a long retry). We keep
the STRONGEST verdict per law: a theorem beats a partial result beats nothing, and
a proved status never gets overwritten by a later timeout.

Two axes, deliberately separated:
  status   — a fact about the law   (theorem, or an open question)
  baseline — a fact about US        (which of our published constructions works)
The rung ladder conflated these. The benchmark's best instances are the
intersection: AUSTIN_PROVEN with baseline=open_to_us — a model provably exists, is
provably infinite, and nothing in our suite writes it down.
"""
import argparse, collections, glob, json

ORDER = ["TRIVIAL", "HAS_FINITE_MODEL", "AUSTIN_PROVEN",
         "NO_FINITE_MODEL", "SATISFIABLE_ONLY", "OPEN"]
SETTLED = {"TRIVIAL", "HAS_FINITE_MODEL", "AUSTIN_PROVEN"}
RANK = {"AUSTIN_PROVEN": 5, "TRIVIAL": 5, "HAS_FINITE_MODEL": 5,
        "NO_FINITE_MODEL": 3, "SATISFIABLE_ONLY": 3, "OPEN": 1}
GLOSS = {
    "TRIVIAL":          "L |= x=y            implication TRUE (proved)",
    "HAS_FINITE_MODEL": "finite countermodel  FALSE, finite (proved)",
    "AUSTIN_PROVEN":    "no finite + exists   FALSE, infinite (proved)",
    "NO_FINITE_MODEL":  "no finite model      existence open",
    "SATISFIABLE_ONLY": "model exists         finiteness open",
    "OPEN":             "nothing proved",
}


def merge(patterns):
    best = {}
    for pat in patterns:
        for f in sorted(glob.glob(pat)):
            for line in open(f):
                if not line.strip():
                    continue
                r = json.loads(line)
                law, cur = r["law"], best.get(r["law"])
                if cur is None or RANK[r["status"]] > RANK[cur["status"]]:
                    best[law] = r
                elif RANK[r["status"]] == RANK[cur["status"]]:
                    # same strength: prefer the row that knows more
                    if r.get("no_finite_model") and not cur.get("no_finite_model"):
                        best[law] = r
    return list(best.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patterns", nargs="+")
    ap.add_argument("--merge-out", default=None)
    ap.add_argument("--gold-out", default=None)
    a = ap.parse_args()

    rows = merge(a.patterns)
    if not rows:
        print("no rows"); return
    n = len(rows)
    st = collections.Counter(r["status"] for r in rows)
    print(f"{n} laws (deduped; strongest verdict per law)\n")
    for s in ORDER:
        if st[s]:
            print(f"  {st[s]:6d}  {s:<18} {GLOSS[s]}")
    proved = sum(st[s] for s in SETTLED)
    print(f"\n  settled (theorem):      {proved}/{n}")
    print(f"  open questions left:    {n - proved}/{n}")
    print(f"  proven Austin:          {st['AUSTIN_PROVEN']}")
    print(f"  proven no finite model: {st['AUSTIN_PROVEN'] + st['NO_FINITE_MODEL']}")

    bl = [r for r in rows if r.get("baseline")]
    if bl:
        print("\nbaseline (orthogonal axis - a fact about us, not the law):")
        for k, v in collections.Counter(r["baseline"] for r in bl).most_common():
            print(f"  {v:6d}  {k}")

    gold = [r for r in rows if r["status"] == "AUSTIN_PROVEN"
            and r.get("baseline") == "open_to_us"]
    print(f"\nBENCHMARK GOLD: {len(gold)}  (proved Austin, no construction from our suite)")
    for r in gold[:25]:
        print("  " + r["law"])
    if len(gold) > 25:
        print(f"  ... and {len(gold)-25} more")

    if a.merge_out:
        with open(a.merge_out, "w") as f:
            for r in sorted(rows, key=lambda r: (ORDER.index(r["status"]), r["law"])):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\nmerged corpus -> {a.merge_out}")
    if a.gold_out:
        with open(a.gold_out, "w") as f:
            for r in gold:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"gold set      -> {a.gold_out}")


if __name__ == "__main__":
    main()
