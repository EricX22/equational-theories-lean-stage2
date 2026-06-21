#!/usr/bin/env python3
"""LLM-contribution report.

Loops over result files in a results directory (default ``pipeline/results``,
default glob ``*merged*.json``; pass --glob to target others) and reports, per
file and in total:

  - solved / total
  - used_llm count          -> the agentic system's measurable contribution
  - solved_by distribution  -> which stage produced each accepted certificate
  - the specific problem IDs the LLM solved (with the stage that did it)

Reads the structured ``used_llm`` / ``solved_by`` fields the proxy now records,
so the LLM-vs-deterministic split is exact, not trace-parsed. Rows missing those
fields (e.g. carried over from a pre-attribution run via the runner's
skip-solved cache) are bucketed as ``(untagged)``.

Usage:
    python3 scripts/llm_report.py
    python3 scripts/llm_report.py --results-dir pipeline/results --glob '*llm*.json'
    python3 scripts/llm_report.py --show-ids
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def dataset_of(rows: list[dict]) -> str:
    for r in rows:
        rid = r.get("id", "")
        if "_" in rid:
            return rid.rsplit("_", 1)[0]
    return "?"


def load_rows(path: Path):
    """Tolerant load: returns (rows, error). A truncated/corrupt file yields
    ([], message) rather than crashing the whole report."""
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        return [], f"unreadable ({exc.__class__.__name__})"
    if not isinstance(data, list):
        return [], "not a list of result rows"
    return data, None


def main() -> None:
    ap = argparse.ArgumentParser(description="LLM-contribution report over result files")
    ap.add_argument("--results-dir", default="pipeline/results",
                    help="directory of result JSON files (default: pipeline/results)")
    ap.add_argument("--glob", nargs="+", default=["*merged*.json"],
                    help="filename glob(s) to include (default: *merged*.json). "
                         "Pass several to combine, e.g. "
                         "--glob '*merged*.json' '*llm*.json'.")
    ap.add_argument("--show-ids", action="store_true",
                    help="list the problem IDs the LLM solved, per file")
    args = ap.parse_args()

    results_dir = Path(args.results_dir)
    matched = {}
    for pat in args.glob:
        for p in results_dir.glob(pat):
            matched[p.name] = p           # dedupe by name across patterns
    files = sorted(matched.values())
    if not files:
        print(f"No files matching {args.glob} in {results_dir}")
        return

    grand_used_llm = 0
    grand_solved = 0
    grand_total = 0
    grand_stage = Counter()

    print(f"=== LLM-contribution report — {results_dir}/ [{' '.join(args.glob)}] ===\n")
    for path in files:
        rows, err = load_rows(path)
        if err:
            print(f"{path.name}: SKIPPED — {err}\n")
            continue
        total = len(rows)
        solved = [r for r in rows if r.get("solved")]
        used_llm = [r for r in solved if r.get("used_llm")]
        # Was the LLM actually invoked? Distinguishes "ran and lost" from
        # "never ran" — both look like used_llm=0 otherwise.
        llm_calls = sum(int(r.get("llm_calls") or 0) for r in rows)
        llm_ran = sum(1 for r in rows if (r.get("llm_calls") or 0) > 0)
        # solved_by distribution over SOLVED rows (None -> untagged)
        stage_dist = Counter((r.get("solved_by") or "(untagged)") for r in solved)

        grand_total += total
        grand_solved += len(solved)
        grand_used_llm += len(used_llm)
        grand_stage.update(stage_dist)

        ds = dataset_of(rows)
        pct = (100.0 * len(solved) / total) if total else 0.0
        print(f"{path.name}  [{ds}]")
        print(f"  solved {len(solved)}/{total} ({pct:.1f}%)  |  used_llm (LLM-solved): {len(used_llm)}"
              f"  |  LLM invoked on {llm_ran} problems ({llm_calls} calls)")
        print("  solved_by:")
        for stage, n in stage_dist.most_common():
            tag = "  <- LLM" if stage.startswith("LLM") else ""
            print(f"      {n:>5}  {stage}{tag}")
        if args.show_ids and used_llm:
            print("  LLM-solved IDs:")
            for r in used_llm:
                print(f"      {r.get('id')}  ({r.get('solved_by')}, "
                      f"verdict={r.get('verdict')}, llm_calls={r.get('llm_calls')})")
        print()

    print("=" * 60)
    print(f"GRAND TOTAL across {len(files)} file(s): "
          f"solved {grand_solved}/{grand_total}  |  LLM-solved (used_llm): {grand_used_llm}")
    llm_stages = {s: n for s, n in grand_stage.items() if s.startswith("LLM")}
    if llm_stages:
        print("LLM solves by stage: " +
              ", ".join(f"{s}={n}" for s, n in sorted(llm_stages.items())))


if __name__ == "__main__":
    main()
