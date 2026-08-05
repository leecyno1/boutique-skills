# Finance / Investment Skills Scorecard

Date: 2026-06-14
Updated: 2026-08-05

This report consolidates the existing finance-skill evaluation artifacts in `reports/finance-skill-eval/` with a fresh static review of the repository's finance and investment-related `SKILL.md` files.

## Scope

Included:

- Investment research, market data, stock/ETF/options analysis, macro, portfolio/risk, backtesting, trading plans, monitoring, valuation, equity research, private equity, wealth management, and investment banking workflows.

Excluded from the recommended standard suite, but still noted:

- Fund administration and KYC/operations skills: finance-adjacent but not investment decision workflows.
- Generic spreadsheet/PPT/document authoring skills: useful infrastructure, but not finance-investment skills by themselves.
- General social/media/content skills unless explicitly finance-market oriented.

## Scoring Rubric

10-point score, normalized to 100 in tables:

- Executability: scripts, commands, data contract, clear input/output.
- Investment value: usefulness in real investor workflow.
- Scope clarity: trigger, boundaries, and fallback behavior.
- Non-overlap: whether it contributes a unique function versus nearby skills.
- Maintenance risk: external keys, unstable scraping, model/platform dependencies, stale references.

Score interpretation:

- 90-100: Standard-suite core.
- 80-89: Strong, core or near-core.
- 70-79: Useful, often optional or category-specific.
- 60-69: Keep as backup/template/lab item.
- Below 60: Do not recommend for standard suite without rewrite or dependency fix.

## 2026-08-05 Day1Global Addendum

The five-skill [Day1Global-Skills](https://github.com/star23/Day1Global-Skills) source family was reviewed at snapshot `562c14b0c0bc84abff755181ead30ebea613d063` and added as an installable finance suite. The suite scores **79/100** overall.

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `tech-earnings-deepdive` | 85 | Standard slot | Strong technology-earnings workflow with 16 modules, six investment lenses, primary-source standards, valuation, variant view, pre-mortem, and action triggers. |
| `macro-liquidity` | 82 | Standard slot | Focused Fed net-liquidity, SOFR, MOVE, and yen carry-trade dashboard that complements broader macro and policy tools. |
| `btc-bottom-model` | 78 | Optional | Transparent 13-indicator model, but its convenience API lacks field-level provenance and published calibration evidence; the mirror requires independent verification. |
| `us-market-sentiment` | 76 | Optional | Useful dashboard, but several institutional and prime-broker inputs are delayed, paywalled, or secondary-source only. |
| `us-value-investing` | 72 | Suite-only | Easy four-factor checklist, but too coarse and overlapping to replace the current stock-analysis and valuation stack. |

Detailed review: [GitHub Day1Global-Skills review](../source-discovery/github-day1global-skills-2026-08-05.md).

## Data And Infrastructure

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `tushare-openclaw-skill` | 95 | Core | Best structured China-market data spine; native Tushare coverage for A-shares, funds, futures, bonds, fundamentals, valuation, dividends, unlocks, and macro. Requires `TUSHARE_TOKEN`, acceptable as a finance data key. |
| `a-stock-data` | 88 | Core A-share multi-source layer | Very broad A-share coverage including quotes, research reports, themes, northbound, Dragon-Tiger, unlocks, margin, block trades, holders, dividends, news, announcements. Complements Tushare by covering real-time, theme, capital-flow, announcement, and no-key direct-source workflows. |
| `llmquant-data` | 86 | Institutional-data core if LLMQuant is available | Clean router for SEC filings, 13F holders, macro snapshots, and grounded macro briefs. Strong data contract, but gated by LLMQuant data/MCP availability. |
| `yfinance-data` | 78 | Core lightweight global data | Good no-key US/global fallback for prices, statements, options, dividends, earnings, holders. Yahoo rate limits mean it should not be the only data source. |
| `akshare-stock` | 76 | A-share fallback | Useful AkShare wrapper with scripts, but overlaps heavily with Tushare and `a-stock-data`; weaker guardrails. |
| `stock_datasource` | 72 | Platform adapter | Useful local project adapter for a stock data platform and subskills; better for deployment/plumbing than day-to-day investment analysis. |
| `stock_datasource/skills/stock-mcp-query` | 72 | Data-service support | Clear MCP query path for historical data and statements; recommended only when that local MCP service is part of the stack. |
| `stock_datasource/skills/stock-rt-subscribe` | 70 | Real-time-data support | WebSocket subscription support is valuable for live monitoring, but operationally narrower than standard analysis workflows. |
| `openclaw-stock-data-skill` | 70 | Backup | Has a specific `data.diemeng.chat` API contract; useful if that API is provisioned, otherwise less standard than Tushare. |
| `tushare-plugin-builder` | 68 | Developer/lab | Good for extending the data platform with new Tushare endpoints; not an investor-facing standard skill. |
| `funda-data` | 66 | Institutional backup | Useful where Funda MCP is configured, but mixed MCP/API dependency makes it less portable than `llmquant-data` or `yfinance-data`. |

## Market, Macro, News, And Events

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `policy-monitor` | 88 | Core for China policy-driven markets | Strong direct policy/regulatory monitoring role; fills a gap not covered by price/fundamental data. |
| `llmquant-macro` | 84 | Core if LLMQuant is available | Strong router for macro dashboards, central bank previews, inflation/growth/liquidity, and portfolio impact. |
| `macro-liquidity` | 82 | Core liquidity specialist | Focused no-key framework for Fed net liquidity, SOFR stress, MOVE volatility, and yen carry-trade risk. |
| `llmquant-market-intelligence` | 84 | Core if LLMQuant is available | Clean market sentiment and event-probability routing; good high-level intelligence layer. |
| `llmquant-events` | 84 | Core if LLMQuant is available | Better event abstraction than many single-purpose earnings/event skills. |
| `macro-regime-detector` | 82 | Core/optional | Useful 1-2 year regime framework with scripts and explicit components; data dependencies apply. |
| `market-environment-analysis` | 78 | Optional | Good broad market briefing workflow with no key, but mostly web-search/reporting guidance rather than a strong executable data pipeline. |
| `alphaear-news` | 77 | Optional news layer | Useful finance-news/trend/prediction-market fetcher with scripts; overlaps with LLMQuant market intelligence. |
| `economic-calendar-fetcher` | 76 | Optional | Valuable calendar function but narrower; can be folded under `llmquant-events` in a standard suite. |
| `market-news-analyst` | 66 | Backup | Good analytical framing, but browser/manual dependence reduces standard-suite fit. |
| `finance-sentiment` | 66 | Backup | Useful sentiment layer, but overlaps with AlphaEar/LLMQuant and depends on external data/model choices. |
| `hormuz-strait` | 62 | Event-specific | Good for one geopolitical theme, too narrow for standard suite. |

## Equity Research, Valuation, And Company Analysis

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `stock-analysis` | 84 | Core | Broad stock/crypto analysis, watchlists, alerts, dividend analysis, scoring, and rumor checks. Practical investor workflow coverage. |
| `tech-earnings-deepdive` | 85 | Core for technology earnings | Deep A-P earnings framework with multi-lens confrontation, valuation, evidence hierarchy, anti-bias checks, and action triggers. |
| `openclaw-stock-analyzer` | 83 | Core/optional | Strong value-investing workflow with Buffett/Duan Yongping framing, valuation, staging, earnings reading, and option suggestions; China-friendly and practical. |
| `us-stock-analysis` | 80 | Core for US-heavy users | Good US stock fundamentals, technicals, valuation, comparisons, and report flow; overlaps with `stock-analysis`, but deeper US framing. |
| `company-valuation` | 78 | Optional | Strong DCF/relative/SOTP methodology and assumptions; dependency and model/API references make it less standard than data-backed analysis plus targeted valuation. |
| `llmquant-equities` | 82 | Core if LLMQuant is available | Good router for stock analysis, comparisons, memos, merger-arb memos, and sell/take-profit work. |
| `anthropic-fs-equity-research-initiating-coverage` | 82 | Institutional template | Excellent report workflow and deliverables; big, document-heavy, and less directly executable for daily investing. |
| `anthropic-fs-equity-research-earnings-analysis` | 76 | Optional template | Strong post-earnings report template, but largely process guidance. |
| `anthropic-fs-equity-research-model-update` | 74 | Optional template | Useful model-update workflow; overlaps with valuation and earnings skills. |
| `anthropic-fs-equity-research-earnings-preview` | 73 | Optional template | Good pre-earnings checklist; less executable than `earnings-calendar`/`earnings-trade-analyzer`. |
| `anthropic-fs-equity-research-sector-overview` | 72 | Optional template | Useful sector report frame; overlaps with `sector-analyst` and LLMQuant workflows. |
| `anthropic-fs-equity-research-thesis-tracker` | 70 | Superseded | Conceptually good, but `trader-memory-core` is more operational. |
| `anthropic-fs-equity-research-morning-note` | 70 | Optional template | Good institutional format, but no unique data capability. |
| `anthropic-fs-equity-research-catalyst-calendar` | 69 | Optional template | Useful concept, but can be covered by `llmquant-events` or earnings/event tools. |
| `anthropic-fs-equity-research-idea-generation` | 68 | Backup template | Good screening prompts, but direct screeners are more actionable. |
| `estimate-analysis` | 68 | Optional | Useful estimate-data framing; overlaps with earnings and valuation skills. |
| `earnings-preview` | 67 | Optional | Useful yfinance-based pre-earnings structure; narrower than `llmquant-events` plus `earnings-trade-analyzer`. |
| `earnings-recap` | 67 | Optional | Useful recap workflow, but mostly template plus yfinance. |

## Screening, Technical Analysis, And Trade Planning

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `canslim-screener` | 86 | Core growth screener | Strong executable growth-stock methodology, scripts, and guardrails. |
| `vcp-screener` | 84 | Core technical screener | Clear Minervini VCP use case, scripts, strict mode, and defined outputs. |
| `sepa-strategy` | 84 | Core trade-plan framework | Excellent method layer for trend template, pattern quality, relative strength, and invalidation rules. |
| `finviz-screener` | 82 | Core US screening utility | Very useful natural-language-to-FinViz screening entry point; data access is external but practical. |
| `value-dividend-screener` | 82 | Core income/value screener | Strong dividend/value/quality niche with scripts and risk framing. |
| `breakout-trade-planner` | 78 | Optional | Good execution planning, but overlaps with SEPA/VCP for standard package. |
| `pead-screener` | 77 | Optional event screener | Useful post-earnings drift niche; keep in lab or event module. |
| `earnings-trade-analyzer` | 77 | Optional event screener | Clear 5-factor post-earnings scoring; overlaps with PEAD and event suite. |
| `parabolic-short-trade-planner` | 76 | Optional specialist | Useful short-side plan for parabolic exhaustion; too specialized for default suite. |
| `pair-trade-screener` | 76 | Optional quant specialist | Strong stat-arb workflow, but more advanced and data/API dependent. |
| `dividend-growth-pullback-screener` | 76 | Optional income niche | Good but overlaps with `value-dividend-screener`. |
| `technical-analyst` | 72 | Optional visual-analysis skill | Strong chart-reading framework, but image/model dependency and overlap with SEPA/VCP reduce default fit. |
| `downtrend-duration-analyzer` | 70 | Backup | Useful pattern diagnostic, narrower than standard technical framework. |
| `breadth-chart-analyst` | 70 | Backup | Useful visual breadth reading, overlaps with executable breadth/uptrend tools. |
| `etf-premium` | 68 | Backup | Niche ETF premium/discount workflow. |

## Market Breadth, Regime, And Top/Bottom Risk

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `uptrend-analyzer` | 88 | Core | Live-tested, public CSV source, actionable trend-health score and equity-exposure guidance. |
| `market-breadth-analyzer` | 82 | Optional/core backup | Similar public-data breadth analysis; useful but live test found output-directory rough edge. |
| `market-top-detector` | 80 | Optional | Good top-risk composite, but overlaps with breadth/uptrend and relies on more inputs. |
| `ibd-distribution-day-monitor` | 78 | Optional | Useful O'Neil-style distribution-day logic; category-specific. |
| `ftd-detector` | 78 | Optional | Useful follow-through-day logic; category-specific. |
| `us-market-bubble-detector` | 78 | Optional | Good bubble-risk framework; keep as risk/regime specialist. |
| `market-breadth-analyzer` | 82 | Optional | Keep if you want separate breadth dashboard alongside `uptrend-analyzer`. |
| `market-top-detector` | 80 | Optional | Keep for late-cycle/top-focused workflows. |

## Portfolio, Risk, Monitoring, And Memory

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `position-sizer` | 90 | Core | Live-tested, directly calculates shares, dollar exposure, risk percent, and reports. Low dependency, high practical value. |
| `stock-monitor-skill` | 88 | Core | Live-tested alert system for cost, moving averages, RSI, volume, gaps, trailing profit; practical ongoing monitoring. |
| `trader-memory-core` | 84 | Core | Operational thesis lifecycle, state transitions, sizing, due dates, and postmortems. More useful than prompt-only thesis trackers. |
| `llmquant-risk` | 84 | Core if LLMQuant is available | Strong risk router for fear scoring, VIX regime, hedge design, and research health checks. |
| `llmquant-portfolio` | 84 | Core if LLMQuant is available | Strong router for company profiles, thesis tracking, theme research, watchlist monitoring, alerts. |
| `portfolio-manager` | 74 | Optional | Good Alpaca-MCP portfolio analysis; strong if user uses Alpaca, otherwise gated. |
| `exposure-coach` | 72 | Optional | Useful exposure guidance, but overlaps with risk/portfolio tools and has data dependencies. |
| `stock-correlation` | 78 | Optional/core for quant users | Useful correlation, substitution, pair, and diversification analysis; not as universal as position sizing. |
| `signal-postmortem` | 78 | Optional | Good learning loop for signal outcomes; best when using the edge pipeline. |
| `stock-liquidity` | 74 | Optional | Useful liquidity/spread/slippage diagnostic, narrower than core risk tools. |

## Backtesting And Strategy Research

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `pybroker-backtest-skill` | 90 | Core | Tests passed in prior live evaluation; real backtest engine with strategy examples. Needs dependency install and alternative data when Yahoo is limited. |
| `backtest-expert` | 86 | Core companion | Excellent methodology for robustness, slippage, bias prevention, parameter stability, and deployment decisions. Not redundant with a backtest engine. |
| `data-quality-checker` | 82 | Core/optional | Strong cross-cutting validation for datasets; valuable before backtesting or modeling. |
| `edge-strategy-reviewer` | 78 | Optional lab | Useful strategy review stage, but belongs with the broader edge pipeline. |
| `edge-pipeline-orchestrator` | 76 | Lab | Good multi-stage research pipeline orchestration, too broad/specialized for standard suite. |
| `edge-signal-aggregator` | 76 | Lab | Useful conviction dashboard for multiple upstream edge skills; optional. |
| `edge-candidate-agent` | 72 | Lab | Candidate discovery component; not standalone standard. |
| `edge-hint-extractor` | 70 | Lab | Supporting extraction component. |
| `edge-concept-synthesizer` | 70 | Lab | Supporting synthesis component. |
| `edge-strategy-designer` | 72 | Lab | Strategy-design component; optional. |
| `strategy-pivot-designer` | 70 | Lab | Useful after failed tests, but not core. |
| `trade-hypothesis-ideator` | 70 | Lab | Good idea-generation helper, but needs stronger execution loop. |

## Options, Derivatives, Rates, FX, Credit, Crypto, Commodities

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `llmquant-options` | 84 | Core if LLMQuant is available | Broad IV, Greeks, strategy construction, volatility surface, unusual activity, earnings IV crush, and backtest routing. |
| `options-strategy-advisor` | 80 | Core if no LLMQuant | Executable options pricing/Greeks/P&L simulation; heavier than `options-payoff` but more complete. |
| `options-payoff` | 74 | Lightweight optional | Good direct payoff curves and simple strategies, but narrower than strategy advisor. |
| `llmquant-rates-fx` | 80 | Optional institutional | Good rates/FX router for yield curves, duration, central-bank divergence, FX carry, real rates, dollar analysis. |
| `llmquant-credit` | 78 | Optional institutional | Useful credit workflow category; keep for cross-asset/institutional users. |
| `llmquant-commodities` | 76 | Optional institutional | Good for commodity workflows, not needed for most stock-focused suites. |
| `llmquant-crypto` | 76 | Optional | Useful if crypto is in mandate; otherwise outside standard stock-investing suite. |
| `llmquant-equity-derivatives` | 78 | Optional institutional | Strong specialized category, but overlaps with options for most users. |
| `llmquant-prediction-markets` | 72 | Optional | Useful alternative signal source, not core. |
| `anthropic-fs-lseg-option-vol-analysis` | 70 | Template/vendor-specific | Good if LSEG workflow exists; not standard without LSEG. |
| `anthropic-fs-lseg-macro-rates-monitor` | 70 | Template/vendor-specific | Useful LSEG-style workflow, but data/vendor gated. |
| `anthropic-fs-lseg-swap-curve-strategy` | 70 | Template/vendor-specific | Specialized rates workflow. |
| `anthropic-fs-lseg-fx-carry-trade` | 70 | Template/vendor-specific | Specialized FX workflow. |
| `anthropic-fs-lseg-bond-relative-value` | 70 | Template/vendor-specific | Specialized fixed income workflow. |
| `anthropic-fs-lseg-bond-futures-basis` | 70 | Template/vendor-specific | Specialized fixed income workflow. |
| `anthropic-fs-lseg-fixed-income-portfolio` | 70 | Template/vendor-specific | Specialized fixed income workflow. |

## Private Equity, Wealth, And Investment Banking

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `anthropic-fs-private-equity-ic-memo` | 80 | Optional PE suite | Strong IC memo framing; useful for private-market investors but not public-market core. |
| `anthropic-fs-private-equity-deal-screening` | 78 | Optional PE suite | Useful sourcing/screening workflow. |
| `anthropic-fs-private-equity-dd-checklist` | 78 | Optional PE suite | Good diligence checklist. |
| `anthropic-fs-private-equity-dd-meeting-prep` | 76 | Optional PE suite | Useful meeting prep workflow. |
| `anthropic-fs-private-equity-returns-analysis` | 76 | Optional PE suite | Useful returns framing. |
| `anthropic-fs-private-equity-unit-economics` | 76 | Optional PE suite | Useful operating analysis. |
| `anthropic-fs-private-equity-portfolio-monitoring` | 76 | Optional PE suite | Useful portfolio operations workflow. |
| `anthropic-fs-private-equity-value-creation-plan` | 74 | Optional PE suite | Useful but process-heavy. |
| `anthropic-fs-private-equity-deal-sourcing` | 74 | Optional PE suite | Useful but overlaps with screening. |
| `anthropic-fs-private-equity-ai-readiness` | 66 | Backup | Too thematic/narrow for standard investment suite. |
| `anthropic-fs-wealth-management-portfolio-rebalance` | 78 | Optional wealth suite | Useful for advisor workflows; overlaps with portfolio/risk tools. |
| `anthropic-fs-wealth-management-investment-proposal` | 76 | Optional wealth suite | Good client proposal template. |
| `anthropic-fs-wealth-management-client-review` | 74 | Optional wealth suite | Good client-review template. |
| `anthropic-fs-wealth-management-client-report` | 74 | Optional wealth suite | Good reporting template. |
| `anthropic-fs-wealth-management-financial-plan` | 72 | Optional wealth suite | Broader planning than investment skill. |
| `anthropic-fs-wealth-management-tax-loss-harvesting` | 72 | Optional wealth suite | Useful but jurisdiction/account-specific. |
| `anthropic-fs-investment-banking-merger-model` | 78 | Optional IB suite | Useful M&A modeling workflow. |
| `anthropic-fs-investment-banking-datapack-builder` | 78 | Optional IB suite | Strong data-pack structure; more banker workflow than investor workflow. |
| `anthropic-fs-investment-banking-cim-builder` | 74 | Optional IB suite | Good sell-side document workflow. |
| `anthropic-fs-investment-banking-buyer-list` | 74 | Optional IB suite | Useful buyer universe workflow. |
| `anthropic-fs-investment-banking-pitch-deck` | 72 | Optional IB suite | Presentation workflow, not investment-decision core. |
| `anthropic-fs-investment-banking-teaser` | 72 | Optional IB suite | Narrow document workflow. |
| `anthropic-fs-investment-banking-strip-profile` | 72 | Optional IB suite | Narrow document workflow. |
| `anthropic-fs-investment-banking-process-letter` | 70 | Optional IB suite | Narrow process-document workflow. |
| `anthropic-fs-investment-banking-deal-tracker` | 70 | Optional IB suite | Useful tracker, but not core investment analysis. |

## Financial Modeling And Presentation Templates

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `anthropic-fs-financial-analysis-dcf-model` | 84 | Optional modeling core | Very detailed DCF builder with scripts and constraints; strong if Excel/model deliverables are needed. |
| `anthropic-fs-financial-analysis-comps-analysis` | 80 | Optional modeling core | Detailed comps methodology; strong but document-heavy. |
| `anthropic-fs-financial-analysis-3-statement-model` | 78 | Optional modeling core | Useful template-completion workflow; not a standard investor skill unless model building is a primary use case. |
| `anthropic-fs-financial-analysis-lbo-model` | 76 | Optional PE/IB modeling | Good LBO model guidance; specialist. |
| `anthropic-fs-financial-analysis-competitive-analysis` | 74 | Optional research template | Useful competitive landscape deck flow. |
| `anthropic-fs-financial-analysis-audit-xls` | 74 | Infrastructure | Useful model audit workflow; generic spreadsheet validation rather than investment insight. |
| `anthropic-fs-financial-analysis-clean-data-xls` | 70 | Infrastructure | Useful cleanup workflow; not investment-specific. |
| `anthropic-fs-financial-analysis-deck-refresh` | 70 | Infrastructure | Useful presentation-refresh workflow. |
| `anthropic-fs-financial-analysis-ib-check-deck` | 70 | Infrastructure | Useful deck QA. |
| `anthropic-fs-financial-analysis-xlsx-author` | 66 | Infrastructure | Generic workbook authoring. |
| `anthropic-fs-financial-analysis-pptx-author` | 66 | Infrastructure | Generic deck authoring. |
| `anthropic-fs-financial-analysis-ppt-template-creator` | 62 | Developer template | Skill creation around PPT templates, not investment. |
| `anthropic-fs-financial-analysis-skill-creator` | 60 | Developer template | Generic skill creation, not investment. |

## AlphaEar And Signal Lab

| Skill | Score | Verdict | Reason |
|---|---:|---|---|
| `alphaear-reporter` | 82 | Optional report layer | Good report planning/writing/chart configuration role; complements data tools, but not a data source. |
| `alphaear-news` | 77 | Optional news layer | See market/news section. |
| `alphaear-deepear-lite` | 74 | Optional signal feed | Useful if DeepEar Lite endpoint is live; narrow signal-source role. |
| `alphaear-signal-tracker` | 72 | Optional signal lifecycle | Good concept, but says it is currently a pattern extracted from FinAgent; `trader-memory-core` is more mature. |
| `alphaear-stock` | 70 | Backup data source | Basic ticker/search/history wrapper; overlaps with Tushare/yfinance. |
| `alphaear-search` | 70 | Backup search | Finance web/local RAG search; overlaps with general web search and LLMQuant data. |
| `alphaear-sentiment` | 68 | Backup sentiment | Useful FinBERT/LLM sentiment wrapper; dependency and overlap concerns. |
| `alphaear-predictor` | 66 | Lab | Kronos forecasting is interesting but model-risk heavy; do not use as standard advice engine. |
| `alphaear-logic-visualizer` | 64 | Utility | Useful for diagrams, not an investment analysis core. |

## Standard Non-Overlapping Recommended Suite

This is the recommended default set for an investor who wants broad coverage without duplicate skills. It assumes finance data keys such as Tushare/FMP/LLMQuant are acceptable when available, but avoids relying on model/platform keys as mandatory dependencies.

| Slot | Recommended Skill | Score | Why This One | Duplicates / Alternatives Not In Default |
|---|---|---:|---|---|
| A-share structured data | `tushare-openclaw-skill` | 95 | Most standard China-market data spine. | `akshare-stock`, `openclaw-stock-data-skill` as optional fallbacks. |
| A-share full-stack quotes/themes | `a-stock-data` | 88 | Best multi-source A-share layer for real-time quotes, research reports, themes, northbound flow, Dragon-Tiger, unlocks, margin, block trades, holder counts, dividends, news, and announcements. | `akshare-stock` as a broader fallback wrapper. |
| Global lightweight data | `yfinance-data` | 78 | Lowest-friction US/global price and fundamentals fallback. | `funda-data` if configured; `llmquant-data` for institutional package. |
| SEC/13F/macro data | `llmquant-data` | 86 | Source-grounded filings, holders, and macro primitives. | Skip if LLMQuant unavailable. |
| Stock analysis | `stock-analysis` | 84 | Broad practical single-stock and watchlist workflow. | `us-stock-analysis` for US-only deep workflows; `openclaw-stock-analyzer` for value-investing variant. |
| Technology earnings deep dive | `tech-earnings-deepdive` | 85 | Adds technology-specific earnings dissection, valuation, variant view, and kill-condition monitoring beyond the general stock workflow. | Anthropic earnings analysis and `earnings-recap` remain optional format alternatives. |
| Valuation/modeling | `anthropic-fs-financial-analysis-dcf-model` | 84 | Best dedicated DCF/model deliverable skill. | `company-valuation` for lighter valuation; comps/3-statement as optional modeling add-ons. |
| Growth screening | `canslim-screener` | 86 | Best growth-stock screener. | `finviz-screener` as general filter utility, not duplicate if both are desired. |
| Technical setup | `vcp-screener` | 84 | Best executable VCP scanner. | `sepa-strategy` for manual trade-plan framework. |
| Trade-plan framework | `sepa-strategy` | 84 | Clear trend-template/invalidation methodology. | `breakout-trade-planner`, `technical-analyst` as optional. |
| Dividend/value screening | `value-dividend-screener` | 82 | Best income/value screener. | `dividend-growth-pullback-screener`, Kanchi skills as optional. |
| Market regime/breadth | `uptrend-analyzer` | 88 | Live-tested and directly actionable. | `market-breadth-analyzer`, `market-top-detector`, `ftd-detector`. |
| Macro/policy | `policy-monitor` + `llmquant-macro` | 88 / 84 | Policy and macro transmission are distinct; keep both if macro matters. | `market-environment-analysis`, `macro-regime-detector` optional. |
| Macro liquidity | `macro-liquidity` | 82 | Narrow, directly scannable liquidity dashboard for Fed balance-sheet plumbing, SOFR, MOVE, and yen carry risk. | Keep `llmquant-macro` for broader macro research. |
| Events/news | `llmquant-events` | 84 | Broad event router avoids many single-purpose earnings skills. | `alphaear-news`, `economic-calendar-fetcher`, `earnings-calendar`. |
| Options | `options-strategy-advisor` | 80 | Best standalone options pricing/Greeks/P&L tool. | Use `llmquant-options` instead if LLMQuant stack is available. |
| Position sizing | `position-sizer` | 90 | Directly reduces execution risk; live-tested. | `exposure-coach`, `portfolio-manager`. |
| Portfolio/risk | `llmquant-risk` + `llmquant-portfolio` | 84 / 84 | Risk and portfolio workflow routers are complementary. | `portfolio-manager` if Alpaca is the real account source. |
| Monitoring | `stock-monitor-skill` | 88 | Live-tested alerting and ongoing watchlist monitoring. | `llmquant-portfolio` alerts if LLMQuant is the main stack. |
| Thesis memory | `trader-memory-core` | 84 | Operational thesis lifecycle and postmortem memory. | `anthropic-fs-equity-research-thesis-tracker`. |
| Backtest engine | `pybroker-backtest-skill` | 90 | Best executable backtest engine. | `pair-trade-screener` and event screeners stay optional. |
| Backtest review | `backtest-expert` | 86 | Methodology gate for robustness, bias, and slippage. | Not a duplicate of the engine. |
| Data quality | `data-quality-checker` | 82 | Prevents bad data from polluting screens/backtests. | `anthropic-fs-financial-analysis-audit-xls` for spreadsheet-specific audits. |
| Research/reporting | `alphaear-reporter` | 82 | Compact report assembly layer for finance outputs. | Anthropic FS report templates as optional institutional formats. |
| Knowledge base | `openclaw-stock-kb` | 78 | Local research-method knowledge base. | `llmquant-investor-lenses` if LLMQuant is configured. |

Recommended default size: 22-24 skills, depending on whether LLMQuant is available.

Minimal no-LLMQuant standard set:

`tushare-openclaw-skill`, `a-stock-data`, `yfinance-data`, `stock-analysis`, `tech-earnings-deepdive`, `anthropic-fs-financial-analysis-dcf-model`, `canslim-screener`, `vcp-screener`, `sepa-strategy`, `value-dividend-screener`, `uptrend-analyzer`, `policy-monitor`, `macro-liquidity`, `options-strategy-advisor`, `position-sizer`, `stock-monitor-skill`, `trader-memory-core`, `pybroker-backtest-skill`, `backtest-expert`, `data-quality-checker`, `alphaear-reporter`, `openclaw-stock-kb`.

Institutional enhanced add-ons:

`llmquant-data`, `llmquant-macro`, `llmquant-events`, `llmquant-market-intelligence`, `llmquant-risk`, `llmquant-portfolio`, `llmquant-options`, `llmquant-etfs`, `llmquant-rates-fx`, `llmquant-credit`.

A-share enhanced add-ons:

`akshare-stock`, `stock_datasource/skills/stock-mcp-query`, `stock_datasource/skills/stock-rt-subscribe`.

Quant/trading lab add-ons:

`pair-trade-screener`, `pead-screener`, `earnings-trade-analyzer`, `parabolic-short-trade-planner`, `market-top-detector`, `ibd-distribution-day-monitor`, `ftd-detector`, `edge-pipeline-orchestrator`, `edge-signal-aggregator`, `signal-postmortem`.

PE/IB/wealth add-ons:

Use Anthropic FS private-equity, investment-banking, and wealth-management skills as separate professional-service bundles rather than mixing them into the public-market investing standard suite.
