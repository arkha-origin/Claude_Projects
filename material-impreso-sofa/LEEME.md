# Material impreso · SOFA 2026

## PDF listos para imprimir (`pdf/`)

| Pieza | Tamaño | Archivos |
|---|---|---|
| Paquetes (Esencia, Protagonista, Ícono) | Oficio 21,6 × 33 cm | `precios-paquetes-oficio-*.pdf` |
| Fotos y videos sueltos, efectos y extras | Carta | `precios-sueltos-carta-*.pdf` |
| Sesiones de grupo (tramos por persona) | Carta | `precios-grupos-carta-*.pdf` |
| Tarjeta de pago Nequi · Llave Bre-B | Media carta 14 × 21,6 cm | `tarjeta-pago-nequi-media-carta-*.pdf` |

Cada pieza viene en dos versiones:

- **`-imprenta.pdf`**: para la imprenta. Lleva 3 mm de sangrado por lado; la imprenta lo corta al tamaño final.
- **`-oficina.pdf`**: tamaño exacto, para imprimir en una impresora normal. Si el borde sale blanco, elige "sin márgenes" o "tamaño real".

Los `-vista.png` son vistas previas.

**Los QR** llevan a `https://cosplay-inc.com/sofa2026`, la tienda de SOFA. Pruébalos con el celular sobre la primera impresión.

**El QR de Nequi** tiene dos opciones:
- **Pegarlo a mano:** la tarjeta deja el recuadro blanco y ahí se pega el QR impreso.
- **Imprimirlo en la tarjeta:** guarda el QR que da la app de Nequi como `arte/qr-nequi.png` y vuelve a generar los PDF.

## Precios

Son los **precios de evento** que tiene hoy la plataforma: el catálogo que el despliegue vuelve a escribir en cada publicación.

Los **tramos de grupo** se pueden cambiar en Administración → Sesiones de grupo. Si allí no coinciden con el afiche, cambia `GRUPOS` en `generar.mjs` y vuelve a generar.

## Volver a generar

Desde la carpeta del proyecto de la plataforma (`cosplay_inc`):

```
node ../Claude_Projects/material-impreso-sofa/generar.mjs
```

## Prompts y arte con IA

- `prompts.md`: prompts para el resto del kit (muestrarios, señalética, stickers, merch).
- Las imágenes generadas con Higgsfield quedaron en la cuenta de Higgsfield, en el historial de generaciones de esta fecha. Las maquetas de merch que llevan el logo son referencia: al taller se le entrega el logo original, no la imagen generada.
- Fuentes: Schibsted Grotesk e Instrument Sans (licencia OFL), las mismas del sitio.
