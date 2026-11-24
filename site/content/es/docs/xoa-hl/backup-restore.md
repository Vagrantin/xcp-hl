---
title: "Crear una copia de seguridad y restaurar una VM"
linkTitle: "Copia de seguridad y restauración"
description: "Respaldar una VM, restaurar una copia segura y probar programaciones, copias incrementales, recuperación de archivos, copias DR y SMB."
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: reviewed
sourceRevision: sha256:1086c300f289c6bf85166266f4e7aac3092d477f4500f32b042493af06b7a089
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Protege su VM de prueba con una copia de seguridad completa en un almacenamiento independiente. Después restaure una copia y compruebe que sus datos sean utilizables. Un trabajo de copia de seguridad correcto es solo la mitad de la prueba: la restauración la completa.

{{< callout type="info" >}}
**Aplicable a** XOA-HL `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2), imagen `xoa-image-20261027-ca44911`. Probado en un dispositivo virtual de laboratorio el 27 de octubre de 2026 con un remoto NFS y una copia completa. Otros remotos y modos de copia de seguridad necesitan sus propias pruebas.
{{< /callout >}}

Las secciones 1 a 5 constituyen el tutorial: una copia completa en NFS y una restauración segura. Las secciones posteriores son pruebas opcionales que se apoyan en él: programaciones y retención, copias incrementales, recuperación de un archivo, una copia DR en otro pool y un remoto SMB.

## Antes de empezar {#before-you-begin}

- [Cree e instale una VM de prueba](/docs/xoa-hl/create-vm/). Utilice una cuenta de administrador de XOA-HL: las páginas de copia de seguridad la requieren en esta versión.
- Obtenga una exportación NFS en un sistema de copia de seguridad independiente, no en el almacenamiento que contiene la VM o el dispositivo virtual. El dispositivo virtual debe poder acceder a ella y crear, leer y eliminar archivos. Pida al administrador del almacenamiento el servidor, la ruta de exportación y las opciones de montaje necesarias.
- Compruebe el espacio libre en tres lugares: el destino de copia de seguridad, el SR de la VM (para instantáneas temporales) y el SR con escritura que recibirá los discos restaurados. Deje espacio para la retención configurada más una ejecución adicional. Los tamaños comprimidos no están garantizados.
- En el invitado, cree un pequeño archivo inocuo y anote su contenido o suma de comprobación. Después apáguelo normalmente y compruebe que la VM esté detenida. No se garantiza que una copia de una VM en ejecución sea coherente para sus aplicaciones.
- Reserve recursos para una segunda VM. La copia restaurada permanece detenida hasta **eliminar todas sus interfaces de red virtuales (NIC)**. Esta prueba solo utiliza la consola, por lo que la copia no necesita red.

Administre las copias de seguridad desde el **navegador**. Cree y compruebe el archivo de muestra **dentro del invitado**. No necesita una consola en el host ni en el dispositivo virtual.

## 1. Añadir el destino de copia de seguridad {#1-add-the-backup-destination}

1. Abra **Settings → Remotes** (`/#/settings/remotes`). Reutilice un remoto adecuado que ya haya comprobado o cree uno llamado `lab-backup-nfs`.
2. Elija **NFS** e introduzca el servidor y la ruta de exportación del administrador del almacenamiento, junto con las opciones de montaje necesarias. Conserve los valores predeterminados de los campos avanzados salvo que su almacenamiento necesite un cambio. No utilice una carpeta local dentro del dispositivo virtual.
3. Guarde el remoto, habilítelo si es necesario y ejecute **Test your remote**. Lea cualquier error de conexión o de prueba antes de continuar.

**Comprobación:** el remoto está habilitado, su prueba tiene éxito y no aparece ningún error de conexión. Esto demuestra el acceso, no que se pueda restaurar una copia de una VM.

## 2. Crear un trabajo de copia completa {#2-create-a-full-backup-job}

1. Abra **Backup → New → VMs** (`/#/backup/new/vms`) y llame al trabajo `lab-first-vm-full`.
2. Seleccione únicamente su VM de prueba. Deje desactivada la selección inteligente para que el trabajo no pueda incluir otras VM.
3. En los modos de copia, seleccione **Backup**. Es el modo de exportación completa. Deje **Rolling snapshot**, **Delta backup**, **Disaster recovery** y **Continuous replication** desactivados.
4. En **Target remotes (for export)**, seleccione `lab-backup-nfs`. Deje **Delete first** desactivado: puede eliminar copias anteriores antes de que la nueva exportación tenga éxito.
5. Añada una programación. Establezca **Backup retention** en `2`, elija una zona horaria explícita como `Asia/Tokyo` y compruebe la vista previa de las próximas ejecuciones. La retención es el número de copias conservadas para esta programación, no un número de días.
6. Deshabilite esta programación en la tabla de programaciones antes de guardar el trabajo. Ejecutará esta primera copia manualmente. La programación permanece deshabilitada hasta [Probar las programaciones y la retención](#backup-schedules).
7. Guarde y compruebe después el resumen: una VM, el remoto correcto y una programación deshabilitada. No cambie los ajustes avanzados de copia para esta primera prueba.

{{< callout type="warning" >}}
La retención puede eliminar copias anteriores en ejecuciones posteriores. Utilice un destino dedicado al laboratorio y nunca reduzca la retención de un trabajo de producción para seguir este ejemplo. Una instantánea conservada en el propio SR de la VM no es una copia de seguridad independiente.
{{< /callout >}}

## 3. Ejecutar y comprobar la copia {#3-run-and-check-the-backup}

1. En **Backup → Overview** (`/#/backup/overview`), utilice la acción de ejecución de la programación deshabilitada del trabajo. Compruebe que la confirmación indique su trabajo y una sola VM; después confirme.
2. Espere a que termine la ejecución. Abra su registro y compruebe el resultado de la exportación de la VM, no solo que el trabajo haya arrancado. Investigue cualquier advertencia, fallo o dato omitido.
3. Abra **Backup → Restore** (`/#/backup/restore`). Localice la VM de prueba y compruebe que la nueva copia completa aparezca con la hora y el remoto esperados. Actualice la lista si es necesario.

**Comprobación:** la ejecución tuvo éxito y aparece su punto de restauración. Anote el trabajo, la programación, el remoto, la hora de la copia y las versiones instaladas. Puede volver a arrancar el invitado original. Mantenga su programación deshabilitada durante la prueba de restauración.

## 4. Restaurar una copia detenida {#4-restore-a-stopped-copy}

1. En **Backup → Restore**, elija la acción de restauración de su VM de prueba y seleccione la copia completa que acaba de crear.
2. Elija un SR con escritura y suficiente espacio libre. Es almacenamiento para discos de VM, no el remoto NFS ni un SR de ISO.
3. Deje **Start VM after restore** **desactivado**. Active **Generate new MAC addresses** para que la copia tenga sus propias direcciones de tarjetas de red. Las nuevas direcciones MAC no cambian la IP estática, el nombre de host ni la identidad de las aplicaciones del invitado.
4. Confirme la restauración y espere a que termine. Compruebe si hay errores en su registro. Identifique la nueva VM por su UUID y sus discos restaurados, no por su nombre.
5. Compruebe que la VM restaurada esté detenida. Renómbrela a `lab-first-vm-restore-test` y anote su UUID junto al de la VM original.

**Comprobación:** existe una VM independiente y detenida con los discos esperados. No la arranque todavía. Si está ejecutándose, deténgala y compruebe a qué red pudo acceder antes de continuar.

## 5. Aislar, arrancar y comprobar la copia {#5-isolate-start-and-check-the-copy}

1. Abra la pestaña **Network de la copia restaurada** (`/#/vms/<restored-uuid>/network`). Mientras está detenida, elimine **todas** sus NIC y compruebe que la lista esté vacía. Un estado «desconectado» no basta: la NIC podría volver a conectarse en el siguiente arranque.
2. Compruebe otra vez el UUID y la lista vacía de NIC. Después arranque la copia y abra **Console**. No toque la red de la VM original.
3. Compruebe que el invitado arranque, que pueda iniciar sesión por la consola y que el archivo de muestra tenga el contenido o suma de comprobación esperados. Compruebe cualquier otro dato que necesite para la recuperación. Que un invitado arranque todavía no es una recuperación completa de la aplicación.
4. Apague normalmente el invitado restaurado. Anote el resultado, la hora de la copia, la duración de la restauración y las versiones. Cuando termine, compruebe el UUID y elimine únicamente la copia de prueba y sus discos restaurados. Conserve la VM original y la copia de seguridad.

**Comprobación:** los datos restaurados coinciden con la muestra y la copia no tenía NIC al arrancar. Si falla la prueba, conserve la copia de seguridad, detén la copia restaurada y lea los registros antes de volver a intentarlo.

## Probar las programaciones y la retención {#backup-schedules}

Esta prueba habilita la programación del trabajo de laboratorio, observa tres ejecuciones automáticas y vuelve a deshabilitarla. Hágala solo después de que hayan funcionado la copia y la restauración manuales anteriores.

**Antes de empezar**

- Utilice únicamente el trabajo de laboratorio `lab-first-vm-full`, su única programación deshabilitada y la única VM de prueba.
- Mantenga la VM de prueba apagada en cada ejecución. Un invitado en ejecución necesita su propia prueba de coherencia.
- Compruebe otra vez el espacio libre y el acceso al remoto.
- Conserve cualquier copia de recuperación necesaria **fuera de este trabajo**: la retención puede eliminar sus copias anteriores.

1. En **Backup → Overview**, anote el identificador del trabajo y copie el identificador exacto de la programación con su botón de portapapeles.
2. Edite el trabajo. En **Schedules**, edite la fila deshabilitada existente; no la elimine y recree. Asígnele un nombre claro de prueba y mantenga **Backup retention** en `2`. Deje desactivados **Delete first**, la retención a largo plazo y las comprobaciones automáticas de restauración. Compruebe que solo estén seleccionados el modo **Backup**, la VM de prueba y `lab-backup-nfs`.
3. Establezca una regla de prueba con el selector visual de hora y una **Timezone** explícita, como `Asia/Tokyo`. Deje entre ejecuciones más tiempo del que tarda una copia manual, más tiempo para investigar fallos. Compruebe al menos tres próximas ejecuciones y anote **Cron pattern**.
4. Anote también la zona horaria del navegador. La regla se ejecuta en la zona seleccionada, pero la vista previa muestra las horas en la zona del navegador, por lo que el mismo instante puede mostrar otra hora. La vista previa predice fechas; no demuestra que la copia vaya a ejecutarse.
5. Mantenga la fila **Disabled** y seleccione **Save**. Vuelva a abrir el trabajo y compruebe el identificador de la programación, la regla, la zona horaria, la retención, la VM y el remoto. El trabajo y su programación se guardan por separado, por lo que un error puede dejar un cambio parcial. No continúe hasta que todo coincida.
6. De vuelta en **Overview**, habilite únicamente esta programación con su botón de estado. El botón se aplica inmediatamente; no hay un guardado aparte. Actualice y compruebe que la fila muestre **Enabled**.
7. Espere a la siguiente ejecución sin pulsar el botón manual. Abra sus detalles y compruebe los identificadores de trabajo y programación, las horas de inicio y fin, la VM y el resultado de exportación. En **Restore**, compruebe que aparezca un punto nuevo en el remoto correcto.
8. Espere al menos tres ejecuciones correctas de esta programación y compare las horas de los puntos de restauración después de cada una. Con retención `2`, deberían quedar las dos copias completas más recientes de esta VM para esta programación. Compruebe la lista real: no suponga un número de archivos ni cuente ejecuciones omitidas o fallidas.
9. Antes de la próxima ejecución prevista, deshabilite la programación en **Overview** y actualice para comprobar **Disabled**. Esto detiene las ejecuciones futuras, pero no cancela una copia en curso (el botón de cancelación está deshabilitado en esta versión). Deje que termine una copia en curso y compruebe que no arranque nada a la siguiente hora prevista.
10. Restaure un punto de una ejecución programada siguiendo las secciones 4 y 5: copia detenida, todas las NIC eliminadas antes del primer arranque, suma de comprobación comparada y copia apagada. Elimine la copia con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/). Anote el estado final de la programación, los puntos restantes y el resultado de la restauración.

**Conviene saber**

- Con **Delete first** desactivado, una ejecución escribe la nueva copia antes de eliminar las anteriores. Si falla la eliminación, puede aparecer como fallida aunque exista la nueva copia. Compruebe los puntos reales antes de repetirla y pruebe una restauración antes de confiar en un punto.
- La retención cuenta copias por VM, por modo y por **identificador de programación en cada remoto**. No cuenta días, nombres ni archivos. Otra programación conserva sus propios puntos. Una programación eliminada y recreada recibe un identificador nuevo, por lo que sus copias antiguas no se incorporan a la nueva política.
- Una ejecución que empieza mientras el mismo trabajo sigue activo puede ser rechazada. Las ejecuciones perdidas mientras el dispositivo virtual estaba apagado no se recuperan después.
- Deshabilitar, editar o eliminar un trabajo no cancela una copia en ejecución.

**Si falta una ejecución o falla**, guarde los identificadores del trabajo, la programación y el remoto, las horas esperadas y reales, el error y la lista de puntos de restauración. Hasta conocer el estado, suponga que todavía puede empezar una ejecución automática. Compruebe que el servidor esté operativo y su reloj sea correcto; después, el estado habilitado, la selección de VM, el acceso al remoto y el espacio libre. Una vez corregido, ejecute el trabajo manualmente una vez sin nada más en ejecución, compruebe el nuevo punto y pruebe una restauración antes de volver a habilitar la programación.

No se abordan aquí: alertas por correo, cambios de horario de verano, recuperación tras una interrupción, retención a largo plazo y políticas de retención de producción.

## Utilizar copias incrementales {#delta-backups}

Una copia incremental (delta) copia solo lo que ha cambiado desde la anterior. Esta prueba crea un trabajo delta independiente, genera tres puntos de restauración y comprueba que un punto anterior siga restaurándose después de la limpieza por retención. Hágala después de que funcionen la copia completa y la restauración anteriores, y conserve esa copia completa.

**Antes de empezar**

- Utilice una VM de prueba con discos virtuales normales: sin discos compartidos o de acceso directo, y sin copia de memoria. Anote los UUID de la VM y los discos (VDI), sus tamaños y la ruta y suma de comprobación del archivo de muestra. No cambie los discos durante la prueba.
- Pida al responsable del almacenamiento una exportación NFS nueva y vacía y añádala como remoto independiente, por ejemplo `lab-delta-nfs`.
- Reserve espacio para instantáneas en el SR de origen, para una copia completa más los cambios posteriores en el remoto y para las copias restauradas en un SR con escritura.
- Utilice una cuenta de administrador. Si faltan **Delta Backup** o sus ajustes en su instalación, deténgase e informe de la versión que ve. No cambie la licencia ni siga instrucciones de XO 6, que tiene una interfaz diferente.

Un punto de restauración delta necesita sus metadatos y su cadena de archivos de disco padre (VHD). Un archivo VHD aislado no es una copia de seguridad de VM. La copia completa del tutorial no puede ser el padre de esta nueva cadena.

### Crear el trabajo delta {#create-the-delta-job}

1. Añada y pruebe el remoto como en la sección 1. Abra **Backup → New → VMs** (`/#/backup/new/vms`), llame al trabajo `lab-delta-chain`, seleccione únicamente la VM de prueba y deje desactivada la selección inteligente.
2. Seleccione solo **Delta Backup**. Deje **Backup**, **Rolling Snapshot**, **Disaster Recovery** y **Continuous Replication** desactivados. Seleccione únicamente `lab-delta-nfs` y deje **Delete first** desactivado. No edite el trabajo completo anterior.
3. En **Advanced settings**, establezca **Full backup interval** en `2`. Deje **Use NBD to transfer disk if available** y **Purge snapshot data when using CBT.** desactivados. Active **Merge backups synchronously**. No utilice las demás opciones avanzadas y nunca elimine las instantáneas que conserva este trabajo.
4. Añada una programación con **Backup retention** `2`, una zona horaria explícita y una vista previa comprobada. Deje **Force full backup** desactivado: hace que todas las ejecuciones sean completas. Deje desactivada la retención a largo plazo. Deshabilite la programación y guarde. Vuelva a abrir el trabajo, compruebe cada ajuste y anote los identificadores del trabajo, la programación y el remoto. Mantenga la programación deshabilitada durante toda la prueba.

**Full backup interval** establece la longitud de la cadena. Con `2`, un trabajo nuevo hace una copia completa, después una incremental y después otra completa. No es un número de días ni el número de puntos conservados. La ausencia de padres, los cambios de discos o los errores pueden alterar este orden, por lo que debe comprobar los registros.

### Crear tres puntos de restauración {#make-three-restore-points}

Antes de cada ejecución, escriba la muestra en el invitado y apáguelo normalmente. Inicie cada ejecución a mano y solo cuando no haya ninguna copia o combinación activa. Para cada ejecución, anote su identificador, la hora, el **Type** de exportación, cualquier advertencia y el nuevo punto de restauración. Revise el estado de cada tarea y cada página, y guarde el JSON original si es necesario.

| Ejecución | En el invitado antes de apagar | Resultado esperado |
| --- | --- | --- |
| 1 | Escriba la versión A y anote la suma A | Exportación completa; aparece el punto A |
| 2 | Arranque la VM, escriba la versión B, anote la suma B y apague | Exportación incremental; aparece el punto B. Restaure B (más abajo) antes de la ejecución 3 |
| 3 | Arranque la VM, escriba la versión C, anote la suma C y apague | Exportación completa (intervalo `2`); compruebe la limpieza y que permanezcan los puntos B y C |

La lista de restauración puede etiquetar como **incremental** un punto de un trabajo delta aunque la exportación haya sido completa. Compruebe el **Type** de exportación en el registro, no esa etiqueta ni el tamaño del archivo. Si la ejecución 2 fue completa, conserve las pruebas, compruebe las instantáneas padre, los discos, el intervalo y los ajustes de **Force**, y no la cuente como transferencia incremental. Nunca elimine un padre para forzar la prueba.

### Restaurar un punto incremental antes y después de la limpieza {#restore-an-incremental-point-before-and-after-cleanup}

1. En **Backup → Restore** (`/#/backup/restore`), seleccione el punto B en `lab-delta-nfs` y un SR con escritura y espacio suficiente. Incluya **todos los discos**: este diálogo permite omitirlos, por lo que debe comprobar cada uno.
2. Deje **Start VM after restore** y **Use differential restore** desactivados. Active **Generate new MAC addresses**. La restauración diferencial reutiliza instantáneas de origen y es una prueba distinta.
3. Aísle y compruebe la copia como en las secciones 4 y 5: anote los nuevos UUID, manténgala detenida, elimine **todas** las NIC, arránquela y compare el archivo con la suma B en la consola. Apáguela normalmente. Elimine la copia con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/).
4. Después de la ejecución 3 y su limpieza, restaure de nuevo el punto B en otra copia aislada y compruebe la suma B. Restaure el punto C por separado y compruebe la suma C. Esto demuestra que el punto incremental anterior sigue funcionando tras la retención. Anote los puntos restantes y mantenga la programación deshabilitada.

**Conviene saber**

- La retención selecciona los puntos de esta VM y esta programación en este remoto. Los límites de combinación o una limpieza fallida pueden dejar puntos adicionales.
- Con **Delete first** desactivado, los puntos antiguos se eliminan después de la transferencia. La limpieza previa a una ejecución todavía puede combinar o eliminar datos.
- La combinación síncrona no hace que una ejecución sea atómica ni demuestra que la recuperación funcione.
- Nunca elimine, renombre, mueva o edite manualmente archivos JSON o VHD de copias de seguridad, ni elimine instantáneas para ordenar una cadena.

**Si algo falla** (un padre ausente, un error de transferencia o combinación, una restauración fallida), guarde el JSON de la ejecución, los identificadores de los puntos de restauración y la lista de VM y discos parciales. Deje de ejecutar el trabajo porque cada ejecución puede cambiar la cadena. Corrija el acceso, el espacio o la propiedad con el responsable de las copias y repita la prueba. No reinicie servicios ni utilice acciones de forzado o reparación como solución genérica. Si no puede recuperar, conserve la copia completa independiente y mantenga la incidencia abierta.

No se abordan aquí: invitados en ejecución, NBD y CBT, remotos cifrados u otros remotos, restauración diferencial y recuperación de fallos reales.

## Recuperar un archivo de una copia delta {#file-restore}

Descargue un archivo de un punto de restauración delta a su ordenador. Esta prueba utiliza el punto B de la prueba incremental anterior después de que su restauración de VM haya funcionado. No vuelve a colocar el archivo en la VM. Las copias completas del tutorial no aparecen en esta página.

**Antes de empezar**

- Utilice una VM Linux de prueba con un disco y una partición normal que se pueda leer.
- Antes de la copia B, anote la ruta, el contenido y el SHA-256 de un pequeño archivo de muestra, por ejemplo `/home/lab/recovery-b.txt`.
- Conserve el punto B y su cadena en el remoto. Asegúrese de que su ordenador tenga espacio para el archivo comprimido.
- Utilice una cuenta de administrador y compruebe que **File Restore** exista en su instalación.
- Para esta primera prueba, evite VM de producción, datos privados, volúmenes cifrados o RAID, enlaces simbólicos y carpetas. Esta prueba no demuestra compatibilidad con todos los sistemas de archivos, disposiciones LVM o remotos.

1. Abra **Backup → File Restore** (`/#/backup/file-restore`). Localice la VM de prueba y abra su acción de restauración de archivos. No pulse los botones de eliminación contiguos. Si falta la VM o el punto, actualice y compruebe que `lab-delta-nfs` esté habilitado. No cambie a la copia completa anterior.
2. Elija el **punto B** por su hora y trabajo y después el disco. Espere al análisis de particiones y elija la que contiene la muestra. Un disco sin tabla de particiones puede mostrar directamente su sistema de archivos. Si falla el análisis, deténgase: no monte ni edite manualmente los archivos de copia.
3. Navegue desde `/` hasta el archivo de muestra y seleccione **solo ese archivo**. No utilice los controles de selección de carpeta o de todo. Compruebe la ruta y conserve el formato **tgz** (predeterminado; **zip** también funciona, pero puede ser más lento). Inicie la descarga y espere a que el navegador termine. Una ventana emergente bloqueada o una descarga incompleta no es un éxito.
4. En su ordenador, anote el nombre, el tamaño y el SHA-256 del archivo comprimido. Enumere su contenido, extraiga solo la muestra en una carpeta nueva y vacía y compare su contenido y SHA-256 con la versión B. Trate las rutas del archivo como no fiables y nunca extraiga sobre datos en uso. No modifique la VM original, el punto B ni la programación.

**Comprobación:** el archivo comprimido se abre, contiene solo el archivo de muestra y este coincide con la suma B. Que coincida el nombre, o que el contenido corresponda a la versión C, no es una coincidencia válida.

Si falla un paso, guarde las pruebas y detén las siguientes ejecuciones de copia hasta que su responsable las haya revisado. No elimine archivos de la cadena, instantáneas de origen ni archivos parciales para hacer aparecer un punto. Copiar el archivo recuperado de vuelta al invitado es una tarea aparte que requiere la aprobación de su propietario.

## Copiar una VM a otro pool (réplica DR) {#dr-replica}

**Disaster Recovery** (DR) copia una VM completa a un SR de otro pool. Es diferente de una copia en NFS y de **Continuous Replication** (CR), que solo envía los cambios. La copia, llamada réplica, permanece detenida y con el arranque bloqueado. **No desbloquee ni arranque la réplica.** Para utilizarla, debe clonarla. Esta prueba comprueba uno de esos clones en un lugar aislado. No prueba la conmutación automática, la pérdida del pool de origen ni el retorno al origen (failback).

**Antes de empezar**

- Utilice una VM de prueba en el pool A y un segundo pool de prueba B administrado por el mismo dispositivo virtual XOA-HL.
- Pida al propietario del pool B un SR dedicado con escritura, `lab-dr-sr`, con espacio para dos copias completas y un clon. Debe estar en un almacenamiento diferente del pool A y no debe ser una biblioteca ISO. Anote los UUID de ambos pools y SR, el espacio libre y qué hosts pueden acceder al SR.
- Conserve la copia NFS independiente del tutorial.
- Utilice una VM de un solo disco sin discos compartidos o de acceso directo. Antes de cada ejecución, escriba una muestra (A, después B y después C), anote su SHA-256 y apague el invitado normalmente.
- Planifique el acceso a consola y un lugar en el pool B **sin red de producción**. Eliminará todas las NIC del clon antes de arrancarlo.
- Si DR o el SR de destino no están disponibles en su instalación, deténgase.

1. Abra **Backup → New → VMs** (`/#/backup/new/vms`) y cree el trabajo `lab-dr-full`. Seleccione únicamente la VM de prueba y deje desactivada la selección inteligente. Seleccione solo **Disaster Recovery**; deje **Backup**, **Delta Backup**, **Continuous Replication** y **Rolling Snapshot** desactivados. En **Target SRs (for replication)**, seleccione únicamente `lab-dr-sr`. Deje **Delete first** desactivado para no eliminar réplicas antiguas antes de la transferencia. No edite los demás trabajos.
2. Añada una programación con **Replication retention** `2`, una zona horaria explícita y una vista previa comprobada. No utilice la retención de instantáneas ni las comprobaciones de estado. Deshabilite la programación y guarde. Vuelva a abrir el trabajo y compruebe la VM, el SR de destino, el modo, la retención, el estado deshabilitado y los identificadores.
3. Con la muestra A escrita y el invitado apagado, ejecute el trabajo una vez desde **Backup → Overview**. Compruebe todas las tareas y advertencias. En el pool B, localice la nueva réplica **detenida** por su UUID, el trabajo y la hora de su nombre, su etiqueta **Disaster Recovery** y su disco. No la arranque.
4. Repita con la muestra B y después con C, completando una ejecución antes de la siguiente. Anote los identificadores de ejecución y réplica, las horas, los discos y los errores. Después de la tercera ejecución, compruebe qué réplicas permanecen: normalmente B y C. Un trabajo en verde no demuestra que los datos sean correctos, y una eliminación fallida no se revierte.
5. Seleccione la **réplica B**, no la VM de origen, la réplica C ni un punto NFS. Haga un **Fast clone** con un nombre exclusivo en el pool B y deje la réplica detenida. Anote los nuevos identificadores de VM y discos del clon y compruebe que esté detenido y sin bloqueo de arranque. Si falla la clonación o el clon está bloqueado, deténgase; no omita el bloqueo.
6. Elimine **todas** las NIC del clon detenido y compruebe que su lista de red esté vacía. Arranque únicamente el clon, abra su consola y compare la muestra con la suma B. Apáguelo normalmente. Puede probar un clon de C del mismo modo.
7. Conserve las réplicas B y C y la copia NFS. Elimine únicamente los clones de prueba con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/).

**Comprobación:** tres ejecuciones completas llegaron al pool y SR correctos; permanecen B y C, o puede explicar por qué no; el clon aislado de B tiene sus propios identificadores, no tenía NIC al arrancar y contiene exactamente la muestra B.

Si falla una transferencia, una comprobación de espacio, una eliminación, una clonación o una comprobación de datos, detén las siguientes ejecuciones y entregue el inventario a los responsables de las copias y del almacenamiento. Nunca retire el bloqueo de arranque de una réplica, elimine un punto solo por su nombre ni elimine una instantánea gestionada por el trabajo de copia.

No se abordan aquí: cadenas CR, ejecuciones programadas, cambio de red, prevención de la ejecución simultánea de la misma VM, retorno al origen y cortes reales.

## Probar una copia SMB en Windows Server {#smb-remote}

Pruebe un remoto SMB con una copia completa y una restauración aislada. La interfaz de XO advierte de que los remotos SMB están destinados a **Windows Server** y recomienda NFS para Samba en Linux y la mayoría de los dispositivos NAS. Esta prueba no cubre otros servidores SMB, almacenamiento SMB para ISO o discos de VM, remotos en la nube ni uso en producción. XO monta el recurso compartido con CIFS y el paquete XOA-HL incluye `cifs-utils`, pero todavía no se ha comprobado el montaje en un dispositivo virtual real.

**Antes de empezar**

- Pida al administrador de Windows Server un **recurso compartido dedicado a pruebas**, en un almacenamiento diferente del de la VM de origen y el dispositivo virtual, con espacio suficiente para la copia y la prueba de restauración.
- Solicite una cuenta dedicada que pueda crear, leer y eliminar archivos en ese recurso, con acceso por red únicamente desde el dispositivo virtual. Obtenga el nombre del servidor, el recurso compartido, la subcarpeta opcional, el dominio y las credenciales por un canal seguro.
- Escriba la contraseña únicamente en su campo. XO construye una URL interna del remoto que contiene las credenciales, por lo que debe tratar las exportaciones de configuración de XO como secretos. Nunca comparta esa URL ni incluya credenciales en capturas, incidencias, extractos de registros u opciones de montaje personalizadas.
- Conserve la copia NFS independiente del tutorial. Utilice la misma VM de prueba pequeña, detenida y de un solo disco, con un nuevo archivo de muestra y su suma de comprobación. Reserve un SR con escritura y un lugar con acceso solo por consola para la copia restaurada.

1. En **Settings → Remotes** (`/#/settings/remotes`), cree `lab-backup-smb` de tipo **SMB**. En **Address\\Share**, introduzca el servidor y el recurso compartido separados por una barra invertida. **Subfolder** es una ruta opcional dentro de ese recurso, no una segunda ruta de recurso compartido. Introduzca el usuario dedicado, la contraseña y el dominio (el formulario comienza con `WORKGROUP`; utilice el valor del administrador). Conserve los valores predeterminados de **Custom mount options**, proxy y cifrado. Guarde y compruebe el identificador del remoto, su estado habilitado, tipo, servidor, recurso, subcarpeta e indicador de error. La contraseña permanece oculta: no intente leerla de la URL mostrada.
2. Ejecute **Test your remote** en este remoto. Escriba un archivo aleatorio de 10 MiB, lo vuelve a leer, lo compara e intenta eliminarlo. Compruebe el icono de éxito, el resultado y cualquier paso fallido. Si falló un paso, pida al administrador que busque un archivo `.test` residual por su nombre exacto. Una prueba correcta solo demuestra este recorrido de escritura y lectura, no una restauración de VM ni una velocidad sostenida.
3. En **Backup → New → VMs** (`/#/backup/new/vms`), cree un trabajo independiente llamado `lab-smb-full`: únicamente la VM de prueba detenida, solo modo **Backup** (completo), `lab-backup-smb` como único remoto de destino y **Delete first** desactivado. Añada una programación con zona horaria explícita y **Backup retention** `2`, manténgala deshabilitada, guarde y compruebe los identificadores. No cambie el trabajo NFS.
4. Ejecute manualmente la programación deshabilitada una vez desde **Backup → Overview**. Compruebe la exportación de la VM y el resultado del remoto en el registro; después localice el punto completo de `lab-backup-smb` en **Backup → Restore**. Anote las horas, los identificadores, el tamaño y cualquier error de montaje SMB, inicio de sesión o espacio. Una instantánea abandonada en el SR de origen o una prueba de remoto correcta no es una copia de seguridad de VM.
5. Restaure ese punto en el SR reservado con **Start VM after restore** desactivado. Anote los nuevos UUID de VM y discos. Con la copia detenida, elimine **todas las NIC** y compruebe que la lista de red esté vacía. Arranque únicamente esta copia desde **Console**, compare la suma de la muestra y apáguela. Conserve la VM original, la copia NFS y el punto SMB hasta registrar el resultado. Después elimine únicamente la copia de prueba con el [procedimiento de eliminación de VM](/docs/xoa-hl/vm-operations/).

**Comprobación:** la prueba del remoto tiene éxito, la copia completa llega al recurso compartido y la copia aislada arranca sin NIC y con los datos correctos.

Si fallan el acceso, la escritura, la lectura, la eliminación, la exportación o la restauración, deténgase. Entregue a los responsables de las copias y del servidor los errores (sin credenciales), los identificadores exactos, el contenido del recurso y las VM parciales. Nunca vuelva a intentarlo contra un recurso de producción ni elimine rutas de copia solo por su nombre.

No se abordan aquí: rotación de contraseñas, cortes del recurso compartido, retención durante muchas ejecuciones, confianza de dominio, versiones SMB y ajustes de seguridad, velocidad y otros servidores SMB.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| Falla la prueba NFS | Compruebe que el dispositivo virtual pueda acceder al servidor y revise la ruta de exportación, los permisos y las opciones de montaje. Que su navegador llegue al NAS no basta. |
| Falla la copia o no aparece un punto de restauración | Lea los registros de la VM y de exportación. Compruebe el acceso al remoto y su espacio libre, el espacio libre del SR de la VM y la VM seleccionada. Una instantánea residual no es una copia de seguridad. |
| Falta el punto de restauración | Compruebe que el remoto esté habilitado y sin errores, actualice la lista y compruebe que el trabajo realmente exportó esta VM. |
| Falla la restauración | Lea su registro y compruebe que se pueda leer el remoto, que el SR de destino tenga espacio y que el host pueda acceder a él. Busque una VM parcial antes de repetirlo. Nunca elimine solo por el nombre. |
| Falla la réplica DR o su clon | Anote los identificadores de ejecución, VM y discos, el espacio y el acceso del SR de destino y el estado de bloqueo. Mantenga las réplicas detenidas. No omita su bloqueo de arranque ni vuelva a ejecutar la retención a ciegas. |
| Falla el remoto SMB o su restauración | Con el responsable de Windows Server, compruebe el paso fallido de la prueba, los registros de trabajo y restauración, el servidor y recurso compartido, el acceso de la cuenta, el espacio libre y los objetos parciales. Conserve la copia NFS independiente. Nunca pegue credenciales en un informe. |
| La VM restaurada no tiene red | Es lo esperado: eliminó todas las NIC para esta prueba exclusivamente por consola. Conectarla a una red de producción requiere revisar por separado su dirección IP y las identidades de los servicios. |
| El archivo difiere o el invitado no arranca | Compruebe que seleccionó el punto de restauración correcto y que el archivo se escribió antes de la copia. Conserve los registros y la copia. La prueba no se ha superado. |

Para los estados de ejecución, las exportaciones parciales y un nuevo intento seguro, consulte [Diagnosticar una copia de seguridad fallida](/docs/xoa-hl/troubleshooting/#backup-failures).

## Siguientes pasos {#next-steps}

Tras una prueba de restauración correcta, decida la frecuencia real de las copias, la retención, la supervisión de capacidad y cómo garantizar la coherencia de las copias para sus aplicaciones. Habilite una programación solo después de comprobar su zona horaria y las próximas ejecuciones. Consulte también la [guía de actualización](/docs/guides/updates/) y el [glosario](/docs/xoa-hl/glossary/). La recuperación de configuración y Continuous Replication necesitan sus propios procedimientos.

{{< details title="Fuentes" closed="true" >}}
- **Programaciones**: [editor, tabla y orden de guardado de programaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [selector de hora y formato de vista previa](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [API, inicio y parada de programaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [comportamiento de tareas cron](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [protección de trabajo en curso e identidad del registro](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs), [retención de copias completas y orden de limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).
- **Copia de seguridad y restauración**: [rutas de copia y acceso de administrador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [formulario de remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [prueba de remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [modos de trabajo y guardado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [programación y retención](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [ejecución manual](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [controles de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [eliminación de NIC](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [versión fijada del proyecto original](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [selección de parches y compilación](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Copias incrementales**: [exportación incremental y selección de base](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs), [transferencia al remoto y retención](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs), [retención de instantáneas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs), [ejecución de limpieza y combinación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs), [lector de cadena de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [implementación de restauración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/ImportVmBackup.mjs), [tipo de exportación en los registros](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js).
- **Recuperación de un archivo**: [interfaz de restauración de archivos y filtro delta](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/index.js), [selector de copia, disco, partición y archivo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/restore-file-modal.js), [API de archivos para administradores y respuesta de archivo comprimido](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/backup-ng.mjs), [partición de solo lectura y adaptador tgz/zip](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [descarga del navegador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **Réplica DR**: [modo del trabajo, SR de destino y programación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [control de retención de replicación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [exportación completa y escritor de SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/FullXapi.mjs), [importación de réplica, bloqueo de arranque y limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullXapiWriter.mjs), [filtro de identidad de réplica](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_listReplicatedVms.mjs), [API de clonación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Remoto SMB**: [formulario de remoto y advertencia de Windows Server](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [analizador y formateador SMB](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-remote-parser/src/index.js), [gestor CIFS](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/smb.js), [opciones de montaje y de remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/_mount.js), [prueba de remoto de 10 MiB](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/abstract.js), [ciclo de vida del remoto](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/remotes.mjs), [dependencia de ejecución de XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **Incidencia conocida**: [encabezados de resultados de prueba de remoto (xoa-hl#38)](https://github.com/Vagrantin/xoa-hl/issues/38).
{{< /details >}}
## Política de producción, ejecuciones perdidas y simulacros de fallo {#backup-policy}

Se aplica a: Xen Orchestra 5.113.2 (`e281c536`) en XOA-HL ce40 y ce47. La pequeña prueba NFS no certifica una política de copia de seguridad de producción. Antes de habilitar un trabajo de producción, acuerde un responsable, la pérdida máxima de datos aceptable (RPO), el tiempo de recuperación (RTO), la consistencia de las aplicaciones, las copias independientes o externas, la retención, la capacidad y la escalada de alertas.

1. Use un trabajo NFS desechable aparte y un invitado pequeño. Conserve la copia independiente que sabe que es buena. Anote la selección de VM, los ID del remoto y de la programación, la zona horaria explícita, la expresión cron, el estado de habilitación, la retención y **Delete first** desactivado. Planifique la capacidad para la instantánea de origen, la nueva copia y los puntos retenidos, incluida la fusión de deltas. Pruebe a restaurar el punto retenido más antiguo y el más reciente; un trabajo en verde no basta para cumplir un RTO.
2. Elija UTC si la ambigüedad del horario de verano no es aceptable. El programador inicia los trabajos según cron y la zona horaria; este mixin no guarda ninguna cola para reproducir ejecuciones perdidas. No suponga que una interrupción se recupera después. En un dispositivo virtual desechable, anote un minuto programado, detén el servicio durante ese minuto, reinícialo y revise los registros y los puntos antes de lanzar manualmente una única ejecución de sustitución, tras comprobar que no hay ningún trabajo activo.
3. Con una zona horaria local que tenga horario de verano, revise las próximas horas de disparo alrededor de ambos cambios y anote los desfases UTC. Una hora de reloj omitida o repetida debe probarse con la implementación cron fijada y una ejecución programada real en el laboratorio antes de aceptar esa política. No cambie el reloj de un dispositivo virtual o host compartido para simular el horario de verano. Hasta verificarlo, use una programación UTC probada o mantenga deshabilitada esa política con horario de verano.
4. Ejecute tres puntos programados correctos con retención 2, compruebe después la depuración por VM, programación y remoto, y restaure cada punto retenido de forma aislada. Mida la duración real de la copia y de la restauración frente al RPO/RTO acordado. Al terminar, deshabilite la programación de prueba y vuelva a leerla.
5. Simule la indisponibilidad del remoto con un remoto de prueba aparte y no válido, no con el remoto que funciona; compruebe el fallo en las subtareas de VM, exportación y remoto, que no se anuncia ningún punto utilizable y que se conservan los puntos buenos conocidos. Corrija solo el remoto de prueba, pruébelo y después ejecute una sustitución supervisada y restáurela.
6. Pruebe un trabajo aparte con una selección de VM deliberadamente no válida o un destino de prueba inaccesible, y una restauración aislada en un almacenamiento desechable insuficiente solo si el responsable del laboratorio lo ha proporcionado. Anote los errores, las VM y discos de destino parciales, las instantáneas de origen y el espacio restante. No llene un SR compartido, no rompa la gestión del host, no trunque una cadena de copias ni interrumpa trabajos de otras personas.
7. Si hay alertas configuradas, provoque un fallo controlado y compruebe la entrega real al destinatario acordado y la escalada. Una entrada de registro no prueba el envío por correo o webhook. El destinatario y la disponibilidad del servicio necesitan su propia autorización y recursos de laboratorio.

**Fallo:** deshabilita la programación de prueba afectada, conserve los registros por VM y subtarea y las marcas de tiempo UTC, inspecciona los puntos parciales y el estado del origen, y resuelva los problemas de capacidad, credenciales o conectividad antes de reintentar. Nunca borre carpetas de copias por su nombre, no active **Delete first** para ocultar un problema de espacio y no dé por recuperada una ejecución fallida o perdida hasta que una restauración aislada sea correcta. La aceptación en producción, los cambios reales de horario de verano y los servicios de alerta no disponibles siguen pendientes hasta observarlos.

Implementación fijada: [packages/xo-server/src/xo-mixins/scheduling.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [@xen-orchestra/cron/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [packages/xo-web/src/xo-app/backup/new/schedules.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/schedules.js), [@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [packages/xo-web/src/xo-app/logs/backup-ng/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js).

**Resultado de laboratorio, 3 de noviembre de 2026 (parcial):** Con un remoto local en el dispositivo virtual y un trabajo de copia completa (retención 3, una ejecución por minuto), había tres puntos tras la tercera ejecución y siguieron siendo tres. Restaurar el punto más antiguo y el más reciente dio VM detenidas cuyos discos sin procesar coincidían con el origen; ese disco de origen estaba vacío, así que esto solo prueba el tamaño y la restauración. Con `xo-server` detenido durante dos minutos programados y luego iniciado, no hubo ejecuciones de recuperación y el siguiente punto llegó en el minuto siguiente: las ejecuciones perdidas no se reproducen. Detener el servicio tardó unos 90 segundos y dejó la unidad en estado `failed`. Un directorio de remoto local que falta se vuelve a crear sin aviso: el trabajo y `remote.test` tuvieron éxito y los puntos anteriores quedaron en el directorio antiguo. Una ruta de remoto situada bajo un archivo normal falló en `get remote adapter` con `ENOTDIR`, y los puntos del remoto correcto no se vieron afectados. No se probaron el horario de verano, la entrega de alertas ni la política de producción, así que este caso aún no está probado por completo.
