---
title: Sauvegarder une VM et tester une restauration isolée
description: Conserver une sauvegarde complète sur un stockage séparé, restaurer une copie arrêtée et vérifier ses données.
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: draft
sourceRevision: sha256:95197e62eaca75f0861baa879c3c3325ab86b29442dbce0e742f847b6ea3f706
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protégez votre VM de test avec une sauvegarde complète sur un stockage séparé, puis restaurez une copie et vérifiez que ses données sont utilisables. La réussite de la tâche de sauvegarde est le début de cette vérification ; la restauration la complète.

{{< callout type="info" >}}
Procédure en prévisualisation : vérifiée dans les sources de XO 5.113.2 (`e281c536`), du paquet XOA-HL `v5.113.2_e281c536-ce38` et de l’image `xoa-image-20261009-5f33c81`. L’exécution sur un laboratoire jetable reste à faire. Ce tutoriel couvre uniquement la sauvegarde complète d’une VM vers NFS ; les autres destinations et modes nécessitent leur propre validation.
{{< /callout >}}

## Avant de commencer

- [Créez et installez une VM de test](/docs/xoa-hl/create-vm/). Utilisez un compte administrateur XOA-HL ; l’espace de sauvegarde de cette version nécessite cet accès.
- Préparez un export NFS sur un système de sauvegarde séparé, hors du stockage de la VM d’origine et de l’appliance. L’appliance doit pouvoir le joindre et créer, lire et supprimer les fichiers de sauvegarde. Demandez à l’administrateur du stockage le serveur, le chemin exporté et les options de montage requises.
- Vérifiez l’espace libre sur la destination, sur le SR d’origine pour les snapshots temporaires, et sur le SR inscriptible qui recevra les disques restaurés. Prévoyez la rétention configurée et une nouvelle exécution ; la taille compressée n’est pas garantie.
- Dans le système invité, créez un petit fichier sans données sensibles, notez son contenu ou sa somme de contrôle, et terminez son écriture avant la sauvegarde. Pour ce premier test, arrêtez normalement le système invité et vérifiez que la VM est arrêtée. Cela évite de supposer qu’une sauvegarde à chaud est cohérente au niveau applicatif.
- Réservez les ressources d’une deuxième VM. Gardez la copie restaurée arrêtée jusqu’à ce que **toutes ses interfaces réseau virtuelles soient supprimées**. Ce test par console ne nécessite aucun réseau invité.

La gestion se fait dans le **navigateur**. La création et la vérification du fichier se font dans la **VM invitée**. Aucune commande sur l’hôte ou l’appliance n’est nécessaire.

## 1. Ajouter la destination de sauvegarde

1. Ouvrez **Paramètres → Stockages distants** (`/#/settings/remotes`). Réutilisez une destination adaptée déjà vérifiée, ou créez-en une nommée `lab-backup-nfs`.
2. Choisissez **NFS**, renseignez le serveur et le chemin exporté fournis par son administrateur, puis les options de montage requises. Conservez les valeurs avancées par défaut sauf nécessité propre au stockage. N’utilisez pas un répertoire local de l’appliance pour ce test.
3. Enregistrez la destination, activez-la si nécessaire et utilisez l’action **Test your remote** (tester la destination). Lisez toute erreur de connexion ou de test avant de continuer.

**Vérification :** la destination est activée, son test réussit et aucune erreur de connexion n’apparaît. Cela vérifie l’accès, pas la capacité à restaurer une sauvegarde de VM.

## 2. Créer une tâche de sauvegarde complète

1. Ouvrez **Sauvegarde → Nouveau → VMs** (`/#/backup/new/vms`) et nommez la tâche `lab-first-vm-full`.
2. Sélectionnez explicitement votre seule VM de test. Désactivez la sélection intelligente pour éviter d’inclure d’autres VM.
3. Dans les modes, choisissez **Backup** (sauvegarde). Laissez **Rolling snapshot**, **Delta backup**, **Disaster recovery** et **Continuous replication** désactivés. Ici, **Backup** correspond à l’export complet.
4. Sélectionnez `lab-backup-nfs` dans **Target remotes (for export)** (destinations d’export). Laissez **Delete old backups first** désactivé : cette option peut supprimer des copies antérieures avant la réussite du nouvel export.
5. Ajoutez explicitement une planification. Pour cet exemple de laboratoire, réglez **Backup retention** (rétention des sauvegardes) sur `2`, choisissez un fuseau explicite comme `Asia/Tokyo` et vérifiez l’aperçu des prochaines exécutions. La rétention est un nombre de sauvegardes conservées pour cette planification, pas un nombre de jours.
6. Désactivez cette planification dans le tableau avant d’enregistrer la tâche. Ce pilote s’exécute manuellement ; ne laissez aucune planification automatique par défaut.
7. Enregistrez et vérifiez la vue d’ensemble : une seule VM attendue, la bonne destination et une planification désactivée. Conservez les paramètres avancés pour ce premier test.

{{< callout type="warning" >}}
La rétention peut supprimer des sauvegardes anciennes lors des exécutions suivantes. Utilisez une destination de laboratoire dédiée et ne réduisez jamais la rétention d’une tâche de production pour suivre cet exemple. Un snapshot sur le SR d’origine n’est pas une sauvegarde indépendante.
{{< /callout >}}

## 3. Exécuter et contrôler la sauvegarde

1. Dans **Sauvegarde → Vue d’ensemble** (`/#/backup/overview`), utilisez l’action d’exécution de la planification désactivée. Vérifiez que la confirmation désigne votre tâche et une seule VM, puis confirmez.
2. Attendez la fin. Ouvrez les journaux et contrôlez le résultat de la VM et de l’export, pas seulement le démarrage de la tâche. Examinez les avertissements, échecs et données ignorées.
3. Ouvrez **Sauvegarde → Restaurer** (`/#/backup/restore`). Retrouvez la VM de test et vérifiez que la nouvelle sauvegarde complète apparaît avec l’horodatage et la destination attendus. Actualisez la liste si nécessaire.

**Vérification :** l’exécution a réussi et le nouveau point de restauration est visible. Notez la tâche, la planification, la destination, l’horodatage et les versions installées. Vous pouvez redémarrer normalement la VM d’origine ; gardez la planification désactivée pendant le test de restauration.

## 4. Restaurer une copie arrêtée

1. Dans **Sauvegarde → Restaurer**, choisissez l’action de restauration de la VM, puis exactement la sauvegarde complète que vous venez de créer.
2. Choisissez un SR inscriptible avec assez d’espace. C’est le stockage des disques de VM, pas la destination NFS ni un SR ISO.
3. Laissez **Start VM after restore** (démarrer après restauration) **désactivé**. Activez **Generate new MAC addresses** pour donner à la copie des adresses MAC distinctes. Cela ne change pas l’adresse IP statique, le nom d’hôte ni l’identité applicative dans le système invité.
4. Confirmez et attendez la fin. Contrôlez les journaux. Identifiez la nouvelle VM par son UUID et ses disques restaurés ; ne vous fiez pas uniquement à son nom.
5. Vérifiez que la copie est arrêtée. Renommez-la `lab-first-vm-restore-test` et notez son UUID à côté de l’UUID différent de la VM d’origine.

**Vérification :** une VM distincte et arrêtée existe avec les disques attendus. Ne la démarrez pas encore. Si elle est déjà en marche, arrêtez la copie et examinez son exposition réseau avant de continuer.

## 5. Isoler, démarrer et vérifier la copie

1. Ouvrez l’onglet **Réseau de la copie restaurée** (`/#/vms/<restored-uuid>/network`). Pendant qu’elle est arrêtée, supprimez **toutes** ses interfaces réseau virtuelles et vérifiez que le tableau est vide. Un simple état déconnecté à l’exécution ne garantit pas l’isolation après un démarrage ultérieur.
2. Revérifiez l’UUID restauré et le tableau vide, puis démarrez cette copie et ouvrez **Console**. Ne modifiez pas le réseau de la VM d’origine.
3. Vérifiez le démarrage, la connexion par console et le contenu ou la somme de contrôle du fichier. Contrôlez les autres données nécessaires à votre objectif de reprise. Le démarrage seul ne valide pas une restauration applicative complète.
4. Arrêtez normalement la copie. Notez le résultat, l’horodatage de sauvegarde, la durée de restauration et les versions. À la fin, supprimez uniquement la copie de test et ses disques restaurés après vérification de son UUID ; conservez la VM d’origine et sa sauvegarde.

**Vérification :** les données restaurées correspondent au fichier enregistré et la copie n’avait aucune interface réseau au démarrage. Si le test échoue, conservez la sauvegarde, arrêtez la copie et analysez les journaux avant de réessayer.

## En cas de problème

| Symptôme | Vérification et action suivante |
| --- | --- |
| Le test NFS échoue | Vérifiez la connectivité depuis l’appliance, le chemin exporté, les droits et les options de montage. L’accès au NAS depuis le navigateur ne suffit pas. |
| La sauvegarde échoue ou n’a pas de point de restauration | Lisez les journaux de la VM et de l’export ; vérifiez l’accès et l’espace distant, l’espace du SR d’origine et la VM sélectionnée. Un snapshot conservé seul ne satisfait pas ce tutoriel. |
| Le point de restauration est absent | Vérifiez que la destination est activée sans erreur, actualisez la liste et contrôlez que la tâche a exporté cette VM. |
| La restauration échoue | Examinez les journaux, la lecture de la destination, l’espace du SR cible et son accessibilité par l’hôte. Vérifiez l’existence d’une VM partielle avant de réessayer ; ne supprimez jamais par nom seul. |
| La copie n’a pas de réseau | C’est normal ici : les interfaces ont été supprimées pour le test par console. Un réseau de production nécessite une revue distincte des IP et des identités de services. |
| Le fichier diffère ou le système ne démarre pas | Vérifiez le point choisi et l’écriture du fichier avant sauvegarde. Conservez les journaux et la sauvegarde ; le test n’a pas réussi. |

## Étape suivante et sources

Après un test réussi, définissez la fréquence, la rétention, la surveillance de capacité et la méthode de cohérence applicative réelles. N’activez une planification qu’après vérification du fuseau et des prochaines exécutions. Consultez le [guide de mise à jour](/docs/guides/updates/) et le [glossaire](/docs/xoa-hl/glossary/). La récupération de configuration, la réplication, les sauvegardes incrémentales et la restauration de fichiers sont des procédures distinctes.

Sources vérifiées à XO@e281c536 : [routes et accès administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [formulaire des destinations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [test de destination](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [modes et enregistrement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [planification et rétention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [exécution manuelle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [contrôles de restauration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [suppression des interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js). Application à XOA-HL : [version amont figée](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [sélection des correctifs et construction](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
