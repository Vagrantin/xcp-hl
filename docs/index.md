---
layout: home
title: Home
nav_order: 1
---

# XCP-ng Community Edition
{: .fs-9 }

A free, community-built XCP-ng ISO that replaces the official Xen Orchestra (Aka XOA)
with a fully **self-hosted** Xen Orchestra. The goal is to ease the deployment of
community-built XOA images, essentially targeting home-labbers.
{: .fs-6 .fw-300 }

[Download latest ISO](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/download/xcp-ng-ce-20260508-alpha2/xcp-ng-ce-8.3.iso){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/Vagrantin/xcp-ce){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is XCP-ng Community Edition?

[XCP-ng](https://xcp-ng.org/) is a powerful, open-source Type-1 hypervisor
based on the Xen Project. Officially it ships with **XO Lite**, a lightweight
in-browser management UI, and a one-click button that deploys the official
**Xen Orchestra Appliance (XOA)**.

**XCP-ng CE** keeps everything that makes XCP-ng great while replacing that
single button with a community-maintained workflow.
Once deployed you will be able to choose between 3 options to deploy XOA:
- Official Vates XOA image
- Ronivay's pre-built image
- Your custom image

One of the goals is to provide a stripped-down XOA image that removes banners
related to the lack of commercial support, as well as features that require a
Vates license — simplifying the XOA experience for home-labbers.

---

## Download

{: .note }
All ISO and RPM releases are signed with the **XCP-ng Community Edition GPG key**.
Verify your download before installing.

[⬇ Download ISO](https://github.com/Vagrantin/xcp-ce/releases/latest){: .btn .btn-primary }

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
gpg --verify SHA256SUMS.asc SHA256SUMS

# Verify the ISO
sha256sum -c SHA256SUMS
```

---

## Quick-start

### 1 · Install XCP-ng CE
Boot from the ISO. The installer is identical to upstream XCP-ng 8.3 —
follow the [official install guide](https://docs.xcp-ng.org/installation/install-xcp-ng/).

### 2 · Open XO Lite
After installation, point your browser at:

```
https://<your-host-ip>
```

Log in with your XCP-ng root credentials.

### 3 · Deploy XOA
In XO Lite, click **Deploy XOA**. The patched UI calls the bundled
[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) which streams the
community XOA image (`image.xva`) directly to XAPI.

### 4 · Connect XO to your host
Once the XOA VM has started, open it in your browser and add your XCP-ng host:

```
Settings → Servers → Add server
Host : <your-XCP-host-ip>
User : root
```

---

## Architecture at a glance

```
┌──────────────────────────────────────────────────────────────┐
│                    XCP-ng CE Host                            │
│                                                              │
│  ┌──────────────┐   patch   ┌──────────────────────────────┐ │
│  │  XO Lite CE  │ ────────► │  DeployXoaView (community)   │ │
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
| [`xcp-ce`](https://github.com/Vagrantin/xcp-ce) | Documentation |
| [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) | XO Lite community patch + RPM build |
| [`xcp-ng-ce-iso`](https://github.com/Vagrantin/xcp-ng-ce-iso) | ISO assembly pipeline and release |
| [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) | Rust HTTP/gzip proxy for XVA delivery + RPM build |

Full technical details in the [Developer section](developers/).

---

## License

XCP-ng CE is released under the **GNU General Public License v3.0**.
It builds on upstream XCP-ng (Apache 2.0 / GPL components) and Xen Orchestra
(AGPL-3.0).

> XCP-ng Community Edition is an independent community project.
> It is not affiliated with, endorsed by, or supported by Vates SAS or the
> XCP-ng project.
