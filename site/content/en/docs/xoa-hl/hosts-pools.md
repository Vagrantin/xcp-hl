---
title: Manage hosts and pool ownership
description: Check connected inventory, move management ownership and inspect stale XOA markers.
weight: 24
translationKey: xoa-manual-hosts-pools
translationStatus: source
sourceRevision: sha256:a6577ca820beb79ac98cf82c2920df54641b60291785bb165ecbad082dfa96de
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Use an administrator account in the **XOA-HL appliance** and authorized host-console access. Record the appliance address, host/pool identities and existing management owner. Use [first login and host connection](/docs/xoa-hl/first-login/) for the initial connection.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. The XO Lite button review additionally covers `xolite-ce v0.21.0-ce29` (upstream `xo-lite-v0.21.0`). Ownership transfer and stale-marker lab tests remain pending.
{{< /callout >}}

## 1. Check the connected pool

Open **Settings → Servers** (`/#/settings/servers`). Check the expected connection is enabled and connected, and that inventory shows the intended host, pool, VMs and storage. A saved server entry is not evidence of a successful connection. If it fails, inspect its error and verify address, credentials and certificate handling through the [connection guide](/docs/xoa-hl/first-login/).

The supported management rule recorded in [#126](https://github.com/Vagrantin/xcp-hl/issues/126) is **one XOA managing a given host/pool**. Multiple appliances can technically connect, but simultaneous management is unsupported. This rule does not mean an appliance is limited to one pool. Coordinate ownership before adding a connection; never leave duplicate backup schedules managing the same guests.

## 2. Move management to another appliance

1. Arrange a window, finish active management/backup tasks and record the old owner's connections, schedules and destinations. [Export its configuration](/docs/xoa-hl/configuration-backup/) for safekeeping; exporting alone does not transfer or disable jobs.
2. Disable the old owner's relevant schedules. In its **Settings → Servers**, remove the connection for the pool before connecting the new owner. Do not remove a host from its pool or delete a VM to transfer XO management.
3. Add the host/pool connection on the new appliance. Check connected inventory and intended permissions. Recreate or restore settings only with the isolation and import precautions in the configuration guide.
4. Confirm the old owner no longer reconnects or runs jobs against the pool. Enable only the intended new schedules after checking destinations and performing an isolated recovery test.

If either appliance's state is unclear, pause the transfer and preserve connection/task errors. Multi-host pool creation, HA and live migration are outside this pilot; this procedure does not change pool membership.

## 3. Understand the XO Lite button

XO writes `xo:clientInfo:<appliance-uuid>` into the pool's `other-config`. With default settings, it marks on connection and every **6 hours**, removing markers older than **48 hours** during those marking passes. A read-only XO connection does not mark the pool. Removing a server connection stops future marking; it does not immediately remove the old marker.

In the reviewed XO Lite version, **Access XOA** uses the marker with the most recent `lastConnected`. It prefers `publicUrl`, otherwise the first address of `eth0` (or the first available interface), using HTTPS. It does not check that the VM or web service is running. When no address is found, it offers **Deploy XOA**. XO Lite does not itself expire a stale marker, so an old button can remain while no XO connects.

An obsolete address is not a reason to deploy a second manager. Check the known appliance address and ownership first. If a valid owner advertises the wrong address, inspect its URL/network configuration rather than repeatedly deleting its marker.

## 4. Inspect or remove one obsolete marker

On the **hypervisor host**, with root privileges, first run these read-only checks. Confirm the pool and exact obsolete key against your ownership record:

```bash
xe pool-list params=uuid,name-label
xe pool-param-get uuid='<pool-uuid>' param-name=other-config
```

Only after the old appliance's connection has been removed, record that marker's value and remove **that one key** if necessary. Replace both placeholders; never remove all `other-config` metadata:

```bash
xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
```

Repeat the read-only check and reload XO Lite. An active old owner can rewrite its marker on reconnect or its next marking pass. If the key returns, investigate the remaining connection. This cleanup changes discovery metadata, not pool membership, VM power or backup data, and has not been executed as part of this source review.

## Sources

XO 5 pin `e281c536`: [server UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [pool marking](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs) and [default intervals](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml). XO Lite source: [button address selection](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [community build and patch targets](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml). The support rule and targeted host cleanup come from [#126](https://github.com/Vagrantin/xcp-hl/issues/126).
