---
title: Features
weight: 1
translationKey: features
aliases: ["/features.html", "/docs/guides/features/"]
---


Current release · {{< latest-release part="version" >}} · {{< latest-release part="date" >}} · Based on XCP-ng 8.3
{class="lead"}

## Base platform

XCP-hl is based on **XCP-ng 8.3**, with changes to the installer, XO Lite,
XOA deployment and package delivery. The base platform uses the upstream
hypervisor and management stack; hardware and feature requirements still apply.

| Attribute | Value |
|---|---|
| Base release | XCP-ng 8.3 (latest upstream point release) |
| Hypervisor | Xen 4.17 |
| Dom0 kernel | Linux 4.19 (XCP-ng kernel) |
| Management API | XAPI (Xen API) |
| Default networking | Open vSwitch (OVS) |
| Installer | XCP-ng text installer |

---

## Customisations

### Patched XO Lite

XO Lite is the lightweight single-page management UI bundled with every
XCP-ng host. XCP-hl changes one screen in it: at build time, an automated
tool rewrites small, targeted pieces of `xoa-deploy.vue` (see
[Components](/docs/components/xolite-ce) if you want the exact mechanism).

The upstream xo-lite version is pinned via the `UPSTREAM_TAG` file in
`xolite-ce` (currently `xo-lite-v0.21.0`, the last known-good release) and
only moves when that pin is deliberately bumped.

**What the patch changes:**

The **"Deploy XOA"** screen now has a **"XOA Image URL"** selector to choose your XO deployment.

Everything else in XO Lite (VM management, console access, SR browsing,
host metrics) remains untouched.

### xoa-proxy: local XVA delivery

A purpose-built **Rust HTTP server** (`xoa-proxy`) is bundled with the ISO
and runs on the host. It:

- Serves the community XOA image with support for gzip-compressed format.
- Supports both HTTP and HTTPS (including self-signed certificates).

### HomeLab XOA image *(default)*

The XOA image deployed by the proxy is [`xoa-hl`](https://github.com/Vagrantin/xoa-hl):
Xen Orchestra built from source for XCP-hl, with the license-gated menu
items and support banners stripped out. See [Components](/docs/components/xoa-hl)
for how it is built.

### Ronivay's XOA image

The XOA image deployed by the proxy is built from
[ronivay/XenOrchestraInstallerUpdater](https://github.com/ronivay/XenOrchestraInstallerUpdater),
a well-maintained community installer for self-hosted Xen Orchestra.

| Detail | Value |
|---|---|
| XO version | Tracks latest stable XO release |
| Default admin user | `admin@admin.net` |
| Default admin password | `admin` |
| SSH user | `xo` |
| SSH password | `xopass` |

{{< callout type="warning" >}}
**Change the default passwords immediately** after first login.
{{< /callout >}}

### Vates XOA image

This is the official image provided by Vates for XCP-ng multi-host management.
In this case you can specify the credentials at the deployment step.

### Custom image

Any XVA, plain or gzipped, served over HTTP or HTTPS. Point the deploy
screen at your own URL: your own build, an older release you kept around,
or an image hosted anywhere reachable from the host. Credential fields are
left blank for you to fill in; nothing is pre-filled since XCP-hl has no way
to know what the image expects.

---

## GPG signing

All XCP-hl artifacts are signed with the **XCP-hl GPG key**, so anyone can
confirm a package or ISO really came from this project and was not tampered
with. This section is reference detail for verifying that yourself; most
readers can skip straight to [What you get](#what-you-get-full-feature-summary).

### Key structure

The key follows an **offline master + subkeys** model:

| Role | Description |
|---|---|
| Master key | Certification only: kept offline, never used for signing |
| RPM signing subkey | Signs all community RPM packages (`xo-lite-community`, `xoa-proxy`) |
| ISO signing subkey | Signs the ISO checksum file (`xcp-ng-8.3-ceN.iso.sha256.asc`) |

| Property | Value |
|---|---|
| Key UID | `XCP-ng Community Edition (Master signing key)` (as shown by `gpg --list-keys`) |
| Master key fingerprint | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Published | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Email | `xcp-ng-ce.lid530@passmail.com` |
| Public key file | [`xcp-ng-ce-public.asc`](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) |

The public key file contains both signing subkeys. Importing it once is
sufficient to verify both RPMs and the ISO checksum.

---

## What you get (full feature summary)

### Hypervisor & host management

- **Full XCP-ng 8.3 feature set**: all VM types (HVM, PV, PVH), live
  migration (XenMotion), Storage XenMotion.
- **Storage Repositories**: Local LVM, NFS, iSCSI (LVM & EXT), HBA/FC,
  XOSTOR (hyper-converged), SMB, ISO SR.
- **Ready-to-use ISO library**: a dedicated 20 GB partition is reserved at
  install time and registered as an ISO SR on first boot, so you can upload
  installer images and build VMs without setting up storage by hand. See
  [ISO storage](#iso-storage).
- **GPU/vGPU**: PCI passthrough and NVIDIA GRID vGPU support.
- **HA**: pool high-availability with automatic VM restart on host failure.

### ISO storage {#iso-storage}

Out of the box, XCP-ng has nowhere to put installer ISOs: no ISO SR exists,
and creating one means picking a path, making a directory and running
`xe sr-create` by hand. XCP-hl does that for you.

**What you get.** A fresh install reserves a 20 GB partition, formats it
ext4 with the label `xcphl-iso`, mounts it at `/var/opt/xen/xcp-hl-iso` and
registers it with XAPI as an ISO SR named **XCP-HL ISO library**. It shows
up in Xen Orchestra straight away, so you can upload an ISO
(*Import → Disk*, selecting the ISO SR) and boot a VM from it with no extra setup.

**Disk requirement.** XCP-hl asks for a **100 GB** disk, which splits
roughly as:

| Area | Size |
|---|---|
| System partitions (root, backup, boot, logs, swap) | ~41.5 GB |
| ISO library | 20 GB |
| Local storage SR (VM disks) | ~38.5 GB |

Below 100 GB the reservation is skipped rather than squeezing VM storage
down to a few GB. The install still completes and the disk is laid out
exactly as stock XCP-ng would lay it out. You simply get no ISO library,
and a line in `/var/log/installer` records why.

**Where it applies.** The partition is created by the installer, so it only
exists on hosts installed from an XCP-hl ISO. A host installed from stock
XCP-ng that later adds the XCP-hl repositories keeps its existing disk
layout untouched: nothing repartitions a running machine. Those hosts can
still create an ISO SR manually in the usual way.

Upgrading an existing XCP-hl host keeps the partition, since upgrades never
repartition, and the ISO SR is picked up again from its filesystem label.

**Known caveat.** If you unplug the SR's PBD and plug it back in *without*
rebooting, XAPI will reattach it but the filesystem stays unmounted, so the
library looks empty until the next reboot remounts it. This is inherent to
how XCP-ng handles local (`legacy_mode`) ISO SRs and affects the built-in
XCP-ng Tools SR in the same way; a reboot, or
`mount /var/opt/xen/xcp-hl-iso`, restores it.

### XO Lite (browser-based quick management)

Available at `https://<host-ip>` immediately after install:

- Pool and host overview (CPU, RAM, storage at a glance).
- VM list: start, stop, reboot, console access.
- Basic SR and network inspection.
- **HomeLab deploy flow**: one-click XOA deployment with no
  external connectivity required if you host your XOA image locally.

### XOA-hl: the administration WebUI {#xen-orchestra-after-xoa-deployment}

Deploying the hl image gives you Xen Orchestra running in its own VM. XOA-hl provides:

- **Host and VM administration** through the Xen Orchestra 5 interface: inspect resources and manage virtual machines.
- **Backup and scheduling controls** from the source-built Xen Orchestra application.
- **XCP-hl host updates** in the host and pool Patches tabs, including the XCP-hl repositories.
- **Appliance update controls** under Settings → XOA-HL Updates. The host and the appliance are updated separately.
- **Focused menus**: the Vates appliance updater, Hub, proxies and XOSTOR menu entries are hidden; the community banner links to XCP-hl documentation.

This description is based on `xoa-hl` release `v5.113.2_e281c536-ce20`, which pins Xen Orchestra to `5.113.2`. Other image choices have their own features and update mechanisms. See [Updates](/docs/guides/updates) and the [XOA-hl component](/docs/components/xoa-hl).

---

## Known limitations in this release

| Limitation | Status |
|---|---|
| Xolite-ce: Deploy button always accessible | [#31](https://github.com/Vagrantin/xcp-hl/issues/31): switch button to "Access XOA" after successful deploy |
| Xoa-proxy: Logs are in UTC | [#62](https://github.com/Vagrantin/xcp-hl/issues/62): investigation to be done |
| Xoa-proxy: Reduce the number of crates | [#63](https://github.com/Vagrantin/xcp-hl/issues/63): investigation to be done |
| Xoa-proxy: Reduce memory footprint | [#64](https://github.com/Vagrantin/xcp-hl/issues/64): xoa-proxy runs in Dom0; its memory impact must be controlled |

---

## Recent releases

The five newest ISO releases and the component versions each one shipped.
Every release is in the [Release Matrix](/docs/reference/release-matrix),
and what changed and why is in the [Changelog](/docs/reference/changelog).

{{< release-matrix-iso limit="5" rpm="false" >}}
