---
layout: default
title: xoa-proxy
parent: 開発者向け
grand_parent: 日本語
nav_order: 1
lang: ja
---

# xoa-proxy
{: .no_toc }

XOA のイメージを XAPI へ流し込む、Rust 製の HTTP/HTTPS プロキシです。
{: .fs-6 .fw-300 }

**リポジトリ：** [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy)
· 言語：Rust · ライセンス：AGPL-3.0

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 目的

XO Lite で手を入れた「Deploy XOA」ボタンを押すと、XAPI は `.xva` という
VM のアーカイブを取り込む必要があります。XAPI は URL を指定して `VM.import`
を呼びますが、その URL のサーバーには HTTP でのみファイルを配信することを
求め、ファイルは XVA 形式でなければなりません。

この制約は私にとって物足りないもので、当初は行き詰まりの原因でもありました。
Ronivay 氏のイメージを使っていたのですが、これは gz 形式で、HTTPS でしか
取得できなかったからです。

そのため xoa-proxy は、XAPI の手前に立つ窓口として、HTTP と HTTPS
（自己署名証明書を含む）に対応し、さらに XVA に加えて gz 形式にも対応
します。

このプロキシがあることで、ローカルを含むさまざまな場所からイメージを取り込む
柔軟性が生まれ、HTTPS への対応によって安全性も高まります。

---

## 設計

### 技術の選択

| 選択 | 理由 |
|---|---|
| **Rust** | メモリー安全性が高く、Dom0 で長時間動き続けるサーバープロセスに向いています |

### リクエストの流れ

```
XO Lite（ブラウザー）
    │  HTTP GET /image.xva
    ▼
xoa-proxy
    │
    │ XAPI 向けの HTTP/HTTPS の窓口
    │ gzip 形式をその場で展開
    │
    ▼
XAPI VM.import
    │  ローカルの SR に VDI を書き込む
    ▼
XOA の VM が作成される
```

### HTTP と HTTPS

xoa-proxy は、上流の XOA イメージを取得するときに HTTP と HTTPS の両方
（自己署名証明書を含む）に対応します。ダウンロード中、gzip で圧縮された
イメージはその場で展開されるため、XAPI が受け取るのは常に圧縮されていない
生の XVA のストリームです。

XAPI への `VM.import` による受け渡しは、意図的に HTTP/1.0 で行っています。
XAPI はチャンク転送エンコーディング（HTTP/1.1 の機能）に対応していないため、
HTTP/1.1 の形式を使うと取り込みが壊れてしまいます。プロキシがこの制約を
内部で処理するので、呼び出す側で設定することはありません。

---

## コードの構成

```
xoa-proxy/
├── src/
│   └── main.rs        ← HTTP サーバー、リクエストの処理、ストリームの制御
├── tests/             ← 結合テスト
├── .cargo/            ← Cargo の設定（クロスコンパイルの設定）
├── Cargo.toml         ← 依存：hyper、tokio、tokio-util など
└── Cargo.lock
```

### ストリーム処理の中心となる書き方

このプロキシの中心は、`tokio::fs::File` を、ファイル全体をメモリーに
読み込むことなく hyper のレスポンスボディに変換する部分です。

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

## ビルド

### 事前に必要なもの

- Rust のツールチェーン（stable）— [rustup](https://rustup.rs/) で導入します
- Dom0 向けのクロスコンパイルには `x86_64-unknown-linux-musl` ターゲット

```bash
# ネイティブのビルド（テスト用）
cargo build

# Dom0 向けのクロスコンパイル（musl の静的バイナリー）
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

できあがる
`target/x86_64-unknown-linux-musl/release/xoa-proxy` は、共有ライブラリーに
依存しない完全な静的実行ファイルで、XCP-ng の DOM0 環境に組み込むのに
適しています。

### 開発やテストのためにローカルで動かす

```bash
# テスト用の XVA を所定のパスに置く
cp /path/to/test.xva image.xva

# プロキシを起動する
./target/release/xoa-proxy

# ストリーム配信を試す
curl -v http://127.0.0.1:3000/image.xva -o /dev/null
```

---

## 設定

現在のリリースでは、待ち受けアドレスとイメージのパスはコードに直接書かれて
います。

| 項目 | 現在の値 |
|---|---|
| 待ち受けアドレス | `127.0.0.1:3000` |
| プロキシのエンドポイント | `image.xva` |

---

## GPG 署名

`xoa-proxy` の RPM は、XCP-ng Community Edition の鍵ペアの
**RPM 署名用サブキー**で署名しています。このサブキーは `xolite-ce` と
共通で、2 つの RPM に対してサブキーは 1 つだけです。

公開鍵（`xcp-ng-ce-public.asc`）は、どのリリースにも同じものが添付されて
います。一度インポートすれば、コミュニティのどの RPM でも検証できます。

ローカルで RPM を検証するには次のようにします。

```bash
# 方法 1 — 鍵サーバーから取得する
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# 方法 2 — リリースページからインポートする
gpg --import xcp-ng-ce-public.asc

# RPM の署名を確認する
rpm --checksig xoa-proxy-*.rpm
```

---

## XO Lite CE との連携

[`xolite-ce`](xolite-ce.html) の XO Lite パッチは、展開先の URL を
`http://127.0.0.1:3000/image.xva` に設定します。これは、XCP-ng HL のホストで
起動したときに `xoa-proxy` が待ち受けるアドレスです。

---

## テスト

```bash
# ユニットテストと結合テストを実行する
cargo test

# 結合テストは tests/ にあります
# プロキシを起動して、ストリーム配信の動作を確認します
```

---

## 開発に参加する

1. [Vagrantin/xoa-proxy](https://github.com/Vagrantin/xoa-proxy) を
   フォークします。
2. ブランチを作ります：`git checkout -b feature/my-change`。
3. コミットの前に `cargo fmt` と `cargo clippy` を実行します。
4. `main` に対してプルリクエストを作ります。
