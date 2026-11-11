# Documentation cutover runbook (#60)

## Decision

The implementation can be reviewed and rehearsed, but replacing production needs
the gates below. A green documentation build proves neither a real ISO install
nor yum compatibility. Do not close #60 based on a placeholder repository test.
Since #190, the current `xcp-hl-release` repository URLs point to
`rpm.xcp-hl.org`. Older installed release packages can still use the Pages
`/repo/8.3/x86_64/` path. Test both client populations separately.

## Before merging the production switch

The first cutover includes the reviewed EN/FR/JA scope. Defer ES/DE PR #293
until after that publication; its approved content is not part of this first-cutover scope.
Vagrantin owns the publication decision and the exact-revision FR/JA technical
and language reviews. Assignment alone does not satisfy the reviewed gate.
Vagrantin requires completion of every task and mode in the 57-task
[feature inventory](XOA-FEATURE-INVENTORY.md) before this first cutover. For
each mode, record release-specific availability, the required documentation
and functional evidence, or evidence for an unavailable/outside-pin disposition.
No `Preview`, `Gap` or unresolved mode may be counted as complete. Review the
resulting EN/FR/JA changes at their exact revisions before publication.
Modes that need infrastructure not yet available (issues #350 to #360, priority
P3) may carry an explicit reader-facing "not tested in this release" boundary
with the release scope. They do not block this cutover or other issues.

1. Record the reviewed source SHA and current release-data SHA. Require both
   `Build Hugo docs (preview)` matrix jobs to pass for that exact source.
2. Deploy that SHA to the existing preview (`Vagrantin/xcp-ce`), with release
   data from current `xcp-hl/main`. Confirm English/French/Japanese navigation,
   search, theme and font persistence, the installation photos and diagram, and
   old `.html` URLs/bookmarked fragments on desktop and mobile.
   Repeat the mobile Lighthouse performance/accessibility checks against that
   deployed endpoint (at least 95 each). Local compressed-server results do not
   establish the latency or configuration of the deployed service.
3. Build and extract the standalone archive; serve it with a plain HTTP server.
   Verify the site at its configured URL without rewrite rules or external assets.
4. Beta ISO acceptance is waived by the owner on 2026-11-10
   ([receipt](https://github.com/Vagrantin/xcp-hl/pull/398#issuecomment-6759282510)).
   ce55 selection remains. The blog photos remain upstream illustrations; no
   ce36 result is ce55 acceptance. This waiver does not satisfy the independent
   deployed-site, signed-repository/client or non-infrastructure inventory gates.
5. Review `.github/workflows/pages.yml`: Hugo runs before legacy repository
   assembly; repository collection, createrepo options, signing and root assembly
   stay intact. Preserve `docs/_data/`, repository IDs and signing key names.
   Compare the current `SOURCES/xcp-hl.repo` and `pages/xcp-hl.repo` contracts.
6. Rehearse the **signed** combined artifact and a disposable XCP-ng 8.3 yum
   client with the legacy Pages repository URL against a staging endpoint.
   Separately verify a client with the current `rpm.xcp-hl.org` configuration.
   The `xcp-ce` docs preview does not establish either yum result.
7. Obtain the maintainer's go-ahead for the production replacement. Keep a known
   good Pages deployment/artifact and the pre-cutover commit available for rollback.

## URL and domain strategy

The first cutover replaces the renderer behind the existing production address,
`https://vagrantin.github.io/xcp-hl/`, and preserves the legacy
`/repo/8.3/x86_64/`, `/xcp-hl.repo` and `/xcp-ng-ce-public.asc` paths there.
Current installed release packages obtain repository metadata from
`rpm.xcp-hl.org`; the Pages paths still serve older installations.
The build uses `actions/configure-pages`' actual base URL.

`xcp-hl.net` currently belongs to the `xcp-ce` preview. Do not transfer its Pages
custom-domain setting or DNS in the renderer cutover. A later domain move needs
separate verification of the installed clients' old repository URL and every
legacy path after redirects. `xcp-hl.org` is not used by this change.

## Production acceptance (immediately after deployment)

- Confirm the Pages run succeeded for the reviewed commit.
- Check all three documentation languages and representative old redirects.
- Record the installed `xcp-hl-release` version and effective `xcp-hl-base`
  URL for each test client. Retrieve the repository metadata, detached signature
  and public key through both the legacy Pages URL and the current RPM URL,
  allowing redirects. Import the public key
  into a temporary GPG keyring, verify fingerprint
  `2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A`, and verify `repomd.xml.asc` against
  `repomd.xml`. HTTP 200 alone is insufficient.
- On disposable XCP-ng 8.3 hosts with the legacy and current repository
  configurations, run a fresh-cache metadata fetch and list the release package
  for each configuration:

  ```bash
  # Read-only package operations: no RPM installation or update.
  work=$(mktemp -d /var/tmp/xcp-hl-docs-check.XXXXXX)
  yum --disablerepo='*' --enablerepo=xcp-hl-base \
      --setopt=cachedir="$work/cache" --setopt=persistdir="$work/persist" \
      --setopt=xcp-hl-base.skip_if_unavailable=False makecache
  yum --disablerepo='*' --enablerepo=xcp-hl-base \
      --setopt=cachedir="$work/cache" --setopt=persistdir="$work/persist" \
      --setopt=xcp-hl-base.skip_if_unavailable=False \
      --showduplicates list available xcp-hl-release
  ```

  Require successful metadata/signature validation and a non-empty package list.
  `skip_if_unavailable=False` applies only to these isolated diagnostics so an
  outage cannot look like success. Do **not** change the installed `.repo` file:
  its normal `skip_if_unavailable=True`, `repo_gpgcheck=1` and `gpgcheck=0` are
  deliberate contracts. Keep both URL identities, logs and selected package
  versions in #60.

### Live evidence recorded 2026-11-11 (deployed main `8aeea1f`)

Read-only checks against the deployed site `https://www.xcp-hl.org/` (Pages
build of main `8aeea1f`, `Last-Modified` one minute after the merge commit) and
against the RPM host, plus a disposable XCP-ng 8.3 yum rehearsal of both client
configurations. Evidence index:
`/home/matth/ga-lab/beta-ce52-acceptance/cutover-browser-20261111/README.md`
(browser, switcher, legacy-URL, redirect, stale-address and RPM-availability
logs) and `/home/matth/ga-lab/beta-ce52-acceptance/cutover-yum-20261111/`
(`current-rpm-client.log`, `legacy-pages-client.log`). These are observations
only; no gate above is closed by them.

- Step 2 (deployed endpoint), partly satisfied. PASS: all 200 sitemap URLs
  return 200; 40 pages per language with the matching `html lang`; both
  language switchers offer the five published languages and land on the same
  page in that language (200 of 200 pages, 200 distinct targets all 200);
  mobile menu verified at 320, 390 and 767 px over eight combinations; 39
  legacy `docs/` paths resolve, 36 through alias stubs; no plain-HTTP
  subresource on any page; the served signing key is byte-identical to
  `xcp-ng-ce-public.asc@8aeea1f` and carries the documented fingerprint
  `2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A`. NOT satisfied: there is no
  recorded mobile Lighthouse score for the deployed endpoint, which step 2
  requires at 95 or better.
- Enforce HTTPS is ON for the Pages site and the chains were verified with
  certificate checks: `http://www.xcp-hl.org/` reaches https in one hop;
  `https://xcp-hl.org/` reaches `https://www.xcp-hl.org/` in one hop;
  `https://rpm.xcp-hl.org/xcp-hl.repo` returns 200 with no hop;
  `http://vagrantin.github.io/xcp-hl/` reaches https in one hop. One extra hop
  remains: `https://vagrantin.github.io/xcp-hl/` with a trailing slash still
  301s to `http://www.xcp-hl.org/` before HTTPS. Every other Pages path tested
  redirects straight to https.
- Plain-HTTP addresses emitted by production (new finding): all 200
  `rel=canonical` links and all 1200 hreflang alternates are
  `http://www.xcp-hl.org/...`, the sitemap entries are http, and all 36 alias
  stubs redirect client-side through http. The stubs are built by
  `site/layouts/alias.html@8aeea1f` from `.Permalink`. Candidate root cause:
  `.github/workflows/pages.yml:85` takes `DOCS_BASE_URL` from
  `steps.pages.outputs.base_url`.
- Step 6 (yum clients): the 2026-11-11 Test-host rehearsal passed metadata and
  signature validation for both client configurations (`makecache` and
  `list available xcp-hl-release` exit 0 on each). The legacy Pages client then
  downloaded `xcp-hl-release-0.0.5-5.g157727f.xcpng8.3.noarch.rpm` with 200 and
  read it with rpm 4.11. The current `rpm.xcp-hl.org` client instead got 404
  HTML for every package the signed metadata lists, on `xcp-hl`, `xolite-ce`
  and `xoa-proxy`, at both the flat and the versioned paths, while the legacy
  Pages copy serves the same filenames with 200. As published, the current
  RPM-domain population can verify metadata and list packages but has no
  downloadable payload.
- Stale addresses inside the published pages: 20 links to
  `https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc` (one
  https-to-https hop; from the three component and features pages in five
  languages plus the verify-iso shortcode) and 5 links that pointed at
  `https://vagrantin.github.io/blog/20260107/xcp-ng-first-install.html`
  (200 with no hop, but it named the Pages host). Per the owner decision of
  2026-11-11 the walkthrough was migrated onto this site, so those 5 links now
  cite `https://www.xcp-hl.org/blog/20260107/xcp-ng-first-install.html`,
  served by the production domain.

### Owner decisions recorded 2026-11-11

A read-only re-verification of the `#409` deploy (main `fd949ed`) resolved the
plain-HTTP finding above: entry points, canonicals, hreflang alternates,
sitemap locations, the key, support and repository links and all 36 alias
stubs are `https://www.xcp-hl.org/` on the deployed site; the served key is
byte-identical to `xcp-ng-ce-public.asc@fd949ed` and both `.repo` files keep
their stanza, `gpgcheck=0` and `repo_gpgcheck=1` contracts. Evidence index:
`/home/matth/ga-lab/beta-ce52-acceptance/live-https-reverify-20261111/README.md`.
One Pages-side item stays: `https://vagrantin.github.io/xcp-hl/` with a
trailing slash still 301s to `http://www.xcp-hl.org/` before HTTPS (GitHub
side, recorded here, not repo-fixable). The five start-page blog links
remain on `https://vagrantin.github.io/blog/20260107/xcp-ng-first-install.html`
until the migration below lands.

Owner decisions recorded the same day:

- Step 7 go-ahead: the owner recorded that the merge of #335 counted as the
  go-ahead for the production replacement. This closes the open step 7
  condition above; rollback material remains available through the pre-cutover
  commits and the Pages deploy history.
- Blog post: the owner chose to publish the author's install walkthrough from
  this site; a migration PR moves the five start-page links to
  `https://www.xcp-hl.org/blog/20260107/xcp-ng-first-install.html` with the
  personal post untouched.
- Jekyll source retention: the owner approved starting the deletion follow-up
  described above ("Delete it in a follow-up only after acceptance"),
  preserving `docs/_data/` and the legacy URL inventory. A separate PR
  retires the tree; this paragraph is its start condition.

## Rollback

If Pages signed metadata or legacy yum acceptance fails, restore the previous
complete Pages artifact, or revert only the renderer-switch commit and rerun the
production workflow. Restore **both docs and the legacy repository together**,
never a docs-only archive. A current RPM-domain failure needs investigation in
that repository's publishing path; a Pages rollback does not repair it.
Preserve current `docs/_data/` updates and signing inputs. No DNS rollback is
needed because this cutover does not move the domain. Recheck metadata and yum
after rollback before reporting recovery.

The old Jekyll source is retained as an audit/rollback reference for this first
cutover. It is no longer rendered by the proposed production workflow. Delete it
in a follow-up only after acceptance, preserving `docs/_data/` and the legacy URL
inventory. #60 and #19 can be closed after the production evidence is recorded;
#133 can be closed once its content changes land in the accepted site.

## Historical integration candidate, 2026-10-28

The integration branch starts from the merged Hugo source at
`6d884fcb27ffb31dcea5bfbd65deafbd8d7f7eba` and merges current main at
`f4f82a4601fb07c94ea211952403f45e482c19d1`.
Main's release data, package workflows, repository settings and screenshot
requests are preserved. The changelog conflict uses main's version. The Pages
workflow retains Hugo plus the current legacy repository notice and explicitly
sets `XOA_PUBLICATION_MODE=reviewed` before any combined artifact is assembled.

The [Phase 1 review packet](reviews/xoa-phase1-20261028.md) covers 18 pending
FR/JA records. It is a pre-check, not approval. PR #334 is a separate D3 change;
refresh the packet and integration branch if it lands before cutover.
Historical branch references in validation records identify past evidence and
stay unchanged. No active xcp-ce publisher ref is switched in this PR.
The updated legacy container anchor is retained in all three Hugo feature pages.
Its status follows #7: dedicated Docker VM work remains draft and unreleased.
The old appliance-local feature claim is not repeated. Repository bootstrap
addresses in the three Hugo update guides follow main and #190.

Keep the integration PR unmerged. Before the maintainer merges it, merge the
then-current main again, preserve any new release data and screenshot work,
rerun exact-head CI and the strict review gate, and satisfy the acceptance
steps above. This branch does not authorize deployment or a domain move.

## Refreshed integration, 2026-11-10

PR #335 retains its original history and incorporates Hugo source
`5311270b22c786cc82bf902c970b8181e7f460e1`, current main including #398
(`506ec8255801decae04006522658e8f93c42ea11`), and the #347/#348 decision commits
`9a2331f9e4fd0e490fbd8462d28fdd33178e7978` and
`94deb0a6a49f33cdd8cf28c5551b39e86d7a9375`. Release data stays in `docs/_data/`;
package/repository/signing contracts and main's source pages are retained.
The current EN/FR/JA repair content from #394/#395 and ce52 limitations from
#398 are adapted to Hugo URLs/callouts, without changing their tested scope.

The owner explicitly authorized this integration and approved current content
and all languages in [the revision-bound receipt](https://github.com/Vagrantin/xcp-hl/pull/398#issuecomment-6759282510).
Vagrantin holds technical and language roles. Current manual review records carry
matching hashes, date and receipt URL; the broader source snapshot record is
[owner-content-approval-20261110.json](reviews/owner-content-approval-20261110.json).
The 2026-10-28 packet is historical, not a current absence-of-signoff gate.
Approval does not create a second reviewer, functional evidence or a campaign date.
ES/DE PR #293 remains deferred until after the first EN/FR/JA cutover.

Current independent evidence disposition:

| Requirement | Evidence / remaining boundary |
| --- | --- |
| Exact integration builds, rendered links/aliases, browser and Lighthouse CI | Both existing docs matrix jobs must pass on the refreshed head; reviewed mode and local release data are explicit in this CI. Record final run and artifacts in #335. |
| Deployed preview and deployed-endpoint Lighthouse | Earlier xcp-ce runs in #201 establish earlier selected SHAs only. They do not validate this integration head or provide current deployed-endpoint scores. |
| Signed combined artifact and legacy Pages yum consumer | `qa/signed-repo/results/2026-11-08/README.md` at main records canonical RPM-domain consumers/fixtures; it explicitly excludes legacy Pages production rehearsal. No exact combined-artifact staging + legacy yum acceptance is established here. |
| Current RPM-domain yum consumer | The 2026-11-08 record identifies ce44 yum/rpm, actual package identities, signed metadata and negative fixtures. Retain that scoped PASS, separate from the legacy Pages population. |
| Non-infrastructure inventory dispositions | #348 and #60 decision `6577451394` defer infrastructure-dependent #350–#360 only. `XOA-CLOSURE.md` and `XOA-DAILY-VALIDATION.md` retain partial/failed modes including HP04 combined-series statistics. The required beta recovery subset in #401 does not complete all manual inventory modes. |
| Current human content/language approval | Satisfied for the receipt's current revision anchors; exact body/source records retained. Later substantive changes require truthful tracking. |
| Beta ISO acceptance | Not required by owner decision; ce55 remains selected, ce36 observations stay ce36. |
| Merge authority / publication timing | Normal integration authorized when extant gates permit; no additional approval invented. Campaign timing is undefined/HOLD; no promotion, announcement or scheduling. |

Refresh current main once more before merge; keep the source/run/release-data
identities and rollback artifact in the PR record. Do not close #60/#19/#189
or their subissues merely because integration CI or the reviewed text gate passes.
