#!/usr/bin/env bash
# smoke.sh — prove a built artifact runs. Accepts a bundle directory OR a docker
# image ref. For a bundle it runs from a FRESH path to prove relocation.
# Usage: scripts/smoke.sh <bundle-dir>|<docker-image>
set -euo pipefail
TARGET="${1:?usage: smoke.sh <bundle-dir>|<docker-image>}"

# ⛔ `-version` never starts the Python interpreter, so it passed an image whose
# `openroad -python` was broken (no stdlib) and would pass a binary built without
# Python at all. LibreLane runs every odb step as `openroad -python`, so the smoke
# does too: the script must import odb, build a database and write a marker file.
# (print() is not used: a half-initialised interpreter loses sys.stdout.)
pysmoke() { # dir holding pysmoke.py; runs "$@" <script>; checks the marker
  local d=$1; shift
  cat > "$d/pysmoke.py" <<'PY'
import openroad
import odb
assert odb.dbDatabase.create() is not None
import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ok"), "w") as f:
    f.write("PY_SMOKE_OK")
PY
  rm -f "$d/ok"
  "$@" "$d/pysmoke.py" >/dev/null 2>&1 || true
  [ "$(cat "$d/ok" 2>/dev/null)" = "PY_SMOKE_OK" ] || { echo "SMOKE_FAIL: openroad -python did not run a script"; exit 1; }
  echo "python: ok"
}

# The Bazel //:openroad is built without Python (banner "-Python"); Python under
# Bazel is the openroad wheel in a venv (OpenROAD#11566). Require the -python run
# only of a binary that CLAIMS Python, so a Python build with a broken stdlib still
# fails here.
has_python() { # dir visible to openroad; "$@" runs openroad
  local d=$1 f; shift
  : > "$d/empty.tcl"
  f=$("$@" -no_init -exit "$d/empty.tcl" 2>&1 | grep -m1 "Features included" || true)
  rm -f "$d/empty.tcl"
  echo "features: ${f:-<no banner>}" >&2
  case "$f" in *+Python*) return 0 ;; *) return 1 ;; esac
}

if [ -d "$TARGET" ]; then
  tmp=$(mktemp -d)
  cp -a "$TARGET" "$tmp/bundle"
  "$tmp/bundle/bin/openroad" -version
  # The tarball bundle takes the Python STDLIB from the host (as it does glibc).
  if ! has_python "$tmp" "$tmp/bundle/bin/openroad"; then
    echo "python: SKIPPED — binary built without Python"
  elif [ -d /usr/lib/python3.12 ]; then
    pysmoke "$tmp" "$tmp/bundle/bin/openroad" -no_splash -exit -python
  else
    echo "python: SKIPPED — this host has no /usr/lib/python3.12 (the bundle's host requirement)"
  fi
  rm -rf "$tmp"
else
  docker run --rm "$TARGET" openroad -version
  tmp=$(mktemp -d)
  if ! has_python "$tmp" docker run --rm -v "$tmp:$tmp" "$TARGET" openroad; then
    echo "python: SKIPPED — binary built without Python"
  else
    pysmoke "$tmp" docker run --rm -v "$tmp:$tmp" "$TARGET" openroad -no_splash -exit -python
  fi
  rm -rf "$tmp"
fi
echo "SMOKE_OK"
