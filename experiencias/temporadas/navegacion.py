NAV_CSS='''
.sitio{position:relative;z-index:30;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;padding:16px 5vw;background:rgba(0,0,0,.35);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,255,255,.08)}
.sitio img{height:30px;filter:invert(1) brightness(1.2);display:block}
.sitio nav{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.sitio nav a{opacity:.8}.sitio nav a:hover{opacity:1;text-decoration:underline}
.pie-sitio{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 22px;margin:18px 0 6px;font-size:14px}
.pie-sitio a{text-decoration:underline;text-underline-offset:3px}
@media(max-width:700px){.sitio nav{gap:6px 12px;font-size:11px}}
'''
NAV_HTML='''<div class="sitio"><a href="/" aria-label="Cosplay Inc · inicio"><img src="/marca/cosplay-inc-web.webp" alt="Cosplay Inc"></a><nav><a href="/experiencias">← Experiencias</a><a href="/portafolio">Portafolio</a><a href="/portafolio/video">Video</a><a href="/sesionpersonalizada">Sesión personalizada</a><a href="/preguntas-frecuentes">Preguntas</a></nav></div>
'''
PIE_HTML='''<nav class="pie-sitio"><a href="/experiencias">← Volver a experiencias</a><a href="/">Inicio</a><a href="/portafolio">Portafolio</a><a href="/sesionpersonalizada">Sesión personalizada</a><a href="/preguntas-frecuentes">Preguntas frecuentes</a></nav>
'''
def aplicar(s):
    s=s.replace('</style>',NAV_CSS+'</style>',1)
    i=s.index('<header>')
    s=s[:i]+NAV_HTML+s[i:]
    s=s.replace('<p class="logo" style="margin-top:10px">COSPLAY <span>INC</span></p>',PIE_HTML+'<p class="logo" style="margin-top:10px">COSPLAY <span>INC</span></p>',1)
    return s
