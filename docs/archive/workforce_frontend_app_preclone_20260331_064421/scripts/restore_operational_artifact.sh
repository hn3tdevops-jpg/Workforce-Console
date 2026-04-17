#!/usr/bin/env bash
set -euo pipefail

# Restore an archived operational artifact into the repo dist/ directory.
# Usage: scripts/restore_operational_artifact.sh "artifacts/operational/<timestamp>"

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <archive-dir-relative-or-absolute>"
  echo "Example: $0 artifacts/operational/20260331T022757Z"
  exit 2
fi

ARCHIVE_DIR="$1"
TARGET_DIR="dist"

if [ ! -d "$ARCHIVE_DIR" ]; then
  echo "Archive directory not found: $ARCHIVE_DIR"
  exit 3
fi

echo "Restoring archive from $ARCHIVE_DIR -> $TARGET_DIR"
rsync -av --delete "$ARCHIVE_DIR"/ "$TARGET_DIR"/

# Compute checksums of restored files for operator verification
TMP_CHECKSUMS="/tmp/restore-checksums-$(date -u +%Y%m%dT%H%M%SZ).txt"
(
  pushd "$TARGET_DIR" >/dev/null
  find . -type f -print0 | xargs -0 sha256sum > "$TMP_CHECKSUMS"
  popd >/dev/null
)

ARCHIVE_CHECKSUMS="${ARCHIVE_DIR}-checksums.txt"
if [ -f "$ARCHIVE_CHECKSUMS" ]; then
  echo "Archive checksum file found: $ARCHIVE_CHECKSUMS"
  echo "Computed restored checksums: $TMP_CHECKSUMS"
  echo "To compare: diff -u \"$ARCHIVE_CHECKSUMS\" \"$TMP_CHECKSUMS\" || true"
else
  echo "No archive checksum file found at: $ARCHIVE_CHECKSUMS"
  echo "Computed restored checksums: $TMP_CHECKSUMS"
fi

echo "Restore complete. Ensure wrapper process (app.py) is restarted and run smoke tests."
exit 0
