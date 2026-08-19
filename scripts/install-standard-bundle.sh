#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/install-standard-bundle.sh [--dry-run]

Install the no-duplicate standard skill bundle generated at catalog/standard-bundle.json.
The bundle keeps at most one skill per capability/conflict group and excludes Open/Hermes presets.
USAGE
}

DRY_RUN="false"
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
elif [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="true"
elif [[ $# -gt 0 ]]; then
  echo "[ERROR] unknown argument: $1" >&2
  usage >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
BUNDLE_JSON="$REPO_ROOT/catalog/standard-bundle.json"
SOURCE_DIR="$REPO_ROOT/skills/default"

if [[ ! -f "$BUNDLE_JSON" ]]; then
  echo "[ERROR] missing standard bundle: $BUNDLE_JSON" >&2
  echo "Run: python3 scripts/generate_enriched_catalog.py" >&2
  exit 1
fi

readarray_output="$(python3 - <<'PY' "$BUNDLE_JSON"
import json, sys
payload=json.load(open(sys.argv[1], encoding='utf-8'))
print(int(payload.get('max_skills') or 40))
print(len(payload.get('skills', [])))
for item in payload.get('skills', []):
    print(item['skill'])
PY
)"
MAX_SKILLS="$(printf '%s\n' "$readarray_output" | sed -n '1p')"
BASE_SKILL_COUNT="$(printf '%s\n' "$readarray_output" | sed -n '2p')"
mapfile -t SKILLS < <(printf '%s\n' "$readarray_output" | sed '1,2d' | awk '!seen[$0]++')

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "[ERROR] standard bundle has no skills" >&2
  exit 1
fi

if [[ "$BASE_SKILL_COUNT" -gt "$MAX_SKILLS" ]]; then
  echo "[ERROR] standard bundle has more than $MAX_SKILLS base skills" >&2
  exit 1
fi

if [[ ${#SKILLS[@]} -gt 40 ]]; then
  echo "[ERROR] standard bundle installs ${#SKILLS[@]} skills; the cap is 40" >&2
  exit 1
fi

echo "[INFO] Standard bundle skills: ${#SKILLS[@]} (base only; skill_packs are reference recommendations)"
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

echo "[DONE] Standard bundle processed."
