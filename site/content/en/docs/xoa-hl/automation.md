---
title: "Automate with xo-cli"
linkTitle: "Automation (xo-cli)"
description: "Read inventory with xo-cli using a short-lived token, then revoke it."
weight: 92
translationKey: xoa-manual-automation
translationStatus: source
sourceRevision: sha256:d62ec0a49c44ac7275b68cb4b2cf81eabcafc83118ff7e2186109ad545cfe4f1
glossaryTerms: ["appliance", "host", "vm"]
---

Use the bundled xo-cli for a small read-only inventory exercise before writing automation that changes a VM.

{{< callout type="info" >}}
Source-reviewed reference for image `xoa-image-20261009-5f33c81`, package `v5.113.2_e281c536-ce38` and XO 5.113.2. Later releases can differ. Installed-appliance acceptance and human translation review remain pending.
{{< /callout >}}

The client at the pin is `xo-cli` **0.32.2** with `xo-lib` **0.11.1**. The commands below were executed with that CLI source against a synthetic loopback HTTPS/WebSocket server: TLS failure/success, password prompt, expiry request, method discovery, inventory parameters and local cleanup passed. This validates the client contract, not a real appliance, token-expiry enforcement, object permissions or XAPI operations.

## 1. Prepare the lab and TLS trust

Run the bundled `/usr/local/bin/xo-cli` **inside the appliance** in a dedicated Bash session. Have a normal test user and a disposable VM available. Confirm the installed release first with [maintenance](/docs/xoa-hl/maintenance/); use [permissions](/docs/xoa-hl/permissions/) for separate authorization tests.

Use an appliance DNS name matching its certificate. Obtain the public CA/certificate through a trusted channel and verify its fingerprint independently. Set the example path to that PEM file and replace the URL/email. `NODE_EXTRA_CA_CERTS` adds trust; it does not waive hostname validation. The initial self-signed `xoa.local` certificate may require lab DNS/certificate preparation. Do not use `--allowUnauthorized` or `NODE_TLS_REJECT_UNAUTHORIZED=0` to bypass a failure.

## 2. Register a short-lived token

This helper isolates credentials in a new directory and preserves any existing CLI configuration. A fresh restrictive umask protects the newly created file. Registration prompts for the password; do not add it as a positional argument or place a token in a URL. If the account requires OTP, add `--otp CODE` before the URL using a current code.

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

The server's pinned defaults are 30 days with a maximum of 0.5 year; the requested `1 hour` is intentionally shorter. Server configuration can change those limits. The token carries its user's authority, not a dedicated read-only scope. Treat the configuration file as a credential and keep it out of shell traces, backups attached to issues and source control. This registration creates authentication state; subsequent examples only read data.

## 3. Discover and read

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| Command | Expected interpretation |
| --- | --- |
| `list-commands xo.getAllObjects` | Human-readable method parameters; discovery is not an authorization grant |
| `system.getServerVersion --json` | Server package version, `"5.193.1"` at this pin; not the XO product version |
| `list-objects --id --name_label --power_state type=VM` | JSON array projected to those properties; no VM state is changed |
| `xo.getAllObjects --json …` | JSON object keyed by object ID; object filter and numeric limit |

Keep flags before parameters. `json:` produces typed JSON: `limit=json:1` sends a number; `limit=1` sends a string. The last command corresponds to this JSON-RPC request over **WebSocket `/api/`**, not an HTTP POST example:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

Inventory filters and output projection are selection tools, **not access boundaries**. Do not assume this API restricts inventory to the objects displayed in a user's UI, or that omitted output fields were never fetched. Keep results private and validate actual account visibility separately. A label is not a stable ID; this limited result is not a complete inventory or a deterministic choice of VM.

## 4. Revoke and clean up

In the independent browser session for the same test user, open **User → Authentication tokens** (`/#/user`) and delete the token associated with this CLI client. Before deleting local credentials, run the first command below and expect a nonzero exit with authentication refusal. Success means revocation has not been established; investigate the account/token before claiming it worked.

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

`unregister` only removes local `server` and `token` fields. It does **not** revoke the server token. Removing the temporary directory is local cleanup, not a substitute for revocation. Close the dedicated shell afterwards. For durable automation, design secret storage, renewal, revocation, error handling and narrowly authorized operations separately.

## Sources

[xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [client storage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js), [token API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [token expiry](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [inventory API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [profile tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
