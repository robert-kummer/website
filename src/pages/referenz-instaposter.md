---
title: Referenz InstaPoster: Instagram-Beiträge aus Hochzeitsfotos – Robert Kummer IT
nav_title: Referenz InstaPoster
description: InstaPoster sortiert Hochzeitsfotos mit der KI von Apple offline auf dem Mac, füllt Canva-Vorlagen und plant die Beiträge in Postiz ein. Gebaut für die Hochzeitsfotografin Michelle Fiedler.
path: /referenzen/instaposter/
llms_section: Referenzen
priority: 0.6
image: assets/img/instaposter-kategorisieren.jpg
image_alt: InstaPoster: Hochzeitsfotos werden automatisch in Kategorien sortiert
---
# <span lang="en">InstaPoster</span>

<p class="updated">Für Michelle Fiedler, Hochzeitsfotografin · Mac-App · gebaut in 2 Tagen</p>

{{testimonial.instaposter.full}}

Michelle Fiedler fotografiert Hochzeiten ([weddingsandotherstories.com](https://www.weddingsandotherstories.com/)). Nach jeder Hochzeit macht sie aus den besten Fotos Karussell-Beiträge für Instagram. Das war Handarbeit, und es kostete sie nach jeder Hochzeit viele Stunden.

## Früher und heute

{{partials.instaposter_flow}}

Bisher bearbeitete sie die Fotos in Adobe Lightroom und bereitete danach jeden Beitrag von Hand vor: Bilder heraussuchen, Karussells zusammenstellen, Text schreiben und zum passenden Zeitpunkt auf Instagram posten.

Heute exportiert sie die Fotos aus Lightroom wie gewohnt. Den Rest übernimmt InstaPoster, sie prüft nur noch und gibt frei.

## Was InstaPoster macht

**Sortieren.** InstaPoster sortiert die Fotos in Kategorien wie Zeremonie, Details oder Party. Das erledigt die KI von Apple direkt auf dem Mac, auch offline: Für die Sortierung verlässt kein Foto den Rechner. Zu jedem Foto zeigt die App, wie sicher sie sich bei der Kategorie ist, und begründet die Wahl in einem Satz. Welche Kategorien es gibt und wie viele Fotos davon in welches Karussell kommen, legt Michelle selbst fest.

**Gestalten.** Damit füllt die App ihre Vorlagen in Canva, mit Platzhaltern für Hoch- und Querformat und für Text. Die Vorlagen sind so vielfältig wie ein Instagram-Karussell: mehrere Fotos in einer Komposition, ein Bild im Passepartout oder ein Foto mit den Namen des Paares und der Location. Auch die Textseite für den Beitrag liegt als Vorlage in Canva. So korrigiert Michelle den Beitragstext zusammen mit der Bildgeschichte und gibt beides gemeinsam frei. Das Design bleibt ihres, gearbeitet wird wie gewohnt in Canva.

**Planen.** Danach plant InstaPoster die fertigen Beiträge in Postiz ein, mit einem Vorschlag für den Beschreibungstext. Postiz veröffentlicht sie zum geplanten Termin auf Instagram. Aus 1.000 Fotos werden so 30 Beiträge, fertig geplant für die nächsten 30 Termine.

<figure class="shot"><button type="button" class="zoom" popovertarget="lb-kategorisieren"><img src="{{base}}assets/img/instaposter-kategorisieren.jpg" width="1616" height="815" loading="lazy" decoding="async" alt="InstaPoster, Ansicht Kategorisieren: Jedes Foto bekommt Kategorien mit Trefferquote, etwa Dekoration 95 %, Party 85 % oder Couple Shoot 95 %, dazu eine kurze Begründung."><span class="sr-only"> (vergrößern)</span></button><figcaption class="meta">Ansicht Kategorisieren. Fotos und Dateinamen sind unkenntlich gemacht. Zum Vergrößern anklicken.</figcaption></figure>
<div id="lb-kategorisieren" class="lightbox" popover><button type="button" class="lightbox-close" popovertarget="lb-kategorisieren" popovertargetaction="hide" aria-label="Großansicht schließen"><img src="{{base}}assets/img/instaposter-kategorisieren.jpg" width="1616" height="815" loading="lazy" decoding="async" alt=""></button></div>

## So kommt die Zeitersparnis zustande

Gemessen hat das niemand, die Zahlen sind Schätzungen:

- **Früher:** rund 20 Minuten je Beitrag für Auswahl, Zusammenstellen, Text und Posten. Bei 30 Beiträgen sind das rund 10 Stunden je Hochzeit.
- **Heute:** Das Sortieren läuft von allein. Prüfen und Freigeben in Canva dauert rund 3 Minuten je Beitrag, also rund 1,5 Stunden je Hochzeit. Das Posten entfällt, weil Postiz die Beiträge zum geplanten Termin veröffentlicht.

Das sind rund 8,5 Stunden weniger Arbeit nach jeder Hochzeit.

## Technik

- Mac-App, gebaut mit Swift und SwiftUI
- Sortierung und Textvorschläge mit Apple Foundation Models, auf dem Mac und ohne Internet
- Vorlagen über die Schnittstelle von Canva, Einplanen über die Schnittstelle von Postiz
- Der Quellcode gehört Michelle, die App läuft auf ihrem Mac

## Du hast auch so einen Ablauf?

Im Workshop „{{offer.name}}“ bauen wir zusammen eine App für deinen zeitraubendsten Ablauf. [Kickoff-Termin buchen]({{kickoff_href}}) oder [zurück zu den Referenzen]({{base}}#referenzen).
