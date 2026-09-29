---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/fr/developers/xolite-ce.html"]
---

Correctif communautaire pour XO Lite et chaîne de build du RPM.
{class="lead"}

**Dépôt :** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Langage : TypeScript / Vue 3 (correctif) · spec RPM · Licence : AGPL-3.0

## Qu'est-ce que XO Lite ?

XO Lite est l'application de gestion légère, en page unique, fournie avec
chaque hôte XCP-ng. Elle s'exécute entièrement dans le navigateur, servie
directement par l'hôte, et se présente sous la forme d'une SPA
Vue 3 / TypeScript / Vite.

Sur un hôte XCP-ng standard, XO Lite comprend un écran **« Deploy XOA »**
(`DeployXoaView.vue`) qui télécharge et importe l'image Xen Orchestra
officielle. XCP-hl remplace ce comportement pour vous laisser choisir
l'image XOA que vous souhaitez déployer.

---

## Le correctif

Le patch s'appuie sur l'outil Rust `xoa-deploy-patcher`, qui applique à la
construction des modifications par motif à `xoa-deploy.vue`. Il applique aussi
`patches/en-hl.json` (les chaînes de la locale HL) et
`patches/xolite-loader.html` (un loader de remplacement qui supprime le
chargement distant de secours depuis `lite.xen-orchestra.com`).

L'écran **« Deploy XOA »** modifié gagne un sélecteur **« XOA Image URL »** proposant quatre sources :

  - **XOA-hl** *(par défaut)* : Xen Orchestra construit depuis les sources pour XCP-hl
  - **image Vates** : l'appliance officielle
  - **image de Ronivay** : un XO communautaire construit depuis les sources
  - **URL personnalisée** : n'importe quel XVA, brut ou gzippé, en HTTP ou HTTPS

Un interrupteur **« Verify if ssl certificate is valid »** permet à
`xoa-proxy` d'accepter les certificats auto-signés du serveur d'images amont.

---

## Chaîne de build

### Vue d'ensemble

```
1. Lire XO_VERSION depuis le RPM présent dans l'ISO XCP-ng amont
2. Cloner vatesfr/xen-orchestra au tag de release correspondant
3. Appliquer patches/community-xoa-deploy.patch
4. Installer les dépendances avec Yarn (Corepack)
5. Construire XO Lite : yarn build:xo-lite
6. Assembler l'archive des sources du RPM
7. rpmbuild -ba SPECS/xo-lite-community.spec
8. rpmsign avec la signing subkey RPM (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
9. Publier le RPM + xcp-ng-ce-public.asc comme artefacts de release GitHub
```

### Détection de la version

La version cible de XO Lite est lue depuis le RPM déjà présent sur l'ISO
XCP-ng amont, elle n'est pas codée en dur :

```bash
XO_VERSION=$(rpm -qp --qf '%{VERSION}' xo-lite-*.rpm)
```

Cela garantit que le RPM communautaire correspond toujours à la version
amont, ce qui en fait un remplacement direct.

### Structure de l'archive

L'archive des sources transmise à `rpmbuild` a la disposition suivante :

```
xo-lite-{VERSION}/
├── dist/               ← sortie compilée de Vite
├── CHANGELOG.md
├── LICENSE
└── xolite.html         ← renommé depuis scripts/xolite-loader.html
```

Le nom de fichier `xolite.html` est obligatoire : c'est le point d'entrée
servi par l'hôte XCP-ng pour charger XO Lite dans le navigateur.

### Spec RPM

`SPECS/xo-lite-community.spec` définit :

- `Name: xo-lite-community`
- `Version: %{XO_VERSION}` (injectée au moment du build)
- `Provides: xo-lite` (afin de satisfaire toute dépendance envers le paquet
  amont)
- `Conflicts: xo-lite` (empêche la cohabitation avec le RPM amont)
- La liste des fichiers : le contenu de `dist/` + `xolite.html`

---

## Développement en local

### Prérequis

- Node.js 20 ou plus et Yarn (activé via `corepack enable`)
- `rpmbuild` (paquet `rpm-build` sur RHEL/CentOS/Fedora)
- `rpmsign` (paquet `rpm-sign`)
- La clé publique GPG de la communauté importée dans votre trousseau

### Déroulement

```bash
# 1. Cloner le dépôt
git clone https://github.com/Vagrantin/xolite-ce.git
cd xolite-ce

# 2. Cloner xen-orchestra amont au tag cible
XO_VERSION=<version>
git clone --depth 1 --branch v${XO_VERSION} \
    https://github.com/vatesfr/xen-orchestra.git upstream

# 3. Appliquer le correctif communautaire
cd upstream
git am ../patches/community-xoa-deploy.patch
cd ..

# 4. Installer les dépendances
cd upstream
corepack enable
yarn install
cd ..

# 5. Construire XO Lite
cd upstream
yarn build:xo-lite
cd ..

# 6. Tester l'interface
scp -r lite/dist/ hote-xcp-ng:/opt/xensource/www/
```

### Mettre à jour le correctif pour une nouvelle version amont

```bash
# Dans un clone amont neuf, faire les modifications à la main
# puis générer un nouveau correctif :
git diff HEAD > ../patches/community-xoa-deploy.patch
# ou avec format-patch, pour un commit propre :
git format-patch HEAD~1 -o ../patches/
```

---

## Signature GPG

Le RPM `xo-lite-community` est signé avec la **signing subkey RPM** de
la paire de clés XCP-hl. La même sous-clé sert aussi à signer le RPM
`xoa-proxy` : il n'y a qu'une sous-clé partagée pour tous les
RPM communautaires.

Le projet publie sa [clé publique](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc)
à la racine du site de production. Vérifiez l’empreinte de la clé principale avant
de l’importer. Les commandes ci-dessous nécessitent une version de RPM prenant
en charge les sous-clés de signature. Le Dom0 de XCP-ng 8.3 utilise RPM 4.11 ;
les hôtes valident donc les métadonnées signées avec `repo_gpgcheck=1`. Conservez
les paramètres de dépôt décrits dans [Mises à jour](/docs/guides/updates).

Pour vérifier le RPM en local :

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Workflow de CI (GitHub Actions)

Le workflow se déclenche sur un push vers `main`.

Étapes principales :

```yaml
- name: Detect XO version
  run: echo "XO_VERSION=$(rpm -qp --qf '%{VERSION}' ...)" >> $GITHUB_ENV

- name: Clone upstream at tag
  run: git clone --depth 1 --branch v${{ env.XO_VERSION }} ...

- name: Apply patch
  run: git am patches/community-xoa-deploy.patch

- name: Build XO Lite
  run: |
    corepack enable
    yarn install
    yarn build:xo-lite

- name: Build RPM
  run: rpmbuild -ba SPECS/xo-lite-community.spec

- name: Sign RPM
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import
    echo "${{ secrets.GPG_PASSPHRASE }}" | gpg --passphrase-fd 0 --batch \
      --pinentry-mode loopback --yes --armor
    rpm --addsign RPMS/x86_64/xo-lite-community-*.rpm

- name: Publish release
  uses: softprops/action-gh-release@v1
  with:
    files: |
      RPMS/x86_64/xo-lite-community-*.rpm
      xcp-ng-ce-public.asc
```

---

## Contribuer

Pour signaler un problème ou proposer une modification, ouvrez un ticket sur
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
