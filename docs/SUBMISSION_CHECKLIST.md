# Pre-submission checklist (Solo track)

Things to confirm/do before uploading `solver.py` to the official judge.
Compliance was reviewed 2026-06-20 against `docs/solo_mode.md` + the proxy; the
merged solver (`scripts/my_solver_merged/solver.py`) passed everything below
EXCEPT the one flagged item.

## Action items

- [ ] **Remove (or gate) the extra `"stage"` key in `call_judge`.**
  Our attribution edit makes `call_judge` send
  `{"call":"judge","verdict","code","stage": CURRENT_STAGE}`. The reference demo
  (`examples/solo/demos/baseline/solver.py`) sends exactly
  `{"call":"judge","verdict","code"}`. The extra key is almost certainly ignored
  by the official proxy (the "malformed" status is about the certificate, not
  request keys) and it gives **zero** competition benefit — it only feeds our
  local proxy's `solved_by`. For a strictly-clean submission, gate it behind an
  env var (e.g. only send `stage` when `SOLVER_ATTRIBUTION=1`) so the wire
  protocol is byte-identical to the reference, while local analysis runs still
  get `solved_by`/`used_llm`.

## Already-verified compliant (no action)

- Single file; submission dir contains only `solver.py`. Source 158 KB < 500 KB.
- `PROMPT` is a top-level string constant (AST-extractable by the proxy).
- Pure stdlib imports (`json, re, sys, time, itertools`); no network, file I/O,
  subprocess, `eval`/`exec`, or `random` (deterministic).
- Protocol matches the reference baseline (judge calls; proxy treats an accepted
  judge response as the final answer — no `submit` message needed).
- Emitted certs within limits (false op-tables ≪ 20 KB; true proofs < 100 KB);
  `set_option maxRecDepth 100000` is standard Lean and was accepted in real runs.

## Misc notes

- `hard3_0001/0002/0003` in `merged_hard3.json` came from a stale 30s-timeout run
  (killed at the wall deadline, not an algorithm miss). Re-run them at the full
  3600s budget for clean numbers — `hard3_0001` solves (valid proof found in
  0.0s); 0002/0003 stay unsolved (genuinely hard).
