"""
SAIR Equational Theories Stage 2 — minimal solver.
(2026-06-10: added affine-model stage + domain-propagation finder portfolio.)

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

PROMPT = """You are an expert in universal algebra (magmas: a set with one binary
operation \u25c7, NO associativity, NO identity) and equational logic. You help prove
that one magma law implies another over ALL magmas.

# Problem
Hypothesis Eq1 ({problem.equation1_id}):  for all vars, {problem.equation1}
Goal       Eq2 ({problem.equation2_id}):  for all vars, {problem.equation2}

# Solver analysis
{solver.analysis}

# Previous attempts (round {history.round})
{history.attempts}

# Response rules
Output ONLY one JSON object. No markdown fences, no prose outside the JSON.
Use the operator character \u25c7 (U+25C7), NEVER `*`.

# Solver mode = {solver.mode}

## If mode is `waypoints` (PREFERRED -- you do NOT write Lean):
A separate verified engine proves each short step; your job is only to sketch the
equational PATH. Treat Eq1 as a two-way rewrite: any instance of one side may be
replaced by the other, anywhere inside a term. Give an ORDERED list of intermediate
terms (`waypoints`) that a proof of  goal_LHS = goal_RHS  passes through, starting
near goal_LHS and ending near goal_RHS, where each consecutive pair differs by only
ONE or a FEW applications of Eq1 to a subterm. Constraints:
- Use ONLY the goal's variables and \u25c7. Fully parenthesize, e.g. (x \u25c7 (y \u25c7 x)).
- 6 to 18 waypoints, each a small term (size 3-13). Keep each step small.
Return EXACTLY: {"mode":"waypoints","waypoints":["term1","term2","..."]}

## If mode is `lemma_strategy` (you do NOT write Lean):
Return ONLY: {"mode":"lemma_strategy","skeleton":"singleton_path","seed_terms":[...]}
- Use only variables p and q. 8-20 nontrivial seed terms (size 3-9), including terms
  shaped like the hypothesis sides with variables renamed to p/q.

## If mode is `proof` (you DO write Lean tactics):
For TRUE:  {"verdict":"true","proof":"<tactic body -- no import, no theorem>"}
For FALSE: {"verdict":"false","counterexample_table":[[0,1],[1,0]]}
Allowed tactics: intro, exact, have, calc, rw, conv, apply, congrArg, .symm, .trans.
The hypothesis is `h`; the proof starts after `intro G _ h` (already added). Your body
only introduces the goal's variables and proves the equation; every calc/have step must
be a valid instance of `h` (optionally inside congrArg), with middle terms matching exactly.
"""


import json
import re
import sys
import time
from itertools import product

# ── Timing budget ────────────────────────────────────────────────
# Total wall-clock seconds the solver is expected to run. Used to
# avoid starting an LLM call when too little time is left.
DEFAULT_BUDGET_SECONDS = 3600
MIN_SECONDS_FOR_LLM = 350
# Wall-clock budget for the domain-propagation model-finder portfolio
# (Stage 2.9 first pass). Generous relative to the old 2s/size finders:
# the solo budget is 3600s and the LLM is essentially unused, so spending
# tens of seconds on the false side is nearly free.
MF2_PORTFOLIO_BUDGET = 240.0  # was 60.0; per-problem cap is 3600s and the
# false-side finder was the scarce resource. Funds the extended large-Fin
# schedule tier below. Only spent on cases the true-proof stages did not close.
SAT_FINDER_BUDGET = 120.0  # complete CDCL false-finder; runs only on
# non-singleton cases the mf2 portfolio missed. Cracks the hard general Fin 6
# residual; bounded so it can't run away on a genuinely-true (unsat) case.
# Non-singleton LLM proof fallback is disabled: it returns unusable
# lemma_strategy output, has solved ~0 cases, and costs 20-340s each (one hard2
# case burned 337s on a single call). The deterministic stages (completion +
# model finder) cover this residual. Flip to True to re-enable.
ENABLE_NS_LLM_FALLBACK = False


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
    vars_needed = goal_vars(eq2_text)
    lines = [line.strip() for line in proof.splitlines() if line.strip()]
    if not lines:
        return False
    if not lines[0].startswith("intro "):
        return True

    got = lines[0].split()[1:]

    # h is already in scope from `intro G _ h`; the proof body should not introduce it.
    if "h" in got:
        return False

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


def _edge_key(src, dst, pf):
    return (src, dst, pf)


def _add_edge(adj, seen_edges, src, dst, pf):
    key = _edge_key(src, dst, pf)
    if key in seen_edges:
        return False
    seen_edges.add(key)
    adj.setdefault(src, []).append((dst, pf))
    return True


def _collect_seen_edges(adj):
    seen = set()
    for src, outs in adj.items():
        for dst, pf in outs:
            seen.add(_edge_key(src, dst, pf))
    return seen


def add_congruence_edges(
    adj,
    context_terms,
    max_term_size=13,
    max_new_edges=60000,
):
    """Add one-step congruence/context edges to an equality graph.

    If the graph has an edge a = b justified by pf, add:
      a ◇ t = b ◇ t by congrArg (fun r => r ◇ t) pf
      t ◇ a = t ◇ b by congrArg (fun r => t ◇ r) pf

    This lets the graph perform rewrites inside one product context.
    """
    seen_edges = _collect_seen_edges(adj)
    base_edges = []
    for src, outs in list(adj.items()):
        for dst, pf in outs:
            base_edges.append((src, dst, pf))

    added = 0
    contexts = list(context_terms)

    for src, dst, pf in base_edges:
        for t in contexts:
            left_src = ("op", src, t)
            left_dst = ("op", dst, t)
            if tree_size(left_src) <= max_term_size and tree_size(left_dst) <= max_term_size:
                t_str = tree_to_str(t)
                new_pf = f"congrArg (fun r => r ◇ {t_str}) ({pf})"
                if _add_edge(adj, seen_edges, left_src, left_dst, new_pf):
                    added += 1
                    if added >= max_new_edges:
                        return added

            right_src = ("op", t, src)
            right_dst = ("op", t, dst)
            if tree_size(right_src) <= max_term_size and tree_size(right_dst) <= max_term_size:
                t_str = tree_to_str(t)
                new_pf = f"congrArg (fun r => {t_str} ◇ r) ({pf})"
                if _add_edge(adj, seen_edges, right_src, right_dst, new_pf):
                    added += 1
                    if added >= max_new_edges:
                        return added

    return added

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

def _parse_seed_terms(seed_term_strings):
    """Parse LLM-proposed seed terms, ignoring malformed ones."""
    out = []
    for s in seed_term_strings or []:
        if not isinstance(s, str):
            continue
        s = s.replace("*", "◇").strip()
        if not s:
            continue
        try:
            out.append(parse_to_tree(s))
        except Exception:
            continue
    return out


def try_singleton_equality_graph_with_extra_seeds(
    problem,
    eq1_text,
    eq2_text,
    extra_seed_terms=(),
    max_path_depth=6,
    max_terms=48,
    max_size=11,
    max_arg_combos=70000,
):
    """Try to prove ∀ p q, p = q using deterministic graph search.

    This is like try_singleton_equality_graph, but allows extra seed
    terms from a strategist. The LLM only proposes terms; Python still
    builds the graph and generates Lean mechanically.
    """
    h_vars = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", eq1_text):
        if v not in seen:
            seen.add(v)
            h_vars.append(v)

    eq2_vars = goal_vars(eq2_text)

    try:
        h_lhs_str, h_rhs_str = eq1_text.split("=", 1)
        goal_lhs, goal_rhs = eq2_text.split("=", 1)
        h_lhs = parse_to_tree(h_lhs_str)
        h_rhs = parse_to_tree(h_rhs_str)
    except Exception:
        return False

    p, q = ("var", "p"), ("var", "q")
    base_seeds = [
        p,
        q,
        ("op", p, q),
        ("op", q, p),
        ("op", p, p),
        ("op", q, q),
        ("op", ("op", p, q), p),
        ("op", ("op", q, p), q),
        ("op", p, ("op", p, q)),
        ("op", q, ("op", q, p)),
    ]

    seeds = ordered_unique(base_seeds + list(extra_seed_terms))
    candidates = generate_candidate_terms(
        ["p", "q"],
        seeds,
        max_depth=2,
        max_terms=max_terms,
        max_size=max_size,
    )

    adj = _build_h_edge_graph(
        h_vars,
        h_lhs,
        h_rhs,
        candidates,
        max_arg_combos=max_arg_combos,
    )

    context_terms = ordered_unique(seeds + candidates[:16], max_items=24)
    added = add_congruence_edges(
        adj,
        context_terms=context_terms,
        max_term_size=max_size + 4,
        max_new_edges=60000,
    )
    trace(
        f"[strategy-graph] candidates={len(candidates)} "
        f"direct_nodes={len(adj)} congr_edges_added={added}"
    )

    path = _find_path(adj, p, q, max_depth=max_path_depth + 1)
    if not path:
        trace(
            f"[strategy-graph] no p→q path; seeds={len(seeds)} "
            f"candidates={len(candidates)} nodes={len(adj)}"
        )
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


def try_llm_strategy_singleton_graph(
    problem,
    eq1_text,
    eq2_text,
    start_time,
    budget_seconds,
):
    """Ask the LLM for seed terms, then run deterministic graph search.

    The LLM is not allowed to write Lean here. It only proposes a
    search-space expansion for the singleton equality graph.
    """
    elapsed = time.monotonic() - start_time
    remaining = budget_seconds - elapsed
    if remaining < MIN_SECONDS_FOR_LLM:
        trace("[strategy] skip: not enough time for LLM strategist")
        return False

    analysis = (
        "We need a hard singleton proof. Do not write Lean. "
        "Suggest seed terms for a deterministic equality-graph search proving "
        "`∀ p q : G, p = q`. Use only variables p and q. "
        "The hypothesis is Eq1 and has a bare variable on the left. "
        "Good seed terms are small products that may appear as intermediate "
        "terms in h-instantiations."
    )

    result = call_llm(
        {
            "mode": "lemma_strategy",
            "analysis": analysis,
            "attempt": "strategy0",
        }
    )

    if "error" in result:
        trace(f"[strategy] LLM error: {result.get('error')}")
        return False

    answer = extract_json(result.get("response", ""))
    if not answer:
        trace("[strategy] unparseable strategy response")
        return False

    if answer.get("mode") != "lemma_strategy":
        trace("[strategy] wrong mode in response")
        return False

    seed_terms = _parse_seed_terms(answer.get("seed_terms", []))
    p, q = ("var", "p"), ("var", "q")
    deterministic_extra = [
        ("op", ("op", p, q), ("op", q, p)),
        ("op", ("op", q, p), ("op", p, q)),
        ("op", ("op", p, p), ("op", q, p)),
        ("op", ("op", q, q), ("op", p, q)),
        ("op", ("op", p, q), ("op", p, q)),
        ("op", ("op", q, p), ("op", q, p)),
        ("op", p, ("op", q, p)),
        ("op", q, ("op", p, q)),
    ]
    seed_terms = ordered_unique(seed_terms + deterministic_extra)
    trace(f"[strategy] parsed {len(seed_terms)} seed terms")

    if not seed_terms:
        return False

    return try_singleton_equality_graph_with_extra_seeds(
        problem,
        eq1_text,
        eq2_text,
        extra_seed_terms=seed_terms,
        max_path_depth=7,
        max_terms=56,
        max_size=11,
        max_arg_combos=90000,
    )


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
    """Conservative small-model singleton hint.

    If ANY magma on Fin 2 or Fin 3 satisfies h, then h does NOT force
    singleton behavior, because the carrier has at least two elements.

    This is only a routing hint, not a Lean proof.
    """
    v1, l1, r1 = parse_equation(eq1_text)

    for n in (2, 3):
        if n == 3 and len(v1) > 4:
            break

        for enc in range(n ** (n * n)):
            table = [
                [(enc // (n ** (i * n + j))) % n for j in range(n)]
                for i in range(n)
            ]
            op = lambda a, b, t=table: t[a][b]

            if equation_holds(v1, l1, r1, n, op):
                return False

    return True

# ── Lean code generation ─────────────────────────────────────────


def make_false_code(n, table):
    # set_option maxRecDepth: decideFin! recurses over all n^vars ground
    # instances; the Lean default (512) is exceeded by Fin 6+ tables, which
    # silently rejected every larger counterexample ("maximum recursion depth
    # has been reached"). Bumping it unblocks the entire Fin 6-9 false side.
    return (
        "import JudgeProblem\n"
        "import JudgeDecide.DecideBang\n"
        "import JudgeFinOp.MemoFinOp\n"
        "open MemoFinOp\n\n"
        "set_option maxRecDepth 100000\n\n"
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


# ── Inlined ordered-completion engine (kc_ namespace) ──
# Source: docs/completion_engine_reference.py. Deterministic singleton
# prover; see docs/completion_singleton_approach.md. Modest recursion
# limit + kc_CEIL term-size bound guard against runaway recursion.
sys.setrecursionlimit(8000)
# ===== inlined ordered-completion engine (kc_ namespace) =====
kc_OP='o'; kc_CEIL=20
def kc_is_v(t): return t[0]=='V'

def kc_parse(text):
    s=text.strip()
    def so(s):
        while len(s)>=2 and s[0]=='(' and s[-1]==')':
            d=0; ok=True
            for i,c in enumerate(s):
                d+=c=='('; d-=c==')'
                if d==0 and i<len(s)-1: ok=False;break
            if ok: s=s[1:-1].strip()
            else: break
        return s
    s=so(s); d=0; last=-1
    for i,c in enumerate(s):
        d+=c=='('; d-=c==')'
        if d==0 and c in '◇*': last=i
    if last<0:
        if len(s)==1 and s.isalpha(): return ('V',s)
        raise ValueError(s)
    return ('F',kc_OP,(kc_parse(s[:last]),kc_parse(s[last+1:])))

def kc_sizecap(t,cap):
    # iterative kc_size, returns kc_size or cap+1 if exceeds
    st=[t]; n=0
    while st:
        x=st.pop(); n+=1
        if n>cap: return cap+1
        if not kc_is_v(x): st.extend(x[2])
    return n
def kc_size(t): return kc_sizecap(t,10**9)

def kc_vars_of(t):
    st=[t]; acc=set()
    while st:
        x=st.pop()
        if kc_is_v(x): acc.add(x[1])
        else: st.extend(x[2])
    return acc

def kc_rename(t,suf):
    if kc_is_v(t): return ('V',t[1]+suf)
    return ('F',t[1],tuple(kc_rename(a,suf) for a in t[2]))

def kc_deref(t,s):
    while kc_is_v(t) and t[1] in s: t=s[t[1]]
    return t
def kc_occurs(v,t,s):
    st=[t]
    while st:
        x=kc_deref(st.pop(),s)
        if kc_is_v(x):
            if x[1]==v: return True
        else: st.extend(x[2])
    return False
def kc_unify(x,y,s):
    if s is None: return None
    x=kc_deref(x,s); y=kc_deref(y,s)
    if kc_is_v(x):
        if kc_is_v(y) and x[1]==y[1]: return s
        if kc_occurs(x[1],y,s): return None
        s2=dict(s); s2[x[1]]=y; return s2
    if kc_is_v(y):
        if kc_occurs(y[1],x,s): return None
        s2=dict(s); s2[y[1]]=x; return s2
    if x[1]!=y[1] or len(x[2])!=len(y[2]): return None
    for a,b in zip(x[2],y[2]):
        s=kc_unify(a,b,s)
        if s is None: return None
    return s
def kc_appsub(t,s):
    t=kc_deref(t,s)
    if kc_is_v(t): return t
    return ('F',t[1],tuple(kc_appsub(a,s) for a in t[2]))
def kc_match(p,t,s):
    if s is None: return None
    if kc_is_v(p):
        if p[1] in s: return s if s[p[1]]==t else None
        s2=dict(s); s2[p[1]]=t; return s2
    if kc_is_v(t) or p[1]!=t[1] or len(p[2])!=len(t[2]): return None
    for a,b in zip(p[2],t[2]):
        s=kc_match(a,b,s)
        if s is None: return None
    return s

kc_PREC={kc_OP:10}
def kc_prec(f): return kc_PREC.get(f,0)
def kc_lpo_gt(s,t):
    if s==t: return False
    if kc_is_v(t): return (not kc_is_v(s)) and (t[1] in kc_vars_of(s))
    if kc_is_v(s): return False
    f,ss=s[1],s[2]; g,kc_ts=t[1],t[2]
    for si in ss:
        if si==t or kc_lpo_gt(si,t): return True
    if all(kc_lpo_gt(s,tj) for tj in kc_ts):
        if kc_prec(f)>kc_prec(g): return True
        if f==g:
            for a,b in zip(ss,kc_ts):
                if a==b: continue
                return kc_lpo_gt(a,b)
            return False
    return False

def kc_nonvar_positions(t,path=()):
    if kc_is_v(t): return
    yield path,t
    for i,a in enumerate(t[2]):
        yield from kc_nonvar_positions(a,path+(i,))
def kc_replace(t,path,new):
    if not path: return new
    i=path[0]
    return ('F',t[1],tuple(kc_replace(a,path[1:],new) if k==i else a for k,a in enumerate(t[2])))

def kc_rewrite_once(t,eqs):
    for (s0,t0) in eqs:
        s_,t_=kc_rename(s0,'$'),kc_rename(t0,'$')
        for (l,r) in ((s_,t_),(t_,s_)):
            for path,sub in kc_nonvar_positions(t):
                sg=kc_match(l,sub,{})
                if sg is None: continue
                lin=kc_appsub(l,sg); rin=kc_appsub(r,sg)
                if kc_lpo_gt(lin,rin):
                    cand=kc_replace(t,path,rin)
                    if kc_sizecap(cand,kc_CEIL)<=kc_CEIL:
                        return cand
    return None
def kc_normalize(t,eqs,steps=80):
    for _ in range(steps):
        nt=kc_rewrite_once(t,eqs)
        if nt is None or nt==t: return t
        t=nt
    return t
def kc_norm_eq(eq,eqs): return (kc_normalize(eq[0],eqs),kc_normalize(eq[1],eqs))

def kc_canon_side(t,m,ctr):
    if kc_is_v(t):
        if t[1] not in m: m[t[1]]='V%d'%ctr[0]; ctr[0]+=1
        return m[t[1]]
    return t[1]+'('+','.join(kc_canon_side(a,m,ctr) for a in t[2])+')'
def kc_canon(eq):
    def one(a,b):
        m={};ctr=[0]; return kc_canon_side(a,m,ctr)+'='+kc_canon_side(b,m,ctr)
    return min(one(eq[0],eq[1]),one(eq[1],eq[0]))

def kc_crit_pairs(e1,e2,cap):
    out=[]
    e2r=(kc_rename(e2[0],'#'),kc_rename(e2[1],'#'))
    for (l1,r1) in ((e1[0],e1[1]),(e1[1],e1[0])):
        for (l2,r2) in ((e2r[0],e2r[1]),(e2r[1],e2r[0])):
            for path,sub in kc_nonvar_positions(l1):
                sg=kc_unify(sub,l2,{})
                if sg is None: continue
                R1=kc_appsub(r1,sg)
                if kc_sizecap(R1,cap)>cap: continue
                L1=kc_appsub(l1,sg)
                if kc_lpo_gt(R1,L1): continue
                if kc_lpo_gt(kc_appsub(r2,sg),kc_appsub(l2,sg)): continue
                newl=kc_appsub(kc_replace(l1,path,r2),sg)
                if kc_sizecap(newl,cap)>cap: continue
                out.append((R1,newl))
    return out

def kc_is_collapse(eq):
    a,b=eq; return kc_is_v(a) and kc_is_v(b) and a[1]!=b[1]

def kc_complete(eq_str, tb=30.0, cap=18, maxp=600, log=True):
    parts=eq_str.split('=')
    E=(kc_parse(parts[0]),kc_parse(parts[1]))
    start=time.time(); processed=[]; queue=[E]; seen=set(); iters=0
    while queue:
        if time.time()-start>tb: return ('timeout',iters,len(processed),None)
        queue.sort(key=lambda e:kc_size(e[0])+kc_size(e[1]))
        e=queue.pop(0)
        e=kc_norm_eq(e,processed)
        if e[0]==e[1]: continue
        k=kc_canon(e)
        if k in seen: continue
        seen.add(k)
        if kc_is_collapse(e): return ('collapse',iters,len(processed),e)
        iters+=1
        if log and iters%50==0:
            print(f"  iter={iters} proc={len(processed)} queue={len(queue)} t={time.time()-start:.1f}s last={kc_canon(e)[:60]}",file=sys.stderr)
        news=[]
        rules=processed+[e]
        for f in rules:
            for cp in kc_crit_pairs(e,f,cap)+kc_crit_pairs(f,e,cap):
                cp=kc_norm_eq(cp,rules)
                if cp[0]==cp[1]: continue
                if kc_sizecap(cp[0],cap)>cap or kc_sizecap(cp[1],cap)>cap: continue
                kk=kc_canon(cp)
                if kk in seen: continue
                if kc_is_collapse(cp): return ('collapse',iters,len(processed),cp)
                news.append(cp)
        processed.append(e)
        queue.extend(news)
        if len(processed)>maxp: return ('maxproc',iters,len(processed),None)
    return ('saturated',iters,len(processed),None)





def kc_ts(t):  # term -> Lean string (over-parenthesised)
    if kc_is_v(t): return t[1]
    return "("+kc_ts(t[2][0])+" ◇ "+kc_ts(t[2][1])+")"

# ---------- proof terms ----------
# ('H',(a,b,c,d))  ('SYM',P)  ('TRANS',P,Q)  ('CL',t,P)  ('CR',t,P)  ('REFL',t)
kc_H_VARS=None; kc_H_LHS=None; kc_H_RHS=None   # set per problem

def kc_psub(t,s):
    if kc_is_v(t): return s.get(t[1],t)
    return ('F',t[1],tuple(kc_psub(a,s) for a in t[2]))
def kc_subst_term(t,s): return kc_appsub(t,s)

def kc_rn_proof(P,suf):
    k=P[0]
    if k=='H': return ('H',tuple(kc_rename(a,suf) for a in P[1]))
    if k=='SYM': return ('SYM',kc_rn_proof(P[1],suf))
    if k=='TRANS': return ('TRANS',kc_rn_proof(P[1],suf),kc_rn_proof(P[2],suf))
    if k in('CL','CR'): return (k,kc_rename(P[1],suf),kc_rn_proof(P[2],suf))
    if k=='REFL': return ('REFL',kc_rename(P[1],suf))
def kc_inst_proof(P,s):
    k=P[0]
    if k=='H': return ('H',tuple(kc_appsub(a,s) for a in P[1]))
    if k=='SYM': return ('SYM',kc_inst_proof(P[1],s))
    if k=='TRANS': return ('TRANS',kc_inst_proof(P[1],s),kc_inst_proof(P[2],s))
    if k in('CL','CR'): return (k,kc_appsub(P[1],s),kc_inst_proof(P[2],s))
    if k=='REFL': return ('REFL',kc_appsub(P[1],s))

def kc_ptype(P):
    """Recompute (lhs,rhs) this proof establishes; raises on malformed compose."""
    k=P[0]
    if k=='H':
        s=dict(zip(kc_H_VARS,P[1]))
        return (kc_psub(kc_H_LHS,s),kc_psub(kc_H_RHS,s))
    if k=='SYM':
        a,b=kc_ptype(P[1]); return (b,a)
    if k=='TRANS':
        a,b=kc_ptype(P[1]); c,d=kc_ptype(P[2])
        assert b==c, "trans mismatch"
        return (a,d)
    if k=='CL':
        a,b=kc_ptype(P[2]); t=P[1]
        return (('F',kc_OP,(a,t)),('F',kc_OP,(b,t)))
    if k=='CR':
        a,b=kc_ptype(P[2]); t=P[1]
        return (('F',kc_OP,(t,a)),('F',kc_OP,(t,b)))
    if k=='REFL':
        return (P[1],P[1])

def kc_render(P):
    k=P[0]
    if k=='H': return "(h "+" ".join(kc_ts(a) for a in P[1])+")"
    if k=='SYM': return "("+kc_render(P[1])+").symm"
    if k=='TRANS': return "(("+kc_render(P[1])+").trans ("+kc_render(P[2])+"))"
    if k=='CL': return "(congrArg (fun s => s ◇ "+kc_ts(P[1])+") "+kc_render(P[2])+")"
    if k=='CR': return "(congrArg (fun s => "+kc_ts(P[1])+" ◇ s) "+kc_render(P[2])+")"
    if k=='REFL': return "(rfl)"


def kc_simplify(P):
    k=P[0]
    if k=='SYM':
        Q=kc_simplify(P[1])
        if Q[0]=='SYM': return Q[1]
        if Q[0]=='REFL': return Q
        return ('SYM',Q)
    if k=='TRANS':
        A=kc_simplify(P[1]); B=kc_simplify(P[2])
        if A[0]=='REFL': return B
        if B[0]=='REFL': return A
        return ('TRANS',A,B)
    if k in('CL','CR'):
        Q=kc_simplify(P[2])
        if Q[0]=='REFL': return ('REFL',('F',kc_OP,(P[1],Q[1])) if k=='CR' else ('F',kc_OP,(Q[1],P[1])))
        return (k,P[1],Q)
    return P

def kc_cong_wrap(t,path,inner):
    if not path: return inner
    i=path[0]; a0,a1=t[2]
    if i==0: return ('CL',a1,kc_cong_wrap(a0,path[1:],inner))
    else:    return ('CR',a0,kc_cong_wrap(a1,path[1:],inner))

kc_CEIL=20
def kc_rewrite_step(t,rules):
    for (s0,t0,P0) in rules:
        s_,t_=kc_rename(s0,'$'),kc_rename(t0,'$'); Pr=kc_rn_proof(P0,'$')
        for (l,r,orient) in ((s_,t_,False),(t_,s_,True)):
            for path,sub in kc_nonvar_positions(t):
                sg=kc_match(l,sub,{})
                if sg is None: continue
                lin=kc_appsub(l,sg); rin=kc_appsub(r,sg)
                if kc_lpo_gt(lin,rin):
                    cand=kc_replace(t,path,rin)
                    if kc_sizecap(cand,kc_CEIL)>kc_CEIL: continue
                    inst = kc_inst_proof(('SYM',Pr) if orient else Pr, sg)  # proves lin=rin
                    step = kc_cong_wrap(t,path,inst)                         # proves t=cand
                    return cand,step
    return None
def kc_normalize_pf(t,rules,steps=80):
    proof=('REFL',t); cur=t
    for _ in range(steps):
        st=kc_rewrite_step(cur,rules)
        if st is None: break
        nt,sp=st
        if nt==cur: break
        proof=('TRANS',proof,sp); cur=nt
    return cur,proof

def kc_norm_eq_pf(a,b,Pab,rules):
    """Pab proves a=b. Normalize both sides; return (a',b',proof a'=b')."""
    a2,PA=kc_normalize_pf(a,rules)   # PA: a=a'
    b2,PB=kc_normalize_pf(b,rules)   # PB: b=b'
    proof=('TRANS',('TRANS',('SYM',PA),Pab),PB)  # a'=a=b=b'
    return a2,b2,proof

def kc_crit_pairs_pf(e1,e2):
    s1,t1,P1=e1; s2,t2,P2=e2
    s2r,t2r=kc_rename(s2,'#'),kc_rename(t2,'#'); P2r=kc_rn_proof(P2,'#')
    out=[]
    for (l1,r1,P1o) in ((s1,t1,P1),(t1,s1,('SYM',P1))):
        for (l2,r2,P2o) in ((s2r,t2r,P2r),(t2r,s2r,('SYM',P2r))):
            for path,sub in kc_nonvar_positions(l1):
                sg=kc_unify(sub,l2,{})
                if sg is None: continue
                R1=kc_appsub(r1,sg)
                if kc_sizecap(R1,kc_CEIL)>kc_CEIL: continue
                L1=kc_appsub(l1,sg)
                if kc_lpo_gt(R1,L1): continue
                if kc_lpo_gt(kc_appsub(r2,sg),kc_appsub(l2,sg)): continue
                newl=kc_appsub(kc_replace(l1,path,r2),sg)
                if kc_sizecap(newl,kc_CEIL)>kc_CEIL: continue
                instP1=kc_inst_proof(P1o,sg)          # σl1 = σr1
                instP2=kc_inst_proof(P2o,sg)          # σl2 = σr2
                congP=kc_cong_wrap(L1,path,instP2)     # σl1 = newl
                proof=('TRANS',('SYM',instP1),congP)# σr1 = newl
                out.append((R1,newl,proof))
    return out

def kc_is_collapse(e): return kc_is_v(e[0]) and kc_is_v(e[1]) and e[0][1]!=e[1][1]

def kc_complete_pf(eq_str, tb=20.0, maxp=200, check=True):
    global kc_H_VARS,kc_H_LHS,kc_H_RHS
    L,Rr=eq_str.split('=',1)
    kc_H_LHS=kc_parse(L); kc_H_RHS=kc_parse(Rr)
    kc_H_VARS=[]
    for v in list(kc_vars_of(kc_H_LHS))+list(kc_vars_of(kc_H_RHS)): pass
    # order vars by first appearance in the string
    import re
    seen=[]
    for v in re.findall(r"\b([a-z])\b",eq_str):
        if v not in seen: seen.append(v)
    kc_H_VARS=seen
    P0=('H',tuple(('V',v) for v in kc_H_VARS))
    E0=(kc_H_LHS,kc_H_RHS,P0)
    if check: assert kc_ptype(P0)==(kc_H_LHS,kc_H_RHS), "base proof bad"
    start=time.time(); processed=[]; queue=[E0]; seen=set()
    def size2(e): return kc_sizecap(e[0],10**9)+kc_sizecap(e[1],10**9)
    while queue:
        if time.time()-start>tb: return ('timeout',None)
        queue.sort(key=size2)
        s,t,P=queue.pop(0)
        s,t,P=kc_norm_eq_pf(s,t,P,processed)
        if s==t: continue
        if check: assert kc_ptype(P)==(s,t), ("norm proof bad",kc_canon((s,t)))
        k=kc_canon((s,t))
        if k in seen: continue
        seen.add(k)
        if kc_is_collapse((s,t)): 
            if check: assert kc_ptype(P)==(s,t)
            return ('collapse',(s,t,P))
        rules=processed+[(s,t,P)]
        news=[]
        for f in rules:
            for cp in kc_crit_pairs_pf((s,t,P),f)+kc_crit_pairs_pf(f,(s,t,P)):
                a,b,Pcp=cp
                if check: assert kc_ptype(Pcp)==(a,b), "cp proof bad"
                a,b,Pcp=kc_norm_eq_pf(a,b,Pcp,rules)
                if a==b: continue
                if kc_sizecap(a,kc_CEIL)>kc_CEIL or kc_sizecap(b,kc_CEIL)>kc_CEIL: continue
                kk=kc_canon((a,b))
                if kk in seen: continue
                if check: assert kc_ptype(Pcp)==(a,b),"cp-norm bad"
                if kc_is_collapse((a,b)): return ('collapse',(a,b,Pcp))
                news.append((a,b,Pcp))
        processed.append((s,t,P))
        queue.extend(news)
        if len(processed)>maxp: return ('maxproc',None)
    return ('saturated',None)

def kc_singleton_lean(eq_str, goal_lhs, goal_rhs, goal_vars, tb=20.0):
    status,res=kc_complete_pf(eq_str,tb=tb)
    if status!='collapse': return None
    s,t,P=res
    # instantiate: collapse var s->p, t->q, all other proof vars -> p
    sub={s[1]:('V','p'), t[1]:('V','q')}
    # find other vars appearing in proof via kc_ptype recompute + scan
    others=set()
    def scan(P):
        if P[0]=='H':
            for a in P[1]: others.update(kc_vars_of(a))
        elif P[0]=='SYM': scan(P[1])
        elif P[0]=='TRANS': scan(P[1]); scan(P[2])
        elif P[0] in('CL','CR'): others.update(kc_vars_of(P[1])); scan(P[2])
        elif P[0]=='REFL': others.update(kc_vars_of(P[1]))
    scan(P)
    for v in others:
        if v not in sub: sub[v]=('V','p')
    Pi=kc_inst_proof(P,sub)
    before=kc_ptype(Pi)
    Pi=kc_simplify(Pi)
    assert kc_ptype(Pi)==before, 'kc_simplify changed type'
    lhs,rhs=kc_ptype(Pi)
    assert kc_is_v(lhs) and kc_is_v(rhs) and lhs[1]=='p' and rhs[1]=='q', (kc_ts(lhs),kc_ts(rhs))
    intro="intro "+" ".join(goal_vars) if goal_vars else ""
    body=(f"{intro}\n"
          "have key : ∀ (p q : G), p = q := by\n"
          "  intro p q\n"
          "  exact "+kc_render(Pi)+"\n"
          f"exact key ({goal_lhs}) ({goal_rhs})")
    return body


def try_completion_singleton(problem, eq1_text, eq2_text, time_budget=25.0):
    """Deterministic ordered-completion singleton prover (Phase 1).

    Runs proof-carrying Knuth-Bendix completion on Eq1. If it derives an
    equation between two distinct variables, Eq1 forces a singleton and we
    emit a mechanically-generated, Python-self-checked Lean proof of
    `key : forall p q, p = q`, then apply key to the goal. The LLM never
    authors this proof. See docs/completion_singleton_approach.md.
    """
    gl, gr = eq2_text.split("=", 1)
    try:
        body = kc_singleton_lean(
            eq1_text, gl.strip(), gr.strip(), goal_vars(eq2_text), tb=time_budget
        )
    except Exception as e:
        trace(f"[completion] error: {e!r}")
        return False
    if not body:
        return False
    return call_judge("true", make_true_code(body)).get("status") == "accepted"


def kc_nonsingleton_lean(eq_str, goal_lhs, goal_rhs, goal_vars, tb=20.0, maxp=600):
    """Phase 2 (Engine B2): prove goal_lhs = goal_rhs as a consequence of Eq1
    WITHOUT singleton collapse. Runs proof-carrying ordered completion on Eq1
    and normalizes both goal sides w.r.t. the accumulated system; on a common
    normal form, composes and kc_ptype-CHECKS the proof. Free variables
    introduced during completion are instantiated to an in-scope goal variable
    before rendering (mirrors the singleton path's p/q mapping). Returns a Lean
    proof body, or None."""
    global kc_H_VARS, kc_H_LHS, kc_H_RHS
    L, Rr = eq_str.split('=', 1)
    kc_H_LHS = kc_parse(L); kc_H_RHS = kc_parse(Rr)
    seen_v = []
    for v in re.findall(r"\b([a-z])\b", eq_str):
        if v not in seen_v: seen_v.append(v)
    kc_H_VARS = seen_v
    P0 = ('H', tuple(('V', v) for v in kc_H_VARS))
    E0 = (kc_H_LHS, kc_H_RHS, P0)
    gl = kc_parse(goal_lhs); gr = kc_parse(goal_rhs)

    def try_goal(rules):
        nl, Pl = kc_normalize_pf(gl, rules)
        nr, Pr = kc_normalize_pf(gr, rules)
        if nl == nr:
            P = kc_simplify(('TRANS', Pl, ('SYM', Pr)))
            if kc_ptype(P) == (gl, gr):
                return P
        return None

    start = time.time(); processed = []; queue = [E0]; seen = set()
    P = try_goal(processed)
    while P is None and queue:
        if time.time() - start > tb:
            break
        queue.sort(key=lambda e: kc_sizecap(e[0], 10**9) + kc_sizecap(e[1], 10**9))
        s, t, Pp = queue.pop(0)
        s, t, Pp = kc_norm_eq_pf(s, t, Pp, processed)
        if s == t:
            continue
        k = kc_canon((s, t))
        if k in seen:
            continue
        seen.add(k)
        rules = processed + [(s, t, Pp)]
        news = []
        for f in rules:
            for cp in kc_crit_pairs_pf((s, t, Pp), f) + kc_crit_pairs_pf(f, (s, t, Pp)):
                a, b, Pcp = cp
                a, b, Pcp = kc_norm_eq_pf(a, b, Pcp, rules)
                if a == b:
                    continue
                if kc_sizecap(a, kc_CEIL) > kc_CEIL or kc_sizecap(b, kc_CEIL) > kc_CEIL:
                    continue
                kk = kc_canon((a, b))
                if kk in seen:
                    continue
                news.append((a, b, Pcp))
        processed.append((s, t, Pp))
        P = try_goal(processed)
        if P is not None:
            break
        queue.extend(news)
        if len(processed) > maxp:
            break
    if P is None:
        return None
    if not goal_vars:
        return None  # need an in-scope element to bind free completion variables
    gset = set(goal_vars)
    pv = set()
    def scan(Q):
        if Q[0] == 'H':
            for a in Q[1]: pv.update(kc_vars_of(a))
        elif Q[0] == 'SYM': scan(Q[1])
        elif Q[0] == 'TRANS': scan(Q[1]); scan(Q[2])
        elif Q[0] in ('CL', 'CR'): pv.update(kc_vars_of(Q[1])); scan(Q[2])
        elif Q[0] == 'REFL': pv.update(kc_vars_of(Q[1]))
    scan(P)
    sub = {v: ('V', goal_vars[0]) for v in pv if v not in gset}
    Pi = kc_inst_proof(P, sub) if sub else P
    Pi = kc_simplify(Pi)
    if kc_ptype(Pi) != (gl, gr):
        return None
    intro = "intro " + " ".join(goal_vars) if goal_vars else ""
    return f"{intro}\nexact " + kc_render(Pi)


def try_completion_nonsingleton(problem, eq1_text, eq2_text, time_budget=20.0):
    """Phase 2 adapter: deterministic non-singleton completion proof of
    goal_lhs = goal_rhs as a consequence of Eq1. Self-checked by kc_ptype
    before submission; the LLM never authors it."""
    gl, gr = eq2_text.split("=", 1)
    try:
        body = kc_nonsingleton_lean(
            eq1_text, gl.strip(), gr.strip(), goal_vars(eq2_text), tb=time_budget
        )
    except Exception as e:
        trace(f"[completion-ns] error: {e!r}")
        return False
    if not body:
        return False
    return call_judge("true", make_true_code(body)).get("status") == "accepted"


# ── Affine model stage (af_ namespace) ──────────────────────────
# op(x,y) = (a*x + b*y + c) mod n. Eq1 holds identically iff per-variable
# coefficients and the constant term match mod n — checked SYMBOLICALLY in
# O(eq size), so any modulus n is reachable (far past the search finders'
# Fin 7-8 ceiling). The constant term is linear in c (multiplier m follows
# m(l◇r) = a*m(l) + b*m(r) + 1), so c is solved, not enumerated.
# Inspired by the ETP paper's "linear models" disproof family.


def af_eval(t, a, b, n):
    """Return (coeff dict var->int, c-multiplier) of term value mod n.
    value = sum coeff_v * v + m * c  (mod n)."""
    if t[0] == 'V':
        return {t[1]: 1}, 0
    cl, ml = af_eval(t[2][0], a, b, n)
    cr, mr = af_eval(t[2][1], a, b, n)
    co = {}
    for v in set(cl) | set(cr):
        co[v] = (a * cl.get(v, 0) + b * cr.get(v, 0)) % n
    return co, (a * ml + b * mr + 1) % n


def af_find(eq1_text, eq2_text, max_decide_cost=400_000, max_n=40, deadline=None):
    """Search (n, a, b), solve for c. Returns (n, table) or None.
    max_decide_cost bounds n^max(vars) so the judge's decideFin! stays fast;
    max_n bounds the false-cert byte size."""
    import math
    k = max(len(goal_vars(eq1_text)), len(goal_vars(eq2_text)))
    ns = [n for n in range(2, max_n + 1) if n ** k <= max_decide_cost]
    l1, r1 = eq1_text.split("=", 1)
    l2, r2 = eq2_text.split("=", 1)
    L1, R1, L2, R2 = map(kc_parse, (l1, r1, l2, r2))
    for n in ns:
        if deadline is not None and time.time() > deadline:
            return None
        for a in range(n):
            for b in range(n):
                cL1, m1 = af_eval(L1, a, b, n)
                cR1, n1 = af_eval(R1, a, b, n)
                if any(cL1.get(v, 0) != cR1.get(v, 0) for v in set(cL1) | set(cR1)):
                    continue
                d1 = (m1 - n1) % n  # need c*d1 == 0 (mod n) for Eq1
                if d1 == 0:
                    cands = range(n)
                else:
                    cands = range(0, n, n // math.gcd(n, d1))
                cL2, m2 = af_eval(L2, a, b, n)
                cR2, n2 = af_eval(R2, a, b, n)
                var_diff = any(cL2.get(v, 0) != cR2.get(v, 0) for v in set(cL2) | set(cR2))
                d2 = (m2 - n2) % n
                for c in cands:
                    if var_diff or (c * d2) % n != 0:
                        tbl = [[(a * i + b * j + c) % n for j in range(n)] for i in range(n)]
                        return n, tbl
    return None


def try_affine_model(eq1_text, eq2_text):
    """False-side stage: symbolic affine counterexample (any modulus).
    Self-verified in Python before submission; judged by decideFin!, so a
    wrong table can never be accepted."""
    try:
        out = af_find(eq1_text, eq2_text)
    except Exception as e:
        trace(f"[affine] error: {e!r}")
        return False
    if not out:
        return False
    n, table = out
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)
    op = lambda x, y, t=table: t[x][y]
    if not (equation_holds(v1, l1, r1, n, op) and not equation_holds(v2, l2, r2, n, op)):
        return False
    return call_judge("false", make_false_code(n, table)).get("status") == "accepted"


def mf_find_false_model(eq1_text, eq2_text, sizes=(4, 5, 6), per_size=2.5):
    """Backtracking finite-model finder (pure Python, Mace4-style). Searches for
    a magma on Fin n that satisfies Eq1 and violates Eq2 by unit-propagating the
    ground instances of Eq1 over the partial op-table and branching on
    undetermined cells. Returns (n, table_rows) or None. The emitted table is
    judge-checkable via make_false_code/decideFin!, so a wrong table can never be
    accepted. Pure Python — no z3/SMT (those are dev-time only)."""
    import time as _t, itertools as _it
    l1, r1 = eq1_text.split("=", 1)
    l2, r2 = eq2_text.split("=", 1)
    A1, B1 = kc_parse(l1), kc_parse(r1)
    A2, B2 = kc_parse(l2), kc_parse(r2)
    v1 = goal_vars(eq1_text)
    v2 = goal_vars(eq2_text)
    for n in sizes:
        tbl = [None] * (n * n)
        e1 = [dict(zip(v1, t)) for t in _it.product(range(n), repeat=len(v1))]
        e2 = [dict(zip(v2, t)) for t in _it.product(range(n), repeat=len(v2))]

        def ev2(t, env):
            if t[0] == 'V':
                return ('val', env[t[1]])
            ra = ev2(t[2][0], env)
            if ra[0] != 'val':
                return ('none',)
            rb = ev2(t[2][1], env)
            if rb[0] != 'val':
                return ('none',)
            idx = ra[1] * n + rb[1]
            v = tbl[idx]
            return ('val', v) if v is not None else ('open', idx)

        def propagate(trail):
            changed = True
            while changed:
                changed = False
                for env in e1:
                    sl = ev2(A1, env)
                    sr = ev2(B1, env)
                    if sl[0] == 'val' and sr[0] == 'val':
                        if sl[1] != sr[1]:
                            return False
                    elif sl[0] == 'val' and sr[0] == 'open':
                        tbl[sr[1]] = sl[1]; trail.append(sr[1]); changed = True
                    elif sr[0] == 'val' and sl[0] == 'open':
                        tbl[sl[1]] = sr[1]; trail.append(sl[1]); changed = True
            return True

        def eq2_violated():
            for env in e2:
                sl = ev2(A2, env)
                sr = ev2(B2, env)
                if sl[0] == 'val' and sr[0] == 'val' and sl[1] != sr[1]:
                    return True
            return False

        start = _t.time()

        def dfs():
            if _t.time() - start > per_size:
                return None
            trail = []
            if not propagate(trail):
                for i in trail:
                    tbl[i] = None
                return None
            idx = -1
            for i in range(n * n):
                if tbl[i] is None:
                    idx = i; break
            if idx < 0:
                if eq2_violated():
                    return [tbl[i * n + j] for i in range(n) for j in range(n)]
                for i in trail:
                    tbl[i] = None
                return None
            for val in range(n):
                tbl[idx] = val
                r = dfs()
                if r is not None:
                    return r
                tbl[idx] = None
            for i in trail:
                tbl[i] = None
            return None

        flat = dfs()
        if flat is not None:
            return n, [[flat[i * n + j] for j in range(n)] for i in range(n)]
    return None


def mf_walk_find_model(eq1_text, eq2_text, sizes=(5, 6, 7), per_size=2.5,
                       max_flips=4000, noise=0.3, seed=20260608):
    """Local-search (WalkSAT/min-conflicts) finite-model finder. Complements the
    backtracking finder: far better at FINDING satisfiable Fin 5-7 magma models
    that violate Eq2 (the cases unit-propagation DFS misses). Pure Python,
    seeded for reproducibility. Returns (n, table_rows) or None; the table is
    judge-checked, so a wrong one can never be accepted."""
    import time as _t, itertools as _it, random as _r
    rng = _r.Random(seed)
    l1, r1 = eq1_text.split("=", 1)
    l2, r2 = eq2_text.split("=", 1)
    A1, B1 = kc_parse(l1), kc_parse(r1)
    A2, B2 = kc_parse(l2), kc_parse(r2)
    v1 = goal_vars(eq1_text)
    v2 = goal_vars(eq2_text)
    for n in sizes:
        e1 = [dict(zip(v1, t)) for t in _it.product(range(n), repeat=len(v1))]
        e2 = [dict(zip(v2, t)) for t in _it.product(range(n), repeat=len(v2))]

        def ev(t, env, tbl):
            if t[0] == 'V':
                return env[t[1]]
            return tbl[ev(t[2][0], env, tbl) * n + ev(t[2][1], env, tbl)]

        def touched(t, env, tbl, acc):
            if t[0] == 'V':
                return env[t[1]]
            a = touched(t[2][0], env, tbl, acc)
            b = touched(t[2][1], env, tbl, acc)
            idx = a * n + b
            acc.add(idx)
            return tbl[idx]

        def nbad(tbl):
            c = 0
            for env in e1:
                if ev(A1, env, tbl) != ev(B1, env, tbl):
                    c += 1
            return c

        def eq2_violated(tbl):
            for env in e2:
                if ev(A2, env, tbl) != ev(B2, env, tbl):
                    return True
            return False

        start = _t.time()
        while _t.time() - start < per_size:
            tbl = [rng.randrange(n) for _ in range(n * n)]
            for _ in range(max_flips):
                if _t.time() - start > per_size:
                    break
                bad = [env for env in e1 if ev(A1, env, tbl) != ev(B1, env, tbl)]
                if not bad:
                    if eq2_violated(tbl):
                        return n, [[tbl[i * n + j] for j in range(n)] for i in range(n)]
                    tbl[rng.randrange(n * n)] = rng.randrange(n)
                    continue
                env = rng.choice(bad)
                acc = set()
                touched(A1, env, tbl, acc)
                touched(B1, env, tbl, acc)
                acc = list(acc)
                if rng.random() < noise:
                    c = rng.choice(acc)
                    tbl[c] = rng.randrange(n)
                else:
                    best = None; bestc = 10 ** 9
                    for c in acc:
                        old = tbl[c]
                        for val in range(n):
                            if val == old:
                                continue
                            tbl[c] = val
                            sc = nbad(tbl)
                            if sc < bestc:
                                bestc = sc; best = (c, val)
                        tbl[c] = old
                    if best:
                        tbl[best[0]] = best[1]
    return None


def _md_dual(t):
    """Swap the operands of every product (term dual). If Eq1 ⇒ Eq2 is
    false, so is the dual implication, and a model for the dual transposes
    directly into a model for the original — a free second shot per size."""
    if t[0] != 'F':
        return t
    return ('F', kc_OP, (_md_dual(t[2][1]), _md_dual(t[2][0])))


def _md_directed_core(A1, B1, A2, B2, v1, v2, n, budget):
    """Search Fin n for a magma satisfying Eq1 and violating Eq2 by *forcing the
    violation first*: for each Eq2 assignment and target value u, post the ground
    constraint eval(Eq2.lhs)=u, then complete Eq1 by unit propagation + DFS under
    the least-number heuristic (only introduce value k+1 after k has appeared,
    which cuts carrier-relabeling duplicates). Any completion that still leaves
    some Eq2 instance violated is a witness. Returns a flat table or None.
    Target constants are marked ('K', v). Pure Python — no z3/SMT."""
    import time as _t, itertools as _it
    e1 = [dict(zip(v1, t)) for t in _it.product(range(n), repeat=len(v1))]
    e2 = [dict(zip(v2, t)) for t in _it.product(range(n), repeat=len(v2))]
    start = _t.time()

    def ev2(t, env, tbl):
        if t[0] == 'V':
            return ('val', env[t[1]])
        if t[0] == 'K':
            return ('val', t[1])
        ra = ev2(t[2][0], env, tbl)
        if ra[0] != 'val':
            return ('none',)
        rb = ev2(t[2][1], env, tbl)
        if rb[0] != 'val':
            return ('none',)
        idx = ra[1] * n + rb[1]
        v = tbl[idx]
        return ('val', v) if v is not None else ('open', idx)

    def propagate(tbl, cons, trail):
        changed = True
        while changed:
            changed = False
            for (L, R, env) in cons:
                sl = ev2(L, env, tbl); sr = ev2(R, env, tbl)
                if sl[0] == 'val' and sr[0] == 'val':
                    if sl[1] != sr[1]:
                        return False
                elif sl[0] == 'val' and sr[0] == 'open':
                    tbl[sr[1]] = sl[1]; trail.append(sr[1]); changed = True
                elif sr[0] == 'val' and sl[0] == 'open':
                    tbl[sl[1]] = sr[1]; trail.append(sl[1]); changed = True
        return True

    def eq2_violated(tbl):
        for env in e2:
            sl = ev2(A2, env, tbl); sr = ev2(B2, env, tbl)
            if sl[0] == 'val' and sr[0] == 'val' and sl[1] != sr[1]:
                return True
        return False

    base = [(A1, B1, env) for env in e1]

    def solve_with_seed(seed):
        tbl = [None] * (n * n)
        cons = base + seed

        def dfs():
            if _t.time() - start > budget:
                return None
            trail = []
            if not propagate(tbl, cons, trail):
                for i in trail:
                    tbl[i] = None
                return None
            cur_max = -1; idx = -1
            for i in range(n * n):
                v = tbl[i]
                if v is None:
                    if idx < 0:
                        idx = i
                elif v > cur_max:
                    cur_max = v
            if idx < 0:
                if eq2_violated(tbl):
                    return tbl[:]
                for i in trail:
                    tbl[i] = None
                return None
            hi = min(n - 1, cur_max + 1)  # least-number heuristic
            for val in range(hi + 1):
                tbl[idx] = val
                r = dfs()
                if r is not None:
                    return r
                tbl[idx] = None
            for i in trail:
                tbl[i] = None
            return None

        return dfs()

    for env in e2:
        for u in range(n):
            if _t.time() - start > budget:
                return None
            r = solve_with_seed([(A2, ('K', u), env)])
            if r is not None:
                return r
    return None


def mf_directed_find_model(eq1_text, eq2_text, sizes=(4, 5, 6, 7), per_size=2.0):
    """Eq2-directed model finder with a duality pass. Complements the DFS and
    WalkSAT finders: by committing to the Eq2 violation up front it reaches the
    awkward Fin 5 / Fin 6 counterexamples they miss. Each size is tried on the
    problem and (transposed) on its dual. Returns (n, table_rows) or None; the
    table is judge-checked by decideFin!, so a wrong one is never accepted."""
    l1, r1 = eq1_text.split("=", 1)
    l2, r2 = eq2_text.split("=", 1)
    A1, B1 = kc_parse(l1), kc_parse(r1)
    A2, B2 = kc_parse(l2), kc_parse(r2)
    v1, v2 = goal_vars(eq1_text), goal_vars(eq2_text)
    dA1, dB1, dA2, dB2 = _md_dual(A1), _md_dual(B1), _md_dual(A2), _md_dual(B2)
    for n in sizes:
        flat = _md_directed_core(A1, B1, A2, B2, v1, v2, n, per_size / 2.0)
        if flat is not None:
            return n, [[flat[i * n + j] for j in range(n)] for i in range(n)]
        flat = _md_directed_core(dA1, dB1, dA2, dB2, v1, v2, n, per_size / 2.0)
        if flat is not None:  # transpose the dual model back to the original
            return n, [[flat[j * n + i] for j in range(n)] for i in range(n)]
    return None


# ── Domain-propagation model finder (mf2_ namespace) ────────────
# SEM/Mace4-style: per-cell bitmask domains; every Eq1 ground instance is
# re-evaluated bottom-up with value SETS (union over arg combos — a sound
# over-approximation, so an empty LHS∩RHS intersection is a conflict). Unit
# rules assign/prune single open cells. MRV branching + least-number symmetry
# breaking via the designated-elements rule (allowed values = domain∩D plus
# ONE fresh representative, D = row/col/value of assigned cells + branch
# cell's indices + directed-env constants). Quasigroup/Latin modes add
# alldifferent row/col pruning — empirically most hard2/hard1 residual
# counterexamples are (idempotent) quasigroups, where this search needs only
# a handful of nodes even at Fin 8.


def mf2_compile(t, env):
    if t[0] == 'V':
        return env[t[1]]
    return ('c', mf2_compile(t[2][0], env), mf2_compile(t[2][1], env))


class mf2_Finder:
    def __init__(self, eq1, eq2, n):
        import itertools as _it
        self.n = n
        self.eq1_text, self.eq2_text = eq1, eq2
        l1, r1 = eq1.split("=", 1)
        l2, r2 = eq2.split("=", 1)
        A1, B1 = kc_parse(l1), kc_parse(r1)
        self.A2s, self.B2s = kc_parse(l2), kc_parse(r2)
        v1 = goal_vars(eq1)
        self.insts = []
        for vals in _it.product(range(n), repeat=len(v1)):
            env = dict(zip(v1, vals))
            self.insts.append((mf2_compile(A1, env), mf2_compile(B1, env), True))
        self.neq_idx = None

    def add_neq(self, env):
        self.insts.append((mf2_compile(self.A2s, env), mf2_compile(self.B2s, env), False))
        self.neq_idx = len(self.insts) - 1
        self.pinned = 0
        for v in env.values():
            self.pinned |= 1 << v

    def solve(self, deadline, qg=False, idem=False, rows=None, cols=None):
        n = self.n
        full = (1 << n) - 1
        dom = [full] * (n * n)
        self.adr = qg if rows is None else rows
        self.adc = qg if cols is None else cols
        self.qg = self.adr or self.adc
        if idem:
            for i in range(n):
                dom[i * n + i] = 1 << i
        watch = [set() for _ in range(n * n)]
        sbit = [1 << v for v in range(n)]
        popcount = getattr(int, "bit_count", None) or (lambda x: bin(x).count("1"))

        def eval_sets(term, dom):
            if isinstance(term, int):
                return sbit[term], -1, ()
            ml, _, tl = eval_sets(term[1], dom)
            mr, _, tr = eval_sets(term[2], dom)
            out = 0
            unit = -1
            a_vals = [a for a in range(n) if ml >> a & 1]
            b_vals = [b for b in range(n) if mr >> b & 1]
            cells = []
            for a in a_vals:
                base = a * n
                for b in b_vals:
                    c = base + b
                    cells.append(c)
                    out |= dom[c]
            if len(cells) == 1 and popcount(dom[cells[0]]) > 1:
                unit = cells[0]
            return out, unit, tl + tr + tuple(cells)

        def check_inst(i, dom, pending):
            L, R, is_eq = self.insts[i]
            mL, uL, tL = eval_sets(L, dom)
            mR, uR, tR = eval_sets(R, dom)
            # watches only grow: after backtrack domains widen, so an old
            # dependency may become live again — never discard.
            for c in set(tL) | set(tR):
                watch[c].add(i)
            if is_eq:
                if (mL & mR) == 0:
                    return False
                if uR >= 0 and popcount(mL) == 1:
                    pending.append((uR, mL))
                if uL >= 0 and popcount(mR) == 1:
                    pending.append((uL, mR))
            else:
                if popcount(mL) == 1 and mL == mR and uL < 0 and uR < 0:
                    return False
                if uR >= 0 and popcount(mL) == 1:
                    pending.append((uR, dom[uR] & ~mL))
                if uL >= 0 and popcount(mR) == 1:
                    pending.append((uL, dom[uL] & ~mR))
            return True

        def qg_prune(cell, vmask, trail, queue):
            r, c = cell // n, cell % n
            others = []
            if self.adr:
                others += [r * n + jj for jj in range(n) if jj != c]
            if self.adc:
                others += [ii * n + c for ii in range(n) if ii != r]
            for other in others:
                od = dom[other]
                if od & vmask:
                    nd = od & ~vmask
                    if nd == 0:
                        return False
                    trail.append((other, od))
                    dom[other] = nd
                    for j in watch[other]:
                        queue.append(j)
                    if nd & (nd - 1) == 0:
                        if not qg_prune(other, nd, trail, queue):
                            return False
            return True

        def propagate(dom, dirty, trail):
            queue = list(dirty)
            qi = 0
            while qi < len(queue):
                i = queue[qi]; qi += 1
                pending = []
                if not check_inst(i, dom, pending):
                    return False
                for cell, mask in pending:
                    new = dom[cell] & mask
                    if new == dom[cell]:
                        continue
                    if new == 0:
                        return False
                    trail.append((cell, dom[cell]))
                    dom[cell] = new
                    for j in watch[cell]:
                        if j not in queue[qi:]:
                            queue.append(j)
                    if self.qg and new & (new - 1) == 0:
                        if not qg_prune(cell, new, trail, queue):
                            return False
            return True

        trail0 = []
        ok0 = True
        if self.qg and idem:
            q0 = []
            for i in range(n):
                if not qg_prune(i * n + i, dom[i * n + i], trail0, q0):
                    ok0 = False
                    break
        # initial propagation only does work if some domain is restricted
        all_dirty = False
        if idem or self.neq_idx is not None:
            if not ok0 or not propagate(dom, range(len(self.insts)), trail0):
                return None
        else:
            all_dirty = True

        pinned = getattr(self, "pinned", 0)

        def designated(dom):
            D = pinned
            for c in range(n * n):
                d = dom[c]
                if d and d & (d - 1) == 0:
                    D |= d | (1 << (c // n)) | (1 << (c % n))
            return D

        def dfs(dom, depth):
            if time.time() > deadline:
                raise TimeoutError
            best = -1; bestc = n + 1
            for c in range(n * n):
                pc = popcount(dom[c])
                if 1 < pc < bestc:
                    bestc = pc; best = c
                    if pc == 2:
                        break
            if best < 0:
                # fully assigned: concrete-verify Eq1 holds AND Eq2 fails
                tbl = [[dom[i * n + j].bit_length() - 1 for j in range(n)] for i in range(n)]
                op = lambda a, b: tbl[a][b]
                v1, l1, r1 = parse_equation(self.eq1_text)
                v2, l2, r2 = parse_equation(self.eq2_text)
                if equation_holds(v1, l1, r1, n, op) and not equation_holds(v2, l2, r2, n, op):
                    return tbl
                return None
            D = designated(dom) | (1 << (best // n)) | (1 << (best % n))
            fresh = dom[best] & ~D
            cand = dom[best] & D
            if fresh:
                cand |= fresh & (-fresh)  # one fresh representative (lowest)
            for v in range(n):
                if not (cand >> v & 1):
                    continue
                trail = [(best, dom[best])]
                dom[best] = 1 << v
                if all_dirty and depth == 0:
                    q0 = list(range(len(self.insts)))
                else:
                    q0 = list(watch[best])
                okq = True
                if self.qg:
                    okq = qg_prune(best, 1 << v, trail, q0)
                if okq and propagate(dom, q0, trail):
                    r = dfs(dom, depth + 1)
                    if r is not None:
                        return r
                for cell, old in reversed(trail):
                    dom[cell] = old
            return None

        try:
            return dfs(dom, 0)
        except TimeoutError:
            return None


# (mode, n, weight) — weights normalized against the per-problem budget.
# Ordering: cheap idempotent-quasigroup probes and small general/directed
# search first, Latin variants next, the expensive general Fin 6-7 last.
mf2_SCHEDULE = [
    ("idem", 4, 0.3), ("idem", 5, 0.5), ("idem", 6, 0.8),
    ("directed", 4, 0.8),
    ("general", 4, 0.8), ("general", 5, 1.5),
    ("idem", 7, 1.2), ("idem", 8, 2.5),
    ("qg", 4, 0.3), ("qg", 5, 0.8), ("qg", 6, 1.0),
    ("rows", 4, 0.3), ("rows", 5, 0.8), ("rows", 6, 1.0),
    ("cols", 4, 0.3), ("cols", 5, 0.8), ("cols", 6, 1.0),
    ("general", 6, 2.5),
    ("qg", 7, 1.2), ("rows", 7, 1.2), ("cols", 7, 1.2),
    ("idem", 9, 2.0), ("qg", 8, 2.0),
    ("general", 7, 3.0),
    ("directed", 5, 2.0), ("directed", 6, 3.0),
    # Extended large-Fin tier (2026-06-12). The finder is schedule-exhaustion-
    # bound, not clock-bound: on the genuinely-hard residual the Fin<=9 schedule
    # completes in ~15s, so the spare per-problem budget (cap is 3600s) is only
    # useful if it also searches BIGGER models. These cells are strictly
    # additive — they run after everything above, so they can only add solves,
    # never remove them, and every table is still verified by decideFin!.
    ("rows", 8, 1.5), ("cols", 8, 1.5),
    ("qg", 9, 2.5), ("rows", 9, 2.0), ("cols", 9, 2.0),
    ("idem", 10, 3.0), ("qg", 10, 3.0),
    ("idem", 11, 3.0), ("qg", 11, 3.0),
    ("directed", 7, 3.0), ("general", 8, 3.0),
]

mf2_MINABS = {("idem", 8): 2.2, ("idem", 9): 2.5, ("qg", 8): 2.2,
              ("directed", 4): 1.0, ("general", 4): 1.0,
              # Floors for the extended large-Fin tier so a big search space
              # isn't abandoned after a fraction of a second when many cells
              # share the budget.
              ("qg", 9): 2.5, ("rows", 9): 2.0, ("cols", 9): 2.0,
              ("idem", 10): 3.0, ("qg", 10): 3.0,
              ("idem", 11): 3.0, ("qg", 11): 3.0,
              ("directed", 7): 2.5, ("general", 8): 2.5}


def mf2_find_portfolio(eq1, eq2, budget_s):
    """Weighted (mode, size) schedule over the domain-propagation finder.
    Returns (n, table) or None. Skips (mode, n) cells whose ground-instance
    count would be unmanageable in pure Python."""
    start = time.time()
    total_w = sum(w for _, _, w in mf2_SCHEDULE)
    scale = budget_s / total_w
    k1 = len(goal_vars(eq1))
    v2 = goal_vars(eq2)

    def left():
        return budget_s - (time.time() - start)

    for mode, n, w in mf2_SCHEDULE:
        if left() <= 0.2:
            return None
        if n ** k1 > 40000:
            continue
        slot = min(max(w * scale, mf2_MINABS.get((mode, n), 0.3)), left())
        if mode == "directed":
            envs = []

            def gen(prefix):
                if len(prefix) == len(v2):
                    envs.append(dict(zip(v2, prefix)))
                    return
                hi = (max(prefix) + 1) if prefix else 0
                for v in range(min(hi, n - 1) + 1):
                    gen(prefix + [v])

            gen([])
            per = max(0.3, slot / max(1, len(envs)))
            t_end = time.time() + slot
            for env in envs:
                if time.time() > t_end or left() <= 0:
                    break
                f = mf2_Finder(eq1, eq2, n)
                f.add_neq(env)
                r = f.solve(min(time.time() + per, t_end))
                if r is not None:
                    trace(f"[mf2] directed Fin{n}")
                    return n, r
            continue
        f = mf2_Finder(eq1, eq2, n)
        kw = {}
        if mode == "idem":
            kw = dict(qg=True, idem=True)
        elif mode == "qg":
            kw = dict(qg=True)
        elif mode == "rows":
            kw = dict(rows=True, cols=False)
        elif mode == "cols":
            kw = dict(rows=False, cols=True)
        r = f.solve(time.time() + slot, **kw)
        if r is not None:
            trace(f"[mf2] {mode} Fin{n}")
            return n, r
    return None


def try_model_finder(eq1_text, eq2_text, budget=MF2_PORTFOLIO_BUDGET):
    """False-side stage: find a Fin counterexample (Eq1 holds, Eq2 fails) the
    exhaustive Fin 2-3 + structured Fin 4-7 search misses. Three complementary
    pure-Python passes: (1) backtracking + unit propagation (fast, reliable for
    Fin 4); (2) WalkSAT local search (recovers many Fin 5-7 models the DFS
    misses); (3) Eq2-directed DFS + duality (reaches the awkward Fin 5 / Fin 6
    models the first two miss). Emits a table judged by decideFin!, so a wrong
    table is never accepted."""
    out = None
    try:
        out = mf2_find_portfolio(eq1_text, eq2_text, budget_s=budget)
        if out is None:
            out = mf_find_false_model(eq1_text, eq2_text, sizes=(4, 5, 6), per_size=1.5)
        if out is None:
            out = mf_walk_find_model(eq1_text, eq2_text, sizes=(5, 6, 7), per_size=2.0)
        if out is None:
            out = mf_directed_find_model(eq1_text, eq2_text, sizes=(4, 5, 6, 7), per_size=2.0)
    except Exception as e:
        trace(f"[modelfinder] error: {e!r}")
        return False
    if not out:
        return False
    n, table = out
    # Self-verify before submission (sound: decideFin! checks the same thing)
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)
    op = lambda a, b, t=table: t[a][b]
    if not (equation_holds(v1, l1, r1, n, op) and not equation_holds(v2, l2, r2, n, op)):
        trace("[modelfinder] candidate failed self-verification; dropped")
        return False
    return call_judge("false", make_false_code(n, table)).get("status") == "accepted"





# ── SAT-based complete false-model finder (pure Python; no z3) ──────
# Sound & complete finite-model search for the hard FALSE residual that the
# heuristic mf2 portfolio misses: general (non-quasigroup, non-affine) magmas
# on Fin 5-7 whose op-table is highly constrained. Encodes "Eq1 holds for ALL
# variable assignments AND some assignment violates Eq2" as CNF — one-hot cell
# variables plus definitional subterm-value clauses (leaf products collapse
# straight onto cell vars) — and solves with an in-process CDCL (2-watched
# literals, 1-UIP learning, VSIDS, phase saving, Luby restarts). Every model is
# still self-verified here and judged by decideFin!, so a bad encoding can only
# ever miss, never produce a wrong answer. Closes the Fin 6 general residual
# (e.g. hard2_0093/0124/0125/0176, hard1_0009) the quasigroup modes can't reach.

def _sat_luby(i):
    k = 1
    while True:
        if i == (1 << k) - 1:
            return 1 << (k - 1)
        if (1 << (k - 1)) <= i < (1 << k) - 1:
            return _sat_luby(i - (1 << (k - 1)) + 1)
        k += 1


class _SatCDCL:
    def __init__(self, nvars):
        self.n = nvars
        self.clauses = []
        self.watches = {}
        for v in range(1, nvars + 1):
            self.watches[v] = []
            self.watches[-v] = []
        self.assign = {}
        self.level = {}
        self.reason = {}
        self.trail = []
        self.qhead = 0
        self.dl = 0
        self.act = [0.0] * (nvars + 1)
        self.inc = 1.0
        self.ok = True
        self.phase = {}

    def add_clause(self, lits):
        seen = set()
        out = []
        for l in lits:
            if -l in seen:
                return
            if l not in seen:
                seen.add(l)
                out.append(l)
        if not out:
            self.ok = False
            return
        ci = len(self.clauses)
        self.clauses.append(out)
        if len(out) == 1:
            if not self._enqueue(out[0], None):
                self.ok = False
        else:
            self.watches[out[0]].append(ci)
            self.watches[out[1]].append(ci)

    def val(self, lit):
        a = self.assign.get(abs(lit))
        return None if a is None else (a == (lit > 0))

    def _enqueue(self, lit, reason):
        v = abs(lit)
        want = lit > 0
        a = self.assign.get(v)
        if a is not None:
            return a == want
        self.assign[v] = want
        self.level[v] = self.dl
        self.reason[v] = reason
        self.trail.append(lit)
        return True

    def _propagate(self):
        while self.qhead < len(self.trail):
            p = self.trail[self.qhead]
            self.qhead += 1
            fl = -p
            wl = self.watches[fl]
            self.watches[fl] = new = []
            i = 0
            conflict = None
            while i < len(wl):
                ci = wl[i]
                i += 1
                cl = self.clauses[ci]
                if cl[0] == fl:
                    cl[0], cl[1] = cl[1], cl[0]
                if self.val(cl[0]) is True:
                    new.append(ci)
                    continue
                rep = -1
                for k in range(2, len(cl)):
                    if self.val(cl[k]) is not False:
                        rep = k
                        break
                if rep != -1:
                    cl[1], cl[rep] = cl[rep], cl[1]
                    self.watches[cl[1]].append(ci)
                    continue
                new.append(ci)
                if self.val(cl[0]) is False:
                    conflict = ci
                    new.extend(wl[i:])
                    break
                else:
                    self._enqueue(cl[0], ci)
            if conflict is not None:
                return conflict
        return None

    def _bump(self, v):
        self.act[v] += self.inc
        if self.act[v] > 1e100:
            for i in range(1, self.n + 1):
                self.act[i] *= 1e-100
            self.inc *= 1e-100

    def _analyze(self, conf):
        learnt = [None]
        seen = set()
        counter = 0
        idx = len(self.trail) - 1
        ci = conf
        p = None
        while True:
            cl = self.clauses[ci]
            start = 0 if p is None else 1
            for j in range(start, len(cl)):
                q = cl[j]
                v = abs(q)
                if v in seen or self.level[v] == 0:
                    continue
                seen.add(v)
                self._bump(v)
                if self.level[v] >= self.dl:
                    counter += 1
                else:
                    learnt.append(q)
            while abs(self.trail[idx]) not in seen:
                idx -= 1
            p = self.trail[idx]
            idx -= 1
            seen.discard(abs(p))
            counter -= 1
            if counter == 0:
                break
            ci = self.reason[abs(p)]
        learnt[0] = -p
        if len(learnt) == 1:
            return learnt, 0
        mxi = 1
        mx = self.level[abs(learnt[1])]
        for i in range(2, len(learnt)):
            if self.level[abs(learnt[i])] > mx:
                mx = self.level[abs(learnt[i])]
                mxi = i
        learnt[1], learnt[mxi] = learnt[mxi], learnt[1]
        return learnt, self.level[abs(learnt[1])]

    def _backtrack(self, lvl):
        while self.trail and self.level[abs(self.trail[-1])] > lvl:
            lit = self.trail.pop()
            v = abs(lit)
            self.phase[v] = self.assign[v]
            del self.assign[v]
            del self.level[v]
            self.reason.pop(v, None)
        self.qhead = len(self.trail)
        self.dl = lvl

    def _pick(self):
        best = -1
        ba = -1.0
        for v in range(1, self.n + 1):
            if v not in self.assign and self.act[v] > ba:
                ba = self.act[v]
                best = v
        return best if best != -1 else None

    def solve(self, deadline=None):
        import time as _t
        if not self.ok:
            return False
        if self._propagate() is not None:
            return False
        confl = 0
        lubi = 1
        unit = 100
        since = 0
        while True:
            c = self._propagate()
            if c is not None:
                confl += 1
                since += 1
                if self.dl == 0:
                    return False
                learnt, bl = self._analyze(c)
                self._backtrack(bl)
                ci = len(self.clauses)
                self.clauses.append(learnt)
                if len(learnt) == 1:
                    self._enqueue(learnt[0], None)
                else:
                    self.watches[learnt[0]].append(ci)
                    self.watches[learnt[1]].append(ci)
                    self._enqueue(learnt[0], ci)
                self.inc /= 0.95
                if since >= unit * _sat_luby(lubi):
                    lubi += 1
                    since = 0
                    self._backtrack(0)
                if deadline and (confl & 1023) == 0 and _t.time() > deadline:
                    return None
            else:
                v = self._pick()
                if v is None:
                    return True
                self.dl += 1
                lit = v if self.phase.get(v, False) else -v
                self._enqueue(lit, None)

    def model(self):
        return {v: self.assign.get(v, False) for v in range(1, self.n + 1)}


def sat_parse_tree(text):
    vs = []
    seen = set()
    for v in re.findall(r"\b([a-z])\b", text):
        if v not in seen:
            seen.add(v)
            vs.append(v)

    def to(s):
        s = s.strip()
        while len(s) >= 2 and s[0] == "(" and s[-1] == ")":
            d = 0
            m = True
            for i, c in enumerate(s):
                d += c == "("
                d -= c == ")"
                if d == 0 and i < len(s) - 1:
                    m = False
                    break
            if m:
                s = s[1:-1].strip()
            else:
                break
        d = 0
        last = -1
        for i, c in enumerate(s):
            d += c == "("
            d -= c == ")"
            if (c == "◇" or c == "*") and d == 0:
                last = i
        if last >= 0:
            return ("op", to(s[:last]), to(s[last + 1:]))
        return ("var", s)

    l, r = text.split("=", 1)
    return vs, to(l), to(r)


class _SatEnc:
    def __init__(self, n):
        self.n = n
        self.nv = n * n * n
        self.clauses = []

    def V(self, a, b, k):
        return 1 + ((a * self.n + b) * self.n + k)

    def alloc(self):
        self.nv += 1
        return self.nv

    def add(self, c):
        self.clauses.append(c)

    def exactly_one(self, lits):
        self.add(list(lits))
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.add([-lits[i], -lits[j]])

    def cells(self):
        n = self.n
        for a in range(n):
            for b in range(n):
                self.exactly_one([self.V(a, b, k) for k in range(n)])

    def litof(self, handle, k):
        if handle[0] == "const":
            return True if k == handle[1] else False
        return handle[1][k]

    def value(self, node, g):
        n = self.n
        if node[0] == "var":
            return ("const", g[node[1]])
        HL = self.value(node[1], g)
        HR = self.value(node[2], g)
        if HL[0] == "const" and HR[0] == "const":
            i, j = HL[1], HR[1]
            return ("lits", [self.V(i, j, k) for k in range(n)])
        T = [self.alloc() for _ in range(n)]
        self.exactly_one(T)
        for i in range(n):
            li = self.litof(HL, i)
            if li is False:
                continue
            for j in range(n):
                lj = self.litof(HR, j)
                if lj is False:
                    continue
                for k in range(n):
                    cl = []
                    if li is not True:
                        cl.append(-li)
                    if lj is not True:
                        cl.append(-lj)
                    cl.append(-self.V(i, j, k))
                    cl.append(T[k])
                    self.add(cl)
        return ("lits", T)

    def eq_force(self, A, B):
        for k in range(self.n):
            la = self.litof(A, k)
            lb = self.litof(B, k)
            if la is True:
                if lb is True:
                    continue
                if lb is False:
                    self.add([])
                else:
                    self.add([lb])
            elif la is False:
                if lb is True:
                    self.add([])
                elif lb is False:
                    continue
                else:
                    self.add([-lb])
            else:
                if lb is True:
                    self.add([la])
                elif lb is False:
                    self.add([-la])
                else:
                    self.add([-la, lb])
                    self.add([la, -lb])


def sat_find_model(eq1_text, eq2_text, n, deadline):
    v1, l1, r1 = sat_parse_tree(eq1_text)
    v2, l2, r2 = sat_parse_tree(eq2_text)
    E = _SatEnc(n)
    E.cells()
    for g in product(range(n), repeat=len(v1)):
        env = dict(zip(v1, g))
        A = E.value(l1, env)
        B = E.value(r1, env)
        E.eq_force(A, B)
    zs = []
    for g in product(range(n), repeat=len(v2)):
        env = dict(zip(v2, g))
        A = E.value(l2, env)
        B = E.value(r2, env)
        z = E.alloc()
        zs.append(z)
        for k in range(n):
            la = E.litof(A, k)
            lb = E.litof(B, k)
            cl = [-z]
            if la is True:
                pass
            elif la is False:
                continue
            else:
                cl.append(-la)
            if lb is True:
                pass
            elif lb is False:
                continue
            else:
                cl.append(-lb)
            E.add(cl)
    E.add(zs)
    s = _SatCDCL(E.nv)
    for c in E.clauses:
        s.add_clause(c)
    if s.solve(deadline=deadline) is not True:
        return None
    m = s.model()
    return [[next(k for k in range(n) if m[E.V(a, b, k)]) for b in range(n)]
            for a in range(n)]


def try_sat_finder(eq1_text, eq2_text, sizes=(5, 6, 7), budget=SAT_FINDER_BUDGET):
    """Last-resort false-side stage: complete CDCL model search for the hard
    general residual the heuristic finders miss. Self-verifies before judging."""
    import time as _t
    out = None
    try:
        per = budget / max(1, len(sizes))
        for n in sizes:
            if n ** 3 * (n ** len(goal_vars(eq1_text))) > 4_000_000:
                continue  # encoding too large for pure Python at this size
            tbl = sat_find_model(eq1_text, eq2_text, n, _t.time() + per)
            if tbl is not None:
                out = (n, tbl)
                break
    except Exception as e:
        trace(f"[satfinder] error: {e!r}")
        return False
    if not out:
        return False
    n, table = out
    v1, l1, r1 = parse_equation(eq1_text)
    v2, l2, r2 = parse_equation(eq2_text)
    op = lambda a, b, t=table: t[a][b]
    if not (equation_holds(v1, l1, r1, n, op) and not equation_holds(v2, l2, r2, n, op)):
        trace("[satfinder] candidate failed self-verification; dropped")
        return False
    trace(f"[satfinder] Fin{n} candidate")
    return call_judge("false", make_false_code(n, table)).get("status") == "accepted"


# ── Goal-directed narrowing prover (nrw_ namespace) ───────────────
# TRUE-side engine that complements kc_* completion. Where completion does
# forward ordered-completion of the hypothesis and then ONLY-REDUCES the goal
# sides to a normal form (so it cannot find proofs that must EXPAND a term),
# this prover does goal-directed bidirectional NARROWING: it skolemizes the
# goal variables to constants and searches for an equational path between the
# two goal sides using the hypothesis as a two-way rewrite under unification
# (superposition). It carries an explicit proof term, recomputes that proof's
# type for a self-check, grounds out any leftover free variables to an in-scope
# goal variable, and renders Lean `exact` syntax. Every proof is finally
# checked by the Lean judge, so a malformed proof can never be accepted.
#
# term: ('o',l,r) | ('c',name) skolem constant (a goal variable) | ('v',name) free var
import time as _nrw_time

def nrw_parse(text, as_goal):
    s = text.strip()
    def sp(s):
        while len(s) >= 2 and s[0] == '(' and s[-1] == ')':
            d = 0; ok = True
            for i, c in enumerate(s):
                d += c == '('; d -= c == ')'
                if d == 0 and i < len(s) - 1: ok = False; break
            if ok: s = s[1:-1].strip()
            else: break
        return s
    def go(s):
        s = s.strip(); s = sp(s); s = s.strip(); d = 0; last = -1
        for i, c in enumerate(s):
            d += c == '('; d -= c == ')'
            if d == 0 and c in '◇*': last = i
        if last < 0:
            return ('c', s) if as_goal else ('v', s)
        return ('o', go(s[:last]), go(s[last + 1:]))
    return go(s)

def nrw_show(t):
    if t[0] == 'o': return '(' + nrw_show(t[1]) + ' ◇ ' + nrw_show(t[2]) + ')'
    return t[1]

def nrw_size(t):
    st = [t]; n = 0
    while st:
        x = st.pop(); n += 1
        if x[0] == 'o': st.append(x[1]); st.append(x[2])
    return n

def nrw_deref(t, s):
    while t[0] == 'v' and t[1] in s: t = s[t[1]]
    return t

def nrw_occurs(v, t, s):
    t = nrw_deref(t, s)
    if t[0] == 'v': return t[1] == v
    if t[0] == 'o': return nrw_occurs(v, t[1], s) or nrw_occurs(v, t[2], s)
    return False

def nrw_unify(x, y, s):
    if s is None: return None
    x = nrw_deref(x, s); y = nrw_deref(y, s)
    if x[0] == 'v':
        if y[0] == 'v' and x[1] == y[1]: return s
        if nrw_occurs(x[1], y, s): return None
        s2 = dict(s); s2[x[1]] = y; return s2
    if y[0] == 'v':
        if nrw_occurs(y[1], x, s): return None
        s2 = dict(s); s2[y[1]] = x; return s2
    if x[0] == 'c' or y[0] == 'c':
        return s if (x[0] == 'c' and y[0] == 'c' and x[1] == y[1]) else None
    s = nrw_unify(x[1], y[1], s)
    if s is None: return None
    return nrw_unify(x[2], y[2], s)

def nrw_app(t, s):
    t = nrw_deref(t, s)
    if t[0] == 'o': return ('o', nrw_app(t[1], s), nrw_app(t[2], s))
    return t

def nrw_rename(t, suf):
    if t[0] == 'v': return ('v', t[1] + suf)
    if t[0] == 'o': return ('o', nrw_rename(t[1], suf), nrw_rename(t[2], suf))
    return t

def nrw_positions(t, path=()):
    if t[0] == 'o':
        yield path, t
        yield from nrw_positions(t[1], path + (0,))
        yield from nrw_positions(t[2], path + (1,))

def nrw_repl(t, path, new):
    if not path: return new
    i = path[0]
    if i == 0: return ('o', nrw_repl(t[1], path[1:], new), t[2])
    return ('o', t[1], nrw_repl(t[2], path[1:], new))

def nrw_key(t):
    if t[0] == 'o': return '(' + nrw_key(t[1]) + nrw_key(t[2]) + ')'
    return t[1] if t[0] == 'c' else '?' + t[1]

# ---- proof terms: ('H',args) ('SYM',P) ('TRANS',P,Q) ('CL',t,P) ('CR',t,P) ('REFL',t)
_NRW = {"vars": None, "lhs": None, "rhs": None}

def nrw_psub(t, s):
    if t[0] == 'v': return s.get(t[1], t)
    if t[0] == 'o': return ('o', nrw_psub(t[1], s), nrw_psub(t[2], s))
    return t

def nrw_pinst(P, s):
    k = P[0]
    if k == 'H': return ('H', tuple(nrw_app(a, s) for a in P[1]))
    if k == 'SYM': return ('SYM', nrw_pinst(P[1], s))
    if k == 'TRANS': return ('TRANS', nrw_pinst(P[1], s), nrw_pinst(P[2], s))
    if k in ('CL', 'CR'): return (k, nrw_app(P[1], s), nrw_pinst(P[2], s))
    if k == 'REFL': return ('REFL', nrw_app(P[1], s))

def nrw_ptype(P):
    k = P[0]
    if k == 'H':
        s = dict(zip(_NRW["vars"], P[1]))
        return (nrw_psub(_NRW["lhs"], s), nrw_psub(_NRW["rhs"], s))
    if k == 'SYM':
        a, b = nrw_ptype(P[1]); return (b, a)
    if k == 'TRANS':
        a, b = nrw_ptype(P[1]); c, d = nrw_ptype(P[2])
        assert b == c, "trans mismatch"
        return (a, d)
    if k == 'CL':
        a, b = nrw_ptype(P[2]); return (('o', a, P[1]), ('o', b, P[1]))
    if k == 'CR':
        a, b = nrw_ptype(P[2]); return (('o', P[1], a), ('o', P[1], b))
    if k == 'REFL':
        return (P[1], P[1])

def nrw_cong_wrap(full, path, inner):
    if not path: return inner
    i = path[0]
    if i == 0: return ('CL', full[2], nrw_cong_wrap(full[1], path[1:], inner))
    return ('CR', full[1], nrw_cong_wrap(full[2], path[1:], inner))

def nrw_render(P):
    k = P[0]
    if k == 'H': return "(h " + " ".join(nrw_show(a) for a in P[1]) + ")"
    if k == 'SYM': return "(" + nrw_render(P[1]) + ").symm"
    if k == 'TRANS': return "((" + nrw_render(P[1]) + ").trans (" + nrw_render(P[2]) + "))"
    # Lambda binder uses a multi-character name so it can never shadow a goal
    # variable (those are single lowercase letters, e.g. order-5 laws use r/u/v/w/x/y/z).
    if k == 'CL': return "(congrArg (fun nrwHole => nrwHole ◇ " + nrw_show(P[1]) + ") " + nrw_render(P[2]) + ")"
    if k == 'CR': return "(congrArg (fun nrwHole => " + nrw_show(P[1]) + " ◇ nrwHole) " + nrw_render(P[2]) + ")"
    if k == 'REFL': return "(rfl)"

def nrw_proof_freevars(P, acc):
    k = P[0]
    if k == 'H':
        for a in P[1]: nrw_term_freevars(a, acc)
    elif k == 'SYM': nrw_proof_freevars(P[1], acc)
    elif k == 'TRANS': nrw_proof_freevars(P[1], acc); nrw_proof_freevars(P[2], acc)
    elif k in ('CL', 'CR'): nrw_term_freevars(P[1], acc); nrw_proof_freevars(P[2], acc)
    elif k == 'REFL': nrw_term_freevars(P[1], acc)

def nrw_term_freevars(t, acc):
    if t[0] == 'v': acc.add(t[1])
    elif t[0] == 'o': nrw_term_freevars(t[1], acc); nrw_term_freevars(t[2], acc)

def nrw_skolems(t, acc):
    if t[0] == 'c': acc.add(t[1])
    elif t[0] == 'o': nrw_skolems(t[1], acc); nrw_skolems(t[2], acc)

def nrw_setup(eq1):
    _NRW["lhs"] = nrw_parse(eq1.split('=', 1)[0], False)
    _NRW["rhs"] = nrw_parse(eq1.split('=', 1)[1], False)
    seen = []
    for v in re.findall(r"\b([a-z])\b", eq1):
        if v not in seen: seen.append(v)
    _NRW["vars"] = seen

def nrw_prove_bidir(eq1, eq2, max_size=26, max_nodes=600000, tb=20.0):
    """Bidirectional narrowing for a full goal `eq2`. Thin wrapper that parses
    the two goal sides and delegates to nrw_prove_terms. Returns
    (status, proof_or_None)."""
    nrw_setup(eq1)
    gl = nrw_parse(eq2.split('=', 1)[0], True)
    gr = nrw_parse(eq2.split('=', 1)[1], True)
    return nrw_prove_terms(gl, gr, max_size=max_size, max_nodes=max_nodes, tb=tb)


def nrw_prove_terms(gl, gr, max_size=26, max_nodes=600000, tb=20.0, filler_pool=None):
    """Bidirectional narrowing between two already-parsed GROUND terms gl, gr
    (skolem constants = goal variables). Assumes nrw_setup() has been called so
    _NRW holds the hypothesis. Returns (status, proof_or_None) where the proof,
    if any, establishes gl = gr. status in {'PROVED','TIMEOUT','EXHAUSTED','CAP'}.
    Deadline is checked inside the hot loops so wall time stays within ~tb.
    filler_pool: skolem names to draw the free-var ground-out filler from
    (defaults to the skolems occurring in gl/gr)."""
    rules = [(_NRW["lhs"], _NRW["rhs"], False), (_NRW["rhs"], _NRW["lhs"], True)]
    deadline = _nrw_time.time() + tb
    ctr = [0]
    sk = set(filler_pool) if filler_pool else set()
    nrw_skolems(gl, sk); nrw_skolems(gr, sk)
    filler = ('c', sorted(sk)[0]) if sk else None

    def ground_out(Pf):
        fv = set(); nrw_proof_freevars(Pf, fv)
        if fv and filler is not None:
            return nrw_pinst(Pf, {v: filler for v in fv})
        return Pf

    F = [(gl, ('REFL', gl))]; B = [(gr, ('REFL', gr))]
    Fseen = {nrw_key(gl)}; Bseen = {nrw_key(gr)}
    Fall = list(F); Ball = list(B)

    def meet(side_a, side_b, a_is_forward):
        # Build the proof so the FORWARD proof (gl=meet) always comes first and
        # the backward (gr=meet) is reversed, yielding gl=gr regardless of which
        # frontier the newly-expanded nodes came from.
        cnt = 0
        for (t1, P1) in side_a:
            for (t2, P2) in side_b:
                cnt += 1
                if cnt & 1023 == 0 and _nrw_time.time() > deadline:
                    return None
                mu = nrw_unify(t1, t2, {})
                if mu is not None:
                    Pf, Pb = (P1, P2) if a_is_forward else (P2, P1)
                    return ground_out(('TRANS', nrw_pinst(Pf, mu), ('SYM', nrw_pinst(Pb, mu))))
        return None

    m = meet(F, B, True)
    if m is not None: return ('PROVED', m)

    def expand(frontier, seen, allnodes, forward):
        nxt = []
        for (t, P) in frontier:
            if _nrw_time.time() > deadline: return nxt
            for (lo, ro, flip) in rules:
                ctr[0] += 1; suf = '#%d' % ctr[0]
                l = nrw_rename(lo, suf); r = nrw_rename(ro, suf)
                for pp, sub in nrw_positions(t):
                    mu = nrw_unify(l, sub, {})
                    if mu is None: continue
                    new = nrw_app(nrw_repl(t, pp, r), mu)
                    if nrw_size(new) > max_size: continue
                    k = nrw_key(new)
                    if k in seen: continue
                    seen.add(k)
                    tmu = nrw_app(t, mu)
                    theta = tuple(nrw_app(('v', v + suf), mu) for v in _NRW["vars"])
                    base = ('H', theta)
                    inst = ('SYM', base) if flip else base
                    step = nrw_cong_wrap(tmu, pp, inst)
                    # forward proof P: gl=t  -> gl=new ; backward proof P: gr=t -> gr=new
                    newP = ('TRANS', nrw_pinst(P, mu), step)
                    nxt.append((new, newP))
        allnodes.extend(nxt)
        return nxt

    while F or B:
        if _nrw_time.time() > deadline: return ('TIMEOUT', None)
        if len(Fseen) + len(Bseen) > max_nodes: return ('CAP', None)
        # Expand the smaller NON-EMPTY frontier. Guarding on emptiness is
        # essential: once one side is exhausted, blindly comparing sizes would
        # keep "expanding" the empty frontier forever and burn the whole budget.
        expand_forward = bool(F) and (not B or len(F) <= len(B))
        if expand_forward:
            newF = expand(F, Fseen, Fall, True); F = newF
            m = meet(newF, Ball, True)
        else:
            newB = expand(B, Bseen, Ball, False); B = newB
            m = meet(newB, Fall, False)
        if m is not None: return ('PROVED', m)
    return ('EXHAUSTED', None)

def _nrw_emit(eq2_text, gv, Pf):
    """Self-check a candidate proof; return Lean code or None."""
    try:
        lhs, rhs = nrw_ptype(Pf)
    except Exception:
        # AssertionError (type mismatch) or RecursionError/anything else on a
        # pathological proof tree — treat as "no usable proof", never crash.
        trace("[narrow] proof self-check (ptype) failed; skipping")
        return None
    gl = nrw_parse(eq2_text.split('=', 1)[0], True)
    gr = nrw_parse(eq2_text.split('=', 1)[1], True)
    if (lhs, rhs) != (gl, gr):
        trace("[narrow] proof proves wrong equation; skipping")
        return None
    fv = set(); nrw_proof_freevars(Pf, fv)
    if fv:
        trace("[narrow] proof still has free vars; skipping")
        return None
    body = "intro " + " ".join(gv) + "\nexact " + nrw_render(Pf)
    code = make_true_code(body)
    if len(code) > 90000:
        trace(f"[narrow] proof too large ({len(code)} chars); skipping")
        return None
    return code


# Iterative-deepening size schedule. Most real proofs are found at a small size
# almost instantly; the right size is the sweet spot (too-small can't fit the
# proof, too-large explodes the branching). So sweep small first with short
# slices, then deepen on the mid/large sizes with the remaining budget.
NRW_SWEEP_SIZES = (14, 16, 18, 20, 22, 24, 26, 28, 31, 34, 38, 44)
NRW_DEEP_SIZES = (22, 26, 30, 36, 44, 52)


def try_narrowing(problem, eq1_text, eq2_text, time_budget=120.0, quick_slice=4.0,
                  deep=False):
    """TRUE-side stage: goal-directed bidirectional narrowing with proof
    extraction. Self-checks the proof type and grounds out free vars, then lets
    the Lean judge make the final ruling (a malformed proof can never be
    accepted). Iterative-deepening on the term-size cap finds cheap proofs fast;
    `deep=True` skips the small-size sweep (already tried by the quick pass) and
    spends the whole budget on the larger size caps."""
    gv = goal_vars(eq2_text)
    if not gv:
        return False
    if "h" in gv:
        # A goal variable literally named `h` would shadow the hypothesis `h`
        # in the emitted Lean; bail rather than emit a wrong-binding proof.
        return False
    start = _nrw_time.time()

    def left():
        return time_budget - (_nrw_time.time() - start)

    def attempt(ms, tb):
        if tb < 0.5:
            return False
        # One try/except around the whole attempt: search, self-check, render,
        # and judge. Any failure (incl. RecursionError on a deep proof tree)
        # just means "this size found nothing", never a solver crash.
        try:
            status, Pf = nrw_prove_bidir(eq1_text, eq2_text, max_size=ms, tb=tb)
            if status != 'PROVED' or Pf is None:
                return False
            code = _nrw_emit(eq2_text, gv, Pf)
            if code is None:
                return False
            trace(f"[narrow] PROVED ms={ms} (codelen={len(code)})")
            return call_judge("true", code).get("status") == "accepted"
        except Exception as e:
            trace(f"[narrow] error ms={ms}: {e!r}")
            return False

    if deep:
        per = max(8.0, time_budget / max(1, len(NRW_DEEP_SIZES)))
        for ms in NRW_DEEP_SIZES:
            if left() < 1.0:
                return False
            if attempt(ms, min(left(), per)):
                return True
        return False

    # Quick pass: small-first sweep, then a short deepen with whatever is left.
    for ms in NRW_SWEEP_SIZES:
        if left() < 1.0:
            return False
        if attempt(ms, min(left(), quick_slice)):
            return True
    deep_slice = max(8.0, left() / max(1, len(NRW_DEEP_SIZES)))
    for ms in NRW_DEEP_SIZES:
        if left() < 1.0:
            return False
        if attempt(ms, min(left(), deep_slice)):
            return True
    return False


# ── LLM-guided waypoint narrowing (neuro-symbolic TRUE-side stage) ────
# The deterministic narrowing prover is complete in the limit but its search
# explodes on the hardest implications (the long, non-obvious derivations).
# This is exactly where an LLM helps: it proposes a sequence of INTERMEDIATE
# terms ("waypoints") that the proof passes through. The solver then proves each
# short segment between consecutive waypoints with the *verified* narrowing
# engine and concatenates the segment proofs. The LLM is never trusted: a wrong
# waypoint just makes a segment unprovable (we skip it or fail), and the final
# proof is checked by nrw_ptype AND the Lean judge. So this can only add solves,
# never a wrong answer — the model's creativity, the prover's rigor.


NRW_SEG_SIZES = (16, 20, 24, 28, 34)


def nrw_bridge_chain(chain, gv, seg_tb=12.0, deadline=None, max_skip=2):
    """Prove gl=gr by bridging consecutive waypoints in `chain` (a list of ground
    terms starting at gl, ending at gr) with narrowing. Each segment gets its own
    iterative-deepening search, so a single well-placed waypoint can split an
    otherwise-unreachable gl->gr into two reachable halves. A bad waypoint can be
    skipped (up to `max_skip` in a row). Returns a composed proof term or None."""
    filler_pool = set(gv)
    proofs = []
    i = 0
    n = len(chain)
    while i < n - 1:
        progressed = False
        # Prefer the nearest next waypoint; on failure, skip ahead (drop a bad one).
        for j in range(i + 1, min(i + 1 + max_skip + 1, n)):
            if deadline is not None and _nrw_time.time() > deadline:
                return None
            for ms in NRW_SEG_SIZES:
                tb = seg_tb
                if deadline is not None:
                    tb = min(tb, max(0.5, deadline - _nrw_time.time()))
                if tb < 0.5:
                    return None
                try:
                    st, P = nrw_prove_terms(chain[i], chain[j], max_size=ms,
                                            tb=tb, filler_pool=filler_pool)
                except Exception:
                    st, P = ('ERR', None)
                if st == 'PROVED' and P is not None:
                    proofs.append(P); i = j; progressed = True
                    break
            if progressed:
                break
        if not progressed:
            return None
    if not proofs:
        return None
    full = proofs[0]
    for P in proofs[1:]:
        full = ('TRANS', full, P)
    return full


def _nrw_parse_goal_term(s, gv):
    """Parse an LLM-proposed term string as a ground term over the goal vars.
    Returns the term iff every variable in it is a goal variable, else None."""
    if not isinstance(s, str):
        return None
    s = s.replace("*", "◇").strip()
    if not s:
        return None
    try:
        t = nrw_parse(s, True)
    except Exception:
        return None
    sk = set(); nrw_skolems(t, sk)
    if sk and sk <= set(gv):
        return t
    return None


def try_llm_waypoints(problem, eq1_text, eq2_text, start_time, budget_seconds,
                      seg_tb=12.0, max_rounds=3, min_seconds=None):
    """Ask the LLM for proof waypoints, then bridge them with verified narrowing.
    Returns True iff a composed, Lean-accepted proof is produced."""
    gv = goal_vars(eq2_text)
    if not gv or "h" in gv:
        return False
    gate = MIN_SECONDS_FOR_LLM if min_seconds is None else min_seconds
    nrw_setup(eq1_text)
    gl = nrw_parse(eq2_text.split('=', 1)[0], True)
    gr = nrw_parse(eq2_text.split('=', 1)[1], True)

    analysis = (
        "Propose proof WAYPOINTS for an equational-logic proof that the hypothesis "
        "Eq1 implies the goal Eq2 over all magmas. Do NOT write Lean. Give an ordered "
        "list of intermediate magma terms the proof passes through, from the goal's "
        "LEFT side to its RIGHT side, where each consecutive pair differs by only a "
        "few applications of the hypothesis (rewriting a subterm using Eq1 in either "
        "direction). Use ONLY the goal's variables and the operator ◇. Prefer 6-16 "
        "small waypoints. The first waypoint should be reachable from the goal LHS in "
        "one or two hypothesis steps, and the last reachable to the goal RHS likewise."
    )

    seen_waypoint_sets = set()
    for rnd in range(max_rounds):
        elapsed = time.monotonic() - start_time
        if budget_seconds - elapsed < gate:
            trace("[waypoints] not enough time left for LLM")
            return False
        try:
            result = call_llm({"mode": "waypoints", "analysis": analysis,
                               "attempt": f"wp{rnd}"})
        except Exception as e:
            trace(f"[waypoints] llm call error: {e!r}")
            return False
        if "error" in result:
            trace(f"[waypoints] llm error: {result.get('error')}")
            return False
        ans = extract_json(result.get("response", ""))
        if not ans:
            trace("[waypoints] unparseable response")
            continue
        raw = ans.get("waypoints") or ans.get("path") or []
        wps = [t for t in (_nrw_parse_goal_term(s, gv) for s in raw) if t is not None]
        key = tuple(nrw_key(t) for t in wps)
        if key in seen_waypoint_sets:
            continue
        seen_waypoint_sets.add(key)
        chain = [gl] + wps + [gr]
        trace(f"[waypoints] round={rnd} parsed {len(wps)} waypoints; bridging {len(chain)} nodes")
        # generous segment deadline scaled to remaining budget
        seg_deadline = time.monotonic() + min(300.0, budget_seconds - (time.monotonic() - start_time) - 30.0)
        proof = nrw_bridge_chain(chain, gv, seg_tb=seg_tb,
                                 deadline=seg_deadline, max_skip=2)
        if proof is None:
            trace("[waypoints] could not bridge chain")
            continue
        code = _nrw_emit(eq2_text, gv, proof)
        if code is None:
            continue
        trace(f"[waypoints] bridged proof codelen={len(code)}")
        if call_judge("true", code).get("status") == "accepted":
            return True
    return False


def try_llm_direct_proof(problem, eq1_text, eq2_text, start_time, budget_seconds,
                         singleton_hint, max_attempts=3, min_seconds=90.0):
    """Ask the LLM to write a Lean proof directly (mode=proof), with a judge
    feedback loop (the proxy auto-appends prior attempts/errors to the prompt).
    Every candidate is judged, so a wrong proof is simply rejected. Best for the
    short-but-structured TRUE residual the deterministic engines miss; yield
    scales with model strength."""
    gv = goal_vars(eq2_text)
    analysis_parts = []
    if singleton_hint:
        analysis_parts.append(
            "Small-model search suggests Eq1 may FORCE the magma to a single element "
            "(no non-trivial model on Fin 2/3). If so, prove `have key : ∀ (a b : G), "
            "a = b := by ...` via h-instantiations, then `exact key <goal_lhs> <goal_rhs>`."
        )
    else:
        analysis_parts.append(
            "Deterministic search found no finite counterexample and no singleton "
            "collapse. Treat this as TRUE: build a calc/have chain from the goal LHS to "
            "the goal RHS where every step is an instance of h (optionally inside congrArg)."
        )
    analysis = " ".join(analysis_parts)
    seen = set()
    for attempt in range(max_attempts):
        elapsed = time.monotonic() - start_time
        if budget_seconds - elapsed < min_seconds:
            trace("[llm-proof] not enough time left")
            return False
        try:
            result = call_llm({"mode": "proof", "analysis": analysis,
                               "attempt": str(attempt)})
        except Exception as e:
            trace(f"[llm-proof] call error: {e!r}")
            return False
        if "error" in result:
            trace(f"[llm-proof] error: {result.get('error')}")
            return False
        answer = extract_json(result.get("response", ""))
        if not answer:
            trace("[llm-proof] unparseable response")
            continue
        verdict = answer.get("verdict")
        if verdict == "true":
            proof = clean_proof(answer.get("proof", ""))
            if not proof or proof in seen or not intro_arity_ok(proof, eq2_text):
                continue
            seen.add(proof)
            code = make_true_code(proof)
        elif verdict == "false":
            if singleton_hint:
                continue  # singleton hint implies TRUE; ignore a false claim
            tbl = answer.get("counterexample_table")
            if not tbl or not isinstance(tbl, list):
                continue
            code = make_false_code(len(tbl), tbl)
        else:
            continue
        try:
            res = call_judge(verdict, code)
        except Exception:
            return False
        trace(f"[llm-proof] attempt={attempt} status={res.get('status')}")
        if res.get("status") == "accepted":
            return True
    return False


# ── Main ─────────────────────────────────────────────────────────


def main():
    start_time = time.monotonic()
    startup = read_message()
    problem = startup["problem"]
    budget_info = startup.get("budget", {})
    budget_seconds = float(
        budget_info.get("timeout_seconds", DEFAULT_BUDGET_SECONDS)
    )
    eq1 = problem["equation1"].replace("*", "\u25c7")
    eq2 = problem["equation2"].replace("*", "\u25c7")
    problem["equation1"], problem["equation2"] = eq1, eq2

    # Budget-aware stage allocation. The reference per-problem budget is 3600s,
    # but the solver must also behave under a tight timeout (small-timeout runs,
    # marathon compression): scale the heavy stages to the granted wall budget so
    # no single stage overruns the deadline and the LLM still gets a fair slice.
    _B = budget_seconds
    mf2_budget = min(MF2_PORTFOLIO_BUDGET, max(15.0, _B * 0.30))
    sat_budget = min(SAT_FINDER_BUDGET, max(8.0, _B * 0.15))
    comp_sing_budget = min(25.0, max(4.0, _B * 0.08))
    comp_ns_budget = min(20.0, max(4.0, _B * 0.06))
    nrw_quick_budget = min(40.0, max(6.0, _B * 0.12))
    # LLM gate: only start an LLM stage if at least this much wall remains. Kept
    # low so fast models (e.g. Gemma) reliably fire; the proxy independently
    # bounds each call by the remaining budget, so a low gate is safe.
    llm_gate = min(MIN_SECONDS_FOR_LLM, max(12.0, _B * 0.15))
    trace(f"[budget] wall={_B:.0f}s mf2={mf2_budget:.0f} sat={sat_budget:.0f} "
          f"nrwQ={nrw_quick_budget:.0f} llm_gate={llm_gate:.0f}")

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

    # Stage 1.3: symbolic affine models (a*x + b*y + c mod n).
    # Microseconds per (n,a,b) cell; reaches moduli far past the search
    # finders (e.g. Z13 with op=7x+7y). Runs early because it is cheap.
    if "try_affine_model" in globals():
        trace("[stage] affine model search")
        if try_affine_model(eq1, eq2):
            trace("[accepted] affine model")
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

    # Stage 2.7: deterministic ordered-completion singleton proof.
    # Decision procedure for the hard-singleton class; runs before the LLM
    # strategist, which historically yielded zero successes here.
    if singleton and "try_completion_singleton" in globals():
        trace("[stage] completion singleton")
        if try_completion_singleton(problem, eq1, eq2, time_budget=comp_sing_budget):
            trace("[accepted] completion singleton")
            return
    elif singleton:
        trace("[skip] completion singleton: function missing")

    # Stage 2.8: deterministic non-singleton ordered-completion proof (Phase 2).
    # Proves goal_lhs = goal_rhs as a consequence of Eq1 without singleton
    # collapse. Runs before the LLM fallback; captures true non-singleton
    # cases the LLM proof path historically could not.
    if "try_completion_nonsingleton" in globals():
        trace("[stage] completion non-singleton")
        if try_completion_nonsingleton(problem, eq1, eq2, time_budget=comp_ns_budget):
            trace("[accepted] completion non-singleton")
            return

    # Stage 2.84: fast false-model probe. Narrowing (next stage) can spend its
    # whole budget on a FALSE case (it never meets-in-the-middle), so first run a
    # cheap backtracking finder on small carriers to catch the easy Fin 4-5
    # counterexamples that the structured search missed. Bounded to a few seconds.
    if "mf_find_false_model" in globals() and not singleton:
        trace("[stage] fast false-model probe")
        try:
            out = mf_find_false_model(eq1, eq2, sizes=(4, 5), per_size=1.8)
        except Exception:
            out = None
        if out is not None:
            n, table = out
            v1, l1, r1 = parse_equation(eq1)
            v2, l2, r2 = parse_equation(eq2)
            op = lambda a, b, t=table: t[a][b]
            if equation_holds(v1, l1, r1, n, op) and not equation_holds(v2, l2, r2, n, op):
                if call_judge("false", make_false_code(n, table)).get("status") == "accepted":
                    trace("[accepted] fast false-model probe")
                    return

    # Stage 2.85: goal-directed bidirectional narrowing (TRUE side) — quick pass.
    # The completion stages above only reduce the goal to a normal form; this
    # prover also EXPANDS terms via the hypothesis (superposition), which closes
    # the hard TRUE residual completion misses. Short budget here so the bulk of
    # provable TRUE cases are solved before the costly false-model search; the
    # deep pass (Stage 2.97) handles whatever this leaves.
    if "try_narrowing" in globals():
        trace("[stage] narrowing (quick)")
        if try_narrowing(problem, eq1, eq2, time_budget=nrw_quick_budget, quick_slice=2.5):
            trace("[accepted] narrowing (quick)")
            return

    # Stage 2.9: backtracking finite-model finder (false side).
    # Catches generic Fin 4-6 counterexamples the structured search misses.
    # Placed after the true-proof stages so true cases are mostly solved
    # first; runs before the costly LLM fallback.
    if "try_model_finder" in globals():
        trace("[stage] backtracking model finder")
        if try_model_finder(eq1, eq2, budget=mf2_budget):
            trace("[accepted] backtracking model finder")
            return

    # Stage 2.95: SAT-based complete false-model finder. Catches the hard
    # general (non-quasigroup) Fin 5-7 counterexamples the heuristic portfolio
    # misses. Gated to non-singleton cases (a singleton hint means TRUE, so no
    # counterexample exists) and bounded so it can't run away on a true case.
    if not singleton and "sat_find_model" in globals():
        trace("[stage] SAT false-model finder")
        if try_sat_finder(eq1, eq2, sizes=(5, 6, 7), budget=sat_budget):
            trace("[accepted] SAT false-model finder")
            return

    # Stage 2.97: goal-directed narrowing (TRUE side) — deep pass. Runs after the
    # false-model finders have ruled out a counterexample, so the remaining
    # residual is almost entirely TRUE. Spends a large slice of the wall budget
    # on bigger term-size caps to crack the hardest implications. Every proof is
    # self-checked and Lean-verified, so this can only add solves.
    if "try_narrowing" in globals():
        elapsed = time.monotonic() - start_time
        # Leave a clear margin above the LLM gate so the LLM stage reliably gets
        # to fire as a fallback (deep narrowing must not eat the whole remainder).
        deep_budget = min(max(0.0, budget_seconds - elapsed - (llm_gate + 15.0)), 900.0)
        if deep_budget >= 20.0:
            trace(f"[stage] narrowing (deep, {deep_budget:.0f}s)")
            if try_narrowing(problem, eq1, eq2, time_budget=deep_budget, deep=True):
                trace("[accepted] narrowing (deep)")
                return

    # Stage 3.0: LLM-guided waypoint narrowing (neuro-symbolic). The LLM proposes
    # intermediate terms; the verified narrowing engine bridges each short segment
    # and Lean checks the composed proof. This targets the hardest TRUE residual
    # that pure search can't reach, while staying sound (LLM output is only a
    # search hint — a wrong waypoint just fails to bridge). Runs for both singleton
    # and non-singleton cases.
    if "try_llm_waypoints" in globals():
        trace("[stage] LLM waypoint narrowing")
        if try_llm_waypoints(problem, eq1, eq2, start_time=start_time,
                             budget_seconds=budget_seconds, min_seconds=llm_gate):
            trace("[accepted] LLM waypoint narrowing")
            return

    # Stage 3.1: direct LLM proof with a judge feedback loop (sound — every
    # candidate is Lean-checked). Complements the waypoint stage for the
    # short-but-structured residual.
    if "try_llm_direct_proof" in globals():
        trace("[stage] LLM direct proof")
        if try_llm_direct_proof(problem, eq1, eq2, start_time=start_time,
                                budget_seconds=budget_seconds,
                                singleton_hint=singleton, min_seconds=llm_gate):
            trace("[accepted] LLM direct proof")
            return

    # Stage 3: LLM fallback.
    # Hard singleton cases are currently low-yield: the model often returns
    # false, wrong intros, or invalid h1.trans h2.symm proofs. Prefer failing
    # fast unless we later add a shape-specific prompt.
    if singleton:
        trace("[stage] LLM strategist singleton graph")
        if try_llm_strategy_singleton_graph(
            problem,
            eq1,
            eq2,
            start_time=start_time,
            budget_seconds=budget_seconds,
        ):
            trace("[accepted] LLM strategist singleton graph")
            return

        trace("[stop] hard singleton reached fallback; strategist failed")
        return

    # Fast-fail gate: the singleton path has already returned above, so only the
    # non-singleton residual reaches here. The LLM proof fallback does not help it,
    # so stop rather than burn a costly call.
    if not ENABLE_NS_LLM_FALLBACK:
        trace("[stop] non-singleton residual: skipping low-yield LLM fallback")
        return

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
    # Non-singleton hard residual is now handled by Stage 2.8 (completion);
    # the LLM proof path yielded ~1/674 at huge cost, so fail fast here.
    MAX_LLM_ATTEMPTS = 2 if singleton else 1
    consecutive_garbage = 0

    for attempt in range(MAX_LLM_ATTEMPTS):
        elapsed = time.monotonic() - start_time
        remaining = budget_seconds - elapsed
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
