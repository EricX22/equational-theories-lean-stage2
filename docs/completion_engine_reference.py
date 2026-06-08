import sys as _kc_sys
_kc_sys.setrecursionlimit(8000)
import time
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


if __name__ == "__main__":
    # Demo: eq2377 (x = (y◇(z◇(x◇w)))◇y) implies eq1139.
    body = kc_singleton_lean(
        "x = (y ◇ (z ◇ (x ◇ w))) ◇ y",
        "x", "y ◇ ((y ◇ (z ◇ z)) ◇ z)", ["x", "y", "z"], tb=20)
    print(body if body else "no singleton collapse")
