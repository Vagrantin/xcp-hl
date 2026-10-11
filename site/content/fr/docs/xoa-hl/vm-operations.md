---
title: Gérer une VM et ses snapshots
description: Démarrer et arrêter une VM de test, créer un snapshot et préparer un clone isolé.
weight: 21
translationKey: xoa-manual-vm-operations
translationStatus: draft
sourceRevision: sha256:2ba0c0496c68e8303779ca864433625d5588c48ef4cdecb71930103c61012066
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Pour ce premier exercice, utilisez une VM jetable sans données de production. Connectez-vous à l’**appliance XOA-HL** comme administrateur et vérifiez que la VM, l’hôte et le stockage sont disponibles. Avant de modifier une VM importante, conservez une [sauvegarde indépendante et testez sa restauration](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests d’alimentation, de snapshot/retour au snapshot et de clonage sur cette appliance restent à faire. Les versions ultérieures peuvent différer.
{{< /callout >}}

## 1. Démarrer, arrêter et redémarrer

Ouvrez la VM choisie (`/#/vms/<id>/general`). Si elle est arrêtée, choisissez **Start** et attendez que son état et sa console montrent le démarrage du système invité. Si elle fonctionne, **Stop** ou **Reboot** demande d’abord un arrêt ou un redémarrage propre de l’invité.

Si le support côté invité manque ou si une opération est bloquée, XO peut proposer une nouvelle confirmation pour forcer l’opération ou contourner le blocage. Lisez ce message avant de continuer. Un arrêt/redémarrage forcé peut perdre des données ; utilisez si possible l’arrêt depuis l’invité. Ne cliquez pas plusieurs fois pendant une tâche. Vérifiez l’état et la console après sa fin ; une notification de succès ne prouve pas que l’application fonctionne correctement.

## 2. Choisir la protection adaptée

| Élément | Objectif et limite |
| --- | --- |
| Snapshot | État de la VM à un instant donné, dépendant de son stockage ; pas une sauvegarde indépendante |
| Clone rapide | Autre VM utilisant une copie économe en stockage ; ne protège pas contre la perte de ce stockage |
| Sauvegarde | Copie de récupération séparée ; à valider par une restauration isolée |

Les snapshots et clones consomment du stockage lorsque les VM changent. Vérifiez l’espace libre du SR et ne supprimez que les objets de test clairement identifiés. Un snapshot à chaud ne prouve pas la cohérence applicative.

## 3. Créer et vérifier un snapshot à froid

1. Arrêtez l’invité jetable et confirmez son état arrêté. Notez l’identité de la VM, ses disques et un fichier ou réglage sans importance à comparer ensuite.
2. Ouvrez **Snapshots** (`/#/vms/<id>/snapshots`) et choisissez **New snapshot**. N’utilisez pas l’option mémoire pour cet exercice.
3. Attendez la fin. Identifiez la nouvelle ligne par sa date et donnez-lui un nom de test explicite. Vérifiez les erreurs de tâche et l’espace restant.

En cas d’échec, conservez l’erreur et vérifiez l’espace et la connectivité avant de réessayer. L’absence de notification ne signifie pas qu’aucun snapshot n’a été créé.

## 4. Revenir au snapshot de la VM de test

Modifiez les données de test sans importance, arrêtez à nouveau l’invité, puis choisissez **Revert VM to this snapshot** sur le snapshot noté. Cette opération remplace l’état actuel de la VM. La confirmation propose de créer d’abord un snapshot de l’état courant, option activée par défaut dans cette version ; vérifiez ce choix et l’espace disponible.

Pour un snapshot pris en fonctionnement, XO peut démarrer ou reprendre la VM après le retour au snapshot. Utilisez ici un snapshot à froid et vérifiez l’état obtenu avant tout démarrage manuel. Démarrez l’invité lorsque cela convient et vérifiez le fichier/réglage noté et ses disques. Ne faites pas cet exercice sur l’appliance ou une VM de production.

## 5. Préparer un clone rapide isolé

Sur une VM jetable arrêtée, choisissez **Fast clone**. Repérez la nouvelle VM (nom par défaut terminé par `_clone`), notez son identité distincte et renommez-la. Gardez-la arrêtée pendant que vous [supprimez toutes ses interfaces réseau héritées](/docs/xoa-hl/storage-networks/) ou établissez une isolation externe vérifiée. Une MAC générée automatiquement n’efface pas les adresses IP, identifiants et identités applicatives copiés.

Démarrez ensuite le clone et inspectez sa console. Ne reconnectez un réseau qu’après avoir résolu les identités dupliquées et vérifié l’isolation. Si aucun clone n’apparaît après une erreur, examinez l’inventaire et les tâches avant de réessayer. Cet exercice ne valide ni la migration à chaud, ni les snapshots mémoire, ni la récupération après perte du SR.

## Sources

Version XO 5 `e281c536` : [actions d’alimentation et de snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [barre d’actions VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [onglet snapshots](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [confirmation de retour au snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js) et [état après retour au snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
