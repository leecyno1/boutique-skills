# 使用条件索引

| 使用条件 | 数量 |
|---|---:|
| `api-key` | 98 |
| `api-key+mcp-required` | 22 |
| `browser-required` | 17 |
| `direct` | 151 |
| `mcp-required` | 71 |

## api-key

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `claude-mem-plugin` | `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY` | 无 | `high` |
| `github` | `GH_TOKEN`, `GITHUB_TOKEN` | `gh` | `medium` |
| `a-stock-data` | `TUSHARE_TOKEN` | `python` | `medium` |
| `agentmail-toolkit` | `AGENTMAIL_API_KEY`, `OPENAI_API_KEY` | 无 | `medium` |
| `akshare-stock` | `TUSHARE_TOKEN` | `python` | `medium` |
| `animation` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `baoyu-article-illustrator` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `baoyu-image-gen` | `ARK_API_KEY`, `AZURE_OPENAI_API_KEY`, `BIGMODEL_API_KEY`, `DASHSCOPE_API_KEY`, `GOOGLE_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID`, `MINIMAX_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `REPLICATE_API_TOKEN`, `ZAI_API_KEY` | 无 | `medium` |
| `baoyu-youtube-transcript` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `ffmpeg`, `python` | `medium` |
| `dual-axis-skill-reviewer` | `OPENAI_API_KEY` | 无 | `medium` |
| `guizang-social-card-skill` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `ffmpeg` | `medium` |
| `ima` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `lark-calendar` | `FEISHU_APP_SECRET` | 无 | `medium` |
| `openclaw-stock-data-skill` | `STOCK_API_KEY` | `python` | `medium` |
| `paperless-docs` | `PAPERLESS_TOKEN` | 无 | `medium` |
| `paperless-ngx-tools` | `PAPERLESS_TOKEN` | 无 | `medium` |
| `seedance2-skill` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `tavily-search` | `OPENAI_API_KEY`, `TAVILY_API_KEY` | `browser`, `python` | `medium` |
| `tushare-openclaw-skill` | `TUSHARE_TOKEN` | 无 | `medium` |
| `agentmail-cli` | `AGENTMAIL_API_KEY` | 无 | `medium` |
| `alphaear-reporter` | `TUSHARE_TOKEN` | `python` | `medium` |
| `alphaear-sentiment` | `OPENAI_API_KEY` | `python` | `medium` |
| `alphaear-stock` | `TUSHARE_TOKEN` | `python` | `medium` |
| `baoyu-comic` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `baoyu-compress-image` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `browser` | `medium` |
| `baoyu-cover-image` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `baoyu-post-to-wechat` | `ACCESS_TOKEN`, `IMA_API_KEY`, `IMA_CLIENT_ID`, `WECHAT_AI_TOOLS_APP_SECRET`, `WECHAT_APP_SECRET`, `WECHAT_BAOYU_APP_SECRET` | `browser` | `medium` |
| `baoyu-post-to-weibo` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `browser`, `ffmpeg` | `medium` |
| `baoyu-post-to-x` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `browser`, `ffmpeg` | `medium` |
| `baoyu-slide-deck` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `baoyu-xhs-images` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `breadth-chart-analyst` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `python` | `medium` |
| `breakout-trade-planner` | `TUSHARE_TOKEN` | 无 | `medium` |
| `canslim-screener` | `FMP_API_KEY` | `python` | `medium` |
| `company-valuation` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `data-quality-checker` | `TUSHARE_TOKEN` | `python` | `medium` |
| `dividend-growth-pullback-screener` | `FINVIZ_API_KEY`, `FMP_API_KEY` | `python` | `medium` |
| `downtrend-duration-analyzer` | `FMP_API_KEY` | 无 | `medium` |
| `earnings-calendar` | `FMP_API_KEY` | `browser`, `python` | `medium` |
| `earnings-preview` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `node`, `python` | `medium` |
| `earnings-recap` | `TUSHARE_TOKEN` | `node`, `python` | `medium` |
| `earnings-trade-analyzer` | `FMP_API_KEY` | `node`, `python` | `medium` |
| `economic-calendar-fetcher` | `FMP_API_KEY` | `node`, `python` | `medium` |
| `edge-candidate-agent` | `TUSHARE_TOKEN` | `python` | `medium` |
| `edge-hint-extractor` | `OPENAI_API_KEY` | `node` | `medium` |
| `estimate-analysis` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `node`, `python` | `medium` |
| `exposure-coach` | `FMP_API_KEY` | 无 | `medium` |
| `finance-sentiment` | `ADANOS_API_KEY` | `python` | `medium` |
| `finance-skill-creator` | `TUSHARE_TOKEN` | `python` | `medium` |
| `finviz-screener` | `FINVIZ_API_KEY` | `python` | `medium` |
| `ftd-detector` | `FMP_API_KEY` | 无 | `medium` |
| `gemini-image-service` | `GEMINI_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `ibd-distribution-day-monitor` | `FMP_API_KEY` | 无 | `medium` |
| `inference-skills` | `OPENAI_API_KEY` | 无 | `medium` |
| `institutional-flow-tracker` | `FMP_API_KEY` | `python` | `medium` |
| `kanchi-dividend-review-monitor` | `TUSHARE_TOKEN` | 无 | `medium` |
| `kanchi-dividend-sop` | `FMP_API_KEY` | `python` | `medium` |
| `macro-regime-detector` | `FMP_API_KEY` | 无 | `medium` |
| `market-environment-analysis` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `python` | `medium` |
| `market-top-detector` | `FMP_API_KEY` | `python` | `medium` |
| `minimax-image-understanding` | `IMA_API_KEY`, `IMA_CLIENT_ID`, `MINIMAX_API_KEY` | 无 | `medium` |
| `options-payoff` | `TUSHARE_TOKEN` | 无 | `medium` |
| `options-strategy-advisor` | `FMP_API_KEY` | 无 | `medium` |
| `oracle` | `OPENAI_API_KEY` | `browser` | `medium` |
| `pair-trade-screener` | `FMP_API_KEY` | `python` | `medium` |
| `parabolic-short-trade-planner` | `ALPACA_API_KEY`, `FMP_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `pead-screener` | `FMP_API_KEY` | `python` | `medium` |
| `position-sizer` | `TUSHARE_TOKEN` | `python` | `medium` |
| `pybroker-backtest-skill` | `TUSHARE_TOKEN` | 无 | `medium` |
| `saas-valuation-compression` | `TUSHARE_TOKEN` | 无 | `medium` |
| `sector-analyst` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `python` | `medium` |
| `sepa-strategy` | `TUSHARE_TOKEN` | `python` | `medium` |
| `signal-postmortem` | `FMP_API_KEY` | 无 | `medium` |
| `stock-analysis` | `TUSHARE_TOKEN` | `node`, `python` | `medium` |
| `stock-correlation` | `TUSHARE_TOKEN` | `python` | `medium` |
| `stock-daily-analysis-skill` | `OPENAI_API_KEY` | `python` | `medium` |
| `stock-liquidity` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `python` | `medium` |
| `stock-monitor-skill` | `TUSHARE_TOKEN` | `python` | `medium` |
| `technical-analyst` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `python` | `medium` |
| `theme-detector` | `FINVIZ_API_KEY`, `FMP_API_KEY` | 无 | `medium` |
| `value-dividend-screener` | `FINVIZ_API_KEY`, `FMP_API_KEY` | `python` | `medium` |
| `vcp-screener` | `FMP_API_KEY` | `python` | `medium` |
| `agentmail` | `AGENTMAIL_API_KEY` | `browser` | `medium` |
| `ai-image-generation` | `GEMINI_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID`, `OPENAI_API_KEY` | 无 | `medium` |
| `frontend-dev` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `browser`, `ffmpeg`, `node` | `medium` |
| `fullstack-dev` | `JWT_SECRET` | `browser`, `node`, `python` | `medium` |
| `media-downloader` | `IMA_API_KEY`, `IMA_CLIENT_ID`, `PEXELS_API_KEY` | `ffmpeg` | `medium` |
| `minimax-docx` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `minimax-multimodal-toolkit` | `IMA_API_KEY`, `IMA_CLIENT_ID`, `MINIMAX_API_KEY` | `browser`, `ffmpeg` | `medium` |
| `minimax-pdf` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `minimax-xlsx` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `node`, `python` | `medium` |
| `notebooklm-skill` | `GEMINI_API_KEY` | `browser` | `medium` |
| `react-native-dev` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `node`, `python` | `medium` |
| `codex-responses-tooling` | `IMA_API_KEY`, `IMA_CLIENT_ID` | 无 | `medium` |
| `gif-sticker-maker` | `IMA_API_KEY`, `IMA_CLIENT_ID`, `MINIMAX_API_KEY` | `ffmpeg` | `medium` |
| `minimax-music-gen` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `ffmpeg` | `medium` |
| `minimax-music-playlist` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `ffmpeg` | `medium` |
| `web-search` | `IMA_API_KEY`, `IMA_CLIENT_ID` | `browser`, `ffmpeg` | `medium` |

## api-key+mcp-required

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `agentmail-mcp` | `AGENTMAIL_API_KEY` | `mcp` | `medium` |
| `funda-data` | `FUNDA_API_KEY`, `IMA_API_KEY`, `IMA_CLIENT_ID` | `mcp`, `python` | `medium` |
| `llmquant-commodities` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-credit` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-crypto` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-data` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-equities` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-equity-derivatives` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-etfs` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-events` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-investor-lenses` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-macro` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-market-intelligence` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-options` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-portfolio` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-portfolio-lab` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-prediction-markets` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-rates-fx` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-risk` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `llmquant-strategies` | `LLMQUANT_API_KEY` | `mcp`, `node` | `medium` |
| `minimax-web-search` | `IMA_API_KEY`, `IMA_CLIENT_ID`, `MINIMAX_API_KEY` | `browser`, `mcp` | `medium` |
| `vision-analysis` | `IMA_API_KEY`, `IMA_CLIENT_ID`, `MINIMAX_API_KEY` | `browser`, `ffmpeg`, `mcp`, `python` | `medium` |

## browser-required

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `html-anything` | 无 | `browser`, `node` | `medium` |
| `impeccable` | 无 | `browser`, `node` | `medium` |
| `agent-browser` | 无 | `browser`, `python` | `medium` |
| `url-to-markdown` | 无 | `browser` | `medium` |
| `tech-earnings-deepdive` | 无 | `browser` | `medium` |
| `macro-liquidity` | 无 | `browser` | `medium` |
| `agent-reach` | 无 | `browser`, `ffmpeg`, `gh` | `medium` |
| `baoyu-url-to-markdown` | 无 | `browser` | `medium` |
| `guizang-ppt-skill` | 无 | `browser` | `medium` |
| `openclaw-cron-setup` | 无 | `browser` | `medium` |
| `btc-bottom-model` | 无 | `browser` | `medium` |
| `us-market-sentiment` | 无 | `browser` | `medium` |
| `alphaear-search` | `TUSHARE_TOKEN` | `browser`, `python` | `medium` |
| `baoyu-markdown-to-html` | 无 | `browser` | `medium` |
| `market-news-analyst` | 无 | `browser`, `node`, `python` | `medium` |
| `video-shotcraft` | 无 | `browser`, `ffmpeg`, `node` | `medium` |
| `us-value-investing` | 无 | `browser` | `medium` |

## direct

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `brainstorming` | 无 | 无 | `low` |
| `find-skills` | 无 | 无 | `low` |
| `model-usage` | 无 | `python` | `low` |
| `planning-with-files` | 无 | 无 | `low` |
| `skill-creator` | 无 | 无 | `low` |
| `skill-security-auditor` | 无 | `python` | `low` |
| `skill-vetter` | 无 | 无 | `low` |
| `subagent-driven-development` | 无 | 无 | `low` |
| `task` | 无 | 无 | `low` |
| `todo` | 无 | `python` | `low` |
| `using-superpowers` | 无 | 无 | `low` |
| `verification-before-completion` | 无 | 无 | `low` |
| `weather` | 无 | 无 | `low` |
| `writing-skills` | 无 | 无 | `low` |
| `animation-vocabulary` | 无 | 无 | `low` |
| `apple-design` | 无 | 无 | `low` |
| `backtest-expert` | 无 | 无 | `low` |
| `behavior-validator` | 无 | 无 | `low` |
| `brandkit` | 无 | 无 | `low` |
| `dasheng-hotspot-radar` | 无 | `python` | `low` |
| `data-analyst` | 无 | `python` | `low` |
| `dbskill` | 无 | 无 | `low` |
| `design-taste-frontend` | 无 | 无 | `low` |
| `design-taste-frontend-v1` | 无 | 无 | `low` |
| `discord-reader` | 无 | `node` | `low` |
| `edge-concept-synthesizer` | 无 | 无 | `low` |
| `edge-pipeline-orchestrator` | 无 | 无 | `low` |
| `edge-signal-aggregator` | 无 | `python` | `low` |
| `edge-strategy-designer` | 无 | 无 | `low` |
| `edge-strategy-reviewer` | 无 | 无 | `low` |
| `emil-design-eng` | 无 | 无 | `low` |
| `feishu-doc-creator` | 无 | `python` | `low` |
| `find-animation-opportunities` | 无 | 无 | `low` |
| `full-output-enforcement` | 无 | 无 | `low` |
| `generative-ui` | 无 | 无 | `low` |
| `gpt-taste` | 无 | 无 | `low` |
| `gsap-core` | 无 | `node` | `low` |
| `gsap-frameworks` | 无 | `node` | `low` |
| `gsap-performance` | 无 | `node` | `low` |
| `gsap-plugins` | 无 | `node` | `low` |
| `gsap-react` | 无 | `node` | `low` |
| `gsap-scrolltrigger` | 无 | `node` | `low` |
| `gsap-timeline` | 无 | `node` | `low` |
| `gsap-utils` | 无 | `node` | `low` |
| `high-end-visual-design` | 无 | 无 | `low` |
| `humanizer-zh` | 无 | 无 | `low` |
| `ian-xiaohei-illustrations` | 无 | 无 | `low` |
| `image-to-code` | 无 | 无 | `low` |
| `imagegen-frontend-mobile` | 无 | 无 | `low` |
| `imagegen-frontend-web` | 无 | 无 | `low` |
| `improve-animations` | 无 | 无 | `low` |
| `industrial-brutalist-ui` | 无 | 无 | `low` |
| `khazix-skills` | 无 | 无 | `low` |
| `linkedin-reader` | 无 | `python` | `low` |
| `minimalist-ui` | 无 | 无 | `low` |
| `multi-search-engine` | 无 | 无 | `low` |
| `nano-pdf` | 无 | 无 | `low` |
| `openclaw-stock-kb` | 无 | `python` | `low` |
| `opencli-reader` | 无 | `python` | `low` |
| `pick-ui-library` | 无 | 无 | `low` |
| `proactive-agent` | 无 | 无 | `low` |
| `redesign-existing-projects` | 无 | 无 | `low` |
| `reflection` | 无 | 无 | `low` |
| `review-animations` | 无 | 无 | `low` |
| `scenario-analyzer` | 无 | `python` | `low` |
| `scroll-world` | 无 | `ffmpeg`, `higgsfield`, `python` | `low` |
| `self-improving-agent-cn` | 无 | 无 | `low` |
| `skill-designer` | 无 | 无 | `low` |
| `skill-integration-tester` | 无 | `python` | `low` |
| `stitch-design-taste` | 无 | 无 | `low` |
| `strategy-pivot-designer` | 无 | 无 | `low` |
| `telegram-reader` | 无 | 无 | `low` |
| `twitter-reader` | 无 | 无 | `low` |
| `writing-plans` | 无 | 无 | `low` |
| `yc-reader` | 无 | `python` | `low` |
| `dasheng-finance-data` | 无 | `python` | `medium` |
| `global-stock-data` | 无 | `python` | `medium` |
| `yfinance-data` | 无 | `python` | `medium` |
| `baoyu-format-markdown` | 无 | 无 | `low` |
| `baoyu-infographic` | 无 | 无 | `low` |
| `baoyu-skills` | 无 | 无 | `low` |
| `baoyu-translate` | 无 | 无 | `low` |
| `bilibili-upload-bridge` | 无 | `ffmpeg`, `node` | `low` |
| `capability-evolver` | 无 | 无 | `low` |
| `channels-account-launch-expert` | 无 | 无 | `low` |
| `dasheng-html-anything-bridge` | 无 | 无 | `low` |
| `dasheng-html-video-bridge` | 无 | `ffmpeg`, `node` | `low` |
| `dasheng-media-sop` | 无 | 无 | `low` |
| `dasheng-paradigm-profiler` | 无 | 无 | `low` |
| `dasheng-publish-operations-bridge` | 无 | 无 | `low` |
| `dasheng-stage-brief-ai` | 无 | 无 | `low` |
| `dasheng-stage-draft` | 无 | 无 | `low` |
| `dasheng-stage-publish` | 无 | 无 | `low` |
| `dasheng-stage-rewrite-v3` | 无 | 无 | `low` |
| `dasheng-stage-transwrite` | 无 | 无 | `low` |
| `dasheng-style-profiler` | 无 | 无 | `low` |
| `dasheng-video-director` | 无 | 无 | `low` |
| `dasheng-video-explainer-html` | 无 | `ffmpeg`, `node` | `low` |
| `dasheng-video-roughcut` | 无 | `ffmpeg`, `node` | `low` |
| `dasheng-video-style-trainer` | 无 | 无 | `low` |
| `dasheng-video-talking-head` | 无 | `ffmpeg`, `node`, `python` | `low` |
| `douyin-account-launch-expert` | 无 | 无 | `low` |
| `jiebang` | 无 | 无 | `low` |
| `skill-idea-miner` | 无 | 无 | `low` |
| `social-auto-upload-bridge` | 无 | `ffmpeg`, `node` | `low` |
| `startup-analysis` | 无 | 无 | `low` |
| `wb-xhs-account-profile` | 无 | 无 | `low` |
| `wb-xhs-humanize-compliance` | 无 | 无 | `low` |
| `wb-xhs-low-follower-pattern` | 无 | 无 | `low` |
| `wb-xhs-monetization-backsolve` | 无 | 无 | `low` |
| `wb-xhs-schedule-review` | 无 | 无 | `low` |
| `wb-xhs-topic-bank` | 无 | 无 | `low` |
| `wechat-account-launch-expert` | 无 | 无 | `low` |
| `x-twitter-cold-start-expert` | 无 | 无 | `low` |
| `xiaohongshu-account-launch-expert` | 无 | 无 | `low` |
| `android-native-dev` | 无 | 无 | `low` |
| `content-strategy` | 无 | 无 | `low` |
| `flutter-dev` | 无 | 无 | `low` |
| `ios-application-dev` | 无 | 无 | `low` |
| `pptx-generator` | 无 | `node` | `low` |
| `shader-dev` | 无 | 无 | `low` |
| `social-content` | 无 | `ffmpeg` | `low` |
| `alphaear-deepear-lite` | 无 | `python` | `medium` |
| `alphaear-logic-visualizer` | 无 | `python` | `medium` |
| `alphaear-news` | 无 | `python` | `medium` |
| `alphaear-predictor` | 无 | `python` | `medium` |
| `alphaear-signal-tracker` | 无 | `python` | `medium` |
| `bayesian-intrinsic-growth-valuation` | 无 | `python` | `medium` |
| `buy-side-equity-research-memo` | 无 | `python` | `medium` |
| `etf-premium` | 无 | `python` | `medium` |
| `gf-dma-health-index` | 无 | `python` | `medium` |
| `hormuz-strait` | 无 | `python` | `medium` |
| `kanchi-dividend-us-tax-accounting` | 无 | 无 | `medium` |
| `market-breadth-analyzer` | 无 | `python` | `medium` |
| `paper-framework-figure-studio-pro` | 无 | `python` | `medium` |
| `policy-monitor` | 无 | 无 | `medium` |
| `serenity-alpha` | 无 | `python` | `medium` |
| `stanley-druckenmiller-investment` | 无 | 无 | `medium` |
| `tam-adj-peg` | 无 | `python` | `medium` |
| `trade-hypothesis-ideator` | 无 | `python` | `medium` |
| `trader-memory-core` | 无 | 无 | `medium` |
| `uptrend-analyzer` | 无 | `python` | `medium` |
| `us-market-bubble-detector` | 无 | `python` | `medium` |
| `us-stock-analysis` | 无 | `python` | `medium` |
| `buddy-sings` | 无 | `ffmpeg` | `low` |
| `marketingskills` | 无 | 无 | `low` |
| `docx` | 无 | 无 | `low` |
| `pdf` | 无 | 无 | `low` |
| `pptx` | 无 | `node` | `low` |
| `shell` | 无 | 无 | `high` |
| `xlsx` | 无 | `node`, `python` | `low` |

## mcp-required

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `chrome-devtools-mcp` | 无 | `browser`, `mcp` | `medium` |
| `mcp-builder` | 无 | `mcp` | `medium` |
| `news-radar` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-equity-research-catalyst-calendar` | 无 | `mcp` | `medium` |
| `anthropic-fs-equity-research-earnings-analysis` | 无 | `mcp` | `medium` |
| `anthropic-fs-equity-research-earnings-preview` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-equity-research-idea-generation` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-equity-research-initiating-coverage` | 无 | `mcp` | `medium` |
| `anthropic-fs-equity-research-model-update` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-equity-research-morning-note` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-equity-research-sector-overview` | 无 | `mcp` | `medium` |
| `anthropic-fs-equity-research-thesis-tracker` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-financial-analysis-3-statement-model` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-financial-analysis-audit-xls` | 无 | `mcp` | `medium` |
| `anthropic-fs-financial-analysis-clean-data-xls` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-financial-analysis-competitive-analysis` | 无 | `mcp` | `medium` |
| `anthropic-fs-financial-analysis-comps-analysis` | 无 | `mcp` | `medium` |
| `anthropic-fs-financial-analysis-dcf-model` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-financial-analysis-deck-refresh` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-financial-analysis-ib-check-deck` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-financial-analysis-lbo-model` | 无 | `mcp` | `medium` |
| `anthropic-fs-financial-analysis-ppt-template-creator` | 无 | `mcp`, `node` | `medium` |
| `anthropic-fs-financial-analysis-pptx-author` | 无 | `mcp`, `node` | `medium` |
| `anthropic-fs-financial-analysis-skill-creator` | 无 | `mcp` | `medium` |
| `anthropic-fs-financial-analysis-xlsx-author` | 无 | `mcp`, `node` | `medium` |
| `anthropic-fs-fund-admin-accrual-schedule` | 无 | `mcp` | `medium` |
| `anthropic-fs-fund-admin-break-trace` | 无 | `mcp` | `medium` |
| `anthropic-fs-fund-admin-gl-recon` | 无 | `mcp` | `medium` |
| `anthropic-fs-fund-admin-nav-tieout` | 无 | `mcp` | `medium` |
| `anthropic-fs-fund-admin-roll-forward` | 无 | `mcp` | `medium` |
| `anthropic-fs-fund-admin-variance-commentary` | 无 | `mcp` | `medium` |
| `anthropic-fs-investment-banking-buyer-list` | 无 | `mcp` | `medium` |
| `anthropic-fs-investment-banking-cim-builder` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-investment-banking-datapack-builder` | 无 | `browser`, `mcp`, `python` | `medium` |
| `anthropic-fs-investment-banking-deal-tracker` | 无 | `mcp` | `medium` |
| `anthropic-fs-investment-banking-merger-model` | 无 | `mcp` | `medium` |
| `anthropic-fs-investment-banking-pitch-deck` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-investment-banking-process-letter` | 无 | `mcp` | `medium` |
| `anthropic-fs-investment-banking-strip-profile` | 无 | `mcp` | `medium` |
| `anthropic-fs-investment-banking-teaser` | 无 | `mcp` | `medium` |
| `anthropic-fs-lseg-bond-futures-basis` | 无 | `mcp` | `medium` |
| `anthropic-fs-lseg-bond-relative-value` | 无 | `mcp` | `medium` |
| `anthropic-fs-lseg-equity-research` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-lseg-fixed-income-portfolio` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-lseg-fx-carry-trade` | 无 | `mcp` | `medium` |
| `anthropic-fs-lseg-macro-rates-monitor` | 无 | `mcp` | `medium` |
| `anthropic-fs-lseg-option-vol-analysis` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-lseg-swap-curve-strategy` | 无 | `mcp` | `medium` |
| `anthropic-fs-operations-kyc-doc-parse` | 无 | `mcp` | `medium` |
| `anthropic-fs-operations-kyc-rules` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-ai-readiness` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-dd-checklist` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-private-equity-dd-meeting-prep` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-deal-screening` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-deal-sourcing` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-ic-memo` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-portfolio-monitoring` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-returns-analysis` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-unit-economics` | 无 | `mcp` | `medium` |
| `anthropic-fs-private-equity-value-creation-plan` | 无 | `mcp` | `medium` |
| `anthropic-fs-spglobal-earnings-preview-beta` | 无 | `mcp` | `medium` |
| `anthropic-fs-spglobal-funding-digest` | 无 | `mcp`, `node`, `python` | `medium` |
| `anthropic-fs-spglobal-tear-sheet` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-wealth-management-client-report` | 无 | `mcp` | `medium` |
| `anthropic-fs-wealth-management-client-review` | 无 | `mcp`, `python` | `medium` |
| `anthropic-fs-wealth-management-financial-plan` | 无 | `mcp` | `medium` |
| `anthropic-fs-wealth-management-investment-proposal` | 无 | `mcp` | `medium` |
| `anthropic-fs-wealth-management-portfolio-rebalance` | 无 | `mcp` | `medium` |
| `anthropic-fs-wealth-management-tax-loss-harvesting` | 无 | `mcp` | `medium` |
| `dasheng-xhs-publish-bridge` | 无 | `browser`, `mcp`, `node` | `medium` |
| `portfolio-manager` | 无 | `mcp`, `python` | `medium` |
