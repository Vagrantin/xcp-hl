---
title: "Linux ゲストツールをインストールする"
linkTitle: "ゲストツール"
description: "Linux ゲスト VM に管理エージェントをインストールし、XOA-HL の表示を確認します。"
weight: 41
translationKey: xoa-manual-guest-tools
translationStatus: reviewed
sourceRevision: sha256:b33c81ebb5d81c67bc786f64145b80c80a063e3836134f53b46590995ecf327e
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Linux ゲスト VM に管理エージェントをインストールし、XOA-HL の表示を確認して、正常なシャットダウンを試します。エージェントは XOA-HL ではなくゲストの中で動作します。手順では、パッケージを確認済みの Ubuntu 24.04 ゲストを例にしています。他の Linux ディストリビューションでは、それぞれのパッケージでエージェントを提供しています。ブラウザーで **XOA-HL アプライアンス** に管理者としてログインし、コマンドはゲストのコンソールで実行します。各セクションを順に進めてください。Windows など他の OS には、それぞれ別の手順が必要です。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce40`（Xen Orchestra 5.113.2）。公開済みのコードに基づく手順で、検証環境でのテストはまだです。ゲストのパッケージは Ubuntu 24.04 LTS（Noble）、amd64 用の `xe-guest-utilities` `7.20.2-0ubuntu1` です。
{{< /callout >}}

## 始める前に

- 新しくインストールした、重要なデータのない Ubuntu 24.04 amd64 のテスト用 VM を使います。たとえば[最初の仮想マシンを作成する](/docs/xoa-hl/create-vm/)で作った VM です。使えるコンソールと、`sudo` を使えるゲストのアカウントが必要です。
- VM の完全な UUID、ホスト、ゲストの OS とカーネル、インストール済みのホストとアプライアンスのバージョンを控えます。テンプレート名だけでは、インストールされた OS は分かりません。
- XOA-HL の管理者アカウントを使います。VM の起動と停止には、その VM の **operate** 権限が必要です。ゲスト内のパッケージ管理は別の権限です。XOA-HL にログインしても、ゲストの `sudo` 権限は得られません。
- シャットダウンのテストのために保守時間を確保します。ゲストの作業を保存し、VM をスケジュールされたジョブから外します。重要なゲストを変更する前に、独立した[バックアップを取り、隔離した復元を試します](/docs/xoa-hl/backup-restore/)。
- ゲストでは DNS が使え、時刻が正しく、承認済みの Ubuntu Noble リポジトリ（`universe` を含む）にアクセスできる必要があります。承認済みの検証用ネットワークを使います。パッケージのミラーに届かせるために、ホストの管理ネットワークを変更しないでください。この手順では、リポジトリの追加やツール ISO の利用は行いません。

このページのシェルコマンドは、必ず**ゲストのコンソール**で実行します。XCP-HL ホストや XOA-HL アプライアンスでは実行しません。VM の状態の確認と電源操作は、アプライアンスのアドレスを開いた**ブラウザー**で行います。

## ゲストツールの状態を確認する {#guest-tools-status}

1. ブラウザーで、控えた UUID の VM を開き、**Running** であることを確認します。
2. **一般**（`/#/vms/<id>/general`）を開きます。仮想化モード、ツールのメッセージ、表示された IP アドレスを控えます。
3. **詳細設定** を開き、**Guest OS** を見つけます。**Management agent version**、**OS name**、**OS kernel** を控えます。これらのタブでは何も変更しないでください。
4. VM のコンソールで次のコマンドを実行し、結果を控えます。

   ```bash
   cat /etc/os-release
   uname -r
   dpkg --print-architecture
   systemd-detect-virt
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl status xe-daemon.service --no-pager
   ```

   パッケージがない、またはサービスが停止している場合は、その結果を控えます。別のマシンでコマンドを実行する理由にはなりません。

**確認:** OS が Ubuntu `24.04`、アーキテクチャが `amd64` で、`systemd-detect-virt` が `xen` と表示します。そうでない場合は作業を止め、その OS 向けの手順を使います。ツールが既にインストールされている場合は、パッケージの入手元とバージョンを控えてから、[XOA-HL の表示を確認する](#check-reporting)に進みます。この例に合わせるためだけに、再インストールや更新をしないでください。

### ツールのメッセージの意味

**一般** のメッセージは、VM が **Running** で、XO にドライバーの情報がある場合にだけ表示されます。XO は PV ドライバー、管理エージェント、エージェントが最新かどうかの順に確認します。最初に当てはまるメッセージが表示されます。

| メッセージ | 意味 |
| --- | --- |
| **仮想マシン(VM)に準仮想ドライバ(Xen tools)がインストールされていません** | PV ドライバーが検出されていません |
| **管理エージェントがインストールされていません。** | ドライバーは検出されていますが、エージェントは検出されていません |
| **古いバージョン {version} の管理エージェントがインストールされています** | エージェントは検出されていますが、古いと報告されています |
| **管理エージェント {version} のインストールを認識中** | エージェントが検出され、最新と報告されています |

メッセージがないことは、ツールがインストール済みであることの証明にはなりません。エージェントが検出されても、アプリケーション、通信、セキュリティのテストにはなりません。

Linux カーネルの PV ドライバーと管理エージェント（ゲスト内のプログラム）は役割が異なります。以下の Ubuntu パッケージはエージェントをインストールするもので、カーネルのドライバーを置き換えるものではありません。XO に表示されるエージェントのバージョンはホストのゲストメトリクスから来ており、Ubuntu パッケージのバージョンと一致するとは限りません。両方を控えます。表記が違うというだけで、ダウングレードや再インストールをしないでください。ドライバー、エージェント、アプリケーションは、それぞれ別に確認します。

## Linux ゲストに管理エージェントをインストールする {#install-linux-agent}

ツールがまだインストールされていないゲストを使います。ツール ISO、ベンダーのエージェント、別のパッケージを既に使っている場合は、まず誰が管理し、どう更新するのかを確認します。

1. ゲストのコンソールでパッケージの一覧を更新し、パッケージの入手元を確認して、インストールをシミュレーションします。

   ```bash
   sudo apt-get update
   apt-cache policy xe-guest-utilities
   apt-get -s install xe-guest-utilities
   ```

2. 候補が予定した Ubuntu Noble リポジトリから来ていることを確認します。この手順はバージョン `7.20.2-0ubuntu1` で確認しています。別のバージョンや入手元の場合は、続ける前に内容を確認します。
3. リポジトリや署名のエラー、候補なし、予定外の削除や更新がある場合は、作業を止めます。検証を回避したり、無関係なリポジトリを追加したりしないでください。
4. パッケージをインストールします。提示された変更内容を読んでから受け入れます。

   ```bash
   sudo apt-get install xe-guest-utilities
   ```

5. サービスを有効にして起動し、パッケージとサービスを確認します。

   ```bash
   sudo systemctl enable --now xe-daemon.service
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl is-enabled xe-daemon.service
   systemctl is-active xe-daemon.service
   ```

**確認:** パッケージの状態が `install ok installed` で、サービスが `enabled` かつ `active` です。Ubuntu Noble のサービス名は **`xe-daemon.service`** です。このサービスは `proc-xen.mount` に依存し、Xen の仮想化とパスの条件を満たす場合にだけ systemd が起動します。一般的な名前の `xe-linux-distribution.service` に置き換えないでください。インストーラーの終了やサービスの有効化だけでは、エージェントが動いていることの証明にはなりません。この手順では、再起動もパッケージの削除も行いません。

## XOA-HL の表示を確認する {#check-reporting}

1. ブラウザーで、同じ実行中の VM の **一般** と **詳細設定** を更新します。ツールのメッセージ、エージェントのバージョン、OS、カーネルを控えます。
2. OS とカーネルを、ゲストのコンソールの表示と比べます。
3. 表示された IP アドレスを、ゲストの予定したインターフェースと現在のアドレスと比べます。

`systemctl` が `active` と表示しているのに、エージェントがない、または古いというメッセージが続く場合、問題は解決していません。見えている内容をそのまま控え、テストを合格にしないでください。

**IPv4アドレスが検出されていません** と表示されるだけでは、エージェントの故障とは言えません。IPv6 だけのゲストやネットワークのないゲストには、IPv4 アドレスがないことがあります。アドレスが表示されても、経路、DNS、SSH や RDP の接続の証明にはなりません。ゲストに必要な通信は別に確認します。

## 正常なシャットダウンを試す {#clean-shutdown}

1. ゲストの作業をすべて保存します。
2. ブラウザーで VM の UUID をもう一度確認します。**仮想マシンの終了** を 1 回だけ選び、確認のメッセージを読みます。
3. XO が強制シャットダウンや、ブロックされた操作の回避を提案した場合は、キャンセルします。それは正常なシャットダウンではありません。エラーを控えます。ゲストがまだ応答するなら、ゲストの中から通常どおりシャットダウンします。タスクの実行中に要求を繰り返さないでください。
4. コンソールでゲストがシャットダウンしたこと、XOA-HL が **Halted** と表示し、停止タスクが残っていないことを確認します。
5. **仮想マシンの起動** を 1 回だけ選びます。コンソールからログインし、アプリケーションやテスト用ファイルを確認します。
6. サービスの確認（`systemctl is-enabled` と `systemctl is-active`）と、[XOA-HL の表示を確認する](#check-reporting)をもう一度行います。

シャットダウンと起動の結果は、エージェントの検出とは分けて控えます。一方で他方を証明することはできません。

**確認:** 正確なパッケージとサービス、更新した XOA-HL の表示、正常なシャットダウン、再起動後のサービスのそれぞれに結果があります。足りない結果や失敗した結果があれば、テストは完了していません。ライブマイグレーション、動的メモリ、ホットプラグ、静止化スナップショット、クリップボード、性能はテストしません。

## うまくいかない場合

| 症状 | 確認すること |
| --- | --- |
| パッケージがない、または入手元が想定と違う | ゲストの OS とリリース、`apt-cache policy`、承認済みの `universe` リポジトリが使えるか、時刻と DNS、更新のエラーを確認します。リポジトリの問題は、その担当者と解決します。ホストやアプライアンス用のパッケージをゲストに入れないでください。 |
| サービスがない、停止している、または失敗している | `dpkg -L xe-guest-utilities` で、インストールされたパッケージとファイルを確認します。`systemctl status xe-daemon.service proc-xen.mount --no-pager` と `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager` を読みます。設定を変える前に、Xen の条件と依存関係のエラーを確認します。 |
| サービスは動いているが、XO ではエージェントがない、または古いと表示される | VM の識別情報、**Running** であること、ホストとの接続を確認します。ゲストのパッケージとサービスの結果を、**一般** と **詳細設定** の表示、それぞれの時刻と比べます。ハイパーバイザーの再起動、警告の非表示、根拠のないドライバーの交換はしないでください。 |
| **仮想マシンの終了** が失敗する、または強制を提案される | 強制や回避はキャンセルします。タスクの正確なエラーを残し、ゲストのコンソールを確認します。できればゲストの中からシャットダウンします。強制的な電源断ではデータが失われることがあり、別に判断が必要です。 |
| 変更の後にゲストが動かない | パッケージの履歴と、起動とサービスのログを残します。ゲストのコンソールと、別に用意した復旧計画を使います。この手順は、アンインストールやダウングレードによる自動的な巻き戻しを約束しません。 |

原因の分からない失敗を隠すために、有効化、再起動、再インストールを繰り返さないでください。[問題を報告](/docs/xoa-hl/troubleshooting/#report-a-problem)するときは、バージョン、VM とホストの ID、時刻、パッケージの入手元とバージョン、サービスの状態、正確なメッセージ、電源タスクの結果を含めます。ログやゲストの画面には、個人名、アドレス、データが含まれることがあります。報告からは除き、元の記録は非公開で保管します。

今後の更新では、ゲストの OS とパッケージのための保守時間を別に計画し、同じ確認を繰り返します。他の Linux ディストリビューション、ツール ISO からのインストール、Windows や BSD のツール、ベンダーの切り替え、パッケージの更新や削除、対応ゲストの一覧はここでは扱いません。次は[VM の管理](/docs/xoa-hl/vm-operations/)と[VM のバックアップと復元](/docs/xoa-hl/backup-restore/)を参照してください。

{{< details title="出典" closed="true" >}}
- **ツールの状態と電源操作**：[ツールのメッセージの順序](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js)、[Guest OS の項目](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js)、[ゲストメトリクスの対応付け](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs)、[終了と強制の確認](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js)、[VM の operate 権限](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs)。
- **HomeLab のビルド**：[xoa-hl のパッチ選択](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh)。
- **Ubuntu パッケージ（2026-10-15 確認）**：[パッケージ `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities)、[amd64 のファイル一覧](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist)、[Debian パッケージのソース](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz)（`debian/xe-guest-utilities.xe-daemon.service`、`debian/proc-xen.mount`）。
- **背景情報**：[XCP-ng の Linux ゲストツール](https://docs.xcp-ng.org/vms/#linux-guest-tools)（一般的な説明で、XCP-HL との互換性を示すものではありません）。
- **UI のラベル**：[XO のラベル一覧](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl)、[HomeLab の翻訳フォールバック](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/compact-xo-locales.py)。
{{< /details >}}
