#!/usr/bin/env bash
# overnight_llm.sh — the remaining ALPS LLM experiments (E2-E5), unattended.
#
# Run from the repo root:
#   export OPENROUTER_API_KEY=...
#   nohup bash paper/scripts/overnight_llm.sh > /dev/null 2>&1 &
#   tail -f paper/results/overnight_llm.log
#
# Properties:
#   - waits for the in-flight o3 cert63 run (E1) to finish before starting;
#   - stage markers in paper/results/.done_llm/ -> rerunning the script skips
#     completed stages (and the autoformalizer resumes row-level anyway);
#   - a credit gate before every API stage (set MIN_CREDITS, default 3 USD):
#     if the OpenRouter balance is below it, remaining API stages are skipped
#     instead of fast-failing with 402s;
#   - stage order = required first: E1 top-up -> solved subset -> E2 support-down
#     -> E5 construction/hard tier -> E3 o4-mini panel -> E4 effort axis.
set -u

cd "$(dirname "$0")/../.." || exit 1
RES=paper/results
MARK=$RES/.done_llm
mkdir -p "$MARK"
LOG=$RES/overnight_llm.log
exec >> "$LOG" 2>&1
echo "=================================================================="
echo "overnight_llm start $(date)"

[ -n "${OPENROUTER_API_KEY:-}" ] || { echo "FATAL: OPENROUTER_API_KEY not set"; exit 1; }
MIN_CREDITS="${MIN_CREDITS:-3}"

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
    c=$(credits)
    echo "-- credit gate: balance=$c (min $MIN_CREDITS)"
    python3 -c "import sys; c='$c'; sys.exit(0 if c=='unknown' or float(c)>=float('$MIN_CREDITS') else 1)" \
        || { echo "-- LOW CREDITS: skipping remaining API stages"; return 1; }
}

stage() {  # stage <name> <cmd...>
    name=$1; shift
    if [ -f "$MARK/$name" ]; then echo "== $name: already done, skipping"; return 0; fi
    echo "== $name: start $(date)"
    if "$@"; then touch "$MARK/$name"; echo "== $name: OK $(date)"
    else echo "== $name: FAILED (continuing to next stage)"; fi
}

# ---------------------------------------------------------------- E1 wait --
echo "== waiting for the in-flight o3 cert63 run (if any)"
while pgrep -f "llm_autoform_o3_cert63" >/dev/null 2>&1; do sleep 120; done
echo "== no o3 cert63 process running $(date)"

# E1 top-up: same command as the main run; row-level resume means this is a
# no-op if the run completed, and finishes the 402-orphaned laws if not.
gate && stage e1_topup \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $RES/easy_chain_harvest.jsonl \
        --model openai/o3 --reasoning-effort medium --rounds 3 --timeout 600 \
        --lean-dir . --out $RES/llm_autoform_o3_cert63.jsonl

# ------------------------------------------------- solved subset (no API) --
build_subset() {
python3 - <<'PY'
import json
solved = set()
for line in open("paper/results/llm_autoform_o3_cert63.jsonl", encoding="utf-8"):
    line = line.strip()
    if not line: continue
    r = json.loads(line)
    if r.get("solved"):
        solved.add(r["law"])
rows = [json.loads(l) for l in open("paper/results/easy_chain_harvest.jsonl", encoding="utf-8") if l.strip()]
keep = [r for r in rows if r.get("law") in solved and r.get("chain")]
with open("paper/results/o3_solved_subset.jsonl", "w", encoding="utf-8") as f:
    for r in keep:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"solved subset: {len(keep)} laws -> paper/results/o3_solved_subset.jsonl")
assert keep, "no solved laws found — E2/E4 have nothing to run on"
PY
}
stage subset build_subset
SUBSET=$RES/o3_solved_subset.jsonl

# ------------------------------------------------- E2: support-down (o3) --
if [ -s "$SUBSET" ]; then
gate && stage e2_nohints \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $SUBSET --hints none \
        --model openai/o3 --reasoning-effort medium --rounds 3 --timeout 600 \
        --lean-dir . --out $RES/llm_autoform_o3_nohints.jsonl
fi

# --------------------------------- E5: construction side, hard-tier (o3) --
build_hard_sample() {
python3 - <<'PY'
import json, random
laws = [json.loads(l)["law"] for l in open("paper/results/final_status.jsonl", encoding="utf-8")
        if '"NO_FINITE_MODEL"' in l]
random.Random(20260720).shuffle(laws)
with open("paper/results/hard25_sample.jsonl", "w", encoding="utf-8") as f:
    for l in laws[:25]:
        f.write(json.dumps({"law": l, "gold": "austin"}, ensure_ascii=False) + "\n")
print(f"hard-tier sample: 25 of {len(laws)} NO_FINITE_MODEL laws (seed 20260720)")
PY
}
stage hard_sample build_hard_sample

stage e5_selftest python3 -B paper/scripts/llm_construct.py --selftest --vampire paper/bin/vampire
gate && stage e5_construct \
    python3 -B paper/scripts/llm_construct.py \
        --laws-file $RES/hard25_sample.jsonl \
        --model openai/o3 --reasoning-effort medium --rounds 3 --timeout 60 \
        --vampire paper/bin/vampire --out $RES/llm_construct_o3_hard25.jsonl

# ------------------------------------------- E3: o4-mini panel on cert63 --
gate && stage e3_o4mini \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $RES/easy_chain_harvest.jsonl \
        --model openai/o4-mini --reasoning-effort medium --rounds 3 --timeout 600 \
        --lean-dir . --out $RES/llm_autoform_o4mini_cert63.jsonl

# ----------------------------------- E4: effort axis, o3 low, solved set --
if [ -s "$SUBSET" ]; then
gate && stage e4_effort_low \
    python3 -B paper/scripts/trivial_autoform.py \
        --laws-file $SUBSET \
        --model openai/o3 --reasoning-effort low --rounds 3 --timeout 600 \
        --lean-dir . --out $RES/llm_autoform_o3_low.jsonl
fi

# ---------------------------------------------------------------- summary --
echo "== SUMMARY $(date)"
python3 - <<'PY'
import json, os
files = {
    "E1 o3 cert63 (hints=full)":   "llm_autoform_o3_cert63.jsonl",
    "E2 o3 solved-set, hints=none":"llm_autoform_o3_nohints.jsonl",
    "E5 o3 hard-tier construct":   "llm_construct_o3_hard25.jsonl",
    "E3 o4-mini cert63":           "llm_autoform_o4mini_cert63.jsonl",
    "E4 o3 solved-set, effort=low":"llm_autoform_o3_low.jsonl",
}
for label, fn in files.items():
    p = os.path.join("paper/results", fn)
    if not os.path.exists(p):
        print(f"{label:34} (not run)"); continue
    rows = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    laws = {}
    for r in rows:                      # last row per law wins
        laws[r.get("law")] = r
    n = len(laws)
    solved = sum(1 for r in laws.values() if r.get("solved"))
    apierr = sum(1 for r in laws.values()
                 if not r.get("solved") and str(r.get("error", "")).startswith("api:"))
    line = f"{label:34} {solved}/{n} solved"
    if apierr: line += f"  ({apierr} api-error rows — rerun to finish)"
    print(line)
PY
echo "overnight_llm end $(date)"
