# XCP-hl

Documentation site for **XCP-hl** — a free, community-built ISO based on upstream XCP-ng that replaces the official one-click XOA deployment with a fully self-hosted, community-maintained Xen Orchestra workflow, aimed at home-labbers.

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

```bash
cd docs
bundle install
bundle exec jekyll serve
```

## Related repositories

- [xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso) — the ISO build (download from its Releases page).
- `../xolite-ce`, `../xoa-proxy`, `../xoa-hl`, `../build-xoa-hl-vm` — the components documented here.
