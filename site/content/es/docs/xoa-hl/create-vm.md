---
title: "Crear su primera máquina virtual"
linkTitle: "Su primera VM"
description: "Cargar una ISO de instalación, crear una VM e instalar su sistema operativo."
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: reviewed
sourceRevision: sha256:7ad93b382e01b5bcf49985b7bfa1aca1a167efcea5adc982557deeaf736346b8
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Cree una pequeña VM de prueba, instale su sistema operativo y compruebe que arranca desde su propio disco virtual.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261027-ca44911`, el paquete `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Probado en un dispositivo virtual de laboratorio el 27 de octubre de 2026 con un invitado Linux; otros sistemas invitados necesitan sus propias pruebas. Los tamaños siguientes son ejemplos, no una lista de sistemas admitidos. Recompilada el 27 de octubre de 2026 con la corrección de aprovisionamiento de `build-xoa-hl@fa0c987`. Consulte [cómo identificar el archivo corregido](/docs/xoa-hl/first-login/#identify-the-rebuilt-image). Los resultados de exportación/importación y de creación de VM registrados en [#315](https://github.com/Vagrantin/xcp-hl/pull/315) son anteriores a esta recompilación. Aquí no consta ninguna repetición de esas pruebas con el archivo recompilado.
{{< /callout >}}

## Antes de empezar {#before-you-begin}

- [Inicie sesión y conecte el host](/docs/xoa-hl/first-login/). Esta guía utiliza una cuenta de administrador de XOA-HL.
- Descargue una ISO de instalación del proveedor del sistema operativo. Compruébela con la suma de comprobación publicada por el proveedor.
- Localice dos tipos de almacenamiento: un **SR de ISO** para los medios de instalación y un **SR con escritura** con espacio libre para los discos de las VM. No todos los hosts tienen la [biblioteca ISO de XCP-HL](/docs/features/#iso-storage).
- ¿Necesita un SR nuevo para los discos de las VM? Primero [crea almacenamiento NFS en una exportación vacía y dedicada](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Vuelva a sus comprobaciones de disco cuando esta VM esté instalada.
- Elija una red de invitados que proporcione al instalador el acceso que necesita. Deje suficiente memoria y almacenamiento del host para XOA-HL y las demás VM.

Administre la VM desde su **navegador**. El sistema operativo se instala en la **consola de la nueva VM**, nunca en el host XCP-HL ni en el dispositivo virtual XOA-HL.

## 1. Obtener la ISO de instalación {#1-get-the-installer-iso}

Si ya hay un instalador comprobado en una biblioteca ISO, utilízalo y omita este paso. Para conectar una biblioteca NFS dedicada, siga [Conectar una biblioteca ISO NFS](/docs/xoa-hl/storage-networks/#nfs-iso-library).

La carga desde el navegador solo funciona si el SR de ISO acepta archivos nuevos y dispone de espacio suficiente. Ver el SR en la lista de importación no lo demuestra: algunas bibliotecas permiten leer medios, pero no aceptan cargas.

1. Abra **Import → Disk** (`/#/import/disk`). Mantenga **From URL** desactivado para cargar el archivo que descargó.
2. Seleccione el **SR de ISO**, por ejemplo `XCP-HL ISO library` si lo tiene. Arrastre el archivo `.iso` a la zona de carga.
3. Compruebe el nombre del archivo y el destino. Seleccione **Import** y espere a que termine.
4. Abra la lista de discos del SR de destino y compruebe que la ISO está presente. No continúe con una carga incompleta.

Si no aparece un SR de ISO adecuado, configúralo primero. Importar una ISO al almacenamiento normal de discos de VM no lo convierte en una biblioteca ISO.

## 2. Crear la VM {#2-create-the-vm}

Abra **New → VM** (`/#/vms/new`) y seleccione su **pool**. Elija una plantilla que permita instalar su sistema operativo, no una plantilla que ya contenga un sistema instalado.

Asigne a la VM un nombre claro, como `lab-first-vm`. Los siguientes tamaños sirven para un pequeño sistema Linux de prueba, siempre que cumplan los requisitos del proveedor:

| Sección del asistente | Qué elegir |
| --- | --- |
| Info | La plantilla de instalación, un nombre y una descripción. |
| Performance | Por ejemplo, 2 vCPU y 2 GiB de RAM. Añada más si el instalador lo necesita. |
| Installation | **ISO/DVD** y, después, la ISO de instalación. |
| Interfaces | La red de invitados. Deje vacía la dirección MAC para que se genere, salvo que su red necesite una fija. |
| Disks | Por ejemplo, un disco de 20 GiB en un SR con escritura al que pueda acceder el host. Nunca coloque el disco del sistema en el SR de ISO. |
| Advanced | Conserve los valores predeterminados de la plantilla salvo que el invitado necesite un cambio documentado. Desmarque **Boot VM after creation** para arrancar la VM manualmente. |
| Summary | Compruebe el pool, la plantilla, la CPU, la memoria, la red y el almacenamiento. |

Seleccione **Create**.

**Comprobación:** aparece una VM con el nombre elegido y su configuración coincide con sus selecciones. Si **Create** está deshabilitado, falta completar una sección obligatoria o una comprobación de recursos. Revise el asistente antes de volver a intentarlo.

Para los controles de la consola o una pantalla vacía o bloqueada, consulte [Usar la consola de una VM](/docs/xoa-hl/vm-operations/#vm-console).

## 3. Instalar el sistema operativo {#3-install-the-operating-system}

1. Abra la nueva VM y compruebe su nombre. Arránquela y abra la pestaña **Console**.
2. Compruebe que se inicia el instalador. Siga los pasos de instalación del proveedor dentro de este invitado.
3. Cuando el instalador pida un disco de destino, compruebe que sea el **disco virtual de la nueva VM** (20 GiB en este ejemplo). Si el disco ya contiene datos, deténgase y compruebe que ha seleccionado la VM correcta.
4. Cuando termine la instalación, abra la pestaña **Disks** de la VM y expulse la ISO de instalación de la unidad de CD virtual. Reinicie el invitado normalmente y compruebe que arranca desde su disco virtual.

{{< callout type="warning" >}}
Trabaje únicamente en la nueva VM de prueba. Formatear un disco o forzar un apagado puede provocar pérdida de datos. Si el invitado responde, utilice su apagado o reinicio normal. Nunca detenga el dispositivo virtual XOA-HL ni el host para reiniciar un invitado.
{{< /callout >}}

## 4. Comprobar el resultado {#4-check-the-result}

- El invitado arranca sin la ISO de instalación y puede iniciar sesión a través de su consola.
- La CPU, la memoria, los discos y la red de la VM coinciden con sus selecciones.
- Dentro del invitado funcionan la dirección IP, la puerta de enlace, el DNS y las conexiones necesarias. La consola sigue funcionando aunque la red del invitado no lo haga.
- Ha anotado la versión del sistema operativo invitado, la plantilla, el nombre de la VM y las versiones de XOA-HL.

Las herramientas del invitado dependen del sistema operativo. Para Ubuntu 24.04, consulte los siguientes pasos.

Esta VM todavía no tiene una copia de seguridad independiente. Una instantánea en el mismo almacenamiento no protege frente a la pérdida de ese almacenamiento. No guarde datos importantes en esta VM hasta haber probado una copia de seguridad y una restauración.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| La ISO no aparece en el asistente | Compruebe que terminó la carga en un SR de ISO y que el pool o host seleccionado puede acceder a ese SR. |
| **Create** está deshabilitado | Compruebe el pool, la plantilla, el nombre, los recursos, la ISO, la red y el almacenamiento de discos. Complete todas las secciones obligatorias. |
| Falla la creación o el arranque de la VM | Lea el error de la tarea. Compruebe la memoria libre del host, el espacio libre del SR y el acceso del host al almacenamiento y a la red elegidos. Antes de repetirlo, compruebe si ya se creó una VM. |
| El instalador vuelve a arrancar después de cada reinicio | Expulse la ISO de la unidad de CD de esta VM. Compruebe que el sistema se instaló en su disco virtual. |
| El invitado no tiene red | Compruebe la red seleccionada y la dirección IP, la puerta de enlace y el DNS del invitado. No cambie la red de administración del host para solucionar un problema del invitado. |

## Siguientes pasos {#next-steps}

1. [Cree una copia de seguridad de la VM de prueba y compruebe una restauración](/docs/xoa-hl/backup-restore/).
2. Para un invitado Ubuntu 24.04 (amd64), [instala el agente de administración](/docs/xoa-hl/guest-tools/#install-linux-agent). Otros sistemas necesitan su propio procedimiento.
3. Para reutilizar un invitado instalado, [crea VM nuevas a partir de una plantilla](/docs/xoa-hl/templates/#deploy-template).

Consulte también el [glosario](/docs/xoa-hl/glossary/) y la [guía de actualización](/docs/guides/updates/).

{{< details title="Fuentes" closed="true" >}}
Contrastado con XO@e281c536: [importación de ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [asistente de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [pestañas de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) y [control de expulsión de CD](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js); [parches aplicados en xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
