#!/usr/bin/env bash
# Read-only snapshot of an overnight run_all.sh (NOT overnight.sh — that's progress.sh).
#   bash paper/scripts/progress_runall.sh
#   watch -n120 bash paper/scripts/progress_runall.sh
# Touches nothing; safe on a live run.
set -u
cd "$(dirname "$0")/../.." || exit 1
R=${R:-paper/results}

echo "=== stages ==="
ls "$R/.done" 2>/dev/null | sed 's/^/  done: /'
echo "  now : $(cat $R/.current 2>/dev/null || echo idle)"
if pgrep -f run_all.sh >/dev/null; then echo "  driver: alive"; else echo "  driver: not running (done or died)"; fi
nb=$(pgrep -fc baseline_probe.py 2>/dev/null); echo "  baseline shards: ${nb:-0}   load: $(cut -d' ' -f1-3 /proc/loadavg)"
last=$(stat -c %Y "$R/run_all.log" 2>/dev/null)
[[ -n "$last" ]] && age=$(( ($(date +%s) - last) / 60 )) && \
    echo "  log age: ${age} min$( [[ $age -gt 90 ]] && echo '   <- STALE, check for a wedge' )"

echo; echo "=== equivalence census (the abstract's number) ==="
if [[ -s "$R/classes.json" ]]; then
    python3 - "$R/classes.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
m = d['n'] - d['classes']
print(f"  {d['n']} laws -> <= {d['classes']} classes  ({m} merges, "
      f"{100*m/d['n']:.0f}% collapse)  [upper bound @ {d['budget']}s]")
PY
else echo "  not finished yet"; fi

echo; echo "=== baseline / budget curve ==="
bl="$R/baseline_v1.jsonl"
if [[ -s "$bl" ]]; then
    python3 - "$bl" <<'PY'
import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
laws = {r["law"] for r in rows}
print(f"  {len(rows)} prover-calls / {len(laws)} laws")
byc = collections.Counter(r["config"] for r in rows if r["verdict"])
if byc:
    print("  resolutions by config (a nonzero TWEE row => hard tier may be Vampire-bound):")
    for c, n in byc.most_common():
        print(f"    {c:26s} {n}")
else:
    print("  no resolutions yet (expected on the hard tier)")
seen, res = collections.defaultdict(set), collections.defaultdict(set)
for r in rows:
    seen[r["budget"]].add(r["law"])
    if r["verdict"]: res[r["budget"]].add(r["law"])
print("  rate by budget (delta should FLATTEN if method-bound):")
prev = None
for b in sorted(seen):
    rate = len(res[b]) / len(seen[b]); d = "" if prev is None else f"  d={rate-prev:+.3f}"
    print(f"    {b:4d}s  {len(res[b]):3d}/{len(seen[b]):3d} = {rate:.3f}{d}"); prev = rate
PY
else echo "  not started (runs after census; or portfolio incomplete)"; fi

echo; echo "=== gates ==="
grep -E "GATE|PROVISIONAL|NOT RUNNABLE|twee (emits|prose)|portfolio signature|SELFTEST" \
    "$R/run_all.log" 2>/dev/null | tail -6
