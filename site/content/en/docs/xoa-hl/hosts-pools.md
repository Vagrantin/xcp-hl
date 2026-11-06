---
title: "Manage hosts and pools: joining, statistics and host maintenance"
linkTitle: "Hosts and pools"
description: "Check which appliance manages a pool, read host statistics, and test pool joining, maintenance mode and HA on lab hosts."
weight: 60
translationKey: xoa-manual-hosts-pools
translationStatus: source
sourceRevision: sha256:6ade76bbc4328f8c9c50e11f0871e5809dda89e8f6f6c2d1fda8e5c6c988f73e
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Check which appliance manages each pool, move management to another appliance, clean up an old XO Lite button, read host statistics, and test pool joining, maintenance mode and high availability (HA) on lab hosts. Sign in to the **XOA-HL appliance** as an administrator, and keep approved access to the host console. Before you start, note the appliance address, the host and pool IDs and which appliance manages them today. For the first connection, see [first login and host connection](/docs/xoa-hl/first-login/).

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system. The XO Lite button section also covers `xolite-ce v0.21.0-ce29` (upstream `xo-lite-v0.21.0`).
{{< /callout >}}

## Check the connection and pool ownership {#connected-pool}

1. Open **Settings → Servers** (`/#/settings/servers`).
2. Check that the expected connection is enabled and connected.
3. Check that the inventory shows the intended host, pool, VMs and storage.

A saved server entry does not prove that the connection works. If the connection fails, read its error, then check the address, credentials and certificate handling with the [connection guide](/docs/xoa-hl/first-login/).

The supported rule, recorded in [issue #126](https://github.com/Vagrantin/xcp-hl/issues/126), is **one XOA manages a given host or pool**. Several appliances can technically connect, but managing the same pool from more than one is not supported. One appliance can still manage several pools. Agree on who manages a pool before you add a connection. Never leave duplicate backup schedules running for the same guests.

## Move management to another appliance {#move-management}

This moves pool ownership from an old appliance to a new one. It does not change pool membership. Never remove a host from its pool or delete a VM to move XO management.

1. Plan a time window. Let running management and backup tasks finish.
2. On the old appliance, note its connections, schedules and backup destinations.
3. [Export its configuration](/docs/xoa-hl/configuration-backup/) and keep the file safe. Exporting alone does not move or disable any job.
4. On the old appliance, disable the schedules that cover this pool.
5. In the old appliance's **Settings → Servers**, remove the connection to the pool. Do this before you connect the new appliance.
6. On the new appliance, add the host or pool connection. Check the connected inventory and the permissions you planned.
7. If you recreate or restore settings, follow the isolation and import precautions of the [configuration backup guide](/docs/xoa-hl/configuration-backup/).
8. Check that the old appliance no longer reconnects or runs jobs against the pool.
9. On the new appliance, check the backup destinations and run an isolated recovery test. Then enable only the schedules you planned.

**Check:** only the new appliance is connected to the pool and runs jobs for it.

If the state of either appliance is unclear, pause the move and save the connection and task errors. To merge hosts into one pool, see [Test pool joining](#pool-join).

## Understand the XO Lite button {#xo-lite-button}

Each connected appliance leaves a marker on the pool. XO Lite reads these markers to build its **Access XOA** button.

- XO writes the key `xo:clientInfo:<appliance-uuid>` into the pool's `other-config`. With the default settings, it writes it when it connects, then every **6 hours**. During each of these passes, it also removes markers older than **48 hours**.
- A read-only XO connection does not write a marker.
- Removing a server connection stops new writes, but does not remove the existing marker at once.
- **Access XOA** uses the marker with the most recent `lastConnected` value. It opens `publicUrl` if it is set, otherwise the first address of `eth0` (or of the first available interface), over HTTPS.
- The button does not check that the appliance VM or its web service is running. If XO Lite finds no address, it offers **Deploy XOA** instead.
- XO Lite does not expire old markers itself. An old button can stay even when no XO connects any more.

An old address is not a reason to deploy a second appliance. First check the known appliance address and which appliance manages the pool. If the right appliance shows the wrong address, check its URL and network settings instead of deleting its marker again and again.

## Remove an obsolete XO Lite marker {#obsolete-marker}

Do this only after you have removed the old appliance's connection (see [Move management to another appliance](#move-management)). It changes discovery data only: not pool membership, VM power states or backup data.

1. On the **hypervisor host**, as root, run these read-only commands:

   ```bash
   xe pool-list params=uuid,name-label
   xe pool-param-get uuid='<pool-uuid>' param-name=other-config
   ```

2. Compare the pool and the exact obsolete key with your records of which appliance manages the pool.
3. Note the value of that marker.
4. Only if you need to, remove **that one key**. Replace both placeholders. Never remove all of `other-config`:

   ```bash
   xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
   ```

5. Run the read-only commands again, then reload XO Lite.

**Check:** the key is no longer listed. If it comes back, an old appliance is still connected: it rewrites its marker when it reconnects or at its next pass. Find that remaining connection.

## Read host statistics {#host-statistics}

Reading statistics changes nothing on the host, its VMs, networks or storage.

**Before you start**

- Choose a known host that is connected and running. Note its ID, its pool, its number of CPUs and its memory size.
- This tab shows one host only. The pool overview and the appliance's own system monitor show something else.

1. Open the host's **Stats** tab (`/#/hosts/<id>/stats`). Check that it is the right host before you read any graph.
2. Start with **Last 10 minutes**, the default range. Note the range, the current time, your browser's time zone, the time of the latest sample shown and any task or connection error.
3. Wait for several sampling intervals and check that new data arrives. A graph that is still on screen does not prove that collection is current.
4. Choose a longer range to compare. XO requests **AVERAGE** samples, so one point on a long range can smooth out a short spike. Go back to the short range to look at recent changes.
5. Leave the **Stacked values** toggle off for a first reading of each series. Turn it on only to compare: it adds summed CPU and network series and can change the scale. Read the legend, the unit and the vertical scale each time.
6. Note a baseline during a known normal workload. Then compare a known busy period with the same host, range and settings. Note the series, the times, the sample spacing and the actual symptom.

Do not run a stress test in production, and do not resize, migrate or restart a guest just to make a graph move. A workload on a lab system needs its own operator approval.

| Range | Expected sample and refresh interval |
| --- | --- |
| Last 10 minutes | 5 seconds |
| Last 2 hours | 1 minute |
| Last day | 1 hour; last 24 hourly samples |
| Last week | 1 hour |
| Last year | 1 day |

A range name says how much history XO requests, not that the host kept all of it. Long ranges do not refresh every five seconds. Compare readings that use the same range and sample spacing. Note the times shown: the last point is not an instant reading.

| Graph | How to read it |
| --- | --- |
| CPU usage | Each `Cpu` series is a percentage. `All Cpus` is their sum, not a host percentage: four CPUs at 50% add up to 200%. Check the CPU count and the single series before you decide that the host is saturated. |
| Memory usage | Host total memory minus free memory, shown as a byte size. It is not a guest's memory limit or the free RAM an application sees. If free-memory data is missing, used memory can show as zero: check an unexpected zero another way. |
| Network throughput | Numbered `eth` series for receive (`rx`) and transmit (`tx`). Match them to the host's interfaces. Values are byte sizes. Conversion to Mbps or Gbps, bonds and VLANs are not covered here. A quiet series does not prove that the link or the guests' connectivity is healthy. |
| Load average | The host's separate `loadavg` metric. It is not a CPU percentage and not a measure of disk capacity. Compare it with CPU, memory, traffic and the actual workload. No general safe threshold is set here. |

**Check:** on the short range, the time of the latest sample keeps moving forward.

| Problem | What to check |
| --- | --- |
| **No stats.**, endless loading, gaps, or a flat or zero line | Note the host, range, time and error. Check the connection and that the host is running. Reload the page and choose the short range again. The tab does not fetch data for a host that is not running. After a failed fetch, waiting alone may not restart collection. Some missing samples become zeros. An empty graph or a zero does not prove that the host is idle or healthy. |
| Sample times still do not move | Use [troubleshooting](/docs/xoa-hl/troubleshooting/) and approved checks on the host itself before any capacity decision. Do not reset statistics or restart a production host to fix the graphs. |

Graphs alone do not show room for another VM, HA failover or a safe migration. Metric accuracy, full history, clock alignment, alerts, dashboard and pool totals, SR capacity and performance diagnosis are not covered here.

## Test pool joining with two lab hosts {#pool-join}

Joining moves a host into another pool. It **changes host membership** and can install missing patches. Practise only on two lab hosts that you can rebuild.

**Before you start**

- Use two lab hosts with a known release. The target is the master of a pool that contains only that host. The source is the only host of a different pool. A standalone host is a pool of one host.
- Keep separate console access to both hosts, a written recovery and rebuild plan, and one XOA-HL appliance that manages both connections.
- Do not use a production pool, a pool with HA, running guests, shared or attached workloads, or a host whose data has no independent backup.
- With the network and storage owners, agree on the join layout on the same network, DNS and time synchronization, separate management access and recovery through the host console. A network or SR with a similar name on each host is not necessarily shared.

1. In the **XOA-HL browser**, open **Settings → Servers**. Check that each of the two pools has one working connection.
2. Note both pool IDs, the target master and source host IDs, their product brand, version, build and patch level, management addresses, network and storage inventory, number of VMs and running jobs. Check that the source pool has no other host.
3. Stop the backup schedules of both pools for the time window. Keep their independent recovery points.
4. Open the **target pool** page (`/#/pools/<target-pool-id>/general`), identify the master and select **Add hosts**.
5. Select only the intended source host. The list hides hosts that belong to a pool with more than one host. It shows the patch differences in both directions.
6. Select **Cancel**, and sort out the cause outside this test, if either patch count is not zero, the brand or version differs, HA is on, a VM or SR on the source must be kept, or the join path is unclear. Do not use this dialog to install patches or to evacuate a host.
7. In the approved window, check the exact target pool and source host in the dialog, then select **OK** once. The UI sends `force: true`, which calls XAPI `pool.join_force`. This confirmation changes the pools: it is not a harmless compatibility check.
8. Wait for the task. After a successful join, the source connection should disappear and the target connection should refresh its inventory. The view can show as disconnected for a moment. Do not submit again just because a task or page has not refreshed.
9. Refresh the target connection. Check that the target pool ID and master are unchanged, that exactly the two expected host IDs belong to it, and that you can explain the state of the old source pool and its connection.
10. On each host, check the networks and PIFs, the SR attachments (PBDs) and management access. Check that the test storage and the isolated guest network work from the right hosts. Look for unexpected VMs, duplicate XOA connections, backup jobs or XO Lite markers.

**Check:** the target pool keeps its master and holds exactly the two expected hosts, and both hosts stay reachable from their consoles.

Note the before and after IDs, the patch-difference counts, the task result, console access and the result of each check. Keep the joined lab pool if it is the result you wanted. **Detach** ejects a host from its pool: it is a separate change, not an automatic rollback. Being in the same pool does not prove that migration or HA is safe.

**If the join fails**, save the task and error, the console state and both inventories. The server may already have applied patches or done part of the join. Stop and follow the host owner's recovery plan. Do not force another merge or eject a host. Removing a host later, HA, shared storage and live migration are not covered here.

## Test maintenance mode on a lab host {#host-maintenance-mode}

Maintenance mode disables a host and moves its running VMs to other hosts of the pool. Practise only on a lab pool that you can rebuild. This test does not install patches, restart a host or check availability during an update. For updates, see the [host update guide](/docs/guides/updates/#updating-xcp-hl-the-host).

**Before you start**

- Use a **two-host lab pool** with a known release, whose network and shared storage have already passed their own tests. Do not use a production workload, or a newly joined pool that you have not checked.
- The host you put in maintenance mode is **not the master**.
- Keep separate console and management access to both hosts, one XOA-HL appliance that manages the pool, and an approved recovery and rebuild plan.
- Use one test VM with a checked, independent recovery point. It must be the **only** ordinary VM on the source host. Its storage and guest network must be available on the other host.
- [Migration within the pool](/docs/xoa-hl/vm-transfer/) must already work for this VM. If you have not tested it, do that test first, then note the source host's state again. Stop if a requirement or the migration network is unclear.

1. In **XOA-HL**, note the pool, master and both host IDs, their versions and patch levels, enabled and power states, management addresses, where each VM runs, SR attachments (PBDs), networks and PIFs, free capacity on the target and running tasks.
2. Finish or pause backup and restore jobs.
3. Through an approved guest session, note how the test VM's application and network behave now. This is your baseline.
4. Open the source host's **Advanced** tab (`/#/hosts/<source-host-id>/advanced`). Check that the exact host and pool are shown.
5. Select **Enable maintenance mode**. The **Maintenance mode** dialog says that all running VMs will migrate to other hosts of the pool. In the approved window, select **OK** once. XO calls `host.setMaintenanceMode`, then XAPI disables the host and calls `host.evacuate`.
6. If a **Bypass blocked migrations** dialog appears, cancel it: that path removes the VMs' migration blocks.
7. Wait for the task result, then refresh the host and VM lists.
8. Check that the source host is disabled, that the test VM runs on the intended target, that no ordinary VM still runs on the source, and that the application and network match your baseline. Note the task, any error and console access.
9. On the same host's **Advanced** tab, select **Disable maintenance mode**. XO calls `host.enable`.
10. Check that the host is enabled, that both management paths and the SR and network attachments are healthy, and that the VM is still on the target.

**Check:** the host is enabled again and the test VM still runs on the target. Leaving maintenance mode does **not** move the VM back. Keep it on the target, or plan a separate, tested migration.

Do not use the host's **Disable** button, a forced restart, an emergency shutdown or a patch button instead of maintenance mode. Turn the backup schedules back on only after you check their scope and an isolated recovery point. Keep the before and after IDs, times, guest checks, task output, the actual host state and where each VM runs. A successful toggle, or pool membership alone, does not prove that the pool is ready for patches or HA.

**If evacuation fails**, stop: some VMs may already have moved. After an evacuation error, XO normally enables the host again, but a failure before that step can leave it disabled. Read the actual enabled state and where every VM runs, then follow the host owner's recovery plan. Do not repeat the toggle, bypass a block or restart the host to clear an unclear state.

## Check HA readiness on a lab pool {#ha-readiness}

When high availability (HA) is on, it can fence and restart a host if heartbeat communication fails. Test it only on a lab pool that you can rebuild. No host is failed on purpose here, and no VM restart is measured. Before you claim any availability, run a separate, approved failure test with a protected test VM.

**Before you start**

- Use a **three-host lab pool** with a known release, which you can rebuild and which has passed its own checks. Keep ordinary workloads off it.
- Manage the pool from one XOA-HL appliance that runs **outside** the pool. Keep the appliance and its access path outside the failure domain.
- Keep separate console and power access to each host, and an approved recovery plan.
- Read the [XCP-ng HA planning guide](https://docs.xcp-ng.org/management/ha/). It recommends three hosts and describes the network and storage heartbeat, capacity and fencing requirements. Check them against the actual XCP-HL host release.
- A two-host join, a successful migration or an SR with the same name does not prove that the pool is ready for HA.

1. In **XOA-HL**, note the exact pool, master and three host IDs, the host releases, management addresses and static management IPs, the current HA status, the VMs, running tasks and the one XOA-HL appliance that manages the pool.
2. Ask the storage and network owners to confirm a shared, writable heartbeat SR, attached and reachable on all three hosts. They also confirm healthy, redundant management and storage paths, and enough capacity for the protected guests after the loss of one host.
3. Note the SR ID and its attachments (PBDs), not just its name. If any requirement or console access is unclear, stop here: so far you have only read.
4. Open the pool's **Advanced** tab (`/#/pools/<pool-id>/advanced`). Look at **Heartbeat SR** and **High Availability**.
5. Turn on the **High Availability** toggle to open the **Enabling high availability** dialog. It lists the shared, writable SRs of this pool. Compare the candidate SR with your storage record. A listed SR does not prove host attachments, heartbeat reliability or failover capacity.
6. Select **Cancel** if the record or the recovery plan is incomplete. Never pick an SR just because the list shows it.
7. Only in an approved lab window, with every requirement met: open the dialog again, select the SR you noted and select **OK** once. XO calls `pool.enableHa`, which calls XAPI `pool.enable_ha`. Note the task and any error.
8. Refresh the pool. Check that **High Availability** is on, that the expected SR is listed under **Heartbeat SR**, that all three hosts are reachable, and that no unexpected VM or task appeared.
9. With the pool healthy and your notes saved, turn off **High Availability**. In the **Disabling high availability** dialog, select **OK** once. XO calls XAPI `pool.disable_ha`.
10. Check that HA is off, that all hosts and SR paths are healthy, and that any next work has its own approval.

**Check:** HA was turned on and off once each, with the expected heartbeat SR, and all three hosts stayed reachable.

While HA is on, the host and pool patch buttons are blocked. Do not start an update or a restart during this test. Keep the before and after pool, host and SR IDs, attachments, capacity assumptions, task output, console access and HA status.

**If enabling fails or a host is fenced**, save the console, task and HA logs, and follow the owner's recovery plan. If the pool is degraded, stop and follow the owner's incident procedure: the HA toggle is not a general recovery command. Do not repeat the toggle, restart a host toolstack or cause a network or storage fault to clear an unclear state.

{{< details title="Sources" closed="true" >}}
- **Host statistics**: [host tab and refresh handling](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js), [range selector and sampling intervals](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/stats.js), [host stats API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [RRD averages, metrics and cache](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs), [chart sums, scales and labels](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js), [memory calculation and byte formatting](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/utils.js).
- **Server connections and XO Lite button**: [server UI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [pool marking](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [default intervals](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [XO Lite button address selection](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [XO Lite CE build and patch targets](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml), [support rule and marker cleanup (issue #126)](https://github.com/Vagrantin/xcp-hl/issues/126).
- **Pool joining**: [target action](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/action-bar.js), [single-host picker and patch counts](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-hosts-modal/index.js), [force flag in the UI wrapper](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permission and merge API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [version and brand checks, patch work and sequential merge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/pool.mjs), [join and connection transition](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [XAPI join_force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs).
- **Host maintenance**: [Advanced tab and buttons](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-advanced.js), [confirmation and blocked-migration branch](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [maintenance API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [disable, evacuate, failure handling and enable](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [confirmation text](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **High availability**: [pool Advanced selector, heartbeat SR list and status](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-advanced.js), [pool API and permission](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [XAPI calls](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [XCP-ng HA planning guide](https://docs.xcp-ng.org/management/ha/).
{{< /details >}}
