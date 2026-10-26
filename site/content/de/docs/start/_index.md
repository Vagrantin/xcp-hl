---
title: Erste Schritte
weight: 1
translationKey: getting-started
---

Installieren Sie den Hypervisor, öffnen Sie XO Lite und stellen Sie XOA-hl zur Verwaltung Ihrer virtuellen Maschinen bereit.
{class="lead"}

<span id="start-overview"></span>

## Was ist XCP-hl? {#what-is-xcp-hl}

XCP-hl ist eine Homelab-Distribution auf Basis von XCP-ng 8.3. Sie läuft direkt auf Ihrer Hardware und beherbergt Ihre virtuellen Maschinen. **XO Lite** ist die kleine Verwaltungsoberfläche, die der Host bereitstellt. **XOA-hl** ist eine separate virtuelle Maschine mit Xen Orchestra, der Weboberfläche zur Verwaltung Ihrer Hosts und VMs.

XO Lite bietet vier Appliances zur Auswahl: **XOA-hl** (Standard), die offizielle Vates-Appliance, Ronivays Image oder ein eigenes XVA-Image. Diese Anleitung beschreibt XOA-hl. Die Unterschiede finden Sie unter [Funktionen](/docs/features).

<span id="start-requirements"></span>

## Bevor Sie beginnen {#before-you-begin}

- Verwenden Sie einen dedizierten, von XCP-ng 8.3 unterstützten Rechner mit aktivierter Hardwarevirtualisierung. Die [Upstream-Anforderungen](https://docs.xcp-ng.org/installation/requirements/) beschreiben die Unterstützung für CPU, Arbeitsspeicher und Netzwerk.
- Sichern Sie sämtliche Daten auf den Datenträgern, die Sie verwenden möchten. **Die Installation löscht die ausgewählten Datenträger.**
- Planen Sie auf dem Installationsdatenträger mindestens **100 GB** für die automatische ISO-Bibliothek mit 20 GB von XCP-hl sowie Platz für Ihre VMs ein. Kleinere unterstützte Datenträger verwenden die Upstream-Aufteilung ohne diese Bibliothek. Siehe [ISO-Speicher](/docs/features#iso-storage).
- Bereiten Sie eine stabile Verwaltungs-IP-Adresse sowie Gateway-, DNS- und NTP-Einstellungen vor. Eine statische Adresse oder DHCP-Reservierung erleichtert es, den Host zu finden.
- Sie benötigen einen zweiten Computer mit Browser und Netzwerkzugriff auf den Host. Für die Appliance-Bereitstellung muss auch die gewählte Image-URL erreichbar sein.

{{< callout type="warning" >}}
XCP-hl ist Alpha-Software für Homelabs und Tests. Lesen Sie die Versionshinweise und rechnen Sie mit Änderungen zwischen Veröffentlichungen. Bewahren Sie Sicherungen außerhalb des Hosts auf.
{{< /callout >}}

<span id="start-download"></span>

## Herunterladen und prüfen {#download--verify}

{{< latest-iso-download text="Neuestes ISO herunterladen" shaText="SHA256-Prüfsumme" >}}

<span id="start-verification"></span>

### ISO prüfen {#verify-the-iso}

Laden Sie Prüfsumme und Signatur aus derselben Veröffentlichung herunter und verwenden Sie den unten verlinkten öffentlichen Projektschlüssel. Prüfen Sie vor dem Vertrauen in den Schlüssel seinen Fingerabdruck: **2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A**. Der historische Schlüsselname lautet `XCP-ng Community Edition (Master signing key)`.

{{< verify-iso >}}

Schreiben Sie das ISO mit einem geeigneten Image-Schreibprogramm auf einen USB-Datenträger oder binden Sie es als virtuelles Installationsmedium ein. Das Schreiben des Images löscht den USB-Datenträger; kontrollieren Sie das ausgewählte Gerät.

<span id="start-quick-start"></span>

## Schnellstart {#quick-start}

<span id="start-install"></span>

### 1 · XCP-hl installieren {#1--install-xcp-hl}

Dies ist eine **sinnvolle Standardkonfiguration für ein Homelab mit einem Host**, abgeleitet von der [Anleitung des Autors zur Erstinstallation von XCP-ng](https://vagrantin.github.io/blog/20260107/xcp-ng-first-install.html). Passen Sie Datenträger, Speicher und Netzwerk an Ihre Anforderungen an. Die folgenden Fotos zeigen das ursprüngliche XCP-ng 8.3; Bezeichnungen können in XCP-hl abweichen. Die [Upstream-Installationsanleitung](https://docs.xcp-ng.org/installation/install-xcp-ng/) beschreibt weitere Optionen.

1. **Starten Sie das Installationsprogramm und wählen Sie Ihre Tastaturbelegung.** Lesen Sie den Installationshinweis und die Lizenzvereinbarung, bevor Sie fortfahren.

   {{< screenshot src="install/keyboard.jpg" alt="Auswahl der Tastaturbelegung im Installationsprogramm" >}}

2. **Wählen Sie den Systemdatenträger und den Datenträger für VM-Speicher.** Kontrollieren Sie Gerätenamen und Kapazitäten. Wählen Sie weder den USB-Installationsdatenträger noch einen Datenträger aus, dessen Daten Sie behalten möchten.

   {{< screenshot src="install/system-disk.jpg" alt="Auswahl des Systemdatenträgers" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Auswahl des Datenträgers für virtuelle Maschinen" >}}

3. **Wählen Sie den Speichertyp.** EXT mit Thin Provisioning ist ein praktischer Einstieg für ein Homelab: Virtuelle Datenträger belegen erst beim Schreiben von Daten Platz. LVM reserviert ihre zugewiesene Kapazität. Wählen Sie passend zu Ihren Anwendungen und überwachen Sie bei beiden Optionen den freien Speicherplatz.

   {{< screenshot src="install/storage-type.jpg" alt="Auswahl von EXT- oder LVM-Speicher" >}}

4. **Verwenden Sie Local media als Installationsquelle.** Führen Sie die angebotene Medienprüfung aus, besonders wenn Sie einen beschädigten Download oder USB-Datenträger vermuten.

   {{< screenshot src="install/source.jpg" alt="Auswahl von Local media als Installationsquelle" >}}

5. **Legen Sie das root-Passwort fest und bewahren Sie es sicher auf.** Mit diesem Konto melden Sie sich an XO Lite an und verbinden den Host mit Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Festlegen des root-Passworts für den Host" >}}

6. **Konfigurieren Sie Verwaltungsnetzwerk und DNS.** Verwenden Sie eine statische Adresse oder DHCP-Reservierung; richten Sie ein VLAN nur ein, wenn Ihr Netzwerk dies erfordert. Geben Sie den Hostnamen und erreichbare DNS-Server ein.

   {{< screenshot src="install/network.jpg" alt="Konfigurieren von Verwaltungs-IP-Adresse und Gateway" >}}
   {{< screenshot src="install/dns.jpg" alt="Konfigurieren von Hostname und DNS-Servern" >}}

7. **Legen Sie Zeitzone und NTP-Server fest und überprüfen Sie die Installation.** Verwenden Sie einen internen NTP-Server, wenn der Host keine öffentlichen Server erreichen kann. Bestätigen Sie die gewählten Datenträger, bevor Sie die Installation starten.

   {{< screenshot src="install/ntp.jpg" alt="Konfigurieren der Zeitsynchronisierung" >}}
   {{< screenshot src="install/confirm.jpg" alt="Abschließende Bestätigung der Installation" >}}

8. **Schließen Sie die Installation ab, entfernen Sie das Installationsmedium und starten Sie neu.** Notieren Sie die Verwaltungsadresse, die auf der Hostkonsole angezeigt wird.

   {{< screenshot src="install/complete.jpg" alt="Installation abgeschlossen und bereit für den Neustart" >}}

<span id="start-open-xo-lite"></span>

### 2 · XO Lite öffnen {#2--open-xo-lite}

Öffnen Sie `https://<your-host-ip>` in Ihrem Browser. Der Host verwendet anfangs ein selbstsigniertes Zertifikat: Stellen Sie vor dem Akzeptieren sicher, dass Sie mit Ihrem eigenen Host verbunden sind. Melden Sie sich als `root` mit dem bei der Installation festgelegten Passwort an.

XO Lite wird bereits vom Host bereitgestellt; Sie müssen keine separate XO-Lite-VM installieren.

<span id="start-deploy-xoa"></span>

### 3 · XOA bereitstellen {#3--deploy-xoa}

Klicken Sie in XO Lite auf **Deploy XOA** und wählen Sie **XOA-hl**. Füllen Sie die angezeigten Netzwerk- und Bereitstellungsfelder aus, prüfen Sie das gewählte Image und die Zugangsdaten und starten Sie die Bereitstellung. Warten Sie, bis die Appliance-VM gestartet ist und eine Adresse erhalten hat. Ändern Sie sämtliche vorgegebenen Standardpasswörter bei der ersten Anmeldung.

Der xoa-proxy des Hosts überträgt das gewählte XVA-Image als Stream an XAPI, das die Appliance-VM erstellt. Das XOA-hl-Image wird zum Bereitstellungszeitpunkt ermittelt, unabhängig von der ISO-Version.

<span id="start-connect-host"></span>

### 4 · XO mit Ihrem Host verbinden {#4--connect-xo-to-your-host}

Öffnen Sie die Adresse der XOA-hl-Appliance in Ihrem Browser. Verwenden Sie in Xen Orchestra `Settings → Servers → Add server`, geben Sie die Hostadresse und dessen root-Zugangsdaten ein und bestätigen Sie die Verbindung. Die Appliance hat eine eigene Adresse; diese unterscheidet sich von der XO-Lite-Adresse des Hosts.

Prüfen Sie nach dem Verbinden Host und Speicher in Xen Orchestra, laden Sie ein Installations-ISO in die ISO-Bibliothek und erstellen Sie Ihre erste VM.

<span id="start-updates"></span>

### 5 · Aktuell halten {#5--keep-it-up-to-date}

Host- und Appliance-Updates sind separate Vorgänge. Verwenden Sie die Registerkarte **Patches** des Hosts für XCP-hl und **Settings → XOA-HL Updates** für XOA-hl. Lesen Sie die [Update-Anleitung](/docs/guides/updates), bevor Sie einen dieser Vorgänge starten.

<span id="start-architecture"></span>

## Architektur im Überblick {#architecture-at-a-glance}

{{< architecture >}}

Ihr Browser kann sich direkt mit **XO Lite auf dem Host** oder mit **Xen Orchestra innerhalb der XOA-hl-VM** verbinden. XOA-hl verwaltet anschließend den Host über XAPI. Andere Gast-VMs laufen neben XOA-hl; sie laufen nicht innerhalb der Appliance.

<span id="start-components"></span><span id="start-license"></span>

## Lizenz {#license}

XCP-hl wird unter **AGPL-3.0** veröffentlicht und baut auf XCP-ng und Xen Orchestra auf. Es ist ein unabhängiges Community-Projekt, das weder mit Vates SAS noch mit dem XCP-ng-Projekt verbunden ist oder von ihnen empfohlen oder unterstützt wird.
