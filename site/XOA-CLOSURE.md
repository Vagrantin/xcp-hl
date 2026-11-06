# XOA-HL documentation completion record (#189)

Status reconciled on 2026-10-25 (Japan), against source
`a4b54fb750f0b66c03a8984426ab72d558165cb8` on `claude/gracious-ride-99qg08`.
This is a maintainer record, not a reader-facing chapter or appliance test report.
Earlier dated validation records preserve their original evidence and limitations.

## Delivered work and remaining acceptance

| Work package | Delivered evidence | Required before closure |
| --- | --- | --- |
| D0 [#195](https://github.com/Vagrantin/xcp-hl/issues/195) | Source/deployment policy, 57-task inventory, release identities and explicit verification gaps (#215); ce40 scope refresh (#262) | Approve the final supported task/mode scope and name standing chapter, language, glossary and publication owners. Page approval is recorded, but does not assign those roles. |
| D1 [#196](https://github.com/Vagrantin/xcp-hl/issues/196), closed | Entry points, locale switching, glossary/status and docs-only deployment (#203, xcp-ce#12) | Complete. Preserve the checks during later work. |
| D2 [#197](https://github.com/Vagrantin/xcp-hl/issues/197) | Beginner journey (#206), ISO library (#223), scheduled-backup extension (#227); current FR/JA text approved in #271 | Reviewed illustrations or justified per-step exceptions, and a release-identified deployment/guest/backup/isolated-restore lab run. |
| D3 [#198](https://github.com/Vagrantin/xcp-hl/issues/198) | Daily administration (#208 and later batches): resources, snapshots/copy/transfer, guest tools/templates, SR/VLAN, backup/DR, hosts/HA, permissions/LDAP/SAML, management/TLS preflight; local SR extension (#270) | Approve the mode-specific checklist in the feature inventory, finish any included gaps, and record installed behavior and image review for that scope. Source-visible options are not tested availability. |
| D4 [#199](https://github.com/Vagrantin/xcp-hl/issues/199) | Maintenance/configuration/troubleshooting (#207), ce40 update correction (#262), sole-admin recovery (#269); current text reviewed | Observe update interruption/reboot behavior and configuration recovery in a disposable lab. Verify any rollback procedure before claiming support. |
| D5 [#200](https://github.com/Vagrantin/xcp-hl/issues/200) | Concepts/configuration/read-only automation (#210), pinned-client fixtures, glossary links and generated release reference (#273–#277) | Approve full reference scope and run the documented client against a release-identified appliance, including authorization/token and actual inventory checks. Release-data follow-ups #267/#268 remain separate. |
| D6 [#201](https://github.com/Vagrantin/xcp-hl/issues/201) | Revision-bound review records/gate/queue, UI glossary consumer (xoa-hl#34), all 40 FR/JA page approvals (#271), reviewed publication (xcp-ce#13) | Name standing review owners, settle final scope and obtain fresh approval for any later content changes. UI catalog review remains in #131. |
| D7 [#202](https://github.com/Vagrantin/xcp-hl/issues/202) | Both URL shapes, links/anchors, search, locale switchers, browser/mobile/themes/keyboard/reflow and Lighthouse CI; reviewed publisher and maintainer content validation | Browser UI zoom and human assistive-technology acceptance, plus critical installed workflows. Existing CSS resize tests do not supply those results. |

The current manual has 20 English pages and their 40 French/Japanese counterparts.
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

## Remaining work in execution order

1. Record the final included task/mode IDs and explicit dispositions for the
   feature-inventory gaps. Name standing owners; do not infer assignments from
   commits or the earlier page approval.
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
   ce47 untested rows (UI language, interrupted import) stay open. A separate
   ce40 installed session, Jenkins reset #176/stop #177, passed the EN/FR/JA
   language-selection pilot and observed partial console, storage, host-stat
   and management-path evidence in the 2026-11-03 records. It found the
   FR/JA HTML language defect [#363](https://github.com/Vagrantin/xcp-hl/issues/363).
   Other requested acceptance rows remain open; ce40 evidence does not transfer
   to ce47 or later releases.
   On 2026-11-03, separate ce55/ce51 disposable cells added an Ubuntu 24.04.5
   guest-tools clean-stop/boot pass and ce51 RPM-appliance results for interrupted
   config import and local OTP/sole-admin recovery. TLS replacement and rollback
   were observed, but the whole SE06 row remains open. See the dated daily,
   maintenance and OTP records. This RPM appliance is a different artifact from
   the published XVA. Defects [#368](https://github.com/Vagrantin/xcp-hl/issues/368),
   [#369](https://github.com/Vagrantin/xcp-hl/issues/369),
   [#370](https://github.com/Vagrantin/xcp-hl/issues/370) and
   [#371](https://github.com/Vagrantin/xcp-hl/issues/371) remain open.
   A later ce55/ce51 RPM cell also passed ordinary guest clean reboot,
   shutdown and boot with a preserved test-file checksum (VM02), plus added
   disk/NIC discovery inside the guest (VM04).
   A 2026-11-05 disposable ce55/ce51 RPM cell repeated VM02 and VM04 and
   verified DHCP and an appliance request bound to the newly added VM04 NIC.
   Earlier template deployment (VM06) and same-pool full-copy (VM07)
   observations were partial. The 2026-11-06 ce55/ce51 RPM continuation passed
   the requested halted VM07 pilot with a zero-VIF guest checksum. VM06 stays
   partial: a later read-write cleanup mount contradicted the guest-writer
   result, so disk attribution and persistence need investigation.
   The ce55/ce51 uncompressed halted XVA export and stopped import pilot
   (VM08) passed its scoped checks, including target SR, one-time link reuse,
   VIF MAC comparison, isolated boot and offline file checksum. The requested
   VM01 state/permission/browser pilot subsequently passed on 2026-11-06,
   including disabled EN/FR/JA display and cleaned Viewer/Operator fixtures.
   Wider console checks and the partial VM06 row remain open.
   A stopped snapshot revert (VM09) restored the guest's A checksum after a B
   change and preserved a before-snapshot point, but the guest retained its
   cell LAN VIFs for SSH, so that earlier run remained partial. The
   [2026-11-06 continuation](XOA-DAILY-VALIDATION.md#lab-run-2026-11-06-ce55-host-ce51-rpm-appliance-v-completion)
   passed the requested stopped VM09 checksum/revert pilot with zero VIFs,
   including recovery of the retained B point. An unexplained snapshot was
   preserved; wider modes, capacity and failure recovery remain open.
   A separate ce55 host/ce51 RPM appliance full cell then passed the scoped
   SN01 failed-write/recovery, SN02 NFS and local SR, and SN03 isolated VIF
   pilots. SN04 tagged VLAN and SN05 read-only diagnosis remain partial because
   the cross-host/recovery and real-fault/remedy cases were not exercised.
   See the dated [daily record](XOA-DAILY-VALIDATION.md#track-n-storage-and-network-2026-11-03)
   and defects [#372](https://github.com/Vagrantin/xcp-hl/issues/372),
   [#373](https://github.com/Vagrantin/xcp-hl/issues/373) and
   [#374](https://github.com/Vagrantin/xcp-hl/issues/374). No Jenkins build ran
   these disposable-cell tests. D3 and the wider storage/network scope stay open.
   The 2026-11-04 [backup evidence audit](XOA-DAILY-VALIDATION.md#lab-run-2026-11-04-backup-evidence-audit-and-final-cleanup)
   kept BK03 partial and BK04/BK06/BK07/BK09 open: the saved cell B summary
   conflicts with earlier operator messages and does not preserve a complete
   release identity, point chain or restore record. At the user's cleanup
   request, H was not started. All `ga-cell` VMs and tagged lab VDIs were
   removed; the two Jenkins-owned VMs were restored to Running, net1 was free,
   and free RAM matched the recorded baseline. No issue closes from this work.
   A 2026-11-05 ce55/ce51 RPM rerun passed VM02 and VM04 on a new cell,
   including connectivity through the added NIC. Separate host and identity
   cells observed partial HP01/HP02, HP04, SE07 and SE03 results. LDAP and
   SAML account-link reset subchecks passed, while test-VM grants, provider
   cleanup, trusted-browser and console-rollback checks remain open. The
   [dated record](XOA-DAILY-VALIDATION.md#lab-run-2026-11-05-ce55-host-ce51-rpm-appliance-disposable-cell-v)
   scopes these observations to the installed alpha release; no Jenkins
   acceptance build ran them.
   The 2026-11-06 [H evidence audit](XOA-DAILY-VALIDATION.md#lab-evidence-audit-2026-11-06-ce55ce51-h-groups-and-quotas)
   supports scoped SE01 local-group/ACL checks. SE02 stays partial: configured
   CPU/RAM/disk limits, access, accounting and an over-memory refusal were
   observed, but CPU and disk quota boundaries were not. Current host/discovery,
   statistics and management-path checks remain open. No wider D3 closure or
   general quota-enforcement claim follows from these alpha ce55/ce51 RPM logs.
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

## Missing-mode work, 2026-11-02

The [feature-inventory supplement](XOA-FEATURE-INVENTORY.md#missing-mode-supplement-2026-11-02)
records EN/FR/JA additions for VM03/06/07/08/09/11, BK03/07, SE01/02/05,
OP04/05/06 and RF01. This does **not** close those IDs. The 2026-11-02 daily,
maintenance and reference validation sections separate each mode, expected
behavior, actual shared-lab obstruction and result. Screenshot jobs #76 through
#80 occupied the lab while instructions were written; this thread has no
functional build numbers or newly observed installed identities.

Source-backed boundaries now distinguish user-only local groups from nesting,
local password change/admin recovery from absent self-service forgotten-password
reset, and settings import/forward package updates from a supported complete
appliance rollback or fresh-image recovery procedure. OP04/05 still need a
maintainer support decision or a successful release-specific recovery exercise;
a documentation boundary is not evidence of technical impossibility.

The explicit cutover rule supplied by Vagrantin requires **every inventory
mode**, including these previously missing modes, to have complete instructions
and release-specific functional evidence, or a cited unavailable/outside-pin
boundary visible to readers. Blocked, failed, skipped and unassessed modes stay
open. No earlier page approval or website build waives this rule. Guest-specific
preparation, real DST behavior, production backup/alert policy and the blocked
lab rows remain acceptance work.

All eight changed manual pages have FR/JA counterparts marked draft with fresh
English meaning hashes. Existing `data/xoa_manual_reviews.json` approvals are
untouched and do not approve this revision. Keep the reviewed-publication gate
and existing docs CI checks intact; obtain Vagrantin's exact-revision review
before publishing the new translations as reviewed.

## Missing-mode lab results, 2026-11-03

Reserved session 191 (`test/docs-lab-reset #191`) ran the API-level parts of VM03/06/07/08/09/11, BK03/07,
SE01/02/05 and RF01 on the ce44 host and ce40 image. See the
[inventory supplement](XOA-FEATURE-INVENTORY.md#missing-mode-lab-supplement-2026-11-03). No inventory ID is
closed: guest-side evidence (the fixture has no guest tools), browser steps, DST, alert delivery, OP04/05/06,
OVA import and token revocation remain open. EN/FR/JA chapters gained release-scoped lab result notes; the
FR and JA text stays draft for Vagrantin's exact-revision review and `data/xoa_manual_reviews.json` is unchanged.

## Acceptance attempt 2026-11-02

The [29-run follow-up](XOA-DAILY-VALIDATION.md#lab-run-2026-11-02-blocked-before-reset)
was blocked before reset by active shared Jenkins work. No installed identities
or functional results were collected. Earlier ce47 results and open PR #336
were checked to avoid repeating their rows. D2/D3/D4 acceptance remains open;
this attempt changes no task to passed. A free Jenkins/lab window is needed
before the next release-identified session.

A second session on 2026-11-03 reset and stopped successfully as Jenkins
#174/#175. [The credential preflight failed](XOA-DAILY-VALIDATION.md#lab-run-2026-11-03-credential-refused-before-acceptance),
so no functional acceptance status advanced.

## Translation review reconciliation, 2026-11-04

The review records merged through #375 remain reviewed where their exact English
and translated revisions still match. Vagrantin's [exact-commit approval for
PR #362](https://github.com/Vagrantin/xcp-hl/issues/201#issuecomment-6621307878)
covers the merged revisions of automation, backup-restore,
configuration-backup, permissions, templates, vm-operations and vm-transfer
in both FR and JA. Their review records now carry those exact hashes.

The combined troubleshooting chapter includes additions from both PR #362 and
the pre-production base. Its English and FR/JA revisions differ from both
previously approved snapshots. Vagrantin [approved the exact combined revision](https://github.com/Vagrantin/xcp-hl/pull/376#issuecomment-6628076135)
on 2026-11-04 as the technical reviewer and both FR/JA language reviewers. The
FR/JA pages are now reviewed with matching records. This documentation review
does not advance any release-scoped functional acceptance row above.
