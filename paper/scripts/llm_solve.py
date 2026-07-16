#!/usr/bin/env python3
"""llm_solve.py — the ALPS LLM baseline harness: two-sided, propose -> judge -> revise.

The task is two-sided and so is this: given a law, the model must DECIDE whether the law
forces triviality or admits a nontrivial model, and prove the matching goal
(`Problem.TrivialGoal` or `Problem.AustinGoal`). We detect which goal its `solution`
targets and run the OFFICIAL answer_spec judge on that side, so a PASS is a genuine solve
(goal pinned to the law, axiom footprint checked). No `solver` dependency.

EVAL DESIGN. Run on the SOLVABLE tier (paper/results/eval/eval_solvable.jsonl: known Austin
+ trivial, fresh orders) where a partial solve rate discriminates systems; the hard tier
(eval_frontier.jsonl) floors everyone and is an optional bonus. The gold label, when
present, is used only for reporting (did the model pick the right side?) --- grading is by
Lean regardless.

CHANNEL NOTE. The judge compiles [header] ++ [body] ++ [footer] with no import line, so
today submissions are CORE Lean 4 only (no Mathlib). Trivial-side proofs and Nat/Int
models go through; most Austin models need Mathlib, which is unlocked by prepending an
import in the judge (a one-line change to answer_spec, to be tested on a machine with
Lean). Until then expect the Austin side to be limited.

USAGE
  export OPENROUTER_API_KEY=...
  # smoke: one law, one round
  python3 paper/scripts/llm_solve.py --law 'x = ...' --lean-dir . --rounds 1 \
      --out paper/results/llm_solve.jsonl
  # the eval:
  python3 paper/scripts/llm_solve.py --laws-file paper/results/eval/eval_solvable.jsonl \
      --rounds 3 --lean-dir . --cert-dir paper/certs/llm --out paper/results/llm_eval.jsonl
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, re, sys, tempfile, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_spec as asp   # problem_header(law); judge(law, side, path, lean_dir, timeout)

# o3's reasoning trace counts against max_tokens; on hard construction prompts it easily
# exceeds 16k and starves the visible answer (finish_reason=length, empty content). Give
# it real room. o3's ceiling is 100k output tokens.
MAX_TOKENS_BY_EFFORT = {"low": 16000, "medium": 48000, "high": 100000}
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


def call_llm(prompt: str, api_key: str, model: str, effort: str, timeout: int = 300):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS_BY_EFFORT.get(effort, 8000),
        "reasoning": {"effort": effort},
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    choice = data["choices"][0]
    content = choice["message"].get("content")
    usage = dict(data.get("usage", {}))
    usage["finish_reason"] = choice.get("finish_reason")
    if content is None:
        raise RuntimeError(f"empty content (finish_reason={usage.get('finish_reason')}, "
                           f"usage={usage}); raise --reasoning-effort or MAX_TOKENS_BY_EFFORT")
    return content, usage


_BLOCK = re.compile(r"```[a-zA-Z0-9]*\s*(.*?)```", re.DOTALL)
def extract_lean(text: str) -> str:
    m = _BLOCK.search(text)
    return (m.group(1) if m else text).strip()


_SIDE = re.compile(r"\bsolution\b[^:=]*:\s*(?:Problem\.)?(AustinGoal|TrivialGoal)")
def detect_side(body: str) -> str | None:
    """Which goal does the submission's `solution` target?"""
    m = _SIDE.search(body)
    if m:
        return "austin" if m.group(1) == "AustinGoal" else "trivial"
    has_a, has_t = "AustinGoal" in body, "TrivialGoal" in body
    if has_a and not has_t:
        return "austin"
    if has_t and not has_a:
        return "trivial"
    return None


REFERENCE = (
    "theorem solution : Problem.AustinGoal :=\n"
    "  ⟨Bool, fun a _ => a, ⟨true, false, by decide⟩, fun _ => rfl⟩"
)

RULES = """RULES (the judge enforces these):
- Declare exactly one `theorem solution` (or `def`/`lemma`) whose type is
  `Problem.AustinGoal` OR `Problem.TrivialGoal` --- prove whichever one holds for this law.
- Mathlib is imported for you; do NOT write any `import` line yourself (your text is
  pasted between a fixed header and footer). You may use Mathlib (e.g. `ZMod`, `ring`,
  `linarith`, `omega`, `decide`, `simp`, `induction`) and all of core Lean 4.
- Use LEAN 4 syntax ONLY. Do NOT use Lean 3: no `begin ... end` blocks and no
  comma-separated tactics. Write tactic proofs with `by` and Lean 4 tactics
  (`intro`, `exact`, `rw`, `simp`, `omega`, `decide`, `ring`, `constructor`, ...).
- Do NOT use: sorry, admit, native_decide, unsafe, implemented_by, axiom, macro, syntax,
  elab. Do NOT redefine `Problem`, `AustinGoal`, `TrivialGoal`, or `Law` (you may only
  reference them as the type of `solution`).
- The final axiom footprint of `solution` must be a subset of
  {propext, Quot.sound, Classical.choice}.

SHAPES.
- `Problem.AustinGoal` unfolds to `∃ (M : Type) (op : M → M → M), (∃ a b : M, a ≠ b) ∧ Law op`,
  so an Austin `solution` is `⟨M, op, ⟨a, b, proof a ≠ b⟩, proof Law op⟩` with M INFINITE
  (e.g. Int/Nat), since the law has no nontrivial finite model.
- `Problem.TrivialGoal` unfolds to `∀ (M) (op), Law op → ∀ a b : M, a = b`, so a trivial
  `solution` assumes `Law op` and derives `a = b` for arbitrary elements.
where `Law op` is `∀ <binders> : M, <the law with ◇ written as op>`.

REFERENCE (Austin form, for the easy law `x = x ◇ x`):
""" + REFERENCE


def build_prompt(law: str, header: str, feedback: str | None) -> str:
    p = f"""You are solving a two-sided problem about a magma law in Lean 4.

The law is:  {law}
(◇ is the binary magma operation.)

Exactly ONE of these is true; decide which and prove it:
  - AUSTIN: the law admits a NONTRIVIAL model (two distinct elements, an operation
    satisfying the law). Such a model is necessarily INFINITE, since the law is certified
    to have no nontrivial finite model --- use an infinite carrier (Int, Nat, or a custom
    type). Prove `Problem.AustinGoal`.
  - TRIVIAL: the law forces every model to a single element (it entails x = y). Prove
    `Problem.TrivialGoal`.

Here is the EXACT problem statement, with both goals defined (generated from the law; do
not restate or edit it --- it is prepended for you):

{header}

{RULES}

Return ONLY a single Lean code block (```lean ... ```) with your `solution` (typed
`Problem.AustinGoal` or `Problem.TrivialGoal`) and any helpers it needs. No prose outside
the code block."""
    if feedback:
        p += f"""

Your previous attempt was REJECTED. Fix it. The judge reported:
{feedback}

Return a corrected single Lean code block."""
    return p


def attempt(law: str, side_mode: str, lean_dir: str, rounds: int, api_key: str,
            model: str, effort: str, timeout: int, cert_dir: str | None,
            preamble: str = ""):
    header = asp.problem_header(law)
    feedback = None
    jside = None
    total_usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for rnd in range(1, rounds + 1):
        prompt = build_prompt(law, header, feedback)
        try:
            content, usage = call_llm(prompt, api_key, model, effort, timeout)
        except Exception as e:                       # noqa: BLE001
            return {"solved": False, "rounds_used": rnd, "attempted_side": jside,
                    "error": f"api: {e}", "usage": total_usage}
        for k in ("prompt_tokens", "completion_tokens"):
            total_usage[k] = total_usage.get(k, 0) + (usage.get(k) or 0)
        body = extract_lean(content)
        jside = (detect_side(body) or "austin") if side_mode == "auto" else side_mode

        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(body); sub_path = fh.name
        passed, why = asp.judge(law, jside, sub_path, lean_dir, timeout, preamble)
        if passed:
            saved = None
            if cert_dir:
                os.makedirs(cert_dir, exist_ok=True)
                h = hashlib.sha1(law.encode()).hexdigest()[:12]
                saved = os.path.join(cert_dir, f"{h}.lean")
                with open(saved, "w", encoding="utf-8") as fh:
                    fh.write(body)
            os.unlink(sub_path)
            return {"solved": True, "rounds_used": rnd, "attempted_side": jside,
                    "cert": saved, "usage": total_usage}
        os.unlink(sub_path)
        feedback = "\n".join(why[:12])
    return {"solved": False, "rounds_used": rounds, "attempted_side": jside,
            "last_reject": feedback, "usage": total_usage}


def load_laws(a) -> list[dict]:
    if a.law:
        return [{"law": a.law}]
    rows: list[dict] = []
    for fn in glob.glob(a.laws_file):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if a.status and r.get("status") and r.get("status") != a.status:
                continue
            rows.append(r)
    # dedup by law, keep first
    seen, out = set(), []
    for r in rows:
        if r["law"] not in seen:
            seen.add(r["law"]); out.append(r)
    if a.n and a.n < len(out):
        import random
        random.Random(a.sample_seed).shuffle(out)
        out = out[:a.n]
    i, n = (int(x) for x in a.shard.split("/"))
    return [r for k, r in enumerate(out) if k % n == i]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--law", help="a single law string (overrides --laws-file)")
    ap.add_argument("--laws-file", help="jsonl with a 'law' field (and optional 'gold')")
    ap.add_argument("--status", help="filter laws-file by this status if present")
    ap.add_argument("--n", type=int, default=0, help="sample N laws (0 = all)")
    ap.add_argument("--sample-seed", type=int, default=20260715)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--side", default="auto", choices=("auto", "austin", "trivial"),
                    help="auto = model decides the side (the real two-sided task)")
    ap.add_argument("--rounds", type=int, default=1, help="self-verify attempts per law")
    ap.add_argument("--model", default="openai/o3")
    ap.add_argument("--reasoning-effort", default="high")
    ap.add_argument("--lean-dir", default=".")
    ap.add_argument("--timeout", type=int, default=600, help="per-judge Lean compile (s)")
    ap.add_argument("--cert-dir", default=None, help="save passing certs here")
    ap.add_argument("--lean-import", default="import Mathlib",
                    help="preamble prepended above the header (empty for core Lean only)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    if not a.law and not a.laws_file:
        print("need --law or --laws-file", file=sys.stderr); sys.exit(1)

    laws = load_laws(a)
    print(f"{len(laws)} law(s); model={a.model} effort={a.reasoning_effort} "
          f"rounds={a.rounds} side={a.side}", file=sys.stderr)
    solved = right_side = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for idx, row in enumerate(laws, 1):
            law, gold = row["law"], row.get("gold")
            t0 = time.time()
            res = attempt(law, a.side, a.lean_dir, a.rounds, api_key,
                          a.model, a.reasoning_effort, a.timeout, a.cert_dir,
                          a.lean_import)
            res.update({"law": law, "gold": gold, "model": a.model,
                        "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            solved += res["solved"]
            if gold and res.get("attempted_side") == gold:
                right_side += 1
            tag = "SOLVED" if res["solved"] else "----"
            g = f" gold={gold}" if gold else ""
            print(f"[{idx}/{len(laws)}] {tag} side={res.get('attempted_side')}{g} "
                  f"r{res['rounds_used']} {res['secs']}s  {law[:52]}", file=sys.stderr)
    msg = f"done: {solved}/{len(laws)} solved -> {a.out}"
    if any(r.get("gold") for r in laws):
        msg += f"; picked correct side {right_side}/{len(laws)}"
    print(msg, file=sys.stderr)


if __name__ == "__main__":
    main()
