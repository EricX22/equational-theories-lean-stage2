#!/usr/bin/env bash
# Run the RUNBOOK end to end, after any live pipeline finishes.
#
#   nohup bash paper/scripts/run_all.sh > /dev/null 2>&1 &
#   tail -f paper/results/run_all.log
#   bash paper/scripts/run_all.sh --status        # read-only, safe on a live run
#
# Design notes, all learned the hard way:
#   * Stages are idempotent. A completed stage drops a marker in results/.done and is
#     skipped on re-run. Delete the marker to force a redo.
#   * Nothing here matches overnight.sh's pgrep patterns (`prove_status.py .*_status_`),
#     so it will not confuse its wait_for. We still wait for it, for the CPU.
#   * A stage that FAILS does not stop the script, except the two gates below, which
#     invalidate everything downstream of them.
#   * Heartbeat every HEARTBEAT seconds: which stage, how long, how many rows out.
#
# Env: SHARDS BUDGETS HEARTBEAT SAMPLE_N VAMPIRE
set -u -o pipefail

cd "$(dirname "$0")/../.." || exit 1
# Same convention as overnight.sh: R=/tmp/rt smoke-tests into a scratch results dir.
R=${R:-paper/results}
IN=${IN:-$R/final_status.jsonl}
D=$R/.done
LOG=$R/run_all.log
mkdir -p "$D" "$R" paper/certs/baseline

SHARDS=${SHARDS:-$(nproc)}
BUDGETS=${BUDGETS:-30,60,120,300,600}
HEARTBEAT=${HEARTBEAT:-3600}
SAMPLE_N=${SAMPLE_N:-250}
# The budget curve is a RATE. A few hundred hard-tier laws measure it as well as 3,428,
# and the full sweep costs ~5550 core-seconds PER LAW (nothing resolves, so every law
# walks the whole ladder): ~5,300 core-hours, ~7 days on 32 cores. BASELINE_N=0 for all.
BASELINE_N=${BASELINE_N:-300}
# A portfolio missing E/Twee cannot produce a publishable hard tier. Refuse by default.
ALLOW_PROVISIONAL=${ALLOW_PROVISIONAL:-0}
VAMPIRE=${VAMPIRE:-paper/bin/vampire}
EPROVER=$(command -v eprover || true)
TWEE=$(command -v twee || true)
LEAN_OK=$(command -v lake >/dev/null && echo 1 || echo 0)

say () { echo "$(date '+%F %T') — $*" | tee -a "$LOG"; }
have () { [[ -f "$D/$1" ]]; }
mark () { touch "$D/$1"; }

# A path on PATH is not a working prover. `curl -o twee <wrong-url>` leaves an HTML page
# that is executable and dies with "Exec format error"; a macOS build does the same. An
# unrunnable binary produces no output, which downstream looks exactly like "this prover
# resolved nothing" — a failure in the flattering direction. Check before trusting.
runnable () {   # $1 = path, $2 = name
    [[ -n "$1" ]] || return 1
    if ! "$1" --version >/dev/null 2>&1 && ! "$1" -h >/dev/null 2>&1; then
        say "  $2 at $1 is NOT RUNNABLE ($(file -b "$1" 2>/dev/null | cut -c1-60))"
        return 1
    fi
    return 0
}

if [[ "${1:-}" == "--status" ]]; then
    echo "stages done: $(ls "$D" 2>/dev/null | tr '\n' ' ')"
    echo "running    : $(cat $R/.current 2>/dev/null || echo none)"
    tail -5 "$LOG" 2>/dev/null
    exit 0
fi

# --- wait for any live pipeline (CPU, not correctness) -----------------------
wait_for_pipeline () {
    local waited=0
    while pgrep -f "prove_status.py .*_status_" >/dev/null \
       || pgrep -f "order6_targeted.py .*_pool_" >/dev/null; do
        [[ $waited -eq 0 ]] && say "waiting for the live pipeline to finish…"
        sleep 60; waited=$((waited+60))
    done
    [[ $waited -gt 0 ]] && say "pipeline finished after ${waited}s of waiting"
    return 0
}

# --- heartbeat ---------------------------------------------------------------
# NOTE: writes to the LOG only, never to stdout, and is started with stdout closed.
# A background child that inherits stdout keeps `run_all.sh | tee` open forever: the
# pipeline never sees EOF even after the script exits.
heartbeat () {
    while true; do
        sleep "$HEARTBEAT"
        local cur rows
        cur=$(cat $R/.current 2>/dev/null || echo idle)
        rows=$(wc -l < $R/baseline_v1.jsonl 2>/dev/null || echo 0)
        echo "$(date '+%F %T') — heartbeat: stage=$cur baseline_rows=$rows" \
             "load=$(cut -d' ' -f1-3 /proc/loadavg)" >> "$LOG"
    done
}

stage () { echo "$1" > $R/.current; say "STAGE $1"; }

# =============================================================================
say "run_all starting. shards=$SHARDS budgets=$BUDGETS heartbeat=${HEARTBEAT}s"
say "provers: vampire=$VAMPIRE eprover=${EPROVER:-MISSING} twee=${TWEE:-MISSING} lean=$LEAN_OK"
runnable "$VAMPIRE" vampire || { say "vampire is unusable — stopping"; exit 1; }
runnable "$EPROVER" eprover || EPROVER=""
runnable "$TWEE"    twee    || TWEE=""
[[ -z "$EPROVER" || -z "$TWEE" ]] && say "WARNING: portfolio incomplete — any hard-tier claim from this run is PROVISIONAL"

wait_for_pipeline
heartbeat >/dev/null 2>&1 & HB=$!
trap 'kill $HB 2>/dev/null; echo idle > $R/.current' EXIT

# --- GATE 1: the answer format ----------------------------------------------
# If Lean cannot check the reference proof, "verification" is not closed and every
# downstream number is about a benchmark nobody can grade.
if ! have answer_spec; then
    stage answer_spec
    if [[ $LEAN_OK == 1 ]]; then
        if python3 paper/scripts/answer_spec.py --selftest --lean-dir . 2>&1 | tee -a "$LOG" \
             | grep -q "SELFTEST OK"; then
            mark answer_spec; say "answer format verified end to end"
        else
            say "GATE 1 FAILED: the judge does not round-trip through Lean. STOPPING."
            exit 1
        fi
    else
        say "GATE 1 SKIPPED: no lake on PATH. Textual gates only; format UNVERIFIED."
    fi
fi

# --- GATE 2: Twee's real output strings --------------------------------------
# baseline_probe::_verdict matches guessed strings. Wrong strings => Twee silently
# resolves nothing => the hard tier looks robust. Failure in the flattering direction.
if [[ -n "$TWEE" ]] && ! have twee_strings; then
    stage twee_strings
    python3 - <<'PY' > /tmp/4916.p
import sys; sys.path.insert(0,"paper/scripts")
import etp_terms as et
print(et.tptp_true("x = y ◇ (x ◇ (x ◇ (y ◇ (z ◇ z))))", "x = y"))
PY
    "$TWEE" /tmp/4916.p > $R/twee_4916.out 2>&1
    say "twee output saved to $R/twee_4916.out — READ IT BY EYE"
    # 4916 is Austin: it does NOT entail x=y, so a complete run must report
    # CounterSatisfiable (SZS), or say so in prose. Anything else and _verdict is blind.
    if grep -qE "SZS status (CounterSatisfiable|Satisfiable)" $R/twee_4916.out; then
        mark twee_strings; say "twee emits SZS status — _verdict reads it directly"
    elif grep -qE "Ran out of critical pairs|conjecture is (true|false)|Goal is true" \
             $R/twee_4916.out; then
        mark twee_strings; say "twee prose recognised (no SZS line; consider --tstp)"
    else
        say "GATE 2 FAILED: none of the expected strings appear. Fix _verdict before"
        say "  trusting the twee column. Continuing WITHOUT twee."
        TWEE=""
    fi
fi

# --- cheap analyses (no prover) ----------------------------------------------
if ! have retry_curve; then
    stage retry_curve
    python3 paper/scripts/retry_curve.py --results $R --out $R/retry_curve.json 2>&1 | tee -a "$LOG"
    mark retry_curve
fi

# --- the baseline: the gate for the hard tier --------------------------------
if ! have baseline_selftest; then
    stage baseline_selftest
    if python3 paper/scripts/baseline_probe.py --selftest --vampire "$VAMPIRE" \
         ${EPROVER:+--eprover "$EPROVER"} ${TWEE:+--twee "$TWEE"} 2>&1 | tee -a "$LOG" \
         | grep -q "SELFTEST OK"; then
        mark baseline_selftest
    else
        say "baseline selftest FAILED — refusing to run the portfolio"; exit 1
    fi
fi

if ! have baseline; then
    if [[ -z "$EPROVER" || -z "$TWEE" ]] && [[ "$ALLOW_PROVISIONAL" != "1" ]]; then
        say "SKIPPING baseline. The portfolio is not usable, so the hard tier it"
        say "  produces cannot be published. Missing or disqualified:"
        [[ -z "$EPROVER" ]] && say "    eprover — not on PATH (RUNBOOK §1)"
        [[ -z "$TWEE"    ]] && say "    twee — either not on PATH, or INSTALLED BUT"
        [[ -z "$TWEE"    ]] && say "      DISQUALIFIED by Gate 2 (its output strings do"
        [[ -z "$TWEE"    ]] && say "      not match _verdict; see $R/twee_4916.out)"
        say "  Re-run with ALLOW_PROVISIONAL=1 for a Vampire-only curve, knowingly."
    else
    stage baseline
    say "baseline: sampling ${BASELINE_N:-all} laws (the curve is a rate, not a census)"
    # Collect shard PIDs and wait on THOSE. A bare `wait` also waits for the heartbeat
    # child, which never exits — the stage would hang forever.
    pids=()
    for i in $(seq 0 $((SHARDS-1))); do
        python3 paper/scripts/baseline_probe.py \
            --in "$IN" --status NO_FINITE_MODEL \
            --vampire "$VAMPIRE" ${EPROVER:+--eprover "$EPROVER"} ${TWEE:+--twee "$TWEE"} \
            --budgets "$BUDGETS" --n "$BASELINE_N" --shard "$i/$SHARDS" \
            --out $R/baseline_v1.jsonl --certs paper/certs/baseline \
            >> $R/baseline_$i.log 2>&1 &
        pids+=($!)
    done
    wait "${pids[@]}"
    rows=$(wc -l < $R/baseline_v1.jsonl 2>/dev/null || echo 0)
    if [[ "$rows" -eq 0 ]]; then
        say "baseline produced 0 rows — NOT marking done; see $R/baseline_*.log"
    else
        mark baseline
        say "baseline done: $rows rows"
        python3 paper/scripts/baseline_probe.py --curve $R/baseline_v1.jsonl 2>&1 | tee -a "$LOG"
    fi
    fi   # end: portfolio-complete guard
fi

# --- corpus hygiene ----------------------------------------------------------
if ! have equiv_sample; then
    stage equiv_sample
    python3 paper/scripts/equiv_sample.py --in "$IN" \
        --status AUSTIN_PROVEN --n "$SAMPLE_N" --vampire "$VAMPIRE" \
        --sat-timeout 20 --prove-timeout 30 --certs /tmp/eqcerts \
        --out $R/classes.json 2>&1 | tee -a "$LOG"
    mark equiv_sample
fi

# --- the contribution --------------------------------------------------------
if [[ $LEAN_OK == 1 ]] && ! have lean_model; then
    stage lean_model
    lake env lean paper/lean/OrderedModel.lean > $R/lean_model.log 2>&1
    if grep -q "error:" $R/lean_model.log; then
        say "OrderedModel.lean does not elaborate yet — see $R/lean_model.log"
        say "  (expected: this file has never been compiled)"
    else
        mark lean_model
        say "OrderedModel.lean elaborates. Remaining sorry: ground_confluent = the paper."
    fi
fi

stage done
say "ALL DONE. gates: answer_spec=$(have answer_spec && echo ok || echo skipped/failed)"
for f in retry_curve.json baseline_v1.jsonl classes.json lean_model.log; do
    [[ -s "$R/$f" ]] && say "  $R/$f  ($(wc -l < "$R/$f") lines)"
done
have baseline || say "  baseline: NOT RUN (portfolio incomplete; see RUNBOOK §1)"
