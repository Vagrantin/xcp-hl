---
layout: default
title: xoa-proxy
parent: Développeurs
grand_parent: Français
nav_order: 1
lang: fr
---

# xoa-proxy
{: .no_toc }

Proxy HTTP/HTTPS en Rust qui transmet une image XOA à XAPI en flux continu.
{: .fs-6 .fw-300 }

**Dépôt :** [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy)
· Langage : Rust · Licence : AGPL-3.0

## Sommaire
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectif

Quand on clique sur le bouton « Deploy XOA » modifié de XO Lite, XAPI doit
importer une archive de VM `.xva`. XAPI appelle `VM.import` avec une URL ; il
attend du serveur situé à cette URL qu'il serve le fichier en HTTP uniquement,
et le fichier doit être au format XVA.

Ce support limité ne me satisfaisait pas et, à l'origine, était même
bloquant : je m'appuyais sur l'image de Ronivay, qui est au format gz et n'est
accessible qu'en HTTPS.

C'est pour cela que xoa-proxy sert d'interface devant XAPI : il prend en
charge les protocoles HTTP et HTTPS (certificats auto-signés compris) et,
en plus du format XVA, le format gz.

Ce proxy apporte la souplesse nécessaire pour importer des images de
différentes sources, y compris locales, et renforce la sécurité en
introduisant la prise en charge de HTTPS.

---

## Conception

### Choix technologiques

| Choix | Justification |
|---|---|
| **Rust** | Sûreté mémoire, adapté à un processus serveur de longue durée dans le Dom0 |

### Cheminement d'une requête

```
XO Lite (navigateur)
    │  HTTP GET /image.xva
    ▼
xoa-proxy
    │
    │ Interface HTTP/HTTPS pour XAPI
    │ Décompression du format gzip à la volée
    │
    ▼
XAPI VM.import
    │  Écrit les VDI sur le SR local
    ▼
VM XOA créée
```

### HTTP et HTTPS

xoa-proxy prend en charge HTTP et HTTPS (certificats auto-signés compris)
lorsqu'il récupère l'image XOA en amont. Pendant le téléchargement, les images
compressées en gzip sont décompressées à la volée, de sorte que XAPI reçoit
toujours un flux XVA brut, non compressé.

Le passage de relais vers XAPI via `VM.import` se fait délibérément en
HTTP/1.0 : XAPI ne prend pas en charge le codage de transfert par blocs
(*chunked transfer encoding*, une fonctionnalité de HTTP/1.1), et utiliser le
découpage HTTP/1.1 corromprait l'import. Le proxy gère cette contrainte en
interne ; l'appelant n'a rien à configurer.

---

## Structure du code

```
xoa-proxy/
├── src/
│   └── main.rs        ← serveur HTTP, gestionnaire de requêtes, logique de flux
├── tests/             ← tests d'intégration
├── .cargo/            ← configuration Cargo (réglages de compilation croisée)
├── Cargo.toml         ← dépendances : hyper, tokio, tokio-util, ...
└── Cargo.lock
```

### Motif central de diffusion en flux

Le cœur du proxy consiste à convertir un `tokio::fs::File` en corps de
réponse hyper sans charger tout le fichier en mémoire :

```rust
use tokio_util::io::ReaderStream;
use hyper::Body;

let file = tokio::fs::File::open("image.xva").await?;
let stream = ReaderStream::new(file);
let body = Body::wrap_stream(stream);

let response = Response::builder()
    .header("Content-Type", "application/octet-stream")
    .header("Content-Encoding", "gzip")
    .body(body)?;
```

---

## Construction

### Prérequis

- Chaîne d'outils Rust (stable) — à installer via [rustup](https://rustup.rs/)
- Pour la compilation croisée vers le Dom0 : la cible
  `x86_64-unknown-linux-musl`

```bash
# Build natif (pour les tests)
cargo build

# Compilation croisée pour le Dom0 (binaire musl statique)
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

Le binaire obtenu dans
`target/x86_64-unknown-linux-musl/release/xoa-proxy` est un exécutable
entièrement statique, sans dépendance à des bibliothèques partagées, ce qui
convient à une intégration dans l'environnement DOM0 de XCP-ng.

### Exécution locale, pour le développement ou les tests

```bash
# Placer une XVA de test au chemin attendu
cp /chemin/vers/test.xva image.xva

# Démarrer le proxy
./target/release/xoa-proxy

# Tester la diffusion en flux
curl -v http://127.0.0.1:3000/image.xva -o /dev/null
```

---

## Configuration

Dans la version actuelle, l'adresse d'écoute et le chemin de l'image sont
codés en dur.

| Paramètre | Valeur actuelle |
|---|---|
| Adresse d'écoute | `127.0.0.1:3000` |
| Point d'accès du proxy | `image.xva` |

---

## Signature GPG

Le RPM `xoa-proxy` est signé avec la **sous-clé de signature RPM** de la paire
de clés XCP-ng Community Edition. La même sous-clé est partagée avec
`xolite-ce` : il n'y a qu'une seule sous-clé pour les deux RPM.

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
rpm --checksig xoa-proxy-*.rpm
```

---

## Intégration avec XO Lite CE

Le correctif XO Lite de [`xolite-ce`](xolite-ce.html) fixe l'URL de
déploiement à `http://127.0.0.1:3000/image.xva`. C'est l'adresse sur laquelle
`xoa-proxy` écoute lorsqu'il est démarré sur un hôte XCP-ng HL.

---

## Tests

```bash
# Lancer les tests unitaires et d'intégration
cargo test

# Les tests d'intégration se trouvent dans tests/
# Ils démarrent le proxy et vérifient son comportement en diffusion continue
```

---

## Contribuer

1. Forkez [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy).
2. Créez une branche : `git checkout -b feature/ma-modification`.
3. Lancez `cargo fmt` et `cargo clippy` avant de committer.
4. Ouvrez une pull request sur `main`.
