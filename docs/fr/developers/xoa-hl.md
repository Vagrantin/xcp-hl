---
layout: default
title: xoa-hl
parent: Développeurs
grand_parent: Français
nav_order: 4
lang: fr
---

# xoa-hl
{: .no_toc }

Build du logiciel XOA-HL : modifie Xen Orchestra pour un usage en homelab et
l'empaquette en archive + RPM léger.
{: .fs-6 .fw-300 }

**Dépôt :** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· Langage : Bash / spec RPM · Licence : AGPL-3.0

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectif

Ce dépôt construit **Xen Orchestra HomeLab Edition** (XOA-HL) : le serveur
open source complet [`xen-orchestra`](https://github.com/vatesfr/xen-orchestra)
et l'interface web XO 5, récupérés à un commit amont figé, modifiés pour un
usage en homelab et empaquetés pour XCP-ng. Chaque build publie deux artefacts
dans une release GitHub :

| Artefact | Contenu |
|---|---|
| `xoa-hl-<version>.tar.gz` | Le monodépôt xen-orchestra élagué et déjà construit |
| `xoa-hl-<version>-1.*.noarch.rpm` | RPM d'installation léger qui récupère l'archive au moment de l'installation |

C'est ce RPM que [`build-xoa-hl`](build-xoa-hl.html) installe dans l'appliance
VM XOA.

---

## Structure du dépôt

```
xoa-hl/
├── container/
│   └── Containerfile           ← image de build AlmaLinux 9 (Node 24, yarn, outillage rpm)
├── scripts/
│   └── build-xo.sh             ← le build : récupération + correctifs + yarn build + tar
├── patches/
│   └── menu-hide-items.patch   ← masque les entrées de menu réservées aux abonnements Vates
├── SPECS/
│   └── xoa-hl.spec             ← RPM noarch léger (télécharge l'archive dans %post)
├── SOURCES/
│   └── xo-server.service       ← unité systemd qui lance xo-server depuis /opt/xo
└── .github/workflows/
    └── build-xoa.yml           ← CI : archive + RPM + release GitHub
```

---

## Version figée

Le build vise un commit amont fixe, défini en tête de
`scripts/build-xo.sh` :

```bash
XO_REPO="https://github.com/vatesfr/xen-orchestra.git"
XO_COMMIT="e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c" # 5.113.2, dernière version XO 5.x
XO_VERSION="5.113.2"
```

La chaîne de version de la release combine les deux :
`<XO_VERSION>_<SHA court>` → par exemple `5.113.2_e281c536`. Elle est écrite
dans `out/VERSION`, que la CI lit pour nommer l'archive, le RPM et le tag de
release (`v<version>`).

{: .note }
L'amont est relevé **délibérément**, en modifiant `XO_COMMIT`/`XO_VERSION`,
jamais automatiquement. `5.113.2` est la dernière version XO 5.x avant que
l'amont ne passe à XO 6.

---

## Déroulement du build, scripts/build-xo.sh

Le build s'exécute dans le conteneur AlmaLinux 9 et travaille dans `/build` :

1. **Récupération superficielle au SHA figé**, `git init` +
   `git fetch --depth 1 origin $XO_COMMIT` + `checkout FETCH_HEAD`. Figer un
   SHA nu avec `--depth 1` évite de récupérer l'historique complet (~1 Go)
   tout en restant reproductible.
2. **Application des correctifs**, chaque `patches/*.patch` est appliqué avec
   `git apply --verbose`. Il n'y en a qu'un pour l'instant :
   `menu-hide-items.patch` (masque les entrées de menu qui ne fonctionnent
   qu'avec un abonnement Vates).
3. **Écriture de `packages/xo-server/xoahl.config.toml`**, la configuration
   d'exécution que le RPM installera ensuite comme configuration utilisateur :
   HTTPS sur le port 443 avec `/opt/xo/xoahl.crt` / `/opt/xo/xoahl.key`, Redis
   sur `redis://127.0.0.1:6379/0`.
4. **Génération d'un certificat TLS auto-signé**, `openssl req -x509`
   (RSA 4096, 10 ans, CN `xoa.local`) → `xoahl.key` (mode 600) et
   `xoahl.crt` (mode 644), livrés dans l'archive.
5. **Installation et build**, `yarn` puis `yarn build` sur tous les
   workspaces (serveur et interface web XO 5).
6. **Élagage**, suppression de `.git`, `.github`, `.changesets`, `docs`,
   `packages/xo-server-test*`, `packages/xo-server-cloud`.
7. **Retrait des devDependencies**, `yarn workspaces focus --production`
   (repli : `yarn install --production`), en préservant les liens symboliques
   des workspaces.
8. **Empaquetage**, `tar czf out/xoa-hl-<version>.tar.gz` de tout le monodépôt
   élagué, en excluant `**/*.map`.

---

## Le RPM léger, SPECS/xoa-hl.spec

Le RPM est volontairement léger : `%files` ne livre **que**
`/usr/lib/systemd/system/xo-server.service`. Tout le reste se passe dans
`%post`, au moment de l'installation :

1. Télécharger l'archive de la release depuis
   `https://github.com/Vagrantin/xoa-hl/releases/download/v<version>/…`
   et l'extraire dans `/opt/xo`.
2. Déplacer la clé et le certificat TLS vers `/opt/xo/xoahl.key` /
   `/opt/xo/xoahl.crt` (les chemins référencés par la configuration).
3. **Initialiser la configuration utilisateur à la première installation
   uniquement**, en copiant `xoahl.config.toml` vers
   `/root/.config/xo-server/config.toml` si ce fichier n'existe pas. Lors
   d'une mise à jour, il est laissé intact pour préserver les personnalisations
   de l'exploitant.
4. Exposer `xo-cli` dans le `PATH` (lien symbolique vers
   `/usr/local/bin/xo-cli`).
5. `systemctl enable redis --now`, puis activer et démarrer `xo-server`.

`%preun` arrête et désactive `xo-server` ; `%postun` supprime le lien
symbolique `xo-cli` et `/opt/xo`.

{: .important }
xo-server lit `~/.config/xo-server/config.toml` (recherche XDG), qui prend le
pas sur tout `config.toml` fourni par le paquet. Sans l'initialisation faite
dans `%post`, l'écoute HTTPS et l'URI Redis ne seraient pas appliquées, quel
que soit le contenu de l'archive.

Dépendances à l'exécution : `nodejs >= 24`, `redis`, `curl`, ainsi que les
utilitaires de montage dont Xen Orchestra a besoin pour les *remotes*
(`nfs-utils`, `cifs-utils`, `ntfs-3g`, `lvm2`).

---

## Environnement de build

`container/Containerfile` définit l'image de build : AlmaLinux 9 avec
gcc/make/git/patch, Python 3, Node.js 24 (NodeSource), yarn, ainsi que
`rpm-build`/`rpmdevtools`. La même image construit l'archive et le RPM.

Les builds s'exécutent **exclusivement sur GitHub Actions**, il n'existe pas
de procédure de build local. La CI construit l'image avec Docker à chaque push
et lance `build-xo.sh` à l'intérieur ; l'archive et le fichier `VERSION`
arrivent dans `out/` sur le runner et sont publiés comme artefacts de release.

---

## Workflow de CI (GitHub Actions)

`.github/workflows/build-xoa.yml` se déclenche sur `push` et
`workflow_dispatch` :

1. Construire l'image du conteneur et y lancer `build-xo.sh` (en montant
   `patches/`, `scripts/` et `out/`).
2. Lire `out/VERSION` pour en déduire la chaîne de version.
3. Lancer `rpmbuild -bb SPECS/xoa-hl.spec` dans la même image, avec
   `_version` défini à partir de cette chaîne.
4. Publier une release GitHub taguée `v<version>` contenant l'archive et le
   RPM noarch.

Les **releases d'images de VM** créées par le `xoa-vm-agent` de
l'orchestrateur (préfixe de tag `xoa-image-`, artefact `xoa-almalinux.xva`)
sont publiées sur [`build-xoa-hl`](build-xoa-hl.html), le dépôt qui construit
l'image, voir [#22](https://github.com/Vagrantin/xcp-hl/issues/22).

{: .warning }
Les releases d'images publiées avant ce déplacement sont toujours là, et y
sont conservées pour que les ISO déjà livrées continuent de les résoudre. Les
outils qui parcourent ce dépôt à la recherche du RPM doivent donc toujours
ignorer les tags `xoa-image-*` : `releases/latest` pointe actuellement vers
l'un d'eux.

{: .note }
L'archive doit être publiée sur la release **avant** que le RPM ne soit
installé où que ce soit : le `%post` du RPM la télécharge depuis cette URL de
release même.

---

## Relation avec les autres composants

- [`build-xoa-hl`](build-xoa-hl.html), installe ce RPM dans l'appliance
  AlmaLinux 9 et l'empaquette en image XVA.
- [`xolite-ce`](xolite-ce.html), le bouton de déploiement de XO Lite installe
  cette appliance.
- [`xoa-proxy`](xoa-proxy.html), passerelle HTTPS/gzip utilisée pendant la
  livraison de l'image de l'appliance.
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
  (dans le dépôt `buildorchestration`), dont le `xoa-vm-agent` déclenche
  `build-xoa.yml` et attend la release du RPM avant de lancer le build de
  l'image de VM.

---

## Contribuer

Pour signaler un problème ou proposer une modification, ouvrez un ticket sur
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).

Aujourd'hui, le build est pris en charge par l'orchestrateur
[`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator),
un sous-répertoire du dépôt `buildorchestration` : son `xoa-vm-agent`
déclenche `build-xoa.yml` et consomme la release qui en résulte.
