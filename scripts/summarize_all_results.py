#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path


DATASET_TO_PROBLEM_FILE = {
    "normal": "normal.jsonl",
    "hard1": "hard1.jsonl",
    "hard2": "hard2.jsonl",
    "hard3": "hard3.jsonl",
    "sample_20": "sample_20.json",
    "sample_200": "sample_200.json",
}


def load_json_or_jsonl(path: Path):
    text = path.read_text().strip()
    if not text:
        return []

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            if isinstance(data.get("results"), list):
                return data["results"]
            return [data]
    except json.JSONDecodeError:
        pass

    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def infer_dataset(path: Path, rows):
    for r in rows:
        pid = str(r.get("id") or r.get("problem_id") or "")
        if pid.startswith("normal_"):
            return "normal"
        if pid.startswith("hard1_"):
            return "hard1"
        if pid.startswith("hard2_"):
            return "hard2"
        if pid.startswith("hard3_"):
            return "hard3"

    name = path.stem.lower()
    if "hard3" in name:
        return "hard3"
    if "hard2" in name:
        return "hard2"
    if "hard1" in name or "hard" in name:
        return "hard1"
    if "sample_20" in name or "baseline" in name:
        return "sample_20"
    if "sample_200" in name:
        return "sample_200"
    if "normal" in name or "my_solver" in name:
        return "normal"
    return "unknown"


def row_id(row):
    return row.get("id") or row.get("problem_id")


def is_solved(row):
    if row.get("solved") is True:
        return True
    if row.get("status") == "accepted":
        return True
    if row.get("verdict") in {"true", "false"} and row.get("code"):
        return True
    return False


def gold_answer(row):
    ans = row.get("answer")
    if isinstance(ans, bool):
        return ans
    if isinstance(ans, str):
        if ans.lower() == "true":
            return True
        if ans.lower() == "false":
            return False
    return None


def load_gold_map(problems_dir: Path, dataset: str):
    fname = DATASET_TO_PROBLEM_FILE.get(dataset)
    if not fname:
        return {}

    path = problems_dir / fname
    if not path.exists():
        return {}

    rows = load_json_or_jsonl(path)
    return {row["id"]: row for row in rows if "id" in row}


def summarize_file(path: Path, problems_dir: Path):
    rows = load_json_or_jsonl(path)
    ds = infer_dataset(path, rows)
    gold = load_gold_map(problems_dir, ds)

    c = Counter()
    stage_counts = Counter()

    for r in rows:
        pid = row_id(r)
        g = gold.get(pid, {})
        ans = gold_answer(g) if g else gold_answer(r)

        solved = is_solved(r)
        verdict = r.get("verdict")

        c["rows"] += 1
        c["solved"] += int(solved)
        c["unsolved"] += int(not solved)

        if verdict == "true":
            c["verdict_true"] += 1
        elif verdict == "false":
            c["verdict_false"] += 1
        else:
            c["verdict_missing"] += 1

        if ans is True:
            c["gold_true"] += 1
            if solved:
                c["solved_gold_true"] += 1
            else:
                c["unsolved_gold_true"] += 1
        elif ans is False:
            c["gold_false"] += 1
            if solved:
                c["solved_gold_false"] += 1
            else:
                c["unsolved_gold_false"] += 1
        else:
            c["gold_unknown"] += 1

        if solved and ans is not None and verdict in {"true", "false"}:
            pred = verdict == "true"
            if pred == ans:
                c["correct"] += 1
            else:
                c["wrong"] += 1

        stage = r.get("candidate") or r.get("stage") or r.get("solved_by")
        if solved and stage:
            stage_counts[str(stage)] += 1

    return ds, path, c, stage_counts


def pct(a, b):
    return 100.0 * a / b if b else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", default="pipeline/results")
    ap.add_argument("--problems-dir", default="examples/problems")
    ap.add_argument("--pattern", default="*.json*")
    ap.add_argument("--stages", action="store_true")
    args = ap.parse_args()

    results_dir = Path(args.results_dir)
    problems_dir = Path(args.problems_dir)

    files = sorted(p for p in results_dir.glob(args.pattern) if p.is_file())
    if not files:
        raise SystemExit(f"No result files found in {results_dir}")

    print("\n=== Per result file ===")
    print(
        f"{'file':45} {'dataset':8} {'solved':14} "
        f"{'missing T':10} {'missing F':10} {'wrong':7} "
        f"{'true solved':12} {'false solved':12}"
    )
    print("-" * 130)

    for path in files:
        try:
            ds, path, c, stage_counts = summarize_file(path, problems_dir)
        except Exception as e:
            print(f"[skip] {path}: {e}")
            continue

        solved = c["solved"]
        rows = c["rows"]

        print(
            f"{str(path):45} {ds:8} "
            f"{solved:4}/{rows:<4} {pct(solved, rows):5.1f}% "
            f"{c['unsolved_gold_true']:10} "
            f"{c['unsolved_gold_false']:10} "
            f"{c['wrong']:7} "
            f"{c['solved_gold_true']:4}/{c['gold_true']:<4} "
            f"{c['solved_gold_false']:4}/{c['gold_false']:<4}"
        )

        if c["gold_unknown"]:
            print(f"  warning: {c['gold_unknown']} rows had no gold answer")

        if args.stages and stage_counts:
            for stage, n in stage_counts.most_common():
                print(f"  {n:4}  {stage}")


if __name__ == "__main__":
    main()