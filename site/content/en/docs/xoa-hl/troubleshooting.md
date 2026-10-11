---
title: Troubleshoot XOA-HL and report a problem
description: Find the right checks for login, host connection, backup and appliance update failures.
weight: 42
translationKey: xoa-manual-troubleshooting
translationStatus: source
sourceRevision: sha256:0b4aff1c1e2ce86c8e6e39cf46a9c33c23b4a840e997e96f5351a12e552a51df
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

**Why are updates listed but the check command returns 100?** The packaged checker maps `dnf check-update` exit 100 to `AVAILABLE`, 0 to `UP_TO_DATE`, and other results to `ERROR`. Listed updates are not an installation failure.

**Does stable reverse a testing update?** No. The channel controls repository selection for later checks/installations. Switching to stable does not downgrade an installed candidate.

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
