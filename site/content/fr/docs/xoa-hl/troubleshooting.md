---
title: Dépanner les échecs de sauvegarde et les problèmes XOA-HL
description: Diagnostiquer la connectivité réseau et les sauvegardes ; examiner les chemins invité, hôte et appliance, puis les mises à jour.
weight: 42
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:bb6d15dd15b3e502c1e1770927a32cabf5969239caf8cf0799a53f5bad49ba59
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

Pour les commandes de console ou un écran vide/sans réponse, suivez [les vérifications de console](/docs/xoa-hl/vm-operations/#vm-console).

## Diagnostiquer la connectivité réseau {#network-connectivity}

Utilisez cette investigation en lecture seule pour un réseau invité ordinaire existant ou le [VLAN de laboratoire](/docs/xoa-hl/storage-networks/#host-vlan-network). Connectez-vous comme administrateur XOA-HL pour examiner l’inventaire complet des VM, pools et hôtes. Les vérifications invité nécessitent une session console autorisée ; celles du commutateur, du DNS et du pare-feu relèvent de leurs responsables. Gardez un accès console indépendant à l’hôte. Ne provoquez pas de panne et ne modifiez pas le réseau de gestion pour tester ce guide. Bonds, SDN, trunks VLAN invités et récupération réseau d’urgence nécessitent des procédures distinctes.

### 1. Identifier le chemin en échec

Notez l’heure avec fuseau, la dernière opération réussie, l’erreur exacte, la machine source, le nom/adresse de destination, le protocole et le port du service. Conservez l’état initial avant toute nouvelle tentative. Un test réussi depuis votre ordinateur ne prouve pas l’accès depuis l’appliance, l’hôte ou l’invité.

| Chemin | Où examiner |
| --- | --- |
| Navigateur → appliance | Vérifiez l’URL prévue, la résolution du nom et l’identité du certificat sur le client ; utilisez la console autorisée de l’appliance si la page est inaccessible. Suivez les vérifications de service ci-dessous. |
| Appliance → hôte | Lisez l’erreur de connexion à `/#/settings/servers`, puis suivez [la connexion des hôtes](/docs/xoa-hl/hosts-pools/). Activé décrit une configuration, pas une connexion fonctionnelle. |
| Hôte → SR NFS | Examinez le SR exact et le rattachement/emplacement de cet hôte avec [les vérifications du stockage](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Un test depuis l’invité ou l’appliance ne remplace pas l’accès de l’hôte. |
| Appliance → destination de sauvegarde | Suivez [le diagnostic des sauvegardes](#backup-failures). Un SR NFS et une destination de sauvegarde ont des clients et identités différents. |
| Invité → pair/service | Suivez la correspondance des interfaces et les vérifications invité ci-dessous. Une connexion XO ou un affichage console réussi ne prouve pas l’accès réseau invité. |

### 2. Relier une interface invitée à la liaison de l’hôte

1. Notez l’UUID de la VM, son état d’alimentation, l’hôte résident et le pool. Ouvrez son onglet réseau (`/#/vms/<id>/network`). Copiez l’UUID de la ligne VIF ; notez numéro de périphérique, MAC, réseau, MTU et état. Retrouvez l’UUID exact du réseau dans le pool (`/#/pools/<id>/network`), pas seulement son nom. Lisez les champs sans cliquer sur les valeurs réseau/MAC modifiables ni les boutons de connexion.
2. **Connecté** indique le rattachement du VIF. Un VIF détaché sur une VM arrêtée ne démontre pas une panne. **Adresses IP** provient des métriques invité regroupées par périphérique VIF ; une adresse absente ne prouve pas une configuration invitée manquante, et une adresse affichée n’est pas un test d’accessibilité en direct. Comparez avec la console invitée et [les vérifications de l’agent](/docs/xoa-hl/guest-tools/).
3. Relevez l’indicateur de verrouillage et les **IPs autorisées** séparément des adresses signalées. Ce sont des réglages de politique du trafic, pas un formulaire d’attribution de l’adresse IP invitée. Conservez tout avertissement et faites interpréter la politique effective par le responsable réseau. Ne déverrouillez pas l’interface, ne retirez pas les restrictions, ne changez pas MAC/MTU et ne désactivez pas la sécurité pour accélérer le diagnostic.
4. Dans la ligne réseau du pool, développez **PIFs** et retrouvez l’hôte résident. Le résumé VLAN utilise le maître ; examinez l’onglet réseau de l’hôte réel (`/#/hosts/<id>/network`) pour l’UUID du PIF, périphérique/MAC, réseau, VLAN, MTU, indicateur de gestion et modes IP. Comparez avec l’inventaire approuvé du câblage/commutateur. Un réseau volontairement interne peut ne pas avoir de liaison physique ; établissez la topologie attendue avant de conclure à une panne.
5. Lisez séparément rattachement et porteuse. Le bouton **Connecté** de l’hôte indique le rattachement du PIF ; l’icône de liaison physique et l’état PIF développé du pool utilisent la porteuse. Des métriques PIF absentes peuvent aussi produire une porteuse fausse dans cette source : une indication négative seule ne prouve donc pas un câble débranché. Actualisez et comparez avec les observations hôte/commutateur. Ne basculez pas les PIF, ne modifiez pas VLAN/MTU/IP, ne supprimez pas de réseau et ne redémarrez pas le réseau pour sonder ce chemin.

### 3. Comparer les paramètres invité et les résultats du service

Depuis la **console invitée**, identifiez l’interface par sa MAC et examinez adresse/préfixe, routes et DNS avec les outils de cet OS. Ne supposez pas que le nom d’interface invité correspond au périphérique de l’hôte. Comparez avec l’adresse unique et le sous-réseau approuvés ; dans l’exercice lié, un VLAN marqué côté hôte présente normalement une interface non marquée à l’invité.

Faites tester le pair et le service applicatif convenus depuis cet invité précis par les administrateurs invité/réseau. Consignez séparément réponses DNS, famille d’adresses choisie, destination, protocole/port et résultat. Si les tests par nom et adresse diffèrent, examinez DNS et identité applicative/TLS avant de conclure ; HTTPS par IP seule peut modifier le comportement du certificat ou de l’hôte virtuel. Ne contournez jamais la vérification du certificat pour déclarer une réussite. Un ping réussi ne prouve pas le fonctionnement d’un service ; un ping échoué n’établit pas l’isolation. Testez uniquement les destinations approuvées, dont celles interdites définies par le responsable si l’isolation est requise.

Un résultat entre VM sur le même hôte ne teste pas la liaison physique. Les tests inter-hôtes ou externes nécessitent des pairs identifiés et un chemin de commutation approuvé ; ne migrez pas une charge pour improviser un diagnostic. Préservez les preuves d’un accès inattendu à la production et arrêtez normalement l’invité de test jetable. Si gestion ou stockage sont affectés, utilisez la console indépendante et le plan de récupération du responsable avant d’autres changements.

### 4. Vérifier la correction choisie par le responsable

Transmettez au responsable les correspondances exactes, heures, erreur et comparaisons. Appliquez la correction convenue via la procédure invité, stockage, hôte ou réseau appropriée ; cette investigation ne prescrit pas de réinitialisation générique. Actualisez ensuite l’inventaire et répétez le **même test de service entre la même source et la même destination**, ainsi que l’isolation requise et les accès gestion/stockage. Notez le changement et le résultat observé. Un indicateur vert seul ne clôt pas l’incident. Si le chemin reste incertain, gardez l’incident ouvert et partagez un rapport expurgé ; la validation des pannes/récupérations sur installation réelle reste en attente.

## Diagnostiquer une sauvegarde complète NFS en échec {#backup-failures}

Utilisez cette procédure uniquement pour la [tâche complète NFS de laboratoire](/docs/xoa-hl/backup-restore/), avec un compte administrateur XOA-HL. Préparez les ID de tâche/planification, l’UUID de la VM source, l’ID de destination, l’heure prévue avec fuseau et le dernier résultat de restauration isolée. L’examen se fait dans le **navigateur** ; les vérifications de stockage relèvent de son administrateur. Aucune panne ne doit être provoquée. Chaînes delta, réplication et récupération en production nécessitent des procédures distinctes.


[Tester les sauvegardes incrémentales et la récupération de chaîne](/docs/xoa-hl/backup-restore/#delta-backups).
[Télécharger et vérifier un fichier d’un point delta conservé](/docs/xoa-hl/backup-restore/#file-restore).
[Tester une réplique DR complète et son clone isolé sur un autre pool](/docs/xoa-hl/backup-restore/#dr-replica).

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

**Un point de métadonnées prouve-t-il la récupération d’un hôte ?** Non. Le [pilote des métadonnées de pool](/docs/xoa-hl/configuration-backup/#pool-metadata) vérifie seulement l’export, la rétention et l’identité des fichiers. La restauration sur un pool jetable isolé reste à valider.

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

Sources du diagnostic réseau (XO `e281c536`): [VM network UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [Host network UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [Pool network UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [PIF carrier display](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [Guest metrics and interface mapping](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [Server connection state](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js).
