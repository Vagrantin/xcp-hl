---
title: "Install Linux guest tools"
linkTitle: "Guest tools"
description: "Install the management agent in an Ubuntu 24.04 VM and check what XOA-HL reports."
weight: 41
translationKey: xoa-manual-guest-tools
translationStatus: source
sourceRevision: sha256:8c9c47b718efc4436950f5657e77083f7fb3d379db7f776360f830647c2ca1e2
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Install the management agent in a disposable Ubuntu 24.04 VM, check what XOA-HL reports, and test an ordinary guest shutdown. Keep kernel drivers, the agent and application health as separate checks.

{{< callout type="info" >}}
Source-reviewed preview: XOA-HL image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38`, XO 5.113.2 (`e281c536`). The guest package scope is Ubuntu 24.04 LTS (Noble), amd64, `xe-guest-utilities` `7.20.2-0ubuntu1`. Installed guest/host behavior and human language review remain pending. This is not a supported guest OS matrix or a Windows tools recipe.
{{< /callout >}}

## Before you begin

- Use a freshly installed disposable Ubuntu 24.04 amd64 VM, such as the [first-VM exercise](/docs/xoa-hl/create-vm/), with a working console and guest account allowed to use `sudo`. Record its full VM UUID, host, guest OS/kernel and the installed host/appliance versions. A template name alone does not identify the installed OS.
- Use an XOA-HL administrator account for this pilot. Guest package administration is a separate permission; VM start/stop requires **operate** on the VM. A browser login does not grant guest `sudo`.
- Arrange a maintenance window for the shutdown test. Save work and exclude the disposable VM from unattended jobs. Keep valuable data out of it; establish an independent [backup and isolated restore](/docs/xoa-hl/backup-restore/) before applying changes to a valuable guest.
- The guest needs working DNS, time and access to its approved Ubuntu Noble repositories, including `universe`. Use an approved lab network; do not alter host management networking to reach a package mirror. This guide does not add repositories or use a tools ISO.

Run the shell commands below **inside this guest's console**, never on the XCP-HL host or XOA-HL appliance. Management readback and power controls run in the **browser at the appliance address**.

## 1. Record the guest and current tools state {#guest-tools-status}

1. In the browser, select the recorded VM UUID and confirm **Running**. Open **General** (`/#/vms/<vm-uuid>/general`) and record its virtualization label, tools/agent message and reported IP. Open **Advanced → Guest OS** and record **Management agent version**, **OS name** and **OS kernel**. Avoid editing nearby controls.
2. In that VM's console, collect the following. An absent package or inactive service is a finding to record, not a reason to run commands on another machine.

```bash
cat /etc/os-release
uname -r
dpkg --print-architecture
systemd-detect-virt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
systemctl status xe-daemon.service --no-pager
```

**Check:** the OS is Ubuntu `24.04`, architecture `amd64`, and virtualization reports `xen`. If these differ, choose a separately reviewed OS-specific procedure. If tools are already installed, record their package source/version and use the reporting checks below; do not reinstall or upgrade them just to match an example.

The General message is conditional. It is hidden unless the VM is Running and driver-detection information is present. When present, the source checks PV-driver detection first, then agent detection, then the reported up-to-date flag. **No Xen tools detected**, **Management agent not detected**, **Management agent {version} out of date** and **Management agent {version} detected** describe different states. A missing message does not prove that tools are installed, and “detected” is not an application, connectivity or security test.

Linux kernel PV drivers and the userspace agent have different roles. The Ubuntu package below supplies the agent; installing it is not a kernel-driver replacement. XO's displayed agent version comes from host guest-metrics fields and need not equal the Ubuntu package version. Preserve both values; do not downgrade or reinstall based only on their spelling.

At this pin, French uses **Général**, **Avancé → OS invité** and English agent messages/version labels. Its inherited VM Start label is **Créer**. Japanese uses **一般**, **詳細設定**, **仮想マシンの起動 / 仮想マシンの終了**; Guest OS/version field labels can remain English. Read the selected VM and operation as well as its label.

## 2. Install the Ubuntu management agent {#install-linux-agent}

For this step, use a guest without an existing tools installation. If a tools ISO, vendor agent or a different package is already in use, first resolve its ownership and upgrade path separately.

1. Refresh the guest's approved package indexes and inspect the candidate and simulated transaction:

```bash
sudo apt-get update
apt-cache policy xe-guest-utilities
apt-get -s install xe-guest-utilities
```

2. Confirm the candidate comes from the expected Ubuntu Noble repository. The source-reviewed package is `7.20.2-0ubuntu1`; a different version/source requires reassessment before this pilot. Stop for repository/signature errors, no candidate or unexpected removals/upgrades. Do not bypass verification or add an unrelated repository.
3. Install interactively, read the proposed transaction, then start and enable the packaged service:

```bash
sudo apt-get install xe-guest-utilities
sudo systemctl enable --now xe-daemon.service
dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
systemctl is-enabled xe-daemon.service
systemctl is-active xe-daemon.service
```

**Check:** package status is `install ok installed`, the unit is `enabled` and `active`. Noble ships **`xe-daemon.service`**, with a dependency on `proc-xen.mount` and Xen virtualization/path conditions. Do not substitute the generic `xe-linux-distribution.service` name. An exited installer or enabled unit alone does not prove that the agent is running. No reboot or package removal is part of this installation step.

## 3. Verify reporting and a clean shutdown

1. Refresh the same running VM's **General** and **Advanced** pages. Record the tools message, reported agent version, OS and kernel. Compare OS/kernel with the guest console. A persistent absent/outdated message remains unresolved even when `systemctl` says active; keep the exact observations instead of marking the pilot passed.
2. Compare any reported IP with the intended guest interface and its current address. **No IPv4 record** alone is not proof of agent failure: an IPv6-only or disconnected guest may have no IPv4 address. A reported address does not prove routing, DNS or SSH/RDP access. Check required guest connectivity separately.
3. Save all guest work. In the browser, recheck the VM UUID and use its ordinary **Stop** action once, reading the confirmation. If XO proposes force shutdown or bypassing a blocked operation, **cancel**; that is not a successful clean shutdown. Record the error and use the guest's own normal shutdown if it remains responsive. Do not repeat the request while a task is active.
4. Verify the console shuts down and XOA-HL reaches **Halted**, with no active stop task. Start this test VM once, verify console login and application/test-file health, and repeat the service and reporting readback. Keep guest shutdown/boot observations separately from agent detection: neither proves the other.

**Check:** the exact package/service, refreshed guest reporting, ordinary shutdown and subsequent boot/service persistence all have recorded results. If any is missing or fails, keep acceptance pending. This does not establish live migration, dynamic memory, hotplug, quiesced snapshots, clipboard support or performance.

## If something does not work

| Symptom | Check and next action |
| --- | --- |
| Package unavailable or unexpected source | Check guest OS/release, `apt-cache policy`, approved `universe` availability, time/DNS and update errors. Resolve the repository issue with its owner; do not install a host/appliance package in the guest. |
| Unit missing, inactive or failed | Confirm the installed package and its files with `dpkg -L xe-guest-utilities`. Read `systemctl status xe-daemon.service proc-xen.mount --no-pager` and `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager`. Check the Xen conditions and dependency errors before changing configuration. |
| Service active but XO reports missing/outdated data | Recheck VM identity, Running state and the host connection. Compare guest package/service evidence with General/Advanced observations and timestamps. Do not restart the hypervisor, suppress the warning or blindly replace drivers. |
| Stop fails or offers force | Cancel force/bypass, retain the exact task error and check the guest console. Use normal guest shutdown when possible. Forced power-off can lose data and needs a separate decision. |
| Guest fails after a change | Preserve package transaction and boot/service logs. Use the guest console and the separately established recovery plan; this guide does not claim an automatic uninstall/downgrade rollback. |

Do not repeatedly enable/restart/install to conceal an unexplained failure. [Report sanitized evidence](/docs/xoa-hl/troubleshooting/#report-a-problem): versions, VM/host IDs, timestamps, package origin/version, service state, exact UI messages and power-task results. Logs and guest screens may contain private names, addresses or data; keep raw evidence private.

For future updates, use a separately planned guest OS/package maintenance window and repeat the same observations. Other Linux distributions, tools-ISO installation, Windows/BSD tools, vendor switching, upgrades/removal and a supported guest matrix remain separate acceptance work. Continue with [VM operations](/docs/xoa-hl/vm-operations/) and [backup/restore](/docs/xoa-hl/backup-restore/).

## Sources

XO at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`: [General detection ordering](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [Advanced guest OS fields](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [host-metrics mapping](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [stop/force confirmations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js) and [VM operate permission](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs). HomeLab scope: [patch selection at `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).

Guest evidence, reviewed 2026-10-15: Ubuntu Noble [package `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities), [amd64 file list](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist), and [versioned Debian packaging](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`). [XCP-ng guest-tools background](https://docs.xcp-ng.org/vms/#linux-guest-tools) is upstream context; it does not establish installed HomeLab compatibility.

[EN/FR/JA label catalogs at the XO pin](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl) / [HomeLab locale fallback](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/compact-xo-locales.py).
