---
title: Docker containers
weight: 5
translationKey: containers
---

Run Docker containers from XOA-hl in a dedicated VM, without touching the host or the appliance.
{class="lead"}

{{< callout type="warning" >}}
**Not released.** This guide describes a feature under development. No released XOA-hl image includes it. Follow [issue #7](https://github.com/Vagrantin/xcp-hl/issues/7) for its status.
{{< /callout >}}

## What you get {#what-you-get}

XOA-hl adds a **Containers** page for administrators. Containers run in a **Docker VM**: a normal VM, created from a prepared template, that only runs Docker.

- XCP-hl hosts and the XOA-hl appliance never run Docker themselves.
- A Docker VM is backed up, snapshotted, started and stopped like any other VM.
- Each container has a CPU limit and a memory limit, so one application cannot starve the others.

## Before you begin {#before-you-begin}

- Sign in to XOA-hl as an administrator.
- Import the Docker VM template into your pool and add the tag `xcp-hl-docker-template-v1` to it. The Containers page reminds you when no template is found.
- Use a network with DHCP that XOA-hl can reach. The Docker VM needs Internet access, or a registry on your network, to download images.

## Deploy a Docker VM {#deploy-a-docker-vm}

1. Open **Containers**. With no Docker VM yet, the page shows a short guide and the **Deploy Docker VM** form.
2. Enter a name, the number of vCPUs and the memory. With one template, a default storage and one network, the page selects them for you.
3. Select **Deploy Docker VM** once. The VM is created with its own 32 GiB disk and starts.
4. Wait a few minutes for the first start. Until the VM is ready, the page says so; do not deploy a second VM.

## Run a container {#run-a-container}

1. In **Create container**, enter a name and an image, for example `nginx:alpine`.
2. Keep or change the limits. The defaults are 1 CPU and 256 MiB.
3. Select **Create container**. An image that is not on the VM yet is downloaded first, then the container starts by itself. The download appears above the list until it ends.
4. Use **Start**, **Stop**, **Restart**, **Logs** and **Remove** on each container. Only a stopped container can be removed, and its volumes are kept.

**Advanced options** accept one entry per line:

| Field | Format | Example |
|---|---|---|
| Published ports | `HOST:CONTAINER/tcp` | `8080:80/tcp` |
| Persistent volumes | `NAME:/path` | `web:/usr/share/nginx/html` |
| Environment | `KEY=value` | `TZ=UTC` |

A published port is reachable at the address of the Docker VM, shown on the page. Do not put passwords in environment variables: other administrators and logs can show them.

## Follow usage on the Dashboard {#dashboard}

Once a Docker VM exists, the **Dashboard** shows a **Docker containers** card to administrators. For each Docker VM it gives the running and total containers, the load, the memory and disk in use, and the limits reserved by running containers.

The card highlights what needs attention: a Docker VM that is stopped or does not answer, a failed download, memory or disk nearly full, and reserved limits above the size of the VM.

## Limits and resources {#limits}

A limit is a ceiling for one container, not a reservation. The sum of the limits can exceed the VM; the page then warns you. Lower a limit, or give the Docker VM more vCPUs or memory from its VM page.

Disk space is shared by all images, containers and volumes of the Docker VM. Remove unused images under **Images** to free space.

## Back up and recover {#back-up-and-recover}

- Back up the Docker VM with a normal XOA-hl backup job. It contains the images, the containers and the volumes.
- Back up the XOA-hl appliance too. It holds the access keys of each Docker VM, and they cannot be recreated.
- After you delete a Docker VM, the page lists its keys under **Unused access keys**. Remove them only when the VM is really gone: a disconnected pool makes its Docker VMs look deleted.
- Updating XOA-hl does not update the Docker VM. Its system and Docker are maintained separately.

## Not in this version {#not-in-this-version}

No Compose files, no terminal inside a container, no privileged containers, no folders shared from the VM, and no stored registry passwords.

These choices keep the first version small and predictable.
