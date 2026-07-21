#!/usr/bin/env bash
# finalize_llm.sh — the last paid experiments (#1 fill the dashes, #3 stability).
# Same conventions as overnight_llm.sh: stage markers, credit gate, resumable.
#   export OPENROUTER_API_KEY=...
#   setsid bash paper/scripts/finalize_llm.sh </dev/null >/dev/null 2>&1 & disown
#   tail -f paper/results/finalize_llm.log
set -u
cd "$(dirname "$0")/../.." || exit 1
RES=paper/results
MARK=$RES/.done_llm
mkdir -p "$MARK"
exec >> $RES/finalize_llm.log 2>&1
echo "=================================================================="
echo "finalize_llm start $(date)"
[ -n "${OPENROUTER_API_KEY:-}" ] || { echo "FATAL: OPENROUTER_API_KEY not set"; exit 1; }
MIN_CREDITS="${MIN_CREDITS:-2}"

credits() {
python3 - <<'PY'
import json, os, urllib.request
try:
    req = urllib.request.Request("https://openrouter.ai/api/v1/credits",
        headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read())["data"]
    print(round(d["total_credits"] - d["total_usage"], 2))
except Exception:
    print("unknown")
PY
}
gate() {
    c=$(credits); echo "-- credit gate: balance=$c (min $MIN_CREDITS)"
    python3 -c "import sys; c='$c'; sys.exit(0 if c=='unknown' or float(c)>=float('$MIN_CREDITS') else 1)" \
        || { echo "-- LOW CREDITS: skipping remaining API stages"; return 1; }
}
stage() {
    name=$1; shift
    if [ -f "$MARK/$name" ]; then echo "== $name: already done, skipping"; return 0; fi
    echo "== $name: start $(date)"
    if "$@"; then touch "$MARK/$name"; echo "== $name: OK $(date)"
    else echo "== $name: FAILED (continuing)"; fi
}

# ---- #1a  GPT-4.1 on the 25 construction cases (near-free) ----------------
gate && stage f1_gpt41_construct \
    python3 -B paper/scripts/llm_construct.py \
        --laws-file $RES/hard25_sample.jsonl \
        --model openai/gpt-4.1 --rounds 3 --timeout 60 \
        --vampire paper/bin/vampire --out $RES/llm_construct_gpt41_hard25.jsonl

# ---- #1b  o4-mini on the 25 construction cases (medium effort) ------------
gate && stage f1_o4mini_construct \
    python3 -B paper/scripts/llm_construct.py \
        --laws-file $RES/hard25_sample.jsonl \
        --model openai/o4-mini --reasoning-effort medium --rounds 3 --timeout 60 \
        --vampire paper/bin/vampire --out $RES/llm_construct_o4mini_hard25.jsonl

# ---- #3  stability: the nine solved + five matched unsolved ---------------
build_repro_set() {
python3 - <<'PY'
import json
runs = {}
for line in open("paper/results/llm_autoform_o3_cert63.jsonl", encoding="utf-8"):
    line = line.strip()
    if line:
        r = json.loads(line); runs[r["law"]] = r
harvest = [json.loads(l) for l in open("paper/results/easy_chain_harvest.jsonl", encoding="utf-8")
           if l.strip() and json.loads(l).get("chain")]
solved = [h for h in harvest if runs.get(h["law"], {}).get("solved")]
unsolved = [h for h in harvest if h["law"] in runs and not runs[h["law"]].get("solved")]
matched = unsolved[:5]                      # harvest order ~ difficulty rank: nearest matches
rows = solved + matched
with open("paper/results/o3_repro_set.jsonl", "w", encoding="utf-8") as f:
    for h in rows:
        f.write(json.dumps(h, ensure_ascii=False) + "\n")
print(f"repro set: {len(solved)} solved + {len(matched)} matched unsolved")
assert len(solved) == 9
PY
}
stage f3_build_set build_repro_set

gate && stage f3_o3_repro \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $RES/o3_repro_set.jsonl \
        --model openai/o3 --reasoning-effort medium --rounds 3 --timeout 600 \
        --lean-dir . --out $RES/llm_autoform_o3_repro.jsonl

# ---- summary --------------------------------------------------------------
echo "== SUMMARY $(date)"
python3 - <<'PY'
import json, os
def rows(p):
    if not os.path.exists(p): return None
    laws = {}
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l); laws[r["law"]] = r
    return laws
for label, fn in [("#1a gpt-4.1 construct", "llm_construct_gpt41_hard25.jsonl"),
                  ("#1b o4-mini construct", "llm_construct_o4mini_hard25.jsonl")]:
    d = rows(f"paper/results/{fn}")
    if d is None: print(f"{label:24} (not run)"); continue
    s = sum(1 for r in d.values() if r.get("solved"))
    # horn split over final round of each law
    corr_only = nonvac_only = neither = 0
    for r in d.values():
        if r.get("solved"): continue
        atts = [a for a in r.get("attempts", []) if "E" in a]
        if not atts: neither += 1; continue
        a = atts[-1]
        if a["corr"] and not a["nonvac"]: corr_only += 1
        elif a["nonvac"] and not a["corr"]: nonvac_only += 1
        else: neither += 1
    print(f"{label:24} {s}/{len(d)} solved | entail-but-collapse {corr_only}, "
          f"consistent-but-weak {nonvac_only}, neither/parse {neither}")
d = rows("paper/results/llm_autoform_o3_repro.jsonl")
if d is None:
    print("#3 o3 repro            (not run)")
else:
    solved_set = set()
    for l in open("paper/results/o3_repro_set.jsonl", encoding="utf-8"):
        r = json.loads(l); solved_set.add(r["law"])
    orig = {}
    for l in open("paper/results/llm_autoform_o3_cert63.jsonl", encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l); orig[r["law"]] = r.get("solved", False)
    rep_of_solved = sum(1 for law, r in d.items() if orig.get(law) and r.get("solved"))
    new_on_unsolved = sum(1 for law, r in d.items() if law in orig and not orig[law] and r.get("solved"))
    n_solved = sum(1 for law in d if orig.get(law))
    n_unsolved = len(d) - n_solved
    print(f"#3 o3 repro            {rep_of_solved}/{n_solved} of solved reproduce; "
          f"{new_on_unsolved}/{n_unsolved} previously-unsolved newly solve")
print("balance-aware: check finalize_llm.log credit-gate lines for spend")
PY
echo "finalize_llm end $(date)"
