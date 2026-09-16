# XCP-hl documentation site (Hugo)

The Hugo replacement for the Jekyll/just-the-docs site under `docs/`
([#60](https://github.com/Vagrantin/xcp-hl/issues/60)). All English, French
and Japanese content is migrated (phases 2–3).

**This site is not published yet.** `docs/` is still what
<https://vagrantin.github.io/xcp-hl/> serves. CI builds this one to an artifact
so it can be reviewed; the cutover is Phase 5.

It lives in `site/` rather than `docs/` on purpose: Jekyll builds everything
under `docs/`, and it would try to Liquid-parse the Hextra shortcodes in
`content/` (`{{< callout >}}` is a Liquid syntax error) and fail the live Pages
deploy. The directory moves at cutover, when there is no Jekyll left to trip.

## Build it locally

Hugo **extended** ≥ 0.146 and Go (the theme is a Hugo Module, which is a Go
module) are the only requirements — no Ruby, no Node, no `npm install`.

The release matrix pages need `data/releases.yml` and `data/xoa_releases.yml`,
staged from `docs/_data/` (not checked in — see **Data staging** below):

```bash
mkdir -p data && cp ../docs/_data/*.yml data/

hugo server            # http://localhost:1313/xcp-hl/
hugo --gc --minify     # one-shot build into site/public/
```

The version CI pins is in `.github/workflows/docs-hugo.yml`.

## Data staging

`content/docs/reference/release-matrix.md` reads `site.Data.releases` and
`site.Data.xoa_releases`, which Hugo loads from `data/*.yml` — but that
directory is gitignored, not checked in. The one committed copy is
`docs/_data/*.yml` (kept current by `xcp-build-agent` after every ISO build,
same as it always has for the live Jekyll site), and CI copies it into
`data/` immediately before `hugo` runs (`.github/workflows/docs-hugo.yml`,
step **Sync release-matrix data**).

This is a real copy, not a symlink, and not `os.ReadFile` reaching across:
Hugo's data loader and `os.ReadFile` both refuse to read outside the working
directory. A `data/releases.yml → ../docs/_data/releases.yml` symlink and an
`os.ReadFile "../docs/_data/releases.yml"` were both tried and both silently
resolve to nothing — no error, just an empty `site.Data.releases`, which is
why the two release-matrix shortcodes (`layouts/_shortcodes/release-matrix-*.html`)
open with an explicit `errorf` if the data is missing, rather than rendering
a quietly-empty table.

At cutover, `docs/_data/` moves under `site/` and this staging step goes
away — see `.github/workflows/docs-hugo.yml`'s header comment.

## Layout

| Path | What it is |
|---|---|
| `hugo.toml` | Site config: languages, menus, theme params. The URL-policy decision (question 2 on #60) is marked in comments. |
| `content/` | English pages, at the content root (the default language has no `contentDir` prefix). `_index.md` is the landing page; `docs/` is the manual. |
| `content/fr/`, `content/ja/` | French and Japanese, same tree shape as `content/`. Every page shares a `translationKey` with its English counterpart — that is what makes the language switcher land on the *same page*, not the other language's home page. |
| `assets/css/custom.css` | Width override, font scale, lead paragraphs. Concatenated after the theme's CSS, so plain overrides win. |
| `assets/js/head/font-size.js` | Font size selector. Hextra glob-concatenates `js/head/*.js` into its render-blocking head script, which is what keeps the restore from flashing. |
| `assets/js/flexsearch.bundle.min.js` | Vendored search engine — see the note in `hugo.toml`. |
| `layouts/_partials/custom/font-size.html` | The selector's markup. |
| `layouts/_partials/navbar.html` | **The one theme file we fork.** Hextra has no navbar extension point. Read the header comment before upgrading Hextra. |
| `layouts/_shortcodes/release-matrix-*.html` | The release-matrix tables. See **Data staging** above for why these are shortcodes and not an inline `{{ range }}` in the Markdown. |
| `i18n/{en,fr,ja}.yaml` | UI strings this site adds on top of Hextra's own — including the release-matrix table headers, which is why the same shortcode above serves every language. |

## Upgrading Hextra

```bash
hugo mod get -u github.com/imfing/hextra
```

Then diff `layouts/_partials/navbar.html` against the theme's copy and re-apply
the one marked branch. Nothing else here is a fork.

## Migrating a page from `docs/`

The content is portable Markdown; what changes is the Just the Docs markup.

| Jekyll / kramdown | Hugo / Hextra |
|---|---|
| `nav_order: N` | `weight: N` |
| `has_children: true` | the page becomes `_index.md` in its own directory |
| `parent:` / `grand_parent:` | directory nesting |
| `permalink: /x/` | `url: /x/` |
| `1. TOC` + `{:toc}`, `{: .no_toc }` | delete — the right-hand rail is automatic |
| `{: .note }` / `{: .warning }` / `{: .important }` | `{{< callout type="info" \| "warning" \| "error" >}}…{{< /callout >}}` |
| `{: .fs-6 .fw-300 }` | `{class="lead"}` |
| `{: .label .label-blue }` | `{{< badge >}}` (Hextra ships one) |
| `{: .btn .btn-primary }` | `{{< hextra/hero-button >}}` or `{{< cards >}}` |
| `{: .d-inline-flex }` + `Label\n{: .label .label-COLOR }` | `{{< badge content="Label" color="COLOR" >}}` inline on the heading — see below |
| `{% for r in site.data.releases %}…{% endfor %}` | a dedicated shortcode — see **Data staging** above, NOT an inline `{{ range }}` |
| **`{: #explicit-anchor }`** | **`{#explicit-anchor}`** — see below |
| internal link, any form (`/x/`, `x.html`, `x`, `#frag`) | absolute page path, `/docs/section/page` (+`#frag`) — see below |

### Explicit anchors need converting, not copying

The plan on #60 says these carry over verbatim. They do not. Goldmark's
attribute syntax has no leading colon, and the mismatch fails *silently*:
`{: #iso-storage }` is emitted as literal text into the page body and the
heading falls back to its auto-generated slug, so the deep link breaks without
the build saying a word. Drop the colon:

```markdown
### ISO storage {#iso-storage}
```

There are ~15 of these across the tree and they are live deep links. Grep for
`{: #` before declaring a page migrated.

### A shortcode inside a heading breaks two things, not one — keep it off the heading line

Found converting the roadmap's status badges. Goldmark computes a heading's
auto-slug — *and* the visible label in the sidebar ToC — from its raw source
text, which at that point still contains Hugo's internal placeholder for the
not-yet-rendered shortcode. `### GPG keys {{< badge content="Security"
color="red" >}}` slugs to `gpg-keys-hahahugoshortcode15s1hbhb...`, and the
sidebar literally reads "GPG keys HAHAHUGOSHORTCODE15s1HBHB" (verified with a
screenshot before this was caught — see the phase-3 commit). An explicit
`{#id}` fixes the anchor but **not** the sidebar label, since both read from
the same polluted source text. There is no shortcode-only fix: put the badge
on its own line below the heading instead —

```markdown
### GPG keys {#gpg-keys}

{{< badge content="Security" color="red" >}}
```

— and give the heading its own explicit id regardless (see above): the slug
this computes from the heading text alone is a Goldmark-vs-kramdown
reimplementation (`slugify()` in the conversion tooling), not the real thing,
so treat it as a best-effort match to verify, not a guarantee.

### Internal links are absolute page paths, not relative Jekyll ones

Every Jekyll-era internal link form — `/release-matrix/`, `features.html`,
a bare `xoa-hl` relative to the current directory — becomes one shape:
an absolute path from the content root, e.g. `/docs/components/xoa-hl`,
`/docs/reference/release-matrix#xoa-hl-releases`. Hextra ships a `render-link`
hook (`layouts/_markup/render-link.html`, not forked here) that resolves any
link starting with `/` through `GetPage` and swaps in that page's real
`RelPermalink` — so it survives a `baseURL` change, a language prefix, or a
move to pretty vs. ugly URLs without the link text changing. This only
applies to real Markdown links; a `link` param on a shortcode (`{{< card >}}`,
`{{< hextra/hero-button >}}`) is not run through it and stays relative to the
current page, browser-style.

## Migrating a translation from `docs/fr/` or `docs/ja/`

Same table as above, plus two things specific to a second language.

**Explicit anchors are the same literal string in every language** — the
original translator kept `{: #iso-storage }` etc. unchanged in `docs/fr/` and
`docs/ja/`, so `convert_anchors()` needs no per-language table for those.
**Auto-generated slugs are not**: they come from the (translated) heading
text, so a badge heading's computed slug differs by language and any
cross-reference to it has to point at that language's own slug — building
`gpg-keys-one-signing-key-per-module` (from the English heading) into the
French page is wrong; the French heading slugs to
`clés-gpg-une-clé-de-signature-par-module`. Verify after building, per
language, rather than assuming a shared table.

**A plain-ASCII slugify mangles accented and CJK text.** The first cut of
`slugify()` collapsed anything outside `[a-z0-9]` to a hyphen, which turns
"Clés GPG" into "cl-s-gpg" (the `é` treated as a separator, not kept) and CJK
headings into nothing at all. Goldmark's real behaviour keeps non-ASCII
letters; match it with `[^\w]+` under Python's Unicode-aware `\w` (the
default for `str` patterns), not an ASCII character class.

## Multilingual setup notes

- **Path-based translation linking, `translationKey` used anyway.** Hugo
  links `content/docs/x.md` and `content/fr/docs/x.md` as translations of
  each other by matching path automatically, no `translationKey` required —
  but every page here sets one regardless, for two reasons: it is one fewer
  thing to get subtly wrong if a page ever moves, and it makes the link
  explicit and grep-able. Every English page needs one even where the
  English content came first and looks "canonical" — a page missing one
  (caught on four pages: the home page and the three section `_index.md`
  files that predate fr/ja) silently falls out of the language switcher for
  its translations.
- **`site.Data` is global, not per-language.** The release-matrix shortcodes
  read the same `site.Data.releases` regardless of which language's page
  calls them — release data doesn't need translating, only the page text
  around it does (see the i18n table-header keys above).
- **No automatic `hreflang` alternates.** The original plan's gap analysis
  expected Hugo's native multilingual mode to emit these for free; Hextra's
  head partial does not, in this version. Not fixed here — it is an SEO
  enhancement, not a functional gap (the language switcher itself works;
  verified in a browser that it lands on the translated page, not the other
  language's home page) — but worth knowing before assuming it is covered.
- **The secondary hero button is invisible in light mode, in every
  language.** Pre-existing since phase 1, only surfaced now because
  screenshots up to this point were all dark-mode. Hextra's
  `hero-button` shortcode hardcodes `hx:text-white` on every button
  regardless of style override; the phase-1 hero used
  `style="background: transparent; border: …"` for the secondary button,
  which leaves white-on-transparent over a light page. Fix: add
  `color: inherit;` to that inline style (done on all three `_index.md`
  hero sections) — verified with light-mode screenshots of all three.
