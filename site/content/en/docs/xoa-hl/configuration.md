---
title: Configure the appliance service
description: Locate operator configuration and prepare a checked service change.
weight: 71
translationKey: xoa-manual-configuration
translationStatus: source
sourceRevision: sha256:968057a7d1a41033c98ff1ff829858fec7d897e9c34b4151899d6bd7b7f814eb
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
