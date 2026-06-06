import json, time, sys
import completion_prototype as kb

def load(path):
    out=[]
    if path.endswith('.json'):
        out=json.load(open(path))
    else:
        for line in open(path):
            line=line.strip()
            if line: out.append(json.loads(line))
    return out

def run(path, limit=None, tb=12.0):
    probs=load(path)
    if limit: probs=probs[:limit]
    n=len(probs); col=0; tt=0.0; hardest=[]
    for p in probs:
        eq1=p['equation1'].replace('*','◇')
        t0=time.time()
        try:
            r=kb.complete(eq1, tb=1.5, cap=16, log=False, maxp=150)
        except Exception as e:
            r=('error',0,0,None)
        dt=time.time()-t0; tt+=dt
        if r[0]=='collapse':
            col+=1
            hardest.append((dt,p.get('id'),p['eq1_id'],r[1]))
    hardest.sort(reverse=True)
    print(f"\n{path.split('/')[-1]}: {col}/{n} solved by singleton-collapse | total {tt:.1f}s, avg {tt/n:.2f}s")
    for dt,pid,e1,it in hardest[:5]:
        print(f"    {pid} eq1={e1}: {dt:.2f}s iters={it}")
    return col,n

if __name__=='__main__':
    run('/tmp/sample_20.json')
    pass
