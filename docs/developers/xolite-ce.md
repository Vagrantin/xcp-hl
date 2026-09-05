---
layout: default
title: xolite-ce
parent: Developers
nav_order: 2
---

# xolite-ce
{: .no_toc }

XO Lite rebuilt for XCP-HL - selectable XOA deploy images, plus the RPM build pipeline.
{: .fs-6 .fw-300 }

**Repository:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Language: TypeScript / Vue 3 (patch) · RPM spec · License: AGPL-3.0

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## What is XO Lite?

XO Lite is the lightweight single-page management application that ships
bundled with every XCP-ng host. It runs entirely in the browser — served
directly from the host — and is implemented as a Vue 3 / TypeScript / Vite SPA.

On a standard XCP-ng host, XO Lite's **"Deploy XOA"** screen downloads and imports one
hardcoded Xen Orchestra image. XCP-HL replaces that screen with an **"XOA Image URL"**
selector offering four sources — XOA-HL (default), the official Vates image, Ronivay's
image, or a custom XVA URL — plus a **"Verify if ssl certificate is valid"** toggle so
`xoa-proxy` can accept self-signed certificates upstream.

---

## The patch

Patching uses the Rust `xoa-deploy-patcher` tool, which applies pattern-based
edits to `xoa-deploy.vue` at build time and fails if the build cannot be applied.
It also applies `patches/en-hl.json` (HL locale strings) and
`patches/xolite-loader.html` (replacement loader that drops the
`lite.xen-orchestra.com` remote-loading fallback).

The modified **"Deploy XOA"** screen gains an **"XOA Image URL"** selector instead
of a single hardcoded appliance, offering four sources:

  - **XOA-HL** *(default)* — Xen Orchestra built from source for XCP-HL, resolved at deploy time from the latest published image release
  - **Vates image** — the official appliance; imported directly by XAPI, without `xoa-proxy`
  - **Ronivay's image** — the community appliance, resolved from `https://xo-image.yawn.fi/downloads/image.txt`
  - **Custom URL** — any XVA, plain or gzipped, over HTTP or HTTPS

A **"Verify if ssl certificate is valid"** toggle lets `xoa-proxy` accept
self-signed certificates on the upstream image server.

---

## Build pipeline

### Overview

```
1. Read XO_VERSION from the RPM in the upstream XCP-ng ISO
2. Clone vatesfr/xen-orchestra at the matching release tag
3. Apply patches/community-xoa-deploy.patch
4. Install dependencies with Yarn (Corepack)
5. Build XO Lite: yarn build:xo-lite
6. Assemble RPM source tarball
7. rpmbuild -ba SPECS/xo-lite-community.spec
8. rpmsign with the RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
9. Publish RPM + xcp-ng-ce-public.asc as GitHub Release assets
```

### Version detection

The target XO Lite version is read from the RPM already on the upstream
XCP-ng ISO, not hardcoded:

```bash
XO_VERSION=$(rpm -qp --qf '%{VERSION}' xo-lite-*.rpm)
```

This ensures the community RPM always matches the upstream version, making
it a drop-in replacement.

### Tarball structure

The source tarball passed to `rpmbuild` has this layout:

```
xo-lite-{VERSION}/
├── dist/               ← compiled Vite output
├── CHANGELOG.md
├── LICENSE
└── xolite.html         ← renamed from scripts/xolite-loader.html
```

The `xolite.html` filename is required, this is the entry point served by
the XCP-ng host to load XO Lite in the browser.

### RPM spec

`SPECS/xo-lite-community.spec` defines:

- `Name: xo-lite-community`
- `Version: %{XO_VERSION}` (injected at build time)
- `Provides: xo-lite` (so it satisfies any dependency on the upstream package)
- `Conflicts: xo-lite` (prevents co-installation with the upstream RPM)
- File list: `dist/` contents + `xolite.html`

---

## Local development

### Prerequisites

- Node.js 20+ and Yarn (enabled via `corepack enable`)
- `rpmbuild` (`rpm-build` package on RHEL/CentOS/Fedora)
- `rpmsign` (`rpm-sign` package)
- The community GPG public key imported in your keyring

### Workflow

```bash
# 1. Clone the repo
git clone https://github.com/Vagrantin/xolite-ce.git
cd xolite-ce

# 2. Clone upstream xen-orchestra at the target tag
XO_VERSION=<version>
git clone --depth 1 --branch v${XO_VERSION} \
    https://github.com/vatesfr/xen-orchestra.git upstream

# 3. Apply the community patch
cd upstream
git am ../patches/community-xoa-deploy.patch
cd ..

# 4. Install dependencies
cd upstream
corepack enable
yarn install
cd ..

# 5. Build XO Lite
cd upstream
yarn build:xo-lite
cd ..

# 6. Test the UI
scp -r lite/dist/ xcp-ng-host:/opt/xensource/www/
```

### Updating the patch for a new upstream version

```bash
# In a fresh upstream clone, make the changes manually
# then generate a new patch:
git diff HEAD > ../patches/community-xoa-deploy.patch
# or using format-patch for a clean commit:
git format-patch HEAD~1 -o ../patches/
```

---

## GPG signing

The `xo-lite-community` RPM is signed with the **RPM signing subkey** of the
XCP-ng Community Edition keypair. The same subkey is also used to sign the
`xoa-proxy` RPM — there is one shared subkey for all community RPMs.

The public key (`xcp-ng-ce-public.asc`) is the same file distributed with
every release. Importing it once is sufficient to verify any community RPM.

To verify the RPM locally:

```bash
# Option 1 — fetch from keyserver
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# Option 2 — import from the release page
gpg --import xcp-ng-ce-public.asc

# Check the RPM signature
rpm --checksig xo-lite-community-*.rpm
```

---

## CI workflow (GitHub Actions)

The workflow triggers on push to `main`.

Key steps:

```yaml
- name: Detect XO version
  run: echo "XO_VERSION=$(rpm -qp --qf '%{VERSION}' ...)" >> $GITHUB_ENV

- name: Clone upstream at tag
  run: git clone --depth 1 --branch v${{ env.XO_VERSION }} ...

- name: Apply patch
  run: git am patches/community-xoa-deploy.patch

- name: Build XO Lite
  run: |
    corepack enable
    yarn install
    yarn build:xo-lite

- name: Build RPM
  run: rpmbuild -ba SPECS/xo-lite-community.spec

- name: Sign RPM
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import
    echo "${{ secrets.GPG_PASSPHRASE }}" | gpg --passphrase-fd 0 --batch \
      --pinentry-mode loopback --yes --armor
    rpm --addsign RPMS/x86_64/xo-lite-community-*.rpm

- name: Publish release
  uses: softprops/action-gh-release@v1
  with:
    files: |
      RPMS/x86_64/xo-lite-community-*.rpm
      xcp-ng-ce-public.asc
```

---

## Contributing

1. Fork [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce).
2. To change the UI patch: edit `patches/community-xoa-deploy.patch`.
3. To change packaging: edit `SPECS/xo-lite-community.spec`.
4. Run the local development workflow above to verify changes.
5. Open a pull request against `main`.
