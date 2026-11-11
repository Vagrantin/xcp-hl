---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/ja/developers/xolite-ce.html"]
---

XO Lite 向けのコミュニティパッチと、RPM のビルドのパイプラインです。
{class="lead"}

**リポジトリ：** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· 言語：TypeScript / Vue 3（パッチ）· RPM の spec · ライセンス：AGPL-3.0

## XO Lite とは

XO Lite は、すべての XCP-ng ホストに同梱される軽量な単一ページの管理
アプリケーションです。ホストから直接配信され、ブラウザーの中だけで動きます。
実装は Vue 3 / TypeScript / Vite の SPA です。

標準の XCP-ng ホストでは、XO Lite に **「Deploy XOA」** の画面
（`xoa-deploy.vue`）があり、公式の Xen Orchestra のイメージを
ダウンロードして取り込みます。XCP-hl はこの動作を置き換え、展開したい
XOA イメージを選べるようにします。

---

## ソースへのパッチ適用

`UPSTREAM_TAG` は `xo-lite-v0.21.0` を
`13f987ff3d34504a90b89178489e15fa2293d1b3` に固定しています。XO Lite CE は、
このソースをレビュー可能なユニファイド diff で変更します。`patches/series` が
diff の順序を定義し、`patches/metadata.toml` が各パッチの目的、対象、担当者、
アップストリームのコミット、依存関係を記録します。シリーズには
`XoaButton.vue` 向けの `xoa-button-empty.patch` と、`xoa-deploy.vue` 向けの
`010-xoa-deploy.patch` が含まれます。ビルドと検証はともに
`scripts/patch-source.sh` を使い、このスクリプトは diff ではないロケール、
ローダー、ホストとゲストのバージョン情報、デプロイ用シークレットの明示的な
変換も実行します。根拠: `xolite-ce/patches/series@ad43fa2`、
`xolite-ce/patches/metadata.toml@ad43fa2`、
`xolite-ce/scripts/patch-source.sh@ad43fa2`。

2026 年 10 月 31 日に `4506112` としてマージされた
[PR #26](https://github.com/Vagrantin/xolite-ce/pull/26) より前は、同梱の
Rust 製実行ファイルが `xoa-deploy.vue` を書き換えていました。diff はこれを
置き換え、アップストリームの固定と最終的なソースのバイト列は変わっていません。

複数コンポーネントにまたがるパッチモデルの[評価](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md)
には意思決定の記録が載っています。コンポーネントの
[メンテナンスガイド](https://github.com/Vagrantin/xolite-ce/blob/ad43fa282dca7023776a142cb4250e96226d8312/docs/patching.md)
は、命名、順序、メタデータの規則を定めています。

---

## ソースの検証

クリーンで固定されたアップストリームのチェックアウトを用意し、
XO Lite CE のツリーで次を実行します。

```sh
python3 scripts/list-patches.py patches
python3 ci/test-patch-series.py
bash scripts/patch-source.sh /path/to/clean/pinned/upstream
```

シリーズ全体は、どの diff を適用するより前にも検証されます。名前の不正、
項目の欠落や重複、メタデータの不一致、依存順序の不正はいずれも検証を
失敗させます。失敗したパッチを飛ばしたり、リモートのローダーに置き換え
たりしないでください。既存のソーステストは、影響を受ける UI、ロケール、
デプロイの後始末を個別に確認します。

`docs/patch-migration.json` は、廃止した実行ファイルのハッシュと、
コンシューマー、アップストリーム、パッチツールのソースの不変なリビジョンを
記録します。`ci/test-patch-migration.py` は、旧パイプラインと現行の
パイプラインの間で、ソースの全バイト、Git の実行ビット、シンボリックリンクの
リンク先を比較します。CI はさらに、固定された Rust のソースを再ビルドし、
その出力を記録済みの実行ファイルと突き合わせます。これは 1 つの固定入力に
対する振る舞いの系譜であって、歴史的なバイナリの再現性ではありません。

---

## ビルドと受け入れ

アプリケーションと RPM のビルドはすべて GitHub Actions で実行します。
PR ごとに `check-patch-series.yml` が、リリースを公開せずに完全な
パイプラインを実行し、パッチ済みの Vue 配布物をビルドします。パッケージングと
署名は `build-xolite-ce.yml` と `SPECS/xo-lite-community.spec` に残ります。

ソースの適用、ホストされるアプリケーションのビルド、RPM のチェック、
インストール後の受け入れは、それぞれ別個の結果として扱ってください。
ビルド `0.21.0-39.g54c289b` はユニファイド diff のシリーズを含みます。
`xcp-hl/qa/ce52-acceptance/2026-11-09.md@7a51eb1` は、インストール済みの
ce36 ホスト 1 台でのこのビルドを記録しており、アプライアンスは同梱の
`#/xoa-deploy` の Custom URL フローで展開されています。ほかのイメージの
取得元、ほかのホスト、インストール環境での移行前後の比較は未検証のままです。

---

## GPG 署名

`xo-lite-ce` の RPM は、XCP-hl の鍵ペアの
**RPM 署名用サブキー**で署名しています。同じサブキーは `xoa-proxy` と
`xcp-hl-release` の RPM の署名にも使っており、コミュニティのすべての RPM
で 1 つのサブキーを共有しています。

プロジェクトの共通の[公開鍵](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc)は
本番サイトのルートで配布しています。インポート前にマスター鍵のフィンガープリントを
確認してください。以下のコマンドには署名サブキーに対応した RPM が必要です。
XCP-ng 8.3 の Dom0 は古い RPM 4.11 を使用するため、ホストでは
`repo_gpgcheck=1` で署名付きリポジトリメタデータを検証します。
[アップデート](/docs/guides/updates)に記載のリポジトリ設定を維持してください。

ローカルで RPM を検証するには次のようにします。

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## 開発に参加する

問題の報告や変更の提案は、[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues)で
issue を作ってください。
