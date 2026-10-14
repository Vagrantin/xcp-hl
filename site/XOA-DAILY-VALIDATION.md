# Daily administration preview (#189 / D3 #198)

## Scope and deployment baseline

This documentation-only batch follows merged #207, source commit
`4a4f8aab0ba314166118508bb3bcfc54a75c35f1` on
`claude/gracious-ride-99qg08`. It adds four chapters in EN/FR/JA:
VM power/snapshots/stopped clone, disk/VIF management, host/pool ownership and
users/object ACLs. French and Japanese remain drafts. The existing full NFS
backup and isolated restore chapter supplies the protection pilot; broader
backup/DR features are not silently treated as accepted.

The preceding #207 deployment was independently verified:
[xcp-ce run 38112619059](https://github.com/Vagrantin/xcp-ce/actions/runs/38112619059)
succeeded, its build log identifies `4a4f8aab0ba314166118508bb3bcfc54a75c35f1`,
and all three live maintenance pages contain the ce38 release scope. These are
website checks, not evidence of appliance operations. The new chapters require
a separate deployment after merge.

## Released source identities

| Component | Source-reviewed baseline |
| --- | --- |
| Image | `xoa-image-20261009-5f33c81` |
| Image build source | `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4` |
| Image published SHA-256 | `a9b621ce71c56445bb3998fe418cc5079c32340477a7a2830a3ef19609cfff0b` |
| Package | `v5.113.2_e281c536-ce38` |
| RPM | `xoa-hl-5.113.2_e281c536-38.g5f33c81.xcpng8.3.el9.x86_64.rpm` |
| RPM published SHA-256 | `3e85d7688664dfd55426b1d5f7e88e692c17fc4bb75d4dce31e58b9b0095bc7a` |
| Package/build source | `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19` |
| XO 5 upstream pin | 5.113.2, `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` |
| XO Lite CE release | `v0.21.0-ce29`, `ca72babb35f435b31d4726a7d1e90f42b9c06cb8` |
| XO Lite RPM | `xo-lite-ce-0.21.0-29.gca72bab.xcpng8.3.noarch.rpm` |
| XO Lite upstream tag/commit | `xo-lite-v0.21.0`, `13f987ff3d34504a90b89178489e15fa2293d1b3` |

XVA/RPM hashes are published identifiers, not locally verified payload hashes.
No released appliance was booted or operated in this batch. Review uses the
XO5 pin with the released xoa-hl patch set, not current XO6. The XO Lite CE
workflow reads UPSTREAM_TAG and applies its deployment patch to
`@xen-orchestra/lite/src/pages/xoa-deploy.vue`; its other patches target loader
and locale selection. It does not patch the reviewed `XoaButton.vue`. These
separate release scopes do not establish host/image integration compatibility.

## Source findings

Public chapters link the exact source blobs. Paths below are relative to the
specified repository. A source observation is not an installed-behavior result.

| Finding | Pinned evidence |
| --- | --- |
| Start/stop/restart, forced/bypass retry prompts; fast clone default name and full_copy=false; snapshot/revert RPCs | `XO/packages/xo-web/src/common/xo/index.js` @ `e281c536` |
| Fast clone shown for stopped VM; UI snapshot actions | `XO/packages/xo-web/src/xo-app/vm/{action-bar,tab-snapshots}.js` @ `e281c536` |
| Revert confirmation defaults snapshotBefore=true; revert of running snapshot may start/resume guest | `XO/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js`, `packages/xo-server/src/xapi/mixins/vm.mjs` @ `e281c536` |
| Disk creation selects writable SR in VM pool, name/size/read-only; separate VBD detach, disconnect and VDI delete | `XO/packages/xo-web/src/xo-app/vm/tab-disks.js`, `common/xo/index.js` @ `e281c536` |
| New VIF selects same-pool network and optional MAC; VIF removal differs from connection toggle | `XO/packages/xo-web/src/xo-app/vm/tab-network.js`, `common/xo/index.js` @ `e281c536` |
| Server connection enable/disable/remove UI and APIs | `XO/packages/xo-web/src/xo-app/settings/servers/index.js`, `common/xo/index.js`, `packages/xo-server/src/api/server.mjs` @ `e281c536` |
| Pool mark on install/interval; read-only skip; publicUrl or OS network interfaces; stale-key cleanup occurs within markPool, not in XO Lite | `XO/packages/xo-server/src/xo-mixins/xen-servers.mjs` @ `e281c536` |
| Default mark every 6h, cleanup age 48h, prefix xo:clientInfo: | `XO/packages/xo-server/config.toml` @ `e281c536` |
| Latest lastConnected marker; publicUrl preferred, otherwise eth0/first interface first address with https; button depends on address, no power/service test | `XO/@xen-orchestra/lite/src/components/XoaButton.vue` @ `13f987ff` |
| Normal User vs global Admin UI; ACL screen plan >2; no XOA_PLAN override in released package build workflow/script; upstream default 5 (OpenSource) | `XO/packages/xo-web/src/xo-app/settings/{users,acls}/index.js`, `packages/xo-web/gulpfile.js` @ `e281c536`; `xoa-hl/scripts/build-xo.sh`, `.github/workflows/build-xoa.yml` @ `5f33c81` |
| Viewer=view; Operator=view+operate; Admin adds administrate; global administrator bypass; group grants combine | `XO/packages/xo-server/src/xo-mixins/acls.mjs` @ `e281c536` |
| Parent/group/object grants may retain access after one rule is removed; multi-selection creates subject×object rules | `XO/packages/xo-acl-resolver/index.js`, `packages/xo-web/src/xo-app/settings/acls/index.js` @ `e281c536` |

#126 supplies the supported one-manager-per-host/pool policy and targeted
`xe pool-param-remove` procedure. Source review establishes the discovery
implementation; it does not independently validate the support policy or XAPI
command execution. The reviewed Lite button requires a usable address, so docs
do not claim that *every* marker guarantees an Access button. Removal of an XO
server connection stops periodic marking but does not immediately remove its
pool marker. A continuing old connection can recreate it. Cleanup here is
limited to a positively identified obsolete key after removing the old owner.

The ACL procedure uses an independent normal-user session and a single test VM.
Global Admin cannot be used to validate ACL restrictions because it bypasses
checks. Revocation checks account for groups/parent grants; no nonexistent
explicit-deny policy is promised. Source-visible plan gating is distinguished
from actual installed UI verification and from commercial Vates subscriptions.

## Website validation

The checker now requires all 13 manual pages. Meaning hashes include only each
English body and its declared glossary definitions. The entry page and new
translations were checked together before stamping their current revisions;
FR/JA remain draft. Desktop/mobile browser coverage, no-JS entry navigation,
ranked task queries and mobile Lighthouse coverage include each new chapter in
every language. Local root and subpath builds pass: 96 language switchers, 12,255 local links/assets,
45 aliases, 39 legacy paths and 53 heading/homepage anchors. Structure parity
passes for 60 translated site pages; the manual checker reports 26 drafts and
the six existing drift/publication regression cases pass. The stricter
`--require-reviewed` gate rejects the drafts as expected. Browser and remote CI
results are linked in the PR/issue comments after completion.

Initial remote CI found low contrast in shell parameter tokens (`params`,
`uuid`): Hextra's `.nv` color #008080 yields 4.42:1 on #f2f7fc. The existing
number-token fix is extended to variables at #006b6b, retaining more specific
dark-theme colors and the performance/accessibility >=95 gate. Final run
results are recorded in the PR/issue comments.

Appliance screenshot capture remains in `jenkins-infra#87`. Website smoke-test
screenshots are website evidence only; no appliance screenshot is synthesized.
No product build, deployed pool mutation, VM power operation or ACL change was
performed as part of this documentation work.

## Disposable-lab acceptance still required

The follow-up after #215 merge `2c6baa522a63ec946fca124b9f882e3080d1e255`
extends the existing VM chapter with inventory IDs **VM03** (stopped CPU/memory
changes) and **VM11** (stopped disposable VM removal). Source/UI paths and
failure boundaries are recorded below. No actual VM was resized or deleted.

D0 #195 still needs the approved shipped-feature inventory, owners, installed
release identities and locale reviewers. This batch advances D3 #198 without
closing it or #126. Record versions, timestamps, operation, expected/actual
results and sanitized task/console evidence for each scenario.

| Scenario | Acceptance required |
| --- | --- |
| Start/clean stop/restart | State/task transitions, guest shutdown/reboot and console/application result on released image |
| Guest support missing or operation blocked | Record prompt and explicitly approved fallback; test on disposable guest, without claiming force safe |
| Stopped snapshot and revert | Identify snapshot, preserve current-state choice, restored file/disk inventory, resulting power state and capacity |
| Running/memory snapshot | Separate consistency and auto-start/resume acceptance; not established by stopped pilot |
| Fast clone | Distinct VM identity, copied devices, all inherited VIFs removed before boot, verified isolation and guest identities |
| Blank test disk | Correct VM/SR/size, guest discovery, distinction between attachment removal and VDI data deletion; partial-failure inventory |
| New VIF | Correct isolated network/MAC, guest discovery, no unintended production reachability; host management remains reachable |
| Move old/new owner | Old schedules disabled and connection removed before new connection; no duplicate jobs/reconnects, correct new inventory and recovery test |
| XO Lite discovery | Recent marker/publicUrl/interface choice, stopped appliance, absent address, old marker and reload behavior |
| Marker cleanup | Exact obsolete key preserved/removed; unrelated metadata intact; active-owner rewrite and 48h cleanup during marking, not wall-clock expiry alone |
| Viewer authorization and revocation | Normal-user baseline, allowed read, denied operation/backend response without VM change, revoke/refresh and additive grant cases |
| Privilege/lockout handling | Global admin vs object role and retained administrator access; no live last-admin experiment |
| Full backup/isolated restore | Existing beginner acceptance still pending; this batch does not convert it to a passed test |
| Broader D3 features | Inventory/availability, then separate acceptance for incremental backup, replication/DR, resource sets, pool formation, HA, migration and external authentication |
| EN/FR/JA reader review | Native-language review, representative task discovery and new deployed source identity after merge |

## VM03 / VM11 source extension (2026-10-12)

Scope remains the ce38/image/XO5 identities above. All paths below are pinned
to XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`; this is code inspection, not
an installed interface or XAPI result. The exact final source/run/artifact
identities are recorded on the implementation PR.

| Finding | Pinned path |
| --- | --- |
| General displays CPU count and dynamic memory maximum, calls editVm with CPUs/memory | `packages/xo-web/src/xo-app/vm/tab-general.js` |
| Advanced current/max CPU, max editable unless Running; static/dynamic memory bounds and Remove action | `packages/xo-web/src/xo-app/vm/tab-advanced.js` |
| Numeric input saves on Enter/blur; size input saves on Enter/leaving focus | `packages/xo-web/src/common/editable/index.js` |
| UI running-state/memory errors can offer ordinary/forced setAndRestart; ordinary delete has no keep-disks control and can retry with force | `packages/xo-web/src/common/xo/index.js` |
| vm.set/delete resolve administrate permission; setAndRestart stops then defers start; delete forwards optional flags; ACL/IP/resource bookkeeping precedes VM_destroy | `packages/xo-server/src/api/vm.mjs` |
| CPUs maps to startup count; CPU maximum constraint; memory selects fixed or dynamic bounds and stopped/running setters | `packages/xo-server/src/xapi/mixins/vm.mjs` |
| Related constraint writes precede a value; independent setters use Promise.all, no automatic transactional rollback | `packages/xo-server/src/xapi/utils.mjs` |
| destroy defaults deleteDisks=true; non-Halted VM hard shutdown; VM destroyed before recursive snapshots/disks; warnings catch some cleanup errors | `@xen-orchestra/xapi/vm.mjs` |
| Disk collection selects VBD type Disk; skips a VDI attached to another non-control-domain VM | `@xen-orchestra/xapi/vm.mjs` |
| French General/Advanced/Remove labels are Général/Avancé/Supprimer; Japanese tabs are 一般/詳細設定, CPU/memory limits and Remove remain English | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

The public exercise requires a clean shutdown and recorded configuration before
resizing. It does not claim that all guests accept hotplug or that a configured
dynamic maximum is current guest RAM usage. Related values must be read back
after success and failure; a failed request does not guarantee unchanged state.

Deletion is a separate destructive procedure. The ordinary UI does not offer
selective disk retention. Passing deleteDisks=false through the API would not
establish this guide's retention workflow: recursive snapshot destruction uses
its default arguments independently. No such mutating API example is supplied.
Source-visible shared-disk skipping and caught/logged cleanup errors require
post-operation VM/snapshot/VDI inventories; neither a success notification nor
the disappearance of the VM establishes complete cleanup. Force can bypass
destroy protection and default-template checks in this source path, so the
pilot cancels a force prompt rather than treating it as a safe retry.

The API starts asynchronous ACL removal, releases VIF IP-pool assignments and
adjusts resource-set bookkeeping before invoking VM_destroy, whose destroy-block
check runs later. Resource-set restoration has failure defers, but this is not
blanket rollback of ACL/IP records. A rejected protected-VM deletion may therefore
leave the VM while changing its management records. This is a source finding;
timing and installed outcomes require the controlled acceptance scenario below.
Component verification/fix tracking is
[xoa-hl #37](https://github.com/Vagrantin/xoa-hl/issues/37). This documentation
batch reports the source finding and does not implement an appliance patch.

All scenarios below remain **Pending**. An authorized lab operator must use
disposable objects, record installed host/image/RPM/UI identities, original and
target object IDs, timestamps, expected/actual results and sanitized evidence.

| Scenario | Required observation |
| --- | --- |
| Stopped CPU increase/decrease | Current/max before/after, modest intended count, readback, guest-visible CPUs and healthy boot; no topology change |
| CPU maximum change | Stopped-state edit, constraints affecting current count, rejected value/host limits and actual resulting values |
| Stopped memory change | All static/dynamic bounds, size units, fixed/DMC starting configuration, adjusted bounds, guest boot/result and baseline restoration |
| Edit failure/partial change | Actual values after rejection, useful error and controlled recovery; no assumed transaction rollback |
| Running edit prompt | Separate authorized scenario to observe restart/force options; ordinary pilot cancels; interruption/start result if explicitly tested |
| Disposable VM removal | Halted VM, exact IDs, VBD/VDI and snapshot inventory, independent recovery copy and observed post-delete results |
| Protected VM refusal | Authorized destroy block on a test VM, refusal/force prompt cancelled; VM/protection plus ACL, IP-pool and resource-set before/after records; no assumed bookkeeping rollback |
| Shared VDI | Separate lab-approved shared-disk fixture; second guest preserved, exact retained VDI and no broad retention inference |
| Cleanup failure | Controlled disposable failure fixture, VM/snapshot/VDI leftovers and sanitized logs; no bulk-orphan deletion |
| Locale/task discovery | New memory/deletion search targets, exact installed labels, readback/warnings in EN/FR/JA; human language review remains pending |

Existing headings/routes are retained; six new ranked task queries extend the
browser check. All 32 manual FR/JA translations remain drafts. Only the changed
VM/home meaning hashes are deliberately updated after comparing all three
versions; no review record is invented or automatically promoted. The build
entry point, strict publication gate, product code/patches, publishing workflows
and release-publisher inputs are unchanged. Appliance screenshots and lab
execution remain separate work in `jenkins-infra#87` and the chapter trackers.

## VM08 / VM10 source extension (2026-10-14)

This batch follows #218 merge `9001b52dd46efb906d98c714187eda8be623a574` and adds
the EN/FR/JA chapter `vm-transfer` for inventory IDs **VM10** (migration between
hosts of the same pool) and **VM08** (uncompressed XVA export of a halted VM and
XVA file import kept stopped). Scope remains the ce38/image/XO5 identities above.
Review used the XO pin with all 14 released `xoa-hl@5f33c81` patches applied
cleanly; labels come from that patched tree. No VM was migrated, exported or
imported, and no appliance was operated.

| Finding | Pinned path (XO `e281c536` unless noted) |
| --- | --- |
| Migrate offered for Running/Halted, not Suspended/Paused, hidden for self-service users; Export/Copy need administrate | `packages/xo-web/src/xo-app/vm/action-bar.js` |
| Destination list excludes current host and can list other pools; SR required unless all disks are shared (or same host); migration network optional intra-pool | `packages/xo-web/src/common/xo/migrate-vm-modal/index.js` |
| Default migration network: pool `xo:migrationNetwork` when target PIF has an IP, otherwise none intra-pool | `packages/xo-web/src/common/xo/utils.js` |
| VM_INCOMPATIBLE_WITH_THIS_HOST leads to a force-migration confirmation | `packages/xo-web/src/common/xo/index.js` |
| vm.migrate resolves administrate on VM, target host and migration network; SR/network maps add administrate checks | `packages/xo-server/src/api/vm.mjs` |
| Any SR, network or map selects storage motion; plain pool_migrate retries with storage motion on VM_REQUIRES_SR; unmapped disks use reachable SR or pool default SR | `packages/xo-server/src/xapi/index.mjs` |
| Export dialog: xva/ova, compression Disabled (default)/GZIP/Zstd when supported; one-time tokenized download URL opened by both the dialog link and OK | `packages/xo-web/src/common/xo/{export-vm-modal/index,index}.js`, `common/select-compression.js`, `packages/xo-server/src/xo.mjs` |
| Running export uses temporary `[XO Export]` snapshot; failed cleanup only logs a warning | `@xen-orchestra/xapi/vm.mjs` |
| XVA export fails on queue when `vmExportConcurrency = 2` is reached | `packages/xo-server/src/api/vm.mjs`, `packages/xo-server/config.toml` |
| Import page: pool, writable SR (default SR proposed), `.xva`/`.ova` extensions only, single import redirects to new VM | `packages/xo-web/src/xo-app/vm-import/{index,utils}.js` |
| XVA import passes only the target SR to XAPI `/import/` | `packages/xo-server/src/xapi/index.mjs`, `@xen-orchestra/xapi/vm.mjs` |
| Start refuses duplicated MAC within the VM or with a running VM unless forced (DUPLICATED_MAC_ADDRESS) | `packages/xo-server/src/xapi/index.mjs` |
| VMware import menu entry hidden | `xoa-hl@5f33c81:patches/zzzzzzzzz-xoa-hl-hide-vmware-and-support-alert.patch` |
| FR keeps Type, Download VM, Disabled, Force migration and From URL in English; JA keeps the migrate dialog labels in English | patched `packages/xo-web/src/common/intl/locales/{fr,ja}.js` |

The guide does not assert whether XAPI regenerates or preserves MAC addresses on
XVA import; it requires removing every inherited VIF before the first start
instead. Compressed XVA import, OVA, URL import, cross-pool migration and VIF
network remapping are explicit gaps, not unavailable features.

Website validation: both URL shapes build (108 switchers, about 15,170 local
links/anchors), 68-page parity, 34 drafts, 14 manual regressions and the glossary
test pass. Locally, the full browser smoke test passes 47 ranked queries,
including new `migrate`/`migrer`/`マイグレーション` targets, and the keyboard/reflow
checks cover 16 pages per locale. The French title uses nouns so that the existing
`exporter` query still ranks the configuration export guide first.

All scenarios below remain **Pending**.

| Scenario | Required observation |
| --- | --- |
| Same-pool live migration, shared SR | Pool/host identities, pool_migrate task, brief pause, guest console/network/application continuity |
| Same-pool migration, local disk | Required SR, per-VDI targets, copy duration/capacity, final disk locations and source SR leftovers |
| Automatic VM_REQUIRES_SR retry | Observed retry path, chosen SR and resulting disk placement |
| Incompatible host | Force prompt shown and cancelled; VM unchanged |
| Halted XVA export | Default options, filename, size, checksum, one-time link reuse refused |
| Export concurrency | Third concurrent export fails, then succeeds after running exports end |
| Running export | `[XO Export]` snapshot appears and is removed; leftover handling on interrupted download |
| XVA import | Target SR, new VM ID/name, power state after import, VIF MACs compared with source |
| Duplicate MAC start | Refusal with source running and import VIF kept; success after VIF removal |
| Failed/interrupted import | Leftover VM/VDI inventory and positively identified cleanup |
| EN/FR/JA labels | Installed labels match the guide; human language review remains pending |

## SN02 NFS ISO library extension (2026-10-14)

After #222 merged as `da5cccb6b088af623bb440632c2171f2e7ffd780`, the existing EN/FR/JA
storage/network chapter adds a dedicated-export NFS ISO connection/rescan pilot.
The beginner guide links it and permits existing verified media to skip upload.
Scope remains the ce38/image/XO5 pins above. No SR, NAS, host or guest was operated;
all installed, screenshot and human language acceptance remains Pending.

Review used the patched XO tree at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`:

| Finding | Pinned source path |
| --- | --- |
| Admin-only New/Storage, `/#/new/sr`; ISO SR group offers Local/NFS ISO/SMB ISO separately from VDI SR | `packages/xo-web/src/xo-app/{menu/index,new/sr/index}.js` |
| NFS version default/4/4.1; changing version does not rerun discovery. Root export search and selected path trigger distinct probes; Summary shows name/description/type, not the server or host | `packages/xo-web/src/xo-app/new/sr/index.js` |
| Even `nfsiso` uses `sr.probeNfs`/`sr.probeNfsExists`, which probe XAPI's `nfs` type. Returned UUIDs must not be assumed ISO libraries | `packages/xo-web/src/xo-app/new/sr/index.js`, `packages/xo-server/src/api/sr.mjs` |
| ISO create sends location server:path (bracketed IPv6), optional nfsversion/options, `content_type: iso`, `type: iso`, `shared: true` for NFS; requires administrate on selected host. Reattach branch differs and is outside pilot | `packages/xo-web/src/common/xo/index.js`, `packages/xo-server/src/api/sr.mjs` |
| SR refresh calls `sr.scan` → async SR.scan. Hosts tab shows per-PBD location and attached state; shared metadata is not installed access acceptance | `packages/xo-web/src/xo-app/sr/{action-bar,tab-host}.js`, `packages/xo-server/src/api/sr.mjs` |
| Import selector only tests positive SR size; it does not verify media-writing capability. ISO file upload invokes VDI.create and RAW import; host storage-driver acceptance is separate | `packages/xo-web/src/common/xo/index.js`, `packages/xo-web/src/xo-app/disk-import/index.js`, `packages/xo-server/src/api/disk.mjs` |
| VM ISO selection requires a present VDI in an iso-type SR in the chosen pool | `packages/xo-web/src/xo-app/new-vm/index.js` |
| NFS ISO/group/type strings are fixed English. FR NFS version/options fall back; JA Hosts, Connected, Disk/Disks and Rescan all disks remain English | patched `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

These source findings do not prove an NFS server/version, discovery response,
host driver, write permissions or pool-wide attachment behavior on an installed
release. The pilot stops on failed discovery or unexpected existing SRs; it does
not recommend reattachment or destructive recreation as recovery. NAS setup,
subdirectories, local/SMB/block provisioning and SR cleanup remain separate gaps.
The server-held ISO is verified using its vendor checksum before guest use;
rescan/name/size checks alone are not integrity acceptance.

| Pending scenario | Required observations |
| --- | --- |
| Dedicated NFS ISO export | NAS/export identity, agreed version, host identities/access policy, complete vendor-verified file |
| Discovery and version changes | Export found from selected host; rerun after version changes; failed/empty discovery handling; actual response to an ISO-only export |
| Creation | One SR UUID, iso backend type, server/path, selected host; no duplicate creation |
| Per-host access | Each intended PBD's location/Connected state and guest media read; never infer from shared flag or appliance reachability |
| Existing-SR detection | Detected UUID/type verified independently; stop without reattach/overwrite or formatting |
| Rescan | Media visible after complete file placement and scan; no checksum claim from a filename |
| New VM use | Same pool, present installer selected, intended host boots test installer; eject before cleanup |
| Read versus upload | Existing-media read accepted separately; upload/VDI-create/RAW-write support remains unvalidated, including read-only export behavior |
| Failure/partial creation | Record error plus SR/PBD identities before retry; no destructive cleanup of unidentified objects |
| EN/FR/JA acceptance | Installed literal labels, human technical/language review, sanitized images and assistive/browser UI zoom checks |

Website validation retains 18 pages per locale / 36 draft translations. Three
ranked ISO-library queries extend the existing browser cases. The accessibility
log now derives its page count from its actual route list, avoiding the stale
literal count left by earlier chapter additions. No publication gate, release
input, product code or appliance screenshot runner changes are included.

Mobile visual review found that Hextra’s trailing ID span and fixed negative
offset could hide a wrapped section heading behind the navbar. The CSS anchors
the existing span at the heading top with measured navbar clearance; IDs and
URLs stay the same. Browser CI follows the new beginner fragment link in all
three locales at 390/320px and checks the heading is below the navbar.
The navbar height observer also corrects a hash heading still visibly covered
when the bar grows after initial positioning. It does not jump back to a
heading already above the viewport. Local checks exercise both initial fragment
loads and the beginner link after changing between 390/320px.
