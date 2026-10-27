---
title: "Exporter la configuration XO"
linkTitle: "Export de la configuration"
description: "Exportez la configuration XO, testez un import sans risque et sauvegardez les métadonnées du pool."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: draft
sourceRevision: sha256:47bd25499d03a51e8e54d786509e24cbb52eb52d99badf9e81e690b46793c9e1
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Avant la maintenance de l’appliance, enregistrez la configuration XO dans un fichier et conservez-le à part de vos sauvegardes de VM. Testez ensuite ce fichier sur une appliance jetable. Les métadonnées du pool demandent leur propre tâche de sauvegarde, décrite plus bas. Vous travaillez dans le **navigateur**, connecté à XOA-HL en tant qu’administrateur XO.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261027-ca44911`, paquet `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Testé sur des appliances de laboratoire le 2026-10-27 : export, import et récupération sur une nouvelle appliance de la même version. Cette page ne décrit pas de procédure de récupération ou de rétrogradation prise en charge. Image reconstruite le 2026-10-27 avec le correctif de configuration de `build-xoa-hl@fa0c987`. Voir [comment identifier le fichier corrigé](/docs/xoa-hl/first-login/#identify-the-rebuilt-image). Les résultats d’export/import et de création de VM consignés dans [#315](https://github.com/Vagrantin/xcp-hl/pull/315) précèdent cette reconstruction. Aucun nouveau test de ces opérations sur le fichier reconstruit n’est consigné ici.
{{< /callout >}}

## Ce que contient l’export {#export-contents}

L’export enregistre la configuration XO : utilisateurs et groupes, règles d’accès, connexions aux serveurs, destinations distantes, tâches, planifications, jetons d’authentification et réglages des plugins. Traitez le fichier comme un secret : il peut contenir des mots de passe de serveurs, des identifiants de destinations et des jetons.

| Élément | Comment le protéger |
| --- | --- |
| Configuration XO | Cet export, depuis **Paramètres → Configuration** |
| Disques et données des invités | Une [sauvegarde et restauration de VM](/docs/xoa-hl/backup-restore/) distincte |
| Métadonnées des hôtes et du pool | Une [sauvegarde des métadonnées du pool](#pool-metadata) distincte. Absentes de cet export |
| OS de l’appliance, paquets RPM et journaux d’exécution | Absents de l’export |
| Fichier TOML du serveur, fichiers TLS, réglages de mise à jour et fuseau horaire | Absents de l’export. Notez-les séparément |

Un export terminé ne prouve pas que le fichier peut restaurer votre installation. Notez avec lui les versions de l’image et de l’application.

## 1. Télécharger et conserver l’export

1. Dans le **navigateur**, connectez-vous en tant qu’administrateur XO. Notez les [versions installées](/docs/xoa-hl/maintenance/#record-versions).
2. Ouvrez **Paramètres → Configuration** (`/#/settings/config`). Sous **Exporter**, sélectionnez **Télécharger la configuration actuelle**.
3. Saisissez une phrase secrète unique et confirmez. Si vous laissez le champ vide, l’export n’est pas chiffré.
4. Conservez la phrase secrète séparément, pour l’avoir encore si l’appliance est perdue.
5. Si le navigateur bloque la nouvelle fenêtre, autorisez le téléchargement. Vérifiez qu’un fichier non vide a été enregistré : `config.json.gz`, avec `.enc` en plus s’il est chiffré. Ne le renommez pas pour le faire passer pour une sauvegarde de VM.
6. Déplacez le fichier vers un stockage protégé hors de l’appliance. Notez la date, la taille du fichier, les versions et s’il est chiffré.
7. Gardez votre export précédent jusqu’à ce que le nouveau réussisse un test d’import sur une appliance isolée.

**Vérification :** vous pouvez accéder au fichier et à sa phrase secrète sans l’appliance d’origine. Ne joignez jamais le fichier à un ticket public et ne collez jamais son contenu déchiffré dans un rapport.

## 2. Tester un import sur une appliance isolée {#import-test}

{{< callout type="warning" >}}
Un import peut reconnecter les serveurs enregistrés et activer les planifications enregistrées. Il peut modifier des entrées existantes et remplacer des utilisateurs en conflit. Il n’existe pas de retour arrière pour l’ensemble de l’import : une erreur peut laisser des modifications partielles. N’utilisez jamais une appliance de production pour découvrir ce que fait un export non testé.
{{< /callout >}}

**Avant de commencer**

- Utilisez une appliance jetable avec les mêmes versions d’image et de paquet que celles que vous avez notées.
- Limitez son réseau avant l’import : votre navigateur de test peut l’atteindre, mais elle ne peut atteindre ni les hôtes de production, ni les destinations de sauvegarde, ni les services externes.
- Imposez cette limite en dehors de XO. Désactiver les connexions ou les planifications avant l’import ne suffit pas, car l’import peut les restaurer.
- Notez l’état de l’appliance neuve. Préparez les identifiants de la configuration exportée : l’import peut modifier les comptes.

1. Ouvrez **Paramètres → Configuration**. Sélectionnez ou déposez le fichier d’export, sélectionnez **Importer**, puis saisissez la phrase secrète de l’export. Attendez le message de réussite ou d’erreur.
2. Si l’import réussit, déconnectez-vous, puis connectez-vous avec un compte administrateur issu de l’export.
3. Comparez les utilisateurs, les permissions, les destinations, les serveurs, les tâches et les planifications avec vos notes sur la source. Des erreurs de connexion aux serveurs sont attendues tant que le réseau est bloqué. L’import ne supprime pas les comptes absents du fichier : supprimez tout compte inattendu, par exemple `admin@admin.net`.
4. Avant d’autoriser l’accès à des ressources de test jetables, désactivez les planifications importées et retirez ou remplacez les destinations de production. Revérifiez ces réglages avant chaque test.
5. Si l’import échoue, notez l’erreur et les journaux `xo-server`, sans les secrets. Supprimez l’appliance et repartez d’une appliance neuve pour la tentative suivante. Ne supposez pas qu’un import échoué n’a rien modifié.

Vérifiez d’abord que l’administrateur restauré peut se connecter. Dans **Paramètres → Utilisateurs**, supprimez les comptes inattendus ou attribuez des mots de passe uniques aux comptes que vous conservez volontairement. Ne supprimez jamais votre seul administrateur fonctionnel. Dans une fenêtre privée, vérifiez que `admin@admin.net` avec le mot de passe `admin` est refusé, puis enregistrez l’état corrigé par un redémarrage normal de l’appliance avant de rétablir l’accès aux ressources de production. La reconstruction du 2026-10-27 corrige la configuration initiale. Elle ne change pas ce comportement de l’import : les utilisateurs absents de l’export peuvent rester sur la destination.

**Vérification :** l’administrateur exporté peut se connecter, et les utilisateurs, les permissions, les destinations, les tâches et les planifications correspondent à vos notes. Un message de réussite seul ne prouve pas que vous pouvez récupérer votre installation. Une phrase secrète incorrecte, des utilisateurs en conflit et un import interrompu ne sont pas traités ici.

## Mettre en place la sauvegarde des métadonnées du pool {#pool-metadata}

Une tâche **Pool metadata** distincte sauvegarde les métadonnées d’un pool. XO lit un flux XAPI `/pool/xmldbdump` depuis le pool choisi. Il écrit `data` et `metadata.json` sur une destination distante, dans `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. Ce n’est ni l’export de **Paramètres → Configuration**, ni une sauvegarde des disques de VM, ni une image de l’appliance, ni une méthode testée pour récupérer un hôte. Les métadonnées peuvent révéler des détails de votre infrastructure : limitez l’accès à la destination et ne joignez jamais ces fichiers à un ticket public.

**Avant de commencer**

- Utilisez un seul pool jetable, qui vous appartient et que vous pouvez reconstruire, connecté à XOA-HL. Ne modifiez et ne restaurez jamais un pool de production pour ce test.
- Utilisez une destination de sauvegarde NFS dédiée, accessible en écriture, qui ne dépend pas du stockage de ce pool : une seule panne ne doit pas toucher les deux.
- Gardez un [plan de sauvegarde et restauration des VM](/docs/xoa-hl/backup-restore/) distinct pour les données des invités.
- Vérifiez l’image et le paquet installés. Vérifiez que l’administrateur voit les contrôles de sauvegarde des métadonnées : dans cette version, l’interface peut les masquer derrière une vérification d’offre. S’ils sont absents, arrêtez-vous.
- Notez l’UUID du pool, les identités du maître et des hôtes, l’ID de la destination et son espace libre.

### Créer une tâche désactivée

1. Ouvrez **Sauvegardes → Nouveau** et choisissez **XO config & Pool metadata Backup** (`/#/backup/new/metadata`). Nommez la tâche `lab-pool-metadata`.
2. Activez uniquement **Pool metadata**, et laissez **XO config** désactivé.
3. Sélectionnez explicitement le pool jetable. Sélectionnez uniquement la destination dédiée. N’ajoutez pas d’autres pools ni d’autres destinations.
4. Ajoutez une planification avec un fuseau horaire explicite. Réglez **Pool retention** sur `2` et laissez la planification désactivée.
5. Enregistrez. Relisez les ID de la tâche et de la planification, le pool, la destination, le mode, la rétention et l’état désactivé. Si l’éditeur ne les a pas conservés, arrêtez-vous.

### Lancer la tâche trois fois

1. Lancez la tâche à la main depuis sa planification enregistrée. Notez l’heure : c’est l’exécution A.
2. Attendez la fin de l’exécution. Dans le journal de la tâche, vérifiez chaque pool et chaque destination, y compris les sous-tâches. Une réussite globale ne prouve pas que la copie distante est complète.
3. Notez l’ID de l’exécution, son état et l’UUID du pool source.
4. Recommencez pour les exécutions B et C, à des heures différentes. Ne lancez chaque exécution qu’après la fin de la précédente.

### Vérifier les points conservés

1. Ouvrez **Sauvegardes → Restaurer → Métadonnées** (`/#/backup/restore/metadata`). Examinez les entrées **pool** des destinations activées, leurs heures et les points disponibles. **Ne sélectionnez ni Restaurer ni Supprimer.**
2. Avec une rétention de `2`, seuls les points des exécutions B et C restent. Comparez-les avec vos notes sur les exécutions A, B et C.
3. Si l’administrateur de stockage peut ouvrir la destination directement, demandez-lui de vérifier chaque point conservé : `data` et `metadata.json` ne sont pas vides, et les identités de la tâche, de la planification et du pool correspondent. Notez les tailles et les empreintes des fichiers dans un endroit protégé. Ne publiez pas leur contenu.
4. Conservez tout point incomplet ou tout résultat de nettoyage inattendu pour analyse.

La tâche écrit ces fichiers sans somme de contrôle. Un point affiché ou une tâche réussie ne prouve pas que XAPI peut l’importer.

**Vérification :** la planification est toujours désactivée, les trois exécutions désignent le bon pool et la bonne destination, et les points B et C conservés et leurs fichiers correspondent à vos notes. Si l’export, l’écriture sur la destination, le nettoyage ou la liste échoue, arrêtez de lancer la tâche et conservez les journaux et l’inventaire. Ne supprimez jamais des dossiers de sauvegarde d’après leur seul nom.

### Avant toute restauration de pool

La restauration d’un pool envoie le fichier `data` du point choisi vers `/pool/xmldbdump` sur le pool cible. Elle modifie le pool, et aucun moyen de l’annuler n’a été démontré. Avant toute restauration, le responsable du pool doit fournir :

- un pool cible isolé et jetable
- un plan de récupération qui correspond aux versions et aux identités
- une copie de secours distincte de l’image ou des métadonnées
- un accès bloqué aux réseaux et au stockage de production
- un moyen de vérifier ensuite la connectivité et l’inventaire des hôtes et du pool

Seulement après l’examen de ces éléments, choisissez un seul point exact et un seul pool cible. Un point disponible ou un export réussi ne prouve pas que vous pouvez récupérer. Gardez séparés les exports de configuration XO et les sauvegardes des invités. La restauration elle-même n’est pas traitée ici, pas plus que la restauration groupée ou la restauration sur un autre pool.

## Limites de récupération et de retour arrière {#recovery-limits}

En cas de perte réelle, conservez l’appliance défaillante et les preuves. Identifiez les versions exactes, et utilisez un plan de récupération qui a réussi un test isolé pour ces versions. Ne connectez jamais deux copies avec des planifications actives aux mêmes destinations de production.

Un ancien paquet RPM n’est pas un retour arrière complet. Une rétrogradation n’annule pas les mises à jour de l’OS, ne restaure pas les données XO et ne récupère pas les fichiers séparés listés plus haut. Les imports entre `v5.113.2_e281c536-ce43` et `v5.113.2_e281c536-ce47`, qui utilisent la même version de Xen Orchestra, ont fonctionné en laboratoire dans les deux sens. Les imports entre versions de Xen Orchestra et la récupération par rétrogradation n’ont pas été testés. Si une mise à jour échoue, consultez la [maintenance](/docs/xoa-hl/maintenance/#update-problems) et le [dépannage](/docs/xoa-hl/troubleshooting/).

{{< details title="Sources" closed="true" >}}
- **Export de la configuration** : [écran de configuration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [API administrateur et format](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [chiffrement et import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [reconnexion des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [activation des planifications](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [conflits utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
- **Sauvegarde des métadonnées du pool** : [éditeur et niveau d’offre](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [API administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [export du pool et fichiers distants](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [modes et destinations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [purge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [choix du point](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js), [point d’import XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
{{< /details >}}
