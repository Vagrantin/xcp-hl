---
title: "XCP-ng first-install walkthrough"
date: 2026-01-07T09:00:00+09:00
slug: xcp-ng-first-install
translationKey: blog-xcp-ng-first-install
---

The author's step-by-step first install of upstream XCP-ng 8.3, from the installer ISO to a deployed Xen Orchestra appliance, with photographs of the upstream installer.
{class="lead"}

{{< callout type="warning" >}}
This walkthrough describes **upstream XCP-ng 8.3**, not XCP-hl. XCP-hl is beta software built on XCP-ng 8.3, so installer labels and some defaults can differ in XCP-hl. The photographs below show the upstream 8.3 installer.
{{< /callout >}}

## About this page

This is the author's XCP-ng 8.3 first-install walkthrough, originally published on the author's personal blog on 2026-01-07 and migrated onto this site on 2026-11-11 per the owner decision recorded in [PR #409](https://github.com/Vagrantin/xcp-hl/pull/409), so the [getting started](/docs/start/) pages link it on the production domain. For the XCP-hl path (ISO download, checksum verification, XOA-hl appliance), follow [Getting started](/docs/start/).

## Before you begin

- A dedicated machine supported by XCP-ng 8.3, with hardware virtualization enabled; see the [upstream requirements](https://docs.xcp-ng.org/installation/requirements/).
- Back up any data on the disks you will use. **Installation erases the selected disks.**
- At least 100 GB on the installation disk, plus space for your VMs.
- A stable management IP address, gateway, DNS and NTP settings. A static address or a DHCP reservation makes the host easier to find.
- A second computer with a browser and network access to the host.

## Write the ISO to a USB drive

Download the XCP-ng 8.3 ISO from the [upstream download page](https://xcp-ng.org/download/), then write it to a USB drive. The write erases the USB drive, so first check with `dmesg` which device the USB drive is, and replace `sdX` below with that device:

```bash
sudo dd if=xcp-ng-8.3.0-20250606.iso of=/dev/sdX bs=8M oflag=direct
```

Double-check the device name before running the command: writing to the wrong disk erases it. Wait for the copy to finish; it can take a while depending on the USB drive.

## Install XCP-ng

XCP-ng is a type 1 hypervisor and is designed to be the only system installed on the machine. Plug in the USB drive, boot from it, and press Enter at the boot prompt.

1. **Select your keyboard layout**, then read the installation warning and the license agreement before continuing.

   {{< screenshot src="install/keyboard.jpg" alt="Installer keyboard layout selection" >}}

2. **Select the system disk and the disk for VM storage.** Check the device names and capacities; do not select the USB installer or a disk whose data you want to keep.

   {{< screenshot src="install/system-disk.jpg" alt="Selecting the system disk" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Selecting the disk for virtual machine storage" >}}

3. **Choose the storage type.** EXT (thin provisioning) uses only the space your data actually occupies: a 1 TB virtual disk holding 20 GB of data takes about 20 GB on the host, at the cost of growing the disk file as data is added. LVM (thick provisioning) reserves the full capacity up front and avoids that growth, at the cost of the space. EXT is a practical default for a homelab; LVM suits performance-sensitive workloads. You can extend the disk later from Xen Orchestra.

   {{< screenshot src="install/storage-type.jpg" alt="Choosing EXT or LVM storage" >}}

4. **Use Local media as the installation source**, and run the media verification when offered, particularly if you suspect a damaged download or USB drive.

   {{< screenshot src="install/source.jpg" alt="Selecting Local media as the installation source" >}}

5. **Set and store the root password.** This is the most important password on the platform; keep it in a safe place. You will use this account to sign in to XO Lite and to connect the host to Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Setting the host root password" >}}

6. **Configure management networking and DNS.** Use a static address or a DHCP reservation; use a VLAN only if your network requires it. Enter the hostname and reachable DNS servers. If the address changed later, you would need DNS in your lab to find the host again.

   {{< screenshot src="install/network.jpg" alt="Configuring the management IP address and gateway" >}}
   {{< screenshot src="install/dns.jpg" alt="Configuring the hostname and DNS servers" >}}

7. **Set the timezone and NTP servers, then review the installation.** Use public NTP servers if the host reaches the internet, or an internal NTP server if it does not. Confirm the selected disks before starting the installation.

   {{< screenshot src="install/ntp.jpg" alt="Configuring time synchronization" >}}
   {{< screenshot src="install/confirm.jpg" alt="Final installation confirmation" >}}

8. **Finish, remove the installation media, and reboot.** Note the management address shown on the host console.

   {{< screenshot src="install/complete.jpg" alt="Installation complete, ready to reboot" >}}

## After the first boot: XO Lite

The host console offers basic administration for this host only (network, VMs, resources, backup and restore). The other way to administer a single host is XO Lite, the web interface served by the host on the default HTTPS port: open `https://<your-host-ip>` (or `https://<hostname>`) in your browser. The host initially uses a self-signed certificate; confirm you are connecting to your own host before accepting it. Sign in as `root` with the password set during installation.

## Deploy XOA

XOA (Xen Orchestra) is the web application that administers one or more XCP-ng hosts and their VMs. It runs as a virtual machine on the host.

1. In XO Lite, click **Deploy XOA** and choose the appliance image. In XCP-hl the default choice is **XOA-hl**; see [Getting started](/docs/start/).
2. Fill in the network and deployment fields shown by the form, review the selected image and credentials, and click **Deploy**.
3. Wait for the appliance VM to start, then open its address in your browser and sign in. The appliance has its own address, different from the host's XO Lite address.

Once the host is connected in Xen Orchestra (`Settings → Servers → Add server`, with the host address and its root credentials), upload an installation ISO to the ISO library and create your first VM. The [upstream installation guide](https://docs.xcp-ng.org/installation/install-xcp-ng/) covers additional options.
