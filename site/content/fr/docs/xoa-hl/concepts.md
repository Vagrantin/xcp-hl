---
title: "Concepts et périmètre fonctionnel"
linkTitle: "Concepts"
description: "Comprenez les composants, les numéros de version et ce que contient cette version."
weight: 90
translationKey: xoa-manual-concepts
translationStatus: draft
sourceRevision: sha256:16d96a198271a59f01a3879f316b87511123b62129dcde83c40e8e7d8dbe06ef
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Cette page de référence indique sur quel composant vous travaillez, ce que signifient les numéros de version et ce que contient cette version. Elle ne contient pas d’étapes à suivre. Consultez-la avant de vous appuyer sur une fonction, ou quand vous signalez un problème.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261009-5f33c81`, paquet `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire.
{{< /callout >}}

## Composants et adresses {#components}

| Composant | Rôle | Où l’atteindre |
| --- | --- | --- |
| Hôte hyperviseur ou pool | Exécute les VM et fournit l’interface de gestion XAPI | L’adresse de gestion de l’hôte |
| XO Lite CE | Une interface web servie par l’hôte. Elle déploie et retrouve l’appliance | L’adresse HTTPS de l’hôte |
| Appliance XOA-HL | Une VM distincte qui exécute xo-server, l’interface web XO 5 et Redis | L’adresse HTTPS de l’appliance |

Pour voir comment ces éléments s’articulent, lisez le [guide d’architecture et de déploiement](/docs/start/#start-architecture). Gérez chaque hôte ou pool avec un seul gestionnaire pris en charge. Lisez [Hôtes et pools](/docs/xoa-hl/hosts-pools/) avant de déplacer une connexion. Les mises à jour de l’hôte et celles de l’appliance sont distinctes, avec leurs propres cibles et calendriers : consultez le [guide des mises à jour](/docs/guides/updates/).

## VM, stockage et protection {#objects}

Une **VM** s’exécute sur un hôte d’un **pool**. Un **dépôt de stockage (SR)** contient les disques virtuels. L’interface réseau d’une VM se connecte à un réseau du pool. Les noms ne sont que des libellés : utilisez les identifiants d’objet pour automatiser.

Un **snapshot** enregistre l’état d’une VM à un instant donné, sur le même stockage. Une **sauvegarde** copie les données vers une destination de sauvegarde distincte. Un snapshot seul ne vous protège pas si ce stockage est perdu, et un job de sauvegarde réussi doit encore être suivi d’un test de restauration.

Pour en savoir plus, consultez le [glossaire](/docs/xoa-hl/glossary/), [Stockage et réseaux](/docs/xoa-hl/storage-networks/) et [Sauvegarder et restaurer une VM](/docs/xoa-hl/backup-restore/).

## Numéros de version {#versions}

| Version | Signification |
| --- | --- |
| XO 5.113.2, commit amont `e281c536` | La version de Xen Orchestra pour l’application et l’interface web. Elle a été choisie délibérément : ce n’est pas XO 6 |
| `xo-server` 5.193.1 | La version du paquet serveur dans cette même version. Sa numérotation est différente |
| `v5.113.2_e281c536-ce38` | La version du paquet XOA-HL, avec son ensemble de correctifs |
| `xoa-image-20261009-5f33c81` | La construction de l’image de l’appliance. C’est un numéro distinct : mettre à jour l’application ne le change pas |

Notez les valeurs installées comme indiqué dans la [maintenance de l’appliance](/docs/xoa-hl/maintenance/). La [matrice des versions](/docs/reference/release-matrix/) liste les versions livrées ensemble ; cela ne signifie pas qu’elles ont passé des tests d’intégration. L’ISO d’installation ne fixe pas l’image d’appliance que vous obtenez : l’image est choisie plus tard, quand vous déployez l’appliance.

## Ce que contient cette version {#feature-scope}

| Domaine | Dans le code de cette version | Avant de vous y fier |
| --- | --- | --- |
| Alimentation des VM, snapshots, disques et réseaux | Les actions et écrans de XO 5 sont présents | Les guides du quotidien ne sont pas encore testés en laboratoire |
| Utilisateurs et droits sur les objets (ACL) | La version publiée conserve le plan amont par défaut (OpenSource). Les écrans d’ACL sont dans le code | Vérifiez l’interface installée, et testez dans une session séparée connectée en tant qu’utilisateur normal |
| Sauvegarde complète et restauration | Une procédure NFS est documentée, d’après le code | Une vraie sauvegarde et une restauration isolée ne sont pas encore testées |
| Mises à jour de l’appliance | API de mise à jour XOA-HL, canaux `stable` et `testing`, et calendriers réglables | Suivez le guide des mises à jour de votre version |
| Menus Hub, section XOA de Vates, proxys de sauvegarde et XOSTOR | Un correctif de menu de ce paquet masque ces entrées | Un menu masqué n’en fait pas une fonction prise en charge. Il ne prouve pas non plus que l’API correspondante a disparu |

Cette version du paquet déclare 14 correctifs. Ils ne signifient pas que chaque option amont a été testée. Les abonnements Vates, le support commercial et les interfaces XO 6 ne s’appliquent pas à ce paquet. Avant de vous appuyer sur une fonction, consultez [Utilisateurs et droits](/docs/xoa-hl/permissions/) et le guide de la tâche.

## Pages associées {#related}

- [Paramètres du service](/docs/xoa-hl/configuration/) : les fichiers de configuration de xo-server.
- [Automatiser avec xo-cli](/docs/xoa-hl/automation/) : lire l’inventaire en ligne de commande avec un jeton de courte durée.
- [Export de la configuration](/docs/xoa-hl/configuration-backup/) : enregistrer les réglages et les données de l’interface web.
- [xoa-hl](/docs/components/xoa-hl/) et [build-xoa-hl](/docs/components/build-xoa-hl/) : comment le paquet est fabriqué. Les builds du produit se font uniquement en CI.

Quand vous proposez une modification de cette documentation, indiquez les versions de l’image et du paquet que vous utilisez.

{{< details title="Sources" closed="true" >}}
- **Versions, correctifs et construction** : [version amont de XO (`UPSTREAM_XO`)](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [liste des correctifs](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/metadata.toml), [correctif qui masque des menus](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/menu-hide-items.patch), [définition du paquet](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [version du paquet xo-server](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [construction de l’interface web](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
{{< /details >}}
