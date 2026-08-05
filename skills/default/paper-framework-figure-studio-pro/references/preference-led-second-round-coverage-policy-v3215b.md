# Preference-Led Second-Round Coverage Policy v3.2.15b

This policy is paper-agnostic. It applies when S3 receives or records explicit user preference signals for one or more first-round S2 candidate IDs.

## Core rule

When S3 records user-preferred first-round candidate IDs, S4 must preserve those preferences as coverage obligations for the second-round/formal candidate set.

For every S3-recorded preferred first-round candidate ID and every S4-declared active second-round style/treatment slot, S4 must include at least one S5 candidate whose role is a local-essence transfer led by that preferred first-round candidate. The declared active slot set must be feasible under the eight-scheme maximum; if not, S4 must redo the slot plan before S5.

This is a coverage requirement, not an unconditional final selection rule. S3/S4 must still apply paper evidence, source-grounded connector rules, modular hierarchy checks, and issue-ledger constraints.

## Required records

S3 must record preference signals in a paper-neutral structure such as:

```json
{
  "user_preferred_first_round_candidate_ids": ["<candidate_id>"],
  "preference_signal_source": "explicit_user_prompt",
  "preference_weighting_policy": "weighted_signal_not_unconditional_selection"
}
```

S4 must record the coverage obligations and produced rows in a structure such as:

```json
{
  "preference_coverage_policy": "v3.2.15b",
  "preferred_source_ids": ["<candidate_id>"],
  "style_slots": [{"style_id": "<style>", "style_label": "<label>"}],
  "required_pair_count": 0,
  "coverage_status": "PASS|FAIL"
}
```

Each S5 candidate row that satisfies this rule must include fields equivalent to:

```json
{
  "source_first_round_candidate_id": "<candidate_id>",
  "style_id": "<style>",
  "preference_coverage_role": "preferred_first_round_local_essence_lead"
}
```

## Candidate count and infeasible coverage

S4 must derive the required candidate count dynamically from:

```text
required_count = number_of_preferred_source_ids × number_of_declared_style_slots
```

The workflow must not hard-code a project-specific candidate count, fixed page count, fixed preferred IDs, or fixed number of styles. The reusable skill does, however, impose a generic second-round maximum of **eight S5 schemes**. S4 may expand beyond the default six only to F07/F08 (or equivalent safe IDs) and must never create a ninth second-round scheme. If `number_of_preferred_source_ids × number_of_declared_style_slots` exceeds eight, S4 must repair/replan or redo the active style-slot/preference allocation before S5 handoff. It must not silently drop preferred-source/style pairs, and it must not close S4 until the active pair set is both covered and feasible within eight.

## Prompt-package implications

For each preferred-source local-essence S5 candidate, the prompt package must state that the preferred first-round candidate is a visual preference signal only. It must not import unsupported arrows, unsupported modules, paper-specific claims absent from the source, or first-round mistakes. The prompt must say to preserve the useful local visual essence while repairing issues identified by S3.

## Negative rule

Do not satisfy this policy by duplicating the same prompt image under multiple candidate IDs. Each required row must have a distinct second-round prompt package and must explicitly bind its preferred source and style slot.
