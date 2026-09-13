---
layout: default
title: build-xoa-hl
parent: Développeurs
grand_parent: Français
nav_order: 5
lang: fr
---

# build-xoa-hl
{: .no_toc }

Chaîne Packer qui construit l'appliance VM XOA-HL sur XCP-ng et produit
l'image XVA que XO Lite CE déploie.
{: .fs-6 .fw-300 }

**Dépôt :** [Vagrantin/build-xoa-hl](https://github.com/Vagrantin/build-xoa-hl)
· Langage : Bash / JSON Packer / Kickstart · Licence : AGPL-3.0

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectif

Ce dépôt construit l'**appliance VM XOA HomeLab Edition** : une VM
AlmaLinux 9, installée et provisionnée par Packer **sur un vrai hôte
XCP-ng**, avec le RPM [`xoa-hl`](xoa-hl.html) à l'intérieur. Le résultat est
une **image XVA** compressée, l'artefact qu'importe le bouton de déploiement
de XO Lite CE.

L'appliance est générique au moment du build : elle embarque deux services de
premier démarrage à exécution unique, qui lisent les données de
provisionnement (réseau, identifiants d'administration) depuis XenStore
lorsque XO Lite la déploie, de sorte qu'une seule image convient à tout le
monde.

---

## Structure du dépôt

```
build-xoa-hl/
├── build.config.sample        ← modèle de configuration d'infrastructure (copier → build.config)
├── scripts/
│   ├── setup-xoa-builder.sh   ← point d'entrée du build : génère le Kickstart + le JSON Packer, lance le build
│   ├── xoa-first-boot.sh      ← phase 1 dans la VM : XenStore → réseau + fichier d'environnement
│   └── xoa-credentials.sh     ← phase 2 dans la VM : définit les identifiants admin XO via xo-cli
├── systemd/
│   ├── xoa-first-boot.service
│   └── xoa-credentials.service
├── bin/                       ← archive VMware VDDK embarquée (prise en charge V2V)
└── artefact/                  ← artefacts de build et de débogage : journaux, liste des RPM installés, mémo
```

---

## Prérequis

- Une machine de build sous Linux avec `apt` et sudo (développé sous Linux
  Mint). Le script d'installation installe ses propres dépendances : Packer
  (dépôt apt HashiCorp), le greffon Packer
  [`ddelnano/xenserver`](https://github.com/ddelnano/packer-plugin-xenserver),
  `wget`, `curl`, `jq`, `ufw`.
- Un **hôte XCP-ng** joignable, avec des identifiants root, un SR
  `Local storage` et un réseau de VM nommé.
- Une release [`xoa-hl`](xoa-hl.html) publiée sur GitHub (le RPM de la
  dernière release est résolu automatiquement).
- `build.config`, copié depuis `build.config.sample` et complété : IP et
  identifiants de l'hôte XCP-ng, nom du réseau, nom de la VM et mot de passe
  root, URL de l'ISO AlmaLinux et URL des RPM `xe-guest-utilities`.

{: .warning }
`build.config` contient des **identifiants en clair** (mot de passe root
XCP-ng, mot de passe root de la VM). Ne le committez jamais : seul
`build.config.sample` a sa place dans git.

---

## Point d'entrée du build, scripts/setup-xoa-builder.sh

S'exécute sur la machine de build et génère tout ce dont Packer a besoin :

1. **Charger `build.config`** (avec repli sur les valeurs par défaut
   intégrées s'il est absent).
2. **Installer les prérequis**, paquets apt, Packer de HashiCorp et le
   greffon Packer `ddelnano/xenserver`.
3. **Ouvrir les ports 8000–9000/tcp** (ufw) : Packer sert le fichier
   Kickstart à la VM via son serveur HTTP intégré, sur un port de cette
   plage.
4. **Résoudre la checksum de l'ISO AlmaLinux**, en analysant le
   fichier `CHECKSUM` du miroir au format BSD, avec repli sur le format GNU
   `SHA256SUMS` ; le build échoue si aucun SHA256 valide n'est trouvé (sauf si
   la valeur est figée dans `build.config`).
5. **Résoudre l'URL du dernier RPM xoa-hl**, en parcourant
   `api.github.com/repos/Vagrantin/xoa-hl/releases` à la recherche de la
   release la plus récente qui porte un artefact `.rpm`. Pas
   `releases/latest` : celle-ci peut encore tomber sur l'une des releases
   `xoa-image-*` antérieures à
   [#22](https://github.com/Vagrantin/xcp-hl/issues/22), qui ne livrent qu'une
   XVA.
6. **Générer `inst.ks`**, le fichier de réponses Kickstart : DHCP sur `eth0`,
   partitionnement EXT4 (sans LVM), SELinux et pare-feu désactivés, jeu de
   paquets minimal ; le `%post` active sshd et chrony, installe
   `epel-release`, `wget`, `nc`, `vim`, et crée l'utilisateur `xo` (dans le
   groupe `wheel`).
7. **Générer `almalinux-build.json`**, le modèle Packer (voir plus bas).
8. **Lancer le build**, `packer validate` puis
   `PACKER_LOG=1 packer build almalinux-build.json`.

---

## Modèle Packer, almalinux-build.json

Un unique builder `xenserver-iso` : Packer envoie l'ISO AlmaLinux sur l'hôte
XCP-ng, démarre une VM (2 Go de RAM, 10 Go de disque) avec
`inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/inst.ks` sur la ligne de
commande du noyau, attend SSH, puis lance les provisionneurs :

1. `dnf update -y`.
2. Installer **xe-guest-utilities** et **xe-guest-utilities-xenstore** (URL
   des RPM issues de `build.config`), nécessaires pour accéder à XenStore au
   premier démarrage.
3. Installer **Node.js 24** (NodeSource).
4. Installer le **RPM xoa-hl**, ce qui tire toute la pile XOA-HL (voir
   [`xoa-hl`](xoa-hl.html) : le `%post` du RPM télécharge l'archive de la
   release dans `/opt/xo` et active `redis` + `xo-server`).
5. Envoyer `xoa-first-boot.sh` / `xoa-credentials.sh` dans `/root/` et les
   deux unités systemd dans `/etc/systemd/system/`, puis activer les deux
   unités.
6. **Alléger l'image**, supprimer les micrologiciels wifi, firewalld, sssd,
   les extras NetworkManager, rsyslog, les pages de documentation, de manuel
   et info, ainsi que les locales autres que l'anglais ; `dnf autoremove` +
   `clean all`.
7. **Effacer l'identité**, vider `/etc/machine-id` pour que chaque VM
   déployée régénère le sien.

Réglages importants du builder : `format: xva_compressed` (la sortie XVA) et
`keep_vm: always` (la VM construite reste sur l'hôte XCP-ng pour inspection).

---

## Auto-configuration au premier démarrage

Deux services à exécution unique sont intégrés à l'image ; XO Lite écrit les
données de provisionnement dans XenStore
(`/local/domain/<domid>/vm-data/*`) lorsqu'il déploie l'appliance.

### Phase 1, xoa-first-boot.service

S'exécute **avant que le réseau ne soit disponible**
(`Before=network.target`, conditionné par
`ConditionPathExists=!/var/lib/xoa-first-boot.done`). Le script :

- lit les clés `vm-data` via `xenstore-read` : `ip`, `netmask`, `gateway`,
  `dns`, `ntp-servers`, `system-account-xoa-password`, ainsi que le bloc JSON
  `admin-account` (e-mail + mot de passe) ;
- les enregistre dans `/etc/xoa-first-boot.env` (mode 600) ;
- écrit un fichier de configuration NetworkManager
  (`/etc/NetworkManager/system-connections/xoa-provisioned.nmconnection`),
  en IP statique si elle est fournie, en DHCP sinon ;
- journalise abondamment dans `/var/log/xoa-first-boot.log` pour le
  diagnostic sur le terrain.

### Phase 2, xoa-credentials.service

S'exécute une fois **après** `network-online.target` et
`xo-server.service`, conditionné par `!/var/lib/xoa-credentials.done`. Le
script :

- attend jusqu'à 3 minutes que xo-server réponde sur le port 443 ;
- définit le mot de passe SSH de l'utilisateur système `xo` à partir de la
  valeur provisionnée ;
- enregistre `xo-cli` auprès de `wss://127.0.0.1` avec les identifiants
  d'amorçage, puis appelle `user.changePassword` et `user.set` pour appliquer
  l'adresse e-mail et le mot de passe administrateur provisionnés ;
- **s'autodétruit** en sortie (via un `trap`) : il écrit le marqueur de fin,
  désactive et supprime les deux unités et les deux scripts, et efface le
  fichier d'environnement contenant les secrets.

{: .note }
Si les données de provisionnement sont absentes ou si la phase 2 échoue,
l'appliance conserve les valeurs d'amorçage par défaut `admin@admin.net` /
`admin` : changez-les depuis l'interface web de XO après le déploiement.

---

## Résultats produits

- L'image XVA compressée, dans `output-xva/` à l'intérieur du répertoire de
  build sur la machine de build.
- La VM construite elle-même, conservée sur l'hôte XCP-ng
  (`keep_vm: always`).
- Dans la chaîne automatisée, une **release GitHub sur ce dépôt**
  (`Vagrantin/build-xoa-hl`) taguée `xoa-image-<date>-<sha7>` et portant
  l'artefact `xoa-almalinux.xva`, celui que résout le bouton de déploiement de
  XO Lite.

---

## Builds automatisés, l'orchestrateur

Dans la chaîne quotidienne, `setup-xoa-builder.sh` est remplacé par la crate
`xoa-vm-agent` de
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration).
Elle effectue les mêmes étapes de manière programmatique, et en plus :

1. Ignore le build lorsque le HEAD du dépôt correspond déjà au dernier SHA
   construit.
2. Déclenche d'abord le workflow `build-xoa.yml` dans `Vagrantin/xoa-hl` via
   `workflow_dispatch` et attend la release du RPM.
3. Lance `packer validate` + `packer build` avec les fichiers `inst.ks` /
   `almalinux-build.json` générés.
4. Publie la XVA comme release GitHub taguée `xoa-image-<date>-<sha7>` sur
   **`Vagrantin/build-xoa-hl`**, ce dépôt (`<sha7>` est le commit `xoa-hl` à
   partir duquel l'image a été construite ; ce commit se trouve dans l'autre
   dépôt, le tag est donc créé sur `main` et le commit source est consigné
   dans le corps de la release). Les releases d'images sont consignées dans la
   [matrice des versions](../release-matrix.html#xoa-hl-releases).

{: .note }
Les images étaient publiées sur `Vagrantin/xoa-hl` jusqu'à
[#22](https://github.com/Vagrantin/xcp-hl/issues/22). Ces releases restent où
elles sont pour que les ISO déjà livrées continuent de les résoudre, ce qui
explique pourquoi les outils qui parcourent `xoa-hl` à la recherche du RPM
doivent toujours ignorer les tags `xoa-image-*`.

---

## Contribuer

Le modèle de contribution n'est pas encore formalisé ; pour l'instant, créez
un ticket sur le
[dépôt XCP-hl](https://github.com/Vagrantin/xcp-hl/issues).
