---
title: "Administrar hosts y pools: incorporación, estadísticas y mantenimiento"
linkTitle: "Hosts y pools"
description: "Compruebe qué appliance administra un pool, lea estadísticas y pruebe incorporación, mantenimiento y HA en hosts de laboratorio."
weight: 60
translationKey: xoa-manual-hosts-pools
translationStatus: draft
sourceRevision: sha256:6ade76bbc4328f8c9c50e11f0871e5809dda89e8f6f6c2d1fda8e5c6c988f73e
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Compruebe qué appliance administra cada pool, transfiera la administración a otro, limpie un botón antiguo de XO Lite, lea estadísticas y pruebe la incorporación a pools, el modo de mantenimiento y la alta disponibilidad (HA) en hosts de laboratorio. Acceda al **appliance XOA-HL** como administrador y conserve acceso autorizado a la consola del host. Antes de empezar, anote la dirección del appliance, los ID de hosts y pools y qué appliance los administra hoy. Para la primera conexión, consulte [primer acceso y conexión de hosts](/docs/xoa-hl/first-login/).

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio. La sección del botón XO Lite también cubre `xolite-ce v0.21.0-ce29` (versión original `xo-lite-v0.21.0`).
{{< /callout >}}

## Compruebe la conexión y la responsabilidad sobre el pool {#connected-pool}

1. Abra **Settings → Servers** (`/#/settings/servers`).
2. Compruebe que la conexión esperada está habilitada y conectada.
3. Compruebe que el inventario muestra el host, pool, VM y almacenamiento previstos.

Una entrada de servidor guardada no demuestra que funcione la conexión. Si falla, lea su error y compruebe dirección, credenciales y gestión del certificado con la [guía de conexión](/docs/xoa-hl/first-login/).

La regla de soporte, registrada en la [incidencia #126](https://github.com/Vagrantin/xcp-hl/issues/126), es **una XOA administra un host o pool determinado**. Técnicamente pueden conectarse varios appliances, pero no se admite administrar el mismo pool desde más de uno. Un appliance sí puede administrar varios pools. Acuerde quién administra el pool antes de añadir una conexión. Nunca deje programaciones de copia de seguridad duplicadas activas para los mismos invitados.

## Transfiera la administración a otro appliance {#move-management}

Esto transfiere la responsabilidad del pool de un appliance antiguo a otro nuevo. No cambia su composición. Nunca quite un host del pool ni elimine una VM para transferir la administración de XO.

1. Planifique una ventana. Deje terminar las tareas de administración y copia de seguridad en curso.
2. En el appliance antiguo, anote conexiones, programaciones y destinos de copia de seguridad.
3. [Exporte su configuración](/docs/xoa-hl/configuration-backup/) y guarde el archivo de forma segura. Exportar por sí solo no transfiere ni desactiva ninguna tarea.
4. En el appliance antiguo, desactive las programaciones que cubren este pool.
5. En **Settings → Servers** del antiguo, quite la conexión al pool. Hágalo antes de conectar el nuevo.
6. En el nuevo, añada la conexión al host o pool. Compruebe el inventario conectado y los permisos previstos.
7. Si vuelve a crear o restaura ajustes, siga las precauciones de aislamiento e importación de la [guía de copia de configuración](/docs/xoa-hl/configuration-backup/).
8. Compruebe que el appliance antiguo ya no se reconecta ni ejecuta tareas contra el pool.
9. En el nuevo, compruebe los destinos de copia y realice una prueba de recuperación aislada. Después active solo las programaciones previstas.

**Comprobación:** solo el nuevo appliance está conectado al pool y ejecuta tareas para él.

Si el estado de cualquiera de los dos no está claro, pause la transferencia y guarde los errores de conexión y tareas. Para reunir hosts en un pool, consulte [Probar la incorporación a un pool](#pool-join).

## Comprenda el botón de XO Lite {#xo-lite-button}

Cada appliance conectado deja un marcador en el pool. XO Lite lee esos marcadores para construir su botón **Access XOA**.

- XO escribe la clave `xo:clientInfo:<appliance-uuid>` en `other-config` del pool. Con los ajustes predeterminados, la escribe al conectarse y después cada **6 horas**. En cada pasada también elimina marcadores de más de **48 horas**.
- Una conexión XO de solo lectura no escribe marcador.
- Quitar una conexión de servidor detiene nuevas escrituras, pero no elimina inmediatamente el marcador existente.
- **Access XOA** usa el marcador con el valor `lastConnected` más reciente. Abre `publicUrl` si está definido; si no, la primera dirección de `eth0` (o de la primera interfaz disponible), por HTTPS.
- El botón no comprueba que la VM del appliance ni su servicio web estén activos. Si XO Lite no encuentra dirección, ofrece **Deploy XOA**.
- XO Lite no hace caducar los marcadores por sí mismo. Un botón antiguo puede permanecer aunque ya no se conecte ninguna XO.

Una dirección antigua no justifica desplegar un segundo appliance. Compruebe primero la dirección conocida y qué appliance administra el pool. Si el correcto muestra una dirección errónea, compruebe URL y ajustes de red en lugar de borrar repetidamente su marcador.

## Quite un marcador obsoleto de XO Lite {#obsolete-marker}

Hágalo solo después de quitar la conexión del appliance antiguo (consulte [Transferir la administración a otro appliance](#move-management)). Solo cambia los datos de descubrimiento: no la composición del pool, los estados de las VM ni los datos de copia de seguridad.

1. En el **host hipervisor**, como root, ejecute estos comandos de solo lectura:

   ```bash
   xe pool-list params=uuid,name-label
   xe pool-param-get uuid='<pool-uuid>' param-name=other-config
   ```

2. Compare el pool y la clave obsoleta exacta con sus registros del appliance responsable.
3. Anote el valor del marcador.
4. Solo si es necesario, quite **esa única clave**. Sustituya ambos marcadores de posición. Nunca quite todo `other-config`:

   ```bash
   xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
   ```

5. Ejecute de nuevo los comandos de solo lectura y recargue XO Lite.

**Comprobación:** la clave ya no aparece. Si vuelve, sigue conectado un appliance antiguo: reescribe el marcador al reconectarse o en su próxima pasada. Encuentre esa conexión restante.

## Lea las estadísticas del host {#host-statistics}

Leer estadísticas no cambia nada en el host, sus VM, redes o almacenamiento.

**Antes de empezar**

- Elija un host conocido, conectado y en ejecución. Anote ID, pool, número de CPU y memoria.
- Esta pestaña muestra un solo host. La vista general del pool y el monitor del propio appliance muestran otra cosa.

1. Abra la pestaña **Stats** del host (`/#/hosts/<id>/stats`). Compruebe que es el correcto antes de leer cualquier gráfico.
2. Empiece con **Last 10 minutes**, el intervalo predeterminado. Anote intervalo, hora actual, zona horaria del navegador, hora de la última muestra y cualquier error de tarea o conexión.
3. Espere varios intervalos de muestreo y compruebe que llegan datos nuevos. Que un gráfico siga en pantalla no demuestra que la recopilación siga actualizada.
4. Elija un intervalo más largo para comparar. XO solicita muestras **AVERAGE**, por lo que un punto en un intervalo largo puede suavizar un pico breve. Vuelva al corto para observar cambios recientes.
5. Deje **Stacked values** desactivado en la primera lectura de cada serie. Actívelo solo para comparar: añade series de CPU y red sumadas y puede cambiar la escala. Lea siempre leyenda, unidad y escala vertical.
6. Anote una referencia durante una carga normal conocida. Compare después un periodo ocupado conocido en el mismo host, intervalo y ajustes. Anote series, horas, separación de muestras y síntoma real.

No ejecute pruebas de estrés en producción ni cambie tamaño, migre o reinicie un invitado solo para mover un gráfico. Una carga de laboratorio necesita autorización de su operador.

| Intervalo | Muestreo y actualización esperados |
| --- | --- |
| Last 10 minutes | 5 segundos |
| Last 2 hours | 1 minuto |
| Last day | 1 hora; últimas 24 muestras horarias |
| Last week | 1 hora |
| Last year | 1 día |

El nombre del intervalo indica el historial que XO solicita, no que el host lo haya conservado entero. Los intervalos largos no se actualizan cada cinco segundos. Compare lecturas con el mismo intervalo y separación de muestras. Observe las horas: el último punto no es una lectura instantánea.

| Gráfico | Cómo interpretarlo |
| --- | --- |
| CPU usage | Cada serie `Cpu` es un porcentaje. `All Cpus` es su suma, no un porcentaje del host: cuatro CPU al 50 % suman 200 %. Compruebe el número de CPU y cada serie antes de decidir que el host está saturado. |
| Memory usage | Memoria total del host menos la libre, mostrada en bytes. No es el límite de memoria de un invitado ni la RAM libre vista por una aplicación. Si faltan datos de memoria libre, el uso puede aparecer como cero: compruebe un cero inesperado por otro medio. |
| Network throughput | Series `eth` numeradas para recepción (`rx`) y transmisión (`tx`). Relaciónelas con las interfaces del host. Los valores son tamaños en bytes. Esta guía no cubre conversión a Mbps/Gbps, bonds ni VLAN. Una serie tranquila no demuestra la salud del enlace ni de la conectividad de los invitados. |
| Load average | Métrica `loadavg` independiente del host. No es porcentaje de CPU ni medida de capacidad de disco. Compárela con CPU, memoria, tráfico y carga real. No se establece aquí un umbral seguro general. |

**Comprobación:** en el intervalo corto, la hora de la muestra más reciente sigue avanzando.

| Problema | Qué comprobar |
| --- | --- |
| **No stats.**, carga interminable, huecos o línea plana o a cero | Anote host, intervalo, hora y error. Compruebe conexión y que el host está en ejecución. Recargue y vuelva a elegir el intervalo corto. La pestaña no obtiene datos de un host detenido. Tras un fallo de consulta, esperar puede no reiniciar la recopilación. Algunas muestras ausentes se convierten en ceros. Un gráfico vacío o un cero no demuestra inactividad ni buena salud. |
| Las horas de muestra siguen sin avanzar | Use [resolución de problemas](/docs/xoa-hl/troubleshooting/) y comprobaciones autorizadas en el propio host antes de decidir sobre capacidad. No restablezca estadísticas ni reinicie un host de producción para corregir los gráficos. |

Los gráficos por sí solos no muestran capacidad para otra VM, una conmutación HA o una migración segura. Quedan fuera precisión de métricas, historial completo, alineación de relojes, alertas, paneles y totales del pool, capacidad del SR y diagnóstico de rendimiento.

## Pruebe la incorporación a un pool con dos hosts de laboratorio {#pool-join}

La incorporación mueve un host a otro pool. **Cambia la pertenencia del host** y puede instalar parches ausentes. Practique solo con dos hosts de laboratorio que pueda reconstruir.

**Antes de empezar**

- Use dos hosts de laboratorio de versión conocida. El destino es el maestro de un pool que solo lo contiene a él. El origen es el único host de otro pool. Un host independiente es un pool de un solo host.
- Conserve acceso por consola independiente a ambos, un plan escrito de recuperación y reconstrucción y un appliance XOA-HL que administre ambas conexiones.
- No use un pool de producción, uno con HA, invitados en ejecución, cargas compartidas o conectadas ni un host cuyos datos no tengan copia independiente.
- Acuerde con los responsables de red y almacenamiento la incorporación en la misma red, DNS y sincronización horaria, acceso de administración separado y recuperación por consola. Una red o SR con nombre similar en cada host no es necesariamente compartido.

1. En el **navegador XOA-HL**, abra **Settings → Servers**. Compruebe una conexión funcional por cada pool.
2. Anote ID de ambos pools, ID del maestro destino y host origen, marca de producto, versión, compilación y nivel de parches, direcciones de administración, inventario de red y almacenamiento, número de VM y tareas activas. Compruebe que no hay otro host en el pool origen.
3. Detenga las programaciones de copia de ambos pools durante la ventana. Conserve sus puntos de recuperación independientes.
4. Abra la página del **pool de destino** (`/#/pools/<target-pool-id>/general`), identifique el maestro y seleccione **Add hosts**.
5. Seleccione únicamente el host de origen previsto. La lista oculta hosts de pools con más de uno. Muestra las diferencias de parches en ambos sentidos.
6. Seleccione **Cancel** y resuelva la causa fuera de esta prueba si cualquier recuento de parches no es cero, difieren marca o versión, HA está activada, debe conservarse una VM o SR del origen o la vía de incorporación no está clara. No use este diálogo para instalar parches ni evacuar un host.
7. En la ventana autorizada, compruebe pool destino y host origen exactos y seleccione **OK** una vez. La interfaz envía `force: true`, que llama a XAPI `pool.join_force`. Esta confirmación cambia los pools: no es una comprobación inocua de compatibilidad.
8. Espere la tarea. Tras incorporarse correctamente, la conexión origen debería desaparecer y la destino actualizar su inventario. La vista puede aparecer desconectada un momento. No vuelva a enviar solo porque una tarea o página no se haya actualizado.
9. Actualice la conexión destino. Compruebe que el ID y maestro del pool no cambiaron, que pertenecen exactamente los dos ID de host esperados y que puede explicar el estado del antiguo pool origen y su conexión.
10. En cada host, compruebe redes y PIF, conexiones de SR (PBD) y acceso de administración. Compruebe que el almacenamiento de prueba y la red aislada del invitado funcionan desde los hosts correctos. Busque VM inesperadas, conexiones XOA duplicadas, tareas de copia o marcadores XO Lite.

**Comprobación:** el pool destino conserva su maestro y contiene exactamente los dos hosts esperados, y ambos siguen accesibles desde sus consolas.

Anote ID anteriores y posteriores, recuentos de diferencias de parches, resultado de tarea, acceso por consola y cada comprobación. Conserve el pool de laboratorio unido si era el resultado deseado. **Detach** expulsa un host de su pool: es un cambio independiente, no una reversión automática. Compartir pool no demuestra seguridad para migración ni HA.

**Si falla la incorporación**, guarde tarea y error, estado de consola y ambos inventarios. El servidor puede haber aplicado ya parches o realizado parte de la incorporación. Deténgase y siga el plan de recuperación del responsable. No fuerce otra combinación ni expulse un host. La retirada posterior de hosts, HA, almacenamiento compartido y migración en vivo quedan fuera de esta sección.

## Pruebe el modo de mantenimiento en un host de laboratorio {#host-maintenance-mode}

El modo de mantenimiento deshabilita un host y traslada sus VM activas a otros hosts del pool. Practique solo en un pool de laboratorio reconstruible. Esta prueba no instala parches, reinicia hosts ni comprueba disponibilidad durante actualizaciones. Para actualizar, consulte la [guía de actualización de hosts](/docs/guides/updates/#updating-xcp-hl-the-host).

**Antes de empezar**

- Use un **pool de laboratorio de dos hosts**, de versión conocida, cuya red y almacenamiento compartido hayan superado sus propias pruebas. No use cargas de producción ni un pool recién unido sin comprobar.
- El host que pondrá en mantenimiento **no es el maestro**.
- Mantenga acceso de consola y administración separado a ambos, un appliance XOA-HL que administre el pool y un plan autorizado de recuperación y reconstrucción.
- Use una VM de prueba con punto de recuperación independiente comprobado. Debe ser la **única** VM normal en el host origen. Su almacenamiento y red de invitado deben estar disponibles en el otro host.
- La [migración dentro del pool](/docs/xoa-hl/vm-transfer/) debe funcionar ya para esta VM. Si no la ha probado, hágalo primero y vuelva a anotar después el estado del host origen. Deténgase si algún requisito o la red de migración no están claros.

1. En **XOA-HL**, anote ID de pool, maestro y ambos hosts, versiones y niveles de parches, estados de habilitación y alimentación, direcciones de administración, ubicación de cada VM, conexiones SR (PBD), redes y PIF, capacidad libre del destino y tareas activas.
2. Termine o pause las tareas de copia de seguridad y restauración.
3. Mediante una sesión autorizada del invitado, anote el comportamiento actual de su aplicación y red. Esta será su referencia.
4. Abra **Advanced** del host origen (`/#/hosts/<source-host-id>/advanced`). Compruebe host y pool exactos.
5. Seleccione **Enable maintenance mode**. El diálogo **Maintenance mode** indica que todas las VM activas migrarán a otros hosts del pool. En la ventana autorizada, seleccione **OK** una vez. XO llama a `host.setMaintenanceMode`; después XAPI deshabilita el host y llama a `host.evacuate`.
6. Si aparece **Bypass blocked migrations**, cancele: esa vía elimina los bloqueos de migración de las VM.
7. Espere el resultado y actualice las listas de hosts y VM.
8. Compruebe que el origen está deshabilitado, la VM de prueba se ejecuta en el destino previsto, ninguna VM normal sigue en el origen y aplicación y red coinciden con la referencia. Anote tarea, errores y acceso por consola.
9. En **Advanced** del mismo host, seleccione **Disable maintenance mode**. XO llama a `host.enable`.
10. Compruebe que el host está habilitado, ambas vías de administración y las conexiones de SR y red están sanas, y la VM sigue en el destino.

**Comprobación:** el host vuelve a estar habilitado y la VM de prueba sigue en el destino. Salir del mantenimiento **no** la devuelve. Manténgala allí o planifique una migración independiente y probada.

No sustituya mantenimiento por el botón **Disable**, reinicio forzado, apagado de emergencia ni botón de parches. Reactive las programaciones de copia solo tras comprobar su alcance y un punto de recuperación aislado. Guarde ID anteriores/posteriores, horas, comprobaciones del invitado, salida de tarea, estado real del host y ubicación de cada VM. Un cambio de interruptor exitoso o la mera pertenencia al pool no demuestran preparación para parches o HA.

**Si falla la evacuación**, deténgase: algunas VM pueden haberse movido ya. Tras un error de evacuación, XO normalmente vuelve a habilitar el host, pero un fallo anterior puede dejarlo deshabilitado. Lea el estado real y la ubicación de todas las VM y siga el plan de recuperación del responsable. No repita el interruptor, omita bloqueos ni reinicie para despejar un estado incierto.

## Compruebe la preparación para HA en un pool de laboratorio {#ha-readiness}

Cuando la alta disponibilidad (HA) está activada, puede aislar mediante fencing y reiniciar un host si falla la comunicación de latidos. Pruébela solo en un pool de laboratorio reconstruible. Aquí no se provoca ningún fallo de host ni se mide reinicio de VM. Antes de afirmar disponibilidad, ejecute una prueba de fallo separada y autorizada con una VM de prueba protegida.

**Antes de empezar**

- Use un **pool de laboratorio de tres hosts** con versión conocida, reconstruible y con sus comprobaciones superadas. Excluya cargas normales.
- Adminístrelo desde un appliance XOA-HL que se ejecute **fuera** del pool. Mantenga appliance y vía de acceso fuera del dominio de fallo.
- Conserve acceso independiente por consola y alimentación a cada host y un plan de recuperación autorizado.
- Lea la [guía de planificación HA de XCP-ng](https://docs.xcp-ng.org/management/ha/). Recomienda tres hosts y describe requisitos de latidos de red y almacenamiento, capacidad y fencing. Contrástelos con la versión real de los hosts XCP-HL.
- Una incorporación de dos hosts, una migración exitosa o un SR con el mismo nombre no demuestran preparación para HA.

1. En **XOA-HL**, anote ID exactos de pool, maestro y tres hosts, versiones, direcciones e IP estáticas de administración, estado HA, VM, tareas activas y el único appliance XOA-HL responsable.
2. Pida a los responsables de red y almacenamiento confirmar un SR de latidos compartido, con escritura, conectado y accesible desde los tres hosts. Deben confirmar también vías de administración y almacenamiento sanas y redundantes y capacidad suficiente para los invitados protegidos tras perder un host.
3. Anote el ID del SR y sus conexiones (PBD), no solo su nombre. Si no está claro un requisito o el acceso por consola, deténgase aquí: hasta ahora solo ha leído.
4. Abra **Advanced** del pool (`/#/pools/<pool-id>/advanced`). Observe **Heartbeat SR** y **High Availability**.
5. Active **High Availability** para abrir **Enabling high availability**. Enumera SR compartidos con escritura de este pool. Compare el candidato con su registro. Que aparezca no demuestra conexión a hosts, fiabilidad de latidos ni capacidad de conmutación.
6. Seleccione **Cancel** si el registro o plan de recuperación están incompletos. Nunca elija un SR solo porque figure en la lista.
7. Solo en una ventana autorizada de laboratorio y cumpliendo todos los requisitos: vuelva a abrir el diálogo, elija el SR anotado y pulse **OK** una vez. XO llama a `pool.enableHa`, que llama a XAPI `pool.enable_ha`. Anote tarea y errores.
8. Actualice el pool. Compruebe **High Availability** activada, el SR esperado en **Heartbeat SR**, los tres hosts accesibles y ausencia de VM o tareas inesperadas.
9. Con el pool sano y las notas guardadas, desactive **High Availability**. En **Disabling high availability**, seleccione **OK** una vez. XO llama a XAPI `pool.disable_ha`.
10. Compruebe HA desactivada, hosts y vías SR sanos y autorización independiente para cualquier siguiente trabajo.

**Comprobación:** HA se activó y desactivó una vez, con el SR de latidos esperado, y los tres hosts siguieron accesibles.

Mientras HA está activa, los botones de parches de host y pool están bloqueados. No inicie actualizaciones ni reinicios durante esta prueba. Guarde ID anteriores/posteriores de pool, hosts y SR, conexiones, supuestos de capacidad, salida de tareas, acceso por consola y estado HA.

**Si falla la activación o un host sufre fencing**, guarde registros de consola, tareas y HA, y siga el plan del responsable. Si el pool está degradado, deténgase y siga su procedimiento de incidente: el interruptor HA no es un comando general de recuperación. No repita el interruptor, reinicie el toolstack ni provoque fallos de red o almacenamiento para despejar un estado incierto.

{{< details title="Fuentes" closed="true" >}}
- **Estadísticas del host**: [pestaña del host y gestión de actualizaciones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js), [selector de intervalos y muestreo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/stats.js), [API de estadísticas del host](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [promedios RRD, métricas y caché](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs), [sumas, escalas y etiquetas de gráficos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js), [cálculo de memoria y formato de bytes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/utils.js).
- **Conexiones de servidor y botón XO Lite**: [interfaz de servidores](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [marcado del pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [intervalos predeterminados](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [selección de dirección del botón XO Lite](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [compilación y objetivos de parches XO Lite CE](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml), [regla de soporte y limpieza de marcadores (incidencia #126)](https://github.com/Vagrantin/xcp-hl/issues/126).
- **Incorporación al pool**: [acción del destino](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/action-bar.js), [selector de host único y recuentos de parches](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-hosts-modal/index.js), [indicador de forzado en el envoltorio de interfaz](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [API de permisos y combinación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [comprobaciones de versión y marca, parches y combinación secuencial](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/pool.mjs), [incorporación y transición de conexiones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [XAPI join_force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs).
- **Mantenimiento del host**: [pestaña Advanced y botones](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-advanced.js), [confirmación y ruta de migraciones bloqueadas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [API de mantenimiento](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [deshabilitación, evacuación, errores y habilitación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [texto de confirmación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Alta disponibilidad**: [selector Advanced del pool, lista SR de latidos y estado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-advanced.js), [API y permisos del pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [llamadas XAPI](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [guía de planificación HA de XCP-ng](https://docs.xcp-ng.org/management/ha/).
{{< /details >}}
