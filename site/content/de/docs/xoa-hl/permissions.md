---
title: "Benutzer, Gruppen und Berechtigungen verwalten"
linkTitle: "Benutzer und Rechte"
description: "Benutzer und Gruppen erstellen, VM-Zugriff gewähren, Ressourcen delegieren und LDAP- oder SAML-Anmeldung testen."
weight: 70
translationKey: xoa-manual-permissions
translationStatus: draft
sourceRevision: sha256:7986e2d599b33c8226ca026293155fa3e4b8333a5816aa94d93ee28ffab32990
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Erstellen Sie einen Testbenutzer, geben Sie ihm Zugriff auf eine VM und testen Sie danach eine Gruppe, eine delegierte Ressourcenmenge und externe Anmeldung (LDAP oder SAML). Sie arbeiten als Administrator in der **XOA-HL-Appliance** und melden sich als Testbenutzer in einer zweiten getrennten Browsersitzung an. Verwenden Sie eine entbehrliche Test-VM. Lassen Sie Ihre Administratorsitzung durchgehend offen. Ändern Sie beim Testen niemals das letzte Administratorkonto oder Ihre eigenen Rechte. Einmalcodes für die Anmeldung eines lokalen Kontos beschreibt [Anmeldung mit einem Einmalcode schützen](/docs/xoa-hl/sign-in-otp/).

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Im standardmäßigen Open-Source-Plan dieses Builds aktiviert der Code die Seiten ACL und Self service: Ein Vates-Abonnement ist nicht erforderlich.
{{< /callout >}}

## Die beiden Rollenarten kennen {#roles}

**Settings → Users** (`/#/settings/users`) legt die globale Berechtigung jedes Kontos fest:

- **User** ist ein normales Konto.
- **Admin** ist ein Administrator und umgeht jede Objektregel.

Eine Zugriffsregel (ACL) gibt einem Benutzer oder einer Gruppe eine Rolle auf einem Objekt. Die Objektrolle **Admin** ist nicht der globale **Admin**: Sie gilt nur für das ausgewählte Objekt und dessen Geltungsbereich.

| Objektrolle | Erlaubte Aktionen |
| --- | --- |
| Viewer | Ansehen |
| Operator | Ansehen und bedienen |
| Admin | Ansehen, bedienen und administrieren |

Beginnen Sie mit **Viewer** auf einer Test-VM. Eine Host- oder Poolregel kann mehr Objekte freigeben als eine Regel für eine VM. Eine Gruppenregel gilt für alle Mitglieder. Berechtigungen addieren sich; eine verweigernde Regel gibt es nicht. Das Entfernen einer Regel beseitigt keinen Zugriff aus einer anderen Gruppe, einem anderen Objekt oder einem übergeordneten Objekt.

## Testbenutzer Zugriff auf eine VM geben {#vm-access}

Diese vier Abschnitte bilden einen Test: normalen Benutzer erstellen, **Viewer** auf einer entbehrlichen VM vergeben, Möglichkeiten prüfen und Zugriff wieder entfernen.

### Testbenutzer erstellen {#create-a-test-user}

1. Erstellen Sie unter **Settings → Users** einen getrennten Testbenutzer mit eigener E-Mail-Adresse oder Anmeldung und einem eindeutigen Passwort.
2. Wählen Sie **User**, nicht **Admin**. Prüfen Sie die angezeigte Kontoberechtigung.
3. Melden Sie sich in der zweiten Browsersitzung als dieser Benutzer an. Notieren Sie, was er vor dem Hinzufügen einer Regel sehen kann.

Prüfen Sie, dass dies wirklich der Testbenutzer und keine wiederverwendete Administratoranmeldung ist. Verwenden Sie keine echten Zugangsdaten und schreiben Sie niemals Passwörter in Notizen. Behalten Sie den Testbenutzer: Der folgende Gruppentest verwendet ihn erneut.

### Viewer auf einer VM vergeben {#grant-viewer}

1. Öffnen Sie als Administrator **Settings → ACLs** (`/#/settings/acls`).
2. Wählen Sie ausschließlich den Testbenutzer als Subjekt, ausschließlich die entbehrliche VM als Objekt und **Viewer** als Rolle. Wählen Sie **Create**.
3. Prüfen Sie Subjekt, Objekt und Rolle der neuen Zeile.

Wählen Sie weder alle Objekte noch den gesamten Pool. Das Formular akzeptiert mehrere Subjekte und Objekte und erstellt für jedes Paar eine Regel. Prüfen Sie Identitäten statt ähnlicher Anzeigenamen. Objekt- und Tagfilter wählen jetzt vorhandene Objekte aus; sie erstellen keine Regel für zukünftige Objekte.

### Möglichkeiten des Benutzers prüfen {#check-what-the-user-can-do}

1. Aktualisieren Sie die Testbenutzersitzung oder melden Sie sich erneut an.
2. Prüfen Sie sichtbare VM und lesbare Grundinformationen.
3. Prüfen Sie, dass Start-, Stopp- und Administrationsaktionen nicht verfügbar sind. Lässt sich eine Aktion dennoch anfordern, muss sie verweigert werden und die VM unverändert bleiben.

Testen Sie dies nur an der entbehrlichen VM. Eine verborgene Schaltfläche allein belegt keine serverseitige Verweigerung.

Gelingt unerwartet eine Aktion, halten Sie an. Prüfen Sie als Administrator globale Kontoberechtigung, Gruppen und andere Regeln auf VM, Host oder Pool. Erweitern Sie Rechte nicht, um einen unerklärten Zugriffsfehler zu beheben. Fehlt die ACL-Seite, notieren Sie Versionen und Fehler und [melden Sie dies](/docs/xoa-hl/troubleshooting/). Nehmen Sie keinen kostenpflichtigen Plan einer anderen Edition als erforderlich an.

### Widerrufen und erneut prüfen {#revoke-and-check-again}

1. Entfernen Sie als Administrator genau die Testregel.
2. Aktualisieren Sie die Testbenutzersitzung oder melden Sie sich erneut an. Prüfen Sie den verlorenen VM-Zugriff.
3. Prüfen Sie, dass Ihr Administrator weiterhin anmelden und die vorgesehenen Objekte verwalten kann.

Bleibt Zugriff bestehen, suchen Sie andere direkte, Gruppen- und geerbte Regeln: Das Entfernen einer Zeile beseitigt nicht jede Freigabe.

**Prüfung:** Der Benutzer konnte die VM lesen, aber nicht ändern, und verlor den Zugriff nach Regelentfernung. Notieren Sie Kontotyp, Regelumfang sowie erwartete und tatsächliche Ergebnisse ohne Zugangsdaten.

Behalten Sie den Testbenutzer bis zum Ende aller Tests dieser Seite. Delegation von Sicherungsaufträgen und API-Tokenumfang werden hier nicht behandelt. Lesen Sie vor umfassenderen Änderungen [Hosts und Pools](/docs/xoa-hl/hosts-pools/) und [exportieren Sie Ihre Konfiguration](/docs/xoa-hl/configuration-backup/).

## Zugriff über lokale Gruppen gewähren {#group-access}

Eine Gruppe wendet ihre Objektregeln auf alle Mitglieder an. Eine Gruppenzugehörigkeit ändert nicht die globale Benutzerberechtigung.

**Vor dem Beginn**

- Schließen Sie [Testbenutzer Zugriff auf eine VM geben](#vm-access) ab. Die direkte Regel muss entfernt sein; der Benutzer darf keinen VM-Zugriff aus einer anderen Gruppe oder einem übergeordneten Objekt erhalten.
- Verwenden Sie denselben normalen Testbenutzer und dieselbe entbehrliche VM.
- Halten Sie zum Vergleich ein zweites normales Testkonto außerhalb der Gruppe bereit.
- Lassen Sie die Administratorsitzung offen.

### Gruppe und Regel erstellen {#create-the-group-and-its-rule}

1. Öffnen Sie **Settings → Groups** (`/#/settings/groups`). Geben Sie unter **New group name** einen eindeutigen Namen wie `lab-vm-viewers` ein und wählen Sie **Create**.
2. Prüfen Sie die leere Benutzerliste der neuen Gruppe. Besteht der Name schon, wählen Sie einen anderen: Verwenden Sie keine unbekannte Gruppe mit deren Freigaben wieder.
3. Wählen Sie unter **Settings → ACLs** nur diese Gruppe als Subjekt, nur die Test-VM als Objekt und **Viewer** als Rolle. Wählen Sie **Create** und prüfen Sie genaue Gruppe, VM und Rolle der neuen Zeile.
4. Prüfen Sie, dass beide normalen Konten weiterhin nur das zuvor Sichtbare sehen. Eine leere Gruppe gibt keinen Zugriff.

### Benutzer hinzufügen und Zugriff prüfen {#add-the-user-and-check-access}

1. Wählen Sie unter **Groups** in **Add user** dieser Gruppe nur den Testbenutzer. Die Änderung wird sofort gesendet; es gibt keine gesonderte Speicherschaltfläche.
2. Klappen Sie die Anzahl **Users** mit dem Plussymbol auf und prüfen Sie den Anmeldenamen.
3. Prüfen Sie unter **Settings → Users**, dass diese Gruppe beim Benutzer erscheint und das Konto weiterhin **User** ist. Aktualisieren Sie nach Fehlern beide Ansichten: Die zwei Mitgliedschaftsdatensätze werden getrennt geschrieben; eine korrekt wirkende Liste reicht deshalb nicht.
4. Aktualisieren Sie die Mitgliedersitzung oder melden Sie sich erneut an. Prüfen Sie lesbare VM sowie nicht verfügbare oder ohne VM-Änderung verweigerte Start-, Stopp- und Administrationsaktionen.
5. Prüfen Sie, dass das zweite Konto weiterhin keinen VM-Zugriff hat.

Weichen Ergebnisse ab, halten Sie an. Prüfen Sie tatsächliche Identität, globale Berechtigung, Gruppen sowie sämtliche direkten und übergeordneten Regeln. Ergänzen Sie keine breiteren Freigaben, um den Test zu bestehen.

### Mitglied entfernen {#remove-the-member}

1. Klappen Sie unter **Groups** die Mitgliederliste auf und wählen Sie das Entfernen-Symbol neben dem genauen Test-Anmeldenamen. Das Entfernen wird sofort ohne Bestätigung gesendet.
2. Prüfen Sie, dass die Anmeldung die Gruppe und die Gruppe die Benutzerdetails verlassen hat.
3. Aktualisieren Sie die Sitzung des früheren Mitglieds oder melden Sie sich erneut an. Prüfen Sie den verlorenen VM-Zugriff aus der Gruppe.

Die Gruppenregel bleibt bestehen: Andere Mitglieder behalten ihren Zugriff.

### Additive Freigaben prüfen {#check-that-grants-add-up}

1. Fügen Sie den Benutzer wieder zur Gruppe hinzu und prüfen Sie zurückgekehrten Viewer-Zugriff.
2. Ergänzen Sie für diesen Benutzer eine eigene direkte **Viewer**-Regel auf derselben VM.
3. Entfernen Sie nur die Gruppenregel auf der VM. Der Benutzer kann die VM über die direkte Regel weiterhin lesen.
4. Entfernen Sie die direkte Regel und prüfen Sie erneut. Ohne andere Freigabe verschwindet der Zugriff, obwohl der Benutzer noch Mitglied ist.

Eine fehlende Gruppenregel verweigert nichts; ein globaler **Admin** umgeht sämtliche Objektregeln.

### Gruppentest aufräumen {#clean-up-the-group-test}

1. Entfernen Sie die Testregeln, solange ihre Benutzer und Gruppen noch existieren.
2. Entfernen Sie Testmitgliedschaften und prüfen Sie die Ergebnisse für beide normalen Konten.
3. Prüfen Sie Zeile und Namen der leeren Testgruppe. Wählen Sie dort **Delete group** und bestätigen Sie. Die Bestätigung nennt die Gruppe nicht; identifizieren Sie sie deshalb vor dem Öffnen.
4. Aktualisieren Sie die Ansichten Groups, ACLs und Users. Behalten Sie den unabhängigen Administrator.

XO entfernt Regeln und Mitgliedschaften gelöschter Gruppen im Hintergrund. Eine verschwundene Gruppe belegt keine vollständige Bereinigung aller zugehörigen Datensätze. Die ACL-Tabelle kann Zeilen ausblenden, deren Subjekt nicht mehr existiert. Ist eine Anfrage fehlgeschlagen oder widersprechen sich Datensätze, halten Sie an. Notieren Sie Identitäten und Fehler ohne Geheimnisse und [melden Sie die Inkonsistenz](/docs/xoa-hl/troubleshooting/), bevor Sie erneut versuchen oder weitere Objekte löschen.

Aus einem Authentifizierungsanbieter synchronisierte Gruppen, verschachtelte Gruppen, Umbenennen und umfassendere Delegation werden hier nicht behandelt. Lokale Namens- und Mitgliedersteuerung sind bei diesen Gruppen eingeschränkt. Verwenden Sie weder **Synchronize LDAP groups** noch das Trennen eines Authentifizierungsanbieters, um diese Grenzen zu umgehen.

## Kontingent einer delegierten Ressourcenmenge testen {#resource-set-delegation}

Eine Ressourcenmenge erlaubt einem normalen Benutzer, VMs aus gewählten Vorlagen, SRs und Netzwerken innerhalb von CPU-, RAM- und Datenträgergrenzen (Kontingenten) zu erstellen. Hier testen Sie eine Menge für einen Benutzer in einem entbehrlichen Pool.

**Vor dem Beginn**

- Verwenden Sie ausschließlich einen entbehrlichen Pool und einen eigenen normalen Testbenutzer ohne umfassende Regel auf diesem Pool.
- Behalten Sie eine unabhängige Administratorsitzung und eine unabhängige Sicherung aller aufzubewahrenden Daten.
- Fügen Sie keinen Produktionsbenutzer hinzu und teilen Sie weder Produktionsspeicher noch Produktionsnetze.
- Verwenden Sie zwei Browsersitzungen: XOA-HL-Administrator und getrennten normalen Benutzer.

### Ressourcenmenge erstellen {#create-the-resource-set}

1. Wählen Sie als Administrator einen entbehrlichen Pool, eine bekannte angehaltene Vorlage, ein beschreibbares Test-SR mit genug Platz und ein isoliertes Labornetz, das die geeigneten Hosts erreichen können.
2. Notieren Sie genaue UUIDs sowie CPU-, RAM- und Datenträgervorgaben der Vorlage. Können deren Datenträger oder Netzwerk nicht auf diesen Ressourcen liegen, halten Sie an.
3. Prüfen Sie **User** statt globalem **Admin** und dass der Testbenutzer in diesem Pool noch keine VM erstellen kann.
4. Öffnen Sie **Self service → Resource sets** (`/#/self`) und wählen Sie **New**. Vergeben Sie einen eindeutigen Labornamen. Wählen Sie nur diesen Benutzer und Pool sowie nur die vorgesehenen **Templates**, **SRs** und **Networks**.
5. Prüfen Sie die Hostliste. Der Editor zeigt anhand von SR- und Netzwerkzugriff geeignete und ausgeschlossene Hosts. Mindestens ein vorgesehener Host muss geeignet sein.
6. Setzen Sie endliche Werte für **Maximum CPUs**, **Maximum RAM** und **Maximum disk space**. Sie müssen eine kleine VM aus der Vorlage ermöglichen, aber unter der folgenden überhöhten Testanforderung bleiben.
7. Lassen Sie **Share VMs by default** aus, ergänzen Sie keinen IP-Pool und wählen Sie **Save**. Der Editor erstellt die Menge und bearbeitet sie anschließend: Aktualisieren Sie nach einem Speicherfehler die Liste und suchen Sie vor erneutem Versuch eine leere oder unvollständige Menge.
8. Laden Sie die Menge neu. Prüfen Sie ID, Benutzer, Vorlagen, SRs, Netzwerke, Hosts und alle drei Grenzen. Notieren Sie aktuelle Nutzung, normalerweise null.

Zeigt die Seite eine Upgradeaufforderung oder fehlt die Menge, notieren Sie die Version und halten Sie an. Nehmen Sie keinen erforderlichen Vates-Plan an und umgehen Sie die Oberfläche nicht durch einen ungeprüften API-Aufruf.

### Kontingent prüfen {#check-the-quota}

1. Öffnen Sie in der normalen Benutzersitzung **New VM** (`/#/vms/new`) und wählen Sie genau diese Ressourcenmenge.
2. Fordern Sie eine VM über der CPU-Grenze an. Lassen Sie Vorlage, SR, Netzwerk, RAM und Datenträger gültig. Der Server muss dies ohne neue VM oder unerwarteten Datenträger verweigern.
3. Prüfen Sie als Administrator Inventar und Kontingentnutzung. Ein verborgenes Bedienelement allein belegt keine Durchsetzung der Grenze. Existiert eine teilweise VM oder ein Datenträger, halten Sie an und erfassen Sie ihn vor jeder Bereinigung.
4. Fordern Sie als normaler Benutzer eine VM innerhalb jeder Grenze mit ausschließlich ausgewählten Objekten an. Lassen Sie sie angehalten. Entfernen oder trennen Sie geerbte VIFs vor einem isolierten Start.
5. Prüfen Sie UUID der neuen VM, Datenträger-SR, Netzwerk, Ressourcenmenge und die Kontingentwerte **Used** und **Total**.
6. Prüfen Sie, dass der normale Benutzer diese VM sehen und administrieren kann und ein anderes normales Konto ohne die Menge dies nicht kann.

Testen Sie die Grenze niemals an einer Produktions-VM. Standardmäßig gibt XO dem VM-Ersteller die Objektrolle **Admin** auf dieser VM. **Share VMs by default** erweitert dies auf die Benutzer der Menge. Der Testbenutzer benötigt keine Administratorregel auf dem gesamten Pool.

**Prüfung:** Die überhöhte Anforderung wurde ohne Überreste verweigert; die VM innerhalb der Grenzen erscheint in der Kontingentnutzung.

### Benutzer aus der Menge entfernen {#remove-the-user-from-the-set}

1. Entfernen Sie als Administrator den Testbenutzer aus der Menge. Aktualisieren Sie die normale Benutzersitzung.
2. Prüfen Sie, dass er die Menge nicht mehr wählen oder darüber weitere VMs erstellen kann.
3. Prüfen Sie verbleibende direkte oder geerbte Regeln auf der bestehenden VM gesondert. Das Entfernen aus einer Menge beseitigt deren VM-Regeln, aber andere Freigaben können Zugriff erhalten.

Stimmen Zugriff oder Nutzung nicht, halten Sie an und notieren Sie Mengen- und VM-IDs sowie Fehler ohne Geheimnisse. Verwenden Sie **Recompute all limits** nicht als unerklärte Reparatur.

### Ressourcenmengentest aufräumen {#clean-up-the-resource-set-test}

1. Stoppen Sie die neue VM und bestätigen Sie genaue VM- und VDI-IDs. Entfernen Sie ihre VIFs.
2. Löschen Sie **nur** diese entbehrliche VM. Prüfen Sie, dass ihre Datenträger und Snapshots wie vorgesehen behandelt wurden.
3. Aktualisieren Sie Kontingentnutzung und VM-Anzahl der Menge. Prüfen Sie, dass keine VM in der Menge bleibt.
4. Wählen Sie **Delete resource set** auf genau dieser Menge. Das Löschen einer Menge trennt ihre VMs nur ab; es löscht sie nicht.
5. Prüfen Sie normalen Benutzer, unabhängigen Administrator und Poolinventar erneut.

Notieren Sie erwartete und tatsächliche IDs, Verweigerungen, Kontingentwerte und Bereinigung ohne Zugangsdaten. Gruppensubjekte, IP-Pools, Standardfreigabe, mehrere VMs gleichzeitig, Bereinigung nach fehlgeschlagener Erstellung und Produktionsdelegation werden hier nicht behandelt.

## Externe LDAP-Anmeldung testen {#ldap-sign-in}

Eine LDAP-Anmeldung kann ein XO-Konto erstellen oder sich mit einem vorhandenen verbinden. Verwenden Sie ein entbehrliches Verzeichnis und eine eigene Testidentität ohne Administratorrechte.

{{< callout type="warning" >}}
Die Voreinstellungen lauten `createUserOnFirstSignin = true` und `mergeProvidersUsers = true`. Ein Verzeichnisbenutzername, der einem lokalen XO-Benutzernamen entspricht, kann sich deshalb mit diesem Konto verbinden und dessen lokales Passwort löschen. Verwenden Sie einen Testbenutzernamen, der **keinem** bestehenden XO-Konto entspricht.
{{< /callout >}}

**Vor dem Beginn**

- Behalten Sie eine unabhängige lokale Administratorsitzung und einen Wiederherstellungsweg.
- Notieren Sie als Administrator Image-, Paket- und XO-Versionen sowie wirksame Authentifizierungseinstellungen. Behalten Sie einen privaten [Konfigurationsexport](/docs/xoa-hl/configuration-backup/).
- Prüfen Sie unter **Settings → Plugins** (`/#/settings/plugins`), dass `auth-ldap` mit Version aufgeführt wird. Notieren Sie Konfiguration, Lade- und Autoload-Zustand ohne Geheimnisse. Fehlt es oder bedient es bereits reale Benutzer, halten Sie an.
- Bereiten Sie mit dem Verzeichnisverantwortlichen einen isolierten LDAPS- oder StartTLS-Endpunkt mit vertrauenswürdiger CA, eindeutigem stabilem Benutzer-ID-Attribut, enger Benutzerbasis und Filter sowie gegebenenfalls eigener Suchidentität vor.
- Ändern Sie weder den letzten lokalen Administrator noch einen bestehenden Anbieter, um diesen Test zu ermöglichen.

### Plugin konfigurieren und laden {#configure-and-load-the-plugin}

1. Tragen Sie im genehmigten Laborfenster nur die Werte des Verzeichnisverantwortlichen in das Pluginformular ein: URI, CA-Pfad, aktivierte Zertifikatsprüfung, StartTLS-Auswahl, Basis, Benutzerfilter, ID-Attribut und Suchzugangsdaten.
2. Lassen Sie **Synchronize groups** ungesetzt. Es kann Mitgliedschaften importieren und Zugriffsrechte ändern.
3. Prüfen Sie TLS-Identität und Erreichbarkeit gesondert. Deaktivieren Sie niemals Zertifikatsprüfungen, um einen Fehler zu verdecken.
4. Speichern Sie die Konfiguration. Laden Sie dann das Plugin und lesen Sie Lade- und Autoload-Zustand zurück. Das Laden auf dieser Seite aktiviert auch Autoload.

Speichern allein belegt keine funktionierende Anmeldung. Halten Sie Geheimnisse aus Bildschirmfotos, Protokollen und Issue-Berichten heraus.

### Einmal anmelden und Konto prüfen {#sign-in-once-and-check-the-account}

Verwenden Sie **Test** **nicht** als harmlose Verbindungsprüfung. Es führt den echten Anmeldepfad aus, der ein XO-Konto erstellen und bei entsprechender Konfiguration Gruppen synchronisieren kann.

1. Melden Sie sich in einer neuen getrennten Browsersitzung einmal mit der eindeutigen Verzeichnis-Testidentität an.
2. Prüfen Sie aus der Administratorsitzung neue XO-Benutzer-ID, Anbieter, globale Berechtigung (**User**), Gruppen und Sichtbarkeit. Eine erfolgreiche Anmeldung allein gewährt keinen Objektzugriff.
3. Geben Sie diesem Konto nur auf einer entbehrlichen VM **Viewer**, wie unter [Viewer auf einer VM vergeben](#grant-viewer). Prüfen Sie in seiner Sitzung lesbare VM und fehlende oder ohne Änderung verweigerte Bedien- und Administrationsaktionen.
4. Entfernen Sie genau diese Regel. Prüfen Sie in einer aktualisierten Sitzung den verlorenen Zugriff.
5. Probieren Sie ein falsches Verzeichnispasswort, ohne es offenzulegen. Prüfen Sie, dass der unabhängige lokale Administrator sich weiterhin anmelden kann.

Wird ein bestehendes XO-Konto verknüpft, erscheint eine unerwartete Administratorrolle oder Gruppe oder sind Anbieter- beziehungsweise Zertifikatsergebnis unklar: Halten Sie an, bewahren Sie bereinigte Nachweise auf und folgen Sie dem Wiederherstellungsplan des Verantwortlichen. Melden Sie sich nicht erneut an und vergeben Sie keine weiteren Rechte.

### LDAP-Test aufräumen {#clean-up-the-ldap-test}

1. Entfernen Sie nur Testregeln und Testmitgliedschaften. Melden Sie die externe Sitzung ab.
2. Entladen Sie `auth-ldap` und lesen Sie Lade- und Autoload-Zustand zurück. Der lokale Administrator muss weiterhin funktionieren.
3. Identifizieren Sie vor dem Löschen des Testkontos den genauen Benutzer, dessen Token und Regeln. Kontolöschung und Bereinigung der Pluginkonfiguration sind getrennte Aktionen. Bereinigen Sie niemals einen Anbieter, der andere Benutzer bedient.

Scheitert Laden, Anmeldung oder Entladen, sichern Sie bereinigte Fehler und tatsächliche Benutzer- und Anbieterzustände vor einem erneuten Versuch. Lockern Sie niemals TLS-Prüfungen und führen Sie keine Konten zusammen, um Fehler zu umgehen. Notieren Sie Anbieter, Version, TLS-Vertrauen, Identitätszuordnung, Benutzer- und Regel-IDs vorher und nachher, erlaubte und verweigerte Ergebnisse sowie erhaltene lokale Anmeldung. Gruppensynchronisation, Verzeichnisausfälle, Zugangsdatenrotation, Identitätsumbenennungen, Token, OTP und Failover werden hier nicht behandelt.

## Externe SAML-Anmeldung testen {#saml-sign-in}

Sie benötigen eine isolierte Anwendung bei einem Identitätsanbieter (IdP), eine eindeutig benannte Testidentität ohne Administratorrechte und einen unabhängigen lokalen XO-Administrator. Das Plugin entnimmt den XO-Benutzernamen dem in `usernameField` benannten Profilattribut.

{{< callout type="warning" >}}
Mit den Voreinstellungen `createUserOnFirstSignin` und `mergeProvidersUsers` kann ein mit einem vorhandenen XO-Konto übereinstimmender Benutzername dieses verknüpfen und sein lokales Passwort löschen. Testen Sie niemals mit einem bestehenden XO-Benutzernamen oder einer produktiven Single-Sign-On-Anwendung (SSO).
{{< /callout >}}

**Vor dem Beginn**

- Notieren Sie mit dem IdP-Verantwortlichen Image-, Paket-, XO- und Pluginversionen, wirksame Authentifizierungseinstellungen und öffentliche HTTPS-Adresse. Behalten Sie einen privaten [Konfigurationsexport](/docs/xoa-hl/configuration-backup/).
- Prüfen Sie `auth-saml` unter **Settings → Plugins** (`/#/settings/plugins`) und dass es keine realen Benutzer bedient.
- Vereinbaren Sie ein stabiles eindeutiges Profilattribut für `usernameField`. Prüfen Sie vor dem Laden dessen Testwert gegen **alle** XO-Benutzernamen.
- Behalten Sie eine funktionierende lokale Administratorsitzung und einen getrennten Konsolen-Wiederherstellungsweg.
- Sind öffentliche Adresse, Proxy oder Kontozuordnung unklar, halten Sie an.

### Appliance beim IdP registrieren {#register-the-appliance-with-the-idp}

1. Registrieren Sie beim IdP nur diesen Labor-Service-Provider. Seine Callback-URL muss `https://<appliance-name>/signin/saml/callback` entsprechen und von außen erreichbar sein. Prüfen Sie genauen DNS-Namen, Zertifikatsvertrauen und Weiterleitung durch etwaige Proxys.
2. Besorgen Sie **Signaturzertifikat**, Einstiegspunkt und vereinbarten Aussteller des IdP über den privaten Kanal des Verantwortlichen. Dieses Zertifikat ist nicht das HTTPS-Zertifikat der Appliance.
3. Verlangen Sie entsprechend der Vereinbarung mit dem IdP-Verantwortlichen eine signierte SAML-Antwort oder Assertion. Die Pluginvorgaben `wantAssertionsSigned` und `wantAuthnResponseSigned` sind beide `false`; das macht unsignierte Nachrichten jedoch **nicht** akzeptabel.

Prüfen Sie diese Optionen mit dem IdP-Verantwortlichen. Schwächen Sie niemals Signatur- oder TLS-Prüfungen ab, um Abweichungen zu verdecken.

### Konfigurieren, laden und anmelden {#configure-load-and-sign-in}

1. Tragen Sie nur Laborzertifikat, Einstiegspunkt, Aussteller und Benutzernamenfeld sowie vom Verantwortlichen genehmigte Callback- oder Strenge-Optionen ein.
2. Speichern Sie die Konfiguration. Laden Sie danach das Plugin und lesen Sie Lade- und Autoload-Zustand zurück. Speichern allein aktiviert es nicht; Laden auf dieser Seite aktiviert auch Autoload.
3. Starten Sie in einer neuen getrennten Browsersitzung die SAML-Anmeldung auf der XO-Anmeldeseite. Authentifizieren Sie sich einmal mit der zugewiesenen Laboridentität.
4. Lassen Sie den IdP-Verantwortlichen signierte Antwort und ausgewähltes Attribut bestätigen, ohne die Assertion zu veröffentlichen.

Fügen Sie niemals Zertifikate, Assertions, Profildaten oder Sitzungstoken in öffentliche Issues ein.

### Neues Konto prüfen {#check-the-new-account}

1. Prüfen Sie aus der Administratorsitzung die **neue** XO-Benutzer-ID, den Anbieter `saml`, globale Berechtigung (**User**), Gruppen und Sichtbarkeit.
2. Geben Sie dem Konto nur auf einer entbehrlichen VM **Viewer**, wie unter [Viewer auf einer VM vergeben](#grant-viewer). Prüfen Sie Lesezugriff und eine verweigerte Bedienaktion.
3. Entfernen Sie genau diese Regel. Prüfen Sie in einer aktualisierten Sitzung den verlorenen Zugriff.
4. Lassen Sie den IdP-Verantwortlichen eine nicht zugewiesene Labor-Kontrollidentität in einer neuen Sitzung verweigern. Dies testet eine neue Anmeldung, nicht den Widerruf bestehender XO-Token.
5. Prüfen Sie die weiterhin funktionierende lokale Administratoranmeldung.

Wird ein bestehender Benutzer verknüpft, erscheint eine privilegierte Rolle, fehlt das Attribut oder sind Signatur- oder Callback-Ergebnis unklar: Halten Sie an und behalten Sie ausschließlich bereinigte Nachweise. Fehlt das Benutzernamenfeld, protokolliert das Plugin das vollständige Profil; behandeln Sie Fehlerprotokolle deshalb als sensibel.

### SAML-Test aufräumen {#clean-up-the-saml-test}

1. Melden Sie die SAML-Testsitzung ab und entfernen Sie die Testregeln.
2. Entladen Sie nur das isolierte Plugin `auth-saml`. Prüfen Sie Lade- und Autoload-Zustand sowie lokale Anmeldung.
3. Listen Sie vor dem Löschen des Kontos den genauen Testbenutzer und seine Token auf. Abmelden oder Anbieter-Deaktivierung belegen keine Ungültigkeit bestehender XO-Token. Bereinigen Sie niemals einen Anbieter mit realen Benutzern.

Notieren Sie bei Fehlern vor einem erneuten Versuch bereinigten Callback und Fehler sowie tatsächliche Benutzer-, Anbieter- und Tokenzustände. Notieren Sie Callback-Adresse, IdP-Zertifikatsidentität und Ablaufdatum, Signaturrichtlinie, zugeordnetes Attribut, Pluginzustand, Benutzer- und Regel-IDs vorher und nachher, Ergebnisse und erhaltenen lokalen Zugriff ohne Geheimnisse. IdP-Ausfälle, Signaturschlüsselrotation, Uhrabweichung, Attributänderungen, Token- und Sitzungswiderruf, OTP und produktive Föderation werden hier nicht behandelt.

{{< details title="Quellen" closed="true" >}}
- **Benutzer, ACLs und Buildplan**: [Benutzeroberfläche](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [ACL-Oberfläche](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [Buildplan-Vorgabe](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [Rollen und Ausnahme für globale Administratoren](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [Vererbung von Objektrechten](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js), [xoa-hl-Buildskript](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Gruppen**: [Gruppenoberfläche](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/groups/index.js), [Gruppen-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/group.mjs), [Mitgliedschaft und Löschen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [Kombinierte Benutzer- und Gruppen-ACLs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [Subjektauswahl](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Ressourcenmengen**: [Ressourcenmengen-Editor und Planschranke](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/self/index.js), [Ressourcenmengen-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/resource-set.mjs), [Grenzen, Kontingentbuchführung und Löschen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/resource-sets.mjs), [VM-Erstellung und ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [Ressourcenmengenauswahl für neue VMs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **LDAP**: [Schema, TLS, Test, Registrierung und optionale Gruppensynchronisation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-ldap/src/index.js), [Pluginseite: Konfiguration, Laden und Test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [Benutzerregistrierung und Behandlung von Namenskollisionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [Authentifizierungsvorgaben](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [XOA-HL-Build-Workspaces](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [RPM-Inhalt](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **SAML**: [Pluginschema, Profilzuordnung und Registrierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-saml/src/index.js), [Web-Callback, Anmeldung und Tokenerstellung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [Plugin-Ladeseite](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [Verhalten bei Benutzerkollisionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [Upstream-SAML-Anleitung für XO 5](https://docs.xen-orchestra.com/users-and-access/users#saml).
{{< /details >}}
