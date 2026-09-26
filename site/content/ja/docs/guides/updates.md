---
title: アップデート
weight: 3
translationKey: updates
aliases: ["/ja/updates.html"]
---

XCP-hl も XOA-hl も、署名済みのパッケージを使ってその場でアップデート
できます。入れ直す必要は一切ありません。ホスト（XCP-hl）は、標準の XCP-ng と
同じく Xen Orchestra の **Patches** タブからアップデートします。
アプライアンス（XOA-hl）は、専用の **XOA-HL Updates** 設定ページから
アップデートします。
{class="lead"}

このページの前半と後半は同じ構成です。Xen Orchestra での手順、
コマンドラインでの同じ操作、内部の仕組み、前のバージョンに戻す方法の
順に説明します。

## XCP-hl（ホスト）のアップデート

### Xen Orchestra で行う

1. **アップデートがあることを確認します。** `Home > Hosts` では、
   アップデートが保留されているホストに、不足しているパッチの数を示す
   赤いバッジが付きます。

   {{< screenshot src="updates/xcp-hl-1-missing-patches.png" alt="ホストの一覧：ホストの赤いバッジが不足しているパッチの数を示している" >}}

2. **ホストの Patches タブを開きます。** ホストを選び、**Patches** を
   開きます。パッケージごとに名前、説明、バージョン、リリース、
   ダウンロードサイズが並び、行にある目のアイコンで RPM の変更履歴を
   表示できます。プール単位の画面 `Home > Pools > <プール> > Patches` にも
   同じ一覧が出ます。

   {{< screenshot src="updates/xcp-hl-2-patches-tab.png" alt="利用できるパッケージが並んだ、ホストの Patches タブ" >}}

3. **Install pool patches をクリックします。**

   {{< screenshot src="updates/xcp-hl-3-installing.png" alt="プールのパッチをインストールしている最中の Patches タブ" >}}

   {{< callout type="warning" >}}
   これは全部かゼロかの操作です。XCP-ng のアップデータープラグインは、
   XCP-ng 標準のリポジトリと XCP-hl のリポジトリをまとめて 1 回の
   `yum update` で処理します。そのため、このボタンは保留中の XCP-ng の
   アップデートも一緒に適用します。ここでは個別のパッケージを選べません。
   XCP-hl のパッケージだけを更新するには、下のコマンドラインを使って
   ください。
   {{< /callout >}}

4. **XOA-hl の再読み込みを待ちます。** アップデートの実行中に Xen
   Orchestra が再読み込みされ、しばらく時間がかかることがあります。
   あわてずに、自然に戻ってくるのを待ってください。

   {{< screenshot src="updates/xcp-hl-4-xoa-reloading.png" alt="ホストのアップデート中に再読み込みしている Xen Orchestra" >}}

5. **完了です。** バッジが消え、Patches タブにホストが最新の状態であると
   表示されます。

   {{< screenshot src="updates/xcp-hl-5-up-to-date.png" alt="ホストが完全に最新になった Patches タブ" >}}

### コマンドラインで行う

ホスト上で次のように実行します。

```bash
yum check-update                   # 何が利用できるか
yum update xcp-hl-release          # リポジトリの設定そのもの
yum update xo-lite-ce xoa-proxy    # XCP-hl のパッケージだけ
yum update                         # すべて（Patches タブと同じ）
```

### 仕組み

XCP-ng には `updater.py` という XAPI プラグインが同梱されており、Xen
Orchestra はこれに利用できるアップデートの一覧を問い合わせます。XOA-hl は
この問い合わせに XCP-hl のリポジトリを含めるように変更してあるため、
XCP-hl のパッケージが標準の XCP-ng のものと並んで表示されます。

リポジトリは `/etc/yum.repos.d/xcp-hl.repo` という 1 つのファイルで定義され、
`xcp-hl-release` パッケージが所有しています。

| リポジトリ ID | 内容 | 公開元 |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{{< callout type="error" >}}
このファイルのセクション名は変更しないでください。Xen Orchestra はこれらの
リポジトリ ID を `updater.py` に渡し、プラグインは渡されたリポジトリの
アップデートしか一覧に出しません。セクション名を変えてもエラーにはならず、
そのパッケージが Patches タブから黙って消えるだけです。
{{< /callout >}}

`yum` はすでに持っている `.repo` ファイルを読み直さないため、リポジトリの
設定は「一度コピーするファイル」ではなくパッケージとして配布しています。
設定の変更は `yum update xcp-hl-release` を通じてホストに届きます。

### 既存のホストでの初回設定

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

新しい ISO には最初から `xcp-hl-release` が入っているため、この手順は
必要ありません。

### 前のバージョンに戻す

各リポジトリは直近のリリースだけを公開しているため、戻せる範囲はそれに
限られます。以前のビルドに戻すには次のようにします。

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<バージョン>
```

## XOA-hl（アプライアンス）のアップデート

### Xen Orchestra で行う

1. **アップデートのページを開きます。** XOA-hl の Web 画面で
   `Settings > XOA-HL Updates` を開きます。インストールされている
   バージョンが表示されます。一度も確認していないうちは、状態は
   *Update status unknown* です。

   {{< screenshot src="updates/xoa-hl-1-update-tab.png" alt="まだ確認していない状態の XOA-HL Updates ページ" >}}

2. **Check for update をクリックします。** アップデートがあるパッケージが、
   バージョンとともに一覧で表示されます。

   {{< screenshot src="updates/xoa-hl-2-check-result.png" alt="確認の結果：利用できるアップデートとパッケージの一覧" >}}

3. **Update now をクリックします。** アップデートのログが、進行に合わせて
   ページに流れます。アップデートの途中で xo-server が再起動するため、
   ページには一時的に *Reconnecting* と表示され、その後は自動で続きます。

   {{< screenshot src="updates/xoa-hl-3-in-progress.png" alt="ログが流れている、実行中のアップデート" >}}

   {{< callout type="warning" >}}
   **Update now** は `xoa-hl` だけでなく、AlmaLinux やカーネルを含め、
   アプライアンスで保留中のすべてのパッケージをインストールします。
   {{< /callout >}}

4. **完了です。** アップデートが終わったらもう一度確認してください。
   ページに *Up to date* と表示されます。

   {{< screenshot src="updates/xoa-hl-4-up-to-date.png" alt="アプライアンスが最新であると表示している XOA-HL Updates ページ" >}}

### コマンドラインで行う

アプライアンス上で次のように実行します。

```bash
dnf check-update         # 何が利用できるか
dnf update xoa-hl        # アプライアンスのアプリケーションのみ
dnf update               # アプリケーションと AlmaLinux のベースをまとめて
```

### 仕組み

アプライアンスには専用の yum リポジトリがあり、`xoa-hl` パッケージ自身が
提供する `/etc/yum.repos.d/xoa-hl.repo` で定義されています。

| リポジトリ ID | 内容 | 公開元 |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

アップデートのページにある 2 つのボタンは、それぞれ次の systemd ユニットを
起動します。

| ユニット | 役割 |
|---|---|
| `xoa-hl-check-update.service` | `dnf check-update` を実行し、結果を `/run/xoa-hl/status` に書き込みます |
| `xoa-hl-update.service` | `dnf -y update` をすべて実行し、ログを `/var/lib/xoa-hl/update.log` に書き込みます |

{{< callout type="info" >}}
どちらのユニットにもタイマーは設定されていないため、**Check for update** を
クリックするまで XOA-hl のアップデートは確認されません。自動アップデートは
[issue #45](https://github.com/Vagrantin/xcp-hl/issues/45) で追跡しています。
{{< /callout >}}

### 前のバージョンに戻す

リポジトリには最新の 5 つのリリースが残っています。以前のリリースに戻すには
次のようにします。

```bash
dnf --showduplicates list xoa-hl
dnf downgrade xoa-hl-<バージョン>
```

## 検証と信頼

XCP-hl と XOA-hl のどちらのパッケージとリポジトリのメタデータも、XCP-hl の
GPG 鍵で署名しています。クライアント側の設定は `repo_gpgcheck=1` と
`gpgcheck=0` です。

RPM は主鍵ではなく GPG の**サブキー**で署名しています。ここには XCP-ng 8.3
のホスト側にある `rpm` ツール（バージョン 4.11）の既知の制限があります。
鍵をインポートしたときに主鍵しか登録しないため、サブキーによる署名は
`NOKEY` と報告され、署名自体は正しくてもパッケージを直接検証できません。

そこで信頼はリポジトリのメタデータを経由します。サブキーを理解できる本来の
GPG ツールが `repomd.xml` を検証します。このファイルには `primary.xml` の
チェックサムが記録され、`primary.xml` にはすべてのパッケージの
チェックサムが記録されています。つまり `repomd.xml` という 1 つのファイルを
検証すれば、リポジトリ内のすべての RPM を検証したことになります。

{{< callout type="warning" >}}
署名用サブキーは **2027 年 5 月 10 日**に期限切れになります。それ以降は、
サブキーの期限を延長し、公開されている鍵を更新し、各ホストで再インポート
するまで検証に失敗します。
{{< /callout >}}

## 既知の制限事項

現時点で既知の制限事項はありません。

{{< callout type="info" >}}
このディストリビューションがアルファ版であることを忘れないでください。
アップデートの前にリリースノートを読んでください。リリースのたびに互換性の
ない変更が入る前提であり、アップデートに手作業が必要になることもあります。
{{< /callout >}}
