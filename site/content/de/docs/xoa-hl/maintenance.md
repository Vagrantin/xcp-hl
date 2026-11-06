---
title: "Appliance warten und aktualisieren"
linkTitle: "Appliance-Wartung"
description: "Installierte Versionen erfassen, ein Wartungsfenster vorbereiten, die Appliance aktualisieren und das Ergebnis prüfen."
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: draft
sourceRevision: sha256:39d5583b5b7de077c177e2558dd46fd8e130596274d3c4c7072c9041137ced1c
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Aktualisieren Sie die XOA-HL-Appliance in vier Schritten: Erfassen Sie die installierten Komponenten, bereiten Sie ein Wartungsfenster vor, wählen Sie die Ausführung der Updates und prüfen Sie anschließend das Ergebnis. Sie arbeiten im **Browser**, als Administrator bei XOA-HL angemeldet. Einige lesende Prüfungen führen Sie **innerhalb der Appliance** über deren Konsole oder SSH aus.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Spätere Pakete können sich anders verhalten.
{{< /callout >}}

## 1. Ausgangszustand erfassen {#record-versions}

1. Öffnen Sie als Administrator im Browser **About** (`/#/about`).
2. Notieren Sie **XOA-HL version**, **XOA-HL VM version**, die Adresse der Appliance und den ursprünglichen Image-Tag. Die VM-Version bezeichnet den Image-Build. Ein Anwendungsupdate ändert sie nicht.

Wenn Sie autorisierten Konsolen- oder SSH-Zugriff haben, führen Sie diese lesenden Befehle innerhalb der Appliance aus. Verwenden Sie bei Bedarf Root-Rechte.

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

Bewahren Sie die Ausgabe zusammen mit der [Versionsmatrix](/docs/reference/release-matrix/) und den [Versionshinweisen](/docs/reference/changelog/) auf. Die Matrix nennt die zusammen ausgelieferten Komponenten; sie belegt keine gemeinsamen Tests.

## 2. Updatefenster vorbereiten {#prepare-window}

- [Exportieren Sie die XO-Konfiguration](/docs/xoa-hl/configuration-backup/). Bewahren Sie die Datei und ihre Passphrase außerhalb der Appliance auf.
- Dokumentieren Sie Änderungen an `/root/.config/xo-server/config.toml`, den TLS-Dateien und `/etc/xoa-hl/update.conf` gesondert. Der Webexport enthält diese Dateien nicht.
- Prüfen Sie, dass Sie die Appliance-Konsole über XO Lite öffnen können, falls die Weboberfläche ausfällt.
- Prüfen Sie, dass Sicherungen, Wiederherstellungen und andere Verwaltungsaufgaben abgeschlossen sind.
- Planen Sie genug Zeit für einen Dienstneustart und gegebenenfalls einen späteren Neustart der Appliance ein.

Diese Seite aktualisiert ausschließlich die XOA-HL-VM. Hostupdates sind eine eigene Aufgabe: Im [Updateleitfaden](/docs/guides/updates/) finden Sie die richtigen Zielsysteme und Befehle.

## 3. Modus und Kanal wählen {#update-mode-channel}

Öffnen Sie **Settings → XOA-HL Updates** (`/#/settings/xoa-hl-updates`). Für manuelle Updates folgen Sie der [Updateanleitung](/docs/guides/updates/) für **Check for update** und **Update now**.

Wählen Sie einen **Mode**:

| Modus | Ihre Aufgabe |
| --- | --- |
| Manual only | Sie starten jede Prüfung und Installation selbst. Dies ist die Voreinstellung |
| Check automatically | Prüfungen laufen nach Zeitplan. Sie entscheiden über die Installation |
| Install automatically | Installationen laufen nach Zeitplan. Verwenden Sie dies erst nach ausdrücklicher Freigabe der Installation in Ihrem Wartungsfenster |

Für einen zeitgesteuerten Modus:

1. Prüfen Sie **Appliance timezone**. Der Zeitplan verwendet diese Zeitzone, nicht die des Hosts oder Browsers. Vergleichen Sie sie mit der Ausgabe von `timedatectl`.
2. Legen Sie **Frequency**, bei wöchentlicher Ausführung den **Day**, und **Local start time** fest. Der Lauf beginnt zu dieser Zeit ohne zufällige Verzögerung.
3. Wählen Sie **Save automatic update settings**.
4. Prüfen Sie die gespeicherten Einstellungen und die Timerliste von `systemctl list-timers 'xoa-hl-*'`.

Belassen Sie **Update channel** für die reguläre Wartung auf **Stable**. **Testing** ergänzt Kandidatenpakete: Verwenden Sie diesen Kanal nur auf einer entbehrlichen Test-Appliance. Ein Kanalwechsel installiert nichts und stuft ein bereits installiertes Kandidatenpaket nicht zurück.

Das verwaltete Update führt ein vollständiges `dnf`-Update mit Ausnahme von `nodejs` aus. Die Installation des Anwendungspakets startet `xo-server` nach der Transaktion neu; dadurch kann die Webseite die Verbindung verlieren. Das allein bedeutet keinen Updatefehler.

## 4. Ergebnis prüfen {#check-result}

1. Verbinden Sie sich erneut mit der Weboberfläche und öffnen Sie **About**. Prüfen Sie die erwartete Anwendungsversion.
2. Prüfen Sie, dass die erwarteten Hosts verbunden sind und ihr Inventar erscheint.
3. Lesen Sie das Updateergebnis. Beim Öffnen zeigt die Seite die zuletzt gespeicherte Prüfung, auch eine zeitgesteuerte. Unter **Last automatic result** erscheint ein fehlgeschlagener automatischer Lauf in einem roten Hinweis.

Ist das Ergebnis unklar, führen Sie innerhalb der Appliance diese lesenden Prüfungen aus:

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| Datei oder Wert | Bedeutung |
| --- | --- |
| `/run/xoa-hl/status` | Letzte Prüfung: `UP_TO_DATE`, `AVAILABLE` oder `ERROR`. Geht beim Appliance-Neustart verloren |
| `/var/lib/xoa-hl/update.log` | Ausgabe der verwalteten Installation mit abschließender Erfolgs- oder Fehlermarkierung. Wird beim nächsten Versuch überschrieben |
| `/var/lib/xoa-hl/auto-update.status` | Nur automatische Läufe. Vergleichen Sie `startedAt` und `finishedAt` (UTC) mit der Updatezeit |
| `result=check_failed` oder `result=failed` | Prüfung oder Installation fehlgeschlagen: Lesen Sie das Protokoll. Keiner der Werte bedeutet Erfolg |
| `rebootNeeded=yes`, `no` oder `unknown` | Einschätzung des automatischen Laufs. `unknown` bedeutet nicht, dass kein Neustart erforderlich ist |

Eine manuelle Installation aktualisiert den Datensatz automatischer Läufe **nicht**. Ein Prüfdienst kann erfolgreich enden und dennoch ein Problem melden; lesen Sie sein Ergebnis. Sichern Sie die relevanten Protokolle vor einem weiteren Versuch.

**Prüfung:** **About** zeigt die erwartete Version, die erwarteten Hosts sind verbunden und das Updateergebnis meldet Erfolg.

## Wenn das Update nicht sauber endet {#update-problems}

Es gibt **keinen automatischen Neustart**. Verwaltete Prüfung und Installation teilen sich eine Sperre; ein in einer Shell gestarteter `dnf`-Befehl fällt jedoch nicht darunter. Solange ein Update laufen könnte, starten Sie niemals einen weiteren `dnf`-Prozess, stoppen Sie keine laufende Transaktion und starten Sie nicht neu, um den belegten Updater freizugeben.

| Problem | Prüfen |
| --- | --- |
| Nur der Browser wurde getrennt | Die Anwendungsinstallation startet `xo-server` neu. Prüfen Sie Dienst und Protokoll über die Konsole, bevor Sie es erneut versuchen. |
| Der Updater scheint belegt | Prüfen Sie Dienst und Protokoll über die Konsole. Starten Sie keinen weiteren `dnf`, stoppen Sie keine Transaktion und starten Sie nicht neu, um ihn freizugeben. |
| Ein automatisches Installationsfenster wurde verpasst | Die verpasste Installation wird beim nächsten Appliance-Start nicht sofort nachgeholt. Planen Sie ein neues Fenster. |
| Der Appliance-Start wurde unterbrochen oder das Ergebnis ist unklar | Sichern Sie die Protokolle und nutzen Sie die [Fehlerbehebung](/docs/xoa-hl/troubleshooting/), bevor Sie ein weiteres Update planen. |
| Die installierten Änderungen könnten einen Neustart erfordern | Starten Sie erst neu, wenn keine Transaktion oder Verwaltungsaufgabe mehr läuft und Sie entschieden haben, dass die Änderungen dies erfordern. Prüfen Sie danach Anmeldung, Versionen und Inventar erneut. |
| Sie möchten zur vorherigen Version zurückkehren | Ein Paket-Downgrade ist kein getestetes Wiederherstellungsverfahren. Es stellt weder das Basisbetriebssystem noch XO-Daten oder eigene Dateien wieder her. Lesen Sie zuerst die [Grenzen der Wiederherstellung](/docs/xoa-hl/configuration-backup/#recovery-limits). |

{{< details title="Quellen" closed="true" >}}
- **Appliance-Updater**: [Zeitplanung](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md), [Installer](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-update.sh), [Status automatischer Läufe](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-auto-update.sh), [Prüfergebnis](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh), [Paketspezifikation](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [Kanal-Patch](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzz-xoa-hl-update-channel.patch), [Korrekturen der Seite für automatische Updates](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzzzzz-xoa-hl-auto-update-ui-fixes.patch).
{{< /details >}}
