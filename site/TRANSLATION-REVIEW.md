# XOA-HL translation review and publishing (#189 / D6 #201)

English is the editorial source. On 2026-10-23 all 40 French/Japanese manual
pages were approved at `a733d92` by Vagrantin, holding both the technical and the
language reviewer roles ([approval](https://github.com/Vagrantin/xcp-hl/issues/201#issuecomment-6361303818)).
`data/xoa_manual_reviews.json` records that approval per page and locale. CI
results and LLM drafts do not establish review.
The current `xcp-ce` deployment is a draft-aware preview. Its existing workflow
does not become a reviewed-publication workflow merely because this PR merges.

## Review a content change

1. Review the English instructions against the stated released image/package
   and pinned source. Keep appliance evidence separate from source/fixture
   evidence. Preserve command targets, permissions, identifiers and warnings.
2. Run the checker from the repository root:

   ```bash
   python3 site/scripts/check_xoa_manual.py --report /tmp/xoa-review-queue.json
   ```

   It exits nonzero on stale meaning or invalid review claims, reports **all**
   affected page/locale records, and still writes the JSON queue. Structural
   failures produce `fatalError`; they must be repaired before a complete queue
   can be generated. It never updates source hashes or review records.
3. Compare each affected English change with FR/JA. Update translated prose,
   literal commands, terminology and links together. Update a page's
   `sourceRevision` only after checking its meaning against the new English
   source. Set translations needing review to `draft`; keep old review records
   as evidence of their old revision until replacement review is completed.
4. A human technical reviewer checks the procedure/applicability; a human
   language reviewer checks terminology and meaning. Record their identities,
   date and the GitHub review/comment that states the approved scope. One person
   may perform both roles if that is explicitly recorded. Actual appliance tests
   still need their own release/installed-state evidence.
5. After both roles approve the exact content, set `translationStatus: reviewed`
   and add the record below under the page's stable `translationKey` and locale.
   Read its two hashes from the checked queue for that exact revision; do not
   automatically stamp every page or fabricate identities/approval evidence.
6. Run structure checks, the reviewed gate and both URL-shape builds. Inspect
   browser evidence and link final commit/run/artifact identities to #201/#189.

The manifest schema is version 1. This is an **illustrative record with
placeholders**, not an approval and not a file to copy unchanged:

```json
{
  "schemaVersion": 1,
  "reviews": {
    "PAGE_TRANSLATION_KEY": {
      "fr": {
        "sourceRevision": "sha256:ENGLISH_HASH_FROM_REVIEWED_QUEUE",
        "translationRevision": "sha256:TRANSLATED_HASH_FROM_REVIEWED_QUEUE",
        "technicalReviewer": "ACTUAL_REVIEWER_IDENTITY",
        "languageReviewer": "ACTUAL_REVIEWER_IDENTITY",
        "reviewedAt": "YYYY-MM-DD",
        "reviewUrl": "https://github.com/OWNER/REPO/pull/NUMBER#ACTUAL_REVIEW"
      }
    }
  }
}
```

`sourceRevision` retains the existing SHA-256 contract: normalized English body
and declared English glossary definitions. `translationRevision` uses the same
normalization with the translated body and that locale's declared glossary
definitions. Front matter, unrelated commits and undeclared terms are excluded.
A translated-text or localized-term change invalidates an old reviewed record,
even if the English hash is unchanged. Draft pages stay drafts even if a matching
record happens to exist. Unknown page/locale keys fail validation.

The checker verifies declared records and exact revision matches; it does not
authenticate identities or query whether a GitHub approval exists. PR review
must verify the linked decision. `reviewed` claims without records block preview
as well as reviewed publication. Invalid old records produce `stale`; missing
records produce `draft`. Neither is displayed as reviewed.

## Preview and reviewed publication

The default build mode remains `preview`, which permits current, labeled drafts
and rejects stale hashes or invalid reviewed claims. Reviewed publication uses
the **same build entry point**, with the gate inside it:

```bash
XOA_PUBLICATION_MODE=reviewed site/scripts/build_docs.sh https://docs.example.org/ /tmp/docs-reviewed
```

Use the actual deployment URL and a new output directory. Unknown modes fail.
All required manual FR/JA pages must be current and have matching human review
records; otherwise no bundle is produced. The standalone checker gate is:

```bash
python3 site/scripts/check_xoa_manual.py --require-reviewed --report /tmp/xoa-reviewed-gate.json
```

Since the 2026-10-23 records it passes; any stale or draft page fails it again. Do not point a reviewed deployment at
a preview artifact. A future `xcp-ce` publication change must explicitly invoke
`XOA_PUBLICATION_MODE=reviewed`, preserve its docs-only guards and record the
selected source commit, bundle checksum, checks and live URL verification.
This does not modify the old `xcp-hl/main` combined docs/RPM publisher.

CI uploads `xoa-review-queue-pages` and `xoa-review-queue-standalone`, including
failure reports, and `xoa-glossary-pages`/`xoa-glossary-standalone`. Queue schema 1
contains `pages`, pending `reviewQueue` entries and all `problems`; structural
errors instead contain `fatalError`. Drafts are pending review, not preview
errors. Failed checks still exit nonzero. Generated status/queue/export files
are ignored; only actual review records and the shared glossary are committed.

## Urgent corrections

Generated changelog entries use one shared release-data source. Their headings,
status labels and explanations are localized, while linked pull request titles
remain in English in all three languages, as decided in #268. This exception
applies only to generated titles; curated prose still follows the usual review
process.

- Correct and technically review the English instruction immediately. Link the
  triggering defect and exact release applicability; do not preserve an unsafe
  instruction merely to keep its old hash.
- Prepare checked FR/JA draft corrections and mark affected pages `draft` until
  language review is completed. Do not copy English into localized pages or
  keep stale hashes to pass CI. The ordinary preview checks still apply.
- If a reviewed deployment needs a temporary translation exception, record an
  explicit publication decision in #201: affected page/locale IDs, source commit,
  reason, accountable owner, deadline and a completion issue. Publish only a
  separately identified draft-aware preview during that exception. The current
  strict gate has no whitelist or automatic bypass; never describe that bundle
  as reviewed publication. A scoped exception in a reviewed bundle would need a
  separate reviewed implementation before use.
- Finish human review, replace the affected records, rerun the reviewed build
  and verify deployment before closing the exception. Preserve its decision and
  correction history in Git/issues.

## Shared glossary for UI translation work (#131)

`data/xoa_glossary.json` remains the single controlled-term source. The consumer
export preserves stable IDs, EN/FR/JA labels/definitions and Unicode, sorted by
term ID. Its `glossaryRevision` hashes all locale content, so a Japanese term
change changes the export identity even when the English page hash is unchanged.

In a UI translation workflow, check out an explicitly reviewed `xcp-hl` commit,
record that commit alongside the artifact, then run:

```bash
python3 site/scripts/export_xoa_glossary.py --output /tmp/xoa-ui-glossary.json
```

Export schema 1 contains `source`, `glossaryRevision`, `locales` and `terms` with
`id`/`translations`. It is an editorial input for #131, **not** XO runtime message
IDs or an automatic replacement for the fork's locale files. Check the released
XO5 UI labels and reviewed terminology before applying a translation. The
component workflow consumer is delivered by merged
[xoa-hl PR #34](https://github.com/Vagrantin/xoa-hl/pull/34), merge
`9713bd7fc352444c693d0115fd53f8eec4c7e934`. Its patch/translation CI checks out
exact docs commit `4c66ea6e05cf98c11df86ce5e34d5b0415647a1c` and validates the
export content identity. The `xoa-ui-glossary-review` artifact supplies glossary
definitions, mapped original UI message literals, source identities and pending
EN/FR/JA review rows. Missing/undefined labels stay explicit; no UI catalog or
approval is generated. See the component's
[review runbook](https://github.com/Vagrantin/xoa-hl/blob/9713bd7fc352444c693d0115fd53f8eec4c7e934/docs/shared-glossary-review.md).
Full UI language review remains open.
Do not maintain a competing glossary or fetch an unpinned moving branch in UI CI.

## Owners and outstanding acceptance

No named assignments were provided; do not infer them from commit authors.

| Responsibility | Assignment | Tracking |
| --- | --- | --- |
| English technical/chapter review | Unassigned | #195, #197–#200 |
| French language review | Unassigned | #195, #201 |
| Japanese language review | Unassigned | #195, #201 |
| Glossary coordination with UI translators | Unassigned | #195, #201, #131 |
| Reviewed publication/urgent-correction owner | Unassigned | #195, #201 |

The 2026-10-23 page approvals do not assign the standing roles above. Named
owners, full agreed feature inventory/coverage, real-appliance acceptance and
human UI terminology review remain open. This runbook and offline evidence checks do not close those issues.

## Implementation evidence

This batch follows #211's merge `3eaf89326f1004ccd4a398a7883cf00d31da6267`.
Its [xcp-ce deployment](https://github.com/Vagrantin/xcp-ce/actions/runs/38144691698)
passed, recorded that exact source commit, and the EN/FR/JA configuration-backup
pages were checked live for the delivered accessibility fixes.

Regression tests cover English drift across multiple pages/locales, missing
review evidence, acceptance of matching synthetic records, translated-body and
localized-term edits, malformed manifest/identities, and a complete JSON queue
on a failed gate. Separate export tests check Unicode/stable IDs, revision
changes on localized meaning edits and rejection of incomplete terms. Test
reviewers and approval URLs are fixture data, never real review claims. The
tests reset their temporary copy to drafts, so they do not depend on real records.
Final-head CI/run/artifact evidence is recorded on the implementation PR.
