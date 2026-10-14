---
title: Protéger la connexion par un code à usage unique (OTP)
description: Activer les codes temporaires à usage unique pour un compte XOA-HL, vérifier la connexion et les retirer sans risque.
weight: 27
translationKey: xoa-manual-sign-in-otp
translationStatus: draft
sourceRevision: sha256:d6ef3292175f1ff56be82e05d96ee210df45b47ee3cece2d19943c60ee24603c
glossaryTerms: ["appliance"]
---

XOA-HL peut demander, après le mot de passe, un code temporaire à usage unique (TOTP) de 6 chiffres produit par une application d’authentification. Chaque compte à mot de passe local l’active pour lui-même. Essayez-le d’abord sur un compte non administrateur [créé pour ce test](/docs/xoa-hl/permissions/).

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests d’enrôlement, de connexion et de retrait de l’OTP sur cette appliance restent à faire. Les versions ultérieures peuvent différer.
{{< /callout >}}

## 1. Préparer

| Prérequis | Raison |
| --- | --- |
| Une application d’authentification TOTP sur un appareil que vous maîtrisez | Elle génère les codes à partir d’un secret partagé |
| Une heure correcte sur l’appliance et sur cet appareil | XO accepte le code courant et ceux des pas de 30 secondes juste avant et juste après |
| Un second administrateur, ou un plan de récupération indépendant | Sans cela, la perte de l’appareil peut bloquer l’unique administrateur |
| Une session de navigateur que vous gardez ouverte pendant le test | Elle permet de retirer l’OTP si la vérification échoue |

La vérification lors de l’enrôlement s’exécute dans votre navigateur, avec l’horloge du navigateur. La connexion est vérifiée par l’appliance, avec sa propre horloge. Un code accepté à l’enrôlement ne prouve donc pas que l’heure de l’appliance est correcte.

## 2. Activer l’OTP pour votre compte

1. Connectez-vous avec le compte à protéger. Ouvrez votre page utilisateur avec l’icône utilisateur du menu (`/#/user`).
2. Repérez l’interrupteur **OTP authentication** (libellé non traduit dans cette version). S’il manque, arrêtez le test et relevez la version installée ; le build examiné utilise le plan open source par défaut de XO, qui affiche ce contrôle. [Signalez cette différence](/docs/xoa-hl/troubleshooting/) sans supposer qu’un abonnement est nécessaire. Activez l’interrupteur. La boîte de dialogue **Add OTP authentication** affiche un QR code et le secret en texte.
3. Scannez le QR code, ou saisissez le secret, dans l’application d’authentification. L’entrée d’enrôlement est émise par `Xen Orchestra` et porte l’adresse e-mail ou l’identifiant du compte.
4. Saisissez le code courant dans **OTP code** et confirmez. Un code erroné rouvre la boîte de dialogue ; saisissez le code affiché à ce moment par l’application. **Annuler** laisse l’OTP désactivé.
5. Après réussite, la page utilisateur continue d’afficher le secret et son QR code à côté de l’interrupteur. Toute personne qui les voit peut générer des codes valides : ne partagez pas cette page et n’en faites pas de capture. Ce QR code utilise l’émetteur `XenOrchestra` (sans espace) avec le même secret ; conservez l’entrée d’origine dans l’application sans le scanner de nouveau.

## 3. Vérifier la connexion dans une nouvelle session

1. Gardez la session actuelle ouverte. Ouvrez une fenêtre de navigation privée et connectez-vous avec le nom d’utilisateur et le mot de passe.
2. Une deuxième page demande un **Code**. Saisissez le code courant de l’application et sélectionnez **Sign in**. Cette page est en anglais quelle que soit la langue de l’interface.
3. Un code erroné ou expiré affiche `Invalid code`. Attendez le code suivant et réessayez.
4. Vérifiez que le compte attendu est connecté, puis fermez la fenêtre privée.

Si la vérification échoue à chaque fois, utilisez la session ouverte pour retirer l’OTP (section 5), vérifiez les deux horloges, puis recommencez l’enrôlement.

## 4. Savoir ce que l’OTP ne couvre pas

- L’activation de l’OTP ne révoque pas les sessions ou jetons existants. Tous les jetons d’authentification valides évitent la vérification OTP, y compris ceux créés après l’enrôlement ; ce sont des identifiants distincts. Après avoir activé l’OTP, ouvrez **Authentication tokens** sur votre page utilisateur et supprimez les jetons que vous ne reconnaissez pas ou dont vous n’avez plus besoin. Un script qui utilise un jeton supprimé cesse de fonctionner.
- L’OTP protège la connexion web à XO pour ce compte. Il ne protège ni l’accès SSH ou console de l’appliance, ni XO Lite ou les comptes root de l’hôte, ni les autres comptes XO.
- Les fournisseurs d’authentification externes et leur propre MFA sont hors du périmètre de ce guide.

## 5. Retirer l’OTP

- **Votre propre compte :** sur votre page utilisateur, désactivez **OTP authentication** et confirmez **Remove OTP authentication**.
- **Un autre compte, en tant qu’administrateur :** ouvrez **Paramètres** > **Utilisateurs**. Dans la colonne **OTP**, sélectionnez **Supprimer** pour ce compte et confirmez. Vérifiez d’abord l’identité du demandeur, par exemple par un autre canal. L’utilisateur peut ensuite enrôler un nouvel appareil.

Les comptes sans OTP affichent **Non configuré** dans cette colonne. Si l’unique administrateur perd son appareil, l’interface ne propose aucune récupération. Les sources contiennent une commande de récupération qui réinitialise le mot de passe d’un compte, retire son OTP et en fait un administrateur. Elle n’a pas été validée sur cette appliance ; ce guide ne la fournit donc pas comme procédure. Gardez plutôt un second administrateur. Après le retrait, vérifiez que l’interrupteur OTP est désactivé et que la colonne OTP du compte affiche **Non configuré**. Dans une nouvelle session privée, vérifiez que la connexion avec l’identifiant et le mot de passe locaux réussit sans demande de code OTP ; gardez l’administrateur de secours connecté jusqu’à cette confirmation.

## Sources

Commit XO 5 `e281c536`, avec les correctifs HomeLab publiés appliqués : [section OTP de la page utilisateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js), [page utilisateur et jetons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js), [boîte de dialogue d’enrôlement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js), [activation et retrait](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [colonne OTP des utilisateurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [pages de connexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [formulaire de connexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug), [authentification et contournement par jeton](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [fenêtre TOTP](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs), [commande de récupération](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs) et [libellés anglais](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).

Disponibilité du build et enrôlement dans le navigateur : [XO default plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [browser authenticator](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js), [user preferences API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs), [HomeLab build](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
