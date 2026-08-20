#!/usr/bin/env python3
"""Local skill usage telemetry: collect Skill-tool call frequency from agent
session logs and write a usage report.

Data sources (auto-detected, read-only):
  - ~/.qoder/projects/**/*.jsonl     (Qoder sessions, Claude-Code-compatible)
  - ~/.claude/projects/**/*.jsonl    (Claude Code sessions)

A skill "use" is a tool_use block with name "Skill" (input.skill), or a
<command-name>/skill</command-name> marker in user text whose value matches a
known skill id. Only skill names, timestamps, session ids, and working
directories are read; message content is never stored.

Outputs:
  reports/usage/usage-YYYY-MM-DD.json   full aggregation
  reports/usage/usage-YYYY-MM-DD.md     human-readable report
  reports/usage/usage-scores.json       per-skill usage bonus (0..8) consumed
                                        by generate_enriched_catalog.py
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "usage"
DEFAULT_CATALOG = ROOT / "catalog" / "default-skills.json"
STANDARD_BUNDLE = ROOT / "catalog" / "standard-bundle.json"
FINANCE_SUITE = ROOT / "catalog" / "suites" / "finance-investment-standard.json"

SESSION_ROOTS = [
    (Path.home() / ".qoder" / "projects", "qoder"),
    (Path.home() / ".claude" / "projects", "claude-code"),
]

COMMAND_NAME_RE = re.compile(r"<command-name>\s*/?([A-Za-z0-9_.-]+)\s*</command-name>")
MAX_LINE_BYTES = 2_000_000


def load_registry() -> set[str]:
    data = json.loads(DEFAULT_CATALOG.read_text(encoding="utf-8"))
    ids = set()
    for tier in data.get("tiers", {}).values():
        for item in tier.get("skills", []):
            ids.add(item["id"])
    return ids


def iter_session_files() -> list[tuple[Path, str]]:
    files = []
    for root, source in SESSION_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.jsonl")):
            files.append((path, source))
    return files


def parse_timestamp(text: str) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_skill_uses(path: Path, source: str, known_skills: set[str]) -> list[dict]:
    """Return one record per Skill tool_use / matching slash command."""
    uses = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                if len(line) > MAX_LINE_BYTES:
                    continue
                # Cheap prefilter: skip lines that cannot mention a skill call.
                if '"skill"' not in line and '"Skill"' not in line and "<command-name>" not in line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = parse_timestamp(obj.get("timestamp"))
                session_id = obj.get("sessionId") or path.stem
                cwd = obj.get("cwd") or ""
                message = obj.get("message") or {}
                content = message.get("content")
                if isinstance(content, list):
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use" and (block.get("name") or "").lower() == "skill":
                            skill = (block.get("input") or {}).get("skill")
                            if isinstance(skill, str) and skill.strip():
                                uses.append({
                                    "skill": skill.strip(),
                                    "timestamp": timestamp,
                                    "session": str(session_id),
                                    "cwd": str(cwd),
                                    "source": source,
                                    "form": "tool_use",
                                })
                        elif block.get("type") == "text":
                            for name in COMMAND_NAME_RE.findall(block.get("text") or ""):
                                if name in known_skills:
                                    uses.append({
                                        "skill": name,
                                        "timestamp": timestamp,
                                        "session": str(session_id),
                                        "cwd": str(cwd),
                                        "source": source,
                                        "form": "slash_command",
                                    })
                elif isinstance(content, str) and "<command-name>" in content:
                    for name in COMMAND_NAME_RE.findall(content):
                        if name in known_skills:
                            uses.append({
                                "skill": name,
                                "timestamp": timestamp,
                                "session": str(session_id),
                                "cwd": str(cwd),
                                "source": source,
                                "form": "slash_command",
                            })
    except OSError:
        pass
    return uses


def usage_bonus(calls: int, days_since_last: float | None) -> int:
    """Map usage to a small catalog score bonus (0..8).

    Log scale on calls plus recency decay: stale usage fades out so the
    bonus tracks current behaviour, not ancient history.
    """
    if calls <= 0:
        return 0
    base = min(6.0, 2.0 * math.log2(calls + 1))
    if days_since_last is None:
        recency = 0.5
    elif days_since_last <= 7:
        recency = 1.0
    elif days_since_last <= 30:
        recency = 0.7
    elif days_since_last <= 90:
        recency = 0.4
    else:
        recency = 0.15
    return int(round(base * recency))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--days", type=int, default=30, help="recent window for the headline stats (default 30)")
    args = parser.parse_args()

    known_skills = load_registry()
    files = iter_session_files()
    all_uses: list[dict] = []
    for path, source in files:
        all_uses.extend(extract_skill_uses(path, source, known_skills))

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=args.days)
    recent = [u for u in all_uses if u["timestamp"] and u["timestamp"] >= window_start]

    def aggregate(uses: list[dict]) -> dict[str, dict]:
        agg: dict[str, dict] = {}
        for use in uses:
            skill = use["skill"]
            entry = agg.setdefault(skill, {
                "calls": 0, "sessions": set(), "projects": set(),
                "sources": set(), "last_used": None, "first_used": None,
            })
            entry["calls"] += 1
            entry["sessions"].add(use["session"])
            if use["cwd"]:
                entry["projects"].add(use["cwd"])
            entry["sources"].add(use["source"])
            ts = use["timestamp"]
            if ts:
                iso = ts.isoformat()
                if entry["last_used"] is None or iso > entry["last_used"]:
                    entry["last_used"] = iso
                if entry["first_used"] is None or iso < entry["first_used"]:
                    entry["first_used"] = iso
        for entry in agg.values():
            entry["sessions"] = len(entry["sessions"])
            entry["projects"] = len(entry["projects"])
            entry["sources"] = sorted(entry["sources"])
        return agg

    total_agg = aggregate(all_uses)
    recent_agg = aggregate(recent)

    for skill, entry in total_agg.items():
        last = parse_timestamp(entry["last_used"])
        days = (now - last).total_seconds() / 86400 if last else None
        entry["days_since_last_use"] = round(days, 1) if days is not None else None
        entry["in_registry"] = skill in known_skills
        entry["usage_bonus"] = usage_bonus(entry["calls"], days)
        entry["recent_calls"] = recent_agg.get(skill, {}).get("calls", 0)

    # Bundle coverage: which bundle skills have zero recorded usage.
    bundle_coverage = {}
    for label, path in (("standard_bundle", STANDARD_BUNDLE), ("finance_suite", FINANCE_SUITE)):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if label == "standard_bundle":
            members = [item.get("skill") for item in data.get("skills", [])]
        else:
            members = data.get("skills", [])
        used = [m for m in members if m and total_agg.get(m, {}).get("calls", 0) > 0]
        bundle_coverage[label] = {
            "size": len([m for m in members if m]),
            "used": len(used),
            "unused": sorted(m for m in members if m and total_agg.get(m, {}).get("calls", 0) == 0),
        }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "window_days": args.days,
        "session_files_scanned": len(files),
        "skill_calls_total": len(all_uses),
        "skill_calls_recent": len(recent),
        "distinct_skills_used": len(total_agg),
        "privacy": "local aggregation only: skill names, timestamps, session ids, working directories; no message content stored",
        "skills": {
            skill: entry for skill, entry in
            sorted(total_agg.items(), key=lambda kv: -kv[1]["calls"])
        },
        "bundle_coverage": bundle_coverage,
    }
    json_path = REPORT_DIR / f"usage-{stamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Machine-readable bonus map for the catalog generator.
    scores_path = REPORT_DIR / "usage-scores.json"
    scores_path.write_text(json.dumps({
        "generated_at": payload["generated_at"],
        "policy": "usage_bonus = min(6, 2*log2(calls+1)) * recency(<=7d:1.0, <=30d:0.7, <=90d:0.4, else:0.15); max bonus 8",
        "bonuses": {skill: entry["usage_bonus"] for skill, entry in total_agg.items() if entry["usage_bonus"] > 0},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Markdown report.
    lines = [
        f"# Skill Usage Report {stamp}",
        "",
        f"- 会话文件扫描: {len(files)}（Qoder + Claude Code JSONL）",
        f"- 近 {args.days} 天调用: {len(recent)} 次 | 全部历史: {len(all_uses)} 次",
        f"- 使用过的技能数: {len(total_agg)}（其中收录在本仓库: {sum(1 for e in total_agg.values() if e['in_registry'])}）",
        f"- 隐私: 仅本地聚合技能名/时间/会话与目录，不读取或存储消息内容",
        "",
        "## Top 使用频率（按全部历史调用次数）",
        "",
        "| Skill | 调用 | 近{}天 | 会话数 | 项目数 | 最近使用 | 收录 |".format(args.days),
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for skill, entry in sorted(total_agg.items(), key=lambda kv: -kv[1]["calls"])[:25]:
        lines.append(
            f"| `{skill}` | {entry['calls']} | {entry['recent_calls']} | {entry['sessions']} | "
            f"{entry['projects']} | {entry['last_used'][:10] if entry['last_used'] else '-'} | "
            f"{'✓' if entry['in_registry'] else '✗'} |"
        )

    hot_unregistered = [
        (skill, entry) for skill, entry in total_agg.items()
        if not entry["in_registry"] and entry["calls"] >= 3
    ]
    if hot_unregistered:
        lines += ["", "## 高频使用但未收录（周度发现候选）", "", "| Skill | 调用 | 最近使用 |", "|---|---:|---|"]
        for skill, entry in sorted(hot_unregistered, key=lambda kv: -kv[1]["calls"])[:15]:
            lines.append(f"| `{skill}` | {entry['calls']} | {entry['last_used'][:10] if entry['last_used'] else '-'} |")

    for label, title in (("standard_bundle", "标准组合"), ("finance_suite", "金融组合")):
        cov = bundle_coverage.get(label)
        if not cov:
            continue
        lines += [
            "",
            f"## {title}使用覆盖（{cov['used']}/{cov['size']} 有调用记录）",
            "",
        ]
        if cov["unused"]:
            lines.append("零调用: " + ", ".join(f"`{m}`" for m in cov["unused"]))
        else:
            lines.append("全部技能均有调用记录。")

    md_path = REPORT_DIR / f"usage-{stamp}.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "files": len(files),
        "calls_total": len(all_uses),
        "calls_recent": len(recent),
        "distinct_skills": len(total_agg),
        "bonus_skills": len(payload["skills"]),
        "report": str(md_path.relative_to(ROOT)),
        "scores": str(scores_path.relative_to(ROOT)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
