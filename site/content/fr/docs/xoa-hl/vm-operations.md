---
title: Gérer une VM — snapshots, CPU, mémoire et suppression
description: Utiliser une VM de test, modifier ses CPU et sa mémoire et comprendre sa suppression.
weight: 21
translationKey: xoa-manual-vm-operations
translationStatus: draft
sourceRevision: sha256:1a66f11d2aaac01ec9a5810382d791682e4e0cf84380a3511c118c219386e5eb
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Pour ce premier exercice, utilisez une VM jetable sans données de production. Connectez-vous à l’**appliance XOA-HL** comme administrateur et vérifiez que la VM, l’hôte et le stockage sont disponibles. Avant de modifier une VM importante, conservez une [sauvegarde indépendante et testez sa restauration](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests d’alimentation, de snapshot/retour au snapshot, de clonage, de modification des CPU/mémoire et de suppression sur cette appliance restent à faire. Les versions ultérieures peuvent différer.
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

## 6. Modifier les ressources d’une VM arrêtée

Prévoyez une fenêtre de maintenance et un invité jetable dont la console est accessible. Notez son ID, son état, ses valeurs CPU/mémoire et leurs limites avant toute modification. Vérifiez la capacité de l’hôte/du pool et les besoins de l’invité ; ce guide ne prescrit pas un nombre de CPU ou une taille mémoire universels.

{{< callout type="warning" >}}
Arrêtez proprement l’invité et confirmez **Halted** avant cet exercice. Une modification à chaud peut proposer un redémarrage normal ou forcé si la valeur ne peut pas être changée en fonctionnement. Annulez cette proposition ici et organisez d’abord l’arrêt. Augmenter une limite ne garantit pas les ressources disponibles sur l’hôte ; réduire la mémoire peut empêcher le démarrage de l’invité.
{{< /callout >}}

1. Ouvrez **Avancé** (`/#/vms/<id>/advanced`) et notez **Limites de CPU** et **Limites de mémoire (min/max)**. La ligne CPU affiche les valeurs courante/maximale ; le maximum est modifiable lorsque la VM ne fonctionne pas. Pour un nombre de CPU supérieur au maximum noté, augmentez d’abord ce maximum avec la VM arrêtée.
2. Ouvrez **Général** (`/#/vms/<id>/general`). Cliquez sur le nombre de CPU, saisissez l’entier positif souhaité et appuyez sur **Entrée**. Attendez, actualisez et relisez la valeur avant de passer à la modification suivante. Ces champs peuvent aussi enregistrer lorsqu’ils perdent le focus ; cliquer ailleurs n’est pas une façon sûre d’annuler une modification.
3. Cliquez sur la valeur mémoire et utilisez le contrôle de taille/unité pour la quantité souhaitée ; appuyez sur **Entrée**. La valeur affichée est le **maximum dynamique** configuré, pas une mesure de la RAM utilisée dans l’invité. Selon les limites existantes, le serveur modifie une configuration à mémoire fixe ou les limites de mémoire dynamique.
4. Actualisez **Général** et **Avancé**, puis notez toutes les valeurs obtenues. Le nombre de CPU ne doit pas dépasser son maximum. Les bornes mémoire doivent rester ordonnées : minimum statique ≤ minimum dynamique ≤ maximum dynamique ≤ maximum statique. Les sources montrent que des limites liées peuvent être ajustées ; ne supposez pas que seul le champ cliqué a changé. Ce pilote ne valide ni le hotplug, ni la mémoire dynamique sous charge, ni le réglage de la topologie CPU.
5. Démarrez la VM de test et vérifiez sa console, les CPU/mémoire visibles dans l’invité et la santé de l’application. Si elle ne démarre pas ou si les valeurs sont inattendues, gardez-la arrêtée, conservez l’erreur de tâche et rétablissez la configuration notée dans la même fenêtre maîtrisée. Relisez chaque limite et ne réessayez qu’après avoir identifié la cause ; une notification de succès ne suffit pas.

Si une modification signale une erreur, inspectez les valeurs réelles avant de réessayer. Les changements liés ne constituent pas une transaction atomique garantie ; un refus ne prouve pas que toutes les anciennes valeurs ont été rétablies. Gardez le [dépannage](/docs/xoa-hl/troubleshooting/) et l’état initial noté à portée de main.

## 7. Supprimer uniquement la VM jetable

{{< callout type="warning" >}}
**Supprimer** est une opération destructive sur la VM, distincte de la déconnexion ou du détachement d’un disque. La confirmation ordinaire de cette version ne propose pas de conserver les disques. La suppression traite aussi les snapshots de la VM et tente de supprimer les VDI de ses disques attachés. Si des données ou un snapshot doivent être conservés, arrêtez-vous avant la confirmation et préparez une procédure de préservation séparée. Un snapshot de cette VM n’est pas une copie de récupération indépendante.
{{< /callout >}}

1. Confirmez que la cible est la VM jetable, pas l’appliance, l’invité d’origine, un modèle ou une autre VM au nom proche. Notez son ID, les ID/SR de ses disques attachés et ses snapshots. Vérifiez ses planifications de sauvegarde/réplication et les autres utilisateurs de disques partagés avant la suppression. Pour des données importantes, effectuez d’abord une [sauvegarde indépendante et un test de restauration isolé](/docs/xoa-hl/backup-restore/).
2. Arrêtez normalement l’invité et confirmez **Halted**. Le serveur de suppression peut arrêter brutalement une VM encore en fonctionnement ou suspendue ; n’utilisez pas **Supprimer** comme commande d’arrêt propre.
3. Ouvrez **Avancé** et choisissez **Supprimer**. Lisez l’avertissement sur la VM et ses disques, puis ne confirmez que cette cible prévue. Si XO propose ensuite de supprimer malgré une protection/un blocage, annulez ce pilote et examinez la protection au lieu d’accepter une nouvelle tentative forcée.
4. Attendez, puis actualisez les inventaires des VM, snapshots et disques des SR. Vérifiez les ID notés ainsi que la tâche et ses erreurs. Ce chemin de code ignore les VDI partagés encore attachés à une autre VM qui n’est pas un domaine de contrôle ; cette exception ne garantit pas la conservation de chaque disque. Des erreurs de nettoyage de snapshot/VDI peuvent être journalisées sans faire échouer toute la suppression ; la disparition de la VM ou une notification de succès ne prouve donc pas un nettoyage complet.
5. Confirmez que la VM d’origine, les autres invités et toute sauvegarde indépendante nécessaire restent utilisables. Examinez chaque objet de test restant à l’aide des [distinctions de gestion des disques](/docs/xoa-hl/storage-networks/) et des ID notés. Ne supprimez pas en masse des disques apparemment orphelins et ne relancez pas une opération forcée pour récupérer de l’espace. Ce guide n’offre pas d’annulation ; récupérer des données invitées supprimées exige une copie de récupération vérifiée séparément.

Si la suppression échoue en cours de route ou si vous annulez la confirmation après un blocage, conservez l’inventaire restant des VM/disques/snapshots et l’erreur. Si la VM existe encore, inspectez aussi ses permissions, réservations de pool IP et appartenance à un ensemble de ressources : l’API commence certaines opérations de gestion avant le contrôle de protection contre la suppression, donc un refus ne garantit pas que ces enregistrements sont inchangés. Ne recréez pas une VM au nom semblable en supposant qu’il s’agit du même objet. [Signalez le problème](/docs/xoa-hl/troubleshooting/) avec les versions et des ID anonymisés avant de poursuivre le nettoyage.

## Sources

Modification des ressources/suppression au même commit : [contrôles Général](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [limites/Supprimer dans Avancé](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [enregistrement des champs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [permissions/paramètres VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [ordre des contraintes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [suppression/disques partagés/nettoyage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [libellés/avertissements anglais](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).

Version XO 5 `e281c536` : [actions d’alimentation et de snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [barre d’actions VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [onglet snapshots](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [confirmation de retour au snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js) et [état après retour au snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
