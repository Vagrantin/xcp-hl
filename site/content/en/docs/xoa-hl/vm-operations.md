---
title: "Manage VMs: console, snapshots, copies, memory and deletion"
linkTitle: "Manage VMs"
description: "Use the console, start and stop a VM, take snapshots, copy, resize and delete VMs."
weight: 40
translationKey: xoa-manual-vm-operations
translationStatus: source
sourceRevision: sha256:b320f3d340c44bc8ba715346e24fd8c93a271e65398b0299c5af51451051c738
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Everyday VM tasks: use the console, start and stop a VM, take and revert snapshots, make clones and copies, change CPU and memory, and delete a VM. Practise each task on a test VM that holds no production data, signed in to the **XOA-HL appliance** as an administrator. Before you change a VM that matters, make sure you have an independent [backup and a tested restore](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. Later versions can differ.
{{< /callout >}}

**D3 observations:** on 2026-10-28, XOA-HL `v5.113.2_e281c536-ce47` (`ca44911`) on one nested XCP-HL v8.3-ce44 host. Tests used disposable clones of one guest with PV drivers but no management agent. The [lab record](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6459388202) covers the power, stopped snapshot/revert, fast clone, disk, resize and deletion observations below. Other procedures remain based on source review. Running or memory snapshots, shared disks and protected VM removal were not tested.

## Use the VM console {#vm-console}

The console shows the VM's screen in your browser. You need permission to **operate** the VM: a Viewer grant is not enough. The guest does not need an IP address for the console, but your browser must reach the appliance, and the appliance must reach the host. Keep the test VM's network isolation as it is.

1. Open the VM's **Console** tab (`/#/vms/<id>/console`). Check that it is the right VM and that its state is **Running**. For any other state, including paused or suspended, the tab shows **Console is only available for running VMs.** Start the VM with a planned [power operation](#vm-power); never force a restart just to get a console.
2. Wait for the expected screen, such as a login prompt, the installer or a known application. The credentials you type here belong to the guest, not to XOA-HL or the host.
3. Move the pointer into the console area to send your keyboard and mouse to the guest. Move it out to get them back, along with the XO shortcuts. To test input, type a harmless string such as `console-test` in a text editor inside the test guest, then delete it. Never test in a shell command or a password field. Seeing the screen does not prove that input works.
4. On a large screen, the zoom controls start at **100%**. They change the display in your browser, not the guest's screen resolution, and they may be hidden on small screens. **Hide info** and **Show info** only hide or show the XO header; they do not stop the guest or switch to full screen.
5. When you are done, leave the tab. This closes the console connection but does not stop the guest. If the VM restarted while you were connected, reopen the tab to get a fresh screen. XO may not notice a disconnection after a restart, and its automatic reconnection attempts do not prove that the guest is healthy.

**Check:** you see the right running guest, your test input reaches it, the XO controls work again when the pointer leaves the console, and the VM is still in the state you expect.

### Clipboard and remote client buttons

- The clipboard text box sends its content to the guest's clipboard after a short pause. **Copy** copies the box's text to your own computer's clipboard. The multi-line button opens **Send to clipboard**. Test with harmless text, and check pasting inside the guest separately. Never put passwords or private data in the box or in screenshots.
- **SSH**, **SSH as…** and **RDP** open your own computer's `ssh://` or `rdp://` handler with the IP address that the guest reports. The buttons appear when an IP address is reported. That does not prove that you have a client installed, that the guest runs the service, or that the network allows it. These buttons do not repair or replace the console.
- **Ctrl+Alt+Del** asks for confirmation, then sends that key combination to the guest. Depending on the guest, it can restart it. Cancel it for this test; it is not a connection test. The ISO selector changes the guest's mounted media: see [Create your first VM](/docs/xoa-hl/create-vm/) before you change it.

### Fix a blank or unresponsive console

1. **The VM is not running, or the console is disabled.** Read the state and the message first. A running VM with `disable_pv_vnc=1` shows **Console is disabled for this VM** instead of the screen. Ask the owner of that setting before you change the VM. Installing tools or restarting does not turn the console back on.
2. **The connection never opens, or keeps dropping.** Check that your account can operate the VM and that the host connection is healthy. In your browser's developer tools, find the WebSocket request ending in `/api/consoles/<id>` and note its error or status. A reverse proxy in front of the appliance must allow WebSocket upgrades, not just normal page requests. Check browser-to-appliance access (including TLS) separately from appliance-to-host access. The guest's IP address, SSH server and firewall are not part of the console path. Fix the problem with the owner of that path. Never expose a VNC port publicly or turn off certificate checks as a quick fix.
3. **The connection opens, but the screen is blank or frozen.** Check that you opened the right VM, what it should show, and any recent power operations. Reopen the tab after a restart. A blank screen can come from the guest or from the connection, so save what you see before you try a guest-specific fix. Do not keep restarting the VM, reinstall it or change its boot media just because the screen is black.
4. **The screen works, but typing or the clipboard does not.** Move the pointer out of the console and back in, then repeat the editor test. Check whether your browser or operating system intercepts the keys, and whether the guest supports the clipboard operation. Treat SSH or RDP problems separately. In your [problem report](/docs/xoa-hl/troubleshooting/#report-a-problem), give the browser and its version, the VM and host IDs, the time, the power state, the exact message and the connection errors, without private data. Keep raw browser traces private: cookies, tokens, clipboard text and guest screens can be sensitive.

## Start, stop and restart a VM {#vm-power}

First open the VM's **General** tab (`/#/vms/<id>/general`) and check whether a management agent is detected. Without it, XO cannot shut the guest down cleanly or restart it. See [the guest tools status and installation guide](/docs/xoa-hl/guest-tools/#guest-tools-status).

On the one guest without a management agent in the D3 run, a clean stop waited 1200 seconds, then failed with `VM_SHUTDOWN_TIMEOUT`. The VM stayed **Running**. Restart was refused immediately with "VM lacks feature". A forced stop changed the VM to **Halted** within seconds.

If the VM is stopped, select **Start** and check the state and console. Before a clean stop or restart, install the guest tools and check the agent, or shut the guest down from inside. Use a forced stop only when the guest cannot be shut down. It is like pulling the power and can lose data.

Read any confirmation before continuing. Do not click again while a task is running. Afterwards, check the VM state, console and application. A success message does not prove that the application is healthy.

## Snapshot, clone, copy or backup? {#protection-types}

| Option | What it gives you, and its limit |
| --- | --- |
| Snapshot | The VM at one point in time, stored with its disks. Not an independent backup |
| Fast clone | Another VM that shares storage with the original. No protection if that storage is lost |
| Full copy | Another VM with copied disks on an SR you choose. Check its data, location and isolation before use |
| Backup | A separate recovery copy. Prove it with an isolated restore |

Snapshots and clones use more storage as the VMs change. Check the SR's free space, and delete only test objects that you have clearly identified. A snapshot of a running VM is not guaranteed to be consistent for its applications.

## Take a snapshot of a stopped VM <span class="hx:absolute" id="3-take-and-check-a-stopped-snapshot"></span> {#stopped-snapshot}

Use a test VM with ordinary disks (no shared disks or passthrough devices) and a working console. Pause its backup and replication schedules, and wait for running tasks to finish. Keep an independent recovery copy of any data you need. Snapshots of running VMs, memory snapshots and application consistency are not covered here.

1. In the guest, create a harmless file containing `snapshot-A` and note its checksum. Shut the guest down cleanly and check that the VM is **Halted**.
2. Note the VM UUID, each disk (VDI) with its ID, SR and size, any existing snapshot UUIDs, and the SR's free space. Then [remove every network interface (VIF) from the test VM](/docs/xoa-hl/storage-networks/) and check that the list is empty. From now on, use the console.
3. Check each disk name. A disk whose name contains `[NOSNAP]` can be left out of snapshots; this is part of the disk name, not a VM tag. Disks left out, shared disks and passthrough devices need another procedure. Do not rename disks to get around an existing policy. Plan space for the snapshot, for later writes, and for the extra snapshot taken before a revert.
4. Open **Snapshots** (`/#/vms/<id>/snapshots`) and select **New snapshot** once. This creates the snapshot straight away, without asking for a name. The default name is the VM name plus a timestamp. Do not use **New snapshot with memory**.
5. Wait and refresh. Find the new row by its **Creation date**, and copy its UUID with the row's copy button. Note that UUID: a name or a time is not enough.
6. Set the **Name** to `lab-snapshot-A` and the **Description** to a short test note. Refresh and check both values. Compare the snapshot's disks and SRs with your notes, and check for errors and free space. The snapshot's disk IDs are new, so compare which disks are covered and their sizes, not their IDs.

**Check:** one identified snapshot covers the intended disks, and the original VM is stopped with no VIF.

If creating or renaming fails, save the error and the actual VM, snapshot and disk lists before you retry. A missing ID or notification does not prove that nothing was created, and a failed rename does not undo the snapshot.

## Revert to a snapshot <span class="hx:absolute" id="4-revert-only-the-test-vm"></span> {#snapshot-revert}

In D3, a snapshot was taken while the test VM was **Halted**. A disk added afterwards was gone after revert. The VM stayed **Halted**, and the snapshot remained. This does not establish guest file or application consistency.

{{< callout type="warning" >}}
Reverting replaces the VM's current state, including settings that can bring back old network interfaces. Changes made after the snapshot can be lost. Only revert this isolated test VM, keep it stopped while you revert, and check its VIFs again before you start it. A snapshot on the same SR does not protect you if that SR is lost.
{{< /callout >}}

1. Start the isolated test VM, change the file content to `snapshot-B`, and note the new checksum. Shut it down cleanly and check that it is **Halted**. Note the current disks, VIFs and snapshots.
2. Check by its UUID that the snapshot you are about to use is `lab-snapshot-A` from the previous section. It must not be a snapshot made by a backup job, or another VM's snapshot.
3. In **Snapshots**, select **Revert VM to this snapshot** on that row, and read the **Revert your VM** confirmation. Leave **Snapshot before** ticked, and check free space first. This option, ticked by default, saves the current state as a separate snapshot before the revert. It is not an independent backup, and it does not guarantee a rollback. Cancel if the VM, its isolation or the free space is in doubt.
4. Confirm once and wait. Refresh, and note the reverted snapshot's UUID, the UUID of the new "before" snapshot, the power state, the disks, the VIFs and any error. If the "before" snapshot fails, XO does not request the revert. If the revert fails later, the "before" snapshot can remain. Check the actual state before any retry, and do not untick **Snapshot before** to get past an unexplained error.
5. Before you start the VM, check that it is **Halted** and that its VIF list is empty. If a VIF came back, remove it while the VM is stopped. A snapshot taken while the VM was running can make the VM start or resume by itself after a revert; such snapshots are not covered here.
6. Start the VM and open the console. Check that the file says `snapshot-A` with the original checksum, and that the disks and application work. Shut the VM down and note the result. The extra "before" snapshot holds the `snapshot-B` state. Getting that state back is a separate, controlled restore, not an undo button.

### Delete a test snapshot {#snapshot-cleanup}

Once you have noted the result, and kept any independent recovery copy you need, keep the VM stopped. Delete only a test snapshot whose UUID and owner you noted.

1. In **Snapshots**, select **Remove this snapshot** on that row. Read the **Delete snapshot** confirmation, and confirm one snapshot only. Do not use **Remove selected snapshots**, do not delete a snapshot made by a backup job, and do not confuse this with the VM's **Remove** action.
2. Wait, then refresh the snapshots, the VM's disks and the SR's free space. Check that the snapshot is gone, that the snapshots you keep and the VM are still there, and that there is no error.

Disk cleanup can log errors without failing the whole deletion. A disappearing row or a success message does not prove that cleanup finished or that space was freed at once. Note any remaining IDs and [report unexplained leftovers](/docs/xoa-hl/troubleshooting/). Never bulk-delete disks that look orphaned. A deleted snapshot cannot be recovered.

## Make an isolated fast clone {#fast-clone}

In D3, the stopped VM produced a fast clone with its own identity, one disk and one inherited NIC. The clone started after that NIC was removed. No running clone or full copy result is recorded in this run.

1. On a stopped test VM, select **Fast clone**. Find the new VM (its default name ends in `_clone`), note its ID and rename it.
2. Keep the clone stopped while you [remove every inherited network interface](/docs/xoa-hl/storage-networks/), or arrange a checked isolation outside XO. A new MAC address does not change the copied IP addresses, credentials or application identities.
3. Start the clone and check its console. Reconnect a network only after you have resolved the duplicated identities and checked the isolation.

If no clone appears after an error, check the inventory and the tasks before you retry. This does not test live migration, memory snapshots or recovery after an SR is lost.

### Make a full copy in the same pool {#full-copy}

Use **Copy**, not the separate **Fast clone** action, when you want ordinary disk copies on an SR you choose. The Copy dialog also offers **Fast clone**; keep **Full copy** selected here. Neither a fast clone nor a full copy in the same pool is an independent backup or a tested disaster recovery.

1. Use one test VM with ordinary disks, without shared disks or passthrough devices. In the guest, note a harmless file and its checksum. Shut the guest down cleanly and check that it is **Halted**. Note the VM ID, each disk's ID, SR and size, the VIFs and any snapshots. Snapshot history is not part of this test.
2. Find a different writable **VM-disk SR in the same pool**. Check its ID, its free space, and that the host that will run the copy can reach it. An ISO library cannot be used. Plan space for the copies and their growth: the dialog does not reserve or check space. If the target SR is not available, fix storage access before you start.
3. On the source VM, select **Copy**. In **Copy VM**, set **Name** to a unique test name such as `lab-vm-full-copy`. The default is `{name}_COPY`, and an empty field keeps the original name. Check that **Full copy** is selected.
4. In **Select SR**, pick the SR by the ID and pool you noted, not by a similar name. Other pools can appear in the list; choosing one switches to an export and import, which this test does not cover. Leave **Compression** at **Disabled**: within one pool, the copy is not compressed.
5. Confirm once and wait for the task. Refresh, and find the new VM by its own ID and the name you chose. Check that it is **Halted**, and check its number of disks, their sizes, their new IDs and the SR of each disk. Check that the source VM and its disks are unchanged. If the new VM is running, or anything differs, stop and restore isolation before you go on.
6. Keep the new VM stopped while you [remove every inherited VIF](/docs/xoa-hl/storage-networks/), and check that the list is empty before the first start. Do not rely on new MAC addresses: the guest's IP addresses, credentials and application identities are copied.
7. Start only the isolated copy, open its console, and check the file checksum, the disks and the application. Resolve duplicate identities before you connect any network, and keep the original isolated or stopped while you check.
8. Shut the copy down. Note the result, then use [Delete a test VM](#delete-vm) to remove only the copy and its disks. Keep the source and any independent backup.

If an error, a lost connection or an interrupted request occurs, save the task, the error and the VM, disk and snapshot lists on both sides before you retry. An incomplete copy is not rolled back automatically, and a missing VM ID does not prove that nothing was created. Check space and host access to the SR, match the exact IDs, and [report unexplained leftovers](/docs/xoa-hl/troubleshooting/). Never retry blindly or bulk-delete disks that look orphaned.

Not covered here: copies of running or suspended VMs, copies to another pool, template copies, shared or passthrough disks, snapshot history and recovery after an SR is lost.

## Change CPU and memory {#resize-vm}

Host limits are checked when the VM starts, not when the value is saved. On the one D3 host, saving 64 vCPUs and 1 TiB of memory on a stopped VM succeeded. Starting it then failed with "no hosts available", and it stayed **Halted**. Always start the VM after an edit. If it will not start, save the error and restore the old values and limits before trying again. The page can show old values for a few seconds after saving; wait and reload to confirm. In D3, the inventory refreshed after about four seconds.

Plan a maintenance window and use a test guest whose console you can open. Before you change anything, note the VM ID, the guest state and the current CPU and memory values and limits. Check the host and pool capacity and the guest's needs; this guide does not recommend a CPU count or memory size.

{{< callout type="warning" >}}
Shut the guest down cleanly and check that it is **Halted** first. If you edit a running VM and a value cannot change live, XO can offer a restart or a forced restart. Cancel it here and shut down first. Raising a limit does not reserve resources on the host, and lowering the memory can stop the guest from starting.
{{< /callout >}}

1. Open **Advanced** (`/#/vms/<id>/advanced`) and note **CPU limits** and **Memory limits (min/max)**. The CPU row shows the current and maximum values. You can edit the maximum while the VM is stopped. To use more CPUs than the current maximum, raise the maximum first.
2. Open **General** (`/#/vms/<id>/general`). Click the CPU count, type the new whole number and press **Enter**. Wait, refresh and check the value before the next change. These fields can also save when you click elsewhere, so clicking away is not a safe way to cancel.
3. Click the memory value, set the new amount and unit, and press **Enter**. This value is the configured **dynamic maximum**, not the memory that the guest is using. Depending on the existing limits, XO updates a fixed memory setting or the dynamic memory limits.
4. Refresh **General** and **Advanced**, and note all the resulting values. The CPU count must not exceed its maximum. Memory limits must stay in order: static minimum ≤ dynamic minimum ≤ dynamic maximum ≤ static maximum. XO can adjust related limits, so do not assume that only the field you clicked changed.
5. Start the test VM, and check its console, the CPU and memory seen inside the guest, and the application. If it does not start, or the values are wrong, keep it stopped, save the task error, and put back the noted settings in the same window. Check every limit again, and retry only once you know the cause.

If an edit shows an error, check the actual values before you retry. Related changes are not applied as one all-or-nothing step, and a refused edit does not prove that the old values are back. Keep [troubleshooting](/docs/xoa-hl/troubleshooting/) and your notes at hand.

Not covered here: changing resources while running (hot-plug), dynamic memory under load and CPU topology tuning.

## Delete a test VM {#delete-vm}

In D3, removing one halted test VM removed that VM, its snapshot and its disk, with no leftover objects. Separately, detaching a blank disk left it on the chosen SR; deleting that disk removed it. Detach and delete have different results. Shared disks, protected VMs and cleanup failures were not tested.

{{< callout type="warning" >}}
**Remove** deletes the VM. It is not the same as disconnecting or detaching a disk. In this version, the confirmation has no option to keep the disks: deletion also removes the VM's snapshots and tries to delete its attached disks. If any data or snapshot must be kept, stop before you confirm and plan how to keep it. A snapshot of this VM is not an independent recovery copy.
{{< /callout >}}

1. Check that the target is the test VM, not the appliance, the original guest, a template, or another VM with a similar name. Note its ID, its attached disks with their IDs and SRs, and its snapshots.
2. Check its backup and replication schedules, and whether another VM uses one of its disks. For valuable data, first make an independent [backup and test an isolated restore](/docs/xoa-hl/backup-restore/).
3. Shut the guest down normally and check that it is **Halted**. Deletion can hard-stop a VM that is still running or suspended, so never use **Remove** as a shutdown.
4. Open **Advanced** and select **Remove**. Read the warning about the VM and its disks, and confirm only this VM. If XO then offers to remove a protected or blocked VM anyway, cancel and find out why it is protected. Do not approve a forced retry.
5. Wait, then refresh the VM, snapshot and SR disk lists. Check the IDs you noted, and the task and its errors. Shared disks still attached to another VM are skipped, but that does not protect every disk. Snapshot or disk cleanup errors can be logged without failing the whole deletion, so a disappearing VM or a success message does not prove that cleanup finished.
6. Check that the original VM, the other guests and any independent backup still work. Check any remaining test objects one by one, with your notes and the [disk guide](/docs/xoa-hl/storage-networks/). Never bulk-delete disks that look orphaned, or retry a forced operation to free space. There is no undo: deleted guest data can only come back from a separately tested recovery copy.

If deletion fails partway, or you cancel a blocked deletion, save the remaining VM, disk and snapshot lists and the error. If the VM still exists, also check its permissions, IP pool reservations and resource set membership: XO starts some of this bookkeeping before it checks the VM's protection, so a refusal does not prove that those records are unchanged. Do not create a VM with a similar name and assume that it is the same object. [Report the problem](/docs/xoa-hl/troubleshooting/) with versions and IDs (without private data) before any further cleanup.

{{< details title="Sources" closed="true" >}}
- **Console**: [tab/controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-console.js), [canvas capture/scaling/reconnect](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/react-novnc.js), [authenticated operate gate](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [host console proxy](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **Full copy**: [Copy dialog/defaults/name pattern](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/copy-vms-modal/index.js), [copy/clone requests](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM/SR permissions and pool branch](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [XAPI copy/clone/remote-copy wrapper](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [writable-SR selector](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Power and snapshots**: [power and snapshot actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM action bar](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [snapshot tab](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [revert confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js), [revert power behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **CPU, memory and deletion**: [General controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [Advanced limits/Remove](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [inline save behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [VM API permissions/restart/delete parameters](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [constraint ordering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [destroy defaults/shared disks/cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [UI labels and warnings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Snapshot coverage and deletion**: [disk-name matching and disk cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs).
{{< /details >}}
