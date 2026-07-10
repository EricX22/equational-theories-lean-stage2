#!/bin/bash
# order6_finish.sh — fully automated order-6 tail:
#   trivial-strip (drop ~99% trivial) -> confirm+grade (fmb + TI + greedy -> rung).
# Run it AFTER the 60s sweep produced paper/results/order6_c_*.jsonl (and after
# pkill -f order6_rescreen). One command, unattended:
#   nohup bash paper/scripts/order6_finish.sh > /dev/null 2>&1 &
#   tail -f paper/results/order6_finish.log
set -u
cd "$(dirname "$0")/../.." || exit 1
LOG=paper/results/order6_finish.log
SHARDS=16

echo "$(date) — STAGE 1: trivial-strip ($SHARDS shards)" >> "$LOG"
for i in $(seq 0 $((SHARDS-1))); do
    nohup python -u paper/scripts/order6_strip_trivial.py \
        --in 'paper/results/order6_c_*.jsonl' --vampire paper/bin/vampire \
        --prove-timeout 10 --shard "$i/$SHARDS" \
        --out "paper/results/order6_austin_$i.jsonl" \
        > "paper/results/order6_strip_$i.log" 2>&1 &
done

sleep 30
while pgrep -f order6_strip_trivial.py > /dev/null; do
    k=$(cat paper/results/order6_austin_*.jsonl 2>/dev/null | wc -l)
    echo "$(date) — strip running: $k non-trivial kept so far" >> "$LOG"
    sleep 1800
done
KEPT=$(cat paper/results/order6_austin_*.jsonl 2>/dev/null | wc -l)
echo "$(date) — strip done: $KEPT non-trivial Austin candidates." >> "$LOG"

echo "$(date) — STAGE 2: confirm+grade ($SHARDS shards, fmb 300s + TI + greedy)" >> "$LOG"
for i in $(seq 0 $((SHARDS-1))); do
    nohup python -u paper/scripts/order6_grade.py \
        --in 'paper/results/order6_austin_*.jsonl' \
        --vampire paper/bin/vampire --fmb-timeout 300 --shard "$i/$SHARDS" \
        --out "paper/results/order6_graded_$i.jsonl" \
        > "paper/results/order6_grade_$i.log" 2>&1 &
done

sleep 30
while pgrep -f order6_grade.py > /dev/null; do
    n=$(cat paper/results/order6_graded_*.jsonl 2>/dev/null | wc -l)
    echo "$(date) — grading running: $n confirmed+graded so far" >> "$LOG"
    sleep 1800
done
echo "$(date) — DONE. Final graded corpus: paper/results/order6_graded_*.jsonl" >> "$LOG"
echo "$(date) — rung counts:" >> "$LOG"
cat paper/results/order6_graded_*.jsonl 2>/dev/null \
  | python3 -c "import sys,json,collections;c=collections.Counter(json.loads(l)['rung'] for l in sys.stdin);print(dict(sorted(c.items())))" >> "$LOG" 2>&1
