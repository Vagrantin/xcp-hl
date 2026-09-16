# XCP-hl documentation site (Hugo)

Phase 1 of [#60](https://github.com/Vagrantin/xcp-hl/issues/60): the Hugo
replacement for the Jekyll/just-the-docs site under `docs/`.

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

```bash
hugo server            # http://localhost:1313/xcp-hl/
hugo --gc --minify     # one-shot build into site/public/
```

The version CI pins is in `.github/workflows/docs-hugo.yml`.

## Layout

| Path | What it is |
|---|---|
| `hugo.toml` | Site config: languages, menus, theme params. The Phase 3 (fr/ja) and URL-policy decisions are marked in comments. |
| `content/` | The pages. `_index.md` is the landing page; `docs/` is the manual. |
| `assets/css/custom.css` | Width override, font scale, lead paragraphs. Concatenated after the theme's CSS, so plain overrides win. |
| `assets/js/head/font-size.js` | Font size selector. Hextra glob-concatenates `js/head/*.js` into its render-blocking head script, which is what keeps the restore from flashing. |
| `assets/js/flexsearch.bundle.min.js` | Vendored search engine — see the note in `hugo.toml`. |
| `layouts/_partials/custom/font-size.html` | The selector's markup. |
| `layouts/_partials/navbar.html` | **The one theme file we fork.** Hextra has no navbar extension point. Read the header comment before upgrading Hextra. |
| `i18n/en.yaml` | UI strings this site adds on top of Hextra's own. |

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
| `{: .d-inline-flex }` | delete |
| `{% for r in site.data.releases %}` | `{{ range .Site.Data.releases }}` |
| **`{: #explicit-anchor }`** | **`{#explicit-anchor}`** — see below |

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
