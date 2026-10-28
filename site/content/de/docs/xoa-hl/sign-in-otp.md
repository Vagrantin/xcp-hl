---
title: "Anmeldung mit einem Einmalcode schützen"
linkTitle: "Einmalcodes (OTP)"
description: "Die Anmeldung eines Kontos um einen Einmalcode ergänzen, prüfen und sicher wieder entfernen."
weight: 71
translationKey: xoa-manual-sign-in-otp
translationStatus: draft
sourceRevision: sha256:6cd964ad6c27dba4fac2174ee07db3969f54dcdebe9b7f253e906688f3346a44
glossaryTerms: ["appliance"]
---

XOA-HL kann nach dem Passwort einen sechsstelligen Einmalcode aus einer Authenticator-App verlangen. Der Code ändert sich zeitabhängig (TOTP). Jedes Konto mit lokalem Passwort aktiviert ihn für sich selbst. Probieren Sie dies zuerst mit einem Nicht-Administratorkonto aus, das Sie [für diesen Test angelegt haben](/docs/xoa-hl/permissions/).

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Spätere Versionen können abweichen.
{{< /callout >}}

## Vor dem Beginn {#prepare}

| Voraussetzung | Grund |
| --- | --- |
| Eine TOTP-Authenticator-App auf einem von Ihnen kontrollierten Gerät | Sie erzeugt Codes aus einem gemeinsamen Geheimnis |
| Korrekte Uhrzeit auf Appliance und Gerät | XO akzeptiert den aktuellen Code sowie die Codes des vorherigen und folgenden 30-Sekunden-Zeitschritts |
| Ein zweiter Administrator oder ein gesonderter Wiederherstellungsplan | Andernfalls kann ein verlorenes Gerät den einzigen Administrator aussperren |
| Eine während des Tests offen gehaltene Browsersitzung | Damit können Sie den Einmalcode entfernen, falls die Prüfung scheitert |

Bei der Einrichtung prüft Ihr Browser den eingegebenen Code anhand seiner eigenen Uhr. Bei der Anmeldung prüft die Appliance ihn anhand ihrer Uhr. Ein bei der Einrichtung akzeptierter Code belegt daher nicht, dass die Appliance-Uhr stimmt.

## Einmalcode für das eigene Konto aktivieren {#enable-otp}

1. Melden Sie sich mit dem zu schützenden Konto an. Öffnen Sie über das Benutzersymbol im Menü Ihre Benutzerseite (`/#/user`).
2. Aktivieren Sie den Schalter **OTP authentication**. Der Dialog **Add OTP authentication** zeigt einen QR-Code und das Geheimnis als Text.
3. Scannen Sie den QR-Code oder geben Sie das Geheimnis in Ihrer Authenticator-App ein. Der neue Eintrag hat den Aussteller `Xen Orchestra` und die E-Mail-Adresse beziehungsweise den Anmeldenamen des Kontos als Namen.
4. Geben Sie den aktuellen Code in **OTP code** ein und bestätigen Sie. Bei einem falschen Code öffnet sich der Dialog erneut: Geben Sie den jetzt angezeigten Code der App ein. Mit **Cancel** bleibt der Einmalcode deaktiviert.

Fehlt der Schalter, halten Sie an und notieren Sie die installierte Version. Dieser Build verwendet den voreingestellten Open-Source-Plan von XO, der den Schalter anzeigt. Ein fehlendes Abonnement ist daher nicht die Ursache. [Melden Sie die Abweichung](/docs/xoa-hl/troubleshooting/).

**Prüfung:** Der Schalter ist eingeschaltet, und die Benutzerseite zeigt daneben das Geheimnis und seinen QR-Code. Jeder, der diese sieht, kann gültige Codes erzeugen: Geben Sie diese Seite nicht weiter und erstellen Sie keine Bildschirmfotos davon. Dieser QR-Code verwendet für dasselbe Geheimnis den Aussteller `XenOrchestra` (ohne Leerzeichen). Behalten Sie den vorhandenen App-Eintrag; scannen Sie ihn nicht erneut.

## Anmeldung in einer neuen Sitzung prüfen {#check-sign-in}

1. Lassen Sie die aktuelle Sitzung offen. Öffnen Sie ein privates Browserfenster und melden Sie sich mit Benutzername und Passwort an.
2. Eine zweite Seite verlangt einen **Code**. Geben Sie den aktuellen App-Code ein und wählen Sie **Sign in**.
3. Ein falscher oder abgelaufener Code führt zu `Invalid code`. Warten Sie auf den nächsten Code und versuchen Sie es erneut.
4. Prüfen Sie, dass das richtige Konto angemeldet ist, und schließen Sie das private Fenster.

**Prüfung:** Die Anmeldung hat einen Code verlangt und den richtigen akzeptiert. Scheitert dies weiterhin, [entfernen Sie den Einmalcode](#remove-otp) über die offene Sitzung, prüfen Sie beide Uhren und aktivieren Sie ihn erneut.

## Was ein Einmalcode nicht schützt {#otp-limits}

- Seine Aktivierung beendet keine bestehenden Sitzungen und widerruft keine Token. Jedes gültige Authentifizierungstoken überspringt die Codeprüfung, auch später erstellte Token: Token sind eigenständige Zugangsdaten. Öffnen Sie nach der Aktivierung **Authentication tokens** auf Ihrer Benutzerseite und löschen Sie unbekannte oder nicht mehr benötigte Token. Ein Skript mit einem gelöschten Token funktioniert anschließend nicht mehr.
- Geschützt wird nur die XO-Webanmeldung dieses Kontos. SSH- oder Konsolenzugriff auf die Appliance, XO Lite, das Root-Konto auf dem Host und andere XO-Konten sind nicht geschützt.
- Externe Anmeldeanbieter und ihre eigene Mehrfaktorauthentifizierung werden hier nicht behandelt.

## Einmalcode entfernen {#remove-otp}

- **Eigenes Konto:** Deaktivieren Sie auf Ihrer Benutzerseite **OTP authentication** und bestätigen Sie **Remove OTP authentication**.
- **Anderes Konto als Administrator:** Öffnen Sie **Settings → Users**. Wählen Sie in der Spalte **OTP** für dieses Konto **Remove** und bestätigen Sie. Prüfen Sie zunächst, wer die Anfrage stellt, beispielsweise über einen anderen Kanal. Der Benutzer kann danach ein neues Gerät einrichten.

Konten ohne Einmalcode zeigen dort **Not configured**. Verliert der einzige Administrator sein Gerät, bietet die Oberfläche keinen Rückweg. Über die Appliance-Konsole können Sie dennoch [den Administratorzugriff wiederherstellen](/docs/xoa-hl/troubleshooting/#recover-admin-access). Ein zweiter Administrator ist einfacher: Halten Sie einen bereit.

**Prüfung:** Der Schalter ist ausgeschaltet und die OTP-Spalte des Kontos zeigt **Not configured**. In einem neuen privaten Fenster meldet sich das Konto mit lokalem Benutzername und Passwort ohne Code an. Lassen Sie den Wiederherstellungsadministrator angemeldet, bis Sie dies bestätigt haben.

{{< details title="Quellen" closed="true" >}}
- **Benutzerseite und Einrichtung**: [OTP-Abschnitt der Benutzerseite](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/otp.js), [Benutzerseite und Token](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js), [Einrichtungsdialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-otp-modal.js), [Aktionen zum Aktivieren und Entfernen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [OTP-Spalte der Benutzereinstellungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js).
- **Anmeldung und Token**: [Anmeldeseiten](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [Anmeldeformular](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/signin.pug), [Authentifizierung und Token-Ausnahme](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [TOTP-Zeitfenster](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@vates/otp/index.mjs), [Wiederherstellungsbefehl](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [Oberflächenbezeichnungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Build und Browsereinrichtung**: [XO-Standardplan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [Browser-Authenticator](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/otp-authenticator.js), [API der Benutzereinstellungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/user.mjs), [HomeLab-Build](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
