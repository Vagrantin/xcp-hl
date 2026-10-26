---
title: "Resolver fallos de copia de seguridad y otros problemas"
linkTitle: "Resolución de problemas"
description: "Encuentre la causa de problemas de red, copias, actualizaciones y acceso, y comunique una incidencia."
weight: 82
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:fa3eed7a7f974bcc1bebcd34d1969b194a60f8eb7ed99d793d0961ff5759c2cd
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Empiece por el síntoma y la última operación anterior, y siga la comprobación correspondiente. La mayoría solo leen información: acceda al **appliance XOA-HL** en el navegador como administrador. Algunas necesitan la consola del appliance o de un invitado. Antes de repetir una actualización, importación o copia fallida, guarde el error y los registros.

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio.
{{< /callout >}}

## Empiece por el síntoma {#symptoms}

| Problema | Qué comprobar |
| --- | --- |
| La página del appliance no se abre | En XO Lite, compruebe VM en ejecución y dirección/red correctas. Después compruebe `xo-server` y espacio mediante las [comprobaciones de consola](#appliance-checks). **Comprobación:** la URL correcta abre la página de acceso. |
| Falla el primer acceso | Siga la [guía del primer acceso](/docs/xoa-hl/first-login/) para credenciales web y alternativa del primer arranque. Con acceso autorizado por consola, lea el registro de aprovisionamiento. **Comprobación:** puede acceder y la contraseña inicial está cambiada. |
| Un host está habilitado pero no aparece nada | En **Settings → Servers**, lea el error. Compruebe dirección, credenciales, identidad del certificado y acceso desde el appliance al host. **Comprobación:** aparecen host y almacenamiento sin error de conexión. |
| Falla crear o instalar una VM | Anote el error de tarea antes de repetir. Contraste pool, plantilla, espacio libre SR, red y medios con [Crear su primera VM](/docs/xoa-hl/create-vm/). **Comprobación:** la VM de prueba arranca el instalador elegido. |
| Falla una copia o restauración | Lea su registro. Compruebe remoto, credenciales, espacio y SR destino y siga [Diagnosticar una copia NFS fallida](#backup-failures). Quite todas las NIC de una copia restaurada antes de arrancar, como en [Copiar y restaurar una VM](/docs/xoa-hl/backup-restore/). **Comprobación:** la tarea tiene éxito y una copia restaurada aislada contiene los datos esperados. |
| Se desconecta la página de actualización | Instalar el paquete reinicia `xo-server`. Lea registro y estado del servicio. No inicie otra actualización. **Comprobación:** el registro termina con éxito, la versión es la esperada, puede acceder y aparecen los hosts. |
| La comprobación de actualización muestra ERROR | Lea `/run/xoa-hl/status` y el diario del servicio de comprobación. Busque errores de repositorio/red o una actualización ya activa antes de repetir. **Comprobación:** una comprobación nueva devuelve `UP_TO_DATE` o `AVAILABLE`. |
| No se ejecutó una actualización automática | Compruebe modo guardado, zona horaria del appliance y temporizadores. Una ventana perdida mientras estaba apagado no se ejecuta al arrancar. **Comprobación:** el temporizador correcto está programado y las horas posteriores coinciden con la ventana. |
| Falla importar una configuración | Guarde error y registro del servidor: pueden quedar cambios. Siga la [prueba de importación aislada](/docs/xoa-hl/configuration-backup/). **Comprobación:** la prueba pasa en un appliance nuevo desechable. No suponga intacto el destino fallido. |
| Ningún administrador puede acceder | Contraseña o dispositivo OTP perdidos, o acceso LDAP/SAML averiado. Siga [Recuperar el acceso administrador](#recover-admin-access) desde la consola. **Comprobación:** la cuenta accede con contraseña nueva y figura como **Admin**. |

Para problemas de consola, controles o pantalla vacía/congelada, consulte [Usar la consola de VM](/docs/xoa-hl/vm-operations/#vm-console).

## Diagnostique la conectividad de red {#network-connectivity}

Use estas comprobaciones de solo lectura para una red normal de invitados existente o la [VLAN de laboratorio](/docs/xoa-hl/storage-networks/#host-vlan-network). Acceda como administrador XOA-HL para ver todas las VM, pools y hosts.

**Antes de empezar**

- Las comprobaciones de invitado necesitan sesión autorizada en su consola. Los responsables comprueban conmutadores, DNS y cortafuegos.
- Mantenga disponible acceso de consola independiente al host.
- No provoque fallos ni cambie la red de administración para probar esta guía.
- No se cubren bonds, SDN, troncales VLAN dentro del invitado ni recuperación de red de emergencia.

### 1. Encuentre la vía que falla {#1-find-the-failing-path}

Anote hora y zona horaria, última operación que funcionó y error exacto. Anote también máquina origen, nombre/dirección destino, protocolo y puerto del servicio. Guarde este estado antes de repetir. Una prueba desde su portátil no demuestra acceso desde appliance, host o invitado.

| Vía | Dónde mirar |
| --- | --- |
| Navegador → appliance | En su equipo, compruebe URL, resolución de nombres e identidad del certificado. Si no abre, use acceso autorizado por consola y las [comprobaciones de consola](#appliance-checks). |
| Appliance → host | Lea el error en **Settings → Servers** (`/#/settings/servers`) y siga [Hosts y pools](/docs/xoa-hl/hosts-pools/). Habilitado es un ajuste, no prueba de conexión funcional. |
| Host → SR NFS | Compruebe SR exacto y conexión/ruta de ese host según [Crear almacenamiento NFS para discos VM](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Una prueba desde invitado o appliance no sustituye el acceso del host. |
| Appliance → remoto de copias | Siga [Diagnosticar una copia NFS fallida](#backup-failures). SR NFS y remoto de copias usan clientes e identidades distintos. |
| Invitado → par o servicio | Siga los pasos 2 a 4. Acceder a XO o ver consola no demuestra acceso de red del invitado. |

### 2. Siga la interfaz del invitado hasta el enlace del host {#2-trace-the-guest-interface-to-the-host-uplink}

Solo lea estas pantallas. No pulse campos editables de red/MAC ni botones de conexión.

1. Anote UUID de VM, estado, host de ejecución y pool. Abra **Network** de la VM (`/#/vms/<id>/network`).
2. Copie UUID de interfaz (VIF) con su botón. Anote número de dispositivo, MAC, red, MTU y estado.
3. Abra redes del pool (`/#/pools/<id>/network`) y coincida UUID exacto de red, no solo nombre.
4. Lea **Connected**: indica si la VIF está conectada. Una VIF separada de una VM detenida no es un fallo.
5. Lea **IP addresses**: procede de métricas del invitado por dispositivo VIF. Una dirección ausente no demuestra invitado sin configurar y una presente no es prueba de accesibilidad en vivo. Compare con consola y [comprobaciones del agente](/docs/xoa-hl/guest-tools/).
6. Anote indicador de bloqueo y **Allowed IPs** por separado de las direcciones comunicadas. Son reglas de tráfico, no un formulario para asignar IP al invitado. Guarde avisos y pida al responsable explicar las reglas. No desbloquee, borre restricciones, cambie MAC/MTU ni desactive seguridad como atajo.
7. En la fila de red del pool, expanda **PIFs** y encuentre el host de ejecución. El resumen VLAN procede solo del maestro.
8. Abra **Network** de ese host (`/#/hosts/<id>/network`). Anote UUID PIF, dispositivo, MAC, red, VLAN, MTU, marca de administración y modo IP. Compare con cableado y registros autorizados. Una red puede ser interna a propósito, sin enlace físico: compruebe el diseño antes de llamarlo fallo.
9. Lea conexión y enlace físico (portadora) por separado. **Connected** del host indica si la PIF está conectada. El icono físico y estado PIF de la fila expandida muestran portadora.

La falta de métricas PIF también puede mostrar ausencia de portadora: un estado negativo no prueba cable desenchufado. Actualice y compare con host y conmutador. No alterne PIF, edite VLAN/MTU/IP, borre redes ni reinicie la red para sondear la vía.

### 3. Compruebe ajustes del invitado y servicio {#3-check-guest-settings-and-the-service}

1. En la **consola del invitado**, encuentre la interfaz por MAC. Su nombre puede diferir del dispositivo del host.
2. Con herramientas del SO, lea dirección/prefijo, rutas y DNS. Compare con dirección única y subred aprobadas. En la VLAN de laboratorio suele ver una interfaz sin etiquetar.
3. Pida a administradores de invitado/red probar par y servicio acordados desde este invitado exacto. Anote por separado respuestas DNS, familia de direcciones, destino, protocolo, puerto y resultado.
4. Si por nombre y por dirección hay resultados distintos, compruebe DNS e identidad de aplicación/TLS antes de concluir. HTTPS a una IP directa puede cambiar certificado o host virtual. Nunca omita verificaciones de certificado para declarar éxito.

Un ping exitoso no demuestra servicio funcional y uno fallido no demuestra aislamiento. Pruebe solo destinos autorizados. Cuando se exija aislamiento, pruebe también los prohibidos definidos por el responsable.

Un par en el mismo host no prueba enlace físico. Las pruebas entre hosts o externas necesitan pares identificados y vía de conmutación aprobada. No migre una carga para improvisar. Si detecta acceso inesperado a producción, guarde pruebas y apague normalmente el invitado de prueba. Si afecta administración/almacenamiento, use consola independiente y plan del responsable antes de otro cambio.

### 4. Compruebe la corrección {#4-check-the-fix}

1. Entregue al responsable asignación exacta, horas, error y comparaciones.
2. Aplique la corrección acordada mediante el procedimiento adecuado de invitado, almacenamiento, host o red. Esta guía no prescribe un restablecimiento general.
3. Actualice inventario. Repita **la misma prueba de servicio desde el mismo origen al mismo destino**.
4. Repita aislamiento requerido y compruebe administración y almacenamiento.
5. Anote cambios y resultado.

**Comprobación:** la misma prueba ahora pasa. Un indicador verde no significa por sí solo problema resuelto. Si la vía sigue incierta, mantenga el incidente abierto y [comunique un problema](#report-a-problem) con datos saneados.

## Diagnostique una copia NFS fallida {#backup-failures}

Úselo solo para la [tarea de copia completa a NFS del tutorial](/docs/xoa-hl/backup-restore/) como administrador XOA-HL. Trabaje en el **navegador**. El responsable del almacenamiento realiza sus comprobaciones. No necesita provocar fallos.

**Antes de empezar**

- Anote ID de tarea/programación, UUID origen, ID remoto, hora prevista y zona y resultado de última restauración aislada.
- No se cubren cadenas incrementales, réplica ni recuperación de producción. Para otras pruebas, consulte [copias incrementales y recuperación de cadenas](/docs/xoa-hl/backup-restore/#delta-backups), [un archivo de una copia delta](/docs/xoa-hl/backup-restore/#file-restore), [réplica DR en otro pool](/docs/xoa-hl/backup-restore/#dr-replica) y [remoto SMB en Windows Server](/docs/xoa-hl/backup-restore/#smb-remote).

### 1. Encuentre la ejecución y guarde sus detalles {#1-find-the-run-and-save-its-details}

1. Abra **Backup → Overview** (`/#/backup/overview`) y encuentre la tarea. Mire la tabla **Logs** inferior.
2. Borre filtros de búsqueda y estado si es necesario. Encuentre ejecución por tarea e inicio. La tabla abrevia ID: use los completos de detalles, no solo nombre.
3. Pulse el estado para abrir detalles. Anote `id`, `jobId`, `scheduleId`, horas de inicio/fin y estado.
4. Antes de cambiar, guarde JSON privadamente con portapapeles o **Download log**. No está saneado: prepare un extracto redactado para informes.
5. Borre búsqueda en detalles y seleccione todos los estados de tareas. Al principio puede mostrar solo pendientes, fallidas o interrumpidas, cinco por página. Revise todas.
6. Encuentre UUID VM y tareas de instantánea, remoto, exportación y transferencia. Guarde errores, motivos de omisión y avisos de cada nivel. No se muestran todas las tareas brutas: si el árbol parece incompleto, lea el JSON.

**Comprobación:** sus notas identifican una ejecución exacta y VM/remoto afectados. Registros o tareas ausentes no demuestran que no se ejecutó nada.

### 2. Lea el estado antes de repetir {#2-read-the-status-before-you-retry}

| Estado (valor JSON) | Significado y comprobaciones |
| --- | --- |
| Started (`pending`) | La ejecución figura activa. Actualice y siga el progreso. No tener hora final no significa éxito. No inicie otra ejecución. |
| Successful (`success`) | Ejecución y tareas registradas terminaron. Lea avisos y compruebe nuevo punto de restauración. Pruebe recuperación del invitado y datos por separado. |
| Skipped (`skipped`) | Se omitió trabajo. Lea motivo: errores como `no disks found`, `no VMs match this pattern` y `unhealthy VDI chain` cuentan como omitidos. No es una copia nueva comprobada. |
| Failed (`failure`) | Falló la ejecución o una tarea hija. Otro trabajo puede haber tenido éxito: compruebe fase fallida y copias reales existentes. |
| Interrupted (`interrupted`) | Hay inicio sin fin correspondiente y el servidor ya no la registra activa. Guarde cronología del servidor y objetos parciales. No demuestra reversión ni seguridad para repetir. |
{.xoa-backup-diagnosis}

### 3. Separe la fase fallida de los datos supervivientes {#3-separate-the-failed-stage-from-surviving-data}

Abra **Backup → Restore** (`/#/backup/restore`) para ver puntos y registros de restauración.

| Problema | Qué comprobar |
| --- | --- |
| No hay ejecución coincidente | Compruebe filtros, ID tarea/programación, estado habilitado, zona, disponibilidad y [programación guardada](/docs/xoa-hl/backup-restore/#backup-schedules). No suponga recuperación de ejecuciones perdidas ni correo enviado. |
| Error VM/instantánea o VM omitida | Compruebe UUID elegido, discos, conexión host y espacio SR origen. Guarde motivo exacto. No borre instantáneas ni cambie cadenas VDI como arreglo general. |
| Error remoto/exportación/transferencia | Con el responsable, compruebe acceso del appliance a NFS, permisos/opciones y espacio remoto. Una prueba remota exitosa no demuestra exportación completa ni restauración. |
| Funcionó transferencia y falló después | Con **Delete first** desactivado, la copia completa escribe exportación/metadatos antes de eliminar puntos antiguos. Un punto nuevo puede sobrevivir a fallo posterior de limpieza. Compruebe horas y puntos conservados antes de repetir o borrar. |
| Falta el punto en Restore | Abra **Backup → Restore** y actualice. Compruebe remoto correcto habilitado y errores de carga. Un remoto ilegible puede faltar: lista vacía no demuestra copias borradas. |
| Falló restaurar | Lea registros de esa página. Compruebe remoto legible y SR/host destino accesibles. Enumere VM o discos parciales por UUID. Conserve origen y copia; nunca borre solo por nombre. |
{.xoa-backup-diagnosis}

**Comprobación:** distingue fase fallida, puntos supervivientes y objetos de estado desconocido. Un archivo o punto listado no demuestra recuperación de datos.

### 4. Corrija la causa y compruebe el resultado {#4-fix-the-cause-and-check-the-result}

1. Para detener futuras ejecuciones, desactive la programación exacta del laboratorio en **Overview** y actualice para comprobarlo. No cancela una copia activa: el botón de cancelación está deshabilitado en esta versión. Reiniciar `xo-server` no cancela ni limpia una copia.
2. Corrija con su responsable el problema de acceso, espacio o selección. Revise después tarea, programación, VM y remoto.
3. Mantenga **Delete first** desactivado y las copias necesarias fuera de la retención de esta tarea. Si duda de actividad restante o propiedad de objetos parciales, guarde pruebas y pida ayuda antes de repetir.
4. Sin ejecución activa y comprendiendo el estado, ejecute manualmente esta tarea de una VM como en el tutorial. Los botones de reinicio y forzado del diálogo **ejecutan copias**: no reinician invitados ni son comprobaciones de lectura. No fuerce. Repetir también puede aplicar retención a puntos antiguos.
5. Compruebe nueva ejecución y puntos. Después [restaure una copia detenida, quite todas las NIC y compruebe datos de ejemplo](/docs/xoa-hl/backup-restore/).
6. Deje la programación desactivada. Antes de reactivarla, anote error original, arreglo, ID nuevos de ejecución/punto y resultado de restauración.

**Comprobación:** pasan nueva ejecución, puntos conservados y restauración aislada de datos. Si no, mantenga abierto el incidente y [comunique un problema](#report-a-problem) con pruebas saneadas.

## Compruebe el appliance desde su consola {#appliance-checks}

Estos comandos solo leen estado. Ejecútelos dentro del appliance, no en el hipervisor, desde consola o SSH autorizados. Algunos requieren root.

```bash
rpm -q xoa-hl nodejs
timedatectl
df -h
systemctl status xo-server redis xoa-hl-update.service --no-pager
systemctl list-timers 'xoa-hl-*'
journalctl -u xo-server -u xoa-hl-check-update.service -u xoa-hl-update.service -u xoa-hl-auto-update.service --since '1 hour ago' --no-pager
tail -n 100 /var/log/xoa-first-boot.log
tail -n 100 /var/lib/xoa-hl/update.log
cat /run/xoa-hl/status
cat /var/lib/xoa-hl/auto-update.status
```

- Que falte un archivo de estado antes de la primera comprobación o tras reiniciar no es por sí solo un fallo.
- `systemctl status` devuelve código distinto de cero para unidades inactivas o fallidas. Lea el estado mostrado.
- El estado automático puede describir una ejecución antigua. Compare sus horas UTC.
- Para significado de estados y decisiones de actualización/reinicio, consulte [Mantener y actualizar el appliance](/docs/xoa-hl/maintenance/).

No borre bases de datos, registros ni bloqueos para hacer desaparecer errores. Si el disco está lleno, identifique archivos crecientes y guarde pruebas antes de elegir qué limpiar.

## Recupere el acceso de administrador {#recover-admin-access}

Úselo si ningún administrador accede: contraseña perdida, dispositivo OTP perdido o LDAP/SAML averiado. Ejecute recuperación **dentro del appliance**, como root, desde consola o SSH. Cualquiera con root puede tomar una cuenta XO así: proteja ese acceso.

El comando cambia la cuenta indicada:

- Establece contraseña nueva.
- Quita su código de un solo uso.
- La convierte en **Admin**.
- Quita vínculos LDAP/SAML y la convierte en local.
- Conserva otros ajustes y tokens de autenticación existentes.

Si no existe ese nombre, crea un administrador local nuevo.

1. Abra consola desde XO Lite o una sesión SSH y conviértase en root.
2. Compruebe la base de datos: `systemctl is-active redis` imprime `active`.
3. Ejecute con nombre exacto de cuenta, normalmente un correo. No necesita detener `xo-server`.

   ```bash
   node /opt/xo/packages/xo-server/dist/recover-account-cli.mjs admin@example.net
   ```

4. En `Password (leave empty for random):`, escriba contraseña nueva y Enter. No se muestra. Si queda vacía, imprime una aleatoria: guárdela en su gestor y limpie la pantalla. No pase contraseña en la línea de comandos: quedaría en el historial.
5. Espere `user admin@example.net has been successfully updated`. Si dice `created`, no coincidió con una cuenta existente. Tras acceder, compruebe nombre en **Settings → Users** y elimine la adicional si no la necesita.
6. En ventana privada nueva, acceda con cuenta y contraseña nueva. No pide OTP.
7. En su página de usuario, lea **Authentication tokens**. Si perdió dispositivo o contraseña, seleccione **Forget all authentication tokens**. Elimina todos salvo el de la sesión actual.
8. Si usaba OTP, [configúrelo de nuevo](/docs/xoa-hl/sign-in-otp/) en un dispositivo propio. Si usaba LDAP/SAML, ahora es local: consérvela como administrador de recuperación local o consulte al responsable antes de vincularla otra vez.

**Comprobación:** accede con contraseña nueva, **Settings → Users** muestra **Admin**, columna **OTP** indica **Not configured** y solo quedan tokens esperados.

| Problema | Qué comprobar |
| --- | --- |
| `node: command not found` o `Cannot find module` | Ejecute `rpm -q xoa-hl nodejs` y compruebe que existe el archivo. Use la ruta exactamente indicada. |
| El comando espera sin terminar o indica error Redis | Ejecute [comprobaciones de consola](#appliance-checks) para `redis` y espacio. No borre bases de datos. |
| Sigue fallando el acceso | Compruebe nombre exacto impreso, use ventana privada nueva y lea `journalctl -u xo-server --since '15 min ago'`. |

## Preguntas frecuentes {#common-questions}

**¿Por qué mantenimiento dejó VM o el host deshabilitado?** Guarde la tarea. Compruebe después estado real y ubicación de cada VM. La [prueba de mantenimiento](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) trata evacuación y rehabilitación por separado. Una evacuación parcial o fallo temprano requiere plan del responsable. No omita bloqueos ni repita el interruptor a ciegas.

**¿Por qué falló incorporar un host al pool?** Guarde tarea, error e inventarios de ambos pools. La [prueba de incorporación](/docs/xoa-hl/hosts-pools/#pool-join) comprueba ID, diferencias de parches, maestro, redes y almacenamiento antes de confirmar. La interfaz fuerza la incorporación: no repita ni expulse hosts para despejar fallos inexplicados.

**¿Por qué se rechazó crear una VM delegada?** Siga la [prueba de conjunto y cuota](/docs/xoa-hl/permissions/#resource-set-delegation). Compare usuario exacto, conjunto, ID plantilla/SR/red y Used/Total. Ver plantilla o botón no demuestra autorización del servidor. Guarde error y busque VM/discos parciales antes de repetir. No eleve cuotas ni dé Admin sobre el pool para eludir fallos inexplicados.

**¿Por qué aparecen actualizaciones si el comando devuelve 100?** El comprobador empaquetado transforma código 100 de `dnf check-update` en `AVAILABLE`, 0 en `UP_TO_DATE` y cualquier otro en `ERROR`. Actualizaciones listadas no son instalación fallida.

**¿Cambiar a stable deshace una actualización testing?** No. El canal elige repositorios para comprobaciones e instalaciones posteriores. Pasar a stable no degrada versiones ya instaladas.

**¿Una copia de metadatos del pool demuestra que se recupera un host?** No. La [prueba de metadatos](/docs/xoa-hl/configuration-backup/#pool-metadata) solo comprueba exportación, retención e identidad del archivo. Aún no cubre restaurarlo en un pool aislado.

**¿Una exportación de configuración sustituye una copia de VM o una reversión del appliance?** No. Lea [alcance y límites de recuperación](/docs/xoa-hl/configuration-backup/) y guarde copias de invitados por separado.

## Comunique un problema {#report-a-problem}

[Abra una incidencia XCP-HL](https://github.com/Vagrantin/xcp-hl/issues/new). Proporcione como texto:

- URL e idioma de la página, o ruta del appliance donde ocurre.
- Etiqueta de imagen, versiones de **About**, versiones instaladas de RPM/Node y canal stable/testing.
- Operación, pasos exactos, resultado esperado y error real.
- Hora con zona, modo manual/automático, estado de servicio relacionado y extracto saneado del registro.
- Si se reproduce en un appliance desechable y última versión funcional.

Quite contraseñas, tokens, cookies, nombres/direcciones privados y datos de usuarios/invitados de registros y capturas. Registros `xo-server` y de primer arranque pueden contener credenciales. Nunca adjunte exportación de configuración, clave TLS privada ni configuración completa. Conserve pruebas originales privadamente.

{{< details title="Fuentes" closed="true" >}}
- **Comportamiento de la versión**: [programación de actualizaciones](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md), [códigos de salida de comprobación](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh), [servicio del servidor](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [aprovisionamiento del primer arranque](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh).
- **Diagnóstico de copias de seguridad**: [vista general y detalles de ejecución](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js), [filtros, páginas y visualización de tareas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js), [registro bruto y botones de reinicio](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js), [cálculo de estado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/backups-ng-logs.mjs), [orden de exportación completa y limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [errores de lista remota y registros de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js).
- **Diagnóstico de red**: [vista de redes de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [vista de redes del host](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [vista de redes del pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [visualización de portadora PIF](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [métricas del invitado y asignación de interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [estado de conexión de servidores](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js).
- **Recuperación de administrador**: [comando de recuperación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [actualización de cuenta](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [ruta instalada y configuración](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
{{< /details >}}
