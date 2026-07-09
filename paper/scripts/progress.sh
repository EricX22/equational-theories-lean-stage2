#!/bin/bash
# progress.sh — read-only snapshot of an overnight.sh run.
#   bash paper/scripts/progress.sh          one snapshot
#   watch -n60 bash paper/scripts/progress.sh
# Writes nothing, so it is safe to run against a live run.
set -u
cd "$(dirname "$0")/../.." || exit 1
R=${R:-paper/results}

echo "=== stage (last 5 log lines) ==="
tail -5 "$R/overnight.log" 2>/dev/null || echo "no overnight.log yet"

echo
echo "=== running ==="
if pgrep -f overnight.sh > /dev/null; then
    echo "driver:      alive (pid $(pgrep -f 'bash.*overnight.sh' | head -1))"
else
    echo "driver:      NOT running (finished, or died — check the log tail above)"
fi
for s in prove_status.py order6_targeted.py; do
    n=$(pgrep -fc "$s" 2>/dev/null); n=${n:-0}   # pgrep -c prints 0 AND exits 1
    echo "$(printf '%-22s' "$s") $n shard(s)"
done
nv=$(pgrep -c vampire 2>/dev/null); echo "vampire procs: ${nv:-0}"
echo "load:          $(cut -d' ' -f1-3 /proc/loadavg)"

echo
echo "=== laws classified per stage ==="
shopt -s nullglob
for pre in o5_status tgt_status r1_status r2_status r3_status retry_status; do
    files=("$R/${pre}"_*.jsonl)
    [ ${#files[@]} -eq 0 ] && continue
    printf '%-14s %6d laws' "$pre" "$(cat "${files[@]}" | wc -l)"
    printf '   (%s)\n' "$(cat "${files[@]}" | python3 -c "
import sys,json,collections
c=collections.Counter(json.loads(l)['status'] for l in sys.stdin if l.strip())
print(' '.join(f'{k}={v}' for k,v in sorted(c.items(), key=lambda kv:-kv[1])))" 2>/dev/null)"
done
for pre in r1_pool r2_pool r3_pool; do
    files=("$R/${pre}"_*.jsonl)
    [ ${#files[@]} -gt 0 ] && printf '%-14s %6d candidates generated\n' "$pre" "$(cat "${files[@]}" | wc -l)"
done

echo
echo "=== corpus so far (merged, strongest verdict per law) ==="
python3 paper/scripts/status_report.py "$R/*_status_*.jsonl" 2>/dev/null | sed -n '1,20p' \
    || echo "nothing classified yet"

echo
echo "=== throughput ==="
newest=$(ls -t "$R"/*_status_*.jsonl 2>/dev/null | head -1)
if [ -n "${newest:-}" ]; then
    echo "last write:  $(date -r "$newest" '+%F %T')  ($newest)"
    echo "certs:       $(ls paper/certs/saturation/*.sat 2>/dev/null | wc -l) existence proofs saved"
    echo "recent secs/law (last 20):"
    tail -q -n 20 "$newest" | python3 -c "
import sys,json
v=[json.loads(l)['secs'] for l in sys.stdin if l.strip()]
print(f'  n={len(v)} mean={sum(v)/len(v):.1f}s max={max(v):.1f}s' if v else '  (none)')"
fi

echo
echo "=== errors (any shard) ==="
grep -lE 'Traceback|FATAL|MemoryError' "$R"/*_status_*.log "$R"/*_gen_*.log 2>/dev/null | head -5 \
    || echo "none"
