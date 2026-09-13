---
layout: default
title: 変更履歴
parent: 日本語
nav_order: 7
lang: ja
---

# 変更履歴
{: .no_toc }

XCP-hl のすべてのリポジトリにまたがる、プロジェクト全体の変更と、それが
解決した issue の一覧です。リリースごとのコンポーネントのバージョンは
[リリース一覧表](release-matrix.html)にあります。
{: .fs-6 .fw-300 }

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 2026 年 9 月

### 既定の ISO ストレージ。[#2](https://github.com/Vagrantin/xcp-hl/issues/2) と [#46](https://github.com/Vagrantin/xcp-hl/issues/46) を解決

新しく入れた XCP-ng ホストには、インストーラーの ISO を置く場所がありません。
ISO SR は存在せず、作るには自分でディレクトリーを用意して `xe sr-create` を
手で実行する必要があります。XCP-hl はインストール時に 20 GB の
パーティションを確保し、`xcphl-iso` というラベルで ext4 にフォーマットして
`/var/opt/xen/xcp-hl-iso` にマウントし、初回起動時に **XCP-HL ISO library**
という名前の ISO SR として登録するようになりました。Xen Orchestra から
すぐにアップロードできます。

これにより XCP-hl が必要とする最小のディスク容量は **100 GB** になりました。
内訳はシステム用パーティションが約 41.5 GB、ISO ライブラリーが 20 GB、
残りの約 38.5 GB が VM のストレージです。これに満たない場合は、VM の
ストレージを数 GB まで削るのではなく確保を行わず、ディスクの構成は XCP-ng
標準とまったく同じになります。

issue [#46](https://github.com/Vagrantin/xcp-hl/issues/46) では、XCP-ng の
アップロード用エンドポイントに ISO 専用の経路を追加できないかが問われました。
結果として、その必要はありませんでした。`PUT /import_raw_vdi` は汎用の
生 VDI インポートで、XO 5 はすでに *Import → Disk* からこれを使っています。
足りなかったのは、取り込み先となる ISO SR だけでした。新しい
エンドポイントは追加していません。

パーティションはインストーラーが作るため、対象は XCP-hl を新規インストール
した場合だけです。XCP-ng 標準からインストールしたあとに XCP-hl の
リポジトリを追加したホストのパーティションを切り直すことはありませんし、
アップグレードでも既存のパーティションを作り直さずそのまま使います。

これは、フォークした `host-installer` の RPM を配布するのではなく、ISO の
ビルド時に `install.img` の中の `host-installer` にパッチを当てることで
実現しています。
[xcp-ng-ce-iso](developers/xcp-ng-ce-iso.html#host-installer-patching) を
参照してください。

## 2026 年 8 月

### リリース一覧表に、実際に配布したパッケージを記載。[#15](https://github.com/Vagrantin/xcp-hl/issues/15) に向けた前進

[リリース一覧表](release-matrix.html)には、コンポーネントごとのリリース
タグしか載っていませんでした。`xoa-proxy` の場合、それだけではホストで動いて
いるものを特定できません。タグはバージョンに対応しますが、RPM のリリース欄
には CI の実行番号とビルド元のコミットが入りますし、いちばん古い 2 行には
バージョンをまったく示さない `v-proxy-automated-*` というビルド実行のタグが
付いています。

ISO ごとの各行に、`rpm -q` が出力するとおりのパッケージ名
（`xoa-proxy-0.1.1.8-55.gc525575.static.x86_64`）を、リリースページへリンク
したバージョンの下に表示するようにしました。ISO、`xolite-ce`、`xoa-proxy` の
いずれについても同じです。既存の行は公開済みのリリース成果物から埋め直し、
`v8.3-ce3` と `v8.3-ce4` の xo-lite のアップストリームのバージョンは、
これらのビルドが実際に含む RPM に合わせて 0.22.0 から 0.21.0 に修正しました。
オーケストレーターは、ビルドのたびにこの新しい項目を記録します
（`xcp-orchestrator` の `shared/src/github.rs`）。

---

## 2026 年 7 月

### XOA の VM イメージのリリースを build-xoa-hl へ移動。[#22](https://github.com/Vagrantin/xcp-hl/issues/22) を修正

XOA-HL の VM（`xoa-image-<日付>-<sha7>`、成果物は `xoa-almalinux.xva`）は、
*ソフトウェア*をビルドするリポジトリである
[`xoa-hl`](https://github.com/Vagrantin/xoa-hl) で、その RPM のリリースと
混ざった状態で公開されていました。これを、実際にイメージをビルドする
リポジトリ [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) で
公開するようにしました。オーケストレーターの `xoa-vm-agent` がそちらで
リリースを作り、XO Lite の展開ボタンはそのリポジトリから最新のイメージを
解決します。

混在には実害がありました。`xoa-hl` の `releases/latest` が RPM の成果物を
持たないイメージのリリースを指してしまい、
`build-xoa-hl/scripts/setup-xoa-builder.sh` での RPM の探索が壊れていました。
現在は、実際に RPM を含む最新のリリースを探すように直してあります。

移動より前に公開したイメージのリリースは `xoa-hl` に残してあります。すでに
配布済みの ISO がそれらを解決し続けられるようにするためです。
[リリース一覧表](release-matrix.html#xoa-hl-releases)では、各項目を
それを置いているリポジトリにリンクしています。

### リリース一覧表に XOA のバージョンを記録。[#13](https://github.com/Vagrantin/xcp-hl/issues/13) を修正

[リリース一覧表](release-matrix.html)に、**XOA アプライアンスのリリース**
専用の表を追加しました。公開された各 VM イメージ（`Vagrantin/xoa-hl` の
`xoa-image-*` リリース）、それに含まれる `xoa-hl` のソフトウェアのバージョン、
そして分岐元となったアップストリームの Xen Orchestra のバージョンを記録
します。ISO ごとの表からは、一度も値が入らなかった `xoa-hl` の列を削除
しました。アプライアンスは展開時に解決され、ISO とは別にバージョン管理される
ためです。

### XOA-HL 版が完成。[#1](https://github.com/Vagrantin/xcp-hl/issues/1) と [#6](https://github.com/Vagrantin/xcp-hl/issues/6) を修正

Xen Orchestra HomeLab Edition は、ソースからのビルド、パッケージ化、展開まで
一通りできるようになりました。

- [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) は、固定した
  アップストリームのコミットから XO 5.113.2（XO 5.x の最後のリリース）を
  ビルドし、画面に手を入れます。ライセンスが必要なメニュー項目（Hub、XOA、
  Proxies、XOSTOR）とサポートなしのバナーを隠します
  （`patches/menu-hide-items.patch`）。
- [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) が、XCP-ng 上の
  Packer を使ってそれを自動設定型の XVA アプライアンスにまとめます。
- XO Lite の展開画面に、展開先のイメージとして **XOA HomeLab (latest
  build)** が加わりました。展開の時点で、エージェントがビルドした最新の XVA
  を GitHub のリリースから解決します（`xolite-ce` のコミット `6abd43f`、
  2026 年 7 月 14 日）。

### リリースの公開を自動化。[#4](https://github.com/Vagrantin/xcp-hl/issues/4) を修正

バージョン付けとリリースノートは、どのパイプラインでも自動で作られるように
なりました。

- `xolite-ce` と `xoa-proxy` は、CI の中でリリースのタグと RPM の
  バージョンを決めます（`xolite-ce` の `7b2e4d4`、`xoa-proxy` の
  `9582718`）。`xoa-proxy` のリリースは GitHub が生成するリリースノートを
  使い、`xolite-ce` と ISO は、ソースのバージョンと検証手順を含む構造化した
  リリース本文を出します。
- ISO のビルドはオーケストレーターが実行し、コンポーネントの正確なリリース
  タグをワークフローの入力として固定します。これにより、古い RPM が
  取り込まれてしまう競合状態がなくなりました（`xcp-ng-ce-iso` の
  `68f211d`）。
- すべての ISO のリリースを[リリース一覧表](release-matrix.html)に記録して
  います。

---

## 2026 年 6 月

### ドキュメントサイトの CI/CD。[#5](https://github.com/Vagrantin/xcp-hl/issues/5) を修正

プロジェクトのサイト（このサイト）は Jekyll で作り、
[`xcp-hl`](https://github.com/Vagrantin/xcp-hl) の `main` に push する
たびに GitHub Pages へ自動でデプロイされます
（`.github/workflows/pages.yml`）。これにより、データから生成される
リリース一覧表を含め、プロジェクトの状況について唯一の正しい情報源に
なっています。

---

## 2026 年 5 月

### GPG 鍵の構成を実装。[#3](https://github.com/Vagrantin/xcp-hl/issues/3) を修正

**オフラインのマスターキーと 2 つの署名用サブキー**という構成で、すべての
ビルドのパイプラインの GPG 署名を統一しました。一方のサブキーが RPM
（`xo-lite-ce`、`xoa-proxy`）に署名し、もう一方が ISO のチェックサム
ファイルに署名します。公開鍵は
[keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com)
で公開し、検証手順は各リリースの本文に含めています。詳しくは
[GPG 署名](developers/#gpg-signing)を参照してください。さらに細かくする案
（モジュールごとに 1 つの鍵）は
[ロードマップ](roadmap.html#gpg-keys--one-signing-key-per-module)に残って
います。
