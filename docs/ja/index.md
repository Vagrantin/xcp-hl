---
layout: default
title: 日本語
nav_order: 11
has_children: true
lang: ja
---

# XCP-ng HomeLab Edition
{: .fs-9 }

コミュニティが作った無料の XCP-ng ISO です。公式の Xen Orchestra（XOA）の
代わりに、完全に**セルフホスト**の Xen Orchestra を使います。コミュニティ製の
XOA イメージを簡単に展開できるようにすることが目的で、おもにホームラボの
利用者を対象にしています。
{: .fs-6 .fw-300 }

> ### ⚠️ アルファ版のソフトウェアです
>
> **XCP-ng HomeLab Edition はアルファ版です。** 現在も活発に開発中で、
> 安定化のための工程をまだ通っていません。**リリースのたびに互換性のない
> 変更が入ると考えてください。** コンポーネントのバージョン、パッケージ名、
> リポジトリの構成、アップデートの動作はいずれも変わる可能性があり、
> その場でのアップデートにホスト側の手作業が必要になることもあります。
>
> 一から作り直してもかまわないハードウェアとデータの上で使ってください。
> バグの報告やご意見は
> [GitHub](https://github.com/Vagrantin/xcp-hl/issues) までお寄せください。

[最新の ISO をダウンロード](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHub で見る](https://github.com/Vagrantin/xcp-hl){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## XCP-ng HomeLab Edition とは

[XCP-ng](https://xcp-ng.org/) は Xen Project をベースにした、強力な
オープンソースのタイプ 1 ハイパーバイザーです。公式版には、ブラウザーで動く
軽量な管理画面 **XO Lite** と、公式の
**Xen Orchestra アプライアンス（XOA）**をワンクリックで展開するボタンが
付いています。

**XCP-hl** は XCP-ng の良いところをそのまま残しつつ、このボタンだけを
コミュニティが保守するワークフローに置き換えます。
導入後は、XOA を展開する方法を次の 3 通りから選べます。
- ホームラボ向けの XOA イメージ（既定）
- Vates 公式の XOA イメージ
- Ronivay 氏のイメージ（最新版を追いかけるもの）
- 独自のイメージ

目的の 1 つは、商用サポートがないことを知らせるバナーや、ライセンスが必要な
機能を取り除いた、軽量な XOA イメージを提供することです。これにより、
ホームラボの利用者にとって XOA が扱いやすくなります。このイメージ
**XOA-HL** は、[`xoa-hl`](https://github.com/Vagrantin/xoa-hl) と
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) の 2 つの
リポジトリから作られます。

安定性と保守のしやすさのため、変更を加えた 2 つのコンポーネントは
**特定のアップストリームのバージョンに固定**しています。アップストリームの
`master` に対してビルドするのは危険が大きく、アップストリームが動くたびに
ビルドが壊れる可能性が高いためです。XO Lite HL は固定したアップストリームの
タグ（現在は `xo-lite-v0.21.0`）から、XOA-HL は固定した Xen Orchestra の
コミット（現在は `5.113.2`。XO 5.x の最後のリリース）からビルドします。
つまり今のところ、**XOA-HL の既定の Web 画面は XO v6 ではなく XO v5** です。
固定するバージョンは、テストのうえで意図的にしか上げません。そのため
アップストリームの変更で既存の環境が壊れることはありません。各リリースに
含まれる正確なバージョンは[リリース一覧表](release-matrix.html)に記録して
います。

---

## ダウンロード

{: .note }
すべての ISO と RPM のリリースは **XCP-ng HomeLab Edition の GPG 鍵**で
署名しています。インストールの前にダウンロードしたファイルを検証して
ください。

[⬇ ISO をダウンロード](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest){: .btn .btn-primary }

### ISO を検証する

コミュニティの GPG 鍵は
[keys.openpgp.org](https://keys.openpgp.org) で公開しています。

| 項目 | 値 |
|---|---|
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

---

## クイックスタート

### 1 · XCP-hl をインストールする
ISO から起動し、
[公式のインストール手順](https://docs.xcp-ng.org/installation/install-xcp-ng/)
に従ってください。インストーラーの見た目と動きはアップストリームの
XCP-ng 8.3 と同じです。

**100 GB 以上のディスクを使ってください。** XCP-HL は、システム用の
パーティションが使う約 41.5 GB に加えて、すぐ使える ISO ライブラリー用に
20 GB のパーティションを確保します。残りの約 38.5 GB が VM の
ストレージになります。これより小さいディスクでもインストールは成功しますが、
ISO ライブラリーは作られず、XCP-ng 標準の構成になります。
[ISO ストレージ](features.html#iso-storage)を参照してください。

### 2 · XO Lite を開く
インストール後、ブラウザーで次のアドレスを開きます。

```
http://<ホストの IP アドレス>
```

XCP-ng の root の資格情報で XO Lite にログインします。

### 3 · XOA を展開する
XO Lite で **Deploy XOA** をクリックします。必要な情報（IP アドレス、
ユーザー、パスワードなど）を入力してください。
展開を開始すると、XO Lite は同梱の
[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) を呼び出し、
XOA イメージ（たとえば `image.xva.gz`）を XAPI へそのまま流し込みます。
詳しくは「開発者向け / xoa-proxy」の節を参照してください。

### 4 · XO をホストに接続する
XOA の VM が起動したら、ブラウザーで開いて XCP-ng ホストを追加します。

```
Settings → Servers → Add server
Host : <XCP ホストの IP アドレス>
User : root
```

### 5 · 最新の状態に保つ
XCP-HL は各コンポーネントを署名済みの RPM として配布するため、稼働中の
ホストをその場でアップデートできます。利用できるアップデートは Xen Orchestra
の `Home > Hosts > <対象のホスト> > Patches` に表示されます。仕組み、
古いホストでの初期設定、切り戻しについては
[アップデート](updates.html)を参照してください。

---

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

---

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

技術的な詳細はすべて[開発者向けの節](developers/)にあります。

---

## ライセンス

XCP-hl は **GNU Affero 一般公衆ライセンス v3.0**（AGPL-3.0）で公開して
います。アップストリームの XCP-ng（Apache 2.0 / GPL のコンポーネント）と
Xen Orchestra（AGPL-3.0）の上に成り立っています。

> XCP-ng Home lab Edition は独立したコミュニティのプロジェクトです。
> XCP-ng の下流にあたりますが、Vates SAS や XCP-ng プロジェクトとの提携は
> なく、両者による推奨やサポートも受けていません。
