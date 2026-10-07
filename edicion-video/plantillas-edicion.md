# Plantillas de edición de video · Cosplay Inc · SOFA 2026

Plantillas para CapCut (escritorio) y DaVinci Resolve, una por cada producto de video. Cada plantilla trae su estructura viral: hook en el primer segundo, rampas de velocidad en el ritmo, corrección de color con el look de la marca, transiciones limpias y cierre con la marca.

**El objetivo es doble:** que cada video retenga en redes, y que el editor cumpla el tiempo que el sistema le da a cada pieza.

| Producto | Duración | Tiempo de edición (sistema) | Look |
|---|---|---|---|
| Aura | 10 s | 8 min | `CosplayInc_Neon` |
| Órbita | 20 s | 18 min | `CosplayInc_Editorial` |
| Video Pasarela | 30 s | 15 min | `CosplayInc_Pasarela` |
| Video FX | 30 s | 30 min | `CosplayInc_Neon` |
| Video IA Inmersivo | 30 s | 45 min | `CosplayInc_Editorial` |
| Grupal Video | 30–45 s | 25 min | `CosplayInc_Pasarela` |

**Archivos de la carpeta:**
- `luts/`: los tres looks de la marca en `.cube`. Sirven en DaVinci y en CapCut.
  - `vista-previa-luts.png` muestra el antes y el después sobre tonos de piel y colores típicos de trajes.
  - Las filas, de arriba abajo: original, Editorial, Neon y Pasarela.
- `marcadores/*.edl`: los tramos de cada producto como marcadores de colores para DaVinci.

---

## 1. Cómo se usa una plantilla

La idea es armar **un proyecto modelo por producto** una sola vez. Para cada cliente se duplica ese proyecto y se **reemplazan los clips**: el efecto, la rampa, el color y los textos se quedan.

### CapCut (escritorio)
1. **Proyecto modelo.** Créalo en 9:16, 1080 × 1920, 30 fps, con clips de muestra en los tramos de la tabla del producto.
2. **Look.** Ajustar → LUT → importa el `.cube` del producto, a una intensidad de 70–100 %.
3. **Rampas.** Velocidad → Curva:
   - presets **Montaje**, **Héroe** o **Bala**, o una curva personalizada con los puntos de la tabla;
   - activa la **cámara lenta suave** (interpolación de cuadros) si el material no se grabó a alta velocidad.
4. **Textos.** Hook arriba y cierre con logo. Guarda los estilos de texto como **predeterminados**.
5. **Por cliente.** Duplica el proyecto y usa clic derecho → **Reemplazar** sobre cada clip; se conservan velocidad, LUT, efectos y duración.
6. **Mejora de imagen.** Úsala con medida: **Reducir ruido** si hay poca luz y, si tu versión lo tiene, el filtro de mejora de calidad o *Enhance* a 30–50 %. Nunca más de un filtro encima del LUT.

### DaVinci Resolve
1. **Línea de tiempo modelo.** Crea una por producto: 1080 × 1920, 30 fps, inicio en 01:00:00:00.
2. **Marcadores.** Con la línea de tiempo abierta, importa `marcadores/<producto>.edl` desde *Timeline → Import → Timeline Markers from EDL*. Si tu versión no lo trae, ponlos a mano con **M** siguiendo la tabla.
3. **Color, en nodos.** Guarda el resultado como **Still** en la Galería y aplícalo a cada cliente.

   | Nodo | Qué hace |
   |---|---|
   | 1 · Balance | Exposición y balance de blancos (Primaries). |
   | 2 · Contraste | Curva; nada más en este nodo. |
   | 3 · Piel | Calificador sobre la piel; solo matiz y saturación, suave. |
   | 4 · Look | LUT `CosplayInc_*` con Key Output Gain al 70–100 %. |
   | 5 · Mejora | Nitidez leve (Blur → Sharpen 0,45) y reducción de ruido. |
   | 6 · Brillo | Solo en Neon y FX: Glow en las altas luces. |

   La reducción de ruido, el Glow, **Super Scale** y **Speed Warp** son de la versión Studio.
4. **Rampas.** Retime Controls (Ctrl + R) con puntos de velocidad, y luego Retime Curve con curvas suaves (bezier).
   - En Clip Attributes, **Retime Process: Optical Flow**.
   - Motion Estimation: **Speed Warp** (Studio) o **Enhanced Better**.
5. **Clip de ajuste.** Uno por encima de todo para grano fino y viñeta. Así el look es el mismo aunque cambien los clips.
6. **Por cliente.** Duplica la línea de tiempo y reemplaza cada clip con **F11** (Replace).

### Al grabar (lo que hace posible la edición)
- **Aura y Órbita:** graba a 120 fps (o 240) en 1080p. En una línea de tiempo de 30 fps eso da 25 % de velocidad (o 12,5 %) sin inventar cuadros.
- **Pasarela:** 60 fps como mínimo, para poder hacer rampas al 40–50 %.
- **Obturación:** 1/250 o más rápido en cámara lenta, para que no haya parpadeo con las luces del evento.
- **Video IA Inmersivo:** fondo lo más liso posible detrás de la pasarela, que ayuda al recorte del personaje.

---

## 2. Reglas de la estructura viral (todas las plantillas)

- **El primer segundo decide.** Abre con lo más fuerte: el gesto, el detalle o la pose final. Nada de logos ni pantallas negras al inicio.
- **Texto del hook:** 3 a 7 palabras, arriba al centro, sin tapar la cara. Que dure hasta el primer corte.
- **Zona segura:** deja libre el 20 % de abajo y el 15 % de la derecha, donde TikTok e Instagram ponen sus botones.
- **Corta en el ritmo.** Los cortes y los cambios de velocidad caen en el golpe de la música; el editor marca los golpes antes de cortar.
- **Rampas:** de rápido a lento justo *en* el gesto, nunca antes. Un golpe de sonido en el cambio vende la rampa.
- **Transiciones limpias.** El 80 % de los cortes son secos. Las demás:
  - flash blanco de 2–3 cuadros;
  - desenfoque de 6–8 cuadros;
  - zoom rápido (*whip*) con desenfoque de movimiento;
  - corte de continuidad, cuando la capa o el arma tapan el lente.

  Nada de cubos, giros 3D ni transiciones decorativas.
- **Cierre de 1,5–2 s:** pose congelada, logo de Cosplay Inc, nombre del personaje (el que se registró en la reserva) y la cuenta de la marca.
- **Final que conecta con el inicio.** Si el último cuadro empalma con el primero, el video se repite solo y cuenta más reproducciones.

### Sonido
- **Música con licencia** (Artlist, Epidemic, la biblioteca de YouTube, o el filtro de *uso comercial* de CapCut). Una canción comercial puede hacer que la red silencie el video del cliente.
- **Audio de tendencia:** recomiéndale al cliente agregarlo en la app al publicar.
- **Efectos:** zumbido (*whoosh*) en las rampas, impacto en los congelados, obturador en los flashes y subida (*riser*) antes del momento fuerte.
- **Volumen:** −14 LUFS integrados, picos en −1 dB.

### Exportación (el entregable)
- **Formato:** MP4 H.264 (o H.265), 1080 × 1920, 30 fps, 16–20 Mbps, audio AAC 320 kbps.
- **Peso:** así un video de 45 s pesa unos 110 MB, dentro del límite de **200 MB** de la entrega.
- **Subida:** se sube en **Ingesta → Entregas**, en la pieza del cliente. Las piezas con la etiqueta **Entrega Rápida** van primero.

---

## 3. Plantillas por producto

### Aura (ultra cámara lenta) · 10 s · look Neon
<!-- tabla:aura -->
| Tiempo | Tramo | Qué se hace |
|---|---|---|
| 0–1 s | **Hook** | Arranca al 150-200 % justo antes del gesto fuerte (giro de capa, pelo, arma). Frase del hook en pantalla. |
| 1–2 s | **Rampa entrada** | Rampa 150 % → 20 % en el instante del gesto. Golpe de sonido (impacto) en el cambio. |
| 2–7.5 s | **Cámara lenta héroe** | 20-25 %, la cámara gira. Acercamiento lento del 100 al 110 %. Sin cortes: es el plano que vende. |
| 7.5–8.5 s | **Rampa salida + flash** | Rampa 20 % → 150 % y flash blanco de 2-3 cuadros. |
| 8.5–10 s | **Cierre** | Pose final congelada 0,5 s, logo y nombre del personaje. |
<!-- /tabla -->

**Hooks (elige uno):**
- «Espera el giro»
- «Así se ve en cámara lenta»
- «POV: llegaste a SOFA así»

**Rampa (curva):** 150 % → 20 % (en el gesto) → 25 % sostenido → 150 % al salir. En CapCut, el preset **Héroe** se acerca; ajusta el punto bajo al gesto.

### Órbita (360° cámara lenta) · 20 s · look Editorial
<!-- tabla:orbita -->
| Tiempo | Tramo | Qué se hace |
|---|---|---|
| 0–1.5 s | **Hook detalle** | Plano macro de un detalle (ojo, prop, bordado) + pregunta en pantalla. |
| 1.5–3 s | **Revelación** | Rampa del detalle al cuerpo entero; el giro empieza. |
| 3–15 s | **Órbita + detalles** | Órbita al 25 %. En 3 golpes de la música, cortes a detalles (props, espalda, accesorios) con rampa 100 % → 30 %. |
| 15–18 s | **Giro completo** | Cierra la vuelta en la pose, acercamiento lento. |
| 18–20 s | **Cierre** | Congelado + logo + nombre del personaje. |
<!-- /tabla -->

**Hooks:**
- «¿Cuántas horas crees que tomó?»
- «Mira cada detalle»
- «Hecho a mano, pieza por pieza»

Solo con datos que dé el cliente: nunca inventes horas ni materiales.

**Rampas:** 3 rampas cortas (100 % → 30 %) en los detalles, sincronizadas con la música.

**Atajo de tiempo:** guarda los encuadres de detalle como **presets de reencuadre** (posición y escala) para reutilizarlos. Es lo que baja la Órbita de unos 18 a 10–12 minutos.

### Video Pasarela · 30 s · look Pasarela
<!-- tabla:pasarela -->
| Tiempo | Tramo | Qué se hace |
|---|---|---|
| 0–1.5 s | **Hook final primero** | Abre con la pose final congelada y el texto del hook; rebobinado rápido (efecto rewind) hacia la entrada. |
| 1.5–4 s | **Entrada** | Entrada a velocidad real, corte en el golpe de la música. |
| 4–20 s | **Caminata con rampas** | Alterna 100 % y 40 % en los pasos que caen en el ritmo. Movimiento de capa o arma al 25 %. Cambio de ángulo cada 3-4 s si hay segunda cámara. |
| 20–26 s | **Pose final** | Acercamiento lento, flashes, congelado con flash blanco y sonido de obturador. |
| 26–30 s | **Cierre** | Logo, nombre del personaje y hashtags del evento. |
<!-- /tabla -->

**Hooks:**
- «Así llegó a la pasarela»
- «El final es lo mejor»
- «Entrada de protagonista»

**Truco:** abrir con la pose final y luego «rebobinar» hasta la entrada mantiene a la gente mirando hasta volver a verla.

### Video FX · 30 s · look Neon
<!-- tabla:video-fx -->
| Tiempo | Tramo | Qué se hace |
|---|---|---|
| 0–1.5 s | **Hook poder** | Adelanto de 1 s del efecto más fuerte y 2 cuadros en negro. |
| 1.5–8 s | **Carga** | Caminata normal; brillo que crece en manos u ojos (máscara + glow). |
| 8–9 s | **Disparo FX** | Rampa 100 % → 15 %, flash, temblor de cámara y explosión del efecto (energía, fuego, rayos, según el personaje). |
| 9–22 s | **Caminata con aura** | Partículas y aura siguiendo al personaje; rampas en los golpes. |
| 22–27 s | **Pose FX** | Pose con el efecto al máximo, congelado y aberración cromática leve. |
| 27–30 s | **Cierre** | Logo, nombre del personaje y hashtags. |
<!-- /tabla -->

**Hooks:**
- «Espera a que active su poder»
- «Esto no es CGI… bueno, un poco»
- «Modo poder: activado»

**Efectos según el personaje:** energía o rayos (anime de acción), fuego o hielo (elementales), runas o magia (fantasía), chispas eléctricas (ciencia ficción).
- **En CapCut:** Efectos → Cuerpo, con el *Body effect* que sigue la silueta, más superposiciones de partículas en modo **Pantalla** o **Adición**.
- **En DaVinci:** Fusion, o superposiciones en fondo negro en modo **Add** o **Screen**.

### Video IA Inmersivo · 30 s · look Editorial
<!-- tabla:video-ia -->
| Tiempo | Tramo | Qué se hace |
|---|---|---|
| 0–1.5 s | **Hook antes/después** | 0,7 s de la pasarela real y corte (barrido o destello) al mundo IA. Texto: «Del SOFA a su mundo». |
| 1.5–5 s | **Revelación del mundo** | Plano abierto del fondo IA con el personaje integrado; movimiento de cámara lento (dolly). |
| 5–22 s | **Caminata en el mundo** | Caminata integrada, parallax, partículas del ambiente (niebla, chispas, nieve). Rampas en los golpes. |
| 22–27 s | **Pose heroica** | Acercamiento, luz del fondo que envuelve al personaje (light wrap), congelado. |
| 27–30 s | **Cierre** | Logo, nombre del personaje y hashtags. |
<!-- /tabla -->

**Hooks:**
- «Del SOFA a su mundo»
- «Lo llevamos a su universo»
- «Así se vería en su serie»

**Cómo se arma:** el flujo completo y los prompts del fondo están en `prompts-fondos-ia.md`.
1. Recortar al personaje: DaVinci **Magic Mask** (Studio) o CapCut **Quitar fondo** → Recorte automático.
2. Poner el fondo IA detrás.
3. Igualar luz y color con el LUT y, si hace falta, **Relight** de Magnific sobre el fondo.
4. Agregar el ambiente: niebla, partículas y *light wrap*.

### Grupal Video · 30–45 s · look Pasarela
<!-- tabla:grupal -->
| Tiempo | Tramo | Qué se hace |
|---|---|---|
| 0–2 s | **Hook equipo** | Pose grupal final congelada + «Conoce al equipo». |
| 2–5 s | **Entrada** | Entrada del grupo, corte en el golpe. |
| 5–38 s | **Momento de cada uno** | 3-4 s por integrante, cada uno con su rampa y el nombre de su personaje. Con más de 9, 2-3 s cada uno. |
| 38–42 s | **Pose grupal** | Todos juntos, acercamiento lento y flash. |
| 42–45 s | **Cierre** | Logo y hashtags del evento. |
<!-- /tabla -->

**Hooks:**
- «Conoce al equipo»
- «Este crew no vino a jugar»
- «¿Quién es tu favorito?»

El último deja que la gente comente su favorito.

**Por integrante:** rótulo con el nombre del personaje durante 1,5 s, en el mismo lugar para todos. Con un estilo guardado se cambia solo el texto.

---

## 4. Lista de revisión antes de subir el entregable
- [ ] El hook está en el primer segundo y fuera de la zona de botones.
- [ ] Las rampas caen en el gesto y el audio acompaña cada cambio.
- [ ] La piel se ve natural: en Neon, si se ve rosada, baja el LUT al 70 %.
- [ ] El nombre del personaje está bien escrito, como en la reserva.
- [ ] La música es con licencia y el volumen está en −14 LUFS.
- [ ] Está exportado a 1080 × 1920 y pesa menos de 200 MB.
