# XCP-ng Home-laber Edition (xcp-hl)

Documentation site for **XCP-ng Community / Home-laber Edition** — a free, community-built XCP-ng ISO that replaces the official one-click XOA deployment with a fully self-hosted, community-maintained Xen Orchestra workflow, aimed at home-labbers.

This repository also builds and publishes the `xcp-hl-release` RPM and its
yum repository (`xcp-hl-base`, `xcp-hl-xolite`, `xcp-hl-xoa-proxy`), served
from GitHub Pages at `repo/8.3/x86_64/`. Installing `xcp-hl-release` on a
host registers all three and keeps their configuration up to date via
`yum update xcp-hl-release`. See `docs/features.md` for the GPG signing
model and `docs/developers/index.md` for build details.

The site is a Jekyll project (Just the Docs theme) under `docs/`:

- `index.md` — landing page: what XCP-ng CE is and download links.
- `features.md` — feature overview.
- `roadmap.md` — planned improvements.
- `release-matrix.md` — component/version compatibility matrix.
- `developers/` — developer-facing documentation.
- `_config.yml`, `_data/`, `Gemfile` — Jekyll configuration.

## Related repositories

- [xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso) — the ISO build (download from its Releases page).
- `../xolite-ce`, `../xoa-proxy`, `../xoa-hl`, `../build-xoa-hl-vm` — the components documented here.
