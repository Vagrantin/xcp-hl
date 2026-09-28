---
layout: default
title: Updates
nav_order: 4
---

# Updating XCP-hl
{: .no_toc }

XCP-hl components are shipped as signed RPMs from yum repositories hosted on
GitHub Pages, so a running host updates in place. There is no need to reinstall
from the ISO to pick up a new XO Lite or `xoa-proxy` build.

1. TOC
{:toc}

---

## Where updates appear

Available XCP-hl updates show up in **Xen Orchestra**, in the same place as
stock XCP-ng updates:

```
Home > Hosts > <your host> > Patches
```

The tab lists each available package with its name, description, version,
release and download size, and a red badge shows the count. Selecting **Show
changelog** eye icon on a row opens the RPM changelog entry. The pool-level view at
`Home > Pools > <pool> > Patches` and the dashboard summary show the same data.

XCP-ng ships an XAPI plugin, `updater.py`, that Xen Orchestra queries for available
updates, and XOA-HL is patched to include the XCP-hl repositories in that query.

## Installing updates

**Install all patches** in the Patches tab applies everything the list shows.

{: .warning }
This is all or nothing. XCP-ng's updater plugin runs a single `yum update`
across the stock XCP-ng repositories and the XCP-hl ones together, so pressing
the button also applies any pending XCP-ng OS updates. There is no way to select
individual packages from this view. If you want only the XCP-hl packages, run
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

Packages and repository metadata are signed with the XCP-hl GPG key. The
client configuration sets `repo_gpgcheck=1` with `gpgcheck=0`.

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

The XOA-HL appliance updates itself from its own yum repository:

```bash
dnf update xoa-hl        # the appliance application only
dnf update               # the application and the AlmaLinux base together
```

Configuration lives in `/etc/yum.repos.d/xoa-hl.repo`, owned by the `xoa-hl`
package itself, and defines a single repository:

| Repository ID | Contents | Published from |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

Updates can also be run from the XOA-HL web UI, under **Settings → XOA-HL
Updates**. The page streams the transaction log while it runs.

Systemd units drive the updates:

| Unit | What it does |
|---|---|
| `xoa-hl-check-update.service` | Runs `dnf check-update` and writes the result to `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Runs a full `dnf -y update`, excluding `nodejs`, and streams it to `/var/lib/xoa-hl/update.log` |
| `xoa-hl-check-update.timer` | Runs the check on a schedule, in `check` mode |
| `xoa-hl-auto-update.service` / `.timer` | Checks, then installs, during a maintenance window, in `install` mode |

{: .warning }
`xoa-hl-update.service` updates **every** package with a pending update, not
just `xoa-hl`. Node.js is the exception: it stays on the major version the
`xoa-hl` package requires.

### Update modes

Releases after `v5.113.2_e281c536-ce18` add scheduled checks and automatic
installation. Both are **off by default**: installing or upgrading the package
never enables either timer. Choose a mode in **Settings → XOA-HL Updates**, or
as root:

```bash
# MODE FREQUENCY DAY TIME RANDOM_DELAY_MINUTES
/usr/libexec/xoa-hl/configure-updates.sh check weekly Sun 03:00 15
```

| Mode | What runs on its own |
|---|---|
| `manual` (default) | Nothing. Checks and updates start only when an administrator runs them |
| `check` | The update check, on schedule and shortly after boot. Installing stays manual |
| `install` | The check, then the update, in the maintenance window. A missed window is not replayed after boot |

The appliance never reboots on its own, even in `install` mode. See
[automatic appliance updates](https://github.com/Vagrantin/xoa-hl/blob/main/docs/automatic-updates.md)
for the schedule options and how to inspect the result.

### The update page loses its connection

Installing a new `xoa-hl` restarts `xo-server`, which also serves the web UI, so
the update page loses its connection for a while. The update itself runs in
`xoa-hl-update.service` and carries on regardless.

Releases after `v5.113.2_e281c536-ce18` handle this:

- the page keeps trying to reconnect for as long as `xo-server` is down, then
  resumes the log where it stopped and shows the result;
- `xo-server` is restarted once, after the whole transaction has finished;
- after a minute without a connection, the page says how long `xo-server` has
  been unreachable and offers a **Reload page** button, which reloads only once
  `xo-server` answers again;
- reloading the page brings back the update that tab started, with its result.

## Known limitations

- **The update that installs the reconnection fix can still look stuck.** The
  page you started it from is still running the old code, which stops trying to
  reconnect after about 2.5 minutes. If it stays on *Reconnecting to
  xo-server*, wait until `xo-server` is reachable again and refresh the page.
  The update is not affected. To read the log from a shell:
  `cat /var/lib/xoa-hl/update.log`. This applies once, to the upgrade from
  `v5.113.2_e281c536-ce18` or earlier. See
  [issue #103](https://github.com/Vagrantin/xcp-hl/issues/103).

{: .note }
Remember that this distribution is in alpha. Read the release notes before
updating: breaking changes are expected at every release, and an update may need
manual intervention on the host.
