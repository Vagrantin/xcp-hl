# Documentation cutover runbook (#60)

## Decision

The implementation can be reviewed and rehearsed, but replacing production needs
the gates below. A green documentation build proves neither a real ISO install
nor yum compatibility. Do not close #60 based on a placeholder repository test.

## Before merging the production switch

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
4. Record a real installation walkthrough with the current XCP-hl ISO. The blog
   photos are upstream installer illustrations, not evidence that this ISO passed.
5. Review `.github/workflows/pages.yml`: Hugo runs before repository assembly;
   repository collection, createrepo options, signing and root assembly stay intact.
   `docs/_data/` and all installed repository URLs/IDs/key names remain unchanged.
6. Rehearse the **signed** combined artifact and a real XCP-ng 8.3 yum client
   against a staging endpoint. The current `xcp-ce` workflow only stages a
   placeholder `repomd.xml`; that does **not** pass this gate.
7. Obtain the maintainer's go-ahead for the production replacement. Keep a known
   good Pages deployment/artifact and the pre-cutover commit available for rollback.

## URL and domain strategy

The first cutover replaces the renderer behind the existing production address,
`https://vagrantin.github.io/xcp-hl/`, and preserves
`/repo/8.3/x86_64/`, `/xcp-hl.repo` and `/xcp-ng-ce-public.asc` at that address.
The build uses `actions/configure-pages`' actual base URL.

`xcp-hl.net` currently belongs to the `xcp-ce` preview. Do not transfer its Pages
custom-domain setting or DNS in the renderer cutover. A later domain move needs
separate verification of the installed clients' old repository URL and every
legacy path after redirects. `xcp-hl.org` is not used by this change.

## Production acceptance (immediately after deployment)

- Confirm the Pages run succeeded for the reviewed commit.
- Check all three documentation languages and representative old redirects.
- Retrieve the repository metadata, detached signature and public key using the
  **installed clients' existing URL**, allowing redirects. Import the public key
  into a temporary GPG keyring, verify fingerprint
  `2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A`, and verify `repomd.xml.asc` against
  `repomd.xml`. HTTP 200 alone is insufficient.
- On a disposable XCP-ng 8.3 host with the existing repository configuration,
  run a fresh-cache metadata fetch and list the release package:

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
  deliberate contracts. Keep the logs and selected package versions in #60.

## Rollback

If signed metadata or yum acceptance fails, restore the previous complete Pages
artifact, or revert only the renderer-switch commit and rerun the production
workflow. Restore **both docs and repository together**, never a docs-only archive.
Preserve current `docs/_data/` updates and signing inputs. No DNS rollback is
needed because this cutover does not move the domain. Recheck metadata and yum
after rollback before reporting recovery.

The old Jekyll source is retained as an audit/rollback reference for this first
cutover. It is no longer rendered by the proposed production workflow. Delete it
in a follow-up only after acceptance, preserving `docs/_data/` and the legacy URL
inventory. #60 and #19 can be closed after the production evidence is recorded;
#133 can be closed once its content changes land in the accepted site.
