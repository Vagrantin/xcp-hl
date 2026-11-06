---
title: "Créer et utiliser un modèle de VM"
linkTitle: "Modèles de VM"
description: "Transformez une copie de VM préparée en modèle, puis créez de nouvelles VM à partir de ce modèle."
weight: 42
translationKey: xoa-manual-templates
translationStatus: reviewed
sourceRevision: sha256:48760dd766f7ce1cb3d4371b2cb0ae8102b3992799119e1e08fae97a6f20d2f1
glossaryTerms: ["backup", "pool", "sr", "vm"]
---

Transformez une copie arrêtée d’une VM en modèle, puis créez deux VM à partir de ce modèle et vérifiez que chacune reçoit ses propres disques et données. La VM d’origine reste inchangée.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Ces étapes réutilisent un disque installé : elles ne préparent pas un système d’exploitation invité à une réutilisation large.
{{< /callout >}}

## Avant de commencer {#before-you-begin}

- Connectez-vous à l’**appliance XOA-HL** en tant qu’administrateur. Convertir une VM demande les droits d’administrateur sur la VM et sur son pool ; un accès à la seule VM ne suffit pas.
- Utilisez un invité de test déjà installé, avec des disques ordinaires : ni disque partagé, ni périphérique en passthrough. Ne convertissez jamais l’appliance ni la VM d’origine.
- Créez une copie de travail distincte avec [Faire une copie complète dans le même pool](/docs/xoa-hl/vm-operations/#full-copy). Notez les UUID de l’original et de la copie, l’ID de VDI, le SR et la taille de chaque disque, et la somme de contrôle d’un fichier témoin sans importance dans l’invité. Vérifiez que la copie démarre de façon isolée, puis arrêtez-la normalement.
- Sur la copie de travail, supprimez **toutes** les interfaces réseau, éjectez l’ISO d’installation, désactivez l’allumage automatique, et tenez-la à l’écart des tâches planifiées.
- Gardez assez de mémoire sur l’hôte et d’espace en écriture sur le SR pour le modèle et deux VM de test.
- Prévoyez un accès console et les identifiants de l’invité. Renommer une VM ou changer son adresse MAC ne change pas les mots de passe, le nom d’hôte, les réglages IP, les clés ni les identités applicatives copiés. Utilisez ces copies uniquement par la console.

Vous travaillez dans le navigateur, à l’adresse de l’appliance. Les vérifications du fichier et de sa somme se font dans la **console de l’invité**, pas sur l’hôte ni sur l’appliance. Un modèle sur la même infrastructure n’est pas une sauvegarde : conservez vos [sauvegardes](/docs/xoa-hl/backup-restore/) à part. Pour un invité Ubuntu 24.04 tout juste installé, [installez les outils invités](/docs/xoa-hl/guest-tools/) avant de faire la copie.

## Convertir la copie arrêtée en modèle {#convert-template}

1. Vérifiez la copie de travail : son UUID, l’état **stoppé**, une liste d’interfaces réseau vide et les disques notés.
2. Donnez-lui un nom unique, comme `lab-template-v1`, et une description avec le système invité et sa version, la date de préparation et la somme témoin. Actualisez et vérifiez ces valeurs.
3. Ouvrez son onglet **Avancé** (`/#/vms/<copy-uuid>/advanced`) et choisissez **Convert to template**. Le bouton ne fonctionne que si la VM est arrêtée. La confirmation avertit que la modification est définitive : annulez si ce n’est pas la copie prévue.
4. Confirmez une seule fois et attendez la fin.
5. Ouvrez **Accueil** et choisissez le type d’objet **Template** (`/#/home?t=VM-template`). Effacez les filtres si besoin, développez la ligne et lisez l’UUID complet.

**Vérification :** le modèle a le **même UUID** que la copie de travail, avec le nom et la description choisis, et la VM d’origine existe toujours. La conversion ne copie pas la VM : c’est la copie elle-même qui devient le modèle.

Avant de marquer la VM comme modèle, XO tente d’éjecter les médias amovibles. Si cela échoue, des modifications de médias antérieures peuvent rester alors que la conversion a échoué. Actualisez le type d’objet, les médias et la tâche avant de réessayer. Retransformer un modèle en VM, et le retour arrière automatique, ne sont pas traités ici.

## Créer une VM arrêtée à partir du modèle {#deploy-template}

1. Ouvrez **Nouveau → VM** (`/#/vms/new`), choisissez le même pool et sélectionnez votre modèle. Nommez la VM `lab-template-test-1`. Vérifiez l’UUID `template=` dans l’adresse de la page, pas seulement le nom du modèle.
2. Vérifiez le CPU, la mémoire, les disques du modèle, leurs tailles et leurs SR de destination accessibles en écriture. Gardez les mêmes disques et les mêmes tailles.
3. Dans **Paramètres d'installation**, choisissez **No config drive**. Ce test réutilise le disque installé : il ne lance aucun installateur et ne compte pas sur cloud-init pour changer l’identité de l’invité. Si les disques ou cette option manquent, arrêtez-vous et vérifiez le modèle choisi.
4. Dans **Interfaces**, supprimez chaque interface proposée et vérifiez que la liste est vide. Même un modèle sans interface peut recevoir les réseaux par défaut du pool depuis l’assistant.
5. Dans **Avancé**, décochez **Démarrer la VM après sa création** et laissez l’allumage automatique désactivé.
6. Dans **Récapitulatif**, décochez **Clonage rapide**. Vérifiez que vous créez une seule VM, avec les disques, les ressources et les SR attendus, et **zéro interface**. Sélectionnez ensuite **Créer** une seule fois. L’assistant active par défaut le démarrage après création et le clonage rapide : ne vous fiez pas à des réglages précédents. Sans clonage rapide, XO fait une copie complète des disques, ce qui demande de l’espace sur le SR.
7. Attendez, actualisez et notez l’UUID de la nouvelle VM.

**Vérification :** avant tout démarrage, la nouvelle VM est **stoppée**, son onglet Réseaux est vide, et ses disques ont le nombre, les tailles et les SR attendus, avec des ID de VDI différents de ceux du modèle et de l’original. Le modèle et l’original existent toujours. Un message de réussite ou un nouveau nom ne le prouve pas. Si une interface est apparue ou si la VM a démarré, arrêtez-la et vérifiez ce qu’elle a pu atteindre avant de continuer.

## Vérifier que chaque VM reçoit sa propre copie {#verify-deployments}

1. Après les vérifications ci-dessus, démarrez uniquement `lab-template-test-1`. Dans sa [console](/docs/xoa-hl/vm-operations/#vm-console), vérifiez que l’invité démarre et que vous pouvez vous connecter, puis vérifiez la disposition des disques et la somme témoin.
2. Modifiez uniquement le fichier témoin avec une nouvelle valeur de test, notez-la, puis arrêtez l’invité normalement.
3. Refaites [Créer une VM arrêtée à partir du modèle](#deploy-template) depuis le **même modèle**, sous le nom `lab-template-test-2`. Revérifiez chaque réglage.
4. Pendant qu’elle est arrêtée, vérifiez qu’elle a un UUID de VM différent, des ID de VDI différents et aucune interface. Démarrez-la par sa console et vérifiez que le fichier témoin a toujours sa somme d’origine, et non la nouvelle valeur du test 1. Arrêtez-la normalement.
5. Notez les UUID et les ID de VDI des deux VM, l’UUID du modèle, les résultats dans les invités et les versions installées. Laissez les VM de test arrêtées.

**Vérification :** les deux invités démarrent avec les données attendues, et la modification du test 1 n’a pas atteint le test 2. Cette vérification de fichier ne teste pas la récupération d’une application, et ne supprime pas les identités système dupliquées. Ne connectez aucun réseau de production avant que le responsable de l’invité les ait réglées.

Pour faire le ménage, [supprimez chaque VM de test](/docs/xoa-hl/vm-operations/) une fois identifiée. Gardez le modèle, la VM d’origine et vos sauvegardes. Pour une nouvelle version du modèle, préparez une nouvelle copie avec un nouveau nom versionné et refaites ces vérifications.

## En cas de problème {#problems}

| Problème | À vérifier |
| --- | --- |
| La conversion est refusée | Lisez l’erreur, les permissions sur la VM et le pool, et l’état réel d’alimentation. Ne forcez pas l’arrêt d’un invité important, et ne convertissez pas de nouveau un objet non identifié. Après une erreur, vérifiez le type d’objet et les médias amovibles du même UUID. |
| Le modèle est introuvable | Choisissez le type d’objet Template, le bon pool et les bons filtres, puis actualisez. Un modèle n’apparaît pas dans la liste normale des VM. Ne faites pas d’autre copie avant d’avoir vérifié l’inventaire. |
| La création de la VM échoue | Conservez l’erreur et la liste des modèles, VM et VDI avant de réessayer. XO tente de nettoyer après un échec, mais une réponse perdue ou un nettoyage raté peut laisser des objets. Ne supprimez jamais en masse des disques qui semblent orphelins. |
| L’invité diffère ou ne démarre pas | Gardez le modèle et les journaux. Vérifiez l’UUID du modèle, les disques copiés, le firmware et les ressources, et les paramètres d’installation. Ne modifiez pas le réseau de gestion de l’hôte pour corriger. |

Modifier un invité à l’intérieur d’un modèle, retirer ou supprimer des modèles, déployer vers un autre pool, le stockage des clones rapides, cloud-init et la préparation propre à chaque système ne sont pas traités ici. Si un problème persiste, [signalez-le](/docs/xoa-hl/troubleshooting/#report-a-problem) sans données sensibles.

{{< details title="Sources" closed="true" >}}
- **Conversion** : [action de l’onglet Avancé, VM arrêtées uniquement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [boîte de confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permissions, médias, conversion et nettoyage après une création échouée](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Assistant de création de VM** : [identité de la ligne du modèle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/home/template-item.js), [réglages par défaut et transmis de l’assistant](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [copie des disques et remplacement des interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **Build HomeLab** : [script de build xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
