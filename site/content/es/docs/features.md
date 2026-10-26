---
title: Características
weight: 3
translationKey: features
aliases: ["/features.html", "/docs/guides/features/"]
---

Versión actual · {{< latest-release part="version" >}} · {{< latest-release part="date" >}} · Basado en XCP-ng 8.3
{class="lead"}

## Plataforma base {#base-platform}

XCP-hl se basa en **XCP-ng 8.3**, con cambios en el instalador, XO Lite, el despliegue de XOA y la distribución de paquetes. La plataforma base utiliza el hipervisor y la pila de administración originales; siguen siendo aplicables los requisitos de hardware y funciones.

| Atributo | Valor |
|---|---|
| Versión base | XCP-ng 8.3 (última revisión del proyecto original) |
| Hipervisor | Xen 4.17 |
| Kernel de Dom0 | Linux 4.19 (kernel de XCP-ng) |
| API de administración | XAPI (Xen API) |
| Red predeterminada | Open vSwitch (OVS) |
| Instalador | Instalador de texto de XCP-ng |

---

## Personalizaciones {#customisations}

### XO Lite modificado {#patched-xo-lite}

XO Lite es la interfaz ligera de gestión de una sola página incluida en cada host XCP-ng. XCP-hl cambia una pantalla: durante la compilación, una herramienta automática reescribe pequeñas partes concretas de `xoa-deploy.vue` (consulta [Componentes](/docs/components/xolite-ce) para conocer el mecanismo exacto).

La versión original de xo-lite se fija mediante el archivo `UPSTREAM_TAG` de `xolite-ce` (actualmente `xo-lite-v0.21.0`, la última versión conocida que funciona) y solo cambia cuando se actualiza deliberadamente esa referencia.

**Qué cambia el parche:**

La pantalla **"Deploy XOA"** tiene ahora un selector **"XOA Image URL"** para elegir tu despliegue de XO.

Todo lo demás en XO Lite (gestión de VM, acceso a consola, exploración de SR y métricas del host) permanece intacto.

### xoa-proxy: distribución local de XVA {#xoa-proxy-local-xva-delivery}

La ISO incluye un **servidor HTTP en Rust** creado para este fin (`xoa-proxy`), que se ejecuta en el host. Sus funciones son:

- Servir la imagen XOA comunitaria, con soporte para el formato comprimido con gzip.
- Admitir HTTP y HTTPS (incluidos los certificados autofirmados).

### Imagen XOA HomeLab *(predeterminada)* {#homelab-xoa-image-default}

La imagen XOA que despliega el proxy es [`xoa-hl`](https://github.com/Vagrantin/xoa-hl): Xen Orchestra compilado desde el código fuente para XCP-hl, con las opciones de menú sujetas a licencia y los avisos de soporte eliminados. Consulta cómo se construye en [Componentes](/docs/components/xoa-hl).

### Imagen XOA de Ronivay {#ronivays-xoa-image}

La imagen XOA que despliega el proxy se construye a partir de [ronivay/XenOrchestraInstallerUpdater](https://github.com/ronivay/XenOrchestraInstallerUpdater), un instalador comunitario de Xen Orchestra autoalojado con buen mantenimiento.

| Detalle | Valor |
|---|---|
| Versión de XO | Sigue la última versión estable de XO |
| Usuario administrador predeterminado | `admin@admin.net` |
| Contraseña de administrador predeterminada | `admin` |
| Usuario SSH | `xo` |
| Contraseña SSH | `xopass` |

{{< callout type="warning" >}}
**Cambia las contraseñas predeterminadas inmediatamente** después del primer inicio de sesión.
{{< /callout >}}

### Imagen XOA de Vates {#vates-xoa-image}

Es la imagen oficial proporcionada por Vates para gestionar varios hosts XCP-ng. En este caso, puedes indicar las credenciales durante el despliegue.

### Imagen personalizada {#custom-image}

Cualquier XVA, sin comprimir o comprimido con gzip, servido por HTTP o HTTPS. Indica tu propia URL en la pantalla de despliegue: tu compilación, una versión antigua que hayas conservado o una imagen alojada en cualquier lugar accesible desde el host. Los campos de credenciales se dejan vacíos para que los rellenes; no se completan de antemano porque XCP-hl no puede saber qué espera esa imagen.

---

## Firma GPG {#gpg-signing}

Todos los artefactos de XCP-hl se firman con la **clave GPG de XCP-hl**, para que cualquiera pueda confirmar que un paquete o una ISO proceden realmente de este proyecto y no han sido alterados. Esta sección es una referencia para verificarlo por tu cuenta; la mayoría puede pasar directamente a [Qué incluye](#what-you-get-full-feature-summary).

### Estructura de la clave {#key-structure}

La clave sigue un modelo de **clave maestra sin conexión y subclaves**:

| Función | Descripción |
|---|---|
| Clave maestra | Solo certificación: se conserva sin conexión y nunca se utiliza para firmar |
| Subclave de firma RPM | Firma todos los paquetes RPM comunitarios (`xo-lite-community`, `xoa-proxy`) |
| Subclave de firma ISO | Firma el archivo de suma de comprobación de la ISO (`xcp-ng-8.3-ceN.iso.sha256.asc`) |

| Propiedad | Valor |
|---|---|
| UID de la clave | `XCP-ng Community Edition (Master signing key)` (como muestra `gpg --list-keys`) |
| Huella de la clave maestra | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Publicada en | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| Correo electrónico | `xcp-ng-ce.lid530@passmail.com` |
| Archivo de clave pública | [`xcp-ng-ce-public.asc`](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) |

El archivo de clave pública contiene ambas subclaves de firma. Basta importarlo una vez para verificar tanto los RPM como la suma de comprobación de la ISO.

---

## Qué incluye (resumen completo de funciones) {#what-you-get-full-feature-summary}

### Hipervisor y administración de hosts {#hypervisor--host-management}

- **Todas las funciones de XCP-ng 8.3**: todos los tipos de VM (HVM, PV, PVH), migración en caliente (XenMotion) y Storage XenMotion.
- **Repositorios de almacenamiento**: LVM local, NFS, iSCSI (LVM y EXT), HBA/FC, XOSTOR (hiperconvergente), SMB y SR de ISO.
- **Biblioteca ISO lista para usar**: se reserva una partición dedicada de 20 GB durante la instalación y se registra como SR de ISO en el primer arranque, para subir imágenes de instalación y crear VM sin configurar el almacenamiento manualmente. Consulta [Almacenamiento ISO](#iso-storage).
- **GPU/vGPU**: passthrough PCI y compatibilidad con NVIDIA GRID vGPU.
- **HA**: alta disponibilidad del pool con reinicio automático de VM cuando falla un host.

### Almacenamiento ISO {#iso-storage}

Por defecto, XCP-ng no tiene dónde guardar las ISO de instalación: no existe ningún SR de ISO, y crearlo implica elegir una ruta, crear un directorio y ejecutar `xe sr-create` manualmente. XCP-hl lo hace por ti.

**Qué obtienes.** Una instalación nueva reserva una partición de 20 GB, la formatea en ext4 con la etiqueta `xcphl-iso`, la monta en `/var/opt/xen/xcp-hl-iso` y la registra en XAPI como SR de ISO llamado **XCP-HL ISO library**. Aparece inmediatamente en Xen Orchestra, para que puedas subir una ISO (*Import → Disk*, seleccionando el SR de ISO) y arrancar una VM con ella sin configuración adicional.

**Requisito de disco.** XCP-hl pide un disco de **100 GB**, que se reparte aproximadamente así:

| Área | Tamaño |
|---|---|
| Particiones del sistema (raíz, copia de seguridad, arranque, registros y swap) | ~41,5 GB |
| Biblioteca ISO | 20 GB |
| SR de almacenamiento local (discos de VM) | ~38,5 GB |

Por debajo de 100 GB, se omite la reserva en lugar de reducir a unos pocos GB el almacenamiento de VM. La instalación se completa y el disco se distribuye exactamente como en XCP-ng original. Simplemente no obtienes biblioteca ISO, y una línea en `/var/log/installer` registra el motivo.

**Dónde se aplica.** El instalador crea la partición, por lo que solo existe en hosts instalados desde una ISO de XCP-hl. Un host instalado desde XCP-ng original al que se añaden después los repositorios de XCP-hl conserva intacta su distribución de discos: no se reparticiona un equipo en ejecución. Esos hosts pueden crear manualmente un SR de ISO de la forma habitual.

Al actualizar un host XCP-hl existente se conserva la partición, ya que las actualizaciones nunca reparticionan, y el SR de ISO se vuelve a detectar mediante su etiqueta de sistema de archivos.

**Advertencia conocida.** Si desconectas el PBD del SR y lo vuelves a conectar *sin* reiniciar, XAPI lo volverá a adjuntar, pero el sistema de archivos quedará desmontado; la biblioteca parecerá vacía hasta que un reinicio la monte de nuevo. Esto es inherente a la gestión de SR de ISO locales (`legacy_mode`) de XCP-ng y afecta del mismo modo al SR integrado de XCP-ng Tools; se restaura con un reinicio o con `mount /var/opt/xen/xcp-hl-iso`.

### XO Lite (gestión rápida desde el navegador) {#xo-lite-browser-based-quick-management}

Disponible en `https://<host-ip>` inmediatamente después de instalar:

- Resumen de pools y hosts (CPU, RAM y almacenamiento de un vistazo).
- Lista de VM: inicio, parada, reinicio y acceso a consola.
- Inspección básica de SR y redes.
- **Despliegue HomeLab**: despliegue de XOA con un clic sin conectividad externa si alojas la imagen XOA en tu red local.

### XOA-hl: la interfaz web de administración {#xen-orchestra-after-xoa-deployment}

Al desplegar la imagen hl obtienes Xen Orchestra en su propia VM. XOA-hl ofrece:

- **Administración de hosts y VM** mediante la interfaz Xen Orchestra 5: inspección de recursos y gestión de máquinas virtuales.
- **Controles de copia de seguridad y programación** de Xen Orchestra compilado desde el código fuente.
- **Actualizaciones del host XCP-hl** en las pestañas Patches del host y del pool, incluidos los repositorios de XCP-hl.
- **Controles de actualización del appliance** en Settings → XOA-HL Updates. El host y el appliance se actualizan por separado.
- **Menús centrados en las tareas**: se ocultan las opciones del actualizador del appliance de Vates, Hub, proxies y XOSTOR; el aviso comunitario enlaza a la documentación de XCP-hl.

Esta descripción se basa en `xoa-hl` `v5.113.2_e281c536-ce20`, que fija Xen Orchestra en `5.113.2`. Las demás imágenes tienen sus propias funciones y mecanismos de actualización. Consulta [Actualizaciones](/docs/guides/updates) y el [componente XOA-hl](/docs/components/xoa-hl).

---

## Limitaciones conocidas de esta versión {#known-limitations-in-this-release}

| Limitación | Estado |
|---|---|
| Xolite-ce: botón Deploy siempre accesible | [#31](https://github.com/Vagrantin/xcp-hl/issues/31): cambiarlo a "Access XOA" tras un despliegue correcto |
| Xoa-proxy: registros en UTC | [#62](https://github.com/Vagrantin/xcp-hl/issues/62): investigación pendiente |
| Xoa-proxy: reducir el número de crates | [#63](https://github.com/Vagrantin/xcp-hl/issues/63): investigación pendiente |
| Xoa-proxy: reducir el uso de memoria | [#64](https://github.com/Vagrantin/xcp-hl/issues/64): xoa-proxy se ejecuta en Dom0; hay que controlar su impacto en memoria |

---

## Publicaciones recientes {#recent-releases}

Las cinco ISO más recientes y las versiones de componentes que incluye cada una. Todas las publicaciones están en la [matriz de versiones](/docs/reference/release-matrix), y los cambios y sus motivos en el [registro de cambios](/docs/reference/changelog).

{{< release-matrix-iso limit="5" rpm="false" >}}
