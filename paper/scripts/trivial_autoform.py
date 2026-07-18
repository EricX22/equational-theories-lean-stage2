#!/usr/bin/env python3
"""trivial_autoform.py — the autoformalizer rung for the trivial side.

Removes the formalization wall: the model emits ONLY a chain of terms
    [a, t1, t2, ..., b]
where each adjacent pair is one WHOLE-TERM application of the law (forward or backward).
The harness finds the law instance for each step by first-order matching and assembles a Lean
`calc` — the model never writes Lean. This isolates reasoning (find the path) from
formalization (handled here), so a model that is formalization-bound can still register a solve.

SCOPE (v1): whole-term steps only. If a correct proof needs a rewrite inside a subterm
(congruence), that step won't match and we report which step failed — the model can re-route
through whole-term steps. A congruence-aware assembler is future work.

Soundness is unchanged: we emit `h <args>` / `(h <args>).symm` and the Lean KERNEL checks the
assembled calc via answer_spec. A wrong chain simply fails to assemble or fails Lean.
"""
from __future__ import annotations
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answer_spec as asp
import etp_terms as et


# --- ASTs are ('var',name) | ('op',l,r) via etp_terms.parse_term -----------------
def _match(pat, term, subst):
    """First-order match: bind pattern vars to subtrees of term; consistent -> True."""
    if pat[0] == "var":
        v = pat[1]
        if v in subst:
            return subst[v] == term
        subst[v] = term
        return True
    if term[0] != "op":
        return False
    return _match(pat[1], term[1], subst) and _match(pat[2], term[2], subst)


def _render(ast):
    """AST -> Lean, using the operation `op` (a,b,... are in-scope constants)."""
    if ast[0] == "var":
        return ast[1]
    return f"(op {_render(ast[1])} {_render(ast[2])})"


def _law(law):
    T = et.parse_term(law.split("=", 1)[1])
    _, vs = asp.lean_law(law)                       # binder order used by the generated `Law`
    return T, list(vs)


def justify_step(T, vs, s, t):
    """A Lean proof term for `s = t` as one whole-term law application, or None."""
    # forward: h with x:=s ;  T[x:=s] must equal t
    for direction in ("fwd", "rev"):
        src, dst = (s, t) if direction == "fwd" else (t, s)
        subst = {"x": src}
        if _match(T, dst, subst):
            args = [_render(subst.get(v, ("var", "a"))) for v in vs]   # unbound var: any element
            term = f"h {' '.join(args)}"
            return term if direction == "fwd" else f"({term}).symm"
    return None


def assemble(law, chain):
    """chain = list of ◇-term strings, chain[0]='a', chain[-1]='b'. -> (lean_body, err)."""
    if len(chain) < 2:
        return None, "chain too short"
    try:
        terms = [et.parse_term(c) for c in chain]
    except Exception as e:                          # noqa: BLE001
        return None, f"unparsable term: {e}"
    if terms[0] != ("var", "a") or terms[-1] != ("var", "b"):
        return None, "chain must start at `a` and end at `b`"
    T, vs = _law(law)
    justs = []
    for i in range(len(terms) - 1):
        j = justify_step(T, vs, terms[i], terms[i + 1])
        if j is None:
            return None, f"step {i+1} ({chain[i]} = {chain[i+1]}) is not a whole-term law application"
        justs.append(j)
    lines = [f"  calc {_render(terms[0])} = {_render(terms[1])} := {justs[0]}"]
    for i in range(1, len(justs)):
        lines.append(f"    _ = {_render(terms[i+1])} := {justs[i]}")
    body = "theorem solution : Problem.TrivialGoal := by\n  intro M op h a b\n" + "\n".join(lines) + "\n"
    return body, None


def build_prompt(law, feedback=None):
    p = f"""You are proving a magma law forces triviality — but you will NOT write Lean. You only
give the collapse chain; we formalize and check it.

Law:  {law}   (write the operation as ◇; the law holds for all inputs)
Goal: for arbitrary elements a and b, show a = b.

The law lets you rewrite ANY whole term in one step: `h e1 e2 ... : e1 = <law RHS with those args>`
(and its reverse). Give the sequence of terms from `a` to `b` where EACH adjacent pair differs by
ONE whole-term application of the law (rewrite the entire current term, not a piece of it).

Return ONLY JSON:  {{"chain": ["a", "<term>", "<term>", ..., "b"]}}
Use only a, b, ◇, and parentheses. First element must be "a", last must be "b".
Example (for the toy law x = y ◇ y):  {{"chain": ["a", "(a ◇ a)", "b"]}}"""
    if feedback:
        p += f"\n\nYour previous chain failed: {feedback}\nRe-route so every step is a whole-term step."
    return p


def parse_chain(content):
    import re
    m = re.search(r"\{.*\}", content, re.DOTALL)
    if not m:
        return None, "no JSON"
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return None, f"bad JSON: {e}"
    ch = obj.get("chain")
    if not isinstance(ch, list) or len(ch) < 2 or not all(isinstance(s, str) for s in ch):
        return None, "chain must be a list of term strings"
    return ch, None


def attempt(law, lean_dir, rounds, api_key, model, effort, timeout):
    import tempfile
    import llm_solve as L
    feedback = None
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for rnd in range(1, rounds + 1):
        try:
            content, u = L.call_llm(build_prompt(law, feedback), api_key, model, effort, timeout)
        except Exception as e:                          # noqa: BLE001
            return {"solved": False, "rounds_used": rnd, "error": f"api: {e}", "usage": usage}
        for k in usage:
            usage[k] += (u.get(k) or 0)
        ch, why = parse_chain(content)
        if ch is None:
            feedback = why; continue
        body, err = assemble(law, ch)
        if body is None:
            feedback = err; continue                    # bad step -> model re-routes
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, encoding="utf-8") as fh:
            fh.write(body); path = fh.name
        passed, rej = asp.judge(law, "trivial", path, lean_dir, timeout)
        os.unlink(path)
        if passed:
            return {"solved": True, "rounds_used": rnd, "chain": ch, "code": body, "usage": usage}
        feedback = "Lean rejected the assembled proof:\n" + "\n".join(rej[:5])
    return {"solved": False, "rounds_used": rounds, "last": feedback, "usage": usage}


def selftest():
    law = "x = y ◇ y"
    _, vs = _law(law)
    print("law vars (binder order):", vs)
    body, err = assemble(law, ["a", "(a ◇ a)", "b"])
    print("assemble err:", err, "\n---- assembled Lean body ----\n" + (body or ""))
    bad, berr = assemble(law, ["a", "(a ◇ b)", "b"])
    print("bad-chain (congruence) correctly rejected:", bad is None, "|", berr)


def main():
    import argparse, json, time
    import llm_trivial as T
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--laws-file"); ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--model", default="openai/o4-mini")
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--lean-dir", default="."); ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()
    if a.dry_run:
        selftest(); return
    if not a.laws_file or not a.out:
        ap.error("--laws-file and --out required unless --dry-run")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr); sys.exit(1)
    laws = T.load_trivial(a.laws_file)
    if a.n:
        laws = laws[:a.n]
    print(f"{len(laws)} trivial law(s); model={a.model} [autoformalizer rung]", file=sys.stderr)
    solved = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for i, law in enumerate(laws, 1):
            t0 = time.time()
            res = attempt(law, a.lean_dir, a.rounds, api_key, a.model, a.reasoning_effort, a.timeout)
            res.update({"law": law, "model": a.model, "secs": round(time.time() - t0, 1)})
            out.write(json.dumps(res, ensure_ascii=False) + "\n"); out.flush()
            solved += res["solved"]
            print(f"[{i}/{len(laws)}] {'SOLVED' if res['solved'] else '----'} "
                  f"{res['secs']}s  {law[:48]}", file=sys.stderr)
    print(f"done: {solved}/{len(laws)} -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
