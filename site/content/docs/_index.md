---
title: Documentation
weight: 1
next: /docs/guides/features
---

Everything about installing, running and building XCP-hl.

{{< callout type="info" >}}
This site is being migrated from Jekyll to Hugo
([#60](https://github.com/Vagrantin/xcp-hl/issues/60)). Only the two pages below
have moved so far — the rest of the documentation is still at
[vagrantin.github.io/xcp-hl](https://vagrantin.github.io/xcp-hl/).
{{< /callout >}}

## Sections

{{< cards >}}
  {{< card link="guides/features" title="Guides" subtitle="What is in a release, how updates work, and the day-to-day operation of a host." >}}
  {{< card link="https://github.com/Vagrantin/xcp-hl" title="Source" subtitle="The repository, the issue tracker and the build pipelines." icon="github" >}}
{{< /cards >}}

## Planned structure

The section tree below is the target for the full platform documentation
(Phase 6 of [#60](https://github.com/Vagrantin/xcp-hl/issues/60)), listed here so
the shape of the site is visible while the migration is in progress. Adding a
section is adding a folder — there is no hand-maintained global ordering.

| Section | Holds |
|---|---|
| `start/` | Download, install, first boot, verify |
| `guides/` | Updating, storage, networking, backup, troubleshooting |
| `components/` | `xcp-ng-ce-iso`, `xolite-ce`, `xoa-proxy`, `xoa-hl`, `build-xoa-hl-vm`, `xoa-deploy-patcher`, `xcp-hl-release` |
| `build/` | Build orchestration, CI, signing, release process |
| `qa/` | QA harness, smoke tests |
| `reference/` | Release matrix, changelog, roadmap, package names, GPG keys |
| `contributing/` | How to contribute |
