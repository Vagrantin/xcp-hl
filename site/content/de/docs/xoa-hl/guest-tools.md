---
title: "Linux-Gastwerkzeuge installieren"
linkTitle: "Gastwerkzeuge"
description: "Verwaltungsagenten in einer Linux-Gast-VM installieren und die Anzeigen von XOA-HL prüfen."
weight: 41
translationKey: xoa-manual-guest-tools
translationStatus: draft
sourceRevision: sha256:b33c81ebb5d81c67bc786f64145b80c80a063e3836134f53b46590995ecf327e
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Installieren Sie den Verwaltungsagenten innerhalb einer Linux-Gast-VM, prüfen Sie die Anzeigen von XOA-HL und testen Sie ein sauberes Herunterfahren. Der Agent läuft im Gast, nicht in XOA-HL. Als Beispiel dient ein Ubuntu-24.04-Gast, weil dessen Paket geprüft wurde; andere Linux-Distributionen stellen den Agenten über eigene Pakete bereit. Sie verwenden die **XOA-HL-Appliance** als Administrator im Browser und führen Befehle in der Gastkonsole aus. Arbeiten Sie die Abschnitte der Reihe nach durch. Andere Systeme, einschließlich Windows, benötigen eigene Verfahren.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Gastpaket: `xe-guest-utilities` `7.20.2-0ubuntu1` für Ubuntu 24.04 LTS (Noble), amd64.
{{< /callout >}}

## Vor dem Beginn {#before-you-begin}

- Verwenden Sie eine frisch installierte Ubuntu-24.04-amd64-Test-VM ohne wertvolle Daten, beispielsweise aus [Erste VM erstellen](/docs/xoa-hl/create-vm/). Sie benötigen eine funktionierende Konsole und ein Gastkonto mit `sudo`-Rechten.
- Notieren Sie vollständige VM-UUID, Host, Gastbetriebssystem und Kernel sowie installierte Host- und Appliance-Versionen. Ein Vorlagenname allein nennt nicht das installierte Betriebssystem.
- Verwenden Sie ein XOA-HL-Administratorkonto. Starten und Stoppen einer VM erfordern die Berechtigung **operate** auf ihr. Die Paketverwaltung im Gast ist ein separates Recht: Eine XOA-HL-Anmeldung verleiht kein `sudo` im Gast.
- Planen Sie ein Wartungsfenster für den Herunterfahrtest. Speichern Sie die Arbeit im Gast und nehmen Sie die VM aus geplanten Jobs. Bevor Sie einen wichtigen Gast ändern, erstellen Sie eine unabhängige [Sicherung und testen eine isolierte Wiederherstellung](/docs/xoa-hl/backup-restore/).
- Der Gast benötigt funktionierendes DNS, richtige Uhrzeit und Zugriff auf seine genehmigten Ubuntu-Noble-Repositories einschließlich `universe`. Verwenden Sie ein genehmigtes Labornetz. Ändern Sie nicht das Host-Verwaltungsnetz zum Erreichen eines Paketspiegels. Diese Anleitung fügt keine Repositories hinzu und verwendet kein Tools-ISO.

Führen Sie die Shell-Befehle dieser Seite ausschließlich **in der Gastkonsole** aus, niemals auf dem XCP-HL-Host oder der XOA-HL-Appliance. Lesen Sie den VM-Status und verwenden Sie ihre Stromschaltflächen im **Browser** unter der Appliance-Adresse.

## Status der Gastwerkzeuge prüfen {#guest-tools-status}

1. Öffnen Sie im Browser die VM mit der notierten UUID und prüfen Sie den Zustand **Running**.
2. Öffnen Sie **General** (`/#/vms/<id>/general`). Notieren Sie Virtualisierungsmodus, Werkzeugmeldung und angezeigte IP-Adresse.
3. Öffnen Sie **Advanced** und suchen Sie **Guest OS**. Notieren Sie **Management agent version**, **OS name** und **OS kernel**. Ändern Sie auf diesen Reitern nichts.
4. Führen Sie in der VM-Konsole diese Befehle aus und notieren Sie die Ausgabe:

   ```bash
   cat /etc/os-release
   uname -r
   dpkg --print-architecture
   systemd-detect-virt
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl status xe-daemon.service --no-pager
   ```

   Ein fehlendes Paket oder ein inaktiver Dienst ist ein festzuhaltendes Ergebnis, kein Grund, die Befehle auf einer anderen Maschine auszuführen.

**Prüfung:** Das Betriebssystem ist Ubuntu `24.04`, die Architektur `amd64`, und `systemd-detect-virt` gibt `xen` aus. Andernfalls halten Sie an und verwenden ein für dieses System geschriebenes Verfahren. Sind die Werkzeuge bereits installiert, notieren Sie Paketquelle und -version und gehen zu [Anzeigen von XOA-HL prüfen](#check-reporting). Installieren oder aktualisieren Sie sie nicht nur, um diesem Beispiel zu entsprechen.

### Bedeutung der Werkzeugmeldung {#what-the-tools-message-means}

Die Meldung unter **General** erscheint nur bei einer VM im Zustand **Running**, wenn XO Treiberinformationen besitzt. XO prüft zuerst die PV-Treiber, dann den Verwaltungsagenten und anschließend dessen Aktualität. Es zeigt die erste zutreffende Meldung:

| Meldung | Bedeutung |
| --- | --- |
| **No Xen tools detected** | Die PV-Treiber werden nicht erkannt |
| **Management agent not detected** | Die Treiber werden erkannt, der Agent jedoch nicht |
| **Management agent {version} out of date** | Der Agent wird erkannt, aber als veraltet gemeldet |
| **Management agent {version} detected** | Der Agent wird erkannt und als aktuell gemeldet |

Eine fehlende Meldung beweist keine installierten Werkzeuge. Ein erkannter Agent prüft weder Anwendungen, Konnektivität noch Sicherheit.

Die PV-Treiber im Linux-Kernel und der Verwaltungsagent (ein Programm im Gast) erfüllen unterschiedliche Aufgaben. Das folgende Ubuntu-Paket installiert den Agenten und ersetzt keine Kernel-Treiber. Die Agentversion in XO stammt aus den Gastmetriken des Hosts und kann von der Ubuntu-Paketversion abweichen. Notieren Sie beide. Führen Sie nicht allein wegen unterschiedlicher Schreibweisen ein Downgrade oder eine Neuinstallation durch. Prüfen Sie Treiber, Agenten und Anwendungen getrennt.

## Verwaltungsagenten in einem Linux-Gast installieren {#install-linux-agent}

Verwenden Sie einen Gast ohne installierte Werkzeuge. Wird bereits ein Tools-ISO, Herstelleragent oder anderes Paket verwendet, klären Sie zuerst Zuständigkeit und Upgrade-Verfahren.

1. Aktualisieren Sie in der Gastkonsole die Paketlisten, prüfen Sie die vorgesehene Paketquelle und simulieren Sie die Installation:

   ```bash
   sudo apt-get update
   apt-cache policy xe-guest-utilities
   apt-get -s install xe-guest-utilities
   ```

2. Prüfen Sie, dass der Kandidat aus dem erwarteten Ubuntu-Noble-Repository stammt. Diese Anleitung wurde gegen Version `7.20.2-0ubuntu1` geprüft. Bewerten Sie jede andere Version oder Quelle, bevor Sie fortfahren.
3. Halten Sie bei Repository- oder Signaturfehlern, fehlendem Kandidaten oder unerwarteten Entfernungen beziehungsweise Upgrades an. Umgehen Sie keine Prüfung und fügen Sie kein fremdes Repository hinzu.
4. Installieren Sie das Paket. Lesen Sie die vorgeschlagenen Änderungen, bevor Sie zustimmen:

   ```bash
   sudo apt-get install xe-guest-utilities
   ```

5. Aktivieren und starten Sie den Dienst und prüfen Sie Paket und Dienst:

   ```bash
   sudo systemctl enable --now xe-daemon.service
   dpkg-query -W -f='${Package} ${Version} ${Status}\n' xe-guest-utilities
   systemctl is-enabled xe-daemon.service
   systemctl is-active xe-daemon.service
   ```

**Prüfung:** Der Paketstatus lautet `install ok installed`, der Dienst ist `enabled` und `active`. Unter Ubuntu Noble heißt der Dienst **`xe-daemon.service`**. Er hängt von `proc-xen.mount` ab und systemd startet ihn nur, wenn seine Xen-Virtualisierungs- und Pfadbedingungen erfüllt sind. Verwenden Sie nicht stattdessen den generischen Namen `xe-linux-distribution.service`. Ein abgeschlossener Installer oder aktivierter Dienst allein beweist keinen laufenden Agenten. Dieser Schritt benötigt keinen Neustart und entfernt kein Paket.

## Anzeigen von XOA-HL prüfen {#check-reporting}

1. Aktualisieren Sie im Browser **General** und **Advanced** derselben laufenden VM. Notieren Sie Werkzeugmeldung, Agentversion, Betriebssystem und Kernel.
2. Vergleichen Sie Betriebssystem und Kernel mit den Ausgaben der Gastkonsole.
3. Vergleichen Sie die angezeigte IP-Adresse mit der vorgesehenen Gastschnittstelle und ihrer aktuellen Adresse.

Wird der Agent weiterhin als fehlend oder veraltet gemeldet, obwohl `systemctl` `active` ausgibt, ist das Problem nicht behoben. Notieren Sie die genaue Anzeige und werten Sie den Test nicht als bestanden.

**No IPv4 record** allein beweist keinen Agentenausfall: Ein Gast nur mit IPv6 oder ohne Netzwerk besitzt möglicherweise keine IPv4-Adresse. Eine angezeigte Adresse beweist weder Routing, DNS noch SSH- oder RDP-Zugriff. Prüfen Sie die vom Gast benötigten Verbindungen getrennt.

## Sauberes Herunterfahren testen {#clean-shutdown}

1. Speichern Sie alle Arbeiten im Gast.
2. Prüfen Sie im Browser die VM-UUID erneut. Wählen Sie einmal **Stop** und lesen Sie die Bestätigung.
3. Bietet XO erzwungenes Herunterfahren oder das Umgehen einer blockierten Operation an, brechen Sie ab: Das ist kein sauberes Herunterfahren. Notieren Sie den Fehler. Reagiert der Gast noch, fahren Sie ihn aus dem Gast regulär herunter. Wiederholen Sie die Anforderung nicht während einer laufenden Aufgabe.
4. Prüfen Sie in der Konsole das Herunterfahren des Gasts und in XOA-HL den Zustand **Halted**, ohne noch laufende Stopp-Aufgabe.
5. Wählen Sie einmal **Start**. Melden Sie sich über die Konsole an und prüfen Sie Anwendung oder Testdatei.
6. Wiederholen Sie Dienstprüfungen (`systemctl is-enabled` und `systemctl is-active`) sowie [Anzeigen von XOA-HL prüfen](#check-reporting).

Notieren Sie Herunterfahr- und Startergebnisse getrennt von der Agentenerkennung: Das eine beweist nicht das andere.

**Prüfung:** Sie haben für jeden Punkt ein Ergebnis: genaues Paket und Dienst, aktualisierte XOA-HL-Anzeige, sauberes Herunterfahren und Dienst nach dem Neustart. Fehlt ein Ergebnis oder schlägt es fehl, ist der Test unvollständig. Live-Migration, dynamischer Arbeitsspeicher, Hotplug, quiescierte Snapshots, Zwischenablage und Leistung werden damit nicht getestet.

## Bei Problemen {#if-something-goes-wrong}

| Problem | Prüfung |
| --- | --- |
| Das Paket fehlt oder stammt aus unerwarteter Quelle | Gastbetriebssystem und -version, `apt-cache policy`, Verfügbarkeit des genehmigten `universe`-Repositorys, Uhrzeit, DNS und Update-Fehler prüfen. Repository mit seinem Verantwortlichen korrigieren. Kein Host- oder Appliance-Paket im Gast installieren. |
| Der Dienst fehlt, ist inaktiv oder fehlgeschlagen | Installiertes Paket und Dateien mit `dpkg -L xe-guest-utilities` prüfen. `systemctl status xe-daemon.service proc-xen.mount --no-pager` sowie `sudo journalctl -u xe-daemon.service -u proc-xen.mount -b --no-pager` lesen. Xen-Bedingungen und Abhängigkeitsfehler vor Konfigurationsänderungen prüfen. |
| Der Dienst ist aktiv, aber XO meldet einen fehlenden oder veralteten Agenten | VM-Identität, Zustand **Running** und Host-Verbindung prüfen. Paket- und Dienstergebnisse des Gasts mit **General** und **Advanced** samt jeweiliger Uhrzeit vergleichen. Nicht blind den Hypervisor neu starten, die Warnung ausblenden oder Treiber ersetzen. |
| **Stop** scheitert oder bietet Erzwingen an | Erzwingen oder Umgehung abbrechen. Genauen Aufgabenfehler festhalten und Gastkonsole prüfen. Wenn möglich aus dem Gast herunterfahren. Erzwungenes Ausschalten kann Daten verlieren und benötigt eine separate Entscheidung. |
| Der Gast fällt nach einer Änderung aus | Paketverlauf, Start- und Dienstprotokolle aufbewahren. Gastkonsole und separaten Wiederherstellungsplan verwenden. Diese Anleitung verspricht keine automatische Rücknahme durch Deinstallation oder Downgrade. |

Aktivieren, starten oder installieren Sie nicht ständig neu, um einen ungeklärten Fehler zu verbergen. [Melden Sie das Problem](/docs/xoa-hl/troubleshooting/#report-a-problem) mit Versionen, VM-/Host-IDs, Zeiten, Paketquelle und -version, Dienstzustand, genauen Meldungen und Ergebnissen der Stromaktionen. Protokolle und Gastansichten können private Namen, Adressen oder Daten enthalten: Lassen Sie diese im Bericht weg und halten Sie Rohbelege privat.

Planen Sie für spätere Updates ein eigenes Wartungsfenster für Gastbetriebssystem und Pakete und wiederholen Sie dieselben Prüfungen. Nicht behandelt: andere Linux-Distributionen, Tools-ISO-Installation, Windows- oder BSD-Werkzeuge, Herstellerwechsel, Paketupgrade oder -entfernung und eine Liste unterstützter Gäste. Als Nächstes siehe [VMs verwalten](/docs/xoa-hl/vm-operations/) und [VM sichern und wiederherstellen](/docs/xoa-hl/backup-restore/).

{{< details title="Quellen" closed="true" >}}
- **Werkzeugstatus und Stromaktionen**: [Reihenfolge der Werkzeugmeldungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [Felder zum Gastbetriebssystem](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [Zuordnung der Gastmetriken](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [Stopp- und Erzwingen-Bestätigungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM-Berechtigung operate](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **HomeLab-Build**: [Patch-Auswahl in xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Ubuntu-Paket (am 2026-10-15 geprüft)**: [Paket `7.20.2-0ubuntu1`](https://packages.ubuntu.com/noble/xe-guest-utilities), [amd64-Dateiliste](https://packages.ubuntu.com/noble/amd64/xe-guest-utilities/filelist), [Debian-Paketierung](https://archive.ubuntu.com/ubuntu/pool/universe/x/xe-guest-utilities/xe-guest-utilities_7.20.2-0ubuntu1.debian.tar.xz) (`debian/xe-guest-utilities.xe-daemon.service`, `debian/proc-xen.mount`).
- **Hintergrund**: [XCP-ng-Linux-Gastwerkzeuge](https://docs.xcp-ng.org/vms/#linux-guest-tools) (allgemeine Informationen, keine Kompatibilitätsaussage für XCP-HL).
- **Oberflächenbeschriftungen**: [XO-Beschriftungskataloge](https://github.com/vatesfr/xen-orchestra/tree/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl), [HomeLab-Übersetzungsfallback](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/compact-xo-locales.py).
{{< /details >}}
