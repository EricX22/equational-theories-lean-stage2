#!/usr/bin/env python3
"""Shared term parsing + emitters for ETP magma equations.

ETP problem rows give equations over a single binary op `◇` and variables
(single letters), e.g. "x = x ◇ (x ◇ ((y ◇ z) ◇ x))". This module parses them
and emits TPTP (for Vampire/E) and LADR (for Prover9/Mace4). No solver imports.
"""
from __future__ import annotations

OP = "◇"


# --- AST: ("var", name) | ("op", left, right) -----------------------------
class _P:
    def __init__(self, s: str):
        self.toks = []
        for ch in s:
            if ch.isspace():
                continue
            if ch == OP or ch in "()":
                self.toks.append(ch)
            elif ch.isalpha():
                self.toks.append(ch)
            else:
                raise ValueError(f"unexpected char {ch!r} in {s!r}")
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def nxt(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def atom(self):
        t = self.nxt()
        if t == "(":
            e = self.expr()
            if self.nxt() != ")":
                raise ValueError("expected )")
            return e
        if t.isalpha():
            return ("var", t)
        raise ValueError(f"unexpected token {t!r}")

    def expr(self):
        left = self.atom()
        while self.peek() == OP:
            self.nxt()
            left = ("op", left, self.atom())  # left-associative
        return left


def parse_term(s: str):
    p = _P(s)
    t = p.expr()
    if p.peek() is not None:
        raise ValueError(f"trailing tokens in {s!r}")
    return t


def parse_equation(eq: str):
    if eq.count("=") != 1:
        raise ValueError(f"expected one '=' in {eq!r}")
    lhs, rhs = eq.split("=")
    return parse_term(lhs), parse_term(rhs)


def variables(ast, acc=None):
    acc = acc if acc is not None else []
    if ast[0] == "var":
        if ast[1] not in acc:
            acc.append(ast[1])
    else:
        variables(ast[1], acc)
        variables(ast[2], acc)
    return acc


# --- TPTP (Vampire, E): f/2, uppercase vars -------------------------------
def to_tptp(ast) -> str:
    if ast[0] == "var":
        return ast[1].upper()
    return f"f({to_tptp(ast[1])},{to_tptp(ast[2])})"


def tptp_eq_vars(eq: str):
    l, r = parse_equation(eq)
    vs = sorted({v.upper() for v in variables(l) + variables(r)})
    return to_tptp(l), to_tptp(r), vs


def tptp_true(eq1: str, eq2: str) -> str:
    """Prove eq1 |= eq2."""
    l1, r1, v1 = tptp_eq_vars(eq1)
    l2, r2, v2 = tptp_eq_vars(eq2)
    q1 = f"! [{','.join(v1)}] : " if v1 else ""
    q2 = f"! [{','.join(v2)}] : " if v2 else ""
    return (f"fof(hyp,  axiom,      {q1}( {l1} = {r1} )).\n"
            f"fof(goal, conjecture, {q2}( {l2} = {r2} )).\n")


def tptp_false(eq1: str, eq2: str) -> str:
    """Find a counterexample magma: eq1 holds, eq2 fails somewhere."""
    l1, r1, v1 = tptp_eq_vars(eq1)
    l2, r2, v2 = tptp_eq_vars(eq2)
    q1 = f"! [{','.join(v1)}] : " if v1 else ""
    q2 = f"? [{','.join(v2)}] : " if v2 else ""
    return (f"fof(hyp, axiom,             {q1}( {l1} = {r1} )).\n"
            f"fof(neg, negated_conjecture, {q2}( {l2} != {r2} )).\n")


# --- LADR (Prover9, Mace4): * op, lowercase vars are variables ------------
def to_ladr(ast) -> str:
    if ast[0] == "var":
        return ast[1]  # lowercase letter -> LADR variable
    return f"({to_ladr(ast[1])} * {to_ladr(ast[2])})"


def ladr_eq(eq: str) -> str:
    l, r = parse_equation(eq)
    return f"{to_ladr(l)} = {to_ladr(r)}"


def ladr_input(eq1: str, eq2: str) -> str:
    """Prover9 proves / Mace4 refutes the same file: assumption eq1, goal eq2.

    Prover9 -> proof of goal means TRUE; Mace4 -> model (assumption holds, goal
    fails) means FALSE (the model is the counterexample magma).
    """
    return ("formulas(assumptions).\n"
            f"  {ladr_eq(eq1)}.\n"
            "end_of_list.\n\n"
            "formulas(goals).\n"
            f"  {ladr_eq(eq2)}.\n"
            "end_of_list.\n")


if __name__ == "__main__":  # tiny self-test
    e1, e2 = "x = y ◇ x", "x = x ◇ (x ◇ ((y ◇ z) ◇ x))"
    print(tptp_true(e1, e2))
    print(tptp_false(e1, e2))
    print(ladr_input(e1, e2))
