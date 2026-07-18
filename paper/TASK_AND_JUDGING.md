# ALPS — Task & Judging (canonical definition)

Written 2026-07-17. This supersedes the "answers are Lean proofs, kernel-checked"
framing wherever it still appears (e.g. `PAPER_HANDOFF.md` §0 thesis / the **V** bullet).
The *task* is unchanged; the *judging* is now **multi-channel**.

---

## The task (unchanged)

Given an admissible law `L` — one **certified to have no nontrivial finite model** (the
(i)-certificate) — the solver faces a two-sided problem and must answer exactly one side:

- **AUSTIN (construct):** exhibit a nontrivial magma satisfying `L` (necessarily infinite).
- **TRIVIAL (collapse):** prove `L ⊨ x = y` (every model satisfies-the-law collapses to a point).

By excluded middle exactly one side holds, so every instance is well-posed.

## What changed: judging is multi-channel

Old framing: *every* answer is a Lean proof of `Problem.AustinGoal` / `Problem.TrivialGoal`,
checked by the Lean kernel. That is **only viable for the TRIVIAL side.** Two facts kill the
Lean route for construction:

1. **No Austin model is arithmetic (descent theorem).** If `op` were a polynomial/affine
   formula over ℤ (or ℤ^k, or ℤ/n), the law would hold as an identity that survives
   reduction mod 2 → a *finite* nontrivial model → contradicts "no finite model." So the
   affine autoformalizer (`llm_autoformalize.py`, "L2-affine") is **provably empty for
   Austin** — retire it. (Empirically confirmed: 0/40 Austin laws admit a 2-element model;
   0/60 admit an affine op.)
2. **Lean can't check the real (rewrite-system) models yet.** The general construction,
   `paper/lean/OrderedModel.lean`, bottoms out at `sorry` for termination + ground
   confluence — that proof is the companion paper, not done.

Resolution: **a certificate from any trusted checker counts.** "A certificate is a
certificate." We use whichever checker fits the side:

| Side | What the solver submits | Checker | Harness |
|------|-------------------------|---------|---------|
| TRIVIAL | a **Lean proof** of `Problem.TrivialGoal` | Lean kernel + axiom allowlist (`answer_spec.py`) | `paper/scripts/llm_trivial.py` |
| AUSTIN  | a **model**, as a finite first-order presentation `E` of `op` (equations) — NOT a Lean proof | **Vampire** (ATP), cross-checkable by Twee | `paper/scripts/llm_construct.py` |

The solver **still just proposes a model** on the Austin side. It does not write a Lean
proof, does not prove confluence — it names `E` and the harness runs the prover.

## The ATP construction certificate (Austin side), in full

The solver proposes `E` = a finite set of equations over the magma symbol (a presentation /
completed rewrite system), **not the law itself**. Two Vampire queries:

- **(A) CORRECTNESS** — prove `E ⊢ law` (law as conjecture → `SZS status Theorem`). This is
  a *refutation* proof, independently checkable — the strong kind of certificate.
- **(B) NON-VACUITY** — saturate `E ∪ {∃a≠b}` (`SZS status Satisfiable`, completeness-guarded:
  reject if Vampire reports "incomplete strategy"). A nontrivial model of `E` exists.

Certified iff **both** pass. Soundness: (B) gives a nontrivial model of `E`; (A) makes it
satisfy the law ⇒ a nontrivial model satisfying `L` exists ⇒ Austin.

**Self-policing** (why the solver can't cheat):
- `E = {law}` gains nothing: (A) is trivial but (B) becomes the *bare* saturation of the law,
  which diverges on exactly the hard laws.
- A collapsing `E` (e.g. `x=y`) passes (A) but **fails (B)** — `E ∪ {a≠b}` is UNSAT.
- Validated with three controls in `llm_construct.py --selftest`: correct → CERTIFIED;
  wrong model (left-projection) → rejected on (A); vacuous collapse → rejected on (B).

Vampire ships in-repo at `paper/bin/vampire` (5.0.1) and runs in the sandbox.

## Trust base (state this in the paper)

Not one uniform trust base: **Lean kernel** for the trivial side, **Vampire saturation**
(cross-checkable by Twee) for the construction side. This is honest and principled — the
entire corpus's Austin labels already rest on ATP saturation, not Lean. What we give up is
the single-checker cleanliness; what we gain is the ability to grade the construction side
*at all*.

## Scope / reach of the ATP channel

- **262 AUSTIN_PROVEN** — bare saturation already certifies these (they got the label *because*
  it terminates). No LLM value; baseline solves them.
- **4,141 NO_FINITE_MODEL** — the LLM niche and the open frontier. Bare saturation *diverges*
  (confirmed across kbo/lpo/discount orderings). These are genuinely open: each is Austin XOR
  trivial and we don't know which. A solver `E` that certifies one **upgrades it
  NO_FINITE_MODEL → proven Austin — a result no automated method in the portfolio reached.**
  Caveat: laws whose completion is *infinite* (non-orientable hard tier, e.g. 12857/33436)
  have no finite `E` and are out of this channel's reach; they stay reported as open. Also:
  these laws collapse under idempotence/commutativity/associativity (0/9) → their models are
  "wild" (non-comm, non-assoc); a crack needs a bespoke presentation, not a nice property.
- **3,080 TRIVIAL** — the Lean-graded deductive rung; where LLM solves are most reachable.

## Reality check on the LLM baseline

- **No LLM has ever produced a verified ALPS solve** in any recorded run. Every prior "solve"
  on file (`ours_llm_*.json`, `hard3_000x`) was the *automated* engine (`used_llm=False`,
  `solved_by="bounded equality graph"/"completion"`), on the trivial side, in the *old
  implication format*.
- The o4-mini L2-affine run scored **0/60** — a channel artifact (affine is empty for Austin),
  not a capability signal. Do not report it as an LLM number.
- The first real verified LLM solves will come from the **trivial rung** (`llm_trivial.py`).
  The construction rung is sound and ready but its niche is a hard, possibly-unreachable
  frontier for current models.

## Files

- `paper/scripts/answer_spec.py` — the Lean statement + judge (trivial side; also defines
  `AustinGoal` for any future Lean-checkable construction).
- `paper/scripts/llm_trivial.py` — trivial rung (LLM writes Lean proof; worked-example prompt).
- `paper/scripts/llm_construct.py` — Austin rung (LLM proposes `E`; Vampire certifies). `--selftest`.
- `paper/scripts/llm_autoformalize.py` — **RETIRED** (L2-affine, provably empty for Austin).
- `paper/scripts/atp_reach.py` — maps bare-saturation reach vs. the NO_FINITE_MODEL niche.
- `paper/bin/vampire` — Vampire 5.0.1 (the construction-side checker).
