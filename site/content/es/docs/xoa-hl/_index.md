---
title: "Manual de XOA-HL"
weight: 2
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:9690e24c060de4d8fcc693f5a8507c57cce56c189f0a4c0c5abd9829f4c4abae
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL es el dispositivo virtual, una máquina virtual lista para usar, que ejecuta Xen Orchestra. Desde el navegador permite administrar tus hosts XCP-HL y tus máquinas virtuales. Este manual explica cómo configurarlo, ejecutar VM, protegerlas y mantenerlo todo actualizado.

{{< callout type="info" >}}
**Aplicable a** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Estas guías siguen el código publicado, pero todavía no se han probado de principio a fin en un laboratorio. Practica primero con VM de prueba.
{{< /callout >}}

## Empieza aquí {#start-here}

¿Es tu primera vez con XOA-HL? Sigue estas tres guías en orden.

{{< cards >}}
  {{< card link="first-login/" title="1. Primer inicio de sesión" subtitle="Inicia sesión, establece tu contraseña, elige un idioma y conecta el host." >}}
  {{< card link="create-vm/" title="2. Tu primera VM" subtitle="Carga una ISO de instalación e instala una VM de prueba." >}}
  {{< card link="backup-restore/" title="3. Copia de seguridad y restauración" subtitle="Crea una copia de seguridad de la VM y comprueba que una copia restaurada funciona." >}}
{{< /cards >}}

¿Todavía no lo has desplegado? Primero [despliega XOA-HL desde XO Lite](/docs/start/#start-deploy-xoa). Para comprender la relación entre el host, XO Lite y el dispositivo virtual, lee la [descripción de la arquitectura](/docs/start/#start-architecture).

## Máquinas virtuales {#virtual-machines}

- [Administrar VM](/docs/xoa-hl/vm-operations/): arranque y apagado, instantáneas, copias, CPU y memoria, eliminación.
- [Usar la consola de la VM](/docs/xoa-hl/vm-operations/#vm-console) y solucionar una pantalla vacía.
- [Crear una instantánea y volver a ella](/docs/xoa-hl/vm-operations/#stopped-snapshot).
- [Instalar herramientas de invitado Linux](/docs/xoa-hl/guest-tools/).
- [Crear y utilizar plantillas](/docs/xoa-hl/templates/).
- [Migrar, exportar e importar una VM](/docs/xoa-hl/vm-transfer/).

## Almacenamiento y redes {#storage-and-networks}

- [Añadir discos e interfaces de red](/docs/xoa-hl/storage-networks/).
- [Crear almacenamiento NFS para los discos de las VM](/docs/xoa-hl/storage-networks/#nfs-vm-storage).
- [Crear una red VLAN](/docs/xoa-hl/storage-networks/#host-vlan-network).
- [Diagnosticar un problema de red](/docs/xoa-hl/troubleshooting/#network-connectivity).

## Copias de seguridad y recuperación {#backup-and-recovery}

- [Programar copias de seguridad y establecer la retención](/docs/xoa-hl/backup-restore/#backup-schedules).
- [Utilizar copias de seguridad incrementales](/docs/xoa-hl/backup-restore/#delta-backups).
- [Recuperar un solo archivo](/docs/xoa-hl/backup-restore/#file-restore).
- [Copiar una VM a otro pool (DR)](/docs/xoa-hl/backup-restore/#dr-replica).
- [Crear copias de seguridad en un recurso compartido de Windows Server (SMB)](/docs/xoa-hl/backup-restore/#smb-remote).
- [Solucionar una copia de seguridad fallida](/docs/xoa-hl/troubleshooting/#backup-failures).

## Hosts, usuarios y seguridad {#hosts-users-and-security}

- [Administrar hosts y pools](/docs/xoa-hl/hosts-pools/): conexiones, botón de XO Lite y estadísticas.
- [Añadir un host a un pool](/docs/xoa-hl/hosts-pools/#pool-join).
- [Poner un host en modo de mantenimiento](/docs/xoa-hl/hosts-pools/#host-maintenance-mode).
- [Administrar usuarios, grupos y permisos](/docs/xoa-hl/permissions/).
- [Delegar recursos con una cuota](/docs/xoa-hl/permissions/#resource-set-delegation).
- [Añadir un código de un solo uso al inicio de sesión](/docs/xoa-hl/sign-in-otp/).

## Mantener XOA-HL en funcionamiento {#keep-xoa-hl-running}

- [Actualizar el dispositivo virtual](/docs/guides/updates/#updating-xoa-hl-the-appliance) y [actualizar el host](/docs/guides/updates/#updating-xcp-hl-the-host).
- [Planificar el mantenimiento y comprobar el resultado](/docs/xoa-hl/maintenance/).
- [Exportar la configuración de XO](/docs/xoa-hl/configuration-backup/).
- [Crear una copia de seguridad de los metadatos del pool](/docs/xoa-hl/configuration-backup/#pool-metadata).
- [Solucionar un problema](/docs/xoa-hl/troubleshooting/).
- [Consultar lo distribuido en cada versión](/docs/reference/release-matrix/) y [leer el registro de cambios](/docs/reference/changelog/).

## Referencia {#reference}

- [Conceptos y alcance funcional](/docs/xoa-hl/concepts/)
- [Configuración del servicio](/docs/xoa-hl/configuration/)
- [Automatización con xo-cli](/docs/xoa-hl/automation/)
- [Glosario](/docs/xoa-hl/glossary/)
- [Páginas para colaboradores](/docs/components/)

## Ayuda y comentarios {#help-and-feedback}

La interfaz de XOA-HL y esta documentación tienen ajustes de idioma independientes. Utiliza el selector de la parte superior de esta página para cambiar el idioma de la documentación. El [estado de revisión de las páginas](/docs/xoa-hl/translation-status/) indica qué páginas se han revisado.

[Comunica un problema de documentación](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Incluye la dirección de la página, el paso que necesita corregirse y la versión de tu dispositivo virtual. Nunca incluyas contraseñas ni datos privados.
