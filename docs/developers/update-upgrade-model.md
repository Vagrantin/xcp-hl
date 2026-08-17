---
layout: default
title: Update and upgrade model
parent: Developers
nav_order: 6
---

# Update and upgrade model
{: .no_toc }

Design proposal for updating XOA-HL in place and for XOA-driven control of
XCP-ng/XO Lite updates.
{: .fs-6 .fw-300 }

Tracks [xcp-hl#14](https://github.com/Vagrantin/xcp-hl/issues/14).
{: .note }

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

This design closes the XOA-HL gap first, then adds the cross-component
control surface the issue also asks for. It does not touch the host-side
`yum`/Patches mechanism, which already works.

---

## Goals (from the issue)

- Update-management sections in both XO Lite and XOA
- Independent update of XCP-ng+XOLite vs. XOA+underlying OS
- XOA able to trigger XO Lite/XCP-ng updates via an API
- Systemd, yum, dnf as the update mechanics
- Tight, auditable boundary between the WebUI and the OS

---

## Proposed phases

### Phase 1 — XOA-HL becomes yum-updatable

Give `xoa-hl` the same repo-based path `xo-lite-ce` and `xoa-proxy` already
have, instead of the thin install-only RPM.

- Publish a fourth repo, `xcp-hl-xoa-hl`, from the `xoa-hl` CI, alongside a
  new `xoa-hl-<version>.noarch.rpm` per release (same signing subkey model).
- Move the `%post` tarball-fetch logic so it also runs correctly on
  **upgrade**, not just first install: stop `xo-server`, replace
  `/opt/xo` contents, preserve `~/.config/xo-server/config.toml`
  untouched (already the rule on first install), restart `xo-server`.
- Add `%config(noreplace)` handling for anything the operator may have
  edited, matching the `xcp-hl.repo` precedent in `xcp-hl-release`.
- Result: `yum update xoa-hl` on the appliance VM upgrades XOA in place.
  This alone closes the "Known limitations" note in
  [Updating XCP-ng HL](../updates).

This phase needs no new API and no UI work; it is the prerequisite for
everything after it.

### Phase 2 — Update-management UI sections

- **XOA UI**: a settings page showing the installed `xoa-hl` version,
  whether an update is available (`yum check-update xoa-hl` run
  server-side), and a button that runs `yum update -y xoa-hl` and restarts
  `xo-server`.
- **XO Lite UI**: already shows host patches via the stock Patches tab;
  add a visible "XCP-ng HL components" grouping so `xo-lite-ce`,
  `xoa-proxy`, and `xcp-hl-release` read as one unit distinct from
  upstream XCP-ng patches.

### Phase 3 — XOA-driven control of XO Lite/XCP-ng updates

- Define a small, explicit API surface XOA calls against the XCP-ng host
  (over the existing XAPI session, not a new open port): trigger
  `updater.py`'s update flow, or run a scoped systemd unit that does
  `yum update xo-lite-ce xoa-proxy` without touching the rest of the
  host's patches.
- This is additive to, not a replacement for, the Patches tab: it lets
  XOA offer "update just the HL components" where today only "update
  everything" exists.

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
  `systemctl start xoa-hl-update.service` and equivalent, not a general
  `sudo yum` grant.
- Each unit hardens with the usual systemd sandboxing knobs
  (`ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, explicit
  `ReadWritePaths=` for only `/opt/xo` or the yum cache as needed).
- Update units log to the journal; the UI reads status back via
  `systemctl show`/`journalctl`, not by parsing free-form script output.

---

## Open questions

- Does Phase 3's API run over the existing XAPI plugin mechanism
  (`updater.py`-style) or a small sidecar the appliance calls directly?
  XAPI reuse avoids opening a new port but couples the feature to
  XCP-ng's plugin API surface.
- Should `xoa-hl` upgrades be all-or-nothing like the host Patches tab,
  or should config-affecting changes (e.g. a `xoahl.config.toml` schema
  change) get a confirmation step before restart?
- Rollback story for `xoa-hl`: `yum downgrade xoa-hl-<version>` mirrors
  the existing host rollback pattern, but the tarball-per-release size
  means the repo needs to keep more than the "most recent" builds it
  keeps today for the other repos, or downgrades run out of window fast.

---

## Sequencing

Phase 1 is scoped enough to implement directly: repo publishing already
exists for two other components, and the `%post` logic mainly needs to
handle the upgrade case that install-only ignores today. Phases 2 and 3
depend on Phase 1 shipping first.
