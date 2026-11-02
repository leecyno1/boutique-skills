# 新模型 / 新 harness 下的 skills 过时分析（2026-11-02）

样本：本机 `~/.qoder/skills` + `~/.codex/skills` 共 532 份安装副本，去重 353 个 skill。
数据：`/tmp/skill_inventory.json`（字段 code=脚本数、cli/endpoint/key=是否含私有 CLI/数据端点/凭证约定、calls=近 30 天引用次数、repo=是否在精品店仓库）。

## 判定标准

一个 skill 值不值得留，只看一条：**它里面有没有模型自己不知道、harness 也没提供的东西。**

- 有 → 留：私有 CLI 用法（lark-cli、zsxq-cli、agent-reach）、真实数据端点与限流（a-stock-data、global-stock-data）、凭证约定、你自己的流程规范（dasheng-*、墨丘利写作规范）、可直接跑的脚本（screener、detector 的 .py）。
- 没有 → 删：只剩通用方法论（"先写测试再写代码"）、人设（"用巴菲特视角"）、教模型做它本来就会的事（写 IC memo、做 DCF）、或被 harness 内置工具替代（browser-use、ImageGen、context7、office 插件、openchatcut）。

被替代的 harness 能力清单（本机 Qoder 已内置）：计划/子代理/并行 Agent、TODO 任务流、WebSearch/WebFetch、browser-use MCP、context7 文档查询、github MCP、node-repl、ImageGen/VideoGen、office-excel 与 Presentations 插件、openchatcut 视频剪辑 MCP、qoder-canvas。

## 第一层：直接删除（约 110 个）

### A1 流程 / 元技能（47 个）—— harness 已原生具备

superpowers 一族：brainstorming、writing-plans、executing-plans、planning-with-files、test-driven-development、systematic-debugging、verification-before-completion、receiving-code-review、dispatching-parallel-agents、subagent-driven-development、using-superpowers、create-plan、jiebang、proactive-agent。
造 skill 一族（5 份重复）：skill-creator、writing-skills、skill-designer、skill-integration-tester、dual-axis-skill-reviewer、skill-idea-miner、finance-skill-creator、anthropic-fs-financial-analysis-skill-creator、mcp-builder。
codex 侧 ecc 一族：context-budget、search-first、triage、documentation-lookup（context7 替代）、code-tour、codebase-onboarding、coding-standards、error-handling、api-design、backend-patterns、frontend-patterns、e2e-testing、security-review、production-audit、verification-loop、tdd-workflow、ai-regression-testing、eval-harness、to-prd、improve-codebase-architecture、playwright/webapp-testing（browser-use 替代）、codex-responses-tooling、ecc-codex-ops。

注意：codex 侧 tdd-workflow(991)、e2e-testing(972)、security-review(667)、frontend-patterns(534)、search-first(485) 引用量很高。内容是通用的，但 codex 确实在频繁加载，删掉会改变它的行为。建议先归档观察一周再决定。

### A2 人设（4 个）

buffett-perspective、stanley-druckenmiller-investment、huashu-nuwa、llmquant-investor-lenses。新模型对这些人物的思想掌握比 skill 里写的全。

### A3 纯知识 / 纯方法论（23 个）

设计：animation-vocabulary、apple-design、emil-design-eng、ui-designer、canvas-design、find-animation-opportunities、improve-animations、animated-financial-display（frontend-design 一个够用）。
写作研究：internal-comms、citation-verification、experimental-design、content-research-writer、idea-evaluator、startup-analysis。
金融方法论：backtest-expert、sepa-strategy、kanchi-dividend-sop/us-tax-accounting/review-monitor、market-news-analyst、scenario-analyzer、technical-analyst、saas-valuation-compression。

### A4 薄封装（6 个）

yfinance-data、akshare-stock、tushare-openclaw-skill（finance-data-router 已覆盖路由）、multi-search-engine、deep-research、weather。模型知道这些库怎么用。

### A5 anthropic-fs 全家桶（60 个纯 prompt，54 个零调用）

equity-research ×9、financial-analysis ×10、fund-admin ×6、investment-banking ×9、lseg ×8、operations ×2、private-equity ×10、spglobal ×3、wealth-management ×3。
全是"写 IC memo / 做 comps / 写 morning note"的工作流 prompt，无脚本无端点；lseg/spglobal 系还依赖本机没有的 MCP。只有 3 个带代码可保留：financial-analysis-dcf-model、ib-check-deck（skill-creator 已在 A1）。
例外：equity-research-sector-overview（36 次）、catalyst-calendar（10 次）有人在用，可先留。

### A6 llmquant 路由壳（18 个）

全部 code=0，只是把问题转发给 LLMQuant 平台的描述文本；平台本身不在本机。合计调用 22 次。整体删除。

## 第二层：同能力多份，合并到一个（约 50 个可删）

| 能力 | 现有 | 保留 | 删除 |
|---|---|---|---|
| PPT | 8 | pptx（16 脚本）；Qoder Presentations 插件为主 | general-ppt、pptx-generator、qoderwork-ppt、baoyu-slide-deck、anthropic-fs-*pptx-author、*ppt-template-creator |
| Excel | 5 | xlsx；Qoder office-excel 插件为主 | minimax-xlsx、anthropic-fs-*xlsx-author、*clean-data-xls、*audit-xls |
| PDF | 3 | pdf | nano-pdf |
| 网页读取 | 8 | agent-reach（74 次，私有 CLI）、baoyu-url-to-markdown（41 脚本，CDP） | lead-research-assistant、yc-reader、deep-research、multi-search-engine、alphaear-search |
| 生图 | 13 | baoyu-image-gen（34 脚本，多 API）；ImageGen 工具为主 | baoyu-imagine、codex-image-bridge、baoyu-infographic、image-enhancer、drafter-diagram；cover-image/article-illustrator 是 prompt 配方可留 |
| 公众号 | 9 | baoyu-post-to-wechat（44 脚本，wechat-api.ts）、baoyu-markdown-to-html（wechat-multi-publisher 只在仓库，本机未装） | wechat-public-cli、md2wechat、html-article-generator、wechat-draft-writer、wechat-style-profiler |
| 视频 | 10 | remotion-best-practices、media-downloader；openchatcut MCP 为主 | video-rough-cut、video-frames、video-use、cut/finish-talking-head、freecut、vox-director、reusable-footage-material、remotion-video-skill（与 remotion-best-practices 重复） |
| 个股分析 | 8 | stock-analysis（7 脚本）、stock-daily-analysis-skill（9 脚本） | us-stock-analysis、alphaear-stock、llmquant-equities、company-valuation、anthropic-fs-lseg-equity-research、*initiating-coverage |
| 财报 | 8 | earnings-trade-analyzer（13 脚本）、earnings-calendar（5 脚本） | earnings-preview、earnings-recap、estimate-analysis、anthropic-fs-*earnings-* ×3 |
| alphaear | 9 | reporter、predictor、signal-tracker（各 30+ 脚本） | search、sentiment、deepear-lite、stock、news、logic-visualizer |

## 第三层：保留（约 190 个）

- **私有 CLI / 平台约定**：lark-* ×26（lark-cli 子命令与 shortcuts）、zsxq、coze-agent-collaboration、agent-reach、wechat-public-cli 之外的 baoyu-post-to-wechat、iosdev-cn（216 次）。
- **真实数据端点与限流**：a-stock-data（358 次）、global-stock-data（74 次）、finance-data-router（418 次）、policy-monitor、hormuz-strait、finance-sentiment、economic-calendar-fetcher。
- **带可执行脚本的量化工具**：screener ×7（vcp/canslim/pead/value-dividend/dividend-growth-pullback/finviz/pair-trade）、market-regime ×13（market-top-detector 34 脚本、theme-detector 31、macro-regime-detector 25……）、edge-pipeline ×11、alphaear 三件、backtest 相关的 pybroker-backtest-skill、data-quality-checker（60 次）。
  这批几乎都是零调用但有代码、有 API key 约定。它们过时的原因不是模型变强，而是你没在用；是否删属于使用习惯问题，不属于本次"被模型覆盖"的范畴。
- **你自己的流程**：dasheng-* ×9（dasheng-vox-skills 76 次）、agent-introspection-debugging（50 次）、skill-scout（33 次）。
- **带大量脚本的文档工具**：pptx、xlsx、docx、pdf、baoyu-markdown-to-html（30 脚本）、baoyu-url-to-markdown（41 脚本）。
- **frontend-design**（744 次，引用最高，留）。

## 执行建议

1. 第一层先动 A1 非 codex 部分 + A2 + A3 + A4 + A5 + A6，约 85 个，全部零或低调用，风险最低。
2. codex 侧 ecc 一族（tdd-workflow 等 20 多个）归档后观察一周，看 codex 输出质量是否下降，再定。
3. 第二层按表合并，每组保留带脚本的那份。
4. 第三层的零调用量化脚本不动；若要瘦身，另按"半年未用"标准单独处理。

执行方式不变：本机走 `scripts/uninstall_skills.py --confirm`（归档到 `*-archive/`，可 `mv` 恢复），仓库内条目走 `scripts/weekly_curation.py prune`，并同步 `catalog/standard-bundle-overrides.json` 的 excluded 列表，避免周六 Quest 把它们再装回来。
