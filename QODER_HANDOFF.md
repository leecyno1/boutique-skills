# Boutique Skills 交接给 Qoder

更新时间：2026-09-30

## 仓库信息

- 路径：/Volumes/PSSD/Projects/boutique-openclaw-skills
- 默认分支：main
- GitHub：https://github.com/leecyno1/boutique-skills（远端 origin；2026-09-11 由 boutique-openclaw-skills 改名，origin URL 已同步更新）
- Gitee：https://gitee.com/leecyno1/boutique-openclaw-skills（远端 gitee；未改名）
- 注意：本地目录名仍是 boutique-openclaw-skills，仓库内出现该字符串的路径（会话转录目录、RepoWiki 目录、审计报告里的绝对路径）是目录名不是仓库名，不要改。
- 当前技能数：458（catalog/skills.enriched.json，生成于 2026-09-30）；skills/default/ 目录 594 个（含未注册候选与套件成员）
- 横向分层：high 458 / medium 85 / low 67（累积分层，非互斥）；纵向 L1 21 / L2 160 / L3 277
- 星级分布：5★ 110 / 4★ 230 / 3★ 112 / 1★ 6
- 来源核验：452 已核验或引用，6 个预设能力豁免，needs_origin_review = 0
- 标准包：30 个 Skill（上限 40，零第三方 key；packs 为参考推荐不随包安装）
- 金融投资标准组合：34 个 Skill（能力位去重，上限 40；同位优先无 key 候选，仅 13 位保留专业数据源 key）
- 组合 API Key 政策：大模型 key 与 GitHub 工具 token 豁免；第三方注册 key 在标准组合硬过滤、在金融组合同位软惩罚（详见 docs/WEEKLY_CURATION.md）

本仓库收录经过搜索、去重、来源审计和评分的 Agent Skills。维护重点是来源可追溯、能力不重复、依赖透明、评分可复核、安装可用。

## 当前待办（2026-09-30 更新）

工作区在本轮补漏周度治理后干净，`main` 与 origin、gitee 三方同步（具体提交号以 `git log --oneline -1` 为准，不要在记忆文件里钉哈希，每次周度提交都会失效）。2026-09-11 批次（README 裂图、仓库改名引用、白名单补齐）明细见 `findings.md`；持久结论：`publish_weekly.sh` 白名单已含 `assets/`、`.gitignore`、`findings.md`、`task_plan.md`，`.gitignore` 排除遥测缓存与 `.qoder/`。

未决（按处理紧迫度）：

1. **周度治理 Quest 处于手动暂停**：id `70f2e60c-b189-445f-ab92-6e4e642f9975`（`0 9 * * 6` Asia/Shanghai）当前 `enabled=false`、`pauseReason=manual`，因此 2026-09-19、2026-09-26 未触发，2026-09-30 为手动补漏。是否重新启用属用户裁决，不代为开启；下次自然触发点为每周六 09:00。
2. **Qoder 侧归档目录已被清空**：`~/.qoder/skills-archive` 不存在，而 `~/.qoder/skills` 有 260/311 个目录 mtime 为 2026-09-16 —— 当天发生过一次批量恢复/重装，2026-08-22 归档卸载的 31 个 Qoder 技能被还原，归档副本同时丢失（`reports/usage/cleanup-receipts.jsonl` 里的 `to` 路径已失效，无法 `mv` 回滚）。Codex 侧未受影响：`~/.codex/skills-archive` 22 项完好，2026-09-12 归档的三项仍未复活。含义：归档式卸载对 Qoder 客户端重装不具持久性，卸载建议应当轮确认执行，不要跨周悬挂。
3. **陈旧重复检出**：`/Volumes/PSSD/Projects/boutique-skills` 与本仓库同指 `leecyno1/boutique-skills`，停在 `e16c7a0`（2026-08-16）且从未 fetch；其工作区含 4 个受保护 tushare-eval 文件的未提交改动（生成时间 2026-06-18，比本仓库已提交的 2026-06-14 新，从未入库）。本轮未触碰该目录，保留/同步/归档待用户裁决。
4. **月度上游检查逾期**：`reports/upstream-check-latest.md` 停在 2026-08-16（45 天），`make upstream-check` 未跑。
5. **7 项本地卸载建议待确认**（`reports/usage/pending-cleanup.json`，绝不自动执行）：qoder 侧 `wechat-topic-outline-planner`、`doc`、`openclaw-stock`、`openclaw-stock-analyzer`、`stock_datasource`；codex 侧 `lin-lefeng-perspective`、`sun-lumin-perspective`。确认后 `python3 scripts/uninstall_skills.py --confirm`。

## 最近完成（2026-09-30 补漏周度治理）

发现阶段评估 41 个候选仓库，自动入库 5 个仓库共 21 个 Skill；出库检查 415 个上游，0 项移除。

| 上游仓库 | 星数 | 评分 | 入库 Skill |
|---|---:|---:|---|
| agricidaniel/claude-seo | 18000 | 80 | seo-agentic、seo-audit、seo-backlinks、seo-cluster、seo-competitor-pages |
| wanshuiyin/auto-claude-code-research-in-sleep | 16852 | 80 | ablation-planner、alphaxiv、analyze-results、arxiv、auto-paper-improvement-loop、browser-cdp |
| zenstory-ai/oh-story-claudecode | 7186 | 80 | story-cover、story-deslop、story-import、story-long-analyze |
| elementalsouls/claude-bughunter | 4731 | 80 | apk-redteam-pipeline、bb-local-toolkit、bb-methodology、bug-bounty、bugcrowd-reporting |
| nevamind-ai/memu | 14495 | 75 | memu（NOASSERTION 已核验为逐字 Apache-2.0，见其 SOURCE.txt） |

本轮另修复 `scripts/weekly_curation.py` 的 curl 回退把 token 暴露在 `ps aux` 的问题（改为 `curl --config -` 走 stdin），新增 `tests/test_curl_token_hygiene.py` 并接入 `weekly_cycle.sh` 第 8 步。

上一轮（2026-08-16）入库：

| Skill | 评分 | 定位 |
|---|---:|---|
| dasheng-vox-skills | 90/100，5 星 | VOX 视频统一编排、Manifest、Provider 路由、Shotcraft、Gemini、Remotion、QC |
| dasheng-video-omni-browser | 82/100，4 星 | 使用已登录 Chrome Gemini Omni 逐镜生成约 10 秒视频 |

## 关键目录

- skills/default/<name>/：Skill 主文件、配置、Agent 展示信息和来源说明。
- catalog/default-skills.json：基础注册表。
- catalog/native-origin-overrides.json：来源核验覆盖。
- catalog/suites/：组合套件（含金融投资标准组合）。
- scripts/generate_enriched_catalog.py：生成评分、依赖和文档索引。
- scripts/generate_finance_suite.py：生成金融组合（能力位去重，<= 40）。
- scripts/weekly_curation.py：周度发现/评分/入库/出库。
- scripts/telemetry_collect.py：本地使用频率遥测（扫描 Qoder/Claude Code/Codex/Kimi Code 会话日志，输出 reports/usage/ 周报与 usage-scores.json，评分联动 +0~8 分；仅本地聚合不读取消息内容）。
- scripts/usage_recommendations.py：skills 调整建议（keep/remove/consider/discover 四级，remove 写入 pending-cleanup.json 待确认）。
- scripts/uninstall_skills.py：确认后的归档式卸载（默认 dry-run，--confirm 执行，移入 *-archive/ 可恢复，活跃技能强制拒绝）。
- scripts/weekly_cycle.sh：周度全流程编排（十步：发现→出库→遥测→目录→组合→README→报告→审计测试→建议→发布）。
- scripts/publish_weekly.sh：白名单提交并推送 GitHub+Gitee。
- scripts/audit_skills.py：全库审计。
- scripts/install-suite.sh：套件安装和 dry-run。
- reports/source-discovery/：评审报告。
- reports/weekly-curation/：周度发现/出库报告。

## 新 Skill 更新流程

1. 先在本地搜索同名和同能力 Skill，避免重复。
2. 再检查来源仓库、SKILL.md、脚本、依赖、许可证和最近提交。
3. 评估功能覆盖、可执行性、质量控制、移植性、安全、来源和维护价值。
4. 评分建议：90 分以上 5 星；75–89 分 4 星；60–74 分 3 星；低于 60 分不入库。
5. 每个候选添加 reports/source-discovery/<name>-review-YYYY-MM-DD.md。
6. 将文件放入 skills/default/<name>/，删除 __pycache__、临时文件、运行媒体和凭证。
7. 添加 SOURCE.txt，记录来源、许可证、快照提交和移植修正。
8. 更新基础目录、来源覆盖、评分覆盖和相关套件。
9. 重新生成目录：

   python3 scripts/generate_enriched_catalog.py

10. 检查安装预览：

   ./scripts/install-suite.sh <suite-id> --dry-run

## 验证命令

    python3 -m json.tool catalog/default-skills.json >/dev/null
    python3 -m json.tool catalog/native-origin-overrides.json >/dev/null
    python3 -m py_compile skills/default/<name>/scripts/*.py
    python3 scripts/audit_skills.py --report /tmp/boutique-audit.md --json /tmp/boutique-audit.json
    git diff --check

有对应测试时运行对应 pytest。若 pytest 未安装，应明确记录为测试环境缺失，不要误报成代码失败。

## Git 规则

- 禁止使用 git reset --hard、git clean、git checkout -- 覆盖工作区。
- 提交前使用白名单 git add（scripts/publish_weekly.sh 已内置）。
- 当前以下四个文件已有用户改动，不能回滚、覆盖或代提交：

    reports/finance-skill-eval/tushare-eval/standard-finance-skills-recommendation.json
    reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.html
    reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.json
    reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.md

- 提交前确认 git diff --cached --name-only 不含以上文件。
- 提交后同步两个远端（publish_weekly.sh 自动完成）：

    git push origin main
    git push gitee main
    git fetch origin main --quiet
    git fetch gitee main --quiet
    git rev-parse HEAD origin/main gitee/main

## 周度自动治理（2026-08-19 新增）

每周定时任务（Qoder 会话 schedule，周六 09:00 Asia/Shanghai）执行：

    ./scripts/weekly_cycle.sh

流程：发现（GitHub 搜索+评分+高分入库）→ 出库（上游失效/低分/被支配）→ 重建目录 → 刷新金融组合 → 审计 → 测试 → 双远端发布。

- 入库门槛：候选 >= 75 分且含 SKILL.md 且 >= 20 星且一年内活跃且无能力重叠；60-74 分进人工复核清单。
- 出库规则：上游 404 / 内部评分 < 60 / 同冲突组内被高出 >= 15 分的同类支配且自身 <= 70 分。
- 标准组合 <= 40 base skills（一能力一技能）；金融组合 <= 40（能力位取最高分）。
- 详见 docs/WEEKLY_CURATION.md。

## 定时维护建议（月度深度评审，可与周度自动流程互补）

每周或每两周：

1. 扫描新候选和上游更新。
2. 检查已入库 Skill 的来源仓库是否有新提交。
3. 对最近更新或高使用频率 Skill 重跑评分。
4. 清理重复能力和失效来源。
5. 运行目录生成、安装 dry-run 和全库审计。
6. 只提交本轮变更，并同步 GitHub/Gitee。

记录位置：新增候选和评分报告放在 reports/source-discovery/；问题放在 findings.md；来源和版本变化写入 SOURCE.txt 与提交记录。

## 已知限制

- dasheng-video-omni-browser 依赖用户已有 Chrome 登录态和 Gemini 网页 UI，不是稳定 API。
- dasheng-vox-skills 的完整导演 CLI、Remotion 工程和实际媒体产物仍在 /Volumes/PSSD/Projects/公众号文章；本仓库收录的是可复用编排核心和必要参考文件。
- 全库审计可能报告其他 Skill 的环境变量或风险扫描提示，先确认是否属于本轮改动。
- 真实 Gemini 在线生成、Chrome 下载和平台登录不在静态验证范围内。

## 接手完成标准

Qoder 接手后应能根据来源链接或本地 Skill 目录完成搜索、评分、去重、入库、目录生成、安装 dry-run、全库审计，并在保留用户改动的前提下同步 GitHub 和 Gitee。

## 记忆位置与上下文恢复（2026-09-11 补记）

会话上下文可能整体丢失，且新会话不一定挂载 `SearchMemory`/`UpdateMemory` 或 `schedule` MCP 工具。此时按下列顺序从磁盘恢复，不要凭印象作答：

1. 本文件（仓库根 `QODER_HANDOFF.md`）：流程、规则、待办，是唯一的权威长期记忆。
2. `task_plan.md` / `progress.md`：历史阶段与验证结论（origin/index/scoring 升级已于 2026-08 完成，needs_origin_review = 0）。
3. `findings.md`：问题清单，按日期分批记录。
4. 会话转录：`~/.qoder/projects/-Volumes-PSSD-Projects-boutique-openclaw-skills/transcript/*.jsonl`，可解析出历次用户指令、工具调用与结论。
5. 结构化仓库知识（RepoWiki）：`~/.qoder/knowledges/boutique-openclaw-skills/main__zh-CN/` 与仓库内 `.qoder/repowiki/`（2026-09-09 生成，完好）。
6. 客观事实以 `git log` / `git status` / `catalog/skills.enriched.json` 的 `summary` 为准，记忆文件与它们冲突时以仓库为准并回写记忆。

Quest（定时任务）由 `schedule` MCP 服务管理，不在本仓库内，也不等于本地 cron。该工具未挂载时无法查询或重建 Quest，只能从 `reports/weekly-curation/` 的最新日期推断是否真的触发过，并在本文件登记预期触发时间。
