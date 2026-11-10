---
title: xoa-proxy
weight: 1
translationKey: xoa-proxy
aliases: ["/de/developers/xoa-proxy.html"]
---

Rust-HTTP-/HTTPS-Proxy, der ein XOA-Image als Stream an XAPI überträgt.
{class="lead"}

**Repository:** [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy)
· Sprache: Rust · Lizenz: AGPL-3.0

## Zweck {#purpose}

Wenn die angepasste Schaltfläche "Deploy XOA" in XO Lite angeklickt wird, muss XAPI ein `.xva`-VM-Archiv importieren. XAPI ruft `VM.import` mit einer URL auf und erwartet, dass der Server dort die Datei ausschließlich über HTTP und im XVA-Format bereitstellt.

Diese eingeschränkte Unterstützung genügte dem Autor nicht und war ursprünglich sogar ein Hindernis, da er Ronivays Image verwendete, das im gz-Format ausschließlich über HTTPS erreichbar ist.

Deshalb dient xoa-proxy als Schnittstelle vor XAPI zur Unterstützung von HTTP und HTTPS (einschließlich selbstsignierter Zertifikate) sowie zusätzlich zum XVA- auch dem gz-Format.

Der Proxy bietet damit die Flexibilität, Images aus verschiedenen, auch lokalen Quellen zu importieren, und erhöht die Sicherheit durch HTTPS-Unterstützung.

---

## Aufbau {#design}

### Technologieentscheidungen {#technology-choices}

| Entscheidung | Begründung |
|---|---|
| **Rust** | Speichersicherheit, geeignet für einen langlebigen Serverprozess in Dom0 |

### Anfrageablauf {#request-flow}

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

### HTTP und HTTPS {#http-vs-https}

xoa-proxy unterstützt HTTP und HTTPS (einschließlich selbstsignierter Zertifikate) beim Abrufen des externen XOA-Images. gzip-komprimierte Images werden während des Downloads entpackt, sodass XAPI stets einen unkomprimierten XVA-Rohdatenstrom erhält.

Die Übergabe an XAPI über VM.import erfolgt bewusst mit HTTP/1.0, da XAPI keine Chunked Transfer Encoding unterstützt (eine HTTP/1.1-Funktion). HTTP/1.1-Framing würde den Import beschädigen. Der Proxy behandelt diese Einschränkung intern; Aufrufer müssen nichts konfigurieren.

---

## Codestruktur {#code-structure}

```
xoa-proxy/
├── src/
│   └── main.rs        ← HTTP server, request handler, streaming logic
├── tests/             ← Integration tests
├── .cargo/            ← Cargo config (cross-compile settings)
├── Cargo.toml         ← Dependencies: hyper, tokio, tokio-util, ...
└── Cargo.lock
```

### Grundmuster für Streaming {#core-streaming-pattern}

Der Kern des Proxys ist die Umwandlung einer `tokio::fs::File` in einen hyper-Antwortkörper, ohne die gesamte Datei in den Arbeitsspeicher zu laden:

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

## Build {#building}

### Voraussetzungen {#prerequisites}

- Stabile Rust-Toolchain, installiert über [rustup](https://rustup.rs/)
- Für Cross-Kompilierung für Dom0: Target `x86_64-unknown-linux-musl`

```bash
# Native build (for testing)
cargo build

# Cross-compile for Dom0 (static musl binary)
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

Das resultierende Programm unter `target/x86_64-unknown-linux-musl/release/xoa-proxy` ist vollständig statisch und benötigt keine gemeinsam genutzten Bibliotheken. Es eignet sich zur Einbindung in die XCP-ng-DOM0-Umgebung.

### Lokal für Entwicklung oder Tests ausführen {#running-locally-for-development-or-tests}

```bash
# Place a test XVA at the expected path
cp /path/to/test.xva image.xva

# Start the proxy
./target/release/xoa-proxy

# Test streaming
curl -v http://127.0.0.1:3000/image.xva -o /dev/null
```

---

## Konfiguration {#configuration}

In der aktuellen Veröffentlichung sind Listen-Adresse und Image-Pfad fest im Code hinterlegt.

| Parameter | Aktueller Wert |
|---|---|
| Listen-Adresse | `127.0.0.1:3000` |
| Proxy-Endpunkt | `image.xva` |

---

## GPG-Signierung {#gpg-signing}

Das `xoa-proxy`-RPM wird mit dem **RPM-Signatur-Unterschlüssel** des XCP-hl-Schlüsselpaars signiert. Derselbe Unterschlüssel wird mit `xolite-ce` geteilt: Es gibt einen Unterschlüssel für beide RPMs.

Das Projekt veröffentlicht seinen gemeinsamen [öffentlichen Schlüssel](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) im Wurzelverzeichnis der Produktionswebsite. Prüfen Sie vor dem Import den Fingerabdruck des Hauptschlüssels. Die folgenden Befehle benötigen eine RPM-Implementierung mit Unterstützung für Signatur-Unterschlüssel. XCP-ng 8.3 Dom0 verwendet das ältere RPM 4.11; installierte Hosts prüfen stattdessen signierte Repository-Metadaten mit `repo_gpgcheck=1`. Behalten Sie die Repository-Einstellungen aus [Updates](/docs/guides/updates) unverändert bei.

So prüfen Sie das RPM lokal:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xoa-proxy-*.rpm
```

---

## Integration mit XO Lite CE {#integration-with-xo-lite-ce}

Der XO-Lite-Patch in [`xolite-ce`](/docs/components/xolite-ce) setzt die Bereitstellungs-URL auf `http://127.0.0.1:3000/image.xva`. Auf dieser Adresse lauscht `xoa-proxy`, wenn es auf einem XCP-hl-Host gestartet wird.

---

## Tests {#testing}

```bash
# Run unit and integration tests
cargo test

# Integration tests are in tests/
# They spin up the proxy and verify streaming behaviour
```

---

## Mitarbeit {#contributing}

Um ein Problem zu melden oder eine Änderung vorzuschlagen, erstellen Sie ein Issue unter [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
