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
    """Search the ansatz's parameter space. Returns (n, table, P) or None.
    `info` about skipped sizes is available via the returned tuple's absence +
    the `skipped` list this function attaches to itself is avoided; callers that
    want detail should pass a small budget and inspect return value."""
    v1, l1, r1 = solver.parse_equation(eq1)
    v2, l2, r2 = solver.parse_equation(eq2)
    ns = {"math": math}
    exec(op_code, ns)
    if "op" not in ns:
        raise ValueError("op_code did not define op(x, y, n, P)")
    op_fn = ns["op"]

    for n in candidate_n:
        n = int(n)
        if n < 2 or n > 40:
            continue
        if _space_size(params, n) > budget:
            continue  # parameter space too large at this n; caller should tighten
        doms = [_domain(p, n) for p in params]
        for combo in product(*doms) if doms else [()]:
            if deadline is not None and time.time() > deadline:
                return None
            P = tuple(combo)
            try:
                table = [[op_fn(x, y, n, P) % n for y in range(n)] for x in range(n)]
            except Exception:
                break  # op_code errors at this n; skip to next n
            op = lambda a, b, t=table: t[a][b]
            if (solver.equation_holds(v1, l1, r1, n, op)
                    and not solver.equation_holds(v2, l2, r2, n, op)):
                return n, table, P
    return None
