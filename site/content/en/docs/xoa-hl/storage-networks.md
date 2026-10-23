---
title: "Manage disks, storage, ISO libraries and networks"
linkTitle: "Storage and networks"
description: "Add disks and network interfaces, connect NFS storage and ISO libraries, and create a VLAN."
weight: 50
translationKey: xoa-manual-storage-networks
translationStatus: source
sourceRevision: sha256:c439d8d2e5c6d454625769bceb1259e67e76e3291923ad9894e3a6f10bc9217b
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Add a disk or a network interface to a VM, connect NFS storage for ISO files or VM disks, and create a VLAN network. Practise on a stopped test VM, never on the appliance itself, signed in to the **XOA-HL appliance** as an administrator. Before you start, note the VM's ID, disks and network interfaces.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system.
{{< /callout >}}

## Know the objects {#objects}

| Object | What it is |
| --- | --- |
| SR | A storage repository: where virtual disks are stored. Check its free space |
| VDI | A virtual disk, stored in an SR |
| VBD | The link between a VM and one of its virtual disks |
| VIF | A VM's virtual network interface |
| PIF | A host's network interface. Changing the host's management network can cut you off from the host |

A VM's network interface is not the host's management interface. Choosing a network or generating a new MAC address does not isolate a VM. Before you connect a cloned or restored guest, check the actual VLAN, uplink and routing.

## Add a small blank disk {#add-disk}

1. Check that the test VM is stopped. Open **Disks** (`/#/vms/<id>/disks`) and select **New disk**.
2. Choose a writable SR in the same pool, a clear test name and a small size with its unit. Leave the read-only option off. Create the disk once and wait until it finishes.
3. Check the new row: name, size, SR and the VM it is attached to. Note the disk ID and the SR's remaining free space before you start the guest.

In the guest console, find the new disk by its size and device details. XO creates the disk and attaches it, but it does not partition, format or mount it inside the guest. That is a separate, operating-system-specific task. Never format a device based only on a guessed device name.

If creation fails, check the task and the VM and SR disk lists before you retry: a partial operation can leave a disk behind. Save the error, check free space and connectivity, and see [troubleshooting](/docs/xoa-hl/troubleshooting/) if needed. Shrinking, growing or moving disks is not covered here.

## Detach or delete a disk {#detach-vs-delete}

Removing the VBD detaches the disk from the VM, but its data (the VDI) still exists. Deleting the VDI destroys the data; that is a separate action, and this screen does not offer it while the disk is attached. Disconnecting an attachment is also different from removing it.

To clean up, stop the guest and identify the blank test disk with certainty. Keep the VDI if its content might still be useful. Never delete a boot disk, a shared disk or an unidentified disk to clear a space warning. [Back up valuable guest data](/docs/xoa-hl/backup-restore/) separately.

## Add an isolated network interface {#add-vif}

1. On the stopped test VM, open **Network** (`/#/vms/<id>/network`) and select **New device**.
2. Select a network in the same pool whose isolation you have checked. Leave the MAC address empty so it is generated, then select **Create**.
3. Before you start the VM, check the new interface, its network and its MAC address. After the start, check that the guest sees the interface and has the connectivity you planned.

To isolate a clone or a restored copy, remove **all** inherited VIFs while the VM is stopped, and check that the list is empty before the first start. Use the delete action, not just the connect toggle: a disconnected interface is not an isolated one. Add a test network only once you have confirmed that it cannot reach production, and resolved the copied guest identities.

If the VM can reach something unexpected, stop it, and check the selected network and the isolation outside XO before you retry. These steps do not configure host interfaces (PIFs), management addresses, bonds or VLANs, and you must not change the host management network while you follow them. For a VLAN on the hosts, see [Create a lab VLAN on a spare uplink](/docs/xoa-hl/storage-networks/#host-vlan-network). For other VM tasks, see [Manage VMs](/docs/xoa-hl/vm-operations/) or [Hosts and pools](/docs/xoa-hl/hosts-pools/).

## Connect an NFS ISO library {#nfs-iso-library}

An ISO SR holds installation media. It is different from a writable SR for VM disks, and from a backup destination. These steps connect an existing, dedicated NFS export that already holds an installer ISO checked against the vendor's checksum. The storage administrator prepares the export and places the file there; you only work in the browser and change nothing on the host.

**Before you start**

- Check whether the pool already has a suitable ISO SR. If its identity, host access and media are right, use it.
- For a new library, note the NFS server, the exact export path, the NFS version agreed with the storage administrator, the pool and hosts, and the ISO's file name and checksum.
- Every host that will read the ISO must be allowed to access the export. Access from your browser or from the appliance does not prove that the hosts can reach it.

1. As an administrator, open **New → Storage** (`/#/new/sr`). Choose a host in the pool. Enter a clear name such as `lab-nfs-iso` and a description that identifies the test export.
2. Under **ISO SR**, select **NFS ISO**. Do not select **NFS** in the **VDI SR** group: that creates VM-disk storage. **Local** means a folder on a hypervisor host, not on your computer or the appliance. Local, SMB and block storage are not covered here.
3. Enter the NFS server in **Server**. Choose the agreed NFS version (the form offers the default, `4` and `4.1`), then select the search icon next to the server. Changing the version does not search again, so search again after any change. Leave **Comma delimited NFS options** empty unless options were agreed.
4. Select the exact export in **Path**, using the export root (subfolders are not covered). Wait for the path check. If the export is missing, the check fails, or **Storage usage** lists existing SRs, stop and look at the error and the IDs. The wizard runs NFS checks even for an ISO library, so a detected SR is not necessarily an ISO library. Do not reattach it, and do not accept a warning about creating over existing storage.
5. In **Summary**, check the name and the selected type (`nfsiso`). Recheck the host, server and path above, then select **Create** once. If it fails, check the pool's SR list before you retry: a failed request can leave a partly created SR or host attachment.
6. Note the new SR's UUID. Its backend type is `iso` (`nfsiso` is only the wizard's choice). Open **Hosts** (`/#/srs/<id>/hosts`) and check that each host's attachment is connected and shows the right export. A shared SR does not prove that every host can reach it. Run VMs only on hosts whose access you checked.
7. Use the SR's **Rescan all disks** action, wait for it to finish, then open **Disks** (`/#/srs/<id>/disks`). Check the ISO's name and size. Rescan again whenever the storage administrator adds or replaces a file. Check the vendor's checksum at the source: a successful scan or a matching name does not prove that the file is intact.

**Check:** in the [new VM wizard](/docs/xoa-hl/create-vm/), choose the same pool and check that **ISO/DVD** offers the expected media. If it does, skip the browser upload. Reading existing media and uploading new media are different abilities: the import list does not prove that this SR accepts new ISO files. Never open up permissions broadly to make an upload work.

| Problem | What to check |
| --- | --- |
| No export found, or the path check fails | Note the error. With the storage administrator, check the server, path, NFS version, export discovery and host access. Stop if the wizard cannot find this export. |
| The SR exists but a host is disconnected | Check that host's attachment, path and access to the export. Another connected host is not enough. Do not disconnect all hosts to try a repair. |
| The scan works but the ISO is missing | Check that the complete file is on the agreed export, its name and size, and the selected SR. Fix the source, then rescan. Do not recreate the SR again and again. |
| The ISO is missing under ISO/DVD | Check the wizard's pool, that the SR is an ISO SR, that the media is there, and the host's attachment. An NFS SR for VM disks is not an ISO SR. |
| Creation fails, or an unexpected SR appears | Save the error and the list of SR UUIDs and attachments. Identify partial objects before any retry or cleanup. Never use Forget, Remove or formatting to make an unexplained error go away. |

Do not remove an ISO, or disconnect or forget its SR, while a VM uses it. Note which VMs use it and eject the media from the test guest before you plan any cleanup. Removing an SR and uploading ISOs are not covered here.

## Create NFS storage for VM disks {#nfs-vm-storage}

Use this when you need a **writable SR for VM disks**. An NFS ISO library holds installation media, and an NFS backup remote holds backups: neither is the SR you create here. Shared storage on its own is not a backup, and does not mean you are ready for migration or high availability (HA).

### Prepare a dedicated export

- Use an empty, dedicated lab export approved by the storage administrator, with room for a test disk and some spare space.
- Note the NFS server, the exact export root, the agreed version and options, the pool and every host that will use it.
- The storage administrator must allow read and write access from those hosts, and check the server's space and quotas.
- Do not reuse the ISO export, the backup destination or an export that holds unidentified data.

Sign in to the **XOA-HL appliance** as an administrator; creating and checking storage requires administrator rights on the selected host. Note the existing SRs first. If the storage already exists in the pool, check its UUID and host access instead of creating another SR. You do not need a VM to create the SR. If this will hold your first VM, create the SR and check it below, then [create and install the VM](/docs/xoa-hl/create-vm/) on it, and come back here for the disk test. Never use XOA-HL itself as the test VM.

### Create the SR and check it

1. Open **New → Storage** (`/#/new/sr`), choose a host in the pool, and enter a clear name such as `lab-nfs-vdis` and a description of the export. Under **VDI SR**, select **NFS**. Check that **NFS ISO**, under **ISO SR**, is not selected.
2. Enter the **Server**, choose the agreed **NFS version** (default, `4` or `4.1`), and select the server's search icon. Leave **Comma delimited NFS options** empty unless options were agreed. If you change the server or the version, search and choose the path again: changing only the version does not check the export again.
3. Select the exact export root in **Path**, without a subfolder, and wait for the check. Look at **Storage usage**. If an existing SR UUID or an entry in use appears, stop and identify it with the storage owner. Do not reattach it or create another SR on top of it. For NFS, XO does **not** ask you to confirm existing storage, so the absence of a warning does not prove that the export is empty.
4. In **Summary**, check the name, the type `nfs` and the path. Recheck the host, server, version and options above, then select **Create** once and wait. If it fails, check the SR and host attachment lists before you retry: a failed request can leave objects behind.
5. Note the new SR's UUID. On **General** (`/#/srs/<id>/general`), check `Type: nfs`, the size, the used and free space, and the pool.
6. Open **Hosts** (`/#/srs/<id>/hosts`). For each host, note its attachment (PBD) and check that it shows **Connected**, with the right `server` and `serverpath` (and `nfsversion` and `options` if you set them). One connected host does not prove that the others are. If an attachment is missing or disconnected, stop before you put VMs there. The status is also a button: read it without clicking it.

### Test a disk on the new SR

1. Follow [Add a small blank disk](#add-disk) on the stopped test VM, choosing this SR. Note the VM, disk and attachment IDs, and check the disk's SR and size.
2. Start the guest only on a host whose attachment you checked. Find the extra disk by its size and device details. Partitioning, formatting and mounting it need an operating-system-specific procedure and certain identification of the device.
3. If a guest administrator prepares this **test disk**, write a harmless sample file to it and note its checksum. Save your work, shut the guest down normally, start it again, and check the same disk, file and checksum.

**Check:** the file and its checksum are unchanged after the restart. An empty disk or a successful rescan does not prove that writes work or persist. Keep this result separate from a backup and restore test. Before you claim that the whole pool can use this storage, repeat the read and write test on each host through a separately approved placement or migration test.

### If something goes wrong

| Problem | What to check |
| --- | --- |
| No export, or the check fails | Save the exact error and the selected host, server, path and version. Ask the storage administrator to check discovery, host permissions and connectivity. Do not switch to local or block storage, or widen permissions, to get around it. |
| An existing SR is detected, or creation fails | Note every SR UUID and attachment, including partial objects. Find out who owns them and what uses them before any retry or reattachment. |
| Wrong type or path, or a host is disconnected | Stop new allocations. Compare the export you noted with each host's attachment. Do not disconnect all hosts or remove an SR to diagnose. |
| A space warning, or a write fails in the guest | Check the SR usage, the server's free space and quotas, running tasks and the exact disk in the guest. Keep the evidence and the data. Do not delete unidentified disks, snapshots or files on the NAS. |

To clean up, save the final list of objects and shut the test VM down normally. Apply [Detach or delete a disk](#detach-vs-delete) only to the test disk you identified with certainty. Keep the SR and the export until their owner has listed every user and recovery need. Destroying, forgetting or reattaching an SR, deleting NAS files and changing the default storage are not covered here, nor are local, SMB or iSCSI storage, NFS subfolders, outages, performance and pool-wide migration or HA.

## Create a lab VLAN on a spare uplink {#host-vlan-network}

This **changes the host and pool configuration**: it creates one tagged guest network from the **XOA-HL browser**. Use a test pool, a dedicated spare physical uplink and a stopped test VM. Keep a separate host console available the whole time.

**Before you start**

- Note the pool, its master and every host, with the existing network and PIF UUIDs, device names, MAC addresses, VLANs, MTU, management flags, IP modes and connection states.
- Have the network administrator approve the VLAN ID, the tagged switch ports, MTU `1500`, the guest addresses, and which destinations are allowed and forbidden.
- Check the spare uplink on **every** host: it carries no management, storage, backup or other traffic, has no host IP address, and is not part of a bond or an existing VLAN. Compare with the cabling and switch records; a device name, or a missing Management badge, is not enough.
- Stop if you cannot confirm this layout. A VLAN number alone does not isolate anything, and does not configure switch ports, routing, DHCP, DNS or firewalls.

### Create the network once

1. As an administrator, open **New → Network** (`/#/new/network`) and select the test **pool** (this requires pool administrator rights). Leave **Bonded network** and **Private network** off; Private network is a different, SDN feature.
2. Under **Info → Interface**, select the spare **PIF on the pool master** that you noted. The list shows master PIFs without a VLAN and hides bond members, but it **does** show management PIFs. Check the UUID, device and MAC against your records. Do not leave Interface empty: that creates a network with no uplink, not the VLAN you want.
3. Enter a clear **Name** and **Description** for the lab. Set **MTU** to `1500` and **VLAN** to the exact approved tagged VLAN ID. Do not leave VLAN empty or use `0`: an empty field is sent as `0`. Select **No NBD Connection**; this guest network does not need NBD.
4. Review the pool, master PIF, VLAN, MTU and both network type toggles, then select **Create network** once. Wait until it finishes and the pool's **Network** view (`/#/pools/<id>/network`) appears. If it fails, save the error and check the pool's networks and every host's PIFs before you retry. XO tries to clean up after a failed creation, but that does not prove every change in the pool was undone.

### Check every host

1. Copy the new network's UUID from its row in the pool view, and note its name, MTU and VLAN. That row's PIF and VLAN summary comes from the **master** only.
2. Expand **PIFs** and compare each host, device and MAC address with your records. The status icon there shows the **physical link (carrier)**. The **Connected** button on a host's Network tab shows whether the PIF is attached. Neither proves that tagged traffic flows. Do not click connect or disconnect just to read a status.
3. For each host, open **Network** (`/#/hosts/<id>/network`), find the new network's PIF, and note its UUID, device, MAC, VLAN, MTU, management badge, IP mode and address, and status. Check the exact approved VLAN, MTU `1500`, the attached state, the expected link, and that the host uses no IP address on it.
4. Compare management and storage connectivity with your starting notes.

If a PIF is missing, disconnected or unexpected, stop before you put a guest there. Do not edit existing VLAN, MTU or IP fields, or toggle the parent PIFs, to fix it.

### Check guest connectivity

1. On a stopped test VM, follow [Add an isolated network interface](#add-vif) and choose this exact network. Note the VM and VIF UUIDs, the MAC address, the network and the host the VM will run on. Check that no inherited interface bypasses the lab design.
2. Start the VM only on a host whose PIF you checked. The guest administrator sets up the agreed **untagged interface** and unique IP settings through the console. These steps do not set up a VLAN trunk inside the guest.
3. Check the guest's address, subnet, route and DNS separately. Test one approved peer or service, and the forbidden destinations that the administrator lists, including production. A failed ping does not prove isolation. Note the tests you ran and their results.
4. Shut the guest down normally, start it again, and repeat the checks.

**Check:** the guest reaches the approved peer, cannot reach the forbidden destinations, and keeps this after a restart; host management, storage and XOA-HL remain reachable throughout. A peer on the same host does not test the physical uplink or another host: traffic between hosts, and migration, each need their own approved test.

| Problem | What to check |
| --- | --- |
| The spare PIF is missing, or the pool is wrong | Check the master, the physical device, and bond or VLAN membership. Stop. Never pick a management or storage PIF, or change the pool, to get around the list. |
| An error, a duplicate network or PIFs missing on some hosts | Save the times, the error and the exact network and PIF UUIDs on every host. Review them with the owner before you retry. A notification does not prove that changes were undone. |
| The link is up but the guest has no expected traffic | Check the attached state, the VIF mapping, the guest's IP, route and DNS, the approved tagged switch path, and the peer and firewall. Never guess by changing the host management IP, the parent MTU or the VLAN. |
| Unexpected production access, or management or storage lost | Stop the test guest, keep the evidence, and use the separate host console with the network administrator's recovery plan. Make no other changes in the browser while the layout is uncertain. |

To finish, save the final records and shut the test VM down normally. Remove the identified test VIF only if the steps above require it. Keep the network, the PIFs and the switch configuration until their owner has listed every user and approved a removal and recovery plan. Deleting the network, editing VLAN or MTU, removing PIFs, bonds, moving the management network and host IP settings are not covered here. Changing the MTU of an existing network can unplug and replug its interfaces. See also [hosts and pools](/docs/xoa-hl/hosts-pools/), [troubleshooting](/docs/xoa-hl/troubleshooting/) and [Diagnose network connectivity](/docs/xoa-hl/troubleshooting/#network-connectivity).

{{< details title="Sources" closed="true" >}}
- **Disks and interfaces**: [disk UI and SR selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [VM interface UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [disk/interface actions](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **NFS storage and ISO libraries**: [new SR wizard](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js), [SR API/probes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs), [SR rescan action](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js), [host attachments](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js), [ISO import API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs), [new VM ISO selection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **SR capacity**: [XO5 `tab-general.js`](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js).
- **VLAN networks**: [VLAN wizard](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/network/index.js), [Network API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/network.mjs), [Pool VLAN creation/cleanup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [Pool network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [PIF carrier view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [Host network view](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [PIF/network fields](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [MTU operations](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/network.mjs).
{{< /details >}}
