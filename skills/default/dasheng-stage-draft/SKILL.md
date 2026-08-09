---
name: dasheng-stage-draft
description: Stage 3 Draft - 初稿生成（标准基线稿）
version: 1.0.0
stage: draft
runner: node
---

# Dasheng Stage Draft - 初稿生成

## 功能概述

Stage 3 Draft 是大声自媒体创作工作台的核心写作阶段，负责将编辑确认的选题转化为可审核、可发布的正文底稿。

**核心原则**：
- 默认生成标准正文；按需可在本环节完成轻量润色或渠道源稿整理
- 严格限制顶层结构为3-4个一级标题
- 每个论断必须可追溯到外部来源
- 绝不在文章内容中包含内部统计数据
- 同步生成可编辑、自包含、离线可打开的 HTML 草稿，供微信公众号预览和人工修改

## 输入要求

### 必需输入
- `selected_topics.json` - 编辑确认的选题列表（来自Brief阶段的HITL gate）

### 可选输入
- `topic_cards.json` - 选题卡片详细信息
- `--asset-specs-file` - 可选，按 `topic_id` 提供 `chart_specs` / `image_specs`，用于 Draft 内直接生成图表与配图
- `--chartjs-file` - 可选，本地 Chart.js v4.4.4 UMD 文件；未提供时使用项目 `vendor/chart.umd.min.js`
- `--run-id` - 自定义运行ID（默认自动生成）
- `--output-dir` - 自定义输出目录；默认应位于 `~/Desktop/自媒体创作/05_初稿生成/<run_id>`，不要写入项目根目录

### 金融数据增强输入

`topic_cards.json` 或 `--asset-specs-file` 可添加 `finance_chart_requests`。Draft 会调用 `dasheng-finance-data` / `scripts/finance_data_adapter.py` 拉取 A 股或指数 K 线，并自动生成 `chart_specs`。
该字段也支持全球市场品种（Yahoo Finance Chart API 直连优先，本地缓存 / yfinance 兜底）、中国宏观/地产数据（东方财富数据中心宏观报表）与经济日历（FMP，需 `FMP_API_KEY`），用于宏观、利率、汇率、商品、地产、股债组合等文章。
如果任一金融图表请求失败，`03_DraftAssets_<topic>.json` 与 `draft_manifest.json` 会写入 `asset_failures.finance_charts`，并把 `asset_status` 标记为 `incomplete`。

## 输出产物

### 文档交付视图
- `03_ReasoningSheet_<topic>.md` - 论证结构表（包含论断、证据、缺失证明）
- `03_标准初稿_<topic>.md` - 标准初稿（每个选题一篇）
- `03_HTML草稿_<topic>.html` - 可编辑自包含 HTML 草稿（每个选题一篇）
- `03_初稿_报告.md` - 初稿生成报告

### 正式状态源（Canonical State）
- `draft_manifest.json` - 初稿清单（包含所有初稿元数据）
- `final_structure_snapshot.json` - **MANDATORY GATE** - 最终结构快照（确认后可直接进入发布）
- `draft_quality_gate.json` - 文字洁癖 / 质量门禁汇总

### 结构化数据
- `03_ReasoningSheet_<topic>.json` - 论证结构JSON（供 Draft 资产绑定 claim）
- `03_质量门禁_<topic>.json` - 单篇初稿质量门禁
- `03_DraftAssets_<topic>.json` - Draft 内已嵌入图表与配图规格（`chart_specs` / `image_specs`）
- `03_IllustrationIntents_<topic>.json` - 原文比喻、举例、类比、拟人和抽象机制的柠檬漫画触发与渠道适配意图

## 执行方式

### Node.js API
```javascript
const { runDraft } = require('./skills/dasheng-stage-draft');

const result = runDraft('/path/to/selected_topics.json', {
  runId: '2026-04-14_120000',
  topicCardsFile: '/path/to/topic_cards.json',
  outputDir: '/custom/output/dir'
});

console.log(result);
// {
//   success: true,
//   run_id: '2026-04-14_120000',
//   out_dir: '~/Desktop/自媒体创作/05_初稿生成/2026-04-14_120000',
//   draft_count: 3,
//   draft_files: ['...', '...', '...'],
//   manifest_file: '.../draft_manifest.json',
//   final_structure_snapshot: '.../final_structure_snapshot.json',
//   next_step: 'dasheng-stage-transwrite'
// }
```

### Python 直接调用
```bash
python3 scripts/build_stage3_draft.py \
  /path/to/selected_topics.json \
  /path/to/topic_cards.json \
  --asset-specs-file /path/to/draft_asset_specs.json \
  --run-id 2026-04-14_120000
```

## Gate 验证规则

### Upstream Gate: `selected_topics.json`
- 必须包含非空的 `selected_topics` 数组
- 每个选题必须有 `topic_id`, `title`, `core_proposition`
- 状态必须为 `approved` 或 `confirmed`

### Output Gate: `final_structure_snapshot.json`
- 初始状态为 `pending`（等待编辑确认）
- 编辑修订初稿后，必须在此文件中写入最终保留的一级/二级结构
- 状态改为 `approved` / `locked` / `finalized` 后，可直接进入 Publish

## 质量标准

1. **结构限制**：顶层结构严格限制为3-4个一级标题，绝不超过4个
2. **可追溯性**：每个论断（Claim）必须映射到 `EvidenceItem` / `MissingProof` / `ChartNeed`
3. **无内部统计**：绝不在文章内容中包含intake统计数据、聚类数据或内部流程指标
4. **主稿定位**：这是可发布正文底稿；图表和正文配图必须在 Draft HTML 内闭环，封面/视频/多版本改写才按需调用
5. **文字洁癖**：少用 `不是……而是……`、`这意味着`、`本质上`、`不可否认`、`综上所述` 等 AI 味高频句式；命中项会写入质量门禁

## HTML 草稿铁律

- Draft HTML 是第三环节交付物，不等到 Publish 才生成；Markdown 仍保留为事实源稿。
- 输出必须是单文件自包含 HTML：CSS/JS 内联，离线可用，不允许 CDN 或本地文件引用。
- 有 Chart.js 图表时，必须内联 `Chart.js v4.4.4 UMD`；自写图表脚本必须用 `DOMContentLoaded` 包裹、`typeof Chart` 降级检查、`responsive:false`、显式 canvas 宽高、`deepMerge` 合并配置，log 坐标必须写 `type:'logarithmic'`。
- 表格标签类放在 `<td>` 内部的 `<span>` 上，不放到 `<td>` 本身。
- HTML 根内容区必须 `contenteditable="true"`，并提供编辑/预览切换、全选、保存下载。
- 配图优先使用与正文场景、人物、机构、产业链、城市空间直接相关的图片或主题视觉；不得把文章大纲包装成无信息量的“研究框架图”。图片必须压缩后 base64 嵌入，最长边不超过 1200px，JPEG 75 左右。
- 生成正文后必须调用 `dasheng-lemon-illustrations` 做一次语义扫描。原文出现有认知价值的比喻、举例、类比、拟人或抽象机制时，生成 `illustration_intents`；关键词只负责召回，最终由 Agent 判断是否值得画。
- 公众号正文漫画使用柠檬人，优先单幅 16:9 或 2-3 格微漫画，紧跟触发它的段落，不得统一堆到文末。长文通常保留 4-8 个高价值漫画锚点，不能每段都画。
- 漫画只解释概念和例子，不得替代真实图表、网页、表格、文档、地图或来源证据。未完成必需漫画时，`illustration_status=pending_agent_generation`，Draft 资产状态保持 incomplete。
- 真实图表和配图必须绑定 `claim_id` / 数据来源；数据未核验时不得生成假曲线，`draft_manifest.json` 必须标记 `asset_status: incomplete`。
- 发布到微信公众号前，canvas 图表建议截图替换为静态图，避免编辑器白屏。

## 锚点标注规范

生成初稿时，在需要配图/链接的位置使用以下标注：
- `{{image: 描述内容}}` - 配图占位
- `{{lemon: intent_id|原文比喻或举例|核心意思|柠檬人动作}}` - 柠檬漫画锚点
- `{{chart: claim_id|图表描述|数据来源或待补来源}}` - 图表占位
- `{{link: URL|显示文字}}` - 链接占位
- `{{ref: 来源名称}}` - 参考文献标注

这些锚点只能作为 `chart_requests` / `image_requests` 输入。Draft 结束时必须产出可直接嵌入 HTML 的 `chart_specs` / `image_specs`；不能只交付计划清单。

## 人工迭代循环

Draft阶段支持人工+AI迭代循环：
1. 编辑可人工写初稿、修改AI初稿、或投喂范文让AI生成
2. AI生成后，编辑提出修改意见，AI修改，进入下一轮
3. 编辑使用 `@批改意见示例@` 标注需要修改的内容
4. AI完成修改后，必须删除所有 `@` 锚点标记
5. 循环终止条件：编辑发送"approve"/"通过"、确认"中版/终版"、或明确指示"进入下一环节"

## 相关素材附加

如果 Intake 阶段存在相关主题的文章或视频链接，须附在初稿末尾，供编辑回看和拓展思路。

Draft 阶段如需真实数据、图表或配图，由当前运行 Agent 主动搜索、核验、生成并嵌入 HTML；不得把图表计划留给不存在的下游阶段。
金融行情、指数走势、个股对比、跨资产市场数据、中国宏观/地产、经济日历统计图优先使用 `dasheng-finance-data` 生成 `chart_specs`，避免手写行情或宏观数据。

## 下游阶段

- **Next Stage**: `dasheng-stage-publish`
- **Optional Tools**: rewrite variants（按需调用，不作为主链 gate）

## 技术实现

- **执行器**: `scripts/build_stage3_draft.py`
- **包装器**: `skills/dasheng-stage-draft/index.js`
- **超时限制**: 5分钟
- **输出格式**: JSON to stdout
