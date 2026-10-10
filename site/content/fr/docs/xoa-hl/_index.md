---
title: Manuel XOA-HL
weight: 3
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:1606313defd7a1203320e00757865cf05cb9ef7e6794b4bdfe355276f5cbba57
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Trouvez votre prochaine tâche dans la documentation XOA-HL. Commencez par le déploiement, puis maintenez à jour l’appliance et l’hôte hyperviseur.

{{< callout type="info" >}}
Ce manuel est en cours d’enrichissement. Les tutoriels de première connexion et de création d’une VM sont disponibles en prévisualisation, vérifiés dans les sources. Les chapitres sur la sauvegarde, la restauration et l’administration restent en préparation.
{{< /callout >}}

## Bien démarrer

- [Se connecter, ajouter un hôte et choisir sa langue](/docs/xoa-hl/first-login/).
- [Créer et installer sa première machine virtuelle](/docs/xoa-hl/create-vm/).
- [Déployer XOA-HL et connecter votre hôte](/docs/start/#start-deploy-xoa).
- [Comprendre l’hôte, XO Lite et l’appliance](/docs/start/#start-architecture).
- [Consulter les composants livrés dans chaque version](/docs/reference/release-matrix/).

XOA-HL possède sa propre adresse. Utilisez l’adresse de l’appliance pour Xen Orchestra et celle de l’hôte pour XO Lite. L’interface de gestion et cette documentation ont des réglages de langue distincts.

## Maintenir votre installation

- [Mettre à jour l’appliance XOA-HL](/docs/guides/updates/#mettre-à-jour-xoa-hl-lappliance).
- [Mettre à jour l’hôte hyperviseur](/docs/guides/updates/#mettre-à-jour-xcp-hl-lhôte).
- [Lire les changements des versions](/docs/reference/changelog/).

Vérifiez les versions auxquelles un guide s’applique avant de le suivre. La matrice indique les composants livrés ensemble ; elle ne remplace pas les résultats des tests d’intégration.

## Comprendre les termes

[Ouvrez le glossaire](glossary/) pour les termes VM, hôte, pool, stockage, snapshot et sauvegarde. Les [pages des composants destinées aux contributeurs](/docs/components/) expliquent l’implémentation.

## Langue et signalement d’erreurs

Le sélecteur de langue ouvre la même page en English, Français ou 日本語. [Consultez l’état des traductions](translation-status/) avant de vous appuyer sur une traduction provisoire.

[Signalez un problème de documentation](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Indiquez l’URL, la langue sélectionnée, la version de l’appliance et l’étape à corriger. N’incluez aucun mot de passe ni donnée privée.
