#!/usr/bin/env python3
"""llm_failure_breakdown.py — turn LLM eval result files into the §4.3 table.

A bare "0/20" is not reportable; the failure MODE is the finding. This classifies every row,
excludes API failures from the denominator (429 rate-limits and reasoning-model output starvation
are not task failures — see the budget memory), and, when a waypoint ranking is supplied, breaks
the result down by instance difficulty.

Categories
  solved              judged correct (Lean or ATP certificate)
  invalid_step        a chain step is not a law application (and not bridgeable) -> DERIVATION-bound
  lean_rejected       assembled/emitted Lean failed the kernel        -> FORMALIZATION-bound
  malformed           no JSON / bad chain shape / degenerate equation -> FORMAT-bound
  wrong_side          targeted the wrong goal
  [excluded] api_error   429 / starved output / HTTP error — NOT counted in the denominator

USAGE
  python3 paper/scripts/llm_failure_breakdown.py paper/results/llm_autoform*.jsonl \
      --ranked paper/results/trivial_easy_ranked.jsonl
"""
from __future__ import annotations
import argparse, collections, glob, json, sys


def classify(r):
    if r.get("solved"):
        return "solved"
    blob = " ".join(str(r.get(k, "")) for k in ("error", "last", "last_reject", "last_spec"))
    low = blob.lower()
    if "api:" in low or "429" in low or "too many requests" in low or "http error" in low:
        return "api_error"
    if not blob.strip() and (r.get("secs") or 0) < 5:
        return "api_error"                       # instant no-op row = rate-limit/starvation
    # "unparsable term" = the model emitted a syntactically invalid term (e.g. unbalanced
    # parens) -> a FORMAT failure, not a separate phenomenon. Keep it out of "other".
    if ("no json" in low or "bad json" in low or "chain must" in low or "degenerate" in low
            or "unparsable" in low or "trailing tokens" in low or "index out of range" in low):
        return "malformed"
    if "must target" in low or "wrong side" in low:
        return "wrong_side"
    if "not a law application" in low or "not a whole-term" in low or "bridged" in low:
        return "invalid_step"
    if "lean rejected" in low or "error:" in low:
        return "lean_rejected"
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--ranked", help="jsonl with law->waypoints, to break down by difficulty")
    a = ap.parse_args()

    wp = {}
    if a.ranked:
        for line in open(a.ranked, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                if "waypoints" in r:
                    wp[r["law"]] = r["waypoints"]

    rows = []
    for pat in a.files:
        for fn in glob.glob(pat):
            for line in open(fn, encoding="utf-8"):
                if line.strip():
                    rows.append(json.loads(line))
    if not rows:
        print("no rows"); return

    bymodel = collections.defaultdict(list)
    for r in rows:
        bymodel[r.get("model", "?")].append(r)

    for model, rs in sorted(bymodel.items()):
        cats = collections.Counter(classify(r) for r in rs)
        excluded = cats.pop("api_error", 0)
        n = sum(cats.values())
        print(f"\n=== {model} ===")
        print(f"attempted {n}   (excluded {excluded} api/rate-limit rows from the denominator)")
        if n:
            for c, k in cats.most_common():
                print(f"  {c:16} {k:4}  {100*k/n:5.1f}%")
        # difficulty breakdown
        if wp:
            seen = [(wp.get(r.get('law')), classify(r)) for r in rs]
            seen = [(w, c) for w, c in seen if w is not None and c != "api_error"]
            if seen:
                byw = collections.defaultdict(lambda: [0, 0])
                for w, c in seen:
                    byw[w][0] += 1
                    byw[w][1] += (c == "solved")
                print("  by waypoint count (difficulty):")
                for w in sorted(byw):
                    tot, sv = byw[w]
                    print(f"    wp={w:<3} n={tot:<4} solved={sv}")
    print("\nRead: invalid_step => derivation-bound; lean_rejected => formalization-bound; "
          "malformed => format-bound.")


if __name__ == "__main__":
    main()
