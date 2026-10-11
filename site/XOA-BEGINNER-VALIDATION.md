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
