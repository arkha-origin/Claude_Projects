# Edición de video · Cosplay Inc

| Archivo | Qué es |
|---|---|
| `plantillas-edicion.md` | Plantillas por producto (Aura, Órbita, Video Pasarela, Video FX, Video IA Inmersivo y Grupal Video): hook, tramos, rampas, color, transiciones, sonido y exportación, en CapCut y DaVinci. |
| `prompts-fondos-ia.md` | Flujo y 20 mundos con prompts para generar los fondos del Video IA Inmersivo y la Foto Inmersiva (Higgsfield, Google Flow, Magnific). |
| `luts/*.cube` | Los tres looks de la marca: Editorial, Neon y Pasarela. Se importan en DaVinci y en CapCut. `vista-previa-luts.png` muestra el antes y el después. |
| `marcadores/*.edl` | Los tramos de cada producto como marcadores de colores para DaVinci (*Timeline → Import → Timeline Markers from EDL*). |

Para cambiar un look o un tramo, edita los datos y vuelve a generar:

```
python3 luts/generar_luts.py
python3 marcadores/generar_marcadores.py   # rehace los .edl y las tablas del documento
```
