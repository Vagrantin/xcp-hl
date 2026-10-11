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
