# XCP-hl

Documentation site for **XCP-hl** — a free, community-built ISO based on upstream XCP-ng that replaces the official one-click XOA deployment with a fully self-hosted, community-maintained Xen Orchestra workflow, aimed at home-labbers.

This repository also builds the `xcp-hl-release` RPM, which installs
`/etc/yum.repos.d/xcp-hl.repo` (repositories `xcp-hl-base`, `xcp-hl-xolite`,
`xcp-hl-xoa-proxy`) and the signing key. The signed RPM is published as a
GitHub Release. Hosts read the repositories from `https://rpm.xcp-hl.org/`,
built by [Vagrantin/xcp-hl-rpm](https://github.com/Vagrantin/xcp-hl-rpm)
(#190). The older GitHub Pages copy of `xcp-hl-base` at `repo/8.3/x86_64/`
is legacy and kept only until hosts have moved. `yum update xcp-hl-release`
keeps the repository configuration current. See
`site/content/en/docs/guides/updates.md` for the update model and
`site/content/en/docs/components/_index.md` for the GPG signing model.

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
