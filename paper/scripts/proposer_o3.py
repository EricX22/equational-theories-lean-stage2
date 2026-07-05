#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import math
import os
import re
import sys
import urllib.request

DEFAULT_PROOF_POLICY = {
    "allowed_axioms": ["propext", "Quot.sound", "Classical.choice"],
    "allowed_declarations": ["letFun"],
    "allowed_declaration_prefixes": [
        "And.", "Bool.", "Classical.", "Decidable.", "Eq.",
        "EquationLHS", "EquationRHS", "Goal",
        "Exists.", "False.",
        "Fin.", "Fintype.", "Function.", "HEq.", "Iff.", "Init.", "Int.", "Lean.",
        "List.", "Magma.", "Mathlib.", "MemoFinOp.", "Nat.", "Nonempty.", "Not.",
        "NthRewrites.", "OfNat.", "Option.", "Or.", "Prod.", "PUnit.",
        "RewriteCombinations.", "RewriteGoal.", "RewriteHypothesis.",
        "RewriteHypothesisAndGoal.", "SimpleRewrites.",
        "Std.", "Subgraph.", "Subtype.", "Sum.",
        "Trans.", "True.", "Unit.",
        "JudgeDecide.", "JudgeFinOp.", "JudgeMagma.",
        "inst", "of_decide_", "submission.",
        "congrArg", "congr_arg", "eq_self", "of_eq_true", "id",
        "eq_comm", "eq_mp", "eq_mpr", "rfl", "absurd",
    ],
}

PORTFOLIO_SUMMARY = """The following have ALL already been tried on this pair and FAILED
(do not propose anything equivalent to these):
- Exhaustive brute force, Fin 2-3
- ~30 structured table families (constant, projections, cyclic add/sub, max/min,
  multiplication mod n, small linear a*i+b*j mod n, XOR, diagonal), Fin 4-7
- 16 curated named witness magmas (Fin 2-4) and single-cell perturbations of them
- Symbolic affine model x*y = a*x + b*y + c (mod n), for every modulus n in 2..40
- A backtracking domain-propagation search over Fin 4-11, including modes
  restricted to: idempotent quasigroups, general quasigroups (Latin squares),
  row-Latin only, column-Latin only, goal-directed search, and unconstrained
  general search (this covers EVERY group of order <=11, since every group
  Cayley table is a Latin square)
- A complete SAT-based search, Fin 5-6
- An algebraic-linear infinite model x*y = a*x + (1-a)*y where a is a root of
  an integer polynomial of degree 2-8 (ZZ[alpha] companion-matrix construction)
- Vampire (both a saturation prover and a finite-model-builder), 40 seconds
  each direction
- Cyclic group Z/n (n=2..12) with twists: add, subtract, reverse-subtract,
  negate-both, left-inverse-add, right-inverse-add, additive-with-constant
- Dihedral groups D_2 through D_6 (order 4-12), both multiplication orders

Propose something NOT equivalent to any of the above. Good directions: larger
non-abelian groups (order >12, e.g. S4, A4, dicyclic groups) with a
non-obvious operation (not just group multiplication -- try conjugation-like
twists, semidirect-product-style combinations, or coordinatewise combinations
of two groups); near-rings (an operation that is NOT globally associative and
NOT commutative, only zero-symmetric); non-associative loops with two-sided
inverses; or an algebraic-linear model with degree > 8."""

PROMPT_TEMPLATE = """You are proposing a candidate countermodel for an equational-logic
problem over magmas (a set G with one binary operation, written a*b below,
NO other assumed structure -- not associative, no identity, nothing).

We need a magma (G, *) such that:
  EQ1 holds for all elements:   {eq1}
  EQ2 FAILS for at least one instance:   {eq2}
(Variables x,y,z,w,u range over G; `a◇b` in the problem text means `a*b`.)

A countermodel is EXPECTED to exist for this pair. "No model exists" / a
trivial order-2 punt is NOT an acceptable answer: you must always output a
concrete, constructive candidate. Your job is to find the construction, not to
judge whether one exists.

{portfolio_summary}

You may propose EITHER of two model types:

(A) A FINITE magma of order n (n >= 4), given as Python code.

(B) An INFINITE algebraic-linear model. This family refutes pairs that have NO
tractable finite model -- it is how previously-unsolved cases were cracked.
Carrier: the number ring ZZ[alpha] = ZZ[X]/(p(X)) for a MONIC integer
polynomial p of degree d >= 2, represented as ZZ^d in the power basis
{{1, alpha, ..., alpha^(d-1)}} with alpha acting as the companion matrix of p.
Operation: x * y = a*x + b*y, where a, b are elements of ZZ[alpha] given as
integer coefficient vectors of length d in that basis. EQ1 must hold as a
ZZ-module identity (it is linear, so it either holds identically or not); EQ2
must fail at a basis witness. IMPORTANT: the deterministic solver already
searches ONLY the idempotent slice b = 1 - a, so to add anything propose a
GENERAL model with b != 1 - a.

Respond with ONLY a JSON object (no markdown fences, no prose outside the JSON).

For a FINITE model, use exactly these keys:
{{
  "model_type": "finite",
  "family": "short name for the construction family",
  "justification": "1-3 sentences tied to the shape of EQ1/EQ2",
  "python_code": "a Python snippet defining def op(a, b, n): returning an int in range(n). Pure, deterministic, only uses math/n/a/b.",
  "candidate_n": [list of 2 to 5 integers to try for n]
}}

For an INFINITE algebraic-linear model, use exactly these keys:
{{
  "model_type": "algebraic_linear",
  "family": "short name for the construction family",
  "justification": "1-3 sentences tied to EQ1/EQ2, including why b != 1 - a",
  "poly": "integer list [c0, c1, ..., c_(d-1)] of the MONIC minimal polynomial p(X) = X^d + c_(d-1) X^(d-1) + ... + c1 X + c0, so length d = degree, d >= 2",
  "a_poly": "integer list of length d: a = sum_k a_poly[k] * alpha^k",
  "b_poly": "integer list of length d: b = sum_k b_poly[k] * alpha^k"
}}
"""


# reasoning:high burns far more tokens on the hidden reasoning trace before
# ever writing the visible answer -- max_tokens must scale with effort or
# the response gets cut off mid-reasoning with content=None (seen 2026-07-03
# on the real cluster: every "high" call failed with
# "'NoneType' object has no attribute 'strip'" because content was None).
MAX_TOKENS_BY_EFFORT = {"low": 4000, "medium": 12000, "high": 65000}


class EmptyContentError(RuntimeError):
    """API returned content=None -- token ceiling too low or misconfigured."""


def call_o3(prompt, api_key, reasoning_effort="low"):
    max_tokens = MAX_TOKENS_BY_EFFORT.get(reasoning_effort, 4000)
    body = json.dumps({
        "model": "openai/o3",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "reasoning": {"effort": reasoning_effort},
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
    )
    # high effort + a much bigger max_tokens can genuinely take a couple of
    # minutes; give it real room rather than timing out or getting impatient.
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    choice = data["choices"][0]
    content = choice["message"].get("content")
    usage = dict(data.get("usage", {}))
    usage["finish_reason"] = choice.get("finish_reason")
    if content is None:
        raise EmptyContentError(
            f"empty content from API (finish_reason={usage.get('finish_reason')}, "
            f"usage={usage}) -- likely hit max_tokens during reasoning; "
            f"increase MAX_TOKENS_BY_EFFORT for this effort level"
        )
    return content, usage


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    return json.loads(text[start:end + 1])


def materialize(python_code, n):
    ns = {"math": math}
    exec(python_code, ns)
    op_fn = ns["op"]
    table = [[op_fn(a, b, n) % n for b in range(n)] for a in range(n)]
    return table


def self_verify(solver, eq1, eq2, n, table):
    op = lambda a, b, t=table: t[a][b]
    v1, l1, r1 = solver.parse_equation(eq1)
    v2, l2, r2 = solver.parse_equation(eq2)
    return solver.equation_holds(v1, l1, r1, n, op) and not solver.equation_holds(v2, l2, r2, n, op)


def verify_algebraic_linear(solver, eq1, eq2, proposal, pid):
    """Self-verify an o3-proposed INFINITE algebraic-linear model over ZZ[alpha]
    and, if valid, emit a Lean certificate via the solver's competition-proven
    al_ machinery. Returns (cert_str, detail) or None.

    Soundness: EQ1 is linear, so checking it on the spanning set (each variable
    set to each power-basis vector, the rest zero) PROVES it holds for all
    inputs -- exact integer arithmetic, no sampling. A model that fails is
    rejected here, so a wrong proposal can never reach the certificate."""
    coeffs = [int(c) for c in proposal["poly"]]
    d = len(coeffs)
    if d < 2:
        return None
    a_poly = ([int(c) for c in proposal["a_poly"]] + [0] * d)[:d]
    b_poly = ([int(c) for c in proposal["b_poly"]] + [0] * d)[:d]
    L1, R1 = solver.al_parse_equation(eq1)
    L2, R2 = solver.al_parse_equation(eq2)
    op = solver.al_make_op(coeffs, a_poly, b_poly)
    e1vars = solver.al_vars_of(L1)
    for v in solver.al_vars_of(R1):
        if v not in e1vars:
            e1vars.append(v)
    e2vars = solver.al_vars_of(L2)
    for v in solver.al_vars_of(R2):
        if v not in e2vars:
            e2vars.append(v)
    # EQ1: must hold on the whole spanning set (basis check = proof for linear op)
    for active in e1vars:
        for k in range(d):
            env = {v: ([1 if i == k else 0 for i in range(d)] if v == active
                       else [0] * d) for v in e1vars}
            if solver.al_eval_term(L1, op, env) != solver.al_eval_term(R1, op, env):
                return None
    # EQ2: must fail at some basis witness
    witness = None
    for cand in e2vars:
        env = {v: ([1] + [0] * (d - 1) if v == cand else [0] * d) for v in e2vars}
        if solver.al_eval_term(L2, op, env) != solver.al_eval_term(R2, op, env):
            witness = cand
            break
    if witness is None:
        return None
    cert = solver.al_emit_cert(coeffs, a_poly, b_poly, e2vars, witness, pid)
    return cert, f"ZZ[alpha] deg {d}, a={a_poly}, b={b_poly}, witness={witness}"


def run_one(pid, eq1, eq2, solver, verify, args, api_key, feedback_text, stats=None):
    prompt = PROMPT_TEMPLATE.format(eq1=eq1, eq2=eq2, portfolio_summary=PORTFOLIO_SUMMARY)
    feedback = feedback_text or ""
    entries = []
    solved = False
    for rnd in range(1, args.rounds + 1):
        entry = {"id": pid, "round": rnd}
        content = None
        try:
            content, usage = call_o3(prompt + feedback, api_key, reasoning_effort=args.reasoning_effort)
            if stats is not None:
                stats["ok"] = stats.get("ok", 0) + 1
                stats["cost"] = stats.get("cost", 0.0) + float(usage.get("cost") or 0.0)
            entry["usage"] = usage
            proposal = extract_json(content)
            entry["family"] = proposal.get("family")
            entry["justification"] = proposal.get("justification")
            entry["python_code"] = proposal.get("python_code")
            entry["candidate_n"] = proposal.get("candidate_n")
        except EmptyContentError as e:
            entry["error"] = repr(e)
            entry["raw"] = content
            entries.append(entry)
            print(pid + " round " + str(rnd) + ": EMPTY CONTENT: " + str(e), file=sys.stderr)
            if stats is not None and stats.get("ok", 0) == 0:
                print("*** ABORTING BATCH: first API call returned empty content with zero "
                      "prior successes -- the token ceiling is misconfigured. Raise "
                      "MAX_TOKENS_BY_EFFORT or drop --reasoning-effort before rerunning. "
                      "Not spending further budget.", file=sys.stderr)
                sys.exit(1)
            continue
        except Exception as e:
            entry["error"] = repr(e)
            entry["raw"] = content
            entries.append(entry)
            print(pid + " round " + str(rnd) + ": PARSE FAILED: " + str(e), file=sys.stderr)
            continue

        _tok = (entry.get("usage") or {}).get("total_tokens")
        _cost = (entry.get("usage") or {}).get("cost")
        model_type = proposal.get("model_type", "finite")
        entry["model_type"] = model_type
        print(pid + " round " + str(rnd) + ": type=" + model_type +
              " family=" + repr(entry["family"]) +
              " n=" + repr(entry["candidate_n"]) +
              " tok=" + repr(_tok) + " cost=$" + format(float(_cost or 0.0), ".4f"),
              file=sys.stderr)

        # ── INFINITE algebraic-linear model branch ──────────────────────────
        if model_type == "algebraic_linear":
            cert = None
            try:
                out = verify_algebraic_linear(solver, eq1, eq2, proposal, pid)
                if out is not None:
                    cert, detail = out
                    entry["al_detail"] = detail
            except Exception as e:
                entry["al_error"] = repr(e)
            entry["self_verified"] = cert is not None
            if cert is None:
                feedback = ("\n\nYour previous algebraic-linear proposal (family: " +
                            repr(entry["family"]) + ") did NOT satisfy EQ1-as-identity "
                            "and-not-EQ2 over ZZ[alpha] (error: " + repr(entry.get("al_error")) +
                            "). Propose a DIFFERENT model -- recheck that EQ1 is a true "
                            "ZZ-module identity and that b != 1 - a.")
                entries.append(entry)
                print(pid + " round " + str(rnd) + ": self-verify FAILED (algebraic_linear)",
                      file=sys.stderr)
                continue
            cert_path = os.path.join(args.cert_dir, pid + "_al.lean")
            os.makedirs(args.cert_dir, exist_ok=True)
            with open(cert_path, "w") as cf:
                cf.write(cert)
            entry["cert_path"] = cert_path
            print(pid + " round " + str(rnd) + ": SELF-VERIFIED (algebraic_linear) -> " +
                  cert_path, file=sys.stderr)
            if verify is not None:
                problem = {"id": pid, "eq1_id": 0, "eq2_id": 0,
                           "equation1": eq1, "equation2": eq2,
                           "proof_policy": DEFAULT_PROOF_POLICY}
                result = verify.verify_answer(problem, json.dumps({"verdict": "false", "code": cert}))
                entry["judge_status"] = result.get("status")
                entry["judge_message"] = result.get("message")
                print(pid + " round " + str(rnd) + ": JUDGE " + str(result.get("status")),
                      file=sys.stderr)
                if result.get("status") == "accepted":
                    solved = True
            entries.append(entry)
            break

        hit = None
        errs = []
        for n in (proposal.get("candidate_n") or []):
            try:
                n = int(n)
                if n < 2 or n > 60:
                    continue
                table = materialize(proposal["python_code"], n)
                if self_verify(solver, eq1, eq2, n, table):
                    hit = (n, table)
                    break
            except Exception as e:
                errs.append("n=" + str(n) + ": " + repr(e))
        entry["materialize_errors"] = errs
        entry["self_verified"] = hit is not None

        if hit is None:
            feedback = ("\n\nYour previous proposal (family: " + repr(entry["family"]) +
                        ") did NOT satisfy EQ1-and-not-EQ2 for any of n=" +
                        repr(proposal.get("candidate_n")) + ". Errors: " + repr(errs) +
                        ". Propose a DIFFERENT family.")
            entries.append(entry)
            print(pid + " round " + str(rnd) + ": self-verify FAILED", file=sys.stderr)
            continue

        n, table = hit
        entry["hit_n"] = n
        entry["hit_table"] = table
        print(pid + " round " + str(rnd) + ": SELF-VERIFIED at n=" + str(n) + "!", file=sys.stderr)

        if verify is not None:
            code = solver.make_false_code(n, table)
            problem = {"id": pid, "eq1_id": 0, "eq2_id": 0,
                       "equation1": eq1, "equation2": eq2,
                       "proof_policy": DEFAULT_PROOF_POLICY}
            result = verify.verify_answer(problem, json.dumps({"verdict": "false", "code": code}))
            entry["judge_status"] = result.get("status")
            entry["judge_message"] = result.get("message")
            print(pid + " round " + str(rnd) + ": JUDGE " + str(result.get("status")), file=sys.stderr)
            if result.get("status") == "accepted":
                solved = True
        entries.append(entry)
        break
    return entries, solved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--judge-dir", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reasoning-effort", default="low")
    ap.add_argument("--cert-dir", default="paper/certs",
                    help="where to write emitted algebraic-linear .lean certificates")
    ap.add_argument("--pair-filter", default=None)
    ap.add_argument("--feedback-file", default=None)
    ap.add_argument("--append", action="store_true")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    sys.path.insert(0, args.solver_dir)
    import solver

    verify = None
    if args.judge_dir:
        sys.path.insert(0, args.judge_dir)
        import verify as _verify
        verify = _verify

    pairs = json.load(open(args.pairs))
    if args.pair_filter:
        pairs = {args.pair_filter: pairs[args.pair_filter]}

    feedback_text = open(args.feedback_file).read() if args.feedback_file else None

    log = []
    any_solved = False
    stats = {"ok": 0, "cost": 0.0}
    for pid, eq_pair in pairs.items():
        eq1, eq2 = eq_pair
        entries, solved = run_one(pid, eq1, eq2, solver, verify, args, api_key, feedback_text, stats)
        log.extend(entries)
        any_solved = any_solved or solved
        if solved:
            print("*** " + pid + ": SOLVED ***", file=sys.stderr)

    print("total API calls: " + str(stats["ok"]) +
          "  total cost: $" + format(stats["cost"], ".4f"), file=sys.stderr)

    with open(args.out, "a" if args.append else "w") as f:
        for e in log:
            f.write(json.dumps(e, default=str) + "\n")
    print("wrote " + str(len(log)) + " log entries -> " + args.out)


if __name__ == "__main__":
    main()
