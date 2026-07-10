#!/bin/bash
# order6_watch.sh — hourly status + auto-requeue.
# Waits for the 60s order6_c_ fmb sweep to finish, then launches the 300s
# fmb-only re-screen over its candidates. Run it WHILE the 60s sweep is active:
#   nohup bash paper/scripts/order6_watch.sh > /dev/null 2>&1 &
#   tail -f paper/results/order6_watch.log
set -u
cd "$(dirname "$0")/../.." || exit 1          # -> repo root
LOG=paper/results/order6_watch.log
PAT='order6_search.py.*order6_c_'
SHARDS=16

echo "$(date) — watcher started; waiting for the 60s sweep ($PAT)" >> "$LOG"

# ---- phase 1: poll hourly until the 60s sweep is gone ----
while pgrep -f "$PAT" > /dev/null; do
    n=$(pgrep -f "$PAT" | wc -l)
    c=$(cat paper/results/order6_c_*.jsonl 2>/dev/null | wc -l)
    done_sh=$(grep -l "Austin candidates" paper/results/order6_c_*.log 2>/dev/null | wc -l)
    echo "$(date) — 60s sweep active: $n shards up, ${done_sh}/${SHARDS} logged-complete, $c raw candidates" >> "$LOG"
    sleep 3600
done

RAW=$(cat paper/results/order6_c_*.jsonl 2>/dev/null | wc -l)
FIN=$(grep -l "Austin candidates" paper/results/order6_c_*.log 2>/dev/null | wc -l)
echo "$(date) — 60s sweep FINISHED. ${FIN}/${SHARDS} shards logged-complete, $RAW raw candidates." >> "$LOG"
if [ "$FIN" -lt "$SHARDS" ]; then
    echo "$(date) — WARNING: only $FIN/$SHARDS shards printed a final line; some may have died early. Re-screening what's present." >> "$LOG"
fi

# ---- phase 2: launch the 300s fmb-only re-screen (the real filter) ----
echo "$(date) — launching 300s fmb-only re-screen ($SHARDS shards)" >> "$LOG"
for i in $(seq 0 $((SHARDS-1))); do
    nohup python -u paper/scripts/order6_rescreen.py \
        --in 'paper/results/order6_c_*.jsonl' \
        --vampire paper/bin/vampire --fmb-timeout 300 --shard "$i/$SHARDS" \
        --out "paper/results/order6_confirmed_$i.jsonl" \
        > "paper/results/order6_rescreen_$i.log" 2>&1 &
done
echo "$(date) — re-screen launched. Watch: cat paper/results/order6_confirmed_*.jsonl | wc -l" >> "$LOG"
echo "$(date) — watcher done (re-screen now running in background)." >> "$LOG"
