---
title: Gérer les disques et le réseau
description: Ajouter un disque de test et une interface isolée sans modifier le réseau de gestion.
weight: 22
translationKey: xoa-manual-storage-networks
translationStatus: draft
sourceRevision: sha256:707daba14083e52696337827be5317053e28a178e872d1824f84603a0c6fccec
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Utilisez une VM jetable arrêtée, avec un compte administrateur dans l’**appliance XOA-HL**. Notez son identité, ses disques et interfaces existants. Choisissez un SR inscriptible avec assez d’espace libre et un réseau existant dont l’isolation a été vérifiée en dehors de XO. N’utilisez pas l’appliance comme invité de test.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests de disque, d’interface et de détection dans l’invité sur l’appliance publiée restent à faire.
{{< /callout >}}

## 1. Identifier les objets

| Objet | Signification |
| --- | --- |
| SR | Dépôt de stockage contenant les disques virtuels ; vérifiez son espace libre |
| VDI | Données d’un disque virtuel stockées dans un SR |
| VBD | Attachement entre une VM et un disque virtuel |
| VIF | Interface réseau virtuelle d’une VM |
| PIF | Interface réseau de l’hôte ; modifier la connectivité de gestion peut déconnecter l’hôte |

L’interface d’une VM n’est pas celle de gestion de l’hôte. Choisir un réseau ou générer une MAC ne crée pas d’isolation ; vérifiez le VLAN, la liaison physique et le routage avant d’y connecter un invité cloné ou restauré.

## 2. Ajouter un petit disque vide

1. Confirmez l’arrêt de la VM de test. Ouvrez **Disks** (`/#/vms/<id>/disks`) et choisissez **New disk**.
2. Choisissez le SR inscriptible prévu dans le même pool, un nom de test explicite et une petite taille avec ses unités. Vérifiez l’option lecture seule ; laissez-la désactivée pour un disque de test inscriptible. Lancez la création une seule fois et attendez sa fin.
3. Vérifiez le nom, la taille, le SR et l’attachement à la bonne VM dans la nouvelle ligne. Notez l’identité du disque et l’espace restant avant de démarrer l’invité.

Dans la console de l’invité, identifiez le nouveau disque par sa taille et ses informations. XO crée le disque virtuel et son attachement ; il ne le partitionne, ne le formate et ne le monte pas automatiquement dans l’invité. Les procédures de système de fichiers dépassent ce pilote. Ne formatez pas un périphérique sur la seule base d’un nom supposé.

En cas d’échec, examinez la tâche et les inventaires VM/SR avant de réessayer : une opération partielle peut laisser un disque. Conservez l’erreur, vérifiez l’espace et la connectivité et [utilisez le dépannage](/docs/xoa-hl/troubleshooting/) si nécessaire. Cet exercice ne valide pas la réduction, l’extension ou la migration du stockage.

## 3. Distinguer détachement et suppression

Supprimer le VBD détache le disque de la VM, sans signifier que les données du VDI sont supprimées. Supprimer le VDI détruit les données ; c’est une autre action, indisponible tant que le disque est attaché dans cette interface. Déconnecter un attachement est aussi distinct de le supprimer.

Pour le nettoyage, arrêtez l’invité et identifiez précisément le seul disque de test vide. Conservez le VDI si son contenu peut être utile. Ne supprimez jamais un disque de démarrage, partagé ou non identifié pour résoudre un avertissement d’espace. [Sauvegardez les données importantes](/docs/xoa-hl/backup-restore/) séparément.

## 4. Ajouter une interface VM isolée

Sur la VM de test arrêtée, ouvrez **Network** (`/#/vms/<id>/network`) et choisissez **New device**. Sélectionnez le réseau isolé vérifié dans le même pool. Laissez la MAC vide pour sa génération automatique, puis choisissez **Create**. Vérifiez l’interface, son réseau et sa MAC avant le démarrage, puis la détection et la connectivité prévues dans l’invité.

Pour un clone ou une restauration isolés, supprimez **toutes** les VIF héritées pendant l’arrêt et confirmez que la liste est vide avant le premier démarrage. Utilisez la suppression de l’interface, pas seulement son commutateur de connexion : la simple déconnexion n’est pas la procédure d’isolation. N’ajoutez un réseau de test qu’après avoir confirmé qu’il n’atteint pas la production et résolu les identités copiées.

Si la connectivité est inattendue, arrêtez la VM de test et inspectez le réseau choisi et l’isolation externe avant de réessayer. Ce guide ne configure pas les PIF, adresses de gestion, agrégations ou VLAN de l’hôte. Ne modifiez pas le réseau de gestion de l’hôte pendant cet exercice. Poursuivez avec [les opérations VM](/docs/xoa-hl/vm-operations/) ou [la gestion des hôtes et pools](/docs/xoa-hl/hosts-pools/).

## Sources

Version XO 5 `e281c536` : [interface des disques et sélection du SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [interface réseau VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js) et [actions disque/interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
