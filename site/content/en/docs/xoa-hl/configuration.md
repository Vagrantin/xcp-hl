---
title: Configure the appliance service
description: Locate operator configuration and prepare a checked service change.
weight: 71
translationKey: xoa-manual-configuration
translationStatus: source
sourceRevision: sha256:99961190bdd241d90252dff4f977f92bc2967fbdc3346794a1823406de7da59f
glossaryTerms: ["appliance", "host", "pool"]
---

Configure xo-server separately from the settings and records exported by the web interface.

{{< callout type="info" >}}
Source-reviewed reference for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Later releases can differ. Installed-appliance acceptance and human translation review remain pending.
{{< /callout >}}

## Locate the settings

| Location | Role at ce38 | How to treat it |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` and `sample.config.toml` | Packaged defaults and commented reference | Read as references; package updates replace packaged files |
| `/root/.config/xo-server/config.toml` | Operator configuration bootstrapped only when absent | Back up privately before editing; preserved by the RPM bootstrap |
| `/root/.config/xo-server/config.z-auto.json` | Settings written by the server | Inspect its presence when tracing overrides; do not blindly overwrite |
| Redis database | XO application records | Use the documented web export/import scope |
| `/etc/xoa-hl/update.conf` | HomeLab updater mode, schedule and channel | Prefer Settings → XOA-HL Updates and the update guide |
| `/opt/xo/xoahl.crt` and `xoahl.key` | Appliance TLS certificate and private key | Preserve separately; never attach the private key to a report |

The packaged systemd unit runs as root and uses the XDG user configuration. The loader also supports `/etc/xo-server/config.*` and local `.xo-server.*` files; multiple files can merge. Check custom unit overrides and other configuration files before deciding which value takes effect. This page describes the shipped unit, not a custom service account.

[Configuration export](/docs/xoa-hl/configuration-backup/) does not include operator TOML, TLS files or updater configuration. Use [maintenance](/docs/xoa-hl/maintenance/) and [updates](/docs/guides/updates/) for those changes.

## Example: advertise an appliance URL

`http.publicUrl` supplies the URL used for pool discovery. It does not create a listener, certificate or DNS record. Choose a real appliance HTTPS URL with matching DNS and a trusted certificate; confirm browser access first. Read [ownership and discovery](/docs/xoa-hl/hosts-pools/) before changing it.

In a disposable lab, merge the property into the **existing** `[http]` table. This minimal example retains the released HTTPS listener and Redis URI; it is not a replacement for a customised file:

```toml
[http]
publicUrl = "https://xoa.lab.example"

[[http.listen]]
port = 443
cert = "/opt/xo/xoahl.crt"
key = "/opt/xo/xoahl.key"

[redis]
uri = "redis://127.0.0.1:6379/0"
```

Do not append another `[http]` table or remove the existing listener. Keep the real configured certificate/key paths. The RPM generates the initial self-signed pair during installation; it does not ship a shared key. A missing key/certificate or missing `/var/lib/xoa-hl/tls-generated` marker causes generation, so record the installed TLS state before an upgrade. Certificate replacement, reverse proxies and Redis migration need their own acceptance tests.

## Map management access before isolation {#management-network}

This is a **source-reviewed, read-only SE07 preflight** for the ce38 image above. The packaged bootstrap configures an HTTPS listener on port `443`; an operator override, proxy, firewall or different deployed image can change the effective path. The UI does not establish a universal firewall rule set. Have the network and host owners agree the permitted management clients, subnets, services, backup destinations and independent console path before changing any ACL, VIF, host PIF or switch policy.

| Path to identify | Readback and boundary |
| --- | --- |
| Authorized browser → XOA-HL | Record the appliance VM/address, resolved name, actual HTTPS endpoint and certificate identity. Verify a fresh login and host inventory from an approved client. The packaged listener is `443`, but inspect the installed configuration and effective endpoint; `http.publicUrl` advertises an address and does not open a listener. |
| XOA-HL → managed host/pool | In **Settings → Servers**, record the connected server address, intended pool/host IDs and certificate handling. Verify live inventory and, if already accepted in the lab, fresh read-only [host statistics](/docs/xoa-hl/hosts-pools/#host-statistics). Do not infer host reachability from browser login alone. |
| Browser → console through XOA-HL → resident host | If console is required, open one disposable running VM through the [console guide](/docs/xoa-hl/vm-operations/#vm-console) and record both the browser result and resident host. The pinned console proxy establishes a separate appliance-to-host WebSocket path; a successful inventory read does not prove it. |
| XOA-HL → remotes and updates | List each configured backup remote and the appliance's own package/DNS/time dependencies with their owners. Test a remote using its [dedicated backup procedure](/docs/xoa-hl/backup-restore/) and package access through the [appliance update guide](/docs/xoa-hl/maintenance/); do not generalize from the web login. |

On a **disposable, release-identified lab**, record the source client, destination name/address, service, observed result and timestamp for each required path. Have the network owner verify that an explicitly unauthorized test client cannot reach the web login, using a permitted test and independent logs; a blocked ping alone proves neither HTTPS isolation nor management availability. Keep console access outside the proposed restricted path. If a policy change is separately approved, change one owner-controlled rule at a time, repeat the same allowed and denied service tests, then check login, host inventory, console and backup scope before closing the window. If any required path fails or access is lost, stop and use the network owner's documented rollback through the independent console; do not remove the XOA connection or change the host management PIF as a shortcut.

No appliance, host or firewall was changed in this source review. The actual listener, client segmentation, proxy/NAT paths, host and remote ports, negative access test, service continuity and rollback remain installed acceptance work. Do not publish a production allowlist from these source observations alone.

## Check syntax and apply in a window

Keep a private copy of the original operator file outside the appliance, with its permissions recorded. Have console access ready and wait for backup, restore and management jobs to finish. Inside the appliance, as root, run the parser after editing:

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` only establishes valid syntax. It does not check file permissions, TLS trust, merged values or reachability. The documented parser and merge behavior were tested with synthetic configuration fixtures, not on a released appliance. Fix parse errors before restarting.

In the agreed maintenance window, apply and inspect:

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

A restart disconnects the web interface. Reconnect at the expected address and verify login, host inventory and discovery after the next mark. If startup fails, restore the saved operator file through the console, parse it again and restart once. Use [troubleshooting](/docs/xoa-hl/troubleshooting/) if the result is unclear. Redact logs before sharing them.

## Sources

[bootstrap](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh), [RPM lifecycle](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [service](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service), [configuration loader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [defaults](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [sample](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [pool discovery](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).

Management-path source at the pins above: [server connection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [console proxy to resident host](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs). Port and reachability in a particular installation require direct observation.
