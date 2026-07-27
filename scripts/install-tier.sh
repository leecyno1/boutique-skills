#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/install-tier.sh <low|medium|high> [--dry-run]

Install one of the curated default skill tiers from this repository.
- low: stable baseline
- medium: production extensions
- high: full expert pack
EOF
}

if [[ $# -lt 1 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

TIER="$1"
DRY_RUN="false"
if [[ "${2:-}" == "--dry-run" ]]; then
  DRY_RUN="true"
fi

case "$TIER" in
  low|medium|high) ;;
  *) echo "[ERROR] unknown tier: $TIER" >&2; usage >&2; exit 1 ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
TIER_JSON="$REPO_ROOT/tiers/$TIER.json"
SOURCE_DIR="$REPO_ROOT/skills/default"

if [[ ! -f "$TIER_JSON" ]]; then
  echo "[ERROR] missing tier file: $TIER_JSON" >&2
  exit 1
fi

SKILLS=()
while IFS= read -r skill; do
  [[ -n "$skill" ]] && SKILLS+=("$skill")
done < <(python3 - <<'PY' "$TIER_JSON"
import json, sys
payload=json.load(open(sys.argv[1], encoding='utf-8'))
for item in payload.get('skills', []):
    print(item['id'])
PY
)

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "[ERROR] tier '$TIER' has no skills" >&2
  exit 1
fi

echo "[INFO] Tier: $TIER"
echo "[INFO] Skills: ${#SKILLS[@]}"
echo "[INFO] Target: $TARGET"
mkdir -p "$TARGET"

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill"
  dst="$TARGET/$skill"
  if [[ ! -d "$src" ]]; then
    echo "[WARN] missing local skill source: $skill" >&2
    continue
  fi
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] sync $src -> $dst"
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "[INSTALL] $skill"
  fi
done

echo "[DONE] Tier '$TIER' processed."
