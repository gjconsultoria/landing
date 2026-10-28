/* Gabriela Jiménez · Consultoría en comunicación
   Interacciones de la landing. Sin dependencias.
   Todo funciona sin JavaScript; este archivo solo suma interacción y movimiento. */
(function () {
  "use strict";

  // ---------------------------------------------------------------------------
  // CONFIGURACIÓN: cuando exista la página de citas de Google Calendar,
  // pega aquí su enlace (por ejemplo https://calendar.app.google/xxxx).
  // Página de citas de Google Calendar (30 min). Si se vacía, «Agendar» abre WhatsApp.
  // ---------------------------------------------------------------------------
  var AGENDA_URL = "https://calendar.app.google/MA7J7cr6MwokBeuJ8";
  var WHATSAPP = "573237160686";
  var CORREO = "gabrielajimenez.consultoria@gmail.com";

  var wa = function (texto) { return "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(texto); };
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  // 1. Enlaces de agenda --------------------------------------------------------
  var enlaceAgenda = AGENDA_URL || wa("Hola Gabriela, quiero agendar la conversación gratuita de 30 minutos. Mi disponibilidad es: ");
  $$("[data-agenda]").forEach(function (a) {
    a.href = enlaceAgenda;
    a.target = "_blank";
    a.rel = "noopener";
  });
  if (!AGENDA_URL) {
    var accion = $("[data-agenda-accion]");
    if (accion) accion.textContent = "Proponer un horario por WhatsApp";
  }

  // 2. Parallax con el cursor (solo con mouse y sin preferencia de movimiento reducido)
  if (!reducido && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    var raiz = document.documentElement, pendiente = false, x = 0, y = 0;
    window.addEventListener("pointermove", function (e) {
      x = e.clientX / window.innerWidth - 0.5;
      y = e.clientY / window.innerHeight - 0.5;
      if (!pendiente) {
        pendiente = true;
        requestAnimationFrame(function () {
          raiz.style.setProperty("--px", x.toFixed(3));
          raiz.style.setProperty("--py", y.toFixed(3));
          pendiente = false;
        });
      }
    }, { passive: true });
  }

  // 3. Pausar animaciones de secciones fuera de pantalla (ahorra batería y datos)
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) { en.target.classList.toggle("fuera-de-vista", !en.isIntersecting); });
    }, { rootMargin: "120px" });
    $$(".seccion").forEach(function (s) { io.observe(s); });
  }

  // 4. Menú «Hablemos» ------------------------------------------------------------
  var boton = $("[data-hablemos]"), menu = $("#menu-hablemos");
  if (boton && menu) {
    var cerrar = function () { menu.hidden = true; boton.setAttribute("aria-expanded", "false"); };
    boton.addEventListener("click", function (e) {
      e.stopPropagation();
      var abrir = menu.hidden;
      menu.hidden = !abrir;
      boton.setAttribute("aria-expanded", String(abrir));
      if (abrir) { var primero = $("a", menu); if (primero) primero.focus(); }
    });
    document.addEventListener("click", function (e) { if (!menu.hidden && !menu.contains(e.target)) cerrar(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !menu.hidden) { cerrar(); boton.focus(); } });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", cerrar); });
  }

  // 5. «¿Te suena alguna de estas situaciones?» ----------------------------------
  var necesidades = {
    visibles: { titulo: "Que tu trabajo llegue a quien debe conocerlo", texto: "Reviso qué comunicas hoy, a quién y por dónde. Con eso definimos juntos los públicos que más importan, los mensajes que sí se entienden y los canales que vale la pena cuidar.", servicio: "Diagnóstico y estrategia de comunicación", ancla: "#servicios", aura: "conic-gradient(from 0deg, #0E6B48, #1FA38A, #2B2D8F, #7ED36B, #0E6B48)" },
    contar: { titulo: "Historias que muestran lo que logras", texto: "Convierto tus resultados en relatos claros: quiénes participan, qué cambió y por qué importa. Así tus piezas, tu web y tus presentaciones dicen lo mismo y convencen.", servicio: "Narrativa y contenidos con propósito", ancla: "#servicios", aura: "conic-gradient(from 0deg, #F7D84A, #D9F08C, #7ED36B, #1FA38A, #F7D84A)" },
    marca: { titulo: "Una imagen que se reconoce y genera confianza", texto: "Ordeno tu identidad: qué te hace diferente, cómo hablas y cómo te ves. Te quedas con un manual sencillo para que cualquiera de tu equipo lo aplique.", servicio: "Marca y posicionamiento", ancla: "#servicios", aura: "conic-gradient(from 0deg, #C9FFEA, #D9F08C, #FFF6C9, #9FE8D4, #C9FFEA)" },
    cuentas: { titulo: "Resultados claros para quien te apoya", texto: "Preparo informes, memorias y casos que muestran el avance de tu proyecto con indicadores sencillos e historias reales, a partir de la información que me compartes y en el formato que tus aliados esperan.", servicio: "Comunicación de proyectos y resultados", ancla: "#servicios", aura: "conic-gradient(from 0deg, #0E6B48, #7ED36B, #F9E55A, #1FA38A, #0E6B48)" },
    tiempo: { titulo: "Un plan a la medida de tus recursos reales", texto: "Priorizo contigo pocas acciones que sí puedes sostener, te formo para hacerlas y sumamos herramientas e inteligencia artificial que te ahorren horas.", servicio: "Talleres prácticos de comunicación", ancla: "#talleres", aura: "conic-gradient(from 0deg, #9FE8D4, #8EA8FF, #2B2D8F, #1FA38A, #9FE8D4)" },
    vender: { titulo: "Mostrar mejor lo que ofreces", texto: "Afino tu propuesta y la llevamos a los canales donde te buscan: WhatsApp Business, Google y tus redes, con fotos y videos hechos con tu celular.", servicio: "Taller Contar para crecer", ancla: "#talleres", aura: "conic-gradient(from 0deg, #7ED36B, #F7D84A, #FF6A3D, #FF4F9A, #7ED36B)" }
  };
  var grupo = $("[data-necesidades]");
  if (grupo) {
    var cuerpo = $("[data-respuesta]"), aura = $("[data-aura]");
    var pintar = function (id, boton) {
      var n = necesidades[id]; if (!n) return;
      $$(".necesidad", grupo).forEach(function (b) { b.setAttribute("aria-pressed", String(b === boton)); });
      $("[data-r-titulo]").textContent = n.titulo;
      $("[data-r-texto]").textContent = n.texto;
      var s = $("[data-r-servicio]"); s.textContent = n.servicio; s.href = n.ancla;
      $("[data-r-wa]").href = wa("Hola Gabriela, en mi organización nos pasa esto: " + boton.textContent.trim().toLowerCase() + ". Me gustaría conversar.");
      aura.style.background = n.aura;
      cuerpo.classList.remove("es-cambio"); void cuerpo.offsetWidth; cuerpo.classList.add("es-cambio");
    };
    $$(".necesidad", grupo).forEach(function (b) { b.addEventListener("click", function () { pintar(b.dataset.id, b); }); });
    var inicial = $(".necesidad[aria-pressed='true']", grupo); if (inicial) pintar(inicial.dataset.id, inicial);
  }

  // 6. Cómo trabajo ----------------------------------------------------------------
  var pasos = {
    1: { duracion: "Gratis · 30 minutos", titulo: "Una conversación para entender tu reto", texto: "Me cuentas qué hace tu organización, a quién quieres llegar y qué te preocupa hoy de tu comunicación. Es para conocernos y ver por dónde empezar, no una asesoría. Por videollamada.", resultado: "Claridad sobre si puedo ayudarte y por dónde convendría empezar." },
    2: { duracion: "Primer paso del trabajo", titulo: "Un diagnóstico de lo que funciona y lo que falta", texto: "Reviso tus canales, públicos, mensajes y recursos, y converso con tu equipo. Miro tu organización desde afuera, como la ven tus clientes y aliados.", resultado: "Un diagnóstico claro, con las prioridades ordenadas." },
    3: { duracion: "Propuesta a la medida", titulo: "Una propuesta con objetivos y prioridades", texto: "Definimos qué lograr, qué hacer primero y con qué recursos. La propuesta detalla alcance, entregables, tiempos y honorarios, sin paquetes que no necesitas.", resultado: "Un plan acordado, con objetivos medibles y un cronograma realista." },
    4: { duracion: "Ejecución conjunta", titulo: "Construimos juntos y tu equipo aprende", texto: "Ejecuto las piezas, estrategias y herramientas, y te involucro en cada decisión para que la comunicación quede instalada en tu organización.", resultado: "Piezas, herramientas y capacidades que se quedan contigo." },
    5: { duracion: "Seguimiento", titulo: "Revisamos los avances y ajustamos", texto: "Medimos con indicadores sencillos qué funcionó y qué no, y ajustamos el camino. Si hay una necesidad recurrente, seguimos acompañándote.", resultado: "Aprendizajes concretos y los siguientes pasos definidos." }
  };
  var listaPasos = $("[data-pasos]");
  if (listaPasos) {
    var detalle = $(".detalle-paso");
    $$(".paso", listaPasos).forEach(function (b) {
      b.addEventListener("click", function () {
        var p = pasos[b.dataset.paso]; if (!p) return;
        $$(".paso", listaPasos).forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        var dur = $("[data-p-duracion]");
        dur.textContent = p.duracion;
        dur.classList.toggle("etiqueta--calida", b.dataset.paso === "1");
        $("[data-p-titulo]").textContent = p.titulo;
        $("[data-p-texto]").textContent = p.texto;
        $("[data-p-resultado]").textContent = p.resultado;
        $("[data-p-acciones]").hidden = b.dataset.paso !== "1";
        detalle.classList.remove("es-cambio"); void detalle.offsetWidth; detalle.classList.add("es-cambio");
      });
    });
  }

  // 7. Talleres: carpetas y módulos ------------------------------------------------
  var talleres = $("[data-talleres]");
  if (talleres) {
    var nombres = { contar: "Contar para crecer: narrativa y contenidos con el celular", estrategia: "Comunicación estratégica en una página" };
    var pestanas = $$("[role='tab']", talleres);
    var linkWa = $("[data-taller-wa]"), linkCorreo = $("[data-taller-correo]");
    var activo = function () { return $("[role='tab'][aria-selected='true']", talleres).dataset.taller; };
    var actualizar = function () {
      var id = activo(), panel = $("[data-panel='" + id + "']", talleres);
      var marcados = $$("input:checked", panel).map(function (i) { return i.dataset.modulo; });
      var n = marcados.length, horas = n * 2, completo = n === 4;
      $("[data-horas]", panel).textContent = horas;
      $("[data-resumen]", panel).textContent = n + (n === 1 ? " módulo" : " módulos") + (completo ? " · 10 % dto." : "");
      var paquete = completo ? " Me interesan los 4 módulos con el 10 % de descuento." : "";
      var texto = "Hola Gabriela, me interesa el taller «" + nombres[id] + "» (" + horas + " horas) con los módulos: " + marcados.join(", ") + "." + paquete + " Somos [número] personas.";
      linkWa.href = wa(texto);
      linkCorreo.href = "mailto:" + CORREO + "?subject=" + encodeURIComponent("Taller: " + nombres[id]) + "&body=" + encodeURIComponent(texto);
    };
    var elegir = function (tab) {
      pestanas.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        $("#" + t.getAttribute("aria-controls")).hidden = !on;
      });
      actualizar();
    };
    pestanas.forEach(function (t, i) {
      t.addEventListener("click", function () { elegir(t); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown" || e.key === "ArrowRight" || e.key === "ArrowUp" || e.key === "ArrowLeft") {
          e.preventDefault();
          var sig = pestanas[(i + (e.key === "ArrowDown" || e.key === "ArrowRight" ? 1 : pestanas.length - 1)) % pestanas.length];
          sig.focus(); elegir(sig);
        }
      });
    });
    $$("input[type='checkbox']", talleres).forEach(function (c) {
      c.addEventListener("change", function () {
        var panel = c.closest("[data-panel]");
        if (!c.checked && $$("input:checked", panel).length === 0) { c.checked = true; } // al menos un módulo
        actualizar();
      });
    });
    actualizar();
  }

  // 8. Botón «volver arriba» -------------------------------------------------------
  var subir = $("[data-subir]");
  if (subir) {
    var verSubir = function () { subir.classList.toggle("visible", window.scrollY > 600); };
    window.addEventListener("scroll", verSubir, { passive: true });
    verSubir();
    subir.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reducido ? "auto" : "smooth" });
      var inicio = $("#inicio"); if (inicio) inicio.focus({ preventScroll: true });
    });
  }

  // 9. Medición: Google Analytics 4 + eventos de conversión ----------------------
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== "function") {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }
  window.gtag("js", new Date());
  window.gtag("config", "G-D3C7HSLH9T");

  var medir = function (evento, params) {
    try {
      params = params || {};
      window.dataLayer.push(Object.assign({ event: evento }, params));
      if (typeof window.gtag === "function") window.gtag("event", evento, params);
    } catch (e) {}
  };
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a, button") : null;
    if (!a) return;
    var ev = a.getAttribute("data-evento") || "";
    if (a.hasAttribute("data-agenda") || /agenda/.test(ev)) {
      medir("agenda_click", { ubicacion: ev || "agenda" });
    } else if (/whatsapp/.test(ev) || (a.href && a.href.indexOf("wa.me") > -1)) {
      medir("whatsapp_click", { ubicacion: ev || "whatsapp" });
    } else if (a.href && a.href.indexOf("mailto:") === 0) {
      medir("correo_click", { ubicacion: ev || "correo" });
    }
  }, true);

  // ===========================================================================
  // Universo «Dosel»: la selva reacciona a la persona
  // ===========================================================================
  var conMouse = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var ancho = function () { return window.innerWidth; };
  var hero = $(".hero");

  // 10. Trazos, liana y río se dibujan al entrar en pantalla ----------------------
  if (!reducido && "IntersectionObserver" in window) {
    var dibujables = $$(".retrato, .metodo__ruta, .recorrido");
    dibujables.forEach(function (el) { el.classList.add("por-dibujar"); });
    var ioDibujo = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.remove("por-dibujar"); ioDibujo.unobserve(en.target); }
      });
    }, { threshold: 0.35 });
    dibujables.forEach(function (el) { ioDibujo.observe(el); });
  }

  // 11. Cabecera flotante y marcador de la sección visible ------------------------
  var cabecera = $(".cabecera");
  var flotar = function () { cabecera.classList.toggle("cabecera--flota", window.scrollY > 40); };
  window.addEventListener("scroll", flotar, { passive: true });
  flotar();

  var enlacesNav = $$(".nav__enlaces a");
  var marcador = document.createElement("span");
  marcador.className = "nav__marcador";
  marcador.setAttribute("aria-hidden", "true");
  var listaNav = $(".nav__enlaces");
  if (listaNav) listaNav.appendChild(marcador);
  var marcar = function (id) {
    var actual = null;
    enlacesNav.forEach(function (a) {
      var on = a.getAttribute("href") === "#" + id;
      if (on) { a.setAttribute("aria-current", "true"); actual = a; } else { a.removeAttribute("aria-current"); }
    });
    if (actual) {
      var li = actual.parentNode;
      marcador.style.width = actual.offsetWidth + "px";
      marcador.style.transform = "translateX(" + (li.offsetLeft) + "px)";
      marcador.classList.add("visible");
    } else {
      marcador.classList.remove("visible");
    }
  };

  // 12. Riel: un tallo que crece y nudos para saltar entre secciones ---------------
  var secciones = $$("main > section");
  var riel = $("[data-riel]"), brote = $("[data-riel-brote]");
  var nudos = [];
  if (riel) {
    secciones.forEach(function (sec) {
      var titulo = $("h1, h2", sec);
      var b = document.createElement("button");
      b.type = "button"; b.className = "riel__nudo"; b.tabIndex = -1;
      var n = document.createElement("span"); n.className = "riel__nombre";
      n.textContent = titulo ? titulo.textContent.trim() : "";
      b.appendChild(n);
      b.addEventListener("click", function () { navegar(sec); });
      riel.appendChild(b);
      nudos.push(b);
    });
  }
  var ubicarNudos = function () {
    var total = document.documentElement.scrollHeight - window.innerHeight;
    secciones.forEach(function (sec, i) {
      if (nudos[i]) nudos[i].style.top = (Math.min(1, Math.max(0, sec.offsetTop / total)) * 100) + "%";
    });
  };
  var alDesplazar = function () {
    var total = document.documentElement.scrollHeight - window.innerHeight;
    var avance = total > 0 ? window.scrollY / total : 0;
    if (brote) brote.style.setProperty("--avance", avance.toFixed(4));
    if (riel) riel.classList.toggle("visible", window.scrollY > window.innerHeight * 0.5);
    // sección visible: la que cruza la mitad de la pantalla
    var mitad = window.scrollY + window.innerHeight * 0.45, visible = secciones[0];
    secciones.forEach(function (sec) { if (sec.offsetTop <= mitad) visible = sec; });
    nudos.forEach(function (b, i) { b.classList.toggle("activo", secciones[i] === visible); });
    var noche = $(".contacto");
    if (noche && cabecera) { var rn = noche.getBoundingClientRect(); cabecera.classList.toggle("cabecera--noche", rn.top < 50 && rn.bottom > 50); }
    marcar(visible ? visible.id : "");
  };
  window.addEventListener("scroll", alDesplazar, { passive: true });
  window.addEventListener("resize", function () { ubicarNudos(); alDesplazar(); });
  window.addEventListener("load", function () { ubicarNudos(); alDesplazar(); });
  ubicarNudos(); alDesplazar();

  // 13. Cortina de hojas: cierra, salta a la sección y se abre --------------------
  var cortina = $("[data-cortina]"), enCortina = false;
  function navegar(destino) {
    if (!destino) return;
    var ir = function () {
      var y = destino.getBoundingClientRect().top + window.scrollY - (destino.classList.contains("hero") ? 0 : 76);
      window.scrollTo({ top: y, behavior: "auto" });
      if (destino.id && history.replaceState) history.replaceState(null, "", "#" + destino.id);
      if (!destino.hasAttribute("tabindex")) destino.setAttribute("tabindex", "-1");
      destino.focus({ preventScroll: true });
    };
    if (reducido || !cortina || enCortina) { ir(); return; }
    enCortina = true;
    cortina.classList.remove("abre");
    cortina.classList.add("cierra");
    setTimeout(function () {
      document.documentElement.style.scrollBehavior = "auto";
      ir();
      document.documentElement.style.scrollBehavior = "";
      cortina.classList.add("abre");
      cortina.classList.remove("cierra");
      setTimeout(function () { cortina.classList.remove("abre"); enCortina = false; }, 820);
    }, 700);
  }
  $$(".nav__enlaces a, .pie__enlaces a, .pie .marca, .nav .marca").forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = (a.getAttribute("href") || "").slice(1);
      var destino = id === "inicio" ? hero : document.getElementById(id);
      if (!destino) return;
      e.preventDefault();
      navegar(destino);
    });
  });

  // 14. Acordeón de servicios ---------------------------------------------------
  var acordeon = $("[data-acordeon]");
  if (acordeon) {
    acordeon.classList.add("acordeon");
    var tarjetas = $$(".servicio", acordeon);
    var activar = function (t) {
      tarjetas.forEach(function (o) {
        var on = o === t;
        o.classList.toggle("activo", on);
        var b = $(".servicio__abrir", o); if (b) b.setAttribute("aria-expanded", String(on));
        var c = $(".servicio__cuerpo", o); if (c) c.inert = !on;
      });
    };
    var espera = null;
    tarjetas.forEach(function (t) {
      t.addEventListener("click", function (e) {
        if (t.classList.contains("activo")) return;
        if (e.target.closest("a, summary")) return;
        activar(t);
      });
      if (conMouse) {
        t.addEventListener("pointerenter", function () {
          if (ancho() <= 1080) return;
          clearTimeout(espera);
          espera = setTimeout(function () { activar(t); }, 160);
        });
        t.addEventListener("pointerleave", function () { clearTimeout(espera); });
      }
    });
    activar(tarjetas[0]);
  }

  // 15. Reflejo que sigue al cursor y botones magnéticos ---------------------------
  $$(".tarjeta-vidrio, .folio, .cifra, .con-quien").forEach(function (el) { el.classList.add("reflejo"); });
  if (conMouse && !reducido) {
    document.addEventListener("pointermove", function (e) {
      var t = e.target.closest ? e.target.closest(".reflejo, .opcion-grande") : null;
      if (t) {
        var r = t.getBoundingClientRect();
        t.style.setProperty("--mx", (e.clientX - r.left) + "px");
        t.style.setProperty("--my", (e.clientY - r.top) + "px");
      }
      var b = e.target.closest ? e.target.closest(".btn") : null;
      if (b) {
        var rb = b.getBoundingClientRect();
        var ox = e.clientX - rb.left, oy = e.clientY - rb.top;
        b.style.setProperty("--bx", ox + "px");
        b.style.setProperty("--by", oy + "px");
        b.style.setProperty("--mx-b", ((ox / rb.width - 0.5) * 8).toFixed(1) + "px");
        b.style.setProperty("--my-b", ((oy / rb.height - 0.5) * 6).toFixed(1) + "px");
      }
    }, { passive: true });
    document.addEventListener("pointerout", function (e) {
      var b = e.target.closest ? e.target.closest(".btn") : null;
      if (b && !b.contains(e.relatedTarget)) { b.style.setProperty("--mx-b", "0px"); b.style.setProperty("--my-b", "0px"); }
    }, { passive: true });
  }

  // 16. El dosel se aparta del cursor y la luciérnaga lo sigue ------------------------
  var dosel = $("[data-dosel]"), luz = $("[data-luz]");
  if (dosel && hero && conMouse && !reducido) {
    var hojasDosel = $$(".hoja--c2, .hoja--c3", dosel).map(function (h) {
      return { el: $(".hoja__giro", h), capa: h.classList.contains("hoja--c3") ? 3 : 2, cx: 0, cy: 0, a: 0, x: 0, y: 0, ta: 0, tx: 0, ty: 0 };
    });
    var medir2 = function () {
      var top = hero.getBoundingClientRect().top;
      hojasDosel.forEach(function (h) {
        var r = h.el.getBoundingClientRect();
        h.cx = r.left + r.width / 2; h.cy = r.top - top + r.height / 2;
      });
    };
    setTimeout(medir2, 2300);
    window.addEventListener("resize", medir2);
    var cursor = { x: -9999, y: -9999 }, heroVisible = true, corriendo = false;
    var paso = function () {
      var top = hero.getBoundingClientRect().top, quieto = true;
      hojasDosel.forEach(function (h) {
        var dx = h.cx - cursor.x, dy = (h.cy + top) - cursor.y;
        var dist = Math.sqrt(dx * dx + dy * dy), R = h.capa === 3 ? 380 : 300;
        var f = dist < R ? Math.pow(1 - dist / R, 2) : 0;
        var prof = h.capa === 3 ? 26 : 12;
        h.ta = (dx >= 0 ? 1 : -1) * 16 * f;
        h.tx = (dx / (dist || 1)) * 30 * f - (cursor.x / window.innerWidth - 0.5) * prof;
        h.ty = (dy / (dist || 1)) * 20 * f - (cursor.y / window.innerHeight - 0.5) * prof * .6;
        h.a += (h.ta - h.a) * 0.08; h.x += (h.tx - h.x) * 0.08; h.y += (h.ty - h.y) * 0.08;
        if (Math.abs(h.ta - h.a) > 0.05 || Math.abs(h.tx - h.x) > 0.1 || Math.abs(h.ty - h.y) > 0.1) quieto = false;
        h.el.style.setProperty("--inclina", h.a.toFixed(2) + "deg");
        h.el.style.setProperty("--dx", h.x.toFixed(1) + "px");
        h.el.style.setProperty("--dy", h.y.toFixed(1) + "px");
      });
      if (!quieto && heroVisible) requestAnimationFrame(paso); else corriendo = false;
    };
    window.addEventListener("pointermove", function (e) {
      cursor.x = e.clientX; cursor.y = e.clientY;
      if (luz) {
        var r = hero.getBoundingClientRect();
        luz.style.setProperty("--lx", (e.clientX - r.left) + "px");
        luz.style.setProperty("--ly", (e.clientY - r.top) + "px");
      }
      if (!corriendo && heroVisible) { corriendo = true; requestAnimationFrame(paso); }
    }, { passive: true });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { heroVisible = en[0].isIntersecting; }).observe(hero);
    }
  }

  // 17. Polen de día y luciérnagas de noche (canvas liviano) ---------------------------
  var lienzos = $$("[data-polen]");
  lienzos.forEach(function (cv) {
    if (reducido) { cv.remove(); return; }
    var noche = cv.dataset.polen === "noche";
    var ctx = cv.getContext("2d"), dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var W = 0, H = 0, motas = [], activo = false, raton = { x: -999, y: -999 };
    // sprite de brillo pre-renderizado
    var brillo = document.createElement("canvas"); brillo.width = brillo.height = 64;
    var bc = brillo.getContext("2d"), g = bc.createRadialGradient(32, 32, 0, 32, 32, 32);
    if (noche) { g.addColorStop(0, "rgba(255,250,200,1)"); g.addColorStop(.25, "rgba(217,240,140,.9)"); g.addColorStop(1, "rgba(217,240,140,0)"); }
    else { g.addColorStop(0, "rgba(255,255,240,1)"); g.addColorStop(.35, "rgba(247,216,74,.7)"); g.addColorStop(1, "rgba(247,216,74,0)"); }
    bc.fillStyle = g; bc.fillRect(0, 0, 64, 64);
    var preparar = function () {
      var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(noche ? 46 : 60, Math.round(W * H / (noche ? 26000 : 20000)));
      motas = [];
      for (var i = 0; i < n; i++) {
        motas.push({ x: Math.random() * W, y: Math.random() * H, r: (noche ? 6 : 3) + Math.random() * (noche ? 10 : 7), v: .15 + Math.random() * .45,
          f: Math.random() * Math.PI * 2, t: Math.random() * Math.PI * 2, ox: 0, oy: 0 });
      }
    };
    var dibujar = function () {
      if (!activo) return;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < motas.length; i++) {
        var m = motas[i];
        m.f += .01; m.t += noche ? .035 : .02;
        m.y -= m.v * (noche ? .35 : 1);
        m.x += Math.sin(m.f) * (noche ? .6 : .35);
        var dx = m.x - raton.x, dy = m.y - raton.y, d2 = dx * dx + dy * dy;
        if (d2 < 16000) { var k = (1 - d2 / 16000) * 2.2; m.ox += dx / 40 * k; m.oy += dy / 40 * k; }
        m.ox *= .94; m.oy *= .94;
        if (m.y < -20) { m.y = H + 20; m.x = Math.random() * W; }
        var a = noche ? Math.max(0, Math.sin(m.t)) : .45 + .45 * Math.sin(m.t);
        ctx.globalAlpha = a * (noche ? .95 : .75);
        var s = m.r * (noche ? 1 + .3 * Math.sin(m.t * 2) : 1);
        ctx.drawImage(brillo, m.x + m.ox - s, m.y + m.oy - s, s * 2, s * 2);
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(dibujar);
    };
    preparar();
    window.addEventListener("resize", preparar);
    var zona = cv.parentNode.closest("section") || cv.parentNode;
    zona.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); raton.x = e.clientX - r.left; raton.y = e.clientY - r.top; }, { passive: true });
    zona.addEventListener("pointerleave", function () { raton.x = raton.y = -999; });
    var encender = function (on) { if (on && !activo) { activo = true; requestAnimationFrame(dibujar); } else if (!on) { activo = false; } };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { encender(en[0].isIntersecting && !document.hidden); }).observe(cv);
      document.addEventListener("visibilitychange", function () { if (document.hidden) encender(false); else { var r = cv.getBoundingClientRect(); encender(r.bottom > 0 && r.top < window.innerHeight); } });
    } else { encender(true); }
  });

  // 18. Cifras que crecen al aparecer (terminan con el texto exacto) ------------------
  if (!reducido && "IntersectionObserver" in window) {
    var formato = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, "."); };
    var ioCifras = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        ioCifras.unobserve(en.target);
        var el = en.target, final = el.textContent, m = final.match(/^(\D*)([\d.]+)(\D*)$/);
        if (!m) return;
        var meta = parseInt(m[2].replace(/\./g, ""), 10), t0 = null, dur = 1500;
        var cuadro = function (t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
          el.textContent = p < 1 ? m[1] + formato(Math.round(meta * e)) + m[3] : final;
          if (p < 1) requestAnimationFrame(cuadro);
        };
        requestAnimationFrame(cuadro);
      });
    }, { threshold: 0.6 });
    $$(".cifra__valor").forEach(function (el) { ioCifras.observe(el); });
  }

  // 19. VENTANAS AL TERRITORIO ------------------------------------------
  // Cada foto recibe --p: 0 cuando asoma por abajo, .5 en el centro de la
  // pantalla y 1 cuando termina de salir. El CSS convierte ese número en
  // la inclinación. Un solo rAF para todas, y solo mientras se ven.
  if (!reducido) {
    var piezas = [];
    $$(".carril .ventana, [data-franja]").forEach(function (el) { piezas.push({ el: el, visible: false, p: -1 }); });

    if (piezas.length) {
      var pendiente = false;

      var actualizar = function () {
        pendiente = false;
        var alto = window.innerHeight || 1;
        for (var i = 0; i < piezas.length; i++) {
          var it = piezas[i];
          if (!it.visible) continue;
          var r = it.el.getBoundingClientRect();
          var p = (alto - r.top) / (alto + r.height);
          p = p < 0 ? 0 : p > 1 ? 1 : p;
          if (Math.abs(p - it.p) < 0.004) continue;
          it.p = p;
          it.el.style.setProperty("--p", p.toFixed(3));
        }
      };

      var pedir = function () {
        if (!pendiente) { pendiente = true; requestAnimationFrame(actualizar); }
      };

      if ("IntersectionObserver" in window) {
        var ioVent = new IntersectionObserver(function (entradas) {
          entradas.forEach(function (e) {
            for (var i = 0; i < piezas.length; i++) {
              if (piezas[i].el === e.target) { piezas[i].visible = e.isIntersecting; break; }
            }
          });
          pedir();
        }, { rootMargin: "120px 0px" });
        piezas.forEach(function (it) { ioVent.observe(it.el); });
      } else {
        piezas.forEach(function (it) { it.visible = true; });
      }

      window.addEventListener("scroll", pedir, { passive: true });
      window.addEventListener("resize", pedir, { passive: true });
      pedir();
    }

    // Las dos ventanas del hero también se apartan del cursor, como las hojas.
    var marcoHero = $(".hero");
    var ventHero = $$(".ventanas-hero .ventana");
    if (marcoHero && ventHero.length && window.matchMedia("(pointer: fine)").matches) {
      var estado = ventHero.map(function (el) { return { el: el, x: 0, y: 0, tx: 0, ty: 0 }; });
      var vivo = false, verHero = true;

      var pasoVent = function () {
        var quieto = true;
        for (var i = 0; i < estado.length; i++) {
          var v = estado[i];
          v.x += (v.tx - v.x) * 0.07;
          v.y += (v.ty - v.y) * 0.07;
          if (Math.abs(v.tx - v.x) > 0.15 || Math.abs(v.ty - v.y) > 0.15) quieto = false;
          v.el.style.setProperty("--vx", v.x.toFixed(1) + "px");
          v.el.style.setProperty("--p", (0.5 + v.y / 260).toFixed(3));
        }
        if (!quieto && verHero) requestAnimationFrame(pasoVent); else vivo = false;
      };

      window.addEventListener("pointermove", function (e) {
        if (!verHero) return;
        var cx = e.clientX / (window.innerWidth || 1) - 0.5;
        var cy = e.clientY / (window.innerHeight || 1) - 0.5;
        for (var i = 0; i < estado.length; i++) {
          var signo = i % 2 === 0 ? -1 : 1;
          estado[i].tx = cx * 26 * signo;
          estado[i].ty = cy * 20 * signo;
        }
        if (!vivo) { vivo = true; requestAnimationFrame(pasoVent); }
      }, { passive: true });

      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) { verHero = en[0].isIntersecting; }).observe(marcoHero);
      }
    }
  }

})();
