---
layout: default
title: Développeurs
parent: Français
nav_order: 8
has_children: true
lang: fr
---

# Documentation développeur
{: .no_toc }

Tout ce qu'il faut pour comprendre, construire et contribuer à XCP-hl.
{: .fs-6 .fw-300 }

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Vue d'ensemble des dépôts

XCP-hl est réparti sur plusieurs dépôts fonctionnels, plus ce dépôt de
documentation.

```
Vagrantin/xcp-hl          ← docs (ce site)
      │
      ├── Vagrantin/xolite-ce       ← correctif XO Lite + build RPM
      │         │ publie le RPM signé comme artefact de release GitHub
      │         │
      ├─────────│───Vagrantin/xoa-proxy           ← proxy HTTP Rust + build RPM
      │         │        │  publie le RPM signé comme artefact de release GitHub
      │         ▼        ▼
      ├── Vagrantin/xcp-ng-ce-iso   ← assemblage de l'ISO + releases GitHub de l'ISO
      │         │ télécharge les RPM de xolite-ce et xoa-proxy, assemble l'ISO
      │
      ├── Vagrantin/xoa-hl          ← XOA-HL : Xen Orchestra modifié (RPM + conteneur)
      │         ▼
      ├── Vagrantin/build-xoa-hl    ← chaîne Packer → image XVA de XOA sur XCP-ng
      │         │ publie la XVA comme release GitHub (tags xoa-image-*)
      │
      └── Vagrantin/buildorchestration ← orchestrateur Rust : déclenche et surveille tous les builds
```

Chaque dépôt a sa propre chaîne GitHub Actions. Ils sont **faiblement
couplés** : `xolite-ce` et `xoa-proxy` publient des artefacts RPM versionnés
que `xcp-ng-ce-iso` récupère par tag de release. Aucun de ces dépôts n'a
besoin d'être récupéré en même temps qu'un autre pour un build normal.
`xoa-hl` construit le Xen Orchestra modifié par la communauté (XOA-HL), et
`build-xoa-hl` l'empaquette en image XVA. `buildorchestration` se place
au-dessus et pilote l'ensemble de la chaîne selon une planification
quotidienne (voir [Orchestration des builds](#build-orchestration) plus bas).

---

## Pile technique

| Couche | Technologie |
|---|---|
| Base hyperviseur | XCP-ng 8.3 (Xen 4.17, Dom0 Linux 4.19) |
| Interface XO Lite | Vue 3 · TypeScript · Vite · Pinia (`@xen-orchestra/lite`) |
| Build de XO Lite | Yarn (Corepack) · `yarn build:xo-lite` |
| Empaquetage RPM | `rpmbuild`, `rpmsign`, `createrepo_c` |
| Assemblage de l'ISO | `create-install-image` (chaîne d'outils XCP-ng, branche master) |
| Outillage ISO | `mksquashfs`, `xorriso`, `isohybrid`, `implantisomd5` |
| Build de XOA-HL | Node.js 24 · workspaces Yarn · conteneur AlmaLinux 9 |
| Build de l'image XVA | Packer · greffon `ddelnano/xenserver` · Kickstart |
| Environnement de build | Docker (`xcp-ng-build-env:8.3`) |
| Serveur proxy | Rust · `hyper` · `tokio` · `tokio_util::io::ReaderStream` |
| CI/CD | GitHub Actions |
| Signature | GPG — offline master key + 2 signing subkeys (voir plus bas) |

---

## Chaîne de build — de bout en bout

```
1. CI xolite-ce (GitHub Actions)
   ├── Cloner vatesfr/xen-orchestra au tag figé dans UPSTREAM_TAG
   │   (actuellement xo-lite-v0.21.0 — relevé délibérément, pas automatiquement)
   ├── Appliquer patches/community-xoa-deploy.patch
   ├── yarn build:xo-lite
   ├── rpmbuild → xo-lite-community-<VERSION>.rpm
   ├── rpmsign avec la signing subkey RPM (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
   └── Publier le RPM signé comme artefact de release GitHub (clé publique sur
       keys.openpgp.org ; étapes d'import dans les notes de version)

2. CI xoa-proxy (GitHub Actions)
   ├── Installer la chaîne d'outils musl (musl-1.2.4, libc statique)
   ├── Installer Rust stable via rustup
   ├── Ajouter la cible x86_64-unknown-linux-musl
   ├── cargo build --release --target x86_64-unknown-linux-musl
   ├── Préparer les sources RPM (binaire + unité systemd + config logrotate)
   ├── rpmbuild → xoa-proxy-<VERSION>.rpm
   ├── rpmsign avec la signing subkey RPM (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
   └── Publier le RPM signé comme artefact de release GitHub (clé publique sur
       keys.openpgp.org ; étapes d'import dans les notes de version)

3. CI xcp-ng-ce-iso (GitHub Actions)
   ├── Télécharger le RPM signé depuis la release xolite-ce
   ├── Télécharger le RPM signé depuis la release xoa-proxy
   ├── Importer GPG_PRIVATE_KEY (signing subkey ISO) dans le trousseau du runner
   ├── Exporter la clé publique du trousseau du runner → l'injecter dans le chroot de l'installateur
   ├── Préparer community-repo/x86_64/ avec createrepo_c
   ├── Lancer create-installimg.sh (root) — construit install.img (SquashFS)
   ├── Lancer create-iso.sh (non-root) — assemble l'ISO
   ├── isohybrid --uefi (fingerprint hybride MBR/GPT)
   ├── implantisomd5
   ├── sha256sum → xcp-ng-8.3-ceN.iso.sha256
   ├── gpg --detach-sign  (signing subkey ISO via GPG_PRIVATE_KEY)
   └── Publier xcp-ng-8.3-ceN.iso + .iso.sha256 + .iso.sha256.asc comme
       release GitHub de Vagrantin/xcp-ng-ce-iso (clé publique sur
       keys.openpgp.org ; étapes de vérification dans les notes de version)

4. CI xoa-hl (GitHub Actions)
   ├── Récupération superficielle de vatesfr/xen-orchestra au commit figé dans XO_COMMIT
   │   (actuellement 5.113.2 — dernière version XO 5.x, relevée délibérément)
   ├── Appliquer patches/*.patch (menu-hide-items)
   ├── Écrire xoahl.config.toml + générer un certificat TLS auto-signé
   ├── yarn && yarn build (tous les workspaces), élaguer, retirer les devDependencies
   ├── tar → xoa-hl-<VERSION>.tar.gz
   ├── rpmbuild → xoa-hl-<VERSION>.noarch.rpm (léger : %post récupère l'archive)
   └── Publier l'archive + le RPM comme release GitHub v<VERSION>

5. build-xoa-hl (Packer, sur un vrai hôte XCP-ng)
   ├── Résoudre la checksum de l'ISO AlmaLinux + l'URL de la dernière release RPM de xoa-hl
   ├── Générer inst.ks (Kickstart) et almalinux-build.json (modèle Packer)
   ├── packer build — installer AlmaLinux 9 via Kickstart sur l'hôte XCP-ng
   ├── Provisionner : xe-guest-utilities, Node 24, RPM xoa-hl, unités de premier démarrage
   ├── Alléger l'image, vider /etc/machine-id
   └── Exporter la XVA (xva_compressed) — l'appliance que XO Lite CE déploie
```

---

## Orchestration des builds
{: #build-orchestration }

Le dépôt
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
automatise la chaîne décrite ci-dessus. Son workspace Rust
`xcp-orchestrator` (crates `orchestrator`, `iso-agent`, `xoa-vm-agent`,
`shared`) s'exécute comme service systemd sur une VM dédiée, déclenché
quotidiennement par une minuterie :

```
minuterie systemd (chaque jour à 05h00)
   ├── Déclencher les workflows xolite-ce et xoa-proxy via workflow_dispatch
   ├── Interroger les exécutions de workflow jusqu'à leur fin
   ├── Ignorer un composant dont la dernière release GitHub correspond déjà à HEAD
   │   (détection de changement basée sur les releases — pas de reconstruction systématique)
   ├── En cas d'échec : récupérer les journaux du job via l'API et les diagnostiquer
   │   avec un LLM local (Ollama, qwen3-coder:30b) — écrit une suggestion de correction exploitable
   ├── En cas de succès : déclencher les builds en aval xcp-ng-ce-iso et l'image XVA de XOA
   └── Afficher un tableau de bord d'état (état par composant + liens vers les journaux)
```

---

## Choix de conception importants

### Stratégie à trois dépôts
Séparer chaque build de RPM de l'assemblage de l'ISO garde les
responsabilités bien délimitées : `xolite-ce` (correctif d'interface,
empaquetage) et `xoa-proxy` (proxy Rust, empaquetage) peuvent chacun évoluer
indépendamment sans toucher à la chaîne d'outils de l'ISO, et réciproquement.
Chacun publie un RPM versionné et signé comme artefact de release GitHub. Ces
artefacts sont ensuite consommés pour construire l'ISO.

### Correctif au niveau du code source
Le correctif XO Lite est appliqué au **code source** Vue/TypeScript de
`DeployXoaView.vue`.

---

## Signature GPG
{: #gpg-signing }

XCP-hl utilise une unique paire de clés suivant un modèle **offline master
key + sous-clés**. La clé maîtresse est conservée hors ligne et n'est
jamais utilisée pour signer. Deux signing subkeys en sont dérivées :
une pour les deux RPM, une pour l'ISO.

### Détails de la clé

| Propriété | Valeur |
|---|---|
| Fingerprint de la clé maîtresse | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Publiée sur | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Adresse e-mail | `xcp-ng-ce.lid530@passmail.com` |
| Fichier de clé publique | `xcp-ng-ce-public.asc` |

### Rôle des sous-clés

| Sous-clé | Utilisée pour |
|---|---|
| Signing subkey RPM | `xo-lite-community-*.rpm` et `xoa-proxy-*.rpm` |
| Signing subkey ISO | `xcp-ng-8.3-ceN.iso.sha256.asc` (detached signature du fichier de checksum de l'ISO) |

---

## Documentation détaillée des composants

| Page | Description |
|---|---|
| [xoa-proxy](xoa-proxy.html) | Proxy HTTP/gzip en Rust pour la livraison des XVA |
| [xolite-ce](xolite-ce.html) | Correctif XO Lite, spec RPM, chaîne de build |
| [xcp-ng-ce-iso](xcp-ng-ce-iso.html) | Assemblage de l'ISO, chaîne d'outils, workflow de CI |
| [xoa-hl](xoa-hl.html) | Xen Orchestra modifié (XOA-HL) — build de l'archive + RPM léger |
| [build-xoa-hl](build-xoa-hl.html) | Chaîne Packer qui construit l'image XVA de XOA sur XCP-ng |
| [buildorchestration (GitHub)](https://github.com/Vagrantin/buildorchestration) | Orchestrateur de build en Rust + diagnostic des builds par LLM |
