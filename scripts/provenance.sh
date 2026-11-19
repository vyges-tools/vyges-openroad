#!/usr/bin/env bash
# provenance.sh — emit manifest.json for the commit being built. Run inside the
# build tree (/OpenROAD present). CI fills image_digest + build_date afterwards.
# Env: OR_COMMIT (required), VERSION (optional).
set -euo pipefail
: "${OR_COMMIT:?set OR_COMMIT}"
VERSION="${VERSION:-dev}"
OR_TREE="${OR_TREE:-/OpenROAD}"

sub() { git -C "$OR_TREE" submodule status "$1" 2>/dev/null | awk '{print $1}' | tr -d '+-' ; }
# OpenSTA is openroad/sta since upstream's src/ -> openroad/ rename (37a84d0a3e, 2026-11-17).
STA_PATH=openroad/sta; [ -e "$OR_TREE/openroad/sta" ] || STA_PATH=src/sta

cat <<JSON
{
  "schema": "vyges-openroad-manifest/1.0",
  "version": "${VERSION}",
  "upstream_commit": "${OR_COMMIT}",
  "submodule_shas": {
    "sta":   "$(sub "$STA_PATH")",
    "abc":   "$(sub third-party/abc)",
    "slang": "$(sub third-party/slang-elab)"
  },
  "base_image": "ubuntu:24.04",
  "build_flags": "-no-gui -no-tests",
  "image_digest": null,
  "build_date": null
}
JSON
