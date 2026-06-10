#!/usr/bin/env python3
"""Experiment: Eq2-directed finite-model finder + duality vs the current
baseline (DFS+unit-prop then WalkSAT), on the hard2 FALSE residual.

A "solve" = a finite magma table that satisfies Eq1 on ALL assignments and
violates Eq2 on SOME assignment. That is exactly what the Lean judge's
decideFin! checks, so verifying in pure Python here is sound (no judge needed).
"""
import json, time, itertools, random, sys

# ── Parser (term = ('V',name) | ('C',int) | ('F',(L,R))) ──────────────────
def parse(text):
    s = text.strip()
    def strip_outer(s):
        while len(s) >= 2 and s[0] == '(' and s[-1] == ')':
            d = 0; ok = True
            for i, c in enumerate(s):
                d += c == '('; d -= c == ')'
                if d == 0 and i < len(s) - 1: ok = False; break
            if ok: s = s[1:-1].strip()
            else: break
        return s
    s = strip_outer(s); d = 0; last = -1
    for i, c in enumerate(s):
        d += c == '('; d -= c == ')'
        if d == 0 and c in '◇*': last = i
    if last < 0:
        if len(s) == 1 and s.isalpha(): return ('V', s)
        raise ValueError(repr(s))
    return ('F', (parse(s[:last]), parse(s[last+1:])))

def vars_of(eq_text):
    out = []
    import re
    for v in re.findall(r"\b([a-z])\b", eq_text):
        if v not in out: out.append(v)
    return out

def dual(t):
    if t[0] in ('V', 'C'): return t
    return ('F', (dual(t[1][1]), dual(t[1][0])))  # swap operands

# ── Concrete evaluation over a full table (for verification) ──────────────
def ev_full(t, env, tbl, n):
    if t[0] == 'V': return env[t[1]]
    if t[0] == 'C': return t[1]
    a = ev_full(t[1][0], env, tbl, n); b = ev_full(t[1][1], env, tbl, n)
    return tbl[a*n+b]

def verify(eq1, eq2, n, tbl):
    """tbl is flat length n*n. Returns True iff Eq1 holds everywhere and Eq2 fails somewhere."""
    A1,B1 = parse(eq1.split('=',1)[0]), parse(eq1.split('=',1)[1])
    A2,B2 = parse(eq2.split('=',1)[0]), parse(eq2.split('=',1)[1])
    v1, v2 = vars_of(eq1), vars_of(eq2)
    for t in itertools.product(range(n), repeat=len(v1)):
        env = dict(zip(v1, t))
        if ev_full(A1,env,tbl,n) != ev_full(B1,env,tbl,n): return False
    for t in itertools.product(range(n), repeat=len(v2)):
        env = dict(zip(v2, t))
        if ev_full(A2,env,tbl,n) != ev_full(B2,env,tbl,n): return True
    return False

# ── BASELINE: DFS+unit-prop (mf_find_false_model) then WalkSAT ────────────
def baseline_dfs(eq1, eq2, sizes, per_size):
    A1,B1 = parse(eq1.split('=',1)[0]), parse(eq1.split('=',1)[1])
    A2,B2 = parse(eq2.split('=',1)[0]), parse(eq2.split('=',1)[1])
    v1, v2 = vars_of(eq1), vars_of(eq2)
    for n in sizes:
        tbl = [None]*(n*n)
        e1 = [dict(zip(v1,t)) for t in itertools.product(range(n), repeat=len(v1))]
        e2 = [dict(zip(v2,t)) for t in itertools.product(range(n), repeat=len(v2))]
        def ev2(t, env):
            if t[0]=='V': return ('val', env[t[1]])
            if t[0]=='C': return ('val', t[1])
            ra = ev2(t[1][0], env)
            if ra[0]!='val': return ('none',)
            rb = ev2(t[1][1], env)
            if rb[0]!='val': return ('none',)
            idx = ra[1]*n+rb[1]; v = tbl[idx]
            return ('val', v) if v is not None else ('open', idx)
        def propagate(trail):
            changed = True
            while changed:
                changed = False
                for env in e1:
                    sl = ev2(A1,env); sr = ev2(B1,env)
                    if sl[0]=='val' and sr[0]=='val':
                        if sl[1]!=sr[1]: return False
                    elif sl[0]=='val' and sr[0]=='open':
                        tbl[sr[1]]=sl[1]; trail.append(sr[1]); changed=True
                    elif sr[0]=='val' and sl[0]=='open':
                        tbl[sl[1]]=sr[1]; trail.append(sl[1]); changed=True
            return True
        def eq2_violated():
            for env in e2:
                sl=ev2(A2,env); sr=ev2(B2,env)
                if sl[0]=='val' and sr[0]=='val' and sl[1]!=sr[1]: return True
            return False
        start = time.time()
        def dfs():
            if time.time()-start > per_size: return None
            trail=[]
            if not propagate(trail):
                for i in trail: tbl[i]=None
                return None
            idx=-1
            for i in range(n*n):
                if tbl[i] is None: idx=i; break
            if idx<0:
                if eq2_violated(): return tbl[:]
                for i in trail: tbl[i]=None
                return None
            for val in range(n):
                tbl[idx]=val
                r=dfs()
                if r is not None: return r
                tbl[idx]=None
            for i in trail: tbl[i]=None
            return None
        flat = dfs()
        if flat is not None: return n, flat
    return None

def baseline_walksat(eq1, eq2, sizes, per_size, max_flips=4000, noise=0.3, seed=20260608):
    rng = random.Random(seed)
    A1,B1 = parse(eq1.split('=',1)[0]), parse(eq1.split('=',1)[1])
    A2,B2 = parse(eq2.split('=',1)[0]), parse(eq2.split('=',1)[1])
    v1, v2 = vars_of(eq1), vars_of(eq2)
    for n in sizes:
        e1 = [dict(zip(v1,t)) for t in itertools.product(range(n), repeat=len(v1))]
        e2 = [dict(zip(v2,t)) for t in itertools.product(range(n), repeat=len(v2))]
        def ev(t, env, tbl):
            if t[0]=='V': return env[t[1]]
            if t[0]=='C': return t[1]
            return tbl[ev(t[1][0],env,tbl)*n+ev(t[1][1],env,tbl)]
        def touched(t, env, tbl, acc):
            if t[0] in ('V','C'): return env[t[1]] if t[0]=='V' else t[1]
            a=touched(t[1][0],env,tbl,acc); b=touched(t[1][1],env,tbl,acc)
            idx=a*n+b; acc.add(idx); return tbl[idx]
        def nbad(tbl):
            return sum(1 for env in e1 if ev(A1,env,tbl)!=ev(B1,env,tbl))
        def eq2_violated(tbl):
            return any(ev(A2,env,tbl)!=ev(B2,env,tbl) for env in e2)
        start=time.time()
        while time.time()-start < per_size:
            tbl=[rng.randrange(n) for _ in range(n*n)]
            for _ in range(max_flips):
                if time.time()-start > per_size: break
                bad=[env for env in e1 if ev(A1,env,tbl)!=ev(B1,env,tbl)]
                if not bad:
                    if eq2_violated(tbl): return n, tbl[:]
                    tbl[rng.randrange(n*n)]=rng.randrange(n); continue
                env=rng.choice(bad); acc=set()
                touched(A1,env,tbl,acc); touched(B1,env,tbl,acc); acc=list(acc)
                if rng.random()<noise:
                    tbl[rng.choice(acc)]=rng.randrange(n)
                else:
                    best=None; bestc=10**9
                    for c in acc:
                        old=tbl[c]
                        for val in range(n):
                            if val==old: continue
                            tbl[c]=val; sc=nbad(tbl)
                            if sc<bestc: bestc=sc; best=(c,val)
                        tbl[c]=old
                    if best: tbl[best[0]]=best[1]
    return None

def baseline(eq1, eq2, budget):
    # mirror solver: DFS sizes 4,5,6 then walksat 5,6,7. Split budget.
    half = budget/2.0
    out = baseline_dfs(eq1, eq2, sizes=(4,5,6), per_size=half/3.0)
    if out is None:
        out = baseline_walksat(eq1, eq2, sizes=(5,6,7), per_size=half/3.0)
    return out

# ── NEW: Eq2-directed DFS with least-number heuristic + duality ───────────
def directed_one(eq1, eq2, n, budget):
    """Directed search on a single size n. Seeds an Eq2 violation: pick an
    Eq2 assignment env2 and force its LHS to value u (a constant constraint),
    then complete Eq1 with the least-number heuristic. Any completion that
    leaves Eq2 violated is returned. Enumerate (env2,u) as restarts."""
    A1,B1 = parse(eq1.split('=',1)[0]), parse(eq1.split('=',1)[1])
    A2,B2 = parse(eq2.split('=',1)[0]), parse(eq2.split('=',1)[1])
    v1, v2 = vars_of(eq1), vars_of(eq2)
    e1 = [dict(zip(v1,t)) for t in itertools.product(range(n), repeat=len(v1))]
    e2 = [dict(zip(v2,t)) for t in itertools.product(range(n), repeat=len(v2))]
    start = time.time()

    def ev2(t, env, tbl):
        if t[0]=='V': return ('val', env[t[1]])
        if t[0]=='C': return ('val', t[1])
        ra = ev2(t[1][0], env, tbl)
        if ra[0]!='val': return ('none',)
        rb = ev2(t[1][1], env, tbl)
        if rb[0]!='val': return ('none',)
        idx = ra[1]*n+rb[1]; v = tbl[idx]
        return ('val', v) if v is not None else ('open', idx)

    def propagate(tbl, constraints, trail):
        # constraints: list of (treeL, treeR, env) meaning eval(L)==eval(R)
        changed = True
        while changed:
            changed = False
            for (L,R,env) in constraints:
                sl = ev2(L,env,tbl); sr = ev2(R,env,tbl)
                if sl[0]=='val' and sr[0]=='val':
                    if sl[1]!=sr[1]: return False
                elif sl[0]=='val' and sr[0]=='open':
                    tbl[sr[1]]=sl[1]; trail.append(sr[1]); changed=True
                elif sr[0]=='val' and sl[0]=='open':
                    tbl[sl[1]]=sr[1]; trail.append(sl[1]); changed=True
        return True

    def eq2_violated(tbl):
        for env in e2:
            sl=ev2(A2,env,tbl); sr=ev2(B2,env,tbl)
            if sl[0]=='val' and sr[0]=='val' and sl[1]!=sr[1]: return True
        return False

    base_constraints = [(A1,B1,env) for env in e1]

    def solve_with_seed(seed_constraints):
        tbl = [None]*(n*n)
        cons = base_constraints + seed_constraints
        def dfs():
            if time.time()-start > budget: return None
            trail=[]
            if not propagate(tbl, cons, trail):
                for i in trail: tbl[i]=None
                return None
            # least-number heuristic: only allow values up to current_max+1
            cur_max = -1
            idx=-1
            for i in range(n*n):
                if tbl[i] is None and idx<0: idx=i
                elif tbl[i] is not None and tbl[i]>cur_max: cur_max=tbl[i]
            if idx<0:
                if eq2_violated(tbl): return tbl[:]
                for i in trail: tbl[i]=None
                return None
            hi = min(n-1, cur_max+1)
            for val in range(hi+1):
                tbl[idx]=val
                r=dfs()
                if r is not None: return r
                tbl[idx]=None
            for i in trail: tbl[i]=None
            return None
        return dfs()

    # Directed restarts: force one Eq2 instance's LHS = u (constant).
    for env in e2:
        for u in range(n):
            if time.time()-start > budget: return None
            seed = [(A2, ('C',u), env)]      # eval(L2 @ env) == u
            r = solve_with_seed(seed)
            if r is not None: return n, r
    return None

def directed(eq1, eq2, budget):
    # try sizes, splitting budget; on each size also try the dual (transpose).
    sizes = (4,5,6,7)
    per = budget/len(sizes)
    deq1, deq2 = None, None
    for n in sizes:
        t0 = time.time()
        out = directed_one(eq1, eq2, n, per/2)
        if out is not None: return out
        # dual pass: solve dual problem, transpose the table back
        if deq1 is None:
            A1,B1 = parse(eq1.split('=',1)[0]), parse(eq1.split('=',1)[1])
            A2,B2 = parse(eq2.split('=',1)[0]), parse(eq2.split('=',1)[1])
            def s(t):
                if t[0]=='V': return t[1]
                return '('+s(t[1][0])+'◇'+s(t[1][1])+')'
            deq1 = s(dual(A1))+'='+s(dual(B1))
            deq2 = s(dual(A2))+'='+s(dual(B2))
        remain = per - (time.time()-t0)
        if remain > 0.05:
            out = directed_one(deq1, deq2, n, remain)
            if out is not None:
                nn, flat = out
                # transpose: original_tbl[i*n+j] = dual_tbl[j*n+i]
                trans = [flat[j*nn+i] for i in range(nn) for j in range(nn)]
                return nn, trans
    return None

# ── Run comparison ────────────────────────────────────────────────────────
RESULTS = '/sessions/gracious-blissful-cerf/mnt/outputs/results_hard2.jsonl'

def run_slice():
    import os
    path = '/sessions/gracious-blissful-cerf/mnt/equational-theories-lean-stage2/examples/problems/hard2.jsonl'
    budget = float(sys.argv[1]) if len(sys.argv)>1 else 3.0
    deadline = float(sys.argv[2]) if len(sys.argv)>2 else 40.0  # wall budget for THIS call
    rows = [json.loads(l) for l in open(path)]
    false_rows = [r for r in rows if r.get('answer') is False]
    done = {}
    if os.path.exists(RESULTS):
        for l in open(RESULTS):
            d=json.loads(l); done[d['id']]=d
    t_start=time.time()
    for r in false_rows:
        rid=r['id']
        if rid in done: continue
        if time.time()-t_start > deadline: break
        eq1=r['equation1'].replace('*','◇'); eq2=r['equation2'].replace('*','◇')
        ob=baseline(eq1,eq2,budget); od=directed(eq1,eq2,budget)
        bn = ob[0] if (ob and verify(eq1,eq2,*ob)) else None
        dn = od[0] if (od and verify(eq1,eq2,*od)) else None
        b_inv = bool(ob) and bn is None
        d_inv = bool(od) and dn is None
        rec={'id':rid,'base_n':bn,'dir_n':dn,'base_invalid':b_inv,'dir_invalid':d_inv}
        with open(RESULTS,'a') as f: f.write(json.dumps(rec)+'\n')
        print(rid,'base',bn,'dir',dn, '  INVALID!' if (b_inv or d_inv) else '')
    # summary
    done={}
    for l in open(RESULTS): d=json.loads(l); done[d['id']]=d
    print(f"\n# progress {len(done)}/{len(false_rows)}")

def main():
    run_slice()

if __name__ == '__main__':
    main()
                                                                         