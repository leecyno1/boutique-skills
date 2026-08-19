#!/usr/bin/env python3
"""Weekly GitHub skills discovery, scoring, import/export curation.

Pipeline stages:
  discover  Search GitHub for new skill candidates, score them, and write a
            weekly report under reports/weekly-curation/.
  import    Download approved high-score candidates into skills/default/,
            register them in catalog/default-skills.json and
            catalog/native-origin-overrides.json, and write a review note.
  prune     Check existing skills for dead upstreams, low scores, and
            clearly dominated duplicates inside the same conflict group.
            Writes removal suggestions; --apply performs the removal.
  run       discover --import + prune (suggestion-only) in one pass.

Scoring thresholds follow QODER_HANDOFF.md: >=75 import, <60 remove.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ENRICHED_CATALOG = ROOT / "catalog" / "skills.enriched.json"
DEFAULT_CATALOG = ROOT / "catalog" / "default-skills.json"
ORIGIN_OVERRIDES = ROOT / "catalog" / "native-origin-overrides.json"
SKILLS_DIR = ROOT / "skills" / "default"
REPORT_DIR = ROOT / "reports" / "weekly-curation"
DISCOVERY_DIR = ROOT / "reports" / "source-discovery"

IMPORT_SCORE = 75
REVIEW_SCORE = 60
REMOVE_SCORE = 60
DOMINATED_GAP = 15
DOMINATED_MAX_SCORE = 70
MIN_STARS = 20
# Safety valve: never auto-import more than this many repos per weekly run.
# Lower-scored import verdicts fall back to the manual review queue.
MAX_WEEKLY_IMPORTS = 5
# Repos without a root SKILL.md (frameworks shipping a skills/ folder on the
# side) need a higher bar before auto-import: more skills and higher score.
MONOREPO_IMPORT_SCORE = 80
MONOREPO_MIN_SUBDIRS = 3
MAX_IMPORT_FILES = 120
MAX_IMPORT_BYTES = 4_000_000
EXCLUDED_PARTS = {".git", "node_modules", "__pycache__", ".venv", "dist", ".next"}

SEARCH_QUERIES = [
    "claude skills in:name,description,readme",
    "topic:claude-skills",
    "topic:agent-skills",
    "agent skills SKILL.md in:readme",
    "claude code skills in:name,description",
    "openclaw skills in:name,description,readme",
]

SKILL_FILE_NAMES = {"SKILL.md", "README.md", "GUIDE.md", "LICENSE", "LICENSE.md", "SOURCE.txt"}
SKILL_DIR_NAMES = {"scripts", "references", "assets", "agents", "examples", "zh"}
# Only directories matching these patterns may contain skills; keeps the
# structure inspection within a couple of API calls per candidate.
SKILL_CONTAINER_HINTS = {
    "skills", "skill", "claude-skills", "agent-skills", "agents",
    "commands", "plugins", "packs",
}


def gh_token() -> str | None:
    env_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if env_token:
        return env_token
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return None
    return result.stdout.strip() or None


def api_get(path: str, token: str | None) -> dict | list | None:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/{path.lstrip('/')}", headers=headers)
    for attempt in range(3):
        try:
            with urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code in {403, 404}:
                return None
            if attempt == 2:
                raise
        except URLError:
            if attempt == 2:
                raise
        time.sleep(1 + attempt)
    return None


def raw_file_bytes(owner: str, repo: str, ref: str, path: str, token: str | None) -> bytes | None:
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            return response.read()
    except (HTTPError, URLError):
        return None


@dataclass
class Candidate:
    owner: str
    repo: str
    url: str
    stars: int = 0
    forks: int = 0
    pushed_at: str = ""
    description: str = ""
    topics: list[str] = field(default_factory=list)
    license: str | None = None
    default_branch: str = "main"
    has_root_skill: bool = False
    skill_subdirs: list[str] = field(default_factory=list)
    score: int = 0
    breakdown: dict[str, int] = field(default_factory=dict)
    overlap: str | None = None
    verdict: str = "review"


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_enriched_index() -> dict[str, dict]:
    data = load_json(ENRICHED_CATALOG, {})
    return {item["id"]: item for item in data.get("skills", [])}


def known_github_repos(skills: dict[str, dict]) -> set[str]:
    repos = set()
    for item in skills.values():
        url = (item.get("origin") or {}).get("origin_url") or ""
        match = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/|$)", url)
        if match:
            repos.add(f"{match.group(1).lower()}/{match.group(2).lower()}")
    return repos


# ---------------------------------------------------------------- discovery


def search_github(token: str | None) -> list[dict]:
    repos: dict[str, dict] = {}
    for query in SEARCH_QUERIES:
        path = f"search/repositories?q={query.replace(' ', '+')}&sort=stars&order=desc&per_page=30"
        payload = api_get(path, token)
        if not isinstance(payload, dict):
            continue
        for item in payload.get("items", []) or []:
            full_name = (item.get("full_name") or "").lower()
            if full_name and full_name not in repos:
                repos[full_name] = item
        time.sleep(2)
    return sorted(repos.values(), key=lambda item: -(item.get("stargazers_count") or 0))


def days_since(date_text: str) -> int | None:
    if not date_text:
        return None
    try:
        pushed = datetime.strptime(date_text[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return max(0, (datetime.now(timezone.utc) - pushed).days)


def inspect_repo_structure(candidate: Candidate, token: str | None) -> None:
    root = api_get(f"/repos/{candidate.owner}/{candidate.repo}/contents", token)
    if isinstance(root, list):
        names = {item.get("name") for item in root}
        dirs = [
            item.get("name")
            for item in root
            if item.get("type") == "dir" and item.get("name") in SKILL_CONTAINER_HINTS
        ]
        candidate.has_root_skill = "SKILL.md" in names
        for dirname in sorted(dirs)[:4]:
            child = api_get(
                f"/repos/{candidate.owner}/{candidate.repo}/contents/{dirname}", token
            )
            if isinstance(child, list):
                checked = 0
                for entry in child:
                    if entry.get("type") != "dir":
                        continue
                    checked += 1
                    if checked > 15:  # cap grandchild probes on large collections
                        break
                    grandchild = api_get(
                        f"/repos/{candidate.owner}/{candidate.repo}/contents/{entry['path']}",
                        token,
                    )
                    if isinstance(grandchild, list) and any(
                        item.get("name") == "SKILL.md" for item in grandchild
                    ):
                        candidate.skill_subdirs.append(entry["path"])
                    time.sleep(0.2)
                    if len(candidate.skill_subdirs) >= 5:
                        break
            if len(candidate.skill_subdirs) >= 5:
                break


def score_candidate(candidate: Candidate, skills: dict[str, dict]) -> None:
    stars = candidate.stars
    if stars >= 2000:
        star_points = 30
    elif stars >= 500:
        star_points = 26
    elif stars >= 200:
        star_points = 22
    elif stars >= 100:
        star_points = 18
    elif stars >= 50:
        star_points = 14
    elif stars >= MIN_STARS:
        star_points = 10
    else:
        star_points = 4

    age = days_since(candidate.pushed_at)
    if age is None:
        activity_points = 0
    elif age <= 30:
        activity_points = 20
    elif age <= 90:
        activity_points = 15
    elif age <= 180:
        activity_points = 10
    elif age <= 365:
        activity_points = 5
    else:
        activity_points = -8

    structure_points = 0
    if candidate.has_root_skill:
        structure_points += 15
    if candidate.skill_subdirs:
        structure_points += min(10, 5 * len(candidate.skill_subdirs))
    if candidate.license in {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "ISC", "MPL-2.0"}:
        structure_points += 5

    quality_points = 0
    if len(candidate.description or "") >= 60:
        quality_points += 5
    if any(topic in {"claude-skills", "agent-skills", "claude-code", "ai-agents", "openclaw"} for topic in candidate.topics):
        quality_points += 5
    if candidate.stars >= 100:
        quality_points += 5

    overlap = detect_overlap(candidate, skills)
    overlap_penalty = 15 if overlap else 0

    score = star_points + activity_points + structure_points + quality_points - overlap_penalty
    candidate.score = max(0, min(100, score))
    candidate.breakdown = {
        "stars": star_points,
        "activity": activity_points,
        "structure": structure_points,
        "quality": quality_points,
        "overlap_penalty": -overlap_penalty,
    }
    candidate.overlap = overlap
    if detect_aggregator(candidate):
        candidate.verdict = "review"
        return
    if candidate.has_root_skill:
        import_score = IMPORT_SCORE
    else:
        import_score = max(IMPORT_SCORE, MONOREPO_IMPORT_SCORE)
        if len(candidate.skill_subdirs) < MONOREPO_MIN_SUBDIRS:
            import_score = 101  # effectively unreachable: side-project skills
    if (
        candidate.score >= import_score
        and (candidate.has_root_skill or candidate.skill_subdirs)
        and stars >= MIN_STARS
        and (age is not None and age <= 365)
        and not overlap
    ):
        candidate.verdict = "import"
    elif candidate.score < REVIEW_SCORE:
        candidate.verdict = "skip"
    else:
        candidate.verdict = "review"


def detect_overlap(candidate: Candidate, skills: dict[str, dict]) -> str | None:
    """Return a conflict group when the candidate clearly duplicates a curated capability."""
    text = " ".join(
        [candidate.repo, candidate.description, *candidate.skill_subdirs]
    ).lower()
    overlap_rules = [
        ("web-search", ["web search", "search engine", "multi-search", "tavily", "brave search", "serpapi"]),
        ("document-docx", ["docx", "word document", "ms word"]),
        ("document-pdf", ["pdf processing", "pdf tools", "pdf manipulation"]),
        ("document-pptx", ["pptx", "powerpoint", "slide generation"]),
        ("spreadsheet-xlsx", ["xlsx", "excel spreadsheet", "spreadsheet processing"]),
        ("finance-data", ["a-share data", "tushare", "akshare", "chinese stock data"]),
        ("finance-global-data", ["yfinance", "us stock data", "global stock data"]),
        ("image-generation", ["image generation", "text-to-image", "ai image gen"]),
        ("url-extraction", ["url to markdown", "webpage to markdown", "web extraction"]),
        ("email-agent", ["email agent", "agentmail", "send email"]),
        ("browser-automation", ["browser automation", "browser-use", "browser use", "web automation", "playwright"]),
        ("database", ["prisma", "object-relational", "database migration", "sql orm"]),
        ("persistent-memory", ["mem0", "memory context", "persistent memory", "cross-session memory"]),
        ("humanizer", ["humanizer", "humanize text", "de-ai text"]),
        ("video-generation", ["video generation", "text-to-video", "ai video gen"]),
        ("music-generation", ["music generation", "text-to-music", "ai music"]),
        ("mcp-builder", ["mcp server builder", "create mcp", "mcp scaffold"]),
        ("github-automation", ["github automation", "pull request automation", "pr review bot"]),
    ]
    for group, needles in overlap_rules:
        if any(needle in text for needle in needles):
            return group
    return None


# ---------------------------------------------------------------- importing


def detect_aggregator(candidate: Candidate) -> bool:
    """Aggregator stores re-package skills scraped from other repos; the curation
    policy requires native origins, so they never auto-import."""
    text = f"{candidate.repo} {candidate.description}".lower()
    needles = (
        "awesome", "collection of", "curated list", "aggregated", "mirror",
        "收录", "聚合", "商店", "汇总", "精选技能包",
    )
    return any(needle in text for needle in needles)


def register_candidate(candidate: Candidate, token: str | None, apply: bool) -> list[str]:
    """Download SKILL.md (+ support files) for a candidate repo and register it.

    Returns the list of installed skill ids.
    """
    installed: list[str] = []
    targets: list[tuple[str, str]] = []  # (skill_id, remote path or "")
    if candidate.has_root_skill:
        repo_name = re.sub(r"[^a-z0-9-]+", "-", candidate.repo.lower()).strip("-")
        targets.append((repo_name, ""))
    for dirname in candidate.skill_subdirs[:5]:
        skill_id = Path(dirname).name
        if skill_id.startswith("_"):
            continue
        targets.append((skill_id, dirname))
    for skill_id, remote_path in targets:
        destination = SKILLS_DIR / skill_id
        if destination.exists():
            continue
        files = collect_skill_files(candidate, remote_path, token)
        if not files:
            continue
        total = sum(size for _, size in files)
        if len(files) > MAX_IMPORT_FILES or total > MAX_IMPORT_BYTES:
            continue
        if not apply:
            installed.append(skill_id)
            continue
        destination.mkdir(parents=True, exist_ok=True)
        for rel_path, size in files:
            data = raw_file_bytes(candidate.owner, candidate.repo, candidate.default_branch, rel_path, token)
            if data is None:
                continue
            target = destination / Path(rel_path).name if not remote_path else destination / Path(rel_path).relative_to(remote_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        source_text = "\n".join([
            f"Source: {candidate.url}",
            f"Base source commit: {candidate.default_branch} @ {today()}",
            f"License: {candidate.license or 'unspecified (verify before redistribution)'}",
            f"Stars at import: {candidate.stars}",
            f"Imported by: scripts/weekly_curation.py on {today()} (score {candidate.score}).",
        ])
        (destination / "SOURCE.txt").write_text(source_text + "\n", encoding="utf-8")
        installed.append(skill_id)
    if apply and installed:
        write_catalog_registration(candidate, installed)
        write_review_note(candidate, installed)
    return installed


def collect_skill_files(candidate: Candidate, remote_path: str, token: str | None) -> list[tuple[str, int]]:
    prefix = f"{remote_path}/" if remote_path else ""
    tree = api_get(
        f"/repos/{candidate.owner}/{candidate.repo}/git/trees/{candidate.default_branch}?recursive=1",
        token,
    )
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        return []
    selected = []
    for item in tree["tree"]:
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        if prefix and not path.startswith(prefix):
            continue
        parts = Path(path).parts
        if any(part in EXCLUDED_PARTS for part in parts):
            continue
        if not prefix and len(parts) > 1 and parts[0] not in SKILL_DIR_NAMES:
            continue
        if prefix and len(parts) - len(Path(prefix).parts) > 2:
            continue
        name = Path(path).name
        if prefix or name in SKILL_FILE_NAMES or path.endswith(".md"):
            selected.append((path, item.get("size") or 0))
    has_skill_md = any(Path(p).name == "SKILL.md" for p, _ in selected)
    if not has_skill_md:
        return []
    return selected


def write_catalog_registration(candidate: Candidate, installed: list[str]) -> None:
    catalog = load_json(DEFAULT_CATALOG, {})
    tiers = catalog.setdefault("tiers", {})
    high = tiers.setdefault("high", {"id": "high", "title": "High", "description": "", "skills": []})
    existing = {item["id"] for item in high.get("skills", [])}
    for skill_id in installed:
        if skill_id in existing:
            continue
        high["skills"].append({
            "id": skill_id,
            "name": skill_id,
            "description": candidate.description or f"Imported from {candidate.owner}/{candidate.repo}.",
            "manual": f"skills/default/{skill_id}/SKILL.md",
            "source": candidate.url,
            "requires_api_keys": False,
            "api_keys": [],
            "groups": [],
        })
    DEFAULT_CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    overrides = load_json(ORIGIN_OVERRIDES, {})
    changed = False
    for skill_id in installed:
        if skill_id not in overrides:
            overrides[skill_id] = candidate.url
            changed = True
    if changed:
        ORIGIN_OVERRIDES.write_text(json.dumps(overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_review_note(candidate: Candidate, installed: list[str]) -> None:
    DISCOVERY_DIR.mkdir(parents=True, exist_ok=True)
    name = installed[0] if len(installed) == 1 else re.sub(r"[^a-z0-9-]+", "-", candidate.repo.lower()).strip("-")
    path = DISCOVERY_DIR / f"{name}-review-{today()}.md"
    lines = [
        f"# Review: {candidate.owner}/{candidate.repo}",
        "",
        f"- URL: {candidate.url}",
        f"- Stars: {candidate.stars} | Forks: {candidate.forks} | License: {candidate.license or 'unknown'}",
        f"- Last push: {candidate.pushed_at or 'unknown'}",
        f"- Auto score: {candidate.score} ({candidate.verdict})",
        f"- Breakdown: {candidate.breakdown}",
        f"- Imported skills: {', '.join(installed) or 'none'}",
        "",
        "## Notes",
        "",
        "Auto-imported by the weekly curation pipeline. Re-run manual scoring",
        "during the next monthly review to confirm the rating.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- pruning


def prune_checks(token: str | None, apply: bool) -> dict:
    skills = load_enriched_index()
    suggestions = []

    # 1. Dead upstreams (GitHub 404/Gone).
    checked = 0
    for skill_id, item in sorted(skills.items()):
        if item.get("preset_excluded"):
            continue
        url = (item.get("origin") or {}).get("origin_url") or ""
        match = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/|$)", url)
        if not match:
            continue
        owner, repo = match.groups()
        repo_data = api_get(f"/repos/{owner}/{repo}", token)
        checked += 1
        if repo_data is None:
            suggestions.append({
                "skill": skill_id,
                "reason": "upstream_gone",
                "detail": f"{owner}/{repo} is gone or inaccessible",
            })
        time.sleep(0.3)

    # 2. Low internal score.
    for skill_id, item in sorted(skills.items()):
        if item.get("preset_excluded"):
            continue
        score = item.get("rating", {}).get("score", 0)
        if score < REMOVE_SCORE:
            suggestions.append({
                "skill": skill_id,
                "reason": "low_score",
                "detail": f"internal score {score} < {REMOVE_SCORE}",
            })

    # 3. Dominated duplicates inside the same conflict group.
    groups: dict[str, list[tuple[str, int]]] = {}
    for skill_id, item in skills.items():
        if item.get("preset_excluded"):
            continue
        groups.setdefault(item.get("conflict_group") or skill_id, []).append(
            (skill_id, item.get("rating", {}).get("score", 0))
        )
    for group, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        best_score = max(score for _, score in members)
        for skill_id, score in members:
            if best_score - score >= DOMINATED_GAP and score <= DOMINATED_MAX_SCORE:
                suggestions.append({
                    "skill": skill_id,
                    "reason": "dominated_duplicate",
                    "detail": f"conflict group '{group}' has a member scoring {best_score}",
                })

    applied = []
    if apply:
        for suggestion in suggestions:
            if remove_skill(suggestion["skill"]):
                applied.append(suggestion["skill"])
    return {"checked_upstreams": checked, "suggestions": suggestions, "applied": applied}


def remove_skill(skill_id: str) -> bool:
    """Remove a skill from the catalog and delete its local directory."""
    catalog = load_json(DEFAULT_CATALOG, {})
    removed = False
    for tier in catalog.get("tiers", {}).values():
        skills = tier.get("skills", [])
        before = len(skills)
        tier["skills"] = [item for item in skills if item.get("id") != skill_id]
        if len(tier["skills"]) != before:
            removed = True
    if not removed:
        return False
    DEFAULT_CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    destination = SKILLS_DIR / skill_id
    if destination.exists():
        subprocess.run(["rm", "-rf", str(destination)], check=False)
    return True


# ---------------------------------------------------------------- reporting


def write_discovery_report(candidates: list[Candidate], imported: list[str]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = today()
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "thresholds": {"import": IMPORT_SCORE, "review": REVIEW_SCORE, "remove": REMOVE_SCORE},
        "candidates": [asdict(item) for item in candidates],
        "imported": imported,
    }
    json_path = REPORT_DIR / f"discovery-{stamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Weekly Skills Discovery {stamp}",
        "",
        f"- Candidates evaluated: {len(candidates)}",
        f"- Import verdicts: {sum(1 for c in candidates if c.verdict == 'import')}",
        f"- Review verdicts: {sum(1 for c in candidates if c.verdict == 'review')}",
        f"- Imported now: {len(imported)} ({', '.join(imported) if imported else 'none'})",
        "",
        "| Repo | Stars | Score | Verdict | Overlap | License |",
        "|---|---:|---:|---|---|---|",
    ]
    for item in sorted(candidates, key=lambda c: -c.score)[:40]:
        lines.append(
            f"| [{item.owner}/{item.repo}]({item.url}) | {item.stars} | {item.score} | "
            f"`{item.verdict}` | {item.overlap or '-'} | {item.license or '-'} |"
        )
    md_path = REPORT_DIR / f"discovery-{stamp}.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path


def write_prune_report(result: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = today()
    payload = {"generated_at": datetime.now().isoformat(timespec="seconds"), **result}
    json_path = REPORT_DIR / f"prune-{stamp}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Weekly Skills Prune {stamp}",
        "",
        f"- Upstreams checked: {result['checked_upstreams']}",
        f"- Removal suggestions: {len(result['suggestions'])}",
        f"- Applied removals: {len(result['applied'])}",
        "",
        "| Skill | Reason | Detail |",
        "|---|---|---|",
    ]
    for item in result["suggestions"]:
        lines.append(f"| `{item['skill']}` | `{item['reason']}` | {item['detail']} |")
    md_path = REPORT_DIR / f"prune-{stamp}.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path


# ---------------------------------------------------------------- commands


def cmd_discover(args: argparse.Namespace) -> int:
    token = gh_token()
    skills = load_enriched_index()
    known = known_github_repos(skills)
    raw_repos = search_github(token)
    candidates: list[Candidate] = []
    for index, repo in enumerate(raw_repos, start=1):
        full_name = (repo.get("full_name") or "").lower()
        if full_name in known or repo.get("fork"):
            continue
        candidate = Candidate(
            owner=full_name.split("/")[0],
            repo=full_name.split("/")[1],
            url=repo.get("html_url") or f"https://github.com/{full_name}",
            stars=repo.get("stargazers_count") or 0,
            forks=repo.get("forks_count") or 0,
            pushed_at=repo.get("pushed_at") or "",
            description=repo.get("description") or "",
            topics=repo.get("topics") or [],
            license=(repo.get("license") or {}).get("spdx_id"),
            default_branch=repo.get("default_branch") or "main",
        )
        age = days_since(candidate.pushed_at)
        if candidate.stars < MIN_STARS or (age is not None and age > 540):
            continue
        print(f"[{index}/{len(raw_repos)}] inspecting {full_name}", file=sys.stderr, flush=True)
        inspect_repo_structure(candidate, token)
        if not candidate.has_root_skill and not candidate.skill_subdirs:
            continue
        score_candidate(candidate, skills)
        candidates.append(candidate)
        time.sleep(0.5)

    imported: list[str] = []
    if args.import_approved:
        approved = [c for c in candidates if c.verdict == "import"]
        approved.sort(key=lambda c: -c.score)
        for candidate in approved[:MAX_WEEKLY_IMPORTS]:
            print(f"[IMPORT] {candidate.owner}/{candidate.repo} (score {candidate.score})", file=sys.stderr, flush=True)
            imported.extend(register_candidate(candidate, token, apply=True))
        deferred = len(approved) - min(len(approved), MAX_WEEKLY_IMPORTS)
        if deferred > 0:
            print(
                f"[INFO] {deferred} import-approved candidates deferred to manual review "
                f"(weekly auto-import cap is {MAX_WEEKLY_IMPORTS})",
                file=sys.stderr,
                flush=True,
            )

    report = write_discovery_report(candidates, imported)
    summary = {
        "candidates": len(candidates),
        "import_verdicts": sum(1 for c in candidates if c.verdict == "import"),
        "review_verdicts": sum(1 for c in candidates if c.verdict == "review"),
        "imported": imported,
        "report": str(report.relative_to(ROOT)),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


def cmd_prune(args: argparse.Namespace) -> int:
    token = gh_token()
    result = prune_checks(token, apply=args.apply)
    report = write_prune_report(result)
    print(json.dumps({
        "checked_upstreams": result["checked_upstreams"],
        "suggestions": len(result["suggestions"]),
        "applied": result["applied"],
        "report": str(report.relative_to(ROOT)),
    }, ensure_ascii=False))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    discover_args = argparse.Namespace(import_approved=True)
    prune_args = argparse.Namespace(apply=args.apply_prune)
    cmd_discover(discover_args)
    cmd_prune(prune_args)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_discover = sub.add_parser("discover", help="search GitHub and score new candidates")
    p_discover.add_argument("--import-approved", action="store_true", help="auto-import candidates scoring >= %d" % IMPORT_SCORE)
    p_discover.set_defaults(func=cmd_discover)

    p_prune = sub.add_parser("prune", help="check existing skills for removal")
    p_prune.add_argument("--apply", action="store_true", help="perform the removals instead of only suggesting")
    p_prune.set_defaults(func=cmd_prune)

    p_run = sub.add_parser("run", help="full weekly pass: discover+import, then prune")
    p_run.add_argument("--apply-prune", action="store_true", help="apply prune removals")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
