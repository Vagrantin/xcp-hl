---
title: Operate a VM and manage snapshots
description: Start and stop a test VM, take a snapshot and prepare an isolated clone.
weight: 21
translationKey: xoa-manual-vm-operations
translationStatus: source
sourceRevision: sha256:2ba0c0496c68e8303779ca864433625d5588c48ef4cdecb71930103c61012066
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Use a disposable VM with no production data for this first practice. Sign in to the **XOA-HL appliance** as an administrator and confirm the VM, host and storage are available. Keep an independent [backup and restore test](/docs/xoa-hl/backup-restore/) before changing a valuable VM.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. VM power, snapshot/revert and clone tests on this appliance are pending. Later releases can differ.
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

## Sources

XO 5 pin `e281c536`: [power and snapshot actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM action bar](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [snapshot tab](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [revert confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js) and [revert power behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
