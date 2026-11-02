# XOA-HL documentation completion record (#189)

Status reconciled on 2026-10-25 (Japan), against source
`a4b54fb750f0b66c03a8984426ab72d558165cb8` on `claude/gracious-ride-99qg08`.
This is a maintainer record, not a reader-facing chapter or appliance test report.
Earlier dated validation records preserve their original evidence and limitations.

## Delivered work and remaining acceptance

| Work package | Delivered evidence | Required before closure |
| --- | --- | --- |
| D0 [#195](https://github.com/Vagrantin/xcp-hl/issues/195) | Source/deployment policy, 57-task inventory, release identities and explicit verification gaps (#215); ce40 scope refresh (#262). Vagrantin is the standing chapter, language, glossary and publication owner and requires every inventoried task/mode to be completed before cutover. | Record a release-specific disposition and required evidence for every mode. Standing ownership does not approve pending page revisions. |
| D1 [#196](https://github.com/Vagrantin/xcp-hl/issues/196), closed | Entry points, locale switching, glossary/status and docs-only deployment (#203, xcp-ce#12) | Complete. Preserve the checks during later work. |
| D2 [#197](https://github.com/Vagrantin/xcp-hl/issues/197) | Beginner journey (#206), ISO library (#223), scheduled-backup extension (#227); current FR/JA text approved in #271 | Reviewed illustrations or justified per-step exceptions, and a release-identified deployment/guest/backup/isolated-restore lab run. |
| D3 [#198](https://github.com/Vagrantin/xcp-hl/issues/198) | Daily administration (#208 and later batches): resources, snapshots/copy/transfer, guest tools/templates, SR/VLAN, backup/DR, hosts/HA, permissions/LDAP/SAML, management/TLS preflight; local SR extension (#270) | Approve the mode-specific checklist in the feature inventory, finish any included gaps, and record installed behavior and image review for that scope. Source-visible options are not tested availability. |
| D4 [#199](https://github.com/Vagrantin/xcp-hl/issues/199) | Maintenance/configuration/troubleshooting (#207), ce40 update correction (#262), sole-admin recovery (#269); current text reviewed | Observe update interruption/reboot behavior and configuration recovery in a disposable lab. Verify any rollback procedure before claiming support. |
| D5 [#200](https://github.com/Vagrantin/xcp-hl/issues/200) | Concepts/configuration/read-only automation (#210), pinned-client fixtures, glossary links and generated release reference (#273–#277) | Approve full reference scope and run the documented client against a release-identified appliance, including authorization/token and actual inventory checks. Release-data follow-ups #267/#268 remain separate. |
| D6 [#201](https://github.com/Vagrantin/xcp-hl/issues/201) | Revision-bound review records/gate/queue, UI glossary consumer (xoa-hl#34), all 40 FR/JA page approvals (#271), reviewed publication (xcp-ce#13). Vagrantin owns both human review roles for pending FR/JA revisions. | Settle final scope and obtain exact-revision approval for changed pages. UI catalog review remains in #131. |
| D7 [#202](https://github.com/Vagrantin/xcp-hl/issues/202) | Both URL shapes, links/anchors, search, locale switchers, browser/mobile/themes/keyboard/reflow and Lighthouse CI; reviewed publisher and maintainer content validation | Browser UI zoom and human assistive-technology acceptance, plus critical installed workflows. Existing CSS resize tests do not supply those results. |

The current manual has 20 English pages and their 40 French/Japanese counterparts.
For the first Hugo-to-main cutover, defer Spanish/German [#293](https://github.com/Vagrantin/xcp-hl/pull/293)
until after EN/FR/JA review and publication. Its draft pages require their own
human technical/language review and five-locale publication checks before any
later inclusion. For the first cutover, Vagrantin requires every task and mode
in the 57-task inventory to have a completed release-specific disposition.
Available modes need complete instructions and functional evidence; unavailable
or outside-pin modes need cited evidence and an explicit reader-facing boundary.
No unresolved `Preview` or `Gap` can satisfy this gate, with one exception:
modes needing lab infrastructure that does not exist yet are tracked as P3 issues
[#350](https://github.com/Vagrantin/xcp-hl/issues/350) to
[#360](https://github.com/Vagrantin/xcp-hl/issues/360). Their reader-facing text
states "not tested in this release" for the named release scope. They do not
block the cutover or closing other issues. Current source coverage
and selected ce47 lab results do not establish that all modes are complete.
The [2026-10-23 approval](https://github.com/Vagrantin/xcp-hl/issues/201#issuecomment-6361303818)
names Vagrantin in both technical and language roles for the exact `a733d92`
revision. #271 records matching page hashes; run `check_xoa_manual.py
--require-reviewed` to establish freshness at a later revision. Do not repeat
old claims that all FR/JA pages are drafts, or assume approval of new changes.

Reviewed publication is implemented by
[xcp-ce#13](https://github.com/Vagrantin/xcp-ce/pull/13), merge `5e92ca4`.
The maintainer's [content validation](https://github.com/Vagrantin/xcp-hl/issues/202#issuecomment-6379283206)
is recorded separately from appliance and assistive-technology acceptance.
[Pages run 40165660264](https://github.com/Vagrantin/xcp-ce/actions/runs/40165660264)
succeeded: its build log identifies source `a4b54fb`,
`XOA_PUBLICATION_MODE=reviewed`, zero draft translations and passing docs-only
validation. Both build and deploy jobs passed.

## Screenshot review inventory

The older [241-item backlog](https://github.com/Vagrantin/xcp-hl/blob/main/docs/screenshots/STEP-COVERAGE.md)
is based on `a7f0885`. It contains repeated section/step labels and does not
describe the complete current source. Retain its prepared-request mappings as
leads, but recheck each mapping against the actual source and UI before use.

Generate a current-source review queue from the repository root:

```bash
python3 site/scripts/export_xoa_steps.py --output browser-evidence/xoa-step-inventory/inventory.json --markdown browser-evidence/xoa-step-inventory/inventory.md
```

Documentation CI exports `xoa-step-inventory-pages` and
`xoa-step-inventory-standalone` for its exact checkout. The report lists every
manual page, including those with no numbered items, and every numbered item
outside front matter, code fences and HTML comments. Each item has a unique
page-wide positional ID, source line, heading path, cue and hash; the page hash
covers continuation text and unnumbered instructions too. IDs can shift after
insertions: a decision must match both `pageRevision` and `itemRevision`.

All generated dispositions are **pending editorial review**. The report does
not inspect existing PNGs, assign exceptions, run Jenkins or approve images.
Unnumbered instructions, tables, wizard fields and command blocks still need
separate editorial disposition. For each item, record either the reviewed image
and covered step(s), or a specific justified exception such as a secret-entry,
CLI-only or guest-dependent screen. A request file alone is not image approval.

The capture runner, fixture configuration and reset procedure stay in
`jenkins-infra`. The older issue comments in
[#91](https://github.com/Vagrantin/jenkins-infra/issues/91) are superseded by merged
[#125](https://github.com/Vagrantin/jenkins-infra/pull/125),
[#126](https://github.com/Vagrantin/jenkins-infra/pull/126),
[#127](https://github.com/Vagrantin/jenkins-infra/pull/127),
[#128](https://github.com/Vagrantin/jenkins-infra/pull/128) and
[#129](https://github.com/Vagrantin/jenkins-infra/pull/129). At infra commit
`18506175a4b8c3ba8efba8d18bd9dd060670e44b`, `config/docs-lab.json` enables
both targets, names Vagrantin as lab owner, and declares ce40/image
`xoa-image-20261022-a280852` plus host `v8.3-ce44`. The runbook records
provisioning, reset and live preflight. Do not repeat the old missing-lab claim.

The first live `docs/screenshots #3` failed at `en/selectors`; #129 fixes the
CSS/text mask mismatch. Its description records successful reset #5 and stop
#6, but no successful post-fix live image bundle. Rerun the existing request
after deploying infra #129, then review its private artifacts. The Jenkins
controller is on the operator LAN; this workspace has no controller session or
vault-mounted runner. Accepted offline build #1 remains simulated illustration,
not proof of the later live pilot or functional journey.

## Lab capacity for the full-inventory gate (2026-11-02)

The current documentation lab is one nested host (`docs-xcphl`, `v8.3-ce44`,
3 GiB), one appliance (`docs-xoahl`, application `5.113.2_e281c536-47`) and the
`docs-nfs` VM. The source is `jenkins-infra@5f90e8a3d4f1360f17f089900946abbe1297bda6`,
`config/docs-lab.json` and `docs/docs-screenshots.md`. Nested hosts need the
Intel Test host. The table groups remaining modes by the resources they need.
It is a planning aid. It does not record a disposition or a test result.

| Lab resource | Modes that depend on it |
| --- | --- |
| Current lab only | Single-host VM01-VM09/VM11 gaps, SN01/SN03/SN05, NFS and spare-disk SN02, BK01/03/04/06/07/08, HP01/02/04, SE01/02/04-07, OP01-03/06, RF01 mutation examples |
| Second and third nested host, or a second pool | VM06/VM07 cross-pool, VM10, HP03, HP05 evacuation, HP06 (three hosts plus shared heartbeat SR), BK05, BK09 isolated restore and host recovery |
| Additional storage or remote targets | BK02 (Windows Server share, Linux Samba/NAS, S3, Azure), SN02 (SMB, iSCSI, ZFS, reattachment) |
| Extra host uplinks | SN04 bonds, host IP or management changes, wider VLAN lifecycle |
| Identity providers | SE03 LDAP and SAML directory, group sync |
| Other guest operating systems | VM05 drivers, other OSes, ISO path, upgrades and removal |
| No lab, cited boundary only | OP04 and OP05 if recorded as unsupported, BD01-BD04, RF02-RF04 |

Each reader-facing change also needs FR/JA updates and exact-revision review by
Vagrantin. Since 2026-11-02, `jenkins-cli` on the controller authenticates
with an `admin` API token read through `JENKINS_API_TOKEN_FILE`. Through it,
`test/docs-lab-reset` #109 (`reset`) and #110 (`stop`) succeeded. Prefer the
Jenkins job: `scripts/docs-lab-reset.sh` skips the `docs-xcphl`/`docs-xoahl` locks.

## Remaining work in execution order

1. Record the final included task/mode IDs and explicit dispositions for the
   feature-inventory gaps. Use the standing assignments in
   [TRANSLATION-REVIEW.md](TRANSLATION-REVIEW.md); do not infer page approvals
   from those assignments.
2. Use the provisioned lab and the existing `docs/screenshots` job after infra
   #129 is deployed. Rerun `XCP_HL_REF=main`,
   `REQUEST=xoa-first-login-live.yaml`; the runner resets the lab beforehand and
   stops it afterwards. Record its build URL and private manifest/PNG hashes.
   Provisioning and source configuration now exist; controller execution and
   successful post-fix image evidence are the next boundary.
3. Run the English beginner lab first, then the included administration,
   backup/restore, update and configuration-recovery cases from the existing
   `XOA-*-VALIDATION.md` records. Record observed host/image/RPM identities,
   expected/actual results, run URLs and sanitized evidence. A failed or blocked
   scenario remains open; screenshots alone do not pass it.
   First release-identified run: 2026-10-27 on ce47 (beginner, maintenance and
   reference records, "Lab run 2026-10-27" sections). Open findings #305 to #311;
   untested rows (UI language, interrupted import) stay open.
4. Capture prepared live states through the existing Jenkins job, review the
   EN/FR/JA bundles and hashes, and integrate approved assets with localized alt
   text and version/language captions. Finish the per-step editorial decisions.
5. Perform actual browser UI zoom and human assistive-technology review, record
   browser/tool versions and observations in `ACCESSIBILITY-VALIDATION.md`, and
   fix any material failures. Retain the existing automated checks.
6. Review any changed translations, pass the strict gate and documentation CI,
   and verify the deployed source/run/URLs. Close each D-issue only against its
   own acceptance evidence, then close #189 after its full checklist passes.

Functional test plans already exist in the beginner, daily, maintenance,
reference and OTP validation records. This completion record consolidates their
dependencies; it does not replace their detailed scenarios or mark them passed.
