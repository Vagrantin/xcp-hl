---
title: XCP-hl
layout: hextra-home
translationKey: home
---

{{< hextra/hero-badge link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>{{< latest-iso-badge label="Alpha" >}}</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  La virtualisation pour tous
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  XCP-hl apporte XCP-ng 8.3 à votre homelab, avec plusieurs choix de déploiement de Xen Orchestra et des commandes intégrées pour mettre à jour les hôtes et l’appliance.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hero-actions hx:mb-6">
{{< latest-iso-download text="Télécharger l'ISO" shaText="Somme de contrôle SHA256" >}}
{{< hextra/hero-button text="Lire la documentation" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl est un logiciel en version alpha.** Le projet est en cours de
développement actif et n'a pas encore connu de cycle de stabilisation.
**Attendez-vous à des changements incompatibles à chaque version.**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Basé sur XCP-ng 8.3"
    subtitle="Construit sur Xen 4.17, XAPI et Open vSwitch, avec les fonctions amont de gestion des hôtes et des VM."
  >}}
  {{< hextra/feature-card
    title="Votre XO, votre choix"
    subtitle="Déployez depuis XO Lite l’image hl (XOA-hl, l’interface Web d’administration), l’appliance officielle de Vates, le build de Ronivay ou votre propre image."
  >}}
  {{< hextra/feature-card
    title="Menus épurés"
    subtitle="XOA-hl simplifie Xen Orchestra avec des menus épurés et des commandes de mise à jour XCP-hl intégrées."
  >}}
  {{< hextra/feature-card
    title="Bibliothèque d'ISO prête à l'emploi"
    subtitle="Sur un disque adapté d’au moins 100 Go, une nouvelle installation réserve une bibliothèque ISO de 20 Go et l’enregistre au premier démarrage."
  >}}
  {{< hextra/feature-card
    title="Signé, mis à jour en place"
    subtitle="Chaque ISO et RPM est signé avec la clé GPG XCP-hl, et un hôte en fonctionnement récupère les mises à jour depuis le dépôt yum du projet."
  >}}
  {{< hextra/feature-card
    title="Figé, pas à la pointe"
    subtitle="XO Lite et XOA-hl utilisent des révisions amont fixes. Ces révisions sont modifiées délibérément ; la matrice des versions indique le contenu de chaque build."
  >}}
{{< /hextra/feature-grid >}}

{{< legacy-home >}}
