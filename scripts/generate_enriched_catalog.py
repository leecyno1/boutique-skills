#!/usr/bin/env python3
"""Generate enriched skill indexes, standard bundle, and README sections."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "catalog" / "default-skills.json"
ORIGIN_OVERRIDES = ROOT / "catalog" / "native-origin-overrides.json"
PRESETS_DIR = ROOT / "catalog" / "presets"
SUITES_DIR = ROOT / "catalog" / "suites"
ENRICHED_PATH = ROOT / "catalog" / "skills.enriched.json"
STANDARD_BUNDLE_PATH = ROOT / "catalog" / "standard-bundle.json"
STANDARD_BUNDLE_OVERRIDES = ROOT / "catalog" / "standard-bundle-overrides.json"
TUSHARE_ROUTING = ROOT / "catalog" / "tushare-finance-routing.json"
TIERS_DIR = ROOT / "tiers"
DOC_TIERS_DIR = ROOT / "docs" / "tiers"
MANUALS_DOC = ROOT / "docs" / "SKILL_MANUALS.md"
HORIZONTAL_PATH = ROOT / "docs" / "generated" / "horizontal-index.md"
TYPE_PATH = ROOT / "docs" / "generated" / "type-index.md"
DEPENDENCY_PATH = ROOT / "docs" / "generated" / "dependency-index.md"
SCORING_PATH = ROOT / "docs" / "generated" / "scoring-model.md"
README_PATH = ROOT / "README.md"
MARKER_START = "<!-- SKILLS_INDEX:START -->"
MARKER_END = "<!-- SKILLS_INDEX:END -->"

TODAY = date.today().isoformat()
MIRROR_PATTERN = re.compile(r"leecyno1/(?:auto-install-Openclaw|boutique-(?:openclaw-)?skills)", re.I)

CATEGORY_LABELS = {
    "core-agent": "核心 Agent 能力",
    "search-research": "搜索 / 研究 / 情报",
    "browser-automation": "浏览器 / 自动化",
    "coding-devtools": "编程 / 工程工具",
    "data-analysis": "数据分析",
    "docs-office": "文档 / 办公",
    "design-ui": "设计 / UI",
    "html-publishing": "HTML 发布 / 视觉出版",
    "media-generation": "媒体生成 / 处理",
    "writing-content": "写作 / 内容",
    "marketing-growth": "营销 / 增长",
    "finance-trading": "金融 / 交易",
    "finance-services": "金融 / 机构服务",
    "finance-data": "金融 / 数据源",
    "finance-knowledge": "金融 / 知识库",
    "finance-monitor": "金融 / 监控预警",
    "policy-monitoring": "政策 / 宏观监控",
    "legal-compliance": "法律 / 合规 / 税务",
    "productivity-pkm": "效率 / 知识管理",
    "memory-context": "记忆 / 上下文基础设施",
    "communication": "通信 / 社交集成",
    "devops-cloud": "DevOps / 云 / 数据库",
    "security-audit": "安全 / 审计",
    "local-macos": "本地 macOS / 桌面",
    "agent-orchestration": "多 Agent / 自动调度",
    "commerce-ops": "商业运营",
    "education-learning": "教育 / 学习",
}

CATEGORY_KEYWORDS = [
    ("finance-trading", ["stock", "trade", "trader", "market", "finance", "earnings", "dividend", "etf", "portfolio", "valuation", "screener", "macro", "alphaear", "canslim", "vcp", "ftd", "options", "liquidity", "breadth", "funda", "yfinance", "akshare", "finviz"]),
    ("legal-compliance", ["tax", "compliance", "legal", "accounting"]),
    ("browser-automation", ["browser", "chrome-devtools", "playwright", "web automation"]),
    ("search-research", ["search", "news", "reader", "radar", "research", "url-to-markdown", "notebooklm", "yc-reader", "telegram-reader", "twitter-reader", "linkedin-reader", "discord-reader"]),
    ("coding-devtools", ["dev", "github", "mcp", "shell", "database", "prisma", "frontend", "fullstack", "flutter", "android", "ios", "react-native", "shader", "skill-creator", "writing-skills"]),
    ("data-analysis", ["data", "analyst", "quality", "reconciliation", "xlsx", "chart"]),
    ("docs-office", ["docx", "pdf", "pptx", "xlsx", "paperless", "meeting", "calendar"]),
    ("html-publishing", ["html-anything", "html publishing", "wechat export", "zhihu", "xiaohongshu card"]),
    ("design-ui", ["design", "ui", "generative-ui", "animation", "visualizer", "brand", "logo"]),
    ("media-generation", ["image", "music", "video", "gif", "multimodal", "vision", "media", "compress", "sings"]),
    ("marketing-growth", ["marketing", "social", "xiaohongshu", "zhihu", "weibo", "content-strategy", "producthunt", "seo"]),
    ("writing-content", ["writing", "translate", "markdown", "article", "post", "draft", "baoyu", "dasheng", "prose"]),
    ("communication", ["agentmail", "mail", "slack", "telegram", "discord", "lark", "feishu", "whatsapp"]),
    ("productivity-pkm", ["todo", "task", "things", "obsidian", "notebook", "calendar", "reminder", "notes"]),
    ("security-audit", ["security", "audit", "reviewer", "danger"]),
    ("memory-context", ["memory", "context injection", "claude-mem", "persistent context", "cross-session"]),
    ("agent-orchestration", ["agent", "subagent", "proactive", "cron", "reflection", "superpowers", "planning", "verification", "brainstorming", "capability"]),
    ("devops-cloud", ["database", "cloud", "deploy", "ops", "sql", "server"]),
]

L1 = {
    "agent-browser", "brainstorming", "chrome-devtools-mcp", "find-skills", "github",
    "mcp-builder", "model-usage", "planning-with-files", "shell", "skill-creator",
    "skill-vetter",
    "skill-security-auditor", "subagent-driven-development", "task", "todo",
    "url-to-markdown", "using-superpowers", "verification-before-completion", "web-search",
    "writing-skills", "weather",
}
L2_HINTS = {
    "data-analyst", "docx", "xlsx", "pptx", "pdf", "frontend-dev", "fullstack-dev",
    "database", "a-stock-data", "media-downloader", "ai-image-generation", "news-radar",
    "tavily-search", "multi-search-engine", "notebooklm-skill", "content-strategy",
    "social-content", "vision-analysis", "openclaw-cron-setup", "proactive-agent",
    "self-improving-agent-cn", "reflection", "writing-plans", "seedance2-skill",
    "html-anything", "ima",
    "behavior-validator",
    "guizang-ppt-skill", "khazix-skills", "humanizer-zh", "dbskill",
    "guizang-social-card-skill", "ian-xiaohei-illustrations",
}

LLMQUANT_SKILL_CATEGORIES = {
    "llmquant-data": "finance-data",
    "llmquant-etfs": "finance-data",
    "llmquant-investor-lenses": "finance-knowledge",
    "llmquant-events": "finance-monitor",
    "llmquant-macro": "finance-monitor",
    "llmquant-market-intelligence": "finance-monitor",
    "llmquant-portfolio": "finance-monitor",
    "llmquant-portfolio-lab": "finance-monitor",
    "llmquant-rates-fx": "finance-monitor",
    "llmquant-risk": "finance-monitor",
}

ANTHROPIC_FS_PLUGIN_CATEGORIES = {
    "equity-research": "finance-services",
    "financial-analysis": "finance-services",
    "fund-admin": "finance-services",
    "investment-banking": "finance-services",
    "operations": "legal-compliance",
    "private-equity": "finance-services",
    "wealth-management": "finance-services",
    "lseg": "finance-data",
    "spglobal": "finance-data",
}

TASTE_SKILLS = {
    "brandkit",
    "design-taste-frontend",
    "design-taste-frontend-v1",
    "full-output-enforcement",
    "gpt-taste",
    "high-end-visual-design",
    "image-to-code",
    "imagegen-frontend-mobile",
    "imagegen-frontend-web",
    "industrial-brutalist-ui",
    "minimalist-ui",
    "redesign-existing-projects",
    "stitch-design-taste",
}

ACCOUNT_LAUNCH_SKILLS = {
    "channels-account-launch-expert",
    "douyin-account-launch-expert",
    "wechat-account-launch-expert",
    "x-twitter-cold-start-expert",
    "xiaohongshu-account-launch-expert",
}

WORKBUDDY_XHS_SKILLS = {
    "wb-xhs-account-profile",
    "wb-xhs-humanize-compliance",
    "wb-xhs-low-follower-pattern",
    "wb-xhs-monetization-backsolve",
    "wb-xhs-schedule-review",
    "wb-xhs-topic-bank",
}

SERENITY_SKILLS = {
    "bayesian-intrinsic-growth-valuation",
    "buy-side-equity-research-memo",
    "gf-dma-health-index",
    "serenity-alpha",
    "tam-adj-peg",
}

EMIL_KOWALSKI_SKILLS = {
    "animation-vocabulary",
    "apple-design",
    "emil-design-eng",
    "find-animation-opportunities",
    "improve-animations",
    "pick-ui-library",
    "review-animations",
}

GSAP_SKILLS = {
    "gsap-core",
    "gsap-frameworks",
    "gsap-performance",
    "gsap-plugins",
    "gsap-react",
    "gsap-scrolltrigger",
    "gsap-timeline",
    "gsap-utils",
}

DAY1GLOBAL_SKILLS = {
    "btc-bottom-model",
    "macro-liquidity",
    "tech-earnings-deepdive",
    "us-market-sentiment",
    "us-value-investing",
}

ALPHAGBM_SKILLS = {
    "alphagbm-alert",
    "alphagbm-bps-backtest",
    "alphagbm-buffett-analysis",
    "alphagbm-chokepoint",
    "alphagbm-company-profile",
    "alphagbm-compare",
    "alphagbm-duan-analysis",
    "alphagbm-earnings-crush",
    "alphagbm-fear-score",
    "alphagbm-greeks",
    "alphagbm-health-check",
    "alphagbm-hedge-advisor",
    "alphagbm-investment-thesis",
    "alphagbm-iv-rank",
    "alphagbm-macro-view",
    "alphagbm-market-sentiment",
    "alphagbm-marks-cycle",
    "alphagbm-options-score",
    "alphagbm-options-strategy",
    "alphagbm-pnl-simulator",
    "alphagbm-polymarket",
    "alphagbm-stock-analysis",
    "alphagbm-take-profit",
    "alphagbm-tepper-signal",
    "alphagbm-theme-research",
    "alphagbm-unusual-activity",
    "alphagbm-vix-status",
    "alphagbm-vol-smile",
    "alphagbm-vol-surface",
    "alphagbm-watchlist",
}

ALPHAGBM_MONITOR_SKILLS = {
    "alphagbm-alert",
    "alphagbm-company-profile",
    "alphagbm-health-check",
    "alphagbm-investment-thesis",
    "alphagbm-macro-view",
    "alphagbm-theme-research",
    "alphagbm-watchlist",
}

EDITORIAL_SCORE_OVERRIDES = {
    "btc-bottom-model": 78,
    "eigenflux": 79,
    "impeccable": 92,
    "macro-liquidity": 82,
    "scientific-illustrator": 93,
    "tech-earnings-deepdive": 85,
    "us-market-sentiment": 76,
    "us-value-investing": 72,
    "video-autopilot-kit": 88,
    "dasheng-video-omni-browser": 82,
    "dasheng-vox-skills": 90,
    "westockdata": 76,
    "uzi-skill": 86,
}

DASHENG_MEDIA_WORKFLOW_CATEGORIES = {
    "bilibili-upload-bridge": "media-generation",
    "dasheng-finance-data": "finance-data",
    "dasheng-hotspot-radar": "search-research",
    "dasheng-html-anything-bridge": "html-publishing",
    "dasheng-html-video-bridge": "media-generation",
    "dasheng-media-sop": "marketing-growth",
    "dasheng-paradigm-profiler": "writing-content",
    "dasheng-publish-operations-bridge": "marketing-growth",
    "dasheng-stage-brief-ai": "writing-content",
    "dasheng-stage-draft": "writing-content",
    "dasheng-stage-publish": "marketing-growth",
    "dasheng-stage-rewrite-v3": "writing-content",
    "dasheng-stage-transwrite": "media-generation",
    "dasheng-style-profiler": "writing-content",
    "dasheng-video-director": "media-generation",
    "dasheng-video-explainer-html": "media-generation",
    "dasheng-video-omni-browser": "media-generation",
    "dasheng-video-roughcut": "media-generation",
    "dasheng-video-style-trainer": "media-generation",
    "dasheng-video-talking-head": "media-generation",
    "dasheng-vox-skills": "media-generation",
    "dasheng-xhs-publish-bridge": "marketing-growth",
    "feishu-doc-creator": "docs-office",
    "jiebang": "agent-orchestration",
    "social-auto-upload-bridge": "media-generation",
}

STANDARD_BUNDLE_MAX_SKILLS = 40

# Reference packs are recommendations only: install-suite.sh covers their domains.
# Trading skills moved to the finance-investment-standard suite; the design
# animation pack stays as the single optional reference pack.
STANDARD_BUNDLE_PACKS = [
    {
        "capability": "design-animation-pack",
        "pack": "emilkowalski-skills",
        "title": "Emil Kowalski Design & Animation Skills",
        "category": "design-ui",
        "stars": 5,
        "score": 92,
        "access_mode": "direct",
        "conflict_group": "design-pack:emilkowalski-skills",
        "origin_url": "https://github.com/emilkowalski/skills",
        "skills_origin_prefix": "https://github.com/emilkowalski/skills",
        "note": "Design engineering, Apple-style fluid interface principles, animation vocabulary, motion opportunity discovery, UI library selection, animation review, and motion improvement planning. Optional reference pack; install on demand.",
    }
]

CONFLICT_GROUP_RULES = [
    ("web-search", ["web-search", "tavily-search", "brave-search", "multi-search-engine", "minimax-web-search"]),
    ("browser-automation", ["agent-browser", "chrome-devtools-mcp"]),
    ("document-docx", ["docx", "minimax-docx"]),
    ("document-pdf", ["pdf", "nano-pdf", "minimax-pdf"]),
    ("document-pptx", ["pptx", "pptx-generator"]),
    ("spreadsheet-xlsx", ["xlsx", "minimax-xlsx"]),
    ("html-publishing", ["html-anything", "baoyu-markdown-to-html"]),
    ("image-generation", ["ai-image-generation", "gemini-image-service", "baoyu-image-gen"]),
    ("music-generation", ["ai-music-generation", "ai-music-prompts", "minimax-music-gen"]),
    ("email-agent", ["agentmail", "agentmail-cli", "agentmail-mcp", "agentmail-toolkit"]),
    ("ima", ["ima"]),
    ("finance-global-data", ["global-stock-data", "yfinance-data"]),
    ("finance-data", ["a-stock-data", "akshare-stock", "yfinance-data", "funda-data", "tushare-openclaw-skill", "openclaw-stock-data-skill"]),
    ("persistent-memory", ["claude-mem-plugin"]),
]

STANDARD_CAPABILITIES = [
    "agent-method", "skill-discovery", "web-search", "url-extraction", "browser-automation",
    "code-hosting", "terminal", "task-tracking", "planning", "verification", "skill-authoring",
    "security-review", "data-analysis", "docs", "spreadsheet", "slides", "pdf", "frontend",
    "fullstack", "database", "mcp", "media-download", "image-generation", "research-news",
    "article-illustration", "social-research", "html-publishing",
    "finance-data", "finance-global-data", "content-strategy", "writing", "automation-followup", "cost-observability",
    "email-agent", "ima-notes-knowledge",
    "weather",
    "persistent-memory",
]

CAPABILITY_RULES = [
    ("agent-method", ["brainstorming", "using-superpowers"]),
    ("skill-discovery", ["find-skills"]),
    ("web-search", ["tavily-search", "web-search", "multi-search-engine", "minimax-web-search"]),
    ("url-extraction", ["url-to-markdown"]),
    ("browser-automation", ["agent-browser", "chrome-devtools-mcp"]),
    ("code-hosting", ["github"]),
    ("terminal", ["shell"]),
    ("task-tracking", ["todo", "task"]),
    ("planning", ["planning-with-files", "writing-plans"]),
    ("verification", ["verification-before-completion"]),
    ("skill-authoring", ["skill-creator", "writing-skills"]),
    ("security-review", ["skill-vetter", "skill-security-auditor"]),
    ("data-analysis", ["data-analyst", "data-quality-checker"]),
    ("docs", ["docx", "minimax-docx"]),
    ("spreadsheet", ["xlsx", "minimax-xlsx"]),
    ("slides", ["pptx", "pptx-generator"]),
    ("pdf", ["pdf", "nano-pdf"]),
    ("frontend", ["frontend-dev", "generative-ui"]),
    ("fullstack", ["fullstack-dev"]),
    ("database", ["database"]),
    ("mcp", ["mcp-builder"]),
    ("media-download", ["media-downloader"]),
    ("image-generation", ["ai-image-generation", "gemini-image-service"]),
    ("research-news", ["news-radar", "notebooklm-skill"]),
    ("article-illustration", ["ian-xiaohei-illustrations", "baoyu-article-illustrator"]),
    ("social-research", ["agent-reach", "opencli-reader", "twitter-reader", "reddit-reader", "discord-reader", "linkedin-reader"]),
    ("html-publishing", ["html-anything", "baoyu-markdown-to-html"]),
    ("finance-data", ["a-stock-data", "openclaw-stock-data-skill", "tushare-openclaw-skill", "yfinance-data", "akshare-stock"]),
    ("finance-global-data", ["global-stock-data", "yfinance-data"]),
    ("content-strategy", ["content-strategy"]),
    ("writing", ["writing-skills", "baoyu-format-markdown"]),
    ("automation-followup", ["proactive-agent", "openclaw-cron-setup"]),
    ("cost-observability", ["model-usage"]),
    ("email-agent", ["agentmail", "agentmail-mcp", "agentmail-cli", "agentmail-toolkit"]),
    ("ima-notes-knowledge", ["ima"]),
    ("weather", ["weather"]),
    ("persistent-memory", ["claude-mem-plugin"]),
]

API_KEY_PATTERNS = {
    "ALPHAGBM_API_KEY": ["alphagbm"],
    "AGENTMAIL_API_KEY": ["agentmail"],
    "IMA_API_KEY": ["ima"],
    "IMA_CLIENT_ID": ["ima"],
    "LLMQUANT_API_KEY": ["llmquant"],
    "TAVILY_API_KEY": ["tavily"],
    "BRAVE_API_KEY": ["brave"],
    "GITHUB_TOKEN": ["github"],
    "GH_TOKEN": ["github"],
    "GEMINI_API_KEY": ["gemini"],
    "ANTHROPIC_API_KEY": ["claude-mem", "anthropic"],
    "OPENROUTER_API_KEY": ["claude-mem", "openrouter"],
    "FMP_API_KEY": ["fmp", "earnings-calendar", "economic-calendar"],
    "OPENAI_API_KEY": ["openai", "ai-image", "inference", "deepseek", "llm"],
    "TUSHARE_TOKEN": ["tushare"],
    "STOCK_API_KEY": ["stock_api_key", "data.diemeng", "diemeng"],
}

# Keys accepted inside the two bundles: mainstream LLM providers and standard
# developer tooling tokens. Everything else is a third-party registration key
# and bundles should avoid it whenever a keyless alternative exists.
LLM_API_KEYS = {
    "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY",
    "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY", "QWEN_API_KEY", "DASHSCOPE_API_KEY",
    "MINIMAX_API_KEY", "ZHIPU_API_KEY", "GLM_API_KEY", "BIGMODEL_API_KEY",
    "TOGETHER_API_KEY", "GROQ_API_KEY", "XAI_API_KEY",
}
TOOL_TOKEN_EXEMPT = {"GITHUB_TOKEN", "GH_TOKEN"}
# Runtime-generated secrets that never require external registration.
SELF_GENERATED_SECRETS = {"JWT_SECRET", "SECRET_KEY"}


def is_third_party_api_key(api_keys: list[str]) -> bool:
    return any(key not in LLM_API_KEYS and key not in TOOL_TOKEN_EXEMPT for key in api_keys)

TOOL_PATTERNS = {
    "browser": ["browser", "chrome", "web", "html-anything"],
    "mcp": ["mcp"],
    "node": ["frontend", "fullstack", "react", "pptx", "xlsx", "next", "html-anything"],
    "python": ["data", "finance", "stock", "analyst", "yfinance", "akshare"],
    "ffmpeg": ["video", "gif", "music", "audio"],
    "gh": ["github"],
}


def norm(text: str) -> str:
    return " ".join((text or "").split())


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(skill_id: str) -> dict[str, Any]:
    path = ROOT / "skills" / "default" / skill_id / "SKILL.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, Any] = {}
    lines = parts[1].splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if ":" not in line or line.startswith(" "):
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {"|", ">"}:
            block = []
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if next_line and not next_line.startswith((" ", "\t")):
                    break
                block.append(next_line.strip())
                index += 1
            data[key] = norm(" ".join(block))
            continue
        data[key] = value.strip('"')
        index += 1
    return data


def dedupe_default_skills() -> list[dict[str, Any]]:
    data = load_json(DEFAULT_CATALOG, {})
    by_id: dict[str, dict[str, Any]] = {}
    tier_membership: dict[str, list[str]] = defaultdict(list)
    for tier in ("low", "medium", "high"):
        for item in data.get("tiers", {}).get(tier, {}).get("skills", []):
            skill_id = item["id"]
            by_id.setdefault(skill_id, dict(item))
            tier_membership[skill_id].append(tier)
    for skill_id, item in by_id.items():
        item["install_tiers"] = tier_membership[skill_id]
    return [by_id[k] for k in sorted(by_id)]


def detect_native_origin(
    skill_id: str,
    item: dict[str, Any],
    overrides: dict[str, str],
    preset_exclusions: set[str],
    previous_origins: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    mirror = item.get("source", "")
    if skill_id in preset_exclusions:
        origin = {
            "origin_url": None,
            "origin_type": "agent-preset",
            "origin_confidence": "agent_preset_excluded",
            "origin_verified_at": TODAY,
            "mirror_source_url": mirror,
            "needs_origin_review": False,
            "excluded_reason": "Provided by target agent runtime; not installed from this registry.",
        }
    elif skill_id in overrides:
        url = overrides[skill_id]
        if "github.com" in url:
            origin_type = "github"
        elif "npmjs.com" in url:
            origin_type = "npm"
        elif "claw" in url.lower():
            origin_type = "clawhub"
        else:
            origin_type = "website"
        origin = {
            "origin_url": url,
            "origin_type": origin_type,
            "origin_confidence": "verified_override",
            "origin_verified_at": TODAY,
            "mirror_source_url": mirror,
            "needs_origin_review": False,
        }
    else:
        local_urls = extract_local_urls(skill_id)
        if local_urls:
            url = local_urls[0]
            origin = {
                "origin_url": url,
                "origin_type": "github" if "github.com" in url else "website",
                "origin_confidence": "local_reference",
                "origin_verified_at": TODAY,
                "mirror_source_url": mirror,
                "needs_origin_review": False,
            }
        else:
            origin = {
                "origin_url": None,
                "origin_type": None,
                "origin_confidence": "missing",
                "origin_verified_at": None,
                "mirror_source_url": mirror,
                "needs_origin_review": True,
                "source_is_mirror": bool(MIRROR_PATTERN.search(mirror)),
            }

    previous = previous_origins.get(skill_id, {})
    identity_fields = (
        "origin_url",
        "origin_type",
        "origin_confidence",
        "needs_origin_review",
    )
    if previous and all(previous.get(key) == origin.get(key) for key in identity_fields):
        origin["origin_verified_at"] = previous.get("origin_verified_at")
    return origin


def extract_local_urls(skill_id: str) -> list[str]:
    base = ROOT / "skills" / "default" / skill_id
    urls: list[str] = []
    for name in ("SKILL.md", "README.md", "GUIDE.md"):
        path = base / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for url in re.findall(r"https://[^\s)\]>'\"]+", text):
            clean = url.rstrip(".,;:")
            if not any(host in clean for host in ("github.com", "skills.h")):
                continue
            lower = clean.lower()
            if any(bad in lower for bad in ("google.com/search", "api/skills/bitcoin-tracker", "suspicious-skill", "example", "localhost", "{", "}", "`")):
                continue
            if "github.com" in lower and not any(token in lower for token in (skill_id.lower(), "/skills/", "minimax-ai/skills", "anthropics/skills", "baoyu-skills", "opc-skills")):
                continue
            urls.append(clean)
    unique = []
    for url in urls:
        if url not in unique and "leecyno1/auto-install-Openclaw" not in url:
            unique.append(url)
    return unique


def classify_category(skill_id: str, description: str) -> str:
    if skill_id in ALPHAGBM_SKILLS:
        return "finance-monitor" if skill_id in ALPHAGBM_MONITOR_SKILLS else "finance-trading"
    if skill_id.startswith("llmquant-"):
        return LLMQUANT_SKILL_CATEGORIES.get(skill_id, "finance-trading")
    if skill_id.startswith("anthropic-fs-"):
        for plugin, category in ANTHROPIC_FS_PLUGIN_CATEGORIES.items():
            if skill_id.startswith(f"anthropic-fs-{plugin}-"):
                return category
        return "finance-services"
    if skill_id in TASTE_SKILLS:
        return "design-ui"
    if skill_id in ACCOUNT_LAUNCH_SKILLS:
        return "marketing-growth"
    if skill_id in WORKBUDDY_XHS_SKILLS:
        return "marketing-growth"
    if skill_id in SERENITY_SKILLS:
        return "finance-trading"
    if skill_id in EMIL_KOWALSKI_SKILLS:
        return "design-ui"
    if skill_id in GSAP_SKILLS:
        return "design-ui"
    if skill_id in DAY1GLOBAL_SKILLS:
        return "finance-trading"
    if skill_id in DASHENG_MEDIA_WORKFLOW_CATEGORIES:
        return DASHENG_MEDIA_WORKFLOW_CATEGORIES[skill_id]
    explicit = {
        "a-stock-data": "finance-data",
        "behavior-validator": "coding-devtools",
        "agent-reach": "search-research",
        "akshare-stock": "finance-data",
        "funda-data": "finance-data",
        "global-stock-data": "finance-data",
        "openclaw-stock-data-skill": "finance-data",
        "tushare-openclaw-skill": "finance-data",
        "westockdata": "finance-data",
        "uzi-skill": "finance-trading",
        "yfinance-data": "finance-data",
        "openclaw-stock-kb": "finance-knowledge",
        "stock-monitor-skill": "finance-monitor",
        "stock-daily-analysis-skill": "finance-trading",
        "stock-analysis": "finance-trading",
        "pybroker-backtest-skill": "finance-trading",
        "policy-monitor": "policy-monitoring",
        "scroll-world": "design-ui",
        "skill-vetter": "security-audit",
        "claude-mem-plugin": "memory-context",
        "html-anything": "html-publishing",
        "ima": "productivity-pkm",
        "guizang-ppt-skill": "html-publishing",
        "khazix-skills": "writing-content",
        "humanizer-zh": "writing-content",
        "dbskill": "marketing-growth",
        "eigenflux": "agent-orchestration",
        "guizang-social-card-skill": "media-generation",
        "ian-xiaohei-illustrations": "media-generation",
        "content-strategy": "marketing-growth",
        "marketingskills": "marketing-growth",
        "frontend-dev": "coding-devtools",
        "ios-application-dev": "coding-devtools",
        "generative-ui": "design-ui",
        "impeccable": "design-ui",
        "video-autopilot-kit": "media-generation",
        "video-shotcraft": "media-generation",
        "paper-framework-figure-studio-pro": "media-generation",
        "scientific-illustrator": "media-generation",
        "media-downloader": "media-generation",
        "minimax-pdf": "docs-office",
        "vision-analysis": "media-generation",
        "buddy-sings": "media-generation",
        "gif-sticker-maker": "media-generation",
        "minimax-music-gen": "media-generation",
        "minimax-music-playlist": "media-generation",
        "discord-reader": "search-research",
        "linkedin-reader": "search-research",
        "opencli-reader": "search-research",
        "telegram-reader": "search-research",
        "twitter-reader": "search-research",
        "yc-reader": "search-research",
        "startup-analysis": "commerce-ops",
    }
    if skill_id in explicit:
        return explicit[skill_id]
    haystack = f"{skill_id} {description}".lower()
    if skill_id in L1 or skill_id in {"task", "todo", "model-usage"}:
        return "core-agent"
    for category, keywords in CATEGORY_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "commerce-ops"


def classify_horizontal(skill_id: str, category: str, origin_confidence: str) -> str:
    if skill_id in ALPHAGBM_SKILLS:
        return "L3 Specialist"
    if skill_id.startswith("llmquant-"):
        return "L2 Professional"
    if skill_id.startswith("anthropic-fs-"):
        return "L3 Specialist"
    if skill_id in L1:
        return "L1 Foundation"
    if skill_id in L2_HINTS or category in {"coding-devtools", "data-analysis", "docs-office", "search-research", "design-ui", "finance-data", "finance-knowledge"}:
        return "L2 Professional"
    if origin_confidence == "missing":
        return "L3 Specialist"
    return "L3 Specialist"


def infer_dependencies(skill_id: str, description: str, existing_keys: list[str]) -> dict[str, Any]:
    haystack = f"{skill_id} {description}".lower()
    api_keys = [key for key in existing_keys if key not in SELF_GENERATED_SECRETS]
    for key, patterns in API_KEY_PATTERNS.items():
        if key in api_keys:
            continue
        # Word-boundary matching: bare substrings like "ima" would otherwise
        # match "image"/"minimal" and mislabel skills with foreign keys.
        if any(re.search(rf"\b{re.escape(pattern)}\b", haystack) for pattern in patterns):
            api_keys.append(key)
    tools = []
    for tool, patterns in TOOL_PATTERNS.items():
        if any(pattern in haystack for pattern in patterns):
            tools.append(tool)
    if skill_id.startswith("llmquant-"):
        api_keys = ["LLMQUANT_API_KEY"]
        tools = ["mcp", "node"]
    if skill_id.startswith("anthropic-fs-"):
        api_keys = []
        tools = sorted(set(tools + ["mcp"]))
    if skill_id == "seedance2-skill":
        tools = []
    if skill_id == "html-anything":
        tools = ["browser", "node"]
    if skill_id == "generative-ui":
        api_keys = []
        tools = []
    if skill_id in TASTE_SKILLS:
        api_keys = []
        tools = []
    if skill_id in ACCOUNT_LAUNCH_SKILLS:
        api_keys = []
        tools = []
    if skill_id in WORKBUDDY_XHS_SKILLS:
        api_keys = []
        tools = []
    if skill_id in SERENITY_SKILLS:
        api_keys = []
        tools = sorted(set(tools + ["python"]))
    if skill_id in EMIL_KOWALSKI_SKILLS:
        api_keys = []
        tools = []
    if skill_id in GSAP_SKILLS:
        api_keys = []
        tools = ["node"]
    if skill_id in DAY1GLOBAL_SKILLS:
        api_keys = []
        tools = ["browser"]
    if skill_id in ALPHAGBM_SKILLS:
        api_keys = ["ALPHAGBM_API_KEY"]
        tools = ["curl"]
    if skill_id == "impeccable":
        api_keys = []
        tools = ["browser", "node"]
    if skill_id == "video-shotcraft":
        api_keys = []
        tools = ["browser", "ffmpeg", "node"]
    if skill_id == "video-autopilot-kit":
        api_keys = []
        tools = ["ffmpeg", "python"]
    if skill_id == "dasheng-video-omni-browser":
        api_keys = []
        tools = ["browser", "python"]
    if skill_id == "dasheng-vox-skills":
        api_keys = []
        tools = ["browser", "ffmpeg", "node", "python"]
    if skill_id == "paper-framework-figure-studio-pro":
        api_keys = []
        tools = ["python"]
    if skill_id == "scientific-illustrator":
        api_keys = []
        tools = ["drawio", "mcp", "node", "python"]
    if skill_id == "eigenflux":
        api_keys = []
        tools = ["eigenflux", "mcp", "node"]
    if skill_id == "westockdata":
        api_keys = []
        tools = ["node"]
    if skill_id == "uzi-skill":
        api_keys = []
        tools = ["browser", "python"]
    if skill_id == "scroll-world":
        api_keys = []
        tools = ["ffmpeg", "higgsfield", "python"]
    if skill_id == "agent-reach":
        api_keys = []
        tools = ["browser", "ffmpeg", "gh"]
    if skill_id in DASHENG_MEDIA_WORKFLOW_CATEGORIES:
        api_keys = []
        if skill_id in {
            "bilibili-upload-bridge",
            "dasheng-html-video-bridge",
            "dasheng-video-explainer-html",
            "dasheng-video-roughcut",
            "dasheng-video-talking-head",
            "dasheng-xhs-publish-bridge",
            "social-auto-upload-bridge",
        }:
            tools = sorted(set(tools + ["node"]))
        elif skill_id == "dasheng-video-omni-browser":
            tools = ["browser", "python"]
        elif skill_id == "dasheng-vox-skills":
            tools = ["browser", "ffmpeg", "node", "python"]
        elif skill_id in {"dasheng-finance-data", "dasheng-hotspot-radar", "feishu-doc-creator"}:
            tools = sorted(set(tools + ["python"]))
        else:
            tools = []
    tools = sorted(set(tools))
    if api_keys and "mcp" in tools:
        access_mode = "api-key+mcp-required"
    elif api_keys:
        access_mode = "api-key"
    elif "mcp" in tools:
        access_mode = "mcp-required"
    elif "browser" in tools:
        access_mode = "browser-required"
    else:
        access_mode = "direct"
    runtime = "online" if api_keys or skill_id == "scroll-world" or skill_id in DAY1GLOBAL_SKILLS or any(word in haystack for word in ["web", "api", "search", "reader", "news"]) else "offline"
    if skill_id == "scientific-illustrator":
        runtime = "offline"
    if skill_id == "eigenflux":
        runtime = "online"
    if skill_id == "uzi-skill":
        runtime = "online"
    return {
        "requires_api_keys": bool(api_keys),
        "api_keys": sorted(api_keys),
        "required_tools": tools,
        "access_mode": access_mode,
        "runtime": runtime,
    }


def conflict_group(skill_id: str, category: str) -> str:
    for group, ids in CONFLICT_GROUP_RULES:
        if skill_id in ids:
            return group
    if category == "finance-trading":
        return f"finance-specialist:{skill_id}"
    return skill_id


def risk_level(skill_id: str, deps: dict[str, Any], category: str) -> str:
    if skill_id == "claude-mem-plugin":
        return "high"
    if skill_id == "eigenflux":
        return "high"
    if skill_id == "html-anything":
        return "medium"
    if skill_id == "paper-framework-figure-studio-pro":
        return "medium"
    if any(token in skill_id for token in ["danger", "shell"]):
        return "high"
    if deps["access_mode"] in {"api-key", "api-key+mcp-required", "mcp-required", "browser-required"}:
        return "medium"
    if category in {"finance-trading", "finance-services", "finance-data", "finance-monitor", "policy-monitoring", "legal-compliance", "devops-cloud"}:
        return "medium"
    return "low"


def score_item(item: dict[str, Any]) -> dict[str, Any]:
    score = 30
    confidence = item["origin"]["origin_confidence"]
    if confidence == "verified_override":
        score += 25
    elif confidence == "local_reference":
        score += 15
    else:
        score -= 20
    if item["horizontal_tier"].startswith("L1"):
        score += 20
    elif item["horizontal_tier"].startswith("L2"):
        score += 12
    else:
        score += 5
    if item["risk_level"] == "low":
        score += 10
    elif item["risk_level"] == "medium":
        score += 4
    else:
        score -= 8
    if item["dependencies"]["access_mode"] == "direct":
        score += 8
    elif item["dependencies"]["access_mode"] in {"browser-required", "mcp-required", "api-key+mcp-required"}:
        score += 3
    if item["description"] and item["description"] != "No description.":
        score += 7
    if item["id"] == "claude-mem-plugin":
        score += 35
    if item["id"] == "html-anything":
        score += 15
    if item["preset_excluded"]:
        score -= 100
    if confidence == "missing":
        score = min(score, 45)
    if item["id"] in EDITORIAL_SCORE_OVERRIDES:
        score = EDITORIAL_SCORE_OVERRIDES[item["id"]]
    if item["id"] in ALPHAGBM_SKILLS:
        score = 82
    score = max(0, min(100, score))
    stars = 5 if score >= 90 else 4 if score >= 75 else 3 if score >= 60 else 2 if score >= 40 else 1
    return {"score": score, "stars": stars, "rating_label": "★" * stars + "☆" * (5 - stars)}


def load_preset_exclusions() -> set[str]:
    excluded = set()
    for path in PRESETS_DIR.glob("*.json"):
        data = load_json(path, {})
        excluded.update(data.get("preset_skills", []))
    return excluded


def load_suites() -> list[dict[str, Any]]:
    suites = []
    if not SUITES_DIR.exists():
        return suites
    for path in sorted(SUITES_DIR.glob("*.json")):
        suite = load_json(path, {})
        if not suite.get("id"):
            continue
        suite["skill_count"] = len(suite.get("skills", []))
        suites.append(suite)
    return suites


def build_enriched() -> dict[str, Any]:
    overrides = load_json(ORIGIN_OVERRIDES, {})
    previous_catalog = load_json(ENRICHED_PATH, {})
    previous_origins = {
        item["id"]: item.get("origin", {})
        for item in previous_catalog.get("skills", [])
        if item.get("id")
    }
    preset_exclusions = load_preset_exclusions()
    tushare_routing = load_json(TUSHARE_ROUTING, {})
    tushare_backed = {item.get("skill_id") for item in tushare_routing.get("convert_to_tushare_backed", [])}
    tushare_supplement = {item.get("skill_id") for item in tushare_routing.get("tushare_supplement_only", [])}
    skills = []
    for base in dedupe_default_skills():
        skill_id = base["id"]
        frontmatter = parse_frontmatter(skill_id)
        description = norm(frontmatter.get("description") or base.get("description") or "No description.")
        origin = detect_native_origin(skill_id, base, overrides, preset_exclusions, previous_origins)
        category = classify_category(skill_id, description)
        horizontal = classify_horizontal(skill_id, category, origin["origin_confidence"])
        deps = infer_dependencies(skill_id, description, base.get("api_keys", []))
        tags = [category, horizontal.split()[0].lower(), deps["access_mode"], deps["runtime"]]
        tags.extend(base.get("groups", []) or [])
        if skill_id.startswith("llmquant-"):
            tags.extend(["llmquant", "institutional-research", "finance-suite"])
        if skill_id.startswith("anthropic-fs-"):
            tags.extend(["anthropic-financial-services", "enterprise-data", "institutional-finance", "finance-suite"])
        if skill_id in EMIL_KOWALSKI_SKILLS:
            tags.extend(["emil-kowalski", "design-animation-suite", "frontend-craft"])
        if skill_id in GSAP_SKILLS:
            tags.extend(["greensock", "gsap-skills", "design-animation-suite", "frontend-craft"])
        if skill_id in DAY1GLOBAL_SKILLS:
            tags.extend(["day1global-skills", "finance-suite", "investment-research"])
        if skill_id in ALPHAGBM_SKILLS:
            tags.extend(["alphagbm", "finance-suite", "options-research", "api-backed"])
        if skill_id == "uzi-skill":
            tags.extend(["uzi-skill", "finance-suite", "a-share", "equity-research", "report-generation"])
        if skill_id in tushare_backed:
            tags.extend(["tushare-backed", "china-market-data"])
            if "TUSHARE_TOKEN" not in deps["api_keys"]:
                deps["api_keys"].append("TUSHARE_TOKEN")
                deps["api_keys"] = sorted(set(deps["api_keys"]))
                deps["requires_api_keys"] = True
                deps["access_mode"] = "api-key" if deps["access_mode"] == "direct" else deps["access_mode"]
        if skill_id in tushare_supplement:
            tags.extend(["tushare-supplement", "china-market-data"])
        if skill_id in DASHENG_MEDIA_WORKFLOW_CATEGORIES:
            tags.extend(["dasheng-media-workflow", "self-media-ops"])
        item = {
            "id": skill_id,
            "name": base.get("name", skill_id),
            "description": description,
            "manual": base.get("manual"),
            "manual_url": base.get("manual_url"),
            "install_tiers": base.get("install_tiers", []),
            "origin": origin,
            "horizontal_tier": horizontal,
            "primary_category": category,
            "category_label": CATEGORY_LABELS[category],
            "tags": sorted(set(tags)),
            "dependencies": deps,
            "risk_level": risk_level(skill_id, deps, category),
            "conflict_group": conflict_group(skill_id, category),
            "preset_excluded": skill_id in preset_exclusions,
        }
        item["rating"] = score_item(item)
        skills.append(item)
    return {
        "schema_version": "2026.05.17",
        "generated_at": TODAY,
        "source_catalog": "catalog/default-skills.json",
        "policy": {
            "native_origin_required": True,
            "mirror_sources_are_not_native": True,
            "missing_origin_max_stars": 2,
            "standard_bundle_max_skills": STANDARD_BUNDLE_MAX_SKILLS,
            "preset_excluded_agents": [p.stem for p in sorted(PRESETS_DIR.glob("*.json"))],
        },
        "summary": summarize(skills),
        "skills": sorted(skills, key=lambda x: (-x["rating"]["score"], x["id"])),
    }


def summarize(skills: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "skills": len(skills),
        "native_origin_verified_or_referenced": sum(not s["origin"].get("needs_origin_review") and not s.get("preset_excluded") for s in skills),
        "native_origin_excluded_presets": sum(s.get("preset_excluded") for s in skills),
        "needs_origin_review": sum(s["origin"].get("needs_origin_review", False) for s in skills),
        "preset_excluded": sum(s["preset_excluded"] for s in skills),
        "by_horizontal_tier": dict(sorted(counter(skills, "horizontal_tier").items())),
        "by_category": dict(sorted(counter(skills, "primary_category").items())),
        "by_access_mode": dict(sorted(counter(skills, lambda s: s["dependencies"]["access_mode"]).items())),
        "by_stars": dict(sorted(counter(skills, lambda s: f"{s['rating']['stars']}★").items())),
    }


def counter(skills: list[dict[str, Any]], key: str | Any) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for item in skills:
        value = item[key] if isinstance(key, str) else key(item)
        out[str(value)] += 1
    return dict(out)


def build_standard_bundle(enriched: dict[str, Any]) -> dict[str, Any]:
    by_id = {s["id"]: s for s in enriched["skills"] if not s["preset_excluded"]}
    overrides = load_json(STANDARD_BUNDLE_OVERRIDES, {})
    pinned = overrides.get("pinned_capabilities", {}) or {}
    excluded = set((overrides.get("excluded_skills", {}) or {}).keys())
    selected = []
    selected_conflicts = set()
    skipped_no_keyless = []
    for capability, candidates in CAPABILITY_RULES:
        choices = [by_id[c] for c in candidates if c in by_id]
        choices = [c for c in choices if c["id"] not in excluded]
        choices = [c for c in choices if c["conflict_group"] not in selected_conflicts]
        if not choices:
            continue
        # Bundle policy: no third-party registration keys. LLM keys and
        # developer tool tokens are exempt; when every candidate needs one,
        # the capability is skipped rather than forcing a signup on users.
        keyless = [c for c in choices if not is_third_party_api_key(c["dependencies"]["api_keys"])]
        if not keyless:
            skipped_no_keyless.append(capability)
            continue
        choices = keyless
        pinned_skill = pinned.get(capability)
        pinned_choices = [choice for choice in choices if choice["id"] == pinned_skill]
        best = pinned_choices[0] if pinned_choices else sorted(choices, key=lambda s: (-s["rating"]["score"], risk_sort(s["risk_level"]), s["id"]))[0]
        selected.append({
            "capability": capability,
            "skill": best["id"],
            "category": best["primary_category"],
            "stars": best["rating"]["stars"],
            "score": best["rating"]["score"],
            "access_mode": best["dependencies"]["access_mode"],
            "conflict_group": best["conflict_group"],
            "origin_url": best["origin"].get("origin_url"),
            "note": best["description"],
        })
        selected_conflicts.add(best["conflict_group"])
        if len(selected) >= STANDARD_BUNDLE_MAX_SKILLS:
            break
    skill_packs = []
    for pack in STANDARD_BUNDLE_PACKS:
        pack_skills = sorted([
            skill["id"]
            for skill in enriched["skills"]
            if (skill.get("origin", {}).get("origin_url") or "").startswith(pack["skills_origin_prefix"])
            and not skill.get("preset_excluded")
        ])
        skill_packs.append({
            "capability": pack["capability"],
            "pack": pack["pack"],
            "title": pack["title"],
            "category": pack["category"],
            "stars": pack["stars"],
            "score": pack["score"],
            "access_mode": pack["access_mode"],
            "conflict_group": pack["conflict_group"],
            "origin_url": pack["origin_url"],
            "note": pack["note"],
            "skills": pack_skills,
        })
    return {
        "schema_version": enriched["schema_version"],
        "generated_at": TODAY,
        "max_skills": STANDARD_BUNDLE_MAX_SKILLS,
        "dedupe_rule": "one highest-scored skill per capability and conflict_group; base skills only (packs are reference recommendations); Open/Hermes preset skills excluded; third-party API-key skills excluded (LLM keys and GitHub tokens exempt)",
        "api_key_policy": {
            "exempt_keys": sorted(LLM_API_KEYS | TOOL_TOKEN_EXEMPT),
            "skipped_capabilities_no_keyless_candidate": sorted(skipped_no_keyless),
        },
        "overrides": {
            "pinned_capabilities": pinned,
            "excluded_skills": sorted(excluded),
        },
        "skill_packs": skill_packs,
        "skills": selected,
    }


def risk_sort(risk: str) -> int:
    return {"low": 0, "medium": 1, "high": 2}.get(risk, 3)


def md_link(url: str | None, label: str = "origin") -> str:
    return f"[{label}]({url})" if url else "待补"


def render_horizontal_index(skills: list[dict[str, Any]]) -> str:
    grouped = defaultdict(list)
    for item in skills:
        grouped[item["horizontal_tier"]].append(item)
    lines = ["# 横向分级索引", "", "| 层级 | 定义 | 数量 |", "|---|---|---:|"]
    definitions = {
        "L1 Foundation": "跨 Agent、跨领域、高通用、低冲突的基础能力",
        "L2 Professional": "常用专业工作流，适合多数生产环境按需安装",
        "L3 Specialist": "领域强绑定、依赖明显或适合专家场景的能力",
    }
    for tier in ["L1 Foundation", "L2 Professional", "L3 Specialist"]:
        lines.append(f"| `{tier}` | {definitions[tier]} | {len(grouped[tier])} |")
    for tier in ["L1 Foundation", "L2 Professional", "L3 Specialist"]:
        lines += ["", f"## {tier}", "", "| Skill | 类型 | 星级 | 使用条件 | 原生来源 |", "|---|---|---:|---|---|"]
        for item in sorted(grouped[tier], key=lambda s: (-s["rating"]["score"], s["id"])):
            lines.append(f"| `{item['id']}` | {item['category_label']} | {item['rating']['stars']}★ | `{item['dependencies']['access_mode']}` | {md_link(item['origin']['origin_url'])} |")
    return "\n".join(lines) + "\n"


def render_type_index(skills: list[dict[str, Any]]) -> str:
    grouped = defaultdict(list)
    for item in skills:
        grouped[item["primary_category"]].append(item)
    lines = ["# 纵向类型索引", "", "| 类型 | 数量 |", "|---|---:|"]
    for category, label in CATEGORY_LABELS.items():
        lines.append(f"| {label} (`{category}`) | {len(grouped[category])} |")
    for category, label in CATEGORY_LABELS.items():
        if not grouped[category]:
            continue
        lines += ["", f"## {label}", "", "| Skill | 横向层级 | 星级 | 标签 |", "|---|---|---:|---|"]
        for item in sorted(grouped[category], key=lambda s: (-s["rating"]["score"], s["id"])):
            lines.append(f"| `{item['id']}` | `{item['horizontal_tier']}` | {item['rating']['stars']}★ | {', '.join(f'`{tag}`' for tag in item['tags'])} |")
    return "\n".join(lines) + "\n"


def render_dependency_index(skills: list[dict[str, Any]]) -> str:
    grouped = defaultdict(list)
    for item in skills:
        grouped[item["dependencies"]["access_mode"]].append(item)
    lines = ["# 使用条件索引", "", "| 使用条件 | 数量 |", "|---|---:|"]
    for mode in sorted(grouped):
        lines.append(f"| `{mode}` | {len(grouped[mode])} |")
    for mode in sorted(grouped):
        lines += ["", f"## {mode}", "", "| Skill | API Key | Tools | 风险 |", "|---|---|---|---|"]
        for item in sorted(grouped[mode], key=lambda s: (-s["rating"]["score"], s["id"])):
            keys = ", ".join(f"`{k}`" for k in item["dependencies"]["api_keys"]) or "无"
            tools = ", ".join(f"`{t}`" for t in item["dependencies"]["required_tools"]) or "无"
            lines.append(f"| `{item['id']}` | {keys} | {tools} | `{item['risk_level']}` |")
    return "\n".join(lines) + "\n"


def render_scoring_model() -> str:
    return """# 评分体系

五星标签由 100 分综合评分映射而来：

| 分数 | 星级 |
|---:|---:|
| 90-100 | 5★ |
| 75-89 | 4★ |
| 60-74 | 3★ |
| 40-59 | 2★ |
| 0-39 | 1★ |

## 当前评分因子

| 因子 | 权重/规则 |
|---|---|
| 原生来源可信度 | verified override +25，本地引用 +15，缺失 -20 |
| 横向通用性 | L1 +20，L2 +12，L3 +5 |
| 风险 | low +10，medium +4，high -8 |
| 使用门槛 | direct +8，browser/mcp +3 |
| 文档描述 | 有描述 +7 |
| 预置排除 | Open/Hermes 已预置的 skill 不进入标准配置组 |

## 后续月评增强

月评任务应补充 GitHub stars/forks/release、ClawHub/CL.Up rating/downloads、skills.h 热度与更新时间。没有可验证原生来源的 skill，即使本地可用，最高只能评为 2★。
"""


def readme_origin(item: dict[str, Any]) -> str:
    if item["preset_excluded"]:
        return "Preset"
    return md_link(item["origin"].get("origin_url"), "Source")


def pluralize_count(count: int, singular: str) -> str:
    suffix = "" if count == 1 else "s"
    return f"{count} {singular}{suffix}"


def bundle_size_label(bundle: dict[str, Any]) -> str:
    label = pluralize_count(len(bundle["skills"]), "skill")
    pack_count = len(bundle.get("skill_packs", []))
    if pack_count:
        label += f" + {pluralize_count(pack_count, 'pack')}"
    return label


def render_badges(summary: dict[str, Any], bundle: dict[str, Any]) -> str:
    bundle_badge_label = bundle_size_label(bundle).replace(" ", "%20").replace("+", "%2B")
    badges = [
        "[![Project](https://img.shields.io/badge/Project-Page-2b6cb0)](#boutique-skills)",
        f"[![Skills](https://img.shields.io/badge/Skills-{summary['skills']}-2ea44f)](#all-skills)",
        "[![Native Origins](https://img.shields.io/badge/Native%20Origins-0%20missing-brightgreen)](docs/UPDATE_AND_AUDIT.md)",
        f"[![Standard Bundle](https://img.shields.io/badge/Standard%20Bundle-{bundle_badge_label}-7c3aed)](catalog/standard-bundle.json)",
        "[![Technique](https://img.shields.io/badge/Technique-Source%20Audited-f97316)](docs/generated/scoring-model.md)",
        "[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)",
    ]
    return "\n".join(badges)


def render_tech_stack_badges() -> str:
    return "\n".join([
        '<p align="center">',
        '  <img src="https://skillicons.dev/icons?i=python,fastapi,pydantic,postgres,redis,docker,githubactions&theme=dark" alt="Core technology stack" />',
        '</p>',
        '<p align="center">',
        '  <img src="https://img.shields.io/badge/OpenAI-Model%20Support-111827?logo=openai&logoColor=white" alt="OpenAI" />',
        '  <img src="https://img.shields.io/badge/Anthropic-Claude%20Ready-111827" alt="Anthropic" />',
        '  <img src="https://img.shields.io/badge/ModelScope-Model%20Ecosystem-111827" alt="ModelScope" />',
        '  <img src="https://img.shields.io/badge/UV-Python%20Packaging-111827" alt="UV" />',
        '  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-111827" alt="SQLAlchemy" />',
        '</p>',
    ])


def render_stats(summary: dict[str, Any], bundle: dict[str, Any], suites: list[dict[str, Any]]) -> str:
    return "\n".join([
        "| Metric | Value |",
        "|---|---:|",
        f"| Curated skills | {summary['skills']} |",
        f"| Skill suites | {len(suites)} |",
        f"| Native sources verified or referenced | {summary['native_origin_verified_or_referenced']} |",
        f"| Agent preset exclusions | {summary['preset_excluded']} |",
        f"| Missing native origins | {summary['needs_origin_review']} |",
        f"| Standard bundle size | {bundle_size_label(bundle)} |",
    ])


def render_all_skills_table(skills: list[dict[str, Any]]) -> str:
    lines = [
        "| Skill | Tier | Type | Stars | Use | Origin |",
        "|---|---|---|---:|---|---|",
    ]
    for item in sorted(skills, key=lambda s: (s["primary_category"], s["id"])):
        lines.append(
            f"| `{item['id']}` | `{item['horizontal_tier']}` | `{item['primary_category']}` | "
            f"{item['rating']['stars']}★ | `{item['dependencies']['access_mode']}` | {readme_origin(item)} |"
        )
    return "\n".join(lines)


def render_standard_bundle_table(bundle: dict[str, Any]) -> str:
    lines = [
        "| Type | Capability | Skill / Pack | Stars | Use |",
        "|---|---|---|---:|---|",
    ]
    for item in bundle["skills"]:
        lines.append(f"| `skill` | `{item['capability']}` | `{item['skill']}` | {item['stars']}★ | `{item['access_mode']}` |")
    for pack in bundle.get("skill_packs", []):
        lines.append(
            f"| `pack` | `{pack['capability']}` | "
            f"[{pack['title']}]({pack['origin_url']}) | {pack['stars']}★ | `{pack['access_mode']}` |"
        )
    return "\n".join(lines)


def render_suites_table(suites: list[dict[str, Any]]) -> str:
    if not suites:
        return "No grouped suites yet."
    lines = [
        "| Suite | Skills | Tier | Category | Requirements | Install |",
        "|---|---:|---|---|---|---|",
    ]
    for suite in suites:
        requirements = []
        api_keys = suite.get("api_keys", []) or []
        tools = suite.get("requires_tools", []) or []
        if api_keys:
            requirements.append("API: " + ", ".join(f"`{key}`" for key in api_keys))
        if tools:
            requirements.append("Tools: " + ", ".join(f"`{tool}`" for tool in tools))
        requirement_text = "<br>".join(requirements) or "`direct`"
        title = md_link(suite.get("source") or suite.get("native_origin"), suite.get("title") or suite["id"])
        lines.append(
            f"| {title} | {suite.get('skill_count', len(suite.get('skills', [])))} | "
            f"`{suite.get('install_tier', '-')}` | `{suite.get('category', '-')}` | "
            f"{requirement_text} | `./scripts/install-suite.sh {suite['id']}` |"
        )
    return "\n".join(lines)


def finance_source_pack_rows(suite: dict[str, Any] | None) -> list[dict[str, str]]:
    if not suite:
        return []
    source_rows = suite.get("included_sources", []) or []
    if not source_rows:
        return []
    family_labels = {
        "llmquant": "LLMQuant",
        "claude-trading-skills": "Claude Trading Skills",
        "a-stock-data": "A-stock-data",
        "global-stock-data": "Global-stock-data",
        "anthropic-fs": "Anthropic Financial Services",
        "alphaear": "AlphaEar",
        "day1global-skills": "Day1Global Skills",
        "alphagbm": "AlphaGBM",
        "uzi-skill": "UZI Skill",
    }
    family_roles = {
        "llmquant": "SEC/13F/宏观、组合/风险、期权、机构研究",
        "claude-trading-skills": "交易筛选、技术形态、执行计划、监控",
        "a-stock-data": "A 股行情、题材、资金流、公告、新闻",
        "global-stock-data": "美股港股行情、K线、基本面、SEC、期权",
        "anthropic-fs": "机构研究、建模、PE/IB/财富管理",
        "alphaear": "新闻、情绪、信号、报告生成",
        "day1global-skills": "科技股财报、宏观流动性、美股情绪、价值与 BTC 周期",
        "alphagbm": "期权波动率、对冲、市场信号、投资框架与研究档案（可选源）",
        "uzi-skill": "A/港/美股综合研究、模拟评审团、龙虎榜、风险信号与 HTML 报告（可选源）",
    }
    rows = []
    for row in source_rows:
        source_id = row.get("id", "")
        rows.append({
            "type": "组合包",
            "slot": family_roles.get(source_id, "Merged source family"),
            "item": family_labels.get(source_id, source_id),
            "score": str(row.get("score", "-")),
            "source": row.get("source") or row.get("origin") or row.get("source_url") or "",
        })
    return rows


def render_finance_standard_combined_table(suite: dict[str, Any] | None, enriched: dict[str, Any]) -> str:
    if not suite:
        return ""
    skill_sources = {skill["id"]: skill.get("origin", {}).get("origin_url", "") for skill in enriched.get("skills", [])}
    rows = finance_source_pack_rows(suite)
    for row in suite.get("standard_slots", []) or []:
        skill_id = row.get("skill", "")
        rows.append({
            "type": "单品",
            "slot": row.get("slot", ""),
            "item": f"`{skill_id}`",
            "score": str(row.get("score", "-")),
            "source": skill_sources.get(skill_id, ""),
        })
    lines = [
        "| 类型 | 能力位 / 作用 | 标准组合项 | Score | 来源 |",
        "|---|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['type']} | {row['slot']} | {row['item']} | {row['score']} | "
            f"{md_link(row['source'], 'Source') if row['source'] else '-'} |"
        )
    return "\n".join(lines)


def render_finance_entry(enriched: dict[str, Any], suites: list[dict[str, Any]]) -> str:
    finance_skills = [
        item for item in enriched["skills"]
        if item.get("primary_category", "").startswith("finance")
        or item["id"].startswith(("anthropic-fs-", "llmquant-"))
    ]
    category_counts = counter(finance_skills, "primary_category")
    suite_ids = {suite.get("id"): suite for suite in suites}
    finance_standard = suite_ids.get("finance-investment-standard")
    scenario_rows = [
        ("A股数据 / 行情 / 财报", "`a-stock-data`, `akshare-stock`, `tushare-openclaw-skill`", "A 股行情、财务、研报、题材、资金流、公告与自选股数据底座。"),
        ("美股 / 全球股票研究", "`yfinance-data`, `stock-analysis`, `us-stock-analysis`, `llmquant-equities`", "轻量行情与基本面、个股评分、研究 memo、同业比较。"),
        ("每日复盘 / 宏观政策", "`alphaear-news`, `stock-daily-analysis-skill`, `llmquant-macro`, `policy-monitor`", "收盘复盘、政策跟踪、宏观冲击、事件日历。"),
        ("选股 / 机会发现", "`finviz-screener`, `canslim-screener`, `vcp-screener`, `theme-detector`", "成长、价值、股息、主题、VCP/CANSLIM 等候选池构建。"),
        ("技术面 / 交易计划", "`technical-analyst`, `sepa-strategy`, `breakout-trade-planner`, `position-sizer`", "趋势模板、突破计划、止损、仓位与市场健康度。"),
        ("财报 / 事件驱动", "`earnings-preview`, `earnings-recap`, `llmquant-events`, `anthropic-fs-equity-research-earnings-preview`", "财报前预案、财报后复盘、PEAD、催化剂跟踪。"),
        ("组合 / 风控 / 监控", "`stock-monitor-skill`, `trader-memory-core`, `llmquant-portfolio`, `llmquant-risk`", "持仓 thesis、预警、暴露、情景模拟、风险健康度。"),
        ("量化 / 回测 / 策略迭代", "`backtest-expert`, `pybroker-backtest-skill`, `trade-hypothesis-ideator`, `signal-postmortem`", "策略假设、回测、配对/相关性、交易后验复盘。"),
        ("机构金融 / 投行 / PE", "`anthropic-fs-*`, `funda-data`, `llmquant-*`", "投行、PE、固收、KYC、基金运营、机构研究报告与材料。"),
    ]
    lines = [
        "## Finance / Investment Workflows",
        "",
        "Finance skills now have a dedicated **Finance Investment Standard Suite**. It is separate from the general no-duplicate bundle, but it is the recommended standard combination for investment research, screening, trading plans, portfolio risk, monitoring, backtesting, reporting, and institutional finance workflows.",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Finance-related skills | {len(finance_skills)} |",
        f"| Finance investment standard suite | {len(finance_standard.get('skills', [])) if finance_standard else 0} skills |",
        f"| Finance data skills | {category_counts.get('finance-data', 0)} |",
        f"| Finance trading/research skills | {category_counts.get('finance-trading', 0)} |",
        f"| Institutional finance services | {category_counts.get('finance-services', 0)} |",
        f"| Finance monitor/risk skills | {category_counts.get('finance-monitor', 0)} |",
        "",
        "### Finance Investment Standard Suite",
        "",
        "This standard suite lists merged upstream source packs and representative standalone skills together, so the install surface is easy to scan without hiding the single-skill standards.",
        "",
        render_finance_standard_combined_table(finance_standard, enriched),
        "",
        "```bash",
        "./scripts/install-suite.sh finance-investment-standard --dry-run",
        "./scripts/install-suite.sh finance-investment-standard",
        "```",
        "",
        "Full manifest: [catalog/suites/finance-investment-standard.json](catalog/suites/finance-investment-standard.json). Scorecard: [finance investment skills scorecard](reports/finance-skill-eval/finance-investment-skills-scorecard-2026-06-14.md).",
        "",
        "### Recommended Entry Points",
        "",
        "| Need | Start Here |",
        "|---|---|",
        "| 金融投资标准组合 | `./scripts/install-suite.sh finance-investment-standard --dry-run` |",
        "| 普通投资者 / A股研究 | `tushare-openclaw-skill` + `a-stock-data` + `openclaw-stock-kb` + `stock-monitor-skill` |",
        "| 美股与全球资产 | `yfinance-data` + `stock-analysis` + `llmquant-equities` |",
        "| 机构研究 / 多资产 | `./scripts/install-suite.sh llmquant --dry-run` |",
        "| 投行 / PE / 财富管理 / 基金运营 | `./scripts/install-suite.sh anthropic-financial-services --dry-run` |",
        "| 选型参考 | [Finance scenario mapping](docs/generated/finance-skills-mapping.md) |",
        "| Tushare 数据接口评测 | [HTML report](reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.html) |",
        "| Tushare 接入路由清单 | [Routing summary](reports/finance-skill-eval/tushare-eval/tushare-routing-summary.md) |",
        "",
        "### Investment Scenario Mapping",
        "",
        "| Scenario | Matching Skills | What It Covers |",
        "|---|---|---|",
    ]
    for scenario, skills, note in scenario_rows:
        lines.append(f"| {scenario} | {skills} | {note} |")
    lines += [
        "",
        "### Install Examples",
        "",
        "```bash",
        "# Preview the finance profile",
        "./scripts/install-profile.sh finance --dry-run",
        "",
        "# Preview the finance investment standard suite",
        "./scripts/install-suite.sh finance-investment-standard --dry-run",
        "",
        "# Install institutional finance suites only when needed",
        "./scripts/install-suite.sh llmquant --dry-run",
        "./scripts/install-suite.sh anthropic-financial-services --dry-run",
        "```",
        "",
        "Detailed list and scenario notes: [docs/generated/finance-skills-mapping.md](docs/generated/finance-skills-mapping.md).",
    ]
    return "\n".join(lines)

def render_readme(enriched: dict[str, Any], bundle: dict[str, Any], suites: list[dict[str, Any]]) -> str:
    summary = enriched["summary"]
    return "\n".join([
        '<div align="center">',
        "",
        '<img src="assets/logo.png" alt="Boutique Skills" width="76%" />',
        "",
        "# Boutique Skills",
        "",
        "**Curated, source-audited skills for AI agents and coding assistants.**",
        "",
        "**面向智能体的精品技能仓库：原生来源可审计、能力不重复、安装可控、持续月评。**",
        "",
        render_badges(summary, bundle),
        "",
        render_tech_stack_badges(),
        "",
        '<img src="assets/hero.png" alt="Boutique Skills curation principles" width="86%" />',
        "",
        "</div>",
        "",
        "## 中文说明",
        "",
        "Boutique Skills 是一个面向 AI Agent 的精品技能合集。仓库把默认技能、标准配置组、横向分级、纵向分类、API Key/工具依赖、风险等级、冲突组和原生上游来源统一整理成可审计的注册表，目标是让用户安装后即获得一套少重复、低噪声、生产可用的能力组合。",
        "",
        "本仓库强调三件事：一是每个活跃 skill 都必须能追溯到 GitHub、ClawHub/CL.Up、skills.h 或官方项目站点；二是同一能力只推荐一个最佳 skill，避免 Web Search、PDF、Email、Finance Data 等能力重复安装；三是每月自动重建索引和审计报告，让 README、JSON Catalog 与安装包保持一致。",
        "",
        "## Overview",
        "",
        "Boutique Skills is a platform-neutral, source-audited registry for AI agents and coding assistants. It keeps a full machine-readable catalog, a recommended no-duplicate bundle, generated indexes, and monthly audit automation in one place.",
        "",
        "## Quick Start",
        "",
        "Install the recommended no-duplicate bundle:",
        "",
        "```bash",
        "./scripts/install-standard-bundle.sh --dry-run",
        "./scripts/install-standard-bundle.sh",
        "```",
        "",
        "Or install a tier:",
        "",
        "```bash",
        "./scripts/install-tier.sh low",
        "./scripts/install-tier.sh medium",
        "./scripts/install-tier.sh high",
        "```",
        "",
        "Or install a grouped suite:",
        "",
        "```bash",
        "./scripts/install-suite.sh llmquant --dry-run",
        "./scripts/install-suite.sh llmquant",
        "```",
        "",
        "## At A Glance",
        "",
        render_stats(summary, bundle, suites),
        "",
        "## Standard Bundle",
        "",
        "The standard bundle keeps one best skill per capability and excludes skills already supplied by the target agent runtime.",
        "",
        "`a-stock-data` is included in the general standard bundle as the default A-share data skill. Use `./scripts/install-suite.sh finance-investment-standard --dry-run` or the finance profile when an investment workflow needs the full domain stack.",
        "",
        render_standard_bundle_table(bundle),
        "",
        render_finance_entry(enriched, suites),
        "",
        "## Skill Suites",
        "",
        "Skill suites are domain packs kept outside the standard no-duplicate bundle. Use them when a specific workflow needs a deeper vertical stack.",
        "",
        render_suites_table(suites),
        "",
        "## All Skills",
        "",
        render_all_skills_table(enriched["skills"]),
        "",
        "## Indexes",
        "",
        "| Document | What it shows |",
        "|---|---|",
        "| [Horizontal index](docs/generated/horizontal-index.md) | L1 Foundation, L2 Professional, L3 Specialist |",
        "| [Type index](docs/generated/type-index.md) | Coding, design, finance, writing, research, media, docs, and more |",
        "| [Dependency index](docs/generated/dependency-index.md) | API keys, tools, runtime mode, and risk |",
        "| [Finance scenario mapping](docs/generated/finance-skills-mapping.md) | Investment workflows mapped to matching finance skills |",
        "| [Scoring model](docs/generated/scoring-model.md) | How star ratings are calculated |",
        "| [Upstream status](docs/generated/upstream-status.md) | Latest GitHub-backed update check and manual-review items |",
        "| [Content creator intake](docs/generated/content-creator-skills-intake.md) | Verification notes for the creator skill intake batch |",
        "| [Update and audit SOP](docs/UPDATE_AND_AUDIT.md) | Monthly review process and risk gates |",
        "",
        "## Curation Rules",
        "",
        "- Every active skill must have a native upstream source; mirrors and copied installer paths are not treated as origins.",
        "- The standard bundle avoids duplicate capabilities by using conflict groups such as `web-search`, `html-publishing`, `document-pdf`, `email-agent`, and `finance-data`.",
        "- Open and Hermes preset skills are excluded from bundle installs because the target agent already provides them.",
        "- Monthly automation regenerates the registry, indexes, README, standard bundle, and audit reports.",
        "",
        "## Repository Map",
        "",
        "| Path | Purpose |",
        "|---|---|",
        "| `skills/default/` | Local skill sources |",
        "| `catalog/skills.enriched.json` | Full machine-readable registry |",
        "| `catalog/standard-bundle.json` | Recommended no-duplicate install set |",
        "| `catalog/native-origin-overrides.json` | Verified native upstream source map |",
        "| `catalog/presets/` | Open and Hermes preset exclusions |",
        "| `docs/generated/` | Generated human-readable indexes |",
        "| `scripts/` | Install, sync, enrich, audit, and bundle tools |",
        "",
        "## Maintenance",
        "",
        "```bash",
        "python3 scripts/generate_enriched_catalog.py",
        "python3 scripts/audit_skills.py",
        "./scripts/build-bundle.sh",
        "```",
        "",
        "The scheduled workflow runs monthly from `.github/workflows/sync-audit.yml`.",
        "",
        "## License",
        "",
        "[MIT](LICENSE)",
        "",
    ])


def render_tier_doc(payload: dict[str, Any]) -> str:
    lines = [
        f"# {payload.get('title', payload.get('id', 'Tier'))} Skills",
        "",
        payload.get("description", ""),
        "",
        f"- 技能数量：`{len(payload.get('skills', []))}`",
        f"- 安装命令：`{payload.get('install_command', './scripts/install-tier.sh ' + payload.get('id', ''))}`",
        f"- JSON 清单：`tiers/{payload.get('id', 'tier')}.json`",
        "",
        "## 技能清单",
        "",
        "| Skill | 说明 | 使用手册 | 原仓库链接 |",
        "|---|---|---|---|",
    ]
    for item in payload.get("skills", []):
        manual = item.get("manual") or f"skills/default/{item.get('id', '')}/SKILL.md"
        source = item.get("source") or ""
        source_link = md_link(source, "source") if source else "待补"
        lines.append(
            f"| `{item.get('id', '')}` | {item.get('description', '')} | "
            f"[{manual}](../../{manual}) | {source_link} |"
        )
    return "\n".join(lines) + "\n"


def write_tier_outputs() -> None:
    catalog = load_json(DEFAULT_CATALOG, {})
    tiers = catalog.get("tiers", {})
    if not tiers:
        return
    TIERS_DIR.mkdir(parents=True, exist_ok=True)
    DOC_TIERS_DIR.mkdir(parents=True, exist_ok=True)
    all_skills = {}
    for tier in ("low", "medium", "high"):
        payload = tiers.get(tier)
        if not payload:
            continue
        (TIERS_DIR / f"{tier}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (DOC_TIERS_DIR / f"{tier}.md").write_text(render_tier_doc(payload), encoding="utf-8")
        for item in payload.get("skills", []):
            all_skills[item["id"]] = item

    manual_lines = [
        "# Default Skills Manual Index",
        "",
        "本文件由 `scripts/generate_enriched_catalog.py` 生成，作为 boutique 仓库维护默认 skills 的统一手册索引。",
        "",
        "| Skill | 说明 | 使用手册 | 原仓库链接 |",
        "|---|---|---|---|",
    ]
    for skill_id in sorted(all_skills):
        item = all_skills[skill_id]
        manual = item.get("manual") or f"skills/default/{skill_id}/SKILL.md"
        source = item.get("source") or ""
        source_link = md_link(source, "source") if source else "待补"
        manual_lines.append(f"| `{skill_id}` | {item.get('description', '')} | [{manual}]({manual}) | {source_link} |")
    manual_lines.append("")
    MANUALS_DOC.write_text("\n".join(manual_lines), encoding="utf-8")


def write_outputs(enriched: dict[str, Any], bundle: dict[str, Any]) -> None:
    suites = load_suites()
    ENRICHED_PATH.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STANDARD_BUNDLE_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    HORIZONTAL_PATH.write_text(render_horizontal_index(enriched["skills"]), encoding="utf-8")
    TYPE_PATH.write_text(render_type_index(enriched["skills"]), encoding="utf-8")
    DEPENDENCY_PATH.write_text(render_dependency_index(enriched["skills"]), encoding="utf-8")
    SCORING_PATH.write_text(render_scoring_model(), encoding="utf-8")
    README_PATH.write_text(render_readme(enriched, bundle, suites), encoding="utf-8")
    write_tier_outputs()


def main() -> int:
    enriched = build_enriched()
    bundle = build_standard_bundle(enriched)
    write_outputs(enriched, bundle)
    print(json.dumps({"summary": enriched["summary"], "standard_bundle": len(bundle["skills"]), "suites": len(load_suites())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
