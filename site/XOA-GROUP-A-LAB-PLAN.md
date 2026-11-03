# XOA group A lab acceptance: execution plan (draft)

Status: active, written 2026-11-03. Phase 0 and the V/X cells have run. Results go to
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
| Full | nested host 3 GiB (2 vCPU, 100 GiB thin disk), appliance 2 GiB, NFS helper 0.5 GiB | 5.5 GiB |
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
2. Build golden host (`xcpng-host` model, latest released ISO tag, 100 GiB thin disk).
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

## Decisions (user, 2026-11-03)

1. `xcpng-ce-qa` and `XOA-TEST` (Jenkins-owned, 6 GiB together) may be stopped
   for the window so two cells run in parallel. The builder stops them only
   when `jenkins-cli running` reports idle, records their prior power state, and
   starts them again at cleanup. Two-slot schedule applies.
2. Appliance artefact: `xoa-hl-host` (RPM on AlmaLinux), the setupxcpvm model.
   Records name it as RPM-installed, not the published XVA image.
3. Addresses: DHCP, with leases read back after each boot. A cell whose address
   changes is recorded as a defect of the harness, not of the product.

Latest releases at planning time: `xcp-ng-ce-iso` v8.3-ce55 and `xoa-hl`
v5.113.2_e281c536-ce51. The builder pins these tags and records them; they are
newer than the ce44 host and ce40 image of the earlier sessions.

## Deviations found during Phase 0

- The XCP-ng installer refuses a disk under 46 GB, so the golden host is 100 GiB
  thin (not 40 GiB). The nested local SR is 37.6 GiB and the XCP-HL ISO library
  (20 GiB) is present, so the ISO-store skip path is not in play.
- Packer's XCP-ng plugin records 127.0.0.1 as the guest IP on this workstation,
  so builds are finished by hand over SSH. Filed as a setupxcpvm harness defect
  in [setupxcpvm #12](https://github.com/Vagrantin/setupxcpvm/issues/12), not fixed here.

## Golden images (Phase 0, 2026-11-03)

| Role | Identity read by the builder |
| --- | --- |
| Nested host | XCP-ng 8.3.0 build ce55 from `xcp-ng-ce-iso` v8.3-ce55; ISO SHA-256 `311dc0fe8156db4ea6be535a9274057b7abe8af68d0644afc62b7e8283d57cfe` matches the published value; 3 GiB, 2 vCPU, 100 GiB thin; xapi 26.1.19, Xen 4.17.7-2.5, kernel 4.19.19-8.0.46.12; `xo-lite-ce-0.21.0-39.g54c289b.xcpng8.3.noarch`, `xoa-proxy-0.1.3.1-73.g1b44984.static.x86_64`, `xcp-hl-release-0.0.5-5.g157727f.xcpng8.3.noarch`, `xcp-ng-release-8.3.0-38` |
| Appliance | AlmaLinux 9.8, `xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64` from tag `v5.113.2_e281c536-ce51`, node v24.22.2, 2 GiB, 2 vCPU, 20 GiB; RPM-installed, not the published XVA image |
| NFS helper | Debian 13.7 (trixie), 512 MiB, nfs-kernel-server 2.8.3-1, exports `/export/vmdisk` (empty) and `/export/backup` |
| Nested guest `ga-ubuntu` | Ubuntu 24.04.5 LTS, kernel 6.8.0-147-generic, no guest tools, 1 vCPU, 1.5 GiB, 16 GiB; installed from `ubuntu-24.04.5-live-server-amd64.iso` SHA-256 `97f3d7ffb032c3eb3b23d2c8be9cc76e60c2c1f2c0146ba5ba9fe01cafae0fd8`, which matches the signed Canonical SHA256SUMS |

Hard limit found: a nested guest with 2 vCPUs crashed the golden host domain
three times (Xen `domain_crash` in `nvmx_n2_vmexit`, invalid guest state on the
Test host Xen 4.17.6-12, i5-12600H). With 1 vCPU it boots and runs, so every
nested guest stays at 1 vCPU. Copies of the golden host share host and pool
UUIDs, so no appliance manages two copies.

## Track status, 2026-11-03

The V cell passed VM05, observed only the VM01 browser transport, and stopped
the ordered sequence when guest display/input could not be verified without a
capture. Its later VM rows were not attempted. The X cell observed BK08 partial
import and local OTP/sole-admin recovery; SE06 certificate replacement and
rollback are partial. Both cells and their test disks were removed. The dated
validation records have the expected, actual and result rows. N, B and H have
not completed. Jenkins reported active/queued work at the first N start gate.
When it later became idle, the N cell helper copied and started three `ga-n-*`
VMs, but no acceptance test ran. Its inherited DHCP lookup actively pinged the
whole `192.168.0.0/24`; this violated the lab-only contact rule. The operator
interrupted the helper, removed only the `ga-n-*` VMs, verified no N-tagged VMs
or ping jobs remained, and released the `net1` ledger entry. The ping sweep did
run; no claim of zero external contact or impact is made. N, B and H stay open
until passive, scoped address discovery is demonstrated. The local scratch
`findip.sh` now reads only a passive ARP capture filtered to the cell VM's own
MAC, and `cell.sh` starts that capture before boot and tears its own cell down
if no address is seen; both scripts passed `bash -n` and an offline ARP parser
check. This replacement has not passed a live cell start. No new cell is
started while Jenkins has active or queued work.
The `ga-gold-` images remain halted for later cells.
