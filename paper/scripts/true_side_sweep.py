#!/usr/bin/env python3
"""Long-budget TRUE-side (and finite-model) sweep to classify open order-5 pairs.

The order-5 survivors are UNLABELED and genuinely open: "hard" only means our
40s screen resolved them in neither direction. Before asking the LLM to build a
countermodel, we must know each pair actually HAS one -- otherwise "o3 failed"
and "no countermodel exists (it's a theorem)" look identical.

For each pair this runs Vampire in two modes at a long budget:
  prove : is EQ1 -> EQ2 a THEOREM?  (EQ1 axiom, EQ2 conjecture; CASC mode)
  fmb   : does a FINITE countermodel exist?  (finite-model builder)

Classification:
  THEOREM        prove succeeds  -> DROP from the countermodel target set
  COUNTERMODEL   fmb finds one   -> valid FALSE target (also a deterministic solve!)
  OPEN           neither at this budget -> genuine open target for the proposer
  CONFLICT       both (should never happen; indicates an encoding bug)

Both outcomes other than OPEN shrink the LLM target set deterministically, which
is the goal: exhaust the deterministic side before spending on the model.

Usage:
  python paper/scripts/true_side_sweep.py --pairs paper/problems/survivors6.json \
      --prove-timeout 300 --fmb-timeout 300 --out paper/results/true_side_survivors.jsonl
  # sandbox: add --vampire paper/bin/vampire
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms  # noqa: E402


def load_pairs(path):
    """Accept either a JSON dict {pid: [eq1, eq2]} or JSONL {id, equation1, equation2}."""
    text = open(path).read()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return [(pid, eq[0], eq[1]) for pid, eq in obj.items()]
    except json.JSONDecodeError:
        pass
    rows = []
    for line in text.splitlines():
        if line.strip():
            r = json.loads(line)
            rows.append((r["id"], r["equation1"], r["equation2"]))
    return rows


def run_vampire(body, cmd_builder, timeout):
    with tempfile.TemporaryDirectory() as wd:
        path = os.path.join(wd, "prob.p")
        open(path, "w").write(body)
        try:
            p = subprocess.run(cmd_builder(path), capture_output=True, text=True,
                               timeout=timeout + 5)
            s = p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            s = "TIMEOUT"
        return s


def prove(eq1, eq2, timeout, vbin):
    t0 = time.time()
    s = run_vampire(etp_terms.tptp_true(eq1, eq2),
                    lambda f: [vbin, "--mode", "casc", "-t", f"{timeout}s", f], timeout)
    ok = ("SZS status Theorem" in s or "SZS status Unsatisfiable" in s
          or "Refutation found" in s)
    return ok, round(time.time() - t0, 1)


def fmb(eq1, eq2, timeout, vbin):
    t0 = time.time()
    s = run_vampire(etp_terms.tptp_false(eq1, eq2),
                    lambda f: [vbin, "-sa", "fmb", "-t", f"{timeout}s", f], timeout)
    ok = ("SZS status Satisfiable" in s or "SZS status CounterSatisfiable" in s
          or "Exiting with 1 model" in s or "interpretation(" in s)
    return ok, round(time.time() - t0, 1)


def classify(is_theorem, has_model):
    if is_theorem and has_model:
        return "CONFLICT"
    if is_theorem:
        return "THEOREM (drop -- no countermodel exists)"
    if has_model:
        return "COUNTERMODEL (valid target; deterministic solve)"
    return "OPEN (genuine proposer target)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prove-timeout", type=int, default=300)
    ap.add_argument("--fmb-timeout", type=int, default=300,
                    help="set 0 to skip the finite-model-builder pass")
    ap.add_argument("--vampire", default="vampire",
                    help="vampire binary (default 'vampire' on PATH; sandbox: paper/bin/vampire)")
    args = ap.parse_args()

    pairs = load_pairs(args.pairs)
    rows = []
    counts = {"THEOREM": 0, "COUNTERMODEL": 0, "OPEN": 0, "CONFLICT": 0}
    print(f"{'pair':<18} {'prove':<7} {'fmb':<7} classification")
    print("-" * 70)
    for pid, eq1, eq2 in pairs:
        thm, t_p = prove(eq1, eq2, args.prove_timeout, args.vampire)
        has_model, t_f = (False, 0.0)
        if args.fmb_timeout > 0:
            has_model, t_f = fmb(eq1, eq2, args.fmb_timeout, args.vampire)
        verdict = classify(thm, has_model)
        counts[verdict.split()[0]] += 1
        rows.append(dict(id=pid, is_theorem=thm, has_finite_model=has_model,
                         prove_time=t_p, fmb_time=t_f, verdict=verdict))
        print(f"{pid:<18} {('THM' if thm else '-'):<7} {('MODEL' if has_model else '-'):<7} {verdict}")
        with open(args.out, "w") as f:  # stream so an interrupted sweep is not lost
            for r in rows:
                f.write(json.dumps(r) + "\n")
    print("-" * 70)
    print("THEOREMs(drop): %d | COUNTERMODELs(solved): %d | OPEN(proposer): %d | CONFLICT: %d"
          % (counts["THEOREM"], counts["COUNTERMODEL"], counts["OPEN"], counts["CONFLICT"]))
    print(f"wrote {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
