---
title: "Migration, export et import d’une VM"
linkTitle: "Migration et export"
description: "Déplacez une VM vers un autre hôte de son pool, exportez-la en fichier XVA et importez une copie."
weight: 43
translationKey: xoa-manual-vm-transfer
translationStatus: reviewed
sourceRevision: sha256:1e0c1a71359bc2780a31862ccef13422bbb20137e03c5b77f967d92131a100d9
glossaryTerms: ["vm", "host", "pool", "sr", "snapshot", "backup"]
---

Utilisez une VM jetable sans données de production. Connectez-vous à l’**appliance XOA-HL** comme administrateur et vérifiez que les hôtes, le stockage et la VM sont disponibles. La migration et l’export déplacent ou copient une VM entière ; ni l’un ni l’autre ne remplace une [sauvegarde indépendante et un test de restauration](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; la migration, l’export et l’import ne sont pas encore testés en laboratoire. Les versions ultérieures peuvent différer.
{{< /callout >}}

## 1. Choisir l’opération

| Objectif | Opération | Résultat |
| --- | --- | --- |
| Exécuter la même VM sur un autre hôte de son pool | **Migrer** | Même objet VM ; les disques restent sur un stockage partagé ou sont copiés vers un SR choisi |
| Conserver un fichier portable d’une VM arrêtée | **Exporter** en XVA | Un fichier enregistré par votre navigateur ; ni planification, ni rétention, ni contrôle de restauration |
| Créer une VM distincte à partir d’un fichier XVA | **Importer** | Un nouvel objet VM avec des identités invitées copiées ; à isoler comme un clone |
| Récupérer après une perte | [Sauvegarde et restauration](/docs/xoa-hl/backup-restore/) | Une copie indépendante validée par une restauration isolée |

Ce guide couvre la migration entre hôtes du **même pool**, l’export XVA sans compression et l’import d’un fichier XVA. La migration entre pools, le remappage des réseaux, les fichiers OVA, l’import depuis une URL, l’import/export de disques seuls et l’import depuis VMware sont hors de son périmètre. Le menu HomeLab masque l’entrée d’import VMware.

Les modes supplémentaires sont décrits dans [Autres modes de transfert](#transfer-modes) ; leur validation installée reste distincte.

## 2. Migrer une VM au sein de son pool

Prérequis à vérifier avant de commencer :

- Le pool compte au moins deux hôtes connectés, et vous disposez du droit d’administration sur la VM et sur l’hôte cible.
- L’hôte cible atteint les réseaux et le stockage de la VM. Les disques situés sur un SR partagé ne sont pas copiés. Un disque situé sur un stockage que la cible n’atteint pas, comme un SR local, est copié.
- Une fenêtre de maintenance. Un invité en fonctionnement est brièvement suspendu pendant une migration à chaud ; une copie de disque dure plus longtemps et demande de l’espace libre sur le SR cible.
- Un relevé de l’ID de la VM, de son hôte actuel, de chaque disque et de son SR, ainsi qu’un contrôle de l’invité, par exemple une connexion à la console ou un test applicatif.

1. Ouvrez la VM et choisissez **Migrer**. L’action est proposée pour les VM en fonctionnement ou arrêtées, pas pour les VM suspendues ou en pause. Les utilisateurs en libre-service ne la voient pas.
2. Dans **Migrer la VM**, utilisez **Sélectionner un hôte de destination :** pour choisir un autre hôte du même pool. La liste exclut l’hôte actuel. Elle peut aussi afficher des hôtes d’autres pools connectés ; ne les choisissez pas pour cet exercice.
3. Lisez la partie stockage. Si tous les disques sont sur un SR partagé, aucun SR n’est requis. Sinon, XO exige un SR principal (**Sélectionner le SR principal…**) et permet de choisir un SR pour chaque VDI. Choisissez des SR accessibles en écriture avec assez d’espace libre ; ces disques sont copiés.
4. **Choisir un réseau de migration :** est facultatif au sein d’un pool. XO présélectionne le réseau de migration configuré pour le pool lorsque l’hôte cible a une adresse sur ce réseau. Tout réseau sélectionné fait passer XO par la migration avec stockage au lieu d’une simple migration dans le pool. Conservez la valeur proposée, sauf si la conception de votre pool désigne un autre réseau.
5. Confirmez et attendez la fin de la tâche. Ne cliquez pas de nouveau pendant que la migration est en cours.
6. Actualisez l’onglet **Général** de la VM. Vérifiez l’hôte, l’état d’alimentation, la console, le réseau de l’invité et l’application. Après une copie de disque, vérifiez où se trouve chaque disque et l’espace libre des deux SR.

{{< callout type="warning" >}}
Si XAPI signale que la VM est incompatible avec l’hôte cible, XO propose **Force migration** (libellé non traduit dans cette version). Annulez-la pour cet exercice et examinez la compatibilité du processeur et de l’hôte. Une migration forcée peut rendre l’invité inutilisable.
{{< /callout >}}

Si une simple migration dans le pool signale qu’un SR est requis, XO la relance automatiquement comme migration avec stockage. Il utilise alors les SR connectés à l’hôte cible ou le SR par défaut du pool. Une migration que vous pensiez rapide peut donc devenir une copie de disque. En cas d’échec, conservez l’erreur de la tâche et vérifiez l’hôte, l’état d’alimentation et les disques de la VM sur chaque SR concerné avant de réessayer. Ne réessayez pas en forçant.

## 3. Exporter une VM arrêtée en fichier XVA

Il vous faut le droit d’administration sur la VM et assez d’espace libre sur l’ordinateur qui exécute le navigateur.

1. Arrêtez proprement l’invité et vérifiez l’état **Halted**. Relevez l’ID de la VM, son nom, ses disques et leur taille totale.
2. Choisissez **Exporter**. Laissez **Type** sur `xva`. Laissez **Compression** sur **Disabled**, la valeur par défaut. Les autres choix sont GZIP (very slow) et, sur les hôtes XCP-ng, Zstd. L’import d’un XVA compressé n’est pas couvert par ce guide.
3. Confirmez. **Download VM** affiche un lien de téléchargement, **OK** et **Annuler**. Le lien et **OK** ouvrent la même URL, que le message décrit comme valable une seule fois, pendant une courte durée. N’utilisez que l’un des deux : sélectionnez le lien, puis fermez la boîte de dialogue avec **Annuler**. L’URL contient un jeton d’accès à usage unique : traitez-la comme un secret jusqu’à son utilisation.
4. Le navigateur enregistre un fichier nommé `<date> - <nom de la VM>.xva`. Laissez le téléchargement aller jusqu’au bout ; l’annuler arrête l’export. Vérifiez que la taille du fichier est plausible au regard des tailles de disque relevées.
5. Sur l’ordinateur qui exécute le navigateur, relevez une somme de contrôle du fichier, par exemple `sha256sum "<fichier>.xva"`. Utilisez-la pour vérifier le fichier avant un import.

Par défaut, au plus deux exports XVA s’exécutent en même temps pour un pool. Un téléchargement supplémentaire échoue au lieu d’attendre. Laissez les exports en cours se terminer, puis demandez un nouveau lien.

Un XVA contient les disques et la configuration de la VM. Conservez-le comme les données qu’il contient et supprimez-le à la fin du test. Un fichier d’export n’a ni planification, ni rétention, ni validation de restauration : ce n’est pas une tâche de sauvegarde.

{{< callout type="warning" >}}
Il est possible d’exporter une VM en fonctionnement, mais XO exporte alors un snapshot temporaire nommé `[XO Export] <nom de la VM>`. Cette copie n’est pas cohérente au niveau applicatif. XO supprime le snapshot à la fin du téléchargement. Si la suppression échoue, il se contente de journaliser un avertissement et le snapshot peut rester sur le SR. Après l’export d’une VM en fonctionnement, vérifiez l’onglet **Instantanés** de la VM. Ce guide utilise plutôt une VM arrêtée.
{{< /callout >}}

## 4. Importer le XVA comme copie isolée

1. Ouvrez **Importer** > **VM** (`/#/import/vm`). L’entrée de menu n’apparaît que si vous pouvez opérer au moins un pool.
2. Choisissez le pool cible dans **Sur le Pool:**. **Sur le SR:** propose le SR par défaut du pool. Choisissez un SR accessible en écriture avec assez d’espace libre.
3. Déposez le fichier `.xva` dans la zone **Déposez ici vos fichiers OVA ou XVA pour importer des machines virtuelles.** Vérifiez le nom et la taille du fichier dans la liste. Les fichiers sans extension `.xva` ou `.ova` sont ignorés. Laissez **From URL** désactivé.
4. Sélectionnez **Importer** et gardez l’onglet du navigateur ouvert jusqu’à la fin de l’envoi. Pour un seul fichier, XO ouvre la page de la nouvelle VM après réussite.
5. Gardez la VM importée arrêtée. Relevez son ID : c’est un objet différent de la VM source, même si le nom est identique. Renommez-la pour éviter toute confusion.
6. Avant le premier démarrage, ouvrez **Réseaux** et [supprimez toutes les interfaces virtuelles](/docs/xoa-hl/storage-networks/) ou mettez en place une isolation externe vérifiée. La copie reprend le même système invité, les mêmes paramètres IP, nom d’hôte, identifiants et identités applicatives que la source.
7. Démarrez la copie, puis vérifiez sa console et les données de test relevées.

XO refuse de démarrer une VM dont l’adresse MAC d’une interface duplique celle d’une autre de ses interfaces ou d’une VM en fonctionnement. Le code d’erreur est `DUPLICATED_MAC_ADDRESS`. Ne forcez pas le démarrage ; supprimez ou isolez d’abord l’interface.

Si l’import échoue (**Import de VM échoué**), des objets peuvent subsister. Avant de réessayer, vérifiez les disques du SR cible et la liste des VM pour repérer les objets créés pendant la tentative. Ne supprimez que les restes formellement identifiés, avec la [procédure de suppression d’une VM jetable](/docs/xoa-hl/vm-operations/#delete-vm).

## 5. Nettoyer

1. Supprimez la VM de test importée avec la [procédure de suppression d’une VM jetable](/docs/xoa-hl/vm-operations/#delete-vm).
2. Supprimez le fichier XVA de l’ordinateur et de tout emplacement temporaire.
3. Vérifiez que la VM source est toujours présente, sur l’hôte attendu, avec ses disques et ses données inchangés.

Si quelque chose ne correspond pas, conservez les relevés et [signalez le problème](/docs/xoa-hl/troubleshooting/) avec les versions et des ID anonymisés.

{{< details title="Sources" closed="true" >}}
Vérifié avec le commit XO 5 `e281c536` et les patchs HomeLab publiés : [barre d’actions de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [actions de migration, d’export et d’import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [boîte de dialogue de migration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/migrate-vm-modal/index.js), [réseau de migration par défaut](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/utils.js), [boîte de dialogue d’export](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/export-vm-modal/index.js), [choix de compression](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-compression.js), [page d’import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [API VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [migration, import et contrôles de démarrage XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [gestion du snapshot d’export](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [exports simultanés](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml) et [libellés de l’interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js). Modifications du menu HomeLab : [entrée d’import VMware](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzz-xoa-hl-hide-vmware-and-support-alert.patch).
{{< /details >}}
## Autres modes de transfert (VM08) {#transfer-modes}

Périmètre : XO 5.113.2 `e281c536`, sources XOA-HL ce40/ce47. Utilisez un administrateur, une VM jetable accessible par console, des disques ordinaires, un échantillon synchronisé avec somme, aucune VIF, des tâches désactivées et assez de place pour snapshots et imports. Gardez une sauvegarde indépendante. Chaque mode exige sa propre validation.

1. **Export en marche :** synchronisez, laissez la VM isolée en marche, **Export**, type **XVA**, compression **Disabled**. Téléchargez entièrement et notez taille/somme. Contrôlez le nettoyage du snapshot temporaire `[XO Export]` et la santé de la source après réussite ou annulation. Ce n'est pas un export mémoire ou cohérent au niveau applicatif.
2. **XVA compressé :** recommencez avec **GZIP (very slow)** (`native`) ; testez **Zstd** séparément uniquement si l'hôte l'annonce. Notez le choix et gardez `.xva`. Importez chaque fichier complet par **Import → VM** sur le SR jetable selon la procédure XVA. Une réussite non compressée ne valide pas les autres modes.
3. **OVA :** exportez la VM isolée en **OVA**, sans sélecteur de compression XVA. Dans **Import → VM**, ouvrez `.ova`, vérifiez nom, CPU, RAM, disques et réseaux analysés, choisissez le SR puis importez une fois. L'analyse ne prouve pas le démarrage. Consignez tout format/disque refusé sans conversion ni suppression silencieuse.
4. **URL :** placez un XVA complet et vérifié à une URL contrôlée par le propriétaire et accessible depuis l'appliance. **Import → VM → From URL**, **XVA**, URL exacte et SR de test. L'accès navigateur ne suffit pas. Aucune information d'authentification dans l'URL. Cette version refuse les imports VM par URL hors XVA. Après erreur, inventoriez les restes avant reprise.
5. **Disque seul :** **Import → Disk**, SR de test inscriptible et fichier connu `.vhd`, `.vmdk` ou `.raw` (ISO exige son SR). Vérifiez nom, format, taille et UUID VDI. Cela crée un disque, pas une VM démarrable. Attachez-le à une position libre d'une VM de récupération arrêtée, retirez toutes les VIF, démarrez et vérifiez l'échantillon. L'action de téléchargement de l'onglet **Disks** exporte un VDI : choisissez un format proposé, enregistrez sa somme puis réimportez pour le même contrôle. L'URL de cette interface disque propose seulement **ISO**.

Pour chaque VM importée, vérifiez nouvel UUID, disques, SR et état. Gardez-la arrêtée et retirez les VIF avant démarrage. Contrôlez console et somme. Nettoyez uniquement les objets identifiés après vérification. Après interruption, préservez erreur/fichier et inventaires source, destination, snapshots et capacité. Un nom de fichier ou une notification ne valide pas la restauration.

Implémentation figée: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [@xen-orchestra/xapi/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [packages/xo-server/src/xapi/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [packages/xo-web/src/xo-app/vm-import/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [packages/xo-web/src/xo-app/disk-import/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [packages/xo-web/src/xo-app/vm/tab-disks.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [packages/xo-server/src/api/disk.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs).

**Resultat du laboratoire, 2026-11-03 (partiel, API et non navigateur) :** Observe par les methodes REST et JSON-RPC d'export et d'import que ces pages utilisent. Un export a chaud de l'invite du laboratoire (disque de 4 Gio) s'est termine sans compression a 3 251 286 528 octets. `vm.export` avec `compress` a `gzip` et `zstd` a renvoye des enveloppes gzip (323 244 900 octets) et zstd (295 357 297 octets) de la meme archive, et non une compression par fragment ; les deux se decompressent en 3 251 286 528 octets. L'export REST n'accepte qu'un booleen `compress`. L'import par URL des deux fichiers compresses a fonctionne (nouvelles VM arretees avec de nouvelles adresses MAC). L'export OVA de l'invite en cours d'execution a produit `metadata.ovf` et un VMDK, mais le televersement de cet OVA vers le point d'import est reste bloque plus de neuf minutes et a laisse une VM partielle `[Importing...]` : l'import OVA n'est pas valide. L'import de disque par URL n'a accepte que VHD et raw ; les imports VMDK et QCOW2 par URL ont ete refuses et un export QCOW2 a renvoye HTTP 500 (`unknown error`). Un fichier VHD importe comme `raw` a cree un disque errone de 2 Mio : declarez donc le bon format. Aucun demarrage ni somme de controle de donnees n'a ete verifie : le mode reste ouvert.
