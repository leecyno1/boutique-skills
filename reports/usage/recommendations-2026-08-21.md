# Skill 调整建议 2026-08-21

- 已安装技能总数: 378（Codex/Qoder/agents/lingma 四运行时）
- 分级: 待卸载 34 | 供参考 136 | 受保护 204 | 入库候选 4
- 依据: 使用遥测 2026-08-21T07:34:37；近 30 天有调用的技能一律保护，绝不进入卸载建议

## 待确认卸载（remove）

| Skill | 运行时 | 理由 |
|---|---|---|
| `doc-coauthoring` | qoder | 未收录且已 112 天未使用（历史 32 次） |
| `wechat-title-generator` | codex | 未收录且已 113 天未使用（历史 12 次） |
| `wechat-title-generator` | qoder | 未收录且已 113 天未使用（历史 12 次） |
| `wechat-topic-outline-planner` | codex | 未收录且已 113 天未使用（历史 12 次） |
| `wechat-topic-outline-planner` | qoder | 未收录且已 113 天未使用（历史 12 次） |
| `web-artifacts-builder` | qoder | 未收录且已 139 天未使用（历史 11 次） |
| `doc` | qoder | 未收录且已 113 天未使用（历史 2 次） |
| `analytics-data-analysis` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `baoyu-diagram` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `baoyu-electron-extract` | qoder | 未收录于仓库且从未记录到调用，已安装 83 天 |
| `changelog-generator` | codex | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `claude-api` | qoder | 未收录于仓库且从未记录到调用，已安装 78 天 |
| `cloudflare-deploy` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `content-research-writer` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `create-plan` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `drafter-diagram` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `general-ppt` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `grill-me` | codex | 未收录于仓库且从未记录到调用，已安装 78 天 |
| `image-enhancer` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `internal-comms` | qoder | 未收录于仓库且从未记录到调用，已安装 78 天 |
| `lead-research-assistant` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `linear` | codex | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `market-research-reports` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `plugin-creator` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `qoderwork-ppt` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `quickbi-smartq-chat` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `setup-pre-commit` | codex | 未收录于仓库且从未记录到调用，已安装 78 天 |
| `slack-gif-creator` | qoder | 未收录于仓库且从未记录到调用，已安装 78 天 |
| `theme-factory` | qoder | 未收录于仓库且从未记录到调用，已安装 78 天 |
| `to-issues` | codex | 未收录于仓库且从未记录到调用，已安装 81 天 |
| `trade-performance-coach` | codex | 未收录于仓库且从未记录到调用，已安装 66 天 |
| `trading-skills-navigator` | codex | 未收录于仓库且从未记录到调用，已安装 66 天 |
| `vm-error-recovery` | qoder | 未收录于仓库且从未记录到调用，已安装 82 天 |
| `windows-desktop-e2e` | codex | 未收录于仓库且从未记录到调用，已安装 79 天 |

确认执行: `python3 scripts/uninstall_skills.py --confirm`（归档式卸载，可恢复）；预览: `python3 scripts/uninstall_skills.py`

## 入库候选（discover，高频但未收录）

| Skill | 运行时 | 调用 | 理由 |
|---|---|---:|---|
| `webapp-testing` | codex | 495 | 未收录但高频使用（历史 495 次 / 近30天 0 次），建议纳入周度发现流程 |
| `webapp-testing` | qoder | 495 | 未收录但高频使用（历史 495 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dispatching-parallel-agents` | qoder | 148 | 未收录但高频使用（历史 148 次 / 近30天 0 次），建议纳入周度发现流程 |
| `requesting-code-review` | qoder | 29 | 未收录但高频使用（历史 29 次 / 近30天 0 次），建议纳入周度发现流程 |

## 供参考（consider，零调用或久未使用）

| Skill | 运行时 | 调用 | 距上次使用 | 说明 |
|---|---|---:|---|---|
| `planning-with-files` | qoder | 257 | 35.0 | 历史 257 次，已 35.0 天未使用 |
| `subagent-driven-development` | qoder | 104 | 32.0 | 历史 104 次，已 32.0 天未使用 |
| `receiving-code-review` | qoder | 19 | 36.8 | 历史 19 次，已 36.8 天未使用 |
| `proactive-agent` | qoder | 18 | 138.5 | 历史 18 次，已 138.5 天未使用 |
| `stock-monitor-skill` | codex | 9 | 66.0 | 历史 9 次，已 66.0 天未使用 |
| `openclaw-stock-kb` | codex | 8 | 65.7 | 历史 8 次，已 65.7 天未使用 |
| `find-skills` | qoder | 7 | 123.0 | 历史 7 次，已 123.0 天未使用 |
| `baoyu-slide-deck` | qoder | 6 | 139.4 | 历史 6 次，已 139.4 天未使用 |
| `llmquant-data` | codex | 6 | 31.8 | 历史 6 次，已 31.8 天未使用 |
| `weather` | qoder | 6 | 158.9 | 历史 6 次，已 158.9 天未使用 |
| `llmquant-equities` | codex | 5 | 67.3 | 历史 5 次，已 67.3 天未使用 |
| `llmquant-rates-fx` | codex | 5 | 65.7 | 历史 5 次，已 65.7 天未使用 |
| `minimax-xlsx` | qoder | 5 | 138.5 | 历史 5 次，已 138.5 天未使用 |
| `context-budget` | codex | 4 | 44.4 | 历史 4 次，已 44.4 天未使用 |
| `llmquant-strategies` | codex | 4 | 67.0 | 历史 4 次，已 67.0 天未使用 |
| `position-sizer` | codex | 4 | 32.4 | 历史 4 次，已 32.4 天未使用 |
| `technical-analyst` | codex | 4 | 63.8 | 历史 4 次，已 63.8 天未使用 |
| `anthropic-fs-equity-research-initiating-coverage` | codex | 3 | 63.8 | 历史 3 次，已 63.8 天未使用 |
| `data-analyst` | qoder | 3 | 95.6 | 历史 3 次，已 95.6 天未使用 |
| `lin-lefeng-perspective` | codex | 3 | 65.7 | 历史 3 次，已 65.7 天未使用 |
| `llmquant-commodities` | codex | 3 | 65.8 | 历史 3 次，已 65.8 天未使用 |
| `llmquant-equity-derivatives` | codex | 3 | 67.3 | 历史 3 次，已 67.3 天未使用 |
| `sepa-strategy` | codex | 3 | 67.5 | 历史 3 次，已 67.5 天未使用 |
| `workspace-surface-audit` | codex | 3 | 36.7 | 历史 3 次，已 36.7 天未使用 |
| `agent-sort` | codex | 2 | 36.7 | 历史 2 次，已 36.7 天未使用 |
| `exposure-coach` | codex | 2 | 65.7 | 历史 2 次，已 65.7 天未使用 |
| `llmquant-crypto` | codex | 2 | 67.3 | 历史 2 次，已 67.3 天未使用 |
| `llmquant-etfs` | codex | 2 | 67.3 | 历史 2 次，已 67.3 天未使用 |
| `llmquant-events` | codex | 2 | 67.3 | 历史 2 次，已 67.3 天未使用 |
| `llmquant-market-intelligence` | codex | 2 | 67.3 | 历史 2 次，已 67.3 天未使用 |
| `llmquant-prediction-markets` | codex | 2 | 67.3 | 历史 2 次，已 67.3 天未使用 |
| `market-top-detector` | codex | 2 | 65.7 | 历史 2 次，已 65.7 天未使用 |
| `plankton-code-quality` | codex | 2 | 36.0 | 历史 2 次，已 36.0 天未使用 |
| `sun-lumin-perspective` | codex | 2 | 65.7 | 历史 2 次，已 65.7 天未使用 |
| `theme-detector` | codex | 2 | 39.0 | 历史 2 次，已 39.0 天未使用 |
| `us-stock-analysis` | codex | 2 | 67.5 | 历史 2 次，已 67.5 天未使用 |
| `alphaear-reporter` | codex | 1 | 67.8 | 历史 1 次，已 67.8 天未使用 |
| `alphaear-signal-tracker` | codex | 1 | 67.8 | 历史 1 次，已 67.8 天未使用 |
| `anthropic-fs-lseg-fixed-income-portfolio` | codex | 1 | 65.7 | 历史 1 次，已 65.7 天未使用 |
| `baoyu-translate` | codex | 1 | 103.0 | 历史 1 次，已 103.0 天未使用 |
| ...另有 96 项见 JSON | | | | |

## 受保护（keep，近期活跃）

`frontend-design`, `frontend-design`, `verification-before-completion`, `brainstorming`, `systematic-debugging`, `lemon`, `test-driven-development`, `e2e-testing`, `using-superpowers`, `iosdev-cn`, `iosdev-cn`, `a-stock-data`, `a-stock-data`, `executing-plans`, `backend-patterns`, `tdd-workflow`, `production-audit`, `improve-codebase-architecture`, `api-design`, `frontend-patterns`, `skill-creator`, `playwright`, `ai-regression-testing`, `search-first`, `writing-plans`, `coding-standards`, `dasheng-stage-material-refill`, `codebase-onboarding`, `ima-skill`, `dasheng-vox-skills`, `remotion-best-practices`, `remotion-best-practices`, `security-review`, `video-rough-cut`, `media-downloader`, `media-downloader`, `apple-design`, `apple-design`, `dasheng-video-omni-browser`, `global-stock-data`, `global-stock-data`, `dasheng-sop-orchestrator`, `writing-skills`, `design-taste-frontend`, `jiebang`, `jiebang`, `baoyu-article-illustrator`, `baoyu-article-illustrator`, `remotion-video-skill`, `baoyu-markdown-to-html`, `baoyu-markdown-to-html`, `finance-data-router`, `finance-data-router`, `baoyu-imagine`, `baoyu-imagine`, `dasheng-stage-intake-brief-draft`, `wechat-draft-writer`, `wechat-draft-writer`, `dasheng-stage-publish-video`, `skill-scout`
...另有 144 个
