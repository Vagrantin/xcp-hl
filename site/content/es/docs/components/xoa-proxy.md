---
title: xoa-proxy
weight: 1
translationKey: xoa-proxy
aliases: ["/developers/xoa-proxy.html"]
---

Proxy HTTP/HTTPS en Rust que transmite una imagen XOA a XAPI.
{class="lead"}

**Repositorio:** [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy)
· Lenguaje: Rust · Licencia: AGPL-3.0

## Objetivo {#purpose}

Cuando se pulsa el botón modificado "Deploy XOA" de XO Lite, XAPI debe importar un archivo de VM `.xva`. XAPI llama a `VM.import` con una URL y espera que el servidor sirva el archivo exclusivamente por HTTP y en formato XVA.

Ese soporte limitado no satisfacía mis necesidades y, al principio, incluso suponía un impedimento: dependía de la imagen de Ronivay, que está comprimida en formato gz y solo es accesible mediante https.

Por eso, xoa-proxy actúa como interfaz delante de XAPI para admitir HTTP y HTTPS (incluidos certificados autofirmados) y, además del formato XVA, también gz.

El proxy permite importar imágenes desde distintos orígenes, incluso locales, y aumenta la seguridad al incorporar soporte HTTPS.

---

## Diseño {#design}

### Elecciones tecnológicas {#technology-choices}

| Elección | Motivo |
|---|---|
| **Rust** | Seguridad de memoria, adecuada para un proceso servidor de larga duración en Dom0 |

### Flujo de solicitudes {#request-flow}

```
XO Lite (browser)
    │  HTTP GET /image.xva
    ▼
xoa-proxy
    │  
    │ HTTP/HTTPS interface for XAPI
    │ Decompress Gzip format on the fly
    │  
    ▼
XAPI VM.import
    │  Writes VDIs to local SR
    ▼
XOA VM created
```

### HTTP frente a HTTPS {#http-vs-https}

xoa-proxy admite tanto HTTP como HTTPS (incluidos certificados autofirmados) al obtener la imagen XOA del servidor de origen. Durante la descarga, las imágenes comprimidas con gzip se descomprimen sobre la marcha, para que XAPI siempre reciba un flujo XVA sin comprimir.

La entrega a XAPI mediante VM.import se sirve deliberadamente por HTTP/1.0, porque XAPI no admite la codificación de transferencia por fragmentos (una función de HTTP/1.1), por lo que usar el formato de mensajes HTTP/1.1 corrompería la importación. El proxy gestiona esta limitación internamente; quienes lo llaman no necesitan configurar nada.

---

## Estructura del código {#code-structure}

```
xoa-proxy/
├── src/
│   └── main.rs        ← HTTP server, request handler, streaming logic
├── tests/             ← Integration tests
├── .cargo/            ← Cargo config (cross-compile settings)
├── Cargo.toml         ← Dependencies: hyper, tokio, tokio-util, ...
└── Cargo.lock
```

### Patrón principal de transmisión {#core-streaming-pattern}

La parte central del proxy convierte un `tokio::fs::File` en el cuerpo de una respuesta hyper sin cargar el archivo completo en memoria:

```rust
use tokio_util::io::ReaderStream;
use hyper::Body;

let file = tokio::fs::File::open("image.xva").await?;
let stream = ReaderStream::new(file);
let body = Body::wrap_stream(stream);

let response = Response::builder()
    .header("Content-Type", "application/octet-stream")
    .header("Content-Encoding", "gzip")
    .body(body)?;
```

---

## Compilación {#building}

### Requisitos previos {#prerequisites}

- Herramientas Rust (stable), instaladas mediante [rustup](https://rustup.rs/)
- Para compilación cruzada destinada a Dom0: objetivo `x86_64-unknown-linux-musl`

```bash
# Native build (for testing)
cargo build

# Cross-compile for Dom0 (static musl binary)
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

El binario resultante en `target/x86_64-unknown-linux-musl/release/xoa-proxy` es un ejecutable completamente estático, sin dependencias de bibliotecas compartidas, adecuado para integrarlo en el entorno DOM0 de XCP-ng.

### Ejecución local para desarrollo o pruebas {#running-locally-for-development-or-tests}

```bash
# Place a test XVA at the expected path
cp /path/to/test.xva image.xva

# Start the proxy
./target/release/xoa-proxy

# Test streaming
curl -v http://127.0.0.1:3000/image.xva -o /dev/null
```

---

## Configuración {#configuration}

En la versión actual, la dirección de escucha y la ruta de la imagen están fijadas en el código.

| Parámetro | Valor actual |
|---|---|
| Dirección de escucha | `127.0.0.1:3000` |
| Endpoint del proxy | `image.xva` |

---

## Firma GPG {#gpg-signing}

El RPM `xoa-proxy` se firma con la **subclave de firma RPM** del par de claves de XCP-hl. Esa misma subclave se comparte con `xolite-ce`: existe una subclave para ambos RPM.

El proyecto publica su [clave pública](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) compartida en la raíz del sitio de producción. Verifica la huella maestra antes de importarla. Los comandos siguientes requieren una implementación de RPM compatible con subclaves de firma. Dom0 de XCP-ng 8.3 utiliza el antiguo RPM 4.11; los hosts instalados validan los metadatos firmados del repositorio mediante `repo_gpgcheck=1`. Conserva sin cambios los ajustes del repositorio de [Actualizaciones](/docs/guides/updates).

Para verificar el RPM localmente:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xoa-proxy-*.rpm
```

---

## Integración con XO Lite CE {#integration-with-xo-lite-ce}

El parche de XO Lite en [`xolite-ce`](/docs/components/xolite-ce) establece la URL de despliegue en `http://127.0.0.1:3000/image.xva`. Es la dirección en la que escucha `xoa-proxy` cuando se inicia en un host XCP-hl.

---

## Pruebas {#testing}

```bash
# Run unit and integration tests
cargo test

# Integration tests are in tests/
# They spin up the proxy and verify streaming behaviour
```

---

## Contribuciones {#contributing}

Para informar de un problema o proponer un cambio, abre una incidencia en [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
