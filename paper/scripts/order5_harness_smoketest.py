#!/usr/bin/env python3
"""Smoke-test: confirm the EXISTING judge (judge/verify.py + JudgeMagma/
JudgeDecide/JudgeFinOp/JudgeSupport) works unmodified on arbitrary order-5
equation pairs -- no new Lean infrastructure needed for the order-5 harness.

Finding (2026-07-01): the judge is equation-TEXT-driven (parses `equation1`/
`equation2` strings and generates a fresh JudgeProblem.lean module per call),
not tied to the specific 4694 pre-registered order-<=4 law IDs. Feeding it a
pair drawn from eq_size5.txt (order-5, ids >4694) works exactly like any
order-<=4 pair. This closes the "Lean harness for arbitrary order-5 laws is
heavy infra" risk flagged in PAPER_PLAN.md -- it's zero infra, not heavy.

Two things you must supply that a bare `problem` dict does NOT include by
default:
  1. `proof_policy` -- verify.py's default (absent field) is "reject every
     axiom", which will bounce ordinary `decide`-based false certs with
     DISALLOWED_AXIOMS (propext/Quot.sound/Classical.choice, which are
     ubiquitous and harmless in Lean4 std). The real system supplies
     `pipeline.proxy.DEFAULT_PROOF_POLICY` -- import and attach it, or every
     local test will spuriously fail.
  2. A Lean toolchain matching `lean-toolchain` (v4.30.0-rc2 as of this
     writing). Mathlib is declared in lakefile.lean but UNUSED by any actual
     judge/submission source (grep confirms zero `import Mathlib` outside
     reference/) -- for local smoke-testing, mirror the project into a
     scratch dir with the `require mathlib` line stripped from lakefile.lean.
     This avoids gigabytes of mathlib source+cache the real dependency would
     otherwise need; a Cowork-sandbox-sized disk (single-digit GB) is enough.

Usage (from repo root, with a Lean 4.30.0-rc2 toolchain + this project's
judge/ mirrored into a mathlib-free scratch lakefile per above):
  python order5_harness_smoketest.py --pair-jsonl paper/problems/order5_probe.jsonl
"""
from __future__ import annotations
import argparse
import json
import os
import sys

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
}  # copied from pipeline/proxy.py::DEFAULT_PROOF_POLICY -- keep in sync


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair-jsonl", required=True,
                     help="jsonl with rows {id, eq1_id, eq2_id, equation1, equation2}")
    ap.add_argument("--judge-dir", default="judge",
                     help="path to the (mathlib-free scratch mirror's) judge/ dir")
    ap.add_argument("--solver-dir", default=None,
                     help="path to scripts/my_solver_merged (to reuse its search "
                          "stages for generating candidate certs); optional")
    ap.add_argument("--limit", type=int, default=1)
    args = ap.parse_args()

    sys.path.insert(0, args.judge_dir)
    import verify  # noqa: E402

    if args.solver_dir:
        sys.path.insert(0, args.solver_dir)
        import solver  # noqa: E402

        captured = {}

        def fake_judge(verdict, code):
            captured["verdict"], captured["code"] = verdict, code
            return {"status": "accepted", "message": "captured, not submitted"}
        solver.call_judge = fake_judge

    rows = [json.loads(l) for l in open(args.pair_jsonl) if l.strip()]
    n_ok = n_tested = 0
    for row in rows:
        if n_tested >= args.limit:
            break
        eq1, eq2 = row["equation1"], row["equation2"]
        problem = {
            "id": row["id"], "eq1_id": row["eq1_id"], "eq2_id": row["eq2_id"],
            "equation1": eq1, "equation2": eq2,
            "proof_policy": DEFAULT_PROOF_POLICY,
        }
        code = verdict = None
        if args.solver_dir:
            n, table = solver.search_counterexample(eq1, eq2, max_n=3)
            if n is not None:
                verdict, code = "false", solver.make_false_code(n, table)
            else:
                captured.clear()
                if solver.try_direct_h_application(problem, eq1, eq2):
                    verdict, code = "true", captured["code"]
        if code is None:
            continue
        n_tested += 1
        result = verify.verify_answer(problem, json.dumps({"verdict": verdict, "code": code}))
        ok = result.get("status") == "accepted"
        n_ok += ok
        print(f"{row['id']}: verdict={verdict} judge_status={result.get('status')} "
              f"({result.get('error_code')})")
        if not ok:
            print("  message:", result.get("message"))

    print(f"\n{n_ok}/{n_tested} accepted")


if __name__ == "__main__":
    main()
