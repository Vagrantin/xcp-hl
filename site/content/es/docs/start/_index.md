---
title: Primeros pasos
weight: 1
translationKey: getting-started
---

Instala el hipervisor, abre XO Lite y despliega XOA-hl para administrar tus máquinas virtuales.
{class="lead"}

<span id="start-overview"></span>

## ¿Qué es XCP-hl? {#what-is-xcp-hl}

XCP-hl es una distribución para laboratorios domésticos basada en XCP-ng 8.3. Se ejecuta directamente sobre tu hardware y aloja tus máquinas virtuales. **XO Lite** es la pequeña interfaz de gestión que sirve el host. **XOA-hl** es una máquina virtual independiente que ejecuta Xen Orchestra, la interfaz web de administración de tus hosts y VM.

XO Lite ofrece cuatro opciones de appliance: **XOA-hl** (predeterminada), el appliance oficial de Vates, la imagen de Ronivay o una imagen XVA personalizada. Esta guía sigue la opción XOA-hl. Consulta las diferencias en [Características](/docs/features).

<span id="start-requirements"></span>

## Antes de empezar {#before-you-begin}

- Utiliza un equipo dedicado compatible con XCP-ng 8.3, con la virtualización por hardware activada. Consulta los [requisitos del proyecto original](https://docs.xcp-ng.org/installation/requirements/) para CPU, memoria y compatibilidad de red.
- Haz una copia de seguridad de los datos de los discos que vayas a utilizar. **La instalación borra los discos seleccionados.**
- Prevé al menos **100 GB** en el disco de instalación para la biblioteca ISO automática de 20 GB de XCP-hl, además de espacio para tus VM. Los discos compatibles de menor tamaño usan la distribución original sin esta biblioteca. Consulta [Almacenamiento ISO](/docs/features#iso-storage).
- Prepara una dirección IP de administración estable, puerta de enlace, DNS y NTP. Una dirección estática o una reserva DHCP facilita encontrar el host.
- Dispón de otro ordenador con navegador y acceso por red al host. El despliegue del appliance también necesita acceso a la URL de la imagen elegida.

{{< callout type="warning" >}}
XCP-hl es software en fase alfa destinado a laboratorios domésticos y pruebas. Lee las notas de publicación y espera cambios entre versiones. Conserva las copias de seguridad fuera del host.
{{< /callout >}}

<span id="start-download"></span>

## Descargar y verificar {#download--verify}

{{< latest-iso-download text="Descargar la última ISO" shaText="Suma de comprobación SHA256" >}}

<span id="start-verification"></span>

### Verificar la ISO {#verify-the-iso}

Descarga la suma de comprobación y su firma de la misma publicación y utiliza la clave pública del proyecto enlazada abajo. Verifica la huella antes de confiar en ella: **2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A**. El nombre histórico de la clave es `XCP-ng Community Edition (Master signing key)`.

{{< verify-iso >}}

Graba la ISO en una unidad USB con una herramienta de escritura de imágenes o móntala como medio de instalación virtual. La escritura borra la unidad USB; comprueba qué dispositivo has seleccionado.

<span id="start-quick-start"></span>

## Inicio rápido {#quick-start}

<span id="start-install"></span>

### 1 · Instalar XCP-hl {#1--install-xcp-hl}

Esta es una **configuración inicial adecuada para un laboratorio doméstico con un solo host**, adaptada de la [guía de primera instalación de XCP-ng del autor](https://vagrantin.github.io/blog/20260107/xcp-ng-first-install.html). Adapta los discos, el almacenamiento y la red a tus necesidades. Las fotografías siguientes muestran XCP-ng 8.3 original; las etiquetas pueden ser diferentes en XCP-hl. La [guía de instalación original](https://docs.xcp-ng.org/installation/install-xcp-ng/) describe otras opciones.

1. **Arranca el instalador y selecciona la distribución del teclado.** Lee la advertencia de instalación y el acuerdo de licencia antes de continuar.

   {{< screenshot src="install/keyboard.jpg" alt="Selección de la distribución del teclado en el instalador" >}}

2. **Selecciona el disco del sistema y el de almacenamiento de VM.** Comprueba los nombres de dispositivo y las capacidades. No selecciones el USB de instalación ni un disco cuyos datos quieras conservar.

   {{< screenshot src="install/system-disk.jpg" alt="Selección del disco del sistema" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Selección del disco de almacenamiento de máquinas virtuales" >}}

3. **Elige el tipo de almacenamiento.** El aprovisionamiento fino EXT es un punto de partida práctico para un laboratorio doméstico: los discos virtuales consumen espacio conforme se escriben datos. LVM reserva su capacidad asignada. Elige según tus cargas de trabajo y vigila el espacio libre con cualquiera de las opciones.

   {{< screenshot src="install/storage-type.jpg" alt="Elección entre almacenamiento EXT y LVM" >}}

4. **Utiliza Local media como origen de instalación.** Ejecuta la verificación del medio cuando se ofrezca, especialmente si sospechas que la descarga o el USB están dañados.

   {{< screenshot src="install/source.jpg" alt="Selección de Local media como origen de instalación" >}}

5. **Establece y guarda la contraseña de root.** Utilizarás esta cuenta para iniciar sesión en XO Lite y conectar el host a Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Configuración de la contraseña root del host" >}}

6. **Configura la red de administración y DNS.** Utiliza una dirección estática o una reserva DHCP; configura una VLAN solo si tu red la requiere. Introduce el nombre del host y servidores DNS accesibles.

   {{< screenshot src="install/network.jpg" alt="Configuración de la IP de administración y la puerta de enlace" >}}
   {{< screenshot src="install/dns.jpg" alt="Configuración del nombre del host y los servidores DNS" >}}

7. **Configura la zona horaria y los servidores NTP, y revisa la instalación.** Utiliza un servidor NTP interno si el host no puede acceder a servidores públicos. Confirma los discos seleccionados antes de iniciar la instalación.

   {{< screenshot src="install/ntp.jpg" alt="Configuración de la sincronización horaria" >}}
   {{< screenshot src="install/confirm.jpg" alt="Confirmación final de la instalación" >}}

8. **Finaliza, retira el medio de instalación y reinicia.** Anota la dirección de administración que aparece en la consola del host.

   {{< screenshot src="install/complete.jpg" alt="Instalación terminada, lista para reiniciar" >}}

<span id="start-open-xo-lite"></span>

### 2 · Abrir XO Lite {#2--open-xo-lite}

Abre `https://<your-host-ip>` en tu navegador. Al principio, el host utiliza un certificado autofirmado: confirma que estás conectándote a tu propio host antes de aceptarlo. Inicia sesión como `root` con la contraseña establecida durante la instalación.

El host ya sirve XO Lite; no hay ninguna VM de XO Lite independiente que instalar.

<span id="start-deploy-xoa"></span>

### 3 · Desplegar XOA {#3--deploy-xoa}

Haz clic en **Deploy XOA** en XO Lite y elige **XOA-hl**. Rellena los campos de red y despliegue del formulario, revisa la imagen y las credenciales seleccionadas e inicia el despliegue. Espera a que arranque la VM del appliance y obtenga una dirección. Cambia las contraseñas predeterminadas proporcionadas al iniciar sesión por primera vez.

El xoa-proxy del host transmite la imagen XVA seleccionada a XAPI, que crea la VM del appliance. La imagen de XOA-hl se resuelve en el momento del despliegue, independientemente de la versión de la ISO.

<span id="start-connect-host"></span>

### 4 · Conectar XO al host {#4--connect-xo-to-your-host}

Abre la dirección del appliance XOA-hl en tu navegador. En Xen Orchestra, utiliza `Settings → Servers → Add server`, introduce la dirección del host y sus credenciales root y confirma la conexión. El appliance tiene su propia dirección, distinta de la dirección XO Lite del host.

Una vez conectado, comprueba el host y el almacenamiento en Xen Orchestra, sube una ISO de instalación a la biblioteca ISO y crea tu primera VM.

<span id="start-updates"></span>

### 5 · Mantenerlo actualizado {#5--keep-it-up-to-date}

Las actualizaciones del host y del appliance son operaciones independientes. Utiliza la pestaña **Patches** del host para XCP-hl y **Settings → XOA-HL Updates** para XOA-hl. Lee la [guía de actualizaciones](/docs/guides/updates) antes de iniciar cualquiera de las operaciones.

<span id="start-architecture"></span>

## Resumen de la arquitectura {#architecture-at-a-glance}

{{< architecture >}}

Tu navegador puede conectarse directamente a **XO Lite en el host** o a **Xen Orchestra dentro de la VM XOA-hl**. XOA-hl administra el host mediante XAPI. Las demás VM invitadas se ejecutan junto a XOA-hl, no dentro de ella.

<span id="start-components"></span><span id="start-license"></span>

## Licencia {#license}

XCP-hl se publica bajo **AGPL-3.0** y se basa en XCP-ng y Xen Orchestra. Es un proyecto comunitario independiente, sin afiliación, aprobación ni soporte de Vates SAS o del proyecto XCP-ng.
