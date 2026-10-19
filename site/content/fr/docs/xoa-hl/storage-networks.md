---
title: "Gérer disques, stockage, bibliothèques ISO et réseaux"
linkTitle: "Stockage et réseaux"
description: "Ajoutez des disques et des interfaces réseau, connectez un stockage NFS et une bibliothèque ISO, et créez un VLAN."
weight: 50
translationKey: xoa-manual-storage-networks
translationStatus: draft
sourceRevision: sha256:264f8565b5015983b162610ece46662eee8d99fe29757d23b63fc237de525f73
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Utilisez une VM jetable arrêtée, avec un compte administrateur dans l’**appliance XOA-HL**. Notez son identité, ses disques et interfaces existants. Choisissez un SR inscriptible avec assez d’espace libre et un réseau existant dont l’isolation a été vérifiée en dehors de XO. N’utilisez pas l’appliance comme invité de test.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Les tests de création NFS, de VLAN hôte, de disque, d’interface et de détection dans l’invité sur l’appliance publiée restent à faire.
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

Si la connectivité est inattendue, arrêtez la VM de test et inspectez le réseau choisi et l’isolation externe avant de réessayer. Cet exercice d’interface VM ne configure pas les PIF, adresses de gestion, agrégations ou VLAN de l’hôte. Pour un exercice distinct sur pool jetable, voir [Créer un VLAN de laboratoire](/docs/xoa-hl/storage-networks/#host-vlan-network). Ne modifiez pas le réseau de gestion de l’hôte pendant cet exercice. Poursuivez avec [les opérations VM](/docs/xoa-hl/vm-operations/) ou [la gestion des hôtes et pools](/docs/xoa-hl/hosts-pools/).

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

## 6. Créer un stockage NFS pour les disques de VM {#nfs-vm-storage}

Utilisez cet exercice distinct pour créer un **SR inscriptible pour les disques de VM**. Une bibliothèque ISO NFS fournit les médias d’installation ; une destination NFS de sauvegarde conserve des sauvegardes indépendantes. Ce sont des usages distincts du SR créé ici. Le stockage partagé seul ne constitue pas une sauvegarde et ne prouve pas que la migration ou la haute disponibilité sont prêtes.

### Préparer un export dédié

Utilisez un export de laboratoire vide et dédié, approuvé par son administrateur de stockage, avec assez d’espace pour le disque de test et une réserve. Notez le serveur NFS, la racine exacte de l’export, la version et les options convenues, le pool et tous les hôtes prévus. L’administrateur doit autoriser leur accès en lecture/écriture et vérifier l’espace serveur et les quotas. Ne réutilisez ni l’export ISO, ni la destination de sauvegarde, ni un export contenant des données non identifiées. La configuration du NAS et du réseau des hôtes est hors de cet exercice dans le navigateur.

Connectez-vous à l’**appliance XOA-HL** comme administrateur. Les API de création et de détection exigent le droit d’administrer l’hôte sélectionné. Notez d’abord les SR existants. Si le stockage prévu existe déjà dans ce pool, vérifiez son UUID et l’accès des hôtes au lieu de créer un autre SR. La création du SR ne nécessite pas de VM existante. Pour vérifier ensuite le disque, utilisez une VM jetable arrêtée, un accès console indépendant et une sauvegarde indépendante des données importantes. S’il s’agit de votre première VM, [créez-la et installez-la](/docs/xoa-hl/create-vm/) sur le nouveau SR après les contrôles du SR ci-dessous, puis revenez ici. N’utilisez pas XOA-HL comme VM de test.

### Créer le SR et vérifier son état

1. Ouvrez **Nouveau → Stockage** (`/#/new/sr`), choisissez un hôte du pool prévu et saisissez un nom distinct comme `lab-nfs-vdis`, avec une description identifiant l’export. Dans **VDI SR**, choisissez **NFS**. Vérifiez que **NFS ISO**, dans **ISO SR**, n’est pas sélectionné.
2. Renseignez **Serveur**, choisissez la version NFS convenue (valeur par défaut, `4` ou `4.1`) et utilisez l’icône de recherche du serveur. Laissez **Comma delimited NFS options** vide sauf options précises convenues. Après un changement de serveur ou de version, refaites la détection et la sélection du chemin ; changer uniquement la version ne relance pas la sonde. Les libellés de version/options NFS restent en anglais dans ce catalogue.
3. Choisissez la racine exacte de l’export dans **Chemin**, sans utiliser de sous-répertoire, et attendez la sonde. Examinez **Utilisation du stockage**. Si un UUID de SR existant ou une entrée déjà utilisée apparaît, arrêtez et identifiez-le avec le propriétaire du stockage. Ne choisissez ni rattachement ni création d’un autre SR par-dessus. La branche de création NFS ne demande **pas** la confirmation de stockage existant utilisée pour certains autres types ; l’absence d’avertissement ne prouve pas que l’export est vide.
4. Dans **Récapitulatif**, vérifiez le nom, le type `nfs` et le chemin. Revérifiez l’hôte, le serveur, la version et les options dans les sections précédentes, puis choisissez **Créer** une seule fois. Attendez la fin. En cas d’erreur, examinez les SR et les attachements des hôtes avant toute nouvelle tentative ; une requête échouée peut laisser des objets.
5. Notez l’UUID du SR obtenu. Dans **Général** (`/#/srs/<id>/general`), vérifiez `Type: nfs`, la taille, l’espace utilisé/libre et le pool prévu. Ouvrez **Hôtes** (`/#/srs/<id>/hosts`) : notez chaque hôte et son attachement (PBD), vérifiez **Connecté**, les entrées `server` et `serverpath`, ainsi que `nfsversion`/`options` si fournies. La déclaration de partage ou un seul hôte connecté ne vérifie pas tous les hôtes. Si un attachement prévu manque ou est déconnecté, arrêtez avant d’y allouer ou déplacer des charges. Le bouton d’état déclenche une action : lisez-le sans cliquer pour le tester.

### Vérifier un disque jetable

Suivez [Ajouter un petit disque vide](#2-ajouter-un-petit-disque-vide) en choisissant ce SR exact sur la VM de test arrêtée. Notez les identités VM, VDI et attachement, puis revérifiez le SR et la taille du disque. Ne démarrez l’invité que sur un hôte dont l’attachement a été contrôlé. Identifiez le disque supplémentaire par sa taille et ses informations ; le partitionnement, le formatage et le montage exigent une procédure propre à l’OS et l’identification certaine du périphérique.

Si un administrateur de l’invité prépare ce **disque de test**, écrivez-y un fichier sans importance et notez sa somme de contrôle. Après enregistrement du travail et arrêt/démarrage normal de l’invité, vérifiez le même disque, le fichier et sa somme. Distinguez ce résultat d’un test de sauvegarde/restauration indépendant. Allouer un disque vide ou réussir un scan ne démontre pas les écritures ni leur persistance. Répétez la validation en lecture/écriture sur chaque hôte prévu via un exercice de placement/migration approuvé séparément avant d’affirmer un accès dans tout le pool.

### Traiter les échecs et préparer le nettoyage

| Symptôme | Vérification et suite |
| --- | --- |
| Export absent ou sonde échouée | Conservez l’erreur exacte et l’hôte, le serveur, le chemin et la version choisis. Faites vérifier détection, droits des hôtes et connectivité par l’administrateur de stockage. Ne contournez pas l’échec avec un stockage local/bloc ou des droits élargis. |
| SR existant détecté ou création échouée | Notez tous les UUID de SR détectés/obtenus et leurs attachements, y compris les objets partiels. Identifiez propriétaires et utilisateurs avant toute nouvelle tentative ou décision de rattachement. |
| Type/chemin incorrect ou hôte déconnecté | Arrêtez les nouvelles allocations ; comparez l’export enregistré à chaque attachement. Ne déconnectez pas tous les hôtes et ne supprimez pas de SR pour diagnostiquer. |
| Alerte d’espace ou écriture échouée | Vérifiez l’usage du SR, l’espace et les quotas du serveur, les tâches et le disque exact dans l’invité. Préservez preuves et données ; ne supprimez ni disque, ni snapshot, ni fichier NAS non identifié. |

Pour le nettoyage, conservez l’inventaire final et arrêtez normalement la VM de test. Appliquez les conseils précédents sur [détachement et suppression](#3-distinguer-détachement-et-suppression) uniquement au disque de test identifié avec certitude. Conservez SR/export jusqu’à l’identification de tous les utilisateurs et besoins de récupération avec leur propriétaire. Cet exercice ne prescrit ni destruction, oubli ou rattachement de SR, ni suppression de fichiers NAS, ni changement du stockage par défaut. Le stockage local/SMB/iSCSI, les sous-répertoires NFS, pannes, performances et migration/HA dans tout le pool exigent une validation distincte.

## 7. Créer un VLAN de laboratoire sur une liaison dédiée {#host-vlan-network}

Cet exercice de **configuration d’hôte/pool** crée un réseau invité étiqueté depuis le **navigateur XOA-HL**. Utilisez un pool jetable, une interface physique de réserve dédiée et une VM jetable arrêtée. Gardez une console indépendante de l’hôte disponible. Notez le pool/master et chaque hôte prévu, les UUID réseau/PIF existants, périphériques, MAC, VLAN, MTU, indicateurs de gestion, modes IP et états de connexion avant de commencer.

Faites approuver par l’administrateur réseau l’identifiant VLAN, les ports de commutateur étiquetés, le MTU `1500`, l’adressage invité et les destinations autorisées/interdites. Vérifiez la liaison de réserve sur **chaque** hôte prévu : aucun trafic de gestion, stockage, sauvegarde ou autre charge, aucune configuration IP d’hôte, aucune agrégation ni organisation VLAN existante. Comparez avec l’inventaire des câbles et commutateurs ; un nom de périphérique ou l’absence de badge Management ne suffit pas. Arrêtez si cette topologie ne peut être établie. Un numéro VLAN ne prouve pas l’isolation et ne configure ni commutateur, routage, DHCP, DNS ou pare-feu.

### Créer le réseau une seule fois

1. Avec un compte administrateur, ouvrez **Nouveau → Network** (`/#/new/network`) et sélectionnez le **pool** jetable. L’API exige l’administration du pool. Laissez **Bonded network** et **Private network** désactivés ; Private network correspond à un autre parcours SDN.
2. Dans **Info → Interface**, choisissez explicitement la **PIF de réserve du master** enregistrée. Le sélecteur se limite aux PIF du master sans VLAN et exclut les interfaces esclaves d’agrégation ; il n’exclut **pas** celles de gestion. Revérifiez UUID/périphérique/MAC et inventaire indépendant. Ne laissez pas Interface vide : cela crée un réseau sans liaison physique, pas le VLAN demandé ici.
3. Saisissez un **Nom** distinct et une **Description** identifiant le laboratoire. Indiquez `1500` dans **MTU** et l’identifiant VLAN étiqueté exactement approuvé dans **VLAN**. Ne laissez pas VLAN vide et ne substituez pas `0` : le navigateur convertit le champ vide en valeur par défaut API `0`. Choisissez **No NBD Connection** ; ce réseau invité ne nécessite pas l’usage NBD.
4. Relisez pool, PIF du master, VLAN, MTU et les deux commutateurs de type, puis choisissez **Créer un réseau** une seule fois. Attendez la fin et la vue **Réseaux** du pool (`/#/pools/<id>/network`). En cas d’échec, conservez l’erreur et inspectez réseaux du pool et PIF de tous les hôtes avant de réessayer. Le serveur tente de nettoyer le réseau après un échec de création ; cela ne prouve pas l’annulation de toutes les modifications du pool.

### Relire chaque hôte prévu

Copiez l’UUID du nouveau réseau depuis sa ligne du pool, et notez nom, MTU et VLAN. Le résumé PIF/VLAN provient du **master** ; il ne prouve pas la configuration des autres hôtes. Développez **PIFs** pour comparer hôte, périphérique et MAC à l’inventaire. Son indicateur d’état représente le **lien physique**, tandis que le bouton **Connecté** de l’onglet Réseaux d’un hôte représente l’attachement de la PIF. Aucun ne prouve le passage du trafic étiqueté. Ne cliquez pas sur connecter/déconnecter pour lire un état.

Pour chaque hôte prévu, ouvrez **Réseaux** (`/#/hosts/<id>/network`), repérez la PIF du nouveau réseau et notez UUID, périphérique/MAC, VLAN, MTU, badge de gestion, modes/adresse IP et état. Confirmez le VLAN exact, MTU `1500`, attachement, lien physique attendu et absence d’usage IP/gestion sur l’hôte. Comparez la connectivité de gestion et de stockage à l’état initial. Si une PIF manque, est déconnectée ou inattendue, arrêtez avant d’y placer un invité ; ne modifiez pas les champs VLAN/MTU/IP existants et ne basculez pas les PIF parentes pour réparer.

### Vérifier la connectivité invitée et garder les preuves

Suivez la [procédure d’interface VM](#4-ajouter-une-interface-vm-isolée) sur une VM jetable arrêtée, en choisissant ce réseau précis. Notez UUID VM/VIF, MAC, réseau et hôte résident ; vérifiez qu’aucune interface héritée ne contourne la conception du laboratoire. Démarrez seulement sur un hôte dont la PIF a été vérifiée. L’administrateur invité configure par console l’**interface invitée non étiquetée** et des adresses uniques convenues ; cet exercice ne configure pas de trunk VLAN dans l’invité.

Vérifiez séparément adresse, sous-réseau, route et DNS. Testez un pair/service autorisé et les destinations interdites définies par l’administrateur, notamment vers la production ; un ping en échec ne prouve pas l’isolation. Notez les tests et résultats réels. Après arrêt normal et démarrage, répétez les contrôles de correspondance et de connectivité. Un pair sur le même hôte ne prouve ni la liaison physique ni un autre hôte : trafic inter-hôtes et migration nécessitent chacun un montage approuvé distinct. Vérifiez aussi le maintien de l’accès à la gestion, au stockage et à XOA-HL.

| Symptôme | Vérification et suite |
| --- | --- |
| PIF de réserve absente ou mauvais pool | Vérifiez master, périphérique physique et appartenance agrégation/VLAN. Arrêtez ; ne choisissez pas une PIF de gestion/stockage et ne changez pas de pool pour contourner le sélecteur. |
| Erreur, doublon ou inventaire PIF partiel | Conservez heures/erreur et UUID réseau/PIF exacts sur tous les hôtes. Faites le point avec le responsable avant de réessayer ; la notification ne prouve pas un retour arrière. |
| Lien physique présent mais trafic invité attendu absent | Vérifiez attachement, correspondance VIF, IP/route/DNS invités, chemin étiqueté approuvé et pair/pare-feu. Ne devinez pas une correction en modifiant IP de gestion, MTU parent ou VLAN. |
| Accès inattendu à la production ou perte de gestion/stockage | Arrêtez l’invité de test, conservez les preuves et utilisez la console indépendante avec le plan de récupération de l’administrateur réseau. Évitez d’autres modifications dans le navigateur tant que la topologie reste incertaine. |

Sauvegardez les inventaires finaux et arrêtez normalement la VM de test. Retirez uniquement la VIF de test formellement identifiée si la procédure précédente le demande. Conservez réseau/PIF et configuration du commutateur tant que le responsable n’a pas recensé tous les utilisateurs et fourni une procédure approuvée de retrait/récupération. Suppression du réseau, modifications VLAN/MTU, retrait de PIF, agrégations, migration de gestion et configuration IP de l’hôte dépassent ce pilote ; modifier le MTU d’un réseau existant peut déconnecter/reconnecter ses interfaces. Poursuivez avec [hôtes/pools](/docs/xoa-hl/hosts-pools/) et [dépannage](/docs/xoa-hl/troubleshooting/). La validation réelle de création, trafic, isolation et récupération reste à faire.

[Diagnostiquer la connectivité réseau](/docs/xoa-hl/troubleshooting/#network-connectivity).

## Sources

Version XO 5 `e281c536` : [interface des disques et sélection du SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [interface réseau VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js) et [actions disque/interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).

[assistant SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js) / [API SR et sondes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs) / [action de rescan SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js) / [attachements des hôtes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js) / [API d’import ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs) / [sélection ISO de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).

Vue de la capacité et de l’usage du SR: [XO5 `tab-general.js`](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js).

[VLAN wizard](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/network/index.js) / [Network API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/network.mjs) / [Pool VLAN creation/cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs) / [Pool network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js) / [PIF carrier view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js) / [Host network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js) / [PIF/network fields](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs) / [MTU operations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/network.mjs).
