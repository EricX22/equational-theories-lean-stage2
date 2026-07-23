#!/usr/bin/env python3
"""Corroboration probe: instantiation-based (iProver) and model-evolution
(Darwin) provers on the hard-25 construction sample.

WHY THIS EXISTS
    The baseline portfolio contains the two paradigms that certify a nontrivial
    (hence infinite) model via a FINITE presentation: superposition (Vampire, E)
    and completion (Twee). Every other automated model-finding method certifies
    satisfiability by exhibiting a *finite* model, which admissibility excludes by
    theorem (Mace4, Paradox, SMT finite-model-finding, and iProver's instantiation
    mode all land here). The only distinct first-order model-search paradigms left
    are instantiation-based (iProver) and model evolution (Darwin). iProver adds no
    infinite-model capability the portfolio lacks (its only such component is
    superposition, already covered); Darwin's finite context can in principle
    represent an infinite Herbrand model, so it is the one paradigm not settled by
    argument.

    This probe runs iProver and Darwin on the hard-25 to confirm empirically that
    neither returns a model certificate within budget. The claim in the paper stays
    scoped to "no method we run": a categorical zero on a stated sample, not a rate.

ENCODING (identical to baseline_probe's saturation problem)
    fof(law,axiom,![vars]:(l=r)).
    fof(nt,axiom,?[U,V]: U != V).
    Satisfiable / CounterSatisfiable -> nontrivial model found      (AUSTIN)
    Theorem / Unsatisfiable          -> collapses to a point        (TRIVIAL)
    neither, within budget           -> no certificate              ('-')

USAGE
    # confirm the wiring on a known-SAT and known-UNSAT toy first
    python3 paper/scripts/paradigm_probe.py --selftest \
        --iprover $(which iproveropt) --darwin $(which darwin)

    # the real run (writes .p files under --certs and a jsonl under --out)
    python3 paper/scripts/paradigm_probe.py \
        --in paper/results/hard25_sample.jsonl \
        --iprover $(which iproveropt) --darwin $(which darwin) \
        --budgets 300 --out paper/results/paradigm_hard25.jsonl \
        --certs paper/certs/paradigm

    # just emit the 25 TPTP files, run no prover
    python3 paper/scripts/paradigm_probe.py --emit-only --certs paper/certs/paradigm

FLAG NOTES
    iProver timeout flag is --time_out_real on current builds; if your build differs
    (older ones use --time_out_virtual), edit PROVERS below. Darwin is guarded by a
    subprocess timeout since not every build honours a native one; if yours does,
    append it in PROVERS.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, tempfile, time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                          # noqa: E402
from prove_status import _lawax, _satisfiable, _proved          # noqa: E402

# kind -> function(binpath, timeout) -> argv prefix (problem file appended last)
PROVERS = {
    "iprover": lambda b, t: [b, "--time_out_real", str(t)],
    "darwin":  lambda b, t: [b],   # guarded by subprocess timeout below
}


def build_body(law: str):
    """The saturation problem for `law`: the law, plus 'two elements differ'."""
    ax, vs = _lawax(et, law)
    return ax + "\nfof(nt,axiom,?[U,V]: U != V).\n", vs


def run_prover(kind: str, binpath: str, body: str, timeout: int) -> str:
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "prob.p")
        with open(p, "w") as fh:
            fh.write(body)
        argv = PROVERS[kind](binpath, timeout) + [p]
        try:
            r = subprocess.run(argv, capture_output=True, text=True,
                               timeout=timeout + 15)
            return (r.stdout or "") + "\n" + (r.stderr or "")
        except subprocess.TimeoutExpired:
            return ""
        except FileNotFoundError:
            sys.exit(f"prover binary not found: {binpath}")


def verdict(out: str) -> str:
    if _satisfiable(out):
        return "AUSTIN"
    if _proved(out):
        return "TRIVIAL"
    return "-"


def selftest(a):
    sat = ("fof(law,axiom,![X]:(X=X)).\n"
           "fof(nt,axiom,?[U,V]: U != V).\n")            # 2-elt model exists
    uns = ("fof(collapse,axiom,![X,Y]:(X=Y)).\n"
           "fof(nt,axiom,?[U,V]: U != V).\n")            # forces 1 = 2, unsat
    ok = True
    for kind, binp in (("iprover", a.iprover), ("darwin", a.darwin)):
        if not binp:
            continue
        vs = verdict(run_prover(kind, binp, sat, 20))
        vu = verdict(run_prover(kind, binp, uns, 20))
        print(f"selftest {kind:8s}: SAT-toy -> {vs} (want AUSTIN), "
              f"UNSAT-toy -> {vu} (want TRIVIAL)")
        ok = ok and vs == "AUSTIN" and vu == "TRIVIAL"
    print("selftest", "PASS" if ok else "CHECK FLAGS")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp",
                    default="paper/results/hard25_sample.jsonl")
    ap.add_argument("--iprover")
    ap.add_argument("--darwin")
    ap.add_argument("--budgets", default="300",
                    help="comma-separated seconds, e.g. 300 or 120,300,600")
    ap.add_argument("--out", default="paper/results/paradigm_hard25.jsonl")
    ap.add_argument("--certs", default="paper/certs/paradigm")
    ap.add_argument("--emit-only", action="store_true",
                    help="write the .p files and exit; run no prover")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest(a)

    budgets = [int(b) for b in a.budgets.split(",")]
    os.makedirs(a.certs, exist_ok=True)
    laws = [json.loads(l)["law"] for l in open(a.inp) if l.strip()]
    provers = [(k, b) for k, b in (("iprover", a.iprover),
                                   ("darwin", a.darwin)) if b]
    if not provers and not a.emit_only:
        sys.exit("give --iprover and/or --darwin, or use --emit-only")

    tally = Counter()
    outfh = None if a.emit_only else open(a.out, "w")
    for i, law in enumerate(laws):
        body, vs = build_body(law)
        pth = os.path.join(a.certs, f"hard25_{i:02d}.p")
        with open(pth, "w") as fh:
            fh.write(f"% hard25 #{i}  vars={vs}  gold=austin\n" + body)
        if a.emit_only:
            print(f"[emit] {pth}  ({len(vs)} vars)")
            continue
        for kind, binp in provers:
            for b in budgets:
                t0 = time.time()
                v = verdict(run_prover(kind, binp, body, b))
                secs = round(time.time() - t0, 1)
                outfh.write(json.dumps({"i": i, "prover": kind, "budget": b,
                                        "verdict": v, "secs": secs,
                                        "law": law}) + "\n")
                outfh.flush()
                tally[(kind, v)] += 1
                print(f"#{i:02d} {kind:8s} {b:4d}s -> {v:8s} ({secs}s)")
    if outfh:
        outfh.close()
        print("\n=== summary (verdicts per prover) ===")
        for kind, _ in provers:
            row = {v: tally[(kind, v)] for v in ("AUSTIN", "TRIVIAL", "-")}
            print(f"  {kind:8s}: {row}")
        print(f"\nwrote {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
