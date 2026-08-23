#!/usr/bin/env python3
"""
generate_content_pipeline.py

Genera el guion estructurado y los medios de un video con la Gemini API
(Google AI Studio) y los deja listos para davinci_auto_edit.py:

    1. Guion de N escenas (visual_prompt, audio_prompt, music_prompt,
       duration_seconds), de una de tres formas:
         a) Generado por Gemini a partir de --topic.
         b) Parseado por Gemini a partir de un guion propio en texto/markdown
            (--script_file), por ejemplo uno ya escrito con Claude.
         c) Reutilizado tal cual desde un manifest.json existente
            (--manifest_json), sin llamar a Gemini para nada de texto.
    2. Video por escena, con audio nativo sincronizado (dialogo/efectos), con
       el motor que elijas via --video_engine:
         - "omni" (default): Gemini Omni Flash, mucho mas barato que Veo.
         - "veo": Veo 3.1, mayor calidad/control cinematografico, mas caro.
       audio_prompt se inyecta en el prompt de video en vez de generarse
       aparte, porque ambos motores ya renderizan dialogo/efectos dentro del
       propio video.
    3. Lyria 3 (generateContent) -> un clip de musica de fondo unico para
       todo el video. Es el mismo motor que usa Google Flow Music por
       detras (Flow Music tampoco expone una API publica).
    4. Descarga todo a --output_dir con nombres consistentes y escribe
       manifest.json en el formato que espera davinci_auto_edit.py.

Nota: Ni Google Flow (video) ni Google Flow Music tienen API publica; son
interfaces web cerradas. Este script llama directamente a los modelos que
esas apps usan por debajo (Omni Flash / Veo, Lyria) a traves de la Gemini
API, que si es programable con una API key de pago.

Requisitos:
    pip install google-genai
    export GEMINI_API_KEY="tu-api-key-de-pago-de-ai-studio"
"""

from __future__ import annotations

import argparse
import base64
import json
import logging
import mimetypes
import os
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("generate_content_pipeline")

DEFAULT_TEXT_MODEL = "gemini-2.5-flash"
DEFAULT_OMNI_MODEL = "gemini-omni-flash-preview"
DEFAULT_VEO_MODEL = "veo-3.1-generate-preview"
DEFAULT_LYRIA_MODEL = "lyria-3-pro-preview"

# Duraciones discretas que soportan los modelos Veo actuales; cualquier
# duration_seconds del guion se ajusta al valor soportado mas cercano.
VEO_SUPPORTED_DURATIONS = (4, 6, 8)

SCENE_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "scenes": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "scene_id": {"type": "INTEGER"},
                    "order": {"type": "INTEGER"},
                    "visual_prompt": {"type": "STRING"},
                    "audio_prompt": {"type": "STRING"},
                    "music_prompt": {"type": "STRING"},
                    "duration_seconds": {"type": "NUMBER"},
                },
                "required": [
                    "scene_id",
                    "order",
                    "visual_prompt",
                    "audio_prompt",
                    "music_prompt",
                    "duration_seconds",
                ],
            },
        }
    },
    "required": ["scenes"],
}


# --------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------
def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


# --------------------------------------------------------------------------
# Modelo de datos
# --------------------------------------------------------------------------
@dataclass
class Scene:
    scene_id: int
    order: int
    visual_prompt: str
    audio_prompt: str
    music_prompt: str
    duration_seconds: float
    file_name: str = ""


def closest_supported_duration(requested: float) -> int:
    return min(VEO_SUPPORTED_DURATIONS, key=lambda d: abs(d - requested))


# --------------------------------------------------------------------------
# Paso 1: guion estructurado con Gemini (invencion desde un topic, o parseo
# de un guion propio ya escrito, ej. en Claude)
# --------------------------------------------------------------------------
def generate_script(
    client,
    text_model: str,
    scene_count: int,
    topic: Optional[str] = None,
    script_text: Optional[str] = None,
) -> list[Scene]:
    from google.genai import types

    if script_text:
        prompt = (
            "Actua como guionista audiovisual. A continuacion hay un guion "
            "ya escrito por el usuario. NO inventes contenido nuevo ni "
            "cambies las ideas: tu tarea es exclusivamente segmentarlo en "
            "escenas y estructurarlo en el JSON pedido, conservando fielmente "
            "las ideas, el tono y el orden originales.\n\n"
            f"--- GUION ORIGINAL ---\n{script_text}\n--- FIN DEL GUION ---\n\n"
            "Para cada escena completa:\n"
            "- visual_prompt: descripcion visual detallada y cinematografica para "
            "un generador de video IA (encuadre, iluminacion, movimiento de camara), "
            "basada en lo que describe el guion original para esa parte.\n"
            "- audio_prompt: el dialogo/narracion/efectos que el guion original indica "
            "para esa escena (el generador de video renderiza el audio de forma "
            "nativa, sincronizado con la imagen).\n"
            "- music_prompt: estilo/mood de musica de fondo sugerido para esa parte "
            "(si el guion original no lo especifica, infierelo del tono del texto).\n"
            "- duration_seconds: duracion sugerida de la escena (entre 4 y 8 segundos).\n\n"
            "El campo 'order' debe ir de 1 a N en el orden narrativo del video. "
            "La cantidad de escenas la definis vos segun como se segmente naturalmente "
            f"el guion (a modo de referencia, el usuario sugirio unas {scene_count})."
        )
        logger.info("Parseando guion propio con %s (sin inventar contenido nuevo)...", text_model)
    else:
        prompt = (
            f"Actua como guionista audiovisual. Crea un guion de exactamente "
            f"{scene_count} escenas para un video corto sobre: '{topic}'.\n\n"
            "Para cada escena completa:\n"
            "- visual_prompt: descripcion visual detallada y cinematografica para "
            "un generador de video IA (encuadre, iluminacion, movimiento de camara).\n"
            "- audio_prompt: dialogo, narracion o efectos de sonido que deberian "
            "escucharse DURANTE esa escena (el generador de video renderiza el "
            "audio de forma nativa, sincronizado con la imagen).\n"
            "- music_prompt: estilo/mood de musica de fondo sugerido para esa parte.\n"
            "- duration_seconds: duracion sugerida de la escena (entre 4 y 8 segundos).\n\n"
            "El campo 'order' debe ir de 1 a N en el orden narrativo del video."
        )
        logger.info("Generando guion con %s (%d escenas) sobre: %s", text_model, scene_count, topic)

    response = client.models.generate_content(
        model=text_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SCENE_RESPONSE_SCHEMA,
        ),
    )

    data = json.loads(response.text)
    scenes_raw = data["scenes"]
    scenes_raw.sort(key=lambda s: s["order"])

    scenes = []
    for s in scenes_raw:
        order = int(s["order"])
        scenes.append(
            Scene(
                scene_id=int(s.get("scene_id", order)),
                order=order,
                visual_prompt=s["visual_prompt"],
                audio_prompt=s.get("audio_prompt", ""),
                music_prompt=s.get("music_prompt", ""),
                duration_seconds=float(s.get("duration_seconds", 6)),
                file_name=f"{order:02d}_scene.mp4",
            )
        )

    logger.info("Guion generado: %d escenas.", len(scenes))
    return scenes


# --------------------------------------------------------------------------
# Paso 2: video por escena (con audio nativo) - motor Omni Flash o Veo 3.1
# --------------------------------------------------------------------------
def build_video_prompt(scene: Scene) -> str:
    prompt = scene.visual_prompt
    if scene.audio_prompt:
        prompt += f"\n\nAudio en escena (dialogo/efectos sincronizados): {scene.audio_prompt}"
    return prompt


def _download_uri(uri: str, api_key: str) -> bytes:
    request = urllib.request.Request(uri, headers={"x-goog-api-key": api_key})
    with urllib.request.urlopen(request) as response:
        return response.read()


def _extract_interaction_video(interaction, api_key: str) -> tuple[Optional[bytes], str]:
    """Busca el video generado en distintas formas posibles de respuesta de la
    Interactions API (el shape exacto puede variar entre versiones preview)."""
    output_video = getattr(interaction, "output_video", None)
    if output_video is not None:
        data = getattr(output_video, "data", None)
        if data:
            return base64.b64decode(data), getattr(output_video, "mime_type", "video/mp4")
        uri = getattr(output_video, "uri", None)
        if uri and uri.startswith("http"):
            return _download_uri(uri, api_key), getattr(output_video, "mime_type", "video/mp4")

    for attr_name in ("steps", "outputs"):
        for item in getattr(interaction, attr_name, None) or []:
            for content_item in getattr(item, "content", None) or []:
                if getattr(content_item, "type", None) != "video":
                    continue
                data = getattr(content_item, "data", None)
                if data:
                    return base64.b64decode(data), getattr(content_item, "mime_type", "video/mp4")
                uri = getattr(content_item, "uri", None)
                if uri and uri.startswith("http"):
                    return _download_uri(uri, api_key), getattr(content_item, "mime_type", "video/mp4")

    return None, "video/mp4"


def generate_scene_video_omni(
    client,
    omni_model: str,
    scene: Scene,
    output_dir: Path,
    aspect_ratio: str,
    poll_interval_s: int,
    max_polls: int,
    api_key: str,
) -> bool:
    """Genera el video de la escena con Gemini Omni Flash (mucho mas barato
    que Veo). No soporta fijar duration_seconds de forma explicita; la
    duracion del guion queda como referencia informativa."""
    prompt = build_video_prompt(scene)

    logger.info("Escena %s: solicitando video a %s (Omni Flash)...", scene.scene_id, omni_model)
    interaction = client.interactions.create(
        model=omni_model,
        input=prompt,
        background=True,
        response_format={"type": "video", "aspect_ratio": aspect_ratio},
    )

    for attempt in range(max_polls):
        status = getattr(interaction, "status", None)
        if status in ("completed", "failed"):
            break
        time.sleep(poll_interval_s)
        interaction = client.interactions.get(interaction.id)
        logger.debug("Escena %s: esperando render de Omni Flash (intento %d/%d)...", scene.scene_id, attempt + 1, max_polls)
    else:
        logger.error("Escena %s: timeout esperando el video de Omni Flash.", scene.scene_id)
        return False

    if getattr(interaction, "status", None) == "failed":
        logger.error("Escena %s: Omni Flash devolvio un error: %s", scene.scene_id, getattr(interaction, "error", "desconocido"))
        return False

    video_bytes, _mime_type = _extract_interaction_video(interaction, api_key)
    if not video_bytes:
        logger.error("Escena %s: no se pudo extraer el video de la respuesta de Omni Flash.", scene.scene_id)
        return False

    dest_path = output_dir / scene.file_name
    dest_path.write_bytes(video_bytes)
    logger.info("Escena %s: video guardado en %s.", scene.scene_id, dest_path)
    return True


def generate_scene_video_veo(
    client,
    veo_model: str,
    scene: Scene,
    output_dir: Path,
    aspect_ratio: str,
    poll_interval_s: int,
    max_polls: int,
) -> bool:
    from google.genai import types

    duration = closest_supported_duration(scene.duration_seconds)
    if duration != scene.duration_seconds:
        logger.info(
            "Escena %s: duration_seconds=%.1f ajustado a %ds (valores soportados: %s).",
            scene.scene_id,
            scene.duration_seconds,
            duration,
            VEO_SUPPORTED_DURATIONS,
        )

    veo_prompt = build_video_prompt(scene)

    logger.info("Escena %s: solicitando video a %s (Veo)...", scene.scene_id, veo_model)
    operation = client.models.generate_videos(
        model=veo_model,
        prompt=veo_prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            duration_seconds=duration,
            number_of_videos=1,
        ),
    )

    for attempt in range(max_polls):
        if operation.done:
            break
        time.sleep(poll_interval_s)
        operation = client.operations.get(operation)
        logger.debug("Escena %s: esperando render de Veo (intento %d/%d)...", scene.scene_id, attempt + 1, max_polls)
    else:
        logger.error("Escena %s: timeout esperando el video de Veo.", scene.scene_id)
        return False

    if operation.error:
        logger.error("Escena %s: Veo devolvio un error: %s", scene.scene_id, operation.error)
        return False

    generated = operation.response.generated_videos
    if not generated:
        logger.error("Escena %s: Veo no devolvio ningun video.", scene.scene_id)
        return False

    dest_path = output_dir / scene.file_name
    client.files.download(file=generated[0].video)
    generated[0].video.save(str(dest_path))
    logger.info("Escena %s: video guardado en %s.", scene.scene_id, dest_path)
    return True


def generate_scene_video(
    client,
    engine: str,
    veo_model: str,
    omni_model: str,
    scene: Scene,
    output_dir: Path,
    aspect_ratio: str,
    poll_interval_s: int,
    max_polls: int,
    api_key: str,
) -> bool:
    if engine == "omni":
        return generate_scene_video_omni(
            client, omni_model, scene, output_dir, aspect_ratio, poll_interval_s, max_polls, api_key
        )
    return generate_scene_video_veo(client, veo_model, scene, output_dir, aspect_ratio, poll_interval_s, max_polls)


# --------------------------------------------------------------------------
# Paso 3: Lyria 3 - musica de fondo
# --------------------------------------------------------------------------
def generate_background_music(client, lyria_model: str, music_prompt: str, output_dir: Path) -> Optional[str]:
    logger.info("Generando musica de fondo con %s...", lyria_model)
    response = client.models.generate_content(model=lyria_model, contents=music_prompt)

    parts = response.candidates[0].content.parts
    audio_part = next((p for p in parts if getattr(p, "inline_data", None)), None)
    if audio_part is None:
        logger.warning("Lyria no devolvio audio embebido; se omite la musica de fondo.")
        return None

    mime_type = audio_part.inline_data.mime_type or "audio/wav"
    extension = mimetypes.guess_extension(mime_type.split(";")[0].strip()) or ".wav"
    file_name = f"background_music{extension}"
    dest_path = output_dir / file_name

    audio_bytes = audio_part.inline_data.data
    if isinstance(audio_bytes, str):
        audio_bytes = base64.b64decode(audio_bytes)

    dest_path.write_bytes(audio_bytes)
    logger.info("Musica de fondo guardada en %s.", dest_path)
    return file_name


# --------------------------------------------------------------------------
# Manifest de salida (formato compatible con davinci_auto_edit.py)
# --------------------------------------------------------------------------
def write_manifest(output_dir: Path, project_name: str, scenes: list[Scene], music_file: Optional[str]) -> Path:
    manifest = {
        "project_name": project_name,
        "music_file": music_file,
        "scenes": [asdict(s) for s in scenes],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("manifest.json escrito en %s.", manifest_path)
    return manifest_path


# --------------------------------------------------------------------------
# Orquestacion
# --------------------------------------------------------------------------
def run_pipeline(args: argparse.Namespace) -> int:
    try:
        from google import genai
    except ImportError:
        logger.error("Falta la libreria google-genai. Instalala con: pip install google-genai")
        return 1

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("No se encontro GEMINI_API_KEY (env var) ni --api_key. Consigue una en Google AI Studio.")
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=api_key)

    if args.manifest_json:
        manifest_path = Path(args.manifest_json).expanduser().resolve()
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        scenes_raw = raw["scenes"] if isinstance(raw, dict) else raw
        scenes = [
            Scene(
                scene_id=int(s.get("scene_id", i + 1)),
                order=int(s.get("order", i + 1)),
                visual_prompt=s["visual_prompt"],
                audio_prompt=s.get("audio_prompt", ""),
                music_prompt=s.get("music_prompt", ""),
                duration_seconds=float(s.get("duration_seconds", 6)),
                file_name=s.get("file_name") or f"{int(s.get('order', i + 1)):02d}_scene.mp4",
            )
            for i, s in enumerate(scenes_raw)
        ]
        scenes.sort(key=lambda sc: sc.order)
        logger.info("Guion reutilizado desde %s (%d escenas); se omite el paso de Gemini texto.", manifest_path, len(scenes))
    elif args.script_file:
        script_path = Path(args.script_file).expanduser().resolve()
        if not script_path.is_file():
            logger.error("El guion indicado en --script_file no existe: %s", script_path)
            return 1
        script_text = script_path.read_text(encoding="utf-8")
        scenes = generate_script(client, args.text_model, args.scene_count, script_text=script_text)
    else:
        if not args.topic:
            logger.error(
                "Se requiere --topic, --script_file (guion propio) o --manifest_json (guion ya estructurado)."
            )
            return 1
        scenes = generate_script(client, args.text_model, args.scene_count, topic=args.topic)

    if args.dry_run:
        write_manifest(output_dir, args.project_id, scenes, music_file=None)
        logger.info("Dry-run: manifest generado sin llamar a Veo/Lyria.")
        return 0

    music_file = None
    if not args.skip_music:
        music_prompt = args.music_prompt or " / ".join(sc.music_prompt for sc in scenes if sc.music_prompt)
        if music_prompt:
            music_file = generate_background_music(client, args.lyria_model, music_prompt, output_dir)

    if not args.skip_video:
        failures = 0
        for scene in scenes:
            ok = generate_scene_video(
                client,
                engine=args.video_engine,
                veo_model=args.veo_model,
                omni_model=args.omni_model,
                scene=scene,
                output_dir=output_dir,
                aspect_ratio=args.aspect_ratio,
                poll_interval_s=args.poll_interval,
                max_polls=args.max_polls,
                api_key=api_key,
            )
            if not ok:
                failures += 1

        if failures:
            logger.error("%d/%d escenas fallaron al generar video.", failures, len(scenes))
            write_manifest(output_dir, args.project_id, scenes, music_file)
            return 1

    write_manifest(output_dir, args.project_id, scenes, music_file)
    logger.info("Pipeline de generacion de contenido completado con exito.")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera/parsea guion (Gemini), video (Omni Flash o Veo 3.1) y musica (Lyria 3) para el pipeline de DaVinci Resolve."
    )
    parser.add_argument("--topic", help="Tema/brief del video, para que Gemini invente el guion (requerido salvo con --script_file o --manifest_json).")
    parser.add_argument(
        "--script_file",
        default=None,
        help="Ruta a un guion propio en texto/markdown (ej. ya escrito con Claude) para que Gemini lo "
        "segmente en escenas SIN inventar contenido nuevo. Alternativa a --topic.",
    )
    parser.add_argument("--project_id", required=True, help="Identificador del proyecto (nombre de carpeta/proyecto).")
    parser.add_argument("--output_dir", required=True, help="Carpeta donde se descargan los medios y el manifest.json.")
    parser.add_argument("--scene_count", type=int, default=4, help="Cantidad de escenas a generar (default: 4; con --script_file es solo una referencia).")
    parser.add_argument(
        "--manifest_json",
        default=None,
        help="Reutiliza un guion ya estructurado en el formato de manifest.json (no llama a Gemini para el texto).",
    )
    parser.add_argument("--api_key", default=None, help="API key de Gemini (si no se usa la env var GEMINI_API_KEY).")
    parser.add_argument("--text_model", default=DEFAULT_TEXT_MODEL, help=f"Modelo de texto (default: {DEFAULT_TEXT_MODEL}).")
    parser.add_argument(
        "--video_engine",
        choices=["omni", "veo"],
        default="omni",
        help="Motor de video: 'omni' (Gemini Omni Flash, mas barato, default) o 'veo' (Veo 3.1, mas caro).",
    )
    parser.add_argument("--omni_model", default=DEFAULT_OMNI_MODEL, help=f"Modelo Omni Flash (default: {DEFAULT_OMNI_MODEL}).")
    parser.add_argument("--veo_model", default=DEFAULT_VEO_MODEL, help=f"Modelo Veo (default: {DEFAULT_VEO_MODEL}).")
    parser.add_argument("--lyria_model", default=DEFAULT_LYRIA_MODEL, help=f"Modelo de musica (default: {DEFAULT_LYRIA_MODEL}).")
    parser.add_argument("--music_prompt", default=None, help="Prompt de musica global (default: combina music_prompt de las escenas).")
    parser.add_argument("--aspect_ratio", default="16:9", help="Aspect ratio para Veo (default: 16:9).")
    parser.add_argument("--poll_interval", type=int, default=10, help="Segundos entre cada poll del render de Veo (default: 10).")
    parser.add_argument("--max_polls", type=int, default=60, help="Cantidad maxima de polls antes de dar timeout (default: 60).")
    parser.add_argument("--skip_video", action="store_true", help="No genera video (solo guion/musica).")
    parser.add_argument("--skip_music", action="store_true", help="No genera musica de fondo.")
    parser.add_argument("--dry_run", action="store_true", help="Solo genera y guarda el guion (manifest.json), sin llamar a Veo/Lyria.")
    parser.add_argument("--verbose", action="store_true", help="Logging en modo debug.")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)
    try:
        return run_pipeline(args)
    except Exception:
        logger.exception("Fallo inesperado en el pipeline de generacion de contenido.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
