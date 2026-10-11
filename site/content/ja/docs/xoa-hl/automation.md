---
title: xo-cli によるインベントリの自動化
description: メソッドを検出し、インベントリを読み取り、短期 CLI トークンを失効します。
weight: 72
translationKey: xoa-manual-automation
translationStatus: draft
sourceRevision: sha256:d62ec0a49c44ac7275b68cb4b2cf81eabcafc83118ff7e2186109ad545cfe4f1
glossaryTerms: ["appliance", "host", "vm"]
---

VM を変更する自動化を作る前に、同梱の xo-cli で小さな読み取り専用インベントリを試します。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 のソースを確認したリファレンスです。後続リリースでは動作が変わる可能性があります。実際のアプライアンスでの検証と人による翻訳レビューは未完了です。
{{< /callout >}}

固定コミットのクライアントは `xo-cli` **0.32.2** と `xo-lib` **0.11.1** です。以下のコマンドは、この CLI ソースを合成のローカル HTTPS/WebSocket サーバーに接続して実行し、TLS の拒否と許可、パスワード入力、期限の要求、メソッド検出、インベントリ引数、ローカルの削除を確認しました。クライアントの契約を確認したもので、実アプライアンス、期限の強制、オブジェクトの権限、XAPI 操作の検証ではありません。

## 1. 検証環境と TLS の信頼を準備する

**アプライアンス内**で、同梱の `/usr/local/bin/xo-cli` を専用の Bash セッションから実行します。一般ユーザーのテストアカウントと使い捨ての VM を用意します。[保守](/docs/xoa-hl/maintenance/)でインストール済みリリースを確認し、認可は[権限ガイド](/docs/xoa-hl/permissions/)で別にテストします。

証明書と一致する DNS 名を使います。信頼できる経路で公開 CA または証明書を取得し、別途フィンガープリントを確認します。例のパスを PEM ファイルに置き換え、URL とメールアドレスも変更します。`NODE_EXTRA_CA_CERTS` は信頼を追加しますが、ホスト名の検証は無効にしません。初期の自己署名証明書 `xoa.local` では検証環境の DNS や証明書の準備が必要な場合があります。`--allowUnauthorized` や `NODE_TLS_REJECT_UNAUTHORIZED=0` で失敗を回避しないでください。

## 2. 有効期間の短いトークンを登録する

この関数は認証情報を新しいディレクトリに隔離し、既存の CLI 設定を保持します。制限した umask で新規ファイルを保護します。登録時にパスワードを求められます。位置引数に追加したり、URL にトークンを埋め込んだりしないでください。OTP が必要なアカウントでは、URL の前に有効なコードで `--otp CODE` を追加します。

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

固定ソースのサーバー既定値は 30 日、最大は 0.5 年です。要求する `1 hour` は意図的に短くしています。サーバー設定によって制限は変わります。トークンはユーザーの権限を持ち、専用の読み取り専用スコープではありません。設定ファイルを認証情報として扱い、シェルのトレース、問題報告に添付するバックアップ、バージョン管理に含めません。登録は認証状態を作成しますが、後続の例はデータを読み取るだけです。

## 3. 検出と読み取り

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| コマンド | 想定する解釈 |
| --- | --- |
| `list-commands xo.getAllObjects` | 人が読むメソッド引数。検出は権限の付与ではない |
| `system.getServerVersion --json` | このコミットでは `"5.193.1"` というサーバーパッケージ版。XO 製品版とは異なる |
| `list-objects --id --name_label --power_state type=VM` | 指定プロパティに絞った JSON 配列。VM の状態は変更しない |
| `xo.getAllObjects --json …` | オブジェクト ID をキーとする JSON オブジェクト。オブジェクト型のフィルターと数値の上限 |

フラグは引数の前に置きます。`json:` は型を持つ JSON を生成し、`limit=json:1` は数値、`limit=1` は文字列を送ります。最後のコマンドは **WebSocket `/api/`** 上の次の JSON-RPC 要求に対応します。HTTP POST の例ではありません。

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

インベントリのフィルターと出力項目の選択は、**アクセスを制限する境界ではありません**。この API がユーザー画面の表示対象だけにインベントリを制限することや、出力から省いた項目が取得されていないことを想定しないでください。結果を非公開で扱い、アカウントの実際の可視性を別途確認します。ラベルは固定 ID ではありません。件数を制限した結果は完全なインベントリでも、常に同じ VM を選ぶ方法でもありません。

## 4. 失効と削除

同じテストユーザーの独立したブラウザーセッションで **User → Authentication tokens** (`/#/user`) を開き、この CLI クライアントに対応するトークンを削除します。ローカルの認証情報を消す前に、以下の最初のコマンドを実行し、認証拒否と非ゼロの終了コードを確認します。成功した場合は失効を確認できていません。対象アカウントとトークンを調べてから結果を判断します。

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

`unregister` はローカルの `server` と `token` フィールドだけを削除し、サーバーのトークンを**失効しません**。一時ディレクトリの削除はローカルの後片付けであり、失効の代わりにはなりません。その後、専用シェルを閉じます。継続的な自動化では、秘密情報の保管、更新、失効、エラー処理、限定した認可操作を別途設計します。

## ソース

[xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [client storage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js), [token API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [token expiry](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [inventory API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [profile tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
