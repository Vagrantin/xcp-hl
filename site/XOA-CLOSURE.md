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
