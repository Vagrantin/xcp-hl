---
layout: default
title: Developers
nav_order: 4
has_children: true
---

# Developer Documentation
{: .no_toc }

Everything you need to understand, build, and contribute to XCP-ng HL.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Repository overview

XCP-ng HL is split across several functional repositories plus this
documentation repo.

```
Vagrantin/xcp-hl          ← docs (this site)
      │
      ├── Vagrantin/xolite-ce       ← XO Lite patch + RPM build
      │         │ publishes signed RPM as GitHub Release artifact
      │         │ 
      ├─────────│───Vagrantin/xoa-proxy           ← Rust HTTP proxy + RPM build
      │         │        │  publishes signed RPM as GitHub Release artifact
      │         ▼        ▼
      ├── Vagrantin/xcp-ng-ce-iso   ← ISO assembly + ISO GitHub Releases
      │         │ downloads RPM from xolite-ce and xoa-proxy, assembles ISO
      │
      ├── Vagrantin/xoa-hl          ← XOA-HL: patched Xen Orchestra (RPM + container)
      │         ▼
      ├── Vagrantin/build-xoa-hl    ← Packer pipeline → XOA XVA image on XCP-ng
      │
      └── Vagrantin/buildorchestration ← Rust orchestrator: triggers/monitors all builds
```

Each repo has its own GitHub Actions pipeline. They are **loosely coupled**:
`xolite-ce` and `xoa-proxy` publish versioned RPM artifacts that `xcp-ng-ce-iso`
fetches by release tag. Neither repo needs to be checked out together for normal
builds. `xoa-hl` builds the community-patched Xen Orchestra (XOA-HL), and
`build-xoa-hl` packages it into an XVA image. `buildorchestration` sits on top
and drives the whole pipeline on a daily schedule (see
[Build orchestration](#build-orchestration) below).

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
| CI/CD | GitHub Actions |
| Signing | GPG — offline master key + 2 signing subkeys (see below) |

---

## Build pipeline — end to end

```
1. xolite-ce CI (GitHub Actions)
   ├── Clone vatesfr/xen-orchestra at the tag pinned in UPSTREAM_TAG
   │   (currently xo-lite-v0.21.0 — bumped deliberately, not automatically)
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
   ├── sha256sum → xcp-ng-8.3-ceN.iso.sha256
   ├── gpg --detach-sign  (ISO signing subkey via GPG_PRIVATE_KEY)
   └── Publish xcp-ng-8.3-ceN.iso + .iso.sha256 + .iso.sha256.asc
       + xcp-ng-ce-public.asc as a Vagrantin/xcp-ng-ce-iso GitHub Release
```

---

## Build orchestration

The [`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
repo automates the pipeline above. Its `xcp-orchestrator` Rust workspace
(`orchestrator`, `iso-agent`, `xoa-vm-agent`, `shared` crates) runs as a
systemd service on a dedicated VM, triggered daily by a timer:

```
systemd timer (daily 05:00)
   ├── Trigger xolite-ce and xoa-proxy workflows via workflow_dispatch
   ├── Poll workflow runs until completion
   ├── Skip a component when its latest GitHub release already matches HEAD
   │   (release-based change detection — no rebuild-every-run)
   ├── On failure: pull job logs via the API and diagnose them with a local
   │   LLM (Ollama, qwen3-coder:30b) — writes an actionable fix suggestion
   ├── On success: trigger downstream xcp-ng-ce-iso and XOA XVA image builds
   └── Render a status dashboard (per-component status + log links)
```

---

## Key design decisions

### Three-repo strategy
Separating each RPM build from the ISO assembly keeps concerns clean:
`xolite-ce` (UI patch, packaging) and `xoa-proxy` (Rust proxy, packaging)
can each be iterated on independently without touching the ISO toolchain,
and vice versa. Each publishes a versioned, signed RPM as a GitHub Release
artifact. Those artifacts are then consumed to build the ISO.

### Patch at source level
The XO Lite patch is applied to the Vue/TypeScript **source** of
`DeployXoaView.vue`.

---

## GPG signing

XCP-ng HL uses a single keypair following an **offline master + subkeys** model.
The master key is kept offline and is never used for signing. Two signing subkeys
are derived from it, one for both RPMs, one for the ISO.

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
| ISO signing subkey | `xcp-ng-8.3-ceN.iso.sha256.asc` (detached signature over the ISO checksum file) |

---

## Detailed component docs

| Page | Description |
|---|---|
| [xoa-proxy](xoa-proxy) | Rust HTTP/gzip proxy for XVA delivery |
| [xolite-ce](xolite-ce) | XO Lite patch, RPM spec, build pipeline |
| [xcp-ng-ce-iso](xcp-ng-ce-iso) | ISO assembly, toolchain, CI workflow |
| [xoa-hl (GitHub)](https://github.com/Vagrantin/xoa-hl) | Community-patched Xen Orchestra appliance (XOA-HL) |
| [build-xoa-hl (GitHub)](https://github.com/Vagrantin/build-xoa-hl) | Packer pipeline building the XOA XVA image on XCP-ng |
| [buildorchestration (GitHub)](https://github.com/Vagrantin/buildorchestration) | Rust build orchestrator + LLM build diagnostics |
