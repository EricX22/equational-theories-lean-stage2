#!/usr/bin/env python3
"""llm_trivial.py — the trivial-side LLM rung (Lean-graded, LLM-reachable).

This is the guaranteed-productive channel. On a law that forces triviality
(L |= x=y), the answer is a short EQUATIONAL derivation: chain instances of the
law until two arbitrary elements are shown equal. That is exactly the kind of
reasoning LLMs can do, and it is core-Lean checkable today (no Mathlib, no
confluence machinery) — unlike the Austin construction side.

We hand the model the exact goal, the proof skeleton, and one worked example,
then judge its proof with the OFFICIAL answer_spec judge on the trivial side. A
PASS is a real, kernel-checked solve; difficulty scales with derivation length,
so partial-solve rate is a genuine gradient.

Distinct from:
  llm_solve.py         two-sided L0 (model picks the side). This file is a
                       trivial-focused prompt (worked example + skeleton) that
                       lifts the trivial-side solve rate.
  llm_construct.py     the Austin side, ATP-certified (Vampire), not Lean.

USAGE
  python3 paper/scripts/llm_trivial.py --dry-run          # inspect wrapped file + scan
  export OPENROUTER_API_KEY=...
  python3 paper/scripts/llm_trivial.py --laws-file paper/results/final_status.jsonl \
      --model openai/o4-mini --lean-dir . --out paper/results/llm_trivial.jsonl
"""
from __future__ import annotations
import argparse, glob, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_spec as asp
import llm_solve as L                    # call_llm, extract_lean

# A complete, correct trivial-side proof for the toy law `x = y ◇ y`, shown to the
# model so it learns the exact shape (intro, then chain law instances with trans/symm).
# For `x = y ◇ y`: h a a : a = a◇a ; h b a : b = a◇a ; so a = a◇a = b.
WORKED = """WORKED EXAMPLE (for the toy law  x = y ◇ y):
The hypothesis is  h : ∀ x y, x = op y y.  To prove  a = b  for arbitrary a b, note
h a a : a = op a a  and  h b a : b = op a a, so a and b are equal to the same thing:

theorem solution : Problem.TrivialGoal := by
  intro M op h a b
  exact (h a a).trans (h b a).symm
"""

RULES = """RULES (the judge enforces these; violating any is an automatic reject):
- Prove EXACTLY `Problem.TrivialGoal`. Your file defines `theorem solution : Problem.TrivialGoal`.
- Core Lean 4 only: intro, exact, rw, calc, .trans, .symm, congrArg, apply. No Mathlib.
- FORBIDDEN: sorry, admit, native_decide, axiom, unsafe, macro, syntax, elab. Do NOT
  redefine or even mention `Problem`, `AustinGoal`, `TrivialGoal`, or `Law` except in the
  one line `theorem solution : Problem.TrivialGoal := ...`.
"""

def build_prompt(law, header, feedback=None):
    p = f"""You are proving that a magma law forces triviality, in Lean 4.

The law is:  {law}
It has been established that this law collapses: every magma satisfying it has all elements
equal. Your job is to PROVE that in Lean.

`Problem.TrivialGoal` unfolds to:
    ∀ (M : Type) (op : M → M → M), (Law op) → ∀ a b : M, a = b
where `Law op` is `∀ <vars>, <the law with ◇ replaced by op>`. After
    intro M op h a b
you have `h : Law op` (the law, universally quantified — instantiate it with `h t1 t2 ...`)
and the goal `a = b`. Build an equational chain: each `h e1 e2 ...` is an equation you can
use with `.trans` and `.symm`, or as a `calc` step. Find substitutions that connect `a` to
`b` through the law.

{WORKED}
{RULES}

Output ONLY the Lean code for the file body (the `theorem solution : Problem.TrivialGoal`
and any helpers). No prose, no markdown fences."""
    if feedback:
        p += f"\n\nYour previous attempt was REJECTED:\n{feedback}\nFix it and try again."
    return p


def attempt(law, lean_dir, rounds, api_key, model, effort, timeout):
    header = asp.problem_header(law)
    feedback = None
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for rnd in range(1, rounds + 1):
        try:
            content, u = L.call_llm(build_prompt(law, header, feedback), api_key, model, effort, timeout)
        except Exception as e:                                  # noqa: BLE001
            return {"solved": False, "rounds_used": rnd, "error": f"api: {e}", "usage": usage}
        for k in usage:
            usage[k] += (u.get(k) or 0)
        body = L.extract_lean(content)
        side = L.detect_side(body)
        if side != "trivial":
            feedback = "Your `solution` must target `Problem.TrivialGoal` (you targeted "
            feedback += f"{side or 'neither goal'}). Prove the trivial side."
            continue
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, encoding="utf-8") as fh:
            fh.write(body); path = fh.name
        passed, rej = asp.judge(law, "trivial", path, lean_dir, timeout)
        os.unlink(path)
        if passed:
            return {"solved": True, "rounds_used": rnd, "code": body, "usage": usage}
        feedback = "\n".join(rej[:8])
    return {"solved": False, "rounds_used": rounds, "last_reject": feedback, "usage": usage}


def load_trivial(pattern):
    laws = []
    for fn in glob.glob(pattern):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("status") == "TRIVIAL" or r.get("gold") == "trivial":
                laws.append(r["law"])
    return sorted(set(laws), key=lambda s: s.count("◇"))     # shortest (easiest) first


def dry_run():
    """No Lean/API needed: build the wrapped judged file for the worked example and
    run the pre-Lean submission scan, so the plumbing is validated in-sandbox."""
    law = "x = y ◇ y"
    body = ("theorem solution : Problem.TrivialGoal := by\n"
            "  intro M op h a b\n"
            "  exact (h a a).trans (h b a).symm\n")
    print("=== detect_side ===", L.detect_side(body))
    print("=== wrapped file the judge would check ===")
    full = asp.problem_header(law) + "\n" + body + "\n" + asp.problem_footer("trivial")
    print(full)
    scan = getattr(asp, "scan_submission", None)
    if scan:
        problems = scan(body)
        print("=== scan_submission (pre-Lean guardrails) ===",
              "CLEAN" if not problems else problems)
    print("\n(Lean kernel check runs on your machine; wrapping + scan validated here.)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--laws-file")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--model", default="openai/o4-mini")
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--lean-dir", default=".")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.dry_run:
        dry_run(); return
    if not a.laws_file or not a.out:
        ap.error("--laws-file and --out required unless --dry-run")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    laws = load_trivial(a.laws_file)
    if a.n:
        laws = laws[:a.n]
    print(f"{len(laws)} trivial law(s); model={a.model} [trivial rung]", file=sys.stderr)
    solved = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt(law, a.lean_dir, a.rounds, api_key, a.model, a.reasoning_effort, a.timeout)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            solved += res["solved"]
            print(f"[{i}/{len(laws)}] {'SOLVED' if res['solved'] else '----'} "
                  f"r{res['rounds_used']} {res['secs']}s  {law[:48]}", file=sys.stderr)
    print(f"done: {solved}/{len(laws)} -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
