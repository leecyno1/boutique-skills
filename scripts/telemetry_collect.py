#!/usr/bin/env python3
"""Local skill usage telemetry: collect skill usage frequency from agent
session logs and write a usage report.

Data sources (auto-detected, read-only):
  - ~/.qoder/projects/**/*.jsonl      (Qoder sessions, Claude-Code-compatible)
  - ~/.claude/projects/**/*.jsonl     (Claude Code sessions)
  - ~/.codex/sessions/**, ~/.codex/archived_sessions/**
                                     (Codex CLI rollouts; a use is a tool call
                                      that reads a skill's SKILL.md — the
                                      skills_instructions injection blocks are
                                      ignored)
  - ~/.kimi-code/sessions/**/*.jsonl  (Kimi Code CLI wire logs; a use is a
                                      tool.call event named "Skill")

Qoder/Claude Code use the Skill tool_use form (input.skill) plus slash
commands. Only skill names, timestamps, session ids, and working directories
are read; message content is never stored.

An incremental scan state (reports/usage/.scan-state.json) skips unchanged
session files so weekly runs stay fast after the first full pass. Large
source sets are scanned with a small process pool.

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
import os
import re
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "usage"
STATE_PATH = REPORT_DIR / ".scan-state.json"
USES_PATH = REPORT_DIR / ".scan-uses.json"
DEFAULT_CATALOG = ROOT / "catalog" / "default-skills.json"
STANDARD_BUNDLE = ROOT / "catalog" / "standard-bundle.json"
FINANCE_SUITE = ROOT / "catalog" / "suites" / "finance-investment-standard.json"

SESSION_ROOTS = [
    (Path.home() / ".qoder" / "projects", "qoder"),
    (Path.home() / ".claude" / "projects", "claude-code"),
    (Path.home() / ".codex" / "sessions", "codex"),
    (Path.home() / ".codex" / "archived_sessions", "codex"),
    (Path.home() / ".kimi-code" / "sessions", "kimi-code"),
]

COMMAND_NAME_RE = re.compile(r"<command-name>\s*/?([A-Za-z0-9_.-]+)\s*</command-name>")
SKILLMD_PATH_RE = re.compile(r"([A-Za-z0-9_.-]+)/SKILL\.md")
CODEX_CALL_PAYLOAD_TYPES = {"custom_tool_call", "function_call"}
MAX_LINE_BYTES = 2_000_000
WORKERS = 4


def load_registry() -> set[str]:
    data = json.loads(DEFAULT_CATALOG.read_text(encoding="utf-8"))
    ids = set()
    for tier in data.get("tiers", {}).values():
        for item in tier.get("skills", []):
            ids.add(item["id"])
    return ids


def parse_timestamp(text: str) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _uses_from_tool_call_text(text: str, timestamp, session: str, cwd: str, source: str) -> list[dict]:
    """One use per distinct skill whose SKILL.md path appears in tool args."""
    found = set(SKILLMD_PATH_RE.findall(text or ""))
    return [
        {"skill": name, "timestamp": timestamp, "session": session, "cwd": cwd,
         "source": source, "form": "skill_read"}
        for name in sorted(found)
    ]


def extract_uses_worker(args: tuple[str, str, tuple[str, ...]]) -> list[dict]:
    """Extract skill-use records from one session file (pool worker)."""
    path_text, source, known = args
    path = Path(path_text)
    known_skills = set(known)
    uses: list[dict] = []

    if source == "codex":
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                session_id = path.stem.split("-")[-1] if "-" in path.stem else path.stem
                cwd = ""
                for index, line in enumerate(handle):
                    if len(line) > MAX_LINE_BYTES:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    payload = obj.get("payload") or {}
                    if not isinstance(payload, dict):
                        continue
                    if index == 0 and obj.get("type") == "session_meta":
                        session_id = payload.get("session_id") or session_id
                        cwd = payload.get("cwd") or ""
                        continue
                    if payload.get("type") not in CODEX_CALL_PAYLOAD_TYPES:
                        continue
                    if "SKILL.md" not in line:
                        continue
                    text = payload.get("input")
                    if not isinstance(text, str):
                        text = payload.get("arguments") or ""
                    uses.extend(
                        _uses_from_tool_call_text(text, parse_timestamp(obj.get("timestamp")), session_id, cwd, source)
                    )
        except OSError:
            pass
        return uses

    if source == "kimi-code":
        # wire.jsonl rows: {type: "context.append_loop_event", time: epoch-ms,
        # event: {type: "tool.call", name: "Skill", args: ...}}. Session id
        # comes from the session_<uuid> path segment; cwd is not recorded.
        session_id = ""
        for part in path.parts:
            if part.startswith("session_"):
                session_id = part[len("session_"):]
                break
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    if len(line) > MAX_LINE_BYTES or '"tool.call"' not in line or '"Skill"' not in line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    event = obj.get("event") or {}
                    if not isinstance(event, dict) or event.get("type") != "tool.call":
                        continue
                    if (event.get("name") or "") != "Skill":
                        continue
                    args = event.get("args")
                    skill = None
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = None
                    if isinstance(args, dict):
                        skill = args.get("skill") or args.get("name")
                    if isinstance(skill, str) and skill.strip():
                        ts = None
                        raw_time = obj.get("time")
                        if isinstance(raw_time, (int, float)):
                            ts = datetime.fromtimestamp(raw_time / 1000.0, tz=timezone.utc)
                        uses.append({
                            "skill": skill.strip(), "timestamp": ts,
                            "session": session_id or path.stem, "cwd": "",
                            "source": source, "form": "tool_use",
                        })
        except OSError:
            pass
        return uses

    # Qoder / Claude Code JSONL.
    try:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                if len(line) > MAX_LINE_BYTES:
                    continue
                if '"skill"' not in line and '"Skill"' not in line and "<command-name>" not in line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = parse_timestamp(obj.get("timestamp"))
                session_id = str(obj.get("sessionId") or path.stem)
                cwd = str(obj.get("cwd") or "")
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
                                    "skill": skill.strip(), "timestamp": timestamp,
                                    "session": session_id, "cwd": cwd,
                                    "source": source, "form": "tool_use",
                                })
                        elif block.get("type") == "text":
                            for name in COMMAND_NAME_RE.findall(block.get("text") or ""):
                                if name in known_skills:
                                    uses.append({
                                        "skill": name, "timestamp": timestamp,
                                        "session": session_id, "cwd": cwd,
                                        "source": source, "form": "slash_command",
                                    })
                elif isinstance(content, str) and "<command-name>" in content:
                    for name in COMMAND_NAME_RE.findall(content):
                        if name in known_skills:
                            uses.append({
                                "skill": name, "timestamp": timestamp,
                                "session": session_id, "cwd": cwd,
                                "source": source, "form": "slash_command",
                            })
    except OSError:
        pass
    return uses


def load_state() -> dict[str, list]:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state: dict[str, list]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")


def load_uses() -> dict[str, list[dict]]:
    """Persisted per-file use records from previous runs (JSON-safe form)."""
    if not USES_PATH.exists():
        return {}
    try:
        raw = json.loads(USES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(raw, dict):
        return {}
    return {path: records for path, records in raw.items() if isinstance(records, list)}


def save_uses(uses: dict[str, list[dict]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    USES_PATH.write_text(json.dumps(uses, ensure_ascii=False), encoding="utf-8")


def rehydrate(record: dict) -> dict:
    record["timestamp"] = parse_timestamp(record.get("timestamp"))
    return record


def collect_uses(known_skills: set[str], rescan_all: bool) -> tuple[list[dict], int, int]:
    """Scan session files incrementally; returns (uses, scanned, skipped).

    Per-file use records persist in .scan-uses.json so the aggregation always
    covers full history, while unchanged files are not re-read. Records for
    files that disappeared (e.g. sessions moved to archived_sessions under a
    new path) are dropped; the moved file is picked up as a new path.
    """
    state = {} if rescan_all else load_state()
    stored_uses = {} if rescan_all else load_uses()

    candidates = []
    for root, source in SESSION_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.jsonl")):
            candidates.append((path, source))

    fresh = []
    disk_paths = set()
    for path, source in candidates:
        key = str(path)
        disk_paths.add(key)
        try:
            stat = [path.stat().st_size, path.stat().st_mtime]
        except OSError:
            continue
        if state.get(key) == stat:
            continue
        fresh.append((key, source, stat))

    known_tuple = tuple(sorted(known_skills))
    jobs = [(key, source, known_tuple) for key, source, _ in fresh]
    results: list[list[dict]] = []
    if jobs:
        workers = min(WORKERS, max(1, os.cpu_count() or 1))
        if len(jobs) > 8:
            with ProcessPoolExecutor(max_workers=workers) as pool:
                results = list(pool.map(extract_uses_worker, jobs, chunksize=4))
        else:
            results = [extract_uses_worker(job) for job in jobs]
    per_file_new = {jobs[i][0]: results[i] for i in range(len(jobs))}

    # Rebuild the persistent store: drop vanished paths, keep unchanged
    # records, replace records for (re)scanned files.
    fresh_paths = set(per_file_new)
    merged: dict[str, list[dict]] = {
        path: records for path, records in stored_uses.items()
        if path in disk_paths and path not in fresh_paths
    }
    merged.update(per_file_new)

    new_state = {key: stat for key, _, stat in fresh}
    for path, stat in state.items():
        if path in disk_paths:
            new_state.setdefault(path, stat)

    # Persist JSON-safe copies (datetime -> ISO strings) and rehydrate for aggregation.
    persist: dict[str, list[dict]] = {}
    all_uses: list[dict] = []
    for path, records in merged.items():
        clean = []
        for use in records:
            item = dict(use)
            ts = item.get("timestamp")
            if isinstance(ts, datetime):
                item["timestamp"] = ts.isoformat()
            clean.append(item)
        persist[path] = clean
        all_uses.extend(rehydrate(dict(item)) for item in clean)

    save_uses(persist)
    save_state(new_state)
    return all_uses, len(jobs), len(candidates) - len(jobs)


def usage_bonus(calls: int, days_since_last: float | None) -> int:
    """Map usage to a small catalog score bonus (0..8)."""
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--days", type=int, default=30, help="recent window for the headline stats (default 30)")
    parser.add_argument("--rescan-all", action="store_true", help="ignore the incremental scan state and rescan every session file")
    args = parser.parse_args()

    known_skills = load_registry()
    all_uses, scanned, skipped = collect_uses(known_skills, args.rescan_all)

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=args.days)
    recent = [u for u in all_uses if u["timestamp"] and u["timestamp"] >= window_start]

    total_agg = aggregate(all_uses)
    recent_agg = aggregate(recent)

    for skill, entry in total_agg.items():
        last = parse_timestamp(entry["last_used"])
        days = (now - last).total_seconds() / 86400 if last else None
        entry["days_since_last_use"] = round(days, 1) if days is not None else None
        entry["in_registry"] = skill in known_skills
        entry["usage_bonus"] = usage_bonus(entry["calls"], days)
        entry["recent_calls"] = recent_agg.get(skill, {}).get("calls", 0)

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
        "session_files_scanned": scanned,
        "session_files_skipped_unchanged": skipped,
        "skill_calls_total": len(all_uses),
        "skill_calls_recent": len(recent),
        "distinct_skills_used": len(total_agg),
        "by_source": dict(Counter(u["source"] for u in all_uses)),
        "privacy": "local aggregation only: skill names, timestamps, session ids, working directories; no message content stored",
        "skills": {
            skill: entry for skill, entry in
            sorted(total_agg.items(), key=lambda kv: -kv[1]["calls"])
        },
        "bundle_coverage": bundle_coverage,
    }
    json_path = REPORT_DIR / f"usage-{stamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    scores_path = REPORT_DIR / "usage-scores.json"
    scores_path.write_text(json.dumps({
        "generated_at": payload["generated_at"],
        "policy": "usage_bonus = min(6, 2*log2(calls+1)) * recency(<=7d:1.0, <=30d:0.7, <=90d:0.4, else:0.15); max bonus 8",
        "bonuses": {skill: entry["usage_bonus"] for skill, entry in total_agg.items() if entry["usage_bonus"] > 0},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Skill Usage Report {stamp}",
        "",
        f"- 本次扫描会话文件: {scanned}（另有 {skipped} 个未变化文件经增量缓存跳过）",
        f"- 近 {args.days} 天调用: {len(recent)} 次 | 全部历史: {len(all_uses)} 次（{', '.join(f'{k}: {v}' for k, v in sorted(payload['by_source'].items()))}）",
        f"- 使用过的技能数: {len(total_agg)}（其中收录在本仓库: {sum(1 for e in total_agg.values() if e['in_registry'])}）",
        f"- 隐私: 仅本地聚合技能名/时间/会话与目录，不读取或存储消息内容",
        "",
        "## Top 使用频率（按全部历史调用次数）",
        "",
        "| Skill | 调用 | 近{}天 | 会话数 | 项目数 | 来源 | 最近使用 | 收录 |".format(args.days),
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for skill, entry in sorted(total_agg.items(), key=lambda kv: -kv[1]["calls"])[:25]:
        lines.append(
            f"| `{skill}` | {entry['calls']} | {entry['recent_calls']} | {entry['sessions']} | "
            f"{entry['projects']} | {', '.join(entry['sources'])} | "
            f"{entry['last_used'][:10] if entry['last_used'] else '-'} | "
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
        "files_scanned": scanned,
        "files_skipped": skipped,
        "calls_total": len(all_uses),
        "calls_recent": len(recent),
        "by_source": payload["by_source"],
        "distinct_skills": len(total_agg),
        "report": str(md_path.relative_to(ROOT)),
        "scores": str(scores_path.relative_to(ROOT)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
