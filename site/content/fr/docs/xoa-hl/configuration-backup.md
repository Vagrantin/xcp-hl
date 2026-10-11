---
title: Exporter la configuration XO et préparer la récupération
description: Conserver un export chiffré et comprendre les limites de l’import et du retour arrière.
weight: 41
translationKey: xoa-manual-configuration-backup
translationStatus: draft
sourceRevision: sha256:6ea2d8b7f9eb7d3a324bdf211a2c6e13676572afc1608ffb59b11fe1536736aa
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
| Métadonnées des hôtes/pools | Protection distincte ; absentes de cet export |
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

## Limites de récupération et de retour arrière

En cas de perte réelle, préservez l’appliance défaillante et les éléments de diagnostic, identifiez les versions exactes et utilisez un plan de récupération testé en isolation pour ces versions. Ne reconnectez pas deux copies avec des planifications actives aux mêmes destinations de production.

Un ancien RPM disponible n’est pas un retour arrière complet : sa rétrogradation n’annule pas les mises à jour OS, ne restaure pas les données XO et ne récupère pas les fichiers distincts listés ci-dessus. Les imports entre versions et la récupération par rétrogradation restent non vérifiés pour cette version. Consultez la [maintenance](/docs/xoa-hl/maintenance/) et le [dépannage](/docs/xoa-hl/troubleshooting/) en cas d’échec de mise à jour.

## Sources

Sources XO à `e281c536` : [écran de configuration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [API administrateur et format](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [chiffrement et import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [reconnexion des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [activation des planifications](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs) et [conflits utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
