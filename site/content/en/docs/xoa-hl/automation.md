---
title: "Automate with xo-cli"
linkTitle: "Automation (xo-cli)"
description: "Read inventory with xo-cli using a short-lived token, then revoke the token."
weight: 92
translationKey: xoa-manual-automation
translationStatus: source
sourceRevision: sha256:1589bd49045f0be3f63c5bc36cefb00d0743df48d444c2b44f1954d93850ee30
glossaryTerms: ["appliance", "host", "vm"]
---

Use the xo-cli command-line client that ships with the appliance to read a small inventory with a short-lived token, then revoke the token. Do this test before you write automation that changes a VM. You run the commands in a shell inside the **XOA-HL appliance**, and revoke the token in a browser signed in as the same test user.

{{< callout type="info" >}}
**Applies to** image `xoa-image-20261022-a280852`, package `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2), with `xo-cli` **0.32.2** and `xo-lib` **0.11.1**. Tested on a lab appliance on 2026-10-27.
{{< /callout >}}

## 1. Prepare the shell and TLS trust {#prepare}

**Before you start**

- Check the installed release, as described in [appliance maintenance](/docs/xoa-hl/maintenance/).
- Have a normal test user account and a test VM that you can lose. Test what this user is allowed to do separately, with [Users and permissions](/docs/xoa-hl/permissions/).
- Use an appliance DNS name that matches its certificate. The self-signed `xoa.local` certificate created at installation may need lab DNS or certificate work first.
- Get the appliance's public CA or certificate as a PEM file through a trusted channel. Check its fingerprint by a separate route.

1. Open a new, dedicated Bash session **inside the appliance**. You use the bundled `/usr/local/bin/xo-cli` there.
2. In the example in the next section, replace the PEM file path, the URL and the email address with your own.

`NODE_EXTRA_CA_CERTS` adds your certificate to the trusted list; the host name is still checked. If the TLS check fails, fix the name or the certificate. Never bypass it with `--allowUnauthorized` or `NODE_TLS_REJECT_UNAUTHORIZED=0`.

## 2. Register a short-lived token {#register-token}

The commands below keep the credentials in a new temporary folder, so your existing xo-cli configuration is not touched. `umask 077` makes the new file readable by you only.

- `register` asks for the password. Do not add it as an argument, and never put a token in a URL.
- If the account uses one-time codes (OTP), add `--otp CODE` before the URL, with a current code.

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

The token asks for `1 hour` on purpose. By default the server gives a token 30 days, with a maximum of half a year; the server configuration can change these limits. If you ask for more than the maximum, registration fails with a general error (`unknown error from the peer`); ask for a shorter time.

The token has all the rights of its user: it is not limited to reading. Treat the configuration folder like a password. Keep it out of shell traces, out of backups attached to issues, and out of source control. Registering creates a login token; the next commands only read data.

## 3. Discover and read the inventory {#read-inventory}

Run these commands. Put flags such as `--json` and `--id` before the parameters.

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| Command | What you get |
| --- | --- |
| `list-commands xo.getAllObjects` | The parameters of the method, in readable form. Seeing a method does not mean you are allowed to use it |
| `system.getServerVersion --json` | The server package version, `"5.193.1"` in this release. This is not the XO version (5.113.2) |
| `list-objects --id --name_label --power_state type=VM` | A JSON array with only these properties. No VM state changes |
| `xo.getAllObjects --json …` | A JSON object keyed by object ID, filtered by object type and limited to one object |

The `json:` prefix sends a typed value: `limit=json:1` sends a number, while `limit=1` sends a string. The last command sends this JSON-RPC request over a **WebSocket to `/api/`** (it is not an HTTP POST):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

In this release, every signed-in account can read the whole inventory through the API, even an account with no permissions at all. Filters and selected fields only choose what you see: they are **not access limits**. Do not assume that the API returns only the objects shown in the user's web interface, or that fields left out of the output were never fetched. Keep the results private, and check separately what the account can really see. A name is not a stable ID. This limited result is not a complete inventory, and it is not a reliable way to pick a VM.

## 4. Revoke the token and clean up {#revoke-token}

1. In a separate browser session, signed in as the same test user, select the user icon in the menu to open **User** (`/#/user`).
2. Under **Authentication tokens**, delete the token of this CLI client.
3. Back in the shell, run the first command below before you remove anything locally. It must fail with an authentication error and a nonzero exit code.
4. If it succeeds, the token is not revoked. Stop, and check the account and its tokens before you say that revocation worked.
5. Run the other commands to remove the local credentials, then close the dedicated shell.

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

**Check:** after you delete the token in the browser, the version command fails with an authentication error.

`unregister` only removes the local `server` and `token` entries; it does **not** revoke the token on the server. Removing the temporary folder is only a local cleanup: it does not replace revocation. Lasting automation needs its own design for secret storage, renewal, revocation, error handling and narrowly limited rights; that is not covered here.

{{< details title="Sources" closed="true" >}}
- **Command-line client**: [xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [where the client stores its settings](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js).
- **Tokens and inventory**: [token API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [token expiry](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [inventory API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [tokens on the user page](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
{{< /details >}}
