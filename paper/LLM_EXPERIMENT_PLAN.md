# LLM EXPERIMENT PLAN — the solver-facing harness and the eval

> **STALE in parts — see `TASK_AND_JUDGING.md` (2026-07-17 pivot).** This doc predates the
> multi-channel judging. Corrections: (1) the Austin/construction side is NOT Lean-verified —
> no Lean construction path exists (confluence `sorry`) and no Austin model is arithmetic
> (descent theorem), so `lean_oracle.py`/L2-affine are retired for Austin. Construction is now
> ATP-certified via `llm_construct.py` (solver proposes a presentation `E`; Vampire checks).
> (2) The "solvable tier" Austin laws (262 AUSTIN_PROVEN) are already bare-certified by
> saturation — no LLM value there; the real construction niche is the 4,141 NO_FINITE_MODEL
> laws. (3) The Lean-verified rung is now the TRIVIAL side only (`llm_trivial.py`), which is
> where the first real LLM solves come from. Read below for the eval *intent*, but take the
> harness/judging specifics from `TASK_AND_JUDGING.md`.

How to run the LLM part of §4, and — the harder design question — what standard
"stepping stone" to ship so that LLM-based solvers built on the benchmark get a *fair,
supported* entry point rather than a bare wall.

---

## 1. What the LLM experiments must show (two parts, not one)

They are not there to prove an LLM is good. They answer two separate questions:

- **Difficulty (the frontier is real for LLMs too).** A fair-effort LLM scores ~0 on the
  hard tier. This is the number that lets the paper say "and current LLMs," and it
  reinforces method-boundedness — the same laws that resist the automated portfolio resist
  a strong model.
- **Climbability (the benchmark is not a wall).** On *fresh, solvable* instances an LLM
  produces a Lean-verified construction, doing genuine per-law work. This is the capability
  case study (the o3 mod-17 affine model is the prototype). Without it, "everything scores
  zero" reads as "possibly impossible."

The two together = "real, answerable, currently unsolved at the frontier," which is the
shape an AI-for-science benchmark wants. **Design the harness so the same rig produces
both**, by varying only the instance tier.

---

## 2. The interaction protocol (identical for every model)

1. **Input:** the law $L$ (in a plain notation + the generated Lean goal), the task
   statement, and the declared tool set. Nothing model-specific.
2. **Output:** a *submission* — a model (carrier + operation) or a triviality argument —
   in a format the harness can turn into a Lean file.
3. **Judge as oracle:** the harness runs `answer_spec.py`, returns accept/reject plus the
   Lean error text on failure.
4. **Self-verify loop:** the model may iterate — propose, read the judge's feedback,
   revise — up to a fixed budget (attempts / tokens / wall). This is pre-registered as
   allowed (it is what a mathematician does: check your work).
5. **Budget and tools are fixed and logged** per the pre-registration in §5.

The whole loop already exists in miniature in `proposer_o3.py`; the work is to
standardize the I/O and wire it to `answer_spec.py` instead of the old finite-regime
verifier.

---

## 3. The stepping stone: a scaffold ladder that isolates the creative step

The barrier for an LLM is usually **not** inventing the structure (a model can propose
"$\mathbb{Z}/17$ with $8x+7y$") but **writing the Lean proof** that it satisfies the law.
If we test only the raw setting, we conflate "can't construct" with "can't wrangle Lean,"
and a capable constructor looks like a failure. So ship a **ladder of scaffolds** and
report which rung each solve needed — this both makes the eval fair and is the artifact
LLM developers build on.

- **L0 — Raw.** Law + goal + judge; the model writes the entire Lean file. Tests
  construction *and* formalization fluency. The unassisted number.
- **L1 — Proof skeleton.** The harness supplies a content-free Lean skeleton — `def op`,
  `theorem law : Law op`, `theorem nontriv` — with the model and proofs as holes. Isolates
  construction from boilerplate. The skeleton must leak nothing about the structure.
- **L2 — Model-spec autoformalizer (the key rung).** The model outputs only the *math* —
  a carrier (`ZMod n`, `ℤ`, a finite type, a quotient) and an operation as a formula — and
  the harness auto-generates the Lean and discharges it with standard tactics (`decide`
  for small finite, `ring`/`linear_combination`/`omega` for algebraic). The model never
  touches Lean syntax; the test is purely "find the right structure." This is the setting
  that most isolates the capability the benchmark is about, and it is what the o3 result
  effectively used.

Reporting solves *by rung* disentangles the two abilities: an L2 solve that fails at L0
says "the model found the structure but couldn't formalize it," which is a finding about
LLMs and formalization, not about construction.

**The autoformalizer is the highest-value thing to build.** It is a thin extension of
`lean_oracle.py`: parse a structured model spec → emit `def op ...` + the generated goal →
try a fixed tactic list → return the judge's verdict. It covers the **algebraic channel**,
which is exactly what is Lean-checkable today (rewrite-system models await
`ground_confluent`, the companion paper), so it aligns the support with the achievable
tier by construction.

---

## 4. Instance selection

- **Hard tier (difficulty):** a sample of `NO_FINITE_MODEL` laws the portfolio leaves
  unresolved. Expect ~0 at every rung. Draw from the published hard tier once the full
  sweep exists; a 100–200 law sample is enough for "~0."
- **Achievable tier (climbability):** **fresh, contamination-free** instances that we have
  privately verified are solvable, and specifically ones whose model sits **outside the
  bounded automated search's reach** (e.g. an affine model over a modulus the finder's
  cap excludes — the o3-1593 shape). Fresh dissolves the contamination worry entirely; the
  "outside the search's reach" property guarantees the solve is genuine construction, not
  something the portfolio would have found. Verify solvability, keep the answer private,
  hand the model only the standard inputs.
- Optionally a **warm-up curriculum:** a handful of easier solvable instances first, to
  establish the pipeline works and to calibrate the scaffold rungs, before the harder
  achievable and hard-tier draws.

---

## 5. Fairness and pre-registration (write this down before the first run)

- **Tool access:** construction suite / templates and the Lean checker — **yes**;
  saturation provers (Vampire/E/Twee) — **no**. Otherwise a model just runs the baseline
  at 10× and "wins," measuring nothing.
- **Same scaffold, same budget, same instances** for every model compared.
- **Self-verify loop allowed**, compute reported.
- **After any LLM solve, re-run the portfolio at 10× on that law.** If it falls, say so —
  the honest analogue of what killed the finite-regime story.
- **Fresh instances for the capability demo**; report the seed and date.
- Pre-register the metric (M∖N and N∖M — solves the model gets that the portfolio doesn't,
  and vice versa) *before* the first call, so the tier can't be tuned to flatter the
  result.

---

## 6. What to report

- Hard tier: solve rate per rung (expected ~0), with the portfolio's rate alongside.
- Achievable tier: solve rate per rung; at least one fully worked, Lean-verified example
  (this is L1 in the figure list — the worked-example listing, doubling as the capability
  demo).
- The rung breakdown: how much of the gap is construction vs formalization.
- Cost (tokens / attempts / wall) per solve.
- The 10× portfolio recheck outcome on every LLM solve.

---

## 7. Released artifacts (this is the "support LLMs built on top of it" part)

Ship the harness so a developer can plug a model in without rebuilding any of this:

- **The judge as a callable** (`answer_spec.py`) — law → generated goals → accept/reject
  + feedback.
- **The scaffold generator** — law → L1 skeleton, and the L2 model-spec schema.
- **The autoformalizer** — model spec → Lean → verdict (the §3 extension of
  `lean_oracle.py`).
- **A reference solver loop** (cleaned-up `proposer_o3.py`) showing the propose →
  auto-formalize → judge → revise cycle end to end.
- **The instance API** — fetch a law, its tier, and (for held-out sets) submit an answer.

A benchmark that ships only static instances forces every entrant to re-implement the
formalization plumbing; shipping the harness is what makes the benchmark *usable* and is
itself a contribution to mention in the paper.

---

## 8. Build order

1. Standardize the model-spec schema (carrier + operation formula) and extend
   `lean_oracle.py` into the **L2 autoformalizer** — highest value, unblocks the fair
   capability demo.
2. Wrap `answer_spec.py` as the judge oracle with feedback.
3. Port `proposer_o3.py` to the new I/O; run **one instance, one model, one round** before
   any sweep (the budget-caution lesson — OpenRouter funds ran dry in a day once).
4. Mint fresh achievable instances (verify solvable, outside the search cap); confirm the
   o3-1593 instance's contamination status or regenerate an analog.
5. Small A/B on the scaffold rungs on a few achievable instances → confirm the ladder
   separates construction from formalization.
6. Then the hard-tier sample for the ~0 difficulty number.

Keep every run cheap first (1 instance / 1 round) and flag scale/cost before any batch.
