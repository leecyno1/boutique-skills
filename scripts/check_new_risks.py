#!/usr/bin/env python3
"""Fail the weekly cycle when the audit finds risky patterns we have not accepted.

Upstream sync imports third-party skill content without human review. The catalog
audit already scans those files, but its exit code only reflects structural
problems, so new `curl | sh`, `eval(` or credential-reading lines would ship
silently. This gate compares the audit's (skill, file, pattern) triples with
catalog/risky-baseline.json and exits non-zero on anything new.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "reports" / "audit-latest.json"
DEFAULT_BASELINE = ROOT / "catalog" / "risky-baseline.json"


def relative(path, root):
    text = str(path)
    prefix = str(root) + "/"
    return text[len(prefix):] if text.startswith(prefix) else text


def triples(report, root):
    return {
        (item["skill"], relative(item["file"], root), item["pattern"])
        for item in report.get("risky") or []
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", default=str(DEFAULT_AUDIT))
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    args = parser.parse_args()

    audit = json.loads(Path(args.audit).read_text(encoding="utf-8"))
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    known = {(e["skill"], e["file"], e["pattern"]) for e in baseline.get("entries", [])}
    current = triples(audit, ROOT)
    new = sorted(current - known)
    gone = sorted(known - current)

    print(
        json.dumps(
            {"current": len(current), "baseline": len(known), "new": len(new), "resolved": len(gone)},
            ensure_ascii=False,
        )
    )
    for skill, file, pattern in new:
        print(f"[NEW RISK] {skill} :: {file} :: {pattern}")
    if gone:
        print(f"[INFO] {len(gone)} baseline entries no longer appear; prune them when convenient")
    if new:
        print(
            "[FAIL] new risky patterns introduced; review them, then either remove the skill "
            "or add the triples to catalog/risky-baseline.json with a reason in findings.md"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
