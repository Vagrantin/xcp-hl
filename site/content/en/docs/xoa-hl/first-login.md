---
title: Log in, connect a host and choose your language
description: Set up your XOA-HL account, connect the hypervisor and choose the interface language.
weight: 10
translationKey: xoa-manual-first-login
translationStatus: source
sourceRevision: sha256:0510b44d9ff31a46a35760be93a081503f05a2ab39b34882e6165c4c94744389
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

Finish this guide with an XOA-HL account you can log in to, a connected host and an interface in your chosen language.

{{< callout type="info" >}}
Preview procedure: checked against the source for image `xoa-image-20261009-5f33c81` and XO 5.113.2. A complete run on a disposable appliance is still pending. Older images or later package updates can differ.
{{< /callout >}}

## Before you begin

- [Deploy XOA-HL through XO Lite](/docs/start/#start-deploy-xoa). Record the image tag and the appliance address.
- Keep the XO administrator login and password entered in the deployment form. You also need the host management address and its `root` password.
- Use a browser on a trusted management network. This tutorial uses an XOA-HL administrator account; delegated access is outside its scope.

All steps below run in the **browser**. No host or appliance shell commands are required.

| Address or account | Use |
| --- | --- |
| Host management address | XO Lite and the server connection in XOA-HL |
| XOA-HL appliance address | Xen Orchestra web interface |
| XO administrator account | Log in to Xen Orchestra |
| Host `root` account | Allow Xen Orchestra to manage the hypervisor |
| Appliance system account `xo` | SSH access; separate from the web account |

## 1. Open the appliance and log in

1. Open `https://<appliance-address>`, replacing the placeholder with the address assigned during deployment. Use the appliance address, not the host address.
2. If the browser reports a self-signed certificate, verify the address belongs to your appliance before accepting it. A changed certificate on an existing installation needs investigation.
3. Wait for first-boot provisioning to finish, then sign in with the **XO administrator credentials from the deployment form**. Do not use the host's `root` account or the appliance's SSH account.

**Check:** the login screen is replaced by the Xen Orchestra interface. An empty inventory is normal before you connect a host.

{{< callout type="warning" >}}
For this image, unsuccessful credential provisioning can leave the bootstrap web account `admin@admin.net` with password `admin`. If the configured account fails on a fresh appliance, try this fallback only on your trusted management network. If it works, change its password immediately in the next step. If neither account works, stop repeated attempts and check the first-boot troubleshooting notes below.
{{< /callout >}}

## 2. Set a password you will keep

1. Select the **user icon** in the navigation to open **User** (`/#/user`).
2. In the password section, enter the current password, a new unique password and its confirmation. Select **OK**.
3. Store the new password, sign out, and confirm you can sign in again with the same web login and the new password.

**Check:** a new login succeeds. This changes the web-account password; it does not change the host `root` password or the appliance's SSH password.

## 3. Choose the interface language

1. Open the **user icon → User → Language**.
2. Select **English**, **Français** or **日本語**. Confirm the interface labels change.

The documentation language selector changes this website independently. Switching one does not switch the other. Some appliance labels may still use English; the route `/#/user` identifies the same screen in every language.

## 4. Connect the host

1. Open **Settings → Servers** (`/#/settings/servers`). If the intended server is already listed and connected, check its inventory instead of adding it twice.
2. In the connection form, enter a descriptive label, the **host management IP address or hostname**, username `root` and the host password set during installation. Do not enter the appliance address.
3. Select **Connect**. If the connection reports a self-signed certificate, first verify the host identity, then accept the certificate exception for that server if appropriate.
4. Check the connection row for an error indicator. Open the inventory and confirm the intended pool, host and storage repositories appear. **Enabled** alone means the connection is enabled; it does not prove it succeeded.

**Check:** the intended host and its storage appear without a connection error. You can now [create your first VM](/docs/xoa-hl/create-vm/).

## 5. Record the installed versions

Open **About** (`/#/about`) as an administrator and record **XOA-HL version** and **XOA-HL VM version**. Keep these with the deployed image tag. The VM version records the image build; package updates can change the application version later.

See the [release matrix](/docs/reference/release-matrix/) for recorded releases. It lists shipped components, not appliance test results.

## If something does not work

| Symptom | Check and next action |
| --- | --- |
| Appliance page does not open | Confirm the appliance VM is running in XO Lite, then check its assigned address, network, gateway and browser connectivity. Do not redeploy over a working VM. |
| Deployment credentials fail | Wait for first boot, verify you used the web credentials, then check the fallback described above. If access is available through the appliance console or an authorized SSH account, inspect `/var/log/xoa-first-boot.log`; do not share it without removing private data. |
| Host authentication fails | Verify the host address and its `root` password. The web administrator password is a different credential. |
| Server shows a certificate error | Verify the host identity before allowing its self-signed certificate; do not accept an unexplained change. |
| Server is enabled but inventory is empty | Read the connection error, check appliance-to-host connectivity and verify the host's management address. Browser-to-host access alone does not prove appliance-to-host access. |

## Next step and sources

[Create and install your first VM](/docs/xoa-hl/create-vm/), or read the [appliance and host update guide](/docs/guides/updates/).

Source review: [image release](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261009-5f33c81); [credential provisioning at build-xoa-hl@2103968](https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-credentials.sh); [user screen at XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [server screen at the same pin](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [XOA-HL About patch at xoa-hl@5f33c81](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
