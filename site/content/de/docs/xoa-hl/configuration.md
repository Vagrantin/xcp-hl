---
title: "Appliance-Dienst konfigurieren"
linkTitle: "Diensteinstellungen"
description: "Dienstkonfigurationsdateien finden, Zugriffswege und HTTPS-Zertifikat prüfen und Änderungen sicher anwenden."
weight: 91
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:cf10324c828a27039571b3a119cc1feacd94fbe74d8a0815a3060736e0c32685
glossaryTerms: ["appliance", "host", "pool"]
---

Finden Sie die xo-server-Konfigurationsdateien der XOA-HL-Appliance, prüfen Sie Verwaltungszugriff und HTTPS-Zertifikat und wenden Sie Änderungen sicher an. Sie arbeiten als root in einer Shell innerhalb der Appliance und halten eine separate Konsole bereit. Diese Dateien sind von den Einstellungen und Datensätzen getrennt, die die Weboberfläche exportiert.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet.
{{< /callout >}}

## Einstellungsdateien finden {#settings-files}

| Ort | Inhalt | Umgang |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` und `sample.config.toml` | Paketstandards und ein kommentiertes Beispiel | Nur lesen. Paketupdates ersetzen diese Dateien |
| `/root/.config/xo-server/config.toml` | Eigene Einstellungen (Betreiberdatei). Bei der Installation nur erstellt, falls noch nicht vorhanden | Vor dem Bearbeiten privat sichern. Die Paketinstallation behält diese Datei |
| `/root/.config/xo-server/config.z-auto.json` | Vom Server selbst geschriebene Einstellungen | Bei der Suche nach Überschreibungen auf Vorhandensein prüfen. Nicht blind überschreiben |
| Redis-Datenbank | XO-Anwendungsdatensätze | Export und Import der Weboberfläche im dokumentierten Umfang verwenden |
| `/etc/xoa-hl/update.conf` | Modus, Zeitplan und Kanal für Appliance-Updates | Stattdessen **Settings → XOA-HL Updates** und die Update-Anleitung verwenden |
| `/opt/xo/xoahl.crt` und `xoahl.key` | TLS-Zertifikat und privater Schlüssel der Appliance | Separate Kopie aufbewahren. Privaten Schlüssel niemals einem Bericht anhängen |

Der mitgelieferte systemd-Dienst läuft als root und liest die Benutzerkonfiguration unter `/root/.config`. xo-server liest außerdem `/etc/xo-server/config.*` sowie lokale `.xo-server.*`-Dateien und führt mehrere Dateien zusammen. Prüfen Sie eigene Dienstüberschreibungen und andere Konfigurationsdateien, bevor Sie entscheiden, welcher Wert gilt. Diese Seite behandelt nur den mitgelieferten Dienst, kein eigenes Dienstkonto.

Der [Konfigurationsexport](/docs/xoa-hl/configuration-backup/) enthält weder Ihre TOML-Datei noch TLS-Dateien oder Update-Einstellungen. Siehe dazu [Appliance-Wartung](/docs/xoa-hl/maintenance/) und [Updates](/docs/guides/updates/).

## Appliance-URL für die Pool-Erkennung festlegen {#public-url}

`http.publicUrl` legt die Appliance-URL fest, die XO zur Erkennung in jedem verbundenen Pool hinterlegt. Die Einstellung erstellt weder Listener noch Zertifikat oder DNS-Eintrag. Verwenden Sie eine tatsächliche HTTPS-URL der Appliance mit passendem DNS und vertrauenswürdigem Zertifikat und prüfen Sie zuerst, dass sie im Browser aufgeht. Lesen Sie vor einer Änderung [Hosts und Pools](/docs/xoa-hl/hosts-pools/).

Versuchen Sie dies auf einer Labor-Appliance, die Sie neu erstellen können. Ergänzen Sie die Eigenschaft in der **vorhandenen** Tabelle `[http]`. Dieses Minimalbeispiel behält den mitgelieferten HTTPS-Listener und die Redis-Adresse. Es ersetzt keine von Ihnen angepasste Datei:

```toml
[http]
publicUrl = "https://xoa.lab.example"

[[http.listen]]
port = 443
cert = "/opt/xo/xoahl.crt"
key = "/opt/xo/xoahl.key"

[redis]
uri = "redis://127.0.0.1:6379/0"
```

Fügen Sie keine zweite `[http]`-Tabelle hinzu und entfernen Sie den bestehenden Listener nicht. Behalten Sie die tatsächlichen Zertifikat- und Schlüsselpfade. Das Paket erstellt bei der Installation ein eigenes selbstsigniertes Zertifikat und einen Schlüssel; es liefert keinen gemeinsamen Schlüssel aus. Fehlt Schlüssel, Zertifikat oder Marker `/var/lib/xoa-hl/tls-generated`, wird ein neues Paar erzeugt. Notieren Sie vor einem Upgrade den installierten TLS-Zustand. Zertifikatsaustausch, Reverse-Proxys und die Verlagerung von Redis werden hier nicht behandelt.

## Verwaltungszugriff erfassen, bevor Sie das Netzwerk einschränken {#management-network}

Diese Prüfung liest nur und verändert nichts. Die mitgelieferte Einrichtung nimmt HTTPS auf Port `443` an. Eigene Einstellungen, Proxy, Firewall oder ein anderes Image können den tatsächlichen Zugriffsweg verändern. Die Weboberfläche legt keine Firewall-Regeln für Sie an.

**Vor dem Beginn**

- Stimmen Sie erlaubte Verwaltungsclients, Subnetze, Dienste und Sicherungsziele mit Netzwerk- und Host-Verantwortlichen ab.
- Vereinbaren Sie einen separaten Konsolenzugang, den die Einschränkung nicht betrifft.
- Führen Sie dies vor Änderungen an ACL, VIF, Host-PIF oder Switch-Richtlinien durch.

| Zugriffsweg | Notieren und prüfen |
| --- | --- |
| Genehmigter Browser → XOA-HL | Appliance-VM und -Adresse, aufgelösten Namen, tatsächlichen HTTPS-Endpunkt und Zertifikatsidentität notieren. Von einem erlaubten Client neu anmelden und die Host-Liste prüfen. Der mitgelieferte Listener nutzt `443`; installierte Konfiguration und echten Endpunkt trotzdem prüfen. `http.publicUrl` kündigt nur eine Adresse an und öffnet keinen Port. |
| XOA-HL → Hosts und Pools | Unter **Settings → Servers** die verbundene Serveradresse, erwartete Pool- und Host-IDs sowie Zertifikatbehandlung notieren. Aktuelle Host-Liste und, falls bereits im Labor getestet, aktuelle schreibgeschützte [Host-Statistiken](/docs/xoa-hl/hosts-pools/#host-statistics) prüfen. Die Browser-Anmeldung allein beweist keine Host-Erreichbarkeit von der Appliance aus. |
| Browser → Konsole über XOA-HL → Host der VM | Falls die Konsole benötigt wird, eine laufende Test-VM nach der [Konsolenanleitung](/docs/xoa-hl/vm-operations/#vm-console) öffnen. Browserergebnis und ausführenden Host notieren. Die Konsole nutzt eine eigene WebSocket-Verbindung von der Appliance zu diesem Host; eine funktionierende Host-Liste beweist diese nicht. |
| XOA-HL → Sicherungs-Remotes und Updates | Jedes Sicherungs-Remote sowie Paket-, DNS- und Zeitdienste der Appliance samt Verantwortlichen erfassen. Remote nach seinem [Sicherungsverfahren](/docs/xoa-hl/backup-restore/) und Paketzugriff nach der [Appliance-Update-Anleitung](/docs/xoa-hl/maintenance/) testen. Eine erfolgreiche Web-Anmeldung beweist diese Wege nicht. |

Auf einer Labor-Appliance mit ermittelter Version:

1. Für jeden benötigten Weg Quellclient, Zielname oder -adresse, Dienst, Ergebnis und Zeit notieren.
2. Den Netzwerkverantwortlichen mit einem erlaubten Test und getrennten Protokollen prüfen lassen, dass ein unberechtigter Testclient die Web-Anmeldeseite nicht erreicht. Ein blockierter Ping beweist weder HTTPS-Isolation noch funktionierende Verwaltung.
3. Konsolenzugriff außerhalb des geplanten eingeschränkten Wegs halten.
4. Wird eine Richtlinienänderung separat genehmigt, jeweils nur eine vom Verantwortlichen kontrollierte Regel ändern. Nach jeder Änderung dieselben erlaubten und verbotenen Tests wiederholen.
5. Vor Ende des Wartungsfensters Anmeldung, Host-Liste, Konsole und Sicherungen prüfen.

**Prüfung:** Alle benötigten Wege funktionieren weiterhin, und der unberechtigte Client erreicht die Anmeldeseite nicht.

Fällt ein benötigter Weg aus oder verlieren Sie Zugriff, halten Sie an. Verwenden Sie über die separate Konsole die dokumentierte Rücknahme des Netzwerkverantwortlichen. Entfernen Sie nicht die XOA-Verbindung und ändern Sie nicht als Abkürzung die Verwaltungs-PIF des Hosts. Tatsächliche Listener, Client-Segmentierung, Proxy- und NAT-Wege, Host- und Remote-Ports sowie Rücknahme werden hier nicht behandelt. Erstellen Sie keine produktive Freigabeliste allein aus dieser Seite.

## HTTPS-Zertifikat vor dem Ersetzen prüfen {#tls-certificate-preflight}

Diese Prüfung liest nur Dateien und Verbindungen und erneuert nichts. Bei der Installation richtet die mitgelieferte Einrichtung einen HTTPS-Listener auf Port `443` mit `/opt/xo/xoahl.crt` und `/opt/xo/xoahl.key` ein. Spätere Änderungen oder ein Reverse-Proxy können TLS an anderer Stelle bereitstellen.

Das Paket liefert keinen gemeinsamen privaten Schlüssel. Bei der Installation erzeugt es ein selbstsigniertes Paar mit `CN=xoa.local`, wenn eine der Dateien oder der Marker `/var/lib/xoa-hl/tls-generated` fehlt. Ein späteres Paketupdate kann das Paar genauso neu erzeugen und startet anschließend `xo-server` neu (`%posttrans`). Notieren Sie vor der Erneuerungsplanung tatsächliche Pfade und Paketzustand. Löschen Sie niemals den Marker zur Zertifikatsrotation.

1. Stellen Sie sicher, dass eine separate Konsole und ein lokales Administratorkonto verfügbar sind.
2. Notieren Sie privat installiertes Image und Paket, die wirksamen Werte von `http.listen` und zusammengeführte Konfigurationsüberschreibungen. Zeigen Sie Dienstüberschreibungen mit `systemctl cat xo-server` an.
3. Notieren Sie, ob Reverse-Proxy, Loadbalancer oder anderer TLS-Endpunkt vor der Appliance stehen. `http.publicUrl` kündigt nur eine Adresse an: Es zeigt weder Listener noch das im Browser sichtbare Zertifikat. Halten Sie an, wenn mehrere Listener oder unerwartete Belegungen auf Port `443` auffallen.
4. Lesen Sie auf der **Appliance** nur die Metadaten des konfigurierten Zertifikats, Schlüssels und Markers. Für die mitgelieferten Pfade zeigen diese schreibgeschützten Befehle Dateimodi und öffentliche Zertifikatsfelder, ohne den privaten Schlüssel auszugeben:

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   Verwendet Ihre Konfiguration andere Dateien, nutzen Sie das **tatsächlich konfigurierte** Paar. Fehlt eine Datei oder der Marker, halten Sie an und klären Sie dies vor jedem Update oder Neustart; erzeugen Sie kein neues Paar. Halten Sie privaten Schlüssel und vollständige Konfiguration aus Screenshots, Protokollen und Issues heraus.
5. Öffnen Sie von einem **genehmigten Client** die echte HTTPS-Adresse und melden Sie sich in einer neuen Browsersitzung erneut an.
6. Ist OpenSSL verfügbar und hat der Verantwortliche Ihnen die Vertrauenskette gegeben, führen Sie `openssl s_client -connect <name>:<port> -servername <name> -verify_hostname <name> -verify_return_error -brief </dev/null` mit tatsächlichem DNS-Namen und Port aus. Ergänzen Sie bei privater CA die genehmigte Option `-CAfile <ca-path>`. Prüfen Sie vor Verwendung der Optionen die installierte OpenSSL-Version.
7. Vergleichen Sie Fingerabdruck, Name, Kette und Ablaufdatum des Zertifikats mit dem erwarteten Endpunkt.

**Prüfung:** Sie haben das vom Browser empfangene Zertifikat und die zugrunde liegenden Dateien notiert. Das bei der Installation erzeugte selbstsignierte Zertifikat kann die Vertrauensprüfung nicht bestehen: Notieren Sie das Ergebnis, schalten Sie jedoch die Prüfung nicht aus und bezeichnen Sie das Zertifikat nicht als vertrauenswürdig. Übernimmt ein Proxy TLS, kann sein Zertifikat von der Appliance-Datei abweichen; notieren Sie beide getrennt.

**Vor der Planung eines Austauschs** vereinbaren Sie mit Zertifikats- und Appliance-Verantwortlichen:

- neue Zertifikatskette, passenden privaten Schlüssel, abgedeckte Namen und Ablaufdatum;
- sichere Ablage sowie Dateieigentümer und Berechtigungen;
- separate Wiederherstellungskonsole und private Sicherung von aktuellem **Zertifikatspaar, Marker und Betreiberdatei**;
- Wartungsfenster nach Job-Abschluss, exakt zu ändernden Listener oder Proxy und getestetes Neustart- und Rücknahmeverfahren;
- anschließende Tests: neue vertrauenswürdige Browser-Anmeldung, korrekter Fingerabdruck, funktionierender lokaler Administrator, Host- und Pool-Liste sowie Konsole.

Eine gültige Konfigurationsdatei, vorhandene Dateien oder ein erfolgreicher Neustart beweisen weder Client-Vertrauen zum Zertifikat noch die Verwendung des richtigen Zertifikats. Die Erneuerung wird hier nicht behandelt: Verwenden Sie diese Prüfung nicht als produktives Austauschverfahren.

## Syntax prüfen und Dienst neu starten {#apply-change}

**Vor dem Beginn**

- Private Kopie der ursprünglichen Betreiberdatei außerhalb der Appliance aufbewahren und Berechtigungen notieren.
- Konsolenzugriff bereithalten.
- Auf Abschluss von Sicherungs-, Wiederherstellungs- und Verwaltungsjobs warten.

Führen Sie nach Bearbeitung der Datei innerhalb der Appliance als root diese Prüfung aus:

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` bedeutet nur gültige Syntax. Es prüft weder Dateiberechtigungen, TLS-Vertrauen, zusammengeführte Werte noch Erreichbarkeit. Beheben Sie jeden Fehler vor dem Neustart.

Starten Sie im vereinbarten Wartungsfenster den Dienst neu und lesen Sie Status sowie aktuelles Protokoll:

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

Der Neustart trennt die Weboberfläche. Verbinden Sie sich erneut unter der erwarteten Adresse.

**Prüfung:** Die Anmeldung funktioniert und die Host-Liste ist vollständig. XO schreibt seine URL regelmäßig in jeden Pool; prüfen Sie daher die Pool-Erkennung nach der nächsten Aktualisierung.

Startet der Dienst nicht, stellen Sie die gesicherte Betreiberdatei über die Konsole wieder her, prüfen Sie ihre Syntax erneut und starten Sie einmal neu. Bei unklarem Ergebnis siehe [Fehlersuche](/docs/xoa-hl/troubleshooting/). Entfernen Sie Geheimnisse vor dem Weitergeben von Protokollen.

{{< details title="Quellen" closed="true" >}}
- **Konfigurationsdateien und Dienst**: [Skript zur Ersteinrichtung](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [Paketinstallation und -update](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [systemd-Dienst](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [Konfigurationslader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [Standardeinstellungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [Kommentiertes Beispiel](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [Pool-Erkennung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).
- **Verwaltungszugriff**: [Serververbindung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [Konsolenproxy zum Host der VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **HTTPS-Zertifikat**: [Erzeugtes Paar, Marker und Neustart nach Update](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [Ursprünglicher Listener](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [Wirksame Listener-Einrichtung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [OpenSSL-x509-Handbuch](https://docs.openssl.org/3.0/man1/openssl-x509/), [OpenSSL-s_client-Handbuch](https://docs.openssl.org/3.0/man1/openssl-s_client/).
{{< /details >}}
