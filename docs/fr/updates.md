---
layout: default
title: Mises à jour
parent: Français
nav_order: 4
lang: fr
---

# Mettre à jour XCP-hl
{: .no_toc }

Les composants de XCP-hl sont livrés sous forme de RPM signés, depuis des
dépôts yum hébergés sur GitHub Pages : un hôte en fonctionnement se met donc à
jour en place. Il n'est pas nécessaire de réinstaller depuis l'ISO pour
récupérer une nouvelle version de XO Lite ou de `xoa-proxy`.

1. TOC
{:toc}

---

## Où apparaissent les mises à jour

Les mises à jour XCP-hl disponibles apparaissent dans **Xen Orchestra**, au
même endroit que les mises à jour XCP-ng standard :

```
Home > Hosts > <votre hôte> > Patches
```

L'onglet liste chaque paquet disponible avec son nom, sa description, sa
version, son numéro de release et sa taille de téléchargement ; une pastille
rouge en indique le nombre. L'icône en forme d'œil **Show changelog** d'une
ligne ouvre l'entrée de changelog du RPM. La vue au niveau du
pool, dans `Home > Pools > <pool> > Patches`, et le résumé du tableau de bord
affichent les mêmes données.

XCP-ng fournit un greffon XAPI, `updater.py`, que Xen Orchestra interroge pour
connaître les mises à jour disponibles ; XOA-HL est modifié pour inclure les
dépôts XCP-hl dans cette interrogation.

## Installer les mises à jour

**Install all patches**, dans l'onglet Patches, applique tout ce que la liste
affiche.

{: .warning }
C'est tout ou rien. Le greffon de mise à jour de XCP-ng lance un unique
`yum update` sur les dépôts XCP-ng standard et les dépôts XCP-hl à la fois :
appuyer sur le bouton applique donc aussi toute mise à jour du système XCP-ng
en attente. Cette vue ne permet pas de sélectionner des paquets
individuellement. Si vous ne voulez que les paquets XCP-hl, lancez plutôt
`yum update xo-lite-ce xoa-proxy` sur l'hôte.

Depuis la ligne de commande de l'hôte, les équivalents sont :

```bash
yum check-update            # ce qui est disponible
yum update xcp-hl-release   # la configuration des dépôts elle-même
yum update xo-lite-ce       # XO Lite (HomeLab Edition)
yum update xoa-proxy        # le proxy de déploiement XVA
```

## Configuration des dépôts

La configuration tient dans un seul fichier, `/etc/yum.repos.d/xcp-hl.repo`,
propriété du paquet `xcp-hl-release`. Il définit trois dépôts :

| Identifiant du dépôt | Contenu | Publié depuis |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{: .important }
Ne renommez pas les sections de ce fichier. Les identifiants de dépôt sont
transmis par Xen Orchestra au greffon `updater.py`, qui ne liste les mises à
jour que pour les dépôts qu'on lui a indiqués. Une section renommée ne
provoque pas d'erreur : elle retire silencieusement ces paquets de l'onglet
Patches.

Comme `yum` ne relit jamais un fichier `.repo` qu'il possède déjà, les réglages
des dépôts sont livrés sous forme de paquet plutôt que de fichier à copier une
fois pour toutes. Une modification de la configuration atteint votre hôte via
`yum update xcp-hl-release`.

Le fichier est marqué `%config(noreplace)` : si vous l'avez modifié
localement, votre version est conservée et la nouvelle est écrite à côté sous
le nom `xcp-hl.repo.rpmnew`.

## Première configuration sur un hôte existant

Les hôtes installés depuis une ISO antérieure au paquet `xcp-hl-release`
demandent une initialisation unique. Ensuite, la configuration est gérée par
yum.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://vagrantin.github.io/xcp-hl/xcp-hl.repo

rpm --import https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

L'installation du paquet remplace le fichier que vous venez de télécharger par
la copie empaquetée, en conservant la vôtre sous le nom
`xcp-hl.repo.rpmorig`. Les deux ne diffèrent que par l'endroit d'où elles
lisent la clé de signature : la copie téléchargée la récupère en HTTPS, tandis
que la copie empaquetée utilise la clé locale que le paquet installe.

Les ISO plus récentes embarquent déjà `xcp-hl-release` : cette section ne les
concerne donc pas.

## Revenir en arrière

Chaque dépôt ne publie que ses versions les plus récentes, ce qui limite la
fenêtre de retour arrière. Pour revenir à un build antérieur :

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<version>
```

## Vérification et confiance

Les paquets et les métadonnées des dépôts sont signés avec la clé GPG XCP-hl.
La configuration côté client définit `repo_gpgcheck=1` avec `gpgcheck=0`.

Les RPM sont signés par une **signing subkey** GPG. Sur le dom0 de
XCP-ng 8.3, rpm 4.11 n'enregistre que la clé principale lors de l'import d'une
clé : il signale donc `NOKEY` pour toute signature produite par une sous-clé
et ne peut pas vérifier les paquets directement. La confiance passe donc par
les métadonnées du dépôt : `repomd.xml` est signé et vérifié par GPG lui-même,
qui sait gérer les sous-clés ; il enregistre une fingerprint SHA-256 de
`primary.xml`, qui enregistre à son tour une fingerprint SHA-256 de chaque
paquet.

{: .warning }
Les signing subkeys expirent le **10 mai 2027**. Passé cette date, la
vérification échoue tant qu'elles n'ont pas été prolongées, que la clé publiée
n'a pas été rafraîchie et qu'elle n'a pas été réimportée sur chaque hôte.

## Limitations connues

XOA-HL ne dispose pas encore de dépôt yum : l'appliance ne peut donc pas se
mettre à jour en place. Mettre à jour XOA-HL signifie aujourd'hui déployer une
image plus récente. Le sujet est suivi dans le
[ticket #14](https://github.com/Vagrantin/xcp-hl/issues/14).

{: .note }
N'oubliez pas que cette distribution est en version alpha. Lisez les notes de
version avant de mettre à jour : des changements incompatibles sont attendus à
chaque version, et une mise à jour peut nécessiter une intervention manuelle
sur l'hôte.
