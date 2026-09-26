---
title: Documentation
weight: 1
next: /docs/start
translationKey: docs-overview
---

Everything about installing, running and building XCP-hl.

{{< callout type="info" >}}
All content has migrated from Jekyll to Hugo, in English, French and
Japanese ([#60](https://github.com/Vagrantin/xcp-hl/issues/60)). This site
is not live yet: production is still
[vagrantin.github.io/xcp-hl](https://vagrantin.github.io/xcp-hl/) until cutover
(phase 5).
{{< /callout >}}

## Sections

{{< cards >}}
  {{< card link="start" title="Getting Started" subtitle="Download, install, deploy XOA, and connect Xen Orchestra to your host." >}}
  {{< card link="guides/features" title="Guides" subtitle="What is in a release, how updates work, and the day-to-day operation of a host." >}}
  {{< card link="components" title="Components" subtitle="The repositories XCP-hl is built from, their build pipelines and how they fit together." >}}
  {{< card link="reference/release-matrix" title="Reference" subtitle="Release matrix, changelog and roadmap." >}}
  {{< card link="https://github.com/Vagrantin/xcp-hl" title="Source" subtitle="The repository, the issue tracker and the build pipelines." icon="github" >}}
{{< /cards >}}

## Planned structure

The section tree below is the target for the full platform documentation
(Phase 6 of [#60](https://github.com/Vagrantin/xcp-hl/issues/60)). `start/`,
`guides/`, `components/` and `reference/` exist today; `build/`, `qa/` and
`contributing/` are future work. Adding a section is adding a folder; there
is no hand-maintained global ordering.

| Section | Holds |
|---|---|
| `start/` | Download, install, first boot, verify |
| `guides/` | Updating, storage, networking, backup, troubleshooting |
| `components/` | `xcp-ng-ce-iso`, `xolite-ce`, `xoa-proxy`, `xoa-hl`, `build-xoa-hl`, `xoa-deploy-patcher`, `xcp-hl-release` |
| `build/` | Build orchestration, CI, signing, release process |
| `qa/` | QA harness, smoke tests |
| `reference/` | Release matrix, changelog, roadmap, package names, GPG keys |
| `contributing/` | How to contribute |

## Open questions on #60 (resolved)

| # | Question | Decision |
|---|---|---|
| 1 | Framework | Hugo + Hextra |
| 2 | URL policy | Pretty URLs, with redirect stubs from every old Jekyll path (see `site/README.md`) |
| 3 | What "standalone" means | A tarball any web server can host, built by `hugo --baseURL <url>`, not a `file://`-opened bundle |
| 4 | Custom domain | `xcp-hl.org`, being rehearsed on this repo's own Pages site first |
| 5 | Site location | Stays in `xcp-hl/docs/` (→ `site/` at cutover), no separate repository |
| 6 | Translation policy | Production waits for all three languages; a pre-production preview may still show an untranslated page as a clearly-marked link to the English original (see `site/README.md`, "Translation-pending pages") |

Only phases 4 (standalone build) and 5 (cutover) remain.
