#!/usr/bin/env python3
"""llm_construct_ladder.py — SUPPORT-THRESHOLD eval for the construction (Austin) side.

Parallel to llm_trivial_ladder.py, cost-efficient. On AUSTIN_PROVEN laws (Vampire's saturation
gives a ground-truth presentation E), record the lowest rung at which the model proposes an E
that CERTIFIES (llm_construct.certify: E⊢law + E∪{a≠b} saturates).

Coarse rungs (≤7):  naked | strategy | +injective S | +25% eqns | +50% | +75% | +100%.
The support material is generated automatically (construct_hints). Reveal rungs exist only for
laws with a finite saturation (AUSTIN_PROVEN); the open frontier has just naked/strategy.

COST: top rung (all equations) is echo-certifiable, so we test it first — if it FAILS the model
is FORMAT-bound (can't even manipulate a near-complete E) → record "none", stop. Else
BINARY-SEARCH down for the threshold. One call per rung.

Threshold: certifies only at high reveal → CONSTRUCTION-bound (can complete, can't find);
fails even at full reveal → FORMAT-bound.

USAGE
  python3 paper/scripts/llm_construct_ladder.py --dry-run
  export OPENROUTER_API_KEY=...
  python3 paper/scripts/llm_construct_ladder.py --laws-file paper/results/eval/eval_solvable.jsonl \
      --vampire paper/bin/vampire --model openai/o4-mini --out paper/results/llm_construct_ladder.jsonl --n 15
"""
from __future__ import annotations
import argparse, glob, json, math, os, sys, time

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
    return (f"KEY: the subterm  S = {S}  is INJECTIVE in x, so it acts like a successor — this "
            "is exactly why no finite model exists and the model must be infinite. Your "
            "presentation should respect S being injective and not onto.")

def _eqs_text(eqs):
    lines = "\n".join(f"    ({i+1})  {e}" for i, e in enumerate(eqs))
    return ("KNOWN EQUATIONS of a valid presentation (each is a true consequence of the law; "
            "include them and complete the rest so an automated prover certifies E):\n" + lines)


def rungs_for(has_S, n_eqs):
    """(label, add_strategy, add_S, n_eqs_shown). Coarse, ≤7, deduped."""
    specs = [("L0 naked", False, False, 0), ("L1 strategy", True, False, 0)]
    seen = {(False, False, 0), (True, False, 0)}
    if has_S:
        specs.append(("+injective S", True, True, 0)); seen.add((True, True, 0))
    for f in (0.25, 0.5, 0.75, 1.0):
        k = math.ceil(f * n_eqs)
        key = (True, has_S, k)
        if k > 0 and key not in seen:
            seen.add(key); specs.append((f"+{int(f*100)}% eqns", True, has_S, k))
    return specs


def build_prompt(law, add_strategy, add_S, k_eqs, S, eqs, feedback=None):
    base = C.build_prompt(law, feedback)
    parts = []
    if add_strategy:
        parts.append(STRATEGY)
    if add_S and S:
        parts.append(_S_text(S))
    if k_eqs > 0:
        parts.append(_eqs_text(eqs[:k_eqs]))
    return base + ("\n\n" + "\n\n".join(parts) if parts else "")


def attempt_ladder(law, vbin, api_key, model, effort, timeout):
    eqs = H.equations(law)
    S = H.injective_subterm(law)
    rungs = rungs_for(bool(S), len(eqs))
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    tried = {}

    def run(idx):
        if idx in tried:
            return tried[idx]
        _, strat, useS, k = rungs[idx]
        try:
            content, u = L.call_llm(build_prompt(law, strat, useS, k, S, eqs),
                                    api_key, model, effort, timeout=300)
        except Exception:                                 # noqa: BLE001
            tried[idx] = False; return False
        for kk in usage:
            usage[kk] += (u.get(kk) or 0)
        E, _ = C.parse_E(content)
        if E is None:
            tried[idx] = False; return False
        tried[idx] = bool(C.certify(law, E, vbin, timeout)["certified"])
        return tried[idx]

    top = len(rungs) - 1
    result = {"n_eqs": len(eqs), "has_S": bool(S), "rungs": [r[0] for r in rungs]}
    if not run(top):                                      # top fails → format-bound
        result.update({"threshold": None, "threshold_rung": None,
                       "tried": {rungs[i][0]: tried[i] for i in tried}, "usage": usage})
        return result
    lo, hi = 0, top
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
    law = "x = ((((y ◇ y) ◇ z) ◇ x) ◇ x) ◇ z"
    eqs = H.equations(law); S = H.injective_subterm(law)
    rungs = rungs_for(bool(S), len(eqs))
    print(f"LAW: {law}\ninjective S: {S}\nsaturated eqns: {len(eqs)}  ->  {len(rungs)} rungs: "
          f"{[r[0] for r in rungs]}")
    print("Cost: top (all eqns) is echo-certifiable, so it usually passes; then ~log2(rungs) "
          "calls to find the threshold. 'none' only if the model can't even format E.")
    for lbl, strat, useS, k in rungs:
        p = build_prompt(law, strat, useS, k, S, eqs)
        print(f"  {lbl:14} strategy={strat} S={useS} eqns_shown={k}  prompt={len(p)} chars")


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
    print(f"{len(laws)} austin law(s); model={a.model} [construction support ladder, cost-efficient]",
          file=sys.stderr)
    ths = []
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt_ladder(law, a.vampire, api_key, a.model, a.reasoning_effort, a.timeout)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            th = res["threshold_rung"]; ths.append(th)
            print(f"[{i}/{len(laws)}] threshold={th or 'none':14} ({len(res['tried'])} call(s), "
                  f"{res['secs']}s)  {law[:40]}", file=sys.stderr)
    solved = [t for t in ths if t]
    print(f"done: {len(solved)}/{len(ths)} certified at some rung; thresholds={solved} -> {a.out}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
