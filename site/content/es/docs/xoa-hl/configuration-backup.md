---
title: "Exportar la configuración de XO"
linkTitle: "Exportar la configuración"
description: "Exportar la configuración de XO, probar una importación de forma segura y respaldar los metadatos del pool."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: reviewed
sourceRevision: sha256:05633ef4f66758e8e6f2c91bc4724045aa4c54b899ca74810a99c0248758a312
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Antes del mantenimiento del dispositivo virtual, guarde la configuración de XO en un archivo y consérvelo separado de las copias de seguridad de las VM. Después pruebe ese archivo en un dispositivo virtual desechable. Los metadatos del pool necesitan su propio trabajo de copia de seguridad, descrito más abajo. Trabaje en el **navegador**, con una sesión de administrador de XO en XOA-HL.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261027-ca44911`, el paquete `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Probado en dispositivos virtuales de laboratorio el 27 de octubre de 2026: exportación, importación y recuperación en un dispositivo virtual nuevo de la misma versión. Esta página no describe un procedimiento de recuperación o de vuelta a una versión anterior admitido. Recompilado el 27 de octubre de 2026 con la corrección de aprovisionamiento de `build-xoa-hl@fa0c987`. Consulte [cómo identificar el archivo corregido](/docs/xoa-hl/first-login/#identify-the-rebuilt-image). Los resultados de exportación/importación y de creación de VM registrados en [#315](https://github.com/Vagrantin/xcp-hl/pull/315) son anteriores a esta recompilación. Aquí no consta ninguna repetición de esas pruebas con el archivo recompilado.
{{< /callout >}}

## Qué incluye la exportación {#export-contents}

La exportación guarda la configuración de XO: usuarios y grupos, reglas de acceso, conexiones de servidores, remotos, trabajos, programaciones, tokens de autenticación y ajustes de complementos. Trate el archivo como un secreto: puede contener contraseñas de servidores, credenciales de remotos y tokens.

| Elemento | Cómo protegerlo |
| --- | --- |
| Configuración de XO | Esta exportación desde **Settings → Config** |
| Discos y datos de los invitados | Una [copia de seguridad y restauración de VM](/docs/xoa-hl/backup-restore/) independiente |
| Metadatos del host y del pool | Una [copia de seguridad de los metadatos del pool](#pool-metadata) independiente. No se incluyen en esta exportación |
| Sistema operativo del dispositivo virtual, paquetes RPM y registros de ejecución | No se incluyen en la exportación |
| Archivo TOML del servidor, archivos TLS, ajustes de actualización y zona horaria | No se incluyen en la exportación. Regístrelos por separado |

Que la exportación termine no demuestra que el archivo pueda restaurar su instalación. Conserve junto a él una nota con las versiones de la imagen y de la aplicación.

## 1. Descargar y guardar la exportación {#1-download-and-store-the-export}

1. En el **navegador**, inicie sesión como administrador de XO. Anote las [versiones instaladas](/docs/xoa-hl/maintenance/#record-versions).
2. Abra **Settings → Config** (`/#/settings/config`). En **Export**, seleccione **Download current config**.
3. Introduzca una frase de contraseña exclusiva y confirme. Si la deja vacía, la exportación no se cifra.
4. Guarde la frase de contraseña por separado para seguir disponiendo de ella si pierde el dispositivo virtual.
5. Si el navegador bloquea la nueva ventana, permite la descarga. Compruebe que se guardó un archivo no vacío: `config.json.gz`, con `.enc` añadido cuando está cifrado. No le cambie el nombre para que parezca una copia de seguridad de VM.
6. Traslade el archivo a un almacenamiento protegido fuera del dispositivo virtual. Anote la fecha, el tamaño, las versiones y si está cifrado.
7. Conserve la exportación anterior hasta que la nueva supere una prueba de importación en un dispositivo virtual aislado.

**Comprobación:** puede acceder al archivo y a su frase de contraseña sin el dispositivo virtual original. Nunca adjunte el archivo a una incidencia pública ni pegue su contenido descifrado en un informe.

## 2. Probar una importación en un dispositivo virtual aislado {#import-test}

{{< callout type="warning" >}}
Una importación puede reconectar servidores guardados y habilitar programaciones guardadas. Puede modificar entradas existentes y sustituir usuarios en conflicto. No hay una operación de reversión de toda la importación: un error puede dejar cambios parciales. Nunca utilice un dispositivo virtual de producción para descubrir qué hace una exportación que no ha probado.
{{< /callout >}}

**Antes de empezar**

- Utilice un dispositivo virtual desechable con las mismas versiones de imagen y paquete que anotó.
- Restrinja su red antes de importar: el navegador de prueba puede acceder a él, pero él no puede acceder a hosts de producción, remotos de copia de seguridad ni servicios externos.
- Imponga esta restricción fuera de XO. Deshabilitar conexiones o programaciones antes de importar no basta, porque la importación puede restaurarlas.
- Anote el estado del dispositivo virtual nuevo. Tenga preparadas las credenciales de la configuración exportada: la importación puede cambiar las cuentas.

1. Abra **Settings → Config**. Seleccione o arrastre el archivo exportado, seleccione **Import** e introduzca la frase de contraseña de la exportación. Espere al mensaje de éxito o de error.
2. Si la importación tiene éxito, cierre la sesión y vuelva a iniciarla con una cuenta de administrador de la exportación.
3. Compare los usuarios, permisos, remotos, servidores, trabajos y programaciones con sus registros del origen. Es normal que haya errores de conexión de servidores mientras la red esté bloqueada. La importación no elimina las cuentas que no están en el archivo: borre cualquier cuenta que no espere, por ejemplo `admin@admin.net`.
4. Antes de permitir el acceso a cualquier recurso de prueba desechable, deshabilite las programaciones importadas y elimine o sustituya los destinos de producción. Vuelva a comprobar estos ajustes antes de cada prueba.
5. Si falla la importación, registre el error y los registros de `xo-server`, eliminando los secretos. Descarte el dispositivo virtual y empiece con uno nuevo para el siguiente intento. No suponga que una importación fallida no cambió nada.

Compruebe primero que el administrador restaurado puede iniciar sesión. En **Settings → Users**, elimine las cuentas inesperadas o asigne contraseñas nuevas y únicas a las cuentas que conserve deliberadamente. Nunca elimine su único administrador operativo. Compruebe en una sesión privada del navegador que `admin@admin.net` con la contraseña `admin` se rechaza, y guarde el estado corregido con un reinicio limpio del dispositivo virtual antes de volver a conectar recursos de producción. La recompilación del 27 de octubre de 2026 corrige el aprovisionamiento. No cambia este comportamiento de la importación: los usuarios que no figuran en la exportación pueden permanecer en el destino.

**Comprobación:** el administrador exportado puede iniciar sesión y los usuarios, permisos, remotos, trabajos y programaciones coinciden con sus registros. Un mensaje de éxito por sí solo no demuestra que pueda recuperar el sistema. No se abordan aquí una frase de contraseña incorrecta, usuarios en conflicto ni una importación interrumpida.

## Configurar la protección de metadatos del pool {#pool-metadata}

Un trabajo independiente de **Pool metadata** copia los metadatos de un pool. XO lee un flujo XAPI `/pool/xmldbdump` del pool seleccionado. Escriba `data` y `metadata.json` en un remoto, bajo `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. No es la exportación de **Settings → Config**, una copia de seguridad de discos de VM, una imagen del dispositivo virtual ni un método probado para recuperar un host. Los metadatos pueden revelar detalles de su infraestructura: restrinja el acceso al remoto y nunca adjunte estos archivos a una incidencia pública.

**Antes de empezar**

- Utilice un pool desechable que sea suyo y pueda reconstruir, conectado a XOA-HL. Nunca modifique ni restaure un pool de producción para esta prueba.
- Utilice un remoto NFS de copia de seguridad dedicado y con escritura que no dependa del almacenamiento de ese pool, de modo que un mismo fallo no afecte a ambos.
- Mantenga un plan independiente de [copia de seguridad y restauración de VM](/docs/xoa-hl/backup-restore/) para los datos de los invitados.
- Compruebe la imagen y el paquete instalados. Compruebe que el administrador pueda ver los controles de copia de seguridad de metadatos: en esta versión, la interfaz puede ocultarlos por una comprobación del plan. Si no están disponibles, deténgase.
- Anote el UUID del pool, las identidades del maestro y de los hosts, el identificador del remoto y su espacio libre.

### Crear un trabajo deshabilitado {#create-a-disabled-job}

1. Abra **Backup → New** y elija **XO config & Pool metadata Backup** (`/#/backup/new/metadata`). Asigne al trabajo el nombre `lab-pool-metadata`.
2. Habilite solo **Pool metadata** y deje **XO config** desactivado.
3. Seleccione explícitamente el pool desechable. Seleccione únicamente el remoto dedicado. No añada otros pools ni remotos.
4. Añada una programación con una zona horaria explícita. Establezca **Pool retention** en `2` y deje la programación deshabilitada.
5. Guarde. Vuelva a leer los identificadores del trabajo y de la programación, el pool, el remoto, el modo, la retención y el estado deshabilitado. Si el editor no los conservó, deténgase.

### Ejecutar el trabajo tres veces {#run-the-job-three-times}

1. Ejecute el trabajo manualmente desde su programación guardada. Anote la hora: esta es la ejecución A.
2. Espere a que termine. En el registro del trabajo, compruebe cada pool y remoto, incluidas las subtareas. Un éxito en el nivel superior no demuestra que la copia en el remoto esté completa.
3. Anote el identificador de ejecución, su estado y el UUID del pool de origen.
4. Repita para las ejecuciones B y C, a horas distintas. Inicie cada ejecución solo después de que termine la anterior.

### Comprobar los puntos conservados {#check-the-kept-points}

1. Abra **Backup → Restore → Metadata** (`/#/backup/restore/metadata`). Observe las entradas de **pool** de los remotos habilitados, sus horas y los puntos disponibles. **No seleccione Restore ni Delete.**
2. Con retención `2`, solo permanecen los puntos de las ejecuciones B y C. Compárelos con sus notas de A, B y C.
3. Si el administrador del almacenamiento puede abrir el remoto directamente, pídale que compruebe cada punto conservado: `data` y `metadata.json` no están vacíos y coinciden las identidades del trabajo, la programación y el pool. Registre los tamaños de archivo y sus hashes en un lugar protegido. No publique el contenido.
4. Conserve cualquier punto incompleto o resultado de limpieza inesperado para investigarlo.

El trabajo escribe estos archivos sin suma de comprobación. Un punto enumerado o una tarea correcta no demuestra que XAPI pueda importarlo.

**Comprobación:** la programación sigue deshabilitada, las tres ejecuciones indican el pool y el remoto previstos, y los puntos B y C conservados y sus archivos coinciden con sus notas. Si fallan la exportación, la escritura en el remoto, la limpieza o el listado, deje de ejecutar el trabajo y conserve los registros y el inventario. Nunca elimine carpetas de copia de seguridad basándote únicamente en sus nombres.

### Antes de cualquier restauración de pool {#before-any-pool-restore}

Una restauración de pool envía el archivo `data` del punto elegido a `/pool/xmldbdump` en el pool de destino. Modifique el pool y no se ha demostrado una forma de deshacerlo. Antes de cualquier restauración, el propietario del pool debe proporcionar:

- un pool de destino aislado y desechable
- un plan de recuperación que corresponda a las versiones e identidades
- una copia independiente de respaldo de la imagen o de los metadatos
- acceso bloqueado a las redes y al almacenamiento de producción
- una forma de comprobar después la conectividad y el inventario de hosts y del pool

Solo después de revisar estos requisitos, elija un punto exacto y un pool de destino. Un punto disponible o una exportación correcta no demuestra que pueda recuperar el sistema. Mantenga separadas las exportaciones de configuración de XO y las copias de los invitados. No se aborda aquí la restauración en sí, ni la restauración masiva ni sobre un pool diferente.

## Límites de recuperación y reversión {#recovery-limits}

Ante una pérdida real, conserve el dispositivo virtual averiado y las pruebas. Identifique las versiones exactas y utilice un plan de recuperación que haya superado una prueba aislada para esas versiones. Nunca conecte dos copias con programaciones activas a los mismos destinos de producción.

Un paquete RPM anterior no constituye una reversión completa. Volver a una versión anterior no deshace las actualizaciones del sistema operativo, no restaura los datos de XO ni recupera los archivos independientes enumerados arriba. Las importaciones entre `v5.113.2_e281c536-ce43` y `v5.113.2_e281c536-ce47`, que usan la misma versión de Xen Orchestra, funcionaron en el laboratorio en ambos sentidos. No se han probado las importaciones entre versiones de Xen Orchestra ni la recuperación mediante una versión anterior. Si falla una actualización, consulte [mantenimiento](/docs/xoa-hl/maintenance/#update-problems) y [solución de problemas](/docs/xoa-hl/troubleshooting/).

### Límite de la recuperación admitida (OP04/OP05) {#supported-recovery-boundary}

Se aplica a: Xen Orchestra 5.113.2 (`e281c536`) en XOA-HL ce40 y ce47. **Este manual no admite para estas versiones una reversión o vuelta a una versión anterior completa del dispositivo virtual, ni un procedimiento de recuperación ante desastres con una imagen nueva.** Es un límite de soporte documentado, no una afirmación de que instalar un RPM anterior o importar la configuración sea técnicamente imposible.

El exportador de configuración serializa los ajustes registrados de XO, no el sistema operativo del dispositivo virtual, la transacción RPM, los discos de los invitados, las claves TLS ni los archivos del operador. El actualizador de XOA-HL ejecuta un `dnf update` hacia delante; no ofrece ninguna reversión coordinada de datos y sistema operativo. Las observaciones anteriores sobre la importación de ajustes entre ce43 y ce47 no validan la recuperación del dispositivo virtual completo.

Antes de poder ofrecer una receta de recuperación, conserve una imagen conocida y la identidad RPM exacta, una exportación de configuración cifrada con su frase de contraseña, la configuración del operador con TLS y otros archivos locales protegidos por separado, y copias de seguridad independientes de las VM. Conserve desconectado el dispositivo virtual averiado. Un sustituto debe arrancar aislado de todos los hosts gestionados, destinos de copias y de la red de producción **antes** de importar los ajustes, porque la importación puede activar conexiones y programaciones. Después necesita un acceso local verificado, ajustes y archivos restaurados, programaciones deshabilitadas, una reconexión deliberada de hosts y remotos, una restauración aislada de un invitado y comprobaciones de trabajos duplicados. Los errores de importación pueden dejar un estado parcial; reconstruya el destino desechable en lugar de reintentar a ciegas.

Estos son requisitos previos para una prueba futura, no una secuencia verificada de recuperación con una imagen nueva. Hasta que se supere ese ejercicio concreto para la versión, obtenga un plan de recuperación aprobado por los mantenedores. No ejecute `dnf downgrade`, no sobrescriba Redis ni conecte un sustituto sin verificar junto al programador antiguo como atajo de recuperación.

Implementación fijada: [packages/xo-server/src/xo-mixins/config-management.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [packages/xo-server/src/xo-mixins/scheduling.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [packages/xo-server/src/xo-mixins/xen-servers.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).

[Actualizador hacia delante de XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/ca44911bcc0cd883421cf2e2daf405250080f6d7/SOURCES/xoa-hl-update.sh), [ciclo de vida del RPM](https://github.com/Vagrantin/xoa-hl/blob/ca44911bcc0cd883421cf2e2daf405250080f6d7/SPECS/xoa-hl.spec).

{{< details title="Fuentes" closed="true" >}}
- **Exportación de la configuración**: [pantalla de configuración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [API exclusiva para administradores y formato de archivo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [cifrado e importador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [reconexión de servidores](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [activación de programaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [conflictos de usuarios](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
- **Copia de seguridad de metadatos del pool**: [editor de trabajos de metadatos y comprobación del plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [API de administración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [exportación del pool y archivos del remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [modos y remotos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [limpieza por retención](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [lista de puntos de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js), [endpoint de importación XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
{{< /details >}}
