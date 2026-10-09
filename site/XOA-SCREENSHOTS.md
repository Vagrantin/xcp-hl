# Jenkins appliance screenshot job — #197

## Job contract

Run `site/scripts/capture_xoa_screenshots.cjs` from the `xcp-hl` documentation
checkout on a Jenkins agent able to reach a **dedicated XOA-HL lab appliance**.
This is separate from GitHub's static-site browser job. The script logs in and
reads prepared screens; it does not create, start, stop, delete or restore VMs,
change passwords, add hosts, import an ISO, update packages or run backups.
Language selection uses a cookie in its temporary browser context.

First run is a lab pilot: selectors were checked against the patched XO 5
source, but have not been exercised against a running appliance here. A green
capture job does not complete D2 lab acceptance. Use
[XOA-BEGINNER-VALIDATION.md](XOA-BEGINNER-VALIDATION.md) for that separate record.

## Prepare the lab once

1. Deploy the recorded image (initial baseline
   `xoa-image-20261009-5f33c81`) on a disposable XCP-HL host/pool. Use a dedicated
   web administrator account with a unique password. The job does not use host
   root or SSH credentials. Do not put private workloads in its inventory.
2. Connect the lab host. Use documentation-friendly labels such as `docs-lab`,
   `lab-first-vm` and `lab-guests`. Ensure no real names, private hostnames,
   credentials, tokens or production data appear in guest consoles or inventory.
3. Import a verified OS installation ISO into the lab ISO SR. Create and install
   `lab-first-vm`; leave it running at a harmless guest console (no password on
   screen), with its installer ISO ejected.
4. Record the pool, installation-template, ISO-SR and VM UUIDs in Jenkins
   parameters; these select existing objects. The wizard capture uses pool and
   template query parameters and never presses Create. It illustrates the
   wizard's initial state, not a fully filled example or a completed installation.
5. Open About privately and copy its exact application and VM version values
   into the job parameters. Record host and guest releases. The script waits for
   those About values to render before accepting that screenshot.

## Agent and parameters

Use an isolated Linux agent/container with Node 24, Playwright **1.62.1**, its
matching Chromium and required Linux libraries, plus fonts supporting French and
Japanese (for example Noto CJK). Pin the container digest when maintaining the
job. Provision browser/system dependencies in the agent image rather than
requiring root privileges during a capture. Set the lab timezone consistently.

Store `XOA_SCREENSHOT_LOGIN` and `XOA_SCREENSHOT_PASSWORD` as a Jenkins
username/password credential. Bind them only for the capture stage. Use shell
`set +x`; do not interpolate secrets into Groovy or command-line arguments.
Do not publish Jenkins logs containing credential dumps or enable Playwright
DEBUG, trace, video, HAR or saved authentication state.

| Parameter | Value |
| --- | --- |
| `XOA_SCREENSHOT_BASE_URL` | HTTPS XO 5 UI base, normally `https://<lab-appliance>/`; no query, hash or credentials |
| `XOA_SCREENSHOT_IMAGE_TAG` | Deployed image tag |
| `XOA_SCREENSHOT_APP_VERSION` | Exact application-version value shown in About |
| `XOA_SCREENSHOT_VM_VERSION` | Exact VM-version value shown in About |
| `XOA_SCREENSHOT_HOST_RELEASE` | Observed host release / ISO identity |
| `XOA_SCREENSHOT_GUEST_OS` | Observed guest OS / installation ISO identity |
| `XOA_SCREENSHOT_POOL_UUID` | Existing connected lab pool UUID |
| `XOA_SCREENSHOT_TEMPLATE_UUID` | Installation template UUID in that pool |
| `XOA_SCREENSHOT_ISO_SR_UUID` | Existing ISO SR UUID |
| `XOA_SCREENSHOT_VM_UUID` | Existing installed test VM UUID |
| `XOA_SCREENSHOT_VM_NAME` | Exact fixture name, for example `lab-first-vm` |
| `XOA_SCREENSHOT_ISO_NAME` | Exact imported ISO name shown in SR disks |
| `XOA_SCREENSHOT_LOCALES` | `en,fr,ja` (default); `en` for the first connectivity pilot |
| `XOA_SCREENSHOT_ALLOW_SELF_SIGNED` | Default false; set `true` only for the identified self-signed lab endpoint |
| `XOA_SCREENSHOT_MASK_SELECTORS` | Optional JSON array of additional CSS selectors to mask |
| `XOA_SCREENSHOT_OUTPUT` | New empty output directory, default `xoa-captures`; existing directory is rejected |

The script masks password inputs, the current web login and server address/
username columns. Those masks do not find all sensitive text, canvases or
private inventory names. The sanitized lab and private artifact review are
required. Do not set global TLS verification overrides.

## Suggested Jenkins stage

The agent image must already contain Node, Chromium dependencies and fonts.
The Jenkins job checks out the documentation branch/ref and supplies the
non-secret parameters above as environment variables.

```groovy
stage('Capture XOA-HL documentation') {
  steps {
    withCredentials([usernamePassword(
      credentialsId: 'xoa-hl-docs-lab',
      usernameVariable: 'XOA_SCREENSHOT_LOGIN',
      passwordVariable: 'XOA_SCREENSHOT_PASSWORD'
    )]) {
      sh '''
        set +x
        set -eu
        unset DEBUG PWDEBUG
        npm install --prefix "$WORKSPACE/capture-tools" --no-audit --no-fund playwright@1.62.1
        export PLAYWRIGHT_MODULE="$WORKSPACE/capture-tools/node_modules/playwright"
        export PLAYWRIGHT_BROWSERS_PATH="$WORKSPACE/capture-browsers"
        node "$WORKSPACE/capture-tools/node_modules/playwright/cli.js" install chromium
        export XOA_SCREENSHOT_OUTPUT="$WORKSPACE/xoa-captures-$BUILD_NUMBER"
        node site/scripts/capture_xoa_screenshots.cjs
      '''
    }
    // Runs only if capture succeeded; failed/partial artifacts stay private.
    archiveArtifacts artifacts: "xoa-captures-${env.BUILD_NUMBER}/**", fingerprint: true
  }
}
```

Restrict build access and artifact retention to the documentation maintainers.
Run manually initially, not on arbitrary untrusted PR code with lab secrets.
Use a trusted reviewed checkout. Keep this job off public CI and do not add
appliance credentials to GitHub Pages or the website repository.

## Captures requested for the current chapters

| File stem (in each locale directory) | Screen | Purpose |
| --- | --- | --- |
| `01-user-language` | User, with password fields empty | Locate password and language settings |
| `02-connected-host` | Settings → Servers, prepared connection | Distinguish enabled from a successful connection |
| `03-about-versions` | About | Identify application/image versions |
| `04-iso-library` | Prepared ISO SR → Disks | Show the imported installation media |
| `05-new-vm-wizard` | New → VM with pool/template selected | Locate wizard sections before creation |
| `06-vm-console` | Installed running fixture → Console | Show where to access the guest console |
| `07-vm-disks` | Same VM → Disks, ISO ejected | Show the virtual disk and CD drive |

The script uses `/#/...` XO 5 hash routes, not XO 6 navigation. It generates
21 PNGs when all three locales are selected, `manifest.json` (versions, browser,
locale, viewport, timestamp, documentation commit, review status) and
`SHA256SUMS`. No credentials or target URL/UUIDs are intentionally written to
the manifest. Full-page captures should be cropped for readability after review.

The console screenshot checks the canvas and VM label, not guest boot success.
Before delivery, privately review that every screenshot shows the intended
screen, an actual connected host and ISO, a useful guest console and no private
data. Return the reviewed archive and lab record in #197. Do not commit raw
captures automatically. We will select useful images, add localized captions/
alt text, include visible version/language context and commit them under
`site/assets/images/xoa-hl/`. The current prose intentionally contains no fake
screenshots or placeholder figures.

## Later expansion: backup and isolated restore

After those chapters have source-checked procedures, extend the manifest/job
with a dedicated independent backup target, a completed sample job, successful
job log and restored test VM on an isolated network. Keep backup credentials
in Jenkins; never publish a target URL with credentials. Separate a job that
performs explicitly authorized lab actions from this capture-only job. Report
observed backup/restore results, target type, job ID (anonymized), restored VM
identity, network isolation and checked guest data. A screenshot alone is not
restore validation. This later fixture is not required to run today's pilot.

Source selectors: `xo-server/signin.pug`, `xo-web/src/common/store/reducer.js`,
`xo-web/src/xo-app/user/index.js`, `settings/servers/index.js` and
`new-vm/index.js` in the XO 5 pin
`e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`, with XOA-HL patches at
`5f33c81f1ae2e74a300dcc33103f4e06cf565c19`.
