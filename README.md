# XCP-ng Home-laber Edition (xcp-hl)

Documentation site for **XCP-ng Community / Home-laber Edition** — a free, community-built XCP-ng ISO that replaces the official one-click XOA deployment with a fully self-hosted, community-maintained Xen Orchestra workflow, aimed at home-labbers.

The site is a Jekyll project (Just the Docs theme) under `docs/`:

- `index.md` — landing page: what XCP-ng CE is and download links.
- `features.md` — feature overview.
- `roadmap.md` — planned improvements.
- `release-matrix.md` — component/version compatibility matrix.
- `developers/` — developer-facing documentation.
- `_config.yml`, `_data/`, `Gemfile` — Jekyll configuration.

## Local preview

```bash
cd docs
bundle install
bundle exec jekyll serve
```

## Related repositories

- [xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso) — the ISO build (download from its Releases page).
- `../xolite-ce`, `../xoa-proxy`, `../xoa-hl`, `../build-xoa-hl-vm` — the components documented here.
