# S0 Paper Foundation Template

S0-PAPER-FOUNDATION initializes state, builds the factual base, screens framework-figure readiness, handles author supplementation, and locks unresolved risks before S1-FIGURE-STRATEGY runs.

Required sections when paper/source material is available:

1. Input material inventory.
2. Problem, assumptions, and contribution summary.
3. Method/algorithm/model pipeline.
4. Module inventory: input, output, role, dependency.
5. Training and inference flow.
6. Objective/loss/equation interpretation.
7. Terminology map: paper term -> figure label -> allowed shorthand.
8. Arrow semantics table.
9. Core innovation modules and internal mechanism evidence.
10. Heavily described, formula-backed, or explicitly improved mechanisms that need visual anchors.
11. Non-droppable core substeps.
12. Figure-relevant omissions and uncertainty.
13. Caption-supported facts, numbers, datasets, metrics, caveats, and formula explanations.
14. Framework-figure risk screen: missing information, contradictions, unsupported lineage, core-module opacity, and scope mismatch.
15. Author supplement request, if major/blocking issues remain.
16. Supplement integration log, if the user provides additional information.
17. Framework-figure risk register with downstream carry-forward instructions.
18. S1 strategy hints.

Required S0 output files:

- `outputs/S0-paper-foundation/paper-foundation-report.md`;
- `outputs/S0-paper-foundation/framework-figure-risk-register.md` when any risk, caveat, declined supplement, or scoped override exists;
- `outputs/S0-paper-foundation/author-supplement-request.md` when author information is needed;
- `outputs/S0-paper-foundation/supplement-integration-log.md` when author information is added after the first S0 read.

Required state key:

```text
s0_foundation_readiness_state.foundation_readiness_status
```

Allowed values:

- `S0_FOUNDATION_READY`;
- `S0_FOUNDATION_READY_WITH_RISK`;
- `S0_NEEDS_AUTHOR_SUPPLEMENT`;
- `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK`.

After S5, human decisions are outside this assistant workflow.

After S5, human decisions are outside this assistant workflow.

Default canvas is 16:9 unless the user requests another ratio.

Default S2 count is 8 sketches. Default S5 count is 6 formal candidates, with a maximum of 8. S5 candidates remain generated raster images. Their icons, arrows, colors, and caption plans should optimize paper meaning; SVG/PPT editability is secondary.
