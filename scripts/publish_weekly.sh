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
  .gitignore \
  README.md \
  QODER_HANDOFF.md \
  findings.md \
  task_plan.md \
  Makefile \
  assets/ \
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

# Some networks cut git's own TLS handshake to github.com (LibreSSL
# SSL_ERROR_SYSCALL) while plain curl to the same host still works, which used
# to abort the publish step and leave GitHub behind Gitee. Fall back to SSH.
ssh_url_for() {
  case "$1" in
    https://github.com/*) echo "git@github.com:${1#https://github.com/}" ;;
    *) echo "" ;;
  esac
}

push_remote() {
  local remote="$1" url fallback
  url="$(git remote get-url "$remote")"
  if git push "$remote" main; then
    return 0
  fi
  fallback="$(ssh_url_for "$url")"
  if [[ -z "$fallback" ]]; then
    echo "[ERROR] push to $remote failed and no SSH fallback exists for $url" >&2
    return 1
  fi
  echo "[WARN] HTTPS push to $remote failed; retrying over SSH: $fallback"
  GIT_SSH_COMMAND="ssh -o ConnectTimeout=20" git push "$fallback" main || return 1
  # Keep the remote-tracking ref truthful even though the push bypassed it.
  GIT_SSH_COMMAND="ssh -o ConnectTimeout=20" \
    git fetch "$fallback" "main:refs/remotes/${remote}/main" --quiet || true
}

resolve_remote_head() {
  local remote="$1" url fallback sha
  url="$(git remote get-url "$remote")"
  sha="$(git ls-remote "$url" main 2>/dev/null | cut -f1)"
  if [[ -z "$sha" ]]; then
    fallback="$(ssh_url_for "$url")"
    if [[ -n "$fallback" ]]; then
      sha="$(GIT_SSH_COMMAND="ssh -o ConnectTimeout=20" git ls-remote "$fallback" main 2>/dev/null | cut -f1)"
    fi
  fi
  if [[ -z "$sha" ]]; then
    echo "[ERROR] cannot resolve $remote main; both HTTPS and SSH failed" >&2
    return 1
  fi
  echo "$sha"
}

echo "[INFO] pushing GitHub (origin)"
push_remote origin

echo "[INFO] pushing Gitee (gitee)"
push_remote gitee

HEAD_SHA="$(git rev-parse HEAD)"
ORIGIN_SHA="$(resolve_remote_head origin)"
GITEE_SHA="$(resolve_remote_head gitee)"
echo "[INFO] HEAD:        $HEAD_SHA"
echo "[INFO] origin/main: $ORIGIN_SHA"
echo "[INFO] gitee/main:  $GITEE_SHA"

if [[ "$HEAD_SHA" == "$ORIGIN_SHA" && "$HEAD_SHA" == "$GITEE_SHA" ]]; then
  echo "[DONE] GitHub and Gitee are in sync."
else
  echo "[ERROR] remotes diverge; check manually" >&2
  exit 1
fi
