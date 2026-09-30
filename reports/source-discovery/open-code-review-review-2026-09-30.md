# Review: alibaba/open-code-review（人工复核队列，未入库）

- URL: https://github.com/alibaba/open-code-review
- Stars: 42789 | License: Apache-2.0 | Last push: 2026-09-29
- 自动评分: 80（verdict `review`）
- 复核日期: 2026-09-30

## 为什么被自动流程挡下

不是因为聚合商店规则（`detect_aggregator` 未命中），而是 monorepo 门槛：`has_root_skill=false` 且 `skill_subdirs=2 < MONOREPO_MIN_SUBDIRS(3)`，`scripts/weekly_curation.py` 把 `import_score` 抬到 101，落入 `review`。该规则本意是挡"产品仓库顺手带的技能目录"，本例正好是产品仓库，但技能本身是仓库的一等公民（`skills/open-code-review`、`skills/open-code-review-delegate`），属规则误伤而非质量不足。

## 实际内容

`skills/open-code-review/SKILL.md` 是 `ocr` CLI 的包装：读取 Git diff，输出行级审查评论，可自动应用修复。声明 `license: Apache-2.0`、`author: alibaba`、`version: 1.0.0`。

依赖：

- `npm install -g @alibaba-group/open-code-review`（或 GitHub release 二进制）
- 首次运行前需配置 LLM provider（Anthropic / OpenAI Chat Completions / OpenAI Responses / AWS Bedrock）

按本仓库访问模式分类属 `api-key` + 外部 CLI，因此**不可能进标准包**（标准包硬过滤第三方 key），只会进目录与分层。

## 质量顾虑

SKILL.md 第 36 行要求 Agent "**Do not pre-check whether `ocr` is installed**"，跳过 `command -v ocr` 探测直接执行，失败后再按 Troubleshooting 安装。这不是恶意内容，但与本仓库"依赖透明"的原则相悖：它把全局 npm 安装变成失败后的隐式动作。若入库，应在 SOURCE.txt 记录该移植修正建议，或改写为先探测再执行。

## 与已收录技能的关系

已有 `code-review`（85 分，来源 `shareAI-lab/learn-claude-code`，教学型仓库的提示词技能，无外部依赖）。两者能力位重叠但实现路径不同：一个是纯提示词，一个是确定性流水线 + LLM 的 CLI。

## 建议

入库，但按下列条件（需用户确认后执行）：

1. 只收 `skills/open-code-review`，`open-code-review-delegate` 待看清职责再定（本次抓取未取到正文）。
2. 注册到 `high` 与 `medium` 双层（保持 medium ⊆ high 单调性，否则 `tests/test_tier_catalog.py` 失败）。
3. `conflict_group` 设为 `code-review`，让组合层按分数仲裁，避免标准包/金融包同时出现两个代码审查技能。
4. `catalog/native-origin-overrides.json` 指向 `https://github.com/alibaba/open-code-review/tree/main/skills/open-code-review`。
5. 访问模式标 `api-key`，确保标准包硬过滤生效。
6. 附带 `reports/source-discovery/open-code-review-review-2026-09-30.md`（本文件）与 SOURCE.txt 移植说明。

同批被 monorepo 门槛挡下的还有 `pascalorg/editor`（24377 星，MIT，2 个子目录，3D 建筑编辑器附带技能）——该例技能是产品的附属物，建议维持不入库。
