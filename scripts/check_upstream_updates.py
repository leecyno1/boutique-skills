#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ENRICHED_CATALOG = ROOT / "catalog" / "skills.enriched.json"
SKILLS_DIR = ROOT / "skills" / "default"
WRAPPER_ORIGINS = ROOT / "catalog" / "wrapper-origins.json"


def load_wrapper_allowlist() -> set[str]:
    """Skills whose upstream URL is a whole repo or docs page (informational
    origin, not a SKILL.md path). We should not flag them as
    metadata_only_root_no_skill_md when the local SKILL.md exists."""
    try:
        data = json.loads(WRAPPER_ORIGINS.read_text(encoding="utf-8"))
        return set(data.get("wrappers", []))
    except FileNotFoundError:
        return set()


WRAPPER_SKILLS = load_wrapper_allowlist()
MAX_ROOT_FILES = 200
MAX_ROOT_BYTES = 2_000_000
EXCLUDED_PARTS = {".git", "node_modules", "__pycache__", ".next", "dist", ".venv", "canvas-fonts"}
ROOT_SYNC_FILE_NAMES = {
    "SKILL.md",
    "GUIDE.md",
    "README.md",
    "README-zh.md",
    "LICENSE",
    "LICENSE.md",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
}
ROOT_SYNC_DIR_NAMES = {"scripts", "references", "examples", "zh"}
TREE_CACHE: dict[tuple[str, str, str], list[dict]] = {}
REPO_META_CACHE: dict[tuple[str, str], dict] = {}


@dataclass
class GitHubSource:
    skill_id: str
    url: str
    owner: str
    repo: str
    ref: str | None
    path: str
    is_file: bool


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
    token = result.stdout.strip()
    return token or None


def api_get(path: str, token: str | None) -> dict | list | None:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/{path.lstrip('/')}", headers=headers)
    for attempt in range(3):
        try:
            with urlopen(request, timeout=12) as response:
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


def parse_github_url(skill_id: str, url: str | None) -> GitHubSource | None:
    if not url or "github.com" not in url:
        return None
    clean = url.split("#", 1)[0].rstrip("/")
    match = re.match(r"https?://github.com/([^/]+)/([^/]+?)(?:\.git)?(?:/(.*))?$", clean)
    if not match:
        return None
    owner, repo, rest = match.groups()
    if repo.endswith(".git"):
        repo = repo[:-4]
    ref = None
    path = ""
    is_file = False
    parts = (rest or "").split("/")
    if len(parts) >= 3 and parts[0] in {"tree", "blob"}:
        is_file = parts[0] == "blob"
        ref = parts[1]
        path = "/".join(parts[2:])
    return GitHubSource(skill_id, url, owner, repo, ref, path, is_file)


def load_sources() -> list[GitHubSource]:
    catalog = json.loads(ENRICHED_CATALOG.read_text(encoding="utf-8"))
    local_skills = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir()}
    sources = []
    for item in catalog.get("skills", []):
        skill_id = item.get("id")
        if skill_id not in local_skills:
            continue
        origin_url = (item.get("origin") or {}).get("origin_url")
        source = parse_github_url(skill_id, origin_url)
        if source:
            sources.append(source)
    return sources


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha_bytes(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def git_blob_sha_file(path: Path) -> str:
    return git_blob_sha_bytes(path.read_bytes())


def normalize_ref(source: GitHubSource, token: str | None) -> str:
    if source.ref:
        return source.ref
    repo = repo_metadata(source, token)
    if isinstance(repo, dict) and repo.get("default_branch"):
        return repo["default_branch"]
    return "main"


def repo_metadata(source: GitHubSource, token: str | None) -> dict:
    key = (source.owner, source.repo)
    if key in REPO_META_CACHE:
        return REPO_META_CACHE[key]
    repo = api_get(f"/repos/{source.owner}/{source.repo}", token)
    if not isinstance(repo, dict):
        REPO_META_CACHE[key] = {}
        return {}
    REPO_META_CACHE[key] = {
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "pushed_at": repo.get("pushed_at"),
        "updated_at": repo.get("updated_at"),
        "default_branch": repo.get("default_branch"),
        "license": (repo.get("license") or {}).get("spdx_id"),
    }
    return REPO_META_CACHE[key]


def repo_tree(source: GitHubSource, token: str | None, ref: str) -> list[dict]:
    key = (source.owner, source.repo, ref)
    if key in TREE_CACHE:
        return TREE_CACHE[key]
    tree = api_get(f"/repos/{source.owner}/{source.repo}/git/trees/{ref}?recursive=1", token)
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        TREE_CACHE[key] = []
        return []
    files = [
        item for item in tree["tree"]
        if item.get("type") == "blob" and not any(part in EXCLUDED_PARTS for part in Path(item.get("path", "")).parts)
    ]
    TREE_CACHE[key] = files
    return files


def tree_files_for_source(source: GitHubSource, token: str | None, ref: str) -> tuple[str, list[dict]]:
    if source.path:
        files = repo_tree(source, token, ref)
        if not files:
            return "source_path_missing", []
        if source.is_file:
            selected = [item for item in files if item.get("path") == source.path]
        else:
            prefix = source.path.rstrip("/") + "/"
            selected = [item for item in files if item.get("path", "").startswith(prefix)]
        return ("ok", selected) if selected else ("source_path_missing", [])
    query = f"?ref={ref}" if ref else ""
    root = api_get(f"/repos/{source.owner}/{source.repo}/contents{query}", token)
    if not isinstance(root, list):
        return "source_path_missing", []
    if not any(item.get("name") == "SKILL.md" and item.get("type") == "file" for item in root):
        return "metadata_only_root_no_skill_md", []
    files = repo_tree(source, token, ref)
    if not files:
        return "source_path_missing", []
    selected = []
    for item in files:
        path = Path(item["path"])
        if len(path.parts) == 1:
            if path.name in ROOT_SYNC_FILE_NAMES or path.name.endswith(".md"):
                selected.append(item)
        elif path.parts[0] in ROOT_SYNC_DIR_NAMES:
            selected.append(item)
    total_size = sum(item.get("size") or 0 for item in selected)
    if len(selected) > MAX_ROOT_FILES or total_size > MAX_ROOT_BYTES:
        return "metadata_only_root_too_large", selected
    return "ok", sorted(selected, key=lambda item: item["path"])


def list_contents(source: GitHubSource, token: str | None, ref: str, path: str, recursive: bool = True) -> tuple[str, list[dict]]:
    query = f"?ref={ref}" if ref else ""
    encoded_path = "/".join(part for part in path.split("/") if part)
    contents = api_get(f"/repos/{source.owner}/{source.repo}/contents/{encoded_path}{query}", token)
    if contents is None:
        return "source_path_missing", []
    if isinstance(contents, dict) and contents.get("type") == "file":
        return "ok", [contents]
    if not isinstance(contents, list):
        return "unsupported_source", []
    files = []
    stack = contents[:]
    while stack:
        entry = stack.pop()
        if any(part in EXCLUDED_PARTS for part in Path(entry.get("path", "")).parts):
            continue
        if entry.get("type") == "file":
            files.append(entry)
        elif recursive and entry.get("type") == "dir":
            child = api_get(f"/repos/{source.owner}/{source.repo}/contents/{entry['path']}{query}", token)
            if isinstance(child, list):
                stack.extend(child)
    return "ok", sorted(files, key=lambda item: item["path"])


def list_root_skill_contents(source: GitHubSource, token: str | None, ref: str) -> tuple[str, list[dict]]:
    query = f"?ref={ref}" if ref else ""
    root = api_get(f"/repos/{source.owner}/{source.repo}/contents{query}", token)
    if not isinstance(root, list):
        return "source_path_missing", []
    if not any(item.get("name") == "SKILL.md" and item.get("type") == "file" for item in root):
        return "metadata_only_root_no_skill_md", []
    files = [
        item for item in root
        if item.get("type") == "file" and (item.get("name") in ROOT_SYNC_FILE_NAMES or item.get("name", "").endswith(".md"))
    ]
    for item in root:
        if item.get("type") != "dir" or item.get("name") not in ROOT_SYNC_DIR_NAMES:
            continue
        status, child_files = list_contents(source, token, ref, item["path"], recursive=True)
        if status == "ok":
            files.extend(child_files)
    total_size = sum(item.get("size") or 0 for item in files)
    if len(files) > MAX_ROOT_FILES or total_size > MAX_ROOT_BYTES:
        return "metadata_only_root_too_large", files
    return "ok", sorted(files, key=lambda item: item["path"])


def file_bytes(entry: dict, token: str | None) -> bytes | None:
    content = entry.get("content")
    if content and entry.get("encoding") == "base64":
        return base64.b64decode(content)
    download_url = entry.get("download_url")
    if not download_url:
        hydrated = api_get(entry["url"].replace("https://api.github.com", ""), token)
        if isinstance(hydrated, dict):
            return file_bytes(hydrated, token)
        return None
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(download_url, headers=headers), timeout=45) as response:
        return response.read()


def raw_file_bytes(source: GitHubSource, token: str | None, ref: str, path: str) -> bytes:
    raw_url = f"https://raw.githubusercontent.com/{source.owner}/{source.repo}/{ref}/{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(raw_url, headers=headers), timeout=12) as response:
        return response.read()


def relative_target(source: GitHubSource, entry: dict, base_path: str) -> Path:
    if source.is_file:
        return Path(Path(entry["path"]).name)
    entry_path = Path(entry["path"])
    if base_path:
        return entry_path.relative_to(base_path)
    return entry_path


def check_source(source: GitHubSource, token: str | None, apply: bool) -> dict:
    ref = normalize_ref(source, token)
    metadata = repo_metadata(source, token)
    base_path = source.path
    status, files = tree_files_for_source(source, token, ref)
    if status != "ok":
        if (
            status == "metadata_only_root_no_skill_md"
            and source.skill_id in WRAPPER_SKILLS
            and (SKILLS_DIR / source.skill_id / "SKILL.md").exists()
        ):
            status = "wrapper_origin"
        return {**asdict(source), "status": status, "ref": ref, "upstream": metadata, "changed": [], "added": [], "same": 0}
    changed = []
    added = []
    same = 0
    destination = SKILLS_DIR / source.skill_id
    for entry in files:
        rel = relative_target(source, entry, base_path)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        target = destination / rel
        if not target.exists():
            added.append(str(target.relative_to(ROOT)))
            needs_write = True
        elif entry.get("sha") != git_blob_sha_file(target):
            changed.append(str(target.relative_to(ROOT)))
            needs_write = True
        else:
            same += 1
            needs_write = False
        if apply and needs_write:
            data = raw_file_bytes(source, token, ref, entry["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    return {
        **asdict(source),
        "status": "updated" if apply and (changed or added) else "would_update" if (changed or added) else "current",
        "ref": ref,
        "upstream": metadata,
        "changed": changed,
        "added": added,
        "same": same,
    }


def write_reports(results: list[dict], output: Path) -> None:
    summary: dict[str, int] = {}
    for item in results:
        summary[item["status"]] = summary.get(item["status"], 0) + 1
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "checked": len(results),
        "summary": dict(sorted(summary.items())),
        "results": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = output.with_suffix(".md")
    lines = [
        "# Upstream Skill Update Check",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Checked GitHub-backed local skills: `{len(results)}`",
    ]
    for status, count in sorted(summary.items()):
        lines.append(f"- {status}: `{count}`")
    lines.extend(["", "| Skill | Status | Changed | Added | Upstream |", "|---|---|---:|---:|---|"])
    for item in sorted(results, key=lambda r: (r["status"], r["skill_id"])):
        lines.append(
            f"| `{item['skill_id']}` | `{item['status']}` | {len(item.get('changed', []))} | "
            f"{len(item.get('added', []))} | [{item['owner']}/{item['repo']}]({item['url']}) |"
        )
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check and optionally sync GitHub-backed skill sources.")
    parser.add_argument("--apply", action="store_true", help="copy changed upstream files into skills/default")
    parser.add_argument("--output", default=str(ROOT / "reports" / "upstream-check-latest.json"))
    args = parser.parse_args()
    token = gh_token()
    results = []
    sources = load_sources()
    for index, source in enumerate(sources, start=1):
        print(f"[{index}/{len(sources)}] {source.skill_id} -> {source.owner}/{source.repo}", file=sys.stderr, flush=True)
        try:
            results.append(check_source(source, token, args.apply))
        except Exception as error:
            results.append({**asdict(source), "status": "error", "error": str(error), "changed": [], "added": [], "same": 0})
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    write_reports(results, output)
    summary = {}
    for item in results:
        summary[item["status"]] = summary.get(item["status"], 0) + 1
    print(json.dumps({"checked": len(results), "summary": dict(sorted(summary.items())), "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
