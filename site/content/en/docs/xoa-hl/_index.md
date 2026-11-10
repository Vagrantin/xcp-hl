---
title: XOA-HL manual
weight: 2
translationKey: xoa-manual-home
translationStatus: source
sourceRevision: sha256:9690e24c060de4d8fcc693f5a8507c57cce56c189f0a4c0c5abd9829f4c4abae
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL is the appliance, a ready-made virtual machine, that runs Xen Orchestra. You use it from your browser to manage your XCP-HL hosts and virtual machines. This manual shows you how to set it up, run VMs, protect them and keep everything up to date.

{{< callout type="info" >}}
**Applies to** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). These guides follow the released code but have not yet been tested end to end on a lab system. Practise on test VMs first.
{{< /callout >}}

## Start here

New to XOA-HL? Follow these three guides in order.

{{< cards >}}
  {{< card link="first-login/" title="1. First sign-in" subtitle="Sign in, set your password, choose a language and connect your host." >}}
  {{< card link="create-vm/" title="2. Your first VM" subtitle="Upload an installer ISO and install a test VM." >}}
  {{< card link="backup-restore/" title="3. Backup and restore" subtitle="Back up the VM, then check that a restored copy works." >}}
{{< /cards >}}

Not deployed yet? [Deploy XOA-HL from XO Lite](/docs/start/#start-deploy-xoa) first. To see how the host, XO Lite and the appliance fit together, read the [architecture overview](/docs/start/#start-architecture).

## Virtual machines

- [Manage VMs](/docs/xoa-hl/vm-operations/): start and stop, snapshots, copies, CPU and memory, deletion.
- [Use the VM console](/docs/xoa-hl/vm-operations/#vm-console) and fix a blank screen.
- [Take and revert a snapshot](/docs/xoa-hl/vm-operations/#stopped-snapshot).
- [Install Linux guest tools](/docs/xoa-hl/guest-tools/).
- [Create and use templates](/docs/xoa-hl/templates/).
- [Migrate, export and import a VM](/docs/xoa-hl/vm-transfer/).

## Storage and networks

- [Add disks and network interfaces](/docs/xoa-hl/storage-networks/).
- [Create NFS storage for VM disks](/docs/xoa-hl/storage-networks/#nfs-vm-storage).
- [Create a VLAN network](/docs/xoa-hl/storage-networks/#host-vlan-network).
- [Diagnose a network problem](/docs/xoa-hl/troubleshooting/#network-connectivity).

## Backup and recovery

- [Schedule backups and set retention](/docs/xoa-hl/backup-restore/#backup-schedules).
- [Use incremental backups](/docs/xoa-hl/backup-restore/#delta-backups).
- [Recover a single file](/docs/xoa-hl/backup-restore/#file-restore).
- [Copy a VM to another pool (DR)](/docs/xoa-hl/backup-restore/#dr-replica).
- [Back up to a Windows Server share (SMB)](/docs/xoa-hl/backup-restore/#smb-remote).
- [Fix a failed backup](/docs/xoa-hl/troubleshooting/#backup-failures).

## Hosts, users and security

- [Manage hosts and pools](/docs/xoa-hl/hosts-pools/): connections, the XO Lite button and statistics.
- [Add a host to a pool](/docs/xoa-hl/hosts-pools/#pool-join).
- [Put a host in maintenance mode](/docs/xoa-hl/hosts-pools/#host-maintenance-mode).
- [Manage users, groups and permissions](/docs/xoa-hl/permissions/).
- [Delegate resources with a quota](/docs/xoa-hl/permissions/#resource-set-delegation).
- [Add a one-time code to sign-in](/docs/xoa-hl/sign-in-otp/).

## Keep XOA-HL running

- [Update the appliance](/docs/guides/updates/#updating-xoa-hl-the-appliance) and [update the host](/docs/guides/updates/#updating-xcp-hl-the-host).
- [Plan maintenance and check the result](/docs/xoa-hl/maintenance/).
- [Export the XO configuration](/docs/xoa-hl/configuration-backup/).
- [Back up pool metadata](/docs/xoa-hl/configuration-backup/#pool-metadata).
- [Troubleshoot a problem](/docs/xoa-hl/troubleshooting/).
- [See what each release shipped](/docs/reference/release-matrix/) and [read the changelog](/docs/reference/changelog/).

## Reference

- [Concepts and feature scope](/docs/xoa-hl/concepts/)
- [Service settings](/docs/xoa-hl/configuration/)
- [Automation with xo-cli](/docs/xoa-hl/automation/)
- [Glossary](/docs/xoa-hl/glossary/)
- [Pages for contributors](/docs/components/)

## Help and feedback

The XOA-HL interface and this documentation have separate language settings. Use the selector at the top of this page to change the documentation language. [Page review status](/docs/xoa-hl/translation-status/) shows which pages have been reviewed.

[Report a documentation problem](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Include the page address, the step to fix and your appliance version. Never include passwords or private data.
