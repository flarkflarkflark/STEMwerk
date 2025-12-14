#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUT_DIR="$ROOT_DIR/installer/macos/dist"
STAGE="$ROOT_DIR/installer/macos/build/root"

VERSION="${STEMWERK_VERSION:-0.0.0}"
PKG_ID="com.flarkaudio.stemwerk"

rm -rf "$OUT_DIR" "$STAGE"
mkdir -p "$OUT_DIR" "$STAGE/Users/Shared/STEMwerk"

# Copy only what we need
rsync -a --delete \
  "$ROOT_DIR/scripts/reaper" \
  "$ROOT_DIR/i18n" \
  "$ROOT_DIR/README.md" \
  "$ROOT_DIR/TODO.md" \
  "$ROOT_DIR/INTEGRATION.md" \
  "$ROOT_DIR/TESTING.md" \
  "$STAGE/Users/Shared/STEMwerk/"

pkgbuild \
  --root "$STAGE" \
  --identifier "$PKG_ID" \
  --version "$VERSION" \
  "$OUT_DIR/STEMwerk-$VERSION.pkg"

echo "Built: $OUT_DIR/STEMwerk-$VERSION.pkg"