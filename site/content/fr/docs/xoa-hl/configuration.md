---
title: Configurer le service de l’appliance
description: Localiser la configuration opérateur et préparer une modification vérifiée.
weight: 71
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:968057a7d1a41033c98ff1ff829858fec7d897e9c34b4151899d6bd7b7f814eb
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
