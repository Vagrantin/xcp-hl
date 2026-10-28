---
title: "Crear tu primera máquina virtual"
linkTitle: "Tu primera VM"
description: "Cargar una ISO de instalación, crear una VM e instalar su sistema operativo."
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: draft
sourceRevision: sha256:8d6fcca90de19f82aff7f4431284f044f9e8f1e2499e67f494ffc106519fd72f
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Crea una pequeña VM de prueba, instala su sistema operativo y comprueba que arranca desde su propio disco virtual.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261022-a280852` (Xen Orchestra 5.113.2). Basado en el código publicado; todavía están pendientes una ejecución completa en un laboratorio y las pruebas específicas del sistema invitado. Los tamaños siguientes son ejemplos, no una lista de sistemas admitidos.
{{< /callout >}}

## Antes de empezar {#before-you-begin}

- [Inicia sesión y conecta el host](/docs/xoa-hl/first-login/). Esta guía utiliza una cuenta de administrador de XOA-HL.
- Descarga una ISO de instalación del proveedor del sistema operativo. Compruébala con la suma de comprobación publicada por el proveedor.
- Localiza dos tipos de almacenamiento: un **SR de ISO** para los medios de instalación y un **SR con escritura** con espacio libre para los discos de las VM. No todos los hosts tienen la [biblioteca ISO de XCP-HL](/docs/features/#iso-storage).
- ¿Necesitas un SR nuevo para los discos de las VM? Primero [crea almacenamiento NFS en una exportación vacía y dedicada](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Vuelve a sus comprobaciones de disco cuando esta VM esté instalada.
- Elige una red de invitados que proporcione al instalador el acceso que necesita. Deja suficiente memoria y almacenamiento del host para XOA-HL y las demás VM.

Administra la VM desde tu **navegador**. El sistema operativo se instala en la **consola de la nueva VM**, nunca en el host XCP-HL ni en el dispositivo virtual XOA-HL.

## 1. Obtener la ISO de instalación {#1-get-the-installer-iso}

Si ya hay un instalador comprobado en una biblioteca ISO, utilízalo y omite este paso. Para conectar una biblioteca NFS dedicada, sigue [Conectar una biblioteca ISO NFS](/docs/xoa-hl/storage-networks/#nfs-iso-library).

La carga desde el navegador solo funciona si el SR de ISO acepta archivos nuevos y dispone de espacio suficiente. Ver el SR en la lista de importación no lo demuestra: algunas bibliotecas permiten leer medios, pero no aceptan cargas.

1. Abre **Import → Disk** (`/#/import/disk`). Mantén **From URL** desactivado para cargar el archivo que descargaste.
2. Selecciona el **SR de ISO**, por ejemplo `XCP-HL ISO library` si lo tienes. Arrastra el archivo `.iso` a la zona de carga.
3. Comprueba el nombre del archivo y el destino. Selecciona **Import** y espera a que termine.
4. Abre la lista de discos del SR de destino y comprueba que la ISO está presente. No continúes con una carga incompleta.

Si no aparece un SR de ISO adecuado, configúralo primero. Importar una ISO al almacenamiento normal de discos de VM no lo convierte en una biblioteca ISO.

## 2. Crear la VM {#2-create-the-vm}

Abre **New → VM** (`/#/vms/new`) y selecciona tu **pool**. Elige una plantilla que permita instalar tu sistema operativo, no una plantilla que ya contenga un sistema instalado.

Asigna a la VM un nombre claro, como `lab-first-vm`. Los siguientes tamaños sirven para un pequeño sistema Linux de prueba, siempre que cumplan los requisitos del proveedor:

| Sección del asistente | Qué elegir |
| --- | --- |
| Info | La plantilla de instalación, un nombre y una descripción. |
| Performance | Por ejemplo, 2 vCPU y 2 GiB de RAM. Añade más si el instalador lo necesita. |
| Installation | **ISO/DVD** y, después, la ISO de instalación. |
| Interfaces | La red de invitados. Deja vacía la dirección MAC para que se genere, salvo que tu red necesite una fija. |
| Disks | Por ejemplo, un disco de 20 GiB en un SR con escritura al que pueda acceder el host. Nunca coloques el disco del sistema en el SR de ISO. |
| Advanced | Conserva los valores predeterminados de la plantilla salvo que el invitado necesite un cambio documentado. Desmarca **Boot VM after creation** para arrancar la VM manualmente. |
| Summary | Comprueba el pool, la plantilla, la CPU, la memoria, la red y el almacenamiento. |

Selecciona **Create**.

**Comprobación:** aparece una VM con el nombre elegido y su configuración coincide con tus selecciones. Si **Create** está deshabilitado, falta completar una sección obligatoria o una comprobación de recursos. Revisa el asistente antes de volver a intentarlo.

Para los controles de la consola o una pantalla vacía o bloqueada, consulta [Usar la consola de una VM](/docs/xoa-hl/vm-operations/#vm-console).

## 3. Instalar el sistema operativo {#3-install-the-operating-system}

1. Abre la nueva VM y comprueba su nombre. Arráncala y abre la pestaña **Console**.
2. Comprueba que se inicia el instalador. Sigue los pasos de instalación del proveedor dentro de este invitado.
3. Cuando el instalador pida un disco de destino, comprueba que sea el **disco virtual de la nueva VM** (20 GiB en este ejemplo). Si el disco ya contiene datos, detente y comprueba que has seleccionado la VM correcta.
4. Cuando termine la instalación, abre la pestaña **Disks** de la VM y expulsa la ISO de instalación de la unidad de CD virtual. Reinicia el invitado normalmente y comprueba que arranca desde su disco virtual.

{{< callout type="warning" >}}
Trabaja únicamente en la nueva VM de prueba. Formatear un disco o forzar un apagado puede provocar pérdida de datos. Si el invitado responde, utiliza su apagado o reinicio normal. Nunca detengas el dispositivo virtual XOA-HL ni el host para reiniciar un invitado.
{{< /callout >}}

## 4. Comprobar el resultado {#4-check-the-result}

- El invitado arranca sin la ISO de instalación y puedes iniciar sesión a través de su consola.
- La CPU, la memoria, los discos y la red de la VM coinciden con tus selecciones.
- Dentro del invitado funcionan la dirección IP, la puerta de enlace, el DNS y las conexiones necesarias. La consola sigue funcionando aunque la red del invitado no lo haga.
- Has anotado la versión del sistema operativo invitado, la plantilla, el nombre de la VM y las versiones de XOA-HL.

Las herramientas del invitado dependen del sistema operativo. Para Ubuntu 24.04, consulta los siguientes pasos.

Esta VM todavía no tiene una copia de seguridad independiente. Una instantánea en el mismo almacenamiento no protege frente a la pérdida de ese almacenamiento. No guardes datos importantes en esta VM hasta haber probado una copia de seguridad y una restauración.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| La ISO no aparece en el asistente | Comprueba que terminó la carga en un SR de ISO y que el pool o host seleccionado puede acceder a ese SR. |
| **Create** está deshabilitado | Comprueba el pool, la plantilla, el nombre, los recursos, la ISO, la red y el almacenamiento de discos. Completa todas las secciones obligatorias. |
| Falla la creación o el arranque de la VM | Lee el error de la tarea. Comprueba la memoria libre del host, el espacio libre del SR y el acceso del host al almacenamiento y a la red elegidos. Antes de repetirlo, comprueba si ya se creó una VM. |
| El instalador vuelve a arrancar después de cada reinicio | Expulsa la ISO de la unidad de CD de esta VM. Comprueba que el sistema se instaló en su disco virtual. |
| El invitado no tiene red | Comprueba la red seleccionada y la dirección IP, la puerta de enlace y el DNS del invitado. No cambies la red de administración del host para solucionar un problema del invitado. |

## Siguientes pasos {#next-steps}

1. [Crea una copia de seguridad de la VM de prueba y comprueba una restauración](/docs/xoa-hl/backup-restore/).
2. Para un invitado Ubuntu 24.04 (amd64), [instala el agente de administración](/docs/xoa-hl/guest-tools/#install-linux-agent). Otros sistemas necesitan su propio procedimiento.
3. Para reutilizar un invitado instalado, [crea VM nuevas a partir de una plantilla](/docs/xoa-hl/templates/#deploy-template).

Consulta también el [glosario](/docs/xoa-hl/glossary/) y la [guía de actualización](/docs/guides/updates/).

{{< details title="Fuentes" closed="true" >}}
Contrastado con XO@e281c536: [importación de ISO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [asistente de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [pestañas de VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) y [control de expulsión de CD](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js); [parches aplicados en xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
