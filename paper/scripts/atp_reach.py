#!/usr/bin/env python3
"""Map the ATP construction channel's reach: for each Austin law, does bare
saturation (E=[law] + a!=b) already certify a nontrivial model, or does it
diverge? The divergent ones are the LLM's niche (need a proposed presentation).

Correctness (E=[law] |- law) is tautological, so only the saturation query runs.
Usage:  python3 atp_reach.py <laws_file> <start> <count> <timeout_s> <out.jsonl>
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import etp_terms as et

VAMP = "paper/bin/vampire"

def sat_status(law, tmo):
    l, r, vs = et.tptp_eq_vars(law)
    body = (f"fof(law,axiom,![{','.join(vs)}]:({l}={r})).\n"
            "fof(nt,axiom,?[U,V]: U != V).\n")
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False) as fh:
        fh.write(body); p = fh.name
    try:
        out = subprocess.run([VAMP, "-sa", "otter", "--show_active", "on",
                              "-t", f"{tmo}s", p],
                             capture_output=True, text=True, timeout=tmo + 5).stdout
    except subprocess.TimeoutExpired:
        out = "TIMEOUT"
    finally:
        os.unlink(p)
    sat = ("SZS status Satisfiable" in out) and ("incomplete strategy" not in out)
    if sat: return "bare_certified"
    if "TIMEOUT" in out or "Time limit" in out: return "diverged"
    if "incomplete strategy" in out: return "incomplete"
    return "other"

def main():
    laws_file, start, count, tmo, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    laws = []
    for line in open(laws_file):
        if not line.strip(): continue
        r = json.loads(line)
        if r.get("gold") == "austin" or r.get("status") == "AUSTIN_PROVEN":
            laws.append(r["law"])
    laws = sorted(set(laws))
    chunk = laws[start:start + count]
    with open(out, "a", encoding="utf-8") as fh:
        for law in chunk:
            st = sat_status(law, tmo)
            fh.write(json.dumps({"law": law, "status": st}) + "\n"); fh.flush()
            print(f"{st:15} {law[:55]}", file=sys.stderr)

if __name__ == "__main__":
    main()
