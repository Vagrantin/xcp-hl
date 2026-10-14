---
title: Gérer les utilisateurs, les groupes et les droits
description: Vérifier les droits Viewer directs et par groupe local, les membres et la révocation sur une VM jetable.
weight: 26
translationKey: xoa-manual-permissions
translationStatus: draft
sourceRevision: sha256:c423b5c89ce3fcae1ac6cb61eaa2aa4133a77d045d0e3687339cb6daf33960d9
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Utilisez une session administrateur existante dans l’**appliance XOA-HL**, une VM jetable et une session de navigateur distincte pour un nouvel utilisateur de test. Gardez la session administrateur disponible pendant tout l’exercice. Ne modifiez pas le compte du dernier administrateur ni vos propres droits pendant le test.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les sources montrent l’écran ACL activé par le niveau open source par défaut du build ; les tests de l’interface installée, des autorisations/refus et de la révocation restent à faire. Ce n’est pas une exigence d’abonnement Vates.
{{< /callout >}}

## 1. Distinguer compte et rôle sur un objet

**Paramètres → Utilisateurs** (`/#/settings/users`) attribue une permission globale au compte. **Utilisateur** est un compte normal ; **Administrateur** contourne les vérifications ACL des objets. Un droit **Admin** sur un objet est différent : il s’applique à l’objet choisi et à sa portée d’autorisation.

| Rôle ACL sur un objet | Opérations accordées |
| --- | --- |
| Viewer | Consulter |
| Operator | Consulter et opérer |
| Admin | Consulter, opérer et administrer |

Commencez par **Viewer** sur une seule VM de test. Un droit sur un hôte ou pool peut ouvrir un accès à davantage d’objets qu’une seule VM. Un droit accordé à un groupe s’applique à tous ses membres. Les permissions s’additionnent : retirer une ACL ne révoque pas un accès encore accordé par un groupe, un autre objet ou un parent. Ce pilote n’utilise pas de règle de refus.

## 2. Créer une identité de test normale

Dans **Paramètres → Utilisateurs**, créez un utilisateur de test distinct avec un e-mail/identifiant et un mot de passe unique. Choisissez **Utilisateur**, pas l’**Administrateur** global. Vérifiez la permission affichée. N’utilisez pas des identifiants de production et ne mettez pas le mot de passe dans les preuves.

Connectez cet utilisateur dans la session de navigateur distincte et notez sa visibilité initiale avant l’ajout d’une ACL. Vérifiez qu’il s’agit bien de l’identité de test, et non d’une session administrateur réutilisée. Gardez la session administrateur d’origine pour corriger ou retirer le droit de test.

## 3. Accorder Viewer sur une VM

Comme administrateur, ouvrez **Paramètres → Droits** (`/#/settings/acls`). Choisissez uniquement l’utilisateur de test comme sujet, uniquement la VM jetable comme objet et **Viewer** comme rôle, puis ajoutez la règle. Vérifiez le sujet, l’objet et le rôle de la ligne créée. Ne choisissez pas tous les objets ni le pool entier pour cet exercice.

Le formulaire accepte plusieurs sujets et objets, créant une règle pour chaque combinaison. Les filtres d’objets/tags sélectionnent des objets actuels ; cet exercice ne définit pas une politique pour les objets futurs. Confirmez les identités plutôt que de vous fier à des noms proches.

## 4. Vérifier visibilité et opérations restreintes

Actualisez la session de l’utilisateur normal ou reconnectez-le. Vérifiez que la VM attendue est visible et que ses informations de base sont consultables. Vérifiez que démarrage/arrêt et administration sont indisponibles ; si une opération peut être demandée, elle doit être refusée sans modifier la VM. Utilisez uniquement la VM jetable pour ce test négatif. Un bouton masqué ne constitue pas une validation complète de l’autorisation côté serveur.

Si une opération réussit contre toute attente, arrêtez l’exercice. Comme administrateur, examinez la permission globale, les groupes et les autres droits sur la VM, l’hôte ou le pool. N’élargissez pas les droits pour résoudre une erreur inexpliquée. Si l’écran ACL manque dans la version installée, notez les versions et l’erreur et [signalez le problème](/docs/xoa-hl/troubleshooting/) ; ne supposez pas qu’un niveau payant d’une autre édition s’applique.

## 5. Révoquer et vérifier à nouveau

Comme administrateur, retirez l’ACL de test exacte. Actualisez ou reconnectez l’utilisateur de test et vérifiez la disparition de l’accès à la VM. S’il reste, examinez les autres droits directs, de groupes et hérités ; retirer une ligne ne révoque pas tous les droits. Vérifiez aussi que l’administrateur conservé peut toujours se connecter et gérer les objets prévus.

Notez le type de compte, la portée et les résultats attendus/réels sans identifiants secrets. Gardez l’identité de test pour l’exercice de groupe local ci-dessous ; supprimez-la seulement après tous les exercices. Ce pilote ne valide pas chaque opération déléguée, les ensembles de ressources, l’authentification externe, les tâches de sauvegarde déléguées ou la portée des jetons API. Consultez [la gestion des hôtes/pools](/docs/xoa-hl/hosts-pools/) et [l’export de configuration](/docs/xoa-hl/configuration-backup/) avant des changements plus larges.

[Protéger la connexion d’un compte local par des codes à usage unique (OTP)](/docs/xoa-hl/sign-in-otp/).

## 6. Accorder l’accès par un groupe local {#group-access}

Utilisez un nouveau groupe local, l’utilisateur normal de la section 2 et la même VM jetable. Terminez d’abord la section 5 : l’ACL directe de test doit être retirée et aucun autre groupe ou objet parent ne doit encore donner accès à la VM. Gardez un second compte normal hors du groupe comme témoin et conservez la session administrateur. Un groupe applique ses ACL d’objets à ses membres ; y ajouter un utilisateur ne change pas sa permission globale.

1. Ouvrez **Paramètres → Groupes** (`/#/settings/groups`). Saisissez un nom distinct, comme `lab-vm-viewers`, dans **Nouveau nom de groupe**, puis sélectionnez **Créer**. Vérifiez que le nouveau groupe n’a aucun utilisateur. Si le nom existe déjà, choisissez-en un autre sans réutiliser un groupe inconnu et ses droits.
2. Dans **Paramètres → Droits**, choisissez uniquement ce groupe comme sujet, uniquement la VM de test comme objet et **Viewer** comme rôle. Créez la règle et vérifiez la ligne groupe/VM/rôle exacte. Un groupe vide ne donne aucun accès à l’utilisateur : vérifiez que les deux comptes normaux gardent leur visibilité initiale.
3. Dans **Groupes**, choisissez uniquement l’utilisateur prévu dans la colonne **Ajouter un utilisateur** de ce groupe. La sélection envoie immédiatement la modification ; il n’y a pas de bouton Enregistrer séparé. Dépliez le compteur de la colonne **Utilisateur** avec l’icône plus et vérifiez l’identifiant. Dans **Paramètres → Utilisateurs**, examinez le compteur/détail de ses groupes et vérifiez la présence de ce groupe ; confirmez aussi la permission **Utilisateur** du compte. Actualisez les deux vues après une erreur : les deux enregistrements d’appartenance sont écrits séparément, donc une seule liste apparemment correcte ne suffit pas.
4. Actualisez ou reconnectez le membre. Vérifiez qu’il peut consulter la VM, mais que démarrage/arrêt et administration restent indisponibles ou refusés sans modifier cette VM jetable. Vérifiez que le compte témoin n’a toujours pas ce droit. Si le résultat diffère, arrêtez et examinez l’identité, la permission globale, les groupes et toutes les ACL directes/héritées ; n’ajoutez pas de droits plus larges pour faire réussir le test.
5. Dans **Groupes**, dépliez la liste et utilisez l’icône de retrait près de l’identifiant exact de test. Le retrait est envoyé immédiatement, sans dialogue de confirmation. Vérifiez que l’identifiant a disparu du groupe et que le groupe a disparu du détail de l’utilisateur. Actualisez/reconnectez l’ancien membre et vérifiez la perte de l’accès accordé par ce groupe. L’ACL du groupe reste en place : les autres membres éventuels gardent son droit.

Pour vérifier l’addition des droits, remettez l’utilisateur dans le groupe et confirmez le retour de Viewer. Ajoutez une ACL **Viewer** directe pour cet utilisateur sur la même VM, puis retirez uniquement l’ACL du groupe sur cette VM. L’utilisateur doit encore pouvoir la consulter grâce à l’ACL directe. Retirez cette dernière et revérifiez l’accès : sans autre droit, il doit disparaître même si l’utilisateur reste membre du groupe. L’absence d’une règle de groupe n’est pas un refus, et un administrateur global contourne les ACL d’objets.

Pour nettoyer, retirez les ACL de test tant que leurs sujets existent, retirez les appartenances de test et vérifiez les résultats des deux comptes normaux. Revérifiez ensuite la ligne/le nom du groupe local vide, sélectionnez **Supprimer le groupe** sur cette ligne et confirmez la suppression. Le dialogue est générique ; identifiez le groupe avant de l’ouvrir. Actualisez les vues groupes/ACL/utilisateurs et conservez l’administrateur indépendant. La suppression d’un groupe programme le nettoyage asynchrone des ACL et appartenances ; sa disparition ne prouve pas que tous les enregistrements liés sont nettoyés. La table ACL peut masquer les lignes dont le sujet n’existe plus. Si une requête échoue ou si les enregistrements diffèrent, arrêtez, relevez les identités/erreurs sans secrets et [signalez l’incohérence](/docs/xoa-hl/troubleshooting/) avant de réessayer ou de supprimer davantage d’objets.

Les groupes synchronisés par un fournisseur sont hors de cet exercice. Leurs contrôles locaux de nom/membres sont limités ; n’utilisez pas **Synchronize LDAP groups** et ne détachez pas un fournisseur d’authentification pour contourner ces restrictions. Les groupes imbriqués, le renommage, les ensembles de ressources, les quotas, la synchronisation d’annuaire et chaque opération déléguée restent à valider séparément.

## Sources

Version XO 5 `e281c536` : [interface des utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [interface ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [niveau par défaut du build](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [rôles et accès global administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs) et [héritage des permissions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js). Build du paquet : [script xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).

[interface des groupes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/groups/index.js) / [API des groupes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/group.mjs) / [appartenance et suppression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs) / [ACL combinées utilisateur/groupe](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs) / [sélecteur des sujets](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
