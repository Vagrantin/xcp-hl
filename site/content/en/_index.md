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
  Virtualization for Everyone
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  XCP-hl brings XCP-ng 8.3 to your homelab, with a choice of Xen Orchestra deployments and integrated host and appliance update controls.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hero-actions hx:mb-6">
{{< latest-iso-download text="Download the ISO" shaText="SHA256 checksum" >}}
{{< hextra/hero-button text="Read the documentation" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
{{< hextra/hero-button text="XOA-HL manual" link="docs/xoa-hl/" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl is alpha software.** It is under active development and has not been
through a stabilisation cycle. **Expect breaking changes at every release.**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Based on XCP-ng 8.3"
    subtitle="Built on Xen 4.17, XAPI and Open vSwitch, with upstream host and VM management capabilities."
  >}}
  {{< hextra/feature-card
    title="Your choice of XO"
    subtitle="Deploy the hl image (XOA-hl, the administration WebUI), the official Vates appliance, Ronivay’s build, or your own image from XO Lite."
  >}}
  {{< hextra/feature-card
    title="Cleaned up menus"
    subtitle="XOA-hl simplifies Xen Orchestra with focused menus and integrated XCP-hl update controls."
  >}}
  {{< hextra/feature-card
    title="Ready-to-use ISO library"
    subtitle="On a suitable disk of at least 100 GB, a fresh install reserves a 20 GB ISO library and registers it on first boot."
  >}}
  {{< hextra/feature-card
    title="Signed, updatable in place"
    subtitle="Every ISO and RPM is signed with the XCP-hl GPG key, and a running host picks up updates from the project's yum repository."
  >}}
  {{< hextra/feature-card
    title="Pinned, not bleeding edge"
    subtitle="XO Lite and XOA-hl use fixed upstream revisions. Changes to those pins are deliberate; the release matrix records what each build shipped."
  >}}
{{< /hextra/feature-grid >}}

{{< legacy-home >}}
