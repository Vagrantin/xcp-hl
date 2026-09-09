---
layout: default
title: Français
nav_order: 10
has_children: true
lang: fr
---

# XCP-hl
{: .fs-9 }

Une ISO XCP-ng gratuite, construite par la communauté, qui remplace le Xen
Orchestra officiel (alias XOA) par un Xen Orchestra entièrement
**auto-hébergé**. L'objectif est de simplifier le déploiement des images XOA
construites par la communauté, en visant surtout les utilisateurs de homelab.
{: .fs-6 .fw-300 }

> ### ⚠️ Logiciel en version alpha
>
> **XCP-hl est en version alpha.** Le projet est en cours de
> développement actif et n'a pas encore connu de cycle de stabilisation.
> **Attendez-vous à des changements incompatibles à chaque version** : les
> versions des composants, les noms de paquets, l'organisation des dépôts et
> le comportement des mises à jour peuvent tous changer, et une mise à jour
> en place peut demander une intervention manuelle sur l'hôte.
>
> Utilisez-le sur du matériel et des données que vous êtes prêt à reconstruire
> de zéro. Les rapports de bogues et les retours sont les bienvenus sur
> [GitHub](https://github.com/Vagrantin/xcp-hl/issues).

[Télécharger la dernière ISO](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Voir sur GitHub](https://github.com/Vagrantin/xcp-hl){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Qu'est-ce que XCP-hl ?

[XCP-ng](https://xcp-ng.org/) est un hyperviseur de type 1 (bare-metal)
open source et puissant, basé sur le projet Xen. Officiellement, il est livré
avec **XO Lite**, une interface de gestion légère qui s'exécute dans le
navigateur, et un bouton qui déploie en un clic l'**appliance Xen Orchestra
officielle (XOA)**.

**XCP-hl** garde tout ce qui fait la force de XCP-ng, mais remplace ce
bouton unique par un workflow maintenu par la communauté.
Une fois déployé, vous pourrez choisir entre 3 options pour déployer XOA :
- l'image XOA pour homelab (par défaut)
- l'image XOA officielle de Vates
- l'image de Ronivay (dernières nouveautés)
- votre propre image personnalisée

L'un des objectifs est de fournir une image XOA allégée, sans les bandeaux
liés à l'absence de support commercial ni les fonctionnalités qui demandent
une licence, ce qui simplifie l'expérience XOA pour les utilisateurs de
homelab. Cette image, **XOA-HL**, est construite à partir des dépôts
[`xoa-hl`](https://github.com/Vagrantin/xoa-hl) et
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl).

Pour la stabilité et la maintenabilité, les deux composants modifiés sont
**figés sur une version amont précise** : construire à partir du `master`
amont serait trop risqué, avec de fortes chances de casser les builds à
chaque évolution upstream. XO Lite HL est construit à partir d'un tag amont
fixe (actuellement `xo-lite-v0.21.0`) et XOA-HL à partir d'un commit Xen
Orchestra fixe (actuellement `5.113.2`, la dernière version XO 5.x) : pour
l'instant, **XOA-HL utilise par défaut l'interface web XO v5, pas XO v6**.
Ces versions figées ne sont relevées que délibérément, après tests, pour
qu'une évolution upstream ne puisse jamais casser un déploiement existant.
Les versions exactes livrées avec chaque release sont consignées dans la
[matrice des versions](release-matrix.html).

---

## Téléchargement

{: .note }
Toutes les ISO et tous les RPM publiés sont signés avec la **clé GPG
XCP-hl**. Vérifiez votre téléchargement avant l'installation.

[⬇ Télécharger l'ISO](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest){: .btn .btn-primary }

### Vérifier l'ISO

La clé GPG de la communauté est publiée sur
[keys.openpgp.org](https://keys.openpgp.org).

| Propriété | Valeur |
|---|---|
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

---

## Démarrage rapide

### 1 · Installer XCP-hl
Démarrez depuis l'ISO et suivez le
[guide d'installation officiel](https://docs.xcp-ng.org/installation/install-xcp-ng/).
L'installateur ressemble et se comporte comme celui du XCP-ng 8.3 upstream.

**Utilisez un disque d'au moins 100 Go.** XCP-HL réserve une partition de
20 Go pour une bibliothèque d'ISO prête à l'emploi, en plus des ~41,5 Go
occupés par les partitions système, ce qui laisse ~38,5 Go pour le stockage
des VM. Sur un disque plus petit l'installation se termine quand même, mais
la bibliothèque d'ISO est ignorée et vous obtenez le partitionnement standard
de XCP-ng. Voir [Stockage ISO](features.html#iso-storage).

### 2 · Ouvrir XO Lite
Après l'installation, pointez votre navigateur sur :

```
http://<ip-de-votre-hote>
```

Connectez-vous à XO Lite avec vos identifiants root XCP-ng.

### 3 · Déployer XOA
Dans XO Lite, cliquez sur **Deploy XOA**. Renseignez les informations
demandées (IP, utilisateur, mot de passe, etc.).
Quand vous lancez le déploiement, XO Lite appelle le
[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) fourni avec l'ISO, qui
transmet l'image XOA (par exemple `image.xva.gz`) directement à XAPI en flux
continu. Plus de détails dans la section Développeurs / xoa-proxy.

### 4 · Connecter XO à votre hôte
Une fois la VM XOA démarrée, ouvrez-la dans votre navigateur et ajoutez votre
hôte XCP-ng :

```
Settings → Servers → Add server
Host : <ip-de-votre-hote-XCP>
User : root
```

### 5 · Maintenir le système à jour
XCP-HL livre ses composants sous forme de RPM signés, un hôte en
fonctionnement se met donc à jour en place. Les mises à jour disponibles
apparaissent dans Xen Orchestra sous
`Home > Hosts > <votre hôte> > Patches`. Voir [Mises à jour](updates.html)
pour comprendre le mécanisme, initialiser un hôte plus ancien et revenir en
arrière.

---

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

---

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

Tous les détails techniques dans la
[section Développeurs](developers/).

---

## Licence

XCP-hl est publié sous **licence publique générale GNU Affero v3.0**
(AGPL-3.0). Il s'appuie sur XCP-ng upstream (composants Apache 2.0 / GPL) et
sur Xen Orchestra (AGPL-3.0).

> XCP-hl est un projet communautaire indépendant.
> Bien qu'il en soit issu, il n'est ni affilié à, ni approuvé par, ni
> supporté par Vates SAS ou le projet XCP-ng.
