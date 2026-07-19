# Draft — §4.3 LLM evaluation (zero-result)

Paste-ready prose. Numbers current as of 2026-07-19; `other` rows folded into `malformed`
(they are `unparsable term` = syntactically invalid emitted terms). o3 excluded (output
starvation); Opus reported at its true n=2 after dropping 8 rate-limited rows.

---

## Headline numbers

| model | valid attempts | solved | invalid step | malformed |
|---|---:|---:|---:|---:|
| gpt-4.1 | 30 | **0** | 23 (77%) | 7 (23%) |
| o4-mini | 20 | **0** | 18 (90%) | 2 (10%) |
| Claude Opus 4 | 2 | **0** | 2 (100%) | 0 |
| **total** | **52** | **0** | **43 (83%)** | **9 (17%)** |

On the easiest tier specifically (wp = 2, the minimum refutation length in the corpus):
**0 / 24** across gpt-4.1 (n=20) and o4-mini (n=4).

o3 is excluded: 9 of its 10 responses returned no parseable answer because reasoning tokens
consumed the output budget. That is an API artifact, not a capability measurement.

---

## Prose

We evaluate on the deductive side of the task, where a solution is a proof that the law
forces triviality. The trivial side is the *easier* of the two channels — it is the side an
automated prover settles, and the side for which a Lean judge exists — so a zero here is the
stronger statement.

Instances are stratified by difficulty. We rank all 3{,}080 trivial laws by the length of the
refutation an automated prover finds, measured as the number of derived intermediate lemmas.
The distribution is wide: 125 laws are settled with two such lemmas, the median is six, the tail
runs past ninety, and 156 laws admit no refutation at all within the budget. We take the twenty
easiest instances, all at the minimum of two lemmas, so that difficulty is not a confound.

The evaluation is deliberately generous. Rather than ask a model to write a proof assistant
term, we remove the formalization burden entirely: the model emits only a chain of terms
connecting two arbitrary elements, and the harness searches for the law instance justifying each
step, assembles the proof — including congruence steps at arbitrary positions — and submits it to
the judge. We additionally reveal the intermediate lemmas the automated refutation passes through,
so the model is told the shape of the collapse it must reproduce, and the harness bridges coarse
steps by searching for short sequences of law applications between consecutive terms. In short,
the model is asked only to supply the mathematical path; every other burden is carried for it.

To ensure a zero is interpretable, we validate the pipeline with positive controls: a complete
worked instance is assembled and accepted by the judge with a clean axiom footprint, and the
congruence construction the assembler emits is separately type-checked. The harness therefore
demonstrably accepts correct answers, and a zero cannot be attributed to the grader.

Under these conditions no model produces a single verified solution. Across 52 valid attempts
spanning three model families the solve rate is zero, and it is zero on the easiest instances in
the corpus. The failure is not marginal: in 83\% of attempts the submitted chain contains a step
that is not an instance of the law at all — most commonly a direct jump between the two arbitrary
elements, which no single application can justify. The remaining 17\% are syntactically malformed
terms. Models do not fail by finding a nearly-correct derivation and stumbling on formalization;
they fail by producing objects that resemble derivations without being them.

We read this as a *derivation-bound* result, and we separate it from three alternatives we
eliminated in turn. It is not instance difficulty: the same models fail at the minimum difficulty
rung. It is not formalization: the models never write a line of proof-assistant syntax. It is not
tooling: the controls establish that correct answers are accepted. What remains is the ability to
produce a valid multi-step equational derivation, which is precisely the capability the benchmark
is designed to isolate.

Two caveats bound the claim. We report a floor, not a ceiling: stronger or differently-prompted
systems may clear it, and our Opus figure rests on only two uninterrupted attempts. And the result
speaks to the deductive side; the construction side, where a solution is an infinite model rather
than a proof of collapse, is harder still and remains open for every method we test.

---

## Notes for whoever edits this

- Do NOT report o3 as 0/10 — it is excluded, with a footnote. Reading its malformed rate as a
  capability signal is wrong and a reviewer will catch it.
- Do NOT report Opus as 0/10 — it is n=2 after excluding rate-limited rows.
- The "0/24 at wp=2" line is the strongest single sentence; it is what kills the "your instances
  were too hard" objection.
- Keep the claim scoped to the models and prompting tested. The honest framing is a floor.
