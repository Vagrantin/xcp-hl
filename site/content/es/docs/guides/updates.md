---
title: Actualizaciones
weight: 3
translationKey: updates
aliases: ["/es/updates.html"]
---

XCP-hl y XOA-hl se actualizan mediante paquetes firmados sin reinstalar para las actualizaciones habituales. El host (XCP-hl) se actualiza desde la pestaña **Patches** de Xen Orchestra, igual que XCP-ng original. El appliance (XOA-hl) se actualiza desde su propia página de ajustes **XOA-HL Updates**.
{class="lead"}

Las dos partes de esta página siguen el mismo esquema: pasos en Xen Orchestra, equivalente por línea de comandos, funcionamiento interno y vuelta a una versión anterior.

## Actualizar XCP-hl (el host del hipervisor) {#updating-xcp-hl-the-host}

{{< callout type="info" >}}
**Se aplica a** la imagen XOA-HL `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Se basa en el código publicado; la instalación de paquetes del host y su reinicio todavía no se han probado en un laboratorio con esta versión.
{{< /callout >}}

### En Xen Orchestra {#in-xen-orchestra}

1. **Comprueba si hay actualizaciones pendientes.** En `Home > Hosts`, un host con actualizaciones pendientes muestra una insignia roja con el número de parches que faltan.

   {{< screenshot src="updates/xcp-hl-1-missing-patches.png" alt="Lista de hosts: una insignia roja cuenta los parches pendientes del host" >}}

2. **Abre la pestaña Patches del host.** Selecciona el host y después **Patches**. La pestaña enumera cada paquete con nombre, descripción, versión, release y tamaño de descarga; el icono del ojo muestra su registro de cambios RPM. La vista del pool, `Home > Pools > <pool> > Patches`, enumera los paquetes pendientes del maestro del pool; comprueba cada host por separado antes de actuar sobre todo el pool.

   {{< screenshot src="updates/xcp-hl-2-patches-tab.png" alt="La pestaña Patches del host con los paquetes disponibles" >}}

3. **Elige el alcance deseado.** En la pestaña Patches del host, **Install all patches** actúa sobre ese host. En la del pool, **Install pool patches** actúa sobre todos los hosts del pool, empezando por el maestro. Comprueba la identidad del host y del pool antes de confirmar cualquiera de las acciones.

   {{< screenshot src="updates/xcp-hl-3-installing.png" alt="La pestaña Patches durante la instalación de los parches del pool" >}}

   {{< callout type="warning" >}}
   Ninguno de los botones selecciona paquetes individuales de XCP-ng. Para cada host seleccionado, `updater.py` ejecuta un único `yum update` sobre los repositorios habilitados de XCP-ng y XCP-hl, por lo que también incluye las actualizaciones pendientes de XCP-ng. Es una operación conjunta de paquetes, no una garantía de reversión atómica. La acción del pool procesa los hosts uno a uno, empezando por el maestro; no evacua las VM ni reinicia los hosts. Para actualizar solo paquetes XCP-hl concretos, utiliza la vía de línea de comandos indicada abajo.
   {{< /callout >}}

4. **Espera a que termine la tarea y actualiza la conexión con el host.** En esta versión de XO, el botón llama al complemento actualizador del host y reinicia después el agente XAPI del host seleccionado tras instalar. Puede producirse una desconexión temporal del host. Este paso no llama al actualizador del appliance XOA-HL ni reinicia `xo-server`. Si la conexión no se recupera, conserva el error e inspecciona el host desde una consola independiente antes de volver a intentarlo.

5. **Verifica el resultado.** Actualiza el inventario del host y pool previstos, el resultado de la tarea, la lista de paquetes/versiones, el número de parches pendientes y la indicación de reinicio necesario. Que desaparezca una insignia no demuestra por sí solo que el host se haya reiniciado ni que los invitados y el almacenamiento estén bien.

   {{< screenshot src="updates/xcp-hl-5-up-to-date.png" alt="La pestaña Patches con el host completamente actualizado" >}}

### Probar una actualización de host en un pool de laboratorio de un solo host {#host-patch-pilot}

Haz tu primera actualización en un pool de laboratorio que puedas reconstruir, no en uno del que dependas. Una prueba con un solo host no demuestra cómo se comporta un pool de varios hosts durante una actualización.

**Antes de empezar**

- Utiliza un **pool de laboratorio de un solo host** cuya versión conozcas, sin VM normales, tareas de copia en ejecución, HA ni appliance XOA-HL ejecutándose en ese host.
- Mantén una consola independiente del host, un plan de recuperación del host y de la red, y una conexión XOA-HL independiente.
- Reserva una ventana aprobada para todo el conjunto de paquetes (originales y HomeLab). Decide el reinicio por separado.

1. Registra las versiones de imagen, paquete y XO anteriores, los UUID del host y del pool, el maestro, la dirección de administración, las versiones de paquetes instalados, los identificadores de repositorio habilitados, los estados de alimentación y habilitación del host y la lista exacta de paquetes pendientes. En la **consola del host**, ejecuta `yum check-update` y compáralo con la pestaña **Patches**. Detente si la comprobación falla o la lista no es la esperada. `yum check-update` puede devolver el estado 100 cuando existen actualizaciones; es normal.
2. En el **navegador de XOA-HL**, abre `/#/hosts/<host-id>/patches`, selecciona **Install all patches**, comprueba el host y confirma una vez. Seleccionar una fila no limita la actualización a ese paquete. Registra el ID de tarea, sus horas de inicio y fin y cualquier salida o error. No vuelvas a pulsar durante una desconexión temporal ni inicies una actualización por línea de comandos al mismo tiempo.
3. Al terminar la tarea, compara con tus notas desde la consola independiente y el inventario XOA-HL actualizado: versiones instaladas, parches restantes, accesibilidad del host, estados de habilitación y alimentación, red de administración y conexiones de SR. Si falla la tarea o no vuelve la conexión, conserva los registros y el estado real de los paquetes. Una actualización parcial requiere el plan de recuperación o reconstrucción del propietario del host; no supongas que se ha revertido.
4. Si la interfaz indica que hace falta reiniciar, planifica un reinicio **independiente**, aprobado, con el pool vacío. Comprueba que no haya aparecido ninguna VM ni tarea de copia y selecciona una vez **Reboot to apply updates** en la pestaña Patches del host. No aceptes indicaciones para forzar el reinicio ni saltarte una suspensión bloqueada, una copia de seguridad o una comprobación de versión. Espera al host desde la consola independiente y comprueba de nuevo la conexión XOA-HL, los paquetes, la indicación de reinicio, la red y los SR. Si el botón o la tarea se comportan de forma inesperada, detente y regístralo. No fuerces un segundo reinicio.

**Comprobación:** el host es accesible, sus paquetes coinciden con las versiones esperadas, no quedan parches ni reinicios pendientes. Conserva las listas de paquetes de antes y después, las salidas de tarea y consola, cualquier error exacto, la decisión sobre el reinicio y la conectividad final. Aquí no se cubren instalaciones interrumpidas, recuperación ni disponibilidad en pools de producción o de varios hosts. El [mantenimiento y la evacuación del host](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) es una tarea aparte con una VM de prueba en ejecución; el botón de parches no la realiza.

### Desde la línea de comandos {#from-the-command-line}

En el host:

```bash
yum check-update                   # what is available
yum update xcp-hl-release          # the repository configuration itself
yum update xo-lite-ce xoa-proxy    # only the XCP-hl packages
yum update                         # everything, as the Patches tab does
```

### Cómo funciona {#how-it-works}

XCP-ng incluye un complemento XAPI, `updater.py`, al que Xen Orchestra solicita la lista de actualizaciones disponibles. XOA-hl está modificado para incluir los repositorios XCP-hl en esa solicitud; por eso aparecen sus paquetes junto a los de XCP-ng.

Los repositorios se definen en un único archivo, `/etc/yum.repos.d/xcp-hl.repo`, propiedad del paquete `xcp-hl-release`:

| ID del repositorio | Contenido | Publicado desde |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{{< callout type="error" >}}
No cambies los nombres de las secciones de ese archivo. Xen Orchestra pasa esos ID a `updater.py`, que solo enumera actualizaciones de los repositorios indicados. Renombrar una sección no provoca ningún error: sus paquetes desaparecen silenciosamente de la pestaña Patches.
{{< /callout >}}

Los ajustes se distribuyen como paquete para que los cambios lleguen a un host instalado, en lugar de depender de un archivo copiado una sola vez. Sus cambios llegan al host mediante `yum update xcp-hl-release`.

### Configuración inicial en un host existente {#first-time-setup-on-an-existing-host}

Los hosts instalados desde una ISO anterior al paquete `xcp-hl-release` necesitan una inicialización única. Después, yum gestiona la configuración.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://vagrantin.github.io/xcp-hl/xcp-hl.repo

rpm --import https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

Al instalar el paquete se sustituye el archivo recién descargado por la copia empaquetada, conservando el tuyo como `xcp-hl.repo.rpmorig`. Solo se diferencian en el origen de la clave de firma: la copia descargada la obtiene mediante HTTPS; la empaquetada utiliza la clave local instalada por el paquete.

Las ISO más recientes ya incluyen `xcp-hl-release`, por lo que este paso no les corresponde.

### Volver a una versión anterior {#rolling-back}

Cada repositorio solo publica sus versiones más recientes, lo que limita hasta dónde puedes retroceder. Para volver a una compilación anterior:

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<version>
```

## Actualizar XOA-hl (la interfaz de administración) {#updating-xoa-hl-the-appliance}

### En Xen Orchestra {#in-xen-orchestra-1}

1. **Abre la página de actualización.** En la interfaz web XOA-hl, ve a `Settings > XOA-HL Updates`. Muestra la versión instalada. Hasta que ejecutes una comprobación, el estado indica *Update status unknown*.

   {{< screenshot src="updates/xoa-hl-1-update-tab.png" alt="La página XOA-HL Updates antes de ejecutar una comprobación" >}}

2. **Pulsa Check for update.** La página enumera todos los paquetes con actualizaciones disponibles y sus versiones.

   {{< screenshot src="updates/xoa-hl-2-check-result.png" alt="Resultado de la comprobación: actualizaciones disponibles y lista de paquetes" >}}

3. **Pulsa Update now.** El registro de actualización se transmite a la página mientras se ejecuta. La actualización reinicia xo-server, por lo que la página muestra brevemente *Reconnecting* y continúa por sí sola.

   {{< screenshot src="updates/xoa-hl-3-in-progress.png" alt="Actualización en curso con su registro en directo" >}}

   {{< callout type="warning" >}}
   **Update now** instala todos los paquetes pendientes del appliance, incluidos AlmaLinux y el kernel, no solo `xoa-hl`. En ce20, el actualizador gestionado excluye Node.js.
   {{< /callout >}}

4. **Terminado.** Al finalizar, vuelve a comprobar: la página indica *Up to date*.

   {{< screenshot src="updates/xoa-hl-4-up-to-date.png" alt="La página XOA-HL Updates indica que el appliance está actualizado" >}}

### Desde la línea de comandos {#from-the-command-line-1}

En el appliance:

```bash
dnf check-update         # what is available
dnf update xoa-hl        # the appliance application only
dnf update --exclude=nodejs  # the application and the AlmaLinux base together
```

### Cómo funciona {#how-it-works-1}

El appliance tiene su propio repositorio yum, definido en `/etc/yum.repos.d/xoa-hl.repo` y propiedad del propio paquete `xoa-hl`:

| ID del repositorio | Contenido | Publicado desde |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

Los dos botones de la página inician dos unidades systemd:

| Unidad | Función |
|---|---|
| `xoa-hl-check-update.service` | Ejecuta `dnf check-update` y escribe el resultado en `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Ejecuta un `dnf -y --refresh --exclude=nodejs update` completo y registra en `/var/lib/xoa-hl/update.log` |

### Comprobaciones y actualizaciones automáticas {#automatic-checks-and-updates}

En `xoa-hl` `v5.113.2_e281c536-ce20`, **Settings → XOA-HL Updates → Automatic updates** ofrece tres modos:

| Modo | Comportamiento |
|---|---|
| Solo manual | Un administrador inicia comprobaciones e instalaciones; es el valor predeterminado. |
| Comprobar automáticamente | Las comprobaciones programadas actualizan el estado; la instalación sigue siendo manual. |
| Instalar automáticamente | Comprueba e instala dentro de la ventana de mantenimiento configurada, tras confirmarlo expresamente. |

Elige la frecuencia, el día (en programación semanal) y la hora local de inicio, y guarda. Las horas utilizan la **zona horaria del appliance**, y las ejecuciones empiezan a la hora fijada sin demora aleatoria. Desde `v5.113.2_e281c536-ce40`, un fallo automático aparece como aviso rojo en la página. Instalar o actualizar el RPM no te inscribe en la instalación automática. Es posible que paquetes antiguos no muestren estos controles; comprueba primero la versión instalada.

El actualizador gestionado excluye Node.js para mantener su versión principal admitida. Las actualizaciones pueden reiniciar servicios, incluido xo-server. **No hay reinicio automático** del sistema; una ventana de instalación perdida no se recupera inmediatamente tras arrancar. Comprueba el resultado y organiza los reinicios necesarios. Consulta la [referencia de programación versionada](https://github.com/Vagrantin/xoa-hl/blob/v5.113.2_e281c536-ce40/docs/automatic-updates.md) para la configuración por línea de comandos y el diagnóstico.

### Volver a una versión anterior {#rolling-back-1}

Los repositorios actualmente habilitados pueden mostrar paquetes antiguos:

```bash
dnf --showduplicates list xoa-hl
```

Su disponibilidad cambia con el tiempo. Para `v5.113.2_e281c536-ce40`, la bajada de versión del paquete y la recuperación de configuración entre versiones no se han validado como procedimientos de recuperación del appliance. Bajar de versión no revierte las actualizaciones del sistema operativo base ni restaura los datos XO y archivos del operador. Prepara una exportación y una prueba de recuperación aislada con la [guía de configuración](/docs/xoa-hl/configuration-backup/) antes de planificar una reversión.

## Verificación y confianza {#verification-and-trust}

Los paquetes y metadatos de repositorio de XCP-hl y XOA-hl se firman con la clave GPG de XCP-hl. La configuración del cliente establece `repo_gpgcheck=1` junto con `gpgcheck=0`.

Los RPM se firman mediante una **subclave** GPG, no la clave maestra, y la herramienta `rpm` del sistema host XCP-ng 8.3 (versión 4.11) tiene una limitación conocida: al importar una clave solo registra la maestra, por lo que informa `NOKEY` para una firma de subclave y no puede verificar directamente el paquete, aunque la firma sea auténtica.

La confianza pasa por los metadatos del repositorio. La herramienta GPG real, que sí entiende subclaves, verifica `repomd.xml`. Ese archivo registra una suma de comprobación de `primary.xml`, que registra a su vez una suma de cada paquete; verificar un único archivo, `repomd.xml`, verifica así todos los RPM del repositorio.

{{< callout type="warning" >}}
Las subclaves de firma caducan el **2027-05-10**. Después, la verificación falla hasta que se amplíen, se actualice la clave publicada y se vuelva a importar en cada host.
{{< /callout >}}

## Limitaciones conocidas {#known-limitations}

Para el alcance del appliance revisado en `v5.113.2_e281c536-ce40`, la recuperación tras interrupciones y el comportamiento de la bajada de versión aún necesitan validación en un laboratorio desechable. Utiliza la [guía de mantenimiento](/docs/xoa-hl/maintenance/) para las comprobaciones del resultado y las decisiones de reinicio.

{{< callout type="info" >}}
Recuerda que esta distribución está en fase alfa. Lee las notas antes de actualizar: se esperan cambios incompatibles en cada versión y una actualización puede requerir intervención manual.
{{< /callout >}}
