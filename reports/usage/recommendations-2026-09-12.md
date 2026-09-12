# Skill 调整建议 2026-09-12

- 已安装技能总数: 315（Codex/Qoder/agents/lingma 四运行时）
- 分级: 待卸载 3 | 供参考 176 | 受保护 132 | 入库候选 4
- 依据: 使用遥测 2026-09-12T09:54:56；近 30 天有调用的技能一律保护，绝不进入卸载建议

## 待确认卸载（remove）

| Skill | 运行时 | 理由 |
|---|---|---|
| `grill-with-docs` | codex | 未收录且已 103 天未使用（历史 1 次） |
| `mcp-server-patterns` | codex | 未收录且已 100 天未使用（历史 1 次） |
| `recursive-decision-ledger` | codex | 未收录且已 103 天未使用（历史 1 次） |

确认执行: `python3 scripts/uninstall_skills.py --confirm`（归档式卸载，可恢复）；预览: `python3 scripts/uninstall_skills.py`

## 入库候选（discover，高频但未收录）

| Skill | 运行时 | 调用 | 理由 |
|---|---|---:|---|
| `video-rough-cut` | codex | 114 | 未收录但高频使用（历史 114 次 / 近30天 0 次），建议纳入周度发现流程 |
| `baoyu-imagine` | codex | 60 | 未收录但高频使用（历史 60 次 / 近30天 0 次），建议纳入周度发现流程 |
| `animated-financial-display` | codex | 34 | 未收录但高频使用（历史 34 次 / 近30天 0 次），建议纳入周度发现流程 |
| `vox-director` | codex | 26 | 未收录但高频使用（历史 26 次 / 近30天 0 次），建议纳入周度发现流程 |

## 供参考（consider，零调用或久未使用）

| Skill | 运行时 | 调用 | 距上次使用 | 说明 |
|---|---|---:|---|---|
| `jiebang` | codex | 72 | 51.1 | 历史 72 次，已 51.1 天未使用 |
| `baoyu-infographic` | codex | 47 | 31.1 | 历史 47 次，已 31.1 天未使用 |
| `baoyu-infographic` | qoder | 47 | 31.1 | 历史 47 次，已 31.1 天未使用 |
| `tushare-openclaw-skill` | codex | 32 | 31.1 | 历史 32 次，已 31.1 天未使用 |
| `improve-animations` | codex | 26 | 30.2 | 历史 26 次，已 30.2 天未使用 |
| `baoyu-xhs-images` | codex | 24 | 51.1 | 历史 24 次，已 51.1 天未使用 |
| `baoyu-xhs-images` | qoder | 24 | 51.1 | 历史 24 次，已 51.1 天未使用 |
| `stock-analysis` | codex | 24 | 43.8 | 历史 24 次，已 43.8 天未使用 |
| `nuwa-skill` | codex | 18 | 31.1 | 历史 18 次，已 31.1 天未使用 |
| `dual-axis-skill-reviewer` | codex | 13 | 31.1 | 历史 13 次，已 31.1 天未使用 |
| `pick-ui-library` | codex | 12 | 31.1 | 历史 12 次，已 31.1 天未使用 |
| `trader-memory-core` | codex | 12 | 41.0 | 历史 12 次，已 41.0 天未使用 |
| `video-frames` | codex | 12 | 31.1 | 历史 12 次，已 31.1 天未使用 |
| `pybroker-backtest-skill` | codex | 9 | 51.1 | 历史 9 次，已 51.1 天未使用 |
| `stock-monitor-skill` | codex | 9 | 88.1 | 历史 9 次，已 88.1 天未使用 |
| `value-dividend-screener` | codex | 9 | 49.5 | 历史 9 次，已 49.5 天未使用 |
| `video-wrapper` | codex | 9 | 31.1 | 历史 9 次，已 31.1 天未使用 |
| `openclaw-stock-kb` | codex | 8 | 87.8 | 历史 8 次，已 87.8 天未使用 |
| `wechat-public-cli` | codex | 8 | 51.1 | 历史 8 次，已 51.1 天未使用 |
| `anthropic-fs-financial-analysis-dcf-model` | codex | 7 | 39.0 | 历史 7 次，已 39.0 天未使用 |
| `emil-design-eng` | codex | 7 | 31.1 | 历史 7 次，已 31.1 天未使用 |
| `yfinance-data` | codex | 7 | 51.1 | 历史 7 次，已 51.1 天未使用 |
| `economic-calendar-fetcher` | codex | 6 | 39.4 | 历史 6 次，已 39.4 天未使用 |
| `iterative-retrieval` | codex | 6 | 34.0 | 历史 6 次，已 34.0 天未使用 |
| `llmquant-data` | codex | 6 | 53.9 | 历史 6 次，已 53.9 天未使用 |
| `alphaear-stock` | codex | 5 | 51.1 | 历史 5 次，已 51.1 天未使用 |
| `claude-shorts` | codex | 5 | 31.1 | 历史 5 次，已 31.1 天未使用 |
| `llmquant-equities` | codex | 5 | 89.4 | 历史 5 次，已 89.4 天未使用 |
| `llmquant-options` | codex | 5 | 37.3 | 历史 5 次，已 37.3 天未使用 |
| `llmquant-rates-fx` | codex | 5 | 87.8 | 历史 5 次，已 87.8 天未使用 |
| `pptx` | qoder | 5 | 43.0 | 历史 5 次，已 43.0 天未使用 |
| `video-use` | codex | 5 | 31.1 | 历史 5 次，已 31.1 天未使用 |
| `context-budget` | codex | 4 | 66.5 | 历史 4 次，已 66.5 天未使用 |
| `council` | codex | 4 | 51.1 | 历史 4 次，已 51.1 天未使用 |
| `install-skill-dependency` | qoder | 4 | 31.1 | 历史 4 次，已 31.1 天未使用 |
| `llmquant-investor-lenses` | codex | 4 | 49.5 | 历史 4 次，已 49.5 天未使用 |
| `llmquant-strategies` | codex | 4 | 89.1 | 历史 4 次，已 89.1 天未使用 |
| `position-sizer` | codex | 4 | 54.5 | 历史 4 次，已 54.5 天未使用 |
| `technical-analyst` | codex | 4 | 85.9 | 历史 4 次，已 85.9 天未使用 |
| `algorithmic-art` | codex | 3 | 31.1 | 历史 3 次，已 31.1 天未使用 |
| ...另有 136 项见 JSON | | | | |

## 受保护（keep，近期活跃）

`frontend-design`, `frontend-design`, `lemon`, `e2e-testing`, `iosdev-cn`, `a-stock-data`, `a-stock-data`, `webapp-testing`, `webapp-testing`, `production-audit`, `tdd-workflow`, `improve-codebase-architecture`, `backend-patterns`, `search-first`, `api-design`, `frontend-patterns`, `skill-creator`, `playwright`, `security-review`, `ai-regression-testing`, `ima-skill`, `codebase-onboarding`, `dasheng-vox-skills`, `remotion-best-practices`, `remotion-best-practices`, `media-downloader`, `media-downloader`, `global-stock-data`, `global-stock-data`, `baoyu-markdown-to-html`, `baoyu-markdown-to-html`, `finance-data-router`, `finance-data-router`, `design-taste-frontend`, `apple-design`, `apple-design`, `baoyu-article-illustrator`, `baoyu-article-illustrator`, `coding-standards`, `remotion-video-skill`, `skill-scout`, `baoyu-post-to-wechat`, `baoyu-post-to-wechat`, `agent-introspection-debugging`, `backtest-expert`, `wechat-draft-writer`, `wechat-draft-writer`, `error-handling`, `documentation-lookup`, `wechat-style-profiler`, `wechat-style-profiler`, `baoyu-format-markdown`, `baoyu-format-markdown`, `md2wechat`, `md2wechat`, `skill-stocktake`, `minimalist-ui`, `remotion-video-toolkit`, `academic-research-suite`, `codex-responses-tooling`
...另有 72 个
