#!/usr/bin/env python3
"""Extract graduated SUPPORT for the trivial side, from Vampire's own proof.

The support ladder needs a tunable knob. Vampire's refutation of `x=y` passes through a
chain of derived equalities (superpositions of the law with itself): e.g.
    law  ->  f10  ->  op(x,y)=z (collapse)  ->  x=y.
Those intermediate lemmas ARE the waypoints. Revealing k of them, in derivation order, is
a continuous support dial: k=0 is the naked run, k=all hands the model the full path and it
only has to formalize the steps.

`lemmas(law)` returns the derived equalities as readable ◇-strings, earliest first.
"""
from __future__ import annotations
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et

VAMP = os.environ.get("VAMPIRE", "paper/bin/vampire")

# --- TPTP term (f/2, Xk vars) -> ◇ notation --------------------------------------
_TOK = re.compile(r"\s*(f|\(|\)|,|[A-Za-z]\w*)")

def _parse(s, i=0):
    m = _TOK.match(s, i); tok = m.group(1); i = m.end()
    if tok == "f":
        assert s[i] == "("; i += 1
        a, i = _parse(s, i)
        assert s[i] == ","; i += 1
        b, i = _parse(s, i)
        assert s[i] == ")"; i += 1
        return ("op", a, b), i
    return ("var", tok), i

_VMAP = {}
def _pp(node, names):
    if node[0] == "var":
        v = node[1]
        if v not in names:
            names[v] = "xyzwabcde"[len(names) % 9]
        return names[v]
    return f"({_pp(node[1],names)} ◇ {_pp(node[2],names)})"

def _tptp_eq_to_diamond(eqstr):
    l, r = eqstr.split("=", 1)
    lt, _ = _parse(l.strip()); rt, _ = _parse(r.strip())
    names = {}
    return f"{_pp(lt,names)} = {_pp(rt,names)}"


def lemmas(law, timeout=6):
    """Derived equalities along Vampire's collapse proof, earliest-first, deduped."""
    l, r, vs = et.tptp_eq_vars(law)
    body = f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\nfof(triv,conjecture,![X,Y]:(X=Y)).\n"
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False) as fh:
        fh.write(body); p = fh.name
    try:
        out = subprocess.run([VAMP, "--mode", "casc", "-p", "tptp", "-t", f"{timeout}s", p],
                             capture_output=True, text=True, timeout=timeout + 4).stdout
    except subprocess.TimeoutExpired:
        return []
    finally:
        os.unlink(p)
    got = []
    # plain steps that ARE an equality between f-terms, from superposition (the real waypoints)
    for m in re.finditer(r"fof\(f\d+,plain,\s*\(?\s*\(?\s*!?\s*\[[^\]]*\]\s*:\s*\(?(.+?)\)?\),?\s*"
                         r"inference\((\w+)", out, re.DOTALL):
        eq, rule = m.group(1).strip(), m.group(2)
        if rule not in ("superposition", "resolution", "forward_demodulation"):
            continue
        eq = re.sub(r"\s+", "", eq)
        if eq.count("=") != 1 or "!=" in eq or "$false" in eq:
            continue
        try:
            d = _tptp_eq_to_diamond(eq)
        except Exception:
            continue
        if d not in got:
            got.append(d)
    return got


if __name__ == "__main__":
    tests = [
        "x = ((((y ◇ w) ◇ z) ◇ ((y ◇ x) ◇ y)) ◇ y)",
        "x = (((y ◇ (w ◇ y)) ◇ ((x ◇ z) ◇ x)) ◇ y)",
        "x = (y ◇ ((x ◇ (z ◇ w)) ◇ (y ◇ (z ◇ z))))",
    ]
    for law in tests:
        ls = lemmas(law)
        print(f"\nLAW {law}\n  {len(ls)} waypoint lemmas:")
        for d in ls:
            print("   ", d[:90])
