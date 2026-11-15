// Robert Kummer IT: Preisrechner und WebMCP-Werkzeuge.
// Kein innerHTML, keine Fremdskripte: die CSP erzwingt Trusted Types ohne Policy.

/** Wird beim Build durch die Daten aus src/data/site.json ersetzt. */
const SITE = __SITE_DATA__;

const euro = new Intl.NumberFormat('de-DE', { style: 'currency', currency: SITE.offer.currency, maximumFractionDigits: 0 });

// ---------------------------------------------------------------------------
// Preis
// ---------------------------------------------------------------------------

function calculatePrice({ days = SITE.offer.recommendedDays, timing = 'weekend', location = 'remote' } = {}) {
  const d = Number(days);
  if (!SITE.offer.days.includes(d)) throw new Error(`days muss ${SITE.offer.days.join(', ')} sein.`);
  if (!['weekend', 'weekday'].includes(timing)) throw new Error('timing muss weekend oder weekday sein.');
  if (!['remote', 'onsite'].includes(location)) throw new Error('location muss remote oder onsite sein.');

  const base = d * SITE.offer.pricePerDay;
  const surcharge = timing === 'weekday' ? d * SITE.offer.weekdaySurchargePerDay : 0;
  const parts = [`${d} × ${euro.format(SITE.offer.pricePerDay)}`];
  if (surcharge) parts[0] += ` + ${d} × ${euro.format(SITE.offer.weekdaySurchargePerDay)} Mo–Do`;
  parts.push(`${d * SITE.offer.hoursPerDay} Stunden`);
  parts.push(location === 'onsite' ? 'zzgl. Reisekosten' : 'remote');

  return {
    days: d,
    timing,
    location,
    hoursPerDay: SITE.offer.hoursPerDay,
    hours: d * SITE.offer.hoursPerDay,
    dayNote: SITE.offer.dayNote,
    currency: SITE.offer.currency,
    base,
    weekdaySurcharge: surcharge,
    total: base + surcharge,
    travelCosts: location === 'onsite' ? SITE.offer.onsite : SITE.offer.remote,
    vat: SITE.offer.vatNote,
    breakdown: parts.join(' · '),
  };
}

const DAY_HINTS = {
  1: '1 Tag: ein klar umrissener Ablauf, am Abend läuft er.',
  2: '2 Tage, empfohlen: Thema gelöst, und du baust danach selbst weiter.',
  3: '3 Tage: mehrere Abläufe oder mehr Zeit zum Selbermachen.',
};

const form = document.getElementById('price-form');
const calcMail = document.getElementById('calc-mail');

// E-Mail-Anfrage mit der Auswahl aus dem Rechner (Standardtext kommt aus build.py, gleicher Aufbau)
function workshopMail(price) {
  const days = price.days === 1 ? '1 Tag' : `${price.days} Tage`;
  const when = price.timing === 'weekday' ? 'Mo–Do' : 'Fr–So';
  const where = price.location === 'onsite' ? 'Vor Ort' : 'Remote';
  const lines = [
    'Hallo Robert,', '',
    `ich interessiere mich für den Workshop „${SITE.offer.name}“:`, '',
    `- Dauer: ${days} (${price.hours} Stunden)`,
    `- Wann: ${price.timing === 'weekday' ? 'Montag bis Donnerstag' : 'Freitag bis Sonntag'}`,
    `- Wo: ${price.location === 'onsite' ? 'Vor Ort (zzgl. Reisekosten)' : 'Remote'}`,
    `- Preis laut Rechner: ${euro.format(price.total)}`, '',
    'Um diesen Ablauf geht es:', '', '',
    'Passende Termine:', '', '',
  ];
  return `mailto:${SITE.contact.email}?subject=${encodeURIComponent(`Workshop-Anfrage: ${days}, ${when}, ${where}`)}&body=${encodeURIComponent(lines.join('\n'))}`;
}

function renderPrice() {
  const data = new FormData(form);
  const price = calculatePrice({ days: data.get('days'), timing: data.get('timing'), location: data.get('location') });
  document.getElementById('total').textContent = euro.format(price.total);
  document.getElementById('breakdown').textContent = price.breakdown;
  document.getElementById('dayHint').textContent = DAY_HINTS[price.days];
  if (calcMail) calcMail.href = workshopMail(price);
  return price;
}

if (form) {
  form.addEventListener('change', renderPrice);
  renderPrice();

  // Deklaratives WebMCP: Ein Agent füllt das Formular aus und sendet es ab.
  // Statt zu navigieren, antworten wir mit dem berechneten Preis.
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!event.agentInvoked || typeof event.respondWith !== 'function') return;
    event.respondWith(Promise.resolve().then(renderPrice));
  });
}

// ---------------------------------------------------------------------------
// Karussell: Scroll-Snap trägt, JS ergänzt Buttons, Status und inert
// ---------------------------------------------------------------------------

for (const carousel of document.querySelectorAll('.carousel')) {
  const track = carousel.querySelector('.carousel-track');
  const slides = [...track.children];
  const prev = carousel.querySelector('[data-carousel="prev"]');
  const next = carousel.querySelector('[data-carousel="next"]');
  const current = carousel.querySelector('[data-carousel="current"]');
  let index = 0;

  const update = (i) => {
    index = i;
    slides.forEach((slide, n) => { slide.inert = n !== i; });
    current.textContent = String(i + 1);
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
  };
  const go = (i) => {
    const target = slides[Math.max(0, Math.min(slides.length - 1, i))];
    track.scrollTo({ left: track.scrollLeft + target.getBoundingClientRect().left - track.getBoundingClientRect().left });
  };

  prev.addEventListener('click', () => go(index - 1));
  next.addEventListener('click', () => go(index + 1));
  track.addEventListener('keydown', (event) => {
    if (event.target !== track) return;
    if (event.key === 'ArrowLeft') { event.preventDefault(); go(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); go(index + 1); }
  });

  // Maus: Ziehen wie beim Wischen (nicht in der inneren Bildleiste). Touch scrollt nativ, Trackpad und Umschalt+Mausrad ebenfalls.
  let drag = null;
  track.addEventListener('pointerdown', (event) => {
    if (event.pointerType !== 'mouse' || event.button !== 0 || event.target.closest('a, button, input, select, textarea, .shots')) return;
    event.preventDefault();
    drag = { x: event.clientX, left: track.scrollLeft, start: index, moved: false, id: event.pointerId };
  });
  track.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    const dx = event.clientX - drag.x;
    if (!drag.moved) {
      if (Math.abs(dx) < 6) return;
      drag.moved = true;
      track.setPointerCapture(event.pointerId);
      track.classList.add('is-dragging');
    }
    track.scrollLeft = drag.left - dx;
  });
  const endDrag = (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    const { moved, x, start } = drag;
    drag = null;
    if (!moved) return;
    track.classList.remove('is-dragging');
    const dx = event.clientX - x;
    go(Math.abs(dx) > track.clientWidth * 0.15 ? start + (dx < 0 ? 1 : -1) : start);
  };
  track.addEventListener('pointerup', endDrag);
  track.addEventListener('pointercancel', endDrag);

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) update(slides.indexOf(entry.target));
    }
  }, { root: track, threshold: 0.6 });
  slides.forEach((slide) => observer.observe(slide));

  carousel.querySelector('.carousel-controls').hidden = false;
  carousel.classList.add('is-enhanced');
  update(0);
}

// ---------------------------------------------------------------------------
// Bildleiste je Referenz: Pfeile auf den Bildern, Klick aufs angeschnittene Nachbarbild fährt es herein
// ---------------------------------------------------------------------------

for (const gallery of document.querySelectorAll('.gallery')) {
  const strip = gallery.querySelector('.shots');
  const items = [...strip.children];
  if (items.length < 2) continue;
  const button = (dir, label, text) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = `gallery-nav gallery-${dir}`; b.setAttribute('aria-label', label); b.textContent = text;
    gallery.append(b); return b;
  };
  const prev = button('prev', 'Vorheriges Bild', '←');
  const next = button('next', 'Nächstes Bild', '→');
  let index = 0;

  const update = () => {
    const left = strip.getBoundingClientRect().left;
    index = items.reduce((best, item, n) =>
      Math.abs(item.getBoundingClientRect().left - left) < Math.abs(items[best].getBoundingClientRect().left - left) ? n : best, 0);
    prev.hidden = index === 0;
    next.hidden = index === items.length - 1;
  };
  const go = (i) => {
    const target = items[Math.max(0, Math.min(items.length - 1, i))];
    strip.scrollTo({ left: strip.scrollLeft + target.getBoundingClientRect().left - strip.getBoundingClientRect().left });
  };

  prev.addEventListener('click', () => go(index - 1));
  next.addEventListener('click', () => go(index + 1));
  // Klick auf das angeschnittene Nachbarbild fährt es herein, statt die Großansicht zu öffnen
  strip.addEventListener('click', (event) => {
    const item = event.target.closest('.shots > *');
    const n = items.indexOf(item);
    if (n < 0 || n === index) return;
    event.preventDefault();
    go(n);
  }, true);
  strip.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  update();
}

// ---------------------------------------------------------------------------
// Split-Button: Popover sitzt per Anchor Positioning am Pfeil, sonst per JS
// ---------------------------------------------------------------------------

if (!CSS.supports('position-area', 'bottom')) {
  for (const menu of document.querySelectorAll('.split-menu[popover]')) {
    const toggle = document.querySelector(`[popovertarget="${menu.id}"]`);
    const close = () => menu.hidePopover();
    menu.addEventListener('toggle', (event) => {
      if (event.newState !== 'open') { removeEventListener('scroll', close); return; }
      const r = toggle.getBoundingClientRect();
      menu.style.position = 'fixed';
      menu.style.top = `${r.bottom + 6}px`;
      menu.style.left = `${Math.max(8, r.right - menu.offsetWidth)}px`;
      menu.style.margin = '0';
      addEventListener('scroll', close, { once: true, passive: true });
    });
  }
}

// ---------------------------------------------------------------------------
// WebMCP (imperativ)
// ---------------------------------------------------------------------------

// Aktuelle Spezifikation: document.modelContext. Ältere Chrome-Builds und Polyfills: navigator.modelContext.
const modelContext = document.modelContext || navigator.modelContext;
const isLegacy = !document.modelContext && !!navigator.modelContext;

// Ältere Implementierungen erwarten ein MCP-Ergebnis, die aktuelle Spezifikation nimmt reine Daten.
function result(data, isError = false) {
  if (!isLegacy) {
    if (isError) throw new Error(String(data));
    return data;
  }
  const text = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
  return isError ? { content: [{ type: 'text', text }], isError: true } : { content: [{ type: 'text', text }] };
}

async function safely(fn) {
  let data;
  try {
    data = await fn();
  } catch (error) {
    return result(error instanceof Error ? error.message : String(error), true);
  }
  return result(data);
}

// Namen, Beschreibungen und Schemas kommen aus dem Build (gleiche Quelle wie /.well-known/webmcp).
const EXECUTORS = {
  get_contact: () => safely(() => SITE.contact),
  get_workshop_offer: () => safely(() => ({ ...SITE.offer, faq: SITE.faq, url: SITE.offerUrl })),
  calculate_workshop_price: (args = {}) => safely(() => calculatePrice(args)),
  get_page_markdown: ({ page } = {}) => safely(async () => {
    const entry = SITE.pages[page];
    if (!entry) throw new Error(`Unbekannte Seite. Erlaubt: ${Object.keys(SITE.pages).join(', ')}`);
    const response = await fetch(new URL(entry.markdown, new URL('../', import.meta.url)), { headers: { Accept: 'text/markdown' } });
    if (!response.ok) throw new Error(`Abruf fehlgeschlagen (${response.status}).`);
    return { page, url: entry.url, markdown: await response.text() };
  }),
};

const TOOLS = SITE.tools.map((tool) => ({ ...tool, annotations: { readOnlyHint: true }, execute: EXECUTORS[tool.name] }));

async function registerTools() {
  if (!modelContext || typeof modelContext.registerTool !== 'function') return;

  let existing = [];
  if (typeof modelContext.getTools === 'function') {
    try { existing = (await modelContext.getTools()) || []; } catch { existing = []; }
  }
  const taken = new Set(existing.map((tool) => tool && tool.name));
  const controller = new AbortController();

  for (const tool of TOOLS) {
    // Das deklarative Formular kann calculate_workshop_price schon bereitstellen.
    if (taken.has(tool.name)) continue;
    try {
      const registered = modelContext.registerTool(tool, { signal: controller.signal });
      if (registered && typeof registered.catch === 'function') registered.catch(() => {});
    } catch {
      // Werkzeug existiert bereits.
    }
  }

  addEventListener('pagehide', (event) => { if (!event.persisted) controller.abort(); });
}

registerTools();
