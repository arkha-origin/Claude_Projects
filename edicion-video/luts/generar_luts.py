"""
Genera los LUT creativos de Cosplay Inc (.cube, 33 puntos, Rec.709 de entrada y salida).

Son LUT de "look", no de conversión: se aplican DESPUÉS de normalizar el material
(en DaVinci, en un nodo posterior a la corrección primaria / CST; en CapCut, sobre el
clip ya ajustado). La piel se protege: el tinte y la saturación casi no la tocan.

Uso:  python3 generar_luts.py   (escribe los .cube junto a este archivo)
"""
import colorsys
import os

N = 33
AQUI = os.path.dirname(os.path.abspath(__file__))

LOOKS = {
    # Retrato limpio y premium: contraste suave, sombras apenas frías, altas cálidas.
    "CosplayInc_Editorial": dict(curva=0.22, levantar=0.015, gamma=1.0,
                                 sombras=(-0.004, 0.006, 0.030), altas=(0.020, 0.008, -0.010), sat=1.08),
    # La marca: rojo y azul de neón. Más contraste, sombras azul-magenta, altas rojizas.
    "CosplayInc_Neon": dict(curva=0.34, levantar=0.02, gamma=1.0,
                            sombras=(0.010, -0.010, 0.050), altas=(0.030, -0.004, 0.006), sat=1.16),
    # Pasarela: más luminoso y cálido, para la alfombra morada y los flashes.
    "CosplayInc_Pasarela": dict(curva=0.18, levantar=0.01, gamma=0.94,
                                sombras=(0.014, 0.000, 0.024), altas=(0.024, 0.012, -0.012), sat=1.06),
}


def recortar(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def peso_piel(r, g, b):
    """1 en tonos de piel (de clara a oscura), 0 lejos de ellos."""
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if not (r > g > b) or v < 0.12:
        return 0.0
    tono = 1.0 - min(abs(h - 0.07) / 0.06, 1.0)  # matiz ~25°
    sat = 1.0 if 0.12 <= s <= 0.65 else 0.0
    return tono * sat


def aplicar(look, r, g, b):
    piel = peso_piel(r, g, b)
    # Gamma (luminosidad general) y curva S.
    canales = []
    for x in (r, g, b):
        x = x ** look["gamma"]
        s = x * x * (3 - 2 * x)
        x = (1 - look["curva"]) * x + look["curva"] * s
        x = look["levantar"] + x * (1 - look["levantar"])
        canales.append(x)
    r, g, b = canales
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # Virado: sombras y altas. La piel recibe solo el 30 %.
    ws, wh = (1 - y) ** 2, y ** 2
    f = 1 - 0.7 * piel
    r += f * (ws * look["sombras"][0] + wh * look["altas"][0])
    g += f * (ws * look["sombras"][1] + wh * look["altas"][1])
    b += f * (ws * look["sombras"][2] + wh * look["altas"][2])
    # Saturación, con la piel protegida.
    sat = 1 + (look["sat"] - 1) * (1 - 0.8 * piel)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return tuple(recortar(y + (c - y) * sat) for c in (r, g, b))


for nombre, look in LOOKS.items():
    lineas = [f'TITLE "{nombre}"', f"LUT_3D_SIZE {N}", "DOMAIN_MIN 0.0 0.0 0.0", "DOMAIN_MAX 1.0 1.0 1.0"]
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):  # el rojo cambia más rápido, como pide el formato .cube
                r, g, b = aplicar(look, ri / (N - 1), gi / (N - 1), bi / (N - 1))
                lineas.append(f"{r:.6f} {g:.6f} {b:.6f}")
    with open(os.path.join(AQUI, f"{nombre}.cube"), "w") as f:
        f.write("\n".join(lineas) + "\n")
    print("✓", nombre)
