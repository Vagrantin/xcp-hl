---
layout: default
title: Roadmap
nav_order: 3
---

# Roadmap
{: .no_toc }

Planned improvements and future direction for XCP-ng Home lab Edition.
{: .fs-6 .fw-300 }

{: .note }
This roadmap reflects current intent. Priorities can shift based on community
feedback and upstream changes. Open an issue on
[GitHub](https://github.com/Vagrantin/xcp-hl/issues) to propose or upvote items.

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Near term — next release

These are actively being worked on or are well-defined enough to implement soon.

### GPG keys — one signing key per module
{: .d-inline-flex }

Security
{: .label .label-red }

The harmonized GPG model from
[xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) is implemented:
offline master key with two signing subkeys (one for the RPMs, one for the
ISO), public key published on keys.openpgp.org — see
[GPG signing](developers/#gpg-signing). Remaining refinement: split the
shared RPM subkey so each module has its own key — one for the
`xo-lite-ce` RPM, one for the `xoa-proxy` RPM, one for the ISO.

**Tracked:** follow-up issue to be opened (xcp-hl#3 is done)

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

## Medium term

Items that are planned but require more design or upstream coordination.

### Automated upstream version tracking
{: .d-inline-flex }

CI/CD
{: .label .label-green }

The [`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
Rust daemon already triggers and monitors all component builds on a daily
timer, skips components whose latest GitHub release is already up to date,
and diagnoses failed CI logs with a local LLM (Ollama). Still to do: detect
new XCP-ng 8.x point releases and XO Lite version bumps and open a PR that
updates the version pin (e.g. `UPSTREAM_TAG` in `xolite-ce`).

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

### Update and upgrade model
{: .d-inline-flex }

Enhancement
{: .label .label-blue }

Give XOA-HL a yum repo so the appliance can update itself in place
(currently only `xo-lite-ce` and `xoa-proxy` are updatable this way), then
add an update-management section to the XOA UI. See the
[design proposal](developers/update-upgrade-model).

**Tracked:** [xcp-hl#14](https://github.com/Vagrantin/xcp-hl/issues/14)

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

**Tracked:** [xcp-hl#7](https://github.com/Vagrantin/xcp-hl/issues/7)

---

### answerfile.xml automated install support
Provide an example `answerfile.xml` for fully unattended HL deployments
(PXE boot / scripted provisioning). This requires the answerfile to be
injected inside `install.img` (SquashFS), which the current build pipeline
already supports.

---

## Completed

| Item | Released |
|---|---|
| XOA-HL edition: license-gated menus and no-support banner removed, image built from source and selectable as deploy option in XO Lite ([#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)) | Jul 2026 |
| Automated release versioning + release notes for the RPMs and the ISO ([#4](https://github.com/Vagrantin/xcp-hl/issues/4)) | Jul 2026 |
| Docs website auto-published on every push via GitHub Pages CI ([#5](https://github.com/Vagrantin/xcp-hl/issues/5)) | Jun 2026 |
| GPG signing model: offline master key + RPM/ISO subkeys, public key on keys.openpgp.org ([#3](https://github.com/Vagrantin/xcp-hl/issues/3)) | May 2026 |
| First XOA-HL patched appliance builds (`xoa-hl` + `build-xoa-hl`) | Jul 2026 |
| Daily build orchestration daemon (`buildorchestration`) | Jul 2026 |
| Upstream xo-lite version pinning (`UPSTREAM_TAG`) | Jul 2026 |
| Initial XO Lite patch (community deploy endpoint) | v8.3-ce Apr 2026 |
| `xoa-proxy` Rust streaming server | v8.3-ce Apr 2026 |
| Two-repo GPG-signed RPM + ISO build pipeline | v8.3-ce Apr 2026 |
| GitHub Actions CI/CD | v8.3-ce Apr 2026 |
| Read-only credential fields in XO Lite deploy view | v8.3-ce Apr 2026 |
