#!/usr/bin/env bash
# Synthetic client/configuration contracts, not a local product build.
set -euo pipefail
fixture_dir="$(mktemp -d)"
trap 'rm -rf "$fixture_dir"' EXIT
npm install --prefix "$fixture_dir" --no-audit --no-fund \
  xo-cli@0.32.2 xo-lib@0.11.1 app-conf@3.0.0 @iarna/toml@2.2.5 ws@8.18.3
upstream_pin=e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c
for file in index.mjs config.mjs; do
  curl -fsSL "https://raw.githubusercontent.com/vatesfr/xen-orchestra/$upstream_pin/packages/xo-cli/$file" \
    -o "$fixture_dir/node_modules/xo-cli/$file"
done
XOA_REFERENCE_MODULES="$fixture_dir/node_modules" node "$(dirname "$0")/test_xoa_reference.cjs"
