---
title: XCP-hl
layout: hextra-home
translationKey: home
---

{{< hextra/hero-badge link="https://github.com/Vagrantin/xcp-ng-ce-iso/releases/latest" >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>{{< latest-iso-badge label="アルファ版" >}}</span>
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  ハイパーバイザーを解放する
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  アップストリームの XCP-ng 8.3 をベースにした ISO で、&nbsp;<br class="hx:sm:block hx:hidden" />
  お好みの Xen Orchestra を展開します。<br><br>
  仮想マシンの管理がこれまでになく簡単になりました。XCP-hl ホストと XOA-hl VM のアップデートも、標準で自動的に行われます。
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
    title="すっきりしたメニュー"
    subtitle="XOA-hl はバナーとライセンスが必要なメニュー項目を取り除いた、シンプルな Xen Orchestra です。"
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
    subtitle="XOLite-hl と XOA-hl は、動作確認済みのアップストリームのリビジョンに固定されています。新しいバージョンへの切り替えは十分なテストを経てから行われるため、アップストリームの変動でホストが壊れることはありません。"
  >}}
{{< /hextra/feature-grid >}}
