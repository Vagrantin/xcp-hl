---
title: "Export the XO configuration"
linkTitle: "Configuration export"
description: "Export the XO configuration, test an import safely and back up pool metadata."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: source
sourceRevision: sha256:180ae9b2a6163db1325b4575e8cf083b05b36f83cd0dc30021bc5104b3f91bf7
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Save XO settings separately from VM backups before appliance maintenance.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38`, XO 5.113.2 at `e281c536`. Export/import round-trip and recovery tests on a disposable appliance are pending. This page does not establish a supported recovery or downgrade path.
{{< /callout >}}

## What the export protects

The web export serializes registered XO configuration entries, including users/groups, access rules, server connections, remotes, jobs, schedules, authentication tokens and plugin settings. Treat it as secret material: server passwords, remote credentials and tokens can be included.

| Material | Protection to arrange |
| --- | --- |
| XO configuration | Export through Settings → Config |
| Guest disks and data | Separate [VM backup and restore](/docs/xoa-hl/backup-restore/) |
| Host/pool metadata | Separate [pool metadata backup](#pool-metadata); absent from this configuration export |
| Appliance OS, RPMs and runtime logs | Absent from the export |
| Server TOML, TLS files, update settings and timezone | Record separately; absent from the export |

Export completion does not prove that the file can restore your installation. Keep its image/application identities with it.

## 1. Download and store the export

1. In the **browser**, sign in as an XO administrator. Record the [installed versions](/docs/xoa-hl/maintenance/).
2. Open **Settings → Config** (`/#/settings/config`) and choose **Download config** under **Export config**. Labels can differ by interface language; the route is unchanged.
3. Enter a unique passphrase and confirm. Leaving it empty produces an unencrypted export. Store the passphrase separately so it remains available if the appliance is lost.
4. Allow the download if the browser blocks the new window. Check that a nonempty file was saved: this API uses `config.json.gz`, adding `.enc` when encrypted. Do not rename it to imply that it is a VM backup.
5. Move the file to protected storage outside the appliance. Record date, file size, versions and encryption choice. Keep an earlier export until the new one passes an isolated import test.

**Check:** the downloaded file and its separately stored passphrase are accessible without the original appliance. Do not attach the file to a public issue or paste its decrypted contents into a report.

## 2. Prepare an isolated import test

{{< callout type="warning" >}}
Import can reconnect saved servers and activate saved schedules. It can update existing entries and replace conflicting user identities. The importer has no transaction-wide rollback: an error can leave partial changes. Never use a production appliance to discover what an untested export does.
{{< /callout >}}

Use a disposable appliance with the same recorded image/package. Before importing, restrict its network so your test browser can reach it but it cannot reach production hosts, backup remotes or external services. This must be enforced outside the imported XO configuration; disabling connections or schedules before import is insufficient because import can restore them.

1. Record the fresh appliance state and prepare credentials from the exported configuration; the import can change accounts.
2. Open **Settings → Config**, select or drop the export file, then choose **Import config** and supply the export passphrase. Wait for the success/error status.
3. On success, sign out and test an exported administrator login. Compare users, permissions, remotes, server definitions, jobs and schedules with the recorded source. Server connection failures are expected while network access is blocked.
4. Disable imported schedules and remove or replace production destinations before allowing access to disposable test resources. Check those settings again before each test operation.
5. On failure, record the error and sanitized `xo-server` logs. Discard the disposable appliance and start fresh for another attempt; do not assume the failed import left its state untouched.

**Acceptance still needed:** encrypted and unencrypted round-trips, wrong passphrase, conflicting users, interrupted import, destination isolation, exported administrator login and representative permissions/jobs. A success banner alone does not satisfy this recovery test.

## 3. Rehearse pool metadata protection {#pool-metadata}

This **source-reviewed preview** uses a separate **Pool metadata** job. XO requests an XAPI `/pool/xmldbdump` stream from the selected pool and writes `data` plus `metadata.json` to a remote under `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. It is not the Settings → Config export, a VM-disk backup, an appliance image or a tested host recovery path. The metadata may reveal infrastructure details; restrict remote access and keep it out of public issue attachments.

Use one disposable pool that you own and can rebuild, with a working XOA-HL connection and a dedicated writable NFS backup remote outside that pool's storage failure domain. Keep an independent [VM backup and restore](/docs/xoa-hl/backup-restore/) plan for guest data. Confirm the installed image/package and the administrator's access to the metadata controls; the pinned UI has a plan gate, so stop if the controls are unavailable. Record the pool UUID, master/host identities, remote ID and capacity. Do not change or restore a production pool for this exercise.

1. In **Backup → New → Metadata** (`/#/backup/new/metadata`), name a new job `lab-pool-metadata`. Enable **Pool metadata** only, select the one disposable pool explicitly, leave **XO config** off, and choose only the dedicated remote. Do not add other pools or remotes. Create one schedule with an explicit timezone, set **Pool metadata retention** to `2`, and leave the schedule disabled. Save and read back its job/schedule IDs, selected pool/remote, mode, retention and disabled state. If the editor cannot preserve that state, stop.
2. Run that job manually using its saved schedule three times at distinct recorded times, A/B/C. Wait for each run to finish before starting the next. Inspect the job log per pool and remote, including child tasks; a top-level success alone does not establish a complete remote copy. Record each run ID/status and the source pool UUID.
3. In **Backup → Restore → Metadata** (`/#/backup/restore/metadata`), inspect **pool** entries from enabled remotes, timestamps and available points. **Do not select Restore or Delete.** For the ordinary retention-2 fixture, compare A/B/C run evidence with the retained B/C inventory. If the remote is independently accessible to its storage administrator, have them confirm that each retained point has nonempty `data` and `metadata.json`, with the expected job/schedule/pool identities, and record file sizes and protected hashes without publishing the contents. The writer disables its output checksum; a displayed point or successful task does not prove that XAPI can import it. Preserve any partial point or pruning discrepancy for investigation.

**Backup pilot pass:** the job remains disabled, three runs identify the intended pool and remote, and the retained B/C points and protected files match the recorded identities. If export, remote write, cleanup or listing fails, stop further runs and retain logs and inventory; do not delete backup paths by name alone.

**Restore acceptance remains pending:** the UI's pool restore sends the selected point's `data` to `/pool/xmldbdump` on the chosen target pool. It is a state-changing operation with no demonstrated rollback here. Before any restore, the pool owner must provide an isolated disposable target and a version/identity-matched recovery plan, a separate fallback image/metadata copy, blocked production networks and storage, and a way to observe host/pool connectivity and inventory afterwards. Select one exact point and one target only after those prerequisites are reviewed; bulk restore and cross-pool substitution are outside this pilot. Do not infer a valid recovery from an available point or a green export. Keep XO configuration export and guest backups separate.

## Recovery and rollback limits

For a real loss, preserve the failed appliance and evidence, identify the exact versions and use a recovery plan that has passed an isolated test for those versions. Do not reconnect two copies with active schedules to the same production destinations.

An available older RPM is not a complete rollback: a downgrade does not reverse OS updates, restore XO data or recover the separate files listed above. Cross-version imports and downgrade recovery remain unverified for this release. Consult [maintenance](/docs/xoa-hl/maintenance/) and [troubleshooting](/docs/xoa-hl/troubleshooting/) when an update fails.

## Sources

XO source at `e281c536`: [configuration screen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [admin-only API and file format](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [encryption and importer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [server reconnection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [schedule activation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs) and [user conflicts](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).

Pool metadata pilot sources (XO `e281c536`): [metadata job editor and plan gate](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [admin API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [pool export and remote files](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [mode/remote runner](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [retention pruning](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [restore chooser](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js) and [XAPI import endpoint](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
