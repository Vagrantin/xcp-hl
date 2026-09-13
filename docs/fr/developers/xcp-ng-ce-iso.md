---
layout: default
title: xcp-ng-ce-iso
parent: Développeurs
grand_parent: Français
nav_order: 3
lang: fr
---

# xcp-ng-ce-iso
{: .no_toc }

Chaîne d'assemblage de l'ISO — prend les builds RPM de la communauté et publie
une ISO XCP-hl amorçable.
{: .fs-6 .fw-300 }

**Dépôt :** [Vagrantin/xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso)
· Langage : Bash / YAML · Licence : AGPL-3.0

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectif

Ce dépôt prend le RPM signé `xo-lite-ce` produit par
[`xolite-ce`](xolite-ce.html) et le RPM signé `xoa-proxy` produit par
[`xoa-proxy`](xoa-proxy.html), les superpose à une base XCP-ng 8.3 standard à
l'aide de la chaîne d'outils officielle
[`create-install-image`](https://github.com/xcp-ng/create-install-image), et
publie l'ISO obtenue comme release GitHub.

---

## Chaîne d'outils — create-install-image

L'ISO d'installation officielle de XCP-ng est assemblée avec la chaîne
d'outils `create-install-image`. XCP-hl l'utilise directement plutôt que de
maintenir un fork.

Cette chaîne fournit deux scripts :

| Script | S'exécute en tant que | Produit |
|---|---|---|
| `create-installimg.sh` | **root** | `install.img` (ramdisk SquashFS) |
| `create-iso.sh` | non-root | le fichier `.iso` final |

Ils doivent être lancés séparément, dans cet ordre. `create-iso.sh` accepte un
argument `--sign-script` pour le fingerprint MD5.

---

## Structure du dépôt

```
xcp-ng-ce-iso/
├── configs/
│   ├── base/
│   │   └── CUSTOMREPO.tmpl     ← modèle de dépôt communautaire
│   └── 8.3/                    ← configuration XCP-ng 8.3 (cible)
├── community-repo/
│   └── x86_64/
│       └── repodata/           ← généré par createrepo_c
├── scripts/
│   └── debug/                  ← scripts d'aide au débogage (superposés dans la CI)
├── Dockerfile.build             ← environnement de build
└── .github/workflows/
    └── build-iso.yml
```

### CUSTOMREPO.tmpl

Le modèle de définition du dépôt communautaire doit être copié de
`configs/base/` vers `configs/8.3/` avant le lancement du build :

```bash
cp configs/base/CUSTOMREPO.tmpl configs/8.3/CUSTOMREPO.tmpl
```

Ce fichier indique à l'installateur où trouver le dépôt RPM communautaire.
L'option `--define-repo` le transmet aux deux scripts de build.

### Organisation du dépôt RPM communautaire

`yum` ajoute automatiquement l'architecture de l'hôte (`x86_64/`) à l'URL de
base configurée dans un fichier de dépôt. Le dépôt communautaire doit donc
être structuré avec `repodata/` sous le sous-répertoire d'architecture :

```
community-repo/
└── x86_64/
    ├── xo-lite-ce-*.rpm
    ├── xoa-proxy-*.rpm
    ├── xcp-hl-release-*.rpm
    └── repodata/
        ├── repomd.xml
        └── ...
```

Générez les métadonnées du dépôt dans le sous-répertoire d'architecture :

```bash
createrepo_c community-repo/x86_64/
```

---

## Comment les paquets arrivent sur l'hôte installé
{: #how-packages-reach-the-installed-host }

{: .important }
`install.img` est le **ramdisk de l'installateur lui-même**, pas le système de
fichiers de l'hôte installé. Ajouter un paquet à `packages.lst` le place dans
l'environnement de l'installateur, et nulle part ailleurs.

L'hôte installé est construit par `host-installer` à partir du répertoire
`Packages/` de l'ISO ; il installe `xcp-ng-deps` ainsi que la fermeture de
dépendances de ce paquet. Placer un RPM sur le média ne suffit donc pas à lui
seul : si rien dans cette fermeture ne l'exige, il reste inutilisé dans le
dépôt de l'ISO.

Les paquets communautaires arrivent par cette chaîne :

```
xcp-ng-deps
    └── exige xo-lite ──► fourni par xo-lite-ce
                                 ├── exige xoa-proxy
                                 └── exige xcp-hl-release
```

Ce `Requires:` est la seule porte d'entrée. `xcp-hl-release` était autrefois
aussi placé par son nom avec `--extra-packages`, mais cette option ne fait que
déposer un paquet dans le dépôt de l'ISO sans le sélectionner pour
installation : une fois la dépendance en place, elle est devenue redondante et
ne faisait qu'obscurcir le mécanisme réel de livraison du paquet.

Une conséquence utile à connaître : figer une release `xolite-ce` antérieure à
l'ajout du `Requires:` produit une ISO sans `xcp-hl-release`. L'étape de
vérification du build détecte ce cas au lieu de livrer une telle ISO.

Vérification sur un hôte installé depuis l'ISO :

```bash
rpm -q xcp-hl-release
ls /etc/yum.repos.d/xcp-hl.repo
```

---

## Environnement de build Docker

Le build s'exécute dans `xcp-ng-build-env:8.3`, committé sous le nom
`xcp-ng-build-ready` après la configuration initiale :

```bash
# Première exécution : committer l'image préparée
docker run --name xcpng-build xcp-ng/xcp-ng-build-env:8.3 /bin/true
docker commit xcpng-build xcp-ng-build-ready
```

---

## Processus de build — étape par étape

### 1. Préparer le dépôt communautaire

```bash
# Télécharger le RPM signé depuis la dernière release de xolite-ce
gh release download --repo Vagrantin/xolite-ce \
    --pattern "xo-lite-ce-*.rpm" \
    --dir community-repo/x86_64/

# Télécharger le RPM signé depuis la dernière release de xoa-proxy
gh release download --repo Vagrantin/xoa-proxy \
    --pattern "xoa-proxy-*.rpm" \
    --dir community-repo/x86_64/

# Générer les métadonnées du dépôt
createrepo_c community-repo/x86_64/
```

### 2. Injecter la clé publique communautaire dans le chroot de l'installateur

La signing subkey de l'ISO (`GPG_PRIVATE_KEY` dans ce dépôt) est
importée dans le trousseau du runner au début de la chaîne. La moitié
**publique** est ensuite exportée depuis ce trousseau et injectée dans les
modèles de chroot de l'installateur, afin que celui-ci puisse vérifier les
RPM communautaires pendant l'installation sans que l'utilisateur final ait à
importer une clé à la main.

{: .important }
`rpm --import` à l'intérieur d'un conteneur écrit dans la base RPM **du
conteneur**, pas dans la racine d'installation du chroot qui finit dans
`install.img`. Passez toujours `--root` pour viser le bon emplacement.

```bash
# Exporter la clé publique depuis le trousseau du runner
gpg --armor --export "${GPG_KEY_ID}" > /tmp/RPM-GPG-KEY-xcp-ng-ce

# Copier dans le modèle de racine d'installation de la chaîne d'outils
mkdir -p create-install-image/templates/installimg/base/etc/pki/rpm-gpg/
cp /tmp/RPM-GPG-KEY-xcp-ng-ce \
   create-install-image/templates/installimg/base/etc/pki/rpm-gpg/

# Importer dans le chroot de l'installateur au moment du build
rpm --root="${ROOTFS}" --import /etc/pki/rpm-gpg/RPM-GPG-KEY-xcp-ng-ce
```

### 3. Lancer create-installimg.sh (root)

```bash
# Doit s'exécuter en tant que root dans le conteneur de build
sudo ./create-installimg.sh \
    --define-repo base \
    --define-repo updates \
    --define-repo community \
    [autres options]
```

L'option `--define-repo` doit lister les trois dépôts : `base`, `updates` et
`community`.

### 4. Inscrire le numéro de build de l'ISO

`host-installer` lit `[build] number` dans le `.treeinfo` du média et l'écrit
dans `BUILD_NUMBER`, au sein de `/etc/xensource-inventory`, sur l'hôte
installé. L'amont livre l'espace réservé `cloud`, et rien d'autre sur un hôte
installé n'indique de quel média il provient : l'étiquette de volume ne
survit pas à l'installation, et les journaux conservés dans
`/var/log/installer/` n'en font pas mention.

Inscrivez le compteur ce dans le modèle avant que `create-iso.sh` ne le copie
dans l'ISO. Seuls les jetons `@@...@@` sont substitués : une valeur littérale
passe donc telle quelle.

```bash
sed -i "s/^number = .*/number = ${CE_COUNTER}/" \
    create-install-image/templates/iso/8.3/.treeinfo
```

Sur un hôte installé depuis l'ISO obtenue :

```bash
$ grep BUILD_NUMBER /etc/xensource-inventory
BUILD_NUMBER='ce23'

# xapi lit cet inventaire, la valeur est donc aussi visible à distance
$ xe host-param-get uuid=<uuid-de-l-hote> param-name=software-version
... build_number: ce23; ...
```

### 5. Lancer create-iso.sh (non-root)

```bash
./create-iso.sh \
    --sign-script implantisomd5 \
    --define-repo base \
    --define-repo updates \
    --define-repo community \
    [autres options]
```

### 6. Post-traitement isohybrid

{: .important }
Cette étape est **obligatoire** pour que l'ISO démarre sur du matériel
physique qui ne prend pas en charge l'UEFI.

```bash
isohybrid --uefi output.iso
```

Vérifiez le résultat avec :

```bash
fdisk -l output.iso
xorriso -report_el_torito output.iso
```

### 7. Checksum et signature

Chaque release livre trois fichiers aux côtés de l'ISO. Le fichier de
checksum porte le nom de l'ISO qu'il couvre :

```
xcp-ng-ce-8.3.iso
xcp-ng-ce-8.3.iso.sha256
xcp-ng-ce-8.3.iso.sha256.asc
```

Le fichier de checksum contient le fingerprint SHA256 de l'ISO. Le
fichier `.asc` est une signature GPG détachée du fichier de checksum,
produite avec la signing subkey de l'ISO. Ensemble, ils forment une
chaîne de vérification en deux étapes :

```
signing subkey ISO
    └── signe ──► xcp-ng-ce-8.3.iso.sha256   (contient le fingerprint de l'ISO)
                      └── fingerprint correspondant ──► xcp-ng-ce-8.3.iso
```

```bash
# Produire le fichier de checksum
sha256sum xcp-ng-ce-8.3.iso > xcp-ng-ce-8.3.iso.sha256

# Le signer avec la signing subkey de l'ISO
gpg --batch --pinentry-mode loopback \
    --detach-sign --armor \
    xcp-ng-ce-8.3.iso.sha256
# → produit xcp-ng-ce-8.3.iso.sha256.asc
```

### 8. Vérifier une release (procédure pour l'utilisateur final)

{: .note }
Les trois fichiers doivent être téléchargés dans le **même répertoire** avant
la vérification. `sha256sum -c` recherche l'ISO par son nom de fichier dans le
répertoire courant.

```bash
# 1. Télécharger les trois fichiers dans le même répertoire
cd ~/Téléchargements
# télécharger xcp-ng-ce-8.3.iso, xcp-ng-ce-8.3.iso.sha256,
#             xcp-ng-ce-8.3.iso.sha256.asc depuis la page de release GitHub

# 2. Importer la clé GPG communautaire (une seule fois)
gpg --keyserver keys.openpgp.org \
    --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A
```

**Étape 3 — vérifier que le fichier de checksum a bien été signé par
ce projet :**

```bash
gpg --verify xcp-ng-ce-8.3.iso.sha256.asc \
             xcp-ng-ce-8.3.iso.sha256
```

Sortie attendue (la ligne importante est `Good signature`) :

```
gpg: Signature made ...
gpg: Good signature from "XCP-ng home lab Edition <xcp-ng-ce.lid530@passmail.com>"
```

Si vous voyez `BAD signature`, le fichier de checksum a été altéré :
n'allez pas plus loin.

**Étape 4 — vérifier que l'ISO correspond à la checksum signée :**

```bash
sha256sum -c xcp-ng-ce-8.3.iso.sha256
```

Sortie attendue :

```
xcp-ng-ce-8.3.iso: OK
```

Si vous voyez `FAILED`, le fichier ISO est corrompu ou a été remplacé :
supprimez-le et retéléchargez-le.

---

## install.img — fonctionnement interne

{: .warning }
`install.img` est une **archive cpio (`newc`) compressée en bzip2**, pas du
SquashFS. `create-installimg.sh` la construit avec
`find . | cpio -o -H newc | bzip2` : `unsquashfs` et `mksquashfs` ne
s'appliquent donc pas.

Elle contient le ramdisk de l'installateur, pas le système de fichiers de
l'hôte installé — voir
[Comment les paquets arrivent sur l'hôte installé](#how-packages-reach-the-installed-host).

### Décompresser et recompresser

```bash
# Décompresser
mkdir installimg-root
bzip2 -dc install.img | (cd installimg-root && cpio -idm)

# Faire les modifications dans installimg-root/
# ...

# Recompresser (comme upstream : cpio newc, bzip2)
(cd installimg-root && find . | cpio -o -H newc) | bzip2 > install.img.new
```

Lister le contenu sans décompresser :

```bash
bzip2 -dc install.img | cpio -it
```

### Modification de host-installer pour la partition de stockage ISO
{: #host-installer-patching }

XCP-hl réserve une partition ISO de 20 Go à l'installation, ce qui suppose de
modifier `host-installer` lui-même. Cela se fait en **corrigeant ses fichiers
à l'intérieur de `install.img` au moment du build**, et non en livrant un RPM
`host-installer` dérivé.

La raison est que `xo-lite-ce` peut l'emporter dans la résolution des
dépendances en fournissant une capacité virtuelle (`Provides: xo-lite`), alors
que `host-installer` est un vrai paquet qui existe déjà dans les dépôts
`base`/`updates` de XCP-ng. Publier un remplaçant du même nom demanderait
d'incrémenter l'epoch sur un canal exposé aux hôtes en production, et il n'y a
nulle part où le placer en toute sécurité. Modifier le ramdisk confine le
changement à l'environnement de l'installateur, qui est jeté une fois
l'installation terminée.

Deux correctifs dans `xcp-ng-ce-iso/patches/` s'en chargent, appliqués par
l'étape de CI `Patch toolchain with git` :

| Correctif | Cible | Rôle |
|---|---|---|
| `installer-iso-sr-hook.patch` | `scripts/create-installimg.sh` | Ajoute une étape `patch -p1 -d "$ROOTFS/opt/xensource/installer"` après l'installation yum, à côté du bloc existant de personnalisation de l'installateur |
| `host-installer-iso-sr.patch` | `$ROOTFS/opt/xensource/installer/` | Le changement lui-même : partitionnement, `mkfs`, fstab, inventaire, plus le script de premier démarrage et son unité |

Le second correctif est généré à partir du
[fork de `host-installer`](https://github.com/Vagrantin/host-installer)
(branche `feat/xcp-hl-iso-storage`), où le changement est maintenu sous forme
de vrais commits sur l'amont et peut être passé à sa propre suite de tests
`test/` :

```bash
cd host-installer
git diff 10.10.38-8.3..feat/xcp-hl-iso-storage \
    -- backend.py constants.py answerfile.py xcp-hl/ \
    > ../xcp-ng-ce-iso/patches/host-installer-iso-sr.patch
```

Regénérez-le chaque fois que cette branche est rebasée sur un tag amont plus
récent. Un correctif qui ne s'applique plus fait échouer le build de manière
visible, plutôt que de livrer silencieusement un installateur non modifié, et
une étape de CI ultérieure décompresse l'`install.img` construit et cherche la
modification dans `backend.py` pour confirmer qu'elle a bien été appliquée.

**Ce que fait le correctif.** `constants.py` reçoit `iso_size` (20480 Mo) et
`min_primary_disk_size_with_iso` (100 Go) ; `backend.py` ajoute une entrée
`ISO` à la table de partitions qu'il met en place, dimensionnée et créée juste
avant la partition LVM pour que le SR local occupe toujours la fin du disque,
la formate en ext4 avec l'étiquette fixe `xcphl-iso`, écrit une entrée fstab
et une clé d'inventaire `ISO_PARTITION`, et dépose un script de premier
démarrage ainsi qu'une unité systemd sur la racine cible.

L'enregistrement du SR nécessite XAPI, qui ne s'exécute que sur l'hôte
installé : cette moitié se fait donc au premier démarrage, sur le modèle de
`storage-init.service`, qui crée le SR local principal de la même manière.
Le rattachement du SR après les redémarrages suivants ne demande rien de notre
part : XAPI rebranche tous les PBD débranchés au démarrage
(`Create_storage.plug_unplugged_pbds`), généralement ~10 s après la mise à
disposition de son API.

### Injection d'answerfile.xml (facultatif)

Un `answerfile.xml` référencé via `file:///` dans l'installateur est résolu
depuis la **racine du ramdisk** (issue d'`install.img`), et non depuis la
racine du CD-ROM de l'ISO. Pour injecter un fichier de réponses en vue d'une
installation automatisée, placez-le dans `install.img` via la procédure de
décompression/recompression ci-dessus.

Désactivez les contrôles liés à GPG via les attributs du fichier de réponses :

```xml
<installation gpgcheck="false" repo-gpgcheck="false">
  ...
</installation>
```

---

## Workflow de CI (GitHub Actions)

Le workflow est **déclenché uniquement par dispatch**. L'`iso-agent` pousse le
tag de release puis déclenche le workflow sur cette référence de tag, en
transmettant les tags de release exacts des composants à intégrer. Un simple
push de tag ne déclenche plus de build : résoudre les composants via
`releases/latest` entrait en concurrence avec les releases de composants
fraîchement publiées et pouvait intégrer un RPM obsolète.

Exigences importantes sur l'environnement :

```yaml
env:
  TMPDIR: /tmp       # Doit être défini ici ET dans le Dockerfile
  HOME: /tmp         # Nécessaire pour l'étape non-root create-iso.sh
```

Étapes principales :

```yaml
- name: Derive versions from tag
  run: |
    TAG="${{ github.ref_name }}"                            # ex. v8.3-ce4
    XCPNG_VER=$(echo "${TAG}" | sed 's/^v//;s/-ce.*//')    # → 8.3
    echo "XCPNG_VER=${XCPNG_VER}" >> $GITHUB_ENV

- name: Import ISO signing key
  # GPG_PRIVATE_KEY dans ce dépôt contient la signing subkey de l'ISO —
  # ce n'est pas le même matériel de clé que GPG_PRIVATE_KEY dans xolite-ce / xoa-proxy
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --batch \
      --pinentry-mode loopback \
      --passphrase "${{ secrets.GPG_PASSPHRASE }}" --import

- name: Export public key for installer chroot
  run: |
    gpg --armor --export "${GPG_KEY_ID}" > /tmp/RPM-GPG-KEY-xcp-ng-ce
    cp /tmp/RPM-GPG-KEY-xcp-ng-ce \
       create-install-image/templates/installimg/base/etc/pki/rpm-gpg/

- name: Set up Docker build environment
  run: docker build -t xcp-ng-build-ready -f Dockerfile.build .

- name: Download xolite-ce RPM
  run: |
    gh release download --repo Vagrantin/xolite-ce \
      --pattern "xo-lite-ce-*.rpm" \
      --dir community-repo/x86_64/

- name: Download xoa-proxy RPM
  run: |
    gh release download --repo Vagrantin/xoa-proxy \
      --pattern "xoa-proxy-*.rpm" \
      --dir community-repo/x86_64/

- name: Prepare community repo
  run: createrepo_c community-repo/x86_64/

- name: Copy CUSTOMREPO.tmpl
  run: cp configs/base/CUSTOMREPO.tmpl configs/8.3/

- name: Run create-installimg.sh (root)
  run: |
    docker run --rm --privileged \
      -v $PWD:/build \
      -v $PWD/create-install-image:/create-install-image \
      xcp-ng-build-ready \
      bash -c "cd /create-install-image && sudo ./create-installimg.sh ..."

- name: Run create-iso.sh (non-root)
  run: |
    docker run --rm \
      -e HOME=/tmp \
      -v $PWD:/build \
      xcp-ng-build-ready \
      bash -c "cd /create-install-image && ./create-iso.sh ..."

- name: Restore working directory ownership
  run: sudo chown -R $(id -u):$(id -g) .

- name: isohybrid post-processing
  run: isohybrid --uefi output.iso

- name: implantisomd5
  run: implantisomd5 output.iso

- name: Generate and sign checksum
  run: |
    CHECKSUM_FILE="${OUTPUT}.sha256"
    sha256sum "${OUTPUT}" > "${CHECKSUM_FILE}"
    echo "CHECKSUM_FILE=${CHECKSUM_FILE}" >> $GITHUB_ENV
    gpg --batch --pinentry-mode loopback \
      --detach-sign --armor "${CHECKSUM_FILE}"
    gpg --verify "${CHECKSUM_FILE}.asc" "${CHECKSUM_FILE}"

- name: Publish GitHub Release
  uses: softprops/action-gh-release@v2
  with:
    tag_name: ${{ github.ref_name }}
    files: |
      ${{ env.OUTPUT }}
      ${{ env.CHECKSUM_FILE }}
      ${{ env.CHECKSUM_FILE }}.asc

- name: Remove GPG private key
  if: always()
  run: shred -u /tmp/community-signing.key || true
```

{: .note }
Le montage de volume Docker doit référencer `create-install-image`. Vérifiez
que la cible du montage correspond au nom réel du répertoire cloné.

---

## Contribuer

1. Forkez
   [Vagrantin/xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso).
2. Testez vos modifications avec la procédure Docker locale ci-dessus.
3. Activez la variable `DEBUG_BUILD` dans les réglages GitHub Actions de votre
   fork pour activer la superposition des scripts de débogage et faciliter le
   diagnostic en CI.
4. Ouvrez une pull request sur `main`.
