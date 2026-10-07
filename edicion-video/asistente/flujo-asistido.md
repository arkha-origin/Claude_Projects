# Flujo de edición asistida: Claude como director de arte del editor

**Lo que se busca:** a partir del nombre del personaje y del video en el editor, Claude lee la toma (luz, color, cámara), propone el mundo y el prompt del fondo con la misma luz y el mismo tono, arma el plan de edición y de VFX, y además hace parte del trabajo dentro del programa.

**Principio que garantiza la consistencia:** el personaje real **nunca** se regenera con IA. Solo se genera lo que lo rodea, y la luz, la cámara y la paleta del fondo salen de leer los cuadros reales. Así el personaje se ve siempre como es, y el fondo se adapta a él.

## Qué se puede automatizar en cada programa

| | DaVinci Resolve | CapCut |
|---|---|---|
| Que Claude **vea** el video | Sí: un script exporta cuadros del clip seleccionado | Solo exportando cuadros a mano |
| Que Claude **escriba** en el proyecto | Sí, con la API de scripting: marcadores con notas, LUT, efectos en pistas superiores con modo de fusión, escala y posición, plantillas de Fusion | No: CapCut no tiene API pública |
| Seguimiento (*tracking*) | El script deja la composición armada; el editor pulsa **Track** | A mano, con Seguimiento de movimiento |

**Recomendación:** el flujo asistido completo va en **DaVinci**. En CapCut, Claude guía con la ficha y el editor ejecuta.

## Fases

### Fase 0 · desde mañana, sin instalar nada
Un Proyecto en claude.ai con las plantillas, la biblioteca de mundos, la guía de VFX y el catálogo. Por cada cliente:
1. el editor sube 3 cuadros, el producto y el personaje;
2. Claude devuelve la ficha: lectura de luz, mundo, prompts, plan de edición con códigos de tiempo, plan de VFX y la integración de color.

Ver `ficha-direccion-arte.md`. No toca la plataforma ni la pausa de cambios.

### Fase 1 · script «Asistente Cosplay Inc» para DaVinci (en el PC del editor)
1. El editor selecciona el clip y lo abre desde *Workspace → Scripts*.
2. Escribe el personaje y el producto.
3. El script exporta 3–5 cuadros y se los manda a Claude, junto con la plantilla y el catálogo de VFX. Recibe un plan estructurado.
4. En la línea de tiempo, el script:
   - pone **marcadores con notas** en cada código de tiempo (hook, rampas, entrada de VFX);
   - aplica el **LUT** en el nodo del look;
   - trae los **efectos del catálogo** a las pistas V2 y V3, en su momento, con su **modo de fusión, escala y posición**;
   - para los efectos que siguen una mano, el piso o un arma, deja la **plantilla de Fusion** lista para pulsar Track;
   - guarda la **ficha** junto al proyecto y copia los prompts del fondo.
5. El editor revisa, ajusta, hace las rampas finas y exporta.

**No toca la plataforma.** Es un script en el computador de edición. Para el jueves no da tiempo de hacerlo y probarlo bien con material real; lo más seguro es construirlo con las tomas de los primeros días de SOFA y usarlo desde el segundo fin de semana o después del evento.

### Fase 2 · después de SOFA, conectado a la plataforma
- **Datos de la reserva:** el script pide el código y la plataforma devuelve el personaje, el producto y si compró Entrega Rápida, sin escribir nada a mano.
- **La llave de Claude no sale del servidor:** el análisis pasa por la plataforma, como ya pasa con las sugerencias de la campaña.
- **Historial de fichas por reserva** y **mundos guardados por personaje**, con prompt y semilla: el próximo cliente con el mismo personaje arranca con su mundo listo.

## Decisiones que necesito para la Fase 1
1. **DaVinci gratuito o Studio, y qué versión.** Magic Mask, Speed Warp, la reducción de ruido y correr scripts desde fuera de DaVinci son de Studio. En la gratuita, el script se corre desde el menú *Workspace → Scripts*.
2. **Sistema operativo del computador de edición** (Windows o Mac).
3. **Llave de Claude para ese computador**, mientras no exista la Fase 2: una llave aparte, con **límite de gasto**, creada en la consola de Anthropic. Se guarda en ese computador; no se pega en el chat.
4. **Formato de la librería de VFX:** con transparencia, fondo negro o croma. El catalogador acepta los tres.

## Datos personales
Los cuadros llevan la cara del cliente. Mandarlos a Claude, o a cualquier servicio de IA, es un tratamiento de datos que debe estar cubierto por la autorización que da el cliente (Ley 1581); con menores, la del acudiente. Conviene revisar que la política de privacidad y los términos de la compra lo mencionen. A los prompts del fondo no va nada del cliente: solo la descripción del lugar.
