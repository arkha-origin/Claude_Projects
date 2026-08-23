# Pipeline de creacion y edicion automatica: Gemini + Veo + Lyria + DaVinci Resolve + n8n

Pipeline end-to-end orquestado desde n8n:

```
[n8n Trigger] -> generate_content_pipeline.py -> davinci_auto_edit.py -> (proyecto listo en Resolve)
                  (Gemini guion + Veo video          (arma la timeline)
                   + Lyria musica -> descarga)
```

## Archivos

- `generate_content_pipeline.py` — genera el guion (Gemini), el video de cada
  escena (Veo 3.1) y la musica de fondo (Lyria 3), y descarga todo a una
  carpeta local junto con un `manifest.json`.
- `davinci_auto_edit.py` — arma la timeline en DaVinci Resolve Studio a
  partir de esos medios y el `manifest.json`.
- `manifest.example.json` — ejemplo de guion estructurado.
- `requirements.txt` — dependencia `google-genai` para el script de generacion.

## Nota importante sobre Google Flow

**Google Flow (labs.google/flow) no tiene API publica** — es una interfaz web
cerrada pensada para uso manual, sin forma oficial de automatizarla (los
"wrappers" que existen son proyectos de terceros no oficiales que controlan
tu cuenta por scraping/CAPTCHA, no recomendados para un pipeline de
produccion). En vez de eso, este pipeline llama **directamente a los mismos
modelos que usa Flow por detras** a traves de la Gemini API, que si es
100% programable con una API key:

- **Veo 3.1** — genera el video de cada escena, incluyendo audio nativo
  sincronizado (dialogo/efectos), asi que no hace falta un paso aparte de
  locucion: el `audio_prompt` de cada escena se inyecta en el prompt de Veo.
- **Lyria 3** — genera la musica de fondo (clips de 30s) a partir de
  `music_prompt`.

Ambos requieren una API key de **Google AI Studio en tier de pago** (Veo y
Lyria no estan disponibles en el tier gratuito).

## Requisitos previos — generacion de contenido (Gemini/Veo/Lyria)

1. Crear una API key en [Google AI Studio](https://aistudio.google.com/apikey)
   con un proyecto de Google Cloud que tenga **facturacion habilitada**
   (tier de pago; Veo y Lyria no funcionan con el tier gratuito).
2. `pip install -r requirements.txt` (instala `google-genai`).
3. Exportar la key como variable de entorno:
   ```bash
   export GEMINI_API_KEY="tu-api-key"
   ```

## Uso manual — generacion de contenido

```bash
python3 generate_content_pipeline.py \
  --topic "Como funciona un centro de datos moderno" \
  --project_id "demo_project" \
  --output_dir "/path/to/media/demo_project" \
  --scene_count 4 \
  --verbose
```

Esto deja en `/path/to/media/demo_project/`: `01_scene.mp4`, `02_scene.mp4`,
..., `background_music.wav` y `manifest.json` — listo como entrada directa
de `davinci_auto_edit.py`.

Argumentos principales:

| Argumento | Requerido | Descripcion |
|---|---|---|
| `--topic` | si* | Tema/brief del video. *No requerido si se pasa `--manifest_json` para reusar un guion ya generado. |
| `--project_id` | si | Identificador del proyecto (nombre de carpeta). |
| `--output_dir` | si | Carpeta destino de los medios + manifest.json. |
| `--scene_count` | no | Cantidad de escenas a generar (default 4). |
| `--manifest_json` | no | Reusa un guion existente y solo genera video/musica (saltea el paso de Gemini texto). |
| `--music_prompt` | no | Prompt global de musica (default: combina los `music_prompt` de las escenas). |
| `--aspect_ratio` | no | Default `16:9`. |
| `--skip_video` / `--skip_music` | no | Para correr solo una parte del pipeline. |
| `--dry_run` | no | Genera solo el guion/manifest.json, sin llamar a Veo/Lyria (util para revisar el guion antes de gastar cuota). |
| `--verbose` | no | Logging en modo debug. |

Limitaciones a tener en cuenta:
- Veo solo soporta duraciones discretas (4/6/8s); `duration_seconds` del
  guion se ajusta automaticamente al valor soportado mas cercano.
- Lyria genera clips fijos de 30s; si el video final es mas largo, hay que
  recortar/loopear la musica manualmente en Resolve (el script de Resolve no
  hace loop automatico).
- Los nombres de modelo (`veo-3.1-generate-preview`, `lyria-3-pro-preview`)
  son *preview* y cambian con el tiempo; revisa
  [ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)
  si el script empieza a fallar por modelo no encontrado, y ajusta
  `--text_model` / `--veo_model` / `--lyria_model`.

---

## Requisitos previos — edicion en DaVinci Resolve

1. **DaVinci Resolve Studio** instalado (la version gratuita no habilita
   scripting externo completo en todas las plataformas; se recomienda Studio).
2. En Resolve: `Preferences > System > General` → habilitar
   **"External scripting using"** en `Local` o `Network`.
3. Python 3.10+ o 3.11+ (misma major/minor que soporta el "External scripting"
   de tu version de Resolve).
4. **DaVinci Resolve debe estar abierto** antes de ejecutar el script: la API
   se conecta a la instancia en ejecucion, no la lanza por si sola.
5. Importante para arquitecturas con VPS: el script solo puede correr en la
   **misma maquina** donde esta instalado y abierto DaVinci Resolve (se
   comunica via IPC local con `fusionscript`). Si n8n corre en un VPS Linux
   headless separado de la estacion de edicion, el nodo `Execute Command`
   debe ejecutarse en un **n8n worker/agent instalado en esa estacion**
   (Windows/macOS, o Linux con entorno grafico), no en el VPS remoto.

## Uso manual

```bash
python3 davinci_auto_edit.py \
  --project_name "demo_project" \
  --media_folder "/path/to/media/demo_project" \
  --manifest_json "/path/to/media/demo_project/manifest.json" \
  --timeline_name "Auto_Edit_Timeline" \
  --verbose
```

Argumentos:

| Argumento | Requerido | Descripcion |
|---|---|---|
| `--project_name` | si | Nombre del proyecto de Resolve (se abre si existe, se crea si no). |
| `--media_folder` | si | Carpeta local con los archivos generados (video/audio). |
| `--manifest_json` | no | Ruta al JSON con el orden y metadata de las escenas. Si se omite, el orden se infiere del prefijo numerico del nombre de archivo (`01_scene.mp4`, `02_scene.mp4`, ...). |
| `--timeline_name` | no | Nombre de la timeline a crear (default `Auto_Edit_Timeline`). |
| `--bin_name` | no | Nombre del bin del Media Pool (default: igual a `--project_name`). |
| `--verbose` | no | Logging en modo debug. |

Codigo de salida `0` en exito, distinto de `0` en fallo (util para que n8n
detecte errores del nodo `Execute Command`).

## Formato del manifest.json

```json
{
  "project_name": "demo_project",
  "music_file": "background_music.mp3",
  "scenes": [
    {
      "scene_id": 1,
      "order": 1,
      "visual_prompt": "...",
      "audio_prompt": "...",
      "music_prompt": "...",
      "duration_seconds": 6.5,
      "file_name": "01_scene.mp4",
      "narration_file": "01_narration.mp3"
    }
  ]
}
```

- `file_name`: clip de video de la escena, va a la pista **Video 1**, en orden.
- `narration_file` (opcional): locucion de esa escena, va a **Audio 1**, en el
  mismo orden que las escenas (la sincronizacion depende de que la duracion
  de la narracion sea similar a la del clip de video correspondiente, dado
  que la API de Resolve solo permite insertar clips en secuencia por pista,
  no en un timecode arbitrario).
- `music_file` (opcional, a nivel raiz del manifest): musica de fondo unica
  para todo el video, va a **Audio 2**.

También podés pasar el manifest como una lista simple de escenas (sin el
wrapper `{"scenes": [...]}`); el script lo detecta automáticamente.

## Invocacion desde n8n (nodos "Execute Command")

Workflow recomendado con dos nodos `Execute Command` encadenados:

**Nodo 1 — Generar contenido (Gemini + Veo + Lyria):**

```bash
python3 /ruta/al/script/generate_content_pipeline.py --topic "{{$json.topic}}" --project_id "{{$json.project_id}}" --output_dir "/path/to/media/{{$json.project_id}}" --scene_count {{$json.scene_count || 4}}
```

**Nodo 2 — Armar timeline en DaVinci Resolve** (encadenado despues del nodo 1):

```bash
python3 /ruta/al/script/davinci_auto_edit.py --project_name "{{$json.project_id}}" --media_folder "/path/to/media/{{$json.project_id}}" --manifest_json "/path/to/media/{{$json.project_id}}/manifest.json" --timeline_name "Timeline_{{$json.project_id}}"
```

Notas:

1. En el nodo 1, definir `GEMINI_API_KEY` como variable de entorno del
   proceso (en **Options > Environment Variables** del nodo, o a nivel del
   worker de n8n) — **no** pasarla como argumento de linea de comandos para
   que no quede expuesta en logs/histórico de ejecuciones de n8n.
2. Ambos nodos necesitan poder ejecutarse en la maquina correcta: el nodo 1
   solo necesita salida a internet (puede correr en el VPS de n8n); el
   nodo 2 **debe** correr en la maquina donde esta abierto DaVinci Resolve
   (ver seccion siguiente) — si son maquinas distintas, el nodo 2 tiene que
   ejecutarse via un worker de n8n instalado en la estacion de edicion, o
   via SSH/Remote hacia esa maquina.
3. En **Options** de cada nodo, activar "Continue on Fail" solo si querés
   capturar el error y manejarlo en un nodo siguiente (por ejemplo
   notificando por Slack/email); de lo contrario dejalo desactivado para que
   el workflow se detenga ante un fallo.
4. El `stdout`/`stderr` de ambos nodos contiene el log estructurado del
   script (`[INFO]`, `[WARNING]`, `[ERROR]`), util para debugging directo
   desde la ejecucion de n8n.
5. Recomendado: agregar un nodo `IF` entre el nodo 1 y el nodo 2 que valide
   que `manifest.json` y los archivos de video/musica esperados existen
   antes de invocar `davinci_auto_edit.py`, para evitar armar una timeline
   con medios incompletos (por ejemplo si alguna escena de Veo fallo).

### Variables de entorno opcionales

Si tu instalacion de Resolve no esta en la ruta estandar, definí antes de
ejecutar (o como variables de entorno del proceso de n8n/worker):

```bash
export RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules"
```

(En Windows/macOS, usar las rutas equivalentes de
`Preferences > System > General > External scripting`.)
