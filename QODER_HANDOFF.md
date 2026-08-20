# Boutique Skills 交接给 Qoder

更新时间：2026-08-19

## 仓库信息

- 路径：/Volumes/PSSD/Projects/boutique-openclaw-skills
- 默认分支：main
- GitHub：https://github.com/leecyno1/boutique-openclaw-skills（远端 origin）
- Gitee：https://gitee.com/leecyno1/boutique-openclaw-skills（远端 gitee）
- 当前技能数：403
- 标准包：30 个 Skill（上限 40，零第三方 key；packs 为参考推荐不随包安装）
- 金融投资标准组合：34 个 Skill（能力位去重，上限 40；同位优先无 key 候选，仅 13 位保留专业数据源 key）
- 组合 API Key 政策：大模型 key 与 GitHub 工具 token 豁免；第三方注册 key 在标准组合硬过滤、在金融组合同位软惩罚（详见 docs/WEEKLY_CURATION.md）

本仓库收录经过搜索、去重、来源审计和评分的 Agent Skills。维护重点是来源可追溯、能力不重复、依赖透明、评分可复核、安装可用。

## 最近完成

| Skill | 评分 | 定位 |
|---|---:|---|
| dasheng-vox-skills | 90/100，5 星 | VOX 视频统一编排、Manifest、Provider 路由、Shotcraft、Gemini、Remotion、QC |
| dasheng-video-omni-browser | 82/100，4 星 | 使用已登录 Chrome Gemini Omni 逐镜生成约 10 秒视频 |

已完成：

- 更新 catalog/default-skills.json、catalog/native-origin-overrides.json。
- 加入高档套件 catalog/suites/dasheng-media-workflow.json。
- 生成 catalog/skills.enriched.json、tiers/high.json 和相关文档索引。
- 添加 reports/source-discovery/dasheng-vox-skills-review-2026-08-16.md。
- 修复 Shotcraft 安装路径发现逻辑。
- 为 Gemini 视频下载增加 Google API 域名校验。
- 未重复收录已有的 video-shotcraft、frontend-design、dasheng-video-director。

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
