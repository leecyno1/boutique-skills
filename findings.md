# Findings

## 2026-09-11（记忆恢复批次）

- 远端 README 三张图裂：`assets/hero-v2.png`、`assets/weekly-pipeline.png`、`assets/bundles-duo.png` 被 README 引用但从未提交，GitHub/Gitee 上 404。根因是 `026c424`（2026-08-19）提交时 `scripts/publish_weekly.sh` 的白名单不含 `assets/`。
- 白名单已于 2026-09-08 补上 `assets/` 与 `.gitignore`，但该修复本身仍未提交；`assets/hero.png` 的本地删除也仍未提交。
- 周度治理 Quest 在 2026-08-29、2026-09-05 两次未触发，`reports/weekly-curation/` 与 `reports/usage/` 最新日期停在 2026-08-22。下次预期触发 2026-09-12（周六）09:00 Asia/Shanghai。
- 记忆文件陈旧：本文件曾记录 318 个技能目录，`QODER_HANDOFF.md` 曾记录 403 个技能；实际为 `skills/default/` 560 个目录、注册表 424 个技能。两者已于 2026-09-11 校正。
- 会话上下文丢失后，新会话未必挂载 `SearchMemory`/`UpdateMemory` 与 `schedule` MCP，记忆必须落在仓库文件里才可恢复（恢复顺序见 `QODER_HANDOFF.md`）。
- `reports/usage/pending-cleanup.json` 的 `items` 为空，无待确认卸载项。

## 2026-08-09（已解决）

- `skills/default` 当时含 318 个技能目录。
- `catalog/default-skills.json` 当时有 320 条分层条目，但仅 179 个唯一技能 ID，因为 low/medium/high 是累积分层。
- 当时所有默认目录条目的 `source` 都指向 `leecyno1/auto-install-Openclaw`，是镜像/拷贝路径而非原生上游。
- `README.md` 声称包含原始仓库链接，但当时的默认目录并未提供。
- 当时工作流按周运行，需求是月度评审。

以上五项已在 enriched catalog 升级中解决：原生来源覆盖后 `needs_origin_review = 0`（418 个已核验或引用，6 个预设能力豁免），分层与索引由 `scripts/generate_enriched_catalog.py` 生成，周度治理保留并另加月度深度评审建议。
