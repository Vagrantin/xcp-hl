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

`xolite-ce@d452937` では、`UPSTREAM_TAG` が `xo-lite-v0.21.0` を
`13f987ff3d34504a90b89178489e15fa2293d1b3` に固定しています。このベースラインは
`xoa-deploy.vue` に対して Rust 製の実行ファイルを同梱して使う方式で、
`XoaButton.vue` にはユニファイド diff を、ロケール、ローダー、ホストと
ゲストのバージョン情報、デプロイ用シークレットには明示的な変換を用いています。
根拠: `xolite-ce/.github/workflows/build-xolite-ce.yml@d452937` と
`xolite-ce/UPSTREAM_TAG@d452937`。

[移行の PR](https://github.com/Vagrantin/xolite-ce/pull/26) は、この同梱の実行
ファイルを、レビュー可能なユニファイド diff に置き換えます。`patches/series` が
diff の順序を定義し、`patches/metadata.toml` が目的、担当者、アップストリーム、
依存関係を記録します。ビルドと検証はともに `scripts/patch-source.sh` を共有
します。diff 以外のアセットとロケールの変換は明示的なままです。アップストリーム
の固定と最終的なソースのバイト列は保たれます。

複数コンポーネントにまたがるパッチモデルの[評価](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md)
には意思決定の記録が、そこからリンクされた移行の PR には実装状況が載っています。
コンポーネントの[メンテナンスガイド](https://github.com/Vagrantin/xolite-ce/blob/7925dbc6bde35bfb387677b2c9c227ef05a886c0/docs/patching.md)
は移行ブランチを説明しています。実装の根拠:
`xolite-ce/scripts/patch-source.sh@7925dbc`,
`xolite-ce/scripts/list-patches.py@7925dbc`, and
`xolite-ce/ci/test-patch-migration.py@7925dbc`.

---

## ソースの検証

クリーンで固定されたアップストリームのチェックアウトを用意し、移行後の
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

`docs/patch-migration.json` は、古い実行ファイルのハッシュと、コンシューマー、
アップストリーム、パッチツールのソースの不変なリビジョンを記録します。
移行のチェックは、新旧のパイプライン間で、ソースの全バイト、Git の実行
ビット、シンボリックリンクのリンク先を比較します。CI はさらに、固定された
Rust のソースを再ビルドし、その出力を記録済みの実行ファイルと突き合わせます。
これは 1 つの固定入力に対する振る舞いの系譜であって、歴史的なバイナリの
再現性ではありません。

---

## ビルドと受け入れ

アプリケーションと RPM のビルドはすべて GitHub Actions で実行します。
移行に伴い、リリースを公開せずに、完全なパイプラインとパッチ済み Vue 配布
物に対する PR check が追加されました。パッケージングと署名は既存の
コンポーネントのワークフローと `SPECS/xo-lite-community.spec` に残ります。

ソースの適用、ホストされるアプリケーションのビルド、RPM のチェック、
インストール後の受け入れは、それぞれ別個の結果として扱ってください。
この移行の期間中は稼働中のアプライアンスを利用できず、インストール後の
デプロイの挙動は未検証のままです。

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
