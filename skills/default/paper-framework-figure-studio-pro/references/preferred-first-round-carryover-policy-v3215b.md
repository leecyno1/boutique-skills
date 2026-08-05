# Preferred First-Round Carryover Policy v3.2.15b

This policy is paper-agnostic. It applies when an S3 handoff prompt, S3 user message, direction-selection record, or S3 issue ledger explicitly names one or more first-round S2 candidate IDs as user-preferred reference signals.

The policy must not encode a specific paper topic, dataset, method name, module name, variable name, project ID, candidate count, or fixed candidate ID list. Candidate IDs and styles are always discovered from prompt-index rows, S3 records, user-provided preference fields, and the S4 candidate matrix.

## Core rule

If S3 records `user_preferred_first_round_candidate_ids`, S4 must guarantee that the second-round S5 candidate matrix contains preference-led local-essence refinements before it can close.

For every user-preferred first-round candidate ID and every active second-round style family, S4 must allocate at least one S5 candidate whose lineage marks that preferred first-round candidate as the dominant source, while keeping the complete second-round/S5 candidate set at eight schemes or fewer:

```json
{
  "lineage_role": "preference_led_local_essence_refinement",
  "dominant_source_candidate_id": "<preferred S2 candidate id>",
  "style_family": "<active S5 style family>"
}
```

A preference-led local-essence refinement is not a copy of the first-round image. It preserves the useful local visual strengths, layout grammar, rhythm, or reader effect of that preferred candidate while applying all S2/S3 issue-ledger fixes and all source-grounded prompt contracts.

## Style-family coverage

The active style families are discovered from the S4 formal candidate matrix or S5 prompt-index rows. If the user or S4 contract declares multiple second-round styles, the coverage rule applies to each declared style. If no explicit style family is declared, the stage has one default style family and the rule still applies once per preferred candidate.

If the default S5 budget is insufficient to satisfy the Cartesian coverage of preferred IDs × active style families, S4 may expand the S5 candidate count dynamically using the stage's safe candidate-id generator only up to the eight-scheme maximum. It must not split S5 or extend the matrix to a ninth scheme. If the required active coverage exceeds eight, S4 must repair/replan or redo the active style-family allocation, or ask the user to narrow preferences/styles, before S5 handoff. It must not drop a preference-led requirement merely to preserve a default count and must not close S4 until the coverage audit passes within the cap.

The generated second-round IDs must remain S5 IDs such as `F01`, `F02`, ... or another validated S5 prefix. They must not reuse first-round S2 IDs such as `C01` unless a project-specific prompt-index already defines a safe S5 ID set.

## Audit requirements

S4 must write a `preference_carryover_coverage_audit` into the formal-candidate matrix, direction contract, or prompt-index metadata. The audit must include:

- `preferred_first_round_candidate_ids` discovered from S3 / user messages;
- `active_style_families` discovered from S4/S5 rows;
- the required coverage pairs;
- the S5 candidate ID satisfying each pair;
- any unsatisfied pair and whether generation is blocked.

S4 must not give the S5 image-only prompt if any required pair is unsatisfied or if the S5 candidate count exceeds eight. It must repair/replan or redo S4 at a text checkpoint and report the missing or infeasible coverage pairs.

## S3 duties

S3 must preserve user-named first-round preferences as preference signals in machine-readable form, even if the final selected direction is a hybrid or another candidate. If S3 chooses not to make a preferred candidate dominant in the selected direction, it must record why, but S4 still needs to provide preference-led local-essence candidates unless the user explicitly withdraws that preference.

S3 must keep preferences as evidence-weighted visual lineage, not as source-paper facts. A preferred first-round candidate cannot introduce unsupported paper claims, unsupported arrows, unsupported modules, or forbidden visual motifs into S4/S5 prompts.

## Negative constraints

Do not satisfy this policy by:

- duplicating a first-round image without repair;
- adding only text discussion without a corresponding S5 candidate row;
- creating a generic hybrid row whose dominant source is not the preferred candidate;
- silently treating a user preference as obsolete because another candidate scored higher;
- hard-coding candidate IDs, image counts, style names, project names, paper topics, or expected filenames.

## Field-name compatibility addendum

S4/S5 rows may use either the older lineage field names (`lineage_role`, `dominant_source_candidate_id`, `style_family`) or the normalized v3.2.15b field names (`preference_coverage_role`, `source_first_round_candidate_id`, `style_id`). The normalized names are preferred for new prompt-index and matrix files. Validation should treat the older names as aliases only when they unambiguously encode the same preferred-source × style coverage pair.
