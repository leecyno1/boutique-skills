# Strict Source-Grounded Modular Prompt Contract Policy v3.2.15b

This policy is mandatory whenever S1 prepares S2 image prompts, S4 prepares S5 image prompts, or any authorized text-only upstream stage creates or modifies a prompt package for a framework, architecture, pipeline, system, data-flow, or method figure. It is generic and must not encode any paper-specific module names, variables, datasets, or topology facts in the reusable skill package.

## 1. Hard Scope

Prompt packages must produce modular framework figures, not fragmented collections of small boxes, decorative posters, experiment dashboards, or duplicated explanation panels. Style choices may change the surface treatment, but they may not weaken modularity, source grounding, connector evidence, edge-label-first variable placement, or simplicity of internal motifs.

## 2. Evidence-Gated Connector Contract

Every arrow, line, connector, bus, fork, merge, and loop must be supported by the current paper/materials for both endpoint direction and transferred meaning.

For every planned connector, the S1/S4 prompt package must record an `edge_support_ledger` row with:

- upstream module/block or source context;
- downstream module/block or target context;
- transferred quantity or relation;
- connector style and arrowhead choice;
- source evidence anchor: paper section, equation, algorithm step, table/figure caption, supplement, S0 foundation report, or author/user source material;
- verdict: `pass`, `revise`, or `remove`.

Unsupported connectors must be removed, merged into a non-directional grouping only when the source supports association but not direction, or rewritten with correct source-supported direction. Decorative or speculative arrows are forbidden.


## 2A. Source-Faithful Prompt Audit And Symbol Disambiguation

Before any S1/S4 image prompt package is handed to S2/S5, every visible entity, label, symbol, module, relation, and connector must pass a source-faithfulness audit. A prompt item is allowed only when it is either directly supported by the paper/materials/S0 report or derived by a recorded strict logical inference from supported premises. Unsupported, contradictory, ambiguous, or decorative items must be revised or removed before image generation.

The prompt package must include `source_faithfulness_audit`, `strict_logical_inference_ledger`, and `symbol_disambiguation_audit`. These records must cover at least visible modules, arrows/lines, edge labels, ports, variables, metrics, formulas, icons, color semantics, line styles, and repeated entity markers.

Symbols cannot be mixed or overloaded: the same glyph/color/label/line style must not represent multiple paper concepts, and different paper concepts must not be collapsed into one symbol unless a source-supported aggregate/group is declared and semantic loss is explicitly ruled out. Variables, metrics, weights, thresholds, probabilities, losses, accuracies, model parameters, and pass-through artifacts remain edge-label-eligible by default and should live on connectors/ports/forks/merges/tags rather than peer module boxes.

If the audit finds a paper contradiction, unsupported relation, reversed arrow direction, ambiguous symbol, or label drift after the bounded repair loop, stop at a residual-risk checkpoint and do not hand off to image generation.

## 3. Connector Multiplicity And Bundling

Between any two block-level modules, default to one bundled connector.

Multiple connectors between the same two block-level modules are allowed only when each connector carries a different, explicitly labeled transfer quantity or relation, such as data/artifact flow versus model/state exchange versus score/weight flow.

Forbidden connector patterns:

- several unlabeled lines between the same two blocks;
- repeated arrows that carry the same or similar meaning;
- parallel connectors used for visual richness rather than source-supported distinct transfer;
- one connector per variable when a labeled bus or fork/merge label would suffice.

If distinct transfers exist, label each line directly on the edge and make the line style explainable in the legend. If the difference is not source-supported, merge the lines.

## 4. Edge-Label-First Variable Placement

Variables, artifacts, scores, weights, thresholds, parameters, temporary states, and intermediate outputs that are transferred between modules must be written on connectors, ports, forks, merge points, or small tags. They must not become peer standalone module boxes unless the source material treats the item itself as a primary method component and S1/S4 explicitly justifies that exception.

Default render roles:

- datasets/artifacts: edge labels, port labels, fork labels, or merge labels;
- scores/weights: dotted edge labels;
- thresholds/gates: small gate tags;
- model states: small state tags or dashed exchange labels;
- repeated entities/agents/samples/views: compressed group cue, exemplar, brace, or ellipsis unless variant-specific operations are source-supported.

Each prompt must include a visible instruction that inter-module variables live on lines/ports/tags, not inside block interiors as independent peer modules.

## 5. Modular-Not-Fragmented Figure Structure

The figure must be organized around a small set of source-grounded primary modules. Primary modules should remain visually stable containers with compact internal motifs. The prompt must not split a coherent method module into many scattered micro-blocks unless the paper itself defines those micro-blocks as separate primary modules.

Required modularity gate:

- list primary modules;
- list optional internal substeps under each primary module;
- mark which internal substeps are shown as compact glyphs or short labels;
- ensure variables and micro-operations do not become separate equal-rank modules;
- ensure the figure can be read as a framework map at first glance.

This rule is compatible with all style options. A low-fidelity sketch can still be modular; a formal schematic can still be simple and non-fragmented.

## 6. Simple, Reviewer-Recognizable Internal Motifs

Internal submodule diagrams must be simple enough to express the idea without becoming a second full workflow. Prefer widely recognized visual conventions that reviewers can decode quickly:

- classifier/model: compact network glyph, decision boundary, or labeled model card;
- data augmentation: small transform/variant glyph;
- prediction/probability: small bar chart or probability vector;
- filtering/thresholding: gate/funnel/checkmark motif;
- aggregation/consensus: weighted sum, merge node, or bundled neighbor-model bus;
- generative/sampling process: simple latent-to-samples or diffusion/noise-step motif;
- evaluation/scoring: small checklist, metric tag, or score edge;
- update/next round: one light loop or state tag.

Forbidden internal-motif patterns:

- dense miniature algorithms inside every block;
- numeric tables unless the table is the target figure;
- multiple repeated histograms/plots when one icon communicates the operation;
- a magnified inset that repeats the same details already visible in the parent module;
- overly decorative or uncommon metaphors that reviewers may misread;
- submodule diagrams more complex than the main module they explain.

## 7. Entity-Variant Compression And Process Instance Budget

Before prompt-index creation, S1/S4 must run `references/entity-compression-and-active-stage-navigation-guard-policy-v3215a.md`. Every repeated entity family must be classified as `context_marker`, `shared_process_instance`, `true_process_branch`, `comparison_target`, or `nonvisual_context`. Only `true_process_branch` and `comparison_target` may become multiple full process lanes.

Every candidate must record `process_instance_budget`. The default is exactly one canonical process and one visible instance of each primary process step. Extra full process instances require source evidence for different operations, different input-output contracts, different phases, or explicit comparison intent.

Every image prompt with repeated entities must include a positive multiplicity lock: draw exactly one canonical process unless source evidence justifies distinct branches; show repeated entity families only as compact markers, grouped tokens, braces, legends, ellipses, or other compressed cues.

S1/S4 must record `variant_to_lane_risk_audit` and `adversarial_generation_risk_audit`. A high residual risk blocks image-only handoff until repaired or recorded as residual risk.

## 8. Redundancy And Workflow Duplication Ban

Do not repeat the same workflow multiple times in one image. A mechanism can be shown at one detail level by default:

- detailed main module, with no duplicate zoom; or
- simplified main module plus one connected zoom/cutaway that adds new source-grounded information not already shown.

If a zoom/cutaway is used, the parent module must be simplified. If the parent module already shows the detail chain, do not enlarge the same chain elsewhere.

Duplicate full pipelines, duplicate icons, duplicate textual explanations, repeated workflow lanes, repeated legends, and repeated side panels must be removed or compressed unless each visible repetition carries distinct source-supported meaning.

## 9. Background Context Budget

Problem context, motivation, constraints, dataset examples, role lists, and background panels must remain a small support area. They must not dominate the figure.

Default priority order:

1. model/framework mechanisms;
2. source-supported transfer relations;
3. compact necessary context and boundaries;
4. legend and minimal notes.

A prompt must explicitly state that background/context is minor and that the method framework is the visual focus. Do not turn a framework figure into a poster, story board, or broad infographic unless the user explicitly asks for that direction and S1/S4 still passes all source-grounding gates.

## 10. Mandatory S1/S4 Audit And Repair Loop

S1 and S4 must audit every generated prompt package before writing the prompt-index or before exposing the image-only handoff. The audit must include:

- `edge_support_ledger`;
- connector multiplicity and bundling check;
- variable placement / edge-label-first check;
- modularity-not-fragmentation check;
- simple internal motif check;
- workflow redundancy check;
- entity variant classification check;
- process instance budget check;
- multiplicity positive lock check;
- variant-to-lane risk audit;
- adversarial generation risk audit;
- background/context budget check;
- source-evidence consistency check;
- forbidden-content check;
- prompt contradiction / hallucination audit.

If any blocker fails, revise the prompt package and audit again. Run at most three cycles:

1. audit → revise;
2. audit → revise;
3. audit → final verdict.

If blockers remain after the third cycle, do not proceed into image generation handoff. Write a residual-risk ledger and stop at a textual checkpoint or ask for user decision.

## 11. Required Hard-Constraint Block Inside Image Prompts

Every S2/S5 image-generation prompt must include a compact hard-constraint block equivalent to:

- Use only paper/material-supported modules, relations, directions, and transferred quantities.
- Do not draw unsupported arrows or decorative connectors.
- Between two modules, use one bundled connector unless distinct source-supported quantities require distinct labeled lines.
- Put inter-module variables on connectors, ports, forks, merges, or tags; do not place transferred variables as standalone peer blocks inside modules.
- Keep the figure modular, not fragmented: primary modules are containers; substeps stay compact inside them.
- Use simple reviewer-recognizable motifs for internal substeps; avoid dense mini-workflows, complex tables, and exotic metaphors.
- Do not duplicate a workflow across both a main block and an inset; if an inset is used, it must add non-redundant source-grounded detail and the parent block must be simplified.
- Draw exactly one canonical process by default; repeated entity families stay as compact markers unless source evidence justifies distinct branches.
- Keep background/context small; prioritize the method framework.

## 12. S3 Guidance Preference Reminder

When S2 first-round candidates have been generated and the next legal prompt is S3-DIRECTION-SELECT, the S3 guidance must remind the user that they may name one or several preferred first-round candidate IDs as reference signals for later selection. The reminder must clarify that user-preferred candidates are preference signals, not automatic winners; S3 still performs evidence-based review, issue-ledger aggregation, and source-faithful direction selection.

If the user provides no preferred candidates, S3 proceeds autonomously using source fidelity, visual clarity, contract compliance, and exploration value.
