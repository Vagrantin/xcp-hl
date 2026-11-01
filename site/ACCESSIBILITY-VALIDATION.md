# Keyboard and enlarged-layout evidence (#189 / D7 #202)

This documentation-only batch follows merged #210 at
`2f51fc2dede3b5b5f8861b7073968102548e598a`. Its docs-only deployment succeeded in
[xcp-ce run 37934948601](https://github.com/Vagrantin/xcp-ce/actions/runs/37934948601)
(build job 114469232993, deploy job 114469324507). The build log records that
exact merge SHA. All nine EN/FR/JA concepts/configuration/automation endpoints
at <https://xcp-hl.net/> were checked for the ce38 image/package scope.

## Regressions addressed

- Text-size controls retain localized descriptions and include the visible
  `A−`, `A` or `A+` in their accessible names. The previous French/Japanese
  descriptions failed Lighthouse's label-content-name-mismatch audit.
- The Hextra 0.12.3 breadcrumb override wraps full ancestor links and the current
  title rather than clipping them. Each ancestor has a minimum 24×24 CSS-pixel
  target; the previous 20px-high targets failed target-size on manual pages.
- The narrow navbar wraps controls and grows in height. The previous layout
  overflowed by 33px at 320 CSS pixels on the configuration-backup page in all
  three languages in the local browser fixture. No controls are removed.
  A ResizeObserver keeps Hextra's sidebar/TOC and heading offsets in sync with
  the actual navbar height; the enlarged mobile menu's focused input is checked
  for visibility below the header.
- Long headings and previous/next guide names wrap within their flex containers.
  At 390px and 200% root text, the configuration-backup heading previously
  expanded the document to 571px in the local fixture.

## Automated coverage

`site/scripts/browser_accessibility.cjs` runs in the standalone docs CI job,
using the same actual built site and pinned Playwright as the existing smoke
checks. It reaches controls through Tab rather than setting DOM focus, and
checks all three languages:

| Check | Evidence |
| --- | --- |
| Skip link | First Tab reaches the visible skip link; Enter follows its content anchor |
| Text size | Enter/Space increase size; maximum disables increase; reload preserves preference; keyboard reset restores default |
| Theme menu | Enter opens and focuses first option; ArrowDown moves focus; Escape closes and restores focus |
| Language menu | ArrowDown opens and focuses first language; End selects last; Escape restores toggle focus |
| Search | Ctrl+K focuses input; localized automation query, ArrowDown and Enter open the correct locale's guide |
| Mobile menu | At 320px, Enter moves focus into sidebar; Escape restores toggle; closed sidebar is excluded from subsequent Tab |
| Reflow | Homepage, Getting Started, manual index and 13 task/reference pages at 720 and 320 CSS pixels: no document overflow, clipped navbar/ancestor links or targets smaller than 24px |
| Text resize | Long-title configuration-backup page at 1440 and 390px with root text set to 200%: same layout checks |

The 720px viewport represents a 1440px window at 200% zoom; 320px represents
1280px at 400%. These are **CSS reflow equivalents**, not browser UI zoom or
pinch-zoom simulation. Root text resizing is a separate check; it scales the
site's rem-based typography, not every fixed-pixel icon. Wide tables, code and
the architecture diagram may scroll within their own containers. Document-level
overflow is rejected.

The existing browser suite still covers desktop/mobile light/dark layouts,
localized ranked search, preference persistence, legacy URLs and no-JavaScript
navigation. Lighthouse still audits 45 pages with a minimum 95 for performance
and accessibility. Its score is not a declaration of WCAG conformance.

The `docs-browser-evidence` CI artifact contains JSON Lighthouse reports,
`accessibility-interactions.json` with completed check names, and reflow/text
resize screenshots. Final run URLs and scores are recorded on the PR so they
refer to its final head, rather than requiring another commit after CI.

## Remaining acceptance

Screen-reader reading order/pronunciation, actual browser UI zoom, other browser
engines, forced-colors behavior and manual focus/overlap review remain human
checks. The selected keyboard assertions do not prove every possible navigation
sequence is accessible. Released-appliance workflow validation, exhaustive
feature availability, chapter owners and human FR/JA review also remain open
in #195–#202. This batch does not change their draft status or claim appliance
testing, production cutover or full D7 completion.
