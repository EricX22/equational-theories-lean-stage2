#!/usr/bin/env python3
"""llm_construct_ladder.py — SUPPORT-THRESHOLD eval for the construction (Austin) side.

Parallel to llm_trivial_ladder.py. On AUSTIN_PROVEN laws (where Vampire's saturation gives a
ground-truth presentation `E`), climb a support ladder and record the lowest rung at which
the model proposes an `E` that CERTIFIES (llm_construct.certify: E⊢law + E∪{a≠b} saturates).

    L0  naked            propose E from the law alone
    L1  +strategy        aim for a completed presentation (entails law, keeps 2 elements)
    L2  +injective S     reveal the (i)-cert subterm — the successor-like map forcing infinity
    L3..  +k equations   reveal k saturated equations (simplest first); model completes the rest

Threshold interpretation (dual diagnostic):
  certifies only at high reveal  -> CONSTRUCTION-bound (can complete, can't find the presentation)
  fails even at full reveal      -> FORMAT-bound (can't manipulate a near-complete E into one that certifies)

Support material is generated automatically (construct_hints). The reveal rungs exist ONLY for
laws with a finite saturation (AUSTIN_PROVEN); the open frontier (NO_FINITE_MODEL) has just
L0/L1 and should be measured separately.

USAGE
  python3 paper/scripts/llm_construct_ladder.py --dry-run
  export OPENROUTER_API_KEY=...
  python3 paper/scripts/llm_construct_ladder.py --laws-file paper/results/eval/eval_solvable.jsonl \
      --vampire paper/bin/vampire --model openai/o4-mini --out paper/results/llm_construct_ladder.jsonl --n 15
"""
from __future__ import annotations
import argparse, glob, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import llm_solve as L
import llm_construct as C
import construct_hints as H

STRATEGY = """STRATEGY: think of `E` as the completed rewrite system a Knuth-Bendix procedure
would converge to — a handful of equations that (a) entail the law and (b) keep two elements
distinct (do not force `x=y`). Orient the law's critical pairs; add the consequences needed to
close them."""

def _S_text(S):
    return (f"KEY: the subterm  S = {S}  is INJECTIVE in x (a left-inverse exists), so it acts "
            "like a successor — this is exactly why no finite model exists and the model must be "
            "infinite. Your presentation should respect S being injective and not onto.")

def _eqs_text(eqs):
    lines = "\n".join(f"    ({i+1})  {e}" for i, e in enumerate(eqs))
    return ("KNOWN EQUATIONS of a valid presentation (each is a true consequence of the law; "
            "include them and complete the rest so an automated prover certifies E):\n" + lines)


def build_prompt(law, level, S, eqs, feedback=None):
    base = C.build_prompt(law, feedback)
    parts = []
    if level >= 1:
        parts.append(STRATEGY)
    n_struct = 1 + (1 if S else 0)
    if S and level >= 2:
        parts.append(_S_text(S))
    k = max(0, level - n_struct)
    if k > 0:
        parts.append(_eqs_text(eqs[:k]))
    return base + ("\n\n" + "\n\n".join(parts) if parts else "")


def max_level(S, eqs):
    return (1 + (1 if S else 0)) + len(eqs)


def attempt_ladder(law, vbin, rounds, api_key, model, effort, timeout):
    eqs = H.equations(law)
    S = H.injective_subterm(law)
    top = max_level(S, eqs)
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    per_level = []
    for level in range(0, top + 1):
        feedback = None
        solved = False
        for rnd in range(1, rounds + 1):
            try:
                content, u = L.call_llm(build_prompt(law, level, S, eqs, feedback),
                                        api_key, model, effort, timeout=300)
            except Exception as e:                            # noqa: BLE001
                per_level.append({"level": level, "error": f"api: {e}"}); break
            for kk in usage:
                usage[kk] += (u.get(kk) or 0)
            E, why = C.parse_E(content)
            if E is None:
                feedback = why
                continue
            res = C.certify(law, E, vbin, timeout)
            per_level.append({"level": level, "certified": res["certified"], "rounds": rnd,
                              "corr": res["corr_theorem"], "nonvac": res["nonvac_satisfiable"]})
            if res["certified"]:
                solved = True; break
            feedback = f"correctness={res['corr_theorem']}, nonvacuity={res['nonvac_satisfiable']}"
        if solved:
            return {"threshold": level, "n_eqs": len(eqs), "has_S": bool(S),
                    "per_level": per_level, "usage": usage}
    return {"threshold": None, "n_eqs": len(eqs), "has_S": bool(S),
            "per_level": per_level, "usage": usage}


def dry_run():
    law = "x = ((((y ◇ y) ◇ z) ◇ x) ◇ x) ◇ z"
    eqs = H.equations(law); S = H.injective_subterm(law)
    print(f"LAW: {law}\ninjective S: {S}\nsaturated eqns: {len(eqs)}  -> ladder height L{max_level(S,eqs)}")
    for level in range(0, max_level(S, eqs) + 1):
        p = build_prompt(law, level, S, eqs)
        cut = p.find("STRATEGY:")
        tail = p[cut:] if cut > -1 else "(naked — no support appended)"
        print(f"\n{'='*70}\nL{level}  ({len(p)} chars):\n{tail}")


def load_austin(pattern):
    laws = []
    for fn in glob.glob(pattern):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("gold") == "austin" or r.get("status") == "AUSTIN_PROVEN":
                laws.append(r["law"])
    return sorted(set(laws))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--vampire", default="paper/bin/vampire")
    ap.add_argument("--laws-file")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--model", default="openai/o4-mini")
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.dry_run:
        dry_run(); return
    if not a.laws_file or not a.out:
        ap.error("--laws-file and --out required unless --dry-run")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    laws = load_austin(a.laws_file)
    if a.n:
        laws = laws[:a.n]
    print(f"{len(laws)} austin law(s); model={a.model} [construction support ladder]", file=sys.stderr)
    thresholds = []
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt_ladder(law, a.vampire, a.rounds, api_key, a.model, a.reasoning_effort, a.timeout)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            th = res["threshold"]; thresholds.append(th)
            print(f"[{i}/{len(laws)}] threshold={'none' if th is None else 'L'+str(th)} "
                  f"(of L{max_level(bool(res['has_S']) and 'S', [0]*res['n_eqs'])})  "
                  f"{res['secs']}s  {law[:42]}", file=sys.stderr)
    solved = [t for t in thresholds if t is not None]
    print(f"done: {len(solved)}/{len(thresholds)} reached some level; thresholds={sorted(solved)} "
          f"-> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
