# Source-Faithful Image Prompt Audit And Symbol Disambiguation Policy v3.2.15b

This policy is mandatory whenever S1 prepares S2 prompt packages, S4 prepares S5 prompt packages, or any upstream text stage creates image-generation instructions for a paper framework figure.

## Non-contradiction rule

No image-generation prompt may include an entity, module, role, variable, metric, formula, symbol, visible label, connector, arrow direction, port, fork/merge, topology, data flow, model flow, control flow, evaluation flow, generation relation, aggregation relation, training relation, or visual metaphor that contradicts the paper, supplement, user-provided source material, S0 deep-reading report, or risk register.

## Evidence or strict inference only

Every planned visible entity and every planned relation/line must be classified as exactly one of:

- `direct_source`: explicitly supported by a source anchor such as paper section, equation, algorithm, table, figure caption, supplement, user material, or S0 foundation report;
- `strict_logical_inference`: not directly drawn, but derived from source-supported premises through a short recorded inference chain;
- `revise`: currently ambiguous or underspecified and must be rewritten before image handoff;
- `remove`: unsupported, decorative, misleading, or contradictory and must be deleted before image handoff.

`revise` and `remove` entries block S2/S5 handoff. Visual convenience, common diagram conventions, or likely image-model behavior are not evidence.

## Symbol and label disambiguation

Symbols must not be mixed or overloaded. The same glyph, letter, color, line style, edge label, icon, or visual token must not refer to multiple paper concepts unless the prompt explicitly defines a source-supported aggregate/group and confirms no semantic loss. Distinct paper concepts must not be collapsed into one symbol if that changes a reviewer’s interpretation.

Variables, metrics, weights, thresholds, probabilities, losses, accuracies, model parameters, and pass-through artifacts are edge-label-eligible by default. They should appear on connectors, ports, forks, merges, or compact tags rather than as peer module boxes unless a source-supported exception is recorded.

## Prompt package outputs

Each S1/S4 prompt package must include:

- `source_faithfulness_audit` for visible entities and relation/line plans;
- `strict_logical_inference_ledger` for inferred relations;
- `symbol_disambiguation_audit` for glyphs, variables, labels, color semantics, line styles, and visual tokens;
- `prompt_contradiction_audit` that blocks handoff on contradictions, unsupported arrows, reversed directions, symbol collisions, or label drift.

The audit/repair loop is bounded to three cycles. If blockers remain, stop at a textual checkpoint plus residual-risk ledger rather than entering S2/S5 image-only generation.
