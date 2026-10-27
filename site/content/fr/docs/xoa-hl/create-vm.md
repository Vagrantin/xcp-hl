---
title: "Créer votre première machine virtuelle"
linkTitle: "Première VM"
description: "Importez un ISO d’installation, créez une VM et installez son système d’exploitation."
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: draft
sourceRevision: sha256:e7be5e5f5f86d71b70010611cb45b1d6195e8a8b985e70b26f0563a58349aa00
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Créez une petite VM de test, installez son système d’exploitation et vérifiez qu’elle démarre depuis son propre disque virtuel.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261027-ca44911`, paquet `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Testé sur une appliance de laboratoire le 2026-10-27 avec un invité Linux ; les autres systèmes invités demandent leurs propres tests. Les tailles ci-dessous sont des exemples, pas une liste de systèmes pris en charge.
{{< /callout >}}

## Avant de commencer

- [Connectez-vous et ajoutez votre hôte](/docs/xoa-hl/first-login/). Ce guide utilise un compte administrateur XOA-HL.
- Téléchargez un ISO d’installation auprès de l’éditeur du système. Vérifiez-le avec la somme de contrôle publiée par l’éditeur.
- Repérez deux types de stockage : un **SR ISO** pour les médias d’installation, et un **SR accessible en écriture** avec de l’espace libre pour les disques de VM. Tous les hôtes n’ont pas la [bibliothèque ISO XCP-HL](/docs/features/#iso-storage).
- Besoin d’un nouveau SR pour les disques de VM ? Commencez par [créer un stockage NFS sur un export vide et dédié](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Revenez à ses vérifications de disque une fois cette VM installée.
- Choisissez un réseau invité qui donne à l’installateur les accès nécessaires. Gardez assez de mémoire et de stockage sur l’hôte pour XOA-HL et vos autres VM.

Vous gérez la VM dans votre **navigateur**. Le système s’installe dans la **console de la nouvelle VM**, jamais sur l’hôte XCP-HL ni dans l’appliance XOA-HL.

## 1. Préparer l’ISO d’installation

Si un média vérifié se trouve déjà dans une bibliothèque ISO, utilisez-le et passez cette étape. Pour connecter une bibliothèque NFS dédiée, suivez [Connecter une bibliothèque ISO NFS](/docs/xoa-hl/storage-networks/#nfs-iso-library).

L’envoi depuis le navigateur ne fonctionne que si le SR ISO accepte de nouveaux fichiers et dispose d’assez d’espace. Voir le SR dans la liste d’import ne le prouve pas : certaines bibliothèques lisent les médias sans accepter d’envoi.

1. Ouvrez **Importer → Disk** (`/#/import/disk`). Laissez **From URL** désactivé pour envoyer le fichier téléchargé.
2. Sélectionnez le **SR ISO**, par exemple `XCP-HL ISO library` s’il existe. Déposez le fichier `.iso` dans la zone d’envoi.
3. Vérifiez le nom du fichier et la destination. Sélectionnez **Importer** et attendez la fin de l’opération.
4. Ouvrez la liste des disques du SR de destination et vérifiez que l’ISO s’y trouve. Ne continuez pas avec un envoi incomplet.

Si aucun SR ISO adapté n’apparaît, préparez-en un d’abord. Importer un ISO dans un stockage ordinaire de disques de VM n’en fait pas une bibliothèque ISO.

## 2. Créer la VM

Ouvrez **Nouveau → VM** (`/#/vms/new`) et sélectionnez votre **pool**. Choisissez un modèle qui installe votre système, et non un modèle qui contient déjà un système installé.

Donnez à la VM un nom clair, par exemple `lab-first-vm`. Les tailles ci-dessous conviennent à un petit système Linux de test, si elles respectent les exigences de l’éditeur :

| Section de l’assistant | Quoi choisir |
| --- | --- |
| Infos | Le modèle d’installation, un nom et une description. |
| Performances | Par exemple 2 vCPU et 2 Gio de RAM. Augmentez si l’installateur en demande plus. |
| Paramètres d’installation | **ISO/DVD**, puis l’ISO d’installation. |
| Interfaces | Le réseau invité. Laissez l’adresse MAC vide pour qu’elle soit générée, sauf si votre réseau impose une adresse fixe. |
| Disques | Par exemple un disque de 20 Gio sur un SR accessible en écriture et joignable par l’hôte. Ne placez jamais le disque système sur le SR ISO. |
| Avancé | Gardez les valeurs du modèle, sauf changement documenté requis par l’invité. Décochez **Démarrer la VM après sa création** pour la démarrer vous-même. |
| Récapitulatif | Vérifiez le pool, le modèle, le CPU, la mémoire, le réseau et le stockage. |

Sélectionnez **Créer**.

**Vérification :** une seule VM portant votre nom apparaît, et ses réglages correspondent à vos choix. Si **Créer** est grisé, une section obligatoire ou une vérification des ressources est incomplète. Relisez l’assistant avant de réessayer.

Pour les commandes de la console, ou un écran noir ou figé, consultez [Utiliser la console d’une VM](/docs/xoa-hl/vm-operations/#vm-console).

## 3. Installer le système d’exploitation

1. Ouvrez la nouvelle VM et vérifiez son nom. Démarrez-la, puis ouvrez l’onglet **Console**.
2. Vérifiez que l’installateur démarre. Suivez les étapes d’installation de l’éditeur dans cet invité.
3. Quand l’installateur demande le disque cible, vérifiez qu’il s’agit du **disque virtuel de la nouvelle VM** (20 Gio dans cet exemple). Si le disque contient déjà des données, arrêtez-vous et vérifiez que vous avez choisi la bonne VM.
4. Une fois l’installation terminée, ouvrez l’onglet **Disques** de la VM et éjectez l’ISO du lecteur CD virtuel. Redémarrez normalement l’invité et vérifiez qu’il démarre depuis son disque virtuel.

{{< callout type="warning" >}}
N’agissez que sur la nouvelle VM de test. Formater un disque ou forcer un arrêt peut faire perdre des données. Si l’invité répond, utilisez son arrêt ou son redémarrage normal. N’arrêtez jamais l’appliance XOA-HL ni l’hôte pour redémarrer un seul invité.
{{< /callout >}}

## 4. Vérifier le résultat

- L’invité démarre sans l’ISO d’installation, et vous pouvez ouvrir une session dans sa console.
- Le CPU, la mémoire, les disques et le réseau de la VM correspondent à vos choix.
- Dans l’invité, l’adresse IP, la passerelle, le DNS et les accès nécessaires fonctionnent. La console reste utilisable même si le réseau de l’invité ne fonctionne pas.
- Vous avez noté la version du système invité, le modèle, le nom de la VM et les versions de XOA-HL.

Les outils invités dépendent du système. Pour Ubuntu 24.04, consultez les étapes suivantes ci-dessous.

Cette VM n’a pas encore de sauvegarde indépendante. Un snapshot sur le même stockage ne vous protège pas si ce stockage est perdu. N’y mettez pas de données importantes avant d’avoir testé une sauvegarde et une restauration.

## En cas de problème

| Problème | À vérifier |
| --- | --- |
| L’ISO n’apparaît pas dans l’assistant | Vérifiez que l’envoi s’est terminé dans un SR ISO, et que le pool ou l’hôte choisi peut joindre ce SR. |
| **Créer** est grisé | Vérifiez le pool, le modèle, le nom, les ressources, l’ISO, le réseau et le stockage des disques. Remplissez chaque section obligatoire. |
| La création ou le démarrage échoue | Lisez l’erreur de la tâche. Vérifiez la mémoire libre de l’hôte, l’espace libre du SR, et que l’hôte peut joindre le stockage et le réseau choisis. Avant de réessayer, vérifiez si une VM a déjà été créée. |
| L’installateur revient à chaque redémarrage | Éjectez l’ISO du lecteur CD de cette VM. Vérifiez que le système est bien installé sur son disque virtuel. |
| L’invité n’a pas de réseau | Vérifiez le réseau choisi ainsi que l’adresse IP, la passerelle et le DNS de l’invité. Ne modifiez pas le réseau de gestion de l’hôte pour corriger un invité. |

## Étapes suivantes

1. [Sauvegardez la VM de test et vérifiez une restauration](/docs/xoa-hl/backup-restore/).
2. Pour un invité Ubuntu 24.04 (amd64), [installez l’agent de gestion](/docs/xoa-hl/guest-tools/#install-linux-agent). Les autres systèmes ont besoin de leur propre procédure.
3. Pour réutiliser un invité installé, [créez de nouvelles VM à partir d’un modèle](/docs/xoa-hl/templates/#deploy-template).

Consultez aussi le [glossaire](/docs/xoa-hl/glossary/) et le [guide de mise à jour](/docs/guides/updates/).

{{< details title="Sources" closed="true" >}}
Vérifié avec XO@e281c536 : [import ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [assistant de création de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [onglets de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) et [éjection du CD](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js) ; [patchs appliqués dans xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
