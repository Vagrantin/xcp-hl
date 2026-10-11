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
