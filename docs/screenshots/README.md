# Screenshot requests

These YAML files are instructions **as data** for the dedicated
[Jenkins documentation runner](https://github.com/Vagrantin/jenkins-infra/blob/main/docs/docs-screenshots.md),
tracked in [jenkins-infra#87](https://github.com/Vagrantin/jenkins-infra/issues/87).
Pipeline code, Playwright, credentials, agents and lab configuration stay in
jenkins-infra. Only reviewed PNGs are later integrated into the documentation.

**Offline requests below require [jenkins-infra PR #110](https://github.com/Vagrantin/jenkins-infra/pull/110) to be merged and deployed first.** They run without a host/appliance lab; live inventory and console requests still need the dedicated documentation lab.

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
| `xoa-first-login-offline.yaml` | Built XOA-HL sign-in template, simulated and unauthenticated | 1 image × EN/FR/JA; source template remains English |
| `xoa-language-offline.yaml` | Actual XOA-HL language-settings UI with a public read-only account fixture | 1 image × EN/FR/JA |
| `xolite-login-error-offline.yaml` | XO Lite-ce authentication error with a fixed refused-login fixture | 1 image × EN/FR/JA |
| `xolite-host.yaml` | Prepared documentation host shown in XO Lite-ce after login | 1 image × EN/FR/JA |

`docPage` currently points to the existing component documentation. Retarget it
when the beginner pages are restored or created. Start live verification with an
English-only request in a maintainer PR, then enable all three locales. The
live examples' selectors need confirmation against the deployed lab release.

Request fields: `id`, `docPage` (Markdown path under `docs/`), `target` (`xoa` or
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
