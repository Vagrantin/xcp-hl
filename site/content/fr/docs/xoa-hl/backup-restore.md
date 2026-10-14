---
title: Sauvegarder une VM — planification, rétention et restauration isolée
description: Tester une sauvegarde complète NFS, sa planification et sa rétention, puis une restauration isolée.
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: draft
sourceRevision: sha256:d47270a711f0c32fa1a709859c556afa66bbf887dba30e0332601a01b2c3aa95
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

1. Ouvrez **Paramètres → Emplacement** (`/#/settings/remotes`). Réutilisez une destination adaptée déjà vérifiée, ou créez-en une nommée `lab-backup-nfs`.
2. Choisissez **NFS**, renseignez le serveur et le chemin exporté fournis par son administrateur, puis les options de montage requises. Conservez les valeurs avancées par défaut sauf nécessité propre au stockage. N’utilisez pas un répertoire local de l’appliance pour ce test.
3. Enregistrez la destination, activez-la si nécessaire et utilisez l’action **Testez votre emplacement**. Lisez toute erreur de connexion ou de test avant de continuer.

**Vérification :** la destination est activée, son test réussit et aucune erreur de connexion n’apparaît. Cela vérifie l’accès, pas la capacité à restaurer une sauvegarde de VM.

Au commit de référence ce38, les titres français de réussite/échec du test distant sont inversés dans le catalogue hérité ([correction suivie](https://github.com/Vagrantin/xoa-hl/issues/38)). Vérifiez l’icône de réussite/erreur et les détails d’erreur/étape plutôt que le titre seul. Une sauvegarde réelle et une restauration isolée restent nécessaires ; aucune correction installée n’est affirmée ici.

## 2. Créer une tâche de sauvegarde complète

1. Ouvrez **Sauvegardes → Nouveau → VMs** (`/#/backup/new/vms`) et nommez la tâche `lab-first-vm-full`.
2. Sélectionnez explicitement votre seule VM de test. Désactivez la sélection intelligente pour éviter d’inclure d’autres VM.
3. Dans les modes, choisissez **Sauvegarder**. Laissez **Rolling snapshot**, **Delta backup**, **Disaster recovery** et **Continuous replication** désactivés. Ici, **Sauvegarder** correspond à l’export complet.
4. Sélectionnez `lab-backup-nfs` dans **Target remotes (for export)** (destinations d’export). Laissez **Supprimer les anciennes sauvegardes** désactivé : cette option peut supprimer des copies antérieures avant la réussite du nouvel export.
5. Ajoutez explicitement une planification. Pour cet exemple de laboratoire, réglez **Backup retention** (rétention des sauvegardes) sur `2`, choisissez un fuseau explicite comme `Asia/Tokyo` et vérifiez l’aperçu des prochaines exécutions. La rétention est un nombre de sauvegardes conservées pour cette planification, pas un nombre de jours.
6. Désactivez cette planification dans le tableau avant d’enregistrer la tâche. Le premier test de sauvegarde/restauration s’exécute manuellement ; gardez la planification désactivée jusqu’à l’exercice supervisé de la section 6.
7. Enregistrez et vérifiez la vue d’ensemble : une seule VM attendue, la bonne destination et une planification désactivée. Conservez les paramètres avancés pour ce premier test.

{{< callout type="warning" >}}
La rétention peut supprimer des sauvegardes anciennes lors des exécutions suivantes. Utilisez une destination de laboratoire dédiée et ne réduisez jamais la rétention d’une tâche de production pour suivre cet exemple. Un snapshot sur le SR d’origine n’est pas une sauvegarde indépendante.
{{< /callout >}}

## 3. Exécuter et contrôler la sauvegarde

1. Dans **Sauvegardes → Vue d’ensemble** (`/#/backup/overview`), utilisez l’action d’exécution de la planification désactivée. Vérifiez que la confirmation désigne votre tâche et une seule VM, puis confirmez.
2. Attendez la fin. Ouvrez les journaux et contrôlez le résultat de la VM et de l’export, pas seulement le démarrage de la tâche. Examinez les avertissements, échecs et données ignorées.
3. Ouvrez **Sauvegardes → Restaurer** (`/#/backup/restore`). Retrouvez la VM de test et vérifiez que la nouvelle sauvegarde complète apparaît avec l’horodatage et la destination attendus. Actualisez la liste si nécessaire.

**Vérification :** l’exécution a réussi et le nouveau point de restauration est visible. Notez la tâche, la planification, la destination, l’horodatage et les versions installées. Vous pouvez redémarrer normalement la VM d’origine ; gardez la planification désactivée pendant le test de restauration.

## 4. Restaurer une copie arrêtée

1. Dans **Sauvegardes → Restaurer**, choisissez l’action de restauration de la VM, puis exactement la sauvegarde complète que vous venez de créer.
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

## 6. Tester la planification et la rétention {#backup-schedules}

Terminez la sauvegarde manuelle et la restauration isolée ci-dessus avant d’activer l’automatisation. Utilisez uniquement cette tâche complète NFS de laboratoire, une VM jetable sélectionnée explicitement et son unique planification désactivée. Gardez l’invité source arrêté proprement pendant tous les passages ; la cohérence à chaud/applicative exige une validation séparée. Revérifiez l’espace et l’accès distant et conservez toute copie de récupération nécessaire **hors de la politique de rétention de cette tâche**.

1. Dans **Sauvegardes → Vue d’ensemble**, notez l’ID de la tâche et copiez l’ID exact de la planification avec son bouton presse-papiers. Ouvrez l’édition de la tâche. Dans **Planifier**, modifiez la ligne désactivée existante, sans la supprimer/recréer. Donnez-lui un nom de test clair, gardez **Backup retention** à `2` et laissez **Supprimer les anciennes sauvegardes**, la rétention longue durée et les contrôles automatiques de restauration désactivés. Vérifiez que seuls le mode complet **Sauvegarder**, la VM prévue et `lab-backup-nfs` restent sélectionnés.
2. Choisissez une règle de laboratoire avec le sélecteur visuel et un **Timezone** explicite, par exemple `Asia/Tokyo`. Espacez les occurrences au-delà de la durée de sauvegarde manuelle observée, avec une marge pour examiner les échecs. Vérifiez au moins trois occurrences dans la fenêtre supervisée et notez le **Cron pattern** généré. Aucun intervalle de production universel n’est prescrit ici. **Backup retention**, **Timezone** et **Cron pattern** dans le tableau restent en anglais dans cette version.
3. Notez aussi le fuseau du navigateur. La règle utilise le fuseau choisi, mais l’aperçu affiche les dates obtenues dans le fuseau d’affichage du navigateur. Une heure affichée différemment ne signifie pas forcément un instant de déclenchement différent. Comparez les instants prévus et l’horloge de l’appliance avant activation ; l’aperçu prédit des dates, sans prouver qu’une sauvegarde sera exécutée.
4. Gardez la ligne **Disabled** dans l’éditeur et choisissez **Enregistrer** pour la tâche. Rouvrez-la et relisez l’ID, la règle, le fuseau, la rétention, la VM et la destination. Les réglages sont enregistrés par des requêtes distinctes de planification/tâche ; une erreur peut laisser une modification partielle. N’activez pas avant concordance de ces éléments.
5. Revenez à la **Vue d’ensemble** et activez uniquement cette planification avec son bouton d’état. Ce bouton envoie immédiatement le changement ; aucun Enregistrer distinct n’est requis. Actualisez et vérifiez **Enabled** sur la ligne notée. Observez le prochain déclenchement sans utiliser l’exécution manuelle. Ouvrez les détails de cette planification et vérifiez les ID tâche/planification, début/fin réels, VM et résultat d’export ; contrôlez un nouveau point dans **Restaurer** sur la bonne destination.
6. Poursuivez jusqu’à au moins trois exécutions réussies de cette même planification. Comparez les horodatages des points après chaque passage. Avec rétention `2`, sans rétention longue durée et avec un nettoyage réussi, le résultat attendu est les deux sauvegardes complètes éligibles les plus récentes pour cette VM/planification sur cette destination. Vérifiez ce résultat au lieu de supposer un nombre de fichiers strict ou de compter les passages ignorés/échoués comme des points de reprise vérifiés. Avec **Supprimer les anciennes sauvegardes** désactivé, ces sources écrivent le nouvel export et ses métadonnées avant de supprimer les anciennes copies sélectionnées ; le nettoyage peut encore échouer et exige son contrôle de journaux/inventaire.
7. Désactivez la planification exacte dans la **Vue d’ensemble** et actualisez pour confirmer **Disabled** avant une autre occurrence attendue. La désactivation arrête les déclenchements futurs, sans annuler une tâche déjà active. Le contrôle d’annulation de cette vue est désactivé à ce commit. Laissez une exécution de laboratoire active se terminer, inspectez son résultat, puis vérifiez que l’occurrence suivante ne crée aucun passage. Terminez avec la règle désactivée.
8. Choisissez un point conservé issu d’un passage planifié et répétez les sections 4–5 : restauration arrêtée, suppression de toutes les NIC héritées avant démarrage, comparaison du fichier et arrêt de la copie. Utilisez la [procédure de suppression d’une VM jetable](/docs/xoa-hl/vm-operations/) pour son nettoyage identifié. Notez l’état final de la planification, les points conservés et le résultat de restauration.

Un nouvel export peut exister même si le nettoyage ultérieur fait échouer le passage. Inspectez les points/fichiers réels avant de réessayer et validez une restauration isolée avant de compter cette copie comme utilisable.

La rétention est définie par VM, mode complet et **ID de planification sur chaque destination**, pas par nom visible ou nombre global de jours/fichiers. Une autre planification peut conserver d’autres points. Supprimer puis recréer une règle au même nom change son identité ; n’en faites pas un raccourci de nettoyage et ne supposez pas que ses anciennes sauvegardes rejoignent la nouvelle politique. Ce pilote ne teste ni les périodes de rétention longue durée ni les chaînes delta.

Si un déclenchement manque, si l’enregistrement/le bouton d’état échoue ou si un passage est en échec, conservez les ID tâche/planification/destination, les heures prévues/réelles, l’erreur et l’inventaire. Considérez l’exécution automatique comme possible jusqu’à établissement de son état. Vérifiez disponibilité/horloge du serveur, activation, sélection de VM, accès et capacité avant de réessayer. Un passage pendant que la tâche fonctionne déjà peut être refusé ; ne supposez pas une file d’attente, une relance ou un rattrapage après indisponibilité de l’appliance. Désactiver, modifier la règle ou supprimer la tâche n’annule pas une exécution active. Après résolution, lancez manuellement une seule fois sans autre passage actif, vérifiez le point et refaites une restauration isolée avant de reprendre la planification convenue. Courriels/alertes, changements d’heure, reprise après panne et rétention de production exigent leurs propres validations.

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

Sources de planification XO `e281c536` : [éditeur, tableau et ordre d’enregistrement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [sélecteur de temps et affichage de l’aperçu](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [démarrage/arrêt des planifications](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [fonctionnement cron](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [refus des chevauchements et identités des journaux](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs) et [rétention complète et ordre de suppression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).

Après un test réussi, définissez la fréquence, la rétention, la surveillance de capacité et la méthode de cohérence applicative réelles. N’activez une planification qu’après vérification du fuseau et des prochaines exécutions. Consultez le [guide de mise à jour](/docs/guides/updates/) et le [glossaire](/docs/xoa-hl/glossary/). La récupération de configuration, la réplication, les sauvegardes incrémentales et la restauration de fichiers sont des procédures distinctes.

Sources vérifiées à XO@e281c536 : [routes et accès administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [formulaire des destinations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [test de destination](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [modes et enregistrement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [planification et rétention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [exécution manuelle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [contrôles de restauration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [suppression des interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js). Application à XOA-HL : [version amont figée](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [sélection des correctifs et construction](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
