---
title: "Sauvegarder et restaurer une VM"
linkTitle: "Sauvegarde et restauration"
description: "Sauvegardez une VM, restaurez une copie isolée, puis testez planification, sauvegardes incrémentales, récupération de fichier, réplique DR et SMB."
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: draft
sourceRevision: sha256:1dcbd01b48561fd25729aaad183c9a571e03b71d4ae45d588571c837b5967ba2
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protégez votre VM de test par une sauvegarde complète sur un stockage séparé. Restaurez ensuite une copie et vérifiez que ses données sont utilisables. Une tâche de sauvegarde réussie n’est que la moitié du test : la restauration le complète.

{{< callout type="info" >}}
**S’applique à** XOA-HL `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2), image `xoa-image-20261009-5f33c81`. Rédigé d’après le code publié ; pas encore testé en laboratoire. Les autres destinations et modes de sauvegarde demandent leurs propres tests.
{{< /callout >}}

Les sections 1 à 5 forment le tutoriel : une sauvegarde complète sur NFS et une restauration sans risque. Les sections suivantes sont des tests facultatifs qui s’appuient dessus : planification et rétention, sauvegardes incrémentales, récupération d’un fichier, réplique DR sur un autre pool et destination SMB.

## Avant de commencer

- [Créez et installez une VM de test](/docs/xoa-hl/create-vm/). Utilisez un compte administrateur XOA-HL : les pages de sauvegarde l’exigent dans cette version.
- Obtenez un export NFS sur un système de sauvegarde séparé, et non sur le stockage de la VM ou de l’appliance. L’appliance doit pouvoir le joindre et y créer, lire et supprimer des fichiers. Demandez à l’administrateur du stockage le serveur, le chemin exporté et les éventuelles options de montage.
- Vérifiez l’espace libre à trois endroits : la destination de sauvegarde, le SR de la VM (pour les snapshots temporaires) et le SR inscriptible qui recevra les disques restaurés. Prévoyez la rétention configurée plus une exécution. La taille compressée n’est pas garantie.
- Dans l’invité, créez un petit fichier sans importance et notez son contenu ou sa somme de contrôle. Arrêtez ensuite normalement l’invité et vérifiez que la VM est arrêtée. La sauvegarde d’une VM en marche n’est pas garantie cohérente pour ses applications.
- Réservez les ressources d’une deuxième VM. La copie restaurée reste arrêtée jusqu’à ce que **toutes ses interfaces réseau virtuelles (NIC) soient supprimées**. Ce test n’utilise que la console : la copie n’a besoin d’aucun réseau.

Vous gérez les sauvegardes dans votre **navigateur**. Vous créez et vérifiez le fichier témoin **dans l’invité**. Aucun shell n’est nécessaire sur l’hôte ou l’appliance.

## 1. Ajouter la destination de sauvegarde

1. Ouvrez **Paramètres → Emplacement** (`/#/settings/remotes`). Réutilisez une destination adaptée déjà vérifiée, ou créez-en une nommée `lab-backup-nfs`.
2. Choisissez **NFS** et saisissez le serveur et le chemin exporté fournis par l’administrateur du stockage, ainsi que les options de montage requises. Gardez les champs avancés par défaut, sauf besoin propre à votre stockage. N’utilisez pas un dossier local de l’appliance.
3. Enregistrez la destination, activez-la si nécessaire, puis lancez **Testez votre emplacement**. Lisez toute erreur de connexion ou de test avant de continuer.

**Vérification :** la destination est activée, son test réussit et aucune erreur de connexion n’apparaît. Cela prouve l’accès, pas la possibilité de restaurer une sauvegarde de VM.

Dans cette version, les titres de réussite et d’échec de ce test sont inversés ([correction suivie](https://github.com/Vagrantin/xoa-hl/issues/38)). Fiez-vous à l’icône de réussite ou d’erreur et au détail des étapes, pas au titre.

## 2. Créer une tâche de sauvegarde complète

1. Ouvrez **Sauvegardes → Nouveau → VMs** (`/#/backup/new/vms`) et nommez la tâche `lab-first-vm-full`.
2. Sélectionnez uniquement votre VM de test. Laissez la sélection intelligente désactivée, pour que la tâche ne prenne pas d’autres VM.
3. Dans les modes de sauvegarde, sélectionnez **Sauvegarder**. C’est le mode d’export complet. Laissez **Rolling snapshot**, **Delta backup**, **Reprise après panne** et **Réplication continue** désactivés.
4. Dans **Target remotes (for export)**, sélectionnez `lab-backup-nfs`. Laissez **Supprimer les anciennes sauvegardes** désactivé : cette option peut supprimer des copies anciennes avant la réussite du nouvel export.
5. Ajoutez une planification. Réglez **Backup retention** sur `2`, choisissez un fuseau horaire explicite comme `Asia/Tokyo` et vérifiez l’aperçu des prochaines exécutions. La rétention est le nombre de sauvegardes conservées pour cette planification, pas un nombre de jours.
6. Désactivez cette planification dans le tableau avant d’enregistrer la tâche. Vous lancerez cette première sauvegarde à la main. La planification reste désactivée jusqu’à [Tester la planification et la rétention](#backup-schedules).
7. Enregistrez, puis vérifiez la vue d’ensemble : une seule VM, la bonne destination et une planification désactivée. Gardez les paramètres avancés inchangés pour ce premier test.

{{< callout type="warning" >}}
La rétention peut supprimer d’anciennes sauvegardes lors des exécutions suivantes. Utilisez une destination de laboratoire dédiée, et ne réduisez jamais la rétention d’une tâche de production pour suivre cet exemple. Un snapshot conservé sur le SR de la VM n’est pas une sauvegarde indépendante.
{{< /callout >}}

## 3. Lancer et contrôler la sauvegarde

1. Dans **Sauvegardes → Vue d’ensemble** (`/#/backup/overview`), utilisez l’action d’exécution de la planification désactivée. Vérifiez que la confirmation désigne votre tâche et une seule VM, puis confirmez.
2. Attendez la fin de l’exécution. Ouvrez son journal et contrôlez le résultat de l’export de la VM, pas seulement le démarrage de la tâche. Examinez tout avertissement, échec ou donnée ignorée.
3. Ouvrez **Sauvegardes → Restaurer** (`/#/backup/restore`). Retrouvez la VM de test et vérifiez que la nouvelle sauvegarde complète apparaît avec l’heure et la destination attendues. Actualisez la liste si besoin.

**Vérification :** l’exécution a réussi et son point de restauration est listé. Notez la tâche, la planification, la destination, l’heure de sauvegarde et les versions installées. Vous pouvez redémarrer l’invité d’origine. Gardez sa planification désactivée pendant le test de restauration.

## 4. Restaurer une copie arrêtée

1. Dans **Sauvegardes → Restaurer**, choisissez l’action de restauration de votre VM de test, puis la sauvegarde complète que vous venez de créer.
2. Choisissez un SR inscriptible avec assez d’espace libre. C’est un stockage de disques de VM, ni la destination NFS ni un SR ISO.
3. Laissez **Start VM after restore** **désactivé**. Activez **Generate new MAC addresses** pour que la copie ait ses propres adresses de cartes réseau. De nouvelles adresses MAC ne changent ni l’adresse IP statique, ni le nom d’hôte, ni l’identité applicative de l’invité.
4. Confirmez la restauration et attendez la fin. Vérifiez l’absence d’erreur dans le journal de restauration. Identifiez la nouvelle VM par son UUID et ses disques restaurés, pas par son nom.
5. Vérifiez que la VM restaurée est arrêtée. Renommez-la `lab-first-vm-restore-test` et notez son UUID à côté de celui de la VM d’origine.

**Vérification :** une VM distincte et arrêtée existe, avec les disques attendus. Ne la démarrez pas encore. Si elle est en marche, arrêtez-la et vérifiez à quel réseau elle a pu accéder avant de continuer.

## 5. Isoler, démarrer et vérifier la copie

1. Ouvrez l’onglet **Réseau de la copie restaurée** (`/#/vms/<restored-uuid>/network`). Pendant qu’elle est arrêtée, supprimez **toutes** ses NIC et vérifiez que la liste est vide. Un état « déconnecté » ne suffit pas : la NIC pourrait se reconnecter au prochain démarrage.
2. Vérifiez de nouveau l’UUID et la liste vide. Démarrez ensuite la copie et ouvrez **Console**. Ne touchez pas au réseau de la VM d’origine.
3. Vérifiez que l’invité démarre, que la connexion par la console fonctionne et que le fichier témoin a le contenu ou la somme de contrôle attendus. Vérifiez les autres données nécessaires à votre reprise. Un invité qui démarre n’est pas encore une reprise applicative complète.
4. Arrêtez normalement l’invité restauré. Notez le résultat, l’heure de la sauvegarde, la durée de restauration et les versions. Une fois terminé, vérifiez l’UUID et supprimez uniquement la copie de test et ses disques restaurés. Conservez la VM d’origine et la sauvegarde.

**Vérification :** les données restaurées correspondent au témoin, et la copie n’avait aucune NIC à son démarrage. Si le test échoue, conservez la sauvegarde, arrêtez la copie et lisez les journaux avant de réessayer.

## Tester la planification et la rétention {#backup-schedules}

Ce test active la planification de la tâche de laboratoire, observe trois exécutions automatiques, puis la désactive. Faites-le seulement après la réussite de la sauvegarde manuelle et de la restauration ci-dessus.

**Avant de commencer**

- Utilisez uniquement la tâche `lab-first-vm-full`, son unique planification désactivée et la VM de test.
- Gardez la VM de test arrêtée pendant toutes les exécutions. Un invité en marche demande son propre test de cohérence.
- Revérifiez l’espace libre et l’accès à la destination.
- Conservez toute copie de récupération nécessaire **hors de cette tâche** : la rétention peut supprimer ses anciennes sauvegardes.

1. Dans **Sauvegardes → Vue d’ensemble**, notez l’ID de la tâche et copiez l’ID exact de la planification avec son bouton presse-papiers.
2. Modifiez la tâche. Dans **Planifier**, modifiez la ligne désactivée existante ; ne la supprimez pas pour la recréer. Donnez-lui un nom de test clair et gardez **Backup retention** à `2`. Laissez **Supprimer les anciennes sauvegardes**, la rétention longue durée et les contrôles automatiques de restauration désactivés. Vérifiez que seuls le mode **Sauvegarder**, la VM de test et `lab-backup-nfs` sont sélectionnés.
3. Définissez une règle de test avec le sélecteur visuel et un **Timezone** explicite, par exemple `Asia/Tokyo`. Espacez les exécutions de plus que la durée d’une sauvegarde manuelle, avec une marge pour examiner les échecs. Vérifiez au moins trois exécutions à venir et notez le **Cron pattern**.
4. Notez aussi le fuseau horaire de votre navigateur. La règle s’exécute dans le fuseau choisi, mais l’aperçu affiche les heures dans celui du navigateur : un même instant peut donc s’afficher à une autre heure. L’aperçu prévoit des dates ; il ne prouve pas qu’une sauvegarde aura lieu.
5. Gardez la ligne **Disabled** et sélectionnez **Enregistrer**. Rouvrez la tâche et vérifiez l’ID de la planification, la règle, le fuseau, la rétention, la VM et la destination. La tâche et sa planification sont enregistrées séparément : une erreur peut laisser une modification partielle. Ne continuez pas tant que tout ne concorde pas.
6. De retour dans la **Vue d’ensemble**, activez uniquement cette planification avec son bouton d’état. Le bouton s’applique immédiatement ; il n’y a pas d’enregistrement séparé. Actualisez et vérifiez que la ligne affiche **Enabled**.
7. Attendez l’exécution suivante sans utiliser le bouton d’exécution manuelle. Ouvrez ses détails et vérifiez les ID de tâche et de planification, les heures de début et de fin, la VM et le résultat de l’export. Dans **Restaurer**, vérifiez qu’un nouveau point apparaît sur la bonne destination.
8. Attendez au moins trois exécutions réussies de cette planification, et comparez l’heure des points après chacune. Avec une rétention de `2`, il doit rester les deux sauvegardes complètes les plus récentes de cette VM pour cette planification. Vérifiez la liste réelle : ne supposez pas un nombre de fichiers, et ne comptez pas les exécutions ignorées ou en échec.
9. Avant l’exécution prévue suivante, désactivez la planification dans la **Vue d’ensemble** et actualisez pour vérifier **Disabled**. Cela arrête les exécutions futures, sans annuler une sauvegarde en cours (le bouton d’annulation est désactivé dans cette version). Laissez une sauvegarde en cours se terminer, puis vérifiez que l’heure prévue suivante ne lance rien.
10. Restaurez un point issu d’une exécution planifiée avec les sections 4 et 5 : copie arrêtée, toutes les NIC supprimées avant le premier démarrage, somme de contrôle comparée, copie arrêtée. Supprimez la copie avec la [procédure de suppression d’une VM](/docs/xoa-hl/vm-operations/). Notez l’état final de la planification, les points restants et le résultat de la restauration.

**Bon à savoir**

- Avec **Supprimer les anciennes sauvegardes** désactivé, une exécution écrit la nouvelle sauvegarde avant de supprimer les anciennes. Si la suppression échoue, l’exécution peut apparaître en échec alors que la nouvelle sauvegarde existe. Vérifiez les points réels avant de réessayer, et testez une restauration avant de compter sur un point.
- La rétention compte les sauvegardes par VM, par mode et par **ID de planification sur chaque destination**. Elle ne compte ni des jours, ni des noms, ni des fichiers. Une autre planification garde ses propres points. Une planification supprimée puis recréée reçoit un nouvel ID : ses anciennes sauvegardes ne rejoignent pas la nouvelle politique.
- Une exécution lancée pendant que la même tâche tourne encore peut être refusée. Les exécutions manquées pendant que l’appliance était éteinte ne sont pas rattrapées.
- Désactiver, modifier ou supprimer une tâche n’annule pas une sauvegarde en cours.

**Si une exécution manque ou échoue**, conservez les ID de la tâche, de la planification et de la destination, les heures prévues et réelles, l’erreur et la liste des points de restauration. Tant que l’état n’est pas connu, considérez qu’une exécution automatique peut encore démarrer. Vérifiez que le serveur fonctionne et que son horloge est juste, puis l’activation, la sélection de la VM, l’accès à la destination et l’espace libre. Une fois le problème corrigé, lancez la tâche une fois à la main sans autre exécution en cours, vérifiez le nouveau point et testez une restauration avant de réactiver la planification.

Non couvert ici : alertes par courriel, changements d’heure, reprise après une panne, rétention longue durée et politiques de rétention de production.

## Utiliser les sauvegardes incrémentales {#delta-backups}

Une sauvegarde incrémentale (delta) ne copie que ce qui a changé depuis la sauvegarde précédente. Ce test crée une tâche delta séparée, produit trois points de restauration et vérifie qu’un point plus ancien se restaure toujours après le nettoyage de la rétention. Faites-le après la réussite de la sauvegarde complète et de la restauration ci-dessus, et conservez cette sauvegarde complète.

**Avant de commencer**

- Utilisez une VM de test avec des disques virtuels ordinaires : pas de disque partagé ou passthrough, pas de sauvegarde de la mémoire. Notez les UUID de la VM et des disques (VDI), leur taille, ainsi que le chemin et la somme de contrôle du fichier témoin. Ne modifiez pas les disques pendant le test.
- Demandez au responsable du stockage un nouvel export NFS vide et ajoutez-le comme destination séparée, par exemple `lab-delta-nfs`.
- Réservez de l’espace pour les snapshots sur le SR source, pour une sauvegarde complète et les changements suivants sur la destination, et pour les copies restaurées sur un SR inscriptible.
- Utilisez un compte administrateur. Si **Delta Backup** ou ses réglages manquent dans votre installation, arrêtez-vous et signalez la version observée. Ne modifiez pas la licence et ne suivez pas des instructions écrites pour XO 6, qui est une autre interface.

Un point de restauration delta a besoin de ses métadonnées et de sa chaîne de fichiers de disque parents (VHD). Un fichier VHD seul n’est pas une sauvegarde de VM. La sauvegarde complète du tutoriel ne peut pas servir de parent à cette nouvelle chaîne.

### Créer la tâche delta

1. Ajoutez et testez la destination comme en section 1. Ouvrez **Sauvegardes → Nouveau → VMs** (`/#/backup/new/vms`), nommez la tâche `lab-delta-chain`, sélectionnez uniquement la VM de test et laissez la sélection intelligente désactivée.
2. Sélectionnez uniquement **Delta Backup**. Laissez **Sauvegarder**, **Rolling Snapshot**, **Reprise après panne** et **Réplication continue** désactivés. Sélectionnez uniquement `lab-delta-nfs` et laissez **Supprimer les anciennes sauvegardes** désactivé. Ne modifiez pas la tâche complète précédente.
3. Dans **Paramètres avancés**, réglez **Full backup interval** sur `2`. Laissez **Use NBD to transfer disk if available** et **Purge snapshot data when using CBT.** désactivés. Activez **Merge backups synchronously**. N’utilisez pas les autres options avancées, et ne supprimez jamais les snapshots conservés par cette tâche.
4. Ajoutez une planification avec **Backup retention** à `2`, un fuseau horaire explicite et un aperçu vérifié. Laissez **Force full backup** désactivé : il rend chaque exécution complète. Laissez la rétention longue durée désactivée. Désactivez la planification, puis enregistrez. Rouvrez la tâche, vérifiez chaque réglage et notez les ID de la tâche, de la planification et de la destination. Gardez la planification désactivée pendant tout le test.

**Full backup interval** fixe la longueur de la chaîne. Avec `2`, une nouvelle tâche fait une sauvegarde complète, puis une incrémentale, puis de nouveau une complète. Ce n’est ni un nombre de jours, ni le nombre de points conservés. Des parents manquants, des disques modifiés ou des erreurs peuvent changer cet ordre : vérifiez les journaux.

### Créer trois points de restauration

Avant chaque exécution, écrivez le témoin dans l’invité et arrêtez normalement l’invité. Lancez chaque exécution à la main, et seulement si aucune sauvegarde ou fusion n’est en cours. Pour chaque exécution, notez son ID, l’heure, le **Type** d’export, les avertissements et le nouveau point. Examinez chaque état et chaque page de tâches, et conservez le JSON brut si nécessaire.

| Exécution | Dans l’invité avant l’arrêt | Résultat attendu |
| --- | --- | --- |
| 1 | Écrire la version A et noter la somme A | Export complet ; le point A apparaît |
| 2 | Démarrer la VM, écrire la version B, noter la somme B, arrêter | Export incrémental ; le point B apparaît. Restaurer B (ci-dessous) avant l’exécution 3 |
| 3 | Démarrer la VM, écrire la version C, noter la somme C, arrêter | Export complet (intervalle `2`) ; vérifier le nettoyage et la présence des points B et C |

La liste de restauration peut afficher **incremental** pour un point d’une tâche delta, même quand l’export était complet. Vérifiez le **Type** d’export dans le journal, pas ce libellé ni la taille du fichier. Si l’exécution 2 a fait un export complet, conservez les preuves, vérifiez les snapshots parents, les disques et les réglages d’intervalle et **Force**, et ne la comptez pas comme un transfert incrémental. Ne supprimez jamais un parent pour forcer le test.

### Restaurer un point incrémental avant et après le nettoyage

1. Dans **Sauvegardes → Restaurer** (`/#/backup/restore`), sélectionnez le point B sur `lab-delta-nfs` et un SR inscriptible avec assez d’espace. Incluez **chaque disque** : cette fenêtre permet d’en ignorer, vérifiez donc chacun.
2. Laissez **Start VM after restore** et **Use differential restore** désactivés. Activez **Generate new MAC addresses**. La restauration différentielle réutilise des snapshots source et constitue un autre test.
3. Isolez et vérifiez la copie comme aux sections 4 et 5 : notez les nouveaux UUID, gardez-la arrêtée, supprimez **toutes** les NIC, démarrez-la et comparez le fichier à la somme B dans la console. Arrêtez-la normalement. Supprimez la copie avec la [procédure de suppression d’une VM](/docs/xoa-hl/vm-operations/).
4. Après l’exécution 3 et son nettoyage, restaurez de nouveau le point B dans une nouvelle copie isolée et vérifiez la somme B. Restaurez séparément le point C et vérifiez la somme C. Cela prouve que l’ancien point incrémental fonctionne encore après la rétention. Notez les points restants et gardez la planification désactivée.

**Bon à savoir**

- La rétention choisit les points de cette VM et de cette planification sur cette destination. Les limites de fusion ou un nettoyage en échec peuvent laisser des points en trop.
- Avec **Supprimer les anciennes sauvegardes** désactivé, les anciens points sont supprimés après le transfert. Le nettoyage avant une exécution peut quand même fusionner ou supprimer des données.
- La fusion synchrone ne rend pas une exécution « tout ou rien » et ne prouve pas que la récupération fonctionne.
- Ne supprimez, ne renommez, ne déplacez et ne modifiez jamais à la main les fichiers JSON ou VHD de sauvegarde, et ne supprimez jamais de snapshot pour « ranger » une chaîne.

**En cas d’échec** (parent manquant, erreur de transfert ou de fusion, restauration échouée), conservez le JSON de l’exécution, les ID des points et la liste des VM et disques partiels. Arrêtez de lancer la tâche, car chaque exécution peut modifier la chaîne. Réglez l’accès, l’espace ou la propriété avec le responsable des sauvegardes, puis refaites le test. Ne redémarrez pas de service et n’utilisez pas les actions de forçage ou de réparation comme solution générique. Si la récupération échoue, conservez la sauvegarde complète indépendante et laissez l’incident ouvert.

Non couvert ici : invités en marche, NBD et CBT, destinations chiffrées ou autres, restauration différentielle et récupération après une vraie panne.

## Récupération d’un fichier depuis une sauvegarde delta {#file-restore}

Téléchargez un fichier depuis un point de restauration delta vers votre ordinateur. Ce test utilise le point B du test incrémental ci-dessus, après la réussite de la restauration de sa VM. Il ne replace pas le fichier dans la VM. Les sauvegardes complètes du tutoriel n’apparaissent pas sur cette page.

**Avant de commencer**

- Utilisez une VM Linux de test avec un seul disque et une partition ordinaire lisible.
- Avant la sauvegarde B, notez le chemin, le contenu et le SHA-256 d’un petit fichier témoin, par exemple `/home/lab/recovery-b.txt`.
- Conservez le point B et sa chaîne sur la destination. Vérifiez que votre ordinateur a de la place pour l’archive.
- Utilisez un compte administrateur et vérifiez que **Restauration de fichiers** existe dans votre installation.
- Pour ce premier test, évitez les VM de production, les données privées, les volumes chiffrés ou RAID, les liens symboliques et les dossiers. Ce test ne prouve pas la prise en charge de tous les systèmes de fichiers, agencements LVM ou destinations.

1. Ouvrez **Sauvegardes → Restauration de fichiers** (`/#/backup/file-restore`). Repérez la VM de test et ouvrez son action de restauration de fichiers. Ne cliquez pas sur les boutons de suppression voisins. Si la VM ou le point manque, actualisez et vérifiez que `lab-delta-nfs` est activée. Ne passez pas à la sauvegarde complète précédente.
2. Choisissez le **point B** d’après son heure et sa tâche, puis le disque. Attendez l’analyse des partitions, puis choisissez celle qui contient le témoin. Un disque sans table de partitions peut afficher directement son système de fichiers. Si l’analyse échoue, arrêtez-vous : ne montez pas et ne modifiez pas à la main les fichiers de sauvegarde.
3. Parcourez depuis `/` jusqu’au fichier témoin et sélectionnez **ce seul fichier**. N’utilisez pas les commandes de sélection de dossier ou de tout sélectionner. Vérifiez le chemin et gardez le format **tgz** (par défaut ; **zip** fonctionne aussi, mais peut être plus lent). Lancez le téléchargement et attendez que le navigateur le termine. Une fenêtre bloquée ou un téléchargement incomplet n’est pas une réussite.
4. Sur votre ordinateur, notez le nom, la taille et le SHA-256 de l’archive. Listez son contenu, extrayez uniquement le témoin dans un nouveau dossier vide et comparez son contenu et son SHA-256 avec la version B. Considérez les chemins de l’archive comme non fiables, et n’extrayez jamais par-dessus des données en service. Ne modifiez ni la VM d’origine, ni le point B, ni la planification.

**Vérification :** l’archive s’ouvre, elle ne contient que le fichier témoin, et ce fichier correspond à la somme B. Un nom de fichier identique, ou le contenu de la version C, ne compte pas comme une correspondance.

Si une étape échoue, conservez les preuves et suspendez les sauvegardes jusqu’à l’examen par le responsable des sauvegardes. Ne supprimez pas de fichiers de chaîne, de snapshots source ou de fichiers partiels pour faire apparaître un point. Recopier le fichier récupéré dans un invité est une autre opération, à faire approuver par son responsable.

## Copier une VM vers un autre pool (réplique DR) {#dr-replica}

**Reprise après panne** (DR) copie une VM entière vers un SR d’un autre pool. C’est différent de la sauvegarde NFS et de **Réplication continue** (CR), qui n’envoie que les changements. La copie, appelée réplique, reste arrêtée et son démarrage est bloqué. **Ne débloquez pas et ne démarrez pas la réplique.** Pour l’utiliser, on la clone. Ce test vérifie un tel clone dans un environnement isolé. Il ne teste ni la bascule automatique, ni la perte du pool source, ni le retour arrière.

**Avant de commencer**

- Utilisez une VM de test sur le pool A, et un deuxième pool de test B géré par la même appliance XOA-HL.
- Demandez au responsable du pool B un SR inscriptible dédié, `lab-dr-sr`, avec de la place pour deux copies complètes et un clone. Il doit être sur un stockage différent de celui du pool A, et ne pas être une bibliothèque ISO. Notez les UUID des deux pools et SR, l’espace libre et les hôtes qui peuvent joindre le SR.
- Conservez la sauvegarde NFS indépendante du tutoriel.
- Utilisez une VM à un seul disque, sans disque partagé ou passthrough. Avant chaque exécution, écrivez un témoin (A, puis B, puis C), notez son SHA-256 et arrêtez normalement l’invité.
- Prévoyez un accès console et un emplacement sur le pool B **sans réseau de production**. Vous supprimerez toutes les NIC du clone avant son démarrage.
- Si DR ou le SR cible n’est pas disponible dans votre installation, arrêtez-vous.

1. Ouvrez **Sauvegardes → Nouveau → VMs** (`/#/backup/new/vms`) et créez la tâche `lab-dr-full`. Sélectionnez uniquement la VM de test et laissez la sélection intelligente désactivée. Sélectionnez uniquement **Reprise après panne** ; laissez **Sauvegarder**, **Delta Backup**, **Réplication continue** et **Rolling Snapshot** désactivés. Sous **Target SRs (for replication)**, sélectionnez uniquement `lab-dr-sr`. Laissez **Supprimer les anciennes sauvegardes** désactivé, pour que les anciennes répliques ne soient pas supprimées avant le transfert. Ne modifiez pas les autres tâches.
2. Ajoutez une planification avec **Replication retention** à `2`, un fuseau horaire explicite et un aperçu vérifié. N’utilisez ni la rétention des snapshots ni les contrôles de santé. Désactivez la planification et enregistrez. Rouvrez la tâche et vérifiez la VM, le SR cible, le mode, la rétention, l’état désactivé et les ID.
3. Témoin A écrit et invité arrêté, lancez la tâche une fois depuis **Sauvegardes → Vue d’ensemble**. Vérifiez chaque tâche et chaque avertissement. Sur le pool B, retrouvez la nouvelle réplique **arrêtée** par son UUID, la tâche et l’heure dans son nom, son étiquette **Disaster Recovery** et son disque. Ne la démarrez pas.
4. Recommencez avec le témoin B, puis C, une exécution terminée à la fois. Notez les ID d’exécution et de réplique, les heures, les disques et les erreurs. Après la troisième exécution, vérifiez quelles répliques restent : normalement B et C. Une tâche verte ne prouve pas que les données sont justes, et une suppression en échec n’est pas annulée.
5. Sélectionnez la **réplique B**, et non la VM source, la réplique C ou un point NFS. Faites un **Clonage rapide** avec un nom unique sur le pool B, en laissant la réplique arrêtée. Notez les nouveaux ID de VM et de disque du clone, et vérifiez qu’il est arrêté et que son démarrage n’est pas bloqué. Si le clonage échoue ou si le clone est bloqué, arrêtez-vous ; ne contournez pas le blocage.
6. Supprimez **toutes** les NIC du clone arrêté et vérifiez que sa liste réseau est vide. Démarrez uniquement le clone, ouvrez sa console et comparez le témoin à la somme B. Arrêtez-le normalement. Vous pouvez tester un clone de C de la même façon.
7. Conservez les répliques B et C et la sauvegarde NFS. Supprimez uniquement les clones de test, avec la [procédure de suppression d’une VM](/docs/xoa-hl/vm-operations/).

**Vérification :** trois exécutions complètes ont atteint le bon pool et le bon SR ; B et C restent, ou vous pouvez expliquer pourquoi ; le clone isolé de B a ses propres ID, n’avait aucune NIC à son démarrage et contient exactement le témoin B.

Si un transfert, un contrôle d’espace, une suppression, un clonage ou une vérification de données échoue, suspendez les exécutions et transmettez l’inventaire aux responsables des sauvegardes et du stockage. Ne retirez jamais le blocage de démarrage d’une réplique, ne supprimez pas un point sur son seul nom et ne supprimez pas un snapshot géré par la tâche de sauvegarde.

Non couvert ici : chaînes CR, exécutions planifiées, bascule réseau, prévention du double démarrage d’une même VM, retour arrière et vraies pannes.

## Tester une sauvegarde SMB sur Windows Server {#smb-remote}

Testez une destination SMB avec une sauvegarde complète et une restauration isolée. L’interface XO indique que les destinations SMB sont prévues pour **Windows Server**, et recommande NFS pour Samba sous Linux et la plupart des NAS. Ce test ne couvre ni les autres serveurs SMB, ni un stockage SMB pour ISO ou disques de VM, ni les destinations cloud, ni un usage en production. XO monte le partage en CIFS, et le paquet XOA-HL inclut `cifs-utils`, mais le montage n’a pas encore été vérifié sur une vraie appliance.

**Avant de commencer**

- Demandez à l’administrateur Windows Server un **partage de test dédié**, sur un stockage différent de celui de la VM source et de l’appliance, avec assez d’espace pour la sauvegarde et le test de restauration.
- Demandez un compte dédié qui peut créer, lire et supprimer des fichiers dans ce partage, avec un accès réseau limité à l’appliance. Obtenez le nom du serveur, le nom du partage, l’éventuel sous-dossier, le domaine et les identifiants par un canal sûr.
- Saisissez le mot de passe uniquement dans son propre champ. XO construit une URL de destination interne qui contient les identifiants : traitez donc les exports de configuration XO comme des secrets. Ne partagez jamais cette URL, et ne mettez jamais d’identifiants dans une capture, un ticket, un extrait de journal ou une option de montage personnalisée.
- Conservez la sauvegarde NFS indépendante du tutoriel. Utilisez la même petite VM de test arrêtée, à un seul disque, avec un nouveau fichier témoin et sa somme de contrôle. Réservez un SR inscriptible et un environnement accessible uniquement par console pour la copie restaurée.

1. Dans **Paramètres → Emplacement** (`/#/settings/remotes`), créez `lab-backup-smb` de type **SMB**. Dans **Address\\Share**, saisissez le serveur et le partage séparés par une barre oblique inversée. **Subfolder** est un chemin facultatif dans ce partage, pas un second chemin de partage. Saisissez l’utilisateur, le mot de passe et le domaine dédiés (le formulaire propose `WORKGROUP` ; utilisez la valeur de l’administrateur). Laissez **Custom mount options**, le proxy et le chiffrement par défaut. Enregistrez, puis vérifiez l’ID, l’état activé, le type, le serveur, le partage, le sous-dossier et l’indicateur d’erreur. Le mot de passe reste masqué : n’essayez pas de le lire dans l’URL affichée.
2. Lancez **Testez votre emplacement** sur cette destination. Le test écrit un fichier aléatoire de 10 Mio, le relit, le compare et tente de le supprimer. Vérifiez l’icône de réussite, le résultat et toute étape en échec ; dans cette version, les titres de réussite et d’échec sont inversés. Si une étape a échoué, demandez à l’administrateur de rechercher un fichier `.test` restant par son nom exact. Un test réussi prouve seulement cet aller-retour, ni une restauration de VM ni un débit soutenu.
3. Dans **Sauvegardes → Nouveau → VMs** (`/#/backup/new/vms`), créez une tâche séparée nommée `lab-smb-full` : uniquement la VM de test arrêtée, uniquement le mode **Sauvegarder** (complet), `lab-backup-smb` comme seule destination, et **Supprimer les anciennes sauvegardes** désactivé. Ajoutez une planification avec un fuseau horaire explicite et **Backup retention** à `2`, gardez-la désactivée, enregistrez et vérifiez les ID. Ne modifiez pas la tâche NFS.
4. Lancez une fois à la main la planification désactivée depuis **Sauvegardes → Vue d’ensemble**. Vérifiez l’export de la VM et le résultat de la destination dans le journal, puis retrouvez le point complet sur `lab-backup-smb` dans **Sauvegardes → Restaurer**. Notez les heures, les ID, la taille et toute erreur de montage SMB, de connexion ou d’espace. Un snapshot resté sur le SR source, ou un test de destination réussi, n’est pas une sauvegarde de VM.
5. Restaurez ce point sur le SR réservé avec **Start VM after restore** désactivé. Notez les nouveaux UUID de VM et de disque. Copie arrêtée, supprimez **toutes les NIC** et vérifiez que la liste réseau est vide. Démarrez uniquement cette copie depuis **Console**, comparez la somme du témoin et arrêtez-la. Conservez la VM d’origine, la sauvegarde NFS et le point SMB jusqu’à ce que le résultat soit noté. Supprimez ensuite uniquement la copie de test avec la [procédure de suppression d’une VM](/docs/xoa-hl/vm-operations/).

**Vérification :** le test de destination réussit, la sauvegarde complète arrive sur le partage, et la copie isolée démarre sans NIC et avec les bonnes données.

Si l’accès, l’écriture, la lecture, la suppression, l’export ou la restauration échoue, arrêtez-vous. Transmettez aux responsables des sauvegardes et du serveur les erreurs (sans identifiants), les ID exacts, le contenu du partage et les éventuelles VM partielles. Ne réessayez jamais sur un partage de production et ne supprimez jamais des chemins de sauvegarde sur leur seul nom.

Non couvert ici : renouvellement du mot de passe, pannes du partage, rétention sur plusieurs exécutions, approbation de domaine, versions et réglages de sécurité SMB, débit et autres serveurs SMB.

## En cas de problème

| Problème | À vérifier |
| --- | --- |
| Le test NFS échoue | Vérifiez que l’appliance peut joindre le serveur, puis le chemin exporté, ses droits et les options de montage. L’accès au NAS depuis votre navigateur ne suffit pas. |
| La sauvegarde échoue ou aucun point n’apparaît | Lisez les journaux de la VM et de l’export. Vérifiez l’accès et l’espace de la destination, l’espace libre sur le SR de la VM et la VM sélectionnée. Un snapshot resté en place n’est pas une sauvegarde. |
| Le point de restauration manque | Vérifiez que la destination est activée et sans erreur, actualisez la liste, et vérifiez que la tâche a bien exporté cette VM. |
| La restauration échoue | Lisez son journal, et vérifiez que la destination est lisible et que le SR cible a de l’espace et est joignable par l’hôte. Cherchez une VM partielle avant de réessayer. Ne supprimez jamais sur le seul nom. |
| La réplique DR ou son clone échoue | Notez l’exécution, les ID de VM et de disque, l’espace et l’accès du SR cible, et l’état de blocage. Gardez les répliques arrêtées. Ne contournez pas leur blocage de démarrage et ne relancez pas la rétention à l’aveugle. |
| La destination SMB ou sa restauration échoue | Avec le responsable Windows Server, vérifiez l’étape de test en échec, les journaux de tâche et de restauration, le serveur et le partage, l’accès du compte, l’espace libre et les objets partiels. Conservez la sauvegarde NFS indépendante. Ne collez jamais d’identifiants dans un rapport. |
| La VM restaurée n’a pas de réseau | C’est normal : vous avez supprimé toutes les NIC pour ce test par console. La connecter à un réseau de production demande d’abord de revoir l’adresse IP de l’invité et les identités de ses services. |
| Le fichier diffère, ou l’invité ne démarre pas | Vérifiez que vous avez choisi le bon point et que le fichier était écrit avant la sauvegarde. Conservez les journaux et la sauvegarde. Le test n’a pas réussi. |

Pour les états d’exécution, les exports partiels et une nouvelle tentative maîtrisée, consultez [Diagnostiquer une sauvegarde en échec](/docs/xoa-hl/troubleshooting/#backup-failures).

## Étapes suivantes

Après un test de restauration réussi, définissez votre fréquence de sauvegarde, votre rétention, la surveillance de la capacité et la façon de rendre les sauvegardes cohérentes pour vos applications. N’activez une planification qu’après avoir vérifié son fuseau horaire et ses prochaines exécutions. Consultez aussi le [guide de mise à jour](/docs/guides/updates/) et le [glossaire](/docs/xoa-hl/glossary/). La récupération de la configuration et la réplication continue demandent leurs propres procédures.

{{< details title="Sources" closed="true" >}}
- **Planification** : [éditeur, tableau et ordre d’enregistrement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [sélecteur de temps et affichage de l’aperçu](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [démarrage/arrêt des planifications](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [fonctionnement cron](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [refus des chevauchements et identités des journaux](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs), [rétention complète et ordre de suppression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).
- **Sauvegarde et restauration** : [routes et accès administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [formulaire des destinations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [test de destination](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [modes et enregistrement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [planification et rétention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [exécution manuelle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [contrôles de restauration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [suppression des interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [version amont figée](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [sélection des correctifs et construction](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
- **Sauvegardes incrémentales** : [Incremental export/base selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs), [Remote transfer/retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs), [Snapshot retention](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs), [Cleanup/merge execution](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs), [Restore chain reader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [Restore implementation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/ImportVmBackup.mjs), [Export type in logs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js).
- **Récupération d’un fichier** : [file-restore UI and delta filter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/index.js), [backup/disk/partition/file selector](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/restore-file-modal.js), [admin file APIs and archive response](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/backup-ng.mjs), [read-only partition and tgz/zip adapter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [browser download](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **Réplique DR** : [job mode/target SR and schedule](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [replication retention control](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [full export and SR writer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/FullXapi.mjs), [replica import, blocked start and pruning](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullXapiWriter.mjs), [replica identity filter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_listReplicatedVms.mjs), [clone API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Destination SMB** : [formulaire et avertissement Windows Server](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [analyseur SMB](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-remote-parser/src/index.js), [gestionnaire CIFS](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/smb.js), [montage et options](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/_mount.js), [test de 10 Mio](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/abstract.js), [cycle de vie de la destination](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/remotes.mjs), [dépendance du RPM XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec).
{{< /details >}}
