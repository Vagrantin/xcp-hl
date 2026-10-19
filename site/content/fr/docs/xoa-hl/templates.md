---
title: "Créer et utiliser un modèle de VM"
linkTitle: "Modèles de VM"
description: "Transformez une copie de VM préparée en modèle, puis créez de nouvelles VM à partir de ce modèle."
weight: 42
translationKey: xoa-manual-templates
translationStatus: draft
sourceRevision: sha256:c7859c3ab668a7fcf3972680f3f5a0dacf530773f1cfa4a958b2bc49afc11c89
glossaryTerms: ["backup", "pool", "sr", "vm"]
---

Transformez une copie de test préparée en modèle réutilisable, puis créez deux VM distinctes et vérifiez leurs disques et données invitées. Conservez la VM d’origine inchangée.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2 (`e281c536`). Conversion et déploiement sur appliance installée restent à tester. Ce pilote de laboratoire isolé n’est pas une procédure validée de généralisation d’OS invité ni de création d’image de production.
{{< /callout >}}

## Avant de commencer

- Utilisez un compte administrateur XOA-HL et un invité installé jetable avec des disques ordinaires, sans disque partagé ni périphérique en passthrough. La conversion exige des droits d’administration sur la VM et son pool ; une autorisation limitée à la VM ne suffit pas.
- Suivez la [copie complète d’une VM arrêtée](/docs/xoa-hl/vm-operations/#full-copy) pour créer une copie de travail distincte. Notez les UUID de l’original et de la copie, les ID des VDI, SR, tailles et la somme de contrôle d’un fichier témoin sans importance. Vérifiez que la copie démarre isolément, puis arrêtez-la normalement.
- Gardez **toutes les cartes réseau supprimées** de la copie, éjectez son ISO d’installation, désactivez son allumage automatique et excluez les objets du laboratoire des tâches non supervisées. Réservez RAM hôte et capacité de SR inscriptible pour le modèle et deux déploiements de test. Ne convertissez ni l’appliance ni la VM d’origine.
- Disposez d’un accès console et des identifiants de l’invité de laboratoire. Renommer une VM ou changer sa MAC ne nettoie pas identifiants, noms d’hôte, paramètres IP, clés et identités applicatives copiés. Gardez ces copies accessibles uniquement par console. Préparation propre à l’OS, licences, cloud-init et outils invités nécessitent des procédures distinctes avant toute réutilisation plus large.

Les opérations de gestion se font dans le **navigateur à l’adresse de l’appliance**. Les contrôles du fichier et de sa somme se font dans la **console de l’invité**, pas sur l’hôte ou l’appliance. Un modèle sur la même infrastructure n’est pas une sauvegarde indépendante ; conservez séparément les [preuves de sauvegarde et restauration](/docs/xoa-hl/backup-restore/) nécessaires.

Pour un invité Ubuntu 24.04 fraîchement installé, utilisez le [pilote des outils invités](/docs/xoa-hl/guest-tools/) avant de préparer une copie ; gardez l’exercice de template accessible uniquement par console.

## 1. Convertir uniquement la copie de travail arrêtée {#convert-template}

1. Revérifiez UUID de la copie, état arrêté (`Halted`), liste réseau vide et disques enregistrés. Donnez-lui un nom unique comme `lab-template-v1` et une description indiquant OS/version, date de préparation et somme témoin. Actualisez et relisez ces valeurs avant conversion.
2. Ouvrez son onglet **Avancé** (`/#/vms/<copy-uuid>/advanced`) et choisissez **Convert to template**. Le bouton est désactivé si la VM n’est pas arrêtée. À ce38, bouton et confirmation restent anglais en EN/FR/JA ; la fenêtre avertit que l’opération est définitive. Annulez si ce n’est pas la copie jetable prévue.
3. Confirmez une fois et attendez la fin. Ouvrez **Accueil**, choisissez le type d’objet **Template** (`/#/home?t=VM-template`), effacez les filtres au besoin et développez la ligne concernée pour lire son UUID complet. Vérifiez qu’il correspond à la copie de travail, avec nom/description attendus. La VM d’origine doit toujours exister séparément.

**Vérification :** la copie existante est devenue un modèle avec le **même UUID**. La conversion n’est pas une copie et ne crée pas une seconde VM. Le serveur tente d’éjecter les médias amovibles avant de définir le type modèle ; une erreur d’éjection peut laisser des modifications antérieures même si la conversion échoue. Actualisez type, médias et tâche avant de réessayer. Aucune procédure de reconversion par l’interface ou de retour arrière automatique n’est établie ici.

## 2. Créer une VM arrêtée depuis ce modèle {#deploy-template}

1. Ouvrez **Nouveau → VM** (`/#/vms/new`), choisissez le même pool et le modèle personnalisé enregistré. Utilisez un nom distinct comme `lab-template-test-1` ; vérifiez l’UUID `template=` dans l’URL obtenue, pas seulement son nom.
2. Relisez CPU/RAM, disques existants du modèle, tailles et SR inscriptibles de destination. Gardez l’ensemble et les tailles attendus pour ce pilote. Choisissez **No config drive** dans Installation : ce test réutilise le disque installé, sans lancer d’installateur ni supposer que cloud-init modifie l’identité invitée. Si les disques attendus ou cette option manquent, arrêtez-vous et revérifiez le modèle.
3. Dans **Interfaces**, supprimez chaque interface proposée et vérifiez la liste vide. Même sans carte dans le modèle, l’assistant peut proposer les réseaux par défaut du pool. Le serveur retire les VIF clonées puis crée les interfaces soumises par ce formulaire ; cela ne garantit pas à lui seul l’isolation.
4. Dans **Avancé**, décochez **Démarrer la VM après sa création** et gardez l’allumage automatique désactivé. Dans **Récapitulatif**, décochez **Clonage rapide**, relisez une seule VM, le nombre de disques, les ressources, les SR cibles et **zéro interface**, puis cliquez une fois sur **Créer**. Démarrage après création et clonage rapide sont initialement activés ; ne vous fiez pas à des réglages mémorisés. Sans clonage rapide, ce chemin de modèle sur disque demande une copie complète ; capacité et sauvegarde indépendante restent à vérifier séparément.
5. Attendez, actualisez et notez le nouvel UUID de VM. Avant tout démarrage, vérifiez état arrêté (`Halted`), onglet Réseau vide, nombre/tailles/SR des disques et ID de VDI distincts des disques enregistrés du modèle et de l’original. Vérifiez que modèle et original existent encore. Si une carte apparaît ou si la VM a démarré, arrêtez la copie et examinez son exposition avant de continuer.

**Vérification :** une VM distincte, arrêtée, avec ses disques et sans carte réseau existe. Une notification de succès ou un nouveau nom ne prouve pas les ressources attendues ni la préparation de l’invité.

## 3. Vérifier des déploiements isolés et reproductibles

1. Démarrez uniquement `lab-template-test-1` après relecture de l’isolation. Par sa [console](/docs/xoa-hl/vm-operations/#vm-console), vérifiez démarrage/connexion, disques et somme témoin. Modifiez uniquement ce fichier sans importance avec une valeur de test distincte, notez-la, puis arrêtez normalement.
2. Répétez la section 2 depuis le **même modèle** sous le nom `lab-template-test-2`, en relisant tous les réglages. Vérifiez autre UUID, VDI distinctes et liste réseau vide à l’arrêt. Démarrez par console et vérifiez que le fichier a sa somme initiale, pas la valeur modifiée de test-1. Arrêtez normalement.
3. Notez les deux inventaires VM/VDI, l’UUID du modèle, les résultats invités et versions installées. Laissez les VM arrêtées. À la fin, suivez la [suppression d’une VM jetable identifiée](/docs/xoa-hl/vm-operations/) pour chaque VM de test uniquement, en conservant modèle, VM d’origine et sauvegardes nécessaires.

**Vérification :** les deux invités isolés démarrent avec les données attendues, et modifier test-1 ne change pas le fichier initial de test-2. Ce petit contrôle n’est ni une récupération applicative, ni une généralisation d’identités OS, ni une matrice d’invités supportés. Ne connectez pas de réseau de production avant que le responsable de l’invité ait résolu séparément les identités dupliquées et validé sa préparation.

## En cas de problème

- **Conversion refusée :** lisez erreur, permissions VM/pool et état réel. Ne forcez pas l’arrêt d’un invité important et ne convertissez pas plusieurs fois un objet mal identifié. Revérifiez type et médias amovibles du même UUID après une erreur.
- **Modèle absent :** choisissez type Template, pool et filtres corrects, puis actualisez. Ne déduisez pas sa suppression de la liste des VM ordinaires et ne créez pas d’autre copie avant rapprochement de l’inventaire.
- **Création en échec :** conservez erreur et inventaire modèle/nouvelle VM/VDI avant de réessayer. Le code prévoit un nettoyage sur échec, mais une réponse perdue ou un nettoyage défaillant ne prouve pas la disparition de tous les objets créés. Ne supprimez jamais en masse des disques apparemment orphelins.
- **Invité différent ou sans démarrage :** gardez modèle et journaux ; vérifiez UUID, disques copiés, firmware/ressources et méthode de configuration. Ne validez pas le pilote et ne modifiez pas le réseau de gestion de l’hôte pour le réparer.

Pour une autre révision, préparez une nouvelle copie jetable avec un nom versionné et répétez les vérifications isolées. Maintenance de l’invité sur place, retrait/suppression du modèle, déploiement entre pools, stockage des clones rapides, cloud-init et nettoyage propre à l’OS restent des validations distinctes. Conservez les résultats non résolus et [signalez des éléments expurgés](/docs/xoa-hl/troubleshooting/#report-a-problem).

## Sources

XO à `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c` : [action Avancé limitée à l’arrêt](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [confirmation anglaise](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permissions, médias, conversion et nettoyage de création](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [identité dans la ligne modèle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/home/template-item.js), [réglages initiaux et transmis de l’assistant](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [copie des disques et remplacement des VIF](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs). Sélection des correctifs/build HomeLab : [xoa-hl à `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
