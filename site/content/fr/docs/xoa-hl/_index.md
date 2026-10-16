---
title: Manuel XOA-HL
weight: 3
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:0489013a9baae9578c8a2897dcd3846e57a3c721e2be7c620eaa133b45785bc7
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
- [Créer un stockage NFS pour les disques de VM](/docs/xoa-hl/storage-networks/#nfs-vm-storage).
- [Créer un VLAN de laboratoire sur une liaison hôte dédiée](/docs/xoa-hl/storage-networks/#host-vlan-network).
- [Migrer une VM dans son pool, l’exporter et importer une copie isolée](/docs/xoa-hl/vm-transfer/).
- [Créer et réutiliser un modèle de VM arrêté](/docs/xoa-hl/templates/).
- [Installer et vérifier les outils invités Linux](/docs/xoa-hl/guest-tools/).
- [Tester la planification et la rétention des sauvegardes](/docs/xoa-hl/backup-restore/#backup-schedules).
- [Tester les sauvegardes incrémentales et la récupération de chaîne](/docs/xoa-hl/backup-restore/#delta-backups).
- [Récupérer un fichier d’une sauvegarde delta](/docs/xoa-hl/backup-restore/#file-restore).
- [Tester une réplique DR complète sur un autre pool](/docs/xoa-hl/backup-restore/#dr-replica).
- [Tester la sauvegarde SMB Windows Server et une restauration isolée](/docs/xoa-hl/backup-restore/#smb-remote).
- [Vérifier la gestion des hôtes/pools, la découverte XO Lite et les statistiques des hôtes](/docs/xoa-hl/hosts-pools/).
- [Répéter la jonction d’un hôte jetable à un pool](/docs/xoa-hl/hosts-pools/#pool-join).
- [Créer des utilisateurs et des groupes et vérifier les droits sur un objet](/docs/xoa-hl/permissions/).
- [Tester un ensemble de ressources délégué et son quota VM](/docs/xoa-hl/permissions/#resource-set-delegation).
- [Protéger la connexion d’un compte local par des codes à usage unique (OTP)](/docs/xoa-hl/sign-in-otp/).

Ces prévisualisations ont été vérifiées dans les sources ; les tests en laboratoire jetable restent à faire. Pour la protection, utilisez le [pilote de sauvegarde complète et restauration isolée](/docs/xoa-hl/backup-restore/) ; les autres modes de sauvegarde/DR nécessitent une validation distincte par version.

## Maintenir votre installation

- [Préparer la maintenance et vérifier son résultat](/docs/xoa-hl/maintenance/).
- [Exporter la configuration XO et préparer un import isolé](/docs/xoa-hl/configuration-backup/).
- [Tester la sauvegarde et la rétention des métadonnées du pool](/docs/xoa-hl/configuration-backup/#pool-metadata).
- [Diagnostiquer une sauvegarde complète NFS en échec](/docs/xoa-hl/troubleshooting/#backup-failures).
- [Diagnostiquer la connectivité réseau](/docs/xoa-hl/troubleshooting/#network-connectivity).
- [Dépanner et signaler un problème](/docs/xoa-hl/troubleshooting/).
- [Mettre à jour l’appliance XOA-HL](/docs/guides/updates/#mettre-à-jour-xoa-hl-lappliance).
- [Mettre à jour l’hôte hyperviseur](/docs/guides/updates/#mettre-à-jour-xcp-hl-lhôte).
- [Répéter la maintenance d’un hôte et l’évacuation d’une VM de test](/docs/xoa-hl/hosts-pools/#host-maintenance-mode).
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
