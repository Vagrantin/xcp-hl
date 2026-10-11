---
title: Back up a VM and test an isolated restore
description: Save a full VM backup on separate storage, restore a stopped copy and verify its data safely.
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: source
sourceRevision: sha256:95197e62eaca75f0861baa879c3c3325ab86b29442dbce0e742f847b6ea3f706
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protect your test VM with a full backup on separate storage, then restore a copy and check that its data is usable. A successful backup job is the beginning of this check; the restore completes it.

{{< callout type="info" >}}
Preview procedure: source-reviewed for XO 5.113.2 (`e281c536`), XOA-HL package `v5.113.2_e281c536-ce38` and image `xoa-image-20261009-5f33c81`. A disposable-lab run is still pending. This tutorial covers full VM backup to NFS only; other remotes and backup modes need their own validation.
{{< /callout >}}

## Before you begin

- [Create and install a test VM](/docs/xoa-hl/create-vm/). Use an XOA-HL administrator account; the backup area at this pin requires administrator access.
- Arrange an NFS export on a separate backup system, outside the storage holding the original VM and appliance. The appliance must be able to reach it and create, read and delete backup files. Ask the storage administrator for the server, export path and required mount options.
- Check free space on the backup target, the original VM's SR for temporary snapshots, and the writable SR that will receive the restored disks. Allow room for the configured retention and another backup run; compressed size is not guaranteed.
- Prepare a small harmless file inside the guest, record its contents or checksum, and finish writing it before backup. For this first test, shut down the guest normally and check that it is stopped. This avoids assuming that a live backup is application-consistent.
- Reserve capacity for a second VM. Plan to keep the restored copy stopped until **every virtual NIC is removed**. This console-only test needs no guest network.

Management steps run in the **browser**. Creating and checking the sample file runs in the **guest VM**. No host or appliance shell command is required.

## 1. Add the backup destination

1. Open **Settings → Remotes** (`/#/settings/remotes`). Reuse an existing suitable remote if it has been verified; otherwise create one named `lab-backup-nfs`.
2. Choose **NFS**, enter the backup server and export path supplied by its administrator, and apply any required mount options. Keep advanced fields at their defaults unless your storage setup requires a change. Do not select a local directory inside the appliance for this test.
3. Save the remote, enable it if necessary, and use its **Test your remote** action. Read any connection or test error before continuing.

**Check:** the remote is enabled, its test succeeds and no connection error is shown. This tests access; it does not prove that a VM backup can be restored.

## 2. Create one full backup job

1. Open **Backup → New → VMs** (`/#/backup/new/vms`) and name the job `lab-first-vm-full`.
2. Select only your test VM explicitly. Leave smart selection off so the job cannot pick up unrelated VMs.
3. In the backup modes, select **Backup**. Leave **Rolling snapshot**, **Delta backup**, **Disaster recovery** and **Continuous replication** off. In this UI, **Backup** is the full export mode.
4. Select `lab-backup-nfs` under **Target remotes (for export)**. Leave **Delete old backups first** off; this option can remove previous copies before the new export succeeds.
5. Add a schedule explicitly. Set **Backup retention** to `2` for this small lab example, choose an explicit timezone such as `Asia/Tokyo`, and review the scheduler's next-run preview. Retention is a count of retained backups for that schedule, not a number of days.
6. Disable that schedule in the schedule table before saving the job. This pilot runs manually; no default automatic schedule should be left behind.
7. Save and check the overview: one intended VM, the intended remote and a disabled schedule. Keep advanced backup settings unchanged for this first test.

{{< callout type="warning" >}}
Retention can delete older backups on subsequent runs. Use a dedicated lab destination and never lower a production job's retention to follow this example. A snapshot kept on the original SR is not an independent backup.
{{< /callout >}}

## 3. Run and inspect the backup

1. In **Backup → Overview** (`/#/backup/overview`), use the run action for the job's disabled schedule. Check the confirmation identifies your job and only one VM, then confirm.
2. Wait for the run to finish. Open its logs and inspect the VM/export result, not just the fact that the job started. Investigate warnings, failures or skipped data.
3. Open **Backup → Restore** (`/#/backup/restore`). Locate the test VM and confirm that the new full backup is listed with the expected timestamp and remote. Refresh the list if necessary.

**Check:** the run succeeded and its new restore point is visible. Record the job, schedule, remote, backup timestamp and installed versions. You can start the original guest normally again; leave its backup schedule disabled during the restore test.

## 4. Restore a stopped copy

1. In **Backup → Restore**, choose the restore action for your test VM, then select the exact full backup you just made.
2. Choose the writable destination SR with enough free space. This is VM-disk storage, not the NFS backup remote or an ISO SR.
3. Leave **Start VM after restore** **off**. Select **Generate new MAC addresses** to give the copy distinct virtual NIC addresses. New MAC addresses do not change a static IP, hostname or application identity inside the guest.
4. Confirm the restore and wait for completion. Check the restore logs for errors. Identify the new VM by its UUID and restored disks; do not identify it by its name alone.
5. Verify the restored VM is stopped. Rename this copy `lab-first-vm-restore-test` and record its UUID alongside the original VM's different UUID.

**Check:** a separate stopped VM exists with the expected disks. Do not start it yet. If it is unexpectedly running, stop the copy and investigate its network exposure before continuing.

## 5. Isolate, boot and verify the copy

1. Open the **restored copy's Network** tab (`/#/vms/<restored-uuid>/network`). While it is stopped, remove **all** its virtual NICs and confirm the table is empty. A disconnected runtime status alone does not guarantee isolation after a later boot.
2. Recheck the restored UUID and empty NIC table, then start this copy and open **Console**. Leave the original VM's networking untouched.
3. Verify the guest boots, console login works, and the sample file has the recorded contents or checksum. Check any other data needed for your recovery goal. Boot success alone is not a complete application-recovery test.
4. Shut down the restored guest normally. Record the result, backup timestamp, restore duration and versions. When finished, delete only the test copy and its restored disks after checking its UUID; keep the original VM and backup intact.

**Check:** the restored data matches the saved sample and the test VM had no NICs when booted. If the test fails, keep the backup, stop the copy and inspect the logs before retrying.

## If something does not work

| Symptom | Check and next action |
| --- | --- |
| NFS test fails | Check appliance-to-server connectivity, export path, export permissions and required mount options. Browser access to the NAS is not enough. |
| Backup fails or has no restore point | Read the per-VM/export logs; check remote access and capacity, original SR free space, and the selected VM. A retained snapshot alone does not meet this tutorial's goal. |
| Restore point is absent | Verify the remote is enabled without errors, refresh the list and check the job actually exported this VM. |
| Restore fails | Inspect its logs, remote readability, destination SR capacity and host access to that SR. Check for a partial VM before retrying; never delete by name alone. |
| Restored VM has no network | Expected here: all NICs were removed for the console-only test. Attaching a production network requires a separate review of guest IP and service identities. |
| File differs or guest does not boot | Verify the selected restore point and that the file was written before backup. Retain logs and the backup; do not count the test as passed. |

## Next step and sources

After a successful restore test, decide your real backup frequency, retention, capacity monitoring and application-consistency method. Enable a schedule only after reviewing its timezone and next runs. Follow the [update guide](/docs/guides/updates/) and [glossary](/docs/xoa-hl/glossary/). Configuration recovery, replication, incremental backup and file-level restore are separate procedures.

Source review at XO@e281c536: [backup routes and administrator access](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [remote form](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [remote test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [job modes and save](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [schedule and retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [manual run](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [restore controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [NIC removal](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js). XOA-HL applicability: [upstream pin](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [patch/build selection](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
