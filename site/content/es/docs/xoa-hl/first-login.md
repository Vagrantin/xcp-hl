---
title: "Iniciar sesión, conectar un host y elegir un idioma"
linkTitle: "Primer inicio de sesión"
description: "Iniciar sesión en XOA-HL, establecer tu contraseña, elegir el idioma de la interfaz y conectar el host."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: draft
sourceRevision: sha256:90b1070b91657a68c53df68d8927605d523fbc946c6b8cf0e3a2fa30a113e037
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

Al terminar esta guía, podrás iniciar sesión en XOA-HL, tu host estará conectado y la interfaz utilizará tu idioma.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261022-a280852` (Xen Orchestra 5.113.2). Basado en el código publicado; todavía está pendiente una ejecución completa en un dispositivo virtual de prueba. Las imágenes anteriores y las actualizaciones posteriores pueden diferir.
{{< /callout >}}

## Antes de empezar {#before-you-begin}

- [Despliega XOA-HL desde XO Lite](/docs/start/#start-deploy-xoa). Anota la etiqueta de la imagen y la dirección del dispositivo virtual.
- Conserva el usuario y la contraseña del administrador de XO que introdujiste en el formulario de despliegue. También necesitas la dirección de administración del host y su contraseña de `root`.
- Utiliza un navegador en una red de administración de confianza.

Todos los pasos se realizan en tu **navegador**. No necesitas una consola en el host ni en el dispositivo virtual.

| Dirección o cuenta | Para qué sirve |
| --- | --- |
| Dirección de administración del host | XO Lite y la conexión del servidor en XOA-HL |
| Dirección del dispositivo virtual XOA-HL | La interfaz web de Xen Orchestra |
| Cuenta de administrador de XO | Iniciar sesión en Xen Orchestra |
| Cuenta `root` del host | Permitir que Xen Orchestra administre el host |
| Cuenta del sistema `xo` del dispositivo virtual | Solo acceso SSH; no es la cuenta web |

## 1. Abrir el dispositivo virtual e iniciar sesión {#1-open-the-appliance-and-sign-in}

1. Abre `https://<appliance-address>`. Utiliza la dirección del dispositivo virtual, no la del host.
2. Si el navegador advierte de un certificado autofirmado, comprueba que la dirección corresponde a tu dispositivo virtual antes de aceptarlo. Si cambia el certificado de una instalación existente, averigua primero por qué.
3. Espera a que termine el primer arranque. Después inicia sesión con la **cuenta de administrador de XO del formulario de despliegue**. No utilices la cuenta `root` del host ni la cuenta SSH del dispositivo virtual.

**Comprobación:** se abre la interfaz de Xen Orchestra. Es normal que el inventario esté vacío hasta que conectes un host.

{{< callout type="warning" >}}
En esta imagen, si el primer arranque no logra establecer tus credenciales, la cuenta web puede seguir siendo `admin@admin.net` con la contraseña `admin`. Si tu cuenta no funciona en un dispositivo virtual nuevo, prueba esta cuenta de respaldo únicamente en tu red de confianza. Si funciona, cambia inmediatamente la contraseña en el paso 2. Si ninguna cuenta funciona, deja de intentarlo y utiliza la tabla de solución de problemas al final de esta página.
{{< /callout >}}

## 2. Establecer una contraseña definitiva {#2-set-a-password-you-will-keep}

1. Selecciona el **icono de usuario** del menú para abrir **User** (`/#/user`).
2. En la sección de contraseña, introduce la contraseña actual y después la nueva dos veces. Utiliza una contraseña exclusiva. Selecciona **OK**.
3. Guarda la nueva contraseña de forma segura. Cierra la sesión y vuelve a iniciarla con la nueva contraseña.

**Comprobación:** puedes iniciar sesión con la nueva contraseña. Esto solo cambia la cuenta web. No cambian la contraseña de `root` del host ni la contraseña SSH del dispositivo virtual.

## 3. Elegir el idioma de la interfaz {#3-choose-the-interface-language}

1. Abre **icono de usuario → User → Language**.
2. Selecciona tu idioma. Las etiquetas cambian inmediatamente.

Este ajuste solo cambia la interfaz de XOA-HL. La documentación tiene su propio selector de idioma en la parte superior de esta página. Algunas etiquetas del dispositivo virtual podrían no estar traducidas todavía. La dirección `/#/user` siempre abre esta pantalla.

## 4. Conectar el host {#4-connect-the-host}

1. Abre **Settings → Servers** (`/#/settings/servers`). Si tu host ya aparece y está conectado, comprueba su inventario en vez de añadirlo otra vez.
2. En el formulario, introduce una etiqueta clara, la **dirección IP de administración o el nombre del host**, el usuario `root` y la contraseña del host establecida durante la instalación. No introduzcas la dirección del dispositivo virtual.
3. Selecciona **Connect**. Si aparece una advertencia de certificado autofirmado, comprueba primero que realmente se trata de tu host. Después acepta el certificado de este servidor.
4. Comprueba si la fila del servidor muestra un indicador de error. Después abre el inventario y comprueba que aparecen el pool, el host y los repositorios de almacenamiento (SR). **Enabled** solo significa que la conexión está habilitada. No significa que funcione.

**Comprobación:** aparecen el host y su almacenamiento, sin errores de conexión. Ya puedes [crear tu primera VM](/docs/xoa-hl/create-vm/).

## 5. Anotar las versiones instaladas {#5-note-the-installed-versions}

Abre **About** (`/#/about`) como administrador. Anota **XOA-HL version** y **XOA-HL VM version** y consérvalas junto con la etiqueta de la imagen. La versión de la VM identifica la compilación de la imagen. Las actualizaciones de paquetes pueden cambiar posteriormente la versión de la aplicación.

La [matriz de versiones](/docs/reference/release-matrix/) enumera lo distribuido en cada versión. No registra resultados de pruebas.

## Si algo falla {#if-something-goes-wrong}

| Problema | Qué comprobar |
| --- | --- |
| No se abre la página del dispositivo virtual | En XO Lite, comprueba que su VM esté en ejecución. Después comprueba su dirección, red y puerta de enlace, y que el navegador pueda acceder a ella. No vuelvas a desplegar encima de una VM que funciona. |
| No funcionan las credenciales de despliegue | Espera a que termine el primer arranque y comprueba que has usado la cuenta web. Después prueba la cuenta de respaldo anterior. Si puedes abrir la consola del dispositivo virtual o una sesión SSH, lee `/var/log/xoa-first-boot.log`. Elimina los datos privados antes de compartirlo. |
| Falla el inicio de sesión en el host | Comprueba la dirección del host y su contraseña de `root`. La contraseña del administrador web es diferente. |
| El servidor muestra un error de certificado | Comprueba la identidad del host antes de aceptar su certificado autofirmado. No aceptes un cambio que no puedas explicar. |
| El servidor está habilitado, pero el inventario está vacío | Lee el error de conexión. Comprueba que el dispositivo virtual pueda acceder al host y que la dirección del host sea correcta. Que tu navegador llegue al host no demuestra que el dispositivo virtual pueda hacerlo. |

## Siguientes pasos {#next-steps}

[Crea tu primera VM](/docs/xoa-hl/create-vm/) o lee la [guía de actualización del dispositivo virtual y del host](/docs/guides/updates/).

{{< details title="Fuentes" closed="true" >}}
Contrastado con: [versión de la imagen](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261022-a280852); [configuración de credenciales en build-xoa-hl@fc7ebfa](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh); [pantalla de usuario en XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [pantalla de servidores de la misma versión](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [parche de la página About de XOA-HL en xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
{{< /details >}}
