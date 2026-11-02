# Orvita Music — arkhaorigin.com/orvitamusic

Sitio web de **Orvita Music**, un sello de Arkha Origin: representación artística, marketing musical, grabación, producción, mezcla, asesoramiento artístico y music business.

Sitio **estático** (HTML + CSS + JS), sin build. Escena 3D con Three.js (r169, incluido en `js/vendor/`, licencia MIT).

## Estructura

```
orvitamusic/
├── index.html          # Página única (hero 3D, servicios, proceso, estudio, contacto)
├── css/styles.css      # Sistema visual y animaciones
├── js/main.js          # Escena 3D + interacciones (tilt, cursor, reveal, contadores)
├── js/vendor/          # three.module.min.js + licencia
├── assets/             # logo.svg, logo-mark.svg, favicon.svg
└── BRAND.md            # Guía de identidad de marca
```

## Ver en local

```bash
cd orvitamusic
python3 -m http.server 8000
# abrir http://localhost:8000
```
(Se necesita un servidor: los módulos JS no cargan con `file://`.)

## Publicar en arkhaorigin.com/orvitamusic

Todas las rutas son relativas, así que basta con subir la carpeta a `/orvitamusic/` del dominio:

- **Hosting tradicional / cPanel:** subir el contenido a `public_html/orvitamusic/`.
- **Netlify / Vercel:** desplegar este repo y, en el sitio principal de Arkha, añadir un rewrite de `/orvitamusic/*` hacia este despliegue.
- **GitHub Pages:** si el repo se llama `orvitamusic` y el dominio `arkhaorigin.com` ya está en Pages, quedará en `arkhaorigin.com/orvitamusic/` automáticamente.

## Pendientes antes de publicar

- [ ] Cambiar `CONTACT_EMAIL` en `js/main.js` (hoy `hola@arkhaorigin.com`). El formulario abre el correo del usuario (`mailto:`); se puede conectar a Formspree o similar.
- [ ] Poner las URLs reales de Instagram, TikTok, YouTube y Spotify en el footer.
- [ ] Revisar las cifras de la sección de estadísticas (son de ejemplo).
- [ ] Añadir fotos/videos reales de artistas y del estudio.
