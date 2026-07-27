#!/usr/bin/env python3
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

REPO = Path(__file__).resolve().parents[1]
LEGACY_CATALOG = REPO / "catalog" / "skills.json"
ENRICHED_CATALOG = REPO / "catalog" / "skills.enriched.json"
LOCAL_SKILLS_DIR = REPO / "skills" / "default"
SKILL_DIRS = [
    LOCAL_SKILLS_DIR,
    Path.home() / ".openclaw" / "skills",
    Path.home() / "Desktop" / "Projects" / "clawdbot" / "skills",
]

HIGH_RISK_PATTERNS = [
    re.compile(r"\bsudo\b"),
    re.compile(r"rm\s+-rf\s+/"),
    re.compile(r"curl\s+[^\n|]+\|\s*(sh|bash)"),
    re.compile(r"wget\s+[^\n|]+\|\s*(sh|bash)"),
    re.compile(r"(?<![A-Za-z0-9_])eval\s*\("),
]


def load_legacy_catalog() -> dict:
    if not LEGACY_CATALOG.exists():
        return {"skills": []}
    return json.loads(LEGACY_CATALOG.read_text(encoding="utf-8"))


def load_enriched_catalog() -> dict:
    if not ENRICHED_CATALOG.exists():
        return {"skills": []}
    return json.loads(ENRICHED_CATALOG.read_text(encoding="utf-8"))


def find_skill_path(skill: str) -> Path | None:
    for base in SKILL_DIRS:
        p = base / skill
        if p.exists():
            return p
    return None


def scan_text_files(root: Path, max_files: int = 120) -> List[dict]:
    findings = []
    checked = 0
    for p in root.rglob("*"):
        if checked >= max_files:
            break
        if not p.is_file():
            continue
        if "node_modules" in p.parts:
            continue
        if ".test." in p.name:
            continue
        if p.suffix.lower() not in {".sh", ".py", ".js", ".ts"}:
            continue
        checked += 1
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rule in HIGH_RISK_PATTERNS:
            if rule.search(text):
                findings.append({"file": str(p), "pattern": rule.pattern})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the curated Boutique Skills registry")
    parser.add_argument("--report", default=str(REPO / "reports" / "audit-latest.md"))
    parser.add_argument("--json", default=str(REPO / "reports" / "audit-latest.json"))
    parser.add_argument("--strict-risk", action="store_true", help="treat risk findings as FAIL instead of WARN")
    args = parser.parse_args()

    legacy_catalog = load_legacy_catalog()
    enriched = load_enriched_catalog()
    enriched_skills = enriched.get("skills", [])
    skills = [
        {
            "id": item.get("id"),
            "requires_api_keys": (item.get("dependencies") or {}).get("requires_api_keys", False),
            "api_keys": (item.get("dependencies") or {}).get("api_keys", []),
        }
        for item in enriched_skills
        if item.get("id") and not item.get("preset_excluded")
    ]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dup_caps = {}
    cap_owner = {}
    for s in legacy_catalog.get("skills", []):
        cap = s["capability"]
        if cap in cap_owner:
            dup_caps.setdefault(cap, [cap_owner[cap]]).append(s["skill"])
        else:
            cap_owner[cap] = s["skill"]

    missing = []
    env_missing = []
    risky = []
    resolved = []
    missing_origins = [
        {
            "skill": item.get("id"),
            "mirror_source_url": (item.get("origin") or {}).get("mirror_source_url"),
        }
        for item in enriched_skills
        if (item.get("origin") or {}).get("needs_origin_review")
    ]
    standard_bundle_issues = []
    standard_bundle_path = REPO / "catalog" / "standard-bundle.json"
    if standard_bundle_path.exists():
        bundle = json.loads(standard_bundle_path.read_text(encoding="utf-8"))
        bundle_items = bundle.get("skills", [])
        max_skills = int(bundle.get("max_skills") or 30)
        capabilities = [item.get("capability") for item in bundle_items]
        conflicts = [item.get("conflict_group") for item in bundle_items]
        if len(bundle_items) > max_skills:
            standard_bundle_issues.append(f"standard bundle has more than {max_skills} skills")
        if len(set(capabilities)) != len(capabilities):
            standard_bundle_issues.append("standard bundle has duplicate capabilities")
        if len(set(conflicts)) != len(conflicts):
            standard_bundle_issues.append("standard bundle has duplicate conflict groups")

    for s in skills:
        skill = s["id"]
        p = find_skill_path(skill)
        if not p:
            missing.append(skill)
            continue
        resolved.append({"skill": skill, "path": str(p)})
        for env in s.get("api_keys", []):
            if not os.environ.get(env):
                env_missing.append({"skill": skill, "env": env})
        risky.extend([{"skill": skill, **f} for f in scan_text_files(p)])

    status = "PASS"
    if dup_caps or standard_bundle_issues or (args.strict_risk and risky):
        status = "FAIL"
    elif missing or env_missing or missing_origins or risky:
        status = "WARN"

    result = {
        "timestamp": ts,
        "status": status,
        "summary": {
            "catalog_skills": len(enriched_skills),
            "audited_skills": len(skills),
            "legacy_catalog_skills": len(legacy_catalog.get("skills", [])),
            "resolved_skills": len(resolved),
            "missing_skills": len(missing),
            "missing_env": len(env_missing),
            "duplicate_capabilities": len(dup_caps),
            "risky_hits": len(risky),
            "missing_native_origins": len(missing_origins),
            "standard_bundle_issues": len(standard_bundle_issues),
        },
        "duplicates": dup_caps,
        "missing_native_origins": missing_origins,
        "standard_bundle_issues": standard_bundle_issues,
        "missing": missing,
        "missing_env": env_missing,
        "risky": risky,
        "resolved": resolved,
    }

    report_lines = [
        f"# Boutique Skills Audit",
        "",
        f"- Time: {ts}",
        f"- Status: **{status}**",
        f"- Catalog skills: {len(enriched_skills)}",
        f"- Audited skills: {len(skills)}",
        f"- Legacy catalog skills: {len(legacy_catalog.get('skills', []))}",
        f"- Installed/Resolved: {len(resolved)}",
        f"- Missing: {len(missing)}",
        f"- Missing env vars: {len(env_missing)}",
        f"- Duplicate capabilities: {len(dup_caps)}",
        f"- Risk hits: {len(risky)}",
        f"- Missing native origins: {len(missing_origins)}",
        f"- Standard bundle issues: {len(standard_bundle_issues)}",
        "",
        "## Missing Skills",
    ]
    report_lines.extend([f"- {s}" for s in missing] or ["- None"])
    report_lines.append("")
    report_lines.append("## Missing Environment Variables")
    report_lines.extend([f"- {item['skill']}: `{item['env']}`" for item in env_missing] or ["- None"])
    report_lines.append("")
    report_lines.append("## Duplicate Capabilities")
    if dup_caps:
        for cap, owners in dup_caps.items():
            report_lines.append(f"- {cap}: {', '.join(owners)}")
    else:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Missing Native Origins")
    if missing_origins:
        for item in missing_origins[:120]:
            report_lines.append(f"- {item['skill']}: {item.get('mirror_source_url') or 'no mirror source'}")
        if len(missing_origins) > 120:
            report_lines.append(f"- ... {len(missing_origins)-120} more missing native origins")
    else:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Standard Bundle Issues")
    report_lines.extend([f"- {issue}" for issue in standard_bundle_issues] or ["- None"])
    report_lines.append("")
    report_lines.append("## Risk Findings")
    if risky:
        for item in risky[:80]:
            report_lines.append(
                f"- {item['skill']}: `{item['pattern']}` in `{item['file']}`"
            )
        if len(risky) > 80:
            report_lines.append(f"- ... {len(risky)-80} more findings")
    else:
        report_lines.append("- None")

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result["summary"], ensure_ascii=False))
    print(f"report: {report_path}")
    print(f"json: {json_path}")

    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
