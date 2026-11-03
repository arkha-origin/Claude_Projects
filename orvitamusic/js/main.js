/* =========================================================
   ORVITA MUSIC — Un universo que se recorre con el scroll
   ---------------------------------------------------------
   Todo el texto vive en el HTML. Este archivo solo:
   1. maneja menú, revelados, etapas y ayudas de navegación, y
   2. dibuja el sistema solar 3D de fondo: cada sección tiene un
      data-cam y la cámara viaja entre ellas según el scroll.
   ========================================================= */
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
const smooth = reduceMotion ? "auto" : "smooth";

document.getElementById("year").textContent = new Date().getFullYear();

/* ---------- Nav ---------- */
const nav = document.getElementById("nav");
const navToggle = document.getElementById("navToggle");
const closeMenu = () => { nav.classList.remove("is-open"); navToggle.setAttribute("aria-expanded", "false"); };
navToggle.addEventListener("click", () => {
  const open = nav.classList.toggle("is-open");
  navToggle.setAttribute("aria-expanded", String(open));
});
document.querySelectorAll("#navLinks a").forEach((a) => a.addEventListener("click", closeMenu));

/* ---------- Revelado al hacer scroll ---------- */
let pendingReveal = [...document.querySelectorAll(".reveal")];
const checkReveal = () => {
  const limit = innerHeight * 0.9;
  pendingReveal = pendingReveal.filter((el) => {
    if (el.getBoundingClientRect().top < limit) { el.classList.add("is-in"); return false; }
    return true;
  });
};

/* ---------- Etapas (pestañas accesibles) ---------- */
(function stageTabs() {
  const tabs = [...document.querySelectorAll(".stage__picker .chip")];
  const select = (tab, focus = false) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).classList.toggle("is-active", on);
    });
    if (focus) tab.focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (e) => {
      const dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (!dir) return;
      e.preventDefault();
      select(tabs[(i + dir + tabs.length) % tabs.length], true);
    });
  });
  if (tabs.length) select(tabs.find((t) => t.getAttribute("aria-selected") === "true") || tabs[0]);
})();

/* ---------- Ayudas de navegación ---------- */
const progressBar = document.getElementById("progressBar");
const toTop = document.getElementById("toTop");
const timeline = document.querySelector(".timeline");
const navAnchors = [...document.querySelectorAll("#navLinks a:not(.btn)")];
const navSections = navAnchors.map((a) => document.querySelector(a.getAttribute("href")));
const orbitbar = document.getElementById("orbitbar");
const orbitLinks = [...orbitbar.querySelectorAll("a")];
const stopsEls = orbitLinks.map((a) => document.querySelector(a.getAttribute("href")));
const mapEl = document.getElementById("servicios");

/* ---------- Recorrido horizontal de planetas ----------
   La sección mide 7 pantallas de alto; su interior queda fijo y el scroll
   vertical lo desplaza de lado. Con una pausa suave en cada planeta. */
const journey = document.getElementById("recorrido");
const track = document.getElementById("journeyTrack");
const jHint = document.getElementById("jHint");
const N = stopsEls.length;
let journeyIndex = 0;
const journeyProgress = () => {
  const r = journey.getBoundingClientRect();
  return Math.min(Math.max(-r.top / (r.height - innerHeight), 0), 1);
};
const updateJourney = () => {
  const seg = journeyProgress() * (N - 1);
  const i = Math.min(Math.floor(seg), N - 2);
  let f = Math.min(Math.max((seg - i - 0.15) / 0.7, 0), 1);
  f = f * f * (3 - 2 * f);
  track.style.transform = `translate3d(${-(i + f) * 100}vw, 0, 0)`;
  journeyIndex = Math.round(i + f);
  jHint.classList.toggle("is-gone", seg > 0.3);
};
// Ir al planeta i: el scroll vertical que le corresponde.
const goToPlanet = (i) => {
  i = Math.min(Math.max(i, 0), N - 1);
  const top = journey.getBoundingClientRect().top + scrollY;
  const y = top + (i / (N - 1)) * (journey.offsetHeight - innerHeight) + 1;
  window.scrollTo({ top: y, behavior: smooth });
};
window.goToPlanet = goToPlanet;
document.querySelectorAll('a[href^="#s-"]').forEach((a) => {
  const i = stopsEls.findIndex((el) => el.id === a.getAttribute("href").slice(1));
  a.addEventListener("click", (e) => { e.preventDefault(); closeMenu(); goToPlanet(i); });
});
document.getElementById("jPrev").addEventListener("click", () => goToPlanet(journeyIndex - 1));
document.getElementById("jNext").addEventListener("click", () => goToPlanet(journeyIndex + 1));
addEventListener("keydown", (e) => {
  if (!["ArrowRight", "ArrowLeft"].includes(e.key) || e.target.closest("input, textarea, [role=tab]")) return;
  const r = journey.getBoundingClientRect();
  if (r.top > 1 || r.bottom < innerHeight - 1) return;
  e.preventDefault();
  goToPlanet(journeyIndex + (e.key === "ArrowRight" ? 1 : -1));
});
if (location.hash.startsWith("#s-")) {
  const i = stopsEls.findIndex((el) => el.id === location.hash.slice(1));
  if (i >= 0) requestAnimationFrame(() => { history.replaceState(null, "", location.pathname); goToPlanet(i); });
}

const updateUI = () => {
  updateJourney();
  checkReveal();
  nav.classList.toggle("is-scrolled", scrollY > 40);
  const max = document.documentElement.scrollHeight - innerHeight;
  progressBar.style.transform = `scaleX(${max > 0 ? Math.min(scrollY / max, 1) : 0})`;
  

  let current = -1;
  navSections.forEach((sec, i) => { if (sec && sec.getBoundingClientRect().top < innerHeight * 0.4) current = i; });
  navAnchors.forEach((a, i) => a.classList.toggle("is-current", i === current));

  // Barra de planetas: visible desde el mapa hasta el último planeta.
  const mid = innerHeight / 2;
  const first = mapEl.getBoundingClientRect().top;
  const last = journey.getBoundingClientRect().bottom;
  orbitbar.classList.toggle("is-on", first < mid && last > mid);
  const jr = journey.getBoundingClientRect();
  const planet = jr.top <= 1 && jr.bottom >= innerHeight - 1 ? journeyIndex : -1;
  orbitLinks.forEach((a, i) => a.classList.toggle("is-current", i === planet));
  toTop.classList.toggle("is-on", scrollY > innerHeight && !orbitbar.classList.contains("is-on"));

  if (timeline) {
    const r = timeline.getBoundingClientRect();
    const p = Math.min(Math.max((innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.4), 0), 1);
    timeline.style.setProperty("--progress", p.toFixed(3));
  }
};
let uiQueued = false;
const queueUI = () => { if (!uiQueued) { uiQueued = true; requestAnimationFrame(() => { uiQueued = false; updateUI(); }); } };
addEventListener("scroll", queueUI, { passive: true });
addEventListener("resize", queueUI);
updateUI();

/* ---------- Botones magnéticos y cursor ---------- */
if (finePointer && !reduceMotion) {
  document.querySelectorAll(".magnetic").forEach((btn) => {
    btn.addEventListener("pointermove", (e) => {
      const r = btn.getBoundingClientRect();
      btn.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.25}px, ${(e.clientY - r.top - r.height / 2) * 0.35}px)`;
    });
    btn.addEventListener("pointerleave", () => { btn.style.transform = ""; });
  });
  const cursor = document.querySelector(".cursor");
  const dot = cursor.querySelector(".cursor__dot");
  const ring = cursor.querySelector(".cursor__ring");
  let mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
  addEventListener("pointermove", (e) => {
    mx = e.clientX; my = e.clientY;
    dot.style.transform = `translate(${mx}px, ${my}px) translate(-50%, -50%)`;
  });
  (function loop() {
    rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
    ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%)`;
    requestAnimationFrame(loop);
  })();
  document.addEventListener("pointerover", (e) => {
    cursor.classList.toggle("is-hover", !!e.target.closest("a, button, summary, .plabel"));
  });
} else {
  document.querySelector(".cursor")?.remove();
}

/* =========================================================
   EL UNIVERSO 3D
   ========================================================= */
const canvas = document.getElementById("universe");
function hasWebGL() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
  } catch { return false; }
}
if (!hasWebGL()) {
  document.documentElement.classList.add("no-webgl");
} else {
  import("./vendor/three.module.min.js")
    .then((THREE) => initUniverse(THREE))
    .catch((err) => {
      console.warn("Orvita 3D no disponible:", err);
      document.documentElement.classList.add("no-webgl");
    });
}

const NOISE_GLSL = /* glsl */ `
vec3 mod289(vec3 x){return x-floor(x*(1./289.))*289.;}
vec4 mod289(vec4 x){return x-floor(x*(1./289.))*289.;}
vec4 permute(vec4 x){return mod289(((x*34.)+1.)*x);}
vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-.85373472095314*r;}
float snoise(vec3 v){
  const vec2 C=vec2(1./6.,1./3.);const vec4 D=vec4(0.,.5,1.,2.);
  vec3 i=floor(v+dot(v,C.yyy));vec3 x0=v-i+dot(i,C.xxx);
  vec3 g=step(x0.yzx,x0.xyz);vec3 l=1.-g;vec3 i1=min(g.xyz,l.zxy);vec3 i2=max(g.xyz,l.zxy);
  vec3 x1=x0-i1+C.xxx;vec3 x2=x0-i2+C.yyy;vec3 x3=x0-D.yyy;
  i=mod289(i);
  vec4 p=permute(permute(permute(i.z+vec4(0.,i1.z,i2.z,1.))+i.y+vec4(0.,i1.y,i2.y,1.))+i.x+vec4(0.,i1.x,i2.x,1.));
  float n_=.142857142857;vec3 ns=n_*D.wyz-D.xzx;
  vec4 j=p-49.*floor(p*ns.z*ns.z);vec4 x_=floor(j*ns.z);vec4 y_=floor(j-7.*x_);
  vec4 x=x_*ns.x+ns.yyyy;vec4 y=y_*ns.x+ns.yyyy;vec4 h=1.-abs(x)-abs(y);
  vec4 b0=vec4(x.xy,y.xy);vec4 b1=vec4(x.zw,y.zw);
  vec4 s0=floor(b0)*2.+1.;vec4 s1=floor(b1)*2.+1.;vec4 sh=-step(h,vec4(0.));
  vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
  vec3 p0=vec3(a0.xy,h.x);vec3 p1=vec3(a0.zw,h.y);vec3 p2=vec3(a1.xy,h.z);vec3 p3=vec3(a1.zw,h.w);
  vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
  p0*=norm.x;p1*=norm.y;p2*=norm.z;p3*=norm.w;
  vec4 m=max(.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.);m=m*m;
  return 42.*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
}`;

/* Los siete planetas: uno por servicio, en el mismo orden que el HTML. */
const PLANETS = [
  { id: "s-roster", name: "Roster & Showcase", a: "#5dffa0", b: "#0b3a2c", atm: "#39ff88", r: 0.62, orbit: 4.6, bands: 5 },
  { id: "s-booking", name: "Booking Directo", a: "#dd9bff", b: "#3a0a6b", atm: "#b026ff", r: 0.82, orbit: 6.3, bands: 9, ring: true },
  { id: "s-audiovisual", name: "Audiovisual 4K", a: "#a8ecff", b: "#123a5a", atm: "#5cd6ff", r: 0.56, orbit: 7.9, bands: 4 },
  { id: "s-live", name: "Live Sessions", a: "#7dffc0", b: "#1d2b6b", atm: "#5cd6ff", r: 1.02, orbit: 9.6, bands: 12, ring: true },
  { id: "s-sync", name: "Sync & Placement", a: "#ff9be0", b: "#4a0d5c", atm: "#b026ff", r: 0.66, orbit: 11.6, bands: 6 },
  { id: "s-consultoria", name: "Consultoría 360°", a: "#6fdcff", b: "#0a1d3d", atm: "#39ff88", r: 0.86, orbit: 13.3, bands: 14 },
  { id: "s-camps", name: "Songwriting Camps", a: "#d2ff7a", b: "#0f3d22", atm: "#39ff88", r: 0.72, orbit: 15.0, bands: 7, moon: true },
];

function initUniverse(THREE) {
  const isMobile = () => innerWidth < 760;
  const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(devicePixelRatio, isMobile() ? 1.5 : 1.75));
  renderer.setClearColor(0x07060d, 1);
  document.documentElement.classList.add("has-universe");

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 800);

  /* --- Texturas pintadas en canvas (sin archivos extra) --- */
  const radialTex = (stops) => {
    const c = document.createElement("canvas"); c.width = c.height = 128;
    const g = c.getContext("2d");
    const grd = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    stops.forEach(([o, col]) => grd.addColorStop(o, col));
    g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  };
  const glowTex = radialTex([[0, "rgba(255,255,255,1)"], [0.25, "rgba(255,255,255,.45)"], [1, "rgba(255,255,255,0)"]]);
  const softTex = radialTex([[0, "rgba(255,255,255,.9)"], [0.5, "rgba(255,255,255,.25)"], [1, "rgba(255,255,255,0)"]]);
  const glow = (color, scale, opacity) => {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTex, color, transparent: true, opacity, blending: THREE.AdditiveBlending, depthWrite: false,
    }));
    s.scale.setScalar(scale); return s;
  };

  /* --- Estrellas y nebulosas --- */
  const stars = (count, rMin, rMax, size, opacity) => {
    const pos = new Float32Array(count * 3), col = new Float32Array(count * 3);
    const tints = [new THREE.Color("#ffffff"), new THREE.Color("#5cd6ff"), new THREE.Color("#d9b3ff"), new THREE.Color("#b6ffd4")];
    for (let i = 0; i < count; i++) {
      const r = rMin + Math.random() * (rMax - rMin);
      const th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1);
      pos.set([r * Math.sin(ph) * Math.cos(th), r * Math.cos(ph) * 0.7, r * Math.sin(ph) * Math.sin(th)], i * 3);
      const c = tints[i % 4]; col.set([c.r, c.g, c.b], i * 3);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    g.setAttribute("color", new THREE.BufferAttribute(col, 3));
    return new THREE.Points(g, new THREE.PointsMaterial({
      size, map: softTex, vertexColors: true, transparent: true, opacity, depthWrite: false,
      blending: THREE.AdditiveBlending, sizeAttenuation: false,
    }));
  };
  const mobileNow = isMobile();
  scene.add(stars(mobileNow ? 1800 : 4200, 90, 320, 2.2 * renderer.getPixelRatio(), 0.9));
  scene.add(stars(mobileNow ? 160 : 380, 90, 300, 4.5 * renderer.getPixelRatio(), 1));
  [["#b026ff", V(-120, 30, -160), 230], ["#5cd6ff", V(150, -40, -120), 200], ["#39ff88", V(40, 70, 170), 180],
   ["#b026ff", V(-160, -60, 120), 220], ["#5cd6ff", V(0, 120, -60), 160]].forEach(([c, p, s]) => {
    const n = new THREE.Sprite(new THREE.SpriteMaterial({ map: softTex, color: c, transparent: true, opacity: 0.16, depthWrite: false, blending: THREE.AdditiveBlending }));
    n.position.copy(p); n.scale.setScalar(s); scene.add(n);
  });

  /* --- El sol: el centro de gravedad (el artista) --- */
  const sunU = { uTime: { value: 0 }, uBeat: { value: 0 }, uGreen: { value: new THREE.Color("#39ff88") }, uPurple: { value: new THREE.Color("#b026ff") }, uSky: { value: new THREE.Color("#5cd6ff") } };
  const sun = new THREE.Mesh(new THREE.IcosahedronGeometry(1.8, mobileNow ? 24 : 48), new THREE.ShaderMaterial({
    uniforms: sunU,
    vertexShader: /* glsl */ `
      uniform float uTime; uniform float uBeat;
      varying float vNoise; varying vec3 vNormal; varying vec3 vView;
      ${NOISE_GLSL}
      void main(){
        vNoise = snoise(normal * 1.6 + uTime * .35) + snoise(normal * 4.0 - uTime * .6) * .35;
        vec3 pos = position + normal * (vNoise * (.2 + uBeat * .16));
        vec4 mv = modelViewMatrix * vec4(pos, 1.);
        vNormal = normalize(normalMatrix * normal); vView = normalize(-mv.xyz);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: /* glsl */ `
      uniform vec3 uGreen; uniform vec3 uPurple; uniform vec3 uSky; uniform float uBeat;
      varying float vNoise; varying vec3 vNormal; varying vec3 vView;
      void main(){
        float t = smoothstep(-.8, .9, vNoise);
        vec3 col = mix(uPurple, uSky, t); col = mix(col, uGreen, smoothstep(.55, 1., t));
        float fres = pow(1. - max(dot(vNormal, vView), 0.), 2.2);
        gl_FragColor = vec4(col * (.55 + .6 * t) + fres * mix(uSky, uGreen, .5) * (1.3 + uBeat), 1.);
      }`,
  }));
  scene.add(sun);
  const sunGlowA = glow("#39ff88", 9, 0.35), sunGlowB = glow("#b026ff", 16, 0.3);
  scene.add(sunGlowA, sunGlowB);
  const sunWire = new THREE.Mesh(new THREE.IcosahedronGeometry(2.5, 2),
    new THREE.MeshBasicMaterial({ color: "#5cd6ff", wireframe: true, transparent: true, opacity: 0.1 }));
  scene.add(sunWire);

  /* --- Planetas, órbitas, anillos --- */
  const planetVS = /* glsl */ `
    varying vec3 vN; varying vec3 vObjN; varying vec3 vW;
    void main(){
      vObjN = normal;
      vec4 w = modelMatrix * vec4(position, 1.);
      vW = w.xyz; vN = normalize(mat3(modelMatrix) * normal);
      gl_Position = projectionMatrix * viewMatrix * w;
    }`;
  const planetFS = /* glsl */ `
    uniform vec3 uA; uniform vec3 uB; uniform vec3 uAtm; uniform float uSeed; uniform float uTime; uniform float uBands; uniform float uFocus;
    varying vec3 vN; varying vec3 vObjN; varying vec3 vW;
    ${NOISE_GLSL}
    void main(){
      vec3 n = normalize(vObjN);
      float f = snoise(n * 2.2 + uSeed + uTime * .02) * .6 + snoise(n * 6. + uSeed * 2.) * .25;
      float bands = sin((n.y + f * .22) * uBands);
      vec3 col = mix(uB, uA, smoothstep(-.6, .8, f + bands * .35));
      vec3 N = normalize(vN); vec3 L = normalize(-vW); vec3 Vd = normalize(cameraPosition - vW);
      float diff = max(dot(N, L), 0.);
      float fres = pow(1. - max(dot(N, Vd), 0.), 2.4);
      vec3 c = col * (.07 + 1.15 * diff) + uAtm * fres * (.35 + .9 * smoothstep(-.3, .6, dot(N, L))) * (1. + uFocus * .6);
      gl_FragColor = vec4(c, 1.);
    }`;
  const seg = mobileNow ? 48 : 72;
  const planets = PLANETS.map((d, i) => {
    const uniforms = {
      uA: { value: new THREE.Color(d.a) }, uB: { value: new THREE.Color(d.b) }, uAtm: { value: new THREE.Color(d.atm) },
      uSeed: { value: i * 3.17 + 1.3 }, uTime: { value: 0 }, uBands: { value: d.bands }, uFocus: { value: 0 },
    };
    const group = new THREE.Group();
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(d.r, seg, seg), new THREE.ShaderMaterial({ uniforms, vertexShader: planetVS, fragmentShader: planetFS }));
    mesh.rotation.z = 0.3 - i * 0.07;
    group.add(mesh);
    const halo = glow(d.atm, d.r * 5, 0.3);
    group.add(halo);
    if (d.ring) {
      const tilt = new THREE.Group(); tilt.rotation.set(Math.PI / 2 - 0.45, 0.2, 0);
      [[1.45, 1.75, 0.45], [1.8, 2.25, 0.22], [2.3, 2.4, 0.35]].forEach(([a, b, o]) => {
        tilt.add(new THREE.Mesh(new THREE.RingGeometry(d.r * a, d.r * b, 128),
          new THREE.MeshBasicMaterial({ color: d.atm, side: THREE.DoubleSide, transparent: true, opacity: o, depthWrite: false })));
      });
      group.add(tilt);
    }
    let moon = null;
    if (d.moon) {
      moon = new THREE.Mesh(new THREE.SphereGeometry(d.r * 0.24, 24, 24), new THREE.MeshBasicMaterial({ color: "#e9f7ff" }));
      moon.add(glow("#5cd6ff", d.r * 1.2, 0.5));
      group.add(moon);
    }
    scene.add(group);

    const pts = [];
    for (let k = 0; k <= 256; k++) { const a = (k / 256) * Math.PI * 2; pts.push(V(Math.cos(a) * d.orbit, 0, Math.sin(a) * d.orbit)); }
    const orbitMat = new THREE.LineBasicMaterial({ color: d.atm, transparent: true, opacity: 0.16 });
    scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), orbitMat));

    return { ...d, group, mesh, halo, moon, uniforms, orbitMat, angle: i * 2.35 + 0.6, speed: 0.42 / Math.pow(d.orbit, 1.5) };
  });

  /* Cinturón de asteroides entre Live Sessions y Sync */
  {
    const n = mobileNow ? 700 : 1600, pos = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const a = Math.random() * Math.PI * 2, r = 10.6 + (Math.random() - 0.5) * 0.9;
      pos.set([Math.cos(a) * r, (Math.random() - 0.5) * 0.25, Math.sin(a) * r], i * 3);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    var belt = new THREE.Points(g, new THREE.PointsMaterial({ size: 0.06, color: "#a39fbf", map: softTex, transparent: true, opacity: 0.8, depthWrite: false }));
    scene.add(belt);
  }

  /* --- Etiquetas clicables sobre los planetas (en la vista del mapa) --- */
  const labelLayer = document.getElementById("plabels");
  const labels = planets.map((p, i) => {
    const b = document.createElement("button");
    b.className = "plabel"; b.type = "button"; b.style.setProperty("--c", p.atm);
    b.innerHTML = `<i></i><span>0${i + 1}</span>${p.name}`;
    b.tabIndex = -1; // ya existen enlaces equivalentes en la lista del mapa
    b.addEventListener("click", () => window.goToPlanet(i));
    labelLayer.appendChild(b);
    return b;
  });

  /* --- Estaciones de cámara: una por sección con data-cam --- */
  const stops = [...document.querySelectorAll("[data-cam]")];
  const keys = stops.map((el) => el.dataset.cam);
  const fixed = {
    //            posición cámara      mira a        desplazamiento en pantalla       velo  etiquetas
    hero:     () => ({ pos: isMobile() ? V(0, 24, 54) : V(0, 9, 28), target: V(), sx: isMobile() ? 0 : 0.2, sy: isMobile() ? 0.36 : 0, veil: isMobile() ? 0.3 : 0, labels: 0 }),
    map:      () => ({ pos: isMobile() ? V(0, 50, 16) : V(0, 30, 17), target: V(), sx: isMobile() ? 0 : 0.2, sy: isMobile() ? 0.34 : 0, veil: isMobile() ? 0.3 : 0, labels: 1 }),
    overview: () => ({ pos: V(0, 44, 0.01), target: V(), sx: 0, sy: 0, veil: 0.55, labels: 0 }),
    side:     () => ({ pos: V(24, 5, 16), target: V(0, 0, 0), sx: 0, sy: 0, veil: 0.5, labels: 0 }),
    process:  () => ({ pos: V(-8, 1.4, 22), target: V(2, 0, 0), sx: 0, sy: 0, veil: 0.5, labels: 0 }),
    sun:      () => ({ pos: isMobile() ? V(0, 2.5, 11) : V(0, 1.6, 8), target: V(), sx: isMobile() ? 0 : -0.22, sy: isMobile() ? 0.38 : 0, veil: isMobile() ? 0.5 : 0.22, labels: 0 }),
    far:      () => ({ pos: V(-38, 16, 54), target: V(), sx: 0, sy: 0, veil: 0.55, labels: 0 }),
    contact:  () => ({ pos: V(0, 3.2, 17), target: V(0, 0.4, 0), sx: 0, sy: 0, veil: 0.2, labels: 0 }),
  };
  const planetState = (i) => {
    const p = planets[i], c = p.group.position, s = p.r;
    const out = V(c.x, 0, c.z).normalize();
    const tan = V(-out.z, 0, out.x);
    const k = isMobile() ? 1.3 : 1;
    const pos = c.clone().addScaledVector(out, -s * 2.6 * k).addScaledVector(tan, s * 4.4 * k).add(V(0, s * 1.5 * k, 0));
    return { pos, target: c.clone(), sx: isMobile() ? 0 : 0.21, sy: isMobile() ? 0.33 : 0, veil: 0.08, labels: 0 };
  };
  const stateOf = (key) => (/^p\d$/.test(key) ? planetState(Number(key.slice(1))) : fixed[key]());

  // Qué estaciones rodean el centro de la pantalla, y cuánto se avanzó entre ellas.
  const blend = () => {
    const midY = innerHeight / 2, midX = innerWidth / 2;
    const c = stops.map((el) => {
      const r = el.getBoundingClientRect();
      return (r.top + r.height / 2 - midY) + (r.left + r.width / 2 - midX) * (innerHeight / innerWidth);
    });
    if (c[0] >= 0) return [0, 0, 0];
    for (let i = 0; i < c.length - 1; i++) {
      if (c[i] <= 0 && c[i + 1] > 0) {
        let t = -c[i] / (c[i + 1] - c[i]);
        t = Math.min(Math.max((t - 0.18) / 0.64, 0), 1); // pausa en cada estación
        return [i, i + 1, t * t * (3 - 2 * t)];
      }
    }
    return [c.length - 1, c.length - 1, 0];
  };

  /* --- Tamaño y desplazamiento de la vista --- */
  let W = 0, H = 0;
  const resize = () => {
    W = canvas.clientWidth; H = canvas.clientHeight;
    renderer.setSize(W, H, false);
    camera.aspect = W / H;
  };
  resize();
  addEventListener("resize", resize);

  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener("pointermove", (e) => {
    pointer.tx = (e.clientX / innerWidth - 0.5) * 2;
    pointer.ty = (e.clientY / innerHeight - 0.5) * 2;
  }, { passive: true });

  const veil = document.getElementById("veil");
  const cam = { pos: V(0, 60, 90), target: V(), sx: 0, sy: 0, veil: 0, labels: 0 };
  const tmp = V();
  const clock = new THREE.Clock();
  const BPM = 112;
  let first = true;

  const render = () => {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;
    const motion = reduceMotion ? 0 : 1;

    // Órbitas
    planets.forEach((p, i) => {
      p.angle += p.speed * dt * motion;
      p.group.position.set(Math.cos(p.angle) * p.orbit, 0, Math.sin(p.angle) * p.orbit);
      p.mesh.rotation.y += dt * (0.15 + i * 0.02) * motion;
      p.uniforms.uTime.value = t;
      if (p.moon) p.moon.position.set(Math.cos(t * 0.8) * p.r * 1.9, Math.sin(t * 0.8) * p.r * 0.4, Math.sin(t * 0.8) * p.r * 1.9);
    });
    belt.rotation.y += dt * 0.01 * motion;

    // Sol que late a 112 BPM
    const beat = reduceMotion ? 0 : Math.exp(-((t * BPM / 60) % 1) * 6);
    sunU.uBeat.value = beat; sunU.uTime.value = t * (reduceMotion ? 0.1 : 1);
    sun.scale.setScalar(1 + beat * 0.035);
    sunGlowA.material.opacity = 0.3 + beat * 0.15;
    sunWire.rotation.y = -t * 0.06 * motion; sunWire.rotation.x = t * 0.04 * motion;

    // Cámara: mezcla entre las dos estaciones más cercanas
    const [ia, ib, k] = blend();
    const A = stateOf(keys[ia]), B = stateOf(keys[ib]);
    // Entre dos planetas, la cámara viaja en arco alrededor del sol (no lo atraviesa).
    const arc = (a, b) => {
      const ra = Math.hypot(a.x, a.z), rb = Math.hypot(b.x, b.z);
      const aa = Math.atan2(a.z, a.x);
      let d = Math.atan2(b.z, b.x) - aa;
      d = Math.atan2(Math.sin(d), Math.cos(d));
      const ang = aa + d * k, r = ra + (rb - ra) * k;
      return V(Math.cos(ang) * r, a.y + (b.y - a.y) * k, Math.sin(ang) * r);
    };
    const bothPlanets = /^p\d$/.test(keys[ia]) && /^p\d$/.test(keys[ib]);
    const goal = {
      pos: bothPlanets ? arc(A.pos, B.pos) : A.pos.lerp(B.pos, k),
      target: bothPlanets ? arc(A.target, B.target) : A.target.lerp(B.target, k),
      sx: A.sx + (B.sx - A.sx) * k, sy: A.sy + (B.sy - A.sy) * k,
      veil: A.veil + (B.veil - A.veil) * k, labels: A.labels + (B.labels - A.labels) * k,
    };
    pointer.x += (pointer.tx - pointer.x) * 0.05; pointer.y += (pointer.ty - pointer.y) * 0.05;
    const dist = goal.pos.distanceTo(goal.target);
    goal.pos.x += pointer.x * dist * 0.03 * motion; goal.pos.y -= pointer.y * dist * 0.02 * motion;

    const f = first ? 1 : 1 - Math.exp(-dt * (reduceMotion ? 20 : 3.2));
    first = false;
    cam.pos.lerp(goal.pos, f); cam.target.lerp(goal.target, f);
    cam.sx += (goal.sx - cam.sx) * f; cam.sy += (goal.sy - cam.sy) * f;
    cam.veil += (goal.veil - cam.veil) * f; cam.labels += (goal.labels - cam.labels) * f;

    camera.position.copy(cam.pos); camera.lookAt(cam.target);
    camera.setViewOffset(W, H, -cam.sx * W, cam.sy * H, W, H);
    camera.updateProjectionMatrix();
    veil.style.opacity = cam.veil.toFixed(3);

    // Foco: la órbita y el brillo del planeta que se está visitando
    planets.forEach((p, i) => {
      const w = (keys[ia] === `p${i}` ? 1 - k : 0) + (keys[ib] === `p${i}` ? k : 0);
      p.orbitMat.opacity = 0.14 + 0.55 * w + 0.2 * cam.labels;
      p.uniforms.uFocus.value = w;
    });

    // Etiquetas proyectadas sobre los planetas
    labelLayer.style.opacity = cam.labels.toFixed(3);
    labelLayer.classList.toggle("is-on", cam.labels > 0.6);
    if (cam.labels > 0.01) {
      planets.forEach((p, i) => {
        tmp.copy(p.group.position); tmp.y += p.r * 1.3; tmp.project(camera);
        const x = (tmp.x + 1) / 2 * W, y = (1 - tmp.y) / 2 * H;
        labels[i].style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -100%)`;
        labels[i].style.visibility = tmp.z < 1 ? "visible" : "hidden";
      });
    }

    renderer.render(scene, camera);
  };

  const loop = () => {
    if (!document.hidden) render();
    requestAnimationFrame(loop);
  };
  loop();
}
