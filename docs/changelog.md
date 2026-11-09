---
layout: default
title: Changelog
nav_order: 6
---

# Changelog
{: .no_toc }

Project-level changes across all XCP-hl repositories, with the issues they
resolve. Per-release component versions live in the
[Release Matrix](/release-matrix/).
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Release notes

{% include generated-changelog.html %}

## Earlier project notes

## November 2026

### XOA-HL provisioning and crash recovery on the ce52 image, towards [#311](https://github.com/Vagrantin/xcp-hl/issues/311)

{: .warning }
XCP-hl is alpha. Everything below is scoped to the exact image, host and
builder listed here and says nothing about other releases.

An unclean shutdown shortly after deployment used to bring back the default
`admin@admin.net` / `admin` account on XOA-HL images built before 2026-10-27
([#311](https://github.com/Vagrantin/xcp-hl/issues/311)), and the SSH
password stayed in the VM's XenStore data
([#310](https://github.com/Vagrantin/xcp-hl/issues/310), closed). The fix lives
in the image's first-boot scripts and Redis configuration, so an application
RPM update does not apply it to an already deployed appliance.

Observed on one isolated test host, with the appliance deployed through the XO
Lite **Deploy XOA** form using a custom URL:

| Item | Value |
|---|---|
| XVA | `qa-xoa-build-76.xva` in release `xoa-image-20261109-8da29b0`, 986,847,999 bytes, SHA-256 `658ad02024680af9714d491c608e7b73f97abbd05c6f6a8f23174b198a6a297c` |
| Application | `xoa-hl-5.113.2_e281c536-52.g8da29b0` (`v5.113.2_e281c536-ce52`) |
| Builder | `build-xoa-hl@f269dc7`, Jenkins `build/xoa-vm-agent` #76 |
| Host | XCP-ng 8.3 installed from a `ce36` ISO, `xo-lite-ce` 0.21.0-39.g54c289b, `xoa-proxy` 0.1.3.1-73.g1b44984, `xcp-hl-release` 0.0.5-5.g157727f |

| Check | Result |
|---|---|
| Sign in as the administrator typed in the form | Accepted, and it is the only XO user |
| `admin@admin.net` / `admin` | Rejected |
| Credential keys after first boot | None in the guest XenStore; the VM's persistent XAPI `xenstore-data` holds only `vm-data/mmio-hole-size` |
| Passwords in guest files and journal | None found (searched `/var/log`, `/etc`, `/run`, `/var/lib`, `/home`, `/root`, `/tmp`) |
| Redis | `appendonly yes`, `appendfsync everysec` |
| Forced power-off about one minute after provisioning finished | Same administrator signs in, default rejected, SSH works with the deployment password, first boot does not run again |
| Password changed, forced power-off 3 seconds later | New password signs in, old and default rejected |
| Password changed, forced power-off immediately | The change was lost and the previous password signed in; the default stayed rejected |
| Fresh deployment, forced power-off during first boot (after phase 1, before phase 2 finished) | Boot retried provisioning and finished about 12 seconds into the next boot; same result as above: intended administrator only, default rejected, SSH works, no credential keys in XenStore or XAPI, no passwords in guest files or journal |

The last row is the documented crash-loss window of about one second under
`appendfsync everysec`. A normal shutdown is still preferable.

Configuration import merges users instead of replacing them. Importing an
export that contains `admin@admin.net` brought that account back with the
password `admin` next to the deployed administrator. Deleting it as the
deployed administrator, then force-stopping the VM 3 seconds later, left only
the deployed administrator after reboot. After any configuration import, review
**Settings > Users** and remove unexpected accounts. This is user-initiated and
scoped to this image; a fix is planned after launch, tracked in
[#388](https://github.com/Vagrantin/xcp-hl/issues/388).

XO Lite reported the deployment successful before phase 2 had finished, so
that message does not mean setup is finished. The bootstrap account
`admin@admin.net` / `admin` exists until phase 2 completes. Wait for phase 2
(the done flag `/var/lib/xoa-credentials.done`, or the end of
`/var/log/xoa-first-boot.log`) before exposing the appliance to untrusted
networks.

A probe on one run (ce52 image `qa-xoa-build-76.xva`, DHCP, one LAN, 2026-11-09)
confirmed that the default account does accept sign-ins in that window: both
`admin@admin.net` / `admin` attempts made after xo-server started listening on
port 443 and before the done flag was written were accepted (05:16:23 and
05:16:25 UTC, done flag at 05:16:26 UTC, about 6 seconds after the default
user was created), and every later attempt was rejected. One run does not
establish the length of the window on other hosts or timings. A forced stop in
that window is recovered by the retry on the next boot, but the retry boot opens
the same window again. This is a documented beta limit and a fix is planned
after launch, tracked in [#389](https://github.com/Vagrantin/xcp-hl/issues/389).

What to do until then:

- Deploy the appliance on a trusted network.
- Do not expose it to untrusted networks until setup has finished: the done
  flag `/var/lib/xoa-credentials.done` exists, or
  `/var/log/xoa-first-boot.log` ends with "Credential provisioning complete".
- If the VM is stopped or crashes during first boot, treat the next boot as a
  new window and wait for the done flag again.

This entry makes no claim that the image is ready for release.

Not covered by this run: a deployment with the SSH account disabled, a failed
provisioning step other than a forced stop, a physical power loss (the VM was
force-stopped from the host), and the Vates, Ronivay and custom image sources.

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

Because Packer derives the XVA filename from `vm_name`, the release asset is
renamed with it, `xoa-almalinux.xva` becomes `XOA-hl.xva`. Nothing resolves
that asset by name: XO Lite's deploy button and the agent's release check both
pick the first `.xva` / `.xva.gz` asset on the newest `xoa-image-*` release, so
already-published images keep working and no ISO needs reissuing.

The name applies to images built after this change. Appliances already
deployed keep the old name and can be renamed in XO; orchestrator hosts with a
`/etc/xcp-orchestrator/build.config` from before this change keep their own
`VM_NAME` (`deploy.sh` never overwrites an existing config) and need that key
updated by hand.

### Default ISO storage, closing [#2](https://github.com/Vagrantin/xcp-hl/issues/2) and [#46](https://github.com/Vagrantin/xcp-hl/issues/46)

A fresh XCP-ng host has nowhere to put installer ISOs: no ISO SR exists and
creating one is a manual `xe sr-create` against a directory you have to make
yourself. XCP-hl now reserves a 20 GB partition at install time, formats it
ext4 as `xcphl-iso`, mounts it at `/var/opt/xen/xcp-hl-iso`, and registers it
on first boot as an ISO SR named **XCP-HL ISO library**, ready to upload to
from Xen Orchestra.

This sets XCP-hl's minimum disk at **100 GB**: ~41.5 GB of system
partitions, 20 GB of ISO library, ~38.5 GB left for VM storage. Below that
the reservation is skipped rather than squeezing VM storage to a few GB, and
the disk is laid out exactly as stock XCP-ng would.

Issue [#46](https://github.com/Vagrantin/xcp-hl/issues/46) asked whether
XCP-ng's upload endpoint could be given an ISO-specific route. It turned out
not to need one: `PUT /import_raw_vdi` is a generic raw-VDI import that XO 5
already drives through *Import → Disk*, and the only thing missing was an
ISO SR to import into. No new endpoint was added.

The partition is created by the installer, so it applies to fresh XCP-hl
installs only. Hosts installed from stock XCP-ng that later add the XCP-hl
repositories are never repartitioned, and upgrades keep the existing
partition rather than recreating it.

Delivered by patching `host-installer` inside `install.img` at ISO build
time rather than shipping a forked `host-installer` RPM. See
[xcp-ng-ce-iso](developers/xcp-ng-ce-iso.html#host-installer-patching).

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
