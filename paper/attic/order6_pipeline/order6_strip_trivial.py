#!/usr/bin/env python3
"""Strip trivial laws from order-6 candidates — the missing Austin filter.

A random order-6 "x = T" law (4 vars) is heavily over-constrained, so most have
no nontrivial finite model *because they are trivial* (they entail x=y). Those pass
a "no finite model" fmb check but are NOT Austin — Austin requires a nontrivial
(infinite) model. This pass removes them cheaply: a fast Vampire proof of L |= x=y
means trivial (drop); failure to prove it means potentially-Austin (keep).

This is far cheaper than fmb (seconds vs minutes) and is the correct discriminator
for the trivial-vs-Austin axis. Run it on the fmb candidates; survivors = laws with
no small finite model AND not provably trivial = genuine Austin candidates.

Usage:
  python paper/scripts/order6_strip_trivial.py \
      --in 'paper/results/order6_c_*.jsonl' --vampire paper/bin/vampire \
      --prove-timeout 10 --shard 0/16 --out paper/results/order6_austin_0.jsonl
"""
from __future__ import annotations
import argparse, glob, json, os, subprocess, sys, tempfile


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


def proves_trivial(et, law, timeout, vbin):
    """Does L |= (x=y)?  (True => trivial => NOT Austin.)"""
    l, r, vs = et.tptp_eq_vars(law)
    body = (f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\n"
            "fof(triv,conjecture,![X,Y]:(X=Y)).\n")
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "p.p")
        open(p, "w").write(body)
        try:
            s = subprocess.run([vbin, "--mode", "casc", "-t", f"{timeout}s", p],
                               capture_output=True, text=True, timeout=timeout + 5).stdout
        except subprocess.TimeoutExpired:
            return False
    return "SZS status Theorem" in s or "Refutation found" in s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--prove-timeout", type=int, default=10)
    ap.add_argument("--shard", default=None)
    args = ap.parse_args()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et

    laws = load_laws(args.inp)
    if args.shard:
        i, m = (int(x) for x in args.shard.split("/"))
        laws = [L for k, L in enumerate(laws) if k % m == i]
    print(f"stripping trivial laws from {len(laws)} candidates", flush=True)

    kept = trivial = 0
    with open(args.out, "w") as f:
        for j, law in enumerate(laws, 1):
            if j % 50 == 0:
                print(f"  {j}/{len(laws)} | {kept} kept (non-trivial), {trivial} trivial", flush=True)
            if proves_trivial(et, law, args.prove_timeout, args.vampire):
                trivial += 1
                continue
            kept += 1
            f.write(json.dumps({"law": law, "stage": "austin_candidate"}) + "\n")
            f.flush()
    print(f"kept {kept} non-trivial (Austin candidates), dropped {trivial} trivial "
          f"-> {args.out}", flush=True)


if __name__ == "__main__":
    main()
