# Screenshot requests

These YAML files are instructions **as data** for the dedicated
[Jenkins documentation runner](https://github.com/Vagrantin/jenkins-infra/blob/main/docs/docs-screenshots.md),
tracked in [jenkins-infra#87](https://github.com/Vagrantin/jenkins-infra/issues/87).
Pipeline code, Playwright, credentials, agents and lab configuration stay in
jenkins-infra. Only reviewed PNGs are later integrated into the documentation.

The offline runner from [jenkins-infra PR #110](https://github.com/Vagrantin/jenkins-infra/pull/110) has been deployed; the first Jenkins offline build was accepted. Offline requests run without a host/appliance lab. Hugo `docPage` paths in the new requests require [jenkins-infra PR #117](https://github.com/Vagrantin/jenkins-infra/pull/117) to be deployed before running them. Live inventory and console requests still need the dedicated documentation lab in [#91](https://github.com/Vagrantin/jenkins-infra/issues/91).

The manual Jenkins job is `docs/screenshots`. Set `XCP_HL_REF` to `main` or to an
open same-repository maintainer `PR-<number>` targeting main, and `REQUEST` to the
YAML filename. Arbitrary branches, tags, forks, paths and executable steps are
rejected. The runner resolves the ref to an immutable commit and records the
request hash. A run returns one private bundle with `reviewStatus: pending`;
it never commits or publishes images here.

| Request | Purpose | Output |
| --- | --- | --- |
| `xoa-beginner.yaml` | Combined lab pilot: language settings, connected server, About, installer ISO, VM wizard, console and disks | 7 images × EN/FR/JA |
| `xoa-first-login-live.yaml` | First-login guide: language settings, connected server and About | 3 images × EN/FR/JA; live lab |
| `xoa-create-vm-live.yaml` | Create-VM guide: installer ISO, wizard, console and disks | 4 images × EN/FR/JA; live lab |
| `xolite-first-login.yaml` | XO Lite-ce login page without credentials | 1 image × EN/FR/JA |
| `xoa-first-login-offline.yaml` | Built XOA-HL sign-in template, simulated and unauthenticated | 1 image × EN/FR/JA; source template remains English |
| `xoa-language-offline.yaml` | Actual XOA-HL language-settings UI with a public read-only account fixture | 1 image × EN/FR/JA |
| `xolite-login-error-offline.yaml` | XO Lite-ce authentication error with a fixed refused-login fixture | 1 image × EN/FR/JA |
| `xolite-host.yaml` | Prepared documentation host shown in XO Lite-ce after login, plus its Patches card once loaded | 2 images × EN/FR/JA |

The existing combined `xoa-beginner.yaml` still uses a legacy component path because it spans two guides. The page-scoped requests and offline/XO Lite requests identify the active Hugo EN source. [STEP-COVERAGE.md](STEP-COVERAGE.md) inventories numbered guide steps and the requested checkpoints; it is a backlog, not proof that those screenshots have been captured or approved. Start live verification with an
English-only request in a maintainer PR, then enable all three locales. The
live examples' selectors need confirmation against the deployed lab release.

Request fields: `id`, `docPage` (legacy Markdown under `docs/` or active `site/content/{en,fr,ja}/docs/` after parser deployment), `target` (`xoa` or
`xolite`), `mode` (`auto`, `live`, `offline`), `locales` (EN/FR/JA), `authenticate`
(boolean), `fixture` (`none`, XOA `beginner` or XO Lite `host`) and `steps`.
Optional `offlineScene` is `login`, `login-error` or XOA-only `user-settings`.
It requires `mode: auto`/`offline`, `authenticate: false`, `fixture: none`, and
one of the runner's supported routes. It never provides credentials or mock code.

Steps allow `goto`, `waitFor`, `click`, `fill`, `select`, `hover`, `mask` and
`screenshot` only. Use root-relative routes, CSS selectors or accessible role/text
locators. No JavaScript, shell, credentials, arbitrary URLs or input templates.
Non-secret literal values only for fill/select. Masks apply until the next goto;
mandatory masks and lab-configured private selectors always remain active.
Translated labels can use `{en: ..., fr: ..., ja: ...}`.

Capture format: the viewport is 1280 x 800 at device scale factor 2, so images are
2560 px wide (a viewport capture is 2560 x 1600). Masks are solid black. Prefer
`screenshot: {name, element}` or `clip` so a figure shows one panel; use `fullPage`
only for an overview. The site can show a 2x image at half width for sharp text.
Before each screenshot the runner fails if a dialog or progress bar is visible; set
`allowDialog: true` or `allowBusy: true` on a step that documents one. The runner also
fails on any blocked outbound request. To wait for a spinner to go away, use
`waitFor` with `hidden: true`, after waiting for the spinner's card to appear.

The reviewed documentation lab config supplies fixture placeholders such as
`{{poolUuid}}`, `{{vmUuid}}` and version strings; operators do not type UUIDs per
run. With the new runner, `auto` selects a supported, enabled offline scene first;
otherwise it uses the enabled live target. Explicit `live` never becomes simulated,
and explicit `offline` stops if the scene is unavailable. The existing
`xolite-first-login.yaml` is eligible for offline automatically.

Offline captures build reviewed immutable HomeLab source pins on a secretless
ephemeral agent, and carry a visible simulation label and build/fixture hashes.
They do not simulate hosts, installed guests, XAPI inventory or consoles. XOA's
sign-in template is English; its language-settings UI exercises the translated
interface. The pinned XO Lite Japanese locale retains some English login/error
labels. Review the source UI as rendered; do not translate screenshot text by hand.

See the [operator/request contract](https://github.com/Vagrantin/jenkins-infra/blob/main/docs/docs-screenshots.md)
for the complete schema, bounds, preparation, routing and failures . The runner rejects aliases/tags/unknown fields and stale or
incomplete bundles. Provision the dedicated lab before a live pilot; offline captures need no lab.

Review language, Japanese glyphs, display state, account/address masking and
console privacy. Record the reviewer, build URL, request commit and approved
hashes. Add approved PNGs with localized captions and alt text through a separate
documentation PR. Screenshots illustrate the UI; they are not functional QA.

Contract evidence for this request format:
`jenkins-infra/e2e/screenshots/request.mjs@95b0450a2d2e57d119dd99300f0e901b68dfa8bd`
and `jenkins-infra/docs/docs-screenshots.md@95b0450a2d2e57d119dd99300f0e901b68dfa8bd`.
Requests describe illustrations, not release compatibility assertions. Offline simulation
is not evidence that a live deployment or guest installation passed.
