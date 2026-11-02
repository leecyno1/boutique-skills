# Skill 调整建议 2026-11-02

- 已安装技能总数: 576（Codex/Qoder/agents/lingma 四运行时）
- 分级: 待卸载 29 | 供参考 413 | 受保护 134 | 入库候选 0
- 依据: 使用遥测 2026-11-02T12:36:24；近 30 天有调用的技能一律保护，绝不进入卸载建议

## 待确认卸载（remove）

| Skill | 运行时 | 理由 |
|---|---|---|
| `using-git-worktrees` | qoder | 未收录且已 112 天未使用（历史 3 次） |
| `finishing-a-development-branch` | qoder | 未收录且已 112 天未使用（历史 2 次） |
| `requesting-code-review` | qoder | 未收录且已 113 天未使用（历史 2 次） |
| `equity-deep-research` | qoder | 未收录且已 101 天未使用（历史 1 次） |
| `agent-sort` | codex | 未收录于仓库且从未记录到调用，已安装 110 天 |
| `algorithmic-art` | codex | 未收录于仓库且从未记录到调用，已安装 101 天 |
| `algorithmic-art` | qoder | 未收录于仓库且从未记录到调用，已安装 152 天 |
| `animated-financial-display` | codex | 未收录于仓库且从未记录到调用，已安装 101 天 |
| `anthropic-fs-wealth-management-financial-plan` | codex | 未收录于仓库且从未记录到调用，已安装 127 天 |
| `anthropic-fs-wealth-management-portfolio-rebalance` | codex | 未收录于仓库且从未记录到调用，已安装 127 天 |
| `anthropic-fs-wealth-management-tax-loss-harvesting` | codex | 未收录于仓库且从未记录到调用，已安装 127 天 |
| `baoyu-imagine` | codex | 未收录于仓库且从未记录到调用，已安装 186 天 |
| `claude-shorts` | codex | 未收录于仓库且从未记录到调用，已安装 101 天 |
| `council` | codex | 未收录于仓库且从未记录到调用，已安装 152 天 |
| `install-skill-dependency` | qoder | 未收录于仓库且从未记录到调用，已安装 155 天 |
| `iterative-retrieval` | codex | 未收录于仓库且从未记录到调用，已安装 152 天 |
| `langsmith-fetch` | codex | 未收录于仓库且从未记录到调用，已安装 127 天 |
| `lin-lefeng-perspective` | codex | 未收录于仓库且从未记录到调用，已安装 139 天 |
| `nuwa-skill` | codex | 未收录于仓库且从未记录到调用，已安装 127 天 |
| `plankton-code-quality` | codex | 未收录于仓库且从未记录到调用，已安装 152 天 |
| `statistical-analysis` | qoder | 未收录于仓库且从未记录到调用，已安装 81 天 |
| `statistical-power` | qoder | 未收录于仓库且从未记录到调用，已安装 81 天 |
| `sun-lumin-perspective` | codex | 未收录于仓库且从未记录到调用，已安装 139 天 |
| `tushare-api` | qoder | 未收录于仓库且从未记录到调用，已安装 89 天 |
| `video-wrapper` | codex | 未收录于仓库且从未记录到调用，已安装 101 天 |
| `wechat-public-cli` | codex | 未收录于仓库且从未记录到调用，已安装 127 天 |
| `wechat-title-generator` | codex | 未收录于仓库且从未记录到调用，已安装 186 天 |
| `wechat-title-generator` | qoder | 未收录于仓库且从未记录到调用，已安装 155 天 |
| `workspace-surface-audit` | codex | 未收录于仓库且从未记录到调用，已安装 110 天 |

确认执行: `python3 scripts/uninstall_skills.py --confirm`（归档式卸载，可恢复）；预览: `python3 scripts/uninstall_skills.py`

## 供参考（consider，零调用或久未使用）

| Skill | 运行时 | 调用 | 距上次使用 | 说明 |
|---|---|---:|---|---|
| `baoyu-article-illustrator` | codex | 18 | 69.6 | 历史 18 次，已 69.6 天未使用 |
| `baoyu-article-illustrator` | qoder | 18 | 69.6 | 历史 18 次，已 69.6 天未使用 |
| `baoyu-post-to-wechat` | codex | 12 | 44.1 | 历史 12 次，已 44.1 天未使用 |
| `baoyu-post-to-wechat` | qoder | 12 | 44.1 | 历史 12 次，已 44.1 天未使用 |
| `anthropic-fs-financial-analysis-dcf-model` | codex | 8 | 42.8 | 历史 8 次，已 42.8 天未使用 |
| `anthropic-fs-financial-analysis-dcf-model` | qoder | 8 | 42.8 | 历史 8 次，已 42.8 天未使用 |
| `baoyu-cover-image` | codex | 8 | 67.8 | 历史 8 次，已 67.8 天未使用 |
| `baoyu-cover-image` | qoder | 8 | 67.8 | 历史 8 次，已 67.8 天未使用 |
| `brandkit` | codex | 6 | 79.8 | 历史 6 次，已 79.8 天未使用 |
| `skill-stocktake` | codex | 6 | 53.1 | 历史 6 次，已 53.1 天未使用 |
| `brainstorming` | qoder | 4 | 54.1 | 历史 4 次，已 54.1 天未使用 |
| `freecut` | codex | 4 | 79.6 | 历史 4 次，已 79.6 天未使用 |
| `writing-plans` | qoder | 4 | 111.8 | 历史 4 次，已 111.8 天未使用 |
| `citation-verification` | qoder | 3 | 37.1 | 历史 3 次，已 37.1 天未使用 |
| `find-animation-opportunities` | codex | 3 | 80.1 | 历史 3 次，已 80.1 天未使用 |
| `find-animation-opportunities` | qoder | 3 | 80.1 | 历史 3 次，已 80.1 天未使用 |
| `guizang-social-card-skill` | codex | 3 | 68.0 | 历史 3 次，已 68.0 天未使用 |
| `llmquant-commodities` | codex | 3 | 69.8 | 历史 3 次，已 69.8 天未使用 |
| `llmquant-commodities` | qoder | 3 | 69.8 | 历史 3 次，已 69.8 天未使用 |
| `portfolio-manager` | codex | 3 | 32.8 | 历史 3 次，已 32.8 天未使用 |
| `portfolio-manager` | qoder | 3 | 32.8 | 历史 3 次，已 32.8 天未使用 |
| `seedance2-skill` | codex | 3 | 31.7 | 历史 3 次，已 31.7 天未使用 |
| `subagent-driven-development` | qoder | 3 | 113.2 | 历史 3 次，已 113.2 天未使用 |
| `academic-research-suite` | qoder | 2 | 78.1 | 历史 2 次，已 78.1 天未使用 |
| `alphaear-search` | codex | 2 | 70.2 | 历史 2 次，已 70.2 天未使用 |
| `alphaear-search` | qoder | 2 | 70.2 | 历史 2 次，已 70.2 天未使用 |
| `alphaear-sentiment` | codex | 2 | 81.2 | 历史 2 次，已 81.2 天未使用 |
| `alphaear-sentiment` | qoder | 2 | 81.2 | 历史 2 次，已 81.2 天未使用 |
| `coze-agent-collaboration` | agents | 2 | 66.6 | 历史 2 次，已 66.6 天未使用 |
| `coze-agent-collaboration` | lingma | 2 | 66.6 | 历史 2 次，已 66.6 天未使用 |
| `coze-agent-collaboration` | qoder | 2 | 66.6 | 历史 2 次，已 66.6 天未使用 |
| `dasheng-hotspot-radar` | codex | 2 | 45.8 | 历史 2 次，已 45.8 天未使用 |
| `dasheng-stage-brief-ai` | qoder | 2 | 81.0 | 历史 2 次，已 81.0 天未使用 |
| `ian-xiaohei-illustrations` | codex | 2 | 69.8 | 历史 2 次，已 69.8 天未使用 |
| `lark-wiki` | qoder | 2 | 31.1 | 历史 2 次，已 31.1 天未使用 |
| `llmquant-risk` | codex | 2 | 49.1 | 历史 2 次，已 49.1 天未使用 |
| `llmquant-risk` | qoder | 2 | 49.1 | 历史 2 次，已 49.1 天未使用 |
| `md2wechat` | codex | 2 | 73.2 | 历史 2 次，已 73.2 天未使用 |
| `md2wechat` | qoder | 2 | 73.2 | 历史 2 次，已 73.2 天未使用 |
| `pre-submission-reviewer` | qoder | 2 | 37.1 | 历史 2 次，已 37.1 天未使用 |
| ...另有 373 项见 JSON | | | | |

## 受保护（keep，近期活跃）

`tdd-workflow`, `e2e-testing`, `security-review`, `frontend-patterns`, `search-first`, `frontend-design`, `frontend-design`, `production-audit`, `api-design`, `error-handling`, `backend-patterns`, `finance-data-router`, `finance-data-router`, `a-stock-data`, `a-stock-data`, `improve-codebase-architecture`, `ai-regression-testing`, `playwright`, `iosdev-cn`, `iosdev-cn`, `webapp-testing`, `webapp-testing`, `dasheng-vox-skills`, `agent-reach`, `agent-reach`, `backtest-expert`, `backtest-expert`, `documentation-lookup`, `agent-introspection-debugging`, `emil-design-eng`, `emil-design-eng`, `codex-image-bridge`, `apple-design`, `apple-design`, `global-stock-data`, `global-stock-data`, `remotion-best-practices`, `remotion-best-practices`, `remotion-video-skill`, `skill-creator`, `skill-scout`, `baoyu-markdown-to-html`, `baoyu-markdown-to-html`, `coding-standards`, `data-quality-checker`, `data-quality-checker`, `verification-before-completion`, `pdf`, `systematic-debugging`, `codebase-onboarding`, `newma-draft`, `cut-talking-head`, `media-downloader`, `media-downloader`, `test-driven-development`, `anthropic-fs-equity-research-sector-overview`, `anthropic-fs-equity-research-sector-overview`, `verification-loop`, `anatomy`, `dasheng-style-profiler`
...另有 74 个
