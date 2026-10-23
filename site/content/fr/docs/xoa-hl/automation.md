---
title: "Automatiser avec xo-cli"
linkTitle: "Automatisation (xo-cli)"
description: "Lisez l’inventaire avec xo-cli et un jeton de courte durée, puis révoquez le jeton."
weight: 92
translationKey: xoa-manual-automation
translationStatus: reviewed
sourceRevision: sha256:02733ac5b32a1b356f14bd4b74120dad79a23bae4b41aff2c910840726898ebc
glossaryTerms: ["appliance", "host", "vm"]
---

Utilisez le client en ligne de commande xo-cli fourni avec l’appliance pour lire un petit inventaire avec un jeton de courte durée, puis révoquez le jeton. Faites ce test avant d’écrire une automatisation qui modifie une VM. Vous lancez les commandes dans un shell de l’**appliance XOA-HL**, et vous révoquez le jeton dans un navigateur connecté avec le même utilisateur de test.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2), avec `xo-cli` **0.32.2** et `xo-lib` **0.11.1**. Rédigé d’après le code publié ; pas encore testé en laboratoire. Les commandes ont seulement été lancées contre un serveur simulé.
{{< /callout >}}

## 1. Préparer le shell et la confiance TLS {#prepare}

**Avant de commencer**

- Vérifiez la version installée, comme indiqué dans la [maintenance de l’appliance](/docs/xoa-hl/maintenance/).
- Prévoyez un compte utilisateur normal de test et une VM de test que vous pouvez perdre. Testez séparément ce que cet utilisateur a le droit de faire, avec [Utilisateurs et droits](/docs/xoa-hl/permissions/).
- Utilisez un nom DNS de l’appliance qui correspond à son certificat. Le certificat auto-signé `xoa.local` créé à l’installation peut demander d’abord une préparation du DNS ou du certificat du laboratoire.
- Obtenez la CA ou le certificat public de l’appliance sous forme de fichier PEM, par un canal de confiance. Vérifiez son empreinte par un autre moyen.

1. Ouvrez une nouvelle session Bash dédiée **dans l’appliance**. Vous y utilisez `/usr/local/bin/xo-cli` fourni.
2. Dans l’exemple de la section suivante, remplacez le chemin du fichier PEM, l’URL et l’adresse e-mail par les vôtres.

`NODE_EXTRA_CA_CERTS` ajoute votre certificat à la liste de confiance ; le nom d’hôte est toujours vérifié. Si la vérification TLS échoue, corrigez le nom ou le certificat. Ne la contournez jamais avec `--allowUnauthorized` ou `NODE_TLS_REJECT_UNAUTHORIZED=0`.

## 2. Enregistrer un jeton de courte durée {#register-token}

Les commandes ci-dessous gardent les identifiants dans un nouveau dossier temporaire : votre configuration xo-cli existante n’est pas touchée. `umask 077` rend le nouveau fichier lisible par vous seul.

- `register` demande le mot de passe. Ne l’ajoutez pas comme argument, et ne placez jamais de jeton dans une URL.
- Si le compte utilise des codes à usage unique (OTP), ajoutez `--otp CODE` avant l’URL, avec un code valide.

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

Le jeton demande volontairement `1 hour`. Par défaut, le serveur donne à un jeton 30 jours, avec un maximum de six mois ; la configuration du serveur peut modifier ces limites.

Le jeton a tous les droits de son utilisateur : il n’est pas limité à la lecture. Traitez le dossier de configuration comme un mot de passe. Gardez-le hors des traces du shell, des sauvegardes jointes aux issues et du contrôle de version. L’enregistrement crée un jeton de connexion ; les commandes suivantes ne font que lire des données.

## 3. Découvrir et lire l’inventaire {#read-inventory}

Lancez ces commandes. Placez les options comme `--json` et `--id` avant les paramètres.

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| Commande | Ce que vous obtenez |
| --- | --- |
| `list-commands xo.getAllObjects` | Les paramètres de la méthode, sous une forme lisible. Voir une méthode ne signifie pas que vous avez le droit de l’utiliser |
| `system.getServerVersion --json` | La version du paquet serveur, `"5.193.1"` dans cette version. Ce n’est pas la version de XO (5.113.2) |
| `list-objects --id --name_label --power_state type=VM` | Un tableau JSON limité à ces propriétés. L’état des VM ne change pas |
| `xo.getAllObjects --json …` | Un objet JSON indexé par identifiant d’objet, filtré par type d’objet et limité à un objet |

Le préfixe `json:` envoie une valeur typée : `limit=json:1` envoie un nombre, alors que `limit=1` envoie une chaîne. La dernière commande envoie cette requête JSON-RPC par **WebSocket vers `/api/`** (ce n’est pas un POST HTTP) :

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

Les filtres et les champs choisis ne font que sélectionner ce que vous voyez : ce **ne sont pas des limites d’accès**. Ne supposez pas que l’API renvoie seulement les objets affichés dans l’interface web de l’utilisateur, ni que les champs absents de la sortie n’ont jamais été récupérés. Gardez les résultats privés, et vérifiez séparément ce que le compte peut réellement voir. Un nom n’est pas un identifiant stable. Ce résultat limité n’est pas un inventaire complet, et ce n’est pas un moyen fiable de choisir une VM.

## 4. Révoquer le jeton et nettoyer {#revoke-token}

1. Dans une session de navigateur séparée, connectée avec le même utilisateur de test, sélectionnez l’icône utilisateur dans le menu pour ouvrir **Utilisateur** (`/#/user`).
2. Sous **Authentication tokens**, supprimez le jeton de ce client CLI.
3. De retour dans le shell, lancez la première commande ci-dessous avant de supprimer quoi que ce soit en local. Elle doit échouer avec une erreur d’authentification et un code de sortie non nul.
4. Si elle réussit, le jeton n’est pas révoqué. Arrêtez-vous, et vérifiez le compte et ses jetons avant d’affirmer que la révocation a fonctionné.
5. Lancez les autres commandes pour supprimer les identifiants locaux, puis fermez le shell dédié.

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

**Vérification :** après la suppression du jeton dans le navigateur, la commande de version échoue avec une erreur d’authentification.

`unregister` supprime seulement les entrées locales `server` et `token` ; il **ne révoque pas** le jeton sur le serveur. Supprimer le dossier temporaire n’est qu’un nettoyage local : cela ne remplace pas la révocation. Une automatisation durable demande sa propre conception pour le stockage des secrets, le renouvellement, la révocation, le traitement des erreurs et des droits limités au strict nécessaire ; ce n’est pas traité ici.

{{< details title="Sources" closed="true" >}}
- **Client en ligne de commande** : [xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [stockage des réglages du client](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js).
- **Jetons et inventaire** : [API des jetons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [expiration des jetons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [API d’inventaire](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [jetons sur la page utilisateur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
{{< /details >}}
