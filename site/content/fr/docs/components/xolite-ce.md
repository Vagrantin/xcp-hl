---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/fr/developers/xolite-ce.html"]
---

Correctif communautaire pour XO Lite et chaîne de build du RPM.
{class="lead"}

**Dépôt :** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Langage : TypeScript / Vue 3 (correctif) · spec RPM · Licence : AGPL-3.0

## Qu'est-ce que XO Lite ?

XO Lite est l'application de gestion légère, en page unique, fournie avec
chaque hôte XCP-ng. Elle s'exécute entièrement dans le navigateur, servie
directement par l'hôte, et se présente sous la forme d'une SPA
Vue 3 / TypeScript / Vite.

Sur un hôte XCP-ng standard, XO Lite comprend un écran **« Deploy XOA »**
(`xoa-deploy.vue`) qui télécharge et importe l'image Xen Orchestra
officielle. XCP-hl remplace ce comportement pour vous laisser choisir
l'image XOA que vous souhaitez déployer.

---

## Correctif au niveau du code source

`UPSTREAM_TAG` épingle `xo-lite-v0.21.0` à
`13f987ff3d34504a90b89178489e15fa2293d1b3`. XO Lite CE modifie ce code
source au moyen de diffs unifiés relisibles. `patches/series` définit
l'ordre des diffs et `patches/metadata.toml` enregistre, pour chaque patch,
l'objectif, la cible, le responsable, le commit amont et les dépendances.
La série contient `xoa-button-empty.patch` pour `XoaButton.vue` et
`010-xoa-deploy.patch` pour `xoa-deploy.vue`. Les builds et la validation
partagent `scripts/patch-source.sh`, qui applique aussi les transformations
explicites, hors diffs, des locales, du chargeur, des versions hôte/invité
et des secrets de déploiement. Preuves : `xolite-ce/patches/series@ad43fa2`,
`xolite-ce/patches/metadata.toml@ad43fa2` et
`xolite-ce/scripts/patch-source.sh@ad43fa2`.

Avant la [PR #26](https://github.com/Vagrantin/xolite-ce/pull/26), fusionnée le
31 octobre 2026 sous `4506112`, un exécutable Rust embarqué réécrivait
`xoa-deploy.vue`. Le diff l'a remplacé sans modifier l'épinglage amont ni
les octets sources finaux.

Voir [l'évaluation du modèle de correctif multi-composants](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md)
pour le dossier de décision. Le
[guide de maintenance du composant](https://github.com/Vagrantin/xolite-ce/blob/ad43fa282dca7023776a142cb4250e96226d8312/docs/patching.md)
fixe les règles de nommage, d'ordre et de métadonnées.

---

## Validation des sources

Utilisez une extraction amont propre, épinglée. Dans l'arbre XO Lite CE :

```sh
python3 scripts/list-patches.py patches
python3 ci/test-patch-series.py
bash scripts/patch-source.sh /path/to/clean/pinned/upstream
```

La série complète est vérifiée avant l'application du moindre diff. Les noms
invalides, les entrées manquantes ou dupliquées, les incohérences de
métadonnées et un ordre de dépendances invalide font échouer la validation.
Ne sautez pas un patch en échec et ne le remplacez pas par un chargeur
distant. Les tests sources existants vérifient séparément l'interface
touchée, les locales et le nettoyage du déploiement.

`docs/patch-migration.json` enregistre l'empreinte de l'exécutable retiré et
les révisions immuables du consommateur, de l'amont et des sources du
patcheur. `ci/test-patch-migration.py` compare tous les octets sources, les
modes exécutables Git et les cibles de liens symboliques entre l'ancienne
chaîne et la chaîne actuelle. La CI reconstruit en outre la source Rust
épinglée et vérifie sa sortie contre l'exécutable enregistré. C'est une
traçabilité comportementale sur une entrée épinglée, pas une
reproductibilité binaire historique.

---

## Builds et acceptation

Tous les builds applicatifs et RPM s'exécutent dans GitHub Actions. Sur les
pull requests, `check-patch-series.yml` exécute la chaîne complète et
construit la distribution Vue patchée, sans publier de release.
L'empaquetage et la signature restent dans `build-xolite-ce.yml` et
`SPECS/xo-lite-community.spec`.

Gardez l'application des sources, les builds applicatifs hébergés, les
contrôles RPM et l'acceptation installée comme des résultats distincts. Le
build `0.21.0-39.g54c289b` contient la série de diffs unifiés.
`xcp-hl/qa/ce52-acceptance/2026-11-09.md@7a51eb1` consigne ce build sur un
hôte ce36 installé, avec des appliances déployées par le flux Custom URL
livré dans `#/xoa-deploy`. Les autres sources d'image, les autres hôtes et
une comparaison installée avant/après restent non vérifiés.

---

## Signature GPG

Le RPM `xo-lite-ce` est signé avec la **signing subkey RPM** de
la paire de clés XCP-hl. La même sous-clé sert aussi à signer les RPM
`xoa-proxy` et `xcp-hl-release` : il n'y a qu'une sous-clé partagée pour tous les
RPM communautaires.

Le projet publie sa [clé publique](https://www.xcp-hl.org/xcp-ng-ce-public.asc)
à la racine du site de production. Vérifiez l’empreinte de la clé principale avant
de l’importer. Les commandes ci-dessous nécessitent une version de RPM prenant
en charge les sous-clés de signature. Le Dom0 de XCP-ng 8.3 utilise RPM 4.11 ;
les hôtes valident donc les métadonnées signées avec `repo_gpgcheck=1`. Conservez
les paramètres de dépôt décrits dans [Mises à jour](/docs/guides/updates).

Pour vérifier le RPM en local :

```bash
curl -fLO https://www.xcp-hl.org/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Contribuer

Pour signaler un problème ou proposer une modification, ouvrez un ticket sur
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
