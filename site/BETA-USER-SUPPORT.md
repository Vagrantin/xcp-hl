# First beta: user and support readiness

Status: preparation only, reviewed 2026-11-09. XOA-HL
`v5.113.2_e281c536-ce52` RPM, tag `8da29b0`, SHA-256
`1a2e8b8b05bd02726a74f8a2f2b3b612192c6466e4f1b71a6e0886bba87e332a`, is
promoted to stable repository generation 20. Jenkins `prod/promote` #45 was
admin-approved, `promotion-consumer-check` #27 passed for the exact RPM, and
the GitHub release is non-prerelease and Latest. This establishes RPM promotion
only. XVA build #76 has separate, limited deployed evidence below; this does not
establish updater or beta-launch acceptance. The intended
beta keeps today's alpha feature scope while reducing risk of breakage. Do not
translate that intent into a compatibility or reliability guarantee.

**Current route status: owner-lifted with a mandatory security limit.** The
owner's 2026-11-09 disposition for confirmed ce52 first-boot default-admin
sign-in in [#389](https://github.com/Vagrantin/xcp-hl/issues/389) allows the XO
Lite XVA route to proceed as a documented beta limitation, with the fix planned
after launch. Deploy only on a trusted network. Do not expose the appliance to
untrusted networks until setup completes. A setup retry after an interrupted
first boot reopens the default-admin sign-in window. The exact user-facing
warning, EN/FR/JA review and beta support gate remain open; do not claim beta
readiness from this disposition alone.

Owner decisions recorded in this thread on 2026-11-06: the supported beta
appliance installation route is **XO Lite XVA deployment only**. Direct XOA-HL
RPM installation is outside user-supported beta scope. No public issue-response
target is set until an owner and target are named. A confirmed data-loss,
exposed-default-credential or unrecoverable-update issue pauses the **affected**
download or deployment route pending an owner decision. Confirmed ce52 #389
triggered this policy; the owner then lifted that route pause with the mandatory
trusted-network/setup-completion limit recorded above.

## User journey and publication gates

| Path | Existing reader entry | Gate before beta wording |
| --- | --- | --- |
| ISO install and XO Lite deployment | `content/*/docs/start/_index.md` | Identify the selected ISO and the XOA XVA asset separately; the image is resolved at deployment time. Record the accepted host/image pair and first-boot result. Installer photographs are upstream XCP-ng 8.3, not a current XCP-HL acceptance run. |
| First sign-in | `content/*/docs/xoa-hl/first-login.md` | On the exact ce52 XVA below, provisioned-credential checks, forced-stop recovery, scenario A retry and secret cleanup passed once; a separate first-boot probe confirmed default-admin sign-in during provisioning (see #389). The owner permits the route with the trusted-network/setup-completion warning; a retry reopens the window. Update reader guidance only with exact-revision EN/FR/JA human review. |
| Host and appliance updates | `content/*/docs/guides/updates.md`, `content/*/docs/xoa-hl/maintenance.md` | Identify which plane is updated. Host Patches applies all pending XCP-ng and XCP-HL packages for the selected host; appliance dnf is separate. ce52 managed-update tests now close #307 for the exact XVA; #306 is closed after an interrupted kernel transaction, successful manual repair, and documentation of the scoped procedure. Do not generalize either to other images or to unattended updates. |
| VM backup and restore | `content/*/docs/xoa-hl/backup-restore.md` | The ce52 build76/ce36-host fixture passed full backup and two isolated whole-disk-verified restores, including one after appliance replacement (evidence below). The selected beta pair still needs its own acceptance; bootable-guest and application consistency were not tested. |
| Configuration recovery | `content/*/docs/xoa-hl/configuration-backup.md` | The ce52 build76/ce36-host fixture passed fresh-appliance XO metadata recovery and a subsequent VM restore (evidence below). This does not establish rollback/downgrade, pool metadata restore, independent remote hardware recovery, or a general recovery support promise. Human-reviewed reader instructions remain separate. |
| Troubleshooting and administrator recovery | `content/*/docs/xoa-hl/troubleshooting.md` | Verify the ce52 console/log and administrator recovery path. The ce51 recovery command needed an interactive terminal; later behavior is unverified. |

The release matrix records components shipped together, not integration-test
results (`AGENTS.md`, `site/README.md`). A beta badge or release claim needs an
owner-approved, release-scoped publication decision after the manual lab. The
current site badge follows the latest stable ISO, not the XOA candidate; do not
change it to beta merely because ce52 exists (`site/layouts/_shortcodes/latest-iso-badge.html`,
`site/README.md`). Check the live badge, download, checksum, issue and manual URLs
again after the actual publishing build; a local link check does not prove a live
deployment.

## Scoped ce52 backup and appliance-loss recovery result

On 2026-11-09, XOA-HL `v5.113.2_e281c536-ce52`, XVA build76
`xoa-image-20261109-8da29b0/qa-xoa-build-76.xva` (SHA-256
`658ad02024680af9714d491c608e7b73f97abbd05c6f6a8f23174b198a6a297c`),
passed full VM backup/restore and appliance-loss recovery on an installed ce36
host. Both appliances were deployed through the actual XO Lite `#/xoa-deploy`
flow. The first restore and the restore after appliance replacement each
matched the source's entire 1 GiB disk SHA-256
`28572f707d4cc882ab77bd707bce6fd1e48a9506bb6cf0e2724c40d823b73353`;
restored guests remained halted with no VIF.

XO metadata recovery on the fresh appliance restored the original administrator
ID, connected host, backup job, remote and disabled schedules. Default-account
sign-in was rejected before and after recovery. This result does not remove
the separately observed #388 configuration-import or #389 bootstrap-window
limitations. Durable evidence:
[`xcp-hl/qa/ce52-acceptance/2026-11-09.md@7a51eb118c7e3364807c4a43df959a5fa1b91f5e`](https://github.com/Vagrantin/xcp-hl/blob/7a51eb118c7e3364807c4a43df959a5fa1b91f5e/qa/ce52-acceptance/2026-11-09.md)
and its adjacent `evidence.txt`, submitted in [PR #401](https://github.com/Vagrantin/xcp-hl/pull/401).

The fixture used a halted guest and a separate local-file backup VDI. It did not
test bootable-guest/application consistency, delta chains, retention, pool
metadata restore, independent remote hardware loss, all remotes or every UI
backup wizard. A same-host backup fixture is not a backup-storage recommendation.
No beta ISO or ce55/ce52 pair acceptance, human review, reader-procedure approval
or broader support promise follows from this result. ISO selection and its
acceptance criteria remain pending.

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
- On XOA-HL image `qa-xoa-build-76.xva`, release `xoa-image-20261109-8da29b0`,
  SHA-256 `658ad02024680af9714d491c608e7b73f97abbd05c6f6a8f23174b198a6a297c`,
  application `v5.113.2_e281c536-ce52`, built by `build-xoa-hl@f269dc7` and
  deployed through XO Lite to one XCP-HL 8.3 test host at ISO build ce36,
  first-login credentials, forced-stop recovery, scenario A retry and secret
  cleanup passed in the observed setup. This is one setup, not broad acceptance.
  The evidence and documentation are in [PR #390](https://github.com/Vagrantin/xcp-hl/pull/390),
  merged to main as `cc44a2f`. The ce47 #311 regression was not reproduced in
  these observed recovery checks; #311 closed on that merge.
- On that same ce52 image and deployment setup, configuration import merged
  users and restored `admin@admin.net` with admin permission and password
  `admin` from an imported configuration ([#388](https://github.com/Vagrantin/xcp-hl/issues/388)).
  An import containing only the deployed administrator also did not remove an
  existing default account. An administrator must initiate the import. The
  planned fix is after launch. Until fixed, review **Settings → Users** after
  every configuration import and remove any default administrator before
  relying on the appliance. Do not use imports from fresh or unreviewed XO
  configurations without this check.
- On the same ce52 deployment, XO Lite reported success before phase-2
  credential provisioning finished; the default administrator existed until
  provisioning completed ([#389](https://github.com/Vagrantin/xcp-hl/issues/389)).
  A separate DHCP/LAN probe on the same build and XVA checksum confirmed that
  the default administrator accepted port-443 sign-in at 05:16:23.107Z and
  05:16:25.333Z; `/var/lib/xoa-credentials.done` appeared at 05:16:26.554Z,
  and sign-in was rejected at 05:16:27.359Z. This confirms exposure in **one
  observed run only**. The issue evidence is
  [#389 comment 6733086878](https://github.com/Vagrantin/xcp-hl/issues/389#issuecomment-6733086878).
  The owner lifted the route pause on 2026-11-09 as a documented beta limit.
  Deploy only on a trusted network and wait for `/var/lib/xoa-credentials.done` or the end of
  `/var/log/xoa-first-boot.log` before exposing an already deployed appliance;
  XO Lite's success message alone does not establish phase-2 completion. If
  setup retries after an interrupted first boot, the default-admin window opens
  again. The planned fix is after launch. This is distinct from #388, where an administrator
  import can restore the default administrator after provisioning.
- On a **ce47 XO 5.113.2 appliance**, an authenticated user with no ACL could
  read full VM inventory through the API even though the web UI hid it. This is
  [#309](https://github.com/Vagrantin/xcp-hl/issues/309), classified as an
  upstream issue and postponed until after launch. Proposed release note if
  confirmed for the accepted beta: “Authenticated accounts may read VM inventory
  through the API despite lacking object ACLs. Limit account access to people
  trusted to see inventory.” Verify the exact candidate before publishing this
  as a beta known issue; do not describe the ce47 observation as a ce52 result.

## Other blocker dispositions for support

- [#311](https://github.com/Vagrantin/xcp-hl/issues/311) is **closed** for the
  **XO Lite deployed-XVA** route. The ce52 build #76 single-setup recovery checks
  passed as recorded above; PR #390 merged as `cc44a2f` and closed #311.
  Do not describe that scoped result as broad candidate acceptance. It is
  distinct from the ce51 direct-RPM default-account observation in #368.
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
  outside the supported beta XVA route. The evidence is in
  [PR #386](https://github.com/Vagrantin/xcp-hl/pull/386), merged to main as
  `9f260b7`. These results do not establish ce52
  XVA deployment, credential cleanup, updater behavior or same-byte promotion.
- [#310](https://github.com/Vagrantin/xcp-hl/issues/310) remains closed. In
  addition to its historical ce44 evidence, the exact ce52 build #76 XVA was
  deployed through XO Lite on the ce36-installed Test host: credential keys
  were absent from XenStore and XAPI after provisioning. This observed cleanup
  is recorded in `docs/changelog.md@7e5ed23d750301d80565ecf01e6997ce4fc6755c`
  ([PR #390](https://github.com/Vagrantin/xcp-hl/pull/390)). It does not establish
  the selected beta ISO/image pair or erase the separately confirmed #389
  first-boot sign-in exposure.
- For ce52 image `qa-xoa-build-76.xva` (SHA-256
  `658ad02024680af9714d491c608e7b73f97abbd05c6f6a8f23174b198a6a297c`),
  `v5.113.2_e281c536-ce52` from `8da29b03`, [#307](https://github.com/Vagrantin/xcp-hl/issues/307)
  is **closed** for these observed XO Lite deployed-XVA checks on one Test host
  at ISO build ce36: a real kernel transaction reported `rebootNeeded=yes`, a
  concurrent start was rejected as busy, and the update verdict distinguished
  pristine `checked:false` from checked `checked:true`. This does not test all
  update paths or failure modes.
- For the same ce52 XVA and managed updater path, a force-stop during
  `kernel-modules` installation corrupted the kernel RPM payload. The updater
  detected corruption, failed honestly, cleared its stale verdict and refused
  a blind retry. The maintainer's verified repair restored integrity; the
  managed update and reboot then succeeded. Follow the technical repair
  procedure in the [appliance update guide](https://github.com/Vagrantin/xcp-hl/blob/c9a872b7384eb4149fc20ef1688d7e4ad603c8f4/docs/updates.md#after-an-interrupted-update).
  The owner closed [#306](https://github.com/Vagrantin/xcp-hl/issues/306);
  untested variants remain gaps.
  Evidence: [#306 test comment](https://github.com/Vagrantin/xcp-hl/issues/306#issuecomment-6733054150).

  **Support response if an appliance update is interrupted:** stop further
  update attempts. Keep the appliance on an isolated management network and
  retain console access. Record the image/package identity, task result,
  `/run/xoa-hl/status`, update log/journal, `dnf history`, and RPM verification
  output; do not treat `dnf check` alone as proof of package integrity. Escalate
  to the maintainer with those sanitized diagnostics. Do not reboot again,
  downgrade, or repeat an updater transaction as a recovery shortcut. Use the
  linked technical procedure only after confirming its scope matches the exact
  ce52 state. Any new user-facing recovery procedure must be written in EN/FR/JA, marked draft in
  FR/JA, reviewed by humans for technical accuracy and language against the
  exact revisions, and pass the reviewed translation gate before publication.
- Keep the separate residual observation visible: on ce52, automatic update
  can record `UP_TO_DATE` with `rebootNeeded=no` even after an earlier manual
  transaction left a reboot pending. This was observed, but is not the #307
  closed managed-update result. Treat `no` from that auto-update verdict as
  insufficient to clear an existing reboot requirement. Track this separately
  as [#392](https://github.com/Vagrantin/xcp-hl/issues/392), a release-scoped
  known issue. Owner disposition: documented beta limitation, fix planned after
  launch (`docs/updates.md@c9a872b`, Known limitations). Keep #307 closed for its
  exact tested managed-update cases; do not imply that #307 covered this
  auto-update observation. Interrupted automatic-update recovery remains
  untested.
  Duplicate-package failure, post-transaction verification failure and an
  interrupted automatic update remain untested despite the closure of #306.
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
4. Keep beta badge/release wording blocked until the owner-approved #389
   limitation has exact EN/FR/JA wording and human technical/language review.
   EN wording and FR/JA drafts for #388, #389 and #392 are in PR #398 for main's
   site; no human review is recorded yet.
   The route pause is lifted with the trusted-network/setup-completion limit;
   this does not establish beta readiness. Then approve dated known issues and
   check live links.
5. Decide #366 IP-pool and #367 token-revocation beta dispositions separately.
   Verify whether the ce47 #309 inventory-visibility observation persists on
   the accepted candidate and approve its release-scoped known-issue text;
   upstream remediation is already postponed until after launch.
