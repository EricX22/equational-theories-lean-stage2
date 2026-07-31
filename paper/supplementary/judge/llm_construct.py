#!/usr/bin/env python3
"""llm_construct.py — ATP-certified construction channel for the Austin side.

The Lean judge can only grade the TRIVIAL side today (the general Austin
construction in OrderedModel.lean bottoms out at a `sorry` for ground
confluence). And no Austin model is expressible as arithmetic over Z/Z^k/Z_n:
any such op descends mod 2 to a *finite* model, which an Austin law forbids by
definition. So the affine autoformalizer (llm_autoformalize.py) is provably
empty for Austin laws.

This module grades the construction side with an ATP certificate instead of a
Lean proof, using the SAME trust base the corpus itself was built on (Vampire
saturation, cross-checkable by Twee).

PROPOSE-AND-CERTIFY PROTOCOL
---------------------------
The model proposes a finite first-order spec of the operation `E` — a small set
of equations over the magma symbol (a presentation / a completed rewrite
system). NOT the law itself. We then run two Vampire queries:

  (A) CORRECTNESS   E |- law            prove `law` from `E`  (SZS Theorem).
                                        This is a *refutation* proof: independently
                                        checkable, the strong kind of certificate.
  (B) NON-VACUITY   E + (exists a!=b)   saturate               (SZS Satisfiable,
                                        completeness-guarded). A nontrivial model
                                        of E exists; since E|-law it satisfies the
                                        law. => Austin, certified.

Soundness: (A) + (B) together exhibit a nontrivial model satisfying the law.
Self-policing: a lazy `E={law}` gains nothing — (B) becomes the original bare
saturation, which diverges on exactly the hard laws. A collapsing `E` (e.g.
`x=y`) passes (A) but fails (B) because `E + a!=b` is UNSAT. The model only
"wins" when its proposed structure makes BOTH queries terminate — which is the
value it adds on laws where blind completion diverges.

SCOPE. Certifies construction for laws admitting a FINITE presentation the model
can name. Laws whose completion is infinite (non-orientable hard tier, e.g.
12857/33436) are out of reach of this channel and stay reported as open.

USAGE
  # verify a hand/LLM proposal:
  python3 paper/scripts/llm_construct.py --selftest --vampire paper/bin/vampire
  # LLM proposes E and we certify (needs OPENROUTER_API_KEY):
  python3 paper/scripts/llm_construct.py --laws-file paper/results/eval/eval_solvable.jsonl \
      --vampire paper/bin/vampire --model openai/o4-mini --out paper/results/llm_construct.jsonl
"""
from __future__ import annotations
import argparse, glob, json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import etp_terms as et


# ------------------------------------------------------------------ vampire ---
def _run(vbin, args, body, timeout):
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False) as fh:
        fh.write(body); path = fh.name
    try:
        r = subprocess.run([vbin] + args + ["-t", f"{timeout}s", path],
                           capture_output=True, text=True, timeout=timeout + 5)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    finally:
        os.unlink(path)


def _theorem(out):
    return "SZS status Theorem" in out or "SZS status Unsatisfiable" in out


def _satisfiable(out):
    # Only trust Satisfiable from a strategy that kept completeness (Vampire prints
    # "incomplete strategy" when it dropped it), matching prove_status.py.
    return ("SZS status Satisfiable" in out or "SZS status CounterSatisfiable" in out) \
        and "incomplete strategy" not in out


# -------------------------------------------------------------------- TPTP ---
def _eq_axiom(name, eqstr):
    """One proposed equation -> a universally-quantified fof axiom."""
    l, r, vs = et.tptp_eq_vars(eqstr)
    quant = f"![{','.join(vs)}]:" if vs else ""
    return f"fof({name},axiom,{quant}({l}={r}))."


def _law_conjecture(law):
    l, r, vs = et.tptp_eq_vars(law)
    return f"fof(goal,conjecture,![{','.join(vs)}]:({l}={r}))."


# --------------------------------------------------------------- certify ---
def certify(law, E, vbin, timeout=30, certdir=None, tag=None):
    """Certify that proposal E is a nontrivial model of `law`.

    Returns dict with the verdict and both prover transcripts (the certificate).
    """
    axioms = "\n".join(_eq_axiom(f"e{i}", e) for i, e in enumerate(E))

    corr_body = axioms + "\n" + _law_conjecture(law)
    corr_out = _run(vbin, ["--mode", "casc"], corr_body, timeout)
    thm = _theorem(corr_out)

    nonvac_body = axioms + "\nfof(nt,axiom,?[U,V]: U != V)."
    nonvac_out = _run(vbin, ["-sa", "otter", "--show_active", "on"], nonvac_body, timeout)
    sat = _satisfiable(nonvac_out)

    ok = thm and sat
    res = {"certified": ok, "corr_theorem": thm, "nonvac_satisfiable": sat, "E": list(E)}
    if ok and certdir:
        os.makedirs(certdir, exist_ok=True)
        import hashlib
        h = tag or hashlib.sha1(law.encode()).hexdigest()[:12]
        p = os.path.join(certdir, f"{h}.construct")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(f"% law: {law}\n% E (proposed model):\n")
            for e in E:
                fh.write(f"%   {e}\n")
            fh.write("\n% ==== (A) correctness  E |- law ====\n" + corr_body + "\n" + corr_out)
            fh.write("\n% ==== (B) non-vacuity  E + a!=b  (saturation) ====\n" + nonvac_body + "\n" + nonvac_out)
        res["cert"] = p
    return res


# ------------------------------------------------------------------- LLM ---
def build_prompt(law, feedback=None):
    p = f"""You are constructing an infinite model for a magma law, to be checked by an
automated theorem prover.

The law is:  {law}
(the binary magma operation is written with the diamond; the law holds for all inputs.)

This law has NO nontrivial FINITE model, so its model is necessarily infinite, and it
CANNOT be an arithmetic formula (any polynomial op over the integers would descend to a
finite model). Instead, propose a finite set of DEFINING EQUATIONS for the operation — a
presentation of the model — from which the law follows and which is consistent with the
carrier having two distinct elements.

Think of it as the completed rewrite system a Knuth-Bendix procedure would converge to:
a handful of equations that (a) entail the law, and (b) do not force all elements equal.

Return ONLY a JSON object, nothing else:
  {{"E": ["<equation>", "<equation>", ...]}}
Each equation uses variables x,y,z,w and the diamond operator, in the form  LHS = RHS .
Example shape (NOT a solution):  {{"E": ["x ◇ (y ◇ x) = y", "(x ◇ x) ◇ x = x ◇ x"]}}
Do NOT just restate the law, and do NOT write `x = y`."""
    if feedback:
        p += f"\n\nYour previous proposal failed to certify: {feedback}\nTry a different presentation."
    return p


def parse_E(content):
    import re
    m = re.search(r"\{.*\}", content, re.DOTALL)
    if not m:
        return None, "no JSON object"
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return None, f"bad JSON: {e}"
    E = obj.get("E")
    if not isinstance(E, list) or not E or not all(isinstance(s, str) for s in E):
        return None, "E must be a nonempty list of 'LHS = RHS' strings"
    for e in E:
        if any(c in e for c in ("\u21d2", "=>", "->", "\u2192", "!=", "\u2260", "&", "|")):
            return None, (f"equation {e!r} is not a plain equation: E must be a set of "
                          "unconditional identities 'LHS = RHS' — no implications, "
                          "disequations, or logical connectives")
        if e.count("=") != 1:
            return None, f"equation {e!r} must contain exactly one '='"
        l, r = (s.strip() for s in e.split("=", 1))
        if {l, r} <= {"x", "y", "z", "w"}:       # reject a lazy `x = y` restatement
            return None, f"degenerate equation {e!r}"
        try:
            et.tptp_eq_vars(e)                   # must survive the TPTP emitter
        except Exception as ex:                  # noqa: BLE001
            return None, f"equation {e!r} failed to parse: {ex}"
    return E, None


def attempt(law, vbin, rounds, api_key, model, effort, timeout, certdir):
    import llm_solve as L
    feedback = None
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    attempts = []                                 # every proposed E + its query outcomes,
    for rnd in range(1, rounds + 1):              # kept for the failure-mode audit
        try:
            content, u = L.call_llm(build_prompt(law, feedback), api_key, model, effort, timeout=600)
        except Exception as e:                    # noqa: BLE001
            return {"solved": False, "rounds_used": rnd, "error": f"api: {e}",
                    "attempts": attempts, "usage": usage}
        for k in usage:
            usage[k] += (u.get(k) or 0)
        E, why = parse_E(content)
        if E is None:
            attempts.append({"round": rnd, "parse_error": why})
            feedback = why
            continue
        try:
            res = certify(law, E, vbin, timeout, certdir)
        except Exception as ex:                   # noqa: BLE001
            attempts.append({"round": rnd, "E": E, "parse_error": f"certify: {ex}"})
            feedback = f"E could not be certified as submitted ({ex}); emit plain equations only"
            continue
        attempts.append({"round": rnd, "E": E, "corr": res["corr_theorem"],
                         "nonvac": res["nonvac_satisfiable"]})
        if res["certified"]:
            return {"solved": True, "rounds_used": rnd, "E": E, "cert": res.get("cert"),
                    "attempts": attempts, "usage": usage}
        feedback = (f"correctness(E|-law)={res['corr_theorem']}, "
                    f"nonvacuity(E+a!=b sat)={res['nonvac_satisfiable']}")
    return {"solved": False, "rounds_used": rounds, "last": feedback,
            "attempts": attempts, "usage": usage}


# ------------------------------------------------------------------ CLI ---
def selftest(vbin):
    law = "x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))"     # 4916, clean austin
    cases = [
        ("POS  correct-ish (E=[law])", [law], True),
        ("NEG  wrong model (left proj)", ["x ◇ y = x"], False),
        ("VAC  collapse (x=y)", ["x = y"], False),
    ]
    ok = True
    for name, E, expect in cases:
        r = certify(law, E, vbin, timeout=8)
        got = r["certified"]
        flag = "ok" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"[{flag}] {name:30} certified={got!s:5} "
              f"(corr={r['corr_theorem']}, nonvac={r['nonvac_satisfiable']})")
    print("selftest", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def load_austin(pattern):
    laws = []
    for fn in glob.glob(pattern):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("gold") in (None, "austin") or r.get("status") == "AUSTIN_PROVEN":
                laws.append(r["law"])
    return sorted(set(laws))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--vampire", default="paper/bin/vampire")
    ap.add_argument("--laws-file")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--model", default="openai/o4-mini")
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--cert-dir", default="paper/certs/llm_construct")
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest(a.vampire))

    if not a.laws_file or not a.out:
        ap.error("--laws-file and --out required unless --selftest")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    laws = load_austin(a.laws_file)
    if a.n:
        laws = laws[:a.n]
    print(f"{len(laws)} austin law(s); model={a.model} [ATP-certified construction]", file=sys.stderr)
    solved = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt(law, a.vampire, a.rounds, api_key, a.model,
                          a.reasoning_effort, a.timeout, a.cert_dir)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            solved += res["solved"]
            print(f"[{i}/{len(laws)}] {'SOLVED' if res['solved'] else '----'} "
                  f"{res['secs']}s  {law[:50]}", file=sys.stderr)
    print(f"done: {solved}/{len(laws)} -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
