---
title: "Anmelden, einen Host verbinden und eine Sprache wählen"
linkTitle: "Erste Anmeldung"
description: "Bei XOA-HL anmelden, das Passwort festlegen, die Oberflächensprache wählen und den Host verbinden."
weight: 10
translationKey: xoa-manual-first-login
translationStatus: reviewed
sourceRevision: sha256:fada0c60468337a6ff9bac62459262ad822b14b101201fd2ccba51590aa4909a
glossaryTerms: ["appliance", "host", "pool", "vm", "xo-lite"]
---

Nach dieser Anleitung können Sie sich bei XOA-HL anmelden, Ihr Host ist verbunden und die Oberfläche verwendet Ihre Sprache.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261027-ca44911`, Paket `v5.113.2_e281c536-ce47` (Xen Orchestra 5.113.2). Am 27.10.2026 auf einer Labor-Appliance getestet. Ältere Images und spätere Updates können abweichen. Am 27.10.2026 mit der Bereitstellungskorrektur in `build-xoa-hl@fa0c987` neu erstellt. Siehe [So erkennen Sie die korrigierte Datei](/docs/xoa-hl/first-login/#identify-the-rebuilt-image).
{{< /callout >}}

Dieser Anmeldeweg setzt das Bereitstellungsformular von XO Lite voraus. Eine direkte RPM-Installation auf AlmaLinux ist ein anderes Artefakt: Die ce51-Labor-Appliance stellte vor der Bereitstellung durch den Betreiber ein Standard-Administratorkonto bereit ([#368](https://github.com/Vagrantin/xcp-hl/issues/368)). Halten Sie diesen Endpunkt isoliert und richten Sie eindeutige Administrator-Zugangsdaten ein, bevor Sie Verwaltungszugriff erlauben. Die Zugangsdatenschritte des Bereitstellungsformulars unten gelten nicht für diese RPM-Installation.

## Vor dem Beginn {#before-you-begin}

- [Stellen Sie XOA-HL über XO Lite bereit](/docs/start/#start-deploy-xoa). Notieren Sie Image-Tag und Appliance-Adresse.
- Bewahren Sie Benutzername und Passwort des XO-Administrators aus dem Bereitstellungsformular auf. Sie benötigen außerdem die Host-Verwaltungsadresse und das `root`-Passwort des Hosts.
- Verwenden Sie einen Browser in einem vertrauenswürdigen Verwaltungsnetzwerk.

Die meisten Schritte laufen in Ihrem **Browser**. Die Image-Prüfung verwendet eine Root-Shell in der Appliance. Die Bereinigung älterer oder unvollständiger Bereitstellungen verwendet eine Root-Shell auf dem Host.

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
Bei Images, die vor der Bereitstellungskorrektur vom 27.10.2026 erstellt wurden, kann ein fehlgeschlagener erster Start das Webkonto bei `admin@admin.net` mit dem Passwort `admin` belassen. Versuchen Sie es nur in einem vertrauenswürdigen Netzwerk und ändern Sie dann sofort sein Passwort. Verwenden Sie beim neu erstellten Image Ihr Bereitstellungskonto. Schlägt es fehl, prüfen Sie die unten beschriebenen Bereitstellungsdienste. Gehen Sie nicht davon aus, dass das Standardkonto funktionieren sollte.
{{< /callout >}}

## 2. Dauerhaftes Passwort festlegen {#2-set-a-password-you-will-keep}

1. Wählen Sie das **Benutzersymbol** im Menü, um **User** (`/#/user`) zu öffnen.
2. Geben Sie im Passwortbereich das aktuelle und anschließend zweimal das neue Passwort ein. Verwenden Sie ein einzigartiges Passwort. Wählen Sie **OK**.
3. Bewahren Sie das neue Passwort sicher auf. Melden Sie sich ab und mit dem neuen Passwort wieder an.

**Prüfung:** Sie können sich mit dem neuen Passwort anmelden. Nur das Webkonto wird geändert. Das `root`-Passwort des Hosts und das SSH-Passwort der Appliance bleiben unverändert.

{{< callout type="warning" >}}
Diese Probleme betreffen Images, die vor der Bereitstellungskorrektur vom 27.10.2026 erstellt wurden, darunter `qa-xoa-build-58.xva` (SHA-256 beginnt mit `5f8427fd`). Sie beschreiben keine erfolgreiche Bereitstellung des unten identifizierten neu erstellten Images:

- **Starten Sie die Appliance einmal neu.** Starten Sie die Appliance-VM nach der Passwortänderung normal aus XO Lite neu (**Restart**, kein erzwungener Neustart). Solange die Appliance ihre Einstellungen nicht gespeichert hat, können ein Stromausfall oder ein erzwungenes Anhalten das Konto `admin@admin.net` mit dem Passwort `admin` zurückbringen, und Ihr eigenes Konto geht verloren. Aus demselben Grund sollten Sie nie einen Snapshot einer laufenden Appliance als bekannten guten Zustand behalten.
- **Entfernen Sie die von der Bereitstellung hinterlassenen Zugangsdaten.** Die VM-Einstellungen auf dem Host können Bereitstellungs-Zugangsdaten im Klartext enthalten. Verwenden Sie nach der Zugriffsprüfung das Bereinigungsverfahren unten, ändern Sie dann das Webpasswort und, falls SSH aktiviert ist, das SSH-Passwort von `xo` mit `passwd`.
{{< /callout >}}

### Neu erstelltes Image erkennen {#identify-the-rebuilt-image}

Die korrigierte Datei ist `qa-xoa-build-59.xva` in der Veröffentlichung `xoa-image-20261027-ca44911`. Ihre SHA-256-Prüfsumme lautet `cc20b9398d5ab0dc03eae6706d3b54236e2d245fa1d0dd1232d59836387057aa`. Sie wurde aus `build-xoa-hl@fa0c987` erstellt. Die frühere Datei verwendete dasselbe Tag und dieselben Versionsangaben unter About.

Führen Sie in der Appliance diese rein lesende Prüfung als **root** aus, über ihre Konsole oder eine autorisierte SSH-Sitzung:

```bash
redis-cli config get appendonly
```

Beim neu erstellten Image lautet das Ergebnis `appendonly`, gefolgt von `yes`. Das vorherige Image gibt `no` zurück. Geprüft wird die aktuelle Einstellung von Redis. Ein manuell geändertes oder eigenes Image kann ebenfalls `yes` zurückgeben; behalten Sie den ursprünglichen Dateinamen und die Prüfsumme als Identität des Images.

Das neu erstellte Image speichert das Bereitstellungskonto, bevor es die Einrichtung als abgeschlossen markiert. Spätere Änderungen verwenden die Append-only-Datei (AOF) von Redis, die jede Sekunde gespeichert wird. Ein erzwungenes Anhalten kann trotzdem etwa die letzte Sekunde an Änderungen verlieren. Verwenden Sie für einen Basis-Snapshot eine normal heruntergefahrene Appliance.

### Ältere oder unvollständige Bereitstellungen bereinigen {#clean-up-older-or-incomplete-deployments}

Warten Sie vor dem Entfernen von Schlüsseln, bis die Appliance die Konten übernommen hat und Sie sich sowohl mit den vorgesehenen Web-Zugangsdaten als auch, falls aktiviert, mit den SSH-Zugangsdaten anmelden können. Verwenden Sie die genaue UUID der Appliance-VM. Prüfen Sie in einer **Root-Shell auf dem XCP-HL-Host** jeden Schlüssel einzeln, ohne seinen Wert anzuzeigen:

```bash
for key in admin-account system-account-xoa-password xoa-updater-credentials; do
  if xe vm-param-get uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key" >/dev/null 2>&1; then
    xe vm-param-remove uuid=<appliance-vm-uuid> param-name=xenstore-data param-key="vm-data/$key"
  fi
done
```

Ein fehlender Schlüssel ist zu erwarten; untersuchen Sie jeden Fehler beim Entfernen. Geben Sie nicht die gesamte Map `xenstore-data` in ein Protokoll oder einen Bericht aus. Alte Protokolle des ersten Starts, VM-Exporte und Sicherungen der Pool-Metadaten können die Bereitstellungspasswörter weiterhin enthalten. Ändern Sie die bei der Bereitstellung angegebenen Web- und SSH-Passwörter und schützen Sie diese älteren Kopien oder sondern Sie sie aus. Das Entfernen der aktuellen Schlüssel löscht keine historischen Kopien.

Lassen Sie den Bereitstellungs-Tab von XO Lite geöffnet, bis er fertig ist. Beim neu erstellten Image entfernte die Bereinigung im Gast nach dem ersten Start auch `vm-data/admin-account` und `vm-data/system-account-xoa-password` aus dem persistenten `xenstore-data` von XAPI. Das wurde auf einem XCP-HL-v8.3-Host in [#311](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771) beobachtet. Gehen Sie nicht vom selben Ergebnis bei älteren Images, Images von Vates oder Ronivay, eigenen Images oder fehlgeschlagenen bzw. abgebrochenen Bereitstellungen aus. Prüfen und entfernen Sie verbleibende Schlüssel auf dem Host wie oben, nachdem die Konten übernommen wurden. Die Bereinigungskorrektur von XO Lite in [#310](https://github.com/Vagrantin/xcp-hl/issues/310) deckt auch andere Image-Quellen ab. Ein reines RPM-Update der Anwendung ersetzt die Bereitstellungsskripte in einem älteren Image nicht.

Bei Images, die mit den Korrekturen aus #310/#311 neu erstellt wurden, verhindert eine fehlgeschlagene Erfassung beim ersten Start absichtlich die Netzwerkverbindung; XO Lite meldet dann möglicherweise "XOA not responding" ohne IP-Adresse. Prüfen Sie an der VM-Konsole `systemctl status xoa-first-boot.service` und `/var/log/xoa-first-boot.log`. Diese Images benötigen von XO Lite eine vollständige Administrator-E-Mail-Adresse und ein Passwort; ein Import der XVA ohne diese Daten wird nicht stillschweigend akzeptiert. Korrigieren Sie die Bereitstellungsdaten vor dem Neustart, und behalten Sie die Zugangsdatenschlüssel, bis die Erfassung erfolgreich ist. War die Erfassung erfolgreich, wurden die Zugangsdaten aber nicht angewendet, prüfen Sie `systemctl status xoa-credentials.service` und starten Sie diesen Dienst nach Behebung der Ursache erneut. Kopieren Sie die nur für root lesbare Datei `/etc/xoa-first-boot.env` nicht in Berichte.

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

Öffnen Sie als Administrator **About** (`/#/about`). Notieren Sie **XOA-HL version** und **XOA-HL VM version** zusammen mit dem ursprünglichen Dateinamen, der Prüfsumme und dem Image-Tag. Die beiden Dateien vom 27.10.2026 haben dieselben Versionsangaben unter About. Unterscheiden Sie ihre Redis-Standardeinstellungen mit der Image-Prüfung oben. Paketupdates können später die Anwendungsversion ändern.

Die [Versionsmatrix](/docs/reference/release-matrix/) nennt den Lieferumfang jeder Veröffentlichung. Sie zeichnet keine Testergebnisse auf.

## Bei Problemen {#if-something-goes-wrong}

| Problem | Prüfung |
| --- | --- |
| Die Appliance-Seite öffnet sich nicht | In XO Lite prüfen, dass die Appliance-VM läuft. Adresse, Netzwerk, Gateway und Browser-Erreichbarkeit prüfen. Nicht erneut über eine funktionierende VM bereitstellen. |
| Die Zugangsdaten aus der Bereitstellung funktionieren nicht | Abschluss des ersten Starts abwarten und prüfen, dass das Webkonto verwendet wurde. Beim neu erstellten Image die oben beschriebenen Bereitstellungsdienste prüfen. Bei einem älteren Image das Ersatzkonto nur in einem vertrauenswürdigen Netzwerk versuchen. Nach einem frühen erzwungenen Anhalten kann ein älteres Image Ihr Konto verloren haben: Passwort des Ersatzkontos ändern, dann Ihr Konto neu anlegen. `/var/log/xoa-first-boot.log` über eine autorisierte Konsole oder SSH-Sitzung lesen. Private Daten vor dem Weitergeben entfernen. |
| Die Anmeldung beim Host schlägt fehl | Host-Adresse und dessen `root`-Passwort prüfen. Das Passwort des Webadministrators ist ein anderes. |
| Der Server zeigt einen Zertifikatsfehler | Host-Identität prüfen, bevor sein selbstsigniertes Zertifikat akzeptiert wird. Keine unerklärte Änderung akzeptieren. |
| Der Server ist aktiviert, aber das Inventar leer | Verbindungsfehler lesen. Prüfen, dass die Appliance den Host erreicht und die Host-Adresse stimmt. Die Erreichbarkeit im Browser beweist nicht die Erreichbarkeit von der Appliance aus. |

## Nächste Schritte {#next-steps}

[Erste VM erstellen](/docs/xoa-hl/create-vm/) oder die [Update-Anleitung für Appliance und Host](/docs/guides/updates/) lesen.

{{< details title="Quellen" closed="true" >}}
Abgeglichen mit: [Image-Veröffentlichung](https://github.com/Vagrantin/build-xoa-hl/releases/tag/xoa-image-20261027-ca44911); [Einrichtung der Zugangsdaten in build-xoa-hl@fa0c987](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-credentials.sh); [Benutzeransicht in XO@e281c536](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/user/index.js); [Serveransicht derselben Version](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js); [XOA-HL-About-Seitenpatch in xoa-hl@a280852](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzz-xoa-hl-about-page.patch).
- [build-xoa-hl@fa0c987: AOF](https://github.com/Vagrantin/build-xoa-hl/blob/fa0c987e320603daec822d19b0df71255f5c6c9c/scripts/xoa-finalize-state.sh)
- [#311: 27.10.2026](https://github.com/Vagrantin/xcp-hl/issues/311#issuecomment-6439980771)
{{< /details >}}
