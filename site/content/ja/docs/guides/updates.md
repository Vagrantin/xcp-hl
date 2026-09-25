---
title: アップデート
weight: 3
translationKey: updates
aliases: ["/ja/updates.html"]
---

XCP-hl のコンポーネントは、GitHub Pages にある yum リポジトリから署名済みの
RPM として配布されます。そのため、稼働中のホストをその場でアップデートでき
ます。新しい XO Lite や `xoa-proxy` を取り込むために ISO から入れ直す必要は
ありません。

**要点だけ言うと:** XCP-hl のアップデート方法は XCP-ng と同じです — Xen
Orchestra の Patches タブから、またはホスト上の `yum`/`dnf` から行います。
XCP-hl のパッケージは、XCP-ng 標準のリポジトリに追加された、いくつかの
リポジトリに置かれているだけだからです。このページの残りの部分では、
アップデートが具体的にどこに表示されるか、XCP-hl 独自の部分だけを更新する
方法、署名の仕組み、そして前のバージョンに戻す方法を詳しく説明します。

## アップデートが表示される場所

利用できる XCP-hl のアップデートは、XCP-ng 標準のアップデートと同じ場所、
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
この問い合わせに XCP-hl のリポジトリを含めるように変更してあります。

## アップデートを適用する

Patches タブの **Install all patches** は、一覧に出ているものをすべて適用
します。

{{< callout type="warning" >}}
これは全部かゼロかの操作です。XCP-ng のアップデータープラグインは、
XCP-ng 標準のリポジトリと XCP-hl のリポジトリをまとめて 1 回の `yum update`
で処理します。そのため、このボタンを押すと未適用の XCP-ng 本体の
アップデートも一緒に適用されます。この画面から個別のパッケージを選ぶことは
できません。XCP-hl のパッケージだけを更新したい場合は、ホスト上で
`yum update xo-lite-ce xoa-proxy` を実行してください。
{{< /callout >}}

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

{{< callout type="error" >}}
このファイルのセクション名は変更しないでください。リポジトリ ID は Xen
Orchestra から `updater.py` プラグインに渡され、プラグインは渡された
リポジトリのアップデートしか一覧に出しません。セクション名を変えても
エラーにはならず、そのパッケージが Patches タブから黙って消えるだけです。
{{< /callout >}}

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

パッケージとリポジトリのメタデータは、XCP-hl の GPG 鍵で署名しています。
クライアント側の設定は `repo_gpgcheck=1` と `gpgcheck=0` です。

RPM は主鍵ではなく GPG の**サブキー**で署名しています。ここには XCP-ng 8.3
のホスト側にある `rpm` ツール（バージョン 4.11）の既知の制限があります。
鍵をインポートしたときに主鍵しか登録しないため、サブキーによる署名は
`NOKEY` と報告され、署名自体は正しくてもパッケージを直接検証できません。

そこで信頼はリポジトリのメタデータを経由します。サブキーを理解できる本来の
GPG ツールが `repomd.xml` を検証します。このファイルには `primary.xml` の
SHA-256 が記録され、`primary.xml` にはすべてのパッケージの SHA-256 が
記録されています。つまり `repomd.xml` という 1 つのファイルを検証すれば、
リポジトリ内のすべての RPM を間接的に検証したことになります。

{{< callout type="warning" >}}
署名用サブキーは **2027 年 5 月 10 日**に期限切れになります。それ以降は、
サブキーの期限を延長し、公開されている鍵を更新し、各ホストで再インポート
するまで検証に失敗します。
{{< /callout >}}

## XOA-HL アプライアンスのアップデート

XOA-HL アプライアンスは、自身の yum リポジトリからアップデートします。

```bash
dnf update xoa-hl        # アプライアンスのアプリケーションのみ
dnf update               # アプリケーションと AlmaLinux のベースをまとめて
```

設定は `/etc/yum.repos.d/xoa-hl.repo` にあります。このファイルは `xoa-hl`
パッケージ自身が提供し、リポジトリを 1 つだけ定義します。

| リポジトリ ID | 内容 | 公開元 |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

アップデートは 2 つの systemd ユニットが担います。

| ユニット | 役割 |
|---|---|
| `xoa-hl-check-update.service` | `dnf check-update` を実行し、結果を `/run/xoa-hl/status` に書き込みます |
| `xoa-hl-update.service` | `dnf -y update` をすべて実行します |

{{< callout type="warning" >}}
`xoa-hl-update.service` は `xoa-hl` だけでなく、アップデートが保留されている
**すべての**パッケージを更新します。
{{< /callout >}}

{{< callout type="info" >}}
どちらのユニットにもタイマーは設定されていないため、XOA-HL のアップデートを
自動で確認する仕組みはまだありません。自動アップデート機能は
[issue #45](https://github.com/Vagrantin/xcp-hl/issues/45) で追跡しています。
{{< /callout >}}

## 既知の制限事項

現時点で既知の制限事項はありません。

{{< callout type="info" >}}
このディストリビューションがアルファ版であることを忘れないでください。
アップデートの前にリリースノートを読んでください。リリースのたびに互換性の
ない変更が入る前提であり、アップデートにホスト側の手作業が必要になることも
あります。
{{< /callout >}}
