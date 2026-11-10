---
title: "ネットワークウィザードの VLAN 観察（ce51）"
translationKey: network-vlan-ce51
excludeSearch: true
weight: 90
---

## 対象範囲

これは SN04（インベントリ行 14）での、リリースを限定した部分的な観察
です。2026-11-03 に Group A full cell で実施しました。ネストされた
XCP-HL 8.3.0 build ce55 ホスト上で、RPM インストールされた XOA-HL は
`xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64`（tag
`v5.113.2_e281c536-ce51`、XO server 5.193.1、AlmaLinux 9.8）でした。
公開済み XVA イメージではありません。他のリリースやインストール経路、
特に ce52 XVA についての主張ではありません。

## 観察内容

New network で Interface を空のまま VLAN 392 を入力すると、エラーや警告
なしに、PIF も VLAN オブジェクトもないネットワークが作成されました。
VLAN のプレースホルダーは「No VLAN if empty」でしたが、章の説明では空値
が 0 として送信されるとされています。予備 uplink を使ってウィザードを
正しく実行した後、VLAN PIF は `carrier=false` を示しました。一方、OS の
リンクは up で、ネストされた `eth1` ではタグ付きフレームが 12 個観測され
ました。

これは部分的な合格です。2 台目の pool member、ホスト間確認、復旧用 fixture
はありませんでした。carrier の意味はここでは確定していません。

## ベータ公開後の修正計画

ベータ公開後、フォーム、リクエスト生成、backend の network/PIF 作成経路を
調査します。

1. Interface のない VLAN を UI で無効として明確な説明を出し、同等の
   リクエストを backend も拒否するか安全に処理することを確認します。
2. VLAN が空の場合の意味を決め、プレースホルダー、章、送信値、backend
   動作を一致させます。
3. VLAN PIF の carrier 値をホストのリンク状態とパケット観測に照らして追跡
   します。契約が誤っている場合のみ修正し、それ以外は意味を文書化します。
4. 入力検証、空 VLAN、carrier の意味を対象とする自動テストを追加します。
5. まず使い捨ての beta 派生 appliance で対象を絞った受け入れ確認をします。
   証拠をレビューした後に限り、サポート対象の XO Lite XVA 経路で ce52
   candidate を試験します。ce52 について結論を出す前に、XVA の識別情報、
   host/build、手順、結果を記録します。

この別個の試験なしに、ce51 RPM/ネストホストでの結果を ce52 XVA に当てはめ
ないでください。
