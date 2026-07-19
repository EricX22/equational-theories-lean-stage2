# Draft — Sections 3 and 4

First-draft prose for the two most settled sections. Register is academic; math in
inline LaTeX-ready notation. Edit freely — this is a page to react to, not a final.

> **STALE (2026-07-17 pivot):** the "an answer is a Lean proof / the space of Lean proofs" framing
> below is superseded — judging is multi-channel (TRIVIAL = Lean proof; AUSTIN = Vampire-certified
> presentation `E`). No Austin model is an arithmetic formula (descent theorem). Rewrite the
> judging paragraphs against `TASK_AND_JUDGING.md` before using this prose.
Placeholders in `\cref{}` style point at figures/sections to be numbered later.

---

## 3. The Task

We work with magmas: a set $M$ equipped with a single binary operation
$\diamond : M \times M \to M$, with no further axioms. An *equational law* is a
universally quantified identity $L : x = T[x, y, z, \dots]$, where $T$ is a term built
from the variables and $\diamond$. A magma *satisfies* $L$ when the identity holds for
every assignment of its elements to the variables. Throughout, the fixed target of
interest is the law $\mathrm{Eq}2 : x = y$, which a magma satisfies exactly when it is
trivial (has a single element); we write $L \models x = y$ for the semantic implication
that every model of $L$ is trivial.

The benchmark is built entirely from laws carrying a machine-checked certificate of a
single structural fact.

> **Definition (admissible instance).** A law $L$ is *admissible* if there is a proof
> that $L$ has no nontrivial finite model: every finite magma satisfying $L$ is trivial.

This certificate is not a result of the benchmark; it is the ticket of admission, and it
is what makes the task well-posed. We produce it with a first-order argument — a
subterm of $T$ containing every occurrence of $x$ acts as a left inverse and is therefore
injective, so on a finite carrier it is surjective, and surjectivity of the relevant map
collapses the magma — mechanised as a query discharged by an automated prover. The
argument is a specialisation of Infinox's method for establishing finite
unsatisfiability~\cref{cite:infinox}, and we claim no novelty for it beyond the
observation that, for the syntactic shape $x = C[S(x)]$, the left inverse is available
without search.

Admissibility has a consequence that turns an open problem into an answerable question.

> **Proposition (dichotomy).** For every admissible $L$, exactly one of the following
> holds: (a) $L \models x = y$, i.e. the implication into $\mathrm{Eq}2$ is valid and
> $L$ is *trivial*; or (b) $L$ admits a nontrivial model, and every nontrivial model of
> $L$ is infinite — $L$ is an *Austin law*.

The proof is immediate from admissibility together with the completeness of first-order
logic: if $L \not\models x = y$ then $L \cup \{\exists u\, v.\ u \neq v\}$ is consistent
and so has a model, which by admissibility cannot be finite. Austin laws — laws with
infinite models but no nontrivial finite one — exist only at order five and
above~\cref{cite:kisielewicz}, which is precisely why the finite regime cannot exhibit
them and why a finite model builder, one of the two standard tools, is inapplicable to
this family by theorem rather than merely slow.

The dichotomy licenses a two-sided task.

> **The task.** Given an admissible law $L$, either exhibit a nontrivial model of $L$
> together with a machine-checkable proof that it satisfies $L$, or prove
> $L \models x = y$.

Exactly one side is achievable, both are machine-checkable, and — this is the point that
distinguishes the construction here from an open-problems list — *no instance is
unanswerable*. The admissibility certificate, combined with the dichotomy, guarantees
that every instance has a determinate answer of one of the two kinds. This is a stronger
guarantee than a benchmark can usually offer: the difficulty of an instance is bounded
below by the effort a solver must expend, never by the possibility that the instance is
ill-posed or the answer nonexistent.

We stress what is deliberately *not* a design criterion: solvability. An instance that no
current method resolves still discriminates between methods, and an instance whose answer
is unreachable in principle would be a defect, but the two are far apart. Every
answer here is a finite object — a Lean proof — and the space of Lean proofs is
recursively enumerable, so no admissible instance is unsolvable in principle; it is only
hard relative to a fixed, named method. Hardness relative to a published baseline is the
normal and sufficient notion for a benchmark, and it is the one we adopt
(\cref{sec:baseline}). Conversely, the benchmark is not vacuous merely because its hard
tier is unresolved: the certificate guarantees that the resolution exists.

## 4. Verification

A benchmark of construction problems is only as meaningful as its ability to check a
proposed construction. We make the checker unconditional by fixing a single arbiter: an
answer is a proof in the Lean proof assistant of a statement we generate mechanically
from the law, and the proof is accepted exactly when Lean's kernel accepts it and its
logical dependencies lie within a fixed allowlist. Nothing about the *form* of the model
— whether it is presented as a subset of the integers, a quotient of a term algebra, or
a rewrite system — enters the judge; any Lean proof of the generated goal is a valid
answer.

For a law $L : x = T$ with variables $x, y, z, \dots$, the judge emits the definitions

$$
\mathrm{Law}(\diamond) \;\equiv\; \forall x\, y\, z\, \dots \in M,\ x = T[\diamond],
$$
$$
\mathrm{AustinGoal} \;\equiv\; \exists\, (M : \mathrm{Type})\, (\diamond : M \to M \to M),\ (\exists\, a\, b : M,\ a \neq b) \wedge \mathrm{Law}(\diamond),
$$
$$
\mathrm{TrivialGoal} \;\equiv\; \forall\, (M : \mathrm{Type})\, (\diamond : M \to M \to M),\ \mathrm{Law}(\diamond) \to \forall\, a\, b : M,\ a = b.
$$

A submission proves one of the two goals. The nontriviality clause $\exists a\, b.\ a
\neq b$ is what forces an Austin answer to exhibit two distinct elements — and, together
with admissibility, what forces the witnessing magma to be infinite — while keeping the
statement itself finiteness-free, so that a submitted model is a genuine model regardless
of whether the admissibility prover was correct.

The judged artifact is the concatenation of a generated header, the submitter's body, and
a generated footer. The header fixes the statement; the footer closes with
`example : Problem.AustinGoal := solution`, which forces the submitter's `solution` to
elaborate at exactly the type the header defines. The submitter never writes the
statement and therefore cannot weaken it. Two safeguards make this airtight. First, a
textual gate run before Lean rejects the escape hatches that would let a file typecheck
without proving the intended proposition: `sorry` and `admit`; `native_decide`, which
discharges goals by trusted compiled code outside the kernel; user-declared `axiom`s; the
metaprogramming constructs (`macro`, `syntax`, `elab`) that could redefine notation; and,
most importantly, any redefinition of the generated names, since the characteristic
attack is to shadow `AustinGoal` with a trivially true proposition and prove that
instead (\cref{fig:shadow-attack}). Second, after Lean accepts the file, the judge reads
the axiom footprint printed by `#print axioms solution` and requires it to be a subset of
$\{\texttt{propext}, \texttt{Quot.sound}, \texttt{Classical.choice}\}$; the appearance of
`sorryAx` or the `native_decide` axiom, or of any axiom outside the allowlist, is a
rejection even when the file compiled. The allowlist is closed rather than a blocklist of
known cheats, so an unforeseen axiom fails by default.

We have verified the judge end to end against a reference answer — a two-element magma
satisfying a simple admissible law — which passes the textual gate, elaborates against
the generated goal, and exhibits the expected axiom footprint; the negative controls
(a `sorry`ed proof, an axiom smuggle, and both the namespaced and bare forms of the
shadowing attack) are each rejected before Lean runs.

Two channels for producing accepted proofs already exist. Concrete algebraic models — a
finite ring, a $\mathbb{Z}$-module, an adjoined-root extension — are checked directly:
the model's operation is a Lean definition and the law is discharged either by a symbolic
identity or, for small carriers, by kernel computation. This is the channel by which a
previously open order-five instance was closed by a mod-17 affine model
(\cref{sec:closed-cases}). The second channel, and the one that reaches the hardest
instances, presents the model as the term algebra modulo a convergent rewrite system
derived from a prover saturation; certifying such a model in Lean requires formalising
ground confluence of ordered rewriting, which we have reduced to a single open lemma in
an otherwise complete development (\cref{sec:formalisation}) and which we treat as the
subject of a companion paper. The judge itself is agnostic to this: it is sound today for
every answer a submitter can drive through the kernel, and widening the set of *easily
producible* answers is a matter of building solver-side tools, not of changing the
arbiter.
