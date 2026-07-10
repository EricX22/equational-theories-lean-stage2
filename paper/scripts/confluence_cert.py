#!/usr/bin/env python3
"""Self-contained, Vampire-free proof that a law `x = T` is nontrivial.

Why this exists
---------------
`AUSTIN_PROVEN` currently rests on Vampire reporting `SZS status Satisfiable`.
That is a claim about Vampire, not a proof we can hand to a referee. This script
replaces it with a finite check anyone can rerun in seconds, and it produces the
model as a side effect.

The argument
------------
Read the law as the rewrite rule  T -> x.

1. TERMINATION IS FREE. `x` occurs in `T` and `T != x`, so every rewrite replaces
   a term by a *proper subterm* of itself. Strictly decreasing size, no ordering
   needed, no proof obligation. This holds for every law of this shape.

2. CONFLUENCE IS A FINITE CHECK. Knuth-Bendix: a terminating rewrite system is
   confluent iff all of its critical pairs are joinable. The system has one rule,
   so the critical pairs are the overlaps of `T` with itself -- finitely many,
   computed by unification. Normalize both sides of each and compare.
   (The critical-pair lemma does not require left-linearity, which matters here:
   these `T` repeat their variables.)

3. THEREFORE the ground terms over two constants a, b, in normal form, are a
   magma satisfying the law -- and `a`, `b` are distinct normal forms, so it is
   nontrivial. `L` does not entail `x = y`.

Combined with claim (i) (no nontrivial *finite* model, from prove_status.py), the
model is nontrivial and cannot be finite: **the law is Austin**, and the model is
the one this script just built.

Both steps are checkable by hand. Neither trusts an ATP.

  python paper/scripts/confluence_cert.py --law "x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))"
  python paper/scripts/confluence_cert.py --in paper/results/gold.jsonl --out certs.jsonl
"""
from __future__ import annotations
import argparse, itertools, json, os, sys


# ---------------------------------------------------------------- terms -----
def rename(t, suf):
    return ("var", t[1] + suf) if t[0] == "var" else ("op", rename(t[1], suf), rename(t[2], suf))


def occurs(v, t):
    return t[1] == v if t[0] == "var" else occurs(v, t[1]) or occurs(v, t[2])


def subst(t, s):
    """Fully resolve through the (triangular) substitution."""
    t = walk(t, s)
    return t if t[0] == "var" else ("op", subst(t[1], s), subst(t[2], s))


def unify(a, b, s=None):
    s = {} if s is None else s
    a, b = walk(a, s), walk(b, s)
    if a == b:
        return s
    if a[0] == "var":
        rb = subst(b, s)          # resolve first: triangular bindings can hide a cycle
        if occurs(a[1], rb):
            return None
        s[a[1]] = rb
        return s
    if b[0] == "var":
        return unify(b, a, s)
    s = unify(a[1], b[1], s)
    return unify(a[2], b[2], s) if s is not None else None


def walk(t, s):
    while t[0] == "var" and t[1] in s:
        t = s[t[1]]
    return t


def positions(t, p=()):
    """Non-variable positions."""
    if t[0] == "op":
        yield p
        yield from positions(t[1], p + (1,))
        yield from positions(t[2], p + (2,))


def at(t, p):
    for i in p:
        t = t[i]
    return t


def put(t, p, new):
    if not p:
        return new
    if p[0] == 1:
        return ("op", put(t[1], p[1:], new), t[2])
    return ("op", t[1], put(t[2], p[1:], new))


def size(t):
    return 1 if t[0] == "var" else size(t[1]) + size(t[2])


def show(t):
    return t[1] if t[0] == "var" else f"({show(t[1])} ◇ {show(t[2])})"


# ------------------------------------------------------------ rewriting -----
def match(pat, t, s):
    """One-way matching; respects repeated variables (T is not left-linear)."""
    if pat[0] == "var":
        if pat[1] in s:
            return s[pat[1]] == t
        s[pat[1]] = t
        return True
    if t[0] != "op":
        return False
    return match(pat[1], t[1], s) and match(pat[2], t[2], s)


def step(t, L, R):
    for p in positions(t):
        s = {}
        if match(L, at(t, p), s):
            return put(t, p, subst(R, s))
    return None


def nf(t, L, R, fuel=100000):
    while fuel:
        u = step(t, L, R)
        if u is None:
            return t
        t = u
        fuel -= 1
    raise RuntimeError("no normal form (termination argument violated?)")


# ------------------------------------------------------- critical pairs -----
def critical_pairs(L, R):
    """Overlaps of the single rule with a renamed copy of itself."""
    L2, R2 = rename(L, "'"), rename(R, "'")
    out = []
    for p in positions(L):
        if p == () :
            continue          # root overlap with a variant of itself: trivial
        s = unify(at(L, p), L2)
        if s is None:
            continue
        left = subst(put(L, p, R2), s)   # rewrite the inner redex with rule 2
        right = subst(R, s)              # rewrite the outer redex with rule 1
        out.append((p, left, right))
    return out


def check_law(law):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et
    lhs, T = et.parse_equation(law)
    assert lhs == ("var", "x"), "expected a law of the form  x = T"
    L, R = T, ("var", "x")

    # 1. termination, for free
    assert occurs("x", T) and size(T) > 1, "x must occur in T and T != x"

    # 2. all critical pairs joinable?
    cps = critical_pairs(L, R)
    bad = []
    for p, u, v in cps:
        if nf(u, L, R) != nf(v, L, R):
            bad.append((p, show(u), show(v)))

    res = {"law": law, "critical_pairs": len(cps), "joinable": len(cps) - len(bad),
           "confluent": not bad}
    if bad:
        res["nonjoinable"] = bad[:3]
        res["nontrivial_model"] = None
        return res

    # 3. the model: ground normal forms over {a, b}
    a, b = ("var", "a"), ("var", "b")
    assert nf(a, L, R) == a and nf(b, L, R) == b and a != b
    terms, frontier = [a, b], [a, b]
    for _ in range(3):
        new = []
        for u in frontier:
            for v in terms:
                for t in (("op", u, v), ("op", v, u)):
                    n = nf(t, L, R)
                    if n not in terms and n not in new:
                        new.append(n)
        terms += new; frontier = new
    res["nontrivial_model"] = True
    res["model"] = "ground terms over {a,b} in normal form; op(u,v) = nf(u◇v)"
    res["distinct_elements_found"] = len(terms)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--law")
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out")
    a = ap.parse_args()

    laws = [a.law] if a.law else [json.loads(l)["law"] for l in open(a.inp) if l.strip()]
    out = open(a.out, "w") if a.out else None
    ok = 0
    for law in laws:
        try:
            r = check_law(law)
        except Exception as e:
            r = {"law": law, "error": str(e)}
        ok += bool(r.get("nontrivial_model"))
        verdict = ("NONTRIVIAL (confluent, model built)" if r.get("nontrivial_model")
                   else f"not proved: {r.get('nonjoinable', r.get('error', 'n/a'))}")
        print(f"{verdict:42s} cps={r.get('critical_pairs','?'):>3} | {law}", flush=True)
        if out:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n{ok}/{len(laws)} laws proved nontrivial by confluence (no ATP involved)")
    if out:
        out.close()


if __name__ == "__main__":
    main()
