---
title: "Create and use VM templates"
linkTitle: "Templates"
description: "Turn a prepared VM copy into a template and create new VMs from it."
weight: 42
translationKey: xoa-manual-templates
translationStatus: source
sourceRevision: sha256:8311899f52c6c35acdf8506250a2785e49af7ba58544130a1bf8397652796909
glossaryTerms: ["backup", "pool", "sr", "vm"]
---

Turn a stopped copy of a VM into a template, then create two VMs from it and check that each one gets its own disks and data. The original VM stays unchanged.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. These steps reuse an installed disk: they do not prepare a guest operating system for wide reuse.
{{< /callout >}}

## Before you begin {#before-you-begin}

- Sign in to the **XOA-HL appliance** as an administrator. Converting a VM needs administrator rights on both the VM and its pool; access to the VM alone is not enough.
- Use a test guest that is already installed, with ordinary disks: no shared disks and no passthrough devices. Never convert the appliance or the original VM.
- Make a separate working copy with [Make a full copy in the same pool](/docs/xoa-hl/vm-operations/#full-copy). Note the UUIDs of the original and the copy, each disk's VDI ID, SR and size, and the checksum of a harmless sample file in the guest. Check that the copy starts in isolation, then shut it down normally.
- On the working copy, remove **all** network interfaces, eject the installer ISO, turn off automatic power-on, and keep it out of scheduled jobs.
- Keep enough host memory and writable SR space for the template and two test VMs.
- Have console access and the guest's login. Renaming a VM or changing its MAC address does not change the copied passwords, host name, IP settings, keys or application identities. Use these copies through the console only.

You work in the browser at the appliance address. File and checksum checks run in the **guest console**, not on the host or the appliance. A template on the same infrastructure is not a backup: keep your [backups](/docs/xoa-hl/backup-restore/) separately. For a fresh Ubuntu 24.04 guest, [install the guest tools](/docs/xoa-hl/guest-tools/) before you make the copy.

## Convert the stopped copy into a template {#convert-template}

1. Check the working copy: its UUID, the **Halted** state, an empty network interface list and the disks you noted.
2. Give it a unique name, such as `lab-template-v1`, and a description with the guest OS and version, the preparation date and the sample checksum. Refresh and check these values.
3. Open its **Advanced** tab (`/#/vms/<copy-uuid>/advanced`) and select **Convert to template**. The button works only when the VM is halted. The confirmation warns that the change is permanent: cancel if this is not the copy you meant.
4. Confirm once and wait until it finishes.
5. Open **Home** and choose the **Template** object type (`/#/home?t=VM-template`). Clear the filters if needed, expand the row and read the full UUID.

**Check:** the template has the **same UUID** as the working copy, with the name and description you set, and the original VM still exists. Converting does not copy the VM: the copy itself becomes the template.

Before it marks the VM as a template, XO tries to eject removable media. If that fails, earlier media changes can remain even though the conversion failed. Refresh the object type, the media and the task before you retry. Turning a template back into a VM, and automatic rollback, are not covered here.

## Create a stopped VM from the template {#deploy-template}

1. Open **New → VM** (`/#/vms/new`), choose the same pool and select your template. Name the VM `lab-template-test-1`. Check the `template=` UUID in the page address, not just the template's name.
2. Check the CPU, the memory, the template's disks, their sizes and their writable destination SRs. Keep the same disks and sizes.
3. In **Install settings**, choose **No config drive**. This test reuses the installed disk: it runs no installer and does not rely on cloud-init to change the guest's identity. If the disks or this option are missing, stop and check the selected template.
4. In **Interfaces**, remove every proposed interface and check that the list is empty. Even a template without interfaces can get the pool's default networks from the wizard.
5. In **Advanced**, clear **Boot VM after creation** and leave automatic power-on off.
6. In **Summary**, clear **Fast clone**. Check that you are creating one VM with the expected disks, resources and SRs, and **zero interfaces**. Then select **Create** once. The wizard turns on boot after creation and fast clone by default, so do not rely on earlier settings. Without fast clone, XO makes a full copy of the disks, which needs SR space.
7. Wait, refresh and note the new VM's UUID.

**Check:** before any start, the new VM is **Halted**, its Network tab is empty, and its disks have the expected count, sizes and SRs, with VDI IDs different from the template's and the original's. The template and the original still exist. A success message or a new name does not prove this. If an interface appeared or the VM started, stop it and check what it could reach before you continue.

## Check that each VM gets its own copy {#verify-deployments}

1. After the checks above, start only `lab-template-test-1`. In its [console](/docs/xoa-hl/vm-operations/#vm-console), check that the guest starts and that you can sign in, then check the disk layout and the sample checksum.
2. Change only the sample file to a new test value, note it, then shut the guest down normally.
3. Repeat [Create a stopped VM from the template](#deploy-template) from the **same template**, as `lab-template-test-2`. Check every setting again.
4. While it is stopped, check that it has a different VM UUID, different VDI IDs and no interfaces. Start it through its console and check that the sample still has its original checksum, not the new value from test 1. Shut it down normally.
5. Note both VMs' UUIDs and VDI IDs, the template UUID, the guest results and the installed versions. Leave the test VMs stopped.

**Check:** both guests start with the expected data, and the change in test 1 did not reach test 2. This file check does not test application recovery, and it does not remove duplicated operating system identities. Do not connect a production network until the guest owner has resolved them.

To clean up, [delete each test VM](/docs/xoa-hl/vm-operations/) once you have identified it. Keep the template, the original VM and your backups. For a new template version, prepare a new copy with a new versioned name and repeat these checks.

## If something goes wrong {#problems}

| Problem | What to check |
| --- | --- |
| The conversion is refused | Read the error, the VM and pool permissions and the actual power state. Do not force-stop a valuable guest, and do not convert an unidentified object again. After an error, check the object type and the removable media of the same UUID. |
| The template is missing | Choose the Template object type, the right pool and the right filters, then refresh. A template does not appear in the normal VM list. Do not make another copy before you have checked the inventory. |
| Creating the VM fails | Save the error and the list of templates, VMs and VDIs before you retry. XO tries to clean up after a failure, but a lost response or a failed cleanup can leave objects behind. Never bulk-delete disks that look orphaned. |
| The guest differs or does not start | Keep the template and the logs. Check the template UUID, the copied disks, the firmware and resources, and the install settings. Do not change the host management network to fix it. |

Changing a guest inside a template, retiring or deleting templates, deploying to another pool, fast-clone storage, cloud-init and operating-system-specific preparation are not covered here. If a problem remains, [report it](/docs/xoa-hl/troubleshooting/#report-a-problem) without sensitive data.

{{< details title="Sources" closed="true" >}}
- **Conversion**: [Advanced tab action, halted VMs only](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [confirmation dialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permissions, media, conversion and cleanup after a failed creation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **New VM wizard**: [template row identity](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/home/template-item.js), [wizard defaults and submitted settings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [disk copy and interface replacement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **HomeLab build**: [xoa-hl build script](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
{{< /details >}}
