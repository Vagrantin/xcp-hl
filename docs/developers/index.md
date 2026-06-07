---
layout: default
title: Developers
nav_order: 4
has_children: true
---

# Developer Documentation
{: .no_toc }

Everything you need to understand, build, and contribute to XCP-ng CE.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Repository overview

XCP-ng CE is split across three functional repositories plus this
documentation/release repo.

```
Vagrantin/xcp-ce          ← docs (this site)
      │
      ├── Vagrantin/xolite-ce       ← XO Lite patch + RPM build
      │         │ publishes signed RPM as GitHub Release artifact
      │         │ 
      ├─────────│───Vagrantin/xoa-proxy           ← Rust HTTP proxy + RPM build
      │         │        │  publishes signed RPM as GitHub Release artifact
      │         ▼        ▼
      └── Vagrantin/xcp-ng-ce-iso   ← ISO assembly + ISO GitHub Releases
                │ downloads RPM from xolite-ce and xoa-proxy, assembles ISO
                │
```

Each repo has its own GitHub Actions pipeline. They are **loosely coupled**:
`xolite-ce` and `xoa-proxy` publish versioned RPM artifacts that `xcp-ng-ce-iso`
fetches by release tag. Neither repo needs to be checked out together for normal
builds.

---

## Tech stack

| Layer | Technology |
|---|---|
| Hypervisor base | XCP-ng 8.3 (Xen 4.17, Linux 4.19 Dom0) |
| XO Lite UI | Vue 3 · TypeScript · Vite · Pinia (`@xen-orchestra/lite`) |
| XO Lite build | Yarn (Corepack) · `yarn build:xo-lite` |
| RPM packaging | `rpmbuild`, `rpmsign`, `createrepo_c` |
| ISO assembly | `create-install-image` (XCP-ng toolchain, master branch) |
| ISO tooling | `mksquashfs`, `xorriso`, `isohybrid`, `implantisomd5` |
| Build environment | Docker (`xcp-ng-build-env:8.3`) |
| Proxy server | Rust · `hyper` · `tokio` · `tokio_util::io::ReaderStream` |
| CI/CD | GitHub Actions (free tier) |
| Signing | GPG — offline master key + 2 signing subkeys (see below) |

---

## Build pipeline — end to end

```
1. xolite-ce CI (GitHub Actions)
   ├── Clone vatesfr/xen-orchestra at release tag
   ├── Apply patches/community-xoa-deploy.patch
   ├── yarn build:xo-lite
   ├── rpmbuild → xo-lite-community-<VERSION>.rpm
   ├── rpmsign with RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
   └── Publish RPM + xcp-ng-ce-public.asc as GitHub Release assets

2. xoa-proxy CI (GitHub Actions)
   ├── Install musl toolchain (musl-1.2.4, static libc)
   ├── Install Rust stable via rustup
   ├── Add x86_64-unknown-linux-musl target
   ├── cargo build --release --target x86_64-unknown-linux-musl
   ├── Prepare RPM sources (binary + systemd unit + logrotate config)
   ├── rpmbuild → xoa-proxy-<VERSION>.rpm
   ├── rpmsign with RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
   └── Publish RPM + xcp-ng-ce-public.asc as GitHub Release assets

3. xcp-ng-ce-iso CI (GitHub Actions)
   ├── Download signed RPM from xolite-ce release
   ├── Download signed RPM from xoa-proxy release
   ├── Import GPG_PRIVATE_KEY (ISO signing subkey) into runner keyring
   ├── Export public key from runner keyring → inject into installer chroot
   ├── Set up community-repo/x86_64/ with createrepo_c
   ├── Run create-installimg.sh (root) — builds install.img (SquashFS)
   ├── Run create-iso.sh (non-root) — assembles ISO
   ├── isohybrid --uefi (hybrid MBR/GPT stamp)
   ├── implantisomd5
   ├── sha256sum → SHA256SUMS
   ├── gpg --detach-sign SHA256SUMS  (ISO signing subkey via GPG_PRIVATE_KEY)
   └── Publish ISO + SHA256SUMS + SHA256SUMS.asc + xcp-ng-ce-public.asc
       to Vagrantin/xcp-ce GitHub Release
```

---

## Key design decisions

### Three-repo strategy
Separating each RPM build from the ISO assembly keeps concerns clean:
`xolite-ce` (UI patch, packaging) and `xoa-proxy` (Rust proxy, packaging)
can each be iterated on independently without touching the ISO toolchain,
and vice versa. Each publishes a versioned, signed RPM as a GitHub Release
artifact — that artifact is the published contract with `xcp-ng-ce-iso`,
which only consumes and builds the ISO.

### Patch at source level
The XO Lite patch is applied to the Vue/TypeScript **source** of
`DeployXoaView.vue`, not to the compiled output.

---

## GPG signing

XCP-ng CE uses a single keypair following an **offline master + subkeys** model.
The master key is kept offline and is never used for signing. Two signing subkeys
are derived from it — one for RPMs, one for the ISO.

### Key details

| Property | Value |
|---|---|
| Master key fingerprint | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Published | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Email | `xcp-ng-ce.lid530@passmail.com` |
| Public key file | `xcp-ng-ce-public.asc` |

### Subkey roles

| Subkey | Used for |
|---|---|
| RPM signing subkey | `xo-lite-community-*.rpm` and `xoa-proxy-*.rpm` |
| ISO signing subkey | `SHA256SUMS.asc` (detached signature over the ISO checksum file) |

### CI secrets

All three repositories use the same secret **names** (`GPG_PRIVATE_KEY` and
`GPG_PASSPHRASE`), but the key material stored in those secrets differs by
repository:

| Repository | `GPG_PRIVATE_KEY` contains | Purpose |
|---|---|---|
| `xolite-ce` | RPM signing subkey (private) | Signs `xo-lite-community-*.rpm` |
| `xoa-proxy` | RPM signing subkey (private) | Signs `xoa-proxy-*.rpm` |
| `xcp-ng-ce-iso` | ISO signing subkey (private) | Signs `SHA256SUMS.asc` |

The public key (`xcp-ng-ce-public.asc`) contains the public halves of **both**
subkeys. It is committed to the `xcp-ng-ce-iso` repository and published as a
release asset alongside every ISO. Importing it once is sufficient for an end
user to verify both RPMs and the ISO checksum.

---

## Detailed component docs

| Page | Description |
|---|---|
| [xoa-proxy](xoa-proxy) | Rust HTTP/gzip proxy for XVA delivery |
| [xolite-ce](xolite-ce) | XO Lite patch, RPM spec, build pipeline |
| [xcp-ng-ce-iso](xcp-ng-ce-iso) | ISO assembly, toolchain, CI workflow |
