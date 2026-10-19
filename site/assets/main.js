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
  var WHATSAPP = "573219300818";
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
    visibles: { titulo: "Que tu trabajo llegue a quien debe conocerlo", texto: "Revisamos qué comunicas hoy, a quién y por dónde. Con eso definimos los públicos que más importan, los mensajes que sí se entienden y los canales que vale la pena cuidar.", servicio: "Diagnóstico y estrategia de comunicación", ancla: "#servicios", aura: "conic-gradient(from 0deg, #2A6BFF, #8A3FFC, #FF4F9A, #FFB23F, #2A6BFF)" },
    contar: { titulo: "Historias que muestran lo que logras", texto: "Convertimos tus resultados en relatos claros: quiénes participan, qué cambió y por qué importa. Así tus piezas, tu web y tus presentaciones dicen lo mismo y convencen.", servicio: "Narrativa y contenidos con propósito", ancla: "#servicios", aura: "conic-gradient(from 0deg, #FFB23F, #FF6A3D, #E2306D, #F9E55A, #FFB23F)" },
    marca: { titulo: "Una imagen que se reconoce y genera confianza", texto: "Ordenamos tu identidad: qué te hace diferente, cómo hablas y cómo te ves. Te quedas con un manual sencillo para que cualquiera de tu equipo lo aplique.", servicio: "Marca y posicionamiento", ancla: "#servicios", aura: "conic-gradient(from 0deg, #BFF3F0, #E7D8FF, #FFD9EC, #FFF6C9, #BFF3F0)" },
    cuentas: { titulo: "Resultados claros para quien te apoya", texto: "Preparamos informes, memorias y casos que muestran el avance de tu proyecto con indicadores sencillos e historias reales, en el formato que tus aliados esperan.", servicio: "Comunicación de proyectos y resultados", ancla: "#servicios", aura: "conic-gradient(from 0deg, #0E6B48, #7ED36B, #F9E55A, #1FA38A, #0E6B48)" },
    tiempo: { titulo: "Un plan a la medida de tus recursos reales", texto: "Priorizamos pocas acciones que sí puedes sostener, te formo para hacerlas y sumamos herramientas e inteligencia artificial que te ahorren horas.", servicio: "Talleres y soluciones digitales", ancla: "#talleres", aura: "conic-gradient(from 0deg, #9FE8FF, #8EA8FF, #E7D8FF, #C9FFEA, #9FE8FF)" },
    vender: { titulo: "Mostrar mejor lo que ofreces", texto: "Afinamos tu propuesta y la llevamos a los canales donde te buscan: WhatsApp Business, Google y tus redes, con fotos y videos hechos con tu celular.", servicio: "Taller Contar para crecer", ancla: "#talleres", aura: "conic-gradient(from 0deg, #FF4F9A, #FF6A3D, #FFB23F, #7ED36B, #FF4F9A)" }
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
    1: { duracion: "Gratis · 30 minutos", titulo: "Una conversación para entender tu reto", texto: "Me cuentas qué hace tu organización, a quién quieres llegar y qué te preocupa hoy de tu comunicación. Por videollamada, de lunes a viernes de 10 a 12 y de 2 a 4.", resultado: "Claridad sobre si puedo ayudarte y por dónde convendría empezar." },
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
      var horas = marcados.length * 2;
      $("[data-horas]", panel).textContent = horas;
      $("[data-resumen]", panel).textContent = marcados.length + (marcados.length === 1 ? " módulo de 4" : " módulos de 4");
      var texto = "Hola Gabriela, me interesa el taller «" + nombres[id] + "» (" + horas + " horas) con los módulos: " + marcados.join(", ") + ". Somos [número] personas.";
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
})();
