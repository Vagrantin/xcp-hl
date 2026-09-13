---
layout: default
title: build-xoa-hl
parent: 開発者向け
grand_parent: 日本語
nav_order: 5
lang: ja
---

# build-xoa-hl
{: .no_toc }

XCP-ng 上で XOA-HL の VM アプライアンスをビルドし、XO Lite CE が展開する
XVA イメージを作る Packer のパイプラインです。
{: .fs-6 .fw-300 }

**リポジトリ：** [Vagrantin/build-xoa-hl](https://github.com/Vagrantin/build-xoa-hl)
· 言語：Bash / Packer の JSON / Kickstart · ライセンス：AGPL-3.0

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 目的

このリポジトリは **XOA HomeLab Edition の VM アプライアンス**をビルドします。
実機の **XCP-ng ホスト上**で Packer によりインストール・設定した
AlmaLinux 9 の VM に、[`xoa-hl`](xoa-hl.html) の RPM を入れたものです。
できあがるのは圧縮した **XVA イメージ**で、これが XO Lite CE の展開ボタンが
取り込む成果物になります。

このアプライアンスはビルドの時点では汎用のままです。初回起動時に 1 回だけ
動く 2 つのサービスを持っており、XO Lite が展開するときに XenStore から
設定情報（ネットワーク、管理者の資格情報）を読み取ります。そのため、1 つの
イメージをすべての利用者が使えます。

---

## リポジトリの構成

```
build-xoa-hl/
├── build.config.sample        ← インフラ設定のテンプレート（コピーして build.config にする）
├── scripts/
│   ├── setup-xoa-builder.sh   ← ビルドの入口：Kickstart と Packer の JSON を生成し、ビルドを実行
│   ├── xoa-first-boot.sh      ← VM 内フェーズ 1：XenStore → ネットワーク + 環境ファイル
│   └── xoa-credentials.sh     ← VM 内フェーズ 2：xo-cli で XO の管理者の資格情報を設定
├── systemd/
│   ├── xoa-first-boot.service
│   └── xoa-credentials.service
├── bin/                       ← 同梱した VMware VDDK のアーカイブ（V2V 対応）
└── artefact/                  ← ビルドとデバッグの成果物：ログ、導入済み RPM の一覧、メモ
```

---

## 事前に必要なもの

- `apt` と sudo が使える Linux のビルド用マシン（Linux Mint で開発して
  います）。セットアップ用のスクリプトが、必要なもの（HashiCorp の apt
  リポジトリから Packer、Packer プラグイン
  [`ddelnano/xenserver`](https://github.com/ddelnano/packer-plugin-xenserver)、
  `wget`、`curl`、`jq`、`ufw`）を自分で導入します。
- 接続できる **XCP-ng ホスト**（root の資格情報、`Local storage` の SR、
  名前の付いた VM 用ネットワークが必要）。
- GitHub で公開済みの [`xoa-hl`](xoa-hl.html) のリリース（最新リリースの
  RPM は自動で解決します）。
- `build.config`。`build.config.sample` からコピーし、XCP-ng ホストの IP
  アドレスと資格情報、ネットワーク名、VM 名と root のパスワード、
  AlmaLinux の ISO の URL、`xe-guest-utilities` の RPM の URL を記入します。

{: .warning }
`build.config` には**平文の資格情報**（XCP-ng の root のパスワード、VM の
root のパスワード）が入ります。決してコミットしないでください。git に入れて
よいのは `build.config.sample` だけです。

---

## ビルドの入口（scripts/setup-xoa-builder.sh）

ビルド用マシンで動き、Packer に必要なものをすべて生成します。

1. **`build.config` を読み込む**（存在しない場合は組み込みの既定値を使い
   ます）。
2. **必要なものを導入する。** apt のパッケージ、HashiCorp の Packer、
   `ddelnano/xenserver` の Packer プラグインです。
3. **8000〜9000/tcp のポートを開ける**（ufw）。Packer は内蔵の HTTP
   サーバーを使い、この範囲のポートで Kickstart のファイルを VM に配信します。
4. **AlmaLinux の ISO のチェックサムを解決する。** ミラーの BSD 形式の
   `CHECKSUM` ファイルを解析し、なければ GNU 形式の `SHA256SUMS` を使い
   ます。有効な SHA256 が見つからない場合はビルドを失敗させます
   （`build.config` で固定している場合を除きます）。
5. **xoa-hl の最新の RPM の URL を解決する。**
   `api.github.com/repos/Vagrantin/xoa-hl/releases` を調べ、`.rpm` の成果物
   を持つ最新のリリースを探します。`releases/latest` を使わないのは、
   [#22](https://github.com/Vagrantin/xcp-hl/issues/22) より前の
   `xoa-image-*` のリリース（XVA しか含まない）に当たることがあるためです。
6. **`inst.ks` を生成する。** Kickstart の応答ファイルです。`eth0` で
   DHCP、EXT4 でのパーティション分割（LVM なし）、SELinux とファイア
   ウォールは無効、パッケージは最小構成。`%post` で sshd と chrony を
   有効にし、`epel-release`、`wget`、`nc`、`vim` を導入して、`xo`
   ユーザー（`wheel` グループ）を作ります。
7. **`almalinux-build.json` を生成する。** Packer のテンプレートです
   （後述）。
8. **ビルドを実行する。** `packer validate` のあと
   `PACKER_LOG=1 packer build almalinux-build.json` を実行します。

---

## Packer のテンプレート（almalinux-build.json）

`xenserver-iso` のビルダーを 1 つだけ使います。Packer は AlmaLinux の ISO を
XCP-ng ホストへアップロードし、カーネルのコマンドラインに
`inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/inst.ks` を指定して VM
（メモリー 2 GB、ディスク 10 GB）を起動し、SSH を待ってからプロビジョナーを
実行します。

1. `dnf update -y`。
2. **xe-guest-utilities** と **xe-guest-utilities-xenstore** を導入します
   （RPM の URL は `build.config` から）。初回起動時に XenStore へ接続する
   ために必要です。
3. **Node.js 24** を導入します（NodeSource）。
4. **xoa-hl の RPM** を導入します。これにより XOA-HL 一式が入ります
   （[`xoa-hl`](xoa-hl.html) を参照。RPM の `%post` がリリースのアーカイブを
   `/opt/xo` にダウンロードし、`redis` と `xo-server` を有効にします）。
5. `xoa-first-boot.sh` と `xoa-credentials.sh` を `/root/` へ、2 つの
   systemd ユニットを `/etc/systemd/system/` へアップロードし、両方の
   ユニットを有効にします。
6. **イメージを軽量化します。** 無線 LAN のファームウェア、firewalld、
   sssd、NetworkManager の追加分、rsyslog、ドキュメント・man・info の
   ページ、英語以外のロケールを削除し、`dnf autoremove` と `clean all` を
   実行します。
7. **固有の情報を消します。** `/etc/machine-id` を空にして、展開された
   各 VM が自分で作り直すようにします。

ビルダーの重要な設定：`format: xva_compressed`（XVA を出力）と
`keep_vm: always`（ビルドした VM を確認用に XCP-ng ホストに残す）です。

---

## 初回起動時の自動設定

1 回だけ動く 2 つのサービスがイメージに組み込まれています。XO Lite は
アプライアンスを展開するときに、設定情報を XenStore
（`/local/domain/<domid>/vm-data/*`）へ書き込みます。

### フェーズ 1（xoa-first-boot.service）

**ネットワークが立ち上がる前**に動きます（`Before=network.target`、
`ConditionPathExists=!/var/lib/xoa-first-boot.done` が条件）。
スクリプトの処理は次のとおりです。

- `xenstore-read` で `vm-data` のキーを読みます。`ip`、`netmask`、
  `gateway`、`dns`、`ntp-servers`、`system-account-xoa-password`、および
  `admin-account` の JSON（メールアドレスとパスワード）です。
- それらを `/etc/xoa-first-boot.env`（モード 600）に保存します。
- NetworkManager の設定ファイル
  （`/etc/NetworkManager/system-connections/xoa-provisioned.nmconnection`）
  を書き出します。IP アドレスが指定されていれば固定 IP、なければ DHCP に
  します。
- 現地での調査に備えて `/var/log/xoa-first-boot.log` に詳しく記録します。

### フェーズ 2（xoa-credentials.service）

`network-online.target` と `xo-server.service` の**あと**に 1 回だけ動きます
（条件は `!/var/lib/xoa-credentials.done`）。スクリプトの処理は次の
とおりです。

- xo-server が 443 番ポートで応答するのを最大 3 分待ちます。
- システムユーザー `xo` の SSH のパスワードを、渡された値に設定します。
- 初期の資格情報を使って `xo-cli` を `wss://127.0.0.1` に登録し、
  `user.changePassword` と `user.set` を呼んで、渡された管理者の
  メールアドレスとパスワードを適用します。
- 終了時に**自分自身を削除します**（trap を使用）。完了の印を書き、2 つの
  ユニットとスクリプトを無効にして削除し、機密情報の入った環境ファイルを
  消します。

{: .note }
設定情報がない場合やフェーズ 2 が失敗した場合、アプライアンスは初期値の
`admin@admin.net` / `admin` のままになります。展開後に XO の Web 画面から
変更してください。

---

## 出力されるもの

- ビルド用マシンのビルドディレクトリー内の `output-xva/` にできる、圧縮
  された XVA イメージ。
- ビルドに使った VM 本体（`keep_vm: always` により XCP-ng ホストに残り
  ます）。
- 自動化されたパイプラインでは、**このリポジトリ**
  （`Vagrantin/build-xoa-hl`）の GitHub リリース。タグは
  `xoa-image-<日付>-<sha7>` で、`xoa-almalinux.xva` を成果物として持ちます。
  これが XO Lite の展開ボタンが解決する成果物です。

---

## 自動ビルドとオーケストレーター

毎日のパイプラインでは、`setup-xoa-builder.sh` の代わりに
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
の `xoa-vm-agent` crate を使います。同じ手順をプログラムから実行し、さらに
次のことを行います。

1. リポジトリの HEAD が最後にビルドした SHA と同じなら、ビルドを飛ばします。
2. まず `Vagrantin/xoa-hl` の `build-xoa.yml` ワークフローを
   `workflow_dispatch` で実行し、RPM のリリースを待ちます。
3. 生成した `inst.ks` と `almalinux-build.json` で `packer validate` と
   `packer build` を実行します。
4. XVA を、**`Vagrantin/build-xoa-hl`**（このリポジトリ）の
   `xoa-image-<日付>-<sha7>` というタグの GitHub リリースとして公開します
   （`<sha7>` はイメージのビルド元となった `xoa-hl` のコミットです。その
   コミットは別のリポジトリにあるため、タグは `main` に作り、元のコミットは
   リリースの本文に記録します）。イメージのリリースは
   [リリース一覧表](../release-matrix.html#xoa-hl-releases)に記録します。

{: .note }
[#22](https://github.com/Vagrantin/xcp-hl/issues/22) までは、イメージは
`Vagrantin/xoa-hl` で公開していました。すでに配布済みの ISO がそれらを解決し
続けられるよう、これらのリリースはそのままにしてあります。そのため、
`xoa-hl` で RPM を探すツールは、今も `xoa-image-*` のタグを飛ばす必要が
あります。

---

## 開発に参加する

参加の方法はまだ正式には決めていません。今のところは
[XCP-hl リポジトリ](https://github.com/Vagrantin/xcp-hl/issues) で issue を
作ってください。
