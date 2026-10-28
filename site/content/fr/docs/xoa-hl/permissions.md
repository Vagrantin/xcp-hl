---
title: "Gérer les utilisateurs et les droits"
linkTitle: "Utilisateurs et droits"
description: "Créez des utilisateurs et des groupes, donnez accès à une VM, déléguez des ressources et testez une connexion LDAP ou SAML."
weight: 70
translationKey: xoa-manual-permissions
translationStatus: draft
sourceRevision: sha256:f565451a1844a1556c044e9aee08213bbb2c4d048289c39c26260b5d6676aa9d
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Créez un utilisateur de test, donnez-lui accès à une VM, puis essayez un groupe, un ensemble de ressources délégué et une connexion externe (LDAP ou SAML). Vous travaillez en administrateur dans l’**appliance XOA-HL**, et vous connectez l’utilisateur de test dans une deuxième session de navigateur, distincte. Utilisez une VM de test jetable. Gardez votre session administrateur ouverte du début à la fin. Ne modifiez jamais le dernier compte administrateur, ni vos propres droits, pendant le test. Pour ajouter des codes à usage unique à la connexion d’un compte local, voir [Protéger la connexion par un code à usage unique](/docs/xoa-hl/sign-in-otp/).

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Les permissions contrôlent ce qu’un utilisateur peut faire, pas ce qu’il peut lire : dans cette version, tout compte connecté peut lire tout l’inventaire par l’API. Avec le plan open source par défaut de ce build, le code active les écrans des droits et du libre-service : aucun abonnement Vates n’est nécessaire.
{{< /callout >}}

**Observations D3 (2026-10-28) :** un compte normal de test et un invité jetable sur XOA-HL `v5.113.2_e281c536-ce47` (`ca44911`), sur un seul hôte XCP-HL v8.3-ce44 imbriqué. Dans l’interface web, le compte sans droits voyait « There are no VMs! ». Les pages Utilisateurs et ACL des paramètres renvoyaient « Page not found ». Les demandes de démarrage et de modification avec Viewer étaient refusées avec « not enough permissions », sans changer la VM. Avec Operator, le démarrage fonctionnait, mais le renommage et la suppression étaient refusés. Le démarrage restait refusé après le retrait du droit Viewer. Ce sont les restrictions appliquées par l’interface web et ses demandes d’action dans le [compte rendu D3](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6459388202). Les droits de groupe en fonctionnement n’ont pas été testés ; les procédures de groupe ci-dessous restent fondées sur le code.

La liste d’objets de l’API n’est pas limitée aux objets autorisés ([#309](https://github.com/Vagrantin/xcp-hl/issues/309)). Ne donnez donc pas d’accès API à un compte qui ne doit pas voir l’inventaire.

## Connaître les deux types de rôles {#roles}

**Paramètres → Utilisateurs** (`/#/settings/users`) fixe la permission globale de chaque compte :

- **Utilisateur** est un compte normal.
- **Administrateur** est un administrateur. Il contourne toutes les règles des objets.

Une règle d’accès (ACL) donne à un utilisateur ou à un groupe un rôle sur un objet. Le rôle d’objet **Admin** n’est pas l’**Administrateur** global : il s’applique uniquement à l’objet choisi et à sa portée.

| Rôle d’objet | Ce qu’il permet |
| --- | --- |
| Viewer | Consulter |
| Operator | Consulter et opérer |
| Admin | Consulter, opérer et administrer |

Commencez par **Viewer** sur une seule VM de test. Une règle sur un hôte ou un pool peut donner accès à plus d’objets qu’une règle sur une seule VM. Une règle pour un groupe s’applique à tous ses membres. Les permissions s’additionnent, et aucune règle ne refuse l’accès. Retirer une règle ne retire pas un accès qui vient encore d’un autre groupe, d’un autre objet ou d’un objet parent.

## Donner à un utilisateur de test l’accès à une VM {#vm-access}

Ces quatre étapes forment un seul test : créer un utilisateur normal, lui donner **Viewer** sur une VM jetable, vérifier ce qu’il peut faire, puis retirer l’accès.

### Créer un utilisateur de test

1. Dans **Paramètres → Utilisateurs**, créez un utilisateur de test distinct, avec son propre e-mail ou identifiant et un mot de passe unique.
2. Choisissez **Utilisateur**, pas **Administrateur**. Vérifiez la permission affichée pour ce compte.
3. Dans la deuxième session de navigateur, connectez-vous avec cet utilisateur. Notez ce qu’il voit avant d’ajouter une règle.

Vérifiez que cette session est bien celle de l’utilisateur de test, et non une connexion administrateur réutilisée. N’utilisez pas de vrais identifiants, et n’écrivez jamais de mot de passe dans vos notes. Gardez l’utilisateur de test : le test de groupe ci-dessous le réutilise.

### Accorder Viewer sur une VM {#grant-viewer}

1. En tant qu’administrateur, ouvrez **Paramètres → Droits** (`/#/settings/acls`).
2. Choisissez uniquement l’utilisateur de test comme sujet, uniquement la VM jetable comme objet et **Viewer** comme rôle. Sélectionnez **Créer**.
3. Vérifiez le sujet, l’objet et le rôle de la nouvelle ligne.

Ne choisissez pas tous les objets ni le pool entier. Le formulaire accepte plusieurs sujets et objets, et crée une règle pour chaque paire. Vérifiez les identités plutôt que des noms d’affichage proches. Les filtres d’objets et de tags sélectionnent les objets actuels ; ils ne créent aucune règle pour les objets futurs.

### Vérifier ce que l’utilisateur peut faire

1. Dans la session de l’utilisateur de test, actualisez la page ou reconnectez-vous.
2. Vérifiez que la VM est visible et que ses informations de base sont consultables.
3. Vérifiez que le démarrage, l’arrêt et l’administration ne sont pas disponibles. Si une action peut encore être demandée, elle doit être refusée et la VM ne doit pas changer.

Faites ce test uniquement sur la VM jetable. Un bouton masqué ne prouve pas à lui seul que le serveur refuse l’action.

Si une action réussit contre toute attente, arrêtez-vous. En tant qu’administrateur, vérifiez la permission globale du compte, ses groupes et toute autre règle sur la VM, son hôte ou son pool. N’élargissez pas les droits pour corriger une erreur d’accès inexpliquée. Si la page des droits est absente, notez les versions et l’erreur et [signalez-le](/docs/xoa-hl/troubleshooting/). Ne supposez pas qu’un plan payant d’une autre édition est nécessaire.

### Révoquer et vérifier à nouveau

1. En tant qu’administrateur, retirez la règle de test exacte.
2. Dans la session de l’utilisateur de test, actualisez ou reconnectez-vous. Vérifiez que l’accès à la VM a disparu.
3. Vérifiez que votre administrateur peut toujours se connecter et gérer les objets prévus.

Si l’accès reste, cherchez d’autres règles directes, de groupe ou héritées : retirer une ligne ne retire pas tous les droits.

**Vérification :** l’utilisateur pouvait consulter la VM sans la modifier, et a perdu l’accès après le retrait de la règle. Notez le type de compte, la portée de la règle et les résultats attendus et réels, sans identifiants.

Gardez l’utilisateur de test jusqu’à la fin de tous les tests de cette page. La délégation des tâches de sauvegarde et la portée des jetons API ne sont pas traitées ici. Avant des changements plus larges, voir [Hôtes et pools](/docs/xoa-hl/hosts-pools/) et [exportez votre configuration](/docs/xoa-hl/configuration-backup/).

## Accorder l’accès avec des groupes locaux {#group-access}

Un groupe applique ses règles d’objets à tous ses membres. Ajouter un utilisateur à un groupe ne change pas sa permission globale.

**Avant de commencer**

- Terminez [Donner à un utilisateur de test l’accès à une VM](#vm-access). Sa règle directe doit être retirée, et l’utilisateur ne doit recevoir aucun accès à la VM par un autre groupe ou un objet parent.
- Utilisez le même utilisateur de test normal et la même VM jetable.
- Gardez un second compte de test normal hors du groupe, pour comparer.
- Gardez la session administrateur ouverte.

### Créer le groupe et sa règle

1. Ouvrez **Paramètres → Groupes** (`/#/settings/groups`). Saisissez un nom distinct, comme `lab-vm-viewers`, dans **Nouveau nom de groupe** et sélectionnez **Créer**.
2. Vérifiez que le nouveau groupe n’a aucun utilisateur. Si le nom existe déjà, choisissez-en un autre : ne réutilisez pas un groupe inconnu, avec ses droits.
3. Dans **Paramètres → Droits**, choisissez uniquement ce groupe comme sujet, uniquement la VM de test comme objet et **Viewer** comme rôle. Sélectionnez **Créer**, puis vérifiez le groupe, la VM et le rôle exacts de la nouvelle ligne.
4. Vérifiez que les deux comptes normaux voient toujours la même chose qu’avant. Un groupe vide ne donne aucun accès.

### Ajouter l’utilisateur et vérifier l’accès

1. Dans **Groupes**, dans la colonne **Ajouter un utilisateur** de ce groupe, choisissez uniquement l’utilisateur de test. La modification est envoyée tout de suite ; il n’y a pas de bouton d’enregistrement séparé.
2. Dépliez le compteur de la colonne **Utilisateur** avec l’icône plus et vérifiez l’identifiant.
3. Dans **Paramètres → Utilisateurs**, vérifiez que les groupes de l’utilisateur incluent ce groupe, et que le compte est toujours **Utilisateur**. Après une erreur, actualisez les deux vues : les deux enregistrements d’appartenance sont écrits séparément, donc une seule liste correcte ne suffit pas.
4. Dans la session du membre, actualisez ou reconnectez-vous. Vérifiez que l’utilisateur peut consulter la VM, et que le démarrage, l’arrêt et l’administration sont indisponibles ou refusés sans modifier la VM.
5. Vérifiez que le second compte n’a toujours aucun accès à la VM.

Si les résultats diffèrent, arrêtez-vous. Vérifiez l’identité réelle, la permission globale, les groupes et toutes les règles directes et parentes. N’ajoutez pas de droits plus larges pour faire réussir le test.

### Retirer le membre

1. Dans **Groupes**, dépliez la liste des membres et sélectionnez l’icône de retrait à côté de l’identifiant de test exact. Le retrait est envoyé tout de suite, sans confirmation.
2. Vérifiez que l’identifiant a quitté le groupe, et que le groupe a disparu du détail de l’utilisateur.
3. Dans la session de l’ancien membre, actualisez ou reconnectez-vous. Vérifiez que l’accès à la VM donné par le groupe a disparu.

La règle du groupe reste en place : les autres membres éventuels gardent son accès.

### Vérifier que les droits s’additionnent

1. Remettez l’utilisateur dans le groupe et vérifiez que l’accès Viewer revient.
2. Ajoutez une règle **Viewer** directe et séparée pour cet utilisateur sur la même VM.
3. Retirez uniquement la règle du groupe sur la VM. L’utilisateur peut encore consulter la VM grâce à la règle directe.
4. Retirez la règle directe et vérifiez de nouveau. Sans autre droit, l’accès disparaît, même si l’utilisateur reste membre du groupe.

L’absence d’une règle de groupe ne refuse rien, et un **Administrateur** global contourne toutes les règles des objets.

### Nettoyer après le test de groupe

1. Retirez les règles de test tant que leurs utilisateurs et groupes existent encore.
2. Retirez les appartenances de test, puis vérifiez les résultats des deux comptes normaux.
3. Vérifiez la ligne et le nom du groupe de test vide. Sélectionnez **Supprimer le groupe** sur cette ligne et confirmez. La confirmation ne nomme pas le groupe : identifiez-le avant de l’ouvrir.
4. Actualisez les vues Groupes, Droits et Utilisateurs. Gardez l’administrateur indépendant.

XO retire en arrière-plan les règles et appartenances d’un groupe supprimé. La disparition du groupe ne prouve pas que tous les enregistrements liés ont disparu. Le tableau des droits peut masquer les lignes dont le sujet n’existe plus. Si une requête a échoué ou si les enregistrements divergent, arrêtez-vous. Notez les identités et les erreurs sans secrets, et [signalez l’incohérence](/docs/xoa-hl/troubleshooting/) avant de réessayer ou de supprimer autre chose.

Les groupes synchronisés depuis un fournisseur d’authentification ne sont pas traités ici, pas plus que les groupes imbriqués, le renommage et la délégation plus large. Leurs contrôles locaux de nom et de membres sont limités. N’utilisez pas **Synchronize LDAP groups**, et ne détachez pas un fournisseur d’authentification, pour contourner ces limites.

## Tester le quota d’un ensemble de ressources délégué {#resource-set-delegation}

Un ensemble de ressources permet à un utilisateur normal de créer des VM à partir de modèles, SR et réseaux choisis, dans des limites de CPU, de RAM et de disque (quotas). Ici, vous testez un ensemble, pour un utilisateur, sur un pool jetable.

**Avant de commencer**

- Utilisez uniquement un pool jetable et un utilisateur de test normal dédié, sans règle large sur ce pool.
- Gardez une session administrateur indépendante, et une sauvegarde indépendante de tout ce que vous voulez conserver.
- N’ajoutez pas d’utilisateur de production, et ne partagez pas le stockage ni les réseaux de production.
- Utilisez deux sessions de navigateur : la session administrateur XOA-HL, et une session séparée pour l’utilisateur normal.

### Créer l’ensemble de ressources

1. En tant qu’administrateur, choisissez un pool jetable, un modèle connu et arrêté, un SR de test accessible en écriture avec assez d’espace libre, et un réseau de laboratoire isolé que les hôtes éligibles peuvent atteindre.
2. Notez leurs UUID exacts, ainsi que les valeurs CPU, RAM et disque par défaut du modèle. Si les disques ou le réseau du modèle ne peuvent pas être placés sur ces ressources, arrêtez-vous.
3. Vérifiez que l’utilisateur de test est **Utilisateur**, pas **Administrateur** global, et qu’il ne peut pas encore créer de VM dans ce pool.
4. Ouvrez **Libre service → Jeu de ressources** (`/#/self`) et sélectionnez **Nouvelle**. Donnez à l’ensemble un nom de laboratoire unique. Choisissez uniquement cet utilisateur et ce pool, puis uniquement les **Templates**, **SRs** et **Networks** retenus.
5. Vérifiez la liste des hôtes. L’éditeur affiche les hôtes éligibles et exclus, selon l’accès au SR et au réseau. Au moins un hôte prévu doit être éligible.
6. Saisissez des valeurs finies dans **CPUs maximum**, **RAM maximum (GiB)** et **Espace disque maximum**. Elles doivent permettre une petite VM issue du modèle, mais rester sous la demande hors limite que vous essaierez ensuite.
7. Laissez **Share VMs by default** désactivé, n’ajoutez pas de plage d’IP, et sélectionnez **Enregistrer**. L’éditeur crée l’ensemble, puis le modifie : après une erreur d’enregistrement, actualisez la liste et cherchez un ensemble vide ou partiel avant de réessayer.
8. Rechargez l’ensemble. Vérifiez son ID, son utilisateur, ses modèles, SR, réseaux, hôtes et les trois limites. Notez la consommation actuelle, normalement nulle.

Si la page affiche une invitation à changer de plan, ou si l’ensemble est absent, notez la version et arrêtez-vous. Ne supposez pas qu’un plan Vates est nécessaire, et ne contournez pas l’interface par un appel API non vérifié.

### Vérifier le quota

1. Dans la session de l’utilisateur normal, ouvrez **Nouvelle VM** (`/#/vms/new`) et choisissez l’ensemble de ressources exact.
2. Demandez une VM qui dépasse la limite de CPU. Gardez le modèle, le SR, le réseau, la RAM et le disque valides. Le serveur doit la refuser, sans nouvelle VM ni disque inattendu.
3. En tant qu’administrateur, vérifiez l’inventaire et la consommation du quota. Un contrôle masqué ne prouve pas à lui seul que la limite est appliquée. Si une VM ou un disque partiel existe, arrêtez-vous et faites-en la liste avant tout nettoyage.
4. En tant qu’utilisateur normal, demandez une VM qui respecte toutes les limites, avec uniquement les objets choisis. Laissez-la arrêtée. Retirez ou déconnectez les VIF héritées avant tout démarrage isolé.
5. Vérifiez l’UUID de la nouvelle VM, le SR de son disque, son réseau, son ensemble de ressources, et les valeurs **Used** et **Total** du quota.
6. Vérifiez que l’utilisateur normal peut voir et administrer cette VM, et qu’un autre compte normal sans cet ensemble ne le peut pas.

Ne testez jamais la limite sur une VM de production. Par défaut, XO donne au créateur de la VM le rôle d’objet **Admin** sur celle-ci. Activer **Share VMs by default** étend ce rôle aux utilisateurs de l’ensemble. L’utilisateur de test n’a besoin d’aucune règle d’administration sur tout le pool.

**Vérification :** la demande hors limite a été refusée sans laisser de traces, et la VM dans les limites apparaît dans la consommation du quota.

### Retirer l’utilisateur de l’ensemble

1. En tant qu’administrateur, retirez l’utilisateur de test de l’ensemble. Actualisez la session de l’utilisateur normal.
2. Vérifiez que l’utilisateur ne peut plus choisir l’ensemble, ni créer d’autre VM avec lui.
3. Vérifiez séparément les règles directes ou héritées restantes sur la VM existante. Retirer un utilisateur d’un ensemble retire les règles de VM liées à l’ensemble, mais un autre droit peut conserver l’accès.

Si l’accès ou la consommation ne correspond pas, arrêtez-vous et notez les ID de l’ensemble et de la VM et l’erreur, sans secrets. N’utilisez pas **Recalculer les limites** comme une réparation que vous ne savez pas expliquer.

### Nettoyer après le test de l’ensemble

1. Arrêtez la nouvelle VM et confirmez ses ID exacts de VM et de VDI. Retirez ses VIF.
2. Supprimez **uniquement** cette VM jetable. Vérifiez que ses disques et snapshots ont été traités comme prévu.
3. Actualisez la consommation du quota et le nombre de VM de l’ensemble. Vérifiez qu’aucune VM ne reste dans l’ensemble.
4. Sélectionnez **Supprimer le jeu de ressources** sur l’ensemble exact. Supprimer un ensemble détache seulement ses VM ; il ne les supprime pas.
5. Revérifiez l’utilisateur normal, l’administrateur indépendant et l’inventaire du pool.

Notez les ID attendus et réels, les refus, les chiffres du quota et le nettoyage, sans identifiants. Les groupes comme sujets, les plages d’IP, le partage par défaut, plusieurs VM à la fois, le nettoyage après une création échouée et la délégation en production ne sont pas traités ici.

## Tester une connexion LDAP externe {#ldap-sign-in}

Une connexion LDAP peut créer un compte XO, ou se lier à un compte existant. Utilisez un annuaire jetable et une identité de test dédiée, non administratrice.

{{< callout type="warning" >}}
Les valeurs par défaut sont `createUserOnFirstSignin = true` et `mergeProvidersUsers = true`. Un nom d’utilisateur de l’annuaire identique à un nom XO local peut donc se lier à ce compte et effacer son mot de passe local. Utilisez un nom de test qui ne correspond à **aucun** compte XO existant.
{{< /callout >}}

**Avant de commencer**

- Gardez une session administrateur locale indépendante et une voie de récupération.
- En tant qu’administrateur, notez les versions de l’image, du paquet et de XO, ainsi que les réglages d’authentification effectifs. Conservez un [export de configuration](/docs/xoa-hl/configuration-backup/) privé.
- Dans **Paramètres → Greffons** (`/#/settings/plugins`), vérifiez que `auth-ldap` figure dans la liste avec une version. Notez ses états de configuration, de chargement et de chargement automatique, sans secrets. S’il est absent, ou s’il sert déjà de vrais utilisateurs, arrêtez-vous.
- Avec le responsable de l’annuaire, préparez un point d’accès LDAPS ou StartTLS isolé avec une autorité de certification de confiance, un attribut d’ID utilisateur unique et stable, une base et un filtre d’utilisateurs restreints, et si besoin une identité de recherche dédiée.
- Ne modifiez ni le dernier administrateur local ni un fournisseur existant pour faire fonctionner ce test.

### Configurer et charger le greffon

1. Pendant une fenêtre de laboratoire approuvée, saisissez dans le formulaire du greffon uniquement les valeurs du responsable de l’annuaire : URI, chemin de l’autorité de certification, vérification des certificats activée, choix StartTLS, base, filtre d’utilisateurs, attribut d’ID et identifiants de recherche.
2. Laissez **Synchronize groups** non configuré. Cette option peut importer des appartenances et changer qui accède à quoi.
3. Vérifiez séparément l’identité TLS et l’accessibilité. Ne désactivez jamais la vérification des certificats pour masquer une erreur.
4. Enregistrez la configuration. Chargez ensuite le greffon et relisez ses états de chargement et de chargement automatique. Le chargement depuis cette page active aussi le chargement automatique.

Enregistrer seul ne prouve pas que la connexion fonctionne. Gardez les secrets privés : hors des captures, des journaux et des rapports de problème.

### Se connecter une fois et vérifier le compte

N’utilisez **pas** le bouton **Test** comme une simple vérification de connexion. Il exécute le vrai processus de connexion, qui peut créer un compte XO et, s’il est configuré, synchroniser des groupes.

1. Dans une nouvelle session de navigateur séparée, connectez-vous une seule fois avec l’identité de test unique de l’annuaire.
2. Depuis la session administrateur, vérifiez l’ID du nouvel utilisateur XO, son fournisseur, sa permission globale (**Utilisateur**), ses groupes et ce qu’il voit. Une connexion réussie ne donne à elle seule aucun accès aux objets.
3. Donnez à ce compte **Viewer** sur une seule VM jetable, comme dans [Accorder Viewer sur une VM](#grant-viewer). Dans sa session, vérifiez qu’il peut consulter la VM, et que les actions d’exploitation et d’administration sont absentes ou refusées sans aucun changement.
4. Retirez cette règle exacte. Dans une session actualisée, vérifiez que l’accès a disparu.
5. Essayez un mauvais mot de passe d’annuaire, sans le divulguer. Vérifiez que l’administrateur local indépendant peut toujours se connecter.

Si un compte XO existant est lié, si un rôle administrateur ou un groupe inattendu apparaît, ou si le résultat du fournisseur ou du certificat est flou : arrêtez-vous, gardez des preuves expurgées et suivez le plan de récupération du responsable. Ne vous reconnectez pas et n’accordez pas plus de droits.

### Nettoyer après le test LDAP

1. Retirez uniquement les règles de test et les éventuelles appartenances de test. Déconnectez la session externe.
2. Déchargez `auth-ldap` et relisez ses états de chargement et de chargement automatique. L’administrateur local doit continuer à fonctionner.
3. Avant de supprimer le compte de test, identifiez exactement l’utilisateur, ses jetons et ses règles. Supprimer le compte et purger la configuration du greffon sont deux actions distinctes. Ne purgez jamais un fournisseur qui sert d’autres utilisateurs.

Si le chargement, la connexion ou le déchargement échoue, conservez les erreurs expurgées et les états réels de l’utilisateur et du fournisseur avant de réessayer. N’assouplissez jamais la vérification TLS et ne fusionnez pas de comptes pour contourner un échec. Notez le fournisseur, la version, la confiance TLS, la correspondance des identités, les ID d’utilisateur et de règles avant et après, les résultats autorisés et refusés, et la connexion locale conservée. La synchronisation des groupes, les pannes d’annuaire, la rotation des identifiants, le renommage des identités, les jetons, l’OTP et la bascule ne sont pas traités ici.

## Tester une connexion SAML externe {#saml-sign-in}

Il vous faut une application de fournisseur d’identité (IdP) isolée, une identité de test non administratrice au nom unique et un administrateur XO local indépendant. Le greffon prend le nom d’utilisateur XO dans l’attribut de profil indiqué par `usernameField`.

{{< callout type="warning" >}}
Avec les valeurs par défaut de `createUserOnFirstSignin` et `mergeProvidersUsers`, un nom d’utilisateur identique à celui d’un compte XO existant peut se lier à ce compte et effacer son mot de passe local. Ne testez jamais avec un nom d’utilisateur XO existant ni avec une application d’authentification unique (SSO) de production.
{{< /callout >}}

**Avant de commencer**

- Avec le responsable de l’IdP, notez les versions de l’image, du paquet, de XO et du greffon, les réglages d’authentification effectifs et l’adresse HTTPS publique. Conservez un [export de configuration](/docs/xoa-hl/configuration-backup/) privé.
- Vérifiez que `auth-saml` figure dans **Paramètres → Greffons** (`/#/settings/plugins`) et ne sert aucun vrai utilisateur.
- Convenez d’un attribut de profil stable et unique pour `usernameField`. Avant de charger le greffon, comparez sa valeur de test à **tous** les noms d’utilisateur XO.
- Gardez une session administrateur locale fonctionnelle et une voie de récupération séparée par la console.
- Si l’adresse publique, le proxy ou la correspondance des comptes n’est pas clair, arrêtez-vous.

### Enregistrer l’appliance auprès de l’IdP

1. Enregistrez uniquement ce fournisseur de service de laboratoire auprès de l’IdP. Son URL de retour doit correspondre à `https://<appliance-name>/signin/saml/callback`, accessible depuis l’extérieur. Vérifiez le nom DNS exact, la confiance du certificat et la redirection à travers un éventuel proxy.
2. Obtenez le **certificat de signature** de l’IdP, son point d’entrée et l’émetteur convenu par le canal privé du responsable. Ce certificat n’est pas le certificat HTTPS de l’appliance.
3. Exigez une réponse ou une assertion SAML signée, comme convenu avec le responsable de l’IdP. Les valeurs par défaut du greffon `wantAssertionsSigned` et `wantAuthnResponseSigned` sont toutes deux `false`, mais cela ne rend **pas** acceptables les messages non signés.

Revoyez ces options avec le responsable de l’IdP. N’affaiblissez jamais la vérification des signatures ou de TLS pour masquer une discordance.

### Configurer, charger et se connecter

1. Saisissez uniquement le certificat, le point d’entrée, l’émetteur et le champ du nom d’utilisateur du laboratoire, ainsi que les éventuelles options de retour ou de contrôle renforcé approuvées par le responsable.
2. Enregistrez la configuration. Chargez ensuite le greffon et relisez ses états de chargement et de chargement automatique. Enregistrer seul ne l’active pas ; le chargement depuis cette page active aussi le chargement automatique.
3. Dans une nouvelle session de navigateur séparée, lancez la connexion SAML depuis la page de connexion XO. Authentifiez-vous une seule fois avec l’identité de laboratoire attribuée.
4. Demandez au responsable de l’IdP de confirmer la réponse signée et l’attribut retenu, sans publier l’assertion.

Ne collez jamais de certificats, d’assertions, de données de profil ou de jetons de session dans des rapports publics.

### Vérifier le nouveau compte

1. Depuis la session administrateur, vérifiez l’ID du **nouvel** utilisateur XO, son fournisseur `saml`, sa permission globale (**Utilisateur**), ses groupes et ce qu’il voit.
2. Donnez-lui **Viewer** sur une seule VM jetable, comme dans [Accorder Viewer sur une VM](#grant-viewer). Vérifiez l’accès en lecture et le refus d’une opération.
3. Retirez cette règle exacte. Dans une session actualisée, vérifiez que l’accès a disparu.
4. Demandez au responsable de l’IdP de refuser une identité témoin non attribuée, dans une nouvelle session. Cela teste une nouvelle connexion, pas la révocation des jetons XO existants.
5. Vérifiez que l’administrateur local peut toujours se connecter.

Si un utilisateur existant est lié, si un rôle privilégié apparaît, si l’attribut manque, ou si le résultat de la signature ou du retour est flou : arrêtez-vous et ne gardez que des preuves expurgées. Quand le champ du nom d’utilisateur manque, le greffon journalise le profil complet : traitez les journaux d’échec comme sensibles.

### Nettoyer après le test SAML

1. Déconnectez la session de test SAML et retirez les règles de test.
2. Déchargez uniquement le greffon `auth-saml` isolé. Vérifiez ses états de chargement et de chargement automatique, ainsi que la connexion locale.
3. Avant de supprimer le compte, listez l’utilisateur de test exact et ses jetons. Se déconnecter, ou désactiver le fournisseur, ne prouve pas que les jetons XO existants sont invalides. Ne purgez jamais un fournisseur qui sert de vrais utilisateurs.

En cas d’échec, notez le retour et l’erreur expurgés, ainsi que les états réels de l’utilisateur, du fournisseur et des jetons, avant de réessayer. Notez l’adresse de retour, l’identité et l’expiration du certificat de l’IdP, la politique de signature, l’attribut utilisé, l’état du greffon, les ID d’utilisateur et de règles avant et après, les résultats et l’accès local conservé, sans secrets. Les pannes de l’IdP, la rotation des clés de signature, la dérive d’horloge, les changements d’attribut, la révocation des jetons et sessions, l’OTP et la fédération en production ne sont pas traités ici.

{{< details title="Sources" closed="true" >}}
- **Utilisateurs, droits et plan du build** : [interface des utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [interface des droits](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [plan par défaut du build](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [rôles et contournement par l’administrateur global](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [héritage des permissions entre objets](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js), [script de build xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Groupes** : [interface des groupes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/groups/index.js), [API des groupes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/group.mjs), [appartenance et suppression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [règles combinées des utilisateurs et des groupes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [sélecteur des sujets](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Ensembles de ressources** : [éditeur des ensembles et condition de plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/self/index.js), [API des ensembles de ressources](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/resource-set.mjs), [contraintes, quotas et suppression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/resource-sets.mjs), [création de VM et ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [choix de l’ensemble à la création de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **LDAP** : [schéma, TLS, test, enregistrement et synchronisation facultative des groupes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-ldap/src/index.js), [page des greffons : configuration, chargement et test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [enregistrement et collision des noms](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [valeurs par défaut de l’authentification](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [espaces de travail du build XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [contenu RPM](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **SAML** : [schéma, attribut du profil et enregistrement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-saml/src/index.js), [retour web, connexion et création des jetons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [page de chargement des greffons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [collision des comptes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [guide SAML de XO 5](https://docs.xen-orchestra.com/users-and-access/users#saml).
{{< /details >}}
