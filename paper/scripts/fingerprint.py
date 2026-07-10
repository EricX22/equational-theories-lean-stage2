#!/usr/bin/env python3
"""Fingerprint laws into candidate equivalence classes, cheaply, before pairwise.

WHY THIS EXISTS
    Pairwise mutual implication over the hard tier is ~5.9M pairs / ~12M prover calls
    (3,428 laws). That is days. This script computes a per-law fingerprint in one pass
    (O(N)), buckets by it, and emits only the pairs that must actually be decided by a
    prover. See PAPER_PLAN.md §5D.

THE INVARIANTS — AND THE MEASUREMENT THAT KILLED TWO OF THEM

    Logically equivalent laws have exactly the same models. So any function of a law's
    model class is an equivalence invariant, and two laws with different values are
    CERTAINLY inequivalent. The obvious cheap choices do not work here, and the reason
    is worth understanding before anyone rebuilds them.

    (1) finite-magma satisfaction (`--exact`, off by default). A fixed seeded sample
        of magmas; does L hold in each? Exact, prover-free, and **empirically
        useless**: measured 2026-07-09 over 247 AUSTIN_PROVEN + 400 NO_FINITE_MODEL +
        400 HAS_FINITE_MODEL laws, the vector is **all-zero for every single law** —
        one bucket, zero separation. A random magma satisfying a specific 4-variable
        order-5+ law is astronomically unlikely, and Austin laws have no nontrivial
        finite models at all. Sampled-structure fingerprints are hopeless on this
        corpus.

    (2) affine-Z satisfaction (`--exact`, off by default). x∘y = a·x + b·y + c over Z
        is infinite, so an Austin law *might* satisfy one. Measured: **all-zero for
        all 1,047 laws** at |a|,|b| ≤ 3, |c| ≤ 1. Same failure, same reason.

    (3) prover-proved probe vector — the only component with signal, and NOT an
        invariant. For a fixed probe set P, record which p ∈ P are proved from L
        within `budget`. Entailment is semi-decidable in the positive direction only,
        so a coordinate reads Y (proved) or U (unknown-or-false), never a certified N.
        Two equivalent laws can land on different vectors — one proved p in 0.9s, the
        other needed 1.1s.

    (4) model-refutation (`--model-refute`). The missing N-channel. If we hold a
        rewrite system presenting a model of L, we can *refute* L ⊨ p: skolemise p's
        variables to fresh constants, normalise both sides, and if the normal forms
        differ then p fails in that model, so L ⊭ p. Certified N, prover-free.

    WHY (4) IS THE WHOLE STORY, AND WHY IT IS NOT FREE.
    Refuting L ⊨ p requires a model of L in which p fails. On the hard tier *every*
    model of L is infinite, so the only available one is the saturation-derived
    rewrite system — and reading distinct normal forms as distinct elements is valid
    only if that system is **convergent**, which is precisely what CSI/TTT2/CeTA
    certify. So:

        the equivalence-class count and the countermodel certification are the
        same bottleneck.

    For 4916 (4 active clauses, all orientable) the channel works. For 12857 and 33436
    the saturated sets have 70 / 69 equations with extra variables on both sides and
    are not term rewrite systems at all, so (4) is unavailable there. Run with
    `--assume-convergent` to use (4) before certification — the output is then a
    conjecture, not a theorem, and is labelled as such.

    CONSEQUENCE, STATED BLUNTLY. With only Y and U, buckets can WRONGLY SPLIT an
    equivalence class; they can never wrongly merge one, because every within-bucket
    pair is decided by the prover afterwards. So the class count is an UPPER BOUND
    that shrinks with compute. That is the wrong direction of error for a headline
    number: we would be over-claiming corpus size. Report it as an upper bound with
    the budget attached, and say so in the paper. Every certified N tightens it.

    Mitigation: `--hamming d` also emits cross-bucket pairs whose probe vectors differ
    in at most d coordinates. Wrong splits from prover flakiness are almost always at
    small Hamming distance. d=0 trusts the buckets; d=2 is cheap insurance. It
    shrinks, but does not close, the over-estimate.

    ACTION ITEM FOR prove_status.py: it does not persist finite models — the `witness`
    field holds the (i)-prover's injective subterm, not a magma. Persisting the FMB
    model for HAS_FINITE_MODEL laws would give channel (4) for free on the easy tiers,
    where it needs no certification at all.

USAGE
    python3 paper/scripts/fingerprint.py --selftest --vampire paper/bin/vampire
    python3 paper/scripts/fingerprint.py \
        --in 'paper/results/final_status.jsonl' --status NO_FINITE_MODEL \
        --vampire paper/bin/vampire --budget 1 --hamming 2 \
        --out paper/results/fp.jsonl --pairs-out paper/results/fp_pairs.jsonl

    Then decide the emitted pairs (both directions) with a real budget, union-find the
    proved equivalences, and report `classes` as an upper bound.

SHARDING: `--shard i/N` splits by law index; outputs append. Never open your own
output with "w" — sibling shards read it back via --skip. (See HISTORY.md.)
"""
from __future__ import annotations
import argparse, glob, itertools, json, os, random, sys, time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                    # noqa: E402
from prove_status import _run, _proved                    # noqa: E402

# --------------------------------------------------------------------------
# Fixed and never to be changed once a corpus has been fingerprinted with it.
# Changing any constant below invalidates every stored fingerprint.
MAGMA_SEED = 20260709
MAGMA_SIZES = (2, 3, 4)
MAGMA_SAMPLES = {2: 16, 3: 24, 4: 24}      # size 2 is exhaustive (2^4 = 16)
AFFINE_RANGE = range(-3, 4)                # a, b
AFFINE_CONST = range(-1, 2)               # c

DEFAULT_PROBES = [
    "x = y",                                  # Eq2: triviality
    "x ◇ x = x",                              # idempotence
    "x ◇ y = y ◇ x",                          # commutativity
    "(x ◇ y) ◇ z = x ◇ (y ◇ z)",              # associativity
    "x ◇ y = x",                              # left projection
    "x ◇ y = y",                              # right projection
    "x ◇ (x ◇ y) = y",
    "(x ◇ y) ◇ y = x",
    "x ◇ (y ◇ x) = x",
    "x ◇ (y ◇ y) = x",
    "(x ◇ x) ◇ y = y",
    "x ◇ (x ◇ x) = x",
    "(x ◇ x) ◇ x = x",
    "x ◇ (y ◇ z) = (x ◇ y) ◇ (x ◇ z)",
    "(x ◇ y) ◇ z = (x ◇ z) ◇ (y ◇ z)",
    "x ◇ y = y ◇ (x ◇ y)",
    "x ◇ (y ◇ z) = y ◇ (x ◇ z)",
    "(x ◇ y) ◇ (y ◇ z) = y",
    "x ◇ (x ◇ (x ◇ y)) = y",
    "((x ◇ y) ◇ y) ◇ y = x",
    "x = x ◇ (y ◇ (x ◇ y))",
    "x = (y ◇ x) ◇ (x ◇ y)",
    "x ◇ (y ◇ z) = (y ◇ x) ◇ z",
    "x ◇ (y ◇ y) = y ◇ (x ◇ x)",
]


# ------------------------------------------------------------- (1) magmas ---
def _magmas():
    """Deterministic magma sample. Same tables for every law, forever."""
    rng = random.Random(MAGMA_SEED)
    out = []
    for n in MAGMA_SIZES:
        if n == 2:                                        # exhaustive
            for bits in range(16):
                out.append((n, [(bits >> (2 * i + j)) & 1 for i in range(n)
                                for j in range(n)]))
        else:
            for _ in range(MAGMA_SAMPLES[n]):
                out.append((n, [rng.randrange(n) for _ in range(n * n)]))
    return out


def _eval_finite(ast, env, n, tab):
    if ast[0] == "var":
        return env[ast[1]]
    return tab[_eval_finite(ast[1], env, n, tab) * n + _eval_finite(ast[2], env, n, tab)]


def holds_finite(lhs, rhs, vs, n, tab):
    for vals in itertools.product(range(n), repeat=len(vs)):
        env = dict(zip(vs, vals))
        if _eval_finite(lhs, env, n, tab) != _eval_finite(rhs, env, n, tab):
            return False
    return True


# ------------------------------------------------------------- (2) affine ---
def _eval_affine(ast, a, b, c):
    """Value as a linear form: (coeff dict over vars, constant)."""
    if ast[0] == "var":
        return ({ast[1]: 1}, 0)
    lc, lk = _eval_affine(ast[1], a, b, c)
    rc, rk = _eval_affine(ast[2], a, b, c)
    out = defaultdict(int)
    for v, k in lc.items():
        out[v] += a * k
    for v, k in rc.items():
        out[v] += b * k
    return ({v: k for v, k in out.items() if k}, a * lk + b * rk + c)


def holds_affine(lhs, rhs, a, b, c):
    return _eval_affine(lhs, a, b, c) == _eval_affine(rhs, a, b, c)


# --------------------------------------------- (4) saturation-model refute ---
def _parse_cnf(sat_path):
    """Active clauses of a `-sa otter --show_active on` certificate."""
    import re
    txt = open(sat_path).read()
    blk = txt.split("SZS output start Saturation")[1].split("SZS output end Saturation")[0]
    return [c for _, c in re.findall(r"cnf\((\w+),\w+,\s*(.*?)\)\.\s*(?=\ncnf|\Z)", blk, re.S)]


def _split_eq(clause):
    import re
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


def _tokenise(s):
    import re
    return re.findall(r"f|\(|\)|,|X\d+|sK\d+|[a-z]\w*", s)


def _parse_tptp(s):
    toks, pos = _tokenise(s), [0]

    def go():
        t = toks[pos[0]]; pos[0] += 1
        if t == "f":
            pos[0] += 1                      # (
            l = go(); pos[0] += 1            # ,
            r = go(); pos[0] += 1            # )
            return ("op", l, r)
        return ("var", t) if t.startswith("X") else ("const", t)
    return go()


def rules_from_sat(sat_path):
    """Orient the active set into a TRS. Returns (rules, n_unorientable).

    A clause is a rule only if one side's variables contain the other's. Equations
    with extra variables on BOTH sides — 70 of 357 for law 12857 — are not rules in
    either direction, and their presence means the model is NOT presented by a TRS.
    """
    rules, bad = [], 0
    for c in _parse_cnf(sat_path):
        eq = _split_eq(c)
        if not eq:
            continue
        L, R = (_parse_tptp(x) for x in eq)
        vl, vr = _vars(L), _vars(R)
        if vr <= vl and vl <= vr:                  # same vars: orient by size
            rules.append((L, R) if _size(R) <= _size(L) else (R, L))
        elif vr <= vl:
            rules.append((L, R))
        elif vl <= vr:
            rules.append((R, L))
        else:                                       # extra vars on BOTH sides
            bad += 1
    return rules, bad


def _vars(t):
    return {t[1]} if t[0] == "var" else set() if t[0] == "const" else _vars(t[1]) | _vars(t[2])


def _size(t):
    return 1 if t[0] in ("var", "const") else 1 + _size(t[1]) + _size(t[2])


def _match(pat, term, sub):
    if pat[0] == "var":
        if pat[1] in sub:
            return sub if sub[pat[1]] == term else None
        sub = dict(sub); sub[pat[1]] = term
        return sub
    if pat[0] == "const":
        return sub if term == pat else None
    if term[0] != "op":
        return None
    s = _match(pat[1], term[1], sub)
    return _match(pat[2], term[2], s) if s is not None else None


def _apply(t, sub):
    if t[0] == "var":
        return sub.get(t[1], t)
    if t[0] == "const":
        return t
    return ("op", _apply(t[1], sub), _apply(t[2], sub))


def normalise(t, rules, cap=20000):
    steps = [0]

    def step(u):
        if steps[0] > cap:
            raise TimeoutError
        for L, R in rules:
            s = _match(L, u, {})
            if s is not None:
                steps[0] += 1
                return _apply(R, s), True
        if u[0] == "op":
            a, ch = step(u[1])
            if ch:
                return ("op", a, u[2]), True
            b, ch = step(u[2])
            if ch:
                return ("op", u[1], b), True
        return u, False

    changed = True
    while changed:
        t, changed = step(t)
    return t


def model_refutes(rules, probe):
    """True iff probe provably FAILS in the model presented by `rules`.

    Sound only if `rules` is convergent — i.e. after CSI/TTT2/CeTA. Skolemise the
    probe's variables to fresh constants; distinct normal forms => distinct elements
    => the probe fails => L does not entail it.
    """
    l, r = et.parse_equation(probe)
    vs = sorted(set(et.variables(l)) | set(et.variables(r)))
    sub = {v: ("const", f"c{i}") for i, v in enumerate(vs)}

    def conv(a):
        return sub[a[1]] if a[0] == "var" else ("op", conv(a[1]), conv(a[2]))
    try:
        return normalise(conv(l), rules) != normalise(conv(r), rules)
    except (TimeoutError, RecursionError):
        return False                                   # no verdict, stay at U


# -------------------------------------------------------------- (3) probes ---
def probe_vector(law, probes, vbin, budget, rules=None):
    """Ternary: Y = proved, N = refuted in an extracted model, U = neither."""
    bits = []
    for p in probes:
        if _proved(_run(vbin, ["--mode", "casc"], et.tptp_true(law, p), budget)):
            bits.append("Y")
        elif rules and model_refutes(rules, p):
            bits.append("N")
        else:
            bits.append("U")
    return "".join(bits)


# -------------------------------------------------------------------- main ---
def fingerprint(law, probes, vbin, budget, magmas):
    lhs, rhs = et.parse_equation(law)
    vs = et.variables(lhs) + [v for v in et.variables(rhs) if v not in et.variables(lhs)]
    fin = "".join("1" if holds_finite(lhs, rhs, vs, n, tab) else "0" for n, tab in magmas)
    aff = "".join("1" if holds_affine(lhs, rhs, a, b, c) else "0"
                  for a in AFFINE_RANGE for b in AFFINE_RANGE for c in AFFINE_CONST)
    prb = probe_vector(law, probes, vbin, budget) if vbin else ""
    return fin, aff, prb


def hamming(u, v):
    return sum(1 for x, y in zip(u, v) if x != y)


def selftest(vbin):
    """Known answers. Exits nonzero on failure; overnight.sh should gate on this."""
    magmas = _magmas()
    ok = True

    # (a) exact invariants are invariant under variable renaming.
    a1 = fingerprint("x = y ◇ ((x ◇ (y ◇ (z ◇ z))) ◇ y)", [], None, 0, magmas)[:2]
    a2 = fingerprint("u = v ◇ ((u ◇ (v ◇ (w ◇ w))) ◇ v)", [], None, 0, magmas)[:2]
    ok &= (a1 == a2); print(f"  rename-invariance      {'OK' if a1 == a2 else 'FAIL'}")

    # (b) the hard-tier degeneracy is real: Austin laws have all-zero magma vectors.
    for lw in ("x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))",          # 4916
               "x = y ◇ ((x ◇ (y ◇ (z ◇ z))) ◇ y)"):         # 12857
        fin = fingerprint(lw, [], None, 0, magmas)[0]
        z = set(fin) <= {"0"}
        ok &= z; print(f"  austin magma all-zero  {'OK' if z else 'FAIL'}  ({lw[:24]}…)")

    # (c) a law with finite models must NOT be all-zero, or component (1) is broken.
    fin = fingerprint("x ◇ y = x", [], None, 0, magmas)[0]
    nz = "1" in fin; ok &= nz
    print(f"  left-projection nonzero{'  OK' if nz else '  FAIL'}")

    # (d) affine component fires on something.
    aff = fingerprint("x ◇ y = y ◇ x", [], None, 0, magmas)[1]
    nz = "1" in aff; ok &= nz
    print(f"  affine vector nonzero  {'OK' if nz else 'FAIL'}")

    # (e) prover component: a law entails itself, and Eq2 entails everything.
    if vbin:
        v = probe_vector("x = y", ["x ◇ y = y ◇ x"], vbin, 5)
        ok &= (v == "Y"); print(f"  Eq2 ⊨ commutativity    {'OK' if v == 'Y' else 'FAIL'}")
        v = probe_vector("x ◇ y = x", ["x = y"], vbin, 5)
        ok &= (v == "U"); print(f"  proj ⊭ Eq2             {'OK' if v == 'U' else 'FAIL'}")

    # (f) model-refutation, if a saturation cert for 4916 is present.
    cert = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "certs", "4916.sat")
    if os.path.exists(cert):
        rules, bad = rules_from_sat(cert)
        c1 = (bad == 0 and len(rules) == 3)
        c2 = not model_refutes(rules, "x = x")       # reflexivity never refuted
        c3 = model_refutes(rules, "x = y")           # Austin: model is nontrivial
        ok &= c1 and c2 and c3
        print(f"  4916 -> 3-rule TRS     {'OK' if c1 else 'FAIL'}")
        print(f"  refl not refuted       {'OK' if c2 else 'FAIL'}")
        print(f"  Eq2 refuted (nontriv)  {'OK' if c3 else 'FAIL'}")

    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out")
    ap.add_argument("--pairs-out")
    ap.add_argument("--vampire")
    ap.add_argument("--probes", help="file, one equation per line; default: built-in")
    ap.add_argument("--status", help="only laws with this status")
    ap.add_argument("--budget", type=int, default=1, help="seconds per probe")
    ap.add_argument("--hamming", type=int, default=0, help="also pair across buckets "
                                                           "within this probe distance")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest(a.vampire))

    probes = ([l.strip() for l in open(a.probes) if l.strip()]
              if a.probes else DEFAULT_PROBES)
    magmas = _magmas()
    i, n = (int(x) for x in a.shard.split("/"))

    laws = []
    for fn in glob.glob(a.inp):
        for line in open(fn):
            r = json.loads(line)
            if a.status and r.get("status") != a.status:
                continue
            laws.append(r["law"])
    laws = sorted(set(laws))
    mine = [(k, lw) for k, lw in enumerate(laws) if k % n == i]
    print(f"{len(laws)} laws, shard {i}/{n} -> {len(mine)}, "
          f"{len(probes)} probes @ {a.budget}s, {len(magmas)} magmas", file=sys.stderr)

    t0, recs = time.time(), []
    with open(a.out, "a") as fh:
        for k, (idx, lw) in enumerate(mine):
            fin, aff, prb = fingerprint(lw, probes, a.vampire, a.budget, magmas)
            rec = {"law": lw, "idx": idx, "finite": fin, "affine": aff, "probe": prb}
            recs.append(rec)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); fh.flush()
            if k % 50 == 0:
                print(f"  {k}/{len(mine)}  {time.time()-t0:.0f}s", file=sys.stderr)

    # Bucket on the EXACT invariants only; probe vector refines within.
    buckets = defaultdict(list)
    for r in recs:
        buckets[(r["finite"], r["affine"])].append(r)

    pairs, exact_classes = [], 0
    for key, group in buckets.items():
        sub = defaultdict(list)
        for r in group:
            sub[r["probe"]].append(r)
        exact_classes += len(sub)
        for g in sub.values():                       # same probe vector: must decide
            pairs += [(x["law"], y["law"]) for x, y in itertools.combinations(g, 2)]
        if a.hamming:                                 # insurance against wrong splits
            for (p, gp), (q, gq) in itertools.combinations(sub.items(), 2):
                if hamming(p, q) <= a.hamming:
                    pairs += [(x["law"], y["law"]) for x in gp for y in gq]

    naive = len(recs) * (len(recs) - 1) // 2
    print(f"\nbuckets (exact invariants): {len(buckets)}"
          f"\nsub-buckets (+probe vector): {exact_classes}   <- UPPER BOUND on classes"
          f"\npairs to decide: {len(pairs)}  (naive pairwise: {naive}, "
          f"{naive / max(len(pairs), 1):.0f}x saved)", file=sys.stderr)

    if a.pairs_out:
        with open(a.pairs_out, "a") as fh:
            for x, y in pairs:
                fh.write(json.dumps({"a": x, "b": y}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
