---
title: "Protect sign-in with a one-time code"
linkTitle: "One-time codes (OTP)"
description: "Add a one-time code to an account’s sign-in, check it and remove it safely."
weight: 71
translationKey: xoa-manual-sign-in-otp
translationStatus: source
sourceRevision: sha256:3ac13b9cf4aac371686aaef7a2d47b123319efb2aa35724b44115380a0c8e448
glossaryTerms: ["appliance"]
---

XOA-HL can ask for a 6-digit one-time code from an authenticator app after the password. The code changes with time (TOTP). Each account that signs in with a local password turns it on for itself. Try it first on a non-administrator account [created for this test](/docs/xoa-hl/permissions/).

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. Later releases can differ.
{{< /callout >}}

## Before you begin {#prepare}

| You need | Why |
| --- | --- |
| A TOTP authenticator app on a device you control | It generates the codes from a shared secret |
| The correct time on the appliance and on that device | XO accepts the current code and the codes of the 30-second steps just before and after it |
| A second administrator, or a separate recovery plan | Without one, a lost device can lock out the only administrator |
| A browser session that you keep open during the test | It lets you remove the one-time code if the check fails |

Your browser checks the code you type during setup, using its own clock. At sign-in, the appliance checks the code with its clock. So a code accepted during setup does not prove that the appliance's time is correct.

## Turn on a one-time code for your account {#enable-otp}

1. Sign in as the account to protect. Open your user page with the user icon in the menu (`/#/user`).
2. Find the **OTP authentication** switch and turn it on. The **Add OTP authentication** dialog shows a QR code and the secret as text.
3. Scan the QR code, or type the secret, in your authenticator app. The new entry is issued by `Xen Orchestra` and named after the account's email or login.
4. Type the current code in **OTP code** and confirm. If the code is wrong, the dialog opens again: type the code that the app shows now. **Cancel** leaves the one-time code off.

If the switch is missing, stop and note the installed version. This build uses XO's default open-source plan, which shows the switch, so a missing subscription is not the cause. [Report the difference](/docs/xoa-hl/troubleshooting/).

**Check:** the switch is on, and your user page shows the secret and its QR code next to it. Anyone who sees them can generate valid codes: do not share this page or take screenshots of it. This QR code names the issuer `XenOrchestra` (no space) for the same secret. Keep the entry you already have in your app; do not scan it again.

## Check sign-in in a new session {#check-sign-in}

1. Keep your current session open. Open a private browser window and sign in with your username and password.
2. A second page asks for a **Code**. Type the current code from the app and select **Sign in**.
3. A wrong or expired code shows `Invalid code`. Wait for the next code and try again.
4. Check that you are signed in to the right account, then close the private window.

**Check:** the sign-in asked for a code and accepted the right one. If it keeps failing, use the open session to [remove the one-time code](#remove-otp), check both clocks, then turn it on again.

## What a one-time code does not protect {#otp-limits}

- Turning it on does not end existing sessions or revoke tokens. Every valid authentication token skips the code check, including tokens created later: tokens are separate credentials. After you turn it on, open **Authentication tokens** on your user page and delete the tokens you do not recognize or no longer need. A script that uses a deleted token stops working.
- It protects XO web sign-in for this account only. It does not protect SSH or console access to the appliance, XO Lite or the root account on the host, or other XO accounts.
- External sign-in providers and their own multi-factor authentication are not covered here.

## Remove a one-time code {#remove-otp}

- **Your own account:** on your user page, turn off **OTP authentication** and confirm **Remove OTP authentication**.
- **Another account, as an administrator:** open **Settings → Users**. In the **OTP** column, select **Remove** for that account and confirm. First check who is asking, for example through another channel. The user can then set up a new device.

Accounts without a one-time code show **Not configured** in that column. If the only administrator loses the device, the interface offers no way back in. XO includes a recovery command that resets an account's password, removes its one-time code and makes it an administrator, but it has not been tested on this appliance, so it is not given here as a procedure. Keep a second administrator instead.

**Check:** the switch is off and the account's OTP column shows **Not configured**. In a new private window, the account signs in with its local username and password and no code. Keep the recovery administrator signed in until you have confirmed this.

{{< details title="Sources" closed="true" >}}
- **User page and setup**: [user page OTP section](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js), [user page and tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js), [setup dialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js), [turn on and remove actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [OTP column in Users settings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js).
- **Sign-in and tokens**: [sign-in pages](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [sign-in form](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug), [authentication and token bypass](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [TOTP time window](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs), [recovery command](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [UI labels](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Build and browser setup**: [XO default plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [browser authenticator](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js), [user preferences API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs), [HomeLab build](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
{{< /details >}}
