---
layout: default
title: ロードマップ
parent: 日本語
nav_order: 3
lang: ja
---

# ロードマップ
{: .no_toc }

XCP-ng Home lab Edition の改善予定と今後の方向性です。
{: .fs-6 .fw-300 }

{: .note }
このロードマップは現時点の方針を表したものです。コミュニティからの意見や
アップストリームの変更によって優先順位は変わります。項目の提案や後押しは
[GitHub](https://github.com/Vagrantin/xcp-hl/issues) で issue を作って
ください。

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 短期 — 次のリリース

現在作業中、あるいは内容が固まっていて近いうちに実装できるものです。

### GPG 鍵 — モジュールごとに 1 つの署名鍵
{: .d-inline-flex #gpg-keys--one-signing-key-per-module }

セキュリティ
{: .label .label-red }

[xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) で決めた統一的な
GPG の構成は実装済みです。オフラインのマスターキーと 2 つの署名用サブキー
（RPM 用と ISO 用）を用意し、公開鍵を keys.openpgp.org で公開しています。
[GPG 署名](developers/#gpg-signing)を参照してください。残っている改善点は、
共通になっている RPM 用サブキーを分けて、モジュールごとに専用の鍵を持たせる
ことです（`xo-lite-ce` の RPM 用、`xoa-proxy` の RPM 用、ISO 用）。

**追跡：** これから issue を作成します（xcp-hl#3 は完了）

---

### XO Lite — 展開に成功したあとの「Deploy XOA」ボタンの状態
{: .d-inline-flex }

不具合
{: .label .label-red }

XOA の展開に成功しても、「Deploy XOA」ボタンが「Access XOA」に切り替わり
ません。展開用の composable でリアクティブな状態の更新を直し、展開が
終わったことを画面に正しく反映させる必要があります。アップストリームでは
すでに動いており、こちらの変更で壊れたものです。

**追跡：** [xolite-ce#4](https://github.com/Vagrantin/xolite-ce/issues/4)

---

## 中期

予定はしているものの、設計やアップストリームとの調整がもう少し必要な項目
です。

### アップストリームのバージョンの自動追跡
{: .d-inline-flex }

CI/CD
{: .label .label-green }

Rust 製のデーモン
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
は、すでに毎日のタイマーですべてのコンポーネントのビルドを実行・監視し、
最新の GitHub リリースがすでに最新のコンポーネントは飛ばし、失敗した CI の
ログをローカルの LLM（Ollama）で診断します。残っているのは、XCP-ng 8.x の
新しいポイントリリースや XO Lite のバージョン更新を検出し、固定している
バージョン（たとえば `xolite-ce` の `UPSTREAM_TAG`）を更新するプルリクエストを
自動で作ることです。

---

### xoa-proxy — メモリー使用量の削減
{: .d-inline-flex }

改善
{: .label .label-blue }

現在 XVA イメージを XAPI へ流し込んでいる Rust 製サービス `xoa-proxy` の、
実行時のメモリー使用量を計測して減らします。目標は、転送の速度を落とさずに
待機時の使用量を小さくすることです。

**追跡：** [xoa-proxy#1](https://github.com/Vagrantin/xoa-proxy/issues/1)

---

### xoa-proxy — 依存（crate）の削減
{: .d-inline-flex }

改善
{: .label .label-blue }

Cargo の依存関係を見直し、同じことをより少ない、あるいはより軽い依存で
実現できる crate は置き換えるか削除します。これによりコンパイル時間が
短くなり、攻撃面も小さくなります。

**追跡：** [xoa-proxy#2](https://github.com/Vagrantin/xoa-proxy/issues/2)

---

### xoa-proxy — logrotate のタイムゾーン（UTC とのずれ）
{: .d-inline-flex }

不具合
{: .label .label-yellow }

`xoa-proxy` の `logrotate` の設定は、ホストのローカルのタイムゾーンに
かかわらず UTC の時刻を使います。ログのローテーションの時刻をホストの
タイムゾーンに合わせ、ログファイルの日付がシステムの日時と一致するように
します。

**追跡：** [xoa-proxy#3](https://github.com/Vagrantin/xoa-proxy/issues/3)

---

### xolite-ce の RPM — LICENSE ファイル
{: .d-inline-flex }

改善
{: .label .label-blue }

`xo-lite-ce` の RPM パッケージにきちんとした `LICENSE` ファイルを含め、
インストール済みパッケージのメタデータからライセンス条件を確認できるように
します。RPM パッケージングの推奨に沿った形にもなります。

**追跡：** [xolite-ce#1](https://github.com/Vagrantin/xolite-ce/issues/1)

---

## 長期 / アイデア

検討はしていますが、実施を決めてはいない項目です。

### 標準でのコンテナ対応
{: .d-inline-flex }

検討中
{: .label .label-purple }

XO Lite または XOA から直接コンテナを展開・管理できるようにするもので、
コミュニティから長く要望のある機能です。これには大きな調査が必要です。
Dom0 で動くコンテナは制御しきれない動作をするおそれがあり、XCP-ng の
ツールスタックにその存在を認識させる必要があります。XOA からの管理は
さらに複雑になります。実装の約束はしていません。

**追跡：** [xcp-hl#7](https://github.com/Vagrantin/xcp-hl/issues/7)

---

### answerfile.xml による自動インストールへの対応
完全に無人での HL の展開（PXE ブートやスクリプトによる構築）に使える
`answerfile.xml` の例を用意します。これには応答ファイルを `install.img`
（SquashFS）の中に入れる必要がありますが、現在のビルドのパイプラインは
すでにそれに対応しています。

---

## 完了した項目

| 項目 | 公開時期 |
|---|---|
| 既定の ISO ストレージ：インストール時に 20 GB のパーティションを確保し、初回起動時に ISO SR として登録（[#2](https://github.com/Vagrantin/xcp-hl/issues/2)、[#46](https://github.com/Vagrantin/xcp-hl/issues/46)） | 2026 年 9 月 |
| XOA-HL 版：ライセンスが必要なメニューとサポートなしのバナーを削除し、ソースからイメージをビルドして XO Lite の展開先として選べるように（[#1](https://github.com/Vagrantin/xcp-hl/issues/1)、[#6](https://github.com/Vagrantin/xcp-hl/issues/6)） | 2026 年 7 月 |
| RPM と ISO のリリースのバージョン付けとリリースノートを自動化（[#4](https://github.com/Vagrantin/xcp-hl/issues/4)） | 2026 年 7 月 |
| GitHub Pages の CI により、push のたびにドキュメントサイトを自動公開（[#5](https://github.com/Vagrantin/xcp-hl/issues/5)） | 2026 年 6 月 |
| GPG 署名の構成：オフラインのマスターキーと RPM/ISO 用サブキー、公開鍵を keys.openpgp.org に登録（[#3](https://github.com/Vagrantin/xcp-hl/issues/3)） | 2026 年 5 月 |
| 手を入れた XOA-HL アプライアンスの最初のビルド（`xoa-hl` + `build-xoa-hl`） | 2026 年 7 月 |
| 毎日のビルドを統括するデーモン（`buildorchestration`） | 2026 年 7 月 |
| アップストリームの xo-lite のバージョン固定（`UPSTREAM_TAG`） | 2026 年 7 月 |
| XO Lite への最初のパッチ（コミュニティ版の展開先） | v8.3-ce 2026 年 4 月 |
| Rust 製のストリーミングサーバー `xoa-proxy` | v8.3-ce 2026 年 4 月 |
| 2 つのリポジトリによる GPG 署名付き RPM + ISO のビルドのパイプライン | v8.3-ce 2026 年 4 月 |
| GitHub Actions の CI/CD | v8.3-ce 2026 年 4 月 |
| XO Lite の展開画面で資格情報欄を読み取り専用に | v8.3-ce 2026 年 4 月 |
