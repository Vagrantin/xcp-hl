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
  separate competing glossary. Merged `xoa-hl` PR #34 now consumes its immutable
  export in translation CI; human UI terminology review remains pending in D6.
- Required manual pages declare `glossaryTerms` as a JSON array of stable IDs.
  The checker validates those controlled IDs, not every natural-language word.
- `translationStatus` is `source` for English and `draft` or `reviewed` for a
  translation. Never infer human review from a successful structure check.
- A `reviewed` claim also requires the page/locale record in
  `data/xoa_manual_reviews.json`, binding named technical/language reviewers,
  date and a GitHub review URL to both the current English source hash and the
  translated body/localized declared-term hash. Missing/invalid records block
  preview as well as reviewed publication. No real reviews are recorded yet.
- `sourceRevision` is `sha256:` followed by the digest of the normalized English
  body plus the English glossary entries declared by that page. Front matter,
  unrelated Git commits and translated text do not enter this digest. Changes to
  English glossary definitions invalidate affected translations.
- `check_xoa_manual.py` validates required pages, terms and revisions and creates
  ignored `site/data/xoa_manual_status.json` for the reader-visible status page.
  It reports stale translations as a CI failure. Drafts may be previewed;
  `--require-reviewed` rejects drafts before a reviewed production publication.
- `build_docs.sh` runs that gate when `XOA_PUBLICATION_MODE=reviewed`; default
  previews retain draft labels. It writes the complete pending review queue and
  all freshness failures, which CI uploads. The publishing/correction process
  and shared glossary consumer format are defined in `TRANSLATION-REVIEW.md`.
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
| First login, VM and full NFS backup/isolated restore | `content/*/docs/xoa-hl/{first-login,create-vm,backup-restore}.md` | Source-reviewed preview in EN/FR/JA; lab acceptance pending |
| Daily administration/protection | `content/*/docs/xoa-hl/{vm-operations,storage-networks,hosts-pools,permissions}.md` | Source-reviewed EN/FR/JA preview; full D0 feature inventory and D3 lab acceptance pending |
| CPU/memory changes and destructive VM removal | `content/*/docs/xoa-hl/vm-operations.md` | VM03/VM11 source-reviewed stopped-test-VM previews; ordered limits, restart/force handling and partial-cleanup boundaries; lab/language acceptance pending |
| Same-pool VM migration and halted XVA transfer | `content/*/docs/xoa-hl/vm-transfer.md` | VM08/VM10 source-reviewed previews from merged #221; guest continuity, import isolation and failed-transfer lab acceptance pending |
| NFS ISO library connection and rescan | `content/*/docs/xoa-hl/storage-networks.md` | SN02 source-reviewed dedicated-export pilot; host access/media readback, provisioning and upload acceptance pending |
| Maintenance, configuration export and troubleshooting | `content/*/docs/xoa-hl/{maintenance,configuration-backup,troubleshooting}.md` | Source-reviewed preview; recovery/rollback and interruptions require lab acceptance (D4 #199) |
| Concepts, configuration and automation reference | `content/*/docs/xoa-hl/{concepts,configuration,automation}.md` | Source-reviewed EN/FR/JA preview and pinned CLI fixture; real-appliance acceptance pending (D5 #200) |
| Local-account OTP sign-in and removal | `content/*/docs/xoa-hl/sign-in-otp.md` | SE04 source-reviewed preview; all valid tokens bypass OTP; enrollment, removal/recovery and installed UI acceptance pending |
| Local groups and additive ACLs | `content/*/docs/xoa-hl/permissions.md` | SE01 source-reviewed Viewer/membership/revocation pilot; independent member/nonmember and partial-write acceptance pending |
| Full translation review and UI glossary reuse | D6 #201 | Revision-bound review gate/export and UI workflow consumer delivered; reviewer assignments and human review pending |
| Ranked task search and deployed usability | D7 #202 | Browser/Lighthouse, keyboard and enlarged-layout checks; human usability and appliance acceptance pending |

Evidence baseline: the source paths above at
`xcp-hl@5570376049d1128c39675ae1426bb40c4e19002a`; packaging/update references at
`xoa-hl/README.md` and `xoa-hl/docs/automatic-updates.md` at
`e1faaaddbfd30eba4f6152920d7f7697c6947417`. These are source observations,
not a record of disposable-appliance validation.

The review proposal in [XOA-FEATURE-INVENTORY.md](XOA-FEATURE-INVENTORY.md) maps
57 task/boundary IDs to pinned source observations, current chapters, coverage
gaps and pending functional checks. It includes unresolved applicability rather
than inferring that undocumented features are absent. D0 #195 remains open for
approval of this scope, installed feature/release evidence, owners and locale
reviewers. D1 #196 tracks structure/deployment;
this batch does not claim that the full manual or appliance acceptance is done.

## Beginner batch and search checks (2026-10-11)

The documentation-only follow-up after #205 restores the first-login and VM
chapters, adds full NFS backup and isolated restore, and requires all three task
pages in the source checker. Release hashes, source pins, lab acceptance and
ownership gaps are recorded in `XOA-BEGINNER-VALIDATION.md`. It does not reinstate
the reverted Jenkins/capture code or `XOA-SCREENSHOTS.md` runbook.

`assets/js/flexsearch.js` overrides Hextra 0.12.3's search client, retaining its
index/DOM contracts and MIT license in `assets/js/HEXTRA-LICENSE`. Normalized
literal title phrases rank before character-token suggestions; `input` and
`compositionend` events handle paste and Japanese IME input. Browser CI checks
VM, backup and update queries against the actual chapter in each locale and
rejects mixed-language results. Compare this override when upgrading Hextra.

The complete manual, semantic language review and appliance acceptance remain
open. D1 was delivered by #203; this batch advances D0, D2, D6 and D7 without
closing those work packages.

## Appliance operations batch (D4 #199)

Maintenance, configuration export and isolated import preparation, troubleshooting
and problem reporting are now present in EN/FR/JA. `XOA-MAINTENANCE-VALIDATION.md`
records the released baseline, source findings and outstanding lab acceptance.
The canonical update guide links these pages and no longer describes package
downgrade as verified appliance rollback. Search/browser/mobile checks cover the
new tasks; French/Japanese retain draft status until human review.

## Daily administration batch (D3 #198)

VM power/snapshots/stopped clone, disk/VIF management, host/pool ownership and
users/ACLs are available in EN/FR/JA. `XOA-DAILY-VALIDATION.md` records source pins,
#126 policy versus observed implementation, and outstanding acceptance. Existing
full NFS backup/isolated restore is linked instead of duplicated. Incremental
backup, replication, disaster recovery, HA, pool formation and cross-pool migration
remain outside the accepted pilot. Same-pool migration and XVA transfer previews
were added by #221; local-account OTP is covered by `sign-in-otp` and
[XOA-OTP-VALIDATION.md](XOA-OTP-VALIDATION.md). All new FR/JA translations remain draft.
