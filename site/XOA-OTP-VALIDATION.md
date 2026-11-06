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
