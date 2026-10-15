---
title: Create and reuse VM templates
description: Convert a stopped disposable copy into a template and verify two isolated deployments.
weight: 24
translationKey: xoa-manual-templates
translationStatus: source
sourceRevision: sha256:c7859c3ab668a7fcf3972680f3f5a0dacf530773f1cfa4a958b2bc49afc11c89
glossaryTerms: ["backup", "pool", "sr", "vm"]
---

Turn a prepared test copy into a reusable template, then create two separate VMs and check their disks and guest data. Keep the original VM unchanged.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2 (`e281c536`). Conversion and deployment on an installed appliance remain pending. This is an isolated lab pilot, not a tested guest OS generalization or production image recipe.
{{< /callout >}}

## Before you begin

- Use an XOA-HL administrator account and a disposable installed guest with ordinary disks, no shared disks or passthrough devices. Conversion requires administrative access to both the VM and its pool; a VM-only grant is insufficient.
- Follow the [stopped full-copy procedure](/docs/xoa-hl/vm-operations/#full-copy) to make a separate working copy. Record the original and copy UUIDs, disk VDI IDs/SRs/sizes and a harmless guest file checksum. Verify that the copy boots in isolation, then shut it down normally.
- Keep **all NICs removed** from the working copy, eject its installer ISO, disable its automatic power-on and exclude the lab objects from unattended jobs. Reserve host RAM and writable SR capacity for the template and two test deployments. Do not convert the appliance or the original VM.
- Have console access and the lab guest login. Copied guest credentials, hostnames, IP settings, keys and application identities are not sanitized by changing a VM name or MAC address. Keep these copies console-only. Guest-specific preparation, licensing, cloud-init and guest-tools validation need separate procedures before any wider reuse.

Management runs in the **browser at the appliance address**. File/checksum checks run inside the **guest console**, not on the host or appliance. A template on the same infrastructure is not an independent backup; preserve any required [backup and restore evidence](/docs/xoa-hl/backup-restore/) separately.

For a fresh Ubuntu 24.04 guest, use the separate [guest-tools pilot](/docs/xoa-hl/guest-tools/) before preparing a copy; keep the template exercise console-only.

## 1. Convert only the stopped working copy {#convert-template}

1. Recheck the working copy's UUID, **Halted** state, empty NIC list and recorded disks. Give it a unique name such as `lab-template-v1` and a description recording guest OS/version, preparation date and sample checksum. Refresh and verify these values before conversion.
2. Open its **Advanced** tab (`/#/vms/<copy-uuid>/advanced`) and choose **Convert to template**. This button is disabled unless the VM is halted. At ce38 the button and confirmation remain English in EN/FR/JA; the dialog warns that the operation is definitive. Cancel if this is not the disposable copy you intended to convert.
3. Confirm once and wait for completion. Open **Home** and select the **Template** object type (`/#/home?t=VM-template`). Clear filters as needed and expand the intended row to read its full UUID. Check that it is the recorded working-copy UUID and has the intended name/description. The original VM must still exist separately.

**Check:** the existing copy became a template with the **same UUID**. Conversion is not a copy operation and does not create a second VM. The source attempts removable-media ejection before setting the template flag; an ejection error can leave earlier media changes even when conversion fails. Refresh object type, media and task state before retrying. No UI conversion-back or automatic rollback procedure is established here.

## 2. Create a stopped VM from that template {#deploy-template}

1. Open **New → VM** (`/#/vms/new`), choose the same pool and select the recorded custom template. Use a distinct name such as `lab-template-test-1`; verify the `template=` UUID in the resulting URL, not just its label.
2. Review CPU/RAM and the existing template disks, their sizes and writable destination SRs. Keep the expected disk set and sizes for this pilot. Choose **No config drive** in Installation; this test reuses the installed disk rather than running an installer or assuming cloud-init changes guest identity. If the expected existing disks or this option are absent, stop and recheck the selected template.
3. In **Interfaces**, remove every proposed interface and check that the list is empty. A template with no NICs can still receive wizard defaults from the pool's networks. The backend removes cloned VIFs, then creates the interfaces submitted by this form; that is not a guarantee of an isolated result.
4. In **Advanced**, clear **Boot VM after creation** and leave automatic power-on off. In **Summary**, clear **Fast clone**, review one VM, the disk count, resources, destination SRs and **zero interfaces**, then choose **Create** once. The wizard initially enables boot-after-create and fast clone; do not rely on remembered settings. With fast clone off, this disk-template path requests a full copy; it still needs capacity and does not establish an independent backup.
5. Wait, refresh and record the new VM UUID. Before any start, verify **Halted**, an empty Network tab, expected disk count/sizes/SRs and VDI IDs distinct from the recorded template/original disks. Check that the template and original still exist. If a NIC appeared or the VM started, stop the copy and investigate exposure before proceeding.

**Check:** a separate, stopped, disk-backed VM exists with no NICs. A success notification or a new name alone does not prove the intended resources or guest preparation.

## 3. Verify isolated, repeatable deployment

1. Start only `lab-template-test-1` after the isolation readback. Use its [console](/docs/xoa-hl/vm-operations/#vm-console) to verify guest boot/login, disk layout and the recorded sample checksum. Change only that harmless sample to a distinct test value, record it, then shut down normally.
2. Repeat section 2 from the **same template** as `lab-template-test-2`, reviewing every setting again. Verify a different VM UUID, separate VDI IDs and an empty NIC list while stopped. Boot through its console and check that its sample still has the original checksum, not test-1's changed value. Shut it down normally.
3. Record both VM/VDI inventories, template UUID, guest results and installed release identities. Leave the test VMs stopped. When finished, follow [identified disposable-VM removal](/docs/xoa-hl/vm-operations/) for each test VM only, preserving the template, original VM and required backups.

**Check:** both isolated guests boot with the intended data, and changing test-1 did not change test-2's initial sample. This small file check is not application recovery, OS identity generalization or a supported guest matrix. Do not attach a production network until the guest owner has separately resolved duplicated identities and validated its preparation process.

## If something does not work

- **Conversion refused:** read the error, VM/pool permissions and actual power state. Do not force-stop a valuable guest or repeatedly convert an unidentified object. Recheck the same UUID's type and removable media after an error.
- **Template missing:** select the Template object type, correct pool and filters, then refresh. Do not infer deletion from the regular VM list or create another copy before reconciling inventory.
- **Creation failed:** preserve the error and template/new VM/VDI inventory before retrying. The source registers failure cleanup, but a lost response or cleanup failure is not proof that all created objects disappeared. Never bulk-delete apparent orphan disks.
- **Guest differs or does not boot:** retain the template and logs, verify template UUID, copied disk set, firmware/resources and selected configuration method. Do not count the pilot as passed or change host management networking to repair it.

For a later template revision, prepare a new disposable copy with a new versioned name and repeat the isolated checks. In-place guest maintenance, template retirement/deletion, cross-pool deployment, fast-clone storage behavior, cloud-init and OS-specific sanitization remain separate acceptance gaps. Keep unresolved results and [report sanitized evidence](/docs/xoa-hl/troubleshooting/#report-a-problem).

## Sources

XO at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`: [halted-only Advanced action](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [English confirmation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [conversion permissions/media/type and creation cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [template row identity](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/home/template-item.js), [wizard defaults and submitted settings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [disk copy and VIF replacement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs). HomeLab patch/build selection: [xoa-hl at `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
