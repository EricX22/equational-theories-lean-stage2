#!/usr/bin/env python3
"""trivial_selfsolve.py — POSITIVE CONTROL for the trivial autoformalizer.

Before any "every model scored 0" claim can be written up, we must exclude the confound
"the harness never accepts anything." This searches for a genuinely valid chain a -> ... -> b
for a real law, using the SAME law-application machinery `trivial_autoform.justify_step`
accepts, then assembles it. If the emitted Lean is accepted by the judge, the pipeline
demonstrably accepts correct answers and any model 0 is a real model failure.

Search: the law's LHS is a bare variable, so a FORWARD application rewrites any subterm e to
T[x:=e, others:=free choice]. We take the forward closure from `a` and from `b` (bounded depth,
bounded term size, free vars drawn from a small pool) and look for a common term M. Then
    a -> ... -> M -> ... -> b
where the b-side steps are traversed in reverse (a reverse law application, which justify_step
also handles). Meeting in the middle keeps it to depth d on each side instead of 2d.

USAGE
  python3 paper/scripts/trivial_selfsolve.py --laws-file paper/results/trivial_easy20.jsonl --n 5
  python3 paper/scripts/trivial_selfsolve.py --law "x = ..." --emit out.lean
"""
from __future__ import annotations
import argparse, json, os, sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import etp_terms as et
import trivial_autoform as A


def size(n):
    return 1 if n[0] == "var" else 1 + size(n[1]) + size(n[2])


def instantiate(node, subst):
    if node[0] == "var":
        return subst.get(node[1], node)
    return ("op", instantiate(node[1], subst), instantiate(node[2], subst))


def render(n):
    return n[1] if n[0] == "var" else f"({render(n[1])} ◇ {render(n[2])})"


def forward_neighbors(u, T, vs, pool, maxsize):
    """One FORWARD law application at any position, other law vars from `pool`."""
    others = [v for v in vs if v != "x"]
    out = []
    for pos, sub in A._subterms(u):
        for assign in product(pool, repeat=len(others)):
            subst = {"x": sub}
            subst.update(dict(zip(others, assign)))
            new = A._replace(u, pos, instantiate(T, subst))
            if new != u and size(new) <= maxsize:
                out.append(new)
    return out


def closure(start, T, vs, pool, depth, maxsize, cap=4000):
    """term -> path from start, via forward applications, to `depth`."""
    seen = {start: [start]}
    frontier = [start]
    for _ in range(depth):
        nxt = []
        for u in frontier:
            # forward grows the term; REVERSE (reduction) is what can eliminate an `a`/`b`
            # from a term, so both are needed for the two closures to meet.
            for nb in forward_neighbors(u, T, vs, pool, maxsize) + A._reduce_neighbors(u, T):
                if nb not in seen:
                    seen[nb] = seen[u] + [nb]
                    nxt.append(nb)
                    if len(seen) > cap:
                        return seen
        frontier = nxt
    return seen


def selfsolve(law, depth=2, maxsize=48):
    T, vs = A._law(law)
    a, b = ("var", "a"), ("var", "b")
    pool = [a, b]
    Fa = closure(a, T, vs, pool, depth, maxsize)
    Fb = closure(b, T, vs, pool, depth, maxsize)
    common = set(Fa) & set(Fb)
    if not common:
        return None
    M = min(common, key=size)                       # smallest meeting point
    return Fa[M] + list(reversed(Fb[M]))[1:]        # a -> ... -> M -> ... -> b


def try_law(law, depth, maxsize):
    chain = selfsolve(law, depth, maxsize)
    if chain is None:
        return None, "no meeting point found"
    strs = [render(t) for t in chain]
    body, err = A.assemble(law, strs)
    if body is None:
        return None, f"chain found but assemble rejected it: {err}"
    return body, f"chain length {len(strs)-1} steps"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--laws-file"); ap.add_argument("--law")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--maxsize", type=int, default=48)
    ap.add_argument("--emit", help="write the first successful Lean body here")
    a = ap.parse_args()

    laws = []
    if a.law:
        laws = [a.law]
    else:
        for line in open(a.laws_file, encoding="utf-8"):
            if line.strip():
                laws.append(json.loads(line)["law"])
        laws = laws[:a.n]

    emitted = False
    for i, law in enumerate(laws, 1):
        body, note = try_law(law, a.depth, a.maxsize)
        tag = "FOUND " if body else "------"
        print(f"[{i}/{len(laws)}] {tag} {note:52} {law[:44]}")
        if body and not emitted:
            print("\n---- assembled Lean (POSITIVE CONTROL) ----\n" + body)
            if a.emit:
                with open(a.emit, "w", encoding="utf-8") as fh:
                    fh.write(body)
                print(f"(written to {a.emit} — judge this once to validate the pipeline)")
            emitted = True


if __name__ == "__main__":
    main()
