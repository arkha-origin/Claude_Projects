"""
Cataloga una carpeta de efectos (VFX) para que el asistente y el editor sepan cómo
usar cada uno: modo de fusión, dónde va, cómo se sigue y cuánto dura.

Lee cada archivo con ffprobe/ffmpeg (no lo modifica) y detecta:
  - si tiene canal alfa (transparencia propia),
  - el color del fondo (negro, blanco, verde de croma) mirando un cuadro del medio,
  - resolución, cuadros por segundo y duración.
Con eso propone el modo de fusión, y por el nombre del archivo adivina la categoría
y el anclaje (manos, suelo, cuerpo…). Lo que adivina se marca para que el editor lo
confirme en el CSV.

Uso:  python3 catalogar_vfx.py /ruta/a/la/libreria-vfx
Escribe catalogo.json y catalogo.csv en esa carpeta. Volver a correrlo conserva lo
que el editor ya corrigió en el CSV (columnas categoria, anclaje, modo, notas).
"""
import csv
import json
import os
import subprocess
import sys

EXTENSIONES = {".mov", ".mp4", ".webm", ".mkv", ".avi", ".mxf", ".png", ".gif"}

# Palabra en el nombre del archivo → (categoría, anclaje, modo si el fondo es negro)
PALABRAS = [
    (("rayo", "lightning", "electric", "electr", "thunder"), "rayo", "manos u ojos", "Agregar (Add)"),
    (("fuego", "fire", "flame", "llama", "burn"), "fuego", "manos o suelo", "Agregar (Add)"),
    (("humo", "smoke", "niebla", "fog", "mist"), "humo/niebla", "suelo", "Pantalla (Screen)"),
    (("chispa", "spark", "ember", "brasa"), "chispas", "manos o arma", "Agregar (Add)"),
    (("energia", "energy", "aura", "power", "poder", "ki"), "aura/energía", "cuerpo completo", "Agregar (Add)"),
    (("magia", "magic", "runa", "rune", "spell", "hechizo", "portal"), "magia", "manos o suelo", "Pantalla (Screen)"),
    (("polvo", "dust", "debris", "escombro"), "polvo/escombros", "suelo", "Pantalla (Screen)"),
    (("explosion", "explosión", "blast", "impact", "impacto", "shockwave"), "impacto/explosión", "punto de impacto", "Agregar (Add)"),
    (("flare", "destello", "lens", "glow", "brillo"), "destello", "fuente de luz", "Pantalla (Screen)"),
    (("hielo", "ice", "frost", "nieve", "snow"), "hielo/nieve", "pantalla completa", "Pantalla (Screen)"),
    (("agua", "water", "splash", "lluvia", "rain"), "agua/lluvia", "pantalla completa", "Pantalla (Screen)"),
    (("particula", "particle", "bokeh", "glitter", "estrella", "star"), "partículas", "pantalla completa", "Pantalla (Screen)"),
    (("slash", "corte", "sword", "espada", "trail", "estela"), "estela de arma", "arma", "Agregar (Add)"),
]

# Cómo se sigue cada anclaje (DaVinci / CapCut).
SEGUIMIENTO = {
    "manos u ojos": "Tracker de punto en Fusion (mano u ojo) / CapCut: Seguimiento de movimiento sobre la mano",
    "manos o suelo": "Tracker de punto (mano) o Planar Tracker (suelo) / CapCut: Seguimiento de movimiento",
    "manos o arma": "Tracker de punto en la mano o la punta del arma / CapCut: Seguimiento de movimiento",
    "cuerpo completo": "Magic Mask del cuerpo + el efecto detrás o alrededor / CapCut: Efectos de cuerpo o Quitar fondo",
    "suelo": "Planar Tracker sobre el piso de la pasarela / CapCut: fijo abajo (la cámara de pasarela casi no se mueve)",
    "punto de impacto": "Fijo en el cuadro del impacto (sin seguimiento), 6-12 cuadros",
    "fuente de luz": "Tracker de punto sobre la luz o el prop brillante",
    "pantalla completa": "Sin seguimiento: capa completa encima, opacidad 40-80 %",
    "arma": "Tracker de punto en la punta del arma; si gira, dos puntos (escala y rotación)",
}


def correr(args):
    return subprocess.run(args, capture_output=True, check=False)


def sondear(ruta):
    r = correr(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                "stream=width,height,pix_fmt,r_frame_rate:format=duration", "-of", "json", ruta])
    datos = json.loads(r.stdout or b"{}")
    s = (datos.get("streams") or [{}])[0]
    num, _, den = (s.get("r_frame_rate") or "0/1").partition("/")
    fps = round(float(num) / float(den or 1), 2) if float(den or 1) else 0
    dur = float((datos.get("format") or {}).get("duration") or 0)
    return s.get("width"), s.get("height"), s.get("pix_fmt") or "", fps, dur


def fondo(ruta, dur):
    """Color medio del borde de un cuadro del medio: negro, blanco, verde u otro."""
    momento = f"{dur / 2:.2f}" if dur > 0 else "0"
    r = correr(["ffmpeg", "-v", "error", "-ss", momento, "-i", ruta, "-frames:v", "1",
                "-vf", "scale=32:18", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    px = r.stdout
    if len(px) < 32 * 18 * 3:
        return "desconocido"
    borde = []
    for y in range(18):
        for x in range(32):
            if x in (0, 1, 30, 31) or y in (0, 1, 16, 17):
                i = (y * 32 + x) * 3
                borde.append(px[i:i + 3])
    rr = sum(p[0] for p in borde) / len(borde) / 255
    gg = sum(p[1] for p in borde) / len(borde) / 255
    bb = sum(p[2] for p in borde) / len(borde) / 255
    if gg > rr + 0.2 and gg > bb + 0.2:
        return "verde (croma)"
    if max(rr, gg, bb) < 0.1:
        return "negro"
    if min(rr, gg, bb) > 0.9:
        return "blanco"
    return "otro"


def adivinar(nombre):
    n = nombre.lower()
    for palabras, categoria, anclaje, modo in PALABRAS:
        if any(p in n for p in palabras):
            return categoria, anclaje, modo
    return "sin clasificar", "pantalla completa", "Pantalla (Screen)"


def catalogar(carpeta):
    previo = {}
    ruta_csv = os.path.join(carpeta, "catalogo.csv")
    if os.path.exists(ruta_csv):
        with open(ruta_csv, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                previo[fila["archivo"]] = fila

    efectos = []
    for raiz, _, archivos in os.walk(carpeta):
        for a in sorted(archivos):
            if os.path.splitext(a)[1].lower() not in EXTENSIONES:
                continue
            ruta = os.path.join(raiz, a)
            rel = os.path.relpath(ruta, carpeta)
            ancho, alto, pix, fps, dur = sondear(ruta)
            if not ancho:
                continue
            alfa = any(k in pix for k in ("yuva", "rgba", "argb", "bgra", "abgr", "ya8", "gbrap"))
            fondo_ = "transparente (alfa)" if alfa else fondo(ruta, dur)
            categoria, anclaje, modo_negro = adivinar(a)
            modo = {
                "transparente (alfa)": "Normal",
                "negro": modo_negro,
                "blanco": "Multiplicar (Multiply)",
                "verde (croma)": "Normal + Delta Keyer / Quitar fondo croma",
            }.get(fondo_, "Revisar a mano")
            e = {
                "archivo": rel, "ancho": ancho, "alto": alto, "fps": fps, "duracion_s": round(dur, 2),
                "fondo": fondo_, "modo": modo, "categoria": categoria, "anclaje": anclaje,
                "seguimiento": SEGUIMIENTO.get(anclaje, ""), "vertical": bool(alto and ancho and alto > ancho),
                "confirmado": "no", "notas": "",
            }
            # Lo que el editor ya corrigió manda sobre lo adivinado.
            for campo in ("categoria", "anclaje", "modo", "notas", "confirmado"):
                if rel in previo and previo[rel].get(campo):
                    e[campo] = previo[rel][campo]
            e["seguimiento"] = SEGUIMIENTO.get(e["anclaje"], e["seguimiento"])
            efectos.append(e)

    with open(os.path.join(carpeta, "catalogo.json"), "w", encoding="utf-8") as f:
        json.dump(efectos, f, ensure_ascii=False, indent=2)
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        campos = list(efectos[0].keys()) if efectos else ["archivo"]
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(efectos)
    return efectos


if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("Uso: python3 catalogar_vfx.py /ruta/a/la/libreria-vfx")
    lista = catalogar(sys.argv[1])
    print(f"✓ {len(lista)} efectos catalogados → catalogo.json y catalogo.csv")
    for e in lista:
        print(f"  {e['archivo']}: {e['fondo']} → {e['modo']} · {e['categoria']} · {e['anclaje']}")
