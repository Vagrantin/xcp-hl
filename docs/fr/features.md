---
layout: default
title: Fonctionnalités
parent: Français
nav_order: 2
lang: fr
---

# Fonctionnalités — v8.3-ce9
{: .no_toc }

Version actuelle · juin 2026 · Basée sur XCP-ng 8.3
{: .fs-6 .fw-300 }

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Plateforme de base

XCP-ng HL est une **ISO de remplacement direct** pour XCP-ng 8.3. Elle hérite
de l'ensemble des fonctionnalités amont ; les différences portent sur XO Lite,
XOA et le workflow de déploiement. Tout ce qui se trouve sous l'installateur
fonctionne exactement comme dans la version officielle.

| Caractéristique | Valeur |
|---|---|
| Version de base | XCP-ng 8.3 (dernière version mineure amont) |
| Hyperviseur | Xen 4.17 |
| Noyau Dom0 | Linux 4.19 (noyau XCP-ng) |
| API de gestion | XAPI (Xen API) |
| Réseau par défaut | Open vSwitch (OVS) |
| Installateur | Installateur XCP-ng en mode texte |

---

## Personnalisations

### XO Lite modifié

XO Lite est l'interface de gestion légère, en page unique, fournie avec chaque
hôte XCP-ng. Dans la HomeLab Edition, le composant amont `DeployXoaView.vue`
est modifié **au niveau du code source** avant la construction du RPM, ce qui
garde le correctif minimal.

La version amont de xo-lite est figée via le fichier `UPSTREAM_TAG` du dépôt
`xolite-ce` (actuellement `xo-lite-v0.21.0`, la dernière version connue comme
fonctionnelle) et ne bouge que lorsque cette valeur est relevée
délibérément.

**Ce que le correctif change :**

- Le bouton **« Deploy XOA »** pointe vers une page de déploiement XOA
  actualisée.
- L'image XOA-HL.
- L'image officielle de Vates.
- L'image fournie par Ronivay.
- Un champ personnalisé pour déployer votre propre image XOA.

Tout le reste de XO Lite — gestion des VM, accès à la console, exploration des
SR, métriques de l'hôte — reste inchangé.

### xoa-proxy — livraison locale des XVA

Un **serveur HTTP écrit en Rust** conçu pour l'occasion (`xoa-proxy`) est
fourni avec l'ISO et s'exécute sur l'hôte. Il :

- sert l'image XOA de la communauté, y compris au format compressé en gzip ;
- prend en charge HTTP et HTTPS (certificats auto-signés compris).

### Image XOA HomeLab

L'image XOA déployée par le proxy est construite en intégrant XOA-HL
[Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl).

### Image XOA de Ronivay

L'image XOA déployée par le proxy est construite à partir de
[ronivay/XenOrchestraInstallerUpdater](https://github.com/ronivay/XenOrchestraInstallerUpdater),
un installateur communautaire bien maintenu pour Xen Orchestra auto-hébergé.

| Détail | Valeur |
|---|---|
| Version de XO | Suit la dernière version stable de XO |
| Utilisateur admin par défaut | `admin@admin.net` |
| Mot de passe admin par défaut | `admin` |
| Utilisateur SSH | `xo` |
| Mot de passe SSH | `xopass` |

{: .warning }
**Changez immédiatement les mots de passe par défaut** après la première
connexion.

### Image XOA de Vates

Il s'agit de l'image officielle fournie par Vates pour la gestion multi-hôtes
de XCP-ng. Dans ce cas, vous pouvez indiquer les identifiants à l'étape de
déploiement.

---

## Signature GPG

Tous les artefacts XCP-ng HL sont signés avec la **clé GPG XCP-ng HomeLab
Edition**.

### Structure de la clé

La clé suit un modèle **clé maîtresse hors ligne + sous-clés** :

| Rôle | Description |
|---|---|
| Clé maîtresse | Certification uniquement — conservée hors ligne, jamais utilisée pour signer |
| Sous-clé de signature des RPM | Signe tous les paquets RPM de la communauté (`xo-lite-community`, `xoa-proxy`) |
| Sous-clé de signature de l'ISO | Signe le fichier de somme de contrôle de l'ISO (`xcp-ng-8.3-ceN.iso.sha256.asc`) |

| Propriété | Valeur |
|---|---|
| Empreinte de la clé maîtresse | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Publiée sur | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Adresse e-mail | `xcp-ng-ce.lid530@passmail.com` |
| Fichier de clé publique | `xcp-ng-ce-public.asc` (joint à chaque release) |

Le fichier de clé publique contient les deux sous-clés de signature. Il suffit
de l'importer une fois pour vérifier à la fois les RPM et la somme de contrôle
de l'ISO.

---

## Ce que vous obtenez (récapitulatif complet)

### Hyperviseur et gestion des hôtes

- **Toutes les fonctionnalités de XCP-ng 8.3** — tous les types de VM (HVM,
  PV, PVH), la migration à chaud (XenMotion) et Storage XenMotion.
- **Storage Repositories (SR)** — LVM local, NFS, iSCSI (LVM et EXT), HBA/FC,
  XOSTOR (hyperconvergé), SMB, SR d'ISO.
- **Bibliothèque d'ISO prête à l'emploi** : une partition dédiée de 20 Go est
  réservée à l'installation et enregistrée comme SR d'ISO au premier
  démarrage, ce qui vous permet d'envoyer des images d'installation et de
  créer des VM sans configurer le stockage à la main. Voir
  [Stockage ISO](#iso-storage).
- **GPU / vGPU** — passthrough PCI et prise en charge des vGPU NVIDIA GRID.
- **HA** — haute disponibilité du pool avec redémarrage automatique des VM en
  cas de panne d'un hôte.

### Stockage ISO
{: #iso-storage }

Par défaut, XCP-ng n'a nulle part où ranger les ISO d'installation : aucun SR
d'ISO n'existe, et en créer un revient à choisir un chemin, créer un
répertoire et lancer `xe sr-create` à la main. XCP-HL le fait pour vous.

**Ce que vous obtenez.** Une installation neuve réserve une partition de
20 Go, la formate en ext4 avec l'étiquette `xcphl-iso`, la monte sur
`/var/opt/xen/xcp-hl-iso` et l'enregistre auprès de XAPI comme SR d'ISO nommé
**XCP-HL ISO library**. Elle apparaît immédiatement dans Xen Orchestra : vous
pouvez donc envoyer une ISO (*Import → Disk*, en sélectionnant le SR d'ISO) et
démarrer une VM dessus sans configuration supplémentaire.

**Taille de disque requise.** XCP-HL demande un disque de **100 Go**, réparti
approximativement ainsi :

| Zone | Taille |
|---|---|
| Partitions système (root, sauvegarde, boot, journaux, swap) | ~41,5 Go |
| Bibliothèque d'ISO | 20 Go |
| SR de stockage local (disques des VM) | ~38,5 Go |

En dessous de 100 Go, la réservation est ignorée plutôt que de réduire le
stockage des VM à quelques Go. L'installation se termine quand même et le
disque est partitionné exactement comme le ferait XCP-ng standard. Vous
n'obtenez simplement pas de bibliothèque d'ISO, et une ligne dans
`/var/log/installer` en indique la raison.

**Où cela s'applique.** La partition est créée par l'installateur : elle
n'existe donc que sur les hôtes installés à partir d'une ISO XCP-HL. Un hôte
installé depuis XCP-ng standard qui ajoute ensuite les dépôts XCP-HL conserve
son partitionnement existant, rien ne repartitionne une machine en
fonctionnement. Ces hôtes peuvent toujours créer un SR d'ISO manuellement, de
la manière habituelle.

La mise à niveau d'un hôte XCP-HL existant conserve la partition, puisqu'une
mise à niveau ne repartitionne jamais, et le SR d'ISO est retrouvé grâce à
l'étiquette du système de fichiers.

**Limitation connue.** Si vous débranchez le PBD du SR puis le rebranchez
*sans* redémarrer, XAPI le rattache mais le système de fichiers reste non
monté : la bibliothèque paraît donc vide jusqu'au prochain redémarrage, qui la
remonte. C'est inhérent à la façon dont XCP-ng gère les SR d'ISO locaux
(`legacy_mode`) et cela affecte de la même manière le SR intégré XCP-ng Tools ;
un redémarrage, ou `mount /var/opt/xen/xcp-hl-iso`, rétablit la situation.

### XO Lite (gestion rapide depuis le navigateur)

Disponible sur `http://<ip-de-l-hote>` immédiatement après l'installation :

- vue d'ensemble du pool et de l'hôte (CPU, RAM, stockage en un coup d'œil) ;
- liste des VM : démarrer, arrêter, redémarrer, accéder à la console ;
- inspection basique des SR et du réseau ;
- **workflow de déploiement HomeLab** : déploiement de XOA en un clic, sans
  connexion à Internet si vous hébergez votre image XOA en local.

### Xen Orchestra (après le déploiement de XOA)

Après un « Deploy XOA » dans XO Lite, vous disposez d'une instance Xen
Orchestra complète :

- **Gestion complète du cycle de vie des VM** — créer, cloner, migrer,
  prendre des instantanés.
- **Sauvegarde sans agent** — complète, différentielle, réplication continue,
  reprise après sinistre.
- **Planification** — tâches de sauvegarde de type cron, avec rétention
  configurable.
- **RBAC / délégation** — rôles (Admin, Opérateur, Observateur) et ensembles
  de ressources.
- **Supervision et alertes** — métriques par VM et par hôte, alertes sur
  seuils.
- **API REST + xo-cli** — accès scriptable à toutes les ressources.
- **Mise à niveau progressive du pool** — mises à niveau sans interruption
  via XO.
- **XOSTOR** — mise en place du stockage hyperconvergé depuis l'interface XO
  (3 nœuds ou plus).

{: .warning }
**Certaines fonctionnalités nécessitent une licence distribuée par Vates.**

---

## Limitations connues dans cette version

| Limitation | État |
|---|---|
| Xolite-ce — le bouton Deploy reste toujours accessible | [issue#4](https://github.com/Vagrantin/xolite-ce/issues/4) — remplacer le bouton par « Access XOA » après un déploiement réussi |
| Xoa-proxy — les journaux sont en UTC | [issue#3](https://github.com/Vagrantin/xoa-proxy/issues/3) — investigation à mener |
| Xoa-proxy — réduire le nombre de crates | [issue#2](https://github.com/Vagrantin/xoa-proxy/issues/2) — investigation à mener |
| Xoa-proxy — réduire l'empreinte mémoire | [issue#1](https://github.com/Vagrantin/xoa-proxy/issues/1) — xoa-proxy s'exécute dans le Dom0 ; son impact mémoire doit être maîtrisé |
| Xcp-hl — versionnage des publications | [issue#4](https://github.com/Vagrantin/xcp-hl/issues/4) — le versionnage est incohérent d'un artefact à l'autre |

---

## Journal des modifications

### v8.3-ce9 (juin 2026)
- xolite-ce `v0.21.0-ce6` — xo-lite amont figé sur `0.21.0` (dernière version
  connue comme fonctionnelle ; `0.22.0` et `0.23.0` cassaient le build) via le
  fichier `UPSTREAM_TAG`.
- xoa-proxy `v0.1.1.x` — versionnage RPM simplifié (suffixe de release
  `.static`) et notes de version GitHub automatisées et catégorisées.
- Nommage cohérent des artefacts : `xcp-ng-8.3-ceN.iso` + `.iso.sha256` +
  `.iso.sha256.asc`, publiés comme releases GitHub de `xcp-ng-ce-iso`.

### v8.3-ce alpha2 (mai 2026)
- Première publication publique.
- Première version réellement utilisable.
- Fournit les fonctions de base pour déployer depuis Vates, Ronivay ou une URL
  personnalisée.
- **GPG** : clé maîtresse hors ligne + sous-clés dédiées à la signature des
  RPM et de l'ISO. Clé publique publiée sur keys.openpgp.org.

### v8.3-ce (avril 2026)
- XO Lite modifié : point de déploiement communautaire, champs d'identifiants
  en lecture seule.
- Serveur Rust `xoa-proxy` intégré : HTTP/HTTPS, flux gzip.
- ISO assemblée à partir de XCP-ng 8.3 amont, avec superposition du dépôt RPM
  communautaire.
- Infrastructure de clés GPG (RSA 4096 bits, clé unique
  `RPM-GPG-KEY-xcp-ng-ce`).
- Chaîne CI/CD GitHub Actions : build RPM → build ISO → releases GitHub.
