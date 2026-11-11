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

The site is a Hugo project (Hextra theme) under `site/`, built by
[site/scripts/build_docs.sh](site/scripts/build_docs.sh):

- `site/content/{en,fr,ja,es,de}/docs/`: the five published languages.
- `site/data/`: release data staged from `docs/_data/` at build time.
- `site/layouts/`, `site/assets/`, `site/i18n/`: templates, static assets
  and translation strings.

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

The old Jekyll source tree was retired on 2026-11-11 after the Hugo cutover
was accepted. What remains under `docs/` is live data, not renderable source:
`docs/_data/` is the release publisher's data contract,
`docs/screenshots/requests/` feeds the jenkins-infra `docs/screenshots` job,
and `docs/developers/patching-model-assessment.md` keeps the decision-record
link published on the component pages.

## Related repositories

- [xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso) — the ISO build (download from its Releases page).
- `../xolite-ce`, `../xoa-proxy`, `../xoa-hl`, `../build-xoa-hl-vm` — the components documented here.
