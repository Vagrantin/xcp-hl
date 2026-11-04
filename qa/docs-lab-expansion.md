# Documentation lab expansion plan

Status: planning and offline work only, 2026-11-04. This plan tracks
[xcp-hl #350-#360](https://github.com/Vagrantin/xcp-hl/issues/350),
[#294](https://github.com/Vagrantin/xcp-hl/issues/294),
[#305](https://github.com/Vagrantin/xcp-hl/issues/305), and
[#297](https://github.com/Vagrantin/xcp-hl/issues/297).

## Priority and evidence boundary

Issues #350-#360 are deferred P3 disposable fixtures. None blocks closure of
#189, #195, or #197-#202. Their modes remain untested for any released image
until a release-identified lab run records the actual result. A fixture's
existence, a passing screenshot job, and a release manifest do not establish a
manual validation pass. The current manual acceptance work uses the same lab;
coordinate a session window with its owner before touching fixtures.

## Issue audit

| Issue | Current finding | Next action |
| --- | --- | --- |
| #297 | `jenkins-infra` PR #150 merged 2026-10-30. `scripts/jenkins-activity.sh` implements `running` using Jenkins `Run.isBuilding()` and queue items; `scripts/bootstrap.sh` uses its guard. Offline cases are in `tests/test_jenkins_activity.py`. Deployed revision `4e796b0` contains the merge, and `jenkins-cli running` reported idle on 2026-11-04. The xcp-hl issue is still open. | Review issue closure after checking an existing busy-state log or observing the command during a naturally active build. No new CLI implementation is needed. |
| #305 | `jenkins-infra` PR #157 merged 2026-10-31. `casc/jenkins.yaml` now uses four-container cloud caps and distinct role image tags; `tests/test_agent_capacity.py` protects this mapping. Deployed revision `4e796b0` contains the merge. The xcp-hl issue is still open. | Check existing successful `docs-offline` and `docs-ui` build evidence under normal competing load. If both roles provision, review issue closure. Do not restart Jenkins to test this. |
| #294 | `jenkins-infra` PR #133 merged 2026-10-30 and added `docs/qa-model.md`, explicitly a proposal awaiting final review. The xcp-hl implementation issue is still open. | Obtain model decisions through normal review. Implement its five slices in separate reviewed changes, with measured gates and explicit test debt. Do not turn proposed budgets into release claims. |
| #350-#360 | All eleven issues remain open and explicitly deferred P3. No issue comment records a provisioned fixture. | Keep them deferred. Provision only against a reviewed `jenkins-infra` change and available capacity, then run the named modes. |

Source evidence: `jenkins-infra/scripts/jenkins-cli.sh@1c3e9effe11b04ae23cee3106c19a974bbb54b1d`,
`jenkins-infra/scripts/jenkins-activity.sh@1c3e9effe11b04ae23cee3106c19a974bbb54b1d`,
`jenkins-infra/scripts/bootstrap.sh@1c3e9effe11b04ae23cee3106c19a974bbb54b1d`,
`jenkins-infra/casc/jenkins.yaml@41c13cba06ed5f301b5128d2182bc550f01c4cb3`,
`jenkins-infra/tests/test_agent_capacity.py@41c13cba06ed5f301b5128d2182bc550f01c4cb3`,
and `jenkins-infra/docs/qa-model.md@55fc20d868270552833cb617eb15535fbdc52bfd`.
The current trees checked were `jenkins-infra@fba49ce53fe4368f19820c0f8e4433a0a5fceb78`
and `xcp-hl@476503652c377a026babbfe1dab881cc0b42d78c`. Issue and PR
states were read on 2026-11-04. The deployed controller checkout was inspected
read-only at `4e796b08a29198f887d864f90cd1e3acbf2c99dd`; its live JCasC
and Docker role tags were not independently inspected.

## Phases

1. **Close the evidence gaps without using the lab.** Review #297 and #305
   against deployed Jenkins configuration and existing build logs. Record the
   exact deployed commit, build IDs, competing load, and observed result on
   each issue. Close only after that review. Resolve #294's design decisions
   and make its test-debt ledger the place for unavailable fixture modes.
2. **Prepare one fixture at a time.** For each P3 issue, submit a reviewed
   `jenkins-infra` config and provisioning change. Include resource estimates,
   ownership tags, the baseline/reset path, independent teardown, and an
   offline selector or cleanup test. Check free Test-host RAM, disk, NICs and
   nested-host capability before approval. Start with low-capacity dependencies:
   #359 mail catcher, #353 Samba/NAS, then #355 storage target and #356 spare
   NICs. #352 Windows, #354 cloud targets, #357 identity providers and #358
   image library need separate licensing, account, disk or security review.
3. **Expand topology when capacity allows.** #350 needs two more nested hosts
   and shared NFS before pool migration, maintenance and HA pilots. #351 needs
   an isolated second pool for cross-pool and disaster-recovery modes. #360
   needs a disposable second appliance for isolated configuration recovery.
   Treat these as separate capacity decisions; do not silently enlarge the
   existing docs-lab baseline or repurpose another VM.
4. **Run release-identified acceptance.** The owning session checks
   `jenkins-cli running`, confirms both docs lab VMs are halted, and acquires
   `/root/docs-lab-session.lock` before any reset. A busy build, running VM or
   existing lock means no session starts. Reset and stop only through
   `test/docs-lab-reset` Jenkins jobs. Do not retag baseline snapshots, change
   `config/docs-lab.json` outside its reviewed PR, or touch Prod. The owner
   records observed host, ISO/XVA/RPM identities, Jenkins build IDs, expected
   and actual behavior, and pass/fail/blocked per mode in the matching
   `site/XOA-*-VALIDATION.md` record. Update the inventory only for observed
   modes and keep blocked modes open. Reader-facing EN/FR/JA changes follow
   exact-revision review before publication.

## Fixture map

| Issue | Fixture | Modes it enables |
| --- | --- | --- |
| #350 | Two more nested hosts, shared NFS | VM10, HP03, HP05, HP06 |
| #351 | Second pool | cross-pool VM06/VM07/VM10, BK05, BK09 |
| #352 | Windows SMB server | BK02 Windows SMB |
| #353 | Samba/NAS | BK02 NAS, SN02 SMB |
| #354 | S3 store, optional Azure account | BK02 S3/Azure |
| #355 | iSCSI target, spare ZFS disk | SN02 iSCSI/ZFS lifecycle |
| #356 | Extra nested-host NICs | SN04 bonds, host IP, VLAN lifecycle |
| #357 | LDAP and SAML providers | SE03 sign-in and group sync |
| #358 | Windows and Linux guest images | VM05 drivers and guest tools |
| #359 | SMTP sink | BK03 alert delivery |
| #360 | Second disposable appliance | BK08, OP05 isolated recovery |

The per-issue requirements govern the actual fixture design. This table is a
planning index, not a claim that any listed mode is available or passed.
