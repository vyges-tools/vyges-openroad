# vyges-openroad

A Vyges-controlled, versioned, **reproducible distribution of mainline OpenROAD**.

OpenROAD has published no semver release since ~2020 and runs a continuous-`master`
model, so every downstream (LibreLane, OpenLane, ORFS) commit-pins and rebuilds.
`vyges-openroad` gives our flow one **pinned, reproducibly built** artifact — as both a
slim container and a relocatable binary tarball — to pop in.

- **Rebuild, never fork or vendor.** We build OpenROAD `master` at a pinned commit — this
  repo holds only the *build recipe* (no OpenROAD source, README, or tree in-tree; CI clones
  upstream at build time). **The plain build carries zero source patches and no unmerged PRs.**
- **Two builds, never confused.** Next to the plain build, some releases also ship a separately
  labelled build with our fixes for reported upstream defects (see
  [Two builds](#two-builds-plain-and--vyges)). Everything about that one carries a `-vyges` suffix.
- **Binary-first.** The relocatable bundle is the primary product; the container wraps the
  *same* bytes (slim runtime image, no build tooling).
- **Images:** `ghcr.io/vyges-tools/vyges-openroad` · **Tarballs:** GitHub Releases.

## Use it

`vyges-openroad` is consumed via the Vyges CLI (`tools.json`) or a direct pull:

```jsonc
{ "tools": {
    // container (most portable):
    "openroad": { "container": {
      "runtime": "docker",
      "image": "ghcr.io/vyges-tools/vyges-openroad:2026.07.0",
      "mounts": ["${PDK_ROOT}:${PDK_ROOT}:ro"]
    } }
    // or the relocatable tarball (host glibc >= 2.39 / ubuntu 24.04+):
    // "openroad": { "path": "/opt/vyges-openroad/current/bin/openroad" }
} }
```

## Two builds: plain and `-vyges`

| | Plain (default) | `-vyges` |
|---|---|---|
| Source | upstream OpenROAD at the pinned commit, unmodified | the same commit with a short list of fix patches applied |
| Release | `YYYY.MM.N` (marked Latest) | `YYYY.MM.N-vyges` (never Latest) |
| Tarball | `vyges-openroad-YYYY.MM.N-g<short>-linux-<arch>.tar.gz` | `vyges-openroad-YYYY.MM.N-vyges-g<short>-linux-<arch>.tar.gz` |
| Image tags | `:YYYY.MM.N`, `:sha-<short>`, `:latest` | `:YYYY.MM.N-vyges`, `:sha-<short>-vyges` only |
| `index.json` / `which.sh` | listed | not listed |

Use the **plain** build unless you need one of the fixes. LibreLane flows and anything that compares
against reference OpenROAD behaviour should stay on it.

The `-vyges` build fixes defects we have reported upstream, each found while checking our own
engines against OpenROAD, mostly in detailed routing (`drt`) and one in the LEF reader (`odb`). The
release notes and the bundle's `VYGES-FIXES.md` / `vyges-fixes.json` list every patch with its
upstream issue number and sha256; `NOTICE` says the build is modified. A patch is dropped as soon as
upstream merges a fix, so the list shrinks to nothing as upstream catches up. The patch files are not
published. The build is made outside this repo, from this repo's recipe at a recorded commit, and only
the built tarballs come here; [`wrap-vyges-image.yml`](.github/workflows/wrap-vyges-image.yml) wraps
them into the image with the same `Dockerfile.runtime`.

## Naming & selecting a build

The **OpenROAD commit hash is the immutable identity**; human tags are pointers to it.

| Tag | Meaning |
|---|---|
| `:sha-<12hex>` | immutable — one commit → one build; never re-pointed |
| `:2026.07.0` | a pinned release (frozen), alias to a `sha-<…>` |
| `:latest` | moves to the newest pinned release |
| `:master-latest` | moves to the newest nightly |

From a git commit, get the binary with no lookup — the tag is the commit, truncated:

```sh
docker pull ghcr.io/vyges-tools/vyges-openroad:sha-$(git rev-parse HEAD | cut -c1-12)
```

For tarballs, dates, and "newest build ≤ commit X", `index.json` is the lookup table:

```sh
scripts/which.sh latest          # newest pinned release
scripts/which.sh master-latest   # newest nightly
scripts/which.sh b5624809f290    # a specific commit/short/date
```

## How it's built

Binary-first, two-stage for cheap free-runner CI:

1. **`deps/Dockerfile`** → `vyges-openroad-deps` (ubuntu:24.04 + OpenROAD's compiled deps).
   Heavy but rebuilt **rarely** (`deps.yml`; re-run when the pinned commit's
   `DependencyInstaller.sh` changes).
2. **`scripts/build-bundle.sh`** (in the deps image) compiles OpenROAD at the pinned commit
   and assembles the **relocatable bundle** (`bin/openroad` wrapper + `libexec/openroad` +
   the non-glibc `lib/` closure) → tarball.
3. **`Dockerfile.runtime`** wraps that same bundle into the slim image.

Workflows: `deps.yml` (base), `release.yml` (pinned release → image + tarball + GH Release +
`index.json`), `nightly.yml` (track `master` HEAD → `:master-latest`), `wrap-vyges-image.yml`
(a `-vyges` release's tarballs → its suffixed image tags).

## Cut a release / bump the pin

Edit **`upstream.yaml`** (`commit`, `updated_at`) — the source of truth — then run the
`release` workflow with a `version` (e.g. `2026.07.0`). A sync workflow proposes pin bumps
via PR when OpenROAD `master` advances.

## Upstream watch

Every Saturday at 15:00 UTC (07:00 PST / 08:00 PDT), [`upstream-watch`](.github/workflows/upstream-watch.yml)
compares the commit [`upstream.yaml`](upstream.yaml) pins with OpenROAD `master` and writes a digest to
[`reports/upstream-watch/`](reports/upstream-watch/) (`latest.md`, plus one file per week):

- the commits since the pin, by module, with the functions each one touched;
- the commits that updated regression goldens (`.ok`, `.defok`, `.guideok`, ...), i.e. the observable behaviour changes;
- the OpenSTA submodule's movement;
- the pull requests and issues updated that week.

It reads public upstream data only (`scripts/upstream-watch.py`, standard library). Run it by hand with
`gh workflow run upstream-watch.yml`, or locally with `GH_TOKEN=$(gh auth token) python3 scripts/upstream-watch.py --out /tmp/uw`.

## Licensing

Repository tooling (Dockerfiles, scripts, workflows) is Apache-2.0 (`LICENSE`). The **built
artifact is upstream OpenROAD, BSD-3-Clause** — each bundle ships OpenROAD's own license as
`LICENSE.OpenROAD` plus a `NOTICE` and `manifest.json` recording the exact commit + submodule
provenance. A `-vyges` bundle is a modified build of the same BSD-3-Clause source, under the same
license; its `NOTICE` says so and `vyges-fixes.json` records what was changed.
