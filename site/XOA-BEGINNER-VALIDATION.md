# Beginner journey validation — D2 #197

The `first-login`, `create-vm` and `backup-restore` tutorials are source-reviewed previews, not a
completed appliance acceptance report. FR/JA remain draft translations. No
appliance screenshots or lab results have been fabricated.

## Source scope reviewed on 2026-10-11

- Released image: [`xoa-image-20261009-5f33c81`](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261009-5f33c81),
  asset `XOA-hl.xva`, published 2026-10-09.
- Image build source: `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4`.
  Credential provisioning applies deployment values and documents the bootstrap
  fallback. HTTPS, separate `xo` SSH account and the image release stamp are
  present in that source.
- Application source: `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19`.
  `UPSTREAM_XO` pins XO 5.113.2 at
  `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`.
- All 14 patches applied successfully in their build-script order to a fresh
  scratch copy of the pinned upstream tree on 2026-10-11. Reviewed the resulting
  menu, User, Servers, disk-import, new-VM, Console, Disks, About, NFS remote
  creation/test, full backup, schedule/manual run, restore and NIC removal controls.
  This checks source applicability; it does not build or run the appliance.

The image tag does not establish which application package is currently
installed after updates. Do not replace these pins with an upstream XO 6 guide.
Release asset metadata retrieved on 2026-10-11:

| Released artifact | Identity / published SHA-256 |
| --- | --- |
| XVA | `XOA-hl.xva`, image `xoa-image-20261009-5f33c81`; `a9b621ce71c56445bb3998fe418cc5079c32340477a7a2830a3ef19609cfff0b` |
| Application RPM | `xoa-hl-5.113.2_e281c536-38.g5f33c81.xcpng8.3.el9.x86_64.rpm`, release `v5.113.2_e281c536-ce38`; `3e85d7688664dfd55426b1d5f7e88e692c17fc4bb75d4dce31e58b9b0095bc7a` |

These are published metadata, not hashes calculated from downloaded payloads.
The RPM release names the same application commit as the image release. That
association does not prove the installed image's RPM NEVRA; record `rpm -q xoa-hl`
on the **appliance**, with authorization, during the lab run. The shared release
matrix remains publisher-owned; this batch does not modify its inputs.

The first backup uses a stopped guest and a separately administered NFS export.
The restore remains stopped until all VIFs are removed, then boots only through
its console. This avoids relying on a generated MAC or a runtime disconnected
flag as an isolation guarantee. Snapshot consistency, incremental chains,
replication, encryption, file restore and appliance-configuration recovery are
outside this beginner pilot. Do not infer their validation from these sources.

## Disposable-lab record to complete

Use a new test appliance and a VM containing no important data. Keep host
management connectivity independent of test guest networking. An operator with
authorized lab access must fill this record; documentation CI cannot supply it.

| Identity | Observed value |
| --- | --- |
| Operator / date | Pending |
| Host ISO/release, installed host packages | Pending |
| Deployed image tag / asset checksum | Pending |
| About: XOA-HL application version | Pending |
| About: XOA-HL VM version | Pending |
| Browser/version, UI language | Pending |
| Guest OS ISO/version/checksum, template | Pending |
| ISO SR, VM-disk SR, guest network | Pending; use anonymized identifiers |
| Installed application RPM NEVRA | Pending |
| NFS server/export and free capacity | Pending; anonymize identifiers |
| Backup job/schedule/timezone/retention | Pending |
| Backup timestamp and original/restored VM UUIDs | Pending |
| Sample file checksum and restore duration | Pending |

| Check | Expected result | Status |
| --- | --- | --- |
| Deploy through XO Lite | Appliance receives intended network and credentials | Pending |
| Log in with deployment web credentials | XO interface opens; host root/SSH accounts are not used | Pending |
| Change password and log in again | New password works with the same web login | Pending |
| Change UI language EN/FR/JA | User settings and task labels match localized instructions | Pending |
| Connect host | Inventory shows intended host, pool and SRs without connection error | Pending |
| Inspect About | Both application and image version values recorded | Pending |
| Import verified ISO | Completed ISO visible in the intended ISO SR | Pending |
| Create one test VM | Chosen template/resources/storage/network match summary | Pending |
| Install OS through guest console | Installation completes on the new virtual disk only | Pending |
| Eject ISO and reboot guest | Installed OS boots and console login succeeds | Pending |
| Check guest networking | Expected IP/gateway/DNS/connectivity | Pending |
| Prepare stopped guest / sample | Sample file flushed, checksum recorded; guest stopped normally | Pending |
| NFS remote access | Separate storage; enable/test succeeds; no remote error | Pending |
| Manual full backup | One explicit VM, full mode, retention 2, disabled schedule; successful VM/export logs | Pending |
| Discover backup | Expected timestamp and remote in Restore | Pending |
| Restore stopped copy | Correct writable SR, auto-start off, distinct UUID; logs successful | Pending |
| Isolate before boot | Copy stopped, all VIFs removed, NIC table empty | Pending |
| Validate restored data | Console boot/login, recorded file/checksum matches; original untouched | Pending |
| Cleanup / schedule | Only restored test UUID/disks removed; lab schedule remains disabled | Pending |

Do not deliberately break credential provisioning on a live appliance to
exercise the fallback. If an authorized isolated failure test is performed,
record exactly which first-boot stage failed; the source's fallback warning is
not proof that every partial failure preserves both default credentials.

Capture only the screens that clarify a task, using the lab appliance itself.
Each capture needs image/application versions, UI language, capture date,
localized caption and alt text. Remove credentials and identifying network
data. Reuse a capture across locales only when its labels remain understandable.

## Lab run 2026-10-27 (ce47, release-identified)

Browser steps were driven with Playwright 1.63 (Chromium) from the Jenkins docs-ui image, signed in as a reader would. A few steps used the same API call that the button sends; they are marked "(API)".

Findings filed during this run: #305 (Jenkins docs agents), #306 (interrupted update, rerun reports success), #307 (updater status gaps), #308 (appliance details), #309 (API inventory visibility), #310 (SSH password in xenstore), #311 (default admin after unclean shutdown). A finding keeps its scenario open until it is fixed or accepted; a failed or untested row is not a pass.

| Identity | Observed value |
| --- | --- |
| Host | nested lab host, XCP-HL v8.3-ce44 (8.3.0), XO Lite `xo-lite-ce-0.21.0`; memory raised to 6 GiB for this run (baseline 3 GiB) |
| Deployed image | "XOA HomeLab Edition (latest build)" = `xoa-image-20261027-ca44911` |
| About: XOA-HL application version | `5.113.2_e281c536-47.gca44911.xcpng8.3.el9` |
| About: XOA-HL VM version | `built 2026-10-27, commit ca44911, release v5.113.2_e281c536-ce47` |
| Installed application RPM | `xoa-hl-5.113.2_e281c536-47.gca44911.xcpng8.3.el9.x86_64` |
| Browser / language | Chromium (Playwright 1.63), en-US |
| Guest ISO | `alpine-virt-3.24.3-x86_64.iso`, 70,254,592 B, SHA-256 `cdc1bc0efc64d8d611bf3733f54868172a545888dfd726f518bf279bcb0ff1af` (matches the published value and the stored SR file); template "Other install media" |
| ISO SR / VM-disk SR / network | XCP-HL ISO library (local ISO SR) / Local storage / Pool-wide network 0 |
| NFS server / export | disposable lab NFS VM, `/srv/docs-backup`, 38 GB free, export restricted to the two lab appliances |
| Backup job | `beginner-full`, full, one explicit VM, retention 2, schedule `0 1 * * *` Asia/Tokyo **disabled** |
| Backup timestamp | `20261027T040818Z`, 636,396,032 B |
| Original / restored VM UUIDs | `5a7c4a3a-...` / `5342fc28-...` (distinct) |
| Sample files | `sample.bin` (5 MB random) `71c234c884c35a9c...29b51090`, `sample.txt` `30410c13597d1780...e2535a4e` |
| Restore duration | backup run 15 s; restore (import) under 1 min |

| Check | Expected | Actual | Status |
| --- | --- | --- | --- |
| Deploy through XO Lite | Appliance gets intended network and credentials | "Deploy XOA" form: latest XOA-HL image, Local storage, Pool-wide network 0, static IP/netmask/gateway/DNS, admin login, SSH account; "Importing XOA..." about 5 min, "Waiting for XOA to respond...", "XOA deployment successful!" at 6 min. VM on intended SR/network, 2 GiB; static address, gateway and DNS exactly as entered | Pass |
| Deploy: button availability | n/a | "Deploy XOA" only appears when the pool has no `xo:clientInfo` mark; on a host already used by an appliance, the button is "Access XOA" | Note for the guide |
| Deploy: VM name and hostname | Recognizable | VM named `qa-xoa-build-58` (the image's build name); guest hostname `localhost.localdomain` | Finding (minor) |
| Deploy: credentials in VM metadata | Removed after first boot | `xenstore-data` keeps `vm-data/system-account-xoa-password` in **plaintext** (#310) | Finding (security) |
| Deploy: "Learn more" links | Point to the manual | Point to docs.xen-orchestra.com (Vates) | Note |
| Log in with deployment web credentials | XO opens; host root/SSH not used | Signed in as the deployment admin (admin permission); only that user exists; SSH key login refused for root and `xo`; `xo` SSH works with the deploy-form password; `/root` not readable by `xo` | Pass |
| Change password and log in again | New password works | Old password refused (`invalid credentials`), new password accepted (API `user.changePassword`) | Pass |
| Change UI language EN/FR/JA | Labels match | Not repeated here; covered by the EN/FR/JA capture requests (docs/screenshots) | Not tested in this run |
| Connect host | Inventory shows host, pool and SRs | `docs-host` connected without error; pool, host, SRs (Local storage, XCP-HL ISO library, ...), networks and VMs listed | Pass |
| Inspect About | Both versions recorded | See identities | Pass |
| Import verified ISO | ISO in the intended ISO SR | Import -> Disk upload (multipart, API) to XCP-HL ISO library: VDI 70,254,592 B; stored file SHA-256 equals the published value; stored as `<vdi-uuid>.img` with the ISO name as label | Pass |
| Create one test VM | Template/resources/storage/network match | `beginner-vm` (API `vm.create`): 1 vCPU, 1 GiB, new 20 GiB disk on Local storage, 1 NIC on Pool-wide network 0, installer ISO in the CD drive, boot order CD then disk, halted | Pass |
| Install OS through guest console | Installs on the new disk only | XOA-HL Console tab: root login on the live ISO, network up, answer file fetched, `setup-alpine` installed to `/dev/xvda` (the new 20 GiB disk): "Installation is complete" | Pass |
| Eject ISO and reboot guest | Boots from disk, console login | Eject (API `vm.ejectCd`); `reboot` typed in the console; guest boots Alpine 3.24.3 from `/dev/xvda3`; CD empty | Pass |
| Check guest networking | IP/gateway/DNS/connectivity | DHCP address on the lab LAN (/24), default via the lab gateway, DNS set, gateway ping OK, SSH with the installed key | Pass |
| Prepare stopped guest / sample | Flushed, checksummed, stopped normally | Files written, `sync`, checksums recorded, `poweroff`; VM halted | Pass |
| NFS remote access | Enable/test succeeds | `remote.test` success | Pass |
| Manual full backup | One VM, full, retention 2, disabled schedule; logs OK | Run 13:08:16 to 13:08:31 JST; log: backup / backup VM / export (remote) / transfer 636,396,032 B / clean-vm, all `success`; schedule still disabled | Pass |
| Discover backup | Timestamp and remote in Restore | `20261027T040818Z`, full, on the NFS remote | Pass |
| Restore stopped copy | Writable SR, auto-start off, distinct UUID | Restored to Local storage: `beginner-vm (20261027T040818Z)`, halted, auto-start off, new UUID, description "Restored on ... from docs-nfs" | Pass |
| Isolate before boot | Stopped, all VIFs removed | 1 VIF removed while halted; 0 VIFs | Pass |
| Validate restored data | Console boot/login, checksums match; original untouched | Console: `sha256sum -c`: `sample.bin: OK`, `sample.txt: OK`; only `lo` present; original halted, never started | Pass |
| Cleanup / schedule | Only the restored copy removed; schedule disabled | Restored VM and its disk deleted; original VM and disk kept; `beginner` schedule disabled | Pass |
| Console typing (tooling note) | n/a | Synthetic Playwright typing into the noVNC console drops Shift (`&` arrives as `7`, `:` as `;`, uppercase as lowercase); explicit Shift+key presses work. Needs a human check before calling it a product bug | Note |

## Publication acceptance

- [ ] Lab checks above complete with release identities and reproducible findings.
- [ ] Useful appliance screenshots captured with metadata.
- [ ] EN technical review and FR/JA technical/language reviews recorded.
- [ ] Written backup/restore procedure passes the lab checks above.
- [ ] Translation statuses changed to reviewed only after those reviews.

Hugo builds, links, language switching, ranked task search and Lighthouse are
separate website checks. Their success does not check a hypervisor, guest OS,
backup target or real appliance credentials. Keep #197 open until its full
acceptance is met.

## Repository ownership and handoff

Screenshot infrastructure is tracked in
[jenkins-infra#87](https://github.com/Vagrantin/jenkins-infra/issues/87).
This source batch contains no appliance capture runner, Jenkins setup or
screenshot provisioning code. Import only approved images with version, language,
date, caption and alt text when that pipeline's reviewed output is available.
Website browser/Lighthouse checks exercise the documentation UI; they are not
appliance screenshot infrastructure.

D0 #195 still needs named technical owners and FR/JA reviewers. This source
review does not appoint people or claim their approval. D2 #197 and D7 #202 remain
open for the lab/screenshots, language review and deployed endpoint acceptance.
