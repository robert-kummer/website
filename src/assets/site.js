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
  if (surcharge) parts.push(`+ ${d} × ${euro.format(SITE.offer.weekdaySurchargePerDay)} Mo–Do`);
  parts.push(location === 'onsite' ? 'zzgl. Reisekosten' : 'remote');

  return {
    days: d,
    timing,
    location,
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

function renderPrice() {
  const data = new FormData(form);
  const price = calculatePrice({ days: data.get('days'), timing: data.get('timing'), location: data.get('location') });
  document.getElementById('total').textContent = euro.format(price.total);
  document.getElementById('breakdown').textContent = price.breakdown;
  document.getElementById('dayHint').textContent = DAY_HINTS[price.days];
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
    const response = await fetch(new URL(entry.markdown, location.href), { headers: { Accept: 'text/markdown' } });
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
