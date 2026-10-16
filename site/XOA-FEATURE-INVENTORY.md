# Released-source feature and chapter inventory — D0 #195 / #189

This is a **scope proposal for review**, assessed on 2026-10-12. It inventories
the tasks requested by #189, maps the existing EN/FR/JA preview chapters, and
identifies the checks needed before production acceptance. No appliance was
booted or operated for this inventory. No owner or language reviewer has been
assigned. Approval of the full content scope remains pending in #195.

## Baseline and evidence meaning

The latest **source-reviewed baseline used by this manual** remains image
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
FR/JA manual pages remain drafts; structural parity is not human language review.

### Start here — D2 #197

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| ST01 Deploy/import XOA-HL | Source-visible, unverified: separate image/deployment flow; [image source][image] | Preview: [start](content/en/docs/start/_index.md); image failure handling is partial | Identified XVA/host, intended network/credentials, first boot and interrupted import |
| ST02 First login and password change | Source-visible, unverified: [user API][user-api] | Preview: [first-login](content/en/docs/xoa-hl/first-login.md) | Deployment credentials, independent web/SSH/host identities, new password and retained admin access |
| ST03 Connect a host/pool | Source-visible, unverified: [server settings][servers] | Preview: first-login; [hosts-pools](content/en/docs/xoa-hl/hosts-pools.md) | Intended pool/SR inventory, TLS/credentials and reconnect failure |
| ST04 Choose documentation/UI language | Source-visible, unverified UI preference: [User page][user-ui]; documentation switching has website tests | Preview: first-login; [manual entry](content/en/docs/xoa-hl/_index.md) | Real UI EN/FR/JA labels; documentation language remains independent |
| ST05 Import ISO and create/install first VM | Source-visible, unverified: [ISO import][disk-import], [new VM][new-vm] | Preview: [create-vm](content/en/docs/xoa-hl/create-vm.md); existing-media NFS ISO setup is linked; writable ISO upload remains a separate prerequisite | ISO identity/SR, template/resources, console installation, media ejection and installed guest boot |

### Virtual machines — D3 #198

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| VM01 Console access | Source-visible, unverified: [Console tab][console], [console client][console-client], [operate gate][console-gate], [host proxy][console-proxy] | Preview: vm-console in [vm-operations](content/en/docs/xoa-hl/vm-operations.md), linked from create-vm/troubleshooting; guest/client/browser acceptance remains pending | Running/disabled state, operate permission, browser-appliance-host route, display versus input, harmless clipboard, local-client separation, restart/reopen and owner-selected remedy |
| VM02 Start/stop/reboot | Source-visible, unverified: [actions][vm-actions] | Preview: [vm-operations](content/en/docs/xoa-hl/vm-operations.md) | Guest clean shutdown, task/state result; forced fallback needs separate explicit approval |
| VM03 Change CPU/RAM | Source-visible, unverified: [General][vm-general], [Advanced][vm-advanced] controls | Preview: stopped CPU/memory exercise in vm-operations; hotplug/DMC/load/topology remain gaps | Current/max CPU, ordered static/dynamic memory bounds, host capacity, related-limit readback, guest-observed result and recorded-baseline recovery |
| VM04 Add/remove disks and NICs | Source-visible, unverified: [Disks][disks], [Networks][vifs] | Preview: [storage-networks](content/en/docs/xoa-hl/storage-networks.md) | Guest discovery, correct VM/SR/network, detach versus data deletion and management connectivity |
| VM05 Guest tools | Source-visible, unverified: [General detection][vm-general], [guest-metrics mapping][guest-metrics], [Advanced fields][vm-advanced]; Ubuntu Noble package 7.20.2-0ubuntu1 | Preview: [guest-tools](content/en/docs/xoa-hl/guest-tools.md), fresh Ubuntu 24.04 amd64 management-agent install/status and clean-stop/boot pilot; other OSes, ISO path, drivers, upgrades/removal and supported guest matrix remain gaps | Package origin/version, xe-daemon/proc-xen unit state, PV versus agent detection, refreshed OS/kernel/IP observations, ordinary stop without force, boot/service persistence and failure/recovery evidence |
| VM06 Templates | Source-visible, unverified: [Advanced conversion][vm-advanced], [VM API][migration] and [new VM][new-vm] | Preview: [templates](content/en/docs/xoa-hl/templates.md), stopped disposable-copy conversion and two console-only deployments; guest generalization, in-place maintenance, retirement, cross-pool and fast-clone behavior remain gaps | VM/pool administration, same conversion UUID, preserved original, persisted template selection, explicit startup/copy/network settings, separate VM/VDI IDs, two isolated guest/checksum checks and failure inventories |
| VM07 Clone/copy | Source-visible, unverified: [actions][vm-actions], [copy dialog][copy-dialog], [copy API][migration], [copy wrapper][copy-wrapper] | Preview: stopped fast clone and same-pool full-copy pilot in vm-operations; running/suspended, cross-pool/template copies and snapshot-history preservation remain gaps | Distinct VM/VDI IDs, selected same-pool writable SR, capacity/host access, all inherited VIFs removed before boot, file checksum, source preservation and incomplete-copy inventory |
| VM08 VM import/export | Source-visible, unverified: [import][vm-import], [export action][vm-actions] | Preview: [vm-transfer](content/en/docs/xoa-hl/vm-transfer.md), uncompressed XVA export of a halted VM and XVA file import kept stopped; OVA, URL, compressed XVA, running export and disk-only paths remain gaps | Format/target resources, incomplete transfer, isolated imported VM and verified guest/data |
| VM09 Snapshots and revert | Source-visible, unverified: [Snapshots][snapshots], [VM API][migration], [disk-name exclusion/cleanup][vm-destroy] | Preview: stopped/no-VIF snapshot, checksum revert and single-test-point cleanup in vm-operations; live/memory, shared/excluded disks and backup-managed cleanup remain gaps | VM/snapshot UUIDs, ordinary disk coverage and [NOSNAP] name check, pre-revert point readback, guest checksum, VIF/power-state readback, partial-failure inventory and cleanup errors/capacity |
| VM10 Migration | Source-visible, unverified: [migration mixin][migration], [actions][vm-actions] | Preview: same-pool migration in vm-transfer; cross-pool, VIF network remapping and warm migration remain gaps | Host/network/storage/CPU prerequisites, transfer interruption, guest continuity and rollback decision |
| VM11 Safe deletion | Source-visible, unverified: [Advanced][vm-advanced], [destroy implementation][vm-destroy] | Preview: stopped disposable VM removal in vm-operations; selective retention remains outside this UI pilot | Exact UUID/disks/snapshots, independent recovery copy, force-refusal, recursive snapshot cleanup, shared-disk exception and remaining-object/error inventory |

### Storage and networking — D3 #198

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| SN01 SRs/disks/ISO concepts and capacity | Source-visible, unverified: [SR General][sr-general], [Disks][disks] | Reference: [concepts](content/en/docs/xoa-hl/concepts.md); preview: storage-networks | Observed SR/disk relationships, writable/free capacity, alerts and failed allocation |
| SN02 Create local/shared/ISO storage | Source-visible, unverified: [new SR][new-sr] | Preview: NFS ISO library connection/rescan and dedicated empty-export NFS VM-disk SR creation/readback in storage-networks; local/SMB/iSCSI, subdirectories, reattachment and destructive SR lifecycle remain gaps | NFS host targets/admin/export permissions, existing-SR stop, type/path/PBD/capacity readback, test-disk persistence and partial-failure inventory; all installed checks pending |
| SN03 Guest network interfaces | Source-visible, unverified: [Networks][vifs] | Preview: isolated VIF in storage-networks | Correct pool network, MAC, guest IP/DNS and no unintended production reachability |
| SN04 Host networks/bridges/VLANs/NICs | Source-visible, unverified: [new network][new-network], [host networking][host-network] | Preview: dedicated spare-uplink tagged guest VLAN in [storage-networks](content/en/docs/xoa-hl/storage-networks.md#host-vlan-network); bonds, host IP/management changes and destructive lifecycle remain gaps | Disposable pool/independent console, per-host PIF/VLAN/MTU/carrier/attachment readback, approved switch topology, guest traffic/isolation/persistence and actual recovery; all installed checks pending |
| SN05 Connectivity troubleshooting | Source-visible, unverified: [VIFs][vifs], [host networking][host-network], [server settings][servers] | Preview: network-connectivity in [troubleshooting](content/en/docs/xoa-hl/troubleshooting.md#network-connectivity), read-only ordinary guest/VLAN path diagnosis; bonds/SDN/trunks and emergency recovery remain gaps | Exact source/destination/service, VIF/network/resident-host/PIF mapping, guest metrics versus IP policy, attachment versus carrier/missing metrics, guest DNS/route/TLS/service results and owner-selected remedy with isolation/management/storage rechecks; all installed scenarios pending |

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
| BK08 Appliance configuration export/import | Source-visible, unverified: [configuration UI][config-ui] | Preview: [configuration-backup](content/en/docs/xoa-hl/configuration-backup.md); isolated import preparation only | Export contents/secret handling, isolated import, recreated connection/ACL/job state; no automatic broad recovery claim |
| BK09 Pool metadata backup/restore | Source-visible, unverified: [metadata backup API][metadata-api], [metadata restore][metadata-restore]; pinned runner/retention details in daily validation | Preview: [pool metadata](content/en/docs/xoa-hl/configuration-backup.md#pool-metadata) uses a separate disabled pool-only job on a disposable pool and NFS remote, with three manual runs and retention 2; isolated restore and host recovery remain gaps | Installed feature access, correct pool/remote/schedule and A/B/C run logs, retained B/C `data`/`metadata.json` identity, partial failures, protected contents, then owner-reviewed isolated same-identity pool import and connectivity/inventory checks |

### Hosts and pools — D3 #198

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| HP01 Add/remove/reconnect and ownership transfer | Source-visible, unverified: [server settings][servers], [pool marking][pool-marking] | Preview: first-login/hosts-pools; #126 support policy remains distinct from observation | Old jobs/connection disabled, one manager, new inventory, no recurring old markers or duplicate jobs |
| HP02 XO Lite discovery/obsolete marker cleanup | Source-visible, unverified: [pool marking][pool-marking], separately pinned [Lite button][lite-button] | Preview: hosts-pools | Fresh/old marker, missing address/stopped appliance, exact obsolete key, reload and active-owner rewrite |
| HP03 Form/join/manage pool topology | Source-visible, unverified: [pool API][pool-api] | Reference only; pool formation is a gap | Pool prerequisites, master/host identities, storage/network implications and failure/recovery on disposable hosts |
| HP04 Monitoring and capacity | Source-visible, unverified: [dashboard][dashboard], [host stats][host-stats], [RRD metrics][rrd-stats], [chart renderer][stats-chart] | Preview: read-only host statistics in hosts-pools; installed accuracy/history, alerts, dashboard/pool aggregation and capacity diagnosis remain gaps | Host identity, selected range/AVERAGE spacing, fresh timestamps, per-CPU versus sums, memory missing-data behavior, PIF/unit coverage and independent diagnosis |
| HP05 Host updates/maintenance | Source-visible, unverified: HomeLab [host-updates patch][host-updates] | Preview: [updates](content/en/docs/guides/updates.md); evacuate/maintenance workflow is partial | Identified host packages, guest handling, combined stock/HomeLab updates, interruption, reboot and recovery |
| HP06 HA and host failure | Source-visible, unverified: [pool Advanced][pool-advanced] | Gap: not established by pool discovery or VM migration source | Shared heartbeat storage, capacity/fencing prerequisites, authorized disposable failure scenario and recovery |

### Users and security — D3 #198 / D4 #199

| ID / task | Source observation | Current chapter / gap | Functional acceptance needed |
| --- | --- | --- | --- |
| SE01 Accounts/groups/object ACLs | Source-visible, unverified: [users][users], [ACL UI][acls], [ACL resolver][acl-resolver] | Preview: [permissions](content/en/docs/xoa-hl/permissions.md); local-group Viewer, membership removal and additive-grant pilot; provider sync/nesting/rename remain gaps | Independent normal user, allowed read/denied operation, additive group/parent grants, revocation and retained administrator |
| SE02 Delegation/resource sets | Source-visible, unverified: [self-service][resource-ui], [resource API][resource-api] | Preview: one normal user, template, SR and isolated network with CPU/RAM/disk quotas in [permissions](content/en/docs/xoa-hl/permissions.md#resource-set-delegation); group subjects, IP pools, default sharing, concurrency and production delegation remain gaps | Installed plan/menu, exact subject/object/eligible-host readback, over-limit denial without partial VM, successful stopped VM and accounting, subject removal/ACL check, VM-first cleanup and set deletion |
| SE03 External authentication | Source-visible, unverified: [SAML plugin][saml], [LDAP plugin][ldap], [plugin settings][plugins-ui] | Gap: packaged workspaces do not establish configured authentication/provider support | Choose providers; installed plugin/configuration, TLS, mappings, lifecycle, outage and retained local access |
| SE04 MFA/TOTP | Source-visible, unverified: [OTP UI][otp], [User gate][user-ui], [authentication][authentication] | Preview: [sign-in-otp](content/en/docs/xoa-hl/sign-in-otp.md), local-account enrollment, fresh login, token limitations and removal; installed acceptance and sole-admin recovery remain gaps | Enrollment, fresh-login challenge, removal/recovery, time sync and token/provider bypass boundaries |
| SE05 Password/admin access | Source-visible, unverified: [user API][user-api] | Preview: first-login/permissions; external-account reset and lockout are gaps | Correct account type, password change/relogin, local recovery and least privilege |
| SE06 TLS certificates/service access | Source-visible, unverified: [package bootstrap][build], [service][service], [server config][server-config] | Reference/preview: [configuration](content/en/docs/xoa-hl/configuration.md), maintenance | Installed listener/certificate/expiry, client trust/name, safe rotation, restart and console restoration |
| SE07 Management-network isolation | Not assessed: no released firewall/exposure topology accepted | Partial prerequisites; hardening task guide is a gap | Agree permitted clients/ports and console path; verify firewall/reachability without cutting off host management |

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
| Host/pool operations | HP03–06; agree topology, monitoring, maintenance and HA scope | Release-identified disposable hosts and explicit failure/recovery results |
| Security/delegation | SE01/02/04 previews have pending lab checks; SE03/06/07, external authentication, wider resource-set modes, sole-admin recovery and TLS/network scope remain gaps | Independent least-privilege sessions, real screens and retained local access |
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
