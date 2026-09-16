---
title: Bien démarrer
weight: 0
translationKey: getting-started
---

Installez XCP-hl, déployez XOA, et maintenez l'hôte à jour.
{class="lead"}

## Téléchargement et vérification

{{< callout type="info" >}}
Toutes les ISO et tous les RPM publiés sont signés avec la **clé GPG XCP-hl**.
Vérifiez votre téléchargement avant l'installation.
{{< /callout >}}

[⬇ Télécharger la dernière ISO](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest)

### Vérifier l'ISO

La clé GPG de la communauté est publiée sur [keys.openpgp.org](https://keys.openpgp.org).

| Propriété | Valeur |
|---|---|
| UID de la clé | `XCP-ng Community Edition (Master signing key)` — tel qu'affiché par `gpg --list-keys` |
| Fichier de clé | `xcp-ng-ce-public.asc` (joint à chaque release) |
| Adresse e-mail | `xcp-ng-ce.lid530@passmail.com` |
| Fingerprint | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |

```bash
# Option 1 — récupérer la clé depuis le serveur de clés
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# Option 2 — importer la clé depuis la page de release
gpg --import xcp-ng-ce-public.asc

# Vérifier la signature du fichier de checksum de l'ISO
# (les fichiers de checksum portent le nom de l'ISO — exemple pour v8.3-ce9)
gpg --verify xcp-ng-8.3-ce9.iso.sha256.asc xcp-ng-8.3-ce9.iso.sha256

# Vérifier l'ISO
sha256sum -c xcp-ng-8.3-ce9.iso.sha256
```

## Démarrage rapide

### 1 · Installer XCP-hl

Démarrez depuis l'ISO et suivez le
[guide d'installation officiel](https://docs.xcp-ng.org/installation/install-xcp-ng/).
L'installateur ressemble et se comporte comme celui du XCP-ng 8.3 upstream.

**Utilisez un disque d'au moins 100 Go.** XCP-hl réserve une partition de
20 Go pour une bibliothèque d'ISO prête à l'emploi, en plus des ~41,5 Go
occupés par les partitions système, ce qui laisse ~38,5 Go pour le stockage
des VM. Sur un disque plus petit l'installation se termine quand même, mais
la bibliothèque d'ISO est ignorée et vous obtenez le partitionnement standard
de XCP-ng. Voir [Stockage ISO](/docs/guides/features#iso-storage).

### 2 · Ouvrir XO Lite

Après l'installation, pointez votre navigateur sur :

```
http://<ip-de-votre-hote>
```

Connectez-vous à XO Lite avec les identifiants root de l'hôte (ceux définis
pendant l'installation).

### 3 · Déployer XOA

Dans XO Lite, cliquez sur **Deploy XOA**. Renseignez les informations
demandées (IP, utilisateur, mot de passe, etc.).
Quand vous lancez le déploiement, XO Lite appelle le
[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) fourni avec l'ISO, qui
transmet l'image XOA (par exemple `image.xva.gz`) directement à XAPI en flux
continu. Plus de détails sur la
[page du composant xoa-proxy](/docs/components/xoa-proxy).

### 4 · Connecter XO à votre hôte

Une fois la VM XOA démarrée, ouvrez-la dans votre navigateur et ajoutez votre
hôte XCP-hl :

```
Settings → Servers → Add server
Host : <ip-de-votre-hote-XCP>
User : root
```

### 5 · Maintenir le système à jour

XCP-hl livre ses composants sous forme de RPM signés, un hôte en
fonctionnement se met donc à jour en place. Les mises à jour disponibles
apparaissent dans Xen Orchestra sous
`Home > Hosts > <votre hôte> > Patches`. Voir
[Mises à jour](/docs/guides/updates) pour comprendre le mécanisme,
initialiser un hôte plus ancien et revenir en arrière.

## Architecture en un coup d'œil

```
┌──────────────────────────────────────────────────────────────┐
│                    Hôte XCP-hl                               │
│                                                              │
│  ┌──────────────┐  correctif ┌──────────────────────────────┐│
│  │  XO Lite HL  │ ────────►  │  DeployXoaView (communauté)  ││
│  │              │            │                              ││
│  └──────┬───────┘            └───────────┬──────────────────┘│
│         │                                │ HTTP              │
│  ┌──────▼────────────────────────────────▼─────────────────┐ │
│  │                   xoa-proxy                             │ │
│  │    HTTP · HTTPS · gzip · livraison XVA en flux continu  │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │ XAPI VM.import                 │
│  ┌──────────────────────────▼──────────────────────────────┐ │
│  │                   XAPI / Dom0                           │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Composants

| Dépôt | Rôle |
|---|---|
| [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) | Documentation |
| [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) | Correctif communautaire pour XO Lite + build RPM |
| [`xcp-ng-ce-iso`](https://github.com/Vagrantin/xcp-ng-ce-iso) | Chaîne d'assemblage de l'ISO et publication |
| [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) | Proxy HTTP/gzip en Rust pour la livraison des XVA + build RPM |
| [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) | Appliance Xen Orchestra adaptée au homelab (XOA-HL) — interface simplifiée, build RPM et conteneur |
| [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) | Chaîne Packer qui construit l'image XVA de XOA sur XCP-ng et la publie comme release |
| [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) | Orchestrateur de build en Rust — déclenche, surveille et diagnostique tous les builds de composants chaque jour |

Tous les détails techniques dans la [section Composants](/docs/components/).

## Licence

XCP-hl est publié sous **licence publique générale GNU Affero v3.0**
(AGPL-3.0). Il s'appuie sur XCP-ng upstream (composants Apache 2.0 / GPL) et
sur Xen Orchestra (AGPL-3.0).

> XCP-hl est un projet communautaire indépendant.
> Bien qu'il en soit issu, il n'est ni affilié à, ni approuvé par, ni
> supporté par Vates SAS ou le projet XCP-ng.
