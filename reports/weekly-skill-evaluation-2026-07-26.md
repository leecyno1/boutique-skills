# Weekly Skills Evaluation — 2026-07-26

## Protected pre-existing changes

The following files were already modified before this run and were not edited, staged, or committed by the weekly maintenance task:

- `reports/finance-skill-eval/tushare-eval/standard-finance-skills-recommendation.json`
- `reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.html`
- `reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.json`
- `reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.md`

## Pre-update baseline

- Catalog skills: 344.
- Star distribution: 5★ 69, 4★ 116, 3★ 151, 2★ 2, 1★ 6.
- Native origins verified/referenced: 338; preset exclusions: 6; missing native origins: 0.
- Standard bundle: 34 skills plus 2 packs; finance investment suite: 159 skills.
- The repository scoring model was used as the traceable base. The weekly review additionally checked uniqueness/overlap, runnable instructions or scripts, documentation completeness, upstream activity, license metadata, audit risk, OpenClaw/Codex `SKILL.md` compatibility, and dependency access mode.

## Post-sync quality view

| Dimension | Result |
|---|---|
| Uniqueness / overlap | 8 catalog conflict groups have multiple alternatives; the standard bundle still resolves to one item per capability/conflict group with 0 structural issues. |
| Executability | 344/344 catalog entries have executable instructions or a `SKILL.md`; many include scripts/tests, but external credentials remain optional requirements. |
| Completeness | 344/344 have `SKILL.md` and a non-empty description. |
| Maintenance activity | 281 GitHub-backed skills have upstream activity within 90 days of the review date. |
| Source / license | 297 catalog entries have a GitHub SPDX license detected; missing/NOASSERTION metadata remains an observation item, not an automatic quality pass. |
| Safety | Audit reports 11 pattern hits for manual review; no external upstream scripts were executed. |
| Codex / OpenClaw compatibility | 344/344 retain the repository's `SKILL.md` layout; synced Superpowers content includes current Codex references. |
| Dependency availability | 142 direct, 99 API-key, 71 MCP, 22 API-key+MCP, 10 browser-required. Audit records 76 missing optional environment variables. |
| Rating distribution | 5★ 68, 4★ 119, 3★ 149, 2★ 2, 1★ 6. Movement reflects updated descriptions/dependency detection, not GitHub popularity. |

## Candidate comparison

| Candidate | Finding | Decision |
|---|---|---|
| `openclaw/agent-skills` | Active, MIT, 7 skills; transcript, review, handoff and session capabilities substantially overlap existing core-agent and verification coverage. | Observe; do not add without a capability-level advantage test. |
| `agentskillexchange/skills` | MIT catalog with 2,806 `SKILL.md` files; breadth is high but provenance and per-skill quality require individual review. | Reject bulk import. |
| `FTShare-Lab/FTShare-skills` | MIT, 148 finance skills and 190 scripts; strong China-market breadth but overlaps A-stock-data, Tushare, AkShare and the existing finance suite. | Observe; benchmark data reliability before considering a narrow replacement. |
| `lungray/investment-workflow-skill` | MIT, 8 skills; end-to-end A/H workflow, but new and overlaps current data/research/screening/portfolio/report chain. | Observe. |
| `SentiSenseApp/skills` | MIT, 7 skills covering sentiment, 13F, political trades and unusual options; limited maintenance history and overlapping data dependencies. | Observe. |
| `JerryGou96/Finance-Skill` | MIT, 4 prompt-oriented skills with no scripts; recent and insufficient evidence of superiority over current macro/portfolio recap skills. | Do not add. |

GitHub stars were recorded only as discovery context and were not used as a substitute for quality, safety, licensing, or overlap review.

## Upstream synchronization

- GitHub-backed sources checked: 323.
- Updated full skill directories: 169.
- Already current: 110.
- Repository-level metadata only: 33.
- Broken or moved source paths: 11; these remain on the next-run repair list.
- High-value changes include expanded `a-stock-data` and `global-stock-data` endpoints, current Anthropic Financial Services instructions, substantial Claude Trading test/implementation improvements, current Baoyu assets/scripts, and Codex-aware Superpowers documentation.
- The sync process added or replaced upstream files but did not delete local extra files, preserving repository-only enhancements outside matching upstream paths.

## Bundle review

- General standard bundle membership: retained at 34 skills plus 2 packs; no additions, replacements, or removals.
- `a-stock-data` remains the A-share standard and now documents ten data layers and 44 endpoints.
- `global-stock-data` remains the global-data standard and now documents CBOE options, FINRA short volume, SEC event streams, Treasury yields, CFTC COT and earnings calendars.
- Finance investment standard suite: retained at 159 skills with no membership changes. The current chain already covers data, research, screening, trade planning, risk, monitoring, backtesting and reporting; no candidate demonstrated a clearly superior non-overlapping replacement.

## Validation

- Catalog generation: passed.
- Skill audit: WARN only; missing skills 0, missing native origins 0, duplicate capabilities 0, standard bundle issues 0.
- Repository unit tests: 7/7 passed.
- Full-tree `pytest -q`: collection blocked by `alphaear-news/tests/test_news.py`, which imports `scripts.news_tools` from a skill-local path and calls `sys.exit(1)` when collected from the repository root; no test assertions ran in that invocation.
- Python compile check: passed.
- Audit observations: 76 optional environment variables absent; 11 risk-pattern hits require manual context review.

## Weekly retrospective

- Added: none.
- Replaced: none.
- Synced: 169 existing skills.
- Retained: all standard and finance suite members.
- Removed: none; no skill met the evidence threshold for removal.
- Watchlist: FTShare market-data reliability and licensing at sub-skill level; OpenClaw agent handoff/session tools; SentiSense political/unusual-options coverage; repair 11 moved upstream paths.
