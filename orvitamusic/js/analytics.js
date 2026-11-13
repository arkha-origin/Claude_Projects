/* =========================================================
   ORVITA MUSIC — Analítica (Google Analytics 4 y Pixel de Meta)
   ---------------------------------------------------------
   Los códigos se ponen en index.html, en window.ORVITA_ANALYTICS:
     gtm:       "GTM-XXXXXXX"    (Google Tag Manager: Analytics y demás etiquetas
                                  se configuran dentro del contenedor)
     ga4:       "G-XXXXXXXXXX"   (opcional: GA4 directo, sin Tag Manager)
     metaPixel: "123456789012345" (Meta Business → Administrador de eventos)
   Si un código está vacío, esa herramienta no se carga.

   Cada evento también se empuja al dataLayer ({ event: "generate_lead", … })
   para usarlo como activador en Tag Manager.

   Eventos que se envían:
   - Clic en cualquier botón de WhatsApp → GA4 «generate_lead» y Meta «Contact»
     (con el servicio: booking, audiovisual, sync…).
   - Clic en «Book Artist» o en la cotización de caché → además Meta «Lead».
   - Clic en el correo → GA4 «contact_email» y Meta «Contact».
   - Llegada a cada planeta del recorrido → GA4 «view_planet».
   ========================================================= */
(function () {
  const cfg = window.ORVITA_ANALYTICS || {};
  const gtm = /^GTM-[A-Z0-9]+$/.test(cfg.gtm || "") ? cfg.gtm : "";
  const ga4 = /^G-[A-Z0-9]+$/.test(cfg.ga4 || "") ? cfg.ga4 : "";
  const pixel = /^\d{8,20}$/.test(cfg.metaPixel || "") ? cfg.metaPixel : "";
  if (!gtm && !ga4 && !pixel) return;

  window.dataLayer = window.dataLayer || [];
  if (gtm) {
    /* Código oficial de Google Tag Manager. */
    window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
  }

  const load = (src) => { const s = document.createElement("script"); s.async = true; s.src = src; document.head.appendChild(s); };

  if (gtm) load(`https://www.googletagmanager.com/gtm.js?id=${gtm}`);

  if (ga4) {
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", ga4, { anonymize_ip: true });
    load(`https://www.googletagmanager.com/gtag/js?id=${ga4}`);
  }

  if (pixel) {
    /* Código base oficial del Pixel de Meta. */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", pixel);
    window.fbq("track", "PageView");
  }

  const gaEvent = (name, params) => {
    if (gtm) window.dataLayer.push({ event: name, ...params });
    if (ga4 && window.gtag) window.gtag("event", name, params);
  };
  const fbEvent = (name, params) => { if (pixel && window.fbq) window.fbq("track", name, params); };

  // Qué servicio pidió: el planeta donde está el botón, o el texto del enlace.
  const serviceOf = (a) => {
    const stop = a.closest(".stop");
    if (stop) return stop.id.replace(/^s-/, "");
    if (a.closest("#contacto")) return "contacto";
    if (a.closest(".nav")) return "book-artist";
    if (a.classList.contains("wa-float")) return "boton-flotante";
    return "general";
  };

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]");
    if (!a) return;
    const href = a.getAttribute("href");
    if (href.startsWith("https://wa.me/")) {
      const service = serviceOf(a);
      gaEvent("generate_lead", { method: "whatsapp", service });
      fbEvent("Contact", { content_name: service });
      if (service === "book-artist" || service === "booking" || /cach/i.test(decodeURIComponent(href))) {
        fbEvent("Lead", { content_name: "booking" });
      }
    } else if (href.startsWith("mailto:")) {
      gaEvent("contact_email", { service: serviceOf(a) });
      fbEvent("Contact", { content_name: "email" });
    }
  }, { capture: true });

  // Planetas vistos en el recorrido horizontal (una vez cada uno por visita).
  const bar = document.getElementById("orbitbar");
  if ((gtm || ga4) && bar) {
    const seen = new Set();
    new MutationObserver(() => {
      const cur = bar.querySelector("a.is-current");
      const id = cur && cur.getAttribute("href").slice(3);
      if (id && !seen.has(id)) { seen.add(id); gaEvent("view_planet", { planet: id }); }
    }).observe(bar, { subtree: true, attributes: true, attributeFilter: ["class"] });
  }
})();
