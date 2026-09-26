---
title: Documentation
weight: 1
next: /docs/start
translationKey: docs-overview
---

Tout sur l'installation, l'utilisation et la construction de XCP-hl.

{{< callout type="info" >}}
Tout le contenu français a été migré de Jekyll vers Hugo
([#60](https://github.com/Vagrantin/xcp-hl/issues/60)). Ce site n'est pas
encore en ligne : la production reste
[vagrantin.github.io/xcp-hl](https://vagrantin.github.io/xcp-hl/) jusqu'à la
bascule (phase 5).
{{< /callout >}}

## Sections

{{< cards >}}
  {{< card link="start" title="Bien démarrer" subtitle="Télécharger, installer, déployer XOA, et connecter Xen Orchestra à votre hôte." >}}
  {{< card link="guides/features" title="Guides" subtitle="Le contenu d'une version, le fonctionnement des mises à jour, et l'utilisation au quotidien d'un hôte." >}}
  {{< card link="components" title="Composants" subtitle="Les dépôts qui composent XCP-hl, leurs chaînes de build et comment ils s'articulent." >}}
  {{< card link="reference/release-matrix" title="Référence" subtitle="Matrice des versions, changelog et roadmap." >}}
  {{< card link="https://github.com/Vagrantin/xcp-hl" title="Source" subtitle="Le dépôt, le suivi des tickets et les chaînes de build." icon="github" >}}
{{< /cards >}}

## Structure prévue

L'arborescence ci-dessous est la cible de la documentation complète de la
plateforme (phase 6 de [#60](https://github.com/Vagrantin/xcp-hl/issues/60)).
`start/`, `guides/`, `components/` et `reference/` existent aujourd'hui ;
`build/`, `qa/` et `contributing/` restent à faire. Ajouter une section revient
à ajouter un dossier ; il n'y a pas d'ordre global maintenu à la main.

| Section | Contenu |
|---|---|
| `start/` | Téléchargement, installation, premier démarrage, vérification |
| `guides/` | Mises à jour, stockage, réseau, sauvegarde, dépannage |
| `components/` | `xcp-ng-ce-iso`, `xolite-ce`, `xoa-proxy`, `xoa-hl`, `build-xoa-hl`, `xoa-deploy-patcher`, `xcp-hl-release` |
| `build/` | Orchestration des builds, CI, signature, processus de release |
| `qa/` | Harnais de QA, tests de fumée |
| `reference/` | Matrice des versions, changelog, roadmap, noms de paquets, clés GPG |
| `contributing/` | Comment contribuer |

## Questions ouvertes sur #60 (résolues)

| # | Question | Décision |
|---|---|---|
| 1 | Framework | Hugo + Hextra |
| 2 | Politique d'URL | URL propres, avec une redirection depuis chaque ancien chemin Jekyll (voir `site/README.md`) |
| 3 | Ce que « autonome » signifie | Une archive que n'importe quel serveur web peut héberger, produite par `hugo --baseURL <url>`, pas un ensemble ouvert en `file://` |
| 4 | Domaine personnalisé | `xcp-hl.org`, d'abord répété sur le site Pages de ce dépôt |
| 5 | Emplacement du site | Reste dans `xcp-hl/docs/` (→ `site/` à la bascule), pas de dépôt séparé |
| 6 | Politique de traduction | La production attend les trois langues ; une préproduction peut tout de même afficher une page non traduite sous la forme d'un lien clairement signalé vers l'original anglais (voir `site/README.md`, « Translation-pending pages ») |

Seules les phases 4 (build autonome) et 5 (bascule) restent à faire.
