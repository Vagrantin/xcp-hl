---
title: Komponenten
weight: 7
translationKey: components
aliases: ["/de/developers/"]
---

Alles, was Sie zum Verständnis, zum Build und zur Mitarbeit an XCP-hl benötigen.
{class="lead"}

## Repository-Überblick {#repository-overview}

XCP-hl ist auf mehrere funktionale Repositorys und dieses Dokumentationsrepository aufgeteilt.

```
Vagrantin/xcp-hl          ← docs (this site)
      │
      ├── Vagrantin/xolite-ce       ← XO Lite patch + RPM build
      │         │ publishes signed RPM as GitHub Release artifact
      │         │
      ├─────────│───Vagrantin/xoa-proxy           ← Rust HTTP proxy + RPM build
      │         │        │  publishes signed RPM as GitHub Release artifact
      │         ▼        ▼
      ├── Vagrantin/xcp-ng-ce-iso   ← ISO assembly + ISO GitHub Releases
      │         │ downloads RPM from xolite-ce and xoa-proxy, assembles ISO
      │
      ├── Vagrantin/xoa-hl          ← XOA-hl: patched Xen Orchestra (RPM + container)
      │         ▼
      ├── Vagrantin/build-xoa-hl    ← Packer pipeline → XOA XVA image on XCP-ng
      │         │ publishes the XVA as a GitHub Release (xoa-image-* tags)
      │
```

Jedes Repository hat eine eigene GitHub-Actions-Pipeline. Sie sind **lose gekoppelt**: `xolite-ce` und `xoa-proxy` veröffentlichen versionierte RPM-Artefakte, die `xcp-ng-ce-iso` anhand des Release-Tags abruft. Für reguläre Builds müssen diese Repositorys nicht gemeinsam ausgecheckt werden. `xoa-hl` erstellt das für die Community angepasste Xen Orchestra (XOA-hl), und `build-xoa-hl` verpackt es als XVA-Image.

---

## Technologiestack {#tech-stack}

| Schicht | Technologie |
|---|---|
| Hypervisor-Basis | XCP-ng 8.3 (Xen 4.17, Linux 4.19 Dom0) |
| XO-Lite-Oberfläche | Vue 3 · TypeScript · Vite · Pinia (`@xen-orchestra/lite`) |
| XO-Lite-Build | Yarn (Corepack) · `yarn build:xo-lite` |
| RPM-Paketierung | `rpmbuild`, `rpmsign`, `createrepo_c` |
| ISO-Zusammenstellung | `create-install-image` (XCP-ng-Toolchain, master-Branch) |
| ISO-Werkzeuge | `mksquashfs`, `xorriso`, `isohybrid`, `implantisomd5` |
| XOA-hl-Build | Node.js 24 · Yarn-Workspaces · AlmaLinux-9-Container |
| XVA-Image-Build | Packer · Plugin `ddelnano/xenserver` · Kickstart |
| Buildumgebung | Docker (`xcp-ng-build-env:8.3`) |
| Proxyserver | Rust · `hyper` · `tokio` · `tokio_util::io::ReaderStream` |
| CI/CD | GitHub Actions |
| Signierung | GPG: Offline-Hauptschlüssel und 2 Signatur-Unterschlüssel (siehe unten) |

---

<span id="build-orchestration"></span>

## Buildpipeline von Anfang bis Ende {#build-pipeline-end-to-end}

```
1. xolite-ce CI (GitHub Actions)
   ├── Clone vatesfr/xen-orchestra at the tag pinned in UPSTREAM_TAG
   │   (currently xo-lite-v0.21.0, bumped deliberately, not automatically)
   ├── Apply patches/community-xoa-deploy.patch
   ├── yarn build:xo-lite
   ├── rpmbuild → xo-lite-community-<VERSION>.rpm
   ├── rpmsign with RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
   └── Publish signed RPM as GitHub Release asset (public key on
       keys.openpgp.org; import steps in the release notes)

2. xoa-proxy CI (GitHub Actions)
   ├── Install musl toolchain (musl-1.2.4, static libc)
   ├── Install Rust stable via rustup
   ├── Add x86_64-unknown-linux-musl target
   ├── cargo build --release --target x86_64-unknown-linux-musl
   ├── Prepare RPM sources (binary + systemd unit + logrotate config)
   ├── rpmbuild → xoa-proxy-<VERSION>.rpm
   ├── rpmsign with RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
   └── Publish signed RPM as GitHub Release asset (public key on
       keys.openpgp.org; import steps in the release notes)

3. xcp-ng-ce-iso CI (GitHub Actions)
   ├── Download signed RPM from xolite-ce release
   ├── Download signed RPM from xoa-proxy release
   ├── Import GPG_PRIVATE_KEY (ISO signing subkey) into runner keyring
   ├── Export public key from runner keyring → inject into installer chroot
   ├── Set up community-repo/x86_64/ with createrepo_c
   ├── Run create-installimg.sh (root): builds install.img (SquashFS)
   ├── Run create-iso.sh (non-root): assembles ISO
   ├── isohybrid --uefi (hybrid MBR/GPT stamp)
   ├── implantisomd5
   ├── sha256sum → xcp-ng-8.3-ceN.iso.sha256
   ├── gpg --detach-sign  (ISO signing subkey via GPG_PRIVATE_KEY)
   └── Publish xcp-ng-8.3-ceN.iso + .iso.sha256 + .iso.sha256.asc as a
       Vagrantin/xcp-ng-ce-iso GitHub Release (public key on
       keys.openpgp.org; verification steps in the release notes)

4. xoa-hl CI (GitHub Actions, on a v<VERSION>-ceN tag)
   ├── Shallow-fetch vatesfr/xen-orchestra at the commit pinned in UPSTREAM_XO
   │   (currently 5.113.2, the last XO 5.x release, bumped deliberately)
   ├── Apply patches/*.patch (menu-hide-items, xcp-hl-updates, xoa-hl-update-api)
   ├── Write xoahl.config.toml + generate self-signed TLS certificate
   ├── yarn && yarn build (all workspaces), prune, strip devDependencies
   ├── tar → xoa-hl-<VERSION>.tar.gz (build input only, not published)
   ├── rpmbuild → xoa-hl-<VERSION>-N.….x86_64.rpm (the whole pre-built XO)
   ├── Publish the RPM as a v<VERSION>-ceN GitHub Release
   └── Republish the 5 newest RPMs as a signed yum repository (appliance updates)

5. build-xoa-hl (Packer, on a real XCP-ng host)
   ├── Resolve AlmaLinux ISO checksum + latest xoa-hl RPM release URL
   ├── Generate inst.ks (Kickstart) and almalinux-build.json (Packer template)
   ├── packer build: install AlmaLinux 9 via Kickstart on the XCP-ng host
   ├── Provision: xe-guest-utilities, Node 24, xoa-hl RPM, first-boot units
   ├── Slim the image, blank /etc/machine-id
   └── Export XVA (xva_compressed): the appliance XO Lite CE deploys
```

---

## Entwurfsentscheidungen {#key-design-decisions}

### Drei Repositorys für die ISO-Seite {#three-repo-split-for-the-iso-side}

Hier geht es speziell um die ISO-Pipeline (`xolite-ce`, `xoa-proxy`, `xcp-ng-ce-iso`); das Diagramm oben zeigt die Einordnung der eigenen XOA-hl-Repositorys in die Komponentenübersicht. Durch die Trennung von RPM-Builds und ISO-Zusammenstellung bleiben die Aufgaben klar: `xolite-ce` (UI-Patch, Paketierung) und `xoa-proxy` (Rust-Proxy, Paketierung) können unabhängig voneinander weiterentwickelt werden, ohne die ISO-Toolchain zu ändern, und umgekehrt. Jedes veröffentlicht ein versioniertes, signiertes RPM als GitHub-Release-Artefakt. Diese Artefakte werden anschließend zum Erstellen des ISOs verwendet.

### Patchen auf Quellcodeebene {#patch-at-source-level}

Der XO-Lite-Patch wird auf den Vue-/TypeScript-**Quellcode** von `DeployXoaView.vue` angewendet.

---

## GPG-Signierung {#gpg-signing}

XCP-hl verwendet ein einziges Schlüsselpaar mit dem Modell **Offline-Hauptschlüssel und Unterschlüssel**. Der Hauptschlüssel wird offline aufbewahrt und niemals zum Signieren verwendet. Zwei Signatur-Unterschlüssel werden daraus abgeleitet, einer für beide RPMs und einer für das ISO.

### Schlüsseldetails {#key-details}

| Eigenschaft | Wert |
|---|---|
| Schlüssel-UID | `XCP-ng Community Edition (Master signing key)` (Ausgabe von `gpg --list-keys`) |
| Fingerabdruck des Hauptschlüssels | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Veröffentlicht | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| E-Mail | `xcp-ng-ce.lid530@passmail.com` |
| Öffentliche Schlüsseldatei | `xcp-ng-ce-public.asc` |

### Aufgaben der Unterschlüssel {#subkey-roles}

| Unterschlüssel | Verwendung |
|---|---|
| RPM-Signatur-Unterschlüssel | `xo-lite-community-*.rpm` und `xoa-proxy-*.rpm` |
| ISO-Signatur-Unterschlüssel | `xcp-ng-8.3-ceN.iso.sha256.asc` (abgetrennte Signatur der ISO-Prüfsummendatei) |

---

## Ausführliche Komponentendokumentation {#detailed-component-docs}

| Seite | Beschreibung |
|---|---|
| [xoa-proxy](/docs/components/xoa-proxy) | Rust-HTTP-/gzip-Proxy zur XVA-Bereitstellung |
| [xolite-ce](/docs/components/xolite-ce) | XO-Lite-Patch, RPM-Spezifikation, Buildpipeline |
| [xcp-ng-ce-iso](/docs/components/xcp-ng-ce-iso) | ISO-Zusammenstellung, Toolchain, CI-Workflow |
| [xoa-hl](/docs/components/xoa-hl) | Angepasstes Xen Orchestra (XOA-hl), als RPM gebaut und verpackt |
| [build-xoa-hl](/docs/components/build-xoa-hl) | Packer-Pipeline zum Erstellen des XOA-XVA-Images auf XCP-ng |
