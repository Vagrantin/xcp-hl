---
title: "Sign in, connect a host and choose a language"
linkTitle: "First sign-in"
description: "Sign in to XOA-HL, set your password, choose the interface language and connect your host."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: source
sourceRevision: sha256:f909b407ee7a8b169888613692858f8a5b922b227cc4eeac52c16e5160fbb160
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

At the end of this guide, you can sign in to XOA-HL, your host is connected, and the interface uses your language.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261027-ca44911`, package `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Tested on a lab appliance on 2026-10-27. Older images and later updates can differ.
{{< /callout >}}

## Before you begin

- [Deploy XOA-HL from XO Lite](/docs/start/#start-deploy-xoa). Note the image tag and the appliance address.
- Keep the XO administrator login and password that you entered in the deployment form. You also need the host management address and the host `root` password.
- Use a browser on a trusted management network.

Every step runs in your **browser**. You do not need a shell on the host or the appliance.

| Address or account | What it is for |
| --- | --- |
| Host management address | XO Lite, and the server connection in XOA-HL |
| XOA-HL appliance address | The Xen Orchestra web interface |
| XO administrator account | Signing in to Xen Orchestra |
| Host `root` account | Letting Xen Orchestra manage the host |
| Appliance system account `xo` | SSH access only; it is not the web account |

## 1. Open the appliance and sign in

1. Open `https://<appliance-address>`. Use the appliance address, not the host address.
2. If the browser warns about a self-signed certificate, check that the address is your appliance before you accept it. If the certificate of an existing installation changes, find out why first.
3. Wait until the first start has finished. Then sign in with the **XO administrator account from the deployment form**. Do not use the host `root` account or the appliance SSH account.

**Check:** the Xen Orchestra interface opens. An empty inventory is normal until you connect a host.

{{< callout type="warning" >}}
On this image, if the first start fails to set your credentials, the web account can stay at `admin@admin.net` with the password `admin`. If your own account does not work on a new appliance, try this fallback account, only on your trusted network. If it works, change the password straight away in step 2. If neither account works, stop retrying and use the troubleshooting table at the end of this page.
{{< /callout >}}

## 2. Set a password you will keep

1. Select the **user icon** in the menu to open **User** (`/#/user`).
2. In the password section, enter the current password, then the new password twice. Use a unique password. Select **OK**.
3. Store the new password safely. Sign out, then sign in again with the new password.

**Check:** you can sign in with the new password. This only changes the web account. The host `root` password and the appliance SSH password do not change.

{{< callout type="warning" >}}
Two known problems with this image, until a fixed image is released:

- **Restart the appliance once.** After you change the password, restart the appliance VM normally from XO Lite (**Restart**, not a forced restart). Until the appliance has saved its settings, a power cut or a forced stop can bring back the `admin@admin.net` account with the password `admin`, and your own account is lost. For the same reason, never keep a snapshot of a running appliance as a known good state.
- **Remove the SSH password left by the deployment.** The deployment keeps the SSH password of the `xo` account, in clear text, in the VM settings on the host. If you have a root shell on the host, remove it, then change the `xo` password with `passwd` in an SSH session:

  ```bash
  xe vm-param-remove uuid=<appliance-vm-uuid> param-name=xenstore-data param-key=vm-data/system-account-xoa-password
  ```
{{< /callout >}}

## 3. Choose the interface language

1. Open the **user icon → User → Language**.
2. Select your language. The labels change straight away.

This setting only changes the XOA-HL interface. The documentation has its own language selector at the top of this page. Some appliance labels may not be translated yet. The address `/#/user` always opens this screen.

## 4. Connect the host

1. Open **Settings → Servers** (`/#/settings/servers`). If your host is already listed and connected, check its inventory instead of adding it again.
2. In the form, enter a clear label, the **host management IP address or host name**, the user `root` and the host password set during installation. Do not enter the appliance address.
3. Select **Connect**. If a self-signed certificate warning appears, first check that it really is your host. Then accept the certificate for this server.
4. Check the server row for an error indicator. Then open the inventory and check that your pool, host and storage repositories (SRs) appear. **Enabled** only means that the connection is switched on. It does not mean that it works.

**Check:** your host and its storage appear, with no connection error. You can now [create your first VM](/docs/xoa-hl/create-vm/).

## 5. Note the installed versions

Open **About** (`/#/about`) as an administrator. Note the **XOA-HL version** and the **XOA-HL VM version**, and keep them with the image tag. The VM version identifies the image build. Package updates can change the application version later.

The [release matrix](/docs/reference/release-matrix/) lists what each release shipped. It does not record test results.

## If something goes wrong

| Problem | What to check |
| --- | --- |
| The appliance page does not open | In XO Lite, check that the appliance VM is running. Then check its address, network and gateway, and that your browser can reach it. Do not deploy again over a working VM. |
| The deployment credentials do not work | Wait until the first start has finished, and check that you used the web account. Then try the fallback account above. After a power cut or a forced stop soon after the deployment, only the fallback account may work: change its password, then create your own account again. If you can open the appliance console or an SSH session, read `/var/log/xoa-first-boot.log`. Remove private data before you share it. |
| Signing in to the host fails | Check the host address and its `root` password. The web administrator password is a different password. |
| The server shows a certificate error | Check the host identity before you accept its self-signed certificate. Do not accept a change that you cannot explain. |
| The server is enabled but the inventory is empty | Read the connection error. Check that the appliance can reach the host and that the host address is right. Your browser reaching the host does not prove that the appliance can. |

## Next steps

[Create your first VM](/docs/xoa-hl/create-vm/), or read the [update guide for the appliance and the host](/docs/guides/updates/).

{{< details title="Sources" closed="true" >}}
Checked against: [image release](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261022-a280852); [credential setup in build-xoa-hl@fc7ebfa](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh); [user screen in XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [servers screen in the same version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [XOA-HL About page patch in xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
{{< /details >}}
