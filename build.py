#!/usr/bin/env python3
"""Baut die Website aus src/ nach dist/. Nur Python-Standardbibliothek.

    python3 build.py                          # Produktion (robert-kummer.de)
    python3 build.py --preview --base-path /website/
    python3 build.py --serve                  # bauen und lokal unter http://localhost:8000 zeigen
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][\w.]*)\s*\}\}")


class Raw(str):
    """Bereits fertiges HTML, wird beim Einsetzen nicht escaped."""


# ---------------------------------------------------------------------------
# Vorlagen
# ---------------------------------------------------------------------------

def lookup(ctx: dict, key: str):
    value = ctx
    for part in key.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            raise KeyError(key)
    return value


def render(template: str, ctx: dict, *, escape: bool, source: str) -> str:
    def replace(match: re.Match) -> str:
        key = match.group(1)
        try:
            value = lookup(ctx, key)
        except KeyError:
            sys.exit(f"{source}: unbekannter Platzhalter {{{{{key}}}}}")
        if isinstance(value, (dict, list)):
            sys.exit(f"{source}: {{{{{key}}}}} ist kein einzelner Wert")
        text = str(value)
        if escape and not isinstance(value, Raw):
            text = html.escape(text, quote=True)
        return text

    return PLACEHOLDER.sub(replace, template)


def front_matter(text: str, source: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        sys.exit(f"{source}: Front Matter nicht abgeschlossen")
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            sys.exit(f"{source}: ungültige Zeile im Front Matter: {line}")
        meta[key.strip()] = value.strip()
    return meta, text[end + 5:]


# ---------------------------------------------------------------------------
# Kleines Markdown: genau das, was die Seiten brauchen
# ---------------------------------------------------------------------------

INLINE_TAG = re.compile(r"</?(?:br|time|abbr|span|strong|em|code|a)\b[^<>]*>")


def slug(text: str) -> str:
    text = text.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def inline(text: str) -> str:
    stash: list[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{html.escape(m.group(1))}</code>"), text)
    text = re.sub(r"<(https?://[^>\s]+)>", lambda m: keep(f'<a href="{html.escape(m.group(1))}">{html.escape(m.group(1))}</a>'), text)
    text = INLINE_TAG.sub(lambda m: keep(m.group(0)), text)
    text = re.sub(r"&(?!#?\w+;)", "&amp;", text).replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def markdown_to_html(md: str) -> str:
    out: list[str] = []
    blocks = re.split(r"\n\s*\n", md.strip())
    for block in blocks:
        lines = block.splitlines()
        first = lines[0]
        heading = re.match(r"(#{1,4})\s+(.*)", first) if len(lines) == 1 else None
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            out.append(f'<h{level} id="{slug(title)}">{inline(title)}</h{level}>')
        elif re.match(r"<(?!https?://)[a-zA-Z/!]", first):
            out.append(block)
        elif all(re.match(r"\s*[-*]\s+", l) or l.startswith("  ") for l in lines):
            items = re.split(r"\n(?=\s*[-*]\s+)", block)
            out.append("<ul>\n" + "\n".join("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", i).strip()) + "</li>" for i in items) + "\n</ul>")
        elif re.match(r"\d+\.\s+", first):
            items = re.split(r"\n(?=\d+\.\s+)", block)
            out.append("<ol>\n" + "\n".join("<li>" + inline(re.sub(r"^\d+\.\s+", "", i).strip()) + "</li>" for i in items) + "\n</ol>")
        elif first.startswith(">"):
            text = " ".join(l.lstrip("> ").strip() for l in lines)
            out.append(f"<blockquote><p>{inline(text)}</p></blockquote>")
        elif first.startswith("|") and len(lines) > 2:
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
            head = "".join(f'<th scope="col">{inline(c)}</th>' for c in rows[0])
            body = "\n".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[2:])
            out.append(f"<table>\n<thead><tr>{head}</tr></thead>\n<tbody>\n{body}\n</tbody>\n</table>")
        else:
            out.append(f"<p>{inline(chr(10).join(lines))}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Hilfen
# ---------------------------------------------------------------------------

def sri(data: bytes) -> str:
    return "sha384-" + base64.b64encode(hashlib.sha384(data).digest()).decode()


def csp_hash(text: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'"


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip() + "\n"


def euro(value: int) -> str:
    return f"{value:,} €".replace(",", ".")


# ---------------------------------------------------------------------------
# WebMCP: eine Quelle für Skript und Manifest
# ---------------------------------------------------------------------------

def tool_definitions(data: dict, page_ids: list[str]) -> list[dict]:
    offer = data["offer"]
    return [
        {
            "name": "get_contact",
            "title": "Kontakt",
            "description": f"Kontaktdaten von {data['site']['name']}: Name, Firma, Rolle, E-Mail, Telefon, Postanschrift, Profile und vCard-URL.",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_workshop_offer",
            "title": "Workshop-Angebot",
            "description": f"Das Angebot „{offer['name']}“: Zielgruppe, Ablauf, Ergebnis, Preise, Voraussetzungen, was nicht dazugehört, und häufige Fragen.",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "calculate_workshop_price",
            "title": "Workshop-Preis berechnen",
            "description": "Berechnet den Preis für den Workshop nach Dauer, Zeitpunkt und Ort. Preise in Euro, keine Umsatzsteuer nach § 19 UStG.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "enum": offer["days"], "description": "Anzahl der Workshop-Tage"},
                    "timing": {"type": "string", "enum": ["weekend", "weekday"],
                               "description": f"weekend = Freitag bis Sonntag, weekday = Montag bis Donnerstag ({euro(offer['weekdaySurchargePerDay'])} Aufschlag pro Tag)"},
                    "location": {"type": "string", "enum": ["remote", "onsite"],
                                 "description": "remote = online ohne Aufpreis, onsite = vor Ort zuzüglich Reisekosten"},
                },
                "required": ["days"],
            },
        },
        {
            "name": "get_page_markdown",
            "title": "Seite als Markdown",
            "description": "Liefert eine Seite dieser Website als Markdown.",
            "inputSchema": {
                "type": "object",
                "properties": {"page": {"type": "string", "enum": page_ids, "description": "Seite: " + ", ".join(page_ids)}},
                "required": ["page"],
            },
        },
    ]


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(args: argparse.Namespace) -> Path:
    data = json.loads((SRC / "data" / "site.json").read_text(encoding="utf-8"))
    site, person, offer = data["site"], data["person"], data["offer"]
    # Seiten verlinken relativ (z. B. ../now/), damit kein Basispfad in den Links steht.
    # Nur die 404-Seite braucht absolute Pfade, weil sie unter beliebigen Adressen erscheint.
    base = "/" + args.base_path.strip("/") + "/" if args.base_path.strip("/") else "/"
    # Alle absoluten Adressen zeigen auf die Live-Domain, auch in Vorschau und lokal (canonical).
    site_url = site["url"].rstrip("/") + "/"
    site = {**site, "url": site_url}
    today = dt.date.today()
    out = ROOT / args.out

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Seiten einlesen ------------------------------------------------------
    pages: list[dict] = []
    md_templates: set[str] = set()
    for file in sorted((SRC / "pages").iterdir()):
        if file.suffix not in (".html", ".md"):
            continue
        meta, body = front_matter(file.read_text(encoding="utf-8"), file.name)
        if not meta:
            continue  # Markdown-Vorlage einer HTML-Seite, siehe "markdown:"
        if meta.get("markdown"):
            md_templates.add(meta["markdown"])
        page_id = "home" if file.stem == "index" else file.stem
        path = meta["path"]
        rel = path.lstrip("/")
        pages.append({
            "id": page_id, "file": file, "meta": meta, "body": body, "kind": file.suffix[1:],
            "path": path, "url": site_url + rel,
            "base": (("../" * rel.count("/")) or "./") if path != "/404.html" else base,
            "out": out / (rel + "index.html" if rel.endswith("/") or not rel else rel),
            "md_rel": (rel + "index.md") if (rel.endswith("/") or not rel) else None,
        })
    pages.sort(key=lambda p: -float(p["meta"].get("priority", "0.5")))
    listed = [p for p in pages if p["md_rel"]]
    page_ids = [p["id"] for p in listed]

    # Gemeinsamer Kontext ----------------------------------------------------
    kickoff_href = "mailto:" + person["email"] + "?subject=" + "Kickoff-Gespr%C3%A4ch"
    steps = offer["steps"]
    steps_html = Raw('<ol class="steps">\n' + "\n".join(
        "      <li" + (' class="is-current"' if s["when"] == "Tag 1" else "") + ">"
        f'<p class="meta">{i + 1:02d} · {html.escape(s["when"])}</p>'
        f'<h3>{html.escape(s["title"])}</h3><p>{html.escape(s["text"])}</p></li>'
        for i, s in enumerate(steps)) + "\n    </ol>")
    faq_html = Raw("\n".join(
        f'      <details class="faq" name="faq"{" open" if i == 0 else ""}>'
        f'<summary>{html.escape(f["q"])}</summary><p>{html.escape(f["a"])}</p></details>'
        for i, f in enumerate(data["faq"])))
    ctx = {
        "site": site, "person": person, "offer": offer, "base": base,
        "kickoff_href": kickoff_href,
        "steps_html": steps_html, "faq_html": faq_html,
        "steps_md": "\n".join(f"{i + 1}. **{s['when']}, {s['title']}:** {s['text']}" for i, s in enumerate(steps)),
        "deliverables_md": "\n".join(f"- {d}" for d in offer["deliverables"]),
        "faq_md": "\n\n".join(f"### {f['q']}\n\n{f['a']}" for f in data["faq"]),
    }

    # Assets ---------------------------------------------------------------
    shutil.copytree(SRC / "assets", out / "assets", ignore=shutil.ignore_patterns("site.css", "site.js", ".DS_Store"))

    contact = {
        "name": person["name"], "organization": person["organization"], "jobTitle": person["jobTitle"],
        "email": person["email"], "telephone": person["telephone"],
        "address": {"streetAddress": person["streetAddress"], "postalCode": person["postalCode"],
                    "locality": person["locality"], "country": person["country"]},
        "website": site_url, "vcard": site_url + person["vcard"],
        "profiles": {s["label"]: s["url"] for s in person["sameAs"]},
    }
    tools = tool_definitions(data, page_ids)
    site_data = {
        "contact": contact,
        "offer": {k: v for k, v in offer.items()},
        "offerUrl": site_url,
        "faq": data["faq"],
        "pages": {p["id"]: {"title": p["meta"]["title"], "url": p["url"], "markdown": p["md_rel"]} for p in listed},
        "tools": tools,
    }
    js = (SRC / "assets" / "site.js").read_text(encoding="utf-8")
    if "__SITE_DATA__" not in js:
        sys.exit("site.js: __SITE_DATA__ fehlt")
    js = js.replace("__SITE_DATA__", json.dumps(site_data, ensure_ascii=False).replace("</", "<\\/"))
    css = minify_css((SRC / "assets" / "site.css").read_text(encoding="utf-8"))
    assets = {}
    for name, content in (("site.css", css), ("site.js", js)):
        raw = content.encode()
        stem, ext = name.rsplit(".", 1)
        hashed = f"{stem}.{hashlib.sha256(raw).hexdigest()[:10]}.{ext}"
        write(out / "assets" / hashed, raw)
        assets[name] = ("assets/" + hashed, sri(raw))

    # Speculation Rules und CSP ----------------------------------------------
    speculation = json.dumps({"prerender": [{
        "where": {"and": [
            {"href_matches": "/*"},
            {"not": {"href_matches": ["/*.md", "/*.vcf", "/*.txt", "/*.xml", "/*.webmanifest"]}},
        ]},
        "eagerness": "moderate",
    }]}, separators=(",", ":"))
    csp_parts = [
        "default-src 'none'",
        f"script-src 'self' {csp_hash(speculation)}",
        "style-src 'self'",
        "img-src 'self'",
        "font-src 'self'",
        "connect-src 'self'",
        "manifest-src 'self'",
        "base-uri 'none'",
        "form-action 'self'",
        "upgrade-insecure-requests",
        "require-trusted-types-for 'script'",
        "trusted-types 'none'",
    ]
    csp_meta = "; ".join(csp_parts)
    csp_header = "; ".join(csp_parts + ["frame-ancestors 'none'"])

    # JSON-LD ----------------------------------------------------------------
    address = {"@type": "PostalAddress", "streetAddress": person["streetAddress"], "postalCode": person["postalCode"],
               "addressLocality": person["locality"], "addressCountry": person["countryCode"]}
    graph_base = [
        {"@type": "WebSite", "@id": site_url + "#website", "url": site_url, "name": site["name"],
         "inLanguage": site["lang"], "publisher": {"@id": site_url + "#org"}},
        {"@type": "Person", "@id": site_url + "#person", "name": person["name"], "givenName": person["givenName"],
         "familyName": person["familyName"], "jobTitle": person["jobTitle"], "email": "mailto:" + person["email"],
         "telephone": person["telephoneHref"], "address": address, "url": site_url,
         "image": site_url + person["photo"], "sameAs": [s["url"] for s in person["sameAs"]],
         "worksFor": {"@id": site_url + "#org"}},
        {"@type": "ProfessionalService", "@id": site_url + "#org", "name": site["name"], "url": site_url,
         "logo": site_url + "icon-512.png", "image": site_url + person["photo"], "email": "mailto:" + person["email"], "vatID": person["vatId"],
         "telephone": person["telephoneHref"], "address": address, "founder": {"@id": site_url + "#person"},
         "areaServed": {"@type": "Country", "name": person["country"]}},
    ]
    service = {
        "@type": "Service", "@id": site_url + "#workshop", "name": offer["name"], "description": offer["summary"],
        "serviceType": "Workshop", "provider": {"@id": site_url + "#org"}, "url": site_url,
        "audience": {"@type": "BusinessAudience", "audienceType": offer["audience"]},
        "areaServed": {"@type": "Country", "name": person["country"]},
        "offers": [
            {"@type": "Offer", "name": f"{offer['name']}, {offer['preferredTiming']}", "priceCurrency": offer["currency"],
             "priceSpecification": {"@type": "UnitPriceSpecification", "price": offer["pricePerDay"],
                                    "priceCurrency": offer["currency"], "unitCode": "DAY", "valueAddedTaxIncluded": False}},
            {"@type": "Offer", "name": f"{offer['name']}, Montag bis Donnerstag", "priceCurrency": offer["currency"],
             "priceSpecification": {"@type": "UnitPriceSpecification",
                                    "price": offer["pricePerDay"] + offer["weekdaySurchargePerDay"],
                                    "priceCurrency": offer["currency"], "unitCode": "DAY", "valueAddedTaxIncluded": False}},
        ],
    }
    faq_ld = {"@type": "FAQPage", "@id": site_url + "#fragen", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in data["faq"]]}

    # Gemeinsame Layout-Teile -------------------------------------------------
    rel_me_links = Raw("".join(f'<link rel="me" href="{html.escape(s["url"])}">\n' for s in person["sameAs"]))
    rel_me_list = Raw("\n        ".join(
        f'<li><a class="u-url" rel="me" href="{html.escape(s["url"])}">{html.escape(s["label"])}</a></li>' for s in person["sameAs"]))
    origin_trial = site.get("webmcpOriginTrial") or ""
    origin_trial_meta = Raw(f'<meta http-equiv="origin-trial" content="{html.escape(origin_trial)}">\n' if origin_trial else "")
    layout = (SRC / "layout.html").read_text(encoding="utf-8")

    markdown_docs: list[tuple[dict, str]] = []

    for page in pages:
        meta = page["meta"]
        name = page["file"].name
        # Inhalt
        if page["kind"] == "html":
            content = render(page["body"], {**ctx, "base": page["base"]}, escape=True, source=name)
            md_source = (SRC / "pages" / meta["markdown"]).read_text(encoding="utf-8") if meta.get("markdown") else None
        else:
            md_text = render(page["body"], {**ctx, "base": page["base"]}, escape=False, source=name)
            content = ('<section class="section">\n  <div class="wrap">\n    <article class="prose">\n'
                       + markdown_to_html(md_text) + "\n    </article>\n  </div>\n</section>")
            md_source = page["body"]
        if md_source is not None and page["md_rel"]:
            md_text = render(md_source, {**ctx, "base": site_url}, escape=False, source=meta.get("markdown", name)).strip()
            md_text = re.sub(r'<p class="updated">(.*?)</p>', lambda m: re.sub(r"<[^>]+>", "", m.group(1)), md_text)
            md_text += f"\n\n---\n\nQuelle: <{page['url']}>\n"
            write(out / page["md_rel"], md_text)
            markdown_docs.append((page, md_text))

        graph = list(graph_base) + [{
            "@type": "WebPage", "@id": page["url"] + "#webpage", "url": page["url"], "name": meta["title"],
            "description": meta.get("description", site["description"]), "inLanguage": site["lang"],
            "isPartOf": {"@id": site_url + "#website"},
            "about": {"@id": site_url + ("#workshop" if page["id"] == "home" else "#person")},
            "dateModified": today.isoformat(),
        }]
        if page["id"] == "home":
            graph += [service, faq_ld]
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
        jsonld = jsonld.replace("</", "<\\/")

        robots = "noindex, nofollow" if args.preview else meta.get("robots", "index, follow, max-image-preview:large")
        page_ctx = {
            **ctx,
            "csp_meta": csp_meta, "origin_trial_meta": origin_trial_meta,
            "title": meta["title"], "description": meta.get("description", site["description"]),
            "robots": robots, "canonical": page["url"],
            "md_href": page["base"] + (page["md_rel"] or "index.md"), "base": page["base"],
            "rel_me_links": rel_me_links, "rel_me_list": rel_me_list,
            "css_href": page["base"] + assets["site.css"][0], "css_sri": assets["site.css"][1],
            "js_href": page["base"] + assets["site.js"][0], "js_sri": assets["site.js"][1],
            "og_image": site_url + person["photo"],
            "jsonld": Raw(jsonld), "speculation_rules": Raw(speculation),
            "content": Raw("\x00CONTENT\x00"),
        }
        shell = render(layout, page_ctx, escape=True, source="layout.html")
        # aktuelle Seite in der Navigation markieren
        shell = shell.replace(f'href="{page["base"] + page["path"].lstrip("/")}"', f'href="{page["base"] + page["path"].lstrip("/")}" aria-current="page"')
        write(page["out"], shell.replace("\x00CONTENT\x00", content))

    # Statische Dateien ------------------------------------------------------
    static_ctx = {**ctx, "csp_header": csp_header, "today": today.isoformat()}
    for file in (SRC / "static").rglob("*"):
        if file.is_dir() or file.name == ".DS_Store":
            continue
        target = out / file.relative_to(SRC / "static")
        if args.preview and file.name == ".htaccess":
            continue  # GitHub Pages kennt kein Apache
        raw = file.read_bytes()
        if file.suffix in ("", ".txt", ".htaccess") or file.name == ".htaccess":
            text = raw.decode("utf-8")
            if "{{" in text:
                raw = render(text, static_ctx, escape=False, source=file.name).encode()
        write(target, raw)

    # Maschinenlesbares ------------------------------------------------------
    sections: dict[str, list[dict]] = {}
    for page in listed:
        sections.setdefault(page["meta"].get("llms_section", "Seiten"), []).append(page)
    llms = [f"# {site['name']}", "", f"> {offer['summary']}", "",
            f"{person['name']} ist {person['jobTitle']} in {person['locality']}. "
            f"Angebot: Workshop „{offer['name']}“, {euro(offer['pricePerDay'])} pro Tag "
            f"({offer['preferredTiming']}), unter der Woche {euro(offer['pricePerDay'] + offer['weekdaySurchargePerDay'])} pro Tag. "
            f"Kontakt: {person['email']}, {person['telephone']}.", ""]
    for title, items in sections.items():
        llms.append(f"## {title}")
        llms.append("")
        llms += [f"- [{p['meta'].get('nav_title', p['meta']['title'])}]({site_url}{p['md_rel']}): {p['meta'].get('description', '')}" for p in items]
        llms.append("")
    llms += ["## Optional", "",
             f"- [Alle Seiten in einer Datei]({site_url}llms-full.txt): vollständiger Inhalt als Markdown",
             f"- [Visitenkarte]({site_url}{person['vcard']}): vCard 3.0",
             f"- [WebMCP-Werkzeuge]({site_url}.well-known/webmcp): Werkzeuge, die die Seite Browser-Agenten anbietet",
             f"- [Sitemap]({site_url}sitemap.xml)", ""]
    write(out / "llms.txt", "\n".join(llms))
    write(out / "llms-full.txt", f"# {site['name']}\n\n> {offer['summary']}\n\n"
          + "\n\n".join(md for _, md in markdown_docs))

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        if page["meta"].get("sitemap") == "false":
            continue
        sitemap.append(f"  <url><loc>{html.escape(page['url'])}</loc><lastmod>{today.isoformat()}</lastmod>"
                       f"<priority>{page['meta'].get('priority', '0.5')}</priority></url>")
    sitemap.append("</urlset>\n")
    write(out / "sitemap.xml", "\n".join(sitemap))

    if args.preview:
        robots_txt = "# Vorschau: nicht indexieren\nUser-agent: *\nDisallow: /\n"
    else:
        robots_txt = f"User-agent: *\nAllow: /\n\nSitemap: {site_url}sitemap.xml\n"
    write(out / "robots.txt", robots_txt)

    write(out / ".well-known" / "security.txt",
          f"Contact: mailto:{person['email']}\n"
          f"Expires: {(today + dt.timedelta(days=365)).isoformat()}T00:00:00Z\n"
          f"Preferred-Languages: de, en\n"
          f"Canonical: {site_url}.well-known/security.txt\n")

    write(out / ".well-known" / "webmcp", json.dumps({
        "name": site["name"],
        "description": site["description"],
        "url": site_url,
        "page": site_url,
        "transport": "webmcp",
        "tools": tools,
    }, ensure_ascii=False, indent=2) + "\n")

    write(out / "manifest.webmanifest", json.dumps({
        "name": site["name"], "short_name": "Robert Kummer", "description": site["description"],
        "lang": site["lang"], "dir": "ltr", "start_url": "./", "scope": "./", "id": "./",
        "display": "minimal-ui", "background_color": site["themeColor"], "theme_color": site["themeColor"],
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }, ensure_ascii=False, indent=2) + "\n")

    print(f"Gebaut: {out.relative_to(ROOT)}/ · Basis {base} · {site_url}" + (" · Vorschau" if args.preview else ""))
    return out


def serve(directory: Path, port: int) -> None:
    import functools
    import http.server

    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                          ".md": "text/markdown; charset=utf-8", ".txt": "text/plain; charset=utf-8",
                          ".webmanifest": "application/manifest+json", ".vcf": "text/vcard",
                          ".avif": "image/avif", ".woff2": "font/woff2", "": "application/json"}

    handler = functools.partial(Handler, directory=str(directory))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Lokale Vorschau: http://localhost:{port}/  (Strg+C beendet)")
        httpd.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Baut die Website nach dist/.")
    parser.add_argument("--base-path", default="/", help="Pfad, unter dem die Seite liegt, z. B. /website/")
    parser.add_argument("--preview", action="store_true", help="Vorschau: noindex und robots.txt sperrt alles")
    parser.add_argument("--out", default="dist", help="Ausgabeordner")
    parser.add_argument("--serve", nargs="?", const=8000, type=int, metavar="PORT", help="nach dem Bauen lokal ausliefern")
    args = parser.parse_args()
    out = build(args)
    if args.serve:
        serve(out, args.serve)


if __name__ == "__main__":
    main()
