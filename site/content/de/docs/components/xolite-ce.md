---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/de/developers/xolite-ce.html"]
---

XO Lite für XCP-hl neu gebaut: auswählbare XOA-Bereitstellungsimages und die RPM-Buildpipeline.
{class="lead"}

**Repository:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Sprache: TypeScript / Vue 3 (Patch) · RPM-Spezifikation · Lizenz: AGPL-3.0

## Was ist XO Lite? {#what-is-xo-lite}

XO Lite ist die schlanke Verwaltungsanwendung als einzelne Webseite, die mit jedem XCP-ng-Host ausgeliefert wird. Sie läuft vollständig im Browser, wird direkt vom Host bereitgestellt und ist als Vue-3-/TypeScript-/Vite-SPA umgesetzt.

Auf einem regulären XCP-ng-Host lädt und importiert die XO-Lite-Ansicht **"Deploy XOA"** ein fest vorgegebenes Xen-Orchestra-Image. XCP-hl ersetzt diese Ansicht durch eine Auswahl **"XOA Image URL"** mit vier Quellen: XOA-hl (Standard), offizielles Vates-Image, Ronivays Image oder eine eigene XVA-URL. Hinzu kommt der Schalter **"Verify if ssl certificate is valid"**, mit dem `xoa-proxy` selbstsignierte Zertifikate der Image-Quelle akzeptieren kann.

---

## Patchen des Quellcodes {#source-patching}

Bei `xolite-ce@d452937` legt `UPSTREAM_TAG` `xo-lite-v0.21.0` auf `13f987ff3d34504a90b89178489e15fa2293d1b3` fest. Diese Basis verwendet ein mitgeliefertes Rust-Programm für `xoa-deploy.vue`, dazu einen Unified Diff für `XoaButton.vue` sowie explizite Transformationen für Sprachdateien, Loader, Host-/Gast-Versionen und Deploy-Geheimnisse. Nachweis: `xolite-ce/.github/workflows/build-xolite-ce.yml@d452937` und `xolite-ce/UPSTREAM_TAG@d452937`.

[Der Migrations-PR](https://github.com/Vagrantin/xolite-ce/pull/26) ersetzt das mitgelieferte Programm durch einen überprüfbaren Unified Diff. `patches/series` legt die Reihenfolge der Diffs fest, und `patches/metadata.toml` erfasst Zweck, Zuständigkeit, Upstream und Abhängigkeiten. Builds und Validierung teilen sich `scripts/patch-source.sh`. Transformationen von Assets und Sprachdateien ohne Diff bleiben explizit. Der Upstream-Pin und die endgültigen Quellbytes bleiben erhalten.

Siehe die [Bewertung des komponentenübergreifenden Patch-Modells](https://github.com/Vagrantin/xcp-hl/blob/main/docs/developers/patching-model-assessment.md) für den Entscheidungsdatensatz und den dort verlinkten Migrations-PR für den Umsetzungsstand. Die [Wartungsanleitung der Komponente](https://github.com/Vagrantin/xolite-ce/blob/7925dbc6bde35bfb387677b2c9c227ef05a886c0/docs/patching.md) beschreibt den Migrationszweig. Umsetzungsnachweis: `xolite-ce/scripts/patch-source.sh@7925dbc`,
`xolite-ce/scripts/list-patches.py@7925dbc`, and
`xolite-ce/ci/test-patch-migration.py@7925dbc`.

---

## Quellcode-Validierung {#source-validation}

Verwende einen sauberen, gepinnten Upstream-Checkout. Im migrierten XO-Lite-CE-Baum:

```sh
python3 scripts/list-patches.py patches
python3 ci/test-patch-series.py
bash scripts/patch-source.sh /path/to/clean/pinned/upstream
```

Die vollständige Serie wird geprüft, bevor irgendein Diff angewendet wird. Ungültige Namen, fehlende oder doppelte Einträge, Metadaten-Abweichungen und eine ungültige Abhängigkeitsreihenfolge lassen die Validierung fehlschlagen. Überspringe keine fehlgeschlagenen Patches und ersetze sie nicht durch einen Remote-Loader. Bestehende Quelltests prüfen die betroffene Oberfläche, die Sprachdateien und das Aufräumen des Deploys separat.

`docs/patch-migration.json` erfasst den Hash des alten Programms sowie die unveränderlichen Revisionen von Konsument, Upstream und Patcher-Quellcode. Der Migrationsabgleich vergleicht alle Quellbytes, ausführbaren Git-Modi und Symlink-Ziele zwischen der alten und der neuen Kette. Die CI baut zusätzlich die gepinnte Rust-Quelle erneut und gleicht ihre Ausgabe mit dem erfassten Programm ab. Das ist eine Verhaltens-Herkunft auf genau einer gepinnten Eingabe, keine historische binäre Reproduzierbarkeit.

---

## Builds und Abnahme {#builds-and-acceptance}

Alle Anwendungs- und RPM-Builds laufen in GitHub Actions. Die Migration ergänzt einen PR-Check für die vollständige Pipeline und die gepatchte Vue-Distribution, ohne ein Release zu veröffentlichen. Paketierung und Signierung bleiben in den bestehenden Komponenten-Workflows und in `SPECS/xo-lite-community.spec`.

Halte Quellanwendung, gehostete Anwendungsbuilts, RPM-Prüfungen und die Abnahme in der Installation als getrennte Ergebnisse. Während dieser Migration stand keine laufende Appliance zur Verfügung; das Verhalten in der Installation bleibt unverifiziert.

---

## GPG-Signierung {#gpg-signing}

Das `xo-lite-ce`-RPM wird mit dem **RPM-Signatur-Unterschlüssel** des XCP-hl-Schlüsselpaars signiert. Derselbe Unterschlüssel signiert auch die RPMs `xoa-proxy` und `xcp-hl-release`: Ein gemeinsamer Unterschlüssel wird für alle Community-RPMs verwendet.

Das Projekt veröffentlicht seinen gemeinsamen [öffentlichen Schlüssel](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) im Wurzelverzeichnis der Produktionswebsite. Prüfen Sie vor dem Import den Fingerabdruck des Hauptschlüssels. Die folgenden Befehle benötigen eine RPM-Implementierung mit Unterstützung für Signatur-Unterschlüssel. XCP-ng 8.3 Dom0 verwendet das ältere RPM 4.11; installierte Hosts prüfen stattdessen signierte Repository-Metadaten mit `repo_gpgcheck=1`. Behalten Sie die Repository-Einstellungen aus [Updates](/docs/guides/updates) unverändert bei.

So prüfen Sie das RPM lokal:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## Mitarbeit {#contributing}

Um ein Problem zu melden oder eine Änderung vorzuschlagen, erstellen Sie ein Issue unter [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
