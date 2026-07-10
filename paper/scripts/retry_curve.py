#!/usr/bin/env python3
"""The budget gate: what does 15x more compute actually buy? PAPER_PLAN.md §5C.

Every label in the corpus is a theorem except hard-tier membership, which means "no
prover we ran finished". The only way that becomes a claim about the LAW rather than
about our patience is to show more budget does not help. The retry stage is exactly
that experiment: the same laws, 20s vs 300s per prover.

Read the cross-tab in two directions, because they mean opposite things:

  NO_FINITE_MODEL -> TRIVIAL     the hard tier was CONTAMINATED. These laws were never
                                 Austin; they entail x=y and we could not prove it in
                                 budget. Removing them is a win, and the rate is the
                                 contamination estimate.
  NO_FINITE_MODEL -> AUSTIN      the hard tier was UNDER-BUDGETED. The saturation closes,
                                 it just needed longer. A high rate here means the
                                 frontier is compute-bound and the benchmark's central
                                 claim is wrong.
  stays put                      evidence (not proof) of method-boundedness, RELATIVE to
                                 the prover and ordering used. One prover is not a
                                 portfolio; see baseline_probe.py.

Also prints the resolution-time distribution of the conversions. If conversions cluster
well below the cap, the budget is past the knee for that direction. If they pile up
against the cap, it is not, and the "flat in log-budget" claim is unsupported.

USAGE
    python3 paper/scripts/retry_curve.py --results paper/results
"""
from __future__ import annotations
import argparse, collections, glob, json, os, statistics as st


def load(results):
    pre, post = {}, {}
    for fn in glob.glob(os.path.join(results, "*_status_*.jsonl")):
        base = os.path.basename(fn)
        for line in open(fn):
            r = json.loads(line)
            if base.startswith("retry"):
                post[r["law"]] = r
            else:
                pre[r["law"]] = (r["status"], base.split("_status")[0])
    return pre, post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="paper/results")
    ap.add_argument("--out")
    a = ap.parse_args()

    pre, post = load(a.results)
    both = [k for k in post if k in pre]
    if not both:
        print("no retry rows matched a pre-retry status — nothing to compare")
        return

    tab = collections.Counter((pre[k][0], post[k]["status"]) for k in both)
    conv = [(pre[k][0], post[k]["status"], post[k]["secs"], pre[k][1])
            for k in both if pre[k][0] != post[k]["status"]]
    stay = [post[k]["secs"] for k in both if pre[k][0] == post[k]["status"]]

    print(f"retry rows matched: {len(both)}\n")
    print(f"{'before':22s} {'after':18s} count")
    for (x, y), n in sorted(tab.items(), key=lambda t: -t[1]):
        print(f"{x:22s} {y:18s} {n:5d}{'   <- CONVERTED' if x != y else ''}")

    print(f"\nconversion rate: {len(conv)}/{len(both)} = {100*len(conv)/len(both):.1f}%")

    # The two readings that matter, isolated.
    nfm = [k for k in both if pre[k][0] == "NO_FINITE_MODEL"]
    to_triv = sum(1 for k in nfm if post[k]["status"] == "TRIVIAL")
    to_aust = sum(1 for k in nfm if post[k]["status"] == "AUSTIN_PROVEN")
    if nfm:
        print(f"\nof {len(nfm)} NO_FINITE_MODEL laws:")
        print(f"  -> TRIVIAL  {to_triv:4d}  ({100*to_triv/len(nfm):.1f}%)  "
              f"hard-tier CONTAMINATION, removed")
        print(f"  -> AUSTIN   {to_aust:4d}  ({100*to_aust/len(nfm):.1f}%)  "
              f"hard-tier UNDER-BUDGETING")
        if to_aust == 0:
            print("  ZERO saturations closed at 300s. Completion diverges on this tier;")
            print("  it is not merely slow. Also: the tier gains no models, so the cheap")
            print("  model-based separations of equiv_sample.py stay unavailable there.")

    if conv:
        print("\nconversions, by seconds spent in the retry:")
        for x, y, s, stage in sorted(conv, key=lambda t: t[2]):
            print(f"  {stage:5s} {x:17s} -> {y:16s} {s:8.1f}s")
    if stay:
        print(f"\nunconverted: median {st.median(stay):.0f}s, max {max(stay):.0f}s "
              f"(n={len(stay)}) — they burn the budget, they are not 'almost done'")

    print("\nCAVEATS: this is one prover and one term ordering. 'Stays put' is evidence")
    print("of method-boundedness relative to THAT configuration only. And the retry")
    print("covers a subset of the unsettled laws — read the rates, not the counts.")

    if a.out:
        json.dump({"matched": len(both), "conversions": len(conv),
                   "nfm": len(nfm), "to_trivial": to_triv, "to_austin": to_aust,
                   "unconverted_median_secs": st.median(stay) if stay else None},
                  open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
