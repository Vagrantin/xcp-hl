---
layout: default
title: Update and upgrade model
parent: Developers
nav_order: 6
---

# Update and upgrade model
{: .no_toc }

Design proposal for updating XOA-HL in place.
{: .fs-6 .fw-300 }

Tracks [xcp-hl#14](https://github.com/Vagrantin/xcp-hl/issues/14).
{: .note }

{: .important }
Phase 1 is implemented, merged to `main` on
[`xoa-hl`](https://github.com/Vagrantin/xoa-hl). See
[xoa-hl: Updates](xoa-hl#updates) for the details. GitHub Pages still needs
to be enabled on that repo before the published yum repo is reachable.

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Where things stand today

Two of the three update paths already work:

| Component | Update path today |
|---|---|
| `xo-lite-ce`, `xoa-proxy` (host, RPM) | `yum update` via the `xcp-hl-*` repos, surfaced in XO's Patches tab through `updater.py`. See [Updating XCP-ng HL](../updates). |
| XCP-ng itself | Same `yum`/Patches path, upstream. |
| **XOA-HL (the appliance)** | **None.** `xoa-hl`'s RPM is thin: `%post` downloads a tarball to `/opt/xo` only on install. There is no repo, no version check, no upgrade path in place. Updating means deploying a new appliance image. |

This design closes the XOA-HL gap. It does not touch the host-side
`yum`/Patches mechanism, which already works.

---

## Scope

The issue also proposes an update-management section in XO Lite and an API
letting XOA trigger XCP-ng/XO Lite updates. Both are dropped from this
design: XO Lite's host updates already surface through the stock Patches
tab (see [Updating XCP-ng HL](../updates)), so a second UI for the same
data would duplicate it without adding capability, and the XOA-driven API
existed only to feed that second UI. Removing the UI removes the reason
for the API.

This design covers XOA-HL only:

- Give XOA-HL a real update path (currently the only component with none)
- Systemd, yum, dnf as the update mechanics
- Tight, auditable boundary between the WebUI and the OS

---

## Proposed phases

### Phase 1 — XOA-HL becomes yum-updatable (done)

Give `xoa-hl` the same repo-based path `xo-lite-ce` and `xoa-proxy` already
have, instead of the thin install-only RPM.

- Use a fourth repo, `xoa-hl`, at
  `https://vagrantin.github.io/xoa-hl/8.3/x86_64/` — the
  [`Vagrantin/xoa-hl`](https://github.com/Vagrantin/xoa-hl) repo itself,
  mirroring how `xolite-ce` and `xoa-proxy` already publish their own repos.
  GitHub Pages is not currently enabled on that repo (confirmed: its Pages
  URL 404s today), so there is no existing site to collide with. Add a
  `pages.yml` there matching `xcp-hl`'s own (`createrepo_c` + GPG-signed
  `repomd.xml`, no Jekyll step needed since `xoa-hl` has no docs site) and a
  new `xoa-hl-<version>.noarch.rpm` per release (same signing subkey model
  as `xo-lite-ce`/`xoa-proxy`).
- **Not** `xcp-hl.repo`. That file is owned by `xcp-hl-release` and lives on
  the XCP-ng host (CentOS 7 dom0) — a different machine from the XOA-HL
  appliance (AlmaLinux 9), which has its own `/etc/yum.repos.d/` the host
  config never touches. The `xoa-hl` RPM's own `%post` writes
  `/etc/yum.repos.d/xoa-hl.repo` on the appliance directly, pointing at the
  `xoa-hl` repo above; nothing changes in the `xcp-hl` repo for this phase.
- Old `xoa-image-*` release tags (pre-`build-xoa-hl` VM image releases,
  still present in this repo's history) do not interfere: the RPM
  collection step matches by asset filename glob (`xoa-hl-*.rpm`), which
  those tags simply have none of, and the existing `xcp-hl` workflow
  already tolerates that case per-tag.
- Move the `%post` tarball-fetch logic so it also runs correctly on
  **upgrade**, not just first install: stop `xo-server`, replace
  `/opt/xo` contents, preserve `~/.config/xo-server/config.toml`
  untouched (already the rule on first install), restart `xo-server`.
- Do not add `%config(noreplace)`, this is an appliance, we replace the file.
- Result: `yum update xoa-hl` on the appliance VM upgrades XOA in place.
  This alone closes the "Known limitations" note in
  [Updating XCP-ng HL](../updates).

This phase needs no UI work; it is the prerequisite for everything after it.

### Phase 2 — Update-management UI in XOA

- A settings page in the XOA UI showing the installed `xoa-hl` version,
  whether an update is available (`yum check-update xoa-hl` run
  server-side), and a button that runs `yum update -y xoa-hl` and restarts
  `xo-server`.

---

## Security boundary

The issue's stated concern is keeping WebUI-triggered OS access narrow.
Proposed shape, to refine once Phase 1 lands:

- Each update action runs as a dedicated **systemd unit** invoked via
  `systemctl start <unit>`, never a shell command built from request
  input. The unit's `ExecStart` is a fixed script; there is nothing for
  a caller to inject.
- `xo-server` (running as a restricted user, not root) triggers units via
  a narrowly scoped **polkit rule** or a `sudoers` entry limited to
  `systemctl start xoa-hl-update.service`, not a general `sudo yum` grant.
- Each unit hardens with the usual systemd sandboxing knobs
  (`ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, explicit
  `ReadWritePaths=` for only `/opt/xo` or the yum cache as needed).
- Update units log to the journal; the UI reads status back via
  `systemctl show`/`journalctl`, not by parsing free-form script output.

---

## Open questions

- Should `xoa-hl` upgrades be all-or-nothing like the host Patches tab,
  or should config-affecting changes (e.g. a `xoahl.config.toml` schema
  change) get a confirmation step before restart?
- Rollback story for `xoa-hl`: `yum downgrade xoa-hl-<version>` mirrors
  the existing host rollback pattern, but the tarball-per-release size
  means the repo needs to keep more than the "most recent" builds it
  keeps today for the other repos, or downgrades run out of window fast.

---

## Sequencing

Phase 1 is done: the RPM's scriptlets are upgrade-safe, and the appliance
repo config and its GitHub Pages publishing workflow are merged. What is
left is a manual, repo-owner-only step (enabling GitHub Pages on `xoa-hl`)
before it is actually reachable. Phase 2 can start once that is confirmed
working end to end.
