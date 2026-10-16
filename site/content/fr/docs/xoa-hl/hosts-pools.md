---
title: Gérer les hôtes — jonction de pool, gestion et statistiques
description: Vérifier la gestion et les marqueurs XOA, lire les statistiques et répéter une jonction de deux hôtes jetables.
weight: 24
translationKey: xoa-manual-hosts-pools
translationStatus: draft
sourceRevision: sha256:4b3536b54887922d1943baba3c0bfb5c369d20209b467cc202b343e8717430e1
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Utilisez un compte administrateur dans l’**appliance XOA-HL** et un accès autorisé à la console de l’hôte. Notez l’adresse de l’appliance, les identités de l’hôte/pool et le gestionnaire actuel. Pour la première connexion, suivez [la connexion initiale et l’ajout d’un hôte](/docs/xoa-hl/first-login/).

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. La revue du bouton XO Lite couvre aussi `xolite-ce v0.21.0-ce29` (amont `xo-lite-v0.21.0`). Les tests de transfert, de marqueurs obsolètes, de statistiques hôte et de jonction de pool restent à faire.
{{< /callout >}}

## 1. Vérifier le pool connecté

Ouvrez **Paramètres → Serveurs** (`/#/settings/servers`). Vérifiez que la connexion attendue est activée et connectée, et que l’inventaire affiche l’hôte, le pool, les VM et le stockage prévus. Une entrée enregistrée ne prouve pas une connexion réussie. En cas d’échec, examinez son erreur et vérifiez l’adresse, les identifiants et le certificat avec [le guide de connexion](/docs/xoa-hl/first-login/).

La règle de gestion supportée décrite dans [#126](https://github.com/Vagrantin/xcp-hl/issues/126) est **une seule XOA pour un hôte/pool donné**. Plusieurs appliances peuvent techniquement se connecter, mais la gestion simultanée n’est pas supportée. Cette règle ne limite pas une appliance à un seul pool. Coordonnez la responsabilité avant d’ajouter une connexion ; ne laissez jamais des planifications de sauvegarde en double gérer les mêmes invités.

## 2. Transférer la gestion à une autre appliance

1. Prévoyez une fenêtre, terminez les tâches de gestion/sauvegarde et notez les connexions, planifications et destinations de l’ancien gestionnaire. [Exportez sa configuration](/docs/xoa-hl/configuration-backup/) pour la conserver ; l’export seul ne transfère ni ne désactive les tâches.
2. Désactivez ses planifications concernées. Dans **Paramètres → Serveurs**, supprimez la connexion au pool avant de connecter le nouveau gestionnaire. Ne retirez pas un hôte du pool et ne supprimez pas une VM pour transférer la gestion XO.
3. Ajoutez la connexion à l’hôte/pool sur la nouvelle appliance. Vérifiez l’inventaire connecté et les droits prévus. Recréez ou restaurez les réglages uniquement avec les précautions d’isolation et d’import du guide de configuration.
4. Confirmez que l’ancien gestionnaire ne se reconnecte plus et n’exécute plus de tâches sur le pool. N’activez que les nouvelles planifications prévues après vérification des destinations et un test de récupération isolé.

Si l’état d’une appliance est incertain, suspendez le transfert et conservez les erreurs. Cette procédure ne modifie pas l’appartenance au pool. Un pilote distinct de jonction de deux hôtes suit ; la HA et la migration à chaud restent hors de son périmètre.

## 3. Comprendre le bouton XO Lite

XO écrit `xo:clientInfo:<appliance-uuid>` dans `other-config` du pool. Par défaut, il écrit à la connexion puis toutes les **6 heures**, supprimant les marqueurs de plus de **48 heures** pendant ces passages. Une connexion XO en lecture seule n’écrit pas de marqueur. Supprimer la connexion arrête les écritures futures, sans supprimer immédiatement l’ancien marqueur.

Dans la version XO Lite étudiée, **Access XOA** utilise le marqueur au `lastConnected` le plus récent. Il préfère `publicUrl`, sinon la première adresse de `eth0` (ou de la première interface disponible), en HTTPS. Il ne vérifie pas que la VM ou le service web fonctionne. Sans adresse disponible, il propose **Deploy XOA**. XO Lite n’expire pas lui-même les anciens marqueurs ; un bouton obsolète peut donc rester si aucune XO ne se connecte.

Une adresse obsolète ne justifie pas un second gestionnaire. Vérifiez d’abord l’adresse connue et la responsabilité de gestion. Si le gestionnaire valide annonce une mauvaise adresse, examinez sa configuration URL/réseau au lieu de supprimer son marqueur à répétition.

## 4. Inspecter ou retirer un marqueur obsolète

Sur l’**hôte hyperviseur**, avec les droits root, commencez par ces commandes en lecture seule. Comparez le pool et la clé obsolète exacte à votre registre de gestion :

```bash
xe pool-list params=uuid,name-label
xe pool-param-get uuid='<pool-uuid>' param-name=other-config
```

Uniquement après avoir supprimé la connexion de l’ancienne appliance, conservez la valeur du marqueur et retirez **cette seule clé** si nécessaire. Remplacez les deux paramètres ; ne supprimez jamais toutes les métadonnées `other-config` :

```bash
xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
```

Répétez la vérification en lecture seule et rechargez XO Lite. Un ancien gestionnaire encore actif peut réécrire son marqueur à la reconnexion ou au prochain passage. Si la clé revient, recherchez la connexion restante. Ce nettoyage modifie la découverte, pas l’appartenance au pool, l’alimentation des VM ou les sauvegardes ; il n’a pas été exécuté pendant cette revue des sources.

## 5. Lire les statistiques d’un hôte {#host-statistics}

Cet exercice d’observation ne modifie aucune configuration d’hôte, de VM, de réseau ou de stockage. Utilisez un hôte connu, connecté et en fonctionnement, puis notez son ID, son pool, son nombre de CPU et sa capacité mémoire. Ouvrez son onglet **Stats** (`/#/hosts/<id>/stats`) et confirmez son identité avant de lire les graphiques. La vue d’ensemble du pool ou le moniteur du système d’exploitation de l’appliance a un périmètre différent.

1. Commencez par **Les 10 dernières minutes**, valeur initiale. Notez la plage choisie, l’heure courante, le fuseau du navigateur, l’heure du dernier échantillon affiché et les éventuelles erreurs de tâche/connexion. Attendez plusieurs intervalles attendus et vérifiez l’arrivée de données récentes. Un graphique encore affiché ne prouve pas que la collecte est à jour.
2. Comparez une plage plus longue avec le sélecteur. Le serveur étudié demande des échantillons **AVERAGE** ; un point sur une longue période peut lisser un bref pic. Revenez à la plage courte pour examiner les changements récents. Les libellés décrivent l’historique demandé, sans garantir que l’hôte a conservé toute cette période.

| Libellé de plage | Intervalle nominal d’échantillonnage / d’actualisation de l’onglet |
| --- | --- |
| Les 10 dernières minutes | 5 secondes |
| Les 2 dernières heures | 1 minute |
| Last day | 1 heure ; 24 derniers échantillons horaires |
| La dernière semaine | 1 heure |
| La dernière année | 1 jour |

**Last day** reste en anglais dans cette version. Une vue longue ne s’actualise pas nécessairement toutes les cinq secondes. Comparez les observations avec la même plage et le même intervalle ; notez les heures affichées plutôt que de traiter le dernier point comme une mesure instantanée.

3. Pour une première lecture par série, laissez **Valeurs cumulées** désactivé, puis comparez volontairement son effet si nécessaire. Relisez la légende, l’unité affichée et l’échelle verticale à chaque fois ; ce bouton ajoute des séries CPU/réseau sommées et peut changer l’échelle.

| Graphique | Interprétation et limite |
| --- | --- |
| Utilisation CPU | Les séries `Cpu` individuelles sont des pourcentages. `All Cpus` est leur somme, pas un pourcentage global normalisé : quatre CPU à 50 % donnent 200 %. Comparez le nombre de CPU et les séries individuelles avant de diagnostiquer une saturation. |
| Utilisation mémoire | Mémoire totale de l’hôte moins mémoire libre, affichée en octets. Ce n’est ni la limite mémoire configurée d’un invité ni sa RAM libre au niveau applicatif. Dans ces sources, l’absence de données de mémoire libre peut afficher une utilisation nulle ; vérifiez indépendamment un zéro inattendu. |
| Échanges réseaux | Examinez les séries numérotées `eth` en réception (`rx`) et en émission (`tx`) et rapprochez-les des interfaces de l’hôte. Les unités affichées sont des tailles en octets ; ce pilote ne valide ni la conversion vers Mbps/Gbps ni la couverture des bonds/VLAN. Une série calme ne prouve pas la santé du lien ou la connectivité des invités. |
| Charge (load) moyenne : | Métrique hôte `loadavg` distincte, pas un pourcentage CPU ou une mesure directe de capacité disque. Rapprochez-la des CPU, de la mémoire, du trafic et de la charge observée ; aucun seuil acceptable universel n’est établi ici. |

4. Notez une référence pendant une activité normale connue, puis comparez une période d’activité identifiée avec le même hôte, la même plage et les mêmes réglages. Conservez les séries concernées, les heures, l’intervalle et le symptôme réel. Ne lancez pas un stress test en production et ne redimensionnez, migrez ou redémarrez pas un invité uniquement pour faire bouger le graphique. Une charge de test en laboratoire exige sa propre autorisation opérateur.

Si un graphique affiche **No stats.**, reste en chargement, présente des trous ou demeure anormalement plat/nul, conservez l’hôte, la plage, l’heure et l’erreur. Vérifiez la connexion et l’état de fonctionnement, puis rechargez la page et choisissez à nouveau la plage courte. L’onglet étudié ne demande pas de données si l’hôte ne fonctionne pas ; une requête échouée peut laisser son état d’attente actif, et attendre ne suffit pas forcément à reprendre la collecte. Certaines données manquantes peuvent aussi devenir des zéros lors de la conversion. Ni un graphique vide ni un zéro ne prouve qu’un hôte est inactif ou sain. Si les heures n’avancent toujours pas, suivez le [dépannage](/docs/xoa-hl/troubleshooting/) et des observations indépendantes autorisées sur l’hôte avant toute décision de capacité ; réinitialiser les statistiques ou redémarrer un hôte de production n’est pas la récupération de cet exercice.

Ce pilote couvre uniquement la lecture des graphiques d’un hôte. L’exactitude des métriques installées, l’historique complet, l’alignement des horloges, les seuils/notifications, les agrégations dashboard/pool, la capacité des SR et le diagnostic de performances exigent des validations séparées. Ces graphiques seuls n’établissent pas la place pour une autre VM, un basculement HA ou une migration sûre.

## 6. Répéter la jonction d’un hôte jetable à un pool {#pool-join}

Cet **aperçu vérifié dans les sources** concerne XO 5.113.2 dans l’image `xoa-image-20261009-5f33c81`, paquet `v5.113.2_e281c536-ce38`. La jonction change l’appartenance d’un hôte et peut installer des correctifs manquants. N’utilisez que deux hôtes de laboratoire réinstallables dont la version est identifiée : la cible est le maître d’un pool à un seul hôte et la source est le seul hôte d’un autre pool. Gardez une console indépendante, un plan de récupération/réinstallation enregistré et une seule XOA-HL responsable des deux connexions. Excluez un pool de production actif, la HA, les invités en fonctionnement, les charges partagées ou attachées et les données sans sauvegarde indépendante.

1. Dans le **navigateur XOA-HL**, vérifiez sous **Paramètres → Serveurs** une connexion fonctionnelle à chacun des pools à un seul hôte. Notez les deux ID de pool, les ID du maître cible et de l’hôte source, la marque produit, la version/build et les correctifs, les adresses de gestion, l’inventaire réseau/stockage, le nombre de VM et les tâches actives. Arrêtez les planifications de sauvegarde des deux ensembles pendant la fenêtre et conservez leurs points de reprise indépendants. Un hôte autonome appartient tout de même à un pool à un seul hôte : confirmez l’absence d’autre hôte dans le pool source. Validez avec le responsable réseau/stockage la topologie de jonction sur le même réseau, la synchronisation DNS/heure, l’accès de gestion distinct et la récupération par console. Des noms de réseau ou de SR semblables ne prouvent pas un stockage partagé.
2. Sur la page du **pool cible** (`/#/pools/<target-pool-id>/general`), identifiez le maître et ouvrez **Add hosts**. Sélectionnez uniquement l’hôte source voulu. Le sélecteur écarte les hôtes appartenant à des pools de plusieurs hôtes et affiche les différences de correctifs dans les deux sens. Si l’un des comptes de correctifs diffère de zéro, si la marque/version diffère, si la HA est active, si une VM ou un SR source doit être conservé ou si la jonction reste incertaine, **annulez** et réconciliez ces conditions hors de cet exercice. N’utilisez pas ce dialogue pour installer des correctifs ou évacuer un hôte. Dans les sources, l’interface transmet `force: true`, ce qui appelle `pool.join_force` dans XAPI ; la confirmation déclenche le changement d’état et ne constitue pas un simple test de compatibilité.
3. Après l’enregistrement du contrôle préalable et pendant la fenêtre approuvée, confirmez le pool cible et l’hôte source exacts puis validez une seule fois. Après une jonction réussie, la connexion source devrait être désenregistrée et l’inventaire cible actualisé ; un affichage momentanément déconnecté est possible. Ne renvoyez pas la demande simplement parce que la tâche ou la page ne s’est pas actualisée. En cas d’échec, conservez la tâche/erreur, l’état des consoles et les deux inventaires. Le serveur peut déjà avoir appliqué des correctifs ou commencé la jonction : arrêtez-vous et suivez le plan de récupération du responsable au lieu de forcer une nouvelle fusion ou d’éjecter l’hôte.
4. Actualisez la connexion cible. Vérifiez que l’ID et le maître du pool cible sont les bons, qu’il contient exactement les deux ID d’hôtes attendus et que l’état du pool/de la connexion source est expliqué. Inspectez les réseaux/PIF, les attaches SR/PBD et l’accès de gestion de chaque hôte, puis vérifiez que le stockage de test et le réseau invité isolé sont utilisables sur les hôtes appropriés. Recherchez les VM, connexions XOA, tâches de sauvegarde ou marqueurs de gestion XO Lite inattendus. L’appartenance au pool ne prouve ni une migration sûre ni la capacité HA.

Conservez les ID avant/après, les comptes de différences de correctifs, le résultat de la tâche, l’accès aux consoles et chaque vérification réussie ou échouée. Gardez le pool joint si c’est le résultat voulu ; **Detach/eject** est un autre changement d’état, pas un retour arrière automatique. Le comportement installé de la jonction, des correctifs, du réseau et du stockage, la récupération après échec, le retrait ultérieur d’un hôte, la HA, le stockage partagé, la migration à chaud et la relecture humaine EN/FR/JA restent à valider.

## Sources

Statistiques hôte au commit XO 5 `e281c536` : [onglet et actualisation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js), [plages et intervalles](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/stats.js), [API de statistiques hôte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [moyennes RRD, métriques et cache](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs), [sommes, échelles et libellés des graphiques](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js) et [calcul mémoire et unités en octets](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/utils.js).

Version XO 5 `e281c536` : [interface des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [marquage du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs) et [intervalles par défaut](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml). Sources XO Lite : [choix de l’adresse du bouton](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [build communautaire et cibles des correctifs](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml). La règle de support et le nettoyage ciblé viennent de [#126](https://github.com/Vagrantin/xcp-hl/issues/126).

Jonction de pool à la version XO 5 `e281c536` :[action du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/action-bar.js), [sélecteur et différences de correctifs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-hosts-modal/index.js), [indicateur force dans l’interface](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [API et permissions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [contrôles version/marque et correctifs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/pool.mjs), [jonction et changement de connexion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [XAPI join_force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs).
