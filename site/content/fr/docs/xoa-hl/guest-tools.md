---
title: "Installer les outils invités Linux"
linkTitle: "Outils invités"
description: "Installez l’agent de gestion dans une VM invitée Linux et vérifiez ce qu’affiche XOA-HL."
weight: 41
translationKey: xoa-manual-guest-tools
translationStatus: draft
sourceRevision: sha256:b33c81ebb5d81c67bc786f64145b80c80a063e3836134f53b46590995ecf327e
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Installez l’agent de gestion dans une VM invitée Linux, vérifiez ce qu’en affiche XOA-HL et testez un arrêt propre. L’agent s’exécute dans l’invité, pas dans XOA-HL. Les étapes prennent pour exemple un invité Ubuntu 24.04, dont le paquet a été vérifié ; les autres distributions Linux fournissent l’agent par leurs propres paquets. Vous utilisez l’**appliance XOA-HL** dans votre navigateur, connecté en tant qu’administrateur, et vous lancez des commandes dans la console de l’invité. Suivez les sections dans l’ordre. Les autres systèmes, dont Windows, demandent leur propre procédure.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Paquet invité : `xe-guest-utilities` `7.20.2-0ubuntu1` pour Ubuntu 24.04 LTS (Noble), amd64.
{{< /callout >}}

## Avant de commencer

- Utilisez une VM de test Ubuntu 24.04 amd64 fraîchement installée et sans données importantes, par exemple celle de [Créer votre première machine virtuelle](/docs/xoa-hl/create-vm/). Il vous faut une console qui fonctionne et un compte invité autorisé à utiliser `sudo`.
- Notez l’UUID complet de la VM, son hôte, l’OS et le noyau de l’invité, et les versions installées de l’hôte et de l’appliance. Le nom d’un modèle ne suffit pas à savoir quel OS est installé.
- Utilisez un compte administrateur XOA-HL. Démarrer et arrêter une VM demande la permission **operate** sur cette VM. Gérer les paquets de l’invité est un droit distinct : la connexion à XOA-HL ne vous donne pas `sudo` dans l’invité.
- Prévoyez une fenêtre de maintenance pour le test d’arrêt. Enregistrez votre travail dans l’invité et retirez la VM des tâches planifiées. Avant de modifier un invité important, faites une [sauvegarde indépendante et testez une restauration isolée](/docs/xoa-hl/backup-restore/).
- L’invité doit avoir un DNS qui fonctionne, l’heure juste et l’accès à ses dépôts Ubuntu Noble approuvés, dont `universe`. Utilisez un réseau de laboratoire approuvé. Ne modifiez pas le réseau de gestion de l’hôte pour atteindre un miroir de paquets. Ce guide n’ajoute pas de dépôt et n’utilise pas d’ISO d’outils.

Lancez les commandes de cette page **dans la console de l’invité** uniquement, jamais sur l’hôte XCP-HL ni sur l’appliance XOA-HL. Lisez l’état de la VM et utilisez ses boutons d’alimentation dans votre **navigateur**, à l’adresse de l’appliance.

## Vérifier l’état des outils invités {#guest-tools-status}

1. Dans le navigateur, ouvrez la VM dont vous avez noté l’UUID et vérifiez qu’elle est **Running**.
2. Ouvrez **Général** (`/#/vms/<id>/general`). Notez le mode de virtualisation, le message des outils et l’adresse IP affichée.
3. Ouvrez **Avancé** et repérez **OS invité**. Notez **Management agent version**, **Nom de l'OS** et **Kernel de l'OS**. Ne modifiez rien dans ces onglets.
4. Dans la console de la VM, lancez ces commandes et notez le résultat :

   ```bash
   cat /etc/os-release
   uname -r
   dpkg --print-architecture
   systemd-detect-virt
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl status xe-daemon.service --no-pager
   ```

   Un paquet absent ou un service inactif est un résultat à noter. Ce n’est pas une raison pour lancer les commandes sur une autre machine.

**Vérification :** l’OS est Ubuntu `24.04`, l’architecture est `amd64`, et `systemd-detect-virt` affiche `xen`. Sinon, arrêtez-vous et utilisez une procédure écrite pour ce système. Si les outils sont déjà installés, notez l’origine et la version du paquet, puis passez à [Vérifier ce qu’affiche XOA-HL](#check-reporting). Ne les réinstallez pas et ne les mettez pas à jour juste pour correspondre à cet exemple.

### Ce que signifie le message des outils

Le message de **Général** n’apparaît que si la VM est **Running** et que XO dispose d’informations sur les pilotes. XO vérifie d’abord les pilotes PV, puis l’agent de gestion, puis si l’agent est à jour. Il affiche le premier message qui s’applique :

| Message | Ce qu’il signifie |
| --- | --- |
| **Pas de Xen tools détectés** | Les pilotes PV ne sont pas détectés |
| **Management agent not detected** | Les pilotes sont détectés, mais pas l’agent |
| **Management agent {version} out of date** | L’agent est détecté, mais signalé comme obsolète |
| **Management agent {version} detected** | L’agent est détecté et signalé comme à jour |

L’absence de message ne prouve pas que les outils sont installés. Un agent détecté ne teste ni vos applications, ni la connectivité, ni la sécurité.

Les pilotes PV du noyau Linux et l’agent de gestion (un programme dans l’invité) ont des rôles différents. Le paquet Ubuntu ci-dessous installe l’agent ; il ne remplace pas les pilotes du noyau. La version de l’agent affichée par XO vient des métriques invitées de l’hôte et peut différer de la version du paquet Ubuntu. Notez les deux. Ne rétrogradez pas et ne réinstallez pas seulement parce qu’elles s’écrivent différemment. Vérifiez séparément les pilotes, l’agent et vos applications.

## Installer l’agent de gestion dans un invité Linux {#install-linux-agent}

Utilisez un invité sans outils déjà installés. Si une ISO d’outils, l’agent d’un fournisseur ou un autre paquet est déjà utilisé, déterminez d’abord qui le maintient et comment il est mis à jour.

1. Dans la console de l’invité, actualisez la liste des paquets, vérifiez d’où viendrait le paquet et simulez l’installation :

   ```bash
   sudo apt-get update
   apt-cache policy xe-guest-utilities
   apt-get -s install xe-guest-utilities
   ```

2. Vérifiez que le candidat vient du dépôt Ubuntu Noble attendu. Ce guide a été vérifié avec la version `7.20.2-0ubuntu1`. Examinez toute autre version ou origine avant de continuer.
3. Arrêtez-vous en cas d’erreur de dépôt ou de signature, d’absence de candidat, ou de suppressions ou mises à jour inattendues. Ne contournez pas les vérifications et n’ajoutez pas de dépôt sans rapport.
4. Installez le paquet. Lisez les changements proposés avant de les accepter :

   ```bash
   sudo apt-get install xe-guest-utilities
   ```

5. Activez et démarrez le service, puis vérifiez le paquet et le service :

   ```bash
   sudo systemctl enable --now xe-daemon.service
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl is-enabled xe-daemon.service
   systemctl is-active xe-daemon.service
   ```

**Vérification :** l’état du paquet est `install ok installed`, et le service est `enabled` et `active`. Sur Ubuntu Noble, le service s’appelle **`xe-daemon.service`**. Il dépend de `proc-xen.mount`, et systemd ne le démarre que si ses conditions de virtualisation Xen et de chemins sont remplies. N’utilisez pas à la place le nom générique `xe-linux-distribution.service`. Un installateur terminé ou un service activé ne prouve pas à lui seul que l’agent fonctionne. Cette étape ne demande aucun redémarrage et ne supprime aucun paquet.

## Vérifier ce qu’affiche XOA-HL {#check-reporting}

1. Dans le navigateur, actualisez **Général** et **Avancé** pour la même VM en marche. Notez le message des outils, la version de l’agent, l’OS et le noyau.
2. Comparez l’OS et le noyau avec ce que montre la console de l’invité.
3. Comparez l’adresse IP affichée avec l’interface prévue de l’invité et son adresse actuelle.

Si le message indique toujours un agent absent ou obsolète alors que `systemctl` affiche `active`, le problème n’est pas résolu. Notez exactement ce que vous voyez, et ne considérez pas le test comme réussi.

**Pas d'enregistrement IPv4** seul ne prouve pas une panne de l’agent : un invité uniquement en IPv6, ou sans réseau, peut ne pas avoir d’adresse IPv4. Une adresse affichée ne prouve ni le routage, ni le DNS, ni l’accès SSH ou RDP. Vérifiez séparément les connexions dont l’invité a besoin.

## Tester un arrêt propre {#clean-shutdown}

1. Enregistrez tout le travail en cours dans l’invité.
2. Dans le navigateur, revérifiez l’UUID de la VM. Sélectionnez **Arrêter** une seule fois et lisez la confirmation.
3. Si XO propose de forcer l’arrêt ou de contourner une opération bloquée, annulez : ce n’est pas un arrêt propre. Notez l’erreur. Si l’invité répond encore, arrêtez-le normalement depuis l’invité. Ne répétez pas la demande pendant qu’une tâche est en cours.
4. Vérifiez dans la console que l’invité s’arrête, et que XOA-HL affiche **Halted** sans tâche d’arrêt en cours.
5. Sélectionnez une seule fois le bouton de démarrage, libellé **Créer** dans cette version. Connectez-vous par la console et vérifiez votre application ou votre fichier de test.
6. Refaites les vérifications du service (`systemctl is-enabled` et `systemctl is-active`) et [Vérifier ce qu’affiche XOA-HL](#check-reporting).

Notez les résultats de l’arrêt et du démarrage séparément de la détection de l’agent : l’un ne prouve pas l’autre.

**Vérification :** vous avez un résultat pour chaque point : le paquet et le service exacts, l’affichage actualisé dans XOA-HL, l’arrêt propre et le service après le redémarrage. Si un résultat manque ou a échoué, le test n’est pas terminé. Ce test ne couvre ni la migration à chaud, ni la mémoire dynamique, ni l’ajout de matériel à chaud, ni les snapshots cohérents (quiesce), ni le presse-papiers, ni les performances.

## En cas de problème

| Problème | À vérifier |
| --- | --- |
| Le paquet est absent ou vient d’une origine inattendue | Vérifiez l’OS et la version de l’invité, `apt-cache policy`, la disponibilité du dépôt approuvé `universe`, l’heure et le DNS, et les erreurs de mise à jour. Réglez le problème de dépôt avec son responsable. N’installez pas de paquet d’hôte ou d’appliance dans l’invité. |
| Le service est absent, inactif ou en échec | Vérifiez le paquet installé et ses fichiers avec `dpkg -L xe-guest-utilities`. Lisez `systemctl status xe-daemon.service proc-xen.mount --no-pager` et `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager`. Vérifiez les conditions Xen et les erreurs de dépendance avant de modifier la configuration. |
| Le service est actif, mais XO affiche un agent absent ou obsolète | Vérifiez l’identité de la VM, qu’elle est **Running**, et la connexion de l’hôte. Comparez les résultats du paquet et du service dans l’invité avec **Général** et **Avancé**, et l’heure de chacun. Ne redémarrez pas l’hyperviseur, ne masquez pas l’alerte et ne remplacez pas les pilotes à l’aveugle. |
| **Arrêter** échoue ou propose de forcer | Annulez le forçage ou le contournement. Gardez l’erreur exacte de la tâche et vérifiez la console de l’invité. Arrêtez depuis l’invité si possible. Une coupure forcée peut perdre des données et demande une décision distincte. |
| L’invité ne fonctionne plus après un changement | Conservez l’historique des paquets et les journaux de démarrage et du service. Utilisez la console de l’invité et votre plan de récupération distinct. Ce guide ne promet pas de retour arrière automatique par désinstallation ou rétrogradation. |

N’activez pas, ne redémarrez pas et ne réinstallez pas en boucle pour masquer une panne inexpliquée. [Signalez le problème](/docs/xoa-hl/troubleshooting/#report-a-problem) avec les versions, les ID de la VM et de l’hôte, les heures, l’origine et la version du paquet, l’état du service, les messages exacts et les résultats des tâches d’alimentation. Les journaux et les écrans de l’invité peuvent contenir des noms, des adresses ou des données privés : retirez-les du signalement, et gardez les preuves brutes privées.

Pour les mises à jour ultérieures, prévoyez une fenêtre de maintenance distincte pour l’OS et les paquets de l’invité, et refaites les mêmes vérifications. Non traités ici : les autres distributions Linux, l’installation depuis une ISO d’outils, les outils Windows ou BSD, le changement de fournisseur, la mise à jour ou la suppression du paquet, et une liste d’invités pris en charge. Ensuite, voir [Gérer les VM](/docs/xoa-hl/vm-operations/) et [Sauvegarder et restaurer une VM](/docs/xoa-hl/backup-restore/).

{{< details title="Sources" closed="true" >}}
- **État des outils et alimentation** : [ordre des messages des outils](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [champs OS invité](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [correspondance des métriques invitées](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [confirmations d’arrêt et de forçage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permission operate sur la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Build HomeLab** : [sélection des correctifs dans xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Paquet Ubuntu (vérifié le 2026-10-15)** : [paquet `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities), [liste des fichiers amd64](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist), [paquetage Debian](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`).
- **Contexte** : [outils invités Linux de XCP-ng](https://docs.xcp-ng.org/vms/#linux-guest-tools) (informations générales, pas une déclaration de compatibilité avec XCP-HL).
- **Libellés de l’interface** : [catalogues de libellés XO](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl), [repli de traduction HomeLab](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/compact-xo-locales.py).
{{< /details >}}
