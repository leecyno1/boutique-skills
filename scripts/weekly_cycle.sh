#!/usr/bin/env bash
# Weekly skills curation cycle.
#
# Pipeline: discover+import -> prune -> rebuild catalogs -> refresh finance
# suite -> audit -> tests -> publish to GitHub and Gitee.
#
# Thresholds (see scripts/weekly_curation.py):
#   import: candidate score >= 75, has SKILL.md, >= 20 stars, active, no overlap
#   prune:  upstream gone / internal score < 60 / dominated duplicate
#           (same conflict group, gap >= 15, weaker side <= 70)
# Bundles: standard bundle <= 40 base skills; finance suite <= 40 skills.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

STAMP="$(date +%F)"

echo "=== [1/9] Discover and import new GitHub skills ==="
python3 scripts/weekly_curation.py discover --import-approved

echo "=== [2/9] Prune dead/low-score/dominated skills ==="
python3 scripts/weekly_curation.py prune --apply

echo "=== [3/9] Collect local skill usage telemetry ==="
python3 scripts/telemetry_collect.py --days 30

echo "=== [4/9] Rebuild enriched catalog and standard bundle ==="
python3 scripts/generate_enriched_catalog.py

echo "=== [5/9] Refresh finance investment suite (<= 40 skills) ==="
python3 scripts/generate_finance_suite.py

echo "=== [6/9] Regenerate README with new suite sizes ==="
python3 scripts/generate_enriched_catalog.py

echo "=== [7/9] Refresh usage report with new bundles ==="
python3 scripts/telemetry_collect.py --days 30

echo "=== [8/9] Audit and tests ==="
python3 scripts/audit_skills.py
python3 tests/test_governance_files.py
python3 tests/test_tier_catalog.py

echo "=== [9/9] Publish to GitHub and Gitee ==="
./scripts/publish_weekly.sh "Weekly skills curation ${STAMP}: discover, score, prune, refresh bundles"

echo "[DONE] weekly cycle complete for ${STAMP}"
