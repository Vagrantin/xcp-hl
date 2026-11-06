---
title: "Proteger el acceso con un código de un solo uso"
linkTitle: "Códigos de un solo uso (OTP)"
description: "Añada un código de un solo uso al acceso de una cuenta, compruébelo y elimínelo de forma segura."
weight: 71
translationKey: xoa-manual-sign-in-otp
translationStatus: draft
sourceRevision: sha256:6cd964ad6c27dba4fac2174ee07db3969f54dcdebe9b7f253e906688f3346a44
glossaryTerms: ["appliance"]
---

XOA-HL puede pedir un código de un solo uso de seis cifras de una aplicación de autenticación después de la contraseña. El código cambia con el tiempo (TOTP). Cada cuenta que accede con contraseña local lo activa para sí misma. Pruébelo primero con una cuenta sin permisos de administrador [creada para esta prueba](/docs/xoa-hl/permissions/).

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio. Las versiones posteriores pueden diferir.
{{< /callout >}}

## Antes de empezar {#prepare}

| Necesita | Por qué |
| --- | --- |
| Una aplicación de autenticación TOTP en un dispositivo bajo su control | Genera los códigos a partir de un secreto compartido |
| La hora correcta en el appliance y en ese dispositivo | XO acepta el código actual y los de los intervalos de 30 segundos inmediatamente anterior y posterior |
| Otro administrador o un plan de recuperación independiente | Sin ello, perder el dispositivo puede bloquear al único administrador |
| Una sesión de navegador que mantendrá abierta durante la prueba | Permite quitar el código si falla la comprobación |

El navegador comprueba el código introducido durante la configuración usando su propio reloj. Al acceder, el appliance comprueba el código con su reloj. Por tanto, que un código sea aceptado al configurarlo no demuestra que la hora del appliance sea correcta.

## Active un código de un solo uso para su cuenta {#enable-otp}

1. Acceda con la cuenta que desea proteger. Abra su página de usuario mediante el icono de usuario del menú (`/#/user`).
2. Busque el interruptor **OTP authentication** y actívelo. El diálogo **Add OTP authentication** muestra un código QR y el secreto como texto.
3. Escanee el QR o escriba el secreto en la aplicación de autenticación. La nueva entrada tiene como emisor `Xen Orchestra` y como nombre el correo o identificador de la cuenta.
4. Introduzca el código actual en **OTP code** y confirme. Si es incorrecto, el diálogo se abre de nuevo: introduzca el código que muestra ahora la aplicación. **Cancel** deja desactivado el código de un solo uso.

Si falta el interruptor, deténgase y anote la versión instalada. Esta compilación usa el plan de código abierto predeterminado de XO, que muestra el interruptor; la causa no es la falta de suscripción. [Informe de la diferencia](/docs/xoa-hl/troubleshooting/).

**Comprobación:** el interruptor está activado y su página de usuario muestra el secreto y su QR al lado. Cualquiera que los vea puede generar códigos válidos: no comparta la página ni haga capturas. Este QR identifica al emisor como `XenOrchestra` (sin espacio) para el mismo secreto. Conserve la entrada que ya tiene en la aplicación; no vuelva a escanearlo.

## Compruebe el acceso en una sesión nueva {#check-sign-in}

1. Mantenga abierta la sesión actual. Abra una ventana privada del navegador y acceda con su usuario y contraseña.
2. Una segunda página pide un **Code**. Introduzca el código actual de la aplicación y seleccione **Sign in**.
3. Un código erróneo o caducado muestra `Invalid code`. Espere al siguiente e inténtelo de nuevo.
4. Compruebe que ha accedido a la cuenta correcta y cierre la ventana privada.

**Comprobación:** el acceso pidió un código y aceptó el correcto. Si sigue fallando, use la sesión abierta para [quitar el código](#remove-otp), compruebe ambos relojes y actívelo de nuevo.

## Lo que no protege un código de un solo uso {#otp-limits}

- Activarlo no termina las sesiones existentes ni revoca tokens. Todo token de autenticación válido omite la comprobación del código, incluso los creados después: los tokens son credenciales independientes. Tras activarlo, abra **Authentication tokens** en su página de usuario y elimine los que no reconozca o ya no necesite. Un script que use un token eliminado dejará de funcionar.
- Solo protege el acceso web de XO para esta cuenta. No protege SSH ni la consola del appliance, XO Lite ni la cuenta root del host, ni otras cuentas de XO.
- Los proveedores externos de acceso y su autenticación multifactor quedan fuera del alcance de esta guía.

## Quite un código de un solo uso {#remove-otp}

- **Su propia cuenta:** en su página de usuario, desactive **OTP authentication** y confirme **Remove OTP authentication**.
- **Otra cuenta, como administrador:** abra **Settings → Users**. En la columna **OTP**, seleccione **Remove** para esa cuenta y confirme. Compruebe primero quién lo solicita, por ejemplo por otro canal. Después el usuario podrá configurar un dispositivo nuevo.

Las cuentas sin código muestran **Not configured** en esa columna. Si el único administrador pierde el dispositivo, la interfaz no ofrece una vía de acceso. Desde la consola del appliance todavía puede [recuperar el acceso de administrador](/docs/xoa-hl/troubleshooting/#recover-admin-access). Es más sencillo tener un segundo administrador: mantenga uno.

**Comprobación:** el interruptor está desactivado y la columna OTP de la cuenta muestra **Not configured**. En una ventana privada nueva, la cuenta accede con su usuario y contraseña locales sin código. Mantenga conectado al administrador de recuperación hasta confirmarlo.

{{< details title="Fuentes" closed="true" >}}
- **Página de usuario y configuración**: [sección OTP de la página de usuario](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js), [página de usuario y tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js), [diálogo de configuración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js), [acciones de activación y eliminación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [columna OTP en ajustes de usuarios](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js).
- **Acceso y tokens**: [páginas de acceso](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [formulario de acceso](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug), [autenticación y omisión por tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [ventana temporal TOTP](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs), [comando de recuperación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [etiquetas de interfaz](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Compilación y configuración del navegador**: [plan predeterminado XO](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [autenticador del navegador](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js), [API de preferencias del usuario](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs), [compilación HomeLab](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
