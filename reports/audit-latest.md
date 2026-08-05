# Boutique Skills Audit

- Time: 2026-08-05 22:07:11
- Status: **WARN**
- Catalog skills: 354
- Audited skills: 348
- Legacy catalog skills: 42
- Installed/Resolved: 348
- Missing: 0
- Missing env vars: 74
- Duplicate capabilities: 0
- Risk hits: 11
- Missing native origins: 0
- Standard bundle issues: 0

## Missing Skills
- None

## Missing Environment Variables
- claude-mem-plugin: `ANTHROPIC_API_KEY`
- claude-mem-plugin: `GEMINI_API_KEY`
- claude-mem-plugin: `OPENROUTER_API_KEY`
- agentmail-mcp: `AGENTMAIL_API_KEY`
- funda-data: `FUNDA_API_KEY`
- llmquant-commodities: `LLMQUANT_API_KEY`
- llmquant-credit: `LLMQUANT_API_KEY`
- llmquant-crypto: `LLMQUANT_API_KEY`
- llmquant-data: `LLMQUANT_API_KEY`
- llmquant-equities: `LLMQUANT_API_KEY`
- llmquant-equity-derivatives: `LLMQUANT_API_KEY`
- llmquant-etfs: `LLMQUANT_API_KEY`
- llmquant-events: `LLMQUANT_API_KEY`
- llmquant-investor-lenses: `LLMQUANT_API_KEY`
- llmquant-macro: `LLMQUANT_API_KEY`
- llmquant-market-intelligence: `LLMQUANT_API_KEY`
- llmquant-options: `LLMQUANT_API_KEY`
- llmquant-portfolio: `LLMQUANT_API_KEY`
- llmquant-portfolio-lab: `LLMQUANT_API_KEY`
- llmquant-prediction-markets: `LLMQUANT_API_KEY`
- llmquant-rates-fx: `LLMQUANT_API_KEY`
- llmquant-risk: `LLMQUANT_API_KEY`
- llmquant-strategies: `LLMQUANT_API_KEY`
- agentmail-toolkit: `AGENTMAIL_API_KEY`
- baoyu-image-gen: `ARK_API_KEY`
- baoyu-image-gen: `AZURE_OPENAI_API_KEY`
- baoyu-image-gen: `BIGMODEL_API_KEY`
- baoyu-image-gen: `DASHSCOPE_API_KEY`
- baoyu-image-gen: `GOOGLE_API_KEY`
- baoyu-image-gen: `OPENROUTER_API_KEY`
- baoyu-image-gen: `REPLICATE_API_TOKEN`
- baoyu-image-gen: `ZAI_API_KEY`
- lark-calendar: `FEISHU_APP_SECRET`
- openclaw-stock-data-skill: `STOCK_API_KEY`
- paperless-docs: `PAPERLESS_TOKEN`
- paperless-ngx-tools: `PAPERLESS_TOKEN`
- agentmail-cli: `AGENTMAIL_API_KEY`
- baoyu-post-to-wechat: `ACCESS_TOKEN`
- baoyu-post-to-wechat: `WECHAT_AI_TOOLS_APP_SECRET`
- baoyu-post-to-wechat: `WECHAT_APP_SECRET`
- baoyu-post-to-wechat: `WECHAT_BAOYU_APP_SECRET`
- canslim-screener: `FMP_API_KEY`
- dividend-growth-pullback-screener: `FINVIZ_API_KEY`
- dividend-growth-pullback-screener: `FMP_API_KEY`
- downtrend-duration-analyzer: `FMP_API_KEY`
- earnings-calendar: `FMP_API_KEY`
- earnings-trade-analyzer: `FMP_API_KEY`
- economic-calendar-fetcher: `FMP_API_KEY`
- exposure-coach: `FMP_API_KEY`
- finance-sentiment: `ADANOS_API_KEY`
- finviz-screener: `FINVIZ_API_KEY`
- ftd-detector: `FMP_API_KEY`
- gemini-image-service: `GEMINI_API_KEY`
- ibd-distribution-day-monitor: `FMP_API_KEY`
- institutional-flow-tracker: `FMP_API_KEY`
- kanchi-dividend-sop: `FMP_API_KEY`
- macro-regime-detector: `FMP_API_KEY`
- market-top-detector: `FMP_API_KEY`
- options-strategy-advisor: `FMP_API_KEY`
- pair-trade-screener: `FMP_API_KEY`
- parabolic-short-trade-planner: `ALPACA_API_KEY`
- parabolic-short-trade-planner: `FMP_API_KEY`
- pead-screener: `FMP_API_KEY`
- signal-postmortem: `FMP_API_KEY`
- theme-detector: `FINVIZ_API_KEY`
- theme-detector: `FMP_API_KEY`
- value-dividend-screener: `FINVIZ_API_KEY`
- value-dividend-screener: `FMP_API_KEY`
- vcp-screener: `FMP_API_KEY`
- agentmail: `AGENTMAIL_API_KEY`
- ai-image-generation: `GEMINI_API_KEY`
- fullstack-dev: `JWT_SECRET`
- media-downloader: `PEXELS_API_KEY`
- notebooklm-skill: `GEMINI_API_KEY`

## Duplicate Capabilities
- None

## Missing Native Origins
- None

## Standard Bundle Issues
- None

## Risk Findings
- skill-vetter: `\bsudo\b` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/skill-vetter/scripts/install.sh`
- alphaear-predictor: `(?<![A-Za-z0-9_])eval\s*\(` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/alphaear-predictor/scripts/utils/predictor/evaluation.py`
- alphaear-predictor: `(?<![A-Za-z0-9_])eval\s*\(` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/alphaear-predictor/scripts/utils/predictor/training.py`
- alphaear-signal-tracker: `(?<![A-Za-z0-9_])eval\s*\(` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/alphaear-signal-tracker/scripts/utils/predictor/evaluation.py`
- alphaear-signal-tracker: `(?<![A-Za-z0-9_])eval\s*\(` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/alphaear-signal-tracker/scripts/utils/predictor/training.py`
- alphaear-reporter: `(?<![A-Za-z0-9_])eval\s*\(` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/alphaear-reporter/scripts/utils/predictor/evaluation.py`
- alphaear-reporter: `(?<![A-Za-z0-9_])eval\s*\(` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/alphaear-reporter/scripts/utils/predictor/training.py`
- vcp-screener: `rm\s+-rf\s+/` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/vcp-screener/scripts/tests/test_historical_vcp.py`
- minimax-docx: `\bsudo\b` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/minimax-docx/scripts/env_check.sh`
- minimax-docx: `\bsudo\b` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/minimax-docx/scripts/setup.sh`
- minimax-xlsx: `\bsudo\b` in `/Volumes/PSSD/Projects/boutique-skills/skills/default/minimax-xlsx/scripts/libreoffice_recalc.py`
