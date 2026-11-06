---
title: "Instalar las herramientas de invitado Linux"
linkTitle: "Herramientas del invitado"
description: "Instalar el agente de administración dentro de una VM Linux y comprobar lo que muestra XOA-HL."
weight: 41
translationKey: xoa-manual-guest-tools
translationStatus: draft
sourceRevision: sha256:b33c81ebb5d81c67bc786f64145b80c80a063e3836134f53b46590995ecf327e
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Instala el agente de administración dentro de una VM Linux, comprueba lo que XOA-HL informa sobre ella y prueba un apagado normal. El agente se ejecuta en el invitado, no en XOA-HL. Los pasos utilizan como ejemplo un invitado Ubuntu 24.04 porque se comprobó su paquete; otras distribuciones Linux proporcionan el agente mediante sus propios paquetes. Utiliza el **dispositivo virtual XOA-HL** en el navegador con una sesión de administrador y ejecuta los comandos en la consola del invitado. Sigue las secciones en orden. Otros sistemas, incluido Windows, necesitan su propio procedimiento.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261022-a280852`, el paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; todavía no se ha probado en un laboratorio. Paquete del invitado: `xe-guest-utilities` `7.20.2-0ubuntu1` para Ubuntu 24.04 LTS (Noble), amd64.
{{< /callout >}}

## Antes de empezar {#before-you-begin}

- Utiliza una VM de prueba Ubuntu 24.04 amd64 recién instalada y sin datos valiosos, por ejemplo la de [Crear tu primera VM](/docs/xoa-hl/create-vm/). Necesitas una consola que funcione y una cuenta del invitado que pueda utilizar `sudo`.
- Anota el UUID completo de la VM, su host, el sistema operativo y el kernel del invitado, y las versiones instaladas del host y del dispositivo virtual. El nombre de una plantilla no indica por sí solo qué sistema operativo está instalado.
- Utiliza una cuenta de administrador de XOA-HL. Arrancar y detener una VM requiere el permiso **operate** sobre ella. Administrar paquetes en el invitado es un permiso independiente: iniciar sesión en XOA-HL no te concede `sudo` en el invitado.
- Planifica una ventana de mantenimiento para probar el apagado. Guarda el trabajo en el invitado y excluye la VM de los trabajos programados. Antes de modificar un invitado importante, haz una [copia de seguridad independiente y prueba una restauración aislada](/docs/xoa-hl/backup-restore/).
- El invitado necesita DNS operativo, la hora correcta y acceso a sus repositorios Ubuntu Noble aprobados, incluido `universe`. Utiliza una red de laboratorio autorizada. No cambies la red de administración del host para acceder a un servidor de paquetes. Esta guía no añade repositorios ni utiliza una ISO de herramientas.

Ejecuta los comandos de esta página únicamente **en la consola del invitado**, nunca en el host XCP-HL ni en el dispositivo virtual XOA-HL. Lee el estado de la VM y utiliza sus botones de encendido y apagado en el **navegador**, en la dirección del dispositivo virtual.

## Comprobar el estado de las herramientas del invitado {#guest-tools-status}

1. En el navegador, abre la VM con el UUID que anotaste y comprueba que esté **Running**.
2. Abre **General** (`/#/vms/<id>/general`). Anota el modo de virtualización, el mensaje sobre las herramientas y la dirección IP mostrada.
3. Abre **Advanced** y busca **Guest OS**. Anota **Management agent version**, **OS name** y **OS kernel**. No cambies nada en estas pestañas.
4. En la consola de la VM, ejecuta estos comandos y anota la salida:

   ```bash
   cat /etc/os-release
   uname -r
   dpkg --print-architecture
   systemd-detect-virt
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl status xe-daemon.service --no-pager
   ```

   Un paquete ausente o un servicio inactivo es un resultado que debes anotar. No es una razón para ejecutar los comandos en otra máquina.

**Comprobación:** el sistema operativo es Ubuntu `24.04`, la arquitectura es `amd64` y `systemd-detect-virt` imprime `xen`. De lo contrario, detente y utiliza un procedimiento escrito para ese sistema. Si las herramientas ya están instaladas, anota el origen del paquete y su versión y pasa a [Comprobar lo que muestra XOA-HL](#check-reporting). No las reinstales ni actualices solo para coincidir con este ejemplo.

### Qué significa el mensaje de las herramientas {#what-the-tools-message-means}

El mensaje de **General** solo aparece cuando la VM está **Running** y XO dispone de información sobre los controladores. XO comprueba primero los controladores PV, después el agente de administración y, por último, si el agente está actualizado. Muestra el primer mensaje aplicable:

| Mensaje | Significado |
| --- | --- |
| **No Xen tools detected** | No se detectan los controladores PV |
| **Management agent not detected** | Se detectan los controladores, pero no el agente |
| **Management agent {version} out of date** | Se detecta el agente, pero se informa de que no está actualizado |
| **Management agent {version} detected** | Se detecta el agente y se informa de que está actualizado |

La ausencia de mensaje no demuestra que las herramientas estén instaladas. Detectar un agente no comprueba tus aplicaciones, la conectividad ni la seguridad.

Los controladores PV del kernel Linux y el agente de administración (un programa en el invitado) cumplen funciones diferentes. El siguiente paquete Ubuntu instala el agente; no sustituye los controladores del kernel. La versión del agente en XO procede de las métricas del invitado del host y puede diferir de la versión del paquete Ubuntu. Anota ambas. No vuelvas a una versión anterior ni reinstales solo porque sus formatos sean distintos. Comprueba por separado los controladores, el agente y tus aplicaciones.

## Instalar el agente de administración en un invitado Linux {#install-linux-agent}

Utiliza un invitado que todavía no tenga herramientas instaladas. Si ya utiliza una ISO de herramientas, un agente de un proveedor u otro paquete, averigua primero quién lo mantiene y cómo se actualiza.

1. En la consola del invitado, actualiza las listas de paquetes, comprueba de dónde procedería el paquete y simula la instalación:

   ```bash
   sudo apt-get update
   apt-cache policy xe-guest-utilities
   apt-get -s install xe-guest-utilities
   ```

2. Comprueba que el candidato proceda del repositorio Ubuntu Noble esperado. Esta guía se contrastó con la versión `7.20.2-0ubuntu1`. Revisa cualquier otra versión u origen antes de continuar.
3. Detente si hay un error de repositorio o firma, no hay candidato o se proponen eliminaciones o actualizaciones inesperadas. No omitas la verificación ni añadas un repositorio ajeno.
4. Instala el paquete. Lee los cambios propuestos antes de aceptarlos:

   ```bash
   sudo apt-get install xe-guest-utilities
   ```

5. Habilita y arranca el servicio; después comprueba el paquete y el servicio:

   ```bash
   sudo systemctl enable --now xe-daemon.service
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl is-enabled xe-daemon.service
   systemctl is-active xe-daemon.service
   ```

**Comprobación:** el estado del paquete es `install ok installed` y el servicio está `enabled` y `active`. En Ubuntu Noble, el servicio es **`xe-daemon.service`**. Depende de `proc-xen.mount` y systemd solo lo inicia cuando se cumplen sus condiciones de virtualización Xen y de rutas. No utilices en su lugar el nombre genérico `xe-linux-distribution.service`. Un instalador que termina o un servicio habilitado no demuestra por sí solo que el agente esté ejecutándose. Este paso no requiere reinicio ni elimina ningún paquete.

## Comprobar lo que muestra XOA-HL {#check-reporting}

1. En el navegador, actualiza **General** y **Advanced** de la misma VM en ejecución. Anota el mensaje de herramientas, la versión del agente, el sistema operativo y el kernel.
2. Compara el sistema operativo y el kernel con lo que muestra la consola del invitado.
3. Compara la dirección IP mostrada con la interfaz prevista del invitado y su dirección actual.

Si el mensaje sigue indicando que falta el agente o que no está actualizado mientras `systemctl` indica `active`, el problema no está resuelto. Anota exactamente lo que ves y no marques la prueba como superada.

**No IPv4 record** no demuestra por sí solo que el agente haya fallado: un invitado solo con IPv6 o sin red puede no tener dirección IPv4. Una dirección mostrada no demuestra el funcionamiento del enrutamiento, DNS o acceso SSH o RDP. Comprueba por separado las conexiones que necesita el invitado.

## Probar un apagado normal {#clean-shutdown}

1. Guarda todo el trabajo en el invitado.
2. En el navegador, comprueba de nuevo el UUID de la VM. Selecciona **Stop** una vez y lee la confirmación.
3. Si XO ofrece forzar el apagado u omitir una operación bloqueada, cancela: eso no es un apagado normal. Anota el error. Si el invitado sigue respondiendo, apágalo normalmente desde dentro. No repitas la solicitud mientras haya una tarea en ejecución.
4. Comprueba en la consola que el invitado se apaga y que XOA-HL muestra **Halted** sin tareas de apagado todavía activas.
5. Selecciona **Start** una vez. Inicia sesión por la consola y comprueba tu aplicación o archivo de prueba.
6. Repite las comprobaciones del servicio (`systemctl is-enabled` y `systemctl is-active`) y [Comprobar lo que muestra XOA-HL](#check-reporting).

Anota los resultados de apagado y arranque por separado de la detección del agente: uno no demuestra lo otro.

**Comprobación:** tienes un resultado para cada elemento: el paquete y servicio exactos, la información actualizada en XOA-HL, el apagado normal y el servicio tras el reinicio. Si falta algún resultado o hay un fallo, la prueba no está completa. Esto no prueba la migración en vivo, la memoria dinámica, la conexión en caliente, las instantáneas con aplicaciones en estado consistente, el portapapeles ni el rendimiento.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| Falta el paquete o procede de un origen inesperado | Comprueba el sistema operativo y la versión del invitado, `apt-cache policy`, la disponibilidad del repositorio `universe` autorizado, la hora, el DNS y los errores de actualización. Corrige el repositorio con su responsable. No instales un paquete del host o del dispositivo virtual en el invitado. |
| Falta el servicio, está inactivo o ha fallado | Comprueba el paquete instalado y sus archivos con `dpkg -L xe-guest-utilities`. Lee `systemctl status xe-daemon.service proc-xen.mount --no-pager` y `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager`. Comprueba las condiciones de Xen y los errores de dependencias antes de cambiar cualquier configuración. |
| El servicio está activo, pero XO muestra que falta el agente o que no está actualizado | Comprueba la identidad de la VM, que esté **Running** y la conexión del host. Compara los resultados del paquete y servicio del invitado con **General** y **Advanced**, y la hora de cada uno. No reinicies el hipervisor, ocultes la advertencia ni sustituyas controladores a ciegas. |
| **Stop** falla u ofrece forzar el apagado | Cancela el apagado forzado o la omisión. Conserva el error exacto de la tarea y comprueba la consola del invitado. Apaga desde dentro del invitado si puedes. Un apagado forzado puede perder datos y requiere una decisión aparte. |
| El invitado falla después de un cambio | Conserva el historial de paquetes y los registros de arranque y del servicio. Utiliza la consola del invitado y tu plan de recuperación independiente. Esta guía no promete una reversión automática mediante desinstalación o vuelta a una versión anterior. |

No sigas habilitando, reiniciando o reinstalando para ocultar un fallo sin explicar. [Comunica el problema](/docs/xoa-hl/troubleshooting/#report-a-problem) con las versiones, los identificadores de VM y host, las horas, el origen y la versión del paquete, el estado del servicio, los mensajes exactos y los resultados de las tareas de encendido y apagado. Los registros y las pantallas del invitado pueden contener nombres, direcciones o datos privados: exclúyelos del informe y conserva en privado las pruebas originales.

Para futuras actualizaciones, planifica una ventana de mantenimiento independiente para el sistema operativo y los paquetes del invitado y repite las mismas comprobaciones. No se abordan aquí: otras distribuciones Linux, la instalación desde una ISO de herramientas, las herramientas Windows o BSD, el cambio de proveedor, la actualización o eliminación del paquete ni una lista de invitados admitidos. Después, consulta [Administrar VM](/docs/xoa-hl/vm-operations/) y [Crear una copia de seguridad y restaurar una VM](/docs/xoa-hl/backup-restore/).

{{< details title="Fuentes" closed="true" >}}
- **Estado de herramientas y acciones de encendido y apagado**: [orden de los mensajes de herramientas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [campos del sistema operativo invitado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [correspondencia de métricas del invitado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [confirmaciones de apagado y apagado forzado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permiso operate de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Compilación HomeLab**: [selección de parches en xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Paquete Ubuntu (comprobado el 2026-10-15)**: [paquete `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities), [lista de archivos amd64](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist), [empaquetado Debian](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`).
- **Contexto**: [herramientas de invitado Linux de XCP-ng](https://docs.xcp-ng.org/vms/#linux-guest-tools) (información general, no una declaración de compatibilidad con XCP-HL).
- **Etiquetas de la interfaz**: [catálogos de etiquetas de XO](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl), [respaldo de traducciones de HomeLab](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/compact-xo-locales.py).
{{< /details >}}
