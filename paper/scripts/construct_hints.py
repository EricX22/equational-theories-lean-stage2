#!/usr/bin/env python3
"""Graduated SUPPORT for the construction (Austin) side, from Vampire's saturation.

Parallel to trivial_hints.py. For an AUSTIN_PROVEN law, `vampire -sa otter` saturates
`{law, ∃a≠b}` and prints the saturated clause set — a ground-truth presentation `E` of a
nontrivial model. Those equations are the reveal-support: hand the model k of them and it
must complete an `E` that certifies (llm_construct.certify). Smaller/simpler equations
first, so early reveals are the most fundamental consequences.

`equations(law)` -> ordered list of saturated equations as ◇-strings (excludes `sK0≠sK1`).
`injective_subterm(law)` -> the (i)-certificate subterm S (the successor-like map), if free.
"""
from __future__ import annotations
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et
from trivial_hints import _tptp_eq_to_diamond          # TPTP f/2 term -> ◇ notation

VAMP = os.environ.get("VAMPIRE", "paper/bin/vampire")


def equations(law, timeout=10):
    l, r, vs = et.tptp_eq_vars(law)
    body = (f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\n"
            "fof(nt,axiom,?[U,V]: U != V).\n")
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False) as fh:
        fh.write(body); p = fh.name
    try:
        out = subprocess.run([VAMP, "-sa", "otter", "--show_active", "on",
                              "-t", f"{timeout}s", p], capture_output=True, text=True,
                             timeout=timeout + 4).stdout
    except subprocess.TimeoutExpired:
        return []
    finally:
        os.unlink(p)
    m = re.search(r"SZS output start Saturation\.(.*?)SZS output end Saturation", out, re.DOTALL)
    if not m:
        return []
    eqs = []
    for cm in re.finditer(r"cnf\([^,]+,[^,]+,\s*(.+?)\)\.", m.group(1), re.DOTALL):
        clause = re.sub(r"\s+", "", cm.group(1))
        if clause.count("=") != 1 or "!=" in clause:      # skip sK0 != sK1
            continue
        try:
            d = _tptp_eq_to_diamond(clause)
        except Exception:
            continue
        if d not in eqs:
            eqs.append(d)
    eqs.sort(key=len)                                     # simplest first
    return eqs


def injective_subterm(law):
    """The (i)-cert's syntactically-free injective subterm S of T (contains every x),
    as a ◇-string — the 'successor-like' map that forces infinity. Best-effort."""
    try:
        import prove_status as ps
        _, T = ps.et.parse(law) if hasattr(ps, "et") else (None, None)
    except Exception:
        T = None
    # Fall back to a self-contained computation on our own AST.
    try:
        rhs = et.parse_term(law.split("=", 1)[1])
    except Exception:
        return None
    # subterm on the path from root to the LCA of all x-occurrences that still contains every x
    def occ(node, v):
        return 0 if node[0] == "var" and node[1] != v else (
            1 if node[0] == "var" else occ(node[1], v) + occ(node[2], v))
    total_x = occ(rhs, "x")
    if total_x == 0:
        return None
    node = rhs
    while node[0] == "op":
        lx, rx = occ(node[1], "x"), occ(node[2], "x")
        if lx == total_x:
            node = node[1]
        elif rx == total_x:
            node = node[2]
        else:
            break
    if node is rhs or node[0] == "var":
        return None
    names = {}
    def pp(n):
        if n[0] == "var":
            return n[1]
        return f"({pp(n[1])} ◇ {pp(n[2])})"
    return pp(node)


if __name__ == "__main__":
    tests = [
        "x = ((((y ◇ y) ◇ z) ◇ x) ◇ x) ◇ z",
        "x = (y ◇ ((x ◇ x) ◇ y)) ◇ (z ◇ z)",
    ]
    for law in tests:
        eqs = equations(law)
        S = injective_subterm(law)
        print(f"\nLAW {law}")
        print(f"  injective subterm S = {S}")
        print(f"  {len(eqs)} saturated equations (reveal-support, simplest first):")
        for e in eqs:
            print("   ", e[:88])
