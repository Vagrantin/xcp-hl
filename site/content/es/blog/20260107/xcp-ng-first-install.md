---
title: "Guía de primera instalación de XCP-ng"
date: 2026-01-07T09:00:00+09:00
slug: xcp-ng-first-install
translationKey: blog-xcp-ng-first-install
---

La instalación paso a paso del autor para un primer XCP-ng 8.3 upstream, desde el ISO del instalador hasta una appliance de Xen Orchestra desplegada, con fotografías del instalador upstream.
{class="lead"}

{{< callout type="warning" >}}
Esta guía describe **XCP-ng 8.3 upstream**, no XCP-hl. XCP-hl es software alfa basado en XCP-ng 8.3, por lo que las etiquetas del instalador y algunos valores predeterminados pueden diferir en XCP-hl. Las fotografías siguientes muestran el instalador 8.3 upstream.
{{< /callout >}}

## Acerca de esta página

Esta es la guía de primera instalación del autor con XCP-ng 8.3, publicada originalmente en su blog personal el 2026-01-07 y migrada a este sitio el 2026-11-11 según la decisión del propietario registrada en la [PR #409](https://github.com/Vagrantin/xcp-hl/pull/409), para que las páginas de [primeros pasos](/docs/start/) la enlacen en el dominio de producción. Para el procedimiento de XCP-hl (descarga del ISO, verificación de la suma de control, appliance XOA-hl), siga [Primeros pasos](/docs/start/).

## Antes de empezar

- Una máquina dedicada compatible con XCP-ng 8.3, con la virtualización por hardware activada; consulte los [requisitos upstream](https://docs.xcp-ng.org/installation/requirements/).
- Haga una copia de seguridad de los datos de los discos que vaya a usar. **La instalación borra los discos seleccionados.**
- Al menos 100 GB en el disco de instalación, más espacio para sus VM.
- Una dirección IP de gestión, puerta de enlace, DNS y NTP estables. Una dirección estática o una reserva DHCP facilitan encontrar el host.
- Un segundo ordenador con un navegador y acceso de red al host.

## Escribir el ISO en una memoria USB

Descargue el ISO de XCP-ng 8.3 desde la [página de descarga upstream](https://xcp-ng.org/download/) y escríbalo en una memoria USB. La escritura borra la memoria USB, así que compruebe primero con `dmesg` qué dispositivo es la memoria USB y sustituya `sdX` a continuación por ese dispositivo:

```bash
sudo dd if=xcp-ng-8.3.0-20250606.iso of=/dev/sdX bs=8M oflag=direct
```

Vuelva a comprobar el nombre del dispositivo antes de ejecutar el comando: escribir en el disco equivocado lo borra. Espere a que termine la copia; puede tardar según la memoria USB.

## Instalar XCP-ng

XCP-ng es un hipervisor de tipo 1 y está diseñado para ser el único sistema instalado en la máquina. Conecte la memoria USB, arranque desde ella y pulse Intro en el indicador de arranque.

1. **Seleccione su distribución de teclado** y lea el aviso de instalación y el acuerdo de licencia antes de continuar.

   {{< screenshot src="install/keyboard.jpg" alt="Selección de la distribución de teclado del instalador" >}}

2. **Seleccione el disco del sistema y el disco para almacenar las VM.** Compruebe los nombres y capacidades de los dispositivos; no seleccione la memoria USB del instalador ni un disco cuyos datos quiera conservar.

   {{< screenshot src="install/system-disk.jpg" alt="Selección del disco del sistema" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Selección del disco para almacenar las máquinas virtuales" >}}

3. **Elija el tipo de almacenamiento.** EXT (aprovisionamiento thin) solo usa el espacio que sus datos ocupan realmente: un disco virtual de 1 TB con 20 GB de datos ocupa unos 20 GB en el host, a cambio de ir ampliando el archivo del disco a medida que crecen los datos. LVM (aprovisionamiento thick) reserva toda la capacidad desde el principio y evita esa ampliación, a cambio del espacio. EXT es una opción práctica para un laboratorio doméstico; LVM conviene para cargas sensibles al rendimiento. Puede ampliar el disco más tarde desde Xen Orchestra.

   {{< screenshot src="install/storage-type.jpg" alt="Elección entre almacenamiento EXT y LVM" >}}

4. **Use Local media como origen de la instalación** y ejecute la verificación del medio cuando si ofrece, en particular si sospecha que la descarga o la memoria USB están dañadas.

   {{< screenshot src="install/source.jpg" alt="Selección de Local media como origen de la instalación" >}}

5. **Defina y guarde la contraseña de root.** Es la contraseña más importante de la plataforma; guárdela en un lugar seguro. La usará para iniciar sesión en XO Lite y para conectar el host a Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Definición de la contraseña de root del host" >}}

6. **Configure la red de gestión y los DNS.** Use una dirección estática o una reserva DHCP; use una VLAN solo si su red lo requiere. Introduzca el nombre del host y servidores DNS alcanzables. Si la dirección cambiara más adelante, necesitaría un DNS en su laboratorio para volver a encontrar el host.

   {{< screenshot src="install/network.jpg" alt="Configuración de la dirección IP de gestión y la puerta de enlace" >}}
   {{< screenshot src="install/dns.jpg" alt="Configuración del nombre del host y los servidores DNS" >}}

7. **Configure la zona horaria y los servidores NTP, y revise la instalación.** Use servidores NTP públicos si el host tiene acceso a internet, o un servidor NTP interno si no lo tiene. Confirme los discos seleccionados antes de iniciar la instalación.

   {{< screenshot src="install/ntp.jpg" alt="Configuración de la sincronización horaria" >}}
   {{< screenshot src="install/confirm.jpg" alt="Confirmación final de la instalación" >}}

8. **Termine, retire el medio de instalación y reinicie.** Anote la dirección de gestión que aparece en la consola del host.

   {{< screenshot src="install/complete.jpg" alt="Instalación completada, listo para reiniciar" >}}

## Después del primer arranque: XO Lite

La consola del host solo ofrece administración básica de este host (red, VM, recursos, copia de seguridad y restauración). La otra forma de administrar un único host es XO Lite, la interfaz web que sirve el host en el puerto HTTPS predeterminado: abra `https://<ip-de-su-host>` (o `https://<nombre-de-host>`) en su navegador. El host usa inicialmente un certificado autofirmado; confirme que se está conectando a su propio host antes de aceptarlo. Inicie sesión como `root` con la contraseña definida durante la instalación.

## Desplegar XOA

XOA (Xen Orchestra) es la aplicación web que administra uno o varios hosts XCP-ng y sus VM. Se ejecuta como una máquina virtual en el host.

1. En XO Lite, haga clic en **Deploy XOA** y elija la imagen de la appliance. En XCP-hl, la opción predeterminada es **XOA-hl**; consulte [Primeros pasos](/docs/start/).
2. Rellene los campos de red y despliegue del formulario, revise la imagen y las credenciales seleccionadas, y haga clic en **Deploy**.
3. Espere a que la VM de la appliance arranque, abra su dirección en el navegador e inicie sesión. La appliance tiene su propia dirección, distinta de la dirección de XO Lite del host.

Una vez que el host esté conectado en Xen Orchestra (`Settings → Servers → Add server`, con la dirección del host y sus credenciales de root), suba un ISO de instalación a la biblioteca de ISO y cree su primera VM. La [guía de instalación upstream](https://docs.xcp-ng.org/installation/install-xcp-ng/) describe opciones adicionales.
