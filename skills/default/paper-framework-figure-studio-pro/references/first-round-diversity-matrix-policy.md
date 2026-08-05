# First-Round And Formal Candidate Diversity Matrix Policy v3.2.3

## S2 Orthogonal Sketch Diversity Matrix

S1-FIGURE-STRATEGY must plan the default 8 S2 candidate cards as an orthogonal exploration set, not eight variants of the same density or layout. S2 still produces exactly 8 separate first-round raster candidates. The distribution changes only the exploration mix; it does not weaken paper coverage, core-detail, line/arrow/connector, first-glance, or audit-only requirements.

Orthogonality is valid only when it serves the paper framework. Do not vary style for novelty. A candidate's visual difference must test or improve at least one paper-framework communication problem: how the whole method is first read, how paper-primary spaces/paths are separated, how core internals become visible, how update/feedback/lineage relations are understood, how much caption burden is acceptable, how repeated families are compressed, or how a scoped mechanism plugs back into the full framework.

Every orthogonal choice must optimize at least one of three higher-level goals:

- `paper_work_showcase_value`: makes the paper's actual contribution, mechanism, system boundary, data/model flow, or innovation more recognizable and defensible;
- `reviewer_attraction_hook`: gives a busy reviewer a strong first-glance reason to keep reading, such as a clear problem-to-solution arc, a crisp mechanism reveal, a surprising but faithful comparison, or an immediately legible method loop;
- `aesthetic_quality_plan`: improves visual polish at the sketch-concept level through proportion, whitespace, hierarchy, rhythm, clean grouping, memorable landmarks, and non-cluttered composition.

Do not let aesthetic novelty override paper fidelity. A beautiful sketch that weakens the paper's method logic, hides the main contribution, or misleads arrow/lineage semantics is not a valid diversity candidate.

Before assigning C01-C08, S1 must derive a paper-serving semantic and style feature space from S0/S1 evidence, `references/paper-core-semantics-and-prompt-contract-policy-v323.md`, and the local style/vector knowledge base as design vocabulary. S1 must consult `references/source-grounded-prompt-audit-and-style-policy-v320.md` and, when useful, `references/vector-library/paper-grounded-style-extension-v320.md`. Local style resources can guide layout grammar, density, visual rhythm, icon/connector grammar, and aesthetic treatment; they cannot authorize paper facts, arrows, symbols, formulas, or claims.

The S1 style derivation must include `local_kb_style_scan`: local resources consulted, selected style lenses, rejected style lenses, style-evidence boundary, and why the chosen axes serve this paper rather than generic novelty.

Before assigning C01-C08, S1 must derive a paper-serving style feature space from S0/S1 evidence:

- `framework_reader_question`: the reviewer question this figure must answer;
- `paper_framework_backbone`: the method/system skeleton that must remain visible;
- `paper_core_semantics_lock`: paper thesis, canonical backbone, artifact lineage, control/evaluation signals, topology/boundary constraints, and forbidden visual inferences;
- `role_flow_separation_strategy`: how repeated or variant entity families are compressed, compared, or branched without paper-specific hardcoding;
- `paper_primary_paths`: co-primary data/model/control/actor/space paths that must not be demoted;
- `core_detail_pressure`: which core modules need visible internals and why;
- `lineage_or_arrow_risk`: high-risk artifact sharing, direction, feedback, or dependency relations;
- `caption_burden_limit`: what can safely move to caption/legend instead of pixels;
- `preferred_style_feature_axes`: selected axes from layout grammar, topology, reader path, density, detail carrier, visual rhetoric, icon/arrow grammar, panel rhythm, local KB style lenses, and reconstruction risk.

Every S1 sketch card must include `s2_style_feature_vector`:

- `layout_grammar`;
- `topology_or_reader_path`;
- `semantic_focus`;
- `density_target`;
- `detail_display_strategy`;
- `visual_rhetoric`;
- `caption_burden`;
- `icon_arrow_grammar`;
- `reconstruction_risk`;
- `paper_framework_service_role`;
- `local_kb_style_lens_id` or `local_kb_style_reference`;
- `paper_work_showcase_value`;
- `reviewer_attraction_hook`;
- `aesthetic_quality_plan`;
- `orthogonality_rationale`;
- `orthogonality_guard`: why this is not merely different-looking.

A candidate passes the orthogonality guard only when:

- it preserves the paper framework backbone, required core-module visibility, and source-grounded arrow semantics;
- it differs from nearby candidates on at least two meaningful style feature axes;
- the difference changes a framework-reading hypothesis, not only color, ornament, rendering texture, or surface style;
- its `paper_framework_service_role` names the paper-specific communication value being tested.
- at least one of `paper_work_showcase_value`, `reviewer_attraction_hook`, or `aesthetic_quality_plan` is concrete and paper-specific rather than generic praise.

If a proposed orthogonal slot weakens the paper framework, hides a core module, invents a visual metaphor or arrow grammar that the paper cannot support, imports unsupported module internals, or increases density without a reader-path benefit, reject the slot and choose a different paper-serving axis.

For complete-paper framework requests, all 8 required sketches must remain eligible complete-paper overview candidates whose `coverage_status` is `complete_compact` or `complete_with_caption_support`. Scoped probes are not part of the required batch; they may appear only as explicitly user-authorized `auxiliary_non_candidate_probes` governed by `references/complete-framework-candidate-eligibility-policy-v321.md`.


## First-Round Style Combination Design Protocol

The first round should make reviewers see different faithful readings of the same paper, not decorative variants. A strong S1 matrix designs orthogonal combinations by crossing paper-derived axes such as:

- whole-framework backbone versus mechanism cutaway;
- actor/space separation versus temporal/update sequence;
- sparse first-glance overview versus controlled core-detail exposure;
- direct pipeline versus loop/lifecycle only when feedback is source-supported;
- separated data/model/control/evaluation line styles when the paper distinguishes them;
- local-KB style lenses such as clean flat modular, swimlane actor-artifact flow, evidence-locked contract sheet, core module cutaway, hierarchical system-to-mechanism, compact distribution context, precision blueprint grid, and scientific editorial overview.

For each combination, S1 must prove that it improves at least one target-paper communication problem: reviewer first-glance, core contribution visibility, arrow/lineage safety, whole-paper coverage, caption burden reduction, or aesthetic clarity. If a style is metaphorical, story-like, or visually surprising, S1 must include a `story_to_paper_bridge` or `metaphor_support_check` showing that the metaphor remains close to paper entities and does not invent relations.

Default C01-C08 orthogonal sketch slots:

| ID | Exploration role | Density target | Paper-framework service role |
| --- | --- | --- | --- |
| C01 | Clean macro backbone overview | sparse | tests the fastest whole-framework scan path |
| C02 | Structured pipeline/swimlane overview | balanced | tests actor/space separation and ordered flow |
| C03 | Loop/lifecycle/feedback overview | balanced | tests update cycle, iteration, or temporal reader path when paper-supported |
| C04 | Main framework plus one controlled detail strip | medium-detail | tests whether signature core internals can be visible without losing backbone |
| C05 | Multi-space or comparison overview | balanced-to-medium | tests parallel paper-primary paths, peer spaces, or mechanism comparison only when role-flow separation proves the lanes are not cloned workflows |
| C06 | Story/metaphor or storyboard overview | sparse-to-balanced | tests a paper-close intuitive narrative bridge, only when it clarifies the actual method |
| C07 | Detail-rich stress-test overview | dense-but-readable | tests maximum useful core-detail load under first-glance gates |
| C08 | Mechanism-emphasized complete overview | balanced-to-medium | tests whether one signature mechanism can receive stronger visual hierarchy while the full framework backbone and all core paths remain visible |

The matrix should make the 8 options style-orthogonal across at least four axes:

- layout grammar: linear flow, swimlane, loop, comparison, inset/detail, narrative, mechanism-emphasized complete cutaway;
- density: at least 2 sparse, at least 3 balanced/medium, at least 1 intentionally dense-but-readable stress test;
- focus: whole-framework macro, paper-primary path separation, core-detail carrier, story bridge, mechanism-emphasized complete overview;
- reader hook: fastest reviewer scan, actor/space organization, temporal/update logic, mechanism insight, intuitive narrative.

Do not make all 8 sketches clean and minimal; that hides whether the paper needs more visible mechanism detail. Do not make all 8 sketches dense; that hides which framework direction has the clearest first-read path. C07 is the only default slot allowed to intentionally test a high-detail layout, and it must still pass reviewer-first-glance, main-flow dominance, and connector/readability gates.

If the target paper makes one slot inappropriate, replace that slot with another orthogonal role and record the substitution in S1. Do not replace it with a near-duplicate of an existing slot. The replacement must state which paper-framework communication problem it tests.

S1 should display an inline `s2_orthogonal_style_feature_matrix` before the eight sketch cards. The table must compare candidate ID, paper-framework service role, local KB style lens/reference, layout grammar, density target, repetition-compression strategy, detail strategy, connector/arrow grammar, reader/reviewer hook, aesthetic quality plan, caption burden, reconstruction risk, and orthogonality guard.

S4-CANDIDATE-BRIEF prepares the S5 formal candidate matrix. The default is 6 candidates arranged as `2 selected directions x 3 visual communication treatments`; the user may change the matrix, but the total must not exceed 8.

S5 candidates are generated raster images. They should be formal, clean, paper-grounded schematic references with precise arrows/colors, paper-relevant icons, visible core-innovation anchors, and style-aware caption plans. SVG/PPT editability is secondary.

Default treatments should vary:

- visual grammar and reading path;
- local KB style lens and why it fits the selected paper direction;
- module grouping and focal hierarchy;
- local-detail display strategy;
- callout or inset strategy;
- semantic density and label budget;
- paper reorganization hypothesis and S1-proposal carry-forward note.

Do not make the default difference mainly about surface rendering, because the S2 stage-level rendering contract now defaults every S2 image prompt to formal publication-style schematic rendering. S2 variation should test paper-serving layout, reader path, density, detail strategy, connector grammar, repetition compression, and caption burden—not merely polished versus sketch rendering. A low-fidelity surface is allowed only when the user explicitly selects that compatible override. A story/metaphor candidate is optional and must be justified by paper-serving value.

If the user explicitly asks for a metaphorical or story-like candidate, or S4 records a `Story-driven narrative` candidate as intentional, S4 may include one optional plain-language candidate. It still must preserve paper entities, module relations, symbols, and non-droppable core steps. Its default treatment should keep internal elements sparse, make the story path intuitive, and may use lightly cartoon-like schematic elements when they improve comprehension; avoid distant analogy or decoration.

S4 must display the matrix as an inline Markdown design-intent table before image generation. The table must compare candidate ID, author need, paper content anchor, local KB style lens/reference, figure-vs-caption split, semantic density budget, visual communication style, layout strategy, connector/arrow safety strategy, first-glance appeal, at-a-glance understanding, approximation feasibility, divergence/enhancement note, and main risk.

## v3.2.12 Narrative-Strategy Divergence Addendum

When S1 plans first-round S2 candidates, load `references/s2-narrative-layout-divergence-policy-v3212.md` before writing the candidate matrix. S2 diversity must be evaluated as diversity of paper-story explanation strategy, not as surface visual style.

S1 must add the following fields to every required S2 sketch card:

- `narrative_strategy_vector` as defined in the v3.2.12 policy;
- `candidate_layout_archetype` and `dominant_visual_spine`;
- `layout_nonnegotiables` that can be copied into S2 image prompts;
- `anti_similarity_directives` naming which other candidate families it must not resemble;
- `layout_projection_seed` indicating which paper-supported edges/paths are primary, secondary, context, or caption-only in this candidate.

S1 must also add a batch-level `s2_layout_divergence_matrix`. This matrix is separate from the visual/style feature matrix. It compares the actual narrative structure of candidates: protagonist, conflict/problem, resolution path, visual spine, canvas partition, primary path, secondary path, and nearest-neighbor difference. A batch fails if all candidates are simply the same full pipeline with renamed style lenses, changed colors, or slightly shifted boxes.

Default C01-C08 slots in this file remain useful, but they are now role families rather than layout recipes. A paper may instantiate them differently. A valid first round should normally include at least four distinct visual spines across eight candidates. Do not let every prompt use the same left-to-right module order with the same edge priority. Shared paper semantics are allowed; shared visible composition is not.

If the current paper requires all candidates to preserve the same canonical backbone, S1 must still vary the `layout_projection_seed`: one candidate may make the macro backbone primary, another actor context, another artifact lineage, another temporal update, another peer space balance, another core mechanism reveal, another problem-solution story, and another dense contract stress test. The common backbone can appear in each candidate, but it must not consume identical area or create an identical reading path in every candidate.

## First-Round Default Surface And User Override Reminder v3.2.15b

The default surface for all C01-C08 S2 first-round candidates is `formal_publication_schematic` / 正式出版风格. Orthogonal diversity should vary paper-serving layout, reader path, density, detail carrier, visual rhetoric, and style lens, but should not silently vary the rendering surface into polished final art.

S0 must add the non-blocking first-round surface-style reminder from `references/first-round-default-style-guidance-policy-v3215a.md` outside the copyable S1 prompt block. The reminder must list the allowed first-round surface-style options, including `acm_ieee_aaai_line_art_schematic`, and tell the user that any override or default-surface cancellation should be added manually to the S1 request before S1 prepares S2 prompt packages. S1-to-S2 handoff must repeat the full mandatory first-round surface-style reminder as non-copyable prose outside the suggested S2 prompt, must list all compatible options, and must explain that S2 follows the S1 prompt-index, so changing surface style after S1 requires rerunning S1 before S2. If no explicit override or cancellation is recorded in S1 artifacts, S2 uses the formal publication surface-style default. The selected surface style must still be combined with narrative, layout, density, semantic focus, connector hierarchy, and source-grounded constraints.
