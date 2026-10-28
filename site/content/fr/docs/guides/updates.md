---
title: Mises à jour
weight: 3
translationKey: updates
aliases: ["/fr/updates.html"]
---

XCP-hl et XOA-hl se mettent tous deux à jour en place, à partir de paquets
signés, sans réinstallation pour les mises à jour courantes. L'hôte (XCP-hl) se met à jour
depuis l'onglet **Patches** de Xen Orchestra, comme XCP-ng standard.
L'appliance (XOA-hl) se met à jour depuis sa propre page de réglages
**XOA-HL Updates**.
{class="lead"}

Les dépôts de paquets utilisent `rpm.xcp-hl.org` après le déplacement suivi dans [#190](https://github.com/Vagrantin/xcp-hl/issues/190). Une mise à jour de `xcp-hl-release` ou de `xoa-hl` apporte les nouvelles adresses des dépôts. Les anciennes adresses sont conservées pendant la transition. Les commandes d’installation initiale ci-dessous utilisent la nouvelle adresse.

Les deux moitiés de cette page suivent le même plan : les étapes dans Xen
Orchestra, l'équivalent en ligne de commande, le fonctionnement sous le capot,
et le retour en arrière.

## Mettre à jour XCP-hl (l’hôte hyperviseur) {#mettre-à-jour-xcp-hl-lhôte}

{{< callout type="info" >}}
**S’applique à** l’image XOA-HL `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; l’installation des paquets de l’hôte et le redémarrage n’ont pas encore été testés en laboratoire avec cette version.
{{< /callout >}}

### Dans Xen Orchestra

1. **Repérer les mises à jour en attente.** Dans `Home > Hosts`, un hôte qui a
   des mises à jour en attente affiche une pastille rouge avec le nombre de
   correctifs manquants.

   {{< screenshot src="updates/xcp-hl-1-missing-patches.png" alt="Liste des hôtes : une pastille rouge sur l'hôte compte ses correctifs manquants" >}}

2. **Ouvrir l'onglet Patches de l'hôte.** Sélectionnez l'hôte, puis
   **Patches**. L'onglet liste chaque paquet avec son nom, sa description, sa
   version, son numéro de release et sa taille de téléchargement ; l'icône en
   forme d'œil d'une ligne affiche le changelog du RPM. La vue au niveau du
   pool, `Home > Pools > <pool> > Patches`, liste les paquets manquants du
   maître ; vérifiez chaque hôte séparément avant une action sur tout le pool.

   {{< screenshot src="updates/xcp-hl-2-patches-tab.png" alt="L'onglet Patches de l'hôte, avec la liste des paquets disponibles" >}}

3. **Choisir la portée voulue.** Dans l’onglet **Patches** de l’hôte, **installer tous les patchs** vise cet hôte. Dans l’onglet du pool, **Installer les patchs sur le pool** vise tous les hôtes du pool, en commençant par le maître. Vérifiez les identités de l’hôte et du pool avant de confirmer.

   {{< screenshot src="updates/xcp-hl-3-installing.png" alt="L'onglet Patches pendant l'installation des correctifs du pool" >}}

   {{< callout type="warning" >}}
   Aucun des deux boutons ne permet de choisir des paquets XCP-ng un par un.
   Pour chaque hôte visé, `updater.py` exécute un `yum update` sur les dépôts
   XCP-ng standard et XCP-hl activés ; les mises à jour standard en attente
   sont donc comprises. Cette opération groupée ne garantit pas un retour
   arrière atomique. Le bouton du pool traite les hôtes un à un, maître en
   premier ; il n’évacue pas les VM et ne redémarre pas les hôtes. Pour ne
   mettre à jour que certains paquets XCP-hl, utilisez séparément la ligne
   de commande ci-dessous.
   {{< /callout >}}

4. **Attendre la tâche et actualiser la connexion à l’hôte.** Dans cette version de XO, le
   bouton appelle le greffon de l’hôte, puis redémarre son agent XAPI après
   l’installation. Une déconnexion temporaire de l’hôte est possible. Cette
   étape n’appelle pas la mise à jour de l’appliance XOA-HL et ne redémarre
   pas `xo-server`. Si la connexion ne revient pas, conservez l’erreur et
   examinez l’hôte par une console indépendante avant toute nouvelle tentative.

5. **Vérifier le résultat.** Actualisez l’inventaire de l’hôte et du pool
   concernés, le résultat de la tâche, les paquets et versions, le nombre de
   correctifs manquants et l’indication de redémarrage requis. La disparition
   de la pastille ne prouve ni un redémarrage ni la santé des VM et du stockage.

   {{< screenshot src="updates/xcp-hl-5-up-to-date.png" alt="L'onglet Patches avec l'hôte entièrement à jour" >}}

### Tester une mise à jour sur un pool de laboratoire à un hôte {#host-patch-pilot}

Faites votre première mise à jour d’hôte sur un pool de laboratoire que vous pouvez réinstaller, pas sur un pool dont vous dépendez. Un test sur un seul hôte ne montre pas le comportement d’un pool à plusieurs hôtes pendant une mise à jour.

**Avant de commencer**

- Utilisez un **pool de laboratoire à un seul hôte** dont vous connaissez la version, sans VM ordinaire, sans tâche de sauvegarde en cours, sans HA et sans appliance XOA-HL exécutée sur cet hôte.
- Gardez une console d’hôte séparée, un plan de récupération de l’hôte et du réseau, et une connexion XOA-HL distincte.
- Réservez une fenêtre approuvée pour l’ensemble des paquets (standard et HomeLab). Décidez du redémarrage séparément.

1. Notez les versions de l’image, du paquet et de XO ci-dessus, les UUID de l’hôte et du pool, le maître, l’adresse de gestion, les versions des paquets installés, les ID des dépôts activés, l’état d’alimentation et d’activation de l’hôte, et la liste exacte des paquets en attente. Sur la **console de l’hôte**, lancez `yum check-update` et comparez avec l’onglet **Patches**. Arrêtez-vous si la vérification échoue ou si la liste est inattendue. `yum check-update` peut renvoyer le code 100 quand des mises à jour existent ; c’est normal.
2. Dans le **navigateur XOA-HL**, ouvrez `/#/hosts/<host-id>/patches`, choisissez **installer tous les patchs**, vérifiez l’hôte et confirmez une seule fois. Sélectionner une ligne ne limite pas la mise à jour à ce paquet. Notez l’ID de la tâche, ses heures de début et de fin, et toute sortie ou erreur. Ne cliquez pas de nouveau pendant une déconnexion temporaire, et ne lancez pas de mise à jour en ligne de commande en même temps.
3. Quand la tâche se termine, comparez avec vos notes, depuis la console séparée et l’inventaire XOA-HL actualisé : versions installées, correctifs restants, accès à l’hôte, état d’activation et d’alimentation, réseau de gestion et attachements des SR. Si la tâche a échoué ou si la connexion n’est pas revenue, conservez les journaux et l’état réel des paquets. Une mise à jour partielle demande le plan de récupération ou de réinstallation du responsable de l’hôte : ne supposez pas qu’elle a été annulée.
4. Si l’interface indique qu’un redémarrage est requis, prévoyez un redémarrage **distinct** et approuvé pendant que le pool est vide. Vérifiez qu’aucune VM ni tâche de sauvegarde n’est apparue, puis choisissez une seule fois **Redémarrer pour appliquer les mises à jour** dans l’onglet Patches de l’hôte. N’acceptez aucune proposition de forcer le redémarrage ou de contourner une suspension bloquée, une sauvegarde ou une vérification de version. Attendez le retour de l’hôte sur la console séparée, puis vérifiez de nouveau la connexion XOA-HL, les paquets, l’indication de redémarrage, le réseau et les SR. Si le bouton ou la tâche se comporte de façon inattendue, arrêtez-vous et notez-le. Ne forcez pas un second redémarrage.

**Vérification :** l’hôte est joignable, ses paquets ont les versions attendues, aucun correctif ne reste et aucun redémarrage n’est en attente. Conservez les listes de paquets d’avant et d’après, les sorties de la tâche et de la console, les erreurs exactes, la décision de redémarrage et la connectivité finale. Les installations interrompues, la récupération et la disponibilité d’un pool de production ou à plusieurs hôtes ne sont pas traitées ici. La [maintenance avec évacuation des VM](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) est une tâche distincte, avec une VM de test en marche ; le bouton des correctifs ne l’effectue pas.

### En ligne de commande

Sur l'hôte :

```bash
yum check-update                   # ce qui est disponible
yum update xcp-hl-release          # la configuration des dépôts elle-même
yum update xo-lite-ce xoa-proxy    # uniquement les paquets XCP-hl
yum update                         # tout, comme l'onglet Patches
```

### Fonctionnement

XCP-ng fournit un greffon XAPI, `updater.py`, auquel Xen Orchestra demande
la liste des mises à jour disponibles. XOA-hl est modifié pour inclure les
dépôts XCP-hl dans cette demande : c'est pourquoi les paquets XCP-hl
apparaissent à côté de ceux de XCP-ng standard.

Les dépôts sont définis dans un seul fichier,
`/etc/yum.repos.d/xcp-hl.repo`, propriété du paquet `xcp-hl-release` :

| Identifiant du dépôt | Contenu | Publié depuis |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{{< callout type="error" >}}
Ne renommez pas les sections de ce fichier. Xen Orchestra transmet ces
identifiants de dépôt à `updater.py`, qui ne liste les mises à jour que pour
les dépôts qu'on lui a indiqués. Une section renommée ne provoque aucune
erreur : ses paquets disparaissent simplement, sans bruit, de l'onglet
Patches.
{{< /callout >}}

Les réglages des dépôts sont livrés sous forme de paquet pour que leurs modifications atteignent les hôtes déjà installés, plutôt que de dépendre d’un fichier copié une seule fois. Une modification atteint votre hôte via
`yum update xcp-hl-release`.

### Première configuration sur un hôte existant

Les hôtes installés depuis une ISO antérieure au paquet `xcp-hl-release`
demandent une initialisation unique. Ensuite, yum gère la configuration.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://rpm.xcp-hl.org/xcp-hl.repo

rpm --import https://rpm.xcp-hl.org/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

L'installation du paquet remplace le fichier que vous venez de télécharger
par la copie empaquetée, en conservant la vôtre sous le nom
`xcp-hl.repo.rpmorig`. Les deux ne diffèrent que par l'endroit d'où elles
lisent la clé de signature : la copie téléchargée la récupère en HTTPS, la
copie empaquetée utilise la clé locale que le paquet installe.

Les ISO plus récentes incluent déjà `xcp-hl-release` : cette étape ne les
concerne donc pas.

### Revenir en arrière

Chaque dépôt ne publie que ses versions les plus récentes, ce qui limite
jusqu'où vous pouvez revenir. Pour revenir à un build antérieur :

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<version>
```

## Mettre à jour XOA-hl (l’interface d’administration) {#mettre-à-jour-xoa-hl-lappliance}

### Dans Xen Orchestra

1. **Ouvrir la page de mise à jour.** Dans l'interface web de XOA-hl, allez
   dans `Settings > XOA-HL Updates`. Elle affiche la version installée. Tant
   qu'aucune vérification n'a été lancée, le statut indique *Update status
   unknown*.

   {{< screenshot src="updates/xoa-hl-1-update-tab.png" alt="La page XOA-HL Updates avant toute vérification" >}}

2. **Cliquer sur Check for update.** La page liste chaque paquet qui a une
   mise à jour disponible, avec sa version.

   {{< screenshot src="updates/xoa-hl-2-check-result.png" alt="Le résultat de la vérification : mises à jour disponibles, avec la liste des paquets" >}}

3. **Cliquer sur Update now.** Le journal de la mise à jour s'affiche dans la
   page au fur et à mesure. La mise à jour redémarre xo-server : la page
   affiche brièvement *Reconnecting*, puis reprend d'elle-même.

   {{< screenshot src="updates/xoa-hl-3-in-progress.png" alt="Une mise à jour en cours, avec son journal qui défile" >}}

   {{< callout type="warning" >}}
   **Update now** installe tous les paquets en attente sur l'appliance, y
   compris AlmaLinux et le noyau, pas seulement `xoa-hl`. Dans ce20, le mécanisme de mise à jour exclut Node.js.
   {{< /callout >}}

4. **Terminé.** Une fois la mise à jour finie, relancez une vérification :
   la page indique *Up to date*.

   {{< screenshot src="updates/xoa-hl-4-up-to-date.png" alt="La page XOA-HL Updates indiquant que l'appliance est à jour" >}}

### En ligne de commande

Sur l'appliance :

```bash
dnf check-update         # ce qui est disponible
dnf update xoa-hl        # l'application de l'appliance seule
dnf update --exclude=nodejs  # l'application et la base AlmaLinux ensemble
```

### Fonctionnement

L'appliance a son propre dépôt yum, défini dans
`/etc/yum.repos.d/xoa-hl.repo`, fourni par le paquet `xoa-hl` lui-même :

| Identifiant du dépôt | Contenu | Publié depuis |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

Les deux boutons de la page de mise à jour démarrent deux unités systemd :

| Unité | Rôle |
|---|---|
| `xoa-hl-check-update.service` | Exécute `dnf check-update` et écrit le résultat dans `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Exécute un `dnf -y --refresh --exclude=nodejs update` complet, journalisé dans `/var/lib/xoa-hl/update.log` |

### Vérifications et mises à jour automatiques

Dans la release `xoa-hl` `v5.113.2_e281c536-ce20`, **Settings → XOA-HL Updates → Automatic updates** propose trois modes :

| Mode | Fonctionnement |
|---|---|
| Manual only | Un administrateur lance les vérifications et les installations ; c’est le mode par défaut. |
| Check automatically | Les vérifications planifiées actualisent l’état ; l’installation reste manuelle. |
| Install automatically | Vérifie et installe pendant la fenêtre de maintenance définie, après confirmation explicite. |

Choisissez la fréquence, le jour (si hebdomadaire) et l’heure locale, puis enregistrez. Les horaires utilisent le **fuseau de l’appliance**, et l’exécution démarre à l’heure choisie, sans délai aléatoire. Depuis `v5.113.2_e281c536-ce40`, une exécution automatique en échec s’affiche dans un bandeau rouge sur la page. L’installation ou la mise à jour du RPM n’active pas l’installation automatique. Les anciens paquets peuvent ne pas afficher ces commandes : vérifiez d’abord la version installée.

Le mécanisme de mise à jour exclut Node.js et conserve sa version majeure prise en charge. Les mises à jour peuvent redémarrer des services, dont xo-server. Il n’y a **aucun redémarrage automatique de la VM** ; une fenêtre d’installation manquée n’est pas rattrapée au démarrage. Vérifiez le résultat et organisez les redémarrages nécessaires. La [référence de planification versionnée](https://github.com/Vagrantin/xoa-hl/blob/v5.113.2_e281c536-ce40/docs/automatic-updates.md) détaille la configuration en ligne de commande et le diagnostic.

### Revenir en arrière

Les dépôts actuellement activés peuvent proposer des paquets plus anciens :

```bash
dnf --showduplicates list xoa-hl
```

La disponibilité évolue. Pour `v5.113.2_e281c536-ce40`, la rétrogradation de paquet et la récupération de configuration entre versions ne sont pas validées comme procédures de récupération de l’appliance. Une rétrogradation n’annule pas les mises à jour du système de base et ne restaure ni les données XO ni vos fichiers. Préparez un export et un test isolé avec le [guide de configuration](/docs/xoa-hl/configuration-backup/) avant de prévoir un retour arrière.

## Vérification et confiance

Les paquets et les métadonnées des dépôts de XCP-hl comme de XOA-hl sont
signés avec la clé GPG XCP-hl. La configuration côté client définit
`repo_gpgcheck=1` avec `gpgcheck=0`.

Les RPM sont signés par une **sous-clé** GPG, pas par la clé maîtresse, et
l'outil `rpm` du système hôte de XCP-ng 8.3 (version 4.11) a une limite
connue à ce sujet : lors de l'import d'une clé, il n'enregistre que la clé
maîtresse. Il signale donc `NOKEY` pour une signature de sous-clé et ne peut
pas vérifier le paquet directement, même si la signature est authentique.

La confiance passe donc par les métadonnées du dépôt. Le véritable outil
GPG, qui comprend les sous-clés, vérifie `repomd.xml`. Ce fichier enregistre
une empreinte de `primary.xml`, qui à son tour enregistre une empreinte de
chaque paquet : vérifier un seul fichier, `repomd.xml`, vérifie donc tous les
RPM du dépôt.

{{< callout type="warning" >}}
Les sous-clés de signature expirent le **10 mai 2027**. Passé cette date, la
vérification échoue tant qu'elles n'ont pas été prolongées, que la clé
publiée n'a pas été rafraîchie et qu'elle n'a pas été réimportée sur chaque
hôte.
{{< /callout >}}

## Limitations connues

Pour le périmètre de l’appliance examiné à `v5.113.2_e281c536-ce40`, la récupération après interruption et la rétrogradation nécessitent encore une validation en laboratoire jetable. Consultez la [maintenance](/docs/xoa-hl/maintenance/) pour vérifier les résultats et décider des redémarrages.

{{< callout type="info" >}}
N'oubliez pas que cette distribution est en version alpha. Lisez les notes
de version avant de mettre à jour : des changements incompatibles sont
attendus à chaque version, et une mise à jour peut nécessiter une
intervention manuelle.
{{< /callout >}}
