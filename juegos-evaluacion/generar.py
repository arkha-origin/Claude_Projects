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

# ── Página «Nuevos · por aplicar»: los juegos generados, en la secuencia de la lista.
ORDEN = [("3°", "mat"), ("3°", "len"), ("3°", "art"), ("3°", "pileo"), ("3°", "eti"), ("3°", "tec"),
         ("4°", "est"), ("4°", "tec"), ("5°", "tec"), ("5°", "eti")]
NOMBRE_GRUPO = {"mat": "Matemáticas", "len": "Lengua Castellana", "art": "Artes", "pileo": "PILEO",
                "eti": "Ética", "tec": "Tecnología e Informática", "est": "Estadística"}
def grupo(n):
    if n["tema"] == "PILEO": return "pileo"
    if n["tema"] == "Estadística": return "est"
    return {"Matemáticas": "mat", "Lengua Castellana": "len", "Artes": "art",
            "Ética y Religión": "eti", "Tecnología e Informática": "tec"}[n["area"]]
secuencia = []
for g, a in ORDEN:
    for n in nuevos:
        if n["grado"] == g and grupo(n) == a:
            secuencia.append({**n, "grupo": f"{g} · {NOMBRE_GRUPO[a]}"})
assert len(secuencia) == len(nuevos)
pagina = open("/tmp/gen/nuevos-plantilla.html").read().replace("__DATOS__", json.dumps(secuencia, ensure_ascii=False))
open(f"{DESTINO}/nuevos.html", "w").write(pagina)

# Pestaña en el índice (una sola vez).
s = open(p).read()
if 'href="nuevos.html"' not in s:
    s = s.replace('<input id="q"', '<a href="nuevos.html" class="pestana-nuevos" style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 14px;padding:14px 18px;border-radius:14px;background:#1f2a5c;color:#fff;font-weight:700;text-decoration:none">✨ ' + str(len(nuevos)) + ' juegos nuevos · por aplicar <span style="background:#ffd43b;color:#1f2a5c;border-radius:99px;padding:4px 12px">Ver la secuencia →</span></a><input id="q"', 1)
    open(p, "w").write(s)
print("nuevos.html con", len(secuencia))

# ── Rincón de inclusión: la lista de juegos para el modo enfoque y el acceso desde el índice.
open(f"{DESTINO}/inclusion/juegos-lista.js", "w").write("var JUEGOS = " + json.dumps(secuencia, ensure_ascii=False) + ";\n")
s = open(p).read()
if 'href="inclusion/index.html"' not in s:
    s = s.replace('<input id="q"', '<a href="inclusion/index.html" style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 14px;padding:14px 18px;border-radius:14px;background:#fff4d6;color:#5b3a00;font-weight:700;text-decoration:none;border:2px solid #ffd43b">🤝 Rincón de inclusión · juegos y apoyos por perfil <span style="background:#5b4bdb;color:#fff;border-radius:99px;padding:4px 12px">Abrir →</span></a><input id="q"', 1)
    open(p, "w").write(s)
