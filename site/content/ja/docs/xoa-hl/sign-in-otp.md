---
title: "ワンタイムコードでサインインを保護する"
linkTitle: "ワンタイムコード"
description: "アカウントのサインインにワンタイムコードを追加し、確認して、安全に解除します。"
weight: 71
translationKey: xoa-manual-sign-in-otp
translationStatus: draft
sourceRevision: sha256:72dc5fd66f02cd884355420cda47e1e51abcd4c36b907da89baa617947b24429
glossaryTerms: ["appliance"]
---

XOA-HL では、パスワードの後に、認証アプリが生成する 6 桁のワンタイムコードを求めることができます。コードは時間とともに変わります（TOTP）。ローカルのパスワードでサインインする各アカウントが、自分で有効にします。まず、[このテスト用に作成した](/docs/xoa-hl/permissions/)管理者以外のアカウントで試してください。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce40`（Xen Orchestra 5.113.2）。公開済みのコードに基づく手順で、検証環境でのテストはまだです。今後のリリースでは動作が変わる場合があります。
{{< /callout >}}

## 始める前に {#prepare}

| 必要なもの | 理由 |
| --- | --- |
| 自分で管理する端末上の TOTP 認証アプリ | 共有シークレットからコードを生成します |
| アプライアンスとその端末の正しい時刻 | XO は現在のコードと、その前後 30 秒のステップのコードを受け付けます |
| 2 人目の管理者、または別の復旧手段 | ない場合、端末をなくすと唯一の管理者がログインできなくなります |
| テストの間、開いたままにしておくブラウザーのセッション | 確認に失敗したときに、ワンタイムコードを解除できます |

設定中に入力したコードは、ブラウザーが自分の時計で確認します。サインイン時には、アプライアンスが自分の時計でコードを確認します。そのため、設定中にコードが受け付けられても、アプライアンスの時刻が正しいとは限りません。

## 自分のアカウントでワンタイムコードを有効にする {#enable-otp}

1. 保護するアカウントでサインインします。メニューのユーザーアイコンからユーザーページ（`/#/user`）を開きます。
2. **OTP認証設定** のスイッチを探してオンにします。**ワンタイムパスワード(OTP)認証を追加します** のダイアログに、QR コードとテキストのシークレットが表示されます。
3. 認証アプリで QR コードを読み取るか、シークレットを入力します。新しい項目の発行者は `Xen Orchestra` で、アカウントのメールアドレスまたはログイン名が付きます。
4. 現在のコードを **OTP code** に入力して確定します。コードが間違っているとダイアログが再び開くので、そのときアプリに表示されているコードを入力します。**キャンセル** を選ぶと、ワンタイムコードはオフのままです。

スイッチが表示されない場合は、作業を止めてインストール済みのバージョンを控えます。このビルドは XO の既定のオープンソースプランを使っており、スイッチが表示されるため、サブスクリプションがないことは原因ではありません。[相違を報告](/docs/xoa-hl/troubleshooting/)してください。

**確認:** スイッチがオンになり、ユーザーページのスイッチの横にシークレットと QR コードが表示されています。これを見た人は有効なコードを生成できます。このページを共有したり、画面を撮影したりしないでください。この QR コードは、同じシークレットに対して発行者 `XenOrchestra`（スペースなし）を表示します。認証アプリにある既存の項目をそのまま使い、もう一度読み取らないでください。

## 新しいセッションでサインインを確認する {#check-sign-in}

1. 現在のセッションは開いたままにします。プライベートウィンドウを開き、ユーザー名とパスワードでサインインします。
2. 2 ページ目で **Code** を求められます。アプリに表示されている現在のコードを入力し、**Sign in** を選びます。
3. コードが間違っているか期限切れの場合は `Invalid code` と表示されます。次のコードを待って、もう一度試します。
4. 正しいアカウントでサインインしたことを確認し、プライベートウィンドウを閉じます。

**確認:** サインインでコードを求められ、正しいコードが受け付けられました。何度も失敗する場合は、開いたままのセッションで[ワンタイムコードを解除](#remove-otp)し、両方の時計を確認してから、もう一度有効にします。

## ワンタイムコードで保護されないもの {#otp-limits}

- 有効にしても、既存のセッションは終了せず、トークンも失効しません。有効な認証トークンは、後から作成したものも含めて、すべてコードの確認を省略します。トークンは別の認証情報です。有効にした後、ユーザーページの **Authentication tokens** を開き、心当たりのないトークンや不要になったトークンを削除します。削除したトークンを使うスクリプトは動かなくなります。
- 保護されるのは、このアカウントの XO への Web サインインだけです。アプライアンスへの SSH やコンソールのアクセス、ホストの XO Lite や root アカウント、他の XO アカウントは保護されません。
- 外部のサインインプロバイダーとその多要素認証は、ここでは扱いません。

## ワンタイムコードを解除する {#remove-otp}

- **自分のアカウント：** ユーザーページで **OTP認証設定** をオフにし、**OTP認証を無効化** を確定します。
- **管理者として別のアカウント：** **設定 → ユーザー一覧** を開きます。**OTP** 列で、そのアカウントの **除去** を選んで確定します。先に、別の連絡手段などで依頼者を確認してください。その後、ユーザーは新しい端末を設定できます。

ワンタイムコードを設定していないアカウントは、この列に **未設定** と表示されます。唯一の管理者が端末をなくした場合、画面上で復旧する方法はありません。XO には、アカウントのパスワードを再設定し、ワンタイムコードを解除して管理者にする復旧コマンドがありますが、このアプライアンスではテストしていないため、ここでは手順として示しません。代わりに 2 人目の管理者を用意してください。

**確認:** スイッチがオフで、アカウントの OTP 列に **未設定** と表示されています。新しいプライベートウィンドウで、そのアカウントがローカルのユーザー名とパスワードだけで、コードなしでサインインできます。これを確認するまで、復旧用の管理者はサインインしたままにします。

{{< details title="出典" closed="true" >}}
- **ユーザーページと設定**：[ユーザーページの OTP 欄](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js)、[ユーザーページとトークン](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js)、[設定ダイアログ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js)、[有効化と解除の操作](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js)、[ユーザー一覧の OTP 列](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js)。
- **サインインとトークン**：[サインインページ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs)、[サインインフォーム](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug)、[認証とトークンによる省略](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs)、[TOTP の時間の許容範囲](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs)、[復旧コマンド](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs)、[画面のラベル](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js)。
- **ビルドとブラウザーでの設定**：[XO の既定プラン](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js)、[ブラウザーの認証処理](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js)、[ユーザー設定の API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs)、[HomeLab のビルド](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh)。
{{< /details >}}
