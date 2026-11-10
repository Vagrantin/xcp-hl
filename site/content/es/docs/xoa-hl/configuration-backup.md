---
title: "Exportar la configuración de XO"
linkTitle: "Exportar la configuración"
description: "Exportar la configuración de XO, probar una importación de forma segura y respaldar los metadatos del pool."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: reviewed
sourceRevision: sha256:3ff424587ab518557d549adfd272c62a75b29be172d3ee76ea8989eb313c9fb4
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Antes del mantenimiento del dispositivo virtual, guarda la configuración de XO en un archivo y consérvalo separado de las copias de seguridad de las VM. Después prueba ese archivo en un dispositivo virtual desechable. Los metadatos del pool necesitan su propio trabajo de copia de seguridad, descrito más abajo. Trabaja en el **navegador**, con una sesión de administrador de XO en XOA-HL.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261027-ca44911`, el paquete `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Probado en dispositivos virtuales de laboratorio el 27 de octubre de 2026: exportación, importación y recuperación en un dispositivo virtual nuevo de la misma versión. Esta página no describe un procedimiento de recuperación o de vuelta a una versión anterior admitido. Recompilado el 27 de octubre de 2026 con la corrección de aprovisionamiento de `build-xoa-hl@fa0c987`. Consulta [cómo identificar el archivo corregido](/docs/xoa-hl/first-login/#identify-the-rebuilt-image). Los resultados de exportación/importación y de creación de VM registrados en [#315](https://github.com/Vagrantin/xcp-hl/pull/315) son anteriores a esta recompilación. Aquí no consta ninguna repetición de esas pruebas con el archivo recompilado.
{{< /callout >}}

## Qué incluye la exportación {#export-contents}

La exportación guarda la configuración de XO: usuarios y grupos, reglas de acceso, conexiones de servidores, remotos, trabajos, programaciones, tokens de autenticación y ajustes de complementos. Trata el archivo como un secreto: puede contener contraseñas de servidores, credenciales de remotos y tokens.

| Elemento | Cómo protegerlo |
| --- | --- |
| Configuración de XO | Esta exportación desde **Settings → Config** |
| Discos y datos de los invitados | Una [copia de seguridad y restauración de VM](/docs/xoa-hl/backup-restore/) independiente |
| Metadatos del host y del pool | Una [copia de seguridad de los metadatos del pool](#pool-metadata) independiente. No se incluyen en esta exportación |
| Sistema operativo del dispositivo virtual, paquetes RPM y registros de ejecución | No se incluyen en la exportación |
| Archivo TOML del servidor, archivos TLS, ajustes de actualización y zona horaria | No se incluyen en la exportación. Regístralos por separado |

Que la exportación termine no demuestra que el archivo pueda restaurar tu instalación. Conserva junto a él una nota con las versiones de la imagen y de la aplicación.

## 1. Descargar y guardar la exportación {#1-download-and-store-the-export}

1. En el **navegador**, inicia sesión como administrador de XO. Anota las [versiones instaladas](/docs/xoa-hl/maintenance/#record-versions).
2. Abre **Settings → Config** (`/#/settings/config`). En **Export**, selecciona **Download current config**.
3. Introduce una frase de contraseña exclusiva y confirma. Si la dejas vacía, la exportación no se cifra.
4. Guarda la frase de contraseña por separado para seguir disponiendo de ella si pierdes el dispositivo virtual.
5. Si el navegador bloquea la nueva ventana, permite la descarga. Comprueba que se guardó un archivo no vacío: `config.json.gz`, con `.enc` añadido cuando está cifrado. No le cambies el nombre para que parezca una copia de seguridad de VM.
6. Traslada el archivo a un almacenamiento protegido fuera del dispositivo virtual. Anota la fecha, el tamaño, las versiones y si está cifrado.
7. Conserva la exportación anterior hasta que la nueva supere una prueba de importación en un dispositivo virtual aislado.

**Comprobación:** puedes acceder al archivo y a su frase de contraseña sin el dispositivo virtual original. Nunca adjuntes el archivo a una incidencia pública ni pegues su contenido descifrado en un informe.

## 2. Probar una importación en un dispositivo virtual aislado {#import-test}

{{< callout type="warning" >}}
Una importación puede reconectar servidores guardados y habilitar programaciones guardadas. Puede modificar entradas existentes y sustituir usuarios en conflicto. No hay una operación de reversión de toda la importación: un error puede dejar cambios parciales. Nunca utilices un dispositivo virtual de producción para descubrir qué hace una exportación que no has probado.
{{< /callout >}}

**Antes de empezar**

- Utiliza un dispositivo virtual desechable con las mismas versiones de imagen y paquete que anotaste.
- Restringe su red antes de importar: el navegador de prueba puede acceder a él, pero él no puede acceder a hosts de producción, remotos de copia de seguridad ni servicios externos.
- Impón esta restricción fuera de XO. Deshabilitar conexiones o programaciones antes de importar no basta, porque la importación puede restaurarlas.
- Anota el estado del dispositivo virtual nuevo. Ten preparadas las credenciales de la configuración exportada: la importación puede cambiar las cuentas.

1. Abre **Settings → Config**. Selecciona o arrastra el archivo exportado, selecciona **Import** e introduce la frase de contraseña de la exportación. Espera al mensaje de éxito o de error.
2. Si la importación tiene éxito, cierra la sesión y vuelve a iniciarla con una cuenta de administrador de la exportación.
3. Compara los usuarios, permisos, remotos, servidores, trabajos y programaciones con tus registros del origen. Es normal que haya errores de conexión de servidores mientras la red esté bloqueada. La importación no elimina las cuentas que no están en el archivo: borra cualquier cuenta que no esperes, por ejemplo `admin@admin.net`.
4. Antes de permitir el acceso a cualquier recurso de prueba desechable, deshabilita las programaciones importadas y elimina o sustituye los destinos de producción. Vuelve a comprobar estos ajustes antes de cada prueba.
5. Si falla la importación, registra el error y los registros de `xo-server`, eliminando los secretos. Descarta el dispositivo virtual y empieza con uno nuevo para el siguiente intento. No supongas que una importación fallida no cambió nada.

Comprueba primero que el administrador restaurado puede iniciar sesión. En **Settings → Users**, elimina las cuentas inesperadas o asigna contraseñas nuevas y únicas a las cuentas que conserves deliberadamente. Nunca elimines tu único administrador operativo. Comprueba en una sesión privada del navegador que `admin@admin.net` con la contraseña `admin` se rechaza, y guarda el estado corregido con un reinicio limpio del dispositivo virtual antes de volver a conectar recursos de producción. La recompilación del 27 de octubre de 2026 corrige el aprovisionamiento. No cambia este comportamiento de la importación: los usuarios que no figuran en la exportación pueden permanecer en el destino.

**Comprobación:** el administrador exportado puede iniciar sesión y los usuarios, permisos, remotos, trabajos y programaciones coinciden con tus registros. Un mensaje de éxito por sí solo no demuestra que puedas recuperar el sistema. No se abordan aquí una frase de contraseña incorrecta, usuarios en conflicto ni una importación interrumpida.

## Configurar la protección de metadatos del pool {#pool-metadata}

Un trabajo independiente de **Pool metadata** copia los metadatos de un pool. XO lee un flujo XAPI `/pool/xmldbdump` del pool seleccionado. Escribe `data` y `metadata.json` en un remoto, bajo `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. No es la exportación de **Settings → Config**, una copia de seguridad de discos de VM, una imagen del dispositivo virtual ni un método probado para recuperar un host. Los metadatos pueden revelar detalles de tu infraestructura: restringe el acceso al remoto y nunca adjuntes estos archivos a una incidencia pública.

**Antes de empezar**

- Utiliza un pool desechable que sea tuyo y puedas reconstruir, conectado a XOA-HL. Nunca modifiques ni restaures un pool de producción para esta prueba.
- Utiliza un remoto NFS de copia de seguridad dedicado y con escritura que no dependa del almacenamiento de ese pool, de modo que un mismo fallo no afecte a ambos.
- Mantén un plan independiente de [copia de seguridad y restauración de VM](/docs/xoa-hl/backup-restore/) para los datos de los invitados.
- Comprueba la imagen y el paquete instalados. Comprueba que el administrador pueda ver los controles de copia de seguridad de metadatos: en esta versión, la interfaz puede ocultarlos por una comprobación del plan. Si no están disponibles, detente.
- Anota el UUID del pool, las identidades del maestro y de los hosts, el identificador del remoto y su espacio libre.

### Crear un trabajo deshabilitado {#create-a-disabled-job}

1. Abre **Backup → New** y elige **XO config & Pool metadata Backup** (`/#/backup/new/metadata`). Asigna al trabajo el nombre `lab-pool-metadata`.
2. Habilita solo **Pool metadata** y deja **XO config** desactivado.
3. Selecciona explícitamente el pool desechable. Selecciona únicamente el remoto dedicado. No añadas otros pools ni remotos.
4. Añade una programación con una zona horaria explícita. Establece **Pool retention** en `2` y deja la programación deshabilitada.
5. Guarda. Vuelve a leer los identificadores del trabajo y de la programación, el pool, el remoto, el modo, la retención y el estado deshabilitado. Si el editor no los conservó, detente.

### Ejecutar el trabajo tres veces {#run-the-job-three-times}

1. Ejecuta el trabajo manualmente desde su programación guardada. Anota la hora: esta es la ejecución A.
2. Espera a que termine. En el registro del trabajo, comprueba cada pool y remoto, incluidas las subtareas. Un éxito en el nivel superior no demuestra que la copia en el remoto esté completa.
3. Anota el identificador de ejecución, su estado y el UUID del pool de origen.
4. Repite para las ejecuciones B y C, a horas distintas. Inicia cada ejecución solo después de que termine la anterior.

### Comprobar los puntos conservados {#check-the-kept-points}

1. Abre **Backup → Restore → Metadata** (`/#/backup/restore/metadata`). Observa las entradas de **pool** de los remotos habilitados, sus horas y los puntos disponibles. **No selecciones Restore ni Delete.**
2. Con retención `2`, solo permanecen los puntos de las ejecuciones B y C. Compáralos con tus notas de A, B y C.
3. Si el administrador del almacenamiento puede abrir el remoto directamente, pídele que compruebe cada punto conservado: `data` y `metadata.json` no están vacíos y coinciden las identidades del trabajo, la programación y el pool. Registra los tamaños de archivo y sus hashes en un lugar protegido. No publiques el contenido.
4. Conserva cualquier punto incompleto o resultado de limpieza inesperado para investigarlo.

El trabajo escribe estos archivos sin suma de comprobación. Un punto enumerado o una tarea correcta no demuestra que XAPI pueda importarlo.

**Comprobación:** la programación sigue deshabilitada, las tres ejecuciones indican el pool y el remoto previstos, y los puntos B y C conservados y sus archivos coinciden con tus notas. Si fallan la exportación, la escritura en el remoto, la limpieza o el listado, deja de ejecutar el trabajo y conserva los registros y el inventario. Nunca elimines carpetas de copia de seguridad basándote únicamente en sus nombres.

### Antes de cualquier restauración de pool {#before-any-pool-restore}

Una restauración de pool envía el archivo `data` del punto elegido a `/pool/xmldbdump` en el pool de destino. Modifica el pool y no se ha demostrado una forma de deshacerlo. Antes de cualquier restauración, el propietario del pool debe proporcionar:

- un pool de destino aislado y desechable
- un plan de recuperación que corresponda a las versiones e identidades
- una copia independiente de respaldo de la imagen o de los metadatos
- acceso bloqueado a las redes y al almacenamiento de producción
- una forma de comprobar después la conectividad y el inventario de hosts y del pool

Solo después de revisar estos requisitos, elige un punto exacto y un pool de destino. Un punto disponible o una exportación correcta no demuestra que puedas recuperar el sistema. Mantén separadas las exportaciones de configuración de XO y las copias de los invitados. No se aborda aquí la restauración en sí, ni la restauración masiva ni sobre un pool diferente.

## Límites de recuperación y reversión {#recovery-limits}

Ante una pérdida real, conserva el dispositivo virtual averiado y las pruebas. Identifica las versiones exactas y utiliza un plan de recuperación que haya superado una prueba aislada para esas versiones. Nunca conectes dos copias con programaciones activas a los mismos destinos de producción.

Un paquete RPM anterior no constituye una reversión completa. Volver a una versión anterior no deshace las actualizaciones del sistema operativo, no restaura los datos de XO ni recupera los archivos independientes enumerados arriba. Las importaciones entre `v5.113.2_e281c536-ce43` y `v5.113.2_e281c536-ce47`, que usan la misma versión de Xen Orchestra, funcionaron en el laboratorio en ambos sentidos. No se han probado las importaciones entre versiones de Xen Orchestra ni la recuperación mediante una versión anterior. Si falla una actualización, consulta [mantenimiento](/docs/xoa-hl/maintenance/#update-problems) y [solución de problemas](/docs/xoa-hl/troubleshooting/).

### Límite de la recuperación admitida (OP04/OP05) {#supported-recovery-boundary}

Alcance: XO 5.113.2 `e281c536`, fuentes de XOA-HL ce40/ce47. **Este manual no admite para estas versiones una reversión o vuelta a una versión anterior completa del dispositivo virtual, ni un procedimiento de recuperación ante desastres con una imagen nueva.** Es un límite documentado de soporte y aceptación, no una afirmación de que instalar un RPM anterior o importar la configuración sea técnicamente imposible.

El exportador de configuración serializa los ajustes registrados de XO, no el sistema operativo del dispositivo virtual, la transacción RPM, los discos de los invitados, las claves TLS ni los archivos del operador. El actualizador de XOA-HL ejecuta un `dnf update` hacia delante; no ofrece ninguna reversión coordinada de datos y sistema operativo. Las observaciones anteriores sobre la importación de ajustes entre ce43 y ce47 no validan la recuperación del dispositivo virtual completo.

Antes de poder ofrecer una receta de recuperación, conserva una imagen conocida y la identidad RPM exacta, una exportación de configuración cifrada con su frase de contraseña, la configuración del operador con TLS y otros archivos locales protegidos por separado, y copias de seguridad independientes de las VM. Conserva desconectado el dispositivo virtual averiado. Un sustituto debe arrancar aislado de todos los hosts gestionados, destinos de copias y de la red de producción **antes** de importar los ajustes, porque la importación puede activar conexiones y programaciones. Después necesita un acceso local verificado, ajustes y archivos restaurados, programaciones deshabilitadas, una reconexión deliberada de hosts y remotos, una restauración aislada de un invitado y comprobaciones de trabajos duplicados. Los errores de importación pueden dejar un estado parcial; reconstruye el destino desechable en lugar de reintentar a ciegas.

Estos son requisitos previos para una prueba futura, no una secuencia verificada de recuperación con una imagen nueva. Hasta que se supere ese ejercicio concreto para la versión, obtén un plan de recuperación aprobado por los mantenedores. No ejecutes `dnf downgrade`, no sobrescribas Redis ni conectes un sustituto sin verificar junto al programador antiguo como atajo de recuperación.

Implementación fijada: [packages/xo-server/src/xo-mixins/config-management.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [packages/xo-server/src/xo-mixins/scheduling.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [packages/xo-server/src/xo-mixins/xen-servers.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).

[Actualizador hacia delante de XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/ca44911bcc0cd883421cf2e2daf405250080f6d7/SOURCES/xoa-hl-update.sh), [ciclo de vida del RPM](https://github.com/Vagrantin/xoa-hl/blob/ca44911bcc0cd883421cf2e2daf405250080f6d7/SPECS/xoa-hl.spec).

{{< details title="Fuentes" closed="true" >}}
- **Exportación de la configuración**: [pantalla de configuración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [API exclusiva para administradores y formato de archivo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [cifrado e importador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [reconexión de servidores](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [activación de programaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [conflictos de usuarios](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
- **Copia de seguridad de metadatos del pool**: [editor de trabajos de metadatos y comprobación del plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [API de administración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [exportación del pool y archivos del remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [modos y remotos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [limpieza por retención](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [lista de puntos de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js), [endpoint de importación XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
{{< /details >}}
