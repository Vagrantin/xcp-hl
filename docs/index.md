---
layout: home
title: Home
nav_order: 1
---

# XCP-ng HomeLab Edition
{: .fs-9 }

A free, community-built XCP-ng ISO that replaces the official Xen Orchestra (Aka XOA)
with a fully **self-hosted** Xen Orchestra. The goal is to ease the deployment of
community-built XOA images, essentially targeting home-labbers.
{: .fs-6 .fw-300 }

> ### ⚠️ Alpha software
>
> **XCP-ng HomeLab Edition is in alpha.** It is under active development and has
> not been through a stabilisation cycle. **Expect breaking changes at every
> release**: component versions, package names, repository layout and update
> behaviour can all change, and an in-place update may require manual
> intervention on the host.
>
> Run it on hardware and data you are prepared to rebuild from scratch. Bug
> reports and feedback are welcome on
> [GitHub](https://github.com/Vagrantin/xcp-hl/issues).

[Download latest ISO](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/Vagrantin/xcp-hl){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is XCP-ng HomeLab Edition?

[XCP-ng](https://xcp-ng.org/) is a powerful, open-source Type-1 hypervisor
based on the Xen Project. Officially it ships with **XO Lite**, a lightweight
in-browser management UI, and a one-click button that deploys the official
**Xen Orchestra Appliance (XOA)**.

**XCP-ng HL** keeps everything that makes XCP-ng great while replacing that
single button with a community-maintained workflow.
Once deployed you will be able to choose between 3 options to deploy XOA:
- XOA image for home labber (default)
- Official Vates XOA image
- Ronivay's image ( bleeding edge )
- Your custom image

One of the goals is to provide a stripped-down XOA image that removes banners
related to the lack of commercial support, as well as features that require a
license — simplifying the XOA experience for home-labbers. This image,
**XOA-HL**, is built from the [`xoa-hl`](https://github.com/Vagrantin/xoa-hl)
and [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) repositories.

For stability and maintainability, both patched components are **pinned to
a specific upstream version**: building against upstream `master` is too
risky, with a high chance of breaking the builds every time upstream moves.
XO Lite HL is built from a fixed upstream tag (currently `xo-lite-v0.21.0`)
and XOA-HL from a fixed Xen Orchestra commit (currently `5.113.2`, the last
XO 5.x release) — for now, **XOA-HL defaults to the XO v5 web UI, not
XO v6**. Pins are only bumped deliberately, after testing, so upstream
changes can never break existing deployments. The exact versions shipped
with each release are recorded in the [Release Matrix](/release-matrix/).

---

## Download

{: .note }
All ISO and RPM releases are signed with the **XCP-ng HomeLab Edition GPG key**.
Verify your download before installing.

[⬇ Download ISO](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest){: .btn .btn-primary }

### Verify the ISO

The community GPG key is published on [keys.openpgp.org](https://keys.openpgp.org).

| Property | Value |
|---|---|
| Key file | `xcp-ng-ce-public.asc` (attached to each release) |
| Email | `xcp-ng-ce.lid530@passmail.com` |
| Fingerprint | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |

```bash
# Option 1 — fetch from keyserver
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# Option 2 — import from the release page
gpg --import xcp-ng-ce-public.asc

# Verify the ISO checksum file signature
# (checksum files are named after the ISO — example for v8.3-ce9)
gpg --verify xcp-ng-8.3-ce9.iso.sha256.asc xcp-ng-8.3-ce9.iso.sha256

# Verify the ISO
sha256sum -c xcp-ng-8.3-ce9.iso.sha256
```

---

## Quick-start

### 1 · Install XCP-ng HL
Boot from the ISO. The installer is identical to upstream XCP-ng 8.3 —
follow the [official install guide](https://docs.xcp-ng.org/installation/install-xcp-ng/).

### 2 · Open XO Lite
After installation, point your browser at:

```
http://<your-host-ip>
```

Log in to XO Lite with your XCP-ng root credentials.

### 3 · Deploy XOA
In XO Lite, click **Deploy XOA**. Fill in the required information, (IP, user, password, etc )
When you trigger the deployment, XO Lite calls the bundled [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) which streams the
XOA image (ie `image.xva.gz`) directly to XAPI. More details on this in the Developers/xoa-proxy section.

### 4 · Connect XO to your host
Once the XOA VM has started, open it in your browser and add your XCP-ng host:

```
Settings → Servers → Add server
Host : <your-XCP-host-ip>
User : root
```

### 5 · Keep it up to date
XCP-HL ships its components as signed RPMs, so a running host updates in place.
Available updates appear in Xen Orchestra under
`Home > Hosts > <your host> > Patches`. See [Updates](updates.html) for how
that works, how to bootstrap an older host, and how to roll back.

---

## Architecture at a glance

```
┌──────────────────────────────────────────────────────────────┐
│                    XCP-ng HL Host                            │
│                                                              │
│  ┌──────────────┐   patch   ┌──────────────────────────────┐ │
│  │  XO Lite HL  │ ────────► │  DeployXoaView (community)   │ │
│  │              │           │                              │ │
│  └──────┬───────┘           └───────────┬──────────────────┘ │
│         │                               │ HTTP               │
│  ┌──────▼───────────────────────────────▼──────────────────┐ │
│  │                   xoa-proxy                             │ │
│  │       HTTP · HTTPS · gzip · streaming XVA delivery      │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │ XAPI VM.import                 │
│  ┌──────────────────────────▼──────────────────────────────┐ │
│  │                   XAPI / Dom0                           │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Components

| Repository | Role |
|---|---|
| [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) | Documentation |
| [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) | XO Lite community patch + RPM build |
| [`xcp-ng-ce-iso`](https://github.com/Vagrantin/xcp-ng-ce-iso) | ISO assembly pipeline and release |
| [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) | Rust HTTP/gzip proxy for XVA delivery + RPM build |
| [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) | HomeLab-patched Xen Orchestra appliance (XOA-HL) — simplified UI, RPM + container build |
| [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) | Packer pipeline that builds the XOA XVA image on XCP-ng and publishes it as a release |
| [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) | Rust build orchestrator — triggers, monitors and diagnoses all component builds daily |

Full technical details in the [Developer section](developers/).

---

## License

XCP-ng HL is released under the **GNU AFFERO GENERAL PUBLIC LICENSE v3.0**.
It builds on upstream XCP-ng (Apache 2.0 / GPL components) and Xen Orchestra (AGPL-3.0).

> XCP-ng Home lab Edition is an independent community project.
> While being downstream, it is not affiliated with, endorsed by, or supported by Vates SAS or the
> XCP-ng project.
