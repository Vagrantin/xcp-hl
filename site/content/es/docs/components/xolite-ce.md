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

En `xolite-ce@d452937`, `UPSTREAM_TAG` fija `xo-lite-v0.21.0` en `13f987ff3d34504a90b89178489e15fa2293d1b3`. Esa base utiliza un ejecutable Rust incluido para `xoa-deploy.vue`, además de un diff unificado para `XoaButton.vue` y transformaciones explícitas de locales, cargador, versiones de host/invitado y secretos de despliegue. Evidencia: `xolite-ce/.github/workflows/build-xolite-ce.yml@d452937` y `xolite-ce/UPSTREAM_TAG@d452937`.

[El PR de migración](https://github.com/Vagrantin/xolite-ce/pull/26) sustituye el ejecutable incluido por un diff unificado revisable. `patches/series` define el orden de los diffs y `patches/metadata.toml` registra propósito, responsables, origen y dependencias. Las compilaciones y la validación comparten `scripts/patch-source.sh`. Las transformaciones de recursos y locales que no son diffs siguen siendo explícitas. La referencia fijada del origen y los bytes finales del código fuente se conservan.

Consulta la [evaluación del modelo de parcheo entre componentes](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md) para el expediente de decisión y el PR de migración enlazado allí para el estado de implementación. La [guía de mantenimiento del componente](https://github.com/Vagrantin/xolite-ce/blob/7925dbc6bde35bfb387677b2c9c227ef05a886c0/docs/patching.md) describe la rama de migración. Evidencia de implementación: `xolite-ce/scripts/patch-source.sh@7925dbc`,
`xolite-ce/scripts/list-patches.py@7925dbc`, and
`xolite-ce/ci/test-patch-migration.py@7925dbc`.

---

## Validación del código fuente {#source-validation}

Usa una copia limpia del origen fijado. En el árbol migrado de XO Lite CE:

```sh
python3 scripts/list-patches.py patches
python3 ci/test-patch-series.py
bash scripts/patch-source.sh /path/to/clean/pinned/upstream
```

La serie completa se comprueba antes de aplicar cualquier diff. Los nombres no válidos, las entradas ausentes o duplicadas, las discrepancias de metadatos y un orden de dependencias no válido hacen fallar la validación. No omitas los parches fallidos ni los sustituyas por un cargador remoto. Las pruebas existentes del código comprueban por separado la interfaz afectada, las locales y la limpieza del despliegue.

`docs/patch-migration.json` registra el hash del ejecutable antiguo y las revisiones inmutables del consumidor, el origen y el código del parcheador. La comprobación de migración compara todos los bytes del código, los modos ejecutables de Git y los destinos de los enlaces simbólicos entre las dos canalizaciones. La CI además reconstruye el código Rust fijado y compara su salida con el ejecutable registrado. Se trata de una procedencia de comportamiento sobre una entrada fijada, no de reproducibilidad binaria histórica.

---

## Compilaciones y aceptación {#builds-and-acceptance}

Todas las compilaciones de la aplicación y de los RPM se ejecutan en GitHub Actions. La migración añade una comprobación de PR para la canalización completa y la distribución Vue parcheada, sin publicar ninguna release. El empaquetado y la firma permanecen en los flujos de trabajo del componente y en `SPECS/xo-lite-community.spec`.

Mantén la aplicación del código, las compilaciones de la aplicación alojada, las comprobaciones de los RPM y la aceptación en instalación como resultados separados. No hubo ningún aparato en ejecución disponible durante esta migración; el comportamiento desplegado sigue sin verificar.

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
