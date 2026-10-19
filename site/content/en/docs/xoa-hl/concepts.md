---
title: "Concepts and feature scope"
linkTitle: "Concepts"
description: "Understand the components, version numbers and what this release includes."
weight: 90
translationKey: xoa-manual-concepts
translationStatus: source
sourceRevision: sha256:5f34ed54ff2d136c85d8ea8fca3bdebf785565736c3dad46a9c10bdb8638f5fe
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Read this page to identify the component you are operating and the limits of a feature claim.

{{< callout type="info" >}}
Source-reviewed reference for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Later releases can differ. Installed-appliance acceptance and human translation review remain pending.
{{< /callout >}}

## Components and addresses

| Component | Responsibility | Address |
| --- | --- | --- |
| Hypervisor host / pool | Runs VMs and exposes XAPI | Host management address |
| XO Lite CE | Host-served browser interface; appliance deployment/discovery | Host HTTPS address |
| XOA-HL appliance | Separate VM running xo-server, XO 5 web UI and Redis | Appliance HTTPS address |

Use the [architecture and deployment guide](/docs/start/#start-architecture) for the flow. Keep one supported manager per host/pool; use [ownership and discovery](/docs/xoa-hl/hosts-pools/) before moving a connection. Host updates and appliance updates have separate targets and schedules: [update guide](/docs/guides/updates/).

## Objects and protection

A **VM** runs on a host in a **pool**. A **storage repository (SR)** stores virtual disks; a VM network interface connects to a pool network. Names are labels, so use object IDs when automating. A **snapshot** records a VM point in time on its storage; a **backup** copies protection data to a configured remote. A snapshot alone does not protect against losing that storage.

Use the [controlled glossary](/docs/xoa-hl/glossary/), [disk/network guide](/docs/xoa-hl/storage-networks/) and [full backup with isolated restore pilot](/docs/xoa-hl/backup-restore/). A successful backup job still needs a restore test.

## Version identities

| Identity in this reference | Meaning |
| --- | --- |
| XO 5.113.2 / upstream `e281c536` | Deliberate application/UI source pin; not XO 6 |
| `xo-server` 5.193.1 | Server package version at that pin; a different numbering scheme |
| `v5.113.2_e281c536-ce38` | HomeLab RPM release and patch set |
| `xoa-image-20261009-5f33c81` | Appliance image build identity; remains distinct after an application update |

Record the installed values as described in [maintenance](/docs/xoa-hl/maintenance/). The [release matrix](/docs/reference/release-matrix/) records shipped combinations, not integration-test acceptance. An ISO does not pin the image later resolved by the deployment flow.

## Feature scope at ce38

| Area | Source observation | Acceptance boundary |
| --- | --- | --- |
| VM power, snapshots, disks and networks | XO 5 action/UI code is present | Daily guides have pending disposable-lab checks |
| Users and object ACLs | Released build keeps upstream OpenSource plan default; ACL UI is source-visible | Check the installed UI and independent normal-user session |
| Full backup and restore | Source-reviewed NFS pilot is documented | Real backup and isolated restore remain pending |
| Appliance updates | HomeLab API, stable/testing channels and configurable schedules | Follow the release-scoped update guide |
| Hub, Vates XOA section, backup proxies and XOSTOR menus | ce38 menu patch hides these entries | Hidden menus are not supported feature promises or proof that every API is absent |

The release contains 14 declared patches. Their presence is not a claim that every upstream option has been validated. Vates subscription tiers, commercial support and XO 6 interfaces do not describe this HomeLab package. Check [permissions](/docs/xoa-hl/permissions/) and the relevant task guide before relying on a feature.

## Reference and contribution

Use [service configuration](/docs/xoa-hl/configuration/), [read-only CLI automation](/docs/xoa-hl/automation/) and [configuration export](/docs/xoa-hl/configuration-backup/) for different kinds of settings and data. For implementation and CI-only product builds, read [xoa-hl](/docs/components/xoa-hl/) and [build-xoa-hl](/docs/components/build-xoa-hl/). Report the release identity with a proposed documentation change.

## Sources

[UPSTREAM_XO](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [patch metadata](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/metadata.toml), [menu patch](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/menu-hide-items.patch), [RPM](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [xo-server package](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [XO build plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
