#!/usr/bin/env python3
"""Structured-ansatz search: the symbolic half of the neurosymbolic constructor.

The LLM proposes a NON-LINEAR *family* of operations (an ansatz) with a few free
parameters -- e.g. "op(x,y) = P[0][x]" for a permutation P[0], or a small
perturbation of right-projection with an integer offset. This module then
EXHAUSTIVELY searches the (bounded) parameter space, materialises each concrete
table, and self-verifies EQ1-and-not-EQ2. Neither half suffices alone: the space
of raw non-linear tables is far too large to brute (Fin>8 is out of reach), and
the LLM can't reliably emit a fully-correct table -- but the LLM can name the
family and the solver can exhaust it.

Sound by construction: only a table that actually satisfies EQ1 and refutes EQ2
is returned; a bad ansatz simply yields nothing.

Param spec (list, one entry per element of the tuple P passed to op):
  {"int": [lo, hi]}  -> integer in range(lo, hi); lo/hi may be the string "n"
  {"perm": true}     -> a permutation of range(n) (a tuple)

op_code must define:  def op(x, y, n, P): -> int   (reduced mod n by the caller)
"""
from __future__ import annotations
import math
import time
from itertools import permutations, product


def _domain(spec, n):
    if spec.get("perm"):
        return list(permutations(range(n)))
    lo, hi = spec["int"]
    lo = n if lo == "n" else int(lo)
    hi = n if hi == "n" else int(hi)
    return list(range(lo, hi))


def _space_size(params, n):
    total = 1
    for p in params:
        if p.get("perm"):
            total *= math.factorial(n)
        else:
            lo, hi = p["int"]
            lo = n if lo == "n" else int(lo)
            hi = n if hi == "n" else int(hi)
            total *= max(1, hi - lo)
    return total


def search_structured(solver, eq1, eq2, op_code, params, candidate_n,
                      budget=300_000, deadline=None):
    """Search the ansatz's parameter space.

    Returns (hit, reason) where hit is (n, table, P) or None, and reason is a
    human-readable diagnosis when hit is None -- distinguishing a family that
    can't satisfy EQ1, a family that's too strong (also satisfies EQ2), a
    parameter space skipped as over-budget, and a buggy op_code. That diagnosis
    is fed back to the LLM so it corrects the right thing."""
    v1, l1, r1 = solver.parse_equation(eq1)
    v2, l2, r2 = solver.parse_equation(eq2)
    ns = {"math": math}
    exec(op_code, ns)
    if "op" not in ns:
        raise ValueError("op_code did not define op(x, y, n, P)")
    op_fn = ns["op"]

    eq1_ever = False       # some parameter made EQ1 hold
    searched_any = False   # at least one n was actually searched (under budget)
    skipped = []           # (n, space_size) skipped as over-budget
    op_errors = 0
    for n in candidate_n:
        n = int(n)
        if n < 2 or n > 40:
            continue
        size = _space_size(params, n)
        if size > budget:
            skipped.append((n, size))
            continue
        searched_any = True
        doms = [_domain(p, n) for p in params]
        for combo in product(*doms) if doms else [()]:
            if deadline is not None and time.time() > deadline:
                return None, "search timed out before covering the parameter space"
            P = tuple(combo)
            try:
                table = [[op_fn(x, y, n, P) % n for y in range(n)] for x in range(n)]
            except Exception:
                op_errors += 1
                break  # op_code errors at this n; skip to next n
            op = lambda a, b, t=table: t[a][b]
            if solver.equation_holds(v1, l1, r1, n, op):
                eq1_ever = True
                if not solver.equation_holds(v2, l2, r2, n, op):
                    return (n, table, P), "ok"

    if op_errors and not searched_any:
        reason = "op_code crashed for every candidate n; fix op(x,y,n,P) to return an int"
    elif not searched_any and skipped:
        reason = ("parameter space too large at EVERY n (skipped %s); it was NOT searched. "
                  "Shrink the params (fewer/smaller ranges, at most one permutation) or use "
                  "smaller n." % [s[0] for s in skipped])
    elif not eq1_ever:
        reason = ("searched, but NO parameter made EQ1 hold -- this family structurally cannot "
                  "satisfy EQ1. Propose a different family.")
    else:
        reason = ("searched, but every parameter that satisfied EQ1 ALSO satisfied EQ2 (family "
                  "too strong). Adjust the family so it can break EQ2.")
    if skipped and searched_any:
        reason += " (note: sizes %s were skipped as over-budget)" % [s[0] for s in skipped]
    return None, reason
