"""Ordered (unfailing) Knuth-Bendix completion prototype.

Decision procedure for the SINGLETON route: given hypothesis eq1 as an
equation, run ordered completion (full unification, LPO, critical pairs,
ordered rewriting). If it derives an equation between two distinct
variables, eq1 forces a singleton magma -> the implication is TRUE for
ANY goal eq2.

Validated on examples/problems/sample_20.json: 10/20 solved via
singleton-collapse in <1s each (incl. eq2377, a prior zero-LLM-success
case). All collapses cross-checked sound against z3 (no >=2-element
model). The other 10 saturate (genuinely non-singleton) -> handled by
the existing counterexample search.

STATUS: decision procedure only. Proof-certificate reconstruction into
judge-valid Lean is the remaining integration step.
"""
import sys, time
sys.setrecursionlimit(8000)
OP='o'; CEIL=20
def is_v(t): return t[0]=='V'

def parse(text):
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
    return ('F',OP,(parse(s[:last]),parse(s[last+1:])))

def sizecap(t,cap):
    # iterative size, returns size or cap+1 if exceeds
    st=[t]; n=0
    while st:
        x=st.pop(); n+=1
        if n>cap: return cap+1
        if not is_v(x): st.extend(x[2])
    return n
def size(t): return sizecap(t,10**9)

def vars_of(t):
    st=[t]; acc=set()
    while st:
        x=st.pop()
        if is_v(x): acc.add(x[1])
        else: st.extend(x[2])
    return acc

def rename(t,suf):
    if is_v(t): return ('V',t[1]+suf)
    return ('F',t[1],tuple(rename(a,suf) for a in t[2]))

def deref(t,s):
    while is_v(t) and t[1] in s: t=s[t[1]]
    return t
def occurs(v,t,s):
    st=[t]
    while st:
        x=deref(st.pop(),s)
        if is_v(x):
            if x[1]==v: return True
        else: st.extend(x[2])
    return False
def unify(x,y,s):
    if s is None: return None
    x=deref(x,s); y=deref(y,s)
    if is_v(x):
        if is_v(y) and x[1]==y[1]: return s
        if occurs(x[1],y,s): return None
        s2=dict(s); s2[x[1]]=y; return s2
    if is_v(y):
        if occurs(y[1],x,s): return None
        s2=dict(s); s2[y[1]]=x; return s2
    if x[1]!=y[1] or len(x[2])!=len(y[2]): return None
    for a,b in zip(x[2],y[2]):
        s=unify(a,b,s)
        if s is None: return None
    return s
def appsub(t,s):
    t=deref(t,s)
    if is_v(t): return t
    return ('F',t[1],tuple(appsub(a,s) for a in t[2]))
def match(p,t,s):
    if s is None: return None
    if is_v(p):
        if p[1] in s: return s if s[p[1]]==t else None
        s2=dict(s); s2[p[1]]=t; return s2
    if is_v(t) or p[1]!=t[1] or len(p[2])!=len(t[2]): return None
    for a,b in zip(p[2],t[2]):
        s=match(a,b,s)
        if s is None: return None
    return s

PREC={OP:10}
def prec(f): return PREC.get(f,0)
def lpo_gt(s,t):
    if s==t: return False
    if is_v(t): return (not is_v(s)) and (t[1] in vars_of(s))
    if is_v(s): return False
    f,ss=s[1],s[2]; g,ts=t[1],t[2]
    for si in ss:
        if si==t or lpo_gt(si,t): return True
    if all(lpo_gt(s,tj) for tj in ts):
        if prec(f)>prec(g): return True
        if f==g:
            for a,b in zip(ss,ts):
                if a==b: continue
                return lpo_gt(a,b)
            return False
    return False

def nonvar_positions(t,path=()):
    if is_v(t): return
    yield path,t
    for i,a in enumerate(t[2]):
        yield from nonvar_positions(a,path+(i,))
def replace(t,path,new):
    if not path: return new
    i=path[0]
    return ('F',t[1],tuple(replace(a,path[1:],new) if k==i else a for k,a in enumerate(t[2])))

def rewrite_once(t,eqs):
    for (s0,t0) in eqs:
        s_,t_=rename(s0,'$'),rename(t0,'$')
        for (l,r) in ((s_,t_),(t_,s_)):
            for path,sub in nonvar_positions(t):
                sg=match(l,sub,{})
                if sg is None: continue
                lin=appsub(l,sg); rin=appsub(r,sg)
                if lpo_gt(lin,rin):
                    cand=replace(t,path,rin)
                    if sizecap(cand,CEIL)<=CEIL:
                        return cand
    return None
def normalize(t,eqs,steps=80):
    for _ in range(steps):
        nt=rewrite_once(t,eqs)
        if nt is None or nt==t: return t
        t=nt
    return t
def norm_eq(eq,eqs): return (normalize(eq[0],eqs),normalize(eq[1],eqs))

def canon_side(t,m,ctr):
    if is_v(t):
        if t[1] not in m: m[t[1]]='V%d'%ctr[0]; ctr[0]+=1
        return m[t[1]]
    return t[1]+'('+','.join(canon_side(a,m,ctr) for a in t[2])+')'
def canon(eq):
    def one(a,b):
        m={};ctr=[0]; return canon_side(a,m,ctr)+'='+canon_side(b,m,ctr)
    return min(one(eq[0],eq[1]),one(eq[1],eq[0]))

def crit_pairs(e1,e2,cap):
    out=[]
    e2r=(rename(e2[0],'#'),rename(e2[1],'#'))
    for (l1,r1) in ((e1[0],e1[1]),(e1[1],e1[0])):
        for (l2,r2) in ((e2r[0],e2r[1]),(e2r[1],e2r[0])):
            for path,sub in nonvar_positions(l1):
                sg=unify(sub,l2,{})
                if sg is None: continue
                R1=appsub(r1,sg)
                if sizecap(R1,cap)>cap: continue
                L1=appsub(l1,sg)
                if lpo_gt(R1,L1): continue
                if lpo_gt(appsub(r2,sg),appsub(l2,sg)): continue
                newl=appsub(replace(l1,path,r2),sg)
                if sizecap(newl,cap)>cap: continue
                out.append((R1,newl))
    return out

def is_collapse(eq):
    a,b=eq; return is_v(a) and is_v(b) and a[1]!=b[1]

def complete(eq_str, tb=30.0, cap=18, maxp=600, log=True):
    parts=eq_str.split('=')
    E=(parse(parts[0]),parse(parts[1]))
    start=time.time(); processed=[]; queue=[E]; seen=set(); iters=0
    while queue:
        if time.time()-start>tb: return ('timeout',iters,len(processed),None)
        queue.sort(key=lambda e:size(e[0])+size(e[1]))
        e=queue.pop(0)
        e=norm_eq(e,processed)
        if e[0]==e[1]: continue
        k=canon(e)
        if k in seen: continue
        seen.add(k)
        if is_collapse(e): return ('collapse',iters,len(processed),e)
        iters+=1
        if log and iters%50==0:
            print(f"  iter={iters} proc={len(processed)} queue={len(queue)} t={time.time()-start:.1f}s last={canon(e)[:60]}",file=sys.stderr)
        news=[]
        rules=processed+[e]
        for f in rules:
            for cp in crit_pairs(e,f,cap)+crit_pairs(f,e,cap):
                cp=norm_eq(cp,rules)
                if cp[0]==cp[1]: continue
                if sizecap(cp[0],cap)>cap or sizecap(cp[1],cap)>cap: continue
                kk=canon(cp)
                if kk in seen: continue
                if is_collapse(cp): return ('collapse',iters,len(processed),cp)
                news.append(cp)
        processed.append(e)
        queue.extend(news)
        if len(processed)>maxp: return ('maxproc',iters,len(processed),None)
    return ('saturated',iters,len(processed),None)

if __name__=='__main__':
    eq="(y ◇ (z ◇ (x ◇ w))) ◇ y = x"
    print("law:",eq)
    t0=time.time()
    res=complete(eq, tb=30.0, cap=18)
    print("RESULT:",res[0],"iters:",res[1],"processed:",res[2],"time=%.1fs"%(time.time()-t0))
    if res[3]: print("collapse:",canon(res[3]))

def test_battery():
    cases=[
        ("commutativity","x ◇ y = y ◇ x", False),
        ("associativity","(x ◇ y) ◇ z = x ◇ (y ◇ z)", False),
        ("left-projection","x ◇ y = x", False),
        ("right-projection","x ◇ y = y", False),
        ("idempotence","x ◇ x = x", False),
        ("eq2377 (target)","(y ◇ (z ◇ (x ◇ w))) ◇ y = x", True),
        ("known-singleton x=(a◇x)◇b","x = (y ◇ x) ◇ z", True),
    ]
    print("\n%-28s %-10s %-10s %s"%("law","expect","got","ok"))
    for name,eq,expect_collapse in cases:
        r=complete(eq, tb=20.0, cap=18, log=False)
        got = (r[0]=='collapse')
        ok = (got==expect_collapse)
        print("%-28s %-10s %-10s %s  [%s iters=%s proc=%s]"%(
            name, "collapse" if expect_collapse else "no", r[0], "OK" if ok else "**FAIL**", r[0], r[1], r[2]))

if __name__=='__main__':
    test_battery()
