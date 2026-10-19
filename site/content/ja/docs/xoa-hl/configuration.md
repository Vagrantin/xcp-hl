---
title: "アプライアンスサービスの設定"
linkTitle: "サービスの設定"
description: "設定ファイルの場所、アクセス経路と証明書の確認、変更の安全な適用方法を説明します。"
weight: 91
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:ba4a7450e3edaab0d44d601a5d06d8ccfaaa4026f7bdf8cda0d283847e6533f4
glossaryTerms: ["appliance", "host", "pool"]
---

xo-server の設定は、管理画面からエクスポートする設定や記録とは別に管理します。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 のソースを確認したリファレンスです。後続リリースでは動作が変わる可能性があります。実際のアプライアンスでの検証と人による翻訳レビューは未完了です。
{{< /callout >}}

## 設定の場所

| 場所 | ce38 での役割 | 扱い方 |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` と `sample.config.toml` | パッケージの既定値とコメント付きの参考設定 | 参照用。パッケージの更新で置き換わる |
| `/root/.config/xo-server/config.toml` | ファイルがない場合だけ作成する運用者の設定 | 編集前に非公開でバックアップ。RPM の初期設定処理では保持する |
| `/root/.config/xo-server/config.z-auto.json` | サーバーが書き込む設定 | 上書き関係を調べる際に存在を確認。無条件で置き換えない |
| Redis データベース | XO のアプリケーション記録 | 文書化した管理画面のエクスポートとインポートの範囲に従う |
| `/etc/xoa-hl/update.conf` | HomeLab 更新のモード、スケジュール、チャネル | Settings → XOA-HL Updates と更新ガイドを優先する |
| `/opt/xo/xoahl.crt` と `xoahl.key` | TLS 証明書と秘密鍵 | 別途保管。問題報告に秘密鍵を添付しない |

配布された systemd ユニットは root で実行し、XDG のユーザー設定を使います。ローダーは `/etc/xo-server/config.*` やローカルの `.xo-server.*` も読み込み、複数のファイルをマージできます。有効な値を判断する前に、ユニットのカスタム設定と他の設定ファイルを確認します。このページは配布されたユニットを対象とし、独自のサービスアカウントは対象外です。

[設定エクスポート](/docs/xoa-hl/configuration-backup/)には運用者の TOML、TLS ファイル、更新設定は含まれません。変更は[保守](/docs/xoa-hl/maintenance/)と[アップデート](/docs/guides/updates/)を参照してください。

## 例：アプライアンス URL を通知する

`http.publicUrl` はプールの検出に使う URL を指定します。リスナー、証明書、DNS レコードは作成しません。DNS と信頼された証明書が一致する実際の HTTPS URL を選び、まずブラウザーでのアクセスを確認します。変更前に[管理担当と検出](/docs/xoa-hl/hosts-pools/)を参照してください。

使い捨ての検証環境で、**既存の** `[http]` テーブルに設定を追加します。次の最小例は配布された HTTPS リスナーと Redis URI を保持します。カスタマイズ済みのファイルをそのまま置き換える例ではありません。

```toml
[http]
publicUrl = "https://xoa.lab.example"

[[http.listen]]
port = 443
cert = "/opt/xo/xoahl.crt"
key = "/opt/xo/xoahl.key"

[redis]
uri = "redis://127.0.0.1:6379/0"
```

別の `[http]` テーブルを追加したり、既存のリスナーを削除したりしないでください。実際の証明書と鍵のパスを維持します。RPM はインストール時に初期の自己署名証明書と鍵を生成し、共通の鍵は配布しません。鍵や証明書、または `/var/lib/xoa-hl/tls-generated` マーカーがない場合は生成されるので、更新前に実際の TLS 状態を記録します。証明書の交換、リバースプロキシ、Redis の移行は個別の検証が必要です。

## 隔離する前に管理経路を把握する {#management-network}

これは上記 ce38 イメージに対する**ソース確認済みの読み取り専用 SE07 事前確認**です。同梱の初期設定は HTTPS のポート `443` で待ち受けますが、運用者の設定、プロキシ、ファイアウォール、別のイメージでは実際の経路が変わります。UI から汎用的なファイアウォール許可規則は決まりません。ACL、VIF、ホストの管理 PIF、スイッチのポリシーを変更する前に、許可する管理クライアント・サブネット・サービス・バックアップ先と、独立したコンソール経路をネットワーク・ホスト担当者と合意します。

| 確認する経路 | 読み取り結果と限界 |
| --- | --- |
| 許可済みブラウザー → XOA-HL | アプライアンス VM とアドレス、名前解決結果、実際の HTTPS エンドポイント、証明書の識別情報を記録します。許可済みクライアントから新規ログインとホスト一覧を確認します。同梱の待ち受けポートは `443` ですが、インストール済み設定と実効経路を調べます。`http.publicUrl` はアドレスを通知するだけで、待ち受けを作りません。 |
| XOA-HL → 管理するホスト・プール | **設定 → サーバ一覧**で接続先アドレス、予定したプール・ホスト ID、証明書の扱いを記録します。現在の一覧と、実験環境で既に受け入れ確認している場合は、読み取り専用の[ホスト統計](/docs/xoa-hl/hosts-pools/#host-statistics)の新しい標本を確認します。ブラウザーのログインだけではホスト到達性は証明できません。 |
| ブラウザー → XOA-HL 経由のコンソール → VM の所属ホスト | コンソールが必要なら、[コンソールガイド](/docs/xoa-hl/vm-operations/#vm-console)に従い、稼働中の使い捨て VM 1 台を開いてブラウザーの結果と所属ホストを記録します。固定したソースのコンソールプロキシはアプライアンスからホストへの別の WebSocket 経路を作ります。一覧の読み取り成功だけでは確認できません。 |
| XOA-HL → バックアップ先と更新先 | 設定済みの各バックアップ先、アプライアンスのパッケージ・DNS・時刻の依存先と担当者を列挙します。バックアップ先は[専用の手順](/docs/xoa-hl/backup-restore/)で、パッケージへの接続は[アプライアンス更新ガイド](/docs/xoa-hl/maintenance/)で検証します。Web ログインの結果から推測しないでください。 |

**リリースを特定した再構築可能な実験環境**で、必要な各経路について送信元クライアント、宛先名・アドレス、サービス、結果と時刻を記録します。ネットワーク担当者に、明示的に許可していないテストクライアントが Web ログインへ接続できないことを、許可済みの試験と独立したログで検証してもらいます。ping が拒否されても HTTPS の隔離や管理の可用性は証明できません。制限予定の経路とは別のコンソールを維持します。ポリシー変更が別途承認されたら、担当者が管理する規則を一つずつ変更し、同じ許可・拒否サービス試験を繰り返し、ログイン、ホスト一覧、コンソール、バックアップ範囲を作業終了前に確認します。必要な経路が失敗したりアクセスを失ったりしたら中止し、独立コンソールからネットワーク担当者の記録済み復旧手順に従います。近道として XOA の接続を削除したりホスト管理 PIF を変更したりしないでください。

このソース確認ではアプライアンス、ホスト、ファイアウォールは変更していません。実際の待ち受け、クライアント分離、プロキシ・NAT 経路、ホストとバックアップ先のポート、拒否試験、サービス継続、復旧は実機での受け入れ確認が必要です。この資料だけから本番用の許可リストを作らないでください。

## 更新前に HTTPS 証明書を調べる {#tls-certificate-preflight}

これは上記 ce38 ソースに対する**読み取り専用の SE06 事前確認**です。初期設定は `/opt/xo/xoahl.crt` と `/opt/xo/xoahl.key` を使う `443` 番ポートの HTTPS 待ち受けを書きますが、その後の設定変更やリバースプロキシで TLS 終端は変わります。RPM は共通の秘密鍵を配布しません。インストール時にどちらかのファイル、または `/var/lib/xoa-hl/tls-generated` マーカーがないと、自己署名の `CN=xoa.local` のペアを生成します。後のパッケージ処理でも、マーカーやファイルが欠けていれば再生成され得ます。また `%posttrans` は `xo-server` を再起動します。更新計画の前に実機のパスとパッケージ状態を記録し、マーカー削除を証明書更新の手段にしないでください。

1. 独立したコンソールとローカル管理者を確保し、インストール済みイメージ・パッケージ、実効 `http.listen` 値、マージされる設定の上書きを非公開で確認します。`systemctl cat xo-server` でサービスの上書きを調べます。前段のリバースプロキシ、ロードバランサー、TLS 終端の有無を記録します。`http.publicUrl` は通知先アドレスであり、待ち受けやブラウザーが見る証明書の証拠ではありません。複数の待ち受けや予期しない `443` 番ポートの所有者があれば中止します。
2. **アプライアンス上で**、設定された証明書・秘密鍵・マーカーのメタデータだけを調べます。出荷時パスに対する次の読み取り専用コマンドは、秘密鍵の中身を出さずにファイル権限と公開証明書の項目を表示します。

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   設定が異なる場合は**実際のペア**のパスを使います。ファイルやマーカーの欠落は更新・再起動前に調査する条件であり、直ちに新しいペアを作る指示ではありません。秘密鍵や設定全体を画像・ログ・Issue に公開しないでください。
3. **許可されたクライアント**から実際の HTTPS 接続先と新しいブラウザーログインを確認します。OpenSSL が利用でき、担当者から信頼チェーンが提供された場合、実際の DNS 名とポートを使い `openssl s_client -connect <name>:<port> -servername <name> -verify_hostname <name> -verify_return_error -brief </dev/null` を実行します（私設 CA には担当者が承認した `-CAfile <ca-path>` を追加）。提示された証明書のフィンガープリント、名前、チェーン、有効期限を予定した接続先と比較します。初期の自己署名証明書は信頼検証に失敗し得ます。その結果を記録し、検証を無効にしたり信頼済みと扱ったりしないでください。プロキシが TLS を終端する場合、その証明書はアプライアンス内のファイルと異なり得るため、両方の経路を別々に記録します。
4. 更新を予定する前に、証明書とアプライアンスの担当者と、新しいチェーン、一致する秘密鍵、対象の名前、期限、安全な保管、ファイルの所有者・権限、独立した復旧コンソール、現在の**証明書ペア・マーカー・運用者設定**の非公開バックアップを特定します。ジョブ終了後の保守時間、変更する正確な待ち受け・プロキシ、検証済みの再起動・復旧手順を合意します。変更後は、信頼できる新規ブラウザーログイン、正しいフィンガープリント、維持したローカル管理者、ホスト・プール一覧、コンソールを確認します。構文が正しいこと、ファイルがあること、サービス再起動の成功だけでは、クライアントの信頼や証明書の正しい識別は証明できません。

このソース確認では証明書を更新していません。実機の待ち受け、信頼チェーン、更新方法、鍵と証明書の一致、パッケージ更新後の維持、障害、復旧は実験環境での検証待ちです。この一覧を本番の更新手順として適用しないでください。

## 構文を確認して保守時間に適用する

元の運用者設定を非公開でアプライアンス外に保存し、アクセス権も記録します。コンソール接続を準備し、バックアップ、復元、管理ジョブの終了を待ちます。編集後、アプライアンス内で root としてパーサーを実行します。

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` は構文が正しいことだけを示します。アクセス権、TLS の信頼、マージ結果、到達性は確認しません。ここで説明するパーサーとマージ動作は合成設定でテストしましたが、公開アプライアンス上では未検証です。再起動前に構文エラーを解消します。

合意した保守時間に適用して確認します。

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

再起動で管理画面の接続が切れます。想定したアドレスへ接続し直し、ログイン、ホストのインベントリ、次回のマーク後の検出を確認します。起動に失敗した場合はコンソールで保存した設定を戻し、再度構文を確認して 1 回再起動します。結果が不明なら[トラブルシューティング](/docs/xoa-hl/troubleshooting/)を参照してください。共有するログから機密情報を除去します。

## ソース

[bootstrap](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh), [RPM lifecycle](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [service](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service), [configuration loader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [defaults](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [sample](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [pool discovery](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).

上記固定バージョンの管理経路ソース：[サーバー接続](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs)、[所属ホストへのコンソールプロキシ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs)。個別環境のポートと到達性は直接観察して確認します。

同じ固定バージョンの TLS 調査：[生成ペア・マーカー・パッケージ処理後の再起動](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec)、[初期の待ち受け](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh)、[実効待ち受けの設定](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs)。OpenSSL の参考：[x509 の調査](https://docs.openssl.org/3.0/man1/openssl-x509/)と [s_client の検証](https://docs.openssl.org/3.0/man1/openssl-s_client/)。オプションを使う前に実機の OpenSSL バージョンを確認してください。
