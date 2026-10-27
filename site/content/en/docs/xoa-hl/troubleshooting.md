---
title: "Troubleshoot backup failures and other problems"
linkTitle: "Troubleshooting"
description: "Find the cause of network, backup, update and sign-in problems, and report an issue."
weight: 82
translationKey: xoa-manual-troubleshooting
translationStatus: source
sourceRevision: sha256:d00c8a19bd7442223695be12b1214627dd1a98f307f3c87fc03e91287c7a340d
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Start from the symptom and the last operation before it, then follow the matching check. Most checks only read information: you sign in to the **XOA-HL appliance** in your browser as an administrator. Some checks need the appliance console or a guest console. Before you retry a failed update, import or backup, save the error and the logs.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system.
{{< /callout >}}

## Start from the symptom {#symptoms}

| Problem | What to check |
| --- | --- |
| The appliance page does not open | In XO Lite, check that the appliance VM is running and that its address and network are right. Then check `xo-server` and disk space with the [console checks](#appliance-checks). **Check:** the right URL opens the sign-in page. |
| The first sign-in fails | Follow the [first sign-in guide](/docs/xoa-hl/first-login/) for the web credentials and the first-boot fallback. With authorized console access, read the provisioning log. **Check:** you can sign in, and the first password has been changed. |
| A host is enabled but nothing is listed | In **Settings → Servers**, read the connection error. Check the host address, the credentials, the certificate identity and that the appliance can reach the host. **Check:** the host and its storage appear, with no connection error. |
| Creating or installing a VM fails | Note the task error before you retry. Check the pool, template, SR free space, network and boot media against [Create your first VM](/docs/xoa-hl/create-vm/). **Check:** a test VM starts the installer you chose. |
| A backup or restore fails | Read the job log. Check the remote, credentials, free space and target SR, then follow [Diagnose a failed NFS backup](#backup-failures). Remove every NIC of a restored copy before its first start, as in [Back up and restore a VM](/docs/xoa-hl/backup-restore/). **Check:** the job succeeds, and an isolated restored copy has the expected data. |
| The update page disconnects | Installing the package restarts `xo-server`. Read the update log and the service state. Do not start a second update. **Check:** the log ends with its success marker, the version is the expected one, you can sign in and the hosts are listed. |
| The update check shows ERROR | Read `/run/xoa-hl/status` and the journal of the check service. Look for repository or network errors, or an update already running, before you check again. **Check:** a new check returns `UP_TO_DATE` or `AVAILABLE`. |
| An automatic update did not run | Check the saved mode, the appliance time zone and the timer list. A window missed while the appliance was off does not run at the next start. **Check:** the right timer is scheduled, and later run times match the window. |
| A configuration import fails | Save the error and the server log: some changes can remain. Follow the [isolated import test](/docs/xoa-hl/configuration-backup/). **Check:** the test passes on a new, disposable appliance. Do not assume that the failed target is unchanged. |
| No administrator can sign in | A lost password, a lost one-time code device or a broken LDAP or SAML sign-in. Follow [Recover administrator access](#recover-admin-access) from the appliance console. **Check:** the account signs in with its new password and is listed as **Admin**. |

For console problems, such as the controls or a blank or frozen screen, see [Use the VM console](/docs/xoa-hl/vm-operations/#vm-console).

## Diagnose network connectivity {#network-connectivity}

Use these read-only checks for an existing, ordinary guest network or for the [lab VLAN](/docs/xoa-hl/storage-networks/#host-vlan-network). Sign in as an XOA-HL administrator, so that you can see every VM, pool and host.

**Before you start**

- Guest checks need an authorized session on the guest console. The owners of the switches, DNS and firewalls check those.
- Keep separate console access to the host available.
- Do not create a fault, and do not change the management network, to test this guide.
- Bonds, SDN, VLAN trunks inside guests and emergency network recovery are not covered here.

### 1. Find the failing path

Note the time with its time zone, the last operation that worked and the exact error. Also note the source machine, the destination name or address, the protocol and the service port. Save this starting state before you retry. A test that works from your laptop does not prove access from the appliance, a host or a guest.

| Path | Where to look |
| --- | --- |
| Browser → appliance | On your computer, check the URL, name resolution and certificate identity. If the page does not open, use authorized console access and the [console checks](#appliance-checks). |
| Appliance → host | Read the connection error in **Settings → Servers** (`/#/settings/servers`), then follow [Hosts and pools](/docs/xoa-hl/hosts-pools/). "Enabled" is a setting, not proof that the connection works. |
| Host → NFS SR | Check the exact SR, and that host's attachment and path, as in [Create NFS storage for VM disks](/docs/xoa-hl/storage-networks/#nfs-vm-storage). A test from a guest or from the appliance does not replace the host's own access. |
| Appliance → backup remote | Follow [Diagnose a failed NFS backup](#backup-failures). An NFS SR and a backup remote use different clients and identities. |
| Guest → peer or service | Follow steps 2 to 4 below. Signing in to XO, or seeing the console, does not prove that the guest has network access. |

### 2. Trace the guest interface to the host uplink

Only read these screens. Do not click editable network or MAC fields, or connection buttons.

1. Note the VM UUID, its power state, the host it runs on and its pool. Open the VM's **Network** tab (`/#/vms/<id>/network`).
2. Copy the interface (VIF) UUID with the row's copy button. Note the device number, MAC address, network, MTU and status.
3. Open the pool's network view (`/#/pools/<id>/network`) and match the exact network UUID, not only its name.
4. Read **Connected**: it shows whether the VIF is attached. A detached VIF on a stopped VM is not a fault.
5. Read **IP addresses**: it comes from the guest metrics, per VIF device. A missing address does not prove that the guest is not configured. A shown address is not a live reachability test. Compare with the guest console and the [guest agent checks](/docs/xoa-hl/guest-tools/).
6. Note the locking mode indicator and **Allowed IPs** separately from the reported addresses. They are traffic rules, not a form to give the guest its IP address. Save any warning, and ask the network owner to explain the rules that apply. Do not unlock the interface, clear restrictions, change the MAC or MTU, or turn off security as a shortcut.
7. In the pool network row, expand **PIFs** and find the host the VM runs on. That row's VLAN summary comes from the pool master only.
8. Open that host's **Network** tab (`/#/hosts/<id>/network`). Note the PIF UUID, device, MAC, network, VLAN, MTU, management flag and IP mode. Compare them with the approved cabling and switch records. A network can be internal on purpose, with no physical uplink: check the expected layout before you call it a fault.
9. Read the attachment and the physical link (carrier) separately. The host's **Connected** button shows whether the PIF is attached. The physical link icon, and the PIF status in the expanded pool row, show the carrier.

Missing PIF metrics can also show as no carrier, so a negative status alone does not prove an unplugged cable. Refresh, and compare with what the host and the switch show. Do not toggle PIFs, edit VLAN, MTU or IP settings, delete networks or restart networking to probe the path.

### 3. Check guest settings and the service

1. On the **guest console**, find the interface by its MAC address. Its name in the guest may differ from the host's device name.
2. With the guest operating system's tools, read its address and prefix, routes and DNS settings. Compare them with the unique address and subnet that the network owner approved. On the lab VLAN, the guest normally sees an untagged interface.
3. Ask the guest or network administrators to test the agreed peer and application service from this exact guest. Note separately the DNS answers, the address family used, the destination, the protocol and port, and the result.
4. If a test by name and a test by address give different results, check DNS and the application or TLS identity before you conclude. HTTPS to a bare IP address can change the certificate or virtual host. Never bypass certificate checks to declare success.

A successful ping does not prove that a service works, and a failed ping does not prove isolation. Test only approved destinations. When isolation is required, also test the forbidden destinations that the owner defines.

A peer on the same host does not test the physical uplink. Tests across hosts, or outside the host, need identified peers and an approved switch path. Do not migrate a workload to improvise a test. If you see unexpected access to production, save the evidence and shut the test guest down normally. If management or storage is affected, use the separate host console and the owner's recovery plan before any other change.

### 4. Check the fix

1. Give the owner the exact mapping, the times, the error and your comparison results.
2. Apply the agreed fix through the right guest, storage, host or network procedure. This guide does not prescribe a general reset.
3. Refresh the inventory. Repeat the **same service test, from the same source to the same destination**.
4. Repeat the required isolation checks, and check management and storage access.
5. Note what changed and the result.

**Check:** the same test now passes. A green indicator alone does not mean that the problem is solved. If the path is still unclear, keep the incident open and [report a problem](#report-a-problem) with sanitized details.

## Diagnose a failed NFS backup {#backup-failures}

Use this only for the [full backup job to NFS from the tutorial](/docs/xoa-hl/backup-restore/), signed in as an XOA-HL administrator. You work in the **browser**. Storage checks belong to the administrator of that storage. You do not need to cause a failure.

**Before you start**

- Note the job and schedule IDs, the source VM UUID, the remote ID, the expected run time with its time zone and the result of the last isolated restore.
- Incremental chains, replication and production recovery are not covered here. For other backup tests, see [incremental backups and chain recovery](/docs/xoa-hl/backup-restore/#delta-backups), [one file from a delta backup](/docs/xoa-hl/backup-restore/#file-restore), [a DR replica on another pool](/docs/xoa-hl/backup-restore/#dr-replica) and [an SMB remote on Windows Server](/docs/xoa-hl/backup-restore/#smb-remote).

### 1. Find the run and save its details

1. Open **Backup → Overview** (`/#/backup/overview`) and find the job. Look at the **Logs** table below it.
2. Clear the log search and status filters if needed. Find the run by its job and start time. The table shortens the job ID, so use the full IDs from the details, not only the name.
3. Select the run's status button to open its details. Note the run `id`, `jobId`, `scheduleId`, the start and end times, and the status.
4. Before you change anything, save the JSON privately with the clipboard button or **Download log**. The downloaded log is not redacted: for a report, make a sanitized excerpt.
5. Clear the search in the details and select all task statuses. At first, the dialog can show only pending, failed or interrupted tasks, five per page. Check every page.
6. Find the VM UUID, then its snapshot, remote, export and transfer tasks. Save the errors, skip reasons and warnings at each level. Not every raw task is shown: if the tree looks incomplete, read the saved JSON.

**Check:** your notes identify one exact run, and the affected VM and remote. Missing logs or tasks do not prove that nothing ran.

### 2. Read the status before you retry

| Status (JSON value) | What it means and what to check |
| --- | --- |
| Started (`pending`) | The run is recorded as active. Refresh and follow its progress. A missing end time does not mean success. Do not start another run. |
| Successful (`success`) | The run and its recorded tasks finished. Read the warnings and check the new restore point. Test the recovery of the guest and its data separately. |
| Skipped (`skipped`) | Some work was left out. Read the reason: errors such as `no disks found`, `no VMs match this pattern` and `unhealthy VDI chain` count as skipped. This is not a new, checked backup. |
| Failed (`failure`) | The run or a child task failed. Other work may have succeeded: check the failed stage and the backups that actually exist. |
| Interrupted (`interrupted`) | A start has no matching end, and the server no longer records the run as active. Save the server timeline and the list of partial objects. This status does not prove a rollback, or that a retry is safe. |
{.xoa-backup-diagnosis}

### 3. Separate the failed stage from surviving data

Open **Backup → Restore** (`/#/backup/restore`) to see the restore points and the restore logs.

| Problem | What to check |
| --- | --- |
| No matching run | Check the log filters, the job and schedule IDs, the enabled state, the time zone, the server's availability and the [saved schedule](/docs/xoa-hl/backup-restore/#backup-schedules). Do not assume that missed runs catch up, or that an email was sent. |
| A VM or snapshot error, or a skipped VM | Check the selected VM UUID, its disks, the host connection and the source SR's free space. Save the exact reason. Do not delete snapshots or change a VDI chain as a general fix. |
| A remote, export or transfer error | With the storage administrator, check that the appliance can reach the NFS export, the export permissions and options, and the remote's free space. A successful remote test does not prove the whole export or a restore. |
| The transfer worked, then the run failed | With **Delete first** off, this full backup writes the export and its metadata before it deletes older points. So a new point can survive a later cleanup failure. Check the times and the kept points before you rerun or delete files. |
| The point is missing from Restore | Open **Backup → Restore** and refresh. Check that the right remote is enabled, and read any loading error. An unreadable remote can be missing from the list: an empty list does not prove that its backups were deleted. |
| The restore failed | Read the restore logs on that page. Check that the remote is readable and that the target SR and host are reachable. List any partial VM or disks by UUID. Keep the source VM and the backup, and never delete by name alone. |
{.xoa-backup-diagnosis}

**Check:** you can tell apart the failed stage, the restore points that survived, and the objects whose state is still unknown. A file or a listed point alone does not prove that the data can be recovered.

### 4. Fix the cause and check the result

1. To stop future runs, disable the exact lab schedule in **Overview**, then refresh to check its state. This does not cancel a running backup: the cancel button in **Overview** is disabled in this version. Restarting `xo-server` does not cancel or clean up a backup.
2. Fix the access, space or selection problem with its owner. Then check the job, schedule, VM and remote again.
3. Keep **Delete first** off, and keep the recovery copies you need outside this job's retention. If you are unsure whether work is still running, or who owns partial objects, save the evidence and ask for help before you retry.
4. When no run is active and you understand the state, run this one-VM lab job by hand, as in the tutorial. The restart and force buttons in the details dialog **run backups**: they do not restart the guest and are not read-only checks. Do not use force. A retry can also apply retention to older points.
5. Check the new run and the restore points. Then [restore a stopped copy, remove every NIC and check the sample data](/docs/xoa-hl/backup-restore/).
6. Leave the lab schedule disabled. Before you turn scheduled runs on again, note the original error, the fix, the new run and point IDs, and the restore result.

**Check:** the new run, the kept restore points and the isolated restore of the guest data all pass. If not, keep the incident open and [report a problem](#report-a-problem) with sanitized evidence.

## Check the appliance from its console {#appliance-checks}

These commands only read the state. Run them inside the appliance, not on the hypervisor host, from an authorized console or SSH session. Some of them need root privileges.

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

- A missing status file before the first check, or after a restart, is not a failure on its own.
- `systemctl status` returns a nonzero code for an inactive or failed unit. Read the state that it shows.
- The automatic update status can describe an older run. Compare its UTC times.
- For what each status means, and for update and restart decisions, see [Maintain and update the appliance](/docs/xoa-hl/maintenance/).

Do not delete database files, logs or locks to make an error go away. If the disk is full, find the files that grow and save the evidence before you choose what to clean up.

## Repair packages after an interrupted update {#interrupted-update}

Use this only when the appliance stopped during an update, for example after a power cut. Run the commands as root inside the appliance, from an authorized console or SSH session, when no update is running.

1. Check the package database. Any problem it reports, for example a duplicate package, means that the repair is needed:

   ```bash
   dnf check
   ```

2. Remove the duplicate package entries:

   ```bash
   dnf remove --duplicates
   ```

3. Check the packages of the newest kernel. A line starting with `S.5` means a damaged file:

   ```bash
   rpm -V kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
   ```

4. If a file is damaged, reinstall these three packages, then check again:

   ```bash
   dnf reinstall kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
   dnf check
   rpm -V kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
   grubby --default-kernel
   ```

5. Restart the appliance normally. Then check sign-in, the installed version and the host list.

**Check:** `dnf check` and `rpm -V` report nothing, and the appliance starts on the kernel shown by `grubby --default-kernel`. Do not trust a later update result on its own: an update run after an interruption can report success and still leave these problems.

## Recover administrator access {#recover-admin-access}

Use this when no administrator can sign in: the password is lost, the device with the one-time code is lost, or an LDAP or SAML sign-in no longer works. You run a recovery command **inside the appliance**, as root, from the appliance console or SSH. Anyone with root access to the appliance can take over an XO account this way, so protect that access.

The command changes the account you name:

- It sets a new password.
- It removes the account's one-time code.
- It makes the account an **Admin**.
- It removes the account's LDAP or SAML links, so the account becomes local.
- It keeps the account's other settings and its existing authentication tokens.

If no account has that name, the command creates a new local administrator.

1. Open the appliance console from XO Lite, or an SSH session, and become root.
2. Check that the database runs: `systemctl is-active redis` prints `active`.
3. Run the command with the account's exact username, usually an email address. You do not need to stop `xo-server`.

   ```bash
   node /opt/xo/packages/xo-server/dist/recover-account-cli.mjs admin@example.net
   ```

4. At `Password (leave empty for random):`, type the new password and press Enter. The password is not shown. If you leave it empty, the command prints a random password: store it in your password manager, then clear the screen. Do not give the password on the command line, because it would stay in the shell history.
5. Wait for `user admin@example.net has been successfully updated`. If the message says `created`, the name did not match an existing account. Once signed in, check the name in **Settings → Users** and delete the extra account if you do not need it.
6. In a new private browser window, sign in with the account and its new password. No one-time code is asked.
7. On your user page, read **Authentication tokens**. If a device or a password was lost, select **Forget all authentication tokens**. It removes every token except the one of your current session.
8. If the account used a one-time code, [set it up again](/docs/xoa-hl/sign-in-otp/) on a device you control. If it used LDAP or SAML, it is now a local account: keep it as your local recovery administrator, or ask the identity owner before you link it again.

**Check:** the account signs in with the new password, **Settings → Users** lists it as **Admin**, its **OTP** column shows **Not configured**, and only the tokens you expect remain.

| Problem | What to check |
| --- | --- |
| `node: command not found`, or `Cannot find module` | Run `rpm -q xoa-hl nodejs`, and check that the file in the command exists. Use the path exactly as shown. |
| The command waits and does not finish, or reports a Redis error | Run the [console checks](#appliance-checks) for `redis` and disk space. Do not delete database files. |
| The sign-in still fails | Check the exact username printed by the command, use a new private window, and read `journalctl -u xo-server --since '15 min ago'`. |

## Common questions {#common-questions}

**Why did host maintenance leave VMs behind, or the host disabled?** Save the task. Then check the host's actual enabled state and where each VM runs. The [host maintenance test](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) handles evacuation and re-enabling separately. A partial evacuation or an early failure needs the host owner's recovery plan. Do not bypass migration blocks, and do not repeat the toggle blindly.

**Why did a host fail to join a pool?** Save the task, the error and the inventories of both pools. The [pool join test](/docs/xoa-hl/hosts-pools/#pool-join) checks the exact IDs, patch differences, master, networks and storage before you confirm. The interface runs a forced join: do not repeat it, and do not eject a host to clear an unexplained failure.

**Why was delegated VM creation refused?** Follow the [resource set and quota test](/docs/xoa-hl/permissions/#resource-set-delegation). Compare the exact user, the selected set, the template, SR and network IDs, and the quota Used/Total. Seeing a template or a button does not prove that the server allows the action. Save the error, and look for a partial VM or disk before you retry. Do not raise quotas or grant Admin on the pool to clear an unexplained failure.

**Why are updates listed while the check command returns 100?** The packaged checker turns the `dnf check-update` exit code 100 into `AVAILABLE`, 0 into `UP_TO_DATE`, and any other code into `ERROR`. Listed updates are not a failed installation.

**Does switching to stable undo a testing update?** No. The channel chooses the repositories for later checks and installations. Switching to stable does not downgrade a version that is already installed.

**Does a pool metadata backup prove that a host can be recovered?** No. The [pool metadata test](/docs/xoa-hl/configuration-backup/#pool-metadata) checks only the export, retention and file identity. Restoring it on an isolated test pool is not covered yet.

**Can a configuration export replace a VM backup or an appliance rollback?** No. Read the [configuration scope and recovery limits](/docs/xoa-hl/configuration-backup/), and keep separate backups of your guests.

## Report a problem {#report-a-problem}

[Open an XCP-HL issue](https://github.com/Vagrantin/xcp-hl/issues/new). Give this information as text:

- The page URL and language, or the appliance route where the problem occurs.
- The image tag, the versions shown in **About**, the installed RPM and Node versions, and the stable or testing channel.
- The operation, the exact steps, the expected result and the actual error.
- The time with its time zone, the manual or automatic mode, the related service state and a sanitized log excerpt.
- Whether the problem repeats on a disposable appliance, and the last version that worked.

Remove passwords, tokens, cookies, private host names and addresses, and user or guest data from logs and screenshots. `xo-server` and first-boot logs can contain credentials. Never attach a configuration export, a TLS private key or a complete configuration file. Keep the original evidence privately.

{{< details title="Sources" closed="true" >}}
- **Release behavior**: [update scheduling](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md), [check exit codes](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh), [server service](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [first-boot provisioning](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh).
- **Backup diagnosis**: [overview and run details](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js), [task filters, pages and display](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js), [raw log and restart buttons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js), [status calculation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/backups-ng-logs.mjs), [full export and cleanup order](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [remote list errors and restore logs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js).
- **Network diagnosis**: [VM network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [host network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [pool network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [PIF carrier display](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [guest metrics and interface mapping](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [server connection state](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js).
- **Administrator recovery**: [recovery command](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [account update](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [installed path and configuration](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
{{< /details >}}
