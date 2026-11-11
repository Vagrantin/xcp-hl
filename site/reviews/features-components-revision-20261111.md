# Review of the features, components and xolite-ce revisions — 2026-11-11

Reviewer: Mistral Vibe (AI agent). Follows the pattern of
[es-de-eight-pages-20261111.md](es-de-eight-pages-20261111.md).
Source: `xcp-hl@main` at `8aeea1f`, plus the topic branch for this change.

## What changed (English)

Two documentation corrections, both folded in from existing owner work:

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
   The assessment decision record is added at
   `docs/developers/patching-model-assessment.md` and the Jekyll developer
   page is replaced by the owner's version.

## Translated pages affected

All four non-English locales carry both changes, keeping inline code,
commands, links, shortcodes, heading levels, table rows and code-fence counts
in step with English:

- `features.md` (fr, ja, es, de): signing-subkey row corrected.
- `components/_index.md` (fr, ja, es, de): subkey-roles row, build-pipeline
  listing and patch-at-source paragraph corrected.
- `components/xolite-ce.md` (fr, ja, es, de): rewritten to the unified-diff
  model, same section structure as English.

## Checks

`check_translation_parity.py` passes for all 152 translated pages
(38 x es/de/fr/ja). The strict manual review gate
(`check_xoa_manual.py --require-reviewed`) is unaffected: no XOA-HL manual
page was modified. No local Hugo build was run; hosted CI provides rendered
validation. The pending entries in
`reviews/owner-content-approval-20261110.json` now carry the exact current
body hashes of the twelve translated pages above.

This is an agent structural review, not a human signoff and not a translation
language review. The 2026-11-10 owner receipt does not extend to these new
revisions; each page needs maintainer review before the reviewed publication
gate that covers it. The previous `agentReview` records and hashes from the
eleven-page review of 2026-11-11 remain valid history for the states they
recorded.

## Reviewed body revisions (post-change)

- `site/content/fr/docs/features.md` — `sha256:519023a5e4125be06e87fd807ea7f868be3ccae74d06b8b478c0714a7275966b`
- `site/content/ja/docs/features.md` — `sha256:7b2cb7d4a2f97b6f733e3c9be827214fbe4e94816500b1ff423715bfd6e8a81e`
- `site/content/es/docs/features.md` — `sha256:9463f340e2cdf6dad327026c48bfe8462e6f9b2e5b3570c63ddb57726ca3f7be`
- `site/content/de/docs/features.md` — `sha256:b0c871c292aebccb52c0d2113e7ad781880a0f88e189147f6ccd0d3916c7c2a4`
- `site/content/fr/docs/components/_index.md` — `sha256:4d5dd61d14b33acf1e84e12f7c08e16e70843d81b03aca25988c8f56f10938fb`
- `site/content/ja/docs/components/_index.md` — `sha256:1ccd20a4bbaf832b1c3a1022f47d37870467b0f997b7679912445b53cf567f97`
- `site/content/es/docs/components/_index.md` — `sha256:c9e2edd5c4a9eb255206ab39929bf3e243eb881aef4e96558202b661e8b167db`
- `site/content/de/docs/components/_index.md` — `sha256:ca38854b10e3e031bdc20348b600b95d1194cb3d089c05dc3973f2ea8e86ca1c`
- `site/content/fr/docs/components/xolite-ce.md` — `sha256:4c3e28ada0150179d0d4690de581e734ce3465cce86bf135bb5a631f04a7dbb5`
- `site/content/ja/docs/components/xolite-ce.md` — `sha256:d7058fe5fc9e29634197876ff2a2d9f79a5bc68961ccffe3112699300e72a0f9`
- `site/content/es/docs/components/xolite-ce.md` — `sha256:539af098cd51d73105d6466fcacd83995f17ec576a17858281b8f3df2e27ca87`
- `site/content/de/docs/components/xolite-ce.md` — `sha256:f1690182867bd84bc2c430c4cfb1d863b037c419b2dc456080b0039d5e450ac8`
