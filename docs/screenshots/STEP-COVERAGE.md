# Screenshot coverage for XOA-HL guide steps

Source: active Hugo branch `claude/gracious-ride-99qg08` at `a7f0885` (2026-10-19). English is the source; review the FR/JA counterpart and UI for each image. This is a backlog, not evidence that captures or lab validation passed. Refresh it when the guides change.

Numbered items are inventoried below. Actionable unnumbered paragraphs and tables also need review; the VM wizard and About page are named below. Commands, secrets, guest-specific screens and browser certificate prompts may need a justified no-image decision. One approved image can cover adjacent steps when it shows their controls or result.

## Existing and prepared checkpoints

| Guide | Steps | Jenkins request / capture | State |
| --- | --- | --- | --- |
| First login | 1.1 | `xoa-first-login-offline.yaml` / `login` | Offline scene available; review image |
| First login | 2.1, 3.1–3.2 | `xoa-language-offline.yaml` or `xoa-first-login-live.yaml` / `user-language` | Offline available; live lab pending |
| First login | 4.4 | `xoa-first-login-live.yaml` / `connected-server` | Live lab pending |
| First login | About (unnumbered) | `xoa-first-login-live.yaml` / `versions` | Live lab pending |
| Create VM | 1.4 | `xoa-create-vm-live.yaml` / `installer-iso` | Live lab pending |
| Create VM | Wizard (unnumbered) | `xoa-create-vm-live.yaml` / `new-vm` | Live lab pending |
| Create VM | 3.1, 3.4 | `xoa-create-vm-live.yaml` / `guest-console`, `guest-disks` | Live lab pending; console privacy review |

The seven-capture `xoa-beginner.yaml` remains the combined lab pilot. The page-scoped requests reuse its selectors. Jenkins accepts `XCP_HL_REF=main` or a trusted PR targeting main and `REQUEST=<filename>`. Hugo `docPage` mappings require [jenkins-infra PR #117](https://github.com/Vagrantin/jenkins-infra/pull/117) deployed. Live captures require the isolated lab in [jenkins-infra #91](https://github.com/Vagrantin/jenkins-infra/issues/91). The runner does not provision, upload an ISO or submit destructive forms.

## Numbered step inventory

`requested` means a YAML capture checkpoint exists, not that a PNG is approved. `pending` requires a safe visual checkpoint or a justified no-image decision. State-changing guides require prearranged disposable fixtures; the capture observes the resulting state.

| Source | Section / step | Cue | State |
| --- | --- | --- | --- |
| `backup-restore.md` | 1 / 1 | Open Settings → Remotes (`/#/settings/remotes`). Reuse an existing suitable remote if it has been ve | pending |
| `backup-restore.md` | 1 / 2 | Choose NFS, enter the backup server and export path supplied by its administrator, and apply any req | pending |
| `backup-restore.md` | 1 / 3 | Save the remote, enable it if necessary, and use its Test your remote action. Read any connection or | pending |
| `backup-restore.md` | 2 / 1 | Open Backup → New → VMs (`/#/backup/new/vms`) and name the job `lab-first-vm-full`. | pending |
| `backup-restore.md` | 2 / 2 | Select only your test VM explicitly. Leave smart selection off so the job cannot pick up unrelated V | pending |
| `backup-restore.md` | 2 / 3 | In the backup modes, select Backup. Leave Rolling snapshot, Delta backup, Disaster recovery and Cont | pending |
| `backup-restore.md` | 2 / 4 | Select `lab-backup-nfs` under Target remotes (for export). Leave Delete first off; this option can r | pending |
| `backup-restore.md` | 2 / 5 | Add a schedule explicitly. Set Backup retention to `2` for this small lab example, choose an explici | pending |
| `backup-restore.md` | 2 / 6 | Disable that schedule in the schedule table before saving the job. This first backup/restore check r | pending |
| `backup-restore.md` | 2 / 7 | Save and check the overview: one intended VM, the intended remote and a disabled schedule. Keep adva | pending |
| `backup-restore.md` | 3 / 1 | In Backup → Overview (`/#/backup/overview`), use the run action for the job's disabled schedule. Che | pending |
| `backup-restore.md` | 3 / 2 | Wait for the run to finish. Open its logs and inspect the VM/export result, not just the fact that t | pending |
| `backup-restore.md` | 3 / 3 | Open Backup → Restore (`/#/backup/restore`). Locate the test VM and confirm that the new full backup | pending |
| `backup-restore.md` | 4 / 1 | In Backup → Restore, choose the restore action for your test VM, then select the exact full backup y | pending |
| `backup-restore.md` | 4 / 2 | Choose the writable destination SR with enough free space. This is VM-disk storage, not the NFS back | pending |
| `backup-restore.md` | 4 / 3 | Leave Start VM after restore off. Select Generate new MAC addresses to give the copy distinct virtua | pending |
| `backup-restore.md` | 4 / 4 | Confirm the restore and wait for completion. Check the restore logs for errors. Identify the new VM  | pending |
| `backup-restore.md` | 4 / 5 | Verify the restored VM is stopped. Rename this copy `lab-first-vm-restore-test` and record its UUID  | pending |
| `backup-restore.md` | 5 / 1 | Open the restored copy's Network tab (`/#/vms/restored-uuid/network`). While it is stopped, remove a | pending |
| `backup-restore.md` | 5 / 2 | Recheck the restored UUID and empty NIC table, then start this copy and open Console. Leave the orig | pending |
| `backup-restore.md` | 5 / 3 | Verify the guest boots, console login works, and the sample file has the recorded contents or checks | pending |
| `backup-restore.md` | 5 / 4 | Shut down the restored guest normally. Record the result, backup timestamp, restore duration and ver | pending |
| `backup-restore.md` | 6 / 1 | In Backup → Overview, record the job ID and copy the exact schedule ID using its clipboard button. O | pending |
| `backup-restore.md` | 6 / 2 | Choose a laboratory rule with the visual time selector and an explicit Timezone, such as `Asia/Tokyo | pending |
| `backup-restore.md` | 6 / 3 | Record the browser's timezone as well. The rule uses its selected timezone, while the preview format | pending |
| `backup-restore.md` | 6 / 4 | Keep the row Disabled in the editor and choose Save for the job. Reopen it and read back the schedul | pending |
| `backup-restore.md` | 6 / 5 | Return to Overview and enable only this schedule with its state button. This button sends the change | pending |
| `backup-restore.md` | 6 / 6 | Repeat the observations until at least three successful runs of this same schedule have completed. C | pending |
| `backup-restore.md` | 6 / 7 | Disable the exact schedule in Overview and refresh to confirm Disabled before another expected occur | pending |
| `backup-restore.md` | 6 / 8 | Select a retained point from a scheduled run and repeat sections 4–5: restore stopped, remove every  | pending |
| `backup-restore.md` | 7 / 1 | Add and test the dedicated remote as in section 1. Open Backup → New → VMs (`/#/backup/new/vms`), na | pending |
| `backup-restore.md` | 7 / 2 | Select Delta Backup only. Leave Backup, Rolling Snapshot, Disaster Recovery and Continuous Replicati | pending |
| `backup-restore.md` | 7 / 3 | In Advanced settings, set Full backup interval to `2`. Leave Use NBD to transfer disk if available a | pending |
| `backup-restore.md` | 7 / 4 | Add one schedule with Backup retention `2`, an explicit timezone and a reviewed next-run preview. Le | pending |
| `backup-restore.md` | 7 / 1 | In Backup → Restore (`/#/backup/restore`), select the exact point B on `lab-delta-nfs`. Choose a wri | pending |
| `backup-restore.md` | 7 / 2 | Leave Start VM after restore and Use differential restore off. Enable Generate new MAC addresses. Di | pending |
| `backup-restore.md` | 7 / 3 | Complete sections 4–5's isolation checks: record the new VM/disk UUIDs, confirm the copy is stopped, | pending |
| `backup-restore.md` | 7 / 4 | After run 3 and completed cleanup/merge inspection, restore the retained point B again to a new stop | pending |
| `backup-restore.md` | 8 / 1 | Open Backup → File Restore (`/#/backup/file-restore`). Locate the disposable VM, then open its file- | pending |
| `backup-restore.md` | 8 / 2 | Choose the exact point B by timestamp and job, then its expected disk. Wait for the partition scan;  | pending |
| `backup-restore.md` | 8 / 3 | Browse from `/` through the folders to the version-B sample and select that file only. Avoid the sel | pending |
| `backup-restore.md` | 8 / 4 | On the workstation, record the archive filename, size and SHA-256. Inspect its entries, extract only | pending |
| `backup-restore.md` | 9 / 1 | In Backup → New → VMs (`/#/backup/new/vms`), make a new job `lab-dr-full` with this VM selected expl | pending |
| `backup-restore.md` | 9 / 2 | Add one schedule with Replication retention `2`, explicit timezone and a reviewed next-run preview.  | pending |
| `backup-restore.md` | 9 / 3 | With the original guest normally stopped after writing A, run the job once from Backup → Overview. C | pending |
| `backup-restore.md` | 9 / 4 | Select the retained B replica, not the source VM, C replica or an NFS restore point. Make a uniquely | pending |
| `backup-restore.md` | 10 / 1 | In Settings → Remotes (`/#/settings/remotes`), create `lab-backup-smb` with type SMB. The Address\\S | pending |
| `backup-restore.md` | 10 / 2 | Use Test your remote on this exact enabled remote. It writes and reads a 10 MiB random test file, co | pending |
| `backup-restore.md` | 10 / 3 | In Backup → New → VMs (`/#/backup/new/vms`), create a separate `lab-smb-full` job: select only the s | pending |
| `backup-restore.md` | 10 / 4 | Run this new disabled schedule manually once in Backup → Overview. Check the per-VM export and remot | pending |
| `backup-restore.md` | 10 / 5 | Restore the exact SMB point to the reserved writable SR with Start VM after restore off. Record the  | pending |
| `configuration-backup.md` | 1 / 1 | In the browser, sign in as an XO administrator. Record the installed versions. | pending |
| `configuration-backup.md` | 1 / 2 | Open Settings → Config (`/#/settings/config`) and choose Download config under Export config. Labels | pending |
| `configuration-backup.md` | 1 / 3 | Enter a unique passphrase and confirm. Leaving it empty produces an unencrypted export. Store the pa | pending |
| `configuration-backup.md` | 1 / 4 | Allow the download if the browser blocks the new window. Check that a nonempty file was saved: this  | pending |
| `configuration-backup.md` | 1 / 5 | Move the file to protected storage outside the appliance. Record date, file size, versions and encry | pending |
| `configuration-backup.md` | 2 / 1 | Record the fresh appliance state and prepare credentials from the exported configuration; the import | pending |
| `configuration-backup.md` | 2 / 2 | Open Settings → Config, select or drop the export file, then choose Import config and supply the exp | pending |
| `configuration-backup.md` | 2 / 3 | On success, sign out and test an exported administrator login. Compare users, permissions, remotes,  | pending |
| `configuration-backup.md` | 2 / 4 | Disable imported schedules and remove or replace production destinations before allowing access to d | pending |
| `configuration-backup.md` | 2 / 5 | On failure, record the error and sanitized `xo-server` logs. Discard the disposable appliance and st | pending |
| `configuration-backup.md` | 3 / 1 | In Backup → New → Metadata (`/#/backup/new/metadata`), name a new job `lab-pool-metadata`. Enable Po | pending |
| `configuration-backup.md` | 3 / 2 | Run that job manually using its saved schedule three times at distinct recorded times, A/B/C. Wait f | pending |
| `configuration-backup.md` | 3 / 3 | In Backup → Restore → Metadata (`/#/backup/restore/metadata`), inspect pool entries from enabled rem | pending |
| `configuration.md` | Inventory the HTTPS certificate before rotation {#tls-certificate-preflight} / 1 | With an independent console and local administrator available, identify the installed image/package, | pending |
| `configuration.md` | Inventory the HTTPS certificate before rotation {#tls-certificate-preflight} / 2 | On the appliance, inspect only metadata for the configured certificate, key and marker. For the ship | pending |
| `configuration.md` | Inventory the HTTPS certificate before rotation {#tls-certificate-preflight} / 3 | From an approved client, inspect the actual HTTPS endpoint and a fresh browser login. Where OpenSSL  | pending |
| `configuration.md` | Inventory the HTTPS certificate before rotation {#tls-certificate-preflight} / 4 | Before scheduling any rotation, have the certificate and appliance owners identify the replacement c | pending |
| `create-vm.md` | 1 / 1 | In XOA-HL, open Import → Disk (`/#/import/disk`). Leave From URL off to upload the file you download | pending |
| `create-vm.md` | 1 / 2 | Select the ISO SR, for example `XCP-HL ISO library` when present. Drop the `.iso` file into the uplo | pending |
| `create-vm.md` | 1 / 3 | Check the filename and destination, select Import, and wait for the operation to finish. | pending |
| `create-vm.md` | 1 / 4 | Check the destination SR's disks list for the ISO. Do not proceed with an incomplete upload. | requested: installer-iso |
| `create-vm.md` | 3 / 1 | Open the new VM, check its name, and start it. Open its Console tab. | requested: guest-console |
| `create-vm.md` | 3 / 2 | Confirm the selected installer starts. Follow your OS vendor's installation instructions inside this | pending |
| `create-vm.md` | 3 / 3 | When the installer asks for a target disk, check it is the new VM's virtual disk. The example create | pending |
| `create-vm.md` | 3 / 4 | After installation, use the VM's Disks tab to eject the installer ISO from the virtual CD drive. Reb | requested: guest-disks |
| `first-login.md` | 1 / 1 | Open `https://appliance-address`, replacing the placeholder with the address assigned during deploym | requested: offline login |
| `first-login.md` | 1 / 2 | If the browser reports a self-signed certificate, verify the address belongs to your appliance befor | pending |
| `first-login.md` | 1 / 3 | Wait for first-boot provisioning to finish, then sign in with the XO administrator credentials from  | pending |
| `first-login.md` | 2 / 1 | Select the user icon in the navigation to open User (`/#/user`). | requested: user-language |
| `first-login.md` | 2 / 2 | In the password section, enter the current password, a new unique password and its confirmation. Sel | pending |
| `first-login.md` | 2 / 3 | Store the new password, sign out, and confirm you can sign in again with the same web login and the  | pending |
| `first-login.md` | 3 / 1 | Open the user icon → User → Language. | requested: user-language |
| `first-login.md` | 3 / 2 | Select English, Français or 日本語. Confirm the interface labels change. | requested: user-language |
| `first-login.md` | 4 / 1 | Open Settings → Servers (`/#/settings/servers`). If the intended server is already listed and connec | pending |
| `first-login.md` | 4 / 2 | In the connection form, enter a descriptive label, the host management IP address or hostname, usern | pending |
| `first-login.md` | 4 / 3 | Select Connect. If the connection reports a self-signed certificate, first verify the host identity, | pending |
| `first-login.md` | 4 / 4 | Check the connection row for an error indicator. Open the inventory and confirm the intended pool, h | requested: connected-server |
| `guest-tools.md` | 1 / 1 | In the browser, select the recorded VM UUID and confirm Running. Open General (`/#/vms/vm-uuid/gener | pending |
| `guest-tools.md` | 1 / 2 | In that VM's console, collect the following. An absent package or inactive service is a finding to r | pending |
| `guest-tools.md` | 2 / 1 | Refresh the guest's approved package indexes and inspect the candidate and simulated transaction: | pending |
| `guest-tools.md` | 2 / 2 | Confirm the candidate comes from the expected Ubuntu Noble repository. The source-reviewed package i | pending |
| `guest-tools.md` | 2 / 3 | Install interactively, read the proposed transaction, then start and enable the packaged service: | pending |
| `guest-tools.md` | 3 / 1 | Refresh the same running VM's General and Advanced pages. Record the tools message, reported agent v | pending |
| `guest-tools.md` | 3 / 2 | Compare any reported IP with the intended guest interface and its current address. No IPv4 record al | pending |
| `guest-tools.md` | 3 / 3 | Save all guest work. In the browser, recheck the VM UUID and use its ordinary Stop action once, read | pending |
| `guest-tools.md` | 3 / 4 | Verify the console shuts down and XOA-HL reaches Halted, with no active stop task. Start this test V | pending |
| `hosts-pools.md` | 2 / 1 | Arrange a window, finish active management/backup tasks and record the old owner's connections, sche | pending |
| `hosts-pools.md` | 2 / 2 | Disable the old owner's relevant schedules. In its Settings → Servers, remove the connection for the | pending |
| `hosts-pools.md` | 2 / 3 | Add the host/pool connection on the new appliance. Check connected inventory and intended permission | pending |
| `hosts-pools.md` | 2 / 4 | Confirm the old owner no longer reconnects or runs jobs against the pool. Enable only the intended n | pending |
| `hosts-pools.md` | 5 / 1 | Start with Last 10 minutes, the default. Record the selected range, current time, browser time zone, | pending |
| `hosts-pools.md` | 5 / 2 | Compare a wider range using the selector. The reviewed backend requests AVERAGE samples; a long-rang | pending |
| `hosts-pools.md` | 5 / 3 | Leave Stacked values off for an initial per-series reading, then compare it deliberately if needed.  | pending |
| `hosts-pools.md` | 5 / 4 | Record a baseline during a known normal workload, then compare a known activity period using the sam | pending |
| `hosts-pools.md` | 6 / 1 | In the XOA-HL browser, check Settings → Servers for one working connection to each single-host pool. | pending |
| `hosts-pools.md` | 6 / 2 | On the target pool page (`/#/pools/target-pool-id/general`), identify the master and open Add hosts. | pending |
| `hosts-pools.md` | 6 / 3 | After the preflight record and an approved window, confirm the exact target pool and source host in  | pending |
| `hosts-pools.md` | 6 / 4 | Refresh the target connection. Check that the target pool ID and master remain the intended ones, ex | pending |
| `hosts-pools.md` | 7 / 1 | In XOA-HL, record the pool/master and both host IDs, versions/patch levels, enabled and power states | pending |
| `hosts-pools.md` | 7 / 2 | Open the source host’s Advanced tab (`/#/hosts/source-host-id/advanced`). With the exact host and po | pending |
| `hosts-pools.md` | 7 / 3 | Wait for the task result, then refresh both host and VM inventories. Confirm the source is disabled, | pending |
| `hosts-pools.md` | 7 / 4 | After the successful readback and before any separate update, select Disable maintenance mode on tha | pending |
| `hosts-pools.md` | 8 / 1 | In XOA-HL, record the exact pool/master and three host IDs, host releases, management addresses and  | pending |
| `hosts-pools.md` | 8 / 2 | Open the pool Advanced tab (`/#/pools/pool-id/advanced`) and inspect Heartbeat SR and High Availabil | pending |
| `hosts-pools.md` | 8 / 3 | Only in an owner-approved lab window with every precondition met, select the recorded SR and confirm | pending |
| `hosts-pools.md` | 8 / 4 | With the pool healthy and the observation recorded, confirm Disabling high availability once in the  | pending |
| `permissions.md` | 6 / 1 | Open Settings → Groups (`/#/settings/groups`). Enter a distinct name such as `lab-vm-viewers` in New | pending |
| `permissions.md` | 6 / 2 | In Settings → ACLs, select only this group as the subject, only the test VM as the object and Viewer | pending |
| `permissions.md` | 6 / 3 | Back in Groups, select only the intended user in that group's Add user column. Selecting the user se | pending |
| `permissions.md` | 6 / 4 | Refresh or sign in again as the member. Verify the VM can be read, while start/stop and administrati | pending |
| `permissions.md` | 6 / 5 | In Groups, expand the member list and use the remove icon next to the exact test login. This sends r | pending |
| `permissions.md` | 7 / 1 | As administrator in the XOA-HL browser, choose one disposable pool, one stopped, known template, one | pending |
| `permissions.md` | 7 / 2 | Open Self service → Resource sets (`/#/self`). Choose New, give the set a unique lab name, select on | pending |
| `permissions.md` | 7 / 3 | Reload the set as administrator. Check its ID, subject, pool-derived template/SR/network objects, ho | pending |
| `permissions.md` | 7 / 4 | In the separate normal-user browser, open New VM (`/#/vms/new`) and select the exact resource set. R | pending |
| `permissions.md` | 7 / 5 | Request one VM within every limit, using only the selected objects. Leave it stopped and remove or d | pending |
| `permissions.md` | 7 / 6 | As administrator, remove the test user from the set and refresh the normal-user session. Verify it c | pending |
| `permissions.md` | 8 / 1 | As the administrator, record the appliance image/package/XO versions, the effective authentication s | pending |
| `permissions.md` | 8 / 2 | During an approved lab window, enter only the owner-provided URI, CA path, certificate checking enab | pending |
| `permissions.md` | 8 / 3 | Do not use Test as a harmless connection probe: the LDAP plugin's test calls its authentication path | pending |
| `permissions.md` | 8 / 4 | Grant that test account Viewer on only one disposable VM as in section 3. In the external session, v | pending |
| `permissions.md` | 8 / 5 | Remove only the test ACLs and any test membership, then sign out the external session. In this isola | pending |
| `permissions.md` | 9 / 1 | With the IdP owner, record the installed image/package/XO and plugin versions, effective authenticat | pending |
| `permissions.md` | 9 / 2 | Register only this lab service provider with the IdP. Its assertion consumer/callback URL must match | pending |
| `permissions.md` | 9 / 3 | Enter only the lab certificate, entry point, issuer, username field and any owner-approved callback/ | pending |
| `permissions.md` | 9 / 4 | From the retained administrator session, read back the new XO user ID, `saml` provider binding, norm | pending |
| `permissions.md` | 9 / 5 | Sign out the SAML test session, remove test ACLs, then unload only the isolated `auth-saml` plugin a | pending |
| `sign-in-otp.md` | 2 / 1 | Sign in as the account to protect. Open your user page with the user icon in the menu (`/#/user`). | pending |
| `sign-in-otp.md` | 2 / 2 | Find the OTP authentication toggle. If it is missing, stop and record the installed version; the rev | pending |
| `sign-in-otp.md` | 2 / 3 | Scan the QR code, or type the secret, in the authenticator app. The enrollment entry is issued by `X | pending |
| `sign-in-otp.md` | 2 / 4 | Type the current code in OTP code and confirm. A wrong code reopens the dialog; type the code curren | pending |
| `sign-in-otp.md` | 2 / 5 | After success, the user page keeps showing the secret and its QR code next to the toggle. Anyone who | pending |
| `sign-in-otp.md` | 3 / 1 | Keep the current session open. Open a private browser window and sign in with the username and passw | pending |
| `sign-in-otp.md` | 3 / 2 | A second page asks for a Code. Type the current code from the app and select Sign in. This page is i | pending |
| `sign-in-otp.md` | 3 / 3 | A wrong or expired code shows `Invalid code`. Wait for the next code and try again. | pending |
| `sign-in-otp.md` | 3 / 4 | Check that the expected account is signed in, then close the private window. | pending |
| `storage-networks.md` | 2 / 1 | Confirm the test VM is stopped. Open Disks (`/#/vms/id/disks`) and select New disk. | pending |
| `storage-networks.md` | 2 / 2 | Select the intended writable SR in the same pool, a clear test name and a small size with explicit u | pending |
| `storage-networks.md` | 2 / 3 | Verify the new row's name, size, SR and attachment to the intended VM. Record its identity and check | pending |
| `storage-networks.md` | 5 / 1 | As an administrator, open New → Storage (`/#/new/sr`). Choose a host in the intended pool. Enter a d | pending |
| `storage-networks.md` | 5 / 2 | Under ISO SR, select NFS ISO. Do not select NFS in the VDI SR group: that creates VM-disk storage. L | pending |
| `storage-networks.md` | 5 / 3 | Enter the NFS server in Server. Select the NFS version agreed with the storage administrator (the fo | pending |
| `storage-networks.md` | 5 / 4 | Select the exact export in Path. Use the export root for this pilot; subdirectory setup is outside i | pending |
| `storage-networks.md` | 5 / 5 | In Summary, review the name and selected type (`nfsiso`). Recheck the host selection and the actual  | pending |
| `storage-networks.md` | 6 / 1 | Open New → Storage (`/#/new/sr`), select a host in the intended pool and enter a distinct name such  | pending |
| `storage-networks.md` | 6 / 2 | Enter Server, choose the agreed NFS version (default, `4` or `4.1`) and use the server search icon.  | pending |
| `storage-networks.md` | 6 / 3 | Select the exact export root in Path, leave the subdirectory unused and wait for the probe. Inspect  | pending |
| `storage-networks.md` | 6 / 4 | In Summary, check name, type `nfs` and path. Recheck the host, server, version and options in the ea | pending |
| `storage-networks.md` | 6 / 5 | Record the resulting SR UUID. On General (`/#/srs/id/general`), check `Type: nfs`, size, used/free c | pending |
| `storage-networks.md` | 7 / 1 | Sign in as an administrator, open New → Network (`/#/new/network`) and select the disposable pool. T | pending |
| `storage-networks.md` | 7 / 2 | Under Info → Interface, explicitly select the recorded spare PIF on the pool master. The selector fi | pending |
| `storage-networks.md` | 7 / 3 | Enter a distinct Name and Description identifying the lab purpose. Set MTU to `1500` and VLAN to the | pending |
| `storage-networks.md` | 7 / 4 | Review pool, master PIF, VLAN, MTU and both type toggles, then choose Create network once. Wait for  | pending |
| `templates.md` | 1 / 1 | Recheck the working copy's UUID, Halted state, empty NIC list and recorded disks. Give it a unique n | pending |
| `templates.md` | 1 / 2 | Open its Advanced tab (`/#/vms/copy-uuid/advanced`) and choose Convert to template. This button is d | pending |
| `templates.md` | 1 / 3 | Confirm once and wait for completion. Open Home and select the Template object type (`/#/home?t=VM-t | pending |
| `templates.md` | 2 / 1 | Open New → VM (`/#/vms/new`), choose the same pool and select the recorded custom template. Use a di | pending |
| `templates.md` | 2 / 2 | Review CPU/RAM and the existing template disks, their sizes and writable destination SRs. Keep the e | pending |
| `templates.md` | 2 / 3 | In Interfaces, remove every proposed interface and check that the list is empty. A template with no  | pending |
| `templates.md` | 2 / 4 | In Advanced, clear Boot VM after creation and leave automatic power-on off. In Summary, clear Fast c | pending |
| `templates.md` | 2 / 5 | Wait, refresh and record the new VM UUID. Before any start, verify Halted, an empty Network tab, exp | pending |
| `templates.md` | 3 / 1 | Start only `lab-template-test-1` after the isolation readback. Use its console to verify guest boot/ | pending |
| `templates.md` | 3 / 2 | Repeat section 2 from the same template as `lab-template-test-2`, reviewing every setting again. Ver | pending |
| `templates.md` | 3 / 3 | Record both VM/VDI inventories, template UUID, guest results and installed release identities. Leave | pending |
| `troubleshooting.md` | Diagnose network connectivity {#network-connectivity} / 1 | Record the VM UUID, power state, resident host and pool. Open its network tab (`/#/vms/id/network`). | pending |
| `troubleshooting.md` | Diagnose network connectivity {#network-connectivity} / 2 | Connected reflects VIF attachment. A stopped VM's detached VIF is not evidence of a fault. IP addres | pending |
| `troubleshooting.md` | Diagnose network connectivity {#network-connectivity} / 3 | Record the locking-mode indicator and Allowed IPs separately from reported IPs. These are traffic-po | pending |
| `troubleshooting.md` | Diagnose network connectivity {#network-connectivity} / 4 | In the pool network row, expand PIFs and find the resident host. The row's VLAN summary uses the mas | pending |
| `troubleshooting.md` | Diagnose network connectivity {#network-connectivity} / 5 | Read attachment and carrier separately. The host's Connected button reflects PIF attachment; the sep | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 1 | Open Backup → Overview (`/#/backup/overview`) and find the job. Inspect the Logs table below it. Cle | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 2 | Select the run's status button to open its details. Record the run `id`, `jobId`, `scheduleId`, star | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 3 | Clear the detail search and select all task statuses. Inspect every page of VM tasks: the dialog can | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 1 | If future triggers need to be paused, disable the exact lab schedule in Overview and refresh to veri | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 2 | Resolve the identified access/capacity/selection problem with its owner and read back the job, sched | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 3 | Once no run is active and the state is understood, use the tutorial's ordinary manual run for this o | pending |
| `troubleshooting.md` | Diagnose a failed full-NFS backup {#backup-failures} / 4 | Inspect the new run and restore-point inventory, then restore a stopped copy, remove every NIC and c | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 1 | Open the intended VM's Console tab (`/#/vms/id/console`) and confirm its identity and Running state. | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 2 | Wait for the expected guest screen. Identify the guest's login/installer or known application before | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 3 | On a large desktop, the scale controls start at 100% and change the browser display, not the guest's | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 4 | When finished, navigate away from the console and record the VM/host IDs, power state and what passe | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 1 | Not Running or console disabled: read the VM state/message first. A Running VM with `disable_pv_vnc= | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 2 | Connection never opens or repeatedly drops: verify the signed-in account has VM operate permission a | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 3 | Connection opens but the picture is blank or stale: verify the selected VM, expected boot/display an | pending |
| `vm-operations.md` | Open and check a VM console {#vm-console} / 4 | Picture works but input/clipboard does not: move the pointer into/out of the canvas and repeat the h | pending |
| `vm-operations.md` | 3 / 1 | In the guest, create a harmless file containing `snapshot-A` and record its checksum. Shut down clea | pending |
| `vm-operations.md` | 3 / 2 | Check every disk's name. This source can exclude a VDI whose name contains the literal `[NOSNAP]`; t | pending |
| `vm-operations.md` | 3 / 3 | Open Snapshots (`/#/vms/id/snapshots`) and select New snapshot once. This per-VM button creates the  | pending |
| `vm-operations.md` | 3 / 4 | Wait, refresh and identify the new row by its Creation date and the row's UUID-copy action. Record t | pending |
| `vm-operations.md` | 4 / 1 | Start the isolated test VM, change the file to `snapshot-B`, record its new checksum, then shut down | pending |
| `vm-operations.md` | 4 / 2 | In Snapshots, select Revert VM to this snapshot for that row. Read the Revert your VM confirmation.  | pending |
| `vm-operations.md` | 4 / 3 | Confirm once and wait. Refresh and record the selected snapshot UUID, new pre-revert snapshot UUID,  | pending |
| `vm-operations.md` | 4 / 4 | Confirm Halted and an empty VIF list before manually starting the VM. If a VIF reappears, remove it  | pending |
| `vm-operations.md` | 4 / 5 | Boot through the console. Verify `snapshot-A` and its original checksum, guest disks and application | pending |
| `vm-operations.md` | 5 / 1 | Use one disposable VM with ordinary attached disks and no shared disks or passthrough devices. While | pending |
| `vm-operations.md` | 5 / 2 | Identify a different writable VM-disk SR in the same pool. Check its ID, free capacity and access fr | pending |
| `vm-operations.md` | 5 / 3 | On the source VM, choose Copy. In Copy VM, set Name to a unique test name such as `lab-vm-full-copy` | pending |
| `vm-operations.md` | 5 / 4 | Confirm once and wait for the task. Refresh inventory and identify the new VM by its distinct ID and | pending |
| `vm-operations.md` | 5 / 5 | Keep the new VM stopped while you remove every inherited VIF. Read back an empty VIF list before the | pending |
| `vm-operations.md` | 5 / 6 | Shut down the copy after the check. Record the result and use section 7 to remove only the positivel | pending |
| `vm-operations.md` | 6 / 1 | Open Advanced (`/#/vms/id/advanced`) and note CPU limits and Memory limits (min/max). The CPU row sh | pending |
| `vm-operations.md` | 6 / 2 | Open General (`/#/vms/id/general`). Click the CPU count, enter the intended positive whole number an | pending |
| `vm-operations.md` | 6 / 3 | Click the memory value and use its size/unit control for the intended amount; press Enter. This disp | pending |
| `vm-operations.md` | 6 / 4 | Refresh General and Advanced and record all resulting values. CPU count must not exceed its maximum. | pending |
| `vm-operations.md` | 6 / 5 | Start the test VM and check its console, guest-visible CPU/memory and application health. If it will | pending |
| `vm-operations.md` | 7 / 1 | Confirm that the target is the disposable VM, not the appliance, original guest, template or another | pending |
| `vm-operations.md` | 7 / 2 | Shut down the guest normally and confirm Halted. The deletion backend can hard-shut down a VM that i | pending |
| `vm-operations.md` | 7 / 3 | Open Advanced and choose Remove. Read the VM/disk warning and confirm only this intended target. If  | pending |
| `vm-operations.md` | 7 / 4 | Wait, then refresh the VM, snapshot and SR disk inventories. Check the recorded IDs and the deletion | pending |
| `vm-operations.md` | 7 / 5 | Confirm that the original VM, other guests and any required independent backup remain usable. Reconc | pending |
| `vm-transfer.md` | 2 / 1 | Open the VM and choose Migrate. It is offered for running and halted VMs, not for suspended or pause | pending |
| `vm-transfer.md` | 2 / 2 | In Migrate VM, use Select a destination host: to pick another host of the same pool. The list exclud | pending |
| `vm-transfer.md` | 2 / 3 | Read the storage section. If every disk is on a shared SR, no SR is required. Otherwise, XO requires | pending |
| `vm-transfer.md` | 2 / 4 | Select a migration network: is optional within a pool. XO preselects the pool's configured migration | pending |
| `vm-transfer.md` | 2 / 5 | Confirm and wait for the task to finish. Do not click again while the migration is pending. | pending |
| `vm-transfer.md` | 2 / 6 | Refresh the VM's General tab. Check the host, power state, console, guest network and application. A | pending |
| `vm-transfer.md` | 3 / 1 | Shut down the guest cleanly and confirm Halted. Record the VM ID, name, disks and their total size. | pending |
| `vm-transfer.md` | 3 / 2 | Choose Export. Keep Type set to `xva`. Keep Compression set to Disabled, the default. The other choi | pending |
| `vm-transfer.md` | 3 / 3 | Confirm. Download VM shows a download link, OK and Cancel. The link and OK open the same URL, which  | pending |
| `vm-transfer.md` | 3 / 4 | The browser saves a file named `date - VM name.xva`. Keep the download running until it ends; cancel | pending |
| `vm-transfer.md` | 3 / 5 | On the computer running the browser, record a checksum of the file, for example `sha256sum "file.xva | pending |
| `vm-transfer.md` | 4 / 1 | Open Import  VM (`/#/import/vm`). The menu entry appears only when you can operate at least one pool | pending |
| `vm-transfer.md` | 4 / 2 | Choose the target pool in To Pool:. To SR: proposes the pool's default SR. Choose a writable SR with | pending |
| `vm-transfer.md` | 4 / 3 | Drop the `.xva` file on the area marked Drop OVA or XVA files here to import Virtual Machines. Check | pending |
| `vm-transfer.md` | 4 / 4 | Select Import and keep the browser tab open until the upload ends. For a single file, XO opens the n | pending |
| `vm-transfer.md` | 4 / 5 | Keep the imported VM stopped. Record its ID: it is a different object from the source VM even when t | pending |
| `vm-transfer.md` | 4 / 6 | Before the first start, open Network and remove every virtual interface or arrange verified external | pending |
| `vm-transfer.md` | 4 / 7 | Start the copy and check its console and the recorded test data. | pending |
| `vm-transfer.md` | 5 / 1 | Remove the imported test VM with the disposable VM removal procedure. | pending |
| `vm-transfer.md` | 5 / 2 | Delete the XVA file from the computer and from any temporary location. | pending |
| `vm-transfer.md` | 5 / 3 | Confirm the source VM is still present, on the expected host, with its disks and data unchanged. | pending |

Inventory: 241 numbered items across 14 pages. Unnumbered UI actions, results and justified exceptions remain editorial work; this record does not mark them complete.

## Review and publication

For each approved PNG, record the Jenkins build URL, request commit, image SHA-256, target, release/UI version, fixture, locale, reviewer and guide location. Review masks, Japanese glyphs, labels, alt text and localized caption. Integrate approved images in a separate Hugo PR. An offline scene must remain visibly labelled simulated and cannot represent live host or guest success.
