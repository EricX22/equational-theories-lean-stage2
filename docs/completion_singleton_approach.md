# Cracking the hard-singleton class with ordered completion

**Status:** design + validated prototype. The solver (`scripts/my_solver/solver.py`)
has been left **unchanged** (reverted to its 1668-line baseline). This document
describes what to build, with working implementation excerpts and concrete use
cases. A complete, tested reference engine lives at
`docs/completion_engine_reference.py`.

---

## 1. The finding in one paragraph

The hard "true singleton" implications (where `Eq1` forces `∀ p q, p = q`, so any
`Eq2` follows) were the class producing **zero** successes from the LLM strategist.
The bottleneck is **not** the LLM and **not** the seed terms — it is the
proof-search *engine*. The current engine (bounded BFS over `h`-instantiations plus
one-step congruence, in `try_singleton_equality_graph`) cannot reach these proofs at
any seed quality; on `eq2377` it saturates to ~87k nodes and finds no path. A
standard **ordered (unfailing) Knuth–Bendix completion** engine solves the same
problems deterministically in milliseconds. Validated on `examples/problems/sample_20.json`:
**10/20 solved** (every singleton, including `eq2377`), each in well under a second,
all cross-checked against z3 (no ≥2-element model exists, so the collapse is real).

The LLM's role for this class should therefore shrink to nothing; completion is a
decision procedure for it. The LLM remains potentially useful only for the cases
completion *cannot* close in budget (see §7).

---

## 2. Why completion is the right algorithm

`Eq1` is a single equation, strongly oriented (its right side is larger than its
left, or vice-versa). Proving the goal — or the singleton collapse — means deriving
a *consequence* of that one equation. "What equations follow from this equation set"
is exactly the question completion answers, via **critical pairs** (the overlaps
where a rewrite rule conflicts with itself or another). Unfailing completion is
*refutationally complete* for equational logic: if the implication is true, ordered
completion will derive it. The current BFS has no such guarantee — it enumerates a
bounded term universe and hopes a path exists inside it, which for these proofs it
does not, because the witnessing intermediate terms are large and specific.

Contrast with equality saturation / e-graphs (what the current engine is a weak
version of): saturation *propagates* a fixed rule set but never *generates* new
oriented rules from critical pairs, so it cannot manufacture the collapsing
equation. Completion generates; saturation only propagates. That is the precise
reason the current engine plateaus.

Papers: Smallbone, *Twee: An Equational Theorem Prover* (CADE-28, 2021); Bachmair,
Dershowitz & Plaisted, *Completion Without Failure* (1989); Baader & Nipkow, *Term
Rewriting and All That* (1998). The Equational Theories Project (arXiv 2512.07087)
resolved all ~22M implication edges using exactly this family of tooling plus Lean.

**Competition constraint:** the solver is a single `solver.py`, no network, isolated
subprocess. So you cannot shell out to Twee/E/Vampire — the algorithm must be
reimplemented in-process Python. It is a few hundred lines; the 3600 s/problem Solo
budget is ample.

---

## 3. Architecture: where it slots in

Add one deterministic stage, gated on the existing `forces_singleton` hint, placed
**before** the LLM strategist fallback in `main()`:

```
... existing deterministic stages ...
Stage 2.6  structural singleton templates      (existing)
Stage 2.7  ordered-completion singleton  <-- NEW, deterministic, no LLM
Stage 3    LLM strategist / fallback           (existing; now rarely reached)
```

The stage does two things:

1. **Decide**: run proof-carrying completion on `Eq1`. If it derives an equation
   between two distinct variables, `Eq1` forces a singleton.
2. **Reconstruct**: turn the derivation into a judge-valid Lean proof of
   `∀ p q, p = q`, then apply it to the goal.

Crucially, the LLM never authors Lean. The engine produces the proof mechanically
and a Python proof-checker validates it before it is ever submitted.

---

## 4. Implementation

All excerpts below are from the tested reference engine
(`docs/completion_engine_reference.py`), lightly trimmed. Terms are
`('V', name)` for variables and `('F', sym, (args...))` for applications
(`sym = 'o'` is the magma operation `◇`).

### 4.1 Full unification (not matching)

The existing solver's `unify` is one-directional *matching*. Completion needs full
unification with occurs-check:

```python
def deref(t, s):
    while is_v(t) and t[1] in s: t = s[t[1]]
    return t

def unify(x, y, s):
    if s is None: return None
    x = deref(x, s); y = deref(y, s)
    if is_v(x):
        if is_v(y) and x[1] == y[1]: return s
        if occurs(x[1], y, s): return None
        s2 = dict(s); s2[x[1]] = y; return s2
    if is_v(y):
        if occurs(y[1], x, s): return None
        s2 = dict(s); s2[y[1]] = x; return s2
    if x[1] != y[1] or len(x[2]) != len(y[2]): return None
    for a, b in zip(x[2], y[2]):
        s = unify(a, b, s)
        if s is None: return None
    return s
```

### 4.2 LPO reduction order (orients equations, guarantees termination)

```python
PREC = {'o': 10}                 # op outranks constants
def lpo_gt(s, t):
    if s == t: return False
    if is_v(t): return (not is_v(s)) and (t[1] in vars_of(s))   # var subterm rule
    if is_v(s): return False
    f, ss = s[1], s[2]; g, ts = t[1], t[2]
    for si in ss:
        if si == t or lpo_gt(si, t): return True
    if all(lpo_gt(s, tj) for tj in ts):
        if PREC.get(f,0) > PREC.get(g,0): return True
        if f == g:
            for a, b in zip(ss, ts):
                if a == b: continue
                return lpo_gt(a, b)
    return False
```

Rewriting only ever applies an instance `l→r` when `lpo_gt(l_inst, r_inst)`, so
rewriting strictly descends a well-founded order and terminates.

### 4.3 The one gotcha that cost the most time

In rewriting, the rule and the target term share a variable namespace. If you match
without renaming, a variable can bind to a term containing **itself**, and the
substitution-application then loops forever (`RecursionError`, or a segfault if you
raised the recursion limit). **Always rename the rule apart from the target before
matching:**

```python
def rewrite_step(t, rules):
    for (s0, t0, P0) in rules:
        s_, t_ = rename(s0, '$'), rename(t0, '$')   # <-- rename rule apart
        ...
```

A second, subtler instance: computing a proof's type with an *identity* substitution
(`{'x': ('V','x')}`) also loops `deref`. Use a plain, non-deref simultaneous
substitution for proof bookkeeping:

```python
def psub(t, s):                  # simultaneous, no deref — safe on identity maps
    if is_v(t): return s.get(t[1], t)
    return ('F', t[1], tuple(psub(a, s) for a in t[2]))
```

### 4.4 Critical pairs

Superpose one equation into a non-variable subterm of another; the overlap is a new
consequence:

```python
def crit_pairs(e1, e2):
    s1,t1 = e1; s2,t2 = e2
    s2r,t2r = rename(s2,'#'), rename(t2,'#')
    out = []
    for (l1,r1) in ((s1,t1),(t1,s1)):
        for (l2,r2) in ((s2r,t2r),(t2r,s2r)):
            for path, sub in nonvar_positions(l1):
                sg = unify(sub, l2, {})
                if sg is None: continue
                R1 = appsub(r1, sg); L1 = appsub(l1, sg)
                if lpo_gt(R1, L1): continue                       # ordering side-cond
                if lpo_gt(appsub(r2,sg), appsub(l2,sg)): continue
                newl = appsub(replace(l1, path, r2), sg)
                out.append((R1, newl))                            # σr1 = σl1[σr2]_p
    return out
```

### 4.5 Proof-carrying layer (so a collapse becomes Lean)

Every equation carries a **proof object** built from `h`-instances and
`congrArg`/`symm`/`trans`. A Python checker (`ptype`) recomputes the `lhs=rhs` each
object establishes and asserts it matches the equation — this is a full proof checker
for the equational calculus, so a malformed proof can never reach the judge.

```python
# proof objects: ('H',(a,b,c,d)) ('SYM',P) ('TRANS',P,Q) ('CL',t,P) ('CR',t,P) ('REFL',t)

def ptype(P):                                 # recompute (lhs, rhs) this proof proves
    k = P[0]
    if k == 'H':
        s = dict(zip(H_VARS, P[1]))
        return (psub(H_LHS, s), psub(H_RHS, s))
    if k == 'SYM':   a,b = ptype(P[1]); return (b, a)
    if k == 'TRANS': a,b = ptype(P[1]); c,d = ptype(P[2]); assert b == c; return (a, d)
    if k == 'CL':    a,b = ptype(P[2]); return (('F','o',(a,P[1])), ('F','o',(b,P[1])))
    if k == 'CR':    a,b = ptype(P[2]); return (('F','o',(P[1],a)), ('F','o',(P[1],b)))
    if k == 'REFL':  return (P[1], P[1])

def render(P):                                # proof object -> Lean term
    k = P[0]
    if k == 'H':     return "(h " + " ".join(ts(a) for a in P[1]) + ")"
    if k == 'SYM':   return "(" + render(P[1]) + ").symm"
    if k == 'TRANS': return "((" + render(P[1]) + ").trans (" + render(P[2]) + "))"
    if k == 'CL':    return "(congrArg (fun s => s ◇ " + ts(P[1]) + ") " + render(P[2]) + ")"
    if k == 'CR':    return "(congrArg (fun s => " + ts(P[1]) + " ◇ s) " + render(P[2]) + ")"
    if k == 'REFL':  return "(rfl)"
```

Critical pairs, rewriting, and normalization each thread proofs through (a CP's proof
is `(σr1=σl1).symm` then a congruence wrap of the second equation; a rewrite step is
a `congrArg` wrap; normalization chains steps with `TRANS`). See the reference file
for the full threading. A `simplify` pass removes `TRANS(REFL,·)`, `SYM(SYM ·)`, etc.,
keeping proofs small (148–436 chars on the sample set).

### 4.6 Reconstruction + the solver adapter

```python
def singleton_lean(eq1, goal_lhs, goal_rhs, goal_vars, tb=20.0):
    status, res = complete_pf(eq1, tb=tb)         # proof-carrying completion
    if status != 'collapse': return None
    s, t, P = res                                 # P proves  s = t  (distinct vars)
    sub = {s[1]: ('V','p'), t[1]: ('V','q')}      # instantiate collapse to p,q
    for v in other_vars(P): sub.setdefault(v, ('V','p'))   # any extra vars -> p
    Pi = simplify(inst_proof(P, sub))
    assert ptype(Pi) == (('V','p'), ('V','q'))    # final self-check before emit
    intro = "intro " + " ".join(goal_vars) if goal_vars else ""
    return (f"{intro}\n"
            "have key : ∀ (p q : G), p = q := by\n"
            "  intro p q\n"
            "  exact " + render(Pi) + "\n"
            f"exact key ({goal_lhs}) ({goal_rhs})")
```

Adapter to drop into `solver.py` (uses the solver's existing `goal_vars`,
`make_true_code`, `call_judge`, `trace`):

```python
def try_completion_singleton(problem, eq1_text, eq2_text, time_budget=25.0):
    gl, gr = eq2_text.split("=", 1)
    try:
        body = kc_singleton_lean(eq1_text, gl.strip(), gr.strip(),
                                 goal_vars(eq2_text), tb=time_budget)
    except Exception as e:
        trace(f"[completion] error: {e!r}"); return False
    if not body: return False
    return call_judge("true", make_true_code(body)).get("status") == "accepted"
```

Stage call in `main()`, right after the structural-singleton stage:

```python
    # Stage 2.7: deterministic ordered-completion singleton proof.
    if singleton:
        trace("[stage] completion singleton")
        if try_completion_singleton(problem, eq1, eq2, time_budget=25.0):
            trace("[accepted] completion singleton")
            return
```

**Inlining note:** the engine defines short helper names (`unify`, `parse`, `match`,
`replace`, …). `unify` collides with the solver's matching `unify` and the rest risk
future collisions, so namespace the whole engine with a `kc_` prefix when inlining
(the reference file already does this). Keep it as one block before `main()`.

---

## 5. Use case: `eq2377 → eq1139` end to end

Problem `normal_0227`:

```
Hypothesis Eq2377:  x = (y ◇ (z ◇ (x ◇ w))) ◇ y
Goal       Eq1139:  x = y ◇ ((y ◇ (z ◇ z)) ◇ z)
```

`forces_singleton(Eq1) = True` (no ≥2-element model exists — z3-confirmed up to
size 6). Completion collapses in 2 iterations. The reconstructed, self-checked Lean
the stage submits:

```lean
import JudgeProblem

def submission : Goal := by
  intro G _ h
  intro x y z
  have key : ∀ (p q : G), p = q := by
    intro p q
    exact (((h p p p p)).trans (((((h q p ((q ◇ p) ◇ (p ◇ ((p ◇ (p ◇ p)) ◇ p))) p)).trans
      ((congrArg (fun s => s ◇ p) (congrArg (fun s => p ◇ s) ((h (p ◇ (p ◇ p)) (q ◇ p) p p)).symm))))).symm))
  exact key (x) (y ◇ ((y ◇ (z ◇ z)) ◇ z))
```

Hand-check of the spine: `h p p p p : p = (p◇(p◇(p◇p)))◇p`. The bracketed term proves
the same right-hand side equals `q` (via one `h` instance rewritten under a
`p ◇ (· ◇ p)` context with `congrArg`, composed with another `h` instance), and
`.symm` flips it, so `p = … = q`. `key` is then applied to the goal's two sides.

## 6. Use case: coverage and the negative controls

Running the engine's *decision* half over `sample_20.json`:

| Outcome | Count | Notes |
|---|---|---|
| Collapse (singleton, solved) | 10/20 | eq ids 2034, 248, 1185, 701, 1808, **2377**, 2421, 3110, 30, 2581 |
| Saturate / not singleton | 10/20 | genuine ≥2-element models exist |

Every collapse was cross-checked against z3 (no ≥2-element model) and every
non-collapse confirmed to *have* one — **zero mismatches**, i.e. no false collapses.
Negative controls behave correctly: commutativity, associativity, both projections,
and idempotence all **saturate without collapsing** (they have non-singleton models),
so the engine does not "prove" singleton for laws that aren't.

End-to-end through an integrated build (mock judge that accepts the completion proof),
all 10 singletons were solved and none of the other 10 falsely triggered.

## 7. Use case: where completion does *not* apply (and the LLM's residual role)

- **Non-singleton TRUE implications** (`Eq2` follows from `Eq1` without collapse):
  point the *same* engine at proving `goal_lhs = goal_rhs` directly (seed the start
  term as `Eq2`'s LHS, target its RHS) instead of seeking a var=var collapse. This is
  a small variant of `singleton_lean`, not a new engine.
- **FALSE implications:** unchanged — the existing finite-model counterexample search
  handles these; completion just saturates and returns nothing.
- **Collapses needing terms beyond the size cap (`CEIL`):** raise `CEIL`/`maxp`/`tb`,
  or this is the one place an LLM *waypoint* (a conjectured intermediate lemma the
  engine then discharges, à la Draft-Sketch-Prove) could genuinely help. Treat any
  such hint as advisory: verify each hop, discard failures, and always run unguided
  completion in parallel as the floor. Correctness must never depend on the LLM.

---

## 8. Validation status — read before trusting

- **Validated here:** the engine's equational reasoning (machine-checked by `ptype`),
  the singleton/non-singleton decision (z3 cross-check), proof generation for all 10
  sample singletons, and end-to-end firing through an integrated build.
- **NOT validated here:** the **real Lean judge**. The dev sandbox has no Lean
  toolchain. Soundness of the *reasoning* is certain; the residual risk is pure Lean
  surface syntax (operator precedence, `congrArg` lambda form). The emitted syntax
  mirrors the solver's existing `add_congruence_edges` forms, but the first real run
  is the true test. If a proof is rejected it will be a syntax nit in `render`, not a
  logic error — the judge's message will point straight at it.

## 9. Operational gotchas worth fixing regardless

1. **Guard against syntax errors.** A committed `SyntaxError` (an unterminated
   docstring) once made `solver.py` fail to import, so every problem returned empty
   with zero calls — a whole 20-problem run silently zeroed. Add
   `python3 -m py_compile scripts/my_solver/solver.py` as a pre-run / pre-commit
   check. Separately, a file corrupted with NUL bytes produces the identical
   "empty solver output → `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`"
   failure on the harness side; the compile check catches that too.
2. **Robustify `read_message`.** It currently does `json.loads(line.strip())` with no
   guard; a blank line crashes it. Skip empty lines and exit cleanly on EOF.
3. **Recursion limit.** If you inline the engine, set a *modest* recursion limit
   (≈8000) and rely on the `CEIL` term-size bound — do not raise it to 10^6 (that
   converts a deep-recursion bug into a segfault, which the proxy then sees as empty
   output).

---

## 10. Files

- `docs/completion_engine_reference.py` — complete, tested, standalone engine.
  Run `python3 docs/completion_engine_reference.py` to print the `eq2377` proof.
  Call `kc_singleton_lean(eq1, goal_lhs, goal_rhs, goal_vars)` to get a Lean body, or
  `kc_complete_pf(eq1)` for just the decision + proof object.
- `scripts/my_solver/solver.py` — **unchanged baseline** (completion not integrated).
- `scripts/my_solver/completion_prototype.py` (+ `_coverage`, `_verify_z3`) — earlier
  decision-only prototype and the z3 cross-check harness, kept as supporting material.
```
