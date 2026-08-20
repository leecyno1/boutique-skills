#!/usr/bin/env python3
"""Generate skill adjustment recommendations from usage telemetry.

Combines three inputs:
  - installed skills across agent runtime roots (~/.codex/skills, ...)
  - the latest usage report (reports/usage/usage-*.json)
  - the registry (catalog/default-skills.json)

Every installed skill is classified:
  keep      actively used within --active-days (never proposed for removal)
  remove    not in the registry, zero recorded calls, installed/present for
            more than --unused-days — written to pending-cleanup.json and
            uninstalled only after the user confirms
  consider  in the registry but unused, or unused for 30-90 days
  discover  not in the registry but heavily used — import candidates for the
            weekly curation flow (e.g. orphan skills with real demand)

Removal is proposal-only; scripts/uninstall_skills.py --confirm performs the
archive-based uninstall after user approval.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "usage"
PENDING_PATH = REPORT_DIR / "pending-cleanup.json"
DEFAULT_CATALOG = ROOT / "catalog" / "default-skills.json"

RUNTIME_ROOTS = [
    (Path.home() / ".codex" / "skills", "codex"),
    (Path.home() / ".qoder" / "skills", "qoder"),
    (Path.home() / ".agents" / "skills", "agents"),
    (Path.home() / ".lingma" / "skills", "lingma"),
]

DISCOVER_MIN_CALLS = 20
DISCOVER_MIN_RECENT = 5


def load_registry() -> set[str]:
    data = json.loads(DEFAULT_CATALOG.read_text(encoding="utf-8"))
    return {item["id"] for tier in data.get("tiers", {}).values() for item in tier.get("skills", [])}


def latest_usage() -> dict:
    files = sorted(
        f for f in REPORT_DIR.glob("usage-*.json")
        if re.fullmatch(r"usage-\d{4}-\d{2}-\d{2}\.json", f.name)
    )
    if not files:
        return {}
    try:
        return json.loads(files[-1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def installed_skills() -> list[dict]:
    """One record per (runtime, skill dir) that contains a SKILL.md."""
    found = []
    for root, runtime in RUNTIME_ROOTS:
        if not root.exists():
            continue
        for entry in sorted(root.iterdir()):
            skill_md = entry / "SKILL.md"
            if entry.is_dir() and skill_md.exists():
                try:
                    age_days = (datetime.now().timestamp() - skill_md.stat().st_mtime) / 86400
                except OSError:
                    age_days = 0.0
                found.append({
                    "skill": entry.name,
                    "runtime": runtime,
                    "path": str(entry),
                    "age_days": round(age_days, 1),
                })
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--active-days", type=int, default=30, help="used within N days counts as active/protected (default 30)")
    parser.add_argument("--unused-days", type=int, default=60, help="installed longer than N days with zero calls may be proposed for removal (default 60)")
    parser.add_argument("--keep", nargs="*", default=[], help="extra skill names to always protect")
    args = parser.parse_args()

    registry = load_registry()
    usage = latest_usage()
    usage_skills = usage.get("skills", {})
    installed = installed_skills()
    extra_keep = set(args.keep)

    recommendations: dict[str, list[dict]] = {"remove": [], "consider": [], "keep": [], "discover": []}

    for item in installed:
        skill = item["skill"]
        entry = usage_skills.get(skill, {})
        calls = entry.get("calls", 0)
        recent_calls = entry.get("recent_calls", 0)
        last_used = entry.get("last_used")
        days_idle = entry.get("days_since_last_use")
        in_registry = skill in registry
        protected = skill in extra_keep

        record = dict(item)
        record.update({
            "in_registry": in_registry,
            "calls": calls,
            "recent_calls": recent_calls,
            "last_used": last_used,
            "days_since_last_use": days_idle,
        })

        if protected:
            record["reason"] = "用户白名单保护"
            recommendations["keep"].append(record)
        elif recent_calls > 0 or (days_idle is not None and days_idle <= args.active_days):
            record["reason"] = f"近 {args.active_days} 天有使用（{recent_calls} 次），受保护"
            recommendations["keep"].append(record)
        elif not in_registry and calls == 0 and item["age_days"] >= args.unused_days:
            record["reason"] = f"未收录于仓库且从未记录到调用，已安装 {item['age_days']:.0f} 天"
            recommendations["remove"].append(record)
        elif not in_registry and days_idle is not None and days_idle > 90:
            record["reason"] = f"未收录且已 {days_idle:.0f} 天未使用（历史 {calls} 次）"
            recommendations["remove"].append(record)
        elif not in_registry and (calls >= DISCOVER_MIN_CALLS or recent_calls >= DISCOVER_MIN_RECENT):
            record["reason"] = f"未收录但高频使用（历史 {calls} 次 / 近30天 {recent_calls} 次），建议纳入周度发现流程"
            recommendations["discover"].append(record)
        elif calls == 0:
            record["reason"] = "零调用记录" + ("，已在仓库注册" if in_registry else "")
            recommendations["consider"].append(record)
        else:
            record["reason"] = f"历史 {calls} 次，已 {days_idle if days_idle is not None else '?'} 天未使用"
            recommendations["consider"].append(record)

    for bucket in recommendations.values():
        bucket.sort(key=lambda r: (-r.get("calls", 0), r["skill"], r["runtime"]))

    stamp = datetime.now().strftime("%Y-%m-%d")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "params": {"active_days": args.active_days, "unused_days": args.unused_days},
        "usage_report_basis": usage.get("generated_at"),
        "installed_total": len(installed),
        "counts": {k: len(v) for k, v in recommendations.items()},
        "recommendations": recommendations,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"recommendations-{stamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Pending cleanup: only the `remove` bucket, awaiting user confirmation.
    pending = {
        "generated_at": payload["generated_at"],
        "status": "pending",
        "source_report": json_path.name,
        "note": "uninstall is archive-based and runs only via scripts/uninstall_skills.py --confirm",
        "items": [
            {"skill": r["skill"], "runtime": r["runtime"], "path": r["path"], "reason": r["reason"]}
            for r in recommendations["remove"]
        ],
    }
    PENDING_PATH.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Skill 调整建议 {stamp}",
        "",
        f"- 已安装技能总数: {len(installed)}（Codex/Qoder/agents/lingma 四运行时）",
        f"- 分级: 待卸载 {len(recommendations['remove'])} | 供参考 {len(recommendations['consider'])} | 受保护 {len(recommendations['keep'])} | 入库候选 {len(recommendations['discover'])}",
        f"- 依据: 使用遥测 {usage.get('generated_at', '无')}；近 {args.active_days} 天有调用的技能一律保护，绝不进入卸载建议",
        "",
    ]
    if recommendations["remove"]:
        lines += ["## 待确认卸载（remove）", "", "| Skill | 运行时 | 理由 |", "|---|---|---|"]
        for r in recommendations["remove"]:
            lines.append(f"| `{r['skill']}` | {r['runtime']} | {r['reason']} |")
        lines += ["", "确认执行: `python3 scripts/uninstall_skills.py --confirm`（归档式卸载，可恢复）；预览: `python3 scripts/uninstall_skills.py`"]
    if recommendations["discover"]:
        lines += ["", "## 入库候选（discover，高频但未收录）", "", "| Skill | 运行时 | 调用 | 理由 |", "|---|---|---:|---|"]
        for r in recommendations["discover"]:
            lines.append(f"| `{r['skill']}` | {r['runtime']} | {r['calls']} | {r['reason']} |")
    if recommendations["consider"]:
        lines += ["", "## 供参考（consider，零调用或久未使用）", "", "| Skill | 运行时 | 调用 | 距上次使用 | 说明 |", "|---|---|---:|---|---|"]
        for r in recommendations["consider"][:40]:
            lines.append(f"| `{r['skill']}` | {r['runtime']} | {r['calls']} | {r['days_since_last_use'] if r['days_since_last_use'] is not None else '-'} | {r['reason']} |")
        if len(recommendations["consider"]) > 40:
            lines.append(f"| ...另有 {len(recommendations['consider']) - 40} 项见 JSON | | | | |")
    lines += ["", "## 受保护（keep，近期活跃）", ""]
    lines.append(", ".join(f"`{r['skill']}`" for r in recommendations["keep"][:60]) or "（无）")
    if len(recommendations["keep"]) > 60:
        lines.append(f"...另有 {len(recommendations['keep']) - 60} 个")

    md_path = REPORT_DIR / f"recommendations-{stamp}.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "installed": len(installed),
        "counts": payload["counts"],
        "report": str(md_path.relative_to(ROOT)),
        "pending": str(PENDING_PATH.relative_to(ROOT)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
