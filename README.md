# vyges-openroad

A Vyges-controlled, versioned, **reproducible distribution of mainline OpenROAD**.

OpenROAD has published no semver release since ~2020 and runs a continuous-`master`
model, so every downstream (LibreLane, OpenLane, ORFS) commit-pins and rebuilds.
`vyges-openroad` gives our flow one **pinned, reproducibly built** artifact — as both a
slim container and a relocatable binary tarball — to pop in.

- **Rebuild, never fork or vendor.** We build OpenROAD `master` at a pinned commit — this
  repo holds only the *build recipe* (no OpenROAD source, README, or tree in-tree; CI clones
  upstream at build time). **Zero source patches, no unmerged PRs.**
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
`index.json`), `nightly.yml` (track `master` HEAD → `:master-latest`).

## Cut a release / bump the pin

Edit **`upstream.yaml`** (`commit`, `updated_at`) — the source of truth — then run the
`release` workflow with a `version` (e.g. `2026.07.0`). A sync workflow proposes pin bumps
via PR when OpenROAD `master` advances.

## Licensing

Repository tooling (Dockerfiles, scripts, workflows) is Apache-2.0 (`LICENSE`). The **built
artifact is upstream OpenROAD, BSD-3-Clause** — each bundle ships OpenROAD's own license as
`LICENSE.OpenROAD` plus a `NOTICE` and `manifest.json` recording the exact commit + submodule
provenance.
