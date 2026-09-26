---
title: ロードマップ
weight: 3
translationKey: roadmap
aliases: ["/ja/roadmap.html"]
---

XCP-hl の今後の方向性を、GitHub の未解決の issue からそのまま一覧にしたものです。各行はその issue にリンクしており、詳細や議論はそちらにあります。
{class="lead"}

{{< callout type="info" >}}
優先度は各 issue の P1 / P2 / P3 のラベルに従い、意見やアップストリームの変更によって変わることがあります。issue のタイトルは GitHub に書かれたとおりに表示しています。項目の提案や後押しは、[GitHub](https://github.com/Vagrantin/xcp-hl/issues) で issue を作るか、コメントしてください。
{{< /callout >}}

## 次に取り組むもの（P1）

- XOA-hl update is breaking the follow up ([#103](https://github.com/Vagrantin/xcp-hl/issues/103)) · `xoa-hl`
- Jenkins CI step 7: ISO install smoke test in Dev ([#74](https://github.com/Vagrantin/xcp-hl/issues/74)) · `QA`
- Jenkins CI step 4: wire Jenkins to the vault, Dev/Test/Prod roles ([#71](https://github.com/Vagrantin/xcp-hl/issues/71)) · `buildorchestration`
- Jenkins CI step 3: choose and stand up the secret store ([#70](https://github.com/Vagrantin/xcp-hl/issues/70)) · `buildorchestration`
- Jenkins CI step 2: dedicated infra repo (JCasC, plugins, agent image) ([#69](https://github.com/Vagrantin/xcp-hl/issues/69)) · `buildorchestration`
- Local Jenkins CI to replace the orchestrator ([#57](https://github.com/Vagrantin/xcp-hl/issues/57)) · `buildorchestration`
- Review and standardize the patching model ([#43](https://github.com/Vagrantin/xcp-hl/issues/43)) · `xoa-hl`, `xolite-ce`, `xoa-deploy-patcher`
- Does yum update import the signature automatically. ([#35](https://github.com/Vagrantin/xcp-hl/issues/35)) · `xcp-hl`, `xcp-ng-ce-iso`
- Clean up old rpm on xolite that are broken. ([#25](https://github.com/Vagrantin/xcp-hl/issues/25)) · `xolite-ce`
- XOA HL patching refactore ([#16](https://github.com/Vagrantin/xcp-hl/issues/16)) · `xoa-deploy-patcher`

## 予定しているもの（P2）

- Update the XOA-hl UI to show that a reboot is required ([#102](https://github.com/Vagrantin/xcp-hl/issues/102)) · `xoa-hl`
- Goose step 2: choose the integration path into XOA-HL (goosed, ACP, or embedded) ([#83](https://github.com/Vagrantin/xcp-hl/issues/83)) · `xoa-hl`
- Goose step 1: headless goose with llama.cpp and mock MCP extensions ([#82](https://github.com/Vagrantin/xcp-hl/issues/82)) · `xoa-hl`
- Model bake-off for natural language VM creation: SLMs against up-to-8B models ([#81](https://github.com/Vagrantin/xcp-hl/issues/81)) · `xoa-hl`
- Jenkins CI step 9: absorb xoa-vm-agent into the Prod pipeline ([#76](https://github.com/Vagrantin/xcp-hl/issues/76)) · `buildorchestration`
- Jenkins CI step 8: promote the ISO smoke test to Test ([#75](https://github.com/Vagrantin/xcp-hl/issues/75)) · `QA`
- Jenkins CI step 6: decide the QA platform topology ([#73](https://github.com/Vagrantin/xcp-hl/issues/73)) · `QA`
- Jenkins CI step 5: prove the Dev loop and the promotion path ([#72](https://github.com/Vagrantin/xcp-hl/issues/72)) · `buildorchestration`
- XOA-HL automatic updates ([#45](https://github.com/Vagrantin/xcp-hl/issues/45)) · `xoa-hl`
- Revisit the unversioned `Obsoletes: xo-lite` workaround when the upstream pin moves ([#42](https://github.com/Vagrantin/xcp-hl/issues/42)) · `xolite-ce`, `xcp-ng-ce-iso`
- Update welcome message ([#27](https://github.com/Vagrantin/xcp-hl/issues/27)) · `xoa-hl`
- Add a description of each image after selection on the right side. ([#18](https://github.com/Vagrantin/xcp-hl/issues/18)) · `xolite-ce`
- Complete version matrix of all the bin and RPM ([#15](https://github.com/Vagrantin/xcp-hl/issues/15)) · `xcp-hl`
- Publish gpg public key with the iso ([#10](https://github.com/Vagrantin/xcp-hl/issues/10)) · `xcp-ng-ce-iso`
- Make the rpm build github workflows consistent ([#8](https://github.com/Vagrantin/xcp-hl/issues/8)) · `xoa-hl`, `xolite-ce`, `xcp-hl`, `xoa-proxy`

## その後（P3）

- Goose step 6: chat box in the XOA-HL UI wired to goose ([#87](https://github.com/Vagrantin/xcp-hl/issues/87)) · `xoa-hl`
- Goose step 5: the create_vm extension behind goose Approve mode ([#86](https://github.com/Vagrantin/xcp-hl/issues/86)) · `xoa-hl`
- Goose step 4: read-only platform chat through the XO MCP extension ([#85](https://github.com/Vagrantin/xcp-hl/issues/85)) · `xoa-hl`
- Goose step 3: package goose for the appliance, pinned and off by default ([#84](https://github.com/Vagrantin/xcp-hl/issues/84)) · `xoa-hl`
- Natural language VM creation in XOA-HL through a chat box ([#80](https://github.com/Vagrantin/xcp-hl/issues/80)) · `xoa-hl`
- Jenkins CI step 10: absorb iso-agent, retire the dashboard and API ([#77](https://github.com/Vagrantin/xcp-hl/issues/77)) · `buildorchestration`
- `xoa-image-*` release `created_at` is pinned to a static commit, not the actual build time ([#41](https://github.com/Vagrantin/xcp-hl/issues/41)) · `build-xoa-hl`
- Rename xo-lite-ce package ([#40](https://github.com/Vagrantin/xcp-hl/issues/40)) · `xolite-ce`, `xcp-hl`, `xcp-ng-ce-iso`
- Rename xoa-proxy package ([#39](https://github.com/Vagrantin/xcp-hl/issues/39)) · `xoa-hl`, `xcp-hl`, `xoa-proxy`
- Put in place the workflow to get changelog up to date and meaningfull ([#34](https://github.com/Vagrantin/xcp-hl/issues/34)) · `xoa-hl`, `build-xoa-hl`
- RPM LICENSE ([#32](https://github.com/Vagrantin/xcp-hl/issues/32)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Switch "deploy XOA" button on success ([#31](https://github.com/Vagrantin/xcp-hl/issues/31)) · `xolite-ce`
- Need to know which version i'm running ([#30](https://github.com/Vagrantin/xcp-hl/issues/30)) · `xoa-hl`
- Change log in github releases ([#24](https://github.com/Vagrantin/xcp-hl/issues/24)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl`, `xoa-proxy`
- Xoa-hl release is messy ([#23](https://github.com/Vagrantin/xcp-hl/issues/23)) · `build-xoa-hl`
- Improve the documentation UI ([#19](https://github.com/Vagrantin/xcp-hl/issues/19)) · `xcp-hl`
- Container out of the box ([#7](https://github.com/Vagrantin/xcp-hl/issues/7)) · `xoa-hl`

## まだ優先度が決まっていないもの

- Improve the memory footprint ([#64](https://github.com/Vagrantin/xcp-hl/issues/64)) · `xoa-proxy`
- Reduce the number of crate it's uisng ([#63](https://github.com/Vagrantin/xcp-hl/issues/63)) · `xoa-proxy`
- Logrotate is UTC ([#62](https://github.com/Vagrantin/xcp-hl/issues/62)) · `xoa-proxy`
- Refactoring doc ([#60](https://github.com/Vagrantin/xcp-hl/issues/60)) · `xcp-hl`
- Investigate forking ([#54](https://github.com/Vagrantin/xcp-hl/issues/54)) · `xoa-hl`, `xolite-ce`, `xcp-hl`
- Identify backend/frontend code ([#53](https://github.com/Vagrantin/xcp-hl/issues/53)) · `xoa-hl`, `xolite-ce`, `build-xoa-hl-vm`, `build-xoa-hl`, `xoa-deploy-patcher`
- XOA-hl-vm build triggers even if XOA-HL build is in progress ([#48](https://github.com/Vagrantin/xcp-hl/issues/48)) · `build-xoa-hl-vm`, `build-xoa-hl`

## まだ issue になっていないもの

検討中で、まだ issue になっていないアイデアです。

### GPG 鍵：モジュールごとに 1 つの署名鍵 {#gpg-鍵-モジュールごとに-1-つの署名鍵}

[xcp-hl#3](https://github.com/Vagrantin/xcp-hl/issues/3) で決めた統一的な
GPG の構成は実装済みです。オフラインのマスターキーと 2 つの署名用サブキー
（RPM 用と ISO 用）を用意し、公開鍵を keys.openpgp.org で公開しています。
[GPG 署名](/docs/components/#gpg-signing)を参照してください。残っている改善点は、
共通になっている RPM 用サブキーを分けて、モジュールごとに専用の鍵を持たせる
ことです（`xo-lite-ce` の RPM 用、`xoa-proxy` の RPM 用、ISO 用）。

### アップストリームのバージョンの自動追跡 {#アップストリームのバージョンの自動追跡}

Rust 製のデーモン
[`buildorchestration`](https://github.com/Vagrantin/buildorchestration)
は、すでに毎日のタイマーですべてのコンポーネントのビルドを実行・監視し、
最新の GitHub リリースがすでに最新のコンポーネントは飛ばし、失敗した CI の
ログをローカルの LLM（Ollama）で診断します。残っているのは、XCP-ng 8.x の
新しいポイントリリースや XO Lite のバージョン更新を検出し、固定している
バージョン（たとえば `xolite-ce` の `UPSTREAM_TAG`）を更新するプルリクエストを
自動で作ることです。

### answerfile.xml による自動インストールへの対応

完全に無人での HL の展開（PXE ブートやスクリプトによる構築）に使える
`answerfile.xml` の例を用意します。これには応答ファイルを `install.img`
（SquashFS）の中に入れる必要がありますが、現在のビルドのパイプラインは
すでにそれに対応しています。

## 完了した項目

| 項目 | 公開時期 |
|---|---|
| 既定の ISO ストレージ：インストール時に 20 GB のパーティションを確保し、初回起動時に ISO SR として登録（[#2](https://github.com/Vagrantin/xcp-hl/issues/2)、[#46](https://github.com/Vagrantin/xcp-hl/issues/46)） | 2026 年 9 月 |
| XOA-hl 版：ライセンスが必要なメニューとサポートなしのバナーを削除し、ソースからイメージをビルドして XO Lite の展開先として選べるように（[#1](https://github.com/Vagrantin/xcp-hl/issues/1)、[#6](https://github.com/Vagrantin/xcp-hl/issues/6)） | 2026 年 7 月 |
| RPM と ISO のリリースのバージョン付けとリリースノートを自動化（[#4](https://github.com/Vagrantin/xcp-hl/issues/4)） | 2026 年 7 月 |
| GitHub Pages の CI により、push のたびにドキュメントサイトを自動公開（[#5](https://github.com/Vagrantin/xcp-hl/issues/5)） | 2026 年 6 月 |
| GPG 署名の構成：オフラインのマスターキーと RPM/ISO 用サブキー、公開鍵を keys.openpgp.org に登録（[#3](https://github.com/Vagrantin/xcp-hl/issues/3)） | 2026 年 5 月 |
| 手を入れた XOA-hl アプライアンスの最初のビルド（`xoa-hl` + `build-xoa-hl`） | 2026 年 7 月 |
| 毎日のビルドを統括するデーモン（`buildorchestration`） | 2026 年 7 月 |
| アップストリームの xo-lite のバージョン固定（`UPSTREAM_TAG`） | 2026 年 7 月 |
| XO Lite への最初のパッチ（コミュニティ版の展開先） | v8.3-ce 2026 年 4 月 |
| Rust 製のストリーミングサーバー `xoa-proxy` | v8.3-ce 2026 年 4 月 |
| 2 つのリポジトリによる GPG 署名付き RPM + ISO のビルドのパイプライン | v8.3-ce 2026 年 4 月 |
| GitHub Actions の CI/CD | v8.3-ce 2026 年 4 月 |
| XO Lite の展開画面で資格情報欄を読み取り専用に | v8.3-ce 2026 年 4 月 |
