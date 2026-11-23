---
title: Primeros pasos
weight: 1
translationKey: getting-started
---

Instale el hipervisor, abra XO Lite y despliegue XOA-hl para administrar sus máquinas virtuales.
{class="lead"}

<span id="start-overview"></span>

## ¿Qué es XCP-hl? {#what-is-xcp-hl}

XCP-hl es una distribución para laboratorios domésticos basada en XCP-ng 8.3. Se ejecuta directamente sobre su hardware y aloja sus máquinas virtuales. **XO Lite** es la pequeña interfaz de gestión que sirve el host. **XOA-hl** es una máquina virtual independiente que ejecuta Xen Orchestra, la interfaz web de administración de sus hosts y VM.

XO Lite ofrece cuatro opciones de appliance: **XOA-hl** (predeterminada), el appliance oficial de Vates, la imagen de Ronivay o una imagen XVA personalizada. Esta guía sigue la opción XOA-hl. Consulte las diferencias en [Características](/docs/features).

<span id="start-requirements"></span>

## Antes de empezar {#before-you-begin}

- Utilice un equipo dedicado compatible con XCP-ng 8.3, con la virtualización por hardware activada. Consulte los [requisitos del proyecto original](https://docs.xcp-ng.org/installation/requirements/) para CPU, memoria y compatibilidad de red.
- Haga una copia de seguridad de los datos de los discos que vaya a utilizar. **La instalación borra los discos seleccionados.**
- Prevea al menos **100 GB** en el disco de instalación para la biblioteca ISO automática de 20 GB de XCP-hl, además de espacio para sus VM. Los discos compatibles de menor tamaño usan la distribución original sin esta biblioteca. Consulte [Almacenamiento ISO](/docs/features#iso-storage).
- Prepare una dirección IP de administración estable, puerta de enlace, DNS y NTP. Una dirección estática o una reserva DHCP facilita encontrar el host.
- Disponga de otro ordenador con navegador y acceso por red al host. El despliegue del appliance también necesita acceso a la URL de la imagen elegida.

{{< callout type="warning" >}}
XCP-hl es software en fase beta destinado a laboratorios domésticos y pruebas. Lea las notas de publicación y espere cambios entre versiones. Conserve las copias de seguridad fuera del host.
{{< /callout >}}

<span id="start-download"></span>

## Descargar y verificar {#download--verify}

{{< latest-iso-download text="Descargar la última ISO" shaText="Suma de comprobación SHA256" >}}

<span id="start-verification"></span>

### Verificar la ISO {#verify-the-iso}

Descargue la suma de comprobación y su firma de la misma publicación y utilice la clave pública del proyecto enlazada abajo. Verifique la huella antes de confiar en ella: **2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A**. El nombre histórico de la clave es `XCP-ng Community Edition (Master signing key)`.

{{< verify-iso >}}

Graba la ISO en una unidad USB con una herramienta de escritura de imágenes o móntela como medio de instalación virtual. La escritura borra la unidad USB; compruebe qué dispositivo ha seleccionado.

<span id="start-quick-start"></span>

## Inicio rápido {#quick-start}

<span id="start-install"></span>

### 1 · Instalar XCP-hl {#1--install-xcp-hl}

Esta es una **configuración inicial adecuada para un laboratorio doméstico con un solo host**, adaptada de la [guía de primera instalación de XCP-ng del autor](https://www.xcp-hl.org/blog/20260107/xcp-ng-first-install.html). Adapte los discos, el almacenamiento y la red a sus necesidades. Las fotografías siguientes muestran XCP-ng 8.3 original; las etiquetas pueden ser diferentes en XCP-hl. La [guía de instalación original](https://docs.xcp-ng.org/installation/install-xcp-ng/) describe otras opciones.

1. **Arranque el instalador y seleccione la distribución del teclado.** Lea la advertencia de instalación y el acuerdo de licencia antes de continuar.

   {{< screenshot src="install/keyboard.jpg" alt="Selección de la distribución del teclado en el instalador" >}}

2. **Seleccione el disco del sistema y el de almacenamiento de VM.** Compruebe los nombres de dispositivo y las capacidades. No seleccione el USB de instalación ni un disco cuyos datos quieras conservar.

   {{< screenshot src="install/system-disk.jpg" alt="Selección del disco del sistema" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Selección del disco de almacenamiento de máquinas virtuales" >}}

3. **Elija el tipo de almacenamiento.** El aprovisionamiento fino EXT es un punto de partida práctico para un laboratorio doméstico: los discos virtuales consumen espacio conforme se escriben datos. LVM reserva su capacidad asignada. Elija según sus cargas de trabajo y vigile el espacio libre con cualquiera de las opciones.

   {{< screenshot src="install/storage-type.jpg" alt="Elección entre almacenamiento EXT y LVM" >}}

4. **Utilice Local media como origen de instalación.** Ejecute la verificación del medio cuando se ofrezca, especialmente si sospecha que la descarga o el USB están dañados.

   {{< screenshot src="install/source.jpg" alt="Selección de Local media como origen de instalación" >}}

5. **Establezca y guarde la contraseña de root.** Utilizará esta cuenta para iniciar sesión en XO Lite y conectar el host a Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Configuración de la contraseña root del host" >}}

6. **Configure la red de administración y DNS.** Utilice una dirección estática o una reserva DHCP; configure una VLAN solo si su red la requiere. Introduzca el nombre del host y servidores DNS accesibles.

   {{< screenshot src="install/network.jpg" alt="Configuración de la IP de administración y la puerta de enlace" >}}
   {{< screenshot src="install/dns.jpg" alt="Configuración del nombre del host y los servidores DNS" >}}

7. **Configure la zona horaria y los servidores NTP, y revise la instalación.** Utilice un servidor NTP interno si el host no puede acceder a servidores públicos. Confirme los discos seleccionados antes de iniciar la instalación.

   {{< screenshot src="install/ntp.jpg" alt="Configuración de la sincronización horaria" >}}
   {{< screenshot src="install/confirm.jpg" alt="Confirmación final de la instalación" >}}

8. **Finalice, retire el medio de instalación y reinicie.** Anote la dirección de administración que aparece en la consola del host.

   {{< screenshot src="install/complete.jpg" alt="Instalación terminada, lista para reiniciar" >}}

<span id="start-open-xo-lite"></span>

### 2 · Abrir XO Lite {#2--open-xo-lite}

Abra `https://<your-host-ip>` en su navegador. Al principio, el host utiliza un certificado autofirmado: confirme que está conectándose a su propio host antes de aceptarlo. Inicie sesión como `root` con la contraseña establecida durante la instalación.

El host ya sirve XO Lite; no hay ninguna VM de XO Lite independiente que instalar.

<span id="start-deploy-xoa"></span>

### 3 · Desplegar XOA {#3--deploy-xoa}

Haga clic en **Deploy XOA** en XO Lite y elija **XOA-hl**. Rellene los campos de red y despliegue del formulario, revise la imagen y las credenciales seleccionadas e inicie el despliegue. Espere a que arranque la VM del appliance y obtenga una dirección. Cambie las contraseñas predeterminadas proporcionadas al iniciar sesión por primera vez.

El xoa-proxy del host transmite la imagen XVA seleccionada a XAPI, que crea la VM del appliance. La imagen de XOA-hl se resuelve en el momento del despliegue, independientemente de la versión de la ISO.

<span id="start-connect-host"></span>

### 4 · Conectar XO al host {#4--connect-xo-to-your-host}

Abra la dirección del appliance XOA-hl en su navegador. En Xen Orchestra, utilice `Settings → Servers → Add server`, introduzca la dirección del host y sus credenciales root y confirme la conexión. El appliance tiene su propia dirección, distinta de la dirección XO Lite del host.

Una vez conectado, compruebe el host y el almacenamiento en Xen Orchestra, suba una ISO de instalación a la biblioteca ISO y cree su primera VM.

<span id="start-updates"></span>

### 5 · Mantenerlo actualizado {#5--keep-it-up-to-date}

Las actualizaciones del host y del appliance son operaciones independientes. Utilice la pestaña **Patches** del host para XCP-hl y **Settings → XOA-HL Updates** para XOA-hl. Lea la [guía de actualizaciones](/docs/guides/updates) antes de iniciar cualquiera de las operaciones.

<span id="start-architecture"></span>

## Resumen de la arquitectura {#architecture-at-a-glance}

{{< architecture >}}

Su navegador puede conectarse directamente a **XO Lite en el host** o a **Xen Orchestra dentro de la VM XOA-hl**. XOA-hl administra el host mediante XAPI. Las demás VM invitadas se ejecutan junto a XOA-hl, no dentro de ella.

<span id="start-components"></span><span id="start-license"></span>

## Licencia {#license}

XCP-hl se publica bajo **AGPL-3.0** y se basa en XCP-ng y Xen Orchestra. Es un proyecto comunitario independiente, sin afiliación, aprobación ni soporte de Vates SAS o del proyecto XCP-ng.
