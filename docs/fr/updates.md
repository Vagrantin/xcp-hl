---
layout: default
title: Mises à jour
parent: Français
nav_order: 4
lang: fr
---

# Mettre à jour XCP-hl
{: .no_toc }

Les composants de XCP-hl sont livrés sous forme de RPM signés, depuis les
dépôts yum de `rpm.xcp-hl.org` : un hôte en fonctionnement se met donc à
jour en place. Il n'est pas nécessaire de réinstaller depuis l'ISO pour
récupérer une nouvelle version de XO Lite ou de `xoa-proxy`.

Les dépôts ont quitté `vagrantin.github.io` pour cette adresse (ticket #190).
Un hôte ou une appliance bascule seul lors de sa prochaine mise à jour de
`xcp-hl-release` ou de `xoa-hl`, qui portent les nouvelles adresses. Les
anciennes adresses restent en ligne pendant la transition.

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
  https://rpm.xcp-hl.org/xcp-hl.repo

rpm --import https://rpm.xcp-hl.org/xcp-ng-ce-public.asc

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

## Mettre à jour l'appliance XOA-HL

L'appliance XOA-HL se met à jour depuis son propre dépôt yum :

```bash
dnf update xoa-hl        # l'application de l'appliance uniquement
dnf update               # l'application et la base AlmaLinux ensemble
```

La configuration se trouve dans `/etc/yum.repos.d/xoa-hl.repo`, qui appartient
au paquet `xoa-hl` lui-même, et définit un seul dépôt :

| ID du dépôt | Contenu | Publié depuis |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

Les mises à jour peuvent aussi être lancées depuis l'interface web de XOA-HL,
sous **Settings → XOA-HL Updates**. La page affiche le journal de la
transaction en continu pendant son exécution.

Des unités systemd pilotent les mises à jour :

| Unité | Rôle |
|---|---|
| `xoa-hl-check-update.service` | Exécute `dnf check-update` et écrit le résultat dans `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Exécute un `dnf -y update` complet, hors `nodejs`, et en diffuse la sortie dans `/var/lib/xoa-hl/update.log` |
| `xoa-hl-check-update.timer` | Lance la vérification selon un calendrier, en mode `check` |
| `xoa-hl-auto-update.service` / `.timer` | Vérifie puis installe, pendant une fenêtre de maintenance, en mode `install` |

{: .warning }
`xoa-hl-update.service` met à jour **tous** les paquets ayant une mise à jour
en attente, pas seulement `xoa-hl`. Node.js fait exception : il reste sur la
version majeure exigée par le paquet `xoa-hl`.

### Modes de mise à jour

Les versions postérieures à `v5.113.2_e281c536-ce18` ajoutent des vérifications
planifiées et l'installation automatique. Les deux sont **désactivées par
défaut** : installer ou mettre à jour le paquet n'active jamais l'un ou
l'autre des timers. Choisissez un mode dans **Settings → XOA-HL Updates**, ou
en root :

```bash
# MODE FREQUENCY DAY TIME RANDOM_DELAY_MINUTES
/usr/libexec/xoa-hl/configure-updates.sh check weekly Sun 03:00 15
```

| Mode | Ce qui s'exécute seul |
|---|---|
| `manual` (par défaut) | Rien. Les vérifications et les mises à jour ne démarrent que lorsqu'un administrateur les lance |
| `check` | La vérification des mises à jour, selon le calendrier et peu après le démarrage. L'installation reste manuelle |
| `install` | La vérification, puis la mise à jour, pendant la fenêtre de maintenance. Une fenêtre manquée n'est pas rejouée après le démarrage |

L'appliance ne redémarre jamais d'elle-même, même en mode `install`. Voir
[les mises à jour automatiques de l'appliance](https://github.com/Vagrantin/xoa-hl/blob/main/docs/automatic-updates.md)
pour les options de calendrier et la façon de consulter le résultat.

### La page de mise à jour perd sa connexion

L'installation d'un nouveau `xoa-hl` redémarre `xo-server`, qui sert aussi
l'interface web : la page de mise à jour perd donc sa connexion pendant un
moment. La mise à jour elle-même s'exécute dans `xoa-hl-update.service` et
continue malgré cela.

Les versions postérieures à `v5.113.2_e281c536-ce18` gèrent ce cas :

- la page continue de tenter de se reconnecter tant que `xo-server` est
  arrêté, puis reprend le journal là où il s'était arrêté et affiche le
  résultat ;
- `xo-server` est redémarré une seule fois, une fois la transaction entière
  terminée ;
- après une minute sans connexion, la page indique depuis combien de temps
  `xo-server` est injoignable et propose un bouton **Reload page**, qui ne
  recharge la page qu'une fois `xo-server` de nouveau joignable ;
- recharger la page rétablit la mise à jour lancée depuis cet onglet, avec son
  résultat.

### Après une mise à jour interrompue

Testé uniquement sur `v5.113.2_e281c536-ce52`. D'autres versions peuvent se
comporter différemment.

Lors d'un test sur ce52, un arrêt forcé pendant que `xoa-hl-update.service`
installait `kernel-modules` a endommagé des fichiers du noyau. La mise à jour
gérée suivante s'est arrêtée à sa vérification d'intégrité préalable et a
signalé un échec. D'autres interruptions peuvent avoir d'autres conséquences.
La fin de `/var/lib/xoa-hl/update.log` se présente ainsi :

```text
Package integrity preflight failed; repair the interrupted transaction before retrying.
=== xoa-hl update failed with exit code 1 at ... ===
```

Lors de ce test, l'appliance a démarré sur son noyau précédent. Le journal
listait les fichiers endommagés au-dessus de ce message ; ne présumez pas
qu'une appliance interrompue démarrera.

{: .warning }
Exécutez les commandes ci-dessous en root et uniquement lorsqu'aucune mise à
jour n'est en cours. Ne supprimez pas le noyau sur lequel l'appliance a
démarré.

**Inspecter.** Vérifiez qu'aucune mise à jour n'est en cours, puis contrôlez la
base de paquets et les paquets du noyau :

```bash
systemctl is-active xoa-hl-update.service    # expect inactive or failed
dnf check
rpm -V $(rpm -qa kernel-core kernel-modules kernel-modules-core)
ls /boot/vmlinuz-*
```

`dnf check` peut ne rien signaler alors que des fichiers du noyau sont
endommagés : exécutez donc les deux contrôles. Des lignes telles que
`S.5......  /lib/modules/<version>/vmlinuz` signifient que les fichiers de
cette version du noyau sont endommagés, et l'absence de
`/boot/vmlinuz-<version>` le confirme. Les lignes signalant des fichiers
manquants sous `/usr/share/licenses` ou `/usr/share/doc` sont normales :
l'image est installée sans documentation, et l'outil de mise à jour les
ignore.

**Réparer.** Réinstallez la version du noyau endommagée indiquée par `rpm -V`,
par exemple `5.14.0-687.66.1.el9_8`, puis vérifiez :

```bash
dnf remove --duplicates
dnf reinstall kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
dnf check
rpm -V kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
grubby --default-kernel
```

Les deux commandes de vérification ne doivent rien afficher, et
`grubby --default-kernel` doit désigner le noyau le plus récent.

**Relancer la mise à jour.** Relancez la mise à jour gérée, depuis **Settings →
XOA-HL Updates** ou avec `systemctl start xoa-hl-update.service`. Elle doit se
terminer par `=== xoa-hl update finished successfully ===`. L'appliance ne
redémarre jamais d'elle-même : redémarrez-la ensuite. `dnf needs-restarting -r`
indique si un redémarrage est en attente, et `uname -r` affiche le noyau en
cours d'exécution après le redémarrage.

Sur `ce52`, cette réparation a été testée pour une transaction du noyau
interrompue pendant l'installation de `kernel-modules`. Elle n'a pas été
testée pour un paquet dupliqué tel que `xz-libs`, pour une mise à jour
automatique (mode `install`) interrompue, ni pour un échec signalé après la
transaction plutôt qu'avant.

## Limitations connues

- **La mise à jour automatique peut indiquer qu'aucun redémarrage n'est
  nécessaire alors qu'il est en attente.** Sur `v5.113.2_e281c536-ce52`, lorsqu'une
  mise à jour manuelle a déjà installé un noyau et que l'exécution
  automatique suivante ne trouve rien à faire, son historique enregistre
  `rebootNeeded: no`. Vérifiez avec `dnf needs-restarting -r`. Un correctif est
  prévu après le lancement. Voir le
  [ticket #392](https://github.com/Vagrantin/xcp-hl/issues/392).

- **La mise à jour qui installe le correctif de reconnexion peut encore sembler
  bloquée.** La page depuis laquelle vous l'avez lancée exécute encore l'ancien
  code, qui cesse de tenter de se reconnecter au bout d'environ 2,5 minutes. Si
  elle reste sur *Reconnecting to xo-server*, attendez que `xo-server` soit de
  nouveau joignable et actualisez la page. La mise à jour n'est pas affectée.
  Pour lire le journal depuis un shell : `cat /var/lib/xoa-hl/update.log`. Cela
  ne s'applique qu'une fois, à la mise à niveau depuis
  `v5.113.2_e281c536-ce18` ou une version antérieure. Voir le
  [ticket #103](https://github.com/Vagrantin/xcp-hl/issues/103).

{: .note }
N'oubliez pas que cette distribution est en version alpha. Lisez les notes de
version avant de mettre à jour : des changements incompatibles sont attendus à
chaque version, et une mise à jour peut nécessiter une intervention manuelle
sur l'hôte.
