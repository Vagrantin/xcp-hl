---
title: はじめに
weight: 0
translationKey: getting-started
---

XCP-hl をインストールし、XOA を展開し、ホストを最新の状態に保ちます。
{class="lead"}

## ダウンロードと検証

{{< callout type="info" >}}
すべての ISO と RPM のリリースは **XCP-hl の GPG 鍵**で署名しています。
インストールの前にダウンロードしたファイルを検証してください。
{{< /callout >}}

[⬇ 最新の ISO をダウンロード](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest)

### ISO を検証する

コミュニティの GPG 鍵は [keys.openpgp.org](https://keys.openpgp.org) で公開しています。

| 項目 | 値 |
|---|---|
| 鍵の UID | `XCP-ng Community Edition (Master signing key)`（`gpg --list-keys` に表示される文字列） |
| 鍵のファイル | `xcp-ng-ce-public.asc`（各リリースに添付） |
| メールアドレス | `xcp-ng-ce.lid530@passmail.com` |
| フィンガープリント | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |

```bash
# 方法 1 — 鍵サーバーから取得する
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# 方法 2 — リリースページからインポートする
gpg --import xcp-ng-ce-public.asc

# ISO のチェックサムファイルの署名を検証する
# （チェックサムファイルの名前は ISO に合わせています。例は v8.3-ce9 のもの）
gpg --verify xcp-ng-8.3-ce9.iso.sha256.asc xcp-ng-8.3-ce9.iso.sha256

# ISO を検証する
sha256sum -c xcp-ng-8.3-ce9.iso.sha256
```

## クイックスタート

### 1 · XCP-hl をインストールする

ISO から起動し、
[公式のインストール手順](https://docs.xcp-ng.org/installation/install-xcp-ng/)
に従ってください。インストーラーの見た目と動きはアップストリームの
XCP-ng 8.3 と同じです。

**100 GB 以上のディスクを使ってください。** XCP-hl は、システム用の
パーティションが使う約 41.5 GB に加えて、すぐ使える ISO ライブラリー用に
20 GB のパーティションを確保します。残りの約 38.5 GB が VM の
ストレージになります。これより小さいディスクでもインストールは成功しますが、
ISO ライブラリーは作られず、XCP-ng 標準の構成になります。
[ISO ストレージ](/docs/guides/features#iso-storage)を参照してください。

### 2 · XO Lite を開く

インストール後、ブラウザーで次のアドレスを開きます。

```
http://<ホストの IP アドレス>
```

ホストの root の資格情報（インストール時に設定したもの）で XO Lite に
ログインします。

### 3 · XOA を展開する

XO Lite で **Deploy XOA** をクリックします。必要な情報（IP アドレス、
ユーザー、パスワードなど）を入力してください。
展開を開始すると、XO Lite は同梱の
[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) を呼び出し、
XOA イメージ（たとえば `image.xva.gz`）を XAPI へそのまま流し込みます。
詳しくは[xoa-proxy コンポーネントのページ](/docs/components/xoa-proxy)を
参照してください。

### 4 · XO をホストに接続する

XOA の VM が起動したら、ブラウザーで開いて XCP-hl ホストを追加します。

```
Settings → Servers → Add server
Host : <XCP ホストの IP アドレス>
User : root
```

### 5 · 最新の状態に保つ

XCP-hl は各コンポーネントを署名済みの RPM として配布するため、稼働中の
ホストをその場でアップデートできます。利用できるアップデートは Xen Orchestra
の `Home > Hosts > <対象のホスト> > Patches` に表示されます。仕組み、
古いホストでの初期設定、切り戻しについては
[アップデート](/docs/guides/updates)を参照してください。

## アーキテクチャの概要

```
┌──────────────────────────────────────────────────────────────┐
│                    XCP-hl ホスト                             │
│                                                              │
│  ┌──────────────┐  パッチ   ┌──────────────────────────────┐ │
│  │  XO Lite HL  │ ────────► │  DeployXoaView（コミュニティ）│ │
│  │              │           │                              │ │
│  └──────┬───────┘           └───────────┬──────────────────┘ │
│         │                               │ HTTP               │
│  ┌──────▼───────────────────────────────▼──────────────────┐ │
│  │                   xoa-proxy                             │ │
│  │      HTTP · HTTPS · gzip · XVA のストリーム配信         │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │ XAPI VM.import                 │
│  ┌──────────────────────────▼──────────────────────────────┐ │
│  │                   XAPI / Dom0                           │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## コンポーネント

| リポジトリ | 役割 |
|---|---|
| [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) | ドキュメント |
| [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) | XO Lite のコミュニティパッチ + RPM ビルド |
| [`xcp-ng-ce-iso`](https://github.com/Vagrantin/xcp-ng-ce-iso) | ISO の組み立てとリリース |
| [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) | XVA 配信用の Rust 製 HTTP/gzip プロキシ + RPM ビルド |
| [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) | ホームラボ向けに手を入れた Xen Orchestra アプライアンス（XOA-HL）。画面を簡素化し、RPM とコンテナをビルド |
| [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) | XCP-ng 上で XOA の XVA イメージをビルドし、リリースとして公開する Packer のパイプライン |
| [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) | Rust 製のビルドオーケストレーター。すべてのコンポーネントのビルドを毎日実行し、監視して原因を診断します |

技術的な詳細はすべて[コンポーネントの節](/docs/components/)にあります。

## ライセンス

XCP-hl は **GNU Affero 一般公衆ライセンス v3.0**（AGPL-3.0）で公開して
います。アップストリームの XCP-ng（Apache 2.0 / GPL のコンポーネント）と
Xen Orchestra（AGPL-3.0）の上に成り立っています。

> XCP-hl は独立したコミュニティのプロジェクトです。
> XCP-ng の下流にあたりますが、Vates SAS や XCP-ng プロジェクトとの提携は
> なく、両者による推奨やサポートも受けていません。
