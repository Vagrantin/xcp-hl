---
title: Änderungsprotokoll
weight: 2
translationKey: changelog
aliases: ["/de/changelog.html"]
---

Projektweite Änderungen über alle XCP-hl-Repositorys hinweg, mit den dadurch gelösten Issues. Die Komponentenversionen pro Veröffentlichung finden Sie in der [Versionsmatrix](/docs/reference/release-matrix).
{class="lead"}

## Automatisch erzeugte Versionshinweise {#generated-release-notes}

{{< changelog-releases >}}

## Frühere Projektänderungen {#earlier-project-changes}

## September 2026 {#september-2026}

### Die bereitgestellte XOA-VM heißt XOA-hl, behebt [#97](https://github.com/Vagrantin/xcp-hl/issues/97) {#the-deployed-xoa-vm-is-named-xoa-hl-fixes-97}

Die Bereitstellung der XOA-hl-Appliance aus XO Lite erzeugte eine VM namens `xoa-almalinux`, dem internen Packer-Buildnamen statt eines Produktnamens. XO Lite benennt importierte VMs nicht um: `VM.import` behält das im XVA enthaltene name-label bei, das genau dem `vm_name` des Builders entspricht. Der Build setzt `vm_name` jetzt auf **`XOA-hl`**, sowohl in `setup-xoa-builder.sh` von [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) (manuelle Builds) als auch im `xoa-vm-agent` des Orchestrators (die tägliche Pipeline, die Images veröffentlicht).

Da Packer den XVA-Dateinamen aus `vm_name` ableitet, ändert sich auch der Name des Release-Artefakts: Aus `xoa-almalinux.xva` wird `XOA-hl.xva`. Kein Verbraucher sucht das Artefakt anhand seines Namens: Die Bereitstellungsschaltfläche von XO Lite und die Releaseprüfung des Agenten wählen beide das erste `.xva`- / `.xva.gz`-Artefakt der neuesten `xoa-image-*`-Veröffentlichung. Bereits veröffentlichte Images funktionieren daher weiter; kein ISO muss neu herausgegeben werden.

Der Name gilt für Images, die nach dieser Änderung gebaut werden. Bereits bereitgestellte Appliances behalten den alten Namen und können in XO umbenannt werden. Orchestrator-Hosts mit einer älteren `/etc/xcp-orchestrator/build.config` behalten ihr eigenes `VM_NAME` (`deploy.sh` überschreibt eine vorhandene Konfiguration nie); dieser Schlüssel muss dort manuell aktualisiert werden.

### Standard-ISO-Speicher, schließt [#2](https://github.com/Vagrantin/xcp-hl/issues/2) und [#46](https://github.com/Vagrantin/xcp-hl/issues/46) {#default-iso-storage-closing-2-and-46}

Ein frisch installierter XCP-ng-Host hat keinen Ablageort für Installations-ISOs: Es gibt kein ISO-SR, und seine Erstellung erfordert manuell `xe sr-create` für ein zuvor selbst angelegtes Verzeichnis. XCP-hl reserviert jetzt bei der Installation eine Partition mit 20 GB, formatiert sie als ext4 mit Label `xcphl-iso`, hängt sie unter `/var/opt/xen/xcp-hl-iso` ein und registriert sie beim ersten Start als ISO-SR namens **XCP-HL ISO library**. Es kann sofort aus Xen Orchestra mit Dateien befüllt werden.

Damit liegt die Mindestgröße des Datenträgers für XCP-hl bei **100 GB**: etwa 41,5 GB Systempartitionen, 20 GB ISO-Bibliothek und etwa 38,5 GB VM-Speicher. Unterhalb dieser Grenze entfällt die Reservierung, statt den VM-Speicher auf wenige GB zu verkleinern. Die Datenträgeraufteilung entspricht dann genau dem ursprünglichen XCP-ng.

Issue [#46](https://github.com/Vagrantin/xcp-hl/issues/46) fragte, ob der Upload-Endpunkt von XCP-ng eine ISO-spezifische Route erhalten könnte. Dies erwies sich als unnötig: `PUT /import_raw_vdi` ist ein generischer Roh-VDI-Import, den XO 5 bereits über *Import → Disk* verwendet. Es fehlte lediglich ein ISO-SR als Importziel. Es wurde kein neuer Endpunkt hinzugefügt.

Die Partition wird vom Installer erstellt und gilt deshalb nur für XCP-hl-Neuinstallationen. Ursprünglich mit XCP-ng installierte Hosts, denen später XCP-hl-Repositorys hinzugefügt werden, werden nie neu partitioniert. Upgrades behalten die vorhandene Partition bei, statt sie neu anzulegen.

Umgesetzt durch Patchen von `host-installer` innerhalb von `install.img` beim ISO-Build, statt ein geforktes `host-installer`-RPM auszuliefern. Siehe [xcp-ng-ce-iso](/docs/components/xcp-ng-ce-iso#host-installer-patching).

## August 2026 {#august-2026}

### Versionsmatrix nennt das exakt ausgelieferte Paket, Fortschritt zu [#15](https://github.com/Vagrantin/xcp-hl/issues/15) {#release-matrix-states-the-exact-package-shipped-towards-15}

Die [Versionsmatrix](/docs/reference/release-matrix) dokumentierte zuvor nur ein Release-Tag je Komponente. Bei `xoa-proxy` genügte das nicht, um den Stand eines Hosts zu identifizieren: Das Tag entspricht einer Version, aber das RPM-Release-Feld enthält CI-Lauf und Quellcommit. Die beiden ältesten Zeilen tragen zudem ein Buildlauf-Tag `v-proxy-automated-*`, das überhaupt keine Version angibt.

Jede ISO-Zeile zeigt jetzt unter einer mit der Release-Seite verlinkten Version das Paket genau wie in der Ausgabe von `rpm -q` (`xoa-proxy-0.1.1.8-55.gc525575.static.x86_64`), für ISO, `xolite-ce` und `xoa-proxy` gleichermaßen. Vorhandene Zeilen wurden anhand veröffentlichter Release-Artefakte ergänzt. Die xo-lite-Upstream-Version für `v8.3-ce3` / `v8.3-ce4` wurde von 0.22.0 auf 0.21.0 korrigiert, passend zum tatsächlich ausgelieferten RPM. Der Orchestrator erfasst das neue Feld bei jedem Build (`xcp-orchestrator` `shared/src/github.rs`).

---

## Juli 2026 {#july-2026}

### XOA-VM-Image-Veröffentlichungen nach build-xoa-hl verschoben, behebt [#22](https://github.com/Vagrantin/xcp-hl/issues/22) {#xoa-vm-image-releases-moved-to-build-xoa-hl-fixes-22}

Die XOA-hl-VM (`xoa-image-<date>-<sha7>`, Artefakt `xoa-almalinux.xva`) wurde zuvor in [`xoa-hl`](https://github.com/Vagrantin/xoa-hl), dem Repository der *Software*, zwischen dessen RPM-Veröffentlichungen publiziert. Sie erscheint jetzt in [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl), das tatsächlich das Image erstellt. Der `xoa-vm-agent` des Orchestrators legt dort die Veröffentlichung an, und die Bereitstellungsschaltfläche von XO Lite ermittelt das neueste Image aus diesem Repository.

Die Vermischung hatte eine konkrete Auswirkung: `releases/latest` auf `xoa-hl` verwies auf eine Image-Veröffentlichung ohne RPM-Artefakt. Das unterbrach die RPM-Suche in `build-xoa-hl/scripts/setup-xoa-builder.sh`; diese durchsucht jetzt die Veröffentlichungen nach der neuesten mit tatsächlichem RPM.

Image-Veröffentlichungen von vor dem Umzug bleiben auf `xoa-hl`, damit bereits ausgelieferte ISOs sie weiter auflösen können. Die [Versionsmatrix](/docs/reference/release-matrix#xoa-hl-releases) verlinkt jeden Eintrag auf das jeweils hostende Repository.

### Versionsmatrix erfasst XOA-Versionen, behebt [#13](https://github.com/Vagrantin/xcp-hl/issues/13) {#release-matrix-records-xoa-versions-fixes-13}

Die [Versionsmatrix](/docs/reference/release-matrix) hat jetzt eine eigene Tabelle **XOA-Appliance-Veröffentlichungen**. Sie erfasst jedes veröffentlichte VM-Image (`xoa-image-*`-Veröffentlichung auf `Vagrantin/xoa-hl`), dessen `xoa-hl`-Softwareversion und die Upstream-Version von Xen Orchestra, von der es abgeleitet wurde. Aus der ISO-Tabelle wurde außerdem die nie befüllte Spalte `xoa-hl` entfernt: Die Appliance wird zum Bereitstellungszeitpunkt ermittelt und unabhängig vom ISO versioniert.

### XOA-hl-Edition fertiggestellt, behebt [#1](https://github.com/Vagrantin/xcp-hl/issues/1), [#6](https://github.com/Vagrantin/xcp-hl/issues/6) {#xoa-hl-edition-complete-fixes-1-6}

Xen Orchestra HomeLab Edition wird jetzt aus dem Quellcode erstellt, verpackt und kann durchgängig bereitgestellt werden:

- [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) erstellt XO 5.113.2 (die letzte XO-5.x-Veröffentlichung) aus einem festen Upstream-Commit und passt die Oberfläche an: Lizenzabhängige Menüpunkte (Hub, XOA, Proxies, XOSTOR) und das Banner für fehlenden Support werden ausgeblendet (`patches/menu-hide-items.patch`).
- [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) verpackt es mit Packer auf XCP-ng in eine sich selbst konfigurierende XVA-Appliance.
- Die XO-Lite-Bereitstellungsansicht bietet jetzt **XOA HomeLab (latest build)** als Imageoption und ermittelt bei der Bereitstellung das neueste vom Agenten erstellte XVA aus GitHub-Veröffentlichungen (`xolite-ce`-Commit `6abd43f`, 2026-07-14).

### Veröffentlichung automatisiert, behebt [#4](https://github.com/Vagrantin/xcp-hl/issues/4) {#release-publication-automated-fixes-4}

Versionierung und Versionshinweise werden jetzt in jeder Pipeline automatisch abgeleitet:

- `xolite-ce` und `xoa-proxy` ermitteln Release-Tag und RPM-Version in CI (`xolite-ce` `7b2e4d4`, `xoa-proxy` `9582718`). `xoa-proxy` verwendet automatisch erzeugte GitHub-Versionshinweise; `xolite-ce` und das ISO enthalten strukturierte Release-Texte mit Quellversionen und Prüfschritten.
- Der Orchestrator startet den ISO-Build mit exakten Komponenten-Release-Tags als Workflow-Eingaben. Dies verhindert Wettläufe mit veralteten RPMs (`xcp-ng-ce-iso` `68f211d`).
- Jede ISO-Veröffentlichung wird in der [Versionsmatrix](/docs/reference/release-matrix) erfasst.

---

## Juni 2026 {#june-2026}

### CI/CD für die Dokumentationswebsite, behebt [#5](https://github.com/Vagrantin/xcp-hl/issues/5) {#documentation-website-cicd-fixes-5}

Die Projektwebsite (diese Website) wird mit Jekyll erstellt und bei jedem Push auf `main` von [`xcp-hl`](https://github.com/Vagrantin/xcp-hl) automatisch auf GitHub Pages veröffentlicht (`.github/workflows/pages.yml`). Sie ist damit die maßgebliche Quelle für den Projektstatus einschließlich der datenbasierten Versionsmatrix.

### v8.3-ce9 veröffentlicht {#v83-ce9-released}

- xolite-ce `v0.21.0-ce6`: Upstream-xo-lite über die Datei `UPSTREAM_TAG` auf `0.21.0` festgelegt, die letzte als funktionierend bekannte Veröffentlichung (`0.22.0` und `0.23.0` ließen den Build fehlschlagen).
- xoa-proxy `v0.1.1.x`: einfachere RPM-Versionierung (Release-Suffix `.static`) und automatisierte, kategorisierte GitHub-Versionshinweise.
- Einheitliche Artefaktnamen: `xcp-ng-8.3-ceN.iso`, `.iso.sha256` und `.iso.sha256.asc`, veröffentlicht als GitHub-Releases von `xcp-ng-ce-iso`.

---

## Mai 2026 {#may-2026}

### GPG-Schlüsselmodell umgesetzt, behebt [#3](https://github.com/Vagrantin/xcp-hl/issues/3) {#gpg-key-model-implemented-fixes-3}

Die GPG-Signierung ist über alle Buildpipelines vereinheitlicht. Sie verwendet das Modell **Offline-Hauptschlüssel mit zwei Signatur-Unterschlüsseln**: Einer signiert die RPMs (`xo-lite-ce`, `xoa-proxy`), der andere die ISO-Prüfsummendatei. Der öffentliche Schlüssel ist auf [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) veröffentlicht; jede Veröffentlichung enthält Prüfschritte. Details unter [GPG-Signierung](/docs/components/#gpg-signing). Eine weitere Verfeinerung (ein Schlüssel je Modul) bleibt auf der [Roadmap](/docs/reference/roadmap#gpg-keys-one-signing-key-per-module).

### Erste öffentliche Veröffentlichung, v8.3-ce alpha2 {#first-public-release-v83-ce-alpha2}

- Erste nutzbare Veröffentlichung.
- Bereitstellung von XOA aus dem Vates-Image, Ronivays Image oder einer eigenen URL.
- **GPG**: Offline-Hauptschlüssel und eigene RPM-/ISO-Signatur-Unterschlüssel. Öffentlicher Schlüssel auf keys.openpgp.org veröffentlicht.

---

## April 2026 {#april-2026}

### Erster Build, v8.3-ce {#first-build-v83-ce}

- XO Lite angepasst: Community-Bereitstellungsendpunkt und schreibgeschützte Zugangsdatenfelder.
- Rust-Server `xoa-proxy` integriert: HTTP/HTTPS und gzip-Streaming.
- ISO aus Upstream-XCP-ng 8.3 mit zusätzlichem Community-RPM-Repository zusammengestellt.
- GPG-Schlüsselinfrastruktur (RSA mit 4096 Bit, einzelner Schlüssel `RPM-GPG-KEY-xcp-ng-ce`).
- GitHub-Actions-CI/CD-Pipeline: RPM-Build → ISO-Build → GitHub Releases.
