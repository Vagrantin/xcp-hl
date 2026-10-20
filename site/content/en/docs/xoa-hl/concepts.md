---
title: "Concepts and feature scope"
linkTitle: "Concepts"
description: "Understand the components, the version numbers and what this version includes."
weight: 90
translationKey: xoa-manual-concepts
translationStatus: source
sourceRevision: sha256:16d96a198271a59f01a3879f316b87511123b62129dcde83c40e8e7d8dbe06ef
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

This reference page explains which component you are working with, what the version numbers mean, and what this version includes. It has no steps to follow. Use it before you rely on a feature, or when you report a problem.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system.
{{< /callout >}}

## Components and addresses {#components}

| Component | What it does | Where you reach it |
| --- | --- | --- |
| Hypervisor host or pool | Runs the VMs and provides the XAPI management interface | The host's management address |
| XO Lite CE | A browser interface served by the host. It deploys and finds the appliance | The host's HTTPS address |
| XOA-HL appliance | A separate VM that runs xo-server, the XO 5 web interface and Redis | The appliance's HTTPS address |

To see how these parts fit together, read the [architecture and deployment guide](/docs/start/#start-architecture). Manage each host or pool with only one supported manager. Read [Hosts and pools](/docs/xoa-hl/hosts-pools/) before you move a connection. Host updates and appliance updates are separate, with their own targets and schedules: see the [update guide](/docs/guides/updates/).

## VMs, storage and protection {#objects}

A **VM** runs on a host in a **pool**. A **storage repository (SR)** stores virtual disks. A VM's network interface connects to a pool network. Names are only labels: use object IDs in automation.

A **snapshot** saves the state of a VM at one point in time, on the same storage. A **backup** copies the data to a separate backup destination (a remote). A snapshot alone does not protect you if that storage is lost, and a successful backup job still needs a restore test.

For more, see the [glossary](/docs/xoa-hl/glossary/), [Storage and networks](/docs/xoa-hl/storage-networks/) and [Back up and restore a VM](/docs/xoa-hl/backup-restore/).

## Version numbers {#versions}

| Version | What it means |
| --- | --- |
| XO 5.113.2, upstream commit `e281c536` | The Xen Orchestra version of the application and web interface. It was chosen on purpose: this is not XO 6 |
| `xo-server` 5.193.1 | The server package version in that same release. It uses a different numbering |
| `v5.113.2_e281c536-ce38` | The XOA-HL package release, with its set of patches |
| `xoa-image-20261009-5f33c81` | The build of the appliance image. It is a separate number: updating the application does not change it |

Note the installed values as described in [appliance maintenance](/docs/xoa-hl/maintenance/). The [release matrix](/docs/reference/release-matrix/) lists the versions that shipped together; it does not mean that they passed integration tests. The installation ISO does not fix which appliance image you get: the image is chosen later, when you deploy the appliance.

## What this version includes {#feature-scope}

| Area | In the code of this version | Before you rely on it |
| --- | --- | --- |
| VM power, snapshots, disks and networks | The XO 5 actions and screens are present | The everyday guides are not yet tested on a lab system |
| Users and object permissions (ACLs) | The released build keeps the upstream default plan (OpenSource). The ACL screens are in the code | Check the installed interface, and test in a separate session signed in as a normal user |
| Full backup and restore | An NFS procedure is documented, based on the code | A real backup and an isolated restore are not yet tested |
| Appliance updates | XOA-HL update API, `stable` and `testing` channels, and schedules you can set | Follow the update guide for your release |
| Hub, the Vates XOA section, backup proxies and XOSTOR menus | A menu patch in this package hides these entries | A hidden menu does not make a supported feature. It does not prove that the matching API is gone either |

This package release declares 14 patches. They do not mean that every upstream option has been tested. Vates subscription plans, commercial support and XO 6 interfaces do not apply to this package. Before you rely on a feature, check [Users and permissions](/docs/xoa-hl/permissions/) and the guide for that task.

## Related pages {#related}

- [Service settings](/docs/xoa-hl/configuration/): the xo-server configuration files.
- [Automation with xo-cli](/docs/xoa-hl/automation/): read inventory from the command line with a short-lived token.
- [Configuration export](/docs/xoa-hl/configuration-backup/): save the settings and records of the web interface.
- [xoa-hl](/docs/components/xoa-hl/) and [build-xoa-hl](/docs/components/build-xoa-hl/): how the package is made. Product builds run only in CI.

When you suggest a change to this documentation, include the image and package versions that you use.

{{< details title="Sources" closed="true" >}}
- **Versions, patches and build**: [upstream XO version (`UPSTREAM_XO`)](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [list of patches](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/metadata.toml), [menu patch that hides entries](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/menu-hide-items.patch), [package definition](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [xo-server package version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [web interface build](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
{{< /details >}}
