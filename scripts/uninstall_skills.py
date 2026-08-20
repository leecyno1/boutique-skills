#!/usr/bin/env python3
"""Execute the pending skill cleanup after user confirmation.

Reads reports/usage/pending-cleanup.json (written by
scripts/usage_recommendations.py, status=pending) and uninstalls the listed
skills by MOVING them into the runtime's own archive directory
(e.g. ~/.codex/skills/<name> -> ~/.codex/skills-archive/<name>), matching the
Codex CLI's own archive convention. Nothing is deleted, so any uninstall can
be undone by moving the directory back.

Default run is a dry-run preview; pass --confirm to execute. Active skills
(recent telemetry usage) are refused as a final safety net.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "usage"
PENDING_PATH = REPORT_DIR / "pending-cleanup.json"
RECEIPT_PATH = REPORT_DIR / "cleanup-receipts.jsonl"


def archive_dir_for(skill_path: Path) -> Path:
    """Sibling archive root: <skills-root>-archive/."""
    return skill_path.parent.with_name(skill_path.parent.name + "-archive")


def load_pending() -> dict:
    if not PENDING_PATH.exists():
        return {}
    try:
        return json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def active_skills() -> set[str]:
    """Skill names with calls in the recent window of the latest usage report."""
    files = sorted(
        f for f in REPORT_DIR.glob("usage-*.json")
        if re.fullmatch(r"usage-\d{4}-\d{2}-\d{2}\.json", f.name)
    )
    if not files:
        return set()
    try:
        data = json.loads(files[-1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {name for name, entry in data.get("skills", {}).items() if entry.get("recent_calls", 0) > 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--confirm", action="store_true", help="execute the pending uninstall (default: dry-run preview)")
    args = parser.parse_args()

    pending = load_pending()
    if not pending:
        print(json.dumps({"error": "no pending cleanup found", "path": str(PENDING_PATH)}, ensure_ascii=False))
        return 1
    if pending.get("status") != "pending":
        print(json.dumps({"error": f"pending cleanup status is {pending.get('status')!r}, not 'pending'"}, ensure_ascii=False))
        return 1

    active = active_skills()
    results = []
    for item in pending.get("items", []):
        skill = item["skill"]
        src = Path(item["path"])
        record = {"skill": skill, "runtime": item.get("runtime"), "from": str(src)}
        if skill in active:
            record.update({"action": "refused", "reason": "skill has recent usage; safety net refused removal"})
        elif not src.exists() or not (src / "SKILL.md").exists():
            record.update({"action": "skipped", "reason": "not installed at recorded path"})
        else:
            archive = archive_dir_for(src)
            dest = archive / skill
            if dest.exists():
                dest = archive / f"{skill}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            if args.confirm:
                archive.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))
                record.update({"action": "archived", "to": str(dest)})
            else:
                record.update({"action": "would_archive", "to": str(dest)})
        results.append(record)

    executed = [r for r in results if r["action"] == "archived"]
    refused = [r for r in results if r["action"] == "refused"]
    skipped = [r for r in results if r["action"] == "skipped"]
    planned = [r for r in results if r["action"] == "would_archive"]

    if args.confirm:
        pending["status"] = "executed" if not planned else "partial"
        pending["executed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        pending["results"] = results
        PENDING_PATH.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if executed:
            receipt = {
                "executed_at": pending["executed_at"],
                "items": [{"skill": r["skill"], "from": r["from"], "to": r["to"]} for r in executed],
            }
            with open(RECEIPT_PATH, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")

    print(json.dumps({
        "mode": "confirm" if args.confirm else "dry-run",
        "items": len(results),
        "archived": len(executed),
        "refused_active": len(refused),
        "skipped_missing": len(skipped),
        "planned": len(planned),
        "receipt": str(RECEIPT_PATH.relative_to(ROOT)) if executed else None,
        "undo": "mv <archive>/<skill> <original path> 恢复；归档目录与技能根同级（*-archive）",
    }, ensure_ascii=False))
    for r in results[:40]:
        print(f"  [{r['action']}] {r['skill']} ({r.get('runtime')}) -> {r.get('to') or r.get('reason')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
