# XOA group A lab acceptance: execution plan (draft)

Status: draft, written 2026-11-03. Nothing in this plan has run. Results go to
the `site/XOA-*-VALIDATION.md` records only after observation. Release scope
for every result is the one read from the cell at run time (host build, appliance
image, RPM NEVRA); XCP-HL is alpha and no compatibility claim follows.

## Why not the shared docs lab

The docs lab (`docs-xcphl`, `docs-xoahl`) is shared with the screenshot
pipeline and the reservation-fix work, and its Jenkins locks cover single
stages, not a whole manual session. Group A needs hours of exclusive,
destructive access. Throwaway cells on the Test host remove that contention.
The docs lab, its baselines and `jenkins-infra` config are not touched.

## Measured Test host capacity (192.168.0.10, 2026-11-03)

| Resource | Measured | Consequence |
| --- | --- | --- |
| RAM | 16.9 GB total (15.7 GiB), dom0 1.8 GiB | About 13.6 GiB usable for VMs |
| Held by Jenkins-owned VMs | `xcpng-ce-qa` 4 GiB (running since 2026-11-02), `XOA-TEST` 2 GiB (running since 2026-11-01) | Not ours; left running unless the user says otherwise |
| Free with the docs lab halted | about 7.4 GiB | One full cell at a time |
| CPU | 16 logical, dom0 has 4 vCPUs | Not the bottleneck; install steps will contend on one NVMe |
| Local SR | 408 GiB, 114 GiB used, ext thin | About 290 GiB free; cells fit |
| dom0 root filesystem | 18 GiB, 3.6 GiB free | Never stage ISOs, exports or backups on dom0 root |
| NICs | `eth0` LAN 192.168.0.10; `eth1` up, no IP, `Pool-wide network 1` | `eth1` is the spare uplink for SN04 |

## Models taken from setupxcpvm

| Role | setupxcpvm model | Use here |
| --- | --- | --- |
| Nested XCP-HL host | `xcpng-host` (Packer, released `xcp-ng-ce-iso`, answerfile install, SSH assertions) | One golden host build, then per-cell copies |
| XOA-HL appliance | `xoa-hl-host` (AlmaLinux 9 kickstart plus released `xoa-hl` RPM) | One golden appliance build, then per-cell copies |
| NFS and Linux guest helper | `linux` (Debian template build) | NFS server with two exports, golden Debian helper |

The harness fixes `KEEP_VM`, `VM_NAME`, `REBOOT_CYCLES` and sizing per build.
Golden builds use `KEEP_VM=always` and the `ga-gold-` name prefix. Local
`build.config` files hold secrets and stay out of git, as `.gitignore` already
enforces.

Fidelity note: the earlier runs recorded the published XVA image
(`xoa-image-*`), while `xoa-hl-host` installs the RPM on AlmaLinux. Both ship the
same pinned XO 5.113.2 source, but the artefact differs. Every record names
which one produced it. See open decision 2.

## Cell shapes and RAM budget

| Cell | VMs | RAM |
| --- | --- | --- |
| Full | nested host 3 GiB (2 vCPU, 40 GiB disk), appliance 2 GiB, NFS helper 0.5 GiB | 5.5 GiB |
| VM-only | nested host 3 GiB, appliance 2 GiB | 5.0 GiB |
| Appliance-only | appliance 2 GiB | 2.0 GiB |

Concurrency rule, enforced by the builder thread: start a cell only if
`xe host-compute-free-memory` is at least the cell size plus 0.75 GiB. With the
Jenkins-owned VMs running that means one VM-only or full cell, and an
appliance-only cell only when the margin holds. With both Jenkins-owned VMs
stopped, two full cells run in parallel.

## Isolation and safety rules

- Every object is named `ga-<cell>-<role>` and tagged `other-config:ga-cell=<cell>`.
  Teardown selects by tag only.
- Never touch Prod (192.168.0.2), `xcpng-ce-qa`, `XOA-TEST`, any `docs-` VM or
  the `/root/docs-lab-session.lock` directory. If a docs lab session is active,
  cell start waits only for RAM, not for that lock.
- One appliance manages only its own cell host. Copies of one golden host share
  host and pool UUIDs, so no appliance may be pointed at two copies.
- `eth1` is leased through a ledger entry `net1`; one cell at a time, with a
  distinct VLAN ID per cell.
- Passwords are generated per cell, stored in the password manager, and never
  put in thread messages, issues, commits or records.
- Static addresses, set inside each VM as in the docs lab, from a reserved
  range (open decision 3).

## Tracks and run assignment

Run numbers follow the original list. Run 1 (ST04) passed on ce40 and its
defect is #363, so it is out of scope here.

| Track | Cell | Runs | Needs |
| --- | --- | --- | --- |
| V: VM lifecycle | VM-only | 5 VM05, 2 VM01, 3 VM02, 4 VM04, 6 VM06, 7 VM07, 8 VM08 (finish open subchecks), 9 VM09 | Ubuntu 24.04 ISO in the ISO library; golden Ubuntu guest installed without tools |
| N: storage and network | Full | 10 SN01, 11 SN02 NFS, 12 SN02 local, 13 SN03, 14 SN04, 15 SN05 | NFS helper with an empty export; spare virtual disk; second VIF on `Pool-wide network 1` |
| B: backup | Full | 16 BK03, 17 BK04, 18 BK06, 19 BK07, 21 BK09 | NFS helper as backup remote; Ubuntu guest on an ext SR |
| H: host and access | VM-only | 22 HP01/HP02, 23 HP04, 24 HP05, 25 SE01, 26 SE02, 29 SE07 | Seeded local update repo (as `docs-lab-seed-patches.sh` does); HP05 last because it patches and reboots |
| X: appliance only | Appliance-only | 20 BK08, 27 SE04/SE05, 28 SE06 | A fresh appliance; SE06 and SE05 change certificate and admin state, so no other track shares it |

## Phases and order

Phase 0, builder thread only, about 2 hours:

1. Check RAM, disk and `eth1` state; create the ledger on the Test host.
2. Build golden host (`xcpng-host` model, latest released ISO tag, 40 GiB disk).
   Record the tag, ISO checksum and installed RPM versions it reports.
3. Build golden appliance (`xoa-hl-host` model, latest release).
4. Build the NFS helper (`linux` model, two exports, `/export/vmdisk` empty and
   `/export/backup`).
5. Inside the golden host, install Ubuntu 24.04 without guest tools and keep the
   guest halted; this is the VM05 starting point.
6. Smoke-test one copy of the golden set end to end, then destroy it.

Phase 1, tracks, lowest risk first:

- One-slot order: V, then N, then B, then H, with X inserted whenever the RAM
  margin allows an appliance-only cell beside the running cell.
- Two-slot order (only if the two Jenkins-owned VMs may be stopped): V with N,
  then B with H, X alongside whichever is lighter.

Rough wall time, unattended mostly: Phase 0 about 2 h; V, N, B, H about 2.5 to 3
h each; X about 1.5 h. One slot: about 12 to 14 h. Two slots: about 7 to 8 h.
These are estimates, not measurements.

## Threads and messaging

Peer top-level threads, started by the lead, that message each other with
`t3_thread_send`. Each message is one line, no secrets, shaped
`GA|<TYPE>|<track or cell>|<detail>`.

| Thread | Owns | Sends | Receives |
| --- | --- | --- | --- |
| Lead (this thread) | Plan, repo, PR, issues, GitHub comments, final report | `GA|GO|<track>` when a slot is free | `GA|RESULT`, `GA|BLOCKED`, `GA|DEFECT` |
| Builder | Test host VM lifecycle, ledger, RAM gate, golden images, teardown | `GA|READY|<track>|<cell>|<endpoints>` | `GA|NEED|<track>`, `GA|DONE|<track>` |
| Track V, N, B, H, X | Their rows only, on their cell only | `GA|NEED`, `GA|RESULT`, `GA|BLOCKED`, `GA|DEFECT`, `GA|DONE` | `GA|READY`, `GA|GO` |

Rules:

- Only the lead edits `site/` records, the inventory, the closure file and the
  PR. Track threads write result fragments (expected, actual, result, build or
  command identity) to `/root/ga-lab/results/<track>.md` on the Test host and
  send the path in `GA|RESULT`. This avoids merge conflicts.
- Only the builder starts or stops cells. A track thread asks with `GA|NEED`
  and waits for `GA|READY`. The builder answers `GA|WAIT|<reason>` if the gate
  fails and re-sends `GA|READY` when it passes.
- A failed, blocked or skipped row stays open. A pass is written only for
  something the track thread observed on its own cell.
- A new defect gets a `GA|DEFECT` message; the lead files the issue and links it.
- Each track thread sends `GA|DONE` so the builder tears the cell down by tag
  and releases ledger RAM and `net1`.

## Recording and reporting

- Lead adds a dated lab-run section per validation record with the identities
  read from each cell, the golden build identities, and expected, actual, result
  per row.
- Inventory and closure status change only where the evidence supports it.
  Reader-facing corrections need FR and JA updates and stay draft for the
  exact-revision review; `data/xoa_manual_reviews.json` approvals are not edited.
- Comments on #197, #198, #199 and #189 carry the evidence. No issue closes
  unless its full acceptance is met.

## Cleanup

At the end the builder destroys every object carrying a `ga-cell` tag, keeps
the golden images only if the user wants them, and confirms free RAM and SR
space against the first measurement.

## Open decisions for the user

1. May `xcpng-ce-qa` and `XOA-TEST` (Jenkins-owned, 6 GiB together) be stopped
   during the window to allow two parallel cells? Default: no, one slot.
2. Appliance artefact: `xoa-hl-host` RPM-on-AlmaLinux as the setupxcpvm model
   (default), or import the published XVA image to match earlier records.
3. A reserved block of free static IPs on 192.168.0.0/24 for the cells
   (six addresses cover three cells plus spares), or DHCP with leases read back.
