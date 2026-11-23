---
title: "Iniciar sesión, conectar un host y elegir un idioma"
linkTitle: "Primer inicio de sesión"
description: "Iniciar sesión en XOA-HL, establecer su contraseña, elegir el idioma de la interfaz y conectar el host."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: reviewed
sourceRevision: sha256:fada0c60468337a6ff9bac62459262ad822b14b101201fd2ccba51590aa4909a
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

Al terminar esta guía, podrá iniciar sesión en XOA-HL, su host estará conectado y la interfaz utilizará su idioma.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261027-ca44911`, el paquete `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Probado en un dispositivo virtual de laboratorio el 27 de octubre de 2026. Las imágenes anteriores y las actualizaciones posteriores pueden diferir. Recompilada el 27 de octubre de 2026 con la corrección de aprovisionamiento de `build-xoa-hl@fa0c987`. Consulte [cómo identificar el archivo corregido](/docs/xoa-hl/first-login/#identify-the-rebuilt-image).
{{< /callout >}}

Este procedimiento de inicio de sesión supone el formulario de despliegue de XO Lite. Una instalación RPM directa en AlmaLinux es otro artefacto: el dispositivo virtual de laboratorio ce51 expuso una cuenta de administrador predeterminada antes del aprovisionamiento por parte del operador ([#368](https://github.com/Vagrantin/xcp-hl/issues/368)). Mantenga aislado ese punto de acceso y establezca una credencial de administrador única antes de permitir el acceso de administración. Los pasos de credenciales del formulario de despliegue que siguen no se aplican a esa instalación RPM.

## Antes de empezar {#before-you-begin}

- [Despliegue XOA-HL desde XO Lite](/docs/start/#start-deploy-xoa). Anote la etiqueta de la imagen y la dirección del dispositivo virtual.
- Conserve el usuario y la contraseña del administrador de XO que introdujo en el formulario de despliegue. También necesita la dirección de administración del host y su contraseña de `root`.
- Utilice un navegador en una red de administración de confianza.

La mayoría de los pasos se realizan en su **navegador**. La comprobación de la imagen usa una consola root dentro del dispositivo virtual. La limpieza de despliegues antiguos o incompletos usa una consola root en el host.

| Dirección o cuenta | Para qué sirve |
| --- | --- |
| Dirección de administración del host | XO Lite y la conexión del servidor en XOA-HL |
| Dirección del dispositivo virtual XOA-HL | La interfaz web de Xen Orchestra |
| Cuenta de administrador de XO | Iniciar sesión en Xen Orchestra |
| Cuenta `root` del host | Permitir que Xen Orchestra administre el host |
| Cuenta del sistema `xo` del dispositivo virtual | Solo acceso SSH; no es la cuenta web |

## 1. Abrir el dispositivo virtual e iniciar sesión {#1-open-the-appliance-and-sign-in}

1. Abra `https://<appliance-address>`. Utilice la dirección del dispositivo virtual, no la del host.
2. Si el navegador advierte de un certificado autofirmado, compruebe que la dirección corresponde a su dispositivo virtual antes de aceptarlo. Si cambia el certificado de una instalación existente, averigüe primero por qué.
3. Espere a que termine el primer arranque. Después inicie sesión con la **cuenta de administrador de XO del formulario de despliegue**. No utilice la cuenta `root` del host ni la cuenta SSH del dispositivo virtual.

**Comprobación:** se abre la interfaz de Xen Orchestra. Es normal que el inventario esté vacío hasta que conecte un host.

{{< callout type="warning" >}}
En las imágenes compiladas antes de la corrección de aprovisionamiento del 27 de octubre de 2026, un primer arranque fallido puede dejar la cuenta web como `admin@admin.net` con la contraseña `admin`. Pruébela solo en una red de confianza y cambie su contraseña inmediatamente. En la imagen recompilada, use su cuenta de despliegue. Si falla, revise los servicios de aprovisionamiento descritos más abajo. No suponga que la cuenta predeterminada debe funcionar.
{{< /callout >}}

## 2. Establecer una contraseña definitiva {#2-set-a-password-you-will-keep}

1. Seleccione el **icono de usuario** del menú para abrir **User** (`/#/user`).
2. En la sección de contraseña, introduzca la contraseña actual y después la nueva dos veces. Utilice una contraseña exclusiva. Seleccione **OK**.
3. Guarde la nueva contraseña de forma segura. Cierre la sesión y vuelva a iniciarla con la nueva contraseña.

**Comprobación:** puede iniciar sesión con la nueva contraseña. Esto solo cambia la cuenta web. No cambian la contraseña de `root` del host ni la contraseña SSH del dispositivo virtual.

{{< callout type="warning" >}}
Estos problemas afectan a las imágenes compiladas antes de la corrección de aprovisionamiento del 27 de octubre de 2026, incluida `qa-xoa-build-58.xva` (SHA-256 que empieza por `5f8427fd`). No describen un despliegue correcto de la imagen recompilada que se identifica más abajo:

- **Reinicie el dispositivo virtual una vez.** Después de cambiar la contraseña, reinicie normalmente la VM del dispositivo virtual desde XO Lite (**Restart**, no un reinicio forzado). Hasta que el dispositivo virtual haya guardado su configuración, un corte de corriente o una parada forzada pueden devolver la cuenta `admin@admin.net` con la contraseña `admin`, y su propia cuenta se pierde. Por el mismo motivo, nunca conserve una instantánea de un dispositivo virtual en ejecución como estado bueno conocido.
- **Elimine las credenciales que deja el despliegue.** La configuración de la VM en el host puede conservar credenciales de despliegue en texto claro. Tras verificar el acceso, use el procedimiento de limpieza siguiente y después cambie la contraseña web y, si SSH está habilitado, la contraseña SSH de `xo` con `passwd`.
{{< /callout >}}

### Identificar la imagen recompilada {#identify-the-rebuilt-image}

El archivo corregido es `qa-xoa-build-59.xva` de la publicación `xoa-image-20261027-ca44911`. Su SHA-256 es `cc20b9398d5ab0dc03eae6706d3b54236e2d245fa1d0dd1232d59836387057aa`. Se compiló a partir de `build-xoa-hl@fa0c987`. El archivo anterior usaba la misma etiqueta y las mismas cadenas de versión en About.

Dentro del dispositivo virtual, ejecute esta comprobación de solo lectura como **root**, desde su consola o una sesión SSH autorizada:

```bash
redis-cli config get appendonly
```

En la imagen recompilada, el resultado es `appendonly` seguido de `yes`. La imagen anterior devuelve `no`. Esto comprueba el ajuste actual de Redis. Una imagen modificada manualmente o personalizada también puede devolver `yes`; conserve el nombre original del archivo y su suma de comprobación como identidad de la imagen.

La imagen recompilada guarda la cuenta de despliegue antes de marcar la configuración como terminada. Los cambios posteriores usan el archivo de solo anexado (AOF) de Redis, que se guarda cada segundo. Una parada forzada aún puede perder aproximadamente el último segundo de cambios. Use un dispositivo virtual apagado normalmente para una instantánea de referencia.

### Limpiar despliegues antiguos o incompletos {#clean-up-older-or-incomplete-deployments}

Antes de eliminar claves, espere a que el dispositivo virtual haya aplicado las cuentas y a poder iniciar sesión tanto con las credenciales web previstas como, si está habilitado, con las credenciales SSH. Use el UUID exacto de la VM del dispositivo virtual. En una **consola root en el host XCP-HL**, compruebe cada clave por separado sin mostrar su valor:

```bash
for key in admin-account system-account-xoa-password xoa-updater-credentials; do
  if xe vm-param-get uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key" >/dev/null 2>&1; then
    xe vm-param-remove uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key"
  fi
done
```

Es normal que falte una clave; investigue cualquier error al eliminarla. No vuelque el mapa `xenstore-data` completo en un registro o informe. Los registros antiguos del primer arranque, las exportaciones de VM y las copias de seguridad de metadatos del pool pueden seguir conteniendo las contraseñas de despliegue. Cambie las contraseñas web y SSH proporcionadas en el despliegue y proteja o retire esas copias antiguas. Eliminar las claves actuales no borra las copias históricas.

Mantenga abierta la pestaña de despliegue de XO Lite hasta que termine. En la imagen recompilada, la limpieza dentro del invitado también eliminó `vm-data/admin-account` y `vm-data/system-account-xoa-password` del `xenstore-data` persistente de XAPI tras el primer arranque. Esto se observó en un host XCP-HL v8.3 en [#311](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771). No suponga el mismo resultado para imágenes antiguas, imágenes de Vates, Ronivay o personalizadas, ni para despliegues fallidos o abandonados. Compruebe y elimine las claves restantes en el host como se indica arriba, una vez aplicadas las cuentas. La corrección de limpieza de XO Lite de [#310](https://github.com/Vagrantin/xcp-hl/issues/310) cubre también otros orígenes de imagen. Una actualización RPM de la aplicación por sí sola no sustituye los scripts de aprovisionamiento de una imagen antigua.

En las imágenes recompiladas con las correcciones de #310/#311, un fallo de captura en el primer arranque impide deliberadamente la conexión de red; XO Lite puede indicar "XOA not responding" sin dirección IP. Desde la consola de la VM, revise `systemctl status xoa-first-boot.service` y `/var/log/xoa-first-boot.log`. Estas imágenes requieren un correo electrónico y una contraseña de administrador completos desde XO Lite; importar el XVA sin esos datos no se acepta en silencio. Corrija los datos de aprovisionamiento antes de reiniciar y conserve las claves de credenciales hasta que la captura tenga éxito. Si la captura tuvo éxito pero no se aplicaron las credenciales, revise `systemctl status xoa-credentials.service` y vuelva a ejecutar ese servicio después de corregir la causa. No copie en los informes el archivo `/etc/xoa-first-boot.env`, legible solo por root.

## 3. Elegir el idioma de la interfaz {#3-choose-the-interface-language}

1. Abra **icono de usuario → User → Language**.
2. Seleccione su idioma. Las etiquetas cambian inmediatamente.

Este ajuste solo cambia la interfaz de XOA-HL. La documentación tiene su propio selector de idioma en la parte superior de esta página. Algunas etiquetas del dispositivo virtual podrían no estar traducidas todavía. La dirección `/#/user` siempre abre esta pantalla.

## 4. Conectar el host {#4-connect-the-host}

1. Abra **Settings → Servers** (`/#/settings/servers`). Si su host ya aparece y está conectado, compruebe su inventario en vez de añadirlo otra vez.
2. En el formulario, introduzca una etiqueta clara, la **dirección IP de administración o el nombre del host**, el usuario `root` y la contraseña del host establecida durante la instalación. No introduzca la dirección del dispositivo virtual.
3. Seleccione **Connect**. Si aparece una advertencia de certificado autofirmado, compruebe primero que realmente se trata de su host. Después acepte el certificado de este servidor.
4. Compruebe si la fila del servidor muestra un indicador de error. Después abra el inventario y compruebe que aparecen el pool, el host y los repositorios de almacenamiento (SR). **Enabled** solo significa que la conexión está habilitada. No significa que funcione.

**Comprobación:** aparecen el host y su almacenamiento, sin errores de conexión. Ya puede [crear su primera VM](/docs/xoa-hl/create-vm/).

## 5. Anotar las versiones instaladas {#5-note-the-installed-versions}

Abra **About** (`/#/about`) como administrador. Anote **XOA-HL version** y **XOA-HL VM version** y consérvelas junto con el nombre original del archivo, su suma de comprobación y la etiqueta de la imagen. Los dos archivos del 27 de octubre de 2026 tienen las mismas cadenas de versión en About. Use la comprobación de la imagen anterior para distinguir sus ajustes predeterminados de Redis. Las actualizaciones de paquetes pueden cambiar posteriormente la versión de la aplicación.

La [matriz de versiones](/docs/reference/release-matrix/) enumera lo distribuido en cada versión. No registra resultados de pruebas.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| No se abre la página del dispositivo virtual | En XO Lite, compruebe que su VM esté en ejecución. Después compruebe su dirección, red y puerta de enlace, y que el navegador pueda acceder a ella. No vuelva a desplegar encima de una VM que funciona. |
| No funcionan las credenciales de despliegue | Espere a que termine el primer arranque y compruebe que ha usado la cuenta web. En la imagen recompilada, revise los servicios de aprovisionamiento descritos arriba. En una imagen antigua, pruebe la cuenta de respaldo solo en una red de confianza. Tras una parada forzada temprana, una imagen antigua puede haber perdido su cuenta: cambie la contraseña de respaldo y vuelva a crear su cuenta. Lea `/var/log/xoa-first-boot.log` desde una consola o sesión SSH autorizada. Elimine los datos privados antes de compartirlo. |
| Falla el inicio de sesión en el host | Compruebe la dirección del host y su contraseña de `root`. La contraseña del administrador web es diferente. |
| El servidor muestra un error de certificado | Compruebe la identidad del host antes de aceptar su certificado autofirmado. No acepte un cambio que no pueda explicar. |
| El servidor está habilitado, pero el inventario está vacío | Lea el error de conexión. Compruebe que el dispositivo virtual pueda acceder al host y que la dirección del host sea correcta. Que su navegador llegue al host no demuestra que el dispositivo virtual pueda hacerlo. |

## Siguientes pasos {#next-steps}

[Cree su primera VM](/docs/xoa-hl/create-vm/) o lea la [guía de actualización del dispositivo virtual y del host](/docs/guides/updates/).

{{< details title="Fuentes" closed="true" >}}
Contrastado con: [versión de la imagen](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261027-ca44911); [configuración de credenciales en build-xoa-hl@fa0c987](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-credentials.sh); [pantalla de usuario en XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [pantalla de servidores de la misma versión](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [parche de la página About de XOA-HL en xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
- [build-xoa-hl@fa0c987: AOF](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-finalize-state.sh)
- [#311: 27 de octubre de 2026](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771)
{{< /details >}}
