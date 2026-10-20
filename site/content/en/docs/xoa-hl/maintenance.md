---
title: "Maintain and update the appliance"
linkTitle: "Appliance maintenance"
description: "Record the installed versions, prepare an update window, update the appliance and check the result."
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: source
sourceRevision: sha256:faec682dbf31ac568cdf40e0b931f9398b8700df7012c927d2894e6c7d80bb3b
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Update the XOA-HL appliance in four steps: record what is installed, prepare a maintenance window, choose how updates run, then check the result. You work in the **browser**, signed in to XOA-HL as an administrator. A few read-only checks run **inside the appliance**, through its console or SSH.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. Later packages can behave differently.
{{< /callout >}}

## 1. Record your starting point {#record-versions}

1. In the browser, open **About** (`/#/about`) as an administrator.
2. Note the **XOA-HL version**, the **XOA-HL VM version**, the appliance address and the original image tag. The VM version identifies the image build. Updating the application does not change it.

If you have authorized console or SSH access, run these read-only commands inside the appliance. Use root privileges where needed.

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

Keep the output with the [release matrix](/docs/reference/release-matrix/) and the [release notes](/docs/reference/changelog/). The matrix lists the components that shipped together; it does not prove that they were tested together.

## 2. Prepare the update window {#prepare-window}

- [Export the XO configuration](/docs/xoa-hl/configuration-backup/). Keep the file and its passphrase outside the appliance.
- Separately record any changes you made to `/root/.config/xo-server/config.toml`, the TLS files and `/etc/xoa-hl/update.conf`. The web export does not include these files.
- Check that you can open the appliance console through XO Lite, in case the web interface is unavailable.
- Check that backups, restores and other management tasks have finished.
- Plan a window long enough for a service restart and, if needed, a later appliance reboot.

This page updates the XOA-HL VM only. Updating hosts is a separate task: see the [update guide](/docs/guides/updates/) for the right target and commands.

## 3. Choose the mode and channel {#update-mode-channel}

Open **Settings → XOA-HL Updates** (`/#/settings/xoa-hl-updates`). To update by hand, follow the [update procedure](/docs/guides/updates/) for **Check for update** and **Update now**.

Choose a **Mode**:

| Mode | What you do |
| --- | --- |
| Manual only | You start each check and each installation. This is the default |
| Check automatically | Checks run on a schedule. You decide when to install |
| Install automatically | Installation runs on a schedule. Use it only after you have explicitly approved installation in your maintenance window |

For a scheduled mode:

1. Check the **Appliance timezone**. The schedule uses it, not the host's or the browser's timezone. Compare it with the `timedatectl` output.
2. Set the **Frequency**, the **Day** for a weekly schedule, the **Local start time** and the **Random delay**. The random delay is added after the start time.
3. Select **Save automatic update settings**.
4. Check the saved settings, and the timer list from `systemctl list-timers 'xoa-hl-*'`.

In **Update channel**, keep **Stable** for routine maintenance. **Testing** adds candidate packages: use it only on a disposable test appliance. Changing the channel does not install anything, and does not downgrade a candidate package that is already installed.

The managed update runs a full `dnf` update, except for `nodejs`. Installing the application package restarts `xo-server` after the transaction, so the web page can disconnect. That alone does not mean that the update failed.

## 4. Check the result {#check-result}

1. Reconnect to the web interface and open **About**. Check that it shows the expected application version.
2. Check that the expected hosts are connected and that their inventory appears.
3. Read the update result.

If the result is unclear, run these read-only checks inside the appliance:

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| File or value | What it tells you |
| --- | --- |
| `/run/xoa-hl/status` | The latest check: `UP_TO_DATE`, `AVAILABLE` or `ERROR`. Lost when the appliance restarts |
| `/var/lib/xoa-hl/update.log` | The output of the managed installation, ending with a success or failure marker. Overwritten by the next attempt |
| `/var/lib/xoa-hl/auto-update.status` | Automatic runs only. Compare `startedAt` and `finishedAt` (UTC) with the time of your update |
| `result=check_failed` or `result=failed` | The check or the installation failed: read its log. Neither means success |
| `rebootNeeded=yes`, `no` or `unknown` | The automatic run's assessment. `unknown` does not mean that no reboot is needed |

A manual installation does **not** update the automatic-run record. A check service can exit successfully and still report a problem, so read its result. Save the relevant logs before you try again.

**Check:** **About** shows the expected version, the expected hosts are connected, and the update result reports success.

## If the update does not finish cleanly {#update-problems}

There is **no automatic reboot**. The managed check and installer share a lock, but a `dnf` command that you start from a shell is outside that lock. While an update might be running, never start another `dnf` process, stop a running transaction or reboot to free a busy updater.

| Problem | What to check |
| --- | --- |
| Only the browser disconnected | Installing the application restarts `xo-server`. Check the service and the log through the console before you retry. |
| The updater seems busy | Check the service and the log through the console. Do not start another `dnf`, stop the transaction or reboot to free it. |
| An automatic installation window was missed | The missed installation does not run immediately when the appliance starts again. Plan another window. |
| The appliance boot was interrupted, or the result is unclear | Save the logs, then use the [troubleshooting guide](/docs/xoa-hl/troubleshooting/) before you plan another update. |
| The installed changes might need a reboot | Reboot only once no transaction or management job is running, and you have decided that the changes need it. Then check sign-in, versions and inventory again. |
| You want to go back to the earlier version | A package downgrade is not a tested recovery procedure. It does not restore the base OS, XO data or your own files. Read the [recovery limits](/docs/xoa-hl/configuration-backup/#recovery-limits) first. |

{{< details title="Sources" closed="true" >}}
- **Appliance updater**: [scheduling](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [installer](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-update.sh), [automatic-run status](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-auto-update.sh), [check result](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [package spec](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [channel patch](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzz-xoa-hl-update-channel.patch).
{{< /details >}}
