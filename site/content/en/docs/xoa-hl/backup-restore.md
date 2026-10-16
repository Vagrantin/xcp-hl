---
title: Back up a VM — schedules, retention and isolated restore
description: Rehearse full and incremental NFS backups, schedules, chain retention and isolated restore.
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: source
sourceRevision: sha256:82d11f2863d7171371a83029e1807784437f2c002b17d21f5b5d2da0fefd6021
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protect your test VM with a full backup on separate storage, then restore a copy and check that its data is usable. A successful backup job is the beginning of this check; the restore completes it.

{{< callout type="info" >}}
Preview procedure: source-reviewed for XO 5.113.2 (`e281c536`), XOA-HL package `v5.113.2_e281c536-ce38` and image `xoa-image-20261009-5f33c81`. A disposable-lab run is still pending. Sections 1–6 cover full VM backup to NFS; section 7 is a separate incremental-backup pilot. Other remotes and modes need their own validation.
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

At this ce38 source pin, the French remote-test success/failure headings are reversed in the inherited catalog ([tracked fix](https://github.com/Vagrantin/xoa-hl/issues/38)). Check the success/error icon and the detailed error/step results, rather than accepting the heading alone. An actual backup and isolated restore remain required; no installed correction is claimed here.

## 2. Create one full backup job

1. Open **Backup → New → VMs** (`/#/backup/new/vms`) and name the job `lab-first-vm-full`.
2. Select only your test VM explicitly. Leave smart selection off so the job cannot pick up unrelated VMs.
3. In the backup modes, select **Backup**. Leave **Rolling snapshot**, **Delta backup**, **Disaster recovery** and **Continuous replication** off. In this UI, **Backup** is the full export mode.
4. Select `lab-backup-nfs` under **Target remotes (for export)**. Leave **Delete first** off; this option can remove previous copies before the new export succeeds.
5. Add a schedule explicitly. Set **Backup retention** to `2` for this small lab example, choose an explicit timezone such as `Asia/Tokyo`, and review the scheduler's next-run preview. Retention is a count of retained backups for that schedule, not a number of days.
6. Disable that schedule in the schedule table before saving the job. This first backup/restore check runs manually; keep the schedule disabled until the supervised exercise in section 6.
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

## 6. Rehearse backup schedules and retention {#backup-schedules}

Complete the manual backup and isolated restore above before enabling automation. Use only that dedicated full-NFS lab job, one explicitly selected disposable VM and its one disabled schedule. Keep the source guest cleanly stopped for all runs in this exercise; live/application consistency needs separate acceptance. Verify capacity and remote access again, and preserve any recovery copy that must survive **outside this job's retention policy**.

1. In **Backup → Overview**, record the job ID and copy the exact schedule ID using its clipboard button. Open the job's edit action. In **Schedules**, edit the existing disabled row rather than deleting and recreating it. Give it a clear test name, keep **Backup retention** at `2`, and leave **Delete first**, long-term retention and automatic restore health checks off. Verify that only full **Backup**, the intended VM and `lab-backup-nfs` remain selected.
2. Choose a laboratory rule with the visual time selector and an explicit **Timezone**, such as `Asia/Tokyo`. Allow more time between occurrences than the observed manual backup duration, including room to investigate failures. Review at least three upcoming occurrences within the supervised test window and record the generated **Cron pattern**. No universal production interval is prescribed here.
3. Record the browser's timezone as well. The rule uses its selected timezone, while the preview formats the resulting dates in the browser's display timezone. A differing clock label is not necessarily a differing trigger instant. Compare the expected instants and appliance clock before enabling; the preview predicts dates and does not prove a backup will execute.
4. Keep the row **Disabled** in the editor and choose **Save** for the job. Reopen it and read back the schedule ID, rule, timezone, retention, VM and remote. Editor changes are saved in separate schedule/job requests, so an error can leave a partial change. Do not enable until these records agree.
5. Return to **Overview** and enable only this schedule with its state button. This button sends the change immediately; there is no separate Save. Refresh and verify **Enabled** on the recorded row. Observe the next trigger without pressing the manual run button. Open that schedule's run details and check its job/schedule IDs, actual start/end times, selected VM and export result; verify a new point in **Restore** on the intended remote.
6. Repeat the observations until at least three successful runs of this same schedule have completed. Compare restore-point timestamps after each run. With retention `2`, long-term retention off and successful cleanup, the expected result is the two newest eligible full backups for this VM/schedule on that remote. Verify that result rather than assuming a strict file count or treating skipped/failed runs as verified recovery points. For **Delete first** off, this source writes the new export/metadata before pruning the selected older backups; cleanup can still fail and needs its own log/inventory check.
7. Disable the exact schedule in **Overview** and refresh to confirm **Disabled** before another expected occurrence. Disabling stops future triggers; it does not cancel an already running job. The Overview cancellation control is disabled at this pin. Let an active lab run finish and inspect its outcome, then check that the next planned trigger produces no new run. Leave the rule disabled at the end.
8. Select a retained point from a scheduled run and repeat sections 4–5: restore stopped, remove every inherited NIC before first boot, compare the sample checksum and shut down the copy. Use the [disposable VM removal procedure](/docs/xoa-hl/vm-operations/) for identified copy cleanup. Record the final schedule state, surviving points and restore result.

A new export can exist even if later cleanup makes the run fail. Inspect the actual restore-point/file inventory before retrying, and prove an isolated restore before counting it as usable.

Retention is scoped by VM, full-backup mode and **schedule ID on each remote**, not by the visible name or a global number of days/files. Another schedule can retain other points. Deleting and recreating a same-named rule changes its identity; do not use that as a cleanup shortcut or assume its old backups join the new policy. This pilot does not test long-term retention buckets or delta chains.

If a trigger is absent, a save/toggle fails, or a run reports failure, preserve the job/schedule/remote IDs, expected and actual times, error and backup inventory. Treat automatic execution as possible until its state is established. Check server availability/clock, enabled state, VM selection, remote access and capacity before retrying. A tick for a job already running can be rejected; do not assume queued overlaps, retry or catch-up after appliance downtime. Disabling, changing a rule or deleting a job is not an active-run cancellation procedure. After resolving an incident, run once manually only when no run is active, verify its restore point and repeat an isolated restore before resuming an agreed schedule. Email/alert delivery, daylight-saving transitions, outage recovery and production retention need their own acceptance.

## 7. Rehearse incremental backups and chain recovery {#delta-backups}

Use this separate **NFS delta-backup pilot** after the full backup and isolated restore above succeed. Keep that independent full backup on its existing destination. A full-mode XVA export is not the initial parent of this new delta job. Delta restore points need their metadata and the required VHD parent chain; one copied VHD is not a complete VM backup.

Use a disposable VM with ordinary virtual disks, no shared/passthrough disks and no memory/checkpoint backup. Record VM/VDI UUIDs, sizes and the guest sample's path/checksum. Keep the same disk set throughout. Obtain an empty dedicated NFS export and a new remote, such as `lab-delta-nfs`, approved by the storage owner. Reserve source snapshot space, remote space for a full export plus later writes/merges, and destination SR space for isolated restores. This is not a production retention policy.

Management runs in the **XOA-HL browser** with an administrator account; sample changes and checksum checks run in the **guest console**. Record the installed release/UI and effective feature availability. If **Delta Backup** or its controls are unavailable, stop and report the actual build/plan state; do not change licensing or substitute XO 6 instructions. Source visibility does not establish installed support.

### Create a separate, disabled job

1. Add and test the dedicated remote as in section 1. Open **Backup → New → VMs** (`/#/backup/new/vms`), name the job `lab-delta-chain`, explicitly select only the disposable VM and leave smart selection off.
2. Select **Delta Backup** only. Leave **Backup**, **Rolling Snapshot**, **Disaster Recovery** and **Continuous Replication** off. Select only `lab-delta-nfs`; leave **Delete first** off. Do not convert or edit the earlier full-backup job.
3. In **Advanced settings**, set **Full backup interval** to `2`. Leave **Use NBD to transfer disk if available** and **Purge snapshot data when using CBT.** off for this pilot. Turn **Merge backups synchronously** on. Leave offline/memory backup, automatic health checks and other advanced options unused. Do not manually remove snapshots retained by this job.
4. Add one schedule with **Backup retention** `2`, an explicit timezone and a reviewed next-run preview. Leave **Force full backup** off: that schedule option overrides the interval with a full backup every run. Leave long-term retention off. Disable the schedule before saving. Save, reopen the editor and verify the VM, remote, interval, options and disabled schedule; record job, schedule and remote IDs. Keep it disabled throughout this manual exercise.

The interval, NBD, CBT-purge, synchronous-merge, Force and differential-restore labels fall back to English in the pinned FR/JA catalogs. The interval is a chain-length setting, not days or the number of restore points to retain. For this fresh single-disk-set fixture, interval `2` is expected to produce a full key export, an incremental export, then another full key export. Missing bases, changed disks or errors can alter that result; verify it in the logs.

### Make three distinguishable points

For each run, finish writing the harmless sample and shut down the original guest normally. Use the job's ordinary manual run action only when no previous backup or merge is active. This pilot does not enable the job's offline-backup mode or force a guest shutdown. Record each run ID, timestamp, VM/schedule/remote, export **Type**, warnings and resulting restore-point identity. Inspect all task statuses/pages and preserve the raw JSON if necessary. A delta job's points can still display **incremental** in the restore selector when the export was full; do not infer the export type from that mode label or file size.

| Run | Guest sample before normal shutdown | Expected observation |
| --- | --- | --- |
| 1 | Version A and checksum A | Full key export for the new job; listed point A |
| 2 | Boot original, write version B, record checksum B, shut down | Incremental export using a usable base; listed point B; perform the isolated restore below before run 3 |
| 3 | Boot original, write version C, record checksum C, shut down | Full key export at interval `2`; inspect cleanup/merge results and retained points B/C, then repeat restores below |

If run 2 reports full or warns about falling back to full, retain the evidence and investigate base snapshots/remote parents, unchanged disks and saved interval/Force settings. Do not count that run as a demonstrated incremental transfer, and do not delete a base to force a test.

Retention selects eligible delta points for this VM/schedule on this remote; merge limits or cleanup failures can leave extra points. With **Delete first** off, old-point deletion follows transfer/chaining, but pre-run cleanup can still merge/remove data and repair metadata. Synchronous merging does not make the operation transactional or prove recovery. Never delete, rename, move or edit individual backup JSON/VHD files, or use snapshot deletion to tidy the chain.

### Restore the incremental point before and after retention

1. In **Backup → Restore** (`/#/backup/restore`), select the exact point B on `lab-delta-nfs`. Choose a writable destination SR with enough capacity. Include **every expected disk**; the delta dialog permits disks to be ignored, so check each disk's destination and do not accept an omitted disk.
2. Leave **Start VM after restore** and **Use differential restore** off. Enable **Generate new MAC addresses**. Differential restore can reuse source-side snapshots and is a different recovery test; it is not required to restore the backup's chain from the remote.
3. Complete sections 4–5's isolation checks: record the new VM/disk UUIDs, confirm the copy is stopped, remove **every** inherited NIC before boot, and compare the restored sample to checksum B through its console. Stop the copy normally and keep the original VM and backup intact. Identify each test copy independently; use the [VM removal procedure](/docs/xoa-hl/vm-operations/) for approved cleanup.
4. After run 3 and completed cleanup/merge inspection, restore the retained point B again to a new stopped isolated copy and verify checksum B. Separately restore point C and verify checksum C. Record the remaining point inventory and results. This checks the older incremental point after retention, not just the latest key export. Leave the schedule disabled.

On missing parents, transfer/merge errors or failed restore, preserve run JSON, point identities and partial VM/disk inventory. Stop further manual runs; a retry can change retention and chain state. Resolve access/capacity/ownership with the backup owner, then repeat the controlled test without changing unidentified chain files. Do not restart services or invoke force/repair controls as a generic remedy. If recovery cannot be established, retain the independent full backup and keep the incident open. Installed failure/recovery, live-guest consistency, NBD/CBT, encrypted/other remotes, differential restore and file-level recovery remain separate acceptance work.

## If something does not work

| Symptom | Check and next action |
| --- | --- |
| NFS test fails | Check appliance-to-server connectivity, export path, export permissions and required mount options. Browser access to the NAS is not enough. |
| Backup fails or has no restore point | Read the per-VM/export logs; check remote access and capacity, original SR free space, and the selected VM. A retained snapshot alone does not meet this tutorial's goal. |
| Restore point is absent | Verify the remote is enabled without errors, refresh the list and check the job actually exported this VM. |
| Restore fails | Inspect its logs, remote readability, destination SR capacity and host access to that SR. Check for a partial VM before retrying; never delete by name alone. |
| Restored VM has no network | Expected here: all NICs were removed for the console-only test. Attaching a production network requires a separate review of guest IP and service identities. |
| File differs or guest does not boot | Verify the selected restore point and that the file was written before backup. Retain logs and the backup; do not count the test as passed. |

For run statuses, partial exports and a controlled retry, follow [backup failure diagnosis](/docs/xoa-hl/troubleshooting/#backup-failures).

## Next step and sources

Scheduling source at XO `e281c536`: [schedule editor/table/save ordering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [time selector and preview formatting](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [schedule API/start/stop](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [cron job behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [running-job guard/log identity](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs) and [full-backup retention and pruning order](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).

After a successful restore test, decide your real backup frequency, retention, capacity monitoring and application-consistency method. Enable a schedule only after reviewing its timezone and next runs. Follow the [update guide](/docs/guides/updates/) and [glossary](/docs/xoa-hl/glossary/). Configuration recovery, replication and file-level restore are separate procedures.

Source review at XO@e281c536: [backup routes and administrator access](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [remote form](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [remote test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [job modes and save](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [schedule and retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [manual run](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [restore controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [NIC removal](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js). XOA-HL applicability: [upstream pin](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [patch/build selection](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).

Incremental pilot sources (XO `e281c536`): [Incremental export/base selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs), [Remote transfer/retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs), [Snapshot retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs), [Cleanup/merge execution](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs), [Restore chain reader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [Restore implementation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/ImportVmBackup.mjs), [Export type in logs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js).
