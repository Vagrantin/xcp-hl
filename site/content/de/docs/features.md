---
title: Funktionen
weight: 3
translationKey: features
aliases: ["/de/features.html", "/de/docs/guides/features/"]
---

Aktuelle Veröffentlichung · {{< latest-release part="version" >}} · {{< latest-release part="date" >}} · Auf Basis von XCP-ng 8.3
{class="lead"}

## Basisplattform {#base-platform}

XCP-hl basiert auf **XCP-ng 8.3**, mit Änderungen am Installationsprogramm, an XO Lite, der XOA-Bereitstellung und der Paketverteilung. Die Basisplattform verwendet den Hypervisor und den Verwaltungsstack des Upstream-Projekts; dessen Hardware- und Funktionsanforderungen gelten weiterhin.

| Eigenschaft | Wert |
|---|---|
| Basisversion | XCP-ng 8.3 (neueste Upstream-Punktversion) |
| Hypervisor | Xen 4.17 |
| Dom0-Kernel | Linux 4.19 (XCP-ng-Kernel) |
| Verwaltungs-API | XAPI (Xen API) |
| Standardnetzwerk | Open vSwitch (OVS) |
| Installationsprogramm | XCP-ng-Textinstaller |

---

## Anpassungen {#customisations}

### Angepasstes XO Lite {#patched-xo-lite}

XO Lite ist die schlanke Verwaltungsoberfläche als Single-Page-Anwendung, die mit jedem XCP-ng-Host ausgeliefert wird. XCP-hl ändert darin eine Ansicht: Beim Build schreibt ein automatisiertes Werkzeug kleine, gezielte Teile von `xoa-deploy.vue` um (den genauen Mechanismus beschreibt [Komponenten](/docs/components/xolite-ce)).

Die Upstream-Version von xo-lite wird über die Datei `UPSTREAM_TAG` in `xolite-ce` festgelegt (derzeit `xo-lite-v0.21.0`, die letzte als funktionierend bekannte Version) und ändert sich nur bei einer bewussten Aktualisierung dieser Festlegung.

**Was der Patch ändert:**

Die Ansicht **"Deploy XOA"** enthält jetzt eine Auswahl **"XOA Image URL"**, mit der Sie Ihre XO-Bereitstellung auswählen.

Alles andere in XO Lite (VM-Verwaltung, Konsolenzugriff, SR-Ansicht, Hostmetriken) bleibt unverändert.

### xoa-proxy: lokale XVA-Bereitstellung {#xoa-proxy-local-xva-delivery}

Ein eigens entwickelter **Rust-HTTP-Server** (`xoa-proxy`) ist im ISO enthalten und läuft auf dem Host. Er:

- Stellt das XOA-Community-Image bereit und unterstützt das gzip-komprimierte Format.
- Unterstützt HTTP und HTTPS (einschließlich selbstsignierter Zertifikate).

### HomeLab-XOA-Image *(Standard)* {#homelab-xoa-image-default}

Das vom Proxy bereitgestellte XOA-Image ist [`xoa-hl`](https://github.com/Vagrantin/xoa-hl): Xen Orchestra, für XCP-hl aus dem Quellcode erstellt, ohne lizenzabhängige Menüpunkte und Supportbanner. Unter [Komponenten](/docs/components/xoa-hl) erfahren Sie, wie es gebaut wird.

### Ronivays XOA-Image {#ronivays-xoa-image}

Das vom Proxy bereitgestellte XOA-Image wird mit [ronivay/XenOrchestraInstallerUpdater](https://github.com/ronivay/XenOrchestraInstallerUpdater) erstellt, einem gut gepflegten Community-Installer für selbst betriebenes Xen Orchestra.

| Detail | Wert |
|---|---|
| XO-Version | Folgt der neuesten stabilen XO-Veröffentlichung |
| Standard-Administrator | `admin@admin.net` |
| Standard-Administratorpasswort | `admin` |
| SSH-Benutzer | `xo` |
| SSH-Passwort | `xopass` |

{{< callout type="warning" >}}
**Ändern Sie die Standardpasswörter unmittelbar** nach der ersten Anmeldung.
{{< /callout >}}

### Vates-XOA-Image {#vates-xoa-image}

Dies ist das offizielle Image von Vates zur Verwaltung mehrerer XCP-ng-Hosts. In diesem Fall können Sie die Zugangsdaten während der Bereitstellung festlegen.

### Eigenes Image {#custom-image}

Jedes XVA, unkomprimiert oder gzip-komprimiert, das über HTTP oder HTTPS bereitgestellt wird. Geben Sie in der Bereitstellungsansicht Ihre eigene URL ein: einen eigenen Build, eine aufbewahrte ältere Version oder ein Image auf einem beliebigen vom Host erreichbaren Server. Die Zugangsdatenfelder bleiben zum Ausfüllen leer; es wird nichts vorausgefüllt, da XCP-hl die Erwartungen des Images nicht kennen kann.

---

## GPG-Signierung {#gpg-signing}

Alle XCP-hl-Artefakte werden mit dem **XCP-hl-GPG-Schlüssel** signiert. So kann jeder bestätigen, dass ein Paket oder ISO tatsächlich aus diesem Projekt stammt und nicht verändert wurde. Dieser Abschnitt dient als Referenz für Ihre eigene Prüfung; die meisten Leser können direkt zu [Funktionsübersicht](#what-you-get-full-feature-summary) springen.

### Schlüsselstruktur {#key-structure}

Der Schlüssel folgt einem Modell mit **Offline-Hauptschlüssel und Unterschlüsseln**:

| Rolle | Beschreibung |
|---|---|
| Hauptschlüssel | Nur zur Zertifizierung: offline aufbewahrt und nie zum Signieren verwendet |
| RPM-Signatur-Unterschlüssel | Signiert alle Community-RPM-Pakete (`xo-lite-community`, `xoa-proxy`) |
| ISO-Signatur-Unterschlüssel | Signiert die ISO-Prüfsummendatei (`xcp-ng-8.3-ceN.iso.sha256.asc`) |

| Eigenschaft | Wert |
|---|---|
| Schlüssel-UID | `XCP-ng Community Edition (Master signing key)` (Ausgabe von `gpg --list-keys`) |
| Fingerabdruck des Hauptschlüssels | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| Veröffentlicht | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| E-Mail | `xcp-ng-ce.lid530@passmail.com` |
| Öffentliche Schlüsseldatei | [`xcp-ng-ce-public.asc`](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) |

Die öffentliche Schlüsseldatei enthält beide Signatur-Unterschlüssel. Ein einmaliger Import genügt, um RPMs und ISO-Prüfsumme zu prüfen.

---

## Funktionsübersicht {#what-you-get-full-feature-summary}

### Hypervisor und Hostverwaltung {#hypervisor--host-management}

- **Vollständiger Funktionsumfang von XCP-ng 8.3**: alle VM-Typen (HVM, PV, PVH), Live-Migration (XenMotion), Storage XenMotion.
- **Storage Repositories**: lokales LVM, NFS, iSCSI (LVM und EXT), HBA/FC, XOSTOR (hyperkonvergiert), SMB, ISO-SR.
- **Sofort nutzbare ISO-Bibliothek**: Eine dedizierte Partition mit 20 GB wird bei der Installation reserviert und beim ersten Start als ISO-SR registriert. Sie können Installations-Images hochladen und VMs erstellen, ohne Speicher manuell einzurichten. Siehe [ISO-Speicher](#iso-storage).
- **GPU/vGPU**: PCI-Passthrough und NVIDIA-GRID-vGPU-Unterstützung.
- **HA**: Hochverfügbarkeit im Pool mit automatischem Neustart von VMs bei Hostausfall.

### ISO-Speicher {#iso-storage}

Direkt nach der Installation bietet XCP-ng keinen Ablageort für Installations-ISOs: Es gibt kein ISO-SR, und seine Erstellung erfordert die manuelle Auswahl eines Pfads, das Anlegen eines Verzeichnisses und `xe sr-create`. XCP-hl übernimmt das für Sie.

**Was Sie erhalten.** Eine Neuinstallation reserviert eine Partition mit 20 GB, formatiert sie mit ext4 und dem Label `xcphl-iso`, hängt sie unter `/var/opt/xen/xcp-hl-iso` ein und registriert sie in XAPI als ISO-SR namens **XCP-HL ISO library**. Es erscheint sofort in Xen Orchestra. Sie können ein ISO hochladen (*Import → Disk*, ISO-SR auswählen) und ohne weitere Einrichtung eine VM davon starten.

**Datenträgeranforderung.** XCP-hl sieht einen Datenträger mit **100 GB** vor, der ungefähr so aufgeteilt wird:

| Bereich | Größe |
|---|---|
| Systempartitionen (root, backup, boot, logs, swap) | ~41,5 GB |
| ISO-Bibliothek | 20 GB |
| Lokales Speicher-SR (VM-Datenträger) | ~38,5 GB |

Unter 100 GB entfällt die Reservierung, statt den VM-Speicher auf wenige GB zu verkleinern. Die Installation wird dennoch abgeschlossen, und der Datenträger wird genau wie beim ursprünglichen XCP-ng aufgeteilt. Sie erhalten lediglich keine ISO-Bibliothek; eine Zeile in `/var/log/installer` dokumentiert den Grund.

**Geltungsbereich.** Die Partition wird vom Installationsprogramm erstellt und existiert deshalb nur auf Hosts, die von einem XCP-hl-ISO installiert wurden. Ein ursprünglich mit XCP-ng installierter Host behält seine Datenträgeraufteilung, wenn später XCP-hl-Repositorys hinzugefügt werden: Ein laufender Rechner wird nicht neu partitioniert. Solche Hosts können weiterhin wie gewohnt manuell ein ISO-SR erstellen.

Beim Upgrade eines vorhandenen XCP-hl-Hosts bleibt die Partition erhalten, da Upgrades nie neu partitionieren. Das ISO-SR wird anhand seines Dateisystem-Labels wieder erkannt.

**Bekannte Einschränkung.** Wenn Sie das PBD des SR trennen und *ohne* Neustart wieder verbinden, bindet XAPI es erneut an, das Dateisystem bleibt aber ausgehängt. Die Bibliothek erscheint bis zum nächsten Neustart leer. Das ergibt sich aus dem Umgang von XCP-ng mit lokalen ISO-SRs (`legacy_mode`) und betrifft das integrierte XCP-ng-Tools-SR ebenso. Ein Neustart oder `mount /var/opt/xen/xcp-hl-iso` stellt den Zugriff wieder her.

### XO Lite (schnelle Verwaltung im Browser) {#xo-lite-browser-based-quick-management}

Unmittelbar nach der Installation unter `https://<host-ip>` verfügbar:

- Pool- und Hostübersicht (CPU, RAM und Speicher auf einen Blick).
- VM-Liste: starten, stoppen, neu starten und auf die Konsole zugreifen.
- Grundlegende SR- und Netzwerkansicht.
- **HomeLab-Bereitstellung**: XOA-Bereitstellung mit einem Klick, ohne externe Verbindung, wenn Sie Ihr XOA-Image lokal bereitstellen.

### XOA-hl: die Verwaltungsoberfläche {#xen-orchestra-after-xoa-deployment}

Mit dem hl-Image erhalten Sie Xen Orchestra in einer eigenen VM. XOA-hl bietet:

- **Host- und VM-Verwaltung** über die Oberfläche von Xen Orchestra 5: Ressourcen prüfen und virtuelle Maschinen verwalten.
- **Sicherungs- und Planungseinstellungen** der aus Quellcode erstellten Xen-Orchestra-Anwendung.
- **XCP-hl-Hostupdates** in den Patches-Registerkarten von Host und Pool, einschließlich der XCP-hl-Repositorys.
- **Appliance-Update-Einstellungen** unter Settings → XOA-HL Updates. Host und Appliance werden separat aktualisiert.
- **Übersichtliche Menüs**: Der Vates-Appliance-Updater sowie die Einträge Hub, Proxies und XOSTOR sind ausgeblendet; das Community-Banner verlinkt zur XCP-hl-Dokumentation.

Diese Beschreibung basiert auf der `xoa-hl`-Veröffentlichung `v5.113.2_e281c536-ce20`, die Xen Orchestra auf `5.113.2` festlegt. Andere Images haben eigene Funktionen und Aktualisierungsverfahren. Siehe [Updates](/docs/guides/updates) und die [XOA-hl-Komponente](/docs/components/xoa-hl).

---

## Bekannte Einschränkungen dieser Veröffentlichung {#known-limitations-in-this-release}

| Einschränkung | Status |
|---|---|
| Xolite-ce: Deploy-Schaltfläche immer verfügbar | [#31](https://github.com/Vagrantin/xcp-hl/issues/31): nach erfolgreicher Bereitstellung in "Access XOA" ändern |
| Xoa-proxy: Protokolle verwenden UTC | [#62](https://github.com/Vagrantin/xcp-hl/issues/62): Untersuchung ausstehend |
| Xoa-proxy: Anzahl der Crates verringern | [#63](https://github.com/Vagrantin/xcp-hl/issues/63): Untersuchung ausstehend |
| Xoa-proxy: Speicherbedarf verringern | [#64](https://github.com/Vagrantin/xcp-hl/issues/64): xoa-proxy läuft in Dom0; seine Speichernutzung muss begrenzt bleiben |

---

## Neueste Veröffentlichungen {#recent-releases}

Die fünf neuesten ISO-Veröffentlichungen mit den jeweils ausgelieferten Komponentenversionen. Alle Veröffentlichungen finden Sie in der [Versionsmatrix](/docs/reference/release-matrix); Änderungen und deren Gründe beschreibt das [Änderungsprotokoll](/docs/reference/changelog).

{{< release-matrix-iso limit="5" rpm="false" >}}
