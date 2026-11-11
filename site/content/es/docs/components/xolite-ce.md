---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/es/developers/xolite-ce.html"]
---

XO Lite recompilado para XCP-hl: selección de imágenes de despliegue XOA y proceso de compilación RPM.
{class="lead"}

**Repositorio:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Lenguaje: TypeScript / Vue 3 (parche) · Especificación RPM · Licencia: AGPL-3.0

## ¿Qué es XO Lite? {#what-is-xo-lite}

XO Lite es la aplicación ligera de gestión de una sola página incluida en cada host XCP-ng. Se ejecuta íntegramente en el navegador, servida directamente por el host, y se implementa como una SPA con Vue 3 / TypeScript / Vite.

En un host XCP-ng estándar, la pantalla **"Deploy XOA"** de XO Lite descarga e importa una imagen fija de Xen Orchestra. XCP-hl sustituye esa pantalla por un selector **"XOA Image URL"** que ofrece cuatro orígenes: XOA-hl (predeterminado), la imagen oficial de Vates, la imagen de Ronivay o una URL XVA personalizada; además, añade el interruptor **"Verify if ssl certificate is valid"** para que `xoa-proxy` pueda aceptar certificados autofirmados en el servidor de origen.

---

## Parcheo del código fuente {#source-patching}

`UPSTREAM_TAG` fija `xo-lite-v0.21.0` en `13f987ff3d34504a90b89178489e15fa2293d1b3`. XO Lite CE modifica ese código fuente mediante diffs unificados revisables. `patches/series` define el orden de los diffs y `patches/metadata.toml` registra, para cada parche, propósito, destino, responsable, commit de origen y dependencias. La serie contiene `xoa-button-empty.patch` para `XoaButton.vue` y `010-xoa-deploy.patch` para `xoa-deploy.vue`. Las compilaciones y la validación comparten `scripts/patch-source.sh`, que también aplica las transformaciones explícitas, sin diff, de locales, cargador, versiones de host/invitado y secretos de despliegue. Evidencia: `xolite-ce/patches/series@ad43fa2`, `xolite-ce/patches/metadata.toml@ad43fa2` y `xolite-ce/scripts/patch-source.sh@ad43fa2`.

Antes del [PR #26](https://github.com/Vagrantin/xolite-ce/pull/26), fusionado el 31 de octubre de 2026 como `4506112`, un ejecutable Rust incluido reescribía `xoa-deploy.vue`. El diff lo sustituyó sin cambiar la referencia fijada del origen ni los bytes finales del código fuente.

Consulta la [evaluación del modelo de parcheo entre componentes](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md) para el expediente de decisión. La [guía de mantenimiento del componente](https://github.com/Vagrantin/xolite-ce/blob/ad43fa282dca7023776a142cb4250e96226d8312/docs/patching.md) establece las reglas de nombres, orden y metadatos.

---

## Validación del código fuente {#source-validation}

Usa una copia limpia del origen fijado. En el árbol de XO Lite CE:

```sh
python3 scripts/list-patches.py patches
python3 ci/test-patch-series.py
bash scripts/patch-source.sh /path/to/clean/pinned/upstream
```

La serie completa se comprueba antes de aplicar cualquier diff. Los nombres no válidos, las entradas ausentes o duplicadas, las discrepancias de metadatos y un orden de dependencias no válido hacen fallar la validación. No omitas los parches fallidos ni los sustituyas por un cargador remoto. Las pruebas existentes del código comprueban por separado la interfaz afectada, las locales y la limpieza del despliegue.

`docs/patch-migration.json` registra el hash del ejecutable retirado y las revisiones inmutables del consumidor, el origen y el código del parcheador. `ci/test-patch-migration.py` compara todos los bytes del código, los modos ejecutables de Git y los destinos de los enlaces simbólicos entre la canalización antigua y la actual. La CI además reconstruye el código Rust fijado y compara su salida con el ejecutable registrado. Se trata de una procedencia de comportamiento sobre una entrada fijada, no de reproducibilidad binaria histórica.

---

## Compilaciones y aceptación {#builds-and-acceptance}

Todas las compilaciones de la aplicación y de los RPM se ejecutan en GitHub Actions. En cada PR, `check-patch-series.yml` ejecuta la canalización completa y compila la distribución Vue parcheada, sin publicar ninguna release. El empaquetado y la firma permanecen en `build-xolite-ce.yml` y `SPECS/xo-lite-community.spec`.

Mantén la aplicación del código, las compilaciones de la aplicación alojada, las comprobaciones de los RPM y la aceptación en instalación como resultados separados. La compilación `0.21.0-39.g54c289b` contiene la serie de diffs unificados. `xcp-hl/qa/ce52-acceptance/2026-11-09.md@7a51eb1` registra esa compilación en un host ce36 instalado, con appliances desplegados mediante el flujo Custom URL incluido en `#/xoa-deploy`. Los demás orígenes de imagen, los demás hosts y una comparación en instalación de antes y después siguen sin verificar.

---

## Firma GPG {#gpg-signing}

El RPM `xo-lite-ce` se firma con la **subclave de firma RPM** del par de claves de XCP-hl. Esa misma subclave firma los RPM `xoa-proxy` y `xcp-hl-release`: existe una subclave compartida para todos los RPM comunitarios.

El proyecto publica su [clave pública](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) compartida en la raíz del sitio de producción. Verifica la huella maestra antes de importarla. Los comandos siguientes requieren una implementación de RPM compatible con subclaves de firma. Dom0 de XCP-ng 8.3 utiliza el antiguo RPM 4.11; los hosts instalados validan los metadatos firmados del repositorio mediante `repo_gpgcheck=1`. Conserva sin cambios los ajustes del repositorio de [Actualizaciones](/docs/guides/updates).

Para verificar el RPM localmente:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Contribuciones {#contributing}

Para informar de un problema o proponer un cambio, abre una incidencia en [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
