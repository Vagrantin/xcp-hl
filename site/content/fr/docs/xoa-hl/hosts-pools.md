---
title: Gérer les hôtes et les pools
description: Vérifier les connexions, transférer la gestion et inspecter les anciens marqueurs XOA.
weight: 24
translationKey: xoa-manual-hosts-pools
translationStatus: draft
sourceRevision: sha256:a6577ca820beb79ac98cf82c2920df54641b60291785bb165ecbad082dfa96de
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Utilisez un compte administrateur dans l’**appliance XOA-HL** et un accès autorisé à la console de l’hôte. Notez l’adresse de l’appliance, les identités de l’hôte/pool et le gestionnaire actuel. Pour la première connexion, suivez [la connexion initiale et l’ajout d’un hôte](/docs/xoa-hl/first-login/).

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. La revue du bouton XO Lite couvre aussi `xolite-ce v0.21.0-ce29` (amont `xo-lite-v0.21.0`). Les tests de transfert et de marqueurs obsolètes restent à faire.
{{< /callout >}}

## 1. Vérifier le pool connecté

Ouvrez **Settings → Servers** (`/#/settings/servers`). Vérifiez que la connexion attendue est activée et connectée, et que l’inventaire affiche l’hôte, le pool, les VM et le stockage prévus. Une entrée enregistrée ne prouve pas une connexion réussie. En cas d’échec, examinez son erreur et vérifiez l’adresse, les identifiants et le certificat avec [le guide de connexion](/docs/xoa-hl/first-login/).

La règle de gestion supportée décrite dans [#126](https://github.com/Vagrantin/xcp-hl/issues/126) est **une seule XOA pour un hôte/pool donné**. Plusieurs appliances peuvent techniquement se connecter, mais la gestion simultanée n’est pas supportée. Cette règle ne limite pas une appliance à un seul pool. Coordonnez la responsabilité avant d’ajouter une connexion ; ne laissez jamais des planifications de sauvegarde en double gérer les mêmes invités.

## 2. Transférer la gestion à une autre appliance

1. Prévoyez une fenêtre, terminez les tâches de gestion/sauvegarde et notez les connexions, planifications et destinations de l’ancien gestionnaire. [Exportez sa configuration](/docs/xoa-hl/configuration-backup/) pour la conserver ; l’export seul ne transfère ni ne désactive les tâches.
2. Désactivez ses planifications concernées. Dans **Settings → Servers**, supprimez la connexion au pool avant de connecter le nouveau gestionnaire. Ne retirez pas un hôte du pool et ne supprimez pas une VM pour transférer la gestion XO.
3. Ajoutez la connexion à l’hôte/pool sur la nouvelle appliance. Vérifiez l’inventaire connecté et les droits prévus. Recréez ou restaurez les réglages uniquement avec les précautions d’isolation et d’import du guide de configuration.
4. Confirmez que l’ancien gestionnaire ne se reconnecte plus et n’exécute plus de tâches sur le pool. N’activez que les nouvelles planifications prévues après vérification des destinations et un test de récupération isolé.

Si l’état d’une appliance est incertain, suspendez le transfert et conservez les erreurs. La création de pools multi-hôtes, la HA et la migration à chaud dépassent ce pilote ; cette procédure ne modifie pas l’appartenance au pool.

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

## Sources

Version XO 5 `e281c536` : [interface des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [marquage du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs) et [intervalles par défaut](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml). Sources XO Lite : [choix de l’adresse du bouton](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [build communautaire et cibles des correctifs](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml). La règle de support et le nettoyage ciblé viennent de [#126](https://github.com/Vagrantin/xcp-hl/issues/126).
