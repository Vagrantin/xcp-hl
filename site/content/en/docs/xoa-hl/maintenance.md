---
title: "Maintain and update the appliance"
linkTitle: "Appliance maintenance"
description: "Record versions, plan an update window and check the result."
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: source
sourceRevision: sha256:932a5f12913363b83e6146fc55c12988da0d9d6c7e314afb19653f8b4996cea1
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Plan an appliance update with a configuration export, console access and a way to check the result after the web interface reconnects.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Interruption and reboot tests on a disposable appliance are pending. Later packages can differ.
{{< /callout >}}

## 1. Record your starting point

In the **browser**, open **About** (`/#/about`) as an administrator. Record **XOA-HL version**, **XOA-HL VM version**, the appliance address and the original image tag. The VM version identifies the image build; updating the application does not replace that image identity.

If authorized console or SSH access is available, run these read-only commands **inside the appliance**, with root privileges where required:

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

Keep the output with the [release matrix](/docs/reference/release-matrix/) and [release notes](/docs/reference/changelog/). The matrix records shipped components, not tested compatibility.

## 2. Prepare the window

- [Export the XO configuration](/docs/xoa-hl/configuration-backup/) and keep the file and passphrase outside the appliance.
- Record any operator changes to `/root/.config/xo-server/config.toml`, TLS material and `/etc/xoa-hl/update.conf` separately. The web export does not include these files.
- Confirm you can reach the appliance console through XO Lite if the web interface is unavailable.
- Check that backup, restore and other management tasks have finished. Arrange a window that allows a service restart and, if needed, a later appliance reboot.

The appliance updater operates inside the XOA-HL VM. Host updates are a separate operation: use the [existing update guide](/docs/guides/updates/) for the correct target and commands.

## 3. Choose the mode and channel

Open **Settings → XOA-HL Updates** (`/#/settings/xoa-hl-updates`). Use the [canonical update procedure](/docs/guides/updates/) for **Check for update** and **Update now**.

| Mode | What you arrange |
| --- | --- |
| Manual only | Start each check and installation yourself; the initial default |
| Check automatically | Scheduled checks; decide when to install manually |
| Install automatically | Explicitly approve scheduled installation in your maintenance window |

The schedule uses the **appliance timezone**, with the selected random delay after the start time. Check the displayed timezone against `timedatectl`; a host or browser timezone is not the schedule reference. Save the frequency, weekly day when applicable, time and delay, then confirm the saved settings and timer listing.

Keep the **stable** channel for routine maintenance. **Testing** adds candidate packages and belongs on a disposable test appliance. Changing the channel does not itself install packages or downgrade an already installed candidate.

The managed update runs a full `dnf` update with `nodejs` excluded. Application package installation restarts `xo-server` after the transaction, so a disconnected web page alone is not evidence of failure.

## 4. Verify the result

Reconnect to the web interface, open **About**, and check the expected application version. Confirm the intended host inventory is connected and read the update result. If the result is unclear, use these read-only appliance checks:

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| Evidence | Interpretation |
| --- | --- |
| `/run/xoa-hl/status` | Latest check: `UP_TO_DATE`, `AVAILABLE` or `ERROR`; transient across reboot |
| `/var/lib/xoa-hl/update.log` | Managed installation output and final success/failure marker; overwritten on another attempt |
| `/var/lib/xoa-hl/auto-update.status` | Automatic run only; compare `startedAt` and `finishedAt` (UTC) with your operation |
| `result=check_failed` or `result=failed` | Investigate the check or installation log; neither is success |
| `rebootNeeded=yes`, `no` or `unknown` | Automatic-run assessment; `unknown` is not confirmation that no reboot is needed |

A manual installation does **not** refresh the automatic-run record. A successful service exit for a check does not replace reading its verdict. Save relevant logs before another attempt.

## 5. Handle disconnection or a missed window

If only the browser disconnected, inspect the service and log through the console before retrying. Do not start another `dnf` process, stop a running transaction or reboot to clear a busy updater. The managed check and installer share a lock; an unmanaged shell transaction is outside that coordination.

There is **no automatic reboot**. A missed automatic installation window is not replayed immediately on boot. After an interrupted appliance boot or an inconclusive result, preserve logs and [use the troubleshooting guide](/docs/xoa-hl/troubleshooting/) before arranging another update. Reboot only after confirming no transaction or management job is active and deciding that the installed changes require it; then recheck login, versions and inventory.

A package downgrade is not a verified appliance recovery procedure. It does not restore the base OS, XO data or operator files. Read [configuration and recovery limits](/docs/xoa-hl/configuration-backup/) before planning a rollback.

## Sources

Reviewed sources at `xoa-hl@5f33c81`: [scheduling](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [installer](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-update.sh), [automatic status](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-auto-update.sh), [check verdict](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [package lifecycle](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec) and [channel patch](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzz-xoa-hl-update-channel.patch).
