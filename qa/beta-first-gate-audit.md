# First-beta readiness audit — 2026-11-10

Final reconciliation completed 2026-11-09 UTC / 2026-11-10 JST after A, B and C finished. Scoped ce52 acceptance is met for the recorded scenarios. First-beta readiness is not yet established: owner scope/ISO decisions, exact-revision human reviews and content reconciliation remain. This is not launch signoff.

Scope: XOA-HL v5.113.2_e281c536-ce52 through XO Lite XVA deployment only. No beta publication, campaign, promotion, or signoff is authorized by this report.

## Artifact identity (GitHub release API checked)

- XOA-HL source: 8da29b03e751667b80ef4b3a58f6a53a6bc5f3b4.
- Builder source: f269dc7a98b11b1a0d16f38826c31db3089995c7.
- XVA: build-xoa-hl release xoa-image-20261109-8da29b0; asset 725900530, qa-xoa-build-76.xva, 986847999 bytes.
- XVA SHA256: 658ad02024680af9714d491c608e7b73f97abbd05c6f6a8f23174b198a6a297c.
- RPM: xoa-hl-5.113.2_e281c536-52.g8da29b0.xcpng8.3.el9.x86_64.rpm.
- RPM SHA256: 1a2e8b8b05bd02726a74f8a2f2b3b612192c6466e4f1b71a6e0886bba87e332a.
- RPM already has normal-release status and recorded stable generation 20; this is historical promotion evidence, not first-beta acceptance.

## Launch gates

| Gate | Status | Evidence and scope |
| --- | --- | --- |
| Exact XVA/RPM provenance | met | GitHub releases and manifest.json |
| Signed-repository consumers #144 | met within recorded release scope | xcp-hl/qa/signed-repo/results/2026-11-08/README.md@570921c0a5064aba347acbf8dcc37064d1f9d087; ce51 appliance consumer, not ce52 XVA acceptance |
| ce52 deployment/credential cleanup #310/#311 | met within recorded runs, with limitations | deploy-310-311-evidence.md; xcp-hl/docs/developers/build-xoa-hl.md@7e5ed23d750301d80565ecf01e6997ce4fc6755c |
| #389 early default credential window | documented limitation | owner comment 6733128404; one-run ~6s result; route pause lifted |
| #388 config import merges users | documented limitation | owner post-launch boundary; never import default-admin configuration without checking users |
| ce52 update/status/interruption repair #306/#307 | met within recorded runs | updater-evidence/SUMMARY.md; xcp-hl/docs/updates.md@fde48670265739f82bf9eb7557bf4dfa0d7486e9 |
| #306 untested variants | gap | xz-libs duplicate, post-transaction failure, interrupted auto-update |
| #392 pending reboot masking | documented limitation | owner comment 6733144716; post-launch fix |
| ce52 VM backup/restore | met | xcp-hl/qa/ce52-acceptance/{2026-11-09.md,evidence.txt}@7a51eb118c7e3364807c4a43df959a5fa1b91f5e; one full backup of halted/no-VIF 1 GiB fixture, entire restored disk matches source |
| ce52 appliance loss/recovery | met | Same QA record; serial fresh XO Lite deployment after predecessor/system disk removal; original admin, connected host, backup job, disabled schedules and remote recovered; second restore checksum matches |
| Lab cleanup and floors | met | r3-evidence/coordinator-final-audit.json and coordination.json: CLOSED at 18:08:42Z; exact 16 baseline guests halted; five owned VMs and six VDIs absent; five existing docs snapshots preserved; temporary credentials absent; matching ledger/Jenkins reservation released |
| Docs/support/marketing reconciliation | gap | #399 merged on downstream as 342afe04cdb3ea685c466ebe48786f5a4c51d3f6; #398 open at aafec5c66eb6137c6f309648dbc61a6c092128f3; marketing #7 draft/HOLD at 4a0fed01366ed890fc348adfd7d1b6489f78f7d4 |
| #364/#365 supported format evidence | gap | verified Vates source or tested fix, no inferred ce52 result |
| #366/#367 | needs owner decision | historical ce40 appliance findings; no later disposition in issues; format list cannot decide functional behavior |
| Beta ISO/XVA acceptance | needs owner decision | ce55 install checks are separate; no selected beta pairing or criteria |
| EN technical / FR and JA language reviews | gap | Vagrantin designated by #348; exact-revision approval absent on #398; merge and CI do not imply review |
| Final launch/publication | needs owner decision | no publication or signoff inferred |

Issue snapshot: #144/#306/#307/#310/#311 CLOSED; #364-#371/#388/#389/#392 OPEN.

Preserve #309 upstream after launch; #368/#370 unsupported RPM path; #369/#371 postponed; #374 documentation/post-launch plan. These dispositions do not prove ce52 runtime behavior.

Contradiction to avoid: updater-evidence/SUMMARY.md says repair docs absent, but xcp-hl PR #394 subsequently merged. Keep that source as a dated test result, not current publication state. Similarly manifest.json acceptance=PENDING and old ledger entries are historical, not proof of final completion.

## Primary evidence and reconciliation

- [XVA release](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261109-8da29b0), [RPM release](https://github.com/Vagrantin/xoa-hl/releases/tag/v5.113.2_e281c536-ce52): release API asset digests match every full hash above. The XVA release body names both full source commits. These are provenance checks, not functional acceptance.
- [Signed-repository report](https://github.com/Vagrantin/xcp-hl/blob/570921c0a5064aba347acbf8dcc37064d1f9d087/qa/signed-repo/results/2026-11-08/README.md): actual yum/rpm and dnf/rpm controls, invalid metadata and RPM bytes, outage behavior, host bootstrap/upgrade. Direct-RPM ce51 consumer evidence is appropriate for this consumer gate only.
- [Deployment source report](https://github.com/Vagrantin/xcp-hl/blob/7e5ed23d750301d80565ecf01e6997ce4fc6755c/docs/developers/build-xoa-hl.md) and `/home/matth/ga-lab/beta-ce52-acceptance/deploy-310-311-evidence.md`: selected XVA deployment, credential cleanup, force-stop/retry runs. Do not generalize to SSH-disabled deployment, physical power failure, other images, or the entire password matrix.
- [Repair guide](https://github.com/Vagrantin/xcp-hl/blob/fde48670265739f82bf9eb7557bf4dfa0d7486e9/docs/updates.md) and `/home/matth/ga-lab/beta-ce52-acceptance/updater-evidence/SUMMARY.md`: installed ce52 preflight rejects the damaged-kernel fixture; manual repair, update and reboot pass. The ce49-to-ce52 run used the ce49 updater, so it does not test the ce52 preflight code. Untested variants remain gaps.
- [#389 owner exception](https://github.com/Vagrantin/xcp-hl/issues/389#issuecomment-6733128404) and [#392 owner disposition](https://github.com/Vagrantin/xcp-hl/issues/392#issuecomment-6733144716) remain controlling. The initial deployment record's failure to observe a default login does not contradict the later timed probe: the later probe established the short pre-provisioning window. Wait for provisioning completion on a trusted network.
- [#395](https://github.com/Vagrantin/xcp-hl/pull/395) is merged; [#396](https://github.com/Vagrantin/xcp-hl/pull/396) and [#399](https://github.com/Vagrantin/xcp-hl/pull/399) are merged into `claude/gracious-ride-99qg08`. That downstream Hugo branch has a separate cutover policy; it was not merged wholesale into main. [#398](https://github.com/Vagrantin/xcp-hl/pull/398) ports safety wording to main's Jekyll docs and marks draft translations. It remains unmerged with human review pending.
- [Marketing #6](https://github.com/Vagrantin/xcp-hl-mkt/pull/6) is merged, superseding older statements that it remained open. [Marketing #7](https://github.com/Vagrantin/xcp-hl-mkt/pull/7) is the current open draft/HOLD correction. Its placeholders and no-acceptance wording remain deliberate until final artifact and acceptance decisions.
- `/home/matth/ga-lab/beta-ce52-acceptance/iso-and-366-367-decision-brief-20261109T1751Z.md`: C's final brief. Independent issue API checks confirm #366/#367 open with no comments. Neither older finding proves ce52 behavior. The format instruction does not settle IP-pool bookkeeping or token self-revocation.
- [ce55 ISO release](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/tag/v8.3-ce55): `xcp-ng-8.3-ce55.iso`, SHA256 `311dc0fe8156db4ea6be535a9274057b7abe8af68d0644afc62b7e8283d57cfe`. `/home/matth/ga-lab/results/golden.md` records two ce55 nested installs with package/build/ISO-SR/reboot checks. These do not establish approved beta ISO acceptance or ce52 XVA deployment on ce55. The ce52 deployment evidence reports host build ce36; matching updated packages do not turn that installation into a tested ce55 ISO deployment.

## Remaining human actions

1. Decide #366 and #367 independently: require supported-route ce52 tests/fixes, or approve exact documented limitations and later work. Their open states alone are not blockers.
2. Select the beta ISO and define whether an ISO/XVA pair needs acceptance, and which checks establish it. No criteria are invented here.
3. Complete exact-revision EN technical and FR/JA review on #398 and applicable support content. Reviewer assignment and passing CI are not approval.
4. Reconcile final A results into support and marketing, resolve placeholders, and approve public content and timing only after the remaining decisions. No broad pilot or integration compatibility is inferred.
5. Make the final go/no-go decision. This audit does not authorize publication, promotion, or announcement.

## Dependency results

- A, final lab acceptance: <t3-thread://v2/93f92a91-f0f2-4397-b92d-1121f046cbb7/mcp:launch:114cab625fe3ee18b054377696ee95048d45a92af64728d6f9e721c6cbb391a4>.
- B, final docs reconciliation: <t3-thread://v2/93f92a91-f0f2-4397-b92d-1121f046cbb7/mcp:launch:efe8bf54a19c45ea6eb7ddcbaa129d011395e41482b81ff4770a18f483030fbb>.
- C, final ISO/decision brief: <t3-thread://v2/93f92a91-f0f2-4397-b92d-1121f046cbb7/mcp:launch:93803a02178477cdaeb8e573368bcc53812bcd916ffe2e9308d796f55f7ad224>.

Local evidence is kept at its original path; no lab resources or other workers' branches were changed by D. D read the primary evidence and reconciled A, then B, then C; D did not rerun the lab tests or infer human approval.

## Final A evidence and scope

[QA PR #401](https://github.com/Vagrantin/xcp-hl/pull/401), head `7a51eb118c7e3364807c4a43df959a5fa1b91f5e`, contains the [release-scoped report](https://github.com/Vagrantin/xcp-hl/blob/7a51eb118c7e3364807c4a43df959a5fa1b91f5e/qa/ce52-acceptance/2026-11-09.md) and [sanitized transcripts](https://github.com/Vagrantin/xcp-hl/blob/7a51eb118c7e3364807c4a43df959a5fa1b91f5e/qa/ce52-acceptance/evidence.txt). Both secret-scan checks passed; no reviews are recorded. The report remains a PR, not merged evidence in main.

D compared the source creation, first restored disk, post-backup source read and second restored disk transcripts. All contain full SHA256 `28572f707d4cc882ab77bd707bce6fd1e48a9506bb6cf0e2724c40d823b73353`. Recovery readback shows the original admin, connected host, full-backup job, disabled schedules and original remote; deployed login succeeds and default login is rejected. A bootstrap remote also remains in the test readback; no claim of byte-identical configuration is made.

This establishes the recorded full-fixture backup and appliance-loss recovery scenario. It does not cover bootable guest/application consistency, delta chains, retention, pool metadata, independent backup-hardware loss, all remote types or every UI wizard. Those remain gaps, without silently becoming launch blockers. The fixture backup on a surviving local VDI is not production backup-placement guidance.

Coordinator audit `r3-evidence/coordinator-final-audit.json` independently verifies cleanup, not acceptance. It records compute free **14,487,891,968 B**, XAPI SR free **83,617,673,216 B**, and backing filesystem available **61,297,897,472 B**, above the 6 GiB and 40 GB floors. At 18:08:42Z the matching ledger entry was removed and Jenkins reported `reserved=false`, `reservedBy=null`, `locked=false`. D checked those values and the local coordination status programmatically. No r3 snapshot remains; the five old docs snapshots were preserved. The earlier empty default VM snapshot query did not prove zero snapshots and is superseded by the explicit snapshot audit.

## Contradictions and remaining content corrections

- The older updater summary's statement that repair docs were absent is superseded by merged #394. The older manifest's pending acceptance field and intermediate ledger observations are not final status; use the dated final QA and closeout records.
- `xcp-hl/site/BETA-USER-SUPPORT.md@342afe04cdb3ea685c466ebe48786f5a4c51d3f6` still says the candidate needs an exact #310 installation test, despite its own preceding ce52 cleanup evidence. `xcp-hl-mkt/LAUNCH-CHECKLIST.md@4a0fed01366ed890fc348adfd7d1b6489f78f7d4` cites only historical ce44 evidence for #310. Update these to cite the actual ce52 runs and list only the untested variants; do not reopen #310 without a failure.
- Support and marketing finished before A's final recovery/closeout. Their broad pending-acceptance wording must be reconciled with #401 before publication, while keeping all wider untested modes explicit. D has not changed their branches.
- Marketing #7 still deliberately has `[ISO_TAG]`/`[XOA_IMAGE_TAG]` placeholders. Tested XVA identity is established above, but the owner must approve the announced pairing and content; tests alone do not authorize replacing all publication placeholders.

Validation: report-only change; `git diff --check`; read-only GitHub release/issue/PR queries; transcript checksum comparison and cleanup-ledger assertions. No local product build, lab mutation, artifact promotion, beta publication or announcement was performed.
