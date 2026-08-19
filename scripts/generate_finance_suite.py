#!/usr/bin/env python3
"""Regenerate the finance-investment-standard suite with capability dedupe.

The suite targets advanced finance/investment users and keeps at most
MAX_SKILLS skills. For every capability slot only the highest-scored
skill is kept, so overlapping skills inside the same slot compete on
score and only the best survives. Run after generate_enriched_catalog.py.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENRICHED_CATALOG = ROOT / "catalog" / "skills.enriched.json"
SUITE_PATH = ROOT / "catalog" / "suites" / "finance-investment-standard.json"
SKILLS_DIR = ROOT / "skills" / "default"

MAX_SKILLS = 40

# (slot, slot_label, [candidate skill ids in tie-break order])
FINANCE_SLOTS = [
    ("a-share-data", "A股结构化数据", ["tushare-openclaw-skill", "a-stock-data", "akshare-stock", "openclaw-stock-data-skill"]),
    ("global-market-data", "美股/港股全栈数据", ["global-stock-data", "yfinance-data"]),
    ("institutional-data", "SEC/13F/机构数据", ["llmquant-data", "funda-data"]),
    ("macro", "宏观研究", ["llmquant-macro", "llmquant-market-intelligence"]),
    ("policy", "宏观/政策跟踪", ["policy-monitor"]),
    ("macro-liquidity", "宏观流动性", ["macro-liquidity"]),
    ("event-news", "事件与新闻", ["llmquant-events", "alphaear-news"]),
    ("stock-analysis", "综合个股研究", ["uzi-skill", "stock-analysis", "us-stock-analysis", "alphagbm-stock-analysis"]),
    ("tech-earnings", "科技股财报深研", ["tech-earnings-deepdive"]),
    ("earnings-cycle", "财报前预案/复盘", ["earnings-preview", "earnings-recap", "anthropic-fs-equity-research-earnings-preview"]),
    ("screener-growth", "成长股筛选", ["canslim-screener"]),
    ("screener-technical", "技术形态筛选", ["vcp-screener"]),
    ("screener-value", "股息/价值筛选", ["value-dividend-screener"]),
    ("screener-us", "美股全市场筛选", ["finviz-screener"]),
    ("theme-research", "主题研究", ["alphagbm-theme-research", "theme-detector"]),
    ("valuation", "估值建模", ["bayesian-intrinsic-growth-valuation", "tam-adj-peg", "anthropic-fs-financial-analysis-dcf-model"]),
    ("equity-research-memo", "买方研究备忘录", ["buy-side-equity-research-memo", "anthropic-fs-equity-research-initiating-coverage"]),
    ("technical-trend", "市场宽度/趋势", ["uptrend-analyzer", "technical-analyst", "breadth-chart-analyst"]),
    ("market-sentiment", "美股市场情绪", ["alphagbm-market-sentiment", "us-market-sentiment"]),
    ("trade-plan", "交易计划", ["sepa-strategy", "breakout-trade-planner"]),
    ("position-sizing", "仓位管理", ["position-sizer"]),
    ("options", "期权策略", ["alphagbm-options-strategy", "llmquant-options", "options-strategy-advisor"]),
    ("portfolio", "组合管理", ["llmquant-portfolio", "llmquant-portfolio-lab"]),
    ("risk", "组合风险", ["llmquant-risk"]),
    ("monitoring", "自选股监控", ["alphagbm-watchlist", "stock-monitor-skill"]),
    ("thesis-memory", "持仓 Thesis 记忆", ["trader-memory-core"]),
    ("backtest-engine", "回测引擎", ["alphagbm-bps-backtest", "pybroker-backtest-skill"]),
    ("backtest-review", "回测审查", ["backtest-expert"]),
    ("postmortem", "交易后验复盘", ["signal-postmortem", "alphaear-predictor"]),
    ("quant-strategy", "量化策略", ["llmquant-strategies"]),
    ("etf", "ETF 研究", ["llmquant-etfs"]),
    ("report", "投研报告生成", ["alphaear-reporter"]),
    ("knowledge-base", "金融知识库", ["openclaw-stock-kb"]),
    ("data-quality", "数据质量", ["data-quality-checker"]),
]

SOURCE_PACKS = [
    {
        "id": "llmquant",
        "title": "LLMQuant Institutional Finance",
        "source": "https://github.com/LLMQuant/skills",
        "score": 81,
    },
    {
        "id": "claude-trading-skills",
        "title": "Claude Trading Skills",
        "source": "https://github.com/tradermonty/claude-trading-skills",
        "score": 84,
    },
    {
        "id": "a-stock-data",
        "title": "A-stock-data",
        "source": "https://github.com/simonlin1212/a-stock-data",
        "score": 78,
    },
    {
        "id": "global-stock-data",
        "title": "Global-stock-data",
        "source": "https://github.com/simonlin1212/global-stock-data",
        "score": 86,
    },
    {
        "id": "anthropic-fs",
        "title": "Anthropic Financial Services",
        "source": "https://github.com/anthropics/financial-services",
        "score": 74,
    },
    {
        "id": "alphagbm",
        "title": "AlphaGBM Options & Research",
        "source": "https://github.com/AlphaGBM/skills",
        "score": 82,
    },
    {
        "id": "uzi-skill",
        "title": "UZI Skill",
        "source": "https://github.com/wbh604/UZI-Skill",
        "score": 86,
    },
]


def load_enriched() -> dict[str, dict]:
    data = json.loads(ENRICHED_CATALOG.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data.get("skills", [])}


def pick_best(candidates: list[str], enriched: dict[str, dict]) -> dict | None:
    """Return the highest-scored locally available candidate; ties keep list order."""
    available = []
    for skill_id in candidates:
        item = enriched.get(skill_id)
        if item and (SKILLS_DIR / skill_id).is_dir() and not item.get("preset_excluded"):
            available.append(item)
    if not available:
        return None
    return min(available, key=lambda item: (-item["rating"]["score"], candidates.index(item["id"])))


def build_suite(enriched: dict[str, dict]) -> dict:
    slots = []
    selected_ids: list[str] = []
    for slot, label, candidates in FINANCE_SLOTS:
        best = pick_best(candidates, enriched)
        if not best or best["id"] in selected_ids:
            continue
        slots.append({
            "slot": label,
            "capability": slot,
            "skill": best["id"],
            "score": best["rating"]["score"],
        })
        selected_ids.append(best["id"])
        if len(selected_ids) >= MAX_SKILLS:
            break

    api_keys = sorted({
        key
        for skill_id in selected_ids
        for key in (enriched[skill_id]["dependencies"].get("api_keys") or [])
    })
    tools = sorted({
        tool
        for skill_id in selected_ids
        for tool in (enriched[skill_id]["dependencies"].get("required_tools") or [])
    })

    return {
        "schema_version": "2026.08.19",
        "id": "finance-investment-standard",
        "title": "Finance Investment Standard Suite",
        "description": (
            "金融投资标准组合（进阶）：面向金融投资用户的数据、研究、筛选、交易计划、"
            "仓位、期权、组合风控、监控、回测、复盘与报告全链路能力位组合。"
            "每个能力位只保留评分最高的技能，总量不超过 %d 个。" % MAX_SKILLS
        ),
        "source": "https://github.com/leecyno1/boutique-openclaw-skills",
        "native_origin": "https://github.com/leecyno1/boutique-openclaw-skills",
        "homepage": "",
        "license": "MIT",
        "install_tier": "high",
        "category": "finance-investment-standard",
        "horizontal_tier": "L3 Specialist",
        "access_mode": "api-key" if api_keys else "direct",
        "requires_api_keys": bool(api_keys),
        "api_keys": api_keys,
        "requires_tools": tools,
        "scorecard": "reports/finance-skill-eval/finance-investment-skills-scorecard-2026-06-14.md",
        "included_sources": [
            {**pack, "role": "upstream source family; representative skills only"}
            for pack in SOURCE_PACKS
        ],
        "standard_slots": slots,
        "skills": selected_ids,
        "notes": [
            "Generated by scripts/generate_finance_suite.py; regenerate after catalog updates.",
            "Capability-slot dedupe keeps only the highest-scored skill per slot.",
            f"Slot count {len(slots)}, skill count {len(selected_ids)} (max {MAX_SKILLS}).",
        ],
        "generated_at": date.today().isoformat(),
    }


def main() -> int:
    enriched = load_enriched()
    suite = build_suite(enriched)
    SUITE_PATH.write_text(json.dumps(suite, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "skills": len(suite["skills"]),
        "slots": len(suite["standard_slots"]),
        "api_keys": suite["api_keys"],
        "tools": suite["requires_tools"],
        "output": str(SUITE_PATH.relative_to(ROOT)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
