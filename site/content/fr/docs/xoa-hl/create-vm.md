---
title: Créer et installer sa première machine virtuelle
description: Importer un ISO d’installation, choisir le stockage et le réseau, puis démarrer une VM dans XOA-HL.
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: draft
sourceRevision: sha256:672451aeaca5fa92a966d3f969974ec5d8da3cae7c0e43f7276bc17d3f6a1b0b
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Créez une VM de test, installez son système d’exploitation et vérifiez qu’elle démarre depuis son propre disque virtuel.

{{< callout type="info" >}}
Procédure en prévisualisation : vérifiée dans les sources de XO 5.113.2 (`e281c536`) avec les patchs XOA-HL de l’image `xoa-image-20261009-5f33c81`. L’essai en laboratoire et les tests propres au système invité restent à faire. Les tailles ci-dessous sont des exemples, pas une matrice des systèmes pris en charge. Cette traduction attend une relecture.
{{< /callout >}}

## Avant de commencer

- [Connectez-vous et ajoutez votre hôte](/docs/xoa-hl/first-login/). Ce guide utilise un compte administrateur XOA-HL.
- Téléchargez un ISO d’installation auprès de l’éditeur du système d’exploitation et vérifiez-le avec la somme de contrôle publiée par l’éditeur.
- Identifiez un **SR ISO** pour les médias d’installation et un **SR accessible en écriture** avec assez d’espace pour les disques de VM. Leurs rôles sont différents. Vérifiez la [disponibilité de la bibliothèque ISO XCP-HL](/docs/features/#iso-storage) ; elle n’existe pas sur tous les hôtes.
- Choisissez un réseau invité donnant les accès nécessaires à l’installateur. Gardez assez de RAM et de stockage libres sur l’hôte pour XOA-HL et les VM existantes.

Les opérations de gestion se font dans le **navigateur**. L’installation du système se déroule dans la **console de la nouvelle VM invitée**, jamais sur l’hôte XCP-HL ni dans l’appliance XOA-HL.

## 1. Importer l’ISO d’installation

1. Dans XOA-HL, ouvrez **Importer → Disk** (`/#/import/disk`). Laissez **From URL** désactivé pour envoyer le fichier téléchargé.
2. Sélectionnez le **SR ISO**, par exemple `XCP-HL ISO library` s’il existe. Déposez le fichier `.iso` dans la zone d’envoi.
3. Vérifiez le nom et la destination, sélectionnez **Importer**, puis attendez la fin de l’opération.
4. Vérifiez que l’ISO apparaît dans la liste des disques du SR de destination. Ne continuez pas avec un envoi incomplet.

Si aucun SR ISO adapté n’apparaît, préparez un dépôt ISO avant de continuer. Importer le média dans un stockage ordinaire de disques de VM ne le transforme pas en bibliothèque ISO.

## 2. Remplir l’assistant de création

Ouvrez **Nouveau → VM** (`/#/vms/new`) et sélectionnez le **pool** prévu. Choisissez un modèle d’installation adapté au système invité, plutôt qu’un modèle contenant déjà un système installé.

Utilisez un nom distinct, comme `lab-first-vm`. Cet exemple convient à une petite installation Linux de test uniquement si les exigences de l’éditeur correspondent à ces ressources :

| Section de l’assistant | Choix et objectif |
| --- | --- |
| Infos | Choisissez le modèle d’installation, le nom et la description. |
| Performances | Exemple : 2 vCPU et 2 Gio de RAM ; augmentez-les si l’installateur l’exige. |
| Paramètres d’installation | Choisissez **ISO/DVD** et l’ISO importé. |
| Interfaces | Sélectionnez le réseau invité. Laissez l’adresse MAC vide pour la génération automatique, sauf exigence de votre réseau. |
| Disques | Exemple : un disque de 20 Gio sur un SR accessible en écriture depuis l’hôte prévu. N’utilisez pas le SR ISO pour le disque système. |
| Avancé | Gardez les valeurs du modèle, sauf changement documenté requis par l’invité. Pour contrôler le premier démarrage, décochez **Démarrer la VM après sa création**. |
| Récapitulatif | Vérifiez le pool, le modèle, le CPU, la RAM, le réseau et le stockage avant de créer une seule VM. |

Sélectionnez **Créer**. **Vérification :** une seule VM portant le nom choisi apparaît avec la configuration attendue. Si le bouton est désactivé, une section obligatoire ou une vérification des ressources est incomplète ; examinez l’assistant avant de réessayer.

## 3. Installer le système d’exploitation

1. Ouvrez la nouvelle VM, vérifiez son nom et démarrez-la. Ouvrez l’onglet **Console**.
2. Confirmez le démarrage de l’installateur choisi. Suivez les instructions de l’éditeur dans cet invité.
3. Quand l’installateur demande le disque cible, vérifiez qu’il s’agit du **disque virtuel de la nouvelle VM**. L’exemple crée un disque de 20 Gio ; toute donnée existante inattendue impose de s’arrêter et de vérifier la VM sélectionnée.
4. Après l’installation, éjectez l’ISO du lecteur CD virtuel dans l’onglet **Disques**. Redémarrez normalement l’invité et vérifiez qu’il démarre depuis son disque virtuel.

{{< callout type="warning" >}}
Agissez uniquement sur la nouvelle VM de test. Formater un disque ou forcer l’arrêt peut perdre des données. Si l’invité répond, utilisez son arrêt ou redémarrage normal ; n’arrêtez pas l’appliance XOA-HL ni l’hyperviseur pour redémarrer cet invité.
{{< /callout >}}

## 4. Vérifier le résultat

- L’invité démarre sans l’ISO et vous pouvez ouvrir une session dans sa console.
- Le CPU, la mémoire, les disques et le réseau correspondent à vos choix.
- Dans l’invité, vérifiez l’adresse IP, la passerelle, le DNS et les accès nécessaires. La console reste utile même si le réseau invité ne fonctionne pas.
- Notez la version du système invité, le modèle, le nom de la VM et les versions XOA-HL installées. Les outils invités et leur installation dépendent du système ; ce tutoriel ne fournit pas de recette testée pour les installer.

Cette VM n’est pas encore protégée par une sauvegarde indépendante. Un snapshot sur le même stockage ne protège pas de la perte de ce stockage. N’y placez pas de données importantes avant d’avoir vérifié une sauvegarde et une restauration.

## En cas de problème

| Symptôme | Vérification et suite |
| --- | --- |
| L’ISO manque dans l’assistant | Confirmez la fin de l’envoi dans un SR ISO et l’accès à ce SR depuis le pool ou l’hôte choisi. |
| Le bouton Créer est désactivé | Vérifiez le pool, le modèle, le nom, les ressources, l’ISO, le réseau et le stockage des disques ; complétez chaque section obligatoire. |
| La création ou le démarrage échoue | Lisez l’erreur de tâche. Vérifiez la RAM libre, l’espace libre du SR et l’accès de l’hôte au stockage et au réseau choisis. Avant de réessayer, vérifiez si une VM a déjà été créée. |
| L’installateur revient à chaque redémarrage | Éjectez l’ISO du lecteur CD de cette VM et vérifiez que le système a été installé sur son disque virtuel. |
| L’invité n’a pas de réseau | Vérifiez le réseau virtuel choisi ainsi que l’IP, la passerelle et le DNS de l’invité. Évitez de modifier le réseau de gestion de l’hôte pour diagnostiquer un invité. |

## Étape suivante et sources

Gardez cette VM pour le prochain tutoriel de sauvegarde indépendante et de restauration isolée. Ces chapitres sont suivis dans [l’issue du parcours débutant](https://github.com/Vagrantin/xcp-hl/issues/197). Consultez le [glossaire](/docs/xoa-hl/glossary/) et le [guide de mise à jour](/docs/guides/updates/) pendant leur validation.

Sources examinées à XO@e281c536 : [import ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [assistant VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [onglets VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) et [éjection du CD](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js) ; [application des patchs à xoa-hl@5f33c81](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
