# First beta: user and support readiness

Status: preparation only, reviewed 2026-11-09. XOA-HL
`v5.113.2_e281c536-ce52` RPM, tag `8da29b0`, SHA-256
`1a2e8b8b05bd02726a74f8a2f2b3b612192c6466e4f1b71a6e0886bba87e332a`, is
promoted to stable repository generation 20. Jenkins `prod/promote` #45 was
admin-approved, `promotion-consumer-check` #27 passed for the exact RPM, and
the GitHub release is non-prerelease and Latest. This establishes RPM promotion
only. XVA build #76 is still active; no XVA deployment, credential, #311,
updater or beta-launch acceptance is established by the promotion. The intended
beta keeps today's alpha feature scope while reducing risk of breakage. Do not
translate that intent into a compatibility or reliability guarantee.

Owner decisions recorded in this thread on 2026-11-06: the supported beta
appliance installation route is **XO Lite XVA deployment only**. Direct XOA-HL
RPM installation is outside user-supported beta scope. No public issue-response
target is set until an owner and target are named. A confirmed data-loss,
exposed-default-credential or unrecoverable-update issue pauses the **affected**
download or deployment route pending an owner decision. This policy does not
claim that any such issue has been observed on ce52.

## User journey and publication gates

| Path | Existing reader entry | Gate before beta wording |
| --- | --- | --- |
| ISO install and XO Lite deployment | `content/*/docs/start/_index.md` | Identify the selected ISO and the XOA XVA asset separately; the image is resolved at deployment time. Record the accepted host/image pair and first-boot result. Installer photographs are upstream XCP-ng 8.3, not a current XCP-HL acceptance run. |
| First sign-in | `content/*/docs/xoa-hl/first-login.md` | Repeat with the exact ce52 image asset and XO Lite XVA route when build #76 is ready. The ce47/rebuilt-image observation does not transfer to ce52. Check credential provisioning, persistence after an immediate unclean stop and recovery, and absence of exposed default credentials. The ce47 deployed-XVA regression in [#311](https://github.com/Vagrantin/xcp-hl/issues/311) is a candidate acceptance gate. |
| Host and appliance updates | `content/*/docs/guides/updates.md`, `content/*/docs/xoa-hl/maintenance.md` | Identify which plane is updated. Host Patches applies all pending XCP-ng and XCP-HL packages for the selected host; appliance dnf is separate. Record the ce52 transaction, service recovery, reboot decision and failure behavior in the lab before claiming it works. [#306](https://github.com/Vagrantin/xcp-hl/issues/306) and [#307](https://github.com/Vagrantin/xcp-hl/issues/307) need exact installed-candidate tests. |
| VM backup and restore | `content/*/docs/xoa-hl/backup-restore.md` | Require a completed backup and an isolated restored guest with checked data on the accepted pair. A successful job or listed restore point alone does not prove recoverability. |
| Configuration recovery | `content/*/docs/xoa-hl/configuration-backup.md` | Keep the documented boundary: its ce40/ce47 material does not establish complete appliance rollback, downgrade or fresh-image disaster recovery for ce52. Owner must choose a tested recovery procedure or explicitly accept that limitation. |
| Troubleshooting and administrator recovery | `content/*/docs/xoa-hl/troubleshooting.md` | Verify the ce52 console/log and administrator recovery path. The ce51 recovery command needed an interactive terminal; later behavior is unverified. |

The release matrix records components shipped together, not integration-test
results (`AGENTS.md`, `site/README.md`). A beta badge or release claim needs an
owner-approved, release-scoped publication decision after the manual lab. The
current site badge follows the latest stable ISO, not the XOA candidate; do not
change it to beta merely because ce52 exists (`site/layouts/_shortcodes/latest-iso-badge.html`,
`site/README.md`). Check the live badge, download, checksum, issue and manual URLs
again after the actual publishing build; a local link check does not prove a live
deployment.

## Known issues: precise public wording

- On a **direct ce51 RPM installation**, the initial XO administrator account
  was the upstream default before operator provisioning. This is [#368](https://github.com/Vagrantin/xcp-hl/issues/368).
  The XO Lite XVA route was not tested in that cell. Do not describe this as
  fixed in ce52 until that exact route and package are checked. For an affected
  direct RPM appliance, isolate management access and set a unique administrator
  credential before exposing it.
- On a **ce51 RPM appliance**, the administrator recovery CLI failed without an
  interactive terminal; `ssh -tt` worked in the recorded cell. This is
  [#369](https://github.com/Vagrantin/xcp-hl/issues/369). The manual now asks for
  an interactive console or pseudo-terminal. ce52 behavior remains unverified.
- On the **ce40 installed lab appliance**, selecting French or Japanese changed
  visible UI labels while the HTML document language stayed English. This is
  [#363](https://github.com/Vagrantin/xcp-hl/issues/363). It is an accessibility
  issue observed on ce40, not a demonstrated ce52 defect or fix.
- Complete appliance rollback/downgrade and fresh-image disaster recovery are
  outside the ce40/ce47 manual's supported procedure. A ce52 procedure and
  support promise require separate acceptance (`content/en/docs/xoa-hl/configuration-backup.md`).
- On a **ce47 XO 5.113.2 appliance**, an authenticated user with no ACL could
  read full VM inventory through the API even though the web UI hid it. This is
  [#309](https://github.com/Vagrantin/xcp-hl/issues/309), classified as an
  upstream issue and postponed until after launch. Proposed release note if
  confirmed for the accepted beta: “Authenticated accounts may read VM inventory
  through the API despite lacking object ACLs. Limit account access to people
  trusted to see inventory.” Verify the exact candidate before publishing this
  as a beta known issue; do not describe the ce47 observation as a ce52 result.

## Other blocker dispositions for support

- [#311](https://github.com/Vagrantin/xcp-hl/issues/311) remains a high-priority
  **XO Lite deployed-XVA** acceptance gate. Its ce47 regression is distinct
  from the ce51 direct-RPM default-account observation in #368. An image or
  source fix does not close the support gate without the exact installed
  candidate test.
- [#368](https://github.com/Vagrantin/xcp-hl/issues/368),
  [#369](https://github.com/Vagrantin/xcp-hl/issues/369),
  [#370](https://github.com/Vagrantin/xcp-hl/issues/370) and
  [#371](https://github.com/Vagrantin/xcp-hl/issues/371) are ce51 direct-RPM
  observations or postponed fixes. Direct RPM installation is outside the
  supported beta route. Check the supported XVA path separately before assigning
  any of them ce52 impact.
- [#144](https://github.com/Vagrantin/xcp-hl/issues/144) is **closed** for
  repository-consumer validation. The [2026-11-08 report at
  `xcp-hl@570921c`](https://github.com/Vagrantin/xcp-hl/blob/570921c0a5064aba347acbf8dcc37064d1f9d087/qa/signed-repo/results/2026-11-08/README.md)
  records passed signed-metadata, tamper and outage behavior on XCP-ng 8.3
  yum/rpm and AlmaLinux 9 dnf/rpm consumers. Host bootstrap install and package
  upgrade passed. The appliance consumer was a **ce51 direct-RPM installation**,
  outside the supported beta XVA route. The evidence is in open, review-pending
  [PR #386](https://github.com/Vagrantin/xcp-hl/pull/386); its review and merge
  remain separate from the closed issue. These results do not establish ce52
  XVA deployment, credential cleanup, updater behavior or same-byte promotion.
- [#310](https://github.com/Vagrantin/xcp-hl/issues/310) still requires an
  exact installed-candidate test of XO Lite XVA credential cleanup.
- [#374](https://github.com/Vagrantin/xcp-hl/issues/374) records a ce51 VLAN
  observation. Its disposition is documentation first, with fix planning after
  launch. It is not a ce52 result.
- [#364](https://github.com/Vagrantin/xcp-hl/issues/364) and
  [#365](https://github.com/Vagrantin/xcp-hl/issues/365) concern import/export
  format lists; verify the pinned upstream source before publishing a supported
  format claim. [#366](https://github.com/Vagrantin/xcp-hl/issues/366) concerns
  IP-pool allocation and [#367](https://github.com/Vagrantin/xcp-hl/issues/367)
  concerns token revocation. Those two need separate owner dispositions; a
  format-list decision does not cover them.

Do not call a historical issue a ce52 known defect. At acceptance, review each
open issue against the exact candidate and publish a dated, release-scoped known
issues list with severity, affected route, safe workaround and link.

## Intake, response and fix-forward

Use the public [beta problem template](../.github/ISSUE_TEMPLATE/beta_problem.yml)
in `Vagrantin/xcp-hl`; it requests the component, exact ISO/image/package
identities, installation route, steps, impact and sanitized evidence. For first
response, acknowledge the report, establish whether access or data is at risk,
ask the reporter to stop repeated writes/updates/restores if an operation may
be partial, and request missing version and error details. Link the applicable
release-scoped guide and known issue. Do not promise a response time until the
owner sets one.

For a confirmed data-loss, exposed-default-credential or unrecoverable-update
problem, pause the affected download/deployment route pending an owner decision.
The owner then decides whether and when to resume it or issue a corrective
release. Record the affected versions/assets and announce the decision at the same public entry
points as the release. Do not recommend RPM downgrade or configuration import
as a generic rollback: the manual does not support that path. Preserve the
installed state, logs and independent backups; use a tested, release-scoped
recovery plan. Publish a fix-forward instruction only after an isolated test of
the exact package/image and its failure mode.

## Translation and owner decisions

The EN manual is the source; FR/JA manual pages carry exact English and
translated-body revision approvals in `site/data/xoa_manual_reviews.json`.
Changing a procedural page invalidates those approvals. Follow
`site/TRANSLATION-REVIEW.md`: update all languages, mark affected translations
draft, obtain human technical and language review of the exact revisions, then
run `check_xoa_manual.py --require-reviewed` and both URL-shape builds. Do not
claim that a passing structure check or old approval tests ce52.

Owner decisions still needed:

1. Define the accepted ISO, XOA image asset/checksum and ce52 package combination,
   with the manual lab evidence and release date.
2. Name the beta issue triage owner and public response target, if any. Until
   then, make no response-time promise.
3. Set the supported ce52 recovery procedure and the owner decision process
   after an affected route is paused. Fix-forward instructions require an
   isolated test of the exact package/image and failure mode.
4. Approve the exact beta badge/release-note text and the dated known issues
   after acceptance, then commission EN/FR/JA human review and live link checks.
5. Decide #366 IP-pool and #367 token-revocation beta dispositions separately.
   Verify whether the ce47 #309 inventory-visibility observation persists on
   the accepted candidate and approve its release-scoped known-issue text;
   upstream remediation is already postponed until after launch.
