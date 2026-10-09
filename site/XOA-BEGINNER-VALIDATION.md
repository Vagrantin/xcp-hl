# Beginner journey validation — D2 #197

The `first-login` and `create-vm` tutorials are source-reviewed previews, not a
completed appliance acceptance report. FR/JA remain draft translations. No
appliance screenshots or lab results have been fabricated.

## Source scope reviewed on 2026-10-09

- Released image: [`xoa-image-20261009-5f33c81`](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261009-5f33c81),
  asset `XOA-hl.xva`, published 2026-10-09.
- Image build source: `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4`.
  Credential provisioning applies deployment values and documents the bootstrap
  fallback. HTTPS, separate `xo` SSH account and the image release stamp are
  present in that source.
- Application source: `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19`.
  `UPSTREAM_XO` pins XO 5.113.2 at
  `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`.
- All 14 patches applied successfully in their build-script order to a scratch
  copy of the pinned upstream tree. Reviewed resulting menu, User, Servers,
  disk-import, new-VM, Console, Disks and About screens and locale labels.
  This checks source applicability; it does not build or run the appliance.

The image tag does not establish which application package is currently
installed after updates. Do not replace these pins with an upstream XO 6 guide.
The shared historical `docs/_data/xoa_releases.yml` lacks today's image at this
review point. D0 must reconcile the release inventory with its publishing owner;
this batch does not modify publisher-owned release data.

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
| Independent backup and isolated restore | Full journey acceptance; procedures not written in this batch | Pending |

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
- [ ] Backup and isolated restore complete the beginner journey.
- [ ] Translation statuses changed to reviewed only after those reviews.

Hugo builds, links, language switching, ranked task search and Lighthouse are
separate website checks. Their success does not check a hypervisor, guest OS,
backup target or real appliance credentials. Keep #197 open until its full
acceptance is met.
