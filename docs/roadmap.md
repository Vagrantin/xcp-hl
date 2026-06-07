---
layout: default
title: Roadmap
nav_order: 3
---

# Roadmap
{: .no_toc }

Planned improvements and future direction for XCP-ng Community Edition.
{: .fs-6 .fw-300 }

{: .note }
This roadmap reflects current intent. Priorities can shift based on community
feedback and upstream changes. Open an issue on
[GitHub](https://github.com/Vagrantin/xcp-ce/issues) to propose or upvote items.

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Near term — next release

These are actively being worked on or are well-defined enough to implement soon.

### GPG key management
{: .d-inline-flex }

Security
{: .label .label-red }

Full refactor of the GPG key management.
The current goal is to have one key per module if doable.
1 key for xo-lite-ce RPM package
1 key for xoa-proxy RPM package
1 key for XCP-ng-ce ISO image

**Tracked:** [xcp-ce#2](https://github.com/Vagrantin/xcp-ce/issues/2)

---

### Release publication fix
{: .d-inline-flex }

Bug
{: .label .label-red }

Fix the current release publication pipeline to ensure artifacts are correctly
published and accessible when a new xcp-CE release is availabale.

**Tracked:** [xcp-ce#3](https://github.com/Vagrantin/xcp-ce/issues/3)

---

### XO Lite — "Deploy XOA" button state on success
{: .d-inline-flex }

Bug
{: .label .label-red }

After a successful XOA deployment the "Deploy XOA" button does not switch to 
"Access XOA". Fix the reactive state update in the deploy composable
so the UI correctly reflects a finished deployment. This is already working 
on upstream and broken with my changes.

**Tracked:** [xolite-ce#4](https://github.com/Vagrantin/xolite-ce/issues/4)

---

### Website documentation & CI/CD integration
{: .d-inline-flex }

CI/CD
{: .label .label-green }

Integrate the CI/CD pipeline output so that documentation updates are
automatically published to the project website on every successful build,
keeping the published docs in sync with the repository without manual steps.

**Tracked:** [xcp-ce#4](https://github.com/Vagrantin/xcp-ce/issues/4)

---

## Medium term

Items that are planned but require more design or upstream coordination.

### Automated upstream version tracking
{: .d-inline-flex }

CI/CD
{: .label .label-green }

A GitHub Actions workflow will periodically check for new XCP-ng 8.x point
releases and XO Lite version bumps. When a new upstream tag is detected, it
will open a PR that updates the version pin and re-runs the full build
pipeline.

---

### Xen Orchestra Community edition (XOA-CE)
{: .d-inline-flex }

Enhancement
{: .label .label-blue }

Produce a community-patched XOA appliance that removes all banners related to
lack of commercial support and strips out features that require a Vates license,
resulting in a clean, fully open community image for home-labbers.

**Tracked:** [xcp-ce#5](https://github.com/Vagrantin/xcp-ce/issues/5)

---

### xoa-proxy — memory footprint reduction
{: .d-inline-flex }

Enhancement
{: .label .label-blue }

Profile and reduce the runtime memory consumption of the `xoa-proxy` Rust
service, which currently streams XVA images to XAPI. Target: smaller idle
footprint without compromising streaming throughput.

**Tracked:** [xoa-proxy#1](https://github.com/Vagrantin/xoa-proxy/issues/1)

---

### xoa-proxy — dependency (crate) reduction
{: .d-inline-flex }

Enhancement
{: .label .label-blue }

Audit the Cargo dependency tree and replace or remove crates where the same
functionality can be achieved with fewer or lighter dependencies, improving
compile times and reducing the attack surface.

**Tracked:** [xoa-proxy#2](https://github.com/Vagrantin/xoa-proxy/issues/2)

---

### xoa-proxy — logrotate timezone (UTC offset)
{: .d-inline-flex }

Bug
{: .label .label-yellow }

The `logrotate` configuration for `xoa-proxy` uses UTC timestamps regardless
of the host's local timezone. Align log rotation timestamps with the host
timezone so log files are dated consistently with the system time and date.

**Tracked:** [xoa-proxy#3](https://github.com/Vagrantin/xoa-proxy/issues/3)

---

### xolite-ce RPM — LICENSE file
{: .d-inline-flex }

Enhancement
{: .label .label-blue }

Include a proper `LICENSE` file inside the `xo-lite-ce` RPM package so that
the license terms are discoverable from the installed package metadata and
comply with RPM packaging best practices.

**Tracked:** [xolite-ce#1](https://github.com/Vagrantin/xolite-ce/issues/1)

---

## Long term / ideas

These are possibilities the project is considering but has not committed to.

### Container support out of the box
{: .d-inline-flex }

Exploratory
{: .label .label-purple }

Provide the ability to deploy and manage containers directly from XO Lite or
XOA, addressing a long-standing community request. This requires significant
investigation: containers running in Dom0 carry risk of uncontrolled behaviour
and the XCP-ng toolstack must be made aware of their existence. Administration
from XOA adds further complexity. No implementation commitment has been made.

**Tracked:** [xcp-ce#6](https://github.com/Vagrantin/xcp-ce/issues/6)

---

### answerfile.xml automated install support
Provide an example `answerfile.xml` for fully unattended CE deployments
(PXE boot / scripted provisioning). This requires the answerfile to be
injected inside `install.img` (SquashFS), which the current build pipeline
already supports.

---

## Completed

| Item | Released |
|---|---|
| Initial XO Lite patch (community deploy endpoint) | v8.3-ce Apr 2026 |
| `xoa-proxy` Rust streaming server | v8.3-ce Apr 2026 |
| Two-repo GPG-signed RPM + ISO build pipeline | v8.3-ce Apr 2026 |
| GitHub Actions free-tier CI/CD | v8.3-ce Apr 2026 |
| Read-only credential fields in XO Lite deploy view | v8.3-ce Apr 2026 |
