import urllib.parse, random
random.seed(7)
B="https://d8j0ntlcm91z4.cloudfront.net/user_3GpmMSlhlwuiXiNZMT5QXNIqOkj/"
WA="https://wa.me/573154575440?text="
def wa(t): return WA+urllib.parse.quote(t)

TEMAS={
 "navidad":dict(
  ruta="/navidad", titulo="Christmas", em="Tales", etiqueta="🎄 Sesión especial de Navidad 🎄",
  nombreEvento="Christmas Tales",
  lema="Tu personaje dentro de un cuento de Navidad. Un set con nieve, luces cálidas y magia, y fotos y video para regalar y guardar toda la vida.",
  cuando="📅 Diciembre 2026 · fecha por anunciar", fuente="Mountains+of+Christmas:wght@700", familia='"Mountains of Christmas"',
  c1="#e63946", c2="#2a9d8f", c3="#ffd166", fondo="#06120f", tarjeta="#0d1f1a", borde="#1f3a33", tinta="#f4fff9", tenue="#a9c9bd",
  set=B+"hf_20261015_231930_f6feab55-7abd-4aa1-baef-e81e98a99ee7.png",
  paquetes=[("Postal","La Reina de las Nieves",B+"hf_20261015_231931_e9853004-f064-446a-8d8e-6be51c4cabbe.png"),
            ("Cuento","El Duende",B+"hf_20261015_231930_4ec26f98-d6cd-47aa-9788-07dc6bbe7bb0.png"),
            ("Mágica","El Noble Victoriano",B+"hf_20261015_231930_9dbc152d-e94a-4341-80c1-6c679ede6da6.png")],
  decor="navidad", vela="✨", pie="🎄 🎁 ⭐ 🔔 ❄️",
  pasos=[("🎟️","Aparta tu cupo","Escríbenos por WhatsApp y te avisamos primero cuando abran los turnos."),("🎄","Entras al set navideño","Árbol, nieve, regalos y luces cálidas. Te guiamos en cada pose."),("🎬","Foto y video en cámara lenta","Tu traje entre la nieve, como en una película de Navidad."),("🎁","Recibe tu galería","Miniaturas en días; editadas listas para regalar y publicar.")],
  h2a="Cómo es la", h2b="Elige tu", h2c="historia de Navidad", privada="🦌 Sesión privada · hasta 4 personas",
  privadaTxt="Una hora con el set solo para ustedes: la foto de familia, de pareja o del grupo de cosplay que se vuelve tarjeta de Navidad.",
  faqTitulo=("Preguntas","bajo el árbol"),
  faq=[("¿Tengo que hacer cosplay?","No. Vale cosplay, un look navideño, un disfraz o tu mejor pinta de fiesta."),("¿Pueden ir menores de edad?","Sí, con un acudiente presente que autoriza la sesión al reservar."),("¿Sirve para la tarjeta de Navidad de la familia?","Sí: la sesión privada es para eso. Hasta 4 personas en el mismo set."),("¿Cuándo es?","En diciembre de 2026 en Bogotá. Aparta tu cupo y te avisamos la fecha y los turnos antes que a nadie.")],
 ),
 "ano-nuevo":dict(
  ruta="/ano-nuevo", titulo="New Year", em="Tales", etiqueta="🎆 Sesión especial de Año Nuevo 🎆",
  nombreEvento="New Year Tales",
  lema="Cierra el año con tu mejor look. Un set de gala con confeti, brillos y fuegos artificiales, y fotos y video para empezar el año en grande.",
  cuando="📅 Diciembre 2026 · fecha por anunciar", fuente="Cinzel+Decorative:wght@700", familia='"Cinzel Decorative"',
  c1="#f5c542", c2="#b388ff", c3="#ffffff", fondo="#07060d", tarjeta="#121021", borde="#2b2645", tinta="#fffaf0", tenue="#c8bfdc",
  set=B+"hf_20261015_231931_0320c274-435a-42fe-9523-e5a8e475d32c.png",
  paquetes=[("Brindis","La Gala Dorada",B+"hf_20261015_231955_d895f2f4-621a-403b-8276-3c4ea02fbe42.png"),
            ("Gala","El Carnaval",B+"hf_20261015_231955_e24f20f7-c5d2-4e70-a32f-b87f8925efac.png"),
            ("Medianoche","La Hechicera de las Estrellas",B+"hf_20261015_231931_1a96a7ba-9a49-4e21-97d3-84f30cd0a7c8.png")],
  decor="anio", vela="✨", pie="🎆 🥂 ⭐ 🕛 🎊",
  pasos=[("🎟️","Aparta tu cupo","Escríbenos por WhatsApp y te avisamos primero cuando abran los turnos."),("🎊","Entras al set de gala","Confeti, globos dorados, brillos y luces. Te guiamos en cada pose."),("🎬","Foto y video en cámara lenta","El confeti cayendo sobre tu traje, como en la noche de fin de año."),("🎆","Recibe tu galería","Miniaturas en días; editadas listas para tu primera publicación del año.")],
  h2a="Cómo es la", h2b="Elige tu", h2c="noche de gala", privada="🕛 Sesión privada · hasta 4 personas",
  privadaTxt="Una hora con el set solo para ustedes: parejas, amigos, familias o grupos de cosplay que quieren su foto de fin de año.",
  faqTitulo=("Preguntas","antes de medianoche"),
  faq=[("¿Tengo que hacer cosplay?","No. Vale cosplay, traje de gala, disfraz o tu mejor look de fin de año."),("¿Pueden ir menores de edad?","Sí, con un acudiente presente que autoriza la sesión al reservar."),("¿Hay brindis de verdad?","Los props son de utilería; no se sirve alcohol en el set."),("¿Cuándo es?","En diciembre de 2026 en Bogotá. Aparta tu cupo y te avisamos la fecha y los turnos antes que a nadie.")],
 ),
}

PRECIOS=[("$230.000","$260.000",["3 fotos editadas","1 video Aura en cámara lenta","Turno de 30 min","Galería privada"]),
         ("$450.000","$520.000",["6 fotos editadas","1 video Aura en cámara lenta","1 «Tale»: micro-película de 15 s para Reels y TikTok","Turno de 30 min","Galería privada"]),
         ("$690.000","$840.000",["10 fotos editadas","3 videos (Aura, Tale y uno más)","Entrega Rápida: primero en la fila de edición","Galería privada"])]

def decor(t):
    if t["decor"]=="navidad":
        copos="".join(f'<span class="copo" style="left:{random.randint(0,100)}%;animation-duration:{random.randint(7,16)}s;animation-delay:-{random.randint(0,16)}s;font-size:{random.randint(10,22)}px;opacity:{random.uniform(.4,.95):.2f}">❄</span>' for _ in range(46))
        luces="".join(f'<i style="background:{["#e63946","#ffd166","#2a9d8f","#8ecae6"][i%4]};animation-delay:{(i%4)*0.35:.2f}s"></i>' for i in range(34))
        flota="".join(f'<span class="flota" style="top:{top}%;{lado}:{x}%;animation-delay:{d}s">{e}</span>' for e,top,lado,x,d in [("🎁",32,"left",4,0),("⭐",58,"right",4,1.5),("🔔",78,"left",3,3),("🎄",44,"right",2,2.2)])
        return f'''<div class="capa" aria-hidden="true"><div class="luces">{luces}</div>{copos}{flota}<span class="trineo">🛷🦌🦌</span><div class="niebla"></div></div>'''
    conf="".join(f'<span class="confeti" style="left:{random.randint(0,100)}%;background:{random.choice(["#f5c542","#b388ff","#ffffff","#ff6fb5","#7ee0ff"])};animation-duration:{random.randint(6,13)}s;animation-delay:-{random.randint(0,13)}s;transform:rotate({random.randint(0,180)}deg)"></span>' for _ in range(60))
    fuegos="".join(f'<span class="fuego" style="left:{x}%;top:{y}%;--c:{c};animation-delay:{d}s"></span>' for x,y,c,d in [(12,18,"#f5c542",0),(80,14,"#b388ff",1.3),(55,26,"#ff6fb5",2.6),(28,40,"#7ee0ff",3.9),(88,46,"#f5c542",5.2)])
    burb="".join(f'<span class="burbuja" style="left:{random.randint(0,100)}%;animation-duration:{random.randint(8,15)}s;animation-delay:-{random.randint(0,15)}s;width:{(w:=random.randint(4,12))}px;height:{w}px"></span>' for _ in range(24))
    return f'<div class="capa" aria-hidden="true">{fuegos}{conf}{burb}<span class="reloj">🕛</span></div>'

def css_decor(t):
    if t["decor"]=="navidad":
        return '''.luces{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;padding:0 8px;height:26px;border-top:2px solid #2f4d44}
.luces i{display:block;width:10px;height:15px;border-radius:50% 50% 45% 45%;margin-top:4px;box-shadow:0 0 12px currentColor;animation:titilar 1.4s ease-in-out infinite}
@keyframes titilar{50%{opacity:.25;filter:brightness(.6)}}
.copo{position:absolute;top:-30px;color:#fff;animation:caer linear infinite;text-shadow:0 0 8px #fff}
@keyframes caer{to{transform:translateY(110vh) translateX(40px) rotate(360deg)}}
.flota{position:absolute;font-size:38px;animation:flotar 6s ease-in-out infinite;filter:drop-shadow(0 0 14px #ffd16688)}
.trineo{position:absolute;top:16%;font-size:40px;white-space:nowrap;animation:trineo 22s linear infinite;filter:drop-shadow(0 0 10px #ffd166)}
@keyframes trineo{0%{transform:translateX(110vw) translateY(0)}50%{transform:translateX(45vw) translateY(-30px)}100%{transform:translateX(-40vw) translateY(10px)}}'''
    return '''.confeti{position:absolute;top:-20px;width:8px;height:14px;border-radius:2px;animation:confeti linear infinite}
@keyframes confeti{to{transform:translateY(110vh) rotate(720deg) translateX(60px)}}
.fuego{position:absolute;width:6px;height:6px;border-radius:50%;opacity:0;animation:estallar 6.5s ease-out infinite;box-shadow:0 0 0 0 var(--c)}
@keyframes estallar{0%{opacity:0;transform:scale(.2);box-shadow:0 0 0 0 var(--c)}6%{opacity:1}22%{opacity:1;transform:scale(1);box-shadow:0 -60px 0 -2px var(--c),42px -42px 0 -2px var(--c),60px 0 0 -2px var(--c),42px 42px 0 -2px var(--c),0 60px 0 -2px var(--c),-42px 42px 0 -2px var(--c),-60px 0 0 -2px var(--c),-42px -42px 0 -2px var(--c),0 -30px 0 -1px #fff,30px 0 0 -1px #fff,0 30px 0 -1px #fff,-30px 0 0 -1px #fff}35%,100%{opacity:0;transform:scale(1.3)}}
.burbuja{position:absolute;bottom:-20px;border-radius:50%;border:1px solid #fff8;background:#ffffff18;animation:subir linear infinite}
@keyframes subir{to{transform:translateY(-110vh) translateX(-30px)}}
.reloj{position:absolute;top:30%;right:4%;font-size:46px;animation:flotar 6s ease-in-out infinite;filter:drop-shadow(0 0 16px #f5c542)}'''

def pagina(t):
    tarjetas=""
    for i,((nombre,personaje,img),(precio,antes,items)) in enumerate(zip(t["paquetes"],PRECIOS)):
        dest=i==1
        boton=f'<a class="boton{"" if dest else " sec"}" href="{wa("Hola, quiero apartar la experiencia "+nombre+" de "+t["nombreEvento"]+" ✨")}" target="_blank" rel="noopener">Apartar {nombre}</a>'
        lis="".join(f"<li>{x}</li>" for x in items)
        tarjetas+=f'''<div class="paquete{" destacado" if dest else ""}">{'<span class="insignia">⭐ LA MÁS ELEGIDA</span>' if dest else ""}<div class="retrato" style="background-image:url('{img}'),linear-gradient(160deg,{t["c2"]}55,var(--tarjeta))"><span class="personaje">{personaje}</span></div><div class="cuerpo"><h3>{nombre}</h3><div class="precio">{precio}</div><div class="antes">{antes} por separado</div><ul>{lis}</ul>{boton}</div></div>'''
    galeria="".join(f'<div class="foto" style="background-image:url(\'{img}\'),linear-gradient(160deg,{t["c2"]}55,var(--tarjeta))"><span>{p}</span></div>' for _,p,img in t["paquetes"])
    galeria+=f'<div class="foto" style="background-image:url(\'{t["set"]}\');background-position:30% center"><span>El set</span></div>'
    pasos="".join(f'<div class="paso"><b>{e}</b><strong>{a}</strong><p class="sub" style="margin:6px 0 0">{b}</p></div>' for e,a,b in t["pasos"])
    vives="".join(f'<div class="paso"><b>{e}</b><strong>{a}</strong><p class="sub" style="margin:6px 0 0">{b}</p></div>' for e,a,b in [("🎭","Set tematizado","Escenografía, luz y ambiente pensados para la temporada."),("📸","Dirección de poses","Te guiamos en cada turno para sacar lo mejor de tu personaje."),("✨","Tus fotos editadas","En tu galería privada, listas para descargar."),("🎬","Tu video","En cámara lenta o tu «Tale» para Reels y TikTok."),("📲","Kit para redes","Formatos, carrusel y el texto para publicar."),("🎟️","Cupos limitados","Pocas personas por turno, para que sea tuya.")])
    faq="".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{r}</p></details>' for i,(q,r) in enumerate(t["faq"]))
    aparta=wa(f"Hola, quiero apartar mi cupo en {t['nombreEvento']} (diciembre) ✨. Avísenme la fecha y los turnos.")
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["nombreEvento"]} · Sesión especial · Cosplay Inc</title>
<meta name="description" content="{t["lema"]} Experiencias desde $230.000 en Bogotá. Cupos limitados.">
<meta property="og:title" content="{t["nombreEvento"]} · Cosplay Inc"><meta property="og:description" content="{t["lema"]}">
<meta property="og:image" content="{t["set"]}"><meta property="og:url" content="https://cosplay-inc.com{t["ruta"]}"><meta name="theme-color" content="{t["fondo"]}">
<link href="https://fonts.googleapis.com/css2?family={t["fuente"]}&display=swap" rel="stylesheet">
<style>
:root{{--fondo:{t["fondo"]};--tinta:{t["tinta"]};--tenue:{t["tenue"]};--c1:{t["c1"]};--c2:{t["c2"]};--c3:{t["c3"]};--borde:{t["borde"]};--tarjeta:{t["tarjeta"]}}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{background:var(--fondo);color:var(--tinta);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;line-height:1.5;overflow-x:hidden}}a{{color:inherit;text-decoration:none}}
.capa{{position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden}}
.niebla{{position:absolute;left:-30%;width:160%;height:30vh;bottom:-8vh;background:radial-gradient(ellipse at 40% 60%,#ffffff22,transparent 60%);filter:blur(28px);animation:niebla 18s ease-in-out infinite alternate}}
@keyframes niebla{{from{{transform:translateX(-8%)}}to{{transform:translateX(8%)}}}}
@keyframes flotar{{0%,100%{{transform:translate(0,0) rotate(-6deg)}}50%{{transform:translate(14px,-22px) rotate(6deg)}}}}
{css_decor(t)}
header{{position:relative;z-index:10;display:flex;justify-content:space-between;align-items:center;padding:26px 6vw 18px}}
.logo{{font-weight:800;letter-spacing:.08em;font-size:14px}}.logo span{{color:var(--c1)}}
.boton{{display:inline-block;background:linear-gradient(135deg,var(--c1),var(--c2));color:#fff;font-weight:800;padding:14px 26px;border-radius:999px;box-shadow:0 0 30px color-mix(in srgb,var(--c1) 50%,transparent);transition:transform .2s;animation:latido 2.6s ease-in-out infinite}}
.boton:hover{{transform:scale(1.06)}}@keyframes latido{{50%{{box-shadow:0 0 48px color-mix(in srgb,var(--c2) 70%,transparent)}}}}
.boton.sec{{background:#ffffff08;border:1px solid var(--borde);box-shadow:none;animation:none}}
.hero{{position:relative;z-index:5;min-height:90vh;display:grid;place-items:center;text-align:center;padding:70px 6vw 110px;overflow:hidden;background:linear-gradient(180deg,color-mix(in srgb,var(--fondo) 75%,transparent),var(--fondo) 94%),url("{t["set"]}") center/cover,var(--fondo)}}
.etiqueta{{display:inline-block;border:1px solid var(--c1);color:var(--c3);border-radius:999px;padding:6px 14px;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;background:color-mix(in srgb,var(--fondo) 70%,transparent)}}
h1{{font-family:{t["familia"]},Georgia,serif;font-size:clamp(52px,10.5vw,132px);line-height:.95;margin:22px 0 12px;text-shadow:0 0 30px color-mix(in srgb,var(--c2) 80%,transparent),0 0 60px color-mix(in srgb,var(--c1) 40%,transparent)}}
h1 em{{font-style:normal;color:var(--c1);display:inline-block;animation:brilla 3s ease-in-out infinite}}@keyframes brilla{{50%{{filter:brightness(1.35);transform:translateY(-3px)}}}}
.lema{{font-size:clamp(18px,2.5vw,25px);color:var(--tinta);opacity:.9;max-width:680px;margin:0 auto}}
.datos{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:28px 0}}.dato{{background:color-mix(in srgb,var(--fondo) 70%,transparent);border:1px solid var(--borde);border-radius:14px;padding:10px 16px;font-weight:600;backdrop-filter:blur(4px)}}
.cupos{{margin-top:18px;color:var(--c3);font-weight:700}}
main{{position:relative;z-index:5}}section{{padding:80px 6vw;max-width:1200px;margin:0 auto}}
h2{{font-family:{t["familia"]},Georgia,serif;font-size:clamp(32px,5.2vw,56px);margin-bottom:10px}}h2 span{{color:var(--c1)}}
.sub{{color:var(--tenue);max-width:660px;margin-bottom:36px}}
.pasos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}}
.paso{{background:var(--tarjeta);border:1px solid var(--borde);border-radius:20px;padding:22px;transition:transform .3s,border-color .3s}}.paso:hover{{transform:translateY(-6px);border-color:var(--c1)}}
.paso b{{display:block;font-size:38px;margin-bottom:6px;animation:flotar 5s ease-in-out infinite}}
.paquetes{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;align-items:stretch}}
.paquete{{position:relative;border:1px solid var(--borde);border-radius:26px;overflow:hidden;display:flex;flex-direction:column;background:var(--tarjeta);transition:transform .35s}}.paquete:hover{{transform:translateY(-8px)}}
.retrato{{height:300px;background-size:cover;background-position:center 20%;position:relative}}.retrato::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,var(--tarjeta))}}
.retrato .personaje{{position:absolute;left:18px;bottom:14px;z-index:2;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:#000000a0;border-radius:999px;padding:4px 10px}}
.paquete .cuerpo{{padding:4px 26px 26px;display:flex;flex-direction:column;flex:1}}
.paquete.destacado{{border:2px solid var(--c1);box-shadow:0 0 60px color-mix(in srgb,var(--c1) 35%,transparent)}}
.insignia{{position:absolute;top:14px;right:14px;z-index:3;background:var(--c1);color:#000;font-size:12px;font-weight:800;border-radius:999px;padding:5px 12px}}
.paquete h3{{font-family:{t["familia"]},Georgia,serif;font-size:34px}}.precio{{font-size:38px;font-weight:800;margin:4px 0 2px}}.antes{{color:var(--tenue);font-size:14px;text-decoration:line-through}}
.paquete ul{{list-style:none;margin:16px 0 22px;display:grid;gap:8px}}.paquete li::before{{content:"{t["vela"]} "}}.paquete .boton{{margin-top:auto;text-align:center}}
.comunidad{{margin-top:26px;background:linear-gradient(90deg,color-mix(in srgb,var(--c2) 22%,transparent),transparent);border:1px solid var(--c2);border-radius:18px;padding:18px 22px}}
.extra{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:20px}}.caja{{background:var(--tarjeta);border:1px solid var(--borde);border-radius:22px;padding:22px}}
.galeria{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.foto{{aspect-ratio:3/4;border-radius:18px;border:1px solid var(--borde);background-size:cover;background-position:center;position:relative;overflow:hidden;transition:transform .4s}}.foto:hover{{transform:scale(1.04)}}
.foto span{{position:absolute;left:10px;bottom:10px;font-size:12px;background:#000000a0;padding:3px 9px;border-radius:999px}}
.aparta{{text-align:center;background:var(--tarjeta);border:1px solid var(--borde);border-radius:28px;padding:40px 24px}}
details{{border-bottom:1px solid var(--borde);padding:16px 0}}summary{{cursor:pointer;font-weight:700}}details p{{color:var(--tenue);margin-top:8px}}
footer{{position:relative;z-index:5;text-align:center;color:var(--tenue);padding:60px 6vw 90px;border-top:1px solid var(--borde)}}
.barra{{position:fixed;left:0;right:0;bottom:0;z-index:40;display:none;padding:12px 16px;background:color-mix(in srgb,var(--fondo) 92%,transparent);border-top:1px solid var(--borde)}}
@media(max-width:700px){{.galeria{{grid-template-columns:repeat(2,1fr)}}.barra{{display:block}}.barra .boton{{display:block;text-align:center}}header .boton{{display:none}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important}}}}
</style></head><body>
{decor(t)}
<header><div class="logo">COSPLAY <span>INC</span> · EXPERIENCE</div><a class="boton" href="{aparta}" target="_blank" rel="noopener">Apartar mi cupo</a></header>
<div class="hero"><div style="position:relative;z-index:7">
<span class="etiqueta">{t["etiqueta"]}</span><h1>{t["titulo"]} <em>{t["em"]}</em></h1><p class="lema">{t["lema"]}</p>
<div class="datos"><span class="dato">{t["cuando"]}</span><span class="dato">📍 Bogotá · estudio tematizado</span><span class="dato">📸 Fotos + 🎬 video</span></div>
<a class="boton" href="#paquetes">Elige tu historia · desde $230.000</a><p class="cupos">✦ Cupos limitados · aparta el tuyo y te avisamos primero</p></div></div>
<main>
<section><h2>{t["h2a"]} <span>experiencia</span></h2><p class="sub">Llega con tu personaje o tu mejor look. Nosotros ponemos el set, la luz, la ambientación y la historia. Creamos tu contenido en foto y video.</p><div class="pasos">{pasos}</div></section>
<section><h2>Lo que <span>vives</span></h2><p class="sub">En cada experiencia, todo esto va incluido.</p><div class="pasos">{vives}</div></section>
<section id="paquetes"><h2>{t["h2b"]} <span>{t["h2c"]}</span></h2><p class="sub">Todo incluido: set, ambientación, dirección de poses, edición y galería privada. Lo que quieras de más, lo sumas después.</p>
<div class="paquetes">{tarjetas}</div>
<div class="comunidad">⭐ <strong>¿Estuviste en SOFA 2026 o ya te tomaste fotos con nosotros?</strong> Tienes <strong>10 % de descuento</strong>: cuéntanos al apartar con el correo o WhatsApp con el que compraste.</div>
<div class="extra"><div class="caja"><strong>{t["vela"]} Adicionales</strong><p class="sub" style="margin:6px 0 0">Foto extra $60.000 · Video extra $80.000. Súmalos el día o desde tu galería.</p></div>
<div class="caja" style="border-color:var(--c2)"><strong>{t["privada"]}</strong><p class="sub" style="margin:6px 0 0">{t["privadaTxt"]} Solo 2 bloques. <b style="color:var(--tinta)">$800.000</b></p></div></div></section>
<section><h2>Así se verá tu <span>historia</span></h2><p class="sub">Referencias del estilo de la sesión. El día del evento, aquí van fotos reales del set.</p><div class="galeria">{galeria}</div></section>
<section><div class="aparta"><h2>Fecha y <span>turnos</span></h2><p class="sub" style="margin:10px auto 24px">Estamos cerrando la fecha de diciembre. Aparta tu cupo por WhatsApp y te escribimos antes que a nadie con la fecha, los turnos y el enlace de pago.</p><a class="boton" href="{aparta}" target="_blank" rel="noopener">Apartar mi cupo por WhatsApp</a></div></section>
<section><h2>{t["faqTitulo"][0]} <span>{t["faqTitulo"][1]}</span></h2>{faq}</section>
</main>
<footer><p style="font-size:34px">{t["pie"]}</p><p class="logo" style="margin-top:10px">COSPLAY <span>INC</span></p><p style="margin-top:8px">cosplay-inc.com{t["ruta"]} · WhatsApp +57 315 457 5440 · <a href="/experiencias" style="text-decoration:underline">Todas las experiencias</a></p></footer>
<div class="barra"><a class="boton" href="#paquetes">Elegir mi historia · desde $230.000</a></div>
</body></html>'''

import sys,os
base=sys.argv[1]
for clave,t in TEMAS.items():
    os.makedirs(f"{base}/{clave}",exist_ok=True)
    open(f"{base}/{clave}/index.html","w").write(pagina(t))
print("ok")
