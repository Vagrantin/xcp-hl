---
title: Manuel XOA-HL
weight: 3
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:aadb06215a0e9d6f8cf2b16433dd84d1b64d4c3864cf651506206a53f4a48bb0
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Trouvez votre prochaine tâche dans la documentation XOA-HL. Commencez par le déploiement, puis maintenez à jour l’appliance et l’hôte hyperviseur.

{{< callout type="info" >}}
Le parcours débutant est disponible en prévisualisation, vérifié dans les sources : déploiement, première connexion, création de VM, sauvegarde complète et restauration isolée. La validation sur un laboratoire jetable et la revue humaine des traductions restent à faire. La maintenance, l’export de configuration et le dépannage sont également disponibles en prévisualisation vérifiée dans les sources ; la validation de récupération et de retour arrière reste à faire.
{{< /callout >}}

## Bien démarrer

- [Se connecter, ajouter un hôte et choisir sa langue](/docs/xoa-hl/first-login/).
- [Créer et installer sa première machine virtuelle](/docs/xoa-hl/create-vm/).
- [Sauvegarder une VM et tester une restauration isolée](/docs/xoa-hl/backup-restore/).
- [Déployer XOA-HL et connecter votre hôte](/docs/start/#start-deploy-xoa).
- [Comprendre l’hôte, XO Lite et l’appliance](/docs/start/#start-architecture).
- [Consulter les composants livrés dans chaque version](/docs/reference/release-matrix/).

XOA-HL possède sa propre adresse. Utilisez l’adresse de l’appliance pour Xen Orchestra et celle de l’hôte pour XO Lite. L’interface de gestion et cette documentation ont des réglages de langue distincts.

## Administration quotidienne

- [Gérer et redimensionner une VM, utiliser les snapshots, cloner, créer une copie complète et comprendre la suppression](/docs/xoa-hl/vm-operations/).
- [Ouvrir la console et diagnostiquer un affichage vide](/docs/xoa-hl/vm-operations/#vm-console).
- [Créer un snapshot à froid, vérifier la restauration et supprimer un point de test](/docs/xoa-hl/vm-operations/#stopped-snapshot).
- [Connecter une bibliothèque ISO, ajouter un disque et gérer les interfaces réseau VM](/docs/xoa-hl/storage-networks/).
- [Migrer une VM dans son pool, l’exporter et importer une copie isolée](/docs/xoa-hl/vm-transfer/).
- [Créer et réutiliser un modèle de VM arrêté](/docs/xoa-hl/templates/).
- [Installer et vérifier les outils invités Linux](/docs/xoa-hl/guest-tools/).
- [Tester la planification et la rétention des sauvegardes](/docs/xoa-hl/backup-restore/#backup-schedules).
- [Vérifier la gestion des hôtes/pools, la découverte XO Lite et les statistiques des hôtes](/docs/xoa-hl/hosts-pools/).
- [Créer des utilisateurs et des groupes et vérifier les droits sur un objet](/docs/xoa-hl/permissions/).
- [Protéger la connexion d’un compte local par des codes à usage unique (OTP)](/docs/xoa-hl/sign-in-otp/).

Ces prévisualisations ont été vérifiées dans les sources ; les tests en laboratoire jetable restent à faire. Pour la protection, utilisez le [pilote de sauvegarde complète et restauration isolée](/docs/xoa-hl/backup-restore/) ; les autres modes de sauvegarde/DR nécessitent une validation distincte par version.

## Maintenir votre installation

- [Préparer la maintenance et vérifier son résultat](/docs/xoa-hl/maintenance/).
- [Exporter la configuration XO et préparer un import isolé](/docs/xoa-hl/configuration-backup/).
- [Diagnostiquer une sauvegarde complète NFS en échec](/docs/xoa-hl/troubleshooting/#backup-failures).
- [Dépanner et signaler un problème](/docs/xoa-hl/troubleshooting/).
- [Mettre à jour l’appliance XOA-HL](/docs/guides/updates/#mettre-à-jour-xoa-hl-lappliance).
- [Mettre à jour l’hôte hyperviseur](/docs/guides/updates/#mettre-à-jour-xcp-hl-lhôte).
- [Lire les changements des versions](/docs/reference/changelog/).

Vérifiez les versions auxquelles un guide s’applique avant de le suivre. La matrice indique les composants livrés ensemble ; elle ne remplace pas les résultats des tests d’intégration.

## Référence et automatisation

- [Comprendre les concepts, versions et fonctions](/docs/xoa-hl/concepts/).
- [Configurer le service de l’appliance](/docs/xoa-hl/configuration/).
- [Découvrir les méthodes API et lire l’inventaire avec xo-cli](/docs/xoa-hl/automation/).

## Comprendre les termes

[Ouvrez le glossaire](glossary/) pour les termes VM, hôte, pool, stockage, snapshot et sauvegarde. Les [pages des composants destinées aux contributeurs](/docs/components/) expliquent l’implémentation.

## Langue et signalement d’erreurs

Le sélecteur de langue ouvre la même page en English, Français ou 日本語. [Consultez l’état des traductions](translation-status/) avant de vous appuyer sur une traduction provisoire.

[Signalez un problème de documentation](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Indiquez l’URL, la langue sélectionnée, la version de l’appliance et l’étape à corriger. N’incluez aucun mot de passe ni donnée privée.
