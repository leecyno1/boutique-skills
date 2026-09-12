# Findings

## 2026-09-12（周度治理·网络故障与修复批次）

已解决：

- 周度流水线第 1 步连续两次失败（`RemoteDisconnected` / `SSLEOFError`），重试无效。根因：网络中间设备切断 Python OpenSSL 的 TLS 指纹（api.github.com 与 raw.githubusercontent.com 均中招）；curl（LibreSSL）与 gh（Go）指纹放行；本地代理 127.0.0.1:7890 对 GitHub 出口反而失效（分流节点问题）。已修复：`scripts/weekly_curation.py` 新增 curl 子进程回退（`_curl_fetch` / `_api_get_curl`，`raw_file_bytes` 同步回退），urllib 遇 SSL 切断/连接重置时自动降级，向后兼容，CI 等正常环境零影响。修复后全流程跑通。
- curl 回退首版漏了 `-L`：prune 检查上游时 `leecyno1/dasheng-media-workflow-skills` 返回 301（上游已改名）被误判为失败。已加 `-L` 跟随重定向，与 urllib 自动重定向行为对齐。
- 上游改名事实：`leecyno1/dasheng-media-workflow-skills` → `leecyno1/newma-media-studio`（301 重定向，上游存活，prune 未误判 404）。SOURCE.txt 与 origin 覆盖仍指旧名，GitHub 会重定向，暂不需改动；若后续 404 再更新。
- 已知残留：curl 子进程命令行携带 token（`ps aux` 可见），本机单用户环境风险可控；后续可改用 `--config -` 从 stdin 传 header 消除。

待观察：

- Python OpenSSL TLS 指纹切断是否为长期网络策略：若恢复，curl 回退自动闲置无害；若持续，后续脚本（如 `check_upstream_updates.py`）如遇同类失败可复用 `_curl_fetch` 模式。

## 2026-09-11（记忆恢复批次）

已解决（commit `2cdfd9f`，已推送 origin 与 gitee）：

- 远端 README 三张图裂：`assets/hero-v2.png`、`assets/weekly-pipeline.png`、`assets/bundles-duo.png` 被 README 引用但从未提交，GitHub/Gitee 上 404。根因是 `026c424`（2026-08-19）提交时 `scripts/publish_weekly.sh` 的白名单不含 `assets/`。三张图已入库，被取代的 `assets/hero.png` 已删除。
- 白名单已补 `assets/` 与 `.gitignore`（2026-09-08 修改，2026-09-11 随本次提交入库）。
- 记忆文件陈旧：本文件曾记录 318 个技能目录，`QODER_HANDOFF.md` 曾记录 403 个技能；实际为 `skills/default/` 560 个目录、注册表 424 个技能。两者已校正。
- 会话上下文丢失后，新会话未必挂载 `SearchMemory`/`UpdateMemory` 与 `schedule` MCP，记忆必须落在仓库文件里才可恢复（恢复顺序见 `QODER_HANDOFF.md`）。
- GitHub 仓库已改名为 `leecyno1/boutique-skills`：推送时远端返回 "This repository moved"。旧 URL 仍重定向，`git ls-remote` 新旧地址同指同一提交，推送不受影响。仓库大部分位置（`scripts/generate_assets.py`、`scripts/import_installer_default_skills.py`、`docs/generated/*`、`docs/tiers/*`、`docs/SKILL_MANUALS.md`）早已用新名，只有三处遗留已修正：`scripts/generate_finance_suite.py` 的硬编码 source/native_origin、`catalog/suites/finance-investment-standard.json`、`README.md` 套件表对应行。`origin` 远端地址已指向新名；Gitee 未改名，`GITEE_URL` 保持原值。本地目录名仍为 boutique-openclaw-skills，属目录名不是仓库名，不改。
- `scripts/publish_weekly.sh` 白名单原本不含 `findings.md` 与 `task_plan.md`，这两个记忆文件的改动永远不会被周度流程提交；已补入白名单。

未决：

- 周度治理 Quest 在 2026-08-29、2026-09-05 两次未触发，`reports/weekly-curation/` 与 `reports/usage/` 最新日期停在 2026-08-22。下次预期触发 2026-09-12（周六）09:00 Asia/Shanghai。
- `reports/usage/pending-cleanup.json` 的 `items` 为空，无待确认卸载项。

## 2026-08-09（已解决）

- `skills/default` 当时含 318 个技能目录。
- `catalog/default-skills.json` 当时有 320 条分层条目，但仅 179 个唯一技能 ID，因为 low/medium/high 是累积分层。
- 当时所有默认目录条目的 `source` 都指向 `leecyno1/auto-install-Openclaw`，是镜像/拷贝路径而非原生上游。
- `README.md` 声称包含原始仓库链接，但当时的默认目录并未提供。
- 当时工作流按周运行，需求是月度评审。

以上五项已在 enriched catalog 升级中解决：原生来源覆盖后 `needs_origin_review = 0`（418 个已核验或引用，6 个预设能力豁免），分层与索引由 `scripts/generate_enriched_catalog.py` 生成，周度治理保留并另加月度深度评审建议。
