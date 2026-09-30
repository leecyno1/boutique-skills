# Findings

## 2026-09-30（补漏周度治理 + curl token 泄露修复）

已解决：

- 2026-09-12 记录的残留项：curl 回退把 GitHub token 放在子进程命令行（`ps aux` 可见）。已改为 `curl --config -` 从 stdin 传 header，token 不再进入 argv；`_curl_config_escape` 负责 config 值转义。新增 `tests/test_curl_token_hygiene.py`（token 不入 argv、转义、无 header 时不加 `--config`），已接入 `scripts/weekly_cycle.sh` 第 8 步。验证：authenticated `rate_limit` 返回 limit=5000、raw 文件下载 200、404 仍返回 None、上游改名仓库 301 仍跟随。
- 补漏周度治理（09-19、09-26 因 Quest 暂停未触发）：发现阶段评估 41 个候选，自动入库 5 个仓库 21 个 Skill（claude-seo 5 个 SEO、auto-claude-code-research-in-sleep 6 个科研、oh-story-claudecode 4 个写作、claude-bughunter 5 个漏洞赏金、memu 1 个记忆）；prune 检查 415 个上游，0 项移除。目录 458 个技能（high 458 / medium 85 / low 67），标准包 30，金融组合 34，needs_origin_review = 0。审计 `missing_skills=0`、`duplicate_capabilities=0`、`missing_native_origins=0`、`standard_bundle_issues=0`，`risky_hits=15` 与上轮持平且无一命中新入库技能，`missing_env` 由 116 升至 149（新技能带 env 依赖，预期）。三个测试文件全部通过。
- 入库质检：21 个新目录 SKILL.md 与 SOURCE.txt 齐备，无 `__pycache__`/媒体/大文件（合计 1.6 MB），15 个附带脚本 `py_compile` 与 `node --check` 全通过，注册表分层单调性成立，21 条 origin 已登记。
- `memu` 许可证核验：GitHub licensee 报 NOASSERTION，实际 `LICENSE.txt` 是逐字 Apache-2.0 正文（仅因缩进与附加版权段识别失败），已在 `skills/default/memu/SOURCE.txt` 记录核验结论与日期。

未决：

- 周度治理 Quest（id `70f2e60c-b189-445f-ab92-6e4e642f9975`，`0 9 * * 6` Asia/Shanghai）当前 `enabled=false`、`pauseReason=manual`，因此 2026-09-19 与 2026-09-26 两次未触发，本轮为手动补漏。是否重新启用待用户裁决，不代为开启。
- **归档式卸载对 Qoder 客户端重装不具持久性**：`~/.qoder/skills-archive` 已不存在，`~/.qoder/skills` 中 260/311 个目录 mtime 为 2026-09-16，说明当天发生过一次批量恢复/重装，2026-08-22 归档卸载的 31 个 Qoder 技能被还原且归档副本丢失 —— `reports/usage/cleanup-receipts.jsonl` 中对应 `to` 路径已失效，无法 `mv` 回滚，只能重新从上游获取。Codex 侧未受影响（`~/.codex/skills-archive` 22 项完好，2026-09-12 归档的 `grill-with-docs`、`mcp-server-patterns`、`recursive-decision-ledger` 仍未复活）。后果已经显现：本轮 7 项卸载建议里 `doc` 与 `wechat-topic-outline-planner` 是 08-22 已卸载过的技能，属被还原后重新命中。处理原则：卸载建议应当轮确认执行，不跨周悬挂。
- `/Volumes/PSSD/Projects/boutique-skills` 是同一 GitHub 仓库（origin 同为 `leecyno1/boutique-skills`）的陈旧本地检出，停在 `e16c7a0`（2026-08-16），未 fetch 过本轮提交。其工作区含 4 个受保护 tushare-eval 文件的未提交改动，生成时间 `2026-06-18T15:20:38`，比本仓库已提交版本的 `2026-06-14T07:38:30` 新，从未入库。本轮不触碰该目录；保留/同步/归档待用户裁决。
- `reports/upstream-check-latest.md` 停在 2026-08-16（45 天），月度上游更新检查未按期跑。
- 本轮 7 项卸载建议待用户确认（`reports/usage/pending-cleanup.json`，status=pending，绝不自动执行）。

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
