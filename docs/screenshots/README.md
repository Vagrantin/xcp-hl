# Screenshot requests

These YAML files are instructions **as data** for the dedicated
[Jenkins documentation runner](https://github.com/Vagrantin/jenkins-infra/pull/88),
tracked in [jenkins-infra#87](https://github.com/Vagrantin/jenkins-infra/issues/87).
Pipeline code, Playwright, credentials, agents and lab configuration stay in
jenkins-infra. Only reviewed PNGs are later integrated into the documentation.

The manual Jenkins job is `docs/screenshots`. Set `XCP_HL_REF` to `main` or to an
open same-repository maintainer `PR-<number>` targeting main, and `REQUEST` to the
YAML filename. Arbitrary branches, tags, forks, paths and executable steps are
rejected. The runner resolves the ref to an immutable commit and records the
request hash. A run returns one private bundle with `reviewStatus: pending`;
it never commits or publishes images here.

| Request | Purpose | Output |
| --- | --- | --- |
| `xoa-beginner.yaml` | Language settings, connected server, About versions, installer ISO, new VM wizard, guest console and disks | 7 images × EN/FR/JA |
| `xolite-first-login.yaml` | XO Lite-ce login page without credentials | 1 image × EN/FR/JA |
| `xolite-host.yaml` | Prepared documentation host shown in XO Lite-ce after login | 1 image × EN/FR/JA |

`docPage` currently points to the existing component documentation. Retarget it
when the beginner pages are restored or created. Start live verification with an
English-only request in a maintainer PR, then enable all three locales. The
examples' selectors need confirmation against the deployed lab release.

Request fields: `id`, `docPage` (Markdown path under `docs/`), `target` (`xoa` or
`xolite`), `mode` (`auto`, `live`, `offline`), `locales` (EN/FR/JA), `authenticate`
(boolean), `fixture` (`none`, XOA `beginner` or XO Lite `host`) and `steps`.

Steps allow `goto`, `waitFor`, `click`, `fill`, `select`, `hover`, `mask` and
`screenshot` only. Use root-relative routes, CSS selectors or accessible role/text
locators. No JavaScript, shell, credentials, arbitrary URLs or input templates.
Non-secret literal values only for fill/select. Masks apply until the next goto;
mandatory masks and lab-configured private selectors always remain active.
Translated labels can use `{en: ..., fr: ..., ja: ...}`.

The reviewed documentation lab config supplies fixture placeholders such as
`{{poolUuid}}`, `{{vmUuid}}` and version strings; operators do not type UUIDs per
run. This rollout routes `auto` conservatively to live documentation resources.
Explicit offline mode stops until the separate pinned UI build service is ready.

See the [operator/request contract](https://github.com/Vagrantin/jenkins-infra/blob/main/docs/docs-screenshots.md)
for the complete schema, bounds, preparation, routing and failures (available once
PR #88 merges). The runner rejects aliases/tags/unknown fields and stale or
incomplete bundles. The dedicated lab must be provisioned before a pilot.

Review language, Japanese glyphs, display state, account/address masking and
console privacy. Record the reviewer, build URL, request commit and approved
hashes. Add approved PNGs with localized captions and alt text through a separate
documentation PR. Screenshots illustrate the UI; they are not functional QA.

Contract evidence for this request format:
`jenkins-infra/e2e/screenshots/request.mjs@86c40657b4537b80ecc12aa179b71082782b6717`
and `jenkins-infra/docs/docs-screenshots.md@86c40657b4537b80ecc12aa179b71082782b6717`.
The requests are proposals for a live pilot, not release compatibility assertions.
