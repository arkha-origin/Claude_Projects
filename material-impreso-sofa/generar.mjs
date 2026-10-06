/**
 * Genera los PDF imprimibles del stand (precios, grupos y tarjeta de pago).
 *
 * Uso, desde la raíz del proyecto de la plataforma (donde están playwright y qrcode):
 *   node /ruta/a/material-impreso-sofa/generar.mjs
 *
 * Sale cada pieza en dos versiones:
 *   - `-imprenta.pdf`: con 3 mm de sangrado por lado, para la imprenta.
 *   - `-oficina.pdf`: tamaño exacto, para imprimir en una impresora normal.
 *
 * Los precios son los de "evento" del catálogo de la plataforma (semilla
 * sofa-2026.ts), que el despliegue vuelve a escribir. Los tramos de grupo son los
 * iniciales: si se editaron en Administración → Sesiones de grupo, cambia GRUPOS.
 */
import { createRequire } from "node:module";
import { readFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(join(process.cwd(), "apps/web/package.json"));
const { chromium } = require("playwright");
const QRCode = require("qrcode");

const AQUI = dirname(fileURLToPath(import.meta.url));
const SALIDA = join(AQUI, "pdf");
mkdirSync(SALIDA, { recursive: true });

const URL_TIENDA = "https://cosplay-inc.com/sofa2026";
const NUMERO_PAGOS = "320 483 1701";

const datosUri = (archivo, tipo) =>
  `data:${tipo};base64,${readFileSync(join(AQUI, archivo)).toString("base64")}`;
const LOGO = datosUri("arte/logo.png", "image/png");
// Si se guarda el QR que da la app de Nequi como arte/qr-nequi.png, la tarjeta lo
// lleva impreso; si no, deja el recuadro para pegarlo a mano.
const QR_NEQUI = existsSync(join(AQUI, "arte/qr-nequi.png")) ? datosUri("arte/qr-nequi.png", "image/png") : null;
const F_TITULAR = datosUri("fuentes/schibsted-grotesk.woff2", "font/woff2");
const F_TEXTO = datosUri("fuentes/instrument-sans.woff2", "font/woff2");

/**
 * Texto con el degradado de la marca, letra por letra en color sólido. El
 * `background-clip: text` deja una raya fina en el PDF de Chromium; esto no.
 */
const degradado = (texto) => {
  const paradas = [[217, 38, 46], [184, 48, 111], [59, 91, 217]];
  const letras = [...texto];
  return letras
    .map((l, i) => {
      const t = letras.length > 1 ? i / (letras.length - 1) : 0;
      const tramo = t < 0.5 ? 0 : 1;
      const u = t < 0.5 ? t / 0.5 : (t - 0.5) / 0.5;
      const [a, b] = [paradas[tramo], paradas[tramo + 1]];
      const c = a.map((x, k) => Math.round(x + (b[k] - x) * u));
      return `<span style="color:rgb(${c.join(",")})">${l}</span>`;
    })
    .join("");
};

const pesos = (n) => "$" + n.toLocaleString("es-CO").replace(/,/g, ".");

// ── Catálogo (precios de evento, COP) ────────────────────────────────────────
const PAQUETES = [
  {
    nombre: "Esencia",
    resumen: "1 foto + 1 video",
    precio: 85_000,
    partes: 40_000 + 50_000,
    incluye: ["1 foto de estudio", "1 video Aura · ultra cámara lenta"],
  },
  {
    nombre: "Protagonista",
    resumen: "3 fotos + 2 videos",
    precio: 229_000,
    partes: 110_000 + 50_000 + 80_000,
    destacado: true,
    incluye: [
      "3 fotos de estudio",
      "1 video Aura · ultra cámara lenta",
      "1 video Órbita · 360° cámara lenta",
    ],
  },
  {
    nombre: "Ícono",
    resumen: "5 fotos + los 3 videos",
    precio: 389_000,
    partes: 180_000 + 50_000 + 80_000 + 100_000,
    incluye: [
      "5 fotos de estudio",
      "1 video Aura · ultra cámara lenta",
      "1 video Órbita · 360° cámara lenta",
      "1 Video Pasarela",
    ],
  },
];

const FOTOS = [
  { nombre: "Fotoestudio", nota: "Retrato en el estudio", p: [40_000, 110_000, 180_000] },
  { nombre: "Foto Pasarela", nota: "En la pasarela, con dos pasadas", p: [35_000, 95_000, 155_000] },
  { nombre: "Dúo", nota: "En pareja: la foto sale con los dos", p: [40_000, 110_000, 180_000] },
];
const VIDEOS = [
  { nombre: "Aura", nota: "Ultra cámara lenta, la cámara gira a tu alrededor", p: 50_000 },
  { nombre: "Órbita", nota: "360° en cámara lenta: cada detalle del traje y tus props", p: 80_000 },
  { nombre: "Video Pasarela", nota: "Tu paso completo: entrada, caminata y pose", p: 100_000 },
];
const EFECTOS = [
  { nombre: "Foto FX", nota: "Foto de estudio con efectos visuales, ya terminada", p: 60_000 },
  { nombre: "Foto Inmersiva", nota: "Fotomontaje completo a partir de tu sesión", p: 120_000 },
  { nombre: "Video FX", nota: "Tu paso por la pasarela con efectos visuales", p: 150_000 },
  { nombre: "Video IA Inmersivo", nota: "Tu paso por la pasarela recompuesto con IA", p: 200_000 },
];
const EXTRAS = [
  { nombre: "Vista Rápida", nota: "Tus capturas suben primero a tu galería", p: 20_000, sufijo: "" },
  { nombre: "Entrega Rápida", nota: "La edición final de esa foto, de primera en la cola", p: 40_000, sufijo: " c/u" },
];
const GRUPOS = [
  {
    nombre: "Grupal Foto",
    nota: "Una foto individual para cada integrante y una grupal para todos.",
    desde: 3,
    tramos: [
      ["3 a 9 personas", 35_000],
      ["10 a 19 personas", 33_000],
      ["20 o más", 32_000],
    ],
    color: "var(--rojo)",
  },
  {
    nombre: "Grupal Video",
    nota: "Video grupal de 30 a 45 segundos, con el momento de cada integrante.",
    desde: 5,
    tramos: [
      ["5 a 9 personas", 90_000],
      ["10 a 14 personas", 85_000],
      ["15 o más", 80_000],
    ],
    color: "var(--azul)",
  },
];

// ── Estilos compartidos ──────────────────────────────────────────────────────
const css = (anchoMm, altoMm, sangrado) => `
@font-face{font-family:Titular;src:url(${F_TITULAR}) format("woff2");font-weight:400 900}
@font-face{font-family:Texto;src:url(${F_TEXTO}) format("woff2");font-weight:400 700}
@page{size:${anchoMm + 2 * sangrado}mm ${altoMm + 2 * sangrado}mm;margin:0}
:root{--rojo:#e0353d;--rosa:#c23a7a;--azul:#4a6af0;--tinta:#f4f5fa;--tenue:#a9adbf;--fondo:#0d0f16;
  --degradado:linear-gradient(110deg,#d9262e,#b8306f 50%,#3b5bd9)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{overflow:hidden;width:${anchoMm + 2 * sangrado}mm;height:${altoMm + 2 * sangrado}mm}
body{font-family:Texto,sans-serif;color:var(--tinta);-webkit-print-color-adjust:exact;print-color-adjust:exact;
  background:
    radial-gradient(60% 40% at 0% 0%,rgba(217,38,46,.42),transparent 70%),
    radial-gradient(55% 40% at 100% 100%,rgba(59,91,217,.45),transparent 70%),
    radial-gradient(45% 30% at 85% 12%,rgba(184,48,111,.28),transparent 70%),
    var(--fondo);position:relative;overflow:hidden}
body::before{content:"";position:absolute;inset:0;opacity:.09;
  background-image:radial-gradient(circle,#fff 0.35mm,transparent 0.45mm);background-size:3.2mm 3.2mm;
  -webkit-mask-image:linear-gradient(180deg,#000,transparent 35%,transparent 70%,#000)}
.lienzo{position:absolute;inset:${sangrado + 9}mm;display:flex;flex-direction:column}
.logo{display:block;margin:0 auto;filter:invert(1) hue-rotate(180deg) drop-shadow(0 0 4mm rgba(217,38,46,.35))}
.antetitulo{font-family:Titular;font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:var(--tenue);text-align:center}
.titulo{font-family:Titular;font-weight:900;text-transform:uppercase;text-align:center;line-height:.95;letter-spacing:-.01em}
.titulo span{white-space:nowrap}
.cifra{font-family:Titular;font-weight:800;letter-spacing:-.01em}
.borde{position:relative;border-radius:5mm;border:.45mm solid transparent;
  background:linear-gradient(var(--relleno,#151824),var(--relleno,#151824)) padding-box,var(--degradado) border-box}
.pie{display:flex;align-items:center;gap:6mm;margin-top:auto}
.qr{background:#fff;border-radius:3mm;padding:2.2mm;flex:none}
.qr svg{display:block;width:100%;height:100%}
.pie h3{font-family:Titular;font-weight:800;text-transform:uppercase;letter-spacing:.02em}
.pie p{color:var(--tenue)}
.pie .url{font-family:Titular;font-weight:700;color:var(--tinta)}
.franja{height:1.2mm;border-radius:1mm;background:var(--degradado)}
`;

const qrSvg = (texto) =>
  QRCode.toString(texto, { type: "svg", margin: 0, errorCorrectionLevel: "M", color: { dark: "#0d0f16", light: "#ffffff" } });

const pieTienda = async (tamQr, extra = "") => `
<div class="pie">
  <div class="qr" style="width:${tamQr}mm;height:${tamQr}mm">${await qrSvg(URL_TIENDA)}</div>
  <div>
    <h3 style="font-size:6mm">Reserva y paga en línea</h3>
    <p style="font-size:3.6mm;margin-top:1mm">Escanea el código o entra a <span class="url">cosplay-inc.com/sofa2026</span></p>
    <p style="font-size:3mm;margin-top:2mm">Precios del evento en pesos colombianos.${extra}</p>
  </div>
</div>`;

// ── Piezas ───────────────────────────────────────────────────────────────────
async function paquetes() {
  const tarjetas = PAQUETES.map(
    (p) => `
    <div class="borde paquete${p.destacado ? " destacado" : ""}">
      ${p.destacado ? '<div class="cinta">Recomendado</div>' : ""}
      <div class="cabeza">
        <div>
          <div class="nombre">${p.nombre}</div>
          <div class="resumen">${p.resumen}</div>
        </div>
        <div class="precio cifra">${pesos(p.precio)}</div>
      </div>
      <div class="cuerpo">
        <ul>${p.incluye.map((i) => `<li>${i}</li>`).join("")}</ul>
        <div class="ahorro">Ahorras ${pesos(p.partes - p.precio)}</div>
      </div>
    </div>`,
  ).join("");
  return {
    nombre: "precios-paquetes-oficio",
    ancho: 216,
    alto: 330,
    cuerpo: `
<style>
.paquetes{display:flex;flex-direction:column;gap:7mm;margin:9mm 0 7mm}
.paquete{padding:6mm 8mm}
.paquete.destacado{border-width:.8mm;background:linear-gradient(135deg,#3a1520,#2c1630 45%,#1a2045) padding-box,var(--degradado) border-box;
  box-shadow:0 0 12mm rgba(184,48,111,.4)}
.cinta{position:absolute;top:-3.6mm;left:8mm;background:var(--degradado);color:#fff;font-family:Titular;font-weight:800;
  font-size:3.3mm;letter-spacing:.2em;text-transform:uppercase;padding:1.3mm 4mm;border-radius:10mm}
.cabeza{display:flex;justify-content:space-between;align-items:flex-end;gap:6mm;padding-bottom:4mm;border-bottom:.3mm solid rgba(255,255,255,.14)}
.nombre{font-family:Titular;font-weight:900;font-size:10.5mm;text-transform:uppercase;line-height:1}
.resumen{color:var(--tenue);font-size:4mm;margin-top:1.5mm;letter-spacing:.04em}
.precio{font-size:13mm;line-height:1}
.destacado .precio{color:#fff}
.cuerpo{display:flex;justify-content:space-between;align-items:flex-end;gap:6mm;margin-top:4mm}
.cuerpo ul{list-style:none;display:grid;gap:1.6mm;font-size:4.3mm}
.cuerpo li{padding-left:6mm;position:relative}
.cuerpo li::before{content:"";position:absolute;left:0;top:1.3mm;width:2.6mm;height:2.6mm;border-radius:50%;background:var(--degradado)}
.ahorro{flex:none;font-family:Titular;font-weight:700;font-size:3.6mm;color:#ffb3bb;border:.3mm solid rgba(255,179,187,.5);border-radius:10mm;padding:1.2mm 3.5mm}
</style>
<img class="logo" src="${LOGO}" style="width:96mm">
<div class="antetitulo" style="font-size:3.6mm;margin-top:5mm">SOFA 2026 · Foto y video para cosplayers</div>
<h1 class="titulo" style="font-size:17mm;margin-top:3mm">Elige tu <span>${degradado("paquete")}</span></h1>
<div class="paquetes">${tarjetas}</div>
<p style="text-align:center;color:var(--tenue);font-size:3.6mm;margin-bottom:5mm">Toda foto de estudio incluye la edición editorial. ¿Algo suelto? Pregunta por fotos y videos individuales.</p>
${await pieTienda(36)}`,
  };
}

async function sueltos() {
  const filaFoto = (f) => `
    <tr><td><b>${f.nombre}</b><small>${f.nota}</small></td>${f.p.map((x) => `<td class="cifra">${pesos(x)}</td>`).join("")}</tr>`;
  const fila = (x) => `
    <div class="fila"><div><b>${x.nombre}</b><small>${x.nota}</small></div><span class="punteado"></span><span class="cifra">${pesos(x.p)}${x.sufijo ?? ""}</span></div>`;
  return {
    nombre: "precios-sueltos-carta",
    ancho: 215.9,
    alto: 279.4,
    cuerpo: `
<style>
h2{font-family:Titular;font-weight:900;text-transform:uppercase;font-size:5.6mm;letter-spacing:.06em;display:flex;align-items:center;gap:3mm;margin-bottom:2mm}
h2::before{content:"";width:2.4mm;height:6mm;border-radius:1mm;background:var(--c)}
.bloque{padding:4mm 5.5mm;margin-bottom:4mm}
table{width:100%;border-collapse:collapse;font-size:3.8mm}
th{font-family:Titular;font-weight:700;color:var(--tenue);font-size:3.1mm;letter-spacing:.12em;text-transform:uppercase;text-align:right;padding-bottom:1.5mm}
td{padding:1.3mm 0;border-top:.25mm solid rgba(255,255,255,.1);vertical-align:middle}
td.cifra{text-align:right;font-size:4.6mm;width:24mm}
b{font-family:Titular;font-weight:800;font-size:4.3mm;display:block}
small{display:block;color:var(--tenue);font-size:3.1mm;margin-top:.4mm}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.fila{display:flex;align-items:flex-end;gap:2mm;padding:1.3mm 0;border-top:.25mm solid rgba(255,255,255,.1)}
.fila:first-of-type{border-top:0}
.fila>div{flex:0 1 auto;max-width:62%}
.punteado{flex:1;border-bottom:.4mm dotted rgba(255,255,255,.3);margin-bottom:1.6mm}
.fila .cifra{font-size:4.6mm;white-space:nowrap}
</style>
<img class="logo" src="${LOGO}" style="width:70mm">
<h1 class="titulo" style="font-size:10.5mm;margin:3mm 0 5mm">Fotos y videos <span>${degradado("sueltos")}</span></h1>
<div class="borde bloque" style="--c:var(--rojo)">
  <h2>Foto</h2>
  <table><tr><th></th><th>1 foto</th><th>3 fotos</th><th>5 fotos</th></tr>${FOTOS.map(filaFoto).join("")}</table>
</div>
<div class="dos">
  <div class="borde bloque" style="--c:var(--azul)"><h2>Video</h2>${VIDEOS.map(fila).join("")}</div>
  <div class="borde bloque" style="--c:var(--rosa)"><h2>Efectos</h2>${EFECTOS.map(fila).join("")}</div>
</div>
<div class="borde bloque" style="--c:#f0a23a"><h2>Extras</h2><div class="dos" style="gap:8mm">${EXTRAS.map(fila).join("")}</div></div>
${await pieTienda(26, " Los paquetes salen más baratos que las piezas sueltas.")}`,
  };
}

async function grupos() {
  const bloque = (g) => `
    <div class="borde grupo" style="--c:${g.color}">
      <div class="desde">Desde ${g.desde} personas</div>
      <h2>${g.nombre}</h2>
      <p class="nota">${g.nota}</p>
      <div class="tramos">
        ${g.tramos
          .map(
            ([q, p], i) => `
          <div class="tramo" style="--h:${14 + i * 5}mm">
            <span class="cifra">${pesos(p)}</span><small>por persona</small>
            <div class="barra"></div><div class="quien">${q}</div>
          </div>`,
          )
          .join("")}
      </div>
    </div>`;
  return {
    nombre: "precios-grupos-carta",
    ancho: 215.9,
    alto: 279.4,
    cuerpo: `
<style>
.grupos{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin:9mm 0}
.grupo{padding:7mm 6mm 6mm}
.desde{display:inline-block;font-family:Titular;font-weight:700;font-size:3.1mm;letter-spacing:.14em;text-transform:uppercase;
  background:var(--c);color:#fff;padding:1mm 3mm;border-radius:10mm}
h2{font-family:Titular;font-weight:900;text-transform:uppercase;font-size:8.5mm;line-height:1;margin-top:4mm}
.nota{color:var(--tenue);font-size:3.7mm;margin-top:2.5mm;min-height:15mm}
.tramos{display:flex;flex-direction:column;gap:3mm;margin-top:5mm}
.tramo{display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;column-gap:4mm;align-items:center;
  padding:3mm 4mm;border-radius:3mm;background:rgba(255,255,255,.05);border-left:1.4mm solid var(--c)}
.tramo .cifra{font-size:7mm}
.tramo small{color:var(--tenue);font-size:3mm;justify-self:end}
.tramo .barra{display:none}
.tramo .quien{grid-column:1/-1;font-family:Titular;font-weight:700;font-size:3.8mm;margin-top:.5mm}
</style>
<img class="logo" src="${LOGO}" style="width:86mm">
<div class="antetitulo" style="font-size:3.4mm;margin-top:5mm">Crews · amigos · familias</div>
<h1 class="titulo" style="font-size:14mm;margin-top:2mm">Sesiones de <span>${degradado("grupo")}</span></h1>
<div class="grupos">${GRUPOS.map(bloque).join("")}</div>
<p style="text-align:center;color:var(--tenue);font-size:3.7mm;margin-bottom:6mm">Todo el grupo paga el valor por persona de su tramo. Una sola persona puede pagar por todos:<br>al cobrar sale un enlace para que cada integrante se registre desde su celular.</p>
${await pieTienda(30)}`,
  };
}

async function tarjetaPago() {
  return {
    nombre: "tarjeta-pago-nequi-media-carta",
    ancho: 139.7,
    alto: 215.9,
    cuerpo: `
<style>
.portal{margin:6mm auto 0;width:78mm;height:78mm;border-radius:6mm;padding:1.2mm;background:var(--degradado);
  box-shadow:0 0 10mm rgba(217,38,46,.45),0 0 18mm rgba(59,91,217,.35)}
.portal div{width:100%;height:100%;border-radius:5mm;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;
  color:#9aa0b4;font-family:Titular;font-weight:700;font-size:3.6mm;text-align:center;line-height:1.4;
  border:.5mm dashed #c9cde0;background-clip:padding-box}
.numero{text-align:center;margin-top:6mm}
.numero small{display:block;color:var(--tenue);font-size:3.2mm;letter-spacing:.14em;text-transform:uppercase;font-family:Titular;font-weight:700}
.numero .cifra{font-size:10mm;display:block;margin-top:1mm}
.numero p{color:var(--tenue);font-size:3.4mm}
.pasos{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:6mm;text-align:center;font-size:3.2mm}
.pasos div{background:rgba(255,255,255,.06);border-radius:3mm;padding:2.6mm 1.5mm}
.pasos b{display:block;font-family:Titular;font-weight:900;font-size:6mm}
</style>
<img class="logo" src="${LOGO}" style="width:62mm">
<h1 class="titulo" style="font-size:12mm;margin-top:5mm">Paga <span>${degradado("aquí")}</span></h1>
<div class="antetitulo" style="font-size:3mm;margin-top:2mm">Nequi · Llave Bre-B</div>
<div class="portal">${
  QR_NEQUI
    ? `<div style="border:0;padding:5mm"><img src="${QR_NEQUI}" style="width:100%;height:100%;object-fit:contain"></div>`
    : '<div>Pega aquí el QR<br>de Nequi<br><span style="font-weight:400;font-size:3mm">(descárgalo de la app)</span></div>'
}</div>
<div class="numero"><small>O paga a este número</small><span class="cifra">${NUMERO_PAGOS}</span><p>Cosplay Inc</p></div>
<div class="pasos">
  <div><b>${degradado("1")}</b>Escanea o marca el número</div>
  <div><b style="color:#b8306f">2</b>Paga el valor exacto</div>
  <div><b style="color:#4a6af0">3</b>Muestra el comprobante</div>
</div>
<p style="text-align:center;color:var(--tenue);font-size:3mm;margin-top:auto">¿Otro medio de pago? Pregúntale al asesor.</p>`,
  };
}

// ── Render ───────────────────────────────────────────────────────────────────
const navegador = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }).catch(() => chromium.launch());
for (const pieza of [await paquetes(), await sueltos(), await grupos(), await tarjetaPago()]) {
  for (const [sufijo, sangrado] of [["imprenta", 3], ["oficina", 0]]) {
    const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><style>${css(pieza.ancho, pieza.alto, sangrado)}</style></head>
<body><div class="lienzo">${pieza.cuerpo}</div></body></html>`;
    const pagina = await navegador.newPage();
    await pagina.setContent(html, { waitUntil: "load" });
    await pagina.evaluate(() => document.fonts.ready);
    const ruta = join(SALIDA, `${pieza.nombre}-${sufijo}.pdf`);
    const desborde = await pagina.evaluate(() => {
      const l = document.querySelector(".lienzo");
      return l.scrollHeight - l.clientHeight;
    });
    if (desborde > 1) console.warn(`⚠ ${pieza.nombre}: el contenido se pasa ${desborde}px del área segura`);
    await pagina.pdf({ path: ruta, printBackground: true, preferCSSPageSize: true, pageRanges: "1" });
    if (sufijo === "oficina") {
      await pagina.setViewportSize({ width: Math.round(pieza.ancho * 3.78), height: Math.round(pieza.alto * 3.78) });
      await pagina.screenshot({ path: join(SALIDA, `${pieza.nombre}-vista.png`), fullPage: false });
    }
    await pagina.close();
    console.log("✓", ruta);
  }
}
await navegador.close();
