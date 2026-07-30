---
layout: default
title: xoa-hl
parent: Developers
nav_order: 4
---

# xoa-hl
{: .no_toc }

XOA-HL software build, patches Xen Orchestra for home-lab use and packages it as a tarball + thin RPM.
{: .fs-6 .fw-300 }

**Repository:** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· Language: Bash / RPM spec · License: AGPL-3.0

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Purpose

This repo builds **Xen Orchestra HomeLab Edition** (XOA-HL): the full
open-source [`xen-orchestra`](https://github.com/vatesfr/xen-orchestra)
server + XO 5 web UI, fetched at a pinned upstream commit, patched for
home-lab use, and packaged for XCP-ng. Each build publishes two artifacts
as a GitHub Release:

| Artifact | Content |
|---|---|
| `xoa-hl-<version>.tar.gz` | The pruned, pre-built xen-orchestra monorepo |
| `xoa-hl-<version>-1.*.noarch.rpm` | Thin installer RPM that fetches the tarball at install time |

The RPM is what [`build-xoa-hl`](build-xoa-hl) installs into the XOA VM
appliance.

---

## Repo structure

```
xoa-hl/
├── container/
│   └── Containerfile           ← AlmaLinux 9 build image (Node 24, yarn, rpm tooling)
├── scripts/
│   └── build-xo.sh             ← the build: fetch + patch + yarn build + tar
├── patches/
│   └── menu-hide-items.patch   ← hides Vates-subscription-only menu items
├── SPECS/
│   └── xoa-hl.spec             ← thin noarch RPM (downloads tarball in %post)
├── SOURCES/
│   └── xo-server.service       ← systemd unit running xo-server from /opt/xo
└── .github/workflows/
    └── build-xoa.yml           ← CI: tarball + RPM + GitHub Release
```

---

## Version pinning

The build targets a fixed upstream commit, set at the top of
`scripts/build-xo.sh`:

```bash
XO_REPO="https://github.com/vatesfr/xen-orchestra.git"
XO_COMMIT="e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c" # 5.113.2, last XO 5.x release
XO_VERSION="5.113.2"
```

The release version string combines both:
`<XO_VERSION>_<short SHA>` → e.g. `5.113.2_e281c536`. It is written to
`out/VERSION`, which CI reads to name the tarball, the RPM, and the release
tag (`v<version>`).

{: .note }
Upstream is bumped **deliberately**, by editing `XO_COMMIT`/`XO_VERSION`,
never automatically. `5.113.2` is the last XO 5.x release before upstream
moved on to XO 6.

---

## Build flow, scripts/build-xo.sh

The build runs inside the AlmaLinux 9 container and works on `/build`:

1. **Shallow fetch at the pinned SHA**, `git init` + `git fetch --depth 1
   origin $XO_COMMIT` + `checkout FETCH_HEAD`. Pinning a bare SHA with
   `--depth 1` avoids pulling the full ~1 GB history while staying
   reproducible.
2. **Apply patches**, every `patches/*.patch` is applied with
   `git apply --verbose`. Currently one patch: `menu-hide-items.patch`
   (hides menu entries that only work with a Vates subscription).
3. **Write `packages/xo-server/xoahl.config.toml`**, the runtime config
   the RPM later installs as the user config: HTTPS on port 443 with
   `/opt/xo/xoahl.crt` / `/opt/xo/xoahl.key`, Redis at
   `redis://127.0.0.1:6379/0`.
4. **Generate a self-signed TLS certificate**, `openssl req -x509`
   (RSA 4096, 10 years, CN `xoa.local`) → `xoahl.key` (mode 600) and
   `xoahl.crt` (mode 644), shipped inside the tarball.
5. **Install + build**, `yarn` then `yarn build` across all workspaces
   (server and XO 5 web UI).
6. **Prune**, drop `.git`, `.github`, `.changesets`, `docs`,
   `packages/xo-server-test*`, `packages/xo-server-cloud`.
7. **Strip devDependencies**, `yarn workspaces focus --production`
   (fallback: `yarn install --production`), preserving workspace symlinks.
8. **Package**, `tar czf out/xoa-hl-<version>.tar.gz` of the whole pruned
   monorepo, excluding `**/*.map`.

---

## The thin RPM, SPECS/xoa-hl.spec

The RPM is deliberately thin: `%files` ships **only**
`/usr/lib/systemd/system/xo-server.service`. Everything else happens in
`%post` at install time:

1. Download the release tarball from
   `https://github.com/Vagrantin/xoa-hl/releases/download/v<version>/…`
   and extract it to `/opt/xo`.
2. Move the TLS key/cert to `/opt/xo/xoahl.key` / `/opt/xo/xoahl.crt`
   (the paths referenced by the config).
3. **Bootstrap the user config on first install only**, copy
   `xoahl.config.toml` to `/root/.config/xo-server/config.toml` if that
   file does not exist. On upgrade it is left untouched to preserve
   operator customisations.
4. Expose `xo-cli` on `PATH` (symlink to `/usr/local/bin/xo-cli`).
5. `systemctl enable redis --now` and enable + start `xo-server`.

`%preun` stops and disables `xo-server`; `%postun` removes the `xo-cli`
symlink and `/opt/xo`.

{: .important }
xo-server reads `~/.config/xo-server/config.toml` (XDG lookup), which
overrides any package-level `config.toml`. Without the `%post` bootstrap,
the HTTPS listener and Redis URI would not be applied regardless of what
the tarball contains.

Runtime dependencies: `nodejs >= 24`, `redis`, `curl`, plus the mount
helpers Xen Orchestra needs for remotes (`nfs-utils`, `cifs-utils`,
`ntfs-3g`, `lvm2`).

---

## Build environment

`container/Containerfile` defines the build image: AlmaLinux 9 with
gcc/make/git/patch, Python 3, Node.js 24 (NodeSource), yarn, and
`rpm-build`/`rpmdevtools`. The same image builds both the tarball and the
RPM.

Builds run **exclusively on GitHub Actions**, there is no local build
workflow. CI builds the image with Docker on every push and runs
`build-xo.sh` inside it; the tarball and `VERSION` file land in `out/`
on the runner and are published as release assets.

---

## CI workflow (GitHub Actions)

`.github/workflows/build-xoa.yml` triggers on `push` and
`workflow_dispatch`:

1. Build the container image and run `build-xo.sh` in it (mounting
   `patches/`, `scripts/`, and `out/`).
2. Read `out/VERSION` to derive the version string.
3. Run `rpmbuild -bb SPECS/xoa-hl.spec` inside the same image, with
   `_version` defined from the version string.
4. Publish a GitHub Release tagged `v<version>` containing the tarball
   and the noarch RPM.

The **VM image releases** created by the orchestrator's `xoa-vm-agent`
(tag prefix `xoa-image-`, asset `xoa-almalinux.xva`) are published on
[`build-xoa-hl`](build-xoa-hl), the repo the image is built from, see
[#22](https://github.com/Vagrantin/xcp-hl/issues/22).

{: .warning }
Image releases published before that move are still here, and are kept so
already-shipped ISOs keep resolving them. Tooling that scans this repo for
the RPM must therefore still skip `xoa-image-*` tags: `releases/latest`
currently points at one of them.

{: .note }
The tarball must be published on the release **before** the RPM is
installed anywhere: the RPM's `%post` downloads it from that very release
URL.

---

## Relationship to other components

- [`build-xoa-hl`](build-xoa-hl), installs this RPM into the AlmaLinux 9
  appliance and packages it as an XVA image.
- [`xolite-ce`](xolite-ce), the XO Lite deploy button installs that
  appliance.
- [`xoa-proxy`](xoa-proxy), HTTPS/gzip bridge used while the appliance
  image is delivered.
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
  (in the `buildorchestration` repo), its `xoa-vm-agent` triggers `build-xoa.yml` and
  waits for the RPM release before starting the VM image build.

---

## Contributing

To report a problem or suggest a change, open an issue on
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).

Today the build is handled by the orchestrator,
[`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator),
a sub-directory of the `buildorchestration` repository: its `xoa-vm-agent`
triggers `build-xoa.yml` and consumes the resulting release.
