#!/usr/bin/env python3
"""
davinci_auto_edit.py

Automatiza el armado de una linea de tiempo en DaVinci Resolve (Studio) a
partir de clips generados por un pipeline de IA (n8n) y un manifiesto JSON
que describe el orden y los metadatos de cada escena.

Flujo:
    1. Conecta con la instancia de DaVinci Resolve que ya debe estar abierta.
    2. Abre (o crea) el proyecto indicado.
    3. Crea un bin dedicado dentro del Media Pool.
    4. Importa todos los medios de la carpeta indicada.
    5. Ordena los clips segun el manifiesto (o, en su defecto, segun el
       prefijo numerico del nombre de archivo).
    6. Crea una timeline nueva e inserta:
         - Video      -> pista de Video 1
         - Narracion  -> pista de Audio 1 (sincronizada por orden de escena)
         - Musica     -> pista de Audio 2
    7. Guarda el proyecto.

Requisitos:
    - DaVinci Resolve Studio debe estar abierto (la API de scripting externo
      solo funciona contra una instancia en ejecucion).
    - Python 3.10+ / 3.11+ (misma version que usa el "External scripting"
      de Resolve, revisar Resolve > Preferences > System > General).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import platform
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("davinci_auto_edit")

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".m4a", ".flac"}


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
# Carga dinamica del modulo DaVinciResolveScript
# --------------------------------------------------------------------------
def _default_resolve_paths() -> tuple[str, str]:
    """Devuelve (RESOLVE_SCRIPT_API, RESOLVE_SCRIPT_LIB) por defecto segun el SO."""
    system = platform.system()

    if system == "Windows":
        api = r"%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
        lib = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
        return os.path.expandvars(api), os.path.expandvars(lib)

    if system == "Darwin":
        api = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
        lib = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
        return api, lib

    # Linux (incluye instalaciones estandar de Resolve Studio)
    api = "/opt/resolve/Developer/Scripting"
    lib = "/opt/resolve/libs/Fusion/fusionscript.so"
    return api, lib


def load_resolve_module():
    """
    Carga el modulo DaVinciResolveScript respetando RESOLVE_SCRIPT_API /
    RESOLVE_SCRIPT_LIB si ya estan definidas en el entorno, o usando las
    rutas por defecto del sistema operativo en caso contrario.
    """
    default_api, default_lib = _default_resolve_paths()

    script_api = os.environ.get("RESOLVE_SCRIPT_API", default_api)
    script_lib = os.environ.get("RESOLVE_SCRIPT_LIB", default_lib)

    os.environ["RESOLVE_SCRIPT_API"] = script_api
    os.environ["RESOLVE_SCRIPT_LIB"] = script_lib

    modules_path = os.path.join(script_api, "Modules")
    if modules_path not in sys.path:
        sys.path.append(modules_path)

    try:
        import DaVinciResolveScript as dvr_script  # type: ignore
    except ImportError as exc:
        logger.error(
            "No se pudo importar DaVinciResolveScript. Verifica que DaVinci "
            "Resolve Studio este instalado y que las variables de entorno "
            "RESOLVE_SCRIPT_API (%s) y RESOLVE_SCRIPT_LIB (%s) sean correctas.",
            script_api,
            script_lib,
        )
        raise SystemExit(1) from exc

    return dvr_script


def get_resolve():
    """Conecta con la instancia activa de DaVinci Resolve."""
    dvr_script = load_resolve_module()
    resolve = dvr_script.scriptapp("Resolve")
    if resolve is None:
        logger.error(
            "No se pudo conectar con DaVinci Resolve. Asegurate de que la "
            "aplicacion este abierta antes de ejecutar este script."
        )
        raise SystemExit(1)
    logger.info("Conectado a DaVinci Resolve correctamente.")
    return resolve


# --------------------------------------------------------------------------
# Modelo de datos del manifiesto
# --------------------------------------------------------------------------
@dataclass
class Scene:
    scene_id: str
    order: int
    file_name: str
    visual_prompt: str = ""
    audio_prompt: str = ""
    music_prompt: str = ""
    duration_seconds: Optional[float] = None
    narration_file: Optional[str] = None


@dataclass
class Manifest:
    scenes: list[Scene] = field(default_factory=list)
    music_file: Optional[str] = None


def load_manifest(manifest_path: Path) -> Manifest:
    """Lee y normaliza el manifest.json (lista de escenas o {"scenes": [...]})."""
    with open(manifest_path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    if isinstance(raw, list):
        scenes_raw, music_file = raw, None
    elif isinstance(raw, dict):
        scenes_raw = raw.get("scenes", [])
        music_file = raw.get("music_file")
    else:
        raise ValueError("Formato de manifest.json no reconocido.")

    scenes = [
        Scene(
            scene_id=str(s.get("scene_id")),
            order=int(s.get("order", i)),
            file_name=s["file_name"],
            visual_prompt=s.get("visual_prompt", ""),
            audio_prompt=s.get("audio_prompt", ""),
            music_prompt=s.get("music_prompt", ""),
            duration_seconds=s.get("duration_seconds"),
            narration_file=s.get("narration_file"),
        )
        for i, s in enumerate(scenes_raw)
    ]
    scenes.sort(key=lambda sc: sc.order)

    logger.info("Manifest cargado: %d escenas.", len(scenes))
    return Manifest(scenes=scenes, music_file=music_file)


# --------------------------------------------------------------------------
# Deteccion de orden a partir del nombre de archivo (fallback sin manifest)
# --------------------------------------------------------------------------
_LEADING_NUMBER_RE = re.compile(r"(\d+)")


def natural_order_key(filename: str) -> int:
    """Extrae el primer numero del nombre de archivo para poder ordenarlo
    (ej. '01_scene.mp4' -> 1). Si no hay numero, se manda al final."""
    match = _LEADING_NUMBER_RE.search(filename)
    return int(match.group(1)) if match else sys.maxsize


def discover_media_without_manifest(media_folder: Path) -> Manifest:
    """Construye un Manifest sintetico inspeccionando la carpeta de medios
    cuando no se provee --manifest_json. Los .mp3/.wav con 'music' en el
    nombre se tratan como musica de fondo; el resto de audios, como
    narracion asociada por orden a las escenas de video."""
    video_files = sorted(
        (p for p in media_folder.iterdir() if p.suffix.lower() in VIDEO_EXTENSIONS),
        key=lambda p: natural_order_key(p.name),
    )
    audio_files = sorted(
        (p for p in media_folder.iterdir() if p.suffix.lower() in AUDIO_EXTENSIONS),
        key=lambda p: natural_order_key(p.name),
    )

    music_files = [p for p in audio_files if "music" in p.name.lower()]
    narration_files = [p for p in audio_files if p not in music_files]

    scenes = []
    for i, video_path in enumerate(video_files):
        narration_name = narration_files[i].name if i < len(narration_files) else None
        scenes.append(
            Scene(
                scene_id=str(i + 1),
                order=i + 1,
                file_name=video_path.name,
                narration_file=narration_name,
            )
        )

    music_file = music_files[0].name if music_files else None
    logger.info(
        "Sin manifest: %d clips de video, %d narraciones, musica=%s.",
        len(scenes),
        len(narration_files),
        music_file,
    )
    return Manifest(scenes=scenes, music_file=music_file)


# --------------------------------------------------------------------------
# DaVinci Resolve: proyecto, media pool, timeline
# --------------------------------------------------------------------------
def open_or_create_project(resolve, project_name: str):
    project_manager = resolve.GetProjectManager()

    project = project_manager.LoadProject(project_name)
    if project is not None:
        logger.info("Proyecto existente '%s' abierto.", project_name)
        return project_manager, project

    project = project_manager.CreateProject(project_name)
    if project is None:
        logger.error("No se pudo abrir ni crear el proyecto '%s'.", project_name)
        raise SystemExit(1)

    logger.info("Proyecto nuevo '%s' creado.", project_name)
    return project_manager, project


def create_project_bin(media_pool, bin_name: str):
    root_folder = media_pool.GetRootFolder()

    for existing in root_folder.GetSubFolderList():
        if existing.GetName() == bin_name:
            media_pool.SetCurrentFolder(existing)
            logger.info("Bin existente '%s' reutilizado.", bin_name)
            return existing

    new_bin = media_pool.AddSubFolder(root_folder, bin_name)
    if new_bin is None:
        logger.error("No se pudo crear el bin '%s'.", bin_name)
        raise SystemExit(1)

    media_pool.SetCurrentFolder(new_bin)
    logger.info("Bin '%s' creado.", bin_name)
    return new_bin


def import_media_files(media_pool, media_folder: Path, file_names: list[str]) -> dict[str, Any]:
    """Importa los archivos indicados y devuelve un mapa file_name -> MediaPoolItem."""
    paths = []
    for name in file_names:
        full_path = media_folder / name
        if not full_path.exists():
            logger.warning("Archivo listado en el manifest no encontrado: %s", full_path)
            continue
        paths.append(str(full_path))

    if not paths:
        logger.error("No hay archivos validos para importar en %s.", media_folder)
        raise SystemExit(1)

    imported_items = media_pool.ImportMedia(paths)
    if not imported_items:
        logger.error("ImportMedia no devolvio ningun clip. Revisa formatos/codecs soportados.")
        raise SystemExit(1)

    if len(imported_items) < len(paths):
        logger.warning(
            "Se esperaban %d clips importados pero solo se importaron %d. "
            "Revisa el log de DaVinci Resolve para ver que archivos fallaron.",
            len(paths),
            len(imported_items),
        )

    item_by_name = {item.GetName(): item for item in imported_items}
    logger.info("Importados %d/%d archivos.", len(item_by_name), len(paths))
    return item_by_name


def create_timeline(media_pool, project, timeline_name: str):
    # Si ya existe una timeline con ese nombre, se reutiliza para permitir
    # reintentos idempotentes del pipeline.
    for i in range(project.GetTimelineCount()):
        existing = project.GetTimelineByIndex(i + 1)
        if existing and existing.GetName() == timeline_name:
            project.SetCurrentTimeline(existing)
            logger.warning("Timeline '%s' ya existia, se reutiliza.", timeline_name)
            return existing

    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    if timeline is None:
        logger.error("No se pudo crear la timeline '%s'.", timeline_name)
        raise SystemExit(1)

    logger.info("Timeline '%s' creada.", timeline_name)
    return timeline


def ensure_audio_tracks(timeline, required_tracks: int) -> None:
    """Garantiza que existan al menos `required_tracks` pistas de audio."""
    current = timeline.GetTrackCount("audio")
    for _ in range(current, required_tracks):
        if not timeline.AddTrack("audio"):
            logger.warning("No se pudo agregar una pista de audio adicional.")
            return
    logger.info("Pistas de audio disponibles: %d.", timeline.GetTrackCount("audio"))


def append_clips(media_pool, items: list, track_index: int, media_type: int, label: str) -> None:
    """Agrega una lista de MediaPoolItem a una pista especifica, en orden.

    media_type: 1 = video, 2 = audio (segun la API de AppendToTimeline).
    """
    if not items:
        return

    clip_infos = [
        {"mediaPoolItem": item, "trackIndex": track_index, "mediaType": media_type}
        for item in items
    ]
    result = media_pool.AppendToTimeline(clip_infos)
    if not result:
        logger.warning("No se pudieron insertar los clips de %s en la pista %d.", label, track_index)
    else:
        logger.info("Insertados %d clips de %s en la pista %d.", len(items), label, track_index)


# --------------------------------------------------------------------------
# Orquestacion principal
# --------------------------------------------------------------------------
def build_timeline_from_manifest(
    resolve,
    project_name: str,
    media_folder: Path,
    manifest: Manifest,
    timeline_name: str,
    bin_name: Optional[str],
) -> None:
    project_manager, project = open_or_create_project(resolve, project_name)
    media_pool = project.GetMediaPool()

    create_project_bin(media_pool, bin_name or project_name)

    video_names = [sc.file_name for sc in manifest.scenes]
    narration_names = [sc.narration_file for sc in manifest.scenes if sc.narration_file]
    all_names = list(dict.fromkeys(video_names + narration_names + ([manifest.music_file] if manifest.music_file else [])))

    item_by_name = import_media_files(media_pool, media_folder, all_names)

    timeline = create_timeline(media_pool, project, timeline_name)
    ensure_audio_tracks(timeline, required_tracks=2)

    video_items = [item_by_name[sc.file_name] for sc in manifest.scenes if sc.file_name in item_by_name]
    append_clips(media_pool, video_items, track_index=1, media_type=1, label="video")

    narration_items = [
        item_by_name[sc.narration_file]
        for sc in manifest.scenes
        if sc.narration_file and sc.narration_file in item_by_name
    ]
    append_clips(media_pool, narration_items, track_index=1, media_type=2, label="narracion")

    if manifest.music_file and manifest.music_file in item_by_name:
        append_clips(media_pool, [item_by_name[manifest.music_file]], track_index=2, media_type=2, label="musica")

    if not project_manager.SaveProject():
        logger.warning("SaveProject() devolvio False; verifica el estado del proyecto en Resolve.")
    else:
        logger.info("Proyecto guardado correctamente.")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatiza el armado de timelines en DaVinci Resolve a partir de un pipeline de IA."
    )
    parser.add_argument("--project_name", required=True, help="Nombre del proyecto de DaVinci Resolve.")
    parser.add_argument("--media_folder", required=True, help="Carpeta con los medios generados (video/audio).")
    parser.add_argument(
        "--manifest_json",
        required=False,
        default=None,
        help="Ruta al manifest.json con el orden y metadata de las escenas. "
        "Si se omite, el orden se infiere del prefijo numerico de los nombres de archivo.",
    )
    parser.add_argument(
        "--timeline_name",
        default="Auto_Edit_Timeline",
        help="Nombre de la timeline a crear (default: Auto_Edit_Timeline).",
    )
    parser.add_argument(
        "--bin_name",
        default=None,
        help="Nombre del bin del Media Pool (default: igual a --project_name).",
    )
    parser.add_argument("--verbose", action="store_true", help="Activa logging en modo debug.")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)

    media_folder = Path(args.media_folder).expanduser().resolve()
    if not media_folder.is_dir():
        logger.error("La carpeta de medios no existe: %s", media_folder)
        return 1

    try:
        if args.manifest_json:
            manifest_path = Path(args.manifest_json).expanduser().resolve()
            if not manifest_path.is_file():
                logger.error("El manifest indicado no existe: %s", manifest_path)
                return 1
            manifest = load_manifest(manifest_path)
        else:
            logger.warning("--manifest_json no provisto; se infiere el orden desde los nombres de archivo.")
            manifest = discover_media_without_manifest(media_folder)

        if not manifest.scenes:
            logger.error("El manifest no contiene escenas para procesar.")
            return 1

        resolve = get_resolve()
        build_timeline_from_manifest(
            resolve=resolve,
            project_name=args.project_name,
            media_folder=media_folder,
            manifest=manifest,
            timeline_name=args.timeline_name,
            bin_name=args.bin_name,
        )
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 1
    except Exception:
        logger.exception("Fallo inesperado durante la automatizacion.")
        return 1

    logger.info("Pipeline de edicion completado con exito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
