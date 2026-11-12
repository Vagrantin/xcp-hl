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
   supports scoped SE01 local-group/ACL checks. SE02 was partial at that
   checkpoint. The later [focused quota run](XOA-DAILY-VALIDATION.md#lab-run-2026-11-06-ce55ce51-h-quota-boundaries)
   completed independent CPU/disk boundary checks, unchanged accounting,
   no-partial-object checks and cleanup. The requested local CPU/RAM/disk
   pilot passed on this alpha ce55/ce51 RPM cell; wider delegation remains open.
   No wider D3 closure follows from these observations.
   The 2026-11-06 [H continuation](XOA-DAILY-VALIDATION.md#lab-run-2026-11-06-ce55ce51-h-discovery-and-statistics)
   observed the requested single-host remove/re-add/reconnect, authenticated
   XO Lite discovery and controlled expired-marker cleanup. Host statistics
   added range/time/memory and FR/JA evidence, but the combined-series switch
   failed its expectation ([#384](https://github.com/Vagrantin/xcp-hl/issues/384)).
   HP04 remains failed/open; host CPU/outage, SE07 trust/console recovery and
   HP05 real-payload patching remain open or blocked. The later focused SE02
   quota pilot above is separate from the unresolved host-statistics checks.
   A later [SE07 console fixture](XOA-DAILY-VALIDATION.md#lab-run-2026-11-06-ce55ce51-h-independent-console-recovery)
   demonstrated actual rollback through the assigned appliance's Xen console
   after denying only the test client's SSH/HTTPS path. Rules and timer were
   cleaned. A later [temporary SAN fixture](XOA-DAILY-VALIDATION.md#lab-run-2026-11-06-ce55ce51-h-temporary-san-certificate)
   passed trusted-browser login and host inventory with normal TLS verification,
   completing the requested SE07 pilot. Exact original certificate/key/config
   rollback and fixture cleanup were observed. This does not establish browser
   trust for the restored no-SAN baseline; SE06 update persistence remains open.
   The subsequent [B0 full-backup prerequisite](XOA-DAILY-VALIDATION.md#lab-run-2026-11-06-ce55ce51-h-full-backup-prerequisite)
   passed on the ce55/ce51 RPM H cell: manual full NFS backup, stopped restore,
   zero VIF before boot, actual guest checksum and exact restore/disk cleanup.
   The independent point and source were preserved. Scheduled retention, delta,
   file recovery, deliberate failures and pool metadata still need separate runs;
   the old B date/run-label contradictions are not resolved by this prerequisite.
   The later [2026-11-07 BK03 run](XOA-DAILY-VALIDATION.md#lab-run-2026-11-07-ce55ce51-h-scheduled-full-retention)
   passed the scheduled-full pilot: three automatic runs, two newest points
   retained, disable/next-tick proof, isolated retained-point guest checksum and
   exact restore/disk cleanup. Delta, file recovery, deliberate failures and
   pool metadata remain open. Older contradictory evidence is not reused.
   The [2026-11-11 inventory rerun](XOA-DAILY-VALIDATION.md#lab-run-2026-11-11-inventory-rerun-first-beta-record)
   executed the owner decision to re-run the partial or failed modes on fresh
   ce55/ce51 RPM cells with direct readbacks. VM06 passed with distinct disks,
   a controlled guest write, persistence and VDI-unique offline attribution,
   and it root-caused the earlier cleanup-mount contradiction (nested dom0 LVM
   autoactivation reads the wrong VDI when mounting by VG). SN04 and SN05
   passed their single-host subcases with a tagged outer capture and a real
   firewall fault and remedy; their cross-host cases stay blocked by the
   deferred #350-#360 infrastructure. HP04 reproduced the #384 combined-series
   failure on a fresh cell without code changes. BK03 passed on the rerun cell
   (three automatic runs, retention 2, disable proof, isolated checksum
   restore), BK07 passed (deliberate failures with raw JSON, corrected rerun
   and isolated sample-C checksum restore) and BK09 passed its backup side
   (three runs, retention 2); BK04 stayed partial at that point (full A,
   incremental B and a checksum-verified B restore passed; the C full failed
   twice for lab capacity reasons and interrupted a synchronous merge, so the
   recipe's stop condition applied), as did BK06 (the file-restore scan hit
   the damaged point-B chain with a raw UUID assertion), and HP01/HP02
   advanced the server side (remove, re-add with reconnect and inventory
   passed) but stopped short of browser discovery and pruning (Chromium
   `net::ERR_FAILED` over an
   endpoint serving TLS1.2 per openssl). The [2026-11-12 capacity
   reconfiguration and residual-mode retry](XOA-DAILY-VALIDATION.md#lab-run-2026-11-12-capacity-reconfiguration-and-residual-mode-retry-test-sub-agent-branch-t3bk-retry-20261111)
   closed those residuals on a fresh, capacity-reworked cell: BK04 passed
   fully (full A, incremental B, full C, synchronous merge, retention 2, and
   isolated checksum-verified restores of A, of B before and after the merge,
   and of C); BK06's exercised subcases passed on the undamaged chain
   (partition scan, file search and a checksum-verified ext4 file restore from
   point B), while its LVM-root sample stays blocked by a reproduced
   product-side defect candidate recorded with root-cause evidence and no code
   changes; and HP01/HP02 passed, with XO Lite discovery completing in
   Chromium (the r11 `net::ERR_FAILED` not reproducing on a fresh context,
   recorded as a browser or lab artifact of that session) and product-side
   expired-marker pruning exercised and observed (fixture pruned, live marker
   refreshed, unrelated keys preserved). SE03's remainder stayed blocked because the Dev IdP host is
   down; nothing was improvised. A mid-session outer-storage exhaustion
   incident (100 percent full shared SR) is recorded there with diagnosis and
   recovery; it is a lab capacity fact, not a product defect claim. No issue
   closes from this work.
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

## Current integration status, 2026-11-10

The [owner receipt](https://github.com/Vagrantin/xcp-hl/pull/398#issuecomment-6759282510)
approves current content and languages with Vagrantin in both review roles.
`data/xoa_manual_reviews.json` now records the exact current manual hashes;
`reviews/owner-content-approval-20261110.json` preserves original page snapshots
and distinguishes renderer adaptations. Historical draft/review gaps above are
superseded for those approved revisions only. ES/DE publication remains deferred.

Beta ISO acceptance is no longer required; ce55 remains selected. The ce52
build76/ce36 recovery results in `qa/ce52-acceptance/2026-11-09.md` at
xcp-hl@7a51eb118c7e3364807c4a43df959a5fa1b91f5e satisfy the currently required
beta recovery scenarios. They do not establish ce55 acceptance or complete the
57-task manual inventory. Keep partial/failed/untested modes and infrastructure
P3 deferrals scoped as recorded. See [the current cutover requirements](CUTOVER.md)
for independent deployment, repository-client and inventory evidence. No campaign,
artifact promotion, publication date or unrelated issue closure is authorized.
