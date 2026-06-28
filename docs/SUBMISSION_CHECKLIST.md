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

- Single file; submission dir contains only `solver.py`. Source ~170 KB < 500 KB
  (grew with the 2026-06-23 algebraic-linear stage; re-check the exact size on a
  clean filesystem before submit).
- `PROMPT` is a top-level string constant (AST-extractable by the proxy).
- Pure stdlib imports (`json, re, sys, time, itertools`, plus `fractions` and
  `math.gcd` used by the algebraic-linear stage for exact rational polynomial
  arithmetic); no network, file I/O, subprocess, `eval`/`exec`, or `random` —
  fully deterministic. (The algebraic-linear stage verifies eq1 by an EXACT
  basis check, not random sampling, so no `random` import was introduced.)
- Protocol matches the reference baseline (judge calls; proxy treats an accepted
  judge response as the final answer — no `submit` message needed).
- Emitted certs within limits (false op-tables ≪ 20 KB; true proofs < 100 KB);
  `set_option maxRecDepth 100000` is standard Lean and was accepted in real runs.

## Misc notes

- `hard3_0001/0002/0003` show unsolved in `merged_hard3.json`, but that was an
  infrastructure death, not an algorithm miss: a slow/cold `lake env` raised an
  uncaught `subprocess.TimeoutExpired` that killed the run before any stage ran.
  Fixed in `judge/verify.py` (also catch `TimeoutExpired`/`SubprocessError` →
  fall through to the static `.lake` glob); per `docs/SOLVER_STATUS.md` §0.3 all
  three now solve deterministically. The merged file predates the fix — re-run
  hard3 on the current code for clean numbers.
- `hard2_0051` shows unsolved in `merged_hard2.json` (predates this session); it
  is now solved by the algebraic-linear stage (judge-accepted). Re-run hard2 for
  clean numbers. Lone remaining false miss: `hard2_0027` (no linear witness).
