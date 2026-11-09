---
layout: default
title: アップデート
parent: 日本語
nav_order: 4
lang: ja
---

# XCP-hl のアップデート
{: .no_toc }

XCP-hl のコンポーネントは、`rpm.xcp-hl.org` の yum リポジトリから署名済みの
RPM として配布されます。そのため、稼働中のホストをその場でアップデートでき
ます。新しい XO Lite や `xoa-proxy` を取り込むために ISO から入れ直す必要は
ありません。

リポジトリは `vagrantin.github.io` からこのアドレスへ移転しました（issue #190）。
ホストやアプライアンスは、新しいアドレスを含む `xcp-hl-release` または `xoa-hl`
の次回アップデートで自動的に移行します。移行期間中は旧アドレスも引き続き利用できます。

1. TOC
{:toc}

---

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

{: .warning }
これは全部かゼロかの操作です。XCP-ng のアップデータープラグインは、
XCP-ng 標準のリポジトリと XCP-hl のリポジトリをまとめて 1 回の `yum update`
で処理します。そのため、このボタンを押すと未適用の XCP-ng 本体の
アップデートも一緒に適用されます。この画面から個別のパッケージを選ぶことは
できません。XCP-hl のパッケージだけを更新したい場合は、ホスト上で
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
  https://rpm.xcp-hl.org/xcp-hl.repo

rpm --import https://rpm.xcp-hl.org/xcp-ng-ce-public.asc

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

## XOA-HL アプライアンスのアップデート

XOA-HL アプライアンスは、自身の yum リポジトリからアップデートします。

```bash
dnf update xoa-hl        # アプライアンスのアプリケーションのみ
dnf update               # アプリケーションと AlmaLinux のベースを合わせて
```

設定は `/etc/yum.repos.d/xoa-hl.repo` にあります。このファイルは `xoa-hl`
パッケージ自体が管理し、次の 1 つのリポジトリを定義します。

| リポジトリ ID | 内容 | 公開元 |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

アップデートは XOA-HL の Web UI の **Settings → XOA-HL Updates** からも実行
できます。このページは、実行中のトランザクションログをストリーミング表示します。

アップデートは systemd ユニットが制御します。

| ユニット | 役割 |
|---|---|
| `xoa-hl-check-update.service` | `dnf check-update` を実行し、結果を `/run/xoa-hl/status` に書き込む |
| `xoa-hl-update.service` | `nodejs` を除いて完全な `dnf -y update` を実行し、出力を `/var/lib/xoa-hl/update.log` にストリーミングする |
| `xoa-hl-check-update.timer` | `check` モードで、スケジュールに従って確認を実行する |
| `xoa-hl-auto-update.service` / `.timer` | `install` モードで、メンテナンスウィンドウ中に確認し、続けてインストールする |

{: .warning }
`xoa-hl-update.service` は、`xoa-hl` だけでなく、アップデートが保留中の
**すべての**パッケージを更新します。例外は Node.js で、`xoa-hl` パッケージが
要求するメジャーバージョンのままになります。

### アップデートモード

`v5.113.2_e281c536-ce18` より後のリリースでは、スケジュールによる確認と自動
インストールが加わります。どちらも**デフォルトでは無効**です。パッケージを
インストールまたはアップグレードしても、どちらのタイマーも有効になりません。
モードは **Settings → XOA-HL Updates** で選ぶか、root で次のように設定します。

```bash
# MODE FREQUENCY DAY TIME RANDOM_DELAY_MINUTES
/usr/libexec/xoa-hl/configure-updates.sh check weekly Sun 03:00 15
```

| モード | 自動で実行される内容 |
|---|---|
| `manual`（デフォルト） | 何も実行されません。確認とアップデートは、管理者が実行したときだけ始まります |
| `check` | アップデートの確認を、スケジュールに従って、また起動直後に実行します。インストールは手動のままです |
| `install` | メンテナンスウィンドウ中に、確認と続くアップデートを実行します。逃したウィンドウは起動後に再実行されません |

`install` モードでも、アプライアンスが自動で再起動することはありません。
スケジュールのオプションと結果の確認方法については、
[アプライアンスの自動アップデート](https://github.com/Vagrantin/xoa-hl/blob/main/docs/automatic-updates.md)
を参照してください。

### アップデートページの接続が切れる

新しい `xoa-hl` をインストールすると、Web UI も提供している `xo-server` が
再起動されるため、アップデートページはしばらく接続を失います。アップデート
自体は `xoa-hl-update.service` で実行されており、そのまま続行されます。

`v5.113.2_e281c536-ce18` より後のリリースでは、これに対処しています。

- `xo-server` が停止している間、ページは再接続を試み続けます。再接続後は、
  止まったところからログを再開し、結果を表示します。
- `xo-server` の再起動は、トランザクション全体が完了した後に 1 回だけ行われ
  ます。
- 1 分間接続できない場合、ページは `xo-server` に到達できない時間を表示し、
  **Reload page** ボタンを表示します。このボタンは、`xo-server` が再び応答
  するようになって初めてページを再読み込みします。
- ページを再読み込みすると、そのタブで開始したアップデートとその結果が
  復元されます。

### 中断されたアップデートの後

`v5.113.2_e281c536-ce52` でのみテストしています。他のリリースでは動作が異なる
可能性があります。

ある ce52 のテストでは、`xoa-hl-update.service` が `kernel-modules` を
インストールしている最中に強制停止すると、カーネルのファイルが破損しました。
次の管理対象アップデートは、事前の整合性チェックで停止し、失敗を報告しました。
他の中断では、結果が異なる可能性があります。`/var/lib/xoa-hl/update.log`
の末尾は次のようになります。

```text
Package integrity preflight failed; repair the interrupted transaction before retrying.
=== xoa-hl update failed with exit code 1 at ... ===
```

このテストでは、アプライアンスは以前のカーネルで起動しました。破損した
ファイルは、このメッセージの上にログとして列挙されていました。中断された
アプライアンスが起動するとは限りません。

{: .warning }
以下のコマンドは root で、アップデートが実行中でないときにだけ実行して
ください。アプライアンスが起動しているカーネルは削除しないでください。

**確認。** アップデートが実行中でないことを確かめてから、パッケージ
データベースとカーネルパッケージを確認します。

```bash
systemctl is-active xoa-hl-update.service    # expect inactive or failed
dnf check
rpm -V $(rpm -qa kernel-core kernel-modules kernel-modules-core)
ls /boot/vmlinuz-*
```

カーネルのファイルが破損していても、`dnf check` は問題を報告しないことが
あります。そのため、両方のチェックを実行してください。
`S.5......  /lib/modules/<バージョン>/vmlinuz` のような行は、そのバージョンの
カーネルのファイルが破損していることを意味し、`/boot/vmlinuz-<バージョン>`
がなければそれが裏付けられます。`/usr/share/licenses` や `/usr/share/doc`
の下のファイルが欠けているという行は正常です。このイメージはドキュメント
なしでインストールされており、アップデーターはそれらを無視します。

**修復。** `rpm -V` が示した破損しているバージョンのカーネル（例:
`5.14.0-687.66.1.el9_8`）を再インストールし、その後検証します。

```bash
dnf remove --duplicates
dnf reinstall kernel-core-<バージョン> kernel-modules-core-<バージョン> kernel-modules-<バージョン>
dnf check
rpm -V kernel-core-<バージョン> kernel-modules-core-<バージョン> kernel-modules-<バージョン>
grubby --default-kernel
```

2 つの検証コマンドは、どちらも何も出力しないはずです。`grubby --default-kernel`
は最新のカーネルを示す必要があります。

**アップデートを再試行。** 管理対象アップデートを再実行します。**Settings →
XOA-HL Updates** から、または `systemctl start xoa-hl-update.service` で
実行できます。最後は `=== xoa-hl update finished successfully ===` で終わる
はずです。アプライアンスは自動では再起動しないため、その後で再起動して
ください。`dnf needs-restarting -r` は再起動が保留中かどうかを示し、再起動後は
`uname -r` が実行中のカーネルを示します。

`ce52` では、`kernel-modules` のインストール中に中断されたカーネルの
トランザクションについて、この修復をテストしました。`xz-libs` のような重複
パッケージ、中断された自動アップデート（`install` モード）、トランザクション
の前ではなく後に報告される失敗については、テストしていません。

## 既知の制限事項

- **自動アップデートは、再起動が保留中でも再起動不要と報告することがあります。**
  `v5.113.2_e281c536-ce52` では、手動アップデートですでにカーネルがインストール
  されていて、次の自動実行で行うことが何もない場合、履歴に `rebootNeeded: no`
  と記録されます。`dnf needs-restarting -r` で確認してください。修正は
  ローンチ後に予定されています。
  [issue #392](https://github.com/Vagrantin/xcp-hl/issues/392) を参照して
  ください。

- **再接続の修正をインストールするアップデートは、止まって見えることが
  あります。** アップデートを開始したページは、まだ古いコードで動いており、
  約 2.5 分で再接続の試行をやめます。*Reconnecting to xo-server* のままの
  場合は、`xo-server` に再び到達できるようになるまで待ってから、ページを
  更新してください。アップデート自体には影響しません。シェルからログを読むには
  `cat /var/lib/xoa-hl/update.log` を実行します。これは
  `v5.113.2_e281c536-ce18` 以前からのアップグレードで一度だけ該当します。
  [issue #103](https://github.com/Vagrantin/xcp-hl/issues/103) を参照して
  ください。

{: .note }
このディストリビューションがアルファ版であることを忘れないでください。
アップデートの前にリリースノートを読んでください。リリースのたびに互換性の
ない変更が入る前提であり、アップデートにホスト側の手作業が必要になることも
あります。
