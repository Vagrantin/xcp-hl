---
layout: default
title: Docker containers (draft)
nav_order: 90
---

# Dedicated Docker VM management (draft, protocol v1)

Tracking: [xcp-hl#7](https://github.com/Vagrantin/xcp-hl/issues/7).
This source targets `UPSTREAM_XO` at `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`.
It is an alpha implementation in draft PRs, not a released feature.

The Containers page in XO 5 manages a separate AlmaLinux 9 VM. It does not
install Docker on XOA-HL or on the XCP-ng host. Each Docker VM can run several
containers. Normal VM operations, console access and backups stay on XO's
existing VM pages. The page is administrator-only, as is every `containers.*`
API method.

## First setup

1. Use the Docker host template CI workflow described in
   [build-xoa-hl/docker-host/README.md](https://github.com/Vagrantin/build-xoa-hl/tree/vibe/container-support-27a085/docker-host).
   The normal XOA image builder is a separate path. No workstation image build is required.
2. Import the resulting XVA through XO into the desired pool. If imported as a
   VM, convert it to a template. Add the exact tag `xcp-hl-docker-template-v1`.
   Do not boot this clean template before converting it.
3. Install the XOA-HL RPM built from the companion draft PR in a QA environment.
   It includes the Containers page and declares `openssh-clients` as a runtime
   dependency. There is no additional Docker package on XOA-HL.
4. Ensure DHCP and IPv4 connectivity from XOA-HL to TCP 22 on the guest network.
   Internet access is needed by CI for packages, and by the guest for registry
   pulls. Local/private registries with anonymous pulls can also be used.

## Deploy and use

1. Open **Containers → Deploy Docker VM**. Choose template, storage and network
   in the same pool, then the name, vCPUs and RAM (minimum 1 GiB). The system disk
   is a full copy of the template, initially 32 GiB. Copying requires adequate
   free storage; provisioned memory and vCPUs must fit the pool. XO/XAPI perform
   their normal VM placement checks.
2. Submit once. XO creates and starts the guest asynchronously, using its
   existing `vm.create` code path. If boot fails, inspect the existing VM's Tasks
   and console and start that VM again. A deployment response is **not** proof
   that the guest has finished booting.
3. Select the Docker VM. Wait for guest tools, DHCP and cloud-init. Refresh
   reports connection or identity failures explicitly, and links to the VM
   console. Do not deploy duplicates while waiting.
4. Pull an image, for example `nginx:alpine`. Then create a container with a name,
   image and mandatory CPU/memory limits. `8080:80/tcp` publishes nginx on port
   8080 of the **Docker VM**. Firewall/segmentation rules for application ports
   belong on the surrounding network; Docker-published ports must not be assumed
   to obey ordinary guest firewall INPUT rules.
5. Optional advanced fields accept one mapping per line: ports
   `8080:80/tcp` or `5353:5353/udp`, volumes `web:/usr/share/nginx/html`, and
   environment `TZ=UTC`. Named volumes have an `xoa-hl-` prefix and are shared
   by name within the VM. Avoid environment secrets: XO administrators and API
   audit/debug logs can expose request values.
6. Start, stop, restart, read logs, or remove stopped containers. Removal is
   confirmed, has no force flag, and preserves named volumes. Docker refuses
   removal of an image that is in use. The UI manages only containers labelled
   `net.xcp-hl.managed=1`; containers created manually are not silently adopted.

The page refreshes every five seconds, without overlapping an operation. Pulls
can take up to four minutes; during an operation other actions for that guest
are serialized. Logs are snapshots of 200 lines within 24 hours, capped at
64 KiB; a command producing over 4 MiB fails instead of exhausting the helper.
Unreachable hosts are shown as errors, never as successful empty lists. Displayed
metrics are the last snapshot; an error means they are stale.

CPU is a hard `--cpus` limit, not a share weight. Memory and swap have matching
limits, with a PID cap of 256 and `no-new-privileges`. The VM OS retains at least
256 MiB outside any one container's requested limit. Limits are per container:
several containers can still overcommit the VM. Disk consumption is monitored,
not individually quota-limited. Allocate and monitor the dedicated VM accordingly.
CPU usage uses differences between `/proc/stat` snapshots; memory and disk are
for the **whole Docker VM**, including OS and Docker overhead. Per-container
CPU can exceed 100% when it uses multiple cores. The existing VM Stats page
provides Xen-side history.

## Access and recovery

XO generates separate Ed25519 client and host keys for every guest. Cloud-init
injects them through the per-VM seed. Root's authorized key includes `restrict`
and a forced helper command; that helper ignores `SSH_ORIGINAL_COMMAND` and
accepts only a bounded versioned JSON request. The guest permits forced-command
root keys only, with password and interactive authentication disabled. Docker's
remote TCP API stays disabled. The management key grants Docker management
access and must be treated as a root-equivalent credential.

The SSH destination comes from live guest-tool addresses. XO pins the host key
in a private per-guest known_hosts file, even when DHCP changes the IP; it never
accepts an unknown host key. Keys and the guest key tag persist under
`/var/lib/xoa-hl/docker-hosts`, outside `/opt/xo`, with directory mode 0700 and
private-key mode 0600. Application RPM updates preserve this state.

Back up this private directory with the XOA VM, and back up the Docker guest
with XO for its disk, images, containers and named-volume data. Application
consistency may require stopping the workload or application-native backups.
Guest snapshots/clones copy the guest's identity and data: do not run two restored
copies simultaneously on the same management network. Deploy a new guest through
the Containers page when a distinct identity is needed.

XO requests deletion of the cloud-init seed through the pinned upstream cleanup
path after boot and guest-tool readiness; if cleanup fails, inspect Tasks/server
logs and remove that seed after confirming cloud-init completion. Cloud-init
keeps a root-only copy of user-data inside the guest, as usual. Credentials are
not returned to the browser. Missing XO credentials must be restored from backup;
do not bypass SSH host verification or substitute an untrusted endpoint. If the
guest host key changes, investigate/recover the guest or deploy a new guest and
restore application data.

Deleting a Docker VM is an explicit action on its normal VM page, not a
container-delete action. The private credential directory is retained for
recovery and can be removed by the appliance administrator after backups and VM
deletion are confirmed. Named-volume pruning is deliberately manual inside the
guest. Upgrades to Docker/AlmaLinux are a separate guest maintenance operation;
updating XOA-HL does not patch the workload guest.

## First-version boundary

No Compose editor, shell/exec terminal, arbitrary startup command, privileged
containers, host bind mounts, host networking, registry credential storage,
existing-host enrollment or VM deletion button. English, French and Japanese
labels are supplied; other existing UI locales use English for these new labels.
These boundaries keep the initial model small and explicit. Image pulls, guest
builds, and installed-package updates require configured network access; no
background external discovery is added.

## Validation before release

Record XOA-HL source SHA/RPM, template source SHA, ISO checksum, XCP-ng release,
Docker version and the CI runs. The source tests do not replace deployed QA.

| Case | Expected |
|---|---|
| Non-admin API call and direct page access | Rejected; no mutation |
| Tagged template, same pool SR/network | One dedicated guest; no Docker installed on XOA or Dom0 |
| Missing template, invalid limits, wrong pool | Clear failure; no orphaned credentials or VM |
| Cold boot/readiness | Explicit wait/error state, then metrics after DHCP/tools/cloud-init |
| Image pull, nginx create, `8080:80/tcp` | Reach guest port from intended clients; enforced CPU/memory limits |
| Named volume + stop/start/reboot | Application data remains |
| Container removal | Confirmation, stopped-only, named volume remains |
| Image removal in use | Docker refuses without force |
| Logs containing HTML and large output | Text only, bounded; no script execution |
| Guest disconnected or SSH key replaced | Visible failure; no unverified connection |
| XO restart/RPM update | Same guest and keys; UI reconnects |
| Two concurrent operations/pull and poll | Serialized; no duplicate container operation |
| VM resource panel | Whole-guest CPU/RAM/disk plus per-container CPU/RAM |
| Cloud-init seed cleanup | Seed removed after boot; investigate cleanup failures |

CI checks patch application, generated keys/SSH arguments, API authorization
metadata, React 15 UI flows, helper validation and real Docker lifecycle. The
Packer image build and this table require an XCP-ng-connected QA runner/host.
Keep all PRs draft and issue #7 open until those results are reviewed.
