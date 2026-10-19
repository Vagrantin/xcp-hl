---
title: "Configurer le service de l’appliance"
linkTitle: "Paramètres du service"
description: "Trouvez les fichiers de configuration, vérifiez les accès et le certificat, et appliquez une modification sans risque."
weight: 91
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:ba4a7450e3edaab0d44d601a5d06d8ccfaaa4026f7bdf8cda0d283847e6533f4
glossaryTerms: ["appliance", "host", "pool"]
---

Configurez xo-server séparément des réglages et données exportés depuis l’interface web.

{{< callout type="info" >}}
Référence vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les versions suivantes peuvent différer. La validation sur appliance installée et la revue humaine des traductions restent à faire.
{{< /callout >}}

## Localiser les réglages

| Emplacement | Rôle à ce38 | Précaution |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` et `sample.config.toml` | Valeurs par défaut du paquet et référence commentée | Consulter comme références ; les mises à jour remplacent ces fichiers du paquet |
| `/root/.config/xo-server/config.toml` | Configuration opérateur initialisée uniquement si absente | Sauvegarder en privé avant modification ; préservée par l’initialisation RPM |
| `/root/.config/xo-server/config.z-auto.json` | Réglages écrits par le serveur | Vérifier sa présence en recherchant les surcharges ; ne pas écraser aveuglément |
| Base Redis | Données de l’application XO | Respecter le périmètre documenté de l’export/import web |
| `/etc/xoa-hl/update.conf` | Mode, calendrier et canal de l’updater HomeLab | Préférer Settings → XOA-HL Updates et le guide des mises à jour |
| `/opt/xo/xoahl.crt` et `xoahl.key` | Certificat TLS et clé privée de l’appliance | Conserver séparément ; ne jamais joindre la clé privée à un rapport |

L’unité systemd du paquet s’exécute en root et utilise la configuration utilisateur XDG. Le chargeur accepte aussi `/etc/xo-server/config.*` et les fichiers locaux `.xo-server.*` ; plusieurs fichiers peuvent fusionner. Vérifiez les surcharges de l’unité et les autres fichiers avant de conclure quelle valeur s’applique. Cette page décrit l’unité livrée, pas un compte de service personnalisé.

L’[export de configuration](/docs/xoa-hl/configuration-backup/) n’inclut pas le TOML opérateur, les fichiers TLS ni la configuration de l’updater. Consultez la [maintenance](/docs/xoa-hl/maintenance/) et les [mises à jour](/docs/guides/updates/) pour ces changements.

## Exemple : annoncer l’URL de l’appliance

`http.publicUrl` fournit l’URL utilisée pour la découverte du pool. Cette option ne crée ni écoute réseau, ni certificat, ni enregistrement DNS. Choisissez une URL HTTPS réelle de l’appliance avec DNS correspondant et certificat de confiance ; vérifiez d’abord l’accès par navigateur. Lisez le [guide de gestion et de découverte](/docs/xoa-hl/hosts-pools/) avant de la modifier.

Dans un laboratoire jetable, ajoutez la propriété à la table `[http]` **existante**. Cet exemple minimal conserve l’écoute HTTPS et l’URI Redis livrées ; il ne remplace pas un fichier personnalisé :

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

N’ajoutez pas une autre table `[http]` et ne supprimez pas l’écoute existante. Gardez les vrais chemins du certificat et de la clé. Le RPM génère la paire auto-signée initiale à l’installation ; il ne distribue pas de clé partagée. Une clé/un certificat manquant ou l’absence du marqueur `/var/lib/xoa-hl/tls-generated` provoquent une génération : relevez l’état TLS installé avant une mise à jour. Le remplacement du certificat, les reverse proxies et la migration Redis nécessitent leurs propres tests.

## Cartographier l’accès de gestion avant l’isolation {#management-network}

Ce **contrôle SE07 en lecture seule, vérifié dans les sources**, concerne l’image ce38 indiquée plus haut. Le bootstrap fourni configure une écoute HTTPS sur le port `443` ; une configuration locale, un proxy, un pare-feu ou une autre image peuvent modifier le chemin réel. L’interface ne définit pas de règles de pare-feu universelles. Avant toute modification d’ACL, VIF, PIF de gestion ou politique de commutateur, convenez avec les responsables réseau et hôte des clients, sous-réseaux, services et destinations de sauvegarde autorisés ainsi que de l’accès console indépendant.

| Chemin à identifier | Lecture et limite |
| --- | --- |
| Navigateur autorisé → XOA-HL | Notez la VM et l’adresse de l’appliance, le nom résolu, le point d’accès HTTPS réel et l’identité du certificat. Vérifiez une nouvelle connexion et l’inventaire des hôtes depuis un client autorisé. L’écoute livrée est `443`, mais inspectez la configuration installée et le point d’accès effectif ; `http.publicUrl` publie une adresse et n’ouvre pas de port. |
| XOA-HL → hôte/pool géré | Dans **Settings → Servers**, notez l’adresse du serveur connecté, les ID du pool/des hôtes et la gestion du certificat. Vérifiez l’inventaire actuel et, si ce test a déjà été accepté dans le laboratoire, des [statistiques d’hôte](/docs/xoa-hl/hosts-pools/#host-statistics) récentes en lecture seule. La connexion du navigateur ne prouve pas l’accès à l’hôte. |
| Navigateur → console via XOA-HL → hôte résident | Si la console est nécessaire, ouvrez celle d’une VM jetable en fonctionnement en suivant le [guide de console](/docs/xoa-hl/vm-operations/#vm-console) et notez le résultat côté navigateur et l’hôte résident. Le proxy de console épinglé établit un chemin WebSocket distinct entre l’appliance et l’hôte ; un inventaire réussi ne le prouve pas. |
| XOA-HL → destinations et mises à jour | Recensez chaque destination de sauvegarde et les dépendances paquets/DNS/temps de l’appliance avec leurs responsables. Testez une destination par sa [procédure de sauvegarde](/docs/xoa-hl/backup-restore/) et l’accès aux paquets par le [guide de mise à jour](/docs/xoa-hl/maintenance/) ; ne généralisez pas depuis l’accès web. |

Dans un **laboratoire jetable dont la version est identifiée**, relevez client source, nom/adresse cible, service, résultat et heure pour chaque chemin nécessaire. Demandez au responsable réseau de vérifier qu’un client de test explicitement non autorisé ne peut pas accéder à la connexion web, au moyen d’un test permis et de journaux indépendants ; un ping bloqué ne prouve ni l’isolation HTTPS ni la disponibilité de la gestion. Conservez une console indépendante du chemin à restreindre. Si une modification de politique est approuvée séparément, changez une seule règle gérée par son responsable à la fois, répétez les mêmes tests de service autorisés et refusés, puis vérifiez connexion, inventaire, console et sauvegardes avant la fin de la fenêtre. Si un chemin requis échoue ou si l’accès est perdu, arrêtez et utilisez le retour arrière documenté du responsable réseau depuis la console indépendante ; ne retirez pas la connexion XOA et ne changez pas le PIF de gestion de l’hôte comme raccourci.

Aucune appliance, aucun hôte ou pare-feu n’a été modifié lors de cette revue de sources. L’écoute réelle, la segmentation des clients, les chemins proxy/NAT, les ports hôtes et destinations, le test négatif, la continuité et le retour arrière restent à valider sur l’installation. N’en déduisez pas une liste d’autorisation pour la production.

## Inventorier le certificat HTTPS avant rotation {#tls-certificate-preflight}

Ce **contrôle préalable SE06 en lecture seule** concerne le code ce38 ci-dessus. L’initialisation écrit une écoute HTTPS sur le port `443` avec `/opt/xo/xoahl.crt` et `/opt/xo/xoahl.key` dans le premier fichier opérateur, mais des réglages ultérieurs ou un proxy inverse peuvent terminer TLS ailleurs. Le RPM ne fournit aucune clé privée commune : à l’installation, il génère une paire autosignée `CN=xoa.local` si l’un des fichiers ou `/var/lib/xoa-hl/tls-generated` manque. Une transaction de paquet ultérieure peut donc régénérer cette paire si le marqueur ou un fichier est absent, et `%posttrans` redémarre `xo-server`. Relevez le chemin et l’état du paquet installés avant de planifier le renouvellement ; ne supprimez jamais le marqueur comme méthode de rotation.

1. Avec une console indépendante et un administrateur local disponibles, déterminez l’image/paquet installés, les valeurs effectives de `http.listen` et les surcharges fusionnées, sans divulguer les secrets. `systemctl cat xo-server` montre les surcharges du service. Notez tout proxy inverse, répartiteur ou terminaison TLS devant l’appliance. `http.publicUrl` annonce une adresse ; il ne prouve ni l’écoute ni le certificat vu par le navigateur. Arrêtez si plusieurs écoutes ou un propriétaire inattendu du port `443` apparaissent.
2. Sur l’**appliance**, examinez seulement les métadonnées du certificat, de la clé et du marqueur configurés. Pour les chemins livrés, ces commandes en lecture seule montrent permissions et champs du certificat public sans afficher la clé privée :

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   Remplacez les chemins par la paire **réellement configurée** si elle diffère. Un fichier ou marqueur absent exige une enquête avant toute mise à jour ou redémarrage ; ne générez pas immédiatement une nouvelle paire. Ne diffusez ni la clé privée ni la configuration complète dans captures, journaux ou issues.
3. Depuis un **client autorisé**, inspectez le véritable point HTTPS et ouvrez une nouvelle session navigateur. Si OpenSSL est disponible et que le responsable a fourni la chaîne de confiance, utilisez le vrai nom DNS et port avec `openssl s_client -connect <nom>:<port> -servername <nom> -verify_hostname <nom> -verify_return_error -brief </dev/null` (ajoutez le `-CAfile <chemin-ca>` approuvé pour une CA privée). Comparez empreinte, nom, chaîne et expiration du certificat présenté avec le point prévu. Le certificat autosigné initial peut échouer à la validation de confiance : consignez ce résultat sans désactiver la vérification ni le déclarer fiable. Si un proxy termine TLS, son certificat peut différer du fichier local ; documentez les deux chemins séparément.
4. Avant toute rotation, faites identifier par les responsables le nouveau certificat et sa chaîne, la clé privée correspondante, les noms visés, l’expiration, le stockage sûr, propriétaire/permissions des fichiers, une console de secours et une copie privée de la **paire, du marqueur et de la configuration opérateur** actuels. Convenez d’une fenêtre après la fin des jobs, de l’écoute ou du proxy exact à modifier, d’une procédure de redémarrage/retour arrière vérifiée, puis des contrôles : nouvelle connexion navigateur fiable, bonne empreinte, administrateur local conservé, inventaire hôtes/pools et console. Une syntaxe valide, des fichiers présents ou un service redémarré ne prouvent pas à eux seuls la confiance client ou l’identité du certificat.

Aucun certificat n’a été renouvelé lors de cette revue des sources. Écoute installée, chaîne de confiance, méthode de renouvellement, correspondance clé/certificat, persistance après mise à jour, interruption et retour arrière restent à valider en laboratoire. N’utilisez pas cet inventaire comme procédure de rotation en production.

## Vérifier la syntaxe et appliquer dans une fenêtre

Conservez une copie privée du fichier opérateur initial hors de l’appliance et relevez ses permissions. Préparez l’accès console et attendez la fin des jobs de sauvegarde, restauration et gestion. Dans l’appliance, en root, lancez le parseur après modification :

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` confirme seulement la syntaxe. Cela ne vérifie ni permissions, ni confiance TLS, ni valeurs fusionnées, ni accessibilité. Le parseur et la fusion documentés ont été testés avec des configurations synthétiques, pas sur une appliance publiée. Corrigez les erreurs avant le redémarrage.

Dans la fenêtre de maintenance convenue, appliquez et vérifiez :

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

Le redémarrage déconnecte l’interface web. Reconnectez-vous à l’adresse attendue, vérifiez l’authentification, l’inventaire des hôtes et la découverte après le prochain marquage. Si le démarrage échoue, restaurez le fichier opérateur sauvegardé via la console, analysez-le de nouveau et redémarrez une fois. Consultez le [dépannage](/docs/xoa-hl/troubleshooting/) si le résultat est incertain. Expurgez les journaux avant de les partager.

## Sources

[bootstrap](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh), [RPM lifecycle](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [service](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service), [configuration loader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [defaults](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [sample](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [pool discovery](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).

Chemins de gestion aux versions épinglées ci-dessus : [connexion au serveur](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [proxy de console vers l’hôte résident](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs). Les ports et l’accessibilité d’une installation particulière nécessitent une observation directe.

Inventaire TLS aux mêmes versions : [paire générée, marqueur et redémarrage après transaction](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [écoute initiale](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh), [mise en place de l’écoute effective](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs). Référence OpenSSL : [inspection x509](https://docs.openssl.org/3.0/man1/openssl-x509/) et [vérification s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/) ; vérifiez la version OpenSSL installée avant d’utiliser les options.
