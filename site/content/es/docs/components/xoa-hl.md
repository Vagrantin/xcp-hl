---
title: xoa-hl
weight: 4
translationKey: xoa-hl
aliases: ["/developers/xoa-hl.html"]
---

Compilación del software XOA-hl: modifica Xen Orchestra para laboratorios domésticos y lo empaqueta como RPM.
{class="lead"}

**Repositorio:** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· Lenguaje: Bash / especificación RPM · Licencia: AGPL-3.0

## Objetivo {#purpose}

Este repositorio construye **Xen Orchestra HomeLab Edition** (XOA-hl): el servidor completo de código abierto [`xen-orchestra`](https://github.com/vatesfr/xen-orchestra) y la interfaz web XO 5, descargados en un commit original fijo, modificados para laboratorios domésticos y empaquetados para XCP-ng. Cada compilación publica un artefacto como publicación de GitHub:

| Artefacto | Contenido |
|---|---|
| `xoa-hl-<version>-<N>.g<commit>.xcpng8.3.el9.x86_64.rpm` | Xen Orchestra precompilado (unos 70 MiB), sus unidades systemd y las herramientas de actualización del appliance |

Este es el RPM que [`build-xoa-hl`](/docs/components/build-xoa-hl) instala en la VM del appliance XOA. Los repositorios RPM publicados proporcionan las actualizaciones del appliance; consulta la guía de [Actualizaciones](/docs/guides/updates), con alcance por versión, para los canales stable/testing.

---

## Estructura del repositorio {#repo-structure}

```
xoa-hl/
├── UPSTREAM_XO                 ← upstream xen-orchestra pin (commit + version)
├── container/
│   └── Containerfile           ← AlmaLinux 9 build image (Node 24, yarn, rpm tooling)
├── scripts/
│   ├── build-xo.sh             ← the build: fetch + patch + yarn build + tar
│   └── validate-patches.sh     ← checks patches/ against metadata.toml
├── patches/
│   ├── metadata.toml           ← what each patch does and which file it targets
│   ├── menu-hide-items.patch   ← hides Vates-subscription-only menu items
│   ├── xcp-hl-updates.patch    ← adds the XCP-hl repositories to the Patches tab
│   └── xoa-hl-update-api.patch ← the appliance's own "XOA-HL Updates" settings page
├── SPECS/
│   └── xoa-hl.spec             ← the RPM: pre-built XO under /opt/xo + systemd units
├── SOURCES/                    ← systemd units, update scripts, sudoers rule, .repo file
├── pages/                      ← index page + .repo file for the published yum repository
└── .github/workflows/
    ├── build-xoa.yml           ← CI: build + RPM + GitHub Release
    └── pages-repo.yml          ← republishes recent RPMs as a signed yum repository
```

---

## Fijación de la versión {#version-pinning}

La compilación utiliza un commit original fijo, definido en el archivo `UPSTREAM_XO` de la raíz del repositorio:

```bash
XO_COMMIT=e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c
XO_VERSION=5.113.2
```

La cadena de versión combina ambos valores: `<XO_VERSION>_<short SHA>` → por ejemplo, `5.113.2_e281c536`. `build-xo.sh` la escribe en `out/VERSION` y CI la utiliza como versión del RPM. Se crea una publicación al subir una etiqueta `v<version>-ce<N>`, por ejemplo, `v5.113.2_e281c536-ce17`: `N` se convierte en el número release del RPM, de modo que cada compilación es un paquete distinto al que `dnf` puede actualizar.

{{< callout type="info" >}}
La versión original se actualiza **deliberadamente**, editando `UPSTREAM_XO`, nunca de forma automática. `5.113.2` es la última versión XO 5.x anterior al paso del proyecto original a XO 6.
{{< /callout >}}

---

## Flujo de compilación, scripts/build-xo.sh {#build-flow-scriptsbuild-xosh}

La compilación se ejecuta dentro del contenedor AlmaLinux 9 y trabaja en `/build`:

1. **Descarga superficial del SHA fijo**, `git init` + `git fetch --depth 1 origin $XO_COMMIT` + `checkout FETCH_HEAD`. Fijar un SHA directamente con `--depth 1` evita descargar todo el historial de aproximadamente 1 GB y mantiene la reproducibilidad.
2. **Aplicación de parches**, después de comprobar que cada `patches/*.patch` tiene una entrada en `patches/metadata.toml` y viceversa; cada parche se aplica con `git apply --verbose`. En ce40 hay 16 parches declarados; algunos ejemplos:
   - `menu-hide-items` oculta determinadas opciones de menú fuera del alcance HomeLab; no demuestra que todas las API asociadas estén ausentes.
   - `xcp-hl-updates` añade los repositorios XCP-hl a la consulta que Xen Orchestra envía al complemento `updater.py` del host, para que los paquetes XCP-hl aparezcan en la pestaña Patches.
   - `xoa-hl-update-api` añade la API de actualización del appliance y la página de ajustes **XOA-HL Updates**.
3. **Escritura de `packages/xo-server/xoahl.config.toml`**, la configuración de ejecución que el RPM instala después como configuración de usuario: HTTPS en el puerto 443 con `/opt/xo/xoahl.crt` / `/opt/xo/xoahl.key`, Redis en `redis://127.0.0.1:6379/0`.
4. **Generación de TLS aplazada hasta instalar el RPM.** La compilación ce40 no distribuye una clave privada compartida. `%post` genera el par inicial en el appliance (RSA 4096, 3650 días, CN `xoa.local`; modo 600 para la clave, 644 para el certificado).
5. **Instalación y compilación**, `yarn` seguido de `yarn build` en todos los espacios de trabajo (servidor e interfaz web XO 5).
6. **Limpieza**, eliminando `.git`, `.github`, `.changesets`, `docs`, `packages/xo-server-test*` y `packages/xo-server-cloud`.
7. **Eliminación de devDependencies**, `yarn workspaces focus --production` (alternativa: `yarn install --production`), conservando los enlaces simbólicos de los espacios de trabajo.
8. **Empaquetado**, `tar czf out/xoa-hl-<version>.tar.gz` de todo el monorepositorio depurado, excluyendo `**/*.map`. El archivo tar solo es una entrada para construir el RPM; no se publica.

---

## El RPM, SPECS/xoa-hl.spec {#the-rpm-specsxoa-hlspec}

El RPM contiene Xen Orchestra precompilado, unos 70 MiB. Es `x86_64`, no `noarch`, porque el árbol `node_modules` contiene extensiones nativas. Instala:

| Ruta | Contenido |
|---|---|
| `/opt/xo` | xen-orchestra precompilado; par TLS `xoahl.key` / `xoahl.crt` generado durante la instalación |
| `/usr/local/bin/xo-cli` | `xo-cli` disponible en `PATH` |
| `/usr/lib/systemd/system/xo-server.service` | Ejecuta xo-server desde `/opt/xo` |
| `/usr/lib/systemd/system/xoa-hl-check-update.service` y `xoa-hl-update.service` | Comprueban y aplican las actualizaciones del appliance |
| `/usr/libexec/xoa-hl/` | Scripts que ejecutan esas dos unidades |
| `/etc/yum.repos.d/xoa-hl.repo` | Repositorio yum propio del appliance |
| `/etc/sudoers.d/xoa-hl` | Permite a xo-server iniciar las dos unidades de actualización |
| `/var/lib/xoa-hl/` | Destino del registro de actualizaciones |

Durante la instalación, `%post`:

1. **Inicializa la configuración de usuario solo en la primera instalación**, copiando `xoahl.config.toml` a `/root/.config/xo-server/config.toml` si no existe. Durante las actualizaciones se deja intacta para conservar las personalizaciones del operador.
2. Genera TLS si falta el par o el marcador `/var/lib/xoa-hl/tls-generated`; el marcador permite sustituir material compartido antiguo.
3. Ejecuta `systemctl enable redis --now` y activa `xo-server`. Los temporizadores de actualización permanecen desactivados hasta configurarlos explícitamente.

`%posttrans` reinicia `xo-server` una vez terminada la transacción de paquetes.

`%preun` detiene y desactiva `xo-server` únicamente al desinstalarlo definitivamente, no al actualizarlo. La eliminación del RPM borra los archivos que le pertenecen; pueden conservarse la configuración del operador y los datos de ejecución sin propietario. `%postun` recarga systemd en la desinstalación definitiva.

{{< callout type="error" >}}
xo-server lee `~/.config/xo-server/config.toml` (búsqueda XDG), que prevalece sobre cualquier `config.toml` del paquete. Sin la inicialización de `%post`, no se aplicarían el listener HTTPS ni la URI de Redis, independientemente del contenido del paquete.
{{< /callout >}}

Dependencias de ejecución en ce40: Node.js 24 (inferior a 25), OpenSSL, Redis, `dnf-plugins-core` y los asistentes de montaje que necesita Xen Orchestra para los destinos remotos (`nfs-utils`, `cifs-utils`, `ntfs-3g`, `lvm2`). El paquete tiene `Epoch: 1`, por lo que prevalece sobre las compilaciones anteriores al esquema actual de numeración.

---

## Entorno de compilación {#build-environment}

`container/Containerfile` define la imagen de compilación: AlmaLinux 9 con gcc/make/git/patch, Python 3, Node.js 24 (NodeSource), yarn y `rpm-build`/`rpmdevtools`. La misma imagen construye el archivo tar y el RPM.

Las compilaciones se ejecutan **exclusivamente en GitHub Actions**; no existe un flujo de compilación local. CI construye la imagen con Docker y ejecuta `build-xo.sh` dentro de ella; el archivo tar y `VERSION` quedan en `out/` en el ejecutor y alimentan la compilación RPM.

---

## Flujo CI (GitHub Actions) {#ci-workflow-github-actions}

`.github/workflows/build-xoa.yml` se activa al subir una etiqueta `v*-ce<N>` y mediante `workflow_dispatch`:

1. Comprueba la sintaxis de todos los scripts de shell: `scripts/*.sh` con `bash`, y los `SOURCES/*.sh` que se incluyen en el RPM con `sh`.
2. Construye la imagen del contenedor y ejecuta `build-xo.sh` dentro de ella (montando `patches/`, `scripts/`, `out/` y `UPSTREAM_XO`).
3. Lee `out/VERSION` y toma `N` de la etiqueta como número release del RPM.
4. Ejecuta `rpmbuild -bb SPECS/xoa-hl.spec` dentro de la misma imagen, con el archivo tar preparado en `SOURCES/`.
5. Publica una versión de GitHub con el nombre de la etiqueta, que contiene el RPM.

`.github/workflows/pages-repo.yml` publica determinados RPM de versiones con metadatos firmados del repositorio. La configuración del repositorio del appliance define los endpoints; consulta [Actualizaciones](/docs/guides/updates) para distinguir stable/testing.

Las **publicaciones de imágenes de VM** creadas por `xoa-vm-agent` del orquestador (prefijo de etiqueta `xoa-image-`, artefacto `XOA-hl.xva`) se publican en [`build-xoa-hl`](/docs/components/build-xoa-hl), el repositorio desde el que se construye la imagen; consulta [#22](https://github.com/Vagrantin/xcp-hl/issues/22).

{{< callout type="warning" >}}
Las imágenes publicadas antes de ese traslado permanecen aquí para que las ISO ya distribuidas puedan seguir resolviéndolas. Las herramientas que busquen RPM en este repositorio deben seguir omitiendo las etiquetas `xoa-image-*`.
{{< /callout >}}

---

## Relación con otros componentes {#relationship-to-other-components}

- [`build-xoa-hl`](/docs/components/build-xoa-hl) instala este RPM en el appliance AlmaLinux 9 y lo empaqueta como imagen XVA.
- [`xolite-ce`](/docs/components/xolite-ce): su botón de despliegue XO Lite instala ese appliance.
- [`xoa-proxy`](/docs/components/xoa-proxy): puente HTTPS/gzip utilizado durante la entrega de la imagen del appliance.
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator) (en el repositorio `buildorchestration`): su `xoa-vm-agent` activa `build-xoa.yml` y espera la publicación del RPM antes de iniciar la construcción de la imagen de VM.

---

## Contribuciones {#contributing}

Para informar de un problema o proponer un cambio, abre una incidencia en [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).

## Alcance de la versión revisada {#reviewed-release-scope}

`v5.113.2_e281c536-ce40` / `xoa-hl@a28085219cdfe9d20700e6060377f5059e42e6b5`.

[UPSTREAM_XO](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [script de compilación](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [RPM](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [metadatos de parches](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/metadata.toml).
