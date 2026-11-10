---
title: Registro de cambios
weight: 2
translationKey: changelog
aliases: ["/es/changelog.html"]
---

Cambios del proyecto en todos los repositorios de XCP-hl y las incidencias que resuelven. Las versiones de componentes de cada publicación están en la [matriz de versiones](/docs/reference/release-matrix).
{class="lead"}

## Notas de publicación generadas {#generated-release-notes}

{{< changelog-releases >}}

## Cambios anteriores del proyecto {#earlier-project-changes}

## Septiembre de 2026 {#september-2026}

### La VM XOA desplegada se llama XOA-hl, resuelve [#97](https://github.com/Vagrantin/xcp-hl/issues/97) {#the-deployed-xoa-vm-is-named-xoa-hl-fixes-97}

Desplegar el appliance XOA-hl desde XO Lite producía una VM llamada `xoa-almalinux`, el nombre interno de compilación de Packer, en lugar de un nombre de producto. XO Lite no cambia el nombre de lo que importa: `VM.import` conserva el name-label del XVA, que es exactamente el `vm_name` del constructor. La compilación establece ahora `vm_name` en **`XOA-hl`**, tanto en `setup-xoa-builder.sh` de [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) (compilaciones manuales) como en `xoa-vm-agent` del orquestador (el proceso diario que publica las imágenes).

Como Packer deriva el nombre del archivo XVA de `vm_name`, el artefacto de la publicación también cambia de nombre: `xoa-almalinux.xva` pasa a ser `XOA-hl.xva`. Nada resuelve ese artefacto por su nombre: tanto el botón de despliegue de XO Lite como la comprobación de publicaciones del agente eligen el primer artefacto `.xva` / `.xva.gz` de la publicación `xoa-image-*` más reciente, así que las imágenes ya publicadas siguen funcionando y no hay que volver a publicar ninguna ISO.

El nombre se aplica a las imágenes construidas después del cambio. Los appliances ya desplegados conservan su nombre antiguo y pueden renombrarse en XO; los hosts del orquestador con un `/etc/xcp-orchestrator/build.config` anterior al cambio conservan su propio `VM_NAME` (`deploy.sh` nunca sobrescribe una configuración existente) y necesitan actualizar esa clave manualmente.

### Almacenamiento ISO predeterminado, cierra [#2](https://github.com/Vagrantin/xcp-hl/issues/2) y [#46](https://github.com/Vagrantin/xcp-hl/issues/46) {#default-iso-storage-closing-2-and-46}

Un host XCP-ng recién instalado no tiene dónde guardar las ISO de instalación: no existe un SR de ISO y hay que crearlo manualmente con `xe sr-create` sobre un directorio que también debes crear. XCP-hl reserva ahora una partición de 20 GB durante la instalación, la formatea en ext4 con la etiqueta `xcphl-iso`, la monta en `/var/opt/xen/xcp-hl-iso` y la registra en el primer arranque como un SR de ISO llamado **XCP-HL ISO library**, listo para subir imágenes desde Xen Orchestra.

Esto fija el disco mínimo de XCP-hl en **100 GB**: unos 41,5 GB de particiones del sistema, 20 GB de biblioteca ISO y unos 38,5 GB restantes para VM. Por debajo de esa capacidad se omite la reserva, en lugar de reducir a unos pocos GB el almacenamiento de VM, y el disco se distribuye exactamente como en XCP-ng original.

La incidencia [#46](https://github.com/Vagrantin/xcp-hl/issues/46) preguntaba si podía añadirse una ruta específica para ISO al endpoint de subida de XCP-ng. Resultó innecesario: `PUT /import_raw_vdi` es una importación genérica de VDI sin procesar que XO 5 ya utiliza mediante *Import → Disk*, y solo faltaba un SR de ISO en el que importar. No se añadió ningún endpoint nuevo.

El instalador crea la partición, por lo que solo se aplica a instalaciones nuevas de XCP-hl. Nunca se reparticionan los hosts instalados desde XCP-ng original a los que después se añaden los repositorios XCP-hl, y las actualizaciones conservan la partición existente en lugar de recrearla.

Se implementa parcheando `host-installer` dentro de `install.img` durante la compilación de la ISO, en lugar de distribuir un RPM bifurcado de `host-installer`. Consulta [xcp-ng-ce-iso](/docs/components/xcp-ng-ce-iso#host-installer-patching).

## Agosto de 2026 {#august-2026}

### La matriz de versiones indica el paquete exacto distribuido, avance de [#15](https://github.com/Vagrantin/xcp-hl/issues/15) {#release-matrix-states-the-exact-package-shipped-towards-15}

La [matriz de versiones](/docs/reference/release-matrix) solo registraba una etiqueta de publicación por componente. Para `xoa-proxy` no bastaba para identificar qué ejecuta un host: la etiqueta corresponde a una versión, pero el campo release del RPM contiene la ejecución CI y el commit de origen, y las dos filas más antiguas usan una etiqueta de ejecución `v-proxy-automated-*` que no indica ninguna versión.

Cada fila por ISO muestra ahora el paquete tal como lo imprime `rpm -q` (`xoa-proxy-0.1.1.8-55.gc525575.static.x86_64`) bajo una versión que enlaza su publicación, tanto para la ISO como para `xolite-ce` y `xoa-proxy`. Las filas existentes se completaron a partir de los artefactos publicados, y la versión original de xo-lite para `v8.3-ce3` / `v8.3-ce4` se corrigió de 0.22.0 a 0.21.0 para coincidir con el RPM que realmente incluyen. El orquestador registra el nuevo campo en cada compilación (`xcp-orchestrator`, `shared/src/github.rs`).

---

## Julio de 2026 {#july-2026}

### Las imágenes de VM XOA se publican en build-xoa-hl, resuelve [#22](https://github.com/Vagrantin/xcp-hl/issues/22) {#xoa-vm-image-releases-moved-to-build-xoa-hl-fixes-22}

La VM XOA-hl (`xoa-image-<date>-<sha7>`, artefacto `xoa-almalinux.xva`) se publicaba en [`xoa-hl`](https://github.com/Vagrantin/xoa-hl), el repositorio que construye el *software*, mezclada con sus publicaciones RPM. Ahora se publica en [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl), el repositorio que realmente construye la imagen. `xoa-vm-agent` del orquestador crea allí la publicación y el botón de despliegue de XO Lite resuelve la imagen más reciente desde ese repositorio.

La mezcla tenía una consecuencia concreta: `releases/latest` en `xoa-hl` apuntaba a una publicación de imagen sin artefacto RPM, rompiendo su búsqueda en `build-xoa-hl/scripts/setup-xoa-builder.sh`; ahora se busca la publicación más reciente que realmente incluye un RPM.

Las imágenes publicadas antes del traslado permanecen en `xoa-hl` para que las ISO ya distribuidas sigan resolviéndolas; la [matriz de versiones](/docs/reference/release-matrix#xoa-hl-releases) enlaza cada entrada al repositorio que la aloja.

### La matriz registra las versiones de XOA, resuelve [#13](https://github.com/Vagrantin/xcp-hl/issues/13) {#release-matrix-records-xoa-versions-fixes-13}

La [matriz de versiones](/docs/reference/release-matrix) tiene ahora una tabla dedicada de **publicaciones del appliance XOA** que registra cada imagen VM publicada (publicación `xoa-image-*` en `Vagrantin/xoa-hl`), la versión del software `xoa-hl` que contiene y la versión original de Xen Orchestra de la que deriva. La tabla por ISO también elimina una columna `xoa-hl` que nunca se rellenaba: el appliance se resuelve en el momento del despliegue y se versiona independientemente de la ISO.

### Edición XOA-hl completada, resuelve [#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6) {#xoa-hl-edition-complete-fixes-1-6}

Xen Orchestra HomeLab Edition ya se compila desde el código fuente, se empaqueta y se puede desplegar de principio a fin:

- [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) construye XO 5.113.2 (la última versión XO 5.x) desde un commit original fijo y modifica la interfaz: oculta las opciones de menú sujetas a licencia (Hub, XOA, Proxies, XOSTOR) y el aviso de ausencia de soporte (`patches/menu-hide-items.patch`).
- [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) lo empaqueta en un appliance XVA con autoconfiguración mediante Packer en XCP-ng.
- La vista de despliegue de XO Lite ofrece ahora **XOA HomeLab (latest build)** como opción de imagen y resuelve el XVA más reciente construido por el agente desde las publicaciones de GitHub en el momento del despliegue (commit `6abd43f` de `xolite-ce`, 2026-07-14).

### Publicación de versiones automatizada, resuelve [#4](https://github.com/Vagrantin/xcp-hl/issues/4) {#release-publication-automated-fixes-4}

Las versiones y notas de publicación se derivan ahora automáticamente en todos los procesos:

- `xolite-ce` y `xoa-proxy` derivan la etiqueta y versión RPM en CI (`xolite-ce` `7b2e4d4`, `xoa-proxy` `9582718`); `xoa-proxy` usa las notas generadas por GitHub, mientras que `xolite-ce` y la ISO incluyen cuerpos de publicación estructurados con versiones de origen y pasos de verificación.
- El orquestador despacha la compilación de la ISO con etiquetas de componentes exactas fijadas como entradas del flujo, eliminando las carreras que podían incluir RPM obsoletos (`xcp-ng-ce-iso` `68f211d`).
- Cada publicación de ISO se registra en la [matriz de versiones](/docs/reference/release-matrix).

---

## Junio de 2026 {#june-2026}

### CI/CD del sitio de documentación, resuelve [#5](https://github.com/Vagrantin/xcp-hl/issues/5) {#documentation-website-cicd-fixes-5}

El sitio web del proyecto (este sitio) se construye con Jekyll y se despliega automáticamente en GitHub Pages en cada push a `main` de [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) (`.github/workflows/pages.yml`), convirtiéndose en la fuente única del estado del proyecto, incluida la matriz de versiones generada a partir de datos.

### Publicación de v8.3-ce9 {#v83-ce9-released}

- xolite-ce `v0.21.0-ce6`: versión original de xo-lite fijada en `0.21.0`, la última conocida que funciona (`0.22.0` y `0.23.0` rompían la compilación), mediante `UPSTREAM_TAG`.
- xoa-proxy `v0.1.1.x`: versionado RPM más sencillo (sufijo release `.static`) y notas de publicación de GitHub automáticas y categorizadas.
- Nombres coherentes de artefactos: `xcp-ng-8.3-ceN.iso` + `.iso.sha256` + `.iso.sha256.asc`, publicados como versiones de GitHub de `xcp-ng-ce-iso`.

---

## Mayo de 2026 {#may-2026}

### Modelo de claves GPG implementado, resuelve [#3](https://github.com/Vagrantin/xcp-hl/issues/3) {#gpg-key-model-implemented-fixes-3}

La firma GPG se armoniza en todos los procesos mediante un modelo de **clave maestra sin conexión y dos subclaves de firma**: una firma los RPM (`xo-lite-ce`, `xoa-proxy`) y otra el archivo de suma de comprobación de la ISO. La clave pública se publica en [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) y cada publicación incluye los pasos de verificación. Consulta los detalles en [Firma GPG](/docs/components/#gpg-signing). Una mejora posterior (una clave por módulo) permanece en la [hoja de ruta](/docs/reference/roadmap#gpg-keys-one-signing-key-per-module).

### Primera publicación pública, v8.3-ce alpha2 {#first-public-release-v83-ce-alpha2}

- Primera publicación utilizable.
- Despliega XOA desde la imagen de Vates, la de Ronivay o una URL personalizada.
- **GPG**: clave maestra sin conexión y subclaves dedicadas para RPM e ISO. Clave pública publicada en keys.openpgp.org.

---

## Abril de 2026 {#april-2026}

### Primera compilación, v8.3-ce {#first-build-v83-ce}

- XO Lite modificado: endpoint de despliegue comunitario y campos de credenciales de solo lectura.
- Servidor Rust `xoa-proxy` incluido: HTTP/HTTPS y transmisión gzip.
- ISO ensamblada desde XCP-ng 8.3 original con un repositorio RPM comunitario añadido.
- Infraestructura de claves GPG (RSA de 4096 bits, clave única `RPM-GPG-KEY-xcp-ng-ce`).
- Proceso CI/CD de GitHub Actions: compilación RPM → compilación ISO → publicaciones de GitHub.
