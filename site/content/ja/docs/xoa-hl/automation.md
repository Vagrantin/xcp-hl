---
title: "xo-cli による自動化"
linkTitle: "自動化 (xo-cli)"
description: "有効期間の短いトークンを使って xo-cli でインベントリを読み取り、その後トークンを失効させます。"
weight: 92
translationKey: xoa-manual-automation
translationStatus: draft
sourceRevision: sha256:8ca25fc0552174edc36e7bc5cb4328012f391a79fd91e6a3584debc5deffbb99
glossaryTerms: ["appliance", "host", "vm"]
---

アプライアンスに同梱のコマンドラインクライアント xo-cli を使い、有効期間の短いトークンで小さなインベントリを読み取ってから、トークンを失効させます。VM を変更する自動化を作る前に、このテストを行います。コマンドは **XOA-HL アプライアンス**内のシェルで実行し、トークンの失効は同じテストユーザーでログインしたブラウザーで行います。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce47`（Xen Orchestra 5.113.2）、`xo-cli` **0.32.2** と `xo-lib` **0.11.1**。2026-10-27 に検証用アプライアンスでテスト済みです。
{{< /callout >}}

## 1. シェルと TLS の信頼を準備する {#prepare}

**始める前に**

- [アプライアンスの保守](/docs/xoa-hl/maintenance/)の説明に従い、インストール済みのリリースを確認します。
- 一般ユーザーのテスト用アカウントと、失っても困らないテスト用 VM を用意します。このユーザーに許可されている操作は、[ユーザーと権限](/docs/xoa-hl/permissions/)に従って別にテストします。
- 証明書と一致するアプライアンスの DNS 名を使います。インストール時に作成された自己署名証明書 `xoa.local` では、先に検証環境の DNS や証明書の準備が必要な場合があります。
- アプライアンスの公開 CA または証明書を、信頼できる経路で PEM ファイルとして入手します。そのフィンガープリントを別の方法で確認します。

1. **アプライアンス内**で、専用の新しい Bash セッションを開きます。そこで同梱の `/usr/local/bin/xo-cli` を使います。
2. 次のセクションの例で、PEM ファイルのパス、URL、メールアドレスを自分のものに置き換えます。

`NODE_EXTRA_CA_CERTS` は証明書を信頼の一覧に追加しますが、ホスト名は引き続き検証されます。TLS の検証に失敗した場合は、名前か証明書を直します。`--allowUnauthorized` や `NODE_TLS_REJECT_UNAUTHORIZED=0` で回避しないでください。

## 2. 有効期間の短いトークンを登録する {#register-token}

次のコマンドは、認証情報を新しい一時フォルダーに保存するため、既存の xo-cli の設定には影響しません。`umask 077` により、新しいファイルは自分だけが読めるようになります。

- `register` はパスワードを尋ねます。パスワードを引数に追加しないでください。URL にトークンを含めないでください。
- アカウントでワンタイムコード（OTP）を使う場合は、URL の前に、有効なコードで `--otp CODE` を追加します。

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

このトークンは、意図して `1 hour` を要求しています。サーバーの既定では、トークンの有効期間は 30 日で、最大は半年です。サーバーの設定で、これらの上限は変わることがあります。上限を超える期間を要求すると、登録は一般的なエラー（`unknown error from the peer`）で失敗します。短い期間を指定してください。

トークンはそのユーザーのすべての権限を持ち、読み取りだけに限定されません。設定フォルダーはパスワードと同じように扱います。シェルのトレース、問題報告に添付するバックアップ、バージョン管理に含めないでください。登録でログイン用のトークンが作成されます。この後のコマンドは、データを読み取るだけです。

## 3. インベントリを検出して読み取る {#read-inventory}

次のコマンドを実行します。`--json` や `--id` などのフラグは、引数の前に置きます。

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| コマンド | 得られる結果 |
| --- | --- |
| `list-commands xo.getAllObjects` | メソッドの引数を読みやすい形で表示します。メソッドが表示されても、使う権限があるとは限りません |
| `system.getServerVersion --json` | サーバーパッケージのバージョンです。このリリースでは `"5.193.1"` です。XO のバージョン（5.113.2）ではありません |
| `list-objects --id --name_label --power_state type=VM` | 指定したプロパティだけを含む JSON 配列です。VM の状態は変わりません |
| `xo.getAllObjects --json …` | オブジェクト ID をキーとする JSON オブジェクトです。オブジェクトの種類で絞り込み、1 件に制限しています |

`json:` を付けると、型を持つ値を送ります。`limit=json:1` は数値を、`limit=1` は文字列を送ります。最後のコマンドは、**`/api/` への WebSocket** で次の JSON-RPC 要求を送ります（HTTP POST ではありません）。

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

このリリースでは、ログインしたアカウントであれば、権限がまったくなくても、API からインベントリ全体を読めます。フィルターや選んだ項目は、表示する内容を選ぶだけで、**アクセスを制限するものではありません**。API がユーザーの管理画面に表示されるオブジェクトだけを返すとは考えないでください。出力から外した項目が取得されていないとも考えないでください。結果は非公開で扱い、アカウントが実際に見られる範囲は別に確認します。名前は固定の ID ではありません。件数を制限したこの結果は完全なインベントリではなく、VM を確実に選ぶ方法でもありません。

## 4. トークンを失効させて後片付けをする {#revoke-token}

1. 同じテストユーザーでログインした別のブラウザーセッションで、メニューの **ユーザーアイコン** を選び、**ユーザー**（`/#/user`）を開きます。
2. **Authentication tokens** で、この CLI クライアントのトークンを削除します。
3. シェルに戻り、ローカルで何かを削除する前に、下の最初のコマンドを実行します。認証エラーと 0 以外の終了コードで失敗するはずです。
4. 成功した場合、トークンは失効していません。作業を止め、失効できたと判断する前に、アカウントとそのトークンを確認します。
5. 残りのコマンドを実行してローカルの認証情報を削除し、専用のシェルを閉じます。

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

**確認:** ブラウザーでトークンを削除した後、バージョンのコマンドが認証エラーで失敗します。

`unregister` はローカルの `server` と `token` の項目を削除するだけで、サーバー上のトークンは**失効させません**。一時フォルダーの削除はローカルの後片付けにすぎず、失効の代わりにはなりません。継続して使う自動化には、秘密情報の保管、更新、失効、エラー処理、必要最小限の権限について、別の設計が必要です。これらはここでは扱いません。

{{< details title="出典" closed="true" >}}
- **コマンドラインクライアント**：[xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs)、[クライアントの設定の保存先](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs)、[xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js)。
- **トークンとインベントリ**：[トークンの API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs)、[トークンの有効期限](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs)、[インベントリの API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs)、[ユーザーページのトークン](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js)。
{{< /details >}}
## 変更する CLI/JSON-RPC の演習 (RF01) {#mutating-example}

対象は XO 5.113.2 `e281c536`、XOA-HL ce47、同梱 xo-cli 0.32.2 です。先に上記の信頼済み TLS 登録を終えます。**停止した使い捨て VM** の正確な UUID と説明を記録し、通常ユーザーに **その VM のみの Admin** を付与します。独立管理者を保持し、名前や `limit=1` で変更先を決めません。

1. 全 `VM_UUID` を記録した UUID に置き換えます。ブラウザーで UUID、停止状態、元の説明を確認します。`vm.set` の定義と対象を先に読みます。
2. 説明のみ変更し、ブラウザーと新規一覧要求で確認します。`vm.set` は `id` を使います。他メソッドのパラメーター名から推測しません。

```bash
xoa_cli list-commands vm.set
xoa_cli xo.getAllObjects --json 'filter=json:{"id":"VM_UUID"}'
xoa_cli vm.set --json id=VM_UUID name_description=rf01-disposable-test
xoa_cli xo.getAllObjects --json 'filter=json:{"id":"VM_UUID"}'
```

認証済み `/api/` WebSocket の変更要求は次です。

```json
{"jsonrpc":"2.0","id":2,"method":"vm.set","params":{"id":"VM_UUID","name_description":"rf01-disposable-test"}}
```

3. 記録した元の説明に `vm.set` で戻し、`name_description=...` 引数を引用符で囲みます。独立に読み直し、電源、ディスク、VIF が変わらないことを確認します。
4. 管理者が試験 ACL のみ削除し、他の権限がないことを確認します。同じ要求を繰り返し、CLI 非ゼロ終了と説明不変を確認します。RPC 成功が空応答でも読み直しは必須です。
5. 上記手順でトークンを失効し一時設定を削除します。時間切れ、切断、エラー後は書き込み済みの可能性があるため、読み直してから再試行します。破壊的操作を無条件で繰り返しません。

**確認：** 許可された説明変更/復元が観察でき、権限削除後の同じ要求は VM を変えず拒否されること。1 件の変更契約の確認で、汎用自動化や一覧の秘匿性の保証ではありません。試験済みとするには実機の証拠が必要です。

固定ソース: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [packages/xo-cli/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [packages/xo-server/src/xo-mixins/acls.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs).

**ラボ結果、2026-11-03(CLI は合格、失効は未完了):** ラボのアプライアンスで、xo-cli 0.32.2 が使い捨ての停止状態 VM の説明を変更し、読み戻しは一致し、元の文字列を復元できました。ユーザーの管理者権限を外した後は、同じリクエストが失敗し(`not enough permissions`、終了コード 1)、ホスト側の独立した読み戻しは変わりませんでした。確認した前提条件: ラボの証明書(`CN=xoa.local`、SAN なし)には `xoa.local` の名前対応とピン留めした CA が必要でした(TLS の回避はしていません)。`register` は端末でパスワードを求め、端末がないと失敗する(`tty.setRawMode is not a function`)ため、テストでは `--token` を使いました。権限のないアカウントが呼んだ `token.delete` は拒否されたため、ブラウザでの失効は確認しておらず、この行は未完了のままです。
