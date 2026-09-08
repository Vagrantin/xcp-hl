---
layout: default
title: xolite-ce
parent: Développeurs
grand_parent: Français
nav_order: 2
lang: fr
---

# xolite-ce
{: .no_toc }

Correctif communautaire pour XO Lite et chaîne de build du RPM.
{: .fs-6 .fw-300 }

**Dépôt :** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Langage : TypeScript / Vue 3 (correctif) · spec RPM · Licence : AGPL-3.0

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Qu'est-ce que XO Lite ?

XO Lite est l'application de gestion légère, en page unique, fournie avec
chaque hôte XCP-ng. Elle s'exécute entièrement dans le navigateur — servie
directement par l'hôte — et se présente sous la forme d'une SPA
Vue 3 / TypeScript / Vite.

Sur un hôte XCP-ng standard, XO Lite comprend un écran **« Deploy XOA »**
(`DeployXoaView.vue`) qui télécharge et importe l'image Xen Orchestra
officielle. XCP-ng HL remplace ce comportement pour vous laisser choisir
l'image XOA que vous souhaitez déployer.

---

## Le correctif

La modification communautaire tient dans un seul fichier
**`git format-patch`** :

```
xolite-ce/
└── patches/
    └── community-xoa-deploy.patch
```

Le correctif ne modifie que `DeployXoaView.vue`. Il :

  - **liste déroulante « XOA Image URL »** proposant trois options :
  - **image XOA pour homelab** *(par défaut)* — passe par `xoa-proxy` pour la
    diffusion en flux continu et la décompression gzip ; les identifiants sont
    pré-remplis
  - **image Vates** — utilise directement l'URL officielle hébergée par
    Vates ; XAPI l'importe sans passer par `xoa-proxy`
  - **URL personnalisée** — passe par `xoa-proxy` ; les champs d'identifiants
    sont laissés vides, à remplir par l'utilisateur

- Ajoute un interrupteur **« Verify if SSL certificate is valid »** qui, une
  fois désactivé, permet à `xoa-proxy` d'accepter les certificats auto-signés
  du serveur d'images en amont.

- Les champs d'identifiants sont **en lecture seule quand l'image de Ronivay
  est sélectionnée** (valeurs par défaut pré-remplies) et **modifiables pour
  toutes les autres options**.

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
8. rpmsign avec la sous-clé de signature RPM (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
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

Le RPM `xo-lite-community` est signé avec la **sous-clé de signature RPM** de
la paire de clés XCP-ng Community Edition. La même sous-clé sert aussi à
signer le RPM `xoa-proxy` : il n'y a qu'une sous-clé partagée pour tous les
RPM communautaires.

La clé publique (`xcp-ng-ce-public.asc`) est le même fichier que celui
distribué avec chaque release. Il suffit de l'importer une fois pour vérifier
n'importe quel RPM communautaire.

Pour vérifier le RPM en local :

```bash
# Option 1 — récupérer la clé depuis le serveur de clés
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# Option 2 — importer la clé depuis la page de release
gpg --import xcp-ng-ce-public.asc

# Vérifier la signature du RPM
rpm --checksig xo-lite-community-*.rpm
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

1. Forkez [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce).
2. Pour modifier le correctif d'interface : éditez
   `patches/community-xoa-deploy.patch`.
3. Pour modifier l'empaquetage : éditez `SPECS/xo-lite-community.spec`.
4. Déroulez le processus de développement local ci-dessus pour vérifier vos
   modifications.
5. Ouvrez une pull request sur `main`.
