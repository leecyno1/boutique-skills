# AGENTS.md — boutique-skills

接手本仓库的 Agent 先读这份，再按任务打开下面的权威文档。换机器接手另读 [docs/MIGRATION.md](docs/MIGRATION.md)。

## 这是什么

一个经过来源审计、去重、评分的 Agent Skills 精选库，外加一条每周自动运行的治理流水线。仓库既是技能内容本身，也是管理这些技能的代码。规模、分层、星级、标准包与组合成员一律现查 `catalog/`，不要从本文档或记忆里取数字。

## 权威文档顺序

1. [QODER_HANDOFF.md](QODER_HANDOFF.md) — 当前状态、未决待办、最近完成。每轮治理后刷新。
2. [findings.md](findings.md) — 每轮裁定的证据与结论，倒序排列。要理解"为什么这样定"看这里。
3. [docs/WEEKLY_CURATION.md](docs/WEEKLY_CURATION.md) — 周度 11 步、发现评分模型、出入库规则、分类器硬规则。
4. [task_plan.md](task_plan.md) — 阶段账本，记录每步做了什么、影响面多大。
5. `catalog/*.json` — 机器可读事实，全部由脚本生成。

提交号以 `git log --oneline -1` 为准。任何文档里的哈希、数量、日期都可能过期，现查优先。

## 硬规则

违反这些会破坏治理链路，不是风格偏好。

- **目录只能由脚本生成。** 改分类、评分、依赖推断就改 `scripts/generate_enriched_catalog.py`，然后重生成。不要手改 `catalog/*.json`、README 索引块或 `docs/generated/`。`tests/test_category_classifier.py` 会断言目录与分类器实时一致。
- **分类器兜底桶必须为空。** `commerce-ops` 只能由 `CATEGORY_OVERRIDES` 显式产生。新技能落进兜底桶时读它的 SKILL.md、按同家族惯例写进覆盖表。加短关键词前先判断会不会嵌在别的英文单词里；`BOUNDARY_KEYWORDS` 里每个词都要有具名实证误命中。改关键词表前先跑影响面模拟，改完重生成并跑全部门禁。
- **设计流派只认 taste 一家为默认。** `design-taste-frontend` 占标准包 frontend 槽位。其他设计技能优于 taste 或与 taste 互补才留，否则按重复出库。裁定记录在 `catalog/retired-skills.json` 的 `design_school_decision`。
- **出库走归档流程，不硬删。** 本机卸载用 `scripts/uninstall_skills.py`（默认 dry-run，`--confirm` 才执行，`--include-active` 只用于人工裁定）。仓库出库要登记进 `catalog/retired-skills.json` 防再导入。整库屏蔽只适用于该库已无在库技能的情况，`tests/test_retired_guard.py` 会断言。
- **四个保护文件永不提交**：`reports/finance-skill-eval/tushare-eval/` 下的 standard-finance-skills-recommendation.json 与 tushare-finance-skill-evaluation.{html,json,md}。`publish_weekly.sh` 内置拦截。
- **发布只用 `scripts/publish_weekly.sh`。** 白名单 add、保护文件拦截、HTTPS→SSH 回退、双远端 SHA 校验都在里面。不要 force-push、squash、`git reset --hard`、`git clean`、`git checkout --`。
- **密钥只读键名。** 需要 token 时只看环境变量名与掩码，绝不把值写进工具输出、提交、报告或回复。

## 验收命令

改动后全部要过，任一非零即中止发布。

```bash
python3 scripts/audit_skills.py          # 目录/来源/能力重复/标准包一致性
python3 scripts/check_skill_syntax.py    # 全库 py + js/mjs 语法
python3 scripts/check_new_risks.py       # 对比 catalog/risky-baseline.json，新增风险即失败
for t in tests/test_*.py; do python3 "$t"; done
```

重生成目录与组合：

```bash
python3 scripts/generate_enriched_catalog.py
python3 scripts/generate_finance_suite.py
```

完整周度流程 `./scripts/weekly_cycle.sh`（11 步，末步双远端发布），单步入口见 `Makefile`。

## 自动化

Quest `436c5b6e-10c6-487b-b73a-1504e4cc89c0`，directory 域绑定本仓库目录，每周六 09:00 Asia/Shanghai，Full Access，独立会话。**同一时间只允许一台机器启用**，两台同时跑会重复发布并互相覆盖。换机器时先停旧机任务再建新机任务，见 docs/MIGRATION.md。

## 工具链

Python >= 3.12（`check_skill_syntax.py` 在低版本会自动 re-exec 到新解释器）、Node（语法门禁要跑 .mjs/.js）、git、gh CLI。`gh` 与 git 凭据用于发现阶段和双远端发布。

周度 11 步与全部门禁只用标准库，不需要预装第三方包。两个离线工具例外：`scripts/build_skills_directory.py` 需要 PyYAML，`scripts/generate_assets.py` 需要 Pillow。**当前旧机缺 PyYAML，前者跑不起来**；它不在周度流程里，所以门禁全绿也掩盖了这一点。要用先 `python3 -m pip install PyYAML Pillow`。

仓库没有 node_modules。`optimization/skillopt/` 是 vendored 子项目，有自己的 requirements.txt 与 .env.example，不参与周度流程。