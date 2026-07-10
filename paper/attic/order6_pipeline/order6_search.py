#!/usr/bin/env python3
"""Order-6 Austin-law search: generate order-6 single laws (x = T, 6 ops / 7 leaves),
screen for "no nontrivial finite model" (the Austin-candidate signal), output
candidates for the greedy easy/hard split.

ETP classified order-5 (57,882 laws) and left 96 open Austin laws; the single-law
"x = T" structure is where our greedy builder is validated competent (the LHS x is
an anchor). Order-6 extends that tractable family — same structure, larger pool —
which is the clean volume source (pairs lack the anchor and can't be auto-graded).
ETP did NOT do the order-6 finite classification, so we do it here.

Pipeline (cheap -> expensive; each stage drops laws with a nontrivial finite model):
  0. generate     unique order-6 x=T laws (deterministic; shardable by --shard)
  1. cheap screen brute-force n=2 then n=3 nontrivial models (pure Python) -> drop
  2. fast finder  optional: solver mf2/SAT up to Fin~11 (reuse harvest infra) -> drop
  3. fmb          Vampire finite-model-builder, LONG timeout (models can be size
                  20+ at order 6, cf. order-5 minima up to 26) -> drop if a model
                  is FOUND; keep as CANDIDATE only if fmb finds none within budget.
Survivors = Austin candidates (no finite model up to the fmb budget). Then run the
validated greedy builder (separate step) to split easy (auto-constructible Austin)
vs hard (LLM targets), and — for rigor — the pigeonhole/cancellativity proof to
UPGRADE "no model found" into "provably no finite model".

IMPORTANT: fmb never proves "no finite model" — it searches sizes until timeout.
A CANDIDATE here means "no finite model up to the fmb budget", a heuristic to be
confirmed by proof. Correctly distinguishes MODEL_FOUND / NO_MODEL_IN_BUDGET
(Vampire "Termination reason: Time limit" or wall timeout) — do not conflate them.

Usage:
  # cheap screen only (fast, no Vampire) to estimate yield / build the pool
  python paper/scripts/order6_search.py --n 20000 --seed 20260706 --cheap-only \
      --out paper/results/order6_cheap.jsonl --shard 0/8
  # full screen with fmb (cluster; long per-law)
  python paper/scripts/order6_search.py --n 20000 --seed 20260706 \
      --fmb-timeout 120 --vampire paper/bin/vampire \
      --out paper/results/order6_candidates.jsonl --shard 0/8
"""
from __future__ import annotations
import argparse, itertools, json, os, random, subprocess, sys, tempfile, time

VARS = ["x", "y", "z", "w"]


# ---- generation ----------------------------------------------------------
def rand_tree(rng, n):
    if n == 1:
        return ("var", rng.choice(VARS))
    k = rng.randint(1, n - 1)
    return ("op", rand_tree(rng, k), rand_tree(rng, n - k))


def has_var(t, v):
    return t[1] == v if t[0] == "var" else (has_var(t[1], v) or has_var(t[2], v))


def canon(t):
    order = {}
    def w(n):
        if n[0] == "var":
            if n[1] not in order:
                order[n[1]] = chr(97 + len(order))
            return order[n[1]]
        return "(" + w(n[1]) + "*" + w(n[2]) + ")"
    return w(t)


def to_str(t):
    return t[1] if t[0] == "var" else "(" + to_str(t[1]) + " ◇ " + to_str(t[2]) + ")"


def to_tptp(t):
    return t[1].upper() if t[0] == "var" else f"f({to_tptp(t[1])},{to_tptp(t[2])})"


def generate(rng, count, leaves=7):
    laws, seen = [], set()
    tries = 0
    while len(laws) < count and tries < count * 40:
        tries += 1
        T = rand_tree(rng, leaves)
        if not has_var(T, "x"):
            continue
        key = canon(("op", ("var", "x"), T))  # canonical form of the whole law x=T
        if key in seen:
            continue
        seen.add(key)
        laws.append(T)
    return laws


# ---- cheap finite-model screen (brute force small n) ---------------------
def _ev(t, op, env):
    if t[0] == "var":
        return env[t[1]]
    return op(_ev(t[1], op, env), _ev(t[2], op, env))


def has_nontrivial_model(T, n):
    """Does some n-element magma satisfy x=T for all assignments? (n>=2 => nontrivial)"""
    vs = sorted(set(v for v in VARS if has_var(T, v)) | {"x"})
    assigns = list(itertools.product(range(n), repeat=len(vs)))
    for tab in itertools.product(range(n), repeat=n * n):
        op = (lambda tt, nn: (lambda a, b: tt[a * nn + b]))(tab, n)
        if all(_ev(T, op, dict(zip(vs, asn))) == dict(zip(vs, asn))["x"] for asn in assigns):
            return True
    return False


# ---- Vampire fmb (correct MODEL vs NO_MODEL_IN_BUDGET detection) ----------
def fmb(T, timeout, vbin):
    vs = sorted(set(v.upper() for v in VARS if has_var(T, v)) | {"X"})
    body = (f"fof(law,axiom,![{','.join(vs)}]:(X={to_tptp(T)})).\n"
            "fof(nontrivial,axiom,?[U,V]:U!=V).\n")
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "p.p")
        open(p, "w").write(body)
        try:
            s = subprocess.run([vbin, "-sa", "fmb", "-t", f"{timeout}s", p],
                               capture_output=True, text=True, timeout=timeout + 5).stdout
        except subprocess.TimeoutExpired:
            return "NO_MODEL_IN_BUDGET", None
    if "Finite Model Found" in s or "SZS status Satisfiable" in s:
        return "MODEL_FOUND", s.count(":$i")           # model order (approx)
    return "NO_MODEL_IN_BUDGET", None                  # incl. Vampire "Time limit"


# ---- stage 2: fast finite-model finder (reuse the solver's mf2/SAT) ------
# A nontrivial finite model of law L == a magma satisfying L that BREAKS "x = y"
# (breaking the all-collapse law just means the carrier has >=2 elements). So the
# solver's false-side finders (satisfy eq1, break eq2) with eq2="x = y" find exactly
# a nontrivial finite model of L -- Fin<=11, far cheaper than long Vampire fmb.
def solver_has_finite_model(solver, law, mf2_budget, sat_sizes):
    eq2 = "x = y"
    try:
        if solver.mf2_find_portfolio(law, eq2, mf2_budget):
            return True
    except Exception:
        pass
    per = max(1.0, mf2_budget) / max(1, len(sat_sizes))
    for n in sat_sizes:
        try:
            if solver.sat_find_model(law, eq2, n, time.time() + per):
                return True
        except Exception:
            pass
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000, help="laws to generate")
    ap.add_argument("--seed", type=int, default=20260706)
    ap.add_argument("--leaves", type=int, default=7, help="7 leaves = 6 ops = order 6")
    ap.add_argument("--out", required=True)
    ap.add_argument("--shard", default=None, help="i/n: keep every generated law with idx%n==i")
    ap.add_argument("--cheap-only", action="store_true", help="skip fmb (fast yield estimate)")
    ap.add_argument("--cheap-max-n", type=int, default=3, help="brute small-model screen up to n")
    ap.add_argument("--fmb-timeout", type=int, default=120)
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--solver-dir", default=None,
                    help="if set, run the solver mf2/SAT finite finder (Fin<=11) "
                         "as a fast stage-2 to drop laws with moderate models before fmb")
    ap.add_argument("--mf2-budget", type=float, default=30.0)
    ap.add_argument("--sat-sizes", default="4,5,6,7,8,9,10,11")
    args = ap.parse_args()

    solver = None
    if args.solver_dir and not args.cheap_only:
        sys.path.insert(0, args.solver_dir)
        import solver as _solver
        _solver.trace = lambda *a, **k: None
        solver = _solver
    sat_sizes = [int(s) for s in args.sat_sizes.split(",") if s.strip()]

    rng = random.Random(args.seed)
    laws = generate(rng, args.n, args.leaves)
    if args.shard:
        i, m = (int(x) for x in args.shard.split("/"))
        laws = [T for k, T in enumerate(laws) if k % m == i]

    cheap_pass = []
    for T in laws:
        if any(has_nontrivial_model(T, n) for n in range(2, args.cheap_max_n + 1)):
            continue
        cheap_pass.append(T)
    print(f"generated {len(laws)} order-6 laws; {len(cheap_pass)} pass cheap n<= {args.cheap_max_n} screen")

    rows, cands, dropped_solver, processed = [], 0, 0, 0
    total = len(cheap_pass)
    with open(args.out, "w") as f:
        for T in cheap_pass:
            processed += 1
            if not args.cheap_only and processed % 50 == 0:
                print(f"  progress: {processed}/{total} processed | "
                      f"{dropped_solver} solver-dropped | {cands} candidates so far",
                      flush=True)
            law = "x = " + to_str(T)
            if args.cheap_only:
                rec = {"law": law, "canon": canon(T), "stage": "cheap_pass"}
            else:
                # stage 2: fast solver finder (Fin<=11) drops moderate-model laws
                if solver is not None and solver_has_finite_model(
                        solver, law, args.mf2_budget, sat_sizes):
                    dropped_solver += 1
                    continue
                # stage 3: Vampire fmb for the hard tail
                verdict, order = fmb(T, args.fmb_timeout, args.vampire)
                if verdict == "MODEL_FOUND":
                    continue  # has a finite model -> not Austin
                rec = {"law": law, "canon": canon(T), "stage": "fmb_candidate",
                       "fmb": verdict, "fmb_timeout": args.fmb_timeout}
                cands += 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()  # candidates visible immediately, not buffered
    if not args.cheap_only and solver is not None:
        print(f"stage-2 solver finder dropped {dropped_solver} (found Fin<=11 models)")
    print(("cheap-only: wrote %d pool laws" % len(cheap_pass)) if args.cheap_only
          else ("Austin candidates (no finite model in %ds fmb): %d" % (args.fmb_timeout, cands)))
    print(f"-> {args.out}   (next: run the validated greedy builder to split easy/hard)")


if __name__ == "__main__":
    main()
