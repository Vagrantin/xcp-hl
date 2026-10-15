---
title: Linux ゲストツールをインストールして確認する
description: Ubuntu 24.04 の管理エージェントを導入し、ゲスト情報と正常終了を確認します。
weight: 21
translationKey: xoa-manual-guest-tools
translationStatus: draft
sourceRevision: sha256:8c9c47b718efc4436950f5657e77083f7fb3d379db7f776360f830647c2ca1e2
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

使い捨ての Ubuntu 24.04 VM に管理エージェントを導入し、XOA-HL の表示とゲストの通常終了を確認します。カーネルのドライバー、エージェント、アプリケーションの正常性は、それぞれ別に確認します。

{{< callout type="info" >}}
ソース確認済みプレビュー：XOA-HL イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 (`e281c536`)。ゲスト側の対象は Ubuntu 24.04 LTS (Noble)、amd64 の `xe-guest-utilities` `7.20.2-0ubuntu1` です。実機のゲスト・ホストでの動作と、人による言語レビューは未実施です。対応ゲスト OS 一覧や Windows ツールの手順ではありません。
{{< /callout >}}

## 始める前に

- [最初の VM 作成](/docs/xoa-hl/create-vm/)などで新規インストールした使い捨ての Ubuntu 24.04 amd64 VM を使います。利用可能なコンソールと `sudo` 権限を持つゲストアカウントを用意します。完全な VM UUID、ホスト、ゲスト OS・カーネル、インストール済みホスト・アプライアンスの版を記録します。テンプレート名だけで OS を判断しないでください。
- この検証には XOA-HL 管理者アカウントを使います。ゲストのパッケージ管理権限は別です。VM の起動・停止には対象 VM の **operate** 権限が必要です。ブラウザーでログインしてもゲストの `sudo` 権限は得られません。
- 終了テスト用の保守時間を確保し、ゲストの作業を保存して、自動ジョブからテスト VM を除外します。重要なデータは入れず、重要なゲストに変更を適用する前に、独立した[バックアップと隔離復元](/docs/xoa-hl/backup-restore/)を検証します。
- ゲストの DNS・時刻が正しく、承認済みの Ubuntu Noble リポジトリ（`universe` を含む）へ接続できる必要があります。承認済みのラボ用ネットワークを使い、ミラーへの接続のためにホスト管理ネットワークを変更しないでください。この手順ではリポジトリの追加やツール ISO の利用は行いません。

以下のシェルコマンドは、必ず**このゲストのコンソール内**で実行します。XCP-HL ホストや XOA-HL アプライアンス上では実行しません。管理情報の確認と電源操作は、**アプライアンスのアドレスを開いたブラウザー**で行います。

## 1. ゲストと現在のツール状態を記録する {#guest-tools-status}

1. ブラウザーで記録した UUID の VM を選び、**実行中** (`Running`) を確認します。**一般** (`/#/vms/<vm-uuid>/general`) で仮想化方式、ツール・エージェントのメッセージ、報告 IP を記録します。**詳細設定 → Guest OS** で **Management agent version**、**OS name**、**OS kernel** を記録します。近くの設定項目は編集しません。
2. 同じ VM のコンソールで以下を確認します。パッケージがない、またはサービスが停止している場合は、その状態を記録します。別のマシンで実行する理由にはなりません。

```bash
cat /etc/os-release
uname -r
dpkg --print-architecture
systemd-detect-virt
dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
systemctl status xe-daemon.service --no-pager
```

**確認：** Ubuntu `24.04`、アーキテクチャ `amd64`、仮想化 `xen` であること。異なる場合は、その OS 向けに別途確認した手順を選びます。既にツールが入っている場合は、パッケージの入手元と版を記録し、以下の情報確認へ進みます。例に合わせるためだけに再インストールや更新をしないでください。

一般タブのメッセージには表示条件があります。VM が実行中でない場合、またはドライバー検出情報がない場合は表示されません。表示できる場合、ソースは PV ドライバー、管理エージェント、報告された最新状態フラグの順に確認します。「ツール未検出」「エージェント未検出」「エージェントが古い」「エージェント検出済み」は別の状態です。この版の日本語には **管理エージェント {version} のインストールを認識中**、**管理エージェントがインストールされていません。** などの表示があります。メッセージがないことはインストール済みの証明ではなく、検出済みでもアプリケーション・通信・セキュリティの検証にはなりません。

Linux カーネルの PV ドライバーとユーザー空間のエージェントは役割が異なります。以下の Ubuntu パッケージはエージェントを提供し、カーネルドライバーを置き換えるものではありません。XO のエージェント版はホストのゲストメトリクスから作られ、Ubuntu パッケージ版と一致するとは限りません。両方を記録し、表記の差だけでダウングレードや再導入をしないでください。

## 2. Ubuntu の管理エージェントを導入する {#install-linux-agent}

この手順では既存のツールが入っていないゲストを使います。ツール ISO、別ベンダーのエージェント、別パッケージを既に使っている場合は、先にその管理元と更新方法を別途確認してください。

1. ゲストの承認済みパッケージ索引を更新し、候補と処理のシミュレーションを確認します。

```bash
sudo apt-get update
apt-cache policy xe-guest-utilities
apt-get -s install xe-guest-utilities
```

2. 候補が予定した Ubuntu Noble リポジトリから来ることを確認します。ソース確認済みパッケージは `7.20.2-0ubuntu1` です。別の版や入手元の場合は、この検証前に再評価が必要です。リポジトリ・署名のエラー、候補なし、予定外の削除・更新があれば停止します。検証を無効化したり、無関係なリポジトリを追加したりしないでください。
3. 対話形式で処理内容を確認して導入し、パッケージのサービスを有効化・起動します。

```bash
sudo apt-get install xe-guest-utilities
sudo systemctl enable --now xe-daemon.service
dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
systemctl is-enabled xe-daemon.service
systemctl is-active xe-daemon.service
```

**確認：** パッケージ状態が `install ok installed`、ユニットが `enabled`、`active` であること。Noble のサービスは **`xe-daemon.service`** です。`proc-xen.mount` に依存し、Xen 仮想化とパスの条件があります。一般的な名称 `xe-linux-distribution.service` に置き換えないでください。インストーラー終了やユニット有効化だけでは、エージェントの稼働は証明できません。この導入手順に再起動やパッケージ削除は含みません。

## 3. 情報の更新と正常終了を確認する

1. 同じ実行中 VM の**一般**・**詳細設定**を更新し、ツールのメッセージ、報告エージェント版、OS、カーネルを記録します。OS・カーネルをゲストコンソールと比較します。`systemctl` が active でも、未検出・古い情報の表示が続く場合は未解決です。正確な観察を残し、合格にしないでください。
2. 報告 IP があれば、対象ゲストの予定したインターフェースと現在のアドレスに照合します。**IPv4アドレスが検出されていません** だけでエージェント故障とは判断できません。IPv6 のみ、または切断されたゲストに IPv4 がない場合があります。IP 表示は経路、DNS、SSH/RDP 接続の証明ではありません。必要な通信は別に確認します。
3. ゲストの作業をすべて保存します。ブラウザーで UUID を再確認し、通常の**仮想マシンの終了**を一度だけ選び、確認画面を読みます。強制終了やブロック回避を提案された場合は**キャンセル**します。それは正常終了の成功ではありません。エラーを記録し、ゲストが応答する場合は OS 自身の通常終了を使います。タスク中に繰り返し要求しないでください。
4. コンソールの終了と XOA-HL の **halted** (`Halted`) 状態、終了タスクが残っていないことを確認します。このテスト VM を**仮想マシンの起動**で一度起動し、コンソールログイン、アプリケーション・確認用ファイルの正常性、サービスと情報表示を再確認します。ゲストの終了・起動とエージェント検出は別々に記録します。一方で他方を証明することはできません。

**確認：** 正確なパッケージ・サービス、最新のゲスト情報、通常終了、次回起動後のサービス継続をすべて記録します。不足や失敗があれば受け入れ検証は未完了です。ライブマイグレーション、動的メモリ、ホットプラグ、静止化スナップショット、クリップボード、性能を証明するものではありません。

## 問題がある場合

| 症状 | 確認と次の対応 |
| --- | --- |
| パッケージがない、入手元が異なる | ゲストの OS・版、`apt-cache policy`、承認済み `universe` の利用可否、時刻・DNS、更新エラーを確認します。管理者とリポジトリ問題を解消し、ホスト・アプライアンス用パッケージをゲストへ入れないでください。 |
| ユニットがない、停止・失敗している | `dpkg -L xe-guest-utilities` でパッケージとファイルを確認します。`systemctl status xe-daemon.service proc-xen.mount --no-pager`、`sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager` を読み、設定変更前に Xen 条件と依存関係エラーを確認します。 |
| サービスは稼働、XO 情報がない・古い | VM の識別情報、実行中状態、ホスト接続を再確認します。ゲストのパッケージ・サービス情報と一般・詳細設定の表示、時刻を比較します。ハイパーバイザー再起動、警告の非表示、根拠のないドライバー交換はしないでください。 |
| 終了失敗、強制操作を提案される | 強制・回避をキャンセルし、正確なタスクエラーを保存してコンソールを確認します。可能ならゲストの通常終了を使います。強制電源断はデータを失う可能性があり、別途判断が必要です。 |
| 変更後にゲストが動かない | パッケージ処理と起動・サービスのログを保存します。ゲストコンソールと別途確立した復旧計画を使います。この手順は削除・ダウングレードによる自動復旧を保証しません。 |

原因不明の失敗を隠すために有効化・再起動・再導入を繰り返さないでください。[機密情報を除いた記録を報告](/docs/xoa-hl/troubleshooting/#問題を報告する)します。版、VM・ホスト ID、時刻、パッケージ入手元・版、サービス状態、正確な UI メッセージ、電源タスクの結果を含めます。ログや画面に個人名、アドレス、ゲストデータが入る場合があるため、元の記録は非公開で保管します。

今後の更新はゲスト OS・パッケージの保守時間を別途計画し、同じ観察を繰り返します。他の Linux、ツール ISO、Windows/BSD、ベンダー切り替え、更新・削除、対応ゲスト一覧は別の受け入れ検証です。[VM 操作](/docs/xoa-hl/vm-operations/)と[バックアップ・復元](/docs/xoa-hl/backup-restore/)へ進んでください。

## ソース

XO `e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c`：[一般タブの検出順序](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js)、[詳細設定のゲスト OS 項目](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js)、[ホストメトリクスの変換](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs)、[終了・強制の確認](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js)、[VM operate 権限](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs)。HomeLab の範囲：[修正の選択 `5f33c81f1ae2e74a300dcc33103f4e06cf565c19`](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh)。

ゲスト側の確認日 2026-10-15：Ubuntu Noble [パッケージ `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities)、[amd64 ファイル一覧](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist)、[版を固定した Debian パッケージソース](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`)。[XCP-ng の説明](https://docs.xcp-ng.org/vms/#linux-guest-tools)は上流の背景情報であり、HomeLab 実機での互換性を証明しません。

[固定 XO 版の EN/FR/JA ラベル](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl) / [HomeLab の言語フォールバック](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/compact-xo-locales.py).
