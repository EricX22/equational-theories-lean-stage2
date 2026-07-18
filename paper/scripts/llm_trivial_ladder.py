#!/usr/bin/env python3
"""llm_trivial_ladder.py — the SUPPORT-THRESHOLD eval for the trivial side.

Naked runs read ~0 on the order-≥5 corpus (min ~10-step collapses), which is expected but
does not discriminate. The informative measurement is: HOW MUCH SUPPORT does a model need
before it makes progress? We climb a support ladder per law and record the lowest rung the
model solves — a gradient that works even when the naked run is 0, and that says how far a
model is from solving unaided.

The support dial is Vampire's own proof: the derived equalities the collapse passes through
(trivial_hints.lemmas) are revealed one at a time as waypoints.

    L0  naked           law only (format + worked example)
    L1  +strategy       the verbal collapse mechanism (superpose law w/ itself -> op(x,y)=z -> x=y)
    L2  +waypoint 1     reveal the first derived lemma
    L3  +waypoints 1-2  reveal two
    ... up to ...
    Lk  +all waypoints  the full path is given; the model only has to formalize it

Report: per law, the threshold rung (or "none"); aggregate = the support profile of the model.
All hints are SOUND — they are consequences of the law the model still has to prove in Lean;
they guide the search, they are not injected as axioms.

USAGE
  python3 paper/scripts/llm_trivial_ladder.py --dry-run                 # inspect the ladder
  export OPENROUTER_API_KEY=...
  python3 paper/scripts/llm_trivial_ladder.py --laws-file paper/results/final_status.jsonl \
      --model openai/o4-mini --lean-dir . --out paper/results/llm_ladder.jsonl --n 15
"""
from __future__ import annotations
import argparse, glob, json, os, sys, tempfile, time

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


def build_prompt(law, header, level, waypoints, feedback=None):
    base = T.build_prompt(law, header, feedback)          # naked (format + worked example)
    if level == 0:
        return base
    add = "\n\n" + STRATEGY
    if level >= 2:
        shown = waypoints[: level - 1]
        lines = "\n".join(f"    ({i+1})  {w}" for i, w in enumerate(shown))
        add += ("\n\nKNOWN CONSEQUENCES OF THE LAW (each is derivable from it; you must still "
                "prove them in Lean, but they are the waypoints your proof should pass through, "
                "in order):\n" + lines)
    return base + add


def attempt_ladder(law, lean_dir, rounds, api_key, model, effort, timeout):
    header = asp.problem_header(law)
    waypoints = H.lemmas(law)
    max_level = 1 + len(waypoints)                        # 0=naked,1=strategy,2..=+k waypoints
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    per_level = []
    for level in range(0, max_level + 1):
        feedback = None
        solved = False
        for rnd in range(1, rounds + 1):
            try:
                content, u = L.call_llm(build_prompt(law, header, level, waypoints, feedback),
                                        api_key, model, effort, timeout)
            except Exception as e:                        # noqa: BLE001
                per_level.append({"level": level, "error": f"api: {e}"}); break
            for k in usage:
                usage[k] += (u.get(k) or 0)
            body = L.extract_lean(content)
            if L.detect_side(body) != "trivial":
                feedback = "Your `solution` must target `Problem.TrivialGoal`."
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, encoding="utf-8") as fh:
                fh.write(body); path = fh.name
            passed, rej = asp.judge(law, "trivial", path, lean_dir, timeout)
            os.unlink(path)
            per_level.append({"level": level, "solved": passed, "rounds": rnd})
            if passed:
                solved = True; break
            feedback = "\n".join(rej[:6])
        if solved:
            return {"threshold": level, "n_waypoints": len(waypoints),
                    "per_level": per_level, "usage": usage}
    return {"threshold": None, "n_waypoints": len(waypoints),
            "per_level": per_level, "usage": usage}


def dry_run():
    law = "x = ((((y ◇ w) ◇ z) ◇ ((y ◇ x) ◇ y)) ◇ y)"
    header = asp.problem_header(law)
    wp = H.lemmas(law)
    print(f"LAW: {law}\nwaypoints ({len(wp)}):")
    for w in wp:
        print("   ", w)
    for level in range(0, 2 + len(wp)):
        p = build_prompt(law, header, level, wp)
        tag = {0: "L0 naked", 1: "L1 +strategy"}.get(level, f"L{level} +{level-1} waypoint(s)")
        print(f"\n{'='*70}\n{tag}  (prompt {len(p)} chars) — support tail:")
        # show only the appended support section
        cut = p.find("STRATEGY (how these")
        print(p[cut:] if cut > -1 else "(naked — no support appended)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--laws-file")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=2)
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
    print(f"{len(laws)} trivial law(s); model={a.model} [support-threshold ladder]", file=sys.stderr)
    thresholds = []
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt_ladder(law, a.lean_dir, a.rounds, api_key, a.model,
                                 a.reasoning_effort, a.timeout)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            th = res["threshold"]
            thresholds.append(th)
            print(f"[{i}/{len(laws)}] threshold={'none' if th is None else 'L'+str(th)} "
                  f"(of L{1+res['n_waypoints']})  {res['secs']}s  {law[:44]}", file=sys.stderr)
    solved = [t for t in thresholds if t is not None]
    print(f"done: {len(solved)}/{len(thresholds)} reached some support level; "
          f"thresholds={sorted(solved)} -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
