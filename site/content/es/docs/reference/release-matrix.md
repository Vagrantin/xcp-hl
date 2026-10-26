---
title: Matriz de versiones
weight: 1
translationKey: release-matrix
aliases: ["/release-matrix/"]
---

XCP-hl y XOA-hl se publican por separado: la ISO que instalas en el host y el appliance XOA-hl que XO Lite despliega sobre él. Esta página registra todas las publicaciones de ambos.
{class="lead"}

## XCP-hl {#xcp-hl-releases}

Cada ISO de XCP-hl se construye a partir de componentes con versiones independientes. Esta tabla registra exactamente qué versiones se distribuyeron juntas y de qué versión original se derivaron los componentes modificados.

Cada versión enlaza con su página de publicación en el repositorio que la produjo. Debajo aparece el paquete exacto que instala la ISO, escrito tal como lo muestra `rpm -q` en un host en ejecución, para que puedas identificar la fila correspondiente a un host:

```bash
rpm -q xoa-proxy xo-lite-ce xcp-hl-release
```

{{< release-matrix-iso >}}

La columna `xcp-hl-release` se rellena a partir del RPM registrado en las notas de publicación de la ISO. Las ISO antiguas que no tienen esa información muestran «No registrado»; no se deduce su identidad RPM a partir de la última versión actual.

[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) no tiene columna de versión original: es código escrito específicamente para este proyecto, no una bifurcación, así que su versión es propia. Su etiqueta sigue el formato `v<cargo version>.<build counter>` (por ejemplo, `v0.1.1.8` corresponde a la versión Cargo `0.1.1`, octava compilación de ella), y el campo release del RPM contiene el número de ejecución de CI y el commit de origen (`55.gc525575.static`). Las dos filas con etiquetas `v-proxy-automated-*` son anteriores a ese esquema: su etiqueta identifica una ejecución de compilación y solo el RPM indica la versión que incluían.

## XOA-hl {#xoa-hl-releases}

La imagen XOA-hl **no** está integrada en la ISO: el botón de despliegue de XO Lite resuelve la imagen de VM más reciente en el momento del despliegue, por lo que el appliance tiene su propia versión independiente de la ISO. Esta tabla registra cada imagen publicada, la versión del software [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) que contiene y la versión original de Xen Orchestra de la que deriva. Las imágenes se publican en [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) desde [#22](https://github.com/Vagrantin/xcp-hl/issues/22); las entradas anteriores enlazan a `xoa-hl`, donde se publicaron originalmente.

Cuando está registrada, la celda del software enlaza la etiqueta exacta de publicación del RPM y muestra la identidad del paquete que devuelve `rpm -q xoa-hl`. Las filas de imágenes antiguas solo tienen la versión del software derivada del proyecto original; eso por sí solo no identifica la compilación RPM concreta incluida en la imagen.

{{< release-matrix-xoa >}}
