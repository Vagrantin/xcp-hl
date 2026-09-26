---
title: xoa-hl
weight: 4
translationKey: xoa-hl
aliases: ["/fr/developers/xoa-hl.html"]
---

Build du logiciel XOA-hl : modifie Xen Orchestra pour un usage en homelab et
l'empaquette en RPM.
{class="lead"}

**Dépôt :** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· Langage : Bash / spec RPM · Licence : AGPL-3.0

## Objectif

Ce dépôt construit **Xen Orchestra HomeLab Edition** (XOA-hl) : le serveur
open source complet [`xen-orchestra`](https://github.com/vatesfr/xen-orchestra)
et l'interface web XO 5, récupérés à un commit amont figé, modifiés pour un
usage en homelab et empaquetés pour XCP-ng. Chaque build publie un seul
artefact dans une release GitHub :

| Artefact | Contenu |
|---|---|
| `xoa-hl-<version>-<N>.g<commit>.xcpng8.3.el9.x86_64.rpm` | Xen Orchestra déjà construit (environ 70 Mio), ses unités systemd et l'outillage de mise à jour de l'appliance |

C'est ce RPM que [`build-xoa-hl`](/docs/components/build-xoa-hl) installe dans l'appliance
VM XOA. Les cinq releases les plus récentes sont aussi republiées sous forme
de dépôt yum signé, d'où une appliance en fonctionnement tire ses mises à jour
(voir [Mises à jour](/docs/guides/updates)).

---

## Structure du dépôt

```
xoa-hl/
├── UPSTREAM_XO                 ← version amont figée de xen-orchestra (commit + version)
├── container/
│   └── Containerfile           ← image de build AlmaLinux 9 (Node 24, yarn, outillage rpm)
├── scripts/
│   ├── build-xo.sh             ← le build : récupération + correctifs + yarn build + tar
│   └── validate-patches.sh     ← vérifie patches/ par rapport à metadata.toml
├── patches/
│   ├── metadata.toml           ← rôle de chaque correctif et fichier qu'il modifie
│   ├── menu-hide-items.patch   ← masque les entrées de menu réservées aux abonnements Vates
│   ├── xcp-hl-updates.patch    ← ajoute les dépôts XCP-hl à l'onglet Patches
│   └── xoa-hl-update-api.patch ← la page de réglages « XOA-HL Updates » de l'appliance
├── SPECS/
│   └── xoa-hl.spec             ← le RPM : XO déjà construit dans /opt/xo + unités systemd
├── SOURCES/                    ← unités systemd, scripts de mise à jour, règle sudoers, fichier .repo
├── pages/                      ← page d'index + fichier .repo du dépôt yum publié
└── .github/workflows/
    ├── build-xoa.yml           ← CI : build + RPM + release GitHub
    └── pages-repo.yml          ← republie les RPM récents en dépôt yum signé
```

---

## Version figée

Le build vise un commit amont fixe, défini dans le fichier `UPSTREAM_XO` à la
racine du dépôt :

```bash
XO_COMMIT=e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c
XO_VERSION=5.113.2
```

La chaîne de version combine les deux :
`<XO_VERSION>_<SHA court>` → par exemple `5.113.2_e281c536`. `build-xo.sh`
l'écrit dans `out/VERSION`, et la CI s'en sert comme version du RPM. Une
release se crée en poussant un tag `v<version>-ce<N>`, par exemple
`v5.113.2_e281c536-ce17` : `N` devient le numéro de release du RPM, si bien
que chaque build est un paquet distinct vers lequel `dnf` peut mettre à jour.

{{< callout type="info" >}}
L'amont est relevé **délibérément**, en modifiant `UPSTREAM_XO`, jamais
automatiquement. `5.113.2` est la dernière version XO 5.x avant que l'amont
ne passe à XO 6.
{{< /callout >}}

---

## Déroulement du build, scripts/build-xo.sh

Le build s'exécute dans le conteneur AlmaLinux 9 et travaille dans `/build` :

1. **Récupération superficielle au SHA figé**, `git init` +
   `git fetch --depth 1 origin $XO_COMMIT` + `checkout FETCH_HEAD`. Figer un
   SHA nu avec `--depth 1` évite de récupérer l'historique complet (~1 Go)
   tout en restant reproductible.
2. **Application des correctifs**, après avoir vérifié que chaque
   `patches/*.patch` a une entrée dans `patches/metadata.toml` et
   inversement, chaque correctif est appliqué avec `git apply --verbose`. Il
   y en a trois :
   - `menu-hide-items`, masque les entrées de menu qui ne fonctionnent
     qu'avec un abonnement Vates.
   - `xcp-hl-updates`, ajoute les dépôts XCP-hl à la requête que Xen
     Orchestra envoie au plugin `updater.py` de l'hôte, pour que les paquets
     XCP-hl apparaissent dans l'onglet Patches.
   - `xoa-hl-update-api`, ajoute l'API de mise à jour propre à l'appliance
     et la page de réglages **XOA-HL Updates**.
3. **Écriture de `packages/xo-server/xoahl.config.toml`**, la configuration
   d'exécution que le RPM installera ensuite comme configuration utilisateur :
   HTTPS sur le port 443 avec `/opt/xo/xoahl.crt` / `/opt/xo/xoahl.key`, Redis
   sur `redis://127.0.0.1:6379/0`.
4. **Génération d'un certificat TLS auto-signé**, `openssl req -x509`
   (RSA 4096, 10 ans, CN `xoa.local`) → `xoahl.key` (mode 600) et
   `xoahl.crt` (mode 644).
5. **Installation et build**, `yarn` puis `yarn build` sur tous les
   workspaces (serveur et interface web XO 5).
6. **Élagage**, suppression de `.git`, `.github`, `.changesets`, `docs`,
   `packages/xo-server-test*`, `packages/xo-server-cloud`.
7. **Retrait des devDependencies**, `yarn workspaces focus --production`
   (repli : `yarn install --production`), en préservant les liens symboliques
   des workspaces.
8. **Empaquetage**, `tar czf out/xoa-hl-<version>.tar.gz` de tout le monodépôt
   élagué, en excluant `**/*.map`. L'archive sert uniquement d'entrée au build
   du RPM, elle n'est pas publiée.

---

## Le RPM, SPECS/xoa-hl.spec

Le RPM livre Xen Orchestra déjà construit, environ 70 Mio. Il est `x86_64` et
non `noarch`, car l'arborescence `node_modules` contient des modules natifs.
Il installe :

| Chemin | Rôle |
|---|---|
| `/opt/xo` | L'arborescence xen-orchestra déjà construite, plus la paire TLS `xoahl.key` / `xoahl.crt` |
| `/usr/local/bin/xo-cli` | `xo-cli` dans le `PATH` |
| `/usr/lib/systemd/system/xo-server.service` | Lance xo-server depuis `/opt/xo` |
| `/usr/lib/systemd/system/xoa-hl-check-update.service` et `xoa-hl-update.service` | Recherchent et appliquent les mises à jour de l'appliance |
| `/usr/libexec/xoa-hl/` | Les scripts lancés par ces deux unités |
| `/etc/yum.repos.d/xoa-hl.repo` | Le dépôt yum propre à l'appliance |
| `/etc/sudoers.d/xoa-hl` | Autorise xo-server à démarrer les deux unités de mise à jour |
| `/var/lib/xoa-hl/` | L'emplacement du journal de mise à jour |

Au moment de l'installation, `%post` :

1. **Initialise la configuration utilisateur à la première installation
   uniquement**, en copiant `xoahl.config.toml` vers
   `/root/.config/xo-server/config.toml` si ce fichier n'existe pas. Lors
   d'une mise à jour, il est laissé intact pour préserver les personnalisations
   de l'exploitant.
2. Lance `systemctl enable redis --now`, puis active et redémarre
   `xo-server`.

`%preun` arrête et désactive `xo-server` uniquement lors de la
désinstallation finale, pas lors d'une mise à jour. Tous les fichiers
ci-dessus appartiennent au paquet, `dnf remove` les supprime donc tous ;
`%postun` se contente de recharger systemd.

{{< callout type="error" >}}
xo-server lit `~/.config/xo-server/config.toml` (recherche XDG), qui prend le
pas sur tout `config.toml` fourni par le paquet. Sans l'initialisation faite
dans `%post`, l'écoute HTTPS et l'URI Redis ne seraient pas appliquées, quel
que soit le contenu du paquet.
{{< /callout >}}

Dépendances à l'exécution : `nodejs >= 24`, `redis`, ainsi que les
utilitaires de montage dont Xen Orchestra a besoin pour les *remotes*
(`nfs-utils`, `cifs-utils`, `ntfs-3g`, `lvm2`). Le paquet porte `Epoch: 1`,
ce qui le place au-dessus des builds antérieurs au schéma de numérotation
actuel.

---

## Environnement de build

`container/Containerfile` définit l'image de build : AlmaLinux 9 avec
gcc/make/git/patch, Python 3, Node.js 24 (NodeSource), yarn, ainsi que
`rpm-build`/`rpmdevtools`. La même image construit l'archive et le RPM.

Les builds s'exécutent **exclusivement sur GitHub Actions**, il n'existe pas
de procédure de build local. La CI construit l'image avec Docker et lance
`build-xo.sh` à l'intérieur ; l'archive et le fichier `VERSION` arrivent dans
`out/` sur le runner et alimentent le build du RPM.

---

## Workflow de CI (GitHub Actions)

`.github/workflows/build-xoa.yml` se déclenche sur la publication d'un tag
`v*-ce<N>` et sur `workflow_dispatch` :

1. Vérifier la syntaxe de chaque script shell : `scripts/*.sh` avec `bash`,
   et les scripts `SOURCES/*.sh` livrés dans le RPM avec `sh`.
2. Construire l'image du conteneur et y lancer `build-xo.sh` (en montant
   `patches/`, `scripts/`, `out/` et `UPSTREAM_XO`).
3. Lire `out/VERSION`, et prendre `N` dans le tag comme numéro de release du
   RPM.
4. Lancer `rpmbuild -bb SPECS/xoa-hl.spec` dans la même image, avec l'archive
   placée dans `SOURCES/`.
5. Publier une release GitHub, nommée d'après le tag, contenant le RPM.

Après chaque build réussi, `.github/workflows/pages-repo.yml` rassemble les
RPM des cinq releases les plus récentes et les publie, avec des métadonnées
signées, comme dépôt yum sur
`https://vagrantin.github.io/xoa-hl/8.3/x86_64/`. C'est vers ce dépôt que
pointe le `xoa-hl.repo` de l'appliance.

Les **releases d'images de VM** créées par le `xoa-vm-agent` de
l'orchestrateur (préfixe de tag `xoa-image-`, artefact `XOA-hl.xva`)
sont publiées sur [`build-xoa-hl`](/docs/components/build-xoa-hl), le dépôt qui construit
l'image, voir [#22](https://github.com/Vagrantin/xcp-hl/issues/22).

{{< callout type="warning" >}}
Les releases d'images publiées avant ce déplacement sont toujours là, et y
sont conservées pour que les ISO déjà livrées continuent de les résoudre. Les
outils qui parcourent ce dépôt à la recherche du RPM doivent donc toujours
ignorer les tags `xoa-image-*`.
{{< /callout >}}

---

## Relation avec les autres composants

- [`build-xoa-hl`](/docs/components/build-xoa-hl), installe ce RPM dans l'appliance
  AlmaLinux 9 et l'empaquette en image XVA.
- [`xolite-ce`](/docs/components/xolite-ce), le bouton de déploiement de XO Lite installe
  cette appliance.
- [`xoa-proxy`](/docs/components/xoa-proxy), passerelle HTTPS/gzip utilisée pendant la
  livraison de l'image de l'appliance.
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
  (dans le dépôt `buildorchestration`), dont le `xoa-vm-agent` déclenche
  `build-xoa.yml` et attend la release du RPM avant de lancer le build de
  l'image de VM.

---

## Contribuer

Pour signaler un problème ou proposer une modification, ouvrez un ticket sur
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
