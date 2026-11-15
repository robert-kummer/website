---
title: Vorbereitung: Ist dein Rechner bereit? – Robert Kummer IT
nav_title: Vorbereitung
description: Schritt für Schritt prüfen, ob dein Rechner für den Workshop „Produktiv in 12 Stunden“ bereit ist: Docker, Git und Claude Code auf Mac, Linux und Windows.
path: /vorbereitung/
llms_section: Seiten
priority: 0.6
---
# Ist dein Rechner bereit?

<p class="updated">Stand: <time datetime="2026-11">November 2026</time></p>

Im Workshop bauen wir auf deinem Rechner. Dafür braucht er drei Werkzeuge: **Docker**, **Git** und **Claude Code**. Mit dieser Anleitung prüfst du vorab selbst, ob alles läuft. So verlieren wir am Workshop-Tag keine Zeit mit der Einrichtung.

Rechne mit 30 bis 60 Minuten. Du brauchst keine Vorkenntnisse. Du tippst nur Befehle ab oder kopierst sie.

> **Wichtig:** Teste auf genau dem Rechner, mit genau dem Benutzerkonto und im selben Netz, die du am Workshop-Tag nutzt. Ein Firmennetz oder ein Proxy (ein Zwischenrechner, über den die Firma den Internetzugang leitet) kann Downloads blockieren. Das merkst du nur, wenn du dort testest.

## Accounts anlegen

Drei Accounts brauchst du für den Workshop. Alle laufen auf deinen Namen oder deine Firma, ich betreibe nichts für dich. Für jeden gibt es eine eigene Anleitung:

- [GitHub-Account anlegen]({{base}}anleitungen/github/): Hier liegt dein Quellcode, von hier wird ausgerollt.
- [Hetzner-Account anlegen]({{base}}anleitungen/hetzner/): Der Server für deine WebApp, in der <abbr title="Europäischen Union">EU</abbr>. Für eine Mac-App nicht nötig.
- [Claude-Konto anlegen]({{base}}anleitungen/claude/): Die KI, mit der wir bauen. Ein bezahlter Plan ist nötig.

Fang mit Hetzner an. Dort kann die Prüfung neuer Kunden etwas dauern.

Soll die App am Ende unter deiner eigenen Domain laufen, kläre außerdem, wer die Einstellungen der Domain (die <abbr title="Domain Name System">DNS</abbr>-Einträge) ändern kann. Das bist du selbst, deine IT oder deine Agentur.

## Was die Werkzeuge tun

- **Docker** startet Programme in abgeschotteten Kästen, sogenannten Containern. Deine App läuft so auf jedem Rechner gleich, und auf deinem System wird nichts verstellt.
- **Git** merkt sich jeden Stand deiner App. Du kannst jederzeit zurück, wenn etwas schiefgeht.
- **Claude Code** ist das KI-Werkzeug, mit dem wir die App bauen. Es läuft im Terminal.
- Das **Terminal** ist ein Fenster, in das du Befehle tippst. Nach jedem Befehl drückst du die Eingabetaste.

## Welches System hast du?

- [Mac](#mac)
- [Linux](#linux)
- [Windows](#windows) (der längste Teil, weil Windows ein Linux-Teilsystem braucht)

Danach machst du bei allen Systemen den [Härtetest](#der-haertetest) und gehst die [Checkliste](#checkliste-alles-gruen) durch.

## Mac

### 1. macOS-Version prüfen

Klicke oben links auf das Apple-Menü und dann auf **Über diesen Mac**. Dort steht die macOS-Version und der Chip: **Apple M1** oder neuer (Apple Silicon) oder **Intel**. Docker Desktop unterstützt die aktuelle und die zwei vorherigen macOS-Versionen. Ist dein Mac älter, schreib mir vorab.

Wenn wir im Workshop eine KI direkt auf deinem Mac laufen lassen wollen, brauchst du macOS 27.

### 2. Terminal öffnen

Drücke Cmd + Leertaste, tippe **Terminal** und drücke die Eingabetaste. Alle folgenden Befehle tippst du dort ein.

### 3. Docker installieren

Du hast zwei Möglichkeiten. Eine reicht.

- **Docker Desktop** (empfohlen): Lade es von [docker.com](https://docs.docker.com/desktop/setup/install/mac-install/) und wähle die Version für deinen Chip (Apple Silicon oder Intel). Öffne die App einmal und warte, bis sie „läuft“ meldet.
- **Kiri** (Alternative): [Kiri](https://runkiri.com/) ist kostenlos und versteht dieselben Docker-Befehle. Es läuft nur auf Apple Silicon ab macOS 14 und ist noch in der Beta-Phase, also eine Testversion.

Prüfe danach im Terminal:

```bash
docker --version
```

Erscheint eine Versionsnummer, ist Docker installiert.

### 4. Git prüfen

```bash
git --version
```

Erscheint eine Versionsnummer, ist alles gut. Fragt der Mac stattdessen, ob er die „Befehlszeilenentwickler­werkzeuge“ installieren soll, klicke auf **Installieren**. Alternativ startest du die Installation selbst:

```bash
xcode-select --install
```

### 5. Claude Code installieren

Das ist der offizielle Befehl aus der [Anleitung von Anthropic](https://code.claude.com/docs/en/setup):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Schließe danach das Terminal und öffne es neu. Weiter geht es mit dem [Härtetest](#der-haertetest).

## Linux

### 1. Docker Engine installieren

Unter Linux nutzt du die Docker Engine. Sie ist kostenlos. Folge der offiziellen Anleitung für deine Distribution (zum Beispiel Ubuntu, Debian oder Fedora): [Docker Engine installieren](https://docs.docker.com/engine/install/).

### 2. Docker ohne sudo nutzen

Damit du Docker ohne `sudo` (Befehl mit Administratorrechten) starten kannst, kommt dein Benutzer in die Gruppe `docker`. So steht es in der [offiziellen Anleitung](https://docs.docker.com/engine/install/linux-postinstall/):

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

Meldet der erste Befehl, dass es die Gruppe schon gibt, ist das in Ordnung. Melde dich danach ab und wieder an. Gut zu wissen: Wer in dieser Gruppe ist, hat auf dem Rechner faktisch Administratorrechte.

### 3. Git installieren

```bash
git --version
```

Fehlt Git, installierst du es unter Ubuntu und Debian so:

```bash
sudo apt update && sudo apt install -y git
```

Unter Fedora nimmst du `sudo dnf install git`.

### 4. Claude Code installieren

Der offizielle Befehl aus der [Anleitung von Anthropic](https://code.claude.com/docs/en/setup):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Schließe danach das Terminal und öffne es neu. Weiter geht es mit dem [Härtetest](#der-haertetest).

## Windows

Unter Windows arbeiten wir in **WSL2**. Das ist ein Linux, das Microsoft direkt in Windows mitliefert. Docker und Claude Code laufen darin wie auf einem Linux-Rechner. Die Einrichtung hat mehr Schritte, ist aber gut machbar.

Am Ende kannst du die Punkte 1 bis 3 auch mit dem [Prüfskript](#pruefskript-fuer-windows) auf einen Blick prüfen.

### 1. Windows-Version prüfen

Drücke die Windows-Taste, tippe `winver` und drücke die Eingabetaste. Ein Fenster zeigt Version und Build-Nummer.

- **Windows 11:** Version 23H2 (Build 22631) oder neuer.
- **Windows 10:** Version 22H2 (Build 19045).

Diese Werte verlangt Docker Desktop. Microsoft pflegt Windows 10 seit Oktober 2025 nur noch über ein Programm für erweiterte Sicherheitsupdates (ESU). Wenn du die Wahl hast, nimm einen Rechner mit Windows 11.

Docker nennt offiziell die Ausgaben Pro, Enterprise und Education. Hast du **Windows Home**, schreib mir vorab kurz, dann prüfen wir das zusammen.

### 2. Virtualisierung prüfen

WSL2 und Docker brauchen die Virtualisierung des Prozessors. Das ist eine Funktion, mit der ein Rechner einen zweiten, abgeschotteten Rechner simulieren kann.

Öffne den Task-Manager mit Strg + Umschalt + Esc. Klicke auf **Leistung** und dann auf **CPU**. Rechts unten muss stehen: **Virtualisierung: Aktiviert**.

Steht dort „Deaktiviert“, muss sie im BIOS oder UEFI eingeschaltet werden. Das sind die Grundeinstellungen des Rechners vor dem Windows-Start. Bei Firmenrechnern macht das meist die IT. Schreib mir in dem Fall, dann sage ich dir, was du deiner IT schreiben kannst.

### 3. Adminrechte prüfen

Für die Einrichtung brauchst du einmalig Administratorrechte. Drücke die Windows-Taste und tippe **PowerShell**. Klicke mit der rechten Maustaste auf **Windows PowerShell** und dann auf **Als Administrator ausführen**. Fragt Windows nach einem Admin-Passwort, das du nicht hast, muss deine IT die Schritte 4 und 6 übernehmen.

### 4. WSL2 mit Ubuntu installieren

Tippe in die PowerShell, die du als Administrator geöffnet hast:

```powershell
wsl --install
```

Das installiert WSL2 und Ubuntu, ein verbreitetes Linux. Starte den Rechner danach neu. Beim ersten Start von Ubuntu legst du einen Benutzernamen und ein Passwort an. Das Passwort ist nur für Ubuntu. Merke es dir gut, du brauchst es gleich wieder.

### 5. Prüfen, ob WSL Version 2 läuft

Öffne eine normale PowerShell (ohne Admin) und tippe:

```powershell
wsl -l -v
```

Die Ausgabe sieht ungefähr so aus. Wichtig ist die **2** in der Spalte VERSION:

```text
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

Steht dort eine 1, stellst du Ubuntu so um:

```powershell
wsl --set-version Ubuntu 2
```

### 6. Docker Desktop installieren

Lade Docker Desktop von der [offiziellen Seite](https://docs.docker.com/desktop/setup/install/windows-install/) und installiere es. Öffne Docker Desktop danach und prüfe zwei Einstellungen unter **Settings** (das Zahnrad oben rechts):

1. **General:** Ein Haken bei **Use WSL 2 based engine**.
2. **Resources** und dann **WSL Integration:** Der Schalter bei **Ubuntu** ist an.

Klicke danach auf **Apply**. Docker Desktop muss laufen, solange du mit Docker arbeitest.

Es gibt auch [Kiri](https://runkiri.com/) für Windows. Dort ist es aber noch eine frühe Testversion. Für den Workshop empfehle ich Docker Desktop.

### 7. Ubuntu öffnen

Ab hier arbeitest du **in Ubuntu**, nicht in der PowerShell. Drücke die Windows-Taste, tippe **Ubuntu** und drücke die Eingabetaste. Ein Terminal-Fenster öffnet sich. Prüfe dort, ob Docker erreichbar ist:

```bash
docker --version
```

### 8. Git in Ubuntu prüfen

```bash
git --version
```

Ubuntu bringt Git meist schon mit. Fehlt es, installierst du es so (Ubuntu fragt nach deinem Ubuntu-Passwort):

```bash
sudo apt update && sudo apt install -y git
```

### 9. Claude Code in Ubuntu installieren

Auch Claude Code installierst du in Ubuntu, nicht in Windows. Der offizielle Befehl aus der [Anleitung von Anthropic](https://code.claude.com/docs/en/setup):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Schließe danach das Ubuntu-Fenster und öffne es neu.

### 10. Projekte im Linux-Ordner anlegen

Deine Projekte gehören in deinen Linux-Ordner (`~`, gesprochen „Tilde“, dein persönlicher Ordner in Ubuntu). Nicht unter `/mnt/c`, denn das ist dein Windows-Laufwerk C:, und darauf ist Docker sehr langsam. Lege dir gleich einen Ordner an:

```bash
mkdir -p ~/projekte && cd ~/projekte
```

## Docker Desktop: kostenlos?

Docker Desktop auf Mac und Windows ist laut Docker kostenlos für private Nutzung und für Unternehmen mit **weniger als 250 Beschäftigten und weniger als 10 Mio. US-Dollar Jahresumsatz**. Beides muss zutreffen. Für die meisten Workshop-Kunden passt das. Verbindlich sind die [Bedingungen von Docker](https://www.docker.com/pricing/faq/). Kiri und die Docker Engine unter Linux sind kostenlos.

## Der Härtetest

Diesen Test machst du auf jedem System. Er zeigt, ob alles zusammenspielt: Docker kann aus dem Internet laden, Programme starten und sie im Browser zeigen.

Öffne das Terminal. Unter Windows ist das **Ubuntu**, nicht die PowerShell.

### 1. Einen Webserver starten

```bash
docker run --rm -p 8080:80 nginx
```

Beim ersten Mal lädt Docker den Webserver herunter. Das dauert einen Moment. Danach laufen Textzeilen durch und das Terminal bleibt stehen. Das ist richtig so.

Öffne jetzt im Browser die Adresse <http://localhost:8080>. Unter Windows nimmst du den ganz normalen Windows-Browser. Dort muss **Welcome to nginx!** stehen.

Hat es geklappt? Dann gehe zurück ins Terminal und beende den Webserver mit Strg + C.

### 2. Testprogramm von Docker

```bash
docker run --rm hello-world
```

Im Text muss **Hello from Docker!** stehen.

### 3. Claude Code prüfen

```bash
claude --version
```

Erscheint eine Versionsnummer, ist Claude Code installiert. Für die Anmeldung brauchst du ein bezahltes Claude-Konto, das kostenlose reicht nicht. Wie du es anlegst, steht in der [Anleitung zum Claude-Konto]({{base}}anleitungen/claude/). Welcher Plan für dich passt, klären wir im Kickoff.

Hast du das Konto schon, teste auch die Anmeldung. Starte Claude Code:

```bash
claude
```

Folge den Hinweisen zur Anmeldung im Browser. Öffnet sich kein Browser, kopiere den angezeigten Link in deinen Browser. Schreib danach zum Beispiel „Hallo“. Kommt eine Antwort, ist auch die Verbindung durch dein Netz in Ordnung. Mit `/exit` beendest du Claude Code.

## Prüfskript für Windows

Dieses kurze Skript ist freiwillig. Es zeigt Windows-Version, Arbeitsspeicher, Virtualisierung, Adminrechte, WSL und Docker auf einen Blick. Es liest nur und ändert nichts an deinem Rechner. Es lädt auch nichts aus dem Internet. Du siehst hier den vollständigen Code.

Öffne eine normale PowerShell (ohne Admin), kopiere den ganzen Block hinein und drücke die Eingabetaste:

```powershell
# Workshop-Check: liest nur, aendert nichts
$os  = Get-CimInstance Win32_OperatingSystem
$cs  = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$admin = [bool](whoami /groups | Select-String 'S-1-5-32-544')
"Windows:          $($os.Caption), Build $($os.BuildNumber)"
"Arbeitsspeicher:  $([math]::Round($cs.TotalPhysicalMemory / 1GB)) GB"
"Hypervisor aktiv: $($cs.HypervisorPresent)"
"Virtualisierung:  $($cpu.VirtualizationFirmwareEnabled)"
"Adminrechte:      $admin"
"--- WSL ---"
if (Get-Command wsl.exe -ErrorAction SilentlyContinue) { wsl.exe -l -v } else { "WSL nicht gefunden" }
"--- Docker ---"
if (Get-Command docker -ErrorAction SilentlyContinue) { docker version } else { "Docker nicht gefunden" }
```

So liest du das Ergebnis:

- **Windows:** Build 22631 oder höher (Windows 11) oder 19045 (Windows 10).
- **Arbeitsspeicher:** Docker Desktop verlangt mindestens 8 GB. Mit 16 GB arbeitet es sich deutlich angenehmer.
- **Hypervisor aktiv** oder **Virtualisierung:** Mindestens einer der beiden Werte muss `True` sein. Läuft WSL2 schon, zeigt Windows bei Virtualisierung oft `False` an. Das ist dann in Ordnung, solange Hypervisor aktiv `True` ist.
- **Adminrechte:** `True` heißt, dein Benutzer gehört zu den Administratoren.
- **WSL:** Ubuntu mit VERSION 2.
- **Docker:** Ein Abschnitt **Client** und ein Abschnitt **Server**. Fehlt Server oder steht dort ein Fehler, läuft Docker Desktop gerade nicht.

## Datenzugriff

Deine App arbeitet mit den Daten aus deinem Ablauf. Kläre vor dem Workshop, dass du an sie herankommst. Je nach Ablauf sind das zum Beispiel:

- **Exporte** aus deiner Software, etwa als CSV- oder Excel-Datei
- ein **Postfach**, aus dem die App E-Mails liest
- ein **API-Zugang**, also eine Schnittstelle, über die Programme Daten abrufen
- **Dateien** in einem Ordner oder Laufwerk

Oft braucht so ein Zugang ein paar Tage, weil ihn jemand freigeben muss. Kümmere dich deshalb früh darum. Echte Beispieldaten machen den Workshop viel ergiebiger.

## Checkliste: Alles grün?

Hake ab, was bei dir funktioniert. Die Haken werden nicht gespeichert.

- [ ] Meine Accounts bei GitHub, Hetzner (nur für eine WebApp) und Claude sind angelegt.
- [ ] Ich weiß, wer die DNS-Einträge meiner Domain ändern kann.
- [ ] Ich habe auf dem Rechner, mit dem Benutzerkonto und im Netz getestet, die ich am Workshop-Tag nutze.
- [ ] `docker --version` zeigt eine Versionsnummer.
- [ ] `git --version` zeigt eine Versionsnummer.
- [ ] `claude --version` zeigt eine Versionsnummer.
- [ ] Unter <http://localhost:8080> erscheint „Welcome to nginx!“.
- [ ] `docker run --rm hello-world` zeigt „Hello from Docker!“.
- [ ] Ich kann mich bei Claude Code anmelden, oder wir klären das Konto im Kickoff.
- [ ] Nur Windows: `wsl -l -v` zeigt Ubuntu mit VERSION 2, und meine Projekte liegen unter `~`.
- [ ] Ich komme an die Daten, die mein Ablauf braucht.

## Wenn etwas hängt

Kein Problem, dafür ist dieser Test da. Mach einen Screenshot von dem Schritt, bei dem es hakt, und schick ihn an [{{person.email}}](mailto:{{person.email}}). Schreib kurz dazu, welches System du nutzt. Das klären wir vor dem Workshop.

Am besten testest du direkt nach dem Kickoff. Dann bleibt genug Zeit, falls deine eigene IT etwas freigeben oder einstellen muss.

Noch kein Kickoff? [Hier geht es zum Angebot]({{base}}#kickoff).
