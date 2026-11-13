---
title: Contenedores Docker
weight: 5
translationKey: containers
---

Ejecuta contenedores Docker desde XOA-hl en una VM dedicada, sin tocar el host ni el appliance.
{class="lead"}

{{< callout type="warning" >}}
**No publicado.** Esta guía describe una función en desarrollo. Ninguna imagen publicada de XOA-hl la incluye. Consulta [la incidencia #7](https://github.com/Vagrantin/xcp-hl/issues/7) para conocer su estado.
{{< /callout >}}

## Qué obtienes {#what-you-get}

XOA-hl añade una página **Containers** para administradores. Los contenedores se ejecutan en una **VM Docker**: una VM normal, creada a partir de una plantilla preparada, que solo ejecuta Docker.

- Los hosts XCP-hl y el appliance XOA-hl nunca ejecutan Docker por sí mismos.
- Una VM Docker se respalda, se captura, se inicia y se detiene como cualquier otra VM.
- Cada contenedor tiene un límite de CPU y un límite de memoria, de modo que una aplicación no puede dejar sin recursos a las demás.

## Antes de empezar {#before-you-begin}

- Inicia sesión en XOA-hl como administrador.
- Importa la plantilla de VM Docker en tu pool y añádele la etiqueta `xcp-hl-docker-template-v1`. La página Containers te lo recuerda cuando no encuentra ninguna plantilla.
- Usa una red con DHCP que XOA-hl pueda alcanzar. La VM Docker necesita acceso a Internet, o un registro en tu red, para descargar imágenes.

## Desplegar una VM Docker {#deploy-a-docker-vm}

1. Abre **Containers**. Sin ninguna VM Docker, la página muestra una guía breve y el formulario **Deploy Docker VM**.
2. Introduce un nombre, el número de vCPU y la memoria. Con una sola plantilla, un almacenamiento predeterminado y una sola red, la página los selecciona por ti.
3. Selecciona **Deploy Docker VM** una sola vez. La VM se crea con su propio disco de 32 GiB y se inicia.
4. Espera unos minutos durante el primer inicio. Mientras la VM no esté lista, la página lo indica; no despliegues una segunda VM.

## Ejecutar un contenedor {#run-a-container}

1. En **Create container**, introduce un nombre y una imagen, por ejemplo `nginx:alpine`.
2. Mantén o cambia los límites. Los valores predeterminados son 1 CPU y 256 MiB.
3. Selecciona **Create container**. Una imagen que aún no está en la VM se descarga primero y después el contenedor se inicia solo. La descarga aparece encima de la lista hasta que termina.
4. Usa **Start**, **Stop**, **Restart**, **Logs** y **Remove** en cada contenedor. Solo se puede eliminar un contenedor detenido, y sus volúmenes se conservan.

Las **Advanced options** aceptan una entrada por línea:

| Campo | Formato | Ejemplo |
|---|---|---|
| Puertos publicados | `HOST:CONTAINER/tcp` | `8080:80/tcp` |
| Volúmenes persistentes | `NAME:/path` | `web:/usr/share/nginx/html` |
| Entorno | `KEY=value` | `TZ=UTC` |

Un puerto publicado es accesible en la dirección de la VM Docker, que se muestra en la página. No pongas contraseñas en variables de entorno: otros administradores y los registros pueden mostrarlas.

## Seguir el uso en el panel {#dashboard}

Cuando existe una VM Docker, el **Dashboard** muestra a los administradores una tarjeta **Docker containers**. Para cada VM Docker indica los contenedores en ejecución y el total, la carga, la memoria y el disco en uso, y los límites reservados por los contenedores en ejecución.

La tarjeta resalta lo que requiere atención: una VM Docker detenida o que no responde, una descarga fallida, memoria o disco casi llenos, y límites reservados superiores al tamaño de la VM.

## Límites y recursos {#limits}

Un límite es un tope para un contenedor, no una reserva. La suma de los límites puede superar la VM; en ese caso la página te avisa. Reduce un límite, o da más vCPU o memoria a la VM Docker desde su página de VM.

El espacio en disco lo comparten todas las imágenes, contenedores y volúmenes de la VM Docker. Elimina las imágenes sin usar en **Images** para liberar espacio.

## Respaldar y recuperar {#back-up-and-recover}

- Respalda la VM Docker con un trabajo de copia de seguridad normal de XOA-hl. Contiene las imágenes, los contenedores y los volúmenes.
- Respalda también el appliance XOA-hl. Guarda las claves de acceso de cada VM Docker, y no se pueden volver a crear.
- Después de eliminar una VM Docker, la página lista sus claves en **Unused access keys**. Elimínalas solo cuando la VM haya desaparecido de verdad: un pool desconectado hace que sus VM Docker parezcan eliminadas.
- Actualizar XOA-hl no actualiza la VM Docker. Su sistema y Docker se mantienen por separado.

## No incluido en esta versión {#not-in-this-version}

Sin archivos Compose, sin terminal dentro de un contenedor, sin contenedores privilegiados, sin carpetas compartidas desde la VM y sin contraseñas de registro guardadas.

Estas decisiones mantienen la primera versión pequeña y predecible.
