---
layout: default
title: build-xoa-hl
parent: Developers
nav_order: 5
---

# build-xoa-hl
{: .no_toc }

Packer pipeline that builds the XOA-HL VM appliance on XCP-ng and produces the XVA image XO Lite CE deploys.
{: .fs-6 .fw-300 }

**Repository:** [Vagrantin/build-xoa-hl](https://github.com/Vagrantin/build-xoa-hl)
· Language: Bash / Packer JSON / Kickstart · License: AGPL-3.0

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Purpose

This repo builds the **XOA HomeLab Edition VM appliance**: an AlmaLinux 9
VM, installed and provisioned by Packer **on a real XCP-ng host**, with
the [`xoa-hl`](xoa-hl) RPM inside. The output is a compressed **XVA
image** — the artifact the XO Lite CE deploy button imports.

The appliance is generic at build time: it carries two one-shot first-boot
services that read provisioning data (network, admin credentials) from
XenStore when XO Lite deploys it, so a single image works for every user.

---

## Repo structure

```
build-xoa-hl/
├── build.config.sample        ← infrastructure config template (copy → build.config)
├── scripts/
│   ├── setup-xoa-builder.sh   ← build entry point: generates Kickstart + Packer JSON, runs build
│   ├── xoa-first-boot.sh      ← in-VM phase 1: XenStore → network + env file
│   └── xoa-credentials.sh     ← in-VM phase 2: sets XO admin credentials via xo-cli
├── systemd/
│   ├── xoa-first-boot.service
│   └── xoa-credentials.service
├── bin/                       ← vendored VMware VDDK tarball (V2V support)
└── artefact/                  ← build/debug artefacts: logs, installed-RPM list, memo
```

---

## Prerequisites

- A Linux build machine with `apt` and sudo (developed on Linux Mint).
  The setup script installs its own dependencies: Packer (HashiCorp apt
  repo), the [`ddelnano/xenserver`](https://github.com/ddelnano/packer-plugin-xenserver)
  Packer plugin, `wget`, `curl`, `jq`, `ufw`.
- A reachable **XCP-ng host** with root credentials, a `Local storage` SR,
  and a named VM network.
- A published [`xoa-hl`](xoa-hl) release on GitHub (the latest release's
  RPM is resolved automatically).
- `build.config`, copied from `build.config.sample` and filled in:
  XCP-ng host IP/credentials, network name, VM name and root password,
  AlmaLinux ISO URL, and the `xe-guest-utilities` RPM URLs.

{: .warning }
`build.config` contains **plaintext credentials** (XCP-ng root password,
VM root password). Never commit it — only `build.config.sample` belongs
in git.

---

## Build entry point — scripts/setup-xoa-builder.sh

Runs on the build machine and generates everything Packer needs:

1. **Load `build.config`** (falls back to built-in defaults if absent).
2. **Install prerequisites** — apt packages, HashiCorp Packer, and the
   `ddelnano/xenserver` Packer plugin.
3. **Open ports 8000–9000/tcp** (ufw) — Packer serves the Kickstart file
   to the VM over its built-in HTTP server on a port in that range.
4. **Resolve the AlmaLinux ISO checksum** — parses the mirror's
   BSD-style `CHECKSUM` file, falling back to GNU-style `SHA256SUMS`;
   fails the build if no valid SHA256 is found (unless pinned in
   `build.config`).
5. **Resolve the latest xoa-hl RPM URL** from
   `api.github.com/repos/Vagrantin/xoa-hl/releases/latest`.
6. **Generate `inst.ks`** — the Kickstart answer file: DHCP on `eth0`,
   EXT4 partitioning (no LVM), SELinux and firewall disabled, minimal
   package set; `%post` enables sshd/chrony, installs `epel-release`,
   `wget`, `nc`, `vim`, and creates the `xo` user (in `wheel`).
7. **Generate `almalinux-build.json`** — the Packer template (see below).
8. **Run the build** — `packer validate` then
   `PACKER_LOG=1 packer build almalinux-build.json`.

---

## Packer template — almalinux-build.json

Single `xenserver-iso` builder: Packer uploads the AlmaLinux ISO to the
XCP-ng host, boots a VM (2 GB RAM, 10 GB disk) with
`inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/inst.ks` on the kernel
command line, waits for SSH, then runs the provisioners:

1. `dnf update -y`.
2. Install **xe-guest-utilities** + **xe-guest-utilities-xenstore**
   (RPM URLs from `build.config`) — required for XenStore access at
   first boot.
3. Install **Node.js 24** (NodeSource).
4. Install the **xoa-hl RPM** — this pulls in the whole XOA-HL stack
   (see [`xoa-hl`](xoa-hl): the RPM's `%post` downloads the release
   tarball into `/opt/xo` and enables `redis` + `xo-server`).
5. Upload `xoa-first-boot.sh` / `xoa-credentials.sh` to `/root/` and the
   two systemd units to `/etc/systemd/system/`, then enable both units.
6. **Slim the image** — remove wifi firmware, firewalld, sssd,
   NetworkManager extras, rsyslog, docs/man/info pages, and non-English
   locales; `dnf autoremove` + `clean all`.
7. **Strip identity** — blank `/etc/machine-id` so each deployed VM
   regenerates its own.

Key builder settings: `format: xva_compressed` (the XVA output),
`keep_vm: always` (the built VM stays on the XCP-ng host for inspection).

---

## First-boot self-configuration

Two one-shot services are baked into the image; XO Lite writes the
provisioning data into XenStore (`/local/domain/<domid>/vm-data/*`) when
it deploys the appliance.

### Phase 1 — xoa-first-boot.service

Runs **before the network comes up** (`Before=network.target`, gated by
`ConditionPathExists=!/var/lib/xoa-first-boot.done`). The script:

- reads the `vm-data` keys via `xenstore-read`: `ip`, `netmask`,
  `gateway`, `dns`, `ntp-servers`, `system-account-xoa-password`, and the
  `admin-account` JSON blob (email + password);
- persists them to `/etc/xoa-first-boot.env` (mode 600);
- writes a NetworkManager keyfile
  (`/etc/NetworkManager/system-connections/xoa-provisioned.nmconnection`)
  — static IP if provided, DHCP otherwise;
- logs verbosely to `/var/log/xoa-first-boot.log` for field diagnostics.

### Phase 2 — xoa-credentials.service

Runs once **after** `network-online.target` and `xo-server.service`,
gated by `!/var/lib/xoa-credentials.done`. The script:

- waits up to 3 minutes for xo-server on port 443;
- sets the `xo` system user's SSH password from the provisioned value;
- registers `xo-cli` against `wss://127.0.0.1` using the bootstrap
  credentials, then calls `user.changePassword` and `user.set` to apply
  the provisioned admin email + password;
- **self-destructs** on exit (trap): writes the done flag, disables and
  removes both units and scripts, and deletes the secrets env file.

{: .note }
If provisioning data is missing or phase 2 fails, the appliance keeps the
bootstrap defaults `admin@admin.net` / `admin` (ronivay convention) —
change them via the XO web UI after deployment.

---

## Outputs

- The compressed XVA image in `output-xva/` inside the build directory on
  the build machine.
- The built VM itself, kept on the XCP-ng host (`keep_vm: always`).

---

## Automated builds — the orchestrator

In the daily pipeline, `setup-xoa-builder.sh` is replaced by the
`xoa-vm-agent` crate in
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration).
It performs the same steps programmatically, and in addition:

1. Skips the build when the repo HEAD already matches the last built SHA.
2. First triggers the `build-xoa.yml` workflow in `Vagrantin/xoa-hl` via
   `workflow_dispatch` and waits for the RPM release.
3. Runs `packer validate` + `packer build` with generated `inst.ks` /
   `almalinux-build.json`.
4. Publishes the XVA as a GitHub Release tagged `xoa-image-<date>-<sha7>`
   on `Vagrantin/xoa-hl` — alongside the RPM releases, distinguished by
   the `xoa-image-` tag prefix (`<sha7>` is the `xoa-hl` commit the image
   was built from). Image releases are recorded in the
   [Release Matrix](/release-matrix/#xoa-appliance-releases).

---

## Contributing

1. Fork [Vagrantin/build-xoa-hl](https://github.com/Vagrantin/build-xoa-hl).
2. Copy `build.config.sample` to `build.config` and point it at a test
   XCP-ng host — never commit `build.config`.
3. Test with `scripts/setup-xoa-builder.sh`; inspect
   `/var/log/xoa-first-boot.log` in a deployed VM when changing the
   first-boot scripts.
4. Open a pull request against `main`.
