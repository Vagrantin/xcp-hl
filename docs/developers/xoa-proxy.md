---
layout: default
title: xoa-proxy
parent: Developers
nav_order: 1
---

# xoa-proxy
{: .no_toc }

Rust HTTP/HTTPS proxy that streams an XOA image to XAPI.
{: .fs-6 .fw-300 }

**Repository:** [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy)
· Language: Rust · License: GPL-3.0

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Purpose

When XO Lite's patched "Deploy XOA" button is clicked, XAPI needs to import
a `.xva` VM archive. XAPI calls `VM.import` with a URL — it expects the server
at that URL to serve the file over HTTP.

The challenge is that a standard XVA can be several gigabytes. `xoa-proxy` solves this by
**streaming** the file directly to XAPI.

Additionally, XVA files are not inherently compressed, making network transfer
slow on low-bandwidth management networks. `xoa-proxy` decompresses
gzip-compressed images on the fly during streaming.

---

## Design

### Technology choices

| Choice | Rationale |
|---|---|
| **Rust** | Memory safety, good for a long-lived server process in Dom0 |

### Request flow

```
XO Lite (browser)
    │  HTTP GET /image.xva
    ▼
xoa-proxy
    │  
    │ HTTP/HTTPS interface for XAPI
    │ Decompress Gzip format on the fly
    │  
    │  
    │  
    ▼
XAPI VM.import
    │  Writes VDIs to local SR
    ▼
XOA VM created
```

### HTTP vs HTTPS

xoa-proxy supports both HTTP and HTTPS (including self-signed certificates) when fetching
the upstream XOA image. During download, gzip-compressed images are decompressed on the fly
so that XAPI always receives a raw, uncompressed XVA stream.

The handoff to XAPI via VM.import is deliberately served over HTTP/1.0 — XAPI does not
support chunked transfer encoding (an HTTP/1.1 feature), so using HTTP/1.1 framing would
corrupt the import. The proxy handles this constraint internally; callers do not need to
configure anything.

---

## Code structure

```
xoa-proxy/
├── src/
│   └── main.rs        ← HTTP server, request handler, streaming logic
├── tests/             ← Integration tests
├── .cargo/            ← Cargo config (cross-compile settings)
├── Cargo.toml         ← Dependencies: hyper, tokio, tokio-util, ...
└── Cargo.lock
```

### Core streaming pattern

The heart of the proxy is converting a `tokio::fs::File` into a hyper response
body without loading the whole file into memory:

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

## Building

### Prerequisites

- Rust toolchain (stable) — install via [rustup](https://rustup.rs/)
- For cross-compilation to Dom0: `x86_64-unknown-linux-musl` target

```bash
# Native build (for testing)
cargo build

# Cross-compile for Dom0 (static musl binary)
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

The resulting binary at `target/x86_64-unknown-linux-musl/release/xoa-proxy`
is a fully static executable with no shared library dependencies — suitable
for embedding in the XCP-ng DOM0 environment.

### Running locally for development or tests

```bash
# Place a test XVA (or any large file) at the expected path
cp /path/to/test.xva image.xva

# Start the proxy
./target/release/xoa-proxy

# Test streaming
curl -v http://127.0.0.1:3000/image.xva -o /dev/null
```

---

## Configuration

In the current release the listen address and image path are hardcoded.

| Parameter | Current value |
|---|---|
| Listen address | `127.0.0.1:3000` |
| Proxy endpoint | `image.xva` |

---

## GPG signing

The `xoa-proxy` RPM is signed with the **RPM signing subkey** of the
XCP-ng Community Edition keypair. The same subkey is shared with
`xolite-ce` — there is one subkey for all community RPMs.

The public key (`xcp-ng-ce-public.asc`) is the same file distributed with
every release. Importing it once is sufficient to verify any community RPM.

To verify the RPM locally:

```bash
# Option 1 — fetch from keyserver
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# Option 2 — import from the release page
gpg --import xcp-ng-ce-public.asc

# Check the RPM signature
rpm --checksig xoa-proxy-*.rpm
```

In CI, the signing subkeys are stored as a single exported secret (no master key):

| Secret | Content |
|---|---|
| `GPG_PRIVATE_KEY` | ASCII-armored exported signing subkeys |
| `GPG_PASSPHRASE` | Subkey passphrase |

---

## Integration with XO Lite CE

The XO Lite patch in [`xolite-ce`](xolite-ce) sets the deploy URL to
`http://127.0.0.1:3000/image.xva`. This is the address `xoa-proxy` listens
on when started on a XCP-ng CE host.

---

## Testing

```bash
# Run unit and integration tests
cargo test

# Integration tests are in tests/
# They spin up the proxy and verify streaming behaviour
```

---

## Contributing

1. Fork [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy).
2. Create a branch: `git checkout -b feature/my-change`.
3. Run `cargo fmt` and `cargo clippy` before committing.
4. Open a pull request against `main`.
