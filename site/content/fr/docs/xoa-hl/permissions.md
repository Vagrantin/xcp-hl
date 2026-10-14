---
title: Gérer les utilisateurs et les droits
description: Créer un utilisateur normal et vérifier un droit Viewer sur une seule VM jetable.
weight: 26
translationKey: xoa-manual-permissions
translationStatus: draft
sourceRevision: sha256:fe06b8f3cf1eaac25412e59f05d041adf8d95c81d32b5e96e0ba266a2f6b3e1e
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Utilisez une session administrateur existante dans l’**appliance XOA-HL**, une VM jetable et une session de navigateur distincte pour un nouvel utilisateur de test. Gardez la session administrateur disponible pendant tout l’exercice. Ne modifiez pas le compte du dernier administrateur ni vos propres droits pendant le test.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les sources montrent l’écran ACL activé par le niveau open source par défaut du build ; les tests de l’interface installée, des autorisations/refus et de la révocation restent à faire. Ce n’est pas une exigence d’abonnement Vates.
{{< /callout >}}

## 1. Distinguer compte et rôle sur un objet

**Settings → Users** (`/#/settings/users`) attribue une permission globale au compte. **User** est un compte normal ; **Admin** contourne les vérifications ACL des objets. Un droit **Admin** sur un objet est différent : il s’applique à l’objet choisi et à sa portée d’autorisation.

| Rôle ACL sur un objet | Opérations accordées |
| --- | --- |
| Viewer | Consulter |
| Operator | Consulter et opérer |
| Admin | Consulter, opérer et administrer |

Commencez par **Viewer** sur une seule VM de test. Un droit sur un hôte, pool ou groupe peut ouvrir un accès plus large. Les permissions s’additionnent : retirer une ACL ne révoque pas un accès encore accordé par un groupe, un autre objet ou un parent. Ce pilote n’utilise pas de règle de refus.

## 2. Créer une identité de test normale

Dans **Settings → Users**, créez un utilisateur de test distinct avec un e-mail/identifiant et un mot de passe unique. Choisissez **User**, pas l’**Admin** global. Vérifiez la permission affichée. N’utilisez pas des identifiants de production et ne mettez pas le mot de passe dans les preuves.

Connectez cet utilisateur dans la session de navigateur distincte et notez sa visibilité initiale avant l’ajout d’une ACL. Vérifiez qu’il s’agit bien de l’identité de test, et non d’une session administrateur réutilisée. Gardez la session administrateur d’origine pour corriger ou retirer le droit de test.

## 3. Accorder Viewer sur une VM

Comme administrateur, ouvrez **Settings → ACLs** (`/#/settings/acls`). Choisissez uniquement l’utilisateur de test comme sujet, uniquement la VM jetable comme objet et **Viewer** comme rôle, puis ajoutez la règle. Vérifiez le sujet, l’objet et le rôle de la ligne créée. Ne choisissez pas tous les objets ni le pool entier pour cet exercice.

Le formulaire accepte plusieurs sujets et objets, créant une règle pour chaque combinaison. Les filtres d’objets/tags sélectionnent des objets actuels ; cet exercice ne définit pas une politique pour les objets futurs. Confirmez les identités plutôt que de vous fier à des noms proches.

## 4. Vérifier visibilité et opérations restreintes

Actualisez la session de l’utilisateur normal ou reconnectez-le. Vérifiez que la VM attendue est visible et que ses informations de base sont consultables. Vérifiez que démarrage/arrêt et administration sont indisponibles ; si une opération peut être demandée, elle doit être refusée sans modifier la VM. Utilisez uniquement la VM jetable pour ce test négatif. Un bouton masqué ne constitue pas une validation complète de l’autorisation côté serveur.

Si une opération réussit contre toute attente, arrêtez l’exercice. Comme administrateur, examinez la permission globale, les groupes et les autres droits sur la VM, l’hôte ou le pool. N’élargissez pas les droits pour résoudre une erreur inexpliquée. Si l’écran ACL manque dans la version installée, notez les versions et l’erreur et [signalez le problème](/docs/xoa-hl/troubleshooting/) ; ne supposez pas qu’un niveau payant d’une autre édition s’applique.

## 5. Révoquer et vérifier à nouveau

Comme administrateur, retirez l’ACL de test exacte. Actualisez ou reconnectez l’utilisateur de test et vérifiez la disparition de l’accès à la VM. S’il reste, examinez les autres droits directs, de groupes et hérités ; retirer une ligne ne révoque pas tous les droits. Vérifiez aussi que l’administrateur conservé peut toujours se connecter et gérer les objets prévus.

Notez le type de compte, la portée et les résultats attendus/réels sans identifiants secrets. Supprimez l’identité de test seulement après la fin. Ce pilote ne valide pas chaque opération déléguée, les ensembles de ressources, l’authentification externe, les tâches de sauvegarde déléguées ou la portée des jetons API. Consultez [la gestion des hôtes/pools](/docs/xoa-hl/hosts-pools/) et [l’export de configuration](/docs/xoa-hl/configuration-backup/) avant des changements plus larges.

[Protéger la connexion d’un compte local par des codes à usage unique (OTP)](/docs/xoa-hl/sign-in-otp/).

## Sources

Version XO 5 `e281c536` : [interface des utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [interface ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [niveau par défaut du build](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [rôles et accès global administrateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs) et [héritage des permissions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js). Build du paquet : [script xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
