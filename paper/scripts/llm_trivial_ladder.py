#!/usr/bin/env python3
"""llm_trivial_ladder.py — the SUPPORT-THRESHOLD eval for the trivial side (cost-efficient).

Naked runs read ~0 on the order-≥5 corpus (min ~10-step collapses), which is expected but
does not discriminate. The informative measurement is: HOW MUCH SUPPORT does a model need
before it makes progress? We record the lowest rung the model solves — a gradient that works
even when the naked run is 0, and disentangles search-bound (needs the path) from
formalization-bound (has the path, can't write the Lean).

The support dial is Vampire's own proof: the derived equalities the collapse passes through
(trivial_hints.lemmas) are revealed as waypoints. Rungs are COARSE (≤6 regardless of proof
length) so the ladder is cheap:

    naked | strategy | +25% waypoints | +50% | +75% | +100%

COST: we test the TOP rung first. If it fails, the model is formalization-bound → record
"none" and stop (1 call, not ~45). Only if the top solves do we BINARY-SEARCH down for the
threshold — O(log rungs) calls. One call per rung (no per-rung revision).

All hints are SOUND — consequences of the law the model still proves in Lean; they guide the
search, they are not axioms.

USAGE
  python3 paper/scripts/llm_trivial_ladder.py --dry-run
  export OPENROUTER_API_KEY=...
  python3 paper/scripts/llm_trivial_ladder.py --laws-file paper/results/final_status.jsonl \
      --model openai/o4-mini --lean-dir . --out paper/results/llm_ladder.jsonl --n 15
"""
from __future__ import annotations
import argparse, glob, json, math, os, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_spec as asp
import llm_solve as L
import llm_trivial as T
import trivial_hints as H

STRATEGY = """STRATEGY (how these laws collapse): superpose the law with itself — substitute
the whole right-hand side into one of its own variables — to derive simpler consequences,
until you reach one of the form `op(x, y) = z` (the operation returns any element). From
there every two elements are equal, giving `a = b`. Work toward that collapse."""


def rungs_for(n_wp):
    """Coarse support rungs: (label, add_strategy, n_waypoints_shown). ≤6, deduped."""
    specs = [("L0 naked", False, 0), ("L1 strategy", True, 0)]
    seen = {(False, 0), (True, 0)}
    for f in (0.25, 0.5, 0.75, 1.0):
        k = math.ceil(f * n_wp)
        if k > 0 and (True, k) not in seen:
            seen.add((True, k)); specs.append((f"+{int(f*100)}% wp", True, k))
    return specs


def build_prompt(law, header, add_strategy, k_wp, waypoints, feedback=None):
    base = T.build_prompt(law, header, feedback)          # naked (format + worked example)
    if not add_strategy:
        return base
    add = "\n\n" + STRATEGY
    if k_wp > 0:
        lines = "\n".join(f"    ({i+1})  {w}" for i, w in enumerate(waypoints[:k_wp]))
        add += ("\n\nKNOWN CONSEQUENCES OF THE LAW (each is derivable from it; you must still "
                "prove them in Lean, but they are the waypoints your proof should pass through, "
                "in order):\n" + lines)
    return base + add


def attempt_ladder(law, lean_dir, api_key, model, effort, timeout):
    header = asp.problem_header(law)
    waypoints = H.lemmas(law)
    rungs = rungs_for(len(waypoints))
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    tried = {}                                            # idx -> solved(bool)

    def run(idx):
        if idx in tried:
            return tried[idx]
        _, add_strat, k = rungs[idx]
        try:
            content, u = L.call_llm(build_prompt(law, header, add_strat, k, waypoints),
                                    api_key, model, effort, timeout)
        except Exception as e:                            # noqa: BLE001
            tried[idx] = False; return False
        for kk in usage:
            usage[kk] += (u.get(kk) or 0)
        body = L.extract_lean(content)
        if L.detect_side(body) != "trivial":
            tried[idx] = False; return False
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, encoding="utf-8") as fh:
            fh.write(body); path = fh.name
        passed, _ = asp.judge(law, "trivial", path, lean_dir, timeout)
        os.unlink(path)
        tried[idx] = bool(passed); return tried[idx]

    top = len(rungs) - 1
    result = {"n_waypoints": len(waypoints), "rungs": [r[0] for r in rungs]}
    if not run(top):                                      # top fails → formalization-bound
        result.update({"threshold": None, "threshold_rung": None,
                       "tried": {rungs[i][0]: tried[i] for i in tried}, "usage": usage})
        return result
    lo, hi = 0, top                                       # binary-search lowest solving rung
    while lo < hi:
        mid = (lo + hi) // 2
        if run(mid):
            hi = mid
        else:
            lo = mid + 1
    result.update({"threshold": lo, "threshold_rung": rungs[lo][0],
                   "tried": {rungs[i][0]: tried[i] for i in tried}, "usage": usage})
    return result


def dry_run():
    law = "x = ((((y ◇ w) ◇ z) ◇ ((y ◇ x) ◇ y)) ◇ y)"
    header = asp.problem_header(law)
    wp = H.lemmas(law)
    rungs = rungs_for(len(wp))
    print(f"LAW: {law}\nwaypoints: {len(wp)}  ->  {len(rungs)} rungs (coarse): "
          f"{[r[0] for r in rungs]}")
    print("Cost: 1 call if top fails; else 1 + ~log2(rungs) calls (was ~rungs×rounds).")
    for lbl, strat, k in rungs:
        p = build_prompt(law, header, strat, k, wp)
        print(f"  {lbl:14} strategy={strat} waypoints_shown={k}  prompt={len(p)} chars")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--laws-file")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--model", default="openai/o4-mini")
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--lean-dir", default=".")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.dry_run:
        dry_run(); return
    if not a.laws_file or not a.out:
        ap.error("--laws-file and --out required unless --dry-run")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    laws = T.load_trivial(a.laws_file)
    if a.n:
        laws = laws[:a.n]
    print(f"{len(laws)} trivial law(s); model={a.model} [support-threshold ladder, cost-efficient]",
          file=sys.stderr)
    ths = []
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt_ladder(law, a.lean_dir, api_key, a.model, a.reasoning_effort, a.timeout)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            th = res["threshold_rung"]; ths.append(th)
            calls = len(res["tried"])
            print(f"[{i}/{len(laws)}] threshold={th or 'none':12} ({calls} call(s), {res['secs']}s)  "
                  f"{law[:42]}", file=sys.stderr)
    solved = [t for t in ths if t]
    print(f"done: {len(solved)}/{len(ths)} solved at some rung; thresholds={solved} -> {a.out}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
