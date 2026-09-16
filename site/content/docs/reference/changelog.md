---
title: Changelog
weight: 2
translationKey: changelog
---

Project-level changes across all XCP-hl repositories, with the issues they
resolve. Per-release component versions live in the
[Release Matrix](/docs/reference/release-matrix).
{class="lead"}

## September 2026

### The deployed XOA VM is named XOA-hl, fixes [#97](https://github.com/Vagrantin/xcp-hl/issues/97)

Deploying the XOA-HL appliance from XO Lite produced a VM called
`xoa-almalinux`, the internal Packer build name, not a product name. XO Lite
does not rename what it imports: `VM.import` keeps the name-label carried by
the XVA, which is exactly the builder's `vm_name`. The build now sets
`vm_name` to **`XOA-hl`**, in both
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl)'s
`setup-xoa-builder.sh` (manual builds) and the orchestrator's `xoa-vm-agent`
(the daily pipeline that publishes the images).

Because Packe
...
dies with source versions and verification steps.
- The ISO build is dispatched by the orchestrator with exact component
  release tags pinned as workflow inputs, eliminating stale-RPM races
  (`xcp-ng-ce-iso` `68f211d`).
- Every ISO release is recorded in the [Release Matrix](/docs/reference/release-matrix).

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
[GPG signing](/docs/components/#gpg-signing) for details. A follow-up refinement
(one key per module) stays on the [roadmap](/docs/reference/roadmap#gpg-keys-one-signing-key-per-module).

