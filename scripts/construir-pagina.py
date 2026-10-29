"""Arma site/index.html.
La página se apoya en la gráfica secundaria de la consultoría: el aura del
logo, los degradados, las hojas vectoriales y los trazos a mano. La idea que
la ordena es la CONEXIÓN: una red viva en la portada, un hilo que enlaza
todas las secciones y tarjetas que reaccionan al cursor.

Uso: python3 scripts/construir-pagina.py
"""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE = os.path.join(RAIZ, "scripts", "_sprite-hojas.html")

AGENDA = "https://calendar.app.google/MA7J7cr6MwokBeuJ8"
WA = "https://wa.me/573237160686?text="
CORREO = "gabrielajimenez.consultoria@gmail.com"
SITIO = "https://gabrielajimenez-consultoria.pages.dev/"
VER = "20261029a"


def hoja(x, y, w, rot, capa=2, forma="hoja-palma", deg="g-selva", ar="3/5"):
    return (f'<div class="hoja hoja--c{capa}" style="--x:{x};--y:{y};--w:{w};--rot:{rot}deg;'
            f'--ar:{ar};--r:url(#{deg})"><div class="hoja__giro">'
            f'<svg class="hoja__svg"><use href="#{forma}" width="100%" height="100%"/></svg>'
            f'</div></div>')


def conector(indice):
    """Hilo que une una sección con la siguiente. Se dibuja al bajar."""
    # Todas las curvas pasan por el punto medio (50, 78): así el nodo cae
    # siempre sobre la línea y el hilo teje de un lado al otro al bajar.
    izq = "M22 0 C22 38 50 46 50 78 C50 110 78 120 78 156"
    der = "M78 0 C78 38 50 46 50 78 C50 110 22 120 22 156"
    d = izq if indice % 2 == 0 else der
    return f'''<div class="conector" aria-hidden="true" data-conector>
  <svg viewBox="0 0 100 156" preserveAspectRatio="none" focusable="false">
    <path class="conector__linea" d="{d}" vector-effect="non-scaling-stroke"/>
    <path class="conector__luz" d="{d}" vector-effect="non-scaling-stroke"/>
  </svg>
  <span class="conector__nodo"></span>
</div>'''


SERVICIOS = [
    ("01", "Diagnóstico y estrategia",
     "Reviso cómo comunicas hoy y definimos un plan claro y medible.",
     "Diagn%C3%B3stico%20y%20estrategia"),
    ("02", "Marca y posicionamiento",
     "Qué te distingue y cómo explicarlo con coherencia en todos tus canales.",
     "Marca%20y%20posicionamiento"),
    ("03", "Narrativa y contenidos",
     "Las historias y los textos que muestran el valor de tu trabajo.",
     "Narrativa%20y%20contenidos"),
    ("04", "Video para redes",
     "Edito el material que tú grabas y lo dejo listo para publicar.",
     "Video%20para%20redes"),
    ("05", "Proyectos y resultados",
     "Avances, memoria e informes para públicos, aliados y financiadores.",
     "Proyectos%20y%20resultados"),
    ("06", "Soluciones digitales e IA",
     "Página web, tableros y flujos sencillos cuando el plan los necesita.",
     "Soluciones%20digitales%20e%20IA"),
]

PASOS = [
    ("Conversamos", "30 minutos gratis para entender tu reto."),
    ("Diagnóstico y propuesta", "Alcance, entregables, tiempos y honorarios por escrito."),
    ("Ejecutamos", "Por proyecto puntual o con acompañamiento mensual."),
]

TALLERES = {
    "contar": {
        "titulo": "Contar para crecer",
        "para": "Emprendimientos, operadores turísticos y asociaciones que quieren mostrar lo que hacen con lo que ya tienen a mano.",
        "modulos": [
            ("Tu historia en tres frases", "Qué haces, para quién y qué te hace distinto.", "Tu presentación lista para publicar"),
            ("Fotos y video con el celular", "Luz, planos, sonido y grabar con respeto.", "Diez fotos o clips propios"),
            ("Edita un video en 20 minutos", "Plantilla de 30 segundos en CapCut gratuito.", "Tu primer video terminado"),
            ("Publica sin agotarte", "Un ritmo realista y tres números que importan.", "Tu calendario de cuatro semanas"),
        ],
    },
    "estrategia": {
        "titulo": "Estrategia en una página",
        "para": "Organizaciones, fundaciones y equipos de proyecto que necesitan ordenar su comunicación y mostrar resultados.",
        "modulos": [
            ("Diagnóstico exprés", "Qué funciona, qué sobra y a quién hablarle primero.", "Tu diagnóstico en una página"),
            ("Mensajes que se entienden", "Un mensaje central y tres por público.", "Tu ficha de mensajes clave"),
            ("Plan de 90 días", "Tres objetivos, seis acciones y responsables.", "Tu plan en hoja editable"),
            ("Muestra tus resultados", "Cinco indicadores y un informe de una página.", "Tu plantilla de informe"),
        ],
    },
}


TERRITORIOS = [
    ("gua-mavecure-rio", "Guainía", "Cerros de piedra sobre el río, en el Guainía"),
    ("ama-raices-ceiba", "Amazonas", "Raíces de un árbol gigante con personas caminando sobre ellas"),
    ("ama-victoria", "Amazonas", "Victorias regias abiertas sobre el agua"),
    ("gua-espejo-rio", "Guainía", "El río como un espejo que refleja las nubes"),
    ("ama-escuela", "Amazonas", "Escuela rural de madera en una comunidad"),
]

CIFRAS = [
    ("3", "años liderando comunicación estratégica"),
    ("25+", "planes de comunicación, del diagnóstico a los resultados"),
    ("47.000+", "reproducciones de pódcast y documentales que lideré"),
    ("+202%", "de crecimiento de comunidad en redes"),
]


def servicios_html():
    out = []
    for i, (num, titulo, texto, asunto) in enumerate(SERVICIOS):
        out.append(f'''        <li class="tarjeta tarjeta--servicio" data-tilt style="--i:{i}">
          <span class="tarjeta__borde" aria-hidden="true"></span>
          <span class="tarjeta__brillo" aria-hidden="true"></span>
          <div class="tarjeta__cuerpo">
            <span class="tarjeta__numero" aria-hidden="true">{num}</span>
            <h3 class="tarjeta__titulo">{titulo}</h3>
            <p class="tarjeta__texto">{texto}</p>
            <a class="tarjeta__enlace" href="{WA}Hola%20Gabriela%2C%20me%20interesa%3A%20{asunto}" target="_blank" rel="noopener" data-evento="whatsapp-servicio">Consultar<span aria-hidden="true">→</span></a>
          </div>
        </li>''')
    return "\n".join(out)


def pasos_html():
    out = []
    for i, (titulo, texto) in enumerate(PASOS, 1):
        out.append(f'''        <li class="paso" style="--i:{i}">
          <span class="paso__nodo" aria-hidden="true"></span>
          <span class="paso__numero" aria-hidden="true">0{i}</span>
          <h3 class="paso__titulo">{titulo}</h3>
          <p class="paso__texto">{texto}</p>
        </li>''')
    return "\n".join(out)


def talleres_html():
    pestanas, paneles = [], []
    for k, (clave, t) in enumerate(TALLERES.items()):
        sel = "true" if k == 0 else "false"
        tab = "" if k == 0 else ' tabindex="-1"'
        pestanas.append(
            f'<button type="button" class="ruta" role="tab" id="tab-{clave}" '
            f'aria-controls="panel-{clave}" aria-selected="{sel}"{tab} data-ruta="{clave}">'
            f'<span class="ruta__punto" aria-hidden="true"></span>{t["titulo"]}</button>')
        mods = "\n".join(
            f'''            <li class="modulo" style="--i:{j}">
              <span class="modulo__num" aria-hidden="true">{j + 1}</span>
              <div>
                <h4 class="modulo__titulo">{m[0]}</h4>
                <p class="modulo__texto">{m[1]}</p>
                <p class="modulo__llevas"><span aria-hidden="true">→</span> {m[2]}</p>
              </div>
            </li>''' for j, m in enumerate(t["modulos"]))
        oculto = "" if k == 0 else " hidden"
        paneles.append(f'''        <div class="panel" id="panel-{clave}" role="tabpanel" aria-labelledby="tab-{clave}" data-panel="{clave}"{oculto}>
          <p class="panel__para">{t["para"]}</p>
          <ul class="modulos">
{mods}
          </ul>
        </div>''')
    return "\n      ".join(pestanas), "\n".join(paneles)


def territorios_html():
    out = []
    for i, (n, lugar, alt) in enumerate(TERRITORIOS):
        srcset = f"/assets/fotos/{n}-600.webp 600w, /assets/fotos/{n}-900.webp 900w"
        out.append(f'''          <figure class="territorio" style="--i:{i}">
            <span class="territorio__marco">
              <img src="/assets/fotos/{n}-600.webp" srcset="{srcset}" sizes="(max-width: 760px) 62vw, 17vw" alt="{alt}" loading="lazy" decoding="async">
            </span>
            <figcaption class="territorio__lugar">{lugar}</figcaption>
          </figure>''')
    return "\n".join(out)


def cifras_html():
    return "\n".join(
        f'''          <li class="cifra" style="--i:{i}"><span class="cifra__valor">{v}</span><span class="cifra__texto">{t}</span></li>'''
        for i, (v, t) in enumerate(CIFRAS))


def construir():
    sprite = open(SPRITE, encoding="utf-8").read()
    pestanas, paneles = talleres_html()

    hero_hojas = "\n".join([
        hoja(-4, 22, 15, 40, capa=1, forma="hoja-palma", deg="g-selva"),
        hoja(104, 16, 16, -44, capa=1, forma="hoja-helecho", deg="g-brote"),
        hoja(-3, 88, 12, -22, capa=2, forma="hoja-ancha", deg="g-luz", ar="10/11"),
        hoja(102, 90, 13, 26, capa=2, forma="hoja-monstera", deg="g-agua", ar="10/11"),
    ])
    cierre_hojas = "\n".join([
        hoja(-3, 104, 17, 26, capa=3, forma="hoja-monstera", deg="g-sombra", ar="10/11"),
        hoja(13, 109, 12, 12, capa=2, forma="hoja-palma", deg="g-sombra"),
        hoja(103, 106, 18, -28, capa=3, forma="hoja-palma", deg="g-sombra"),
        hoja(85, 110, 10, -18, capa=2, forma="hoja-lanza", deg="g-sombra", ar="1/2"),
    ])

    html = f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Comunicación estratégica para organizaciones de Colombia | Gabriela Jiménez</title>
<meta name="description" content="Consultoría de comunicación para pequeñas empresas, organizaciones, fundaciones y cooperativas de los territorios de Colombia. Diagnóstico, estrategia, narrativa, video, proyectos y talleres prácticos. Primera conversación gratuita de 30 minutos.">
<link rel="canonical" href="{SITIO}">
<meta name="theme-color" content="#F4F6F3">
<meta name="robots" content="index, follow">
<meta name="google-site-verification" content="6ZMTMDRqHVKUnYCg9Wx8z4b2x_3A3JN_dlIWpXBCIWk" />
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Gabriela Jiménez · Consultoría en comunicación">
<meta property="og:title" content="Comunicación que hace visible tu trabajo">
<meta property="og:description" content="Acompaño a pequeñas empresas, organizaciones, fundaciones y cooperativas de los territorios de Colombia. Primera conversación gratuita de 30 minutos.">
<meta property="og:url" content="{SITIO}">
<meta property="og:image" content="{SITIO}og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500&amp;display=swap">
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D3C7HSLH9T"></script>
<script src="/assets/main.js?v={VER}" defer></script>
<!-- Cloudflare Web Analytics (sin cookies, sin datos personales) -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "8e3493f7ea244f278128128fefcb5674"}}'></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Gabriela Jiménez · Consultoría en comunicación",
  "description": "Consultoría independiente de comunicación estratégica para pequeñas empresas, organizaciones, fundaciones y cooperativas de los territorios de Colombia.",
  "url": "{SITIO}",
  "email": "{CORREO}",
  "image": "{SITIO}og-image.jpg",
  "priceRange": "Según el alcance de cada proyecto",
  "founder": {{ "@type": "Person", "name": "Gabriela Jiménez", "jobTitle": "Comunicadora corporativa" }},
  "address": {{ "@type": "PostalAddress", "addressCountry": "CO" }},
  "areaServed": {{ "@type": "Country", "name": "Colombia" }},
  "knowsLanguage": ["es"],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Servicios de comunicación estratégica",
    "itemListElement": [
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Diagnóstico y estrategia de comunicación" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Marca y posicionamiento" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Narrativa y contenidos" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Edición de video para redes" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Comunicación de proyectos y resultados" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Soluciones digitales e inteligencia artificial" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Talleres prácticos de comunicación" }} }}
    ]
  }}
}}
</script>
</head>
<body>
{sprite}
<div class="grano" aria-hidden="true"></div>
<div class="cortina" aria-hidden="true" data-cortina><span class="cortina__pano cortina__pano--izq"></span><span class="cortina__pano cortina__pano--der"></span><span class="cortina__aura"></span></div>
<a class="saltar" href="#contenido">Saltar al contenido</a>

<header class="cabecera" id="inicio">
  <div class="cabecera__barra">
    <a class="marca" href="#inicio" aria-label="Gabriela Jiménez, inicio">
      <span class="marca__aura" aria-hidden="true"></span>
      <span class="marca__nombre">Gabriela Jiménez</span>
    </a>
    <nav class="nav" aria-label="Secciones">
      <ul class="nav__enlaces">
        <li><a href="#servicios">Servicios</a></li>
        <li><a href="#proceso">Cómo trabajo</a></li>
        <li><a href="#talleres">Talleres</a></li>
        <li><a href="#sobre-mi">Sobre mí</a></li>
      </ul>
      <span class="nav__marcador" aria-hidden="true"></span>
    </nav>
    <a class="btn btn--oscuro btn--chico iman" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-cabecera" data-iman>Hablemos</a>
  </div>
</header>

<main id="contenido">

<!-- 1. PORTADA: la red viva -->
<section class="hero" aria-labelledby="hero-titulo">
  <div class="hero__fondo" aria-hidden="true">
    <div class="malla" data-malla>
      <span class="malla__mancha malla__mancha--1"></span>
      <span class="malla__mancha malla__mancha--2"></span>
      <span class="malla__mancha malla__mancha--3"></span>
    </div>
    <canvas class="red" data-red></canvas>
    <div class="capa capa--hojas" style="--fx:-22; --fy:-12">
{hero_hojas}
    </div>
    <div class="hero__aura anim-respira"></div>
  </div>

  <div class="envoltura hero__contenido">
    <p class="etiqueta entra entra--1"><span class="etiqueta__pin" aria-hidden="true"></span>Colombia · remoto y en territorio</p>
    <h1 id="hero-titulo" class="titulo-1 entra entra--2">Comunicación que <em>conecta</em> tu trabajo con las personas adecuadas</h1>
    <p class="hero__bajada entra entra--3">Acompaño a pequeñas empresas, organizaciones, fundaciones y cooperativas de los territorios de Colombia.</p>
    <div class="hero__acciones entra entra--4">
      <a class="btn btn--oscuro iman" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-hero" data-iman>Agendar 30 minutos gratis</a>
      <a class="btn btn--borde iman" href="#servicios" data-iman>Ver servicios</a>
    </div>
    <p class="hero__pie entra entra--4" aria-hidden="true">Mueve el cursor: así se ve una red que conecta</p>
  </div>
</section>

{conector(0)}

<!-- 2. SERVICIOS -->
<section class="seccion servicios" id="servicios" aria-labelledby="servicios-titulo">
  <div class="envoltura">
    <div class="seccion__cabeza revela">
      <p class="seccion__eco" aria-hidden="true">Servicios</p>
      <h2 id="servicios-titulo" class="titulo-2">En qué puedo ayudarte</h2>
      <p class="seccion__bajada">El alcance lo definimos juntos en la primera conversación.</p>
    </div>
    <ul class="rejilla-conectada revela" data-rejilla>
{servicios_html()}
    </ul>
  </div>
</section>

{conector(1)}

<!-- 3. CÓMO TRABAJO -->
<section class="seccion proceso" id="proceso" aria-labelledby="proceso-titulo">
  <div class="envoltura">
    <div class="seccion__cabeza revela">
      <p class="seccion__eco" aria-hidden="true">Proceso</p>
      <h2 id="proceso-titulo" class="titulo-2">Cómo trabajo</h2>
      <p class="seccion__bajada">Tres pasos, sin vueltas.</p>
    </div>
    <div class="proceso__hilo revela" data-proceso>
      <span class="proceso__linea" aria-hidden="true"></span>
      <ol class="pasos">
{pasos_html()}
      </ol>
    </div>
  </div>
</section>

{conector(2)}

<!-- 4. TALLERES -->
<section class="seccion talleres" id="talleres" aria-labelledby="talleres-titulo">
  <div class="envoltura">
    <div class="seccion__cabeza revela">
      <p class="seccion__eco" aria-hidden="true">Talleres</p>
      <h2 id="talleres-titulo" class="titulo-2">Aprende y termina con algo hecho</h2>
      <p class="seccion__bajada">Talleres virtuales. Cada módulo dura 2 horas y termina con un entregable. Elige 2 módulos, o los 4 con 10&nbsp;% de descuento.</p>
    </div>

    <div class="rutas revela">
      <div class="rutas__pestanas" role="tablist" aria-label="Rutas de taller">
      {pestanas}
      </div>
{paneles}
      <div class="rutas__pie">
        <p>Incluye plantillas editables y una sesión de seguimiento gratuita de 30 minutos.</p>
        <a class="btn btn--borde btn--chico iman" href="{WA}Hola%20Gabriela%2C%20quiero%20informaci%C3%B3n%20de%20los%20talleres." target="_blank" rel="noopener" data-evento="whatsapp-talleres" data-iman>Consultar talleres</a>
      </div>
    </div>
  </div>
</section>

{conector(3)}

<!-- 5. SOBRE MÍ -->
<section class="seccion sobre" id="sobre-mi" aria-labelledby="sobre-titulo">
  <div class="envoltura">
    <div class="sobre__rejilla">
      <figure class="retrato revela">
        <span class="retrato__anillo" aria-hidden="true"></span>
        <span class="retrato__marco">
          <img src="/assets/gabriela-920.webp" srcset="/assets/gabriela-560.webp 560w, /assets/gabriela-920.webp 920w" sizes="(max-width: 860px) 62vw, 300px" width="920" height="920" alt="Gabriela Jiménez en campo" loading="lazy" decoding="async">
        </span>
      </figure>
      <div class="sobre__texto revela">
        <p class="seccion__eco" aria-hidden="true">Sobre mí</p>
        <h2 id="sobre-titulo" class="titulo-2">Soy Gabriela Jiménez</h2>
        <p class="parrafo-destacado">Comunicadora corporativa. He liderado la comunicación de proyectos de innovación, cooperación internacional, cultura y desarrollo rural.</p>
        <p>Trabajo escuchando primero: entiendo el contexto y construyo con cada organización, no por encima de ella.</p>
      </div>
    </div>
    <ul class="cifras revela" aria-label="Experiencia en cifras">
{cifras_html()}
    </ul>

    <div class="territorios revela" data-territorios>
      <p class="territorios__linea">Territorios que he recorrido</p>
      <div class="territorios__fotos">
{territorios_html()}
      </div>
    </div>
  </div>
</section>

{conector(4)}

<!-- 6. CONTACTO -->
<section class="seccion cierre" id="contacto" aria-labelledby="cierre-titulo">
  <div class="cierre__fondo" aria-hidden="true">
    <canvas class="red red--noche" data-red="noche"></canvas>
    <div class="cierre__aura"><span class="aura-logo anim-respira"></span></div>
    <div class="capa capa--hojas" style="--fx:-20; --fy:-10">
{cierre_hojas}
    </div>
  </div>
  <div class="envoltura cierre__contenido">
    <h2 id="cierre-titulo" class="titulo-1">Hablemos 30 minutos</h2>
    <p class="cierre__bajada">Sin costo. Revisamos tu necesidad y te digo si puedo ayudarte.</p>
    <div class="cierre__opciones">
      <a class="opcion opcion--principal iman" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-cierre" data-iman>
        <span class="opcion__titulo">Agendar videollamada</span>
        <span class="opcion__accion" data-agenda-accion>Ver horarios</span>
      </a>
      <a class="opcion iman" href="{WA}Hola%20Gabriela%2C%20quiero%20conversar%20sobre%20la%20comunicaci%C3%B3n%20de%20mi%20organizaci%C3%B3n." target="_blank" rel="noopener" data-evento="whatsapp-cierre" data-iman>
        <span class="opcion__titulo">Escribir por WhatsApp</span>
        <span class="opcion__accion">Abrir WhatsApp</span>
      </a>
      <a class="opcion iman" href="mailto:{CORREO}?subject=Conversaci%C3%B3n%20sobre%20comunicaci%C3%B3n" data-evento="correo-cierre" data-iman>
        <span class="opcion__titulo">Enviar un correo</span>
        <span class="opcion__accion">{CORREO}</span>
      </a>
    </div>
  </div>
</section>
</main>

<footer class="pie">
  <div class="envoltura pie__contenido">
    <a class="marca marca--pie" href="#inicio">
      <span class="marca__aura" aria-hidden="true"></span>
      <span class="marca__nombre">Gabriela Jiménez</span>
    </a>
    <p class="pie__nota">Consultoría independiente de comunicación estratégica · Colombia · © 2026</p>
  </div>
</footer>

<div class="barra-movil">
  <a class="btn btn--borde btn--chico" href="{WA}Hola%20Gabriela%2C%20quiero%20conversar%20sobre%20la%20comunicaci%C3%B3n%20de%20mi%20organizaci%C3%B3n." target="_blank" rel="noopener" data-evento="whatsapp-barra">WhatsApp</a>
  <a class="btn btn--oscuro btn--chico" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-barra">Agendar gratis</a>
</div>

<button class="subir" type="button" data-subir aria-label="Volver arriba"><span aria-hidden="true">↑</span></button>
</body>
</html>
'''
    salida = os.path.join(RAIZ, "site", "index.html")
    open(salida, "w", encoding="utf-8").write(html)
    print(f"index.html: {len(html)} caracteres")


if __name__ == "__main__":
    construir()
