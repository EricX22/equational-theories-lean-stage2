#!/usr/bin/env python3
"""Heavy re-screen of order6_search's light-pass candidates.

The light pass (small SAT sizes, short fmb) over-counts: any law whose smallest
model is larger than the light screen reaches survives as a false candidate. This
re-runs the finite screen at HEAVY budget on just those survivors -- solver
mf2/SAT up to Fin~11 + a long Vampire fmb -- and keeps only laws that STILL show
no finite model. Reuses the same "satisfy L, break x=y == nontrivial model" trick.

Usage:
  python paper/scripts/order6_rescreen.py \
      --in 'paper/results/order6_candidates_*.jsonl' \
      --solver-dir scripts/my_solver_merged --vampire paper/bin/vampire \
      --mf2-budget 30 --sat-sizes 4,5,6,7,8,9,10,11 --fmb-timeout 300 \
      --out paper/results/order6_confirmed.jsonl --shard 0/8
"""
from __future__ import annotations
import argparse, glob, json, os, subprocess, sys, tempfile, time


def load_laws(patterns):
    seen, laws = set(), []
    for pat in patterns:
        for path in sorted(glob.glob(pat)):
            for line in open(path):
                line = line.strip()
                if not line:
                    continue
                law = json.loads(line).get("law")
                if law and law not in seen:
                    seen.add(law)
                    laws.append(law)
    return laws


def solver_has_finite_model(solver, law, mf2_budget, sat_sizes):
    eq2 = "x = y"
    try:
        if solver.mf2_find_portfolio(law, eq2, mf2_budget):
            return True
    except Exception:
        pass
    per = max(1.0, mf2_budget) / max(1, len(sat_sizes))
    for n in sat_sizes:
        try:
            if solver.sat_find_model(law, eq2, n, time.time() + per):
                return True
        except Exception:
            pass
    return False


def fmb_from_law(et, law, timeout, vbin):
    l, r, vs = et.tptp_eq_vars(law)
    body = (f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\n"
            "fof(nontrivial,axiom,?[U,V]:U!=V).\n")
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "p.p")
        open(p, "w").write(body)
        try:
            s = subprocess.run([vbin, "-sa", "fmb", "-t", f"{timeout}s", p],
                               capture_output=True, text=True, timeout=timeout + 5).stdout
        except subprocess.TimeoutExpired:
            return "NO_MODEL_IN_BUDGET"
    if "Finite Model Found" in s or "SZS status Satisfiable" in s:
        return "MODEL_FOUND"
    return "NO_MODEL_IN_BUDGET"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--solver-dir", default=None,
                    help="optional Fin<=11 solver pre-filter; omit for pure fmb "
                         "(the fmb pass upstream already ruled out small models)")
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--mf2-budget", type=float, default=30.0)
    ap.add_argument("--sat-sizes", default="4,5,6,7,8,9,10,11")
    ap.add_argument("--fmb-timeout", type=int, default=300)
    ap.add_argument("--shard", default=None)
    args = ap.parse_args()

    solver = None
    if args.solver_dir:
        sys.path.insert(0, args.solver_dir)
        import solver
        solver.trace = lambda *a, **k: None
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et
    sat_sizes = [int(x) for x in args.sat_sizes.split(",") if x.strip()]

    laws = load_laws(args.inp)
    if args.shard:
        i, m = (int(x) for x in args.shard.split("/"))
        laws = [L for k, L in enumerate(laws) if k % m == i]
    print(f"re-screening {len(laws)} light-pass candidates at heavy budget", flush=True)

    confirmed = 0
    with open(args.out, "w") as f:
        for j, law in enumerate(laws, 1):
            if j % 25 == 0:
                print(f"  {j}/{len(laws)} | {confirmed} confirmed", flush=True)
            if solver is not None and solver_has_finite_model(
                    solver, law, args.mf2_budget, sat_sizes):
                continue
            if fmb_from_law(et, law, args.fmb_timeout, args.vampire) == "MODEL_FOUND":
                continue
            confirmed += 1
            f.write(json.dumps({"law": law, "stage": "confirmed_no_finite_model",
                                "fmb_timeout": args.fmb_timeout}) + "\n")
            f.flush()
    print(f"confirmed Austin candidates (no finite model in {args.fmb_timeout}s): "
          f"{confirmed}/{len(laws)} -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
