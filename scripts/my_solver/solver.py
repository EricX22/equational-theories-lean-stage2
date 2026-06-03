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

# ── Timing budget ────────────────────────────────────────────────
# Total wall-clock seconds the solver is expected to run. Used to
# avoid starting an LLM call when too little time is left.
BUDGET_SECONDS = 110
MIN_SECONDS_FOR_LLM = 8


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

def trace(msg):
    """Write lightweight solver-stage diagnostics to stderr.

    These show up in solver_stderr logs without interfering with the
    JSON stdin/stdout protocol used by the proxy.
    """
    print(msg, file=sys.stderr, flush=True)


def has_bare_side(eq_text):
    """True if Eq1 has a bare variable on either side.

    For equations like x = RHS or RHS = x, generic rw [h] often fails
    because Lean sees the rewrite pattern as a metavariable. In those
    cases, skip the generic tactic battery and use graph/singleton search.
    """
    lhs, rhs = eq_text.split("=", 1)
    lhs = lhs.strip()
    rhs = rhs.strip()
    return (len(lhs) == 1 and lhs.isalpha()) or (len(rhs) == 1 and rhs.isalpha())


def goal_vars(eq_text):
    """Variables in first-appearance order."""
    out = []
    for v in re.findall(r"\b([a-z])\b", eq_text):
        if v not in out:
            out.append(v)
    return out


def intro_arity_ok(proof, eq2_text):
    """Filter LLM proofs that introduce too many/few goal variables."""
    vars_needed = goal_vars(eq2_text)
    lines = [line.strip() for line in proof.splitlines() if line.strip()]
    if not lines:
        return False
    if not lines[0].startswith("intro "):
        return True
    got = lines[0].split()[1:]
    return len(got) == len(vars_needed)

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


def search_named_witnesses(eq1_text, eq2_text):
    """Check a small set of named magma tables as counterexample witnesses.

    Returns (name, n, table) if any table satisfies eq1 and violates eq2,
    or (None, None, None) if none match.
    """
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)

    named = {
        "LP2":      (2, [[0, 0], [1, 1]]),
        "RP2":      (2, [[0, 1], [0, 1]]),
        "XOR2":     (2, [[0, 1], [1, 0]]),
        "LC3":      (3, [[0, 0, 0], [1, 1, 1], [2, 2, 2]]),
        "RC3":      (3, [[0, 1, 2], [0, 1, 2], [0, 1, 2]]),
        "Z3":       (3, [[0, 1, 2], [1, 2, 0], [2, 0, 1]]),
        "MAX3":     (3, [[0, 1, 2], [1, 1, 2], [2, 2, 2]]),
        "MIN3":     (3, [[0, 0, 0], [0, 1, 1], [0, 1, 2]]),
        "FLIP3":    (3, [[2, 2, 2], [1, 1, 1], [0, 0, 0]]),
        "CONST3_0": (3, [[0]*3]*3),
        "CONST3_1": (3, [[1]*3]*3),
        "XOR4":     (4, [[(i ^ j) for j in range(4)] for i in range(4)]),
        "Z4":       (4, [[(i + j) % 4 for j in range(4)] for i in range(4)]),
        "LP4":      (4, [[i] * 4 for i in range(4)]),
        "RP4":      (4, [list(range(4)) for _ in range(4)]),
        "MAX4":     (4, [[max(i, j) for j in range(4)] for i in range(4)]),
        "MIN4":     (4, [[min(i, j) for j in range(4)] for i in range(4)]),
    }

    for name, (n, table) in named.items():
        op = lambda a, b, t=table: t[a][b]
        if equation_holds(v1, l1, r1, n, op) and not equation_holds(v2, l2, r2, n, op):
            return name, n, table

    return None, None, None


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



def _perturb_table_one_cell(table):
    """Yield tables that differ from `table` in exactly one cell.

    This is the first step toward constraint-guided finite model search:
    rather than enumerating all n^(n*n) magmas, search the local
    neighborhood of operation families that often work as witnesses.
    """
    n = len(table)
    for i in range(n):
        for j in range(n):
            old = table[i][j]
            for val in range(n):
                if val == old:
                    continue
                t = [row[:] for row in table]
                t[i][j] = val
                yield t


def search_perturbed_witnesses(eq1_text, eq2_text, sizes=(2, 3, 4), max_bases_per_n=24):
    """Try one-cell perturbations around structured tables.

    False proofs are finite-model search. A fully exhaustive Fin 4 search is
    impossible, but many useful witnesses are near a simple algebraic family.
    This stage uses those families to define a much smaller targeted search.
    """
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)
    seen = set()
    for n in sizes:
        base_count = 0
        for base in _structured_tables(n):
            base_count += 1
            if base_count > max_bases_per_n:
                break
            for table in _perturb_table_one_cell(base):
                key = tuple(tuple(row) for row in table)
                if key in seen:
                    continue
                seen.add(key)
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



def tree_size(tree):
    if tree[0] == "var":
        return 1
    return 1 + tree_size(tree[1]) + tree_size(tree[2])


def subterms(tree):
    out = [tree]
    if tree[0] == "op":
        out.extend(subterms(tree[1]))
        out.extend(subterms(tree[2]))
    return out


def apply_subst_tree(tree, subst):
    if tree[0] == "var":
        return subst.get(tree[1], tree)
    return ("op", apply_subst_tree(tree[1], subst), apply_subst_tree(tree[2], subst))


def ordered_unique(seq, max_items=None):
    out, seen = [], set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
        if max_items is not None and len(out) >= max_items:
            break
    return out


def generate_candidate_terms(var_names, seed_terms=(), max_depth=2, max_terms=36, max_size=9):
    """Generate a small, ordered candidate term universe for true-proof search."""
    base = [("var", v) for v in var_names]
    terms = ordered_unique(list(seed_terms) + base)
    frontier = terms[:]
    for _ in range(max_depth):
        new_terms = []
        left_pool = ordered_unique(terms[:12] + frontier[:12])
        right_pool = ordered_unique(terms[:12] + frontier[:12])
        for a in left_pool:
            for b in right_pool:
                t = ("op", a, b)
                if tree_size(t) <= max_size:
                    new_terms.append(t)
        old_len = len(terms)
        terms = ordered_unique(terms + new_terms, max_terms)
        frontier = terms[old_len:]
        if len(terms) >= max_terms or not frontier:
            break
    indexed = list(enumerate(terms))
    indexed.sort(key=lambda p: (tree_size(p[1]), p[0]))
    return [t for _, t in indexed[:max_terms]]


def _bounded_arg_pool(candidates, arity, max_arg_combos=20000):
    if arity <= 0:
        return []
    pool = candidates[:]
    while len(pool) > 1 and (len(pool) ** arity) > max_arg_combos:
        pool = pool[:-1]
    return pool


def _build_h_edge_graph(h_vars, h_lhs, h_rhs, candidates, max_arg_combos=20000):
    """Instantiate h over a bounded candidate universe and return adjacency."""
    arg_pool = _bounded_arg_pool(candidates, len(h_vars), max_arg_combos=max_arg_combos)
    adj = {}
    if not arg_pool:
        return adj
    for combo in product(arg_pool, repeat=len(h_vars)):
        subst = dict(zip(h_vars, combo))
        lhs = apply_subst_tree(h_lhs, subst)
        rhs = apply_subst_tree(h_rhs, subst)
        args = " ".join(tree_to_str(subst[v]) for v in h_vars)
        pf = f"h {args}"
        adj.setdefault(lhs, []).append((rhs, pf))
        adj.setdefault(rhs, []).append((lhs, f"({pf}).symm"))
    return adj


def _find_path(adj, start, target, max_depth=4):
    if start == target:
        return []
    q = [(start, [])]
    seen = {start}
    head = 0
    while head < len(q):
        node, path = q[head]
        head += 1
        if len(path) >= max_depth:
            continue
        for nxt, pf in adj.get(node, []):
            if nxt in seen:
                continue
            new_path = path + [(node, nxt, pf)]
            if nxt == target:
                return new_path
            seen.add(nxt)
            q.append((nxt, new_path))
    return None


def calc_from_path(path):
    if not path:
        return "rfl"
    lines = ["calc"]
    first_lhs, first_rhs, first_pf = path[0]
    lines.append(f"  {tree_to_str(first_lhs)} = {tree_to_str(first_rhs)} := {first_pf}")
    for _, rhs, pf in path[1:]:
        lines.append(f"  _ = {tree_to_str(rhs)} := {pf}")
    return "\n".join(lines)


def try_bounded_equality_graph(problem, eq1_text, eq2_text, max_path_depth=4):
    """Search for a symbolic equality path from Eq2.lhs to Eq2.rhs."""
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

    seeds = subterms(g_lhs) + subterms(g_rhs)
    candidates = generate_candidate_terms(g_vars, seeds, max_depth=2, max_terms=34, max_size=9)
    adj = _build_h_edge_graph(h_vars, h_lhs, h_rhs, candidates, max_arg_combos=22000)
    path = _find_path(adj, g_lhs, g_rhs, max_depth=max_path_depth)
    if not path:
        return False
    intro = "intro " + " ".join(g_vars) if g_vars else ""
    body = intro + "\n" + calc_from_path(path)
    code = make_true_code(body)
    return call_judge("true", code).get("status") == "accepted"


def try_singleton_equality_graph(problem, eq1_text, eq2_text, max_path_depth=5):
    """Try to prove `∀ p q, p = q` by equality-path search over p/q terms."""
    h_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq1_text):
        if v not in seen:
            seen.add(v)
            h_vars.append(v)
    eq2_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq2_text):
        if v not in seen:
            seen.add(v)
            eq2_vars.append(v)
    try:
        h_lhs_str, h_rhs_str = eq1_text.split("=", 1)
        goal_lhs, goal_rhs = eq2_text.split("=", 1)
        h_lhs = parse_to_tree(h_lhs_str)
        h_rhs = parse_to_tree(h_rhs_str)
    except Exception:
        return False

    p, q = ("var", "p"), ("var", "q")
    seeds = [p, q, ("op", p, q), ("op", q, p), ("op", p, p), ("op", q, q)]
    candidates = generate_candidate_terms(["p", "q"], seeds, max_depth=2, max_terms=32, max_size=9)
    adj = _build_h_edge_graph(h_vars, h_lhs, h_rhs, candidates, max_arg_combos=26000)
    path = _find_path(adj, p, q, max_depth=max_path_depth)
    if not path:
        return False

    intro = "intro " + " ".join(eq2_vars) if eq2_vars else ""
    calc = calc_from_path(path)
    body = (
        f"{intro}\n"
        "have key : ∀ (p q : G), p = q := by\n"
        "  intro p q\n"
        + "\n".join("  " + line for line in calc.splitlines())
        + f"\nexact key ({goal_lhs.strip()}) ({goal_rhs.strip()})"
    )
    code = make_true_code(body)
    return call_judge("true", code).get("status") == "accepted"


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
    # Strip a stray leading `by` wrapper. The newline-specific case matters:
    # otherwise `by\n  intro ...` can leave indentation that becomes malformed
    # once make_true_code wraps the body.
    p = re.sub(r"^\s*by\s*\n", "", p)
    p = re.sub(r"^\s*by\s+", "", p)
    return p.strip()


def _goal_vars(eq_text):
    out = []
    for v in re.findall(r"\b([a-z])\b", eq_text):
        if v not in out:
            out.append(v)
    return out


def intro_arity_ok(proof, eq2_text):
    """Cheaply filter LLM proofs that introduce too many/few goal vars."""
    vars_needed = _goal_vars(eq2_text)
    lines = [line.strip() for line in proof.splitlines() if line.strip()]
    if not lines:
        return False
    if not lines[0].startswith("intro "):
        return True
    got = lines[0].split()[1:]
    return len(got) == len(vars_needed)



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


def main():
    start_time = time.monotonic()
    startup = read_message()
    problem = startup["problem"]
    eq1 = problem["equation1"].replace("*", "\u25c7")
    eq2 = problem["equation2"].replace("*", "\u25c7")
    problem["equation1"], problem["equation2"] = eq1, eq2

    trace(f"[problem] {problem.get('id', '?')} eq1={problem.get('eq1_id')} eq2={problem.get('eq2_id')}")
    trace(f"[eq1] {eq1}")
    trace(f"[eq2] {eq2}")

    # Stage 1: exhaustive counterexample search on Fin 2–3.
    trace("[stage] exhaustive Fin 2-3 counterexample search")
    n, table = search_counterexample(eq1, eq2, max_n=3)
    if n is not None:
        trace(f"[solved-candidate] exhaustive false witness Fin {n}")
        if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
            trace("[accepted] exhaustive false witness")
            return

    # Stage 1.25: named finite witness tables.
    trace("[stage] named witness tables")
    name, n, table = search_named_witnesses(eq1, eq2)
    if n is not None:
        trace(f"[solved-candidate] named false witness {name} Fin {n}")
        if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
            trace(f"[accepted] named false witness {name}")
            return

    # Stage 1.35: perturbed structured witnesses.
    # This is the first false-side search-space narrowing stage:
    # start from useful structured magmas and perturb one table cell.
    if "search_perturbed_witnesses" in globals():
        trace("[stage] perturbed witness tables")
        n, table = search_perturbed_witnesses(eq1, eq2, sizes=(2, 3, 4))
        if n is not None:
            trace(f"[solved-candidate] perturbed false witness Fin {n}")
            if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
                trace("[accepted] perturbed false witness")
                return
    else:
        trace("[skip] perturbed witness tables: function missing")

    # Stage 1.5: structured counterexample families on Fin 4–7.
    trace("[stage] structured Fin 4-7 counterexample search")
    n, table = search_counterexample_extended(eq1, eq2, sizes=(4, 5, 6, 7))
    if n is not None:
        trace(f"[solved-candidate] structured false witness Fin {n}")
        if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
            trace("[accepted] structured false witness")
            return

    # Stage 2: direct h-application via unification.
    trace("[stage] direct h application")
    if try_direct_h_application(problem, eq1, eq2):
        trace("[accepted] direct h application")
        return

    # Stage 2.2: two-step h chain.
    trace("[stage] two-step h chain")
    if try_two_step_h_chain(problem, eq1, eq2, max_judge_calls=6):
        trace("[accepted] two-step h chain")
        return

    # Compute singleton hint earlier so it can route deterministic search.
    trace("[stage] singleton small-model hint")
    singleton = forces_singleton(eq1)
    trace(f"[singleton_hint] {singleton}")

    # Stage 2.25: bounded equality graph from goal lhs to goal rhs.
    if "try_bounded_equality_graph" in globals():
        trace("[stage] bounded equality graph")
        if try_bounded_equality_graph(problem, eq1, eq2, max_path_depth=4):
            trace("[accepted] bounded equality graph")
            return
    else:
        trace("[skip] bounded equality graph: function missing")

    # Stage 2.3: singleton equality graph, prioritized before generic rw/simp.
    if singleton and "try_singleton_equality_graph" in globals():
        trace("[stage] singleton equality graph")
        if try_singleton_equality_graph(problem, eq1, eq2, max_path_depth=5):
            trace("[accepted] singleton equality graph")
            return
    elif singleton:
        trace("[skip] singleton equality graph: function missing")

    # Stage 2.4: generic one-line Lean tactics.
    # Skip these for bare-side equations because rw [h] often fails with
    # metavariable-pattern errors and just wastes judge calls.
    if not has_bare_side(eq1):
        trace("[stage] generic tactics")
        if try_generic_tactics(problem, eq1, eq2, max_judge_calls=12):
            trace("[accepted] generic tactics")
            return
    else:
        trace("[skip] generic tactics: Eq1 has bare side")

    # Stage 2.5: trivial singleton template.
    trace("[stage] trivial singleton template")
    proof = try_trivial_singleton(eq1, eq2)
    if proof is not None:
        if call_judge("true", make_true_code(proof)).get("status") == "accepted":
            trace("[accepted] trivial singleton template")
            return

    # Stage 2.6: structural singleton templates.
    trace("[stage] structural singleton pattern")
    if try_structural_singleton_pattern(problem, eq1, eq2):
        trace("[accepted] structural singleton pattern")
        return

    # Stage 3: LLM fallback.
    trace("[stage] LLM fallback")
    analysis_lines = []
    if singleton:
        lhs_str, rhs_str = eq1.split("=", 1)
        lhs_var = lhs_str.strip()
        rhs_vars_set = set(re.findall(r"\b([a-z])\b", rhs_str))
        x_in_rhs = len(lhs_var) == 1 and lhs_var in rhs_vars_set

        analysis_lines.append(
            "STRUCTURAL FINDING: h appears singleton-like by small-model search "
            "(no non-singleton model found on searched Fin 2/3 cases). The intended "
            "proof is TRUE via `key : ∀ (a b : G), a = b`, then applying key to the goal."
        )
        analysis_lines.append(
            "IMPORTANT: Treat this as a TRUE proof task. Do NOT output verdict false. "
            "Do NOT output a counterexample_table. Output only verdict true with a Lean proof body."
        )
        analysis_lines.append(
            "Do NOT prove key using `have h1 := h a a ...; have h2 := h b b ...; "
            "exact h1.trans h2.symm`. That is invalid unless the middle terms are definitionally identical."
        )

        if not x_in_rhs:
            analysis_lines.append(
                "Easy singleton case: h's LHS variable does NOT appear in RHS. A one-line "
                "proof may work by making a and b equal to the same RHS using identical fillers."
            )
        else:
            analysis_lines.append(
                "Hard singleton case: h's LHS variable also appears in RHS. You need a multi-step "
                "constancy/equality chain. Use explicit `have` lemmas whose middle terms match exactly."
            )
            analysis_lines.append(
                "Proof shape:\n"
                "intro <goal vars>\n"
                "have key : ∀ (p q : G), p = q := by\n"
                "  intro p q\n"
                "  ... several h-instantiations and rewrites ...\n"
                "exact key <goal_lhs> <goal_rhs>"
            )
    else:
        analysis_lines.append(
            "No finite counterexample found by deterministic search and no singleton hint. "
            "Try a true calc chain from Eq2.lhs to Eq2.rhs using exact h-instantiations, "
            "or propose a finite counterexample table only if it genuinely satisfies Eq1 and falsifies Eq2."
        )

    seen = set()
    MAX_LLM_ATTEMPTS = 2 if singleton else 4
    consecutive_garbage = 0

    for attempt in range(MAX_LLM_ATTEMPTS):
        elapsed = time.monotonic() - start_time
        remaining = BUDGET_SECONDS - elapsed
        trace(f"[llm] attempt={attempt} remaining={remaining:.1f}s singleton={singleton}")

        if remaining < MIN_SECONDS_FOR_LLM:
            trace("[stop] not enough time left for another LLM call")
            break

        ctx = {
            "analysis": "\n".join(analysis_lines),
            "attempt": str(attempt),
        }
        result = call_llm(ctx)
        if "error" in result:
            trace(f"[stop] LLM error: {result.get('error')}")
            return

        answer = extract_json(result.get("response", ""))
        if not answer:
            consecutive_garbage += 1
            trace("[llm] unparseable response")
            if consecutive_garbage >= 2:
                trace("[stop] repeated unparseable LLM responses")
                return
            continue

        consecutive_garbage = 0
        verdict = answer.get("verdict")

        if verdict == "true":
            proof = clean_proof(answer.get("proof", ""))
            if not proof:
                trace("[llm] empty true proof")
                continue
            if proof in seen:
                trace("[llm] duplicate proof skipped")
                continue
            if not intro_arity_ok(proof, eq2):
                trace("[llm] intro arity mismatch skipped")
                continue

            seen.add(proof)
            code = make_true_code(proof)

        elif verdict == "false":
            if singleton:
                trace("[llm] skipped false answer because singleton hint is true")
                continue

            tbl = answer.get("counterexample_table")
            if not tbl or not isinstance(tbl, list):
                trace("[llm] malformed false table")
                continue

            code = make_false_code(len(tbl), tbl)

        else:
            trace(f"[llm] unknown verdict: {verdict}")
            continue

        res = call_judge(verdict, code)
        trace(f"[judge] LLM candidate status={res.get('status')}")
        if res.get("status") == "accepted":
            trace("[accepted] LLM candidate")
            return

if __name__ == "__main__":
    main()
