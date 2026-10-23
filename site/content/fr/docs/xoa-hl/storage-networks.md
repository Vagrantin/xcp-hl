---
title: "Gérer disques, stockage, bibliothèques ISO et réseaux"
linkTitle: "Stockage et réseaux"
description: "Ajoutez des disques et des interfaces réseau, connectez un stockage NFS et une bibliothèque ISO, et créez un VLAN."
weight: 50
translationKey: xoa-manual-storage-networks
translationStatus: draft
sourceRevision: sha256:c439d8d2e5c6d454625769bceb1259e67e76e3291923ad9894e3a6f10bc9217b
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Ajoutez un disque ou une interface réseau à une VM, connectez un stockage NFS pour les fichiers ISO ou les disques de VM, et créez un réseau VLAN. Entraînez-vous sur une VM de test arrêtée, jamais sur l’appliance elle-même, connecté à l’**appliance XOA-HL** en tant qu’administrateur. Avant de commencer, notez l’ID de la VM, ses disques et ses interfaces réseau.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire.
{{< /callout >}}

## Connaître les objets {#objects}

| Objet | Ce que c’est |
| --- | --- |
| SR | Un dépôt de stockage : l’endroit où sont stockés les disques virtuels. Vérifiez son espace libre |
| VDI | Un disque virtuel, stocké dans un SR |
| VBD | Le lien entre une VM et l’un de ses disques virtuels |
| VIF | L’interface réseau virtuelle d’une VM |
| PIF | Une interface réseau de l’hôte. Modifier le réseau de gestion de l’hôte peut vous couper de l’hôte |

L’interface réseau d’une VM n’est pas l’interface de gestion de l’hôte. Choisir un réseau ou générer une nouvelle adresse MAC n’isole pas une VM. Avant de connecter un invité cloné ou restauré, vérifiez le VLAN, la liaison physique et le routage réels.

## Ajouter un petit disque vide {#add-disk}

1. Vérifiez que la VM de test est arrêtée. Ouvrez **Disques** (`/#/vms/<id>/disks`) et choisissez **Nouveau disque**.
2. Choisissez un SR accessible en écriture dans le même pool, un nom de test explicite et une petite taille avec son unité. Laissez l’option lecture seule désactivée. Créez le disque une seule fois et attendez la fin.
3. Vérifiez la nouvelle ligne : nom, taille, SR et VM à laquelle le disque est attaché. Notez l’ID du disque et l’espace libre restant sur le SR avant de démarrer l’invité.

Dans la console de l’invité, repérez le nouveau disque par sa taille et ses informations de périphérique. XO crée le disque et l’attache, mais ne le partitionne, ne le formate et ne le monte pas dans l’invité. C’est une tâche distincte, propre à chaque système d’exploitation. Ne formatez jamais un périphérique d’après un nom deviné.

Si la création échoue, vérifiez la tâche et les listes de disques de la VM et du SR avant de réessayer : une opération partielle peut laisser un disque derrière elle. Conservez l’erreur, vérifiez l’espace libre et la connectivité, et consultez le [dépannage](/docs/xoa-hl/troubleshooting/) si besoin. Réduire, agrandir ou déplacer des disques n’est pas traité ici.

## Détacher ou supprimer un disque {#detach-vs-delete}

Supprimer le VBD détache le disque de la VM, mais ses données (le VDI) existent toujours. Supprimer le VDI détruit les données ; c’est une action distincte, que cet écran ne propose pas tant que le disque est attaché. Déconnecter un attachement est aussi différent de le supprimer.

Pour faire le ménage, arrêtez l’invité et identifiez avec certitude le disque de test vide. Gardez le VDI si son contenu peut encore servir. Ne supprimez jamais un disque de démarrage, un disque partagé ou un disque non identifié pour faire disparaître un avertissement d’espace. [Sauvegardez les données importantes de l’invité](/docs/xoa-hl/backup-restore/) séparément.

## Ajouter une interface réseau isolée {#add-vif}

1. Sur la VM de test arrêtée, ouvrez **Réseaux** (`/#/vms/<id>/network`) et choisissez **Nouvelle interface**.
2. Sélectionnez un réseau du même pool dont vous avez vérifié l’isolation. Laissez l’adresse MAC vide pour qu’elle soit générée, puis choisissez **Créer**.
3. Avant de démarrer la VM, vérifiez la nouvelle interface, son réseau et son adresse MAC. Après le démarrage, vérifiez que l’invité voit l’interface et dispose de la connectivité prévue.

Pour isoler un clone ou une copie restaurée, supprimez **toutes** les VIF héritées pendant que la VM est arrêtée, et vérifiez que la liste est vide avant le premier démarrage. Utilisez l’action de suppression, pas seulement le bouton de connexion : une interface déconnectée n’est pas une interface isolée. N’ajoutez un réseau de test qu’après avoir confirmé qu’il ne peut pas atteindre la production et réglé les identités copiées de l’invité.

Si la VM peut atteindre quelque chose d’inattendu, arrêtez-la, puis vérifiez le réseau choisi et l’isolation en dehors de XO avant de réessayer. Ces étapes ne configurent ni les interfaces de l’hôte (PIF), ni les adresses de gestion, ni les agrégations, ni les VLAN, et vous ne devez pas modifier le réseau de gestion de l’hôte en les suivant. Pour un VLAN sur les hôtes, voir [Créer un VLAN de laboratoire sur une liaison libre](/docs/xoa-hl/storage-networks/#host-vlan-network). Pour les autres tâches sur les VM, voir [Gérer les VM](/docs/xoa-hl/vm-operations/) ou [Hôtes et pools](/docs/xoa-hl/hosts-pools/).

## Connecter une bibliothèque ISO NFS {#nfs-iso-library}

Un SR ISO contient des médias d’installation. Il est différent d’un SR accessible en écriture pour les disques de VM, et d’une destination de sauvegarde. Ces étapes connectent un export NFS existant et dédié, qui contient déjà un ISO d’installation vérifié avec la somme de contrôle de l’éditeur. L’administrateur de stockage prépare l’export et y dépose le fichier ; vous travaillez uniquement dans le navigateur et ne modifiez rien sur l’hôte.

**Avant de commencer**

- Vérifiez si le pool dispose déjà d’un SR ISO adapté. Si son identité, l’accès des hôtes et les médias sont corrects, utilisez-le.
- Pour une nouvelle bibliothèque, notez le serveur NFS, le chemin exact de l’export, la version NFS convenue avec l’administrateur de stockage, le pool et les hôtes, ainsi que le nom de fichier et la somme de contrôle de l’ISO.
- Chaque hôte qui lira l’ISO doit être autorisé à accéder à l’export. L’accès depuis votre navigateur ou depuis l’appliance ne prouve pas que les hôtes peuvent l’atteindre.

1. En tant qu’administrateur, ouvrez **Nouveau → Stockage** (`/#/new/sr`). Choisissez un hôte du pool. Saisissez un nom explicite comme `lab-nfs-iso` et une description qui identifie l’export de test.
2. Sous **ISO SR**, sélectionnez **NFS ISO**. Ne sélectionnez pas **NFS** dans le groupe **VDI SR** : cela crée un stockage pour disques de VM. **Local** désigne un dossier sur un hôte hyperviseur, pas sur votre ordinateur ni sur l’appliance. Le stockage local, SMB et en mode bloc n’est pas traité ici.
3. Saisissez le serveur NFS dans **Serveur**. Choisissez la version NFS convenue (le formulaire propose la valeur par défaut, `4` et `4.1`), puis sélectionnez l’icône de recherche à côté du serveur. Changer la version ne relance pas la recherche : recherchez de nouveau après chaque changement. Laissez **Comma delimited NFS options** vide, sauf si des options ont été convenues.
4. Sélectionnez l’export exact dans **Chemin**, en utilisant la racine de l’export (les sous-dossiers ne sont pas traités). Attendez la vérification du chemin. Si l’export est absent, si la vérification échoue ou si **Utilisation du stockage** liste des SR existants, arrêtez-vous et examinez l’erreur et les ID. L’assistant fait des vérifications NFS même pour une bibliothèque ISO : un SR détecté n’est donc pas forcément une bibliothèque ISO. Ne le rattachez pas, et n’acceptez pas d’avertissement sur une création par-dessus un stockage existant.
5. Dans **Récapitulatif**, vérifiez le nom et le type choisi (`nfsiso`). Revérifiez l’hôte, le serveur et le chemin plus haut, puis sélectionnez **Créer** une seule fois. En cas d’échec, vérifiez la liste des SR du pool avant de réessayer : une requête échouée peut laisser un SR ou un attachement d’hôte partiellement créé.
6. Notez l’UUID du nouveau SR. Son type interne est `iso` (`nfsiso` n’est que le choix de l’assistant). Ouvrez **Hôtes** (`/#/srs/<id>/hosts`) et vérifiez que l’attachement de chaque hôte est connecté et affiche le bon export. Un SR partagé ne prouve pas que chaque hôte peut l’atteindre. N’exécutez des VM que sur les hôtes dont vous avez vérifié l’accès.
7. Utilisez l’action **Rescanner tous les disques** du SR, attendez la fin, puis ouvrez **Disques** (`/#/srs/<id>/disks`). Vérifiez le nom et la taille de l’ISO. Relancez le scan chaque fois que l’administrateur de stockage ajoute ou remplace un fichier. Vérifiez la somme de contrôle de l’éditeur à la source : un scan réussi ou un nom identique ne prouve pas que le fichier est intact.

**Vérification :** dans l’[assistant de création de VM](/docs/xoa-hl/create-vm/), choisissez le même pool et vérifiez que **ISO/DVD** propose le média attendu. Si c’est le cas, passez l’envoi depuis le navigateur. Lire un média existant et envoyer un nouveau média sont deux capacités différentes : la liste d’import ne prouve pas que ce SR accepte de nouveaux fichiers ISO. N’élargissez jamais les permissions pour faire fonctionner un envoi.

| Problème | À vérifier |
| --- | --- |
| Aucun export trouvé, ou la vérification du chemin échoue | Notez l’erreur. Avec l’administrateur de stockage, vérifiez le serveur, le chemin, la version NFS, la découverte des exports et l’accès des hôtes. Arrêtez-vous si l’assistant ne trouve pas cet export. |
| Le SR existe mais un hôte est déconnecté | Vérifiez l’attachement de cet hôte, son chemin et son accès à l’export. Un autre hôte connecté ne suffit pas. Ne déconnectez pas tous les hôtes pour tenter une réparation. |
| Le scan fonctionne mais l’ISO est absent | Vérifiez que le fichier complet est sur l’export convenu, son nom et sa taille, et le SR sélectionné. Corrigez la source, puis relancez le scan. Ne recréez pas le SR encore et encore. |
| L’ISO est absent de ISO/DVD | Vérifiez le pool de l’assistant, que le SR est bien un SR ISO, que le média est présent, et l’attachement de l’hôte. Un SR NFS pour disques de VM n’est pas un SR ISO. |
| La création échoue, ou un SR inattendu apparaît | Conservez l’erreur et la liste des UUID de SR et des attachements. Identifiez les objets partiels avant toute nouvelle tentative ou tout nettoyage. N’utilisez jamais l’oubli, la suppression ou le formatage pour faire disparaître une erreur inexpliquée. |

Ne retirez pas un ISO, et ne déconnectez ni n’oubliez son SR, tant qu’une VM l’utilise. Notez quelles VM l’utilisent et éjectez le média de l’invité de test avant de prévoir un nettoyage. La suppression d’un SR et l’envoi d’ISO ne sont pas traités ici.

## Créer un stockage NFS pour les disques de VM {#nfs-vm-storage}

Suivez cette partie quand il vous faut un **SR accessible en écriture pour les disques de VM**. Une bibliothèque ISO NFS contient des médias d’installation, et une destination de sauvegarde NFS contient des sauvegardes : ni l’une ni l’autre n’est le SR créé ici. Un stockage partagé n’est pas à lui seul une sauvegarde, et ne signifie pas que vous êtes prêt pour la migration ou la haute disponibilité (HA).

### Préparer un export dédié

- Utilisez un export de laboratoire vide et dédié, approuvé par l’administrateur de stockage, avec de la place pour un disque de test et une marge.
- Notez le serveur NFS, la racine exacte de l’export, la version et les options convenues, le pool et chaque hôte qui l’utilisera.
- L’administrateur de stockage doit autoriser la lecture et l’écriture depuis ces hôtes, et vérifier l’espace et les quotas du serveur.
- Ne réutilisez pas l’export ISO, la destination de sauvegarde ni un export qui contient des données non identifiées.

Connectez-vous à l’**appliance XOA-HL** en tant qu’administrateur ; créer et vérifier un stockage demande les droits d’administrateur sur l’hôte choisi. Notez d’abord les SR existants. Si le stockage existe déjà dans le pool, vérifiez son UUID et l’accès des hôtes au lieu de créer un autre SR. Vous n’avez pas besoin de VM pour créer le SR. S’il doit accueillir votre première VM, créez le SR et vérifiez-le ci-dessous, puis [créez et installez la VM](/docs/xoa-hl/create-vm/) dessus, et revenez ici pour le test de disque. N’utilisez jamais XOA-HL elle-même comme VM de test.

### Créer le SR et le vérifier

1. Ouvrez **Nouveau → Stockage** (`/#/new/sr`), choisissez un hôte du pool, et saisissez un nom explicite comme `lab-nfs-vdis` et une description de l’export. Sous **VDI SR**, sélectionnez **NFS**. Vérifiez que **NFS ISO**, sous **ISO SR**, n’est pas sélectionné.
2. Saisissez le **Serveur**, choisissez la version convenue dans **NFS version** (valeur par défaut, `4` ou `4.1`), et sélectionnez l’icône de recherche du serveur. Laissez **Comma delimited NFS options** vide, sauf si des options ont été convenues. Si vous changez le serveur ou la version, relancez la recherche et choisissez de nouveau le chemin : changer seulement la version ne revérifie pas l’export.
3. Sélectionnez la racine exacte de l’export dans **Chemin**, sans sous-dossier, et attendez la vérification. Regardez **Utilisation du stockage**. Si un UUID de SR existant ou une entrée déjà utilisée apparaît, arrêtez-vous et identifiez-le avec le responsable du stockage. Ne le rattachez pas et ne créez pas d’autre SR par-dessus. Pour NFS, XO ne vous demande **pas** de confirmer un stockage existant : l’absence d’avertissement ne prouve donc pas que l’export est vide.
4. Dans **Récapitulatif**, vérifiez le nom, le type `nfs` et le chemin. Revérifiez l’hôte, le serveur, la version et les options plus haut, puis sélectionnez **Créer** une seule fois et attendez. En cas d’échec, vérifiez les listes de SR et d’attachements d’hôtes avant de réessayer : une requête échouée peut laisser des objets derrière elle.
5. Notez l’UUID du nouveau SR. Dans **Général** (`/#/srs/<id>/general`), vérifiez `Type: nfs`, la taille, l’espace utilisé et libre, et le pool.
6. Ouvrez **Hôtes** (`/#/srs/<id>/hosts`). Pour chaque hôte, notez son attachement (PBD) et vérifiez qu’il affiche **Connecté**, avec les bons `server` et `serverpath` (et `nfsversion` et `options` si vous les avez définis). Un hôte connecté ne prouve pas que les autres le sont. Si un attachement manque ou est déconnecté, arrêtez-vous avant d’y placer des VM. L’état est aussi un bouton : lisez-le sans cliquer dessus.

### Tester un disque sur le nouveau SR

1. Suivez [Ajouter un petit disque vide](#add-disk) sur la VM de test arrêtée, en choisissant ce SR. Notez les ID de la VM, du disque et de l’attachement, et vérifiez le SR et la taille du disque.
2. Ne démarrez l’invité que sur un hôte dont vous avez vérifié l’attachement. Repérez le disque supplémentaire par sa taille et ses informations de périphérique. Le partitionner, le formater et le monter demande une procédure propre au système d’exploitation et une identification certaine du périphérique.
3. Si un administrateur de l’invité prépare ce **disque de test**, écrivez-y un fichier sans importance et notez sa somme de contrôle. Enregistrez votre travail, arrêtez l’invité normalement, redémarrez-le, et vérifiez le même disque, le même fichier et la même somme.

**Vérification :** le fichier et sa somme de contrôle sont inchangés après le redémarrage. Un disque vide ou un nouveau scan réussi ne prouve pas que les écritures fonctionnent ni qu’elles sont conservées. Gardez ce résultat séparé d’un test de sauvegarde et de restauration. Avant d’affirmer que tout le pool peut utiliser ce stockage, refaites le test de lecture et d’écriture sur chaque hôte, dans le cadre d’un test de placement ou de migration approuvé séparément.

### En cas de problème

| Problème | À vérifier |
| --- | --- |
| Aucun export, ou la vérification échoue | Conservez l’erreur exacte et l’hôte, le serveur, le chemin et la version choisis. Demandez à l’administrateur de stockage de vérifier la découverte, les droits des hôtes et la connectivité. Ne passez pas à un stockage local ou en mode bloc, et n’élargissez pas les droits, pour contourner le problème. |
| Un SR existant est détecté, ou la création échoue | Notez chaque UUID de SR et chaque attachement, y compris les objets partiels. Trouvez à qui ils appartiennent et ce qui les utilise avant toute nouvelle tentative ou tout rattachement. |
| Mauvais type ou mauvais chemin, ou un hôte est déconnecté | Arrêtez les nouvelles allocations. Comparez l’export que vous avez noté avec l’attachement de chaque hôte. Ne déconnectez pas tous les hôtes et ne supprimez pas de SR pour diagnostiquer. |
| Un avertissement d’espace, ou une écriture échoue dans l’invité | Vérifiez l’utilisation du SR, l’espace libre et les quotas du serveur, les tâches en cours et le disque exact dans l’invité. Gardez les preuves et les données. Ne supprimez pas de disques, d’instantanés ou de fichiers non identifiés sur le NAS. |

Pour faire le ménage, conservez la liste finale des objets et arrêtez normalement la VM de test. N’appliquez [Détacher ou supprimer un disque](#detach-vs-delete) qu’au disque de test identifié avec certitude. Gardez le SR et l’export jusqu’à ce que leur responsable ait listé chaque utilisateur et chaque besoin de récupération. Détruire, oublier ou rattacher un SR, supprimer des fichiers sur le NAS et changer le stockage par défaut ne sont pas traités ici, pas plus que le stockage local, SMB ou iSCSI, les sous-dossiers NFS, les pannes, les performances, la migration à l’échelle du pool ou la HA.

## Créer un VLAN de laboratoire sur une liaison libre {#host-vlan-network}

Cette partie **modifie la configuration de l’hôte et du pool** : elle crée un réseau invité étiqueté depuis le **navigateur XOA-HL**. Utilisez un pool de test, une liaison physique libre et dédiée, et une VM de test arrêtée. Gardez une console d’hôte séparée disponible pendant toute l’opération.

**Avant de commencer**

- Notez le pool, son maître et chaque hôte, avec les UUID des réseaux et PIF existants, les noms de périphériques, les adresses MAC, les VLAN, le MTU, les indicateurs de gestion, les modes IP et les états de connexion.
- Faites approuver par l’administrateur réseau l’ID du VLAN, les ports de commutateur étiquetés, le MTU `1500`, les adresses des invités, et les destinations autorisées et interdites.
- Vérifiez la liaison libre sur **chaque** hôte : elle ne transporte ni gestion, ni stockage, ni sauvegarde, ni autre trafic, n’a pas d’adresse IP d’hôte, et ne fait partie ni d’une agrégation ni d’un VLAN existant. Comparez avec les relevés de câblage et de commutateurs ; un nom de périphérique, ou l’absence du badge Management, ne suffit pas.
- Arrêtez-vous si vous ne pouvez pas confirmer cette configuration. Un numéro de VLAN seul n’isole rien, et ne configure ni les ports de commutateur, ni le routage, ni le DHCP, ni le DNS, ni les pare-feu.

### Créer le réseau une seule fois

1. En tant qu’administrateur, ouvrez **Nouveau → Network** (`/#/new/network`) et sélectionnez le **pool** de test (cela demande les droits d’administrateur du pool). Laissez **Bonded network** et **Private network** désactivés ; Private network est une autre fonction, de type SDN.
2. Sous **Info → Interface**, sélectionnez la **PIF libre du maître du pool** que vous avez notée. La liste montre les PIF du maître sans VLAN et masque les membres d’agrégation, mais elle **montre** les PIF de gestion. Vérifiez l’UUID, le périphérique et l’adresse MAC avec vos relevés. Ne laissez pas Interface vide : cela crée un réseau sans liaison physique, pas le VLAN voulu.
3. Saisissez un **Nom** et une **Description** explicites pour le laboratoire. Réglez **MTU** sur `1500` et **VLAN** sur l’ID exact du VLAN étiqueté approuvé. Ne laissez pas VLAN vide et n’utilisez pas `0` : un champ vide est envoyé comme `0`. Sélectionnez **No NBD Connection** ; ce réseau invité n’a pas besoin de NBD.
4. Relisez le pool, la PIF du maître, le VLAN, le MTU et les deux interrupteurs de type de réseau, puis sélectionnez **Créer un réseau** une seule fois. Attendez la fin et l’affichage de la vue **Réseaux** du pool (`/#/pools/<id>/network`). En cas d’échec, conservez l’erreur et vérifiez les réseaux du pool et les PIF de chaque hôte avant de réessayer. XO tente de nettoyer après une création échouée, mais cela ne prouve pas que chaque modification du pool a été annulée.

### Vérifier chaque hôte

1. Copiez l’UUID du nouveau réseau depuis sa ligne dans la vue du pool, et notez son nom, son MTU et son VLAN. Le résumé PIF et VLAN de cette ligne ne vient que du **maître**.
2. Développez **PIFs** et comparez chaque hôte, périphérique et adresse MAC avec vos relevés. L’icône d’état y indique le **lien physique (porteuse)**. Le bouton **Connecté** de l’onglet Réseaux d’un hôte indique si la PIF est attachée. Ni l’un ni l’autre ne prouve que le trafic étiqueté passe. Ne cliquez pas sur connecter ou déconnecter juste pour lire un état.
3. Pour chaque hôte, ouvrez **Réseaux** (`/#/hosts/<id>/network`), repérez la PIF du nouveau réseau, et notez son UUID, son périphérique, son adresse MAC, son VLAN, son MTU, son badge de gestion, son mode et son adresse IP, et son état. Vérifiez le VLAN exact approuvé, le MTU `1500`, l’état attaché, le lien attendu, et que l’hôte n’y utilise aucune adresse IP.
4. Comparez la connectivité de gestion et de stockage avec vos notes de départ.

Si une PIF manque, est déconnectée ou inattendue, arrêtez-vous avant d’y placer un invité. Ne modifiez pas les champs VLAN, MTU ou IP existants, et ne basculez pas les PIF parentes, pour corriger.

### Vérifier la connectivité de l’invité

1. Sur une VM de test arrêtée, suivez [Ajouter une interface réseau isolée](#add-vif) et choisissez exactement ce réseau. Notez les UUID de la VM et de la VIF, l’adresse MAC, le réseau et l’hôte sur lequel la VM tournera. Vérifiez qu’aucune interface héritée ne contourne la conception du laboratoire.
2. Ne démarrez la VM que sur un hôte dont vous avez vérifié la PIF. L’administrateur de l’invité configure par la console l’**interface non étiquetée** convenue et des réglages IP uniques. Ces étapes ne configurent pas de trunk VLAN dans l’invité.
3. Vérifiez séparément l’adresse, le sous-réseau, la route et le DNS de l’invité. Testez un pair ou un service approuvé, ainsi que les destinations interdites que l’administrateur a listées, y compris la production. Un ping qui échoue ne prouve pas l’isolation. Notez les tests effectués et leurs résultats.
4. Arrêtez l’invité normalement, redémarrez-le, et refaites les vérifications.

**Vérification :** l’invité atteint le pair approuvé, ne peut pas atteindre les destinations interdites, et garde ce comportement après un redémarrage ; la gestion des hôtes, le stockage et XOA-HL restent joignables tout du long. Un pair sur le même hôte ne teste ni la liaison physique ni un autre hôte : le trafic entre hôtes et la migration demandent chacun leur propre test approuvé.

| Problème | À vérifier |
| --- | --- |
| La PIF libre est absente, ou le pool n’est pas le bon | Vérifiez le maître, le périphérique physique et l’appartenance à une agrégation ou à un VLAN. Arrêtez-vous. Ne choisissez jamais une PIF de gestion ou de stockage, et ne changez pas de pool, pour contourner la liste. |
| Une erreur, un réseau en double ou des PIF absentes sur certains hôtes | Conservez les heures, l’erreur et les UUID exacts des réseaux et PIF sur chaque hôte. Examinez-les avec le responsable avant de réessayer. Une notification ne prouve pas que les modifications ont été annulées. |
| Le lien est actif mais l’invité n’a pas le trafic attendu | Vérifiez l’état attaché, la correspondance des VIF, l’IP, la route et le DNS de l’invité, le chemin étiqueté approuvé dans les commutateurs, et le pair et le pare-feu. Ne tentez jamais de deviner en modifiant l’IP de gestion de l’hôte, le MTU parent ou le VLAN. |
| Accès inattendu à la production, ou perte de la gestion ou du stockage | Arrêtez l’invité de test, conservez les preuves, et utilisez la console d’hôte séparée avec le plan de récupération de l’administrateur réseau. Ne faites aucune autre modification dans le navigateur tant que la configuration est incertaine. |

Pour terminer, conservez les relevés finaux et arrêtez normalement la VM de test. Ne retirez la VIF de test identifiée que si les étapes ci-dessus le demandent. Gardez le réseau, les PIF et la configuration des commutateurs jusqu’à ce que leur responsable ait listé chaque utilisateur et approuvé un plan de retrait et de récupération. La suppression du réseau, la modification du VLAN ou du MTU, le retrait de PIF, les agrégations, le déplacement du réseau de gestion et les réglages IP de l’hôte ne sont pas traités ici. Modifier le MTU d’un réseau existant peut débrancher puis rebrancher ses interfaces. Voir aussi [hôtes et pools](/docs/xoa-hl/hosts-pools/), le [dépannage](/docs/xoa-hl/troubleshooting/) et [Diagnostiquer la connectivité réseau](/docs/xoa-hl/troubleshooting/#network-connectivity).

{{< details title="Sources" closed="true" >}}
- **Disques et interfaces** : [interface des disques et sélection du SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [interface réseau VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [actions sur les disques et interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **Stockage NFS et bibliothèques ISO** : [assistant SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js), [API SR et vérifications](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs), [action de rescan SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js), [attachements des hôtes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js), [API d’import ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs), [sélection ISO de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **Capacité du SR** : [XO5 `tab-general.js`](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js).
- **Réseaux VLAN** : [assistant VLAN](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/network/index.js), [API réseau](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/network.mjs), [création et nettoyage du VLAN du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [vue réseau du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [vue de la porteuse des PIF](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [vue réseau de l’hôte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [champs des PIF et réseaux](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [opérations sur le MTU](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/network.mjs).
{{< /details >}}
