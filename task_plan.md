# Task Plan: Skill Origin, Index, Scoring, and README Upgrade

## Goal
Upgrade the repository from copied installer-source metadata to a maintainable enriched registry that supports native upstream URLs, horizontal tiers, vertical categories, dependency labels, scoring, monthly review, and a non-duplicated standard bundle.

## Phases

| Phase | Status | Output |
|---|---|---|
| 1. Audit current metadata shape | complete | Current catalog gaps and script inputs identified |
| 2. Define enriched catalog schema | complete | Machine-readable schema and generated enriched catalog |
| 3. Generate indexes and README sections | complete | Tier/type/dependency/standard bundle Markdown generated |
| 4. Update monthly automation docs | complete | GitHub Action and update SOP changed to monthly review |
| 5. Run verification checks | complete | JSON validity, generator output, audit command results |

## Decisions
- Treat existing installer URLs as mirror sources, not native origins.
- Preserve existing skill files; add metadata/index generation rather than editing hundreds of skill directories manually.
- Use deterministic heuristic classification as a first pass, with explicit `origin_confidence` and `needs_origin_review` flags.
- Exclude Open/Hermes preset skills from the standard install bundle via a preset exclusion list.

## Errors Encountered
| Error | Attempt | Resolution |
|---|---|---|

## Continuation Phases

| Phase | Status | Output |
|---|---|---|
| 6. Review installer and audit scripts | complete | Identify where standard bundle and origin gate fit |
| 7. Add origin audit gate | complete | Audit reports missing native origin counts |
| 8. Add standard bundle installer | complete | Install the no-duplicate standard bundle |
| 9. Refresh README usage docs | complete | Usage command documented on README home |
| 10. Run verification checks | complete | JSON/script/audit/install dry-run verified |

## Origin Refill Batch 1

| Phase | Status | Output |
|---|---|---|
| 11. Identify priority missing origins | complete | Standard bundle and L1 missing origins listed |
| 12. Verify first-party source URLs | complete | Confirmed reachable first-party URLs only |
| 13. Update origin overrides | complete | Added verified overrides for priority skills |
| 14. Regenerate indexes | complete | Enriched catalog and README refreshed |
| 15. Run verification checks | complete | JSON/audit/install checks rerun |

## Origin Refill Batch 2

| Phase | Status | Output |
|---|---|---|
| 16. List next missing candidates | complete | Standard leftovers and high-value category gaps listed |
| 17. Search and verify sources | complete | Reachable sources checked for batch 2 |
| 18. Patch origin overrides | complete | Added second batch of verified origin URLs |
| 19. Regenerate catalog outputs | complete | Enriched catalog and README refreshed |
| 20. Run final checks | complete | JSON/audit/install checks rerun |

## Origin Refill Batch 3

| Phase | Status | Output |
|---|---|---|
| 21. List finance missing origins | complete | Remaining finance-trading gaps identified |
| 22. Find matching upstream sources | complete | TraderMonty, finance-skills, AlphaEar, ClawHub candidates matched |
| 23. Patch verified finance origins | complete | Added verified finance origin URLs in bulk |
| 24. Regenerate registry outputs | complete | Enriched catalog and README refreshed |
| 25. Run verification checks | complete | JSON/audit/install checks rerun |

## Origin Refill Batch 4

| Phase | Status | Output |
|---|---|---|
| 26. List remaining missing origins | complete | Remaining 31 gaps listed |
| 27. Verify remaining source candidates | complete | Workflow, AgentMail, Paperless, MiniMax, finance leftovers checked |
| 28. Patch final origin overrides | complete | Added final verified batch |
| 29. Regenerate all outputs | complete | Enriched catalog and README refreshed |
| 30. Run completion checks | complete | JSON/audit/install checks rerun |

## Goal Completion Cleanup

| Phase | Status | Output |
|---|---|---|
| 31. Resolve final four origins | complete | animation, writing-plans, finance-data sourced; shell excluded as preset |
| 32. Patch source policy metadata | complete | Preset exclusions do not count as missing origins |
| 33. Regenerate registry outputs | complete | Enriched catalog and README refreshed |
| 34. Run full verification | complete | JSON/audit/install checks rerun |
| 35. Mark goal complete | complete | Enriched summary (2026-08-22) reports needs_origin_review=0, 418 verified origins |

## Memory Recovery (2026-09-11)

| Phase | Status | Output |
|---|---|---|
| 36. Recover lost session context | complete | Parsed 2026-09-08 transcript; restored Quest status and pending work list |
| 37. Correct stale memory files | complete | QODER_HANDOFF.md counts refreshed to 424 registered / 560 dirs; findings.md re-dated |
| 38. Document memory recovery order | complete | New QODER_HANDOFF.md section listing on-disk memory sources |
| 39. Fix remote README broken images | complete | Commit `2cdfd9f` added 3 assets, dropped hero.png, pushed origin + gitee |
| 40. Update stale GitHub repo URL references | complete | Generator, suite JSON and README row all point to leecyno1/boutique-skills; origin URL repointed |
| 41. Add memory files to publish whitelist | complete | findings.md and task_plan.md added to publish_weekly.sh whitelist |
