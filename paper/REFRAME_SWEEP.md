# Reframe-Consistency Sweep — find→replace list for Overleaf

Audited against the current compile (`Eric___AAAI_27 4.pdf`, confirmed current
2026-07-24). Find strings are given as rendered text; in the tex, line breaks,
`---`, and math may differ, so search on a distinctive substring. Ordered by
section. Items marked **DECISION** need a call from you before applying.

---

## A. Term sync (invention → valid creativity)

1. **Table 1 caption (tab_gap)**
   FIND: `Each property removes one confound in measuring invention`
   REPLACE: `Each property removes one confound in measuring valid creativity`

2. **Table 1 caption, closing clause**
   FIND: `but measuring invention requires all three`
   REPLACE: `but measuring valid creativity requires all three`

3. **§3.2 Deduplication**
   FIND: `no invention is credited twice`
   REPLACE: `no solution is credited twice`

4. **§3.2 (admissibility paragraph, last sentence)**
   FIND: `only by inventing a model or proving triviality`
   REPLACE: `only by constructing a model or proving triviality`

5. **§3.1 (optional — plain-verb use is permitted, but "constructing" matches
   the construction-channel terminology)**
   FIND: `means inventing an infinite magma tailored to the individual law`
   REPLACE: `means constructing an infinite magma tailored to the individual law`

6. **§2.1 closer (Related Works)** — "genuine" is a rule-7 intensifier; this
   also syncs the closer to the three defined properties.
   FIND: `objective scoring, endless renewal, and a demand for genuine construction`
   REPLACE: `objective scoring, endless renewal, and a constructive task that no
   known general procedure solves`

7. **§2.1 (synthetic-puzzles paragraph)** — drop the intensifier.
   FIND: `rather than to truly construct a creative solution`
   REPLACE: `rather than to construct a creative solution`

## B. Banned terminology and antithesis budget

8. **§4.2** — "horns" is retired; the fixed terms are checks (a) and (b).
   FIND: `Every attempt satisfies one horn of the certificate; none satisfies both.`
   REPLACE: `Every attempt passes exactly one of the two checks; none passes both.`

9. **§3.3 opener** — a second antithesis; the abstract holds the paper's single
   allocation ("not compute, but the absence of any method...").
   FIND: `A solved ALPS instance is a verified mathematical fact, not a predicted label.`
   REPLACE: `Each solved ALPS instance is a machine-verified mathematical statement.`

10. **§4.2 closing sentence** — antithesis + personification ("yields to
    nothing"). Coordinate with item 15, whose deleted clause moves here.
    FIND: `The asymmetry of the task thus reappears one level up: the deductive
    side yields, modestly and under support, to the strongest reasoning model we
    test; the construction side yields to nothing.`
    REPLACE: `This outcome mirrors the automated baseline. The strongest
    reasoning model we test produces verified proofs on the trivial side under
    supported settings; no method we run — prover, completion, or reasoning
    model — produces a certified construction.`

## C. De-punch (retired register)

11. **§3.3 (single-judge paragraph)** — drop the flourish clause; the descent
    argument that follows carries the point.
    FIND: `A single Lean judge for both sides is not available, for a reason that
    strengthens the benchmark's premise.`
    REPLACE: `A single Lean judge covering both sides is not available.`

12. **§4.2** — listed BAD example in the style guide.
    FIND: `The construction side stays at zero, and the way it stays there is the finding.`
    REPLACE: `No construction attempt certifies, and the failures follow a
    consistent pattern.`
    (The existing "In 23 of 25 attempts..." sentence then follows as evidence.)

13. **§4.2** — dial metaphor.
    FIND: `Solves exist only toward the top of both dials`
    REPLACE: `Solves occur only at full support and medium reasoning effort`

14. **§4.2** — personified oracle; also contains the vendor claim (see item 26).
    FIND: `the verification oracle does real work, and the capability tracks
    reasoning tier rather than vendor or prompt`
    REPLACE: `most solves complete on the second or third feedback round, and
    success tracks reasoning tier`
    **DECISION:** keep `rather than vendor` only if the Gemini cert-63 run
    happens (~$5–8 budget remains); otherwise it is unsupported with three
    OpenAI models.

15. **§4.2** — intensifier "precisely"; the "nothing we ran" clause moves to
    item 10's replacement.
    FIND: `Inventing a structure strong enough to entail the law yet loose enough
    to keep two elements apart is precisely the synthesis the benchmark isolates,
    and nothing we ran — prover, completion, or reasoning model — achieves it.`
    REPLACE: `Constructing a presentation strong enough to entail the law while
    remaining consistent with a ≠ b is the synthesis the benchmark isolates.`

16. **§4.2 (instance-selection paragraph)** — "blamed" + "almost instantly"
    (rule 7: intensifiers need numbers).
    FIND: `A zero on this set cannot be blamed on the instances — the answers
    exist, are short, and are found by uninformed search almost instantly.`
    REPLACE: `A zero on this set is attributable to the model rather than the
    instances: each answer exists, is at most a few law applications long, and is
    found by uninformed search in under five seconds.`

17. **§4.3 opener** — rhythm sentence.
    FIND: `The floor is not without content.`
    REPLACE: `The resolved set contains a result of independent interest.`

18. **§4.3** — "floor's edge" is a listed offender; aphorism shape.
    FIND: `The pipeline, pointed at the literature, returns a new fact — but the
    portfolio reaches it, so the case marks the floor's edge, not the frontier.`
    REPLACE: `The result is new to the literature, but the automated portfolio
    reaches it, so the case lies within the resolved tier rather than the hard tier.`

19. **§4.3**
    FIND: `which is precisely the ground-confluence obstacle`
    REPLACE: `which is the ground-confluence obstacle`

20. **§1 ¶1** — informal phrasing.
    FIND: `reason through problems and come up with creative solutions`
    REPLACE: `reason through problems and produce creative solutions`

21. **§1 properties ¶ (optional)** — slightly above the KDD register line.
    FIND: `Construction is the property that takes work to secure.`
    REPLACE: `Construction is the property that must be established by design.`

## D. Mechanical

22. **Spaced hyphens rendering as " - "** (should be `---` in tex). Occurrences
    spotted: §1 ¶1 `real world - formalizing`; §1 ¶1 `materials - AI-for-science`;
    §1 walk-through `executed - specification, construction, and verification -`;
    contributions bullet `channels - a Lean proof ... certificate ... - with no
    human in the loop`; §2.3 `algebra - the identities`; §3.2 `recursive - laws
    confirmed Austin at order n seed the round at order n + 1 - so`. Search the
    tex for ` - ` globally.

23. **Possible truncated sentence at Eq. (3):** the compile renders literally
    `Figure 3 ...` before the two prover queries. Verify in Overleaf that the
    paragraph introducing checks (a)/(b) is complete (e.g., "Figure 3 walks
    through both checks on a toy law. Formally, the judge issues two queries
    (Kovács and Voronkov 2013):").

24. **§5 Discussion is an empty header** and there is no Conclusion — expected
    (both TODO), noting so the compile isn't mistaken for complete.

## E. Numbers — three snapshots currently disagree (**DECISION / after frozen sweep**)

25. The paper currently mixes:
    - Abstract + intro validation ¶: 2.5% resolved, +0.1% at 20× budget, 4,141 pool
      (%PROV registry extrapolation; registry also had resolved 111, hard 4,030 = 97.3%,
      ladder 105/109/110/111/111).
    - §4.1 + Table 3: 90 residual resolutions (2.2% of residual), 73 at 30 s + 17
      later, models 4+0+0+0+0, trivial 69/7/4/3/3, hard tier 4,051 (97.8%).
    When the frozen sweep is final, sync in one pass: abstract, intro ¶7,
    §4.1 ¶2/¶4, Table 3, Figure 4 labels, and every 97.x%. Keep the abstract/intro
    pair matched to the BUDGET split (30 s rung vs added later), per the registry note.

26. **Figure 4 label conflict:** the flow figure labels the 4,141 block
    `Hard Tier: 4,141 Laws`, while §4.1 defines the hard tier as the post-sweep
    4,051. Rename the block (e.g., `Admissible residual: 4,141 laws`) or align the
    definitions. **DECISION.**

27. **Abstract "14% of instances on the proof side"** = single-run 9/63. The §4.2
    rewrite moves to pass@1 + per-law solve probability (repro: 1/9 reproduced,
    1/5 new, 10 distinct laws across runs). Decide the abstract's phrasing (e.g.,
    "solves 14% at pass@1") so abstract and §4.2 state the same quantity. **DECISION.**

28. **Float plan:** state doc says tab_frontier replaces tab:curve (the current
    budget-ladder Table 3) — confirm whether Table 3 in this compile is the
    to-be-deleted tab:curve or already tab_frontier.

## F. Rewrites pending (not find→replace)

29. **§4.2 wholesale rewrite** (current text predates both the repro run and the
    style correction): pass@1/stochastic-solve framing; ablation downgraded to
    suggestive (current "locates what the solves depend on" overclaims — 4/9
    no-waypoints is within run noise of the 1/9 rerun); clean signals stated as
    such (effort-low 0 every run; GPT-4.1 and o4-mini 0 at every setting;
    construction 0 everywhere); weak-model construction breakdowns (o4-mini 0/25:
    10 both-fail / 11 entail-collapse / 4 weak; GPT-4.1 0/25: 3 / 9 / 9 —
    re-derive tallies before publication); cost sentence; seed-distinctness
    pointer; unpublished-instances sentence; launch-condition closer. Also reduce
    em-dash density (several paragraphs exceed one pair).

30. **§3.3 construction channel:** the semantic reading of E is merged; the rest
    of the drafted clarity rewrite (syllogism; "the prover never reasons about
    infinity") is not — confirm and merge. Negative-controls sentence pending
    (verify actual gate contents first).

31. **Captions on deck:** fig_failed_submission ("bound by method, not budget")
    and tab_frontier ("the rule that erases...") carry old-register lines — fix
    when placing those floats.

32. **§5 Discussion + Conclusion:** anchors per the state doc — valid-creativity
    scope concession (certifies the artifact/task conditions, not cognition);
    falsifiability + renewability (automated tailoring retires those laws; the
    generator mints past them); ground confluence as the companion-work boundary;
    hard-tier interior un-censused; chain-length ladder as a designed future rung;
    what methods the benchmark motivates (satisfy-the-law-without-collapse
    tension); hard-tier meaningfulness via provenance (reviewer point 3, still
    OPEN — contained ETP open problems; settled 12857/33436).
