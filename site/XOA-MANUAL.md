# XOA-HL manual implementation (#189)

## Source and deployment

Documentation source lives in `Vagrantin/xcp-hl/site/`. The first implementation
branches from `claude/gracious-ride-99qg08` at
`5570376049d1128c39675ae1426bb40c4e19002a`. `Vagrantin/xcp-ce` is the deployment
repository; its workflow checks out an explicit `xcp-hl` ref. Its old local
`site/` copy is not authoritative. The requester confirmed this separation on
2026-10-09.

The new deployment is documentation only. Do not stage RPMs, `.repo` files or
`repodata`, including fake placeholder repositories. The old official
`xcp-hl/main` documentation/package deployment is outside this change. #60's
combined renderer/RPM cutover and #144 are not gates for publication in `xcp-ce`.
`site/CUTOVER.md` still describes that separate old-production renderer change.
Do not interpret its combined-artifact requirements as requirements here.

Until the Hugo tree is merged into main, edit public prose in this Hugo tree
only. Do not duplicate edits in Jekyll. Release data remains at `docs/_data/`;
the existing publishers still own it. Use the actual deployment base URL, not a
hardcoded assumption about the domain or project subpath.

## Editorial decisions

- Initial scope is the latest reviewed released appliance. Every procedural
  chapter states its tested application/image/package identities. Historical
  sources can be preserved by Git tags; parallel versioned URL trees are deferred.
- Canonical manual routes are `docs/xoa-hl/`, `fr/docs/xoa-hl/` and
  `ja/docs/xoa-hl/`, relative to the deployment base URL.
- Use English as the editorial source, with French and Japanese written in
  common virtualization terminology. Preserve literal commands and identifiers.
- Keep FlexSearch. D7 tests ranked results for Japanese and accented French
  queries when the corresponding task chapters exist. Engine changes need evidence.
- Capture screenshots when useful rather than for every step. Record product
  version and UI language, localize captions/alt text, and recapture only when
  relevant UI changes. Do not label existing upstream installer photos as XOA-HL
  appliance test evidence.
- `site/data/xoa_glossary.json` is the tracked, machine-readable term source.
  Hugo consumes it directly; #131 can consume the same file rather than create a
  separate competing glossary. That UI integration remains work in D6.
- Required manual pages declare `glossaryTerms` as a JSON array of stable IDs.
  The checker validates those controlled IDs, not every natural-language word.
- `translationStatus` is `source` for English and `draft` or `reviewed` for a
  translation. Never infer human review from a successful structure check.
- `sourceRevision` is `sha256:` followed by the digest of the normalized English
  body plus the English glossary entries declared by that page. Front matter,
  unrelated Git commits and translated text do not enter this digest. Changes to
  English glossary definitions invalidate affected translations.
- `check_xoa_manual.py` validates required pages, terms and revisions and creates
  ignored `site/data/xoa_manual_status.json` for the reader-visible status page.
  It reports stale translations as a CI failure. Drafts may be previewed;
  `--require-reviewed` rejects drafts before a reviewed production publication.
- Editing sourceRevision is a review action: update it only after checking the
  changed meaning against the translation. CI prints the expected revision but
  must not automatically stamp translations as current.

## Current inventory and remaining work

| Material | Source | State |
| --- | --- | --- |
| Deploy, connect host, architecture | `content/*/docs/start/_index.md` | Existing guide; link rather than duplicate |
| Host/appliance updates | `content/*/docs/guides/updates.md` | Existing guide; localized anchors preserved |
| Release identities | `content/*/docs/reference/release-matrix.md` and `docs/_data/` | Records shipped components, not proven compatibility |
| Component/build architecture | `content/*/docs/components/` | Existing contributor material |
| Manual entry, glossary, status | `content/*/docs/xoa-hl/` | Foundation batch; FR/JA explicitly draft |
| First login, host connection, language and first VM | `content/*/docs/xoa-hl/{first-login,create-vm}.md` | Source-checked preview; lab/screenshots and locale review pending |
| Independent backup and isolated restore | D2 #197 | Next beginner chapters; procedures and lab validation pending |
| Daily administration/protection | D3 #198 | Feature inventory and procedures pending |
| Recovery and failure runbooks | D4 #199 | Must verify recovery before claiming support |
| Automation/configuration reference | D5 #200 | Verify against released upstream pin |
| Full translation review and UI glossary reuse | D6 #201 | Reviewer assignments and review pending |
| Ranked task search and deployed usability | D7 #202 | Tests/acceptance to extend |

Evidence baseline: the source paths above at
`xcp-hl@5570376049d1128c39675ae1426bb40c4e19002a`; packaging/update references at
`xoa-hl/README.md` and `xoa-hl/docs/automatic-updates.md` at
`e1faaaddbfd30eba4f6152920d7f7697c6947417`. These are source observations,
not a record of disposable-appliance validation.

D0 #195 remains open for released-feature availability, installed release
identities, owners and locale reviewers. D1 #196 tracks structure/deployment;
this batch does not claim that the full manual or appliance acceptance is done.

The beginner batch adds required-page gates and EN/FR/JA VM search ranking,
FR/JA update ranking, mobile/no-JS tutorial checks and Lighthouse for both new
chapters. Backup search ranking remains deferred until its guide exists.
See [XOA-BEGINNER-VALIDATION.md](XOA-BEGINNER-VALIDATION.md) for the newer pinned
image/application evidence and the pending disposable-lab acceptance record.

The Jenkins appliance screenshot pilot is specified in
[XOA-SCREENSHOTS.md](XOA-SCREENSHOTS.md). Capture outputs require private review
before integration; Jenkins is not a new website deployment dependency.
