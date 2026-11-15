---
title: Referenz Fundus: Fotos und Dokumente in einer Bibliothek – Robert Kummer IT
nav_title: Referenz Fundus
description: Fundus bringt Google Fotos, Google Drive und Festplatten in einer Bibliothek auf dem eigenen Mac zusammen, private und gewerbliche Dokumente getrennt, automatisch einsortiert, mit Volltextsuche und geprüftem Backup.
path: /referenzen/fundus/
llms_section: Referenzen
priority: 0.6
image: assets/img/fundus-karte.jpg
image_alt: Fundus: Fotos und Dokumente auf einer Karte
---
# Fundus

<p class="updated">Für mich selbst, als Privatperson · Mac-App · erste Fassung im Workshop-Rahmen</p>

Meine Fotos lagen in Google Fotos, meine Dateien in Google Drive und auf mehreren Festplatten. Dazu kamen private und gewerbliche Dokumente, die ich getrennt halten will. Ich wollte alles an einem Ort haben, auf meinem eigenen Mac, ohne von einer Cloud abhängig zu sein.

Am meisten Zeit hat das Einsortieren gekostet. Die Fotos kamen von selbst in Google Fotos an, die Dokumente aber sammelten sich in Google Drive in einem Inbox-Ordner. Von dort habe ich jedes Dokument von Hand dorthin verschoben, wo es hingehört. Heute ziehe ich ein Dokument in Fundus, und es wird automatisch richtig archiviert. Das erledigen eine lokale KI und die Texterkennung von Apple auf dem Mac, zusammen mit den Metadaten der Datei.

Die erste Fassung von Fundus entstand im selben Rahmen wie ein Workshop. Seitdem baue ich sie Schritt für Schritt weiter, so wie du es nach dem Workshop mit deiner App tust.

## Was Fundus macht

**Alles kommt über die Inbox.** Dateien, Ordner oder Zips landen in der Inbox. Fundus erkennt den Export aus Google Fotos und übernimmt Aufnahmedatum, Ort, Beschreibung und Alben aus den Begleitdaten von Google. Downloads aus Google Drive werden entpackt und Datei für Datei einsortiert. Dasselbe Foto liegt danach nur einmal in der Bibliothek, auch wenn es in mehreren Alben war.

**Fotos und Videos.** Ein Raster nach Monaten, eine Zeitleiste, Alben und eine Diashow. Fotos mit GPS bekommen Land und Stadt als Schlagwort.

**Dokumente.** Fundus liest den Text aus PDFs und Office-Dateien. Gescannte Seiten gehen durch die Texterkennung auf dem Mac. Fundus erkennt die Art des Dokuments, etwa Rechnung, Vertrag oder Bescheid, dazu Datum, Absender und Beträge. Daraus vergibt Fundus die Schlagworte und archiviert das Dokument, ohne dass ich eingreifen muss.

**Privat und gewerblich getrennt.** Fundus kann mehrere Bibliotheken verwalten, zum Beispiel „Privat“ und „Gewerbe“, auch auf getrennten Laufwerken. Innerhalb einer Bibliothek ordnen Schlagworte mit Ebenen, etwa Gewerbe, Belege, 2026.

**Suchen und filtern.** Die Suche findet Namen, Schlagworte, Kommentare und den Text in den Dokumenten. Filter lassen sich als eigene Ansicht speichern, als Tabelle, Raster, Zeitleiste oder Karte.

**Backup.** Fundus spiegelt die Bibliothek auf ein zweites Laufwerk, auf Wunsch automatisch beim Anschließen und täglich. Jede Kopie wird geprüft. Was aus der Bibliothek entfernt wird, bleibt im Backup noch 30 Tage erhalten.

<figure class="shot"><button type="button" class="zoom" popovertarget="lb-fundus-zeit"><img src="{{base}}assets/img/fundus-zeitleiste.jpg" width="1523" height="812" loading="lazy" decoding="async" alt="Fundus, Ansicht Zeitleiste: oben eine Reihe „An diesem Tag“ mit Fotos von vor vier Jahren, darunter je Jahr eine Zeile mit einer Kachel pro Monat und der Zahl der Dateien, insgesamt 29.302 Dateien. Links die Seitenleiste mit Inbox, Karte, Filtern, Fotos, Dokumenten und Schlagworten."><span class="sr-only"> (vergrößern)</span></button><figcaption class="meta">Ansicht Zeitleiste. Die Fotos sind unkenntlich gemacht. Zum Vergrößern anklicken.</figcaption></figure>
<div id="lb-fundus-zeit" class="lightbox" popover><button type="button" class="lightbox-close" popovertarget="lb-fundus-zeit" popovertargetaction="hide" aria-label="Großansicht schließen"><img src="{{base}}assets/img/fundus-zeitleiste.jpg" width="1523" height="812" loading="lazy" decoding="async" alt=""></button></div>

<figure class="shot"><button type="button" class="zoom" popovertarget="lb-fundus-karte"><img src="{{base}}assets/img/fundus-karte.jpg" width="1523" height="812" loading="lazy" decoding="async" alt="Fundus, Ansicht Karte: Fotos mit GPS erscheinen als Stapel über Europa, etwa in Portugal, Spanien, Italien und Griechenland, jeder Stapel mit der Zahl seiner Fotos."><span class="sr-only"> (vergrößern)</span></button><figcaption class="meta">Ansicht Karte. Die Fotos sind unkenntlich gemacht. Zum Vergrößern anklicken.</figcaption></figure>
<div id="lb-fundus-karte" class="lightbox" popover><button type="button" class="lightbox-close" popovertarget="lb-fundus-karte" popovertargetaction="hide" aria-label="Großansicht schließen"><img src="{{base}}assets/img/fundus-karte.jpg" width="1523" height="812" loading="lazy" decoding="async" alt=""></button></div>

## Was mir wichtig war

- **Die Dateien überleben die App.** Alles liegt in normalen, lesbaren Ordnern. Die Metadaten stehen in einer Begleitdatei direkt neben jeder Datei. Ohne Fundus bleibt alles nutzbar.
- **Finder und Spotlight finden mit.** Auf Wunsch schreibt Fundus die Schlagworte als Finder-Tags.
- **Nichts geht verloren.** Jede Datei wird beim Verschieben geprüft, Gelöschtes landet erst im Papierkorb.
- **Große Mengen sind normal.** Ausgelegt auf 100.000 Dateien und mehr.

## Technik

- Mac-App, gebaut mit Swift und SwiftUI
- Datenbank und Volltextsuche mit SQLite
- Texterkennung und Dokumentauswertung auf dem Mac, mit den Frameworks von Apple
- Nur für Ortsnamen fragt Fundus bei Apple Maps nach

## Du hast auch so einen Ablauf?

Im Workshop „{{offer.name}}“ bauen wir zusammen eine App für deinen zeitraubendsten Ablauf. [Kickoff anfragen]({{kickoff_href}}) oder [zurück zu den Referenzen]({{base}}#referenzen).
