---
title: "Migrate, export and import a VM"
linkTitle: "Migrate and export"
description: "Move a VM to another host in its pool, export it as an XVA file and import a copy."
weight: 43
translationKey: xoa-manual-vm-transfer
translationStatus: source
sourceRevision: sha256:1e0c1a71359bc2780a31862ccef13422bbb20137e03c5b77f967d92131a100d9
glossaryTerms: ["vm", "host", "pool", "sr", "snapshot", "backup"]
---

Use a disposable VM with no production data. Sign in to the **XOA-HL appliance** as an administrator and confirm the hosts, storage and the VM are available. Migration and export move or copy a whole VM; neither replaces an independent [backup and restore test](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; migration, export and import are not yet tested on a lab system. Later versions can differ.
{{< /callout >}}

## 1. Choose the operation

| Goal | Operation | Result |
| --- | --- | --- |
| Run the same VM on another host of its pool | **Migrate** | Same VM object; disks stay on shared storage or are copied to a selected SR |
| Keep a portable file of a stopped VM | **Export** as XVA | A file saved by your browser; no schedule, retention or restore check |
| Create a separate VM from an XVA file | **Import** | A new VM object with copied guest identities; isolate it like a clone |
| Recover after loss | [Backup and restore](/docs/xoa-hl/backup-restore/) | An independent copy validated by an isolated restore |

This guide covers migration between hosts of the **same pool**, XVA export without compression and XVA file import. Cross-pool migration, network remapping, OVA files, import from a URL, disk-only import/export and VMware import are outside its scope. The HomeLab menu hides the VMware import entry.

Additional source-reviewed modes are described in [Additional transfer modes](#transfer-modes); installed acceptance remains separate.

## 2. Migrate a VM within its pool

Prerequisites, checked before you start:

- The pool has at least two connected hosts, and you hold administrate permission on the VM and the target host.
- The target host reaches the VM's networks and storage. Disks on a shared SR need no copy. A disk on storage the target cannot reach, such as a local SR, is copied.
- A maintenance window. A running guest pauses briefly during live migration; a disk copy takes longer and needs free capacity on the target SR.
- A record of the VM ID, current host, each disk and its SR, and a guest check such as a console login or an application test.

1. Open the VM and choose **Migrate**. It is offered for running and halted VMs, not for suspended or paused ones. Self-service users do not see it.
2. In **Migrate VM**, use **Select a destination host:** to pick another host of the same pool. The list excludes the current host. It can also list hosts of other connected pools; do not choose them for this exercise.
3. Read the storage section. If every disk is on a shared SR, no SR is required. Otherwise, XO requires a main SR (**Select main SR…**) and lets you pick an SR for each VDI. Choose writable SRs with enough free space; those disks are copied.
4. **Select a migration network:** is optional within a pool. XO preselects the pool's configured migration network when the target host has an address on it. Any selected network makes XO use the storage-migration path instead of a simple pool migration. Keep the proposed value unless your pool design names another network.
5. Confirm and wait for the task to finish. Do not click again while the migration is pending.
6. Refresh the VM's **General** tab. Check the host, power state, console, guest network and application. After a disk copy, check where each disk now resides and the free space on both SRs.

{{< callout type="warning" >}}
If XAPI reports that the VM is incompatible with the target host, XO offers **Force migration**. Cancel it in this exercise and investigate CPU and host compatibility. A forced migration can leave the guest unusable.
{{< /callout >}}

If a simple pool migration reports that an SR is required, XO retries it automatically as a storage migration. It then uses SRs connected to the target host or the pool's default SR. A migration you expected to be quick can therefore become a disk copy. If a migration fails, preserve the task error and check the VM's host, power state and disks on every SR involved before retrying. Do not retry with force.

## 3. Export a stopped VM as an XVA file

You need administrate permission on the VM and enough free space on the computer running the browser.

1. Shut down the guest cleanly and confirm **Halted**. Record the VM ID, name, disks and their total size.
2. Choose **Export**. Keep **Type** set to `xva`. Keep **Compression** set to **Disabled**, the default. The other choices are GZIP (very slow) and, on XCP-ng hosts, Zstd. Importing a compressed XVA is not covered by this guide.
3. Confirm. **Download VM** shows a download link, **OK** and **Cancel**. The link and **OK** open the same URL, which the message describes as valid once, for a short period. Use only one of them: select the link, then close the dialog with **Cancel**. The URL contains a one-time access token: treat it as a secret until it is used.
4. The browser saves a file named `<date> - <VM name>.xva`. Keep the download running until it ends; cancelling it stops the export. Check that the file size is plausible against the recorded disk sizes.
5. On the computer running the browser, record a checksum of the file, for example `sha256sum "<file>.xva"`. Use it to check the file before an import.

By default, at most two XVA exports run at once for a pool. A further download fails instead of waiting. Let running exports finish, then request a new link.

An XVA contains the VM's disks and configuration. Store it like the data inside it and delete it when the test is over. An export file has no schedule, retention or restore validation, so it is not a backup job.

{{< callout type="warning" >}}
Exporting a running VM is possible, but XO then exports a temporary snapshot named `[XO Export] <VM name>`. This copy is not application-consistent. XO deletes the snapshot when the download ends. If deletion fails, it only logs a warning and the snapshot can remain on the SR. After a running export, check the VM's **Snapshots** tab. This guide uses a halted VM instead.
{{< /callout >}}

## 4. Import the XVA as an isolated copy

1. Open **Import** > **VM** (`/#/import/vm`). The menu entry appears only when you can operate at least one pool.
2. Choose the target pool in **To Pool:**. **To SR:** proposes the pool's default SR. Choose a writable SR with enough free space.
3. Drop the `.xva` file on the area marked **Drop OVA or XVA files here to import Virtual Machines.** Check the file name and size in the list. Files without an `.xva` or `.ova` extension are ignored. Leave **From URL** disabled.
4. Select **Import** and keep the browser tab open until the upload ends. For a single file, XO opens the new VM's page after success.
5. Keep the imported VM stopped. Record its ID: it is a different object from the source VM even when the name is the same. Rename it so that nobody confuses the two.
6. Before the first start, open **Network** and [remove every virtual interface](/docs/xoa-hl/storage-networks/) or arrange verified external isolation. The copy carries the same guest operating system, IP settings, host name, credentials and application identities as the source.
7. Start the copy and check its console and the recorded test data.

XO refuses to start a VM whose interface MAC address duplicates one of its own interfaces or a running VM's interface. The error code is `DUPLICATED_MAC_ADDRESS`. Do not force the start; remove or isolate the interface first.

If the import fails (**VM import failed**), objects can remain. Check the target SR's disks and the VM list for objects created during the attempt before you retry. Remove only positively identified leftovers, using the [disposable VM removal procedure](/docs/xoa-hl/vm-operations/#delete-vm).

## 5. Clean up

1. Remove the imported test VM with the [disposable VM removal procedure](/docs/xoa-hl/vm-operations/#delete-vm).
2. Delete the XVA file from the computer and from any temporary location.
3. Confirm the source VM is still present, on the expected host, with its disks and data unchanged.

If something does not match, keep the records and [report the problem](/docs/xoa-hl/troubleshooting/) with versions and sanitized IDs.

{{< details title="Sources" closed="true" >}}
Checked against XO 5 commit `e281c536` with the released HomeLab patches: [VM action bar](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [migrate/export/import actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [migration dialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/migrate-vm-modal/index.js), [default migration network](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/utils.js), [export dialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/export-vm-modal/index.js), [compression choices](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-compression.js), [import page](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [VM API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [XAPI migration, import and start checks](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [export snapshot handling](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [export concurrency](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml) and [UI labels](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js). HomeLab menu changes: [VMware import entry](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzz-xoa-hl-hide-vmware-and-support-alert.patch).
{{< /details >}}
## Additional transfer modes (VM08) {#transfer-modes}

Scope: XO 5.113.2 `e281c536`, XOA-HL ce40/ce47 sources. Use an administrator and a disposable, console-accessible VM with ordinary disks, a flushed checksum sample, no VIFs, jobs off and enough space for temporary snapshots and imports. Keep an independent backup. Lab acceptance is mode-specific.

1. **Running export:** flush the sample, leave the isolated VM running, choose **Export**, type **XVA** and compression **Disabled**. Download fully and record size/hash. The running export uses a temporary `[XO Export]` snapshot; check its cleanup and source health after completion or cancellation. It is not an application-consistent or memory export.
2. **Compressed XVA:** repeat with **GZIP (very slow)** (`native`) compression; test **Zstd** separately only if the host advertises it. Record the exact selection. Keep the `.xva` extension. Import each completed file through **Import → VM** into the disposable SR, as in the XVA procedure. Do not infer compressed-import acceptance from uncompressed success.
3. **OVA:** export the same isolated VM with type **OVA**; the XVA compression selector does not apply. In **Import → VM**, select the downloaded `.ova`, review parsed name, CPU, RAM, disks and networks, choose the SR and import once. Parsing success does not establish guest boot or fidelity. Record any unsupported disk/format error, without converting or silently dropping disks to make it pass.
4. **URL import:** place a completed, hashed XVA on an owner-controlled URL reachable by the appliance. Use **Import → VM → From URL**, type **XVA**, exact URL and test SR. The appliance fetches the URL; browser access is insufficient. Do not put credentials in it. This pin refuses non-XVA URL VM imports. A failed request can leave objects: inventory before retry.
5. **Disk-only:** use **Import → Disk**, choose the writable test SR and a known `.vhd`, `.vmdk` or `.raw` file (ISO has its own SR requirements). Check name, format, size and resulting VDI UUID. This creates a disk, not a bootable VM. Attach it to a halted recovery VM at an unused position, remove all VIFs, start and check the sample. In the source VM's **Disks** tab, the disk download action exports one VDI; choose a supported offered format, save/hash it and import it separately for the same check. Disk URL import in this UI offers **ISO** only, not a general URL VM or arbitrary disk converter.

For every imported VM, verify a distinct UUID, disk count/sizes/SRs and power state. Keep it halted and remove every inherited VIF before start. Check console boot and the sample checksum. Delete only identified test copies/VDIs after checks. On interruption, preserve the file/error and compare source, destination, snapshot and capacity inventories; a download filename or successful notification is not a restore test.

Pinned implementation: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [@xen-orchestra/xapi/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [packages/xo-server/src/xapi/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [packages/xo-web/src/xo-app/vm-import/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [packages/xo-web/src/xo-app/disk-import/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [packages/xo-web/src/xo-app/vm/tab-disks.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [packages/xo-server/src/api/disk.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs).

**Lab result, 2026-11-03 (partial, API not browser):** Observed through the REST and JSON-RPC export and import methods that these pages use. A running export of the lab guest (4 GiB disk) completed uncompressed at 3,251,286,528 bytes. `vm.export` with `compress` set to `gzip` and `zstd` returned whole-file gzip (323,244,900 bytes) and zstd (295,357,297 bytes) wrappers of the same archive, not per-chunk compression; both decompress to 3,251,286,528 bytes. The REST export accepts only a boolean `compress`. URL import of both compressed files worked (new halted VMs with new MAC addresses). OVA export of the running guest produced `metadata.ovf` and one VMDK, but uploading that OVA to the import endpoint stalled for over nine minutes and left a partial `[Importing...]` VM, so OVA import is not accepted. Disk URL import accepted VHD and raw only; VMDK and QCOW2 URL imports were refused and a QCOW2 export returned HTTP 500 (`unknown error`). A VHD file imported as `raw` created a wrong 2 MiB disk, so declare the format correctly. No guest boot or data checksum was checked and the mode stays open.
