---
title: "Install Linux guest tools"
linkTitle: "Guest tools"
description: "Install the management agent inside a Linux guest VM and check what XOA-HL reports."
weight: 41
translationKey: xoa-manual-guest-tools
translationStatus: source
sourceRevision: sha256:b33c81ebb5d81c67bc786f64145b80c80a063e3836134f53b46590995ecf327e
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Install the management agent inside a Linux guest VM, check what XOA-HL reports about it, and test a clean shutdown. The agent runs in the guest, not in XOA-HL. The steps use an Ubuntu 24.04 guest as the example because its package was checked; other Linux distributions provide the agent through their own packages. You use the **XOA-HL appliance** in your browser, signed in as an administrator, and run commands in the guest's console. Work through the sections in order. Other systems, including Windows, need their own procedure.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. Guest package: `xe-guest-utilities` `7.20.2-0ubuntu1` for Ubuntu 24.04 LTS (Noble), amd64.
{{< /callout >}}

## Before you begin

- Use a newly installed Ubuntu 24.04 amd64 test VM with no valuable data, for example the one from [Create your first VM](/docs/xoa-hl/create-vm/). You need a working console and a guest account that can use `sudo`.
- Note the full VM UUID, its host, the guest OS and kernel, and the installed host and appliance versions. A template name alone does not tell you which OS is installed.
- Use an XOA-HL administrator account. Starting and stopping a VM needs the **operate** permission on it. Managing packages in the guest is a separate right: signing in to XOA-HL does not give you `sudo` in the guest.
- Plan a maintenance window for the shutdown test. Save your work in the guest, and take the VM out of scheduled jobs. Before you change a guest that matters, make an independent [backup and test an isolated restore](/docs/xoa-hl/backup-restore/).
- The guest needs working DNS, the correct time, and access to its approved Ubuntu Noble repositories, including `universe`. Use an approved lab network. Do not change the host management network to reach a package mirror. This guide does not add repositories or use a tools ISO.

Run the shell commands on this page **in the guest's console** only, never on the XCP-HL host or the XOA-HL appliance. Read the VM's status and use its power buttons in your **browser**, at the appliance address.

## Check the guest tools status {#guest-tools-status}

1. In the browser, open the VM with the UUID you noted, and check that it is **Running**.
2. Open **General** (`/#/vms/<id>/general`). Note the virtualization mode, the tools message and the IP address shown.
3. Open **Advanced** and find **Guest OS**. Note **Management agent version**, **OS name** and **OS kernel**. Do not change anything on these tabs.
4. In the VM's console, run these commands and note the output:

   ```bash
   cat /etc/os-release
   uname -r
   dpkg --print-architecture
   systemd-detect-virt
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl status xe-daemon.service --no-pager
   ```

   A missing package or an inactive service is a result to note. It is not a reason to run the commands on another machine.

**Check:** the OS is Ubuntu `24.04`, the architecture is `amd64`, and `systemd-detect-virt` prints `xen`. If not, stop and use a procedure written for that system. If the tools are already installed, note where the package comes from and its version, then go to [Check what XOA-HL reports](#check-reporting). Do not reinstall or upgrade them just to match this example.

### What the tools message means

The message on **General** appears only when the VM is **Running** and XO has driver information. XO checks the PV drivers first, then the management agent, then whether the agent is up to date. It shows the first message that applies:

| Message | What it means |
| --- | --- |
| **No Xen tools detected** | The PV drivers are not detected |
| **Management agent not detected** | The drivers are detected, but not the agent |
| **Management agent {version} out of date** | The agent is detected, but reported as out of date |
| **Management agent {version} detected** | The agent is detected and reported as up to date |

No message does not prove that the tools are installed. A detected agent does not test your applications, connectivity or security.

The PV drivers in the Linux kernel and the management agent (a program in the guest) do different jobs. The Ubuntu package below installs the agent; it does not replace kernel drivers. The agent version in XO comes from the host's guest metrics and can differ from the Ubuntu package version. Note both. Do not downgrade or reinstall only because they are written differently. Check the drivers, the agent and your applications separately.

## Install the management agent in a Linux guest {#install-linux-agent}

Use a guest that has no tools installed yet. If a tools ISO, a vendor agent or another package is already in use, first find out who maintains it and how it is upgraded.

1. In the guest's console, refresh the package lists, check where the package would come from, and simulate the installation:

   ```bash
   sudo apt-get update
   apt-cache policy xe-guest-utilities
   apt-get -s install xe-guest-utilities
   ```

2. Check that the candidate comes from the expected Ubuntu Noble repository. This guide was checked against version `7.20.2-0ubuntu1`. Review any other version or source before you continue.
3. Stop if you see a repository or signature error, no candidate, or unexpected removals or upgrades. Do not bypass verification or add an unrelated repository.
4. Install the package. Read the proposed changes before you accept them:

   ```bash
   sudo apt-get install xe-guest-utilities
   ```

5. Enable and start the service, then check the package and the service:

   ```bash
   sudo systemctl enable --now xe-daemon.service
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl is-enabled xe-daemon.service
   systemctl is-active xe-daemon.service
   ```

**Check:** the package status is `install ok installed`, and the service is `enabled` and `active`. On Ubuntu Noble the service is **`xe-daemon.service`**. It depends on `proc-xen.mount`, and systemd starts it only when its Xen virtualization and path conditions are met. Do not use the generic name `xe-linux-distribution.service` instead. A finished installer or an enabled service alone does not prove that the agent is running. This step needs no restart and removes no package.

## Check what XOA-HL reports {#check-reporting}

1. In the browser, refresh **General** and **Advanced** for the same running VM. Note the tools message, the agent version, the OS and the kernel.
2. Compare the OS and the kernel with what the guest console shows.
3. Compare the IP address shown with the guest's intended interface and its current address.

If the message still says that the agent is missing or out of date while `systemctl` says `active`, the problem is not solved. Note exactly what you see, and do not mark the test as passed.

**No IPv4 record** alone does not prove that the agent failed: a guest with only IPv6, or with no network, may have no IPv4 address. A displayed address does not prove routing, DNS, or SSH or RDP access. Check the connections that the guest needs separately.

## Test a clean shutdown {#clean-shutdown}

1. Save all work in the guest.
2. In the browser, check the VM UUID again. Select **Stop** once and read the confirmation.
3. If XO offers to force the shutdown or to bypass a blocked operation, cancel: that is not a clean shutdown. Note the error. If the guest still responds, shut it down normally from inside the guest. Do not repeat the request while a task is running.
4. Check in the console that the guest shuts down, and that XOA-HL shows **Halted** with no stop task still running.
5. Select **Start** once. Sign in through the console and check your application or test file.
6. Repeat the service checks (`systemctl is-enabled` and `systemctl is-active`) and [Check what XOA-HL reports](#check-reporting).

Note the shutdown and start results separately from the agent detection: one does not prove the other.

**Check:** you have a result for each item: the exact package and service, the refreshed report in XOA-HL, the clean shutdown, and the service after the restart. If any result is missing or failed, the test is not complete. This does not test live migration, dynamic memory, hot-plug, quiesced snapshots, the clipboard or performance.

## If something goes wrong

| Problem | What to check |
| --- | --- |
| The package is missing or comes from an unexpected source | Check the guest OS and release, `apt-cache policy`, that the approved `universe` repository is available, the time and DNS, and the update errors. Fix the repository with its owner. Do not install a host or appliance package in the guest. |
| The service is missing, inactive or failed | Check the installed package and its files with `dpkg -L xe-guest-utilities`. Read `systemctl status xe-daemon.service proc-xen.mount --no-pager` and `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager`. Check the Xen conditions and dependency errors before you change any configuration. |
| The service is active, but XO shows the agent as missing or out of date | Check the VM identity, that it is **Running**, and the host connection. Compare the guest's package and service results with **General** and **Advanced**, and the time of each. Do not restart the hypervisor, hide the warning or replace drivers blindly. |
| **Stop** fails or offers to force | Cancel the force or bypass. Keep the exact task error and check the guest console. Shut down from inside the guest if you can. A forced power-off can lose data and needs a separate decision. |
| The guest fails after a change | Keep the package history and the boot and service logs. Use the guest console and your separate recovery plan. This guide does not promise an automatic rollback by uninstalling or downgrading. |

Do not keep enabling, restarting or reinstalling to hide an unexplained failure. [Report the problem](/docs/xoa-hl/troubleshooting/#report-a-problem) with the versions, the VM and host IDs, the times, the package source and version, the service state, the exact messages and the power task results. Logs and guest screens can contain private names, addresses or data: leave them out of the report, and keep the raw evidence private.

For later updates, plan a separate maintenance window for the guest OS and packages, and repeat the same checks. Not covered here: other Linux distributions, installing from a tools ISO, Windows or BSD tools, switching vendors, upgrading or removing the package, and a list of supported guests. Next, see [Manage VMs](/docs/xoa-hl/vm-operations/) and [Back up and restore a VM](/docs/xoa-hl/backup-restore/).

{{< details title="Sources" closed="true" >}}
- **Tools status and power actions**: [order of the tools messages](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [guest OS fields](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [guest metrics mapping](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [stop and force confirmations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM operate permission](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **HomeLab build**: [patch selection in xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Ubuntu package (checked on 2026-10-15)**: [package `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities), [amd64 file list](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist), [Debian packaging](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`).
- **Background**: [XCP-ng Linux guest tools](https://docs.xcp-ng.org/vms/#linux-guest-tools) (general information, not a compatibility statement for XCP-HL).
- **UI labels**: [XO label catalogs](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl), [HomeLab translation fallback](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/compact-xo-locales.py).
{{< /details >}}
