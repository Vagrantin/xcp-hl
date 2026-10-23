---
title: "Back up and restore a VM"
linkTitle: "Backup and restore"
description: "Back up a VM, restore a safe copy, then test schedules, incremental backups, file recovery, DR copies and SMB."
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: source
sourceRevision: sha256:b4f67c2357cf7a39bb06c2688686bbcaa192c9d8d8408f8e293955ce27ad06c9
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protect your test VM with a full backup on separate storage. Then restore a copy and check that its data is usable. A successful backup job is only half of the test: the restore completes it.

{{< callout type="info" >}}
**Applies to** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2), image `xoa-image-20261022-a280852`. Based on the released code; not yet tested on a lab system. Other remotes and backup modes need their own tests.
{{< /callout >}}

Sections 1 to 5 are the tutorial: one full backup to NFS and a safe restore. The sections after them are optional tests that build on it: schedules and retention, incremental backups, single-file recovery, a DR copy on another pool, and an SMB remote.

## Before you begin

- [Create and install a test VM](/docs/xoa-hl/create-vm/). Use an XOA-HL administrator account: the backup pages require it in this version.
- Get an NFS export on a separate backup system, not on the storage that holds the VM or the appliance. The appliance must be able to reach it and to create, read and delete files there. Ask the storage administrator for the server, the export path and any required mount options.
- Check free space in three places: the backup destination, the VM's SR (for temporary snapshots) and the writable SR that will receive the restored disks. Leave room for the retention you configure plus one more run. Compressed sizes are not guaranteed.
- In the guest, create a small harmless file and note its content or checksum. Then shut the guest down normally and check that the VM is stopped. A backup of a running VM is not guaranteed to be consistent for its applications.
- Reserve resources for a second VM. The restored copy stays stopped until **all its virtual network interfaces (NICs) are removed**. This test uses only the console, so the copy needs no network.

You manage backups in your **browser**. You create and check the sample file **inside the guest**. You do not need a shell on the host or the appliance.

## 1. Add the backup destination

1. Open **Settings → Remotes** (`/#/settings/remotes`). Reuse a suitable remote that you have already checked, or create one named `lab-backup-nfs`.
2. Choose **NFS** and enter the server and export path from the storage administrator, plus any required mount options. Keep the advanced fields at their defaults unless your storage needs a change. Do not use a local folder inside the appliance.
3. Save the remote, enable it if needed, and run **Test your remote**. Read any connection or test error before you continue.

**Check:** the remote is enabled, its test passes and no connection error appears. This proves access, not that a VM backup can be restored.

## 2. Create a full backup job

1. Open **Backup → New → VMs** (`/#/backup/new/vms`) and name the job `lab-first-vm-full`.
2. Select only your test VM. Leave smart selection off, so that the job cannot pick up other VMs.
3. Under the backup modes, select **Backup**. This is the full export mode. Leave **Rolling snapshot**, **Delta backup**, **Disaster recovery** and **Continuous replication** off.
4. Under **Target remotes (for export)**, select `lab-backup-nfs`. Leave **Delete first** off: it can delete older copies before the new export has succeeded.
5. Add a schedule. Set **Backup retention** to `2`, choose an explicit time zone such as `Asia/Tokyo`, and check the preview of the next runs. Retention is the number of backups kept for this schedule, not a number of days.
6. Disable this schedule in the schedule table before you save the job. You will run this first backup by hand. The schedule stays disabled until [Test backup schedules and retention](#backup-schedules).
7. Save, then check the overview: one VM, the right remote and a disabled schedule. Keep the advanced backup settings unchanged for this first test.

{{< callout type="warning" >}}
Retention can delete older backups on later runs. Use a dedicated lab destination, and never lower a production job's retention to follow this example. A snapshot kept on the VM's own SR is not an independent backup.
{{< /callout >}}

## 3. Run and check the backup

1. In **Backup → Overview** (`/#/backup/overview`), use the run action on the job's disabled schedule. Check that the confirmation names your job and only one VM, then confirm.
2. Wait for the run to finish. Open its log and check the result of the VM export, not only that the job started. Look into any warning, failure or skipped data.
3. Open **Backup → Restore** (`/#/backup/restore`). Find the test VM and check that the new full backup is listed with the expected time and remote. Refresh the list if needed.

**Check:** the run succeeded and its restore point is listed. Note the job, schedule, remote, backup time and installed versions. You can start the original guest again. Keep its schedule disabled during the restore test.

## 4. Restore a stopped copy

1. In **Backup → Restore**, choose the restore action for your test VM, then select the full backup you just made.
2. Choose a writable SR with enough free space. This is VM-disk storage, not the NFS remote and not an ISO SR.
3. Leave **Start VM after restore** **off**. Turn on **Generate new MAC addresses** so that the copy gets its own network card addresses. New MAC addresses do not change the guest's static IP address, host name or application identity.
4. Confirm the restore and wait for it to finish. Check the restore log for errors. Identify the new VM by its UUID and its restored disks, not by its name.
5. Check that the restored VM is stopped. Rename it `lab-first-vm-restore-test` and note its UUID next to the original VM's UUID.

**Check:** a separate, stopped VM exists with the expected disks. Do not start it yet. If it is running, stop it and check what network it could reach before you continue.

## 5. Isolate, start and check the copy

1. Open the **restored copy's Network** tab (`/#/vms/<restored-uuid>/network`). While it is stopped, remove **all** its NICs and check that the list is empty. A "disconnected" status is not enough: the NIC could reconnect at the next start.
2. Check the UUID and the empty NIC list again. Then start the copy and open **Console**. Do not touch the original VM's network.
3. Check that the guest starts, that you can sign in on the console, and that the sample file has the expected content or checksum. Check any other data that your recovery needs. A guest that starts is not yet a full application recovery.
4. Shut the restored guest down normally. Note the result, the backup time, how long the restore took and the versions. When you are done, check the UUID and delete only the test copy and its restored disks. Keep the original VM and the backup.

**Check:** the restored data matches the sample, and the copy had no NIC when it started. If the test fails, keep the backup, stop the copy and read the logs before you retry.

## Test backup schedules and retention {#backup-schedules}

This test turns the lab job's schedule on, watches three automatic runs, and turns it off again. Do it only after the manual backup and restore above have worked.

**Before you start**

- Use only the lab job `lab-first-vm-full`, its single disabled schedule and the one test VM.
- Keep the test VM shut down for every run. A running guest needs its own consistency test.
- Check free space and remote access again.
- Keep any recovery copy you need **outside this job**: retention can delete its old backups.

1. In **Backup → Overview**, note the job ID and copy the exact schedule ID with its clipboard button.
2. Edit the job. In **Schedules**, edit the existing disabled row; do not delete and recreate it. Give it a clear test name and keep **Backup retention** at `2`. Leave **Delete first**, long-term retention and automatic restore health checks off. Check that only **Backup** mode, the test VM and `lab-backup-nfs` are selected.
3. Set a test rule with the visual time selector and an explicit **Timezone**, such as `Asia/Tokyo`. Leave more time between runs than one manual backup takes, plus time to look into failures. Check at least three upcoming runs and note the **Cron pattern**.
4. Note your browser's time zone too. The rule runs in the selected time zone, but the preview shows the times in your browser's time zone, so the same moment can show a different clock time. The preview predicts dates; it does not prove that a backup will run.
5. Keep the row **Disabled** and select **Save**. Reopen the job and check the schedule ID, rule, time zone, retention, VM and remote. The job and its schedule are saved separately, so an error can leave a partial change. Do not continue until everything matches.
6. Back in **Overview**, enable only this schedule with its state button. The button applies at once; there is no separate save. Refresh and check that the row shows **Enabled**.
7. Wait for the next run without pressing the manual run button. Open its details and check the job and schedule IDs, the start and end times, the VM and the export result. In **Restore**, check that a new point appears on the right remote.
8. Wait for at least three successful runs of this schedule, and compare the restore point times after each one. With retention `2`, you should end up with the two newest full backups of this VM for this schedule. Check the actual list: do not assume a file count, and do not count skipped or failed runs.
9. Before the next planned run, disable the schedule in **Overview** and refresh to check **Disabled**. This stops future runs but does not cancel a running backup (the cancel button is disabled in this version). Let a running backup finish, then check that the next planned time starts nothing.
10. Restore one point from a scheduled run with sections 4 and 5: a stopped copy, every NIC removed before the first start, the checksum compared, the copy shut down. Remove the copy with the [VM removal procedure](/docs/xoa-hl/vm-operations/). Note the final schedule state, the remaining points and the restore result.

**Good to know**

- With **Delete first** off, a run writes the new backup before it deletes old ones. If the deletion fails, the run can show as failed even though the new backup exists. Check the actual restore points before you retry, and test a restore before you rely on a point.
- Retention counts backups per VM, per mode and per **schedule ID on each remote**. It does not count days, names or files. Another schedule keeps its own points. A schedule that you delete and recreate gets a new ID, so its old backups do not join the new policy.
- A run that starts while the same job is still running can be refused. Runs missed while the appliance was off are not caught up later.
- Disabling, editing or deleting a job does not cancel a running backup.

**If a run is missing or fails**, save the job, schedule and remote IDs, the expected and actual times, the error and the list of restore points. Until you know the state, assume that an automatic run can still start. Check that the server is up and its clock is right, then the enabled state, VM selection, remote access and free space. Once fixed, run the job by hand once while nothing else runs, check the new point and test a restore before you turn the schedule back on.

Not covered here: email alerts, daylight saving changes, recovery after an outage, long-term retention and production retention policies.

## Use incremental backups {#delta-backups}

An incremental (delta) backup copies only what changed since the previous backup. This test creates a separate delta job, makes three restore points, and checks that an older point still restores after retention has cleaned up. Do it after the full backup and restore above have worked, and keep that full backup.

**Before you start**

- Use a test VM with ordinary virtual disks: no shared or passthrough disks, and no memory backup. Note the VM and disk (VDI) UUIDs, their sizes, and the path and checksum of the sample file. Do not change the disks during the test.
- Ask the storage owner for a new, empty NFS export and add it as a separate remote, for example `lab-delta-nfs`.
- Reserve space for snapshots on the source SR, for one full backup plus later changes on the remote, and for restored copies on a writable SR.
- Use an administrator account. If **Delta Backup** or its settings are missing in your installation, stop and report the version you see. Do not change the licence or follow instructions written for XO 6, which is a different interface.

A delta restore point needs its metadata and its chain of parent disk files (VHD). One VHD file on its own is not a VM backup. The full backup from the tutorial cannot be the parent of this new chain.

### Create the delta job

1. Add and test the remote as in section 1. Open **Backup → New → VMs** (`/#/backup/new/vms`), name the job `lab-delta-chain`, select only the test VM and leave smart selection off.
2. Select **Delta Backup** only. Leave **Backup**, **Rolling Snapshot**, **Disaster Recovery** and **Continuous Replication** off. Select only `lab-delta-nfs` and leave **Delete first** off. Do not edit the earlier full job.
3. In **Advanced settings**, set **Full backup interval** to `2`. Leave **Use NBD to transfer disk if available** and **Purge snapshot data when using CBT.** off. Turn **Merge backups synchronously** on. Leave the other advanced options unused, and never delete the snapshots this job keeps.
4. Add one schedule with **Backup retention** `2`, an explicit time zone and a checked preview. Leave **Force full backup** off: it makes every run a full backup. Leave long-term retention off. Disable the schedule, then save. Reopen the job, check every setting, and note the job, schedule and remote IDs. Keep the schedule disabled for the whole test.

**Full backup interval** sets the length of the chain. With `2`, a new job makes a full backup, then an incremental one, then a full one again. It is not a number of days, and not the number of points kept. Missing parents, changed disks or errors can change this order, so check the logs.

### Make three restore points

Before each run, write the sample in the guest and shut the guest down normally. Start each run by hand, and only when no backup or merge is running. For each run, note the run ID, the time, the export **Type**, any warning and the new restore point. Look at every task status and page, and save the raw JSON if needed.

| Run | In the guest before shutdown | Expected result |
| --- | --- | --- |
| 1 | Write version A and note checksum A | Full export; point A is listed |
| 2 | Start the VM, write version B, note checksum B, shut down | Incremental export; point B is listed. Restore B (below) before run 3 |
| 3 | Start the VM, write version C, note checksum C, shut down | Full export (interval `2`); check the cleanup and that points B and C remain |

The restore list can label a delta job's point **incremental** even when the export was full. Check the export **Type** in the log, not that label or the file size. If run 2 was a full export, keep the evidence, check the parent snapshots, the disks and the interval and **Force** settings, and do not count it as an incremental transfer. Never delete a parent to force the test.

### Restore an incremental point before and after cleanup

1. In **Backup → Restore** (`/#/backup/restore`), select point B on `lab-delta-nfs` and a writable SR with enough space. Include **every disk**: this dialog lets you skip disks, so check each one.
2. Leave **Start VM after restore** and **Use differential restore** off. Turn **Generate new MAC addresses** on. Differential restore reuses source snapshots and is a different test.
3. Isolate and check the copy as in sections 4 and 5: note the new UUIDs, keep it stopped, remove **every** NIC, start it and compare the file with checksum B on the console. Shut it down normally. Remove the copy with the [VM removal procedure](/docs/xoa-hl/vm-operations/).
4. After run 3 and its cleanup, restore point B again to a new isolated copy and check checksum B. Restore point C separately and check checksum C. This proves that the older incremental point still works after retention. Note the remaining points and keep the schedule disabled.

**Good to know**

- Retention picks the points for this VM and schedule on this remote. Merge limits or a failed cleanup can leave extra points.
- With **Delete first** off, old points are deleted after the transfer. The cleanup before a run can still merge or delete data.
- Synchronous merging does not make a run all-or-nothing, and does not prove that recovery works.
- Never delete, rename, move or edit backup JSON or VHD files by hand, and never delete snapshots to tidy a chain.

**If something fails** (a missing parent, a transfer or merge error, a failed restore), save the run JSON, the restore point IDs and the list of any partial VMs and disks. Stop running the job, because each run can change the chain. Fix access, space or ownership with the backup owner, then repeat the test. Do not restart services or use force or repair actions as a generic fix. If you cannot recover, keep the independent full backup and keep the incident open.

Not covered here: running guests, NBD and CBT, encrypted or other remotes, differential restore and real failure recovery.

## Recover one file from a delta backup {#file-restore}

Download one file from a delta restore point to your computer. This test uses point B from the incremental test above, after its VM restore has worked. It does not put the file back into the VM. The full backups from the tutorial do not appear on this page.

**Before you start**

- Use a Linux test VM with one disk and an ordinary, readable partition.
- Before backup B, note the path, content and SHA-256 of a small sample file, for example `/home/lab/recovery-b.txt`.
- Keep point B and its chain on the remote. Make sure your computer has space for the archive.
- Use an administrator account and check that **File Restore** exists in your installation.
- For this first test, avoid production VMs, private data, encrypted or RAID volumes, symbolic links and folders. This test does not prove support for every file system, LVM layout or remote.

1. Open **Backup → File Restore** (`/#/backup/file-restore`). Find the test VM and open its file restore action. Do not click the delete buttons next to it. If the VM or point is missing, refresh and check that `lab-delta-nfs` is enabled. Do not switch to the earlier full backup.
2. Choose **point B** by its time and job, then the disk. Wait for the partition scan, then choose the partition that holds the sample. A disk without a partition table can show its file system directly. If the scan fails, stop: do not mount or edit backup files by hand.
3. Browse from `/` to the sample file and select **only that file**. Do not use the select-folder or select-all controls. Check the path and keep the **tgz** format (the default; **zip** also works but can be slower). Start the download and wait until your browser finishes it. A blocked pop-up or an incomplete download is not a success.
4. On your computer, note the archive's name, size and SHA-256. List its contents, extract only the sample into a new empty folder, and compare its content and SHA-256 with version B. Treat paths inside the archive as untrusted, and never extract over live data. Keep the original VM, point B and the schedule unchanged.

**Check:** the archive opens, it contains only the sample file, and the file matches checksum B. A matching file name, or content from version C, is not a match.

If a step fails, save the evidence and stop further backup runs until the backup owner has looked at it. Do not delete chain files, source snapshots or partial files to make a point appear. Copying the recovered file back into a guest is a separate task that needs the owner's approval.

## Copy a VM to another pool (DR replica) {#dr-replica}

**Disaster Recovery** (DR) copies a whole VM to an SR in another pool. This is different from NFS backup, and from **Continuous Replication** (CR), which sends only changes. The copy, called a replica, stays stopped and is blocked from starting. **Do not unblock or start the replica.** To use it, you clone it. This test checks such a clone in an isolated place. It does not test automatic failover, the loss of the source pool, or moving back (failback).

**Before you start**

- Use a test VM on pool A, and a second test pool B managed by the same XOA-HL appliance.
- Ask the owner of pool B for a dedicated writable SR, `lab-dr-sr`, with room for two full copies and one clone. It must be on different storage from pool A, and it must not be an ISO library. Note the UUIDs of both pools and SRs, the free space and which hosts can reach the SR.
- Keep the independent NFS backup from the tutorial.
- Use a single-disk VM without shared or passthrough disks. Before each run, write a sample (A, then B, then C), note its SHA-256 and shut the guest down normally.
- Plan console access and a place on pool B with **no production network**. You will remove every NIC from the clone before it starts.
- If DR or the target SR is not available in your installation, stop.

1. Open **Backup → New → VMs** (`/#/backup/new/vms`) and create the job `lab-dr-full`. Select only the test VM and leave smart selection off. Select **Disaster Recovery** only; leave **Backup**, **Delta Backup**, **Continuous Replication** and **Rolling Snapshot** off. Under **Target SRs (for replication)**, select only `lab-dr-sr`. Leave **Delete first** off, so that old replicas are not removed before the transfer. Do not edit the other jobs.
2. Add one schedule with **Replication retention** `2`, an explicit time zone and a checked preview. Leave snapshot retention and health checks unused. Disable the schedule and save. Reopen the job and check the VM, target SR, mode, retention, disabled state and IDs.
3. With sample A written and the guest shut down, run the job once from **Backup → Overview**. Check every task and warning. On pool B, find the new **stopped** replica by its UUID, the job and time in its name, its **Disaster Recovery** tag and its disk. Do not start it.
4. Repeat with sample B, then C, one finished run at a time. Note the run and replica IDs, times, disks and errors. After the third run, check which replicas remain: normally B and C. A green job does not prove that the data is right, and a failed deletion is not rolled back.
5. Select the **B replica**, not the source VM, the C replica or an NFS point. Make a **Fast clone** with a unique name on pool B, and leave the replica stopped. Note the clone's new VM and disk IDs, and check that it is stopped and not blocked from starting. If cloning fails or the clone is blocked, stop; do not bypass the block.
6. Remove **every** NIC from the stopped clone and check that its network list is empty. Start only the clone, open its console and compare the sample with checksum B. Shut it down normally. You can test a clone of C in the same way.
7. Keep the B and C replicas and the NFS backup. Remove only the test clones, with the [VM removal procedure](/docs/xoa-hl/vm-operations/).

**Check:** three full runs reached the right pool and SR; B and C remain, or you can explain why not; the isolated clone of B has its own IDs, had no NIC when it started, and holds exactly sample B.

If a transfer, space check, deletion, clone or data check fails, stop further runs and give the inventory to the backup and storage owners. Never remove a replica's start block, delete a point by name alone, or delete a snapshot that the backup job manages.

Not covered here: CR chains, scheduled runs, network cutover, preventing the same VM from running twice, failback and real outages.

## Test a Windows Server SMB backup {#smb-remote}

Test one SMB remote with a full backup and an isolated restore. The XO interface warns that SMB remotes are meant for **Windows Server**, and recommends NFS for Linux Samba and most NAS devices. This test does not cover other SMB servers, SMB storage for ISOs or VM disks, cloud remotes or production use. XO mounts the share with CIFS, and the XOA-HL package includes `cifs-utils`, but mounting has not yet been checked on a real appliance.

**Before you start**

- Ask the Windows Server administrator for a **dedicated test share**, on different storage from the source VM and the appliance, with enough space for the backup and the restore test.
- Ask for a dedicated account that can create, read and delete files in that share, with network access from the appliance only. Get the server name, share name, optional subfolder, domain and credentials through a secure channel.
- Type the password only in its own field. XO builds an internal remote URL that contains the credentials, so treat XO configuration exports as secrets. Never share that URL, and never put credentials in a screenshot, issue, log extract or custom mount option.
- Keep the independent NFS backup from the tutorial. Use the same small, stopped, single-disk test VM with a new sample file and its checksum. Reserve a writable SR and a console-only place for the restored copy.

1. In **Settings → Remotes** (`/#/settings/remotes`), create `lab-backup-smb` with the type **SMB**. In **Address\\Share**, enter the server and the share, separated by a backslash. **Subfolder** is an optional path inside that share, not a second share path. Enter the dedicated username, password and domain (the form starts with `WORKGROUP`; use the administrator's value). Leave **Custom mount options**, proxy and encryption at their defaults. Save, then check the remote's ID, enabled state, type, server, share, subfolder and error indicator. The password stays hidden: do not try to read it from the displayed URL.
2. Run **Test your remote** on this remote. It writes a 10 MiB random file, reads it back, compares it and tries to delete it. Check the success icon, the result and any failed step. If a step failed, ask the administrator to look for a leftover `.test` file by its exact name. A passing test only proves this round trip, not a VM restore or a sustained speed.
3. In **Backup → New → VMs** (`/#/backup/new/vms`), create a separate job named `lab-smb-full`: only the stopped test VM, **Backup** (full) mode only, `lab-backup-smb` as the only target remote, and **Delete first** off. Add one schedule with an explicit time zone and **Backup retention** `2`, keep it disabled, save and check the IDs. Do not change the NFS job.
4. Run the disabled schedule by hand once from **Backup → Overview**. Check the VM export and the remote result in the log, then find the full point on `lab-backup-smb` in **Backup → Restore**. Note the times, IDs, size and any SMB mount, sign-in or space error. A snapshot left on the source SR, or a passing remote test, is not a VM backup.
5. Restore that point to the reserved SR with **Start VM after restore** off. Note the new VM and disk UUIDs. With the copy stopped, remove **every NIC** and check that the network list is empty. Start only this copy from **Console**, compare the sample checksum and shut it down. Keep the original VM, the NFS backup and the SMB point until you have recorded the result. Then remove only the test copy with the [VM removal procedure](/docs/xoa-hl/vm-operations/).

**Check:** the remote test passes, the full backup reaches the share, and the isolated copy starts with no NIC and the right data.

If access, writing, reading, deleting, the export or the restore fails, stop. Give the backup and server owners the errors (without credentials), the exact IDs, the share contents and any partial VMs. Never retry against a production share, or delete backup paths by name alone.

Not covered here: password rotation, share outages, retention over many runs, domain trust, SMB versions and security settings, speed, and other SMB servers.

## If something goes wrong

| Problem | What to check |
| --- | --- |
| The NFS test fails | Check that the appliance can reach the server, and check the export path, export permissions and mount options. Your browser reaching the NAS is not enough. |
| The backup fails or no restore point appears | Read the VM and export logs. Check remote access and free space, free space on the VM's SR, and the selected VM. A snapshot left behind is not a backup. |
| The restore point is missing | Check that the remote is enabled with no error, refresh the list, and check that the job really exported this VM. |
| The restore fails | Read its log, and check that the remote is readable and that the target SR has space and is reachable from the host. Look for a partial VM before you retry. Never delete by name alone. |
| The DR replica or its clone fails | Note the run, VM and disk IDs, the target SR's space and access, and the blocked state. Keep the replicas stopped. Do not bypass their start block or rerun retention blindly. |
| The SMB remote or its restore fails | With the Windows Server owner, check the failed test step, the job and restore logs, the server and share, the account's access, free space and partial objects. Keep the independent NFS backup. Never paste credentials into a report. |
| The restored VM has no network | This is expected: you removed all NICs for this console-only test. Connecting it to a production network needs a separate review of the guest's IP address and service identities. |
| The file differs, or the guest does not start | Check that you selected the right restore point and that the file was written before the backup. Keep the logs and the backup. The test has not passed. |

For run statuses, partial exports and a safe retry, see [Diagnose a failed backup](/docs/xoa-hl/troubleshooting/#backup-failures).

## Next steps

After a successful restore test, decide your real backup frequency, retention, capacity monitoring and how you make backups consistent for your applications. Turn a schedule on only after checking its time zone and next runs. See also the [update guide](/docs/guides/updates/) and the [glossary](/docs/xoa-hl/glossary/). Configuration recovery and Continuous Replication need their own procedures.

{{< details title="Sources" closed="true" >}}
- **Schedules**: [schedule editor/table/save ordering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [time selector and preview formatting](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [schedule API/start/stop](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [cron job behavior](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [running-job guard/log identity](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs), [full-backup retention and pruning order](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).
- **Backup and restore**: [backup routes and administrator access](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [remote form](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [remote test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [job modes and save](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [schedule and retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [manual run](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [restore controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [NIC removal](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [upstream pin](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [patch/build selection](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Incremental backups**: [Incremental export/base selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs), [Remote transfer/retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs), [Snapshot retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs), [Cleanup/merge execution](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs), [Restore chain reader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [Restore implementation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/ImportVmBackup.mjs), [Export type in logs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js).
- **Single-file recovery**: [file-restore UI and delta filter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/index.js), [backup/disk/partition/file selector](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/restore-file-modal.js), [admin file APIs and archive response](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/backup-ng.mjs), [read-only partition and tgz/zip adapter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [browser download](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **DR replica**: [job mode/target SR and schedule](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [replication retention control](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [full export and SR writer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/FullXapi.mjs), [replica import, blocked start and pruning](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullXapiWriter.mjs), [replica identity filter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_listReplicatedVms.mjs), [clone API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **SMB remote**: [remote form and Windows Server warning](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [SMB parser and formatter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-remote-parser/src/index.js), [CIFS handler](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/smb.js), [mount and remote options](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/_mount.js), [10 MiB remote test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/abstract.js), [remote lifecycle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/remotes.mjs), [XOA-HL runtime dependency](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **Known issue**: [remote test result headings (xoa-hl#38)](https://github.com/Vagrantin/xoa-hl/issues/38).
{{< /details >}}
