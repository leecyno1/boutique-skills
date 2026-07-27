#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "catalog" / "skills.json"
PROFILES_DIR = REPO_ROOT / "profiles"
SUITES_DIR = REPO_ROOT / "catalog" / "suites"


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_profile(profile_id: str) -> dict:
    p = PROFILES_DIR / f"{profile_id}.json"
    if not p.exists():
        raise FileNotFoundError(f"Profile not found: {profile_id}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_suite(suite_id: str) -> dict:
    p = SUITES_DIR / f"{suite_id}.json"
    if not p.exists():
        raise FileNotFoundError(f"Suite not found: {suite_id}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def index_by_capability(catalog: dict) -> Dict[str, dict]:
    index = {}
    for item in catalog.get("skills", []):
        cap = item["capability"]
        if cap in index:
            raise ValueError(f"Duplicate capability in catalog: {cap}")
        index[cap] = item
    return index


def resolve_profile_skills(profile_id: str) -> List[str]:
    catalog = load_catalog()
    profile = load_profile(profile_id)
    idx = index_by_capability(catalog)
    resolved = []
    seen = set()

    def add_skill(skill: str) -> None:
        if skill and skill not in seen:
            seen.add(skill)
            resolved.append(skill)

    for cap in profile.get("capabilities", []):
        if cap not in idx:
            raise KeyError(f"Profile {profile_id} references unknown capability: {cap}")
        add_skill(idx[cap]["skill"])
    for extra in profile.get("extra_skills", []):
        add_skill(extra)
    for skill in profile.get("skills", []):
        add_skill(skill)
    for suite_ref in profile.get("skill_suites", []):
        suite = suite_ref
        if isinstance(suite_ref, str):
            suite = load_suite(suite_ref)
        for skill in suite.get("skills", []):
            add_skill(skill)
    return resolved


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Resolve boutique-skills profiles")
    parser.add_argument("profile", help="Profile ID, e.g. core")
    args = parser.parse_args()

    for s in resolve_profile_skills(args.profile):
        print(s)


if __name__ == "__main__":
    main()
