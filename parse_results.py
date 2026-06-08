#!/usr/bin/env python3
"""
parse_results.py

Analyze Stage 2 runner results JSON/JSONL.

Features:
  - overall solved/unsolved score
  - verdict/stage/time/call breakdowns
  - optional join with problem JSON/JSONL to show equation text + gold answer
  - inspect specific IDs with final accepted solution code if solved
  - inspect failed judge attempts and LLM responses if unsolved
  - export CSV
  - dump accepted solution code files
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
from typing import Any, Dict, List, Optional, Tuple


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
    if text[0] in "[{":
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def normalize_rows(obj: Any) -> List[Dict[str, Any]]:
    if isinstance(obj, list):
        return [r for r in obj if isinstance(r, dict)]
    if isinstance(obj, dict):
        for key in ("results", "entries", "data", "rows"):
            if isinstance(obj.get(key), list):
                return [r for r in obj[key] if isinstance(r, dict)]
        vals = list(obj.values())
        if vals and all(isinstance(v, dict) for v in vals):
            return vals
        return [obj]
    raise TypeError(f"Unsupported result shape: {type(obj)}")


def load_results(path: Path) -> List[Dict[str, Any]]:
    return normalize_rows(load_json_or_jsonl(path))


def load_problems(path: Optional[Path]) -> Dict[str, Dict[str, Any]]:
    if path is None:
        return {}
    rows = normalize_rows(load_json_or_jsonl(path))
    out: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        pid = r.get("id") or r.get("problem_id")
        if pid:
            out[str(pid)] = r
    return out


def log_entries(row: Dict[str, Any], typ: Optional[str] = None) -> List[Dict[str, Any]]:
    logs = row.get("log") or []
    if not isinstance(logs, list):
        return []
    if typ is None:
        return [x for x in logs if isinstance(x, dict)]
    return [x for x in logs if isinstance(x, dict) and x.get("type") == typ]


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


def judge_entries(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    return log_entries(row, "judge")


def llm_entries(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    return log_entries(row, "llm")


def judge_time(row: Dict[str, Any]) -> float:
    return sum(float(e.get("elapsed") or 0.0) for e in judge_entries(row))


def llm_time(row: Dict[str, Any]) -> float:
    return sum(float(e.get("elapsed") or 0.0) for e in llm_entries(row))


def accepted_judge_code(row: Dict[str, Any]) -> Optional[str]:
    """Prefer top-level final code, otherwise accepted judge request code."""
    code = row.get("code")
    if isinstance(code, str) and code.strip():
        return code
    for e in judge_entries(row):
        resp = e.get("response") or {}
        req = e.get("request") or {}
        if isinstance(resp, dict) and resp.get("status") == "accepted":
            c = req.get("code")
            if isinstance(c, str) and c.strip():
                return c
    return None


def final_solution_kind(row: Dict[str, Any]) -> str:
    code = accepted_judge_code(row)
    if code:
        return "accepted_code"
    if row.get("solved"):
        return "solved_no_code?"
    return "no_final_solution"


def get_attempt_code(row: Dict[str, Any], attempt_index: int) -> Optional[str]:
    judges = judge_entries(row)
    if 1 <= attempt_index <= len(judges):
        req = judges[attempt_index - 1].get("request") or {}
        c = req.get("code")
        return c if isinstance(c, str) else None
    return None


def summarize_llm_response(entry: Dict[str, Any]) -> str:
    resp = entry.get("response")
    if isinstance(resp, dict):
        if isinstance(resp.get("response"), str):
            return resp["response"]
        return json.dumps(resp, ensure_ascii=False)
    if isinstance(resp, str):
        return resp
    return ""


def truncate(s: Any, n: int) -> str:
    s = "" if s is None else str(s)
    if n <= 0 or len(s) <= n:
        return s
    return s[: max(0, n - 3)] + "..."


def indent_block(s: str, prefix: str = "  ") -> str:
    return textwrap.indent(s.rstrip(), prefix)


def row_stage(row: Dict[str, Any]) -> str:
    info = parse_stderr(row)
    if info["solved_candidate"]:
        return info["solved_candidate"]
    if info["stages"]:
        return info["stages"][-1]
    return "?"


def joined_problem(row: Dict[str, Any], problems: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    pid = str(row.get("id", ""))
    p = problems.get(pid, {})
    info = parse_stderr(row)
    return {
        "equation1": p.get("equation1") or info.get("eq1_text"),
        "equation2": p.get("equation2") or info.get("eq2_text"),
        "answer": p.get("answer"),
        "difficulty": p.get("difficulty"),
        "index": p.get("index"),
    }


def sort_rows(rows: List[Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
    if mode == "time_desc":
        return sorted(rows, key=lambda r: float(r.get("elapsed_seconds") or 0.0), reverse=True)
    if mode == "time_asc":
        return sorted(rows, key=lambda r: float(r.get("elapsed_seconds") or 0.0))
    if mode == "judge_calls_desc":
        return sorted(rows, key=lambda r: int(r.get("judge_calls") or 0), reverse=True)
    if mode == "llm_calls_desc":
        return sorted(rows, key=lambda r: int(r.get("llm_calls") or 0), reverse=True)
    if mode == "id":
        return sorted(rows, key=lambda r: str(r.get("id", "")))
    return rows


def percentile(xs: List[float], p: float) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = (len(xs) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    frac = k - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def print_summary(rows: List[Dict[str, Any]]) -> None:
    n = len(rows)
    solved = [r for r in rows if bool(r.get("solved"))]
    unsolved = [r for r in rows if not bool(r.get("solved"))]
    elapsed = [float(r.get("elapsed_seconds") or 0.0) for r in rows]
    verdicts = Counter(r.get("verdict") for r in rows)
    stages_solved = Counter(row_stage(r) for r in solved)
    stages_unsolved = Counter(row_stage(r) for r in unsolved)

    total_judge_calls = sum(int(r.get("judge_calls") or len(judge_entries(r))) for r in rows)
    total_llm_calls = sum(int(r.get("llm_calls") or len(llm_entries(r))) for r in rows)
    total_judge_time = sum(judge_time(r) for r in rows)
    total_llm_time = sum(llm_time(r) for r in rows)
    total_elapsed = sum(elapsed)
    overhead = total_elapsed - total_judge_time - total_llm_time

    print("=== Overall ===")
    print(f"rows:             {n}")
    print(f"solved:           {len(solved)} / {n} ({(100*len(solved)/n if n else 0):.1f}%)")
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

    print("\n=== Solved by candidate/stage ===")
    for k, v in stages_solved.most_common():
        print(f"{v:5d}  {k}")

    print("\n=== Unsolved last observed stage ===")
    for k, v in stages_unsolved.most_common():
        print(f"{v:5d}  {k}")

    print("\n=== Verdict counts, including unsolved/missing ===")
    for k, v in verdicts.most_common():
        print(f"{v:5d}  {k}")


def print_row_detail(
    row: Dict[str, Any],
    problems: Dict[str, Dict[str, Any]],
    show_code: bool,
    show_attempts: bool,
    show_llm: bool,
    show_log: bool,
    attempt_code: Optional[int],
    max_chars: int,
) -> None:
    pid = row.get("id", "?")
    p = joined_problem(row, problems)
    info = parse_stderr(row)

    print("\n" + "=" * 88)
    print(f"{pid}")
    print("-" * 88)
    print(
        f"eq1_id={row.get('eq1_id')} eq2_id={row.get('eq2_id')} "
        f"solved={row.get('solved')} verdict={row.get('verdict')} "
        f"gold={p.get('answer')}"
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
    print(f"Solution status: {final_solution_kind(row)}")

    if show_code:
        code = accepted_judge_code(row)
        print("\nFinal accepted solution code:")
        if code:
            print(indent_block(truncate(code, max_chars)))
        else:
            print("  <not stored; row is unsolved or no accepted judge request exists>")

    if attempt_code is not None:
        c = get_attempt_code(row, attempt_code)
        print(f"\nJudge attempt {attempt_code} code:")
        if c:
            print(indent_block(truncate(c, max_chars)))
        else:
            print("  <no such judge attempt>")

    if show_attempts:
        judges = judge_entries(row)
        print(f"\nJudge attempts ({len(judges)}):")
        for i, e in enumerate(judges, start=1):
            req = e.get("request") or {}
            resp = e.get("response") or {}
            status = resp.get("status")
            msg = resp.get("message")
            verdict = req.get("verdict")
            elapsed = float(e.get("elapsed") or 0.0)
            print(f"\n  Attempt {i}: verdict={verdict} status={status} elapsed={elapsed:.2f}s")
            if msg:
                print(indent_block(truncate(msg, max_chars), "    "))
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
                if ctx:
                    print("    solver_context:")
                    print(indent_block(truncate(json.dumps(ctx, ensure_ascii=False, indent=2), max_chars), "      "))
            response = summarize_llm_response(e)
            if response:
                print("    response:")
                print(indent_block(truncate(response, max_chars), "      "))

    if show_log:
        raw = row.get("log")
        print("\nRaw log:")
        print(indent_block(truncate(json.dumps(raw, ensure_ascii=False, indent=2), max_chars)))


def export_csv(rows: List[Dict[str, Any]], problems: Dict[str, Dict[str, Any]], path: Path) -> None:
    fields = [
        "id", "eq1_id", "eq2_id", "solved", "verdict", "gold_answer",
        "elapsed_seconds", "judge_calls", "llm_calls", "judge_time", "llm_time",
        "overhead_estimate", "candidate_stage", "singleton_hint", "equation1",
        "equation2", "has_final_code",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            p = joined_problem(r, problems)
            info = parse_stderr(r)
            elapsed = float(r.get("elapsed_seconds") or 0.0)
            jt = judge_time(r)
            lt = llm_time(r)
            w.writerow({
                "id": r.get("id"),
                "eq1_id": r.get("eq1_id"),
                "eq2_id": r.get("eq2_id"),
                "solved": r.get("solved"),
                "verdict": r.get("verdict"),
                "gold_answer": p.get("answer"),
                "elapsed_seconds": elapsed,
                "judge_calls": r.get("judge_calls"),
                "llm_calls": r.get("llm_calls"),
                "judge_time": jt,
                "llm_time": lt,
                "overhead_estimate": elapsed - jt - lt,
                "candidate_stage": row_stage(r),
                "singleton_hint": info.get("singleton_hint"),
                "equation1": p.get("equation1"),
                "equation2": p.get("equation2"),
                "has_final_code": bool(accepted_judge_code(r)),
            })


def dump_solutions(rows: List[Dict[str, Any]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for r in rows:
        code = accepted_judge_code(r)
        if not code:
            continue
        pid = str(r.get("id", f"row_{count}"))
        verdict = str(r.get("verdict", "unknown"))
        path = out_dir / f"{pid}_{verdict}.lean"
        path.write_text(code, encoding="utf-8")
        count += 1
    print(f"Wrote {count} accepted Lean solution files to {out_dir}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze Stage 2 results JSON/JSONL.")
    ap.add_argument("results", type=Path)
    ap.add_argument("--problems", type=Path, help="Optional problem JSON/JSONL to join equation text and gold answer.")
    ap.add_argument("--id", nargs="+", help="Show details for specific problem IDs.")
    ap.add_argument("--only", choices=["all", "solved", "unsolved", "true", "false"], default="all")
    ap.add_argument("--limit", type=int, default=0, help="Limit displayed detail rows. 0 means no details unless --id is used.")
    ap.add_argument("--sort", choices=["input", "id", "time_desc", "time_asc", "judge_calls_desc", "llm_calls_desc"], default="input")
    ap.add_argument("--show-code", action="store_true", help="Show final accepted solution code; for attempts, also shows attempted code.")
    ap.add_argument("--show-attempts", action="store_true", help="Show judge attempts and error messages.")
    ap.add_argument("--show-llm", action="store_true", help="Show LLM call summaries and responses.")
    ap.add_argument("--show-log", action="store_true", help="Show raw log JSON for displayed rows.")
    ap.add_argument("--attempt-code", type=int, help="Show code for a specific judge attempt number for displayed rows.")
    ap.add_argument("--max-chars", type=int, default=4000, help="Max chars for displayed code/messages/LLM outputs. 0 = unlimited.")
    ap.add_argument("--export-csv", type=Path)
    ap.add_argument("--dump-solutions", type=Path, help="Directory to write accepted Lean solution files.")
    args = ap.parse_args()

    rows = load_results(args.results)
    problems = load_problems(args.problems)

    if args.only == "solved":
        rows2 = [r for r in rows if bool(r.get("solved"))]
    elif args.only == "unsolved":
        rows2 = [r for r in rows if not bool(r.get("solved"))]
    elif args.only == "true":
        rows2 = [r for r in rows if r.get("verdict") == "true"]
    elif args.only == "false":
        rows2 = [r for r in rows if r.get("verdict") == "false"]
    else:
        rows2 = rows

    if args.id:
        ids = set(args.id)
        rows2 = [r for r in rows if str(r.get("id")) in ids]

    rows2 = sort_rows(rows2, args.sort)

    print_summary(rows)

    if args.export_csv:
        export_csv(rows, problems, args.export_csv)
        print(f"\nWrote CSV: {args.export_csv}")

    if args.dump_solutions:
        dump_solutions(rows, args.dump_solutions)

    if args.id:
        to_show = rows2
    elif args.limit and args.limit > 0:
        to_show = rows2[: args.limit]
    else:
        to_show = []

    if to_show:
        print(f"\n=== Details: showing {len(to_show)} row(s) ===")
        for r in to_show:
            print_row_detail(
                r,
                problems,
                show_code=args.show_code,
                show_attempts=args.show_attempts,
                show_llm=args.show_llm,
                show_log=args.show_log,
                attempt_code=args.attempt_code,
                max_chars=args.max_chars,
            )


if __name__ == "__main__":
    main()
