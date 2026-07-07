#!/usr/bin/env bash
# smoke.sh — prove a built artifact runs. Accepts a bundle directory OR a docker
# image ref. For a bundle it runs from a FRESH path to prove relocation.
# Usage: scripts/smoke.sh <bundle-dir>|<docker-image>
set -euo pipefail
TARGET="${1:?usage: smoke.sh <bundle-dir>|<docker-image>}"

if [ -d "$TARGET" ]; then
  tmp=$(mktemp -d)
  cp -a "$TARGET" "$tmp/bundle"
  "$tmp/bundle/bin/openroad" -version
  rm -rf "$tmp"
else
  docker run --rm "$TARGET" openroad -version
fi
echo "SMOKE_OK"
