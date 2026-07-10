#!/usr/bin/env python3
"""Prove the STATUS of each law, instead of sieving it.

Replaces the "rung" sieve for the epistemic axis. Every law `x = T` is put into
exactly one of these buckets, and the first four are THEOREMS, not "we searched
and found nothing":

  TRIVIAL              L |= (x=y).  The implication is TRUE. Not Austin.
  AUSTIN_PROVEN        (i) no nontrivial FINITE model  AND  (iii) some nontrivial
                       model exists  =>  a nontrivial model exists and is infinite.
  NO_FINITE_MODEL      (i) proved; existence of a nontrivial model still open.
  HAS_FINITE_MODEL     fmb exhibited a nontrivial finite model. Not Austin.
  SATISFIABLE_ONLY     nontrivial model proved to exist, (i) not proved.
  OPEN                 nothing proved either way.

Why this matters
----------------
`L |= E` is semi-decidable (Birkhoff: complete proof search), and "a finite
countermodel exists" is semi-decidable too (enumerate finite magmas). So every
TRUE instance and every FALSE-with-finite-countermodel instance is eventually
settled by brute compute. Equational implication is nevertheless undecidable, so
the undecidability must live entirely in the remaining class: FALSE with no finite
countermodel. For the target E = (x=y) that class is exactly the Austin laws.
They are the only instances whose difficulty does not evaporate with a faster CPU.

The three provers
-----------------
1. TRIVIAL      Vampire proves L |= x=y.                       (--mode casc)

2. (i) NO NONTRIVIAL FINITE MODEL  -- pigeonhole, mechanized.
   Pick a subterm S of T containing x. If S is injective in x, then in a FINITE
   model x |-> S(x) is also surjective (pigeonhole). Surjectivity is an ordinary
   first-order sentence, so we may hand it to Vampire as an axiom -- this is how
   we say "finite" to a first-order prover, which otherwise cannot express it.
   If Vampire then proves x=y from L + surj(S), every finite model of L is
   trivial. That is claim (i), machine-checked.

   Injectivity is obtained two ways:
     tier 1 (free, syntactic): if S contains EVERY occurrence of x, then T = C[S]
       with C x-free, and the law x = C[S(x)] exhibits C as a left inverse of S.
       Injectivity needs no proof at all. Candidates = the subterms along the path
       from the root to the LCA of the x-occurrences, tried innermost-first.
     tier 2 (proved): for any other subterm S containing x, ask Vampire to prove
       S(x1)=S(x2) -> x1=x2 from L.

   Soundness note: surj(S) is asserted only inside the finite-model argument; the
   conclusion is "every FINITE model of L is trivial", never "L |= x=y".

3. (iii) EXISTENCE  Saturation on L + (exists two distinct elements). A COMPLETE
   saturation strategy that saturates without a refutation proves the theory
   consistent, hence (Goedel) that a nontrivial model exists. We use `-sa otter`
   and require the literal `SZS status Satisfiable` with no `incomplete strategy`
   in the output -- Vampire suppresses the Satisfiable status and says
   "Refutation not found, incomplete strategy" whenever completeness was lost, so
   the status line is itself the completeness certificate. We re-check it anyway.

   AUSTIN_PROVEN = (2) and (3). No construction required: existence is sometimes
   mechanical. Constructing the explicit infinite magma is not, and that -- not
   existence -- is the benchmark task.

Optionally records which deterministic baseline (translation-invariant / greedy)
builds a model, as a separate, non-epistemic attribute.

Usage:
  python paper/scripts/prove_status.py --in 'paper/results/o5_graded_*.jsonl' \
      --vampire paper/bin/vampire --out paper/results/o5_status.jsonl \
      --trivial-timeout 30 --i-timeout 30 --sat-timeout 30 --fmb-timeout 0 \
      --baseline --shard 0/16
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, subprocess, sys, tempfile, time


# ---------------------------------------------------------------- vampire ---
def _run(vbin, args, body, timeout):
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "p.p")
        with open(p, "w") as fh:
            fh.write(body)
        try:
            r = subprocess.run([vbin] + args + ["-t", f"{timeout}s", p],
                               capture_output=True, text=True, timeout=timeout + 10)
            return r.stdout
        except subprocess.TimeoutExpired:
            return ""


def _proved(out):
    return "SZS status Theorem" in out or "SZS status Unsatisfiable" in out \
        or "Refutation found" in out


def _satisfiable(out):
    """Only trust Satisfiable from a strategy that kept completeness."""
    return ("SZS status Satisfiable" in out or "SZS status CounterSatisfiable" in out) \
        and "incomplete strategy" not in out


# ------------------------------------------------------------------ terms ---
def vars_of(t):
    return {t[1]} if t[0] == "var" else vars_of(t[1]) | vars_of(t[2])


def subterms(t):
    yield t
    if t[0] == "op":
        yield from subterms(t[1])
        yield from subterms(t[2])


def paths_to(t, v, p=()):
    if t[0] == "var":
        if t[1] == v:
            yield p
    else:
        yield from paths_to(t[1], v, p + (1,))
        yield from paths_to(t[2], v, p + (2,))


def at(t, p):
    for s in p:
        t = t[s]
    return t


def free_inj_candidates(T):
    """Subterms containing EVERY occurrence of x: injective for free.

    They are exactly the subterms on the root->LCA path. Innermost first (the
    smallest such subterm is the informative one; the root gives a vacuous axiom).
    """
    xs = list(paths_to(T, "x"))
    if not xs:
        return []
    lca = []
    for i in range(min(len(p) for p in xs)):
        col = {p[i] for p in xs}
        if len(col) == 1:
            lca.append(xs[0][i])
        else:
            break
    out = []
    for k in range(len(lca), -1, -1):
        S = at(T, tuple(lca[:k]))
        if S[0] != "var":
            out.append(S)
    return out


def other_x_subterms(T, free):
    seen = {id(s) for s in free}
    keys = {_key(s) for s in free}
    out = []
    for S in subterms(T):
        if S[0] == "op" and "x" in vars_of(S) and _key(S) not in keys:
            keys.add(_key(S))
            out.append(S)
    return out


def _key(t):
    return t[1] if t[0] == "var" else f"({_key(t[1])}*{_key(t[2])})"


# ---------------------------------------------------------------- provers ---
def prove_trivial(et, law, vbin, timeout):
    l, r, vs = et.tptp_eq_vars(law)
    body = (f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\n"
            "fof(triv,conjecture,![X,Y]:(X=Y)).\n")
    return _proved(_run(vbin, ["--mode", "casc"], body, timeout))


def _lawax(et, law):
    l, r, vs = et.tptp_eq_vars(law)
    return f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).", vs


def prove_injective(et, law, S, vbin, timeout):
    """L |= S(x1,p) = S(x2,p) -> x1 = x2 ?  (tier-2 injectivity)"""
    ax, _ = _lawax(et, law)
    params = sorted(v.upper() for v in vars_of(S) - {"x"})
    s1 = et.to_tptp(S).replace("X", "X1")
    s2 = et.to_tptp(S).replace("X", "X2")
    q = ",".join(params + ["X1", "X2"])
    body = (ax + f"\nfof(inj,conjecture,![{q}]:({s1}={s2} => X1=X2)).\n")
    return _proved(_run(vbin, ["--mode", "casc"], body, timeout))


def prove_no_finite_model(et, law, vbin, timeout, tier2=True):
    """Claim (i): every finite model of L is trivial.  Returns witness S or None."""
    _, T = et.parse_equation(law)
    ax, _ = _lawax(et, law)
    cands = [(S, True) for S in free_inj_candidates(T)]
    if tier2:
        cands += [(S, False) for S in other_x_subterms(T, free_inj_candidates(T))]
    for S, free in cands:
        if not free and not prove_injective(et, law, S, vbin, timeout):
            continue
        params = sorted(v.upper() for v in vars_of(S) - {"x"})
        pre = f"![{','.join(params + ['U'])}]:" if params else "![U]:"
        body = (ax + f"\nfof(surj,axiom,{pre} ?[X]: {et.to_tptp(S)} = U).\n"
                     "fof(g,conjecture,![X,Y]: X = Y).\n")
        if _proved(_run(vbin, ["--mode", "casc"], body, timeout)):
            return _key(S)
    return None


def prove_nontrivial_model(et, law, vbin, timeout, certdir=None, tag=None):
    """Claim (iii): a nontrivial model exists (complete saturation => consistent).

    On success Vampire prints the saturated clause set between
    `SZS output start Saturation` / `end Saturation`. That set IS the certificate:
    it is finitely checkable and independent of trusting the binary's verdict.
    """
    ax, _ = _lawax(et, law)
    body = ax + "\nfof(nt,axiom,?[U,V]: U != V).\n"
    # `--show_active on` is REQUIRED: the `SZS output Saturation` block prints only a
    # subset of the final clause set (for 4916 it shows 2 clauses; the saturation
    # actually closed with 5, three of them derived by superposition). Without this
    # the archived certificate is not the saturated set and cannot be replayed.
    out = _run(vbin, ["-sa", "otter", "--show_active", "on"], body, timeout)
    ok = _satisfiable(out)
    if ok and certdir:
        os.makedirs(certdir, exist_ok=True)
        with open(os.path.join(certdir, f"{tag}.sat"), "w") as fh:
            fh.write(body + "\n% ---- vampire -sa otter ----\n" + out)
    return ok


def fmb_finite_model(et, law, vbin, timeout):
    ax, _ = _lawax(et, law)
    body = ax + "\nfof(nt,axiom,?[U,V]: U != V).\n"
    out = _run(vbin, ["-sa", "fmb"], body, timeout)
    return "Finite Model Found" in out or "SZS status Satisfiable" in out


# --------------------------------------------------------------- pipeline ---
def classify(et, law, vbin, a):
    """Cheap -> expensive, and never pay for a search a theorem has settled.

    trivial?  ->  (i)-prover  ->  [fmb ONLY if (i) failed]  ->  saturation
    If (i) is proved there is provably no nontrivial finite model, so running a
    finite model builder on it is pure waste. That reordering is most of the
    speedup on a big pool.
    """
    rec = {"law": law}
    t0 = time.time()

    if prove_trivial(et, law, vbin, a.trivial_timeout):
        rec.update(status="TRIVIAL", proved=True)
        rec["secs"] = round(time.time() - t0, 1)
        return rec

    wit = prove_no_finite_model(et, law, vbin, a.i_timeout, tier2=not a.no_tier2)
    rec["no_finite_model"] = bool(wit)
    rec["witness"] = wit

    if not wit and a.fmb_timeout and fmb_finite_model(et, law, vbin, a.fmb_timeout):
        rec.update(status="HAS_FINITE_MODEL", proved=True)
        rec["secs"] = round(time.time() - t0, 1)
        return rec

    tag = hashlib.sha1(law.encode()).hexdigest()[:12]
    sat = prove_nontrivial_model(et, law, vbin, a.sat_timeout, a.cert_dir, tag)
    if a.cert_dir:
        rec["cert"] = tag
    rec["nontrivial_model"] = sat
    if wit and sat:
        rec.update(status="AUSTIN_PROVEN", proved=True)
    elif wit:
        rec.update(status="NO_FINITE_MODEL", proved=False)
    elif sat:
        rec.update(status="SATISFIABLE_ONLY", proved=False)
    else:
        rec.update(status="OPEN", proved=False)
    rec["secs"] = round(time.time() - t0, 1)
    return rec


def load_laws(patterns):
    seen, laws = set(), []
    for pat in patterns:
        for path in sorted(glob.glob(pat)):
            for line in open(path):
                line = line.strip()
                if line:
                    law = json.loads(line).get("law")
                    if law and law not in seen:
                        seen.add(law); laws.append(law)
    return laws


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--trivial-timeout", type=int, default=30)
    ap.add_argument("--i-timeout", type=int, default=30)
    ap.add_argument("--sat-timeout", type=int, default=30)
    ap.add_argument("--fmb-timeout", type=int, default=0,
                    help="0 = skip (use when no-finite-model is already established)")
    ap.add_argument("--no-tier2", action="store_true",
                    help="only free/syntactic injectivity witnesses")
    ap.add_argument("--baseline", action="store_true",
                    help="also record which deterministic builder solves it")
    ap.add_argument("--cert-dir", default=None,
                    help="save the saturated clause set for each existence proof")
    ap.add_argument("--skip", nargs="*", default=[],
                    help="globs of jsonl whose laws are already classified (resume/dedup)")
    ap.add_argument("--shard", default=None)
    a = ap.parse_args()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et
    grade = None
    if a.baseline:
        import order6_grade
        grade = order6_grade.grade

    laws = load_laws(a.inp)
    if a.skip:
        done = set(load_laws(a.skip))
        laws = [L for L in laws if L not in done]
    if a.shard:
        i, m = (int(x) for x in a.shard.split("/"))
        laws = [L for k, L in enumerate(laws) if k % m == i]
    print(f"classifying {len(laws)} laws", flush=True)

    tally = {}
    # append, never truncate: --skip reads these same files on resume, and a shard
    # truncating its own output would silently drop laws another shard just skipped.
    with open(a.out, "a") as f:
        for j, law in enumerate(laws, 1):
            rec = classify(et, law, a.vampire, a)
            if grade is not None:
                try:
                    _, rec["baseline"] = grade(et, law)
                except Exception as e:
                    rec["baseline"] = f"error:{e}"
            tally[rec["status"]] = tally.get(rec["status"], 0) + 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if j % 10 == 0:
                print(f"  {j}/{len(laws)} | {dict(sorted(tally.items()))}", flush=True)
    print(f"DONE {dict(sorted(tally.items()))} -> {a.out}", flush=True)


def selftest(vbin):
    """Functional check. A truncated copy of this file still compiles, so parse
    checks are not enough — run the provers on laws with known answers."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et
    ok = True
    # holds in the 2-element left-projection magma => must NOT prove (i)
    for law in ["x = x \u25c7 (x \u25c7 x)", "x = (x \u25c7 y) \u25c7 x"]:
        w = prove_no_finite_model(et, law, vbin, 5)
        print(f"  negative control {law!r}: witness={w}", flush=True)
        ok &= (w is None)
    # ETP-confirmed Austin law 4916: (i) provable, saturation satisfiable
    law = "x =  y \u25c7 (x \u25c7 (x \u25c7 (y \u25c7 (z \u25c7 z))))"
    w = prove_no_finite_model(et, law, vbin, 10)
    s = prove_nontrivial_model(et, law, vbin, 10)
    print(f"  positive control 4916: witness={w} satisfiable={s}", flush=True)
    ok &= bool(w) and s
    print("SELFTEST " + ("OK" if ok else "FAILED"), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        i = sys.argv.index("--selftest")
        sys.exit(selftest(sys.argv[i + 1] if len(sys.argv) > i + 1 else "vampire"))
    main()
