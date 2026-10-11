---
title: Export the XO configuration and plan recovery
description: Save an encrypted configuration export and understand the limits of import and rollback.
weight: 41
translationKey: xoa-manual-configuration-backup
translationStatus: source
sourceRevision: sha256:6ea2d8b7f9eb7d3a324bdf211a2c6e13676572afc1608ffb59b11fe1536736aa
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
| Host/pool metadata | Separate protection; absent from this configuration export |
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

## Recovery and rollback limits

For a real loss, preserve the failed appliance and evidence, identify the exact versions and use a recovery plan that has passed an isolated test for those versions. Do not reconnect two copies with active schedules to the same production destinations.

An available older RPM is not a complete rollback: a downgrade does not reverse OS updates, restore XO data or recover the separate files listed above. Cross-version imports and downgrade recovery remain unverified for this release. Consult [maintenance](/docs/xoa-hl/maintenance/) and [troubleshooting](/docs/xoa-hl/troubleshooting/) when an update fails.

## Sources

XO source at `e281c536`: [configuration screen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [admin-only API and file format](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [encryption and importer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [server reconnection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [schedule activation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs) and [user conflicts](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
