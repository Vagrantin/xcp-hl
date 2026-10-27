# Appliance operations batch (#189 / D4 #199)

## Scope and evidence level

This documentation-only batch follows merged #206 on the Hugo source branch
`claude/gracious-ride-99qg08`, merge commit
`5ec5fd7c871397fb240dd187d6d7efb8e11281ce`. It adds maintenance,
configuration export/isolated import preparation and troubleshooting in EN/FR/JA.
French and Japanese remain draft translations. It advances D4 and D7; it does
not close D4, the roadmap, or claim a supported rollback/recovery path.

#206 deployment was independently checked: `Vagrantin/xcp-ce` run
[38105978878](https://github.com/Vagrantin/xcp-ce/actions/runs/38105978878)
succeeded, and its build log records source commit `5ec5fd7c871397fb240dd187d6d7efb8e11281ce`.
The live Japanese backup/restore page contains the reviewed image identity and
NIC isolation guidance. This is website deployment evidence, not appliance
acceptance evidence. The new pages need their own deployment after merge.

## Released baseline

| Identity | Reviewed value |
| --- | --- |
| Image | `xoa-image-20261009-5f33c81` |
| Image build source | `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4` |
| Image published SHA-256 | `a9b621ce71c56445bb3998fe418cc5079c32340477a7a2830a3ef19609cfff0b` |
| Package release | `v5.113.2_e281c536-ce38` |
| RPM | `xoa-hl-5.113.2_e281c536-38.g5f33c81.xcpng8.3.el9.x86_64.rpm` |
| RPM published SHA-256 | `3e85d7688664dfd55426b1d5f7e88e692c17fc4bb75d4dce31e58b9b0095bc7a` |
| Application/build source | `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19` |
| Upstream pin | XO 5.113.2, `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` |

Published hashes above identify release metadata; this batch did not download,
boot or verify the XVA/RPM payload. Source review uses the XO5 pin with the
release's patches, not current upstream XO6. The generated root AGENTS.md's
older no-timer statement is superseded here by the released scripts below.

## Source findings

Paths are relative to the identified repository/commit. Public chapters link
the exact source blobs; these observations are not substitutes for lab tests.

| Finding | Source |
| --- | --- |
| Initial manual mode; appliance timezone; check persistence vs installation `Persistent=false`; schedule delay; no automatic reboot | `xoa-hl/docs/automatic-updates.md`, `SOURCES/xoa-hl-{configure-updates,auto-update}.sh`, timer units @ `5f33c81` |
| Full managed update excludes Node.js; shared managed lock; rc 75 on contention; log truncated before acquiring lock; final success/failure marker | `xoa-hl/SOURCES/xoa-hl-update.sh` @ `5f33c81` |
| Check maps dnf 100/0/other to AVAILABLE/UP_TO_DATE/ERROR; a busy check can exit successfully while recording ERROR | `xoa-hl/SOURCES/xoa-hl-check-update.sh` @ `5f33c81` |
| Automatic record uses UTC startedAt/finishedAt, result, exitCode, rebootNeeded; manual installation does not refresh it; unknown reboot assessment is distinct from no | `xoa-hl/SOURCES/xoa-hl-auto-update.sh` @ `5f33c81` |
| Stable/testing repository selection; switching channel changes selection without performing downgrade | `xoa-hl/patches/zzzzzzzz-xoa-hl-update-channel.patch` and managed scripts @ `5f33c81` |
| Operator TOML bootstrapped only if absent, update.conf is config(noreplace); xo-server restarted in posttrans | `xoa-hl/SPECS/xoa-hl.spec` @ `5f33c81` |
| Config screen route/actions and optional passphrase | `XO/packages/xo-web/src/xo-app/settings/config/index.js`, `common/xo/index.js`, `common/xo/{export,import}-config-modal/index.js` @ `e281c536` |
| Admin-only export/import; default gzip with config.json.gz[.enc]; JSON registered entries; OpenPGP encryption; dependency-ordered import without whole-operation rollback | `XO/packages/xo-server/src/api/xo.mjs`, `xo-mixins/config-management.mjs` @ `e281c536` |
| Export includes credential-bearing server/remotes/tokens, users, ACLs, jobs/schedules/plugins; import can reconnect servers, activate schedules, replace conflicting users | `XO/packages/xo-server/src/xo-mixins/{subjects,xen-servers,authentication,remotes,acls,scheduling,plugins}.mjs`, `jobs/index.mjs` @ `e281c536` |
| Config export lacks guest disks, pool metadata and appliance filesystem; no OS/package/TOML/TLS/update.conf/timezone restoration mechanism in exporter | Registered managers in `XO/packages/xo-server/src/xo-mixins/` and `config-management.mjs` @ `e281c536` |
| First-boot log and independent SSH/web accounts | `build-xoa-hl/scripts/xoa-credentials.sh` @ `2103968` and beginner validation record |

The configuration chapter's categories are examples, not an exhaustive promise
about every runtime plugin. Isolation must be imposed outside XO before import:
restored settings can re-enable both server connections and schedules before
an operator has time to change them. Import errors can leave partial changes;
a fresh disposable target is required for another test. No production import,
package downgrade, database deletion or forced update interruption was executed.

The canonical update guide now lists older package availability without a
mutating downgrade command or a time-dependent five-release guarantee. It
states the release-scoped recovery gap instead of "No known limitation".
Host update procedures, trust policy and localized/legacy anchors are preserved.

## Website validation

- Source parity: 52 translated pages, 18 explicitly draft manual translations.
- Manual checker: all nine required manual pages, controlled glossary IDs and
  English meaning hashes; existing six translation-drift/publication regression
  tests pass. Human review remains pending.
- Root and project-subpath Hugo builds: 84 language switchers, 9,708 local links
  and assets, 45 aliases, 39 legacy paths and 53 legacy heading/homepage anchors.
- Browser CI covers the new pages in all three languages, desktop and 390px
  mobile overflow checks, no-JS maintenance-to-configuration navigation and
  ranked maintenance/export/troubleshooting queries with locale isolation.
- Initial CI exposed low contrast in Hextra’s numeric shell tokens (`100` in
  diagnostic commands). The custom stylesheet now sets readable number colors
  for light mode while preserving the theme’s readable dark colors; the 95 gate
  is retained.
- Mobile Lighthouse CI includes all three new pages in each language, alongside
  the 15 existing entry/tutorial checks; performance/accessibility gate is 95.
  Final run results are linked in the PR/issue comments.

No appliance screenshots are synthesized. Capture implementation remains in
`jenkins-infra#87`; documentation can consume approved evidence later.

## Required disposable-lab acceptance

Keep an evidence record with installed versions, timestamps/timezone, operation,
expected/actual result and sanitized outputs. Owner and lab access remain to be
assigned in D0; native-language review remains D6.

| Scenario | Acceptance still needed |
| --- | --- |
| Manual check/install, no updates and available updates | Correct verdict, final log marker, installed version, reconnect and host inventory; auto status demonstrably not mistaken for manual result |
| Check/install modes and stable/testing | Saved settings, actual timers, local timezone/random delay and explicit installation confirmation |
| Powered off during scheduled window | Check persistence and no immediate replay of missed installation; actual later schedule confirmed |
| Browser disconnect / service restart | Transaction completes without duplicate operation; web login and host inventory recover |
| Interrupted update or appliance reboot | Disposable failure injection at recorded phase; preserved logs; recovery behavior established without declaring generic safe interruption |
| Reboot assessment yes/no/unknown | Match installed changes and helper availability; no automatic reboot; post-reboot login/version/inventory |
| Encrypted/unencrypted configuration round-trip | File, passphrase, account login, ACLs, remotes and representative jobs/settings validated |
| Wrong passphrase / conflicts / interrupted import | Record errors and partial-state behavior; disposable target rebuilt before retry |
| Import destination isolation | Network prevents production host, remote and external access throughout import; imported schedules/destinations disabled before test resources become reachable |
| Recovery after appliance loss | Same-version replacement proved with required separate files and access; no duplicate schedules against production |
| Older package / cross-version import | Determine supported version pair, data/OS implications and successful restoration before offering rollback/recovery as supported |
| Deployed page usability / EN/FR/JA review | New source deployed after merge; representative readers find tasks and locale reviewers approve meaning |

## Lab run 2026-10-27 (release-identified)

Starting point: docs lab XOA-HL VM reverted to baseline `2026-10-25-ce43`.

Findings filed during this run: #305 (Jenkins docs agents), #306 (interrupted update, rerun reports success), #307 (updater status gaps), #308 (appliance details), #309 (API inventory visibility), #310 (SSH password in xenstore), #311 (default admin after unclean shutdown). A finding keeps its scenario open until it is fixed or accepted; a failed or untested row is not a pass.

| Identity | Observed value |
| --- | --- |
| Application RPM | `xoa-hl-5.113.2_e281c536-43.gd7d202c.xcpng8.3.el9.x86_64` |
| Image | built 2026-10-22, commit a280852, release v5.113.2_e281c536-ce40 |
| Node.js | `nodejs-24.22.1-1nodesource` |
| Appliance timezone | Asia/Tokyo (JST, +0900), clock synchronized |
| update.conf | MODE=manual, FREQUENCY=daily, DAY=Sun, TIME=03:00, AUTO_REBOOT=no, CHANNEL=stable |
| Timers | none active in manual mode; check timer unit `Persistent=true`, install timer `Persistent=false`, both `RandomizedDelaySec=0` |

| Check | Expected | Actual | Status |
| --- | --- | --- | --- |
| Status before any check | Distinguishable from "up to date" | `xoaHl.getUpdateStatus` = `{"packages":[],"updateAvailable":false}`, no `/run/xoa-hl/status` | Finding: API shape cannot tell "never checked" from "up to date" (UI to confirm) |
| Manual check, stable, updates available | AVAILABLE with packages | `xoaHl.checkForUpdate` 11:34 JST: `updateAvailable:true`, 13 packages incl. `xoa-hl 45.g53cbcfd`, kernel 5.14.0-687.60.1, python3, xz; `/run/xoa-hl/status` = `AVAILABLE` + `checkedAt` (UTC) + package list | Pass |
| Auto record untouched by manual check | No change | `/var/lib/xoa-hl/auto-update.status` absent | Pass |
| Manual install (stable) | Success marker, version, reconnect, inventory | `xoaHl.startUpdate` 11:41:06; one dnf transaction (13 packages incl. kernel 687.60.1 and xoa-hl 43 to 45); `update.log` ends `=== xoa-hl update finished successfully at 2026-10-27 11:42:38 JST ===`; xo-server restarted 11:42:36; API version ce45; server connected; host listed; recheck `updateAvailable:false` | Pass |
| Second start during an update | Busy / no duplicate | Second `xoaHl.startUpdate` 0.3 s later also returned `{"started":true}`; no second transaction (systemd unit already activating) | Pass, finding: API reports `started:true` for a no-op |
| Manual run vs automatic record | Not mixed | `auto-update.status` absent; `lastRun` `{}` and history empty after the manual install | Pass |
| Reboot helper | Assessment possible | Running kernel 687.59.1 vs installed 687.60.1 after the manual update; `needs-restarting` (yum-utils) not installed | See reboot row |
| Testing channel | Candidates listed, nothing installed | `setUpdateChannel testing`: `CHANNEL=testing` saved, testing repo stays `enabled=0` in the file; check lists `xoa-hl 47.gca44911`; installed version unchanged (45) | Pass |
| Back to stable | No downgrade | `UP_TO_DATE`, still 45 | Pass |
| Check automatically, daily | Saved, timer in appliance time, no random delay | `MODE=check TIME=11:45`; drop-in `OnCalendar=*-*-* 11:45:00`, `RandomizedDelaySec=0`; ran 11:45:06 JST; `/run/xoa-hl/status` `UP_TO_DATE`, `checkedAt` UTC; next run next day 11:45; no `auto-update.status`, `lastRun` unchanged | Pass |
| Powered off during install window | No replay, next window kept | Install window 11:48 JST (testing, ce47 available); appliance halted 11:4x, booted 11:50; no auto-update journal entry this boot, still ce45, no new dnf transaction, no record; next run next day 11:48 | Pass |
| Install automatically | Record with UTC times, no reboot | Ran 11:54:07 JST; record `startedAt=02:54:07Z`, `finishedAt=02:54:44Z`, `result=succeeded`, `exitCode=0`, `rebootNeeded=unknown`; while running: `result=running`, empty `finishedAt`; history entry lists `xoa-hl` 45 to 47; same boot ID (no automatic reboot); API version ce47; server connected; host listed | Pass |
| Reboot assessment | yes/no/unknown matches changes and helper | Always `unknown` on the shipped image: script uses `/run/reboot-required` (never created on EL9) or `needs-restarting` (yum-utils, not installed). `dnf needs-restarting -r` (dnf-plugins-core, installed) answers correctly ("Reboot should not be necessary") | Finding |
| Manual reboot | Login, version, inventory | No update unit active; reboot 11:55; kernel 687.60.1, ce47, xo-server active, server connected, timers kept, record kept; `/run/xoa-hl/status` lost as documented, API back to `{"packages":[],"updateAvailable":false}` | Pass |
| Interrupted update (failure injection) | Logs kept, recovery established | Fresh ce43 revert; `xoaHl.startUpdate` 11:57:15; forced VM power-off from the host at 11:57:51 JST, dnf transaction step 4/22 (`xz-libs` upgraded, `kernel-modules` 687.60.1 installing). Boot in 20 s on kernel 687.59.1; xo-server active; still ce43; server connected; `update.log` kept up to the cut; dnf history transaction 2 marked incomplete (`##`); **`dnf check`: xz-libs duplicate**; kernel-core/modules 687.60.1 registered | Pass (boot), Finding (rpmdb) |
| Managed rerun after interruption | Repairs or reports problem | Check `AVAILABLE` (9 packages); rerun `=== finished successfully 12:00:29 ===`, ce45 installed; **duplicate kept** (`dnf check` fails); **kernel 687.60.1 registered but files corrupt** (`rpm -V`: `S.5` on `vmlinuz`, `System.map`), no `/boot` image, not in boot menu. Updater reports success anyway | Finding (serious) |
| Manual repair (no update unit running) | Clean rpmdb, bootable kernel | `dnf remove --duplicates` (reinstalled `xz-libs-...el9_8.1`), `dnf reinstall` of kernel-core/modules-core/modules 687.60.1: `dnf check` clean, `rpm -V` clean, `/boot` image + initramfs, default kernel 687.60.1; reboot: kernel 687.60.1, ce45, xo-server active, server connected, host listed | Pass (verified procedure) |
| Clock after snapshot revert | Correct time | Appliance clock about 90 s ahead right after a revert until chrony corrects it; affects log timestamps in revert-based tests | Note |

### Configuration export/import and pool metadata (source: ce47 baseline)

Source state built by API: group `docs-ops` with user `docs-op`, viewer ACL on the lab VM, NFS remote `docs-nfs` (disposable lab NFS VM; remote test OK), full VM backup job `lab-vm-full` (schedule `nightly`, disabled, Asia/Tokyo, retention 2), pool metadata job `lab-pool-metadata` (pool metadata only, schedule `pool-meta`, disabled, Asia/Tokyo, pool retention 2). Isolation note: every destination in the export is a lab object (nested lab host, lab NFS VM), so network isolation was **not** enforced with a firewall; the import targets were reverted lab appliances.

| Check | Expected | Actual | Status |
| --- | --- | --- | --- |
| Pool metadata runs A, B, C (manual, disabled schedule) | Each run succeeds per pool | 3 runs `success`, pool sub-task `success` each | Pass |
| Kept points, retention 2 | B and C only | Restore list and remote show `20261027T030513Z` (B) and `20261027T030533Z` (C); A removed | Pass |
| Remote files (as storage admin) | Non-empty `data` and `metadata.json`, matching IDs | `data` 431,979 B (different SHA-256 per point), `metadata.json` 119,357 B; job, schedule and pool IDs match. `metadata.json` also embeds the pool record incl. XO client info (appliance addresses) | Pass |
| Schedules after runs | Still disabled | Both disabled | Pass |
| Export, plain | `config.json.gz` | `xo.exportConfig` returns one-time `$getFrom`; 1,403 B, gzip; entries: 3 users, 1 group, 1 ACL, 1 server, 1 remote, 2 jobs, 2 schedules, 18 plugins, 0 tokens | Pass |
| Export, encrypted | `config.json.gz.enc` | 1,504 B, OpenPGP symmetric (AES-256); `gpg` decrypts it with the passphrase to the gzip | Pass |
| Wrong passphrase | Error, no change | HTTP 500; server log `Error decrypting message: Session key decryption failed.`; target unchanged | Pass (generic HTTP 500 to the client) |
| Encrypted round trip | Entries restored | `config successfully imported`; users, group membership, ACL, remote, jobs, schedules (still **disabled**) and the remote's metadata points match the source; exported `docs-op` signs in | Pass |
| Conflicting user | Recorded | Target had its own `docs-op` (other ID and password): the import **replaced** it with the exported user; only the exported password works | Pass (matches warning) |
| Interrupted import | Partial state recorded | Not achieved: `SIGKILL` of xo-server landed about 7 ms after a 1.5 KB import had already completed; xo-server auto-restarted in 6 s with all entries persisted | Not tested |
| Cross-version: ce47 export into ce43 | Recorded | Success, all entries restored | Pass (same XO 5.113.2 upstream only) |
| Cross-version: ce43 export into ce47 | Recorded | Success, all entries restored | Pass (same XO 5.113.2 upstream only) |
| Upload content type (tooling note) | n/a | A POST to `$sendTo` labelled `application/x-www-form-urlencoded` reaches the handler empty (`Unexpected end of JSON input` / OpenPGP parse error); browsers send the file type, so the UI is not affected | Note for scripted imports |
| Recovery after appliance loss (same version) | Replacement works from the separate files; no duplicate schedules | Source appliance halted ("lost"). Replacement: fresh XO Lite deployment of `xoa-image-20261027-ca44911` (ce47, same application version as the export). Encrypted export + passphrase (kept off the appliance) imported: `config successfully imported`; exported admin signs in; users, group, ACL, NFS remote, server (connected), both jobs, both schedules (still disabled) and the remote's metadata points match. Old appliance stayed halted, so no duplicate active schedules. Operator TOML, TLS files and `update.conf` were defaults on both, so no separate file needed restoring (not exercised) | Pass |
| Replacement after an unclean shutdown | Deployment credentials kept | Replacement reverted to a snapshot taken while running (crash-consistent): Redis came back with the image-build `dump.rdb` (RDB only, `appendonly no`); deployment admin gone; **`admin@admin.net` with the default password is an active admin**; first boot does not re-run. Clean shutdowns are not affected (#311) | Finding (serious) |
| Default admin after recovery import | Only exported accounts | `admin@admin.net` still active after the import: import does not remove existing users | Finding |
