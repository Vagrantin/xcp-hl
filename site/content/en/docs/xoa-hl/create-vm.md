---
title: "Create your first virtual machine"
linkTitle: "Your first VM"
description: "Upload an installer ISO, create a VM and install its operating system."
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: source
sourceRevision: sha256:7ad93b382e01b5bcf49985b7bfa1aca1a167efcea5adc982557deeaf736346b8
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Create a small test VM, install its operating system and check that it starts from its own virtual disk.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261027-ca44911`, package `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Tested on a lab appliance on 2026-10-27 with one Linux guest; other guest systems need their own tests. The sizes below are examples, not a list of supported systems. Rebuilt on 2026-10-27 with the provisioning fix in `build-xoa-hl@fa0c987`. See [how to identify the fixed asset](/docs/xoa-hl/first-login/#identify-the-rebuilt-image). The export/import and VM-creation results recorded in [#315](https://github.com/Vagrantin/xcp-hl/pull/315) predate this rebuild. No repeat of those tests on the rebuilt asset is recorded here.
{{< /callout >}}

## Before you begin

- [Sign in and connect your host](/docs/xoa-hl/first-login/). This guide uses an XOA-HL administrator account.
- Download an installer ISO from the operating system vendor. Check it with the checksum that the vendor publishes.
- Find two kinds of storage: an **ISO SR** for installer media, and a **writable SR** with free space for VM disks. Not every host has the [XCP-HL ISO library](/docs/features/#iso-storage).
- Need a new SR for VM disks? First [create NFS storage on an empty, dedicated export](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Come back to its disk checks once this VM is installed.
- Pick a guest network that gives the installer the access it needs. Leave enough host memory and storage for XOA-HL and your other VMs.

You manage the VM in your **browser**. The operating system installs in the **new VM's console**, never on the XCP-HL host or the XOA-HL appliance.

## 1. Get the installer ISO

If a checked installer is already in an ISO library, use it and skip this step. To connect a dedicated NFS library, follow [Connect an NFS ISO library](/docs/xoa-hl/storage-networks/#nfs-iso-library).

Uploading from your browser only works if the ISO SR accepts new files and has enough space. Seeing the SR in the import list does not prove this: some libraries can read media but do not accept uploads.

1. Open **Import → Disk** (`/#/import/disk`). Leave **From URL** off, so that you upload the file you downloaded.
2. Select the **ISO SR**, for example `XCP-HL ISO library` if you have it. Drop the `.iso` file into the upload area.
3. Check the file name and the destination. Select **Import** and wait until it finishes.
4. Open the destination SR's disk list and check that the ISO is there. Do not continue with an incomplete upload.

If no suitable ISO SR appears, set one up first. Importing an ISO into ordinary VM-disk storage does not turn that storage into an ISO library.

## 2. Create the VM

Open **New → VM** (`/#/vms/new`) and select your **pool**. Choose a template that installs your operating system, not a template that already contains an installed system.

Give the VM a clear name, such as `lab-first-vm`. The sizes below suit a small Linux test system, if they meet the vendor's requirements:

| Wizard section | What to choose |
| --- | --- |
| Info | The installation template, a name and a description. |
| Performance | For example 2 vCPUs and 2 GiB of RAM. Add more if the installer needs it. |
| Installation | **ISO/DVD**, then the installer ISO. |
| Interfaces | The guest network. Leave the MAC address empty so that it is generated, unless your network needs a fixed one. |
| Disks | For example one 20 GiB disk on a writable SR that the host can reach. Never put the system disk on the ISO SR. |
| Advanced | Keep the template defaults unless the guest needs a documented change. Clear **Boot VM after creation** so that you start the VM yourself. |
| Summary | Check the pool, template, CPU, memory, network and storage. |

Select **Create**.

**Check:** one VM with your name appears, and its settings match your choices. If **Create** is greyed out, a required section or a resource check is incomplete. Review the wizard before you try again.

For console controls, or a blank or frozen screen, see [Use the VM console](/docs/xoa-hl/vm-operations/#vm-console).

## 3. Install the operating system

1. Open the new VM and check its name. Start it, then open the **Console** tab.
2. Check that the installer starts. Follow the vendor's installation steps inside this guest.
3. When the installer asks for a target disk, check that it is the **new VM's virtual disk** (20 GiB in this example). If the disk already contains data, stop and check that you selected the right VM.
4. When the installation is done, open the VM's **Disks** tab and eject the installer ISO from the virtual CD drive. Restart the guest normally and check that it starts from its virtual disk.

{{< callout type="warning" >}}
Only work on the new test VM. Formatting a disk or forcing a shutdown can lose data. If the guest responds, use its normal shutdown or restart. Never stop the XOA-HL appliance or the host to restart one guest.
{{< /callout >}}

## 4. Check the result

- The guest starts without the installer ISO, and you can sign in through its console.
- The VM's CPU, memory, disks and network match your choices.
- Inside the guest, the IP address, gateway, DNS and required connections work. The console still works when the guest network does not.
- You have noted the guest OS version, template, VM name and XOA-HL versions.

Guest tools depend on the operating system. For Ubuntu 24.04, see the next steps below.

This VM has no independent backup yet. A snapshot on the same storage does not protect you if that storage is lost. Keep important data off this VM until you have tested a backup and a restore.

## If something goes wrong

| Problem | What to check |
| --- | --- |
| The ISO is missing in the wizard | Check that the upload finished into an ISO SR, and that the selected pool or host can reach that SR. |
| **Create** is greyed out | Check the pool, template, name, resources, ISO, network and disk storage. Fill in every required section. |
| Creating or starting the VM fails | Read the task error. Check free host memory, free space on the SR, and that the host can reach the chosen storage and network. Before you retry, check whether a VM was already created. |
| The installer starts again after every restart | Eject the ISO from this VM's CD drive. Check that the system was installed on its virtual disk. |
| The guest has no network | Check the selected network and the guest IP address, gateway and DNS. Do not change the host management network to fix a guest. |

## Next steps

1. [Back up the test VM and check a restore](/docs/xoa-hl/backup-restore/).
2. For an Ubuntu 24.04 (amd64) guest, [install the management agent](/docs/xoa-hl/guest-tools/#install-linux-agent). Other systems need their own procedure.
3. To reuse an installed guest, [create new VMs from a template](/docs/xoa-hl/templates/#deploy-template).

See also the [glossary](/docs/xoa-hl/glossary/) and the [update guide](/docs/guides/updates/).

{{< details title="Sources" closed="true" >}}
Checked against XO@e281c536: [ISO import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [VM wizard](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [VM tabs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) and [CD eject control](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js); [patches applied in xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
