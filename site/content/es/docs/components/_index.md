---
title: Componentes
weight: 7
translationKey: components
aliases: ["/es/developers/"]
---

Todo lo que necesitas para comprender, construir y contribuir a XCP-hl.
{class="lead"}

## Resumen de los repositorios {#repository-overview}

XCP-hl se divide en varios repositorios funcionales, además de este repositorio de documentación.

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

Cada repositorio tiene su propio proceso de GitHub Actions. Están **acoplados de forma flexible**: `xolite-ce` y `xoa-proxy` publican artefactos RPM versionados que `xcp-ng-ce-iso` descarga por etiqueta de publicación. No es necesario descargar juntos los repositorios para las compilaciones habituales. `xoa-hl` construye Xen Orchestra con los parches comunitarios (XOA-hl), y `build-xoa-hl` lo empaqueta en una imagen XVA.

---

## Pila tecnológica {#tech-stack}

| Capa | Tecnología |
|---|---|
| Base del hipervisor | XCP-ng 8.3 (Xen 4.17, Linux 4.19 Dom0) |
| Interfaz de XO Lite | Vue 3 · TypeScript · Vite · Pinia (`@xen-orchestra/lite`) |
| Compilación de XO Lite | Yarn (Corepack) · `yarn build:xo-lite` |
| Empaquetado RPM | `rpmbuild`, `rpmsign`, `createrepo_c` |
| Ensamblado de la ISO | `create-install-image` (herramientas de XCP-ng, rama master) |
| Herramientas ISO | `mksquashfs`, `xorriso`, `isohybrid`, `implantisomd5` |
| Compilación de XOA-hl | Node.js 24 · Espacios de trabajo Yarn · Contenedor AlmaLinux 9 |
| Construcción de la imagen XVA | Packer · Complemento `ddelnano/xenserver` · Kickstart |
| Entorno de compilación | Docker (`xcp-ng-build-env:8.3`) |
| Servidor proxy | Rust · `hyper` · `tokio` · `tokio_util::io::ReaderStream` |
| CI/CD | GitHub Actions |
| Firma | GPG: clave maestra sin conexión y 2 subclaves de firma (véase abajo) |

---

<span id="build-orchestration"></span>

## Proceso de compilación de principio a fin {#build-pipeline-end-to-end}

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

## Decisiones de diseño {#key-design-decisions}

### División en tres repositorios para la ISO {#three-repo-split-for-the-iso-side}
Esto se refiere específicamente al proceso de la ISO (`xolite-ce`, `xoa-proxy`, `xcp-ng-ce-iso`); el diagrama anterior muestra cómo encajan los repositorios de XOA-hl en el conjunto de componentes. Separar cada compilación RPM del ensamblado de la ISO mantiene claras las responsabilidades: `xolite-ce` (parches de la interfaz, empaquetado) y `xoa-proxy` (proxy Rust, empaquetado) pueden evolucionar independientemente sin tocar las herramientas ISO, y viceversa. Cada uno publica un RPM versionado y firmado como artefacto de una publicación de GitHub. Esos artefactos se consumen después para construir la ISO.

### Parchear el código fuente {#patch-at-source-level}
El parche de XO Lite se aplica al **código fuente** Vue/TypeScript de `DeployXoaView.vue`.

---

## Firma GPG {#gpg-signing}

XCP-hl utiliza un solo par de claves siguiendo el modelo de **clave maestra sin conexión y subclaves**. La clave maestra se conserva sin conexión y nunca se utiliza para firmar. De ella se derivan dos subclaves de firma: una para ambos RPM y otra para la ISO.

### Detalles de la clave {#key-details}

| Propiedad | Valor |
|---|---|
| UID de la clave | `XCP-ng Community Edition (Master signing key)` (como muestra `gpg --list-keys`) |
| Huella de la clave maestra | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Publicada en | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Correo electrónico | `xcp-ng-ce.lid530@passmail.com` |
| Archivo de clave pública | `xcp-ng-ce-public.asc` |

### Funciones de las subclaves {#subkey-roles}

| Subclave | Uso |
|---|---|
| Subclave de firma RPM | `xo-lite-community-*.rpm` y `xoa-proxy-*.rpm` |
| Subclave de firma ISO | `xcp-ng-8.3-ceN.iso.sha256.asc` (firma separada del archivo de suma de comprobación de la ISO) |

---

## Documentación detallada de los componentes {#detailed-component-docs}

| Página | Descripción |
|---|---|
| [xoa-proxy](/docs/components/xoa-proxy) | Proxy HTTP/gzip en Rust para distribuir XVA |
| [xolite-ce](/docs/components/xolite-ce) | Parche de XO Lite, especificación RPM y proceso de compilación |
| [xcp-ng-ce-iso](/docs/components/xcp-ng-ce-iso) | Ensamblado de la ISO, herramientas y flujo CI |
| [xoa-hl](/docs/components/xoa-hl) | Xen Orchestra modificado (XOA-hl), construido y empaquetado como RPM |
| [build-xoa-hl](/docs/components/build-xoa-hl) | Proceso Packer para construir la imagen XOA XVA en XCP-ng |
