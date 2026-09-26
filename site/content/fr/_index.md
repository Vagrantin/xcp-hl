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
  L'hyperviseur libéré
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  Une ISO basée sur XCP-ng 8.3 amont, qui déploie le Xen Orchestra de votre choix.<br><br>&nbsp;<br class="hx:sm:block hx:hidden" />
  Administrer vos machines virtuelles n'a jamais été aussi simple : les mises à jour de vos hôtes XCP-hl et de votre VM XOA-hl sont gérées nativement.
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
    title="Compatible XCP-ng 8.3"
    subtitle="L'intégralité des fonctionnalités amont : Xen 4.17, XAPI, Open vSwitch, migration à chaud, HA, vGPU."
  >}}
  {{< hextra/feature-card
    title="Votre XOA, votre choix"
    subtitle="Déployez l'image HomeLab, l'appliance officielle de Vates, le build de Ronivay, ou la vôtre, choisie depuis un sélecteur dans XO Lite."
  >}}
  {{< hextra/feature-card
    title="Menus épurés"
    subtitle="XOA-hl retire les bandeaux et les entrées de menu qui nécessitent une licence : XOA-hl est un Xen Orchestra simplifié."
  >}}
  {{< hextra/feature-card
    title="Bibliothèque d'ISO prête à l'emploi"
    subtitle="Une partition de 20 Go est réservée à l'installation et enregistrée comme SR d'ISO au premier démarrage. Importez une image et construisez une VM sans toucher à la ligne de commande."
  >}}
  {{< hextra/feature-card
    title="Signé, mis à jour en place"
    subtitle="Chaque ISO et RPM est signé avec la clé GPG XCP-hl, et un hôte en fonctionnement récupère les mises à jour depuis le dépôt yum du projet."
  >}}
  {{< hextra/feature-card
    title="Figé, pas à la pointe"
    subtitle="XOLite-hl et XOA-hl sont figés sur des versions amont connues comme stables. Le passage à une version plus récente n'a lieu qu'après des tests approfondis, si bien que les évolutions amont ne peuvent pas casser votre hôte."
  >}}
{{< /hextra/feature-grid >}}
