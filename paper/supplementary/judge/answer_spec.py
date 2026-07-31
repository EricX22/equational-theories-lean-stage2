#!/usr/bin/env python3
"""The answer format. What a submission IS, and how it is judged.

WHY THIS EXISTS
    "Verification" is not a gap in this project once you decide that **Lean is the
    arbiter**: an answer is a Lean proof of a statement we fix in advance, and Lean
    checks it. That is closed by construction. But it is only closed once the
    statement is actually written down, and until this file existed it wasn't. A
    benchmark whose problem statement lives in a README is not a benchmark.

    Everything else follows from the two-sided task. Given a law L for which we have
    *proved* that no nontrivial finite model exists, exactly one of these holds:

      AUSTIN   ∃ a magma satisfying L with two distinct elements  (necessarily infinite)
      TRIVIAL  every magma satisfying L collapses to a point

    So the submission is a Lean proof of `AustinGoal` or of `TrivialGoal`. Nothing else
    is accepted, from a model or from our own baseline. Answer-channel parity is not a
    nicety: if the baseline emits partial magmas and the model emits Lean proofs, then
    "the baseline scored 0" is a category error, not a zero.

THE STATEMENTS, in full, for law `x = T[x,y,z,…]`:

    AustinGoal  : ∃ (M : Type) (op : M → M → M),
                    (∃ a b : M, a ≠ b) ∧ (∀ x y z …, x = T[op])

    TrivialGoal : ∀ (M : Type) (op : M → M → M),
                    (∀ x y z …, x = T[op]) → ∀ a b : M, a = b

    `∃ a b, a ≠ b` is what makes the model nontrivial, and it also gives us `M`
    inhabited for free. No finiteness appears anywhere: the Austin property comes from
    the separately-proved (i)-certificate, not from this statement. The statement is
    therefore honest even if the (i)-prover is wrong — a submitted model is a real
    model regardless.

WHAT THE JUDGE ENFORCES
    The statement is generated HERE, from the law, and the submitter never writes it.
    The judged file is  [our header] ++ [their body] ++ [our footer].  The footer
    contains `example : Problem.AustinGoal := solution`, which is what forces their
    `solution` to have exactly the type we asked for — they cannot weaken it, because
    Lean's elaborator checks it against our definition.

    Rejected outright, before Lean ever runs (see `scan_submission`):
      sorry / admit            — incomplete proof
      native_decide            — trusts compiled code, bypasses the kernel
      axiom                    — assume what you were asked to prove
      unsafe / implemented_by  — escape hatches out of the kernel
      macro / macro_rules / syntax / elab / attribute
                               — a submission that redefines notation can make our
                                 footer typecheck against something other than our goal
      any mention of AustinGoal / TrivialGoal / namespace Problem
                               — shadowing our statement is the whole attack

    Then Lean runs, and the axiom footprint of `solution` must be a subset of
    {propext, Quot.sound, Classical.choice}. `sorryAx` or `Lean.ofReduceBool` in the
    footprint is a fail even if the file compiled. `lean_oracle.py` already implements
    this scan; this module is what tells it *which statement* was supposed to be proved.

WHAT THIS DELIBERATELY DOES NOT DO
    It does not require the model be presented in any particular way — integers,
    ℤ[α], a quotient of a term algebra, a Herbrand model over a rewrite system. Any
    Lean proof is a proof. That is the point: the format must not quietly reward the
    shapes our own construction suite already knows how to build, or the eval measures
    interpolation over our recipe rather than construction. Coverage is limited only
    by what a submitter can push through Lean, and the generic infinite-model
    formalisation (PAPER_PLAN.md §5B) is what widens it.

USAGE
    python3 paper/scripts/answer_spec.py --selftest
    python3 paper/scripts/answer_spec.py --law 'x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))' \
        --side austin --emit-problem paper/lean/Problem_4916.lean
    python3 paper/scripts/answer_spec.py --law '...' --side austin \
        --submission answer.lean --judge --lean-dir .
"""
from __future__ import annotations
import argparse, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et                                              # noqa: E402

ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}
FORBIDDEN_AXIOMS = {"sorryAx", "Lean.ofReduceBool", "Lean.trustCompiler"}

# Token -> why it is banned. Order matters only for the error message.
BANNED = {
    "sorry": "incomplete proof",
    "admit": "incomplete proof",
    "native_decide": "trusts compiled code, bypasses the kernel",
    "unsafe": "escapes the kernel",
    "implemented_by": "escapes the kernel",
    "macro_rules": "can redefine notation so our footer checks a different goal",
    "macro ": "can redefine notation so our footer checks a different goal",
    "syntax ": "can redefine notation so our footer checks a different goal",
    "elab ": "metaprogramming",
    "namespace Problem": "the statement is ours; reopening the namespace is the attack",
}
AXIOM_DECL_RE = re.compile(r"^\s*axiom\s", re.MULTILINE)

# A submission MUST mention `Problem.AustinGoal` to state its own theorem, so the token
# itself cannot be banned. What must be banned is REDEFINING it — that is the attack:
# shadow our statement with `True`, prove that, and our footer typechecks.
REDEF_RE = re.compile(
    r"^\s*(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(?:def|abbrev|theorem|lemma|instance|structure|inductive|class|notation|alias|export)"
    r"\s+[^\n:=]*\b(AustinGoal|TrivialGoal|Law)\b", re.MULTILINE)


# ---------------------------------------------------------------- emitters ---
def lean_term(ast) -> str:
    if ast[0] == "var":
        return ast[1]
    return f"(op {lean_term(ast[1])} {lean_term(ast[2])})"


def lean_law(law: str) -> tuple[str, list[str]]:
    """`x = T` -> ('x = (op …)', ['x','y','z'])  with binders in first-seen order."""
    lhs, rhs = et.parse_equation(law)
    vs = et.variables(lhs)
    for v in et.variables(rhs):
        if v not in vs:
            vs.append(v)
    return f"{lean_term(lhs)} = {lean_term(rhs)}", vs


def problem_header(law: str) -> str:
    body, vs = lean_law(law)
    binders = " ".join(vs)
    return f'''/-
  Problem statement. GENERATED — do not edit, do not redefine in a submission.

    law:  {law}

  Exactly one of `AustinGoal` and `TrivialGoal` is true, given the separately
  machine-checked fact that this law admits no nontrivial FINITE model.
-/
namespace Problem

/-- A magma satisfying the law. -/
def Law {{M : Type}} (op : M → M → M) : Prop :=
  ∀ {binders} : M, {body}

/-- There is a nontrivial model. (It is then necessarily infinite.) -/
def AustinGoal : Prop :=
  ∃ (M : Type) (op : M → M → M), (∃ a b : M, a ≠ b) ∧ Law op

/-- Every model collapses. Equivalently `law ⊨ x = y`. -/
def TrivialGoal : Prop :=
  ∀ (M : Type) (op : M → M → M), Law op → ∀ a b : M, a = b

end Problem
'''


def problem_footer(side: str) -> str:
    goal = "Problem.AustinGoal" if side == "austin" else "Problem.TrivialGoal"
    return f'''
-- GENERATED. Forces `solution` to have exactly the type we asked for.
example : {goal} := solution

#print axioms solution
'''


# ------------------------------------------------------------------- judge ---
def strip_comments(src: str) -> str:
    src = re.sub(r"/-.*?-/", " ", src, flags=re.DOTALL)
    return re.sub(r"--[^\n]*", " ", src)


def scan_submission(src: str) -> list[str]:
    """Textual rejects. Runs BEFORE Lean, because some of these subvert Lean."""
    code, bad = strip_comments(src), []
    for tok, why in BANNED.items():
        if tok in code:
            bad.append(f"banned token {tok.strip()!r}: {why}")
    for m in REDEF_RE.finditer(code):
        bad.append(f"redefines {m.group(1)!r}: the statement is ours")
    if AXIOM_DECL_RE.search(code):
        bad.append("declares an axiom: assumes what it was asked to prove")
    if not re.search(r"^\s*(theorem|def|lemma)\s+solution\b", code, re.MULTILINE):
        bad.append("no `solution` declaration found")
    return bad


AXIOM_LINE_RE = re.compile(r"'([\w.]+)' depends on axioms: \[([^\]]*)\]")


def check_axioms(out: str) -> list[str]:
    """The footprint is an ALLOWLIST. Anything not named is a failure.

    A blocklist would be unsound: it only catches the cheats we thought of. Lean
    prints `'solution' depends on axioms: [propext, Classical.choice]`, or
    `'solution' does not depend on any axioms`. Both are fine; anything else is not.
    """
    bad = []
    if "declaration uses 'sorry'" in out:
        bad.append("sorry warning from Lean")

    seen_footprint = False
    for name, axioms in AXIOM_LINE_RE.findall(out):
        seen_footprint = True
        used = {a.strip() for a in axioms.split(",") if a.strip()}
        for ax in sorted(used - ALLOWED_AXIOMS):        # allowlist, not blocklist
            why = " (FORBIDDEN)" if ax in FORBIDDEN_AXIOMS else ""
            bad.append(f"{name}: unexpected axiom {ax!r}{why}")
    if not seen_footprint and "does not depend on any axioms" not in out:
        bad.append("no `#print axioms` output — cannot certify the footprint")
    return bad


def judge(law: str, side: str, submission: str, lean_dir: str = ".",
          timeout: int = 600, preamble: str = "") -> tuple[bool, list[str]]:
    src = open(submission, encoding="utf-8").read()
    problems = scan_submission(src)
    if problems:
        return False, problems

    # An optional preamble (e.g. "import Mathlib") is prepended ABOVE the header so the
    # submission can use library lemmas; imports must precede all commands, so this is the
    # only place they can go. Default "" keeps the core-Lean behaviour and the selftest.
    head = (preamble.rstrip() + "\n\n") if preamble.strip() else ""
    full = head + problem_header(law) + "\n" + src + problem_footer(side)
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "Answer.lean")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(full)
        try:
            r = subprocess.run(["lake", "env", "lean", p], cwd=lean_dir,
                               capture_output=True, text=True, timeout=timeout)
        except FileNotFoundError:
            return False, ["lean/lake not found — cannot judge"]
        except subprocess.TimeoutExpired:
            return False, [f"timeout after {timeout}s"]
        out = r.stdout + r.stderr
        if r.returncode != 0 or "error:" in out:
            return False, ["lean rejected the proof"] + out.splitlines()[:12]
        return (not check_axioms(out)), check_axioms(out)


# ---------------------------------------------------------------- selftest ---
# A reference answer, provable without Mathlib. Law `x = x ◇ x` (idempotence,
# written in our `x = T` shape); Bool with `op a _ = a` satisfies it and is nontrivial.
REFERENCE_LAW = "x = x ◇ x"
REFERENCE_ANSWER = '''
theorem solution : Problem.AustinGoal :=
  ⟨Bool, fun a _ => a, ⟨true, false, by decide⟩, fun _ => rfl⟩
'''

# The attack this format exists to stop: shadow our statement with something trivial,
# prove that instead, and let our footer typecheck against the impostor.
SHADOW_ATTACK = '''
namespace Problem
def AustinGoal : Prop := True
end Problem
theorem solution : Problem.AustinGoal := trivial
'''
OPEN_SHADOW_ATTACK = '''
def AustinGoal : Prop := True
theorem solution : AustinGoal := trivial
'''


def selftest(lean_dir=None):
    ok = True
    hdr = problem_header("x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))")     # 4916

    c = "op x (op x (op x (op y (op z z))))" in hdr.replace("  ", " ") or "op" in hdr
    ok &= c; print(f"  header mentions op        {'OK' if c else 'FAIL'}")
    c = "∀ x y z : M" in hdr
    ok &= c; print(f"  binders in first-seen ord {'OK' if c else 'FAIL'}")
    c = "AustinGoal" in hdr and "TrivialGoal" in hdr
    ok &= c; print(f"  both goals emitted        {'OK' if c else 'FAIL'}")

    # Negative tests: each of these MUST be rejected without running Lean.
    attacks = {
        "sorry":        "theorem solution : Problem.AustinGoal := by sorry",
        "axiom":        "axiom cheat : Problem.AustinGoal\ntheorem solution := cheat",
        "shadow ns":    SHADOW_ATTACK,
        "shadow open":  OPEN_SHADOW_ATTACK,
        "redef Law":    "def Law {M : Type} (_ : M → M → M) : Prop := True\n"
                        "theorem solution : Problem.AustinGoal := by exact?",
        "native":       "theorem solution : Problem.AustinGoal := by native_decide",
        "no solution":  "theorem answer : Problem.AustinGoal := by decide",
    }
    for name, src in attacks.items():
        rejected = bool(scan_submission(src))
        ok &= rejected
        print(f"  reject {name:12s}       {'OK' if rejected else 'FAIL — ACCEPTED!'}")

    # Positive test: the reference answer must pass the textual scan.
    clean = not scan_submission(REFERENCE_ANSWER)
    ok &= clean; print(f"  reference answer clean    {'OK' if clean else 'FAIL'}")

    if lean_dir:
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as fh:
            fh.write(REFERENCE_ANSWER); path = fh.name
        passed, why = judge(REFERENCE_LAW, "austin", path, lean_dir)
        ok &= passed
        print(f"  reference answer compiles {'OK' if passed else 'FAIL: ' + str(why[:2])}")
        os.unlink(path)
    else:
        print("  NOTE: no --lean-dir; Lean was not run. The textual gate is only half "
              "the judge — the axiom footprint check needs a real Lean.")

    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--law")
    ap.add_argument("--side", choices=("austin", "trivial"), default="austin")
    ap.add_argument("--emit-problem")
    ap.add_argument("--submission")
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--lean-dir")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest(a.lean_dir))
    if a.emit_problem:
        with open(a.emit_problem, "w", encoding="utf-8") as fh:
            fh.write(problem_header(a.law))
        print(f"wrote {a.emit_problem}")
    if a.judge:
        passed, why = judge(a.law, a.side, a.submission, a.lean_dir or ".", a.timeout)
        print("PASS" if passed else "FAIL")
        for w in why:
            print(f"  {w}")
        sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
