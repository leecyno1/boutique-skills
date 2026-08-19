#!/usr/bin/env bash
# Publish weekly curation changes to GitHub and Gitee.
#
# Whitelist add only; never stage the four user-protected tushare-eval files;
# commit, push origin main and gitee main, then verify both remotes.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

GITEE_URL="${GITEE_URL:-https://gitee.com/leecyno1/boutique-openclaw-skills.git}"
COMMIT_MSG="${1:-Weekly skills curation: discover, score, prune, refresh bundles}"

PROTECTED=(
  "reports/finance-skill-eval/tushare-eval/standard-finance-skills-recommendation.json"
  "reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.html"
  "reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.json"
  "reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.md"
)

if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  :
else
  echo "[INFO] nothing to publish"
  exit 0
fi

git add -- \
  README.md \
  QODER_HANDOFF.md \
  Makefile \
  catalog/ \
  categories/ \
  docs/ \
  reports/ \
  skills/ \
  scripts/ \
  tiers/ \
  tests/ \
  2>/dev/null || true

STAGED="$(git diff --cached --name-only)"
if [[ -z "$STAGED" ]]; then
  echo "[INFO] no staged changes after whitelist add"
  exit 0
fi

for file in "${PROTECTED[@]}"; do
  if git diff --cached --name-only | grep -Fxq "$file"; then
    echo "[ERROR] refusing to stage protected file: $file" >&2
    git reset -- "$file" >/dev/null 2>&1 || true
  fi
done

if git diff --cached --name-only | grep -Fxq "${PROTECTED[0]}"; then
  echo "[ERROR] protected files still staged" >&2
  exit 1
fi

if git diff --check; then
  :
else
  echo "[WARN] git diff --check reported whitespace issues; continuing"
fi

git commit -m "$COMMIT_MSG"

if ! git remote | grep -qx gitee; then
  git remote add gitee "$GITEE_URL"
  echo "[INFO] added gitee remote: $GITEE_URL"
fi

echo "[INFO] pushing GitHub (origin)"
git push origin main

echo "[INFO] pushing Gitee (gitee)"
git push gitee main

git fetch origin main --quiet
git fetch gitee main --quiet
echo "[INFO] HEAD:        $(git rev-parse HEAD)"
echo "[INFO] origin/main: $(git rev-parse origin/main)"
echo "[INFO] gitee/main:  $(git rev-parse gitee/main)"

if [[ "$(git rev-parse HEAD)" == "$(git rev-parse origin/main)" \
   && "$(git rev-parse HEAD)" == "$(git rev-parse gitee/main)" ]]; then
  echo "[DONE] GitHub and Gitee are in sync."
else
  echo "[ERROR] remotes diverge; check manually" >&2
  exit 1
fi
