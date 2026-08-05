# S2/S5 Image-Only Terminal Orchestration Policy v3.2.15b

This policy defines the active image-only stage behavior.

## Canonical workflow

```text
S0-PAPER-FOUNDATION
  ↓
S1-FIGURE-STRATEGY + S2 prompt-package preparation duties
  ↓
S2-SKETCH-EXPLORE / IMAGE_GENERATE only
  ↓
S3-DIRECTION-SELECT + S3 review/aggregate duties over S2 outputs
  ↓
S4-CANDIDATE-BRIEF + S5 prompt-package preparation duties
  ↓
S5-CANDIDATE-IMAGE / IMAGE_GENERATE only
  ↓
END — human decision boundary
```

## Invalid units

The following units are not valid public-stage substages in v3.2.15b:

- S2 text-planning substage.
- S2 candidate image rerun.
- S2 candidate review.
- S2 text aggregate checkpoint substage.
- S5 text-planning substage.
- S5 text review substage.
- S5 candidate image rerun.
- S5 candidate review.
- S5 text aggregate checkpoint substage.
- Any assistant workflow after S5.
- Any finalization, final selection, final audit, caption text outside the assistant workflow, or final rerun loop.
- Any inactive dynamic image-stage pattern/future-image-stage parity rule based on the inactive text-image substage model.

## Mandatory responsibility relocation

S1 MUST perform the S2 prompt-package preparation responsibilities before closing S1:

- sketch candidate registry;
- S2 prompt packages and prompt-index;
- layout/routing/edge contracts;
- source-grounded text whitelist;
- line-carried variable registry;
- semantic graph versus visual render graph split;
- core-module internal visual motif plan;
- prompt contradiction audit;
- S2 image-generation handoff prompt.

S3 MUST perform the S3 review/aggregate responsibilities over S2 outputs before or as part of direction selection:

- inspect registered S2 sketches;
- write issue-ledger and visual signal summaries;
- record semantic, connector, hierarchy, density, and core-visibility problems;
- create an S2 exploration aggregate inside the S3 report/checkpoint;
- select the refinement direction after this review.

S4 MUST perform the S5 prompt-package preparation responsibilities before closing S4:

- formal candidate matrix;
- S2 issue-to-S5 risk transfer;
- S5 prompt packages and prompt-index;
- formal layout/routing/arrow contracts;
- formal visible text whitelist;
- line-carried variable registry;
- internal visual motif plan;
- prompt contradiction audit;
- S5 image-generation handoff prompt.


## Candidate id coherence

S2/S5 image-only stages must apply `references/candidate-artifact-id-coherence-policy-v3215.md`.
The prompt-index row-level `candidate_id` is the source of truth for:

- prompt paths;
- target image paths;
- stage manifests;
- substage `candidate_ids`;
- candidate registry keys;
- artifact ids and artifact `candidate_id` fields;
- image-generation event `candidate_outputs`;
- checkpoint image inventory.

Default families are `C01`-`C08` for S2 and `F01`-`F06` for S5. These defaults must not override a validated prompt-index.

## Image-only stage behavior

S2 and S5 are image-only public stages. They must:

- read the already-prepared prompt-index;
- generate only the requested raster candidates through the environment-locked image route;
- preserve the exact prompt-index `candidate_id` for every generated image;
- mirror active generated images into the same prompt-index row's `target_image_path`;
- record generation provenance.

S2 and S5 must not:

- write text plans;
- write audits;
- write rankings;
- write rerun guidance;
- rerun or review images;
- create aggregate checkpoint narratives;
- create final captions or final handoff prompts;
- continue into any assistant workflow after S5.

## Terminal response rule

After S5 candidate generation, the assistant workflow is complete. If asked what comes after S5, the response must be:

```text
我的任务已经完成，剩下由人类来决策。
```
