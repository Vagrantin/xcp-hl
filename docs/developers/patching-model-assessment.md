---
layout: default
title: Patching model assessment
parent: Developers
nav_exclude: true
---

# Patching model assessment

Assessment for xcp-hl issues #43 and #16, dated 2026-10-30. The initial
assessment below is retained as history. The owner subsequently approved
unified diffs, shared maintenance rules first, and pinned provenance with
complete output comparison. This is not a compatibility statement. Issues
#53 and #54 remain excluded.

## Current source and ownership

The issue bodies and all comments were read before this assessment. Their
September counts and failure-mode descriptions are historical, not the
current source baseline:

- `xoa-hl` at `dc25ee0` applies unified diffs using `git apply --check`
  followed by `git apply`. `patches/series`, read through
  `scripts/list-patches.sh`, determines order for builds, validation and
  release notes. `patches/metadata.toml` documents purpose, upstream,
  ownership and dependencies. Evidence:
  `xoa-hl/scripts/build-xo.sh@dc25ee0`,
  `xoa-hl/scripts/list-patches.sh@dc25ee0`,
  `xoa-hl/scripts/validate-patches.sh@dc25ee0`,
  `xoa-hl/scripts/release-notes.sh@dc25ee0`.
- `xoa-hl/UPSTREAM_XO@dc25ee0` pins XO 5.113.2 at
  `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`. This assessment does not
  establish support for other XO versions.
- `xolite-ce` at `d452937` uses a mixed pipeline: a checked git patch for
  `XoaButton.vue`, locale and host/guest information scripts, deploy-secret cleanup, a
  replacement loader and the vendored
  `patches/xoa-deploy-patcher` executable for `xoa-deploy.vue`. The workflow
  separately checks source and distribution strings. Evidence:
  `xolite-ce/.github/workflows/build-xolite-ce.yml@d452937`,
  `xolite-ce/patches/update_locales.sh@d452937`,
  `xolite-ce/patches/update-login-locales.py@d452937`,
  `xolite-ce/patches/update-xolite-loader.sh@d452937`.
- `xolite-ce/UPSTREAM_TAG@d452937` pins `xo-lite-v0.21.0`. No other tag is
  claimed to work here.
- `xoa-deploy-patcher/src/main.rs@dbd7c88` contains 13 ordered static
  name/search/replace definitions. It checks that each anchor occurs exactly
  once in the evolving content, exits nonzero otherwise, and writes the
  target only after all transformations succeed. This is string replacement,
  not AST manipulation and not a silent missing-anchor no-op. Its source
  alone does not prove the provenance of XO Lite's vendored executable.

## #292 verification

The cleanup is already merged in xoa-hl PR #72 at `1acd8396`. Current
`xoa-hl/scripts/list-patches.sh@dc25ee0` requires numbered descriptive
filenames except three preserved contract names, and rejects incomplete or
duplicate series entries. `scripts/validate-patches.sh` additionally checks
unique numeric prefixes and dependency order. Regression coverage is in
`xoa-hl/tests/test-patch-order.py@dc25ee0`. No second rename is needed.

## Inconsistencies and safe work

There is no shared execution mechanism across the two components. XO Lite
already mixes diffs, file copies, locale merging and binary transformations;
XOA-HL has a centralized ordered diff series. A single format cannot be
adopted merely by renaming files. Evidence: the pipelines cited above.

XOA-HL's metadata `target` is descriptive free text, not a checked file
inventory. For example, `xoa-hl-update-api` declares only the server module
but its diff also changes web settings and reconnection code. Other entries
use directories, globs and abbreviated lists. Evidence:
`xoa-hl/patches/metadata.toml@dc25ee0` and the corresponding diff headers.
Correcting the incomplete API target description is safe without changing
its type, patch bytes, dependencies, application order or upstream pin.
A machine-readable target schema and exhaustive migration need agreement.

## Proposed standard for #43

Retain pinned upstream sources and reviewable patch payloads. Use one explicit
ordered series per consumer. Keep stable IDs and document purpose, owner,
upstream commit/version, dependency IDs and validation commands. Ordering
must be explicit, never inferred from repeated filename letters. Preserve
existing external contract paths.

Require validation of the entire series on its exact upstream pin, including
missing/duplicate/unlisted entries, dependency order, dry application,
feature assertions, locale contracts and existing tests. A rejected patch is
an upstream maintenance task, not permission to skip it or use fuzzy fallback.
Source application, packaged build and installed acceptance are separate
results. Do not claim version compatibility from metadata alone.

Keep payloads with their consumer and leave upstream-version changes as
separate reviewed changes. For XO Lite, preserve the local loader, image
selection, proxy routing and locale behavior during any migration.

## Decisions proposed in the initial assessment

1. **#16: external data or unified diffs for the deploy transformations?**
   Recommendation: use unified diffs in XO Lite for source edits, matching
   XOA-HL, with explicit copy/locale steps where needed. If editable TOML/JSON
   transformations are the product requirement, retain an exact-one-match
   engine with versioned external definitions instead. Either is feasible;
   selecting one is an architecture decision. Do not replace the shipped
   binary or switch the workflow until this is decided.
2. **#43: shared schema or shared rules with component-specific manifests?**
   Recommendation: adopt shared rules first. Preserve XOA-HL's existing
   metadata and series until a versioned schema handles ordered diffs,
   replacement assets and locale merges without maintaining two order lists.
3. **#16: how should executable provenance be established during migration?**
   Recommendation: pin the source revision and record artifact hashes, then
   compare old and new complete output on the exact XO Lite pin before any
   build switch. Successful source tests do not identify the vendored binary.

No decision here depends on resolving or changing #53 or #54. Neither issue
is acted on by this assessment.

## #16 source audit and migration acceptance

The source-location question is resolved by
`xoa-deploy-patcher/src/main.rs@dbd7c88`; there is no need to request a missing
source repository. The remaining choice is representation and distribution.
Current XO Lite also runs `cleanup-deploy-secrets.py` after the binary and
applies host/guest information scripts separately. A migration must compare
the complete pipeline output, not just one Vue file or the 13 definitions.
Evidence: `xolite-ce/.github/workflows/build-xolite-ce.yml@d452937`.

Before switching, require byte-for-byte output comparison on the current pin,
missing and duplicate anchor rejection without partial writes, repeated-apply
rejection, locale coverage, a hosted packaged build and installed acceptance.
A source-only audit cannot establish installed behavior. Preserve the existing
build path until the representation decision and acceptance evidence exist.

## Offline validation record

Run on the baselines above, with only the API target description changed in
XOA-HL. Logs are retained locally under
`/home/matth/devouille/xcp-ce/patching-review-evidence/`.

- #292: metadata validation, all ten naming/order regressions and the
  release-note fixture passed. The current series contains 26 patches.
- XOA-HL: `ci/check.sh` passed, including ShellCheck and update/locale tests.
  Additional Python tests for update integrity, package assets, glossary,
  assistant configuration and proposals passed. All 26 patches passed
  sequential `git apply --check` and application on pinned XO `e281c536`.
  Appearance, assistant read/UI, update API, runtime stamp, MCP probe,
  server syntax, translation audit and production locale compaction passed.
  The UI test initially lacked `linkedom`; it passed using a temporary
  installation outside the checkout. Two Python tests initially received
  an inappropriate source argument and passed when invoked correctly.
- XO Lite: `ci/check.sh` and the three upstream drift unit tests passed.
  All four pinned-source Python checks, host/guest Node tests, XOA button
  check, the complete source patch pipeline and deployment-secret test
  passed at tag `xo-lite-v0.21.0` (`13f987ff3`). A test harness initially
  supplied a relative deploy path from the wrong directory; rerunning with
  the correct path passed. The local loader contains no remote loader
  domain, and the deploy source retains the community image reference.
  The vendored executable passed pinned-source, missing-anchor,
  ambiguous-anchor and repeated-apply checks; failures preserved input bytes.
- Patcher source: Cargo format and Clippy passed. `cargo test --locked`
  passed with **zero tests**. The repo's nextest step could not run because
  `cargo-nextest` is absent; this is not a tested-engine coverage claim.
- XCP-HL: ShellCheck, repository contract and release-data checks passed.
  `ci/check.sh` stopped at missing `rpmspec`. The final key comparison was
  run separately and passed. XO Lite's RPM fixture stopped at missing
  `rpmbuild`. No local package build was performed.

ShellCheck was initially missing and was extracted into a temporary tools
directory under `/home/matth` before rerunning the component checks. A shared
glossary export against the separately pinned documentation repository,
full packaged builds and installed appliance behavior were not verified
locally. There is no appliance access. No deployment, release or manual
Jenkins build was started. Source checks do not establish installed acceptance.

## Accepted implementation direction

The owner accepted all three recommendations: unified diffs for XO Lite deploy
source edits, shared maintenance rules without a common schema migration, and
pinned source/artifact hashes with complete old/new output comparison.

The implementation belongs in `xolite-ce`, where the binary is consumed.
`xoa-deploy-patcher` remains historical source and is not changed or released.
The migration preserves the exact deploy payload and existing locale, loader,
host/guest and secret-cleanup transformations. It centralizes the source
pipeline so validation and packaged builds cannot choose different diff order.
Source equivalence is checked on the immutable XO Lite baseline, not inferred
for another upstream version. Rebuilding the pinned patcher in CI checks
behavioral correspondence; it does not claim historical binary reproducibility.

Installed acceptance remains unavailable. This does not block review of the
source-only refactor, and no appliance is deployed or release published here.

Implementation: [xolite-ce PR #26](https://github.com/Vagrantin/xolite-ce/pull/26),
`xolite-ce/scripts/patch-source.sh@7925dbc` and
`xolite-ce/docs/patching.md@7925dbc`. The offline complete-pipeline comparison
passed on pinned `13f987ff3`: all 3,639 files matched, including 23 changed
files, Git executable modes, symlink targets and robots.txt preparation.
The pinned source rebuild and patched Vue build are hosted CI checks. The
first comparator reported a group-write permission difference on an otherwise
identical file; Git file modes now avoid local-umask dependence.
