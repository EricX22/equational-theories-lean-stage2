#!/bin/bash
# order6_targeted_finish.sh — full automated TARGETED pipeline:
#   generate (extend known Austin laws) -> trivial-strip -> confirm+grade -> rungs.
# High Austin yield vs random. Recursively re-seedable (feed tgt_graded back in).
#   nohup bash paper/scripts/order6_targeted_finish.sh > /dev/null 2>&1 &
#   tail -f paper/results/order6_targeted_finish.log
set -u
cd "$(dirname "$0")/../.." || exit 1
LOG=paper/results/order6_targeted_finish.log
SHARDS=16
wait_for () {   # $1 = process pattern, $2 = human label, $3 = watch-file glob
    sleep 20
    while pgrep -f "$1" > /dev/null; do
        echo "$(date) — $2: $(cat $3 2>/dev/null | wc -l) so far" >> "$LOG"; sleep 1200
    done
}

echo "$(date) — STAGE 0: targeted generation" >> "$LOG"
for i in $(seq 0 $((SHARDS-1))); do
    nohup python -u paper/scripts/order6_targeted.py \
        --out "paper/results/tgt_pool_$i.jsonl" --shard "$i/$SHARDS" \
        > "paper/results/tgt_gen_$i.log" 2>&1 &
done
wait_for order6_targeted.py "generating" "paper/results/tgt_pool_*.jsonl"
echo "$(date) — generated $(cat paper/results/tgt_pool_*.jsonl 2>/dev/null | wc -l) candidates" >> "$LOG"

echo "$(date) — STAGE 1: trivial-strip" >> "$LOG"
for i in $(seq 0 $((SHARDS-1))); do
    nohup python -u paper/scripts/order6_strip_trivial.py \
        --in 'paper/results/tgt_pool_*.jsonl' --vampire paper/bin/vampire \
        --prove-timeout 10 --shard "$i/$SHARDS" \
        --out "paper/results/tgt_austin_$i.jsonl" > "paper/results/tgt_strip_$i.log" 2>&1 &
done
wait_for order6_strip_trivial.py "stripping" "paper/results/tgt_austin_*.jsonl"
echo "$(date) — $(cat paper/results/tgt_austin_*.jsonl 2>/dev/null | wc -l) non-trivial" >> "$LOG"

echo "$(date) — STAGE 2: confirm+grade" >> "$LOG"
for i in $(seq 0 $((SHARDS-1))); do
    nohup python -u paper/scripts/order6_grade.py \
        --in 'paper/results/tgt_austin_*.jsonl' --vampire paper/bin/vampire \
        --fmb-timeout 300 --shard "$i/$SHARDS" \
        --out "paper/results/tgt_graded_$i.jsonl" > "paper/results/tgt_grade_$i.log" 2>&1 &
done
wait_for order6_grade.py "grading" "paper/results/tgt_graded_*.jsonl"
echo "$(date) — DONE. rung counts:" >> "$LOG"
cat paper/results/tgt_graded_*.jsonl 2>/dev/null \
  | python3 -c "import sys,json,collections;print(dict(sorted(collections.Counter(json.loads(l)['rung'] for l in sys.stdin).items())))" >> "$LOG" 2>&1
