---
title: "Configure the appliance service"
linkTitle: "Service settings"
description: "Find the service configuration files, check access paths and the HTTPS certificate, and apply a change safely."
weight: 91
translationKey: xoa-manual-configuration
translationStatus: source
sourceRevision: sha256:cf10324c828a27039571b3a119cc1feacd94fbe74d8a0815a3060736e0c32685
glossaryTerms: ["appliance", "host", "pool"]
---

Find the xo-server configuration files of the XOA-HL appliance, check its management access and its HTTPS certificate, and apply a change safely. You work as root in a shell inside the appliance, with a separate console ready. These files are separate from the settings and records that the web interface exports.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Based on the released code; not yet tested on a lab system.
{{< /callout >}}

## Find the settings files {#settings-files}

| Location | What it holds | How to handle it |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` and `sample.config.toml` | Package defaults and a commented example | Read only. A package update replaces these files |
| `/root/.config/xo-server/config.toml` | Your own settings (the operator file). Created at installation only if it does not exist | Keep a private backup before you edit it. Package installation keeps this file |
| `/root/.config/xo-server/config.z-auto.json` | Settings that the server writes itself | Check whether it exists when you look for overrides. Do not overwrite it blindly |
| Redis database | XO application records | Use the export and import of the web interface, within their documented scope |
| `/etc/xoa-hl/update.conf` | Mode, schedule and channel of appliance updates | Use **Settings → XOA-HL Updates** and the update guide instead |
| `/opt/xo/xoahl.crt` and `xoahl.key` | The appliance's TLS certificate and private key | Keep a separate copy. Never attach the private key to a report |

The shipped systemd service runs as root and reads the user configuration under `/root/.config`. xo-server also reads `/etc/xo-server/config.*` and local `.xo-server.*` files, and merges several files together. Before you decide which value applies, check for custom service overrides and other configuration files. This page covers the shipped service only, not a custom service account.

The [configuration export](/docs/xoa-hl/configuration-backup/) does not include your TOML file, the TLS files or the update settings. For those, see [appliance maintenance](/docs/xoa-hl/maintenance/) and [updates](/docs/guides/updates/).

## Set the appliance URL for pool discovery {#public-url}

`http.publicUrl` sets the appliance URL that XO records in each connected pool, for pool discovery. It does not create a listener, a certificate or a DNS record. Use a real HTTPS URL of the appliance, with matching DNS and a trusted certificate, and check first that it opens in a browser. Read [Hosts and pools](/docs/xoa-hl/hosts-pools/) before you change it.

Try this on a lab appliance that you can rebuild. Add the property to the **existing** `[http]` table. This minimal example keeps the shipped HTTPS listener and Redis address. It is not a replacement for a file you have customised:

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

Do not add a second `[http]` table, and do not remove the existing listener. Keep the real certificate and key paths. The package creates its own self-signed certificate and key at installation; it does not ship a shared key. If the key, the certificate or the `/var/lib/xoa-hl/tls-generated` marker is missing, a new pair is generated. Note the installed TLS state before an upgrade. Replacing the certificate, reverse proxies and moving Redis are not covered here.

## Map management access before you restrict the network {#management-network}

This check only reads; it changes nothing. The shipped setup listens for HTTPS on port `443`. Your own settings, a proxy, a firewall or a different image can change the real path. The web interface does not set any firewall rules for you.

**Before you start**

- Agree with the network and host owners on the allowed management clients, subnets, services and backup destinations.
- Agree on a separate console access path that the restriction will not affect.
- Do this before you change any ACL, VIF, host PIF or switch policy.

| Path | What to note and check |
| --- | --- |
| Approved browser → XOA-HL | Note the appliance VM and address, the resolved name, the real HTTPS endpoint and the certificate identity. From an approved client, sign in again and check the host list. The shipped listener is `443`, but check the installed configuration and the real endpoint. `http.publicUrl` only advertises an address; it does not open a port. |
| XOA-HL → hosts and pools | In **Settings → Servers**, note the connected server address, the expected pool and host IDs, and how the certificate is handled. Check the live host list and, if you have already tested it in the lab, recent read-only [host statistics](/docs/xoa-hl/hosts-pools/#host-statistics). A browser sign-in alone does not prove that the appliance reaches the hosts. |
| Browser → console through XOA-HL → the VM's host | If you need the console, open one running test VM with the [console guide](/docs/xoa-hl/vm-operations/#vm-console). Note the browser result and the host the VM runs on. The console uses a separate WebSocket connection from the appliance to that host; a working host list does not prove it. |
| XOA-HL → backup remotes and updates | List each backup remote and the appliance's package, DNS and time services, with their owners. Test a remote with its [backup procedure](/docs/xoa-hl/backup-restore/), and package access with the [appliance update guide](/docs/xoa-hl/maintenance/). A working web sign-in does not prove these paths. |

On a lab appliance whose release you have identified:

1. For each required path, note the source client, the destination name or address, the service, the result and the time.
2. Ask the network owner to check that an unauthorized test client cannot reach the web sign-in page, with an allowed test and separate logs. A blocked ping proves neither HTTPS isolation nor that management still works.
3. Keep your console access outside the path that you plan to restrict.
4. If a policy change is approved separately, change one owner-controlled rule at a time. After each change, repeat the same allowed and denied tests.
5. Before you close the window, check sign-in, the host list, the console and backups.

**Check:** every required path still works, and the unauthorized client cannot reach the sign-in page.

If a required path fails or you lose access, stop. Use the network owner's documented rollback through the separate console. Do not remove the XOA connection or change the host management PIF as a shortcut. Real listeners, client segmentation, proxy and NAT paths, host and remote ports, and rollback are not covered here. Do not build a production allowlist from this page alone.

## Check the HTTPS certificate before you replace it {#tls-certificate-preflight}

This check only reads files and connections; it renews nothing. At installation, the shipped setup writes an HTTPS listener on port `443` that uses `/opt/xo/xoahl.crt` and `/opt/xo/xoahl.key`. Later changes or a reverse proxy can serve TLS somewhere else.

The package does not ship a shared private key. At installation, it generates a self-signed `CN=xoa.local` pair if either file or the `/var/lib/xoa-hl/tls-generated` marker is missing. A later package update can regenerate the pair in the same way, and it restarts `xo-server` afterwards (`%posttrans`). Note the real paths and the package state before you plan a renewal. Never delete the marker to rotate the certificate.

1. Make sure that a separate console and a local administrator account are available.
2. Privately note the installed image and package, the effective `http.listen` values and any merged configuration overrides. Run `systemctl cat xo-server` to see service overrides.
3. Note whether a reverse proxy, a load balancer or another TLS endpoint sits in front of the appliance. `http.publicUrl` only advertises an address: it does not show the listener or the certificate that browsers see. Stop if you find several listeners, or something unexpected on port `443`.
4. On the **appliance**, read only the metadata of the configured certificate, key and marker. For the shipped paths, these read-only commands show the file modes and the public certificate fields, without printing the private key:

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   If your configuration uses other files, use the **actual configured** pair. If a file or the marker is missing, stop and find out why before any update or restart; do not generate a new pair. Keep the private key and the complete configuration out of screenshots, logs and issues.
5. From an **approved client**, open the real HTTPS address and sign in again in a fresh browser session.
6. If OpenSSL is available and the owner gave you the trust chain, run `openssl s_client -connect <name>:<port> -servername <name> -verify_hostname <name> -verify_return_error -brief </dev/null` with the real DNS name and port. For a private CA, add the owner-approved `-CAfile <ca-path>`. Check the installed OpenSSL version before you use these options.
7. Compare the certificate's fingerprint, name, chain and expiry date with the endpoint you expect.

**Check:** you have noted the certificate that the browser receives, and the files it comes from. The self-signed certificate created at installation may fail the trust check: note that result, but do not turn off verification or call the certificate trusted. If a proxy handles TLS, its certificate may differ from the appliance file; note both separately.

**Before you plan a replacement**, agree with the certificate and appliance owners on:

- the new certificate chain, its matching private key, the names it covers and its expiry date;
- secure storage, and the file owner and permissions;
- a separate recovery console, and a private backup of the current **certificate pair, marker and operator file**;
- a maintenance window after jobs finish, the exact listener or proxy to change, and a tested restart and rollback procedure;
- the tests to run afterwards: a fresh, trusted browser sign-in, the right fingerprint, a working local administrator, the host and pool list, and the console.

A valid configuration file, files in place or a successful restart do not prove that clients trust the certificate, or that it is the right one. Renewing the certificate is not covered here: do not use this check as a production replacement procedure.

## Check the syntax and restart the service {#apply-change}

**Before you start**

- Keep a private copy of the original operator file outside the appliance, and note its permissions.
- Have console access ready.
- Wait until backup, restore and management jobs have finished.

After you edit the file, run this check inside the appliance, as root:

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` only means that the syntax is valid. It does not check file permissions, TLS trust, the merged values or reachability. Fix any error before you restart.

In the agreed maintenance window, restart the service and read its status and recent log:

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

The restart disconnects the web interface. Reconnect at the expected address.

**Check:** you can sign in and the host list is complete. XO writes its URL to each pool at a regular interval, so check pool discovery after the next update.

If the service does not start, restore the saved operator file through the console, check its syntax again and restart once. If the result is unclear, see [troubleshooting](/docs/xoa-hl/troubleshooting/). Remove secrets from logs before you share them.

{{< details title="Sources" closed="true" >}}
- **Configuration files and service**: [initial setup script](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [package install and update](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [systemd service](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [configuration loader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [default settings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [commented example](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [pool discovery](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).
- **Management access**: [server connection](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [console proxy to the VM's host](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **HTTPS certificate**: [generated pair, marker and restart after an update](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [initial listener](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [effective listener setup](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [OpenSSL x509 manual](https://docs.openssl.org/3.0/man1/openssl-x509/), [OpenSSL s_client manual](https://docs.openssl.org/3.0/man1/openssl-s_client/).
{{< /details >}}
