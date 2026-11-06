---
title: "Migrar, exportar e importar una VM"
linkTitle: "Migrar y exportar"
description: "Mueva una VM a otro host de su pool, expórtela como archivo XVA e importe una copia."
weight: 43
translationKey: xoa-manual-vm-transfer
translationStatus: draft
sourceRevision: sha256:a5665d0df57eca23794c955b06c1e75b2c10f373c55fe2b59f2c3a165ab2f756
glossaryTerms: ["vm", "host", "pool", "sr", "snapshot", "backup"]
---

Use una VM desechable sin datos de producción. Acceda al **appliance XOA-HL** como administrador y confirme que están disponibles los hosts, el almacenamiento y la VM. Migrar y exportar mueven o copian una VM completa; ninguna operación sustituye una [prueba independiente de copia de seguridad y restauración](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; migración, exportación e importación aún no probadas en un laboratorio. Las versiones posteriores pueden diferir.
{{< /callout >}}

## 1. Elija la operación {#1-choose-the-operation}

| Objetivo | Operación | Resultado |
| --- | --- | --- |
| Ejecutar la misma VM en otro host de su pool | **Migrate** | Mismo objeto VM; los discos siguen en almacenamiento compartido o se copian a un SR seleccionado |
| Conservar un archivo portátil de una VM detenida | **Export** como XVA | Archivo guardado por el navegador; sin programación, retención ni comprobación de restauración |
| Crear una VM independiente desde un archivo XVA | **Import** | Objeto VM nuevo con identidades del invitado copiadas; aíslelo como un clon |
| Recuperarse de una pérdida | [Copia de seguridad y restauración](/docs/xoa-hl/backup-restore/) | Copia independiente validada mediante una restauración aislada |

Esta guía cubre migración entre hosts del **mismo pool**, exportación XVA sin compresión e importación de archivos XVA. Quedan fuera la migración entre pools, reasignación de redes, archivos OVA, importación desde URL, importación/exportación solo de discos e importación VMware. El menú HomeLab oculta la entrada de importación VMware.

## 2. Migre una VM dentro de su pool {#2-migrate-a-vm-within-its-pool}

Requisitos que debe comprobar antes de empezar:

- El pool tiene al menos dos hosts conectados y usted tiene permiso de administración sobre la VM y el host de destino.
- El host de destino alcanza las redes y el almacenamiento de la VM. Los discos en un SR compartido no necesitan copia. Un disco en almacenamiento inaccesible desde el destino, como un SR local, se copia.
- Una ventana de mantenimiento. Un invitado en ejecución se pausa brevemente durante la migración en vivo; copiar discos tarda más y requiere capacidad libre en el SR de destino.
- Un registro del ID de la VM, host actual, cada disco y su SR, y una comprobación del invitado, como acceso por consola o una prueba de aplicación.

1. Abra la VM y elija **Migrate**. Está disponible para VM en ejecución o detenidas, no suspendidas ni pausadas. Los usuarios de autoservicio no la ven.
2. En **Migrate VM**, use **Select a destination host:** para elegir otro host del mismo pool. La lista excluye el host actual. También puede enumerar hosts de otros pools conectados; no los elija en este ejercicio.
3. Lea la sección de almacenamiento. Si todos los discos están en un SR compartido, no hace falta elegir SR. De lo contrario, XO exige un SR principal (**Select main SR…**) y permite elegir uno por VDI. Elija SR con escritura y espacio libre suficiente; esos discos se copiarán.
4. **Select a migration network:** es opcional dentro de un pool. XO preselecciona la red de migración configurada en el pool cuando el host de destino tiene dirección en ella. Seleccionar cualquier red hace que XO use la vía de migración de almacenamiento en vez de una migración simple del pool. Mantenga el valor propuesto salvo que el diseño del pool especifique otra red.
5. Confirme y espere a que termine la tarea. No vuelva a pulsar mientras la migración esté pendiente.
6. Actualice la pestaña **General** de la VM. Compruebe host, estado, consola, red del invitado y aplicación. Tras copiar discos, compruebe dónde reside ahora cada uno y el espacio libre en ambos SR.

{{< callout type="warning" >}}
Si XAPI informa de que la VM es incompatible con el host de destino, XO ofrece **Force migration**. Cancele en este ejercicio e investigue la compatibilidad de CPU y host. Una migración forzada puede dejar inutilizable el invitado.
{{< /callout >}}

Si una migración simple de pool indica que necesita un SR, XO la reintenta automáticamente como migración de almacenamiento. Entonces usa los SR conectados al host de destino o el SR predeterminado del pool. Una migración que esperaba rápida puede convertirse en una copia de discos. Si falla, conserve el error de la tarea y compruebe host, estado y discos de la VM en cada SR implicado antes de repetir. No repita con la opción de forzar.

## 3. Exporte una VM detenida como archivo XVA {#3-export-a-stopped-vm-as-an-xva-file}

Necesita permiso de administración sobre la VM y espacio libre suficiente en el equipo que ejecuta el navegador.

1. Apague limpiamente el invitado y confirme **Halted**. Anote ID de VM, nombre, discos y tamaño total.
2. Elija **Export**. Mantenga **Type** en `xva` y **Compression** en **Disabled**, su valor predeterminado. Las otras opciones son GZIP (muy lenta) y, en hosts XCP-ng, Zstd. Importar un XVA comprimido queda fuera de esta guía.
3. Confirme. **Download VM** muestra un enlace de descarga, **OK** y **Cancel**. El enlace y **OK** abren la misma URL, que el mensaje describe como válida una sola vez durante un breve periodo. Use solo uno: seleccione el enlace y cierre el diálogo con **Cancel**. La URL contiene un token de acceso de un solo uso: trátela como secreto hasta usarla.
4. El navegador guarda un archivo llamado `<date> - <VM name>.xva`. Mantenga la descarga hasta que termine; cancelarla detiene la exportación. Compruebe que el tamaño es razonable frente a los tamaños de disco anotados.
5. En el equipo del navegador, anote una suma de comprobación, por ejemplo `sha256sum "<file>.xva"`. Úsela para comprobar el archivo antes de importarlo.

Por defecto se ejecutan como máximo dos exportaciones XVA simultáneas por pool. Otra descarga falla en vez de esperar. Deje terminar las activas y solicite un enlace nuevo.

Un XVA contiene discos y configuración de la VM. Almacénelo como los datos que contiene y elimínelo al acabar la prueba. Un archivo exportado no tiene programación, retención ni validación de restauración: no es una tarea de copia de seguridad.

{{< callout type="warning" >}}
Es posible exportar una VM en ejecución, pero entonces XO exporta una instantánea temporal llamada `[XO Export] <VM name>`. Esta copia no es coherente a nivel de aplicación. XO elimina la instantánea al terminar la descarga. Si falla su eliminación, solo registra un aviso y la instantánea puede quedar en el SR. Tras exportar una VM en ejecución, compruebe su pestaña **Snapshots**. Esta guía usa una VM detenida.
{{< /callout >}}

## 4. Importe el XVA como copia aislada {#4-import-the-xva-as-an-isolated-copy}

1. Abra **Import** > **VM** (`/#/import/vm`). La entrada solo aparece si puede operar al menos un pool.
2. Elija el pool de destino en **To Pool:**. **To SR:** propone el SR predeterminado del pool. Elija uno con escritura y espacio libre suficiente.
3. Suelte el archivo `.xva` en el área **Drop OVA or XVA files here to import Virtual Machines.** Compruebe su nombre y tamaño en la lista. Los archivos sin extensión `.xva` u `.ova` se ignoran. Deje **From URL** desactivado.
4. Seleccione **Import** y mantenga abierta la pestaña hasta que termine la carga. Para un solo archivo, XO abre la página de la nueva VM tras el éxito.
5. Mantenga detenida la VM importada. Anote su ID: es un objeto distinto del original incluso si conserva su nombre. Renómbrela para evitar confusiones.
6. Antes del primer arranque, abra **Network** y [quite todas las interfaces virtuales](/docs/xoa-hl/storage-networks/) o establezca un aislamiento externo verificado. La copia contiene el mismo SO invitado, configuración IP, nombre de host, credenciales e identidades de aplicaciones que la fuente.
7. Arranque la copia y compruebe su consola y los datos de prueba anotados.

XO rechaza arrancar una VM cuya MAC duplique la de otra interfaz propia o la de una VM en ejecución. El código de error es `DUPLICATED_MAC_ADDRESS`. No fuerce el arranque; quite o aísle antes la interfaz.

Si falla la importación (**VM import failed**), pueden quedar objetos. Compruebe los discos del SR de destino y la lista de VM en busca de objetos creados durante el intento antes de repetir. Elimine solo restos identificados con certeza mediante el [procedimiento de eliminación de VM desechables](/docs/xoa-hl/vm-operations/#delete-vm).

## 5. Limpie {#5-clean-up}

1. Elimine la VM de prueba importada mediante el [procedimiento de eliminación de VM desechables](/docs/xoa-hl/vm-operations/#delete-vm).
2. Elimine el archivo XVA del equipo y de cualquier ubicación temporal.
3. Confirme que la VM fuente sigue presente, en el host esperado y con sus discos y datos intactos.

Si algo no coincide, conserve los registros y [comunique el problema](/docs/xoa-hl/troubleshooting/) con las versiones e identificadores saneados.

{{< details title="Fuentes" closed="true" >}}
Contrastado con el commit de XO 5 `e281c536` con los parches HomeLab publicados: [barra de acciones de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [acciones de migración, exportación e importación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [diálogo de migración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/migrate-vm-modal/index.js), [red de migración predeterminada](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/utils.js), [diálogo de exportación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/export-vm-modal/index.js), [opciones de compresión](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-compression.js), [página de importación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [API de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [comprobaciones XAPI de migración, importación y arranque](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [gestión de instantáneas de exportación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [exportaciones simultáneas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml) y [etiquetas de interfaz](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js). Cambios del menú HomeLab: [entrada de importación VMware](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzz-xoa-hl-hide-vmware-and-support-alert.patch).
{{< /details >}}
