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
  すべての人に仮想化を
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  XCP-hl は XCP-ng 8.3 をホームラボ向けに提供します。Xen Orchestra の配布イメージを選べるほか、ホストとアプライアンスの更新を管理する機能を備えています。
{{< /hextra/hero-subtitle >}}
</div>

<div class="hero-actions hx:mb-6">
{{< latest-iso-download text="ISO をダウンロード" shaText="SHA256 チェックサム" >}}
{{< hextra/hero-button text="ドキュメントを読む" link="docs" style="background: transparent; border: 1px solid rgba(125,125,125,.4); color: inherit;" >}}
</div>

{{< callout type="warning" >}}
**XCP-hl はアルファ版のソフトウェアです。** 現在も活発に開発中で、安定化の
ための工程をまだ通っていません。**リリースのたびに互換性のない変更が入ると考えてください。**
{{< /callout >}}

<div class="hx:mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="XCP-ng 8.3 ベース"
    subtitle="Xen 4.17、XAPI、Open vSwitch を基盤に、アップストリームのホスト管理・VM 管理機能を提供します。"
  >}}
  {{< hextra/feature-card
    title="XO を自由に選択"
    subtitle="XO Lite から hl イメージ（管理 Web UI の XOA-hl）、Vates 公式アプライアンス、Ronivay 版、または独自のイメージを展開できます。"
  >}}
  {{< hextra/feature-card
    title="すっきりしたメニュー"
    subtitle="XOA-hl はメニューを整理し、XCP-hl の更新管理を統合した Xen Orchestra です。"
  >}}
  {{< hextra/feature-card
    title="すぐ使える ISO ライブラリー"
    subtitle="100 GB 以上の適切なディスクへの新規インストール時に、20 GB の ISO ライブラリーを確保し、初回起動時に登録します。"
  >}}
  {{< hextra/feature-card
    title="署名済み、その場でアップデート"
    subtitle="すべての ISO と RPM は XCP-hl の GPG 鍵で署名されており、稼働中のホストはプロジェクトの yum リポジトリからアップデートを取得します。"
  >}}
  {{< hextra/feature-card
    title="最新を追わず、固定"
    subtitle="XO Lite と XOA-hl は特定のアップストリームのリビジョンに固定されています。変更は明示的に行い、各ビルドに含まれるバージョンはリリース一覧表で確認できます。"
  >}}
{{< /hextra/feature-grid >}}

{{< legacy-home >}}
