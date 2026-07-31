#!/usr/bin/env bash
# run_remaining.sh — the three experiments left after the numbers were finalized
# (2026-07-14). Run on the real machine (provers + Lean required; none of this runs in
# the Cowork sandbox). Grounded in the actual CLIs of baseline_probe / answer_spec /
# lean_oracle / ordered_model / attic/proposer_o3, but NOT tested here — read the echoes.
#
# Prereqs (see RUNBOOK §1): vampire at paper/bin/vampire, eprover + twee on PATH, and
# `lake` on PATH for the Lean checks. Portfolio install is unchanged from the RUNBOOK.
#
# Usage:
#   bash paper/scripts/run_remaining.sh list-hard [N]        # print N hard-tier laws to attempt
#   bash paper/scripts/run_remaining.sh handsolve <cert.lean> ["<law>"]   # verify a hand-built model
#   bash paper/scripts/run_remaining.sh sweep                # FULL hard-tier sweep -> membership list
#   bash paper/scripts/run_remaining.sh llm-smoke <pairs.jsonl>   # 1-pair/1-round proposer smoke test
set -u -o pipefail
cd "$(dirname "$0")/../.." || exit 1   # -> repo root (same as run_all.sh)

R=paper/results
IN=$R/final_status.jsonl
VAMPIRE=${VAMPIRE:-paper/bin/vampire}
EPROVER=$(command -v eprover || true)
TWEE=$(command -v twee || true)
SHARDS=${SHARDS:-$(nproc)}

cmd=${1:-help}; shift || true

case "$cmd" in

# ---------------------------------------------------------------------------
# TASK 7 prep — list hard-tier laws (status NO_FINITE_MODEL) to hand-solve.
# These are the 4,141 admissible-but-unresolved laws; pick a few with small witnesses.
# ---------------------------------------------------------------------------
list-hard)
  N=${1:-20}
  python3 - "$IN" "$N" <<'PY'
import json,sys
inp,N=sys.argv[1],int(sys.argv[2])
rows=[json.loads(l) for l in open(inp) if l.strip()]
hard=[r for r in rows if r.get("status")=="NO_FINITE_MODEL"]
# shortest laws first: easiest to eyeball an algebraic model for
hard.sort(key=lambda r: len(r["law"]))
for r in hard[:N]:
    print(f'{r.get("cert","")[:12]}  {r["law"]}')
print(f'\n# {len(hard)} hard-tier laws total', file=sys.stderr)
PY
  ;;

# ---------------------------------------------------------------------------
# TASK 7 — verify a hand-built (or LLM-built) algebraic model of a hard-tier law.
# You supply a Lean certificate file (carrier + operation + proof it satisfies the law,
# nontrivial). Two checks: quick standalone compile, then the OFFICIAL benchmark judge
# (fixed statement + axiom-footprint allowlist). cf. paper/certs/Order5v2_1593.lean.
# ---------------------------------------------------------------------------
handsolve)
  CERT=${1:?need a .lean certificate path}; LAW=${2:-}
  echo "== 1) quick standalone oracle (lean_oracle.py: does the cert compile?) =="
  python3 paper/scripts/lean_oracle.py "$CERT" --lake-dir . --timeout 600
  echo
  if [[ -n "$LAW" ]]; then
    echo "== 2) OFFICIAL judge (answer_spec.py --judge: fixed goal + axiom allowlist) =="
    python3 paper/scripts/answer_spec.py --law "$LAW" --side austin \
        --submission "$CERT" --judge --lean-dir . --timeout 600
  else
    echo "(skip official judge: pass the law string as arg 2 to run answer_spec --judge)"
    echo " see the exact submission format with:  python3 paper/scripts/answer_spec.py --selftest --lean-dir ."
  fi
  echo
  echo "== optional non-vacuity pre-check for saturation-derived models =="
  echo "python3 paper/scripts/ordered_model.py --cert <sat> --law \"\$LAW\" --verify-law --nontrivial --refute 'x=y'"
  ;;

# ---------------------------------------------------------------------------
# TASK 9 — FULL hard-tier sweep for the membership list (not the 300 sample).
# Runs the whole NO_FINITE_MODEL set (--n 0 = all) at the full ladder, sharded, to a
# FRESH file so it never clobbers baseline_v1.jsonl (the finalized 300-sample curve).
# Cost per RUNBOOK: ~5,300 core-hours (~7 days on 32 cores); nothing resolves, so every
# law walks the whole ladder. Launch under nohup.
# ---------------------------------------------------------------------------
sweep)
  [[ -x "$VAMPIRE" ]] || { echo "vampire not at $VAMPIRE"; exit 1; }
  [[ -n "$EPROVER" && -n "$TWEE" ]] || { echo "eprover/twee missing — a hard tier from an incomplete portfolio is provisional (RUNBOOK §1)"; exit 1; }
  OUT=$R/baseline_full.jsonl
  echo "selftest first (refuses to run otherwise)…"
  python3 paper/scripts/baseline_probe.py --selftest --vampire "$VAMPIRE" \
      --eprover "$EPROVER" --twee "$TWEE" | grep -q "SELFTEST OK" \
      || { echo "SELFTEST FAILED — stopping"; exit 1; }
  : > "$OUT"   # truncate ONCE before the fleet (shards append; no resume logic)
  echo "launching $SHARDS shards over ALL NO_FINITE_MODEL laws -> $OUT"
  pids=()
  for i in $(seq 0 $((SHARDS-1))); do
    python3 paper/scripts/baseline_probe.py \
      --in "$IN" --status NO_FINITE_MODEL \
      --vampire "$VAMPIRE" --eprover "$EPROVER" --twee "$TWEE" \
      --budgets 30,60,120,300,600 --n 0 --shard "$i/$SHARDS" \
      --out "$OUT" --certs paper/certs/baseline \
      >> "$R/sweep_$i.log" 2>&1 &
    pids+=($!)
  done
  wait "${pids[@]}"
  echo "sweep done: $(wc -l < "$OUT") rows"
  python3 paper/scripts/baseline_probe.py --curve "$OUT"
  echo "# unresolved laws in \$OUT are the definitive hard-tier membership list."
  ;;

# ---------------------------------------------------------------------------
# TASK 8 — LLM baseline SMOKE TEST (1 pair, 1 round) with the existing proposer.
# NOTE: attic/finite_regime/proposer_o3.py is the finite-regime, pairs-format prototype.
# It proves the propose->self-verify->judge loop end-to-end and is the base for the
# ALPS harness (LLM_EXPERIMENT_PLAN §8: wrap answer_spec.py as judge + L2 autoformalizer
# around lean_oracle.py). Run ONE pair / ONE round first — OpenRouter funds drained in a
# day once (see memory). Use reasoning-effort low in constrained envs; high on the cluster.
# ---------------------------------------------------------------------------
llm-smoke)
  PAIRS=${1:?need a pairs .jsonl (equation1/equation2 format)}
  [[ -n "${OPENROUTER_API_KEY:-}" ]] || { echo "export OPENROUTER_API_KEY first"; exit 1; }
  python3 paper/attic/finite_regime/proposer_o3.py \
      --pairs "$PAIRS" --rounds 1 \
      --solver-dir paper/solver_frozen --judge-dir . \
      --reasoning-effort "${EFFORT:-high}" \
      --cert-dir paper/certs \
      --out "$R/llm_smoke.jsonl"
  echo "# check $R/llm_smoke.jsonl; scale rounds/pairs only after this one solve is verified."
  ;;

*)
  echo "usage: bash paper/scripts/run_remaining.sh {list-hard [N] | handsolve <cert.lean> [law] | sweep | llm-smoke <pairs.jsonl>}"
  ;;
esac
