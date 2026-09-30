# Skill 调整建议 2026-09-30

- 已安装技能总数: 573（Codex/Qoder/agents/lingma 四运行时）
- 分级: 待卸载 7 | 供参考 465 | 受保护 62 | 入库候选 39
- 依据: 使用遥测 2026-09-30T21:27:03；近 30 天有调用的技能一律保护，绝不进入卸载建议

## 待确认卸载（remove）

| Skill | 运行时 | 理由 |
|---|---|---|
| `wechat-topic-outline-planner` | qoder | 未收录且已 154 天未使用（历史 12 次） |
| `openclaw-stock` | qoder | 未收录且已 179 天未使用（历史 6 次） |
| `openclaw-stock-analyzer` | qoder | 未收录且已 179 天未使用（历史 6 次） |
| `stock_datasource` | qoder | 未收录且已 179 天未使用（历史 6 次） |
| `lin-lefeng-perspective` | codex | 未收录且已 106 天未使用（历史 3 次） |
| `doc` | qoder | 未收录且已 154 天未使用（历史 2 次） |
| `sun-lumin-perspective` | codex | 未收录且已 106 天未使用（历史 2 次） |

确认执行: `python3 scripts/uninstall_skills.py --confirm`（归档式卸载，可恢复）；预览: `python3 scripts/uninstall_skills.py`

## 入库候选（discover，高频但未收录）

| Skill | 运行时 | 调用 | 理由 |
|---|---|---:|---|
| `lemon` | codex | 1232 | 未收录但高频使用（历史 1232 次 / 近30天 0 次），建议纳入周度发现流程 |
| `test-driven-development` | qoder | 1055 | 未收录但高频使用（历史 1055 次 / 近30天 0 次），建议纳入周度发现流程 |
| `executing-plans` | qoder | 495 | 未收录但高频使用（历史 495 次 / 近30天 0 次），建议纳入周度发现流程 |
| `tdd-workflow` | codex | 370 | 未收录但高频使用（历史 370 次 / 近30天 0 次），建议纳入周度发现流程 |
| `ai-regression-testing` | codex | 168 | 未收录但高频使用（历史 168 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dispatching-parallel-agents` | qoder | 148 | 未收录但高频使用（历史 148 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dasheng-stage-material-refill` | qoder | 146 | 未收录但高频使用（历史 146 次 / 近30天 0 次），建议纳入周度发现流程 |
| `ima-skill` | codex | 137 | 未收录但高频使用（历史 137 次 / 近30天 0 次），建议纳入周度发现流程 |
| `remotion-best-practices` | codex | 123 | 未收录但高频使用（历史 123 次 / 近30天 0 次），建议纳入周度发现流程 |
| `remotion-best-practices` | qoder | 123 | 未收录但高频使用（历史 123 次 / 近30天 0 次），建议纳入周度发现流程 |
| `video-rough-cut` | codex | 114 | 未收录但高频使用（历史 114 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dasheng-sop-orchestrator` | qoder | 81 | 未收录但高频使用（历史 81 次 / 近30天 0 次），建议纳入周度发现流程 |
| `remotion-video-skill` | codex | 73 | 未收录但高频使用（历史 73 次 / 近30天 0 次），建议纳入周度发现流程 |
| `baoyu-imagine` | codex | 60 | 未收录但高频使用（历史 60 次 / 近30天 0 次），建议纳入周度发现流程 |
| `baoyu-imagine` | qoder | 60 | 未收录但高频使用（历史 60 次 / 近30天 0 次），建议纳入周度发现流程 |
| `skill-scout` | codex | 59 | 未收录但高频使用（历史 59 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dasheng-stage-publish-video` | qoder | 52 | 未收录但高频使用（历史 52 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dasheng-stage-intake-brief-draft` | qoder | 51 | 未收录但高频使用（历史 51 次 / 近30天 0 次），建议纳入周度发现流程 |
| `wechat-draft-writer` | codex | 49 | 未收录但高频使用（历史 49 次 / 近30天 0 次），建议纳入周度发现流程 |
| `wechat-draft-writer` | qoder | 49 | 未收录但高频使用（历史 49 次 / 近30天 0 次），建议纳入周度发现流程 |
| `wechat-style-profiler` | codex | 39 | 未收录但高频使用（历史 39 次 / 近30天 0 次），建议纳入周度发现流程 |
| `wechat-style-profiler` | qoder | 39 | 未收录但高频使用（历史 39 次 / 近30天 0 次），建议纳入周度发现流程 |
| `md2wechat` | codex | 37 | 未收录但高频使用（历史 37 次 / 近30天 0 次），建议纳入周度发现流程 |
| `md2wechat` | qoder | 37 | 未收录但高频使用（历史 37 次 / 近30天 0 次），建议纳入周度发现流程 |
| `remotion-video-toolkit` | codex | 35 | 未收录但高频使用（历史 35 次 / 近30天 0 次），建议纳入周度发现流程 |
| `animated-financial-display` | codex | 34 | 未收录但高频使用（历史 34 次 / 近30天 0 次），建议纳入周度发现流程 |
| `animated-financial-display` | qoder | 34 | 未收录但高频使用（历史 34 次 / 近30天 0 次），建议纳入周度发现流程 |
| `finishing-a-development-branch` | qoder | 33 | 未收录但高频使用（历史 33 次 / 近30天 0 次），建议纳入周度发现流程 |
| `using-git-worktrees` | qoder | 33 | 未收录但高频使用（历史 33 次 / 近30天 0 次），建议纳入周度发现流程 |
| `academic-research-suite` | qoder | 32 | 未收录但高频使用（历史 32 次 / 近30天 0 次），建议纳入周度发现流程 |
| `requesting-code-review` | qoder | 29 | 未收录但高频使用（历史 29 次 / 近30天 0 次），建议纳入周度发现流程 |
| `vox-director` | codex | 26 | 未收录但高频使用（历史 26 次 / 近30天 0 次），建议纳入周度发现流程 |
| `canvas-design` | codex | 25 | 未收录但高频使用（历史 25 次 / 近30天 0 次），建议纳入周度发现流程 |
| `canvas-design` | qoder | 25 | 未收录但高频使用（历史 25 次 / 近30天 0 次），建议纳入周度发现流程 |
| `verification-loop` | codex | 25 | 未收录但高频使用（历史 25 次 / 近30天 0 次），建议纳入周度发现流程 |
| `dasheng-stage-rewrite` | qoder | 24 | 未收录但高频使用（历史 24 次 / 近30天 0 次），建议纳入周度发现流程 |
| `finish-talking-head` | codex | 23 | 未收录但高频使用（历史 23 次 / 近30天 0 次），建议纳入周度发现流程 |
| `wechat-article-extractor-skill` | codex | 22 | 未收录但高频使用（历史 22 次 / 近30天 0 次），建议纳入周度发现流程 |
| `wechat-article-extractor-skill` | qoder | 22 | 未收录但高频使用（历史 22 次 / 近30天 0 次），建议纳入周度发现流程 |

## 供参考（consider，零调用或久未使用）

| Skill | 运行时 | 调用 | 距上次使用 | 说明 |
|---|---|---:|---|---|
| `using-superpowers` | qoder | 872 | 69.5 | 历史 872 次，已 69.5 天未使用 |
| `a-stock-data` | codex | 561 | 35.4 | 历史 561 次，已 35.4 天未使用 |
| `a-stock-data` | qoder | 561 | 35.4 | 历史 561 次，已 35.4 天未使用 |
| `planning-with-files` | qoder | 257 | 75.6 | 历史 257 次，已 75.6 天未使用 |
| `skill-creator` | qoder | 250 | 34.7 | 历史 250 次，已 34.7 天未使用 |
| `writing-plans` | qoder | 168 | 54.2 | 历史 168 次，已 54.2 天未使用 |
| `dasheng-vox-skills` | codex | 124 | 45.4 | 历史 124 次，已 45.4 天未使用 |
| `media-downloader` | codex | 115 | 36.1 | 历史 115 次，已 36.1 天未使用 |
| `media-downloader` | qoder | 115 | 36.1 | 历史 115 次，已 36.1 天未使用 |
| `subagent-driven-development` | qoder | 104 | 72.6 | 历史 104 次，已 72.6 天未使用 |
| `global-stock-data` | codex | 95 | 37.1 | 历史 95 次，已 37.1 天未使用 |
| `global-stock-data` | qoder | 95 | 37.1 | 历史 95 次，已 37.1 天未使用 |
| `apple-design` | codex | 80 | 45.4 | 历史 80 次，已 45.4 天未使用 |
| `apple-design` | qoder | 80 | 45.4 | 历史 80 次，已 45.4 天未使用 |
| `baoyu-article-illustrator` | codex | 80 | 36.9 | 历史 80 次，已 36.9 天未使用 |
| `baoyu-article-illustrator` | qoder | 80 | 36.9 | 历史 80 次，已 36.9 天未使用 |
| `writing-skills` | qoder | 77 | 69.5 | 历史 77 次，已 69.5 天未使用 |
| `jiebang` | codex | 73 | 43.1 | 历史 73 次，已 43.1 天未使用 |
| `jiebang` | qoder | 73 | 43.1 | 历史 73 次，已 43.1 天未使用 |
| `baoyu-infographic` | codex | 47 | 49.6 | 历史 47 次，已 49.6 天未使用 |
| `baoyu-infographic` | qoder | 47 | 49.6 | 历史 47 次，已 49.6 天未使用 |
| `baoyu-format-markdown` | codex | 37 | 36.9 | 历史 37 次，已 36.9 天未使用 |
| `baoyu-format-markdown` | qoder | 37 | 36.9 | 历史 37 次，已 36.9 天未使用 |
| `tushare-openclaw-skill` | codex | 32 | 49.6 | 历史 32 次，已 49.6 天未使用 |
| `tushare-openclaw-skill` | qoder | 32 | 49.6 | 历史 32 次，已 49.6 天未使用 |
| `codex-responses-tooling` | codex | 31 | 39.6 | 历史 31 次，已 39.6 天未使用 |
| `baoyu-cover-image` | codex | 30 | 35.2 | 历史 30 次，已 35.2 天未使用 |
| `baoyu-cover-image` | qoder | 30 | 35.2 | 历史 30 次，已 35.2 天未使用 |
| `macro-regime-detector` | codex | 30 | 43.0 | 历史 30 次，已 43.0 天未使用 |
| `macro-regime-detector` | qoder | 30 | 43.0 | 历史 30 次，已 43.0 天未使用 |
| `dasheng-stage-brief-ai` | qoder | 28 | 48.4 | 历史 28 次，已 48.4 天未使用 |
| `policy-monitor` | codex | 28 | 37.0 | 历史 28 次，已 37.0 天未使用 |
| `policy-monitor` | qoder | 28 | 37.0 | 历史 28 次，已 37.0 天未使用 |
| `improve-animations` | codex | 26 | 48.6 | 历史 26 次，已 48.6 天未使用 |
| `improve-animations` | qoder | 26 | 48.6 | 历史 26 次，已 48.6 天未使用 |
| `baoyu-xhs-images` | codex | 24 | 69.5 | 历史 24 次，已 69.5 天未使用 |
| `baoyu-xhs-images` | qoder | 24 | 69.5 | 历史 24 次，已 69.5 天未使用 |
| `stock-analysis` | codex | 24 | 62.2 | 历史 24 次，已 62.2 天未使用 |
| `stock-analysis` | qoder | 24 | 62.2 | 历史 24 次，已 62.2 天未使用 |
| `animation-vocabulary` | codex | 23 | 47.5 | 历史 23 次，已 47.5 天未使用 |
| ...另有 425 项见 JSON | | | | |

## 受保护（keep，近期活跃）

`frontend-design`, `frontend-design`, `verification-before-completion`, `brainstorming`, `systematic-debugging`, `e2e-testing`, `iosdev-cn`, `iosdev-cn`, `webapp-testing`, `webapp-testing`, `production-audit`, `search-first`, `improve-codebase-architecture`, `backend-patterns`, `api-design`, `frontend-patterns`, `playwright`, `security-review`, `codebase-onboarding`, `coding-standards`, `baoyu-markdown-to-html`, `baoyu-markdown-to-html`, `finance-data-router`, `finance-data-router`, `design-taste-frontend`, `baoyu-post-to-wechat`, `baoyu-post-to-wechat`, `error-handling`, `backtest-expert`, `backtest-expert`, `agent-introspection-debugging`, `documentation-lookup`, `skill-stocktake`, `minimalist-ui`, `codex-image-bridge`, `data-quality-checker`, `data-quality-checker`, `ecc-codex-ops`, `pdf`, `citation-verification`, `dasheng-hotspot-radar`, `dasheng-style-profiler`, `anthropic-fs-financial-analysis-dcf-model`, `anthropic-fs-financial-analysis-dcf-model`, `portfolio-manager`, `portfolio-manager`, `pptx`, `pre-submission-reviewer`, `llmquant-risk`, `llmquant-risk`, `llmquant-portfolio`, `llmquant-portfolio`, `deep-research`, `docx`, `html-article-generator`, `anthropic-fs-lseg-bond-futures-basis`, `anthropic-fs-lseg-bond-futures-basis`, `content-research-writer`, `hormuz-strait`, `zsxq`
...另有 2 个
