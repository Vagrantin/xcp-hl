---
title: "Protéger la connexion par un code à usage unique"
linkTitle: "Codes à usage unique"
description: "Ajoutez un code à usage unique à la connexion d’un compte, vérifiez-le et retirez-le sans risque."
weight: 71
translationKey: xoa-manual-sign-in-otp
translationStatus: reviewed
sourceRevision: sha256:6cd964ad6c27dba4fac2174ee07db3969f54dcdebe9b7f253e906688f3346a44
glossaryTerms: ["appliance"]
---

XOA-HL peut demander, après le mot de passe, un code à usage unique de 6 chiffres produit par une application d’authentification. Le code change avec le temps (TOTP). Chaque compte qui se connecte avec un mot de passe local l’active pour lui-même. Essayez-le d’abord sur un compte non administrateur [créé pour ce test](/docs/xoa-hl/permissions/).

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Les versions ultérieures peuvent différer.
{{< /callout >}}

## Avant de commencer {#prepare}

| Il vous faut | Pourquoi |
| --- | --- |
| Une application d’authentification TOTP sur un appareil que vous maîtrisez | Elle génère les codes à partir d’un secret partagé |
| L’heure exacte sur l’appliance et sur cet appareil | XO accepte le code courant et ceux des pas de 30 secondes juste avant et juste après |
| Un second administrateur, ou un plan de récupération distinct | Sans cela, la perte de l’appareil peut bloquer l’unique administrateur |
| Une session de navigateur que vous gardez ouverte pendant le test | Elle permet de retirer le code à usage unique si la vérification échoue |

Pendant l’activation, c’est votre navigateur qui vérifie le code saisi, avec sa propre horloge. À la connexion, c’est l’appliance qui vérifie le code, avec la sienne. Un code accepté à l’activation ne prouve donc pas que l’heure de l’appliance est correcte.

## Activer un code à usage unique pour votre compte {#enable-otp}

1. Connectez-vous avec le compte à protéger. Ouvrez votre page utilisateur avec l’icône utilisateur du menu (`/#/user`).
2. Repérez l’interrupteur **OTP authentication** et activez-le. La boîte de dialogue **Add OTP authentication** affiche un QR code et le secret en texte.
3. Scannez le QR code, ou saisissez le secret, dans votre application d’authentification. La nouvelle entrée est émise par `Xen Orchestra` et porte l’adresse e-mail ou l’identifiant du compte.
4. Saisissez le code courant dans **OTP code** et confirmez. Si le code est faux, la boîte de dialogue se rouvre : saisissez le code que l’application affiche à ce moment. **Annuler** laisse le code à usage unique désactivé.

Si l’interrupteur est absent, arrêtez-vous et notez la version installée. Ce build utilise le plan open source par défaut de XO, qui affiche l’interrupteur : l’absence d’abonnement n’en est donc pas la cause. [Signalez la différence](/docs/xoa-hl/troubleshooting/).

**Vérification :** l’interrupteur est activé, et votre page utilisateur affiche le secret et son QR code à côté. Toute personne qui les voit peut générer des codes valides : ne partagez pas cette page et n’en faites pas de capture d’écran. Ce QR code indique l’émetteur `XenOrchestra` (sans espace) pour le même secret. Gardez l’entrée déjà présente dans votre application ; ne le scannez pas de nouveau.

## Vérifier la connexion dans une nouvelle session {#check-sign-in}

1. Gardez votre session actuelle ouverte. Ouvrez une fenêtre de navigation privée et connectez-vous avec votre nom d’utilisateur et votre mot de passe.
2. Une deuxième page demande un **Code**. Saisissez le code courant de l’application et sélectionnez **Sign in**.
3. Un code faux ou expiré affiche `Invalid code`. Attendez le code suivant et réessayez.
4. Vérifiez que vous êtes connecté au bon compte, puis fermez la fenêtre privée.

**Vérification :** la connexion a demandé un code et a accepté le bon. Si elle échoue à chaque fois, utilisez la session ouverte pour [retirer le code à usage unique](#remove-otp), vérifiez les deux horloges, puis réactivez-le.

## Ce que le code à usage unique ne protège pas {#otp-limits}

- L’activer ne ferme pas les sessions existantes et ne révoque pas les jetons. Tout jeton d’authentification valide évite la vérification du code, y compris les jetons créés plus tard : les jetons sont des identifiants distincts. Après l’activation, ouvrez **Authentication tokens** sur votre page utilisateur et supprimez les jetons que vous ne reconnaissez pas ou dont vous n’avez plus besoin. Un script qui utilise un jeton supprimé cesse de fonctionner.
- Il protège uniquement la connexion web à XO pour ce compte. Il ne protège ni l’accès SSH ou console à l’appliance, ni XO Lite ou le compte root de l’hôte, ni les autres comptes XO.
- Les fournisseurs de connexion externes et leur propre authentification à plusieurs facteurs ne sont pas traités ici.

## Retirer un code à usage unique {#remove-otp}

- **Votre propre compte :** sur votre page utilisateur, désactivez **OTP authentication** et confirmez **Remove OTP authentication**.
- **Un autre compte, en tant qu’administrateur :** ouvrez **Paramètres → Utilisateurs**. Dans la colonne **OTP**, sélectionnez **Supprimer** pour ce compte et confirmez. Vérifiez d’abord qui fait la demande, par exemple par un autre canal. L’utilisateur peut ensuite configurer un nouvel appareil.

Les comptes sans code à usage unique affichent **Non configuré** dans cette colonne. Si l’unique administrateur perd son appareil, l’interface ne propose aucun moyen de récupérer l’accès. Depuis la console de l’appliance, vous pouvez encore [récupérer l’accès administrateur](/docs/xoa-hl/troubleshooting/#recover-admin-access). Un second administrateur reste plus simple : gardez-en un.

**Vérification :** l’interrupteur est désactivé et la colonne OTP du compte affiche **Non configuré**. Dans une nouvelle fenêtre privée, le compte se connecte avec son nom d’utilisateur et son mot de passe locaux, sans code. Gardez l’administrateur de secours connecté jusqu’à cette confirmation.

{{< details title="Sources" closed="true" >}}
- **Page utilisateur et activation** : [section OTP de la page utilisateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js), [page utilisateur et jetons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js), [boîte de dialogue d’activation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js), [actions d’activation et de retrait](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [colonne OTP des paramètres Utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js).
- **Connexion et jetons** : [pages de connexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [formulaire de connexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug), [authentification et contournement par jeton](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [fenêtre de temps TOTP](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs), [commande de récupération](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [libellés de l’interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Build et activation dans le navigateur** : [plan XO par défaut](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [authentificateur du navigateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js), [API des préférences utilisateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs), [build HomeLab](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
