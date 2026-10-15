---
title: Installer et vérifier les outils invités Linux
description: Installer l’agent de gestion Ubuntu 24.04 et vérifier les informations invitées et un arrêt propre.
weight: 21
translationKey: xoa-manual-guest-tools
translationStatus: draft
sourceRevision: sha256:8c9c47b718efc4436950f5657e77083f7fb3d379db7f776360f830647c2ca1e2
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Installez l’agent de gestion dans une VM Ubuntu 24.04 jetable, vérifiez les informations remontées dans XOA-HL et testez un arrêt normal de l’invité. Distinguez les pilotes du noyau, l’agent et la santé des applications.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources : image XOA-HL `xoa-image-20261009-5f33c81`, paquet `v5.113.2_e281c536-ce38`, XO 5.113.2 (`e281c536`). Le paquet invité étudié est `xe-guest-utilities` `7.20.2-0ubuntu1` pour Ubuntu 24.04 LTS (Noble), amd64. Le comportement sur invité/hôte installé et la revue humaine des traductions restent à valider. Ce n’est ni une matrice d’OS invités pris en charge ni une procédure pour Windows.
{{< /callout >}}

## Avant de commencer

- Utilisez une VM Ubuntu 24.04 amd64 jetable, fraîchement installée, par exemple celle du [premier exercice VM](/docs/xoa-hl/create-vm/), avec une console fonctionnelle et un compte invité autorisé à utiliser `sudo`. Notez UUID complet de VM, hôte, OS/noyau invité et versions installées de l’hôte/appliance. Le nom du template ne suffit pas à identifier l’OS installé.
- Utilisez un compte administrateur XOA-HL pour ce pilote. L’administration des paquets invités est une autorisation distincte ; démarrer/arrêter exige **operate** sur la VM. Une connexion au navigateur n’accorde pas `sudo` dans l’invité.
- Prévoyez une fenêtre de maintenance pour le test d’arrêt. Enregistrez le travail et excluez la VM jetable des tâches automatiques. N’y conservez pas de données importantes ; établissez une [sauvegarde indépendante avec restauration isolée](/docs/xoa-hl/backup-restore/) avant de modifier un invité important.
- L’invité doit avoir DNS et heure corrects et accès à ses dépôts Ubuntu Noble approuvés, dont `universe`. Utilisez un réseau de laboratoire approuvé ; ne modifiez pas le réseau de gestion de l’hôte pour accéder à un miroir. Ce guide n’ajoute pas de dépôt et n’utilise pas d’ISO d’outils.

Exécutez les commandes ci-dessous **dans la console de cet invité**, jamais sur l’hôte XCP-HL ni sur l’appliance XOA-HL. Les vérifications de gestion et commandes d’alimentation se font **dans le navigateur à l’adresse de l’appliance**.

## 1. Relever l’invité et l’état actuel des outils {#guest-tools-status}

1. Dans le navigateur, sélectionnez l’UUID enregistré et confirmez l’état **en cours** (`Running`). Ouvrez **Général** (`/#/vms/<vm-uuid>/general`) et notez le mode de virtualisation, le message des outils/de l’agent et l’IP indiquée. Ouvrez **Avancé → OS invité** et relevez **Management agent version**, **Nom de l’OS** et **Kernel de l’OS**. N’éditez pas les contrôles voisins.
2. Dans la console de cette VM, collectez les informations suivantes. Un paquet absent ou un service inactif est un résultat à noter, pas une raison d’exécuter ces commandes sur une autre machine.

```bash
cat /etc/os-release
uname -r
dpkg --print-architecture
systemd-detect-virt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
systemctl status xe-daemon.service --no-pager
```

**Vérification :** OS Ubuntu `24.04`, architecture `amd64`, virtualisation `xen`. Sinon, choisissez une procédure distincte vérifiée pour cet OS. Si les outils sont déjà installés, notez origine/version du paquet et utilisez les vérifications de remontée ci-dessous ; ne réinstallez pas ou ne mettez pas à jour uniquement pour correspondre à l’exemple.

Le message de Général est conditionnel. Il est masqué si la VM n’est pas en cours d’exécution ou si l’information de détection des pilotes manque. Sinon, le code vérifie d’abord les pilotes PV, puis l’agent, puis l’indicateur de mise à jour remonté. **Pas de Xen tools détectés**, **Management agent not detected**, **Management agent {version} out of date** et **Management agent {version} detected** correspondent à des états différents. Les messages de l’agent restent en anglais à ce pin. Un message absent ne prouve pas l’installation ; « détecté » ne valide ni application, ni connectivité, ni sécurité.

Les pilotes PV du noyau Linux et l’agent en espace utilisateur ont des rôles distincts. Le paquet Ubuntu ci-dessous fournit l’agent ; son installation ne remplace pas les pilotes du noyau. La version affichée par XO vient des métriques invitées de l’hôte et peut différer de la version du paquet Ubuntu. Conservez les deux valeurs ; ne rétrogradez pas ou ne réinstallez pas sur cette seule différence.

## 2. Installer l’agent de gestion Ubuntu {#install-linux-agent}

Pour cette étape, utilisez un invité sans outils déjà installés. Si une ISO d’outils, un agent fournisseur ou un autre paquet est déjà utilisé, clarifiez d’abord séparément son origine et sa méthode de mise à jour.

1. Actualisez les index des dépôts approuvés de l’invité et inspectez le candidat et la simulation :

```bash
sudo apt-get update
apt-cache policy xe-guest-utilities
apt-get -s install xe-guest-utilities
```

2. Confirmez que le candidat provient du dépôt Ubuntu Noble attendu. Le paquet vérifié dans les sources est `7.20.2-0ubuntu1` ; une autre version/origine exige une nouvelle analyse avant ce pilote. Arrêtez-vous en cas d’erreur de dépôt/signature, de candidat absent ou de suppressions/mises à jour inattendues. Ne contournez pas les vérifications et n’ajoutez pas de dépôt sans rapport.
3. Installez de manière interactive, lisez la transaction proposée puis activez et démarrez le service fourni :

```bash
sudo apt-get install xe-guest-utilities
sudo systemctl enable --now xe-daemon.service
dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
systemctl is-enabled xe-daemon.service
systemctl is-active xe-daemon.service
```

**Vérification :** état du paquet `install ok installed`, unité `enabled` et `active`. Noble fournit **`xe-daemon.service`**, dépendant de `proc-xen.mount` et soumis à des conditions de virtualisation/chemin Xen. Ne remplacez pas ce nom par le générique `xe-linux-distribution.service`. La fin du programme d’installation ou une unité activée ne prouve pas que l’agent fonctionne. Cette étape ne demande ni redémarrage ni suppression de paquet.

## 3. Vérifier les informations et un arrêt propre

1. Actualisez **Général** et **Avancé** de la même VM en cours d’exécution. Notez message des outils, version remontée de l’agent, OS et noyau. Comparez OS/noyau avec la console. Un message absent ou obsolète persistant reste non résolu même si `systemctl` indique active ; conservez les observations exactes sans valider le pilote.
2. Comparez toute IP remontée à l’interface prévue et son adresse actuelle. **Pas d’enregistrement IPv4** ne prouve pas seul une panne de l’agent : un invité uniquement IPv6 ou déconnecté peut ne pas avoir d’IPv4. Une adresse remontée ne prouve ni routage, ni DNS, ni accès SSH/RDP. Vérifiez séparément la connectivité nécessaire.
3. Enregistrez tout travail invité. Dans le navigateur, revérifiez l’UUID et utilisez une fois l’action normale **Arrêter**, en lisant la confirmation. Si XO propose un arrêt forcé ou le contournement d’une opération bloquée, **annulez** ; ce n’est pas un arrêt propre réussi. Notez l’erreur et utilisez l’arrêt normal de l’invité s’il répond encore. Ne répétez pas la demande pendant une tâche active.
4. Vérifiez l’arrêt dans la console et l’état **stoppé** (`Halted`) dans XOA-HL, sans tâche d’arrêt active. Démarrez une fois cette VM de test : le bouton hérité **Créer** correspond ici à **Start**, pas à la création d’une autre VM. Vérifiez connexion console et santé des applications/du fichier témoin, puis relevez à nouveau service et informations remontées. Conservez les observations arrêt/démarrage séparément de la détection de l’agent : aucune ne prouve l’autre.

**Vérification :** paquet/service exact, informations invitées actualisées, arrêt normal puis démarrage/persistance du service ont chacun un résultat enregistré. Si un élément manque ou échoue, laissez l’acceptation en attente. Ce test ne valide ni migration à chaud, mémoire dynamique, hotplug, snapshots quiescés, presse-papiers ni performances.

## En cas de problème

| Symptôme | Vérification et action suivante |
| --- | --- |
| Paquet absent ou origine inattendue | Vérifiez OS/version invité, `apt-cache policy`, disponibilité approuvée de `universe`, heure/DNS et erreurs de mise à jour. Résolvez le problème de dépôt avec son responsable ; n’installez pas de paquet hôte/appliance dans l’invité. |
| Unité absente, inactive ou en échec | Confirmez paquet et fichiers avec `dpkg -L xe-guest-utilities`. Lisez `systemctl status xe-daemon.service proc-xen.mount --no-pager` et `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager`. Vérifiez conditions Xen et dépendances avant de modifier la configuration. |
| Service actif, mais informations XO absentes/obsolètes | Revérifiez identité de VM, état en cours et connexion de l’hôte. Comparez preuves paquet/service invité aux observations Général/Avancé et horodatages. Ne redémarrez pas l’hyperviseur, ne masquez pas l’alerte et ne remplacez pas les pilotes à l’aveugle. |
| Arrêt en échec ou proposition de forcer | Annulez force/contournement, gardez l’erreur exacte et vérifiez la console. Utilisez l’arrêt normal de l’invité si possible. Une coupure forcée peut perdre des données et exige une décision distincte. |
| Invité en panne après modification | Conservez transaction de paquet et journaux démarrage/service. Utilisez console et plan de récupération établi séparément ; ce guide ne garantit pas un retour arrière automatique par désinstallation/rétrogradation. |

N’activez/redémarrez/réinstallez pas en boucle pour masquer une panne inexpliquée. [Signalez les éléments expurgés](/docs/xoa-hl/troubleshooting/#signaler-un-problème) : versions, ID VM/hôte, horodatages, origine/version du paquet, état du service, messages exacts et résultats des tâches d’alimentation. Journaux et écrans invités peuvent contenir noms, adresses ou données privés ; gardez les preuves brutes privées.

Pour les mises à jour ultérieures, planifiez séparément une maintenance OS/paquet invité et répétez ces observations. Autres distributions Linux, installation par ISO, outils Windows/BSD, changement de fournisseur, mises à jour/suppression et matrice d’invités pris en charge restent des validations distinctes. Continuez avec les [opérations VM](/docs/xoa-hl/vm-operations/) et la [sauvegarde/restauration](/docs/xoa-hl/backup-restore/).

## Sources

XO à `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` : [ordre de détection Général](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [champs OS invité Avancé](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [conversion des métriques hôte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [confirmations arrêt/force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js) et [permission VM operate](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs). Périmètre HomeLab : [correctifs à `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).

Sources invitées vérifiées le 2026-10-15 : Ubuntu Noble [paquet `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities), [fichiers amd64](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist) et [sources Debian versionnées](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`). Le [contexte amont XCP-ng](https://docs.xcp-ng.org/vms/#linux-guest-tools) ne valide pas la compatibilité HomeLab installée.

[Catalogues des libellés EN/FR/JA au pin XO](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl) / [Repli de langue HomeLab](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/compact-xo-locales.py).
