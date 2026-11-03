# Released-source feature and chapter inventory — D0 #195 / #189

This is a **scope proposal for review**, assessed on 2026-10-12. It inventories
the tasks requested by #189, maps the existing EN/FR/JA preview chapters, and
identifies the checks needed before production acceptance. No appliance was
booted or operated for this inventory. Standing owners remain unassigned; the
current 40 FR/JA page approvals are recorded by #271. Approval of the full
content scope remains pending in #195. See [the completion record](XOA-CLOSURE.md)
for current status; dated source observations below retain their original scope.

## Baseline and evidence meaning

The **original source-review baseline** used for the inventory was image
`xoa-image-20261009-5f33c81`, application release `v5.113.2_e281c536-ce38`,
`xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19`, and XO 5.113.2 at
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. This is not an assertion that no
newer release exists, or that these versions have passed integration tests.

| Identity | Pinned evidence / limitation |
| --- | --- |
| Image source | `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4`; [beginner validation](XOA-BEGINNER-VALIDATION.md) records first-boot findings |
| Published XVA SHA-256 | `a9b621ce71c56445bb3998fe418cc5079c32340477a7a2830a3ef19609cfff0b`; published metadata, not a locally downloaded payload hash |
| Application RPM | `xoa-hl-5.113.2_e281c536-38.g5f33c81.xcpng8.3.el9.x86_64.rpm` |
| Published RPM SHA-256 | `3e85d7688664dfd55426b1d5f7e88e692c17fc4bb75d4dce31e58b9b0095bc7a`; published metadata, not installed NEVRA evidence |
| XO5 source and package recipe | [UPSTREAM_XO][pin], [build script][build], [RPM spec][rpm], [patch metadata][patches]; 14 patches applied during the preceding source review |
| XO Lite discovery reference | `xolite-ce@ca72babb35f435b31d4726a7d1e90f42b9c06cb8` / `v0.21.0-ce29`, upstream `13f987ff3d34504a90b89178489e15fa2293d1b3`; separate scope, not a compatibility claim |
| Documentation baseline before the VM03/VM11 extension | #215 merge `xcp-hl@2c6baa522a63ec946fca124b9f882e3080d1e255`, source branch `claude/gracious-ride-99qg08`; the extension's exact PR/run identity is recorded on its implementation PR |
| Installed host/image/application identities | **Unobserved**; fill the release-identified lab records before asserting installed availability |

### Scope refresh to ce40 (2026-10-23)

Reader-facing "Applies to" scope now names image `xoa-image-20261022-a280852`
and application release `v5.113.2_e281c536-ce40`
(`xoa-hl@a28085219cdfe9d20700e6060377f5059e42e6b5`). The XO pin is unchanged
(`e281c536`), so the ce38 source review above still covers every page except the
appliance updater. The `ce38..ce40` diff changes only these runtime paths:

| Change | Source | Manual effect |
| --- | --- | --- |
| Random delay removed from UI, API (`randomDelayMinutes`), `update.conf` and the configure helper (now four arguments); both timers use `RandomizedDelaySec=0` | xoa-hl #35/#36, xcp-hl #216/#217 | Maintenance and updates pages no longer ask for a random delay; runs start at the set time |
| Stored check result shown when the Updates page opens | patch `zzzzzzzzzzzz-xoa-hl-update-check-status-on-load` | Maintenance result step mentions it |
| Failed automatic run shown as a red banner | patch `zzzzzzzzzzzzz-xoa-hl-auto-update-ui-fixes` | Maintenance and updates pages mention it |
| Automatic run trusts the update log when a glibc upgrade drops the systemctl D-Bus link | `SOURCES/xoa-hl-auto-update.sh` | No procedure change; fewer false failures |
| Image first boot applies custom NTP servers | `build-xoa-hl@fc7ebfa7ad68664fc9b5701049cc314ebf18bea9`, xcp-hl #156 | No procedure change; the manual does not document appliance NTP input |

Published identities: RPM `xoa-hl-5.113.2_e281c536-40.ga280852.xcpng8.3.el9.x86_64.rpm`
(`sha256:00dd48cb4eccbf11ce7dd4e76826ca1b39de9a7a2df3233d05de8cd6700be825`),
XVA asset `qa-xoa-build-48.xva`
(`sha256:4b67bc22bc54b0f9f7af33fcc24a3832d85773d4066f4339479f0912d5e6a1c9`).
These are published metadata, not installed observations. The release declares
16 patches. Source links in the manual now point at `a280852`/`fc7ebfa`; every
linked file is unchanged from ce38 except the updater files above and
`patches/metadata.toml` (two new entries). The
validation records keep their dated ce38 evidence.

The matrix separates source observations from availability on a running
appliance. Its states deliberately include an unresolved state:

| State | Meaning |
| --- | --- |
| **Source-visible, unverified** | The pinned implementation/entry point was inspected. Installed UI, build-plan gates, prerequisites and successful behavior remain unverified. This is not “available and tested.” |
| **Hidden UI** | The released HomeLab patch hides the named navigation entry. This does not prove that a route, API or backend implementation is absent. |
| **Not assessed** | A required task remains in the inventory, but applicability/implementation has not been established for this release. Do not infer either availability or unavailability. |
| **Outside this pin** | The named product/version is outside the deliberate XO5/HomeLab baseline. It cannot supply instructions for this manual. |

No row is marked **available and tested**. “Unverified” does not mean
“unavailable,” and missing instructions do not mean a missing feature. A planned
documentation chapter is not a planned product feature. After lab evidence and
scope review, record available/tested, available/unverified, unavailable or
planned dispositions with the deciding evidence; do not derive them from a
successful website build.

The recipe builds all workspaces and prunes test/cloud packages, while the
upstream web build defaults to OpenSource plan 5 ([build][build], [plan][plan]).
That source observation explains why commercial-plan conditions alone do not
establish HomeLab feature absence. It is not a payload audit or installed-plan
observation. Plugin presence is not plugin configuration, external-service
compatibility or authentication acceptance.

## Chapter and task map

Chapter paths below are relative to `content/<locale>/docs/`; every linked
current chapter has EN/FR/JA counterparts. `Preview` means source-reviewed
instructions with lab acceptance pending. `Reference` supplies context, not a
complete task procedure. `Gap` requires a scope decision, additional instructions
and release-specific acceptance. **All functional checks below are pending.**
FR/JA manual pages were approved on 2026-10-23 (see `TRANSLATION-REVIEW.md`); structural parity alone is not language review.

### Start here — D2 #197

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| ST01 Deploy/import XOA-HL | Source-visible, unverified: separate image/deployment flow; [image source][image] | Preview: [start](content/en/docs/start/_index.md); image failure handling is partial | Identified XVA/host, intended network/credentials, first boot and interrupted import |
| ST02 First login and password change | Source-visible, unverified: [user API][user-api] | Preview: [first-login](content/en/docs/xoa-hl/first-login.md) | Deployment credentials, independent web/SSH/host identities, new password and retained admin access |
| ST03 Connect a host/pool | Source-visible, unverified: [server settings][servers] | Preview: first-login; [hosts-pools](content/en/docs/xoa-hl/hosts-pools.md) | Intended pool/SR inventory, TLS/credentials and reconnect failure |
| ST04 Choose documentation/UI language | Installed ce40 lab, reset #176: EN/FR/JA user and task labels switched; HTML language stayed `en` in FR/JA ([#363](https://github.com/Vagrantin/xcp-hl/issues/363)); documentation switching has website tests | Preview: first-login; [manual entry](content/en/docs/xoa-hl/_index.md) | Later-release and human assistive/language review; documentation language remains independent |
| ST05 Import ISO and create/install first VM | Source-visible, unverified: [ISO import][disk-import], [new VM][new-vm] | Preview: [create-vm](content/en/docs/xoa-hl/create-vm.md); existing-media NFS ISO setup is linked; writable ISO upload remains a separate prerequisite | ISO identity/SR, template/resources, console installation, media ejection and installed guest boot |

### Virtual machines — D3 #198

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| VM01 Console access | Ce40 lab reset #176: running VM canvas and `/api/consoles/<id>` WebSocket frames observed; [Console tab][console], [console client][console-client], [operate gate][console-gate], [host proxy][console-proxy] | Preview: vm-console in [vm-operations](content/en/docs/xoa-hl/vm-operations.md); guest display/input, disabled state and permission gate remain pending | Running/disabled state, operate permission, actual display and input, harmless clipboard, local-client separation, restart/reopen and owner-selected remedy |
| VM02 Start/stop/reboot | Ce55 host / ce51 RPM appliance cell V2: browser clean reboot changed guest boot ID; ordinary Stop reached Halted and Start booted, with test-file checksum and tools service preserved. | [VM operations](content/en/docs/xoa-hl/vm-operations.md); [release run](XOA-DAILY-VALIDATION.md#track-v2-clean-guest-reboot-and-shutdown-2026-11-03) | Pass for clean guest path on this cell; unsupported-guest prompt and forced fallback remain separate acceptance |
| VM03 Change CPU/RAM | Source-visible, unverified: [General][vm-general], [Advanced][vm-advanced] controls | Preview: stopped CPU/memory exercise in vm-operations; hotplug/DMC/load/topology remain gaps | Current/max CPU, ordered static/dynamic memory bounds, host capacity, related-limit readback, guest-observed result and recorded-baseline recovery |
| VM04 Add/remove disks and NICs | Ce55 host / ce51 RPM appliance cell V2: browser added a 1 GiB disk and generated-MAC VIF to the stopped Ubuntu guest; guest identified blank `xvdb` and matching `enX1`, while original `enX0` and IP remained. | [Storage chapter](content/en/docs/xoa-hl/storage-networks.md); [release run](XOA-DAILY-VALIDATION.md#track-v2-clean-guest-reboot-and-shutdown-2026-11-03) | Added-device discovery passed; detach versus VDI deletion and broader network connectivity remain open |
| VM05 Guest tools | Installed ce55 host / ce51 RPM appliance: Ubuntu 24.04.5 `xe-guest-utilities 7.20.2-0ubuntu1`, agent detection and ordinary Stop/Start passed ([lab record](XOA-DAILY-VALIDATION.md#lab-run-2026-11-03-ce55ce51-disposable-cells)) | Preview: [guest-tools](content/en/docs/xoa-hl/guest-tools.md); other OSes, upgrades/removal and supported guest matrix remain gaps | Broader guest/version matrix, IP-report behavior and failure recovery |
| VM06 Templates | Ce55/ce51 RPM cell V2: a halted working copy converted to a template with the same UUID; two zero-VIF, halted full deployments had distinct VM/VDI IDs, booted separately and retained the original sample checksum in offline reads. | [Templates](content/en/docs/xoa-hl/templates.md); [release run](XOA-DAILY-VALIDATION.md#track-v2-clean-guest-reboot-and-shutdown-2026-11-03) | Partial: no in-guest change in one deployment, so guest-side independence and repeatability remain open; generalization, maintenance, retirement, cross-pool and fast clone also remain gaps |
| VM07 Clone/copy | Ce55/ce51 RPM cell V2: browser Full copy of a halted VM to a named separate ext SR placed both new VDIs there; inherited VIFs were removed, isolated copy booted and offline sample checksum matched the source. | [VM operations](content/en/docs/xoa-hl/vm-operations.md); [release run](XOA-DAILY-VALIDATION.md#track-v2-clean-guest-reboot-and-shutdown-2026-11-03) | Partial: in-guest copy checksum and incomplete-copy recovery remain open; running, suspended and cross-pool modes are separate gaps |
| VM08 VM import/export | Ce55/ce51 RPM cell V2: halted uncompressed XVA export, completed one-time URL reuse HTTP 404, stopped import to named non-default SR, VIF MAC comparison/removal, isolated Ubuntu boot and offline test-file checksum passed; earlier ce40 small-disk round trip is separate. | [VM transfer](content/en/docs/xoa-hl/vm-transfer.md); [release run](XOA-DAILY-VALIDATION.md#track-v2-clean-guest-reboot-and-shutdown-2026-11-03) | Specified XVA pilot passed on this cell; incomplete transfer, OVA, URL, compression and running export remain separate gaps |
| VM09 Snapshots and revert | Ce55/ce51 RPM cell V2: stopped snapshot covered two ordinary disks; guest checksum changed A to B and returned to A after browser Revert with a before-snapshot preservation point; VM was Halted. | [VM operations](content/en/docs/xoa-hl/vm-operations.md); [release run](XOA-DAILY-VALIDATION.md#track-v2-clean-guest-reboot-and-shutdown-2026-11-03) | Partial: two cell LAN VIFs remained attached for SSH, contrary to the zero-VIF guide; snapshot cleanup/capacity and wider snapshot modes remain open |
| VM10 Migration | Source-visible, unverified: [migration mixin][migration], [actions][vm-actions] | Preview: same-pool migration in vm-transfer; cross-pool, VIF network remapping and warm migration remain gaps | Host/network/storage/CPU prerequisites, transfer interruption, guest continuity and rollback decision |
| VM11 Safe deletion | Source-visible, unverified: [Advanced][vm-advanced], [destroy implementation][vm-destroy] | Preview: stopped disposable VM removal in vm-operations; selective retention remains outside this UI pilot | Exact UUID/disks/snapshots, independent recovery copy, force-refusal, recursive snapshot cleanup, shared-disk exception and remaining-object/error inventory |

### Storage and networking — D3 #198

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| SN01 SRs/disks/ISO concepts and capacity | Ce55/ce51 RPM cell N: Local ext SR capacity matched XAPI; a controlled write exhausted the SR and returned guest I/O error; free space recovered after test-disk removal. Thin virtual disk creation overcommitted without warning and General was stale until rescan ([#372](https://github.com/Vagrantin/xcp-hl/issues/372)). | [Storage chapter](content/en/docs/xoa-hl/storage-networks.md); [run record](XOA-DAILY-VALIDATION.md#track-n-storage-and-network-2026-11-03) | Wider disk relationships, alert behavior on other SR types and human review remain open |
| SN02 Create local/shared/ISO storage | Ce55/ce51 RPM cell N: browser created NFS ISO and writable NFS SRs plus local ext SR on an identified spare disk; exact paths/PBDs and guest checksums survived guest and host restarts. ISO capacity displayed `-1 B` ([#373](https://github.com/Vagrantin/xcp-hl/issues/373)). | [Storage chapter](content/en/docs/xoa-hl/storage-networks.md); [run record](XOA-DAILY-VALIDATION.md#track-n-storage-and-network-2026-11-03) | Multi-host access, upload, failure recovery, SMB/iSCSI/ZFS, reattachment and destructive lifecycle remain open |
| SN03 Guest network interfaces | Ce55/ce51 RPM cell N: isolated no-uplink VIF, generated MAC, static guest IP/DNS, same-host HTTP peer and forbidden cell destinations checked across clean guest restart. | [Storage chapter](content/en/docs/xoa-hl/storage-networks.md#add-vif); [run record](XOA-DAILY-VALIDATION.md#track-n-storage-and-network-2026-11-03) | Cross-host paths and wider guest/network types remain open |
| SN04 Host networks/bridges/VLANs/NICs | Ce55/ce51 RPM cell N: VLAN 392 on spare nested eth1, tagged guest frames and same-host service observed; empty Interface silently dropped the VLAN, and XAPI carrier disagreed with OS link ([#374](https://github.com/Vagrantin/xcp-hl/issues/374)). | [Storage chapter](content/en/docs/xoa-hl/storage-networks.md#host-vlan-network); [run record](XOA-DAILY-VALIDATION.md#track-n-storage-and-network-2026-11-03) | Partial: second member, outer path, actual recovery, bonds and management changes remain open |
| SN05 Connectivity troubleshooting | Ce55/ce51 RPM cell N: read-only guest/VIF/network/host/PIF/appliance/NFS chain, guest IP versus XO missing report, DNS and HTTP service checks observed. | [Troubleshooting](content/en/docs/xoa-hl/troubleshooting.md#network-connectivity); [run record](XOA-DAILY-VALIDATION.md#track-n-storage-and-network-2026-11-03) | Partial: real fault/remedy, guest TLS, cross-host and missing carrier metrics remain open |

### Protection — D2 #197 / D3 #198 / D4 #199

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| BK01 Full backup and isolated restore | Source-visible, unverified: [backup editor][backup-editor], [Restore][restore] | Preview: [backup-restore](content/en/docs/xoa-hl/backup-restore.md), stopped guest/full NFS pilot | Independent remote, sample checksum, successful backup, stopped restore with all VIFs removed, console/data verification |
| BK02 Remotes beyond NFS | Source-visible, unverified: parser and pinned CIFS runtime support SMB; [remote parser][remote-parser], Windows Server warning and RPM dependency in daily validation | Preview: [smb-remote](content/en/docs/xoa-hl/backup-restore.md#smb-remote) tests one dedicated Windows Server share with remote read/write test, separate full VM job and isolated restore; Linux Samba/NAS, S3/Azure/local and production policy remain gaps | Installed CIFS helper and mount/share permissions, remote test step, full export point, stopped NIC-free restore and checksum; credential rotation, provider behavior, retention, outage and throughput remain pending |
| BK03 Schedules/retention/results | Source-visible, unverified: [backup editor][backup-editor], [schedules][backup-schedules], [scheduler][scheduler], [full writer][full-writer] | Preview: supervised scheduled full-NFS/retention-2 exercise in backup-restore; production policy, long-term/delta, outage/DST and alert delivery remain gaps | Stable schedule ID, timezone versus browser preview, automatic triggers, 3 successful runs, per-VM/schedule/remote pruning, partial failures, disable readback and isolated retained-point restore |
| BK04 Incremental/delta chains | Source-visible, unverified: delta mode/interval in [backup editor][backup-editor] and incremental runner/writer; pinned paths in daily validation | Preview: delta-backups in [backup-restore](content/en/docs/xoa-hl/backup-restore.md#delta-backups), separate disabled NFS job, stopped guest, interval 2/retention 2 and remote-chain restore; live/NBD/CBT/differential/provider scope remain gaps | Actual feature access, full/incremental/full logs, independent full backup retained, complete disk/chain identity, synchronous cleanup/retention, incremental point restored before/after retention and newest key restored with matching checksums; installed failure/recovery remains pending |
| BK05 Replication/disaster recovery | Source-visible, unverified: DR/full and CR/delta SR targets, plan conditions in [backup editor][backup-editor]; pinned full XAPI writer/replica metadata in daily validation | Preview: [dr-replica](content/en/docs/xoa-hl/backup-restore.md#dr-replica) tests DR full copies to a second disposable pool and an isolated B clone; CR, real failover/failback remain gaps | Installed DR access, source/target pool/SR identity and capacity, A/B/C full copies with retention 2, protected blocked replica, distinct stopped clone with all NICs removed before B checksum; source-pool outage, network ownership and failback pending |
| BK06 File restore | Source-visible, unverified: [file-restore UI][file-restore], pinned disk/partition/archive API and adapter in daily validation | Preview: [file-restore](content/en/docs/xoa-hl/backup-restore.md#file-restore) downloads one file from retained BK04 delta point B; full-mode XVA excluded | Installed admin/feature access, exact B/disk/partition and filesystem scan, completed tgz archive and matching file checksum; broader filesystem/tool/remote support and guest reinjection pending |
| BK07 Backup failures and restore checks | Source-visible, unverified: [backup logs][backup-logs] | Preview: full-NFS run-status/partial-result diagnosis in [troubleshooting](content/en/docs/xoa-hl/troubleshooting.md); reproduced failures, other modes and production recovery remain gaps | Exact run/VM/remote IDs, all task filters/pages and raw JSON, failed/skipped/interrupted interpretation, surviving points/partial objects, corrected non-overlapping rerun and isolated data restore |
| BK08 Appliance configuration export/import | Installed ce51 RPM appliance: UI import interrupted by xo-server SIGKILL left a measured partial users/groups state; service restarted and same file converged ([lab record](XOA-MAINTENANCE-VALIDATION.md#lab-run-2026-11-03-ce51-rpm-interrupted-import)) | Preview: [configuration-backup](content/en/docs/xoa-hl/configuration-backup.md); no automatic broad recovery claim | Interrupted ACL/job/schedule/server/remote objects and other interruption modes remain open |
| BK09 Pool metadata backup/restore | Source-visible, unverified: [metadata backup API][metadata-api], [metadata restore][metadata-restore]; pinned runner/retention details in daily validation | Preview: [pool metadata](content/en/docs/xoa-hl/configuration-backup.md#pool-metadata) uses a separate disabled pool-only job on a disposable pool and NFS remote, with three manual runs and retention 2; isolated restore and host recovery remain gaps | Installed feature access, correct pool/remote/schedule and A/B/C run logs, retained B/C `data`/`metadata.json` identity, partial failures, protected contents, then owner-reviewed isolated same-identity pool import and connectivity/inventory checks |

### Hosts and pools — D3 #198

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| HP01 Add/remove/reconnect and ownership transfer | Source-visible, unverified: [server settings][servers], [pool marking][pool-marking] | Preview: first-login/hosts-pools; #126 support policy remains distinct from observation | Old jobs/connection disabled, one manager, new inventory, no recurring old markers or duplicate jobs |
| HP02 XO Lite discovery/obsolete marker cleanup | Source-visible, unverified: [pool marking][pool-marking], separately pinned [Lite button][lite-button] | Preview: hosts-pools | Fresh/old marker, missing address/stopped appliance, exact obsolete key, reload and active-owner rewrite |
| HP03 Form/join/manage pool topology | Source-visible, unverified: [pool API][pool-api] and pinned UI/backend join path | Preview: [two-host join pilot](content/en/docs/xoa-hl/hosts-pools.md#pool-join) on rebuildable hosts; installed behavior, removal, HA and migration remain gaps | Exact pool/master/host IDs, patch difference and forced-join boundary, source connection transition, storage/network checks and failure/recovery on disposable hosts |
| HP04 Monitoring and capacity | Ce40 lab reset #176: host graphs rendered; two CPU series and host memory/free RRD values matched nested host `xe` units; [dashboard][dashboard], [host stats][host-stats], [RRD metrics][rrd-stats], [chart renderer][stats-chart] | Preview: read-only host statistics in hosts-pools; full accuracy/history, alerts, dashboard/pool aggregation and capacity diagnosis remain gaps | Other ranges and fresh timestamps, per-CPU sums, missing-data behavior, PIF/unit coverage, failure recovery and independent diagnosis |
| HP05 Host updates/maintenance | Source-visible, unverified: HomeLab [host-updates patch][host-updates] and pinned XO maintenance and patch UI/API/XAPI paths | Preview: [host maintenance/evacuation](content/en/docs/xoa-hl/hosts-pools.md#host-maintenance-mode) on a disposable two-host pool, plus [single-host patch/reboot pilot](content/en/docs/guides/updates.md#host-patch-pilot); installed evacuation, combined package transaction, reboot and recovery remain gaps | Exact host/VM/target identities, shared SR/network and capacity for evacuation; separate empty pool and console for patching, pending/installed packages, task/error, agent reconnection, reboot indication and recovery |
| HP06 HA and host failure | Source-visible, unverified: [pool Advanced][pool-advanced] and pinned enable/disable API/XAPI path | Preview: [three-host HA readiness and enable/readback/disable rehearsal](content/en/docs/xoa-hl/hosts-pools.md#ha-readiness); no host-failure or VM-restart claim | Shared heartbeat SR and each host attachment, static/redundant paths, capacity, independent consoles, installed enable/disable; separately authorized disposable failure/fencing/VM restart and recovery |

### Users and security — D3 #198 / D4 #199

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| SE01 Accounts/groups/object ACLs | Source-visible, unverified: [users][users], [ACL UI][acls], [ACL resolver][acl-resolver] | Preview: [permissions](content/en/docs/xoa-hl/permissions.md); local-group Viewer, membership removal and additive-grant pilot; provider sync/nesting/rename remain gaps | Independent normal user, allowed read/denied operation, additive group/parent grants, revocation and retained administrator |
| SE02 Delegation/resource sets | Source-visible, unverified: [self-service][resource-ui], [resource API][resource-api] | Preview: one normal user, template, SR and isolated network with CPU/RAM/disk quotas in [permissions](content/en/docs/xoa-hl/permissions.md#resource-set-delegation); group subjects, IP pools, default sharing, concurrency and production delegation remain gaps | Installed plan/menu, exact subject/object/eligible-host readback, over-limit denial without partial VM, successful stopped VM and accounting, subject removal/ACL check, VM-first cleanup and set deletion |
| SE03 External authentication | Source-visible, unverified: [SAML plugin][saml], [LDAP plugin][ldap], [plugin settings][plugins-ui] and pinned user-registration/defaults path | Preview: isolated [LDAP](content/en/docs/xoa-hl/permissions.md#ldap-sign-in) and [SAML](content/en/docs/xoa-hl/permissions.md#saml-sign-in) sign-in pilots with distinct identities and retained local admin; installed plugin/IdP behavior, group sync and production provider policy remain gaps | Confirm installed plugin/version, unique mapping/collision settings, trusted directory or signed IdP response and callback, first user role/ACL, denial/revocation, local recovery, provider outage and cleanup |
| SE04 MFA/TOTP | Installed ce51 RPM appliance: browser enrollment, fresh challenge, removal, token bypass/revocation and clock skew observed ([lab record](XOA-OTP-VALIDATION.md#lab-run-2026-11-03-ce51-rpm-otp-and-sole-admin-recovery)); wrong-code wording [#371](https://github.com/Vagrantin/xcp-hl/issues/371) | Preview: [sign-in-otp](content/en/docs/xoa-hl/sign-in-otp.md); local-account pilot passed | Provider bypass, enforced policy, FR/JA and human assistive review remain open |
| SE05 Password/admin access | Installed ce51 RPM appliance: local password change, least privilege and sole-admin recovery passed ([lab record](XOA-OTP-VALIDATION.md#lab-run-2026-11-03-ce51-rpm-otp-and-sole-admin-recovery)); direct RPM default admin [#368](https://github.com/Vagrantin/xcp-hl/issues/368), recovery CLI TTY [#369](https://github.com/Vagrantin/xcp-hl/issues/369) | Preview: first-login/permissions; corrected [recovery instructions](content/en/docs/xoa-hl/troubleshooting.md#recover-admin-access) remain draft in FR/JA | LDAP/SAML link reset, self-service reset and broader recovery remain open |
| SE06 TLS certificates/service access | Installed ce51 RPM appliance: replacement pair, endpoint trust/name verification and SSH rollback after injected mismatch passed; service-readiness defect [#370](https://github.com/Vagrantin/xcp-hl/issues/370) ([lab record](XOA-DAILY-VALIDATION.md#lab-run-2026-11-03-ce55ce51-disposable-cells)) | Preview: [read-only certificate/listener preflight](content/en/docs/xoa-hl/configuration.md#tls-certificate-preflight); rotation evidence is partial | Browser trust store, host/console after rotation, package-update persistence and independent console remain open |
| SE07 Management-network isolation | Ce40 lab reset #176: appliance browser login, connected host inventory and console WebSocket observed; lab certificate is self-signed with no SAN; no released firewall/exposure topology accepted | Preview: [read-only management path inventory](content/en/docs/xoa-hl/configuration.md#management-network); no production allowlist or policy change recipe | Agree permitted clients/services and independent console; observe listener/config, remotes and denied client; test owner-controlled rules and rollback without cutting off host management |

### Appliance operations and troubleshooting — D4 #199

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| OP01 Identify versions/settings | Source-visible, unverified: [About patch][about], [server config][server-config] | Preview: first-login/[maintenance](content/en/docs/xoa-hl/maintenance.md); configuration reference | Installed image/application/server/RPM values, effective settings and release applicability |
| OP02 Manual/automatic appliance updates | Source-visible, unverified: [update API patch][update-api], [RPM lifecycle][rpm] | Preview: updates/maintenance; host operations stay separate | Modes/channels, timezone/window, delayed/missed run, interruptions, service restart and reboot indication |
| OP03 Logs/service/reboot diagnosis | Source-visible, unverified: [RPM lifecycle][rpm], [service][service] | Preview: troubleshooting/maintenance | Sanitized service/update logs, useful symptoms, permissions and verified recovery |
| OP04 Rollback/downgrade | Not assessed as a supported recovery path | Explicit limitation in maintenance/configuration-backup/updates | Decide image/package/data compatibility; preserve data, execute isolated rollback and verify restored state before publishing a recipe |
| OP05 Fresh-image/disaster recovery | Not assessed as a complete restore procedure | Partial: deployment and configuration import preparation | Identified replacement image, preserved export/backups, isolated import, service/login/jobs/connections and data recovery |
| OP06 FAQ/failure reporting | Source-visible diagnostic paths above; remedies require their own acceptance | Preview: troubleshooting; deployment/storage/auth/backup failure coverage remains partial | Reproduce each symptom, collect sanitized identities/logs, validate remedy and success check |

### Automation, reference and contributions — D5 #200 / D6 #201 / D7 #202

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| RF01 Read-only CLI/API | Source-visible: [CLI][cli]; synthetic client/configuration checks passed, appliance unverified | Preview: [automation](content/en/docs/xoa-hl/automation.md); broader mutation examples are a gap | Real TLS/token lifecycle, permissions, request/response shapes and independent observed inventory |
| RF02 Concepts/configuration/terminology | Source-visible: pinned config and controlled glossary | Reference: concepts/configuration/[glossary](content/en/docs/xoa-hl/glossary.md) | Technical and language reviewers approve exact meaning and UI applicability |
| RF03 Availability/version/release limitations | Source pins/recipe above; no installed-availability acceptance | Reference: concepts/[release matrix](content/en/docs/reference/release-matrix.md); this D0 proposal | Agree full scope; observed release identities and supported/unavailable dispositions with evidence |
| RF04 Contributor/build architecture | Source-visible: recipe and component sources | Reference: [xoa-hl](content/en/docs/components/xoa-hl.md)/[build-xoa-hl](content/en/docs/components/build-xoa-hl.md) | Technical maintainer review; keep contributor material separate from beginner tasks |

### Explicit product/lineage boundaries

| ID / area | Disposition and evidence | Documentation decision |
| --- | --- | --- |
| BD01 XO6/latest interfaces | Outside this pin: deliberate XO5 [UPSTREAM_XO][pin] | No XO6 paths/API examples inferred from current upstream guides |
| BD02 Vates XOA updater/subscription/support | Hidden UI: XOA navigation in [menu patch][menu]; HomeLab update implementation in [update API patch][update-api] | Do not present Vates updater/subscription support as HomeLab appliance operations; hidden navigation does not prove backend absence |
| BD03 Hub/backup proxies/XOSTOR | Hidden UI: [menu patch][menu] | Not an accepted manual feature promise; independent route/backend and availability assessment needed before any future inclusion |
| BD04 Product features not enumerated above | Not assessed | Full upstream catalog is not an approved HomeLab feature promise; additions need pinned evidence and scope review |

## Coverage and decisions still required

This inventory covers the roadmap's requested **task families**. It is not an
exhaustive audit of every upstream option or a finished production manual.
Existing previews cover the beginner full-NFS journey, selected daily tasks,
maintenance/troubleshooting and read-only references. The gaps above remain
candidates for the full agreed scope; they have not been silently excluded or
approved as release features.

| Proposed next content batch | IDs / decision needed | Acceptance record |
| --- | --- | --- |
| VM completion | VM03/08/10/11 previews now have pending lab checks; broader VM05 OS/driver/upgrade scope and VM06 lifecycle/guest preparation, cross-pool migration, OVA/URL import and selective disk retention need further scope/instructions | Extend [daily validation](XOA-DAILY-VALIDATION.md) with mode-specific isolated guest checks |
| Storage/network provisioning | SN02 NFS VM-disk pilot now has pending lab checks; SN04 spare-uplink VLAN pilot now has pending lab checks; select further storage types and SN04/05 host-network/recovery scope | Host console/recovery and independent management connectivity required |
| Broader protection | BK02–07/09; agree remotes, chains, replication/DR and metadata scope | Separate backup/restore/retention/failover acceptance; full NFS results do not transfer |
| Host/pool operations | HP03 two-host join, HP04 host statistics and HP05 maintenance/patch previews await lab checks; HP06 HA and wider topology/monitoring remain gaps | Release-identified disposable hosts and explicit failure/recovery results |
| Security/delegation | SE01/02/03/04/06/07 previews have pending lab checks; broader external-auth policy, certificate rotation, wider resource-set modes, sole-admin recovery and production TLS/network scope remain gaps | Independent least-privilege sessions, real screens and retained local access |
| Recovery | OP04/05; establish supported rollback/rebuild/export boundaries | Extend [maintenance validation](XOA-MAINTENANCE-VALIDATION.md) only after isolated recovery succeeds |

No dates or named assignments are invented. Before D0 is complete, the maintainer
must record the accepted task IDs/exclusions with reasons, release applicability,
and assignments in #195. Assign English technical/chapter owners, FR/JA language
reviewers, glossary/UI coordination, publication ownership and lab operators.
All are currently **Unassigned**. For each accepted ID, link the EN/FR/JA chapter,
technical/language decision and installed lab evidence. Keep unresolved features
visible with the exact remaining question.

Use [translation review](TRANSLATION-REVIEW.md) to bind approvals to content;
source parity or test fixtures cannot supply those approvals. Screenshot/capture
infrastructure stays in `Vagrantin/jenkins-infra#87`; approved images and localized
captions belong here. No Jenkins/Playwright appliance runner is introduced.

## Source, deployment and maintenance

The canonical prose source is `Vagrantin/xcp-hl/site/`, on the Hugo branch above.
Deployment is docs-only through `Vagrantin/xcp-ce`; its old `site/` copy is stale.
The [2026-10-12 scheduled run](https://github.com/Vagrantin/xcp-ce/actions/runs/38208968908)
selected exact source `4c66ea6e05cf98c11df86ce5e34d5b0415647a1c`, passed build and
deploy (jobs `114678643179` / `114678734363`), and passed the no-RPM/.repo/repodata
guard. Live EN/FR/JA status pages each contain 16 rows. These are website checks,
not functional appliance evidence.

[xoa-hl #34](https://github.com/Vagrantin/xoa-hl/pull/34) is merged as
`9713bd7fc352444c693d0115fd53f8eec4c7e934`: UI translation CI consumes the pinned
shared glossary and reports exact-source label comparisons. Its report is still
pending human review; four inherited catalog gaps remain explicit. That newer
workflow commit does not replace the ce38 appliance evidence baseline above.

Routes remain `docs/xoa-hl/`, `fr/docs/xoa-hl/`, `ja/docs/xoa-hl/`, relative to the
actual deployment URL. Historical sources remain accessible by Git tags; parallel
versioned manuals are deferred. Old `xcp-hl/main` prose/package endpoints and
publisher-owned `docs/_data/` inputs stay outside this change.

On a release or task change, reassess the affected inventory IDs against exact
source and installed identities, update the relevant chapters/acceptance records,
and run the existing translation/build checks. Do not relabel all source-visible
features as tested when a release build or website CI passes.

## Pinned source index

Each link names the inspected repository/path at a full commit. XO links use the
XO5 pin; HomeLab modifications use the ce38 application source. The preceding
validation records supply the patched-tree observations for existing previews.

[pin]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO
[build]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh
[rpm]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec
[patches]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/metadata.toml
[image]: https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-first-boot.sh
[plan]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js
[user-api]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs
[user-ui]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js
[servers]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js
[disk-import]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js
[new-vm]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js
[console]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-console.js
[vm-actions]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js
[copy-dialog]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/copy-vms-modal/index.js
[copy-wrapper]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs
[vm-general]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js
[vm-advanced]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js
[vm-destroy]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs
[disks]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js
[vifs]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js
[vm-import]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js
[snapshots]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js
[migration]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs
[sr-general]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js
[new-sr]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js
[new-network]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/network/index.js
[host-network]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js
[backup-editor]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js
[restore]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js
[remote-parser]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-remote-parser/src/index.js
[backup-schedules]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/schedules.js
[scheduler]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs
[full-writer]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs
[file-restore]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/index.js
[backup-logs]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js
[config-ui]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js
[metadata-api]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs
[metadata-restore]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js
[pool-marking]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs
[lite-button]: https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue
[pool-api]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs
[dashboard]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/dashboard/overview/index.js
[host-stats]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js
[rrd-stats]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs
[stats-chart]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js
[host-updates]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/xcp-hl-updates.patch
[pool-advanced]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-advanced.js
[users]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js
[acls]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js
[acl-resolver]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js
[resource-ui]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/self/index.js
[resource-api]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/resource-set.mjs
[saml]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-saml/src/index.js
[ldap]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-ldap/src/index.js
[plugins-ui]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js
[otp]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js
[authentication]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs
[about]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzzzz-xoa-hl-about-page.patch
[service]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service
[server-config]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml
[update-api]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/xoa-hl-update-api.patch
[cli]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs
[menu]: https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/menu-hide-items.patch

[console-client]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/react-novnc.js
[console-gate]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs
[console-proxy]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs

[guest-metrics]: https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs

## Acceptance follow-up 2026-11-02

The [requested lab batch](XOA-DAILY-VALIDATION.md#lab-run-2026-11-02-blocked-before-reset)
was blocked before reset by the shared session preflight. No installed release
was identified and no feature status is advanced. PR #336's ce47 observations
remain separate evidence; its browser and guest-data limits still apply.
