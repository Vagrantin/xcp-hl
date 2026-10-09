---
title: Se connecter, ajouter un hôte et choisir sa langue
description: Configurer votre compte XOA-HL, connecter l’hyperviseur et choisir la langue de l’interface.
weight: 10
translationKey: xoa-manual-first-login
translationStatus: draft
sourceRevision: sha256:0510b44d9ff31a46a35760be93a081503f05a2ab39b34882e6165c4c94744389
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

À la fin de ce guide, vous disposerez d’un compte XOA-HL accessible, d’un hôte connecté et d’une interface dans la langue de votre choix.

{{< callout type="info" >}}
Procédure en prévisualisation : vérifiée dans les sources de l’image `xoa-image-20261009-5f33c81` et de XO 5.113.2. L’essai complet sur une appliance de test reste à faire. Les anciennes images ou les mises à jour ultérieures peuvent différer. Cette traduction est un brouillon en attente de relecture.
{{< /callout >}}

## Avant de commencer

- [Déployez XOA-HL depuis XO Lite](/docs/start/#start-deploy-xoa). Notez le tag de l’image et l’adresse de l’appliance.
- Conservez l’identifiant et le mot de passe administrateur XO saisis dans le formulaire de déploiement. Il vous faut aussi l’adresse de gestion de l’hôte et son mot de passe `root`.
- Utilisez un navigateur sur un réseau de gestion de confiance. Ce tutoriel utilise un compte administrateur XOA-HL ; les accès délégués ne sont pas couverts.

Toutes les étapes ci-dessous s’effectuent dans le **navigateur**. Aucune commande sur l’hôte ou dans l’appliance n’est nécessaire.

| Adresse ou compte | Usage |
| --- | --- |
| Adresse de gestion de l’hôte | XO Lite et connexion du serveur dans XOA-HL |
| Adresse de l’appliance XOA-HL | Interface web Xen Orchestra |
| Compte administrateur XO | Connexion à Xen Orchestra |
| Compte `root` de l’hôte | Autoriser Xen Orchestra à gérer l’hyperviseur |
| Compte système `xo` de l’appliance | Accès SSH, distinct du compte web |

## 1. Ouvrir l’appliance et se connecter

1. Ouvrez `https://<appliance-address>` en remplaçant le paramètre par l’adresse attribuée au déploiement. Utilisez l’adresse de l’appliance, pas celle de l’hôte.
2. Si le navigateur signale un certificat autosigné, vérifiez que l’adresse appartient à votre appliance avant de l’accepter. Un changement de certificat sur une installation existante doit être examiné.
3. Attendez la fin de la configuration au premier démarrage, puis connectez-vous avec les **identifiants administrateur XO du formulaire de déploiement**. N’utilisez ni le compte `root` de l’hôte ni le compte SSH de l’appliance.

**Vérification :** l’interface Xen Orchestra remplace l’écran de connexion. Un inventaire vide est normal tant qu’aucun hôte n’est connecté.

{{< callout type="warning" >}}
Pour cette image, un échec de configuration des identifiants peut laisser le compte web initial `admin@admin.net` avec le mot de passe `admin`. Si le compte configuré ne fonctionne pas sur une appliance neuve, essayez ce compte de secours uniquement sur votre réseau de gestion de confiance. S’il fonctionne, changez immédiatement son mot de passe à l’étape suivante. Si aucun compte ne fonctionne, cessez les tentatives répétées et consultez le dépannage ci-dessous.
{{< /callout >}}

## 2. Définir un mot de passe à conserver

1. Sélectionnez l’**icône utilisateur** dans la navigation pour ouvrir **Utilisateur** (`/#/user`).
2. Dans la section du mot de passe, saisissez le mot de passe actuel, un nouveau mot de passe unique et sa confirmation. Sélectionnez **OK**.
3. Conservez le nouveau mot de passe, déconnectez-vous et vérifiez que vous pouvez vous reconnecter avec le même identifiant web et le nouveau mot de passe.

**Vérification :** une nouvelle connexion réussit. Cette opération change le mot de passe du compte web, pas celui de `root` sur l’hôte ni celui du compte SSH de l’appliance.

## 3. Choisir la langue de l’interface

1. Ouvrez l’**icône utilisateur → Utilisateur → Langue**.
2. Sélectionnez **English**, **Français** ou **日本語**. Vérifiez que les libellés changent.

Le sélecteur de langue de la documentation agit indépendamment sur ce site. Changer l’un ne change pas l’autre. Certains libellés de l’appliance peuvent rester en anglais ; la route `/#/user` identifie le même écran dans toutes les langues.

## 4. Connecter l’hôte

1. Ouvrez **Paramètres → Serveurs** (`/#/settings/servers`). Si le serveur souhaité est déjà présent et connecté, vérifiez son inventaire au lieu de l’ajouter deux fois.
2. Dans le formulaire de connexion, saisissez un libellé explicite, l’**adresse IP de gestion ou le nom d’hôte de l’hyperviseur**, l’utilisateur `root` et le mot de passe défini à l’installation. Ne saisissez pas l’adresse de l’appliance.
3. Sélectionnez **Connecter**. Si la connexion signale un certificat autosigné, vérifiez d’abord l’identité de l’hôte, puis acceptez l’exception pour ce serveur si elle est justifiée.
4. Vérifiez l’absence d’indicateur d’erreur sur la ligne de connexion. Ouvrez l’inventaire et confirmez la présence du pool, de l’hôte et des SR attendus. **Enabled** indique seulement que la connexion est activée, pas qu’elle a réussi.

**Vérification :** l’hôte et son stockage apparaissent sans erreur de connexion. Vous pouvez maintenant [créer votre première VM](/docs/xoa-hl/create-vm/).

## 5. Noter les versions installées

Ouvrez **À propos** (`/#/about`) avec un compte administrateur et notez la **version XOA-HL** et la **version de la VM XOA-HL**. Conservez-les avec le tag de l’image déployée. La version de la VM décrit la construction de l’image ; des mises à jour de paquets peuvent modifier ensuite la version de l’application.

La [matrice des versions](/docs/reference/release-matrix/) recense les versions enregistrées. Elle indique les composants livrés, pas les résultats de tests de l’appliance.

## En cas de problème

| Symptôme | Vérification et suite |
| --- | --- |
| La page de l’appliance ne s’ouvre pas | Vérifiez dans XO Lite que la VM de l’appliance fonctionne, puis son adresse, son réseau, sa passerelle et l’accès depuis le navigateur. Ne redéployez pas par-dessus une VM fonctionnelle. |
| Les identifiants du déploiement échouent | Attendez le premier démarrage, vérifiez les identifiants web, puis essayez le compte de secours décrit plus haut. Si la console de l’appliance ou un compte SSH autorisé est accessible, examinez `/var/log/xoa-first-boot.log` ; retirez les données privées avant tout partage. |
| L’authentification à l’hôte échoue | Vérifiez l’adresse de l’hôte et son mot de passe `root`. Le mot de passe administrateur web est distinct. |
| Le serveur signale une erreur de certificat | Vérifiez l’identité de l’hôte avant d’autoriser son certificat autosigné ; n’acceptez pas un changement inexpliqué. |
| Le serveur est activé, mais l’inventaire est vide | Lisez l’erreur de connexion, vérifiez l’accès de l’appliance à l’hôte et son adresse de gestion. L’accès depuis le navigateur ne prouve pas l’accès depuis l’appliance. |

## Étape suivante et sources

[Créez et installez votre première VM](/docs/xoa-hl/create-vm/), ou consultez le [guide de mise à jour de l’appliance et de l’hôte](/docs/guides/updates/).

Sources examinées : [version de l’image](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261009-5f33c81) ; [configuration des identifiants à build-xoa-hl@2103968](https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-credentials.sh) ; [écran utilisateur à XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js) ; [écran des serveurs au même commit](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js) ; [patch À propos à xoa-hl@5f33c81](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
