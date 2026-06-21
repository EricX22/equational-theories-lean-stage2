#!/usr/bin/env python3
"""Run the REAL judge on the hard2_0051 infinite-model certificate.

This is how to test docs/spike_0051_judge.lean: the judge writes JudgeProblem
for Eq2531/Eq4307, compiles our Submission.lean against it (with its Mathlib
path), and returns the verdict. Run from the repo root:

    python scripts/test_spike_judge.py

Needs the Lean toolchain + built .lake (same env that compiled the standalone).
Prints the judge result dict — look for  "status": "accepted".
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from judge.verify import verify_answer  # noqa: E402

# Load hard2_0051 and keep ONLY the keys the judge accepts (strip index/difficulty/answer).
probs = {
    json.loads(l)["id"]: json.loads(l)
    for l in (ROOT / "examples/problems/hard2.jsonl").read_text().splitlines()
    if l.strip()
}
p = probs["hard2_0051"]
problem = {k: p[k] for k in ("id", "eq1_id", "eq2_id", "equation1", "equation2")}
# Use the REAL competition policy (what pipeline/proxy.py injects), not the bare
# empty default — the empty default bans ALL axioms, which isn't what grading uses.
from pipeline.proxy import DEFAULT_PROOF_POLICY  # noqa: E402
problem["proof_policy"] = DEFAULT_PROOF_POLICY

code = (ROOT / "docs/spike_0051_judge.lean").read_text(encoding="utf-8")
raw_answer = json.dumps({"verdict": "false", "code": code})

print(f"Judging {problem['id']}:  Equation{problem['eq1_id']} ⊬ Equation{problem['eq2_id']}")
print("(compiling JudgeProblem + Submission via Lean — may take a minute)\n")

result = verify_answer(problem, raw_answer)
print(json.dumps(result, indent=2, ensure_ascii=False))

status = result.get("status")
print()
if status == "accepted":
    print("✅ ACCEPTED — the infinite algebraic-model certificate works through the judge.")
else:
    print(f"⚠️  status = {status!r}.  If it's an import/path issue, the judge env may not "
          "expose Mathlib to submissions; if it's a proof error, paste the message and "
          "I'll patch the Lean.")
