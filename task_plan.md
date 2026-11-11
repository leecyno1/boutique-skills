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

## Catch-up Curation (2026-09-30)

| Phase | Status | Output |
|---|---|---|
| 42. Recover session context and diagnose gap | complete | Quest found disabled (pauseReason=manual); 09-19 and 09-26 skipped; remotes in sync at b53674e |
| 43. Fix curl token exposure residual | complete | weekly_curation.py sends headers via `curl --config -` stdin; tests/test_curl_token_hygiene.py added to weekly_cycle.sh step 8 |
| 44. Run discovery and prune | complete | 41 candidates, 5 repos / 21 skills imported, 415 upstreams checked, 0 removals |
| 45. Rebuild catalogs, telemetry, audit, tests | complete | 458 skills, standard bundle 30, finance suite 34, audit gates all zero, 3 test files pass |
| 46. Generate recommendations | complete | 573 installed: remove 7 / consider 465 / keep 62 / discover 39; pending-cleanup awaiting user confirmation |
| 47. Publish and verify dual remotes | pending | publish_weekly.sh + SHA equality across HEAD/origin/gitee |
| 48. Record archive-durability finding | complete | ~/.qoder/skills-archive wiped by 2026-09-16 mass restore; 31 archived skills revived, receipts unrollbackable |

## Weekly Governance Repair (2026-10-31)

| Phase | Status | Output |
|---|---|---|
| 49. Diagnose month-long gap | complete | Quest was enabled=false since 2026-09-30 and its scope was chatOnly (no repo cwd); no commits in October |
| 50. Rebuild the Quest with a real execution scope | complete | New task 436c5b6e-10c6-487b-b73a-1504e4cc89c0, directory scope, Sat 09:00 Asia/Shanghai, Full Access; old chatOnly task deleted |
| 51. Add upstream sync to the weekly cycle | complete | weekly_cycle.sh grew to 11 steps; step 3 runs check_upstream_updates.py --apply (report comes from the same run) |
| 52. Add publish gates for unattended updates | complete | check_skill_syntax.py (1379 py + 355 js, 0 errors) and check_new_risks.py + catalog/risky-baseline.json |
| 53. Apply first automatic upstream sync | complete | 436 sources, 118 skills updated, 468 modified + 227 added files; audit and tests green |
| 54. Review the one new risk hit | complete | huashu-design verify-video.sh evals ffprobe's avg_frame_rate; accepted with reason, not patched locally |
| 55. Rename the local directory | complete | boutique-openclaw-skills -> boutique-skills; stale same-name checkout archived as boutique-skills.stale-2026-08-16 |
| 56. Publish and verify dual remotes | complete | 41fa7a1 on HEAD, origin and gitee |

## Upstream Path Governance (2026-10-31)

| Phase | Status | Output |
|---|---|---|
| 57. Relocate origins whose upstream path moved | complete | 30 skills remapped (15 AlphaGBM, 12 taste-skill branch pins, 3 anthropics); overrides + SOURCE.txt updated |
| 58. Prune skills deleted upstream | complete | 22 orphans removed (15 AlphaGBM, 3 anthropics, 2 dasheng stage, omni-browser, funda-data); catalog 458 -> 436 |
| 59. Reorder weekly cycle and refresh docs | complete | sync before prune, prune --upstream-report, relocation test wired in; docs, handoff and Quest prompt updated |
| 60. Publish and verify dual remotes | complete | 462c20e on HEAD, origin and gitee; audit/syntax/risk green before publish |

## Maintenance Pass (2026-10-31)

| Phase | Status | Output |
|---|---|---|
| 61. Extract dependency manifests from the stale desktop clone | complete | wechat-multi-publisher package.json/lock merged; node_modules/ ignored |
| 62. Archive the stale desktop clone | complete | /Volumes/PSSD/Projects/boutique-skills.stale-desktop-2026-10-31 (521MB, no tracked changes left behind) |
| 63. Install agent-reach into Qoder | complete | ~/.qoder/skills/agent-reach -> repo skills/default/agent-reach; CLI verified |
| 64. Verify single-branch state | complete | only main on local, origin and gitee |

## Local Skills Cleanup (2026-11-02)

| Phase | Status | Output |
|---|---|---|
| 65. Refresh telemetry and rebuild cleanup candidates | complete | 576 installed; 29 engine candidates + 9 manual long-stale/repo-deleted = 38 |
| 66. Archive unused skills and junk | complete | Qoder 312→292, Codex 263→241; 3 broken links, 2 empty dirs, 1 old backup cleaned |
| 67. Record cleanup and publish | complete | findings.md, QODER_HANDOFF.md and reports/usage refreshed; archived copies remain restorable |
| 68. Obsolescence analysis under modern models/harnesses | complete | 353 unique installed skills scored on cli/endpoint/key/code/calls; 3 tiers written to reports/usage/obsolescence-analysis-2026-11-02.md |
| 69. Archive obsolete local copies | complete | 193 skills / 300 copies archived; Qoder 292→132, Codex 241→100; --include-active added to uninstall_skills.py |
| 70. Retire obsolete skills from the repo with re-import guard | complete | 132 removed (436→304); catalog/retired-skills.json + discover/import guard + tests/test_retired_guard.py; syntax gate re-execs to python>=3.12 |

## Design School Consolidation (2026-11-11)

| Phase | Status | Output |
|---|---|---|
| 71. Assess the elayadesign skill from the Xiaohongshu post | complete | ai-design-skills 15242★ MIT; score 70 (review) and skill_subdirs=2<3 so auto-import unreachable; rules conflict with taste-skill; figma-designer needs Figma MCP (0 tools locally) → do not import |
| 72. Keep only the taste school on this machine | complete | landing-page-design ×2 archived via --include-active; local redesign-existing-projects swapped from elaya (6558d92fdeb2) to repo taste (0713bbfa0337), elaya copy backed up to skills-archive/redesign-existing-projects-elaya-20261111/ |
| 73. Register the exclusion and fix the over-broad block | complete | design-school group (2 ids) + 2 elaya repos blocked + design_school_decision record; new test caught anthropics/skills blocking live frontend-dev → moved to shared_repos_not_blocked (134 ids / 7 blocked / 10 shared) |
| 74. Publish leftover sync output, then the decision | complete | 713e65d commits 1572 files the canceled 11-07 run never published (38MB taste v2 assets, memu, baoyu); bb2b9de carries the decision + doc count fixes; gates green (audit 0/0/0/0, syntax 1266py+502js 0 errors, risk 15=15 new 0, 5 test files OK); HEAD=origin=gitee |
| 75. Decide the remaining non-taste design schools | complete | User rule: keep a design skill only if it beats taste or complements it, otherwise drop the duplicate. RETIRE animation (bytesagain, 677-line shell wrapper around CSS keyframes), impeccable (pbakaus, competing 24-command school; taste 96>92 and already ships lint.mjs + inspect.mjs), frontend-design (origin located: anthropics/skills@00756142, 2025-12-04, SKILL.md 94.67% identical), web-animation-design (canonical origin unlocatable, only aggregators/mirrors; duplicates review-animations 98). KEEP review-animations 98, pick-ui-library 92, scroll-world 93, generative-ui 92 (inline chat widgets), huashu-design 81 (prototypes/decks/infographics, explicitly not production web apps), gsap ×8 (library API knowledge), taste family 13 |
| 76. Make taste the standard default frontend library | complete | CAPABILITY_RULES frontend candidates = [design-taste-frontend, frontend-dev, generative-ui]; bundle frontend slot moved generative-ui(92) → design-taste-frontend(96, direct, keyless); bundle still 21 slots, finance suite still 28 |
| 77. Execute the dedupe and register it | complete | remove_skill(animation, impeccable) + git rm frontend-design/web-animation-design (never registered); 4 local copies archived with --include-active --confirm after dry-run refused all 4 as active; retired registry 138 ids / 9 blocked repos (+bytesagain/ai-skills, +pbakaus/impeccable); design_school_decision gained standard_default/dedupe_rule/kept_complementary/retired_duplicates and its pending list is empty; wrapper-origins dropped animation |
| 78. Fix two catalog-generator bugs surfaced by promoting taste | complete | parse_frontmatter now accepts block-scalar chomping headers (`>-`, `|-`, …) — 4 descriptions had degraded to the literal ">-"; BOUNDARY_KEYWORDS={"ui"} stops "quick"/"build"/"guide" matching design-ui — 11 skills reclassified (baoyu-translate→writing-content, memu→agent-orchestration, agentmail-toolkit→communication, …), design-ui 45→34, install tiers unchanged 53/68/317 |
| 79. Regenerate, gate, publish | complete | catalog 317 skills / 454 dirs, 5★89 4★164 3★58 1★6, L1 12 / L2 118 / L3 187; audit 317/311 missing_skills 0 duplicate_capabilities 0 standard_bundle_issues 0; syntax 1266py + 394js 0 errors (-108 js all from impeccable); risk 15=15 new 0; 5 test files OK; commit 6d71277 (197 files, +760/-78176), HEAD=origin=gitee, no protected file staged |
