# S4 Formal Candidate Brief Template v3.2.15b

This template is for S4-CANDIDATE-BRIEF. It prepares S5 formal candidate prompts and prompt-index entries. S5 is image-generation-only and terminal; human selection after S5 is outside the assistant workflow.

## Candidate ID Coherence

- The prompt-index row `candidate_id` is the source of truth for each S5 formal candidate.
- Default S5 candidate IDs are `F01-F06`.
- Do not rewrite formal candidate IDs as `C01-C06`, numeric IDs, or runtime-generated image names.
- For every row, keep this equality chain coherent:
  - `candidate_id`
  - `prompt_path`
  - `target_image_path`
  - candidate registry key
  - artifact `candidate_id`
  - active image path
  - checkpoint image inventory entry

Example default S5 row:

```json
{
  "candidate_id": "F01",
  "prompt_path": "outputs/S5-candidate-image/candidates/F01/prompt-v01.md",
  "target_image_path": "outputs/S5-candidate-image/candidates/F01/image-v01.png"
}
```

## S4 Six-Candidate Matrix Fields

For complete-paper / framework / method-overview tasks, prepare six generic formal candidate briefs unless the user asks for fewer. Each brief should include:

| Field | Required content |
|---|---|
| candidate_id | Exact formal candidate ID, usually F01-F06 |
| prompt_path | Prompt package path containing the same candidate ID segment |
| target_image_path | Target image path containing the same candidate ID segment |
| visual treatment | Clean formal schematic treatment, not paper-specific hardcoding |
| reader path | 3-5 anchor path for first-glance comprehension |
| figure-caption symbiosis plan | What the figure shows versus what surrounding text/caption should explain outside the image |
| issue-ledger transfer | S2 issues converted into S5 negative constraints |
| prompt-risk transfer | Forbidden topology, wrong edge directions, variable-as-block risks, unsupported modules |
| edge / port contract | Source, target, direction, label policy, and forbidden alternatives |
| visible text whitelist | Short labels and symbols allowed in the figure |
| internal motif plan | Pictorial micro-chain for core composite modules |
| density budget | Explicit compression for repeated entities, samples, rows, panels, legends, and arrows |
| generation note | S5 only generates images and ends the assistant workflow |


## Strict Prompt Contract Checklist

For every S5 prompt package, record and pass before prompt-index finalization:

- edge-support ledger for every connector, including upstream/downstream evidence anchors;
- connector multiplicity audit: one bundled connector between two block-level modules unless distinct labeled quantities are source-supported;
- edge-label-first variable placement: transferred variables on connectors, ports, forks, merges, or tags;
- modularity-not-fragmentation gate: primary modules remain coherent containers, not scattered micro-blocks;
- simple internal motif gate: submodule diagrams use common, minimal conventions that reviewers can read quickly;
- redundancy gate: no duplicate workflow in a main block and an inset; no repeated full workflow lanes without distinct source-supported meaning;
- background/context budget gate: context remains small and the method framework remains dominant;
- audit/repair cycle log, maximum three cycles.

Every image-generation prompt must include these hard constraints inside the prompt text itself.

## Prompt-Index Generation Checklist

- Write `outputs/S5-candidate-image/prompt-index.json` before S4 closes.
- Use list-shaped `candidates[]` rows plus `candidate_map` compatibility if produced by script.
- Validate that each `prompt_path` exists.
- Validate that each `target_image_path` parent directory matches the same `candidate_id`.
- Validate that stage manifest/substage plan candidate IDs come from prompt-index, not from a separate default renumbering.

## S5 Handoff Text

Suggested handoff prompts should say:

```text
请使用 paper-framework-figure-studio-pro skill，根据当前状态和 prompt-index，执行 S5-CANDIDATE-IMAGE 的 IMAGE_GENERATE。
```

Do not mention versioned ZIP filenames in suggested prompts.
