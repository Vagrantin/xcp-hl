---
title: "XCP-ng-Erstinstallation Schritt für Schritt"
date: 2026-01-07T09:00:00+09:00
slug: xcp-ng-first-install
translationKey: blog-xcp-ng-first-install
---

Die Schritt-für-Schritt-Erstinstallation des Autors für ein Upstream-XCP-ng 8.3, vom Installer-ISO bis zur bereitgestellten Xen-Orchestra-Appliance, mit Fotografien des Upstream-Installers.
{class="lead"}

{{< callout type="warning" >}}
Diese Anleitung beschreibt **Upstream-XCP-ng 8.3**, nicht XCP-hl. XCP-hl ist Alpha-Software auf Basis von XCP-ng 8.3, daher können Installer-Bezeichnungen und einige Voreinstellungen in XCP-hl abweichen. Die folgenden Fotografien zeigen den Upstream-Installer 8.3.
{{< /callout >}}

## Über diese Seite

Dies ist die XCP-ng-8.3-Erstinstallationsanleitung des Autors, ursprünglich am 2026-01-07 in seinem persönlichen Blog veröffentlicht und am 2026-11-11 gemäß dem in [PR #409](https://github.com/Vagrantin/xcp-hl/pull/409) dokumentierten Eigentümerbeschluss auf diese Seite migriert, damit die [Erste-Schritte](/docs/start/)-Seiten auf der Produktionsdomain auf sie verlinken. Für den XCP-hl-Weg (ISO-Download, Prüfsummen-Verifikation, XOA-hl-Appliance) folgen Sie stattdessen [Erste Schritte](/docs/start/).

## Bevor Sie beginnen

- Ein dedizierter Rechner, der von XCP-ng 8.3 unterstützt wird, mit aktivierter Hardware-Virtualisierung; siehe die [Upstream-Anforderungen](https://docs.xcp-ng.org/installation/requirements/).
- Sichern Sie alle Daten auf den Datenträgern, die Sie verwenden werden. **Die Installation löscht die ausgewählten Datenträger.**
- Mindestens 100 GB auf dem Installationsdatenträger, dazu Platz für Ihre VMs.
- Eine stabile Verwaltungs-IP-Adresse, Gateway, DNS und NTP. Eine statische Adresse oder eine DHCP-Reservierung macht den Host leichter auffindbar.
- Ein zweiter Computer mit Browser und Netzwerkzugang zum Host.

## ISO auf einen USB-Stick schreiben

Laden Sie das XCP-ng-8.3-ISO von der [Upstream-Downloadseite](https://xcp-ng.org/download/) herunter und schreiben Sie es auf einen USB-Stick. Das Schreiben löscht den USB-Stick, ermitteln Sie also zuerst mit `dmesg`, welches Gerät der USB-Stick ist, und ersetzen Sie `sdX` unten durch dieses Gerät:

```bash
sudo dd if=xcp-ng-8.3.0-20250606.iso of=/dev/sdX bs=8M oflag=direct
```

Prüfen Sie den Gerätenamen noch einmal, bevor Sie den Befehl ausführen: Das Schreiben auf den falschen Datenträger löscht diesen. Warten Sie, bis die Kopie abgeschlossen ist; je nach USB-Stick kann das eine Weile dauern.

## XCP-ng installieren

XCP-ng ist ein Typ-1-Hypervisor und dafür gedacht, das einzige System auf dem Rechner zu sein. Stecken Sie den USB-Stick an, booten Sie davon und drücken Sie an der Boot-Aufforderung die Eingabetaste.

1. **Wählen Sie Ihr Tastaturlayout** und lesen Sie danach den Installationshinweis und die Lizenzvereinbarung, bevor Sie fortfahren.

   {{< screenshot src="install/keyboard.jpg" alt="Auswahl des Tastaturlayouts im Installer" >}}

2. **Wählen Sie den Systemdatenträger und den Datenträger für die VM-Speicherung.** Prüfen Sie Gerätenamen und Kapazitäten; wählen Sie weder den USB-Installer noch einen Datenträger, dessen Daten Sie behalten möchten.

   {{< screenshot src="install/system-disk.jpg" alt="Auswahl des Systemdatenträgers" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Auswahl des Datenträgers für die Speicherung virtueller Maschinen" >}}

3. **Wählen Sie den Speichertyp.** EXT (Thin Provisioning) belegt nur den Platz, den Ihre Daten tatsächlich brauchen: eine virtuelle Platte mit 1 TB, auf der 20 GB Daten liegen, belegt etwa 20 GB auf dem Host, wachsen aber die Datenträgerdatei beim Hinzufügen von Daten. LVM (Thick Provisioning) reserviert die volle Kapazität von Anfang an und vermeidet dieses Wachstum, kostet aber den Platz. EXT ist eine pragmatische Wahl für ein Homelab; LVM eignet sich für leistungskritische Workloads. Die Platte können Sie später in Xen Orchestra erweitern.

   {{< screenshot src="install/storage-type.jpg" alt="Wahl zwischen EXT- und LVM-Speicher" >}}

4. **Verwenden Sie Local media als Installationsquelle** und führen Sie die Medienprüfung durch, wenn sie angeboten wird, besonders wenn Sie einen beschädigten Download oder USB-Stick vermuten.

   {{< screenshot src="install/source.jpg" alt="Auswahl von Local media als Installationsquelle" >}}

5. **Legen Sie das Root-Passwort fest und merken Sie es sich.** Das ist das wichtigste Passwort der Plattform; bewahren Sie es sicher auf. Sie verwenden es für die Anmeldung an XO Lite und zum Verbinden des Hosts mit Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Festlegen des Root-Passworts des Hosts" >}}

6. **Konfigurieren Sie Verwaltungsnetzwerk und DNS.** Verwenden Sie eine statische Adresse oder eine DHCP-Reservierung; ein VLAN nur, wenn Ihr Netzwerk es erfordert. Geben Sie den Hostnamen und erreichbare DNS-Server ein. Würde sich die Adresse später ändern, bräuchten Sie DNS in Ihrem Labor, um den Host wiederzufinden.

   {{< screenshot src="install/network.jpg" alt="Konfiguration der Verwaltungs-IP-Adresse und des Gateways" >}}
   {{< screenshot src="install/dns.jpg" alt="Konfiguration von Hostname und DNS-Servern" >}}

7. **Stellen Sie Zeitzone und NTP-Server ein und prüfen Sie die Installation.** Verwenden Sie öffentliche NTP-Server, wenn der Host Internetzugang hat, sonst einen internen NTP-Server. Bestätigen Sie die ausgewählten Datenträger, bevor Sie die Installation starten.

   {{< screenshot src="install/ntp.jpg" alt="Konfiguration der Zeitsynchronisation" >}}
   {{< screenshot src="install/confirm.jpg" alt="Abschließende Installationsbestätigung" >}}

8. **Beenden Sie die Installation, entfernen Sie das Installationsmedium und starten Sie neu.** Notieren Sie die auf der Host-Konsole angezeigte Verwaltungsadresse.

   {{< screenshot src="install/complete.jpg" alt="Installation abgeschlossen, bereit zum Neustart" >}}

## Nach dem ersten Start: XO Lite

Die Host-Konsole bietet nur grundlegende Verwaltung für diesen einen Host (Netzwerk, VMs, Ressourcen, Backup und Wiederherstellung). Die andere Möglichkeit, einen einzelnen Host zu verwalten, ist XO Lite, die Web-Oberfläche, die der Host auf dem Standard-HTTPS-Port bereitstellt: Öffnen Sie `https://<Ihre-Host-IP>` (oder `https://<Hostname>`) im Browser. Der Host verwendet anfangs ein selbstsigniertes Zertifikat; stellen Sie sicher, dass Sie sich mit Ihrem eigenen Host verbinden, bevor Sie es akzeptieren. Melden Sie sich als `root` mit dem bei der Installation festgelegten Passwort an.

## XOA bereitstellen

XOA (Xen Orchestra) ist die Webanwendung, die einen oder mehrere XCP-ng-Hosts und deren VMs verwaltet. Sie läuft als virtuelle Maschine auf dem Host.

1. Klicken Sie in XO Lite auf **Deploy XOA** und wählen Sie das Appliance-Image. In XCP-hl ist **XOA-hl** die Vorauswahl; siehe [Erste Schritte](/docs/start/).
2. Füllen Sie die im Formular angezeigten Netzwerk- und Bereitstellungsfelder aus, prüfen Sie das ausgewählte Image und die Anmeldedaten und klicken Sie auf **Deploy**.
3. Warten Sie, bis die Appliance-VM gestartet ist, öffnen Sie deren Adresse im Browser und melden Sie sich an. Die Appliance hat eine eigene Adresse, die sich von der XO-Lite-Adresse des Hosts unterscheidet.

Sobald der Host in Xen Orchestra verbunden ist (`Settings → Servers → Add server` mit Host-Adresse und Root-Anmeldedaten), laden Sie ein Installations-ISO in die ISO-Bibliothek hoch und erstellen Sie Ihre erste VM. Die [Upstream-Installationsanleitung](https://docs.xcp-ng.org/installation/install-xcp-ng/) beschreibt weitere Optionen.
