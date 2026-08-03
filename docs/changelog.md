---
layout: default
title: Changelog
nav_order: 5
---

# Changelog
{: .no_toc }

Project-level changes across all XCP-ng HL repositories, with the issues they
resolve. Per-release component versions live in the
[Release Matrix](/release-matrix/).
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## August 2026

### Release matrix states the exact package shipped, towards [#15](https://github.com/Vagrantin/xcp-hl/issues/15)

The [Release Matrix](/release-matrix/) recorded only a release tag per
component. For `xoa-proxy` that was not enough to identify what a host is
running: the tag maps to a version, but the RPM release field carries the CI
run and source commit, and the two oldest rows carry a `v-proxy-automated-*`
build-run tag that states no version at all.

Each per-ISO row now shows the package as `rpm -q` prints it
(`xoa-proxy-0.1.1.8-55.gc525575.static.x86_64`) under a version that links to
its release page, for the ISO, `xolite-ce` and `xoa-proxy` alike. Existing
rows were backfilled from the published release assets, and the `v8.3-ce3` /
`v8.3-ce4` xo-lite upstream was corrected from 0.22.0 to 0.21.0 to match the
RPM those builds actually ship. The orchestrator records the new field on
every build (`xcp-orchestrator` `shared/src/github.rs`).

---

## July 2026

### XOA VM image releases moved to build-xoa-hl, fixes [#22](https://github.com/Vagrantin/xcp-hl/issues/22)

The XOA-HL VM (`xoa-image-<date>-<sha7>`, asset `xoa-almalinux.xva`) was
published on [`xoa-hl`](https://github.com/Vagrantin/xoa-hl), the repo that
builds the *software*, mixed in with its RPM releases. It is now published on
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl), the repo that
actually builds the image. The orchestrator's `xoa-vm-agent` creates the release
there, and XO Lite's deploy button resolves the newest image from that repo.

The mixing had a concrete cost: `releases/latest` on `xoa-hl` resolved to an
image release with no RPM asset, breaking the RPM lookup in
`build-xoa-hl/scripts/setup-xoa-builder.sh`, now fixed to scan for the newest
release that actually ships an RPM.

Image releases published before the move stay on `xoa-hl` so already-shipped
ISOs keep resolving them; the [Release Matrix](/release-matrix/#xoa-hl-releases)
links each entry to the repo that hosts it.

### Release matrix records XOA versions, fixes [#13](https://github.com/Vagrantin/xcp-hl/issues/13)

The [Release Matrix](/release-matrix/) now has a dedicated
**XOA appliance releases** table recording each published VM image
(`xoa-image-*` release on `Vagrantin/xoa-hl`), the `xoa-hl` software
version it contains, and the upstream Xen Orchestra version it was forked
from. The per-ISO table also dropped a never-populated `xoa-hl` column,
the appliance is resolved at deploy time and versions independently of the
ISO.

### XOA-HL edition complete, fixes [#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)

Xen Orchestra HomeLab Edition is now built from source, packaged, and
deployable end to end:

- [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) builds XO 5.113.2 (the
  last XO 5.x release) from a pinned upstream commit and patches the UI:
  the license-gated menu entries (Hub, XOA, Proxies, XOSTOR) and the
  no-support banner are hidden (`patches/menu-hide-items.patch`).
- [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) packages it
  into a self-configuring XVA appliance via Packer on XCP-ng.
- XO Lite's deploy view now offers **XOA HomeLab (latest build)** as a
  deploy image option, resolving the newest agent-built XVA from GitHub
  releases at deploy time (`xolite-ce` commit `6abd43f`, 2026-07-14).

### Release publication automated, fixes [#4](https://github.com/Vagrantin/xcp-hl/issues/4)

Versioning and release notes are now derived automatically in every
pipeline:

- `xolite-ce` and `xoa-proxy` derive the release tag and RPM version in CI
  (`xolite-ce` `7b2e4d4`, `xoa-proxy` `9582718`); `xoa-proxy` releases use
  GitHub's generated release notes, `xolite-ce` and the ISO ship structured
  release bodies with source versions and verification steps.
- The ISO build is dispatched by the orchestrator with exact component
  release tags pinned as workflow inputs, eliminating stale-RPM races
  (`xcp-ng-ce-iso` `68f211d`).
- Every ISO release is recorded in the [Release Matrix](/release-matrix/).

---

## June 2026

### Documentation website CI/CD, fixes [#5](https://github.com/Vagrantin/xcp-hl/issues/5)

The project website (this site) is built with Jekyll and deployed to
GitHub Pages automatically on every push to `main` of
[`xcp-hl`](https://github.com/Vagrantin/xcp-hl)
(`.github/workflows/pages.yml`), making it the single source of truth for
project status, including the data-driven release matrix.

---

## May 2026

### GPG key model implemented, fixes [#3](https://github.com/Vagrantin/xcp-hl/issues/3)

GPG signing is harmonized across all build pipelines using an **offline
master key + two signing subkeys** model: one subkey signs the RPMs
(`xo-lite-ce`, `xoa-proxy`), the other signs the ISO checksum file. The
public key is published on
[keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com)
and verification steps ship in every release body. See
[GPG signing](developers/#gpg-signing) for details. A follow-up refinement
(one key per module) stays on the [roadmap](roadmap#gpg-keys--one-signing-key-per-module).
