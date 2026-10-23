---
title: "Configurer le service de l’appliance"
linkTitle: "Paramètres du service"
description: "Trouvez les fichiers de configuration du service, vérifiez les accès et le certificat HTTPS, et appliquez une modification sans risque."
weight: 91
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:cf10324c828a27039571b3a119cc1feacd94fbe74d8a0815a3060736e0c32685
glossaryTerms: ["appliance", "host", "pool"]
---

Trouvez les fichiers de configuration de xo-server sur l’appliance XOA-HL, vérifiez ses accès de gestion et son certificat HTTPS, et appliquez une modification sans risque. Vous travaillez en root dans un shell de l’appliance, avec une console séparée prête à servir. Ces fichiers sont distincts des réglages et des données que l’interface web exporte.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire.
{{< /callout >}}

## Trouver les fichiers de réglages {#settings-files}

| Emplacement | Contenu | Comment le traiter |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` et `sample.config.toml` | Valeurs par défaut du paquet et exemple commenté | En lecture seule. Une mise à jour du paquet remplace ces fichiers |
| `/root/.config/xo-server/config.toml` | Vos propres réglages (le fichier opérateur). Créé à l’installation seulement s’il n’existe pas | Gardez une sauvegarde privée avant de le modifier. L’installation du paquet conserve ce fichier |
| `/root/.config/xo-server/config.z-auto.json` | Réglages écrits par le serveur lui-même | Vérifiez s’il existe quand vous cherchez des surcharges. Ne l’écrasez pas à l’aveugle |
| Base Redis | Données de l’application XO | Utilisez l’export et l’import de l’interface web, dans leur périmètre documenté |
| `/etc/xoa-hl/update.conf` | Mode, calendrier et canal des mises à jour de l’appliance | Utilisez plutôt **Paramètres → Mises à jour XOA-HL** et le guide des mises à jour |
| `/opt/xo/xoahl.crt` et `xoahl.key` | Certificat TLS et clé privée de l’appliance | Gardez-en une copie à part. Ne joignez jamais la clé privée à un rapport |

Le service systemd livré s’exécute en root et lit la configuration utilisateur sous `/root/.config`. xo-server lit aussi `/etc/xo-server/config.*` et les fichiers locaux `.xo-server.*`, et fusionne plusieurs fichiers. Avant de conclure quelle valeur s’applique, recherchez les surcharges du service et les autres fichiers de configuration. Cette page couvre seulement le service livré, pas un compte de service personnalisé.

L’[export de configuration](/docs/xoa-hl/configuration-backup/) n’inclut ni votre fichier TOML, ni les fichiers TLS, ni les réglages de mise à jour. Pour ceux-ci, consultez la [maintenance de l’appliance](/docs/xoa-hl/maintenance/) et les [mises à jour](/docs/guides/updates/).

## Définir l’URL de l’appliance pour la découverte des pools {#public-url}

`http.publicUrl` définit l’URL de l’appliance que XO enregistre dans chaque pool connecté, pour la découverte des pools. Ce réglage ne crée ni écoute réseau, ni certificat, ni enregistrement DNS. Utilisez une vraie URL HTTPS de l’appliance, avec un DNS correspondant et un certificat de confiance, et vérifiez d’abord qu’elle s’ouvre dans un navigateur. Lisez [Hôtes et pools](/docs/xoa-hl/hosts-pools/) avant de la modifier.

Faites cet essai sur une appliance de laboratoire que vous pouvez reconstruire. Ajoutez la propriété à la table `[http]` **existante**. Cet exemple minimal conserve l’écoute HTTPS et l’adresse Redis livrées. Il ne remplace pas un fichier que vous avez personnalisé :

```toml
[http]
publicUrl = "https://xoa.lab.example"

[[http.listen]]
port = 443
cert = "/opt/xo/xoahl.crt"
key = "/opt/xo/xoahl.key"

[redis]
uri = "redis://127.0.0.1:6379/0"
```

N’ajoutez pas de seconde table `[http]` et ne supprimez pas l’écoute existante. Gardez les vrais chemins du certificat et de la clé. Le paquet crée son propre certificat auto-signé et sa clé à l’installation ; il ne fournit pas de clé partagée. Si la clé, le certificat ou le marqueur `/var/lib/xoa-hl/tls-generated` manque, une nouvelle paire est générée. Notez donc l’état TLS installé avant une mise à jour. Le remplacement du certificat, les proxys inverses et le déplacement de Redis ne sont pas traités ici.

## Cartographier l’accès de gestion avant de restreindre le réseau {#management-network}

Ce contrôle se contente de lire ; il ne modifie rien. La configuration livrée écoute en HTTPS sur le port `443`. Vos propres réglages, un proxy, un pare-feu ou une autre image peuvent changer le chemin réel. L’interface web ne crée aucune règle de pare-feu à votre place.

**Avant de commencer**

- Convenez avec les responsables du réseau et des hôtes des clients de gestion, sous-réseaux, services et destinations de sauvegarde autorisés.
- Convenez d’un accès console séparé que la restriction ne touchera pas.
- Faites-le avant de modifier une ACL, une VIF, une PIF d’hôte ou une politique de commutateur.

| Chemin | Ce qu’il faut noter et vérifier |
| --- | --- |
| Navigateur autorisé → XOA-HL | Notez la VM et l’adresse de l’appliance, le nom résolu, le vrai point d’accès HTTPS et l’identité du certificat. Depuis un client autorisé, reconnectez-vous et vérifiez la liste des hôtes. L’écoute livrée est `443`, mais vérifiez la configuration installée et le point d’accès réel. `http.publicUrl` annonce seulement une adresse ; il n’ouvre pas de port. |
| XOA-HL → hôtes et pools | Dans **Paramètres → Serveurs**, notez l’adresse du serveur connecté, les ID attendus du pool et des hôtes, et la façon dont le certificat est traité. Vérifiez la liste des hôtes en direct et, si vous l’avez déjà testé en laboratoire, des [statistiques d’hôte](/docs/xoa-hl/hosts-pools/#host-statistics) récentes en lecture seule. Une connexion du navigateur ne prouve pas à elle seule que l’appliance atteint les hôtes. |
| Navigateur → console via XOA-HL → hôte de la VM | Si vous avez besoin de la console, ouvrez celle d’une VM de test en fonctionnement avec le [guide de la console](/docs/xoa-hl/vm-operations/#vm-console). Notez le résultat dans le navigateur et l’hôte sur lequel tourne la VM. La console utilise une connexion WebSocket distincte entre l’appliance et cet hôte ; une liste des hôtes qui fonctionne ne la prouve pas. |
| XOA-HL → destinations de sauvegarde et mises à jour | Listez chaque destination de sauvegarde et les services de paquets, de DNS et d’heure de l’appliance, avec leurs responsables. Testez une destination avec sa [procédure de sauvegarde](/docs/xoa-hl/backup-restore/), et l’accès aux paquets avec le [guide de mise à jour de l’appliance](/docs/xoa-hl/maintenance/). Une connexion web qui fonctionne ne prouve pas ces chemins. |

Sur une appliance de laboratoire dont vous avez identifié la version :

1. Pour chaque chemin nécessaire, notez le client source, le nom ou l’adresse de destination, le service, le résultat et l’heure.
2. Demandez au responsable réseau de vérifier qu’un client de test non autorisé ne peut pas atteindre la page de connexion web, avec un test permis et des journaux séparés. Un ping bloqué ne prouve ni l’isolation HTTPS ni que la gestion fonctionne toujours.
3. Gardez votre accès console en dehors du chemin que vous prévoyez de restreindre.
4. Si une modification de politique est approuvée séparément, changez une seule règle à la fois, gérée par son responsable. Après chaque changement, refaites les mêmes tests autorisés et refusés.
5. Avant de fermer la fenêtre, vérifiez la connexion, la liste des hôtes, la console et les sauvegardes.

**Vérification :** chaque chemin nécessaire fonctionne toujours, et le client non autorisé ne peut pas atteindre la page de connexion.

Si un chemin nécessaire échoue ou si vous perdez l’accès, arrêtez-vous. Utilisez le retour arrière documenté du responsable réseau depuis la console séparée. Ne retirez pas la connexion XOA et ne modifiez pas la PIF de gestion de l’hôte pour aller plus vite. Les écoutes réelles, la segmentation des clients, les chemins de proxy et de NAT, les ports des hôtes et des destinations, et le retour arrière ne sont pas traités ici. N’établissez pas de liste d’autorisation de production à partir de cette seule page.

## Vérifier le certificat HTTPS avant de le remplacer {#tls-certificate-preflight}

Ce contrôle lit seulement des fichiers et des connexions ; il ne renouvelle rien. À l’installation, la configuration livrée écrit une écoute HTTPS sur le port `443` qui utilise `/opt/xo/xoahl.crt` et `/opt/xo/xoahl.key`. Des modifications ultérieures ou un proxy inverse peuvent servir TLS ailleurs.

Le paquet ne fournit pas de clé privée partagée. À l’installation, il génère une paire auto-signée `CN=xoa.local` si l’un des fichiers ou le marqueur `/var/lib/xoa-hl/tls-generated` manque. Une mise à jour ultérieure du paquet peut régénérer la paire de la même façon, puis elle redémarre `xo-server` (`%posttrans`). Notez les vrais chemins et l’état du paquet avant de prévoir un renouvellement. Ne supprimez jamais le marqueur pour changer de certificat.

1. Assurez-vous qu’une console séparée et un compte d’administrateur local sont disponibles.
2. Notez en privé l’image et le paquet installés, les valeurs effectives de `http.listen` et les surcharges de configuration fusionnées. Lancez `systemctl cat xo-server` pour voir les surcharges du service.
3. Notez si un proxy inverse, un répartiteur de charge ou un autre point de terminaison TLS se trouve devant l’appliance. `http.publicUrl` annonce seulement une adresse : il ne montre ni l’écoute ni le certificat que voient les navigateurs. Arrêtez-vous si vous trouvez plusieurs écoutes, ou quelque chose d’inattendu sur le port `443`.
4. Sur l’**appliance**, lisez seulement les métadonnées du certificat, de la clé et du marqueur configurés. Pour les chemins livrés, ces commandes en lecture seule affichent les permissions des fichiers et les champs du certificat public, sans afficher la clé privée :

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   Si votre configuration utilise d’autres fichiers, utilisez la paire **réellement configurée**. Si un fichier ou le marqueur manque, arrêtez-vous et cherchez pourquoi avant toute mise à jour ou tout redémarrage ; ne générez pas de nouvelle paire. Gardez la clé privée et la configuration complète hors des captures d’écran, des journaux et des issues.
5. Depuis un **client autorisé**, ouvrez la vraie adresse HTTPS et reconnectez-vous dans une nouvelle session de navigateur.
6. Si OpenSSL est disponible et que le responsable vous a fourni la chaîne de confiance, lancez `openssl s_client -connect <nom>:<port> -servername <nom> -verify_hostname <nom> -verify_return_error -brief </dev/null` avec le vrai nom DNS et le vrai port. Pour une CA privée, ajoutez le `-CAfile <chemin-ca>` approuvé par le responsable. Vérifiez la version d’OpenSSL installée avant d’utiliser ces options.
7. Comparez l’empreinte, le nom, la chaîne et la date d’expiration du certificat avec le point d’accès attendu.

**Vérification :** vous avez noté le certificat que reçoit le navigateur, et les fichiers dont il provient. Le certificat auto-signé créé à l’installation peut échouer à la vérification de confiance : notez ce résultat, mais ne désactivez pas la vérification et ne déclarez pas le certificat fiable. Si un proxy gère TLS, son certificat peut différer du fichier de l’appliance ; notez les deux séparément.

**Avant de prévoir un remplacement**, convenez avec les responsables du certificat et de l’appliance :

- de la nouvelle chaîne de certificats, de la clé privée correspondante, des noms couverts et de la date d’expiration ;
- du stockage sécurisé, du propriétaire et des permissions des fichiers ;
- d’une console de secours séparée, et d’une sauvegarde privée de la **paire de certificats, du marqueur et du fichier opérateur** actuels ;
- d’une fenêtre de maintenance après la fin des jobs, de l’écoute ou du proxy exact à modifier, et d’une procédure de redémarrage et de retour arrière testée ;
- des tests à faire ensuite : une nouvelle connexion de navigateur de confiance, la bonne empreinte, un administrateur local qui fonctionne, la liste des hôtes et des pools, et la console.

Un fichier de configuration valide, des fichiers en place ou un redémarrage réussi ne prouvent pas que les clients font confiance au certificat, ni que c’est le bon. Le renouvellement du certificat n’est pas traité ici : n’utilisez pas ce contrôle comme procédure de remplacement en production.

## Vérifier la syntaxe et redémarrer le service {#apply-change}

**Avant de commencer**

- Gardez une copie privée du fichier opérateur d’origine en dehors de l’appliance, et notez ses permissions.
- Préparez l’accès console.
- Attendez la fin des jobs de sauvegarde, de restauration et de gestion.

Après avoir modifié le fichier, lancez ce contrôle dans l’appliance, en root :

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` signifie seulement que la syntaxe est valide. Cela ne vérifie ni les permissions des fichiers, ni la confiance TLS, ni les valeurs fusionnées, ni l’accessibilité. Corrigez toute erreur avant de redémarrer.

Dans la fenêtre de maintenance convenue, redémarrez le service et lisez son état et son journal récent :

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

Le redémarrage déconnecte l’interface web. Reconnectez-vous à l’adresse attendue.

**Vérification :** vous pouvez vous connecter et la liste des hôtes est complète. XO écrit son URL dans chaque pool à intervalle régulier : vérifiez la découverte des pools après la prochaine mise à jour de cette information.

Si le service ne démarre pas, restaurez le fichier opérateur sauvegardé depuis la console, vérifiez de nouveau sa syntaxe et redémarrez une fois. Si le résultat n’est pas clair, consultez le [dépannage](/docs/xoa-hl/troubleshooting/). Retirez les secrets des journaux avant de les partager.

{{< details title="Sources" closed="true" >}}
- **Fichiers de configuration et service** : [script d’installation initiale](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [installation et mise à jour du paquet](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [service systemd](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [chargement de la configuration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [valeurs par défaut](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [exemple commenté](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [découverte des pools](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).
- **Accès de gestion** : [connexion au serveur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [proxy de console vers l’hôte de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **Certificat HTTPS** : [paire générée, marqueur et redémarrage après une mise à jour](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [écoute initiale](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [mise en place de l’écoute effective](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [manuel OpenSSL x509](https://docs.openssl.org/3.0/man1/openssl-x509/), [manuel OpenSSL s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/).
{{< /details >}}
