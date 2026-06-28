#!/usr/bin/env python3
"""Join ATP baselines + our two runs into the per-problem solved-by matrix.

Inputs (per problem set):
  --problems      paper/problems/<set>.jsonl   (gold + eq ids)
  --baselines     paper/results/baselines_<set>.jsonl   (run_baselines.py)
  --ours-nollm    paper/results/ours_nollm_<set>.json   (run_ours.py)
  --ours-llm      paper/results/ours_llm_<set>.json      (run_ours.py)

Output: solved_by_matrix CSV with one row per problem. A method "solves" an
instance iff it returns a definitive verdict equal to the gold answer (sound
tools never disagree with gold; we score against it so a spurious verdict can't
inflate coverage). classical_vbs = OR over {vampire, eprover, prover9, mace4}.

uniquely_solved_by_llm = ours_llm & ours_used_llm & judge_ok
                         & ~classical_vbs & ~ours_nollm
That column is the paper's headline result.

Usage:
  python build_matrix.py --set hard3 --results-dir paper/results \
      --problems paper/problems/hard3.jsonl --out paper/results/solved_by_matrix_hard3.csv
"""
from __future__ import annotations
import argparse, csv, json, os
from collections import defaultdict

CLASSICAL = ["vampire", "eprover", "prover9", "mace4"]
# baselines.jsonl tool keys -> matrix column (vampire prove+fmb collapse to one)
TOOLKEY_TO_COL = {"vampire": "vampire", "vampire_fmb": "vampire",
                  "eprover": "eprover", "prover9": "prover9", "mace4": "mace4"}


def _gold_str(g):
    return "true" if g in (True, "true", "True") else "false"


def load_jsonl(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def load_json(path):
    if not path or not os.path.exists(path):
        return []
    raw = open(path, encoding="utf-8").read().strip()
    return json.loads(raw) if raw else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problems", required=True)
    ap.add_argument("--baselines", required=True)
    ap.add_argument("--ours-nollm", required=True)
    ap.add_argument("--ours-llm", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    problems = load_jsonl(args.problems)
    gold = {p["id"]: _gold_str(p["answer"]) for p in problems}
    meta = {p["id"]: (p["eq1_id"], p["eq2_id"]) for p in problems}

    # baselines: best (correct) verdict per (id, column)
    base = defaultdict(dict)  # id -> col -> "true"/"false"/None
    for r in load_jsonl(args.baselines):
        col = TOOLKEY_TO_COL.get(r["tool"], r["tool"])
        v = r.get("verdict")
        if v:  # keep first definitive verdict for that column
            base[r["id"]].setdefault(col, v)

    nollm = {r["id"]: r for r in load_json(args.ours_nollm)}
    llm = {r["id"]: r for r in load_json(args.ours_llm)}

    rows = []
    for pid in gold:
        g = gold[pid]
        cells = {}
        for col in CLASSICAL:
            v = base.get(pid, {}).get(col)
            cells[col] = v if v else ""
        classical_vbs = any(cells[c] == g for c in CLASSICAL)

        rn = nollm.get(pid, {})
        rl = llm.get(pid, {})
        ours_nollm = bool(rn.get("solved")) and rn.get("verdict") == g
        ours_llm = bool(rl.get("solved")) and rl.get("verdict") == g
        used_llm = bool(rl.get("used_llm"))
        judge_ok = bool(rl.get("solved"))  # in the harness, solved => judge-accepted
        unique = ours_llm and used_llm and judge_ok and not classical_vbs and not ours_nollm

        rows.append(dict(
            id=pid, eq1_id=meta[pid][0], eq2_id=meta[pid][1], gold=g,
            vampire=cells["vampire"], eprover=cells["eprover"],
            prover9=cells["prover9"], mace4=cells["mace4"],
            classical_vbs=int(classical_vbs),
            ours_nollm=int(ours_nollm), ours_llm=int(ours_llm),
            ours_solved_by=rl.get("solved_by") or "",
            ours_used_llm=int(used_llm), judge_ok=int(judge_ok),
            uniquely_solved_by_llm=int(unique),
        ))

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    cols = ["id", "eq1_id", "eq2_id", "gold", "vampire", "eprover", "prover9",
            "mace4", "classical_vbs", "ours_nollm", "ours_llm", "ours_solved_by",
            "ours_used_llm", "judge_ok", "uniquely_solved_by_llm"]
    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    uniq = sum(r["uniquely_solved_by_llm"] for r in rows)
    print(f"wrote {len(rows)} rows -> {args.out}  (uniquely-solved-by-LLM: {uniq})")


if __name__ == "__main__":
    main()
