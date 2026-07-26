---
name: dasheng-stage-brief-ai
description: AI-driven topic generation for Dasheng workflow. Analyzes intake data to generate insightful, valuable, and actionable topic proposals with natural language titles and clear arguments.
---

# Dasheng Stage: Brief (AI-Driven)

## 目标

使用 AI 推理能力从 intake 数据中生成有洞察力、有价值、可执行的选题，替代硬编码规则系统。

## 默认路径

- `DASHENG_WORKSPACE=${DASHENG_WORKSPACE:-/Volumes/PSSD/Projects/公众号文章}`
- 输入：`产物/01_内容采集/{run_id}/`
- 输出：`产物/02_Brief/{run_id}/`

## 核心改进

### 与旧系统的对比

**旧系统 (phase2_rebuilder.py)**：
- ❌ 硬编码 7 个固定模板
- ❌ 字符串拼接生成标题
- ❌ 关键词匹配分类
- ❌ 没有理解事件因果关系
- ❌ 标题生硬、逻辑不清

**新系统 (dasheng-stage-brief-ai)**：
- ✅ AI 理解事件内容和因果关系
- ✅ AI 推理为什么值得写
- ✅ AI 生成自然语言标题
- ✅ 集成 7 种写作框架
- ✅ 集成 4 种内容增强策略
- ✅ 提供完整的论证和证据需求

## 工作流程

### 步骤 1：加载输入数据

从 intake 环节读取：
- `brief_input.json`：编辑向的聚合数据
- `event_clusters.json`：事件聚类结果
- `channel_top10.json`：各渠道热门内容
- `raw/intake_records.json`：原始采集数据（可选）

### 步骤 2：AI 分析

**任务**：
1. 理解每个事件簇的核心内容
2. 识别事件之间的关联和因果关系
3. 判断哪些话题值得深入写作
4. 为每个值得写的话题生成选题

**参考文档**：
- `references/topic-evaluation.md`：选题评估框架
- `references/ai-generation-guide.md`：AI 生成指南
- `references/frameworks.md`：7 种写作框架
- `references/content-enhance.md`：4 种内容增强策略

**AI 提示词要点**：
```
你是资深财经媒体选题编辑。

【核心原则】
1. 理解事件，不要套模板
2. 提供洞察，不要复述事实
3. 创造价值，不要追逐热闹
4. 自然表达，不要生硬拼接

【输入数据】
- 事件簇：{event_clusters}
- 热点排名：{channel_top10}
- 时间范围：{date_range}

【你的任务】
为每个值得写的话题生成一个选题，包含：
1. 标题（自然、流畅，15-30字）
2. 核心论点（一句话）
3. 为什么值得写（2-3句）
4. 目标读者
5. 证据需求和来源
6. 推荐的写作框架
7. 推荐的内容增强策略
8. 5 维评分

【质量标准】
- 标题要自然，不要像模板拼接
- 论点要清晰，有明确立场
- 角度要独特，不重复主流观点
- 证据要充分，可以获得
- 价值要明确，对读者有用
```

### 步骤 3：生成选题

AI 为每个话题生成完整的选题卡片：

```json
{
  "topic_id": "topic-{slug}",
  "title": "中东冲突如何改变全球能源供给秩序",
  "core_argument": "中东冲突正在从短期价格冲击转变为长期供给秩序重构",
  "why_now": "当前市场关注的是油价短期波动，但更重要的是霍尔木兹海峡封锁对全球能源供给秩序的长期影响...",
  "target_audience": "宏观投资者、商品交易员、能源行业从业者",
  "evidence_needs": [
    "霍尔木兹海峡的历史通行量数据和当前封锁情况",
    "全球主要能源进口国的供应链依赖度",
    "替代航线的成本和可行性分析"
  ],
  "evidence_sources": [
    "官方：国际能源署(IEA)、美国能源信息署(EIA)",
    "行业：航运数据平台、能源咨询公司报告"
  ],
  "recommended_framework": "结构型",
  "framework_reason": "需要拆解复杂的供应链结构，帮助读者理解传导机制",
  "recommended_strategy": "密度强化",
  "strategy_application": "提供具体数据、拆解传导链路、给出可操作框架",
  "scores": {
    "timeliness": 9.0,
    "unique_angle": 8.5,
    "evidence": 8.0,
    "reader_value": 9.0,
    "longevity": 8.5,
    "composite": 8.6
  },
  "generation_method": "ai",
  "source_status": "AI生成"
}
```

### 步骤 4：评分和排序

按综合评分排序，推荐 Top 8-10 个选题。

**评分公式**：
```
综合分 = 时效性 × 0.2 + 独特角度 × 0.25 + 证据充分性 × 0.2 + 读者价值 × 0.2 + 持久性 × 0.15
```

### 步骤 5：生成输出文件

生成与旧系统兼容的输出文件：

1. **brief_manifest.json**：阶段清单
2. **selected_topics.json**：待编辑审核的选题
3. **02_编辑Brief库.md**：人类可读的选题库
4. **02_编辑Brief_报告.md**：简要报告
5. **topic_cards.json**：完整的选题卡片数据

## 输出格式

### selected_topics.json

```json
{
  "run_id": "2026-04-04_204231",
  "gate": "Brief Gate",
  "status": "pending_editor_review",
  "generation_method": "ai",
  "instructions": [
    "从 candidate_topics 中选择进入 draft 的题目。",
    "未被选中的题请写入 rejected_topic_ids。",
    "只有 selected_topics 非空且状态为 approved，draft 才允许执行。"
  ],
  "selected_topics": [],
  "rejected_topic_ids": [],
  "candidate_topics": [
    {
      "topic_id": "topic-middle-east-energy-supply-order",
      "title": "中东冲突如何改变全球能源供给秩序",
      "core_argument": "中东冲突正在从短期价格冲击转变为长期供给秩序重构",
      "why_now": "...",
      "target_audience": "宏观投资者、商品交易员、能源行业从业者",
      "evidence_needs": [...],
      "evidence_sources": [...],
      "recommended_framework": "结构型",
      "recommended_strategy": "密度强化",
      "scores": {...},
      "generation_method": "ai",
      "source_status": "AI生成",
      "composite_score": 8.6
    }
  ]
}
```

### 02_编辑Brief库.md

```markdown
# 第二环节 编辑 Brief 库（AI 生成）

运行批次：`2026-04-04_204231`
生成方式：`AI 推理`
输入来源：`/Volumes/PSSD/Projects/公众号文章/产物/01_内容采集/2026-04-04_204231/`

## 本轮原则

- 使用 AI 理解事件内容和因果关系
- 生成自然语言标题，不使用固定模板
- 为每个选题提供完整的论证和证据需求
- 集成 7 种写作框架和 4 种内容增强策略

## 候选选题（8 题）

### 题目 1
- 选题名：`中东冲突如何改变全球能源供给秩序`
- 核心论点：中东冲突正在从短期价格冲击转变为长期供给秩序重构
- 为什么值得写：当前市场关注的是油价短期波动，但更重要的是霍尔木兹海峡封锁对全球能源供给秩序的长期影响。这不仅影响油价，还会重塑航运、库存、定价机制等整个供应链。这个结构性变化被短期情绪掩盖了，但对投资者和企业的长期决策至关重要。
- 目标读者：宏观投资者、商品交易员、能源行业从业者
- 推荐框架：结构型
- 推荐策略：密度强化
- 评分：时效性 9.0 / 独特角度 8.5 / 证据 8.0 / 读者价值 9.0 / 持久性 8.5 / 综合 8.6
- 证据需求：
  - 霍尔木兹海峡的历史通行量数据和当前封锁情况
  - 全球主要能源进口国的供应链依赖度
  - 替代航线的成本和可行性分析
  - 历史上类似事件对供给秩序的长期影响
- 证据来源：
  - 官方：国际能源署(IEA)、美国能源信息署(EIA)
  - 行业：航运数据平台、能源咨询公司报告
  - 媒体：Bloomberg、Reuters、FT 的深度报道
```

## 与旧系统的兼容性

### 保持兼容
- ✅ 输入文件格式不变
- ✅ 输出文件格式兼容
- ✅ Brief Gate 机制不变
- ✅ 可以与 draft 环节无缝对接

### 新增字段
- `generation_method`: "ai" 或 "rule"
- `core_argument`: 核心论点
- `why_now`: 为什么值得写
- `target_audience`: 目标读者
- `evidence_needs`: 证据需求
- `evidence_sources`: 证据来源
- `recommended_framework`: 推荐框架
- `framework_reason`: 框架理由
- `recommended_strategy`: 推荐策略
- `strategy_application`: 策略应用方式
- `scores`: 详细评分

## 使用方式

### 方式 1：直接使用（推荐）

通过 OpenClaw/Claude Code 调用：
```
使用 dasheng-stage-brief-ai 从最新的 intake 数据生成选题
```

### 方式 2：Python 脚本（待实现）

```bash
cd "${DASHENG_WORKSPACE}"
python3 scripts/brief_ai_generator.py \
  --intake-dir "产物/01_内容采集/2026-04-04_204231" \
  --output-dir "产物/02_Brief/2026-04-04_204231" \
  --candidate-count 10
```

### 方式 3：对比测试

同时运行新旧系统，对比效果：
```bash
# 旧系统
python3 scripts/phase2_rebuilder.py \
  "产物/01_内容采集/2026-04-04_204231/raw/intake_records.json" \
  "产物/02_Brief/2026-04-04_204231_rule"

# 新系统（通过 skill）
# 使用 dasheng-stage-brief-ai 生成选题到 产物/02_Brief/2026-04-04_204231_ai

# 对比
diff 产物/02_Brief/2026-04-04_204231_rule/02_编辑Brief库.md \
     产物/02_Brief/2026-04-04_204231_ai/02_编辑Brief库.md
```

## 质量保证

### 自动检查
- 标题长度：15-30 字
- 核心论点：必须有明确立场
- 证据需求：至少 3 条
- 评分：每项 0-10 分

### 人工审核
- Brief Gate：编辑审核和选择
- 可以修改标题、论点、证据需求
- 可以要求 AI 重新生成

## 参考文档

- 选题评估框架：`references/topic-evaluation.md`
- AI 生成指南：`references/ai-generation-guide.md`
- 写作框架：`../dasheng-stage-rewrite/references/frameworks.md`
- 内容增强策略：`../dasheng-stage-rewrite/references/content-enhance.md`

## 下一阶段

- 输出：`selected_topics.json`（状态为 approved）
- 下游：`dasheng-stage-intake-brief-draft` 的 draft 环节
