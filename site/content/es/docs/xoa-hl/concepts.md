---
title: "Conceptos y alcance funcional"
linkTitle: "Conceptos"
description: "Comprender los componentes, los números de versión y lo que incluye esta versión."
weight: 90
translationKey: xoa-manual-concepts
translationStatus: draft
sourceRevision: sha256:9457bbb19ed144e4eabca2b0c7af226bd1db4d60fb67217e695f2165868fc341
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Esta página de referencia explica con qué componente trabajas, qué significan los números de versión y qué incluye esta versión. No contiene pasos que debas ejecutar. Consúltala antes de depender de una función o cuando comuniques un problema.

{{< callout type="info" >}}
**Aplicable a** la imagen `xoa-image-20261022-a280852`, el paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; todavía no se ha probado en un laboratorio.
{{< /callout >}}

## Componentes y direcciones {#components}

| Componente | Función | Dónde acceder |
| --- | --- | --- |
| Host del hipervisor o pool | Ejecuta las VM y proporciona la interfaz de administración XAPI | La dirección de administración del host |
| XO Lite CE | Interfaz de navegador servida por el host. Despliega y localiza el dispositivo virtual | La dirección HTTPS del host |
| Dispositivo virtual XOA-HL | VM independiente que ejecuta xo-server, la interfaz web XO 5 y Redis | La dirección HTTPS del dispositivo virtual |

Para comprender cómo encajan estas partes, consulta la [guía de arquitectura y despliegue](/docs/start/#start-architecture). Administra cada host o pool con un único gestor admitido. Lee [Hosts y pools](/docs/xoa-hl/hosts-pools/) antes de trasladar una conexión. Las actualizaciones del host y del dispositivo virtual son independientes, con sus propios destinos y horarios: consulta la [guía de actualización](/docs/guides/updates/).

## VM, almacenamiento y protección {#objects}

Una **VM** se ejecuta en un host de un **pool**. Un **repositorio de almacenamiento (SR)** guarda discos virtuales. La interfaz de red de una VM se conecta a una red del pool. Los nombres son solo etiquetas: utiliza identificadores de objeto en la automatización.

Una **instantánea** guarda el estado de una VM en un momento determinado, en el mismo almacenamiento. Una **copia de seguridad** copia los datos a un destino de copia de seguridad independiente (un remoto). Una instantánea por sí sola no protege frente a la pérdida de ese almacenamiento, y un trabajo de copia de seguridad correcto sigue necesitando una prueba de restauración.

Para obtener más información, consulta el [glosario](/docs/xoa-hl/glossary/), [Almacenamiento y redes](/docs/xoa-hl/storage-networks/) y [Crear una copia de seguridad y restaurar una VM](/docs/xoa-hl/backup-restore/).

## Números de versión {#versions}

| Versión | Significado |
| --- | --- |
| XO 5.113.2, commit del proyecto original `e281c536` | La versión de Xen Orchestra de la aplicación y de la interfaz web. Se eligió deliberadamente: no es XO 6 |
| `xo-server` 5.193.1 | La versión del paquete del servidor en esa misma versión. Utiliza una numeración diferente |
| `v5.113.2_e281c536-ce40` | La versión del paquete XOA-HL con su conjunto de parches |
| `xoa-image-20261022-a280852` | La compilación de la imagen del dispositivo virtual. Es un número independiente: actualizar la aplicación no lo cambia |

Anota los valores instalados como se explica en [mantenimiento del dispositivo virtual](/docs/xoa-hl/maintenance/). La [matriz de versiones](/docs/reference/release-matrix/) enumera las versiones distribuidas juntas; no significa que hayan superado pruebas de integración. La ISO de instalación no fija qué imagen del dispositivo virtual obtendrás: la imagen se elige después, durante el despliegue.

## Qué incluye esta versión {#feature-scope}

| Área | En el código de esta versión | Antes de depender de ella |
| --- | --- | --- |
| Encendido y apagado de VM, instantáneas, discos y redes | Están presentes las acciones y pantallas de XO 5 | Las guías de uso cotidiano todavía no se han probado en un laboratorio |
| Usuarios y permisos de objetos (ACL) | La compilación publicada conserva el plan predeterminado del proyecto original (OpenSource). Las pantallas ACL están en el código | Comprueba la interfaz instalada y realiza pruebas en otra sesión iniciada como usuario normal |
| Copia de seguridad completa y restauración | Se documenta un procedimiento NFS basado en el código | Todavía no se han probado una copia real y una restauración aislada |
| Actualizaciones del dispositivo virtual | API de actualización de XOA-HL, canales `stable` y `testing`, y horarios configurables | Sigue la guía de actualización correspondiente a tu versión |
| Hub, sección XOA de Vates, proxies de copia de seguridad y menús XOSTOR | Un parche del menú de este paquete oculta estas entradas | Un menú oculto no convierte una función en admitida. Tampoco demuestra que la API correspondiente haya desaparecido |

Esta versión del paquete declara 16 parches. No significan que se hayan probado todas las opciones del proyecto original. Los planes de suscripción de Vates, el soporte comercial y las interfaces de XO 6 no se aplican a este paquete. Antes de depender de una función, consulta [Usuarios y permisos](/docs/xoa-hl/permissions/) y la guía de esa tarea.

## Páginas relacionadas {#related}

- [Configuración del servicio](/docs/xoa-hl/configuration/): los archivos de configuración de xo-server.
- [Automatización con xo-cli](/docs/xoa-hl/automation/): consultar el inventario desde la línea de comandos con un token de corta duración.
- [Exportar la configuración](/docs/xoa-hl/configuration-backup/): guardar los ajustes y registros de la interfaz web.
- [xoa-hl](/docs/components/xoa-hl/) y [build-xoa-hl](/docs/components/build-xoa-hl/): cómo se genera el paquete. Las compilaciones del producto se ejecutan únicamente en CI.

Cuando propongas un cambio en esta documentación, incluye las versiones de la imagen y del paquete que utilizas.

{{< details title="Fuentes" closed="true" >}}
- **Versiones, parches y compilación**: [versión de XO del proyecto original (`UPSTREAM_XO`)](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [lista de parches](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/metadata.toml), [parche del menú que oculta entradas](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/menu-hide-items.patch), [definición del paquete](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [versión del paquete xo-server](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [compilación de la interfaz web](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
{{< /details >}}
