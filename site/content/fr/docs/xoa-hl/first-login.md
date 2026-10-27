---
title: "Se connecter, ajouter un hôte et choisir la langue"
linkTitle: "Première connexion"
description: "Connectez-vous à XOA-HL, changez le mot de passe, choisissez la langue de l’interface et ajoutez votre hôte."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: draft
sourceRevision: sha256:db4332ad53583587f2c85f7b871c7ed805fde9d300e42942500e267cbfa98141
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

À la fin de ce guide, vous pouvez vous connecter à XOA-HL, votre hôte est connecté et l’interface s’affiche dans votre langue.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261027-ca44911`, paquet `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Testé sur une appliance de laboratoire le 2026-10-27. Les images plus anciennes et les mises à jour ultérieures peuvent différer. Image reconstruite le 2026-10-27 avec le correctif de configuration de `build-xoa-hl@fa0c987`. Voir [comment identifier le fichier corrigé](/docs/xoa-hl/first-login/#identify-the-rebuilt-image).
{{< /callout >}}

## Avant de commencer

- [Déployez XOA-HL depuis XO Lite](/docs/start/#start-deploy-xoa). Notez le tag de l’image et l’adresse de l’appliance.
- Gardez l’identifiant et le mot de passe administrateur XO saisis dans le formulaire de déploiement. Il vous faut aussi l’adresse de gestion de l’hôte et son mot de passe `root`.
- Utilisez un navigateur sur un réseau de gestion de confiance.

La plupart des étapes se font dans votre **navigateur**. La vérification de l’image demande un shell root dans l’appliance. Le nettoyage des déploiements anciens ou incomplets demande un shell root sur l’hôte.

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
Sur les images construites avant le correctif du 2026-10-27, un premier démarrage en échec peut laisser le compte web `admin@admin.net` avec le mot de passe `admin`. Essayez-le uniquement sur un réseau de confiance, puis changez immédiatement son mot de passe. Sur l’image reconstruite, utilisez le compte du déploiement. S’il ne fonctionne pas, examinez les services de configuration décrits ci-dessous. Ne supposez pas que le compte par défaut doit fonctionner.
{{< /callout >}}

## 2. Définir un mot de passe durable

1. Sélectionnez l’**icône utilisateur** dans le menu pour ouvrir **Utilisateur** (`/#/user`).
2. Dans la section du mot de passe, saisissez le mot de passe actuel, puis deux fois le nouveau. Choisissez un mot de passe unique. Sélectionnez **OK**.
3. Rangez le nouveau mot de passe en lieu sûr. Déconnectez-vous, puis reconnectez-vous avec le nouveau mot de passe.

**Vérification :** la connexion avec le nouveau mot de passe réussit. Seul le compte web change. Le mot de passe `root` de l’hôte et celui du compte SSH de l’appliance restent identiques.

{{< callout type="warning" >}}
Ces problèmes concernent les images construites avant le correctif du 2026-10-27, dont `qa-xoa-build-58.xva` (SHA-256 commençant par `5f8427fd`). Ils ne décrivent pas un déploiement réussi de l’image reconstruite identifiée ci-dessous :

- **Redémarrez l’appliance une fois.** Après le changement de mot de passe, redémarrez normalement la VM de l’appliance depuis XO Lite (**Redémarrer**, pas un redémarrage forcé). Tant que l’appliance n’a pas enregistré ses réglages, une coupure de courant ou un arrêt forcé peut rétablir le compte `admin@admin.net` avec le mot de passe `admin`, et votre propre compte est perdu. Pour la même raison, ne gardez jamais un instantané d’une appliance en marche comme état de référence.
- **Supprimez les identifiants laissés par le déploiement.** Les réglages de la VM sur l’hôte peuvent conserver les identifiants du déploiement en clair. Après avoir vérifié l’accès, suivez la procédure de nettoyage ci-dessous, puis changez le mot de passe web et celui du compte SSH `xo` avec `passwd` si SSH est activé.
{{< /callout >}}

### Identifier l’image reconstruite {#identify-the-rebuilt-image}

Le fichier corrigé est `qa-xoa-build-59.xva`, dans la version `xoa-image-20261027-ca44911`. Son SHA-256 est `cc20b9398d5ab0dc03eae6706d3b54236e2d245fa1d0dd1232d59836387057aa`. Il a été construit depuis `build-xoa-hl@fa0c987`. Le fichier précédent portait le même tag et les mêmes versions dans À propos.

Dans l’appliance, exécutez cette vérification en lecture seule en tant que **root**, depuis sa console ou une session SSH autorisée :

```bash
redis-cli config get appendonly
```

Sur l’image reconstruite, le résultat est `appendonly`, puis `yes`. L’image précédente renvoie `no`. Cette commande vérifie le réglage actuel de Redis. Une image modifiée ou personnalisée peut aussi renvoyer `yes` ; conservez le nom du fichier d’origine et sa somme de contrôle pour identifier l’image.

L’image reconstruite enregistre le compte du déploiement avant de marquer la configuration comme terminée. Les changements suivants utilisent le fichier d’ajouts de Redis (AOF), enregistré chaque seconde. Un arrêt forcé peut encore perdre environ la dernière seconde de changements. Arrêtez normalement l’appliance avant de créer un instantané de référence.

### Nettoyer les déploiements anciens ou incomplets

Avant de supprimer les clés, attendez que l’appliance ait appliqué les comptes et vérifiez la connexion avec les identifiants web prévus et, si SSH est activé, avec les identifiants SSH. Utilisez l’UUID exact de la VM de l’appliance. Dans un **shell root sur l’hôte XCP-HL**, vérifiez chaque clé sans afficher sa valeur :

```bash
for key in admin-account system-account-xoa-password xoa-updater-credentials; do
  if xe vm-param-get uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key" >/dev/null 2>&1; then
    xe vm-param-remove uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key"
  fi
done
```

Une clé absente est normale ; examinez toute erreur de suppression. Ne copiez pas toute la table `xenstore-data` dans un journal ou un rapport. Les anciens journaux du premier démarrage, exports de VM et sauvegardes des métadonnées du pool peuvent encore contenir les mots de passe du déploiement. Changez les mots de passe web et SSH fournis au déploiement, puis protégez ou retirez ces anciennes copies. Supprimer les clés actuelles n’efface pas les copies historiques.

Gardez l’onglet de déploiement XO Lite ouvert jusqu’à la fin. Sur l’image reconstruite, le nettoyage dans l’invité a aussi supprimé `vm-data/admin-account` et `vm-data/system-account-xoa-password` de la table persistante `xenstore-data` de XAPI après le premier démarrage. Ce résultat a été observé sur un seul hôte XCP-HL v8.3 dans [#311](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771). Ne supposez pas le même résultat avec les images anciennes, Vates, Ronivay ou personnalisées, ni avec les déploiements en échec ou abandonnés. Vérifiez et supprimez les clés restantes sur l’hôte comme ci-dessus, après l’application des comptes. Le correctif XO Lite de [#310](https://github.com/Vagrantin/xcp-hl/issues/310) couvre aussi les autres sources d’images. Une mise à jour du seul RPM de l’application ne remplace pas les scripts de configuration d’une ancienne image.

Pour les images reconstruites avec les correctifs #310/#311, un échec de la collecte au premier démarrage bloque volontairement le réseau ; XO Lite peut afficher « XOA ne répond pas » sans adresse IP. Depuis la console de la VM, consultez `systemctl status xoa-first-boot.service` et `/var/log/xoa-first-boot.log`. Ces images exigent une adresse e-mail et un mot de passe administrateur complets fournis par XO Lite ; un import de XVA sans ces données n’est pas accepté silencieusement. Corrigez les données de déploiement avant de redémarrer et conservez les clés jusqu’à la réussite de la collecte. Si la collecte a réussi mais que les identifiants n’ont pas été appliqués, consultez `systemctl status xoa-credentials.service` et relancez ce service après avoir corrigé la cause. Ne copiez pas le fichier `/etc/xoa-first-boot.env`, réservé à root, dans les rapports.

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

Ouvrez **À propos** (`/#/about`) avec un compte administrateur. Notez la **version XOA-HL** et la **version de la VM XOA-HL**. Conservez-les avec le nom du fichier d’origine, sa somme de contrôle et le tag de l’image. Les deux fichiers du 2026-10-27 affichent les mêmes versions dans À propos. La vérification ci-dessus distingue leurs réglages Redis par défaut. Les mises à jour de paquets peuvent ensuite changer la version de l’application.

La [matrice des versions](/docs/reference/release-matrix/) liste le contenu de chaque version publiée. Elle ne contient pas de résultats de tests.

## En cas de problème

| Problème | À vérifier |
| --- | --- |
| La page de l’appliance ne s’ouvre pas | Dans XO Lite, vérifiez que la VM de l’appliance fonctionne. Vérifiez ensuite son adresse, son réseau, sa passerelle et l’accès depuis votre navigateur. Ne redéployez pas par-dessus une VM qui fonctionne. |
| Les identifiants du déploiement ne fonctionnent pas | Attendez la fin du premier démarrage et vérifiez que vous utilisez le compte web. Sur l’image reconstruite, examinez les services de configuration décrits plus haut. Sur une ancienne image, essayez le compte de secours uniquement sur un réseau de confiance. Après un arrêt forcé précoce, une ancienne image peut avoir perdu votre compte : changez le mot de passe de secours, puis recréez votre compte. Lisez `/var/log/xoa-first-boot.log` depuis une console ou une session SSH autorisée. Retirez les données privées avant tout partage. |
| La connexion à l’hôte échoue | Vérifiez l’adresse de l’hôte et son mot de passe `root`. Le mot de passe administrateur web est un autre mot de passe. |
| Le serveur affiche une erreur de certificat | Vérifiez l’identité de l’hôte avant d’accepter son certificat autosigné. N’acceptez pas un changement que vous ne savez pas expliquer. |
| Le serveur est activé mais l’inventaire est vide | Lisez l’erreur de connexion. Vérifiez que l’appliance peut joindre l’hôte et que l’adresse de l’hôte est correcte. Un accès depuis votre navigateur ne prouve pas que l’appliance y a accès. |

## Étapes suivantes

[Créez votre première VM](/docs/xoa-hl/create-vm/), ou consultez le [guide de mise à jour de l’appliance et de l’hôte](/docs/guides/updates/).

{{< details title="Sources" closed="true" >}}
Vérifié avec : [version de l’image](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261027-ca44911) ; [configuration des identifiants dans build-xoa-hl@fa0c987](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-credentials.sh) ; [écran utilisateur dans XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js) ; [écran des serveurs dans la même version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js) ; [patch de la page À propos dans xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
- [build-xoa-hl@fa0c987: AOF](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-finalize-state.sh)
- [#311: 2026-10-27](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771)
{{< /details >}}
