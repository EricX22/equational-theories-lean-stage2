#!/usr/bin/env python3
"""Equivalence classes by SAMPLE, with model-based separation. PAPER_PLAN.md §5D.

THE GATE
    "Do 3,428 laws collapse to forty classes?" does not need 3,428 laws or 12M prover
    calls. Sample n, count classes, stop. 250 laws giving 240 classes means no collapse;
    250 giving 30 means the paper changes and you knew by lunchtime.

THE ALGORITHM, and why it is cheap
    Naive pairwise is O(n²) prover calls, each expensive. But a law's saturated set IS a
    model of it (JRS; see `ordered_model.py`). So for AUSTIN_PROVEN laws:

        L_j fails on a ground instance in M_i   =>   L_i does not entail L_j
                                                =>   CERTIFIED inequivalent, no prover

    Only pairs that survive *mutual* ground satisfaction go to the prover, and there we
    ask for a real proof in both directions. Measured on a 48-law sample: 1,123 of 1,128
    pairs separated prover-free, 5 sent to Vampire. A 225x reduction.

    Note the direction of every error:
      - separation is SOUND (a counterexample instance is a counterexample);
      - a surviving pair is only a CANDIDATE, and the prover decides it;
      - so we never wrongly merge. We can still wrongly split, if the prover fails to
        prove a true equivalence inside the budget. Class count is an UPPER BOUND.

    Equivalence is semi-decidable in the positive direction only, so that bound cannot
    be closed by more cleverness — only by more compute. Report it as a bound, with the
    budget attached.

WHERE THIS DOES NOT WORK
    The hard tier is `NO_FINITE_MODEL`: laws whose saturation did NOT close. No
    saturated set, no model, no cheap separations. There the sample must be decided by
    the prover alone, incremental union-find against class representatives, two calls
    per (law, representative). That is the run this script performs with `--no-models`.

USAGE
    python3 paper/scripts/equiv_sample.py --in 'paper/results/*_status_*.jsonl' \
        --status AUSTIN_PROVEN --n 250 --vampire paper/bin/vampire \
        --sat-timeout 20 --prove-timeout 30 --certs /tmp/eqcerts
"""
from __future__ import annotations
import argparse, glob, itertools, json, os, random, sys
import concurrent.futures as cf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                              # noqa: E402
import prove_status as ps                                           # noqa: E402
import ordered_model as om                                          # noqa: E402

CARRIER = [("const", "sK0"), ("const", "sK1")]


def saturate(law, vbin, timeout, path):
    if os.path.exists(path):
        return True
    ax, _ = ps._lawax(et, law)
    body = ax + "\nfof(nt,axiom,?[U,V]: U != V).\n"
    args = ["-sa", "otter", "--show_active", "on"]
    out = ps._run(vbin, args, body, timeout)
    if not ps._satisfiable(out):
        return False
    with open(path, "w") as fh:
        fh.write(f"% law: {law}\n% saturated-with: {' '.join(args)} (default -to kbo)\n\n"
                 + body + "\n" + out)
    return True


def holds_in(eqs, small, law, cap=3000):
    """None = no verdict (step cap). False = CERTIFIED failure. True = passed the sample."""
    vs = sorted({v for t in et.parse_equation(law) for v in et.variables(t)})
    for vals in itertools.product(CARRIER, repeat=len(vs)):
        L, R = om.ground_law(law, dict(zip(vs, vals)))
        try:
            nl, _ = om.normalise(L, eqs, om.kbo_gt, small, cap)
            nr, _ = om.normalise(R, eqs, om.kbo_gt, small, cap)
        except TimeoutError:
            return None
        if nl != nr:
            return False
    return True


def equivalent(a, b, vbin, timeout):
    fwd = ps._proved(ps._run(vbin, ["--mode", "casc"], et.tptp_true(a, b), timeout))
    if not fwd:
        return False
    return ps._proved(ps._run(vbin, ["--mode", "casc"], et.tptp_true(b, a), timeout))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--status", default="AUSTIN_PROVEN")
    ap.add_argument("--n", type=int, default=250)
    ap.add_argument("--seed", type=int, default=2)
    ap.add_argument("--vampire", required=True)
    ap.add_argument("--sat-timeout", type=int, default=20)
    ap.add_argument("--prove-timeout", type=int, default=30)
    ap.add_argument("--certs", default="/tmp/eqcerts")
    ap.add_argument("--no-models", action="store_true",
                    help="hard tier: no saturations exist, decide every pair by prover")
    ap.add_argument("--out")
    a = ap.parse_args()

    laws = []
    for fn in glob.glob(a.inp):
        for line in open(fn):
            r = json.loads(line)
            if r.get("status") == a.status:
                laws.append(r["law"])
    laws = sorted(set(laws))
    random.Random(a.seed).shuffle(laws)
    laws = laws[:a.n]
    print(f"{len(laws)} laws, status={a.status}", file=sys.stderr)

    os.makedirs(a.certs, exist_ok=True)
    models, pairs = {}, []
    sep = capped = 0
    total_pairs = len(laws) * (len(laws) - 1) // 2

    if not a.no_models:
        with cf.ThreadPoolExecutor() as ex:
            got = list(ex.map(lambda t: (t[0], saturate(t[1], a.vampire, a.sat_timeout,
                                                        f"{a.certs}/{t[0]:03d}.sat")),
                              enumerate(laws)))
        for i, ok in got:
            if ok:
                eqs, _ = om.load(f"{a.certs}/{i:03d}.sat")
                models[i] = (eqs, om.smallest_const(eqs))
        print(f"{len(models)} saturations ({len(laws) - len(models)} timed out)", file=sys.stderr)

        for i, j in itertools.combinations(range(len(laws)), 2):
            if i not in models or j not in models:
                pairs.append((i, j))                      # no model: prover must decide
                continue
            ij = holds_in(*models[i], laws[j])
            ji = holds_in(*models[j], laws[i])
            if ij is False or ji is False:
                sep += 1                                   # CERTIFIED inequivalent
            elif ij is None or ji is None:
                capped += 1; pairs.append((i, j))
            else:
                pairs.append((i, j))
        print(f"separated prover-free: {sep}   step-capped: {capped}   "
              f"to prover: {len(pairs)}", file=sys.stderr)
    else:
        pairs = list(itertools.combinations(range(len(laws)), 2))

    parent = list(range(len(laws)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    merged = []
    with cf.ThreadPoolExecutor() as ex:
        for (i, j), eq in zip(pairs, ex.map(
                lambda p: equivalent(laws[p[0]], laws[p[1]], a.vampire, a.prove_timeout), pairs)):
            if eq:
                merged.append((laws[i], laws[j]))
                x, y = find(i), find(j)
                if x != y:
                    parent[x] = y

    classes = {}
    for i in range(len(laws)):
        classes.setdefault(find(i), []).append(i)
    print(f"\nlaws {len(laws)}  ->  classes <= {len(classes)}   "
          f"(UPPER BOUND at {a.prove_timeout}s/direction)")
    print(f"non-singleton classes: {sum(1 for v in classes.values() if len(v) > 1)}")
    print(f"pair accounting: total {total_pairs}  separated {sep}  "
          f"proven-equiv {len(merged)}  INCONCLUSIVE {len(pairs) - len(merged)}")
    for x, y in merged:
        print(f"  EQUIVALENT  {x}\n              {y}")

    if a.out:
        with open(a.out, "w") as fh:
            json.dump({"n": len(laws), "classes": len(classes),
                       "merged": merged, "budget": a.prove_timeout,
                       "total_pairs": total_pairs,
                       "separated_prover_free": sep, "step_capped": capped,
                       "to_prover": len(pairs), "proven_equivalent": len(merged),
                       "inconclusive": len(pairs) - len(merged)}, fh, indent=1)


if __name__ == "__main__":
    main()
