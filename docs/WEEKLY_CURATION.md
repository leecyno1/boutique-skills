# Weekly Skills Curation

每周自动化治理流程：搜索 GitHub 优质 skills、评估打分、高分入库、低分/失效/被支配技能出库、刷新标准组合与金融组合，并同步 GitHub 与 Gitee。

## 一键执行

```bash
./scripts/weekly_cycle.sh
```

完整流程（发现入库 → 出库 → 重建目录 → 刷新金融组合 → 审计 → 测试 → 双远端发布）。

## 分步命令

```bash
# 1. 搜索 + 评估（只产报告，不入库）
python3 scripts/weekly_curation.py discover

# 2. 搜索 + 评估 + 自动入库高分候选（>=75 分）
python3 scripts/weekly_curation.py discover --import-approved

# 3. 出库检查（只产建议报告）
python3 scripts/weekly_curation.py prune

# 4. 执行出库
python3 scripts/weekly_curation.py prune --apply

# 5. 重建目录与标准组合
python3 scripts/generate_enriched_catalog.py

# 6. 重建金融组合（能力位去重，<= 40）
python3 scripts/generate_finance_suite.py

# 7. 审计 + 测试
python3 scripts/audit_skills.py
python3 tests/test_governance_files.py
python3 tests/test_tier_catalog.py

# 8. 发布到 GitHub 和 Gitee
./scripts/publish_weekly.sh "Weekly skills curation $(date +%F)"
```

## 发现与评分模型（候选仓库，0-100）

| 因子 | 分值 | 规则 |
|---|---:|---|
| GitHub stars | 0-30 | >=2000★:30; >=500★:26; >=200★:22; >=100★:18; >=50★:14; >=20★:10 |
| 活跃度 | -8~20 | 最近推送 <=30天:20; <=90天:15; <=180天:10; <=365天:5; >365天:-8 |
| 结构 | 0-30 | 根 SKILL.md +15; skills/ 子目录各 +5（封顶 +10）; 明确 license +5 |
| 质量 | 0-15 | 描述 >=60 字符 +5; 相关 topics +5; >=100★ +5 |
| 能力重叠 | -15 | 与现有冲突组能力重复 |

**入库门槛（自动）**：score >= 75 且含 SKILL.md 且 stars >= 20 且一年内有推送且无能力重叠。
60-74 分进入 `review` 清单，由月评人工处理；低于 60 忽略。

## 出库规则（自动）

1. **upstream_gone**：原生来源 GitHub 仓库 404/不可访问。
2. **low_score**：内部评分 < 60。
3. **dominated_duplicate**：同一冲突组内存在高出 >= 15 分的同类技能，且自身 <= 70 分。

## 组合控制（用户要求：各 <= 40）

| 组合 | 定位 | 数量 | 生成器 |
|---|---|---:|---|
| Standard Bundle (`catalog/standard-bundle.json`) | 日常用户基础场景，一能力一技能，零第三方 key | 30 base（上限 40） | `scripts/generate_enriched_catalog.py` |
| Finance Suite (`catalog/suites/finance-investment-standard.json`) | 金融投资用户进阶场景，能力位去重取最优 | 34（上限 40） | `scripts/generate_finance_suite.py` |

### API Key 政策（2026-08-19 新增）

两个组合尽量避免需要复杂注册的第三方服务 API key（大模型 key 与 GitHub 工具 token 豁免）：

- **豁免 key**：主流大模型（OPENAI/ANTHROPIC/GEMINI/DEEPSEEK/MOONSHOT/QWEN/DASHSCOPE/MINIMAX/ZHIPU 等）与开发者工具 token（GITHUB_TOKEN/GH_TOKEN）。
- **标准组合**：硬过滤——任何需要第三方 key 的技能不入组合；能力位无 keyless 候选时直接跳过该位（当前跳过：email-agent、finance-data、ima-notes-knowledge、media-download）。政策与跳过清单写入 `standard-bundle.json` 的 `api_key_policy` 字段。
- **金融组合**：软惩罚（同位候选评分 -12）——同位存在 direct/browser 候选时必胜出；仅当整位无 keyless 候选才保留 key 类技能（当前 13/34 位，均为机构数据/美股筛选器/期权/组合风险等专业深水区，且 TUSHARE_TOKEN 类为免费注册）。每个能力位的 access 与 api_keys 字段已在 suite JSON 中标注，可自行取舍。
- **误报修复**：key 检测已改为词边界匹配（修复 "ima" 误匹配 "image"），自签 secret（JWT_SECRET 等）不再计入 API key。

- 标准组合安装只装 base skills；`skill_packs` 是参考推荐（Claude Trading Skills 已并入金融组合）。
- 金融组合每个能力位（A股数据/全球数据/宏观/政策/筛选/估值/交易计划/仓位/期权/组合风控/监控/回测/复盘/报告/知识库等 34 位）只保留评分最高的技能。
- 同类重复比较：能力位/冲突组内按评分排序，只保留最高分；被支配技能按出库规则 3 清理。

## 发布规则

`scripts/publish_weekly.sh`：

- 白名单 `git add`（catalog/ skills/ docs/ reports/ scripts/ tiers/ tests/ README 等）。
- 拒绝提交 4 个用户保护文件（`reports/finance-skill-eval/tushare-eval/` 下）。
- 提交后推送 `origin main`（GitHub）与 `gitee main`（Gitee），并校验三方 SHA 一致。
- 远端 `gitee` 缺失时自动添加（`GITEE_URL` 可覆盖）。

## 报告位置

- 发现周报：`reports/weekly-curation/discovery-YYYY-MM-DD.{md,json}`
- 出库周报：`reports/weekly-curation/prune-YYYY-MM-DD.{md,json}`
- 入库评审：`reports/source-discovery/<skill>-review-YYYY-MM-DD.md`

## 使用频率遥测（2026-08-21 新增）

`scripts/telemetry_collect.py` 从本机 Agent 会话日志统计每个 skill 的被调用频率，支持三个运行时：

| 运行时 | 日志位置 | 使用信号 |
|---|---|---|
| Qoder | `~/.qoder/projects/**/*.jsonl` | `Skill` tool_use（`input.skill`）与 `/skill` 斜杠命令 |
| Claude Code | `~/.claude/projects/**/*.jsonl` | 同上（同构格式） |
| Codex CLI | `~/.codex/sessions/` 与 `~/.codex/archived_sessions/` 的 rollout JSONL | **工具调用中读取技能的 SKILL.md 路径**（`skills/<name>/SKILL.md`）；`<skills_instructions>` 注入列表不计入 |
| Kimi Code | `~/.kimi-code/sessions/**/wire.jsonl` | `tool.call` 事件且 `name="Skill"`（args.skill） |

已探测但不接入的运行时（无技能使用信号或无会话数据）：Gemini CLI（会话为 tmp 检查点格式，无结构化工具日志）、OpenCode（SQLite 中无实质会话）、GitHub Copilot CLI（ACP 后端，无 Agent Skills 机制）、cagent/Lingma/MarsCode/OpenClaw 生态（无技能机制或无数据）。新装上述以外的 Agent CLI 时，在 `SESSION_ROOTS` 中追加日志根目录并按格式扩展 `extract_uses_worker` 即可。

- 输出：`reports/usage/usage-YYYY-MM-DD.{json,md}`（频率报告，含组合覆盖与未收录高频清单）与 `reports/usage/usage-scores.json`（机器可读加分）。
- 评分联动：使用频率加分 0~8（log₂ 调用次数 × 时间衰减：≤7天 1.0 / ≤30天 0.7 / ≤90天 0.4 / 更久 0.15），在 `generate_enriched_catalog.py` 的 `score_item` 中叠加，无数据时为 0（向后兼容）。
- 性能：首次全量扫描后，增量状态（`.scan-state.json`/`.scan-uses.json`，已 gitignore）记录文件指纹与已提取记录，后续运行只扫新增/变化文件（秒级）；Codex 历史约 68GB，4 进程并行首扫约 1 分钟。`--rescan-all` 强制全量。
- 隐私红线：仅本地聚合技能名/时间戳/会话 ID/工作目录，不读取或存储任何消息内容，不上传。

```bash
python3 scripts/telemetry_collect.py --days 30               # 增量采集
python3 scripts/telemetry_collect.py --days 30 --rescan-all  # 强制全量
```

## 清理建议与确认卸载（2026-08-21 新增）

周度流水线第 9 步运行 `scripts/usage_recommendations.py`，综合已安装技能（Codex/Qoder/agents/lingma 四运行时）、最新使用遥测与仓库注册表，把每个已装技能分为四级：

| 分级 | 判定 | 动作 |
|---|---|---|
| keep | 近 30 天有调用 | 永久保护，绝不进入卸载建议 |
| remove | 未收录且零调用满 60 天，或未收录且 90 天未用 | 写入 pending-cleanup.json 待用户确认 |
| consider | 在册但零调用，或 30-90 天未用 | 仅供参考（组合瘦身边缘信号） |
| discover | 未收录但高频（历史≥20 次或近30天≥5 次） | 反哺周度发现流程的入库候选 |

**用户确认后才卸载**：`python3 scripts/uninstall_skills.py`（默认 dry-run 预览）→ `--confirm` 执行（或 `make cleanup-confirm`）。卸载为归档式（移入各运行时同级 `*-archive/` 目录，与 Codex 自身 skills-archive 惯例一致），不删除任何文件，`mv` 回原路径即可恢复；执行后写入 cleanup-receipts.jsonl 回执。执行器内置双重安全网：近 30 天有调用的技能即使出现在待确认清单中也会被拒绝卸载。

```bash
make recommendations   # 生成建议（周度流水线内含）
make cleanup-preview   # 预览待卸载项
make cleanup-confirm   # 确认执行归档式卸载
```

## 定时执行

由 Qoder 会话定时任务每周六 09:00（Asia/Shanghai）触发，执行
`./scripts/weekly_cycle.sh` 并监督异常（网络失败、审计 FAIL 时人工介入）。
