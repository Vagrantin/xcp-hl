---
title: Updates
weight: 3
translationKey: updates
aliases: ["/de/updates.html"]
---

XCP-hl und XOA-hl werden beide mit signierten Paketen im laufenden System aktualisiert; für reguläre Paketupdates ist keine Neuinstallation erforderlich. Der Host (XCP-hl) wird wie das ursprüngliche XCP-ng über die Registerkarte **Patches** von Xen Orchestra aktualisiert. Die Appliance (XOA-hl) wird über ihre eigene Einstellungsseite **XOA-HL Updates** aktualisiert.
{class="lead"}

Die Paketrepositories verwenden `rpm.xcp-hl.org` nach dem in [#190](https://github.com/Vagrantin/xcp-hl/issues/190) verfolgten Umzug. Ein Update von `xcp-hl-release` oder `xoa-hl` bringt die neuen Repository-Adressen mit. Die alten Adressen bleiben während des Übergangs erhalten. Die folgenden Bootstrap-Befehle verwenden die neue Adresse.

Beide Hälften dieser Seite folgen demselben Aufbau: Schritte in Xen Orchestra, entsprechende Befehle, Funktionsweise im Hintergrund und Rückkehr zu einer früheren Version.

## XCP-hl aktualisieren (Hypervisor-Host) {#updating-xcp-hl-the-host}

{{< callout type="info" >}}
**Gilt für** XOA-HL-Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basiert auf dem veröffentlichten Code; Installation von Hostpaketen und Neustart wurden mit dieser Version noch nicht auf einem Laborsystem getestet.
{{< /callout >}}

### In Xen Orchestra {#in-xen-orchestra}

1. **Ausstehende Updates erkennen.** Unter `Home > Hosts` zeigt ein rotes Abzeichen am Host die Anzahl fehlender Patches an.

   {{< screenshot src="updates/xcp-hl-1-missing-patches.png" alt="Hostliste: Ein rotes Abzeichen am Host zählt die fehlenden Patches" >}}

2. **Patches-Registerkarte des Hosts öffnen.** Wählen Sie den Host und dann **Patches**. Die Registerkarte führt jedes Paket mit Name, Beschreibung, Version, Release und Downloadgröße auf; das Augensymbol in einer Zeile zeigt dessen RPM-Änderungsprotokoll. Die Poolansicht `Home > Pools > <pool> > Patches` zeigt die fehlenden Pakete des Poolmasters. Prüfen Sie jeden Host separat vor einer Aktion für den gesamten Pool.

   {{< screenshot src="updates/xcp-hl-2-patches-tab.png" alt="Patches-Registerkarte des Hosts mit verfügbaren Paketen" >}}

3. **Gewünschten Umfang wählen.** Auf der Patches-Registerkarte des Hosts betrifft **Install all patches** diesen Host. Auf der Patches-Registerkarte des Pools betrifft **Install pool patches** alle Poolhosts, beginnend mit dem Master. Prüfen Sie die Identität von Host und Pool, bevor Sie eine Aktion bestätigen.

   {{< screenshot src="updates/xcp-hl-3-installing.png" alt="Patches-Registerkarte während der Installation der Poolpatches" >}}

   {{< callout type="warning" >}}
   Keine der beiden Schaltflächen wählt einzelne XCP-ng-Pakete aus. Für jeden gewählten Host führt `updater.py` ein `yum update` über die aktivierten ursprünglichen XCP-ng- und XCP-hl-Repositorys aus; ausstehende Upstream-Updates sind daher enthalten. Das ist ein gemeinsamer Paketvorgang, keine Garantie für ein atomares Rollback. Die Poolaktion verarbeitet Hosts einzeln, zuerst den Master; sie evakuiert keine VMs und startet Hosts nicht automatisch neu. Wenn Sie nur ausgewählte XCP-hl-Pakete aktualisieren möchten, verwenden Sie den separaten Befehlsweg unten.
   {{< /callout >}}

4. **Auf die Aufgabe warten und Hostverbindung aktualisieren.** In dieser XO-Version ruft die Schaltfläche das Updater-Plugin des Hosts auf und startet nach der Installation den XAPI-Agenten auf dem gewählten Host neu. Dabei kann die Hostverbindung vorübergehend abbrechen. Dieser Schritt ruft weder den XOA-HL-Appliance-Updater auf noch startet er `xo-server` neu. Bewahren Sie bei einer nicht wiederkehrenden Verbindung die Fehlermeldung auf und prüfen Sie den Host über eine unabhängige Konsole, bevor Sie erneut versuchen.

5. **Ergebnis prüfen.** Aktualisieren Sie das Inventar des betreffenden Hosts und Pools und prüfen Sie Aufgabenergebnis, Paket-/Versionsliste, Anzahl fehlender Patches und Neustarthinweis. Ein verschwundenes Abzeichen allein belegt weder einen Hostneustart noch den ordnungsgemäßen Zustand von Gästen und Speicher.

   {{< screenshot src="updates/xcp-hl-5-up-to-date.png" alt="Patches-Registerkarte mit vollständig aktualisiertem Host" >}}

### Hostupdate in einem Laborpool mit einem Host testen {#host-patch-pilot}

Führen Sie Ihr erstes Hostupdate in einem wiederherstellbaren Laborpool durch, nicht in einem Pool, auf den Sie angewiesen sind. Ein Test mit einem Host zeigt nicht, wie sich ein Pool mit mehreren Hosts während eines Updates verhält.

**Bevor Sie beginnen**

- Verwenden Sie einen **Laborpool mit einem Host**, dessen Veröffentlichung bekannt ist, ohne reguläre VMs, laufende Sicherungsaufgabe, HA oder XOA-HL-Appliance auf diesem Host.
- Halten Sie eine separate Hostkonsole, einen Wiederherstellungsplan für Host und Netzwerk sowie eine separate XOA-HL-Verbindung bereit.
- Reservieren Sie ein freigegebenes Wartungsfenster für den gesamten Paketsatz (Upstream und HomeLab). Entscheiden Sie über den Neustart separat.

1. Notieren Sie die oben genannten Image-, Paket- und XO-Versionen, Host- und Pool-UUIDs, Master, Verwaltungsadresse, installierte Paketversionen, aktivierte Repository-IDs, Betriebs- und Aktivierungszustand des Hosts und die genaue Liste ausstehender Pakete. Führen Sie auf der **Hostkonsole** `yum check-update` aus und vergleichen Sie das Ergebnis mit **Patches**. Stoppen Sie bei einem fehlgeschlagenen Check oder einer unerwarteten Liste. `yum check-update` kann bei verfügbaren Updates Status 100 zurückgeben; das ist normal.
2. Öffnen Sie im **XOA-HL-Browser** `/#/hosts/<host-id>/patches`, wählen Sie **Install all patches**, prüfen Sie den Host und bestätigen Sie einmal. Das Auswählen einer Zeile beschränkt das Update nicht auf dieses Paket. Notieren Sie Aufgaben-ID, Start- und Endzeit sowie Ausgaben oder Fehler. Klicken Sie bei einer vorübergehenden Trennung nicht erneut und starten Sie parallel kein Befehlszeilenupdate.
3. Vergleichen Sie nach Aufgabenende Ihre Notizen mit der separaten Konsole und dem aktualisierten XOA-HL-Inventar: installierte Versionen, verbleibende Patches, Erreichbarkeit des Hosts, Aktivierungs- und Betriebszustand, Verwaltungsnetzwerk und SR-Anbindungen. Bewahren Sie bei einem Fehler oder einer nicht wiederkehrenden Verbindung die Protokolle und den tatsächlichen Paketzustand auf. Für ein Teilupdate benötigen Sie den Wiederherstellungs- oder Neuaufbauplan des Hostverantwortlichen; gehen Sie nicht von einem erfolgten Rollback aus.
4. Wenn die Oberfläche einen Neustart verlangt, planen Sie einen **separaten**, freigegebenen Neustart bei leerem Pool. Prüfen Sie, dass keine VM oder Sicherungsaufgabe hinzugekommen ist. Wählen Sie dann einmal **Reboot to apply updates** auf der Patches-Registerkarte des Hosts. Bestätigen Sie keine Aufforderung, den Neustart zu erzwingen oder eine blockierte Suspendierung, Sicherung oder Versionsprüfung zu umgehen. Beobachten Sie den Host über die separate Konsole und prüfen Sie danach XOA-HL-Verbindung, Pakete, Neustarthinweis, Netzwerk und SRs erneut. Stoppen Sie bei unerwartetem Verhalten der Schaltfläche oder Aufgabe und dokumentieren Sie es. Erzwingen Sie keinen zweiten Neustart.

**Prüfung:** Der Host ist erreichbar, seine Pakete entsprechen den erwarteten Versionen, es fehlen keine Patches und es steht kein Neustart aus. Bewahren Sie Paketlisten vor und nach dem Vorgang, Aufgaben- und Konsolenausgaben, genaue Fehler, Neustartentscheidung und abschließende Erreichbarkeit auf. Unterbrochene Installationen, Wiederherstellung und Verfügbarkeit in produktiven Pools oder Pools mit mehreren Hosts sind hier nicht abgedeckt. [Hostwartung und Evakuierung](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) sind eine separate Aufgabe mit einer laufenden Test-VM; die Patch-Schaltfläche führt sie nicht aus.

### Über die Befehlszeile {#from-the-command-line}

Auf dem Host:

```bash
yum check-update                   # what is available
yum update xcp-hl-release          # the repository configuration itself
yum update xo-lite-ce xoa-proxy    # only the XCP-hl packages
yum update                         # everything, as the Patches tab does
```

### Funktionsweise {#how-it-works}

XCP-ng liefert das XAPI-Plugin `updater.py`, das Xen Orchestra nach der Liste verfügbarer Updates fragt. XOA-hl ist so angepasst, dass die Anfrage auch die XCP-hl-Repositorys enthält. Deshalb erscheinen XCP-hl-Pakete neben den ursprünglichen XCP-ng-Paketen.

Die Repositorys sind in einer einzigen Datei definiert: `/etc/yum.repos.d/xcp-hl.repo`, die zum Paket `xcp-hl-release` gehört:

| Repository-ID | Inhalt | Veröffentlicht aus |
|---|---|---|
| `xcp-hl-base` | `xcp-hl-release` | [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) |
| `xcp-hl-xolite` | `xo-lite-ce` | [`xolite-ce`](https://github.com/Vagrantin/xolite-ce) |
| `xcp-hl-xoa-proxy` | `xoa-proxy` | [`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) |

{{< callout type="error" >}}
Benennen Sie die Abschnitte in dieser Datei nicht um. Xen Orchestra übergibt diese Repository-IDs an `updater.py`, das nur Updates für die angefragten Repositorys aufführt. Ein umbenannter Abschnitt erzeugt keinen Fehler; seine Pakete verschwinden stillschweigend aus der Patches-Registerkarte.
{{< /callout >}}

Repository-Einstellungen werden als Paket ausgeliefert, damit Änderungen installierte Hosts erreichen können, statt auf eine einmal kopierte Datei angewiesen zu sein. Über `yum update xcp-hl-release` erreichen solche Änderungen Ihren Host.

### Erstmalige Einrichtung auf einem vorhandenen Host {#first-time-setup-on-an-existing-host}

Hosts, deren Installations-ISO älter als das Paket `xcp-hl-release` ist, benötigen eine einmalige Ersteinrichtung. Danach verwaltet yum die Konfiguration.

```bash
curl -L -o /etc/yum.repos.d/xcp-hl.repo \
  https://rpm.xcp-hl.org/xcp-hl.repo

rpm --import https://rpm.xcp-hl.org/xcp-ng-ce-public.asc

yum clean all
yum install xcp-hl-release
```

Die Paketinstallation ersetzt die gerade heruntergeladene Datei durch die Paketversion und bewahrt Ihre Datei als `xcp-hl.repo.rpmorig` auf. Beide unterscheiden sich nur darin, woher sie den Signaturschlüssel lesen: Die heruntergeladene Kopie lädt ihn über HTTPS, die Paketkopie verwendet den vom Paket installierten lokalen Schlüssel.

Neuere ISOs enthalten `xcp-hl-release` bereits; für sie entfällt dieser Schritt.

### Zu einer früheren Version zurückkehren {#rolling-back}

Jedes Repository veröffentlicht nur seine neuesten Releases. Das begrenzt, wie weit Sie zurückgehen können. So kehren Sie zu einem älteren Build zurück:

```bash
yum --showduplicates list xo-lite-ce
yum downgrade xo-lite-ce-<version>
```

## XOA-hl aktualisieren (Verwaltungsoberfläche) {#updating-xoa-hl-the-appliance}

### In Xen Orchestra {#in-xen-orchestra-1}

1. **Update-Seite öffnen.** Gehen Sie in der XOA-hl-Weboberfläche zu `Settings > XOA-HL Updates`. Die installierte Version wird angezeigt. Bis zur ersten Prüfung lautet der Status *Update status unknown*.

   {{< screenshot src="updates/xoa-hl-1-update-tab.png" alt="Seite XOA-HL Updates vor einer Prüfung" >}}

2. **Check for update anklicken.** Die Seite führt alle Pakete mit verfügbaren Updates einschließlich Version auf.

   {{< screenshot src="updates/xoa-hl-2-check-result.png" alt="Prüfergebnis: verfügbare Updates mit Paketliste" >}}

3. **Update now anklicken.** Das Update-Protokoll wird während des Vorgangs auf die Seite übertragen. Das Update startet xo-server neu; die Seite zeigt kurz *Reconnecting* an und läuft anschließend selbstständig weiter.

   {{< screenshot src="updates/xoa-hl-3-in-progress.png" alt="Laufendes Update mit fortlaufender Protokollausgabe" >}}

   {{< callout type="warning" >}}
   **Update now** installiert alle ausstehenden Pakete der Appliance einschließlich AlmaLinux und Kernel, nicht nur `xoa-hl`. In ce20 schließt der verwaltete Updater Node.js aus.
   {{< /callout >}}

4. **Abschluss.** Prüfen Sie nach Abschluss erneut: Die Seite meldet *Up to date*.

   {{< screenshot src="updates/xoa-hl-4-up-to-date.png" alt="Seite XOA-HL Updates meldet einen aktuellen Stand der Appliance" >}}

### Über die Befehlszeile {#from-the-command-line-1}

Auf der Appliance:

```bash
dnf check-update         # what is available
dnf update xoa-hl        # the appliance application only
dnf update --exclude=nodejs  # the application and the AlmaLinux base together
```

### Funktionsweise {#how-it-works-1}

Die Appliance hat ihr eigenes yum-Repository, definiert in `/etc/yum.repos.d/xoa-hl.repo`, das zum Paket `xoa-hl` selbst gehört:

| Repository-ID | Inhalt | Veröffentlicht aus |
|---|---|---|
| `xoa-hl` | `xoa-hl` | [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) |

Die beiden Schaltflächen auf der Update-Seite starten zwei systemd-Units:

| Unit | Aufgabe |
|---|---|
| `xoa-hl-check-update.service` | Führt `dnf check-update` aus und schreibt das Ergebnis nach `/run/xoa-hl/status` |
| `xoa-hl-update.service` | Führt ein vollständiges `dnf -y --refresh --exclude=nodejs update` aus und protokolliert nach `/var/lib/xoa-hl/update.log` |

### Automatische Prüfungen und Updates {#automatic-checks-and-updates}

In der `xoa-hl`-Veröffentlichung `v5.113.2_e281c536-ce20` bietet **Settings → XOA-HL Updates → Automatic updates** drei Modi:

| Modus | Verhalten |
|---|---|
| Manual only | Ein Administrator startet Prüfungen und Installationen; dies ist der Standard. |
| Check automatically | Geplante Prüfungen aktualisieren den Status; die Installation bleibt manuell. |
| Install automatically | Prüft und installiert nach ausdrücklicher Bestätigung im konfigurierten Wartungsfenster. |

Wählen Sie Häufigkeit, Wochentag (bei wöchentlichen Plänen) und lokale Startzeit und speichern Sie. Die Zeiten verwenden die **Zeitzone der Appliance**. Ausführungen beginnen zur festgelegten Zeit ohne zufällige Verzögerung. Seit `v5.113.2_e281c536-ce40` erscheint bei einer fehlgeschlagenen automatischen Ausführung ein rotes Banner auf der Seite. Die Installation oder Aktualisierung des RPM aktiviert keine automatische Installation. Ältere Pakete zeigen diese Einstellungen möglicherweise nicht; prüfen Sie zuerst die installierte Version.

Der verwaltete Updater schließt Node.js aus, sodass dessen unterstützte Hauptversion unverändert bleibt. Updates können Dienste einschließlich xo-server neu starten. Es gibt **keinen automatischen Neustart**; ein verpasstes Installationsfenster wird nicht unmittelbar nach dem Booten nachgeholt. Prüfen Sie das Ergebnis und organisieren Sie erforderliche Neustarts selbst. Die [versionierte Planungsreferenz](https://github.com/Vagrantin/xoa-hl/blob/v5.113.2_e281c536-ce40/docs/automatic-updates.md) beschreibt Befehlszeilenkonfiguration und Diagnose.

### Die Update-Seite verliert die Verbindung

Die Installation eines neuen `xoa-hl` startet `xo-server` neu, der auch die Weboberfläche bereitstellt; daher verliert die Update-Seite für eine Weile die Verbindung. Das Update selbst läuft in `xoa-hl-update.service` und wird unabhängig davon fortgesetzt.

Veröffentlichungen nach `v5.113.2_e281c536-ce18` behandeln das so:

- Die Seite versucht weiter, die Verbindung wiederherzustellen, solange `xo-server` nicht läuft, setzt dann das Protokoll an der unterbrochenen Stelle fort und zeigt das Ergebnis an.
- `xo-server` wird einmal neu gestartet, nachdem die gesamte Transaktion abgeschlossen ist.
- Nach einer Minute ohne Verbindung nennt die Seite, wie lange `xo-server` schon nicht erreichbar ist, und bietet die Schaltfläche **Reload page** an, die erst neu lädt, wenn `xo-server` wieder antwortet.
- Beim Neuladen der Seite erscheint das Update, das dieser Tab gestartet hat, mit seinem Ergebnis.

### Nach einem unterbrochenen Update {#after-an-interrupted-update}

Nur mit `v5.113.2_e281c536-ce52` getestet. Andere Veröffentlichungen können sich anders verhalten.

In einem ce52-Test beschädigte ein erzwungener Stopp während der Installation von `kernel-modules` durch `xoa-hl-update.service` Kerneldateien. Das nächste verwaltete Update hielt bei seiner Integritätsprüfung an und meldete einen Fehler. Andere Unterbrechungen können andere Folgen haben. Das Ende von `/var/lib/xoa-hl/update.log` lautet:

```text
Package integrity preflight failed; repair the interrupted transaction before retrying.
=== xoa-hl update failed with exit code 1 at ... ===
```

In diesem Test startete die Appliance mit ihrem vorherigen Kernel. Das Protokoll nannte die beschädigten Dateien oberhalb dieser Meldung; gehen Sie nicht davon aus, dass eine unterbrochene Appliance startet.

{{< callout type="warning" >}}
Führen Sie die folgenden Befehle als root aus und nur, solange kein Update läuft. Entfernen Sie nicht den Kernel, mit dem die Appliance gestartet wurde.
{{< /callout >}}

**Prüfen.** Stellen Sie sicher, dass kein Update läuft, und prüfen Sie dann die Paketdatenbank und die Kernelpakete:

```bash
systemctl is-active xoa-hl-update.service    # expect inactive or failed
dnf check
rpm -V $(rpm -qa kernel-core kernel-modules kernel-modules-core)
ls /boot/vmlinuz-*
```

`dnf check` kann nichts Auffälliges melden, obwohl Kerneldateien beschädigt sind; führen Sie daher beide Prüfungen aus. Zeilen wie `S.5......  /lib/modules/<version>/vmlinuz` bedeuten, dass die Dateien dieser Kernelversion beschädigt sind, und ein fehlendes `/boot/vmlinuz-<version>` bestätigt es. Zeilen zu fehlenden Dateien unter `/usr/share/licenses` oder `/usr/share/doc` sind normal: Das Image wird ohne Dokumentation installiert, und der Updater ignoriert sie.

**Reparieren.** Installieren Sie die von `rpm -V` angezeigte beschädigte Kernelversion neu, zum Beispiel `5.14.0-687.66.1.el9_8`, und prüfen Sie anschließend:

```bash
dnf remove --duplicates
dnf reinstall kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
dnf check
rpm -V kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
grubby --default-kernel
```

Beide Prüfbefehle dürfen nichts ausgeben, und `grubby --default-kernel` sollte den neuesten Kernel nennen.

**Update wiederholen.** Führen Sie das verwaltete Update erneut aus, über **Settings → XOA-HL Updates** oder mit `systemctl start xoa-hl-update.service`. Es sollte mit `=== xoa-hl update finished successfully ===` enden. Die Appliance startet nie von selbst neu; starten Sie sie danach neu. `dnf needs-restarting -r` zeigt, ob ein Neustart aussteht, und `uname -r` den laufenden Kernel nach dem Neustart.

Unter `ce52` wurde diese Reparatur für eine Kerneltransaktion getestet, die während der Installation von `kernel-modules` abgebrochen wurde. Nicht getestet wurde sie für ein doppeltes Paket wie `xz-libs`, für ein unterbrochenes automatisches Update (Modus `install`) oder für einen Fehler, der nach statt vor der Transaktion gemeldet wird.

### Zu einer früheren Version zurückkehren {#rolling-back-1}

Ältere Pakete können von den aktuell aktivierten Repositorys aufgeführt werden:

```bash
dnf --showduplicates list xoa-hl
```

Die Verfügbarkeit ändert sich mit der Zeit. Für `v5.113.2_e281c536-ce40` wurden Paket-Downgrade und versionsübergreifende Konfigurationswiederherstellung nicht als Verfahren zur Appliance-Wiederherstellung validiert. Ein Downgrade macht weder Basisbetriebssystem-Updates rückgängig noch stellt es XO-Daten und Betreiberdateien wieder her. Bereiten Sie anhand der [Konfigurationsanleitung](/docs/xoa-hl/configuration-backup/) einen Export und einen isolierten Wiederherstellungstest vor, bevor Sie ein Rollback planen.

## Prüfung und Vertrauen {#verification-and-trust}

Pakete und Repository-Metadaten von XCP-hl und XOA-hl werden mit dem XCP-hl-GPG-Schlüssel signiert. Die Clientkonfiguration setzt `repo_gpgcheck=1` zusammen mit `gpgcheck=0`.

Die RPMs werden von einem GPG-**Unterschlüssel** signiert, nicht vom Hauptschlüssel. Das `rpm`-Werkzeug im Hostsystem von XCP-ng 8.3 (Version 4.11) hat dabei eine bekannte Einschränkung: Beim Import eines Schlüssels registriert es nur den Hauptschlüssel. Deshalb meldet es für eine Unterschlüsselsignatur `NOKEY` und kann das Paket nicht direkt prüfen, obwohl die Signatur echt ist.

Stattdessen verläuft die Vertrauenskette über die Repository-Metadaten. Das eigentliche GPG-Werkzeug, das Unterschlüssel versteht, prüft `repomd.xml`. Diese Datei enthält eine Prüfsumme von `primary.xml`, die wiederum eine Prüfsumme jedes Pakets enthält. Die Prüfung einer Datei, `repomd.xml`, prüft damit jedes RPM im Repository.

{{< callout type="warning" >}}
Die Signatur-Unterschlüssel laufen am **2027-05-10** ab. Danach schlägt die Prüfung fehl, bis ihre Gültigkeit verlängert, der veröffentlichte Schlüssel aktualisiert und auf jedem Host erneut importiert wurde.
{{< /callout >}}

## Bekannte Einschränkungen {#known-limitations}

- **Das automatische Update kann melden, dass kein Neustart nötig ist, obwohl einer aussteht.** Wenn unter `v5.113.2_e281c536-ce52` ein manuelles Update bereits einen Kernel installiert hat und der nächste automatische Lauf nichts zu tun findet, verzeichnet sein Verlauf `rebootNeeded: no`. Prüfen Sie mit `dnf needs-restarting -r`. Eine Korrektur ist nach dem Launch geplant. Siehe [Issue #392](https://github.com/Vagrantin/xcp-hl/issues/392).

- **Das Update, das die Verbindungskorrektur installiert, kann weiterhin hängend wirken.** Die Seite, von der Sie es gestartet haben, führt noch den alten Code aus, der nach etwa 2,5 Minuten aufhört, die Verbindung wiederherzustellen. Bleibt sie bei *Reconnecting to xo-server*, warten Sie, bis `xo-server` wieder erreichbar ist, und laden Sie die Seite neu. Das Update ist nicht betroffen. Das Protokoll lesen Sie in einer Shell mit `cat /var/lib/xoa-hl/update.log`. Das gilt einmalig für das Upgrade von `v5.113.2_e281c536-ce18` oder früher. Siehe [Issue #103](https://github.com/Vagrantin/xcp-hl/issues/103).

{{< callout type="info" >}}
Denken Sie daran, dass sich diese Distribution im Beta-Stadium befindet. Lesen Sie vor dem Aktualisieren die Versionshinweise: Inkompatible Änderungen sind bei jeder Veröffentlichung zu erwarten; ein Update kann manuelle Eingriffe erfordern.
{{< /callout >}}
