#!/usr/bin/env bash
# resume_sweep.sh — restart the frozen hard-tier sweep WITHOUT losing completed work.
#
# Why this exists: `run_remaining.sh sweep` TRUNCATES baseline_full.jsonl before
# launching (": > $OUT" — shards append, no resume logic), so re-running it would
# destroy the ~129k rows already computed. This script instead:
#   1. backs up the current file to baseline_full.part1.jsonl (once; never overwrites)
#   2. builds remaining_input.jsonl = NO_FINITE_MODEL laws not yet finished
#      (finished = resolved with a verdict, OR walked the full ladder to 600s)
#   3. launches shards into a FRESH baseline_full.part2.jsonl
# In-flight laws that were only partially swept when the run died are re-run in
# full in part2; `merge` drops their partial part1 rows so nothing double-counts.
#
# Usage (on the cluster, from anywhere; same conventions as run_remaining.sh):
#   bash paper/scripts/resume_sweep.sh resume   # backup + build remaining set + launch
#   bash paper/scripts/resume_sweep.sh merge    # AFTER completion: rebuild canonical baseline_full.jsonl
#
# Env overrides: SHARDS (default nproc — use the same count as the original run),
#                VAMPIRE (default paper/bin/vampire)
set -u -o pipefail
cd "$(dirname "$0")/../.." || exit 1
R=paper/results
VAMPIRE=${VAMPIRE:-paper/bin/vampire}
EPROVER=$(command -v eprover || true)
TWEE=$(command -v twee || true)
SHARDS=${SHARDS:-$(nproc)}

case ${1:-resume} in

resume)
  if pgrep -f "baseline_probe.py.*--out" >/dev/null; then
    echo "a baseline_probe.py is still running — stop it before resuming"; exit 1
  fi
  [[ -x "$VAMPIRE" ]] || { echo "vampire not at $VAMPIRE"; exit 1; }
  [[ -n "$EPROVER" && -n "$TWEE" ]] || { echo "eprover/twee missing — install per RUNBOOK §1 first"; exit 1; }
  echo "selftest first (refuses to run otherwise)…"
  python3 paper/scripts/baseline_probe.py --selftest --vampire "$VAMPIRE" \
      --eprover "$EPROVER" --twee "$TWEE" | grep -q "SELFTEST OK" \
      || { echo "SELFTEST FAILED — stopping"; exit 1; }

  # 1) preserve completed work (idempotent: never overwrite an existing backup)
  [[ -f "$R/baseline_full.part1.jsonl" ]] || cp "$R/baseline_full.jsonl" "$R/baseline_full.part1.jsonl"

  # 2) remaining-laws input
  python3 - <<'PY'
import json
resolved, seen600 = set(), set()
for l in open('paper/results/baseline_full.part1.jsonl'):
    if not l.strip(): continue
    r = json.loads(l)
    if r.get('verdict'): resolved.add(r['law'])
    if r.get('budget') == 600: seen600.add(r['law'])
done = resolved | seen600
kept = 0
with open('paper/results/remaining_input.jsonl', 'w') as out:
    for l in open('paper/results/final_status.jsonl'):
        if not l.strip(): continue
        r = json.loads(l)
        if r.get('status') == 'NO_FINITE_MODEL' and r['law'] not in done:
            out.write(l); kept += 1
print(f'remaining laws to sweep: {kept}  '
      f'(already finished: {len(done)} = {len(resolved)} resolved '
      f'+ {len(done - resolved)} full-ladder unresolved)')
PY

  # 3) launch shards into a fresh part-2 file (NEVER touches baseline_full.jsonl)
  echo "launching $SHARDS shards over remaining laws -> $R/baseline_full.part2.jsonl"
  for i in $(seq 0 $((SHARDS-1))); do
    nohup python3 paper/scripts/baseline_probe.py \
      --in "$R/remaining_input.jsonl" --status NO_FINITE_MODEL \
      --vampire "$VAMPIRE" --eprover "$EPROVER" --twee "$TWEE" \
      --budgets 30,60,120,300,600 --n 0 --shard "$i/$SHARDS" \
      --out "$R/baseline_full.part2.jsonl" --certs paper/certs/baseline \
      >> "$R/sweep2_$i.log" 2>&1 &
  done
  echo "watch progress:  wc -l $R/baseline_full.part2.jsonl"
  echo "live shards:     pgrep -cf baseline_probe.py"
  ;;

merge)
  if pgrep -f "baseline_probe.py.*--out" >/dev/null; then
    echo "shards still running — merge only after completion"; exit 1
  fi
  python3 - <<'PY'
import json
p2 = [l for l in open('paper/results/baseline_full.part2.jsonl') if l.strip()]
laws2 = {json.loads(l)['law'] for l in p2}
n1 = n2 = 0
with open('paper/results/baseline_full.jsonl', 'w') as out:
    for l in open('paper/results/baseline_full.part1.jsonl'):
        if l.strip() and json.loads(l)['law'] not in laws2:
            out.write(l); n1 += 1
    for l in p2:
        out.write(l); n2 += 1
print(f'merged: {n1} part1 rows + {n2} part2 rows -> baseline_full.jsonl')
PY
  python3 paper/scripts/baseline_probe.py --curve "$R/baseline_full.jsonl"
  echo "# baseline_full.jsonl is canonical again; unresolved laws are the hard-tier membership list."
  ;;

*)
  echo "usage: bash paper/scripts/resume_sweep.sh {resume|merge}"
  ;;
esac
