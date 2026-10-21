# Marca de jerseys geek · Propuesta de negocio y de producto digital

> Documento de trabajo (Paso 0). Nada de esto está programado todavía: se programa cuando se aprueben las decisiones de la sección 9.
> Lo marcado **[POR DEFINIR]** es contenido provisional: no hay nombre, precios, materiales, proveedores ni plazos confirmados.

---

## 1. Cómo volverlo un buen negocio (lo más importante)

Una camiseta estampada compite por precio. Una **identidad deportiva coleccionable** compite por deseo. Estas son las palancas que mueven la aguja, en orden de impacto.

### 1.1 Producir solo lo que ya está vendido
- **Preventa con meta:** cada diseño abre una preventa con meta visible («faltan 18 reservas para producir el lote»). Si la alcanza, se produce. Si no, se devuelve el dinero o se cambia por otro diseño.
- **Qué gana el negocio:** riesgo de inventario casi nulo, dinero por adelantado para pagar al taller, y validación real (pagos, no «me gusta»).
- **Condición:** términos de preventa claros (plazo, reembolso, comunicación del avance). En Colombia esto también es una obligación legal; ver sección 8.

### 1.2 Escasez honesta: drops numerados
- Cada colección sale en **lotes limitados y numerados** (por ejemplo «Edición 01 · 50 unidades»), con fecha de cierre.
- La segunda tanda se hace solo si hay lista de espera. Eso crea urgencia y coleccionabilidad sin descuentos.

### 1.3 La comunidad diseña contigo
- **Votación de conceptos:** se publican 3 o 4 mockups conceptuales y la comunidad vota con su correo. El que gana va a muestra física.
- **Qué gana el negocio:** la lista de correos más valiosa posible (gente que ya eligió un producto) y datos para decidir qué producir.

### 1.4 El mayor margen está en los equipos, no en la persona suelta (B2B)
- Grupos de cosplay, clubes de fans, equipos de esports, ligas de fútbol amistosas, empresas geek y eventos: piden **10 a 30 jerseys con su propio escudo, nombres y números**.
- **Qué gana el negocio:** pedido grande, pagado por adelantado, sin riesgo de inventario, y cada equipo uniformado es publicidad caminando.
- Recomiendo un formulario de **«Uniforma a tu equipo»** desde la primera versión, con cotización. Se puede reutilizar el cotizador que ya existe en Cosplay Inc.

### 1.5 La ventaja injusta: Cosplay Inc
Ninguna marca nueva arranca con esto:
- **Audiencia:** 14 años de comunidad y 300 mil seguidores en Facebook.
- **Producción de imagen propia:** estudio, exteriores, foto inmersiva y video. Las campañas salen de casa, a costo marginal.
- **Presencia en eventos (SOFA, Comic Con):** un **stand de muestras** para medir tallas, tocar la tela y tomar preventas en persona, con el sistema de stand que ya opera.
- **Cosplayers como embajadores** de cada colección, con sesiones editoriales en exteriores.

### 1.6 Personalización con reglas (fase 2)
- Nombre y número en la espalda, con tipografía de la colección. Es el detalle que más eleva el precio percibido.
- Se habilita solo cuando el taller confirme qué puede hacer y cuánto cuesta. Hasta entonces, nada de personalización libre.

### 1.7 Números que hay que conocer antes de lanzar [POR DEFINIR con el taller]
| Concepto | Para qué sirve |
|---|---|
| Costo unitario por talla y por cantidad (10, 25, 50 u.) | Definir el lote mínimo rentable |
| Costo de muestra y de patrones | Inversión inicial por diseño |
| Empaque, etiqueta, bolsa, tarjeta de colección | Experiencia de unboxing |
| Comisión de pasarela y envío | Precio final y envío gratis desde X |
| Precio objetivo de venta | Margen bruto meta |

**Regla práctica:** el precio sale del valor percibido (diseño, edición limitada, calidad), no del costo. Un margen bruto saludable en moda de autor suele estar muy por encima del costo de producción. **Lo validamos con números reales, no con supuestos.**

---

## 2. El riesgo que puede tumbar la marca: propiedad intelectual

Los conceptos explorados se apoyan en franquicias con dueño:
- **Gotham:** DC / Warner Bros.
- **Hidden Leaf / shinobi:** Naruto, de Shueisha / Studio Pierrot.
- **Saiyan:** Dragon Ball, de Shueisha / Toei.

Usar sus nombres, escudos o personajes en productos a la venta **sin licencia** expone a:
- retiro de publicaciones en Instagram, Meta Shop y Mercado Libre;
- bloqueo de pasarelas de pago;
- reclamaciones legales.

En Colombia, la marca se registra ante la SIC y el derecho de autor protege a los personajes. Recomiendo:
1. **Colecciones originales como núcleo:** universos y equipos ficticios propios, con narrativa, escudo y paleta propios. Por ejemplo, un club de una ciudad gótica inventada, o una academia ninja de nombre original. Ese es el activo que la marca puede registrar, licenciar y escalar.
2. **Homenaje sin copia:** evocar géneros (shinobi, energía cósmica, noir urbano) sin nombres, logos, personajes ni frases registradas de terceros.
3. **Licencias oficiales cuando haya tracción:** la plataforma tendrá un campo «Origen: original / licenciado / homenaje» para priorizar y etiquetar cada colección.
4. **Antes de vender:** una **revisión con un abogado de propiedad intelectual** de los nombres de colección y del nombre de la marca, más una búsqueda de antecedentes en la SIC.

Los mockups hechos con IA se marcan como **«Diseño conceptual»** hasta que exista una muestra física aprobada. No se presenta como real una prenda que no se ha fabricado.

---

## 3. Arquitectura

```
                ┌──────────────── Sitio público (marca) ────────────────┐
 Visitante ───▶ │ Inicio · Tienda · Colección · Producto · Uniforma tu   │
                │ equipo · Nosotros · Tallas · FAQ · Contacto · Políticas│
                └───────┬──────────────────────────────┬─────────────────┘
                        │ carrito / preventa           │ votos, lista de espera, contacto
                        ▼                              ▼
                ┌───────────────┐              ┌──────────────────┐
                │ Pedidos       │              │ Interesados      │
                │ (estado de    │              │ (correo, talla,  │
                │  producción)  │              │  diseño votado)  │
                └──────┬────────┘              └────────┬─────────┘
                       ▼                                ▼
                ┌──────────────────── Admin ────────────────────────────┐
                │ Colecciones · Productos y variantes · Lotes/preventas │
                │ Pedidos y producción · Interesados · Cotizaciones B2B │
                │ Analítica (vistos, votos, intención, ventas)          │
                └───────────────────────────────────────────────────────┘
        Pagos: pasarela colombiana (Wompi / Bold / Mercado Pago) + Nequi QR
        Correo transaccional · WhatsApp (fase 2) · Analítica GA4 + Meta Pixel
```

**Modelo de datos (resumido):**
- **Colección:** nombre, narrativa, paleta, escudo, origen (original / licenciado / homenaje) y estado (próximamente, votación, preventa, disponible, agotada).
- **Producto:** deporte, colección, fotos frontal y posterior, y si es conceptual o muestra real.
- **Variante:** talla.
- **Lote:** meta de unidades, cupo, fecha de cierre y plazo de producción [POR DEFINIR].
- **Pedido:** estados en orden: pagado → en producción → control de calidad → enviado → entregado.
- **Interesado** y **voto.**

Así el catálogo crece agregando colecciones desde el admin, sin rediseñar la tienda.

---

## 4. Mapa de navegación

- **Inicio:** hero con el jersey protagonista, mensaje de marca, «Explorar colecciones» / «Novedades», drops activos con su contador de meta, colecciones recientes, por qué somos distintos, editorial, captación de correos.
- **Tienda:** filtros por deporte, colección, temática, talla y estado; orden por novedad, popularidad y precio.
- **Colección:** imagen principal, narrativa, paleta, productos, estado del lanzamiento y votación si aplica.
- **Producto:** galería frontal, posterior y detalles; etiqueta «Diseño conceptual» o «Muestra real»; talla con guía de ajuste; precio; disponibilidad real; plazo [POR DEFINIR]; botón «Comprar», «Reservar en preventa» o «Avísame», según el estado.
- **Uniforma a tu equipo (B2B):** formulario para cotizar.
- **Nosotros**, **Guía de tallas** (en cm), **Preguntas frecuentes**, **Contacto** (formulario y WhatsApp).
- **Políticas:** datos personales, términos, envíos, cambios y devoluciones, preventa, propiedad intelectual.

---

## 5. Dirección visual

- **Paleta base neutra:** negro, grafito, blanco hueso. El color lo pone cada colección (tokens por colección, como ya hacemos con las experiencias de temporada en Cosplay Inc).
- **Tipografía:**
  - **Títulos:** condensada deportiva, estilo dorsal o número de jersey.
  - **Texto:** grotesca limpia.
  - **Detalles técnicos:** monoespaciada (tallas, lote, «Edición 01/50»).
- **Composición editorial:** fotos grandes a sangre, mucho aire y fichas técnicas como de catálogo de equipamiento profesional.
- **Animaciones sutiles:** la tela en hover, el paso de frontal a posterior y el contador de meta. Sin neón, sin efectos de videojuego y sin nada infantil.
- **Cada colección tiene su «kit de identidad»:** escudo, paleta, patrón textil, número y narrativa corta. Eso hace que se sienta como un equipo real.

---

## 6. Tecnología y costos estimados

> Rangos de referencia: verifica las tarifas vigentes antes de decidir. No incluyen impuestos ni los costos de producción de la ropa.

| Opción | Qué es | Costo mensual aprox. | A favor | En contra |
|---|---|---|---|---|
| **A · Reutilizar la plataforma de Cosplay Inc (recomendada)** | Nueva tienda en el mismo sistema (Next.js + base de datos), con dominio y marca propios | Hosting ya pagado; solo el dominio (pago anual) | Ya tiene: preventa con cupos y apartado, pagos Nequi QR y comprobante único, admin, correos de marca, analítica, cotizador B2B, multi-idioma, stand para eventos | Hay que construir el catálogo de variantes y el carrito multi-producto |
| B · Shopify | Tienda alquilada | Plan básico en dólares, más comisiones por venta | Rápida de montar, muchas apps | Costo fijo en dólares, preventas y metas por apps de pago, menos control de la experiencia |
| C · WooCommerce | WordPress con tienda | Hosting + plugins | Barato | Mantenimiento, seguridad y velocidad dependen de plugins |

**Pagos en Colombia:**
- **Pasarela:** Wompi, Bold o Mercado Pago, que cobran comisión por transacción.
- **Nequi QR**, que ya opera en Cosplay Inc.

**Envíos:** tarifa fija por ciudad al inicio, configurable. Cálculo automático con transportadora en una fase posterior.

**Recomendación:** la **opción A**. El 70 % de lo que necesita la validación (preventa, meta, apartado, pagos, admin, correos, analítica, B2B) ya existe y está probado. El costo tecnológico mensual adicional es casi nulo, y el negocio queda con el control de sus datos y su experiencia.

---

## 7. Plan por etapas

**Etapa 1 · Validación (sin vender todavía)**
- Sitio de marca: inicio, colecciones conceptuales, votación, «Avísame» con talla, Nosotros, FAQ y políticas base.
- Captación de correos y medición: diseños más vistos y más votados, tallas más pedidas.
- **Meta:** decidir con datos qué 2 o 3 diseños van a muestra.

**Etapa 2 · Prototipos**
- Admin de colecciones y productos, guía de tallas con las medidas reales del taller.
- Fotos reales en estudio y exteriores (Cosplay Inc). La etiqueta «Muestra real» reemplaza a «Diseño conceptual».

**Etapa 3 · Tienda y preventa**
- Carrito, tallas, preventa con meta y lote numerado, pago con pasarela y Nequi, envíos configurables.
- Pedidos con estados de producción y correos en cada etapa.
- «Uniforma a tu equipo» con el cotizador.

**Etapa 4 · Escalamiento**
- Nuevas colecciones, personalización de nombre y número (con las reglas del taller), WhatsApp Business, ventas internacionales y colecciones licenciadas.

---

## 8. Legal y confianza (Colombia) — a validar con un abogado

- **Estatuto del Consumidor (Ley 1480 de 2011):**
  - información veraz del producto y del plazo;
  - derecho de retracto en ventas a distancia;
  - garantía;
  - reversión del pago.
- **Preventas:** condiciones transparentes de plazo, qué pasa si no se alcanza la meta y cómo se reembolsa.
- **Datos personales (Ley 1581 de 2012):** política de tratamiento y autorización expresa, por ejemplo para la lista de correos.
- **Propiedad intelectual:** ver sección 2, más el registro del nombre de la marca ante la SIC.
- **Facturación electrónica** según el régimen tributario del negocio.

---

## 9. Decisiones que necesito de ti

1. **Nombre de la marca:** ¿ya hay candidatos? Propongo validarlo con una búsqueda en la SIC antes de diseñar el logo.
2. **Estrategia de colecciones:** ¿arrancamos con **universos originales** (recomendado) o quieres explorar licencias desde el inicio?
3. **Plataforma:** ¿aprobamos la **opción A** (sobre la plataforma de Cosplay Inc, con dominio propio)?
4. **Dominio** que quieres usar.
5. **Primera etapa:** ¿empezamos por la **Etapa 1 (validación)** con 3 o 4 conceptos para votar?
6. **Taller:** cuando tengas cotizaciones, compárteme costo por unidad, lote mínimo, tiempos y tabla de tallas. Con eso se fijan precio, meta de lote y plazos.
