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

No-JavaScript fragment checks cover the same mobile widths/locales. Without a
height observer, the anchor uses an 8rem fallback to clear the wrapped navbar.

## SE01 local groups and ACL extension (2026-10-14)

After #223 merged as `ac3ed5868031742501c5844d6b1860d2a2553dcd`, the existing
EN/FR/JA permissions chapter adds a local-group Viewer pilot. Source scope stays
ce38/image/XO5 above. No account, group, ACL or VM was operated. All lab and human
language acceptance remains Pending; this is not an installed authorization test.

Review uses XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` with the ce38 HomeLab
patches applied. Group UI/API/subjects/ACL aggregation/resolver paths are unchanged
by those patches; labels were read from the patched catalogs.

| Finding | Pinned source path |
| --- | --- |
| Settings is admin-only; Groups route is `/#/settings/groups`. New groups start without members; names are unique | `packages/xo-web/src/xo-app/settings/{index,groups/index}.js`, `packages/xo-server/src/models/group.mjs` |
| Group membership selector accepts users not already present, not groups. Selecting sends add immediately; expanding count exposes remove buttons without a confirmation | `packages/xo-web/src/xo-app/settings/groups/index.js`, `packages/xo-web/src/common/xo/index.js` |
| Users group-count tooltip reads user.groups; group member list reads group.users. Add/remove await independent writes to both collections, with no transaction/compensation in these methods | `packages/xo-web/src/xo-app/settings/users/index.js`, `packages/xo-server/src/xo-mixins/subjects.mjs` |
| Group create/add/remove/set/delete APIs require global admin. Add/remove/rename reject provider-synchronized groups; local UI hides their name/member controls | `packages/xo-server/src/api/group.mjs`, `packages/xo-web/src/xo-app/settings/groups/index.js` |
| ACL selector combines users/groups. Multiple subjects × objects creates multiple independent requests. Group grants and direct user grants are unioned; global admin bypasses object checks | `packages/xo-web/src/common/select-objects.js`, `packages/xo-web/src/xo-app/settings/acls/index.js`, `packages/xo-server/src/xo-mixins/acls.mjs` |
| Object access may also come from parent/container relations; a group adds subjects, not a broader object scope or deny rule | `packages/xo-acl-resolver/index.js`, `packages/xo-server/src/xo-mixins/acls.mjs` |
| Group-delete confirmation is generic, not a name-bearing strong confirmation. Backend removes group then starts ignored-error asynchronous ACL/user membership cleanup | `packages/xo-web/src/common/xo/index.js`, `packages/xo-server/src/xo-mixins/subjects.mjs` |
| ACL display filters rows whose subject/object/action cannot be resolved; a vanished row after subject deletion is not proof of database cleanup | `packages/xo-web/src/xo-app/settings/acls/index.js` |
| FR has Paramètres/Utilisateurs/Groupes/Droits and global Utilisateur/Administrateur; object role names remain Viewer/Operator/Admin. JA has 設定/ユーザー一覧/グループ一覧/ACL一覧 but group columns/actions and global User/Admin remain English | patched `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

The guide separates group membership from account-global permissions and
object scope. It requires an independent normal nonmember control, readback of
both membership views, expected retained access through a direct grant and
revocation checks. Cleanup removes the known test ACLs while subjects still
exist, then memberships, then the empty group. This avoids treating the group's
disappearance as proof of asynchronous cleanup. Unexpected success, errors or
inconsistent records stop the exercise instead of triggering broader grants.
Group nesting, rename, provider synchronization, quotas/resource sets and wider
delegation remain separate gaps; local group visibility is not provider support.

| Pending scenario | Required observation |
| --- | --- |
| Baseline | Retained administrator; two normal accounts; no alternate grant to the disposable VM |
| Empty local group | Unique name, no members, group Viewer row grants neither test account access |
| Membership add | Exact login in group.users view and group in user.groups view; global permission unchanged |
| Member/nonmember authorization | Member reads VM; forbidden operations refused without changing it; control remains denied |
| Membership removal | Both views updated; former member loses group-derived access; ACL still exists for other members |
| Additive grants | Direct Viewer preserves access after group ACL removal; removing direct ACL denies with no other grants |
| Errors/partial writes | Sanitized error and both records plus independent effective access recorded before retry |
| Cleanup | Known ACLs/memberships removed first; empty group deleted; residual records checked rather than inferred from hidden rows |
| Provider boundary | Locally created group only; sync/provider detach not used to bypass restrictions |
| EN/FR/JA review | Installed exact labels; named technical/language review; sanitized screenshots and assistive acceptance |

Three ranked groups/groupes/グループ queries extend the existing browser suite.
The manual remains 18 pages per locale / 36 draft translations, with new meaning
hashes only for permissions and the changed manual entry. Shared glossary,
publication gate, product code, release inputs and screenshot backend are unchanged.

## VM07 same-pool full-copy extension (2026-10-14)

After #224 merged as `5df1c0824aa9149a5d4c4fec13e2dd0c30a72878`, the existing
EN/FR/JA VM operations guide adds a `full-copy` subsection under section 5.
Existing numbered sections and routes remain intact. The exercise uses one
halted disposable VM and a different writable VM-disk SR in the same pool.
Source scope remains image `xoa-image-20261009-5f33c81` / ce38 / XO 5.113.2 above.
No VM, VDI, VIF, SR or appliance was operated; all installed and human language
acceptance remains **Pending**.

Review used XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` with all 14 released
HomeLab patches applied. Those patches do not change the copy dialog, action,
API or XAPI wrapper paths below. Catalog observations use the patched tree.

| Finding | Pinned source path (XO `e281c536`) |
| --- | --- |
| Copy offered for Running/Halted/Suspended, hidden for self-service users and gated by administrate; ordinary fast-clone action shown for Halted | `packages/xo-web/src/xo-app/vm/action-bar.js` |
| Copy dialog defaults fullCopy, `{name}_COPY` and disabled compression; empty name preserves original; absent target SR returns no usable full-copy selection | `packages/xo-web/src/common/xo/copy-vms-modal/index.js` |
| Fast clone mode calls vm.clone with full_copy=false; full copy requires selected SR and calls vm.copy; no start request follows these calls | `packages/xo-web/src/common/xo/index.js` |
| SR selector defaults to writable storage; restricted effective UI plans constrain it to source pool, otherwise other pools can appear | `packages/xo-web/src/common/{select-objects,xoa-plans}.js`, `common/xo/copy-vms-modal/index.js` |
| vm.copy resolves administrate on VM and operate on target SR; same pool uses copyVm, different pool uses remoteCopyVm; resource-set support remains TODO | `packages/xo-server/src/api/vm.mjs` |
| Fast clone invokes VM.clone; normal copy invokes VM.copy with chosen SR. Running copy takes a temporary snapshot and destroys it in finally; remote copy uses export/import | `packages/xo-server/src/xapi/index.mjs` |
| Same-pool copy does not consume compression. `_copyVm` does not supply a compensating cleanup for failed VM.copy; wrapper completion is not installed disk/guest acceptance | `packages/xo-server/src/xapi/index.mjs`, `packages/xo-server/src/api/vm.mjs` |
| FR action Copier differs from dialog Fast clone/Full copy fallback labels; dialog Copier la VM/Nom/Sélectionner le SR. JA action 仮想マシンの複製; Copy VM/Name/Select SR and modes remain English; 圧縮 is localized. Disabled remains English in both | patched `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

The guide distinguishes the direct Fast clone action from the dialog's two modes,
and explicitly selects the same-pool destination instead of inferring scope from
the dialog. Its chosen SR receives the ordinary copied disk VDIs. The UI's
writable filter is not proof of host reachability or sufficient unreserved
capacity; each remains an installed prerequisite and readback check.

There is no claim that all snapshots are copied, MACs are regenerated, a failed
request leaves no objects, or the new VM's power state is proven by source alone.
The pilot verifies Halted, distinct VM and VDI IDs, disk count/sizes/SRs and source
preservation, then removes every inherited VIF before first boot. Guest file
checksum and console/application checks establish the intended data comparison
only when actually performed. Same-pool copy is not independent backup/DR
acceptance. Running/suspended copies, cross-pool or template copies, shared or
passthrough disks, snapshot history and SR-loss recovery remain separate gaps.

| Pending scenario | Required observation |
| --- | --- |
| Baseline and capacity | Installed identities, administrator, cleanly halted disposable VM, source IDs/disks/VIFs/snapshots, harmless file checksum; different same-pool writable SR and intended-host access/capacity |
| Name and mode selection | Exact action/dialog labels, unique name, default pattern/empty-name behavior, Full copy selected, target ID/pool and Disabled compression |
| Missing/invalid target | No target causes refusal/error without a claimed complete copy; read back inventories before retry; distinguish writable filter from actual access |
| Successful full copy | New distinct VM/VDI IDs, Halted readback, each disk's size and selected SR, original VM/disk preservation |
| First boot and data | Every inherited VIF removed and empty list read back before boot; isolated console, matching file checksum, guest disks/application and duplicate-identity handling |
| Error/interruption | Sanitized error and source/destination VM/VDI/snapshot inventories, capacity/connectivity diagnosis; no rollback or absence-of-leftovers inferred |
| Cleanup | Exact copy IDs, clean stop, section 7 removal and remaining-object inventory; source and independent recovery copy preserved |
| Boundary scenarios | Separate authorization and acceptance for running/suspended/cross-pool/template copies, snapshots, shared/passthrough disks or SR loss; no transfer of pilot results |
| EN/FR/JA review | Installed literal labels, named technical/language review, sanitized appliance captures and assistive acceptance |

Three new ranked full copy/copie complète/フルコピー queries extend the browser
suite without changing search ranking. The manual stays at 18 pages per locale
and 36 FR/JA drafts. Only VM operations and the changed home entry receive new
meaning hashes after comparing all three versions. The shared glossary, review
manifest, strict publication gate, product/release/build/publishing code and
appliance capture backend are unchanged. Final-head website CI/artifact results
are recorded on the implementation PR and #189/#198 after verification.

## HP04 read-only host-statistics extension (2026-10-14)

After #225 merged as `ef26680b78ed608de3bc51f91286aa39822d984d`, the existing
EN/FR/JA hosts/pools chapter adds section 5, `host-statistics`. It observes one
known running host's charts without changing host, VM, network or storage state.
The released source baseline remains image `xoa-image-20261009-5f33c81` / ce38 /
XO 5.113.2 above. No host statistics, capacity or installed metric accuracy was
actually observed; all functional and human language acceptance is **Pending**.

Review used XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` with the ce38
patches applied. The stats paths below are unchanged by the released HomeLab
patches, while catalog labels were read after patching.

| Finding | Pinned path (XO `e281c536`) |
| --- | --- |
| Host route has a Stats tab. Parent fetches default overview and the tab can reuse matching-interval overview data; tab skips non-running hosts | `packages/xo-web/src/xo-app/host/{index,tab-stats}.js` |
| Default Last 10 minutes/seconds; 5s, 60s, 3600s, 86400s polling/spacing; Last day uses hours with keep=24; week uses hours, year uses days | `packages/xo-web/src/common/stats.js`, `xo-app/host/tab-stats.js` |
| host.stats requires view on the host; xen-servers mixin delegates to the RRD helper | `packages/xo-server/src/api/host.mjs`, `xo-mixins/xen-servers.mjs` |
| Helper uses host server time and /rrd_updates cf=AVERAGE, requested interval/history; validates actual step, filters host UUID/metric names, reverses data and retains endTimestamp/interval; cache is interval-bound | `packages/xo-server/src/xapi-stats.mjs` |
| Chart timestamps derive from endTimestamp/interval, formatted by react-intl; provider sets locale without an explicit timeZone | `packages/xo-web/src/common/xo-line-chart/index.js`, `common/intl/index.js` |
| CPU metrics multiplied by 100, individual chart max 100; toggle adds All Cpus sum, not a normalized average. Combined scale uses stats.length, whereas this helper builds keyed CPU series; actual axis behavior needs acceptance rather than assuming a working CPU-count cap | `packages/xo-server/src/xapi-stats.mjs`, `packages/xo-web/src/common/{xo-line-chart/index,xo-stats}.js` |
| Host RAM uses memory_total_kib/free_kib ×1024; memory renderer subtracts free from total. Missing memoryFree defaults to memory, yielding zero used memory | `packages/xo-server/src/xapi-stats.mjs`, `packages/xo-web/src/common/{utils,xo-line-chart/index}.js` |
| parseNumber maps NaN to null; CPU/memory unit transforms can multiply null into zero. A displayed zero does not independently establish inactivity | `packages/xo-server/src/xapi-stats.mjs` |
| PIF matching is pif_eth<number>_rx/tx; renderer names eth/All rx/tx series and formats sizes in bytes, not formatSpeed. Mbps/Gbps conversion and bond/VLAN completeness are not accepted by this pilot | `packages/xo-server/src/xapi-stats.mjs`, `packages/xo-web/src/common/{xo-line-chart/index,utils}.js` |
| Load chart uses host loadavg, a separate metric. Chart/initial missing-state message is literal No stats. | `packages/xo-server/src/xapi-stats.mjs`, `packages/xo-web/src/xo-app/host/tab-stats.js`, `common/xo-line-chart/index.js` |
| Tab sets statsIsPending before fetch and clears it only on fulfilled promise; a rejection can leave polling guarded. Parent loop also schedules its next request only after success | `packages/xo-web/src/xo-app/host/{index,tab-stats}.js` |
| FR Stats/Utilisation CPU/Utilisation mémoire/Échanges réseaux/Valeurs cumulées; JA 状態/CPU利用量/メモリ利用量/ネットワーク転送量 with Stacked values and Load average in English. Last day falls back to English in both | patched `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |
| Inherited Settings/Servers wording corrected to FR Paramètres → Serveurs and JA 設定 → サーバ一覧 | same patched catalogs |

The public guide records both requested ranges and nominal refresh/sample
spacing, without promising a complete retained history or instantaneous peaks.
It distinguishes one-host metrics from guest memory limits, pool totals or the
appliance OS. CPU sums, missing-memory zeros, stalled pending state and PIF/byte
formatting are source findings, not installed measurement or a runtime fix.
No universal alert threshold, capacity budget, link-speed conversion, HA margin
or safe migration promise is derived from the graphs.

| Pending scenario | Required observation |
| --- | --- |
| Host identity and scope | Installed host/image/RPM/UI identities, running connection, exact host/pool ID, CPU series/count and memory capacity; no mix-up with appliance/guest/pool scope |
| Ranges/history/freshness | All five labels, requested spacing, actual samples/end time, complete versus short history, browser/host clock alignment; coarse view not treated as a peak capture |
| CPU and sums | Individual percentages, sum option and scale, four 50% series sum to 200%, no normalized-average claim |
| Memory and missing metrics | Total/free/used relation with independent authorized observation; missing free series or NaN/coercion case is not accepted as real zero use |
| PIF traffic | Match legend to host interface/device, actual source units, rx/tx and sum behavior, bond/VLAN inclusion/exclusion and no link-health inference |
| Load/workload | Actual loadavg and known workload, correlated CPU/memory/traffic; no universal threshold or production stress introduced |
| Non-running/outage/fetch error | No stats/loading/stale timestamps, sanitized error, pending/poll behavior; read-only connection checks/reload recover if applicable, no host reboot or collector reset recipe |
| Baseline/diagnosis | Same-host/range/settings comparison, recorded sample age and symptom, independent evidence before a capacity or performance decision |
| EN/FR/JA review | Literal installed labels, technical/language reviewers, sanitized appliance images and assistive acceptance |

Three host statistics/statistiques des hôtes/ホスト統計 ranked queries extend the
browser suite. Routes/page counts remain unchanged: 18 pages per locale and 36
FR/JA drafts. Hosts/pools and the changed manual entry receive meaning hashes
only after comparing the translated meanings. Shared glossary, human review
manifest, strict publication gate, product/release/build/publishing code and
appliance capture backend are unchanged. Final-head website evidence is recorded
on the implementation PR and #189/#198 after verification.

## BK03 scheduled full-NFS/retention extension (2026-10-14)

After #226 merged as `9ed3ffd97967a5bcce719e7ef2d53d81590b1aa8`, the existing
EN/FR/JA backup/restore guide adds section 6, `backup-schedules`, and a manual-home
daily-task link. It extends the existing manual full-NFS/isolated-restore pilot
with a supervised halted-guest schedule, retention 2, disable and retained-point
restore. Source scope stays image `xoa-image-20261009-5f33c81` / ce38 / XO5 above.
No schedule, job, remote, VM or appliance was operated; no backup was pruned.
All installed, capture and human language acceptance remains **Pending**.

The XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` checkout was reconstructed in
this workspace and all 14 released HomeLab patches applied cleanly. No product
build was performed. Schedule/cron/full-writer paths are unmodified by that patch
set; literal labels were checked in its patched catalogs.

| Finding | Pinned source path (XO `e281c536`) |
| --- | --- |
| Default rule is midnight daily with browser-guessed timezone and retention 1; explicit added schedules default enabled. Pilot retains its existing disabled rule, retention 2 and explicit timezone | `packages/xo-web/src/xo-app/backup/new/index.js` |
| Editor state toggle updates local state; Save issues independent schedule requests before job/settings update. Partial failure is not a transaction rollback | same file, `new/schedules.js` |
| Schedule API is global-admin-only. Backend restarts/stops its timer before persisting schedule updates, so a failed write does not establish runtime timer state | `packages/xo-server/src/api/schedule.mjs`, `xo-mixins/scheduling.mjs` |
| Overview state button immediately calls enableSchedule/disableSchedule. Clipboard copies full schedule ID; run/status details are schedule-specific. Active-job cancellation button is deliberately disabled | `packages/xo-web/src/xo-app/backup/overview/tab-jobs.js`, `common/xo/index.js` |
| Visual selector and preview use the selected timezone to generate Date instants; FormattedTime preview has no explicit timeZone, and IntlProvider sets locale only. Browser-display timezone can differ from rule timezone | `packages/xo-web/src/common/{scheduling,timezone-picker,intl/index}.js`, `@xen-orchestra/cron/index.js` |
| Timer stop clears future scheduling, not the separately running backup. Backend callback does not return the backup promise to the cron job; execution is guarded against an already-running job ID | `packages/xo-server/src/xo-mixins/scheduling.mjs`, `jobs/index.mjs`, `@xen-orchestra/cron/index.js` |
| Cron computes next dates from current time; missed-run replay/queue/retry is not established by this pilot. Service outage and daylight-saving handling remain lab scenarios | `@xen-orchestra/cron/index.js`, `packages/xo-server/src/xo-mixins/scheduling.mjs` |
| Full retention lists only mode=full entries with matching scheduleId for the VM on each adapter; getOldEntries(retention-1) selects older points. Same visible name/new schedule ID is not the same policy | `@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs`, `_getOldEntries.mjs` |
| deleteFirst=false transfers/validates XVA, writes metadata, then prunes selected older backups. Later failure can coexist with a new export/metadata; counts/logs and actual isolated restore are independent checks | `@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs` |
| Long-term buckets have distinct timezone/settings semantics and are outside retention-2 pilot; global job timezone is browser-derived separately from schedule timezone | `@xen-orchestra/backups/_getOldEntries.mjs`, `packages/xo-web/src/xo-app/backup/new/index.js` |
| FR uses Sauvegardes/Vue d’ensemble/Planifier/Sauvegarder/Enregistrer, with Backup retention/Timezone and table Cron pattern falling back to English. JA uses バックアップ/オーバービュー/バックアップの作成/バックアップジョブの保存; schedule fields/states remain English | patched `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |
| Delete-first label is EN Delete first, FR Supprimer les anciennes sauvegardes, JA 古いバックアップを最初に削除する. Remote-test actions and FR Emplacement menu wording are corrected to catalog literals | same catalogs; `xo-app/settings/{index,remotes/index}.js` |
| French remoteTestSuccess says Test échoué, and remoteTestFailure says Test réussi. UI success/error branches use those keys with the correct icons and detailed error/step results; headings cannot be used alone for acceptance | `packages/xo-web/src/common/intl/locales/fr.js`, `xo-app/settings/remotes/index.js` |

The French heading defect is tracked in
[xoa-hl #38](https://github.com/Vagrantin/xoa-hl/issues/38). Duplicate searches for
remoteTestSuccess/remote test found no existing component issue. Current xoa-hl
main `a28085219cdfe9d20700e6060377f5059e42e6b5` retains this XO pin; the 14 baseline
patch blobs are identical, and its two additional update-UI patches do not
change these keys. No latest-installed-image or corrected-appliance claim is
made. This docs batch adds the ce38 caveat in all three languages and leaves the
runtime fix/release verification in that component issue; it does not patch XO.

| Pending scenario | Required observation |
| --- | --- |
| Baseline | Successful manual backup/isolated restore, halted disposable source VM, dedicated full-NFS job/remote, capacity and preserved recovery copy outside retention policy |
| Editor/readback | Stable job/schedule IDs, one VM/remote, retention 2, long-term/health-check/delete-first off; disabled state before Save and reopened persisted values |
| Rule and clocks | Explicit timezone, generated visual-selector rule, 3 upcoming instants versus browser/appliance clocks; no preview-as-execution claim |
| Immediate enable | Correct Overview row, successful direct toggle, Enabled readback and first automatic trigger without manual run |
| Repeated automatic export | At least 3 successful same-schedule runs with job/schedule IDs, actual times, per-VM/export logs and remote restore points |
| Retention pruning | Two newest eligible full points after successful cleanup; per-VM/schedule/remote identity, other schedule points not inferred or bulk-deleted |
| Partial failure | Error plus persisted schedule/job/settings and possible runtime activity; new/partial exports and leftover inventory before retry; no rollback assumption |
| Disable | Disabled readback before next tick, in-flight run finishes separately, next expected occurrence creates no run; no cancellation claim from state toggle |
| Retained-point recovery | Scheduled-run point restored stopped, every inherited NIC removed before boot, matching checksum, identified copy cleanup and source preservation |
| Outage/overlap/DST/reporting | Separate authorized fixtures for missed runs, already-running refusal, clock changes and configured alerts; no guaranteed queue/catch-up or email claim |
| EN/FR/JA labels | Exact installed labels, French reversed headline versus icons/details, named technical/language review and sanitized appliance evidence |

Six ranked schedule/retention queries and twelve 390/320px localized home-link
fragment checks with/without JavaScript extend the browser suite. The manual
stays at 18 pages per locale / 36 FR/JA drafts. Backup and home meaning hashes are
updated only after comparing translations. Shared glossary, review manifest,
strict publication gate, product/build/release/publishing code and Jenkins
appliance-capture backend are unchanged. Final-head website CI/artifact evidence
is recorded in the PR and #189/#197/#198 after verification.

The first full browser run found a Japanese ranking regression: the expanded
backup chapter's character suggestions displaced `vm-transfer` for the existing
マイグレーション query. The Japanese transfer title now explicitly includes
that task term alongside 移行. Its route and meaning hash stay unchanged because
the guide body/glossary are unchanged. All existing query assertions remain;
the search implementation is unchanged. Final evidence uses the corrected head.

## BK07 full-NFS failure diagnosis (2026-10-14)

After #227 merged as `a35177fb779c32bb6eca7b621ae2631f67b11847`, the existing
EN/FR/JA troubleshooting chapter adds `backup-failures`. The manual entry and
full-NFS tutorial link directly to it. This is a source-reviewed diagnostic
procedure for the same one-VM lab job, not a reproduced outage or a general
production recovery recipe. No backup, remote, schedule, VM, service or storage
was operated; no failure was injected and no backup was pruned.

Source remains image `xoa-image-20261009-5f33c81`, ce38 / XO 5.113.2 at full
commit `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, with HomeLab source
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19`. All 14 released patch files were
inspected for affected paths: none modify the reviewed backup/log implementation
files. Their applicable catalog hunks were applied in build order to the English,
French and Japanese catalogs for the literal-label review. This is a source
check, not evidence of an installed payload or UI.

| Finding | Pinned source relative to XO `e281c536` |
| --- | --- |
| Overview includes backup Logs; shortened job ID, status opens details | `packages/xo-web/src/xo-app/backup/overview/index.js`, `packages/xo-web/src/xo-app/logs/backup-ng/index.js` |
| Detail search/status filters, default pending/failure/interrupted filter, five tasks per page; unmapped raw tasks and some successful zero-size transfers are not rendered | `packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js` |
| Clipboard/download serialize the full consolidated JSON without a redaction pass; restart/force execute backup RPCs | `packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js` |
| Start is pending only while current running-job ID matches; unmatched completion yields interrupted; selected error messages map to skipped; child failure/skips affect aggregate status | `packages/xo-server/src/xo-mixins/backups-ng-logs.mjs` |
| Overlap produces an already-running error; start/end records preserve run/job/schedule identity | `packages/xo-server/src/xo-mixins/jobs/index.mjs` |
| Delete-first=false writes export and metadata before older-point deletion; later failure does not imply absence of the new point | `@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs` |
| Restore list loads enabled remotes; a per-remote exception shows a loading notification; restore logs are a separate table on that page | `packages/xo-web/src/xo-app/backup/restore/index.js`, `packages/xo-web/src/xo-app/logs/restore.js` |
| Overview cancellation is explicitly disabled | `packages/xo-web/src/xo-app/backup/overview/tab-jobs.js` |
| Started is Démarré / スタートしました; other job statuses, Logs and Download log fall back to English after compacting undefined locale entries | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}`; `xoa-hl/scripts/compact-xo-locales.py` at `5f33c81` and released patch set |

The chapter separates log state, failed stage and surviving data. It requires
all task pages/statuses plus preserved JSON, full IDs rather than names, and an
inventory before an ordinary non-overlapping lab retry. Disabling future
triggers is not active-run cancellation. Any remedy affecting a live target or
uncertain partial-object ownership needs its owner's decision; no chain repair,
snapshot/file deletion, forced rerun or service-restart recipe is introduced.

| Pending lab scenario | Required observation |
| --- | --- |
| Run evidence | Installed release identities; exact run/job/schedule/VM/remote IDs, timestamps/timezone and private JSON; sanitized report excerpt |
| Detail visibility | Installed filters/default, all five-entry pages and status choices; omitted visible tasks compared with preserved JSON |
| Pending versus finished | Active run, progress/end readback and no duplicate run; warnings and isolated restore checked independently of success |
| Skipped/failure/interruption | Separately authorized disposable fixtures for each status; reason and raw task context; no status-as-rollback assumption |
| Access/capacity failure | Dedicated NFS lab outage or capacity fixture, exact error/failed stage, storage-owner remedy and preserved earlier recovery copy; not a production volume filled/disconnected |
| Post-transfer cleanup failure | Controlled fixture proves whether new metadata/point survives, older-point inventory and no blind rerun/file deletion |
| Unreadable remote | Enabled state, actual loading notification, inventory after restored readability; empty UI does not establish deletion |
| Failed restore | Separate restore log, destination capacity/access and positively identified partial VM/VDIs before any approved cleanup |
| Retry and recovery | No active run, read-back settings/delete-first off, ordinary one-VM rerun, retained-point inventory and stopped/all-NICs-removed guest checksum restore |
| Final state and languages | Disabled lab schedule; original error/remedy/new IDs/result; installed EN/FR/JA labels and named human review |

Three new ranked failure-diagnosis queries and twelve 390/320px localized
home-link fragment checks with/without JavaScript extend the existing browser
suite. Every pre-existing query stays in place. Meaning hashes are refreshed
after comparing all three affected page bodies (troubleshooting, home and
backup-restore). The manual stays at 18 pages per locale and 36 FR/JA drafts;
human review records and the reviewed-publication gate are unchanged. Website
checks and final-head CI are recorded on the PR separately from these Pending
appliance scenarios. Multi-mode runbooks, production recovery, alerts and human
language acceptance remain gaps. Product/build/release/publishing code and the
Jenkins appliance-capture backend are unchanged.

The first-head CI passed all 71 ranked queries, browser/keyboard/reflow checks
and 51 Lighthouse reports at 100/100. Its verified browser artifact exposed a
French mobile stage-table overflow caused by slash-separated labels. Labels are
now ordinary words, and the Restore route is placed before the table so it does
not impose a narrow-cell minimum width. A new assertion requires both diagnosis
tables to fit their containers in EN/FR/JA at 390/320px. Final-head evidence must
be rechecked after this correction; the first-head screenshots are not final QA.

The first width assertion incorrectly searched only descendants although Hugo
renders a table as a direct sibling. It now selects the two explicit table
classes and compares their actual scroll/client widths. A scoped fixed table
layout with wrapping cells keeps these two checklists within the reading column;
other site tables keep their existing layout. Final-head CI must pass the
corrected assertion and the unchanged broader website suite.

## VM09 stopped snapshot/revert/cleanup pilot (2026-10-14)

This independent continuation starts at #227 merge
`a35177fb779c32bb6eca7b621ae2631f67b11847`. PR #230 remains a separate open
backup-failure batch; no merge/deployment of that PR is assumed. Existing EN/FR/JA
VM-operation sections now require a guest-file checksum, stopped/no-VIF baseline,
ordinary-disk coverage, UUID identification, persisted rename, pre-revert point
inventory and one-snapshot cleanup. The manual links directly to
`stopped-snapshot`; `snapshot-revert` and `snapshot-cleanup` are stable shared
anchors. The previous localized section 3/4 anchors remain inside the headings.

Source scope stays image `xoa-image-20261009-5f33c81`, package
`v5.113.2_e281c536-ce38`, XO 5.113.2 at
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, HomeLab source
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19`. All 14 released patch paths were
reviewed: snapshot tab/API/XAPI implementations and snapshot client handlers
are unchanged. Catalog hunks were applied in build order to a clean copy of
the pinned English/French/Japanese sources; compaction makes undefined keys
fall back to English. This is source review, not an installed appliance check.

| Finding | Source relative to the pinned XO commit |
| --- | --- |
| Per-VM New snapshot acts directly, default name includes ISO timestamp; memory button uses a separate confirmation/checkpoint path | `packages/xo-web/src/xo-app/vm/tab-snapshots.js`, `packages/xo-web/src/common/xo/index.js`, `packages/xo-server/src/api/vm.mjs` |
| Row date/name/description edits, UUID-copy action and single/grouped delete are distinct controls | `packages/xo-web/src/xo-app/vm/tab-snapshots.js` |
| Snapshot requires VM operate and normally SR operate; pilot uses administrator instead of claiming delegated/resource-set acceptance | `packages/xo-server/src/api/vm.mjs` |
| API passes ignoredVdisTag=[NOSNAP]; wrapper matches substring in VDI name_label, with host-API fallback handling | `packages/xo-server/src/api/vm.mjs`, `@xen-orchestra/xapi/vm.mjs` |
| Snapshot-before=true by default; client awaits separate ordinary snapshot then requests revert; failure is not atomic undo | `packages/xo-web/src/common/xo/revert-snapshot-modal/index.js`, `packages/xo-web/src/common/xo/index.js` |
| Revert requires snapshot view plus source VM operate; resource-set/IP bookkeeping is separate from XAPI revert | `packages/xo-server/src/api/vm.mjs` |
| Running-state snapshot can invoke asynchronous start/resume with errors ignored; revert success is not guest-boot acceptance | `packages/xo-server/src/xapi/mixins/vm.mjs` |
| Snapshot removal invokes vm.delete; VDI cleanup errors are logged, shared attachments can skip disk deletion | `packages/xo-web/src/common/xo/index.js`, `packages/xo-server/src/api/vm.mjs`, `@xen-orchestra/xapi/vm.mjs` |
| FR literals are Instantanés, Nouvel instantané, Restaurer la MV à cet instantané, Faire un instantané avant, Supprimer cet instantané | patched `packages/xo-web/src/common/intl/locales/fr.js` |
| JA tab is スナップショット; snapshot actions largely retain English; snapshotDescription incorrectly says Name like snapshotName | patched `packages/xo-web/src/common/intl/locales/ja.js` |

The Japanese duplicate Name heading is described in the preview, not changed in
the component runtime. Exact installed labels and UI translation corrections
remain #131 work. The document excludes live/memory snapshots, shared/excluded
or passthrough disks, backup-managed point cleanup and SR-loss recovery.

| Pending lab scenario | Required observation |
| --- | --- |
| Baseline/isolation | Installed image/RPM identities, disposable source UUID, ordinary VDI inventory, no [NOSNAP] names, paused triggers/no active tasks, no VIFs and independent recovery copy where needed |
| Creation/readback | Halted state, one direct snapshot, new UUID/date/default name, expected disk coverage/SRs/sizes, rename/description persisted, capacity and errors |
| Modified state | Console-only snapshot-B checksum differs, clean shutdown and recorded current inventory |
| Pre-revert preservation | Correct snapshot-A UUID, preservation checked, distinct pre-revert point UUID and capacity; later controlled recovery of B separately validated |
| Revert/result | Halted/no-VIF readback before boot, configuration/disk inventory, console boot with matching A checksum and guest/application checks |
| Partial failure | Separately authorized fixtures for pre-snapshot versus later revert failure, surviving objects and actual state before retry; no rollback assumption |
| Cleanup | Exact owned test UUID only, single-row confirmation, retained points/source remain, disk/error/capacity readback; no immediate-reclamation promise |
| Languages | Installed EN/FR/JA action labels, Japanese duplicate header and named human technical/language review |

The existing EN/FR/JA ranked snapshot queries remain; 36 locale/width/JS fragment
checks extend website CI. screenshots capture all three pilot headings at 390/320px, and six
old heading-anchor assertions preserve existing bookmarks. Mobile geometry also
checks that all anchor spans align with the actual heading top, including the
legacy aliases; these aliases use Hextra’s absolute-position class. Existing broader
search/reflow/Lighthouse assertions remain. Meaning hashes are refreshed after
all three bodies are updated; 18 pages per locale and 36 FR/JA drafts remain.
Final-head CI and artifact evidence belong on the implementation PR. No
appliance/VM/snapshot/VDI/job was operated, no data was reverted or deleted, and
no functional/human acceptance is claimed. #189/#198/#201/#202 stay open.

## VM01 console use and diagnosis (2026-10-15 JST)

Continuation starts at #231 merge `5e40dc84bdae782dbb6402b0eb7212ea960d6ab5`,
after #230/#231 were both merged into `claude/gracious-ride-99qg08`. The existing
EN/FR/JA VM-operation chapter now includes `vm-console`, linked from the manual,
first-VM tutorial and troubleshooting chapter. It covers the running-VM gate,
operate permission, expected display, harmless editor input, pointer capture and
release, desktop scale/header controls, clipboard direction, separate SSH/RDP
handlers and symptom-based checks. No guest/host/appliance or console session
was operated; these are source-reviewed instructions with lab checks pending.

Applicability remains image `xoa-image-20261009-5f33c81`, package
`v5.113.2_e281c536-ce38`, XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`,
HomeLab source `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`. All 14 released patch
paths/hunks were reviewed; none change the console tab, noVNC wrapper, server
console-upgrade handler or console proxy. Their EN/FR/JA catalog hunks were
applied in build order. The locale-compaction script at the HomeLab pin records
English fallback for missing/undefined entries. No current installed payload,
guest OS/clipboard support, browser/mobile compatibility or human approval is
inferred from those source observations.

| Finding | Source relative to the XO pin |
| --- | --- |
| Only power_state=Running mounts console; other states have a hardcoded English message; disable_pv_vnc=1 replaces the canvas | `packages/xo-web/src/xo-app/vm/tab-console.js`, `packages/xo-web/src/common/xo/index.js` |
| Mouse enter grabs keyboard/mouse and blurs active element; exit releases capture and re-enables XO shortcuts | `packages/xo-web/src/common/react-novnc.js` |
| Clipboard field sends debounced edits; Copy writes local clipboard; multiline confirmation feeds the same remote setter | `packages/xo-web/src/xo-app/vm/tab-console.js`, `packages/xo-web/src/common/react-novnc.js` |
| SSH/RDP use reported main IP and local URI handlers; their presence does not establish guest services or client software | `packages/xo-web/src/xo-app/vm/tab-console.js` |
| Ctrl+Alt+Del confirms then sends keys; ISO selector is a separate media control; scale adjusts client display/mouse, header toggle is not full-screen | same tab and `packages/xo-web/src/common/react-novnc.js` |
| Browser console upgrades at /api/consoles/id, authenticates cookie token and requires VM operate permission; open/close audit events | `packages/xo-server/src/index.mjs` |
| Browser HTTP(S) becomes WS(S); disconnect retries use backoff; server source notes missing VM-restart disconnection detection | `packages/xo-web/src/common/react-novnc.js`, `packages/xo-server/src/index.mjs` |
| Appliance proxies host console using XAPI session; it has modern WebSocket and legacy CONNECT paths and uses the configured host proxy agent where supplied | `packages/xo-server/src/proxy-console.mjs`, `packages/xo-server/src/index.mjs` |
| Host console transport uses rejectUnauthorized=false; ordinary host-connection trust and browser-appliance TLS are separate concerns, not an end-to-end verified-TLS claim | `packages/xo-server/src/proxy-console.mjs` |
| FR Console/Copier/Ctrl+Alt+Supp/header labels; JA コンソール/コピー/clipboard labels, English header tooltips; JA disabledConsole is misleading imperative wording | patched `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

The Japanese disabled-console wording is explained as an informational state,
not a control. Component terminology/installed-label review remains #131 work.
The guide does not provide a disable_pv_vnc policy override, public VNC exposure,
certificate-verification bypass, SSH/RDP setup or guest-specific reinstall/
force-reboot recipe. Rendering a canvas is not guest health, accepted input or
clipboard support; repeated reconnects are not a successful session.

| Pending lab scenario | Required observation |
| --- | --- |
| Identity and route | Installed image/RPM, disposable VM UUID/resident host, retained VIF isolation, browser-appliance and appliance-host paths |
| Running gate and permissions | Halted/paused/suspended versus Running display; admin/operate allowed and Viewer denied without increasing privileges as a workaround |
| Display/input | Expected guest screen, harmless editor input, pointer release and working XO controls; guest credentials distinct from host/appliance |
| Scale/header | Desktop scale and pointer alignment, header readback, smaller-screen availability without promising every browser/device |
| Clipboard | Harmless text in both directions, actual guest paste where supported, unsupported case and no private clipboard/screens in reports |
| Client shortcuts | Reported-IP versus absent-IP buttons, local handler availability and independent guest SSH/RDP/service/network acceptance |
| Restart/disconnection | Separately authorized test restart, stale/blank view, reopen/fresh display and backend/browser evidence; no forced restart as generic diagnosis |
| Disabled display | Approved disabled-state fixture and exact informational EN/FR/JA messages, without altering an existing policy |
| Connection failure | Separately authorized proxy/auth/access fixture, exact status/error, owner-selected remedy and verified restored connection |
| Language and accessibility | Installed labels, named technical/language review, browser/keyboard/mobile console interaction; website checks do not establish appliance UI accessibility |

Three new ranked console queries and twelve localized 390/320px fragment checks
with/without JavaScript extend website CI. Existing queries and both preceding
backup/snapshot suites remain. Meaning hashes are refreshed after updating all
four corresponding page bodies in all locales. Coverage remains 18 pages per
locale / 36 FR/JA drafts, with human review records unchanged. Final-head website
CI/artifact evidence is recorded on the PR separately from Pending lab checks.


## VM06 stopped-template conversion and reuse (2026-10-15)

After #232 merged as `df0537681c5c3e33071e666c628aba8b223b56db`, a separate
EN/FR/JA `templates` guide extends the VM06 gap. It converts only an identified,
stopped full working copy, preserving the original. It creates two separate
console-only test VMs with fast clone and automatic startup off, explicitly
removes wizard-proposed NICs, verifies VM/VDI/SR identity before boot, and compares
a harmless sample across the two deployments. Template lifecycle/retirement,
OS-specific generalization, guest tools, licensing, cloud-init, cross-pool and
fast-clone storage acceptance remain gaps. No appliance/VM/template/disk/job was
operated, no template was converted and no data was deleted during this work.

### Source review and limits

Baseline remains image `xoa-image-20261009-5f33c81`, package
`v5.113.2_e281c536-ce38`, HomeLab source
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19` and XO
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. The 14 released HomeLab patch files
were checked for conversion/wizard changes and the literal keys used here; no
patch changes these conversion, fast-clone, boot or template-type labels. This
is source review, not installed or latest-release availability acceptance.

| Finding | Pinned XO path at `e281c536` |
| --- | --- |
| Advanced conversion button disabled except Halted; automatic power-on toggle | `packages/xo-web/src/xo-app/vm/tab-advanced.js` |
| Confirmation is hard-coded English and calls vm.convertToTemplate | `packages/xo-web/src/common/xo/index.js` |
| VM administrate plus pool administrate; removable-media ejections precede set_is_a_template(true), with selected eject errors ignored; conversion is the same object | `packages/xo-server/src/api/vm.mjs` |
| Home query t=VM-template; expanded row exposes full ID, name/description are editable and description is hidden at narrower widths | `packages/xo-web/src/xo-app/home/{index,template-item}.js` |
| bootAfterCreate=true and fastClone=true defaults; template query persisted on selection; existing disks copied into form; no-template-VIF fallback proposes pool network defaults | `packages/xo-web/src/xo-app/new-vm/index.js` |
| Empty VIF list passes interface validation; form submits VIFs and copy/boot settings; fast-clone checkbox is in Summary | `packages/xo-web/src/xo-app/new-vm/index.js` |
| Creation calls xapi.createVm with destroyAllVifs=true, registers failure cleanup and optionally starts guest | `packages/xo-server/src/api/vm.mjs` |
| createVm chooses _cloneVm or _copyVm, provisions/edits disks, destroys template VIFs then creates submitted VIFs; cleanup is registered but not a proven failure-recovery result | `packages/xo-server/src/xapi/mixins/vm.mjs` |
| Convert to template and No config drive remain English in FR/JA; boot-after-create is French-translated, Japanese English; template type is Template / Template / テンプレート | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}`; locale-compaction fallback in `xoa-hl/scripts/compact-xo-locales.py` at `5f33c81` |

The page cites immutable source blobs. Its prerequisites require a known lab
guest, recorded OS/version/sample, excluded unattended jobs, original preservation
and capacity. This deliberately does not prescribe Sysprep, cloud-init reset,
machine identity cleanup, key rotation or a guest-tools installation recipe.
A new VM UUID or absent NIC does not establish guest generalization. The source's
attempted creation cleanup does not establish that interrupted/failed creation
leaves no VM or VDI; the procedure preserves object/task inventories first.

### Pending installed acceptance

Every scenario below is **Pending**, with installed host/image/application
identities and named technical/language reviewers still required.

| Scenario | Required observation |
| --- | --- |
| Working-copy preparation | Distinct halted full copy, known ordinary VDI/SR set and sample checksum, no VIFs, ejected ISO, no unattended startup/jobs, original/required backups preserved |
| Conversion authorization | VM and pool permission behavior, halted-only control and actual EN/FR/JA button/confirmation labels |
| Conversion result/failure | Same UUID becomes template, original survives, persisted name/description, eject/task/type readback after partial error; no untested reversal assumption |
| Template selection | Home Template view/full ID and wizard template= query agree; correct pool/guest/disk set |
| Wizard settings | Explicit No config drive, fast clone off, boot-after-create/automatic power-on off; proposed VIF rows removed, zero-interface summary and sufficient SR/host capacity |
| First deployment | Separate Halted VM and VDIs with expected sizes/SRs, no NICs before first boot, console login/disk/sample check and controlled harmless sample change |
| Repeatability | Second creation from same template rechecks all settings, produces separate VM/VDI IDs and no NICs, retains initial sample independently of test-1 |
| Failure inventory/cleanup | Exact task/error plus known template/new VM/VDI state before any authorized retry/removal; only identified test VMs removed, source/template/required backups preserved |
| Wider preparation/lifecycle | Separate accepted guest-specific identity/tools/licensing, network connection, template update/retirement, fast-clone and cross-pool scenarios |

### Website validation

The manual checker requires `templates.md`; locale parity, freshness/status and
review gating cover 19 pages per locale / 38 FR/JA drafts. The existing failed-gate
regression now expects all 38 draft problems and queue records. New task searches
are templates / modèle de VM / テンプレート; every previous query is retained.
The new guide participates in desktop/mobile screenshots, 720/320px reflow,
no-JS task navigation and mobile Lighthouse (54 entry/task reports). The new
beginner-to-deployment fragment is exercised at 390/320px in every locale with
and without JavaScript. Root/subpath and final-head CI/artifact evidence are
recorded on the implementation PR after verification. No named human review,
appliance capture/backend, product/build/release or deployment workflow is changed.

The first browser head exposed a singular/plural search mismatch for the new
English query `templates`. The English title now names `VM templates` explicitly.
The query, expected task target and all prior assertions are retained; no search
engine or body-meaning revision is changed by this editorial title correction.
Final evidence must use the corrected head.

## VM05 Ubuntu guest management-agent pilot (2026-10-15)

After #234 merged as `97dba869e8185e44f457f550b838f6292780de6e`, the next
VM05 batch adds EN/FR/JA `guest-tools` instructions. Scope is a freshly installed,
disposable Ubuntu 24.04 LTS Noble amd64 guest and Ubuntu package
`xe-guest-utilities` `7.20.2-0ubuntu1`. It records an existing installation instead
of blindly reinstalling/upgrading, checks candidate origin and the simulated
transaction, installs interactively, enables the actual packaged unit and checks
fresh XO reporting plus a normal stop/boot. No guest/appliance/host was operated,
no package was installed or service started, and no shutdown test was executed.
All functional and human-review results below remain **Pending**.

### Reviewed sources and boundaries

The appliance baseline remains image `xoa-image-20261009-5f33c81`, package
`v5.113.2_e281c536-ce38`, `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19`
and XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. The released HomeLab patches
were scanned for the guest-agent/detection fields and labels used here; none
changes these paths. Source presence is not installed HomeLab compatibility.

| Finding | Source |
| --- | --- |
| General hides the detection message unless Running and pvDriversDetected is defined; then checks missing PV drivers, missing agent, up-to-date flag in that order | XO `packages/xo-web/src/xo-app/vm/tab-general.js@e281c536` |
| Mapping requires running VM metrics and guest metrics; major+minor version or feature-static-ip-setting supplies agent detection; formatted version and up-to-date flag come from host guest metrics | XO `packages/xo-server/src/xapi-object-to-xo.mjs@e281c536` |
| Advanced displays agent version, guest OS name and kernel; OS data derives from guest metrics | XO `packages/xo-web/src/xo-app/vm/tab-advanced.js@e281c536`, mapping above |
| Ordinary stop/restart can retry with force or bypass after extra confirmations; stop/start need VM operate permission | XO `packages/xo-web/src/common/xo/index.js`, `packages/xo-server/src/api/vm.mjs@e281c536` |
| French agent messages/version field fall back to English; General/Advanced/Guest OS are Général/Avancé/OS invité; inherited Start is Créer | XO `packages/xo-web/src/common/intl/{messages.js,locales/fr.js}@e281c536`; HomeLab locale compaction at `5f33c81` |
| Japanese General/Advanced and start/stop are localized; agent detection messages are Japanese, Guest OS/version fields remain English | Same catalogs, `locales/ja.js@e281c536` |
| Ubuntu Noble lists xe-guest-utilities 7.20.2-0ubuntu1 in universe and the amd64 package provides xe-daemon.service, proc-xen.mount and guest agent binaries | [Ubuntu package](https://packages.ubuntu.com/noble/xe-guest-utilities), [file list](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist), retrieved 2026-10-15 |
| xe-daemon.service requires proc-xen.mount, checks Xen virtualization and /proc/xen/capabilities; ExecStartPre runs xe-linux-distribution, ExecStart runs xe-daemon; multi-user.target enables it | Versioned packaging archive below, `debian/xe-guest-utilities.xe-daemon.service` |
| proc-xen.mount mounts xenfs at /proc/xen, has Xen virtualization condition and local-fs.target install target | Same archive, `debian/proc-xen.mount` |

Downloaded source archives were inspected without executing their contents:

| Ubuntu source artifact | SHA-256 |
| --- | --- |
| [xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) | `f1ee050cfddcf98c51c7ddb5f1583c4f452b0956ecb7ef086df7704d1bf92997` |
| [xe-guest-utilities_7.20.2.orig.tar.gz](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2.orig.tar.gz) | `7cf5a34ab1b94a77eeacc330984cc681ca285aae1c06a080e079f526fd876953` |

Upstream source `guestmetric/guestmetric_linux.go` reports PVAddons version
fields from build substitutions; XO formats host guest-metrics fields. The guide
preserves the package version and reported version separately instead of claiming
they must match. Generic upstream guest-tools guidance is background only; its
usual xe-linux-distribution service name is not applied to Noble's package.

### Pending installed acceptance

| Scenario | Required observation |
| --- | --- |
| Identity and access | Installed host/image/RPM, VM UUID/resident host, actual Ubuntu 24.04 amd64/kernel/Xen, guest sudo versus VM operate, retained console and approved lab repository connectivity |
| Existing-install branch | Package absent versus present; preserve existing origin/version and avoid unreviewed upgrades or vendor mixing |
| Package transaction | Successful approved index refresh, Noble universe candidate 7.20.2-0ubuntu1, simulated transaction reviewed, interactive install result, no signature bypass or unrelated repository |
| Service startup | Actual package/file inventory, proc-xen.mount and Xen conditions, xe-daemon.service enabled and active, useful timestamped logs |
| UI states | Running gate, no metrics/undefined detection versus missing PV drivers versus missing/outdated/detected agent, correct EN/FR/JA literals |
| Report readback | Refreshed same-VM General/Advanced, recorded agent/package versions separately, OS/kernel compared to console, IP compared independently with IPv4 absence allowed |
| Clean power operation | Saved work, ordinary Stop confirmation, actual clean guest shutdown and Halted, no active task; cancel any force/bypass and record guest-normal fallback separately |
| Boot persistence | Same VM boots, console login/test-file/application checks, service enabled/active and fresh reports after boot |
| Failure and recovery | Package/unit/host/report mismatch and stop refusal evidence, owner-selected correction and repeated verification; separately established backup/restore plan rather than an untested uninstall/downgrade promise |
| Wider scope | Other distros, tools ISO, Windows/BSD, kernel/driver acceptance, migration/DMC/hotplug/quiescing/performance, upgrades/removal and supported guest matrix each need separate review |

### Website validation scope

Link the chapter from the manual, beginner, VM power and template guides; stable
anchors are `guest-tools-status` and `install-linux-agent`. Extend required-page
and human-review-gate coverage to 20 manual pages per locale / 40 FR/JA drafts,
without changing human review records. Retain all 77 preceding task queries and
add guest tools / outils invités / ゲストツール. Include the page in desktop/mobile,
no-JS navigation, 720/320px reflow and Lighthouse (57 reports). Exercise beginner
installation and VM-operation status fragments at 390/320px in all locales with
and without JavaScript. Record actual build/CI/artifact/visual results on the PR.
Appliance captures and their Jenkins infrastructure remain outside this change.

## SN02 NFS VM-disk storage pilot (2026-10-15)

Continued after merged #235 (`cd37bd4f4c147d553bd01c6525b7dddef6a7e3f4`).
Extend the existing EN/FR/JA storage-networks chapter with `nfs-vm-storage`:
an empty dedicated export, administrator browser creation of NFS in **VDI SR**,
probe/readback and disposable-disk verification. ISO libraries and backup remotes
retain their distinct purposes. The appliance/source baseline remains image
`xoa-image-20261009-5f33c81`, application `v5.113.2_e281c536-ce38`,
`xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19` and XO5
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. No storage, VM, guest, host or
appliance was operated; no installed availability or persistence is claimed.

### Pinned-source findings

All XO paths below are relative to `vatesfr/xen-orchestra` at the full XO5 pin
above. The ce38 HomeLab `patches/` were scanned for these wizard/API/PBD paths
and labels; no patch changes the documented NFS flow. This is source review,
not a payload audit or installed release test.

| Finding | Inspected source |
| --- | --- |
| Admin-only wizard; hardcoded VDI SR/NFS versus ISO SR/NFS ISO groups; host selection, server, default/4/4.1 versions, options, export search and selected-path probe | `packages/xo-web/src/xo-app/new/sr/index.js` |
| Version change only changes state; server discovery and path selection must be repeated; path probe records existing SR UUIDs with used/unused and reattach controls | Same wizard, `_handleNfsVersion`, `_handleSearchServer`, `_handleSrPathSelection`, `getUsedSrs`, Storage usage render |
| NFS is exempt from the existing-SR strong confirmation; do not infer an empty export from lack of confirmation | Same wizard, `_handleSubmit`; this pilot stops on any existing-SR result and excludes reattach/subdirectory modes |
| Browser sends host/name/description/server/serverPath, optional version/options and optional reattach UUID | `packages/xo-web/src/common/xo/index.js`, `createSrNfs` |
| New SR uses `SR_create`, type nfs and shared true; server/serverpath plus optional nfsversion/options; reattach is separate; create/probe resolve host administrate | `packages/xo-server/src/api/sr.mjs`, `createNfs`, `probeNfs`, `probeNfsExists` |
| General shows type/size/physical usage/free; Hosts shows per-PBD device_config and attached status with connect/disconnect handlers | `packages/xo-web/src/xo-app/sr/{tab-general,tab-host}.js`; a Connected status is also a button, so read without toggling |
| English literals and FR/JA translations/fallbacks; type-group names are hardcoded, FR NFS labels absent, JA NFS labels undefined | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}`; use fallback literals, not invented localization |

### Pending installed acceptance

| Scenario | Required observation — all Pending |
| --- | --- |
| Release and lab identities | Host/pool, image/RPM, actual UI language, intended host scope, independent console and stopped disposable VM |
| Storage preparation | Owner-approved empty dedicated export, agreed server/root/version/options, per-host read/write access, NAS free space/quotas and reserve |
| Existing storage branch | Baseline SR inventory; in-use and unattached existing UUID cases stop without create/reattach; no warning absence used as an emptiness test |
| Successful create | One request, exact resulting UUID/pool/type nfs, server/path, version/options when supplied, General capacity and every intended PBD/host attached |
| Partial failure | Timestamp/error/task, before/after SR/host/PBD inventory, owner-directed reconciliation before retry, no blind duplicate create |
| Disk and guest | New small test VDI on exact SR, VM/VBD identities, capacity, guest device identification; separately prepared test filesystem/sample checksum and ordinary shutdown/boot persistence |
| Host scope | Each intended host needs independent guest read/write acceptance via separately approved placement/migration; shared true does not prove this |
| Recovery and cleanup | Preserve data/error evidence; exact disposable disk only, retain SR/export until all consumers/recovery requirements accounted for; no destructive SR/NAS cleanup prescribed |
| Wider scope | Local/SMB/iSCSI, reattach/subdirectories, defaults, destructive lifecycle, outage, performance, migration/HA require separate source review and tests |

### Website validation scope

Add manual and beginner links to the stable fragment in all three locales.
Refresh body hashes only for those three page families; all 40 FR/JA translations
remain drafts and no human approvals are added. Retain the prior 80 ranked queries
and add NFS storage / stockage NFS / NFSストレージ. Existing desktop/mobile,
no-JS reading, keyboard, 720/320px reflow, 200% text and 57 Lighthouse reports
already include storage-networks. Add 24 fragment navigations (two entry points,
three languages, two widths, JS on/off) with 12 viewport screenshots.
Record actual root/subpath, CI and artifact/visual results on the implementation
PR. Browser tests validate the documentation interface; installed NFS behavior
and human language acceptance remain Pending. No capture pipeline or publication
workflow is changed.

The first CI head passed EN/FR NFS queries but failed `NFSストレージ`: the
page title spells `NFS ストレージ`, so literal-title ranking missed the page and
suggested character matches won. Phrase ranking now ignores optional whitespace
beside Han/Hiragana/Katakana characters, after the existing NFKC/case
normalization. Latin word spaces, tokenization and displayed titles are retained.
Keep the failing query and also test `NFS ストレージ` (84 total ranked queries).
Final evidence must use the corrected head; the failed run is not acceptance.

The first-VM path provisions and reads back the SR without an existing guest.
Only then does it return to create-vm; disposable-disk verification follows guest
installation. This ordering avoids making an existing test VM a prerequisite
for a beginner who is creating their first writable SR and first VM.

## SN04 tagged guest VLAN pilot (2026-10-15)

Continued after merged #236 (`c336b135e7fddeea056eb7028fbf1cd8ee4086d0`).
The existing EN/FR/JA storage chapter adds `host-vlan-network`: administrator
creation of one tagged guest network on a dedicated spare physical uplink in a
disposable pool. This is a host/pool operation initiated in the appliance browser,
not guest VIF creation. All release/image/package identities remain those above.
No host, switch, guest, network or appliance was configured or operated.

Sources below are at XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`.
The released xoa-hl patch set at `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`
was searched for changes to this wizard, pool/host networking and its label IDs;
no relevant override was found. This is source review, not installed UI evidence.

| Source finding | Pinned path |
| --- | --- |
| Pool selection; ordinary/bonded/SDN branches; master PIFs only, VLAN=-1 and not bond slave; management PIFs remain selectable | `packages/xo-web/src/xo-app/new/network/index.js` |
| Interface optional for ordinary network; absent PIF forwarded as undefined; blank VLAN/MTU forwarded as undefined; explicit NBD false available | `packages/xo-web/src/xo-app/new/network/index.js` |
| network.create requires pool administrate, defaults MTU=1500/VLAN=0; no switch/guest-IP configuration; NBD purpose is a later API step | `packages/xo-server/src/api/network.mjs` |
| Creates network with automatic=false, then pool.create_VLAN_from_PIF when a PIF is supplied; failure defer attempts network.destroy; no guaranteed rollback of all host/VLAN state | `packages/xo-server/src/xapi/index.mjs` |
| Pool PIF/VLAN summary selects master PIF; copy UUID, expandable PIFs and editable VLAN/MTU controls | `packages/xo-web/src/xo-app/pool/tab-network.js` |
| Expanded pool PIF status uses carrier, with separate actionable plug/unplug controls; it is not currently_attached | `packages/xo-web/src/common/sorted-table/pifs-column.js` |
| Host rows show VLAN/MTU, management badge, address/current IP mode, MAC and attached-state button with separate physical carrier icon; UUID copy action | `packages/xo-web/src/xo-app/host/tab-network.js` |
| PIF attached, carrier, management, physical, bond, IP modes, VLAN/MTU and network links map from distinct XAPI fields | `packages/xo-server/src/xapi-object-to-xo.mjs` |
| Existing-network MTU update invokes VIF/PIF unplug/replug; destructive network cleanup removes VLAN/bond/tunnel objects before network.destroy | `@xen-orchestra/xapi/network.mjs`, `packages/xo-server/src/xapi/index.mjs` |
| FR Nouveau/Network then Réseaux tab, Interface/Nom/Description/VLAN/MTU/Créer un réseau/Connecté; missing FR network-menu/type/NBD labels fall back to English; JA 新規作成/Network then ネットワーク tab, wizard/state fields remain English | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}`, `packages/xo-web/src/xo-app/{menu,host,pool}/index.js` |

Procedure decisions: require independent console and network-owner topology;
unused nonbonded physical uplinks on all intended hosts, no host IP or
management/storage consumers; explicit approved tagged VLAN and MTU 1500;
NBD off. Interface or VLAN must not be left blank. Read every host separately;
carrier and attachment are separate observations, neither proves tagged traffic.
A guest uses an ordinary untagged interface on this network; guest trunking is
outside scope. Peer/service and forbidden-destination checks are owner-defined;
a ping refusal alone does not establish isolation. Same-host traffic does not
prove an uplink or cross-host path. Partial-failure inventories precede retries.
Retain network/PIF/switch objects pending an approved owner teardown; no deletion,
IP reconfiguration, VLAN/MTU edit or emergency-reset command is prescribed.

All installed scenarios below are **Pending**, including recovery. Record actual
host/image/RPM/UI identities, pool/master/host/network/PIF/VM/VIF IDs, timestamps,
baseline, expected and observed results, and sanitized console/task evidence.

| Scenario | Acceptance still required |
| --- | --- |
| Topology and access | Dedicated spare uplinks on every intended host, approved switch tagged path/VLAN/MTU, independent console exercised and management/storage baseline retained |
| Creation | Correct pool/master PIF UUID/device/MAC, type switches off, explicit VLAN/1500/NBD off, task result, exact resulting network UUID and no unintended duplicate |
| Host readback | Each PIF mapped to correct host/network/device/MAC, VLAN/MTU, no host IP/management use, attachment and carrier separately observed; no parent-PIF manipulation |
| Guest traffic/isolation | Exact VIF mapping and resident host, no inherited bypass, unique guest IP/route/DNS, approved peer/service works and owner-defined forbidden destinations fail with meaningful evidence |
| Persistence and boundaries | Guest normal stop/boot and repeat mapping/traffic; management/storage/XOA reachability; cross-host and migration need separately approved fixtures |
| Refusal/partial failure | Permission/selector/preexisting/duplicate/error inventory, actual leftovers on every host before retry, no assumed transactional rollback |
| Incident/recovery | Controlled disposable fixture, stop guest, independent console/network-owner recovery plan and actual restored access; no live-management experiment |
| Lifecycle and wider scope | Owner-approved consumer inventory and teardown remain pending; bonds, host IP/management migration, VLAN/MTU editing, PIF removal and SDN need separate procedures/acceptance |
| Locale review | Installed EN/FR/JA labels, human language/technical review and task discovery; all FR/JA translations stay drafts |

Website coverage retains the 20-page manual / 40 FR/JA draft queue. Add a VLAN
query per locale and fragment navigation from the manual and the guest-interface
section at 390/320px, JavaScript on/off. Existing root/subpath, regression,
CLI/configuration, browser/accessibility and 57 Lighthouse checks remain.
Final checks, artifact identities and visual review are recorded on the PR.

## SN05 network connectivity diagnosis (2026-10-15)

Continued after merged #237 (`cc55872846ba1b69f6c7795dccfec5ad67306bdf`).
EN/FR/JA troubleshooting adds `network-connectivity`, linked from the manual and
storage/network chapter. Release scope stays image xoa-image-20261009-5f33c81,
application v5.113.2_e281c536-ce38 and XO 5.113.2. No appliance, host, guest,
switch or storage system was operated. No failure or network change was induced.
The latest xcp-ce run observed at implementation start was 38692107149, before
#237; this batch does not claim deployment acceptance of #237.

### Pinned source review

All XO paths below were read at
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. The ce38 patch set in
`xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19` contains no override of these
network views, mapping fields or the named VIF label IDs. This is source evidence,
not an observation of the installed UI.

| Finding | Source path |
| --- | --- |
| VIF device/MAC/network/MTU and UUID copy; status reads attached; fields and state buttons mutate configuration; reported IPs grouped by device separately from Allowed IPs and locking-mode policy | `packages/xo-web/src/xo-app/vm/tab-network.js` |
| VM addresses use guestMetrics.networks; VIF attachment uses currently_attached; allowed addresses and locking mode are separate fields | `packages/xo-server/src/xapi-object-to-xo.mjs` |
| PIF attachment is currently_attached; carrier is Boolean(metrics && metrics.carrier), so missing metrics can produce false; management/IP/VLAN/MTU and host/network references are separate | `packages/xo-server/src/xapi-object-to-xo.mjs` |
| Host PIF attachment button and carrier icon are separate; UUID copy, management badge and IP/VLAN/MTU fields | `packages/xo-web/src/xo-app/host/tab-network.js` |
| Pool summary uses master PIF; expanded PIF status reads carrier, not attached | `packages/xo-web/src/xo-app/pool/tab-network.js`, `packages/xo-web/src/common/sorted-table/pifs-column.js` |
| Enabled-state toggle and connection error are separate; error dialog preserves code/message; host field is editable | `packages/xo-web/src/xo-app/settings/servers/index.js` |
| EN Connected/IP addresses/Allowed IPs; FR Connecté/Adresses IP/IPs autorisées; JA retains these English VIF strings | `packages/xo-web/src/common/intl/messages.js`, `packages/xo-web/src/common/intl/locales/{fr,ja}.js` |

The diagnostic design separates client-to-appliance, appliance-to-host,
host-to-SR, appliance-to-backup and guest-to-service paths. Record exact endpoints,
protocol/port, address family, timestamps and object identities. Console display,
reported guest IPs, attachment, carrier and working application service are distinct
observations. Allowed IPs is traffic policy, not guest address assignment. The
owner chooses the service/forbidden-destination tests and any OS-specific tools;
no generic shell/reset, certificate bypass, policy removal, migration or management
change is prescribed. Same-host traffic cannot establish the uplink path. Repeat
the same service test after an owner-approved remedy, preserving isolation and
management/storage access. Bonds/SDN/trunks and emergency recovery are outside scope.

### Installed acceptance — all Pending

Record actual image/RPM/UI/host identities, VM/pool/resident-host/network/VIF/PIF
UUIDs, time with timezone, approved topology, expected/observed results and sanitized
evidence. Do not manufacture failures on live management or storage paths.

| Scenario | Acceptance still required |
| --- | --- |
| Path selection | Distinguish browser, appliance, host and guest origins; a working laptop or guest must not clear a host-to-NFS fault |
| VIF identity/state | Exact VM/device/MAC/network UUID mapping; stopped-VM detachment distinguished from running-guest symptoms; inspect without mutation |
| Guest reporting/policy | Compare missing or stale IP reports against guest console; record Allowed IPs and effective locking policy separately, without weakening it |
| Host path | Correct resident host, master-summary limitation, per-host UUID/VLAN/MTU and internal versus uplink topology |
| Carrier evidence | Distinguish attachment, carrier, missing metrics and actual switch/cable observations; no toggle to diagnose |
| Service/DNS/TLS | Agreed guest peer/service, address-family/DNS results and valid certificate identity; ping alone cannot accept service or isolation |
| Scope of traffic | Same-host success versus separately approved cross-host/off-host fixture; owner-defined forbidden destinations, no migration experiment |
| Remedy/recovery | Owner-selected correction, repeat same endpoint/service and isolation tests, management/storage recheck, preserve unresolved evidence |
| Locale acceptance | Installed labels and human EN/FR/JA technical/language review; FR/JA remain drafts |

Website validation adds three ranked searches (network connectivity / connectivité
réseau / ネットワーク接続) and 24 fragment navigations from manual/storage at
390/320px, with and without JavaScript. Existing queries, root/subpath builds,
regressions, reference contracts, reflow and 57 Lighthouse audits are retained.
Final CI and screenshot evidence are recorded on the implementation PR.

## BK04 incremental NFS backup/chain-restore pilot (2026-10-15)

Continued after #238 merge `9e7f1d20b2ca33374091de2a15eff4ccdb82300d`.
The EN/FR/JA backup chapter adds `delta-backups`; full-mode sections retain their
scope. Links from manual/troubleshooting and ranked search lead to the pilot.
The baseline stays image xoa-image-20261009-5f33c81 / ce38 / XO 5.113.2.
No VM/appliance/storage operation, backup, merge, failure injection or restore
was performed. All installed acceptance below is Pending.

File restore was considered first, but the pinned file-restore UI filters backups
to mode=delta. BK04 therefore precedes a future BK06 recipe. This batch does not
claim file-restore or delta functionality was tested on an appliance.

### Source observations

XO files were read at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`; HomeLab
recipe/patches at `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`. No delta/interval/
merge/restore algorithm override was found in that patch set. The core UI patch
localizes Advanced settings to FR Paramètres avancés / JA 詳細設定; do not infer
all labels from the upstream catalogs alone. Delta Backup, interval, Force,
NBD/purge/merge and differential-restore strings retain English at this pin.

| Finding | Path at XO pin |
| --- | --- |
| Delta mode selects mode=delta/remotes; admin backup area; delta button has XOA_PLAN gate; global fullInterval and target deleteFirst; synchronous merge and NBD/CBT controls | `packages/xo-web/src/xo-app/backup/{index.js,new/index.js}` |
| Schedule Force full backup sets fullInterval=1; off clears its override; schedule exportRetention and save/readback distinct from global interval | `packages/xo-web/src/xo-app/backup/new/new-schedule.js`, `packages/xo-web/src/xo-app/backup/new/index.js` |
| No eligible source base gives full export; latest successfully exported VDI bases, chain length and fullInterval test; interval 2 produces full/incremental/full for clean unchanged fixture; missing remote bases can force full per disk | `@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs` |
| Validates mergeable remote parent per VDI; beforeBackup cleans with merge/remove; export task records isFull; metadata includes per-disk differencing; retention filters mode=delta plus scheduleId in the VM directory; deletion capped by maxMergedDeltasPerRun | `@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs` |
| Transfer/chaining precedes cleanup when deleteFirst=false; VHD files deliberately lack checksum files because merge/chaining change them; a new point is not standalone VHD evidence | `@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs` |
| Snapshot cleanup retains latest job snapshot across schedules for delta; source snapshots and remote restore points have different retention purposes | `@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs` |
| Cleanup can repair metadata/remove temporary data and records warnings; synchronous setting controls whether afterBackup merge is performed here or may be delegated to a merge worker; not transactional | `@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs` |
| Run details derive Type full/delta from export isFull; raw metadata contains more detail; backup selector marks mode delta as incremental even for key/full points | `packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js`, `packages/xo-web/src/common/render-xo-item.js` |
| Delta dialog allows disk omission via null SR, defaults differential restore off and offers start/MAC switches | `packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js` |
| Ordinary delta restore reads remote disk chain; differential path may reuse source snapshots; ignored disks are filtered out | `@xen-orchestra/backups/ImportVmBackup.mjs`, `@xen-orchestra/backups/RemoteAdapter.mjs` |
| File-restore list excludes full-mode backups | `packages/xo-web/src/xo-app/backup/file-restore/index.js` |
| Literal/fallback labels | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` plus HomeLab `patches/zzz-xo-core-ui-translations.patch` |

Pilot decisions: retain earlier independent full backup; new empty dedicated NFS
remote and new job; unchanged ordinary disk set; normal guest shutdown by operator,
not offline-backup mode; one disabled schedule, retention 2, global fullInterval 2,
Force off, deleteFirst off, no long-term retention; NBD/CBT purge off, synchronous
merge on, no automatic health check. Actual build/plan availability must be read
back, not inferred from upstream plan gating or patched-source visibility.

Use sample versions/checksums A/B/C. Verify export type and warnings on each of
three runs, then verify whole-VM restore of incremental B before and after run 3's
retention/merging, plus key C. Include all disks, differential restore/start off,
new MACs, then remove all inherited VIFs before boot. Verify distinct VM/VDI UUIDs
and checksums; a green job, small transfer or listed point alone is insufficient.
Missing parent/fallback/partial transfer/merge issues stop further manual runs;
no VHD/JSON editing, deletion of source snapshots, force or repair/reset recipe.

| Installed scenario — all Pending | Evidence still required |
| --- | --- |
| Preconditions | Exact installed identities and feature access, independent full restore accepted, dedicated remote/export and source/remote/destination capacity, VM/disk/sample IDs |
| Job persistence | Correct explicit VM/remote, new job/schedule IDs, global interval 2, Force off, retention 2, synchronous merge on, NBD/purge/other modes off, schedule disabled after save/reopen |
| Export sequence | A full, B incremental, C full with run IDs, actual Type/isFull/warnings and observed restore-point identities; missing-base fallback not counted as incremental success |
| Retention/chain | Inspect cleanup/merge warnings and remaining points; expected B/C for clean fixture, extra-point or missing-point explanation, no filesystem-level manipulation |
| Restore independence | B restored before/after cleanup and C separately, all disks included, differential/start off, new VM/disk IDs, every VIF removed before boot, correct version checksums |
| Failure/recovery | Controlled disposable fixture only, complete partial-object/chain inventory, owner-selected remedy and actual recoverability; no live-data failure injection |
| Locale and broader scope | Human/installed EN/FR/JA review, live consistency, production retention, NBD/CBT, other/encrypted remotes, differential and file restore remain pending |

Website tests retain the 20-page manual and 40 current FR/JA draft translations.
Three new ranked queries and 24 manual/troubleshooting-to-delta fragment checks
cover all locales, 390/320px and JS/no-JS. Existing searches, accessibility/reflow,
root/subpath builds, reference contracts, regressions and 57 Lighthouse audits
remain. Exact head/run/artifact and screenshot evidence belongs on the PR.

## BK06 file-level recovery from a retained delta point (2026-10-16)

Continued after #241 merged as `9aea2d1fccc82f5d2d5ce2960f26f5ca7a7550e3` into
`claude/gracious-ride-99qg08`. The EN/FR/JA backup chapter adds `file-restore`,
linked from the manual and troubleshooting. Baseline remains XO 5.113.2
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, XOA-HL package
`v5.113.2_e281c536-ce38` and image `xoa-image-20261009-5f33c81` at
HomeLab source `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`. These are pinned
source observations, not an installed appliance result. No backup, VM, guest,
filesystem or archive extraction was performed here.

| Source observation at XO pin | Path |
| --- | --- |
| Administrator backup route; File Restore action has an availability gate. The enabled-remote list filters VM backups to `mode=delta`; full-mode XVA is absent; nearby delete actions are separate. | `packages/xo-web/src/xo-app/backup/{index.js,file-restore/index.js}` |
| Selector chooses exact backup, disk and partition; empty partition list browses a raw filesystem, traversal starts at `/`; one file can be selected; `tgz` defaults and `zip` is offered. | `packages/xo-web/src/xo-app/backup/file-restore/restore-file-modal.js` |
| Partition/file listing and archive request require `admin`; file fetch registers an HTTP download with a restore filename and format extension. | `packages/xo-server/src/api/backup-ng.mjs`, `packages/xo-web/src/common/xo/index.js` |
| Remote adapter mounts VHD and a partition read-only for browsing, can discover ordinary partitions or LVM volumes, and streams tar/gzip or zip; actual helper/filesystem availability on the appliance was not checked. | `@xen-orchestra/backups/RemoteAdapter.mjs`, `packages/xo-server/src/xo-mixins/file-restore-ng.mjs` |
| The HomeLab recipe pins this XO source; no file-restore algorithm override was found in the selected patch set. | `xoa-hl/UPSTREAM_XO`, `xoa-hl/scripts/build-xo.sh`, `xoa-hl/patches` at `5f33c81` |

The controlled recipe uses the retained point B of BK04 after whole-VM chain
recovery, a single ordinary Linux sample file with its pre-backup B SHA-256,
and the exact disk/partition. Download its default tgz archive to a workstation,
inspect archive entries and extract only the sample into a new disposable
directory, then compare bytes/checksum B. Download is not guest reinjection.
No claim is made for full-mode XVA, every filesystem/RAID/LVM/encryption/remote,
symlinks, directories, production use or installed tooling. Errors preserve
identity and logs; no chain manipulation or forced repair is prescribed.

| Installed acceptance — all Pending | Evidence needed |
| --- | --- |
| Feature and point | Installed identity and admin access, enabled NFS remote, correct job/VM/time and retained B point after BK04 chain restore; no full-mode point substitution |
| Disk and scan | Exact disk and partition, ordinary filesystem and file path; scan/list success with no manual mounts or edits |
| Archive | Completed browser download, tgz filename/size/hash, archive entry inventory, one safely extracted sample and content/SHA-256 matching pre-backup B, not C |
| Failure/recovery | Actual error, point/chain and partial-download evidence, owner-selected remedy and repeatable success; stop further retention runs on failure |
| Locale and scope | Human EN/FR/JA review, installed filesystem/helper and plan availability; broader layout/remote and guest reinjection acceptance remains pending |

Three new ranked search cases and 24 file-restore fragment checks cover all
locales, 390/320px and JS/no-JS from manual and troubleshooting. Existing
root/subpath builds, reference contracts, regression checks and Lighthouse
must pass at the PR head. Exact run/artifact and screenshot evidence belongs on
that PR.

## BK05 full SR disaster-recovery replica pilot (2026-10-16)

Continued after #242 merged as `e74a3b3f1c1fd12e586fc4201b0e0da736d182a6` into
`claude/gracious-ride-99qg08`. The EN/FR/JA backup chapter adds `dr-replica`
and manual/troubleshooting links. Baseline is still XO 5.113.2 at
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, XOA-HL source
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19`, package
`v5.113.2_e281c536-ce38`, image `xoa-image-20261009-5f33c81`.
No appliance, VM, storage, replication or outage test was performed in this
review; installed acceptance remains Pending.

| Source observation at XO pin | Path |
| --- | --- |
| DR is full-mode, CR delta-mode; selecting either requires target SRs, not export remotes. DR is disabled below `XOA_PLAN` 3 and CR below 4 in upstream UI; installed HomeLab availability must be observed. | `packages/xo-web/src/xo-app/backup/new/index.js` |
| Schedule has separate `copyRetention` (Replication retention), not export retention. Global/target settings and disabled schedule need save/readback; `deleteFirst` is a target setting. | `packages/xo-web/src/xo-app/backup/new/{index.js,new-schedule.js}` |
| Full-mode runner exports the VM/XVA stream to a full XAPI writer on selected SR; normal halted single-disk fixture avoids live-consistency assumptions. | `@xen-orchestra/backups/_runners/_vmRunners/{_AbstractXapi,FullXapi}.mjs` |
| Full writer imports into target SR, tags `Disaster Recovery`, names source/job/timestamp, disables HA restart, blocks `start`/`start_on`, and records job/schedule/source/SR metadata; code explicitly instructs cloning to use it. With Delete first off, old replica deletion follows successful transfer. | `@xen-orchestra/backups/_runners/_writers/FullXapiWriter.mjs` |
| Retention identifies replicas by blocked-start metadata and job/schedule, source VM, SR; interrupted copies have a separate cleanup path. `copyRetention-1` older entries are pruned after transfer for the ordinary full fixture, but failures/partial objects must be inspected. | `@xen-orchestra/backups/_runners/_writers/_listReplicatedVms.mjs`, `@xen-orchestra/backups/_getOldEntries.mjs` |
| UI clone uses `vm.clone`, and API calls `xapi.cloneVm`; actual clone start-block behavior and disk/data health require an installed check. | `packages/xo-web/src/common/xo/index.js`, `packages/xo-server/src/api/vm.mjs` |
| HomeLab recipe pins XO source; no DR writer/mode algorithm override found in selected patches. FR labels include Reprise après panne/Clonage rapide; JA retains Disaster Recovery/Fast clone, while target SR and replication retention fall back to English in the catalog. | `xoa-hl/UPSTREAM_XO`, `xoa-hl/scripts/build-xo.sh`, `xoa-hl/patches` at `5f33c81`; XO `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

Pilot decisions: second disposable pool with dedicated writable SR in a distinct
storage failure domain; dedicated DR-only job and one disabled schedule,
copyRetention 2, deleteFirst off, explicit source VM, no export remote,
smart selection or other mode. Retain the independent NFS backup. Create stopped
guest versions A/B/C, inspect three full copies and B/C inventory after
retention; never start or unblock a replica. Clone retained B on the target,
confirm distinct IDs and normal start eligibility, remove all VIFs while
stopped, boot only the clone via console and compare checksum B. Stop if clone
remains blocked. Do not present this as a source-pool outage or failover test.

| Installed acceptance — all Pending | Evidence needed |
| --- | --- |
| Preconditions | Exact installed identities/DR access, two disposable pools and distinct failure domains, target SR UUID/capacity/host access, source VM/disk and independent NFS restore |
| Persistence | DR-only full job, correct explicit VM and one target SR, schedule ID/timezone/disabled readback, replication retention 2, Delete first off |
| Copies/retention | Three completed runs with run JSON, source/target VM and disk IDs, stopped/tagged/blocked A/B/C replicas, observed B/C after cleanup or explained deviation and partial objects |
| Isolated clone | Retained B selected, new target VM/VDI IDs, no lingering start block, all NICs removed before boot, console checksum B, source and retained replicas intact |
| Failure and wider scope | Owner-reviewed partial transfer/deletion/clone remediation; CR delta chains, planned operation, pool outage, network cutover/split-brain, failback, production recovery and human EN/FR/JA review |

Three new ranked queries and 24 manual/troubleshooting-to-DR fragment checks
cover EN/FR/JA at 390/320px with JS/no-JS. Existing root/subpath builds,
reference checks, accessibility and Lighthouse remain required. Record exact
head/run/artifact and rendered capture evidence on the PR.

## BK09 pool metadata backup pilot (2026-10-16)

Continued after #243 merged as `64aad7a0b05880ef2b993a67e77a9bb8b8c21b70` into
`claude/gracious-ride-99qg08`. The EN/FR/JA configuration chapter adds
`pool-metadata` and links from the manual and troubleshooting. Baseline remains
XO 5.113.2 at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, XOA-HL source
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19`, package
`v5.113.2_e281c536-ce38`, image `xoa-image-20261009-5f33c81`.
No appliance, pool, metadata export or restore was operated in this review.

| Source observation at XO pin | Path |
| --- | --- |
| Metadata job editor supports Pool metadata and XO config separately, selected pools and remotes, schedules and per-mode retention (display default 1). It has a plan gate of 3; actual HomeLab installed availability must be checked. | `packages/xo-web/src/xo-app/backup/new/metadata/index.js` |
| API job create/run/list/restore is admin-only. Restore resolves the selected target pool UUID; do not infer that a different pool can safely accept a dump. | `packages/xo-server/src/api/metadata-backup.mjs` |
| Runner resolves the selected pool and remote, checks nonzero matching retention and logs per-pool and per-remote tasks. An aggregate result alone is insufficient evidence. | `@xen-orchestra/backups/_runners/Metadata.mjs` |
| Pool writer reads `/pool/xmldbdump` from XAPI, writes raw `data` and a `metadata.json` containing job, pool/master, schedule and timestamp under `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. Output checksum is disabled and retention follows the writes. | `@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs` |
| Retention sorts timestamp directories and prunes older entries; UI lists enabled remote points and offers Restore/Delete actions. | `@xen-orchestra/backups/RemoteAdapter.mjs`, `packages/xo-web/src/xo-app/backup/restore/metadata.js` |
| Pool restore sends the selected `data` stream to `/pool/xmldbdump` on the chosen XAPI. The source does not establish a transaction-wide rollback, compatible cross-pool identity or completed host recovery. | `@xen-orchestra/backups/RestoreMetadataBackup.mjs` |

Pilot decisions: one disposable rebuildable pool, one separate dedicated writable
NFS remote, pool mode only, one disabled schedule with explicit timezone,
retention 2 and three sequential manual runs A/B/C. Observe per-pool/remote
logs, point inventory and protected remote files; expect retained B/C or
record deviations. Do not select Restore/Delete, inspect the raw dump publicly,
or infer pool recovery. Preserve independent XO configuration export and VM
backups. A separate owner-reviewed isolated restoration needs a matching pool
identity/version plan, independent fallback, production isolation and post-import
host/pool checks.

| Installed acceptance — all Pending | Evidence needed |
| --- | --- |
| Preconditions | Exact installed identities/feature access, source pool/master/host UUIDs, remote ID/capacity and independent guest/XO protection |
| Job persistence | Pool-only selection, separate remote, one schedule ID/timezone/disabled readback and pool retention 2 |
| Export and retention | A/B/C job and child task logs, pool/remote identity, nonempty `data` and `metadata.json` for retained B/C, protected sizes/hashes and partial/pruning deviations |
| Restore boundary | Pool owner approval and isolation, same-identity/version recovery plan, fallback copy, import result, post-import connectivity/inventory; bulk/cross-pool and production restore excluded |
| Wider scope | Failure injection, secrets review, host/image recovery, human EN/FR/JA review and production policy |

Three new ranked queries and 24 manual/troubleshooting-to-metadata fragment checks
cover EN/FR/JA at 390/320px with JS/no-JS. Existing root/subpath builds,
reference checks, accessibility and Lighthouse remain required. Record exact
head/run/artifact and rendered capture evidence on the PR.

## BK02 Windows Server SMB remote pilot (2026-10-17 JST)

Continued after #244 merged as `a617c825f3184b33b05d64740254babd10691fba`
into `claude/gracious-ride-99qg08`. EN/FR/JA backup chapter adds `smb-remote`
with links from manual and troubleshooting. Baseline remains XO 5.113.2 at
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, XOA-HL source
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19`, package
`v5.113.2_e281c536-ce38`, image `xoa-image-20261009-5f33c81`.
No appliance, SMB share, VM backup or restore was operated in this review.

| Source observation at pinned revisions | Path |
| --- | --- |
| SMB form needs `address\\share`, optional subfolder, username/password and domain (default `WORKGROUP`). It warns that SMB is meant for Windows Server; use NFS for Linux Samba/most NAS. | XO `packages/xo-web/src/xo-app/settings/remotes/remote.js`, `packages/xo-web/src/common/intl/messages.js` |
| Parser formats SMB URL fields; a successful parse is not a mount or restore guarantee. | XO `packages/xo-remote-parser/src/index.js` |
| SMB handler constructs a CIFS mount with domain and USER/PASSWD environment; mount handler invokes `mount -t cifs`, keeps the mount open and unmounts when forgotten. Installed helper/share access still needs observation. | XO `@xen-orchestra/fs/src/{smb,_mount}.js` |
| `Test your remote` writes 10 MiB random bytes, reads and compares them, attempts deletion in `finally`; it reports the failing step and may leave a test file. Remote errors and enabled state are tracked separately. | XO `@xen-orchestra/fs/src/abstract.js`, `packages/xo-server/src/xo-mixins/remotes.mjs`, `packages/xo-web/src/xo-app/settings/remotes/index.js` |
| XOA-HL's RPM declares `cifs-utils` (along with NFS and other helpers), and its XO pin matches the reviewed source; installed package/behavior is not established by the spec. | XOA-HL `SPECS/xoa-hl.spec`, `UPSTREAM_XO` at `5f33c81` |

Pilot decisions: dedicated disposable Windows Server share outside source/appliance
storage failure domain, protected dedicated account, one explicit halted VM,
separate `lab-smb-full` Backup-only job, one disabled schedule and retention 2,
Delete first off. Test the exact remote, run one full export, restore that exact
point to a distinct stopped VM on a writable SR, remove all VIFs before boot and
compare a new guest checksum over console. Preserve the independent NFS backup.
Do not publish credentials or infer sustained throughput or production readiness
from a 10 MiB remote test. Server administrator supplies share ACL and capacity;
no server commands are prescribed in this browser-based pilot.

| Installed acceptance — all Pending | Evidence needed |
| --- | --- |
| Preconditions | Exact installed identity/CIFS helper, Windows Server/share and dedicated account permission, isolated reachability, capacity, original VM and independent NFS point |
| Remote test | Remote ID/type/enabled/error, server/share/subfolder without secret, 10 MiB test result/write-read-delete step and exact leftover file if failed |
| Full export and isolated restore | One saved disabled full-only job/schedule, exact VM/remote IDs, run and full point, target SR, distinct stopped VM/VDI, empty VIF list before boot and matching checksum |
| Wider scope | Credential rotation, domain trust, dialect/security negotiation, longer throughput, share outage, multi-run retention/pruning, Linux Samba/NAS, S3/Azure/local providers and human EN/FR/JA review |

Three new ranked queries and 24 manual/troubleshooting-to-SMB fragment checks
cover EN/FR/JA at 390/320px with JS/no-JS. Existing root/subpath builds,
reference checks, accessibility and Lighthouse remain required. Record exact
head/run/artifact and rendered capture evidence on the PR.
