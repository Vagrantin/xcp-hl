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
  Virtualisierung für alle
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  XCP-hl bringt XCP-ng 8.3 in Ihr Homelab, mit verschiedenen Xen-Orchestra-Bereitstellungen und integrierten Einstellungen für Host- und Appliance-Updates.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hero-actions hx:mb-6">
{{< latest-iso-download text="ISO herunterladen" shaText="SHA256-Prüfsumme" >}}
{{< hextra/hero-button text="Dokumentation lesen" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
{{< hextra/hero-button text="XOA-HL-Handbuch" link="docs/xoa-hl/" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl ist Alpha-Software.** Es wird aktiv entwickelt und hat noch keinen
Stabilisierungszyklus durchlaufen. **Rechnen Sie bei jeder Veröffentlichung mit inkompatiblen Änderungen.**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Auf Basis von XCP-ng 8.3"
    subtitle="Basiert auf Xen 4.17, XAPI und Open vSwitch und bietet die Host- und VM-Verwaltung des Upstream-Projekts."
  >}}
  {{< hextra/feature-card
    title="XO nach Ihrer Wahl"
    subtitle="Stellen Sie über XO Lite das hl-Image (XOA-hl, die Verwaltungsoberfläche), die offizielle Vates-Appliance, Ronivays Build oder Ihr eigenes Image bereit."
  >}}
  {{< hextra/feature-card
    title="Aufgeräumte Menüs"
    subtitle="XOA-hl vereinfacht Xen Orchestra mit übersichtlichen Menüs und integrierten Einstellungen für XCP-hl-Updates."
  >}}
  {{< hextra/feature-card
    title="Sofort nutzbare ISO-Bibliothek"
    subtitle="Bei einer Neuinstallation wird auf einem geeigneten Datenträger mit mindestens 100 GB eine ISO-Bibliothek mit 20 GB reserviert und beim ersten Start registriert."
  >}}
  {{< hextra/feature-card
    title="Signiert und direkt aktualisierbar"
    subtitle="Jedes ISO und RPM wird mit dem GPG-Schlüssel von XCP-hl signiert. Ein laufender Host bezieht Updates aus dem yum-Repository des Projekts."
  >}}
  {{< hextra/feature-card
    title="Festgelegte statt experimenteller Versionen"
    subtitle="XO Lite und XOA-hl verwenden feste Upstream-Revisionen. Änderungen erfolgen bewusst; die Versionsmatrix dokumentiert den Inhalt jedes Builds."
  >}}
{{< /hextra/feature-grid >}}

{{< legacy-home >}}
