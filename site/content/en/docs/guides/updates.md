---
title: Updates
weight: 3
translationKey: updates
aliases: ["/updates.html"]
---

XCP-hl and XOA-hl both update in place from signed packages, so there is
never a reason to reinstall. The host (XCP-hl) updates from Xen
Orchestra's **Patches** tab, the same way stock XCP-ng does. The appliance
(XOA-hl) updates from its own **XOA-HL Updates** settings page.
{class="lead"}

Both halves of this page follow the same outline: the steps in Xen
Orchestra, the command-line equivalent, how it works underneath, and how
to roll back.

## Updating XCP-hl (the host)

### In Xen Orchestra

1. **See that updates are waiting.** In `Home > Hosts`, a host with
   pending updates shows a red badge with the number of missing patches.

   {{< screenshot src="updates/xcp-hl-1-missing-patches.png" alt="Host list: a red badge on the host counts its missing patches" >}}

2. **Open the host's Patches tab.** Select the host, then **Patches**. The
   tab lists each package with its name, description, version, release and
   download size; the eye icon on a row shows its RPM changelog. The
   pool-level view, `Home > Pools > <pool> > Patches`, shows the same list.

   {{< screenshot src="updates/xcp-hl-2-patches-tab.png" alt="The host's Patches tab listing the available packages" >}}

3. **Click Install pool patches.**

   {{< screenshot src="updates/xcp-hl-3-installing.png" alt="The Patches tab while the pool patches are being installed" >}}

   {{< callout type="warning" >}}
   This is all or nothing. XCP-ng's updater plugin runs a single
   `yum update` across the stock XCP-ng repositories and the XCP-hl ones
   together, so the button also applies any pending XCP-ng updates. There
   is no way to pick individual packages here. To update only the XCP-hl
   packages, use the command line below.
   {{< /callout >}}

4. **Wait for XOA-hl to reload.** Xen Orchestra reloads while the update
   runs, and this can take a while. Be patient and let it come back on its
   own.

   {{< screenshot src="updates/xcp-hl-4-xoa-reloading.png" alt="Xen Orchestra reloading while the host update runs" >}}

5. **Done.** The badge is gone and the Patches tab reports the host as up
   to date.

   {{< screenshot src="updates/xcp-hl-5-up-to-date.png" alt="The Patches tab with the host fully up to date" >}}

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

Because `yum` never re-reads a `.repo` file it already has, the repository
settings are delivered as a package rather than as a file you copy once.
A change to them reaches your host through `yum update xcp-hl-release`.

### First-time setup on an existing host

Hosts installed from an ISO that predates the `xcp-hl-release` package
need a one-time bootstrap. Afterwards, yum manages the configuration.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://vagrantin.github.io/xcp-hl/xcp-hl.repo

rpm --import https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc

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

## Updating XOA-hl (the appliance)

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
   including AlmaLinux and the kernel, not just `xoa-hl`.
   {{< /callout >}}

4. **Done.** Once the update finishes, check again: the page reports
   *Up to date*.

   {{< screenshot src="updates/xoa-hl-4-up-to-date.png" alt="The XOA-HL Updates page reporting the appliance up to date" >}}

### From the command line

On the appliance:

```bash
dnf check-update         # what is available
dnf update xoa-hl        # the appliance application only
dnf update               # the application and the AlmaLinux base together
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
| `xoa-hl-update.service` | Runs a full `dnf -y update`, logging to `/var/lib/xoa-hl/update.log` |

{{< callout type="info" >}}
Neither unit runs on a timer, so nothing checks for XOA-hl updates until
you click **Check for update**. Automatic updates are tracked in
[issue #45](https://github.com/Vagrantin/xcp-hl/issues/45).
{{< /callout >}}

### Rolling back

The repository keeps the five most recent releases. To return to an
earlier one:

```bash
dnf --showduplicates list xoa-hl
dnf downgrade xoa-hl-<version>
```

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

No known limitation at this time.

{{< callout type="info" >}}
Remember that this distribution is in alpha. Read the release notes before
updating: breaking changes are expected at every release, and an update
may need manual intervention.
{{< /callout >}}
