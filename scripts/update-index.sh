#!/usr/bin/env bash
# update-index.sh — prepend a build row to index.json (newest-first). The index
# is the commit -> artifact lookup (VyCatalog tier-1 idiom) used by
# `vyges-openroad which` and by "newest build <= commit X" queries.
# Args: <commit> <short> <version> <image_digest> <tarball_url> [channel]
set -euo pipefail
COMMIT="${1:?}"; SHORT="${2:?}"; VERSION="${3:?}"; DIGEST="${4:?}"; TARBALL="${5-}"  # tarball optional (nightly has none)
CHANNEL="${6:-release}"
DATE=$(date -u +%Y-%m-%d)
IMAGE="ghcr.io/vyges-tools/vyges-openroad"

[ -f index.json ] || echo '{"schema":"vyges-openroad-index/1.0","builds":[]}' > index.json

row=$(jq -n \
  --arg commit "$COMMIT" --arg short "$SHORT" --arg version "$VERSION" \
  --arg date "$DATE" --arg digest "$DIGEST" --arg tarball "$TARBALL" \
  --arg channel "$CHANNEL" --arg image "$IMAGE:sha-$SHORT" \
  '{commit:$commit, short:$short, version:$version, date:$date, channel:$channel,
    image_ref:$image, image_digest:$digest, tarball_url:$tarball}')

# De-dup by commit, then prepend (newest-first).
jq --argjson row "$row" \
  '.builds |= ([$row] + (map(select(.commit != $row.commit))))' \
  index.json > index.json.tmp && mv index.json.tmp index.json
echo "index.json updated: $SHORT ($CHANNEL)"
