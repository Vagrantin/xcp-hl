---
title: XCP-hl
layout: hextra-home
translationKey: home
---

{{< hextra/hero-badge link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>アルファ版 · v8.3-ce9</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  ハイパーバイザーを解放する
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  アップストリームの XCP-ng 8.3 をベースにコミュニティが作った ISO で、&nbsp;<br class="hx:sm:block hx:hidden" />
  セルフホストの Xen Orchestra アプライアンスを展開します。
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-button text="ISO をダウンロード" link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
{{< hextra/hero-button text="ドキュメントを読む" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl はアルファ版のソフトウェアです。** 現在も活発に開発中で、安定化の
ための工程をまだ通っていません。**リリースのたびに互換性のない変更が入ると考えてください。**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="そのまま置き換わる XCP-ng 8.3"
    subtitle="アップストリームの機能をすべて搭載 — Xen 4.17、XAPI、Open vSwitch、ライブマイグレーション、HA、vGPU。"
  >}}
  {{< hextra/feature-card
    title="XOA を選べる"
    subtitle="ホームラボ向けイメージ、Vates 公式アプライアンス、Ronivay 氏のビルド、あるいは独自のイメージを、XO Lite のセレクターから選んで展開できます。"
  >}}
  {{< hextra/feature-card
    title="サブスクリプションのバナーなし"
    subtitle="XOA-hl はバナーとライセンス関連のメニュー項目を取り除き、Xen Orchestra を完全に使える状態にします。"
  >}}
  {{< hextra/feature-card
    title="すぐ使える ISO ライブラリー"
    subtitle="インストール時に 20 GB のパーティションを確保し、初回起動時に ISO SR として登録します。コマンドラインを使わずにイメージをアップロードして VM を作成できます。"
  >}}
  {{< hextra/feature-card
    title="署名済み、その場でアップデート"
    subtitle="すべての ISO と RPM は XCP-hl の GPG 鍵で署名されており、稼働中のホストはプロジェクトの yum リポジトリからアップデートを取得します。"
  >}}
  {{< hextra/feature-card
    title="最新を追わず、固定"
    subtitle="XO Lite と Xen Orchestra は、動作確認済みのアップストリームのリビジョンに固定されています。固定バージョンはテストのうえで意図的にしか動かさないため、アップストリームの変動でホストが壊れることはありません。"
  >}}
{{< /hextra/feature-grid >}}
