#!/bin/bash
# overnight.sh — one command: prove what we have, generate more, prove that too.
#
#   nohup bash paper/scripts/overnight.sh > /dev/null 2>&1 &
#   tail -f paper/results/overnight.log
#
# Stages
#   0  preflight (vampire, python, parse-check every script — the mount truncates)
#   1  STATUS   classify the graded order-5 corpus            (long timeouts)
#   2  STATUS   classify any existing targeted order-6 pool   (long timeouts)
#   3  HARVEST  ROUNDS x [ extend proved-Austin seeds by one op -> cheap screen
#               -> classify the new laws ]  (each round's proved laws seed the next)
#   4  RETRY    everything still unsettled, at a long timeout + fmb
#   5  REPORT   merged trichotomy + the benchmark gold set
#
# Every stage is wall-clocked (`timeout`), and prove_status.py flushes one line per
# law, so a stage that runs out of time still contributes everything it proved.
# Re-running resumes: --skip drops laws already classified.
#
# Knobs (env):
#   SHARDS=32  TMO_FAST=20  TMO_SLOW=120  TMO_HARD=300  ROUNDS=2  SEED_CAP=400
#   S1_MAX/S2_MAX/S3_MAX/S4_MAX = per-stage wall seconds
set -u
cd "$(dirname "$0")/../.." || exit 1

R=${R:-paper/results}   # override for smoke tests: R=/tmp/rt bash paper/scripts/overnight.sh
LOG=$R/overnight.log
V=paper/bin/vampire
CERTS=paper/certs/saturation

SHARDS=${SHARDS:-$(nproc 2>/dev/null || echo 16)}
[ "$SHARDS" -gt 32 ] && SHARDS=32
TMO_FAST=${TMO_FAST:-20}      # per-prover, harvest pass (many laws)
TMO_SLOW=${TMO_SLOW:-120}     # per-prover, curated corpora
TMO_HARD=${TMO_HARD:-300}     # per-prover, final retry on the stubborn ones
ROUNDS=${ROUNDS:-2}
SEED_CAP=${SEED_CAP:-400}
S1_MAX=${S1_MAX:-3600}
S2_MAX=${S2_MAX:-7200}
S3_MAX=${S3_MAX:-10800}       # per round
S4_MAX=${S4_MAX:-10800}

mkdir -p "$R" "$CERTS"
say () { echo "$(date '+%F %T') — $*" | tee -a "$LOG"; }

# ---------------------------------------------------------------- preflight --
say "preflight: SHARDS=$SHARDS TMO_FAST=$TMO_FAST TMO_SLOW=$TMO_SLOW TMO_HARD=$TMO_HARD ROUNDS=$ROUNDS"
[ -x "$V" ] || { say "FATAL: no vampire at $V"; exit 1; }
for f in prove_status.py status_report.py seeds_from_status.py order6_targeted.py; do
    python3 -m py_compile "paper/scripts/$f" 2>>"$LOG" \
        || { say "FATAL: $f does not parse (mount truncation?) — re-sync and rerun"; exit 1; }
done
"$V" --version >/dev/null 2>&1 || { say "FATAL: vampire will not run"; exit 1; }
# A truncated python file still COMPILES (it just loses its `main()` call and exits
# 0 doing nothing) — that would burn the whole night. So run the provers on laws
# with known answers before trusting anything.
python3 -u paper/scripts/prove_status.py --selftest "$V" 2>&1 | tee -a "$LOG" | grep -q "SELFTEST OK" \
    || { say "FATAL: prove_status selftest failed"; exit 1; }
say "preflight OK"

# --------------------------------------------------------------- primitives --
wait_for () {  # $1 = pgrep pattern, $2 = label, $3 = glob to count
    sleep 15
    while pgrep -f "$1" > /dev/null; do
        say "$2: $(cat $3 2>/dev/null | wc -l) laws done"
        sleep 600
    done
}

# classify <input-glob> <out-prefix> <per-prover timeout> <fmb timeout> <stage wall>
classify () {
    local IN="$1" OUT="$2" TMO="$3" FMB="$4" WALL="$5"
    say "classify -> ${OUT}_*.jsonl  (tmo=${TMO}s fmb=${FMB}s wall=${WALL}s)"
    for i in $(seq 0 $((SHARDS-1))); do
        nohup timeout "$WALL" python3 -u paper/scripts/prove_status.py \
            --in "$IN" --out "$R/${OUT}_$i.jsonl" --vampire "$V" \
            --trivial-timeout "$TMO" --i-timeout "$TMO" --sat-timeout "$TMO" \
            --fmb-timeout "$FMB" --cert-dir "$CERTS" --baseline \
            --skip "$R/*_status_*.jsonl" --shard "$i/$SHARDS" \
            > "$R/${OUT}_$i.log" 2>&1 &
    done
    wait_for "prove_status.py .*${OUT}_" "$OUT" "$R/${OUT}_*.jsonl"
    say "$OUT done:"
    python3 paper/scripts/status_report.py "$R/${OUT}_*.jsonl" | tee -a "$LOG"
}

# ------------------------------------------------- 1/2. classify what we have -
# order-5: ETP already established "no finite model", so don't pay for fmb.
if ls $R/o5_graded_*.jsonl >/dev/null 2>&1; then
    classify "$R/o5_graded_*.jsonl" o5_status "$TMO_SLOW" 0 "$S1_MAX"
else
    say "skip stage 1: no o5_graded_*.jsonl"
fi

# order-6 targeted candidates from the earlier pipeline: these are self-generated,
# so a finite model may well exist -> fmb is a real check, not a formality.
if ls $R/tgt_austin_*.jsonl >/dev/null 2>&1; then
    classify "$R/tgt_austin_*.jsonl" tgt_status "$TMO_SLOW" 120 "$S2_MAX"
else
    say "skip stage 2: no tgt_austin_*.jsonl"
fi

# ------------------------------------------------------------- 3. harvest loop -
for r in $(seq 1 "$ROUNDS"); do
    SEEDS=$R/seeds_r$r.jsonl
    say "ROUND $r: selecting seeds (proved no-finite-model laws)"
    python3 paper/scripts/seeds_from_status.py --in "$R/*_status_*.jsonl" \
        --status AUSTIN_PROVEN NO_FINITE_MODEL --max "$SEED_CAP" --out "$SEEDS" \
        | tee -a "$LOG"
    n=$(wc -l < "$SEEDS")
    if [ "$n" -lt 2 ]; then say "ROUND $r: only $n seeds, stopping harvest"; break; fi

    say "ROUND $r: generating one-op extensions + cheap n<=3 screen"
    for i in $(seq 0 $((SHARDS-1))); do
        nohup python3 -u paper/scripts/order6_targeted.py \
            --seeds-in "$SEEDS" --out "$R/r${r}_pool_$i.jsonl" --shard "$i/$SHARDS" \
            > "$R/r${r}_gen_$i.log" 2>&1 &
    done
    wait_for "order6_targeted.py .*r${r}_pool_" "round $r generation" "$R/r${r}_pool_*.jsonl"
    say "ROUND $r: $(cat $R/r${r}_pool_*.jsonl 2>/dev/null | wc -l) candidates survived the cheap screen"

    classify "$R/r${r}_pool_*.jsonl" "r${r}_status" "$TMO_FAST" 60 "$S3_MAX"
done

# --------------------------------------------------------------- 4. hard retry -
say "RETRY: collecting everything still unsettled"
python3 paper/scripts/seeds_from_status.py --in "$R/*_status_*.jsonl" \
    --unsettled --out "$R/unsettled.jsonl" | tee -a "$LOG"
if [ "$(wc -l < "$R/unsettled.jsonl")" -gt 0 ]; then
    # deliberately NOT skipping: this pass is allowed to re-decide the same laws
    say "RETRY -> retry_status_*.jsonl (tmo=${TMO_HARD}s fmb=${TMO_HARD}s)"
    for i in $(seq 0 $((SHARDS-1))); do
        nohup timeout "$S4_MAX" python3 -u paper/scripts/prove_status.py \
            --in "$R/unsettled.jsonl" --out "$R/retry_status_$i.jsonl" --vampire "$V" \
            --trivial-timeout "$TMO_HARD" --i-timeout "$TMO_HARD" --sat-timeout "$TMO_HARD" \
            --fmb-timeout "$TMO_HARD" --cert-dir "$CERTS" --baseline --shard "$i/$SHARDS" \
            > "$R/retry_status_$i.log" 2>&1 &
    done
    wait_for "prove_status.py .*retry_status_" "retry" "$R/retry_status_*.jsonl"
fi

# ------------------------------------------------------------------ 5. report -
say "FINAL REPORT (merged; strongest verdict per law wins)"
python3 paper/scripts/status_report.py "$R/*_status_*.jsonl" \
    --merge-out "$R/final_status.jsonl" --gold-out "$R/gold.jsonl" | tee -a "$LOG"
say "ALL DONE. corpus: $R/final_status.jsonl | gold: $R/gold.jsonl | certs: $CERTS"
