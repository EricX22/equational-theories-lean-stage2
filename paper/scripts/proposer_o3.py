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

A finite countermodel is EXPECTED to exist for this pair -- these are open
order-5-and-up problems where a finite refutation is believed to exist but has
not yet been found. "No model exists" / a trivial order-2 punt is therefore NOT
an acceptable answer: you must always output a concrete, constructive candidate
of order >= 4. Your job is to find the construction, not to judge whether one
exists.

{portfolio_summary}

Respond with ONLY a JSON object (no markdown fences, no prose outside the
JSON) with these exact keys:
{{
  "family": "short name for the construction family",
  "justification": "1-3 sentences tied to the shape of EQ1/EQ2",
  "python_code": "a Python snippet defining def op(a, b, n): returning an int in range(n). Pure, deterministic, only uses math/n/a/b.",
  "candidate_n": [list of 2 to 5 integers to try for n]
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
        print(pid + " round " + str(rnd) + ": family=" + repr(entry["family"]) +
              " n=" + repr(entry["candidate_n"]) +
              " tok=" + repr(_tok) + " cost=$" + format(float(_cost or 0.0), ".4f"),
              file=sys.stderr)

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
