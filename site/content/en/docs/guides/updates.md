---
title: Updates
weight: 3
translationKey: updates
aliases: ["/updates.html"]
---

XCP-hl and XOA-hl both update in place from signed packages, without reinstalling for routine package updates. The host (XCP-hl) updates from Xen
Orchestra's **Patches** tab, the same way stock XCP-ng does. The appliance
(XOA-hl) updates from its own **XOA-HL Updates** settings page.
{class="lead"}

The package repositories use `rpm.xcp-hl.org` after the move tracked in [#190](https://github.com/Vagrantin/xcp-hl/issues/190). An update of `xcp-hl-release` or `xoa-hl` carries the new repository addresses. The old addresses are retained during the transition. The bootstrap commands below use the new address.

Both halves of this page follow the same outline: the steps in Xen
Orchestra, the command-line equivalent, how it works underneath, and how
to roll back.

## Updating XCP-hl (the hypervisor host) {#updating-xcp-hl-the-host}

{{< callout type="info" >}}
**Applies to** XOA-HL image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; installing host packages and rebooting have not yet been tested on a lab system with this version.
{{< /callout >}}

### In Xen Orchestra

1. **See that updates are waiting.** In `Home > Hosts`, a host with
   pending updates shows a red badge with the number of missing patches.

   {{< screenshot src="updates/xcp-hl-1-missing-patches.png" alt="Host list: a red badge on the host counts its missing patches" >}}

2. **Open the host's Patches tab.** Select the host, then **Patches**. The
   tab lists each package with its name, description, version, release and
   download size; the eye icon on a row shows its RPM changelog. The
   pool-level view, `Home > Pools > <pool> > Patches`, lists the pool master's
   missing packages; check each host separately before a pool-wide action.

   {{< screenshot src="updates/xcp-hl-2-patches-tab.png" alt="The host's Patches tab listing the available packages" >}}

3. **Choose the intended scope.** On the host's Patches tab, **Install all patches** targets that host. On the pool's Patches tab, **Install pool patches** targets all pool hosts, starting with the master. Check the host and pool identities before confirming either action.

   {{< screenshot src="updates/xcp-hl-3-installing.png" alt="The Patches tab while the pool patches are being installed" >}}

   {{< callout type="warning" >}}
   Neither button selects individual XCP-ng packages. For each selected host,
   `updater.py` runs one `yum update` over the enabled stock XCP-ng and
   XCP-hl repositories, so pending stock updates are included. This is a
   combined package operation, not an atomic rollback guarantee. The
   pool action processes hosts one at a time, master first; it does not
   evacuate VMs or reboot hosts for you. To update selected XCP-hl
   packages only, use the separate command-line path below.
   {{< /callout >}}

4. **Wait for the task and refresh the host connection.** In this XO version, the
   button calls the host's updater plugin, then restarts the XAPI agent on the
   selected host after installation. A transient host disconnect can occur.
   This step does not call the XOA-HL appliance updater or restart
   `xo-server`. Preserve an error and inspect the host from an independent
   console before retrying if the connection does not recover.

5. **Verify the result.** Refresh the intended host and pool inventory, task
   result, package/version list, missing-patch count and reboot-required
   indication. A disappearing badge alone does not establish that the
   host rebooted or that guests and storage are healthy.

   {{< screenshot src="updates/xcp-hl-5-up-to-date.png" alt="The Patches tab with the host fully up to date" >}}

### Test a host update on a single-host lab pool {#host-patch-pilot}

Run your first host update on a lab pool you can rebuild, not on a pool you depend on. A single-host test does not show how a multi-host pool behaves during an update.

**Before you start**

- Use a **single-host lab pool** whose release you know, with no ordinary VMs, no running backup task, no HA, and no XOA-HL appliance running on that host.
- Keep a separate host console, a host and network recovery plan, and a separate XOA-HL connection.
- Book an approved window for the whole package set (stock and HomeLab). Decide on the reboot separately.

1. Record the image, package and XO versions above, the host and pool UUIDs, the master, the management address, the installed package versions, the enabled repository IDs, the host's power and enabled state, and the exact list of pending packages. On the **host console**, run `yum check-update` and compare it with the **Patches** tab. Stop if the check fails or the list is unexpected. `yum check-update` can return status 100 when updates exist; that is normal.
2. In the **XOA-HL browser**, open `/#/hosts/<host-id>/patches`, select **Install all patches**, check the host and confirm once. Selecting a row does not limit the update to that package. Record the task ID, its start and end times, and any output or error. Do not click again during a temporary disconnect, and do not start a command-line update at the same time.
3. When the task ends, compare with your notes, using the separate console and the refreshed XOA-HL inventory: installed versions, remaining patches, host reachability, enabled and power state, management network and SR attachments. If the task failed or the connection did not come back, keep the logs and the actual package state. A partial update needs the host owner's recovery or rebuild plan: do not assume it was rolled back.
4. If the UI says a reboot is required, plan a **separate**, approved reboot while the pool is empty. Check that no VM or backup task has appeared, then select **Reboot to apply updates** once on the host's Patches tab. Do not accept any prompt to force the reboot or bypass a blocked suspend, a backup or a version check. Wait for the host on the separate console, then check the XOA-HL connection, packages, reboot indication, network and SRs again. If the button or task behaves unexpectedly, stop and record it. Do not force a second reboot.

**Check:** the host is reachable, its packages match the expected versions, no patches remain and no reboot is pending. Keep the package lists from before and after, the task and console output, any exact error, the reboot decision and the final connectivity. Interrupted installs, recovery and availability in a production or multi-host pool are not covered here. [Host maintenance and evacuation](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) is a separate task with a running test VM; the patch button does not do it.

### From the command line

On the host:

```bash
yum check-update                   # what is available
yum update xcp-hl-release          # the repository configuration itself
yum update xo-lite-ce xoa-proxy    # only the XCP-hl packages
yum update                         # everything, as the Patches tab does
```

### How it works

XCP-ng ships an XAPI plugin, `updater.py`, that Xen Orchestra asks for the
list of available updates. XOA-hl is patched to include the XCP-hl
repositories in that request, which is why XCP-hl packages appear next to
the stock XCP-ng ones.

The repositories are defined in a single file,
`/etc/yum.repos.d/xcp-hl.repo`, owned by the `xcp-hl-release` package:

| Repository ID | Contents | Published from |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{{< callout type="error" >}}
Do not rename the sections in that file. Xen Orchestra passes these
repository IDs to `updater.py`, which lists updates only for the
repositories it was told about. A renamed section raises no error, its
packages just silently disappear from the Patches tab.
{{< /callout >}}

Repository settings are delivered as a package so changes can reach an installed host, rather than relying on a file copied once.
A change to them reaches your host through `yum update xcp-hl-release`.

### First-time setup on an existing host

Hosts installed from an ISO that predates the `xcp-hl-release` package
need a one-time bootstrap. Afterwards, yum manages the configuration.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://rpm.xcp-hl.org/xcp-hl.repo

rpm --import https://rpm.xcp-hl.org/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

Installing the package replaces the file you just downloaded with the
packaged copy, keeping yours as `xcp-hl.repo.rpmorig`. The two differ only
in where they read the signing key from: the downloaded copy fetches it
over HTTPS, the packaged copy uses the local key the package installs.

Newer ISOs already include `xcp-hl-release`, so this step does not apply
to them.

### Rolling back

Each repository publishes only its most recent releases, which bounds how
far back you can go. To return to an earlier build:

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<version>
```

## Updating XOA-hl (the administration UI) {#updating-xoa-hl-the-appliance}

### In Xen Orchestra

1. **Open the update page.** In the XOA-hl web UI, go to
   `Settings > XOA-HL Updates`. It shows the installed version. Until you
   run a check, the status reads *Update status unknown*.

   {{< screenshot src="updates/xoa-hl-1-update-tab.png" alt="The XOA-HL Updates page before any check" >}}

2. **Click Check for update.** The page lists every package with an update
   available, with its version.

   {{< screenshot src="updates/xoa-hl-2-check-result.png" alt="The check result: updates available, with the package list" >}}

3. **Click Update now.** The update log streams into the page as it runs.
   The update restarts xo-server, so the page briefly shows *Reconnecting*
   and then carries on by itself.

   {{< screenshot src="updates/xoa-hl-3-in-progress.png" alt="An update in progress, with its log streaming" >}}

   {{< callout type="warning" >}}
   **Update now** installs every pending package on the appliance,
   including AlmaLinux and the kernel, not just `xoa-hl`. In ce20, the managed updater excludes Node.js.
   {{< /callout >}}

4. **Done.** Once the update finishes, check again: the page reports
   *Up to date*.

   {{< screenshot src="updates/xoa-hl-4-up-to-date.png" alt="The XOA-HL Updates page reporting the appliance up to date" >}}

### From the command line

On the appliance:

```bash
dnf check-update         # what is available
dnf update xoa-hl        # the appliance application only
dnf update --exclude=nodejs  # the application and the AlmaLinux base together
```

### How it works

The appliance has its own yum repository, defined in
`/etc/yum.repos.d/xoa-hl.repo` and owned by the `xoa-hl` package itself:

| Repository ID | Contents | Published from |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

The two buttons on the update page start two systemd units:

| Unit | What it does |
|---|---|
| `xoa-hl-check-update.service` | Runs `dnf check-update` and writes the result to `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Runs a full `dnf -y --refresh --exclude=nodejs update`, logging to `/var/lib/xoa-hl/update.log` |

### Automatic checks and updates

In `xoa-hl` release `v5.113.2_e281c536-ce20`, **Settings → XOA-HL Updates → Automatic updates** offers three modes:

| Mode | Behaviour |
|---|---|
| Manual only | An administrator starts checks and installations; this is the default. |
| Check automatically | Scheduled checks refresh the status; installation remains manual. |
| Install automatically | Checks and installs in the configured maintenance window, after explicit confirmation. |

Choose the frequency, day (for weekly schedules), and local start time, then save. Times use the **appliance’s timezone**, and runs start at the set time with no random delay. Since `v5.113.2_e281c536-ce40`, a failed automatic run shows as a red banner on the page. Installing or upgrading the RPM does not opt you into automatic installation. Older packages may not show these controls: check the installed version first.

The managed updater excludes Node.js, so its supported major version does not change. Updates can restart services, including xo-server. There is **no automatic reboot**; a missed installation window is not replayed immediately after boot. Check the result and arrange any necessary reboot yourself. See the [versioned scheduling reference](https://github.com/Vagrantin/xoa-hl/blob/v5.113.2_e281c536-ce40/docs/automatic-updates.md) for command-line configuration and diagnostics.

### Rolling back

Older packages may be listed by the currently enabled repositories:

```bash
dnf --showduplicates list xoa-hl
```

Availability changes over time. For `v5.113.2_e281c536-ce40`, package downgrade and cross-version configuration recovery have not been validated as appliance recovery procedures. A downgrade does not reverse base-OS updates or restore XO data and operator files. Prepare an export and an isolated recovery test using the [configuration guide](/docs/xoa-hl/configuration-backup/) before planning a rollback.

## Verification and trust

Packages and repository metadata for both XCP-hl and XOA-hl are signed
with the XCP-hl GPG key. The client configuration sets `repo_gpgcheck=1`
with `gpgcheck=0`.

The RPMs are signed by a GPG **subkey**, not the master key, and the
`rpm` tool on XCP-ng 8.3's host system (version 4.11) has a known
limitation here: when you import a key it only registers the master key,
so it reports `NOKEY` for a subkey's signature and can't verify the
package directly, even though the signature is genuine.

Trust runs through the repository metadata instead. The real GPG tool,
which does understand subkeys, verifies `repomd.xml`. That file records a
checksum of `primary.xml`, which in turn records a checksum of every
package, so verifying one file, `repomd.xml`, verifies every RPM in the
repository.

{{< callout type="warning" >}}
The signing subkeys expire **2027-05-10**. After that date verification
fails until they are extended, the published key is refreshed, and it is
re-imported on each host.
{{< /callout >}}

## Known limitations

For the appliance scope reviewed at `v5.113.2_e281c536-ce40`, interruption recovery and downgrade behavior still need disposable-lab validation. Use the [maintenance guide](/docs/xoa-hl/maintenance/) for result checks and reboot decisions.

{{< callout type="info" >}}
Remember that this distribution is in alpha. Read the release notes before
updating: breaking changes are expected at every release, and an update
may need manual intervention.
{{< /callout >}}
