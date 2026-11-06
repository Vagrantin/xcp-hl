---
title: "Mit xo-cli automatisieren"
linkTitle: "Automatisierung (xo-cli)"
description: "Inventar mit xo-cli und einem kurzlebigen Token lesen, danach das Token widerrufen."
weight: 92
translationKey: xoa-manual-automation
translationStatus: draft
sourceRevision: sha256:02733ac5b32a1b356f14bd4b74120dad79a23bae4b41aff2c910840726898ebc
glossaryTerms: ["appliance", "host", "vm"]
---

Lesen Sie mit dem mitgelieferten Kommandozeilenclient xo-cli und einem kurzlebigen Token einen kleinen Inventarausschnitt, und widerrufen Sie das Token anschließend. Führen Sie diesen Test aus, bevor Sie eine Automatisierung schreiben, die eine VM verändert. Die Befehle laufen in einer Shell innerhalb der **XOA-HL-Appliance**. Das Token widerrufen Sie im Browser, angemeldet als derselbe Testbenutzer.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2), mit `xo-cli` **0.32.2** und `xo-lib` **0.11.1**. Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Die Befehle wurden nur gegen einen simulierten Server ausgeführt.
{{< /callout >}}

## 1. Shell und TLS-Vertrauen vorbereiten {#prepare}

**Vor dem Beginn**

- Prüfen Sie die installierte Version wie unter [Appliance-Wartung](/docs/xoa-hl/maintenance/) beschrieben.
- Halten Sie ein normales Testbenutzerkonto und eine entbehrliche Test-VM bereit. Prüfen Sie die Berechtigungen dieses Benutzers gesondert mit [Benutzer und Berechtigungen](/docs/xoa-hl/permissions/).
- Verwenden Sie einen Appliance-DNS-Namen, der zum Zertifikat passt. Das bei der Installation erstellte selbstsignierte Zertifikat für `xoa.local` kann zunächst Anpassungen an Labor-DNS oder Zertifikat erfordern.
- Beschaffen Sie die öffentliche CA oder das Zertifikat der Appliance als PEM-Datei über einen vertrauenswürdigen Kanal. Prüfen Sie den Fingerabdruck über einen unabhängigen Weg.

1. Öffnen Sie eine neue, eigene Bash-Sitzung **innerhalb der Appliance**. Dort verwenden Sie das mitgelieferte `/usr/local/bin/xo-cli`.
2. Ersetzen Sie im Beispiel des nächsten Abschnitts PEM-Dateipfad, URL und E-Mail-Adresse durch Ihre eigenen Werte.

`NODE_EXTRA_CA_CERTS` ergänzt die Liste vertrauenswürdiger Zertifikate; der Hostname wird weiterhin geprüft. Schlägt die TLS-Prüfung fehl, korrigieren Sie Namen oder Zertifikat. Umgehen Sie die Prüfung niemals mit `--allowUnauthorized` oder `NODE_TLS_REJECT_UNAUTHORIZED=0`.

## 2. Kurzlebiges Token registrieren {#register-token}

Die folgenden Befehle bewahren die Zugangsdaten in einem neuen temporären Ordner auf; Ihre bestehende xo-cli-Konfiguration bleibt unberührt. Durch `umask 077` können nur Sie die neue Datei lesen.

- `register` fragt das Passwort ab. Geben Sie es nicht als Argument an, und setzen Sie niemals ein Token in eine URL.
- Verwendet das Konto Einmalcodes (OTP), ergänzen Sie vor der URL `--otp CODE` mit einem aktuellen Code.

```bash
umask 077
xoa_cli_config="$(mktemp -d)"
xoa_cli_ca="/path/to/verified-appliance-ca.pem"
xoa_cli() {
  XDG_CONFIG_HOME="$xoa_cli_config" NODE_EXTRA_CA_CERTS="$xoa_cli_ca" xo-cli "$@"
}
xoa_cli register --expiresIn '1 hour' https://xoa.lab.example user@example.invalid
```

Das Token fordert absichtlich `1 hour` an. Standardmäßig erteilt der Server ein Token für 30 Tage, höchstens für ein halbes Jahr; die Serverkonfiguration kann diese Grenzen ändern.

Das Token besitzt alle Rechte seines Benutzers: Es ist nicht auf Lesezugriffe beschränkt. Behandeln Sie den Konfigurationsordner wie ein Passwort. Halten Sie ihn aus Shell-Traces, Sicherungen in Issue-Anhängen und der Versionsverwaltung heraus. Die Registrierung erstellt ein Anmeldetoken; die nächsten Befehle lesen ausschließlich Daten.

## 3. Inventar erkunden und lesen {#read-inventory}

Führen Sie diese Befehle aus. Optionen wie `--json` und `--id` stehen vor den Parametern.

```bash
xoa_cli list-commands xo.getAllObjects
xoa_cli system.getServerVersion --json
xoa_cli list-objects --id --name_label --power_state type=VM
xoa_cli xo.getAllObjects --json 'filter=json:{"type":"VM"}' 'limit=json:1'
```

| Befehl | Ergebnis |
| --- | --- |
| `list-commands xo.getAllObjects` | Die Parameter der Methode in lesbarer Form. Eine sichtbare Methode bedeutet nicht, dass Sie sie verwenden dürfen |
| `system.getServerVersion --json` | Die Server-Paketversion, in dieser Version `"5.193.1"`. Das ist nicht die XO-Version (5.113.2) |
| `list-objects --id --name_label --power_state type=VM` | Ein JSON-Array nur mit diesen Eigenschaften. Kein VM-Zustand wird verändert |
| `xo.getAllObjects --json …` | Ein nach Objekt-ID indiziertes JSON-Objekt, nach Objekttyp gefiltert und auf ein Objekt begrenzt |

Das Präfix `json:` übermittelt einen typisierten Wert: `limit=json:1` sendet eine Zahl, `limit=1` eine Zeichenkette. Der letzte Befehl sendet diese JSON-RPC-Anfrage über einen **WebSocket an `/api/`** (kein HTTP POST):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "xo.getAllObjects",
  "params": { "filter": { "type": "VM" }, "limit": 1 }
}
```

Filter und ausgewählte Felder bestimmen nur die Anzeige: Sie sind **keine Zugriffsbeschränkungen**. Nehmen Sie weder an, dass die API nur die in der Weboberfläche des Benutzers sichtbaren Objekte zurückgibt, noch, dass ausgelassene Felder nie abgerufen wurden. Halten Sie die Ergebnisse privat und prüfen Sie gesondert, was das Konto tatsächlich sehen kann. Ein Name ist keine stabile ID. Dieses begrenzte Ergebnis ist kein vollständiges Inventar und keine zuverlässige Methode, eine VM auszuwählen.

## 4. Token widerrufen und aufräumen {#revoke-token}

1. Öffnen Sie in einer getrennten Browsersitzung als derselbe Testbenutzer über das Benutzersymbol im Menü **User** (`/#/user`).
2. Löschen Sie unter **Authentication tokens** das Token dieses CLI-Clients.
3. Führen Sie zurück in der Shell den ersten folgenden Befehl aus, bevor Sie lokal etwas entfernen. Er muss mit einem Authentifizierungsfehler und einem von null verschiedenen Rückgabecode scheitern.
4. Ist er erfolgreich, wurde das Token nicht widerrufen. Halten Sie an und prüfen Sie Konto und Token, bevor Sie einen erfolgreichen Widerruf behaupten.
5. Entfernen Sie mit den übrigen Befehlen die lokalen Zugangsdaten und schließen Sie danach die dafür geöffnete Shell.

```bash
xoa_cli system.getServerVersion --json
xoa_cli unregister
rm -rf -- "$xoa_cli_config"
unset -f xoa_cli
unset xoa_cli_config xoa_cli_ca
```

**Prüfung:** Nach dem Löschen des Tokens im Browser scheitert der Versionsbefehl mit einem Authentifizierungsfehler.

`unregister` entfernt nur die lokalen Einträge `server` und `token`; es widerruft das Token auf dem Server **nicht**. Das Entfernen des temporären Ordners ist nur eine lokale Bereinigung und ersetzt keinen Widerruf. Dauerhafte Automatisierung braucht ein eigenes Konzept für Geheimnisablage, Erneuerung, Widerruf, Fehlerbehandlung und eng begrenzte Rechte; das wird hier nicht behandelt.

{{< details title="Quellen" closed="true" >}}
- **Kommandozeilenclient**: [xo-cli](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/index.mjs), [Ablageort der Clienteinstellungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-cli/config.mjs), [xo-lib](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-lib/src/index.js).
- **Token und Inventar**: [Token-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/token.mjs), [Token-Ablauf](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/authentication.mjs), [Inventar-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [Token auf der Benutzerseite](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js).
{{< /details >}}
