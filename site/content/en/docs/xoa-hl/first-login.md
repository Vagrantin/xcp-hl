---
title: "Sign in, connect a host and choose a language"
linkTitle: "First sign-in"
description: "Sign in to XOA-HL, set your password, choose the interface language and connect your host."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: source
sourceRevision: sha256:db4332ad53583587f2c85f7b871c7ed805fde9d300e42942500e267cbfa98141
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

At the end of this guide, you can sign in to XOA-HL, your host is connected, and the interface uses your language.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261027-ca44911`, package `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Tested on a lab appliance on 2026-10-27. Older images and later updates can differ. Rebuilt on 2026-10-27 with the provisioning fix in `build-xoa-hl@fa0c987`. See [how to identify the fixed asset](/docs/xoa-hl/first-login/#identify-the-rebuilt-image).
{{< /callout >}}

## Before you begin

- [Deploy XOA-HL from XO Lite](/docs/start/#start-deploy-xoa). Note the image tag and the appliance address.
- Keep the XO administrator login and password that you entered in the deployment form. You also need the host management address and the host `root` password.
- Use a browser on a trusted management network.

Most steps run in your **browser**. The image check uses a root shell inside the appliance. Cleanup for older or incomplete deployments uses a root shell on the host.

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
On images built before the 2026-10-27 provisioning fix, a failed first start can leave the web account at `admin@admin.net` with password `admin`. Try it only on a trusted network, then change its password straight away. On the rebuilt image, use your deployment account. If it fails, inspect the provisioning services below. Do not assume that the default account should work.
{{< /callout >}}

## 2. Set a password you will keep

1. Select the **user icon** in the menu to open **User** (`/#/user`).
2. In the password section, enter the current password, then the new password twice. Use a unique password. Select **OK**.
3. Store the new password safely. Sign out, then sign in again with the new password.

**Check:** you can sign in with the new password. This only changes the web account. The host `root` password and the appliance SSH password do not change.

{{< callout type="warning" >}}
These problems affect images built before the 2026-10-27 provisioning fix, including `qa-xoa-build-58.xva` (SHA-256 starting `5f8427fd`). They do not describe a successful deployment of the rebuilt image identified below:

- **Restart the appliance once.** After you change the password, restart the appliance VM normally from XO Lite (**Restart**, not a forced restart). Until the appliance has saved its settings, a power cut or a forced stop can bring back the `admin@admin.net` account with the password `admin`, and your own account is lost. For the same reason, never keep a snapshot of a running appliance as a known good state.
- **Remove the credentials left by the deployment.** The VM settings on the host can retain deployment credentials in clear text. After verifying access, use the cleanup procedure below, then rotate the web password and change the `xo` SSH password with `passwd` if SSH is enabled.
{{< /callout >}}

### Identify the rebuilt image

The fixed asset is `qa-xoa-build-59.xva` in release `xoa-image-20261027-ca44911`. Its SHA-256 is `cc20b9398d5ab0dc03eae6706d3b54236e2d245fa1d0dd1232d59836387057aa`. It was built from `build-xoa-hl@fa0c987`. The earlier asset used the same tag and About version strings.

Inside the appliance, run this read-only check as **root**, from its console or an authorized SSH session:

```bash
redis-cli config get appendonly
```

For the rebuilt image, the result is `appendonly` followed by `yes`. The previous image returns `no`. This checks Redis's current setting. A manually changed or custom image can also return `yes`; keep the original asset name and checksum as the image identity.

The rebuilt image saves the deployment account before it marks setup complete. Later changes use Redis's append-only file (AOF), saved every second. A forced stop can still lose about the last second of changes. Use a normally shut down appliance for a baseline snapshot.

### Clean up older or incomplete deployments

Before removing keys, wait until the appliance has applied the accounts and you can sign in with both the intended web credentials and, if enabled, SSH credentials. Use the exact appliance VM UUID. In a **root shell on the XCP-HL host**, check each key individually without displaying its value:

```bash
for key in admin-account system-account-xoa-password xoa-updater-credentials; do
  if xe vm-param-get uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key" >/dev/null 2>&1; then
    xe vm-param-remove uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key"
  fi
done
```

A missing key is expected; investigate any removal error. Do not dump the whole `xenstore-data` map into a log or report. Old first-boot logs, VM exports and pool metadata backups can still contain the deployment passwords. Rotate the web and SSH passwords that were supplied at deployment and protect or retire those older copies. Removing current keys does not erase historical copies.

Keep the XO Lite deployment tab open until it finishes. On the rebuilt image, guest cleanup also removed `vm-data/admin-account` and `vm-data/system-account-xoa-password` from XAPI’s persistent `xenstore-data` after first boot. This was observed on one XCP-HL v8.3 host in [#311](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771). Do not assume the same result for older images, Vates, Ronivay or custom images, or failed or abandoned deployments. Check and remove remaining keys on the host as above, after the accounts have been applied. The XO Lite cleanup fix in [#310](https://github.com/Vagrantin/xcp-hl/issues/310) also covers other image sources. An application RPM update alone does not replace the provisioning scripts in an older image.

For images rebuilt with the #310/#311 fixes, a failed first-boot capture deliberately prevents networking; XO Lite may report "XOA not responding" without an IP address. From the VM console, inspect `systemctl status xoa-first-boot.service` and `/var/log/xoa-first-boot.log`. These images require a complete administrator email and password from XO Lite; importing the XVA without that data is not silently accepted. Correct the provisioning data before rebooting, and keep the credential keys until capture succeeds. If capture succeeded but credentials were not applied, inspect `systemctl status xoa-credentials.service` and retry that service after correcting the cause. Do not copy the root-only `/etc/xoa-first-boot.env` into reports.

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

Open **About** (`/#/about`) as an administrator. Note the **XOA-HL version** and the **XOA-HL VM version**, and keep them with the original asset name, checksum and image tag. The two 2026-10-27 assets have the same About version strings. Use the image check above to distinguish their default Redis settings. Package updates can change the application version later.

The [release matrix](/docs/reference/release-matrix/) lists what each release shipped. It does not record test results.

## If something goes wrong

| Problem | What to check |
| --- | --- |
| The appliance page does not open | In XO Lite, check that the appliance VM is running. Then check its address, network and gateway, and that your browser can reach it. Do not deploy again over a working VM. |
| The deployment credentials do not work | Wait until the first start has finished and check that you used the web account. On the rebuilt image, inspect the provisioning services described above. On an older image, try the fallback account only on a trusted network. After an early forced stop, an older image may have lost your account: change the fallback password, then create your account again. Read `/var/log/xoa-first-boot.log` from an authorized console or SSH session. Remove private data before sharing it. |
| Signing in to the host fails | Check the host address and its `root` password. The web administrator password is a different password. |
| The server shows a certificate error | Check the host identity before you accept its self-signed certificate. Do not accept a change that you cannot explain. |
| The server is enabled but the inventory is empty | Read the connection error. Check that the appliance can reach the host and that the host address is right. Your browser reaching the host does not prove that the appliance can. |

## Next steps

[Create your first VM](/docs/xoa-hl/create-vm/), or read the [update guide for the appliance and the host](/docs/guides/updates/).

{{< details title="Sources" closed="true" >}}
Checked against: [image release](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261027-ca44911); [credential setup in build-xoa-hl@fa0c987](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-credentials.sh); [user screen in XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [servers screen in the same version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [XOA-HL About page patch in xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
- [build-xoa-hl@fa0c987: AOF](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-finalize-state.sh)
- [#311: 2026-10-27](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771)
{{< /details >}}
