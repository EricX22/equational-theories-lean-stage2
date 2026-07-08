#!/usr/bin/env python3
"""Targeted order-6 generation: extend KNOWN Austin laws by one operation.

Random order-6 sampling finds Austin laws at ~0.02% (and ~0 Rung-4). But a
one-operation extension of a known Austin law preserves Austin-ness far more
often (~10% reach the non-trivial + no-small-model stage in tests) — because the
no-finite-model mechanism is largely inherited. Extending the RUNG-4 laws is the
way to generate more *hard* problems rather than hoping they appear at random.

For each seed law "x = T", replace each variable-leaf `v` with `(v ◇ w)` or
`(w ◇ v)` for every variable w, giving order-6 (7-leaf) laws. Canonically dedup,
run the cheap n<=3 no-small-model screen, and emit survivors as a candidate pool
(one {"law": ...} per line) for the strip -> confirm -> grade pipeline.

Seeds: by default the order-5 Austin corpus (order_5.tex tables); or pass
--seeds-in <jsonl with "law"> to extend any set (e.g. newly-confirmed order-6
Austin laws, to go to order 7).

Usage:
  python paper/scripts/order6_targeted.py \
      --out paper/problems/order6_targeted_pool.jsonl [--seeds-in ...] [--shard 0/8]
"""
from __future__ import annotations
import argparse, itertools, json, re, sys


VARS = ["x", "y", "z", "w"]


def parse_term(s):
    # minimal parser for "a ◇ b" terms with parens; returns nested tuple
    toks = re.findall(r"◇|\(|\)|[A-Za-z]\w*", s)
    pos = 0
    def atom():
        nonlocal pos
        t = toks[pos]
        if t == "(":
            pos += 1; e = expr(); pos += 1; return e
        pos += 1; return ("var", t)
    def expr():
        nonlocal pos
        left = atom()
        while pos < len(toks) and toks[pos] == "◇":
            pos += 1; left = ("op", left, atom())
        return left
    return expr()


def rhs_of(law):
    return parse_term(law.split("=", 1)[1])


def ts(t):
    return t[1] if t[0] == "var" else "(" + ts(t[1]) + " ◇ " + ts(t[2]) + ")"


def hv(t, v):
    return t[1] == v if t[0] == "var" else (hv(t[1], v) or hv(t[2], v))


def canon_law(T):
    order = {}
    def w(n):
        if n[0] == "var":
            if n[1] not in order: order[n[1]] = chr(97 + len(order))
            return order[n[1]]
        return "(" + w(n[1]) + "*" + w(n[2]) + ")"
    return "a=" + w(T)   # lhs var 'x' -> 'a'


def leaf_paths(t, path=()):
    if t[0] == "var":
        yield path
    else:
        yield from leaf_paths(t[1], path + (1,))
        yield from leaf_paths(t[2], path + (2,))


def get_at(t, p):
    for s in p: t = t[s]
    return t


def repl_at(t, p, new):
    if not p: return new
    if p[0] == 1: return ("op", repl_at(t[1], p[1:], new), t[2])
    return ("op", t[1], repl_at(t[2], p[1:], new))


def extensions(T):
    for p in leaf_paths(T):
        leaf = get_at(T, p)
        for w in VARS:
            yield repl_at(T, p, ("op", leaf, ("var", w)))
            yield repl_at(T, p, ("op", ("var", w), leaf))


def _ev(t, op, env):
    if t[0] == "var": return env[t[1]]
    return op(_ev(t[1], op, env), _ev(t[2], op, env))


def has_small_model(T, maxn=3):
    vs = sorted(set(v for v in VARS if hv(T, v)) | {"x"})
    for n in range(2, maxn + 1):
        assigns = list(itertools.product(range(n), repeat=len(vs)))
        for tab in itertools.product(range(n), repeat=n * n):
            op = (lambda tt, nn: (lambda a, b: tt[a * nn + b]))(tab, n)
            if all(_ev(T, op, dict(zip(vs, a))) == dict(zip(vs, a))["x"] for a in assigns):
                return True
    return False


def load_seeds(args):
    if args.seeds_in:
        return [json.loads(l)["law"] for l in open(args.seeds_in) if l.strip()]
    tex = open(args.order5_tex).read()
    return ["x = " + re.sub(r"\s+", " ", b.replace("\\op", "◇").replace("\\", "").strip()).split("=", 1)[1]
            for b, _ in re.findall(r"\$(x =[^$]+)\$ \((\d+)\)", tex)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds-in", default=None, help="jsonl of seed laws (default: order5 tables)")
    ap.add_argument("--order5-tex",
                    default="../reference/equational_theories/blueprint/src/chapter/order_5.tex")
    ap.add_argument("--cheap-max-n", type=int, default=3)
    ap.add_argument("--shard", default=None)
    args = ap.parse_args()

    seeds = load_seeds(args)
    # generate + canonically dedup all one-op extensions
    seen, laws = set(), []
    for law in seeds:
        T = rhs_of(law)
        for E in extensions(T):
            k = canon_law(E)
            if k not in seen:
                seen.add(k); laws.append(E)
    if args.shard:
        i, m = (int(x) for x in args.shard.split("/"))
        laws = [E for j, E in enumerate(laws) if j % m == i]
    print(f"{len(seeds)} seeds -> {len(laws)} unique one-op extensions (this shard)", flush=True)

    kept = 0
    with open(args.out, "w") as f:
        for j, E in enumerate(laws, 1):
            if j % 200 == 0:
                print(f"  cheap-screened {j}/{len(laws)}, {kept} kept", flush=True)
            if has_small_model(E, args.cheap_max_n):
                continue
            kept += 1
            f.write(json.dumps({"law": "x = " + ts(E)}, ensure_ascii=False) + "\n")
            f.flush()
    print(f"kept {kept} extensions with no model up to Fin{args.cheap_max_n} "
          f"-> {args.out}  (next: strip -> confirm+grade)", flush=True)


if __name__ == "__main__":
    main()
