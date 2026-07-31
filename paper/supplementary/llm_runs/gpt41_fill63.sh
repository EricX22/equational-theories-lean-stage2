#!/usr/bin/env bash
# gpt41_fill63.sh — fill Table 5's GPT-4.1 cells on the full 63-law set, both
# conditions. Same conventions as finalize_llm.sh: stage markers, credit gate,
# resumable, FRESH output filenames (never appends to an existing results file).
#   export OPENROUTER_API_KEY=...
#   setsid bash paper/scripts/gpt41_fill63.sh </dev/null >/dev/null 2>&1 & disown
#   tail -f paper/results/gpt41_fill63.log
set -u
cd "$(dirname "$0")/../.." || exit 1
RES=paper/results
MARK=$RES/.done_llm
mkdir -p "$MARK"
exec >> $RES/gpt41_fill63.log 2>&1
echo "=================================================================="
echo "gpt41_fill63 start $(date)"
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

# ---- build the 63-law input from run A of the o3 cert file ----------------
# First 63 records of llm_autoform_o3_cert63.jsonl are run A (one record per
# law); strip to bare {"law": ...} lines so the loader applies no status filter
# (same trick as hard25_trivial_input.jsonl).
build_input() {
python3 - <<'PY'
import json
laws, seen = [], set()
for line in open("paper/results/llm_autoform_o3_cert63.jsonl", encoding="utf-8"):
    line = line.strip()
    if not line: continue
    law = json.loads(line)["law"]
    if law in seen: continue
    seen.add(law); laws.append(law)
    if len(laws) == 63: break
assert len(laws) == 63, f"expected 63 laws, got {len(laws)}"
with open("paper/results/cert63_input.jsonl", "w", encoding="utf-8") as f:
    for law in laws:
        f.write(json.dumps({"law": law}, ensure_ascii=False) + "\n")
print("cert63_input.jsonl: 63 laws")
PY
}
stage g0_build_input build_input

# ---- GPT-4.1, no waypoints (matches o3 nohints condition) -----------------
gate && stage g1_gpt41_nohints63 \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $RES/cert63_input.jsonl \
        --model openai/gpt-4.1 --rounds 3 --timeout 600 --hints none \
        --lean-dir . --out $RES/llm_autoform_gpt41_nohints63.jsonl

# ---- GPT-4.1, with waypoints (matches o3 cert63 condition) ----------------
gate && stage g2_gpt41_cert63 \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $RES/cert63_input.jsonl \
        --model openai/gpt-4.1 --rounds 3 --timeout 600 --hints full \
        --lean-dir . --out $RES/llm_autoform_gpt41_cert63.jsonl

# ---- summary --------------------------------------------------------------
echo "== SUMMARY $(date)"
python3 - <<'PY'
import json, os
for label, fn in [("gpt-4.1 no waypoints", "llm_autoform_gpt41_nohints63.jsonl"),
                  ("gpt-4.1 waypoints", "llm_autoform_gpt41_cert63.jsonl")]:
    p = f"paper/results/{fn}"
    if not os.path.exists(p):
        print(f"{label:22} (not run)"); continue
    laws = {}
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l); laws[r["law"]] = r
    s = sum(1 for r in laws.values() if r.get("solved"))
    ctok = sum(r.get("completion_tokens", 0) for r in laws.values())
    print(f"{label:22} {s}/{len(laws)} solved ({100*s/len(laws):.1f}% pass@1), {ctok:,} ctok")
print("balance: check gpt41_fill63.log credit-gate lines for spend")
PY
echo "gpt41_fill63 end $(date)"