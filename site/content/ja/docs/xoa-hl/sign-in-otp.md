---
title: ワンタイムコード (OTP) でサインインを保護する
description: XOA-HL アカウントで時間ベースのワンタイムコードを有効にし、サインインを確認して、安全に解除します。
weight: 27
translationKey: xoa-manual-sign-in-otp
translationStatus: draft
sourceRevision: sha256:d6ef3292175f1ff56be82e05d96ee210df45b47ee3cece2d19943c60ee24603c
glossaryTerms: ["appliance"]
---

XOA-HL では、パスワードの後に認証アプリが生成する 6 桁の時間ベースのワンタイムコード (TOTP) を要求できます。ローカルパスワードを使う各アカウントが自分で有効にします。まず、[このテスト用に作成した](/docs/xoa-hl/permissions/)管理者以外のアカウントで試してください。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 を対象としたソース確認済みのプレビューです。このアプライアンスでの OTP の登録、サインイン、解除のテストは未完了です。後のリリースでは動作が異なる場合があります。
{{< /callout >}}

## 1. 準備する

| 必要なもの | 理由 |
| --- | --- |
| 自分で管理する端末上の TOTP 認証アプリ | 共有シークレットからコードを生成する |
| アプライアンスとその端末の正しい時刻 | XO は現在のコードと、その前後 30 秒のステップのコードを受け付ける |
| 2 人目の管理者、または独立した復旧手段 | ない場合、端末を紛失すると唯一の管理者がログインできなくなる |
| テスト中に開いたままにするブラウザーのセッション | 確認に失敗したときに OTP を解除できる |

登録時の確認はブラウザー内で、ブラウザーの時計を使って行われます。サインインはアプライアンスが自身の時計で確認します。そのため、登録時にコードが受け付けられても、アプライアンスの時刻が正しいとは限りません。

## 2. 自分のアカウントで OTP を有効にする

1. 保護するアカウントでサインインします。メニューのユーザーアイコンからユーザーページ (`/#/user`) を開きます。
2. **OTP認証設定** のスイッチを探します。表示されない場合はテストを止め、インストール済みバージョンを記録してください。確認したビルドは XO の既定のオープンソースプランを使い、このスイッチを表示します。サブスクリプションが必要だと判断せず、[相違を報告](/docs/xoa-hl/troubleshooting/)してください。スイッチをオンにします。**ワンタイムパスワード(OTP)認証を追加します** のダイアログに、QR コードとテキストのシークレットが表示されます。
3. 認証アプリで QR コードを読み取るか、シークレットを入力します。登録時のエントリーの発行者は `Xen Orchestra` で、アカウントのメールアドレスまたはログイン名が付きます。
4. 現在のコードを **OTP code** に入力して確認します。この固定バージョンの日本語カタログでは、このラベルは英語です。コードが間違っているとダイアログが再び開くので、その時点でアプリに表示されているコードを入力します。**キャンセル**を選ぶと OTP は無効のままです。
5. 有効にした後も、ユーザーページのスイッチの横にシークレットと QR コードが表示され続けます。これを見た人は有効なコードを生成できるため、このページを共有したり画面を記録したりしないでください。この後の QR コードは同じシークレットに対して発行者 `XenOrchestra` (スペースなし) を使います。もう一度読み取らず、認証アプリの元のエントリーを使い続けてください。

## 3. 新しいセッションでサインインを確認する

1. 現在のセッションは開いたままにします。プライベートウィンドウを開き、ユーザー名とパスワードでサインインします。
2. 2 ページ目で **Code** を求められます。アプリの現在のコードを入力し、**Sign in** を選びます。このページは UI の言語設定にかかわらず英語です。
3. コードが間違っているか期限切れの場合は `Invalid code` と表示されます。次のコードを待って再試行します。
4. 想定したアカウントでサインインしたことを確認し、プライベートウィンドウを閉じます。

確認が何度も失敗する場合は、開いたままのセッションで OTP を解除し (セクション 5)、両方の時計を確認してから登録し直してください。

## 4. OTP で保護されない範囲を理解する

- OTP を有効にしても、既存のセッションやトークンは失効しません。有効な認証トークンはすべて OTP の確認を省略します。登録後に作成したトークンも同様で、独立した認証情報として扱ってください。OTP を有効にした後、ユーザーページの **Authentication tokens** を開き、心当たりのないトークンや不要になったトークンを削除してください。削除したトークンを使うスクリプトは動作しなくなります。
- OTP が保護するのは、このアカウントの XO への Web サインインです。アプライアンスの SSH・コンソールのアクセス、ホストの XO Lite や root アカウント、他の XO アカウントは保護しません。
- 外部の認証プロバイダーとその MFA は、このガイドの対象外です。

## 5. OTP を解除する

- **自分のアカウント：** ユーザーページで **OTP認証設定** をオフにし、**OTP認証を無効化** を確認します。
- **管理者として別のアカウント：** **設定** > **ユーザー一覧** を開きます。**OTP** 列で対象アカウントの **除去** を選び、確認します。先に、別の連絡手段などで依頼者の本人確認をしてください。その後、ユーザーは新しい端末を登録できます。

OTP を設定していないアカウントは、この列に **未設定** と表示されます。唯一の管理者が端末を紛失した場合、画面上で復旧する方法はありません。ソースには、アカウントのパスワードを再設定し、OTP を解除して管理者にする復旧コマンドがあります。このアプライアンスでは検証されていないため、このガイドでは手順として提供しません。代わりに 2 人目の管理者を用意してください。解除後は OTP スイッチがオフで、対象アカウントの OTP 列が **未設定** になっていることを確認します。新しいプライベートセッションで、ローカルのユーザー名とパスワードだけで OTP を求められずにログインできることを確認してください。確認が終わるまで復旧用の管理者のセッションを保持します。

## ソース

XO 5 の固定コミット `e281c536` に、公開済みの HomeLab パッチを適用したもの：[ユーザーページの OTP 欄](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js)、[ユーザーページとトークン](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js)、[登録ダイアログ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js)、[有効化と解除](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js)、[ユーザー一覧の OTP 列](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js)、[サインインページ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs)、[サインインフォーム](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug)、[認証とトークンによる省略](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs)、[TOTP の許容範囲](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs)、[復旧コマンド](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs)、[英語のラベル](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js)。

ビルドでの表示条件とブラウザーでの登録： [XO default plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [browser authenticator](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js), [user preferences API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs), [HomeLab build](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh).
