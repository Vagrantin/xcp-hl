---
title: "Export the XO configuration"
linkTitle: "Configuration export"
description: "Export the XO configuration, test an import safely and back up pool metadata."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: source
sourceRevision: sha256:72e05e0e98f3c43537742df9848f514ff5c7dc8c05ff135dff73c2622ccdedef
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Before appliance maintenance, save the XO configuration to a file and keep it apart from your VM backups. Then test that file on a disposable appliance. Pool metadata needs its own backup job, described below. You work in the **browser**, signed in to XOA-HL as an XO administrator.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. This page does not describe a supported recovery or downgrade path.
{{< /callout >}}

## What the export includes {#export-contents}

The export saves the XO configuration: users and groups, access rules, server connections, remotes, jobs, schedules, authentication tokens and plugin settings. Treat the file as a secret: it can contain server passwords, remote credentials and tokens.

| What | How to protect it |
| --- | --- |
| XO configuration | This export, from **Settings → Config** |
| Guest disks and data | A separate [VM backup and restore](/docs/xoa-hl/backup-restore/) |
| Host and pool metadata | A separate [pool metadata backup](#pool-metadata). Not in this export |
| Appliance OS, RPM packages and runtime logs | Not in the export |
| Server TOML file, TLS files, update settings and timezone | Not in the export. Record them separately |

A finished export does not prove that the file can restore your installation. Keep a note of the image and application versions with it.

## 1. Download and store the export

1. In the **browser**, sign in as an XO administrator. Record the [installed versions](/docs/xoa-hl/maintenance/#record-versions).
2. Open **Settings → Config** (`/#/settings/config`). Under **Export**, select **Download current config**.
3. Enter a unique passphrase and confirm. If you leave it empty, the export is not encrypted.
4. Store the passphrase separately, so that you still have it if the appliance is lost.
5. If the browser blocks the new window, allow the download. Check that a non-empty file was saved: `config.json.gz`, with `.enc` added when it is encrypted. Do not rename it to look like a VM backup.
6. Move the file to protected storage outside the appliance. Record the date, the file size, the versions and whether it is encrypted.
7. Keep your previous export until the new one passes an import test on an isolated appliance.

**Check:** you can reach the file and its passphrase without the original appliance. Never attach the file to a public issue, and never paste its decrypted content into a report.

## 2. Test an import on an isolated appliance {#import-test}

{{< callout type="warning" >}}
An import can reconnect saved servers and enable saved schedules. It can change existing entries and replace users that conflict. There is no rollback for the whole import: an error can leave partial changes. Never use a production appliance to find out what an untested export does.
{{< /callout >}}

**Before you start**

- Use a disposable appliance with the same image and package versions that you recorded.
- Restrict its network before the import: your test browser can reach it, but it cannot reach production hosts, backup remotes or external services.
- Enforce this restriction outside XO. Disabling connections or schedules before the import is not enough, because the import can restore them.
- Record the state of the fresh appliance. Have the credentials from the exported configuration ready: the import can change accounts.

1. Open **Settings → Config**. Select or drop the export file, select **Import**, then enter the export passphrase. Wait for the success or error message.
2. If the import succeeds, sign out, then sign in with an administrator account from the export.
3. Compare users, permissions, remotes, servers, jobs and schedules with your records of the source. Server connection errors are expected while the network is blocked.
4. Before you allow access to any disposable test resources, disable the imported schedules and remove or replace production destinations. Check these settings again before each test.
5. If the import fails, record the error and the `xo-server` logs, with secrets removed. Discard the appliance and start from a fresh one for the next attempt. Do not assume that a failed import changed nothing.

**Check:** the exported administrator can sign in, and users, permissions, remotes, jobs and schedules match your records. A success message alone does not prove that you can recover. A wrong passphrase, conflicting users and an interrupted import are not covered here.

## Set up pool metadata protection {#pool-metadata}

A separate **Pool metadata** job backs up a pool's metadata. XO reads an XAPI `/pool/xmldbdump` stream from the selected pool. It writes `data` and `metadata.json` to a remote, under `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. This is not the **Settings → Config** export, a VM disk backup, an appliance image or a tested way to recover a host. The metadata can reveal details of your infrastructure: restrict access to the remote, and never attach these files to a public issue.

**Before you start**

- Use one disposable pool that you own and can rebuild, connected to XOA-HL. Never change or restore a production pool for this test.
- Use a dedicated, writable NFS backup remote that does not depend on that pool's storage, so that one failure cannot affect both.
- Keep a separate [VM backup and restore](/docs/xoa-hl/backup-restore/) plan for guest data.
- Check the installed image and package. Check that the administrator can see the metadata backup controls: in this version, the interface can hide them behind a plan check. If they are missing, stop.
- Note the pool UUID, the master and host identities, the remote ID and its free space.

### Create a disabled job

1. Open **Backup → New** and choose **XO config & Pool metadata Backup** (`/#/backup/new/metadata`). Name the job `lab-pool-metadata`.
2. Enable **Pool metadata** only, and leave **XO config** off.
3. Select the disposable pool explicitly. Select only the dedicated remote. Do not add other pools or remotes.
4. Add one schedule with an explicit timezone. Set **Pool retention** to `2`, and leave the schedule disabled.
5. Save. Read back the job and schedule IDs, the pool, the remote, the mode, the retention and the disabled state. If the editor did not keep them, stop.

### Run the job three times

1. Run the job by hand from its saved schedule. Note the time: this is run A.
2. Wait until the run finishes. In the job log, check each pool and remote, including the sub-tasks. A top-level success does not prove that the remote copy is complete.
3. Note the run ID, its status and the source pool UUID.
4. Repeat for runs B and C, at different times. Start each run only after the previous one has finished.

### Check the kept points

1. Open **Backup → Restore → Metadata** (`/#/backup/restore/metadata`). Look at the **pool** entries from enabled remotes, their times and the available points. **Do not select Restore or Delete.**
2. With retention `2`, only the points from runs B and C remain. Compare them with your notes on runs A, B and C.
3. If the storage administrator can open the remote directly, ask them to check each kept point: `data` and `metadata.json` are not empty, and the job, schedule and pool identities match. Record the file sizes and hashes in a protected place. Do not publish the contents.
4. Keep any incomplete point or unexpected cleanup result for investigation.

The job writes these files without a checksum. A listed point or a successful task does not prove that XAPI can import it.

**Check:** the schedule is still disabled, the three runs name the intended pool and remote, and the kept B and C points and their files match your notes. If the export, the write to the remote, the cleanup or the listing fails, stop running the job and keep the logs and the inventory. Never delete backup folders based only on their names.

### Before any pool restore

A pool restore sends the chosen point's `data` to `/pool/xmldbdump` on the target pool. It changes the pool, and no way to undo it has been shown. Before any restore, the pool owner must provide:

- an isolated, disposable target pool
- a recovery plan that matches the versions and identities
- a separate fallback copy of the image or metadata
- blocked access to production networks and storage
- a way to check host and pool connectivity and inventory afterwards

Only after these are reviewed, choose one exact point and one target pool. An available point or a successful export does not prove that you can recover. Keep XO configuration exports and guest backups separate. The restore itself is not covered here, nor are bulk restore and restoring onto a different pool.

## Recovery and rollback limits {#recovery-limits}

For a real loss, keep the failed appliance and the evidence. Identify the exact versions, and use a recovery plan that has passed an isolated test for those versions. Never connect two copies with active schedules to the same production destinations.

An older RPM package is not a complete rollback. A downgrade does not undo OS updates, restore XO data or recover the separate files listed above. Imports between versions and recovery by downgrade have not been tested for this release. If an update fails, see [maintenance](/docs/xoa-hl/maintenance/#update-problems) and [troubleshooting](/docs/xoa-hl/troubleshooting/).

{{< details title="Sources" closed="true" >}}
- **Configuration export**: [configuration screen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [admin-only API and file format](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [encryption and importer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [server reconnection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [schedule activation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [user conflicts](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
- **Pool metadata backup**: [metadata job editor and plan check](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [admin API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [pool export and remote files](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [modes and remotes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [retention cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [restore point list](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js), [XAPI import endpoint](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
{{< /details >}}
