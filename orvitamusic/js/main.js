/* =========================================================
   ORVITA MUSIC — Interacciones y escena 3D
   ========================================================= */
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

document.getElementById("year").textContent = new Date().getFullYear();

/* ---------- Nav ---------- */
const nav = document.getElementById("nav");
const navToggle = document.getElementById("navToggle");
const onScrollNav = () => nav.classList.toggle("is-scrolled", window.scrollY > 40);
onScrollNav();
window.addEventListener("scroll", onScrollNav, { passive: true });
navToggle.addEventListener("click", () => {
  const open = nav.classList.toggle("is-open");
  navToggle.setAttribute("aria-expanded", String(open));
});
document.querySelectorAll("#navLinks a").forEach((a) =>
  a.addEventListener("click", () => {
    nav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  })
);

/* ---------- Reveal on scroll ----------
   Se revisa en cada scroll (throttle con rAF) para que nada quede oculto
   si el usuario salta con un ancla o hace scroll muy rápido. */
let pendingReveal = [...document.querySelectorAll(".reveal")];
let revealQueued = false;
const checkReveal = () => {
  revealQueued = false;
  const limit = window.innerHeight * 0.9;
  pendingReveal = pendingReveal.filter((el) => {
    if (el.getBoundingClientRect().top < limit) {
      el.classList.add("is-in");
      return false;
    }
    return true;
  });
  if (!pendingReveal.length) window.removeEventListener("scroll", queueReveal);
};
const queueReveal = () => { if (!revealQueued) { revealQueued = true; requestAnimationFrame(checkReveal); } };
window.addEventListener("scroll", queueReveal, { passive: true });
window.addEventListener("resize", queueReveal);
checkReveal();

/* ---------- Timeline progress ---------- */
const timeline = document.querySelector(".timeline");
const updateTimeline = () => {
  if (!timeline) return;
  const r = timeline.getBoundingClientRect();
  const vh = window.innerHeight;
  const p = Math.min(Math.max((vh * 0.85 - r.top) / (r.height + vh * 0.4), 0), 1);
  timeline.style.setProperty("--progress", p.toFixed(3));
};
updateTimeline();
window.addEventListener("scroll", updateTimeline, { passive: true });

/* ---------- Cards con tilt 3D ---------- */
if (finePointer && !reduceMotion) {
  document.querySelectorAll(".tilt").forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width;
      const y = (e.clientY - r.top) / r.height;
      card.style.setProperty("--ry", `${(x - 0.5) * 16}deg`);
      card.style.setProperty("--rx", `${(0.5 - y) * 16}deg`);
      card.style.setProperty("--mx", `${x * 100}%`);
      card.style.setProperty("--my", `${y * 100}%`);
    });
    card.addEventListener("pointerleave", () => {
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    });
  });
}

/* ---------- Botones magnéticos ---------- */
if (finePointer && !reduceMotion) {
  document.querySelectorAll(".magnetic").forEach((btn) => {
    btn.addEventListener("pointermove", (e) => {
      const r = btn.getBoundingClientRect();
      const x = e.clientX - r.left - r.width / 2;
      const y = e.clientY - r.top - r.height / 2;
      btn.style.transform = `translate(${x * 0.25}px, ${y * 0.35}px)`;
    });
    btn.addEventListener("pointerleave", () => { btn.style.transform = ""; });
  });
}

/* ---------- Cursor personalizado ---------- */
if (finePointer && !reduceMotion) {
  const cursor = document.querySelector(".cursor");
  const dot = cursor.querySelector(".cursor__dot");
  const ring = cursor.querySelector(".cursor__ring");
  let mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
  window.addEventListener("pointermove", (e) => {
    mx = e.clientX; my = e.clientY;
    dot.style.transform = `translate(${mx}px, ${my}px) translate(-50%, -50%)`;
  });
  const loop = () => {
    rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
    ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%)`;
    requestAnimationFrame(loop);
  };
  loop();
  document.querySelectorAll("a, button, .card").forEach((el) => {
    el.addEventListener("pointerenter", () => cursor.classList.add("is-hover"));
    el.addEventListener("pointerleave", () => cursor.classList.remove("is-hover"));
  });
} else {
  document.querySelector(".cursor")?.remove();
}

/* =========================================================
   ESCENA 3D — Planeta sonoro con anillos orbitales
   ========================================================= */
const canvas = document.getElementById("orbit3d");

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
    .then((THREE) => initScene(THREE))
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

function initScene(THREE) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0, 9);

  const GREEN = new THREE.Color("#39ff88");
  const PURPLE = new THREE.Color("#b026ff");
  const SKY = new THREE.Color("#5cd6ff");

  const world = new THREE.Group();
  scene.add(world);

  /* --- Planeta sonoro (shader con ruido) --- */
  const uniforms = {
    uTime: { value: 0 },
    uBeat: { value: 0 },
    uGreen: { value: GREEN },
    uPurple: { value: PURPLE },
    uSky: { value: SKY },
  };
  const planetMat = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: /* glsl */ `
      uniform float uTime; uniform float uBeat;
      varying float vNoise; varying vec3 vNormal; varying vec3 vView;
      ${NOISE_GLSL}
      void main(){
        float n = snoise(normal * 1.6 + uTime * .35);
        float n2 = snoise(normal * 4.0 - uTime * .6) * .35;
        vNoise = n + n2;
        vec3 pos = position + normal * (vNoise * (.22 + uBeat * .18));
        vec4 mv = modelViewMatrix * vec4(pos, 1.);
        vNormal = normalize(normalMatrix * normal);
        vView = normalize(-mv.xyz);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: /* glsl */ `
      uniform vec3 uGreen; uniform vec3 uPurple; uniform vec3 uSky; uniform float uBeat;
      varying float vNoise; varying vec3 vNormal; varying vec3 vView;
      void main(){
        float t = smoothstep(-.8, .9, vNoise);
        vec3 col = mix(uPurple, uSky, t);
        col = mix(col, uGreen, smoothstep(.55, 1., t));
        float fres = pow(1. - max(dot(vNormal, vView), 0.), 2.2);
        col = col * (.35 + .5 * t) + fres * mix(uSky, uGreen, .5) * (1.2 + uBeat);
        gl_FragColor = vec4(col, 1.);
      }`,
  });
  const planet = new THREE.Mesh(new THREE.IcosahedronGeometry(1.7, window.innerWidth < 760 ? 24 : 48), planetMat);
  world.add(planet);

  // Malla wireframe exterior
  const wire = new THREE.Mesh(
    new THREE.IcosahedronGeometry(2.25, 2),
    new THREE.MeshBasicMaterial({ color: SKY, wireframe: true, transparent: true, opacity: 0.12 })
  );
  world.add(wire);

  /* --- Anillos orbitales + satélites --- */
  const rings = [];
  const ringDefs = [
    { r: 3.0, tube: 0.012, color: GREEN, tilt: [1.2, 0.2, 0], speed: 0.35 },
    { r: 3.6, tube: 0.008, color: PURPLE, tilt: [1.0, -0.5, 0.3], speed: -0.25 },
    { r: 4.3, tube: 0.006, color: SKY, tilt: [1.5, 0.6, -0.2], speed: 0.18 },
  ];
  ringDefs.forEach((d) => {
    const pivot = new THREE.Group();
    pivot.rotation.set(...d.tilt);
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(d.r, d.tube, 8, 220),
      new THREE.MeshBasicMaterial({ color: d.color, transparent: true, opacity: 0.85 })
    );
    pivot.add(ring);
    const sat = new THREE.Mesh(
      new THREE.SphereGeometry(0.09, 16, 16),
      new THREE.MeshBasicMaterial({ color: d.color })
    );
    const halo = new THREE.Mesh(
      new THREE.SphereGeometry(0.22, 16, 16),
      new THREE.MeshBasicMaterial({ color: d.color, transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending, depthWrite: false })
    );
    sat.add(halo);
    pivot.add(sat);
    world.add(pivot);
    rings.push({ pivot, sat, ...d, angle: Math.random() * Math.PI * 2 });
  });

  /* --- Partículas (disco + polvo estelar) --- */
  const COUNT = window.innerWidth < 760 ? 1400 : 3200;
  const positions = new Float32Array(COUNT * 3);
  const colors = new Float32Array(COUNT * 3);
  const palette = [GREEN, PURPLE, SKY];
  for (let i = 0; i < COUNT; i++) {
    const disc = i < COUNT * 0.6;
    let x, y, z;
    if (disc) {
      const a = Math.random() * Math.PI * 2;
      const rad = 2.6 + Math.pow(Math.random(), 0.7) * 3.2;
      x = Math.cos(a) * rad; z = Math.sin(a) * rad; y = (Math.random() - 0.5) * 0.25;
    } else {
      const rad = 6 + Math.random() * 14;
      const th = Math.random() * Math.PI * 2;
      const ph = Math.acos(2 * Math.random() - 1);
      x = rad * Math.sin(ph) * Math.cos(th); y = rad * Math.sin(ph) * Math.sin(th); z = rad * Math.cos(ph) - 6;
    }
    positions.set([x, y, z], i * 3);
    const c = palette[i % 3].clone().lerp(new THREE.Color("#ffffff"), Math.random() * 0.3);
    colors.set([c.r, c.g, c.b], i * 3);
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  pGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  const dotTex = (() => {
    const c = document.createElement("canvas"); c.width = c.height = 64;
    const g = c.getContext("2d");
    const grd = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    grd.addColorStop(0, "rgba(255,255,255,1)"); grd.addColorStop(0.3, "rgba(255,255,255,.6)"); grd.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = grd; g.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  })();
  const particles = new THREE.Points(pGeo, new THREE.PointsMaterial({
    size: 0.07, map: dotTex, vertexColors: true, transparent: true, opacity: 0.9,
    blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true,
  }));
  const disc = new THREE.Group();
  disc.rotation.set(0.35, 0, 0.15);
  disc.add(particles);
  world.add(disc);

  /* --- Layout responsivo --- */
  const resize = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const mobile = w < 760;
    world.position.x = mobile ? 0 : 2.8;
    world.position.y = mobile ? 2.2 : 0;
    world.scale.setScalar(mobile ? 0.62 : 1);
  };
  resize();
  window.addEventListener("resize", resize);

  /* --- Interacción --- */
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  window.addEventListener("pointermove", (e) => {
    pointer.tx = (e.clientX / innerWidth - 0.5) * 2;
    pointer.ty = (e.clientY / innerHeight - 0.5) * 2;
  }, { passive: true });

  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { threshold: 0 }).observe(canvas);

  const clock = new THREE.Clock();
  const BPM = 112;
  const render = () => {
    const t = clock.getElapsedTime();
    const speed = reduceMotion ? 0.15 : 1;
    // Pulso tipo kick: decaimiento exponencial en cada beat
    const phase = (t * BPM / 60) % 1;
    uniforms.uBeat.value = reduceMotion ? 0 : Math.exp(-phase * 6);
    uniforms.uTime.value = t * speed;

    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;
    const scroll = Math.min(window.scrollY / innerHeight, 1.5);

    planet.rotation.y = t * 0.15 * speed;
    planet.scale.setScalar(1 + uniforms.uBeat.value * 0.04);
    wire.rotation.y = -t * 0.08 * speed;
    wire.rotation.x = t * 0.05 * speed;
    disc.rotation.y = t * 0.05 * speed;

    rings.forEach((r) => {
      r.angle += r.speed * 0.01 * speed;
      r.sat.position.set(Math.cos(r.angle) * r.r, Math.sin(r.angle) * r.r, 0);
      r.pivot.rotation.z += r.speed * 0.002 * speed;
    });

    world.rotation.x = pointer.y * 0.25 + scroll * 0.6;
    world.rotation.y = pointer.x * 0.35;
    camera.position.z = 9 + scroll * 3;
    camera.position.y = -scroll * 1.2;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
  };

  const animate = () => {
    if (visible) render();
    requestAnimationFrame(animate);
  };
  animate();
}
