---
title: Roadmap
weight: 3
translationKey: roadmap
aliases: ["/fr/roadmap.html"]
---

La direction que prend XCP-hl, directement à partir des tickets ouverts sur GitHub. Chaque ligne renvoie vers son ticket, où se trouvent les détails et la discussion.
{class="lead"}

{{< callout type="info" >}}
Les priorités suivent les labels P1 / P2 / P3 de chaque ticket et peuvent évoluer selon les retours et les changements amont. Les titres des tickets sont affichés tels qu'ils sont écrits sur GitHub. Pour proposer ou soutenir un élément, ouvrez ou commentez un ticket sur [GitHub](https://github.com/Vagrantin/xcp-hl/issues).
{{< /callout >}}

## Prochainement (P1)

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

## Prévu (P2)

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

## Plus tard (P3)

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

## Pas encore priorisé

- Improve the memory footprint ([#64](https://github.com/Vagrantin/xcp-hl/issues/64)) · `xoa-proxy`
- Reduce the number of crate it's uisng ([#63](https://github.com/Vagrantin/xcp-hl/issues/63)) · `xoa-proxy`
- Logrotate is UTC ([#62](https://github.com/Vagrantin/xcp-hl/issues/62)) · `xoa-proxy`
- Refactoring doc ([#60](https://github.com/Vagrantin/xcp-hl/issues/60)) · `xcp-hl`
- Investigate forking ([#54](https://github.com/Vagrantin/xcp-hl/issues/54)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Identify backend/frontend code ([#53](https://github.com/Vagrantin/xcp-hl/issues/53)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl-vm`, `build-xoa-hl`, `xoa-deploy-patcher`
- XOA-hl-vm build triggers even if XOA-HL build is in progress ([#48](https://github.com/Vagrantin/xcp-hl/issues/48)) · `build-xoa-hl-vm`, `build-xoa-hl`

## Pas encore suivi dans un ticket

Des idées à l'étude qui n'ont pas encore de ticket.

### Clés GPG : une clé de signature par module {#clés-gpg-une-clé-de-signature-par-module}

Le modèle GPG harmonisé issu de
[xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) est en place :
clé maîtresse hors ligne avec deux sous-clés de signature (une pour les RPM, une
pour l'ISO), clé publique publiée sur keys.openpgp.org (voir
[Signature GPG](/docs/components/#gpg-signing)). Reste à affiner : scinder la
sous-clé RPM partagée pour que chaque module ait sa propre clé : une pour le
RPM `xo-lite-ce`, une pour le RPM `xoa-proxy`, une pour l'ISO.

### Suivi automatisé des versions amont {#suivi-automatisé-des-versions-amont}

Le démon Rust
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
déclenche et surveille déjà tous les builds de composants sur une minuterie
quotidienne, ignore les composants dont la dernière release GitHub est déjà à
jour, et diagnostique les journaux de CI en échec avec un LLM local (Ollama).
Reste à faire : détecter les nouvelles versions mineures de XCP-ng 8.x et les
montées de version de XO Lite, puis ouvrir une pull request qui met à jour la
version figée (par exemple `UPSTREAM_TAG` dans `xolite-ce`).

### Prise en charge de l'installation automatisée par answerfile.xml

Fournir un exemple d'`answerfile.xml` pour des déploiements HL entièrement
automatisés (démarrage PXE / provisionnement par script). Cela suppose
d'injecter le fichier de réponses dans `install.img` (SquashFS), ce que la
chaîne de build actuelle sait déjà faire.

## Terminé

| Élément | Publié |
|---|---|
| Stockage ISO par défaut : partition de 20 Go réservée à l'installation, enregistrée comme SR d'ISO au premier démarrage ([#2](https://github.com/Vagrantin/xcp-hl/issues/2), [#46](https://github.com/Vagrantin/xcp-hl/issues/46)) | sept. 2026 |
| Édition XOA-hl : menus soumis à licence et bandeau d'absence de support supprimés, image construite depuis les sources et proposée comme option de déploiement dans XO Lite ([#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)) | juil. 2026 |
| Versionnage automatisé des releases + notes de version pour les RPM et l'ISO ([#4](https://github.com/Vagrantin/xcp-hl/issues/4)) | juil. 2026 |
| Site de documentation publié automatiquement à chaque push via la CI GitHub Pages ([#5](https://github.com/Vagrantin/xcp-hl/issues/5)) | juin 2026 |
| Modèle de signature GPG : offline master key + sous-clés RPM/ISO, clé publique sur keys.openpgp.org ([#3](https://github.com/Vagrantin/xcp-hl/issues/3)) | mai 2026 |
| Premiers builds de l'appliance XOA-hl modifiée (`xoa-hl` + `build-xoa-hl`) | juil. 2026 |
| Démon d'orchestration des builds quotidiens (`buildorchestration`) | juil. 2026 |
| Version amont de xo-lite figée (`UPSTREAM_TAG`) | juil. 2026 |
| Premier correctif XO Lite (point de déploiement communautaire) | v8.3-ce avr. 2026 |
| Serveur de flux `xoa-proxy` en Rust | v8.3-ce avr. 2026 |
| Chaîne de build RPM + ISO signés GPG sur deux dépôts | v8.3-ce avr. 2026 |
| CI/CD GitHub Actions | v8.3-ce avr. 2026 |
| Champs d'identifiants en lecture seule dans la vue de déploiement de XO Lite | v8.3-ce avr. 2026 |
