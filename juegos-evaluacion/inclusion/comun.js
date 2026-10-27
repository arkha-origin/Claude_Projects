/* Apoyos comunes de los juegos de inclusión: voz, sonidos suaves y celebración. Sin internet. */
(function () {
  var A = (window.APOYO = {});
  var ctx = null;
  A.sonidoOn = localStorage.getItem("incl-sonido") !== "no";
  A.vozOn = localStorage.getItem("incl-voz") !== "no";
  A.hablar = function (t) {
    if (!A.vozOn || !window.speechSynthesis) return;
    try {
      speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(t);
      u.lang = "es-CO"; u.rate = 0.85; u.pitch = 1.05;
      var v = speechSynthesis.getVoices().find(function (x) { return /^es/i.test(x.lang); });
      if (v) u.voice = v;
      speechSynthesis.speak(u);
    } catch (e) {}
  };
  A.tono = function (tipo) {
    if (!A.sonidoOn) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      var notas = tipo === "bien" ? [523, 659, 784] : tipo === "suave" ? [392] : tipo === "toque" ? [440 + Math.random() * 300] : [330, 294];
      notas.forEach(function (f, i) {
        var o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime + i * 0.12;
        o.type = "sine"; o.frequency.value = f;
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.15, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.4);
        o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + 0.45);
      });
    } catch (e) {}
  };
  A.celebrar = function (n) {
    var e = ["⭐", "🎉", "✨", "🌟", "💛"];
    for (var i = 0; i < (n || 14); i++) {
      var s = document.createElement("span");
      s.textContent = e[i % e.length];
      s.style.cssText = "position:fixed;z-index:99;pointer-events:none;font-size:" + (28 + Math.random() * 30) + "px;left:" + Math.random() * 100 + "vw;top:100vh;transition:transform 1.6s ease-out,opacity 1.6s";
      document.body.appendChild(s);
      requestAnimationFrame(function (x) { return function () { x.style.transform = "translateY(-" + (60 + Math.random() * 40) + "vh) rotate(" + (Math.random() * 360) + "deg)"; x.style.opacity = "0"; }; }(s));
      setTimeout(function (x) { return function () { x.remove(); }; }(s), 1700);
    }
  };
  A.barajar = function (a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; };
  A.ajustes = function (cont) {
    function boton(txt, on, f) { var b = document.createElement("button"); b.className = "ajuste" + (on ? " on" : ""); b.textContent = txt; b.onclick = function () { f(); b.classList.toggle("on"); }; cont.appendChild(b); }
    boton("🔊 Voz", A.vozOn, function () { A.vozOn = !A.vozOn; localStorage.setItem("incl-voz", A.vozOn ? "si" : "no"); });
    boton("🎵 Sonidos", A.sonidoOn, function () { A.sonidoOn = !A.sonidoOn; localStorage.setItem("incl-sonido", A.sonidoOn ? "si" : "no"); });
  };
  if (window.speechSynthesis) speechSynthesis.onvoiceschanged = function () {};
})();
