---
title: "Gérer les VM : console, snapshots, copies, mémoire et suppression"
linkTitle: "Gérer les VM"
description: "Utilisez la console, démarrez et arrêtez une VM, prenez des snapshots, copiez, redimensionnez et supprimez des VM."
weight: 40
translationKey: xoa-manual-vm-operations
translationStatus: draft
sourceRevision: sha256:7c18d61073e570872e7dba3b0dbad4bc8ec204f2c28bef3c65edeab15bf7cf50
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Les tâches courantes sur une VM : utiliser la console, démarrer et arrêter une VM, créer et restaurer des snapshots, faire des clones et des copies, modifier le CPU et la mémoire, et supprimer une VM. Entraînez-vous sur une VM de test sans données de production, connecté à l’**appliance XOA-HL** avec un compte administrateur. Avant de modifier une VM importante, assurez-vous d’avoir une [sauvegarde indépendante et une restauration testée](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261009-5f33c81`, paquet `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Les versions ultérieures peuvent différer.
{{< /callout >}}

## Utiliser la console d’une VM {#vm-console}

La console affiche l’écran de la VM dans votre navigateur. Il faut le droit d’**opérer** la VM : un droit Viewer ne suffit pas. L’invité n’a pas besoin d’adresse IP pour la console, mais votre navigateur doit joindre l’appliance, et l’appliance doit joindre l’hôte. Gardez l’isolation réseau de la VM de test telle quelle.

1. Ouvrez l’onglet **Console** de la VM (`/#/vms/<id>/console`). Vérifiez qu’il s’agit de la bonne VM et que son état est **Running**. Pour tout autre état, y compris en pause ou suspendue, l’onglet affiche **Console is only available for running VMs.** Démarrez la VM par une [opération d’alimentation](#vm-power) prévue ; ne forcez jamais un redémarrage juste pour obtenir une console.
2. Attendez l’écran attendu : invite de connexion, installateur ou application connue. Les identifiants saisis ici sont ceux de l’invité, pas ceux de XOA-HL ou de l’hôte.
3. Placez le pointeur dans la zone de la console pour envoyer clavier et souris à l’invité. Sortez-le pour les récupérer, ainsi que les raccourcis XO. Pour tester la saisie, tapez un texte sans risque comme `console-test` dans un éditeur de l’invité de test, puis effacez-le. Ne testez jamais dans une commande de shell ou un champ de mot de passe. Voir l’écran ne prouve pas que la saisie fonctionne.
4. Sur un grand écran, les réglages de zoom commencent à **100 %**. Ils changent l’affichage dans votre navigateur, pas la résolution de l’invité, et peuvent être masqués sur un petit écran. **Cacher les infos** et **Afficher les infos** ne font que masquer ou afficher l’en-tête XO ; ils n’arrêtent pas l’invité et ne passent pas en plein écran.
5. Une fois terminé, quittez l’onglet. Cela ferme la connexion de console sans arrêter l’invité. Si la VM a redémarré pendant la connexion, rouvrez l’onglet pour obtenir un écran à jour. XO peut ne pas détecter une déconnexion après un redémarrage, et ses tentatives de reconnexion automatique ne prouvent pas que l’invité va bien.

**Vérification :** vous voyez le bon invité en marche, votre saisie de test lui parvient, les commandes XO fonctionnent de nouveau quand le pointeur quitte la console, et la VM reste dans l’état attendu.

### Presse-papiers et boutons de clients distants

- La zone de texte du presse-papiers envoie son contenu au presse-papiers de l’invité après un court délai. **Copier** copie le texte de la zone dans le presse-papiers de votre ordinateur. Le bouton multiligne ouvre **Send to clipboard**. Testez avec un texte sans importance, et vérifiez le collage dans l’invité séparément. Ne mettez jamais de mot de passe ou de données privées dans la zone ni dans des captures.
- **SSH**, **SSH as…** et **RDP** ouvrent le gestionnaire `ssh://` ou `rdp://` de votre ordinateur avec l’adresse IP signalée par l’invité. Les boutons apparaissent quand une adresse IP est signalée. Cela ne prouve pas qu’un client est installé, que l’invité fait tourner le service, ni que le réseau l’autorise. Ces boutons ne réparent ni ne remplacent la console.
- **Ctrl+Alt+Supp** demande une confirmation, puis envoie cette combinaison de touches à l’invité. Selon l’invité, cela peut le redémarrer. Annulez pour ce test ; ce n’est pas un test de connexion. Le sélecteur ISO change le média monté dans l’invité : consultez [Créer votre première VM](/docs/xoa-hl/create-vm/) avant de le modifier.

### Corriger une console vide ou qui ne répond pas

1. **La VM ne fonctionne pas, ou la console est désactivée.** Lisez d’abord l’état et le message. Une VM en marche avec `disable_pv_vnc=1` affiche **Console is disabled for this VM** à la place de l’écran. Demandez au responsable de ce réglage avant de modifier la VM. Installer des outils ou redémarrer ne réactive pas la console.
2. **La connexion ne s’ouvre jamais, ou se coupe sans cesse.** Vérifiez que votre compte peut opérer la VM et que la connexion à l’hôte est saine. Dans les outils de développement du navigateur, repérez la requête WebSocket finissant par `/api/consoles/<id>` et notez son erreur ou son état. Un proxy inverse devant l’appliance doit autoriser les mises à niveau WebSocket, pas seulement les requêtes de page ordinaires. Vérifiez l’accès du navigateur à l’appliance (TLS compris) séparément de l’accès de l’appliance à l’hôte. L’adresse IP, le serveur SSH et le pare-feu de l’invité ne font pas partie du chemin de la console. Corrigez le problème avec le responsable de ce chemin. N’exposez jamais un port VNC publiquement et ne désactivez jamais la vérification des certificats comme solution rapide.
3. **La connexion s’ouvre, mais l’écran est vide ou figé.** Vérifiez que vous avez ouvert la bonne VM, ce qu’elle devrait afficher et les opérations d’alimentation récentes. Rouvrez l’onglet après un redémarrage. Un écran vide peut venir de l’invité ou de la connexion : notez ce que vous voyez avant d’essayer une correction propre à l’invité. Ne redémarrez pas la VM en boucle, ne la réinstallez pas et ne changez pas son média de démarrage simplement parce que l’écran est noir.
4. **L’écran fonctionne, mais la saisie ou le presse-papiers non.** Sortez le pointeur de la console puis revenez-y, et refaites le test dans l’éditeur. Vérifiez si votre navigateur ou votre système intercepte les touches, et si l’invité prend en charge l’opération de presse-papiers. Traitez séparément les problèmes SSH ou RDP. Dans votre [signalement](/docs/xoa-hl/troubleshooting/#signaler-un-problème), indiquez le navigateur et sa version, les ID de la VM et de l’hôte, l’heure, l’état d’alimentation, le message exact et les erreurs de connexion, sans données privées. Gardez les traces brutes du navigateur privées : cookies, jetons, texte du presse-papiers et écrans de l’invité peuvent être sensibles.

## Démarrer, arrêter et redémarrer une VM {#vm-power}

Ouvrez la VM (`/#/vms/<id>/general`). Si elle est arrêtée, sélectionnez le bouton de démarrage, libellé **Créer** dans cette version, et attendez que son état et sa console montrent l’invité qui démarre. Si elle fonctionne, **Arrêter** ou **Redémarrer** demande d’abord à l’invité un arrêt ou un redémarrage propre.

Si l’invité ne peut pas répondre, ou si l’opération est bloquée, XO peut proposer une seconde confirmation qui force l’opération ou contourne le blocage. Lisez ce message avant de continuer. Un arrêt ou un redémarrage forcé peut faire perdre des données dans l’invité : arrêtez depuis l’invité quand c’est possible. Ne cliquez pas de nouveau pendant qu’une tâche est en cours. Ensuite, vérifiez l’état de la VM et la console : un message de succès ne signifie pas que l’application fonctionne.

Avant de diagnostiquer des outils manquants ou de forcer une opération d’alimentation, [vérifiez l’état des outils invités](/docs/xoa-hl/guest-tools/#guest-tools-status).

## Snapshot, clone, copie ou sauvegarde ? {#protection-types}

| Option | Ce qu’elle apporte, et sa limite |
| --- | --- |
| Snapshot | La VM à un instant donné, stockée avec ses disques. Pas une sauvegarde indépendante |
| Clone rapide | Une autre VM qui partage le stockage de l’original. Aucune protection si ce stockage est perdu |
| Copie complète | Une autre VM avec des disques copiés sur un SR de votre choix. Vérifiez ses données, son emplacement et son isolation avant usage |
| Sauvegarde | Une copie de récupération séparée. À prouver par une restauration isolée |

Les snapshots et les clones consomment davantage de stockage à mesure que les VM changent. Vérifiez l’espace libre du SR, et ne supprimez que des objets de test clairement identifiés. Un snapshot d’une VM en marche n’est pas garanti cohérent pour ses applications.

## Créer un snapshot d’une VM arrêtée <span class="hx:absolute" id="3-créer-et-vérifier-un-snapshot-à-froid"></span> {#stopped-snapshot}

Utilisez une VM de test avec des disques ordinaires (sans disque partagé ni périphérique en passthrough) et une console qui fonctionne. Suspendez ses planifications de sauvegarde et de réplication, et attendez la fin des tâches en cours. Gardez une copie de récupération indépendante des données nécessaires. Les snapshots de VM en marche, les snapshots avec mémoire et la cohérence applicative ne sont pas couverts ici.

1. Dans l’invité, créez un fichier sans importance contenant `snapshot-A` et notez sa somme de contrôle. Arrêtez proprement l’invité et vérifiez que la VM est **Halted**.
2. Notez l’UUID de la VM, chaque disque (VDI) avec son ID, son SR et sa taille, les UUID des snapshots existants et l’espace libre du SR. Ensuite, [supprimez toutes les interfaces réseau (VIF) de la VM de test](/docs/xoa-hl/storage-networks/) et vérifiez que la liste est vide. À partir de là, utilisez la console.
3. Vérifiez le nom de chaque disque. Un disque dont le nom contient `[NOSNAP]` peut être exclu des snapshots ; il s’agit d’une partie du nom du disque, pas d’un tag de VM. Les disques exclus, partagés ou en passthrough demandent une autre procédure. Ne renommez pas de disque pour contourner une politique existante. Prévoyez l’espace pour le snapshot, les écritures suivantes et le snapshot supplémentaire pris avant une restauration.
4. Ouvrez **Instantanés** (`/#/vms/<id>/snapshots`) et sélectionnez une seule fois **Nouvel instantané**. Le snapshot est créé immédiatement, sans demander de nom. Le nom par défaut est le nom de la VM suivi d’un horodatage. N’utilisez pas **New snapshot with memory**.
5. Attendez et actualisez. Retrouvez la nouvelle ligne par sa **Date de création**, et copiez son UUID avec le bouton de copie de la ligne. Notez cet UUID : un nom ou une heure ne suffit pas.
6. Réglez **Nom** sur `lab-snapshot-A` et **Description** sur une courte note de test. Actualisez et vérifiez les deux valeurs. Comparez les disques et les SR du snapshot avec vos notes, et vérifiez les erreurs et l’espace libre. Les ID de disque du snapshot sont nouveaux : comparez les disques couverts et leur taille, pas leurs ID.

**Vérification :** un seul snapshot identifié couvre les disques prévus, et la VM d’origine est arrêtée, sans VIF.

Si la création ou le renommage échoue, conservez l’erreur et les listes réelles de VM, de snapshots et de disques avant de réessayer. Un ID ou une notification manquants ne prouvent pas que rien n’a été créé, et un renommage en échec n’annule pas le snapshot.

## Restaurer un snapshot <span class="hx:absolute" id="4-restaurer-uniquement-la-vm-de-test"></span> {#snapshot-revert}

{{< callout type="warning" >}}
Restaurer un snapshot remplace l’état actuel de la VM, y compris des réglages qui peuvent faire revenir d’anciennes interfaces réseau. Les changements faits après le snapshot peuvent être perdus. Ne restaurez que cette VM de test isolée, gardez-la arrêtée pendant la restauration, et revérifiez ses VIF avant de la démarrer. Un snapshot sur le même SR ne vous protège pas si ce SR est perdu.
{{< /callout >}}

1. Démarrez la VM de test isolée, remplacez le contenu du fichier par `snapshot-B` et notez la nouvelle somme de contrôle. Arrêtez-la proprement et vérifiez qu’elle est **Halted**. Notez les disques, VIF et snapshots actuels.
2. Vérifiez par son UUID que le snapshot à utiliser est bien `lab-snapshot-A`, créé à la section précédente. Ce ne doit être ni un snapshot créé par une tâche de sauvegarde, ni le snapshot d’une autre VM.
3. Dans **Instantanés**, sélectionnez **Restaurer la MV à cet instantané** sur cette ligne (libellé tel qu’affiché), et lisez la confirmation **Restaurer la VM**. Laissez **Faire un instantané avant** coché, et vérifiez d’abord l’espace libre. Cette option, cochée par défaut, enregistre l’état actuel dans un snapshot séparé avant la restauration. Ce n’est pas une sauvegarde indépendante, et elle ne garantit pas un retour arrière. Annulez si la VM, son isolation ou l’espace libre sont incertains.
4. Confirmez une seule fois et attendez. Actualisez, puis notez l’UUID du snapshot restauré, celui du nouveau snapshot « avant », l’état d’alimentation, les disques, les VIF et toute erreur. Si le snapshot « avant » échoue, XO ne demande pas la restauration. Si la restauration échoue ensuite, le snapshot « avant » peut rester. Vérifiez l’état réel avant toute nouvelle tentative, et ne décochez pas **Faire un instantané avant** pour contourner une erreur inexpliquée.
5. Avant de démarrer la VM, vérifiez qu’elle est **Halted** et que sa liste de VIF est vide. Si une VIF est revenue, supprimez-la pendant que la VM est arrêtée. Un snapshot pris pendant que la VM était en marche peut faire démarrer ou reprendre la VM d’elle-même après une restauration ; ces snapshots ne sont pas couverts ici.
6. Démarrez la VM et ouvrez la console. Vérifiez que le fichier contient `snapshot-A` avec la somme de contrôle d’origine, et que les disques et l’application fonctionnent. Arrêtez la VM et notez le résultat. Le snapshot « avant » supplémentaire contient l’état `snapshot-B`. Récupérer cet état est une restauration séparée et maîtrisée, pas un bouton d’annulation.

### Supprimer un snapshot de test {#snapshot-cleanup}

Une fois le résultat noté, et toute copie de récupération indépendante nécessaire conservée, gardez la VM arrêtée. Ne supprimez qu’un snapshot de test dont vous avez noté l’UUID et le propriétaire.

1. Dans **Instantanés**, sélectionnez **Supprimer cet instantané** sur cette ligne. Lisez la confirmation **Supprimer l'instantané** et ne confirmez qu’un seul snapshot. N’utilisez pas **Remove selected snapshots**, ne supprimez pas un snapshot créé par une tâche de sauvegarde, et ne confondez pas cette action avec **Supprimer** sur la VM.
2. Attendez, puis actualisez les snapshots, les disques de la VM et l’espace libre du SR. Vérifiez que le snapshot a disparu, que les snapshots conservés et la VM sont toujours là, et qu’aucune erreur n’apparaît.

Le nettoyage des disques peut journaliser des erreurs sans faire échouer toute la suppression. Une ligne qui disparaît ou un message de succès ne prouvent pas que le nettoyage est terminé ni que l’espace est libéré immédiatement. Notez les ID restants et [signalez les objets inexpliqués](/docs/xoa-hl/troubleshooting/). Ne supprimez jamais en masse des disques qui semblent orphelins. Un snapshot supprimé ne peut pas être récupéré.

## Faire un clone rapide isolé {#fast-clone}

1. Sur une VM de test arrêtée, sélectionnez **Clonage rapide**. Retrouvez la nouvelle VM (son nom par défaut se termine par `_clone`), notez son ID et renommez-la.
2. Gardez le clone arrêté pendant que vous [supprimez toutes les interfaces réseau héritées](/docs/xoa-hl/storage-networks/), ou mettez en place une isolation vérifiée en dehors de XO. Une nouvelle adresse MAC ne change ni les adresses IP, ni les identifiants, ni les identités applicatives copiés.
3. Démarrez le clone et vérifiez sa console. Ne reconnectez un réseau qu’après avoir résolu les identités dupliquées et vérifié l’isolation.

Si aucun clone n’apparaît après une erreur, vérifiez l’inventaire et les tâches avant de réessayer. Cela ne teste ni la migration à chaud, ni les snapshots avec mémoire, ni la récupération après la perte d’un SR.

### Faire une copie complète dans le même pool {#full-copy}

Utilisez **Copier**, et non l’action séparée **Clonage rapide**, pour obtenir des copies ordinaires des disques sur un SR de votre choix. La fenêtre de copie propose aussi **Fast clone** ; gardez **Full copy** sélectionné ici. Ni un clone rapide ni une copie complète dans le même pool ne constituent une sauvegarde indépendante ou une reprise après sinistre testée.

1. Utilisez une seule VM de test avec des disques ordinaires, sans disque partagé ni périphérique en passthrough. Dans l’invité, notez un fichier sans importance et sa somme de contrôle. Arrêtez proprement l’invité et vérifiez qu’il est **Halted**. Notez l’ID de la VM, l’ID, le SR et la taille de chaque disque, les VIF et les éventuels snapshots. L’historique des snapshots ne fait pas partie de ce test.
2. Choisissez un autre **SR de disques de VM accessible en écriture dans le même pool**. Vérifiez son ID, son espace libre, et que l’hôte qui fera tourner la copie peut le joindre. Une bibliothèque ISO ne convient pas. Prévoyez l’espace pour les copies et leur croissance : la fenêtre ne réserve ni ne vérifie l’espace. Si le SR cible n’est pas disponible, réglez l’accès au stockage avant de commencer.
3. Sur la VM source, sélectionnez **Copier**. Dans **Copier la VM**, réglez **Nom** sur un nom de test unique, par exemple `lab-vm-full-copy`. La valeur par défaut est `{name}_COPY`, et un champ vide conserve le nom d’origine. Vérifiez que **Full copy** est sélectionné.
4. Dans **Sélectionner le SR**, choisissez le SR d’après l’ID et le pool notés, pas d’après un nom ressemblant. D’autres pools peuvent apparaître dans la liste ; en choisir un passe par un export et un import, que ce test ne couvre pas. Laissez **Compression** sur **Disabled** : dans un même pool, la copie n’est pas compressée.
5. Confirmez une seule fois et attendez la tâche. Actualisez, et retrouvez la nouvelle VM par son propre ID et le nom choisi. Vérifiez qu’elle est **Halted**, ainsi que le nombre de disques, leur taille, leurs nouveaux ID et le SR de chacun. Vérifiez que la VM source et ses disques n’ont pas changé. Si la nouvelle VM fonctionne, ou si quelque chose diffère, arrêtez-vous et rétablissez l’isolation avant de continuer.
6. Gardez la nouvelle VM arrêtée pendant que vous [supprimez toutes les VIF héritées](/docs/xoa-hl/storage-networks/), et vérifiez que la liste est vide avant le premier démarrage. Ne comptez pas sur de nouvelles adresses MAC : les adresses IP, identifiants et identités applicatives de l’invité sont copiés.
7. Démarrez uniquement la copie isolée, ouvrez sa console, et vérifiez la somme de contrôle du fichier, les disques et l’application. Résolvez les identités dupliquées avant de connecter un réseau, et gardez l’original isolé ou arrêté pendant la vérification.
8. Arrêtez la copie. Notez le résultat, puis suivez [Supprimer une VM de test](#delete-vm) pour supprimer uniquement la copie et ses disques. Conservez la source et toute sauvegarde indépendante.

En cas d’erreur, de perte de connexion ou de requête interrompue, conservez la tâche, l’erreur et les listes de VM, de disques et de snapshots des deux côtés avant de réessayer. Une copie incomplète n’est pas annulée automatiquement, et l’absence d’ID de VM ne prouve pas que rien n’a été créé. Vérifiez l’espace et l’accès de l’hôte au SR, rapprochez les ID exacts, et [signalez les objets inexpliqués](/docs/xoa-hl/troubleshooting/). Ne relancez jamais à l’aveugle et ne supprimez jamais en masse des disques qui semblent orphelins.

Non couvert ici : copies de VM en marche ou suspendues, copies vers un autre pool, copies de modèles, disques partagés ou en passthrough, historique des snapshots et récupération après la perte d’un SR.

## Modifier le CPU et la mémoire {#resize-vm}

Prévoyez une fenêtre de maintenance et utilisez un invité de test dont la console est accessible. Avant toute modification, notez l’ID de la VM, l’état de l’invité, et les valeurs et limites actuelles de CPU et de mémoire. Vérifiez la capacité de l’hôte et du pool et les besoins de l’invité ; ce guide ne recommande aucun nombre de CPU ni taille de mémoire.

{{< callout type="warning" >}}
Arrêtez d’abord proprement l’invité et vérifiez qu’il est **Halted**. Si vous modifiez une VM en marche et qu’une valeur ne peut pas changer à chaud, XO peut proposer un redémarrage normal ou forcé. Annulez-le ici et arrêtez d’abord la VM. Augmenter une limite ne réserve pas de ressources sur l’hôte, et réduire la mémoire peut empêcher l’invité de démarrer.
{{< /callout >}}

1. Ouvrez **Avancé** (`/#/vms/<id>/advanced`) et notez **Limites de CPU** et **Limites de mémoire (min/max)**. La ligne CPU affiche les valeurs actuelle et maximale. Le maximum est modifiable quand la VM est arrêtée. Pour utiliser plus de CPU que le maximum actuel, augmentez d’abord le maximum.
2. Ouvrez **Général** (`/#/vms/<id>/general`). Cliquez sur le nombre de CPU, tapez le nouveau nombre entier et appuyez sur **Entrée**. Attendez, actualisez et vérifiez la valeur avant la modification suivante. Ces champs peuvent aussi enregistrer quand vous cliquez ailleurs : cliquer ailleurs n’est donc pas un moyen sûr d’annuler.
3. Cliquez sur la valeur de mémoire, réglez la nouvelle quantité et son unité, puis appuyez sur **Entrée**. Cette valeur est le **maximum dynamique** configuré, pas la mémoire utilisée par l’invité. Selon les limites existantes, XO modifie une mémoire fixe ou les limites de mémoire dynamique.
4. Actualisez **Général** et **Avancé**, et notez toutes les valeurs obtenues. Le nombre de CPU ne doit pas dépasser son maximum. Les limites de mémoire doivent rester dans l’ordre : minimum statique ≤ minimum dynamique ≤ maximum dynamique ≤ maximum statique. XO peut ajuster des limites liées : ne supposez pas que seul le champ cliqué a changé.
5. Démarrez la VM de test, et vérifiez sa console, le CPU et la mémoire vus dans l’invité, et l’application. Si elle ne démarre pas, ou si les valeurs sont fausses, gardez-la arrêtée, conservez l’erreur de la tâche et remettez les réglages notés dans la même fenêtre. Revérifiez chaque limite, et ne réessayez qu’une fois la cause connue.

Si une modification affiche une erreur, vérifiez les valeurs réelles avant de réessayer. Les changements liés ne sont pas appliqués en une seule étape « tout ou rien », et une modification refusée ne prouve pas que les anciennes valeurs sont revenues. Gardez le [dépannage](/docs/xoa-hl/troubleshooting/) et vos notes à portée de main.

Non couvert ici : modification à chaud (hot-plug), mémoire dynamique sous charge et réglage de la topologie CPU.

## Supprimer une VM de test {#delete-vm}

{{< callout type="warning" >}}
**Supprimer** efface la VM. Ce n’est pas la même chose que déconnecter ou détacher un disque. Dans cette version, la confirmation ne propose pas de conserver les disques : la suppression efface aussi les snapshots de la VM et tente de supprimer ses disques attachés. Si des données ou un snapshot doivent être conservés, arrêtez-vous avant de confirmer et prévoyez comment les garder. Un snapshot de cette VM n’est pas une copie de récupération indépendante.
{{< /callout >}}

1. Vérifiez que la cible est la VM de test, et non l’appliance, l’invité d’origine, un modèle ou une autre VM au nom proche. Notez son ID, ses disques attachés avec leurs ID et SR, et ses snapshots.
2. Vérifiez ses planifications de sauvegarde et de réplication, et si une autre VM utilise l’un de ses disques. Pour des données importantes, faites d’abord une [sauvegarde indépendante et testez une restauration isolée](/docs/xoa-hl/backup-restore/).
3. Arrêtez normalement l’invité et vérifiez qu’il est **Halted**. La suppression peut arrêter brutalement une VM encore en marche ou suspendue : n’utilisez jamais **Supprimer** pour arrêter une VM.
4. Ouvrez **Avancé** et sélectionnez **Supprimer**. Lisez l’avertissement sur la VM et ses disques, et ne confirmez que cette VM. Si XO propose ensuite de supprimer quand même une VM protégée ou bloquée, annulez et cherchez la raison de cette protection. N’acceptez pas une nouvelle tentative forcée.
5. Attendez, puis actualisez les listes de VM, de snapshots et de disques des SR. Vérifiez les ID notés, ainsi que la tâche et ses erreurs. Les disques partagés encore attachés à une autre VM sont ignorés, mais cela ne protège pas tous les disques. Des erreurs de nettoyage de snapshots ou de disques peuvent être journalisées sans faire échouer toute la suppression : une VM qui disparaît ou un message de succès ne prouvent donc pas que le nettoyage est terminé.
6. Vérifiez que la VM d’origine, les autres invités et toute sauvegarde indépendante fonctionnent toujours. Examinez un par un les objets de test restants, avec vos notes et le [guide des disques](/docs/xoa-hl/storage-networks/). Ne supprimez jamais en masse des disques qui semblent orphelins, et ne relancez pas une opération forcée pour libérer de l’espace. Il n’y a pas d’annulation : des données d’invité supprimées ne peuvent revenir que depuis une copie de récupération testée séparément.

Si la suppression échoue en cours de route, ou si vous annulez une suppression bloquée, conservez les listes restantes de VM, de disques et de snapshots et l’erreur. Si la VM existe encore, vérifiez aussi ses droits, ses réservations de pool IP et son appartenance à un ensemble de ressources : XO commence une partie de cette gestion avant de vérifier la protection de la VM, donc un refus ne prouve pas que ces enregistrements sont inchangés. Ne créez pas une VM au nom proche en supposant qu’il s’agit du même objet. [Signalez le problème](/docs/xoa-hl/troubleshooting/) avec les versions et les ID (sans données privées) avant tout autre nettoyage.

{{< details title="Sources" closed="true" >}}
- **Console** : [onglet/commandes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-console.js), [capture/échelle/reconnexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/react-novnc.js), [authentification/droit d’opérer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [proxy vers la console de l’hôte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **Copie complète** : [fenêtre de copie, valeurs initiales et motif de nom](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/copy-vms-modal/index.js), [requêtes de copie/clonage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [droits VM/SR et branche selon le pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [code XAPI de copie/clonage/copie distante](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [sélecteur de SR accessibles en écriture](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **CPU, mémoire et suppression** : [contrôles Général](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [limites/Supprimer dans Avancé](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [enregistrement des champs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [permissions/paramètres VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [ordre des contraintes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [suppression/disques partagés/nettoyage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [libellés et avertissements de l’interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Alimentation et snapshots** : [actions d’alimentation et de snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [barre d’actions VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [onglet snapshots](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [confirmation de retour au snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js), [état après retour au snapshot](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **Couverture et suppression des snapshots** : [détection dans le nom des disques et nettoyage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs).
{{< /details >}}
