---
title: Gérer les bibliothèques ISO, les disques et le réseau
description: Connecter une bibliothèque ISO NFS, ajouter un disque de test et gérer des interfaces VM isolées.
weight: 22
translationKey: xoa-manual-storage-networks
translationStatus: draft
sourceRevision: sha256:529fe9b2d47eac1c033278e21e8813c5964885191cb2148fe63252f95db25927
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Utilisez une VM jetable arrêtée, avec un compte administrateur dans l’**appliance XOA-HL**. Notez son identité, ses disques et interfaces existants. Choisissez un SR inscriptible avec assez d’espace libre et un réseau existant dont l’isolation a été vérifiée en dehors de XO. N’utilisez pas l’appliance comme invité de test.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests de disque, d’interface et de détection dans l’invité sur l’appliance publiée restent à faire.
{{< /callout >}}

## 1. Identifier les objets

| Objet | Signification |
| --- | --- |
| SR | Dépôt de stockage contenant les disques virtuels ; vérifiez son espace libre |
| VDI | Données d’un disque virtuel stockées dans un SR |
| VBD | Attachement entre une VM et un disque virtuel |
| VIF | Interface réseau virtuelle d’une VM |
| PIF | Interface réseau de l’hôte ; modifier la connectivité de gestion peut déconnecter l’hôte |

L’interface d’une VM n’est pas celle de gestion de l’hôte. Choisir un réseau ou générer une MAC ne crée pas d’isolation ; vérifiez le VLAN, la liaison physique et le routage avant d’y connecter un invité cloné ou restauré.

## 2. Ajouter un petit disque vide

1. Confirmez l’arrêt de la VM de test. Ouvrez **Disks** (`/#/vms/<id>/disks`) et choisissez **New disk**.
2. Choisissez le SR inscriptible prévu dans le même pool, un nom de test explicite et une petite taille avec ses unités. Vérifiez l’option lecture seule ; laissez-la désactivée pour un disque de test inscriptible. Lancez la création une seule fois et attendez sa fin.
3. Vérifiez le nom, la taille, le SR et l’attachement à la bonne VM dans la nouvelle ligne. Notez l’identité du disque et l’espace restant avant de démarrer l’invité.

Dans la console de l’invité, identifiez le nouveau disque par sa taille et ses informations. XO crée le disque virtuel et son attachement ; il ne le partitionne, ne le formate et ne le monte pas automatiquement dans l’invité. Les procédures de système de fichiers dépassent ce pilote. Ne formatez pas un périphérique sur la seule base d’un nom supposé.

En cas d’échec, examinez la tâche et les inventaires VM/SR avant de réessayer : une opération partielle peut laisser un disque. Conservez l’erreur, vérifiez l’espace et la connectivité et [utilisez le dépannage](/docs/xoa-hl/troubleshooting/) si nécessaire. Cet exercice ne valide pas la réduction, l’extension ou la migration du stockage.

## 3. Distinguer détachement et suppression

Supprimer le VBD détache le disque de la VM, sans signifier que les données du VDI sont supprimées. Supprimer le VDI détruit les données ; c’est une autre action, indisponible tant que le disque est attaché dans cette interface. Déconnecter un attachement est aussi distinct de le supprimer.

Pour le nettoyage, arrêtez l’invité et identifiez précisément le seul disque de test vide. Conservez le VDI si son contenu peut être utile. Ne supprimez jamais un disque de démarrage, partagé ou non identifié pour résoudre un avertissement d’espace. [Sauvegardez les données importantes](/docs/xoa-hl/backup-restore/) séparément.

## 4. Ajouter une interface VM isolée

Sur la VM de test arrêtée, ouvrez **Network** (`/#/vms/<id>/network`) et choisissez **New device**. Sélectionnez le réseau isolé vérifié dans le même pool. Laissez la MAC vide pour sa génération automatique, puis choisissez **Create**. Vérifiez l’interface, son réseau et sa MAC avant le démarrage, puis la détection et la connectivité prévues dans l’invité.

Pour un clone ou une restauration isolés, supprimez **toutes** les VIF héritées pendant l’arrêt et confirmez que la liste est vide avant le premier démarrage. Utilisez la suppression de l’interface, pas seulement son commutateur de connexion : la simple déconnexion n’est pas la procédure d’isolation. N’ajoutez un réseau de test qu’après avoir confirmé qu’il n’atteint pas la production et résolu les identités copiées.

Si la connectivité est inattendue, arrêtez la VM de test et inspectez le réseau choisi et l’isolation externe avant de réessayer. Ce guide ne configure pas les PIF, adresses de gestion, agrégations ou VLAN de l’hôte. Ne modifiez pas le réseau de gestion de l’hôte pendant cet exercice. Poursuivez avec [les opérations VM](/docs/xoa-hl/vm-operations/) ou [la gestion des hôtes et pools](/docs/xoa-hl/hosts-pools/).

## 5. Connecter une bibliothèque ISO NFS {#nfs-iso-library}

Un SR ISO contient les médias d’installation ; il est distinct du SR inscriptible pour les disques de VM et d’une destination de sauvegarde. Cet exercice connecte un export NFS existant et dédié, contenant un ISO d’installation vérifié avec la somme publiée par l’éditeur. La préparation du NAS/export et le dépôt du fichier relèvent de son administrateur de stockage, hors de cette procédure dans le navigateur. Cette procédure dans le navigateur ne nécessite aucune commande dans le shell de l’hôte ni modification du réseau de gestion.

Avant toute création, cherchez un SR ISO adapté dans le pool prévu. Utilisez-le si son identité, l’accès des hôtes et les médias sont corrects. Pour une nouvelle bibliothèque de test, notez le serveur NFS, le chemin exporté exact, la version NFS convenue, le pool/les hôtes prévus et le nom/la somme de l’ISO. Chaque hôte qui lira l’ISO doit être autorisé à accéder à l’export. L’accès depuis le navigateur ou l’appliance XOA-HL seule ne prouve pas celui des hôtes.

1. En tant qu’administrateur, ouvrez **Nouveau → Stockage** (`/#/new/sr`). Choisissez un hôte du pool prévu. Donnez un nom distinct, comme `lab-nfs-iso`, et une description identifiant l’export de test.
2. Dans **ISO SR**, sélectionnez **NFS ISO**. Ne sélectionnez pas **NFS** dans le groupe **VDI SR**, destiné aux disques de VM. **Local** désigne un chemin sur un hôte hyperviseur, pas un dossier de votre ordinateur ou de l’appliance ; le stockage local, SMB et sur périphérique bloc reste hors de cet exercice.
3. Saisissez le serveur NFS dans **Serveur**. Choisissez la version convenue avec l’administrateur de stockage (le formulaire propose la valeur par défaut, `4` et `4.1`), puis utilisez l’icône de recherche à côté du serveur. Un changement de version ne relance pas la détection : recherchez de nouveau après ce changement. Laissez **Comma delimited NFS options** vide pour le premier test, sauf options précises convenues. Les libellés de version/options NFS restent en anglais dans ce catalogue.
4. Sélectionnez l’export exact dans **Chemin**. Utilisez sa racine pour ce pilote ; les sous-répertoires ne sont pas couverts. Attendez la vérification du chemin. Si le serveur/export manque, si la sonde échoue ou si **Utilisation du stockage** affiche des SR existants, arrêtez et examinez l’erreur et leurs identités. L’assistant utilise des sondes NFS même pour NFS ISO ; un SR détecté n’est pas une preuve de bibliothèque ISO. Ne le rattachez pas et n’acceptez pas un avertissement de création sur un stockage existant.
5. Dans **Récapitulatif**, vérifiez le nom et le type choisi (`nfsiso`). Revérifiez l’hôte et le serveur/chemin dans les sections précédentes, puis sélectionnez **Créer** une seule fois. En cas d’échec, examinez l’inventaire des SR du pool avant de réessayer ; la requête peut laisser un SR ou un attachement partiellement créé.

Le type backend du SR créé est `iso` ; `nfsiso` est le choix de l’assistant. Notez son UUID, puis ouvrez **Hôtes** (`/#/srs/<id>/hosts`) et vérifiez que chaque attachement prévu est connecté et que son emplacement affiché correspond à l’export. Un SR déclaré partagé ne prouve pas que tous les hôtes y accèdent. Gardez l’hôte choisi pour la VM dans le périmètre d’accès observé.

Utilisez l’action de rafraîchissement **Rescanner tous les disques**, attendez la fin de la requête, puis ouvrez **Disques** (`/#/srs/<id>/disks`). Vérifiez le nom et la taille de l’ISO attendu. Après l’ajout ou le remplacement d’un fichier par l’administrateur de stockage, relancez le scan. Vérifiez la somme publiée par l’éditeur à la source du fichier ; un scan réussi ou un nom identique ne prouve pas son intégrité.

Dans [l’assistant de création de VM](/docs/xoa-hl/create-vm/), choisissez le même pool et vérifiez que **ISO/DVD** propose le média attendu. S’il est déjà dans la bibliothèque, sautez l’envoi depuis le navigateur. Lire un média existant et en envoyer un nouveau sont des capacités distinctes : le sélecteur d’import ne prouve pas que ce SR/export autorise la création et l’écriture d’ISO. N’élargissez pas globalement les permissions pour faire fonctionner un envoi.

| Symptôme | Vérification et suite |
| --- | --- |
| Aucun export trouvé ou sonde du chemin en échec | Notez l’erreur ; vérifiez le serveur/chemin, la version, la détection des exports et l’accès des hôtes avec l’administrateur de stockage. Arrêtez si l’assistant ne peut pas détecter cet export. |
| SR créé mais hôte déconnecté | Vérifiez l’attachement/l’emplacement et l’accès de cet hôte. Un autre hôte connecté ne suffit pas ; ne déconnectez pas tous les hôtes pour tenter une réparation. |
| Scan réussi mais ISO absent | Vérifiez le fichier complet sur l’export convenu, son nom/sa taille et le SR sélectionné. Rescannez après correction de la source ; ne recréez pas le SR à répétition. |
| ISO absent de ISO/DVD | Vérifiez le pool de l’assistant, le type du SR ISO, la présence du média et l’attachement de l’hôte prévu. Un SR NFS pour disques de VM n’est pas un SR ISO. |
| Échec de création ou SR inattendu | Conservez l’erreur et l’inventaire UUID/attachements. Identifiez les objets partiels avant toute nouvelle tentative ou suppression ; n’utilisez pas l’oubli, le retrait ou le formatage pour effacer une erreur non identifiée. |

Ne retirez pas un ISO et ne déconnectez/oubliez pas son SR pendant qu’une VM l’utilise. Notez les consommateurs et éjectez le média de l’invité de test avant de prévoir le nettoyage. Ce pilote ne valide ni une procédure de destruction de SR ni l’envoi d’ISO en écriture.

## Sources

Version XO 5 `e281c536` : [interface des disques et sélection du SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [interface réseau VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js) et [actions disque/interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).

[assistant SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js) / [API SR et sondes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs) / [action de rescan SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js) / [attachements des hôtes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js) / [API d’import ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs) / [sélection ISO de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
