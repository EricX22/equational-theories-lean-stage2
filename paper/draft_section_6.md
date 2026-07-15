# Draft — Section 6

First-draft prose for the empirical core. All numbers are frozen results; sources noted
in `% comments` for your checking, to be deleted before submission.

---

## 6. The Baseline and the Hard Tier

The hard tier of the benchmark is not a fixed list of laws but a property relative to a
named method: an admissible law belongs to the hard tier when a published, reproducible
portfolio of automated provers fails to resolve it — fails to prove it trivial and fails
to construct a nontrivial model — within a stated budget. This section defines that
portfolio, reports how the tier behaves under it, and establishes the two facts the
benchmark rests on: that the frontier is bounded by *method* rather than by *compute*,
and that it is not an artifact of any single prover.

### 6.1 The portfolio

A single prover under a single term ordering is not a baseline; it is a shrug. A law
whose completion diverges under one reduction ordering may terminate under another, so a
defensible baseline must range over provers, orderings, and budget. Portfolio v1.0
comprises eight configurations: Vampire~5.0.1 in five modes — three proof-search
configurations targeting $L \models x = y$ (`casc`, `casc` under LPO, and the `discount`
saturation loop) and two saturation configurations testing consistency
(`otter` under KBO and under LPO) — the E prover in a proof and a saturation mode, and
Twee~2.6.1, an implementation of unfailing completion purpose-built for the unit
equational fragment in which every law of our corpus lives. Each configuration is run
over a budget ladder of $30, 60, 120, 300,$ and $600$ seconds, and a law is recorded as
resolved as soon as any configuration returns a verdict, whereupon the remaining ladder
is skipped.

The two directions of the task are found by different machinery, and the portfolio must
contain both: a proof of triviality is proof search, whereas a nontrivial model is
witnessed by a saturation closing — a saturated clause set in this fragment *is* a
ground-convergent rewrite system and hence an explicit model~\cref{cite:jrs}. A portfolio
that only refutes would never find the second kind of answer. Every verdict is mapped
from the prover's SZS status line, and a `Satisfiable` verdict from a strategy that
sacrificed completeness is discarded rather than trusted. Provers, versions, and exact
flags are pinned in a container image released with the benchmark, and the harness
refuses to run unless a known-answer self-test passes.

### 6.2 The tier is method-bound, not compute-bound

The central empirical question is whether the hard tier is genuinely beyond the reach of
these methods or merely under-budgeted. The two are separable by measurement: run the
ladder and record, at each budget, the fraction of laws resolved. If resolution keeps
rising with budget, the frontier is a matter of compute; if it flattens, the surviving
laws are bound by what the methods can express, not by how long they run.

Over a sample of 120 laws from the no-finite-model tier, the portfolio resolves three
laws at 30 seconds and *not one additional law at any higher budget*:

% source: paper/results/baseline_v1.jsonl, portfolio d4ee2fb7, 2026-07-10
$$
\begin{array}{lrl}
\text{budget} & \text{resolved} & \\
30\text{ s}   & 3/120 = 0.025 & \\
60\text{ s}   & 0/117 = 0.000 & (\Delta = -0.025)\\
120\text{ s}  & 0/117 = 0.000 & (\Delta = 0)\\
300\text{ s}  & 0/117 = 0.000 & (\Delta = 0)\\
600\text{ s}  & 0/117 = 0.000 & (\Delta = 0)\\
\end{array}
$$

Twenty times the compute buys nothing. This licenses the definition we adopt: the hard
tier is the set of admissible laws left unresolved at the ladder's maximum budget under
*every* configuration, and the flatness of the curve past 30 seconds is the evidence
that this maximum lies beyond the knee rather than short of it. We report the curve, not
a single timeout, precisely so this judgment is checkable.

A prior single-prover measurement points the same way and rules out the most deflationary
explanation. Re-running the corpus's earlier classifier at 300 seconds per prover, an
order of magnitude above its original budget, converted 3.7% of laws — and of the 216
no-finite-model laws in that pass, four became provably trivial while *none* acquired a
nontrivial model.
% source: paper/results/retry_curve.py output, 2026-07-09
The laws that resisted the shorter budget resisted the longer one on the construction
side without exception; the only movement was the removal of trivial laws the shorter
budget had failed to prove trivial (\cref{sec:contamination}).

### 6.3 The frontier is not an artifact of one prover

Flatness under a portfolio could in principle hide a weakness common to all its members.
The sharpest test available is Twee, whose completion procedure is algorithmically
distinct from Vampire's and E's superposition and is the tool most likely, on prior
grounds, to complete a system the others leave open. It does complete systems the others
find awkward — on one of the two order-five laws we later close
(\cref{sec:closed-cases}), Vampire's saturation runs to 357 clauses while Twee's
unfailing completion terminates in seconds. Yet across the sampled tier, Twee resolves
*no* law that the rest of the portfolio does not, and in particular contributes no new
nontrivial model. The reshaping outcome we explicitly tested for — a law solved only by
completion, which would have shown the tier to be an artifact of Vampire's search rather
than a genuine frontier — does not occur. Twee is a strong member of the portfolio, not a
key to the tier.

### 6.4 Contamination and what resolution means here

Every law the portfolio does resolve, it resolves as *trivial*: of the sampled tier,
eleven laws are proved to satisfy $L \models x = y$, and zero acquire a nontrivial model.
% source: baseline_v1.jsonl — 11 TRIVIAL, 0 AUSTIN of 120
These trivial laws are contamination rather than error. They are admissible — they have
no nontrivial finite model — and the shorter classifier budget had failed to prove them
trivial, so they sat in the no-finite-model tier without being Austin. The stronger
portfolio removes them, and the two-sided task is exactly what makes this harmless: a law
that turns out trivial is a legitimately answered instance, not a mislabelled one. The
completion provers carry more of this load than Vampire's proof modes — one law is proved
trivial by E in one second and by Twee in twelve while all five Vampire configurations
exhaust thirty seconds — which is a second, quieter argument for a portfolio over a single
strong prover.

That the portfolio produces zero new models is therefore the result to hold onto. The
hard tier's construction side is untouched by the strongest automated methods we can
assemble, across orderings and an order of magnitude of budget, while every instance in
it is certified to possess an answer (\cref{sec:task}). The gap between *an answer exists*
and *this portfolio finds it* is the quantity the benchmark measures.

### 6.5 Scope of the measurement

The 120-law figure is a sample of the roughly 3,400 no-finite-model laws in the current
corpus, and it is sound for a *rate*: the shape of the resolution curve and the absence of
completion-only models are properties of the population, estimated without bias by the
sample. It is not the tier's *membership list*. Publishing the definitive hard tier — the
exact laws that survive portfolio v1.0 at maximum budget — requires the full sweep, a
single long run we schedule once the ladder and portfolio are frozen, since its cost is
dominated by the laws that never resolve and therefore traverse the entire ladder. The
membership list refines the artifact; it does not change the method or the rate reported
here.
