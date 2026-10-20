---
title: "Maintenir l’appliance à jour"
linkTitle: "Maintenance de l’appliance"
description: "Relevez les versions installées, préparez une fenêtre de mise à jour, mettez à jour l’appliance et vérifiez le résultat."
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: draft
sourceRevision: sha256:faec682dbf31ac568cdf40e0b931f9398b8700df7012c927d2894e6c7d80bb3b
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Mettez à jour l’appliance XOA-HL en quatre étapes : relevez ce qui est installé, préparez une fenêtre de maintenance, choisissez le mode de mise à jour, puis vérifiez le résultat. Vous travaillez dans le **navigateur**, connecté à XOA-HL en tant qu’administrateur. Quelques vérifications en lecture seule se font **dans l’appliance**, par sa console ou en SSH.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261009-5f33c81`, paquet `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Les paquets ultérieurs peuvent se comporter différemment.
{{< /callout >}}

## 1. Relever l’état de départ {#record-versions}

1. Dans le navigateur, ouvrez **À propos** (`/#/about`) en tant qu’administrateur.
2. Notez la **Version de XOA-HL**, la **Version de la VM XOA-HL**, l’adresse de l’appliance et le tag de l’image d’origine. La version de la VM identifie la construction de l’image. Mettre à jour l’application ne la change pas.

Si vous disposez d’un accès console ou SSH autorisé, exécutez ces commandes en lecture seule dans l’appliance. Utilisez les privilèges root si nécessaire.

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

Conservez la sortie avec la [matrice des versions](/docs/reference/release-matrix/) et les [notes de version](/docs/reference/changelog/). La matrice liste les composants livrés ensemble ; elle ne prouve pas qu’ils ont été testés ensemble.

## 2. Préparer la fenêtre de mise à jour {#prepare-window}

- [Exportez la configuration XO](/docs/xoa-hl/configuration-backup/). Conservez le fichier et sa phrase secrète hors de l’appliance.
- Notez à part vos modifications de `/root/.config/xo-server/config.toml`, des fichiers TLS et de `/etc/xoa-hl/update.conf`. L’export web ne comprend pas ces fichiers.
- Vérifiez que vous pouvez ouvrir la console de l’appliance par XO Lite, au cas où l’interface web serait indisponible.
- Vérifiez que les sauvegardes, les restaurations et les autres tâches de gestion sont terminées.
- Prévoyez une fenêtre assez longue pour un redémarrage du service et, si besoin, un redémarrage ultérieur de l’appliance.

Cette page met à jour uniquement la VM XOA-HL. La mise à jour des hôtes est une tâche distincte : voir le [guide de mise à jour](/docs/guides/updates/) pour la bonne cible et les bonnes commandes.

## 3. Choisir le mode et le canal {#update-mode-channel}

Ouvrez **Paramètres → Mises à jour XOA-HL** (`/#/settings/xoa-hl-updates`). Pour une mise à jour manuelle, suivez la [procédure de mise à jour](/docs/guides/updates/) pour **Rechercher des mises à jour** et **Mettre à jour maintenant**.

Choisissez un **Mode** :

| Mode | Ce que vous faites |
| --- | --- |
| Manuel uniquement | Vous lancez vous-même chaque vérification et chaque installation. C’est le mode par défaut |
| Vérification automatique | Les vérifications suivent une planification. Vous décidez quand installer |
| Installation automatique | L’installation suit une planification. Utilisez ce mode seulement après avoir approuvé explicitement l’installation dans votre fenêtre de maintenance |

Pour un mode planifié :

1. Vérifiez le **Fuseau horaire de l'appliance**. La planification utilise ce fuseau, et non celui de l’hôte ou du navigateur. Comparez-le avec la sortie de `timedatectl`.
2. Réglez la **Fréquence**, le **Jour** pour une planification hebdomadaire, l’**Heure de début locale** et le **Délai aléatoire**. Le délai aléatoire s’ajoute après l’heure de début.
3. Sélectionnez **Enregistrer les paramètres de mise à jour automatique**.
4. Vérifiez les réglages enregistrés, ainsi que la liste des timers donnée par `systemctl list-timers 'xoa-hl-*'`.

Dans **Canal de mise à jour**, gardez **Stable** pour la maintenance habituelle. **Test** ajoute des paquets candidats : utilisez-le seulement sur une appliance de test jetable. Changer de canal n’installe rien et ne rétrograde pas un paquet candidat déjà installé.

La mise à jour gérée lance une mise à jour `dnf` complète, sauf pour `nodejs`. L’installation du paquet applicatif redémarre `xo-server` après la transaction : la page web peut donc se déconnecter. Cela seul ne signifie pas que la mise à jour a échoué.

## 4. Vérifier le résultat {#check-result}

1. Reconnectez-vous à l’interface web et ouvrez **À propos**. Vérifiez que la page affiche la version attendue de l’application.
2. Vérifiez que les hôtes attendus sont connectés et que leur inventaire apparaît.
3. Lisez le résultat de la mise à jour.

Si le résultat n’est pas clair, exécutez ces vérifications en lecture seule dans l’appliance :

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| Fichier ou valeur | Ce qu’il indique |
| --- | --- |
| `/run/xoa-hl/status` | La dernière vérification : `UP_TO_DATE`, `AVAILABLE` ou `ERROR`. Perdu au redémarrage de l’appliance |
| `/var/lib/xoa-hl/update.log` | La sortie de l’installation gérée, terminée par un marqueur de succès ou d’échec. Écrasé à la tentative suivante |
| `/var/lib/xoa-hl/auto-update.status` | Exécutions automatiques uniquement. Comparez `startedAt` et `finishedAt` (UTC) avec l’heure de votre mise à jour |
| `result=check_failed` ou `result=failed` | La vérification ou l’installation a échoué : lisez son journal. Aucune des deux valeurs ne signifie un succès |
| `rebootNeeded=yes`, `no` ou `unknown` | L’évaluation de l’exécution automatique. `unknown` ne signifie pas qu’aucun redémarrage n’est nécessaire |

Une installation manuelle ne met **pas** à jour l’enregistrement de l’exécution automatique. Le service de vérification peut se terminer sans erreur et signaler quand même un problème : lisez donc son résultat. Conservez les journaux utiles avant de réessayer.

**Vérification :** **À propos** affiche la version attendue, les hôtes attendus sont connectés et le résultat de la mise à jour indique un succès.

## Si la mise à jour ne se termine pas normalement {#update-problems}

Il n’y a **aucun redémarrage automatique**. La vérification et l’installation gérées partagent un verrou, mais une commande `dnf` lancée depuis un shell échappe à ce verrou. Tant qu’une mise à jour peut être en cours, ne lancez jamais un autre processus `dnf`, n’arrêtez pas une transaction en cours et ne redémarrez pas pour débloquer l’outil de mise à jour.

| Problème | À vérifier |
| --- | --- |
| Seul le navigateur s’est déconnecté | L’installation de l’application redémarre `xo-server`. Vérifiez le service et le journal par la console avant de réessayer. |
| L’outil de mise à jour semble occupé | Vérifiez le service et le journal par la console. Ne lancez pas un autre `dnf`, n’arrêtez pas la transaction et ne redémarrez pas pour le débloquer. |
| Une fenêtre d’installation automatique a été manquée | L’installation manquée ne s’exécute pas immédiatement au redémarrage de l’appliance. Prévoyez une autre fenêtre. |
| Le démarrage de l’appliance a été interrompu, ou le résultat n’est pas clair | Conservez les journaux, puis consultez le [guide de dépannage](/docs/xoa-hl/troubleshooting/) avant de prévoir une autre mise à jour. |
| Les changements installés pourraient demander un redémarrage | Redémarrez seulement quand aucune transaction ni tâche de gestion n’est en cours, et après avoir décidé que les changements le demandent. Vérifiez ensuite de nouveau la connexion, les versions et l’inventaire. |
| Vous voulez revenir à la version précédente | Rétrograder un paquet n’est pas une procédure de récupération testée. Cela ne restaure ni le système de base, ni les données XO, ni vos propres fichiers. Lisez d’abord les [limites de récupération](/docs/xoa-hl/configuration-backup/#recovery-limits). |

{{< details title="Sources" closed="true" >}}
- **Outil de mise à jour de l’appliance** : [planification](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [script d’installation](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-update.sh), [état de l’exécution automatique](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-auto-update.sh), [résultat de la vérification](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [spec du paquet](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [correctif du canal](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzz-xoa-hl-update-channel.patch).
{{< /details >}}
