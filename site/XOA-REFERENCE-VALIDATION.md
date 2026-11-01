# Concepts, configuration and automation reference (#189 / D5 #200)

## Scope and released sources

This documentation batch follows merged #208 at
`e934f99e45e1fdf8c7575f48e2a91f888c5d349b` on
`claude/gracious-ride-99qg08`. Three new chapters have EN/FR/JA counterparts:
concepts and source-visible feature scope, appliance service configuration,
and a read-only xo-cli inventory exercise. FR/JA remain drafts. The existing
eight controlled glossary entries supply the common sector terminology;
this does not complete the management-interface translation review in #131.

| Component | Reviewed identity |
| --- | --- |
| Image | `xoa-image-20261009-5f33c81` |
| Image source | `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4` |
| Package | `v5.113.2_e281c536-ce38` |
| HomeLab source | `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19` |
| XO product/upstream | XO 5.113.2, `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` |
| Server package | `xo-server` 5.193.1 |
| Client packages | `xo-cli` 0.32.2, `xo-lib` 0.11.1 |

Public chapters link the pinned source blobs. Product, server package, RPM and
image versions are distinct. XO 6 APIs and commercial Vates subscription claims
are outside this reference. A release matrix records shipped combinations,
not integration acceptance. No product build or appliance operation ran locally.

## Source observations and fixture boundaries

| Finding | Evidence at the identity above |
| --- | --- |
| 14 declared patches; selected Hub/XOA/proxy/XOSTOR menus hidden | `xoa-hl/patches/{metadata.toml,menu-hide-items.patch}` |
| HTTPS 443, generated TLS paths, local Redis bootstrap | `xoa-hl/scripts/build-xo.sh` |
| Root service; first-install operator config; TLS generation and legacy marker; disabled timers; restart in posttrans | `xoa-hl/SOURCES/xo-server.service`, `SPECS/xoa-hl.spec` |
| app-conf loader, automatic JSON settings, package defaults and sample | `XO/packages/xo-server/{src/index.mjs,config.toml,sample.config.toml,package.json}` |
| publicUrl advertises pool-discovery address; it does not create HTTPS/DNS | `XO/packages/xo-server/src/xo-mixins/xen-servers.mjs` |
| CLI password prompt, expiresIn request, method discovery, typed parameters and projections | `XO/packages/xo-cli/{index.mjs,config.mjs}` |
| WebSocket `/api/`, authenticated connection, version endpoint | `XO/packages/xo-lib/src/index.js`, `packages/xo-server/src/api/{session,system}.mjs` |
| Token creation, own-token deletion, limits and profile controls | `XO/packages/xo-server/src/api/token.mjs`, `src/xo-mixins/authentication.mjs`, `config.toml`; `packages/xo-web/src/xo-app/user/index.js` |
| Inventory filters/limit; projection is client-side | `XO/packages/xo-server/src/api/xo.mjs`, `packages/xo-cli/index.mjs` |

`site/scripts/test_xoa_reference.sh` installs the exact direct fixture dependencies
and fetches the CLI files from the immutable upstream pin. The Node fixture
verifies their hashes before executing the actual client; it does not replace
its argument parsing with a copy. The fixture uses Node 24, xo-cli 0.32.2,
xo-lib 0.11.1, app-conf 3.0.0, @iarna/toml 2.2.5 and ws 8.18.3.
The dependency install is a documentation client test, not an XO/RPM build.
Registry transitive dependencies and compiled xo-lib are not a payload audit
of the released RPM.

CLI source hashes:

- `index.mjs`: `88ab9dd096b21a60d72cc0adf26eaa29f2a797a0661844cfc4f89616515872b8`
- `config.mjs`: `70b55517018213fd861a52f645eaedaa41f3db80b44e37366266328120af4698`

The HTTPS/WebSocket loopback fixture checks untrusted TLS refusal, trusted TLS
success, hostname mismatch refusal, password entry through a real PTY without
echoing it, the `1 hour` token request, credential mode 0600, default verification
enabled, method-name filtering, server version output, VM filter and projected
JSON array, typed object filter/numeric limit and malformed JSON refusal before
RPC. It verifies that unregister only clears local server/token fields and sends
no revocation request; the synthetic token remains usable until the fixture
explicitly revokes it, then authentication fails. Invented fixture credentials
never refer to a real user or appliance.

The configuration fixture checks the documented TOML structure, duplicate-table
failure and app-conf merging of port 443/TLS paths over vendor port 80 while
preserving local Redis. It isolates fixture files and does not write to `/root`
or `/etc`, restart services or connect to a real Redis database.

These results verify client/configuration contracts only. The mock server does
not run xo-server authorization, token expiration, XAPI, real inventory or profile
revocation. Discovery is not an authorization grant; filters and output projection
are not access boundaries. The docs do not promise ACL-filtered inventory.
The CLI's `list-commands --json` returns a value printed by the generic object
inspector at this pin, so the public discovery example uses readable output.
The API example uses the generic RPC command's working `--json` mode.

## Website validation

The manual checker requires 16 pages with synchronized meaning hashes. There
are 32 draft translations and 66 translated site pages. Root and subpath builds
validate 105 language switchers, 14,385/14,397 local links/assets, 45 aliases,
39 legacy paths and 53 legacy anchors. Six translation-drift regression cases
continue to pass.

Desktop/mobile interaction, ranked task search and no-JS navigation cover all
three references in every language. Existing queries remain assertions. Adding
the references exposed a Japanese `プール` regression: suggested CJK character
matches filled the 20-page candidate limit before the literal host/pool title
reached ranking. The search override now includes literal title candidates before
deduplication/capping, preserving the configured limits. This keeps the old query
and adds concepts/configuration/automation queries without weakening checks.

The new code examples also exposed insufficient light-theme contrast for Bash
builtins (`cd`, `umask`, `unset`): #0086b3 on #f2f7fc scored 3.85:1. A light-only
#006782 override corrects these tokens while preserving the dark palette.

The CI standalone job runs the contract fixture on Node 24, full browser checks
with Japanese fonts and 45 mobile Lighthouse audits (three new pages × three
languages added to the previous 36). Performance and accessibility gates remain
95. Exact final CI results are recorded on the PR, without implying appliance
acceptance. Appliance screenshot capture remains in jenkins-infra#87; no capture
backend or screenshot automation for a running appliance is added here.

## Previous merged batch deployment

#208 is deployed at https://xcp-hl.net/. The first rerun of today's deployment
failed because two retained artifacts were named `github-pages`. Recovery reran
the identical current workflow from an older scheduled run with no remaining
artifacts: [xcp-ce run 38027745601](https://github.com/Vagrantin/xcp-ce/actions/runs/38027745601),
build job `114424522977`, deploy job `114424587384`, both successful. The build
log identifies `e934f99e45e1fdf8c7575f48e2a91f888c5d349b` and passes the docs-only
artifact guard. All 12 daily-administration pages (four chapters × three languages)
returned the ce38 scope live. The new references need their own deployment after
merge. No RPM repository, signing policy or deployment workflow was changed.

## Remaining acceptance

| Check on a disposable released appliance | Required evidence |
| --- | --- |
| Feature scope | Installed UI matches the source observations; unsupported modes stay outside accepted coverage |
| publicUrl configuration | Valid TOML, effective merged settings, successful restart/login/inventory and next pool mark; console restoration tested |
| TLS and CLI registration | Trusted certificate/name succeeds, untrusted/mismatched certificate fails; real token request obeys configured bounds |
| Read-only inventory | Actual method parameters and JSON shapes; account visibility independently recorded; no VM changes |
| Token lifecycle | Actual expiry refusal and own-token revocation, tested before unregister; local cleanup verified |
| EN/FR/JA review | Native reviewers check sector terms, meaning and release applicability; #131 UI work remains separate |

#200 and #189 remain open until the agreed acceptance and human language review
are complete. Source review, synthetic contracts and website checks do not close
the remaining lab gates.

## Lab run 2026-10-27 (release-identified)

Findings filed during this run: #305 (Jenkins docs agents), #306 (interrupted update, rerun reports success), #307 (updater status gaps), #308 (appliance details), #309 (API inventory visibility), #310 (SSH password in xenstore), #311 (default admin after unclean shutdown). A finding keeps its scenario open until it is fixed or accepted; a failed or untested row is not a pass.

| Identity | Observed value |
| --- | --- |
| Appliance | docs lab XOA-HL VM, reset to baseline `2026-10-27-ce47` before the run |
| Image (`xoaHl.getVmVersion`) | built 2026-10-22, commit a280852, release v5.113.2_e281c536-ce40 |
| Application RPM | `xoa-hl-5.113.2_e281c536-47.gca44911.xcpng8.3.el9.x86_64` |
| Node.js on appliance | `nodejs-24.22.1-1nodesource` |
| Bundled client | `/usr/local/bin/xo-cli` -> `/opt/xo/packages/xo-cli/index.mjs`, xo-cli 0.32.2, xo-lib 0.11.1, xo-server 5.193.1 |
| Client source hashes | `index.mjs` 88ab9dd0...872b8, `config.mjs` 70b55517...af4698: both match the pinned hashes |
| Connected host | nested lab host, XCP-HL v8.3-ce44, product version 8.3.0 |
| Test account | `docs-cli@docs-lab.invalid`, permission `none`, no ACLs |

| Check | Expected | Actual | Status |
| --- | --- | --- | --- |
| TLS preflight (read-only commands) | Certificate metadata, no key output | `CN=xoa.local`, self-signed, no subjectAltName, valid 2026-10-22 to 2036-10-19; key 0600 root; `tls-generated` marker present | Pass |
| Operator file | Private | `/root/.config/xo-server/config.toml` is mode **0644** (world-readable); `config.z-auto.json` 0600 | Finding |
| Untrusted certificate | Refused | `DEPTH_ZERO_SELF_SIGNED_CERT`, exit 1 | Pass |
| Name mismatch (CA trusted, other name) | Refused | `ERR_TLS_CERT_ALTNAME_INVALID`, exit 1 | Pass |
| Trusted name (`xoa.local` via hosts entry) + `NODE_EXTRA_CA_CERTS` | Registered | "Successfully logged", exit 0; password prompted, masked with `*`, not echoed (typed at human pace through a PTY) | Pass |
| Credential file | 0600 | `config.json` 0600 in a 0700 folder; keys `allowUnauthorized:false`, `clientId`, `server`, `token` | Pass |
| `1 hour` token | Expires in 1 h | Expiration exactly issue time + 1 h; description `xo-cli@0.32.2 - <appliance hostname> - Linux x86_64` | Pass |
| Bounds: `1 year` (> `maxTokenValidity` 0.5 year) | Refused | Client: `JsonRpcError: unknown error from the peer` (-32000), exit 1; server log: `too high expiresIn duration: 1 year`. Not capped silently | Pass (message generic) |
| Bounds: `180 days` | Accepted | Accepted, expiry +180 days | Pass |
| `list-commands xo.getAllObjects` | Readable signature | `xo.getAllObjects [filter=<object|string>] [limit=<number>] [ndjson=<boolean>]`, exit 0 | Pass |
| `system.getServerVersion --json` | `"5.193.1"` | `"5.193.1"` | Pass |
| `list-objects --id --name_label --power_state type=VM` | Projected array | `[{"id":...,"name_label":"lab-first-vm","power_state":"Running"}]` | Pass |
| `xo.getAllObjects` filter + `limit=json:1` | One VM keyed by ID | One full VM object keyed by ID | Pass |
| `limit=1` (string) / malformed JSON | Refused before RPC | `invalid parameters ... must be number`, exit 1; malformed JSON exit 1 | Pass |
| Account visibility | Recorded | A `none` user with **no ACL** receives the full VM object (BIOS strings, xapi refs, VIF/VBD IDs) | Finding: confirms the chapter warning |
| Expiry refusal | Refused after expiry | `1 minute` token works at once; after 75 s `invalid credentials` (code 3), exit 1 | Pass |
| Own-token revocation | Refused, nonzero | `token.deleteOwn` from a second session (API behind the User page delete); revoked client gets `invalid credentials`, exit 1 | Pass (API, not the browser button) |
| `unregister` | Local only | Leaves `allowUnauthorized`, `clientId`; token still listed and still usable when reused | Pass (matches warning) |
| `token.deleteOwn` with no arguments | n/a | Server `TypeError: Cannot read properties of undefined (reading 'some')`; nothing deleted although both parameters are optional | Finding (upstream) |
| publicUrl in existing `[http]` table | Valid TOML, restart OK | Documented `node ... TOML.parse` check: `TOML syntax OK`; restart active in 15 s | Pass |
| After restart | Sign-in, hosts, console | Sign-in OK, server connected, host listed; console WebSocket returns `RFB 003.008` | Pass |
| Pool mark | publicUrl recorded | Pool `other_config` `xo:clientInfo:<appliance VM UUID>` gains `"publicUrl":"https://<appliance FQDN>"` at reconnect (not only at a later interval) | Pass (faster than documented) |
| Restore original operator file | Original behavior | Restart OK, server connected, `publicUrl` removed from pool mark at reconnect | Pass |
| Startup log | Clean | Every start logs `could not detect current commit ... spawn git ENOENT` | Finding (minor) |
| Feature scope (browser, admin) | Hidden menus | No Hub, XOA, Proxies or XOSTOR entries. Present: REST API doc, **Try XO 6 (/v6)**, XOA-HL Updates, XO config, Audit, Self service | Partial: Try XO 6 not in source record |
| Default appearance | Arctic + System | `data-xhl-theme=arctic`, `mode=system`, light scheme; stored `xoa-hl.appearance.v1` | Pass |
| Welcome banner | n/a | "Thank you for using XOA-HL! Documentation is available here" rendered in a red alert frame | Finding (screenshots) |
