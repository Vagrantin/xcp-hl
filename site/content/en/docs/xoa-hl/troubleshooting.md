---
title: "Troubleshoot backup failures and other problems"
linkTitle: "Troubleshooting"
description: "Diagnose network, backup, update and sign-in problems, and report an issue."
weight: 82
translationKey: xoa-manual-troubleshooting
translationStatus: source
sourceRevision: sha256:36005ab36c53c37c111ad42e7878c01a9bc11a9ba3f7fc93a528fccdfea56519
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Start with the symptom and the operation that preceded it. Preserve evidence before retrying a failed update or import.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. These checks are not a record of reproduced appliance failures or verified recovery. Commands below run inside the appliance, not on the hypervisor host.
{{< /callout >}}

## Choose the next check

| Symptom | Check and next action | Verify before continuing |
| --- | --- | --- |
| Appliance page does not open | In XO Lite, check the VM is running and its address/network are correct. Use console access to inspect `xo-server` and disk space below. | Correct appliance URL opens the login page |
| First-login credentials fail | Follow [first-login guidance](/docs/xoa-hl/first-login/) for web credentials and first-boot fallback. Inspect provisioning logs through authorized console access. | Login works and the bootstrap password has been changed |
| Host is enabled but inventory is empty | In Settings → Servers, read the connection error. Verify the host address, credentials, certificate identity and connectivity from the appliance. | Intended host and storage appear without connection error |
| VM creation or installation fails | Recheck selected pool, template, SR capacity, network and boot media against [the VM tutorial](/docs/xoa-hl/create-vm/). Record the task error before retrying. | Disposable VM boots the intended installer |
| Backup or restore fails | Read the job log and check the remote, credentials, storage capacity and target SR. Use [the backup tutorial](/docs/xoa-hl/backup-restore/); keep every restored NIC removed before first boot. | Job succeeds and an isolated restored guest has the expected data |
| Update page disconnects | Read the managed installation log and service state; the RPM restarts `xo-server`. Do not launch a duplicate transaction. | Final success marker, expected version, login and host inventory |
| Update check says ERROR | Read `/run/xoa-hl/status` and the check-service journal. Investigate repository/network errors or a busy updater before checking again. | A fresh verdict is `UP_TO_DATE` or `AVAILABLE` |
| Automatic update did not run | Check saved mode, appliance timezone, delay and timer listing. An installation window missed while powered off is not replayed at boot. | Intended timer is scheduled; later run timestamps match the window |
| Configuration import fails | Save the error and server log; partial changes can remain. Follow [isolated import guidance](/docs/xoa-hl/configuration-backup/). | Fresh disposable test passes; do not treat the failed target as unchanged |

For console controls or a blank/unresponsive screen, follow [VM console checks](/docs/xoa-hl/vm-operations/#vm-console).

## Diagnose network connectivity {#network-connectivity}

Use this read-only investigation for an existing ordinary guest network or the [lab VLAN](/docs/xoa-hl/storage-networks/#host-vlan-network). Sign in as an XOA-HL administrator to inspect the complete VM/pool/host inventory. Guest checks require an authorized guest console session; switch, DNS and firewall checks belong to their owners. Keep independent host console access available. Do not create a failure or change management networking to test this guide. Bonds, SDN, guest VLAN trunks and emergency network recovery need separate procedures.

### 1. Identify the failing path

Record the time with timezone, last successful operation, exact error, source machine, destination name/address, protocol and service port. Preserve the baseline before retrying. A successful test from your laptop does not establish access from the appliance, host or guest.

| Path | Where to investigate |
| --- | --- |
| Browser → appliance | Check the intended URL, name resolution and certificate identity on the client; use authorized appliance console access if the page is unreachable. Follow the service checks below. |
| Appliance → host | Read the connection error at `/#/settings/servers`, then use [host connection guidance](/docs/xoa-hl/hosts-pools/). Enabled is a configuration state, not proof of a working connection. |
| Host → NFS SR | Inspect the exact SR and that host's attachment/location using [storage readback](/docs/xoa-hl/storage-networks/#nfs-vm-storage). A guest or appliance test cannot substitute for host access. |
| Appliance → backup remote | Use [backup failure checks](#backup-failures). An NFS SR and a backup remote have different clients and identities. |
| Guest → peer/service | Follow the mapping and guest checks below. Successful XO login or console display does not prove guest network access. |

### 2. Trace one guest interface to its host uplink

1. Record the VM UUID, power state, resident host and pool. Open its network tab (`/#/vms/<id>/network`). Use the VIF row's UUID copy action; record device number, MAC, network, MTU and status. Match the exact network UUID in the pool view (`/#/pools/<id>/network`), not just its name. Read controls without clicking editable network/MAC fields or connection buttons.
2. **Connected** reflects VIF attachment. A stopped VM's detached VIF is not evidence of a fault. **IP addresses** comes from guest metrics grouped by VIF device; an absent address does not prove missing guest configuration, and a displayed address is not a live reachability test. Compare with the guest console and [guest-agent checks](/docs/xoa-hl/guest-tools/).
3. Record the locking-mode indicator and **Allowed IPs** separately from reported IPs. These are traffic-policy settings, not a form for assigning the guest's IP address. Preserve any warning and ask the network owner to interpret the effective policy. Do not unlock the interface, clear restrictions, change MAC/MTU or disable security as a diagnostic shortcut.
4. In the pool network row, expand **PIFs** and find the resident host. The row's VLAN summary uses the master; inspect the actual host's network tab (`/#/hosts/<id>/network`) for PIF UUID, device/MAC, network, VLAN, MTU, management flag and IP modes. Compare with the approved cabling/switch inventory. An intentionally internal network may have no physical uplink; establish the expected topology before calling that a fault.
5. Read attachment and carrier separately. The host's **Connected** button reflects PIF attachment; the separate physical-link icon and expanded pool PIF status use carrier. Missing PIF metrics can also map to false carrier in this source, so a negative indication alone does not prove an unplugged cable. Refresh and correlate with host/switch observations. Do not toggle PIFs, edit VLAN/MTU/IP, delete networks or restart networking to probe the path.

### 3. Compare guest settings and service results

Through the **guest console**, match the interface by MAC and inspect its current address/prefix, routes and DNS settings using that OS's tools. Do not assume a guest interface name matches the host's device name. Compare with the network owner's approved unique address and subnet; a tagged host VLAN normally presents an untagged guest interface in the linked lab exercise.

Have the guest/network administrators test the agreed peer and application service from that exact guest. Record name-resolution answers, selected address family, destination, protocol/port and result separately. If name and address tests differ, investigate DNS and application/TLS identity before drawing a conclusion; accessing HTTPS by bare IP may change certificate or virtual-host behavior. Never bypass certificate verification to declare success. Ping success does not prove a service works; ping failure does not establish isolation. Test only approved endpoints, including owner-defined forbidden destinations where isolation is required.

A same-host peer result does not test the physical uplink. Cross-host or off-host tests require identified peers and an approved switch path; do not migrate a workload as an improvised diagnosis. Preserve evidence of unexpected production access and stop the disposable test guest normally. If management or storage is affected, use independent console access and the owner's recovery plan before further changes.

### 4. Verify the owner-selected remedy

Give the responsible owner the exact mapping, timestamps, error and comparison results. Apply an agreed correction through the relevant guest, storage, host or network procedure; this investigation does not prescribe a generic reset. Then refresh the inventory and repeat the **same source-to-destination service test**, plus required isolation checks and management/storage access. Record what changed and the observed result. A green indicator alone is not resolution. If the path remains uncertain, keep the incident open and share a sanitized report; installed fault/recovery acceptance remains pending.

## Diagnose a failed full-NFS backup {#backup-failures}

Use this procedure for the [full-NFS lab job](/docs/xoa-hl/backup-restore/) only, with an XOA-HL administrator account. You need the job/schedule IDs, source VM UUID, remote ID, expected run time with timezone and the last isolated restore result. Inspection runs in the **browser**; storage checks belong to the administrator of the affected storage system. No failure injection is required. Delta chains, replication and production recovery need separate procedures.


[Rehearse incremental backups and chain recovery](/docs/xoa-hl/backup-restore/#delta-backups).
[Download and verify one file from its retained delta point](/docs/xoa-hl/backup-restore/#file-restore).
[Rehearse a full DR replica and isolated clone on another pool](/docs/xoa-hl/backup-restore/#dr-replica).
[Test one Windows Server SMB remote with a full backup and isolated restore](/docs/xoa-hl/backup-restore/#smb-remote).


### 1. Identify the run and preserve its details

1. Open **Backup → Overview** (`/#/backup/overview`) and find the job. Inspect the **Logs** table below it. Clear the log search/status filters if necessary, then match the job and start time. The table shows a shortened job ID; use the full IDs in the details rather than a name alone.
2. Select the run's status button to open its details. Record the run `id`, `jobId`, `scheduleId`, start/end times and status. Use the clipboard or **Download log** button to preserve the JSON privately before changing anything. Create a sanitized excerpt for a report; the downloaded log is not automatically redacted.
3. Clear the detail search and select all task statuses. Inspect every page of VM tasks: the dialog can initially show only pending/failed/interrupted tasks and paginates at five entries. Match the VM UUID, then its snapshot, remote/export and transfer tasks. Preserve errors, skipped reasons and warnings at each relevant level. Not every raw task is rendered; consult the preserved JSON if the visible tree is incomplete.

**Check:** the evidence identifies one exact run and the affected VM/remote. Missing logs or missing tasks do not prove that no work occurred.

### 2. Interpret the status before retrying

These literal status labels come from the ce38 catalogs. In French, **Started** is **Démarré**; in Japanese it is **スタートしました**. The other job-status labels below, **Logs** and **Download log**, fall back to English at this pin.

| Status / JSON value | Meaning and next check |
| --- | --- |
| Started / `pending` | The run is recorded as active. Refresh and inspect progress; an absent end time is not successful completion. Do not start another run. |
| Successful / `success` | The recorded run/tasks completed successfully. Read warnings and confirm the new restore point; prove guest/data recovery separately. |
| Skipped / `skipped` | Work was omitted. Read the reason: this source classifies errors such as `no disks found`, `no VMs match this pattern` and `unhealthy VDI chain` as skipped. This is not a new verified backup. |
| Failed / `failure` | The run or a child task failed. Other work may have succeeded; inspect the affected stage and actual backup inventory. |
| Interrupted / `interrupted` | A start has no matching completion and the server no longer records that run as active. Preserve the server timeline and partial-object inventory; this status does not establish rollback or safe retry. |
{.xoa-backup-diagnosis}

### 3. Separate the failed stage from surviving data

Use **Backup → Restore** (`/#/backup/restore`) for the restore-point inventory and restore logs.

| Observation | Check before choosing a remedy |
| --- | --- |
| No matching run | Recheck log filters, job/schedule IDs, enabled state, timezone, server availability and the [schedule readback](/docs/xoa-hl/backup-restore/#backup-schedules). Do not assume automatic catch-up or email delivery. |
| VM or snapshot error, or skipped VM | Check selected VM UUID, disks, host connection and source SR capacity. Preserve the exact reason. Do not remove snapshots or manipulate a VDI chain as a generic fix. |
| Remote, export or transfer error | Check appliance-to-NFS access, export permissions/options and remote capacity with the storage administrator. A successful remote test does not prove the whole export or restore. |
| Transfer succeeded but the run failed later | With **Delete first** off, this full writer exports and writes metadata before pruning older points. A new point may survive a later cleanup failure. Check timestamps and retained points before rerunning or deleting files. |
| Point missing from Restore | Open **Backup → Restore** and refresh. Check the intended remote is enabled and read any remote-loading error. An unreadable remote can be absent from the list; an empty list is not proof its backups were deleted. |
| Restore failed | Read the restore logs on that page, check remote readability and destination SR/host access, and inventory any partial VM/disks by UUID. Keep the source VM and backup; do not delete by name alone. |
{.xoa-backup-diagnosis}

**Check:** distinguish the failed stage, surviving recovery points and objects whose state is still unknown. A file or listed point alone is not proven recoverable data.

### 4. Recover in the lab and verify the result

1. If future triggers need to be paused, disable the exact lab schedule in Overview and refresh to verify its state. Disabling does not cancel active work. The Overview cancellation control is disabled at this pin; restarting `xo-server` is not a backup cancellation or cleanup recipe.
2. Resolve the identified access/capacity/selection problem with its owner and read back the job, schedule, VM and remote. Keep **Delete first** off and protect required recovery copies outside the job's retention. If active work or partial-object ownership is uncertain, preserve the evidence and seek help before retrying.
3. Once no run is active and the state is understood, use the tutorial's ordinary manual run for this one-VM lab job. The detail dialog's restart/force controls **execute backups**; they are not guest reboot buttons or read-only diagnostics. This procedure does not use force or claim that a retry is free of retention changes.
4. Inspect the new run and restore-point inventory, then [restore a stopped copy, remove every NIC and check the sample data](/docs/xoa-hl/backup-restore/). Leave the lab schedule disabled. Record the original error, remedy, new run/point IDs and isolated restore result before considering scheduled operation again.

**Check:** the corrected run, retained inventory and isolated guest/data restore all pass. Otherwise keep the incident open and [report the sanitized evidence](#report-a-problem). Appliance failure/recovery and human language acceptance remain pending for this preview.

## Read-only appliance diagnostics

Use an authorized console or SSH session with root privileges where required. A missing runtime status file before a first check, or after reboot, is not itself proof of failure. A nonzero `systemctl status` result can describe an inactive or failed unit; read the displayed state.

```bash
rpm -q xoa-hl nodejs
timedatectl
df -h
systemctl status xo-server redis xoa-hl-update.service --no-pager
systemctl list-timers 'xoa-hl-*'
journalctl -u xo-server -u xoa-hl-check-update.service -u xoa-hl-update.service -u xoa-hl-auto-update.service --since '1 hour ago' --no-pager
tail -n 100 /var/log/xoa-first-boot.log
tail -n 100 /var/lib/xoa-hl/update.log
cat /run/xoa-hl/status
cat /var/lib/xoa-hl/auto-update.status
```

Do not delete database files, logs or locks to make an error disappear. For a full disk, identify the growing files and preserve evidence before choosing a cleanup. See [maintenance](/docs/xoa-hl/maintenance/) for status meanings and update/reboot decisions. The automatic status can describe an older run; compare its UTC timestamps.

## Common questions

**Why did host maintenance leave VMs behind or the host disabled?** Preserve the task and inspect the actual host enabled state and each VM’s residence. The [disposable host-maintenance pilot](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) separates evacuation from re-enabling. A partial evacuation or an early failure needs the host owner’s recovery plan; do not bypass migration blocks or repeat the toggle blindly.

**Why did a host fail to join a pool?** Preserve the task/error and both pool inventories. The [two-host pool-join pilot](/docs/xoa-hl/hosts-pools/#pool-join) checks exact IDs, patch differences, master, networks and storage before confirmation. The UI invokes a forced join; do not repeat it or eject a host to clear an unexplained failure.

**Why was delegated VM creation refused?** Follow the [resource-set quota pilot](/docs/xoa-hl/permissions/#resource-set-delegation). Compare the exact user, selected set, template/SR/network IDs and quota Used/Total. A visible template or button alone does not establish server permission. Preserve the error and check for a partial VM or disk before retrying; do not raise quotas or grant pool Admin to clear an unexplained failure.

**Why are updates listed but the check command returns 100?** The packaged checker maps `dnf check-update` exit 100 to `AVAILABLE`, 0 to `UP_TO_DATE`, and other results to `ERROR`. Listed updates are not an installation failure.

**Does stable reverse a testing update?** No. The channel controls repository selection for later checks/installations. Switching to stable does not downgrade an installed candidate.

**Does a pool metadata point prove that a host can be recovered?** No. The [pool metadata pilot](/docs/xoa-hl/configuration-backup/#pool-metadata) checks only export, retention and file identity. Restore on an isolated disposable pool remains pending.

**Can a configuration export replace a VM backup or appliance rollback?** No. Use the [configuration scope and recovery limits](/docs/xoa-hl/configuration-backup/) and retain separate guest backups.

## Report a problem

[Open an XCP-HL issue](https://github.com/Vagrantin/xcp-hl/issues/new). Include this information as text:

- Page URL and language, or the appliance route where the problem occurs.
- Image tag, About versions, installed RPM/Node versions and stable/testing channel.
- Operation, exact steps, expected result and actual error.
- Time with timezone, manual/automatic mode, relevant service state and sanitized log excerpt.
- Whether the problem repeats on a disposable appliance and the last known working version.

Remove passwords, tokens, cookies, private hostnames/addresses and user or guest data from logs and screenshots. `xo-server` and first-boot logs can contain credentials. Never attach a configuration export, TLS private key or complete configuration file. Preserve the original evidence privately.

## Sources

Release-scoped behavior: [update scheduling](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [check exit-code mapping](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [server service](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service) and [first-boot provisioning](https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-credentials.sh). The linked task chapters cite their pinned UI/API sources.

Backup-diagnosis sources at XO `e281c536`: [overview and run details](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js), [task filters, pagination and rendering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js), [raw log and restart controls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js), [status aggregation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/backups-ng-logs.mjs), [full export/pruning order](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [remote-list errors and restore logs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js).

Network diagnosis sources (XO `e281c536`): [VM network UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [Host network UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [Pool network UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [PIF carrier display](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [Guest metrics and interface mapping](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [Server connection state](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js).
