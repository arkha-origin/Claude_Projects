import json, re, sys, unicodedata, importlib.util, glob, html
DESTINO = sys.argv[1]  # .../public/evaluacion

def slug(t):
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:90]

def preg(x):
    q, ok, malas, fb = x
    d = {"q": q, "op": [ok] + malas, "ok": 0}
    if fb: d["fb"] = fb
    return d

temas = []
for f in sorted(glob.glob("/tmp/gen/c_*.py")):
    spec = importlib.util.spec_from_file_location("m", f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    temas += m.TEMAS

PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title><link rel="stylesheet" href="../_motor/motor.css"></head>
<body><div class="marco" id="juego"></div>
<script>window.JUEGO = {datos};</script>
<script src="../_motor/motor.js"></script></body></html>
"""
nuevos = []
for t in temas:
    for clave in ("explicacion", "practica", "evaluacion"):
        assert t[clave], (t["nombre"], clave)
    datos = {
        "titulo": t["nombre"], "area": t.get("areaVisible", t["area"]), "grado": t["grado"],
        "icono": t["icono"], "color": t["color"],
        "explicacion": [{"t": a, "p": b, **({"e": c} if c else {})} for a, b, c in t["explicacion"]],
        "demostracion": {"intro": t["demo"][0], "pasos": [{"t": a, "p": b} for a, b in t["demo"][1]]},
        "practica": [preg(x) for x in t["practica"]],
        "evaluacion": [preg(x) for x in t["evaluacion"]],
    }
    nombre_archivo = slug(t["tema"] + "-" + t["nombre"]) + ".html"
    ruta = f"juegos/{t['carpeta']}/{nombre_archivo}"
    with open(f"{DESTINO}/{ruta}", "w") as fh:
        fh.write(PLANTILLA.format(titulo=html.escape(t["nombre"]), datos=json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")))
    nuevos.append({"area": t["area"], "tema": t["tema"], "nombre": t["nombre"], "grado": t["grado"], "href": ruta})

# Al índice: reemplaza las entradas generadas antes y agrega las nuevas.
p = f"{DESTINO}/index.html"
s = open(p).read()
i = s.index("const DATA = ") + len("const DATA = ")
j = s.index("];", i) + 1
data = json.loads(s[i:j])
hrefs = {n["href"] for n in nuevos}
data = [d for d in data if d["href"] not in hrefs] + nuevos
s = s[:i] + json.dumps(data, ensure_ascii=False) + s[j:]
open(p, "w").write(s)
print(len(nuevos), "juegos ·", len(data), "en el índice")
