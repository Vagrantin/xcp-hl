---
title: "Administrar discos, almacenamiento, bibliotecas ISO y redes"
linkTitle: "Almacenamiento y redes"
description: "Añada discos e interfaces de red, conecte almacenamiento NFS y bibliotecas ISO, añada almacenamiento local y cree una VLAN."
weight: 50
translationKey: xoa-manual-storage-networks
translationStatus: draft
sourceRevision: sha256:dc1dfa67e33ea10129415cf1f53a040988944af6b59b5e8a76b0fb63a2cbf854
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Añada un disco o interfaz de red a una VM, conecte NFS para ISO o discos de VM, convierta un disco libre del host en almacenamiento local y cree una red VLAN. Practique con una VM de prueba detenida, nunca con el propio appliance, conectado al **appliance XOA-HL** como administrador. Antes de empezar, anote ID, discos e interfaces de la VM.

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio.
{{< /callout >}}

## Conozca los objetos {#objects}

| Objeto | Qué es |
| --- | --- |
| SR | Repositorio de almacenamiento: donde se guardan discos virtuales. Compruebe su espacio libre |
| VDI | Disco virtual almacenado en un SR |
| VBD | Enlace entre una VM y uno de sus discos virtuales |
| VIF | Interfaz de red virtual de una VM |
| PIF | Interfaz de red de un host. Cambiar la red de administración puede dejarle sin acceso al host |

La interfaz de una VM no es la interfaz de administración del host. Elegir una red o generar una MAC nueva no aísla una VM. Antes de conectar un invitado clonado o restaurado, compruebe VLAN, enlace físico y enrutamiento reales.

## Añada un disco vacío pequeño {#add-disk}

1. Compruebe que la VM de prueba está detenida. Abra **Disks** (`/#/vms/<id>/disks`) y seleccione **New disk**.
2. Elija un SR con escritura en el mismo pool, un nombre claro de prueba y un tamaño pequeño con su unidad. Deje desactivada la opción de solo lectura. Cree el disco una vez y espere a que termine.
3. Compruebe la fila nueva: nombre, tamaño, SR y VM conectada. Anote el ID del disco y espacio libre restante del SR antes de arrancar.

En la consola del invitado, identifique el disco nuevo por su tamaño y datos del dispositivo. XO lo crea y conecta, pero no lo particiona, formatea ni monta dentro del invitado. Esa es una tarea independiente específica del SO. Nunca formatee un dispositivo basándose solo en un nombre supuesto.

Si falla la creación, compruebe la tarea y las listas de discos de VM y SR antes de repetir: una operación parcial puede dejar un disco. Guarde el error, compruebe espacio y conectividad y consulte [resolución de problemas](/docs/xoa-hl/troubleshooting/) si hace falta. Reducir, ampliar o mover discos queda fuera de esta sección.

## Desconecte o elimine un disco {#detach-vs-delete}

Eliminar el VBD separa el disco de la VM, pero sus datos (VDI) siguen existiendo. Eliminar el VDI destruye los datos; es otra acción y esta pantalla no la ofrece mientras esté conectado. Desconectar una conexión también es distinto de eliminarla.

Para limpiar, detenga el invitado e identifique con certeza el disco vacío de prueba. Conserve el VDI si su contenido aún puede ser útil. Nunca borre un disco de arranque, compartido o sin identificar para despejar un aviso de espacio. [Proteja los datos valiosos del invitado](/docs/xoa-hl/backup-restore/) por separado.

## Añada una interfaz de red aislada {#add-vif}

1. En la VM de prueba detenida, abra **Network** (`/#/vms/<id>/network`) y seleccione **New device**.
2. Seleccione una red del mismo pool cuyo aislamiento haya comprobado. Deje la MAC vacía para que se genere y seleccione **Create**.
3. Antes de arrancar, compruebe interfaz nueva, red y MAC. Tras arrancar, compruebe que el invitado ve la interfaz y tiene la conectividad prevista.

Para aislar un clon o restauración, quite **todas** las VIF heredadas con la VM detenida y compruebe la lista vacía antes del primer arranque. Use eliminar, no solo el interruptor de conexión: una interfaz desconectada no es una interfaz aislada. Añada una red de prueba solo tras confirmar que no alcanza producción y resolver las identidades del invitado copiadas.

Si la VM alcanza destinos inesperados, deténgala y compruebe red elegida y aislamiento externo a XO antes de repetir. Estos pasos no configuran PIF de host, direcciones de administración, bonds ni VLAN; no cambie la red de administración del host al seguirlos. Para una VLAN en hosts, consulte [Crear una VLAN de laboratorio en un enlace libre](/docs/xoa-hl/storage-networks/#host-vlan-network). Para otras tareas, consulte [Administrar VM](/docs/xoa-hl/vm-operations/) o [Hosts y pools](/docs/xoa-hl/hosts-pools/).

## Conecte una biblioteca ISO NFS {#nfs-iso-library}

Un SR ISO contiene medios de instalación. Difiere de un SR con escritura para discos de VM y de un destino de copias. Estos pasos conectan una exportación NFS dedicada ya existente con un ISO comprobado frente a la suma del proveedor. El administrador de almacenamiento prepara la exportación y coloca el archivo; usted trabaja solo en el navegador sin cambiar el host.

**Antes de empezar**

- Compruebe si el pool ya tiene un SR ISO apropiado. Si identidad, acceso de hosts y medios son correctos, úselo.
- Para una biblioteca nueva, anote servidor NFS, ruta exacta exportada, versión NFS acordada, pool y hosts y nombre y suma del ISO.
- Todos los hosts que lean el ISO deben tener acceso autorizado a la exportación. Acceder desde navegador o appliance no demuestra acceso desde hosts.

1. Como administrador, abra **New → Storage** (`/#/new/sr`). Elija un host del pool. Introduzca un nombre claro, como `lab-nfs-iso`, y una descripción que identifique la exportación de prueba.
2. En **ISO SR**, seleccione **NFS ISO**. No elija **NFS** de **VDI SR**: crea almacenamiento de discos VM. **Local** significa una carpeta del hipervisor, no de su equipo ni appliance. Almacenamiento local, SMB y de bloques quedan fuera de esta sección.
3. Introduzca el servidor en **Server**. Elija la versión acordada (el formulario ofrece predeterminada, `4` y `4.1`) y pulse el icono de búsqueda junto al servidor. Cambiar versión no repite la búsqueda: hágala tras cada cambio. Deje **Comma delimited NFS options** vacío salvo opciones acordadas.
4. Seleccione la exportación exacta en **Path**, en su raíz (no se cubren subcarpetas). Espere la comprobación. Si falta, falla la comprobación o **Storage usage** enumera SR existentes, deténgase y revise error e ID. El asistente ejecuta comprobaciones NFS incluso para ISO: un SR detectado no es necesariamente una biblioteca ISO. No lo vuelva a conectar ni acepte crear sobre almacenamiento existente.
5. En **Summary**, compruebe nombre y tipo (`nfsiso`). Revise host, servidor y ruta arriba y pulse **Create** una vez. Si falla, compruebe SR del pool antes de repetir: una solicitud fallida puede dejar un SR o conexión de host parcial.
6. Anote UUID del SR. Su tipo de backend es `iso` (`nfsiso` es solo la elección del asistente). Abra **Hosts** (`/#/srs/<id>/hosts`) y compruebe que cada conexión está conectada y muestra la exportación correcta. Ser compartido no demuestra acceso desde todos los hosts. Ejecute VM solo en hosts con acceso comprobado.
7. Use **Rescan all disks** del SR, espere y abra **Disks** (`/#/srs/<id>/disks`). Compruebe nombre y tamaño del ISO. Repita el escaneo cuando el administrador añada o sustituya archivos. Compruebe la suma del proveedor en origen: un escaneo correcto o nombre coincidente no demuestran integridad.

**Comprobación:** en el [asistente de VM nueva](/docs/xoa-hl/create-vm/), elija el mismo pool y compruebe que **ISO/DVD** ofrece el medio esperado. Si aparece, omita la carga por navegador. Leer medios y cargar nuevos son capacidades distintas: la lista de importación no demuestra que este SR admita ISO nuevos. Nunca amplíe permisos indiscriminadamente para hacer funcionar una carga.

| Problema | Qué comprobar |
| --- | --- |
| No aparece exportación o falla la ruta | Anote el error. Compruebe con el administrador servidor, ruta, versión, descubrimiento y acceso de hosts. Deténgase si el asistente no encuentra la exportación. |
| Existe el SR pero un host está desconectado | Compruebe conexión, ruta y acceso de ese host a la exportación. Otro host conectado no basta. No desconecte todos para intentar repararlo. |
| El escaneo funciona pero falta el ISO | Compruebe archivo completo en la exportación acordada, nombre, tamaño y SR seleccionado. Corrija el origen y repita el escaneo. No recree el SR repetidamente. |
| Falta el ISO en ISO/DVD | Compruebe pool del asistente, tipo ISO del SR, presencia del medio y conexión del host. Un SR NFS para discos VM no es un SR ISO. |
| Falla la creación o aparece un SR inesperado | Guarde error y lista de UUID y conexiones. Identifique objetos parciales antes de repetir o limpiar. Nunca use Forget, Remove ni formateo para ocultar un error inexplicado. |

No quite un ISO ni desconecte u olvide su SR mientras una VM lo use. Anote qué VM lo usan y expulse el medio del invitado de prueba antes de planear la limpieza. No se cubren eliminación de SR ni carga de ISO.

## Cree almacenamiento NFS para discos de VM {#nfs-vm-storage}

Úselo cuando necesite un **SR con escritura para discos de VM**. Una biblioteca ISO NFS almacena instaladores y un remoto NFS de copias almacena copias: ninguno es el SR creado aquí. El almacenamiento compartido por sí solo no es una copia ni implica preparación para migración o HA.

### Prepare una exportación dedicada {#prepare-a-dedicated-export}

- Use una exportación de laboratorio vacía y dedicada, aprobada por el responsable, con espacio para disco de prueba y margen libre.
- Anote servidor NFS, raíz exacta, versión y opciones acordadas, pool y todos los hosts que la usarán.
- El administrador debe permitir lectura/escritura desde esos hosts y comprobar espacio y cuotas del servidor.
- No reutilice exportación ISO, destino de copias ni exportación con datos sin identificar.

Acceda al **appliance XOA-HL** como administrador; crear y comprobar almacenamiento requiere administración del host seleccionado. Anote primero los SR existentes. Si el almacenamiento ya existe, compruebe UUID y acceso de hosts en vez de crear otro SR. No necesita una VM para crearlo. Si contendrá su primera VM, créelo y compruébelo abajo, [cree e instale la VM](/docs/xoa-hl/create-vm/) en él y vuelva para la prueba de disco. Nunca use XOA-HL como VM de prueba.

### Cree el SR y compruébelo {#create-the-sr-and-check-it}

1. Abra **New → Storage** (`/#/new/sr`), elija un host y un nombre claro como `lab-nfs-vdis` y descripción de la exportación. En **VDI SR**, seleccione **NFS**. Compruebe que **NFS ISO**, de **ISO SR**, no está seleccionado.
2. Introduzca **Server**, elija **NFS version** acordada (predeterminada, `4` o `4.1`) y pulse búsqueda. Deje **Comma delimited NFS options** vacío salvo opciones acordadas. Si cambia servidor o versión, repita búsqueda y ruta: cambiar solo versión no comprueba de nuevo la exportación.
3. Seleccione la raíz exacta en **Path**, sin subcarpeta, y espere. Mire **Storage usage**. Si aparece UUID de SR existente o entrada en uso, deténgase e identifique con el propietario. No reconecte ni cree otro encima. Para NFS, XO **no** pide confirmar almacenamiento existente: no ver un aviso no demuestra una exportación vacía.
4. En **Summary**, compruebe nombre, tipo `nfs` y ruta. Revise host, servidor, versión y opciones y seleccione **Create** una vez; espere. Si falla, compruebe listas SR y conexiones antes de repetir: pueden quedar objetos.
5. Anote UUID del SR. En **General** (`/#/srs/<id>/general`), compruebe `Type: nfs`, tamaño, espacio usado/libre y pool.
6. Abra **Hosts** (`/#/srs/<id>/hosts`). Anote PBD de cada host y compruebe **Connected**, con `server` y `serverpath` correctos (y `nfsversion` y `options` si los configuró). Un host conectado no demuestra los demás. Si falta una conexión o está desconectada, deténgase antes de ubicar VM. El estado es también un botón: léalo sin pulsarlo.

### Pruebe un disco en el SR nuevo {#test-a-disk-on-the-new-sr}

1. Siga [Añadir un disco vacío pequeño](#add-disk) sobre la VM detenida eligiendo este SR. Anote ID de VM, disco y conexión y compruebe SR y tamaño.
2. Arranque solo en un host con conexión comprobada. Identifique el disco extra por tamaño y datos del dispositivo. Particionarlo, formatearlo y montarlo requiere procedimiento específico del SO e identificación segura.
3. Si un administrador del invitado prepara este **disco de prueba**, escriba un archivo inocuo y anote su suma. Guarde el trabajo, apague normalmente, arranque de nuevo y compruebe el mismo disco, archivo y suma.

**Comprobación:** archivo y suma no cambian tras reiniciar. Un disco vacío o escaneo exitoso no demuestra escritura ni persistencia. Mantenga el resultado separado de una prueba de copia/restauración. Antes de afirmar acceso desde todo el pool, repita lectura y escritura en cada host mediante una prueba de ubicación o migración autorizada por separado.

### Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| No hay exportación o falla la comprobación | Guarde error exacto, host, servidor, ruta y versión. Pida al administrador comprobar descubrimiento, permisos y conectividad. No cambie a almacenamiento local o de bloques ni amplíe permisos para eludirlo. |
| Se detecta SR existente o falla la creación | Anote cada UUID y conexión, incluidos objetos parciales. Averigüe propietario y usuarios antes de repetir o reconectar. |
| Tipo/ruta incorrectos o host desconectado | Detenga nuevas asignaciones. Compare exportación anotada con cada conexión. No desconecte todos ni quite un SR para diagnosticar. |
| Aviso de espacio o escritura fallida en invitado | Compruebe uso SR, espacio/cuotas del servidor, tareas activas y disco exacto del invitado. Conserve pruebas y datos. No elimine discos, instantáneas ni archivos del NAS sin identificar. |

Para limpiar, guarde la lista final y apague normalmente la VM. Aplique [Desconectar o eliminar un disco](#detach-vs-delete) solo al disco identificado con certeza. Conserve SR y exportación hasta que el responsable enumere usuarios y necesidades de recuperación. No se cubren destrucción, olvido o reconexión de SR, borrado en NAS, cambio de almacenamiento predeterminado, SMB o iSCSI, subcarpetas NFS, caídas, rendimiento ni migración o HA del pool.

## Cree almacenamiento local en un disco libre {#local-disk-storage}

Convierta un disco físico vacío y libre de **un host** en un SR con escritura para VM. Solo pertenece a ese host: sus VM no pueden trasladarse sin mover sus discos y se pierde con el host. No es una copia de seguridad.

{{< callout type="warning" >}}
Crear el SR **borra todo el disco o partición** que introduzca. XO acepta cualquier ruta. No comprueba que esté vacío ni que no sea el disco de sistema o un SR existente.
{{< /callout >}}

### Identifique el disco en el host {#identify-the-disk-on-the-host}

Trabaje **en el host XCP-HL** que contiene el disco, como root, mediante consola o SSH.

1. Enumere discos e identidades. Sustituya `/dev/sdX` por el candidato y `<host-uuid>` por el UUID del host.

   ```bash
   lsblk -o NAME,SIZE,TYPE,MODEL,SERIAL,MOUNTPOINT
   ls -l /dev/disk/by-id/
   blkid /dev/sdX
   pvs
   xe pbd-list host-uuid=<host-uuid> params=sr-uuid,device-config
   ```

2. Encuentre el disco cuyo tamaño, modelo y serie coincidan con el añadido. No debe mostrar particiones ni punto de montaje; `blkid` no debe imprimir nada para él y `pvs` no debe enumerarlo.
3. Compruebe que ningún SR existente lo use: ningún valor `device-config` enumera el disco.
4. Anote su ruta estable en `/dev/disk/by-id/`, por ejemplo `/dev/disk/by-id/ata-<model>_<serial>`. Nombres como `/dev/sdb` pueden cambiar tras reiniciar; `by-id` no.

Si hay algo sin identificar en el disco, deténgase. No lo borre para hacer espacio.

### Elija el tipo {#choose-the-type}

- **ext (local)** guarda cada disco virtual como archivo y usa espacio según se escriben datos (aprovisionamiento fino).
- **LVM (local)** reserva todo el tamaño de cada disco al crearlo (aprovisionamiento grueso).

Ambos almacenan discos de VM. Sin motivo para diferir, use el mismo tipo que el SR local existente del host.

### Cree el SR y compruébelo {#create-the-sr-and-check-it-1}

1. En XOA-HL, abra **New → Storage** (`/#/new/sr`). Elija el **Host** del disco y un nombre claro como `local-disk2` y descripción con modelo y serie. En **VDI SR**, seleccione **ext (local)** o **LVM (local)**.
2. En **Device**, pegue la ruta `by-id` anotada.
3. En **Summary**, compruebe host, nombre y tipo y seleccione **Create** una vez.
4. La confirmación dice *This will erase the entire disk or partition (…) to create a new storage repository.* Compruebe que la ruta entre paréntesis es la anotada y confirme.
5. Anote UUID nuevo. En **General** (`/#/srs/<id>/general`), compruebe tipo (`ext` o `lvm`), tamaño próximo al disco y pool.
6. Abra **Hosts** (`/#/srs/<id>/hosts`). Compruebe que la única conexión es del host elegido y muestra **Connected**, con su ruta `by-id` como `device`.

**Comprobación:** siga [Probar un disco en el SR nuevo](#nfs-vm-storage) usando este SR: archivo y suma de prueba sobreviven a reiniciar el invitado. Reinicie después el host en una ventana de mantenimiento y compruebe que el SR se reconecta.

### Si algo falla {#if-something-goes-wrong-1}

| Problema | Qué comprobar |
| --- | --- |
| La creación falla con error de dispositivo | Guarde el error. Compruebe ruta y ausencia de particiones, volúmenes o montajes. No fuerce el borrado sin identificar su contenido. |
| Tamaño incorrecto u otro host conectado | Detenga asignaciones de discos. Compare `device` con el disco anotado. Puede haber formateado otro disco: conserve todo y pida ayuda. |
| SR desconectado tras reinicio del host | Compruebe que existe la ruta `by-id` mediante `ls -l /dev/disk/by-id/` y lea el error. No cree un SR nuevo en el mismo disco: lo borraría. |

No se cubren retirada/destrucción de SR local, RAID, particiones como dispositivos SR, **ZFS (local)** ni traslado de VM entre SR locales.

## Cree una VLAN de laboratorio en un enlace libre {#host-vlan-network}

Esto **cambia la configuración del host y pool**: crea una red etiquetada de invitado desde el **navegador XOA-HL**. Use un pool de prueba, enlace físico libre dedicado y VM detenida. Mantenga una consola del host independiente disponible todo el tiempo.

**Antes de empezar**

- Anote pool, maestro y todos los hosts con UUID de redes/PIF existentes, nombres de dispositivo, MAC, VLAN, MTU, marcas de administración, modos IP y estados de conexión.
- Obtenga aprobación de ID VLAN, puertos etiquetados del conmutador, MTU `1500`, direcciones de invitados y destinos permitidos/prohibidos del administrador de red.
- Compruebe el enlace libre en **todos** los hosts: no transporta administración, almacenamiento, copias ni otro tráfico, no tiene IP de host ni pertenece a bond o VLAN existente. Contraste cableado y registros del conmutador; no bastan nombre de dispositivo o ausencia de marca Management.
- Deténgase si no confirma este diseño. Un número VLAN no aísla por sí solo ni configura puertos, rutas, DHCP, DNS o cortafuegos.

### Cree la red una sola vez {#create-the-network-once}

1. Como administrador, abra **New → Network** (`/#/new/network`) y seleccione el **pool** de prueba (requiere administración del pool). Deje **Bonded network** y **Private network** desactivados; Private network es otra función SDN.
2. En **Info → Interface**, elija la **PIF libre del maestro** anotada. La lista muestra PIF del maestro sin VLAN y oculta miembros de bonds, pero **sí** muestra PIF de administración. Compruebe UUID, dispositivo y MAC. No deje Interface vacío: crearía red sin enlace físico, no la VLAN prevista.
3. Introduzca **Name** y **Description** claros. Configure **MTU** `1500` y **VLAN** con el ID etiquetado exacto autorizado. No deje VLAN vacío ni use `0`: el campo vacío se envía como `0`. Seleccione **No NBD Connection**; esta red no necesita NBD.
4. Revise pool, PIF del maestro, VLAN, MTU y ambos interruptores de tipo y pulse **Create network** una vez. Espere hasta que aparezca **Network** del pool (`/#/pools/<id>/network`). Si falla, guarde error y compruebe redes del pool y PIF de cada host antes de repetir. XO intenta limpiar al fallar, pero eso no demuestra reversión de todos los cambios.

### Compruebe todos los hosts {#check-every-host}

1. Copie el UUID de red de su fila del pool y anote nombre, MTU y VLAN. El resumen PIF/VLAN de esa fila procede solo del **maestro**.
2. Expanda **PIFs** y compare host, dispositivo y MAC con sus registros. El icono indica el **enlace físico (portadora)**. El botón **Connected** de Network del host indica si está conectada la PIF. Ninguno demuestra flujo de tráfico etiquetado. No pulse conectar/desconectar solo para leer estado.
3. En cada host abra **Network** (`/#/hosts/<id>/network`), encuentre la PIF nueva y anote UUID, dispositivo, MAC, VLAN, MTU, marca de administración, modo/dirección IP y estado. Compruebe VLAN autorizada exacta, MTU `1500`, conexión, enlace esperado y ausencia de IP de host.
4. Compare conectividad de administración y almacenamiento con sus notas iniciales.

Si falta una PIF o está desconectada o es inesperada, deténgase antes de ubicar invitados. No edite VLAN, MTU o IP existentes ni alterne PIF padre para arreglarlo.

### Compruebe la conectividad del invitado {#check-guest-connectivity}

1. En una VM detenida, siga [Añadir una interfaz aislada](#add-vif) y elija esta red exacta. Anote UUID de VM/VIF, MAC, red y host donde correrá. Compruebe que ninguna interfaz heredada evita el diseño de laboratorio.
2. Arranque solo en un host con PIF comprobada. El administrador del invitado configura mediante consola la **interfaz sin etiquetar** y las IP únicas acordadas. Estos pasos no configuran un troncal VLAN dentro del invitado.
3. Compruebe por separado dirección, subred, ruta y DNS. Pruebe un par o servicio autorizado y los destinos prohibidos enumerados, incluida producción. Un ping fallido no demuestra aislamiento. Anote pruebas y resultados.
4. Apague normalmente, arranque otra vez y repita las comprobaciones.

**Comprobación:** el invitado alcanza el par autorizado, no alcanza destinos prohibidos y lo conserva tras reiniciar; administración del host, almacenamiento y XOA-HL siguen accesibles durante todo el proceso. Un par en el mismo host no prueba enlace físico ni otro host: tráfico entre hosts y migración necesitan pruebas autorizadas propias.

| Problema | Qué comprobar |
| --- | --- |
| Falta la PIF libre o el pool es incorrecto | Compruebe maestro, dispositivo físico y pertenencia a bond/VLAN. Deténgase. Nunca elija PIF de administración/almacenamiento ni cambie de pool para evitar la lista. |
| Error, red duplicada o PIF ausentes en algunos hosts | Guarde horas, error y UUID exactos de red/PIF de todos los hosts. Revise con el propietario antes de repetir. Una notificación no demuestra reversión. |
| Enlace activo pero sin tráfico esperado | Compruebe conexión, asignación VIF, IP/ruta/DNS del invitado, vía etiquetada autorizada del conmutador, par y cortafuegos. Nunca cambie por intuición IP de administración, MTU padre o VLAN. |
| Acceso inesperado a producción o pérdida de administración/almacenamiento | Detenga el invitado, conserve pruebas y use consola independiente con el plan del administrador de red. No haga otros cambios en navegador mientras el diseño sea incierto. |

Para terminar, guarde registros finales y apague normalmente la VM. Quite solo la VIF identificada si los pasos lo requieren. Conserve red, PIF y configuración del conmutador hasta que el responsable enumere usuarios y apruebe un plan de retirada y recuperación. No se cubren borrado de red, edición VLAN/MTU, retirada PIF, bonds, traslado de administración ni IP del host. Cambiar MTU de una red existente puede desconectar y reconectar interfaces. Consulte también [hosts y pools](/docs/xoa-hl/hosts-pools/), [resolución de problemas](/docs/xoa-hl/troubleshooting/) y [Diagnosticar conectividad de red](/docs/xoa-hl/troubleshooting/#network-connectivity).

{{< details title="Fuentes" closed="true" >}}
- **Discos e interfaces**: [interfaz de discos y selección SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [interfaz de red de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [acciones de discos e interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **Almacenamiento NFS y bibliotecas ISO**: [asistente de SR nuevo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js), [API y sondeos SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs), [acción de reescaneo SR](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js), [conexiones de hosts](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js), [API de importación ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs), [selección ISO de VM nueva](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **Capacidad SR**: [XO5 `tab-general.js`](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js).
- **Redes VLAN**: [asistente VLAN](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/network/index.js), [API de redes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/network.mjs), [creación y limpieza VLAN del pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [vista de redes del pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [vista de portadora PIF](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [vista de redes del host](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [campos de PIF y red](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [operaciones MTU](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/network.mjs).
- **Almacenamiento local**: [formulario SR nuevo y confirmación de borrado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js), [creación ext y LVM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs).
{{< /details >}}
