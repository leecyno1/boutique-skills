#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST="$REPO_ROOT/dist"
mkdir -p "$DIST"
TS="$(date +%Y%m%d-%H%M%S)"
NAME="boutique-skills-$TS.tar.gz"

tar -czf "$DIST/$NAME" \
  -C "$REPO_ROOT" \
  README.md LICENSE catalog profiles tiers skills scripts docs assets .github

echo "$DIST/$NAME"
