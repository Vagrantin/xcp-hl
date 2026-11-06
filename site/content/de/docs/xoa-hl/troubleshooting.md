---
title: "Sicherungsfehler und andere Probleme beheben"
linkTitle: "Fehlerbehebung"
description: "Ursachen von Netzwerk-, Sicherungs-, Update- und Anmeldeproblemen finden und ein Problem melden."
weight: 82
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:fa3eed7a7f974bcc1bebcd34d1969b194a60f8eb7ed99d793d0961ff5759c2cd
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Beginnen Sie mit dem Symptom und dem letzten vorherigen Vorgang und folgen Sie der passenden Prüfung. Die meisten Prüfungen lesen nur Informationen: Sie melden sich im Browser bei der **XOA-HL-Appliance** als Administrator an. Einige Prüfungen benötigen Appliance- oder Gastkonsole. Sichern Sie Fehler und Protokolle, bevor Sie ein fehlgeschlagenes Update, einen Import oder eine Sicherung wiederholen.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet.
{{< /callout >}}

## Mit dem Symptom beginnen {#symptoms}

| Problem | Prüfen |
| --- | --- |
| Appliance-Seite öffnet sich nicht | Prüfen Sie in XO Lite laufende Appliance-VM sowie richtige Adresse und Netzwerk. Prüfen Sie danach `xo-server` und Datenträgerplatz mit den [Konsolenprüfungen](#appliance-checks). **Prüfung:** Die richtige URL öffnet die Anmeldeseite. |
| Erste Anmeldung scheitert | Folgen Sie der [Anleitung zur ersten Anmeldung](/docs/xoa-hl/first-login/) für Webzugangsdaten und Ersatzweg beim ersten Start. Lesen Sie mit autorisiertem Konsolenzugriff das Bereitstellungsprotokoll. **Prüfung:** Anmeldung funktioniert und erstes Passwort wurde geändert. |
| Host aktiviert, aber nichts aufgelistet | Lesen Sie unter **Settings → Servers** den Verbindungsfehler. Prüfen Sie Hostadresse, Zugangsdaten, Zertifikatsidentität und Erreichbarkeit des Hosts von der Appliance. **Prüfung:** Host und Speicher erscheinen ohne Verbindungsfehler. |
| VM-Erstellung oder Installation scheitert | Notieren Sie vor einem weiteren Versuch den Aufgabenfehler. Prüfen Sie Pool, Vorlage, freien SR-Platz, Netzwerk und Startmedium anhand von [Erste VM erstellen](/docs/xoa-hl/create-vm/). **Prüfung:** Eine Test-VM startet den gewählten Installer. |
| Sicherung oder Wiederherstellung scheitert | Lesen Sie das Auftragsprotokoll. Prüfen Sie Sicherungsziel, Zugangsdaten, freien Platz und Ziel-SR; folgen Sie dann [Fehlgeschlagene NFS-Sicherung diagnostizieren](#backup-failures). Entfernen Sie vor dem ersten Start einer wiederhergestellten Kopie jede NIC wie unter [VM sichern und wiederherstellen](/docs/xoa-hl/backup-restore/). **Prüfung:** Auftrag erfolgreich und isolierte wiederhergestellte Kopie mit erwarteten Daten. |
| Updateseite verliert Verbindung | Die Paketinstallation startet `xo-server` neu. Lesen Sie Updateprotokoll und Dienstzustand. Starten Sie kein zweites Update. **Prüfung:** Protokoll endet mit Erfolgsmarkierung, Version stimmt, Anmeldung funktioniert und Hosts sind gelistet. |
| Updateprüfung zeigt ERROR | Lesen Sie `/run/xoa-hl/status` und das Journal des Prüfdienstes. Suchen Sie vor erneuter Prüfung Repository- oder Netzwerkfehler oder ein bereits laufendes Update. **Prüfung:** Neue Prüfung ergibt `UP_TO_DATE` oder `AVAILABLE`. |
| Automatisches Update lief nicht | Prüfen Sie gespeicherten Modus, Appliance-Zeitzone und Timerliste. Ein bei ausgeschalteter Appliance verpasstes Fenster läuft beim nächsten Start nicht nach. **Prüfung:** Richtiger Timer geplant und spätere Laufzeiten passen zum Fenster. |
| Konfigurationsimport scheitert | Sichern Sie Fehler und Serverprotokoll: Änderungen können teilweise bestehen bleiben. Folgen Sie dem [isolierten Importtest](/docs/xoa-hl/configuration-backup/). **Prüfung:** Test auf einer neuen entbehrlichen Appliance erfolgreich. Nehmen Sie kein unverändertes fehlgeschlagenes Ziel an. |
| Kein Administrator kann sich anmelden | Verlorenes Passwort, verlorenes Einmalcode-Gerät oder defekte LDAP-/SAML-Anmeldung. Folgen Sie [Administratorzugriff wiederherstellen](#recover-admin-access) über die Appliance-Konsole. **Prüfung:** Konto meldet sich mit neuem Passwort an und wird als **Admin** gelistet. |

Bei Konsolenproblemen wie Bedienelementen oder leerem beziehungsweise eingefrorenem Bildschirm siehe [VM-Konsole verwenden](/docs/xoa-hl/vm-operations/#vm-console).

## Netzwerkkonnektivität diagnostizieren {#network-connectivity}

Verwenden Sie diese lesenden Prüfungen für ein bestehendes gewöhnliches Gastnetz oder das [Labor-VLAN](/docs/xoa-hl/storage-networks/#host-vlan-network). Melden Sie sich als XOA-HL-Administrator an, damit alle VMs, Pools und Hosts sichtbar sind.

**Vor dem Beginn**

- Gastprüfungen benötigen eine autorisierte Gastsitzung über die Konsole. Switches, DNS und Firewalls prüfen deren Verantwortliche.
- Halten Sie getrennten Konsolenzugriff auf den Host bereit.
- Erzeugen Sie keine Störung und ändern Sie das Verwaltungsnetz nicht zum Test dieser Anleitung.
- Bonds, SDN, VLAN-Trunks im Gast und Notfall-Netzwerkwiederherstellung werden hier nicht behandelt.

### 1. Fehlerhaften Pfad finden {#1-find-the-failing-path}

Notieren Sie Zeitpunkt samt Zeitzone, letzten funktionierenden Vorgang und genauen Fehler. Erfassen Sie auch Quellcomputer, Zielname oder -adresse, Protokoll und Dienstport. Sichern Sie den Ausgangszustand vor einem weiteren Versuch. Ein erfolgreicher Laptoptest belegt keinen Zugriff aus Appliance, Host oder Gast.

| Pfad | Prüfstelle |
| --- | --- |
| Browser → Appliance | Prüfen Sie auf Ihrem Computer URL, Namensauflösung und Zertifikatsidentität. Öffnet sich die Seite nicht, nutzen Sie autorisierten Konsolenzugriff und die [Konsolenprüfungen](#appliance-checks). |
| Appliance → Host | Lesen Sie den Verbindungsfehler unter **Settings → Servers** (`/#/settings/servers`) und folgen Sie [Hosts und Pools](/docs/xoa-hl/hosts-pools/). „Enabled“ ist eine Einstellung, kein Nachweis einer funktionierenden Verbindung. |
| Host → NFS-SR | Prüfen Sie genaues SR sowie Anbindung und Pfad dieses Hosts wie unter [NFS-Speicher für VM-Datenträger erstellen](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Gast- oder Appliance-Tests ersetzen nicht den Zugriff des Hosts selbst. |
| Appliance → Sicherungsziel | Folgen Sie [Fehlgeschlagene NFS-Sicherung diagnostizieren](#backup-failures). NFS-SR und Sicherungsziel verwenden verschiedene Clients und Identitäten. |
| Gast → Peer oder Dienst | Folgen Sie den Schritten 2 bis 4 unten. Eine XO-Anmeldung oder sichtbare Konsole belegt keinen Gastnetzwerkzugriff. |

### 2. Gastschnittstelle bis zum Host-Uplink verfolgen {#2-trace-the-guest-interface-to-the-host-uplink}

Lesen Sie diese Ansichten nur. Klicken Sie weder bearbeitbare Netzwerk- oder MAC-Felder noch Verbindungsschaltflächen an.

1. Notieren Sie VM-UUID, Betriebszustand, Ausführungshost und Pool. Öffnen Sie **Network** der VM (`/#/vms/<id>/network`).
2. Kopieren Sie die Schnittstellen-UUID (VIF) mit der Kopierschaltfläche der Zeile. Notieren Sie Gerätenummer, MAC-Adresse, Netzwerk, MTU und Status.
3. Öffnen Sie die Poolnetzwerkansicht (`/#/pools/<id>/network`) und gleichen Sie die genaue Netzwerk-UUID ab, nicht nur den Namen.
4. Lesen Sie **Connected**: Es zeigt die Anbindung der VIF. Eine abgehängte VIF einer angehaltenen VM ist kein Fehler.
5. Lesen Sie **IP addresses**: Diese Angaben kommen pro VIF-Gerät aus Gastmetriken. Eine fehlende Adresse belegt keinen unkonfigurierten Gast. Eine angezeigte Adresse ist kein aktueller Erreichbarkeitstest. Vergleichen Sie Gastkonsole und [Gastagent-Prüfungen](/docs/xoa-hl/guest-tools/).
6. Notieren Sie Sperrmodusindikator und **Allowed IPs** getrennt von gemeldeten Adressen. Dies sind Verkehrsregeln, kein Formular zur IP-Vergabe an den Gast. Sichern Sie Warnungen und lassen Sie den Netzwerkverantwortlichen die geltenden Regeln erklären. Entsperren Sie die Schnittstelle nicht, entfernen Sie keine Beschränkungen, ändern Sie weder MAC noch MTU und deaktivieren Sie Sicherheit nicht als Abkürzung.
7. Klappen Sie in der Poolnetzwerkzeile **PIFs** auf und finden Sie den Ausführungshost der VM. Die VLAN-Zusammenfassung dieser Zeile stammt ausschließlich vom Poolmaster.
8. Öffnen Sie **Network** dieses Hosts (`/#/hosts/<id>/network`). Notieren Sie PIF-UUID, Gerät, MAC, Netzwerk, VLAN, MTU, Verwaltungsmarkierung und IP-Modus. Vergleichen Sie genehmigte Verkabelungs- und Switchaufzeichnungen. Ein Netz kann absichtlich intern ohne physischen Uplink sein: Prüfen Sie das erwartete Layout vor einer Fehlerbewertung.
9. Lesen Sie Anbindung und physischen Link (Carrier) getrennt. **Connected** am Host zeigt die PIF-Anbindung. Physisches Linksymbol und PIF-Status in der aufgeklappten Poolzeile zeigen den Carrier.

Fehlende PIF-Metriken können ebenfalls als fehlender Carrier erscheinen; ein negativer Status allein belegt kein gezogenes Kabel. Aktualisieren Sie die Ansicht und vergleichen Sie Host- und Switchangaben. Schalten Sie zur Pfadprüfung keine PIFs um, bearbeiten Sie weder VLAN, MTU noch IP, löschen Sie keine Netzwerke und starten Sie das Netzwerk nicht neu.

### 3. Gasteinstellungen und Dienst prüfen {#3-check-guest-settings-and-the-service}

1. Finden Sie in der **Gastkonsole** die Schnittstelle anhand ihrer MAC-Adresse. Ihr Name im Gast kann vom Hostgerätenamen abweichen.
2. Lesen Sie mit Betriebssystemwerkzeugen Adresse und Präfix, Routen und DNS-Einstellungen. Vergleichen Sie die vom Netzwerkverantwortlichen genehmigte eindeutige Adresse und das Subnetz. Im Labor-VLAN sieht der Gast normalerweise eine ungetaggte Schnittstelle.
3. Lassen Sie Gast- oder Netzwerkadministratoren den vereinbarten Peer und Anwendungsdienst aus genau diesem Gast testen. Notieren Sie DNS-Antworten, verwendete Adressfamilie, Ziel, Protokoll und Port sowie Ergebnis jeweils getrennt.
4. Liefern Tests per Name und Adresse verschiedene Ergebnisse, prüfen Sie DNS und Anwendungs- oder TLS-Identität vor einer Schlussfolgerung. HTTPS an eine reine IP-Adresse kann Zertifikat oder virtuellen Host ändern. Umgehen Sie niemals Zertifikatsprüfungen für eine Erfolgsmeldung.

Ein erfolgreicher Ping belegt keinen funktionierenden Dienst; ein fehlgeschlagener Ping keine Isolation. Testen Sie ausschließlich genehmigte Ziele. Ist Isolation erforderlich, testen Sie auch die vom Verantwortlichen festgelegten verbotenen Ziele.

Ein Peer auf demselben Host testet keinen physischen Uplink. Tests über Hostgrenzen oder außerhalb des Hosts benötigen identifizierte Peers und einen genehmigten Switchpfad. Migrieren Sie keine Arbeitslast für einen improvisierten Test. Bei unerwartetem Produktionszugriff sichern Sie Nachweise und fahren Sie den Testgast normal herunter. Sind Verwaltung oder Speicher betroffen, nutzen Sie vor weiteren Änderungen die getrennte Hostkonsole und den Wiederherstellungsplan des Verantwortlichen.

### 4. Korrektur prüfen {#4-check-the-fix}

1. Geben Sie dem Verantwortlichen genaue Zuordnung, Zeiten, Fehler und Vergleichsergebnisse.
2. Wenden Sie die vereinbarte Korrektur über das passende Gast-, Speicher-, Host- oder Netzwerkverfahren an. Diese Anleitung schreibt kein allgemeines Zurücksetzen vor.
3. Aktualisieren Sie das Inventar. Wiederholen Sie **denselben Diensttest von derselben Quelle zum selben Ziel**.
4. Wiederholen Sie erforderliche Isolationsprüfungen und prüfen Sie Verwaltungs- und Speicherzugriff.
5. Notieren Sie Änderung und Ergebnis.

**Prüfung:** Derselbe Test ist jetzt erfolgreich. Ein grüner Indikator allein bedeutet keine Lösung. Bleibt der Pfad unklar, lassen Sie die Störung offen und [melden Sie ein Problem](#report-a-problem) mit bereinigten Details.

## Fehlgeschlagene NFS-Sicherung diagnostizieren {#backup-failures}

Verwenden Sie dies nur für den [NFS-Vollsicherungsauftrag der Einführung](/docs/xoa-hl/backup-restore/), als XOA-HL-Administrator angemeldet. Sie arbeiten im **Browser**. Speicherprüfungen gehören zum Administrator dieses Speichers. Sie müssen keinen Fehler verursachen.

**Vor dem Beginn**

- Notieren Sie Auftrags- und Zeitplan-IDs, Quell-VM-UUID, Ziel-ID, erwartete Laufzeit samt Zeitzone und Ergebnis der letzten isolierten Wiederherstellung.
- Inkrementelle Ketten, Replikation und Produktionswiederherstellung werden hier nicht behandelt. Weitere Sicherungstests: [Inkrementelle Sicherungen und Kettenwiederherstellung](/docs/xoa-hl/backup-restore/#delta-backups), [eine Datei aus einer Delta-Sicherung](/docs/xoa-hl/backup-restore/#file-restore), [DR-Replik in einem anderen Pool](/docs/xoa-hl/backup-restore/#dr-replica) und [SMB-Ziel auf Windows Server](/docs/xoa-hl/backup-restore/#smb-remote).

### 1. Lauf finden und Details sichern {#1-find-the-run-and-save-its-details}

1. Öffnen Sie **Backup → Overview** (`/#/backup/overview`) und finden Sie den Auftrag. Betrachten Sie die darunterliegende Tabelle **Logs**.
2. Leeren Sie bei Bedarf Protokollsuche und Statusfilter. Finden Sie den Lauf anhand von Auftrag und Startzeit. Die Tabelle kürzt die Auftrags-ID; verwenden Sie deshalb vollständige IDs aus den Details statt nur des Namens.
3. Öffnen Sie die Details über die Statusschaltfläche des Laufs. Notieren Sie `id`, `jobId`, `scheduleId`, Start- und Endzeit sowie Status.
4. Sichern Sie vor Änderungen das JSON privat über Zwischenablageschaltfläche oder **Download log**. Der Download ist nicht bereinigt: Erstellen Sie für Berichte einen bereinigten Auszug.
5. Leeren Sie die Suche in den Details und wählen Sie alle Aufgabenstatus. Anfangs zeigt der Dialog möglicherweise nur ausstehende, fehlgeschlagene oder unterbrochene Aufgaben, fünf pro Seite. Prüfen Sie jede Seite.
6. Finden Sie VM-UUID und danach deren Snapshot-, Ziel-, Export- und Übertragungsaufgaben. Sichern Sie Fehler, Überspringgründe und Warnungen jeder Ebene. Nicht jede rohe Aufgabe wird angezeigt: Lesen Sie bei unvollständigem Baum das gespeicherte JSON.

**Prüfung:** Ihre Notizen identifizieren genau einen Lauf sowie betroffene VM und Sicherungsziel. Fehlende Protokolle oder Aufgaben belegen nicht, dass nichts lief.

### 2. Status vor einem weiteren Versuch lesen {#2-read-the-status-before-you-retry}

| Status (JSON-Wert) | Bedeutung und Prüfung |
| --- | --- |
| Started (`pending`) | Lauf als aktiv erfasst. Aktualisieren und Fortschritt verfolgen. Fehlende Endzeit bedeutet keinen Erfolg. Keinen weiteren Lauf starten. |
| Successful (`success`) | Lauf und erfasste Aufgaben abgeschlossen. Warnungen lesen und neuen Wiederherstellungspunkt prüfen. Wiederherstellung von Gast und Daten gesondert testen. |
| Skipped (`skipped`) | Arbeiten ausgelassen. Grund lesen: Fehler wie `no disks found`, `no VMs match this pattern` und `unhealthy VDI chain` zählen als übersprungen. Dies ist keine neue geprüfte Sicherung. |
| Failed (`failure`) | Lauf oder untergeordnete Aufgabe fehlgeschlagen. Andere Arbeiten können erfolgreich sein: Fehlerphase und tatsächlich vorhandene Sicherungen prüfen. |
| Interrupted (`interrupted`) | Ein Start hat kein passendes Ende; der Server erfasst den Lauf nicht mehr als aktiv. Serverzeitablauf und unvollständige Objekte sichern. Dies belegt weder Zurückrollen noch gefahrloses Wiederholen. |
{.xoa-backup-diagnosis}

### 3. Fehlerphase von erhaltenen Daten trennen {#3-separate-the-failed-stage-from-surviving-data}

Öffnen Sie **Backup → Restore** (`/#/backup/restore`) für Wiederherstellungspunkte und -protokolle.

| Problem | Prüfen |
| --- | --- |
| Kein passender Lauf | Prüfen Sie Protokollfilter, Auftrags- und Zeitplan-IDs, Aktivierungszustand, Zeitzone, Serververfügbarkeit und [gespeicherten Zeitplan](/docs/xoa-hl/backup-restore/#backup-schedules). Nehmen Sie weder nachgeholte verpasste Läufe noch versendete E-Mails an. |
| VM-/Snapshot-Fehler oder übersprungene VM | Prüfen Sie gewählte VM-UUID, Datenträger, Hostverbindung und freien Quell-SR-Platz. Sichern Sie den genauen Grund. Löschen Sie Snapshots nicht und ändern Sie keine VDI-Kette als allgemeine Reparatur. |
| Ziel-, Export- oder Übertragungsfehler | Prüfen Sie mit dem Speicheradministrator NFS-Exporterreichbarkeit von der Appliance, Exportrechte und -optionen sowie freien Zielplatz. Ein erfolgreicher Zieltest belegt weder gesamten Export noch Wiederherstellung. |
| Übertragung funktionierte, danach Lauf fehlgeschlagen | Mit deaktiviertem **Delete first** schreibt diese Vollsicherung Export und Metadaten vor dem Löschen älterer Punkte. Ein neuer Punkt kann daher einen späteren Bereinigungsfehler überstehen. Prüfen Sie Zeiten und aufbewahrte Punkte vor Wiederholung oder Dateilöschung. |
| Punkt fehlt unter Restore | Öffnen und aktualisieren Sie **Backup → Restore**. Prüfen Sie das richtige aktivierte Ziel und Ladefehler. Ein unlesbares Ziel kann in der Liste fehlen: Eine leere Liste belegt keine gelöschten Sicherungen. |
| Wiederherstellung scheiterte | Lesen Sie die Wiederherstellungsprotokolle dieser Seite. Prüfen Sie lesbares Ziel und erreichbares Ziel-SR samt Host. Erfassen Sie unvollständige VMs oder Datenträger per UUID. Behalten Sie Quell-VM und Sicherung; löschen Sie niemals nur nach Namen. |
{.xoa-backup-diagnosis}

**Prüfung:** Sie unterscheiden Fehlerphase, erhaltene Wiederherstellungspunkte und Objekte mit unbekanntem Zustand. Eine Datei oder ein gelisteter Punkt allein belegt keine wiederherstellbaren Daten.

### 4. Ursache beheben und Ergebnis prüfen {#4-fix-the-cause-and-check-the-result}

1. Deaktivieren Sie zum Stoppen künftiger Läufe den genauen Laborzeitplan unter **Overview** und aktualisieren Sie zur Zustandsprüfung. Dies bricht keine laufende Sicherung ab: Die Abbruchschaltfläche unter **Overview** ist in dieser Version deaktiviert. Ein `xo-server`-Neustart bricht eine Sicherung weder ab noch bereinigt er sie.
2. Beheben Sie Zugriffs-, Platz- oder Auswahlproblem mit dem Verantwortlichen. Prüfen Sie danach Auftrag, Zeitplan, VM und Ziel erneut.
3. Lassen Sie **Delete first** aus und behalten Sie benötigte Wiederherstellungskopien außerhalb der Aufbewahrung dieses Auftrags. Ist unklar, ob noch Arbeiten laufen oder wem unvollständige Objekte gehören, sichern Sie Nachweise und holen Sie vor erneutem Versuch Hilfe.
4. Wenn kein Lauf aktiv und der Zustand geklärt ist, starten Sie diesen Ein-VM-Laborauftrag manuell wie in der Einführung. Neustart- und Erzwingen-Schaltflächen im Detaildialog **führen Sicherungen aus**: Sie starten nicht den Gast neu und sind keine lesenden Prüfungen. Erzwingen Sie nichts. Ein weiterer Versuch kann auch Aufbewahrung auf ältere Punkte anwenden.
5. Prüfen Sie neuen Lauf und Wiederherstellungspunkte. [Stellen Sie dann eine angehaltene Kopie wieder her, entfernen Sie jede NIC und prüfen Sie Beispieldaten](/docs/xoa-hl/backup-restore/).
6. Lassen Sie den Laborzeitplan deaktiviert. Notieren Sie vor erneuter Zeitplanaktivierung ursprünglichen Fehler, Korrektur, neue Lauf- und Punkt-IDs sowie Wiederherstellungsergebnis.

**Prüfung:** Neuer Lauf, aufbewahrte Punkte und isolierte Wiederherstellung der Gastdaten sind erfolgreich. Andernfalls lassen Sie die Störung offen und [melden Sie ein Problem](#report-a-problem) mit bereinigten Nachweisen.

## Appliance über ihre Konsole prüfen {#appliance-checks}

Diese Befehle lesen ausschließlich den Zustand. Führen Sie sie innerhalb der Appliance aus, nicht auf dem Hypervisor-Host, über eine autorisierte Konsolen- oder SSH-Sitzung. Einige benötigen Root-Rechte.

```bash
rpm -q xoa-hl nodejs
timedatectl
df -h
systemctl status xo-server redis xoa-hl-update.service --no-pager
systemctl list-timers 'xoa-hl-*'
journalctl -u xo-server -u xoa-hl-check-update.service -u xoa-hl-update.service -u xoa-hl-auto-update.service --since '1 hour ago' --no-pager
tail -n 100 /var/log/xoa-first-boot.log
tail -n 100 /var/lib/xoa-hl/update.log
cat /run/xoa-hl/status
cat /var/lib/xoa-hl/auto-update.status
```

- Eine fehlende Statusdatei vor der ersten Prüfung oder nach einem Neustart ist allein kein Fehler.
- `systemctl status` liefert für eine inaktive oder fehlgeschlagene Unit einen Wert ungleich null. Lesen Sie den angezeigten Zustand.
- Der automatische Updatestatus kann einen älteren Lauf beschreiben. Vergleichen Sie seine UTC-Zeiten.
- Bedeutung der Statuswerte sowie Update- und Neustartentscheidungen beschreibt [Appliance warten und aktualisieren](/docs/xoa-hl/maintenance/).

Löschen Sie weder Datenbankdateien, Protokolle noch Sperren zur Fehlerbeseitigung. Ist der Datenträger voll, identifizieren Sie wachsende Dateien und sichern Sie Nachweise, bevor Sie über Bereinigung entscheiden.

## Administratorzugriff wiederherstellen {#recover-admin-access}

Verwenden Sie dies, wenn kein Administrator sich anmelden kann: Passwort oder Einmalcode-Gerät verloren oder LDAP-/SAML-Anmeldung defekt. Sie führen einen Wiederherstellungsbefehl **innerhalb der Appliance** als root über deren Konsole oder SSH aus. Jeder mit Root-Zugriff auf die Appliance kann damit ein XO-Konto übernehmen; schützen Sie daher diesen Zugriff.

Der Befehl ändert das benannte Konto:

- Er setzt ein neues Passwort.
- Er entfernt den Einmalcode des Kontos.
- Er macht das Konto zu einem **Admin**.
- Er entfernt LDAP- oder SAML-Verknüpfungen, sodass das Konto lokal wird.
- Er behält andere Kontoeinstellungen und bestehende Authentifizierungstoken.

Existiert der Name nicht, erstellt der Befehl einen neuen lokalen Administrator.

1. Öffnen Sie die Appliance-Konsole aus XO Lite oder eine SSH-Sitzung und werden Sie root.
2. Prüfen Sie die laufende Datenbank: `systemctl is-active redis` gibt `active` aus.
3. Führen Sie den Befehl mit dem genauen Kontobenutzernamen aus, gewöhnlich einer E-Mail-Adresse. Sie müssen `xo-server` nicht stoppen.

   ```bash
   node /opt/xo/packages/xo-server/dist/recover-account-cli.mjs admin@example.net
   ```

4. Geben Sie bei `Password (leave empty for random):` das neue Passwort ein und drücken Sie Enter. Es wird nicht angezeigt. Lassen Sie die Eingabe leer, gibt der Befehl ein Zufallspasswort aus: Speichern Sie es im Passwortmanager und leeren Sie anschließend den Bildschirm. Geben Sie das Passwort nicht auf der Befehlszeile an; dort bliebe es im Shellverlauf.
5. Warten Sie auf `user admin@example.net has been successfully updated`. Bei `created` entsprach der Name keinem bestehenden Konto. Prüfen Sie nach der Anmeldung den Namen unter **Settings → Users** und löschen Sie das zusätzliche Konto, falls unnötig.
6. Melden Sie sich in einem neuen privaten Browserfenster mit Konto und neuem Passwort an. Kein Einmalcode wird verlangt.
7. Lesen Sie auf Ihrer Benutzerseite **Authentication tokens**. Bei verlorenem Gerät oder Passwort wählen Sie **Forget all authentication tokens**. Es entfernt alle Token außer dem Ihrer aktuellen Sitzung.
8. Verwendete das Konto einen Einmalcode, [richten Sie ihn erneut ein](/docs/xoa-hl/sign-in-otp/) auf einem von Ihnen kontrollierten Gerät. Bei zuvor genutztem LDAP oder SAML ist es jetzt lokal: Behalten Sie es als lokalen Wiederherstellungsadministrator oder fragen Sie vor erneutem Verknüpfen den Identitätsverantwortlichen.

**Prüfung:** Anmeldung mit neuem Passwort funktioniert, **Settings → Users** listet **Admin**, die Spalte **OTP** zeigt **Not configured**, und nur erwartete Token bleiben.

| Problem | Prüfen |
| --- | --- |
| `node: command not found` oder `Cannot find module` | Führen Sie `rpm -q xoa-hl nodejs` aus und prüfen Sie die vorhandene Befehlsdatei. Verwenden Sie genau den gezeigten Pfad. |
| Befehl wartet endlos oder meldet Redis-Fehler | Führen Sie die [Konsolenprüfungen](#appliance-checks) für `redis` und freien Platz aus. Löschen Sie keine Datenbankdateien. |
| Anmeldung scheitert weiterhin | Prüfen Sie den genau ausgegebenen Benutzernamen, verwenden Sie ein neues privates Fenster und lesen Sie `journalctl -u xo-server --since '15 min ago'`. |

## Häufige Fragen {#common-questions}

**Warum ließ die Hostwartung VMs zurück oder den Host deaktiviert?** Sichern Sie die Aufgabe. Prüfen Sie dann tatsächlichen Aktivierungszustand und Ausführungsort jeder VM. Der [Hostwartungstest](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) behandelt Evakuierung und Reaktivierung getrennt. Teilweise Evakuierung oder früher Fehler benötigen den Wiederherstellungsplan des Hostverantwortlichen. Umgehen Sie keine Migrationssperren und wiederholen Sie Schalterwechsel nicht blind.

**Warum trat ein Host dem Pool nicht bei?** Sichern Sie Aufgabe, Fehler und Inventare beider Pools. Der [Poolbeitrittstest](/docs/xoa-hl/hosts-pools/#pool-join) prüft genaue IDs, Patchunterschiede, Master, Netzwerke und Speicher vor Bestätigung. Die Oberfläche führt einen erzwungenen Beitritt aus: Wiederholen Sie ihn nicht und werfen Sie keinen Host aus, um einen ungeklärten Fehler zu beseitigen.

**Warum wurde delegierte VM-Erstellung verweigert?** Folgen Sie dem [Ressourcenmengen- und Kontingenttest](/docs/xoa-hl/permissions/#resource-set-delegation). Vergleichen Sie genauen Benutzer, gewählte Menge, Vorlagen-, SR- und Netzwerk-IDs sowie Kontingent Used/Total. Eine sichtbare Vorlage oder Schaltfläche belegt keine serverseitige Erlaubnis. Sichern Sie den Fehler und suchen Sie unvollständige VMs oder Datenträger vor erneutem Versuch. Erhöhen Sie weder Kontingente noch vergeben Sie Pool-Admin zur Beseitigung ungeklärter Fehler.

**Warum sind Updates gelistet, während der Prüfbefehl 100 zurückgibt?** Der paketierte Prüfer übersetzt `dnf check-update`-Rückgabecode 100 zu `AVAILABLE`, 0 zu `UP_TO_DATE` und alle anderen zu `ERROR`. Gelistete Updates sind keine fehlgeschlagene Installation.

**Macht der Wechsel zu Stable ein Testing-Update rückgängig?** Nein. Der Kanal bestimmt Repositories für spätere Prüfungen und Installationen. Der Wechsel zu Stable stuft keine bereits installierte Version zurück.

**Belegt eine Pool-Metadatensicherung die Wiederherstellbarkeit eines Hosts?** Nein. Der [Pool-Metadatentest](/docs/xoa-hl/configuration-backup/#pool-metadata) prüft nur Export, Aufbewahrung und Dateiidentität. Wiederherstellung auf einem isolierten Testpool wird noch nicht behandelt.

**Kann ein Konfigurationsexport VM-Sicherung oder Appliance-Rollback ersetzen?** Nein. Lesen Sie [Konfigurationsumfang und Wiederherstellungsgrenzen](/docs/xoa-hl/configuration-backup/) und behalten Sie getrennte Gastsicherungen.

## Problem melden {#report-a-problem}

[Öffnen Sie ein XCP-HL-Issue](https://github.com/Vagrantin/xcp-hl/issues/new). Geben Sie als Text an:

- Seiten-URL und Sprache oder Appliance-Route des Problems.
- Image-Tag, Versionen unter **About**, installierte RPM- und Node-Versionen sowie Stable- oder Testing-Kanal.
- Vorgang, genaue Schritte, erwartetes Ergebnis und tatsächlichen Fehler.
- Zeitpunkt samt Zeitzone, manuellen oder automatischen Modus, zugehörigen Dienstzustand und bereinigten Protokollauszug.
- Wiederholbarkeit auf einer entbehrlichen Appliance und letzte funktionierende Version.

Entfernen Sie Passwörter, Token, Cookies, private Hostnamen und Adressen sowie Benutzer- und Gastdaten aus Protokollen und Bildschirmfotos. `xo-server`- und Erststartprotokolle können Zugangsdaten enthalten. Hängen Sie niemals Konfigurationsexport, privaten TLS-Schlüssel oder vollständige Konfigurationsdatei an. Behalten Sie Originalnachweise privat.

{{< details title="Quellen" closed="true" >}}
- **Versionsverhalten**: [Updatezeitplanung](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md), [Prüfrückgabecodes](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh), [Serverdienst](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [Erststartbereitstellung](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh).
- **Sicherungsdiagnose**: [Übersicht und Laufdetails](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js), [Aufgabenfilter, Seiten und Anzeige](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js), [Rohprotokoll und Neustartschaltflächen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js), [Statusberechnung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/backups-ng-logs.mjs), [Vollständiger Export und Bereinigungsreihenfolge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [Ziellistenfehler und Wiederherstellungsprotokolle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js).
- **Netzwerkdiagnose**: [VM-Netzwerkansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [Hostnetzwerkansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [Poolnetzwerkansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [PIF-Carrier-Anzeige](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [Gastmetriken und Schnittstellenzuordnung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [Serververbindungszustand](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js).
- **Administratorwiederherstellung**: [Wiederherstellungsbefehl](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [Kontoaktualisierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [Installierter Pfad und Konfiguration](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
{{< /details >}}
