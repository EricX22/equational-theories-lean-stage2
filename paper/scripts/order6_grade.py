#!/usr/bin/env python3
"""Confirm + grade order-6 Austin candidates by construction rung.

Input: order6_austin_*.jsonl (no small finite model + not trivial).
For each law:
  1. CONFIRM Austin: long fmb; if a finite model turns up it's not Austin -> drop.
  2. GRADE the survivors by the strongest-that-works construction method:
       Rung 1  translation-invariant model  a<>b = b + f(b-a)  (verified f)
       Rung 2  greedy magma builder, verified on its full constructed domain
       Rung 4  resisted both  -> open-to-us (the hard frontier)
Output: {law, austin, rung, method} per confirmed law.

Rung 3 (bespoke case-defined) isn't automated, so "resists 1 and 2" = Rung 4 here,
i.e. "beyond our published construction suite" — the honest, reproducible label.
"""
from __future__ import annotations
import argparse, glob, itertools, json, os, subprocess, sys, tempfile


def load_laws(patterns):
    seen, laws = set(), []
    for pat in patterns:
        for path in sorted(glob.glob(pat)):
            for line in open(path):
                line = line.strip()
                if line:
                    law = json.loads(line).get("law")
                    if law and law not in seen:
                        seen.add(law); laws.append(law)
    return laws


def fmb_has_model(et, law, timeout, vbin):
    l, r, vs = et.tptp_eq_vars(law)
    body = (f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\n"
            "fof(nt,axiom,?[U,V]:U!=V).\n")
    with tempfile.TemporaryDirectory() as wd:
        p = os.path.join(wd, "p.p"); open(p, "w").write(body)
        try:
            s = subprocess.run([vbin, "-sa", "fmb", "-t", f"{timeout}s", p],
                               capture_output=True, text=True, timeout=timeout + 5).stdout
        except subprocess.TimeoutExpired:
            return False
    return "Finite Model Found" in s or "SZS status Satisfiable" in s


# ---- Rung 1: translation-invariant solver (op(a,b)=b+f(b-a)) ----
def ti_solve(et, rhs, R=4, budget=6000):
    L = ('var', 'x')  # laws are "x = rhs"
    v = sorted(set(et.variables(('var', 'x')) + et.variables(rhs)) | {'x'})
    f = {0: 0}; nov = [10**6]
    class Conflict(Exception): pass
    def ev(node, env, top=False):
        if node[0] == 'var': return env[node[1]]
        va = ev(node[1], env); vb = ev(node[2], env); d = vb - va
        if top:
            need = env['x'] - vb
            if d in f:
                if f[d] != need: raise Conflict()
            else: f[d] = need
            return env['x']
        if d not in f: nov[0] += 1; f[d] = nov[0]
        return vb + f[d]
    dom = range(-R, R + 1); pr = 0
    for t in itertools.product(dom, repeat=len(v)):
        if pr >= budget: break
        pr += 1
        try: ev(rhs, dict(zip(v, t)), top=True)
        except Conflict: return False
    def evc(node, env):
        if node[0] == 'var': return env[node[1]]
        va = evc(node[1], env); vb = evc(node[2], env); d = vb - va
        return None if d not in f else vb + f[d]
    for t in itertools.product(dom, repeat=len(v)):
        env = dict(zip(v, t)); val = evc(rhs, env)
        if val is not None and val != env['x']: return False
    return True


# ---- Rung 2: greedy magma builder + full-domain verification ----
# NOTE: vars must be the law's actual variables, x first. Hardcoding x,y,z here
# silently raised KeyError('w') on every 4-variable law -- i.e. on most one-op
# extensions -- and the caller swallowed it as baseline="error:'w'".
def greedy_build(rhs, vs, budget=4000, K=5, cap=40, step_cap=6000):
    op = {}; nov = [10**7]; carrier = [1, 2, 3]
    def values(node, env, steps):
        if node[0] == 'var': yield env[node[1]]; return
        for a in values(node[1], env, steps):
            for b in values(node[2], env, steps):
                if steps[0] <= 0: return
                key = (a, b)
                if key in op: yield op[key]
                else:
                    nov[0] += 1
                    for c in [nov[0]] + carrier[:K]:
                        steps[0] -= 1; op[key] = c; yield c; del op[key]
    def satisfy(env, want):
        steps = [step_cap]
        if rhs[0] == 'var': return env[rhs[1]] == want
        for a in values(rhs[1], env, steps):
            for b in values(rhs[2], env, steps):
                if steps[0] <= 0: return False
                key = (a, b)
                if key in op:
                    if op[key] == want: return True
                else: op[key] = want; return True
        return False
    carrset = set(carrier); done = set(); pr = 0
    while pr < budget:
        nt = [t for t in itertools.product(carrier, repeat=len(vs)) if t not in done]
        if not nt:
            add = sorted(e for e in (set(op.values()) | {a for k in op for a in k}) if e not in carrset)
            if not add or len(carrier) >= cap: break
            for e in add[:4]:
                if len(carrier) < cap: carrset.add(e); carrier.append(e)
            continue
        for t in nt:
            if pr >= budget: break
            done.add(t); pr += 1
            env = dict(zip(vs, t))
            if not satisfy(env, env['x']): return None
    return op, sorted(carrset)


def verify_domain(op, carrier, rhs, vs):
    def ev(node, env):
        if node[0] == 'var': return env[node[1]]
        a = ev(node[1], env); b = ev(node[2], env)
        if a is None or b is None: return None
        return op.get((a, b))
    for t in itertools.product(carrier, repeat=len(vs)):
        env = dict(zip(vs, t)); val = ev(rhs, env)
        if val is not None and val != env['x']: return False
    return True


def law_vars(et, l, r):
    """x first, then the rest -- greedy_build wants env['x'] as the target."""
    vs = et.variables(l) + et.variables(r)
    rest = sorted(set(vs) - {'x'})
    return ['x'] + rest


def grade(et, law):
    l, r = et.parse_equation(law)
    if ti_solve(et, r): return 1, "translation_invariant"
    vs = law_vars(et, l, r)
    res = greedy_build(r, vs)
    if res is not None and verify_domain(res[0], res[1], r, vs): return 2, "greedy_verified"
    return 4, "open_to_us"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--vampire", default="vampire")
    ap.add_argument("--fmb-timeout", type=int, default=300,
                    help="long fmb to CONFIRM no finite model before grading")
    ap.add_argument("--shard", default=None)
    args = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import etp_terms as et

    laws = load_laws(args.inp)
    if args.shard:
        i, m = (int(x) for x in args.shard.split("/"))
        laws = [L for k, L in enumerate(laws) if k % m == i]
    print(f"confirm+grade {len(laws)} candidates", flush=True)

    tally = {1: 0, 2: 0, 4: 0}; dropped = 0
    with open(args.out, "w") as f:
        for j, law in enumerate(laws, 1):
            if j % 20 == 0:
                print(f"  {j}/{len(laws)} | R1={tally[1]} R2={tally[2]} R4={tally[4]} "
                      f"| dropped(non-Austin)={dropped}", flush=True)
            if fmb_has_model(et, law, args.fmb_timeout, args.vampire):
                dropped += 1
                continue
            rung, method = grade(et, law)
            tally[rung] += 1
            f.write(json.dumps({"law": law, "austin": True,
                                "rung": rung, "method": method}) + "\n")
            f.flush()
    print(f"graded: Rung1={tally[1]} Rung2={tally[2]} Rung4={tally[4]} "
          f"| dropped(had finite model)={dropped} -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
