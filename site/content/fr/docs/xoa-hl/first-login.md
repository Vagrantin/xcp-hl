---
title: "Se connecter, ajouter un hôte et choisir la langue"
linkTitle: "Première connexion"
description: "Connectez-vous à XOA-HL, changez le mot de passe, choisissez la langue de l’interface et ajoutez votre hôte."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: draft
sourceRevision: sha256:90b1070b91657a68c53df68d8927605d523fbc946c6b8cf0e3a2fa30a113e037
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

À la fin de ce guide, vous pouvez vous connecter à XOA-HL, votre hôte est connecté et l’interface s’affiche dans votre langue.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; un essai complet sur une appliance de test reste à faire. Les images plus anciennes et les mises à jour ultérieures peuvent différer.
{{< /callout >}}

## Avant de commencer

- [Déployez XOA-HL depuis XO Lite](/docs/start/#start-deploy-xoa). Notez le tag de l’image et l’adresse de l’appliance.
- Gardez l’identifiant et le mot de passe administrateur XO saisis dans le formulaire de déploiement. Il vous faut aussi l’adresse de gestion de l’hôte et son mot de passe `root`.
- Utilisez un navigateur sur un réseau de gestion de confiance.

Toutes les étapes se font dans votre **navigateur**. Aucun shell n’est nécessaire sur l’hôte ou l’appliance.

| Adresse ou compte | À quoi il sert |
| --- | --- |
| Adresse de gestion de l’hôte | XO Lite, et connexion du serveur dans XOA-HL |
| Adresse de l’appliance XOA-HL | Interface web Xen Orchestra |
| Compte administrateur XO | Connexion à Xen Orchestra |
| Compte `root` de l’hôte | Autoriser Xen Orchestra à gérer l’hôte |
| Compte système `xo` de l’appliance | Accès SSH uniquement ; ce n’est pas le compte web |

## 1. Ouvrir l’appliance et se connecter

1. Ouvrez `https://<appliance-address>`. Utilisez l’adresse de l’appliance, pas celle de l’hôte.
2. Si le navigateur signale un certificat autosigné, vérifiez que l’adresse est bien celle de votre appliance avant de l’accepter. Si le certificat d’une installation existante change, cherchez-en d’abord la raison.
3. Attendez la fin du premier démarrage. Connectez-vous ensuite avec le **compte administrateur XO du formulaire de déploiement**. N’utilisez ni le compte `root` de l’hôte ni le compte SSH de l’appliance.

**Vérification :** l’interface Xen Orchestra s’ouvre. Un inventaire vide est normal tant qu’aucun hôte n’est connecté.

{{< callout type="warning" >}}
Avec cette image, si le premier démarrage n’arrive pas à définir vos identifiants, le compte web peut rester `admin@admin.net` avec le mot de passe `admin`. Si votre propre compte ne fonctionne pas sur une appliance neuve, essayez ce compte de secours, uniquement sur votre réseau de confiance. S’il fonctionne, changez immédiatement le mot de passe à l’étape 2. Si aucun compte ne fonctionne, arrêtez les tentatives et consultez le tableau de dépannage en fin de page.
{{< /callout >}}

## 2. Définir un mot de passe durable

1. Sélectionnez l’**icône utilisateur** dans le menu pour ouvrir **Utilisateur** (`/#/user`).
2. Dans la section du mot de passe, saisissez le mot de passe actuel, puis deux fois le nouveau. Choisissez un mot de passe unique. Sélectionnez **OK**.
3. Rangez le nouveau mot de passe en lieu sûr. Déconnectez-vous, puis reconnectez-vous avec le nouveau mot de passe.

**Vérification :** la connexion avec le nouveau mot de passe réussit. Seul le compte web change. Le mot de passe `root` de l’hôte et celui du compte SSH de l’appliance restent identiques.

## 3. Choisir la langue de l’interface

1. Ouvrez l’**icône utilisateur → Utilisateur → Langue**.
2. Sélectionnez **Français**. Les libellés changent aussitôt.

Ce réglage ne modifie que l’interface de XOA-HL. La documentation a son propre sélecteur de langue, en haut de cette page. Certains libellés de l’appliance ne sont pas encore traduits. L’adresse `/#/user` ouvre toujours cet écran.

## 4. Connecter l’hôte

1. Ouvrez **Paramètres → Serveurs** (`/#/settings/servers`). Si votre hôte est déjà présent et connecté, vérifiez son inventaire au lieu de l’ajouter une seconde fois.
2. Dans le formulaire, saisissez un libellé clair, l’**adresse IP de gestion ou le nom de l’hôte**, l’utilisateur `root` et le mot de passe défini à l’installation. Ne saisissez pas l’adresse de l’appliance.
3. Sélectionnez **Connecter**. Si un avertissement de certificat autosigné apparaît, vérifiez d’abord qu’il s’agit bien de votre hôte. Acceptez ensuite le certificat pour ce serveur.
4. Vérifiez l’absence d’indicateur d’erreur sur la ligne du serveur. Ouvrez ensuite l’inventaire et vérifiez que votre pool, votre hôte et vos dépôts de stockage (SR) apparaissent. **Enabled** signifie seulement que la connexion est activée, pas qu’elle fonctionne.

**Vérification :** votre hôte et son stockage apparaissent, sans erreur de connexion. Vous pouvez maintenant [créer votre première VM](/docs/xoa-hl/create-vm/).

## 5. Noter les versions installées

Ouvrez **À propos** (`/#/about`) avec un compte administrateur. Notez la **version XOA-HL** et la **version de la VM XOA-HL**, et conservez-les avec le tag de l’image. La version de la VM identifie la construction de l’image. Les mises à jour de paquets peuvent ensuite changer la version de l’application.

La [matrice des versions](/docs/reference/release-matrix/) liste le contenu de chaque version publiée. Elle ne contient pas de résultats de tests.

## En cas de problème

| Problème | À vérifier |
| --- | --- |
| La page de l’appliance ne s’ouvre pas | Dans XO Lite, vérifiez que la VM de l’appliance fonctionne. Vérifiez ensuite son adresse, son réseau, sa passerelle et l’accès depuis votre navigateur. Ne redéployez pas par-dessus une VM qui fonctionne. |
| Les identifiants du déploiement ne fonctionnent pas | Attendez la fin du premier démarrage et vérifiez que vous utilisez le compte web. Essayez ensuite le compte de secours décrit plus haut. Si vous avez accès à la console de l’appliance ou à une session SSH, lisez `/var/log/xoa-first-boot.log`. Retirez les données privées avant tout partage. |
| La connexion à l’hôte échoue | Vérifiez l’adresse de l’hôte et son mot de passe `root`. Le mot de passe administrateur web est un autre mot de passe. |
| Le serveur affiche une erreur de certificat | Vérifiez l’identité de l’hôte avant d’accepter son certificat autosigné. N’acceptez pas un changement que vous ne savez pas expliquer. |
| Le serveur est activé mais l’inventaire est vide | Lisez l’erreur de connexion. Vérifiez que l’appliance peut joindre l’hôte et que l’adresse de l’hôte est correcte. Un accès depuis votre navigateur ne prouve pas que l’appliance y a accès. |

## Étapes suivantes

[Créez votre première VM](/docs/xoa-hl/create-vm/), ou consultez le [guide de mise à jour de l’appliance et de l’hôte](/docs/guides/updates/).

{{< details title="Sources" closed="true" >}}
Vérifié avec : [version de l’image](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261022-a280852) ; [configuration des identifiants dans build-xoa-hl@fc7ebfa](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh) ; [écran utilisateur dans XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js) ; [écran des serveurs dans la même version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js) ; [patch de la page À propos dans xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
{{< /details >}}
