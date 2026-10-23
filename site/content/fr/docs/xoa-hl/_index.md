---
title: Manuel XOA-HL
weight: 2
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:9690e24c060de4d8fcc693f5a8507c57cce56c189f0a4c0c5abd9829f4c4abae
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL est l’appliance, une machine virtuelle prête à l’emploi, qui exécute Xen Orchestra. Depuis votre navigateur, elle vous permet de gérer vos hôtes XCP-HL et vos machines virtuelles. Ce manuel explique comment la mettre en service, faire fonctionner vos VM, les protéger et tout maintenir à jour.

{{< callout type="info" >}}
**S’applique à** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Ces guides suivent le code publié, mais n’ont pas encore été testés de bout en bout sur un laboratoire. Entraînez-vous d’abord sur des VM de test.
{{< /callout >}}

## Pour commencer

Vous découvrez XOA-HL ? Suivez ces trois guides dans l’ordre.

{{< cards >}}
  {{< card link="first-login/" title="1. Première connexion" subtitle="Connectez-vous, changez le mot de passe, choisissez la langue et ajoutez votre hôte." >}}
  {{< card link="create-vm/" title="2. Première VM" subtitle="Importez un ISO d’installation et installez une VM de test." >}}
  {{< card link="backup-restore/" title="3. Sauvegarde et restauration" subtitle="Sauvegardez la VM, puis vérifiez qu’une copie restaurée fonctionne." >}}
{{< /cards >}}

XOA-HL n’est pas encore déployée ? Commencez par [la déployer depuis XO Lite](/docs/start/#start-deploy-xoa). Pour comprendre le rôle de l’hôte, de XO Lite et de l’appliance, lisez la [présentation de l’architecture](/docs/start/#start-architecture).

## Machines virtuelles

- [Gérer les VM](/docs/xoa-hl/vm-operations/) : démarrage et arrêt, snapshots, copies, CPU et mémoire, suppression.
- [Utiliser la console d’une VM](/docs/xoa-hl/vm-operations/#vm-console) et corriger un écran noir.
- [Créer un snapshot et revenir en arrière](/docs/xoa-hl/vm-operations/#stopped-snapshot).
- [Installer les outils invités Linux](/docs/xoa-hl/guest-tools/).
- [Créer et utiliser des modèles de VM](/docs/xoa-hl/templates/).
- [Migrer, exporter et importer une VM](/docs/xoa-hl/vm-transfer/).

## Stockage et réseaux

- [Ajouter des disques et des interfaces réseau](/docs/xoa-hl/storage-networks/).
- [Créer un stockage NFS pour les disques de VM](/docs/xoa-hl/storage-networks/#nfs-vm-storage).
- [Créer un réseau VLAN](/docs/xoa-hl/storage-networks/#host-vlan-network).
- [Diagnostiquer un problème réseau](/docs/xoa-hl/troubleshooting/#network-connectivity).

## Sauvegarde et récupération

- [Planifier les sauvegardes et régler la rétention](/docs/xoa-hl/backup-restore/#backup-schedules).
- [Utiliser les sauvegardes incrémentales](/docs/xoa-hl/backup-restore/#delta-backups).
- [Récupérer un seul fichier](/docs/xoa-hl/backup-restore/#file-restore).
- [Copier une VM vers un autre pool (réplique DR)](/docs/xoa-hl/backup-restore/#dr-replica).
- [Sauvegarder sur un partage Windows Server (SMB)](/docs/xoa-hl/backup-restore/#smb-remote).
- [Corriger une sauvegarde en échec](/docs/xoa-hl/troubleshooting/#backup-failures).

## Hôtes, utilisateurs et sécurité

- [Gérer les hôtes et les pools](/docs/xoa-hl/hosts-pools/) : connexions, bouton XO Lite et statistiques.
- [Ajouter un hôte à un pool](/docs/xoa-hl/hosts-pools/#pool-join).
- [Mettre un hôte en mode maintenance](/docs/xoa-hl/hosts-pools/#host-maintenance-mode).
- [Gérer les utilisateurs, les groupes et les droits](/docs/xoa-hl/permissions/).
- [Déléguer des ressources avec un quota](/docs/xoa-hl/permissions/#resource-set-delegation).
- [Ajouter un code à usage unique à la connexion](/docs/xoa-hl/sign-in-otp/).

## Maintenir XOA-HL en service

- [Mettre à jour l’appliance](/docs/guides/updates/#mettre-à-jour-xoa-hl-lappliance) et [mettre à jour l’hôte](/docs/guides/updates/#mettre-à-jour-xcp-hl-lhôte).
- [Préparer la maintenance et vérifier le résultat](/docs/xoa-hl/maintenance/).
- [Exporter la configuration XO](/docs/xoa-hl/configuration-backup/).
- [Sauvegarder les métadonnées du pool](/docs/xoa-hl/configuration-backup/#pool-metadata).
- [Dépanner un problème](/docs/xoa-hl/troubleshooting/).
- [Voir le contenu de chaque version](/docs/reference/release-matrix/) et [lire le journal des modifications](/docs/reference/changelog/).

## Référence

- [Concepts et périmètre fonctionnel](/docs/xoa-hl/concepts/)
- [Paramètres du service](/docs/xoa-hl/configuration/)
- [Automatisation avec xo-cli](/docs/xoa-hl/automation/)
- [Glossaire](/docs/xoa-hl/glossary/)
- [Pages pour les contributeurs](/docs/components/)

## Aide et retours

L’interface de XOA-HL et cette documentation ont chacune leur propre réglage de langue. Utilisez le sélecteur en haut de cette page pour changer la langue de la documentation. L’[état de relecture des pages](/docs/xoa-hl/translation-status/) indique quelles pages ont été relues.

[Signaler un problème dans la documentation](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Indiquez l’adresse de la page, l’étape à corriger et la version de votre appliance. N’y mettez jamais de mot de passe ni de donnée privée.
