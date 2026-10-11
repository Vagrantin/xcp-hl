---
title: Automatiser l’inventaire avec xo-cli
description: Découvrir les méthodes, lire l’inventaire et révoquer un jeton CLI court.
weight: 72
translationKey: xoa-manual-automation
translationStatus: draft
sourceRevision: sha256:d62ec0a49c44ac7275b68cb4b2cf81eabcafc83118ff7e2186109ad545cfe4f1
glossaryTerms: ["appliance", "host", "vm"]
---

Utilisez xo-cli fourni pour un petit inventaire en lecture seule avant d’automatiser des modifications de VM.

{{< callout type="info" >}}
Référence vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les versions suivantes peuvent différer. La validation sur appliance installée et la revue humaine des traductions restent à faire.
{{< /callout >}}

Le client au commit figé est `xo-cli` **0.32.2** avec `xo-lib` **0.11.1**. Les commandes ci-dessous ont été exécutées avec cette source CLI contre un serveur HTTPS/WebSocket synthétique local : refus/acceptation TLS, saisie du mot de passe, demande d’expiration, découverte des méthodes, paramètres d’inventaire et nettoyage local ont passé. Cela valide le contrat client, pas une appliance réelle, l’application de l’expiration, les droits sur les objets ni les opérations XAPI.

## 1. Préparer le laboratoire et la confiance TLS

Lancez `/usr/local/bin/xo-cli` fourni **dans l’appliance**, dans une session Bash dédiée. Préparez un utilisateur normal de test et une VM jetable. Vérifiez d’abord la release avec la [maintenance](/docs/xoa-hl/maintenance/) ; utilisez les [droits](/docs/xoa-hl/permissions/) pour les tests d’autorisation distincts.

Utilisez un nom DNS correspondant au certificat de l’appliance. Obtenez le certificat/CA public par un canal de confiance et vérifiez son empreinte indépendamment. Remplacez le chemin par ce fichier PEM, ainsi que l’URL et l’adresse de compte. `NODE_EXTRA_CA_CERTS` ajoute la confiance sans désactiver la vérification du nom. Le certificat initial auto-signé `xoa.local` peut nécessiter une préparation DNS/certificat du laboratoire. Ne contournez pas un échec avec `--allowUnauthorized` ou `NODE_TLS_REJECT_UNAUTHORIZED=0`.

## 2. Enregistrer un jeton de courte durée

Cette fonction isole les identifiants dans un nouveau dossier et préserve la configuration CLI existante. Un umask restrictif protège le nouveau fichier. L’enregistrement demande le mot de passe ; ne l’ajoutez pas comme argument positionnel et ne placez pas de jeton dans une URL. Si le compte exige un OTP, ajoutez `--otp CODE` avant l’URL avec un code valide.

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

Les valeurs serveur figées sont 30 jours par défaut et 0,5 an au maximum ; la demande `1 hour` est volontairement plus courte. La configuration serveur peut modifier ces limites. Le jeton porte les droits de son utilisateur, pas un périmètre dédié à la lecture seule. Traitez le fichier de configuration comme un secret : excluez-le des traces shell, des sauvegardes jointes aux issues et du contrôle de version. Cet enregistrement crée un état d’authentification ; les exemples suivants lisent seulement les données.

## 3. Découvrir et lire

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| Commande | Interprétation attendue |
| --- | --- |
| `list-commands xo.getAllObjects` | Paramètres lisibles par une personne ; la découverte ne donne aucun droit |
| `system.getServerVersion --json` | Version du paquet serveur, `"5.193.1"` à ce commit ; pas la version du produit XO |
| `list-objects --id --name_label --power_state type=VM` | Tableau JSON limité à ces propriétés ; ne change aucun état VM |
| `xo.getAllObjects --json …` | Objet JSON indexé par identifiant d’objet ; filtre objet et limite numérique |

Gardez les options avant les paramètres. `json:` produit du JSON typé : `limit=json:1` transmet un nombre ; `limit=1` transmet une chaîne. La dernière commande correspond à cette requête JSON-RPC sur **WebSocket `/api/`**, pas à un exemple de POST HTTP :

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

Les filtres d’inventaire et la projection de sortie sélectionnent les données : **ce ne sont pas des frontières d’accès**. Ne supposez pas que cette API limite l’inventaire aux objets affichés dans l’interface de l’utilisateur, ni que les champs omis de la sortie n’ont jamais été récupérés. Gardez les résultats privés et vérifiez séparément la visibilité réelle du compte. Un libellé n’est pas un ID stable ; ce résultat limité n’est ni un inventaire complet ni un choix déterministe de VM.

## 4. Révoquer et nettoyer

Dans la session navigateur indépendante du même utilisateur, ouvrez **User → Authentication tokens** (`/#/user`) et supprimez le jeton associé à ce client CLI. Avant d’effacer les identifiants locaux, lancez la première commande ci-dessous et attendez un code de sortie non nul avec refus d’authentification. Une réussite ne démontre pas la révocation ; recherchez le compte/jeton concerné avant de déclarer le test réussi.

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

`unregister` enlève seulement les champs locaux `server` et `token`. Il **ne révoque pas** le jeton serveur. Supprimer le dossier temporaire est un nettoyage local, pas un remplacement de la révocation. Fermez ensuite le shell dédié. Pour une automatisation durable, concevez séparément le stockage des secrets, le renouvellement, la révocation, le traitement des erreurs et les opérations précisément autorisées.

## Sources

[xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [client storage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js), [token API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [token expiry](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [inventory API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [profile tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
