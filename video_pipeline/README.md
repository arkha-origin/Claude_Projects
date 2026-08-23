# Pipeline de edicion automatica con DaVinci Resolve + n8n

Este directorio contiene el script `davinci_auto_edit.py`, que arma una
timeline en DaVinci Resolve Studio a partir de clips generados por IA y un
`manifest.json` con el guion estructurado.

## Archivos

- `davinci_auto_edit.py` — script principal (CLI).
- `manifest.example.json` — ejemplo de guion estructurado.

## Requisitos previos

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

## Invocacion desde n8n (nodo "Execute Command")

1. Agregar un nodo **Execute Command** despues del paso que descarga los
   medios generados (video/audio) al directorio local.
2. Command:

```bash
python3 /ruta/al/script/davinci_auto_edit.py --project_name "{{$json.project_id}}" --media_folder "/path/to/media/{{$json.project_id}}" --manifest_json "/path/to/media/{{$json.project_id}}/manifest.json" --timeline_name "Timeline_{{$json.project_id}}"
```

3. En **Options**, activar "Continue on Fail" solo si querés capturar el
   error y manejarlo en un nodo siguiente (por ejemplo notificando por
   Slack/email); de lo contrario dejalo desactivado para que el workflow se
   detenga si DaVinci Resolve no pudo procesar el proyecto.
4. El `stdout`/`stderr` del nodo va a contener el log del script
   (`[INFO]`, `[WARNING]`, `[ERROR]`), util para debugging directo desde la
   ejecucion de n8n.
5. Recomendado: agregar un nodo previo que valide (`IF`) que la cantidad de
   archivos descargados coincide con la cantidad de escenas del manifest,
   antes de invocar el script, para evitar ejecutar la automatizacion con
   medios incompletos.

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
