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

# ------------------------------------------------------------------ CMake path
# Kept verbatim as a function so the -no-tests compat heredoc below is not
# re-indented or otherwise disturbed by the dispatch added above it.
compile_cmake() {
echo "== compile (Build.sh -no-gui -no-tests) =="
# Upstream made Bazel the default build system (Build.sh: useBazel=yes) and now
# hard-exits when no bazelisk/bazel launcher is present. This deps image ships the
# CMake dependency set (or-tools, Boost, ... compiled + recorded in deps-prefixes),
# so force the CMake path via -cmake-build. The flag only exists on newer commits;
# add it conditionally so builds of older pinned commits (CMake-default) still work.
BUILD_FLAGS=(-deps-prefixes-file=/opt/deps-prefixes.txt -no-gui -no-tests -threads="$(nproc)")
if grep -q -- '-cmake-build' ./etc/Build.sh; then
  BUILD_FLAGS+=(-cmake-build)
fi

# -no-tests compat shim. A module's gtest block is expected to sit behind
# `if(ENABLE_TESTS)` -- odb/mpl/rsz guard `add_subdirectory(test)` in the module
# CMakeLists, grt guards `add_subdirectory(cpp)` inside its test one. A module
# that adds its test subdirectory unconditionally and then writes a gtest block
# reaches, with -no-tests, two things upstream creates only under that guard:
#   build_and_test      top-level CMakeLists.txt, under if(ENABLE_TESTS)
#   GTest::gtest_main   src/CMakeLists.txt: find_package(GTest REQUIRED), same guard
# and configure dies twice over:
#   CMake Error at src/drt/test/CMakeLists.txt:36 (add_dependencies):
#     Cannot add target-level dependencies to non-existent target "build_and_test"
#   CMake Error at src/drt/test/CMakeLists.txt:34 (target_link_libraries):
#     Target "WatermarkCostTest" links to: GTest::gtest_main but the target was not found
# (drt, from OpenROAD PR #11160, merged 2026-09-15 -- broke nightly on 2026-09-16;
# reported upstream as issue #11427.)
#
# Supply both instead of patching the upstream tree, so the bundle stays a build of
# unmodified sources at $OR_COMMIT. Injected via CMAKE_PROJECT_<name>_INCLUDE, which
# CMake runs at the end of the top-level `project(OpenROAD ...)`: that is before
# `add_subdirectory(src)`, and it is top-level directory scope, so GTest's imported
# targets are visible in every module subdirectory the way the guarded find_package
# would make them. `if(NOT ENABLE_TESTS)` makes the whole shim inert the moment
# upstream restores the guard. The flag rides in on Build.sh's `-cmake=` pass-through;
# older pinned commits without it just build as before.
SHIM=/tmp/or-no-tests-compat.cmake
cat > "$SHIM" <<'SHIMEOF'
if(NOT ENABLE_TESTS)
  if(NOT TARGET build_and_test)
    message(STATUS "vyges: stubbing build_and_test (ENABLE_TESTS=OFF)")
    add_custom_target(build_and_test)
  endif()
  # Not REQUIRED: absent GTest is not itself an error here, and the module that
  # wanted it reports a clearer one than a failed find_package would.
  find_package(GTest QUIET)
  message(STATUS "vyges: GTest for unguarded module tests: GTest_FOUND=${GTest_FOUND}")
endif()
SHIMEOF
if grep -q -- '-cmake=\*)' ./etc/Build.sh; then
  BUILD_FLAGS+=(-cmake="-DCMAKE_PROJECT_OpenROAD_INCLUDE=$SHIM")
else
  echo "WARNING: Build.sh has no -cmake= pass-through; skipping no-tests compat shim"
fi

./etc/Build.sh "${BUILD_FLAGS[@]}"
}

# ---------------------------------------------------------------- build system
# ⛔ Upstream made Bazel the default in etc/Build.sh at d29f14a2 (2026-07-12),
# deprecated -bazel with a warning, and maliberty on issue #11427: "cmake is
# headed for deprecation soon ... I would suggest moving to bazel." No date was
# given, so CMake is being left to rot rather than cut - which is exactly how
# #11427 was found. We follow upstream for the OPENROAD build only; our own
# Rust/cargo infrastructure is unaffected and is NOT moving to Bazel.
#
#   OR_BUILD_SYSTEM=bazel  (default)  | cmake  (retained fallback)
#
# ⚠️ The CMake path is kept deliberately, not as dead code. It is what lets a
# build of an OLDER pinned commit still work, and it is the control if a Bazel
# build ever produces a binary that differs from the one we have been shipping.
OR_BUILD_SYSTEM="${OR_BUILD_SYSTEM:-bazel}"

if [ "$OR_BUILD_SYSTEM" = "bazel" ]; then
  echo "== compile (bazel: --config=release --//:platform=cli //:openroad) =="
  BZL=$(command -v bazelisk || command -v bazel || true)
  [ -n "$BZL" ] || { echo "ERROR: OR_BUILD_SYSTEM=bazel but no bazelisk/bazel on PATH"; exit 1; }

  # --//:platform=cli is upstream's OWN mapping of -no-gui: BUILD.bazel declares a
  # `platform` string_flag with config_settings platform_cli / platform_gui, and
  # //:openroad (as against //:openroad-qt) is the CLI binary.
  #
  # ⛔ No -no-tests equivalent is needed, and no compat shim. The CMake path
  # carries one because ENABLE_TESTS=OFF reaches targets upstream creates only
  # under if(ENABLE_TESTS) - issue #11427, our PR #11435 still open. Bazel
  # configures only the requested target's dependency graph, so those test
  # targets are never reached and the whole class of breakage does not arise.
  # That is a reason to prefer this path, not merely conformity with upstream.
  "$BZL" build --config=release --//:platform=cli //:openroad

  # bazel-bin is a symlink into the output base, so resolve it: the bundle copies
  # a real file and then reads its ldd closure.
  OR=$(readlink -f bazel-bin/openroad)
else
  compile_cmake
  OR=$(find /OpenROAD -name openroad -type f -executable | grep -v third-party | head -1)
fi


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
# Arch from the build host (x86_64 or aarch64), not hardcoded — same recipe, correct
# label on amd64 and arm64 runners.
ARCH="$(uname -m)"
TARBALL="${NAME}-linux-${ARCH}.tar.gz"
tar -C "$OUT_DIR" -czf "$OUT_DIR/${TARBALL}" "$NAME"
echo "bundle: $BUNDLE"
du -sh "$BUNDLE" "$OUT_DIR/${TARBALL}"
echo "BUILD_BUNDLE_OK short=$SHORT arch=$ARCH name=$NAME tarball=${TARBALL}"
