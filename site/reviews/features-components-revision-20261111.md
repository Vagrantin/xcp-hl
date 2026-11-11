# Review of the features, components and xolite-ce revisions, 2026-11-11

Reviewer: Mistral Vibe (AI agent). Follows the pattern of
[es-de-eight-pages-20261111.md](es-de-eight-pages-20261111.md).
Source: `xcp-hl@main` at `8aeea1f`, plus the topic branch for this change.

## What changed (English)

Three documentation corrections, all folded in from existing owner work:

1. The RPM signing subkey was listed as signing `xo-lite-community` and
   `xoa-proxy` only. It signs `xo-lite-ce`, `xoa-proxy` and `xcp-hl-release`
   (evidence: `SPECS` naming at the current xolite-ce head, `Name: xo-lite-ce`,
   and `rpmsign --addsign xcp-hl-release-*.rpm` in this repo's
   `.github/workflows/build-release-rpm.yml`). The `xo-lite-community` package
   name was also corrected in build-pipeline listings and the
   patch-at-source component is `xoa-deploy.vue`, not `DeployXoaView.vue`.

2. The xolite-ce pages described the removed Rust `xoa-deploy-patcher`
   executable, a local rpmbuild workflow and a stale CI sketch. They now carry
   the owner's PR #339 rewrite: unified diffs applied by
   `scripts/patch-source.sh`, ordered by `patches/series`, described in
   `patches/metadata.toml`, with CI-only builds and acceptance scope.
   A later pass moved that description into the present tense and cites the
   merged state instead of a pull-request head: `xolite-ce@ad43fa2` for
   `patches/`, `scripts/` and `docs/patching.md`, and PR #26 merged on
   2026-10-31 as `4506112` for the history paragraph. Installed acceptance is
   limited to what `xcp-hl/qa/ce52-acceptance/2026-11-09.md@7a51eb1` records:
   build `0.21.0-39.g54c289b` on one installed ce36 host, appliances deployed
   through the shipped `#/xoa-deploy` Custom URL flow. The assessment decision
   record is added at `docs/developers/patching-model-assessment.md` and the
   Jekyll developer page is replaced by the owner's version.

3. The signing-subkey sentence in the four translated `xoa-proxy` pages still
   said one subkey signed two RPMs. It now names `xo-lite-ce`, `xoa-proxy` and
   `xcp-hl-release`, matching the corrected English sentence.

## Translated pages affected

All four non-English locales carry the changes, keeping inline code,
commands, links, shortcodes, heading levels, table rows and code-fence counts
in step with English:

- `features.md` (fr, ja, es, de): signing-subkey row corrected.
- `components/_index.md` (fr, ja, es, de): subkey-roles row, build-pipeline
  listing and patch-at-source paragraph corrected.
- `components/xolite-ce.md` (fr, ja, es, de): rewritten to the unified-diff
  model in the present tense, same section structure as English.
- `components/xoa-proxy.md` (fr, ja, es, de): signing-subkey scope corrected
  to all three RPMs.

## Checks

`check_translation_parity.py` passes for all translated pages (38 x
es/de/fr/ja). The strict manual review gate
(`check_xoa_manual.py --require-reviewed`) is unaffected: no XOA-HL manual
page was modified. No local Hugo build was run; hosted CI provides rendered
validation. The pending entries in
`reviews/owner-content-approval-20261110.json` now carry the exact current
body hashes of the sixteen translated pages below.

This is an agent structural review, not a human signoff and not a translation
language review. The translations in this branch are agent-written and were
not reviewed by a human. The 2026-11-10 owner receipt does not extend to these
new revisions; each page needs maintainer review before the reviewed
publication gate that covers it. The previous `agentReview` records and hashes
from the eleven-page review of 2026-11-11 remain valid history for the states
they recorded.

## Reviewed body revisions (post-change)

- `site/content/fr/docs/features.md`: `sha256:519023a5e4125be06e87fd807ea7f868be3ccae74d06b8b478c0714a7275966b`
- `site/content/ja/docs/features.md`: `sha256:7b2cb7d4a2f97b6f733e3c9be827214fbe4e94816500b1ff423715bfd6e8a81e`
- `site/content/es/docs/features.md`: `sha256:9463f340e2cdf6dad327026c48bfe8462e6f9b2e5b3570c63ddb57726ca3f7be`
- `site/content/de/docs/features.md`: `sha256:b0c871c292aebccb52c0d2113e7ad781880a0f88e189147f6ccd0d3916c7c2a4`
- `site/content/fr/docs/components/_index.md`: `sha256:4d5dd61d14b33acf1e84e12f7c08e16e70843d81b03aca25988c8f56f10938fb`
- `site/content/ja/docs/components/_index.md`: `sha256:1ccd20a4bbaf832b1c3a1022f47d37870467b0f997b7679912445b53cf567f97`
- `site/content/es/docs/components/_index.md`: `sha256:c9e2edd5c4a9eb255206ab39929bf3e243eb881aef4e96558202b661e8b167db`
- `site/content/de/docs/components/_index.md`: `sha256:ca38854b10e3e031bdc20348b600b95d1194cb3d089c05dc3973f2ea8e86ca1c`
- `site/content/fr/docs/components/xolite-ce.md`: `sha256:e48ab6ae8f014c556a054a2930ea1c81b11b5c3053baee6c2bdbed97359e57ea`
- `site/content/ja/docs/components/xolite-ce.md`: `sha256:e019fed4ea40dd6aebc016818bc6893115e24c4f88f9c8b0fae01c078fef8038`
- `site/content/es/docs/components/xolite-ce.md`: `sha256:4c8f0d7edfc20fc7defed27ccfe4a9d4f7ead90e8eb14e841fe3a40ac01b64e6`
- `site/content/de/docs/components/xolite-ce.md`: `sha256:be8ffc234daab00e61660d54bfee230e055e7993768bdb4e7e0677e78464eacf`
- `site/content/fr/docs/components/xoa-proxy.md`: `sha256:79e37c16ce7e5186ac6d3f590a94272d40a204dcf0f27bd301189d76134e13f2`
- `site/content/ja/docs/components/xoa-proxy.md`: `sha256:f3a0073e483b0ceeeb5146d46a43136c911e8a8f26db50bf6b12e41181f94c8a`
- `site/content/es/docs/components/xoa-proxy.md`: `sha256:76f3bc094cbed84d3c2cab1b5bcb1447912b9320a831d7220bf6f4d8faf5a40a`
- `site/content/de/docs/components/xoa-proxy.md`: `sha256:b8740318cf12a4463c529ff6302bae33a6587b04b65662f01a750ab37957b717`
