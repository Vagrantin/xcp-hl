---
title: "Crear una copia de seguridad y restaurar una VM"
linkTitle: "Copia de seguridad y restauración"
description: "Respaldar una VM, restaurar una copia segura y probar programaciones, copias incrementales, recuperación de archivos, copias DR y SMB."
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: draft
sourceRevision: sha256:b4f67c2357cf7a39bb06c2688686bbcaa192c9d8d8408f8e293955ce27ad06c9
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protege tu VM de prueba con una copia de seguridad completa en un almacenamiento independiente. Después restaura una copia y comprueba que sus datos sean utilizables. Un trabajo de copia de seguridad correcto es solo la mitad de la prueba: la restauración la completa.

{{< callout type="info" >}}
**Aplicable a** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2), imagen `xoa-image-20261022-a280852`. Basado en el código publicado; todavía no se ha probado en un laboratorio. Otros remotos y modos de copia de seguridad necesitan sus propias pruebas.
{{< /callout >}}

Las secciones 1 a 5 constituyen el tutorial: una copia completa en NFS y una restauración segura. Las secciones posteriores son pruebas opcionales que se apoyan en él: programaciones y retención, copias incrementales, recuperación de un archivo, una copia DR en otro pool y un remoto SMB.

## Antes de empezar {#before-you-begin}

- [Crea e instala una VM de prueba](/docs/xoa-hl/create-vm/). Utiliza una cuenta de administrador de XOA-HL: las páginas de copia de seguridad la requieren en esta versión.
- Obtén una exportación NFS en un sistema de copia de seguridad independiente, no en el almacenamiento que contiene la VM o el dispositivo virtual. El dispositivo virtual debe poder acceder a ella y crear, leer y eliminar archivos. Pide al administrador del almacenamiento el servidor, la ruta de exportación y las opciones de montaje necesarias.
- Comprueba el espacio libre en tres lugares: el destino de copia de seguridad, el SR de la VM (para instantáneas temporales) y el SR con escritura que recibirá los discos restaurados. Deja espacio para la retención configurada más una ejecución adicional. Los tamaños comprimidos no están garantizados.
- En el invitado, crea un pequeño archivo inocuo y anota su contenido o suma de comprobación. Después apágalo normalmente y comprueba que la VM esté detenida. No se garantiza que una copia de una VM en ejecución sea coherente para sus aplicaciones.
- Reserva recursos para una segunda VM. La copia restaurada permanece detenida hasta **eliminar todas sus interfaces de red virtuales (NIC)**. Esta prueba solo utiliza la consola, por lo que la copia no necesita red.

Administra las copias de seguridad desde el **navegador**. Crea y comprueba el archivo de muestra **dentro del invitado**. No necesitas una consola en el host ni en el dispositivo virtual.

## 1. Añadir el destino de copia de seguridad {#1-add-the-backup-destination}

1. Abre **Settings → Remotes** (`/#/settings/remotes`). Reutiliza un remoto adecuado que ya hayas comprobado o crea uno llamado `lab-backup-nfs`.
2. Elige **NFS** e introduce el servidor y la ruta de exportación del administrador del almacenamiento, junto con las opciones de montaje necesarias. Conserva los valores predeterminados de los campos avanzados salvo que tu almacenamiento necesite un cambio. No utilices una carpeta local dentro del dispositivo virtual.
3. Guarda el remoto, habilítalo si es necesario y ejecuta **Test your remote**. Lee cualquier error de conexión o de prueba antes de continuar.

**Comprobación:** el remoto está habilitado, su prueba tiene éxito y no aparece ningún error de conexión. Esto demuestra el acceso, no que se pueda restaurar una copia de una VM.

## 2. Crear un trabajo de copia completa {#2-create-a-full-backup-job}

1. Abre **Backup → New → VMs** (`/#/backup/new/vms`) y llama al trabajo `lab-first-vm-full`.
2. Selecciona únicamente tu VM de prueba. Deja desactivada la selección inteligente para que el trabajo no pueda incluir otras VM.
3. En los modos de copia, selecciona **Backup**. Es el modo de exportación completa. Deja **Rolling snapshot**, **Delta backup**, **Disaster recovery** y **Continuous replication** desactivados.
4. En **Target remotes (for export)**, selecciona `lab-backup-nfs`. Deja **Delete first** desactivado: puede eliminar copias anteriores antes de que la nueva exportación tenga éxito.
5. Añade una programación. Establece **Backup retention** en `2`, elige una zona horaria explícita como `Asia/Tokyo` y comprueba la vista previa de las próximas ejecuciones. La retención es el número de copias conservadas para esta programación, no un número de días.
6. Deshabilita esta programación en la tabla de programaciones antes de guardar el trabajo. Ejecutarás esta primera copia manualmente. La programación permanece deshabilitada hasta [Probar las programaciones y la retención](#backup-schedules).
7. Guarda y comprueba después el resumen: una VM, el remoto correcto y una programación deshabilitada. No cambies los ajustes avanzados de copia para esta primera prueba.

{{< callout type="warning" >}}
La retención puede eliminar copias anteriores en ejecuciones posteriores. Utiliza un destino dedicado al laboratorio y nunca reduzcas la retención de un trabajo de producción para seguir este ejemplo. Una instantánea conservada en el propio SR de la VM no es una copia de seguridad independiente.
{{< /callout >}}

## 3. Ejecutar y comprobar la copia {#3-run-and-check-the-backup}

1. En **Backup → Overview** (`/#/backup/overview`), utiliza la acción de ejecución de la programación deshabilitada del trabajo. Comprueba que la confirmación indique tu trabajo y una sola VM; después confirma.
2. Espera a que termine la ejecución. Abre su registro y comprueba el resultado de la exportación de la VM, no solo que el trabajo haya arrancado. Investiga cualquier advertencia, fallo o dato omitido.
3. Abre **Backup → Restore** (`/#/backup/restore`). Localiza la VM de prueba y comprueba que la nueva copia completa aparezca con la hora y el remoto esperados. Actualiza la lista si es necesario.

**Comprobación:** la ejecución tuvo éxito y aparece su punto de restauración. Anota el trabajo, la programación, el remoto, la hora de la copia y las versiones instaladas. Puedes volver a arrancar el invitado original. Mantén su programación deshabilitada durante la prueba de restauración.

## 4. Restaurar una copia detenida {#4-restore-a-stopped-copy}

1. En **Backup → Restore**, elige la acción de restauración de tu VM de prueba y selecciona la copia completa que acabas de crear.
2. Elige un SR con escritura y suficiente espacio libre. Es almacenamiento para discos de VM, no el remoto NFS ni un SR de ISO.
3. Deja **Start VM after restore** **desactivado**. Activa **Generate new MAC addresses** para que la copia tenga sus propias direcciones de tarjetas de red. Las nuevas direcciones MAC no cambian la IP estática, el nombre de host ni la identidad de las aplicaciones del invitado.
4. Confirma la restauración y espera a que termine. Comprueba si hay errores en su registro. Identifica la nueva VM por su UUID y sus discos restaurados, no por su nombre.
5. Comprueba que la VM restaurada esté detenida. Renómbrala a `lab-first-vm-restore-test` y anota su UUID junto al de la VM original.

**Comprobación:** existe una VM independiente y detenida con los discos esperados. No la arranques todavía. Si está ejecutándose, detenla y comprueba a qué red pudo acceder antes de continuar.

## 5. Aislar, arrancar y comprobar la copia {#5-isolate-start-and-check-the-copy}

1. Abre la pestaña **Network de la copia restaurada** (`/#/vms/<restored-uuid>/network`). Mientras está detenida, elimina **todas** sus NIC y comprueba que la lista esté vacía. Un estado «desconectado» no basta: la NIC podría volver a conectarse en el siguiente arranque.
2. Comprueba otra vez el UUID y la lista vacía de NIC. Después arranca la copia y abre **Console**. No toques la red de la VM original.
3. Comprueba que el invitado arranque, que puedas iniciar sesión por la consola y que el archivo de muestra tenga el contenido o suma de comprobación esperados. Comprueba cualquier otro dato que necesites para la recuperación. Que un invitado arranque todavía no es una recuperación completa de la aplicación.
4. Apaga normalmente el invitado restaurado. Anota el resultado, la hora de la copia, la duración de la restauración y las versiones. Cuando termines, comprueba el UUID y elimina únicamente la copia de prueba y sus discos restaurados. Conserva la VM original y la copia de seguridad.

**Comprobación:** los datos restaurados coinciden con la muestra y la copia no tenía NIC al arrancar. Si falla la prueba, conserva la copia de seguridad, detén la copia restaurada y lee los registros antes de volver a intentarlo.

## Probar las programaciones y la retención {#backup-schedules}

Esta prueba habilita la programación del trabajo de laboratorio, observa tres ejecuciones automáticas y vuelve a deshabilitarla. Hazla solo después de que hayan funcionado la copia y la restauración manuales anteriores.

**Antes de empezar**

- Utiliza únicamente el trabajo de laboratorio `lab-first-vm-full`, su única programación deshabilitada y la única VM de prueba.
- Mantén la VM de prueba apagada en cada ejecución. Un invitado en ejecución necesita su propia prueba de coherencia.
- Comprueba otra vez el espacio libre y el acceso al remoto.
- Conserva cualquier copia de recuperación necesaria **fuera de este trabajo**: la retención puede eliminar sus copias anteriores.

1. En **Backup → Overview**, anota el identificador del trabajo y copia el identificador exacto de la programación con su botón de portapapeles.
2. Edita el trabajo. En **Schedules**, edita la fila deshabilitada existente; no la elimines y recrees. Asígnale un nombre claro de prueba y mantén **Backup retention** en `2`. Deja desactivados **Delete first**, la retención a largo plazo y las comprobaciones automáticas de restauración. Comprueba que solo estén seleccionados el modo **Backup**, la VM de prueba y `lab-backup-nfs`.
3. Establece una regla de prueba con el selector visual de hora y una **Timezone** explícita, como `Asia/Tokyo`. Deja entre ejecuciones más tiempo del que tarda una copia manual, más tiempo para investigar fallos. Comprueba al menos tres próximas ejecuciones y anota **Cron pattern**.
4. Anota también la zona horaria del navegador. La regla se ejecuta en la zona seleccionada, pero la vista previa muestra las horas en la zona del navegador, por lo que el mismo instante puede mostrar otra hora. La vista previa predice fechas; no demuestra que la copia vaya a ejecutarse.
5. Mantén la fila **Disabled** y selecciona **Save**. Vuelve a abrir el trabajo y comprueba el identificador de la programación, la regla, la zona horaria, la retención, la VM y el remoto. El trabajo y su programación se guardan por separado, por lo que un error puede dejar un cambio parcial. No continúes hasta que todo coincida.
6. De vuelta en **Overview**, habilita únicamente esta programación con su botón de estado. El botón se aplica inmediatamente; no hay un guardado aparte. Actualiza y comprueba que la fila muestre **Enabled**.
7. Espera a la siguiente ejecución sin pulsar el botón manual. Abre sus detalles y comprueba los identificadores de trabajo y programación, las horas de inicio y fin, la VM y el resultado de exportación. En **Restore**, comprueba que aparezca un punto nuevo en el remoto correcto.
8. Espera al menos tres ejecuciones correctas de esta programación y compara las horas de los puntos de restauración después de cada una. Con retención `2`, deberían quedar las dos copias completas más recientes de esta VM para esta programación. Comprueba la lista real: no supongas un número de archivos ni cuentes ejecuciones omitidas o fallidas.
9. Antes de la próxima ejecución prevista, deshabilita la programación en **Overview** y actualiza para comprobar **Disabled**. Esto detiene las ejecuciones futuras, pero no cancela una copia en curso (el botón de cancelación está deshabilitado en esta versión). Deja que termine una copia en curso y comprueba que no arranque nada a la siguiente hora prevista.
10. Restaura un punto de una ejecución programada siguiendo las secciones 4 y 5: copia detenida, todas las NIC eliminadas antes del primer arranque, suma de comprobación comparada y copia apagada. Elimina la copia con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/). Anota el estado final de la programación, los puntos restantes y el resultado de la restauración.

**Conviene saber**

- Con **Delete first** desactivado, una ejecución escribe la nueva copia antes de eliminar las anteriores. Si falla la eliminación, puede aparecer como fallida aunque exista la nueva copia. Comprueba los puntos reales antes de repetirla y prueba una restauración antes de confiar en un punto.
- La retención cuenta copias por VM, por modo y por **identificador de programación en cada remoto**. No cuenta días, nombres ni archivos. Otra programación conserva sus propios puntos. Una programación eliminada y recreada recibe un identificador nuevo, por lo que sus copias antiguas no se incorporan a la nueva política.
- Una ejecución que empieza mientras el mismo trabajo sigue activo puede ser rechazada. Las ejecuciones perdidas mientras el dispositivo virtual estaba apagado no se recuperan después.
- Deshabilitar, editar o eliminar un trabajo no cancela una copia en ejecución.

**Si falta una ejecución o falla**, guarda los identificadores del trabajo, la programación y el remoto, las horas esperadas y reales, el error y la lista de puntos de restauración. Hasta conocer el estado, supone que todavía puede empezar una ejecución automática. Comprueba que el servidor esté operativo y su reloj sea correcto; después, el estado habilitado, la selección de VM, el acceso al remoto y el espacio libre. Una vez corregido, ejecuta el trabajo manualmente una vez sin nada más en ejecución, comprueba el nuevo punto y prueba una restauración antes de volver a habilitar la programación.

No se abordan aquí: alertas por correo, cambios de horario de verano, recuperación tras una interrupción, retención a largo plazo y políticas de retención de producción.

## Utilizar copias incrementales {#delta-backups}

Una copia incremental (delta) copia solo lo que ha cambiado desde la anterior. Esta prueba crea un trabajo delta independiente, genera tres puntos de restauración y comprueba que un punto anterior siga restaurándose después de la limpieza por retención. Hazla después de que funcionen la copia completa y la restauración anteriores, y conserva esa copia completa.

**Antes de empezar**

- Utiliza una VM de prueba con discos virtuales normales: sin discos compartidos o de acceso directo, y sin copia de memoria. Anota los UUID de la VM y los discos (VDI), sus tamaños y la ruta y suma de comprobación del archivo de muestra. No cambies los discos durante la prueba.
- Pide al responsable del almacenamiento una exportación NFS nueva y vacía y añádela como remoto independiente, por ejemplo `lab-delta-nfs`.
- Reserva espacio para instantáneas en el SR de origen, para una copia completa más los cambios posteriores en el remoto y para las copias restauradas en un SR con escritura.
- Utiliza una cuenta de administrador. Si faltan **Delta Backup** o sus ajustes en tu instalación, detente e informa de la versión que ves. No cambies la licencia ni sigas instrucciones de XO 6, que tiene una interfaz diferente.

Un punto de restauración delta necesita sus metadatos y su cadena de archivos de disco padre (VHD). Un archivo VHD aislado no es una copia de seguridad de VM. La copia completa del tutorial no puede ser el padre de esta nueva cadena.

### Crear el trabajo delta {#create-the-delta-job}

1. Añade y prueba el remoto como en la sección 1. Abre **Backup → New → VMs** (`/#/backup/new/vms`), llama al trabajo `lab-delta-chain`, selecciona únicamente la VM de prueba y deja desactivada la selección inteligente.
2. Selecciona solo **Delta Backup**. Deja **Backup**, **Rolling Snapshot**, **Disaster Recovery** y **Continuous Replication** desactivados. Selecciona únicamente `lab-delta-nfs` y deja **Delete first** desactivado. No edites el trabajo completo anterior.
3. En **Advanced settings**, establece **Full backup interval** en `2`. Deja **Use NBD to transfer disk if available** y **Purge snapshot data when using CBT.** desactivados. Activa **Merge backups synchronously**. No utilices las demás opciones avanzadas y nunca elimines las instantáneas que conserva este trabajo.
4. Añade una programación con **Backup retention** `2`, una zona horaria explícita y una vista previa comprobada. Deja **Force full backup** desactivado: hace que todas las ejecuciones sean completas. Deja desactivada la retención a largo plazo. Deshabilita la programación y guarda. Vuelve a abrir el trabajo, comprueba cada ajuste y anota los identificadores del trabajo, la programación y el remoto. Mantén la programación deshabilitada durante toda la prueba.

**Full backup interval** establece la longitud de la cadena. Con `2`, un trabajo nuevo hace una copia completa, después una incremental y después otra completa. No es un número de días ni el número de puntos conservados. La ausencia de padres, los cambios de discos o los errores pueden alterar este orden, por lo que debes comprobar los registros.

### Crear tres puntos de restauración {#make-three-restore-points}

Antes de cada ejecución, escribe la muestra en el invitado y apágalo normalmente. Inicia cada ejecución a mano y solo cuando no haya ninguna copia o combinación activa. Para cada ejecución, anota su identificador, la hora, el **Type** de exportación, cualquier advertencia y el nuevo punto de restauración. Revisa el estado de cada tarea y cada página, y guarda el JSON original si es necesario.

| Ejecución | En el invitado antes de apagar | Resultado esperado |
| --- | --- | --- |
| 1 | Escribe la versión A y anota la suma A | Exportación completa; aparece el punto A |
| 2 | Arranca la VM, escribe la versión B, anota la suma B y apaga | Exportación incremental; aparece el punto B. Restaura B (más abajo) antes de la ejecución 3 |
| 3 | Arranca la VM, escribe la versión C, anota la suma C y apaga | Exportación completa (intervalo `2`); comprueba la limpieza y que permanezcan los puntos B y C |

La lista de restauración puede etiquetar como **incremental** un punto de un trabajo delta aunque la exportación haya sido completa. Comprueba el **Type** de exportación en el registro, no esa etiqueta ni el tamaño del archivo. Si la ejecución 2 fue completa, conserva las pruebas, comprueba las instantáneas padre, los discos, el intervalo y los ajustes de **Force**, y no la cuentes como transferencia incremental. Nunca elimines un padre para forzar la prueba.

### Restaurar un punto incremental antes y después de la limpieza {#restore-an-incremental-point-before-and-after-cleanup}

1. En **Backup → Restore** (`/#/backup/restore`), selecciona el punto B en `lab-delta-nfs` y un SR con escritura y espacio suficiente. Incluye **todos los discos**: este diálogo permite omitirlos, por lo que debes comprobar cada uno.
2. Deja **Start VM after restore** y **Use differential restore** desactivados. Activa **Generate new MAC addresses**. La restauración diferencial reutiliza instantáneas de origen y es una prueba distinta.
3. Aísla y comprueba la copia como en las secciones 4 y 5: anota los nuevos UUID, mantenla detenida, elimina **todas** las NIC, arráncala y compara el archivo con la suma B en la consola. Apágala normalmente. Elimina la copia con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/).
4. Después de la ejecución 3 y su limpieza, restaura de nuevo el punto B en otra copia aislada y comprueba la suma B. Restaura el punto C por separado y comprueba la suma C. Esto demuestra que el punto incremental anterior sigue funcionando tras la retención. Anota los puntos restantes y mantén la programación deshabilitada.

**Conviene saber**

- La retención selecciona los puntos de esta VM y esta programación en este remoto. Los límites de combinación o una limpieza fallida pueden dejar puntos adicionales.
- Con **Delete first** desactivado, los puntos antiguos se eliminan después de la transferencia. La limpieza previa a una ejecución todavía puede combinar o eliminar datos.
- La combinación síncrona no hace que una ejecución sea atómica ni demuestra que la recuperación funcione.
- Nunca elimines, renombres, muevas o edites manualmente archivos JSON o VHD de copias de seguridad, ni elimines instantáneas para ordenar una cadena.

**Si algo falla** (un padre ausente, un error de transferencia o combinación, una restauración fallida), guarda el JSON de la ejecución, los identificadores de los puntos de restauración y la lista de VM y discos parciales. Deja de ejecutar el trabajo porque cada ejecución puede cambiar la cadena. Corrige el acceso, el espacio o la propiedad con el responsable de las copias y repite la prueba. No reinicies servicios ni utilices acciones de forzado o reparación como solución genérica. Si no puedes recuperar, conserva la copia completa independiente y mantén la incidencia abierta.

No se abordan aquí: invitados en ejecución, NBD y CBT, remotos cifrados u otros remotos, restauración diferencial y recuperación de fallos reales.

## Recuperar un archivo de una copia delta {#file-restore}

Descarga un archivo de un punto de restauración delta a tu ordenador. Esta prueba utiliza el punto B de la prueba incremental anterior después de que su restauración de VM haya funcionado. No vuelve a colocar el archivo en la VM. Las copias completas del tutorial no aparecen en esta página.

**Antes de empezar**

- Utiliza una VM Linux de prueba con un disco y una partición normal que se pueda leer.
- Antes de la copia B, anota la ruta, el contenido y el SHA-256 de un pequeño archivo de muestra, por ejemplo `/home/lab/recovery-b.txt`.
- Conserva el punto B y su cadena en el remoto. Asegúrate de que tu ordenador tenga espacio para el archivo comprimido.
- Utiliza una cuenta de administrador y comprueba que **File Restore** exista en tu instalación.
- Para esta primera prueba, evita VM de producción, datos privados, volúmenes cifrados o RAID, enlaces simbólicos y carpetas. Esta prueba no demuestra compatibilidad con todos los sistemas de archivos, disposiciones LVM o remotos.

1. Abre **Backup → File Restore** (`/#/backup/file-restore`). Localiza la VM de prueba y abre su acción de restauración de archivos. No pulses los botones de eliminación contiguos. Si falta la VM o el punto, actualiza y comprueba que `lab-delta-nfs` esté habilitado. No cambies a la copia completa anterior.
2. Elige el **punto B** por su hora y trabajo y después el disco. Espera al análisis de particiones y elige la que contiene la muestra. Un disco sin tabla de particiones puede mostrar directamente su sistema de archivos. Si falla el análisis, detente: no montes ni edites manualmente los archivos de copia.
3. Navega desde `/` hasta el archivo de muestra y selecciona **solo ese archivo**. No utilices los controles de selección de carpeta o de todo. Comprueba la ruta y conserva el formato **tgz** (predeterminado; **zip** también funciona, pero puede ser más lento). Inicia la descarga y espera a que el navegador termine. Una ventana emergente bloqueada o una descarga incompleta no es un éxito.
4. En tu ordenador, anota el nombre, el tamaño y el SHA-256 del archivo comprimido. Enumera su contenido, extrae solo la muestra en una carpeta nueva y vacía y compara su contenido y SHA-256 con la versión B. Trata las rutas del archivo como no fiables y nunca extraigas sobre datos en uso. No modifiques la VM original, el punto B ni la programación.

**Comprobación:** el archivo comprimido se abre, contiene solo el archivo de muestra y este coincide con la suma B. Que coincida el nombre, o que el contenido corresponda a la versión C, no es una coincidencia válida.

Si falla un paso, guarda las pruebas y detén las siguientes ejecuciones de copia hasta que su responsable las haya revisado. No elimines archivos de la cadena, instantáneas de origen ni archivos parciales para hacer aparecer un punto. Copiar el archivo recuperado de vuelta al invitado es una tarea aparte que requiere la aprobación de su propietario.

## Copiar una VM a otro pool (réplica DR) {#dr-replica}

**Disaster Recovery** (DR) copia una VM completa a un SR de otro pool. Es diferente de una copia en NFS y de **Continuous Replication** (CR), que solo envía los cambios. La copia, llamada réplica, permanece detenida y con el arranque bloqueado. **No desbloquees ni arranques la réplica.** Para utilizarla, debes clonarla. Esta prueba comprueba uno de esos clones en un lugar aislado. No prueba la conmutación automática, la pérdida del pool de origen ni el retorno al origen (failback).

**Antes de empezar**

- Utiliza una VM de prueba en el pool A y un segundo pool de prueba B administrado por el mismo dispositivo virtual XOA-HL.
- Pide al propietario del pool B un SR dedicado con escritura, `lab-dr-sr`, con espacio para dos copias completas y un clon. Debe estar en un almacenamiento diferente del pool A y no debe ser una biblioteca ISO. Anota los UUID de ambos pools y SR, el espacio libre y qué hosts pueden acceder al SR.
- Conserva la copia NFS independiente del tutorial.
- Utiliza una VM de un solo disco sin discos compartidos o de acceso directo. Antes de cada ejecución, escribe una muestra (A, después B y después C), anota su SHA-256 y apaga el invitado normalmente.
- Planifica el acceso a consola y un lugar en el pool B **sin red de producción**. Eliminarás todas las NIC del clon antes de arrancarlo.
- Si DR o el SR de destino no están disponibles en tu instalación, detente.

1. Abre **Backup → New → VMs** (`/#/backup/new/vms`) y crea el trabajo `lab-dr-full`. Selecciona únicamente la VM de prueba y deja desactivada la selección inteligente. Selecciona solo **Disaster Recovery**; deja **Backup**, **Delta Backup**, **Continuous Replication** y **Rolling Snapshot** desactivados. En **Target SRs (for replication)**, selecciona únicamente `lab-dr-sr`. Deja **Delete first** desactivado para no eliminar réplicas antiguas antes de la transferencia. No edites los demás trabajos.
2. Añade una programación con **Replication retention** `2`, una zona horaria explícita y una vista previa comprobada. No utilices la retención de instantáneas ni las comprobaciones de estado. Deshabilita la programación y guarda. Vuelve a abrir el trabajo y comprueba la VM, el SR de destino, el modo, la retención, el estado deshabilitado y los identificadores.
3. Con la muestra A escrita y el invitado apagado, ejecuta el trabajo una vez desde **Backup → Overview**. Comprueba todas las tareas y advertencias. En el pool B, localiza la nueva réplica **detenida** por su UUID, el trabajo y la hora de su nombre, su etiqueta **Disaster Recovery** y su disco. No la arranques.
4. Repite con la muestra B y después con C, completando una ejecución antes de la siguiente. Anota los identificadores de ejecución y réplica, las horas, los discos y los errores. Después de la tercera ejecución, comprueba qué réplicas permanecen: normalmente B y C. Un trabajo en verde no demuestra que los datos sean correctos, y una eliminación fallida no se revierte.
5. Selecciona la **réplica B**, no la VM de origen, la réplica C ni un punto NFS. Haz un **Fast clone** con un nombre exclusivo en el pool B y deja la réplica detenida. Anota los nuevos identificadores de VM y discos del clon y comprueba que esté detenido y sin bloqueo de arranque. Si falla la clonación o el clon está bloqueado, detente; no omitas el bloqueo.
6. Elimina **todas** las NIC del clon detenido y comprueba que su lista de red esté vacía. Arranca únicamente el clon, abre su consola y compara la muestra con la suma B. Apágalo normalmente. Puedes probar un clon de C del mismo modo.
7. Conserva las réplicas B y C y la copia NFS. Elimina únicamente los clones de prueba con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/).

**Comprobación:** tres ejecuciones completas llegaron al pool y SR correctos; permanecen B y C, o puedes explicar por qué no; el clon aislado de B tiene sus propios identificadores, no tenía NIC al arrancar y contiene exactamente la muestra B.

Si falla una transferencia, una comprobación de espacio, una eliminación, una clonación o una comprobación de datos, detén las siguientes ejecuciones y entrega el inventario a los responsables de las copias y del almacenamiento. Nunca retires el bloqueo de arranque de una réplica, elimines un punto solo por su nombre ni elimines una instantánea gestionada por el trabajo de copia.

No se abordan aquí: cadenas CR, ejecuciones programadas, cambio de red, prevención de la ejecución simultánea de la misma VM, retorno al origen y cortes reales.

## Probar una copia SMB en Windows Server {#smb-remote}

Prueba un remoto SMB con una copia completa y una restauración aislada. La interfaz de XO advierte de que los remotos SMB están destinados a **Windows Server** y recomienda NFS para Samba en Linux y la mayoría de los dispositivos NAS. Esta prueba no cubre otros servidores SMB, almacenamiento SMB para ISO o discos de VM, remotos en la nube ni uso en producción. XO monta el recurso compartido con CIFS y el paquete XOA-HL incluye `cifs-utils`, pero todavía no se ha comprobado el montaje en un dispositivo virtual real.

**Antes de empezar**

- Pide al administrador de Windows Server un **recurso compartido dedicado a pruebas**, en un almacenamiento diferente del de la VM de origen y el dispositivo virtual, con espacio suficiente para la copia y la prueba de restauración.
- Solicita una cuenta dedicada que pueda crear, leer y eliminar archivos en ese recurso, con acceso por red únicamente desde el dispositivo virtual. Obtén el nombre del servidor, el recurso compartido, la subcarpeta opcional, el dominio y las credenciales por un canal seguro.
- Escribe la contraseña únicamente en su campo. XO construye una URL interna del remoto que contiene las credenciales, por lo que debes tratar las exportaciones de configuración de XO como secretos. Nunca compartas esa URL ni incluyas credenciales en capturas, incidencias, extractos de registros u opciones de montaje personalizadas.
- Conserva la copia NFS independiente del tutorial. Utiliza la misma VM de prueba pequeña, detenida y de un solo disco, con un nuevo archivo de muestra y su suma de comprobación. Reserva un SR con escritura y un lugar con acceso solo por consola para la copia restaurada.

1. En **Settings → Remotes** (`/#/settings/remotes`), crea `lab-backup-smb` de tipo **SMB**. En **Address\\Share**, introduce el servidor y el recurso compartido separados por una barra invertida. **Subfolder** es una ruta opcional dentro de ese recurso, no una segunda ruta de recurso compartido. Introduce el usuario dedicado, la contraseña y el dominio (el formulario comienza con `WORKGROUP`; utiliza el valor del administrador). Conserva los valores predeterminados de **Custom mount options**, proxy y cifrado. Guarda y comprueba el identificador del remoto, su estado habilitado, tipo, servidor, recurso, subcarpeta e indicador de error. La contraseña permanece oculta: no intentes leerla de la URL mostrada.
2. Ejecuta **Test your remote** en este remoto. Escribe un archivo aleatorio de 10 MiB, lo vuelve a leer, lo compara e intenta eliminarlo. Comprueba el icono de éxito, el resultado y cualquier paso fallido. Si falló un paso, pide al administrador que busque un archivo `.test` residual por su nombre exacto. Una prueba correcta solo demuestra este recorrido de escritura y lectura, no una restauración de VM ni una velocidad sostenida.
3. En **Backup → New → VMs** (`/#/backup/new/vms`), crea un trabajo independiente llamado `lab-smb-full`: únicamente la VM de prueba detenida, solo modo **Backup** (completo), `lab-backup-smb` como único remoto de destino y **Delete first** desactivado. Añade una programación con zona horaria explícita y **Backup retention** `2`, mantenla deshabilitada, guarda y comprueba los identificadores. No cambies el trabajo NFS.
4. Ejecuta manualmente la programación deshabilitada una vez desde **Backup → Overview**. Comprueba la exportación de la VM y el resultado del remoto en el registro; después localiza el punto completo de `lab-backup-smb` en **Backup → Restore**. Anota las horas, los identificadores, el tamaño y cualquier error de montaje SMB, inicio de sesión o espacio. Una instantánea abandonada en el SR de origen o una prueba de remoto correcta no es una copia de seguridad de VM.
5. Restaura ese punto en el SR reservado con **Start VM after restore** desactivado. Anota los nuevos UUID de VM y discos. Con la copia detenida, elimina **todas las NIC** y comprueba que la lista de red esté vacía. Arranca únicamente esta copia desde **Console**, compara la suma de la muestra y apágala. Conserva la VM original, la copia NFS y el punto SMB hasta registrar el resultado. Después elimina únicamente la copia de prueba con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/).

**Comprobación:** la prueba del remoto tiene éxito, la copia completa llega al recurso compartido y la copia aislada arranca sin NIC y con los datos correctos.

Si fallan el acceso, la escritura, la lectura, la eliminación, la exportación o la restauración, detente. Entrega a los responsables de las copias y del servidor los errores (sin credenciales), los identificadores exactos, el contenido del recurso y las VM parciales. Nunca vuelvas a intentarlo contra un recurso de producción ni elimines rutas de copia solo por su nombre.

No se abordan aquí: rotación de contraseñas, cortes del recurso compartido, retención durante muchas ejecuciones, confianza de dominio, versiones SMB y ajustes de seguridad, velocidad y otros servidores SMB.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| Falla la prueba NFS | Comprueba que el dispositivo virtual pueda acceder al servidor y revisa la ruta de exportación, los permisos y las opciones de montaje. Que tu navegador llegue al NAS no basta. |
| Falla la copia o no aparece un punto de restauración | Lee los registros de la VM y de exportación. Comprueba el acceso al remoto y su espacio libre, el espacio libre del SR de la VM y la VM seleccionada. Una instantánea residual no es una copia de seguridad. |
| Falta el punto de restauración | Comprueba que el remoto esté habilitado y sin errores, actualiza la lista y comprueba que el trabajo realmente exportó esta VM. |
| Falla la restauración | Lee su registro y comprueba que se pueda leer el remoto, que el SR de destino tenga espacio y que el host pueda acceder a él. Busca una VM parcial antes de repetirlo. Nunca elimines solo por el nombre. |
| Falla la réplica DR o su clon | Anota los identificadores de ejecución, VM y discos, el espacio y el acceso del SR de destino y el estado de bloqueo. Mantén las réplicas detenidas. No omitas su bloqueo de arranque ni vuelvas a ejecutar la retención a ciegas. |
| Falla el remoto SMB o su restauración | Con el responsable de Windows Server, comprueba el paso fallido de la prueba, los registros de trabajo y restauración, el servidor y recurso compartido, el acceso de la cuenta, el espacio libre y los objetos parciales. Conserva la copia NFS independiente. Nunca pegues credenciales en un informe. |
| La VM restaurada no tiene red | Es lo esperado: eliminaste todas las NIC para esta prueba exclusivamente por consola. Conectarla a una red de producción requiere revisar por separado su dirección IP y las identidades de los servicios. |
| El archivo difiere o el invitado no arranca | Comprueba que seleccionaste el punto de restauración correcto y que el archivo se escribió antes de la copia. Conserva los registros y la copia. La prueba no se ha superado. |

Para los estados de ejecución, las exportaciones parciales y un nuevo intento seguro, consulta [Diagnosticar una copia de seguridad fallida](/docs/xoa-hl/troubleshooting/#backup-failures).

## Siguientes pasos {#next-steps}

Tras una prueba de restauración correcta, decide la frecuencia real de las copias, la retención, la supervisión de capacidad y cómo garantizar la coherencia de las copias para tus aplicaciones. Habilita una programación solo después de comprobar su zona horaria y las próximas ejecuciones. Consulta también la [guía de actualización](/docs/guides/updates/) y el [glosario](/docs/xoa-hl/glossary/). La recuperación de configuración y Continuous Replication necesitan sus propios procedimientos.

{{< details title="Fuentes" closed="true" >}}
- **Programaciones**: [editor, tabla y orden de guardado de programaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [selector de hora y formato de vista previa](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [API, inicio y parada de programaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [comportamiento de tareas cron](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [protección de trabajo en curso e identidad del registro](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs), [retención de copias completas y orden de limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).
- **Copia de seguridad y restauración**: [rutas de copia y acceso de administrador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [formulario de remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [prueba de remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [modos de trabajo y guardado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [programación y retención](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [ejecución manual](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [controles de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [eliminación de NIC](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [versión fijada del proyecto original](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [selección de parches y compilación](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Copias incrementales**: [exportación incremental y selección de base](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs), [transferencia al remoto y retención](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs), [retención de instantáneas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs), [ejecución de limpieza y combinación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs), [lector de cadena de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [implementación de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/ImportVmBackup.mjs), [tipo de exportación en los registros](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js).
- **Recuperación de un archivo**: [interfaz de restauración de archivos y filtro delta](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/index.js), [selector de copia, disco, partición y archivo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/restore-file-modal.js), [API de archivos para administradores y respuesta de archivo comprimido](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/backup-ng.mjs), [partición de solo lectura y adaptador tgz/zip](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [descarga del navegador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **Réplica DR**: [modo del trabajo, SR de destino y programación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [control de retención de replicación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [exportación completa y escritor de SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/FullXapi.mjs), [importación de réplica, bloqueo de arranque y limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullXapiWriter.mjs), [filtro de identidad de réplica](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_listReplicatedVms.mjs), [API de clonación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Remoto SMB**: [formulario de remoto y advertencia de Windows Server](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [analizador y formateador SMB](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-remote-parser/src/index.js), [gestor CIFS](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/smb.js), [opciones de montaje y de remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/_mount.js), [prueba de remoto de 10 MiB](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/abstract.js), [ciclo de vida del remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/remotes.mjs), [dependencia de ejecución de XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **Incidencia conocida**: [encabezados de resultados de prueba de remoto (xoa-hl#38)](https://github.com/Vagrantin/xoa-hl/issues/38).
{{< /details >}}
