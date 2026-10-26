---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/developers/xolite-ce.html"]
---

XO Lite recompilado para XCP-hl: selección de imágenes de despliegue XOA y proceso de compilación RPM.
{class="lead"}

**Repositorio:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Lenguaje: TypeScript / Vue 3 (parche) · Especificación RPM · Licencia: AGPL-3.0

## ¿Qué es XO Lite? {#what-is-xo-lite}

XO Lite es la aplicación ligera de gestión de una sola página incluida en cada host XCP-ng. Se ejecuta íntegramente en el navegador, servida directamente por el host, y se implementa como una SPA con Vue 3 / TypeScript / Vite.

En un host XCP-ng estándar, la pantalla **"Deploy XOA"** de XO Lite descarga e importa una imagen fija de Xen Orchestra. XCP-hl sustituye esa pantalla por un selector **"XOA Image URL"** que ofrece cuatro orígenes: XOA-hl (predeterminado), la imagen oficial de Vates, la imagen de Ronivay o una URL XVA personalizada; además, añade el interruptor **"Verify if ssl certificate is valid"** para que `xoa-proxy` pueda aceptar certificados autofirmados en el servidor de origen.

---

## El parche {#the-patch}

Los parches se aplican con la herramienta Rust `xoa-deploy-patcher`, que modifica `xoa-deploy.vue` mediante patrones durante la compilación. También aplica `patches/en-hl.json` (cadenas de idioma HL) y `patches/xolite-loader.html` (cargador de sustitución que elimina el recurso de carga remota desde `lite.xen-orchestra.com`).

La pantalla modificada **"Deploy XOA"** incorpora un selector **"XOA Image URL"** con cuatro orígenes:

  - **XOA-hl** *(predeterminado)*: Xen Orchestra compilado desde el código fuente para XCP-hl
  - **Imagen de Vates**: el appliance oficial
  - **Imagen de Ronivay**: un XO comunitario compilado desde el código fuente
  - **URL personalizada**: cualquier XVA, sin comprimir o con gzip, por HTTP o HTTPS

El interruptor **"Verify if ssl certificate is valid"** permite a `xoa-proxy` aceptar certificados autofirmados del servidor de origen de la imagen.

---

## Proceso de compilación {#build-pipeline}

### Resumen {#overview}

```
1. Read XO_VERSION from the RPM in the upstream XCP-ng ISO
2. Clone vatesfr/xen-orchestra at the matching release tag
3. Apply patches/community-xoa-deploy.patch
4. Install dependencies with Yarn (Corepack)
5. Build XO Lite: yarn build:xo-lite
6. Assemble RPM source tarball
7. rpmbuild -ba SPECS/xo-lite-community.spec
8. rpmsign with the RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
9. Publish RPM + xcp-ng-ce-public.asc as GitHub Release assets
```

### Detección de la versión {#version-detection}

La versión objetivo de XO Lite se obtiene del RPM ya presente en la ISO original de XCP-ng, en lugar de fijarse directamente:

```bash
XO_VERSION=$(rpm -qp --qf '%{VERSION}' xo-lite-*.rpm)
```

Así se garantiza que el RPM comunitario coincida siempre con la versión original y pueda sustituirla directamente.

### Estructura del archivo tar {#tarball-structure}

El archivo fuente que recibe `rpmbuild` tiene esta estructura:

```
xo-lite-{VERSION}/
├── dist/               ← compiled Vite output
├── CHANGELOG.md
├── LICENSE
└── xolite.html         ← renamed from scripts/xolite-loader.html
```

El nombre `xolite.html` es obligatorio: es el punto de entrada que sirve el host XCP-ng para cargar XO Lite en el navegador.

### Especificación RPM {#rpm-spec}

`SPECS/xo-lite-community.spec` define:

- `Name: xo-lite-community`
- `Version: %{XO_VERSION}` (inyectada durante la compilación)
- `Provides: xo-lite` (satisface las dependencias del paquete original)
- `Conflicts: xo-lite` (impide instalarlo junto al RPM original)
- Lista de archivos: contenido de `dist/` y `xolite.html`

---

## Desarrollo local {#local-development}

### Requisitos previos {#prerequisites}

- Node.js 20+ y Yarn (activado mediante `corepack enable`)
- `rpmbuild` (paquete `rpm-build` en RHEL/CentOS/Fedora)
- `rpmsign` (paquete `rpm-sign`)
- La clave pública GPG de la comunidad importada en tu llavero

### Flujo de trabajo {#workflow}

```bash
# 1. Clone the repo
git clone https://github.com/Vagrantin/xolite-ce.git
cd xolite-ce

# 2. Clone upstream xen-orchestra at the target tag
XO_VERSION=<version>
git clone --depth 1 --branch v${XO_VERSION} \
    https://github.com/vatesfr/xen-orchestra.git upstream

# 3. Apply the community patch
cd upstream
git am ../patches/community-xoa-deploy.patch
cd ..

# 4. Install dependencies
cd upstream
corepack enable
yarn install
cd ..

# 5. Build XO Lite
cd upstream
yarn build:xo-lite
cd ..

# 6. Test the UI
scp -r lite/dist/ xcp-ng-host:/opt/xensource/www/
```

### Actualizar el parche para una nueva versión original {#updating-the-patch-for-a-new-upstream-version}

```bash
# In a fresh upstream clone, make the changes manually
# then generate a new patch:
git diff HEAD > ../patches/community-xoa-deploy.patch
# or using format-patch for a clean commit:
git format-patch HEAD~1 -o ../patches/
```

---

## Firma GPG {#gpg-signing}

El RPM `xo-lite-community` se firma con la **subclave de firma RPM** del par de claves de XCP-hl. Esa misma subclave firma el RPM `xoa-proxy`: existe una subclave compartida para todos los RPM comunitarios.

El proyecto publica su [clave pública](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) compartida en la raíz del sitio de producción. Verifica la huella maestra antes de importarla. Los comandos siguientes requieren una implementación de RPM compatible con subclaves de firma. Dom0 de XCP-ng 8.3 utiliza el antiguo RPM 4.11; los hosts instalados validan los metadatos firmados del repositorio mediante `repo_gpgcheck=1`. Conserva sin cambios los ajustes del repositorio de [Actualizaciones](/docs/guides/updates).

Para verificar el RPM localmente:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Flujo CI (GitHub Actions) {#ci-workflow-github-actions}

El flujo se activa con cada push a `main`.

Pasos principales:

```yaml
- name: Detect XO version
  run: echo "XO_VERSION=$(rpm -qp --qf '%{VERSION}' ...)" >> $GITHUB_ENV

- name: Clone upstream at tag
  run: git clone --depth 1 --branch v${{ env.XO_VERSION }} ...

- name: Apply patch
  run: git am patches/community-xoa-deploy.patch

- name: Build XO Lite
  run: |
    corepack enable
    yarn install
    yarn build:xo-lite

- name: Build RPM
  run: rpmbuild -ba SPECS/xo-lite-community.spec

- name: Sign RPM
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import
    echo "${{ secrets.GPG_PASSPHRASE }}" | gpg --passphrase-fd 0 --batch \
      --pinentry-mode loopback --yes --armor
    rpm --addsign RPMS/x86_64/xo-lite-community-*.rpm

- name: Publish release
  uses: softprops/action-gh-release@v1
  with:
    files: |
      RPMS/x86_64/xo-lite-community-*.rpm
      xcp-ng-ce-public.asc
```

---

## Contribuciones {#contributing}

Para informar de un problema o proponer un cambio, abre una incidencia en [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
