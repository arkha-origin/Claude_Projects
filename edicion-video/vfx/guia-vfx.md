# Guía de la librería de VFX

## 1. Ordenar la librería
```
libreria-vfx/
  fuego/       fuego_llamarada_negro_3s.mov
  rayo/        rayo_mano_alfa_2s.mov
  humo/        humo_suelo_negro_8s.mp4
  ...
```
- **Nombre del archivo:** `categoria_descripcion_fondo_duracion`. El catalogador adivina la categoría y el anclaje por las palabras del nombre.
- **Catalogar:** `python3 catalogar_vfx.py /ruta/libreria-vfx`. Escribe `catalogo.csv` y `catalogo.json`.
  - Detecta solo si el efecto tiene **transparencia (alfa)** o fondo **negro, blanco o verde**, y propone el modo de fusión.
- **Confirmar:** el editor revisa el CSV, corrige categoría, anclaje o modo y pone `confirmado = sí`. Si se vuelve a correr, lo corregido se respeta.

## 2. Modo de fusión según el fondo del efecto

| Fondo del efecto | Modo | Por qué |
|---|---|---|
| Transparente (alfa: ProRes 4444, PNG) | Normal | Ya trae su recorte. |
| Negro: fuego, rayos, chispas, energía | **Agregar (Add)** | Suma luz: brilla de verdad sobre el personaje. |
| Negro: humo, niebla, polvo, partículas suaves | **Pantalla (Screen)** | Aclara sin quemar; más natural en lo suave. |
| Blanco: tinta, sombras, grietas | **Multiplicar** | Solo oscurece. |
| Verde de croma | Normal + llave | DaVinci: Delta Keyer o 3D Keyer. CapCut: Quitar fondo → Croma. |

En **CapCut**, el modo de fusión está en el clip superpuesto → *Básico → Mezclar*. En **DaVinci**, en el Inspector → *Composite Mode*.

## 3. Escala y posición según el anclaje

| Anclaje | Escala típica | Dónde | Seguimiento |
|---|---|---|---|
| Manos u ojos | 20–40 % del cuadro | Centro del efecto en la palma u ojo | **Punto**: Tracker en Fusion, o en CapCut Seguimiento de movimiento sobre la mano |
| Arma (estela, chispas) | 30–60 % | Punta del arma | Punto; si gira, **dos puntos** (escala y rotación) |
| Cuerpo completo (aura) | 110–130 % del cuerpo | Detrás del personaje | **Magic Mask** del cuerpo: aura detrás y un poco delante en los bordes |
| Suelo (humo, polvo, impacto) | Ancho total del piso | Pies, en la línea del piso | **Planar Tracker** sobre el piso (la cámara de pasarela casi no se mueve) |
| Punto de impacto | 60–100 % | Donde golpea, 6–12 cuadros | Sin seguimiento |
| Pantalla completa (partículas, lluvia, nieve) | 100 % | Encima de todo | Sin seguimiento, opacidad 40–80 % |

Si el efecto está en horizontal y el video es vertical, **no lo estires**: escálalo por altura y recorta a los lados, o úsalo girado si no tiene dirección (humo, chispas).

## 4. Que el efecto parezca parte de la escena
1. **Color:** tíñelo hacia la paleta del mundo o del traje.
   - **DaVinci:** un nodo propio con Gain del color.
   - **CapCut:** Ajustar → HSL o Color.
2. **Luz sobre el personaje:** si el efecto brilla, el lado del personaje que lo mira debe recibir esa luz.
   - **DaVinci:** una ventana suave con el color del efecto, en Add o Soft Light, al 20–40 %, que siga el mismo tracker.
   - **CapCut:** una capa de color en Luz suave con máscara.
3. **Delante y detrás:** un aura o humo se ve real cuando una parte pasa detrás del personaje. Con Magic Mask o Quitar fondo se hace una copia del personaje encima del efecto.
4. **Movimiento:**
   - **Desenfoque de movimiento** en el efecto si la cámara o el personaje se mueven rápido.
   - **Temblor de cámara** de 4–6 cuadros en los impactos.
5. **Ritmo:** el efecto entra en el golpe de la música o en el punto bajo de la rampa, nunca entre dos golpes.
6. **Grano:** el mismo para todo, con el clip de ajuste de la plantilla encima de todas las capas.

## 5. DaVinci: plantillas de Fusion para no empezar de cero
Por cada tipo de anclaje, arma **una vez** una composición en Fusion y guárdala como plantilla (*macro*):
- **Punto:** MediaIn → Tracker → Merge (Apply Mode: Screen o Add) con el efecto → ColorCorrector → MediaOut.
- **Suelo:** el mismo esquema con Planar Tracker → Planar Transform.
- **Aura:** Magic Mask del personaje → el efecto detrás → el personaje encima (Merge).

Con la plantilla, el editor solo cambia el efecto y pulsa **Track**.
