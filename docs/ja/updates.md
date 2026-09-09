---
layout: default
title: アップデート
parent: 日本語
nav_order: 4
lang: ja
---

# XCP-ng HomeLab Edition のアップデート
{: .no_toc }

XCP-HL のコンポーネントは、GitHub Pages にある yum リポジトリから署名済みの
RPM として配布されます。そのため、稼働中のホストをその場でアップデートでき
ます。新しい XO Lite や `xoa-proxy` を取り込むために ISO から入れ直す必要は
ありません。

1. TOC
{:toc}

---

## アップデートが表示される場所

利用できる XCP-HL のアップデートは、XCP-ng 標準のアップデートと同じ場所、
**Xen Orchestra** に表示されます。

```
Home > Hosts > <対象のホスト> > Patches
```

このタブには、利用できるパッケージごとに名前、説明、バージョン、リリース、
ダウンロードサイズが並び、赤いバッジに件数が出ます。行にある目のアイコン
**Show changelog** を選ぶと、その RPM の変更履歴が開きます。
`Home > Pools > <プール> > Patches` のプール単位の画面と、ダッシュボードの
概要にも同じ内容が表示されます。

XCP-ng には `updater.py` という XAPI プラグインが同梱されており、Xen
Orchestra はこれに問い合わせて利用できるアップデートを調べます。XOA-HL は、
この問い合わせに XCP-HL のリポジトリを含めるように変更してあります。

## アップデートを適用する

Patches タブの **Install all patches** は、一覧に出ているものをすべて適用
します。

{: .warning }
これは全部かゼロかの操作です。XCP-ng のアップデータープラグインは、
XCP-ng 標準のリポジトリと XCP-HL のリポジトリをまとめて 1 回の `yum update`
で処理します。そのため、このボタンを押すと未適用の XCP-ng 本体の
アップデートも一緒に適用されます。この画面から個別のパッケージを選ぶことは
できません。XCP-HL のパッケージだけを更新したい場合は、ホスト上で
`yum update xo-lite-ce xoa-proxy` を実行してください。

ホストのコマンドラインでの対応する操作は次のとおりです。

```bash
yum check-update            # 何が利用できるか
yum update xcp-hl-release   # リポジトリの設定そのもの
yum update xo-lite-ce       # XO Lite（HomeLab Edition）
yum update xoa-proxy        # XVA 展開用プロキシ
```

## リポジトリの設定

設定は `/etc/yum.repos.d/xcp-hl.repo` という 1 つのファイルにまとまって
おり、`xcp-hl-release` パッケージが所有しています。このファイルは 3 つの
リポジトリを定義します。

| リポジトリ ID | 内容 | 公開元 |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{: .important }
このファイルのセクション名は変更しないでください。リポジトリ ID は Xen
Orchestra から `updater.py` プラグインに渡され、プラグインは渡された
リポジトリのアップデートしか一覧に出しません。セクション名を変えても
エラーにはならず、そのパッケージが Patches タブから黙って消えるだけです。

`yum` はすでに持っている `.repo` ファイルを読み直さないため、リポジトリの
設定は「一度コピーするファイル」ではなくパッケージとして配布しています。
設定の変更は `yum update xcp-hl-release` を通じてホストに届きます。

このファイルには `%config(noreplace)` が付いています。手元で編集していた
場合は、その内容が残り、新しいファイルは `xcp-hl.repo.rpmnew` として横に
書き出されます。

## 既存のホストでの初回設定

`xcp-hl-release` パッケージより前の ISO からインストールしたホストでは、
一度だけ初期設定が必要です。そのあとは設定を yum が管理します。

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://vagrantin.github.io/xcp-hl/xcp-hl.repo

rpm --import https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

パッケージをインストールすると、いまダウンロードしたファイルはパッケージに
含まれるものに置き換わり、元のファイルは `xcp-hl.repo.rpmorig` として
残ります。両者の違いは署名鍵をどこから読むかだけです。ダウンロードした方は
HTTPS で取得し、パッケージに含まれる方はパッケージが入れるローカルの鍵を
使います。

新しい ISO には最初から `xcp-hl-release` が入っているため、この節は
当てはまりません。

## 前のバージョンに戻す

各リポジトリは直近のリリースだけを公開しているため、戻せる範囲はそれに
限られます。以前のビルドに戻すには次のようにします。

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<バージョン>
```

## 検証と信頼

パッケージとリポジトリのメタデータは、XCP-ng HomeLab Edition の GPG 鍵で
署名しています。クライアント側の設定は `repo_gpgcheck=1` と `gpgcheck=0`
です。

RPM は GPG の**署名用サブキー**で署名しています。XCP-ng 8.3 の dom0 では、
rpm 4.11 は鍵をインポートしたときに主鍵しか登録しません。そのため、サブキー
による署名はすべて `NOKEY` と報告され、パッケージを直接検証できません。
そこで信頼はリポジトリのメタデータを経由します。`repomd.xml` は署名され、
サブキーを扱える GPG 本体で検証されます。`repomd.xml` には `primary.xml` の
SHA-256 が記録され、`primary.xml` にはすべてのパッケージの SHA-256 が
記録されています。

{: .warning }
署名用サブキーは **2027 年 5 月 10 日**に期限切れになります。それ以降は、
サブキーの期限を延長し、公開されている鍵を更新し、各ホストで再インポート
するまで検証に失敗します。

## 既知の制限事項

XOA-HL 自体にはまだ yum リポジトリがないため、アプライアンスをその場で
アップデートできません。現在 XOA-HL を更新するには、新しいイメージを展開
します。この件は
[issue #14](https://github.com/Vagrantin/xcp-hl/issues/14) で追跡して
います。

{: .note }
このディストリビューションがアルファ版であることを忘れないでください。
アップデートの前にリリースノートを読んでください。リリースのたびに互換性の
ない変更が入る前提であり、アップデートにホスト側の手作業が必要になることも
あります。
