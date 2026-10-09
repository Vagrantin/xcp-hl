# XCP-hl documentation (Hugo + Hextra)

Source of truth: `Vagrantin/xcp-hl/site/`. English, French and Japanese share
one structure and use Hugo's native multilingual support. Each language has its
own, non-overlapping `contentDir` and every page has a `translationKey`.

The existing production site is <https://vagrantin.github.io/xcp-hl/>.
The migration preview is <https://xcp-hl.net/>, deployed by `Vagrantin/xcp-ce`
from a selected `xcp-hl` ref. `xcp-hl.org` was an earlier proposal and is not the
preview domain. See [CUTOVER.md](CUTOVER.md) before changing production or DNS.

The XOA-HL manual source and editorial policy are described in
[XOA-MANUAL.md](XOA-MANUAL.md) (#189). Its new deployment through `xcp-ce` is
documentation-only and does not require the old combined docs/RPM cutover.
The manual's glossary is tracked at `data/xoa_glossary.json`; release and status
data in that directory are generated. `build_docs.sh` validates the required
manual pages and translation source revisions before rendering the status table.
French/Japanese foundation pages are explicitly drafts. Use
`python3 site/scripts/check_xoa_manual.py --require-reviewed` as the reviewed
publication gate; preview builds allow draft translations.

## Build and validation

Documentation previews require Hugo **extended 0.151.0**, Go **1.24.7** and
Python 3. These are documentation-only builds; product RPM/ISO builds stay in CI.
The theme is pinned to Hextra 0.12.3 in `go.mod`/`go.sum`. FlexSearch is vendored
in `assets/js/` with its Apache-2.0 license. Rendering needs no live API calls;
initial Hugo module resolution needs network access unless cached.

From the repository root, choose a new output directory:

```bash
site/scripts/build_docs.sh https://vagrantin.github.io/xcp-hl/ /tmp/docs-pages
site/scripts/build_docs.sh https://docs.example.org/ /tmp/docs-standalone
python3 -m http.server 8000 --directory /tmp/docs-standalone
```

The script checks translation structure, missing translations/screenshots,
duplicate output paths, every language switcher, local assets, internal links
and fragments, language alternates, and old Jekyll paths/explicit anchors.
CI also exercises real browser interactions and requires mobile Lighthouse
performance and accessibility scores of at least 95 on the homepage and
Getting Started in all three languages. JSON reports and screenshots are
uploaded as `docs-browser-evidence`. Local results are lab measurements, not
measurements of the deployed Pages service. The Lighthouse fixture uses HTTP
gzip (`serve_docs.py`); enable text compression on a standalone host and repeat
the measurements on the actual staging endpoint before cutover. Plain HTTP
serving was also checked for functional compatibility.
It refuses to overwrite an existing output directory. `check_legacy_urls.py`
uses the old `docs/` tree as a migration inventory, so retain that source until
cutover is accepted (or replace it with a reviewed frozen inventory first).

`.github/workflows/docs-hugo.yml` validates both URL shapes and uploads
`docs-pages.tar.gz` and `docs-standalone.tar.gz`, each with a SHA256 file.
These artifacts contain **documentation only**, not the signed yum repository.
A standalone bundle must be built for its actual public URL and served by an
HTTP server with directory indexes (`index.html`); it is not a `file://` bundle.
No rewrite rules or third-party assets are needed. Search is local to the bundle.

## Production publishing

`pages.yml` is the only workflow allowed to publish production Pages. It builds
and checks Hugo before assembling the signed yum repository, then uploads both
as **one** artifact. A final gate rejects missing RPMs, metadata, signature,
bootstrap repository configuration or public key. A standalone documentation
artifact must never replace this combined production artifact.

The proposed Hugo workflow becomes active only after the migration is merged.
Keep this distinction explicit when reporting a successful preview build.

## Release data and curated pages

`docs/_data/releases.yml` and `docs/_data/xoa_releases.yml` remain the committed
inputs written by the existing release publisher. **Do not move them at cutover.**
`build_docs.sh` stages a real copy under gitignored `site/data/`; symlinks outside
the Hugo source directory do not work reliably.

Homepage badges, ISO download/checksum/signature links, verification commands,
Features release details and release matrices render from those inputs. A build
reflects the input commit; it is not a browser-time query of GitHub. Previewing an
old branch can therefore show old release data. The staging workflow should use
current `main` release data and record both the source and data commit SHAs.

Per the explicit decision in #109, Known limitations and Roadmap remain curated.
The Roadmap identifies itself as an engineering backlog and carries a review
date. Refresh it when issues close; the linked GitHub list is the live status.
Do not imply that a package's inclusion in a matrix proves tested compatibility.

## Editing and translations

- Edit all three languages together; `check_translation_parity.py` checks
  structure and links, not linguistic quality.
- Keep existing heading IDs when renaming a section. Goldmark uses `{#id}`,
  not kramdown's `{: #id }`. Do not put shortcodes inside headings.
- Use `/docs/...` links for pages; Hextra resolves them for the current language
  and base path. French/Japanese alias values must explicitly include `/fr/`
  or `/ja/`; aliases are not automatically language-prefixed.
- `assets/legacy-home.json` records the old homepage fragments observed on
  production. The small `legacy-home` shortcode forwards them to Getting Started,
  with visible destination links as a no-JavaScript fallback. `layouts/alias.html`
  preserves fragments on old `.html` URLs; meta refresh alone drops them in Chromium.
- Installation photos are original assets from the author's blog, reused at the
  request in #133. Attribution and source revision are in
  `assets/images/install/README.md`. They illustrate upstream 8.3, not a verified
  run of the current XCP-hl installer.
- `architecture-{en,fr,ja}.svg` are local, accessible, translated diagrams.
- Hextra 0.12.3 overrides: `layouts/_partials/navbar.html` adds font controls;
  `language-switch.html` and `theme-toggle.html` preserve visible accessible
  names; `layouts/_shortcodes/hextra/feature-card.html` uses H2 after the hero H1.
  Compare these files with upstream when upgrading the theme. The font restore runs in the
  head script before paint. `custom/head-end.html` adds `hreflang` alternates.
- Core reading/navigation works without JavaScript. Theme/font preference,
  mobile menu, local search and automatic legacy-fragment forwarding use small
  local scripts. No external browser services or analytics are required.

## Evidence for the readiness changes

- `Vagrantin/xcp-hl@0f81b5b`: migrated site, screenshot assets and original content.
- `Vagrantin/xcp-hl@88b2574`: ISO release matrix includes `v8.3-ce38`.
- `Vagrantin/xoa-hl@6ca485d443a8bfd87c4142c9a66b3983bd158604`
  (`v5.113.2_e281c536-ce20`): `UPSTREAM_XO`, `patches/menu-hide-items.patch`,
  `patches/xoa-hl-update-api.patch`, `SOURCES/xoa-hl-update.sh`, and
  `docs/automatic-updates.md` substantiate the scoped XOA-hl descriptions.
- `Vagrantin/xolite-ce@e9234ed562b7df53c2dde87fd81ab249bbc20110/README.md`:
  deployment image choices and runtime image resolution.
- `Vagrantin/blog@b25cb75bd81a1f8f9f8ada4ead2fca5dcec2ff06/20260107/`:
  installation walkthrough and photographs.

Historical migration decisions remain in #60. They do not belong on the public
documentation landing page. Planned build/QA/contribution sections can be added
as real content becomes available; empty placeholders are not a release gate.
