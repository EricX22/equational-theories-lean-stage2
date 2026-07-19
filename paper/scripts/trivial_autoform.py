#!/usr/bin/env python3
"""trivial_autoform.py — the autoformalizer rung for the trivial side.

Removes the formalization wall: the model emits ONLY a chain of terms
    [a, t1, t2, ..., b]
where each adjacent pair is one WHOLE-TERM application of the law (forward or backward).
The harness finds the law instance for each step by first-order matching and assembles a Lean
`calc` — the model never writes Lean. This isolates reasoning (find the path) from
formalization (handled here), so a model that is formalization-bound can still register a solve.

Each step is ONE application of the law at a single position — whole-term OR inside a subterm
(congruence-aware: the harness emits `congrArg` down to the differing position). A step that
changes two positions at once is rejected with a message so the model splits it.

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


def _wholeterm(T, vs, s, t):
    """Lean term for `s = t` as one WHOLE-TERM law application, or None."""
    for direction in ("fwd", "rev"):
        src, dst = (s, t) if direction == "fwd" else (t, s)
        subst = {"x": src}
        if _match(T, dst, subst):
            args = [_render(subst.get(v, ("var", "a"))) for v in vs]   # unbound var: any element
            term = f"h {' '.join(args)}"
            return term if direction == "fwd" else f"({term}).symm"
    return None


def justify_step(T, vs, s, t):
    """Lean term for `s = t` as one law application at ANY position (congruence-aware).

    Whole-term first; else descend into the single differing child, wrapping the sub-proof in
    `congrArg (fun z => op z R)` / `congrArg (fun z => op L z)`. Exactly one child may differ
    (a single law application rewrites one position)."""
    if s == t:
        return None
    wt = _wholeterm(T, vs, s, t)
    if wt:
        return wt
    if s[0] == "op" and t[0] == "op":
        ld, rd = s[1] != t[1], s[2] != t[2]
        if ld and not rd:
            sub = justify_step(T, vs, s[1], t[1])
            if sub:
                return f"congrArg (fun z => op z {_render(s[2])}) ({sub})"
        elif rd and not ld:
            sub = justify_step(T, vs, s[2], t[2])
            if sub:
                return f"congrArg (fun z => op {_render(s[1])} z) ({sub})"
    return None


# --- gap-filling: bridge a coarse step with a few single law applications --------
GAP_K = 3                                            # max law applications per bridged gap

def _subterms(node, pos=()):
    out = [(pos, node)]
    if node[0] == "op":
        out += _subterms(node[1], pos + (1,))
        out += _subterms(node[2], pos + (2,))
    return out

def _replace(node, pos, new):
    if not pos:
        return new
    if pos[0] == 1:
        return ("op", _replace(node[1], pos[1:], new), node[2])
    return ("op", node[1], _replace(node[2], pos[1:], new))

def _reduce_neighbors(u, T):
    """Terms one REVERSE law application from u: a subterm matching the law RHS `T` collapses
    to its x-value. Reverse apps strictly shrink the term, so search is finite."""
    out = []
    for pos, sub in _subterms(u):
        subst = {}
        if _match(T, sub, subst) and "x" in subst:
            nu = _replace(u, pos, subst["x"])
            if nu != u and nu not in out:
                out.append(nu)
    return out

def _find_path(a, b, T, k):
    from collections import deque
    if a == b:
        return [a]
    seen = {a}; q = deque([[a]])
    while q:
        path = q.popleft()
        if len(path) - 1 >= k:
            continue
        for nb in _reduce_neighbors(path[-1], T):
            if nb in seen:
                continue
            np = path + [nb]
            if nb == b:
                return np
            seen.add(nb); q.append(np)
    return None

def _bridge(s, t, T, k):
    """A path s -> ... -> t of ≤k single law applications (reductions, either direction)."""
    p = _find_path(s, t, T, k)
    if p:
        return p
    p = _find_path(t, s, T, k)
    return p[::-1] if p else None


def assemble(law, chain):
    """chain = list of ◇-term strings, chain[0]='a', chain[-1]='b'. Coarse steps are bridged
    by up to GAP_K single law applications, so the model only needs waypoints. -> (lean, err)."""
    if len(chain) < 2:
        return None, "chain too short"
    try:
        terms = [et.parse_term(c) for c in chain]
    except Exception as e:                          # noqa: BLE001
        return None, f"unparsable term: {e}"
    if terms[0] != ("var", "a") or terms[-1] != ("var", "b"):
        return None, "chain must start at `a` and end at `b`"
    T, vs = _law(law)
    expanded = [terms[0]]                           # gap-fill to atomic single-application steps
    for i in range(len(terms) - 1):
        s, t = expanded[-1], terms[i + 1]
        if s == t:
            continue
        if justify_step(T, vs, s, t) is not None:
            expanded.append(t); continue
        path = _bridge(s, t, T, GAP_K)
        if path is None:
            return None, (f"step {i+1} ({chain[i]} = {chain[i+1]}) is not a law application and "
                          f"could not be bridged within {GAP_K} steps")
        expanded.extend(path[1:])
    justs = []
    for i in range(len(expanded) - 1):
        j = justify_step(T, vs, expanded[i], expanded[i + 1])
        if j is None:
            return None, f"internal: bridged step {i+1} unjustifiable"
        justs.append(j)
    lines = [f"  calc {_render(expanded[0])} = {_render(expanded[1])} := {justs[0]}"]
    for i in range(1, len(justs)):
        lines.append(f"    _ = {_render(expanded[i+1])} := {justs[i]}")
    body = "theorem solution : Problem.TrivialGoal := by\n  intro M op h a b\n" + "\n".join(lines) + "\n"
    return body, None


def build_prompt(law, feedback=None, waypoints=None):
    hint_block = ""
    if waypoints:
        hint_block = ("\n\nThe collapse passes through these consequences of the law (aim your chain "
                      "through them; each is derivable from the law):\n"
                      + "\n".join(f"    - {w}" for w in waypoints))
    p = f"""You are proving a magma law forces triviality. You will NOT write Lean — you give only a
sequence of terms, and a theorem prover checks each step.

Law:  {law}
Read it as a rewrite rule. Write the law as  L = R, where L is the single variable on the left and
R is the big right-hand term. ONE step does exactly one of:
  • pick any subterm `e` of the current term and replace that ONE occurrence with R, taking L := e
    (so `e` becomes R with the law's left variable set to `e`); OR
  • the reverse — replace a subterm that exactly matches an instance of R by the corresponding `e`.
Everything OUTSIDE that one chosen subterm stays byte-for-byte identical.

Goal: build  a = t1 = t2 = ... = b. Adjacent terms should be only a FEW (1–3) such steps apart —
you may skip intermediate terms and the checker will fill short gaps automatically, so give
WAYPOINTS, not necessarily every atomic step. Prefer smaller jumps.

HARD RULES — a jump breaking any of these is rejected, so self-check each one before writing it:
  • You may NOT write "a = b" or otherwise relate a and b directly. They are opaque atoms; the only
    way to connect them is through the law. (A jump like `a → b`, or a subterm `a → b`, is illegal.)
  • Each jump must be a GENUINE short derivation — at most ~3 single law applications apart. A leap
    between unrelated terms cannot be bridged and is rejected.
  • Every application is a REAL instance: a subterm `e → R[L:=e]` (or its reverse) for some choice of
    the law's other variables. If you can't name that instance, the step is invalid.

STRATEGY: rewrite FORWARD from `a` (each rewrite grows the term via the law) toward a term the law
forces to collapse — these laws let you derive `op(_, _) = (any element)`; once both `a` and `b`
reduce to a common term, the chain closes.{hint_block}

Return ONLY JSON:  {{"chain": ["a", "<term>", ..., "b"]}}   first "a", last "b"; use only a, b, ◇, ().
Example (toy law  x = y ◇ y):  {{"chain": ["a", "(a ◇ a)", "b"]}}
  step 1: `a` → `(a ◇ a)` — the law with x:=a, y:=a gives  a = a◇a. ✓
  step 2: `(a ◇ a)` → `b` — reverse: the law with x:=b, y:=a gives  b = a◇a, so  a◇a = b. ✓
Only write steps you can justify this way."""
    if feedback:
        p += (f"\n\nYour previous chain was REJECTED: {feedback}\n"
              "That step was not a single valid law application. Re-route so EVERY step rewrites one "
              "subterm as a real instance of the law, and never jump between a and b directly.")
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
    import trivial_hints as H
    try:
        waypoints = H.lemmas(law)                   # Vampire-derived collapse lemmas as hints
    except Exception:                               # noqa: BLE001
        waypoints = None
    feedback = None
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for rnd in range(1, rounds + 1):
        try:
            content, u = L.call_llm(build_prompt(law, feedback, waypoints), api_key, model, effort, timeout)
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
    T, vs = _law(law)
    print("law vars (binder order):", vs)
    body, err = assemble(law, ["a", "(a ◇ a)", "b"])
    print("whole-term assemble err:", err, "\n---- assembled Lean body ----\n" + (body or ""))
    # congruence: rewrite the LEFT child  a -> (a ◇ a)  inside (a ◇ c), keeping c fixed
    s = et.parse_term("(a ◇ c)"); t = et.parse_term("((a ◇ a) ◇ c)")
    print("congruence step ->", justify_step(T, vs, s, t))
    # gap-filling: law with x in T; bridge a 2-reduction coarse gap  ((a◇p)◇q) -> a
    T2, _ = _law("x = (x ◇ y)")
    path = _bridge(et.parse_term("((a ◇ p) ◇ q)"), et.parse_term("a"), T2, 3)
    print("bridge coarse gap ->", [_render(x) for x in path] if path else None)


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
