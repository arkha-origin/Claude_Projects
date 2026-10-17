# Prompt para abrir el chat de la productora audiovisual

Copia todo lo que está dentro del bloque de abajo y pégalo como **primer mensaje**
del chat nuevo. Antes de pegarlo, completa lo que está entre `[corchetes]`. Lo
que no sepas déjalo así: el asistente lo va a preguntar en vez de inventarlo.

---

```text
Vamos a construir el sistema web de una PRODUCTORA AUDIOVISUAL reutilizando el
sistema que ya construimos para Cosplay Inc (estudio de fotografía y video
cosplay). Responde siempre en español neutro.

## 1. La empresa nueva
- Nombre comercial: [NOMBRE]
- Dominio: [DOMINIO, ej. productora.com]
- Ciudad / país: [Bogotá, Colombia]
- Qué vende (servicios y paquetes): [videos corporativos, comerciales, videoclips,
  eventos, contenido para redes, podcast, drones, fotografía de producto…]
- Cómo vende hoy: [cotización por proyecto / paquetes con precio fijo / ambos]
- Clientes típicos: [marcas, agencias, artistas, eventos, personas]
- Equipo y roles: [productor, director, editor, camarógrafo, vendedor…]
- Medios de pago: [QR Nequi / transferencia / pasarela / abonos por etapas]
- Identidad: logo [ruta o enlace], colores [hex], tono de marca [sobrio, creativo…]
- Repositorio nuevo en GitHub: [owner/repo] (o pídeme crearlo)
- Servidor: [mismo VPS de Cosplay Inc con otro dominio / VPS nuevo]

## 2. De dónde partimos
El sistema de origen está en el repositorio arkha-origin/Cosplay_Inc (rama
claude/cosplay-inc-project-lerlst). La documentación y los planes viven en
arkha-origin/Claude_Projects. Pide acceso a los dos con add_repo y LÉELOS
antes de proponer nada: no partas de cero ni copies a ciegas.

Stack (mantenerlo igual):
- Monorepo npm workspaces: apps/web (Next.js 15 App Router, React 19, server
  actions con useActionState, Tailwind v4), packages/db (Prisma 6 + Postgres,
  seed idempotente), packages/pricing-engine (precios y modalidades).
- sharp para imágenes, ffmpeg para video, @anthropic-ai/sdk para textos con
  Claude, Playwright para pruebas e2e.
- Despliegue: GitHub Actions `desplegar.yml` con runner propio en el VPS
  (sin SSH entrante). Cada push a la rama de trabajo despliega y corre seed +
  verificaciones. Traefik delante. Los secretos SOLO en el .env del servidor.

## 3. Qué reutilizar (módulos de Cosplay Inc) y cómo adaptarlo
Reutilizar casi tal cual:
- Autenticación y roles (src/server/auth.ts): administrador, vendedor, editor…
  → renombrar a los roles de la productora.
- Administración con menú lateral (src/app/admin, components/nav-admin.tsx).
- Clientes y fichas: ficha del cliente, editar datos, historial, teléfono que
  abre WhatsApp en todas partes (components/whatsapp-cliente.tsx).
- Botón flotante de WhatsApp en todas las pantallas (components/whatsapp-flotante.tsx)
  y asistente de preguntas frecuentes (components/asistente-*.tsx).
- Pagos: QR de Nequi con comprobante y cola «Pagos por confirmar»
  (server/pagos/proveedor.ts → pagoQrNequi, server/pago-directo.ts,
  app/admin/confirmar-pagos). Bold queda opcional.
- Preventas / reservas con abono (lib/preventas.ts, server/preventas.ts).
- Proyectos personalizados con etapas, propuesta, pagos por etapa y enlace
  privado del cliente (server/proyectos.ts, app/proyecto, app/admin/proyectos)
  → ES EL CORAZÓN de una productora: cotización → propuesta → anticipo →
  preproducción → rodaje → edición → revisiones → entrega final.
- Encuestas/brief antes de cotizar (lib/brief*.ts, server/encuestas.ts,
  app/sesionpersonalizada) → brief de producción (objetivo, público, duración,
  formatos, locaciones, fechas, presupuesto, referencias).
- Galería de entrega con marca de agua, selección y compra de adicionales
  (server/galeria.ts, app/g/[codigo]) → sala de revisión de cortes: el cliente
  ve el video con marca de agua, deja comentarios y aprueba.
- Almacén de archivos, miniaturas, videos derivados y marca de agua
  (server/almacen/*).
- «Para tus redes»: formatos 4:5, 1:1, 9:16, 16:9, reels y videos adaptados
  (server/almacen/redes.ts, reel.ts, video-redes.ts).
- Estudio de contenido para redes (app/admin/contenido, components/estudio-contenido.tsx,
  server/estudio-contenido.ts, server/acciones-estudio.ts,
  server/almacen/video-dinamico.ts): textos con Claude, imagen, carrusel, top,
  encuesta, reel/video con estilos dinámicos, composición, fondos, editor de
  textos, vista previa en vivo y descarga en ZIP.
- Portafolio público con categorías por producto (server/portafolio.ts,
  app/portafolio) → reel de la productora por tipo de servicio.
- Blog con artículos en código y fecha de publicación (lib/blog/*), sitemap,
  llms.txt y SEO.
- Directorio de lugares (estudios/locaciones) con foto de su web y Google Maps
  (server/directorio.ts) → directorio de locaciones y foros de grabación.
- Notificaciones y correos con plantillas editables (registrarEvento,
  plantillas, textos editables desde Administración → Textos).
- Campaña de WhatsApp asistida con sugerencias de Claude (admin/campanas).
- Textos del sitio editables desde el admin y traducción es/en/pt.

Adaptar o reemplazar:
- El «stand» de ferias y la parrilla de horarios por estación (SOFA) NO aplican
  tal cual: convertirlos en agenda de rodajes y equipo (quién, dónde, qué
  equipo), salvo que la productora haga activaciones en eventos.
- Catálogo de productos por evento → catálogo de servicios y paquetes.
- Niveles de edición / acabados → niveles de postproducción (corte básico,
  color, sonido, motion graphics, subtítulos).
- Menores de edad, cosplay, personajes y hashtags del evento → quitar o
  convertir en campos del proyecto (marca, campaña, derechos de imagen).

Nuevo para la productora (proponer y confirmar conmigo antes):
- Cotizador por proyecto (días de rodaje, equipo, personal, locación,
  postproducción, entregables, licencias de música).
- Calendario de rodajes y reserva de equipo.
- Revisiones de corte con comentarios por minuto y control de versiones.
- Contratos/órdenes de servicio y cesión de derechos.
- Gastos por proyecto (personal por día, alquileres, transporte) y margen.

## 4. Reglas de trabajo (obligatorias)
- Nunca inventes reglas comerciales (precios, descuentos, políticas, plazos):
  pregúntame. Si tienes que elegir algo para avanzar, dímelo explícitamente.
- Dinero siempre en pesos colombianos enteros (sin decimales).
- No escribas nombres de personas reales en documentos, blog ni código.
- Seguridad: no me pidas ni pegues contraseñas o llaves en el chat. Las
  credenciales van solo en el .env del servidor; comparte solo NOMBRES de
  variables. Nunca desactives TLS. Datos de clientes (Ley 1581) fuera del chat y
  de GitHub. Acciones destructivas en producción: pedir confirmación.
- No subir imágenes de menores a servicios de IA. Imágenes generadas: personas
  ficticias adultas, sin personajes con derechos de autor.
- Cambios mínimos y con pruebas: tsc, build y e2e del módulo tocado antes de
  cada push. Commits claros en español. No crear PR salvo que lo pida.
- Explícame en lenguaje sencillo qué quedó, dónde lo veo y qué falta de mi lado.

## 5. Cómo empezar
1. Lee los dos repositorios y resume en una tabla: módulo de Cosplay Inc →
   se reutiliza / se adapta / se descarta para la productora.
2. Hazme las preguntas que falten de la sección 1 (en una sola tanda, máximo 6).
3. Propón el plan por fases:
   - Fase 1: base del monorepo copiada y renombrada, marca, home, portafolio,
     contacto WhatsApp, admin con usuarios y textos, despliegue funcionando.
   - Fase 2: brief + cotización + proyectos con etapas y pagos por QR.
   - Fase 3: sala de revisión y entrega de videos.
   - Fase 4: estudio de contenido, blog/SEO, campañas.
4. Arranca la Fase 1 cuando la apruebe.
```

---

## Notas para ti (no hace falta pegarlas)

- **Antes de abrir el chat:** crea el repositorio nuevo vacío en GitHub (o pide
  que lo cree) y define si va en el mismo VPS con otro dominio. Si es el mismo
  servidor, la nueva app necesita su propia base de datos y su propio `.env`.
- **Secretos:** la productora necesita sus propias llaves (base de datos,
  `AUTH_SECRET`, `ANTHROPIC_API_KEY`, correo). No reutilices las de Cosplay Inc;
  recuerda además que en este proyecto hay llaves pendientes de rotar.
- **Qué conviene tener a mano:** logo en PNG/SVG, colores, lista de servicios
  con precios de referencia, 10–20 piezas del portafolio y el número de WhatsApp.
