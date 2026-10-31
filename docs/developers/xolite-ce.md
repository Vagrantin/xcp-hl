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
covers the source-maintenance migration for issues #16 and #43. It does not
establish support for an upstream version beyond the pinned baseline.

## Source patching

At `xolite-ce@d452937`, `UPSTREAM_TAG` pins `xo-lite-v0.21.0` at
`13f987ff3d34504a90b89178489e15fa2293d1b3`. That baseline uses a vendored
Rust executable for `xoa-deploy.vue`, plus a unified diff for `XoaButton.vue`
and explicit locale, loader, host/guest and deploy-secret transformations.
Evidence: `xolite-ce/.github/workflows/build-xolite-ce.yml@d452937` and
`xolite-ce/UPSTREAM_TAG@d452937`.

[The migration PR](https://github.com/Vagrantin/xolite-ce/pull/26) replaces
the vendored executable with a reviewable
unified diff. `patches/series` defines diff order and `patches/metadata.toml`
records purpose, ownership, upstream and dependencies. Builds and validation
share `scripts/patch-source.sh`. Non-diff asset and locale transformations
remain explicit. The upstream pin and final source bytes are preserved.

See the [assessment](patching-model-assessment.md) for the decision record
and the migration PR linked there for implementation status. The component's
[maintenance guide](https://github.com/Vagrantin/xolite-ce/blob/7925dbc6bde35bfb387677b2c9c227ef05a886c0/docs/patching.md)
describes the migration branch. Implementation evidence:
`xolite-ce/scripts/patch-source.sh@7925dbc`,
`xolite-ce/scripts/list-patches.py@7925dbc`, and
`xolite-ce/ci/test-patch-migration.py@7925dbc`.

## Source validation

Use a clean pinned upstream checkout. In the migrated XO Lite CE tree:

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

`docs/patch-migration.json` records the old executable hash and immutable
consumer, upstream and patcher-source revisions. The migration check compares
all source bytes, Git executable modes and symlink targets from the old and
new pipelines. CI additionally rebuilds the pinned Rust source and checks
its output against the recorded executable. This is behavioral provenance
on one pinned input, not historical binary reproducibility.

## Builds and acceptance

All application and RPM builds run in GitHub Actions. The migration adds a
PR check for the complete pipeline and patched Vue distribution without
publishing a release. Packaging and signing remain in the existing component
workflows and `SPECS/xo-lite-community.spec`.

Keep source application, hosted application builds, RPM checks and installed
acceptance as separate results. No running appliance was available during
this migration; installed deployment behavior remains unverified.
