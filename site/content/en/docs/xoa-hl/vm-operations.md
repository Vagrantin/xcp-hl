---
title: Operate a VM — snapshots, CPU, memory and deletion
description: Operate a test VM, resize its CPU and memory, and understand deletion boundaries.
weight: 21
translationKey: xoa-manual-vm-operations
translationStatus: source
sourceRevision: sha256:1a66f11d2aaac01ec9a5810382d791682e4e0cf84380a3511c118c219386e5eb
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Use a disposable VM with no production data for this first practice. Sign in to the **XOA-HL appliance** as an administrator and confirm the VM, host and storage are available. Keep an independent [backup and restore test](/docs/xoa-hl/backup-restore/) before changing a valuable VM.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Power, snapshot/revert, clone, CPU/memory changes and deletion tests on this appliance are pending. Later releases can differ.
{{< /callout >}}

## 1. Start, stop and restart

Open the selected VM (`/#/vms/<id>/general`). For a stopped VM, choose **Start** and wait for its state and console to show the intended guest boot. For a running VM, **Stop** or **Reboot** first requests a clean guest shutdown or reboot.

If guest support is missing or an operation is blocked, XO can offer another confirmation that forces the operation or bypasses a block. Read that message before proceeding. Forced shutdown/reboot can lose guest data; use the guest's own shutdown when possible. Do not repeatedly click while a task is active. Check the VM state and console after completion; a success notification alone does not confirm that its application is healthy.

## 2. Choose the right protection

| Item | Purpose and limit |
| --- | --- |
| Snapshot | A VM point in time, dependent on its storage; not an independent backup |
| Fast clone | Another VM using a storage-efficient copy; not protection against losing that storage |
| Backup | A separate recovery copy; validate it with an isolated restore |

Snapshots and clones consume storage as the VMs change. Check the SR's free capacity and remove only test objects you have positively identified. A running snapshot is not proof of application consistency.

## 3. Take and check a stopped snapshot

1. Shut down the disposable guest and confirm its stopped state. Record the VM identity, disk list and a harmless guest file or setting to compare later.
2. Open **Snapshots** (`/#/vms/<id>/snapshots`) and select **New snapshot**. For this exercise, do not use the memory option.
3. Wait for completion. Identify the new row by its date and rename it to a meaningful test label. Check for task errors and remaining storage capacity.

If creation fails, preserve the error and inspect capacity and connectivity before trying again. Do not assume a missing notification means no snapshot was created.

## 4. Revert only the test VM

Change the harmless test data, shut down the guest again, then select the recorded snapshot's **Revert VM to this snapshot** action. Reverting replaces the VM's current state. The confirmation offers a snapshot of the current state first, enabled by default in this release; check that choice and available capacity.

A snapshot taken while running can cause XO to start or resume the VM after revert. Use a stopped snapshot here and inspect the resulting power state before any manual start. Start the guest when appropriate and verify the recorded file/setting and disk inventory. Do not rehearse revert on the appliance or a production VM.

## 5. Prepare an isolated fast clone

On a stopped disposable VM, choose **Fast clone**. Find the new VM (default name ends in `_clone`), record its distinct identity and rename it. Keep it stopped while you [remove every inherited network interface](/docs/xoa-hl/storage-networks/) or arrange verified external isolation. An automatically generated MAC does not remove copied IP addresses, guest credentials or application identities.

Only then start the clone and inspect its console. Reconnect a network only after resolving duplicated identities and validating isolation. If no clone appears after an error, inspect inventory and tasks before retrying. This exercise does not validate live migration, memory snapshots or recovery after SR loss.

## 6. Resize a stopped VM

Use a maintenance window and a disposable guest whose console you can open. Record its ID, guest state, current CPU/memory values and limits before changing anything. Check the host/pool capacity and guest requirements; this guide does not prescribe a universal CPU count or memory size.

{{< callout type="warning" >}}
Stop the guest cleanly and confirm **Halted** before this exercise. A running-VM edit can offer a restart or forced restart when a value cannot be changed live. Cancel that prompt here and arrange the shutdown first. Increasing a limit does not guarantee enough host resources, and reducing memory can prevent the guest from booting.
{{< /callout >}}

1. Open **Advanced** (`/#/vms/<id>/advanced`) and note **CPU limits** and **Memory limits (min/max)**. The CPU row shows current/max values; the maximum is editable when the VM is not running. For an intended CPU count above the recorded maximum, increase that maximum first while the VM is stopped.
2. Open **General** (`/#/vms/<id>/general`). Click the CPU count, enter the intended positive whole number and press **Enter**. Wait, refresh and read back the value before making the next change. Inline fields can also save when focus leaves them; clicking elsewhere is not a safe way to cancel an edit.
3. Click the memory value and use its size/unit control for the intended amount; press **Enter**. This displayed value is the configured **dynamic maximum**, not a measurement of RAM currently used inside the guest. Depending on the existing bounds, the backend updates a fixed-memory configuration or dynamic-memory limits.
4. Refresh **General** and **Advanced** and record all resulting values. CPU count must not exceed its maximum. Memory bounds must remain ordered: static minimum ≤ dynamic minimum ≤ dynamic maximum ≤ static maximum. The source can adjust related limits, so do not assume only the field you clicked changed. This pilot does not establish hotplug, dynamic-memory behavior under load or CPU-topology tuning.
5. Start the test VM and check its console, guest-visible CPU/memory and application health. If it will not start or the values are unexpected, keep it stopped, preserve the task error and restore the recorded configuration in the same controlled window. Re-read every limit and retry only after identifying the cause; a success notification alone is insufficient.

If an edit reports an error, inspect the actual values before retrying. Related changes are not a guaranteed atomic transaction, and a rejected edit does not establish that all previous values were restored. Keep [troubleshooting](/docs/xoa-hl/troubleshooting/) and the recorded baseline available.

## 7. Remove only the disposable VM

{{< callout type="warning" >}}
**Remove** is a destructive VM operation, distinct from disconnecting or detaching a disk. The ordinary confirmation at this pin offers no keep-disks choice. Deletion also processes the VM's snapshots and attempts to delete its attached disk VDIs. If any data or snapshot must be retained, stop before confirming and plan a separate preservation procedure. A snapshot on that VM is not an independent recovery copy.
{{< /callout >}}

1. Confirm that the target is the disposable VM, not the appliance, original guest, template or another VM with a similar name. Record its ID, attached disk IDs/SRs and snapshots. Check its backup/replication schedules and any shared-disk users before deleting it. For valuable data, first complete an independent [backup and isolated restore test](/docs/xoa-hl/backup-restore/).
2. Shut down the guest normally and confirm **Halted**. The deletion backend can hard-shut down a VM that is still running or suspended; do not use **Remove** as a clean shutdown command.
3. Open **Advanced** and choose **Remove**. Read the VM/disk warning and confirm only this intended target. If XO offers a second prompt to remove a protected/blocked VM anyway, cancel this pilot and investigate the protection rather than approving a force retry.
4. Wait, then refresh the VM, snapshot and SR disk inventories. Check the recorded IDs and the deletion task/errors. Shared VDIs still attached to another non-control-domain VM are skipped by this source path; that exception is not a retention guarantee for every disk. Snapshot/VDI cleanup errors can be logged without making the whole deletion fail, so disappearance of the VM or a success notification does not prove complete cleanup.
5. Confirm that the original VM, other guests and any required independent backup remain usable. Reconcile remaining test objects individually using the [disk-management distinctions](/docs/xoa-hl/storage-networks/) and recorded IDs. Do not bulk-delete apparent orphan disks or retry a force operation to recover space. This guide provides no undo; recovery of deleted guest data requires a separately verified recovery copy.

If deletion fails partway or a blocked-delete prompt is cancelled, preserve the remaining VM/disk/snapshot inventory and error. If the VM remains, also inspect its permissions, IP-pool reservations and resource-set membership: the API starts some bookkeeping before the backend's destroy-protection check, so refusal does not guarantee that these records are unchanged. Do not recreate a similarly named VM and assume it is the same object. [Report the problem](/docs/xoa-hl/troubleshooting/) with versions and sanitized IDs before further cleanup.

## Sources

XO 5 pin `e281c536`: [power and snapshot actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM action bar](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [snapshot tab](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [revert confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js) and [revert power behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).

Resizing/deletion at the same pin: [General controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [Advanced limits/Remove](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [inline save behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [VM API permissions/restart/delete parameters](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [constraint ordering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [destroy defaults/shared disks/cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs) and [English labels/warnings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
