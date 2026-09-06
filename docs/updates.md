---
layout: default
title: Updates
nav_order: 4
---

# Updating XCP-ng HomeLab Edition
{: .no_toc }

XCP-HL components are shipped as signed RPMs from yum repositories hosted on
GitHub Pages, so a running host updates in place. There is no need to reinstall
from the ISO to pick up a new XO Lite or `xoa-proxy` build.

1. TOC
{:toc}

---

## Where updates appear

Available XCP-HL updates show up in **Xen Orchestra**, in the same place as
stock XCP-ng updates:

```
Home > Hosts > <your host> > Patches
```

The tab lists each available package with its name, description, version,
release and download size, and a red badge shows the count. Selecting **Show
changelog** eye icon on a row opens the RPM changelog entry. The pool-level view at
`Home > Pools > <pool> > Patches` and the dashboard summary show the same data.

XCP-ng ships an XAPI plugin, `updater.py`, that Xen Orchestra queries for available
updates, and XOA-HL is patched to include the XCP-HL repositories in that query.

## Installing updates

**Install all patches** in the Patches tab applies everything the list shows.

{: .warning }
This is all or nothing. XCP-ng's updater plugin runs a single `yum update`
across the stock XCP-ng repositories and the XCP-HL ones together, so pressing
the button also applies any pending XCP-ng OS updates. There is no way to select
individual packages from this view. If you want only the XCP-HL packages, run
`yum update xo-lite-ce xoa-proxy` on the host instead.

From the host command line, the equivalents are:

```bash
yum check-update            # what is available
yum update xcp-hl-release   # repository configuration itself
yum update xo-lite-ce       # XO Lite (HomeLab Edition)
yum update xoa-proxy        # XVA deploy proxy
```

## Repository configuration

Configuration lives in a single file, `/etc/yum.repos.d/xcp-hl.repo`, owned by
the `xcp-hl-release` package. It defines three repositories:

| Repository ID | Contents | Published from |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{: .important }
Do not rename the sections in that file. The repository IDs are passed 
by Xen Orchestra to the `updater.py` plugin, which lists updates only for
repositories it was told about. A renamed section does not raise an error, it
silently removes those packages from the Patches tab.

Because `yum` never re-reads a `.repo` file it already has, repository settings
are delivered as a package rather than as a file you copy once. A change to the
configuration reaches your host through `yum update xcp-hl-release`.

The file is deliberately **not** marked `%config`, so `yum update
xcp-hl-release` replaces it outright and any local edit to it is lost. That is
the intent: keeping a modified copy would stop corrected repository settings
from ever reaching a host that had once edited the file. Override a setting for
a single command with `yum --setopt=xcp-hl-base.<option>=<value>` instead of
editing the file.

## First-time setup on an existing host

Hosts installed from an ISO that predates the `xcp-hl-release` package need a
one-time bootstrap. Afterwards, configuration is managed by yum.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://vagrantin.github.io/xcp-hl/xcp-hl.repo

rpm --import https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

Installing the package replaces the file you just downloaded with the packaged
copy, keeping yours as `xcp-hl.repo.rpmorig`. The two differ only in where they
read the signing key from: the downloaded copy fetches it over HTTPS, while the
packaged copy uses the local key the package installs.

Newer ISOs carry `xcp-hl-release` already, so this section does not apply to
them.

## Rolling back

Each repository publishes only its most recent releases, which bounds the
rollback window. To move back to an earlier build:

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<version>
```

## Verification and trust

Packages and repository metadata are signed with the XCP-ng HomeLab Edition GPG
key. The client configuration sets `repo_gpgcheck=1` with `gpgcheck=0`.

The RPMs are signed by a GPG **signing subkey**. On XCP-ng 8.3 dom0, rpm 4.11
registers only the primary key when a key is imported, so it reports `NOKEY` for
any signature made by a subkey and cannot verify the packages directly. Trust
therefore runs through the repository metadata: `repomd.xml` is signed and
verified by GPG proper, which is subkey aware; it records a SHA-256 of
`primary.xml`, which in turn records a SHA-256 of every package.

{: .warning }
The signing subkeys expire **2027-05-10**. After that date verification fails
until they are extended, the published key is refreshed, and it is re-imported
on each host.

## Updating the XOA-HL appliance

The XOA-HL appliance updates itself from its own yum repository, separate from
the three host repositories above. The appliance runs AlmaLinux 9, so the
command is `dnf`, not `yum`:

```bash
dnf update xoa-hl        # the appliance application only
dnf update               # the application and the AlmaLinux base together
```

Configuration lives in `/etc/yum.repos.d/xoa-hl.repo`, owned by the `xoa-hl`
package itself, and defines a single repository:

| Repository ID | Contents | Published from |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

The ID is deliberately not one of the `xcp-hl-*` names. Those are a contract
with dom0's `updater.py` plugin, and the appliance is a guest that never calls
it, so XOA-HL updates do **not** appear in the Patches tab.

Two systemd units drive the same work from the appliance UI:

| Unit | What it does |
|---|---|
| `xoa-hl-check-update.service` | Runs `dnf check-update` and writes the result to `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Runs a full `dnf -y update` |

{: .warning }
`xoa-hl-update.service` updates **every** package with a pending update, not
just `xoa-hl`. On this appliance that includes `nodejs` from the NodeSource
repository, and a Node major bump can leave `xo-server` unable to start.

{: .note }
Neither unit is on a timer, so nothing checks for XOA-HL updates on its own
yet. Scheduling the check is tracked in
[issue #45](https://github.com/Vagrantin/xcp-hl/issues/45).

## Known limitations

Updating in place covers the XOA-HL application and the appliance's AlmaLinux
packages. It does not cover the appliance image itself: changes to
partitioning, to the kickstart, or to the base OS release still need a newer
XVA to be deployed. The wider update and upgrade management work is tracked in
[issue #14](https://github.com/Vagrantin/xcp-hl/issues/14) and
[issue #33](https://github.com/Vagrantin/xcp-hl/issues/33).

{: .note }
Remember that this distribution is in alpha. Read the release notes before
updating: breaking changes are expected at every release, and an update may need
manual intervention on the host.
