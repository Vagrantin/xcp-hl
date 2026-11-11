---
layout: default
title: xolite-ce
parent: Developers
nav_order: 2
---

# xolite-ce

**Repository:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)

XO Lite CE adds the XOA-HL, Vates, Ronivay and custom-image choices to the
upstream deployment screen and supplies a host-local loader. This page
covers source maintenance (issues #16 and #43). It does not establish
support for an upstream version beyond the pinned baseline.

## Source patching

`UPSTREAM_TAG` pins `xo-lite-v0.21.0` at
`13f987ff3d34504a90b89178489e15fa2293d1b3`. XO Lite CE changes that source
with reviewable unified diffs. `patches/series` defines diff order and
`patches/metadata.toml` records each patch's purpose, target, owner,
upstream commit and dependencies. The series holds `xoa-button-empty.patch`
for `XoaButton.vue` and `010-xoa-deploy.patch` for `xoa-deploy.vue`.
Builds and validation share `scripts/patch-source.sh`, which also runs the
explicit locale, loader, host/guest and deploy-secret transformations that
are not diffs. Evidence: `xolite-ce/patches/series@ad43fa2`,
`xolite-ce/patches/metadata.toml@ad43fa2` and
`xolite-ce/scripts/patch-source.sh@ad43fa2`.

Before [PR #26](https://github.com/Vagrantin/xolite-ce/pull/26), merged on
2026-10-31 as `4506112`, a vendored Rust executable rewrote `xoa-deploy.vue`.
The diff replaced it without changing the upstream pin or the final source
bytes.

See the [assessment](patching-model-assessment.md) for the decision
record. The component's
[maintenance guide](https://github.com/Vagrantin/xolite-ce/blob/ad43fa282dca7023776a142cb4250e96226d8312/docs/patching.md)
sets the naming, ordering and metadata rules.

## Source validation

Use a clean pinned upstream checkout. In the XO Lite CE tree:

```sh
python3 scripts/list-patches.py patches
python3 ci/test-patch-series.py
bash scripts/patch-source.sh /path/to/clean/pinned/upstream
```

The complete series is checked before any diff is applied. Invalid names,
missing or duplicate entries, metadata mismatches and invalid dependency
order fail validation. Do not skip failed patches or substitute a remote
loader. Existing source tests check the affected UI, locales and deployment
cleanup separately.

`docs/patch-migration.json` records the retired executable's hash and the
immutable consumer, upstream and patcher-source revisions.
`ci/test-patch-migration.py` compares all source bytes, Git executable modes
and symlink targets from the legacy and current pipelines. CI also rebuilds
the pinned Rust source and checks its output against the recorded
executable. This is behavioral provenance on one pinned input, not
historical binary reproducibility.

## Builds and acceptance

All application and RPM builds run in GitHub Actions. On pull requests,
`check-patch-series.yml` runs the complete pipeline and builds the patched
Vue distribution without publishing a release. Packaging and signing remain
in `build-xolite-ce.yml` and `SPECS/xo-lite-community.spec`.

Keep source application, hosted application builds, RPM checks and
installed acceptance as separate results. Build `0.21.0-39.g54c289b`
contains the unified-diff series. `xcp-hl/qa/ce52-acceptance/2026-11-09.md@7a51eb1`
records that build on one installed ce36 host, with appliances deployed
through the shipped `#/xoa-deploy` Custom URL flow. Other image sources,
other hosts and a before/after installed comparison remain unverified.
