/**
 * Hoja de control de autorizaciones de menores (carta, fondo blanco para ahorrar tinta).
 * La autorización firmada se archiva aparte; esta hoja solo dice qué reserva la tiene y
 * si se autorizó o no el uso promocional, que es lo que el equipo de edición necesita saber.
 *
 * Uso, desde la raíz del proyecto de la plataforma:  node /ruta/material-impreso-sofa/generar-registro-menores.mjs
 */
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(join(process.cwd(), "apps/web/package.json"));
const { chromium } = require("playwright");
const AQUI = dirname(fileURLToPath(import.meta.url));
const b64 = (f) => readFileSync(join(AQUI, f)).toString("base64");

const filas = Array.from({ length: 18 }, () => `<tr><td></td><td></td><td></td><td class="c">SÍ ☐ &nbsp; NO ☐</td><td class="c">☐</td><td></td></tr>`).join("");
const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{font-family:T;src:url(data:font/woff2;base64,${b64("fuentes/schibsted-grotesk.woff2")}) format("woff2");font-weight:400 900}
@font-face{font-family:X;src:url(data:font/woff2;base64,${b64("fuentes/instrument-sans.woff2")}) format("woff2");font-weight:400 700}
@page{size:279.4mm 215.9mm;margin:10mm}
body{font-family:X,sans-serif;color:#15151c;font-size:3.3mm}
header{display:flex;align-items:center;justify-content:space-between;border-bottom:.8mm solid #d9262e;padding-bottom:3mm}
h1{font-family:T;font-weight:900;font-size:6mm;margin:0;text-transform:uppercase}
.nota{color:#4b4f63;margin:2.5mm 0 3mm;line-height:1.45}
table{width:100%;border-collapse:collapse}
th{font-family:T;font-weight:700;font-size:2.9mm;text-transform:uppercase;letter-spacing:.06em;text-align:left;background:#f1f1f5;padding:2mm}
td{border-bottom:.25mm solid #c9cbd6;height:7.6mm;padding:0 2mm}
td.c,th.c{text-align:center;white-space:nowrap}
</style></head><body>
<header><h1>Control de autorizaciones · menores de edad · SOFA 2026</h1>
<img src="data:image/png;base64,${b64("arte/logo.png")}" style="height:11mm"></header>
<p class="nota">Antes de la sesión, el acudiente llena y firma la <b>Autorización para tratamiento de imagen y datos personales de menores de edad</b>. El formato firmado va a la carpeta de autorizaciones; aquí solo se anota el control.
Si el uso promocional dice <b>NO</b>: el material se entrega al cliente, pero <b>no</b> se publica en redes, portafolio ni publicidad de la marca.</p>
<table><tr><th style="width:15%">Fecha</th><th style="width:16%">Código de reserva</th><th>Personaje</th><th class="c" style="width:17%">Uso promocional</th><th class="c" style="width:11%">Firmada y archivada</th><th style="width:14%">Asesor</th></tr>${filas}</table>
</body></html>`;

const navegador = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }).catch(() => chromium.launch());
const pagina = await navegador.newPage();
await pagina.setContent(html, { waitUntil: "load" });
await pagina.evaluate(() => document.fonts.ready);
await pagina.pdf({ path: join(AQUI, "pdf", "control-autorizaciones-menores.pdf"), printBackground: true, preferCSSPageSize: true, pageRanges: "1" });
await navegador.close();
console.log("✓ pdf/control-autorizaciones-menores.pdf");
