#!/usr/bin/env python3
"""Finite-model-order probe + finder-reach triage for a target set.

The harvest recorded only `vampire_fmb: True/False` -- it threw away the ORDER of
the model Vampire found. For the step-0 miss-set (pairs a strong unconstrained
finder missed but fmb proved a model exists) that order is the number that gates
everything downstream:

  * If the model order n <= the finder's searched range, our deterministic finder
    SHOULD have found it and didn't -> a bug / encoding gap / timeout to fix,
    and a red flag on the A/B control arm (a "beyond-frontier" pair that isn't).
  * If n > the searched range, the miss is STRUCTURAL: the finder never looked
    there. The pair is a legitimate frontier target, and a SAT/CP finisher must
    run at that n (or the LLM must name a structure realizable at small n).

This script re-runs Vampire fmb on each pair, parses the model's domain order,
DUMPS the raw model (so a solve is auditable / reusable as a certificate seed),
and classifies each pair against the finder ranges you actually ran.

Reaches: mf2 searched Fin 4-11, SAT searched Fin 5-8 (defaults; override to match
your step-0 budget). "within finder range" => REVIEW; "beyond" => frontier.

Usage:
  python paper/scripts/fmb_probe.py --pairs paper/problems/cap_frontier_misses.json \
      --out paper/results/fmb_probe_misses.jsonl --models-dir paper/results/fmb_models \
      --fmb-timeout 600 --vampire paper/bin/vampire --mf2-max 11 --sat-min 5 --sat-max 8
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms  # noqa: E402


def load_pairs(path):
    """JSON dict {pid:[eq1,eq2]} or JSONL {id,equation1,equation2}."""
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


def parse_fmb_order(out):
    """Extract the finite-model domain order from Vampire fmb output.

    Robust to version differences: try (1) the cardinality axiom
    '! [X] : (X = a | X = b | ...)' alt-count, (2) count of domain-element type
    declarations of sort $i, (3) distinct element-constant tokens. Returns an int
    or None (None => keep the raw dump for manual inspection)."""
    block = out
    m = re.search(r"SZS output start\s+FiniteModel(.*?)SZS output end", out, re.S)
    if m:
        block = m.group(1)
    # (1) domain cardinality axiom: the widest "X = a | X = b | ..." disjunction.
    best = 0
    for clause in re.findall(r"!\s*\[[^\]]*\]\s*:\s*\((.*?)\)", block, re.S):
        alts = re.findall(r"=\s*[\w$']+", clause)
        best = max(best, len(alts))
    if best:
        return best
    # (2) element type declarations: 'tff(...,type, <name> : $i).'
    decls = re.findall(r"type,\s*([\w$']+)\s*:\s*\$i\b", block)
    if decls:
        return len(set(decls))
    # (3) distinct fmb element tokens.
    toks = set(re.findall(r"fmb_\$i_\d+", block)) or set(re.findall(r"\be\d+\b", block))
    return len(toks) or None


def run_fmb(eq1, eq2, timeout, vbin):
    """Run Vampire fmb; return (found_bool, order_or_None, raw_output, secs)."""
    t0 = time.time()
    body = etp_terms.tptp_false(eq1, eq2)
    with tempfile.TemporaryDirectory() as wd:
        path = os.path.join(wd, "prob.p")
        open(path, "w").write(body)
        try:
            p = subprocess.run(
                [vbin, "-sa", "fmb", "-t", f"{timeout}s", path],
                capture_output=True, text=True, timeout=timeout + 5)
            s = p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            return False, None, "TIMEOUT", round(time.time() - t0, 1)
    found = ("SZS status Satisfiable" in s or "SZS status CounterSatisfiable" in s
             or "Exiting with 1 model" in s or "interpretation(" in s
             or "Finite Model Found" in s)
    order = parse_fmb_order(s) if found else None
    return found, order, s, round(time.time() - t0, 1)


def triage(found, order, mf2_max, sat_min, sat_max):
    if not found:
        return "NO_MODEL (fmb did not reproduce a model at this budget -- re-check)"
    if order is None:
        return "MODEL_FOUND_ORDER_UNKNOWN (raw dump saved; parse manually)"
    if order <= mf2_max:
        return (f"REVIEW: order {order} <= mf2 range {mf2_max}; the finder should "
                f"have found this -> bug/encoding/timeout, and NOT a clean A/B target")
    return (f"FRONTIER: order {order} > finder ranges (mf2<= {mf2_max}, sat {sat_min}-"
            f"{sat_max}); structural miss -> legit target, finisher needs n={order}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--models-dir", default=None,
                    help="dir to dump each pair's raw fmb model (recommended)")
    ap.add_argument("--fmb-timeout", type=int, default=600)
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--mf2-max", type=int, default=11, help="max Fin mf2 searched")
    ap.add_argument("--sat-min", type=int, default=5)
    ap.add_argument("--sat-max", type=int, default=8)
    args = ap.parse_args()

    if args.models_dir:
        os.makedirs(args.models_dir, exist_ok=True)
    pairs = load_pairs(args.pairs)
    rows = []
    counts = {"FRONTIER": 0, "REVIEW": 0, "NO_MODEL": 0, "MODEL_FOUND_ORDER_UNKNOWN": 0}
    print(f"{'pair':<20} {'fmb':<6} {'order':<6} triage")
    print("-" * 78)
    for pid, eq1, eq2 in pairs:
        found, order, raw, secs = run_fmb(eq1, eq2, args.fmb_timeout, args.vampire)
        verdict = triage(found, order, args.mf2_max, args.sat_min, args.sat_max)
        key = verdict.split()[0].rstrip(":")
        counts[key] = counts.get(key, 0) + 1
        if args.models_dir and found:
            with open(os.path.join(args.models_dir, pid + ".fmb.txt"), "w") as f:
                f.write(raw)
        rows.append(dict(id=pid, fmb_found=found, model_order=order,
                         fmb_secs=secs, verdict=verdict))
        print(f"{pid:<20} {('YES' if found else 'no'):<6} {str(order):<6} {verdict}")
        with open(args.out, "w") as f:  # stream so an interrupted probe is not lost
            for r in rows:
                f.write(json.dumps(r) + "\n")
    print("-" * 78)
    print("FRONTIER(legit): %d | REVIEW(finder-should-have): %d | NO_MODEL: %d | ORDER_UNKNOWN: %d"
          % (counts.get("FRONTIER", 0), counts.get("REVIEW", 0),
             counts.get("NO_MODEL", 0), counts.get("MODEL_FOUND_ORDER_UNKNOWN", 0)))
    print(f"wrote {len(rows)} rows -> {args.out}"
          + (f"; models -> {args.models_dir}" if args.models_dir else ""))


if __name__ == "__main__":
    main()
