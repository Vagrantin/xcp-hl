---
title: Hoja de ruta
weight: 3
translationKey: roadmap
aliases: ["/es/roadmap.html"]
---

Esta página es una **lista de trabajo de ingeniería mantenida manualmente**, revisada por última vez el **2026-09-28**. Incluye incidencias etiquetadas por componente y trabajo de infraestructura, no compromisos de publicación. Consulta el estado actual en la [lista de incidencias](https://github.com/Vagrantin/xcp-hl/issues).
{class="lead"}

{{< callout type="info" >}}
Las prioridades siguen las etiquetas P1 / P2 / P3 de cada incidencia y pueden cambiar según los comentarios y cambios del proyecto original. Los títulos de las incidencias se muestran tal como están escritos en GitHub. Para proponer o apoyar un elemento, abre una incidencia o comenta una existente en [GitHub](https://github.com/Vagrantin/xcp-hl/issues).
{{< /callout >}}

## A continuación (P1) {#next-up-p1}

- XOA-HL UI translation ([#131](https://github.com/Vagrantin/xcp-hl/issues/131)) · `xoa-hl`
- Jenkins CI step 2: dedicated infra repo (JCasC, plugins, agent image) ([#69](https://github.com/Vagrantin/xcp-hl/issues/69)) · `buildorchestration`
- Local Jenkins CI to replace the orchestrator ([#57](https://github.com/Vagrantin/xcp-hl/issues/57)) · `buildorchestration`
- Review and standardize the patching model ([#43](https://github.com/Vagrantin/xcp-hl/issues/43)) · `xoa-hl`, `xolite-ce`, `xoa-deploy-patcher`
- Clean up old rpm on xolite that are broken. ([#25](https://github.com/Vagrantin/xcp-hl/issues/25)) · `xolite-ce`
- XOA HL patching refactore ([#16](https://github.com/Vagrantin/xcp-hl/issues/16)) · `xoa-deploy-patcher`

## Planificado (P2) {#planned-p2}

- Update the XOA-hl UI to show that a reboot is required ([#102](https://github.com/Vagrantin/xcp-hl/issues/102)) · `xoa-hl`
- goose step 2: choose the integration path into XOA-HL (goosed, ACP, or embedded) ([#83](https://github.com/Vagrantin/xcp-hl/issues/83)) · `xoa-hl`
- goose step 1: headless goose with llama.cpp and mock MCP extensions ([#82](https://github.com/Vagrantin/xcp-hl/issues/82)) · `xoa-hl`
- Model bake-off for natural language VM creation: SLMs against up-to-8B models ([#81](https://github.com/Vagrantin/xcp-hl/issues/81)) · `xoa-hl`
- Jenkins CI step 9: absorb xoa-vm-agent into the Prod pipeline ([#76](https://github.com/Vagrantin/xcp-hl/issues/76)) · `buildorchestration`
- Jenkins CI step 8: promote the ISO smoke test to Test ([#75](https://github.com/Vagrantin/xcp-hl/issues/75)) · `QA`
- Jenkins CI step 5: prove the Dev loop and the promotion path ([#72](https://github.com/Vagrantin/xcp-hl/issues/72)) · `buildorchestration`
- Revisit the unversioned `Obsoletes: xo-lite` workaround when the upstream pin moves ([#42](https://github.com/Vagrantin/xcp-hl/issues/42)) · `xolite-ce`, `xcp-ng-ce-iso`
- update welcome message ([#27](https://github.com/Vagrantin/xcp-hl/issues/27)) · `xoa-hl`
- Add a description of each image after selection on the right side. ([#18](https://github.com/Vagrantin/xcp-hl/issues/18)) · `xolite-ce`
- Complete version matrix of all the bin and RPM ([#15](https://github.com/Vagrantin/xcp-hl/issues/15)) · `xcp-hl`
- Publish gpg public key with the iso ([#10](https://github.com/Vagrantin/xcp-hl/issues/10)) · `xcp-ng-ce-iso`
- make the rpm build github workflows consistent ([#8](https://github.com/Vagrantin/xcp-hl/issues/8)) · `xoa-hl`, `xolite-ce`, `xcp-hl`, `xoa-proxy`

## Más adelante (P3) {#later-p3}

- goose step 6: chat box in the XOA-HL UI wired to goose ([#87](https://github.com/Vagrantin/xcp-hl/issues/87)) · `xoa-hl`
- goose step 5: the create_vm extension behind goose Approve mode ([#86](https://github.com/Vagrantin/xcp-hl/issues/86)) · `xoa-hl`
- goose step 4: read-only platform chat through the XO MCP extension ([#85](https://github.com/Vagrantin/xcp-hl/issues/85)) · `xoa-hl`
- goose step 3: package goose for the appliance, pinned and off by default ([#84](https://github.com/Vagrantin/xcp-hl/issues/84)) · `xoa-hl`
- Natural language VM creation in XOA-HL through a chat box ([#80](https://github.com/Vagrantin/xcp-hl/issues/80)) · `xoa-hl`
- Jenkins CI step 10: absorb iso-agent, retire the dashboard and API ([#77](https://github.com/Vagrantin/xcp-hl/issues/77)) · `buildorchestration`
- `xoa-image-*` release `created_at` is pinned to a static commit, not the actual build time ([#41](https://github.com/Vagrantin/xcp-hl/issues/41)) · `build-xoa-hl`
- Rename xo-lite-ce package ([#40](https://github.com/Vagrantin/xcp-hl/issues/40)) · `xolite-ce`, `xcp-hl`, `xcp-ng-ce-iso`
- Rename xoa-proxy package ([#39](https://github.com/Vagrantin/xcp-hl/issues/39)) · `xoa-hl`, `xcp-hl`, `xoa-proxy`
- Put in place the workflow to get changelog up to date and meaningfull ([#34](https://github.com/Vagrantin/xcp-hl/issues/34)) · `xoa-hl`, `build-xoa-hl`
- RPM LICENSE ([#32](https://github.com/Vagrantin/xcp-hl/issues/32)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Switch "deploy XOA" button on success ([#31](https://github.com/Vagrantin/xcp-hl/issues/31)) · `xolite-ce`
- Need to know which version i'm running ([#30](https://github.com/Vagrantin/xcp-hl/issues/30)) · `xoa-hl`
- change log in github releases ([#24](https://github.com/Vagrantin/xcp-hl/issues/24)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl`, `xoa-proxy`
- xoa-hl release is messy ([#23](https://github.com/Vagrantin/xcp-hl/issues/23)) · `build-xoa-hl`
- Improve the documentation UI ([#19](https://github.com/Vagrantin/xcp-hl/issues/19)) · `xcp-hl`
- Container out of the box ([#7](https://github.com/Vagrantin/xcp-hl/issues/7)) · `xoa-hl`

## Sin prioridad asignada {#not-yet-prioritized}

- Need to update the links ([#132](https://github.com/Vagrantin/xcp-hl/issues/132)) · `xoa-hl`
- Improve the memory footprint ([#64](https://github.com/Vagrantin/xcp-hl/issues/64)) · `xoa-proxy`
- Reduce the number of crate it's uisng ([#63](https://github.com/Vagrantin/xcp-hl/issues/63)) · `xoa-proxy`
- Logrotate is UTC ([#62](https://github.com/Vagrantin/xcp-hl/issues/62)) · `xoa-proxy`
- Refactoring doc ([#60](https://github.com/Vagrantin/xcp-hl/issues/60)) · `xcp-hl`
- investigate forking ([#54](https://github.com/Vagrantin/xcp-hl/issues/54)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- identify backend/frontend code ([#53](https://github.com/Vagrantin/xcp-hl/issues/53)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl-vm`, `build-xoa-hl`, `xoa-deploy-patcher`
- XOA-hl-vm build triggers even if XOA-HL build is in progress ([#48](https://github.com/Vagrantin/xcp-hl/issues/48)) · `build-xoa-hl-vm`, `build-xoa-hl`

## Todavía sin incidencia de seguimiento {#not-yet-tracked-in-an-issue}

Ideas en consideración que todavía no tienen una incidencia.

### Claves GPG: una clave de firma por módulo {#gpg-keys-one-signing-key-per-module}

El modelo GPG armonizado de [xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) está implementado: clave maestra sin conexión y dos subclaves de firma (una para los RPM y otra para la ISO), con clave pública publicada en keys.openpgp.org (consulta [Firma GPG](/docs/components/#gpg-signing)). Mejora pendiente: dividir la subclave RPM compartida para que cada módulo tenga su propia clave, una para el RPM `xo-lite-ce`, otra para el RPM `xoa-proxy` y otra para la ISO.

### Seguimiento automático de versiones originales {#automated-upstream-version-tracking}

El demonio Rust [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) ya activa y supervisa todas las compilaciones de componentes mediante un temporizador diario, omite los componentes cuya última publicación de GitHub ya está actualizada y diagnostica los registros CI fallidos con un LLM local (Ollama). Pendiente: detectar nuevas revisiones XCP-ng 8.x y aumentos de versión XO Lite, y abrir un PR que actualice la referencia fija (por ejemplo, `UPSTREAM_TAG` en `xolite-ce`).

### Soporte de instalación automática con answerfile.xml {#answerfilexml-automated-install-support}

Proporcionar un ejemplo `answerfile.xml` para despliegues HL totalmente desatendidos (arranque PXE / aprovisionamiento con scripts). Requiere inyectar el archivo de respuestas dentro de `install.img` (SquashFS), algo que el proceso de compilación actual ya admite.

## Completado {#completed}

| Elemento | Publicado |
|---|---|
| Almacenamiento ISO predeterminado: partición de 20 GB reservada al instalar y registrada como SR de ISO en el primer arranque ([#2](https://github.com/Vagrantin/xcp-hl/issues/2), [#46](https://github.com/Vagrantin/xcp-hl/issues/46)) | Sep 2026 |
| Edición XOA-hl: eliminados los menús sujetos a licencia y el aviso de ausencia de soporte; imagen construida desde el código fuente y seleccionable para despliegue en XO Lite ([#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6)) | Jul 2026 |
| Versionado y notas de publicación automáticos para los RPM y la ISO ([#4](https://github.com/Vagrantin/xcp-hl/issues/4)) | Jul 2026 |
| Sitio de documentación publicado automáticamente en cada push mediante CI de GitHub Pages ([#5](https://github.com/Vagrantin/xcp-hl/issues/5)) | Jun 2026 |
| Modelo de firma GPG: clave maestra sin conexión y subclaves RPM/ISO, clave pública en keys.openpgp.org ([#3](https://github.com/Vagrantin/xcp-hl/issues/3)) | May 2026 |
| Primeras compilaciones del appliance XOA-hl modificado (`xoa-hl` + `build-xoa-hl`) | Jul 2026 |
| Demonio de orquestación de compilaciones diarias (`buildorchestration`) | Jul 2026 |
| Fijación de la versión original de xo-lite (`UPSTREAM_TAG`) | Jul 2026 |
| Parche inicial de XO Lite (endpoint de despliegue comunitario) | v8.3-ce Abr 2026 |
| Servidor Rust de transmisión `xoa-proxy` | v8.3-ce Abr 2026 |
| Proceso de compilación RPM e ISO firmados con GPG en dos repositorios | v8.3-ce Abr 2026 |
| GitHub Actions CI/CD | v8.3-ce Abr 2026 |
| Campos de credenciales de solo lectura en la vista de despliegue XO Lite | v8.3-ce Abr 2026 |

