---
layout: default
title: Features
nav_order: 2
---

# Features — v8.3-ce9
{: .no_toc }

Current release · June 2026 · Based on XCP-ng 8.3
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Base platform

XCP-ng HL is a **drop-in ISO replacement** for XCP-ng 8.3. It inherits the
full upstream feature set, the differences are in XO Lite, XOA and the
deployment workflow. Everything below the installer works exactly as in
the official release.

| Attribute | Value |
|---|---|
| Base release | XCP-ng 8.3 (latest upstream point release) |
| Hypervisor | Xen 4.17 |
| Dom0 kernel | Linux 4.19 (XCP-ng kernel) |
| Management API | XAPI (Xen API) |
| Default networking | Open vSwitch (OVS) |
| Installer | XCP-ng text installer |

---

## customisations

### Patched XO Lite

XO Lite is the lightweight single-page management UI bundled with every
XCP-ng host. In HomeLab Edition, the upstream `DeployXoaView.vue` component
is patched at **source level** before the RPM is built, so the patch is
minimal.

The upstream xo-lite version is pinned via the `UPSTREAM_TAG` file in
`xolite-ce` (currently `xo-lite-v0.21.0`, the last known-good release) and
only moves when that pin is deliberately bumped.

**What the patch changes:**

- The **"Deploy XOA"** button targets an updated XOA deploy webpage.
- The XOA-HL image 
- The official Vates image.
- The image provided by Ronivay.
- A custom field to deploy your own XOA image.

Everything else in XO Lite — VM management, console access, SR browsing,
host metrics — remains untouched.

### xoa-proxy — local XVA delivery

A purpose-built **Rust HTTP server** (`xoa-proxy`) is bundled with the ISO
and runs on the host. It:

- Serves the community XOA image with support for gzip-compressed format.
- Supports both HTTP and HTTPS (including self-signed certificates).

### HomeLab XOA image

The XOA image deployed by the proxy is built by integrating XOA-HL
[Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl),

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

{: .warning }
**Change the default passwords immediately** after first login.

### Vates XOA image

This is the official image provided by Vates for XCP-ng multi-host management.
In this case you can specify the credentials at the deployment step.

---

## GPG signing

All XCP-ng HL artifacts are signed with the **XCP-ng HomeLab Edition GPG key**.

### Key structure

The key follows an **offline master + subkeys** model:

| Role | Description |
|---|---|
| Master key | Certification only — kept offline, never used for signing |
| RPM signing subkey | Signs all community RPM packages (`xo-lite-community`, `xoa-proxy`) |
| ISO signing subkey | Signs the ISO checksum file (`xcp-ng-8.3-ceN.iso.sha256.asc`) |

| Property | Value |
|---|---|
| Master key fingerprint | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Published | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Email | `xcp-ng-ce.lid530@passmail.com` |
| Public key file | `xcp-ng-ce-public.asc` (attached to every release) |

The public key file contains both signing subkeys. Importing it once is
sufficient to verify both RPMs and the ISO checksum.

---

## What you get (full feature summary)

### Hypervisor & host management

- **Full XCP-ng 8.3 feature set** — all VM types (HVM, PV, PVH), live
  migration (XenMotion), Storage XenMotion.
- **Storage Repositories** — Local LVM, NFS, iSCSI (LVM & EXT), HBA/FC,
  XOSTOR (hyper-converged), SMB, ISO SR.
- **Ready-to-use ISO library**: a dedicated 20 GB partition is reserved at
  install time and registered as an ISO SR on first boot, so you can upload
  installer images and build VMs without setting up storage by hand. See
  [ISO storage](#iso-storage).
- **GPU/vGPU** — PCI passthrough and NVIDIA GRID vGPU support.
- **HA** — pool high-availability with automatic VM restart on host failure.

### ISO storage
{: #iso-storage }

Out of the box, XCP-ng has nowhere to put installer ISOs: no ISO SR exists,
and creating one means picking a path, making a directory and running
`xe sr-create` by hand. XCP-HL does that for you.

**What you get.** A fresh install reserves a 20 GB partition, formats it
ext4 with the label `xcphl-iso`, mounts it at `/var/opt/xen/xcp-hl-iso` and
registers it with XAPI as an ISO SR named **XCP-HL ISO library**. It shows
up in Xen Orchestra straight away, so you can upload an ISO
(*Import → Disk*, selecting the ISO SR) and boot a VM from it with no extra setup.

**Disk requirement.** XCP-HL asks for a **100 GB** disk, which splits
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
exists on hosts installed from an XCP-HL ISO. A host installed from stock
XCP-ng that later adds the XCP-HL repositories keeps its existing disk
layout untouched: nothing repartitions a running machine. Those hosts can
still create an ISO SR manually in the usual way.

Upgrading an existing XCP-HL host keeps the partition, since upgrades never
repartition, and the ISO SR is picked up again from its filesystem label.

**Known caveat.** If you unplug the SR's PBD and plug it back in *without*
rebooting, XAPI will reattach it but the filesystem stays unmounted, so the
library looks empty until the next reboot remounts it. This is inherent to
how XCP-ng handles local (`legacy_mode`) ISO SRs and affects the built-in
XCP-ng Tools SR in the same way; a reboot, or
`mount /var/opt/xen/xcp-hl-iso`, restores it.

### XO Lite (browser-based quick management)

Available at `http://<host-ip>` immediately after install:

- Pool and host overview (CPU, RAM, storage at a glance).
- VM list: start, stop, reboot, console access.
- Basic SR and network inspection.
- **HomeLab deploy flow**: one-click XOA deployment with no
  external connectivity required if you host your XOA image locally.

### Container Management (XOA-HL)
{: #container-management }

XOA-HL includes built-in Docker container support, allowing you to deploy and
manage containers directly from the Xen Orchestra web interface.

**What you get:**

- **Container Deployment**: Deploy containers from any Docker image with configurable:
  - Container name
  - Docker image (with image pull functionality)
  - CPU limits (shares)
  - Memory limits and reservations
  - Port mappings (host:container)
  - Volume mappings (host path:container path)
  - Environment variables
  - Restart policies (no, on-failure, always, unless-stopped)
  - Privileged mode
  - Network mode

- **Container Management**: Full lifecycle control:
  - Start, stop, restart containers
  - Remove containers (with optional volume removal)
  - View container logs with tail and timestamp options
  - Monitor resource usage (CPU, memory)

- **Image Management**:
  - List all Docker images on the system
  - Pull new images from Docker registries
  - Remove images

- **Docker System Info**: View Docker system information and configuration

**Implementation Details:**

- Docker runs inside the XOA-HL appliance VM (AlmaLinux 9)
- Configured with overlay2 storage driver optimized for XCP-ng
- Resource limits enforced to prevent resource exhaustion
- Designed for beginners with advanced options available
- Real-time resource monitoring integrated into the UI

**Important Notes:**

- Containers run in the appliance VM, not on Dom0 (this is intentional for safety)
- Docker is pre-installed and configured in XOA-HL images
- The container management UI is available under the "Containers" menu item
- All container operations require admin privileges

**Security Considerations:**

- Privileged mode should be used with caution
- Resource limits are recommended to prevent one container from consuming all resources
- Container networking is isolated by default
- Always use trusted images from verified sources

### Xen Orchestra (after XOA deployment)

After "Deploy XOA" in XO Lite, you get a full Xen Orchestra instance:

**New in XOA-HL:**

- **Full lifecycle VM management** — create, clone, migrate, snapshot.
- **Agentless backup** — full, delta, continuous replication, disaster recovery.
- **Scheduling** — cron-based backup jobs with configurable retention.
- **RBAC / delegation** — roles (Admin, Operator, Viewer) and resource sets.
- **Monitoring & alerting** — per-VM and per-host metrics, threshold alerts.
- **REST API + xo-cli** — scriptable access to all resources.
- **Rolling pool upgrade** — zero-downtime upgrades via XO.
- **XOSTOR** — hyper-converged storage setup via the XO UI (3+ nodes).

{: .warning }
**Some features require a license distributed by Vates.**

---

## Known limitations in this release

| Limitation | Status |
|---|---|
| XOA-HL - Container support | [issue#7](https://github.com/Vagrantin/xcp-hl/issues/7) - Docker container management now available |

| Limitation | Status |
|---|---|
| Xolite-ce — Deploy button always accessible | [issue#4](https://github.com/Vagrantin/xolite-ce/issues/4) — switch button to "Access XOA" after successful deploy |
| Xoa-proxy — Logs are in UTC | [issue#3](https://github.com/Vagrantin/xoa-proxy/issues/3) — investigation to be done |
| Xoa-proxy — Reduce the number of crates | [issue#2](https://github.com/Vagrantin/xoa-proxy/issues/2) — investigation to be done |
| Xoa-proxy — Reduce memory footprint | [issue#1](https://github.com/Vagrantin/xoa-proxy/issues/1) — xoa-proxy runs in Dom0; its memory impact must be controlled |
| Xcp-hl — Release publication versioning | [issue#4](https://github.com/Vagrantin/xcp-hl/issues/4) — versioning is inconsistent across artifacts |

---

## Changelog

### v8.3-ce9 (June 2026)
- xolite-ce `v0.21.0-ce6` — upstream xo-lite pinned to `0.21.0` (last known-good
  release; `0.22.0`/`0.23.0` broke the build) via the `UPSTREAM_TAG` file.
- xoa-proxy `v0.1.1.x` — simplified RPM versioning (`.static` release suffix)
  and automated, categorized GitHub release notes.
- Consistent artifact naming: `xcp-ng-8.3-ceN.iso` + `.iso.sha256` +
  `.iso.sha256.asc`, published as `xcp-ng-ce-iso` GitHub Releases.

### v8.3-ce alpha2 (May 2026)
- Initial public release.
- First usable release.
- Provides basic feature to deploy from Vates, Ronivay, or custom URL.
- **GPG**: offline master key + dedicated RPM and ISO signing subkeys.
  Public key published to keys.openpgp.org.

### v8.3-ce (April 2026)
- XO Lite patched: community deploy endpoint, read-only credential fields.
- `xoa-proxy` Rust server bundled: HTTP/HTTPS, gzip streaming.
- ISO assembled from upstream XCP-ng 8.3 with community RPM repo overlay.
- GPG key infrastructure (4096-bit RSA, single key `RPM-GPG-KEY-xcp-ng-ce`).
- GitHub Actions CI/CD pipeline: RPM build → ISO build → GitHub Releases.
