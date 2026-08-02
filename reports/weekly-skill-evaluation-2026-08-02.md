# Weekly Skills Evaluation — 2026-08-02

## Protected pre-existing changes

These four files were modified before this run and were not edited, staged, or committed by the weekly maintenance task:

- `reports/finance-skill-eval/tushare-eval/standard-finance-skills-recommendation.json`
- `reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.html`
- `reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.json`
- `reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.md`

## Pre-update baseline

- Catalog: 353 skills; 347 audited/resolved entries; missing skills 0.
- Rating baseline: 5★ 77, 4★ 119, 3★ 151, 2★ 0, 1★ 6.
- Native origins: 347 verified or referenced, 6 preset exclusions, 0 missing native origins.
- Quality dimensions: 353/353 catalog entries retain a skill manual or executable instructions; 11 conflict groups have alternatives; 74 optional environment variables are absent; 11 audit risk-pattern hits require manual review.
- Dependency baseline: direct 151, API-key 97, MCP 71, API-key+MCP 22, browser 12.
- Standard bundle: 34 skills plus 2 packs. Finance investment standard suite: 159 skills.

The repository scoring model was used as the traceable base. The review also considered uniqueness, executable content, documentation completeness, upstream activity, license/source traceability, safety, Codex/OpenClaw layout compatibility, dependency access, and overlap. Stars were discovery context only.

## GitHub and finance candidate review

| Candidate | Evidence | Decision |
|---|---|---|
| `VoltAgent/awesome-openclaw-skills` | MIT, 51,663 stars, head `69f6512`; 0 `SKILL.md` files and an index of 5,400+ registry entries. | Do not import bulk; keep as discovery index. |
| `VoltAgent/awesome-agent-skills` | MIT, 29,395 stars, head `6c82fb7`; README-only curated list, 0 `SKILL.md` files. | Do not import bulk. |
| `alirezarezvani/claude-skills` | MIT, 23,621 stars, head `aa8d778`; 798 `SKILL.md` files across broad engineering/marketing/finance domains. | Reject bulk replacement: substantial overlap and no capability-level superiority evidence. |
| `Imbad0202/academic-research-skills` | 40,452 stars, head `c804e94`; 4 skills, but repository license metadata is `NOASSERTION`. | Observe; license must be clarified before inclusion. |
| `HKUDS/Vibe-Trading` | MIT, 29,163 stars, head `bec189f`; 89 skills embedded in a full trading application with factor/data/runtime coupling. | Observe; overlaps the existing finance chain and is not a drop-in skill directory. |
| `FTShare-Lab/FTShare-skills` | MIT, 18 stars, head `c43a3d6`; 148 finance skills with strong China-market coverage. | Observe; overlaps A-stock-data/Tushare/AkShare and needs per-skill data-reliability benchmarking. |
| `avenoxai/avenoxskills` | MIT, 16 stars, head `66c519d`; 9 skills, recently active, mostly graphics/video/fleet orchestration. | Do not add; overlaps existing media and agent-orchestration coverage. |
| `RobinGru/AgentSkillForge` | Apache-2.0, head `23bd86a`; 14 coding/review/security skills. | Do not add; overlaps existing coding-devtools and verification skills without a clear quality advantage. |

No candidate met the repository threshold for a new capability, replacement, or standard-bundle entry.

## Upstream synchronization

- Checked 332 GitHub-backed sources.
- Applied 17 complete skill-directory updates; after application: 290 current, 31 repository-level metadata-only, 11 source paths missing, 0 pending updates.
- Updated source groups and latest heads: `openclaw/agent-skills` `4b79fc9` (MIT), `oso95/scroll-world` `71cc36d` (MIT), `leecyno1/dasheng-media-workflow-skills` `06c1220` (MIT), `simonlin1212/global-stock-data` `c0b3ed8` (Apache-2.0), `jackbauerxu/workbuddy-xhs-skills` `8070632` (license metadata absent), `MiniMax-AI/skills` `60aaae5` (MIT), `pbakaus/impeccable` `c5e1ddd` (Apache-2.0), `tradermonty/claude-trading-skills` `500ca4c` (MIT), and `Vincentwei1021/video-shotcraft` `d491544` (Apache-2.0).
- Preserved local enhancements and added a local layout compatibility fix for `trader-memory-core`; no upstream scripts were executed.
- Repair watchlist remains 11 moved/missing source paths: `brainstorming`, `task`, `data-analyst`, `dasheng-publish-operations-bridge`, `dasheng-video-director`, `dasheng-video-style-trainer`, `social-content`, `minimax-web-search`, `news-radar`, `finance-skill-creator`, and `minimax-image-understanding`.

## Bundle review and retrospective

- Added: none.
- Replaced: none.
- Synced: 17 existing skills.
- Retained: all 34 general standard-bundle skills plus 2 packs; finance investment suite remains 159 skills covering data, research, screening, trade planning, risk, backtesting, monitoring, and reporting.
- Removed: none; no skill met the low-quality, unsafe, duplicate, or inactive-removal threshold.
- Post-sync dependency view: direct 150, API-key 98, MCP 71, API-key+MCP 22, browser 12; the one-count shift reflects updated upstream instructions, not popularity.
- Next watchlist: FTShare data reliability/licensing at sub-skill level, Vibe-Trading's standalone skill extraction, academic-research-skills licensing, the 11 moved source paths, and newly active AgentSkillForge/Avenox skills.

## Validation

- Catalog/enriched catalog/README/generated indexes/standard bundle: passed.
- Audit: passed with WARN only — missing skills 0, missing native origins 0, duplicate capabilities 0, standard bundle issues 0; 74 optional environment variables absent; 11 risk-pattern hits for manual review.
- Repository tests: `pytest -q tests` passed 7/7.
- Synced skill tests: `pair-trade-screener` 31/31; `trader-memory-core` 373/373 after adapting upstream launcher paths to this repository's `skills/default` layout.
- Python compile check: passed.
- Standard-bundle dry-run: passed; 97 installed entries (34 base plus pack expansion).
- Full-tree `pytest -q`: collection remains blocked by the pre-existing `alphaear-news/tests/test_news.py` import/SystemExit behavior (`scripts.news_tools` unavailable from repository-root collection); no assertions ran in that invocation.
- `git diff --check`: passed.

## Release

This run contains substantive upstream synchronization, catalog regeneration, compatibility repair, and the traceable weekly report. Only files produced or changed by this run will be staged; the four protected Tushare files remain unstaged and uncommitted.
