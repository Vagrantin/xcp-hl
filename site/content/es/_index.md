---
title: XCP-hl
layout: hextra-home
translationKey: home
---

{{< hextra/hero-badge link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>{{< latest-iso-badge label="Alfa" >}}</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  Virtualización para todos
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  XCP-hl lleva XCP-ng 8.3 a tu laboratorio doméstico, con varias opciones de despliegue de Xen Orchestra y controles integrados de actualización del host y del appliance.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hero-actions hx:mb-6">
{{< latest-iso-download text="Descargar la ISO" shaText="Suma de comprobación SHA256" >}}
{{< hextra/hero-button text="Leer la documentación" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
{{< hextra/hero-button text="Manual de XOA-HL" link="docs/xoa-hl/" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl es software en fase alfa.** Está en desarrollo activo y todavía no ha pasado por un ciclo de estabilización. **Espera cambios incompatibles en cada versión.**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card title="Basado en XCP-ng 8.3" subtitle="Construido sobre Xen 4.17, XAPI y Open vSwitch, con las funciones de gestión de hosts y máquinas virtuales del proyecto original." >}}
  {{< hextra/feature-card title="Elige tu XO" subtitle="Despliega desde XO Lite la imagen hl (XOA-hl, la interfaz web de administración), el appliance oficial de Vates, la compilación de Ronivay o tu propia imagen." >}}
  {{< hextra/feature-card title="Menús simplificados" subtitle="XOA-hl simplifica Xen Orchestra con menús centrados en las tareas y controles integrados de actualización de XCP-hl." >}}
  {{< hextra/feature-card title="Biblioteca ISO lista para usar" subtitle="En un disco adecuado de al menos 100 GB, una instalación nueva reserva una biblioteca ISO de 20 GB y la registra en el primer arranque." >}}
  {{< hextra/feature-card title="Firmado y actualizable sin reinstalar" subtitle="Cada ISO y RPM se firma con la clave GPG de XCP-hl; un host en ejecución recibe las actualizaciones desde el repositorio yum del proyecto." >}}
  {{< hextra/feature-card title="Revisiones fijas, sin seguir la última novedad" subtitle="XO Lite y XOA-hl usan revisiones fijas del proyecto original. Esas revisiones solo cambian deliberadamente; la matriz de versiones registra lo que incluye cada compilación." >}}
{{< /hextra/feature-grid >}}

{{< legacy-home >}}
