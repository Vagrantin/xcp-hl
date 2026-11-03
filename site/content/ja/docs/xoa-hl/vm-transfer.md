---
title: "VM の移行（マイグレーション）、エクスポート、インポート"
linkTitle: "VM の移行"
description: "VM をプール内の別のホストへ移行し、XVA ファイルにエクスポートして、コピーをインポートします。"
weight: 43
translationKey: xoa-manual-vm-transfer
translationStatus: draft
sourceRevision: sha256:1e0c1a71359bc2780a31862ccef13422bbb20137e03c5b77f967d92131a100d9
glossaryTerms: ["vm", "host", "pool", "sr", "snapshot", "backup"]
---

本番データを含まない使い捨ての VM を使用します。管理者として **XOA-HL アプライアンス**にログインし、ホスト、ストレージ、VM が利用できることを確認してください。移行とエクスポートは VM 全体を移動またはコピーする操作であり、どちらも独立した[バックアップと復元テスト](/docs/xoa-hl/backup-restore/)の代わりにはなりません。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce40`（Xen Orchestra 5.113.2）。公開済みのコードに基づく手順で、移行、エクスポート、インポートは検証環境でまだテストしていません。今後のバージョンでは異なる場合があります。
{{< /callout >}}

## 1. 操作を選ぶ

| 目的 | 操作 | 結果 |
| --- | --- | --- |
| 同じ VM をプール内の別のホストで実行する | **移設(マイグレーション)** | 同じ VM オブジェクト。ディスクは共有ストレージに残るか、選択した SR にコピーされる |
| 停止中の VM を持ち運べるファイルとして保存する | XVA として**エクスポート** | ブラウザーが保存するファイル。スケジュール、保持期間、復元確認はない |
| XVA ファイルから別の VM を作成する | **インポート** | ゲストの識別情報をコピーした新しい VM オブジェクト。クローンと同様に隔離する |
| 障害後に復旧する | [バックアップと復元](/docs/xoa-hl/backup-restore/) | 隔離した復元で確認した独立コピー |

このガイドは、**同じプール**内のホスト間の移行、圧縮なしの XVA エクスポート、XVA ファイルのインポートを扱います。プール間の移行、ネットワークの再割り当て、OVA ファイル、URL からのインポート、ディスク単体のインポート・エクスポート、VMware からのインポートは対象外です。HomeLab のメニューでは VMware インポートの項目が非表示になっています。

追加モードは [その他の転送モード](#transfer-modes)を参照してください。実機検証は別途必要です。

## 2. プール内で VM を移行する

開始前に確認する前提条件：

- プールに接続済みのホストが 2 台以上あり、VM と移行先ホストに対する管理権限を持っていること。
- 移行先ホストから VM のネットワークとストレージに到達できること。共有 SR 上のディスクはコピーされません。ローカル SR など、移行先から到達できないストレージ上のディスクはコピーされます。
- メンテナンス時間を確保すること。ライブマイグレーション中は実行中のゲストが短時間停止します。ディスクのコピーには時間がかかり、移行先 SR の空き容量が必要です。
- VM の ID、現在のホスト、各ディスクとその SR を記録し、コンソールへのログインやアプリケーションのテストなど、ゲストの確認方法を用意すること。

1. VM を開き、**移設(マイグレーション)** を選びます。実行中と停止中の VM で表示され、サスペンド中や一時停止中の VM では表示されません。セルフサービスのユーザーには表示されません。
2. **Migrate VM** で、**Select a destination host:** から同じプールの別のホストを選びます。このバージョンでは、移行ダイアログのラベルは翻訳されていません。一覧には現在のホストは含まれません。接続済みの別のプールのホストが表示される場合もありますが、この練習では選ばないでください。
3. ストレージの項目を確認します。すべてのディスクが共有 SR 上にあれば、SR の選択は不要です。そうでない場合、XO はメインの SR (**Select main SR…**) を要求し、VDI ごとに SR を選択できます。十分な空き容量がある書き込み可能な SR を選んでください。これらのディスクはコピーされます。
4. **Select a migration network:** はプール内の移行では省略できます。移行先ホストがプールに設定された移行用ネットワーク上にアドレスを持つ場合、XO はそのネットワークを事前に選択します。ネットワークを選択すると、XO は単純なプール内移行ではなくストレージ移行の処理を使います。プールの設計で別のネットワークが指定されていない限り、提示された値のままにしてください。
5. 確認してタスクの完了を待ちます。移行中に繰り返しクリックしないでください。
6. VM の**一般**タブを再読み込みします。ホスト、電源状態、コンソール、ゲストのネットワーク、アプリケーションを確認します。ディスクをコピーした場合は、各ディスクの配置先と両方の SR の空き容量を確認します。

{{< callout type="warning" >}}
VM が移行先ホストと互換性がないと XAPI が報告すると、XO は **Force migration** を提示します。この練習ではキャンセルし、CPU とホストの互換性を調べてください。強制移行によってゲストが使用できなくなる場合があります。
{{< /callout >}}

単純なプール内移行で SR が必要と報告されると、XO は自動的にストレージ移行として再試行します。このとき、移行先ホストに接続された SR、またはプールのデフォルト SR が使われます。短時間で終わると想定した移行が、ディスクのコピーになる場合があります。移行が失敗した場合は、タスクのエラーを保存し、再試行する前に VM のホスト、電源状態、関係するすべての SR 上のディスクを確認してください。強制オプションで再試行しないでください。

## 3. 停止中の VM を XVA ファイルにエクスポートする

VM に対する管理権限と、ブラウザーを実行するコンピューターの十分な空き容量が必要です。

1. ゲストを正常にシャットダウンし、**Halted** を確認します。VM の ID、名前、ディスクとその合計サイズを記録します。
2. **エクスポート**を選びます。**Type** は `xva` のままにします。**圧縮**は既定値の **Disabled** のままにします。その他の選択肢は GZIP (very slow) と、XCP-ng ホストでの Zstd です。圧縮した XVA のインポートはこのガイドの対象外です。
3. 確認します。**Download VM** には、ダウンロードリンク、**OK**、**キャンセル**が表示されます。リンクと **OK** は同じ URL を開き、メッセージではこの URL は短時間に一度だけ有効と説明されています。どちらか一方だけを使ってください。リンクを選んだ後、**キャンセル**でダイアログを閉じます。URL には一回限りのアクセストークンが含まれるため、使用するまで秘密情報として扱ってください。
4. ブラウザーは `<日付> - <VM 名>.xva` という名前のファイルを保存します。ダウンロードは最後まで続けてください。キャンセルするとエクスポートも停止します。記録したディスクサイズと比べて、ファイルサイズが妥当か確認します。
5. ブラウザーを実行するコンピューターで、`sha256sum "<ファイル>.xva"` などでファイルのチェックサムを記録します。インポート前のファイル確認に使います。

既定では、1 つのプールで同時に実行できる XVA エクスポートは 2 件までです。それを超えるダウンロードは待機せずに失敗します。実行中のエクスポートが終わってから、新しいリンクを取得してください。

XVA には VM のディスクと構成が含まれます。中のデータと同じように保管し、テストが終わったら削除してください。エクスポートファイルにはスケジュール、保持期間、復元の確認がないため、バックアップジョブではありません。

{{< callout type="warning" >}}
実行中の VM もエクスポートできますが、その場合 XO は `[XO Export] <VM 名>` という一時スナップショットをエクスポートします。このコピーはアプリケーションの整合性を保証しません。XO はダウンロード終了時にスナップショットを削除します。削除に失敗しても警告をログに記録するだけで、スナップショットが SR に残る場合があります。実行中の VM をエクスポートした後は、VM の**スナップショット**タブを確認してください。このガイドでは停止中の VM を使います。
{{< /callout >}}

## 4. XVA を隔離したコピーとしてインポートする

1. **インポート** > **VM** (`/#/import/vm`) を開きます。このメニュー項目は、少なくとも 1 つのプールを操作できる場合にだけ表示されます。
2. **作成先プール:** で対象のプールを選びます。**作成先SR:** にはプールのデフォルト SR が提示されます。十分な空き容量がある書き込み可能な SR を選んでください。
3. **OVA、あるいはXVAファイルをドラッグアンドドロップしてください。** と表示された領域に `.xva` ファイルをドロップします。一覧でファイル名とサイズを確認します。拡張子が `.xva` または `.ova` でないファイルは無視されます。**From URL** は無効のままにします。
4. **インポート**を選び、アップロードが終わるまでブラウザーのタブを開いたままにします。ファイルが 1 つの場合、成功すると XO は新しい VM のページを開きます。
5. インポートした VM は停止したままにします。ID を記録してください。名前が同じでも、元の VM とは別のオブジェクトです。混同しないよう名前を変更します。
6. 初回起動の前に**ネットワーク**を開き、[すべての仮想インターフェースを削除](/docs/xoa-hl/storage-networks/)するか、確認済みの外部隔離を用意します。コピーには、元の VM と同じゲスト OS、IP 設定、ホスト名、認証情報、アプリケーションの識別情報が含まれます。
7. コピーを起動し、コンソールと記録したテストデータを確認します。

インターフェースの MAC アドレスが、同じ VM の別のインターフェースや実行中の VM のインターフェースと重複している場合、XO は VM の起動を拒否します。エラーコードは `DUPLICATED_MAC_ADDRESS` です。強制起動はせず、先にインターフェースを削除または隔離してください。

インポートが失敗した場合 (**仮想マシン(VM)のインポートに失敗しました。**)、オブジェクトが残っている場合があります。再試行する前に、移行先 SR のディスクと VM 一覧で、試行中に作成されたオブジェクトを確認してください。確実に特定できた残りのオブジェクトだけを、[使い捨て VM の削除手順](/docs/xoa-hl/vm-operations/#delete-vm)で削除します。

## 5. 後片付け

1. インポートしたテスト VM を[使い捨て VM の削除手順](/docs/xoa-hl/vm-operations/#delete-vm)で削除します。
2. コンピューターと一時的な保存場所から XVA ファイルを削除します。
3. 元の VM が想定したホスト上に残っており、ディスクとデータが変わっていないことを確認します。

想定と異なる点があれば、記録を保存し、バージョンと機密情報を除いた ID を添えて[問題を報告](/docs/xoa-hl/troubleshooting/)してください。

{{< details title="出典" closed="true" >}}
XO 5 のコミット `e281c536` と公開済みの HomeLab パッチで確認：[VM 操作バー](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js)、[移行・エクスポート・インポートの操作](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js)、[移行ダイアログ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/migrate-vm-modal/index.js)、[既定の移行用ネットワーク](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/utils.js)、[エクスポートダイアログ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/export-vm-modal/index.js)、[圧縮の選択肢](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-compression.js)、[インポート画面](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js)、[VM API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs)、[XAPI の移行・インポート・起動時の確認](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs)、[エクスポート用スナップショットの処理](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs)、[同時エクスポート数](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml)、[画面のラベル](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js)。HomeLab のメニュー変更：[VMware インポートの項目](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzz-xoa-hl-hide-vmware-and-support-alert.patch)。
{{< /details >}}
## その他の転送モード (VM08) {#transfer-modes}

対象は XO 5.113.2 `e281c536`、XOA-HL ce40/ce47 のソースです。管理者、通常ディスクの使い捨て VM、コンソール、同期済みサンプルとチェックサム、空の VIF 一覧、無効なジョブ、スナップショット/インポート用容量、独立バックアップが必要です。モードごとに検証します。

1. **稼働中エクスポート：** サンプルを同期し、隔離 VM を動かしたまま **Export**、**XVA**、圧縮 **Disabled** を選択します。完全に保存してサイズとハッシュを記録します。一時 `[XO Export]` ポイントの削除とソースの健全性を完了/取消後に確認します。メモリーやアプリ整合性の保証ではありません。
2. **圧縮 XVA：** **GZIP (very slow)** (`native`) で繰り返し、ホストが提供する場合のみ **Zstd** を別に試します。選択値を記録し `.xva` を維持します。各完成ファイルを XVA 手順で **Import → VM** から試験 SR に入れます。非圧縮の成功は圧縮の証拠になりません。
3. **OVA：** 隔離 VM を **OVA** で出力します。XVA 圧縮指定は適用されません。**Import → VM** で `.ova` を開き、解析された名前、CPU、RAM、ディスク、ネットワークと SR を確認して一度インポートします。解析成功だけで起動や忠実な再現を判断しません。非対応形式は記録し、変換やディスク除外で回避しません。
4. **URL：** 完成したハッシュ確認済み XVA を、所有者管理下でアプライアンスから到達できる URL に置きます。**Import → VM → From URL**、**XVA**、正確な URL、試験 SR を指定します。ブラウザーからの到達だけでは不足です。認証情報を URL に入れません。この版の VM URL は XVA のみです。失敗後は残存オブジェクトを調べてから再試行します。
5. **ディスク単体：** **Import → Disk**、書き込み可能な試験 SR、既知の `.vhd`、`.vmdk`、`.raw` を指定します。ISO は別の SR 条件があります。名前、形式、サイズ、VDI UUID を確認します。ディスク作成だけでは起動 VM になりません。停止した復元 VM の空き位置に接続し、全 VIF を外して起動、サンプルを確認します。ソースの **Disks** のダウンロードは 1 VDI を出力します。提示された対応形式で保存/ハッシュ確認し、再インポートして同じ確認を行います。ディスク画面の URL 指定は **ISO** のみです。

各 VM の別 UUID、ディスク数/サイズ/SR、電源状態を確認します。停止したまま全 VIF を外してから起動し、コンソールとチェックサムを確認します。確認後は特定した試験オブジェクトだけを削除します。中断時はファイル/エラーとソース、転送先、ポイント、容量を記録します。ファイル名や通知だけでは復元成功ではありません。

固定ソース: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [@xen-orchestra/xapi/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [packages/xo-server/src/xapi/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [packages/xo-web/src/xo-app/vm-import/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [packages/xo-web/src/xo-app/disk-import/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [packages/xo-web/src/xo-app/vm/tab-disks.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [packages/xo-server/src/api/disk.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs).

**ラボ結果、2026-11-03(一部、ブラウザではなく API):** これらのページが使う REST と JSON-RPC のエクスポート/インポートメソッドで観察しました。ラボのゲスト(4 GiB ディスク)の実行中エクスポートは、非圧縮で 3,251,286,528 バイトで完了しました。`vm.export` の `compress` に `gzip` と `zstd` を指定すると、同じアーカイブ全体を包む gzip(323,244,900 バイト)と zstd(295,357,297 バイト)になり、チャンク単位の圧縮ではありません。どちらも展開後は 3,251,286,528 バイトです。REST エクスポートの `compress` は真偽値のみ受け付けます。両方の圧縮ファイルの URL インポートは成功しました(新しい MAC アドレスを持つ停止状態の新規 VM)。実行中ゲストの OVA エクスポートは `metadata.ovf` と 1 つの VMDK を生成しましたが、その OVA をインポート先へアップロードする処理は 9 分以上停止し、部分的な `[Importing...]` VM が残ったため、OVA インポートは未承認です。ディスクの URL インポートは VHD と raw のみ受け付け、VMDK と QCOW2 の URL インポートは拒否され、QCOW2 エクスポートは HTTP 500(`unknown error`)を返しました。VHD ファイルを `raw` としてインポートすると 2 MiB の誤ったディスクができるため、形式を正しく指定してください。ゲスト起動とデータのチェックサムは確認しておらず、このモードは未完了のままです。
