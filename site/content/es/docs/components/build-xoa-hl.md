---
title: build-xoa-hl
weight: 5
translationKey: build-xoa-hl
aliases: ["/developers/build-xoa-hl.html"]
---

Proceso Packer que construye el appliance VM XOA-hl en XCP-ng y genera la imagen XVA que despliega XO Lite CE.
{class="lead"}

**Repositorio:** [Vagrantin/build-xoa-hl](https://github.com/Vagrantin/build-xoa-hl)
· Lenguaje: Bash / JSON de Packer / Kickstart · Licencia: AGPL-3.0

## Objetivo {#purpose}

Este repositorio construye el **appliance VM XOA HomeLab Edition**: una VM AlmaLinux 9, instalada y aprovisionada por Packer **en un host XCP-ng real**, con el RPM [`xoa-hl`](/docs/components/xoa-hl) dentro. El resultado es una **imagen XVA** comprimida, el artefacto que importa el botón de despliegue de XO Lite CE.

El appliance es genérico durante su construcción: incluye dos servicios de primer arranque de una sola ejecución que leen los datos de aprovisionamiento (red y credenciales de administrador) de XenStore cuando XO Lite lo despliega, para que una única imagen sirva para todos los usuarios.

---

## Estructura del repositorio {#repo-structure}

```
build-xoa-hl/
├── build.config.sample        ← infrastructure config template (copy → build.config)
├── scripts/
│   ├── setup-xoa-builder.sh   ← build entry point: generates Kickstart + Packer JSON, runs build
│   ├── xoa-first-boot.sh      ← in-VM phase 1: XenStore → network + env file
│   └── xoa-credentials.sh     ← in-VM phase 2: sets XO admin credentials via xo-cli
├── systemd/
│   ├── xoa-first-boot.service
│   └── xoa-credentials.service
├── bin/                       ← vendored VMware VDDK tarball (V2V support)
└── artefact/                  ← build/debug artefacts: logs, installed-RPM list, memo
```

---

## Requisitos previos {#prerequisites}

- Un equipo de compilación Linux con `apt` y sudo (desarrollado en Linux Mint). El script de preparación instala sus dependencias: Packer (repositorio apt de HashiCorp), el complemento Packer [`ddelnano/xenserver`](https://github.com/ddelnano/packer-plugin-xenserver), `wget`, `curl`, `jq` y `ufw`.
- Un **host XCP-ng** accesible con credenciales root, un SR `Local storage` y una red de VM con nombre.
- Una publicación de [`xoa-hl`](/docs/components/xoa-hl) en GitHub (se resuelve automáticamente el RPM de la última versión).
- `build.config`, copiado de `build.config.sample` y cumplimentado: IP/credenciales del host XCP-ng, nombre de red, nombre de VM y contraseña root, URL de la ISO de AlmaLinux y URL de los RPM `xe-guest-utilities`.

{{< callout type="warning" >}}
`build.config` contiene **credenciales en texto plano** (contraseña root de XCP-ng y contraseña root de la VM). Nunca lo subas al repositorio; solo `build.config.sample` debe estar en git.
{{< /callout >}}

---

## Punto de entrada de la compilación, scripts/setup-xoa-builder.sh {#build-entry-point-scriptssetup-xoa-buildersh}

Se ejecuta en el equipo de compilación y genera todo lo que necesita Packer:

1. **Carga `build.config`** (usa valores integrados si no existe).
2. **Instala los requisitos previos**: paquetes apt, HashiCorp Packer y el complemento Packer `ddelnano/xenserver`.
3. **Abre los puertos 8000–9000/tcp** (ufw): Packer sirve el archivo Kickstart a la VM desde su servidor HTTP integrado en un puerto de ese intervalo.
4. **Resuelve la suma de comprobación de la ISO de AlmaLinux**: analiza el archivo `CHECKSUM` de estilo BSD del espejo y, como alternativa, `SHA256SUMS` de estilo GNU; falla si no encuentra un SHA256 válido (salvo que esté fijado en `build.config`).
5. **Resuelve la URL del último RPM xoa-hl**: busca en `api.github.com/repos/Vagrantin/xoa-hl/releases` la publicación más reciente con un artefacto `.rpm`. No utiliza `releases/latest`: aún podría apuntar a una publicación `xoa-image-*` anterior a [#22](https://github.com/Vagrantin/xcp-hl/issues/22), que solo contiene un XVA.
6. **Genera `inst.ks`**, el archivo de respuestas Kickstart: DHCP en `eth0`, particionado EXT4 (sin LVM), SELinux y cortafuegos desactivados, conjunto mínimo de paquetes; `%post` activa sshd/chrony, instala `epel-release`, `wget`, `nc` y `vim`, y crea el usuario `xo` (en `wheel`).
7. **Genera `almalinux-build.json`**, la plantilla Packer (véase abajo).
8. **Ejecuta la compilación**, `packer validate` y después `PACKER_LOG=1 packer build almalinux-build.json`.

---

## Plantilla Packer, almalinux-build.json {#packer-template-almalinux-buildjson}

Un único constructor `xenserver-iso`: Packer sube la ISO de AlmaLinux al host XCP-ng, arranca una VM (2 GB de RAM, disco de 10 GB) con `inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/inst.ks` en la línea de comandos del kernel, espera a SSH y ejecuta los aprovisionadores:

1. `dnf update -y`.
2. Instala **xe-guest-utilities** y **xe-guest-utilities-xenstore** (URL de los RPM de `build.config`), necesarios para acceder a XenStore en el primer arranque.
3. Instala **Node.js 24** (NodeSource).
4. Instala el **RPM xoa-hl**, que incorpora toda la pila XOA-hl (consulta [`xoa-hl`](/docs/components/xoa-hl): el RPM incluye Xen Orchestra precompilado en `/opt/xo`, y su `%post` activa `redis` y `xo-server`).
5. Sube `xoa-first-boot.sh` / `xoa-credentials.sh` a `/root/` y las dos unidades systemd a `/etc/systemd/system/`, y activa ambas unidades.
6. **Reduce la imagen**: elimina firmware wifi, firewalld, sssd, extras de NetworkManager, rsyslog, documentación/páginas man/info e idiomas distintos del inglés; ejecuta `dnf autoremove` y `clean all`.
7. **Elimina la identidad**: vacía `/etc/machine-id` para que cada VM desplegada genere la suya.

Ajustes principales del constructor: `format: xva_compressed` (salida XVA), `keep_vm: never` (la VM construida se elimina del host XCP-ng) y `vm_name` (`XOA-hl`), que Packer incorpora al XVA como name-label de la VM. Es la etiqueta que muestra XO Lite cuando se despliega el appliance y también determina el archivo de salida, `<vm_name>.xva`.

---

## Autoconfiguración en el primer arranque {#first-boot-self-configuration}

La imagen incluye dos servicios de una sola ejecución; XO Lite escribe los datos de aprovisionamiento en XenStore (`/local/domain/<domid>/vm-data/*`) al desplegar el appliance.

### Fase 1, xoa-first-boot.service {#phase-1-xoa-first-bootservice}

Se ejecuta **antes de que se active la red** (`Before=network.target`, condicionado por `ConditionPathExists=!/var/lib/xoa-first-boot.done`). El script:

- Lee mediante `xenstore-read` las claves `vm-data`: `ip`, `netmask`, `gateway`, `dns`, `ntp-servers`, `system-account-xoa-password` y el bloque JSON `admin-account` (correo electrónico y contraseña).
- Las guarda en `/etc/xoa-first-boot.env` (modo 600).
- Escribe un archivo de claves NetworkManager (`/etc/NetworkManager/system-connections/xoa-provisioned.nmconnection`), con IP estática si se proporciona y DHCP en caso contrario.
- Escribe registros detallados en `/var/log/xoa-first-boot.log` para facilitar el diagnóstico.

### Fase 2, xoa-credentials.service {#phase-2-xoa-credentialsservice}

Se ejecuta una vez **después de** `network-online.target` y `xo-server.service`, condicionado por `!/var/lib/xoa-credentials.done`. El script:

- Espera hasta 3 minutos a xo-server en el puerto 443.
- Establece la contraseña SSH del usuario de sistema `xo` con el valor aprovisionado.
- Registra `xo-cli` en `wss://127.0.0.1` con las credenciales iniciales y llama a `user.changePassword` y `user.set` para aplicar el correo y la contraseña de administrador aprovisionados.
- **Se elimina a sí mismo** al salir (trap): escribe el marcador de finalización, desactiva y elimina ambas unidades y scripts, y borra el archivo de entorno con secretos.

{{< callout type="info" >}}
Si faltan los datos de aprovisionamiento o falla la fase 2, el appliance conserva los valores iniciales `admin@admin.net` / `admin`; cámbialos desde la interfaz web XO después del despliegue.
{{< /callout >}}

---

## Resultados {#outputs}

- La imagen XVA comprimida en `output-xva/`, dentro del directorio de compilación del equipo de compilación.
- La propia VM construida, conservada en el host XCP-ng (`keep_vm: always`).
- En el proceso automático, una **publicación de GitHub en este repositorio** (`Vagrantin/build-xoa-hl`) con etiqueta `xoa-image-<date>-<sha7>` y el artefacto `XOA-hl.xva`, que resuelve el botón de despliegue de XO Lite.

---

## Compilaciones automáticas, el orquestador {#automated-builds-the-orchestrator}

En el proceso diario, el crate `xoa-vm-agent` de [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) sustituye a `setup-xoa-builder.sh`. Realiza los mismos pasos mediante código y, además:

1. Omite la compilación si el HEAD del repositorio ya coincide con el último SHA construido.
2. Primero activa el flujo `build-xoa.yml` de `Vagrantin/xoa-hl` mediante `workflow_dispatch` y espera a la publicación del RPM.
3. Ejecuta `packer validate` y `packer build` con `inst.ks` / `almalinux-build.json` generados.
4. Publica el XVA como una versión de GitHub con etiqueta `xoa-image-<date>-<sha7>` en **`Vagrantin/build-xoa-hl`**, este repositorio (`<sha7>` es el commit de `xoa-hl` con el que se construyó la imagen; ese commit pertenece al otro repositorio, por lo que la etiqueta se crea en `main` y el commit de origen se registra en el cuerpo de la publicación). Las imágenes se registran en la [matriz de versiones](/docs/reference/release-matrix#xoa-hl-releases).

{{< callout type="info" >}}
Las imágenes se publicaban en `Vagrantin/xoa-hl` hasta [#22](https://github.com/Vagrantin/xcp-hl/issues/22). Esas publicaciones se conservan para que las ISO ya distribuidas sigan resolviéndolas; por eso, las herramientas que buscan el RPM en `xoa-hl` deben seguir omitiendo las etiquetas `xoa-image-*`.
{{< /callout >}}

---

## Contribuciones {#contributing}

Para informar de un problema o proponer un cambio, abre una incidencia en [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
