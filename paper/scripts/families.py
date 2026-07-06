#!/usr/bin/env python3
"""A vocabulary of structurally-distinct NON-LINEAR magma families.

Motivation. The proposer's dominant failure on the open/capability sets was
"NO parameter made EQ1 hold": o3 kept emitting affine-with-a-twist families
(permuted_affine, quadratic_affine_mod, perm_shift) that structurally cannot
thread the rigid EQ1 identities. The one real win (order5big_0584) came from a
categorically different structure (bit/coordinate decomposition). So the lever
is VOCABULARY -- a library of genuinely non-affine families spanning distinct
algebraic ideas (projection/translation, quandle/conjugation, coordinate
decomposition, piecewise, semilattice, Steiner-idempotent, central groupoid,
near-ring twist).

Each entry is a VALID `structured_finite` proposal (op_code + params +
candidate_n), so this module does double duty:

  1. Few-shot vocabulary for the proposer prompt (render_fewshot) -- concrete,
     schema-correct templates o3 can instantiate or riff on, instead of
     defaulting to affine variants.
  2. A ZERO-TOKEN deterministic non-linear stage (scan_families): run every
     family through structured_search over a target set; whatever it cracks
     extends the frontier for free, sharpens the A/B, and shrinks the paid o3
     target set. No API involved.

None of these is of the form a*x + b*y (+c): linear ops are already exhausted
by the affine/algebraic-linear stages and proven impossible on the non-linear-
required pairs, so a purely linear family here would be redundant. Every op_code
uses only `math`, x, y, n, and the parameter tuple P (matching structured_search,
which execs op_code with ns={"math": math}).
"""
from __future__ import annotations

# Each family: name, idea (why it's non-linear and what law-shape it fits),
# op_code (single-line def op(x,y,n,P)), params (structured_search spec),
# candidate_n. Keep perm-families' n small (a perm domain is n!).
FAMILIES = [
    {
        "name": "perm_right_translation",
        "idea": "Right translation twisted by an arbitrary permutation: op(x,y)=P[x]+y "
                "with P a non-linear relabelling of x. Non-affine whenever P is not "
                "an arithmetic progression; fits laws needing invertibility in y.",
        "op_code": "def op(x, y, n, P): return (P[0][x] + y) % n",
        "params": [{"perm": True}],
        "candidate_n": [4, 5, 6, 7],
    },
    {
        "name": "perm_projection_idempotent",
        "idea": "Idempotent off-diagonal permutation: op(x,x)=x, else op(x,y)=P[y]. "
                "Guarantees idempotence (op(a,a)=a) which many x=<term> laws force, "
                "while staying non-linear off the diagonal.",
        "op_code": "def op(x, y, n, P): return x if x == y else P[0][y]",
        "params": [{"perm": True}],
        "candidate_n": [4, 5, 6, 7],
    },
    {
        "name": "twisted_dihedral_quandle",
        "idea": "Core/dihedral quandle 2y-x relabelled by a permutation: "
                "op(x,y)=P[(2y-x) mod n]. Self-distributive and idempotent-flavoured "
                "but non-linear because of P; a classic non-associative structure.",
        "op_code": "def op(x, y, n, P): return P[0][(2 * y - x) % n]",
        "params": [{"perm": True}],
        "candidate_n": [4, 5, 6, 7],
    },
    {
        "name": "coordinate_decomposition",
        "idea": "Generalises the order5big_0584 win: split the index base-d and "
                "recombine coordinates crosswise, op(x,y)=(x//d)+d*(y%d). Genuinely "
                "non-linear (integer div/mod), fits product-structure laws.",
        "op_code": "def op(x, y, n, P): return ((x // P[0]) + P[0] * (y % P[0])) % n",
        "params": [{"int": [2, "n"]}],
        "candidate_n": [4, 6, 8, 9],
    },
    {
        "name": "piecewise_threshold_projection",
        "idea": "Piecewise left/right projection on a threshold: op(x,y)=x if y<t "
                "else y. Conditional => non-linear; naturally satisfies x=<term> laws "
                "where the inner term stays below threshold.",
        "op_code": "def op(x, y, n, P): return x if y < P[0] else y",
        "params": [{"int": [1, "n"]}],
        "candidate_n": [4, 5, 6, 7],
    },
    {
        "name": "steiner_idempotent_commutative",
        "idea": "Steiner-quasigroup style: idempotent+commutative, op(x,x)=x and "
                "op(x,y)=(c-x-y) mod n off-diagonal. Commutative idempotent quasigroup, "
                "non-linear via the diagonal special-case.",
        "op_code": "def op(x, y, n, P): return x if x == y else (P[0] - x - y) % n",
        "params": [{"int": [0, "n"]}],
        "candidate_n": [5, 7, 9],
    },
    {
        "name": "permuted_semilattice",
        "idea": "Semilattice (assoc+comm+idempotent) under a permuted total order: "
                "op(x,y)=argmax by P-rank. Satisfies strong absorption laws; non-linear "
                "because the order is an arbitrary permutation.",
        "op_code": "def op(x, y, n, P): return x if P[0].index(x) >= P[0].index(y) else y",
        "params": [{"perm": True}],
        "candidate_n": [4, 5, 6, 7],
    },
    {
        "name": "central_groupoid_pairs",
        "idea": "Central groupoid on d*d pairs: (a,b)*(c,d)=(b,c), encoded on Fin(d^2) "
                "as op(x,y)=(x mod d)*d+(y//d). Satisfies (x*y)*(y*z)=y; strongly "
                "non-associative and non-linear.",
        "op_code": "def op(x, y, n, P): return ((x % P[0]) * P[0] + (y // P[0])) % n",
        "params": [{"int": [2, "n"]}],
        "candidate_n": [4, 9, 16],
    },
    {
        "name": "nearring_perm_multiplier",
        "idea": "Zero-symmetric near-ring twist: op(x,y)=P[x]+P[y] style additive core "
                "with a non-linear multiplier P applied to both, then combined. "
                "Non-distributive over +, so non-linear.",
        "op_code": "def op(x, y, n, P): return (P[0][x] + P[0][y] + x) % n",
        "params": [{"perm": True}],
        "candidate_n": [4, 5, 6, 7],
    },
    {
        "name": "conjugation_shift",
        "idea": "Conjugation-like: op(x,y)=P[(P.index(y)+P.index(x)+1) mod n]. Mimics "
                "y^{-1}xy-style non-commutative combination; non-linear and "
                "non-associative for generic P.",
        "op_code": "def op(x, y, n, P): return P[0][(P[0].index(x) + P[0].index(y) + 1) % n]",
        "params": [{"perm": True}],
        "candidate_n": [4, 5, 6],
    },
]


def render_fewshot(max_families=None):
    """Render the library as a few-shot block for the proposer prompt.

    Shows each family as a schema-correct structured_finite skeleton so the model
    riffs on distinct algebraic structures instead of affine variants."""
    fams = FAMILIES if max_families is None else FAMILIES[:max_families]
    lines = [
        "STRUCTURED NON-LINEAR VOCABULARY (few-shot). Below are known families that "
        "span DISTINCT algebraic structures, each already in the structured_finite "
        "schema. They are STARTING POINTS: instantiate one, adapt it to EQ1/EQ2's "
        "shape, or invent a genuinely new NON-LINEAR structure. Do NOT return an "
        "a*x+b*y variant -- linear forms are proven impossible on these pairs.",
        "",
    ]
    for i, f in enumerate(FAMILIES if max_families is None else fams, 1):
        lines.append(f"{i}. {f['name']} -- {f['idea']}")
        lines.append(f'   op_code: {f["op_code"]}')
        lines.append(f'   params:  {f["params"]}   candidate_n: {f["candidate_n"]}')
    return "\n".join(lines)


def scan_families(solver, eq1, eq2, budget=300_000, deadline=None, families=None):
    """Zero-token deterministic stage: try every library family via
    structured_search. Returns (hit, info) where hit=(name, n, table, P) or None,
    and info lists the per-family diagnosis so a total miss is still legible."""
    import structured_search
    fams = families if families is not None else FAMILIES
    diagnoses = []
    for f in fams:
        res = structured_search.search_structured(
            solver, eq1, eq2, f["op_code"], f["params"], f["candidate_n"],
            budget=budget, deadline=deadline)
        # Defensive: structured_search must return (hit, reason). A bare None or
        # bad shape means a broken/stale dependency (e.g. the sandbox mount-
        # truncation caveat) -- record it rather than crash the whole scan.
        if not (isinstance(res, tuple) and len(res) == 2):
            diagnoses.append((f["name"], f"search_structured returned {res!r} "
                              "(expected (hit, reason)); dependency may be truncated/stale"))
            continue
        out, reason = res
        if out is not None:
            n_hit, table, P = out
            return (f["name"], n_hit, table, P), diagnoses
        diagnoses.append((f["name"], reason))
    return None, diagnoses


def _main():
    import argparse, json, sys, time
    ap = argparse.ArgumentParser(description="Zero-token non-linear family scan over a target set.")
    ap.add_argument("--pairs", required=True, help="{id:[eq1,eq2]} json (e.g. the step-0 miss-set)")
    ap.add_argument("--solver-dir", required=True)
    ap.add_argument("--budget", type=int, default=300_000)
    ap.add_argument("--per-pair-secs", type=float, default=0.0,
                    help="wall-clock deadline per pair (0 = none)")
    ap.add_argument("--out", default=None, help="optional jsonl of results")
    ap.add_argument("--print-fewshot", action="store_true",
                    help="just print the few-shot prompt block and exit")
    args = ap.parse_args()

    if args.print_fewshot:
        print(render_fewshot())
        return

    sys.path.insert(0, args.solver_dir)
    import solver
    solver.trace = lambda *a, **k: None

    pairs = json.load(open(args.pairs))
    rows, n_solved = [], 0
    print(f"scanning {len(FAMILIES)} families over {len(pairs)} pairs (zero tokens)")
    print(f"{'pair':<20} {'solved_by_family':<28} {'n'}")
    print("-" * 60)
    for pid, (eq1, eq2) in pairs.items():
        deadline = time.time() + args.per_pair_secs if args.per_pair_secs else None
        hit, diagnoses = scan_families(solver, eq1, eq2, budget=args.budget, deadline=deadline)
        if hit:
            name, n_hit, table, P = hit
            n_solved += 1
            rows.append({"id": pid, "solved_by_family": name, "n": n_hit,
                         "params": repr(P), "table": table})
            print(f"{pid:<20} {name:<28} {n_hit}")
        else:
            rows.append({"id": pid, "solved_by_family": None,
                         "diagnoses": {nm: rs for nm, rs in diagnoses}})
            print(f"{pid:<20} {'-- (no family)':<28} -")
    print("-" * 60)
    print(f"family portfolio solved {n_solved}/{len(pairs)} with ZERO tokens")
    if args.out:
        with open(args.out, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    _main()
