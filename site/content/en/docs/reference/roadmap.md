---
title: Roadmap
weight: 3
translationKey: roadmap
aliases: ["/roadmap.html"]
---

Where XCP-hl is heading, straight from the open issues on GitHub. Each line links to its issue, where the details and discussion live.
{class="lead"}

{{< callout type="info" >}}
Priorities follow the P1 / P2 / P3 labels on each issue and can shift with feedback and upstream changes. Issue titles are shown as written on GitHub. To propose or upvote an item, open or comment on an issue on [GitHub](https://github.com/Vagrantin/xcp-hl/issues).
{{< /callout >}}

## Next up (P1)

- XOA-hl update is breaking the follow up ([#103](https://github.com/Vagrantin/xcp-hl/issues/103)) · `xoa-hl`
- Jenkins CI step 7: ISO install smoke test in Dev ([#74](https://github.com/Vagrantin/xcp-hl/issues/74)) · `QA`
- Jenkins CI step 4: wire Jenkins to the vault, Dev/Test/Prod roles ([#71](https://github.com/Vagrantin/xcp-hl/issues/71)) · `buildorchestration`
- Jenkins CI step 3: choose and stand up the secret store ([#70](https://github.com/Vagrantin/xcp-hl/issues/70)) · `buildorchestration`
- Jenkins CI step 2: dedicated infra repo (JCasC, plugins, agent image) ([#69](https://github.com/Vagrantin/xcp-hl/issues/69)) · `buildorchestration`
- Local Jenkins CI to replace the orchestrator ([#57](https://github.com/Vagrantin/xcp-hl/issues/57)) · `buildorchestration`
- Review and standardize the patching model ([#43](https://github.com/Vagrantin/xcp-hl/issues/43)) · `xoa-hl`, `xolite-ce`, `xoa-deploy-patcher`
- Does yum update import the signature automatically. ([#35](https://github.com/Vagrantin/xcp-hl/issues/35)) · `xcp-hl`, `xcp-ng-ce-iso`
- Clean up old rpm on xolite that are broken. ([#25](https://github.com/Vagrantin/xcp-hl/issues/25)) · `xolite-ce`
- XOA HL patching refactore ([#16](https://github.com/Vagrantin/xcp-hl/issues/16)) · `xoa-deploy-patcher`

## Planned (P2)

- Update the XOA-hl UI to show that a reboot is required ([#102](https://github.com/Vagrantin/xcp-hl/issues/102)) · `xoa-hl`
- Goose step 2: choose the integration path into XOA-HL (goosed, ACP, or embedded) ([#83](https://github.com/Vagrantin/xcp-hl/issues/83)) · `xoa-hl`
- Goose step 1: headless goose with llama.cpp and mock MCP extensions ([#82](https://github.com/Vagrantin/xcp-hl/issues/82)) · `xoa-hl`
- Model bake-off for natural language VM creation: SLMs against up-to-8B models ([#81](https://github.com/Vagrantin/xcp-hl/issues/81)) · `xoa-hl`
- Jenkins CI step 9: absorb xoa-vm-agent into the Prod pipeline ([#76](https://github.com/Vagrantin/xcp-hl/issues/76)) · `buildorchestration`
- Jenkins CI step 8: promote the ISO smoke test to Test ([#75](https://github.com/Vagrantin/xcp-hl/issues/75)) · `QA`
- Jenkins CI step 6: decide the QA platform topology ([#73](https://github.com/Vagrantin/xcp-hl/issues/73)) · `QA`
- Jenkins CI step 5: prove the Dev loop and the promotion path ([#72](https://github.com/Vagrantin/xcp-hl/issues/72)) · `buildorchestration`
- XOA-HL automatic updates ([#45](https://github.com/Vagrantin/xcp-hl/issues/45)) · `xoa-hl`
- Revisit the unversioned `Obsoletes: xo-lite` workaround when the upstream pin moves ([#42](https://github.com/Vagrantin/xcp-hl/issues/42)) · `xolite-ce`, `xcp-ng-ce-iso`
- Update welcome message ([#27](https://github.com/Vagrantin/xcp-hl/issues/27)) · `xoa-hl`
- Add a description of each image after selection on the right side. ([#18](https://github.com/Vagrantin/xcp-hl/issues/18)) · `xolite-ce`
- Complete version matrix of all the bin and RPM ([#15](https://github.com/Vagrantin/xcp-hl/issues/15)) · `xcp-hl`
- Publish gpg public key with the iso ([#10](https://github.com/Vagrantin/xcp-hl/issues/10)) · `xcp-ng-ce-iso`
- Make the rpm build github workflows consistent ([#8](https://github.com/Vagrantin/xcp-hl/issues/8)) · `xoa-hl`, `xolite-ce`, `xcp-hl`, `xoa-proxy`

## Later (P3)

- Goose step 6: chat box in the XOA-HL UI wired to goose ([#87](https://github.com/Vagrantin/xcp-hl/issues/87)) · `xoa-hl`
- Goose step 5: the create_vm extension behind goose Approve mode ([#86](https://github.com/Vagrantin/xcp-hl/issues/86)) · `xoa-hl`
- Goose step 4: read-only platform chat through the XO MCP extension ([#85](https://github.com/Vagrantin/xcp-hl/issues/85)) · `xoa-hl`
- Goose step 3: package goose for the appliance, pinned and off by default ([#84](https://github.com/Vagrantin/xcp-hl/issues/84)) · `xoa-hl`
- Natural language VM creation in XOA-HL through a chat box ([#80](https://github.com/Vagrantin/xcp-hl/issues/80)) · `xoa-hl`
- Jenkins CI step 10: absorb iso-agent, retire the dashboard and API ([#77](https://github.com/Vagrantin/xcp-hl/issues/77)) · `buildorchestration`
- `xoa-image-*` release `created_at` is pinned to a static commit, not the actual build time ([#41](https://github.com/Vagrantin/xcp-hl/issues/41)) · `build-xoa-hl`
- Rename xo-lite-ce package ([#40](https://github.com/Vagrantin/xcp-hl/issues/40)) · `xolite-ce`, `xcp-hl`, `xcp-ng-ce-iso`
- Rename xoa-proxy package ([#39](https://github.com/Vagrantin/xcp-hl/issues/39)) · `xoa-hl`, `xcp-hl`, `xoa-proxy`
- Put in place the workflow to get changelog up to date and meaningfull ([#34](https://github.com/Vagrantin/xcp-hl/issues/34)) · `xoa-hl`, `build-xoa-hl`
- RPM LICENSE ([#32](https://github.com/Vagrantin/xcp-hl/issues/32)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Switch "deploy XOA" button on success ([#31](https://github.com/Vagrantin/xcp-hl/issues/31)) · `xolite-ce`
- Need to know which version i'm running ([#30](https://github.com/Vagrantin/xcp-hl/issues/30)) · `xoa-hl`
- Change log in github releases ([#24](https://github.com/Vagrantin/xcp-hl/issues/24)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl`, `xoa-proxy`
- Xoa-hl release is messy ([#23](https://github.com/Vagrantin/xcp-hl/issues/23)) · `build-xoa-hl`
- Improve the documentation UI ([#19](https://github.com/Vagrantin/xcp-hl/issues/19)) · `xcp-hl`
- Container out of the box ([#7](https://github.com/Vagrantin/xcp-hl/issues/7)) · `xoa-hl`

## Not yet prioritized

- Improve the memory footprint ([#64](https://github.com/Vagrantin/xcp-hl/issues/64)) · `xoa-proxy`
- Reduce the number of crate it's uisng ([#63](https://github.com/Vagrantin/xcp-hl/issues/63)) · `xoa-proxy`
- Logrotate is UTC ([#62](https://github.com/Vagrantin/xcp-hl/issues/62)) · `xoa-proxy`
- Refactoring doc ([#60](https://github.com/Vagrantin/xcp-hl/issues/60)) · `xcp-hl`
- Investigate forking ([#54](https://github.com/Vagrantin/xcp-hl/issues/54)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Identify backend/frontend code ([#53](https://github.com/Vagrantin/xcp-hl/issues/53)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl-vm`, `build-xoa-hl`, `xoa-deploy-patcher`
- XOA-hl-vm build triggers even if XOA-HL build is in progress ([#48](https://github.com/Vagrantin/xcp-hl/issues/48)) · `build-xoa-hl-vm`, `build-xoa-hl`

## Not yet tracked in an issue

Ideas that are on the table but have no issue yet.

### GPG keys: one signing key per module {#gpg-keys-one-signing-key-per-module}

The harmonized GPG model from
[xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) is implemented:
offline master key with two signing subkeys (one for the RPMs, one for the
ISO), public key published on keys.openpgp.org (see
[GPG signing](/docs/components/#gpg-signing)). Remaining refinement: split the
shared RPM subkey so each module has its own key: one for the
`xo-lite-ce` RPM, one for the `xoa-proxy` RPM, one for the ISO.

### Automated upstream version tracking {#automated-upstream-version-tracking}

The [`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
Rust daemon already triggers and monitors all component builds on a daily
timer, skips components whose latest GitHub release is already up to date,
and diagnoses failed CI logs with a local LLM (Ollama). Still to do: detect
new XCP-ng 8.x point releases and XO Lite version bumps and open a PR that
updates the version pin (e.g. `UPSTREAM_TAG` in `xolite-ce`).

### answerfile.xml automated install support

Provide an example `answerfile.xml` for fully unattended HL deployments
(PXE boot / scripted provisioning). This requires the answerfile to be
injected inside `install.img` (SquashFS), which the current build pipeline
already supports.

## Completed

| Item | Released |
|---|---|
| Default ISO storage: 20 GB partition reserved at install, registered as an ISO SR on first boot ([#2](https://github.com/Vagrantin/xcp-hl/issues/2), [#46](https://github.com/Vagrantin/xcp-hl/issues/46)) | Sep 2026 |
| XOA-hl edition: license-gated menus and no-support banner removed, image built from source and selectable as deploy option in XO Lite ([#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)) | Jul 2026 |
| Automated release versioning + release notes for the RPMs and the ISO ([#4](https://github.com/Vagrantin/xcp-hl/issues/4)) | Jul 2026 |
| Docs website auto-published on every push via GitHub Pages CI ([#5](https://github.com/Vagrantin/xcp-hl/issues/5)) | Jun 2026 |
| GPG signing model: offline master key + RPM/ISO subkeys, public key on keys.openpgp.org ([#3](https://github.com/Vagrantin/xcp-hl/issues/3)) | May 2026 |
| First XOA-hl patched appliance builds (`xoa-hl` + `build-xoa-hl`) | Jul 2026 |
| Daily build orchestration daemon (`buildorchestration`) | Jul 2026 |
| Upstream xo-lite version pinning (`UPSTREAM_TAG`) | Jul 2026 |
| Initial XO Lite patch (community deploy endpoint) | v8.3-ce Apr 2026 |
| `xoa-proxy` Rust streaming server | v8.3-ce Apr 2026 |
| Two-repo GPG-signed RPM + ISO build pipeline | v8.3-ce Apr 2026 |
| GitHub Actions CI/CD | v8.3-ce Apr 2026 |
| Read-only credential fields in XO Lite deploy view | v8.3-ce Apr 2026 |

