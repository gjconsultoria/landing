"""Arma site/index.html a partir de la plantilla y el sprite de hojas.
Uso: python3 scripts/construir-pagina.py
"""
import os, random

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE = "/tmp/claude-0/-home-claude/e25420f1-890b-596a-bb6c-070532ca213a/scratchpad/sprite.html"

AGENDA = "https://calendar.app.google/MA7J7cr6MwokBeuJ8"
WA = "https://wa.me/573237160686?text="
CORREO = "gabrielajimenez.consultoria@gmail.com"
SITIO = "https://gabrielajimenez-consultoria.pages.dev/"
VER = "20261028b"

HOJAS = ["hoja-lanza", "hoja-ancha", "hoja-palma", "hoja-helecho", "hoja-monstera"]
DEGRADADOS = ["g-selva", "g-brote", "g-luz", "g-agua", "g-sombra"]


def hoja(x, y, w, rot, capa=2, forma=None, deg=None, ar="3/5", semilla=0):
    """Una hoja decorativa colocada en porcentajes del contenedor."""
    r = random.Random(semilla)
    forma = forma or r.choice(HOJAS)
    deg = deg or r.choice(DEGRADADOS[:4])
    return (f'<div class="hoja hoja--c{capa}" style="--x:{x};--y:{y};--w:{w};--rot:{rot}deg;'
            f'--ar:{ar};--r:url(#{deg})"><div class="hoja__giro">'
            f'<svg class="hoja__svg"><use href="#{forma}" width="100%" height="100%"/></svg>'
            f'</div></div>')


def foto(nombre, alt, sizes, clase="", lazy=True, anchos=(600, 900, 1400)):
    srcset = ", ".join(f"/assets/fotos/{nombre}-{a}.webp {a}w" for a in anchos)
    carga = 'loading="lazy" decoding="async"' if lazy else 'decoding="async" fetchpriority="high"'
    cl = f' class="{clase}"' if clase else ""
    return (f'<img{cl} src="/assets/fotos/{nombre}-900.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{alt}" {carga}>')


SERVICIOS = [
    ("Diagnóstico y estrategia",
     "Reviso cómo comunicas hoy y definimos un plan claro y medible.",
     "g-selva", "Diagn%C3%B3stico%20y%20estrategia"),
    ("Marca y posicionamiento",
     "Qué te distingue y cómo explicarlo con coherencia en todos tus canales.",
     "g-agua", "Marca%20y%20posicionamiento"),
    ("Narrativa y contenidos",
     "Las historias y los textos que muestran el valor de tu trabajo.",
     "g-brote", "Narrativa%20y%20contenidos"),
    ("Video para redes",
     "Edito el material que tú grabas y lo dejo listo para publicar.",
     "g-luz", "Video%20para%20redes"),
    ("Proyectos y resultados",
     "Avances, memoria e informes para públicos, aliados y financiadores.",
     "g-agua", "Proyectos%20y%20resultados"),
    ("Soluciones digitales e IA",
     "Página web, tableros y flujos sencillos cuando el plan los necesita.",
     "g-selva", "Soluciones%20digitales"),
]

PASOS = [
    ("Conversamos", "30 minutos gratis para entender tu reto."),
    ("Diagnóstico y propuesta", "Alcance, entregables, tiempos y honorarios por escrito."),
    ("Ejecutamos", "Por proyecto puntual o con acompañamiento mensual."),
]

CIFRAS = [
    ("3", "años liderando comunicación estratégica"),
    ("25+", "planes de comunicación, del diagnóstico a los resultados"),
    ("47.000+", "reproducciones de pódcast y documentales que lideré"),
    ("+202%", "de crecimiento de comunidad en redes"),
]

CARRIL = [
    ("gua-mavecure-rio", "Cerros de piedra sobre el río, en el Guainía", ""),
    ("ama-raices-ceiba", "Raíces de un árbol gigante con personas caminando sobre ellas", ""),
    ("ama-victoria", "Victorias regias abiertas sobre el agua", ""),
    ("ama-casa-rio", "Casa flotante sobre el río", ""),
    ("ama-escuela", "Escuela rural de madera en una comunidad", ""),
    ("gua-espejo-rio", "El río como un espejo que refleja las nubes", ""),
]


def servicios_html():
    out = []
    for i, (titulo, texto, deg, asunto) in enumerate(SERVICIOS):
        out.append(f'''        <li class="servicio reflejo" style="--acento: var(--c{i % 4 + 1})">
          <span class="servicio__marca" aria-hidden="true"></span>
          <h3 class="servicio__titulo">{titulo}</h3>
          <p class="servicio__texto">{texto}</p>
          <a class="servicio__enlace" href="{WA}Hola%20Gabriela%2C%20me%20interesa%3A%20{asunto}" target="_blank" rel="noopener" data-evento="whatsapp-servicio">Consultar<span aria-hidden="true">→</span></a>
        </li>''')
    return "\n".join(out)


def pasos_html():
    out = []
    for i, (titulo, texto) in enumerate(PASOS, 1):
        out.append(f'''        <li class="paso">
          <span class="paso__numero" aria-hidden="true">{i}</span>
          <h3 class="paso__titulo">{titulo}</h3>
          <p class="paso__texto">{texto}</p>
        </li>''')
    return "\n".join(out)


def cifras_html():
    out = []
    for i, (valor, texto) in enumerate(CIFRAS):
        out.append(f'''          <li class="cifra"><span class="cifra__valor">{valor}</span><span class="cifra__texto">{texto}</span></li>''')
    return "\n".join(out)


def carril_html():
    out = []
    for i, (n, alt, extra) in enumerate(CARRIL):
        rot = [-1.4, 1.2, -0.9, 1.5, -1.2, 0.9][i]
        lado = -1 if i % 2 == 0 else 1
        out.append(f'''        <figure class="ventana{extra}" style="--rot:{rot}deg;--lado:{lado}">{foto(n, alt, "(max-width: 760px) 74vw, 30vw")}</figure>''')
    return "\n".join(out)


def construir():
    sprite = open(SPRITE, encoding="utf-8").read()

    hero_hojas = "\n".join([
        hoja(-3, 24, 14, 38, capa=1, forma="hoja-palma", deg="g-selva", semilla=1),
        hoja(103, 18, 15, -42, capa=1, forma="hoja-helecho", deg="g-brote", semilla=2),
        hoja(-2, 86, 12, -24, capa=2, forma="hoja-ancha", deg="g-luz", ar="10/11", semilla=3),
        hoja(101, 88, 13, 28, capa=2, forma="hoja-monstera", deg="g-agua", ar="10/11", semilla=4),
    ])
    cierre_hojas = "\n".join([
        hoja(-2, 104, 16, 26, capa=3, forma="hoja-monstera", deg="g-sombra", ar="10/11", semilla=5),
        hoja(14, 108, 12, 12, capa=2, forma="hoja-palma", deg="g-sombra", semilla=6),
        hoja(102, 106, 17, -28, capa=3, forma="hoja-palma", deg="g-sombra", semilla=7),
        hoja(86, 109, 10, -18, capa=2, forma="hoja-lanza", deg="g-sombra", ar="1/2", semilla=8),
    ])

    html = f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Comunicación estratégica para organizaciones de Colombia | Gabriela Jiménez</title>
<meta name="description" content="Consultoría de comunicación para pequeñas empresas, organizaciones, fundaciones y cooperativas de los territorios de Colombia. Diagnóstico, estrategia, narrativa, video y comunicación de proyectos. Primera conversación gratuita de 30 minutos.">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500&amp;display=swap">
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
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Soluciones digitales e inteligencia artificial" }} }}
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
        <li><a href="#sobre-mi">Sobre mí</a></li>
      </ul>
    </nav>
    <a class="btn btn--oscuro btn--chico" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-cabecera">Hablemos</a>
  </div>
</header>

<main id="contenido">

<!-- 1. PORTADA -->
<section class="hero" aria-labelledby="hero-titulo">
  <div class="hero__fondo" aria-hidden="true">
    <div class="hero__aura"></div>
    <div class="capa capa--hojas" style="--fx:-26; --fy:-14">
{hero_hojas}
    </div>
    <canvas class="polen" data-polen></canvas>
  </div>

  <div class="envoltura hero__rejilla">
    <div class="hero__texto">
      <p class="etiqueta entra entra--1"><span class="etiqueta__pin" aria-hidden="true"></span>Colombia · remoto y en territorio</p>
      <h1 id="hero-titulo" class="titulo-1 entra entra--2">Comunicación que hace visible tu trabajo</h1>
      <p class="hero__bajada entra entra--3">Acompaño a pequeñas empresas, organizaciones, fundaciones y cooperativas de los territorios de Colombia.</p>
      <div class="hero__acciones entra entra--4">
        <a class="btn btn--oscuro" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-hero">Agendar 30 minutos gratis</a>
        <a class="btn btn--borde" href="#servicios">Ver servicios</a>
      </div>
    </div>

    <div class="hero__fotos entra entra--4" data-fotos-hero>
      <figure class="ventana ventana--uno" style="--rot:-3deg;--lado:-1">{foto("gua-mavecure-rio", "Cerros de piedra sobre el río, en el Guainía", "(max-width: 640px) 31vw, (max-width: 860px) 60vw, 30vw", lazy=False, anchos=(600, 900, 1400))}</figure>
      <figure class="ventana ventana--dos" style="--rot:4deg;--lado:1">{foto("ama-raices-ceiba", "Raíces de un árbol gigante en el Amazonas", "(max-width: 640px) 31vw, (max-width: 860px) 40vw, 20vw", lazy=False, anchos=(600, 900))}</figure>
      <figure class="ventana ventana--tres" style="--rot:-2deg;--lado:-1">{foto("ama-victoria", "Victorias regias abiertas sobre el agua", "(max-width: 640px) 31vw, (max-width: 860px) 36vw, 18vw", anchos=(600, 900))}</figure>
    </div>
  </div>
</section>

<!-- 2. SERVICIOS -->
<section class="seccion servicios" id="servicios" aria-labelledby="servicios-titulo">
  <div class="envoltura">
    <div class="seccion__cabeza">
      <h2 id="servicios-titulo" class="titulo-2">En qué puedo ayudarte</h2>
      <p class="seccion__bajada">El alcance lo definimos juntos en la primera conversación.</p>
    </div>
    <ul class="servicios__rejilla">
{servicios_html()}
    </ul>
  </div>
</section>

<!-- 3. CÓMO TRABAJO -->
<section class="seccion proceso" id="proceso" aria-labelledby="proceso-titulo">
  <div class="envoltura">
    <div class="seccion__cabeza">
      <h2 id="proceso-titulo" class="titulo-2">Cómo trabajo</h2>
      <p class="seccion__bajada">Tres pasos, sin vueltas.</p>
    </div>
    <ol class="pasos">
{pasos_html()}
    </ol>
  </div>
</section>

<!-- 4. SOBRE MÍ Y TERRITORIO -->
<section class="seccion sobre" id="sobre-mi" aria-labelledby="sobre-titulo">
  <div class="envoltura">
    <div class="sobre__rejilla">
      <figure class="retrato">
        <span class="retrato__aura anim-respira" aria-hidden="true"></span>
        <div class="retrato__arco">
          <img src="/assets/gabriela-760.webp" srcset="/assets/gabriela-480.webp 480w, /assets/gabriela-760.webp 760w" sizes="(max-width: 860px) 54vw, 320px" width="760" height="950" alt="Gabriela Jiménez" loading="lazy" decoding="async">
        </div>
      </figure>
      <div class="sobre__texto">
        <h2 id="sobre-titulo" class="titulo-2">Soy Gabriela Jiménez</h2>
        <p class="parrafo-destacado">Comunicadora corporativa. He liderado la comunicación de proyectos de innovación, cooperación internacional, cultura y desarrollo rural.</p>
        <p>Trabajo escuchando primero: entiendo el contexto y construyo con cada organización, no por encima de ella.</p>
        <ul class="cifras" aria-label="Experiencia en cifras">
{cifras_html()}
        </ul>
      </div>
    </div>

    <div class="territorio">
      <p class="territorio__linea">He recorrido territorios del país, del Amazonas al Guainía, documentando el trabajo de quienes los habitan.</p>
      <div class="carril" data-carril>
{carril_html()}
      </div>
    </div>
  </div>
</section>

<!-- 5. CONTACTO -->
<section class="seccion cierre" id="contacto" aria-labelledby="cierre-titulo">
  <div class="cierre__fondo" aria-hidden="true">
    <div class="cierre__foto" data-franja>{foto("ama-orilla-bote", "", "100vw", anchos=(900, 1400))}</div>
    <div class="cierre__aura"><span class="aura-logo anim-respira"></span></div>
    <canvas class="polen polen--noche" data-polen="noche"></canvas>
    <div class="capa capa--hojas" style="--fx:-24; --fy:-12">
{cierre_hojas}
    </div>
  </div>
  <div class="envoltura cierre__contenido">
    <h2 id="cierre-titulo" class="titulo-1">Hablemos 30 minutos</h2>
    <p class="cierre__bajada">Sin costo. Revisamos tu necesidad y te digo si puedo ayudarte.</p>
    <div class="cierre__opciones">
      <a class="opcion opcion--principal" href="{AGENDA}" target="_blank" rel="noopener" data-agenda data-evento="agenda-cierre">
        <span class="opcion__titulo">Agendar videollamada</span>
        <span class="opcion__accion" data-agenda-accion>Ver horarios</span>
      </a>
      <a class="opcion" href="{WA}Hola%20Gabriela%2C%20quiero%20conversar%20sobre%20la%20comunicaci%C3%B3n%20de%20mi%20organizaci%C3%B3n." target="_blank" rel="noopener" data-evento="whatsapp-cierre">
        <span class="opcion__titulo">Escribir por WhatsApp</span>
        <span class="opcion__accion">Abrir WhatsApp</span>
      </a>
      <a class="opcion" href="mailto:{CORREO}?subject=Conversaci%C3%B3n%20sobre%20comunicaci%C3%B3n" data-evento="correo-cierre">
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

<div class="barra-movil" aria-hidden="false">
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
