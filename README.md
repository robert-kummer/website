# robert-kummer.de

Quellcode der Website von Robert Kummer IT.

## Aufbau

```
src/layout.html                Rahmen jeder Seite: Kopf, Navigation, Fußzeile mit h-card
src/pages/                     Seiten: index.html (Startseite), now.md, uses.md, impressum.md, datenschutz.md, 404.html
src/pages/index.md             Markdown-Fassung der Startseite
src/data/site.json             Alle Fakten an einer Stelle: Kontakt, Angebot, Preise, FAQ
src/assets/                    CSS, JavaScript, Schriften (Geist, selbst gehostet), Bilder
src/static/                    Dateien für das Wurzelverzeichnis: Favicons, vCard, .htaccess
build.py                       Baut alles nach dist/ (nur Python-Standardbibliothek)
.github/workflows/preview.yml  Vorschau auf GitHub Pages bei jedem Push auf main
.github/workflows/deploy.yml   Deployment zu Mittwald bei jedem Release
```

Kontaktdaten, Preise und FAQ stehen nur in `src/data/site.json`. Seite, Markdown, JSON-LD, `llms.txt` und die WebMCP-Werkzeuge lesen alle daraus.

## Lokal bauen

Python 3.9 oder neuer, keine weiteren Abhängigkeiten.

```bash
python3 build.py              # baut nach dist/
python3 build.py --serve      # baut und zeigt die Seite unter http://localhost:8000
```

Neue Seite: eine Markdown-Datei mit Front Matter (`title`, `nav_title`, `description`, `path`, `llms_section`, `priority`) in `src/pages/` legen. Sie landet automatisch in Sitemap, `llms.txt`, `llms-full.txt` und im WebMCP-Werkzeug `get_page_markdown`.

## Was die Seite kann

- **Barrierefreiheit nach WCAG 2.2 AAA, soweit technisch prüfbar:** Kontrast mindestens 7:1, Klickflächen ab 44 px, sichtbarer Fokus, Skip-Link, Landmarks, `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, Abkürzungen mit Erklärung, englische Begriffe mit `lang="en"`.
- **Maschinenlesbar:** Microformats (`h-card` im Fuß jeder Seite, `h-product` für das Angebot), JSON-LD (Person, ProfessionalService, Service mit Preisen, FAQPage), vCard, `rel="me"`.
- **Für Sprachmodelle:** jede Seite auch als Markdown (`/index.md`, `/now/index.md` …, verlinkt per `<link rel="alternate" type="text/markdown">`), `Accept: text/markdown` liefert auf dem Server direkt Markdown, dazu `/llms.txt` und `/llms-full.txt`.
- **WebMCP:** Die Seite bietet Browser-Agenten die Werkzeuge `get_contact`, `get_workshop_offer`, `calculate_workshop_price` und `get_page_markdown` an, imperativ über `document.modelContext` und deklarativ über das Preisformular. Übersicht unter `/.well-known/webmcp`.
- **Sicherheit:** strenge Content Security Policy ohne Inline-Skripte, Trusted Types, Subresource Integrity, HSTS, COOP/COEP/CORP, Permissions-Policy, `/.well-known/security.txt`. Keine Cookies, kein Tracking, keine Anfragen an Dritte.
- **Tempo:** Lighthouse 100 als Ziel, Schriften lokal mit `font-display: swap` und angepasster Ersatzschrift, Bilder als AVIF mit `srcset` und Lazy Loading, CSS und JS mit Hash im Dateinamen und ein Jahr Cache, Speculation Rules für sofortige Seitenwechsel, View Transitions.

### WebMCP aktivieren

WebMCP läuft in Chrome derzeit hinter einem Flag oder über einen Origin Trial. Für den Trial unter https://developer.chrome.com/origintrials ein Token für `https://robert-kummer.de` holen und in `src/data/site.json` bei `site.webmcpOriginTrial` eintragen. Der Build setzt dann das passende `<meta http-equiv="origin-trial">`.

## Vorschau

Jeder Push auf `main` aktualisiert die Vorschau unter **https://robert-kummer.github.io/website/**. Der Workflow baut mit `--preview`: alle Seiten bekommen `noindex`, die `robots.txt` sperrt alles, die `.htaccess` entfällt.

Alle Links zwischen den Seiten sind relativ (`../now/`, `index.md`). Deshalb funktioniert dieselbe Ausgabe unter `/website/`, lokal und live, ohne dass ein Basispfad in den Links steht. Nur die 404-Seite verlinkt absolut, weil sie unter beliebigen Adressen erscheint. Absolute Adressen (canonical, JSON-LD, Markdown, `llms.txt`, Sitemap) zeigen immer auf https://robert-kummer.de/.

## Deployment

Gearbeitet wird nur auf `main`. Live geht die Seite erst mit einem **Release**:

1. Änderungen auf `main` pushen und in der Vorschau prüfen.
2. Auf GitHub einen Release anlegen (Releases → Draft a new release, Tag z. B. `v1.0.0`) und veröffentlichen.
3. GitHub Actions baut die Seite aus diesem Tag und lädt `dist/` per SFTP zu Mittwald hoch.

Per Kommandozeile:

```bash
gh release create v1.0.0 --generate-notes
```

Ein Rollback ist ein erneutes Deployment eines älteren Tags: Den Workflow-Lauf des alten Releases unter Actions erneut starten („Re-run all jobs“).

> **Achtung:** Der Upload spiegelt `dist/` auf den Zielordner (`mirror --delete`). Dateien im Zielordner, die nicht in `dist/` liegen, werden gelöscht. `SFTP_PATH` muss deshalb auf den Ordner zeigen, der nur die Website enthält.

## Einstellungen auf GitHub

Unter **Settings → Secrets and variables → Actions** (oder am Environment `production`):

| Name | Art | Inhalt |
|---|---|---|
| `SFTP_HOST` | Variable | SSH/SFTP-Host aus dem Mittwald mStudio |
| `SFTP_PORT` | Variable | optional, Standard `22` |
| `SFTP_USER` | Variable | SFTP-/SSH-Benutzer aus dem mStudio |
| `SFTP_PATH` | Variable | Zielordner auf dem Server, z. B. `/html/robert-kummer.de` |
| `SFTP_KNOWN_HOSTS` | Variable | Host-Key des Servers, siehe unten |
| `SFTP_PRIVATE_KEY` | Secret | privater SSH-Schlüssel (empfohlen) |
| `SFTP_PASSWORD` | Secret | Passwort, nur falls kein Schlüssel genutzt wird |

Es reicht entweder `SFTP_PRIVATE_KEY` oder `SFTP_PASSWORD`. Ist beides gesetzt, wird der Schlüssel genommen.

**Host-Key ermitteln** (einmalig, Fingerprint mit den Angaben im mStudio abgleichen):

```bash
ssh-keyscan -p 22 <SFTP_HOST>
```

Die komplette Ausgabe als `SFTP_KNOWN_HOSTS` eintragen. Ohne passenden Host-Key bricht das Deployment ab, damit nicht versehentlich an einen fremden Server übertragen wird.

**Deploy-Schlüssel erzeugen** (ohne Passphrase, nur für GitHub Actions):

```bash
ssh-keygen -t ed25519 -N "" -C "github-actions website" -f mittwald-deploy
```

`mittwald-deploy.pub` im mStudio beim SFTP-/SSH-Benutzer hinterlegen, den Inhalt von `mittwald-deploy` als Secret `SFTP_PRIVATE_KEY` eintragen und die beiden Dateien danach lokal löschen.
