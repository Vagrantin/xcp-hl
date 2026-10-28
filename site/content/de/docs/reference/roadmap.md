---
title: Roadmap
weight: 3
translationKey: roadmap
aliases: ["/de/roadmap.html"]
---

Diese Seite ist eine **manuell gepflegte technische Aufgabenliste**, zuletzt geprüft am **2026-09-28**. Sie enthält Issues mit Komponentenkennzeichnung und Infrastrukturarbeiten, keine verbindlichen Veröffentlichungszusagen. Den aktuellen Stand finden Sie in der [laufenden Issue-Liste](https://github.com/Vagrantin/xcp-hl/issues).
{class="lead"}

{{< callout type="info" >}}
Prioritäten folgen den Labels P1 / P2 / P3 der jeweiligen Issues und können sich durch Rückmeldungen und Upstream-Änderungen verschieben. Issue-Titel werden so angezeigt, wie sie auf GitHub stehen. Um einen Punkt vorzuschlagen oder zu unterstützen, erstellen oder kommentieren Sie ein Issue auf [GitHub](https://github.com/Vagrantin/xcp-hl/issues).
{{< /callout >}}

## Als Nächstes (P1) {#next-up-p1}

- XOA-HL UI translation ([#131](https://github.com/Vagrantin/xcp-hl/issues/131)) · `xoa-hl`
- Jenkins CI step 2: dedicated infra repo (JCasC, plugins, agent image) ([#69](https://github.com/Vagrantin/xcp-hl/issues/69)) · `buildorchestration`
- Local Jenkins CI to replace the orchestrator ([#57](https://github.com/Vagrantin/xcp-hl/issues/57)) · `buildorchestration`
- Review and standardize the patching model ([#43](https://github.com/Vagrantin/xcp-hl/issues/43)) · `xoa-hl`, `xolite-ce`, `xoa-deploy-patcher`
- Clean up old rpm on xolite that are broken. ([#25](https://github.com/Vagrantin/xcp-hl/issues/25)) · `xolite-ce`
- XOA HL patching refactore ([#16](https://github.com/Vagrantin/xcp-hl/issues/16)) · `xoa-deploy-patcher`

## Geplant (P2) {#planned-p2}

- Update the XOA-hl UI to show that a reboot is required ([#102](https://github.com/Vagrantin/xcp-hl/issues/102)) · `xoa-hl`
- goose step 2: choose the integration path into XOA-HL (goosed, ACP, or embedded) ([#83](https://github.com/Vagrantin/xcp-hl/issues/83)) · `xoa-hl`
- goose step 1: headless goose with llama.cpp and mock MCP extensions ([#82](https://github.com/Vagrantin/xcp-hl/issues/82)) · `xoa-hl`
- Model bake-off for natural language VM creation: SLMs against up-to-8B models ([#81](https://github.com/Vagrantin/xcp-hl/issues/81)) · `xoa-hl`
- Jenkins CI step 9: absorb xoa-vm-agent into the Prod pipeline ([#76](https://github.com/Vagrantin/xcp-hl/issues/76)) · `buildorchestration`
- Jenkins CI step 8: promote the ISO smoke test to Test ([#75](https://github.com/Vagrantin/xcp-hl/issues/75)) · `QA`
- Jenkins CI step 5: prove the Dev loop and the promotion path ([#72](https://github.com/Vagrantin/xcp-hl/issues/72)) · `buildorchestration`
- Revisit the unversioned `Obsoletes: xo-lite` workaround when the upstream pin moves ([#42](https://github.com/Vagrantin/xcp-hl/issues/42)) · `xolite-ce`, `xcp-ng-ce-iso`
- update welcome message ([#27](https://github.com/Vagrantin/xcp-hl/issues/27)) · `xoa-hl`
- Add a description of each image after selection on the right side. ([#18](https://github.com/Vagrantin/xcp-hl/issues/18)) · `xolite-ce`
- Complete version matrix of all the bin and RPM ([#15](https://github.com/Vagrantin/xcp-hl/issues/15)) · `xcp-hl`
- Publish gpg public key with the iso ([#10](https://github.com/Vagrantin/xcp-hl/issues/10)) · `xcp-ng-ce-iso`
- make the rpm build github workflows consistent ([#8](https://github.com/Vagrantin/xcp-hl/issues/8)) · `xoa-hl`, `xolite-ce`, `xcp-hl`, `xoa-proxy`

## Später (P3) {#later-p3}

- goose step 6: chat box in the XOA-HL UI wired to goose ([#87](https://github.com/Vagrantin/xcp-hl/issues/87)) · `xoa-hl`
- goose step 5: the create_vm extension behind goose Approve mode ([#86](https://github.com/Vagrantin/xcp-hl/issues/86)) · `xoa-hl`
- goose step 4: read-only platform chat through the XO MCP extension ([#85](https://github.com/Vagrantin/xcp-hl/issues/85)) · `xoa-hl`
- goose step 3: package goose for the appliance, pinned and off by default ([#84](https://github.com/Vagrantin/xcp-hl/issues/84)) · `xoa-hl`
- Natural language VM creation in XOA-HL through a chat box ([#80](https://github.com/Vagrantin/xcp-hl/issues/80)) · `xoa-hl`
- Jenkins CI step 10: absorb iso-agent, retire the dashboard and API ([#77](https://github.com/Vagrantin/xcp-hl/issues/77)) · `buildorchestration`
- `xoa-image-*` release `created_at` is pinned to a static commit, not the actual build time ([#41](https://github.com/Vagrantin/xcp-hl/issues/41)) · `build-xoa-hl`
- Rename xo-lite-ce package ([#40](https://github.com/Vagrantin/xcp-hl/issues/40)) · `xolite-ce`, `xcp-hl`, `xcp-ng-ce-iso`
- Rename xoa-proxy package ([#39](https://github.com/Vagrantin/xcp-hl/issues/39)) · `xoa-hl`, `xcp-hl`, `xoa-proxy`
- Put in place the workflow to get changelog up to date and meaningfull ([#34](https://github.com/Vagrantin/xcp-hl/issues/34)) · `xoa-hl`, `build-xoa-hl`
- RPM LICENSE ([#32](https://github.com/Vagrantin/xcp-hl/issues/32)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Switch "deploy XOA" button on success ([#31](https://github.com/Vagrantin/xcp-hl/issues/31)) · `xolite-ce`
- Need to know which version i'm running ([#30](https://github.com/Vagrantin/xcp-hl/issues/30)) · `xoa-hl`
- change log in github releases ([#24](https://github.com/Vagrantin/xcp-hl/issues/24)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl`, `xoa-proxy`
- xoa-hl release is messy ([#23](https://github.com/Vagrantin/xcp-hl/issues/23)) · `build-xoa-hl`
- Improve the documentation UI ([#19](https://github.com/Vagrantin/xcp-hl/issues/19)) · `xcp-hl`
- Container out of the box ([#7](https://github.com/Vagrantin/xcp-hl/issues/7)) · `xoa-hl`

## Noch nicht priorisiert {#not-yet-prioritized}

- Need to update the links ([#132](https://github.com/Vagrantin/xcp-hl/issues/132)) · `xoa-hl`
- Improve the memory footprint ([#64](https://github.com/Vagrantin/xcp-hl/issues/64)) · `xoa-proxy`
- Reduce the number of crate it's uisng ([#63](https://github.com/Vagrantin/xcp-hl/issues/63)) · `xoa-proxy`
- Logrotate is UTC ([#62](https://github.com/Vagrantin/xcp-hl/issues/62)) · `xoa-proxy`
- Refactoring doc ([#60](https://github.com/Vagrantin/xcp-hl/issues/60)) · `xcp-hl`
- investigate forking ([#54](https://github.com/Vagrantin/xcp-hl/issues/54)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- identify backend/frontend code ([#53](https://github.com/Vagrantin/xcp-hl/issues/53)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl-vm`, `build-xoa-hl`, `xoa-deploy-patcher`
- XOA-hl-vm build triggers even if XOA-HL build is in progress ([#48](https://github.com/Vagrantin/xcp-hl/issues/48)) · `build-xoa-hl-vm`, `build-xoa-hl`

## Noch nicht in einem Issue erfasst {#not-yet-tracked-in-an-issue}

Ideen, die zur Diskussion stehen, für die aber noch kein Issue existiert.

### GPG-Schlüssel: ein Signaturschlüssel je Modul {#gpg-keys-one-signing-key-per-module}

Das vereinheitlichte GPG-Modell aus [xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) ist umgesetzt: Offline-Hauptschlüssel mit zwei Signatur-Unterschlüsseln (einer für RPMs, einer für das ISO), öffentlicher Schlüssel auf keys.openpgp.org veröffentlicht (siehe [GPG-Signierung](/docs/components/#gpg-signing)). Verbleibende Verfeinerung: den gemeinsamen RPM-Unterschlüssel aufteilen, damit jedes Modul einen eigenen Schlüssel hat: einer für das `xo-lite-ce`-RPM, einer für das `xoa-proxy`-RPM und einer für das ISO.

### Automatisierte Überwachung von Upstream-Versionen {#automated-upstream-version-tracking}

Der Rust-Daemon [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) startet und überwacht bereits täglich alle Komponentenbuilds, überspringt Komponenten mit bereits aktueller neuester GitHub-Veröffentlichung und diagnostiziert fehlgeschlagene CI-Protokolle mit einem lokalen LLM (Ollama). Noch ausstehend: neue XCP-ng-8.x-Punktversionen und XO-Lite-Versionen erkennen und einen PR zur Aktualisierung der Versionsfestlegung öffnen (beispielsweise `UPSTREAM_TAG` in `xolite-ce`).

### Unterstützung automatischer Installation mit answerfile.xml {#answerfilexml-automated-install-support}

Eine Beispiel-`answerfile.xml` für vollständig unbeaufsichtigte HL-Bereitstellungen bereitstellen (PXE-Boot / skriptgesteuerte Einrichtung). Dafür muss die Antwortdatei in `install.img` (SquashFS) eingefügt werden, was die aktuelle Buildpipeline bereits unterstützt.

## Abgeschlossen {#completed}

| Aufgabe | Veröffentlicht |
|---|---|
| Standard-ISO-Speicher: 20-GB-Partition bei Installation reserviert, beim ersten Start als ISO-SR registriert ([#2](https://github.com/Vagrantin/xcp-hl/issues/2), [#46](https://github.com/Vagrantin/xcp-hl/issues/46)) | Sep. 2026 |
| XOA-hl-Edition: lizenzabhängige Menüs und Banner für fehlenden Support entfernt, Image aus Quellcode erstellt und als Bereitstellungsoption in XO Lite auswählbar ([#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)) | Juli 2026 |
| Automatisierte Versionsnummern und Versionshinweise für RPMs und ISO ([#4](https://github.com/Vagrantin/xcp-hl/issues/4)) | Juli 2026 |
| Dokumentationswebsite bei jedem Push über GitHub-Pages-CI automatisch veröffentlicht ([#5](https://github.com/Vagrantin/xcp-hl/issues/5)) | Juni 2026 |
| GPG-Signaturmodell: Offline-Hauptschlüssel und RPM-/ISO-Unterschlüssel, öffentlicher Schlüssel auf keys.openpgp.org ([#3](https://github.com/Vagrantin/xcp-hl/issues/3)) | Mai 2026 |
| Erste Builds der angepassten XOA-hl-Appliance (`xoa-hl` und `build-xoa-hl`) | Juli 2026 |
| Daemon für tägliche Buildorchestrierung (`buildorchestration`) | Juli 2026 |
| Festlegung der Upstream-xo-lite-Version (`UPSTREAM_TAG`) | Juli 2026 |
| Erster XO-Lite-Patch (Community-Bereitstellungsendpunkt) | v8.3-ce April 2026 |
| Rust-Streamingserver `xoa-proxy` | v8.3-ce April 2026 |
| GPG-signierte RPM-/ISO-Buildpipeline mit zwei Repositorys | v8.3-ce April 2026 |
| GitHub-Actions-CI/CD | v8.3-ce April 2026 |
| Schreibgeschützte Zugangsdatenfelder in der XO-Lite-Bereitstellungsansicht | v8.3-ce April 2026 |
