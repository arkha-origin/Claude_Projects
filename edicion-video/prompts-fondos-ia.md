# Prompts de fondos IA por personaje · Video IA Inmersivo y Foto Inmersiva

Biblioteca de prompts para generar con **Higgsfield, Google Flow o Magnific** el mundo de cada personaje. El fondo se genera solo, sin personas; el cosplayer real se integra después en la edición (ver `plantillas-edicion.md`).

---

## 1. El flujo, de la pasarela al mundo del personaje

1. **Ficha del cliente.** Personaje, colores del traje y elemento (fuego, hielo, rayo…), con la plantilla del punto 6. Se elige el **arquetipo** de mundo más cercano de la biblioteca (punto 4).
2. **Fondo fijo.** En 9:16, sin personas, con el suelo y la perspectiva de la cámara de la pasarela (punto 2).
3. **Movimiento.** De imagen a video, 5–8 s, con un movimiento de cámara lento que acompañe la toma real; normalmente un *dolly* hacia adelante.
4. **Escalado y luz.** Escalar a 1080 × 1920 o más con **Magnific** y, si la luz del fondo no coincide con la de la pasarela, ajustarla con **Relight**.
5. **Montaje.** En DaVinci o CapCut:
   - recortar al personaje y poner el fondo detrás;
   - aplicar el LUT a los dos para que compartan color;
   - sumar niebla o partículas del mundo encima y *light wrap*.

**Tiempo objetivo:** el sistema le da 45 minutos de edición al Video IA Inmersivo. Generar el fondo toma 10–15; reutilizar el mundo de un personaje ya hecho (con el mismo prompt y la misma semilla) lo baja a casi nada.

---

## 2. Reglas para que el fondo funcione

- **No nombres la franquicia ni el personaje.** Describe el lugar: «aldea ninja de madera en el bosque», no el nombre de la serie. Da mejores resultados, evita bloqueos de las herramientas y evita copiar escenas protegidas. El traje ya es del cliente.
- **Sin personas, sin texto, sin logos.** Siempre.
- **La cámara de la pasarela manda:**
  - altura de los ojos (más o menos 1,2 m) y lente de 35 mm;
  - un camino o suelo libre que va del frente hacia el centro, donde se pondrá al personaje caminando hacia la cámara;
  - el horizonte recto, a un tercio desde arriba.
- **La luz también.** Escribe de dónde viene la luz principal según cómo estaban las luces de la pasarela (por ejemplo, «key light from front left, rim light from behind»). Si no coincide, el montaje se nota.
- **Color que haga resaltar el traje:** un traje rojo se lee mejor en un mundo azul o verde azulado; uno azul, en un mundo cálido.
- **Guarda prompt y semilla** de cada personaje: el próximo cliente con el mismo personaje usa el mismo mundo.
- **Prompts en inglés:** los modelos los siguen mejor. Abajo va cada prompt listo para copiar, con su explicación en español.

### Plantilla base (imagen)
```
Vertical 9:16 cinematic background plate, no people, no text, no logos.
[ESCENARIO]. Eye-level camera at 1.2 m height, 35mm lens, a clear [SUELO] path
leading from the foreground to the center of the frame, where a person will be
composited walking toward the camera. Key light from [DIRECCIÓN], [HORA/LUZ],
[ATMÓSFERA]. Color palette: [PALETA]. Sharp foreground floor, soft depth of field
in the far background, straight horizon in the upper third. Photorealistic,
cinematic, high detail, subtle film grain.
```

### Plantilla base (movimiento, de imagen a video)
```
Slow dolly-in, the camera moves gently forward at walking pace, 6 seconds, no cuts,
stable horizon, no people appear. [PARTÍCULAS] drift slowly through the air,
subtle [ELEMENTO EN MOVIMIENTO]. Seamless, calm, cinematic.
```

### Lo que hay que evitar (si la herramienta acepta prompt negativo)
```
people, person, character, crowd, text, letters, watermark, logo, signature,
tilted horizon, fisheye, warped architecture, blurry foreground, oversaturated,
cartoon, low resolution
```

---

## 3. Cómo usar cada herramienta

Los nombres de modelos y botones cambian seguido; revisa lo que muestra tu plan.

| Herramienta | Para qué usarla | Cómo |
|---|---|---|
| **Higgsfield** | Fondo fijo y movimiento | Imagen: GPT Image o similar, en 9:16 y alta resolución. Movimiento: imagen a video con un movimiento de cámara tipo *Dolly In* o *Push In*, 5–8 s. Guarda el trabajo en un proyecto por evento. |
| **Google Flow** (Veo) | Movimiento con mucha calidad y ambiente | *Frames to Video* con el fondo como primer cuadro; el movimiento se describe en el prompt («slow dolly in»). Si tu cuenta solo genera en 16:9, deja el camino en el centro y escala con Magnific antes de recortar a 9:16: un recorte de 1080p queda en 608 px de ancho. |
| **Magnific** | Calidad final | **Upscale** del fondo (imagen o video) a 4K. **Relight** para que la luz del fondo coincida con la de la pasarela. **Mystic** también sirve para generar el fondo fijo. |

### Alternativa: reestilizar el video real
Algunas herramientas transforman el video real completo (*video a video*). Tiene dos riesgos:
- **la cara del cliente puede cambiar**, así que la cara y el traje reales se dejan siempre en una capa recortada encima;
- **es subir la imagen del cliente a un servicio externo**, lo que pide su autorización (Ley 1581, datos personales). Con menores de edad, nunca sin la del acudiente.

Generar solo el fondo, desde texto, no usa ningún dato del cliente. Es el camino recomendado. **Con menores de edad es el único camino:** su autorización no cubre subir su imagen a servicios externos (ver `material-impreso-sofa/protocolo-menores.md`).

---

## 4. Biblioteca de mundos (arquetipos)

Cada mundo trae: para qué personajes sirve, el prompt de imagen, el detalle del movimiento y el LUT que mejor le queda.

### 1. Aldea ninja en el bosque
*Para:* anime de ninjas, shinobi, samuráis jóvenes. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. A traditional wooden
ninja village hidden in a dense forest, paper lanterns, wooden bridges and rooftops,
falling autumn leaves. Eye-level camera at 1.2 m, 35mm lens, a clear dirt path leading
from the foreground to the center. Warm late-afternoon sun from the left, soft haze.
Palette: warm orange, deep green, wood brown. Photorealistic, cinematic, high detail.
```
*Movimiento:* falling leaves drifting, lanterns gently swaying.

### 2. Ciudad cyberpunk de noche
*Para:* ciencia ficción, hackers, androides, personajes de videojuego futurista. · *LUT:* Neon
```
Vertical 9:16 cinematic background plate, no people, no text, no readable signs.
A narrow futuristic city street at night after rain, towering buildings with glowing
abstract neon shapes in red and electric blue, steam rising from vents, wet asphalt
reflecting the lights. Eye-level camera at 1.2 m, 35mm lens, clear wet street leading
to the center. Rim light from behind, cool ambient light. Photorealistic, cinematic.
```
*Movimiento:* light rain falling, steam drifting, neon flickering subtly.

### 3. Salón del trono de fantasía oscura
*Para:* reyes, reinas, villanos, caballeros oscuros. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. A vast gothic throne
hall, tall stone columns, a red carpet leading to an empty dark throne, candles and
iron chandeliers, light beams through stained glass windows. Eye-level camera at 1.2 m,
35mm lens, the carpet runs from the foreground to the center. Cold blue window light
from behind, warm candle light from the sides. Photorealistic, cinematic, high detail.
```
*Movimiento:* dust floating in the light beams, candle flames flickering.

### 4. Bosque mágico élfico
*Para:* elfos, hadas, druidas, princesas de fantasía. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. An enchanted ancient
forest with giant moss-covered trees, glowing mushrooms, soft mist and floating
fireflies, a stone path leading from the foreground to the center. Eye-level camera at
1.2 m, 35mm lens. Soft moonlight from behind, magical teal and gold glow. Photorealistic,
dreamy, cinematic, high detail.
```
*Movimiento:* fireflies drifting, mist slowly rolling.

### 5. Templo antiguo en ruinas
*Para:* aventureros, exploradores, guerreros, cazadores de tesoros. · *LUT:* Pasarela
```
Vertical 9:16 cinematic background plate, no people, no text. Ancient overgrown temple
ruins in a jungle, massive carved stone blocks, vines, a sunlit stone stairway path
leading from the foreground to the center. Eye-level camera at 1.2 m, 35mm lens. Golden
sunlight beams from the upper left through the canopy, humid haze. Photorealistic,
cinematic, high detail.
```
*Movimiento:* dust in the sunbeams, leaves moving softly.

### 6. Puente de mando de una nave espacial
*Para:* ciencia ficción, pilotos, capitanes, soldados espaciales. · *LUT:* Neon
```
Vertical 9:16 cinematic background plate, no people, no text, no readable screens.
The bridge of a large starship, clean metallic corridor with glowing blue light strips,
a huge window showing a nebula and stars at the end. Eye-level camera at 1.2 m, 35mm
lens, the corridor floor leads to the center. Cool blue light, red accent lights.
Photorealistic, cinematic, high detail.
```
*Movimiento:* stars drifting slowly outside the window, light strips pulsing softly.

### 7. Desierto alienígena con dos lunas
*Para:* guerreros del desierto, cazarrecompensas, personajes espaciales. · *LUT:* Pasarela
```
Vertical 9:16 cinematic background plate, no people, no text. An alien desert at dusk,
rippled orange sand dunes, strange rock arches, two large moons in a violet sky, a flat
sandy path leading to the center. Eye-level camera at 1.2 m, 35mm lens. Low warm sunset
light from the left, cool fill from the sky. Photorealistic, epic, cinematic.
```
*Movimiento:* sand blowing gently across the ground.

### 8. Azotea de ciudad de superhéroes
*Para:* superhéroes, vigilantes, villanos urbanos. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text, no logos. A skyscraper
rooftop at golden hour overlooking a huge city skyline, water towers, antennas, a clear
rooftop floor leading to the center edge. Eye-level camera at 1.2 m, 35mm lens. Sun low
behind the city creating a strong rim light, warm and dramatic sky. Photorealistic,
cinematic, high detail.
```
*Movimiento:* clouds moving, light wind, distant birds.

### 9. Biblioteca de una academia de magia
*Para:* magos, brujas, estudiantes de magia. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. A grand ancient library
of a magic academy, towering bookshelves, floating candles, spiral staircases, a long
wooden floor aisle leading to the center. Eye-level camera at 1.2 m, 35mm lens. Warm
candle light, soft golden haze, cool moonlight from tall windows behind. Photorealistic,
cinematic, high detail.
```
*Movimiento:* candles floating and bobbing, dust and sparkles drifting.

### 10. Cubierta de barco pirata en tormenta
*Para:* piratas, marinos, capitanes. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. The wooden deck of a large
pirate ship during a storm at sea, ropes and masts, torn sails, huge waves in the
background, lanterns swinging. Eye-level camera at 1.2 m, 35mm lens, the deck leads to
the center. Lightning from behind, warm lantern light. Photorealistic, dramatic, cinematic.
```
*Movimiento:* rain, sea spray, lanterns swinging, lightning flashes.

### 11. Escenario de concierto idol
*Para:* idols, cantantes de anime, personajes de música y K-pop o J-pop. · *LUT:* Neon
```
Vertical 9:16 cinematic background plate, no people, no audience faces, no text. A huge
empty concert stage, glossy floor, rows of moving spotlights and lasers in pink, red and
electric blue, confetti in the air, light haze. Eye-level camera at 1.2 m, 35mm lens,
the stage runway leads to the center. Strong backlight. Photorealistic, vibrant,
cinematic.
```
*Movimiento:* spotlights sweeping, confetti falling, lasers moving.

### 12. Ciudad posapocalíptica
*Para:* sobrevivientes, soldados, personajes de videojuegos de supervivencia. · *LUT:* Pasarela
```
Vertical 9:16 cinematic background plate, no people, no text, no readable signs. A ruined
city street years after a catastrophe, cracked asphalt with grass, abandoned cars covered
in dust, collapsed buildings, a hazy orange sky. Eye-level camera at 1.2 m, 35mm lens,
clear street leading to the center. Harsh sun from behind through dust. Photorealistic,
gritty, cinematic.
```
*Movimiento:* dust and ash drifting, light wind.

### 13. Reino de hielo
*Para:* personajes de hielo o nieve, reinas de invierno, guerreros del norte. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. A frozen kingdom of ice,
crystal-clear ice pillars and arches, snowy mountains behind, a smooth icy path leading
to the center, glowing blue cracks. Eye-level camera at 1.2 m, 35mm lens. Cold blue
ambient light, soft sun glare from behind. Photorealistic, majestic, cinematic.
```
*Movimiento:* snow falling softly, ice sparkles.

### 14. Inframundo de fuego y lava
*Para:* demonios, villanos, personajes de fuego. · *LUT:* Neon
```
Vertical 9:16 cinematic background plate, no people, no text. A volcanic underworld,
black obsidian rocks, rivers of glowing lava on both sides, a dark stone path leading to
the center, embers floating, red smoky sky. Eye-level camera at 1.2 m, 35mm lens. Strong
orange underlight from the lava, red rim light from behind. Photorealistic, intense,
cinematic.
```
*Movimiento:* embers rising, lava bubbling, heat haze.

### 15. Ciudad steampunk
*Para:* inventores, aviadores, personajes victorianos. · *LUT:* Pasarela
```
Vertical 9:16 cinematic background plate, no people, no text. A Victorian steampunk city
street, brass pipes, giant gears on buildings, airships in a hazy sky, cobblestone street
leading to the center, gas lamps. Eye-level camera at 1.2 m, 35mm lens. Warm amber light,
soft fog, sun from behind. Photorealistic, cinematic, high detail.
```
*Movimiento:* steam puffs, gears turning slowly, airships drifting.

### 16. Japón feudal al amanecer
*Para:* samuráis, ronin, personajes de época japonesa. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. A misty Japanese mountain
temple at dawn, a long path through rows of red torii gates leading to the center, stone
lanterns, cherry blossom trees. Eye-level camera at 1.2 m, 35mm lens. Soft pink dawn
light from behind, gentle mist. Photorealistic, serene, cinematic.
```
*Movimiento:* cherry blossom petals falling, mist drifting.

### 17. Pasillo de colegio japonés al atardecer
*Para:* anime escolar, comedia romántica, *slice of life*. · *LUT:* Pasarela
```
Vertical 9:16 cinematic background plate, no people, no text. A Japanese high school
hallway at sunset, polished wooden floor, big windows with warm orange light streaming
in, lockers and classroom doors, the hallway leads to the center. Eye-level camera at
1.2 m, 35mm lens. Strong warm side light from the windows on the left. Photorealistic,
nostalgic, cinematic.
```
*Movimiento:* dust in the sunlight, curtains moving gently.

### 18. Arena de torneo de pelea
*Para:* personajes de videojuegos de pelea, luchadores, artistas marciales. · *LUT:* Neon
```
Vertical 9:16 cinematic background plate, no people, no text, no logos. A dramatic
fighting tournament arena at night, octagonal stone stage, torches and spotlights, a
blurred empty stadium around, the stage floor leads to the center. Eye-level camera at
1.2 m, 35mm lens. Strong backlight, red and blue colored lights. Photorealistic, epic,
cinematic.
```
*Movimiento:* torch flames, spotlights sweeping, dust.

### 19. Mansión embrujada (Halloween)
*Para:* terror, vampiros, brujas, personajes góticos. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. A haunted Victorian mansion
hallway at night, old portraits without faces, dusty chandeliers, cobwebs, a long carpet
leading to the center, moonlight through tall windows. Eye-level camera at 1.2 m, 35mm
lens. Cold blue moonlight from behind, faint purple fog. Photorealistic, eerie, cinematic.
```
*Movimiento:* fog creeping on the floor, curtains moving, candle flicker.

### 20. Reino submarino
*Para:* sirenas, criaturas marinas, personajes del océano. · *LUT:* Editorial
```
Vertical 9:16 cinematic background plate, no people, no text. An underwater kingdom,
coral reefs and ancient sunken columns, schools of small fish, a sandy seabed path
leading to the center, sun rays from the surface. Eye-level camera at 1.2 m, 35mm lens.
Soft turquoise light, caustic light patterns on the sand. Photorealistic, magical,
cinematic.
```
*Movimiento:* bubbles rising, light rays shimmering, fish drifting.

---

## 5. Personalizar un mundo para un personaje concreto

Toma el arquetipo más cercano y cambia tres cosas, en este orden:
1. **Paleta:** la complementaria del traje. Por ejemplo: «Palette: deep teal and cold blue, so a red costume stands out».
2. **Elemento del personaje:** «floating sparks of lightning», «drifting ice crystals», «falling cherry petals», «glowing runes on the ground».
3. **Detalle de su historia, sin nombres:** «a broken sword stuck in the ground», «a giant moon behind», «a ruined castle on the horizon».

Para la **Foto Inmersiva** se usa el mismo fondo fijo, escalado con Magnific a 4K, sin el paso de movimiento.

---

## 6. Ficha por cliente (cópiala para cada pedido)

```
Código de reserva:
Personaje (como está en la reserva):
Arquetipo de mundo (1–20):
Colores del traje:            Paleta del fondo:
Elemento (fuego, hielo, rayo, magia…):
Dirección de la luz en la pasarela:
Herramienta y modelo:
Prompt final:
Semilla:
Notas para el editor:
```

En los prompts no van el nombre del cliente ni su código: solo la descripción del lugar.
