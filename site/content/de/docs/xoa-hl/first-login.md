---
title: "Anmelden, einen Host verbinden und eine Sprache wählen"
linkTitle: "Erste Anmeldung"
description: "Bei XOA-HL anmelden, das Passwort festlegen, die Oberflächensprache wählen und den Host verbinden."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: draft
sourceRevision: sha256:90b1070b91657a68c53df68d8927605d523fbc946c6b8cf0e3a2fa30a113e037
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

Nach dieser Anleitung können Sie sich bei XOA-HL anmelden, Ihr Host ist verbunden und die Oberfläche verwendet Ihre Sprache.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; ein vollständiger Durchlauf auf einer Test-Appliance steht noch aus. Ältere Images und spätere Updates können abweichen.
{{< /callout >}}

## Vor dem Beginn {#before-you-begin}

- [Stellen Sie XOA-HL über XO Lite bereit](/docs/start/#start-deploy-xoa). Notieren Sie Image-Tag und Appliance-Adresse.
- Bewahren Sie Benutzername und Passwort des XO-Administrators aus dem Bereitstellungsformular auf. Sie benötigen außerdem die Host-Verwaltungsadresse und das `root`-Passwort des Hosts.
- Verwenden Sie einen Browser in einem vertrauenswürdigen Verwaltungsnetzwerk.

Jeder Schritt läuft in Ihrem **Browser**. Sie benötigen keine Shell auf Host oder Appliance.

| Adresse oder Konto | Zweck |
| --- | --- |
| Host-Verwaltungsadresse | XO Lite und die Serververbindung in XOA-HL |
| Adresse der XOA-HL-Appliance | Xen-Orchestra-Weboberfläche |
| XO-Administratorkonto | Anmeldung bei Xen Orchestra |
| `root`-Konto des Hosts | Ermöglicht Xen Orchestra die Host-Verwaltung |
| Systemkonto `xo` der Appliance | Nur SSH-Zugriff; nicht das Webkonto |

## 1. Appliance öffnen und anmelden {#1-open-the-appliance-and-sign-in}

1. Öffnen Sie `https://<appliance-address>`. Verwenden Sie die Appliance-Adresse, nicht die Host-Adresse.
2. Warnt der Browser vor einem selbstsignierten Zertifikat, prüfen Sie vor dem Akzeptieren, dass die Adresse zu Ihrer Appliance gehört. Ändert sich das Zertifikat einer bestehenden Installation, klären Sie zunächst die Ursache.
3. Warten Sie auf den Abschluss des ersten Starts. Melden Sie sich anschließend mit dem **XO-Administratorkonto aus dem Bereitstellungsformular** an. Verwenden Sie weder das `root`-Konto des Hosts noch das SSH-Konto der Appliance.

**Prüfung:** Die Xen-Orchestra-Oberfläche öffnet sich. Ein leeres Inventar ist normal, solange noch kein Host verbunden ist.

{{< callout type="warning" >}}
Kann der erste Start in diesem Image Ihre Zugangsdaten nicht setzen, kann das Webkonto bei `admin@admin.net` mit Passwort `admin` verbleiben. Funktioniert Ihr eigenes Konto auf einer neuen Appliance nicht, versuchen Sie dieses Ersatzkonto ausschließlich im vertrauenswürdigen Netzwerk. Funktioniert es, ändern Sie das Passwort sofort in Schritt 2. Funktioniert keines der Konten, beenden Sie weitere Versuche und nutzen Sie die Fehlersuchtabelle am Seitenende.
{{< /callout >}}

## 2. Dauerhaftes Passwort festlegen {#2-set-a-password-you-will-keep}

1. Wählen Sie das **Benutzersymbol** im Menü, um **User** (`/#/user`) zu öffnen.
2. Geben Sie im Passwortbereich das aktuelle und anschließend zweimal das neue Passwort ein. Verwenden Sie ein einzigartiges Passwort. Wählen Sie **OK**.
3. Bewahren Sie das neue Passwort sicher auf. Melden Sie sich ab und mit dem neuen Passwort wieder an.

**Prüfung:** Sie können sich mit dem neuen Passwort anmelden. Nur das Webkonto wird geändert. Das `root`-Passwort des Hosts und das SSH-Passwort der Appliance bleiben unverändert.

## 3. Oberflächensprache wählen {#3-choose-the-interface-language}

1. Öffnen Sie **Benutzersymbol → User → Language**.
2. Wählen Sie Ihre Sprache. Die Beschriftungen ändern sich sofort.

Diese Einstellung ändert nur die XOA-HL-Oberfläche. Die Dokumentation hat oben auf dieser Seite eine eigene Sprachauswahl. Manche Appliance-Beschriftungen sind möglicherweise noch nicht übersetzt. Die Adresse `/#/user` öffnet diese Ansicht immer.

## 4. Host verbinden {#4-connect-the-host}

1. Öffnen Sie **Settings → Servers** (`/#/settings/servers`). Ist Ihr Host bereits aufgeführt und verbunden, prüfen Sie sein Inventar, statt ihn erneut hinzuzufügen.
2. Geben Sie im Formular eine verständliche Bezeichnung, die **Verwaltungs-IP-Adresse oder den Hostnamen des Hosts**, Benutzer `root` und das bei der Installation gesetzte Host-Passwort ein. Geben Sie nicht die Appliance-Adresse ein.
3. Wählen Sie **Connect**. Erscheint eine Warnung zum selbstsignierten Zertifikat, prüfen Sie zunächst, dass dies tatsächlich Ihr Host ist. Akzeptieren Sie anschließend das Zertifikat für diesen Server.
4. Prüfen Sie die Serverzeile auf eine Fehleranzeige. Öffnen Sie danach das Inventar und prüfen Sie, dass Pool, Host und Storage Repositories (SRs) erscheinen. **Enabled** bedeutet nur, dass die Verbindung eingeschaltet ist. Es bedeutet nicht, dass sie funktioniert.

**Prüfung:** Host und Speicher erscheinen ohne Verbindungsfehler. Jetzt können Sie [Ihre erste VM erstellen](/docs/xoa-hl/create-vm/).

## 5. Installierte Versionen notieren {#5-note-the-installed-versions}

Öffnen Sie als Administrator **About** (`/#/about`). Notieren Sie **XOA-HL version** und **XOA-HL VM version** zusammen mit dem Image-Tag. Die VM-Version bezeichnet den Image-Build. Paketupdates können später die Anwendungsversion ändern.

Die [Versionsmatrix](/docs/reference/release-matrix/) nennt den Lieferumfang jeder Veröffentlichung. Sie zeichnet keine Testergebnisse auf.

## Bei Problemen {#if-something-goes-wrong}

| Problem | Prüfung |
| --- | --- |
| Die Appliance-Seite öffnet sich nicht | In XO Lite prüfen, dass die Appliance-VM läuft. Adresse, Netzwerk, Gateway und Browser-Erreichbarkeit prüfen. Nicht erneut über eine funktionierende VM bereitstellen. |
| Die Zugangsdaten aus der Bereitstellung funktionieren nicht | Abschluss des ersten Starts abwarten und prüfen, dass das Webkonto verwendet wurde. Anschließend das obige Ersatzkonto versuchen. Bei Zugriff auf Appliance-Konsole oder SSH `/var/log/xoa-first-boot.log` lesen. Private Daten vor dem Weitergeben entfernen. |
| Die Anmeldung beim Host schlägt fehl | Host-Adresse und dessen `root`-Passwort prüfen. Das Passwort des Webadministrators ist ein anderes. |
| Der Server zeigt einen Zertifikatsfehler | Host-Identität prüfen, bevor sein selbstsigniertes Zertifikat akzeptiert wird. Keine unerklärte Änderung akzeptieren. |
| Der Server ist aktiviert, aber das Inventar leer | Verbindungsfehler lesen. Prüfen, dass die Appliance den Host erreicht und die Host-Adresse stimmt. Die Erreichbarkeit im Browser beweist nicht die Erreichbarkeit von der Appliance aus. |

## Nächste Schritte {#next-steps}

[Erste VM erstellen](/docs/xoa-hl/create-vm/) oder die [Update-Anleitung für Appliance und Host](/docs/guides/updates/) lesen.

{{< details title="Quellen" closed="true" >}}
Abgeglichen mit: [Image-Veröffentlichung](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261022-a280852); [Einrichtung der Zugangsdaten in build-xoa-hl@fc7ebfa](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh); [Benutzeransicht in XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [Serveransicht derselben Version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [XOA-HL-About-Seitenpatch in xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
{{< /details >}}
