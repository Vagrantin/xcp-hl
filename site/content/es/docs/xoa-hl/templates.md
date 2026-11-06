---
title: "Crear y usar plantillas de VM"
linkTitle: "Plantillas"
description: "Convierta una copia preparada de una VM en plantilla y cree nuevas VM a partir de ella."
weight: 42
translationKey: xoa-manual-templates
translationStatus: draft
sourceRevision: sha256:48760dd766f7ce1cb3d4371b2cb0ae8102b3992799119e1e08fae97a6f20d2f1
glossaryTerms: ["backup", "pool", "sr", "vm"]
---

Convierta una copia detenida de una VM en plantilla, cree dos VM a partir de ella y compruebe que cada una obtiene sus propios discos y datos. La VM original permanece intacta.

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio. Estos pasos reutilizan un disco instalado: no preparan un sistema operativo invitado para su reutilización generalizada.
{{< /callout >}}

## Antes de empezar {#before-you-begin}

- Acceda al **appliance XOA-HL** como administrador. Convertir una VM exige permisos de administración tanto sobre la VM como sobre su pool; el acceso solo a la VM no basta.
- Use un invitado de pruebas ya instalado con discos normales: sin discos compartidos ni dispositivos de paso directo. Nunca convierta el appliance ni la VM original.
- Cree una copia de trabajo independiente con [Crear una copia completa en el mismo pool](/docs/xoa-hl/vm-operations/#full-copy). Anote los UUID del original y la copia, el ID VDI, SR y tamaño de cada disco, y la suma de comprobación de un archivo de ejemplo inocuo dentro del invitado. Compruebe que la copia arranca aislada y apáguela normalmente.
- En la copia de trabajo, quite **todas** las interfaces de red, expulse el ISO del instalador, desactive el encendido automático y exclúyala de las tareas programadas.
- Reserve memoria del host y espacio en SR con escritura para la plantilla y dos VM de prueba.
- Disponga de acceso a la consola y de las credenciales del invitado. Renombrar una VM o cambiar su MAC no cambia las contraseñas, nombre de host, configuración IP, claves ni identidades de aplicaciones copiados. Use estas copias únicamente mediante la consola.

Trabaje en el navegador, en la dirección del appliance. Compruebe archivos y sumas en la **consola del invitado**, no en el host ni en el appliance. Una plantilla en la misma infraestructura no es una copia de seguridad: guarde sus [copias de seguridad](/docs/xoa-hl/backup-restore/) por separado. Para un invitado Ubuntu 24.04 nuevo, [instale las herramientas de invitado](/docs/xoa-hl/guest-tools/) antes de crear la copia.

## Convierta la copia detenida en plantilla {#convert-template}

1. Compruebe la copia de trabajo: su UUID, estado **Halted**, lista de interfaces de red vacía y los discos anotados.
2. Asígnele un nombre único, como `lab-template-v1`, y una descripción con el SO invitado y su versión, la fecha de preparación y la suma del archivo de ejemplo. Actualice la página y compruebe estos valores.
3. Abra la pestaña **Advanced** (`/#/vms/<copy-uuid>/advanced`) y seleccione **Convert to template**. El botón solo funciona cuando la VM está detenida. La confirmación advierte que el cambio es permanente: cancele si no es la copia deseada.
4. Confirme una vez y espere a que termine.
5. Abra **Home** y elija el tipo de objeto **Template** (`/#/home?t=VM-template`). Borre los filtros si es necesario, expanda la fila y lea el UUID completo.

**Comprobación:** la plantilla tiene el **mismo UUID** que la copia de trabajo, con el nombre y descripción elegidos, y la VM original sigue existiendo. La conversión no copia la VM: la propia copia se convierte en plantilla.

Antes de marcar la VM como plantilla, XO intenta expulsar los medios extraíbles. Si falla, los cambios previos en los medios pueden permanecer aunque falle la conversión. Actualice el tipo de objeto, los medios y la tarea antes de repetir. Esta guía no trata la reconversión de plantilla a VM ni la reversión automática.

## Cree una VM detenida a partir de la plantilla {#deploy-template}

1. Abra **New → VM** (`/#/vms/new`), elija el mismo pool y seleccione su plantilla. Llame a la VM `lab-template-test-1`. Compruebe el UUID `template=` en la dirección de la página, no solo el nombre de la plantilla.
2. Compruebe CPU, memoria, discos de la plantilla, tamaños y SR de destino con escritura. Mantenga los mismos discos y tamaños.
3. En **Install settings**, elija **No config drive**. Esta prueba reutiliza el disco instalado: no ejecuta un instalador ni depende de cloud-init para cambiar la identidad del invitado. Si faltan los discos o esta opción, deténgase y compruebe la plantilla seleccionada.
4. En **Interfaces**, quite todas las interfaces propuestas y compruebe que la lista está vacía. Incluso una plantilla sin interfaces puede recibir las redes predeterminadas del pool mediante el asistente.
5. En **Advanced**, desmarque **Boot VM after creation** y deje desactivado el encendido automático.
6. En **Summary**, desmarque **Fast clone**. Compruebe que está creando una VM con los discos, recursos y SR esperados y **cero interfaces**. Seleccione **Create** una sola vez. El asistente activa por defecto el arranque tras la creación y la clonación rápida; no confíe en ajustes anteriores. Sin clonación rápida, XO realiza una copia completa de los discos, que requiere espacio en el SR.
7. Espere, actualice y anote el UUID de la nueva VM.

**Comprobación:** antes de cualquier arranque, la VM nueva está **Halted**, su pestaña Network está vacía y los discos tienen el número, tamaños y SR esperados, con ID VDI distintos de los de la plantilla y el original. La plantilla y el original siguen existiendo. Un mensaje de éxito o un nombre nuevo no lo demuestra. Si apareció una interfaz o arrancó la VM, deténgala y compruebe a qué pudo acceder antes de continuar.

## Compruebe que cada VM obtiene su propia copia {#verify-deployments}

1. Tras las comprobaciones anteriores, arranque solo `lab-template-test-1`. En su [consola](/docs/xoa-hl/vm-operations/#vm-console), compruebe que el invitado arranca y puede acceder; después compruebe la disposición de los discos y la suma del archivo de ejemplo.
2. Cambie solo el archivo de ejemplo a un nuevo valor de prueba, anótelo y apague normalmente el invitado.
3. Repita [Crear una VM detenida a partir de la plantilla](#deploy-template) desde la **misma plantilla**, como `lab-template-test-2`. Revise de nuevo todos los ajustes.
4. Estando detenida, compruebe que tiene un UUID de VM diferente, ID VDI distintos y ninguna interfaz. Arránquela mediante la consola y compruebe que el archivo de ejemplo conserva su suma original, no el nuevo valor de la prueba 1. Apáguela normalmente.
5. Anote los UUID e ID VDI de ambas VM, el UUID de la plantilla, los resultados del invitado y las versiones instaladas. Deje detenidas las VM de prueba.

**Comprobación:** ambos invitados arrancan con los datos esperados y el cambio en la prueba 1 no llegó a la prueba 2. Esta comprobación de archivo no prueba la recuperación de aplicaciones ni elimina las identidades duplicadas del SO. No conecte una red de producción hasta que el responsable del invitado las haya resuelto.

Para limpiar, [elimine cada VM de prueba](/docs/xoa-hl/vm-operations/) tras identificarla. Conserve la plantilla, la VM original y sus copias de seguridad. Para una versión nueva de la plantilla, prepare otra copia con un nombre de versión nuevo y repita estas comprobaciones.

## Si algo falla {#problems}

| Problema | Qué comprobar |
| --- | --- |
| Se rechaza la conversión | Lea el error, los permisos de la VM y el pool y el estado real de alimentación. No fuerce la detención de un invitado valioso ni vuelva a convertir un objeto sin identificar. Tras un error, compruebe el tipo de objeto y los medios extraíbles del mismo UUID. |
| La plantilla no aparece | Elija el tipo de objeto Template, el pool y los filtros correctos, y actualice. Una plantilla no aparece en la lista normal de VM. No cree otra copia antes de comprobar el inventario. |
| Falla la creación de la VM | Guarde el error y la lista de plantillas, VM y VDI antes de repetir. XO intenta limpiar tras un fallo, pero una respuesta perdida o una limpieza fallida pueden dejar objetos. Nunca elimine en masa discos que parezcan huérfanos. |
| El invitado difiere o no arranca | Conserve la plantilla y los registros. Compruebe el UUID de plantilla, discos copiados, firmware, recursos y ajustes de instalación. No cambie la red de administración del host para resolverlo. |

Quedan fuera de esta guía la modificación del invitado dentro de una plantilla, la retirada o eliminación de plantillas, el despliegue en otro pool, el almacenamiento para clonación rápida, cloud-init y la preparación específica de cada SO. Si persiste un problema, [comuníquelo](/docs/xoa-hl/troubleshooting/#report-a-problem) sin datos sensibles.

{{< details title="Fuentes" closed="true" >}}
- **Conversión**: [acción de la pestaña Advanced, solo VM detenidas](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [diálogo de confirmación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [permisos, medios, conversión y limpieza tras creación fallida](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Asistente de VM nueva**: [identidad de la fila de plantilla](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/home/template-item.js), [valores predeterminados del asistente y ajustes enviados](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [copia de discos y sustitución de interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **Compilación HomeLab**: [script de compilación xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
