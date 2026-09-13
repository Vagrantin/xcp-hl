---
layout: default
title: 開発者向け
parent: 日本語
nav_order: 8
has_children: true
lang: ja
---

# 開発者向けドキュメント
{: .no_toc }

XCP-hl を理解し、ビルドし、開発に加わるために必要なことをまとめています。
{: .fs-6 .fw-300 }

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## リポジトリの全体像

XCP-hl は、いくつかの機能別のリポジトリと、このドキュメント用の
リポジトリに分かれています。

```
Vagrantin/xcp-hl          ← ドキュメント（このサイト）
      │
      ├── Vagrantin/xolite-ce       ← XO Lite のパッチ + RPM ビルド
      │         │ 署名済み RPM を GitHub リリースの成果物として公開
      │         │
      ├─────────│───Vagrantin/xoa-proxy           ← Rust 製 HTTP プロキシ + RPM ビルド
      │         │        │  署名済み RPM を GitHub リリースの成果物として公開
      │         ▼        ▼
      ├── Vagrantin/xcp-ng-ce-iso   ← ISO の組み立て + ISO の GitHub リリース
      │         │ xolite-ce と xoa-proxy から RPM を取得し、ISO を組み立て
      │
      ├── Vagrantin/xoa-hl          ← XOA-HL：手を入れた Xen Orchestra（RPM + コンテナ）
      │         ▼
      ├── Vagrantin/build-xoa-hl    ← Packer のパイプライン → XCP-ng 上で XOA の XVA イメージを作成
      │         │ XVA を GitHub リリースとして公開（xoa-image-* タグ）
      │
      └── Vagrantin/buildorchestration ← Rust 製オーケストレーター：すべてのビルドを実行・監視
```

各リポジトリはそれぞれの GitHub Actions のパイプラインを持っています。
これらは**疎結合**です。`xolite-ce` と `xoa-proxy` はバージョン付きの RPM
成果物を公開し、`xcp-ng-ce-iso` はそれをリリースタグで取得します。通常の
ビルドで、これらを同時にチェックアウトする必要はありません。`xoa-hl` は
コミュニティが手を入れた Xen Orchestra（XOA-HL）をビルドし、
`build-xoa-hl` がそれを XVA イメージにまとめます。`buildorchestration` は
その上に立ち、パイプライン全体を毎日のスケジュールで動かします
（後述の[ビルドの統括](#build-orchestration)を参照）。

---

## 技術スタック

| 層 | 技術 |
|---|---|
| ハイパーバイザーの土台 | XCP-ng 8.3（Xen 4.17、Dom0 は Linux 4.19） |
| XO Lite の画面 | Vue 3 · TypeScript · Vite · Pinia（`@xen-orchestra/lite`） |
| XO Lite のビルド | Yarn（Corepack）· `yarn build:xo-lite` |
| RPM のパッケージング | `rpmbuild`、`rpmsign`、`createrepo_c` |
| ISO の組み立て | `create-install-image`（XCP-ng のツールチェーン、master ブランチ） |
| ISO 関連のツール | `mksquashfs`、`xorriso`、`isohybrid`、`implantisomd5` |
| XOA-HL のビルド | Node.js 24 · Yarn workspaces · AlmaLinux 9 のコンテナ |
| XVA イメージのビルド | Packer · `ddelnano/xenserver` プラグイン · Kickstart |
| ビルド環境 | Docker（`xcp-ng-build-env:8.3`） |
| プロキシサーバー | Rust · `hyper` · `tokio` · `tokio_util::io::ReaderStream` |
| CI/CD | GitHub Actions |
| 署名 | GPG — オフラインのマスターキー + 2 つの署名用サブキー（後述） |

---

## ビルドのパイプライン — 最初から最後まで

```
1. xolite-ce の CI（GitHub Actions）
   ├── UPSTREAM_TAG で固定したタグで vatesfr/xen-orchestra をクローン
   │   （現在は xo-lite-v0.21.0。自動ではなく意図的に更新）
   ├── patches/community-xoa-deploy.patch を適用
   ├── yarn build:xo-lite
   ├── rpmbuild → xo-lite-community-<VERSION>.rpm
   ├── RPM 署名用サブキーで rpmsign（GPG_PRIVATE_KEY + GPG_PASSPHRASE）
   └── 署名済み RPM を GitHub リリースの成果物として公開（公開鍵は
       keys.openpgp.org。インポート手順はリリースノートに記載）

2. xoa-proxy の CI（GitHub Actions）
   ├── musl のツールチェーンを導入（musl-1.2.4、静的 libc）
   ├── rustup で Rust stable を導入
   ├── x86_64-unknown-linux-musl のターゲットを追加
   ├── cargo build --release --target x86_64-unknown-linux-musl
   ├── RPM のソースを準備（バイナリー + systemd ユニット + logrotate の設定）
   ├── rpmbuild → xoa-proxy-<VERSION>.rpm
   ├── RPM 署名用サブキーで rpmsign（GPG_PRIVATE_KEY + GPG_PASSPHRASE）
   └── 署名済み RPM を GitHub リリースの成果物として公開（公開鍵は
       keys.openpgp.org。インポート手順はリリースノートに記載）

3. xcp-ng-ce-iso の CI（GitHub Actions）
   ├── xolite-ce のリリースから署名済み RPM をダウンロード
   ├── xoa-proxy のリリースから署名済み RPM をダウンロード
   ├── GPG_PRIVATE_KEY（ISO 署名用サブキー）をランナーのキーリングにインポート
   ├── ランナーのキーリングから公開鍵をエクスポート → インストーラーの chroot に注入
   ├── createrepo_c で community-repo/x86_64/ を用意
   ├── create-installimg.sh を実行（root）— install.img（SquashFS）を作成
   ├── create-iso.sh を実行（非 root）— ISO を組み立て
   ├── isohybrid --uefi（MBR/GPT ハイブリッドの刻印）
   ├── implantisomd5
   ├── sha256sum → xcp-ng-8.3-ceN.iso.sha256
   ├── gpg --detach-sign（GPG_PRIVATE_KEY による ISO 署名用サブキー）
   └── xcp-ng-8.3-ceN.iso + .iso.sha256 + .iso.sha256.asc を
       Vagrantin/xcp-ng-ce-iso の GitHub リリースとして公開（公開鍵は
       keys.openpgp.org。検証手順はリリースノートに記載）

4. xoa-hl の CI（GitHub Actions）
   ├── XO_COMMIT で固定したコミットで vatesfr/xen-orchestra を浅く取得
   │   （現在は 5.113.2。XO 5.x の最後のリリースで、意図的に更新）
   ├── patches/*.patch を適用（menu-hide-items）
   ├── xoahl.config.toml を書き出し、自己署名の TLS 証明書を生成
   ├── yarn && yarn build（すべての workspace）、不要物の削除、devDependencies の除去
   ├── tar → xoa-hl-<VERSION>.tar.gz
   ├── rpmbuild → xoa-hl-<VERSION>.noarch.rpm（軽量：%post でアーカイブを取得）
   └── アーカイブと RPM を v<VERSION> の GitHub リリースとして公開

5. build-xoa-hl（Packer、実機の XCP-ng ホスト上）
   ├── AlmaLinux の ISO のチェックサムと、xoa-hl の最新リリースの RPM の URL を解決
   ├── inst.ks（Kickstart）と almalinux-build.json（Packer のテンプレート）を生成
   ├── packer build — XCP-ng ホスト上で Kickstart により AlmaLinux 9 をインストール
   ├── プロビジョニング：xe-guest-utilities、Node 24、xoa-hl の RPM、初回起動用ユニット
   ├── イメージを軽量化し、/etc/machine-id を空にする
   └── XVA をエクスポート（xva_compressed）— XO Lite CE が展開するアプライアンス
```

---

## ビルドの統括
{: #build-orchestration }

[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
リポジトリが、上記のパイプラインを自動化します。その Rust の workspace
`xcp-orchestrator`（`orchestrator`、`iso-agent`、`xoa-vm-agent`、`shared`
の各 crate）は専用の VM 上で systemd のサービスとして動き、毎日タイマーで
起動します。

```
systemd のタイマー（毎日 05:00）
   ├── workflow_dispatch で xolite-ce と xoa-proxy のワークフローを実行
   ├── ワークフローの実行が終わるまで状態を確認
   ├── 最新の GitHub リリースがすでに HEAD と一致するコンポーネントは飛ばす
   │   （リリースを基準にした変更の検出。毎回ビルドし直さない）
   ├── 失敗時：API でジョブのログを取得し、ローカルの LLM
   │   （Ollama、qwen3-coder:30b）で診断し、実行できる修正案を書き出す
   ├── 成功時：後続の xcp-ng-ce-iso と XOA の XVA イメージのビルドを実行
   └── 状況のダッシュボードを表示（コンポーネントごとの状態 + ログへのリンク）
```

---

## 設計上の重要な判断

### 3 つのリポジトリに分ける方針
RPM のビルドと ISO の組み立てを分けることで、責任範囲がはっきりします。
`xolite-ce`（画面のパッチとパッケージング）と `xoa-proxy`（Rust のプロキシと
パッケージング）は、ISO のツールチェーンに触れずにそれぞれ独立して手を
入れられますし、その逆も同じです。各リポジトリは、バージョン付きの署名済み
RPM を GitHub リリースの成果物として公開します。ISO はそれらの成果物を
取り込んでビルドします。

### ソースコードの段階でパッチを当てる
XO Lite のパッチは、`DeployXoaView.vue` の Vue / TypeScript の**ソース
コード**に対して当てます。

---

## GPG 署名
{: #gpg-signing }

XCP-hl は、**オフラインのマスターキーとサブキー**という形の鍵ペアを
1 組だけ使います。マスターキーはオフラインで保管し、署名には使いません。
そこから 2 つの署名用サブキーを作り、一方を両方の RPM に、もう一方を ISO に
使います。

### 鍵の詳細

| 項目 | 値 |
|---|---|
| 鍵の UID | `XCP-ng Community Edition (Master signing key)`（`gpg --list-keys` に表示される文字列） |
| マスターキーのフィンガープリント | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| 公開先 | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| メールアドレス | `xcp-ng-ce.lid530@passmail.com` |
| 公開鍵のファイル | `xcp-ng-ce-public.asc` |

### サブキーの役割

| サブキー | 用途 |
|---|---|
| RPM 署名用サブキー | `xo-lite-community-*.rpm` と `xoa-proxy-*.rpm` |
| ISO 署名用サブキー | `xcp-ng-8.3-ceN.iso.sha256.asc`（ISO のチェックサムファイルに対する分離署名） |

---

## コンポーネントごとの詳しいドキュメント

| ページ | 説明 |
|---|---|
| [xoa-proxy](xoa-proxy.html) | XVA 配信用の Rust 製 HTTP/gzip プロキシ |
| [xolite-ce](xolite-ce.html) | XO Lite のパッチ、RPM の spec、ビルドのパイプライン |
| [xcp-ng-ce-iso](xcp-ng-ce-iso.html) | ISO の組み立て、ツールチェーン、CI のワークフロー |
| [xoa-hl](xoa-hl.html) | 手を入れた Xen Orchestra（XOA-HL）— アーカイブと軽量 RPM のビルド |
| [build-xoa-hl](build-xoa-hl.html) | XCP-ng 上で XOA の XVA イメージを作る Packer のパイプライン |
| [buildorchestration（GitHub）](https://github.com/Vagrantin/buildorchestration) | Rust 製のビルドオーケストレーターと、LLM によるビルドの診断 |
