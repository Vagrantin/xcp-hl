---
title: XOA-HL のトラブルシューティングと問題報告
description: ログイン、ホスト接続、バックアップ、更新の失敗を調べます。
weight: 42
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:0b4aff1c1e2ce86c8e6e39cf46a9c33c23b4a840e997e96f5351a12e552a51df
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

症状と直前に行った操作から調べます。失敗した更新やインポートを再試行する前に記録を保全してください。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 のソースを確認したプレビューです。これらの確認は、アプライアンスで再現した障害や検証済み復旧の記録ではありません。以下のコマンドはハイパーバイザーホストではなくアプライアンス内で実行します。
{{< /callout >}}

## 次の確認を選ぶ

| 症状 | 確認と次の操作 | 続ける前の確認 |
| --- | --- | --- |
| アプライアンスのページが開かない | XO Lite で VM が動作中か、アドレスとネットワークが正しいか確認。コンソールから以下の `xo-server` とディスク容量を調べる | 正しい URL でログイン画面が開く |
| 初回ログインの認証情報で入れない | [初回ログイン](/docs/xoa-hl/first-login/)の Web 認証情報と代替アカウントを確認。許可されたコンソールから初期設定ログを調べる | ログインでき、初期パスワードを変更済み |
| ホストが有効でもインベントリが空 | Settings → Servers でエラーを読み、アドレス、認証情報、証明書の識別、アプライアンスからの接続を確認 | 対象ホストとストレージがエラーなく表示される |
| VM の作成やインストールが失敗 | [VM 手順](/docs/xoa-hl/create-vm/)とプール、テンプレート、SR 容量、ネットワーク、起動メディアを照合。再試行前にタスクのエラーを記録 | 使い捨て VM が目的のインストーラーを起動する |
| バックアップや復元が失敗 | ジョブログを読み、リモート先、認証情報、容量、対象 SR を確認。[バックアップ手順](/docs/xoa-hl/backup-restore/)を参照し、復元した NIC は初回起動前にすべて削除する | ジョブが成功し、隔離した復元ゲストに期待するデータがある |
| 更新画面が切断 | 管理されたインストールのログとサービス状態を確認。RPM は `xo-server` を再起動する。重複する処理を開始しない | 成功マーカー、期待するバージョン、ログイン、ホスト一覧を確認 |
| 更新確認が ERROR | `/run/xoa-hl/status` と確認サービスのログを読む。再確認前にリポジトリ・ネットワークのエラーや実行中の更新を調べる | 新しい結果が `UP_TO_DATE` または `AVAILABLE` |
| 自動更新が実行されない | 保存したモード、アプライアンスのタイムゾーン、遅延、タイマーを確認。停止中に逃した実行時間帯は起動時に再実行されない | 目的のタイマーが予定され、後の実行記録が時間帯と一致する |
| 設定インポートが失敗 | エラーとサーバーログを保存。一部の変更が残る可能性がある。[隔離したインポート](/docs/xoa-hl/configuration-backup/)を参照 | 新しい使い捨て環境でテストに合格する。失敗した対象が元の状態とは考えない |

## アプライアンスの読み取り専用診断

許可されたコンソールまたは SSH セッションを使い、必要に応じて root 権限を使います。最初の確認前や再起動後に実行時の状態ファイルがなくても、それ自体は障害の証拠ではありません。`systemctl status` が非ゼロを返した場合は、停止中や失敗状態の場合があります。表示された状態を読んでください。

```bash
rpm -q xoa-hl nodejs
timedatectl
df -h
systemctl status xo-server redis xoa-hl-update.service --no-pager
systemctl list-timers 'xoa-hl-*'
journalctl -u xo-server -u xoa-hl-check-update.service -u xoa-hl-update.service -u xoa-hl-auto-update.service --since '1 hour ago' --no-pager
tail -n 100 /var/log/xoa-first-boot.log
tail -n 100 /var/lib/xoa-hl/update.log
cat /run/xoa-hl/status
cat /var/lib/xoa-hl/auto-update.status
```

エラーを消す目的でデータベース、ログ、ロックを削除しないでください。ディスクが満杯の場合は、増加しているファイルを特定し、記録を保存してから削除対象を判断します。状態の意味と更新・再起動の判断は[保守](/docs/xoa-hl/maintenance/)を参照してください。自動実行の状態は過去の記録の場合があるため、UTC の時刻を照合します。

## よくある質問

**更新が表示されているのに確認コマンドが 100 を返すのはなぜですか？** パッケージの確認処理は `dnf check-update` の終了コード 100 を `AVAILABLE`、0 を `UP_TO_DATE`、その他を `ERROR` に変換します。更新があることはインストールの失敗ではありません。

**Stable に戻すと testing の更新が取り消されますか？** いいえ。チャネルは次回以降の確認・インストールで使うリポジトリを選びます。stable への変更はインストール済み候補版をダウングレードしません。

**設定エクスポートは VM バックアップやアプライアンスのロールバックに使えますか？** 代わりにはなりません。[設定の対象範囲と復旧の制約](/docs/xoa-hl/configuration-backup/)を確認し、ゲストのバックアップは別途保存します。

## 問題を報告する

[XCP-HL の Issue を作成](https://github.com/Vagrantin/xcp-hl/issues/new)し、次の情報をテキストで記載します。

- ページの URL と表示言語、または問題が起きたアプライアンス画面のパス。
- イメージタグ、About のバージョン、インストール済み RPM・Node のバージョン、stable/testing チャネル。
- 操作、正確な手順、期待した結果、実際のエラー。
- タイムゾーン付きの時刻、手動・自動モード、関連サービスの状態、機密情報を除いたログの抜粋。
- 使い捨て環境で再現するかどうかと、最後に正常動作したバージョン。

ログやスクリーンショットからパスワード、トークン、Cookie、非公開のホスト名・アドレス、ユーザー・ゲストのデータを除いてください。`xo-server` と初回起動のログは認証情報を含む可能性があります。設定エクスポート、TLS 秘密鍵、設定ファイル全体は添付しないでください。元の記録は非公開で保管します。

## ソース

対象リリースの動作：[更新スケジュール](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md)、[確認の終了コード](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh)、[サーバーサービス](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service)、[初回起動の設定](https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-credentials.sh)。リンク先の作業手順には、固定した UI・API ソースが記載されています。
