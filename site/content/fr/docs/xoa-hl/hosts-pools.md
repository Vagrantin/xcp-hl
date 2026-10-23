---
title: "Gérer les hôtes et les pools"
linkTitle: "Hôtes et pools"
description: "Vérifiez quelle appliance gère un pool, lisez les statistiques des hôtes, et testez la jonction de pool, le mode maintenance et la HA sur des hôtes de laboratoire."
weight: 60
translationKey: xoa-manual-hosts-pools
translationStatus: draft
sourceRevision: sha256:6ade76bbc4328f8c9c50e11f0871e5809dda89e8f6f6c2d1fda8e5c6c988f73e
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Vérifiez quelle appliance gère chaque pool, transférez la gestion à une autre appliance, nettoyez un ancien bouton XO Lite, lisez les statistiques des hôtes, et testez la jonction de pool, le mode maintenance et la haute disponibilité (HA) sur des hôtes de laboratoire. Connectez-vous à l’**appliance XOA-HL** en tant qu’administrateur, et gardez un accès autorisé à la console de l’hôte. Avant de commencer, notez l’adresse de l’appliance, les ID des hôtes et des pools, et l’appliance qui les gère aujourd’hui. Pour la première connexion, voir [la première connexion et l’ajout d’un hôte](/docs/xoa-hl/first-login/).

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. La partie sur le bouton XO Lite couvre aussi `xolite-ce v0.21.0-ce29` (amont `xo-lite-v0.21.0`).
{{< /callout >}}

## Vérifier la connexion et l’appliance responsable du pool {#connected-pool}

1. Ouvrez **Paramètres → Serveurs** (`/#/settings/servers`).
2. Vérifiez que la connexion attendue est activée et connectée.
3. Vérifiez que l’inventaire affiche l’hôte, le pool, les VM et le stockage prévus.

Une entrée de serveur enregistrée ne prouve pas que la connexion fonctionne. Si la connexion échoue, lisez son erreur, puis vérifiez l’adresse, les identifiants et la gestion du certificat avec le [guide de connexion](/docs/xoa-hl/first-login/).

La règle prise en charge, notée dans le [ticket #126](https://github.com/Vagrantin/xcp-hl/issues/126), est la suivante : **une seule XOA gère un hôte ou un pool donné**. Plusieurs appliances peuvent techniquement se connecter, mais gérer le même pool depuis plusieurs appliances n’est pas pris en charge. Une appliance peut tout de même gérer plusieurs pools. Convenez de l’appliance responsable d’un pool avant d’ajouter une connexion. Ne laissez jamais des planifications de sauvegarde en double tourner pour les mêmes invités.

## Transférer la gestion à une autre appliance {#move-management}

Cette procédure transfère la responsabilité d’un pool d’une ancienne appliance à une nouvelle. Elle ne modifie pas l’appartenance au pool. Ne retirez jamais un hôte de son pool et ne supprimez jamais une VM pour transférer la gestion XO.

1. Prévoyez un créneau. Laissez se terminer les tâches de gestion et de sauvegarde en cours.
2. Sur l’ancienne appliance, notez ses connexions, ses planifications et ses destinations de sauvegarde.
3. [Exportez sa configuration](/docs/xoa-hl/configuration-backup/) et conservez le fichier en lieu sûr. L’export seul ne transfère ni ne désactive aucune tâche.
4. Sur l’ancienne appliance, désactivez les planifications qui concernent ce pool.
5. Dans **Paramètres → Serveurs** de l’ancienne appliance, supprimez la connexion au pool. Faites-le avant de connecter la nouvelle appliance.
6. Sur la nouvelle appliance, ajoutez la connexion à l’hôte ou au pool. Vérifiez l’inventaire connecté et les droits prévus.
7. Si vous recréez ou restaurez des réglages, suivez les précautions d’isolation et d’import du [guide de sauvegarde de la configuration](/docs/xoa-hl/configuration-backup/).
8. Vérifiez que l’ancienne appliance ne se reconnecte plus et n’exécute plus de tâches sur le pool.
9. Sur la nouvelle appliance, vérifiez les destinations de sauvegarde et faites un test de restauration isolé. Activez ensuite uniquement les planifications prévues.

**Vérification :** seule la nouvelle appliance est connectée au pool et exécute ses tâches.

Si l’état de l’une des appliances est incertain, suspendez le transfert et conservez les erreurs de connexion et de tâche. Pour regrouper des hôtes dans un même pool, voir [Tester la jonction de deux hôtes](#pool-join).

## Comprendre le bouton XO Lite {#xo-lite-button}

Chaque appliance connectée laisse un marqueur sur le pool. XO Lite lit ces marqueurs pour construire son bouton **Access XOA**.

- XO écrit la clé `xo:clientInfo:<appliance-uuid>` dans `other-config` du pool. Avec les réglages par défaut, il l’écrit à la connexion, puis toutes les **6 heures**. À chacun de ces passages, il supprime aussi les marqueurs de plus de **48 heures**.
- Une connexion XO en lecture seule n’écrit pas de marqueur.
- Supprimer une connexion de serveur arrête les nouvelles écritures, mais ne supprime pas tout de suite le marqueur existant.
- **Access XOA** utilise le marqueur dont la valeur `lastConnected` est la plus récente. Il ouvre `publicUrl` si elle est définie, sinon la première adresse de `eth0` (ou de la première interface disponible), en HTTPS.
- Le bouton ne vérifie pas que la VM de l’appliance ou son service web fonctionne. Si XO Lite ne trouve aucune adresse, il propose **Deploy XOA** à la place.
- XO Lite ne fait pas expirer lui-même les anciens marqueurs. Un ancien bouton peut rester alors qu’aucune XO ne se connecte plus.

Une ancienne adresse ne justifie pas le déploiement d’une seconde appliance. Vérifiez d’abord l’adresse connue de l’appliance et celle qui gère le pool. Si la bonne appliance annonce une mauvaise adresse, vérifiez sa configuration d’URL et de réseau au lieu de supprimer son marqueur encore et encore.

## Retirer un marqueur XO Lite obsolète {#obsolete-marker}

Faites-le uniquement après avoir supprimé la connexion de l’ancienne appliance (voir [Transférer la gestion à une autre appliance](#move-management)). Cela ne modifie que les données de découverte : ni l’appartenance au pool, ni l’alimentation des VM, ni les sauvegardes.

1. Sur l’**hôte hyperviseur**, en tant que root, lancez ces commandes en lecture seule :

   ```bash
   xe pool-list params=uuid,name-label
   xe pool-param-get uuid='<pool-uuid>' param-name=other-config
   ```

2. Comparez le pool et la clé obsolète exacte avec vos relevés de l’appliance qui gère le pool.
3. Notez la valeur de ce marqueur.
4. Seulement si nécessaire, retirez **cette seule clé**. Remplacez les deux paramètres. Ne supprimez jamais tout `other-config` :

   ```bash
   xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
   ```

5. Relancez les commandes en lecture seule, puis rechargez XO Lite.

**Vérification :** la clé n’apparaît plus. Si elle revient, une ancienne appliance est encore connectée : elle réécrit son marqueur à la reconnexion ou à son prochain passage. Trouvez cette connexion restante.

## Lire les statistiques des hôtes {#host-statistics}

Lire les statistiques ne modifie rien sur l’hôte, ses VM, ses réseaux ou son stockage.

**Avant de commencer**

- Choisissez un hôte connu, connecté et en fonctionnement. Notez son ID, son pool, son nombre de CPU et sa taille de mémoire.
- Cet onglet ne montre qu’un seul hôte. La vue d’ensemble du pool et le moniteur système de l’appliance montrent autre chose.

1. Ouvrez l’onglet **Stats** de l’hôte (`/#/hosts/<id>/stats`). Vérifiez qu’il s’agit du bon hôte avant de lire un graphique.
2. Commencez par **Les 10 dernières minutes**, la plage par défaut. Notez la plage, l’heure actuelle, le fuseau horaire du navigateur, l’heure du dernier échantillon affiché et toute erreur de tâche ou de connexion.
3. Attendez plusieurs intervalles d’échantillonnage et vérifiez que de nouvelles données arrivent. Un graphique encore affiché ne prouve pas que la collecte est à jour.
4. Choisissez une plage plus longue pour comparer. XO demande des échantillons **AVERAGE** : un point sur une longue plage peut lisser un pic bref. Revenez à la plage courte pour examiner les changements récents.
5. Laissez l’interrupteur **Valeurs cumulées** désactivé pour une première lecture de chaque série. Activez-le seulement pour comparer : il ajoute des séries CPU et réseau sommées et peut changer l’échelle. Relisez la légende, l’unité et l’échelle verticale à chaque fois.
6. Notez une référence pendant une activité normale connue. Comparez ensuite une période chargée connue avec le même hôte, la même plage et les mêmes réglages. Notez les séries, les heures, l’intervalle entre échantillons et le symptôme réel.

Ne lancez pas de test de charge en production, et ne redimensionnez, ne migrez ni ne redémarrez un invité juste pour faire bouger un graphique. Une charge sur un système de laboratoire demande sa propre autorisation de l’opérateur.

| Plage | Intervalle prévu d’échantillonnage et d’actualisation |
| --- | --- |
| Les 10 dernières minutes | 5 secondes |
| Les 2 dernières heures | 1 minute |
| Last day | 1 heure ; les 24 derniers échantillons horaires |
| La dernière semaine | 1 heure |
| La dernière année | 1 jour |

Le nom d’une plage indique l’historique demandé par XO, pas que l’hôte a conservé tout cet historique. Les longues plages ne s’actualisent pas toutes les cinq secondes. Comparez des relevés qui utilisent la même plage et le même intervalle. Notez les heures affichées : le dernier point n’est pas une mesure instantanée.

| Graphique | Comment le lire |
| --- | --- |
| Utilisation CPU | Chaque série `Cpu` est un pourcentage. `All Cpus` est leur somme, pas un pourcentage de l’hôte : quatre CPU à 50 % font 200 %. Vérifiez le nombre de CPU et chaque série avant de conclure que l’hôte est saturé. |
| Utilisation mémoire | Mémoire totale de l’hôte moins mémoire libre, affichée en octets. Ce n’est ni la limite mémoire d’un invité ni la RAM libre vue par une application. Si les données de mémoire libre manquent, la mémoire utilisée peut s’afficher à zéro : vérifiez un zéro inattendu par un autre moyen. |
| Échanges réseaux | Séries `eth` numérotées en réception (`rx`) et en émission (`tx`). Rapprochez-les des interfaces de l’hôte. Les valeurs sont des tailles en octets. La conversion en Mbps ou Gbps, les agrégations et les VLAN ne sont pas traités ici. Une série calme ne prouve pas que le lien ou la connectivité des invités est sain. |
| Charge (load) moyenne : | La métrique `loadavg` distincte de l’hôte. Ce n’est ni un pourcentage CPU ni une mesure de capacité disque. Comparez-la avec le CPU, la mémoire, le trafic et la charge réelle. Aucun seuil sûr général n’est fixé ici. |

**Vérification :** sur la plage courte, l’heure du dernier échantillon continue d’avancer.

| Problème | À vérifier |
| --- | --- |
| **No stats.**, chargement sans fin, trous, ou ligne plate ou à zéro | Notez l’hôte, la plage, l’heure et l’erreur. Vérifiez la connexion et que l’hôte fonctionne. Rechargez la page et choisissez de nouveau la plage courte. L’onglet ne demande pas de données pour un hôte arrêté. Après une requête échouée, attendre ne suffit pas toujours à relancer la collecte. Certains échantillons manquants deviennent des zéros. Un graphique vide ou un zéro ne prouve pas que l’hôte est inactif ou sain. |
| Les heures des échantillons n’avancent toujours pas | Utilisez le [dépannage](/docs/xoa-hl/troubleshooting/) et des vérifications autorisées sur l’hôte lui-même avant toute décision de capacité. Ne réinitialisez pas les statistiques et ne redémarrez pas un hôte de production pour réparer les graphiques. |

Les graphiques seuls ne montrent pas la place pour une autre VM, un basculement HA ou une migration sûre. L’exactitude des métriques, l’historique complet, l’alignement des horloges, les alertes, les totaux du tableau de bord et du pool, la capacité des SR et le diagnostic de performances ne sont pas traités ici.

## Tester la jonction de deux hôtes de laboratoire {#pool-join}

La jonction déplace un hôte dans un autre pool. Elle **modifie l’appartenance de l’hôte** et peut installer des correctifs manquants. Entraînez-vous uniquement sur deux hôtes de laboratoire que vous pouvez réinstaller.

**Avant de commencer**

- Utilisez deux hôtes de laboratoire de version connue. La cible est le maître d’un pool qui ne contient que cet hôte. La source est le seul hôte d’un autre pool. Un hôte autonome forme un pool à un seul hôte.
- Gardez un accès console séparé aux deux hôtes, un plan écrit de récupération et de réinstallation, et une seule appliance XOA-HL qui gère les deux connexions.
- N’utilisez pas un pool de production, un pool avec HA, des invités en fonctionnement, des charges partagées ou attachées, ni un hôte dont les données n’ont pas de sauvegarde indépendante.
- Avec les responsables du réseau et du stockage, convenez de la topologie de jonction sur le même réseau, de la synchronisation DNS et horaire, d’un accès de gestion séparé et de la récupération par la console de l’hôte. Un réseau ou un SR au nom semblable sur chaque hôte n’est pas forcément partagé.

1. Dans le **navigateur XOA-HL**, ouvrez **Paramètres → Serveurs**. Vérifiez que chacun des deux pools a une connexion qui fonctionne.
2. Notez les deux ID de pool, les ID du maître cible et de l’hôte source, leur marque de produit, leur version, leur build et leur niveau de correctifs, les adresses de gestion, l’inventaire réseau et stockage, le nombre de VM et les tâches en cours. Vérifiez que le pool source ne contient aucun autre hôte.
3. Arrêtez les planifications de sauvegarde des deux pools pendant le créneau. Conservez leurs points de restauration indépendants.
4. Ouvrez la page du **pool cible** (`/#/pools/<target-pool-id>/general`), repérez le maître et sélectionnez **Add hosts**.
5. Sélectionnez uniquement l’hôte source prévu. La liste masque les hôtes qui appartiennent à un pool de plusieurs hôtes. Elle affiche les différences de correctifs dans les deux sens.
6. Sélectionnez **Annuler**, et réglez la cause en dehors de ce test, si l’un des nombres de correctifs n’est pas zéro, si la marque ou la version diffère, si la HA est active, si une VM ou un SR de la source doit être conservé, ou si le chemin de jonction n’est pas clair. N’utilisez pas ce dialogue pour installer des correctifs ou pour évacuer un hôte.
7. Pendant le créneau approuvé, vérifiez le pool cible et l’hôte source exacts dans le dialogue, puis sélectionnez **OK** une seule fois. L’interface envoie `force: true`, ce qui appelle `pool.join_force` dans XAPI. Cette confirmation modifie les pools : ce n’est pas un simple test de compatibilité.
8. Attendez la fin de la tâche. Après une jonction réussie, la connexion source devrait disparaître et la connexion cible devrait actualiser son inventaire. La vue peut apparaître déconnectée un instant. Ne renvoyez pas la demande juste parce qu’une tâche ou une page ne s’est pas actualisée.
9. Actualisez la connexion cible. Vérifiez que l’ID et le maître du pool cible n’ont pas changé, que le pool contient exactement les deux ID d’hôtes attendus, et que vous pouvez expliquer l’état de l’ancien pool source et de sa connexion.
10. Sur chaque hôte, vérifiez les réseaux et les PIF, les attachements de SR (PBD) et l’accès de gestion. Vérifiez que le stockage de test et le réseau invité isolé fonctionnent depuis les bons hôtes. Recherchez les VM, connexions XOA en double, tâches de sauvegarde ou marqueurs XO Lite inattendus.

**Vérification :** le pool cible garde son maître et contient exactement les deux hôtes attendus, et les deux hôtes restent joignables depuis leur console.

Notez les ID avant et après, les nombres de différences de correctifs, le résultat de la tâche, l’accès aux consoles et le résultat de chaque vérification. Gardez le pool de laboratoire joint si c’est le résultat voulu. **Détacher** éjecte un hôte de son pool : c’est un changement distinct, pas un retour arrière automatique. Être dans le même pool ne prouve pas que la migration ou la HA est sûre.

**Si la jonction échoue**, conservez la tâche et l’erreur, l’état des consoles et les deux inventaires. Le serveur a peut-être déjà appliqué des correctifs ou effectué une partie de la jonction. Arrêtez-vous et suivez le plan de récupération du responsable de l’hôte. Ne forcez pas une nouvelle fusion et n’éjectez pas d’hôte. Le retrait ultérieur d’un hôte, la HA, le stockage partagé et la migration à chaud ne sont pas traités ici.

## Tester la maintenance d’hôte sur un pool de laboratoire {#host-maintenance-mode}

Le mode maintenance désactive un hôte et déplace ses VM en fonctionnement vers d’autres hôtes du pool. Entraînez-vous uniquement sur un pool de laboratoire que vous pouvez réinstaller. Ce test n’installe pas de correctifs, ne redémarre pas d’hôte et ne vérifie pas la disponibilité pendant une mise à jour. Pour les mises à jour, voir le [guide de mise à jour de l’hôte](/docs/guides/updates/#mettre-à-jour-xcp-hl-lhôte).

**Avant de commencer**

- Utilisez un **pool de laboratoire à deux hôtes** de version connue, dont le réseau et le stockage partagé ont déjà réussi leurs propres tests. N’utilisez pas de charge de production, ni un pool récemment joint que vous n’avez pas vérifié.
- L’hôte que vous mettez en maintenance **n’est pas le maître**.
- Gardez un accès console et un accès de gestion séparés aux deux hôtes, une seule appliance XOA-HL qui gère le pool, et un plan approuvé de récupération et de réinstallation.
- Utilisez une VM de test avec un point de restauration indépendant et vérifié. Ce doit être la **seule** VM ordinaire sur l’hôte source. Son stockage et son réseau invité doivent être disponibles sur l’autre hôte.
- La [migration au sein du pool](/docs/xoa-hl/vm-transfer/) doit déjà fonctionner pour cette VM. Si vous ne l’avez pas testée, faites ce test d’abord, puis notez de nouveau l’état de l’hôte source. Arrêtez-vous si un prérequis ou le réseau de migration n’est pas clair.

1. Dans **XOA-HL**, notez les ID du pool, du maître et des deux hôtes, leurs versions et niveaux de correctifs, leurs états activé et d’alimentation, les adresses de gestion, l’hôte où tourne chaque VM, les attachements de SR (PBD), les réseaux et les PIF, la capacité libre de la cible et les tâches en cours.
2. Terminez ou suspendez les tâches de sauvegarde et de restauration.
3. Dans une session invitée autorisée, notez le comportement actuel de l’application et du réseau de la VM de test. C’est votre référence.
4. Ouvrez l’onglet **Avancé** de l’hôte source (`/#/hosts/<source-host-id>/advanced`). Vérifiez que l’hôte et le pool exacts sont affichés.
5. Sélectionnez **Enable maintenance mode**. Le dialogue **Maintenance mode** indique que toutes les VM en fonctionnement migreront vers d’autres hôtes du pool. Pendant le créneau approuvé, sélectionnez **OK** une seule fois. XO appelle `host.setMaintenanceMode`, puis XAPI désactive l’hôte et appelle `host.evacuate`.
6. Si un dialogue **Bypass blocked migrations** apparaît, annulez-le : cette voie retire les blocages de migration des VM.
7. Attendez le résultat de la tâche, puis actualisez les listes des hôtes et des VM.
8. Vérifiez que l’hôte source est désactivé, que la VM de test tourne sur la cible prévue, qu’aucune VM ordinaire ne tourne encore sur la source, et que l’application et le réseau correspondent à votre référence. Notez la tâche, toute erreur et l’accès aux consoles.
9. Dans l’onglet **Avancé** du même hôte, sélectionnez **Disable maintenance mode**. XO appelle `host.enable`.
10. Vérifiez que l’hôte est activé, que les deux chemins de gestion et les attachements de SR et de réseau sont sains, et que la VM est toujours sur la cible.

**Vérification :** l’hôte est de nouveau activé et la VM de test tourne toujours sur la cible. Quitter le mode maintenance ne ramène **pas** la VM. Gardez-la sur la cible, ou prévoyez une migration distincte et testée.

N’utilisez pas le bouton **Désactiver** de l’hôte, un redémarrage forcé, un arrêt d’urgence ou un bouton de correctifs à la place du mode maintenance. Ne réactivez les planifications de sauvegarde qu’après avoir vérifié leur périmètre et un point de restauration isolé. Conservez les ID avant et après, les heures, les vérifications de l’invité, la sortie de la tâche, l’état réel de l’hôte et l’hôte où tourne chaque VM. Une activation réussie du mode maintenance, ou la seule appartenance au pool, ne prouve pas que le pool est prêt pour les correctifs ou la HA.

**Si l’évacuation échoue**, arrêtez-vous : certaines VM ont peut-être déjà été déplacées. Après une erreur d’évacuation, XO réactive normalement l’hôte, mais un échec avant cette étape peut le laisser désactivé. Lisez l’état activé réel et l’hôte où tourne chaque VM, puis suivez le plan de récupération du responsable de l’hôte. Ne relancez pas le mode maintenance, ne contournez pas un blocage et ne redémarrez pas l’hôte pour lever un état incertain.

## Vérifier la préparation à la HA sur un pool de laboratoire {#ha-readiness}

Quand la haute disponibilité (HA) est active, elle peut isoler (fencing) et redémarrer un hôte si la communication par signal de présence (heartbeat) échoue. Testez-la uniquement sur un pool de laboratoire que vous pouvez réinstaller. Aucun hôte n’est mis en panne volontairement ici, et aucun redémarrage de VM n’est mesuré. Avant d’affirmer une quelconque disponibilité, faites un test de panne distinct et approuvé avec une VM de test protégée.

**Avant de commencer**

- Utilisez un **pool de laboratoire à trois hôtes** de version connue, que vous pouvez réinstaller et qui a réussi ses propres vérifications. N’y placez pas de charges ordinaires.
- Gérez le pool depuis une seule appliance XOA-HL qui tourne **en dehors** du pool. Gardez l’appliance et son chemin d’accès en dehors du domaine de panne.
- Gardez un accès console et un accès à l’alimentation séparés pour chaque hôte, et un plan de récupération approuvé.
- Lisez le [guide de planification HA de XCP-ng](https://docs.xcp-ng.org/management/ha/). Il recommande trois hôtes et décrit les prérequis de signal de présence réseau et stockage, de capacité et d’isolation. Vérifiez-les pour la version réelle des hôtes XCP-HL.
- Une jonction de deux hôtes, une migration réussie ou un SR portant le même nom ne prouvent pas que le pool est prêt pour la HA.

1. Dans **XOA-HL**, notez les ID exacts du pool, du maître et des trois hôtes, les versions des hôtes, les adresses de gestion et les IP de gestion statiques, l’état HA actuel, les VM, les tâches en cours et la seule appliance XOA-HL qui gère le pool.
2. Demandez aux responsables du stockage et du réseau de confirmer un SR de signal de présence partagé et accessible en écriture, attaché et joignable sur les trois hôtes. Ils confirment aussi des chemins de gestion et de stockage sains et redondants, et une capacité suffisante pour les invités protégés après la perte d’un hôte.
3. Notez l’ID du SR et ses attachements (PBD), pas seulement son nom. Si un prérequis ou un accès console n’est pas clair, arrêtez-vous ici : jusqu’ici, vous n’avez fait que lire.
4. Ouvrez l’onglet **Avancé** du pool (`/#/pools/<pool-id>/advanced`). Regardez **Heartbeat SR** et **Haute Disponibilité**.
5. Activez l’interrupteur **Haute Disponibilité** pour ouvrir le dialogue **Enabling high availability**. Il liste les SR partagés et accessibles en écriture de ce pool. Comparez le SR candidat avec votre relevé de stockage. Un SR listé ne prouve ni les attachements des hôtes, ni la fiabilité du signal, ni la capacité de basculement.
6. Sélectionnez **Annuler** si le relevé ou le plan de récupération est incomplet. Ne choisissez jamais un SR juste parce que la liste l’affiche.
7. Uniquement pendant un créneau de laboratoire approuvé, avec tous les prérequis remplis : rouvrez le dialogue, sélectionnez le SR noté et sélectionnez **OK** une seule fois. XO appelle `pool.enableHa`, qui appelle `pool.enable_ha` dans XAPI. Notez la tâche et toute erreur.
8. Actualisez le pool. Vérifiez que **Haute Disponibilité** est actif, que le SR attendu figure sous **Heartbeat SR**, que les trois hôtes sont joignables, et qu’aucune VM ou tâche inattendue n’est apparue.
9. Le pool étant sain et vos notes enregistrées, désactivez **Haute Disponibilité**. Dans le dialogue **Disabling high availability**, sélectionnez **OK** une seule fois. XO appelle `pool.disable_ha` dans XAPI.
10. Vérifiez que la HA est inactive, que tous les hôtes et chemins de SR sont sains, et que tout travail suivant a sa propre autorisation.

**Vérification :** la HA a été activée puis désactivée une fois chacune, avec le SR de signal de présence attendu, et les trois hôtes sont restés joignables.

Tant que la HA est active, les boutons de correctifs des hôtes et du pool sont bloqués. Ne lancez ni mise à jour ni redémarrage pendant ce test. Conservez les ID avant et après du pool, des hôtes et des SR, les attachements, les hypothèses de capacité, la sortie des tâches, l’accès aux consoles et l’état HA.

**Si l’activation échoue ou si un hôte est isolé**, conservez les journaux des consoles, des tâches et de la HA, et suivez le plan de récupération du responsable. Si le pool est dégradé, arrêtez-vous et suivez la procédure d’incident du responsable : l’interrupteur HA n’est pas une commande de récupération universelle. Ne répétez pas l’activation ou la désactivation de la HA, ne redémarrez pas le toolstack d’un hôte et ne provoquez pas de panne réseau ou stockage pour lever un état incertain.

{{< details title="Sources" closed="true" >}}
- **Statistiques des hôtes** : [onglet Stats de l’hôte et actualisation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js), [sélecteur de plage et intervalles d’échantillonnage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/stats.js), [API de statistiques hôte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [moyennes RRD, métriques et cache](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs), [sommes, échelles et libellés des graphiques](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js), [calcul mémoire et unités en octets](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/utils.js).
- **Connexions aux serveurs et bouton XO Lite** : [interface des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [marquage du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [intervalles par défaut](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [choix de l’adresse du bouton XO Lite](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [build de XO Lite CE et cibles des correctifs](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml), [règle de prise en charge et nettoyage des marqueurs (ticket #126)](https://github.com/Vagrantin/xcp-hl/issues/126).
- **Jonction de pool** : [action du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/action-bar.js), [sélecteur d’hôtes et différences de correctifs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-hosts-modal/index.js), [indicateur force dans l’interface web](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [API de fusion et permissions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [contrôles de version et de marque, correctifs et fusion séquentielle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/pool.mjs), [jonction et changement de connexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [XAPI join_force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs).
- **Maintenance d’hôte** : [onglet Avancé et boutons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-advanced.js), [confirmation et migrations bloquées](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [API de maintenance](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [désactivation, évacuation, erreurs et réactivation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [texte de confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Haute disponibilité** : [onglet Avancé du pool, liste des SR de signal et état](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-advanced.js), [API et permissions du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [appels XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [guide de planification HA de XCP-ng](https://docs.xcp-ng.org/management/ha/).
{{< /details >}}
