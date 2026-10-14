---
title: Operate a VM — snapshots, full copy, CPU, memory and deletion
description: Operate a test VM, make an isolated full copy, resize its CPU and memory, and understand deletion boundaries.
weight: 21
translationKey: xoa-manual-vm-operations
translationStatus: source
sourceRevision: sha256:072ec6d8f72307aa29deb9f37009b955e6aa460139ab998592795861e94d5549
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Use a disposable VM with no production data for this first practice. Sign in to the **XOA-HL appliance** as an administrator and confirm the VM, host and storage are available. Keep an independent [backup and restore test](/docs/xoa-hl/backup-restore/) before changing a valuable VM.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Power, snapshot/revert, clone/full copy, CPU/memory changes and deletion tests on this appliance are pending. Later releases can differ.
{{< /callout >}}

## 1. Start, stop and restart

Open the selected VM (`/#/vms/<id>/general`). For a stopped VM, choose **Start** and wait for its state and console to show the intended guest boot. For a running VM, **Stop** or **Reboot** first requests a clean guest shutdown or reboot.

If guest support is missing or an operation is blocked, XO can offer another confirmation that forces the operation or bypasses a block. Read that message before proceeding. Forced shutdown/reboot can lose guest data; use the guest's own shutdown when possible. Do not repeatedly click while a task is active. Check the VM state and console after completion; a success notification alone does not confirm that its application is healthy.

## 2. Choose the right protection

| Item | Purpose and limit |
| --- | --- |
| Snapshot | A VM point in time, dependent on its storage; not an independent backup |
| Fast clone | Another VM using a storage-efficient copy; not protection against losing that storage |
| Full copy | Another VM with copied disk VDIs on a selected SR; verify its data, placement and isolation before use |
| Backup | A separate recovery copy; validate it with an isolated restore |

Snapshots and clones consume storage as the VMs change. Check the SR's free capacity and remove only test objects you have positively identified. A running snapshot is not proof of application consistency.

## 3. Take and check a stopped snapshot <span id="3-take-and-check-a-stopped-snapshot"></span> {#stopped-snapshot}

This browser exercise uses an XOA-HL administrator account and one disposable VM with ordinary disks, no shared disks or passthrough devices, and a working console. Pause its backup/replication triggers and wait for active tasks to finish. Keep an independent recovery copy for any data you need to retain. Running/memory snapshots and application-consistency guarantees are outside this pilot.

1. In the guest, create a harmless file containing `snapshot-A` and record its checksum. Shut down cleanly and confirm **Halted**. Record the VM UUID, disk VDI IDs/SRs/sizes, existing snapshot UUIDs and available SR capacity. Before taking the snapshot, [remove every test VM network interface](/docs/xoa-hl/storage-networks/) and read back an empty VIF list; use the console for later checks.
2. Check every disk's name. This source can exclude a VDI whose name contains the literal `[NOSNAP]`; that is a substring in the disk name, not a VM tag. Excluded/shared/passthrough disks need a separate procedure. Do not rename them simply to bypass an existing policy. For this pilot, use only ordinary disks without that marker and plan enough space for the snapshot, later writes and the pre-revert snapshot.
3. Open **Snapshots** (`/#/vms/<id>/snapshots`) and select **New snapshot** once. This per-VM button creates the snapshot directly; it does not ask for a name first. The default name combines the VM name and an ISO timestamp. Do not use **New snapshot with memory**.
4. Wait, refresh and identify the new row by its **Creation date** and the row's UUID-copy action. Record that distinct UUID; a name or time alone is insufficient. Edit **Name** to `lab-snapshot-A` and **Description** to a meaningful test note, then refresh and read back both. Inspect the snapshot's disk inventory and SR placement against the baseline, plus task errors and free capacity. Different snapshot VDI IDs are expected; check disk coverage and sizes rather than requiring the original VDI IDs.

**Check:** one identified stopped snapshot covers the intended ordinary disks and the original VM remains stopped with no VIFs. If creation or rename fails, preserve the error and actual VM/snapshot/disk inventory before retrying. No returned ID or missing notification does not prove that nothing was created; a failed rename does not undo snapshot creation.

## 4. Revert only the test VM <span id="4-revert-only-the-test-vm"></span> {#snapshot-revert}

{{< callout type="warning" >}}
Revert replaces the VM's current state, including configuration that can restore earlier network interfaces. Changes after the selected snapshot can be lost. Use only this isolated disposable VM, keep it stopped before reverting, and recheck all VIFs before boot. A snapshot stored on the same SR does not protect against losing that SR.
{{< /callout >}}

1. Start the isolated test VM, change the file to `snapshot-B`, record its new checksum, then shut down cleanly and confirm **Halted**. Record the current disk/VIF/snapshot inventory. Confirm the selected UUID is `lab-snapshot-A` from section 3, not a backup-managed snapshot or a different VM's point.
2. In **Snapshots**, select **Revert VM to this snapshot** for that row. Read the **Revert your VM** confirmation. Leave **Snapshot before** checked for this pilot and verify capacity first. It is enabled by default and makes a separate ordinary snapshot of the current state before requesting revert; it is not an independent backup or a guaranteed rollback transaction. Cancel if the identity, isolation or capacity is uncertain.
3. Confirm once and wait. Refresh and record the selected snapshot UUID, new pre-revert snapshot UUID, VM power state, disk inventory, VIFs and task errors. A failed pre-revert snapshot prevents the subsequent revert request in this UI path; a later revert failure can leave the pre-revert snapshot. Inspect actual state before any retry. Do not uncheck preservation simply to work around an unexplained error.
4. Confirm **Halted** and an empty VIF list before manually starting the VM. If a VIF reappears, remove it while stopped and read back isolation first. A snapshot originally taken while running can trigger an asynchronous start/resume after revert; successful revert does not establish successful guest boot. Such snapshots are outside this pilot.
5. Boot through the console. Verify `snapshot-A` and its original checksum, guest disks and application behavior. Shut down again and record the result. The additional pre-revert snapshot should be separately identified as the `snapshot-B` state; recovering it needs its own controlled verification, not an assumed undo.

### Remove an identified test snapshot {#snapshot-cleanup}

After recording the result and arranging any required independent recovery copy, keep the VM stopped and remove only a test snapshot whose UUID and ownership you recorded. In **Snapshots**, use that row's **Remove this snapshot**, read **Delete snapshot** and confirm one target. Do not use **Remove selected snapshots**, delete a backup-managed point, or confuse this with the VM's **Remove** action.

Wait and refresh snapshots, VM disks and SR capacity. Confirm the recorded snapshot is absent, retained points and the original VM remain, and check errors. Disk cleanup can log failures without failing the whole deletion; disappearance of the row or a success notification does not establish complete cleanup or immediate space reclamation. Preserve remaining-object IDs and [report unexplained leftovers](/docs/xoa-hl/troubleshooting/); do not bulk-delete apparently orphaned VDIs. This procedure offers no undelete.

## 5. Prepare an isolated fast clone

On a stopped disposable VM, choose **Fast clone**. Find the new VM (default name ends in `_clone`), record its distinct identity and rename it. Keep it stopped while you [remove every inherited network interface](/docs/xoa-hl/storage-networks/) or arrange verified external isolation. An automatically generated MAC does not remove copied IP addresses, guest credentials or application identities.

Only then start the clone and inspect its console. Reconnect a network only after resolving duplicated identities and validating isolation. If no clone appears after an error, inspect inventory and tasks before retrying. This exercise does not validate live migration, memory snapshots or recovery after SR loss.

### Make a full copy within the same pool {#full-copy}

Use **Copy**, not the separate **Fast clone** action, when you intend a normal disk copy on a chosen SR. The Copy dialog also offers **Fast clone**; leave **Full copy** selected for this exercise. Neither a fast clone nor a same-pool full copy establishes an independent backup or tested disaster recovery.

1. Use one disposable VM with ordinary attached disks and no shared disks or passthrough devices. While the guest is available, record a harmless file and its checksum. Shut down cleanly, confirm **Halted**, and record the source VM ID, disk VDI IDs/SRs/sizes, VIFs and any snapshots. This exercise checks the current VM's disks; it makes no promise of copying snapshot history.
2. Identify a different writable **VM-disk SR in the same pool**. Check its ID, free capacity and access from the host intended to run the copy. An ISO library is not this destination. Allow space for the disk copies and later growth; the dialog does not reserve or prove sufficient capacity. If the target is unavailable, stop and resolve storage access before starting a copy.
3. On the source VM, choose **Copy**. In **Copy VM**, set **Name** to a unique test name such as `lab-vm-full-copy`; the default pattern is `{name}_COPY`, and an empty field preserves the original name. Confirm **Full copy**, then **Select SR** using the recorded destination ID and pool, not just a similar name. Other pools can appear depending on the effective UI plan; selecting one changes the backend path to export/import and is outside this pilot. Leave **Compression** at **Disabled**; the same-pool path uses XAPI `VM.copy`, not a compressed transfer.
4. Confirm once and wait for the task. Refresh inventory and identify the new VM by its distinct ID and chosen name. Verify **Halted**, its disk count/sizes, distinct disk VDI IDs and each disk's destination SR. Check that the source VM and its disks still exist unchanged. A notification or matching name alone does not prove a complete copy. If the new VM is unexpectedly running or objects differ, stop the exercise and restore isolation before proceeding.
5. Keep the new VM stopped while you [remove every inherited VIF](/docs/xoa-hl/storage-networks/). Read back an empty VIF list before the first boot. Do not depend on MAC regeneration: guest IP addresses, credentials and application identities are copied. Start only the isolated copy, open its console and verify the recorded file checksum, guest disks and application behavior. Resolve duplicate identities before any network reconnection; keep the original isolated or stopped while checking conflicting identities.
6. Shut down the copy after the check. Record the result and use section 7 to remove only the positively identified test VM/disks, preserving the source and any independent backup. Cleanup is destructive and requires its own post-operation inventory.

On an error, lost connection or interrupted request, preserve the task/error plus source/destination VM, VDI and snapshot inventories before retrying. The source wrapper does not guarantee rollback of an incomplete XAPI copy; no returned VM ID does not prove that no object was created. Inspect capacity and host/SR access, reconcile exact IDs and [report unexplained leftovers](/docs/xoa-hl/troubleshooting/). Do not retry blindly or bulk-delete apparent orphan disks. Running/suspended copies, cross-pool transfer, template copies, shared/passthrough disks, snapshot-history preservation and recovery after SR loss need separate acceptance.

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

Full copy at XO 5 pin `e281c536`: [Copy dialog/defaults/name pattern](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/copy-vms-modal/index.js), [copy/clone requests](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM/SR permissions and pool branch](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [XAPI copy/clone/remote-copy wrapper](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs) and [writable-SR selector](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).

XO 5 pin `e281c536`: [power and snapshot actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM action bar](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [snapshot tab](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [revert confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js) and [revert power behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).

Resizing/deletion at the same pin: [General controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [Advanced limits/Remove](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [inline save behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [VM API permissions/restart/delete parameters](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [constraint ordering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [destroy defaults/shared disks/cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs) and [English labels/warnings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).

Snapshot coverage/deletion at the same pin: [snapshot/revert permissions and [NOSNAP] option](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [disk-name matching and disk cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs).
