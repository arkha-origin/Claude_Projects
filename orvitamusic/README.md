# Orvita Music — orvitamusic.com

Sitio web de **Orvita Music**: roster y showcase, booking directo, producción audiovisual 4K, live sessions y contenido, sync, consultoría 360° y songwriting camps.

Sitio **estático** (HTML + CSS + JS), sin build. Escena 3D con Three.js (r169, incluido en `js/vendor/`, licencia MIT).

## Estructura

```
orvitamusic/
├── index.html          # Página única (hero 3D, servicios, proceso, estudio, próximamente)
├── css/styles.css      # Sistema visual y animaciones
├── js/main.js          # Escena 3D + interacciones (tilt, cursor, reveal)
├── js/vendor/          # three.module.min.js + licencia
├── assets/             # logo.svg, logo-mark.svg, favicon.svg
├── BRAND.md            # Guía de identidad de marca
└── PROMPTS-FOTOS.md    # Prompts para generar las fotos en Google Flow
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

## Pendientes (cuando Orvita tenga su propio dominio)

- [x] Contacto: WhatsApp +57 314 440 9823 en todos los botones (mensajes prellenados por servicio).
- [ ] Correo @orvitamusic.com y formulario propio (opcional).
- [ ] Funciones propias de cada planeta (hoy llevan a WhatsApp): Book Artist, showreel y cotizador audiovisual, paquetes de contenido, biblioteca de beats, agenda y pago de mentorías, inscripción a camps.
- [ ] Fichas de los artistas del roster: fotos, música y trayectoria.
- [ ] Redes sociales en el footer (Instagram, TikTok, YouTube, Spotify).
- [ ] Cifras / estadísticas, cuando haya resultados que mostrar.
- [ ] Fotos: generarlas con los prompts de `PROMPTS-FOTOS.md` y guardarlas en `assets/img/`.
