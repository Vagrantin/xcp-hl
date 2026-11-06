---
title: "Mantener y actualizar el appliance"
linkTitle: "Mantenimiento del appliance"
description: "Anote las versiones instaladas, prepare una ventana de actualización, actualice el appliance y compruebe el resultado."
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: draft
sourceRevision: sha256:39d5583b5b7de077c177e2558dd46fd8e130596274d3c4c7072c9041137ced1c
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Actualice el appliance XOA-HL en cuatro pasos: anote lo instalado, prepare una ventana de mantenimiento, elija cómo se ejecutan las actualizaciones y compruebe el resultado. Trabaje en el **navegador**, conectado a XOA-HL como administrador. Algunas comprobaciones de solo lectura se ejecutan **dentro del appliance**, mediante su consola o SSH.

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio. Los paquetes posteriores pueden comportarse de otra forma.
{{< /callout >}}

## 1. Anote el punto de partida {#record-versions}

1. En el navegador, abra **About** (`/#/about`) como administrador.
2. Anote **XOA-HL version**, **XOA-HL VM version**, la dirección del appliance y la etiqueta de la imagen original. La versión de la VM identifica la compilación de la imagen. Actualizar la aplicación no la cambia.

Si tiene acceso autorizado por consola o SSH, ejecute estos comandos de solo lectura dentro del appliance. Use privilegios de root cuando sea necesario.

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

Guarde la salida junto con la [matriz de versiones](/docs/reference/release-matrix/) y las [notas de versión](/docs/reference/changelog/). La matriz enumera los componentes distribuidos juntos; no demuestra que se hayan probado juntos.

## 2. Prepare la ventana de actualización {#prepare-window}

- [Exporte la configuración de XO](/docs/xoa-hl/configuration-backup/). Guarde el archivo y su frase de contraseña fuera del appliance.
- Anote por separado los cambios en `/root/.config/xo-server/config.toml`, los archivos TLS y `/etc/xoa-hl/update.conf`. La exportación web no incluye estos archivos.
- Compruebe que puede abrir la consola del appliance mediante XO Lite por si la interfaz web queda inaccesible.
- Compruebe que las copias de seguridad, restauraciones y otras tareas de administración han terminado.
- Reserve tiempo suficiente para reiniciar el servicio y, si es necesario, reiniciar después el appliance.

Esta página actualiza únicamente la VM XOA-HL. Actualizar los hosts es otra tarea: consulte la [guía de actualización](/docs/guides/updates/) para elegir el destino y los comandos correctos.

## 3. Elija el modo y el canal {#update-mode-channel}

Abra **Settings → XOA-HL Updates** (`/#/settings/xoa-hl-updates`). Para actualizar manualmente, siga el [procedimiento de actualización](/docs/guides/updates/) para **Check for update** y **Update now**.

Elija un **Mode**:

| Modo | Qué hace |
| --- | --- |
| Manual only | Usted inicia cada comprobación y cada instalación. Es el valor predeterminado |
| Check automatically | Las comprobaciones siguen una programación. Usted decide cuándo instalar |
| Install automatically | La instalación sigue una programación. Úselo solo tras aprobar expresamente la instalación en su ventana de mantenimiento |

Para un modo programado:

1. Compruebe **Appliance timezone**. La programación usa esa zona horaria, no la del host ni la del navegador. Compárela con la salida de `timedatectl`.
2. Configure **Frequency**, **Day** si la programación es semanal y **Local start time**. La ejecución comienza a esa hora, sin retraso aleatorio.
3. Seleccione **Save automatic update settings**.
4. Compruebe los ajustes guardados y la lista de temporizadores de `systemctl list-timers 'xoa-hl-*'`.

En **Update channel**, mantenga **Stable** para el mantenimiento habitual. **Testing** añade paquetes candidatos: úselo solo en un appliance de pruebas desechable. Cambiar el canal no instala nada ni degrada un paquete candidato ya instalado.

La actualización administrada ejecuta una actualización completa con `dnf`, salvo `nodejs`. Instalar el paquete de la aplicación reinicia `xo-server` tras la transacción, por lo que la página web puede desconectarse. Eso por sí solo no significa que la actualización haya fallado.

## 4. Compruebe el resultado {#check-result}

1. Vuelva a conectarse a la interfaz web y abra **About**. Compruebe que muestra la versión de la aplicación esperada.
2. Compruebe que los hosts esperados están conectados y que aparece su inventario.
3. Lea el resultado de la actualización. Al abrirse, la página muestra la última comprobación almacenada, incluida una programada. En **Last automatic result**, una ejecución automática fallida aparece en un aviso rojo.

Si el resultado no está claro, ejecute estas comprobaciones de solo lectura dentro del appliance:

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| Archivo o valor | Qué indica |
| --- | --- |
| `/run/xoa-hl/status` | Última comprobación: `UP_TO_DATE`, `AVAILABLE` o `ERROR`. Se pierde al reiniciar el appliance |
| `/var/lib/xoa-hl/update.log` | Salida de la instalación administrada, terminada con una marca de éxito o fallo. El siguiente intento la sobrescribe |
| `/var/lib/xoa-hl/auto-update.status` | Solo ejecuciones automáticas. Compare `startedAt` y `finishedAt` (UTC) con la hora de su actualización |
| `result=check_failed` o `result=failed` | La comprobación o la instalación falló: lea su registro. Ninguno significa éxito |
| `rebootNeeded=yes`, `no` o `unknown` | Evaluación de la ejecución automática. `unknown` no significa que no sea necesario reiniciar |

Una instalación manual **no** actualiza el registro automático. Un servicio de comprobación puede terminar correctamente y aun así informar de un problema; lea su resultado. Guarde los registros pertinentes antes de volver a intentarlo.

**Comprobación:** **About** muestra la versión esperada, los hosts esperados están conectados y el resultado indica éxito.

## Si la actualización no termina correctamente {#update-problems}

**No hay reinicio automático**. La comprobación y el instalador administrados comparten un bloqueo, pero un comando `dnf` iniciado desde una shell queda fuera de él. Si puede haber una actualización en curso, nunca inicie otro proceso `dnf`, detenga una transacción activa ni reinicie para liberar un actualizador ocupado.

| Problema | Qué comprobar |
| --- | --- |
| Solo se desconectó el navegador | Instalar la aplicación reinicia `xo-server`. Compruebe el servicio y el registro mediante la consola antes de repetir. |
| El actualizador parece ocupado | Compruebe el servicio y el registro mediante la consola. No inicie otro `dnf`, no detenga la transacción ni reinicie para liberarlo. |
| Se perdió una ventana de instalación automática | La instalación perdida no se ejecuta inmediatamente al arrancar de nuevo el appliance. Planifique otra ventana. |
| Se interrumpió el arranque del appliance o el resultado no está claro | Guarde los registros y consulte la [guía de resolución de problemas](/docs/xoa-hl/troubleshooting/) antes de planear otra actualización. |
| Los cambios instalados pueden requerir un reinicio | Reinicie solo cuando no haya transacciones ni tareas de administración en curso y haya decidido que los cambios lo requieren. Después vuelva a comprobar acceso, versiones e inventario. |
| Quiere volver a la versión anterior | Degradar el paquete no es un procedimiento de recuperación probado. No restaura el sistema base, los datos de XO ni sus archivos. Lea primero los [límites de recuperación](/docs/xoa-hl/configuration-backup/#recovery-limits). |

{{< details title="Fuentes" closed="true" >}}
- **Actualizador del appliance**: [programación](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md), [instalador](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-update.sh), [estado de ejecución automática](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-auto-update.sh), [resultado de comprobación](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh), [especificación del paquete](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [parche de canales](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzz-xoa-hl-update-channel.patch), [correcciones de la página de actualización automática](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzzzzz-xoa-hl-auto-update-ui-fixes.patch).
{{< /details >}}
