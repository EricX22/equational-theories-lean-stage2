#!/usr/bin/env python3
"""The saturated set as an explicit model, by ORDERED rewriting (JRS Defs 1-2).

THE CORRECTION THIS FILE ENCODES
    We believed an active set containing equations with a free variable on each side
    (70 of 357 for law 12857) could not present a model. Wrong. That constraint is on
    JRS's *printer*, not on the construction:

      "we have modified Vampire and E to print the rewrite system on saturation,
       provided that every equation l ~ r is pre-ordered, i.e. l > r."

    The model (their Def 1) rewrites a ground term when the ground instance decreases,
    t[s(l)] -> t[s(r)] whenever s(l) > s(r), and: "If there are unbound variables on
    the other side of the equation, they can be mapped to any ground term such that
    s(l) > s(r), in practice the smallest constant."

    So: every equation is usable, in whichever direction decreases the instance.
    Termination is free because > is well-founded on ground terms. Ground confluence
    comes from saturation under unfailing completion. The model for 12857 and 33436
    is therefore computable today; what is missing is only an off-the-shelf CERTIFIER,
    because CSI/TTT2 check plain TRSs. Since `answer_spec.py` makes Lean the arbiter,
    CeTA was never on the critical path.

SOUNDNESS -- READ BEFORE QUOTING ANY OUTPUT
    Three claims, with different standing:

    (1) TERMINATION of `normalise` is guaranteed for any reduction ordering. Ours are
        LPO and a KBO; both are. This is unconditional.

    (2) GROUND CONFLUENCE is inherited from the saturation, and ONLY with respect to
        the ordering the prover saturated under. Evaluating with a different ordering
        than the prover used breaks it silently -- you still get normal forms, they
        just may not be canonical. This is the trap. `--check-ordering` reports the
        evidence; a cert carries `% saturated-with:` and this script refuses to
        evaluate unless the recorded flags match `--ordering`.

    (3) NONTRIVIALITY of the model: the two skolem constants of the `u != v` axiom
        must have distinct normal forms. That is a computation, reported by
        `--nontrivial`, not an assumption.

    So a passing run says: "under ordering O, which is the ordering the prover used,
    the saturated set normalises every sampled ground instance of the law to a common
    form, and separates the two constants." Ground confluence is *inherited*, not
    re-proved here. Re-proving it is the Lean contribution (PAPER_PLAN.md 5B) and it
    is exactly the case JRS leave open: unorientable equations, their 43, our ~36%.

USAGE
    python3 paper/scripts/ordered_model.py --selftest
    python3 paper/scripts/ordered_model.py --cert paper/certs/12857.sat \
        --law 'x = y ◇ ((x ◇ (y ◇ (z ◇ z))) ◇ y)' --ordering lpo \
        --verify-law --nontrivial --refute 'x ◇ y = y ◇ x' --check-ordering
"""
from __future__ import annotations
import argparse, itertools, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                              # noqa: E402

CAP = 20000


# ------------------------------------------------------------------ parsing ---
def active_clauses(text: str) -> list[str]:
    blk = text.split("SZS output start Saturation")[1].split("SZS output end Saturation")[0]
    return [c for _, c in re.findall(r"cnf\((\w+),\w+,\s*(.*?)\)\.\s*(?=\ncnf|\Z)", blk, re.S)]


def split_eq(clause: str):
    c = re.sub(r"\s+", "", clause)
    if "!=" in c or "|" in c:
        return None
    d = 0
    for i, ch in enumerate(c):
        d += ch == "("
        d -= ch == ")"
        if d == 0 and ch == "=":
            return c[:i], c[i + 1:]
    return None


def parse(s: str):
    toks, pos = re.findall(r"f|\(|\)|,|X\d+|sK\d+|c\d+", s), [0]

    def go():
        t = toks[pos[0]]; pos[0] += 1
        if t == "f":
            pos[0] += 1; l = go(); pos[0] += 1; r = go(); pos[0] += 1
            return ("op", l, r)
        return ("var", t) if t.startswith("X") else ("const", t)
    return go()


def load(path: str):
    txt = open(path).read()
    eqs = []
    for c in active_clauses(txt):
        e = split_eq(c)
        if e:
            eqs.append((parse(e[0]), parse(e[1])))
    m = re.search(r"% saturated-with:(.*)", txt)
    return eqs, (m.group(1).strip() if m else None)


# ----------------------------------------------------------------- orderings ---
def head(t):
    return "f" if t[0] == "op" else t[1]


def args(t):
    return [t[1], t[2]] if t[0] == "op" else []


def prec(sym: str) -> int:
    """Total precedence on symbols. f (arity 2) above all constants; constants by name.
    Matches Vampire's `--symbol_precedence arity` on this signature, where the only
    arity-0 symbols are the two skolems and any probe constants."""
    if sym == "f":
        return 10_000
    if sym.startswith("c"):
        return 1_000 + int(sym[1:])
    return int(sym[2:])                                  # sK0 -> 0, sK1 -> 1


def lpo_gt(s, t) -> bool:
    if s == t:
        return False
    if any(u == t or lpo_gt(u, t) for u in args(s)):
        return True
    ps, pt = prec(head(s)), prec(head(t))
    if ps > pt:
        return all(lpo_gt(s, u) for u in args(t))
    if ps < pt:
        return False
    for a, b in zip(args(s), args(t)):
        if a == b:
            continue
        return lpo_gt(a, b) and all(lpo_gt(s, u) for u in args(t))
    return False


def size(t) -> int:
    return 1 if t[0] != "op" else 1 + size(t[1]) + size(t[2])


def kbo_gt(s, t) -> bool:
    """KBO with all weights 1 (Vampire's default on a signature with no unary symbols;
    the variable condition is vacuous on ground terms)."""
    if s == t:
        return False
    ws, wt = size(s), size(t)
    if ws != wt:
        return ws > wt
    ps, pt = prec(head(s)), prec(head(t))
    if ps != pt:
        return ps > pt
    for a, b in zip(args(s), args(t)):
        if a != b:
            return kbo_gt(a, b)
    return False


ORDERINGS = {"lpo": lpo_gt, "kbo": kbo_gt}


# ------------------------------------------------------- ordered rewriting ---
def vars_(t):
    return set() if t[0] == "const" else {t[1]} if t[0] == "var" else vars_(t[1]) | vars_(t[2])


def match(p, t, s):
    if p[0] == "var":
        if p[1] in s:
            return s if s[p[1]] == t else None
        s = dict(s); s[p[1]] = t
        return s
    if p[0] == "const":
        return s if t == p else None
    if t[0] != "op":
        return None
    a = match(p[1], t[1], s)
    return match(p[2], t[2], a) if a is not None else None


def apply(t, s):
    if t[0] == "var":
        return s[t[1]]
    if t[0] == "const":
        return t
    return ("op", apply(t[1], s), apply(t[2], s))


def smallest_const(eqs):
    """JRS: unbound variables on the far side go to 'the smallest constant'."""
    cs = set()

    def walk(t):
        if t[0] == "const":
            cs.add(t[1])
        elif t[0] == "op":
            walk(t[1]); walk(t[2])
    for l, r in eqs:
        walk(l); walk(r)
    return ("const", min(cs, key=prec)) if cs else ("const", "sK0")


def rewrite_top(t, eqs, gt, small):
    for l, r in eqs:
        for a, b in ((l, r), (r, l)):                   # both directions
            s = match(a, t, {})
            if s is None:
                continue
            s2 = dict(s)
            s2.update({v: small for v in vars_(b) - set(s)})
            lhs, rhs = apply(a, s2), apply(b, s2)
            if gt(lhs, rhs):                             # only if the instance decreases
                return rhs
    return None


def normalise(t, eqs, gt, small, cap=CAP):
    n = [0]

    def step(u):
        if n[0] > cap:
            raise TimeoutError("step cap")
        v = rewrite_top(u, eqs, gt, small)
        if v is not None:
            n[0] += 1
            return v, True
        if u[0] == "op":
            a, ch = step(u[1])
            if ch:
                return ("op", a, u[2]), True
            b, ch = step(u[2])
            if ch:
                return ("op", u[1], b), True
        return u, False

    ch = True
    while ch:
        t, ch = step(t)
    return t, n[0]


# ------------------------------------------------------------------- checks ---
def ground_law(law, sub):
    l, r = et.parse_equation(law)

    def conv(a):
        return sub[a[1]] if a[0] == "var" else ("op", conv(a[1]), conv(a[2]))
    return conv(l), conv(r)


def verify_law(law, eqs, gt, small, carrier):
    """Every ground instance of the law must join. NON-VACUITY IS CHECKED: at least one
    side must actually rewrite, else we are 'confirming' a rule that never fired --
    the exact mistake recorded in HISTORY.md."""
    vs = sorted({v for t in et.parse_equation(law) for v in et.variables(t)})
    ok = bad = fired = capped = 0
    for vals in itertools.product(carrier, repeat=len(vs)):
        L, R = ground_law(law, dict(zip(vs, vals)))
        try:
            nl, sl = normalise(L, eqs, gt, small)
            nr, sr = normalise(R, eqs, gt, small)
        except TimeoutError:
            capped += 1
            continue
        fired += (sl + sr) > 0
        ok += nl == nr
        bad += nl != nr
    return ok, bad, fired, capped


def refutes(probe, eqs, gt, small):
    l, r = et.parse_equation(probe)
    vs = sorted(set(et.variables(l)) | set(et.variables(r)))
    sub = {v: ("const", f"c{i}") for i, v in enumerate(vs)}

    def conv(a):
        return sub[a[1]] if a[0] == "var" else ("op", conv(a[1]), conv(a[2]))
    nl, _ = normalise(conv(l), eqs, gt, small)
    nr, _ = normalise(conv(r), eqs, gt, small)
    return nl != nr


def check_ordering(eqs, gt):
    """Necessary, not sufficient. Every PRE-ORDERED equation (same variables on both
    sides) should be comparable under the prover's ordering. Many incomparables means
    our ordering is not the prover's, and ground confluence does not transfer."""
    same = comp = 0
    for l, r in eqs:
        if vars_(l) != vars_(r):
            continue
        same += 1
        gl, gr = apply(l, {v: ("const", "sK0") for v in vars_(l)}), \
                 apply(r, {v: ("const", "sK0") for v in vars_(r)})
        comp += gl == gr or gt(gl, gr) or gt(gr, gl)
    return comp, same


def selftest():
    ok = True
    # a > b, f(a,b) > a, and LPO/KBO agree on these
    a, b = ("const", "sK0"), ("const", "sK1")
    for name, gt in ORDERINGS.items():
        c1 = gt(b, a) and not gt(a, b)
        c2 = gt(("op", a, b), a) and gt(("op", a, b), b)
        c3 = not gt(a, a)
        ok &= c1 and c2 and c3
        print(f"  {name}: total on consts, subterm property, irreflexive "
              f"{'OK' if c1 and c2 and c3 else 'FAIL'}")

    # A one-rule system: f(x,x) ~ x. Normalises f(a,a) -> a, does not loop.
    eqs = [(("op", ("var", "X0"), ("var", "X0")), ("var", "X0"))]
    nf, steps = normalise(("op", a, a), eqs, lpo_gt, a)
    c = nf == a and steps == 1
    ok &= c; print(f"  ordered rewriting fires {'OK' if c else 'FAIL'}")

    # Extra variable on the RHS: f(x,x) ~ f(x,y). Must instantiate y := smallest const
    # and only rewrite in the decreasing direction; must terminate.
    eqs = [(("op", ("var", "X0"), ("var", "X0")), ("op", ("var", "X0"), ("var", "X1")))]
    try:
        nf, steps = normalise(("op", b, b), eqs, lpo_gt, a)
        c = True
    except TimeoutError:
        c = False
    ok &= c; print(f"  extra-var eq terminates {'OK' if c else 'FAIL'}")

    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert")
    ap.add_argument("--law")
    ap.add_argument("--ordering", choices=sorted(ORDERINGS), default="kbo")
    ap.add_argument("--verify-law", action="store_true")
    ap.add_argument("--nontrivial", action="store_true")
    ap.add_argument("--refute", action="append", default=[])
    ap.add_argument("--check-ordering", action="store_true")
    ap.add_argument("--force", action="store_true", help="evaluate despite an ordering mismatch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest())

    eqs, flags = load(a.cert)
    gt = ORDERINGS[a.ordering]
    small = smallest_const(eqs)
    print(f"{os.path.basename(a.cert)}: {len(eqs)} equations, ordering={a.ordering}, "
          f"smallest constant={small[1]}")

    if flags is None:
        print("  WARNING: cert has no `% saturated-with:` header. Ground confluence "
              "transfers only if this ordering is the prover's. Regenerate the cert.")
    elif f"-to {a.ordering}" not in flags and not (a.ordering == "kbo" and "-to " not in flags):
        msg = f"  ORDERING MISMATCH: cert saturated with `{flags}`, evaluating with {a.ordering}"
        if not a.force:
            print(msg + "\n  refusing (pass --force to evaluate anyway; output is not sound)")
            sys.exit(2)
        print(msg + "  [--force]")

    if a.check_ordering:
        comp, same = check_ordering(eqs, gt)
        print(f"  pre-ordered equations comparable: {comp}/{same}"
              f"{'  <- mismatch suspected' if same and comp < same else ''}")

    if a.verify_law:
        carrier = [("const", "sK0"), ("const", "sK1"),
                   ("op", ("const", "sK0"), ("const", "sK1"))]
        ok, bad, fired, capped = verify_law(a.law, eqs, gt, small, carrier)
        print(f"  law holds on ground instances: {ok}/{ok + bad}"
              f"   (rewrites fired in {fired}; step-cap hit {capped})")
        if fired == 0:
            print("  VACUOUS: no rule ever fired. See HISTORY.md.")

    if a.nontrivial:
        nl, _ = normalise(("const", "sK0"), eqs, gt, small)
        nr, _ = normalise(("const", "sK1"), eqs, gt, small)
        print(f"  nontrivial (sK0 !~ sK1): {nl != nr}")

    for p in a.refute:
        print(f"  refutes {p!r}: {refutes(p, eqs, gt, small)}")


if __name__ == "__main__":
    main()
