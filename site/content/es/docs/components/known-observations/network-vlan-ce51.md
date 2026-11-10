---
title: "Observación de VLAN en el asistente de red (ce51)"
translationKey: network-vlan-ce51
excludeSearch: true
weight: 90
---

## Alcance

Esta es una observación parcial, limitada a una versión, de SN04 (fila 14 del inventario), realizada el 2026-11-03 en la celda completa n del Grupo A. El host anidado XCP-HL 8.3.0 compilación ce55 ejecutó un appliance XOA-HL instalado desde RPM, `xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64` (etiqueta `v5.113.2_e281c536-ce51`, servidor XO 5.193.1, AlmaLinux 9.8). No era la imagen XVA publicada. No se afirma nada sobre otras versiones ni vías de instalación, incluido el XVA ce52.

## Observado

En New network, al introducir la VLAN 392 y dejar Interface vacío se creó una red sin PIF y sin objeto VLAN, sin ningún error ni aviso. El texto del campo VLAN decía “No VLAN if empty”, mientras que el capítulo decía que un valor vacío se envía como 0. Tras usar el asistente con el enlace ascendente libre, el PIF de la VLAN indicó `carrier=false` aunque el enlace del sistema operativo estaba activo y se vieron 12 tramas etiquetadas en `eth1` anidado.

Fue solo un resultado parcial: no hubo segundo miembro del pool, comprobación entre hosts ni escenario de recuperación. El resultado del portador se registra tal como se observó; aquí no se establece su significado.

## Plan de corrección tras la beta

Después del lanzamiento de la beta, hay que inspeccionar el formulario del asistente, la construcción de la solicitud y la ruta del backend que crea la red y el PIF. A continuación:

1. Hacer que una VLAN sin interfaz no sea válida en la interfaz, con un mensaje de validación claro; confirmar que el backend también rechaza o gestiona de forma segura la solicitud equivalente.
2. Elegir y documentar un único significado para una VLAN vacía, y alinear el texto del campo, el capítulo, el valor de la solicitud y el comportamiento del backend.
3. Contrastar el valor de portador del PIF de la VLAN con el estado del enlace del host y la observación de paquetes. Corregirlo solo si su contrato es erróneo; si no, documentar qué significa el indicador.
4. Añadir cobertura automatizada para la validación, la VLAN vacía y la semántica del portador.
5. Ejecutar primero una aceptación específica en un appliance desechable derivado de la beta. Solo después de revisar esa evidencia, probar un candidato ce52 mediante la vía XVA de XO Lite admitida. Registrar la identidad del XVA, el host y la compilación, los pasos y los resultados antes de hacer cualquier afirmación sobre ce52.

No atribuyas este resultado del RPM ce51 en host anidado al XVA ce52 sin esa prueba independiente.
