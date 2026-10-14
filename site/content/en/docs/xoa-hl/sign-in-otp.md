---
title: Protect sign-in with a one-time code (OTP)
description: Enable time-based one-time codes for an XOA-HL account, check sign-in and remove them safely.
weight: 27
translationKey: xoa-manual-sign-in-otp
translationStatus: source
sourceRevision: sha256:b4ebb4c4ebaf22947e783575c878bd2dae49d464c2675e1d6a4c2d619fe34528
glossaryTerms: ["appliance"]
---

XOA-HL can ask for a 6-digit, time-based one-time code (TOTP) from an authenticator app after the password. Each account enables it for itself. Test it first on a non-administrator account you [created for this purpose](/docs/xoa-hl/permissions/).

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. OTP enrollment, sign-in and removal tests on this appliance are pending. Later releases can differ.
{{< /callout >}}

## 1. Prepare

| Requirement | Why |
| --- | --- |
| A TOTP authenticator app on a device you control | It generates the codes from a shared secret |
| Correct time on the appliance and on that device | XO accepts the current code and the codes of the 30-second steps just before and after it |
| A second administrator, or an independent recovery plan | Without one, a lost device can lock the only administrator out |
| A browser session you keep open during the test | It lets you remove OTP if the check fails |

The enrollment check runs in your browser, with the browser's clock. Sign-in is checked by the appliance, with its own clock. A code accepted during enrollment therefore does not prove that the appliance time is correct.

## 2. Enable OTP for your account

1. Sign in as the account to protect. Open your user page with the user icon in the menu (`/#/user`).
2. Switch on the **OTP authentication** toggle. The **Add OTP authentication** dialog shows a QR code and the secret as text.
3. Scan the QR code, or type the secret, in the authenticator app. The entry is issued by `Xen Orchestra` and labelled with the account's name.
4. Type the current code in **OTP code** and confirm. A wrong code reopens the dialog; type the code currently shown by the app. **Cancel** leaves OTP disabled.
5. After success, the user page keeps showing the secret and its QR code next to the toggle. Anyone who sees them can generate valid codes, so do not share or capture this page.

## 3. Check sign-in in a new session

1. Keep the current session open. Open a private browser window and sign in with the username and password.
2. A second page asks for a **Code**. Type the current code from the app and select **Sign in**. This page is in English in every UI language.
3. A wrong or expired code shows `Invalid code`. Wait for the next code and try again.
4. Check that the expected account is signed in, then close the private window.

If the check keeps failing, use the open session to remove OTP (section 5), check both clocks, then enroll again.

## 4. Know what OTP does not cover

- Sessions and authentication tokens that already exist keep working without a code. XO treats them as already authenticated. After enabling OTP, open **Authentication tokens** on your user page and delete tokens you do not recognize or no longer need. A script that uses a deleted token stops working.
- OTP protects XO web sign-in for this account. It does not protect the appliance's SSH or console access, the host's XO Lite or root accounts, or other XO accounts.
- External authentication providers and their own MFA are outside this guide.

## 5. Remove OTP

- **Your own account:** on your user page, switch off **OTP authentication** and confirm **Remove OTP authentication**.
- **Another account, as an administrator:** open **Settings** > **Users**. In the **OTP** column, select **Remove** for that account and confirm. Check the requester's identity first, for example through another channel. The user can then enroll a new device.

Accounts without OTP show **Not configured** in that column. If the only administrator loses the device, the interface offers no recovery. The source contains a recovery command that resets an account's password, removes its OTP and makes it an administrator. It has not been validated on this appliance, so this guide does not provide it as a procedure. Keep a second administrator instead.

## Sources

XO 5 pin `e281c536`, with the released HomeLab patches applied: [user page OTP section](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js), [user page and tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js), [enrollment dialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js), [enable/remove actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [Users settings OTP column](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [sign-in pages](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [sign-in form](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug), [authentication and token bypass](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [TOTP window](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs), [recovery command](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs) and [English labels](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
