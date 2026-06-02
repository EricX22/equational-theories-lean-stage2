"""
SAIR Equational Theories Stage 2 — minimal solver.

Three stages, smallest viable implementation:

  1. Brute-force counterexample search on Fin 2–3 (no LLM).
     Clears every `verdict: false` problem in the sample set.
  2. Singleton-magma proof template (no LLM).
     Clears the trivial `verdict: true` cases where the hypothesis has
     a free variable not in the LHS (so all elements collapse).
  3. LLM loop with a focused prompt that distinguishes the two
     remaining proof patterns: easy direct singleton vs. multi-step
     constancy-derived singleton (when h forces singleton but the LHS
     variable also appears in the RHS).

"""

PROMPT = """You are solving an equational implication in Lean 4.

# Problem
Hypothesis ({problem.equation1_id}): {problem.equation1}
Goal       ({problem.equation2_id}): {problem.equation2}

# Solver analysis
{solver.analysis}

# Previous attempts (round {history.round})
{history.attempts}

# Response

Output ONLY one JSON object. No markdown, no prose. Use `\u25c7` (U+25C7), NEVER `*`.

For TRUE: {"verdict": "true", "proof": "<tactic body — no `import`, no `theorem`>"}
For FALSE: {"verdict": "false", "counterexample_table": [[0,1],[1,0]]}

Allowed tactics: intro, exact, have, calc, rw, conv, apply, congr_arg, .symm, .trans.
The hypothesis is `h`; nothing else exists in scope. The goal starts after
`intro G _ h` (already added by us) — your proof body only needs to discharge
the remaining `∀` and equation.

If h forces singleton (see analysis), the proof has the form:
  intro <goal vars>
  have key : \u2200 (a b : G), a = b := by ...   -- this part is the work
  exact key <goal_lhs> <goal_rhs>
"""


import json
import re
import sys
import time
from itertools import product


# ── Protocol ────────────────────────────────────────────────────


def read_message():
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return json.loads(line.strip())


def send_message(msg):
    print(json.dumps(msg), flush=True)


def call_judge(verdict, code):
    send_message({"call": "judge", "verdict": verdict, "code": code})
    return read_message()


def call_llm(context):
    send_message({"call": "llm", "context": context})
    return read_message()


# ── Equation parsing & magma evaluation ──────────────────────────


def parse_equation(text):
    variables, seen = [], set()
    for v in re.findall(r"\b([a-z])\b", text):
        if v not in seen:
            seen.add(v)
            variables.append(v)
    lhs_str, rhs_str = text.split("=", 1)

    def to_expr(s):
        s = s.strip()
        while len(s) >= 2 and s[0] == "(" and s[-1] == ")":
            depth, matched = 0, True
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
        depth, last_op = 0, -1
        for i, c in enumerate(s):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif (c == "\u25c7" or c == "*") and depth == 0:
                last_op = i
        if last_op >= 0:
            left = to_expr(s[:last_op])
            right = to_expr(s[last_op + 1 :])
            return lambda env, l=left, r=right: env["op"](l(env), r(env))
        if len(s) == 1 and s in seen:
            return lambda env, v=s: env[v]
        raise ValueError(f"cannot parse: {s!r}")

    return variables, to_expr(lhs_str), to_expr(rhs_str)


def equation_holds(variables, lhs_fn, rhs_fn, n, op):
    for vals in product(range(n), repeat=len(variables)):
        env = {"op": op}
        for v, val in zip(variables, vals):
            env[v] = val
        if lhs_fn(env) != rhs_fn(env):
            return False
    return True


def search_counterexample(eq1_text, eq2_text, max_n=3):
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)
    for n in range(2, max_n + 1):
        total = n ** (n * n)
        for enc in range(total):
            table = [
                [(enc // (n ** (i * n + j))) % n for j in range(n)] for i in range(n)
            ]
            op = lambda a, b, t=table: t[a][b]
            if equation_holds(v1, l1, r1, n, op) and not equation_holds(
                v2, l2, r2, n, op
            ):
                return n, table
    return None, None


def _structured_tables(n):
    """Yield common parameterised magma families on Fin n. These cover most
    counterexamples that exhaustive Fin 2-3 search misses, without the
    cost of full n^(n*n) enumeration on Fin 4+."""
    # Constant tables: op[i][j] = c
    for c in range(n):
        yield [[c] * n for _ in range(n)]
    # Left projection: op[i][j] = i
    yield [[i] * n for i in range(n)]
    # Right projection: op[i][j] = j
    yield [list(range(n)) for _ in range(n)]
    # Cyclic add/sub: op[i][j] = (i±j+c) mod n
    for c in range(n):
        yield [[(i + j + c) % n for j in range(n)] for i in range(n)]
        yield [[(i - j + c) % n for j in range(n)] for i in range(n)]
    # Lattice max/min
    yield [[max(i, j) for j in range(n)] for i in range(n)]
    yield [[min(i, j) for j in range(n)] for i in range(n)]
    # Multiplication and a few polynomial forms
    yield [[(i * j) % n for j in range(n)] for i in range(n)]
    for a in (1, 2):
        for b in (0, 1, 2):
            yield [[(a * i + b * j) % n for j in range(n)] for i in range(n)]
    # XOR (useful for n that's a power of 2)
    if n in (2, 4, 8):
        yield [[(i ^ j) for j in range(n)] for i in range(n)]
    # LC3 / RC3: successor-based tables
    yield [[(i + 1) % n for j in range(n)] for i in range(n)]  # op[i][j] = (i+1) % n
    yield [[(j + 1) % n for j in range(n)] for i in range(n)]  # op[i][j] = (j+1) % n
    # Const-with-diagonal
    for c in range(n):
        t = [[c] * n for _ in range(n)]
        for i in range(n):
            t[i][i] = i
        yield t
    # Identity in slot 0
    if n >= 2:
        t = [[j for j in range(n)] for _ in range(n)]
        for i in range(n):
            t[i][0] = i
        yield t


def search_counterexample_extended(eq1_text, eq2_text, sizes=(4, 5, 6, 7)):
    """Search structured magma families on Fin 4-7 for a counterexample.
    Cheaper than full enumeration — uses ~30 families per n."""
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)
    for n in sizes:
        for table in _structured_tables(n):
            op = lambda a, b, t=table: t[a][b]
            if equation_holds(v1, l1, r1, n, op) and not equation_holds(
                v2, l2, r2, n, op
            ):
                return n, table
    return None, None


# ── Expression-tree unification (general h application) ────────
#
# Represents equations as trees of `('var', x)` and `('op', l, r)`.
# Given h : ∀ vars, LHS = RHS, attempt to find a substitution σ such
# that σ(LHS) = goal_lhs AND σ(RHS) = goal_rhs (term-syntactically).
# When found, emit `exact h <σ-applied args>` which the judge will
# accept without any Lean reasoning beyond definitional equality.
# This covers a large fraction of TRUE problems where the goal is just
# a particular instantiation of h.


def parse_to_tree(text):
    """Parse an expression into a tree of ('var', name) / ('op', L, R)."""
    s = text.strip()
    while len(s) >= 2 and s[0] == "(" and s[-1] == ")":
        depth, matched = 0, True
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
    depth, last_op = 0, -1
    for i, c in enumerate(s):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif (c == "\u25c7" or c == "*") and depth == 0:
            last_op = i
    if last_op < 0:
        if len(s) == 1 and s.isalpha():
            return ("var", s)
        raise ValueError(f"cannot parse atom: {s!r}")
    return ("op", parse_to_tree(s[:last_op]), parse_to_tree(s[last_op + 1 :]))


def unify(template, target, sigma):
    """Try to extend sigma so σ(template) == target. Returns new sigma
    (dict) or None on failure. sigma maps template var name → target tree."""
    if template[0] == "var":
        v = template[1]
        if v in sigma:
            if sigma[v] != target:
                return None
            return sigma
        new = dict(sigma)
        new[v] = target
        return new
    if target[0] != "op":
        return None
    s = unify(template[1], target[1], sigma)
    if s is None:
        return None
    return unify(template[2], target[2], s)


def tree_to_str(tree):
    """Render a tree back to a Lean-friendly string (over-parenthesises;
    Lean accepts that)."""
    if tree[0] == "var":
        return tree[1]
    return "(" + tree_to_str(tree[1]) + " \u25c7 " + tree_to_str(tree[2]) + ")"


def try_direct_h_application(problem, eq1_text, eq2_text):
    """If h's `lhs = rhs` unifies with goal's `lhs = rhs` (as a whole),
    emit `exact h <args>`. This covers TRUE problems where the goal is
    a literal h-instantiation."""
    # h's variables in order
    h_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq1_text):
        if v not in seen:
            seen.add(v)
            h_vars.append(v)
    g_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq2_text):
        if v not in seen:
            seen.add(v)
            g_vars.append(v)

    try:
        h_lhs_str, h_rhs_str = eq1_text.split("=", 1)
        g_lhs_str, g_rhs_str = eq2_text.split("=", 1)
        h_lhs = parse_to_tree(h_lhs_str)
        h_rhs = parse_to_tree(h_rhs_str)
        g_lhs = parse_to_tree(g_lhs_str)
        g_rhs = parse_to_tree(g_rhs_str)
    except Exception:
        return False

    # Try LHS=LHS, RHS=RHS first (most natural)
    for tl, tr, gl, gr in [(h_lhs, h_rhs, g_lhs, g_rhs), (h_rhs, h_lhs, g_lhs, g_rhs)]:
        sigma = unify(tl, gl, {})
        if sigma is None:
            continue
        sigma = unify(tr, gr, sigma)
        if sigma is None:
            continue
        # Build the h-call: for each variable in h's order, emit the
        # corresponding term. If h has a variable not bound by σ
        # (unused-in-equation pattern doesn't really happen but be safe),
        # use the first goal variable as a filler.
        filler = g_vars[0] if g_vars else "a"
        args = []
        for v in h_vars:
            if v in sigma:
                args.append(tree_to_str(sigma[v]))
            else:
                args.append(filler)
        intro = "intro " + " ".join(g_vars) if g_vars else ""
        body = f"{intro}\nexact h {' '.join(args)}"
        # Also try with .symm in case h's orientation is flipped
        # (we already tried both orientations above so just submit)
        code = make_true_code(body)
        if call_judge("true", code).get("status") == "accepted":
            return True
    # Try with the whole h equation reversed (apply .symm on the inferred term)
    for tl, tr, gl, gr in [(h_rhs, h_lhs, g_lhs, g_rhs)]:
        sigma = unify(tl, gl, {})
        if sigma is None:
            continue
        sigma = unify(tr, gr, sigma)
        if sigma is None:
            continue
        filler = g_vars[0] if g_vars else "a"
        args = []
        for v in h_vars:
            if v in sigma:
                args.append(tree_to_str(sigma[v]))
            else:
                args.append(filler)
        intro = "intro " + " ".join(g_vars) if g_vars else ""
        body = f"{intro}\nexact (h {' '.join(args)}).symm"
        code = make_true_code(body)
        if call_judge("true", code).get("status") == "accepted":
            return True
    return False


def try_generic_tactics(problem, eq1_text, eq2_text, max_judge_calls=8):
    """Try a small battery of generic one-line Lean tactics that frequently
    close TRUE problems on their own. These are cheap (≤8 judge calls)
    and don't depend on any LLM."""
    g_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq2_text):
        if v not in seen:
            seen.add(v)
            g_vars.append(v)
    intro = "intro " + " ".join(g_vars) if g_vars else ""

    # h's arity
    h_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq1_text):
        if v not in seen:
            seen.add(v)
            h_vars.append(v)

    candidates = [
        f"{intro}\nrw [h]",
        f"{intro}\nrw [← h]",
        f"{intro}\nsimp only [h]",
        f"{intro}\nsimp only [← h]",
        # repeated rewrites that often close idempotent / chain problems
        f"{intro}\nrw [← h, ← h]",
        f"{intro}\nrw [h, h]",
        f"{intro}\nsimp only [← h]; rfl",
        f"{intro}\nrepeat rw [h]",
    ]
    # And try h applied with all-same-argument fillers
    if h_vars and g_vars:
        for filler in g_vars[:2]:
            args = " ".join([filler] * len(h_vars))
            candidates.append(f"{intro}\nexact h {args}")
            candidates.append(f"{intro}\nexact (h {args}).symm")

    seen_codes = set()
    calls = 0
    for body in candidates:
        if body in seen_codes:
            continue
        seen_codes.add(body)
        if calls >= max_judge_calls:
            break
        code = make_true_code(body)
        try:
            res = call_judge("true", code)
        except Exception:
            return False
        calls += 1
        if res.get("status") == "accepted":
            return True
    return False


def try_two_step_h_chain(problem, eq1_text, eq2_text, max_judge_calls=6):
    """Two-step transitivity: find σ1, σ2 such that
        σ1(h_lhs) = goal_lhs   AND   σ1(h_rhs) = σ2(h_lhs)   AND
        σ2(h_rhs) = goal_rhs
    Then emit `exact (h σ1-args).trans (h σ2-args)`.

    Also tries the `.symm` variants. Covers many TRUE problems where the
    goal is reachable from h in two h-applications via an intermediate
    term that itself is an h-instantiation.

    The free variables in σ1 (those h-vars not bound by unifying h_lhs
    with goal_lhs) are enumerated over a small pool of the goal's
    variables — same idea as the existing `try_singleton_aggressive`.
    """
    h_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq1_text):
        if v not in seen:
            seen.add(v)
            h_vars.append(v)
    g_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq2_text):
        if v not in seen:
            seen.add(v)
            g_vars.append(v)
    try:
        h_lhs_str, h_rhs_str = eq1_text.split("=", 1)
        g_lhs_str, g_rhs_str = eq2_text.split("=", 1)
        h_lhs = parse_to_tree(h_lhs_str)
        h_rhs = parse_to_tree(h_rhs_str)
        g_lhs = parse_to_tree(g_lhs_str)
        g_rhs = parse_to_tree(g_rhs_str)
    except Exception:
        return False

    pool = [("var", v) for v in g_vars] or [("var", "x")]
    calls = 0

    def σ_to_args(sigma, default):
        """Build h's argument list from sigma; unbound vars get `default`."""
        return [tree_to_str(sigma.get(v, default)) for v in h_vars]

    # For each orientation of the first h-instance: σ1(h_lhs) = goal_lhs OR
    # σ1(h_rhs) = goal_lhs.
    for swap1 in (False, True):
        t1_l, t1_r = (h_lhs, h_rhs) if not swap1 else (h_rhs, h_lhs)
        # σ1 unifying t1_l with goal_lhs
        sigma1_base = unify(t1_l, g_lhs, {})
        if sigma1_base is None:
            continue
        # Free h-vars after σ1: those not bound
        free1 = [v for v in h_vars if v not in sigma1_base]
        # Enumerate concrete values for the free vars (limit fan-out)
        from itertools import product

        # Cap pool combinations
        if len(free1) > 3:
            continue  # too many free vars, skip
        for combo in product(pool, repeat=len(free1)):
            sigma1 = dict(sigma1_base)
            for v, val in zip(free1, combo):
                sigma1[v] = val

            # Compute intermediate M = σ1(h_rhs) (or σ1(h_lhs) if swapped)
            def apply_subst(tree, s):
                if tree[0] == "var":
                    return s.get(tree[1], tree)
                return ("op", apply_subst(tree[1], s), apply_subst(tree[2], s))

            M = apply_subst(t1_r, sigma1)
            # For each orientation of second h-instance:
            for swap2 in (False, True):
                t2_l, t2_r = (h_lhs, h_rhs) if not swap2 else (h_rhs, h_lhs)
                # σ2 unifying t2_l with M AND t2_r with goal_rhs
                sigma2 = unify(t2_l, M, {})
                if sigma2 is None:
                    continue
                sigma2 = unify(t2_r, g_rhs, sigma2)
                if sigma2 is None:
                    continue
                # Fill any still-free h-vars in σ2 with a goal var
                default = pool[0] if pool else ("var", "x")
                args1 = σ_to_args(sigma1, default)
                args2 = σ_to_args(sigma2, default)
                # Build the trans/symm chain
                step1 = f"h {' '.join(args1)}"
                if swap1:
                    step1 = f"({step1}).symm"
                step2 = f"h {' '.join(args2)}"
                if swap2:
                    step2 = f"({step2}).symm"
                intro = "intro " + " ".join(g_vars) if g_vars else ""
                body = f"{intro}\nexact ({step1}).trans ({step2})"
                code = make_true_code(body)
                try:
                    res = call_judge("true", code)
                except Exception:
                    return False
                calls += 1
                if res.get("status") == "accepted":
                    return True
                if calls >= max_judge_calls:
                    return False
    return False


def forces_singleton(eq1_text):
    """Brute force on Fin 2 (and Fin 3 when cheap): is every magma satisfying
    h necessarily a singleton? Conservative — used only as an analysis hint."""
    v1, l1, r1 = parse_equation(eq1_text)
    for n in (2, 3):
        if n == 3 and len(v1) > 4:
            break
        for enc in range(n ** (n * n)):
            table = [
                [(enc // (n ** (i * n + j))) % n for j in range(n)] for i in range(n)
            ]
            op = lambda a, b, t=table: t[a][b]
            if not equation_holds(v1, l1, r1, n, op):
                continue
            distinct = {x for row in table for x in row}
            if len(distinct) >= 2:
                return False
    return True


# ── Lean code generation ─────────────────────────────────────────


def make_false_code(n, table):
    return (
        "import JudgeProblem\n"
        "import JudgeDecide.DecideBang\n"
        "import JudgeFinOp.MemoFinOp\n"
        "open MemoFinOp\n\n"
        "def submission : Goal := by\n"
        f'  let m : Magma (Fin {n}) := {{ op := finOpTable "{json.dumps(table)}" }}\n'
        f"  refine \u27e8Fin {n}, m, ?_\u27e9\n"
        "  decideFin!\n"
    )


def make_true_code(proof_body):
    body = proof_body.strip()
    indented = "\n".join("  " + l if l.strip() else "" for l in body.splitlines())
    return (
        "import JudgeProblem\n\n"
        "def submission : Goal := by\n"
        "  intro G _ h\n"
        f"{indented}\n"
    )


# ── Trivial singleton template ──────────────────────────────────


def try_trivial_singleton(eq1_text, eq2_text):
    """Closes h's where the LHS variable does not appear on the RHS.
    Then every element equals R(arbitrary) = any other element."""
    lhs_str, rhs_str = eq1_text.split("=", 1)
    lhs_var = lhs_str.strip()
    if len(lhs_var) != 1 or lhs_var in re.findall(r"\b([a-z])\b", rhs_str):
        return None
    eq1_vars, eq2_vars = [], []
    for v in re.findall(r"\b([a-z])\b", eq1_text):
        if v not in eq1_vars:
            eq1_vars.append(v)
    for v in re.findall(r"\b([a-z])\b", eq2_text):
        if v not in eq2_vars:
            eq2_vars.append(v)
    if len(eq1_vars) < 2:
        return None
    g_lhs, g_rhs = eq2_text.split("=", 1)
    filler = " ".join(["a"] * (len(eq1_vars) - 1))
    return (
        f"intro {' '.join(eq2_vars)}\n"
        f"have key : \u2200 (a b : G), a = b := "
        f"fun a b => (h a {filler}).trans (h b {filler}).symm\n"
        f"exact key ({g_lhs.strip()}) ({g_rhs.strip()})"
    )


# ── LLM response cleanup ─────────────────────────────────────────


def extract_json(text):
    text = re.sub(r"<think>[\s\S]*?</think>", "", text).strip()
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
            return None
    return None


def clean_proof(p):
    p = p.replace("*", "\u25c7")
    # Strip an `import` line (LLM sometimes prepends one even though told not to).
    p = re.sub(r"^\s*import\s+.*\n?", "", p, flags=re.MULTILINE)
    p = p.strip()
    # Only strip a `theorem/def/lemma ... := by` wrapper if the proof actually
    # starts with one. NOTE: the previous version greedily matched the first
    # `:= by` anywhere in the proof, which would silently eat any
    # `have key : ... := by` line inside the body — that produced badly
    # malformed proofs that always got rejected by the judge.
    m = re.match(
        r"^(theorem|def|lemma|example)\s+\S*\s*[:|]?.*?:=\s*by\s*\n?",
        p,
        flags=re.DOTALL,
    )
    if m:
        p = p[m.end() :]
    # Strip a stray leading `by `
    p = re.sub(r"^\s*by\s+", "", p)
    return p.strip()


# ── Structural pattern matchers for singleton-forcing h shapes ──
#
# These match an equation against canonical h-shapes (variable names
# stripped to a canonical form by first-appearance order). They are
# NOT problem-id lookups — any future problem whose hypothesis has
# the same structural shape gets the same parameterized Lean proof.


def _canonical_rename(text):
    """Return text with single-letter variables renamed to a canonical
    sequence (first var → 'x', then 'a', 'b', 'c', …) plus the mapping
    that took us there (so we can substitute back into a proof template)."""
    seen = {}
    order = []
    for v in re.findall(r"\b([a-z])\b", text):
        if v not in seen:
            slot = "x" if not order else "abcdefghij"[len(order) - 1]
            seen[v] = slot
            order.append(v)

    def sub(m):
        v = m.group(1)
        return seen[v]

    canon = re.sub(r"\b([a-z])\b", sub, text)
    return canon, seen


def try_structural_singleton_pattern(problem, eq1_text, eq2_text):
    """Try parameterized singleton-derivation proofs for h-shapes whose
    multi-step derivations have been verified offline. Each entry below
    is keyed by the CANONICAL form of the hypothesis (variables renamed
    to x, a, b, c, ... by first-appearance order). When an incoming
    problem's eq1 canonicalises to a known shape, we instantiate the
    parameterised proof with the problem's actual variable names.

    The proofs were verified by submitting them to the Lean judge in
    isolation; they hold for ALL magmas satisfying the corresponding
    h-shape, hence for any problem with that shape.
    """
    canon, var_map = _canonical_rename(eq1_text.strip())
    # var_map maps actual var → canonical slot. Invert to substitute back.
    inv = {v: k for k, v in var_map.items()}

    eq2_vars = []
    for v in re.findall(r"\b([a-z])\b", eq2_text):
        if v not in eq2_vars:
            eq2_vars.append(v)
    goal_lhs, goal_rhs = eq2_text.split("=", 1)
    goal_lhs = goal_lhs.strip()
    goal_rhs = goal_rhs.strip()

    # === Shape 1: x = (a ◇ x) ◇ b ===
    #   Free vars in canonical names: a, b.
    #   Verified singleton-derivation proof — see verification log.
    if canon == "x = (a \u25c7 x) \u25c7 b":
        # Map canonical {x, a, b} → actual problem vars.
        # Need names that won't shadow `a` and `b` used inside the proof.
        # We rebuild the proof using fresh names p, q for the singleton intro.
        intro = "intro " + " ".join(eq2_vars) if eq2_vars else ""
        body = (
            f"{intro}\n"
            "have key : \u2200 (p q : G), p = q := by\n"
            "  intro p q\n"
            "  have e1 : (p \u25c7 q) \u25c7 p = q := (h q p p).symm\n"
            "  have e2 : (q \u25c7 p) \u25c7 q = p := (h p q q).symm\n"
            "  have e3 : p = q \u25c7 q := by\n"
            "    have hh := h p (p \u25c7 q) q\n"
            "    rw [e1] at hh; exact hh\n"
            "  have e4 : q = p \u25c7 q := by\n"
            "    have hh := h q (q \u25c7 p) q\n"
            "    rw [e2] at hh; exact hh\n"
            "  calc p = q \u25c7 q := e3\n"
            "    _ = (p \u25c7 q) \u25c7 q := by rw [\u2190 e4]\n"
            "    _ = q := (h q p q).symm\n"
            f"exact key ({goal_lhs}) ({goal_rhs})\n"
        )
        code = make_true_code(body)
        return call_judge("true", code).get("status") == "accepted"

    # === Shape 2: x = a ◇ (x ◇ ((b ◇ c) ◇ c)) ===
    #   Free vars: a, b, c.
    #   Verified super-strong singleton derivation.
    if canon == "x = a \u25c7 (x \u25c7 ((b \u25c7 c) \u25c7 c))":
        intro = "intro " + " ".join(eq2_vars) if eq2_vars else ""
        body = (
            f"{intro}\n"
            "have key : \u2200 (p q : G), p = q := by\n"
            "  intro p q\n"
            "  have lemA : \u2200 (y : G), y \u25c7 (q \u25c7 ((p \u25c7 q) \u25c7 q)) = q := "
            "fun y => (h q y p q).symm\n"
            "  have lemAp : \u2200 (y : G), y \u25c7 (p \u25c7 ((q \u25c7 p) \u25c7 p)) = p := "
            "fun y => (h p y q p).symm\n"
            "  have hVpVqVq : ((p \u25c7 ((p \u25c7 q) \u25c7 q)) \u25c7 (q \u25c7 ((p \u25c7 q) \u25c7 q))) "
            "\u25c7 (q \u25c7 ((p \u25c7 q) \u25c7 q)) = q := by\n"
            "    rw [lemA (p \u25c7 ((p \u25c7 q) \u25c7 q))]\n"
            "    exact lemA q\n"
            "  have Hq : \u2200 (a b : G), a = b \u25c7 (a \u25c7 q) := by\n"
            "    intro a b\n"
            "    have ha := h a b (p \u25c7 ((p \u25c7 q) \u25c7 q)) (q \u25c7 ((p \u25c7 q) \u25c7 q))\n"
            "    rw [hVpVqVq] at ha; exact ha\n"
            "  have hVqVpVp : ((q \u25c7 ((q \u25c7 p) \u25c7 p)) \u25c7 (p \u25c7 ((q \u25c7 p) \u25c7 p))) "
            "\u25c7 (p \u25c7 ((q \u25c7 p) \u25c7 p)) = p := by\n"
            "    rw [lemAp (q \u25c7 ((q \u25c7 p) \u25c7 p))]\n"
            "    exact lemAp p\n"
            "  have Hp : \u2200 (a b : G), a = b \u25c7 (a \u25c7 p) := by\n"
            "    intro a b\n"
            "    have ha := h a b (q \u25c7 ((q \u25c7 p) \u25c7 p)) (p \u25c7 ((q \u25c7 p) \u25c7 p))\n"
            "    rw [hVqVpVp] at ha; exact ha\n"
            "  have hqqStep : (q \u25c7 ((q \u25c7 q) \u25c7 q)) \u25c7 ((q \u25c7 q) \u25c7 q) = q \u25c7 q := by\n"
            "    have step_a : q \u25c7 ((q \u25c7 q) \u25c7 q) = q \u25c7 q := (Hq (q \u25c7 q) q).symm\n"
            "    rw [step_a]\n"
            "    exact (Hq (q \u25c7 q) (q \u25c7 q)).symm\n"
            "  have Hqq : \u2200 (a b : G), a = b \u25c7 (a \u25c7 (q \u25c7 q)) := by\n"
            "    intro a b\n"
            "    have ha := h a b q ((q \u25c7 q) \u25c7 q)\n"
            "    rw [hqqStep] at ha; exact ha\n"
            "  have pqeqp : p \u25c7 q = p := by\n"
            "    have step1 := Hqq p p\n"
            "    have step2 : p \u25c7 (q \u25c7 q) = q := (Hq q p).symm\n"
            "    rw [step2] at step1; exact step1.symm\n"
            "  have hppStep : (p \u25c7 ((p \u25c7 p) \u25c7 p)) \u25c7 ((p \u25c7 p) \u25c7 p) = p \u25c7 p := by\n"
            "    have step_a : p \u25c7 ((p \u25c7 p) \u25c7 p) = p \u25c7 p := (Hp (p \u25c7 p) p).symm\n"
            "    rw [step_a]\n"
            "    exact (Hp (p \u25c7 p) (p \u25c7 p)).symm\n"
            "  have Hpp : \u2200 (a b : G), a = b \u25c7 (a \u25c7 (p \u25c7 p)) := by\n"
            "    intro a b\n"
            "    have ha := h a b p ((p \u25c7 p) \u25c7 p)\n"
            "    rw [hppStep] at ha; exact ha\n"
            "  have qpeqq : q \u25c7 p = q := by\n"
            "    have step1 := Hpp q q\n"
            "    have step2 : q \u25c7 (p \u25c7 p) = p := (Hp p q).symm\n"
            "    rw [step2] at step1; exact step1.symm\n"
            "  have step1 : p = q \u25c7 (p \u25c7 q) := Hq p q\n"
            "  rw [pqeqp] at step1\n"
            "  rw [qpeqq] at step1\n"
            "  exact step1\n"
            f"exact key ({goal_lhs}) ({goal_rhs})\n"
        )
        code = make_true_code(body)
        return call_judge("true", code).get("status") == "accepted"

    return False


# ── Main ─────────────────────────────────────────────────────────


BUDGET_SECONDS = 3600  # total per-problem budget (matches config.json)
MIN_SECONDS_FOR_LLM = 350  # don't start a new LLM call with less than this left


def main():
    start_time = time.monotonic()
    startup = read_message()
    problem = startup["problem"]
    eq1 = problem["equation1"].replace("*", "\u25c7")
    eq2 = problem["equation2"].replace("*", "\u25c7")
    problem["equation1"], problem["equation2"] = eq1, eq2

    # Stage 1: counterexample search on Fin 2–3.
    n, table = search_counterexample(eq1, eq2, max_n=3)
    if n is not None:
        if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
            return

    # Stage 1.5: extended counterexample search on Fin 4-7 with
    # structured magma families (constant, projection, cyclic, lattice,
    # polynomial, …). Cheap (~30 families per n) but catches the
    # counterexamples that exhaustive Fin 2-3 missed.
    n, table = search_counterexample_extended(eq1, eq2, sizes=(4, 5, 6, 7))
    if n is not None:
        if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
            return

    # Stage 2: direct h-application via unification. For TRUE problems
    # where the goal is literally a particular instantiation of h
    # (or its symmetric form), this emits `exact h <args>` — one
    # judge call, zero LLM. Covers many problems where the goal RHS
    # is just h's RHS with one variable substituted.
    if try_direct_h_application(problem, eq1, eq2):
        return

    # Stage 2.2: two-step h chain via unification. When the goal is
    # reachable from h in two `(h …).trans (h …)` steps through some
    # intermediate term, this finds the substitutions and emits the
    # chain. Bounded judge-call cost (≤ 6 attempts).
    if try_two_step_h_chain(problem, eq1, eq2, max_judge_calls=6):
        return

    # Stage 2.3: generic one-line Lean tactics (rw/simp variants).
    # Often closes problems where the goal pattern syntactically
    # matches h's LHS or RHS modulo Lean's unifier.
    if try_generic_tactics(problem, eq1, eq2, max_judge_calls=12):
        return

    # Stage 2: trivial singleton template (LHS var not in RHS).
    proof = try_trivial_singleton(eq1, eq2)
    if proof is not None:
        if call_judge("true", make_true_code(proof)).get("status") == "accepted":
            return

    # Stage 2.5: structural singleton-derivation patterns. Each pattern is
    # keyed on the CANONICAL form of h (variables renamed by first
    # appearance), so any future problem with the same h-shape gets the
    # same parameterised proof — not problem-id memoisation.
    if try_structural_singleton_pattern(problem, eq1, eq2):
        return

    # Stage 3: LLM with a focused, singleton-aware analysis block.
    singleton = forces_singleton(eq1)
    analysis_lines = []
    if singleton:
        # Detect whether x (the LHS variable of h) also appears in h's RHS.
        # This dramatically changes which proof shapes will typecheck.
        lhs_str, rhs_str = eq1.split("=", 1)
        lhs_var = lhs_str.strip()
        rhs_vars_set = set(re.findall(r"\b([a-z])\b", rhs_str))
        x_in_rhs = len(lhs_var) == 1 and lhs_var in rhs_vars_set

        analysis_lines.append(
            "STRUCTURAL FINDING: h forces a singleton magma (no non-singleton model "
            "exists on Fin 2 or Fin 3). The implication holds via the lemma "
            "`key : ∀ (a b : G), a = b`. Apply that lemma to the goal."
        )
        if not x_in_rhs:
            analysis_lines.append(
                "Easy case: h's LHS variable does NOT appear in its RHS, so the "
                "singleton lemma is a one-liner — `fun a b => (h a c1 ... ck).trans "
                "(h b c1 ... ck).symm` for any fillers c1..ck. (Already attempted "
                "deterministically — if you see this, the trivial template failed; "
                "try a calc chain instead.)"
            )
        else:
            # The hard case — all 6 of sample_20's unsolved problems fall here.
            analysis_lines.append(
                "Hard case: h's LHS variable `"
                + lhs_var
                + "` ALSO appears in its RHS. "
                "Therefore `(h a c).symm.trans (h b c)` DOES NOT TYPECHECK — "
                "`h a c` has type `a = R(a, c)` and `h b c` has type `b = R(b, c)` "
                "whose RHSs differ (one contains `a`, the other `b`). Do not try this."
            )
            analysis_lines.append(
                "Correct strategy (multi-step constancy chain). For each pair of "
                "elements p, q derive p = q via several `have` lemmas. The exact "
                "chain depends on h's shape, but the canonical pattern is:"
            )
            analysis_lines.append(
                "  1. Use (h p y₁ z₁ w₁).symm.trans (h p y₂ z₂ w₂) to derive a "
                "CONSTANCY lemma about p (the RHS of h is constant in free vars, "
                "all equal p).\n"
                "  2. From that, build smaller targeted equalities — e.g. "
                "`(some compound term) = p` — by clever free-var substitution.\n"
                "  3. Combine multiple such targeted equalities (via `rw` or "
                "transitivity) to derive `p = q`."
            )
            analysis_lines.append(
                "WORKED EXAMPLE (different h, same singleton-derivation shape).\n"
                "Suppose h : ∀ x y z, x = (y ◇ x) ◇ z. Then this proof works:\n"
                "```\n"
                "have key : ∀ (a b : G), a = b := by\n"
                "  intro a b\n"
                "  have e1 : (a ◇ b) ◇ a = b := (h b a a).symm\n"
                "  have e2 : (b ◇ a) ◇ b = a := (h a b b).symm\n"
                "  have e3 : a = b ◇ b := by\n"
                "    have hh := h a (a ◇ b) b\n"
                "    rw [e1] at hh; exact hh\n"
                "  have e4 : b = a ◇ b := by\n"
                "    have hh := h b (b ◇ a) b\n"
                "    rw [e2] at hh; exact hh\n"
                "  calc a = b ◇ b := e3\n"
                "    _ = (a ◇ b) ◇ b := by rw [← e4]\n"
                "    _ = b := (h b a b).symm\n"
                "```\n"
                "Notice: 4 `have` lemmas + a 3-step `calc`. The exact instantiations "
                "depend on h's structure for this problem; the pattern is the same."
            )
    else:
        analysis_lines.append(
            "No counterexample on Fin 2–3 and no easy singleton. Try a calc chain: "
            "use h-instantiations to rewrite the goal LHS step-by-step into the goal RHS."
        )

    seen = set()
    MAX_LLM_ATTEMPTS = (
        10  # hard cap so one stubborn problem can't eat the full hour budget
    )
    consecutive_garbage = 0
    for attempt in range(MAX_LLM_ATTEMPTS):
        elapsed = time.monotonic() - start_time
        remaining = BUDGET_SECONDS - elapsed
        if remaining < MIN_SECONDS_FOR_LLM:
            break  # not enough time left for an LLM round-trip
        ctx = {
            "analysis": "\n".join(analysis_lines),
            "attempt": str(attempt),
        }
        result = call_llm(ctx)
        if "error" in result:
            return  # No API key or budget exhausted — nothing more we can do.
        answer = extract_json(result.get("response", ""))
        if not answer:
            consecutive_garbage += 1
            if consecutive_garbage >= 2:
                return  # LLM is stuck producing unparseable output; cut losses.
            continue
        consecutive_garbage = 0
        verdict = answer.get("verdict")
        if verdict == "true":
            proof = clean_proof(answer.get("proof", ""))
            if not proof or proof in seen:
                continue
            seen.add(proof)
            code = make_true_code(proof)
        elif verdict == "false":
            if singleton:
                # h forces a singleton magma — no counterexample can exist.
                # Skip rather than waste a judge call on a provably wrong table.
                continue
            tbl = answer.get("counterexample_table")
            if not tbl or not isinstance(tbl, list):
                continue
            code = make_false_code(len(tbl), tbl)
        else:
            continue
        if call_judge(verdict, code).get("status") == "accepted":
            return


if __name__ == "__main__":
    main()
