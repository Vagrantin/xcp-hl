---
title: Manage storage and network interfaces
description: Add a test disk and isolated network interface without changing host management.
weight: 22
translationKey: xoa-manual-storage-networks
translationStatus: source
sourceRevision: sha256:707daba14083e52696337827be5317053e28a178e872d1824f84603a0c6fccec
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Practice on a stopped disposable VM, as an administrator in the **XOA-HL appliance**. Record its identity, existing disks and interfaces. Choose a writable SR with enough free capacity and an existing network whose isolation has been verified outside XO. Do not use the appliance itself as the test guest.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Disk, interface and guest-discovery tests on the released appliance are pending.
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

## Sources

XO 5 pin `e281c536`: [disk UI and SR selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [VM interface UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js) and [disk/interface actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
