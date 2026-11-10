---
title: "Administrar VM: consola, instantáneas, copias, memoria y eliminación"
linkTitle: "Administrar VM"
description: "Use la consola, arranque y detenga VM, cree instantáneas, copie, cambie recursos y elimine VM."
weight: 40
translationKey: xoa-manual-vm-operations
translationStatus: reviewed
sourceRevision: sha256:8b4bb1976ace6e6ecdb9f020d03a69d61f3233f9989145281bbf60a598155abf
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Tareas habituales de VM: usar la consola, arrancar y detener, crear y revertir instantáneas, clonar y copiar, cambiar CPU y memoria y eliminar. Practique cada tarea con una VM de prueba sin datos de producción, conectado al **appliance XOA-HL** como administrador. Antes de cambiar una VM importante, asegúrese de tener una [copia de seguridad independiente y una restauración probada](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio. Las versiones posteriores pueden diferir.
{{< /callout >}}

**Observaciones D3:** el 28 de octubre de 2026, XOA-HL `v5.113.2_e281c536-ce47` (`ca44911`) en un host anidado XCP-HL v8.3-ce44. Las pruebas usaron clones desechables de un invitado con controladores PV pero sin agente de administración. El [registro de laboratorio](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6459388202) cubre las observaciones siguientes sobre energía, instantánea y reversión en estado detenido, clon rápido, discos, cambio de tamaño y eliminación. Los demás procedimientos siguen basándose en la revisión del código fuente. Los resultados D3 posteriores sobre instantáneas y protección se enlazan más abajo. No se probaron las instantáneas de memoria, los discos compartidos ni los fallos de limpieza.

## Use la consola de la VM {#vm-console}

La consola muestra la pantalla de la VM en el navegador. Necesita permiso para **operar** la VM: Viewer no basta. El invitado no necesita IP para la consola, pero su navegador debe alcanzar el appliance y este al host. Mantenga el aislamiento de red de la VM de prueba.

1. Abra **Console** de la VM (`/#/vms/<id>/console`). Compruebe identidad y estado **Running**. Para cualquier otro estado, incluidos pausado o suspendido, aparece **Console is only available for running VMs.** Arranque mediante una [operación de alimentación](#vm-power) planificada; nunca fuerce un reinicio solo para obtener consola.
2. Espere la pantalla prevista, como acceso, instalador o aplicación conocida. Las credenciales introducidas pertenecen al invitado, no a XOA-HL ni al host.
3. Lleve el puntero al área de consola para enviar teclado y ratón al invitado. Sáquelo para recuperarlos junto con los atajos XO. Para probar entrada, escriba una cadena inocua como `console-test` en un editor del invitado y bórrela. Nunca pruebe en un comando de shell ni campo de contraseña. Ver la pantalla no demuestra que funcione la entrada.
4. En pantalla grande, el zoom comienza en **100%**. Cambia la visualización del navegador, no la resolución del invitado, y puede ocultarse en pantallas pequeñas. **Hide info** y **Show info** solo ocultan/muestran la cabecera XO; no detienen el invitado ni pasan a pantalla completa.
5. Al terminar, salga de la pestaña. Cierra la conexión de consola sin detener el invitado. Si la VM se reinició mientras estaba conectado, reabra la pestaña para obtener una pantalla nueva. XO puede no detectar la desconexión tras reiniciar; los reintentos automáticos no demuestran buena salud del invitado.

**Comprobación:** ve el invitado correcto en ejecución, recibe el texto de prueba, los controles XO vuelven a funcionar al sacar el puntero y la VM conserva el estado esperado.

### Portapapeles y botones de cliente remoto {#clipboard-and-remote-client-buttons}

- El cuadro de texto del portapapeles envía su contenido al portapapeles del invitado tras una pausa breve. **Copy** copia el texto al portapapeles de su propio equipo. El botón multilínea abre **Send to clipboard**. Pruebe con texto inocuo y compruebe el pegado dentro del invitado por separado. Nunca coloque contraseñas ni datos privados en el cuadro o las capturas.
- **SSH**, **SSH as…** y **RDP** abren el controlador `ssh://` o `rdp://` de su equipo con la IP comunicada por el invitado. Aparecen cuando se comunica una IP. No demuestra cliente instalado, servicio activo ni permiso de red. No reparan ni sustituyen la consola.
- **Ctrl+Alt+Del** pide confirmación y envía esa combinación al invitado. Según el SO puede reiniciarlo. Cancele en esta prueba; no es una prueba de conexión. El selector ISO cambia el medio montado: consulte [Crear su primera VM](/docs/xoa-hl/create-vm/) antes de modificarlo.

### Corrija una consola vacía o sin respuesta {#fix-a-blank-or-unresponsive-console}

1. **La VM no está en ejecución o la consola está desactivada.** Lea primero estado y mensaje. Una VM activa con `disable_pv_vnc=1` muestra **Console is disabled for this VM**. Consulte al responsable antes de cambiarlo. Instalar herramientas o reiniciar no reactiva la consola.
2. **La conexión no se abre o se corta continuamente.** Compruebe permiso de operar y conexión sana al host. En herramientas de desarrollo del navegador, encuentre la solicitud WebSocket terminada en `/api/consoles/<id>` y anote error/estado. Un proxy inverso debe permitir actualizaciones WebSocket, no solo páginas normales. Compruebe navegador-appliance (incluido TLS) por separado de appliance-host. IP, SSH y cortafuegos del invitado no forman parte de esta vía. Resuélvalo con su responsable. Nunca exponga un puerto VNC públicamente ni desactive comprobaciones de certificado como arreglo rápido.
3. **Se abre pero la pantalla está vacía o congelada.** Compruebe VM correcta, pantalla prevista y operaciones recientes. Reabra la pestaña tras reiniciar. La pantalla vacía puede venir del invitado o conexión: guarde lo observado antes de un arreglo específico del SO. No reinicie repetidamente, reinstale ni cambie medios de arranque solo por una pantalla negra.
4. **La pantalla funciona pero no teclado o portapapeles.** Saque y vuelva a meter el puntero y repita la prueba del editor. Compruebe si navegador/SO interceptan teclas y si el invitado admite el portapapeles. Trate SSH/RDP por separado. En el [informe](/docs/xoa-hl/troubleshooting/#report-a-problem), incluya navegador/versión, ID de VM/host, hora, estado, mensaje exacto y errores sin datos privados. Mantenga trazas brutas privadas: cookies, tokens, texto y pantallas pueden ser sensibles.

## Arranque, detenga y reinicie una VM {#vm-power}

Abra primero la pestaña **General** de la VM (`/#/vms/<id>/general`) y compruebe si se detecta un agente de administración. Sin él, XO no puede apagar limpiamente el invitado ni reiniciarlo. Consulte [el estado y la instalación de las herramientas de invitado](/docs/xoa-hl/guest-tools/#guest-tools-status).

Con el único invitado sin agente de administración de la ejecución D3, una detención limpia esperó 1200 segundos y luego falló con `VM_SHUTDOWN_TIMEOUT`. La VM siguió en **Running**. El reinicio se rechazó de inmediato con "VM lacks feature". Una detención forzada pasó la VM a **Halted** en segundos.

Si la VM está detenida, seleccione **Start** y compruebe el estado y la consola. Antes de una detención o un reinicio limpios, instale las herramientas del invitado y compruebe el agente, o apague el invitado desde dentro. Use una detención forzada solo cuando el invitado no pueda apagarse. Equivale a desenchufar la alimentación y puede perder datos.

Lea cualquier confirmación antes de continuar. No pulse de nuevo con una tarea en curso. Después, compruebe el estado de la VM, la consola y la aplicación. Un mensaje de éxito no demuestra que la aplicación esté sana.

## ¿Instantánea, clon, copia o copia de seguridad? {#protection-types}

| Opción | Qué ofrece y su límite |
| --- | --- |
| Instantánea | VM en un momento concreto, guardada con sus discos. No es copia independiente |
| Clon rápido | Otra VM que comparte almacenamiento con el original. No protege si se pierde ese almacenamiento |
| Copia completa | Otra VM con discos copiados en el SR elegido. Compruebe datos, ubicación y aislamiento antes de usarla |
| Copia de seguridad | Copia de recuperación separada. Demuéstrelo con una restauración aislada |

Instantáneas y clones usan más almacenamiento al cambiar las VM. Compruebe espacio libre del SR y elimine solo objetos de prueba identificados. Una instantánea de una VM activa no garantiza coherencia de sus aplicaciones.

## Cree una instantánea de una VM detenida <span class="hx:absolute" id="3-take-and-check-a-stopped-snapshot"></span> {#stopped-snapshot}

Use una VM de prueba con discos normales (sin compartidos ni paso directo) y consola funcional. Pause sus programaciones de copia y réplica y espere las tareas activas. Conserve una copia independiente de los datos necesarios. No se cubren instantáneas de VM activas, memoria ni coherencia de aplicaciones.

1. En el invitado, cree un archivo inocuo con `snapshot-A` y anote su suma. Apague limpiamente y compruebe **Halted**.
2. Anote UUID de VM, cada VDI con ID, SR y tamaño, UUID de instantáneas existentes y espacio libre. [Quite todas las VIF](/docs/xoa-hl/storage-networks/) y compruebe lista vacía. A partir de ahora use la consola.
3. Compruebe nombres de disco. Un nombre con `[NOSNAP]` puede excluirse de instantáneas; es parte del nombre, no una etiqueta de VM. Discos excluidos, compartidos o de paso directo requieren otro procedimiento. No renombre para eludir políticas. Prevea espacio para instantánea, escrituras futuras y la instantánea adicional previa a revertir.
4. Abra **Snapshots** (`/#/vms/<id>/snapshots`) y pulse **New snapshot** una vez. La crea inmediatamente sin pedir nombre. El predeterminado es nombre de VM más fecha/hora. No use **New snapshot with memory**.
5. Espere y actualice. Encuentre la fila nueva por **Creation date** y copie UUID con su botón. Anótelo: nombre u hora no bastan.
6. Establezca **Name** `lab-snapshot-A` y una nota breve en **Description**. Actualice y compruebe ambos. Compare discos y SR con sus notas y compruebe errores/espacio. Los ID de discos de la instantánea son nuevos: compare cobertura y tamaños, no ID.

**Comprobación:** una instantánea identificada cubre los discos previstos y la VM original está detenida sin VIF.

Si falla crear o renombrar, guarde error y listas reales de VM, instantáneas y discos antes de repetir. Un ID o aviso ausente no demuestra que no se creara nada; fallar al renombrar no deshace la instantánea.

## Revierta a una instantánea <span class="hx:absolute" id="4-revert-only-the-test-vm"></span> {#snapshot-revert}

En D3, se tomó una instantánea mientras la VM de prueba estaba **Halted**. Un disco añadido después había desaparecido tras revertir. La VM siguió **Halted** y la instantánea se conservó. Esto no demuestra la coherencia de los archivos del invitado ni de las aplicaciones.

En la [segunda prueba de instantáneas](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6460786269), se tomó una instantánea solo de disco mientras la VM estaba **Running**. Revertirla sobre la VM detenida devolvió la VM al estado **Running**. Compruebe la VM y su aislamiento de red antes de revertir: una instantánea puede restaurar su estado de energía registrado. No se probó una instantánea con memoria (suspensión).

{{< callout type="warning" >}}
Revertir sustituye el estado actual, incluidos ajustes que pueden recuperar interfaces antiguas. Pueden perderse cambios posteriores. Una instantánea tomada con la VM en ejecución puede arrancar esa VM al revertir, aunque el objeto de la instantánea solo de disco aparezca como Halted. Compruebe el aislamiento de red de la VM antes de confirmar la reversión; no se fíe del estado de energía del objeto de la instantánea. El ejercicio siguiente usa solo esta VM aislada y una instantánea tomada con la VM detenida. Compruebe de nuevo sus VIF antes de arrancarla. Una instantánea en el mismo SR no protege si se pierde el SR.
{{< /callout >}}

1. Arranque la VM aislada, cambie el archivo a `snapshot-B` y anote suma nueva. Apague limpiamente y confirme **Halted**. Anote discos, VIF e instantáneas actuales.
2. Compruebe mediante UUID que usará `lab-snapshot-A` de la sección anterior. No debe ser una instantánea de tarea de copia ni de otra VM.
3. En **Snapshots**, elija **Revert VM to this snapshot** en esa fila y lea **Revert your VM**. Deje **Snapshot before** marcado y compruebe espacio primero. Esta opción predeterminada guarda el estado actual como otra instantánea previa. No es copia independiente ni garantiza reversión. Cancele ante dudas de VM, aislamiento o espacio.
4. Confirme una vez y espere. Actualice y anote UUID revertido, UUID de la nueva instantánea previa, estado, discos, VIF y errores. Si falla la instantánea previa, XO no solicita revertir. Si falla después la reversión, la previa puede permanecer. Compruebe estado real antes de repetir y no desmarque **Snapshot before** para eludir un error inexplicado.
5. Antes de arrancar, compruebe **Halted** y lista VIF vacía. Si volvió alguna, quítela detenida. Una instantánea de VM activa puede hacer que arranque o reanude sola al revertir; no se cubre aquí.
6. Arranque y abra consola. Compruebe `snapshot-A`, suma original, discos y aplicación. Apague y anote resultado. La instantánea adicional previa conserva `snapshot-B`. Recuperarla es otra restauración controlada, no un botón de deshacer.

### Elimine una instantánea de prueba {#snapshot-cleanup}

Tras anotar resultado y guardar las copias independientes necesarias, mantenga la VM detenida. Elimine solo una instantánea de prueba con UUID y propietario anotados.

1. En **Snapshots**, elija **Remove this snapshot** en su fila. Lea **Delete snapshot** y confirme solo una. No use **Remove selected snapshots**, no borre instantáneas creadas por copias ni confunda con **Remove** de la VM.
2. Espere y actualice instantáneas, discos y espacio libre. Compruebe que desapareció, siguen presentes VM e instantáneas conservadas y no hay error.

La limpieza de discos puede registrar errores sin fallar toda la eliminación. Una fila desaparecida o mensaje exitoso no demuestra limpieza terminada ni espacio liberado al instante. Anote ID restantes y [comunique restos inexplicados](/docs/xoa-hl/troubleshooting/). Nunca elimine en masa discos aparentemente huérfanos. Una instantánea eliminada no es recuperable.

## Cree un clon rápido aislado {#fast-clone}

En D3, la VM detenida produjo un clon rápido con identidad propia, un disco y una NIC heredada. El clon arrancó después de quitar esa NIC. En esta ejecución no consta ningún resultado de un clon en ejecución ni de una copia completa.

1. En una VM detenida de prueba, seleccione **Fast clone**. Encuentre la nueva VM (su nombre predeterminado termina en `_clone`), anote ID y renómbrela.
2. Manténgala detenida mientras [quita todas las interfaces heredadas](/docs/xoa-hl/storage-networks/) o establece aislamiento externo comprobado. Una MAC nueva no cambia IP, credenciales ni identidades de aplicaciones copiadas.
3. Arranque el clon y compruebe consola. Reconecte red solo tras resolver identidades duplicadas y comprobar aislamiento.

Si no aparece tras un error, compruebe inventario y tareas antes de repetir. Esto no prueba migración en vivo, instantáneas de memoria ni recuperación tras perder un SR.

### Cree una copia completa en el mismo pool {#full-copy}

Use **Copy**, no la acción separada **Fast clone**, para copias normales de discos en el SR elegido. El diálogo también ofrece **Fast clone**; mantenga **Full copy**. Ni clon rápido ni copia completa en el mismo pool son copia independiente ni recuperación ante desastres probada.

1. Use una VM con discos normales, sin compartidos ni paso directo. Anote archivo inocuo y suma dentro del invitado. Apague limpiamente y compruebe **Halted**. Anote ID VM, ID/SR/tamaño de cada disco, VIF e instantáneas. Su historial no forma parte de la prueba.
2. Encuentre otro **SR de discos VM con escritura en el mismo pool**. Compruebe ID, espacio y acceso desde el host de la copia. No puede usarse biblioteca ISO. Prevea copias y crecimiento: el diálogo no reserva ni comprueba espacio. Si falta SR destino, resuelva acceso antes de empezar.
3. En el origen, seleccione **Copy**. En **Copy VM**, establezca **Name** único como `lab-vm-full-copy`. El predeterminado es `{name}_COPY`; vacío conserva el nombre original. Compruebe **Full copy**.
4. En **Select SR**, elija por ID y pool anotados, no por nombre similar. Pueden aparecer otros pools: elegir uno cambia a exportación/importación, fuera de esta prueba. Deje **Compression** en **Disabled**: dentro de un pool no se comprime.
5. Confirme una vez y espere. Actualice y encuentre la VM por ID propio y nombre elegido. Compruebe **Halted**, número de discos, tamaños, ID nuevos y SR de cada disco. Compruebe origen y sus discos intactos. Si la nueva está activa o algo difiere, deténgase y restablezca aislamiento antes de seguir.
6. Manténgala detenida mientras [quita todas las VIF heredadas](/docs/xoa-hl/storage-networks/) y compruebe lista vacía antes del primer arranque. No confíe en MAC nuevas: se copian IP, credenciales e identidades de aplicaciones.
7. Arranque solo la copia aislada, abra consola y compruebe suma, discos y aplicación. Resuelva identidades duplicadas antes de conectar red y mantenga el original aislado o detenido durante las comprobaciones.
8. Apague la copia. Anote resultado y use [Eliminar una VM de prueba](#delete-vm) para quitar solo copia y discos. Conserve origen y copias independientes.

Ante error, desconexión o solicitud interrumpida, guarde tarea, error y listas de VM/discos/instantáneas en ambos lados antes de repetir. Una copia incompleta no revierte automáticamente y un ID ausente no demuestra que no se creara nada. Compruebe espacio y acceso al SR, coincida ID exactos y [comunique restos inexplicados](/docs/xoa-hl/troubleshooting/). Nunca repita a ciegas ni elimine discos huérfanos en masa.

No se cubren copias de VM activas o suspendidas, a otro pool, de plantillas, discos compartidos o de paso directo, historial de instantáneas ni recuperación tras perder un SR.

## Cambie CPU y memoria {#resize-vm}

Los límites del host se comprueban al arrancar la VM, no al guardar el valor. En el único host D3, guardar 64 vCPU y 1 TiB de memoria en una VM detenida funcionó. Al arrancarla después falló con "no hosts available" y siguió **Halted**. Arranque siempre la VM tras una edición. Si no arranca, guarde el error y restaure los valores y límites anteriores antes de reintentar. La página puede mostrar valores antiguos durante unos segundos tras guardar; espere y vuelva a cargar para confirmarlos. En D3, el inventario se actualizó tras unos cuatro segundos.

Planifique mantenimiento y use un invitado de prueba con consola accesible. Antes de cambiar, anote ID, estado, CPU/memoria actuales y límites. Compruebe capacidad de host/pool y necesidades del invitado; esta guía no recomienda número de CPU ni memoria.

{{< callout type="warning" >}}
Apague limpiamente y compruebe primero **Halted**. Si edita una VM activa y el valor no cambia en vivo, XO puede ofrecer reinicio o reinicio forzado. Cancele y apague primero. Elevar un límite no reserva recursos y reducir memoria puede impedir arrancar.
{{< /callout >}}

1. Abra **Advanced** (`/#/vms/<id>/advanced`) y anote **CPU limits** y **Memory limits (min/max)**. La fila CPU muestra valores actual/máximo. Puede editar máximo detenida. Para usar más que el máximo actual, elévelo primero.
2. Abra **General** (`/#/vms/<id>/general`). Pulse número CPU, escriba entero nuevo y **Enter**. Espere, actualice y compruebe antes de otro cambio. También pueden guardar al pulsar fuera: hacerlo no cancela de forma segura.
3. Pulse memoria, establezca cantidad/unidad y **Enter**. Es el **máximo dinámico** configurado, no memoria usada. Según límites existentes, XO actualiza memoria fija o límites dinámicos.
4. Actualice **General** y **Advanced** y anote todos los resultados. CPU no debe superar máximo. Memoria debe mantener: mínimo estático ≤ mínimo dinámico ≤ máximo dinámico ≤ máximo estático. XO puede ajustar límites relacionados: no suponga que solo cambió el campo pulsado.
5. Arranque y compruebe consola, CPU/memoria vistas dentro y aplicación. Si no arranca o valores son erróneos, manténgala detenida, guarde error y reponga ajustes anotados en la misma ventana. Compruebe todos los límites y repita solo al conocer la causa.

Si editar muestra error, compruebe valores reales antes de repetir. Los cambios relacionados no se aplican como una operación indivisible y rechazar uno no demuestra restauración de los antiguos. Tenga a mano [resolución de problemas](/docs/xoa-hl/troubleshooting/) y sus notas.

No se cubren cambios en vivo (hot-plug), memoria dinámica bajo carga ni ajuste de topología CPU.

## Elimine una VM de prueba {#delete-vm}

En D3, eliminar una VM de prueba detenida eliminó esa VM, su instantánea y su disco, sin objetos sobrantes. Por separado, separar un disco vacío lo dejó en el SR elegido; eliminar ese disco lo borró. Separar y eliminar tienen resultados distintos. No se probaron los discos compartidos ni los fallos de limpieza.

En la misma [prueba ce47](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6460786269), la eliminación normal de una VM protegida se rechazó y la VM se conservó, pero una eliminación forzada la borró. La protección contra eliminación es un seguro contra errores, no un control de acceso. Si se rechaza una eliminación protegida, deténgase e investigue; no la fuerce.

{{< callout type="warning" >}}
**Remove** elimina la VM. No equivale a desconectar o separar un disco. En esta versión la confirmación no permite conservar discos: elimina también instantáneas e intenta borrar discos conectados. Si necesita datos o instantáneas, deténgase antes de confirmar y planifique conservarlos. Una instantánea de esta VM no es copia independiente.
{{< /callout >}}

1. Compruebe que es la VM de prueba, no el appliance, invitado original, plantilla u otra con nombre parecido. Anote ID, discos conectados con ID/SR e instantáneas.
2. Compruebe programaciones de copia/réplica y si otra VM usa sus discos. Para datos valiosos, cree primero [copia independiente y pruebe restauración aislada](/docs/xoa-hl/backup-restore/).
3. Apague normalmente y compruebe **Halted**. Eliminar puede detener bruscamente una VM aún activa o suspendida: nunca use **Remove** como apagado.
4. Abra **Advanced** y seleccione **Remove**. Lea aviso sobre VM/discos y confirme solo esta VM. Si XO ofrece después quitarla pese a protección o bloqueo, cancele e investigue el motivo. No apruebe reintento forzado.
5. Espere y actualice listas de VM, instantáneas y discos SR. Compruebe ID anotados, tarea y errores. Se omiten discos compartidos conectados a otra VM, pero eso no protege todos. Los errores de limpieza pueden registrarse sin fallar la eliminación: desaparecer la VM o un mensaje exitoso no demuestran limpieza completa.
6. Compruebe que original, otros invitados y copias independientes siguen funcionando. Revise objetos restantes uno a uno con sus notas y la [guía de discos](/docs/xoa-hl/storage-networks/). Nunca elimine discos huérfanos en masa ni fuerce reintentos para liberar espacio. No hay deshacer: solo una copia de recuperación probada aparte devuelve los datos eliminados.

Si falla parcialmente o cancela una eliminación bloqueada, guarde listas restantes y error. Si existe la VM, compruebe también permisos, reservas IP y pertenencia a conjuntos: XO inicia parte de esta gestión antes de comprobar protección, por lo que un rechazo no demuestra registros intactos. No cree otra con nombre similar suponiendo que sea el mismo objeto. [Comunique el problema](/docs/xoa-hl/troubleshooting/) con versiones e ID (sin datos privados) antes de otra limpieza.

{{< details title="Fuentes" closed="true" >}}
- **Consola**: [pestaña y controles](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-console.js), [captura, escala y reconexión del lienzo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/react-novnc.js), [control de permiso operativo autenticado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [proxy de consola del host](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **Copia completa**: [diálogo Copy, valores predeterminados y patrón de nombre](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/copy-vms-modal/index.js), [solicitudes de copia y clonación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permisos VM/SR y selección por pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [envoltorio XAPI de copia, clonación y copia remota](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [selector de SR con escritura](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Alimentación e instantáneas**: [acciones de alimentación e instantáneas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [barra de acciones VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [pestaña de instantáneas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [confirmación de reversión](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js), [estado de alimentación al revertir](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **CPU, memoria y eliminación**: [controles General](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [límites Advanced y Remove](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [guardado de edición en línea](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [permisos y parámetros API de reinicio y borrado VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [orden de restricciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [valores de destrucción, discos compartidos y limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [etiquetas y avisos de interfaz](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Cobertura y eliminación de instantáneas**: [selección por nombre de disco y limpieza](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs).
{{< /details >}}

## Cambios de CPU y memoria en ejecución (VM03) {#running-resources}

Alcance: XO 5.113.2 en `e281c536`, fuentes de XOA-HL ce40/ce47. Es un procedimiento para un invitado desechable; la aceptación en una instalación y en el invitado se registra por separado.

1. Conserve una copia de seguridad independiente probada. Use un administrador, discos normales, una consola operativa y un invitado compatible con la conexión en caliente de CPU y con balloon. Anote el número de CPU del invitado, la memoria disponible y el estado de la aplicación, el UUID de la VM, las CPU actuales y máximas, los cuatro límites de memoria y la memoria libre del host. No use la sobreasignación del host como prueba.
2. Con la VM detenida, reserve un techo pequeño, por ejemplo 2 CPU máximas y 1 GiB de máximo estático para un invitado de 1 CPU y 512 MiB. En **Advanced**, respete `static min <= dynamic min <= dynamic max <= static max`. Arranque y confirme esa referencia en el invitado. Los cambios del número máximo de CPU y de la memoria estática requieren para este ejercicio una ventana de mantenimiento con la VM detenida.
3. En ejecución, cambie las CPU actuales de 1 a 2 en **General**. Espere, actualice ambas pestañas y compruebe las CPU activas del invitado y la carga de trabajo. No supere el máximo anotado. Un número de arranque guardado por sí solo no demuestra que la CPU esté disponible en vivo.
4. En **Advanced**, fije el mínimo dinámico en 512 MiB y el máximo dinámico en 768 MiB, dentro de los límites estáticos reservados. Compruebe ambos límites tras cada edición. La memoria de **General** se aplica de forma distinta con memoria fija y con DMC; use los campos dinámicos explícitos para esta prueba. Observe la memoria del invitado y el estado de la aplicación cuando el balloon se estabilice.
5. Anote por separado los resultados del host y del invitado. Restaure los límites y el número de CPU anotados, con un apagado limpio si la retirada en vivo falla o el invitado no puede volver de forma segura. Arranque y verifique de nuevo la carga de trabajo original.

**Fallo:** deténgase ante un error, presión de memoria en el invitado o un cambio inesperado de un límite relacionado. Vuelva a leer cada límite, el número de CPU y la tarea antes de reintentar. No fuerce un reinicio ni siga reduciendo la memoria para que una llamada a la API funcione. Ni DMC ni una llamada correcta a la API garantizan capacidad para las aplicaciones del invitado.

**Resultado de laboratorio, 3 de noviembre de 2026 (parcial):** Observado en el host anidado ce44 con la imagen del appliance ce40 (aplicación 5.113.2_e281c536-47), a través de la API JSON-RPC del appliance, en un invitado desechable sin herramientas de invitado. Se rechazó un cambio de CPU en vivo por encima del máximo (`VM state is running but should be halted`). Un cambio de CPU en caliente en un invitado sin soporte de conexión en caliente falló con `VM lacks feature`; el número de arranque se quedó en el nuevo valor hasta el siguiente cambio mientras el número de CPU activas seguía en 1, así que vuelva a leer ambos. Un máximo superior al número de CPU del host impide el arranque (`Not enough CPUs`). Los límites dinámicos de memoria cambiaron con la VM en ejecución. El máximo estático no puede cambiar en ejecución, y el campo `memory` solo cambia el máximo dinámico. No se observó la respuesta de CPU ni de balloon en el invitado, así que este modo sigue pendiente.

## Copiar una VM en ejecución o suspendida (VM07) {#active-copy}

Alcance: la misma base de fuentes XO5/ce40/ce47. Use el [procedimiento de copia completa](#full-copy) existente con estos pasos específicos de cada estado.

1. Use un invitado desechable con un archivo de muestra y su suma de comprobación ya volcados a disco, espacio suficiente en un SR con escritura del mismo pool y sin dispositivos compartidos ni de paso directo. Quite todas las VIF antes de arrancarlo. Mantenga desactivados los trabajos de copia de seguridad y haga inventario de las instantáneas existentes.
2. Para **Running**, vuelque a disco los datos del invitado y después seleccione **Copy**, **Full copy**, un nombre único y el SR exacto del mismo pool. En el mismo pool no se usa compresión. El backend toma una instantánea de la VM en ejecución, la copia y después intenta limpiar la instantánea. Esto no es una inmovilización de la aplicación ni un punto de control de memoria.
3. Pruebe por separado **Suspended**: suspenda el origen aislado con la acción de energía, confirme el estado y solicite otra copia completa con nombre. Esta versión la rechaza (consulte el resultado de laboratorio más abajo). No suponga que una copia conserva la memoria suspendida ni el estado de energía del origen.
4. Para cada resultado, anote los ID de VM de origen y copia, los ID de disco, los SR, el estado de energía y los restos de instantáneas temporales. Mantenga cada copia detenida y quite todas las VIF heredadas antes de arrancarla o reanudarla. Si no está detenida, deténgase e investigue antes de continuar. Arranque por consola y compare la suma de comprobación de la muestra. Confirme que el origen sigue utilizable en su estado previsto.

**Fallo:** haga inventario de las VM, discos e instantáneas parciales antes de limpiar o reintentar. Conserve el origen y la copia de seguridad independiente. Una tarea completada por sí sola no demuestra la coherencia de los discos ni la conservación del historial de instantáneas.

**Resultado de laboratorio, 3 de noviembre de 2026 (parcial):** A través de la API, un origen en ejecución produjo una copia detenida con su propio disco y una dirección MAC nueva; el origen siguió Running y no quedó ninguna instantánea temporal. La copia conservó la VIF del origen, así que quítela antes de cualquier arranque. Un origen Suspended se rechaza (`VM state is suspended but should be halted`): reanúdelo o deténgalo primero y no espere una copia suspendida. No se ejecutaron el arranque del invitado ni la suma de comprobación de la copia, así que este modo sigue pendiente.

## Instantáneas en vivo y con memoria (VM09) {#active-snapshots}

Alcance: la misma base de fuentes XO5/ce40/ce47. Use un invitado desechable aislado sin VIF, con discos normales incluidos, acceso por consola, capacidad libre de SR y host y los trabajos desactivados. Anote su UUID, la cobertura de discos, la suma de comprobación del archivo de referencia y las instantáneas existentes.

1. Con el invitado en ejecución, vuelque a disco un archivo de muestra que contenga `live-A`. En **Snapshots**, seleccione **New snapshot**. Anote el nuevo UUID y la cobertura de discos. Es una instantánea de disco, no una garantía de coherencia de la aplicación.
2. Cambie la muestra a `live-B`, vuélquela a disco, apague el invitado limpiamente y siga el [procedimiento de reversión](#snapshot-revert) con **Snapshot before** activado. Un punto en vivo puede arrancar la VM durante la reversión, así que el aislamiento ya debe existir en el punto guardado. Compruebe el estado, las VIF, la consola y la suma de comprobación de `live-A`.
3. En una prueba aparte, ejecute el invitado aislado con un marcador inofensivo sin guardar en un editor del invitado. Seleccione **New snapshot with memory**. Anote el UUID y si existe realmente un punto de control con memoria. El backend puede recurrir a una instantánea de disco ante `VM_BAD_POWER_STATE`; el botón por sí solo no demuestra que se haya guardado la memoria.
4. Cambie el marcador y la muestra de disco, y después revierta a ese punto de control exacto con un punto previo y capacidad suficiente. Compruebe el marcador de RAM restaurado, la suma de comprobación del disco, la consola, la carga de trabajo y el estado de energía real. No considere un éxito solo de disco como un éxito de memoria.
5. Tras la aceptación, elimine solo los puntos de prueba anotados y compruebe las instantáneas, los discos y la capacidad restantes. No toque los puntos gestionados por copias de seguridad.

**Fallo:** guarde los errores de tarea y los inventarios; compruebe el estado de la VM de origen antes de reintentar. Los puntos de control con discos excluidos o compartidos o con paso directo, la inmovilización de aplicaciones y la coherencia de las copias de seguridad requieren pruebas aparte.

**Resultado de laboratorio, 3 de noviembre de 2026 (parcial):** En un invitado en ejecución, una instantánea de disco tenía el estado de energía Halted y ningún VDI de suspensión. **New snapshot with memory** produjo una instantánea con estado de energía Suspended y un VDI de suspensión. Revertir a cualquiera de ellas dejó la VM en Running. El invitado de prueba no tiene herramientas de invitado, así que no se comprobaron el marcador de RAM ni los datos del invitado, y este modo sigue pendiente.

## Conservar discos seleccionados al eliminar (VM11) {#retain-disks}

Alcance: la misma base de fuentes XO5/ce40/ce47. La API de eliminación de VM tiene un booleano `deleteDisks` para toda la VM, no una lista por disco. Conserve los discos seleccionados separando primero sus VBD, con la VM desechable detenida.

1. Cree y verifique una copia de recuperación independiente. Anote el UUID de la VM, todos los ID de VBD y VDI, el SR, el tamaño, las instantáneas y qué discos deben sobrevivir. Use discos normales no compartidos y detenga todos los trabajos relacionados.
2. En **Disks**, use **Remove VDI from this VM** para cada disco que conserve, no **Destroy VDI**. La acción de la fila elimina el VBD de inmediato; la eliminación de la VM no tiene ninguna casilla para conservar discos concretos. Actualice: el VBD debe haber desaparecido, pero ese VDI exacto debe seguir existiendo en su SR. Desconectar un disco sin más no basta.
3. Elimine la VM detenida identificada con la confirmación normal. Esto puede eliminar recursivamente sus instantáneas y los discos restantes que cumplan las condiciones. Cancele cualquier solicitud de forzado e investigue.
4. Compruebe que la VM ya no existe, que los VDI conservados siguen existiendo y que solo se eliminaron los discos conectados desechables previstos. Conecte un VDI conservado a otra VM de recuperación detenida y aislada, arránquela y compruebe la suma de comprobación de la muestra; después sepárelo sin eliminarlo.

**Fallo:** deténgase si el diálogo no distingue entre quitar la conexión y eliminar datos. Anote los inventarios parciales de VM, VDI e instantáneas tras cualquier fallo. Nunca deduzca la conservación a partir de una fila de VM desaparecida o de un disco desconectado.

Implementación fijada: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [packages/xo-server/src/api/vbd.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vbd.mjs), [packages/xo-server/src/xapi/mixins/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs), [packages/xo-server/src/xapi/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [@xen-orchestra/xapi/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [packages/xo-web/src/xo-app/vm/tab-advanced.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [packages/xo-web/src/xo-app/vm/tab-disks.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js).

**Resultado de laboratorio, 3 de noviembre de 2026 (solo a nivel de almacenamiento):** A través de la API, quitar el VBD de un segundo disco y eliminar después la VM con `deleteDisks` en true eliminó la VM y su disco de sistema y dejó el VDI separado en su SR. No se ejecutaron la conexión del disco conservado a una VM de recuperación ni la comprobación de sus datos, así que este modo sigue pendiente.
