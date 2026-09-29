---
title: はじめに
weight: 1
translationKey: getting-started
---

ハイパーバイザーをインストールし、XO Lite を開いて XOA-hl を展開し、仮想マシンを管理します。
{class="lead"}

<span id="start-overview"></span>

## XCP-hl とは

XCP-hl は XCP-ng 8.3 をベースにしたホームラボ向けディストリビューションです。ハードウェアに直接インストールして仮想マシンを動かします。**XO Lite** はホストが配信する軽量な管理画面です。**XOA-hl** は Xen Orchestra を実行する独立した VM で、ホストと VM を管理する Web UI を提供します。

XO Lite では **XOA-hl**（既定）、Vates 公式アプライアンス、Ronivay 版、独自の XVA イメージの 4 種類から選べます。このガイドでは XOA-hl を使用します。違いについては[機能](/docs/features)をご覧ください。

<span id="start-requirements"></span>

## 始める前に

- XCP-ng 8.3 に対応する専用マシンを用意し、ハードウェア仮想化を有効にしてください。CPU、メモリー、ネットワークの対応状況は[アップストリームの要件](https://docs.xcp-ng.org/installation/requirements/)で確認できます。
- 使用するディスクのデータをバックアップしてください。**インストールで選択したディスクのデータは消去されます。**
- 自動作成される 20 GB の ISO ライブラリーを利用するには、インストール先ディスクに **100 GB 以上**の容量と、VM に必要な空き容量を用意してください。対応する小容量ディスクではライブラリーなしの標準構成になります。[ISO ストレージ](/docs/features#iso-storage)をご覧ください。
- 固定の管理 IP アドレス、ゲートウェイ、DNS、NTP の設定を準備してください。固定 IP または DHCP 予約にすると、ホストへアクセスしやすくなります。
- ホストにネットワーク接続でき、ブラウザーが使える別のコンピューターを用意してください。アプライアンスの展開時には、選択したイメージの URL にもアクセスできる必要があります。

{{< callout type="warning" >}}
XCP-hl はホームラボとテスト向けのアルファ版です。リリースノートを確認し、バージョン間で変更があることを前提にしてください。バックアップはホストの外部に保存してください。
{{< /callout >}}

<span id="start-download"></span>

## ダウンロードと検証

{{< latest-iso-download text="最新 ISO をダウンロード" shaText="SHA256 チェックサム" >}}

<span id="start-verification"></span>

### ISO を検証する

同じリリースからチェックサムとその署名をダウンロードし、下記リンクのプロジェクトの公開鍵を使用します。鍵を信頼する前にフィンガープリント **2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A** を確認してください。鍵の従来の名前は `XCP-ng Community Edition (Master signing key)` です。

{{< verify-iso >}}

イメージ書き込みツールで ISO を USB メモリーに書き込むか、仮想インストールメディアとして接続します。書き込みで USB メモリーのデータが消去されるため、選択したデバイスを確認してください。

<span id="start-quick-start"></span>

## クイックスタート

<span id="start-install"></span>

### 1 · XCP-hl をインストールする

以下は **1 台のホストで始めるホームラボ向けの基本構成**です。著者の [XCP-ng 初回インストール記事](https://vagrantin.github.io/blog/20260107/xcp-ng-first-install.html)を基にしています。ディスク、ストレージ、ネットワークの設定は用途に合わせて調整してください。写真はアップストリームの XCP-ng 8.3 のもので、XCP-hl では表示が異なる場合があります。その他の選択肢は[アップストリームのインストールガイド](https://docs.xcp-ng.org/installation/install-xcp-ng/)をご覧ください。

1. **インストーラーを起動してキーボード配列を選びます。** インストールの警告とライセンス契約を読んでから進んでください。

   {{< screenshot src="install/keyboard.jpg" alt="インストーラーのキーボード配列選択" >}}

2. **システム用ディスクと VM 用ディスクを選びます。** デバイス名と容量を確認してください。インストール用 USB メモリーや、データを残したいディスクを選ばないでください。

   {{< screenshot src="install/system-disk.jpg" alt="システム用ディスクの選択" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="仮想マシン用ディスクの選択" >}}

3. **ストレージの種類を選びます。** ホームラボでは EXT のシンプロビジョニングが実用的な出発点です。データの書き込みに応じて仮想ディスクが容量を使用します。LVM は割り当てた容量を確保します。用途に合わせて選び、どちらでも空き容量を監視してください。

   {{< screenshot src="install/storage-type.jpg" alt="EXT または LVM ストレージの選択" >}}

4. **インストール元に Local media を選びます。** ダウンロードや USB メモリーの破損が疑われる場合は特に、表示されるメディア検証を実行してください。

   {{< screenshot src="install/source.jpg" alt="インストール元として Local media を選択" >}}

5. **root パスワードを設定して保管します。** XO Lite へのログインと、Xen Orchestra からホストへの接続に使います。

   {{< screenshot src="install/password.jpg" alt="ホストの root パスワード設定" >}}

6. **管理ネットワークと DNS を設定します。** 固定 IP または DHCP 予約を使い、ネットワークで必要な場合のみ VLAN を設定してください。ホスト名と到達可能な DNS サーバーを入力します。

   {{< screenshot src="install/network.jpg" alt="管理 IP アドレスとゲートウェイの設定" >}}
   {{< screenshot src="install/dns.jpg" alt="ホスト名と DNS サーバーの設定" >}}

7. **タイムゾーンと NTP サーバーを設定し、内容を確認します。** 公開 NTP サーバーにアクセスできない場合は内部サーバーを使ってください。開始前に選択したディスクを再確認します。

   {{< screenshot src="install/ntp.jpg" alt="時刻同期の設定" >}}
   {{< screenshot src="install/confirm.jpg" alt="インストール前の最終確認" >}}

8. **完了後にメディアを取り外して再起動します。** ホストのコンソールに表示される管理アドレスを控えてください。

   {{< screenshot src="install/complete.jpg" alt="インストール完了、再起動の準備" >}}

<span id="start-open-xo-lite"></span>

### 2 · XO Lite を開く

ブラウザーで `https://<ホストのIPアドレス>` を開きます。最初は自己署名証明書が使われるため、接続先が自分のホストであることを確認してから受け入れてください。インストール時のパスワードで `root` としてログインします。

XO Lite はホストが配信しており、別途 XO Lite 用の VM をインストールする必要はありません。

<span id="start-deploy-xoa"></span>

### 3 · XOA を展開する

XO Lite の **Deploy XOA** をクリックし、**XOA-hl** を選びます。フォームのネットワークと展開の項目を入力し、イメージと認証情報を確認して展開を開始してください。VM が起動してアドレスを取得するまで待ちます。初回ログイン時に既定のパスワードを変更してください。

ホストの xoa-proxy が選択した XVA イメージを XAPI に転送し、XAPI がアプライアンス VM を作成します。XOA-hl イメージは ISO のバージョンとは独立して、展開時に決まります。

<span id="start-connect-host"></span>

### 4 · XO をホストに接続する

ブラウザーで XOA-hl アプライアンスのアドレスを開きます。Xen Orchestra の `Settings → Servers → Add server` でホストのアドレスと root の認証情報を入力し、接続を確認してください。アプライアンスのアドレスは、ホストの XO Lite のアドレスとは別です。

接続後に Xen Orchestra でホストとストレージを確認し、ISO ライブラリーにインストール用 ISO をアップロードして、最初の VM を作成します。

<span id="start-updates"></span>

### 5 · 最新の状態に保つ

ホストの更新とアプライアンスの更新は別の操作です。XCP-hl にはホストの **Patches** タブ、XOA-hl には **Settings → XOA-HL Updates** を使います。開始前に[更新ガイド](/docs/guides/updates)を確認してください。

<span id="start-architecture"></span>

## アーキテクチャの概要

{{< architecture >}}

ブラウザーからは、**ホスト上の XO Lite** または **XOA-hl VM 内の Xen Orchestra** にアクセスします。XOA-hl は XAPI 経由でホストを管理します。他のゲスト VM は XOA-hl と並んで動作し、その内部で動くわけではありません。

<span id="start-components"></span>

## コンポーネント

[コンポーネント](/docs/components/)ではリポジトリ、固定されたアップストリームのバージョン、パッケージ、ビルドの流れを説明しています。[リリース一覧表](/docs/reference/release-matrix)は各 ISO とアプライアンスイメージに同梱されたバージョンを記録しており、結合テストによる互換性の認証ではありません。

<span id="start-license"></span>

## ライセンス

XCP-hl は **AGPL-3.0** で公開され、XCP-ng と Xen Orchestra を基にしています。独立したコミュニティープロジェクトであり、Vates SAS や XCP-ng プロジェクトとの提携、承認、サポート関係はありません。
