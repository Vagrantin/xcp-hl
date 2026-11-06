---
title: "Configurar el servicio del dispositivo virtual"
linkTitle: "Configuración del servicio"
description: "Localizar los archivos de configuración del servicio, comprobar las vías de acceso y el certificado HTTPS y aplicar un cambio de forma segura."
weight: 91
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:cf10324c828a27039571b3a119cc1feacd94fbe74d8a0815a3060736e0c32685
glossaryTerms: ["appliance", "host", "pool"]
---

Localiza los archivos de configuración de xo-server del dispositivo virtual XOA-HL, comprueba su acceso de administración y su certificado HTTPS y aplica un cambio de forma segura. Trabaja como root en una consola dentro del dispositivo virtual, con otra consola independiente preparada. Estos archivos son independientes de los ajustes y registros que exporta la interfaz web.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261022-a280852`, el paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; todavía no se ha probado en un laboratorio.
{{< /callout >}}

## Localizar los archivos de configuración {#settings-files}

| Ubicación | Contenido | Cómo tratarla |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` y `sample.config.toml` | Valores predeterminados del paquete y un ejemplo comentado | Solo lectura. Una actualización del paquete sustituye estos archivos |
| `/root/.config/xo-server/config.toml` | Tus propios ajustes (archivo del operador). Se crea durante la instalación solo si no existe | Guarda una copia privada antes de editarlo. La instalación del paquete conserva este archivo |
| `/root/.config/xo-server/config.z-auto.json` | Ajustes que escribe el propio servidor | Comprueba si existe al buscar valores sobrescritos. No lo sobrescribas a ciegas |
| Base de datos Redis | Registros de la aplicación XO | Utiliza la exportación e importación de la interfaz web dentro de su alcance documentado |
| `/etc/xoa-hl/update.conf` | Modo, programación y canal de las actualizaciones del dispositivo virtual | Utiliza **Settings → XOA-HL Updates** y la guía de actualización |
| `/opt/xo/xoahl.crt` y `xoahl.key` | Certificado TLS y clave privada del dispositivo virtual | Conserva una copia independiente. Nunca adjuntes la clave privada a un informe |

El servicio systemd distribuido se ejecuta como root y lee la configuración de usuario en `/root/.config`. xo-server también lee `/etc/xo-server/config.*` y los archivos locales `.xo-server.*`, y combina varios archivos. Antes de decidir qué valor se aplica, comprueba si hay ajustes personalizados del servicio y otros archivos de configuración. Esta página solo aborda el servicio distribuido, no una cuenta de servicio personalizada.

La [exportación de configuración](/docs/xoa-hl/configuration-backup/) no incluye tu archivo TOML, los archivos TLS ni los ajustes de actualización. Para ellos, consulta [mantenimiento del dispositivo virtual](/docs/xoa-hl/maintenance/) y [actualizaciones](/docs/guides/updates/).

## Establecer la URL del dispositivo virtual para descubrir pools {#public-url}

`http.publicUrl` establece la URL del dispositivo virtual que XO registra en cada pool conectado para su descubrimiento. No crea un punto de escucha, un certificado ni un registro DNS. Utiliza una URL HTTPS real del dispositivo virtual, con DNS coincidente y un certificado de confianza, y comprueba primero que se abre en un navegador. Lee [Hosts y pools](/docs/xoa-hl/hosts-pools/) antes de cambiarla.

Pruébalo en un dispositivo virtual de laboratorio que puedas reconstruir. Añade la propiedad a la tabla `[http]` **existente**. Este ejemplo mínimo conserva el punto de escucha HTTPS y la dirección de Redis distribuidos. No sustituye un archivo que hayas personalizado:

```toml
[http]
publicUrl = "https://xoa.lab.example"

[[http.listen]]
port = 443
cert = "/opt/xo/xoahl.crt"
key = "/opt/xo/xoahl.key"

[redis]
uri = "redis://127.0.0.1:6379/0"
```

No añadas una segunda tabla `[http]` ni elimines el punto de escucha existente. Conserva las rutas reales del certificado y de la clave. El paquete crea su propio certificado autofirmado y su clave durante la instalación; no distribuye una clave compartida. Si falta la clave, el certificado o el marcador `/var/lib/xoa-hl/tls-generated`, se genera una pareja nueva. Anota el estado de TLS instalado antes de actualizar. No se abordan aquí la sustitución del certificado, los proxies inversos ni el traslado de Redis.

## Identificar las vías de administración antes de restringir la red {#management-network}

Esta comprobación solo lee; no cambia nada. La configuración distribuida escucha HTTPS en el puerto `443`. Tus ajustes, un proxy, un cortafuegos o una imagen diferente pueden cambiar la vía real. La interfaz web no configura reglas de cortafuegos por ti.

**Antes de empezar**

- Acuerda con los responsables de la red y de los hosts los clientes, subredes, servicios y destinos de copia de seguridad autorizados para administración.
- Acuerda una vía independiente de acceso a consola a la que no afecte la restricción.
- Hazlo antes de cambiar cualquier ACL, VIF, PIF del host o política del switch.

| Vía | Qué anotar y comprobar |
| --- | --- |
| Navegador autorizado → XOA-HL | Anota la VM del dispositivo virtual y su dirección, el nombre resuelto, el endpoint HTTPS real y la identidad del certificado. Desde un cliente autorizado, vuelve a iniciar sesión y comprueba la lista de hosts. El punto de escucha distribuido es `443`, pero comprueba la configuración instalada y el endpoint real. `http.publicUrl` solo anuncia una dirección; no abre un puerto. |
| XOA-HL → hosts y pools | En **Settings → Servers**, anota la dirección del servidor conectado, los identificadores esperados del pool y del host, y cómo se trata el certificado. Comprueba la lista de hosts en vivo y, si ya las has probado en el laboratorio, las [estadísticas de hosts](/docs/xoa-hl/hosts-pools/#host-statistics) recientes de solo lectura. Iniciar sesión en el navegador no demuestra por sí solo que el dispositivo virtual llegue a los hosts. |
| Navegador → consola a través de XOA-HL → host de la VM | Si necesitas la consola, abre una VM de prueba en ejecución con la [guía de consola](/docs/xoa-hl/vm-operations/#vm-console). Anota el resultado en el navegador y el host donde se ejecuta la VM. La consola utiliza una conexión WebSocket independiente desde el dispositivo virtual a ese host; una lista de hosts que funciona no la demuestra. |
| XOA-HL → remotos de copia de seguridad y actualizaciones | Enumera cada remoto de copia de seguridad y los servicios de paquetes, DNS y hora del dispositivo virtual, con sus responsables. Prueba un remoto con su [procedimiento de copia de seguridad](/docs/xoa-hl/backup-restore/) y el acceso a paquetes con la [guía de actualización del dispositivo virtual](/docs/xoa-hl/maintenance/). Un inicio de sesión web correcto no demuestra estas vías. |

En un dispositivo virtual de laboratorio cuya versión hayas identificado:

1. Para cada vía necesaria, anota el cliente de origen, el nombre o la dirección de destino, el servicio, el resultado y la hora.
2. Pide al responsable de la red que compruebe que un cliente de prueba no autorizado no pueda acceder a la página web de inicio de sesión, con una prueba permitida y registros independientes. Un ping bloqueado no demuestra ni aislamiento HTTPS ni que la administración siga funcionando.
3. Mantén el acceso a consola fuera de la vía que piensas restringir.
4. Si se aprueba por separado un cambio de política, modifica una regla controlada por su responsable cada vez. Después de cada cambio, repite las mismas pruebas permitidas y denegadas.
5. Antes de cerrar la ventana de mantenimiento, comprueba el inicio de sesión, la lista de hosts, la consola y las copias de seguridad.

**Comprobación:** todas las vías necesarias siguen funcionando y el cliente no autorizado no puede acceder a la página de inicio de sesión.

Si falla una vía necesaria o pierdes acceso, detente. Utiliza el procedimiento de reversión documentado del responsable de la red a través de la consola independiente. No elimines la conexión de XOA ni cambies la PIF de administración del host como atajo. No se abordan aquí los puntos de escucha reales, la segmentación de clientes, las vías de proxy y NAT, los puertos de hosts y remotos ni la reversión. No construyas una lista de permitidos para producción basándote solo en esta página.

## Comprobar el certificado HTTPS antes de sustituirlo {#tls-certificate-preflight}

Esta comprobación solo lee archivos y conexiones; no renueva nada. Durante la instalación, la configuración distribuida escribe un punto de escucha HTTPS en el puerto `443` que utiliza `/opt/xo/xoahl.crt` y `/opt/xo/xoahl.key`. Los cambios posteriores o un proxy inverso pueden servir TLS desde otro lugar.

El paquete no distribuye una clave privada compartida. Durante la instalación genera una pareja autofirmada `CN=xoa.local` si falta alguno de los archivos o el marcador `/var/lib/xoa-hl/tls-generated`. Una actualización posterior del paquete puede regenerar la pareja del mismo modo y reinicia `xo-server` después (`%posttrans`). Anota las rutas reales y el estado del paquete antes de planificar una renovación. Nunca elimines el marcador para rotar el certificado.

1. Asegúrate de disponer de una consola independiente y de una cuenta de administrador local.
2. Anota de forma privada la imagen y el paquete instalados, los valores efectivos de `http.listen` y cualquier ajuste sobrescrito por la configuración combinada. Ejecuta `systemctl cat xo-server` para ver los ajustes del servicio.
3. Anota si hay un proxy inverso, un balanceador de carga u otro endpoint TLS delante del dispositivo virtual. `http.publicUrl` solo anuncia una dirección: no muestra el punto de escucha ni el certificado que ven los navegadores. Detente si encuentras varios puntos de escucha o algo inesperado en el puerto `443`.
4. En el **dispositivo virtual**, lee únicamente los metadatos del certificado, la clave y el marcador configurados. Para las rutas distribuidas, estos comandos de solo lectura muestran los modos de archivo y los campos públicos del certificado sin imprimir la clave privada:

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   Si tu configuración utiliza otros archivos, utiliza la pareja **realmente configurada**. Si falta un archivo o el marcador, detente y averigua por qué antes de actualizar o reiniciar; no generes una pareja nueva. No incluyas la clave privada ni la configuración completa en capturas, registros o incidencias.
5. Desde un **cliente autorizado**, abre la dirección HTTPS real y vuelve a iniciar sesión en una nueva sesión del navegador.
6. Si OpenSSL está disponible y el responsable te ha proporcionado la cadena de confianza, ejecuta `openssl s_client -connect <name>:<port> -servername <name> -verify_hostname <name> -verify_return_error -brief </dev/null` con el nombre DNS y el puerto reales. Para una CA privada, añade el `-CAfile <ca-path>` aprobado por el responsable. Comprueba la versión de OpenSSL instalada antes de utilizar estas opciones.
7. Compara la huella digital, el nombre, la cadena y la fecha de caducidad del certificado con el endpoint esperado.

**Comprobación:** has anotado el certificado que recibe el navegador y los archivos de los que procede. El certificado autofirmado creado durante la instalación puede no superar la comprobación de confianza: anota ese resultado, pero no desactives la verificación ni afirmes que es un certificado de confianza. Si un proxy gestiona TLS, su certificado puede diferir del archivo del dispositivo virtual; anota ambos por separado.

**Antes de planificar una sustitución**, acuerda con los responsables del certificado y del dispositivo virtual:

- la nueva cadena de certificados, su clave privada correspondiente, los nombres que cubre y su fecha de caducidad;
- el almacenamiento seguro, el propietario de los archivos y sus permisos;
- una consola de recuperación independiente y una copia privada de la **pareja de certificado y clave, el marcador y el archivo del operador** actuales;
- una ventana de mantenimiento después de que terminen los trabajos, el punto de escucha o proxy exacto que se cambiará y un procedimiento probado de reinicio y reversión;
- las pruebas posteriores: un nuevo inicio de sesión en navegador con confianza TLS, la huella correcta, un administrador local operativo, la lista de hosts y pools, y la consola.

Un archivo de configuración válido, los archivos presentes o un reinicio correcto no demuestran que los clientes confíen en el certificado ni que sea el adecuado. No se aborda aquí la renovación del certificado: no utilices esta comprobación como procedimiento de sustitución en producción.

## Comprobar la sintaxis y reiniciar el servicio {#apply-change}

**Antes de empezar**

- Conserva una copia privada del archivo original del operador fuera del dispositivo virtual y anota sus permisos.
- Ten preparado el acceso a consola.
- Espera a que terminen los trabajos de copia de seguridad, restauración y administración.

Después de editar el archivo, ejecuta esta comprobación dentro del dispositivo virtual como root:

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` solo significa que la sintaxis es válida. No comprueba los permisos de archivo, la confianza TLS, los valores combinados ni la accesibilidad. Corrige cualquier error antes de reiniciar.

En la ventana de mantenimiento acordada, reinicia el servicio y lee su estado y su registro reciente:

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

El reinicio desconecta la interfaz web. Vuelve a conectarte en la dirección esperada.

**Comprobación:** puedes iniciar sesión y la lista de hosts está completa. XO escribe su URL en cada pool a intervalos regulares, por lo que debes comprobar el descubrimiento del pool después de la siguiente actualización.

Si el servicio no arranca, restaura el archivo del operador guardado mediante la consola, comprueba de nuevo su sintaxis y reinicia una vez. Si el resultado no está claro, consulta [solución de problemas](/docs/xoa-hl/troubleshooting/). Elimina los secretos de los registros antes de compartirlos.

{{< details title="Fuentes" closed="true" >}}
- **Archivos de configuración y servicio**: [script de configuración inicial](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [instalación y actualización del paquete](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [servicio systemd](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [cargador de configuración](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [ajustes predeterminados](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [ejemplo comentado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [descubrimiento de pools](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).
- **Acceso de administración**: [conexión del servidor](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [proxy de consola hacia el host de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **Certificado HTTPS**: [pareja generada, marcador y reinicio tras una actualización](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [punto de escucha inicial](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [configuración del punto de escucha efectivo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [manual de OpenSSL x509](https://docs.openssl.org/3.0/man1/openssl-x509/), [manual de OpenSSL s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/).
{{< /details >}}
