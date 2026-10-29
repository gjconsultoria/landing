/* Gabriela Jiménez · Consultoría en comunicación
   Interacciones de la landing. Sin dependencias.
   La página funciona completa sin JavaScript; esto solo suma movimiento.

   1 agenda · 2 medición · 3 cabecera · 4 cortina · 5 revelar · 6 conectores
   7 red viva · 8 tarjetas 3D · 9 botones imantados · 10 capas con el cursor
   11 talleres · 12 cifras */
(function () {
  "use strict";

  var AGENDA = "https://calendar.app.google/MA7J7cr6MwokBeuJ8";
  var WHATSAPP = "573237160686";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finos = window.matchMedia("(pointer: fine)").matches;
  var limita = function (v, a, b) { return v < a ? a : v > b ? b : v; };

  // 1. AGENDA ----------------------------------------------------------
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

  // 3. CABECERA --------------------------------------------------------
  var cabecera = $(".cabecera");
  var nav = $(".nav");
  var marcador = $(".nav__marcador");
  var enlacesNav = $$(".nav__enlaces a");
  var botonSubir = $("[data-subir]");

  var alBajar = function () {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (cabecera) cabecera.classList.toggle("cabecera--flota", y > 20);
    if (botonSubir) botonSubir.classList.toggle("subir--visible", y > 700);
  };
  window.addEventListener("scroll", alBajar, { passive: true });
  alBajar();

  var moverMarcador = function (a) {
    if (!marcador || !nav || !a) return;
    marcador.style.setProperty("--mx", a.offsetLeft + "px");
    marcador.style.setProperty("--mw", a.offsetWidth + "px");
    nav.classList.add("nav--marcado");
  };

  if ("IntersectionObserver" in window && enlacesNav.length) {
    var ioSec = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.id;
        enlacesNav.forEach(function (a) {
          var activo = a.getAttribute("href") === "#" + id;
          a.setAttribute("aria-current", activo ? "true" : "false");
          if (activo) moverMarcador(a);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    ["servicios", "proceso", "talleres", "sobre-mi"].forEach(function (id) {
      var s = document.getElementById(id);
      if (s) ioSec.observe(s);
    });
    enlacesNav.forEach(function (a) {
      a.addEventListener("pointerenter", function () { moverMarcador(a); });
    });
    if (nav) nav.addEventListener("pointerleave", function () {
      var act = $('.nav__enlaces a[aria-current="true"]');
      if (act) moverMarcador(act); else nav.classList.remove("nav--marcado");
    });
  }

  // 4. CORTINA DE HOJAS AL SALTAR DE SECCIÓN ----------------------------
  var cortina = $("[data-cortina]");
  var navegar = function (destino) {
    var el = document.querySelector(destino);
    if (!el) return;
    if (reducido || !cortina) { el.scrollIntoView({ behavior: "auto", block: "start" }); return; }
    cortina.classList.add("cortina--cierra");
    setTimeout(function () {
      el.scrollIntoView({ behavior: "auto", block: "start" });
      setTimeout(function () { cortina.classList.remove("cortina--cierra"); }, 160);
    }, 500);
  };
  $$('.nav__enlaces a, .hero__acciones a[href^="#"], .marca[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var h = a.getAttribute("href");
      if (!h || h.charAt(0) !== "#") return;
      e.preventDefault();
      navegar(h);
    });
  });
  if (botonSubir) {
    botonSubir.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reducido ? "auto" : "smooth" });
    });
  }

  // 5. REVELAR AL ENTRAR EN PANTALLA ------------------------------------
  if ("IntersectionObserver" in window) {
    var ioRev = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("visible"); ioRev.unobserve(en.target); }
      });
    }, { threshold: 0.18, rootMargin: "0px 0px -40px" });
    $$(".revela, .conector, .cifras").forEach(function (el) { ioRev.observe(el); });
  } else {
    $$(".revela, .conector, .cifras").forEach(function (el) { el.classList.add("visible"); });
  }

  // 6. CONECTORES: el hilo se dibuja a medida que la sección se acerca ---
  if (!reducido) {
    var conectores = $$("[data-conector]").map(function (el) {
      return { el: el, luz: $(".conector__luz", el), visible: false, v: -1 };
    });
    if (conectores.length) {
      var pendC = false;
      var pintarConectores = function () {
        pendC = false;
        var alto = window.innerHeight || 1;
        conectores.forEach(function (c) {
          if (!c.visible || !c.luz) return;
          var r = c.el.getBoundingClientRect();
          // 0 cuando asoma por abajo, 1 cuando ya pasó el centro
          var p = limita((alto * 0.92 - r.top) / (r.height + alto * 0.34), 0, 1);
          if (Math.abs(p - c.v) < 0.006) return;
          c.v = p;
          c.luz.style.setProperty("--avance", (1 - p).toFixed(3));
        });
      };
      var pedirC = function () { if (!pendC) { pendC = true; requestAnimationFrame(pintarConectores); } };

      if ("IntersectionObserver" in window) {
        var ioCon = new IntersectionObserver(function (ens) {
          ens.forEach(function (en) {
            for (var i = 0; i < conectores.length; i++) {
              if (conectores[i].el === en.target) { conectores[i].visible = en.isIntersecting; break; }
            }
          });
          pedirC();
        }, { rootMargin: "200px 0px" });
        conectores.forEach(function (c) { ioCon.observe(c.el); });
      } else {
        conectores.forEach(function (c) { c.visible = true; });
      }
      window.addEventListener("scroll", pedirC, { passive: true });
      window.addEventListener("resize", pedirC, { passive: true });
      pedirC();
    }
  }

  // 7. LA RED VIVA ------------------------------------------------------
  // Nodos que flotan y se enlazan entre sí cuando están cerca. El cursor
  // los atrae: es la gráfica de la consultoría convertida en conexión.
  if (!reducido) {
    $$("[data-red]").forEach(function (cv) {
      var noche = cv.getAttribute("data-red") === "noche";
      var ctx = cv.getContext && cv.getContext("2d");
      if (!ctx) return;

      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = 0, h = 0, nodos = [], activo = false;
      var raton = { x: -9999, y: -9999 };
      var DIST = 0;

      var tintas = noche
        ? ["rgba(126,211,107,", "rgba(217,240,140,", "rgba(31,163,138,"]
        : ["rgba(14,107,72,", "rgba(31,163,138,", "rgba(126,211,107,", "rgba(43,45,143,"];

      var medir = function () {
        var r = cv.getBoundingClientRect();
        w = Math.max(1, r.width); h = Math.max(1, r.height);
        cv.width = w * dpr; cv.height = h * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        DIST = Math.min(190, Math.max(110, w * 0.13));
        var cuantos = Math.round(limita((w * h) / 24000, 16, noche ? 34 : 54));
        nodos = [];
        for (var i = 0; i < cuantos; i++) {
          nodos.push({
            x: Math.random() * w, y: Math.random() * h,
            vx: (Math.random() - 0.5) * 0.22, vy: (Math.random() - 0.5) * 0.22,
            r: 1.4 + Math.random() * 2.1,
            t: tintas[i % tintas.length],
            f: Math.random() * Math.PI * 2
          });
        }
      };

      var pintar = function () {
        if (!activo) return;
        ctx.clearRect(0, 0, w, h);

        for (var i = 0; i < nodos.length; i++) {
          var n = nodos[i];
          n.x += n.vx; n.y += n.vy; n.f += 0.01;
          if (n.x < -20) n.x = w + 18; else if (n.x > w + 20) n.x = -18;
          if (n.y < -20) n.y = h + 18; else if (n.y > h + 20) n.y = -18;

          // El cursor atrae suavemente a los nodos cercanos
          var dxm = raton.x - n.x, dym = raton.y - n.y;
          var dm = Math.sqrt(dxm * dxm + dym * dym);
          if (dm < 200 && dm > 0.5) {
            var fuerza = (1 - dm / 200) * 0.5;
            n.x += (dxm / dm) * fuerza;
            n.y += (dym / dm) * fuerza;
          }
        }

        // Enlaces entre nodos cercanos
        for (var a = 0; a < nodos.length; a++) {
          for (var b = a + 1; b < nodos.length; b++) {
            var p = nodos[a], q = nodos[b];
            var dx = p.x - q.x, dy = p.y - q.y;
            var d = Math.sqrt(dx * dx + dy * dy);
            if (d > DIST) continue;
            var fuerzaL = 1 - d / DIST;
            var mx = (p.x + q.x) / 2, my = (p.y + q.y) / 2;
            var dcm = Math.sqrt((raton.x - mx) * (raton.x - mx) + (raton.y - my) * (raton.y - my));
            var cerca = dcm < 240 ? (1 - dcm / 240) : 0;
            var alfa = (noche ? 0.14 : 0.1) * fuerzaL + cerca * fuerzaL * (noche ? 0.5 : 0.42);
            if (alfa < 0.012) continue;
            ctx.strokeStyle = p.t + alfa.toFixed(3) + ")";
            ctx.lineWidth = 0.7 + cerca * 0.9;
            ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
          }
        }

        // Nodos
        for (var k = 0; k < nodos.length; k++) {
          var nn = nodos[k];
          var dxn = raton.x - nn.x, dyn = raton.y - nn.y;
          var dn = Math.sqrt(dxn * dxn + dyn * dyn);
          var halo = dn < 200 ? (1 - dn / 200) : 0;
          var rad = nn.r * (1 + halo * 0.8) + Math.sin(nn.f) * 0.3;
          var alfaN = (noche ? 0.5 : 0.42) + halo * 0.45;
          var g = ctx.createRadialGradient(nn.x, nn.y, 0, nn.x, nn.y, rad * 4.5);
          g.addColorStop(0, nn.t + alfaN.toFixed(3) + ")");
          g.addColorStop(1, nn.t + "0)");
          ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(nn.x, nn.y, rad * 4.5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = nn.t + Math.min(1, alfaN + 0.3).toFixed(3) + ")";
          ctx.beginPath(); ctx.arc(nn.x, nn.y, rad * 0.55, 0, Math.PI * 2); ctx.fill();
        }

        requestAnimationFrame(pintar);
      };

      var encender = function (on) {
        if (on && !activo) { activo = true; requestAnimationFrame(pintar); }
        else if (!on) { activo = false; }
      };

      medir();
      window.addEventListener("resize", medir);
      window.addEventListener("pointermove", function (e) {
        var r = cv.getBoundingClientRect();
        raton.x = e.clientX - r.left;
        raton.y = e.clientY - r.top;
      }, { passive: true });
      window.addEventListener("pointerleave", function () { raton.x = -9999; raton.y = -9999; });
      document.addEventListener("visibilitychange", function () { encender(!document.hidden); });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) { encender(en[0].isIntersecting && !document.hidden); }).observe(cv);
      } else { encender(true); }
    });
  }

  // 8. TARJETAS QUE SE INCLINAN CON EL CURSOR ---------------------------
  if (finos && !reducido) {
    $$("[data-tilt]").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width;
        var py = (e.clientY - r.top) / r.height;
        el.style.setProperty("--ry", ((px - 0.5) * 7).toFixed(2) + "deg");
        el.style.setProperty("--rx", ((0.5 - py) * 6).toFixed(2) + "deg");
        el.style.setProperty("--mx", (px * 100).toFixed(1) + "%");
        el.style.setProperty("--my", (py * 100).toFixed(1) + "%");
      }, { passive: true });
      el.addEventListener("pointerleave", function () {
        el.style.setProperty("--ry", "0deg");
        el.style.setProperty("--rx", "0deg");
      });
    });

    // La retícula de servicios se ilumina alrededor del cursor
    var rejilla = $("[data-rejilla]");
    if (rejilla) {
      rejilla.addEventListener("pointermove", function (e) {
        var r = rejilla.getBoundingClientRect();
        rejilla.style.setProperty("--mx", (e.clientX - r.left) + "px");
        rejilla.style.setProperty("--my", (e.clientY - r.top) + "px");
      }, { passive: true });
    }
  }

  // 9. BOTONES IMANTADOS ------------------------------------------------
  if (finos && !reducido) {
    $$("[data-iman]").forEach(function (el) {
      var dentro = false;
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2);
        var dy = e.clientY - (r.top + r.height / 2);
        el.style.setProperty("--ix", (dx * 0.16).toFixed(1) + "px");
        el.style.setProperty("--iy", (dy * 0.22).toFixed(1) + "px");
        dentro = true;
      }, { passive: true });
      el.addEventListener("pointerleave", function () {
        if (!dentro) return;
        dentro = false;
        el.style.setProperty("--ix", "0px");
        el.style.setProperty("--iy", "0px");
      });
    });
  }

  // 10. CAPAS QUE SE DESPLAZAN CON EL CURSOR ----------------------------
  if (finos && !reducido) {
    var capas = $$(".capa, [data-malla]");
    if (capas.length) {
      var cx = 0, cy = 0, vivo = false;
      var mover = function () {
        capas.forEach(function (c) {
          var fx = parseFloat(c.style.getPropertyValue("--fx"));
          var fy = parseFloat(c.style.getPropertyValue("--fy"));
          if (isNaN(fx)) fx = 26;
          if (isNaN(fy)) fy = 16;
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

  // 11. TALLERES: cambio de ruta ---------------------------------------
  var pestanas = $$(".ruta");
  if (pestanas.length) {
    var abrirRuta = function (clave) {
      pestanas.forEach(function (b) {
        var activa = b.getAttribute("data-ruta") === clave;
        b.setAttribute("aria-selected", activa ? "true" : "false");
        b.tabIndex = activa ? 0 : -1;
      });
      $$("[data-panel]").forEach(function (p) {
        p.hidden = p.getAttribute("data-panel") !== clave;
      });
    };
    pestanas.forEach(function (b) {
      b.addEventListener("click", function () { abrirRuta(b.getAttribute("data-ruta")); });
      b.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        e.preventDefault();
        var i = pestanas.indexOf(b);
        var sig = pestanas[(i + (e.key === "ArrowRight" ? 1 : pestanas.length - 1)) % pestanas.length];
        abrirRuta(sig.getAttribute("data-ruta"));
        sig.focus();
      });
    });
  }

  // 12. CIFRAS QUE CUENTAN ----------------------------------------------
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
