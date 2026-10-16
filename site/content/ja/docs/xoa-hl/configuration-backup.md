---
title: XO 設定のエクスポートと復旧の準備
description: 暗号化した設定を保存し、インポートとロールバックの制約を確認します。
weight: 41
translationKey: xoa-manual-configuration-backup
translationStatus: draft
sourceRevision: sha256:180ae9b2a6163db1325b4575e8cf083b05b36f83cd0dc30021bc5104b3f91bf7
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

アプライアンスの保守前に、VM バックアップとは別に XO 設定を保存します。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、`e281c536` の XO 5.113.2 をソースで確認したプレビューです。使い捨てのアプライアンスでのエクスポート・インポートと復旧テストは未完了です。このページはサポートされる復旧・ダウングレード経路を確立するものではありません。
{{< /callout >}}

## エクスポートの対象

Web エクスポートは、登録された XO 設定項目を保存します。ユーザーとグループ、アクセス規則、サーバー接続、リモート先、ジョブ、スケジュール、認証トークン、プラグイン設定などが含まれます。サーバーのパスワード、リモート先の認証情報、トークンを含む可能性があるため、機密情報として扱ってください。

| 対象 | 必要な保護 |
| --- | --- |
| XO 設定 | Settings → Config からエクスポート |
| ゲストのディスクとデータ | 別途 [VM のバックアップと復元](/docs/xoa-hl/backup-restore/) |
| ホスト・プールのメタデータ | [プールメタデータのバックアップ](#pool-metadata)として別途保護する。この設定エクスポートには含まれない |
| アプライアンスの OS、RPM、実行ログ | エクスポートには含まれない |
| サーバー TOML、TLS ファイル、更新設定、タイムゾーン | 別途記録する。エクスポートには含まれない |

エクスポートが完了しても、インストール環境を復元できるとは限りません。イメージとアプリケーションの識別情報を一緒に保存してください。

## 1. エクスポートをダウンロードして保存する

1. **ブラウザー**で XO 管理者としてログインします。[インストール済みのバージョン](/docs/xoa-hl/maintenance/)を記録します。
2. **Settings → Config** (`/#/settings/config`) を開き、**Export config** の **Download config** を選びます。表示言語でラベルが異なる場合も、画面のパスは同じです。
3. 一意のパスフレーズを入力して確定します。空欄にすると暗号化されません。アプライアンスを失っても使えるよう、パスフレーズは別に保存します。
4. ブラウザーが新しいウィンドウをブロックした場合はダウンロードを許可します。空でないファイルが保存されたことを確認します。API のファイル名は `config.json.gz` で、暗号化した場合は `.enc` が付きます。VM バックアップと誤解する名前に変更しないでください。
5. ファイルをアプライアンス外の保護されたストレージに移します。日付、ファイルサイズ、バージョン、暗号化の有無を記録します。新しいファイルが隔離したインポートテストに合格するまでは、以前のエクスポートも保存します。

**確認：** 元のアプライアンスを使わずに、ファイルと別保存したパスフレーズを取り出せることを確認します。ファイルを公開 Issue に添付したり、復号した内容を報告に貼り付けたりしないでください。

## 2. 隔離したインポートテストを準備する

{{< callout type="warning" >}}
インポートは保存されたサーバーに再接続し、保存されたスケジュールを有効にする可能性があります。既存項目を更新し、競合するユーザー ID を置き換える場合もあります。インポート全体のロールバックはなく、エラー後も一部の変更が残る可能性があります。未検証のエクスポートを調べるために本番アプライアンスを使わないでください。
{{< /callout >}}

記録したものと同じイメージ・パッケージの使い捨てアプライアンスを使います。インポート前にネットワークを制限し、テスト用ブラウザーからは接続できる一方、アプライアンスから本番ホスト、バックアップ先、外部サービスには接続できないようにします。この制限はインポートされる XO 設定の外で実施する必要があります。接続やスケジュールを事前に無効にしても、インポートで復元される可能性があります。

1. 新しいアプライアンスの状態を記録し、エクスポートした設定に含まれる認証情報を用意します。インポートでアカウントが変更される可能性があります。
2. **Settings → Config** でファイルを選択またはドロップし、**Import config** を選んでエクスポートのパスフレーズを入力します。成功またはエラーの表示を待ちます。
3. 成功したらログアウトし、エクスポートした管理者アカウントでログインを確認します。ユーザー、権限、リモート先、サーバー定義、ジョブ、スケジュールを元の記録と比較します。ネットワークを遮断している間のサーバー接続エラーは想定される結果です。
4. インポートしたスケジュールを無効にし、本番の接続先を削除または置き換えてから、使い捨てのテスト用リソースへのアクセスを許可します。各テスト操作の前に設定を再確認します。
5. 失敗したら、エラーと機密情報を除いた `xo-server` ログを記録します。次の試行では使い捨てアプライアンスを破棄して新しく作成します。失敗前の状態が維持されているとは考えないでください。

**未完了の検証：** 暗号化あり・なしの往復、誤ったパスフレーズ、ユーザーの競合、インポートの中断、接続先の隔離、エクスポートした管理者のログイン、代表的な権限とジョブ。成功の表示だけでは復旧テストに合格したことにはなりません。

## 3. プールメタデータを保存する {#pool-metadata}

この**ソース確認済みプレビュー**では、独立した **Pool metadata** ジョブを使います。XO は選択したプールの XAPI `/pool/xmldbdump` を取得し、リモート先の `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/` に `data` と `metadata.json` を書き込みます。これは Settings → Config のエクスポート、VM ディスクのバックアップ、アプライアンスのイメージ、検証済みのホスト復旧手段ではありません。メタデータからインフラの情報が分かる場合があります。リモート先のアクセスを制限し、公開 Issue に添付しないでください。

再構築できる使い捨ての 1 プールと XOA-HL の接続を用意し、そのプールのストレージとは別の障害領域に書き込み可能な専用 NFS バックアップ先を置きます。ゲストのデータには別の [VM バックアップと復元](/docs/xoa-hl/backup-restore/) 計画を保持します。導入済みのイメージ・パッケージと管理者によるメタデータ画面へのアクセスを確認してください。固定した UI にはプラン制限があるため、操作できなければ中止します。プール UUID、マスターとホストの識別情報、リモート先 ID と容量を記録します。本番プールを変更・復元して試してはいけません。

1. **Backup → New → Metadata** (`/#/backup/new/metadata`) で `lab-pool-metadata` ジョブを作ります。**Pool metadata** だけを有効にし、使い捨てプールを明示的に選択します。**XO config** はオフにして、専用リモート先だけを選びます。他のプールやリモート先は追加しません。タイムゾーンを明示したスケジュールを 1 つ作り、**Pool metadata retention** を `2` にして無効のままにします。保存後にジョブとスケジュールの ID、プール、リモート先、モード、保持数、無効状態を読み直します。保持されなければ中止します。
2. 保存したスケジュールを使い、異なる記録時刻 A/B/C に手動で 3 回実行します。各回の完了を待ってから次へ進みます。プールとリモート先ごとの子タスクを含むジョブログを確認します。全体の成功表示だけでリモートの完全なコピーを証明できません。各実行の ID と状態、元プールの UUID を記録します。
3. **Backup → Restore → Metadata** (`/#/backup/restore/metadata`) で、有効なリモート先の **pool** 行、時刻、利用可能なポイントを確認します。**Restore や Delete は選びません。** この単純な保持数 2 の例では A/B/C の実行と B/C の残存ポイントを照合します。ストレージ管理者が別経路でリモート先を確認できる場合、保持された各ポイントの `data` と `metadata.json` が空でなく、ジョブ・スケジュール・プールの識別情報が一致することを確認してもらいます。ファイルサイズと保護したハッシュを記録し、内容を公開しません。書き込み側はチェックサムを無効にしているため、一覧表示やタスクの成功は XAPI でのインポート成功を保証しません。不完全なポイントや削除結果の差異は調査用に保存します。

**バックアップ試行の合格条件：** スケジュールは無効のまま、3 回の実行が意図したプールとリモート先を示し、残存する B/C と保護されたファイルが記録した識別情報に一致します。エクスポート、書き込み、整理、一覧に失敗したら追加実行を止め、ログと一覧を保存します。名前だけを頼りにバックアップのパスを削除しないでください。

**復元の検証は未完了：** プールの復元は選んだポイントの `data` を、指定したターゲットプールの `/pool/xmldbdump` に送ります。状態を変更する操作であり、ここではロールバックを確認していません。実行前にプール管理者が、隔離した使い捨てターゲット、バージョンと識別情報が一致する復旧計画、別のイメージまたはメタデータの予備、本番ネットワーク・ストレージとの遮断、および復元後にホストとプールの接続・一覧を確認する方法を用意する必要があります。これらを確認してから、正確な 1 ポイントと 1 ターゲットを選びます。一括復元と別プールへの置き換えはこの試行に含めません。ポイントの存在やエクスポート成功だけを復旧の証拠にはしません。XO 設定エクスポートとゲストのバックアップは別に保管します。

## 復旧とロールバックの制約

実際に障害が発生した場合は、故障したアプライアンスと記録を保全し、正確なバージョンを特定して、そのバージョンで隔離テストに合格した復旧計画を使います。有効なスケジュールを持つ 2 つのコピーを同じ本番接続先に接続しないでください。

古い RPM があっても、完全なロールバックにはなりません。ダウングレードは OS の更新を戻さず、XO データや上記の別管理ファイルも復元しません。このリリースでの異なるバージョン間のインポートとダウングレードによる復旧は未検証です。更新に失敗した場合は[保守](/docs/xoa-hl/maintenance/)と[トラブルシューティング](/docs/xoa-hl/troubleshooting/)を参照してください。

## ソース

`e281c536` の XO ソース：[設定画面](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js)、[管理者 API とファイル形式](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs)、[暗号化とインポート処理](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs)、[サーバー再接続](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs)、[スケジュールの有効化](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs)、[ユーザーの競合](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs)。

プールメタデータ試行の XO `e281c536` ソース：[ジョブ編集とプラン制限](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js)、[管理者 API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs)、[プールのエクスポートとリモートファイル](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs)、[モードとリモート先の処理](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs)、[保持数による整理](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs)、[復元ポイントの選択](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js)、[XAPI のインポート先](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs)。
