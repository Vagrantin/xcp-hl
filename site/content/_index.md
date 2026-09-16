---
title: XCP-hl
layout: hextra-home
---

{{< hextra/hero-badge link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>Alpha · v8.3-ce9</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  Open virtualization,&nbsp;<br class="hx:sm:block hx:hidden" />no subscription
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  A community-built ISO based on upstream XCP-ng 8.3 that deploys a&nbsp;<br class="hx:sm:block hx:hidden" />
  self-hosted Xen Orchestra appliance — no phone-home, no licence gates.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-button text="Download the ISO" link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
{{< hextra/hero-button text="Read the documentation" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4);" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl is alpha software.** It is under active development and has not been
through a stabilisation cycle. **Expect breaking changes at every release:**
component versions, package names, repository layout and update behaviour can
all change, and an in-place update may require manual intervention on the host.
Run it on hardware and data you are prepared to rebuild from scratch.
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Drop-in XCP-ng 8.3"
    subtitle="The full upstream feature set — Xen 4.17, XAPI, Open vSwitch, live migration, HA, vGPU. The differences start above the installer."
  >}}
  {{< hextra/feature-card
    title="Your choice of XOA"
    subtitle="Deploy the HomeLab image, the official Vates appliance, Ronivay's build, or your own — picked from a selector in XO Lite instead of a single hard-wired button."
  >}}
  {{< hextra/feature-card
    title="No subscription banners"
    subtitle="XOA-HL strips the nag banners and the licence-gated menu items, leaving a Xen Orchestra that behaves like the open-source project it is."
  >}}
  {{< hextra/feature-card
    title="Ready-to-use ISO library"
    subtitle="A 20 GB partition is reserved at install time and registered as an ISO SR on first boot. Upload an image and build a VM without touching xe sr-create."
  >}}
  {{< hextra/feature-card
    title="Signed, updatable in place"
    subtitle="Every ISO and RPM is signed with the XCP-hl GPG key, and a running host picks up updates from the project's yum repository."
  >}}
  {{< hextra/feature-card
    title="Pinned, not bleeding edge"
    subtitle="XO Lite and Xen Orchestra are pinned to known-good upstream revisions. Pins move deliberately, after testing — upstream churn cannot break your host."
  >}}
{{< /hextra/feature-grid >}}
