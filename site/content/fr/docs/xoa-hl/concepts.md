---
title: "Concepts et périmètre fonctionnel"
linkTitle: "Concepts"
description: "Comprenez les composants, les numéros de version et le contenu de cette version."
weight: 90
translationKey: xoa-manual-concepts
translationStatus: draft
sourceRevision: sha256:5f34ed54ff2d136c85d8ea8fca3bdebf785565736c3dad46a9c10bdb8638f5fe
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Cette page identifie le composant sur lequel vous intervenez et les limites des affirmations concernant ses fonctions.

{{< callout type="info" >}}
Référence vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les versions suivantes peuvent différer. La validation sur appliance installée et la revue humaine des traductions restent à faire.
{{< /callout >}}

## Composants et adresses

| Composant | Rôle | Adresse |
| --- | --- | --- |
| Hôte hyperviseur / pool | Exécute les VM et expose XAPI | Adresse de gestion de l’hôte |
| XO Lite CE | Interface servie par l’hôte ; déploiement/découverte de l’appliance | Adresse HTTPS de l’hôte |
| Appliance XOA-HL | VM distincte exécutant xo-server, l’interface XO 5 et Redis | Adresse HTTPS de l’appliance |

Consultez le [guide d’architecture et de déploiement](/docs/start/#start-architecture). Gardez un seul gestionnaire pris en charge par hôte/pool ; utilisez le [guide de gestion et de découverte](/docs/xoa-hl/hosts-pools/) avant de déplacer une connexion. Les mises à jour de l’hôte et de l’appliance ont des cibles et des calendriers distincts : [guide des mises à jour](/docs/guides/updates/).

## Objets et protection

Une **VM** s’exécute sur un hôte d’un **pool**. Un **dépôt de stockage (SR)** contient les disques virtuels ; une interface réseau VM rejoint un réseau du pool. Les noms sont des libellés : utilisez les identifiants d’objet pour automatiser. Un **snapshot** conserve un état de la VM sur son stockage ; une **sauvegarde** copie les données de protection vers une destination configurée. Un snapshot seul ne protège pas de la perte de ce stockage.

Utilisez le [glossaire contrôlé](/docs/xoa-hl/glossary/), le [guide disques/réseau](/docs/xoa-hl/storage-networks/) et le [pilote de sauvegarde complète avec restauration isolée](/docs/xoa-hl/backup-restore/). Même si le job de sauvegarde réussit, il faut tester une restauration.

## Identités de version

| Identité dans cette référence | Signification |
| --- | --- |
| XO 5.113.2 / amont `e281c536` | Version source application/interface délibérément figée ; pas XO 6 |
| `xo-server` 5.193.1 | Version du paquet serveur à ce commit ; numérotation différente |
| `v5.113.2_e281c536-ce38` | Release RPM HomeLab et ensemble de patches |
| `xoa-image-20261009-5f33c81` | Identité de construction de l’image ; reste distincte après une mise à jour de l’application |

Relevez les valeurs installées comme indiqué dans la [maintenance](/docs/xoa-hl/maintenance/). La [matrice des versions](/docs/reference/release-matrix/) indique les combinaisons livrées, pas leur validation en intégration. Un ISO ne fige pas l’image résolue ultérieurement par le déploiement.

## Périmètre des fonctions à ce38

| Domaine | Observation dans les sources | Limite de validation |
| --- | --- | --- |
| Alimentation VM, snapshots, disques et réseaux | Actions et interface XO 5 présentes | Les guides quotidiens attendent les tests en laboratoire jetable |
| Utilisateurs et ACL d’objets | Le build publié conserve le plan OpenSource amont par défaut ; interface ACL visible dans les sources | Vérifier l’interface installée et une session indépendante d’utilisateur normal |
| Sauvegarde complète et restauration | Pilote NFS vérifié dans les sources et documenté | Sauvegarde réelle et restauration isolée encore à tester |
| Mises à jour de l’appliance | API HomeLab, canaux stable/testing et calendriers configurables | Suivre le guide applicable à la version |
| Menus Hub, section XOA Vates, proxies de sauvegarde et XOSTOR | Le patch de menu ce38 masque ces entrées | Un menu masqué ne promet aucune prise en charge et ne prouve pas l’absence de chaque API |

La release contient 14 patches déclarés. Leur présence ne signifie pas que toutes les options amont ont été validées. Les abonnements Vates, le support commercial et les interfaces XO 6 ne décrivent pas ce paquet HomeLab. Consultez les [droits](/docs/xoa-hl/permissions/) et le guide de la tâche avant de vous appuyer sur une fonction.

## Référence et contribution

La [configuration du service](/docs/xoa-hl/configuration/), l’[automatisation CLI en lecture seule](/docs/xoa-hl/automation/) et l’[export de configuration](/docs/xoa-hl/configuration-backup/) concernent différents réglages et données. Pour l’implémentation et les builds de produit exclusivement en CI, lisez [xoa-hl](/docs/components/xoa-hl/) et [build-xoa-hl](/docs/components/build-xoa-hl/). Indiquez l’identité de la release avec votre proposition documentaire.

## Sources

[UPSTREAM_XO](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [patch metadata](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/metadata.toml), [menu patch](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/menu-hide-items.patch), [RPM](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [xo-server package](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [XO build plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
