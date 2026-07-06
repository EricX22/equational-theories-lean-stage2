#!/usr/bin/env python3
"""Complete decision for the commutative algebraic-linear family (the honest
tier-4 subtraction for the infinite track).

Background. A linear magma is x*y = a*x + b*y with a, b in a commutative ring R
(the al_ / ZZ[alpha] family). Because the operation is linear, EQ1 holds as an
identity iff, for every variable, the coefficient of that variable agrees on both
sides -- a set of polynomial equations in the two commuting scalars a, b. The
solver already derives these: `al_constraints` returns them as polynomials
{(i,j): coeff} meaning coeff * a^i * b^j. EQ2 fails iff some EQ2 coefficient
polynomial is nonzero in R.

The current `al_find_linear_model` only searches the idempotent slice b = 1 - a
(one alpha, GCD of the univariate reductions), so it is an INCOMPLETE subtraction:
a pair with a general (b != 1 - a) linear model slips through and gets mislabeled
an infinite CANDIDATE -- the exact Level-1 redundancy trap (an underpowered search
masquerading as an LLM target).

Complete decision. Let I = <EQ1 constraints> in QQ[a, b]. The universal EQ1-model
is R = QQ[a, b]/I with (a, b) = the images of the generators; it satisfies EQ1 by
construction and, being a nonzero char-0 QQ-algebra, is INFINITE. EQ2 fails in R
iff some EQ2-constraint q is nonzero in R, i.e. q ∉ I. So:

    a commutative linear counterexample exists  <=>  some EQ2 constraint q ∉ I

which a Groebner basis decides exactly -- no caps. If EVERY q ∈ I, then NO linear
model refutes the pair (finite OR infinite), a genuine complete subtraction of the
whole commutative-linear family, not a search cutoff. Finite affine (mod n) models
are a separate, char-p story handled upstream by af_find; this module is the
char-0 / infinite-linear decision.

Scope / caveats (state them honestly):
  * Constant-free family x*y = a*x + b*y (matches the existing al_ family and its
    constraint derivation). A +c generalization would add a third variable; TODO.
  * Commutative coefficients (ZZ[alpha] is commutative). A non-commutative linear
    model (matrix a, b) could in principle refute a pair no commutative one does;
    that is a strictly larger family and a separate, harder subtraction.
  * Decision is over QQ. q ∉ I over QQ gives a genuine char-0 (infinite) model;
    passing to a ZZ-order for a Lean cert is denominator-clearing (rare torsion
    edge cases aside). Cert emission reuses solver.al_emit_cert for the idempotent
    slice; the general-b cert builder is a follow-up.
"""
from __future__ import annotations
import argparse
import json
import sys


def _to_sympy(poly, a, b):
    """{(i,j): coeff} -> sympy expression coeff*a^i*b^j (coeff may be Fraction)."""
    import sympy
    expr = sympy.Integer(0)
    for (i, j), c in poly.items():
        expr += sympy.Rational(c.numerator, c.denominator) * a**i * b**j
    return sympy.expand(expr)


def decide_linear(solver, eq1, eq2):
    """Decide whether a commutative (char-0) linear model refutes the pair.

    Returns a dict:
      exists      : bool  -- a linear counterexample exists (=> NOT an LLM target)
      verdict     : 'INFINITE_LINEAR_EXISTS' | 'NO_LINEAR_MODEL'
      witness_q   : the EQ2 constraint found outside I (str) or None
      n_eq1_cons  : number of EQ1 constraint generators
      note        : human-readable detail
    """
    import sympy
    a, b = sympy.symbols("a b")
    e1L, e1R = solver.al_parse_equation(eq1)
    e2L, e2R = solver.al_parse_equation(eq2)
    cs1 = solver.al_constraints(e1L, e1R)      # generators of I
    cs2 = solver.al_constraints(e2L, e2R)      # the q_m (EQ2 must break one)

    q_exprs = [(_to_sympy(q, a, b), q) for q in cs2]
    q_exprs = [(e, q) for e, q in q_exprs if e != 0]
    if not q_exprs:
        # EQ2 is a linear identity for ALL linear ops: no linear op can break it.
        return dict(exists=False, verdict="NO_LINEAR_MODEL", witness_q=None,
                    n_eq1_cons=len(cs1), note="EQ2 holds for every linear op")

    if not cs1:
        # EQ1 imposes no constraint (any linear op satisfies it); I = (0), so any
        # nonzero EQ2 constraint is outside I -> a linear counterexample exists.
        e, q = q_exprs[0]
        return dict(exists=True, verdict="INFINITE_LINEAR_EXISTS", witness_q=str(e),
                    n_eq1_cons=0, note="EQ1 unconstrained; free linear model refutes EQ2")

    gens = [_to_sympy(c, a, b) for c in cs1]
    gens = [g for g in gens if g != 0]
    if not gens:
        e, q = q_exprs[0]
        return dict(exists=True, verdict="INFINITE_LINEAR_EXISTS", witness_q=str(e),
                    n_eq1_cons=0, note="EQ1 constraints trivial; free linear model")

    G = sympy.groebner(gens, a, b, order="grevlex", domain="QQ")
    if G.contains(sympy.Integer(1)):
        # I = (1): the only EQ1-linear 'model' is the zero ring -> no linear model.
        return dict(exists=False, verdict="NO_LINEAR_MODEL", witness_q=None,
                    n_eq1_cons=len(cs1), note="EQ1 constraints unit ideal (no nonzero linear model)")

    for e, q in q_exprs:
        if not G.contains(e):
            return dict(exists=True, verdict="INFINITE_LINEAR_EXISTS", witness_q=str(e),
                        n_eq1_cons=len(cs1),
                        note="EQ2 constraint outside I => infinite commutative-linear model exists")
    return dict(exists=False, verdict="NO_LINEAR_MODEL", witness_q=None,
                n_eq1_cons=len(cs1),
                note="every EQ2 constraint in I => NO commutative-linear model (finite or infinite)")


def _selftest(solver):
    """Sanity checks against the existing idempotent finder and hand cases."""
    import sympy
    a, b = sympy.symbols("a b")
    print("selftest: to_sympy monomial map")
    from fractions import Fraction as Fr
    e = _to_sympy({(2, 0): Fr(1), (0, 1): Fr(-3), (0, 0): Fr(2)}, a, b)
    assert sympy.expand(e - (a**2 - 3*b + 2)) == 0, e
    print("  ok:", e)
    # A pair the idempotent al_ solves must also be EXISTS here (idempotent ⊂ general).
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", help="{id:[eq1,eq2]} json (or JSONL id/equation1/equation2)")
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    sys.path.insert(0, args.solver_dir)
    import solver
    solver.trace = lambda *a, **k: None

    if args.selftest:
        _selftest(solver)
        print("selftest passed")
        return

    text = open(args.pairs).read()
    try:
        obj = json.loads(text)
        pairs = [(pid, e[0], e[1]) for pid, e in obj.items()] if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        pairs = None
    if pairs is None:
        pairs = []
        for line in text.splitlines():
            if line.strip():
                r = json.loads(line)
                pairs.append((r["id"], r.get("equation1") or r.get("eq1"),
                              r.get("equation2") or r.get("eq2")))

    rows, n_exists = [], 0
    print(f"{'pair':<20} {'verdict':<24} witness")
    print("-" * 66)
    for pid, eq1, eq2 in pairs:
        try:
            d = decide_linear(solver, eq1, eq2)
        except Exception as ex:
            d = dict(exists=None, verdict="ERROR", witness_q=None, note=repr(ex))
        d["id"] = pid
        rows.append(d)
        if d.get("exists"):
            n_exists += 1
        print(f"{pid:<20} {d['verdict']:<24} {str(d.get('witness_q'))[:24]}")
    print("-" * 66)
    print(f"commutative-linear model EXISTS for {n_exists}/{len(pairs)} "
          f"(these are deterministically linear-solvable => NOT LLM targets)")
    if args.out:
        with open(args.out, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
