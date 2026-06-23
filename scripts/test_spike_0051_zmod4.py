#!/usr/bin/env python3
"""Run the REAL judge on the hard2_0051 ℤ-module (ℤ⁴ companion-matrix) cert.

Same harness contract as scripts/test_spike_judge.py, pointed at the integer-only
certificate docs/spike_0051_zmod4.lean (no Real/Polynomial/AdjoinRoot/CommRing).

    python scripts/test_spike_0051_zmod4.py

Needs the Lean toolchain + built .lake (the WSL env that compiles JudgeProblem).
On rejection the judge returns `direct_declarations` — that list pinpoints the
exact disallowed constant to swap a tactic for.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from judge.verify import verify_answer  # noqa: E402
from pipeline.proxy import DEFAULT_PROOF_POLICY  # noqa: E402

probs = {
    json.loads(l)["id"]: json.loads(l)
    for l in (ROOT / "examples/problems/hard2.jsonl").read_text().splitlines()
    if l.strip()
}
p = probs["hard2_0051"]
problem = {k: p[k] for k in ("id", "eq1_id", "eq2_id", "equation1", "equation2")}
problem["proof_policy"] = DEFAULT_PROOF_POLICY

code = (ROOT / "docs/spike_0051_zmod4.lean").read_text(encoding="utf-8")
raw_answer = json.dumps({"verdict": "false", "code": code})

print(f"Judging {problem['id']}:  Equation{problem['eq1_id']} ⊬ Equation{problem['eq2_id']}")
print("(compiling JudgeProblem + Submission via Lean — may take a minute)\n")

result = verify_answer(problem, raw_answer)
print(json.dumps(result, indent=2, ensure_ascii=False))

status = result.get("status")
print()
if status == "accepted":
    print("✅ ACCEPTED — the integer-only infinite model clears the allowlist. "
          "False side reopens for the algebraic-linear family.")
else:
    print(f"⚠️  status = {status!r}.")
    bad = result.get("direct_declarations")
    if status and "DECLARATION" in str(result.get("code", "")).upper():
        print("Disallowed declarations were reported — the offending constant tells us "
              "which tactic to swap (see the fallback note in the .lean).")
    if bad:
        print("direct_declarations:", bad)
