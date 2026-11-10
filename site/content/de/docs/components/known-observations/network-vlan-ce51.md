---
title: "Beobachtung zu VLAN im Netzwerk-Assistenten (ce51)"
translationKey: network-vlan-ce51
excludeSearch: true
weight: 90
---

## Geltungsbereich

Dies ist eine auf eine Veröffentlichung beschränkte, teilweise Beobachtung aus SN04 (Inventarzeile 14), durchgeführt am 2026-11-03 in der vollständigen Zelle n der Gruppe A. Der verschachtelte XCP-HL-8.3.0-Host (Build ce55) betrieb eine per RPM installierte XOA-HL-Appliance `xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64` (Tag `v5.113.2_e281c536-ce51`, XO-Server 5.193.1, AlmaLinux 9.8). Es war nicht das veröffentlichte XVA-Image. Über andere Veröffentlichungen oder Installationswege, einschließlich des ce52-XVA, wird nichts behauptet.

## Beobachtet

Bei New network wurde mit eingegebener VLAN 392 und leerem Feld Interface ein Netzwerk ohne PIF und ohne VLAN-Objekt erstellt, ohne Fehler oder Warnung. Der Platzhalter im VLAN-Feld lautete „No VLAN if empty“, während das Kapitel sagte, ein leerer Wert werde als 0 gesendet. Nach Verwendung des Assistenten mit dem freien Uplink meldete der VLAN-PIF `carrier=false`, obwohl die Verbindung des Betriebssystems aktiv war und auf dem verschachtelten `eth1` 12 getaggte Frames zu sehen waren.

Das war nur ein Teilergebnis: Es gab kein zweites Pool-Mitglied, keine hostübergreifende Prüfung und keine Wiederherstellungsumgebung. Das Carrier-Ergebnis ist so festgehalten, wie es beobachtet wurde; seine Bedeutung ist hier nicht geklärt.

## Korrekturplan nach der Beta

Nach dem Beta-Launch sind das Assistentenformular, die Anfrageerstellung und der Backend-Pfad zur Netzwerk- und PIF-Erstellung zu untersuchen. Danach:

1. VLAN ohne Interface in der Oberfläche ungültig machen, mit einer klaren Validierungsmeldung; bestätigen, dass das Backend die entsprechende Anfrage ebenfalls ablehnt oder sicher behandelt.
2. Eine einzige Bedeutung für ein leeres VLAN festlegen und dokumentieren und dann Platzhalter, Kapitel, Anfragewert und Backend-Verhalten angleichen.
3. Den Carrier-Wert des VLAN-PIF mit dem Link-Status des Hosts und der Paketbeobachtung abgleichen. Ihn nur korrigieren, wenn sein Vertrag falsch ist; andernfalls dokumentieren, was das Flag bedeutet.
4. Automatisierte Tests für Validierung, leeres VLAN und Carrier-Semantik ergänzen.
5. Zuerst eine gezielte Abnahme auf einer entbehrlichen, aus der Beta abgeleiteten Appliance durchführen. Erst nach Prüfung dieser Ergebnisse einen ce52-Kandidaten über den unterstützten XO-Lite-XVA-Weg testen. XVA-Identität, Host/Build, Schritte und Ergebnisse festhalten, bevor eine Aussage zu ce52 getroffen wird.

Ordnen Sie dieses ce51-RPM-Ergebnis auf dem verschachtelten Host nicht dem ce52-XVA zu, ohne diesen separaten Test.
