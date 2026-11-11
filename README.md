# XCP-hl

Documentation site for **XCP-hl** — a free, community-built ISO based on upstream XCP-ng that replaces the official one-click XOA deployment with a fully self-hosted, community-maintained Xen Orchestra workflow, aimed at home-labbers.

This repository also builds and publishes the `xcp-hl-release` RPM and its
yum repository (`xcp-hl-base`, `xcp-hl-xolite`, `xcp-hl-xoa-proxy`), served
from GitHub Pages at `repo/8.3/x86_64/`. Installing `xcp-hl-release` on a
host registers all three and keeps their configuration up to date via
`yum update xcp-hl-release`. See `docs/features.md` for the GPG signing
model and `docs/developers/index.md` for build details.

The site is a Jekyll project (Just the Docs theme) under `docs/`:

- `index.md` — landing page: what XCP-hl is and download links.
- `features.md` — feature overview.
- `roadmap.md` — planned improvements.
- `release-matrix.md` — component/version compatibility matrix.
- `developers/` — developer-facing documentation.
- `_config.yml`, `_data/`, `Gemfile` — Jekyll configuration.

## Project naming

Use **XCP-hl** for this project in every documentation language. Use **XCP-ng**
when referring to the upstream hypervisor, its tools, or its ecosystem.

The rule covers prose only. Anything a user can see, type, or match against the
running system is reproduced verbatim, whatever its casing:

- repository URLs, package and artifact filenames (`xcp-ng-ce-public.asc`,
  `RPM-GPG-KEY-xcp-ng-ce`);
- GPG identities — the signing key's UID is literally
  `XCP-ng Community Edition (Master signing key)`, which is what
  `gpg --list-keys` and `rpm -qi` print;
- component and build names such as `XOA-HL` and `xolite-ce`;
- exact system labels such as the `XCP-HL ISO library` ISO SR.

## Local preview

The Hugo documentation source is in `site/`. See [site/README.md](site/README.md)
for pinned tools, validation and standalone bundles, and
[site/CUTOVER.md](site/CUTOVER.md) for production acceptance and rollback.

```bash
site/scripts/build_docs.sh http://127.0.0.1:8000/ /tmp/xcp-hl-docs
python3 -m http.server 8000 --directory /tmp/xcp-hl-docs
```

The old Jekyll `docs/` tree is retained for the migration audit and rollback.
`docs/_data/` remains the release publisher's data contract.

## Related repositories

- [xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso) — the ISO build (download from its Releases page).
- `../xolite-ce`, `../xoa-proxy`, `../xoa-hl`, `../build-xoa-hl-vm` — the components documented here.
