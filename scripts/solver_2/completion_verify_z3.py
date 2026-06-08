import json, itertools, z3
import completion_prototype as kb
probs=json.load(open('/tmp/sample_20.json'))
def sat_eq1(eq1, n):
    # is there an n-element magma satisfying eq1? (n>=2 => non-singleton model exists)
    s=z3.Solver()
    f=z3.Function('f',z3.IntSort(),z3.IntSort(),z3.IntSort())
    V=[[z3.Int(f"o_{i}_{j}") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            s.add(V[i][j]>=0,V[i][j]<n,f(i,j)==V[i][j])
    F=lambda a,b:f(a,b)
    # parse eq1 into a python evaluator using kb tree
    t=kb.parse(eq1.split('=')[0]); u=kb.parse(eq1.split('=')[1])
    vs=sorted(kb.vars_of(t)|kb.vars_of(u))
    def ev(node,env):
        if node[0]=='V': return env[node[1]]
        return F(ev(node[2][0],env),ev(node[2][1],env))
    for vals in itertools.product(range(n),repeat=len(vs)):
        env=dict(zip(vs,vals))
        s.add(ev(t,env)==ev(u,env))
    return s.check()==z3.sat

print(f"{'id':14} {'eq1':4} {'engine':10} {'z3: >=2-elt model up to n=4':28} {'verdict'}")
for p in probs:
    eq1=p['equation1'].replace('*','◇')
    r=kb.complete(eq1, tb=1.5, cap=16, log=False, maxp=150)
    eng = 'COLLAPSE' if r[0]=='collapse' else r[0]
    # z3: does a >=2 model exist up to n=4?
    has_model=False
    for n in (2,3,4):
        if sat_eq1(eq1,n): has_model=True; break
    singleton = not has_model
    # consistency: engine says collapse  <=>  z3 says singleton-forcing (up to n=4)
    consistent = (r[0]=='collapse')==singleton
    print(f"{p['id']:14} {p['eq1_id']:<4} {eng:10} {'no model(singleton)' if singleton else 'HAS >=2 model':28} {'consistent' if consistent else '** MISMATCH **'}")
