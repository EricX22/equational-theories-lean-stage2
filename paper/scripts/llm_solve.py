#!/usr/bin/env python3
"""llm_solve.py — the ALPS LLM baseline: propose a Lean model, judge it, loop on feedback.

Unlike attic/finite_regime/proposer_o3.py (finite tables + a `solver` import for the old
pairs pipeline), this targets the ALPS task directly and has NO solver dependency. It
reuses the OFFICIAL judge in answer_spec.py, so a PASS is a genuine ALPS solve: the goal
is pinned to the law and the axiom footprint is checked against {propext, Quot.sound,
Classical.choice}. The propose -> judge -> read-error -> revise loop is the same
self-verification a mathematician does, and is pre-registered as allowed
(LLM_EXPERIMENT_PLAN.md).

CHANNEL / LIMITATION. The judge compiles [our header] ++ [LLM body] ++ [our footer], so
the submission is a *body* and cannot contain `import` lines (they would land mid-file).
That means CORE Lean 4 only — no Mathlib. Models over Nat/Int provable with
rfl/decide/simp/omega/induction go through; anything needing Mathlib's algebra does not
yet, and is the job of the generic infinite-model formalisation (PAPER_PLAN.md §5B) /
the L2 autoformalizer. Use the lean_oracle standalone channel for Mathlib certs meanwhile
(see run_remaining.sh handsolve).

USAGE
  export OPENROUTER_API_KEY=...
  # one law, one round (do this first — cost caution):
  python3 paper/scripts/llm_solve.py --law 'x = ((((y ◇ x) ◇ y) ◇ y) ◇ z) ◇ y' \
      --lean-dir . --rounds 1 --out paper/results/llm_solve.jsonl
  # a batch over the hard tier (sharded), a few rounds each:
  python3 paper/scripts/llm_solve.py --laws-file paper/results/final_status.jsonl \
      --status NO_FINITE_MODEL --n 50 --shard 0/1 --rounds 3 \
      --lean-dir . --cert-dir paper/certs/llm --out paper/results/llm_hardtier.jsonl
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_spec as asp   # problem_header(law); judge(law, side, path, lean_dir, timeout)

# reasoning:high spends most tokens on the hidden trace before the visible answer;
# max_tokens must scale with effort or content comes back None (see proposer_o3 note).
MAX_TOKENS_BY_EFFORT = {"low": 6000, "medium": 16000, "high": 65000}
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


REFERENCE = (
    "theorem solution : Problem.AustinGoal :=\n"
    "  ⟨Bool, fun a _ => a, ⟨true, false, by decide⟩, fun _ => rfl⟩"
)

RULES = """RULES (the judge enforces these):
- Declare exactly one `theorem solution : Problem.AustinGoal := ...` (or a `def`/`lemma`).
- Do NOT write any `import` line, and do NOT use Mathlib. Only CORE Lean 4 is available
  (Nat, Int, Bool, custom inductive/structure types; tactics rfl, decide, simp, omega,
  induction, cases, constructor, exact, refine). Imports are impossible: your text is
  pasted between a fixed header and footer.
- Do NOT use: sorry, admit, native_decide, unsafe, implemented_by, axiom, macro, syntax,
  elab. Do NOT redefine `Problem`, `AustinGoal`, `TrivialGoal`, or `Law` (you may only
  reference `Problem.AustinGoal` as the type of `solution`).
- The final axiom footprint of `solution` must be a subset of
  {propext, Quot.sound, Classical.choice}. (`decide`/`omega`/`rfl` are fine.)

SHAPE. `Problem.AustinGoal` unfolds to
  `∃ (M : Type) (op : M → M → M), (∃ a b : M, a ≠ b) ∧ Law op`,
so `solution` is an anonymous constructor
  `⟨M, op, ⟨a, b, proof a ≠ b⟩, proof that Law op holds⟩`,
where `Law op` is `∀ <binders> : M, <the law with ◇ written as op>`.

REFERENCE ANSWER (for the easy law `x = x ◇ x`, which DOES have a finite model):
""" + REFERENCE


def build_prompt(law: str, header: str, feedback: str | None) -> str:
    p = f"""You are proving, in Lean 4, that a magma law admits a NONTRIVIAL model.

The law is:  {law}
(◇ is the binary magma operation.)

This law has been machine-certified to have NO nontrivial FINITE model. Therefore any
nontrivial model is necessarily INFINITE: your carrier `M` must be an infinite type
(e.g. `Nat`, `Int`, or a custom recursive type), NOT a finite one. Pick an operation
`op : M → M → M` and prove it satisfies the law while having two distinct elements.
Good first attempts: affine-style ops on `Int`/`Nat` (`fun x y => a*x + b*y + c`) proved
with `omega`/`ring_nf`-free `simp`/`induction`; or structured recursive ops proved by
induction. Keep proofs within core Lean.

Here is the EXACT problem statement your `solution` must inhabit (generated from the law;
do not restate or edit it — it is prepended for you):

{header}

{RULES}

Return ONLY a single Lean code block (```lean ... ```) containing your `solution` body
and any helper defs/lemmas it needs. No prose outside the code block."""
    if feedback:
        p += f"""

Your previous attempt was REJECTED. Fix it. The judge reported:
{feedback}

Return a corrected single Lean code block."""
    return p


def attempt(law: str, side: str, lean_dir: str, rounds: int, api_key: str,
            model: str, effort: str, timeout: int, cert_dir: str | None):
    header = asp.problem_header(law)
    feedback = None
    total_usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for rnd in range(1, rounds + 1):
        prompt = build_prompt(law, header, feedback)
        try:
            content, usage = call_llm(prompt, api_key, model, effort, timeout)
        except Exception as e:                       # noqa: BLE001
            return {"solved": False, "rounds_used": rnd, "error": f"api: {e}",
                    "usage": total_usage}
        for k in ("prompt_tokens", "completion_tokens"):
            total_usage[k] = total_usage.get(k, 0) + (usage.get(k) or 0)
        body = extract_lean(content)

        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(body); sub_path = fh.name
        try:
            passed, why = asp.judge(law, side, sub_path, lean_dir, timeout)
        finally:
            pass
        if passed:
            saved = None
            if cert_dir:
                os.makedirs(cert_dir, exist_ok=True)
                h = hashlib.sha1(law.encode()).hexdigest()[:12]
                saved = os.path.join(cert_dir, f"{h}.lean")
                with open(saved, "w", encoding="utf-8") as fh:
                    fh.write(body)
            os.unlink(sub_path)
            return {"solved": True, "rounds_used": rnd, "cert": saved,
                    "usage": total_usage}
        os.unlink(sub_path)
        feedback = "\n".join(why[:12])
    return {"solved": False, "rounds_used": rounds, "last_reject": feedback,
            "usage": total_usage}


def load_laws(a) -> list[str]:
    if a.law:
        return [a.law]
    laws: list[str] = []
    for fn in glob.glob(a.laws_file):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if a.status and r.get("status") != a.status:
                continue
            laws.append(r["law"])
    laws = sorted(set(laws))
    if a.n and a.n < len(laws):
        import random
        random.Random(a.sample_seed).shuffle(laws)
        laws = sorted(laws[:a.n])
    i, n = (int(x) for x in a.shard.split("/"))
    return [lw for k, lw in enumerate(laws) if k % n == i]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--law", help="a single law string (overrides --laws-file)")
    ap.add_argument("--laws-file", help="jsonl with a 'law' field per line")
    ap.add_argument("--status", help="filter laws-file by this status (e.g. NO_FINITE_MODEL)")
    ap.add_argument("--n", type=int, default=0, help="sample N laws (0 = all)")
    ap.add_argument("--sample-seed", type=int, default=20260714)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--side", choices=("austin", "trivial"), default="austin")
    ap.add_argument("--rounds", type=int, default=1, help="self-verify attempts per law")
    ap.add_argument("--model", default="openai/o3")
    ap.add_argument("--reasoning-effort", default="high")
    ap.add_argument("--lean-dir", default=".")
    ap.add_argument("--timeout", type=int, default=600, help="per-judge Lean compile (s)")
    ap.add_argument("--cert-dir", default=None, help="save passing certs here")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    if not a.law and not a.laws_file:
        print("need --law or --laws-file", file=sys.stderr); sys.exit(1)

    laws = load_laws(a)
    print(f"{len(laws)} law(s); model={a.model} effort={a.reasoning_effort} "
          f"rounds={a.rounds}", file=sys.stderr)
    solved = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for idx, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt(law, a.side, a.lean_dir, a.rounds, api_key,
                          a.model, a.reasoning_effort, a.timeout, a.cert_dir)
            res.update({"law": law, "side": a.side, "model": a.model,
                        "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            solved += res["solved"]
            tag = "SOLVED" if res["solved"] else "----"
            print(f"[{idx}/{len(laws)}] {tag} r{res['rounds_used']} "
                  f"{res['secs']}s  {law[:60]}", file=sys.stderr)
    print(f"done: {solved}/{len(laws)} solved -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
