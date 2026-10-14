---
title: Dépanner les échecs de sauvegarde et les problèmes XOA-HL
description: Examiner les états et résultats partiels des sauvegardes, puis les connexions et mises à jour.
weight: 42
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:14e5a0d9728e81817eec0da5ba28dbc63fa087c7bb5a7718d1dc33b61df29223
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Partez du symptôme et de l’opération qui l’a précédé. Préservez les éléments de diagnostic avant de réessayer une mise à jour ou un import en échec.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Ces vérifications ne constituent pas un relevé de pannes reproduites ni de récupérations vérifiées. Les commandes ci-dessous s’exécutent dans l’appliance, pas sur l’hôte hyperviseur.
{{< /callout >}}

## Choisir la prochaine vérification

| Symptôme | Vérification et action suivante | À vérifier avant de continuer |
| --- | --- | --- |
| La page de l’appliance ne s’ouvre pas | Dans XO Lite, vérifiez que la VM fonctionne et que son adresse/réseau sont corrects. Examinez `xo-server` et l’espace disque par la console, ci-dessous. | L’URL correcte ouvre la page de connexion |
| Les identifiants initiaux échouent | Suivez la [première connexion](/docs/xoa-hl/first-login/) pour les identifiants web et le compte de secours. Examinez les journaux de provisionnement par un accès console autorisé. | La connexion fonctionne et le mot de passe initial a été changé |
| Hôte activé mais inventaire vide | Dans Settings → Servers, lisez l’erreur. Vérifiez adresse, identifiants, identité du certificat et connectivité depuis l’appliance. | Hôte et stockage attendus apparaissent sans erreur |
| Création ou installation de VM en échec | Revérifiez pool, modèle, capacité du SR, réseau et média de démarrage avec [le tutoriel VM](/docs/xoa-hl/create-vm/). Notez l’erreur de tâche avant de réessayer. | La VM jetable démarre l’installateur prévu |
| Sauvegarde ou restauration en échec | Lisez le journal de tâche et vérifiez destination, identifiants, capacité de stockage et SR cible. Suivez [le tutoriel de sauvegarde](/docs/xoa-hl/backup-restore/) ; retirez toutes les cartes réseau restaurées avant le premier démarrage. | La tâche réussit et l’invité restauré isolé possède les données attendues |
| Page de mise à jour déconnectée | Lisez le journal d’installation gérée et l’état du service ; le RPM redémarre `xo-server`. Ne lancez pas une seconde transaction. | Marqueur final de succès, version attendue, connexion et inventaire |
| La vérification indique ERROR | Lisez `/run/xoa-hl/status` et le journal du service de vérification. Examinez les erreurs réseau/dépôt ou l’outil occupé avant de revérifier. | Le nouveau verdict est `UP_TO_DATE` ou `AVAILABLE` |
| Mise à jour automatique non exécutée | Vérifiez mode enregistré, fuseau de l’appliance, délai et timers. Une fenêtre manquée pendant l’arrêt n’est pas rejouée au démarrage. | Le timer prévu est planifié ; les dates d’exécution ultérieures correspondent à la fenêtre |
| Import de configuration en échec | Conservez erreur et journal serveur ; des changements partiels peuvent rester. Suivez [le test d’import isolé](/docs/xoa-hl/configuration-backup/). | Le test sur une appliance jetable neuve réussit ; ne supposez pas la cible défaillante inchangée |

## Diagnostiquer une sauvegarde complète NFS en échec {#backup-failures}

Utilisez cette procédure uniquement pour la [tâche complète NFS de laboratoire](/docs/xoa-hl/backup-restore/), avec un compte administrateur XOA-HL. Préparez les ID de tâche/planification, l’UUID de la VM source, l’ID de destination, l’heure prévue avec fuseau et le dernier résultat de restauration isolée. L’examen se fait dans le **navigateur** ; les vérifications de stockage relèvent de son administrateur. Aucune panne ne doit être provoquée. Chaînes delta, réplication et récupération en production nécessitent des procédures distinctes.

### 1. Identifier l’exécution et conserver ses détails

1. Ouvrez **Sauvegardes → Vue d’ensemble** (`/#/backup/overview`) et trouvez la tâche. Examinez le tableau **Logs** en dessous. Effacez au besoin les filtres de recherche/état des journaux, puis rapprochez tâche et heure de début. Le tableau abrège l’ID de tâche ; utilisez les ID complets des détails plutôt que le seul nom.
2. Cliquez sur le bouton d’état de l’exécution pour ouvrir ses détails. Notez `id`, `jobId`, `scheduleId`, dates de début/fin et état. Utilisez le presse-papiers ou **Download log** pour conserver le JSON en privé avant toute modification. Préparez un extrait expurgé pour le signalement ; le téléchargement ne masque pas automatiquement les données sensibles.
3. Effacez la recherche des détails et sélectionnez tous les états de sous-tâches. Examinez chaque page de tâches VM : la fenêtre peut initialement ne montrer que les tâches en cours/en échec/interrompues et affiche cinq entrées par page. Identifiez l’UUID de VM, puis ses tâches de snapshot, destination/export et transfert. Conservez erreurs, motifs d’omission et avertissements à chaque niveau utile. Toutes les tâches brutes ne sont pas affichées ; consultez le JSON conservé si l’arbre visible est incomplet.

**Vérification :** les éléments identifient une exécution précise et la VM/destination concernée. L’absence de journaux ou de tâches ne prouve pas qu’aucune opération n’a eu lieu.

### 2. Interpréter l’état avant de réessayer

Ces libellés exacts viennent des catalogues ce38. En français, **Started** est **Démarré** ; en japonais, **スタートしました**. Les autres états ci-dessous, **Logs** et **Download log**, utilisent le texte anglais par défaut à cette version.

| État / valeur JSON | Sens et prochaine vérification |
| --- | --- |
| Démarré / `pending` | L’exécution est enregistrée comme active. Actualisez et examinez la progression ; l’absence d’heure de fin n’est pas un succès. Ne lancez pas d’autre exécution. |
| Successful / `success` | L’exécution et ses tâches enregistrées se sont terminées avec succès. Lisez les avertissements et confirmez le nouveau point ; vérifiez séparément la récupération de l’invité et des données. |
| Skipped / `skipped` | Des opérations ont été omises. Lisez le motif : ces sources classent notamment `no disks found`, `no VMs match this pattern` et `unhealthy VDI chain` comme omis. Ce n’est pas une nouvelle sauvegarde vérifiée. |
| Failed / `failure` | L’exécution ou une sous-tâche a échoué. D’autres opérations ont pu réussir ; examinez l’étape concernée et l’inventaire réel des sauvegardes. |
| Interrupted / `interrupted` | Un début n’a pas de fin correspondante et le serveur ne considère plus cette exécution comme active. Conservez la chronologie serveur et l’inventaire des objets partiels ; cet état ne prouve ni retour arrière ni possibilité de réessayer sans risque. |
{.xoa-backup-diagnosis}

### 3. Distinguer l’étape défaillante des données conservées

Utilisez **Sauvegardes → Restaurer** (`/#/backup/restore`) pour l’inventaire des points et les journaux de restauration.

| Observation | À vérifier avant de choisir une correction |
| --- | --- |
| Aucune exécution correspondante | Revérifiez filtres, ID de tâche/planification, activation, fuseau, disponibilité serveur et [relecture de la planification](/docs/xoa-hl/backup-restore/#backup-schedules). Ne supposez ni rattrapage automatique ni réception d’un courriel. |
| Erreur de VM ou snapshot, VM omise | Vérifiez UUID sélectionné, disques, connexion hôte et capacité du SR source. Conservez le motif exact. Ne supprimez pas de snapshots et ne modifiez pas de chaîne VDI comme correction générique. |
| Erreur de destination, d’export ou de transfert | Vérifiez accès appliance-NFS, permissions/options d’export et capacité de destination avec le responsable du stockage. Un test de destination réussi ne prouve pas l’export ou la restauration complète. |
| Transfert réussi, puis échec | Avec **Delete first** désactivé, cet export complet écrit les données et métadonnées avant de supprimer les anciens points. Un nouveau point peut subsister après un échec de nettoyage. Vérifiez dates et points conservés avant de relancer ou de supprimer des fichiers. |
| Point absent de Restore | Ouvrez **Sauvegardes → Restaurer** et actualisez. Vérifiez l’activation de la destination et les erreurs de chargement. Une destination illisible peut être absente ; une liste vide ne prouve pas la suppression de ses sauvegardes. |
| Restauration en échec | Lisez les journaux de restauration sur cette page, vérifiez lecture de la destination et accès au SR/hôte cible, puis inventoriez VM/disques partiels par UUID. Gardez VM source et sauvegarde ; ne supprimez pas au seul nom. |
{.xoa-backup-diagnosis}

**Vérification :** distinguez étape défaillante, points conservés et objets dont l’état reste inconnu. Un fichier ou un point listé ne prouve pas la récupérabilité des données.

### 4. Corriger au laboratoire et vérifier le résultat

1. Pour suspendre les prochains déclenchements, désactivez la planification exacte dans Vue d’ensemble et actualisez pour vérifier son état. Cela n’annule pas une exécution active. Le contrôle d’annulation de cette vue est désactivé à cette version ; redémarrer `xo-server` n’est pas une procédure d’annulation ou de nettoyage de sauvegarde.
2. Corrigez le problème identifié d’accès/capacité/sélection avec son responsable et relisez tâche, planification, VM et destination. Gardez **Delete first** désactivé et protégez les copies indispensables hors de la rétention de cette tâche. Si l’activité ou la propriété d’objets partiels reste incertaine, préservez les éléments et demandez de l’aide avant de réessayer.
3. Une fois l’absence d’exécution active et l’état établis, utilisez l’exécution manuelle ordinaire du tutoriel pour cette tâche de laboratoire à une VM. Les contrôles restart/force des détails **exécutent des sauvegardes** ; ils ne redémarrent pas l’invité et ne sont pas un diagnostic en lecture. Cette procédure n’utilise pas force et ne prétend pas qu’une nouvelle tentative laisse la rétention inchangée.
4. Examinez nouvelle exécution et inventaire des points, puis [restaurez une copie arrêtée, retirez toutes ses cartes réseau et vérifiez les données témoin](/docs/xoa-hl/backup-restore/). Laissez la planification désactivée. Notez erreur initiale, correction, nouveaux ID d’exécution/point et résultat isolé avant d’envisager une reprise planifiée.

**Vérification :** exécution corrigée, inventaire conservé et restauration isolée de l’invité/des données réussissent tous. Sinon, gardez l’incident ouvert et [signalez les éléments expurgés](#signaler-un-problème). Validation des pannes/récupérations sur appliance et revue humaine des langues restent en attente pour ce brouillon.

## Diagnostic en lecture dans l’appliance

Utilisez une console ou une session SSH autorisée, avec les privilèges root si nécessaire. L’absence d’un fichier d’état avant la première vérification ou après redémarrage ne prouve pas un échec. Un résultat non nul de `systemctl status` peut décrire une unité inactive ou défaillante ; lisez l’état affiché.

```bash
rpm -q xoa-hl nodejs
timedatectl
df -h
systemctl status xo-server redis xoa-hl-update.service --no-pager
systemctl list-timers 'xoa-hl-*'
journalctl -u xo-server -u xoa-hl-check-update.service -u xoa-hl-update.service -u xoa-hl-auto-update.service --since '1 hour ago' --no-pager
tail -n 100 /var/log/xoa-first-boot.log
tail -n 100 /var/lib/xoa-hl/update.log
cat /run/xoa-hl/status
cat /var/lib/xoa-hl/auto-update.status
```

Ne supprimez pas base de données, journaux ou verrous pour masquer une erreur. Si le disque est plein, identifiez les fichiers qui grossissent et conservez les éléments de diagnostic avant de choisir un nettoyage. Consultez la [maintenance](/docs/xoa-hl/maintenance/) pour le sens des états et les décisions de mise à jour/redémarrage. L’état automatique peut concerner une ancienne exécution ; comparez ses dates UTC.

## Questions fréquentes

**Pourquoi des mises à jour sont-elles listées avec un code de retour 100 ?** Le vérificateur du paquet traduit le code 100 de `dnf check-update` en `AVAILABLE`, 0 en `UP_TO_DATE` et les autres en `ERROR`. Des mises à jour disponibles ne sont pas un échec d’installation.

**Stable annule-t-il une mise à jour testing ?** Non. Le canal sélectionne les dépôts des vérifications/installations suivantes. Revenir à stable ne rétrograde pas un candidat installé.

**L’export de configuration remplace-t-il une sauvegarde VM ou un retour arrière de l’appliance ?** Non. Consultez le [périmètre et les limites de récupération](/docs/xoa-hl/configuration-backup/) et conservez des sauvegardes distinctes des invités.

## Signaler un problème

[Ouvrez un ticket XCP-HL](https://github.com/Vagrantin/xcp-hl/issues/new). Fournissez ces informations sous forme de texte :

- URL et langue de la page, ou chemin de l’écran de l’appliance concerné.
- Tag de l’image, versions About, versions RPM/Node installées et canal stable/testing.
- Opération, étapes précises, résultat attendu et erreur réelle.
- Heure avec fuseau, mode manuel/automatique, état du service concerné et extrait de journal expurgé.
- Reproduction éventuelle sur une appliance jetable et dernière version fonctionnelle connue.

Retirez mots de passe, jetons, cookies, noms/adresses privés et données utilisateur/invité des journaux et captures. Les journaux `xo-server` et du premier démarrage peuvent contenir des identifiants. Ne joignez jamais d’export de configuration, clé TLS privée ou fichier de configuration complet. Gardez les éléments d’origine en privé.

## Sources

Comportement de cette version : [planification des mises à jour](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [codes de vérification](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [service serveur](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service) et [provisionnement initial](https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-credentials.sh). Les chapitres liés citent leurs sources UI/API épinglées.

Sources du diagnostic de sauvegarde à XO `e281c536` : [vue d’ensemble et détails](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js), [filtres, pagination et affichage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js), [journal brut et relance](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js), [agrégation des états](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/backups-ng-logs.mjs), [ordre export complet/suppression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [erreurs de liste et journaux de restauration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js).
