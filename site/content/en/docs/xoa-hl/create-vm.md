---
title: Create and install your first virtual machine
description: Import an installer ISO, select storage and networking, and boot a new VM in XOA-HL.
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: source
sourceRevision: sha256:672451aeaca5fa92a966d3f969974ec5d8da3cae7c0e43f7276bc17d3f6a1b0b
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Create a small test VM, install its operating system and verify it boots from its own virtual disk.

{{< callout type="info" >}}
Preview procedure: checked against XO 5.113.2 (`e281c536`) with XOA-HL patches from image `xoa-image-20261009-5f33c81`. The disposable-lab run and guest-specific testing are pending. Resource sizes below are examples, not a supported-guest matrix.
{{< /callout >}}

## Before you begin

- [Log in and connect your host](/docs/xoa-hl/first-login/). This guide uses an XOA-HL administrator account.
- Download an installer ISO from your operating-system vendor and verify it using the vendor's published checksum.
- Identify an **ISO SR** for installation media and a **writable SR** with free space for VM disks. These have different purposes. Check [XCP-HL ISO library availability](/docs/features/#iso-storage); do not assume every host has that library.
- Choose a guest network with the connectivity the installer needs. Have enough free host RAM and storage while leaving capacity for XOA-HL and existing VMs.

Perform the management steps in the **browser**. The operating-system installation runs in the **new guest VM's console**, never on the XCP-HL host or XOA-HL appliance.

## 1. Import the installation ISO

1. In XOA-HL, open **Import → Disk** (`/#/import/disk`). Leave **From URL** off to upload the file you downloaded.
2. Select the **ISO SR**, for example `XCP-HL ISO library` when present. Drop the `.iso` file into the upload area.
3. Check the filename and destination, select **Import**, and wait for the operation to finish.
4. Check the destination SR's disks list for the ISO. Do not proceed with an incomplete upload.

If no suitable ISO SR appears, arrange an ISO repository before continuing. Importing installation media into ordinary VM-disk storage does not make it an ISO library.

## 2. Fill in the new VM wizard

Open **New → VM** (`/#/vms/new`) and select the intended **pool**. Select an installation template appropriate for your guest OS, rather than a template containing an already-installed guest.

Use a distinct name such as `lab-first-vm`. The following example suits a small Linux test installation only if its vendor requirements fit these resources:

| Wizard section | Choice and purpose |
| --- | --- |
| Info | Select the guest installation template, name and description. |
| Performance | Example: 2 vCPUs and 2 GiB RAM; increase these if your installer requires more. |
| Installation | Choose **ISO/DVD** and the imported installer ISO. |
| Interfaces | Select the guest network. Leave the MAC address empty for automatic generation unless your network design requires a fixed one. |
| Disks | Example: one 20 GiB disk on a writable SR accessible to the intended host. Do not select the ISO SR for the system disk. |
| Advanced | Leave template defaults unless the guest requires a documented change. For a deliberate first start, clear **Boot VM after creation**. |
| Summary | Review the pool, template, CPU, RAM, network and destination storage before creating one VM. |

Select **Create**. **Check:** a single VM with the chosen name appears and its configuration matches your choices. A disabled Create button means a required section or resource check is incomplete; review the wizard before retrying.

## 3. Install the operating system

1. Open the new VM, check its name, and start it. Open its **Console** tab.
2. Confirm the selected installer starts. Follow your OS vendor's installation instructions inside this guest.
3. When the installer asks for a target disk, check it is the **new VM's virtual disk**. The example creates a 20 GiB disk; any unexpected existing data is a reason to stop and recheck the selected VM.
4. After installation, use the VM's **Disks** tab to eject the installer ISO from the virtual CD drive. Reboot the guest normally and confirm it boots from its virtual disk.

{{< callout type="warning" >}}
Only operate on the new test VM. Formatting a disk or forcing a shutdown can lose data. Use the guest's normal shutdown/reboot path when it responds; do not stop the XOA-HL appliance or hypervisor to restart this guest.
{{< /callout >}}

## 4. Verify the result

- The guest boots without the installer ISO and you can log in through its console.
- The VM's CPU, memory, disks and network match your selections.
- Inside the guest, check the IP address, gateway, DNS and required connectivity. Console access is useful even when guest networking is not working.
- Record the guest OS version, template, VM name and installed XOA-HL versions. Guest tools and their installation procedure depend on the OS; this tutorial does not claim a tested guest-tools recipe.

The new VM is not yet protected by an independent backup. A snapshot on the same storage cannot protect you from losing that storage. Keep important data out of this test VM until a backup and restore have been verified.

## If something does not work

| Symptom | Check and next action |
| --- | --- |
| ISO missing from the wizard | Confirm the upload completed into an ISO SR and the selected pool/host can access it. |
| Create button disabled | Check the selected pool, template, name, resources, ISO, network and disk destination; complete every required section. |
| Creation or start fails | Read the displayed task error. Check host free RAM, writable SR free space and whether the selected storage and network are accessible to that host. Check whether a VM was already created before retrying. |
| Installer starts after every reboot | Eject the ISO from this VM's CD drive and check that the OS was installed on its virtual disk. |
| Guest has no network | Check the selected virtual network and the guest's IP, gateway and DNS. Avoid changing host management networking while diagnosing a guest. |

## Next step and sources

Keep the test VM for the forthcoming independent-backup and isolated-restore tutorial. Those chapters are tracked in [the beginner-journey issue](https://github.com/Vagrantin/xcp-hl/issues/197). Review the [glossary](/docs/xoa-hl/glossary/) and [update guide](/docs/guides/updates/) while those procedures are validated.

Source review at XO@e281c536: [ISO import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [VM wizard](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [VM tabs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) and [CD eject control](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js); [patch application at xoa-hl@5f33c81](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
