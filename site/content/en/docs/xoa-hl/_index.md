---
title: XOA-HL manual
weight: 3
translationKey: xoa-manual-home
translationStatus: source
sourceRevision: sha256:17789bad31865209a5a33c733b7d4a25e8d47e3842943b19b91db3302a2e0aac
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Find your next task in the XOA-HL documentation. Start with deployment, then keep the appliance and the hypervisor host up to date.

{{< callout type="info" >}}
The beginner journey is available as a source-reviewed preview: deployment, first login, VM creation, full backup and isolated restore. Disposable-lab acceptance and human translation review are pending. Maintenance, configuration export and troubleshooting are also available as source-reviewed previews; recovery and rollback acceptance remain pending.
{{< /callout >}}

## Start here

- [Log in, connect a host and choose your language](/docs/xoa-hl/first-login/).
- [Create and install your first virtual machine](/docs/xoa-hl/create-vm/).
- [Back up a VM and test an isolated restore](/docs/xoa-hl/backup-restore/).
- [Deploy XOA-HL and connect your host](/docs/start/#start-deploy-xoa).
- [Understand the host, XO Lite and the appliance](/docs/start/#start-architecture).
- [Check what each release shipped](/docs/reference/release-matrix/).

XOA-HL has its own address. Use the appliance address for Xen Orchestra and the host address for XO Lite. The management interface and this documentation have separate language settings.

## Daily administration

- [Operate and resize a VM, use snapshots, clone and understand deletion](/docs/xoa-hl/vm-operations/).
- [Add a test disk and manage VM network interfaces](/docs/xoa-hl/storage-networks/).
- [Migrate a VM within its pool, export it and import an isolated copy](/docs/xoa-hl/vm-transfer/).
- [Check host/pool ownership and XO Lite discovery](/docs/xoa-hl/hosts-pools/).
- [Create a user and verify object permissions](/docs/xoa-hl/permissions/).

These are source-reviewed previews with disposable-lab checks still pending. For protection, use the [full backup and isolated restore pilot](/docs/xoa-hl/backup-restore/); other backup/DR modes need separate release-scoped acceptance.

## Maintain your installation

- [Plan appliance maintenance and check its result](/docs/xoa-hl/maintenance/).
- [Export XO configuration and plan an isolated import test](/docs/xoa-hl/configuration-backup/).
- [Troubleshoot and report a problem](/docs/xoa-hl/troubleshooting/).
- [Update the XOA-HL appliance](/docs/guides/updates/#updating-xoa-hl-the-appliance).
- [Update the hypervisor host](/docs/guides/updates/#updating-xcp-hl-the-host).
- [Read release changes](/docs/reference/changelog/).

Check the release applicability in a guide before following it. A release matrix records what shipped together; it does not replace integration-test results.

## Reference and automation

- [Understand concepts, versions and feature scope](/docs/xoa-hl/concepts/).
- [Configure the appliance service](/docs/xoa-hl/configuration/).
- [Discover API methods and read inventory with xo-cli](/docs/xoa-hl/automation/).

## Learn the terms

[Open the glossary](glossary/) for VM, host, pool, storage, snapshot and backup terminology. For implementation details, use the [contributor component pages](/docs/components/).

## Language and page feedback

Use the language selector to open the same page in English, Français or 日本語. [Check the translation status](translation-status/) before relying on a draft translation.

[Report a documentation problem](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Include the page URL, selected language, appliance version and the step that needs correction. Do not include passwords or private data.
