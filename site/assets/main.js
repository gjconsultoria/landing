/* Gabriela Jiménez · Consultoría en comunicación
   Interacciones de la landing. Sin dependencias.
   La página funciona completa sin JavaScript; esto solo suma movimiento. */
(function () {
  "use strict";

  var AGENDA = "https://calendar.app.google/MA7J7cr6MwokBeuJ8";
  var WHATSAPP = "573237160686";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finos = window.matchMedia("(pointer: fine)").matches;

  // 1. AGENDA ----------------------------------------------------------
  // Si algún día no hay página de citas, los botones caen a WhatsApp.
  if (!AGENDA) {
    $$("[data-agenda]").forEach(function (a) {
      a.href = "https://wa.me/" + WHATSAPP + "?text=" +
        encodeURIComponent("Hola Gabriela, quiero agendar una conversación de 30 minutos.");
      a.removeAttribute("target");
      var acc = $("[data-agenda-accion]", a);
      if (acc) acc.textContent = "Escribir por WhatsApp";
    });
  }

  // 2. MEDICIÓN (GA4) --------------------------------------------------
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag("js", new Date());
  gtag("config", "G-D3C7HSLH9T");
  window.gtag = window.gtag || gtag;

  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("[data-evento]") : null;
    if (!a) return;
    var ev = a.getAttribute("data-evento");
    var nombre = ev.indexOf("agenda") === 0 ? "agenda_click"
      : ev.indexOf("whatsapp") === 0 ? "whatsapp_click"
      : ev.indexOf("correo") === 0 ? "correo_click" : "cta_click";
    try { gtag("event", nombre, { origen: ev }); } catch (err) {}
  });

  // 3. CABECERA: flota al bajar y marca la sección visible --------------
  var cabecera = $(".cabecera");
  var enlacesNav = $$(".nav__enlaces a");
  var ultimo = 0;

  var alBajar = function () {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (cabecera) cabecera.classList.toggle("cabecera--flota", y > 20);
    var subir = $("[data-subir]");
    if (subir) subir.classList.toggle("subir--visible", y > 700);
    ultimo = y;
  };
  window.addEventListener("scroll", alBajar, { passive: true });
  alBajar();

  if ("IntersectionObserver" in window && enlacesNav.length) {
    var ioSec = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.id;
        enlacesNav.forEach(function (a) {
          a.setAttribute("aria-current", a.getAttribute("href") === "#" + id ? "true" : "false");
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    ["servicios", "proceso", "sobre-mi"].forEach(function (id) {
      var s = document.getElementById(id);
      if (s) ioSec.observe(s);
    });
  }

  // 4. NAVEGACIÓN CON CORTINA DE HOJAS ---------------------------------
  // El mismo gesto que sirve de entrada y salida para redes.
  var cortina = $("[data-cortina]");
  var navegar = function (destino) {
    var el = document.querySelector(destino);
    if (!el) return;
    if (reducido || !cortina) { el.scrollIntoView({ behavior: "auto", block: "start" }); return; }
    cortina.classList.add("cortina--cierra");
    setTimeout(function () {
      el.scrollIntoView({ behavior: "auto", block: "start" });
      setTimeout(function () { cortina.classList.remove("cortina--cierra"); }, 160);
    }, 520);
  };
  $$('.nav__enlaces a, .hero__acciones a[href^="#"], .marca[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var h = a.getAttribute("href");
      if (!h || h.charAt(0) !== "#") return;
      e.preventDefault();
      navegar(h);
    });
  });

  var subir = $("[data-subir]");
  if (subir) {
    subir.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reducido ? "auto" : "smooth" });
    });
  }

  // 5. SECCIONES QUE SE ENCIENDEN AL ENTRAR ----------------------------
  if ("IntersectionObserver" in window) {
    var ioVis = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("visible"); ioVis.unobserve(en.target); }
      });
    }, { threshold: 0.25 });
    $$(".proceso, .sobre").forEach(function (s) { ioVis.observe(s); });
  } else {
    $$(".proceso, .sobre").forEach(function (s) { s.classList.add("visible"); });
  }

  // 6. FOTOS QUE SE INCLINAN SEGÚN SU LUGAR EN LA PANTALLA --------------
  // --p vale 0 cuando la foto asoma por abajo, .5 en el centro y 1 al salir.
  if (!reducido) {
    var piezas = $$(".carril .ventana, .hero__fotos .ventana, [data-franja]").map(function (el) {
      return { el: el, visible: false, p: -1 };
    });

    if (piezas.length) {
      var pendiente = false;
      var actualizar = function () {
        pendiente = false;
        var alto = window.innerHeight || 1;
        piezas.forEach(function (it) {
          if (!it.visible) return;
          var r = it.el.getBoundingClientRect();
          var p = (alto - r.top) / (alto + r.height);
          p = p < 0 ? 0 : p > 1 ? 1 : p;
          if (Math.abs(p - it.p) < 0.004) return;
          it.p = p;
          it.el.style.setProperty("--p", p.toFixed(3));
        });
      };
      var pedir = function () { if (!pendiente) { pendiente = true; requestAnimationFrame(actualizar); } };

      if ("IntersectionObserver" in window) {
        var ioFoto = new IntersectionObserver(function (entradas) {
          entradas.forEach(function (en) {
            for (var i = 0; i < piezas.length; i++) {
              if (piezas[i].el === en.target) { piezas[i].visible = en.isIntersecting; break; }
            }
          });
          pedir();
        }, { rootMargin: "140px 0px" });
        piezas.forEach(function (it) { ioFoto.observe(it.el); });
      } else {
        piezas.forEach(function (it) { it.visible = true; });
      }

      window.addEventListener("scroll", pedir, { passive: true });
      window.addEventListener("resize", pedir, { passive: true });
      pedir();
    }
  }

  // 7. REFLEJO QUE SIGUE AL CURSOR EN LAS TARJETAS ----------------------
  if (finos && !reducido) {
    $$(".reflejo").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", (e.clientX - r.left) + "px");
        el.style.setProperty("--my", (e.clientY - r.top) + "px");
      }, { passive: true });
    });
  }

  // 8. CAPAS QUE SE DESPLAZAN CON EL CURSOR (hojas y auras) -------------
  if (finos && !reducido) {
    var capas = $$(".capa");
    if (capas.length) {
      var cx = 0, cy = 0, vivo = false;
      var mover = function () {
        capas.forEach(function (c) {
          var fx = parseFloat(c.style.getPropertyValue("--fx")) || 0;
          var fy = parseFloat(c.style.getPropertyValue("--fy")) || 0;
          c.style.transform = "translate3d(" + (cx * fx / 100).toFixed(1) + "px," + (cy * fy / 100).toFixed(1) + "px,0)";
        });
        vivo = false;
      };
      window.addEventListener("pointermove", function (e) {
        cx = e.clientX / (window.innerWidth || 1) - 0.5;
        cy = e.clientY / (window.innerHeight || 1) - 0.5;
        if (!vivo) { vivo = true; requestAnimationFrame(mover); }
      }, { passive: true });
    }
  }

  // 9. POLEN Y LUCIÉRNAGAS ---------------------------------------------
  // Partículas sobre lienzo: se pausan fuera de pantalla y con la pestaña oculta.
  if (!reducido) {
    $$("[data-polen]").forEach(function (cv) {
      var noche = cv.getAttribute("data-polen") === "noche";
      var ctx = cv.getContext && cv.getContext("2d");
      if (!ctx) return;

      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = 0, h = 0, granos = [], activo = false;

      var medir = function () {
        var r = cv.getBoundingClientRect();
        w = Math.max(1, r.width); h = Math.max(1, r.height);
        cv.width = w * dpr; cv.height = h * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        var cuantos = Math.round(Math.min(46, (w * h) / 26000));
        granos = [];
        for (var i = 0; i < cuantos; i++) {
          granos.push({
            x: Math.random() * w, y: Math.random() * h,
            r: noche ? 1.1 + Math.random() * 1.6 : 0.8 + Math.random() * 1.5,
            vx: (Math.random() - 0.5) * 0.17, vy: -0.05 - Math.random() * 0.2,
            f: Math.random() * Math.PI * 2, vf: 0.012 + Math.random() * 0.02
          });
        }
      };

      var pintar = function () {
        if (!activo) return;
        ctx.clearRect(0, 0, w, h);
        for (var i = 0; i < granos.length; i++) {
          var g = granos[i];
          g.x += g.vx; g.y += g.vy; g.f += g.vf;
          if (g.y < -8) { g.y = h + 6; g.x = Math.random() * w; }
          if (g.x < -8) g.x = w + 6; else if (g.x > w + 8) g.x = -6;
          var a = (noche ? 0.4 : 0.32) + Math.sin(g.f) * (noche ? 0.34 : 0.2);
          if (a <= 0) continue;
          var grad = ctx.createRadialGradient(g.x, g.y, 0, g.x, g.y, g.r * 4);
          grad.addColorStop(0, noche ? "rgba(217,240,140," + a + ")" : "rgba(247,216,74," + a + ")");
          grad.addColorStop(1, "rgba(247,216,74,0)");
          ctx.fillStyle = grad;
          ctx.beginPath(); ctx.arc(g.x, g.y, g.r * 4, 0, Math.PI * 2); ctx.fill();
        }
        requestAnimationFrame(pintar);
      };

      var encender = function (on) {
        if (on && !activo) { activo = true; requestAnimationFrame(pintar); }
        else if (!on) { activo = false; }
      };

      medir();
      window.addEventListener("resize", medir);
      document.addEventListener("visibilitychange", function () { encender(!document.hidden); });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) { encender(en[0].isIntersecting && !document.hidden); }).observe(cv);
      } else { encender(true); }
    });
  }

  // 10. CIFRAS QUE CUENTAN AL APARECER ----------------------------------
  if (!reducido && "IntersectionObserver" in window) {
    var ioCifra = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        ioCifra.unobserve(el);
        var m = /^(\D*)([\d.]+)(\D*)$/.exec(el.textContent.trim());
        if (!m) return;
        var pre = m[1], crudo = m[2], post = m[3];
        var fin = parseInt(crudo.replace(/\./g, ""), 10);
        if (!isFinite(fin) || fin === 0) return;
        var miles = crudo.indexOf(".") > -1;
        var t0 = performance.now(), dur = 1100;
        var cuadro = function (t) {
          var p = Math.min(1, (t - t0) / dur);
          var v = Math.round(fin * (1 - Math.pow(1 - p, 3)));
          el.textContent = pre + (miles ? v.toLocaleString("es-CO") : v) + post;
          if (p < 1) requestAnimationFrame(cuadro);
        };
        requestAnimationFrame(cuadro);
      });
    }, { threshold: 0.6 });
    $$(".cifra__valor").forEach(function (el) { ioCifra.observe(el); });
  }
})();
