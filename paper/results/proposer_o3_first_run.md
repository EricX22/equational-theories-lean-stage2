# First real o3 proposer run (2026-07-01)

Wired the actual proposer per `paper/PROPOSER_LOOP_SPEC.md`: `openai/o3` via
OpenRouter (the same key/model the paper track already uses), prompted with
the §2 contract (propose a construction *family* as an executable Python
rule for `op(a,b,n)`, not a hand-filled table), on the 4 pairs validated in
[[proposer-loop-spec]] as genuinely resistant to the full portfolio +
Vampire 40s.

## Sandbox note (important for reruns)
`openai/o3` at `reasoning: {"effort": "high"}` routinely exceeds this
Cowork sandbox's 45s-per-command cap and gets silently killed with zero
output (no background processes survive between tool calls here). Dropping
to `"low"` effort keeps most calls under ~35-40s while still doing genuine
multi-thousand-token reasoning (observed 1,500-3,000 reasoning tokens per
call) — used `"low"` throughout. Outside this sandbox (the real machine via
`run.sh`), `"high"` should work fine and is recommended for the real study.

Also hit and worked around a real infra bug: the Cowork FUSE mount
truncated `paper/scripts/proposer_o3.py` mid-write after several sequential
Edit-tool calls (matches the known "mount sync truncates files" caveat, not
previously seen below ~175KB — now confirmed it can happen well under 12KB
too). Fix: write the file via a bash heredoc directly instead of the
Edit/Write tool for anything that will be repeatedly modified, verify with
`grep -c "if __name__"` before running.

## Results: 6 real attempts, all self-verify-failed, $0.12 total
| Pair | Round | Family proposed | Self-verified | Note |
|---|---|---|---|---|
| order5v2_0073 | 1 | quadratic-twist modular | No | clean code, no witness found |
| order5v2_1593 | 1 | Quaternion conjugation rack | No | code bug (IndexError at n=8) |
| order5v2_0534 | 1 | UpperTriAff (upper-triangular affine) | No | clean code, no witness found |
| order5v2_0515 | 1 | coordinate-swap semidirect square | No | clean code, no witness found |
| order5v2_0534 | 2 | quadratic-bilinear mod-n magma | No | clean code, no witness found |
| order5v2_0515 | 2 | high-degree modular polynomial | No | clean code, no witness found |

Total cost: **$0.1234** (12,480 reasoning tokens across 6 calls). Zero
candidates reached the Lean judge — the self-verification gate held for
every attempt (the "0 accepted wrong" invariant never had a chance to be
tested because nothing false-but-plausible got through, which is the
correct/safe behavior, not a failure of the gate).

Every proposal was **genuinely distinct and non-trivial** — none were
repeats of the ruled-out families (cyclic twists, dihedral groups) from the
earlier manual attempt, and 5/6 were clean, bug-free, executable code on
the first shot (only the quaternion one had an implementation bug, not a
mathematical dead end — worth retrying with a bug-fixed materializer).

## What this demonstrates
1. **The full C3 pipeline works end-to-end for real**, not just in design:
   real o3 call → JSON-parsed proposal → Python materializer → self-verify
   → (would-be) judge submission, with cost/attempt data collected exactly
   as PAPER_PLAN's C3 reporting spec asks for (`attempts/cost per solve`
   — here, 6 attempts / $0.12 / 0 solves, a real if so-far-negative data
   point).
2. **No positive result yet.** Four genuinely hard order-5 pairs remain
   unsolved after 6 real o3 attempts. This is itself informative: these
   four pairs are hard enough that even fairly creative LLM proposals (a
   Latin-square-plus-conjugation "rack" structure, upper-triangular affine
   matrices, high-degree polynomials) don't immediately crack them.
3. **The mount-truncation bug is now documented and worked around** —
   relevant for any future script iteration in this sandbox, not just this
   file.

## Honest next steps
- Re-run with `"high"` reasoning effort on the real machine (via `run.sh`,
  where the 45s cap doesn't apply) — `"low"` effort may simply be
  under-powered for genuinely hard order-5 constructions.
- Fix the quaternion-rack materializer bug and retry that family
  specifically — it's the one attempt that failed on an implementation
  error, not a real mathematical miss.
- Increase `--rounds` per pair now that the pipeline is proven to work
  (only got 1-2 rounds per pair here due to the sandbox time budget).
- Consider giving the model the *specific equation shape* as a hint more
  aggressively (e.g. "eq1 has a self-referential left-identity pattern") —
  the design doc's negative manual log already flagged this; o3's own
  justifications increasingly gestured at similar structural reasoning
  (e.g. the "UpperTriAff" proposal explicitly reasoned about eq1's nested
  self-reference) but didn't land a working construction.
