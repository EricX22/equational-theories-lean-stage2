#!/usr/bin/env python3
"""Summarize SAIR Equational Theories Stage 2 runner results.

Works with a JSON array, JSON object with a results/items/data key, id->row dicts,
or JSONL. It prints an overall score, timing/call breakdowns, stage summaries,
and selected solved/unsolved examples with problem text, logs, and optionally code.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics as stats
from pathlib import Path
from typing import Any, Iterable


def load_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return [r for r in obj if isinstance(r, dict)]
        if isinstance(obj, dict):
            for key in ("results", "items", "entries", "data", "rows"):
                val = obj.get(key)
                if isinstance(val, list):
                    return [r for r in val if isinstance(r, dict)]
            # common fallback: {problem_id: row, ...}
            vals = list(obj.values())
            if vals and all(isinstance(v, dict) for v in vals):
                return vals
            return [obj]
    except json.JSONDecodeError:
        pass

    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip().rstrip(",")
        if not line:
            continue
        rows.append(json.loads(line))
    return [r for r in rows if isinstance(r, dict)]


def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except (TypeError, ValueError):
        return default


def log_entries(row: dict[str, Any], typ: str | None = None) -> list[dict[str, Any]]:
    log = row.get("log") or []
    if not isinstance(log, list):
        return []
    out = [e for e in log if isinstance(e, dict)]
    if typ is not None:
        out = [e for e in out if e.get("type") == typ]
    return out


def tail_text(row: dict[str, Any]) -> str:
    parts = []
    for e in log_entries(row, "solver_stderr"):
        t = e.get("tail")
        if isinstance(t, str):
            parts.append(t)
    return "\n".join(parts)


def extract_line(prefix: str, text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return None


def problem_eqs(row: dict[str, Any]) -> tuple[str | None, str | None]:
    text = tail_text(row)
    eq1 = extract_line("[eq1]", text)
    eq2 = extract_line("[eq2]", text)
    return eq1, eq2


def stages(row: dict[str, Any]) -> list[str]:
    text = tail_text(row)
    out = []
    for line in text.splitlines():
        if line.startswith("[stage]"):
            out.append(line[len("[stage]"):].strip())
    return out


def solved_candidate(row: dict[str, Any]) -> str | None:
    text = tail_text(row)
    for line in text.splitlines():
        if line.startswith("[solved-candidate]"):
            return line[len("[solved-candidate]"):].strip()
    # fallback: final stage before accepted judge
    st = stages(row)
    if row.get("solved") and st:
        return st[-1]
    return None


def judge_time(row: dict[str, Any]) -> float:
    return sum(safe_float(e.get("elapsed")) for e in log_entries(row, "judge"))


def llm_time(row: dict[str, Any]) -> float:
    return sum(safe_float(e.get("elapsed")) for e in log_entries(row, "llm"))


def fmt_seconds(x: float) -> str:
    return f"{x:.2f}s"


def quantiles(vals: list[float]) -> str:
    if not vals:
        return "-"
    vals = sorted(vals)
    mean = sum(vals) / len(vals)
    med = stats.median(vals)
    p90 = vals[int(0.9 * (len(vals) - 1))]
    return f"mean={fmt_seconds(mean)} median={fmt_seconds(med)} p90={fmt_seconds(p90)} max={fmt_seconds(max(vals))}"


def truncate(s: str | None, n: int) -> str:
    if not s:
        return ""
    s = s.rstrip()
    if n <= 0 or len(s) <= n:
        return s
    return s[: n - 3] + "..."


def print_summary(rows: list[dict[str, Any]]) -> None:
    total = len(rows)
    solved = [r for r in rows if bool(r.get("solved"))]
    unsolved = [r for r in rows if not bool(r.get("solved"))]
    true_rows = [r for r in solved if r.get("verdict") == "true"]
    false_rows = [r for r in solved if r.get("verdict") == "false"]

    total_elapsed = sum(safe_float(r.get("elapsed_seconds")) for r in rows)
    total_judge_time = sum(judge_time(r) for r in rows)
    total_llm_time = sum(llm_time(r) for r in rows)
    total_judge_calls = sum(safe_int(r.get("judge_calls")) for r in rows)
    total_llm_calls = sum(safe_int(r.get("llm_calls")) for r in rows)

    print("=== Overall ===")
    print(f"rows:             {total}")
    print(f"solved:           {len(solved)} / {total} ({(100 * len(solved) / total if total else 0):.1f}%)")
    print(f"unsolved:         {len(unsolved)}")
    print(f"true verdicts:    {len(true_rows)}")
    print(f"false verdicts:   {len(false_rows)}")
    print(f"elapsed total:    {fmt_seconds(total_elapsed)}")
    print(f"time distribution:{' ' if rows else ' '} {quantiles([safe_float(r.get('elapsed_seconds')) for r in rows])}")
    print(f"judge calls:      {total_judge_calls} ({fmt_seconds(total_judge_time)} logged judge time)")
    print(f"llm calls:        {total_llm_calls} ({fmt_seconds(total_llm_time)} logged llm time)")
    overhead = max(0.0, total_elapsed - total_judge_time - total_llm_time)
    print(f"solver/overhead:  {fmt_seconds(overhead)} approx")

    from collections import Counter
    by_verdict = Counter(str(r.get("verdict", "?")) for r in rows)
    by_candidate = Counter(solved_candidate(r) or "?" for r in solved)
    by_last_stage_unsolved = Counter((stages(r)[-1] if stages(r) else "?") for r in unsolved)

    print("\n=== Solved by candidate/stage ===")
    for k, v in by_candidate.most_common(20):
        print(f"{v:5d}  {k}")

    if unsolved:
        print("\n=== Unsolved last observed stage ===")
        for k, v in by_last_stage_unsolved.most_common(20):
            print(f"{v:5d}  {k}")

    print("\n=== Verdict counts, including unsolved/missing ===")
    for k, v in by_verdict.most_common():
        print(f"{v:5d}  {k}")


def sorted_rows(rows: list[dict[str, Any]], sort_by: str) -> list[dict[str, Any]]:
    if sort_by == "time_desc":
        return sorted(rows, key=lambda r: safe_float(r.get("elapsed_seconds")), reverse=True)
    if sort_by == "time_asc":
        return sorted(rows, key=lambda r: safe_float(r.get("elapsed_seconds")))
    if sort_by == "judge_calls_desc":
        return sorted(rows, key=lambda r: safe_int(r.get("judge_calls")), reverse=True)
    if sort_by == "llm_calls_desc":
        return sorted(rows, key=lambda r: safe_int(r.get("llm_calls")), reverse=True)
    return sorted(rows, key=lambda r: str(r.get("id", "")))


def print_row(row: dict[str, Any], *, show_code: bool, show_log: bool, code_chars: int, log_chars: int) -> None:
    eq1, eq2 = problem_eqs(row)
    jid = row.get("id", "?")
    solved = bool(row.get("solved"))
    verdict = row.get("verdict", "?")
    et = safe_float(row.get("elapsed_seconds"))
    jt = judge_time(row)
    lt = llm_time(row)
    overhead = max(0.0, et - jt - lt)
    print("\n" + "=" * 88)
    print(f"{jid}  eq1={row.get('eq1_id', '?')}  eq2={row.get('eq2_id', '?')}")
    print(f"solved={solved}  verdict={verdict}  elapsed={fmt_seconds(et)}  judge={fmt_seconds(jt)}  llm={fmt_seconds(lt)}  overhead={fmt_seconds(overhead)}")
    print(f"calls: judge={row.get('judge_calls', 0)}  llm={row.get('llm_calls', 0)}")
    cand = solved_candidate(row)
    if cand:
        print(f"solved-candidate/stage: {cand}")
    st = stages(row)
    if st:
        print(f"stages: {' -> '.join(st)}")
    if eq1:
        print(f"Eq1: {eq1}")
    if eq2:
        print(f"Eq2: {eq2}")

    judges = log_entries(row, "judge")
    if judges:
        print("judge responses:")
        for i, e in enumerate(judges, 1):
            resp = e.get("response") or {}
            status = resp.get("status", "?") if isinstance(resp, dict) else "?"
            msg = resp.get("message", "") if isinstance(resp, dict) else ""
            print(f"  {i}. status={status} elapsed={fmt_seconds(safe_float(e.get('elapsed')))} {msg}")

    if show_code:
        code = row.get("code") or ""
        if code:
            print("\n--- code ---")
            print(truncate(str(code), code_chars))

    if show_log:
        log = tail_text(row)
        if log:
            print("\n--- solver stderr tail ---")
            print(truncate(log, log_chars))


def export_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fields = [
        "id", "eq1_id", "eq2_id", "solved", "verdict", "elapsed_seconds",
        "judge_calls", "llm_calls", "judge_time", "llm_time", "overhead_time",
        "solved_candidate", "last_stage", "eq1", "eq2",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            eq1, eq2 = problem_eqs(r)
            et = safe_float(r.get("elapsed_seconds"))
            jt = judge_time(r)
            lt = llm_time(r)
            st = stages(r)
            w.writerow({
                "id": r.get("id", ""),
                "eq1_id": r.get("eq1_id", ""),
                "eq2_id": r.get("eq2_id", ""),
                "solved": bool(r.get("solved")),
                "verdict": r.get("verdict", ""),
                "elapsed_seconds": et,
                "judge_calls": safe_int(r.get("judge_calls")),
                "llm_calls": safe_int(r.get("llm_calls")),
                "judge_time": jt,
                "llm_time": lt,
                "overhead_time": max(0.0, et - jt - lt),
                "solved_candidate": solved_candidate(r) or "",
                "last_stage": st[-1] if st else "",
                "eq1": eq1 or "",
                "eq2": eq2 or "",
            })
    print(f"wrote {path}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Summarize and inspect SAIR results JSON/JSONL.")
    ap.add_argument("results", type=Path)
    ap.add_argument("--only", choices=["solved", "unsolved", "true", "false"], help="Filter examples to print.")
    ap.add_argument("--id", nargs="*", help="Print specific problem id(s).")
    ap.add_argument("--limit", type=int, default=0, help="Number of examples to print after filtering. 0 prints none unless --id is used.")
    ap.add_argument("--sort", choices=["id", "time_desc", "time_asc", "judge_calls_desc", "llm_calls_desc"], default="id")
    ap.add_argument("--show-code", action="store_true")
    ap.add_argument("--show-log", action="store_true")
    ap.add_argument("--code-chars", type=int, default=4000)
    ap.add_argument("--log-chars", type=int, default=4000)
    ap.add_argument("--export-csv", type=Path)
    args = ap.parse_args()

    rows = load_rows(args.results)
    print_summary(rows)

    if args.export_csv:
        export_csv(rows, args.export_csv)

    selected = rows
    if args.id:
        wanted = set(args.id)
        selected = [r for r in rows if str(r.get("id")) in wanted]
    elif args.only == "solved":
        selected = [r for r in rows if bool(r.get("solved"))]
    elif args.only == "unsolved":
        selected = [r for r in rows if not bool(r.get("solved"))]
    elif args.only == "true":
        selected = [r for r in rows if bool(r.get("solved")) and r.get("verdict") == "true"]
    elif args.only == "false":
        selected = [r for r in rows if bool(r.get("solved")) and r.get("verdict") == "false"]

    selected = sorted_rows(selected, args.sort)
    if not args.id and args.limit > 0:
        selected = selected[: args.limit]
    elif not args.id and args.limit == 0:
        selected = []

    for row in selected:
        print_row(row, show_code=args.show_code, show_log=args.show_log, code_chars=args.code_chars, log_chars=args.log_chars)


if __name__ == "__main__":
    main()
