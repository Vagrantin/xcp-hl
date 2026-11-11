---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/developers/xolite-ce.html"]
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

See the [assessment of the cross-component patching model](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md)
for the decision record and the migration PR linked there for implementation
status. The component's [maintenance guide](https://github.com/Vagrantin/xolite-ce/blob/7925dbc6bde35bfb387677b2c9c227ef05a886c0/docs/patching.md)
describes the migration branch. Implementation evidence:
`xolite-ce/scripts/patch-source.sh@7925dbc`,
`xolite-ce/scripts/list-patches.py@7925dbc`, and
`xolite-ce/ci/test-patch-migration.py@7925dbc`.

---

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

---

## Builds and acceptance

All application and RPM builds run in GitHub Actions. The migration adds a
PR check for the complete pipeline and patched Vue distribution without
publishing a release. Packaging and signing remain in the existing component
workflows and `SPECS/xo-lite-community.spec`.

Keep source application, hosted application builds, RPM checks and installed
acceptance as separate results. No running appliance was available during
this migration; installed deployment behavior remains unverified.

---

## GPG signing

The `xo-lite-ce` RPM is signed with the **RPM signing subkey** of the
XCP-hl keypair. The same subkey also signs the `xoa-proxy` and
`xcp-hl-release` RPMs: there is one shared subkey for all community RPMs.

The project publishes its shared [public key](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc)
at the production site root. Verify the master fingerprint before importing it.
The commands below require an RPM implementation that supports signing subkeys.
XCP-ng 8.3 Dom0 uses older RPM 4.11; installed hosts instead validate signed
repository metadata with `repo_gpgcheck=1`. Keep the repository settings in
[Updates](/docs/guides/updates) unchanged.

To verify the RPM locally:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Contributing

To report a problem or suggest a change, open an issue on
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
