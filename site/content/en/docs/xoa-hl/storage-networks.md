---
title: Manage NFS storage, ISO libraries, disks and network interfaces
description: Connect NFS ISO and VM-disk storage, add a test disk and manage isolated VM interfaces.
weight: 22
translationKey: xoa-manual-storage-networks
translationStatus: source
sourceRevision: sha256:93f126a0cebd79047220a59e8cc7b98e37cf47ebba0a665285a67fdc4b15cfd6
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Practice on a stopped disposable VM, as an administrator in the **XOA-HL appliance**. Record its identity, existing disks and interfaces. Choose a writable SR with enough free capacity and an existing network whose isolation has been verified outside XO. Do not use the appliance itself as the test guest.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. NFS provisioning, disk, interface and guest-discovery tests on the released appliance are pending.
{{< /callout >}}

## 1. Identify the objects

| Object | What it represents |
| --- | --- |
| SR | Storage repository that holds virtual disks; check its free capacity |
| VDI | Virtual disk data stored in an SR |
| VBD | The attachment between a VM and a virtual disk |
| VIF | A VM's virtual network interface |
| PIF | A host's network interface; changing management connectivity can disconnect the host |

A VM interface is not the host management interface. Selecting a network or generating a new MAC does not establish isolation; verify the actual VLAN, uplink and routing before using it for a cloned or restored guest.

## 2. Add a small blank disk

1. Confirm the test VM is stopped. Open **Disks** (`/#/vms/<id>/disks`) and select **New disk**.
2. Select the intended writable SR in the same pool, a clear test name and a small size with explicit units. Review the read-only choice; leave it off for a writable test disk. Create the disk once and wait for completion.
3. Verify the new row's name, size, SR and attachment to the intended VM. Record its identity and check remaining SR capacity before starting the guest.

In the guest console, identify the new disk by its size and device information. XO creates the virtual disk and attachment; it does not automatically partition, format or mount it inside the guest. Guest filesystem procedures are outside this pilot. Do not format a device based only on a guessed device name.

If creation fails, inspect the task and both VM/SR inventories before retrying: a partially completed operation may leave a disk. Preserve the error, check capacity and connectivity, and [troubleshoot](/docs/xoa-hl/troubleshooting/) if necessary. Disk shrinking, expansion and storage migration are not validated by this exercise.

## 3. Distinguish detach from delete

A VBD removal detaches the disk from the VM. It does not mean its VDI data was deleted. VDI deletion destroys the disk data; it is a different action, with deletion unavailable while attached in this UI. Disconnecting an attachment is also distinct from removing it.

For cleanup, stop the guest and positively identify only the blank test disk. Keep its VDI if its contents might be needed. Never delete a boot disk, shared disk or unidentified VDI to fix a capacity warning. [Back up valuable guest data](/docs/xoa-hl/backup-restore/) independently.

## 4. Add an isolated VM interface

On the stopped test VM, open **Network** (`/#/vms/<id>/network`) and choose **New device**. Select the verified isolated network in the same pool. Leave the MAC empty for automatic generation, then select **Create**. Check the new interface, network and MAC before booting; inspect the guest's device detection and intended connectivity afterwards.

For an isolated clone or restore, remove **all** inherited VIFs while the VM is stopped, and confirm the interface list is empty before its first boot. Use the interface deletion action, not merely its connect/disconnect toggle: disconnection alone is not the isolation procedure. Add a test network only after confirming it cannot reach production and resolving copied guest identities.

If connectivity is unexpected, stop the test VM and inspect its network mapping and external isolation before retrying. This guide does not configure host PIFs, management addresses, bonds or VLANs. Do not alter the host management network during this exercise. Continue with [VM operations](/docs/xoa-hl/vm-operations/) or [host and pool ownership](/docs/xoa-hl/hosts-pools/).

## 5. Connect an NFS ISO library {#nfs-iso-library}

An ISO SR holds installation media; it is separate from the writable SR used for VM disks and from a backup remote. This exercise connects an existing, dedicated NFS export containing a vendor-verified installer ISO. Preparing the NAS/export and placing the file there are tasks for its storage administrator, outside this browser procedure. No host shell commands or management-network edits are required in this browser procedure.

Before creating anything, check whether a suitable ISO SR already exists in the intended pool. Use it if its identity, host access and media are correct. For a new test library, record the NFS server address, exact exported path, agreed NFS version, intended pool/hosts and ISO filename/checksum. Each host that will read the ISO must be permitted to access the export. Access from your browser or from the XOA-HL appliance alone is not proof of host access.

1. As an administrator, open **New → Storage** (`/#/new/sr`). Choose a host in the intended pool. Enter a distinct name such as `lab-nfs-iso` and a description identifying the test export.
2. Under **ISO SR**, select **NFS ISO**. Do not select **NFS** in the **VDI SR** group: that creates VM-disk storage. **Local** refers to a path on a hypervisor host, not a folder on your computer or the appliance; local, SMB and block-device provisioning are outside this exercise.
3. Enter the NFS server in **Server**. Select the NFS version agreed with the storage administrator (the form offers a default plus `4` and `4.1`), then use the search icon beside the server. Changing the version does not rerun discovery: search again after a change. Leave **Comma delimited NFS options** empty for the initial test unless specific options have been agreed.
4. Select the exact export in **Path**. Use the export root for this pilot; subdirectory setup is outside its scope. Wait for the path check. If the server/export is absent, probing fails, or **Storage usage** shows existing SRs, stop and inspect the error and identities. This wizard uses NFS probes even for NFS ISO; a detected SR is not proof that it is an ISO library. Do not reattach it or accept a warning about creating over existing storage.
5. In **Summary**, review the name and selected type (`nfsiso`). Recheck the host selection and the actual server/path in the earlier sections, then select **Create** once. If the request fails, inspect the pool's SR inventory before retrying; a request can leave a partially created SR or host attachment.

The created SR's backend type is `iso`; `nfsiso` is the wizard choice. Record the SR UUID, then open **Hosts** (`/#/srs/<id>/hosts`) and verify each intended host's attachment is connected and its displayed location matches the export. A shared-SR declaration does not establish working access from every host. Keep the selected VM host within the observed access scope.

Use the SR's refresh action **Rescan all disks**, wait for the request to complete, then open **Disks** (`/#/srs/<id>/disks`). Check the expected ISO name and size. After the storage administrator adds or replaces a file, rescan again. Verify the file's vendor checksum at its source; a successful scan or matching filename is not an integrity check.

In [the new-VM wizard](/docs/xoa-hl/create-vm/), choose the same pool and check that **ISO/DVD** offers the expected media. If it is already in the library, skip the browser-upload step. Reading existing media and uploading new media are different capabilities: the Import selector does not prove that this SR/export permits ISO creation and writing. Do not change permissions broadly to make an upload work.

| Symptom | Check and next action |
| --- | --- |
| No export found or path probe fails | Record the displayed error; verify server/path, selected version, export discovery and host access with the storage administrator. Stop if the wizard cannot discover this export. |
| SR created but a host is disconnected | Check that host's attachment/location and access to the export. A connected peer host is not sufficient; do not disconnect all hosts as a repair experiment. |
| Scan succeeds but ISO is absent | Check the completed file at the agreed export, its name/size and the selected SR. Rescan only after correcting the source; do not recreate the SR repeatedly. |
| ISO missing from ISO/DVD | Check the wizard's pool, ISO SR type, media presence and intended host attachment. A VM-disk NFS SR is not an ISO SR. |
| Creation fails or unexpected SR appears | Preserve the error and UUID/attachment inventory. Identify partial objects before any retry or cleanup; do not use Forget, Remove or storage formatting to clear an unidentified error. |

Do not remove an ISO or disconnect/forget its SR while a VM uses it. Record consumers and eject media from the test guest before planning cleanup. This pilot does not establish a destructive SR-removal procedure or writable ISO-upload support.

## 6. Create NFS storage for VM disks {#nfs-vm-storage}

Use this separate exercise when you need a **writable VM-disk SR**. An NFS ISO library supplies installation media; an NFS backup remote stores independent backups. Neither is the VM-disk SR created here. Shared storage alone does not provide a backup or establish migration/HA readiness.

### Prepare a dedicated export

Use an empty, dedicated lab export approved by its storage administrator, with space for the test disk and reserve capacity. Record the NFS server, exact export root, agreed version/options, pool and every intended host. The storage administrator must approve host read/write access and check server capacity and quotas. Do not reuse the ISO export, backup destination or an export containing unidentified data. NAS configuration and host-network changes are outside this browser exercise.

Sign in to the **XOA-HL appliance** as an administrator. The creation and probe APIs require administration of the selected host. Record the current SR inventory first. If the intended storage already exists in that pool, verify its UUID and host access instead of creating another SR. SR creation does not require an existing VM. For the later disk verification, use a stopped disposable VM with independent console access and an independent backup for any valuable data. If this is your first VM, [create and install it](/docs/xoa-hl/create-vm/) on the new SR after completing the SR readback below, then return here. Do not use XOA-HL itself as the test VM.

### Create and read back the SR

1. Open **New → Storage** (`/#/new/sr`), select a host in the intended pool and enter a distinct name such as `lab-nfs-vdis` plus a description identifying the export. Under **VDI SR**, select **NFS**. Check that **NFS ISO** in **ISO SR** is not selected.
2. Enter **Server**, choose the agreed **NFS version** (default, `4` or `4.1`) and use the server search icon. Leave **Comma delimited NFS options** empty unless specific options have been agreed. If the server or version changes, repeat discovery and path selection; changing the version alone does not reprobe the export.
3. Select the exact export root in **Path**, leave the subdirectory unused and wait for the probe. Inspect **Storage usage**. If any existing SR UUID or in-use entry appears, stop and identify it with the storage owner. Do not choose reattach or create another SR over it. The NFS creation branch does **not** require the existing-storage confirmation used for some other types; absence of a warning does not establish that an export is empty.
4. In **Summary**, check name, type `nfs` and path. Recheck the host, server, version and options in the earlier sections, then select **Create** once. Wait for completion. On an error, inspect the SR and host-attachment inventories before any retry; do not assume the failed request left nothing behind.
5. Record the resulting SR UUID. On **General** (`/#/srs/<id>/general`), check `Type: nfs`, size, used/free capacity and the intended pool. Open **Hosts** (`/#/srs/<id>/hosts`): record each intended host and its attachment (PBD), check **Connected** and the configuration entries `server` and `serverpath`, plus `nfsversion`/`options` when supplied. A shared declaration or one connected host does not verify every host. If an intended attachment is absent or disconnected, stop before allocating or moving workloads there. The status button is actionable: read its state without clicking to test it.

### Verify a disposable disk

Follow [Add a small blank disk](#2-add-a-small-blank-disk), selecting this exact SR on the stopped test VM. Record VM, VDI and attachment identities and recheck the disk's SR and size. Start the guest only on a host whose attachment was checked. Identify the extra disk from its size and device details; guest partitioning, formatting and mounting require a separate OS-specific procedure and positive device identification.

If a guest administrator prepares that **test disk**, write a harmless sample there and record its checksum. After saving work and performing a normal guest shutdown/boot, confirm the same disk, sample and checksum. Keep this result separate from an independent backup/restore test. An empty-disk allocation or a successful rescan alone does not demonstrate guest writes or persistence. Repeat guest read/write acceptance on each intended host through a separately approved placement/migration exercise before claiming pool-wide access.

### Handle failure and plan cleanup

| Symptom | Check and next action |
| --- | --- |
| No export or failed probe | Preserve the exact error and selected host/server/path/version. Ask the storage administrator to check discovery, host permissions and connectivity. Do not switch to local/block storage or broaden permissions to bypass the failure. |
| Existing SR detected or creation fails | Record all detected/resulting SR UUIDs and attachments, including partial objects. Establish ownership and current consumers before a retry or reattachment decision. |
| Wrong type, path or disconnected host | Stop new allocations; compare the recorded export with each host attachment. Do not disconnect all hosts or remove an SR as a diagnosis step. |
| Capacity warning or failed disk write | Check both SR usage and server free space/quotas, active tasks and the exact guest disk. Preserve evidence and data; do not delete unidentified disks, snapshots or NAS files. |

For cleanup, save the final object inventory and stop the test VM normally. Use the earlier [detach versus delete guidance](#3-distinguish-detach-from-delete) only for the positively identified test disk. Retain the SR/export until every consumer and recovery requirement is accounted for with its owner. This exercise does not prescribe SR destruction, forgetting, reattachment, removal of NAS files, or changes to default storage. Local/SMB/iSCSI provisioning, NFS subdirectories, outages, performance and pool-wide migration/HA need separate validation.

## Sources

XO 5 pin `e281c536`: [disk UI and SR selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [VM interface UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js) and [disk/interface actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).

[new SR wizard](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js) / [SR API/probes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs) / [SR rescan action](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js) / [host attachments](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js) / [ISO import API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs) / [new VM ISO selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).

SR capacity and usage view: [XO5 `tab-general.js`](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js).
