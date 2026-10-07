"""
Estructura de cada producto de video: genera los marcadores para DaVinci (.edl)
y las tablas de `plantillas-edicion.md` desde los MISMOS datos, para que el
documento y la línea de tiempo nunca digan cosas distintas.

Uso:  python3 generar_marcadores.py
"""
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(AQUI, "..", "plantillas-edicion.md")
FPS = 30

# (inicio s, fin s, color Resolve, nombre corto del marcador, qué se hace)
PRODUCTOS = {
    "aura": dict(
        nombre="Aura (ultra cámara lenta)", duracion=10, look="CosplayInc_Neon",
        tramos=[
            (0.0, 1.0, "Red", "HOOK", "Arranca al 150-200 % justo antes del gesto fuerte (giro de capa, pelo, arma). Frase del hook en pantalla."),
            (1.0, 2.0, "Yellow", "RAMPA ENTRADA", "Rampa 150 % → 20 % en el instante del gesto. Golpe de sonido (impacto) en el cambio."),
            (2.0, 7.5, "Blue", "CAMARA LENTA HEROE", "20-25 %, la cámara gira. Acercamiento lento del 100 al 110 %. Sin cortes: es el plano que vende."),
            (7.5, 8.5, "Green", "RAMPA SALIDA + FLASH", "Rampa 20 % → 150 % y flash blanco de 2-3 cuadros."),
            (8.5, 10.0, "Purple", "CIERRE", "Pose final congelada 0,5 s, logo y nombre del personaje."),
        ],
    ),
    "orbita": dict(
        nombre="Órbita (360° cámara lenta)", duracion=20, look="CosplayInc_Editorial",
        tramos=[
            (0.0, 1.5, "Red", "HOOK DETALLE", "Plano macro de un detalle (ojo, prop, bordado) + pregunta en pantalla."),
            (1.5, 3.0, "Yellow", "REVELACION", "Rampa del detalle al cuerpo entero; el giro empieza."),
            (3.0, 15.0, "Blue", "ORBITA + DETALLES", "Órbita al 25 %. En 3 golpes de la música, cortes a detalles (props, espalda, accesorios) con rampa 100 % → 30 %."),
            (15.0, 18.0, "Green", "GIRO COMPLETO", "Cierra la vuelta en la pose, acercamiento lento."),
            (18.0, 20.0, "Purple", "CIERRE", "Congelado + logo + nombre del personaje."),
        ],
    ),
    "pasarela": dict(
        nombre="Video Pasarela", duracion=30, look="CosplayInc_Pasarela",
        tramos=[
            (0.0, 1.5, "Red", "HOOK FINAL PRIMERO", "Abre con la pose final congelada y el texto del hook; rebobinado rápido (efecto rewind) hacia la entrada."),
            (1.5, 4.0, "Yellow", "ENTRADA", "Entrada a velocidad real, corte en el golpe de la música."),
            (4.0, 20.0, "Blue", "CAMINATA CON RAMPAS", "Alterna 100 % y 40 % en los pasos que caen en el ritmo. Movimiento de capa o arma al 25 %. Cambio de ángulo cada 3-4 s si hay segunda cámara."),
            (20.0, 26.0, "Green", "POSE FINAL", "Acercamiento lento, flashes, congelado con flash blanco y sonido de obturador."),
            (26.0, 30.0, "Purple", "CIERRE", "Logo, nombre del personaje y hashtags del evento."),
        ],
    ),
    "video-fx": dict(
        nombre="Video FX", duracion=30, look="CosplayInc_Neon",
        tramos=[
            (0.0, 1.5, "Red", "HOOK PODER", "Adelanto de 1 s del efecto más fuerte y 2 cuadros en negro."),
            (1.5, 8.0, "Yellow", "CARGA", "Caminata normal; brillo que crece en manos u ojos (máscara + glow)."),
            (8.0, 9.0, "Pink", "DISPARO FX", "Rampa 100 % → 15 %, flash, temblor de cámara y explosión del efecto (energía, fuego, rayos, según el personaje)."),
            (9.0, 22.0, "Blue", "CAMINATA CON AURA", "Partículas y aura siguiendo al personaje; rampas en los golpes."),
            (22.0, 27.0, "Green", "POSE FX", "Pose con el efecto al máximo, congelado y aberración cromática leve."),
            (27.0, 30.0, "Purple", "CIERRE", "Logo, nombre del personaje y hashtags."),
        ],
    ),
    "video-ia": dict(
        nombre="Video IA Inmersivo", duracion=30, look="CosplayInc_Editorial",
        tramos=[
            (0.0, 1.5, "Red", "HOOK ANTES/DESPUES", "0,7 s de la pasarela real y corte (barrido o destello) al mundo IA. Texto: «Del SOFA a su mundo»."),
            (1.5, 5.0, "Yellow", "REVELACION DEL MUNDO", "Plano abierto del fondo IA con el personaje integrado; movimiento de cámara lento (dolly)."),
            (5.0, 22.0, "Blue", "CAMINATA EN EL MUNDO", "Caminata integrada, parallax, partículas del ambiente (niebla, chispas, nieve). Rampas en los golpes."),
            (22.0, 27.0, "Green", "POSE HEROICA", "Acercamiento, luz del fondo que envuelve al personaje (light wrap), congelado."),
            (27.0, 30.0, "Purple", "CIERRE", "Logo, nombre del personaje y hashtags."),
        ],
    ),
    "grupal": dict(
        nombre="Grupal Video", duracion=45, look="CosplayInc_Pasarela",
        tramos=[
            (0.0, 2.0, "Red", "HOOK EQUIPO", "Pose grupal final congelada + «Conoce al equipo»."),
            (2.0, 5.0, "Yellow", "ENTRADA", "Entrada del grupo, corte en el golpe."),
            (5.0, 38.0, "Blue", "MOMENTO DE CADA UNO", "3-4 s por integrante, cada uno con su rampa y el nombre de su personaje. Con más de 9, 2-3 s cada uno."),
            (38.0, 42.0, "Green", "POSE GRUPAL", "Todos juntos, acercamiento lento y flash."),
            (42.0, 45.0, "Purple", "CIERRE", "Logo y hashtags del evento."),
        ],
    ),
}


def tc(segundos):
    """Código de tiempo desde 01:00:00:00, como arranca una línea de tiempo de DaVinci."""
    cuadros = round(segundos * FPS)
    s, f = divmod(cuadros, FPS)
    m, s = divmod(s, 60)
    return f"01:{m:02d}:{s:02d}:{f:02d}"


def edl(codigo, p):
    lineas = [f"TITLE: Plantilla {codigo}", "FCM: NON-DROP FRAME", ""]
    for i, (ini, fin, color, nombre, _) in enumerate(p["tramos"], start=1):
        lineas.append(f"{i:03d}  001      V     C        {tc(ini)} {tc(ini + 1 / FPS)} {tc(ini)} {tc(ini + 1 / FPS)}  ")
        lineas.append(f" |C:ResolveColor{color} |M:{nombre} |D:{round((fin - ini) * FPS)}")
        lineas.append("")
    return "\n".join(lineas)


# Los marcadores van sin tildes (por si la versión de DaVinci no las lee bien);
# en el documento se escriben como se dicen.
LEGIBLE = {"camara": "cámara", "revelacion": "revelación", "orbita": "órbita", "despues": "después", "fx": "FX", "heroe": "héroe"}


def legible(nombre):
    palabras = nombre.lower().replace("/", " / ").split()
    texto = " ".join(LEGIBLE.get(w, w) for w in palabras).replace(" / ", "/")
    return texto[0].upper() + texto[1:]


def tabla(p):
    filas = ["| Tiempo | Tramo | Qué se hace |", "|---|---|---|"]
    for ini, fin, _, nombre, que in p["tramos"]:
        filas.append(f"| {ini:g}–{fin:g} s | **{legible(nombre)}** | {que} |")
    return "\n".join(filas)


for codigo, p in PRODUCTOS.items():
    with open(os.path.join(AQUI, f"{codigo}.edl"), "w") as f:
        f.write(edl(codigo, p))
    print("✓", codigo)

# Reemplaza en el documento cada bloque <!-- tabla:codigo --> … <!-- /tabla -->.
if os.path.exists(DOC):
    texto = open(DOC).read()
    for codigo, p in PRODUCTOS.items():
        texto = re.sub(
            rf"<!-- tabla:{codigo} -->.*?<!-- /tabla -->",
            f"<!-- tabla:{codigo} -->\n{tabla(p)}\n<!-- /tabla -->",
            texto,
            flags=re.S,
        )
    open(DOC, "w").write(texto)
    print("✓ tablas en plantillas-edicion.md")
