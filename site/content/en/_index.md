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
  Hypervisor liberated
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  An ISO based on upstream XCP-ng 8.3 that deploys the&nbsp;<br class="hx:sm:block hx:hidden" />
  Xen Orchestra of your choice.
  
  It's never be easier to administrate your Virtual machines, updates of your XCP-hl hosts and XOA-hl VM are handle out of the box.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-button text="Download the ISO" link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
{{< hextra/hero-button text="Read the documentation" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl is alpha software.** It is under active development and has not been
through a stabilisation cycle. **Expect breaking changes at every release.**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Drop-in XCP-ng 8.3"
    subtitle="The full upstream feature set — Xen 4.17, XAPI, Open vSwitch, live migration, HA, vGPU."
  >}}
  {{< hextra/feature-card
    title="Your choice of XOA"
    subtitle="Deploy the HomeLab image, the official Vates appliance, Ronivay's build, or your own, picked from a selector in XO Lite."
  >}}
  {{< hextra/feature-card
    title="Cleaned up menus"
    subtitle="XOA-hl strips banners and the menu items that requires a license, XOA-hl is a simplified Xen Orchestra."
  >}}
  {{< hextra/feature-card
    title="Ready-to-use ISO library"
    subtitle="A 20 GB partition is reserved at install time and registered as an ISO SR on first boot. Upload an image and build a VM without touching the command line."
  >}}
  {{< hextra/feature-card
    title="Signed, updatable in place"
    subtitle="Every ISO and RPM is signed with the XCP-hl GPG key, and a running host picks up updates from the project's yum repository."
  >}}
  {{< hextra/feature-card
    title="Pinned, not bleeding edge"
    subtitle="XOLite-hl and XOA-hl are pinned to known-good upstream revisions. Move to a more recent version only done after heavy testing, upstream changes cannot break your host."
  >}}
{{< /hextra/feature-grid >}}
