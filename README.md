# robert-kummer.de

Quellcode der Website von Robert Kummer IT.

## Aufbau

```
public/                        Alles, was auf den Server kommt (wird 1:1 hochgeladen)
public/assets/                 CSS, JavaScript, Schriften (Geist, selbst gehostet), Bilder
.github/workflows/preview.yml  Vorschau auf GitHub Pages bei jedem Push auf main
.github/workflows/deploy.yml   Deployment zu Mittwald bei jedem Release
```

Die Seite ist reines HTML/CSS/JS ohne Build-Schritt. Lokal reicht es, `public/index.html` im Browser zu öffnen.

## Vorschau

Jeder Push auf `main` aktualisiert die Vorschau unter **https://robert-kummer.github.io/website/**. Die Vorschau bekommt automatisch `noindex` und eine `robots.txt` mit `Disallow: /`, damit Suchmaschinen sie nicht indexieren. Alle Pfade in `public/` sind relativ, deshalb funktioniert die Seite im Unterordner genauso wie auf der Domain.

## Deployment

Gearbeitet wird nur auf `main`. Live geht die Seite erst mit einem **Release**:

1. Änderungen auf `main` pushen und in der Vorschau prüfen.
2. Auf GitHub einen Release anlegen (Releases → Draft a new release, Tag z. B. `v1.0.0`) und veröffentlichen.
3. GitHub Actions lädt den Inhalt von `public/` aus diesem Tag per SFTP zu Mittwald hoch.

Per Kommandozeile:

```bash
gh release create v1.0.0 --generate-notes
```

Ein Rollback ist ein erneutes Deployment eines älteren Tags: Den Workflow-Lauf des alten Releases unter Actions erneut starten („Re-run all jobs“).

> **Achtung:** Der Upload spiegelt `public/` auf den Zielordner (`mirror --delete`). Dateien im Zielordner, die nicht in `public/` liegen, werden gelöscht. `SFTP_PATH` muss deshalb auf den Ordner zeigen, der nur die Website enthält.

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
