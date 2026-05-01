"""
Marathon triage solver — two-pass with budget-aware priority.

Strategy:

  Pass A (cheap, free):
    Run brute-force counterexample search (Fin 2..3) on every problem.
    Roughly 40-50% of normal-distribution problems are counterexampled.
    Tokens spent: zero.

  Pass B (LLM, budget-aware):
    Sort the remaining (likely answer=true) problems by a difficulty
    heuristic — shorter total equation length first, fewer variables
    second. Walk in that order; for each problem ask the LLM for a
    Lean tactic body. Skip on parse fail or LLM error. Stop early when
    the projected cost of the next call would exceed remaining budget.

  Pass C (refinement, budget permitting):
    Walk Pass-B failures and retry once with the previous attempt as
    feedback in the prompt — same shape as Stage 2 multi-round loops.
    Capped at ``MAX_REFINE_PER_PROBLEM`` per problem so one stubborn
    target can't drain the budget.

Cross-problem experience reuse: each successful Lean proof body is
appended to ``<scratch>/proof_patterns.jsonl`` so future demos can
mine it. The current solver does not yet reuse patterns from prior
problems mid-run — that's the next iteration.

Token budget discipline:
  * marathon_llm.call_llm self-polices and refuses calls past the cap.
  * The proxy enforces the cap at the network layer via a pessimistic
    reservation (prompt_estimate + clamped max_tokens) — it returns
    402 BEFORE forwarding upstream when the reservation would overshoot.
  * The runner watchdog reads the proxy's settled-only counter (so an
    exact-budget legal reservation isn't killed mid-flight) and
    SIGTERMs the solver if billed cost exceeds the budget after settle.
  * This solver additionally pre-checks budget_remaining() before
    expensive Pass-C retries.
"""

PROMPT_FIRST_TRY = """You are solving an equational-theory implication in Lean 4.

Given two equational laws on a magma G with operation ◇:

  Law A ({problem.equation1_id}): {problem.equation1}
  Law B ({problem.equation2_id}): {problem.equation2}

Decide whether every magma satisfying A also satisfies B.

The proof goes inside this template (don't restate it):

    def submission : Goal := by
      intro G _ h
      <YOUR TACTIC BODY HERE>

``h : <Law A>`` is in scope. Use ``exact``, ``rw``, ``simp [h]``, ``intro``,
``apply``, ``have``, ``calc``, etc. No imports. No theorem statements.

If you believe the implication is FALSE, return a 2-D table on Fin n
(2 ≤ n ≤ 4) instead.

Reply with ONLY one JSON object, no markdown:

    {"verdict": "true",  "proof": "<tactic body>"}
or
    {"verdict": "false", "counterexample_table": [[0,1],[1,0]]}
"""

PROMPT_REFINE = """Your previous attempt for {problem.equation1_id} → {problem.equation2_id} did not verify.

Previous proof body:
{prev_proof}

Lean error:
{prev_error}

Try a different tactic. Same template, same response shape:
{"verdict": "true", "proof": "<new tactic body>"}
"""

PROMPT = PROMPT_FIRST_TRY  # for prompt extraction by the proxy (Stage 2 mode)


import json
import os
import re
import sys
import time
from itertools import product
from pathlib import Path


_LIB_DIR = os.environ.get("JUDGE_MARATHON_LIB_DIR")
if _LIB_DIR and _LIB_DIR not in sys.path:
    sys.path.insert(0, _LIB_DIR)


MAX_REFINE_PER_PROBLEM = 1
PASS_C_MIN_BUDGET_FRACTION = 0.10  # Reserve 10% of token budget for Pass C; skip if less.


# ───────── Equation parsing & brute-force ─────────

def _parse_equation(text):
    variables = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", text):
        if v not in seen:
            seen.add(v)
            variables.append(v)
    lhs_str, rhs_str = text.split("=", 1)

    def _to_expr(s):
        s = s.strip()
        while len(s) >= 2 and s[0] == "(" and s[-1] == ")":
            depth = 0
            matched = True
            for i, c in enumerate(s):
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                if depth == 0 and i < len(s) - 1:
                    matched = False
                    break
            if matched:
                s = s[1:-1].strip()
            else:
                break
        depth = 0
        last_op = -1
        for i, c in enumerate(s):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == "\u25c7" and depth == 0:
                last_op = i
        if last_op >= 0:
            left = _to_expr(s[:last_op])
            right = _to_expr(s[last_op + 1:])
            return lambda env, l=left, r=right: env["op"](l(env), r(env))
        s = s.strip()
        if len(s) == 1 and s in seen:
            return lambda env, v=s: env[v]
        raise ValueError(f"cannot parse: {s!r}")

    return variables, _to_expr(lhs_str), _to_expr(rhs_str)


def _check_eq(variables, lhs_fn, rhs_fn, n, op):
    for vals in product(range(n), repeat=len(variables)):
        env = {"op": op}
        for v, val in zip(variables, vals):
            env[v] = val
        if lhs_fn(env) != rhs_fn(env):
            return False
    return True


def search_counterexample(eq1_text, eq2_text, max_n=3, time_budget=None):
    try:
        lhs_vars, lhs_l, lhs_r = _parse_equation(eq1_text)
        rhs_vars, rhs_l, rhs_r = _parse_equation(eq2_text)
    except (ValueError, IndexError):
        return None, None
    deadline = (time.monotonic() + time_budget) if time_budget else None
    for n in range(2, max_n + 1):
        total = n ** (n * n)
        for enc in range(total):
            if deadline is not None and time.monotonic() > deadline:
                return None, None
            table = [[(enc // (n ** (i * n + j))) % n for j in range(n)]
                     for i in range(n)]
            op = lambda a, b, t=table: t[a][b]
            if not _check_eq(lhs_vars, lhs_l, lhs_r, n, op):
                continue
            if _check_eq(rhs_vars, rhs_l, rhs_r, n, op):
                continue
            return n, table
    return None, None


# ───────── Lean code generators ─────────

def make_false_code(n, table):
    table_str = json.dumps(table)
    return (
        "import JudgeProblem\n"
        "import JudgeDecide.DecideBang\n"
        "import JudgeFinOp.MemoFinOp\n"
        "open MemoFinOp\n\n"
        "def submission : Goal := by\n"
        f"  let m : Magma (Fin {n}) := {{\n"
        f"    op := finOpTable \"{table_str}\"\n"
        f"  }}\n"
        f"  refine \u27e8Fin {n}, m, ?_\u27e9\n"
        f"  decideFin!\n"
    )


def make_true_code(proof_body):
    proof_body = proof_body.strip()
    if ":= by" in proof_body:
        proof_body = re.sub(r"^.*?:=\s*by\s*\n?", "", proof_body, count=1, flags=re.DOTALL)
    proof_body = re.sub(r"^\s*by\s+", "", proof_body)
    proof_body = re.sub(r"^\s*import\s+.*\n?", "", proof_body, flags=re.MULTILINE)
    lines = proof_body.split("\n")
    indented = "\n".join("  " + ln if ln.strip() else "" for ln in lines)
    return (
        "import JudgeProblem\n\n"
        "def submission : Goal := by\n"
        "  intro G _ h\n"
        f"{indented}\n"
    )


def _extract_json(text):
    text = re.sub(r"<think>[\s\S]*?</think>", "", text or "").strip()
    text = re.sub(r"^```(?:json)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return None


def _fill_first(prob):
    eq1_name = f"Equation{prob['eq1_id']}"
    eq2_name = f"Equation{prob['eq2_id']}"
    return (PROMPT_FIRST_TRY
            .replace("{problem.equation1}", prob.get("equation1", ""))
            .replace("{problem.equation2}", prob.get("equation2", ""))
            .replace("{problem.equation1_id}", eq1_name)
            .replace("{problem.equation2_id}", eq2_name))


def _fill_refine(prob, prev_proof, prev_error):
    eq1_name = f"Equation{prob['eq1_id']}"
    eq2_name = f"Equation{prob['eq2_id']}"
    return (PROMPT_REFINE
            .replace("{problem.equation1_id}", eq1_name)
            .replace("{problem.equation2_id}", eq2_name)
            .replace("{prev_proof}", prev_proof[:1500])
            .replace("{prev_error}", prev_error[:1500]))


# ───────── Triage scoring ─────────

def difficulty_score(prob):
    """Smaller is easier. Combine equation char length + distinct-var count."""
    eq1 = prob.get("equation1", "")
    eq2 = prob.get("equation2", "")
    var_count = len(set(re.findall(r"\b([a-z])\b", eq1 + " " + eq2)))
    return (len(eq1) + len(eq2)) + 5 * var_count


# ───────── Marathon driver ─────────

def _load_manifest(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                out.append(json.loads(raw))
            except json.JSONDecodeError:
                continue
    return out


def _append_answer(output_path, entry):
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    with open(output_path, "a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        try:
            os.fsync(fh.fileno())
        except OSError:
            pass


def _record_pattern(scratch_dir, prob, proof_body):
    """Append a winning proof pattern to scratch (cross-problem reuse hook)."""
    try:
        path = Path(scratch_dir) / "proof_patterns.jsonl"
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "id": prob["id"],
                "eq1_id": prob.get("eq1_id"),
                "eq2_id": prob.get("eq2_id"),
                "proof": proof_body,
            }) + "\n")
    except OSError:
        pass


def run_marathon():
    try:
        from marathon_llm import call_llm, budget_remaining, tokens_used
    except ImportError:
        call_llm = None  # type: ignore[assignment]

        def budget_remaining():  # noqa: D401
            return 0

        def tokens_used():  # noqa: D401
            return 0

    manifest_path = os.environ["JUDGE_MARATHON_MANIFEST"]
    output_path = os.environ["JUDGE_MARATHON_OUTPUT"]
    scratch_dir = os.environ["JUDGE_MARATHON_SCRATCH_DIR"]
    budget_seconds = float(os.environ.get("JUDGE_MARATHON_BUDGET_SECONDS", "3600"))
    cap_tokens = int(os.environ.get("JUDGE_MARATHON_BUDGET_TOKENS", "0"))
    deadline = time.monotonic() + budget_seconds
    tail_margin = 15.0

    # max_output_tokens is moderate (8192). The marathon_llm helper refuses
    # any call where ``estimated_prompt + max_output_tokens > budget_tokens``,
    # so on a compressed marathon (e.g. ``compression_ratio=0.5`` × 5 problems
    # × 65536 tokens = 32k cap) a 32k max_out blocks every call. 8192 fits
    # the median equational-theory proof body comfortably; non-compressed
    # contestants can raise this as needed.
    llm_config = {
        "model": os.environ.get("JUDGE_MARATHON_MODEL", "openai/gpt-oss-120b"),
        "provider": "deepinfra/bf16",
        "max_output_tokens": 8192,
        "temperature": 0.0,
        "reasoning_effort": "low",
        "use_seed": True,
        "seed": 0,
        "http_timeout_seconds": 600.0,
    }

    problems = _load_manifest(manifest_path)
    solved: set[str] = set()
    last_attempt: dict[str, tuple[str, str]] = {}  # id -> (proof, error)

    # ── Pass A: brute-force counterexample on every problem ──
    for prob in problems:
        if time.monotonic() + tail_margin >= deadline:
            break
        try:
            n, table = search_counterexample(prob["equation1"], prob["equation2"],
                                             max_n=3, time_budget=4.0)
        except Exception:  # noqa: BLE001
            continue
        if n is None:
            continue
        _append_answer(output_path, {
            "id": prob["id"], "verdict": "false",
            "code": make_false_code(n, table),
        })
        solved.add(prob["id"])

    # ── Pass B: LLM, sorted by difficulty ──
    if call_llm is None:
        return
    remaining = [p for p in problems if p["id"] not in solved]
    remaining.sort(key=difficulty_score)

    pass_c_reserve = int(cap_tokens * PASS_C_MIN_BUDGET_FRACTION) if cap_tokens else 0

    for prob in remaining:
        if time.monotonic() + tail_margin >= deadline:
            break
        if cap_tokens and tokens_used() + pass_c_reserve >= cap_tokens:
            break
        prompt = _fill_first(prob)
        try:
            resp = call_llm(prompt, config=llm_config)
        except Exception:  # noqa: BLE001
            continue
        if "error" in resp:
            if "exhausted" in str(resp.get("error", "")):
                break
            continue
        obj = _extract_json(resp.get("response", ""))
        if not isinstance(obj, dict):
            continue
        verdict = obj.get("verdict")
        if verdict == "true":
            body = obj.get("proof", "")
            if not body:
                continue
            code = make_true_code(body)
            _append_answer(output_path, {"id": prob["id"], "verdict": "true", "code": code})
            last_attempt[prob["id"]] = (body, "")
            _record_pattern(scratch_dir, prob, body)
        elif verdict == "false":
            tbl = obj.get("counterexample_table")
            if isinstance(tbl, list) and tbl:
                _append_answer(output_path, {
                    "id": prob["id"], "verdict": "false",
                    "code": make_false_code(len(tbl), tbl),
                })

    # ── Pass C: single refine pass (skipped if budget too low) ──
    if cap_tokens and tokens_used() < cap_tokens - pass_c_reserve // 2:
        for prob in remaining:
            if time.monotonic() + tail_margin >= deadline:
                break
            if cap_tokens and tokens_used() >= cap_tokens:
                break
            pid = prob["id"]
            if pid not in last_attempt:
                continue
            prev_proof, prev_error = last_attempt[pid]
            prompt = _fill_refine(prob, prev_proof, prev_error)
            try:
                resp = call_llm(prompt, config=llm_config)
            except Exception:  # noqa: BLE001
                continue
            if "error" in resp:
                if "exhausted" in str(resp.get("error", "")):
                    break
                continue
            obj = _extract_json(resp.get("response", ""))
            if not isinstance(obj, dict) or obj.get("verdict") != "true":
                continue
            body = obj.get("proof", "")
            if not body:
                continue
            _append_answer(output_path, {
                "id": pid, "verdict": "true", "code": make_true_code(body),
            })


# ───────── Stage-2 fallback ─────────

def _read_message():
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return json.loads(line.strip())


def _send_message(msg):
    print(json.dumps(msg), flush=True)


def run_stage2():
    """Brute-force-only Stage-2 path; not a competitive contender."""
    startup = _read_message()
    problem = startup["problem"]
    n, table = search_counterexample(problem["equation1"], problem["equation2"], max_n=3)
    if n is None:
        return
    _send_message({"call": "judge", "verdict": "false", "code": make_false_code(n, table)})
    _read_message()


def main():
    if "JUDGE_MARATHON_MANIFEST" in os.environ:
        run_marathon()
    else:
        run_stage2()


if __name__ == "__main__":
    main()
