---
title: "Automatizar con xo-cli"
linkTitle: "Automatización (xo-cli)"
description: "Consultar el inventario con xo-cli mediante un token de corta duración y revocarlo después."
weight: 92
translationKey: xoa-manual-automation
translationStatus: reviewed
sourceRevision: sha256:8ca25fc0552174edc36e7bc5cb4328012f391a79fd91e6a3584debc5deffbb99
glossaryTerms: ["appliance", "host", "vm"]
---

Utiliza el cliente de línea de comandos xo-cli incluido en el dispositivo virtual para consultar un pequeño inventario con un token de corta duración y revocarlo después. Realiza esta prueba antes de escribir automatizaciones que modifiquen una VM. Ejecuta los comandos en una consola dentro del **dispositivo virtual XOA-HL** y revoca el token desde un navegador con la sesión del mismo usuario de prueba.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261022-a280852`, el paquete `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2), con `xo-cli` **0.32.2** y `xo-lib` **0.11.1**. Probado en un dispositivo virtual de laboratorio el 27 de octubre de 2026.
{{< /callout >}}

## 1. Preparar la consola y la confianza TLS {#prepare}

**Antes de empezar**

- Comprueba la versión instalada como se explica en [mantenimiento del dispositivo virtual](/docs/xoa-hl/maintenance/).
- Prepara una cuenta de usuario normal para pruebas y una VM de prueba que puedas perder. Comprueba por separado lo que este usuario puede hacer con [Usuarios y permisos](/docs/xoa-hl/permissions/).
- Utiliza un nombre DNS del dispositivo virtual que coincida con su certificado. El certificado autofirmado `xoa.local` creado durante la instalación puede requerir primero ajustes del DNS del laboratorio o del certificado.
- Obtén la CA pública o el certificado del dispositivo virtual como archivo PEM por un canal de confianza. Comprueba su huella digital por otra vía.

1. Abre una nueva sesión Bash dedicada **dentro del dispositivo virtual**. Allí utilizarás el `/usr/local/bin/xo-cli` incluido.
2. En el ejemplo de la siguiente sección, sustituye la ruta del archivo PEM, la URL y la dirección de correo electrónico por las tuyas.

`NODE_EXTRA_CA_CERTS` añade tu certificado a la lista de confianza; el nombre del servidor se sigue comprobando. Si falla la comprobación TLS, corrige el nombre o el certificado. Nunca la omitas con `--allowUnauthorized` ni `NODE_TLS_REJECT_UNAUTHORIZED=0`.

## 2. Registrar un token de corta duración {#register-token}

Los siguientes comandos guardan las credenciales en una carpeta temporal nueva, sin modificar la configuración existente de xo-cli. `umask 077` hace que solo tú puedas leer el nuevo archivo.

- `register` solicita la contraseña. No la añadas como argumento ni incluyas nunca un token en una URL.
- Si la cuenta usa códigos de un solo uso (OTP), añade `--otp CODE` antes de la URL con un código vigente.

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

El token solicita deliberadamente `1 hour`. De forma predeterminada, el servidor concede 30 días a un token, con un máximo de medio año; su configuración puede cambiar estos límites. Si pides más que el máximo, el registro falla con un error genérico (`unknown error from the peer`); pide una duración más corta.

El token tiene todos los permisos de su usuario: no está limitado a la lectura. Trata la carpeta de configuración como una contraseña. No la incluyas en trazas de consola, copias de seguridad adjuntas a incidencias ni sistemas de control de versiones. El registro crea un token de inicio de sesión; los siguientes comandos solo leen datos.

## 3. Descubrir y consultar el inventario {#read-inventory}

Ejecuta estos comandos. Coloca las opciones como `--json` y `--id` antes de los parámetros.

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| Comando | Resultado |
| --- | --- |
| `list-commands xo.getAllObjects` | Los parámetros del método en un formato legible. Ver un método no significa que tengas permiso para utilizarlo |
| `system.getServerVersion --json` | La versión del paquete del servidor, `"5.193.1"` en esta versión. No es la versión de XO (5.113.2) |
| `list-objects --id --name_label --power_state type=VM` | Un array JSON que solo contiene estas propiedades. No cambia el estado de ninguna VM |
| `xo.getAllObjects --json …` | Un objeto JSON cuyas claves son los identificadores de objeto, filtrado por tipo de objeto y limitado a un objeto |

El prefijo `json:` envía un valor con tipo: `limit=json:1` envía un número, mientras que `limit=1` envía una cadena. El último comando envía esta solicitud JSON-RPC mediante un **WebSocket a `/api/`** (no es un HTTP POST):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

En esta versión, cualquier cuenta con sesión iniciada puede leer todo el inventario a través de la API, incluso una cuenta sin ningún permiso. Los filtros y los campos seleccionados solo determinan lo que ves: **no son límites de acceso**. No supongas que la API devuelve únicamente los objetos mostrados en la interfaz web del usuario ni que los campos omitidos de la salida nunca se consultaron. Mantén los resultados privados y comprueba por separado lo que la cuenta puede ver realmente. Un nombre no es un identificador estable. Este resultado limitado no es un inventario completo ni una forma fiable de seleccionar una VM.

## 4. Revocar el token y limpiar {#revoke-token}

1. En otra sesión del navegador, iniciada con el mismo usuario de prueba, selecciona el icono de usuario del menú para abrir **User** (`/#/user`).
2. En **Authentication tokens**, elimina el token de este cliente CLI.
3. De vuelta en la consola, ejecuta el primer comando siguiente antes de eliminar nada localmente. Debe fallar con un error de autenticación y un código de salida distinto de cero.
4. Si tiene éxito, el token no está revocado. Detente y comprueba la cuenta y sus tokens antes de afirmar que la revocación funcionó.
5. Ejecuta los demás comandos para eliminar las credenciales locales y cierra la consola dedicada.

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

**Comprobación:** después de eliminar el token en el navegador, el comando de versión falla con un error de autenticación.

`unregister` solo elimina las entradas locales `server` y `token`; **no** revoca el token en el servidor. Eliminar la carpeta temporal es únicamente una limpieza local: no sustituye la revocación. Una automatización permanente necesita su propio diseño para el almacenamiento de secretos, la renovación, la revocación, el tratamiento de errores y unos permisos estrictamente limitados; eso no se aborda aquí.

{{< details title="Fuentes" closed="true" >}}
- **Cliente de línea de comandos**: [xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [dónde guarda el cliente su configuración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js).
- **Tokens e inventario**: [API de tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [caducidad de los tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [API de inventario](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [tokens en la página de usuario](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
{{< /details >}}
## Ejercicio de modificación con CLI y JSON-RPC (RF01) {#mutating-example}

Alcance: XO 5.113.2 `e281c536`, XOA-HL ce47 y el xo-cli 0.32.2 incluido. Completa antes el registro de confianza descrito arriba. Usa una **VM detenida** desechable, anota su UUID exacto y su descripción, y concede al usuario de prueba normal **Admin solo sobre esa VM**. Mantén un segundo administrador para revocar el permiso de prueba. No elijas el objetivo de una modificación por su nombre ni con `limit=1`.

1. Sustituye `VM_UUID` en cada comando por el UUID anotado de la VM desechable. Confirma de forma independiente en la interfaz web el UUID, el estado detenido y la descripción original. Descubre `vm.set` y lee el objeto exacto antes de cambiarlo.
2. Cambia solo la descripción y compruébalo en el navegador y con una nueva consulta de inventario. La CLI usa `id`, mientras que `vm.start` tiene otro contrato de parámetros; no deduzcas los nombres a partir de otros métodos.

```bash
xoa_cli list-commands vm.set
xoa_cli xo.getAllObjects --json 'filter=json:{"id":"VM_UUID"}'
xoa_cli vm.set --json id=VM_UUID name_description=rf01-disposable-test
xoa_cli xo.getAllObjects --json 'filter=json:{"id":"VM_UUID"}'
```

La modificación corresponde a este mensaje JSON-RPC en el WebSocket autenticado `/api/`:

```json
{"jsonrpc":"2.0","id":2,"method":"vm.set","params":{"id":"VM_UUID","name_description":"rf01-disposable-test"}}
```

3. Restaura la descripción original anotada con `vm.set`, usando un argumento `name_description=...` entre comillas. Vuelve a leerla de forma independiente; comprueba que el estado de energía, los discos y las VIF no han cambiado.
4. Como administrador, retira solo el permiso Admin de prueba de este usuario (asegúrate de que no quede ningún otro permiso). Repite la misma solicitud de descripción. Debe fallar con un estado de salida de la CLI distinto de cero y dejar la descripción sin cambios. Una respuesta RPC correcta normal puede estar vacía; la relectura es obligatoria.
5. Revoca el token y limpia la configuración temporal del cliente como se indica arriba. Tras un tiempo de espera agotado, una desconexión o un error, lee el objeto antes de reintentar: el servidor puede haber aplicado ya una escritura. No reintentes a ciegas una modificación destructiva.

**Comprobación:** se observan el cambio de descripción permitido y su restauración; la misma solicitud sin el permiso se rechaza sin modificar la VM. Esto demuestra un único contrato de modificación, no la seguridad general de la automatización ni la confidencialidad del inventario. Se siguen necesitando pruebas funcionales en una instalación antes de marcar este ejercicio como probado.

Implementación fijada: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [packages/xo-cli/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [packages/xo-server/src/xo-mixins/acls.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs).

**Resultado de laboratorio, 3 de noviembre de 2026 (CLI superada, revocación pendiente):** En el dispositivo virtual de laboratorio, xo-cli 0.32.2 cambió la descripción de una VM detenida desechable, la relectura coincidió y se restauró el texto original. Tras retirar el permiso Admin del usuario, la misma solicitud falló (`not enough permissions`, código de salida 1) y una relectura independiente en el host no mostró cambios. Requisitos observados: el certificado del laboratorio (`CN=xoa.local`, sin SAN) necesitó una asignación de nombre para `xoa.local` más la CA fijada, sin omitir TLS. `register` pide la contraseña en un terminal y falla sin él (`tty.setRawMode is not a function`), por lo que la prueba usó `--token`. `token.delete` llamado por una cuenta sin permiso fue rechazado, así que no se verificó la revocación en el navegador y esta fila sigue abierta.
