#!/usr/bin/env bash
# build-bundle.sh — compile OpenROAD at $OR_COMMIT (inside the deps-env image,
# where /OpenROAD and /opt/deps-prefixes.txt already exist) and assemble the
# relocatable binary bundle + tarball into $OUT_DIR.
#
# Binary-first: THIS bundle is the primary artifact; the container (Dockerfile.runtime)
# wraps the same bytes. Relocatable = real ELF + non-glibc ldd closure + a wrapper
# that sets LD_LIBRARY_PATH. Host floor: glibc >= 2.39 (the ubuntu:24.04 build base).
#
# Env: OR_COMMIT (required), VERSION (default "dev"), OUT_DIR (default /out).
# Run:  docker run --rm -e OR_COMMIT=<sha> -e VERSION=<ver> -v "$PWD/dist:/out" \
#         -v "$PWD/scripts:/scripts" ghcr.io/vyges-tools/vyges-openroad-deps:<tag> \
#         bash /scripts/build-bundle.sh
set -euo pipefail

: "${OR_COMMIT:?set OR_COMMIT}"
VERSION="${VERSION:-dev}"
OUT_DIR="${OUT_DIR:-/out}"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$OUT_DIR"

echo "== checkout $OR_COMMIT =="
cd /OpenROAD
git fetch --depth 1 origin "$OR_COMMIT" 2>/dev/null || git fetch origin
git checkout -q "$OR_COMMIT"
git submodule update --init --recursive

echo "== compile (Build.sh -no-gui -no-tests) =="
./etc/Build.sh -deps-prefixes-file=/opt/deps-prefixes.txt -no-gui -no-tests -threads="$(nproc)"

OR=$(find /OpenROAD -name openroad -type f -executable | grep -v third-party | head -1)
[ -n "$OR" ] || { echo "ERROR: built openroad not found"; exit 1; }
"$OR" -version

SHORT=$(echo "$OR_COMMIT" | cut -c1-12)
NAME="vyges-openroad-${VERSION}-g${SHORT}"
BUNDLE="$OUT_DIR/$NAME"
echo "== assemble relocatable bundle: $BUNDLE =="
rm -rf "$BUNDLE"
mkdir -p "$BUNDLE"/{bin,libexec,lib}
cp "$OR" "$BUNDLE/libexec/openroad"

# Non-glibc shared-lib closure (glibc + libgcc/libstdc++ stay a host requirement,
# provided by the matching ubuntu:24.04 runtime base / host).
ldd "$BUNDLE/libexec/openroad" | awk '/=>/{print $3}' | grep -E '^/' \
  | grep -vE '/libc\.so|/libm\.so|/libpthread|/libdl\.so|/librt\.so|/libresolv|ld-linux|/libgcc_s|/libstdc\+\+' \
  | sort -u | xargs -I{} cp -Ln {} "$BUNDLE/lib/" 2>/dev/null || true

cat > "$BUNDLE/bin/openroad" <<'WRAP'
#!/bin/sh
# vyges-openroad launcher — relocatable: resolve libs next to this bundle.
HERE=$(cd "$(dirname "$0")/.." && pwd)
export LD_LIBRARY_PATH="$HERE/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "$HERE/libexec/openroad" "$@"
WRAP
chmod +x "$BUNDLE/bin/openroad"

# Ship OpenROAD's own LICENSE with the binary (BSD-3-Clause requires the license +
# copyright notice to accompany binary redistributions) + a short attribution NOTICE.
for lic in LICENSE LICENSE.txt COPYING; do
  [ -f "/OpenROAD/$lic" ] && cp "/OpenROAD/$lic" "$BUNDLE/LICENSE.OpenROAD" && break
done
cat > "$BUNDLE/NOTICE" <<NOTICE
This is a reproducible build of OpenROAD (https://github.com/The-OpenROAD-Project/OpenROAD),
BSD-3-Clause — see LICENSE.OpenROAD. Built by Vyges from commit ${OR_COMMIT}.
The OpenROAD name and trademarks belong to their respective owners; this build is unaffiliated.
NOTICE

# MCP-friendliness: a self-describing tool descriptor + tools.json example (the shared
# vyges-tool-descriptor/1.0 convention, also in vyges-klayout) so the vyges resolve/MCP
# layer can discover + invoke this backing tool uniformly. Mirrored as com.vyges.tool.* labels.
cat > "$BUNDLE/vyges-tool.json" <<TOOLJSON
{
  "schema": "vyges-tool-descriptor/1.0",
  "tool": "openroad",
  "version": "${VERSION}",
  "kind": "backing-tool",
  "headless": true,
  "provides": ["synthesis", "floorplan", "placement", "cts", "routing", "rcx", "sta", "gds-out"],
  "invoke": { "binary": "openroad", "entrypoint": "openroad" },
  "env": { "required": ["PDK_ROOT"], "optional": [] },
  "license": "BSD-3-Clause",
  "upstream_commit": "${OR_COMMIT}"
}
TOOLJSON

cat > "$BUNDLE/tools.json.example" <<'TJ'
{ "tools": {
    "openroad": { "container": {
      "runtime": "docker",
      "image": "ghcr.io/vyges-tools/vyges-openroad:latest",
      "mounts": ["${PDK_ROOT}:${PDK_ROOT}:ro"]
    } }
} }
TJ

# Provenance manifest (image_digest + build_date are filled by CI post-build).
if [ -x "$SCRIPTS_DIR/provenance.sh" ]; then
  OR_COMMIT="$OR_COMMIT" VERSION="$VERSION" "$SCRIPTS_DIR/provenance.sh" > "$BUNDLE/manifest.json" || true
fi

echo "== tarball =="
tar -C "$OUT_DIR" -czf "$OUT_DIR/${NAME}-linux-x86_64.tar.gz" "$NAME"
echo "bundle: $BUNDLE"
du -sh "$BUNDLE" "$OUT_DIR/${NAME}-linux-x86_64.tar.gz"
echo "BUILD_BUNDLE_OK short=$SHORT name=$NAME"
