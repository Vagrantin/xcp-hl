---
layout: default
title: Journal des modifications
parent: Français
nav_order: 7
lang: fr
---

# Journal des modifications
{: .no_toc }

Changements au niveau du projet, tous dépôts XCP-ng HL confondus, avec les
tickets qu'ils résolvent. Les versions des composants pour chaque release se
trouvent dans la [matrice des versions](release-matrix.html).
{: .fs-6 .fw-300 }

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Septembre 2026

### Stockage ISO par défaut, qui clôt [#2](https://github.com/Vagrantin/xcp-hl/issues/2) et [#46](https://github.com/Vagrantin/xcp-hl/issues/46)

Un hôte XCP-ng fraîchement installé n'a nulle part où ranger les ISO
d'installation : aucun SR d'ISO n'existe et en créer un demande un
`xe sr-create` manuel sur un répertoire que vous devez créer vous-même.
XCP-HL réserve désormais une partition de 20 Go à l'installation, la formate
en ext4 sous l'étiquette `xcphl-iso`, la monte sur
`/var/opt/xen/xcp-hl-iso` et l'enregistre au premier démarrage comme SR d'ISO
nommé **XCP-HL ISO library**, prêt à recevoir des envois depuis Xen
Orchestra.

Cela porte la taille de disque minimale de XCP-HL à **100 Go** : ~41,5 Go de
partitions système, 20 Go de bibliothèque d'ISO, ~38,5 Go restants pour le
stockage des VM. En dessous, la réservation est ignorée plutôt que de réduire
le stockage des VM à quelques Go, et le disque est partitionné exactement
comme le ferait XCP-ng standard.

Le ticket [#46](https://github.com/Vagrantin/xcp-hl/issues/46) demandait si le
point d'envoi de XCP-ng pouvait recevoir une route spécifique aux ISO. Il
s'est avéré qu'il n'en avait pas besoin : `PUT /import_raw_vdi` est un import
générique de VDI brut que XO 5 pilote déjà via *Import → Disk*, et il ne
manquait qu'un SR d'ISO où importer. Aucun nouveau point d'accès n'a été
ajouté.

La partition est créée par l'installateur : cela ne concerne donc que les
installations neuves de XCP-HL. Les hôtes installés depuis XCP-ng standard qui
ajoutent ensuite les dépôts XCP-HL ne sont jamais repartitionnés, et les mises
à niveau conservent la partition existante au lieu de la recréer.

Livré en modifiant `host-installer` à l'intérieur de `install.img` au moment
de la construction de l'ISO, plutôt qu'en livrant un RPM `host-installer`
dérivé. Voir
[xcp-ng-ce-iso](developers/xcp-ng-ce-iso.html#host-installer-patching).

## Août 2026

### La matrice des versions indique le paquet exact livré, avancée sur [#15](https://github.com/Vagrantin/xcp-hl/issues/15)

La [matrice des versions](release-matrix.html) ne consignait qu'un tag de
release par composant. Pour `xoa-proxy`, cela ne suffisait pas à identifier ce
qu'un hôte exécute : le tag correspond à une version, mais le champ release du
RPM porte l'exécution de CI et le commit source, et les deux lignes les plus
anciennes portent un tag d'exécution de build `v-proxy-automated-*` qui
n'indique aucune version.

Chaque ligne par ISO affiche désormais le paquet tel que `rpm -q` l'écrit
(`xoa-proxy-0.1.1.8-55.gc525575.static.x86_64`), sous une version qui renvoie
vers sa page de release, aussi bien pour l'ISO que pour `xolite-ce` et
`xoa-proxy`. Les lignes existantes ont été complétées à partir des artefacts
de release publiés, et la version amont de xo-lite pour `v8.3-ce3` et
`v8.3-ce4` a été corrigée de 0.22.0 en 0.21.0 pour correspondre au RPM que ces
builds livrent réellement. L'orchestrateur consigne le nouveau champ à chaque
build (`xcp-orchestrator`, `shared/src/github.rs`).

---

## Juillet 2026

### Les images de VM XOA sont publiées sur build-xoa-hl, corrige [#22](https://github.com/Vagrantin/xcp-hl/issues/22)

La VM XOA-HL (`xoa-image-<date>-<sha7>`, artefact `xoa-almalinux.xva`) était
publiée sur [`xoa-hl`](https://github.com/Vagrantin/xoa-hl), le dépôt qui
construit le *logiciel*, mêlée à ses releases de RPM. Elle est désormais
publiée sur [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl), le
dépôt qui construit réellement l'image. Le `xoa-vm-agent` de l'orchestrateur y
crée la release, et le bouton de déploiement de XO Lite résout la dernière
image depuis ce dépôt.

Ce mélange avait un coût concret : `releases/latest` sur `xoa-hl` renvoyait
vers une release d'image sans artefact RPM, ce qui cassait la recherche de RPM
dans `build-xoa-hl/scripts/setup-xoa-builder.sh` ; le script parcourt
désormais les releases pour trouver la plus récente qui livre réellement un
RPM.

Les images publiées avant ce déplacement restent sur `xoa-hl`, afin que les
ISO déjà livrées continuent de les résoudre ; la
[matrice des versions](release-matrix.html#xoa-hl-releases) fait le lien entre
chaque entrée et le dépôt qui l'héberge.

### La matrice des versions consigne les versions de XOA, corrige [#13](https://github.com/Vagrantin/xcp-hl/issues/13)

La [matrice des versions](release-matrix.html) comporte désormais un tableau
dédié aux **versions de l'appliance XOA**, qui consigne chaque image de VM
publiée (release `xoa-image-*` sur `Vagrantin/xoa-hl`), la version du logiciel
`xoa-hl` qu'elle contient, et la version amont de Xen Orchestra dont elle est
dérivée. Le tableau par ISO a également perdu une colonne `xoa-hl` jamais
remplie : l'appliance est résolue au moment du déploiement et versionnée
indépendamment de l'ISO.

### L'édition XOA-HL est complète, corrige [#1](https://github.com/Vagrantin/xcp-hl/issues/1) et [#6](https://github.com/Vagrantin/xcp-hl/issues/6)

Xen Orchestra HomeLab Edition est désormais construit depuis les sources,
empaqueté et déployable de bout en bout :

- [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) construit XO 5.113.2 (la
  dernière version XO 5.x) à partir d'un commit amont figé et modifie
  l'interface : les entrées de menu soumises à licence (Hub, XOA, Proxies,
  XOSTOR) et le bandeau d'absence de support sont masqués
  (`patches/menu-hide-items.patch`).
- [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) l'empaquette en
  une appliance XVA auto-configurable, via Packer sur XCP-ng.
- La vue de déploiement de XO Lite propose désormais **XOA HomeLab (latest
  build)** comme image de déploiement, en résolvant au moment du déploiement
  la dernière XVA construite par l'agent depuis les releases GitHub (commit
  `6abd43f` de `xolite-ce`, 14/07/2026).

### Publication des releases automatisée, corrige [#4](https://github.com/Vagrantin/xcp-hl/issues/4)

Le versionnage et les notes de version sont désormais dérivés
automatiquement dans chaque chaîne de build :

- `xolite-ce` et `xoa-proxy` dérivent le tag de release et la version RPM dans
  la CI (`xolite-ce` `7b2e4d4`, `xoa-proxy` `9582718`) ; les releases de
  `xoa-proxy` utilisent les notes de version générées par GitHub, tandis que
  `xolite-ce` et l'ISO livrent des corps de release structurés, avec les
  versions des sources et les étapes de vérification.
- Le build de l'ISO est déclenché par l'orchestrateur avec les tags de release
  exacts des composants figés en entrées de workflow, ce qui élimine les
  situations de concurrence où un RPM obsolète était intégré
  (`xcp-ng-ce-iso` `68f211d`).
- Chaque release d'ISO est consignée dans la
  [matrice des versions](release-matrix.html).

---

## Juin 2026

### CI/CD du site de documentation, corrige [#5](https://github.com/Vagrantin/xcp-hl/issues/5)

Le site du projet (ce site) est construit avec Jekyll et déployé
automatiquement sur GitHub Pages à chaque push sur `main` de
[`xcp-hl`](https://github.com/Vagrantin/xcp-hl)
(`.github/workflows/pages.yml`), ce qui en fait la source unique de vérité sur
l'état du projet, matrice des versions pilotée par les données comprise.

---

## Mai 2026

### Modèle de clés GPG implémenté, corrige [#3](https://github.com/Vagrantin/xcp-hl/issues/3)

La signature GPG est harmonisée dans toutes les chaînes de build selon un
modèle **clé maîtresse hors ligne + deux sous-clés de signature** : une
sous-clé signe les RPM (`xo-lite-ce`, `xoa-proxy`), l'autre signe le fichier
de somme de contrôle de l'ISO. La clé publique est publiée sur
[keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com)
et les étapes de vérification sont livrées dans chaque corps de release. Voir
[Signature GPG](developers/#gpg-signing) pour les détails. Un affinage
ultérieur (une clé par module) reste sur la
[feuille de route](roadmap.html#gpg-keys--one-signing-key-per-module).
