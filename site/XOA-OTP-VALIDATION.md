# SE04 local-account OTP sign-in (#189 / D3 #198)

## Scope and branch review (2026-10-14)

This completes the EN/FR/JA draft begun at `docs/sign-in-otp@bcba65e77055aecb01129822eb2f096c92cf72c6`, after VM-transfer #221 merged as `bea5c60`. #218 is also merged. The OTP chapter is now linked from the manual and permissions guide, required by the manual checker and covered by ranked search, desktop/mobile/no-JS, keyboard/reflow and Lighthouse checks in every locale.

The source baseline remains image `xoa-image-20261009-5f33c81`, appliance build `build-xoa-hl@210396877e15d8761f579f569f1d911cc35b05e4`, application `v5.113.2_e281c536-ce38` / `xoa-hl@5f33c81f1ae2e74a300dcc33103f4e06cf565c19`, and XO 5.113.2 at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. These identify reviewed sources, not an installed appliance or tested compatibility. Release payload identities remain in [the feature inventory](XOA-FEATURE-INVENTORY.md).

No account was enrolled, signed in, reset or recovered. There are no appliance screenshots or human review records. FR/JA stay drafts; the reviewed-publication gate remains enforced. Screenshot infrastructure belongs in `jenkins-infra#87`.

## Source findings

Paths below are relative to `vatesfr/xen-orchestra@e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. The existing source review tree has the ce38 HomeLab patches applied; relevant UI/backend paths are unchanged except the shared action file/catalogs. Catalog literals were read from the patched tree, with English fallback when missing/undefined.

| Finding | Pinned source |
| --- | --- |
| OTP appears when `XOA_PLAN > 2` or an OTP secret exists; open-source default is 5. The HomeLab script invokes the normal build. Missing installed controls need a versioned report, not a paid-tier assumption | `packages/xo-web/src/xo-app/user/index.js`, `packages/xo-web/gulpfile.js`; `Vagrantin/xoa-hl@5f33c81:scripts/build-xo.sh` |
| Browser generates the secret and checks enrollment; cancellation writes nothing. A valid browser check is not appliance-clock acceptance | `packages/xo-web/src/common/{otp-authenticator.js,xo/add-otp-modal.js,xo/index.js}` |
| Enrollment QR issuer is `Xen Orchestra`; post-enrollment QR issuer is `XenOrchestra`. Both label the entry with `user.email`; the saved secret is displayed on the user page | `packages/xo-web/src/common/xo/add-otp-modal.js`, `packages/xo-web/src/xo-app/user/otp.js` |
| Password web login retains a pending user before redirecting to `/signin-otp`; a valid code creates a token. Wrong code renders `Invalid code`; template Code/Sign in is hardcoded English | `packages/xo-server/src/index.mjs`, `packages/xo-server/signin.pug` |
| Server uses six digits, 30-second steps and default window 1 (previous/current/next step); browser enrollment uses otplib, not this server helper | `@vates/otp/index.mjs`, `packages/xo-web/src/common/otp-authenticator.js` |
| Every valid authentication token bypasses OTP, regardless of creation date. Enrollment does not revoke tokens; existing web cookies remain accepted. Provider bypass paths require separate acceptance | `packages/xo-server/src/xo-mixins/authentication.mjs`, `packages/xo-server/src/index.mjs` |
| Own-user toggle and admin Users/OTP Remove both confirm before clearing the preference; no fresh OTP/password challenge is added to these UI actions | `packages/xo-web/src/common/xo/index.js`, `packages/xo-web/src/xo-app/settings/users/index.js`, `packages/xo-server/src/api/user.mjs` |
| Recovery CLI clears OTP/authProviders, resets password and makes an existing account Admin (or creates an account); availability/use on the image remains unvalidated | `packages/xo-server/src/recover-account-cli.mjs` |
| FR OTP labels fall back to English; JA OTP code and Authentication tokens fall back, while toggle/add/remove labels have Japanese literals | `packages/xo-web/src/common/intl/{messages.js,locales/fr.js,locales/ja.js}` |

Review corrections clarify that newly created tokens also bypass OTP, record the two QR issuer spellings, qualify the control's source-visible availability and add fresh-login verification after removal. Other authentication providers, enforced organization-wide MFA, sole-admin recovery commands and token permission scope remain outside this pilot.

## Disposable-appliance acceptance

Every row remains **Pending**. Use local-password test accounts, retain an independent administrator session, and record image/package/installed versions, UI language, expected/actual result and operator/date. Never record passwords, OTP values, secrets, QR codes or authentication tokens in artifacts. Use sanitized descriptions of the secret-bearing screens.

| Scenario | Required observation |
| --- | --- |
| Installed availability | User control and Users OTP column exist; exact EN/FR/JA labels, default build identity |
| Enrollment/cancellation | Cancel leaves OTP disabled; incorrect code retries; valid code saves; saved toggle persists after reload |
| Clock difference | Browser/authenticator/appliance time recorded; fresh sign-in checked independently of enrollment; restore time sync after controlled clock test |
| Fresh local sign-in | New private session asks for code after password; valid code succeeds as expected identity; wrong code fails; a code outside the server window fails |
| Existing session/token | Existing session survives enrollment; a valid preexisting token still authenticates without OTP; a newly created test token also bypasses OTP |
| Token revocation | Delete only the disposable test token; new use fails; retained administrator session remains usable |
| Own-account removal | Confirm clears secret/toggle; new local-password session succeeds without OTP; cancellation leaves OTP enabled |
| Admin-assisted lost device | Verify test requester identity; admin removes only that user's OTP; Not configured appears; user re-enrolls and fresh sign-in succeeds |
| Secret exposure | User page retains secret/QR as source describes; observations sanitized; no secret-bearing screenshots uploaded |
| Sole-admin recovery | Separate controlled image test must validate CLI packaging, configuration/data access, service handling and resulting account permissions before a recovery procedure is published |
| Language/assistive review | Named technical and FR/JA reviewers, installed labels, screen-reader and human mobile/readability checks |

Website checks verify documentation behavior only. The expected queue has 18 pages per locale and 36 draft translations; source hashes bind this chapter and its changed entry links to the checked translations. Final CI evidence belongs in the PR/tracker after the exact head completes.

## Lab run 2026-11-02 (blocked before reset)

See the [shared session preflight and identity record](XOA-DAILY-VALIDATION.md#lab-run-2026-11-02-blocked-before-reset).
Jenkins reset #163 and stop #164 succeeded for the reserved session. The
[shared record](XOA-DAILY-VALIDATION.md#lab-run-2026-11-02-blocked-before-reset)
contains the observed XCP-HL host/XO Lite identities and SR inventory. The
private `docs-capture` password was unavailable, so no XOA UI scenario ran;
XOA image/About/RPM identities were not observed. Historical ce47 evidence is
not transferred to this session. This remains blocked, not a product failure.

| Run / inventory ID | Expected | Actual | Result |
| --- | --- | --- | --- |
| 27 SE04/SE05 | Browser enrollment/cancellation, fresh login, removal and isolated sole-admin recovery | Reset/preflight only; XOA credential unavailable, no acceptance operation | Blocked |

PR #336 already records ce47 login-window/token observations. They were checked, not repeated; the remaining UI and recovery rows stay open. No OTP secret, code or credential was collected.

## Lab run 2026-11-03 (credential refused before acceptance)

[Jenkins reset #174 and stop #175](XOA-DAILY-VALIDATION.md#lab-run-2026-11-03-credential-refused-before-acceptance)
completed and left both lab VMs halted with the marker removed. A private
`docs-capture` sign-in returned `invalid credentials` twice. No appliance
identity or acceptance scenario was observed in this session, so the row above
remains blocked. The login identity is being checked; no product defect is
claimed.

## Lab run 2026-11-03 (ce51 RPM, OTP and sole-admin recovery)

The appliance-only `ga-x-xoa` cell used AlmaLinux 9.8 and RPM `xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64`, Node v24.22.2 and xo-server 5.193.1. This was an RPM installation, not the published XVA. Browser: Playwright Core 1.58 and Chromium 156. Jenkins reset #191 was the capacity gate; the cell operations were not Jenkins jobs. The cell was removed by its `ga-cell=x` tag. No passwords, OTP secrets, tokens or screenshots are included.

### Run 27 SE04/SE05 OTP enrolment, fresh login, removal and sole-admin recovery

Method: all behaviour under test through the browser (headless Chromium, disposable contexts, self-signed certificate accepted); API only for setup (user, token creation) and readback. TOTP codes computed locally (RFC 6238, SHA-1, 6 digits, 30 s; generator checked against the RFC 6238 vectors, t=59 gives 287082 and t=1111111109 gives 081804). Secrets lived only in a root-only tmpfs directory and are deleted at the end. Accounts: `otp-a@lab.invalid` (permission User), default `admin@admin.net` (sole Admin). Already recorded in PR #336 and not repeated as passes: ce47 login-window and repeated-wrong-code results.

| Run / ID | Expected | Actual | Result |
| --- | --- | --- | --- |
| 27 Installed availability | OTP switch on user page; Users page OTP column | User page (`/#/user`) has **OTP authentication** with a toggle icon; Settings > Users has columns Username, Member of, Permissions, Password / Authentication methods, OTP. Un-enrolled row shows `Not configured`, enrolled row shows a `Remove` button. Language: English only (FR/JA not reviewed) | Pass |
| 27 Cancel | Cancel leaves OTP off | Dialog **Add OTP authentication** (text "To enable OTP authentication, add it to your application and then enter the current password to validate", field **OTP code**, QR image, secret text with copy button, OK / Cancel). Cancel: toggle still off, still off after reload, Users column still `Not configured` | Pass |
| 27 Wrong code at enrolment | Dialog stays, retry | Wrong code (computed 600 s away) left the dialog open with inline `Password is invalid` (the label says Password although the field is the OTP code), same secret kept, toggle off. Right code then closed the dialog, toggle on, still on after reload | Pass; UX note: error wording says "Password" |
| 27 Secret exposure | Page keeps secret and QR as source says | After enrolment the user page shows the secret as text and a QR image (`img alt=qrcode`). Decoded the two QR images locally: the enrolment dialog QR is `otpauth://totp/Xen Orchestra:<login>?issuer=Xen Orchestra&secret=...`; the user-page QR is `otpauth://totp/XenOrchestra:<login>?issuer=XenOrchestra&secret=...` (matches the chapter's two issuer spellings). Both carry only `issuer` and `secret`, 32-character secret. No secret recorded | Pass |
| 27 Fresh local sign-in | New private session asks for code; right code OK; wrong code fails | Password then redirect to `/signin-otp` (single field `otp`). Wrong code: page text `Invalid code`; right code: signed in, user page shows the expected account and toggle on | Pass |
| 27 Existing session | Survives enrolment | Browser session open before enrolment kept working after enrolment (reload of `/#/user`, toggle on, no sign-in prompt) | Pass |
| 27 Existing and new tokens | Both bypass OTP | Token T1 (created before enrolment) and T2 (created after, from the T1 session) both `session.signInWithToken` OK after enrolment with no code. API `session.signIn` with email and password only for the enrolled account returned `invalid credentials` (OTP is enforced on API password sign-in) | Pass |
| 27 Token revocation | Delete only the test token | Deleted T2 in User page > Authentication tokens (confirm dialog **Delete authentication token**, which prints the full token text). Then T2 `signInWithToken`: `invalid credentials`; T1 still valid; retained browser session and admin session still usable | Pass |
| 27 Forget all authentication tokens | Removes every token except current session | Button has no confirmation: token list went to 1 row (current session) and the earlier tokens (incl. an admin test token) stopped working; current session stayed signed in | Pass |
| 27 Clock difference | Record times; clock test; restore | Client UTC 04:58:13.222, appliance 04:58:13.469, chrony 0.0006 s fast. Stopped chronyd and set the appliance clock ahead: +20 s with the true-time code accepted; about +120 s with the true-time code rejected (`Invalid code`) and the code computed for the appliance clock accepted. `systemctl start chronyd; chronyc makestep`: appliance 04:58:36.044 vs client 04:58:36.094, `System clock synchronized: yes`, true-time code accepted again | Pass (closes the "wrong appliance clock" gap named in PR #336) |
| 27 Own-account removal | Confirm clears; cancel keeps | Dialog **Remove OTP authentication**, "Are you sure you want to remove OTP authentication?". Cancel then reload: still on. OK then reload: toggle off, QR and secret gone; new private session signs in with username and password only | Pass |
| 27 Admin-assisted lost device | Admin removes only that user's OTP; re-enrol; fresh sign-in | Admin Settings > Users > OTP **Remove** (same confirm dialog, does not name the account). Cancel keeps; OK then reload shows `Not configured`; user signs in without a code; user re-enrols with a new secret (differs from the old); fresh sign-in: old device code rejected, new device code accepted; admin row shows `Remove` again | Pass |
| 27 SE05 Password change and relogin | Password changes in the user page; old password rejected | Password section (three fields) on `/#/user`: change from the default to a generated value; `session.signIn` with the old value then returned `invalid credentials`; new value works; browser Sign out then sign in with the new value works. Rapid retries are throttled (`too fast authentication tries` in the xo-server log) | Pass |
| 27 SE05 Account type and least privilege | User cannot administer | `otp-a` (User): `xo.exportConfig`, `user.getAll`, `user.create`, `group.create`, `server.getAll`, `acl.get` each `not enough permissions`; UI `/#/settings/users` and `/#/settings/config` show `Page not found`. Users page lists `admin@admin.net` as Admin and `otp-a` as User | Pass |
| 27 Sole-admin recovery | Documented CLI recovers the only admin; no stop of xo-server | Setup: admin enrolled OTP through the UI; fresh sign-in asked for a code; with the code unavailable the sign-in failed with `Invalid code` and the UI offers no way back. Simulated loss of device and password (secret file shredded, password record dropped). On the appliance as root (`redis` active): `node /opt/xo/packages/xo-server/dist/recover-account-cli.mjs admin@admin.net`, password typed at `Password (leave empty for random):` (echoed as asterisks), output `user admin@admin.net has been successfully updated`, rc 0 in about 4 s. xo-server MainPID unchanged (78672, no restart). Afterwards: old password rejected; new private window signs in with the new password and no code page; Users shows `Admin` and OTP `Not configured`; token created before recovery still valid (as documented); **Forget all authentication tokens** then invalidated it and kept the session; admin re-enrolled OTP on a new secret and a fresh sign-in with a code succeeded | Pass |
| 27 Recovery for a missing account | Creates a new local admin | `recover-account-cli.mjs recover-probe@lab.invalid` with an empty password printed a generated password and `user recover-probe@lab.invalid has been successfully created`; Users lists it as `Admin`, OTP `Not configured`. Probe account deleted afterwards | Pass |

Not covered (rows stay open): LDAP/SAML link removal by the recovery command (no provider configured), FR/JA label review, screen-reader and mobile review, enforced OTP policy, provider bypass.

Observations for the lead:
1. `recover-account-cli.mjs` needs a TTY: with a piped stdin it fails with `tty.setRawMode is not a function` (password prompt uses the `pw` module). Over SSH with a pty it works. The chapter says SSH is fine; a non-interactive SSH command (`ssh host cmd`) fails the same way. The CLI also takes the password as a second argument and has an `-s` mode that creates `xoa-support`; neither is in the chapter. The prompt echoes asterisks, whereas the chapter says "The password is not shown".
2. The enrolment dialog shows `Password is invalid` for a wrong OTP code.
3. The token delete dialog prints the whole token. Forget all authentication tokens has no confirmation.
4. A fresh RPM install (no deployment form) ships `admin@admin.net` with the documented default password active, and Redis `appendonly no`. See the DEFECT line.


Defects observed in this release: fresh RPM default administrator [#368](https://github.com/Vagrantin/xcp-hl/issues/368), recovery CLI non-TTY failure [#369](https://github.com/Vagrantin/xcp-hl/issues/369), and incorrect OTP enrolment error wording [#371](https://github.com/Vagrantin/xcp-hl/issues/371). The Redis persistence configuration was already reported in #311.
