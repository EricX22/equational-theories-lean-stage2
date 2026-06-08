#!/usr/bin/env python3
"""
parse_results.py

Analyze Stage 2 runner results JSON/JSONL, optionally joined with a problem JSONL.

Examples:

  python parse_results.py pipeline/results/my_solver.json

  python parse_results.py pipeline/results/my_solver.json \
    --problems examples/problems/normal.jsonl

  python parse_results.py pipeline/results/my_solver.json \
    --problems examples/problems/normal.jsonl \
    --id normal_0032 --show-attempts --show-llm --show-code

  python parse_results.py pipeline/results/my_solver.json \
    --problems examples/problems/normal.jsonl \
    --only unsolved --sort time_desc --limit 10 --show-attempts --show-llm

  python parse_results.py pipeline/results/my_solver.json \
    --problems examples/problems/normal.jsonl \
    --only wrong --limit 20

  python parse_results.py pipeline/results/my_solver.json \
    --problems examples/problems/normal.jsonl \
    --export-csv results_summary.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics as stats
import textwrap
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional


STAGE_RE = re.compile(r"^\[stage\]\s*(.*)$")
SOLVED_CAND_RE = re.compile(r"^\[solved-candidate\]\s*(.*)$")
PROBLEM_RE = re.compile(r"^\[problem\]\s+(\S+)\s+eq1=(\d+)\s+eq2=(\d+)")
EQ1_RE = re.compile(r"^\[eq1\]\s*(.*)$")
EQ2_RE = re.compile(r"^\[eq2\]\s*(.*)$")
SINGLETON_RE = re.compile(r"^\[singleton_hint\]\s*(.*)$")


def load_json_or_jsonl(path: Path) -> Any:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # Try ordinary JSON first.
    if text[0] in "[{":
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    # Fall back to JSONL.
    rows = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSONL line {line_no} in {path}: {e}") from e
    return rows


def normalize_rows(obj: Any) -> List[Dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]

    if isinstance(obj, dict):
        for key in ("results", "entries", "data", "rows"):
            if isinstance(obj.get(key), list):
                return [x for x in obj[key] if isinstance(x, dict)]

        # Mapping from id -> result row.
        vals = list(obj.values())
        if vals and all(isinstance(v, dict) for v in vals):
            return vals

        # Single row object.
        if "id" in obj:
            return [obj]

    raise TypeError(f"Unsupported JSON shape: {type(obj)}")


def load_results(path: Path) -> List[Dict[str, Any]]:
    return normalize_rows(load_json_or_jsonl(path))


def load_problems(path: Optional[Path]) -> Dict[str, Dict[str, Any]]:
    if path is None:
        return {}

    rows = normalize_rows(load_json_or_jsonl(path))
    out: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        pid = r.get("id") or r.get("problem_id")
        if pid is not None:
            out[str(pid)] = r
    return out


def log_entries(row: Dict[str, Any], typ: Optional[str] = None) -> List[Dict[str, Any]]:
    logs = row.get("log") or []
    if not isinstance(logs, list):
        return []
    if typ is None:
        return [x for x in logs if isinstance(x, dict)]
    return [x for x in logs if isinstance(x, dict) and x.get("type") == typ]


def judge_entries(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    return log_entries(row, "judge")


def llm_entries(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    return log_entries(row, "llm")


def stderr_text(row: Dict[str, Any]) -> str:
    parts = []
    for e in log_entries(row, "solver_stderr"):
        tail = e.get("tail")
        if isinstance(tail, str):
            parts.append(tail)
    return "\n".join(parts)


def parse_stderr(row: Dict[str, Any]) -> Dict[str, Any]:
    text = stderr_text(row)
    info: Dict[str, Any] = {
        "problem_line": None,
        "eq1_text": None,
        "eq2_text": None,
        "stages": [],
        "solved_candidate": None,
        "singleton_hint": None,
    }

    for line in text.splitlines():
        m = PROBLEM_RE.match(line)
        if m:
            info["problem_line"] = line

        m = EQ1_RE.match(line)
        if m:
            info["eq1_text"] = m.group(1)

        m = EQ2_RE.match(line)
        if m:
            info["eq2_text"] = m.group(1)

        m = STAGE_RE.match(line)
        if m:
            info["stages"].append(m.group(1))

        m = SOLVED_CAND_RE.match(line)
        if m:
            info["solved_candidate"] = m.group(1)

        m = SINGLETON_RE.match(line)
        if m:
            info["singleton_hint"] = m.group(1)

    return info


def judge_time(row: Dict[str, Any]) -> float:
    return sum(float(e.get("elapsed") or 0.0) for e in judge_entries(row))


def llm_time(row: Dict[str, Any]) -> float:
    return sum(float(e.get("elapsed") or 0.0) for e in llm_entries(row))


def accepted_solution_code(row: Dict[str, Any]) -> Optional[str]:
    """
    Final Lean certificate/code.

    Usually top-level row["code"] for solved cases.
    If missing, recover accepted judge request code from log.
    """
    code = row.get("code")
    if isinstance(code, str) and code.strip():
        return code

    for e in judge_entries(row):
        resp = e.get("response") or {}
        req = e.get("request") or {}
        if isinstance(resp, dict) and resp.get("status") == "accepted":
            code = req.get("code")
            if isinstance(code, str) and code.strip():
                return code

    return None


def attempt_code(row: Dict[str, Any], idx_1based: int) -> Optional[str]:
    entries = judge_entries(row)
    if idx_1based < 1 or idx_1based > len(entries):
        return None
    req = entries[idx_1based - 1].get("request") or {}
    code = req.get("code")
    return code if isinstance(code, str) else None


def problem_info(row: Dict[str, Any], problems: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    pid = str(row.get("id", ""))
    p = problems.get(pid, {})
    stderr = parse_stderr(row)

    return {
        "id": pid,
        "index": p.get("index"),
        "difficulty": p.get("difficulty"),
        "eq1_id": p.get("eq1_id", row.get("eq1_id")),
        "eq2_id": p.get("eq2_id", row.get("eq2_id")),
        "equation1": p.get("equation1") or stderr.get("eq1_text"),
        "equation2": p.get("equation2") or stderr.get("eq2_text"),
        "answer": p.get("answer"),
    }


def answer_as_verdict(answer: Any) -> Optional[str]:
    if answer is None:
        return None
    if isinstance(answer, bool):
        return "true" if answer else "false"
    s = str(answer).strip().lower()
    if s in ("true", "false"):
        return s
    return None


def verdict_matches_gold(row: Dict[str, Any], problems: Dict[str, Dict[str, Any]]) -> Optional[bool]:
    p = problem_info(row, problems)
    gold = answer_as_verdict(p.get("answer"))
    verdict = row.get("verdict")
    if gold is None or verdict is None:
        return None
    return str(verdict).lower() == gold


def row_stage(row: Dict[str, Any]) -> str:
    info = parse_stderr(row)
    if info["solved_candidate"]:
        return info["solved_candidate"]
    if info["stages"]:
        return info["stages"][-1]
    return "?"


def percentile(xs: List[float], p: float) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = (len(xs) - 1) * p / 100.0
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    frac = k - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def truncate(s: Any, n: int) -> str:
    s = "" if s is None else str(s)
    if n <= 0 or len(s) <= n:
        return s
    return s[: max(0, n - 3)] + "..."


def indent_block(s: str, prefix: str = "  ") -> str:
    return textwrap.indent(s.rstrip(), prefix)


def summarize_llm_response(entry: Dict[str, Any]) -> str:
    resp = entry.get("response")
    if isinstance(resp, dict):
        if isinstance(resp.get("response"), str):
            return resp["response"]
        return json.dumps(resp, ensure_ascii=False)
    if isinstance(resp, str):
        return resp
    return ""


def sort_rows(rows: List[Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
    if mode == "input":
        return rows
    if mode == "id":
        return sorted(rows, key=lambda r: str(r.get("id", "")))
    if mode == "time_desc":
        return sorted(rows, key=lambda r: float(r.get("elapsed_seconds") or 0.0), reverse=True)
    if mode == "time_asc":
        return sorted(rows, key=lambda r: float(r.get("elapsed_seconds") or 0.0))
    if mode == "judge_calls_desc":
        return sorted(rows, key=lambda r: int(r.get("judge_calls") or 0), reverse=True)
    if mode == "llm_calls_desc":
        return sorted(rows, key=lambda r: int(r.get("llm_calls") or 0), reverse=True)
    raise ValueError(f"Unknown sort mode: {mode}")


def print_summary(rows: List[Dict[str, Any]], problems: Dict[str, Dict[str, Any]]) -> None:
    n = len(rows)
    solved = [r for r in rows if bool(r.get("solved"))]
    unsolved = [r for r in rows if not bool(r.get("solved"))]
    elapsed = [float(r.get("elapsed_seconds") or 0.0) for r in rows]
    verdicts = Counter(r.get("verdict") for r in rows)
    solved_stages = Counter(row_stage(r) for r in solved)
    unsolved_stages = Counter(row_stage(r) for r in unsolved)

    total_elapsed = sum(elapsed)
    total_judge_calls = sum(int(r.get("judge_calls") or len(judge_entries(r))) for r in rows)
    total_llm_calls = sum(int(r.get("llm_calls") or len(llm_entries(r))) for r in rows)
    total_judge_time = sum(judge_time(r) for r in rows)
    total_llm_time = sum(llm_time(r) for r in rows)
    overhead = total_elapsed - total_judge_time - total_llm_time

    print("=== Overall ===")
    print(f"rows:             {n}")
    print(f"solved:           {len(solved)} / {n} ({100 * len(solved) / n if n else 0:.1f}%)")
    print(f"unsolved:         {len(unsolved)}")
    print(f"true verdicts:    {verdicts.get('true', 0)}")
    print(f"false verdicts:   {verdicts.get('false', 0)}")
    print(f"missing verdicts: {verdicts.get(None, 0)}")
    print(f"elapsed total:    {total_elapsed:.2f}s")

    if elapsed:
        print(
            "time distribution: "
            f"mean={stats.mean(elapsed):.2f}s "
            f"median={stats.median(elapsed):.2f}s "
            f"p90={percentile(elapsed, 90):.2f}s "
            f"max={max(elapsed):.2f}s"
        )

    print(f"judge calls:      {total_judge_calls} ({total_judge_time:.2f}s logged judge time)")
    print(f"llm calls:        {total_llm_calls} ({total_llm_time:.2f}s logged llm time)")
    print(f"solver/overhead:  {overhead:.2f}s approx")

    if problems:
        matched = 0
        correct_solved = 0
        wrong_solved = 0
        unsolved_true = 0
        unsolved_false = 0
        gold_counts = Counter()

        for r in rows:
            p = problem_info(r, problems)
            gold = answer_as_verdict(p.get("answer"))
            if gold is None:
                continue
            matched += 1
            gold_counts[gold] += 1

            if bool(r.get("solved")):
                m = verdict_matches_gold(r, problems)
                if m is True:
                    correct_solved += 1
                elif m is False:
                    wrong_solved += 1
            else:
                if gold == "true":
                    unsolved_true += 1
                elif gold == "false":
                    unsolved_false += 1

        print("\n=== Cross-check against problem answers ===")
        print(f"matched problem rows: {matched} / {n}")
        print(f"gold true:            {gold_counts.get('true', 0)}")
        print(f"gold false:           {gold_counts.get('false', 0)}")
        print(f"solved correct:       {correct_solved}")
        print(f"solved wrong:         {wrong_solved}")
        print(f"unsolved gold true:   {unsolved_true}")
        print(f"unsolved gold false:  {unsolved_false}")

    print("\n=== Solved by candidate/stage ===")
    for k, v in solved_stages.most_common():
        print(f"{v:5d}  {k}")

    print("\n=== Unsolved last observed stage ===")
    for k, v in unsolved_stages.most_common():
        print(f"{v:5d}  {k}")

    print("\n=== Verdict counts, including unsolved/missing ===")
    for k, v in verdicts.most_common():
        print(f"{v:5d}  {k}")


def print_detail(
    row: Dict[str, Any],
    problems: Dict[str, Dict[str, Any]],
    show_code: bool,
    show_attempts: bool,
    show_llm: bool,
    show_log: bool,
    attempt_code_num: Optional[int],
    max_chars: int,
) -> None:
    p = problem_info(row, problems)
    info = parse_stderr(row)
    match = verdict_matches_gold(row, problems)

    print("\n" + "=" * 88)
    print(f"{row.get('id')}")
    print("-" * 88)
    print(
        f"eq1_id={row.get('eq1_id')} eq2_id={row.get('eq2_id')} "
        f"solved={row.get('solved')} verdict={row.get('verdict')} "
        f"gold={answer_as_verdict(p.get('answer'))} match={match}"
    )
    print(
        f"elapsed={float(row.get('elapsed_seconds') or 0.0):.2f}s "
        f"judge_calls={row.get('judge_calls')} llm_calls={row.get('llm_calls')} "
        f"judge_time={judge_time(row):.2f}s llm_time={llm_time(row):.2f}s"
    )

    if p.get("equation1") or p.get("equation2"):
        print("\nProblem:")
        print(f"  Eq1: {p.get('equation1')}")
        print(f"  Eq2: {p.get('equation2')}")

    if info["stages"]:
        print("\nStages:")
        for s in info["stages"]:
            print(f"  - {s}")

    if info["singleton_hint"] is not None:
        print(f"\nSingleton hint: {info['singleton_hint']}")

    print(f"\nCandidate/stage result: {row_stage(row)}")

    final_code = accepted_solution_code(row)
    if show_code:
        print("\nFinal accepted solution code:")
        if final_code:
            print(indent_block(truncate(final_code, max_chars)))
        else:
            print("  <none stored: unsolved row or no accepted judge attempt>")

    if attempt_code_num is not None:
        code = attempt_code(row, attempt_code_num)
        print(f"\nJudge attempt {attempt_code_num} code:")
        if code:
            print(indent_block(truncate(code, max_chars)))
        else:
            print("  <no such attempt>")

    if show_attempts:
        judges = judge_entries(row)
        print(f"\nJudge attempts ({len(judges)}):")
        for i, e in enumerate(judges, start=1):
            req = e.get("request") or {}
            resp = e.get("response") or {}
            verdict = req.get("verdict")
            status = resp.get("status")
            message = resp.get("message")
            elapsed = float(e.get("elapsed") or 0.0)
            print(f"\n  Attempt {i}: verdict={verdict} status={status} elapsed={elapsed:.2f}s")
            if message:
                print(indent_block(truncate(message, max_chars), "    "))

            if show_code:
                code = req.get("code")
                if isinstance(code, str):
                    print("    code:")
                    print(indent_block(truncate(code, max_chars), "      "))

    if show_llm:
        llms = llm_entries(row)
        print(f"\nLLM calls ({len(llms)}):")
        for i, e in enumerate(llms, start=1):
            elapsed = float(e.get("elapsed") or 0.0)
            print(f"\n  LLM call {i}: elapsed={elapsed:.2f}s")
            req = e.get("request") or {}

            if isinstance(req, dict):
                ctx = req.get("solver_context")
                if ctx is not None:
                    print("    solver_context:")
                    print(indent_block(truncate(json.dumps(ctx, ensure_ascii=False, indent=2), max_chars), "      "))

            resp = summarize_llm_response(e)
            if resp:
                print("    response:")
                print(indent_block(truncate(resp, max_chars), "      "))

    if show_log:
        print("\nRaw log:")
        print(indent_block(truncate(json.dumps(row.get("log"), ensure_ascii=False, indent=2), max_chars)))


def export_csv(rows: List[Dict[str, Any]], problems: Dict[str, Dict[str, Any]], path: Path) -> None:
    fields = [
        "id",
        "index",
        "difficulty",
        "eq1_id",
        "eq2_id",
        "equation1",
        "equation2",
        "gold_answer",
        "solved",
        "verdict",
        "verdict_matches_gold",
        "elapsed_seconds",
        "judge_calls",
        "llm_calls",
        "judge_time",
        "llm_time",
        "overhead_estimate",
        "candidate_stage",
        "singleton_hint",
        "has_final_code",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()

        for r in rows:
            p = problem_info(r, problems)
            info = parse_stderr(r)
            elapsed = float(r.get("elapsed_seconds") or 0.0)
            jt = judge_time(r)
            lt = llm_time(r)

            w.writerow(
                {
                    "id": r.get("id"),
                    "index": p.get("index"),
                    "difficulty": p.get("difficulty"),
                    "eq1_id": r.get("eq1_id"),
                    "eq2_id": r.get("eq2_id"),
                    "equation1": p.get("equation1"),
                    "equation2": p.get("equation2"),
                    "gold_answer": answer_as_verdict(p.get("answer")),
                    "solved": r.get("solved"),
                    "verdict": r.get("verdict"),
                    "verdict_matches_gold": verdict_matches_gold(r, problems),
                    "elapsed_seconds": elapsed,
                    "judge_calls": r.get("judge_calls"),
                    "llm_calls": r.get("llm_calls"),
                    "judge_time": jt,
                    "llm_time": lt,
                    "overhead_estimate": elapsed - jt - lt,
                    "candidate_stage": row_stage(r),
                    "singleton_hint": info.get("singleton_hint"),
                    "has_final_code": bool(accepted_solution_code(r)),
                }
            )


def dump_solutions(rows: List[Dict[str, Any]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    for r in rows:
        code = accepted_solution_code(r)
        if not code:
            continue
        pid = str(r.get("id", f"row_{count}"))
        verdict = str(r.get("verdict", "unknown"))
        path = out_dir / f"{pid}_{verdict}.lean"
        path.write_text(code, encoding="utf-8")
        count += 1

    print(f"\nWrote {count} accepted Lean solution files to {out_dir}")


def filter_rows(rows: List[Dict[str, Any]], problems: Dict[str, Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
    if mode == "all":
        return rows
    if mode == "solved":
        return [r for r in rows if bool(r.get("solved"))]
    if mode == "unsolved":
        return [r for r in rows if not bool(r.get("solved"))]
    if mode == "true":
        return [r for r in rows if str(r.get("verdict")).lower() == "true"]
    if mode == "false":
        return [r for r in rows if str(r.get("verdict")).lower() == "false"]
    if mode == "gold_true":
        return [r for r in rows if answer_as_verdict(problem_info(r, problems).get("answer")) == "true"]
    if mode == "gold_false":
        return [r for r in rows if answer_as_verdict(problem_info(r, problems).get("answer")) == "false"]
    if mode == "wrong":
        return [r for r in rows if verdict_matches_gold(r, problems) is False]
    if mode == "unsolved_gold_true":
        return [
            r
            for r in rows
            if not bool(r.get("solved"))
            and answer_as_verdict(problem_info(r, problems).get("answer")) == "true"
        ]
    if mode == "unsolved_gold_false":
        return [
            r
            for r in rows
            if not bool(r.get("solved"))
            and answer_as_verdict(problem_info(r, problems).get("answer")) == "false"
        ]
    raise ValueError(f"Unknown filter mode: {mode}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("results", type=Path)
    ap.add_argument("--problems", type=Path, help="Problem JSON/JSONL with id, equation1, equation2, answer.")
    ap.add_argument("--id", nargs="+", help="Problem IDs to inspect.")

    ap.add_argument(
        "--only",
        choices=[
            "all",
            "solved",
            "unsolved",
            "true",
            "false",
            "gold_true",
            "gold_false",
            "wrong",
            "unsolved_gold_true",
            "unsolved_gold_false",
        ],
        default="all",
    )
    ap.add_argument(
        "--sort",
        choices=["input", "id", "time_desc", "time_asc", "judge_calls_desc", "llm_calls_desc"],
        default="input",
    )
    ap.add_argument("--limit", type=int, default=0, help="Show this many detailed rows. 0 = summary only unless --id is set.")

    ap.add_argument("--show-code", action="store_true", help="Show final code. With --show-attempts, also show attempted code.")
    ap.add_argument("--show-attempts", action="store_true", help="Show judge attempts/errors.")
    ap.add_argument("--show-llm", action="store_true", help="Show LLM responses.")
    ap.add_argument("--show-log", action="store_true", help="Show raw log JSON.")
    ap.add_argument("--attempt-code", type=int, help="Show code for one judge attempt number.")
    ap.add_argument("--max-chars", type=int, default=4000, help="Truncate long blocks. 0 = unlimited.")

    ap.add_argument("--export-csv", type=Path)
    ap.add_argument("--dump-solutions", type=Path)

    args = ap.parse_args()

    rows = load_results(args.results)
    problems = load_problems(args.problems)

    print_summary(rows, problems)

    if args.export_csv:
        export_csv(rows, problems, args.export_csv)
        print(f"\nWrote CSV: {args.export_csv}")

    if args.dump_solutions:
        dump_solutions(rows, args.dump_solutions)

    if args.id:
        wanted = set(args.id)
        display_rows = [r for r in rows if str(r.get("id")) in wanted]
    else:
        display_rows = filter_rows(rows, problems, args.only)
        display_rows = sort_rows(display_rows, args.sort)
        if args.limit > 0:
            display_rows = display_rows[: args.limit]
        else:
            display_rows = []

    if display_rows:
        print(f"\n=== Details: showing {len(display_rows)} row(s) ===")
        for r in display_rows:
            print_detail(
                r,
                problems,
                show_code=args.show_code,
                show_attempts=args.show_attempts,
                show_llm=args.show_llm,
                show_log=args.show_log,
                attempt_code_num=args.attempt_code,
                max_chars=args.max_chars,
            )


if __name__ == "__main__":
    main()