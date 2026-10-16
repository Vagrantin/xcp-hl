---
title: Manage hosts — pool ownership and host statistics
description: Check ownership and XOA markers, then read host statistics with their sampling and freshness limits.
weight: 24
translationKey: xoa-manual-hosts-pools
translationStatus: source
sourceRevision: sha256:beb44b88bfe26bde42f94f6adbc46fcbe7eb8a679d9aa32b886a42a6541d8a75
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Use an administrator account in the **XOA-HL appliance** and authorized host-console access. Record the appliance address, host/pool identities and existing management owner. Use [first login and host connection](/docs/xoa-hl/first-login/) for the initial connection.

{{< callout type="info" >}}
Source-reviewed preview for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. The XO Lite button review additionally covers `xolite-ce v0.21.0-ce29` (upstream `xo-lite-v0.21.0`). Ownership transfer, stale-marker and host-statistics lab tests remain pending.
{{< /callout >}}

## 1. Check the connected pool

Open **Settings → Servers** (`/#/settings/servers`). Check the expected connection is enabled and connected, and that inventory shows the intended host, pool, VMs and storage. A saved server entry is not evidence of a successful connection. If it fails, inspect its error and verify address, credentials and certificate handling through the [connection guide](/docs/xoa-hl/first-login/).

The supported management rule recorded in [#126](https://github.com/Vagrantin/xcp-hl/issues/126) is **one XOA managing a given host/pool**. Multiple appliances can technically connect, but simultaneous management is unsupported. This rule does not mean an appliance is limited to one pool. Coordinate ownership before adding a connection; never leave duplicate backup schedules managing the same guests.

## 2. Move management to another appliance

1. Arrange a window, finish active management/backup tasks and record the old owner's connections, schedules and destinations. [Export its configuration](/docs/xoa-hl/configuration-backup/) for safekeeping; exporting alone does not transfer or disable jobs.
2. Disable the old owner's relevant schedules. In its **Settings → Servers**, remove the connection for the pool before connecting the new owner. Do not remove a host from its pool or delete a VM to transfer XO management.
3. Add the host/pool connection on the new appliance. Check connected inventory and intended permissions. Recreate or restore settings only with the isolation and import precautions in the configuration guide.
4. Confirm the old owner no longer reconnects or runs jobs against the pool. Enable only the intended new schedules after checking destinations and performing an isolated recovery test.

If either appliance's state is unclear, pause the transfer and preserve connection/task errors. This ownership transfer does not change pool membership. A separate two-host pool-join pilot follows; HA and live migration remain outside it.

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

## 5. Read host statistics {#host-statistics}

This observation exercise changes no host, VM, network or storage configuration. Use a known connected, running host and record its ID, pool, CPU count and memory capacity. Open that host's **Stats** tab (`/#/hosts/<id>/stats`); confirm the host identity before interpreting any graph. A pool overview or the appliance's own operating-system monitor has a different scope.

1. Start with **Last 10 minutes**, the default. Record the selected range, current time, browser time zone, latest displayed sample time and any task/connection error. Wait through several expected sampling intervals and check whether fresh data arrives. A graph still visible on screen is not proof that collection is current.
2. Compare a wider range using the selector. The reviewed backend requests **AVERAGE** samples; a long-range point can smooth a brief spike. Returning to the short range helps examine recent changes. The labels describe requested history, not a guarantee that the host has retained that entire period.

| Range label | Nominal sample / tab refresh interval |
| --- | --- |
| Last 10 minutes | 5 seconds |
| Last 2 hours | 1 minute |
| Last day | 1 hour; last 24 hourly samples |
| Last week | 1 hour |
| Last year | 1 day |

The long-range view is not expected to refresh every five seconds. Compare observations using the same range and sample spacing; record the displayed timestamps rather than treating the last point as an instantaneous reading.

3. Leave **Stacked values** off for an initial per-series reading, then compare it deliberately if needed. Read the legend, displayed unit and vertical scale each time; the toggle adds summed CPU/network series and can change the scale.

| Graph | Interpretation and limit |
| --- | --- |
| CPU usage | Individual `Cpu` series are percentages. `All Cpus` is their sum, not a normalized host percentage: four CPUs at 50% sum to 200%. Compare the CPU count and individual series before diagnosing saturation. |
| Memory usage | Host total minus free memory, displayed as a byte size. This is not a guest's configured memory limit or application-level free RAM. Missing free-memory data can render as zero used memory in this source; independently check an unexpected zero. |
| Network throughput | Examine numbered `eth` receive (`rx`) and transmit (`tx`) series and match them to the host's interface inventory. The graph uses byte-size labels; this pilot does not validate a conversion to Mbps/Gbps or coverage of bonds/VLANs. A quiet series does not prove link health or guest connectivity. |
| Load average | A separate host `loadavg` metric, not a CPU percentage or a direct measure of disk capacity. Correlate it with CPU, memory, traffic and the observed workload; no universal acceptable threshold is established here. |

4. Record a baseline during a known normal workload, then compare a known activity period using the same host/range/settings. Capture the affected series, times, sample spacing and actual symptom. Do not create a production stress test or resize/migrate/reboot a guest merely to make the graph move. An existing lab workload needs its own operator authorization.

If a chart shows **No stats.**, remains loading, has gaps or stays unexpectedly flat/zero, preserve the selected host/range, time and error. Check the connection and running state, then reload the page and reselect the short range. The reviewed tab does not fetch when the host is not running, and a failed fetch can leave its pending state set; waiting alone may not resume collection. Some missing samples can also become zeros during conversion. Neither an empty chart nor a zero is evidence of an idle or healthy host. If timestamps still fail to advance, use [troubleshooting](/docs/xoa-hl/troubleshooting/) and authorized independent host observations before making a capacity decision; do not reset statistics or reboot a production host as this exercise's recovery step.

This pilot covers reading host charts only. Installed metric accuracy, full history, clock alignment, alert thresholds/notifications, dashboard/pool aggregation, SR capacity and performance diagnosis remain separate acceptance work. The charts alone do not establish room for another VM, HA failover or a safe migration.

## 6. Rehearse joining one disposable host to a pool {#pool-join}

This **source-reviewed preview** applies to XO 5.113.2 in image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38`. It changes host membership and can install missing patches. Use two rebuildable, release-identified lab hosts only: the target is the master of an existing single-host pool, and the source is the sole host in a different pool. Keep independent console access, a recorded recovery/rebuild plan and one XOA-HL owner for both connections. Do not use an active production pool, HA, live guests, shared/attached workloads or a host with data that has no independent backup.

1. In the **XOA-HL browser**, check **Settings → Servers** for one working connection to each single-host pool. Record both pool IDs, target master and source host IDs, their product brand, version/build/patch level, management addresses, network and storage inventory, VM count and current jobs. Stop both sets of backup schedules during the window and retain their independent recovery points. A standalone host still has a one-host pool; verify that the source pool contains no other host. Arrange the network/storage owner’s approved same-network join topology, DNS/time synchronization, separate management reachability and host console recovery before changing membership. Do not assume a similarly named network or SR on each host is shared.
2. On the **target pool** page (`/#/pools/<target-pool-id>/general`), identify the master and open **Add hosts**. Select only the intended source host. The picker excludes hosts in pools with more than one host and shows patch differences in both directions. If either patch count is nonzero, the brand/version differs, HA is on, a source VM or SR requires preservation, or the join path is uncertain, **Cancel** and reconcile outside this exercise. Do not use this dialog as a patch-installation or evacuation shortcut. Source review shows the UI submits `force: true`, which calls XAPI `pool.join_force`; clicking confirmation is the state-changing boundary, not a harmless compatibility probe.
3. After the preflight record and an approved window, confirm the exact target pool and source host in the dialog and submit once. Expect the source connection to be unregistered after a successful join and the target connection to refresh its inventory; a transient disconnected view is possible. Do not repeatedly submit because a task or page has not refreshed. If the operation fails, preserve the task/error, console state and both inventories. The backend may already have performed patch work or part of a join; stop and follow the host owner’s recovery plan rather than forcing another merge or ejecting a host.
4. Refresh the target connection. Check that the target pool ID and master remain the intended ones, exactly two expected host IDs belong to it, and the separate source-pool/connection state is accounted for. Inspect each host’s network/PIF, SR/PBD attachment and management reachability, and verify that the intended test storage and isolated guest network are usable from the appropriate hosts. Check for unexpected VMs, duplicate XOA connections, backup jobs or XO Lite ownership markers. Do not infer a safe migration or HA capability from pool membership alone.

Record before/after IDs, patch-difference counts, the task result, host console reachability and each failed or successful check. Keep the joined lab topology if it is the intended result; do not treat **Detach/eject** as an automatic rollback, since it is a separate state-changing path. Installed join/patch/network/storage behavior, failure recovery, later host removal, HA, shared storage, live migration and human EN/FR/JA review remain pending.

## Sources

Host statistics at XO 5 pin `e281c536`: [host tab and refresh handling](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js), [range selector and sampling intervals](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/stats.js), [host stats API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [RRD averages/metrics/cache](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs), [chart sums/scales/labels](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js) and [memory calculation/byte formatting](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/utils.js).

XO 5 pin `e281c536`: [server UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [pool marking](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs) and [default intervals](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml). XO Lite source: [button address selection](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [community build and patch targets](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml). The support rule and targeted host cleanup come from [#126](https://github.com/Vagrantin/xcp-hl/issues/126).

Pool join at XO 5 pin `e281c536`: [target action](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/action-bar.js), [single-host picker and patch counts](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-hosts-modal/index.js), [force flag in UI wrapper](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permission and merge API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [version/brand checks, patch work and sequential merge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/pool.mjs), [join and connection transition](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [XAPI join_force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs).
