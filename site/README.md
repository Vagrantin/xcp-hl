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

Before pushing a change that touches `content/` or the `[languages]` block,
run what CI runs — both catch silent breakage that renders fine:

```bash
python3 scripts/check_translation_parity.py                          # fr/ja still match en
hugo --gc --minify --printPathWarnings --destination ../_site_hugo   # no "Duplicate target paths"
python3 scripts/check_switcher.py ../_site_hugo
```

## Data staging

`content/en/docs/reference/release-matrix.md` reads `site.Data.releases` and
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
| `content/en/` | English pages. `_index.md` is the landing page; `docs/` is the manual. English has its own `contentDir` like every other language — see **Every language needs its own `contentDir`** below; that is not optional, and not just tidiness. |
| `content/fr/`, `content/ja/` | French and Japanese, same tree shape as `content/en/`. Hugo pairs a page with its translations by matching the path *below* each language's `contentDir`, so the three trees mirror each other; `translationKey` in the front matter states the same pairing explicitly. |
| `assets/css/custom.css` | Width override, font scale, lead paragraphs. Concatenated after the theme's CSS, so plain overrides win. |
| `assets/js/head/font-size.js` | Font size selector. Hextra glob-concatenates `js/head/*.js` into its render-blocking head script, which is what keeps the restore from flashing. |
| `assets/js/flexsearch.bundle.min.js` | Vendored search engine — see the note in `hugo.toml`. |
| `layouts/_partials/custom/font-size.html` | The selector's markup. |
| `layouts/_partials/navbar.html` | **The one theme file we fork.** Hextra has no navbar extension point. Read the header comment before upgrading Hextra. |
| `layouts/_shortcodes/release-matrix-*.html` | The release-matrix tables. See **Data staging** above for why these are shortcodes and not an inline `{{ range }}` in the Markdown. |
| `i18n/{en,fr,ja}.yaml` | UI strings this site adds on top of Hextra's own — including the release-matrix table headers, which is why the same shortcode above serves every language. |
| `scripts/check_translation_parity.py` | CI check: asserts every `content/fr` and `content/ja` page still has the same headings, shortcodes, code fences, table rows and link targets as its `content/en` counterpart. Runs on the sources: `python3 site/scripts/check_translation_parity.py`. |
| `scripts/check_switcher.py` | CI check: asserts that on every built page, each language-switcher entry resolves to that same page in that language. Run it on a build, not on the sources: `python3 site/scripts/check_switcher.py _site_hugo`. |

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

**Diff the migrated page against its Jekyll original — the migration can
drop content silently.** `content/en/docs/reference/changelog.md` came out of
phase 2 with five of its nine entries missing, the August and July 2026 months
gone entirely, and the surviving text cut mid-word around a literal `...` line
(`Because Packe` / `...` / `dies with source versions`). Nothing failed: Hugo
built it, the link checker passed it (every link it still contained resolved),
and it went to the preview site that way. The French and Japanese migrations
carried all nine entries correctly, which is what eventually exposed it —
the translations were *ahead* of the English. Compare structure (heading
count, code fences, table rows, link count) between `docs/` and
`site/content/<lang>/` for every page before calling a migration done;
`scripts/check_translation_parity.py` does that between the three language
trees on every CI run, and is what would have caught this one — the fr and ja
changelogs were complete, so the English page was the outlier.

**A line break inside a CJK sentence renders as a visible space.** Markdown
joins wrapped source lines with a space, which is correct for languages that
separate words with one and wrong for Japanese: `変更が入ると\n考えてください`
renders as `変更が入ると 考えてください`. Goldmark's `eastAsianLineBreaks`
extension would suppress it globally, but it is not enabled here and only two
instances ever existed — wrap Japanese source lines at punctuation instead, and
check with a `CJK space CJK` grep over the built `ja/` HTML.

**A plain-ASCII slugify mangles accented and CJK text.** The first cut of
`slugify()` collapsed anything outside `[a-z0-9]` to a hyphen, which turns
"Clés GPG" into "cl-s-gpg" (the `é` treated as a separator, not kept) and CJK
headings into nothing at all. Goldmark's real behaviour keeps non-ASCII
letters; match it with `[^\w]+` under Python's Unicode-aware `\w` (the
default for `str` patterns), not an ASCII character class.

## Multilingual setup notes

- **Every language needs its own `contentDir` — including the default one.**
  This is the single most important line in `hugo.toml`'s `[languages]`
  block, and leaving it off `en` cost a real bug. A language with no
  `contentDir` falls back to `content/`, which is *the whole tree* — so with
  English at the root and `content/fr` / `content/ja` beneath it, English
  also built every French and Japanese page as an English page at that
  page's own URL. What that looked like:

  | Symptom | Why |
  |---|---|
  | The language switcher could not reach English, from any page in any language — including the English pages | Each page had 5 "translations", not 3: the 2 phantom English copies of the fr and ja pages joined `.AllTranslations`. Hextra's `utils/lang-link.html` assigns on every match, so the *last* `en` entry wins — the phantom English copy of the Japanese page. |
  | 72 `Duplicate target paths` warnings | `/fr/docs/…` etc. written twice, once by the phantom English page and once by the real French one. Which one survived depended on language `weight` ordering. |
  | `en.search-data.json` held 51 entries instead of 17 | French and Japanese text indexed as English. |
  | A shortcode embedding the English page's `.Content` hung the build forever, with no error | A genuine cycle: the English page set contained a copy of the French page, which was asking for the English page's rendered content. |

  Each of those reads like a separate Hugo or Hextra defect, and each was
  investigated as one. They were one line of config. **If translation
  linking, search or cross-page rendering misbehaves, check for overlapping
  `contentDir`s before blaming the framework** — `hugo --printPathWarnings`
  names it in one run, and the per-language page counts in the build summary
  should be roughly equal (here 31/29/29, not 77/29/29).
- **Path-based translation linking, `translationKey` set anyway.** With the
  trees disjoint, Hugo pairs `content/en/docs/x.md` with
  `content/fr/docs/x.md` automatically by matching the path below each
  `contentDir`; no `translationKey` is required. Every page sets one
  regardless — it is one fewer thing to get subtly wrong if a page ever
  moves, and it makes the pairing explicit and grep-able. Set it on English
  pages too, not only the translations. Note it is *not* a workaround for
  the `contentDir` bug above and does not mask it: with overlapping trees a
  `translationKey` made things worse, by pulling the phantom pages into
  `.AllTranslations` that path matching had ignored.
- **`site.Data` is global, not per-language.** The release-matrix shortcodes
  read the same `site.Data.releases` regardless of which language's page
  calls them — release data doesn't need translating, only the page text
  around it does (see the i18n table-header keys above).
- **No automatic `hreflang` alternates.** The original plan's gap analysis
  expected Hugo's native multilingual mode to emit these for free; Hextra's
  head partial does not, in this version. Not fixed here — it is an SEO
  enhancement, not a functional gap — but worth knowing before assuming it
  is covered. (The earlier version of this note claimed the switcher itself
  was "verified in a browser". It had been spot-checked in one direction
  only, which is how the `contentDir` bug above survived to production
  preview. `scratchpad/check_switcher.py` now asserts, for all 57 built
  pages, that every entry points at that same page in that language.)
- **The secondary hero button is invisible in light mode, in every
  language.** Pre-existing since phase 1, only surfaced now because
  screenshots up to this point were all dark-mode. Hextra's
  `hero-button` shortcode hardcodes `hx:text-white` on every button
  regardless of style override; the phase-1 hero used
  `style="background: transparent; border: …"` for the secondary button,
  which leaves white-on-transparent over a light page. Fix: add
  `color: inherit;` to that inline style (done on all three `_index.md`
  hero sections) — verified with light-mode screenshots of all three.

## URL policy: pretty URLs + redirect stubs (question 2 on #60, resolved)

Decided: pretty URLs, with redirect stubs for the ~42 paths the old Jekyll
site published (14 pages × 3 languages, minus each language's home page,
which needed no alias — old and new both serve it at `/`, `/fr/`, `/ja/`).
Every migrated page's front matter carries an `aliases:` entry for its old
`.html` (or, for `release-matrix` and `developers/`, already-pretty) Jekyll
path; Hugo generates a small redirect page at that old path pointing at the
new one.

**The one thing to get right: `aliases` does NOT auto-prefix by language,
unlike every other URL Hugo computes.** Set `aliases: ["/features.html"]`
identically on the English, French and Japanese `features.md`, and all
three redirects land at the same un-prefixed `/features.html` — no error,
no warning, just the last-built language's version silently winning (here,
Japanese; verified: the generated file said `lang="ja"` regardless of which
language's page declared the alias). French and Japanese pages need the
prefix written into the alias value by hand: `aliases: ["/fr/features.html"]`,
`aliases: ["/ja/features.html"]`. English, the default language with no
`contentDir` prefix, does not.

Verified with a script that reads every generated alias file and confirms
both its `lang` attribute and its redirect target — all 36, correct
language, correct target — not just that the file exists.

## Translation-pending pages

For question 6 on #60 (updated by the requester after the original plan): a
page should not go out under a language's URL until it is actually
translated, but on a pre-production preview it should still be reachable —
clearly marked as pending, one click from the real content — instead of a
404, so reviewers can see what is missing. Currently unused (all pages are
fully translated in all three languages), but built and verified against a
temporary demo page before being kept as ready-to-use infrastructure.

To add one: create the thin stub —

```markdown
---
title: <your best translation of the English title>
translationKey: <same key as the English page, for the language switcher>
---

{{< translation-pending en="/docs/guides/the-page/" >}}
```

`en` is the English page's own path, given explicitly. Two different ways
of having the shortcode *discover* it instead — both more automatic, and
both tried first — turned out unreliable in this Hugo/Hextra combination:

- Embedding `$en.Content` inline (fetching the English page's rendered
  content and outputting it here) hung the build indefinitely, no error.
  Hugo's dependency graph does not safely handle a shortcode in page A
  pulling page B's fully-rendered `.Content` in every case.
- Finding the English page by filtering `.AllTranslations` on
  `.Language.Lang == "en"` silently returned the WRONG entries: debugged
  directly, of 5 `AllTranslations` entries for one 3-language page, 3
  reported `.Language.Lang == "en"` — including the French and Japanese
  pages themselves, identified by their own permalinks. That field does not
  reliably reflect each translation's actual language here.

An explicit path sidesteps both: `relURL` is a plain string operation, no
cross-page `Page` object involved, nothing to hang or misreport.
`layouts/_shortcodes/translation-pending.html` has the full account.

Gating the actual *production* deploy on every page having all three
languages complete is a CI/process decision for phase 5, once a real
deploy pipeline exists to gate — nothing to build in Hugo itself for that
half of the policy.
