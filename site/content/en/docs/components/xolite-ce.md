---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/developers/xolite-ce.html", "/developers/patching-model-assessment.html"]
---

XO Lite rebuilt for XCP-hl - selectable XOA deploy images, plus the RPM build pipeline.
{class="lead"}

**Repository:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Language: TypeScript / Vue 3 (patch) · RPM spec · License: AGPL-3.0

## What is XO Lite?

XO Lite is the lightweight single-page management application that ships
bundled with every XCP-ng host. It runs entirely in the browser, served
directly from the host, and is implemented as a Vue 3 / TypeScript / Vite SPA.

On a standard XCP-ng host, XO Lite's **"Deploy XOA"** screen downloads and imports one
hardcoded Xen Orchestra image. XCP-hl replaces that screen with an **"XOA Image URL"**
selector offering four sources: XOA-hl (default), the official Vates image, Ronivay's
image, or a custom XVA URL, plus a **"Verify if ssl certificate is valid"** toggle so
`xoa-proxy` can accept self-signed certificates upstream.

---

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

See the [assessment of the cross-component patching model](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md)
for the decision record. The component's
[maintenance guide](https://github.com/Vagrantin/xolite-ce/blob/ad43fa282dca7023776a142cb4250e96226d8312/docs/patching.md)
sets the naming, ordering and metadata rules.

---

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

---

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

---

## GPG signing

The `xo-lite-ce` RPM is signed with the **RPM signing subkey** of the
XCP-hl keypair. The same subkey also signs the `xoa-proxy` and
`xcp-hl-release` RPMs: there is one shared subkey for all community RPMs.

The project publishes its shared [public key](https://www.xcp-hl.org/xcp-ng-ce-public.asc)
at the production site root. Verify the master fingerprint before importing it.
The commands below require an RPM implementation that supports signing subkeys.
XCP-ng 8.3 Dom0 uses older RPM 4.11; installed hosts instead validate signed
repository metadata with `repo_gpgcheck=1`. Keep the repository settings in
[Updates](/docs/guides/updates) unchanged.

To verify the RPM locally:

```bash
curl -fLO https://www.xcp-hl.org/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Contributing

To report a problem or suggest a change, open an issue on
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
