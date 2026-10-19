---
title: "Exporter la configuration XO"
linkTitle: "Export de la configuration"
description: "Exportez la configuration XO, testez un import sans risque et sauvegardez les métadonnées du pool."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: draft
sourceRevision: sha256:180ae9b2a6163db1325b4575e8cf083b05b36f83cd0dc30021bc5104b3f91bf7
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Sauvegardez les réglages XO séparément des sauvegardes de VM avant la maintenance de l’appliance.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38`, XO 5.113.2 à `e281c536`. Les tests aller-retour d’export/import et de récupération sur une appliance jetable restent à faire. Cette page n’établit pas de procédure de récupération ou de rétrogradation prise en charge.
{{< /callout >}}

## Ce que protège l’export

L’export web sérialise les entrées de configuration XO enregistrées : utilisateurs/groupes, règles d’accès, connexions aux serveurs, destinations distantes, tâches, planifications, jetons d’authentification et réglages des plugins. Traitez-le comme un secret : il peut contenir mots de passe des serveurs, identifiants des destinations et jetons.

| Élément | Protection à prévoir |
| --- | --- |
| Configuration XO | Export par Settings → Config |
| Disques et données des invités | [Sauvegarde et restauration de VM](/docs/xoa-hl/backup-restore/) distinctes |
| Métadonnées des hôtes/pools | [Sauvegarde des métadonnées du pool](#pool-metadata) distincte ; absentes de cet export |
| OS de l’appliance, RPM et journaux d’exécution | Absents de l’export |
| TOML serveur, fichiers TLS, réglages de mise à jour et fuseau horaire | À consigner séparément ; absents de l’export |

La fin d’un export ne prouve pas que le fichier peut restaurer votre installation. Conservez avec lui les identités de l’image et de l’application.

## 1. Télécharger et conserver l’export

1. Dans le **navigateur**, connectez-vous en administrateur XO. Relevez les [versions installées](/docs/xoa-hl/maintenance/).
2. Ouvrez **Settings → Config** (`/#/settings/config`) et choisissez **Download config** sous **Export config**. Les libellés peuvent varier avec la langue ; le chemin reste identique.
3. Saisissez une phrase secrète unique et confirmez. Un champ vide produit un export non chiffré. Conservez la phrase séparément pour qu’elle reste accessible si l’appliance est perdue.
4. Autorisez le téléchargement si le navigateur bloque la nouvelle fenêtre. Vérifiez qu’un fichier non vide est enregistré : l’API utilise `config.json.gz`, avec `.enc` si chiffré. Ne le renommez pas comme une sauvegarde de VM.
5. Déplacez le fichier vers un stockage protégé hors de l’appliance. Notez date, taille, versions et choix du chiffrement. Gardez un export antérieur jusqu’à ce que le nouveau réussisse un test d’import isolé.

**Vérification :** le fichier téléchargé et la phrase conservée séparément sont accessibles sans l’appliance d’origine. Ne joignez pas le fichier à un ticket public et ne copiez pas son contenu déchiffré dans un rapport.

## 2. Préparer un test d’import isolé

{{< callout type="warning" >}}
L’import peut reconnecter les serveurs enregistrés et activer les planifications. Il peut modifier des entrées existantes et remplacer des identités utilisateur en conflit. Il n’a pas de retour arrière global : une erreur peut laisser des modifications partielles. N’utilisez jamais une appliance de production pour découvrir les effets d’un export non testé.
{{< /callout >}}

Utilisez une appliance jetable avec la même image et le même paquet enregistrés. Avant l’import, limitez son réseau : votre navigateur de test doit pouvoir l’atteindre, mais elle ne doit atteindre ni hôtes de production, ni destinations de sauvegarde, ni services externes. Cette restriction doit être imposée hors de la configuration XO importée ; désactiver connexions ou planifications avant l’import ne suffit pas, car l’import peut les restaurer.

1. Relevez l’état de l’appliance neuve et préparez les identifiants de la configuration exportée ; l’import peut changer les comptes.
2. Ouvrez **Settings → Config**, sélectionnez ou déposez le fichier, choisissez **Import config** et saisissez la phrase de l’export. Attendez l’état de réussite ou d’erreur.
3. En cas de succès, déconnectez-vous et testez un compte administrateur exporté. Comparez utilisateurs, permissions, destinations, définitions de serveurs, tâches et planifications avec l’état source. Des erreurs de connexion aux serveurs sont attendues tant que le réseau est bloqué.
4. Désactivez les planifications importées et retirez ou remplacez les destinations de production avant d’autoriser l’accès à des ressources de test jetables. Revérifiez ces réglages avant chaque opération de test.
5. En cas d’échec, notez l’erreur et les journaux `xo-server` expurgés. Supprimez l’appliance jetable et repartez d’une neuve pour réessayer ; ne supposez pas que l’échec a laissé son état intact.

**Validation encore nécessaire :** aller-retour chiffré et non chiffré, phrase incorrecte, utilisateurs en conflit, import interrompu, isolation des destinations, connexion administrateur exportée et permissions/tâches représentatives. Une bannière de succès ne suffit pas à valider la récupération.

## 3. Vérifier la sauvegarde des métadonnées du pool {#pool-metadata}

Cette **prévisualisation vérifiée dans les sources** utilise une tâche **Pool metadata** distincte. XO demande au pool un flux XAPI `/pool/xmldbdump` et écrit `data` et `metadata.json` sur une destination distante dans `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. Ce n’est ni l’export de Settings → Config, ni une sauvegarde des disques des VM, ni une image de l’appliance ou une récupération d’hôte validée. Les métadonnées peuvent révéler l’infrastructure : limitez l’accès à la destination et ne joignez pas ces fichiers à un ticket public.

Utilisez un pool jetable que vous pouvez reconstruire, connecté à XOA-HL, et une destination NFS dédiée accessible en écriture hors du domaine de panne de son stockage. Conservez séparément un [plan de sauvegarde et restauration des VM](/docs/xoa-hl/backup-restore/) pour les données invitées. Vérifiez l’image et le paquet installés ainsi que l’accès de l’administrateur aux contrôles des métadonnées ; l’interface épinglée impose un niveau d’offre, donc arrêtez-vous si ces contrôles sont indisponibles. Notez l’UUID du pool, les identités du maître/des hôtes, l’ID et la capacité de la destination. Ne modifiez et ne restaurez aucun pool de production pour cet essai.

1. Dans **Backup → New → Metadata** (`/#/backup/new/metadata`), créez `lab-pool-metadata`. Activez uniquement **Pool metadata**, choisissez explicitement ce pool jetable, laissez **XO config** désactivé et sélectionnez seulement la destination dédiée. N’ajoutez pas d’autre pool ou destination. Créez une planification avec un fuseau horaire explicite, fixez **Pool metadata retention** à `2` et laissez-la désactivée. Enregistrez puis relisez les ID de tâche/planification, pool/destination, mode, rétention et état désactivé. Arrêtez-vous si l’éditeur ne conserve pas ces valeurs.
2. Lancez manuellement cette tâche avec sa planification enregistrée trois fois à des heures distinctes A/B/C. Attendez la fin de chaque exécution. Examinez le journal par pool et destination, y compris les sous-tâches ; une réussite générale ne prouve pas à elle seule que la copie distante est complète. Notez ID/état de chaque exécution et UUID du pool source.
3. Dans **Backup → Restore → Metadata** (`/#/backup/restore/metadata`), examinez les entrées **pool**, les dates et points disponibles des destinations activées. **Ne choisissez ni Restore ni Delete.** Pour ce cas simple de rétention 2, confrontez A/B/C à l’inventaire B/C. Si l’administrateur du stockage peut accéder séparément à la destination, faites-lui confirmer pour chaque point conservé des fichiers `data` et `metadata.json` non vides, avec les bonnes identités de tâche/planification/pool ; relevez tailles et empreintes protégées sans publier le contenu. Le code désactive la somme de contrôle à l’écriture : un point visible ou une tâche réussie ne prouve pas qu’XAPI peut l’importer. Préservez tout point incomplet ou écart de purge pour analyse.

**Réussite de l’essai de sauvegarde :** la planification reste désactivée, trois exécutions désignent le bon pool et la bonne destination, et les points B/C et fichiers protégés correspondent aux identités relevées. En cas d’échec d’export, d’écriture, de nettoyage ou de liste, arrêtez les exécutions et conservez journaux et inventaire ; ne supprimez pas les chemins de sauvegarde sur leur seul nom.

**Validation de restauration encore en attente :** la restauration de pool envoie `data` du point choisi vers `/pool/xmldbdump` sur le pool cible sélectionné. Cette opération modifie son état, sans retour arrière démontré ici. Avant toute restauration, le responsable du pool doit fournir une cible jetable isolée, un plan de récupération correspondant à la version et à l’identité, une image/copie de métadonnées de repli, des réseaux et stockages de production bloqués, et un moyen de vérifier ensuite connectivité et inventaire des hôtes/pools. Un seul point exact et une seule cible seront choisis après cet examen ; restauration groupée et substitution entre pools sont exclues de cet essai. Un point disponible ou un export réussi ne prouve pas la récupération. Conservez séparément l’export XO et les sauvegardes des invités.

## Limites de récupération et de retour arrière

En cas de perte réelle, préservez l’appliance défaillante et les éléments de diagnostic, identifiez les versions exactes et utilisez un plan de récupération testé en isolation pour ces versions. Ne reconnectez pas deux copies avec des planifications actives aux mêmes destinations de production.

Un ancien RPM disponible n’est pas un retour arrière complet : sa rétrogradation n’annule pas les mises à jour OS, ne restaure pas les données XO et ne récupère pas les fichiers distincts listés ci-dessus. Les imports entre versions et la récupération par rétrogradation restent non vérifiés pour cette version. Consultez la [maintenance](/docs/xoa-hl/maintenance/) et le [dépannage](/docs/xoa-hl/troubleshooting/) en cas d’échec de mise à jour.

## Sources

Sources XO à `e281c536` : [écran de configuration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [API administrateur et format](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [chiffrement et import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [reconnexion des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [activation des planifications](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs) et [conflits utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).

Sources de l’essai des métadonnées de pool (XO `e281c536`) : [éditeur et niveau d’offre](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [API administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [export du pool et fichiers distants](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [modes et destinations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [purge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [choix du point](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js) et [point d’import XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
