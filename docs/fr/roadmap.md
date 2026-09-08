---
layout: default
title: Feuille de route
parent: Français
nav_order: 3
lang: fr
---

# Feuille de route
{: .no_toc }

Améliorations prévues et orientations futures de XCP-ng Home lab Edition.
{: .fs-6 .fw-300 }

{: .note }
Cette feuille de route reflète les intentions actuelles. Les priorités peuvent
évoluer selon les retours de la communauté et les changements en amont. Ouvrez
un ticket sur [GitHub](https://github.com/Vagrantin/xcp-hl/issues) pour
proposer un élément ou le soutenir.

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Court terme — prochaine version

Ces points sont en cours de travail ou suffisamment définis pour être
implémentés bientôt.

### Clés GPG — une clé de signature par module
{: .d-inline-flex #gpg-keys--one-signing-key-per-module }

Sécurité
{: .label .label-red }

Le modèle GPG harmonisé issu de
[xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) est en place : clé
maîtresse hors ligne avec deux sous-clés de signature (une pour les RPM, une
pour l'ISO), clé publique publiée sur keys.openpgp.org — voir
[Signature GPG](developers/#gpg-signing). Reste à affiner : scinder la
sous-clé RPM partagée pour que chaque module ait sa propre clé — une pour le
RPM `xo-lite-ce`, une pour le RPM `xoa-proxy`, une pour l'ISO.

**Suivi :** ticket de suivi à ouvrir (xcp-hl#3 est terminé)

---

### XO Lite — état du bouton « Deploy XOA » après un succès
{: .d-inline-flex }

Bogue
{: .label .label-red }

Après un déploiement XOA réussi, le bouton « Deploy XOA » ne devient pas
« Access XOA ». Il faut corriger la mise à jour de l'état réactif dans le
composable de déploiement pour que l'interface reflète correctement un
déploiement terminé. Cela fonctionne déjà en amont et a été cassé par mes
modifications.

**Suivi :** [xolite-ce#4](https://github.com/Vagrantin/xolite-ce/issues/4)

---

## Moyen terme

Éléments prévus, mais qui demandent davantage de conception ou de
coordination avec l'amont.

### Suivi automatisé des versions amont
{: .d-inline-flex }

CI/CD
{: .label .label-green }

Le démon Rust
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
déclenche et surveille déjà tous les builds de composants sur une minuterie
quotidienne, ignore les composants dont la dernière release GitHub est déjà à
jour, et diagnostique les journaux de CI en échec avec un LLM local (Ollama).
Reste à faire : détecter les nouvelles versions mineures de XCP-ng 8.x et les
montées de version de XO Lite, puis ouvrir une pull request qui met à jour la
version figée (par exemple `UPSTREAM_TAG` dans `xolite-ce`).

---

### xoa-proxy — réduction de l'empreinte mémoire
{: .d-inline-flex }

Amélioration
{: .label .label-blue }

Profiler et réduire la consommation mémoire à l'exécution du service Rust
`xoa-proxy`, qui transmet actuellement les images XVA à XAPI en flux continu.
Objectif : une empreinte plus faible au repos, sans compromettre le débit de
transfert.

**Suivi :** [xoa-proxy#1](https://github.com/Vagrantin/xoa-proxy/issues/1)

---

### xoa-proxy — réduction des dépendances (crates)
{: .d-inline-flex }

Amélioration
{: .label .label-blue }

Auditer l'arbre de dépendances Cargo et remplacer ou supprimer les crates
lorsque la même fonctionnalité peut être obtenue avec des dépendances moins
nombreuses ou plus légères, ce qui améliore les temps de compilation et réduit
la surface d'attaque.

**Suivi :** [xoa-proxy#2](https://github.com/Vagrantin/xoa-proxy/issues/2)

---

### xoa-proxy — fuseau horaire de logrotate (décalage UTC)
{: .d-inline-flex }

Bogue
{: .label .label-yellow }

La configuration `logrotate` de `xoa-proxy` utilise des horodatages UTC, quel
que soit le fuseau horaire local de l'hôte. Il faut aligner les horodatages de
rotation des journaux sur le fuseau horaire de l'hôte, pour que les fichiers
de journaux soient datés de manière cohérente avec l'heure et la date du
système.

**Suivi :** [xoa-proxy#3](https://github.com/Vagrantin/xoa-proxy/issues/3)

---

### RPM xolite-ce — fichier LICENSE
{: .d-inline-flex }

Amélioration
{: .label .label-blue }

Inclure un vrai fichier `LICENSE` dans le paquet RPM `xo-lite-ce`, afin que
les termes de la licence soient consultables depuis les métadonnées du paquet
installé et que le paquet respecte les bonnes pratiques d'empaquetage RPM.

**Suivi :** [xolite-ce#1](https://github.com/Vagrantin/xolite-ce/issues/1)

---

## Long terme / idées

Ce sont des pistes que le projet envisage sans s'y être engagé.

### Prise en charge des conteneurs par défaut
{: .d-inline-flex }

Exploratoire
{: .label .label-purple }

Offrir la possibilité de déployer et de gérer des conteneurs directement
depuis XO Lite ou XOA, ce qui répond à une demande ancienne de la communauté.
Cela demande une investigation importante : des conteneurs exécutés dans le
Dom0 risquent de se comporter de manière incontrôlée, et la pile logicielle
XCP-ng doit être informée de leur existence. L'administration depuis XOA
ajoute encore de la complexité. Aucun engagement d'implémentation n'a été
pris.

**Suivi :** [xcp-hl#7](https://github.com/Vagrantin/xcp-hl/issues/7)

---

### Prise en charge de l'installation automatisée par answerfile.xml
Fournir un exemple d'`answerfile.xml` pour des déploiements HL entièrement
automatisés (démarrage PXE / provisionnement par script). Cela suppose
d'injecter le fichier de réponses dans `install.img` (SquashFS), ce que la
chaîne de build actuelle sait déjà faire.

---

## Terminé

| Élément | Publié |
|---|---|
| Stockage ISO par défaut : partition de 20 Go réservée à l'installation, enregistrée comme SR d'ISO au premier démarrage ([#2](https://github.com/Vagrantin/xcp-hl/issues/2), [#46](https://github.com/Vagrantin/xcp-hl/issues/46)) | sept. 2026 |
| Édition XOA-HL : menus soumis à licence et bandeau d'absence de support supprimés, image construite depuis les sources et proposée comme option de déploiement dans XO Lite ([#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)) | juil. 2026 |
| Versionnage automatisé des releases + notes de version pour les RPM et l'ISO ([#4](https://github.com/Vagrantin/xcp-hl/issues/4)) | juil. 2026 |
| Site de documentation publié automatiquement à chaque push via la CI GitHub Pages ([#5](https://github.com/Vagrantin/xcp-hl/issues/5)) | juin 2026 |
| Modèle de signature GPG : clé maîtresse hors ligne + sous-clés RPM/ISO, clé publique sur keys.openpgp.org ([#3](https://github.com/Vagrantin/xcp-hl/issues/3)) | mai 2026 |
| Premiers builds de l'appliance XOA-HL modifiée (`xoa-hl` + `build-xoa-hl`) | juil. 2026 |
| Démon d'orchestration des builds quotidiens (`buildorchestration`) | juil. 2026 |
| Version amont de xo-lite figée (`UPSTREAM_TAG`) | juil. 2026 |
| Premier correctif XO Lite (point de déploiement communautaire) | v8.3-ce avr. 2026 |
| Serveur de flux `xoa-proxy` en Rust | v8.3-ce avr. 2026 |
| Chaîne de build RPM + ISO signés GPG sur deux dépôts | v8.3-ce avr. 2026 |
| CI/CD GitHub Actions | v8.3-ce avr. 2026 |
| Champs d'identifiants en lecture seule dans la vue de déploiement de XO Lite | v8.3-ce avr. 2026 |
