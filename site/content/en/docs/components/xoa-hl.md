---
title: xoa-hl
weight: 4
translationKey: xoa-hl
aliases: ["/developers/xoa-hl.html"]
---

XOA-hl software build: patches Xen Orchestra for home-lab use and packages it as an RPM.
{class="lead"}

**Repository:** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· Language: Bash / RPM spec · License: AGPL-3.0

## Purpose

This repo builds **Xen Orchestra HomeLab Edition** (XOA-hl): the full
open-source [`xen-orchestra`](https://github.com/vatesfr/xen-orchestra)
server + XO 5 web UI, fetched at a pinned upstream commit, patched for
home-lab use, and packaged for XCP-ng. Each build publishes one artifact
as a GitHub Release:

| Artifact | Content |
|---|---|
| `xoa-hl-<version>-<N>.g<commit>.xcpng8.3.el9.x86_64.rpm` | The pre-built Xen Orchestra (about 70 MiB), its systemd units, and the appliance's self-update tooling |

The RPM is what [`build-xoa-hl`](/docs/components/build-xoa-hl) installs into the XOA VM
appliance. The five most recent releases are also republished as a signed
yum repository, which is where a running appliance gets its updates from
(see [Updates](/docs/guides/updates)).

---

## Repo structure

```
xoa-hl/
├── UPSTREAM_XO                 ← upstream xen-orchestra pin (commit + version)
├── container/
│   └── Containerfile           ← AlmaLinux 9 build image (Node 24, yarn, rpm tooling)
├── scripts/
│   ├── build-xo.sh             ← the build: fetch + patch + yarn build + tar
│   └── validate-patches.sh     ← checks patches/ against metadata.toml
├── patches/
│   ├── metadata.toml           ← what each patch does and which file it targets
│   ├── menu-hide-items.patch   ← hides Vates-subscription-only menu items
│   ├── xcp-hl-updates.patch    ← adds the XCP-hl repositories to the Patches tab
│   └── xoa-hl-update-api.patch ← the appliance's own "XOA-HL Updates" settings page
├── SPECS/
│   └── xoa-hl.spec             ← the RPM: pre-built XO under /opt/xo + systemd units
├── SOURCES/                    ← systemd units, update scripts, sudoers rule, .repo file
├── pages/                      ← index page + .repo file for the published yum repository
└── .github/workflows/
    ├── build-xoa.yml           ← CI: build + RPM + GitHub Release
    └── pages-repo.yml          ← republishes recent RPMs as a signed yum repository
```

---

## Version pinning

The build targets a fixed upstream commit, set in the `UPSTREAM_XO` file at
the root of the repository:

```bash
XO_COMMIT=e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c
XO_VERSION=5.113.2
```

The version string combines both:
`<XO_VERSION>_<short SHA>` → e.g. `5.113.2_e281c536`. `build-xo.sh` writes
it to `out/VERSION`, and CI uses it as the RPM version. A release is cut
by pushing a tag `v<version>-ce<N>`, for example
`v5.113.2_e281c536-ce17`: `N` becomes the RPM release number, so every
build is a distinct package that `dnf` can upgrade to.

{{< callout type="info" >}}
Upstream is bumped **deliberately**, by editing `UPSTREAM_XO`, never
automatically. `5.113.2` is the last XO 5.x release before upstream moved
on to XO 6.
{{< /callout >}}

---

## Build flow, scripts/build-xo.sh

The build runs inside the AlmaLinux 9 container and works on `/build`:

1. **Shallow fetch at the pinned SHA**, `git init` + `git fetch --depth 1
   origin $XO_COMMIT` + `checkout FETCH_HEAD`. Pinning a bare SHA with
   `--depth 1` avoids pulling the full ~1 GB history while staying
   reproducible.
2. **Apply patches**, after checking that every `patches/*.patch` has an
   entry in `patches/metadata.toml` and the other way round, each patch is
   applied with `git apply --verbose`. There are three:
   - `menu-hide-items`, hides menu entries that only work with a Vates
     subscription.
   - `xcp-hl-updates`, adds the XCP-hl repositories to the query Xen
     Orchestra sends the host's `updater.py` plugin, so XCP-hl packages
     show up in the Patches tab.
   - `xoa-hl-update-api`, adds the appliance's own update API and the
     **XOA-HL Updates** settings page.
3. **Write `packages/xo-server/xoahl.config.toml`**, the runtime config
   the RPM later installs as the user config: HTTPS on port 443 with
   `/opt/xo/xoahl.crt` / `/opt/xo/xoahl.key`, Redis at
   `redis://127.0.0.1:6379/0`.
4. **Generate a self-signed TLS certificate**, `openssl req -x509`
   (RSA 4096, 10 years, CN `xoa.local`) → `xoahl.key` (mode 600) and
   `xoahl.crt` (mode 644).
5. **Install + build**, `yarn` then `yarn build` across all workspaces
   (server and XO 5 web UI).
6. **Prune**, drop `.git`, `.github`, `.changesets`, `docs`,
   `packages/xo-server-test*`, `packages/xo-server-cloud`.
7. **Strip devDependencies**, `yarn workspaces focus --production`
   (fallback: `yarn install --production`), preserving workspace symlinks.
8. **Package**, `tar czf out/xoa-hl-<version>.tar.gz` of the whole pruned
   monorepo, excluding `**/*.map`. The tarball is only an input to the RPM
   build, it is not published.

---

## The RPM, SPECS/xoa-hl.spec

The RPM ships the pre-built Xen Orchestra itself, about 70 MiB. It is
`x86_64`, not `noarch`, because the `node_modules` tree carries native
add-ons. It installs:

| Path | What it is |
|---|---|
| `/opt/xo` | The pre-built xen-orchestra tree, plus the TLS pair `xoahl.key` / `xoahl.crt` |
| `/usr/local/bin/xo-cli` | `xo-cli` on `PATH` |
| `/usr/lib/systemd/system/xo-server.service` | Runs xo-server from `/opt/xo` |
| `/usr/lib/systemd/system/xoa-hl-check-update.service` and `xoa-hl-update.service` | Check for, and apply, appliance updates |
| `/usr/libexec/xoa-hl/` | The scripts those two units run |
| `/etc/yum.repos.d/xoa-hl.repo` | The appliance's own yum repository |
| `/etc/sudoers.d/xoa-hl` | Lets xo-server start the two update units |
| `/var/lib/xoa-hl/` | Where the update log is written |

At install time, `%post`:

1. **Bootstraps the user config on first install only**, copying
   `xoahl.config.toml` to `/root/.config/xo-server/config.toml` if that
   file does not exist. On upgrade it is left untouched to preserve
   operator customisations.
2. Runs `systemctl enable redis --now`, then enables and restarts
   `xo-server`.

`%preun` stops and disables `xo-server` on final removal only, not on
upgrade. Every file above belongs to the package, so `dnf remove` cleans
them all up; `%postun` only reloads systemd.

{{< callout type="error" >}}
xo-server reads `~/.config/xo-server/config.toml` (XDG lookup), which
overrides any package-level `config.toml`. Without the `%post` bootstrap,
the HTTPS listener and Redis URI would not be applied regardless of what
the package contains.
{{< /callout >}}

Runtime dependencies: `nodejs >= 24`, `redis`, plus the mount helpers Xen
Orchestra needs for remotes (`nfs-utils`, `cifs-utils`, `ntfs-3g`, `lvm2`).
The package carries `Epoch: 1`, so it outranks builds from before the
current numbering scheme.

---

## Build environment

`container/Containerfile` defines the build image: AlmaLinux 9 with
gcc/make/git/patch, Python 3, Node.js 24 (NodeSource), yarn, and
`rpm-build`/`rpmdevtools`. The same image builds both the tarball and the
RPM.

Builds run **exclusively on GitHub Actions**, there is no local build
workflow. CI builds the image with Docker and runs `build-xo.sh` inside
it; the tarball and `VERSION` file land in `out/` on the runner and feed
the RPM build.

---

## CI workflow (GitHub Actions)

`.github/workflows/build-xoa.yml` triggers on a pushed `v*-ce<N>` tag and
on `workflow_dispatch`:

1. Check the syntax of every shell script: `scripts/*.sh` with `bash`,
   and the `SOURCES/*.sh` scripts that ship in the RPM with `sh`.
2. Build the container image and run `build-xo.sh` in it (mounting
   `patches/`, `scripts/`, `out/` and `UPSTREAM_XO`).
3. Read `out/VERSION`, and take `N` from the tag as the RPM release number.
4. Run `rpmbuild -bb SPECS/xoa-hl.spec` inside the same image, with the
   tarball staged in `SOURCES/`.
5. Publish a GitHub Release, named after the tag, containing the RPM.

After each successful build, `.github/workflows/pages-repo.yml` collects
the RPMs of the five newest releases and publishes them, with signed
metadata, as a yum repository at
`https://vagrantin.github.io/xoa-hl/8.3/x86_64/`. That is the repository
the appliance's `xoa-hl.repo` points at.

The **VM image releases** created by the orchestrator's `xoa-vm-agent`
(tag prefix `xoa-image-`, asset `XOA-hl.xva`) are published on
[`build-xoa-hl`](/docs/components/build-xoa-hl), the repo the image is built from, see
[#22](https://github.com/Vagrantin/xcp-hl/issues/22).

{{< callout type="warning" >}}
Image releases published before that move are still here, and are kept so
already-shipped ISOs keep resolving them. Tooling that scans this repo for
the RPM must therefore still skip `xoa-image-*` tags.
{{< /callout >}}

---

## Relationship to other components

- [`build-xoa-hl`](/docs/components/build-xoa-hl), installs this RPM into the AlmaLinux 9
  appliance and packages it as an XVA image.
- [`xolite-ce`](/docs/components/xolite-ce), the XO Lite deploy button installs that
  appliance.
- [`xoa-proxy`](/docs/components/xoa-proxy), HTTPS/gzip bridge used while the appliance
  image is delivered.
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
  (in the `buildorchestration` repo), its `xoa-vm-agent` triggers `build-xoa.yml` and
  waits for the RPM release before starting the VM image build.

---

## Contributing

To report a problem or suggest a change, open an issue on
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
