#!/usr/bin/env python3
"""Reject one-op extensions that are logically equivalent to their own seed.

WHY
    `equiv_sample.py` on 48 AUSTIN_PROVEN laws found 5 equivalent pairs, and **every one
    was a seed and its own one-op extension** — e.g.

        x = (((y ◇ y) ◇ y) ◇ x) ◇ (y ◇ z)               (28770)
        x = ((((y ◇ y) ◇ y) ◇ x) ◇ (y ◇ (z ◇ y)))       its extension: the SAME LAW

    Extension by one operation can leave the theory unchanged. That is a systematic
    inflation of the corpus, it scales with the harvest, and it lands directly on the
    number that goes in an abstract. Filter at generation time, not at write-up time.

HOW, AND WHY IT IS ALMOST FREE
    A seed that is `AUSTIN_PROVEN` has a saturated set, and by JRS that set IS a model of
    the seed (see `ordered_model.py`). So:

        extension fails on a ground instance in the seed's model
            => seed does not entail extension
            => not equivalent, KEEP the extension          [no prover, microseconds]

    Only extensions that survive the seed's model go to Vampire, and there we demand
    proofs in both directions before discarding anything.

    Error direction: we never discard a law that is not provably equivalent to its seed.
    We may keep a law that IS equivalent but whose proof missed the budget — the corpus
    is then an over-count, which is the same bound we report everywhere else.

USAGE
    python3 paper/scripts/seed_dedupe.py --seed-law 'x = ...' --seed-cert paper/certs/....sat \
        --extensions exts.jsonl --vampire paper/bin/vampire --out kept.jsonl
"""
from __future__ import annotations
import argparse, itertools, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                              # noqa: E402
import prove_status as ps                                           # noqa: E402
import ordered_model as om                                          # noqa: E402

CARRIER = [("const", "sK0"), ("const", "sK1")]


def fails_in_model(eqs, small, law, cap=3000):
    """True  = law provably FAILS in this model  => keep (certified inequivalent).
       False = law survived the sampled instances => candidate, ask the prover.
       None  = step cap, no verdict               => candidate."""
    vs = sorted({v for t in et.parse_equation(law) for v in et.variables(t)})
    for vals in itertools.product(CARRIER, repeat=len(vs)):
        L, R = om.ground_law(law, dict(zip(vs, vals)))
        try:
            nl, _ = om.normalise(L, eqs, om.kbo_gt, small, cap)
            nr, _ = om.normalise(R, eqs, om.kbo_gt, small, cap)
        except TimeoutError:
            return None
        if nl != nr:
            return True
    return False


def equivalent(a, b, vbin, timeout):
    if not ps._proved(ps._run(vbin, ["--mode", "casc"], et.tptp_true(a, b), timeout)):
        return False
    return ps._proved(ps._run(vbin, ["--mode", "casc"], et.tptp_true(b, a), timeout))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-law", required=True)
    ap.add_argument("--seed-cert", help="saturation of the seed; enables the free filter")
    ap.add_argument("--extensions", required=True, help="jsonl with a 'law' field")
    ap.add_argument("--vampire", required=True)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--out")
    a = ap.parse_args()

    exts = [json.loads(l)["law"] for l in open(a.extensions) if l.strip()]
    eqs = small = None
    if a.seed_cert and os.path.exists(a.seed_cert):
        eqs, _ = om.load(a.seed_cert)
        small = om.smallest_const(eqs)

    kept, dropped, free, asked = [], [], 0, 0
    for law in exts:
        if eqs is not None:
            v = fails_in_model(eqs, small, law)
            if v is True:                       # certified inequivalent to the seed
                kept.append(law); free += 1
                continue
        asked += 1
        if equivalent(a.seed_law, law, a.vampire, a.timeout):
            dropped.append(law)
        else:
            kept.append(law)

    print(f"extensions {len(exts)}  kept {len(kept)}  dropped-as-duplicate {len(dropped)}")
    print(f"  separated prover-free by the seed's model: {free}   sent to prover: {asked}")
    for d in dropped:
        print(f"  DROP (≡ seed)  {d}")

    if a.out:
        with open(a.out, "w") as fh:
            for law in kept:
                fh.write(json.dumps({"law": law}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
