---
title: Maintenir l’appliance XOA-HL
description: Relever les versions, préparer la maintenance et vérifier le résultat des mises à jour.
weight: 40
translationKey: xoa-manual-maintenance
translationStatus: draft
sourceRevision: sha256:932a5f12913363b83e6146fc55c12988da0d9d6c7e314afb19653f8b4996cea1
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Préparez une mise à jour de l’appliance avec un export de configuration, un accès console et un moyen de vérifier le résultat après la reconnexion de l’interface web.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests d’interruption et de redémarrage sur une appliance jetable restent à faire. Les paquets ultérieurs peuvent différer.
{{< /callout >}}

## 1. Relever l’état initial

Dans le **navigateur**, ouvrez **About** (`/#/about`) en administrateur. Relevez **XOA-HL version**, **XOA-HL VM version**, l’adresse de l’appliance et le tag de l’image d’origine. La version de la VM identifie la construction de l’image ; mettre à jour l’application ne remplace pas cette identité.

Si vous disposez d’un accès console ou SSH autorisé, exécutez ces commandes de lecture **dans l’appliance**, avec les privilèges root lorsque nécessaire :

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

Conservez la sortie avec la [matrice des versions](/docs/reference/release-matrix/) et les [notes de version](/docs/reference/changelog/). La matrice indique les composants livrés, pas une compatibilité testée.

## 2. Préparer la fenêtre

- [Exportez la configuration XO](/docs/xoa-hl/configuration-backup/) et conservez le fichier et la phrase secrète hors de l’appliance.
- Consignez séparément vos modifications de `/root/.config/xo-server/config.toml`, les éléments TLS et `/etc/xoa-hl/update.conf`. L’export web ne comprend pas ces fichiers.
- Vérifiez que la console de l’appliance reste accessible par XO Lite si l’interface web devient indisponible.
- Vérifiez que les sauvegardes, restaurations et autres tâches de gestion sont terminées. Prévoyez une fenêtre permettant un redémarrage du service et, si nécessaire, un redémarrage ultérieur de l’appliance.

L’outil de mise à jour de l’appliance agit dans la VM XOA-HL. Les mises à jour de l’hôte sont une opération distincte : utilisez le [guide existant](/docs/guides/updates/) pour choisir la bonne cible et les commandes.

## 3. Choisir le mode et le canal

Ouvrez **Settings → XOA-HL Updates** (`/#/settings/xoa-hl-updates`). Suivez la [procédure canonique](/docs/guides/updates/) pour **Check for update** et **Update now**.

| Mode | Votre organisation |
| --- | --- |
| Manual only | Lancez vous-même chaque vérification et installation ; mode initial par défaut |
| Check automatically | Vérifications planifiées ; choisissez quand installer manuellement |
| Install automatically | Approuvez explicitement l’installation planifiée dans votre fenêtre de maintenance |

La planification utilise le **fuseau horaire de l’appliance**, avec le délai aléatoire choisi après l’heure de début. Comparez le fuseau affiché à `timedatectl` ; celui de l’hôte ou du navigateur n’est pas la référence. Enregistrez la fréquence, le jour pour une fréquence hebdomadaire, l’heure et le délai, puis vérifiez les réglages enregistrés et la liste des timers.

Gardez le canal **stable** pour la maintenance habituelle. **Testing** ajoute des paquets candidats et doit servir sur une appliance de test jetable. Changer de canal n’installe aucun paquet et ne rétrograde pas un candidat déjà installé.

La mise à jour gérée lance une mise à jour `dnf` complète en excluant `nodejs`. L’installation du paquet applicatif redémarre `xo-server` après la transaction ; une page web déconnectée ne prouve donc pas un échec.

## 4. Vérifier le résultat

Reconnectez-vous à l’interface web, ouvrez **About** et vérifiez la version attendue de l’application. Confirmez la connexion de l’inventaire de l’hôte prévu et lisez le résultat de la mise à jour. En cas de doute, utilisez ces vérifications de lecture dans l’appliance :

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| Indice | Interprétation |
| --- | --- |
| `/run/xoa-hl/status` | Dernière vérification : `UP_TO_DATE`, `AVAILABLE` ou `ERROR` ; disparaît au redémarrage |
| `/var/lib/xoa-hl/update.log` | Sortie de l’installation gérée et marqueur final de succès/échec ; écrasé à la tentative suivante |
| `/var/lib/xoa-hl/auto-update.status` | Exécution automatique uniquement ; comparez `startedAt` et `finishedAt` (UTC) à votre opération |
| `result=check_failed` ou `result=failed` | Examinez le journal de vérification ou d’installation ; aucun ne signifie un succès |
| `rebootNeeded=yes`, `no` ou `unknown` | Évaluation de l’exécution automatique ; `unknown` ne confirme pas l’absence de redémarrage nécessaire |

Une installation manuelle ne met **pas** à jour l’enregistrement automatique. La réussite du service de vérification ne remplace pas la lecture de son verdict. Conservez les journaux utiles avant une autre tentative.

## 5. Gérer une déconnexion ou une fenêtre manquée

Si seul le navigateur s’est déconnecté, examinez le service et le journal par la console avant de réessayer. Ne lancez pas un autre `dnf`, n’arrêtez pas une transaction active et ne redémarrez pas pour débloquer l’outil. La vérification et l’installation gérées partagent un verrou ; une transaction lancée directement dans le shell échappe à cette coordination.

Il n’y a **aucun redémarrage automatique**. Une fenêtre d’installation automatique manquée n’est pas rejouée immédiatement au démarrage. Après un démarrage interrompu ou un résultat incertain, conservez les journaux et [consultez le dépannage](/docs/xoa-hl/troubleshooting/) avant de planifier une autre mise à jour. Redémarrez seulement après avoir confirmé qu’aucune transaction ni tâche de gestion n’est active et déterminé que les changements installés le nécessitent ; vérifiez ensuite connexion, versions et inventaire.

Rétrograder un paquet n’est pas une procédure de récupération de l’appliance vérifiée. Cela ne restaure ni le système de base, ni les données XO, ni vos fichiers. Lisez les [limites de configuration et de récupération](/docs/xoa-hl/configuration-backup/) avant de prévoir un retour arrière.

## Sources

Sources examinées à `xoa-hl@5f33c81` : [planification](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [installation](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-update.sh), [état automatique](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-auto-update.sh), [verdict de vérification](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [cycle du paquet](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec) et [correctif du canal](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzz-xoa-hl-update-channel.patch).
