# S3 Preference-Carryover And Formal Local-Essence Candidate Policy v3.2.15b

This policy is paper-agnostic. It applies when the S3-DIRECTION-SELECT user prompt names one or more preferred first-round/S2 candidate ids as a preference signal.

## Core rule

If S3 receives explicit user-preferred first-round candidate ids, S3 must record them as a machine-readable `preference_carryover_contract` in the S3 direction record and S4 must preserve them in the formal/S5 candidate matrix, subject to the absolute maximum of eight second-round schemes.

The preference signal is not an automatic winner. S3 still selects direction by source evidence, issue-ledger findings, and figure-contract quality. However, once user preference ids are recorded, S4 must not collapse them into a vague narrative such as "inspired by prior candidates". They must become explicit dominant source bindings for second-round formal candidates.

## Required S3 recording

S3 must record, without hard-coded ids or counts:

```json
{
  "preference_carryover_contract": {
    "applies": true,
    "source_stage": "S2-SKETCH-EXPLORE",
    "preferred_source_candidate_ids": ["<ids from user prompt>"],
    "carryover_mode": "dominant_local_essence_candidates_required",
    "style_coverage_rule": "for every S5 style/treatment group, at least one formal candidate must be user-preference-led",
    "individual_preference_coverage_rule": "each preferred source id must lead at least one formal candidate for every active S5 style/treatment family; keep total S5 second-round schemes <= 8; repair/replan or redo S4 if coverage cannot fit"
  }
}
```

The field names may be embedded in a larger direction record, but the preferred ids and the carryover rules must remain machine-readable.

## Required S4/S5 matrix behavior

When the S3 carryover contract applies, S4 must generate the S5 formal candidate matrix so that:

1. Every style/treatment group scheduled for S5 has at least one candidate row marked as `user_preference_led_local_essence` or an equivalent machine-readable preference-led mode.
2. The preference-led row for each style/treatment group includes a `dominant_source_candidate_ids` or equivalent field whose values intersect the S3 `preferred_source_candidate_ids`.
3. Across the whole S5 matrix, every preferred source id appears as a dominant source at least once when the available candidate budget permits.
4. If the number of style groups and preferred ids exceeds the nominal S5 candidate count, S4 may expand the candidate matrix only up to eight total second-round schemes. It must not split or extend S5 to a ninth scheme. If coverage cannot fit within eight, S4 must repair/replan or redo the active style-slot/preference allocation before S5 handoff; it must not silently omit the user's preferred first-round choices or close S4 until coverage passes within the cap.
5. A hybrid candidate may be valid only if the preferred source remains dominant for that row; a generic hybrid with the preferred id listed only as a weak inspiration does not satisfy this policy.

## Prompt-package obligations

Every preference-led formal candidate prompt must contain a compact, paper-neutral provenance line, for example:

```text
Preference-led local essence: preserve the dominant structural strengths of source candidate <ID(s)> while repairing its recorded S2/S3 issues and following the S4 source-grounded prompt contract.
```

This line is a provenance/control instruction, not a request to copy pixels or imitate the original generated image exactly.

## Forbidden behavior

Do not:

- ignore explicit user-preferred S2 ids after S3;
- represent user preference only as a scoring bonus while producing no preference-led formal candidate;
- create only one preference-led candidate when multiple S5 styles/treatments are scheduled;
- use hard-coded candidate ids, image counts, paper names, model names, dataset names, or task-specific modules;
- copy the first-round image pixel-for-pixel, or preserve its known defects without repair;
- override source-grounded evidence constraints or checkpoint integrity gates.

## Validation

S4 close must run a generic preference-carryover guard when S3 recorded preferences. The guard must derive preferred ids, style groups, and candidate rows from S3/S4/S5 state files and prompt-index artifacts, not from fixed candidate id or image-count assumptions.
