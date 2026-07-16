#!/usr/bin/env python3
"""llm_autoformalize.py — the L2 rung of the ALPS LLM ladder.

The model outputs ONLY the math: a carrier and a binary operation as an arithmetic
formula. The harness writes the Lean 4 and discharges it, so the model never touches a
tactic. A solve therefore means "found the right structure" — it isolates CONSTRUCTION
from Lean-wrangling, unlike the raw rung (llm_solve.py) where a wrong dialect or a failed
tactic counts as a miss.

SCOPE. The construction side only (propose a nontrivial model for an Austin law), and the
algebraic channel only (carrier Int, op an integer-arithmetic expression in x,y). This is
exactly the fragment Lean discharges automatically with `ring`/`omega` today; models whose
only models are non-algebraic (rewrite-system) are out of reach of this rung by design.

The model returns  {"carrier": "Int", "op": "<expr in x,y>"}  and we build
    theorem solution : Problem.AustinGoal :=
      ⟨Int, fun x y => (<op>), ⟨0, 1, by decide⟩, by intro <vars>; <ring-ish>⟩
then run the OFFICIAL answer_spec judge (goal pinned to the law, axiom allowlist).

USAGE
  export OPENROUTER_API_KEY=...
  python3 paper/scripts/llm_autoformalize.py --laws-file paper/results/eval/eval_solvable.jsonl \
      --model openai/o4-mini --reasoning-effort medium --lean-dir . \
      --out paper/results/llm_l2.jsonl
"""
from __future__ import annotations
import argparse, glob, json, os, re, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_spec as asp                 # lean_law(law), judge(...)
import llm_solve as L                      # reuse call_llm, extract_lean

PREAMBLE = "import Mathlib"

# op is an integer-arithmetic expression in x and y only. Whitelist characters so nothing
# can inject Lean commands: digits, x, y, + - * , parens, spaces. (No z/w/other vars, no
# identifiers, no Mathlib calls — pure arithmetic.)
_OP_OK = re.compile(r"^[0-9xy +\-*()]+$")
_CARRIERS = {"Int", "Nat"}


def build_spec_prompt(law: str, feedback: str | None) -> str:
    p = f"""You are constructing a model for a magma law, to be checked mechanically.

The law is:  {law}
(◇ is the binary magma operation; the law must hold for all values.)

This law has NO nontrivial finite model, so a model must live on an INFINITE carrier — use
the integers. Propose a binary operation op(x, y) as an integer-arithmetic formula so the
law holds for all inputs and the carrier has two distinct elements.

The form that works for these laws is almost always AFFINE:
    op(x, y) = a*x + b*y + c      for integer constants a, b, c.
Solve for a, b, c so that substituting op makes the law a true identity (a purely linear
constraint). Prefer affine; only if no affine op works should you try a higher-degree
polynomial in x and y.

Return ONLY a JSON object, nothing else:
  {{"carrier": "Int", "op": "<expression in x and y>"}}
Use only x, y, integer constants, + - *, and parentheses. Examples: "2*x - y + 3",
"-x + 2*y", "x + y - 1".
Do NOT write Lean, tactics, or a proof — only the arithmetic formula for op. We generate and
verify the Lean ourselves."""
    if feedback:
        p += f"\n\nYour previous formula did not satisfy the law (the check failed). Try a " \
             f"different operation. Previous: {feedback}"
    return p


def parse_spec(content: str):
    """Extract {carrier, op} from the model's reply. Returns (carrier, op) or (None, reason)."""
    txt = content.strip()
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    if not m:
        return None, "no JSON object"
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return None, f"bad JSON: {e}"
    carrier = str(obj.get("carrier", "Int")).strip()
    op = str(obj.get("op", "")).strip()
    if carrier not in _CARRIERS:
        return None, f"carrier {carrier!r} not in {_CARRIERS}"
    if not op or not _OP_OK.match(op):
        return None, f"op {op!r} fails the arithmetic whitelist"
    return (carrier, op), None


def generate_body(law: str, carrier: str, op: str) -> str:
    _, vs = asp.lean_law(law)                       # law variables, in order
    binders = " ".join(vs) if vs else "x"
    # law proof: after intro, the goal is  x = <polynomial in the binders> ; ring closes any
    # true polynomial identity once the lambda is beta-reduced. Try a few shapes.
    law_pf = (f"by intro {binders}; "
              f"first | ring | (simp only []; ring) | (dsimp only; ring) | omega")
    nontriv = "⟨(0 : " + carrier + "), 1, by first | decide | omega | norm_num⟩"
    return (f"theorem solution : Problem.AustinGoal :=\n"
            f"  ⟨{carrier}, fun x y => ({op}), {nontriv},\n"
            f"   {law_pf}⟩")


def attempt(law: str, lean_dir: str, rounds: int, api_key: str, model: str,
            effort: str, timeout: int, cert_dir: str | None):
    feedback = None
    usage_tot = {"prompt_tokens": 0, "completion_tokens": 0}
    for rnd in range(1, rounds + 1):
        try:
            content, usage = L.call_llm(build_spec_prompt(law, feedback), api_key,
                                        model, effort, timeout=300)
        except Exception as e:                       # noqa: BLE001
            return {"solved": False, "rounds_used": rnd, "error": f"api: {e}",
                    "usage": usage_tot}
        for k in ("prompt_tokens", "completion_tokens"):
            usage_tot[k] = usage_tot.get(k, 0) + (usage.get(k) or 0)
        spec, why = parse_spec(content)
        if spec is None:
            feedback = why
            continue
        carrier, op = spec
        body = generate_body(law, carrier, op)
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(body); path = fh.name
        passed, rej = asp.judge(law, "austin", path, lean_dir, timeout, PREAMBLE)
        os.unlink(path)
        if passed:
            saved = None
            if cert_dir:
                os.makedirs(cert_dir, exist_ok=True)
                import hashlib
                saved = os.path.join(cert_dir, hashlib.sha1(law.encode()).hexdigest()[:12] + ".lean")
                open(saved, "w", encoding="utf-8").write(body)
            return {"solved": True, "rounds_used": rnd, "carrier": carrier, "op": op,
                    "cert": saved, "usage": usage_tot}
        feedback = f"op={op} -> " + "\n".join(rej[:6])
    return {"solved": False, "rounds_used": rounds, "last_spec": feedback, "usage": usage_tot}


def load_austin(a) -> list[str]:
    laws = []
    for fn in glob.glob(a.laws_file):
        for line in open(fn, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("gold") in (None, "austin"):     # construction side only
                laws.append(r["law"])
    laws = sorted(set(laws))
    if a.n and a.n < len(laws):
        import random
        random.Random(a.sample_seed).shuffle(laws); laws = laws[:a.n]
    i, n = (int(x) for x in a.shard.split("/"))
    return [lw for k, lw in enumerate(laws) if k % n == i]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--laws-file", required=True)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--sample-seed", type=int, default=20260716)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--rounds", type=int, default=3, help="propose->check->revise attempts")
    ap.add_argument("--model", default="openai/o4-mini")
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--lean-dir", default=".")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--cert-dir", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    laws = load_austin(a)
    print(f"{len(laws)} Austin law(s); model={a.model} rounds={a.rounds} [L2 autoformalize]",
          file=sys.stderr)
    solved = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for idx, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt(law, a.lean_dir, a.rounds, api_key, a.model,
                          a.reasoning_effort, a.timeout, a.cert_dir)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            solved += res["solved"]
            tag = "SOLVED" if res["solved"] else "----"
            extra = f" op={res.get('op')}" if res["solved"] else ""
            print(f"[{idx}/{len(laws)}] {tag} r{res['rounds_used']} {res['secs']}s{extra}  "
                  f"{law[:52]}", file=sys.stderr)
    print(f"done: {solved}/{len(laws)} solved -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
